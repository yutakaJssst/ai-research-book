# 『生成AI時代の検証可能な研究術』Webサポート

松野 裕『生成AI時代の検証可能な研究術――文献調査、分析、執筆、発表の基本と実践』の教材を公開するリポジトリです。

[Webサポートを開く](https://yutakajssst.github.io/ai-research-book/)

## 教材

- `index.html`：章別の教材、コピーして使うプロンプト、配布ファイル、更新・正誤情報
- `downloads/`：AI活用記録票、文献整理シート、提出前確認シート、Pythonコード、Colabノートブック
- `slides/`：Webサポートから参照する授業スライドと表示用CSS
- `guides/`：画面例付きの操作ガイド
- `assets/chapter8/`：第8章操作ガイドの画面例と出典

本文は研究の進め方と判断の理由を扱い、このサイトでは実際に手を動かすための資料を提供します。
対応原稿は2026年10月24日改訂版です。

大学院の授業と研究の実例から、AIと進める文献調査、分析、執筆、発表を学ぶ本です。
理工系大学院生に加え、企業の研究開発者や技術者にも活用していただける内容です。
第9章の[数学の補足](https://yutakajssst.github.io/ai-research-book/guides/ai-math.html)には、件数と更新履歴、確認日、公式資料の参照した版を掲載しています。

第8章の[操作ガイド](https://yutakajssst.github.io/ai-research-book/guides/github-pages.html)は、GitHub Desktopでの記録からGitHub Pagesの公開・更新までを扱います。
WindowsとmacOSの違い、AIへの相談例、操作後の確認を掲載しています。
画面例はGitHub DocsのCC BY 4.0の画像を転載し、出典をガイドと `assets/chapter8/README.md` に記録しています。

## ノートブック

- [第6章：平均値関数とテストをColabで開く](https://colab.research.google.com/github/yutakaJssst/ai-research-book/blob/main/downloads/chapter6/average-tests.ipynb)
- [第7章：Titanic分析をColabで開く](https://colab.research.google.com/github/yutakaJssst/ai-research-book/blob/main/downloads/chapter7/titanic-walkthrough.ipynb)

Titanicのデータはノートブックから取得します。
付属の検証・図生成コードは、このリポジトリの特定コミットから取得し、実行する版を固定しています。
CSVはExcelでも日本語を読み込めるUTF-8 BOM付き、その他の配布テキストはUTF-8です。

## 利用条件

コードはMIT License、文書、スライド、記入シート、プロンプトはCC BY 4.0で提供します。
学生の提出物に基づく例、引用した他者の著作物、外部から取得するデータは対象外です。
詳細は [LICENSE.md](LICENSE.md) を参照してください。
誤りの報告は [Issues](https://github.com/yutakaJssst/ai-research-book/issues) からお願いします。

## 2026年10月24日の更新

- 刊行前レビューを受け、旧授業スライドの助言を本文にそろえた（第2章スライドの確信度の自己申告と文献を渡さない新規性評価の例、第4章スライドの新規性の質問）。
- 誤りの報告先と教材の利用条件を明記し、`LICENSE.md` を追加した。
- 数学の例の件数と訂正履歴を、確認日付きの第9章補足へ移した。
- 書籍の紹介文と、第6章の入出力の照合、第8章の他者による再実行・公開確認の案内を更新した。
- 配布資料の対応原稿日付と、第9章からの補足への案内をそろえた。

## 2026年10月20日の更新

- 最終稿（2026年10月19日改訂）に対応。
- `downloads/chapter7/survey/README.md` を、同順位の処理と解釈の限界の説明に絞った。
- 記録票の記入例と操作ガイドの表記を本文の規約にそろえた。

## 2026年10月15日の整合確認

- Titanic図の95％信頼区間をWilson法へ変更。本文の図生成コードと配布版は同一。
- データ分析スライドは、分割→訓練側で補完値の決定→同じ変換を両側へ適用する順序に修正。
- 英語推敲PDFの先頭に、意味と構造から始める現行4段階の補足を追加。原授業スライドは補足の後に保持。
- `downloads/chapter7/survey/` に、公開データの版を固定した統計検算コード、訂正・限界の説明、再計算結果を掲載。刊行論文の書き換えと区別する。

## 公開と更新

GitHub Pagesの公開元は `main` ブランチのルートです。
教材を更新するときは、サイト内の案内、配布ファイル、ノートブックの内容をそろえ、`index.html` の更新履歴に記録してください。
リンク、文字コード、Colabの取得先を確認してからpushします。

授業全体の資料は[情報論のサイト](https://yutakajssst.github.io/InformationTheory/)で公開しています。
旧Webサポートの入口には移転案内を置き、配布ファイルの旧URLも利用できるようにしています。

## ローカルでの確認

```sh
python3 -m http.server 8000
```

ブラウザで `http://localhost:8000/` を開いてください。
