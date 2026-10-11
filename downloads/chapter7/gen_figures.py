# 第7章掲載用の図を生成する（白黒印刷対応、ベクターPDF）
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "train.csv"
OUT = BASE_DIR / "figs"

if not DATA_FILE.exists():
    raise FileNotFoundError(
        "train.csv が見つかりません。README.mdを参照し、このファイルと同じフォルダーへ保存してください。"
    )

OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA_FILE)

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "pdf.fonttype": 42,
})

GRAY = "#808080"

# 図1: グループ別生存率
fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.6))
for ax, col in zip(axes, ["Pclass", "Sex", "Embarked"]):
    rates = df.groupby(col)["Survived"].mean()
    ax.bar(
        [str(v) for v in rates.index],
        rates.values,
        color=GRAY,
        edgecolor="black",
        linewidth=0.8,
    )
    ax.set_title(f"Survival Rate by {col}", fontsize=10)
    ax.set_ylabel("Survival Rate")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linewidth=0.4, alpha=0.4)
    ax.set_axisbelow(True)
    for i, value in enumerate(rates.values):
        ax.text(i, value + 0.03, f"{value:.2f}", ha="center", fontsize=8)
plt.tight_layout()
plt.savefig(OUT / "fig7_eda_survival_rates.pdf")
plt.close()

# 図2: Fareの分布
fig, ax = plt.subplots(figsize=(5.4, 3.0))
bins = np.arange(0, 300, 10)
ax.hist(
    df.loc[df["Survived"] == 0, "Fare"],
    bins=bins,
    color=GRAY,
    edgecolor="black",
    linewidth=0.5,
    label="Died (n=549)",
)
ax.hist(
    df.loc[df["Survived"] == 1, "Fare"],
    bins=bins,
    facecolor="white",
    edgecolor="black",
    linewidth=0.8,
    hatch="///",
    alpha=0.75,
    label="Survived (n=342)",
)
mean_fare = df["Fare"].mean()
median_fare = df["Fare"].median()
ax.axvline(mean_fare, color="black", linestyle="--", linewidth=1.2, label=f"Mean = {mean_fare:.1f}")
ax.axvline(median_fare, color="black", linestyle=":", linewidth=1.2, label=f"Median = {median_fare:.1f}")
ax.set_xlabel("Fare")
ax.set_ylabel("Number of Passengers")
ax.set_xlim(0, 300)
ax.legend(frameon=False, fontsize=9)
ax.grid(axis="y", linewidth=0.4, alpha=0.4)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(OUT / "fig7_fare_histogram.pdf")
plt.close()

# 図3: 調整前（既定出力のまま）と調整後（論文品質）の比較
pivot = df.pivot_table(index="Pclass", columns="Sex", values="Survived", aggfunc="mean")
counts = df.pivot_table(index="Pclass", columns="Sex", values="Survived", aggfunc="count")
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
x = np.arange(3)
w = 0.35

ax = axes[0]
ax.bar(x - w / 2, pivot["female"], w, label="female")
ax.bar(x + w / 2, pivot["male"], w, label="male")
ax.set_xticks(x, ["1", "2", "3"])
ax.set_title("(a) Default output", fontsize=10)
ax.legend()

ax = axes[1]
for shift, sex, hatch, face in [
    (-w / 2, "female", None, GRAY),
    (w / 2, "male", "///", "white"),
]:
    probabilities = pivot[sex].values
    sample_sizes = counts[sex].values
    error = 1.96 * np.sqrt(probabilities * (1 - probabilities) / sample_sizes)
    ax.bar(
        x + shift,
        probabilities,
        w,
        yerr=error,
        capsize=3,
        facecolor=face,
        edgecolor="black",
        linewidth=0.8,
        hatch=hatch,
        label=sex,
        error_kw={"linewidth": 0.9},
    )
ax.set_xticks(x, ["1st", "2nd", "3rd"])
ax.set_xlabel("Passenger Class")
ax.set_ylabel("Survival Rate")
ax.set_ylim(0, 1.05)
ax.set_title("(b) Publication quality", fontsize=10)
ax.legend(frameon=False)
ax.grid(axis="y", linewidth=0.4, alpha=0.4)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(OUT / "fig7_graph_before_after.pdf")
plt.close()

print("survival rates by Pclass:", df.groupby("Pclass")["Survived"].mean().round(3).to_dict())
print("survival rates by Sex:", df.groupby("Sex")["Survived"].mean().round(3).to_dict())
print("survival rates by Embarked:", df.groupby("Embarked")["Survived"].mean().round(3).to_dict())
print("Fare mean/median:", round(mean_fare, 1), round(median_fare, 1))
print("Fare > 300:", (df["Fare"] > 300).sum(), "passengers, max =", df["Fare"].max())
print("pivot:\n", pivot.round(3))
print("counts:\n", counts)
print("done")
