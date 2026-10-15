# 第7章掲載用の図を生成する（白黒印刷対応、ベクターPDF）
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "figs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "train.csv")

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "pdf.fonttype": 42,
})

GRAY = "#808080"

# ---------------------------------------------------------------
# 図1: グループ別生存率（本文のEDAコードの実行結果、印刷用に整えたもの)
# ---------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.6))

for ax, col in zip(axes, ["Pclass", "Sex", "Embarked"]):
    rates = df.groupby(col)["Survived"].mean()
    ax.bar([str(v) for v in rates.index], rates.values,
           color=GRAY, edgecolor="black", linewidth=0.8)
    ax.set_title(f"Survival Rate by {col}", fontsize=10)
    ax.set_ylabel("Survival Rate")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linewidth=0.4, alpha=0.4)
    ax.set_axisbelow(True)
    for i, v in enumerate(rates.values):
        ax.text(i, v + 0.03, f"{v:.2f}", ha="center", fontsize=8)

plt.tight_layout()
plt.savefig(f"{OUT}/fig7_eda_survival_rates.pdf")
plt.close()

# ---------------------------------------------------------------
# 図2: Fareの分布（生存・非生存の重ね描き、平均と中央値）
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.4, 3.0))

bins = np.arange(0, 300, 10)
ax.hist(df.loc[df["Survived"] == 0, "Fare"], bins=bins,
        color=GRAY, edgecolor="black", linewidth=0.5,
        label="Died (n=549)")
ax.hist(df.loc[df["Survived"] == 1, "Fare"], bins=bins,
        facecolor="white", edgecolor="black", linewidth=0.8,
        hatch="///", alpha=0.75, label="Survived (n=342)")

mean_fare = df["Fare"].mean()
median_fare = df["Fare"].median()
ax.axvline(mean_fare, color="black", linestyle="--", linewidth=1.2,
           label=f"Mean = {mean_fare:.1f}")
ax.axvline(median_fare, color="black", linestyle=":", linewidth=1.2,
           label=f"Median = {median_fare:.1f}")

ax.set_xlabel("Fare")
ax.set_ylabel("Number of Passengers")
ax.set_xlim(0, 300)
ax.legend(frameon=False, fontsize=9)
ax.grid(axis="y", linewidth=0.4, alpha=0.4)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig(f"{OUT}/fig7_fare_histogram.pdf")
plt.close()

# ---------------------------------------------------------------
# 図3: 調整前（既定出力のまま）と調整後（論文品質）の比較
# ---------------------------------------------------------------
pivot = df.pivot_table(index="Pclass", columns="Sex",
                       values="Survived", aggfunc="mean")
counts = df.pivot_table(index="Pclass", columns="Sex",
                        values="Survived", aggfunc="count")

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))

# (a) 既定出力のまま: 色だけで系列を区別、軸ラベルや単位の整理なし
ax = axes[0]
x = np.arange(3)
w = 0.35
ax.bar(x - w/2, pivot["female"], w, label="female")   # 既定色1
ax.bar(x + w/2, pivot["male"], w, label="male")       # 既定色2
ax.set_xticks(x, ["1", "2", "3"])
ax.set_title("(a) Default output", fontsize=10)
ax.legend()

# (b) 論文品質: ハッチングで区別、エラーバー、軸ラベル、基準線
ax = axes[1]
for shift, sex, hatch, face in [(-w/2, "female", None, GRAY),
                                (w/2, "male", "///", "white")]:
    p = pivot[sex].values
    n = counts[sex].values
    # Wilson score interval: asymmetric and bounded by 0 and 1.
    z = 1.959963984540054
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denominator
    half_width = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    lower, upper = center - half_width, center + half_width
    err = np.vstack([p - lower, upper - p])
    ax.bar(x + shift, p, w, yerr=err, capsize=3,
           facecolor=face, edgecolor="black", linewidth=0.8,
           hatch=hatch, label=sex,
           error_kw={"linewidth": 0.9})
ax.set_xticks(x, ["1st", "2nd", "3rd"])
ax.set_xlabel("Passenger Class")
ax.set_ylabel("Survival Rate")
ax.set_ylim(0, 1.0)
ax.set_title("(b) Publication quality", fontsize=10)
ax.legend(frameon=False)
ax.grid(axis="y", linewidth=0.4, alpha=0.4)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig(f"{OUT}/fig7_graph_before_after.pdf")
plt.close()

# 数値の記録（キャプション用）
print("survival rates by Pclass:", df.groupby("Pclass")["Survived"].mean().round(3).to_dict())
print("survival rates by Sex:", df.groupby("Sex")["Survived"].mean().round(3).to_dict())
print("survival rates by Embarked:", df.groupby("Embarked")["Survived"].mean().round(3).to_dict())
print("Fare mean/median:", round(mean_fare, 1), round(median_fare, 1))
print("Fare > 300:", (df["Fare"] > 300).sum(), "passengers, max =", df["Fare"].max())
print("pivot:\n", pivot.round(3))
print("counts:\n", counts)
print("done")
