---
title: TiDB Documentation PDF Generation Tutorial
summary: 特定のシナリオのニーズに合わせて、TiDB ドキュメントの PDF 出力をローカルでカスタマイズする方法を学習します。
---

# TiDBドキュメントPDF生成チュートリアル {#tidb-documentation-pdf-generation-tutorial}

このチュートリアルでは、TiDBドキュメントをPDF形式で生成する方法を紹介します。この方法を使えば、TiDBドキュメント内の特定のコンテンツをローカルで柔軟に並べ替えたり削除したり、特定のシナリオのニーズに合わせてPDF出力をカスタマイズしたりできます。

## 環境の準備 {#environment-preparation}

次の準備手順は、PDF ファイルを初めて生成するときに 1 回だけ実行する必要があり、今後の PDF 生成では直接スキップできます。

### 準備1: Docker環境のインストールと設定 {#preparation-1-install-and-configure-the-docker-environment}

> 推定所要時間: 30 分。

次の手順では、Docker Desktop のインストールとして macOS または Windows を例に説明します。

1.  [Dockerデスクトップ](https://docs.docker.com/get-docker/)をインストールします。

2.  macOS ターミナルまたは Windows PowerShell で`docker --version`コマンドを実行します。

    Docker のバージョン情報が表示されれば、インストールは成功です。

3.  Docker リソースを構成します。

    1.  Docker アプリケーションを起動し、右上隅にある歯車アイコンをクリックします。

    2.  **[リソース]**をクリックし、**メモリ**を`8.00 GB`に設定します。

4.  macOS ターミナルまたは Windows PowerShell で次のコマンドを実行して、TiDB PDF ドキュメントの構築に使用される Docker イメージをプルします。

    ```bash
    docker pull andelf/doc-build:0.1.9
    ```

### 準備2: TiDBドキュメントリポジトリをローカルディスクにクローンする {#preparation-2-clone-the-tidb-documentation-repository-to-your-local-disk}

> 推定所要時間: 10 分。

TiDB 英語ドキュメントリポジトリ: [https://github.com/pingcap/docs](https://github.com/pingcap/docs) ; TiDB 中国語ドキュメントリポジトリ: [https://github.com/pingcap/docs-cn](https://github.com/pingcap/docs-cn)

次の手順では、TiDB の英語ドキュメントを例にして、リポジトリのクローンを作成する方法を説明します。

1.  TiDB 英語ドキュメント リポジトリに移動します: [https://github.com/pingcap/docs](https://github.com/pingcap/docs) 。

2.  右上隅の[**フォーク**](https://github.com/pingcap/docs/fork)クリックし、フォークが完了するまで待ちます。

3.  次のいずれかの方法を使用して、TiDB ドキュメント リポジトリをローカルに複製します。

    -   方法 1: GitHub デスクトップ クライアントを使用します。

        1.  [GitHubデスクトップ](https://desktop.github.com/)をインストールして起動します。
        2.  GitHub Desktop で、 **「ファイル」** &gt; **「リポジトリのクローン」**をクリックします。
        3.  **GitHub.com**タブをクリックし、 **「Your Repositories」**でフォークしたリポジトリを選択して、右下隅の**「Clone」を**クリックします。

    -   方法 2: 次の Git コマンドを使用します。

        ```shell
        cd $working_dir # Replace `$working_dir` with the directory where you want the repository to be placed. For example, `cd ~/Documents/GitHub`
        git clone git@github.com:$user/docs.git # Replace `$user` with your GitHub ID

        cd $working_dir/docs
        git remote add upstream git@github.com:pingcap/docs.git # Add upstream repository
        git remote -v
        ```

## 手順 {#steps}

> 推定時間: 以下の操作には 2 分しかかかりませんが、PDF の生成には 0.5 ～ 1 時間かかります。

1.  ローカルの TiDB ドキュメント リポジトリ内のファイルが、アップストリーム GitHub リポジトリの最新バージョンであることを確認します。

2.  必要に応じて、TiDB ドキュメントの内容を並べ替えたり削除したりします。

    1.  ローカル リポジトリのルート ディレクトリにある`TOC.md`ファイルを開きます。
    2.  `TOC.md`ファイルを編集します。例えば、不要なドキュメントの章のタイトルとリンクをすべて削除できます。

3.  `TOC.md`ファイルに従って、すべてのドキュメントの章を 1 つの Markdown ファイルに統合します。

    1.  Docker アプリケーションを起動します。

    2.  PDF ドキュメントのビルド用の Docker イメージを実行するには、macOS ターミナルまたは Windows PowerShell で次のコマンドを実行します。

        ```bash
        docker run -it -v ${doc-path}:/opt/data andelf/doc-build:0.1.9
        ```

        コマンド中の`${doc-path}` 、PDF生成用のドキュメントのローカルパスです。例えば、パスが`/Users/${username}/Documents/GitHub/docs`場合、コマンドは以下のようになります。

        ```bash
        docker run -it -v /Users/${username}/Documents/GitHub/docs:/opt/data andelf/doc-build:0.1.9
        ```

        実行後、 `WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested`が返された場合は無視できます。

    3.  `opt/data`ディレクトリに移動します。

        ```bash
        cd /opt/data
        ```

    4.  `TOC.md`に従って、すべての Markdown ドキュメント ファイルを`doc.md`ファイルに統合します。

        ```bash
        python3 scripts/merge_by_toc.py
        ```

        **期待される出力:**

        `TOC.md`と同じフォルダーに、新しく生成された`doc.md`ファイルが表示されます。

4.  PDF ドキュメントを生成します:

    ```bash
    bash scripts/generate_pdf.sh
    ```

    **期待される出力:**

    PDFファイルの生成にかかる時間はドキュメントのサイズによって異なります。TiDBの完全なドキュメントの場合は約1時間かかります。生成が完了すると、ドキュメントが保存されているフォルダに新しく生成されたPDFファイル`output.pdf`表示されます。
