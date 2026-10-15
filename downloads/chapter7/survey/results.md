# SafeComp survey: verification edition, 2026-10-15

Historical paper values are distinguished in [the accompanying notes](README.md).

- Source data commit: `0db8336d94d97e4be11f23b72cccd45a615e985b`
- Data SHA-256: `3d58873f2cd16f436596e5446589a43a4702cbfefe9534edc8de1d7c82a4d138`
- Environment: Python 3.9.6, NumPy 2.0.2, pandas 2.3.2, SciPy 1.13.1
- Signed-rank p: exact sign distribution with average tied ranks, zeros removed.
- Signed-rank r: tie-adjusted variance, no continuity correction; omitted if n(nonzero)<10.
- Mann--Whitney p: tie-adjusted normal approximation with continuity correction; exact sensitivity below.
- Mann--Whitney r: tie-adjusted Z without continuity correction.
- Results do not establish respondent independence or industry-wide representativeness.

# Reproducibility Analysis Results

N = 30 respondents

## Respondent Profile

**Company type**: Tier 1 supplier: 17, OEM: 10, Tier 2+ supplier: 2, Tier 1 & Tier 2: 1
**Role**: Safety assessor: 11, Engineer: 8, Quality assurance: 4, Development manager: 4, Corporate FuSa promotion: 1, Standards/process: 1, Consultant: 1
**A-SPICE status**: Operating: 15, Not operating: 9, Preparing: 5, NA: 1
**ISO 26262 experience**: 5+ years: 26, 1-3 years: 2, 3-5 years: 2

## Adoption Status (Fig. 1)

| Standard | Active use | Preparing | Considering | No plans |
|----------|------------|-----------|-------------|----------|
| ISO 26262 | 28 | 0 | 1 | 1 |
| SOTIF | 3 | 18 | 5 | 4 |
| UL 4600 | 0 | 2 | 11 | 16 |

## RQ1: Perceived Benefits and Costs (Table 3)

### Descriptive Statistics

| Item | ISO n | ISO M | ISO SD | SOTIF n | SOTIF M | SOTIF SD |
|------|-------|-------|--------|---------|---------|----------|
| Safety improvement | 26 | 3.73 | 0.96 | 13 | 2.92 | 0.95 |
| Operational burden | 26 | 4.23 | 0.82 | 12 | 4.17 | 0.39 |
| Cost-effectiveness | 25 | 3.20 | 1.00 | 12 | 2.92 | 1.00 |

### Wilcoxon Signed-Rank: ISO 26262 vs SOTIF

| Item | n(pair) | n(nz) | W | p | p(Holm) | r |
|------|---------|-------|---|---|---------|---|
| Safety improvement | 12 | 8 | 2.5 | 0.0391 | 0.1172 | --- |
| Operational burden | 12 | 6 | 9.0 | 1.0000 | 1.0000 | --- |
| Cost-effectiveness | 11 | 6 | 6.0 | 0.4375 | 0.8750 | --- |

### A-SPICE Maturity Effect (Mann-Whitney U)

**ISO 26262**:

| Item | Op. n | Op. M | Not op. n | Not op. M | U | p | p(Holm) | r |
|------|-------|-------|-----------|-----------|---|---|---------|---|
| Safety improvement | 13 | 3.92 | 12 | 3.50 | 97.5 | 0.2806 | 0.6451 | 0.221 |
| Operational burden | 13 | 4.31 | 12 | 4.08 | 84.5 | 0.7234 | 0.7234 | 0.077 |
| Cost-effectiveness | 12 | 3.42 | 12 | 2.92 | 93.0 | 0.2150 | 0.6451 | 0.259 |

**SOTIF**:

| Item | Op. n | Op. M | Not op. n | Not op. M | U | p | p(Holm) | r |
|------|-------|-------|-----------|-----------|---|---|---------|---|
| Safety improvement | 8 | 3.12 | 5 | 2.60 | 25.5 | 0.4421 | 0.8841 | 0.235 |
| Operational burden | 7 | 4.14 | 5 | 4.20 | 16.5 | 0.9002 | 0.9002 | 0.072 |
| Cost-effectiveness | 7 | 3.43 | 5 | 2.20 | 29.5 | 0.0510 | 0.1531 | 0.588 |

