---
title: Export Data from TiDB
summary: This page has instructions for exporting data from your TiDB cluster in TiDB Cloud.
---

# TiDBからデータをエクスポートする {#export-data-from-tidb}

このページでは、 TiDB Cloudでクラスタからデータをエクスポートする方法について説明します。

毎日のバックアップは、 TiDB CloudのTiDBクラスターに対して自動的にスケジュールされます。バックアップスナップショットを選択して、いつでも新しいTiDBクラスタに復元できます。自動バックアップにより、極端な災害状況での損失を減らすことができます。

TiDBはデータをロックインしません。それでも、TiDBから他のデータプラットフォームにデータを移行できるようにしたい場合があります。 TiDBはMySQLとの互換性が高いため、MySQLに適した任意のエクスポートツールをTiDBにも使用できます。

同じツール[Dumpling](https://github.com/pingcap/dumpling)をデータのエクスポートに使用できます。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、TiUPは対応する`profile`のファイルの絶対パスを表示します。次のコマンドで`.bash_profile`を`profile`ファイルのパスに変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source .bash_profile
    ```

3.  Dumplingをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup install dumpling
    ```

4.  TiDBからのDumplingを使用してデータをエクスポートします。

    {{< copyable "" >}}

    ```shell
    tiup dumpling -h ${tidb-endpoint} -P 3306 -u ${user} -F 67108864 -t 4 -o /path/to/export/dir
    ```

    指定したデータベースのみをエクスポートする場合は、 `-B`を使用してデータベース名のコンマ区切りリストを指定します。

    必要な最小権限は次のとおりです。

    -   `SELECT`
    -   `RELOAD`
    -   `LOCK TABLES`
    -   `REPLICATION CLIENT`

    現在、 DumplingはMydumper形式の出力のみをサポートしており、 [TiDB Lightning](https://github.com/pingcap/tidb-lightning)を使用してMySQL互換データベースに簡単に復元できます。
