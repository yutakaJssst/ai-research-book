# 第8章：情報メモとGitHub Pagesの公開手順

2026年10月11日改訂の原稿に対応。

## AIに渡す情報を整理する

プロンプトを書く前に、ページに載せる情報をメモにします。
氏名と所属は架空の記入例です。
自分が公開してよい情報だけを記入してください。

| 項目 | 記入例 | 自分の情報 |
|---|---|---|
| 氏名 | 山田 太郎 | |
| 所属 | ○○大学大学院 ○○研究科 ○○専攻 | |
| 研究室 | ○○研究室 | |
| 研究テーマ | 自動運転システムの安全性保証 | |
| 使用技術 | Python、JavaScript、Git、LaTeX | |
| 公開リンク | GitHub、Google Scholar、ORCID | |

公開リンクはサービス名だけでなく、自分のページのURLも記入します。
学籍番号や共同研究先の秘密情報など、公開しない情報はAIへの入力にも含めないでください。

## アカウントとクライアントを用意する

1. [GitHubのアカウント作成手順](https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github)に従い、アカウントを作成してメールアドレスを確認します。
2. [GitHub Desktopの導入手順](https://docs.github.com/en/desktop/overview/getting-started-with-github-desktop)に従い、アプリをインストールしてGitHubにサインインします。
3. 本文の演習では、GitHub Desktopの `File` → `New Repository` で新しいリポジトリを作ります。名前は、自分のGitHubユーザ名を使った `ユーザ名.github.io` にします。
4. `Repository` → `Show in Finder`（Windowsでは `Show in Explorer`）で、そのリポジトリの作業フォルダを確認します。HTMLはこのフォルダに保存します。

すでにあるリポジトリを使う場合は、`File` → `Clone Repository` で複製し、既存の公開方法と公開範囲に従ってください。

画面名や配置はOSとアプリの版によって異なるため、公式手順も確認してください。
[リポジトリの作成・公開・更新の公式手順](https://docs.github.com/en/desktop/overview/creating-your-first-repository-using-github-desktop)にも、各画面の説明があります。

## HTMLを保存してプレビューする

1. GitHub Desktopで作ったリポジトリの作業フォルダをVS Codeで開きます。
2. [HTMLの骨格](portfolio-skeleton.html)、またはAIが生成したコードを `index.html` として保存します。
3. ブラウザでファイルを開き、表示とコードを見比べます。
4. 名前、所属、研究内容を自分の情報に直し、その都度表示とリンクを確認します。
5. [公開前チェックリスト](../publication-checklist.md)を確認し、GitHub Desktopで差分を読んでからコミットします。

## GitHub Pagesで公開する

以下は、静的HTMLを `main` ブランチのルートに置く場合の手順です。
すでに公開元やGitHub Actionsが設定されているリポジトリでは、その設定に従ってください。

1. 公開してよいファイルだけが含まれていることを確認し、初回はGitHub Desktopの `Publish Repository` でGitHubへ送ります。GitHub Freeでこの演習を行う場合は、`Keep this code private` を外し、公開リポジトリとして作成します。以後の変更は `Push origin` で送ります。
2. GitHubのリポジトリで `Settings` → `Pages` を開きます。
3. `Build and deployment` の `Source` に `Deploy from a branch` を選びます。
4. ブランチを `main`、フォルダを `/(root)` にして保存します。
5. デプロイの完了後、`Pages` に表示された公開URLを開きます。
6. 別の端末やシークレットウィンドウでも、ページ内リンク、画像、ダウンロード、スマートフォンでの表示を確認します。

本文の演習のように `ユーザ名.github.io` という名前で作るユーザサイトは、`https://ユーザ名.github.io/` に公開されます。
別名のリポジトリで作るプロジェクトサイトは、通常 `https://ユーザ名.github.io/リポジトリ名/` になります。
利用できる公開元は契約プランなどによって異なるため、[サイト作成の公式手順](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)と[公開元の設定](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)を確認してください。
リポジトリの公開範囲と、Webページの公開範囲は別に確認する必要があります。
組織の規程で公開できない場合は、非公開リポジトリで管理し、ローカルプレビューを確認したうえで、公開しない理由を記録します。