## RQ2: Adoption Drivers (Tables 4--5)

### Descriptive Statistics

| Driver | ISO n | ISO M | ISO SD | SOTIF n | SOTIF M | SOTIF SD |
|--------|-------|-------|--------|---------|---------|----------|
| Technical safety | 28 | 4.18 | 0.90 | 20 | 3.75 | 1.12 |
| Accountability to clients | 26 | 4.08 | 1.26 | 18 | 3.78 | 1.26 |
| Accountability to end users/certifiers | 27 | 4.44 | 0.70 | 19 | 4.37 | 0.60 |
| Contract requirements | 25 | 4.44 | 1.16 | 17 | 3.47 | 1.28 |
| Conformity to industry practice | 28 | 4.25 | 0.80 | 19 | 3.58 | 0.84 |

### RQ2a: Wilcoxon Signed-Rank ISO 26262 vs SOTIF (Table 4)

| Driver | n(pair) | n(nz) | W | p | p(Holm) | r |
|--------|---------|-------|---|---|---------|---|
| Technical safety | 20 | 10 | 8.0 | 0.0566 | 0.1699 | 0.655 |
| Accountability to clients | 18 | 7 | 3.5 | 0.1094 | 0.2188 | --- |
| Accountability to end users/certifiers | 19 | 7 | 4.0 | 0.1250 | 0.2188 | --- |
| Contract requirements | 17 | 10 | 0.0 | 0.0020 | 0.0098** | 0.921 |
| Conformity to industry practice | 19 | 9 | 0.0 | 0.0039 | 0.0156* | --- |

### Friedman Test (within-standard driver comparison)

- **ISO 26262**: n=25, chi2=7.61, p=0.1068
- **SOTIF**: n=17, chi2=13.18, p=0.0104

### RQ2b: OEM vs Supplier (Mann-Whitney U, Table 5)

**ISO 26262**:

| Driver | OEM n | OEM M | Sup. n | Sup. M | U | p | p(Holm) | r |
|--------|-------|-------|--------|--------|---|---|---------|---|
| Technical safety | 9 | 4.22 | 19 | 4.16 | 95.0 | 0.6331 | 1.0000 | 0.095 |
| Accountability to clients | 8 | 3.38 | 18 | 4.39 | 40.5 | 0.0612 | 0.2447 | 0.373 |
| Accountability to end users/certifiers | 9 | 4.67 | 18 | 4.33 | 100.5 | 0.2666 | 0.7998 | 0.219 |
| Contract requirements | 7 | 3.29 | 18 | 4.89 | 22.0 | 0.0019 | 0.0095** | 0.629 |
| Conformity to industry practice | 9 | 4.22 | 19 | 4.26 | 82.5 | 0.8934 | 1.0000 | 0.030 |

**SOTIF**:

| Driver | OEM n | OEM M | Sup. n | Sup. M | U | p | p(Holm) | r |
|--------|-------|-------|--------|--------|---|---|---------|---|
| Technical safety | 8 | 3.25 | 12 | 4.08 | 29.5 | 0.1479 | 0.5667 | 0.333 |
| Accountability to clients | 7 | 3.00 | 11 | 4.27 | 23.0 | 0.1417 | 0.5667 | 0.358 |
| Accountability to end users/certifiers | 8 | 4.50 | 11 | 4.27 | 52.0 | 0.4836 | 0.9672 | 0.171 |
| Contract requirements | 6 | 2.50 | 11 | 4.00 | 12.5 | 0.0379 | 0.1895 | 0.516 |
| Conformity to industry practice | 8 | 3.50 | 11 | 3.64 | 39.5 | 0.7221 | 0.9672 | 0.092 |

## RQ3: V-Model Role Allocation (Table 6)

### Descriptive Statistics

