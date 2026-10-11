# 第7章のコードを忠実に実行し、本文の数値を検証する
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


DATA_FILE = Path(__file__).with_name("train.csv")
if not DATA_FILE.exists():
    raise FileNotFoundError(
        "train.csv が見つかりません。README.mdを参照し、このファイルと同じフォルダーへ保存してください。"
    )

df = pd.read_csv(DATA_FILE)

print("=== Step 1: データの意味 ===")
print("shape:", df.shape, "(本文: (891, 12))")

print("\n=== Step 2: 欠損値 ===")
missing_count = df.isnull().sum()
missing_rate = (df.isnull().sum() / len(df) * 100).round(1)
for col in ["Age", "Cabin", "Embarked"]:
    print(f"{col}: {missing_count[col]}件 ({missing_rate[col]}%)")
print("(本文: Age 177件19.9% / Cabin 687件77.1% / Embarked 2件0.2%)")

print("\n=== Step 3: EDA ===")
print("生存率:", round(df["Survived"].mean() * 100, 1), "% (本文: 38.4%)")
print(
    "全員死亡と予測した場合の正解率:",
    round((1 - df["Survived"].mean()) * 100, 1),
    "% (本文: 約62%)",
)

# 前処理（欠損値を埋める前に訓練用と評価用へ分割する）
df_work = df.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
df_work["Sex"] = df_work["Sex"].map({"male": 0, "female": 1})

X = df_work.drop("Survived", axis=1)
y = df_work["Survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 補完に使う値は訓練データだけから決める
age_median = X_train["Age"].median()
embarked_mode = X_train["Embarked"].mode()[0]
fill = {"Age": age_median, "Embarked": embarked_mode}
X_train = X_train.fillna(fill)
X_test = X_test.fillna(fill)

# 両方に同じカテゴリを指定し、Cを基準に符号化する
embarked_type = pd.CategoricalDtype(categories=["C", "Q", "S"])
X_train["Embarked"] = X_train["Embarked"].astype(embarked_type)
X_test["Embarked"] = X_test["Embarked"].astype(embarked_type)

X_train = pd.get_dummies(X_train, columns=["Embarked"], drop_first=True, dtype=int)
X_test = pd.get_dummies(X_test, columns=["Embarked"], drop_first=True, dtype=int)

print("\n=== 前処理後 ===")
print("補完値: Age中央値", age_median, "/ Embarked最頻値", embarked_mode)
print("（全データの中央値は", df["Age"].median(), "。訓練データだけで決めるため一致しない）")
print("説明変数の列数:", X_train.shape[1], "(本文: 8列)")
print("列:", list(X_train.columns))

print("\n=== モデル ===")
print("訓練:", len(X_train), "評価:", len(X_test), "(本文: 712 / 179)")

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)
cm = confusion_matrix(y_test, pred)
print("正解率:", round(acc, 3), "(本文: 0.804)")
print("混同行列:\n", cm, "\n(本文: TN98 FP12 / FN23 TP46)")
tn, fp, fn, tp = cm.ravel()
print("生存者の再現率:", round(tp / (tp + fn), 3), "(本文: 0.667)")

print("\n=== 係数 ===")
for name, coef in zip(X_train.columns, model.coef_[0]):
    print(f"{name}: {coef:+.3f}")
print("(本文: Sex +2.558 / Pclass -1.093 / Fare +0.002)")
