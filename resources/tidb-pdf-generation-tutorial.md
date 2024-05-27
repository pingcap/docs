---
title: TiDB Documentation PDF Generation Tutorial
summary: 特定のシナリオのニーズに合わせて、TiDB ドキュメントの PDF 出力をローカルでカスタマイズする方法を学習します。
---

# TiDB ドキュメント PDF 生成チュートリアル {#tidb-documentation-pdf-generation-tutorial}

このチュートリアルでは、TiDB ドキュメントを PDF 形式で生成する方法を紹介します。この方法を使用すると、TiDB ドキュメント内の特定のコンテンツをローカルで柔軟に並べ替えたり削除したり、特定のシナリオのニーズに合わせて PDF 出力をカスタマイズしたりできます。

## 環境の準備 {#environment-preparation}

次の準備手順は、PDF ファイルを初めて生成するときに 1 回だけ実行する必要があり、今後の PDF 生成では直接スキップできます。

### 準備1: Docker環境のインストールと設定 {#preparation-1-install-and-configure-the-docker-environment}

> 所要時間：30分。

以下の手順では、Docker Desktop のインストールとして macOS または Windows を例に説明します。

1.  [Dockerデスクトップ](https://docs.docker.com/get-docker/)インストールします。

2.  macOS ターミナルまたは Windows PowerShell で`docker --version`コマンドを実行します。

    Docker のバージョン情報が表示されれば、インストールは成功です。

3.  Docker リソースを構成します。

    1.  Docker アプリケーションを起動し、右上隅にある歯車アイコンをクリックします。

    2.  **「リソース」**をクリックし、**メモリを**`8.00 GB`に設定します。

4.  macOS ターミナルまたは Windows PowerShell で次のコマンドを実行して、TiDB PDF ドキュメントの構築に使用される Docker イメージをプルします。

    ```bash
    docker pull andelf/doc-build:0.1.9
    ```

### 準備2: TiDBドキュメントリポジトリをローカルディスクにクローンする {#preparation-2-clone-the-tidb-documentation-repository-to-your-local-disk}

> 推定所要時間: 10 分。

TiDB 英語ドキュメントリポジトリ: [ドキュメント](https://github.com/pingcap/docs) ; TiDB 中国語ドキュメントリポジトリ: [翻訳元:](https://github.com/pingcap/docs-cn)

次の手順では、TiDB の英語ドキュメントを例にして、リポジトリをクローンする方法を示します。

1.  TiDB 英語ドキュメント リポジトリに移動します: [ドキュメント](https://github.com/pingcap/docs) 。

2.  右上隅の[**フォーク**](https://github.com/pingcap/docs/fork)クリックし、フォークが完了するまで待ちます。

3.  次のいずれかの方法を使用して、TiDB ドキュメント リポジトリをローカルに複製します。

    -   方法 1: GitHub デスクトップ クライアントを使用します。

        1.  [GitHub デスクトップ](https://desktop.github.com/)インストールして起動します。
        2.  GitHub Desktop で、 **「ファイル」** &gt; **「リポジトリのクローン」**をクリックします。
        3.  **GitHub.com**タブをクリックし、 **「Your Repositories」**でフォークしたリポジトリを選択して、右下隅の**「Clone」**をクリックします。

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

1.  ローカルの TiDB ドキュメント リポジトリ内のファイルが、アップストリーム GitHub リポジトリ内の最新バージョンであることを確認します。

2.  必要に応じて、TiDB ドキュメントの内容を並べ替えたり削除したりします。

    1.  ローカル リポジトリのルート ディレクトリにある`TOC.md`ファイルを開きます。
    2.  `TOC.md`ファイルを編集します。たとえば、不要なドキュメントの章のタイトルとリンクをすべて削除できます。

3.  `TOC.md`ファイルに従って、すべてのドキュメントの章を 1 つの Markdown ファイルに統合します。

    1.  Docker アプリケーションを起動します。

    2.  PDF ドキュメントのビルド用の Docker イメージを実行するには、macOS ターミナルまたは Windows PowerShell で次のコマンドを実行します。

        ```bash
        docker run -it -v ${doc-path}:/opt/data andelf/doc-build:0.1.9
        ```

        コマンドでは、 `${doc-path}`​​ PDF 生成用のドキュメントのローカル パスです。たとえば、パスが`/Users/${username}/Documents/GitHub/docs`の場合、コマンドは次のようになります。

        ```bash
        docker run -it -v /Users/${username}/Documents/GitHub/docs:/opt/data andelf/doc-build:0.1.9
        ```

        実行後、 `WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested`が返された場合は無視できます。

    3.  `opt/data`ディレクトリに移動します。

        ```bash
        cd /opt/data
        ```

    4.  `TOC.md`に従って、すべての Markdown ドキュメント ファイルを 1 つ`doc.md`ファイルに統合します。

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

    PDF ファイルの生成に必要な時間は、ドキュメントのサイズによって異なります。完全な TiDB ドキュメントの場合は、約 1 時間かかります。生成が完了すると、ドキュメントが保存されているフォルダーに新しく生成された PDF ファイル`output.pdf`が表示されます。
