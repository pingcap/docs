---
title: Export Data from TiDB
summary: This page has instructions for exporting data from your TiDB cluster in TiDB Cloud.
---

# TiDB からデータをエクスポート {#export-data-from-tidb}

このページでは、 TiDB Cloudのクラスターからデータをエクスポートする方法について説明します。

TiDB はデータをロックインしません。 TiDB から他のデータ プラットフォームにデータを移行できるようにしたい場合があります。 TiDB は MySQL と高い互換性があるため、MySQL に適したエクスポート ツールはすべて TiDB にも使用できます。

データのエクスポートにはツール[<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)を使用できます。

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

    [<a href="/tidb-cloud/connect-via-standard-connection.md">**接続**</a>](/tidb-cloud/connect-via-standard-connection.md)ダイアログの接続文字列から、次の接続パラメータ`${tidb_endpoint}` 、 `${port}` 、および`${user}`を取得できます。

    <SimpleTab>

    <div label="TiDB Serverless">

    ```shell
    tiup dumpling -h ${tidb_endpoint} -P 4000 -u ${user} -p ${password} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql --consistency none
    ```

    > **ノート：**
    >
    > TiDB Serverlessless クラスター データをエクスポートするには、 Dumpling のバージョンが少なくとも v6.5.0 であることを確認する必要があります。 Dumpling のバージョンが v6.5.0 の場合は、コマンドで`--ca=${ca_path}`を設定する必要もあります。システム上の CA ルート パスを見つけるには、 [<a href="/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#root-certificate-default-paTiDB Serverlessrverlessへの TLS 接続</a>](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#root-certificate-default-path)を参照してください。

    </div>
     <div label="TiDB Dedicated">

    ```shell
    tiup dumpling:v6.5.2 -h ${tidb_endpoint} -P ${port} -u ${user} -p ${password} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql
    ```

    </div>
     </SimpleTab>

    オプションは次のように説明されます。

    -   `-h` : TiDB クラスターのエンドポイント。
    -   `-P` : TiDB クラスターのポート。
    -   `-u` : TiDB クラスターのユーザー。
    -   `-p` : TiDB クラスターのパスワード。
    -   `-F` : 1 つのファイルの最大サイズ。
    -   `-o` : エクスポートディレクトリ。
    -   `--filetype` : エクスポートされたファイルの種類。デフォルト値は`sql`です。 `sql`と`csv`からお選びいただけます。
    -   `--consistency` : データの一貫性。デフォルト値は`auto`です。 TiDB Serverlesslessの場合は、これを`none`に設定する必要があります。

    Dumplingオプションの詳細については、 [<a href="/dumpling-overview.md#option-list-of-dumpling">Dumplingオプション一覧</a>](/dumpling-overview.md#option-list-of-dumpling)を参照してください。

    最低限必要な権限は次のとおりです。

    -   `SELECT`
    -   `RELOAD`
    -   `LOCK TABLES`
    -   `REPLICATION CLIENT`

Dumplingを使用してデータをエクスポートした後、 [<a href="https://docs.pingcap.com/tidb/stable/tidb-lightning-overview">TiDB Lightning</a>](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)を使用してデータを MySQL 互換データベースにインポートできます。
