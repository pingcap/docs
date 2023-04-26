---
title: Export Data from TiDB
summary: This page has instructions for exporting data from your TiDB cluster in TiDB Cloud.
---

# TiDB からのデータのエクスポート {#export-data-from-tidb}

このページでは、 TiDB Cloudのクラスターからデータをエクスポートする方法について説明します。

TiDB はデータをロックしません。 TiDB から他のデータ プラットフォームにデータを移行できるようにしたい場合があります。 TiDB は MySQL との互換性が高いため、MySQL に適したエクスポート ツールはすべて TiDB にも使用できます。

ツール[Dumpling](/dumpling-overview.md)使用してデータをエクスポートできます。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、 TiUP は対応する`profile`ファイルの絶対パスを表示します。次のコマンドの`.bash_profile` `profile`ファイルのパスに変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source .bash_profile
    ```

3.  Dumplingをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup install dumpling
    ```

4.  TiDB からDumpling を使用してデータをエクスポートします。

    [**接続**](/tidb-cloud/connect-via-standard-connection.md)ダイアログの接続文字列から、次の接続パラメーター`${tidb_endpoint}` 、 `${port}` 、および`${user}`を取得できます。

    <SimpleTab>

    <div label="Serverless Tier">

    ```shell
    tiup dumpling -h ${tidb_endpoint} -P 4000 -u ${user} -p ${password} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql --consistency none
    ```

    > **ノート：**
    >
    > Serverless Tierクラスタ データをエクスポートするには、 Dumpling のバージョンが少なくとも v6.5.0 であることを確認する必要があります。 Dumpling のバージョンが v6.5.0 の場合は、コマンドで`--ca=${ca_path}`を設定する必要もあります。システムの CA ルート パスを見つけるには、 [Serverless Tierへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#root-certificate-default-path)を参照してください。

    </div>
     <div label="Dedicated Tier">

    ```shell
    tiup dumpling:v6.5.2 -h ${tidb_endpoint} -P ${port} -u ${user} -p ${password} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql
    ```

    </div>
     </SimpleTab>

    オプションの説明は次のとおりです。

    -   `-h` : TiDB クラスターのエンドポイント。
    -   `-P` : TiDB クラスターのポート。
    -   `-u` : TiDB クラスター ユーザー。
    -   `-p` : TiDB クラスターのパスワード。
    -   `-F` : 1 つのファイルの最大サイズ。
    -   `-o` : エクスポート ディレクトリ。
    -   `--filetype` : エクスポートされたファイルの種類。デフォルト値は`sql`です。 `sql`と`csv`から選択できます。
    -   `--consistency` : データの整合性。デフォルト値は`auto`です。 Serverless Tierの場合は、 `none`に設定する必要があります。

    Dumplingオプションの詳細については、 [Dumplingのオプション一覧](/dumpling-overview.md#option-list-of-dumpling)を参照してください。

    最低限必要な権限は次のとおりです。

    -   `SELECT`
    -   `RELOAD`
    -   `LOCK TABLES`
    -   `REPLICATION CLIENT`

Dumplingを使用してデータをエクスポートした後、 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)を使用して MySQL 互換データベースにデータをインポートできます。
