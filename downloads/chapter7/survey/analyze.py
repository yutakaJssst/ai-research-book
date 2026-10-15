#!/usr/bin/env python3
"""Recheck the SafeComp survey using tie-aware signed-rank calculations.

Adapted from the author's public reproduction script at commit
0db8336d94d97e4be11f23b72cccd45a615e985b:
https://github.com/yutakaJssst/SafeComp2026SurveyQuestionnaire

This 2026-10-15 verification edition corrects tied signed ranks and their
variance. Historical paper values and limitations are described in README.md.
It does not replace the published paper or establish respondent independence.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import platform
from collections import Counter
from urllib.request import urlopen
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats


# ============================================================================
# Statistical test functions
# ============================================================================

def signed_rank(diff) -> Dict[str, float]:
    """Two-sided conditional exact signed-rank p, retaining average tied ranks.

    Zero differences are removed (Wilcox convention). Each nonzero sign is
    equiprobable under the symmetric null. Integer counts enumerate the full
    sign distribution by dynamic programming, without random simulation.
    This script is intended for this small, integer-valued survey (n <= 30).
    r uses the tied-rank variance without continuity correction; it is an
    approximate standardized effect, separate from the exact p-value.
    """
    d = np.asarray(diff, dtype=float)
    d = d[np.isfinite(d)]
    nz = d[d != 0]
    n = len(nz)
    if not n:
        return {"n_nonzero": 0, "W": 0.0, "p": 1.0, "r": 0.0}
    ranks = stats.rankdata(np.abs(nz), method="average")
    doubled = np.rint(2 * ranks).astype(int)
    target = int(doubled[nz > 0].sum())
    distribution = {0: 1}
    for rank in doubled:
        updated = distribution.copy()
        for total, ways in distribution.items():
            key = total + int(rank)
            updated[key] = updated.get(key, 0) + ways
        distribution = updated
    low = sum(ways for total, ways in distribution.items() if total <= target)
    high = sum(ways for total, ways in distribution.items() if total >= target)
    p = min(1.0, 2 * min(low, high) / 2**n)
    positive = float(ranks[nz > 0].sum())
    w = min(positive, float(ranks.sum()) - positive)
    variance = float(np.sum(ranks**2)) / 4
    mean = float(ranks.sum()) / 2
    r = abs(positive - mean) / math.sqrt(variance * n) if n >= 10 else float("nan")
    return {"n_nonzero": n, "W": w, "p": p, "r": r}


def wilcoxon_paired(x: pd.Series, y: pd.Series) -> Dict[str, float]:
    """Pairwise complete observations; exclude zero differences before ranks."""
    mask = x.notna() & y.notna()
    if not mask.any():
        return {"n_pair": 0, "n_nonzero": 0, "W": float("nan"),
                "p": float("nan"), "r": float("nan")}
    return {"n_pair": int(mask.sum()), **signed_rank(x[mask].to_numpy() - y[mask].to_numpy())}


def mann_whitney_u(x: pd.Series, y: pd.Series) -> Dict[str, float]:
    """Mann-Whitney U test with tie-corrected effect size."""
    xv, yv = x.dropna().values, y.dropna().values
    n1, n2 = len(xv), len(yv)
    if n1 == 0 or n2 == 0:
        return {"n1": n1, "n2": n2, "U": float("nan"),
                "p": float("nan"), "r": float("nan")}
    res = stats.mannwhitneyu(xv, yv, alternative="two-sided",
                             method="asymptotic", use_continuity=True)
    combined = np.concatenate([xv, yv])
    _, counts = np.unique(combined, return_counts=True)
    N = n1 + n2
    mean_u = n1 * n2 / 2
    tie_correction = sum(int(c) ** 3 - int(c) for c in counts if c > 1)
    var_u = n1 * n2 / 12 * ((N + 1) - tie_correction / (N * (N - 1))) if N > 1 else n1 * n2 * (N + 1) / 12
    z = (res.statistic - mean_u) / math.sqrt(var_u) if var_u > 0 else 0.0
    r = min(abs(z) / math.sqrt(N), 1.0)
    return {"n1": int(n1), "n2": int(n2), "U": float(res.statistic),
            "p": float(res.pvalue), "r": float(r)}


def one_sample_wilcoxon(x: pd.Series, median: float = 3.0) -> Dict[str, float]:
    """Signed-rank test against midpoint 3; location interpretation needs symmetry."""
    xv = x.dropna().to_numpy()
    if not len(xv):
        return {"n": 0, "n_nonzero": 0, "W": float("nan"),
                "p": float("nan"), "r": float("nan")}
    return {"n": len(xv), **signed_rank(xv - median)}


def mann_whitney_exact(x, y) -> float:
    """Conditional exact two-sided rank-sum test, allowing pooled ties.

    Count all group-label assignments. A tied group contributes comb(t, k)
    assignments when k of its t observations are allocated to group x.
    The two-sided convention is twice the smaller inclusive tail.
    """
    a, b = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    if not len(a) or not len(b):
        return float("nan")
    values = np.concatenate([a, b])
    ranks = np.rint(2 * stats.rankdata(values, method="average")).astype(int)
    target = int(ranks[:len(a)].sum())
    groups = Counter(ranks)
    distribution = {(0, 0): 1}
    for rank, count in groups.items():
        updated = {}
        for (selected, total), ways in distribution.items():
            for k in range(min(count, len(a) - selected) + 1):
                key = (selected + k, total + k * int(rank))
                updated[key] = updated.get(key, 0) + ways * math.comb(count, k)
        distribution = updated
    low = sum(v for (k, t), v in distribution.items() if k == len(a) and t <= target)
    high = sum(v for (k, t), v in distribution.items() if k == len(a) and t >= target)
    return min(1.0, 2 * min(low, high) / math.comb(len(values), len(a)))


def friedman_test(df_sub: pd.DataFrame) -> Tuple[int, float, float]:
    """Friedman test across columns (listwise deletion of NaN)."""
    clean = df_sub.dropna()
    n = len(clean)
    if n == 0:
        return 0, float("nan"), float("nan")
    stat, p = stats.friedmanchisquare(*[clean[col] for col in clean.columns])
    return n, float(stat), float(p)


def holm_correction(pvals: List[float]) -> List[float]:
    """Apply Holm-Bonferroni step-down correction."""
    arr = np.array(pvals, dtype=float)
    adj = np.full_like(arr, np.nan)
    mask = ~np.isnan(arr)
    if mask.sum() == 0:
        return adj.tolist()
    vals = arr[mask]
    m = len(vals)
    order = np.argsort(vals)
    prev = 0.0
    out = np.empty(m)
    for rank, idx in enumerate(order):
        adj_val = (m - rank) * vals[idx]
        prev = max(prev, adj_val)
        out[idx] = min(prev, 1.0)
    adj[mask] = out
    return adj.tolist()


def desc(s: pd.Series) -> Tuple[int, float, float]:
    """Return n, mean, SD for a numeric series (dropping NaN)."""
    v = s.dropna()
    n = len(v)
    if n == 0:
        return 0, float("nan"), float("nan")
    if n == 1:
        return 1, float(v.mean()), float("nan")
    return n, float(v.mean()), float(v.std(ddof=1))


# ============================================================================
# Formatting helpers
# ============================================================================

def fp(p):
    if math.isnan(p): return "---"
    return f"{p:.6f}" if p < 0.001 else f"{p:.4f}"

def fr(r):
    if math.isnan(r): return "---"
    return f"{r:.3f}"

def ff(v, d=2):
    if math.isnan(v): return "---"
    return f"{v:.{d}f}"

def sig(p_holm):
    if math.isnan(p_holm): return ""
    if p_holm < 0.001: return "***"
    if p_holm < 0.01: return "**"
    if p_holm < 0.05: return "*"
    return ""


# ============================================================================
# Column name definitions
# ============================================================================

DRIVER_COLS = ["technical_safety", "2nd_party_accountability",
               "3rd_party_accountability", "contract_requirements",
               "industry_conformity"]
DRIVER_LABELS = {
    "technical_safety": "Technical safety",
    "2nd_party_accountability": "Accountability to clients",
    "3rd_party_accountability": "Accountability to end users/certifiers",
    "contract_requirements": "Contract requirements",
    "industry_conformity": "Conformity to industry practice",
}

BC_COLS = ["safety_improvement", "operational_burden", "cost_effectiveness"]
BC_LABELS = {
    "safety_improvement": "Safety improvement",
    "operational_burden": "Operational burden",
    "cost_effectiveness": "Cost-effectiveness",
}

ROLE_COLS = ["upper_requirements", "validation", "detailed_design",
             "implementation", "integration"]
ROLE_LABELS = {
    "upper_requirements": "Upper requirements definition",
    "validation": "Requirements validation",
    "detailed_design": "Detailed design",
    "implementation": "Implementation & unit verification",
    "integration": "Integration & system verification",
}


# ============================================================================
# Main analysis
# ============================================================================

def run_analysis(df: pd.DataFrame) -> str:
    lines: List[str] = []
    lines.append("# Reproducibility Analysis Results")
    lines.append("")
    lines.append(f"N = {len(df)} respondents")
    lines.append("")

    # --- Profile ---
    lines.append("## Respondent Profile")
    lines.append("")
    for col, label in [("company_type", "Company type"),
                       ("role", "Role"),
                       ("aspice_status", "A-SPICE status"),
                       ("iso26262_experience", "ISO 26262 experience")]:
        vc = df[col].value_counts(dropna=False)
        lines.append(f"**{label}**: " + ", ".join(
            f"{'NA' if pd.isna(v) else v}: {c}" for v, c in vc.items()
        ))
    lines.append("")

    # --- Adoption status ---
    lines.append("## Adoption Status (Fig. 1)")
    lines.append("")
    lines.append("| Standard | Active use | Preparing | Considering | No plans |")
    lines.append("|----------|------------|-----------|-------------|----------|")
    for std, col in [("ISO 26262", "iso26262_adoption"),
                     ("SOTIF", "sotif_adoption"), ("UL 4600", "ul4600_adoption")]:
        vc = df[col].value_counts()
        lines.append(f"| {std} | {vc.get('Active use', 0)} | {vc.get('Preparing', 0)} "
                     f"| {vc.get('Considering', 0)} | {vc.get('No plans', 0)} |")
    lines.append("")

    # ------------------------------------------------------------------
    # RQ1: Perceived benefits and costs
    # ------------------------------------------------------------------
    lines.append("## RQ1: Perceived Benefits and Costs (Table 3)")
    lines.append("")
    lines.append("### Descriptive Statistics")
    lines.append("")
    lines.append("| Item | ISO n | ISO M | ISO SD | SOTIF n | SOTIF M | SOTIF SD |")
    lines.append("|------|-------|-------|--------|---------|---------|----------|")
    for item in BC_COLS:
        ni, mi, si = desc(df[f"iso26262_{item}"])
        ns, ms, ss = desc(df[f"sotif_{item}"])
        lines.append(f"| {BC_LABELS[item]} | {ni} | {ff(mi)} | {ff(si)} "
                     f"| {ns} | {ff(ms)} | {ff(ss)} |")
    lines.append("")

    # Wilcoxon paired ISO vs SOTIF
    lines.append("### Wilcoxon Signed-Rank: ISO 26262 vs SOTIF")
    lines.append("")
    rq1_results = []
    for item in BC_COLS:
        res = wilcoxon_paired(df[f"iso26262_{item}"], df[f"sotif_{item}"])
        rq1_results.append((BC_LABELS[item], res))
    rq1_holm = holm_correction([r["p"] for _, r in rq1_results])

    lines.append("| Item | n(pair) | n(nz) | W | p | p(Holm) | r |")
    lines.append("|------|---------|-------|---|---|---------|---|")
    for i, (label, res) in enumerate(rq1_results):
        lines.append(f"| {label} | {res['n_pair']} | {res['n_nonzero']} "
                     f"| {ff(res['W'],1)} | {fp(res['p'])} "
                     f"| {fp(rq1_holm[i])}{sig(rq1_holm[i])} | {fr(res['r'])} |")
    lines.append("")

    # A-SPICE maturity effect
    lines.append("### A-SPICE Maturity Effect (Mann-Whitney U)")
    lines.append("")
    oem_mask = df["company_type"] == "OEM"
    aspice_op = df["aspice_status"] == "Operating"
    aspice_not = df["aspice_status"].isin(["Not operating", "Preparing"])

    for std_lbl, prefix in [("ISO 26262", "iso26262"), ("SOTIF", "sotif")]:
        lines.append(f"**{std_lbl}**:")
        lines.append("")
        lines.append("| Item | Op. n | Op. M | Not op. n | Not op. M | U | p | p(Holm) | r |")
        lines.append("|------|-------|-------|-----------|-----------|---|---|---------|---|")
        mat_results = []
        for item in BC_COLS:
            col = f"{prefix}_{item}"
            x = df.loc[aspice_op, col]
            y = df.loc[aspice_not, col]
            res = mann_whitney_u(x, y)
            nx, mx, _ = desc(x)
            ny, my, _ = desc(y)
            mat_results.append((BC_LABELS[item], nx, mx, ny, my, res))
        mat_holm = holm_correction([r["p"] for *_, r in mat_results])
        for i, (label, nx, mx, ny, my, res) in enumerate(mat_results):
            lines.append(f"| {label} | {nx} | {ff(mx)} | {ny} | {ff(my)} "
                         f"| {ff(res['U'],1)} | {fp(res['p'])} "
                         f"| {fp(mat_holm[i])}{sig(mat_holm[i])} | {fr(res['r'])} |")
        lines.append("")

    # ------------------------------------------------------------------
    # RQ2: Adoption drivers
    # ------------------------------------------------------------------
    lines.append("## RQ2: Adoption Drivers (Tables 4--5)")
    lines.append("")
    lines.append("### Descriptive Statistics")
    lines.append("")
    lines.append("| Driver | ISO n | ISO M | ISO SD | SOTIF n | SOTIF M | SOTIF SD |")
    lines.append("|--------|-------|-------|--------|---------|---------|----------|")
    for item in DRIVER_COLS:
        ni, mi, si = desc(df[f"iso26262_drv_{item}"])
        ns, ms, ss = desc(df[f"sotif_drv_{item}"])
        lines.append(f"| {DRIVER_LABELS[item]} | {ni} | {ff(mi)} | {ff(si)} "
                     f"| {ns} | {ff(ms)} | {ff(ss)} |")
    lines.append("")

    # Wilcoxon paired (RQ2a)
    lines.append("### RQ2a: Wilcoxon Signed-Rank ISO 26262 vs SOTIF (Table 4)")
    lines.append("")
    rq2a_results = []
    for item in DRIVER_COLS:
        res = wilcoxon_paired(df[f"iso26262_drv_{item}"], df[f"sotif_drv_{item}"])
        rq2a_results.append((DRIVER_LABELS[item], res))
    rq2a_holm = holm_correction([r["p"] for _, r in rq2a_results])

    lines.append("| Driver | n(pair) | n(nz) | W | p | p(Holm) | r |")
    lines.append("|--------|---------|-------|---|---|---------|---|")
    for i, (label, res) in enumerate(rq2a_results):
        lines.append(f"| {label} | {res['n_pair']} | {res['n_nonzero']} "
                     f"| {ff(res['W'],1)} | {fp(res['p'])} "
                     f"| {fp(rq2a_holm[i])}{sig(rq2a_holm[i])} | {fr(res['r'])} |")
    lines.append("")

    # Friedman
    lines.append("### Friedman Test (within-standard driver comparison)")
    lines.append("")
    for std_lbl, prefix in [("ISO 26262", "iso26262_drv"), ("SOTIF", "sotif_drv")]:
        cols_df = df[[f"{prefix}_{d}" for d in DRIVER_COLS]]
        n, chi2, p = friedman_test(cols_df)
        lines.append(f"- **{std_lbl}**: n={n}, chi2={ff(chi2,2)}, p={fp(p)}")
    lines.append("")

    # OEM vs Supplier (RQ2b)
    lines.append("### RQ2b: OEM vs Supplier (Mann-Whitney U, Table 5)")
    lines.append("")
    for std_lbl, prefix in [("ISO 26262", "iso26262_drv"), ("SOTIF", "sotif_drv")]:
        lines.append(f"**{std_lbl}**:")
        lines.append("")
        lines.append("| Driver | OEM n | OEM M | Sup. n | Sup. M | U | p | p(Holm) | r |")
        lines.append("|--------|-------|-------|--------|--------|---|---|---------|---|")
        oem_results = []
        for item in DRIVER_COLS:
            col = f"{prefix}_{item}"
            res = mann_whitney_u(df.loc[oem_mask, col], df.loc[~oem_mask, col])
            no, mo, _ = desc(df.loc[oem_mask, col])
            ns, ms, _ = desc(df.loc[~oem_mask, col])
            oem_results.append((DRIVER_LABELS[item], no, mo, ns, ms, res))
        oem_holm = holm_correction([r["p"] for *_, r in oem_results])
        for i, (label, no, mo, ns, ms, res) in enumerate(oem_results):
            lines.append(f"| {label} | {no} | {ff(mo)} | {ns} | {ff(ms)} "
                         f"| {ff(res['U'],1)} | {fp(res['p'])} "
                         f"| {fp(oem_holm[i])}{sig(oem_holm[i])} | {fr(res['r'])} |")
        lines.append("")

    # ------------------------------------------------------------------
    # RQ3: V-model role allocation
    # ------------------------------------------------------------------
    lines.append("## RQ3: V-Model Role Allocation (Table 6)")
    lines.append("")
    lines.append("### Descriptive Statistics")
    lines.append("")
    lines.append("| Activity | ISO n | ISO M | ISO SD | SOTIF n | SOTIF M | SOTIF SD |")
    lines.append("|----------|-------|-------|--------|---------|---------|----------|")
    for item in ROLE_COLS:
        ni, mi, si = desc(df[f"iso26262_role_{item}"])
        ns, ms, ss = desc(df[f"sotif_role_{item}"])
        lines.append(f"| {ROLE_LABELS[item]} | {ni} | {ff(mi)} | {ff(si)} "
                     f"| {ns} | {ff(ms)} | {ff(ss)} |")
    lines.append("")

    # Wilcoxon paired (RQ3a) + boundary clarity (RQ3b) — single Holm family (6 tests)
    lines.append("### RQ3a: Wilcoxon Signed-Rank ISO 26262 vs SOTIF")
    lines.append("")
    rq3a_results = []
    for item in ROLE_COLS:
        res = wilcoxon_paired(df[f"iso26262_role_{item}"], df[f"sotif_role_{item}"])
        rq3a_results.append((ROLE_LABELS[item], res))

    # RQ3b: boundary clarity
    boundary = df["sotif_boundary_clarity"]
    b_res = one_sample_wilcoxon(boundary, median=3.0)

    # Holm correction over all 6 RQ3 tests (5 role + 1 boundary)
    rq3_pvals = [r["p"] for _, r in rq3a_results] + [b_res["p"]]
    rq3_holm = holm_correction(rq3_pvals)

    lines.append("| Activity | n(pair) | n(nz) | W | p | p(Holm) | r |")
    lines.append("|----------|---------|-------|---|---|---------|---|")
    for i, (label, res) in enumerate(rq3a_results):
        lines.append(f"| {label} | {res['n_pair']} | {res['n_nonzero']} "
                     f"| {ff(res['W'],1)} | {fp(res['p'])} "
                     f"| {fp(rq3_holm[i])}{sig(rq3_holm[i])} | {fr(res['r'])} |")
    lines.append("")

    lines.append("### RQ3b: SOTIF Boundary Clarity (One-Sample Wilcoxon)")
    lines.append("")
    nb, mb, sb = desc(boundary)
    ambig = int(((boundary == 1) | (boundary == 2)).sum())
    rq3b_holm_p = rq3_holm[5]  # 6th test in the family
    lines.append(f"- n = {nb}, mean = {ff(mb)}, SD = {ff(sb)}")
    lines.append(f"- Rated 'less clear' or 'much less clear': {ambig} ({ambig*100//nb}%)")
    lines.append(f"- One-sample signed-rank test against midpoint=3: "
                 f"W={ff(b_res['W'],1)}, n_nonzero={b_res['n_nonzero']}, "
                 f"p={fp(b_res['p'])}, p(Holm)={fp(rq3b_holm_p)}{sig(rq3b_holm_p)}, "
                 f"r={fr(b_res['r'])}")
    lines.append("")

    # ------------------------------------------------------------------
    # Multi-standard challenges
    # ------------------------------------------------------------------
    lines.append("## Multi-Standard Challenges (Table 7)")
    lines.append("")
    challenge_counts = {}
    for val in df["multi_standard_challenges"].dropna():
        for part in str(val).split("; "):
            part = part.strip()
            if part:
                challenge_counts[part] = challenge_counts.get(part, 0) + 1
    sorted_ch = sorted(challenge_counts.items(), key=lambda x: -x[1])
    lines.append("| Challenge | Count |")
    lines.append("|-----------|-------|")
    for ch, cnt in sorted_ch:
        lines.append(f"| {ch} | {cnt} |")
    lines.append("")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    lines.append("## Summary: Holm-Corrected Significant Findings")
    lines.append("")
    lines.append("With the methods and test families specified here, the following four findings survive Holm correction (p < 0.05):")
    lines.append("")

    cr = rq2a_results[3][1]
    lines.append(f"1. **Contract requirements** (RQ2a): ISO > SOTIF, "
                 f"W={ff(cr['W'],1)}, p={fp(cr['p'])}, "
                 f"p(Holm)={fp(rq2a_holm[3])}, r={fr(cr['r'])}")

    ic = rq2a_results[4][1]
    lines.append(f"2. **Industry conformity** (RQ2a): ISO > SOTIF, "
                 f"W={ff(ic['W'],1)}, p={fp(ic['p'])}, "
                 f"p(Holm)={fp(rq2a_holm[4])}")

    # Recalculate ISO contract OEM/Supplier for summary
    cr_mwu = mann_whitney_u(df.loc[oem_mask, "iso26262_drv_contract_requirements"],
                            df.loc[~oem_mask, "iso26262_drv_contract_requirements"])
    iso_oem_pvals = []
    for item in DRIVER_COLS:
        col = f"iso26262_drv_{item}"
        iso_oem_pvals.append(mann_whitney_u(
            df.loc[oem_mask, col], df.loc[~oem_mask, col])["p"])
    iso_oem_holm = holm_correction(iso_oem_pvals)
    lines.append(f"3. **ISO 26262 contract requirements: OEM vs Supplier** (RQ2b): "
                 f"Supplier > OEM, U={ff(cr_mwu['U'],1)}, p={fp(cr_mwu['p'])}, "
                 f"p(Holm)={fp(iso_oem_holm[3])}, r={fr(cr_mwu['r'])}")

    lines.append(f"4. **SOTIF boundary clarity** (RQ3b): below neutral, "
                 f"W={ff(b_res['W'],1)}, p={fp(b_res['p'])}, "
                 f"p(Holm)={fp(rq3b_holm_p)}, r={fr(b_res['r'])}")
    lines.append("")

    lines.append("## Sensitivity: Conditional Exact OEM--Supplier Comparisons")
    lines.append("")
    lines.append("Pooled tied ranks; exact group-label assignments; Holm over five drivers per standard.")
    lines.append("")
    lines.append("| Standard | Driver | Exact p | Exact p(Holm) |")
    lines.append("|---|---|---|---|")
    for standard in ["iso26262", "sotif"]:
        exact_ps = [mann_whitney_exact(
            df.loc[oem_mask, f"{standard}_drv_{item}"],
            df.loc[~oem_mask, f"{standard}_drv_{item}"]) for item in DRIVER_COLS]
        corrected = holm_correction(exact_ps)
        for item, p, adjusted in zip(DRIVER_COLS, exact_ps, corrected):
            lines.append(f"| {standard} | {DRIVER_LABELS[item]} | {fp(p)} | {fp(adjusted)} |")
    lines.append("")
    lines.append("## Sensitivity: Boundary Clarity Sign Test")
    nonzero_boundary = boundary.dropna() - 3
    nonzero_boundary = nonzero_boundary[nonzero_boundary != 0]
    sign_p = stats.binomtest(int((nonzero_boundary > 0).sum()), len(nonzero_boundary), 0.5).pvalue
    lines.append(f"- Two-sided exact sign-test p = {sign_p:.9f}; zero differences excluded.")
    lines.append("- This avoids using the sizes of ordinal rating differences; independence is still assumed.")
    lines.append("")
    return "\n".join(lines)


SOURCE_COMMIT = "0db8336d94d97e4be11f23b72cccd45a615e985b"
DATA_URL = ("https://raw.githubusercontent.com/yutakaJssst/"
            f"SafeComp2026SurveyQuestionnaire/{SOURCE_COMMIT}/data/responses.csv")
DATA_SHA256 = "3d58873f2cd16f436596e5446589a43a4702cbfefe9534edc8de1d7c82a4d138"


def main():
    parser = argparse.ArgumentParser(description="Recheck survey statistics with tied ranks")
    parser.add_argument("--input", type=Path, help="Optional local copy of the public responses.csv")
    parser.add_argument("--output", type=Path, help="Save the aggregate Markdown report")
    args = parser.parse_args()
    if args.input is None:
        with urlopen(DATA_URL, timeout=30) as response:
            raw = response.read()
    else:
        raw = args.input.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != DATA_SHA256:
        raise ValueError("Data SHA-256 differs from the pinned public survey; review its source before use.")
    df = pd.read_csv(io.BytesIO(raw))
    for col in df.columns:
        if col.endswith(("_safety", "_accountability", "_requirements", "_conformity",
                         "_improvement", "_burden", "_effectiveness")) or "_role_" in col or col.endswith("_boundary_clarity"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
    import scipy
    header = ("# SafeComp survey: verification edition, 2026-10-15\n\n"
              "Historical paper values are distinguished in [the accompanying notes](README.md).\n\n"
              f"- Source data commit: `{SOURCE_COMMIT}`\n"
              f"- Data SHA-256: `{digest}`\n"
              f"- Environment: Python {platform.python_version()}, NumPy {np.__version__}, "
              f"pandas {pd.__version__}, SciPy {scipy.__version__}\n"
              "- Signed-rank p: exact sign distribution with average tied ranks, zeros removed.\n"
              "- Signed-rank r: tie-adjusted variance, no continuity correction; omitted if n(nonzero)<10.\n"
              "- Mann--Whitney p: tie-adjusted normal approximation with continuity correction; exact sensitivity below.\n"
              "- Mann--Whitney r: tie-adjusted Z without continuity correction.\n"
              "- Results do not establish respondent independence or industry-wide representativeness.\n\n")
    report = (header + run_analysis(df)).rstrip() + "\n"
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