| Activity | ISO n | ISO M | ISO SD | SOTIF n | SOTIF M | SOTIF SD |
|----------|-------|-------|--------|---------|---------|----------|
| Upper requirements definition | 26 | 1.73 | 0.83 | 13 | 1.77 | 0.83 |
| Requirements validation | 26 | 1.85 | 0.67 | 12 | 1.83 | 1.11 |
| Detailed design | 26 | 3.69 | 0.79 | 12 | 3.25 | 1.22 |
| Implementation & unit verification | 26 | 4.23 | 0.65 | 12 | 4.17 | 0.72 |
| Integration & system verification | 26 | 3.08 | 0.93 | 12 | 2.92 | 1.24 |

### RQ3a: Wilcoxon Signed-Rank ISO 26262 vs SOTIF

| Activity | n(pair) | n(nz) | W | p | p(Holm) | r |
|----------|---------|-------|---|---|---------|---|
| Upper requirements definition | 13 | 3 | 1.5 | 0.7500 | 1.0000 | --- |
| Requirements validation | 12 | 4 | 5.0 | 1.0000 | 1.0000 | --- |
| Detailed design | 12 | 3 | 0.0 | 0.2500 | 1.0000 | --- |
| Implementation & unit verification | 12 | 3 | 2.0 | 1.0000 | 1.0000 | --- |
| Integration & system verification | 12 | 5 | 6.0 | 1.0000 | 1.0000 | --- |

### RQ3b: SOTIF Boundary Clarity (One-Sample Wilcoxon)

- n = 15, mean = 1.93, SD = 0.80
- Rated 'less clear' or 'much less clear': 11 (73%)
- One-sample signed-rank test against midpoint=3: W=0.0, n_nonzero=11, p=0.000977, p(Holm)=0.0059**, r=0.910

## Multi-Standard Challenges (Table 7)

| Challenge | Count |
|-----------|-------|
| Requirement overlap | 14 |
| Scope understanding | 12 |
| Document integration | 11 |
| Terminology confusion | 10 |
| Cross-department coordination | 10 |
| Customer requirement differences | 8 |
| Priority judgment | 8 |
| No challenges | 4 |
| Not using multiple standards | 1 |
| Compliance sequencing | 1 |

## Summary: Holm-Corrected Significant Findings

With the methods and test families specified here, the following four findings survive Holm correction (p < 0.05):

1. **Contract requirements** (RQ2a): ISO > SOTIF, W=0.0, p=0.0020, p(Holm)=0.0098, r=0.921
2. **Industry conformity** (RQ2a): ISO > SOTIF, W=0.0, p=0.0039, p(Holm)=0.0156
3. **ISO 26262 contract requirements: OEM vs Supplier** (RQ2b): Supplier > OEM, U=22.0, p=0.0019, p(Holm)=0.0095, r=0.629
4. **SOTIF boundary clarity** (RQ3b): below neutral, W=0.0, p=0.000977, p(Holm)=0.0059, r=0.910

## Sensitivity: Conditional Exact OEM--Supplier Comparisons

Pooled tied ranks; exact group-label assignments; Holm over five drivers per standard.

| Standard | Driver | Exact p | Exact p(Holm) |
|---|---|---|---|
| iso26262 | Technical safety | 0.6243 | 1.0000 |
| iso26262 | Accountability to clients | 0.0597 | 0.2387 |
| iso26262 | Accountability to end users/certifiers | 0.4137 | 1.0000 |
| iso26262 | Contract requirements | 0.0043 | 0.0217 |
| iso26262 | Conformity to industry practice | 0.9469 | 1.0000 |
| sotif | Technical safety | 0.1517 | 0.5852 |
| sotif | Accountability to clients | 0.1463 | 0.5852 |
| sotif | Accountability to end users/certifiers | 0.6766 | 1.0000 |
| sotif | Contract requirements | 0.0433 | 0.2165 |
| sotif | Conformity to industry practice | 0.7841 | 1.0000 |

## Sensitivity: Boundary Clarity Sign Test
- Two-sided exact sign-test p = 0.000976562; zero differences excluded.
- This avoids using the sizes of ordinal rating differences; independence is still assumed.
