---
title: Export Data from TiDB
summary: This page has instructions for exporting data from your TiDB cluster in TiDB Cloud.
---

# TiDB からデータをエクスポート {#export-data-from-tidb}

このページでは、 TiDB Cloudのクラスターからデータをエクスポートする方法について説明します。

TiDB はデータをロックインしません。 TiDB から他のデータ プラットフォームにデータを移行できるようにしたい場合があります。 TiDB は MySQL と高い互換性があるため、MySQL に適したエクスポート ツールはすべて TiDB にも使用できます。

データのエクスポートにはツール[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用できます。

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

    <SimpleTab>

    <div label="TiDB Serverless">

    [**接続**](/tidb-cloud/connect-via-standard-connection-serverless.md)ダイアログの接続文字列から、次の接続パラメータ`${tidb_endpoint}` 、 `${port}` 、および`${user}`を取得できます。

    ```shell
    tiup dumpling -h ${tidb_endpoint} -P 4000 -u ${user} -p ${password} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql --consistency none
    ```

    > **ノート：**
    >
    > TiDB サーバーレス クラスター データをエクスポートするには、 Dumpling のバージョンが少なくとも v6.5.0 であることを確認する必要があります。 Dumpling のバージョンが v6.5.0 の場合は、コマンドで`--ca=${ca_path}`を設定する必要もあります。システム上の CA ルート パスを見つけるには、 [TiDB サーバーレスへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)を参照してください。

    </div>
     <div label="TiDB Dedicated">

    [**接続**](/tidb-cloud/connect-via-standard-connection.md)ダイアログの接続文字列から、次の接続パラメータ`${tidb_endpoint}` 、 `${port}` 、および`${user}`を取得できます。

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
    -   `--consistency` : データの一貫性。デフォルト値は`auto`です。 TiDB サーバーレスの場合は、これを`none`に設定する必要があります。

    Dumplingオプションの詳細については、 [Dumplingオプション一覧](https://docs.pingcap.com/tidb/stable/dumpling-overview#option-list-of-dumpling)を参照してください。

    最低限必要な権限は次のとおりです。

    -   `SELECT`
    -   `RELOAD`
    -   `LOCK TABLES`
    -   `REPLICATION CLIENT`

Dumplingを使用してデータをエクスポートした後、 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)を使用してデータを MySQL 互換データベースにインポートできます。
