---
title: TiDB Control User Guide
summary: Use TiDB Control to obtain TiDB status information for debugging.
---

# TiDB コントロール ユーザー ガイド {#tidb-control-user-guide}

TiDB Control は TiDB のコマンドライン ツールで、通常はデバッグのために TiDB のステータス情報を取得するために使用されます。このドキュメントでは、TiDB Control の機能とその使用方法を紹介します。

> **注記：**
>
> TiDB コントロールはデバッグ目的に特化して設計されており、TiDB に導入される将来の機能と完全な互換性がない可能性があります。情報を取得するために、アプリケーションまたはユーティリティの開発にこのツールを含めることはお勧めできません。

## TiDB コントロールを取得する {#get-tidb-control}

TiDB Control を入手するには、 TiUPを使用してインストールするか、ソース コードからコンパイルします。

> **注記：**
>
> 使用する制御ツールのバージョンがクラスターのバージョンと一致していることをお勧めします。

### TiUPを使用して TiDB コントロールをインストールする {#install-tidb-control-using-tiup}

TiUPをインストールした後、 `tiup ctl:v<CLUSTER_VERSION> tidb`コマンドを使用して TiDB コントロールを取得して実行できます。

### ソースコードからコンパイルする {#compile-from-source-code}

-   コンパイル環境要件： [行く](https://golang.org/) 1.21以降
-   コンパイル手順: [TiDB コントロール プロジェクト](https://github.com/pingcap/tidb-ctl)のルート ディレクトリに移動し、 `make`コマンドを使用してコンパイルし、 `tidb-ctl`を生成します。
-   コンパイル ドキュメント: ヘルプ ファイルは`doc`ディレクトリにあります。ヘルプ ファイルが失われた場合、またはヘルプ ファイルを更新したい場合は、 `make doc`コマンドを使用してヘルプ ファイルを生成します。

## 使い方の紹介 {#usage-introduction}

このセクションでは、 `tidb-ctl`のコマンド、サブコマンド、オプション、およびフラグの使用方法について説明します。

-   コマンド: `-`または`--`のない文字
-   サブコマンド: コマンドに続く`-`または`--`のない文字
-   オプション: `-`または`--`の文字
-   flag: コマンド/サブコマンドまたはオプションの直後にある文字で、コマンド/サブコマンドまたはオプションに値を渡します。

使用例： `tidb-ctl schema in mysql -n db`

-   `schema` : コマンド
-   `in` : `schema`のサブコマンド
-   `mysql` : `in`のフラグ
-   `-n` : オプション
-   `db` : `-n`のフラグ

現在、TiDB Control には次のサブコマンドがあります。

-   `tidb-ctl base64decode` : `BASE64`デコードに使用
-   `tidb-ctl decoder` : `KEY`のデコードに使用
-   `tidb-ctl etcd` : etcdの操作に使用されます。
-   `tidb-ctl log` : 単一行のスタック情報を展開するためにログ ファイルをフォーマットするために使用されます。
-   `tidb-ctl mvcc` : MVCC 情報の取得に使用されます。
-   `tidb-ctl region` :リージョン情報の取得に使用されます。
-   `tidb-ctl schema` : スキーマ情報の取得に使用されます
-   `tidb-ctl table` : テーブル情報の取得に使用されます。

### 助けを得ます {#get-help}

使用状況情報を取得するには`tidb-ctl -h/--help`使用します。

TiDB Control は複数のコマンド層で構成されています。各コマンド/サブコマンドの後に`-h/--help`を使用すると、それぞれの使用法情報を取得できます。

次の例は、スキーマ情報を取得する方法を示しています。

使用量の詳細を取得するには、 `tidb-ctl schema -h`を使用します。 `schema`コマンド自体には`in`と`tid`という 2 つのサブコマンドがあります。

-   `in`は、データベース名を通じてデータベース内のすべてのテーブルのテーブル スキーマを取得するために使用されます。
-   `tid`は、データベース全体で一意の`table_id`を使用してテーブル スキーマを取得するために使用されます。

### グローバルオプション {#global-options}

`tidb-ctl`には、次の接続関連のグローバル オプションがあります。

-   `--host` : TiDB サービスアドレス (デフォルトは 127.0.0.1)
-   `--port` : TiDB ステータスポート (デフォルトは 10080)
-   `--pdhost` : PD サービスアドレス (デフォルトは 127.0.0.1)
-   `--pdport` : PD サービスポート (デフォルトは 2379)
-   `--ca` : TLS 接続に使用される CA ファイル パス
-   `--ssl-key` : TLS 接続に使用されるキーファイルのパス
-   `--ssl-cert` : TLS 接続に使用される証明書ファイルのパス

`--pdhost`と`--pdport`は主に`etcd`サブコマンドで使用されます。たとえば、 `tidb-ctl etcd ddlinfo` 。アドレスとポートを指定しない場合は、次のデフォルト値が使用されます。

-   TiDB および PD のデフォルトのサービス アドレス: `127.0.0.1` 。サービス アドレスは IP アドレスである必要があります。
-   TiDB のデフォルトのサービス ポート: `10080` 。
-   PD のデフォルトのサービス ポート: `2379` 。

### <code>schema</code>コマンド {#the-code-schema-code-command}

#### <code>in</code>サブコマンド {#the-code-in-code-subcommand}

`in`は、データベース名を通じてデータベース内のすべてのテーブルのテーブル スキーマを取得するために使用されます。

```bash
tidb-ctl schema in <database name>
```

たとえば、 `tidb-ctl schema in mysql`を実行すると、次の結果が返されます。

```json
[
    {
        "id": 13,
        "name": {
            "O": "columns_priv",
            "L": "columns_priv"
        },
              ...
        "update_timestamp": 399494726837600268,
        "ShardRowIDBits": 0,
        "Partition": null
    }
]
```

結果はJSON形式で表示されます。 (上記の出力は切り詰められています。)

-   テーブル名を指定する場合は、 `tidb-ctl schema in <database> -n <table name>`を使用してフィルターします。

    たとえば、 `tidb-ctl schema in mysql -n db`データベース`mysql`のテーブル`db`のテーブル スキーマを返します。

    ```json
    {
        "id": 9,
        "name": {
            "O": "db",
            "L": "db"
        },
        ...
        "Partition": null
    }
    ```

    (上記の出力も切り詰められています。)

    デフォルトの TiDB サービスのアドレスとポートを使用したくない場合は、 `--host`および`--port`オプションを使用して設定します。たとえば、 `tidb-ctl --host 172.16.55.88 --port 8898 schema in mysql -n db` 。

#### <code>tid</code>サブコマンド {#the-code-tid-code-subcommand}

`tid`は、データベース全体で一意の`table_id`を使用してテーブル スキーマを取得するために使用されます。 `in`サブコマンドを使用して特定のスキーマのすべてのテーブル ID を取得し、 `tid`サブコマンドを使用して詳細なテーブル情報を取得できます。

たとえば、 `mysql.stat_meta`のテーブル ID は`21`です。 `tidb-ctl schema tid -i 21`使用すると、 `mysql.stat_meta`の詳細を取得できます。

```json
{
 "id": 21,
 "name": {
  "O": "stats_meta",
  "L": "stats_meta"
 },
 "charset": "utf8mb4",
 "collate": "utf8mb4_bin",
  ...
}
```

`in`サブコマンドと同様に、デフォルトの TiDB サービス アドレスとステータス ポートを使用したくない場合は、 `--host`および`--port`オプションを使用してホストとポートを指定します。

#### <code>base64decode</code>コマンド {#the-code-base64decode-code-command}

`base64decode`は`base64`データをデコードするために使用されます。

```shell
tidb-ctl base64decode [base64_data]
tidb-ctl base64decode [db_name.table_name] [base64_data]
tidb-ctl base64decode [table_id] [base64_data]
```

1.  次の SQL ステートメントを実行して環境を準備します。

    ```sql
    use test;
    create table t (a int, b varchar(20),c datetime default current_timestamp , d timestamp default current_timestamp, unique index(a));
    insert into t (a,b,c) values(1,"哈哈 hello",NULL);
    alter table t add column e varchar(20);
    ```

2.  HTTP API インターフェイスを使用した Obtian MVCC データ:

    ```shell
    $ curl "http://$IP:10080/mvcc/index/test/t/a/1?a=1"
    {
     "info": {
      "writes": [
       {
        "start_ts": 407306449994645510,
        "commit_ts": 407306449994645513,
        "short_value": "AAAAAAAAAAE="    # The unique index a stores the handle id of the corresponding row.
       }
      ]
     }
    }%

    $ curl "http://$IP:10080/mvcc/key/test/t/1"
    {
     "info": {
      "writes": [
       {
        "start_ts": 407306588892692486,
        "commit_ts": 407306588892692489,
        "short_value": "CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk="  # Row data that handle id is 1.
       }
      ]
     }
    }%
    ```

3.  デコード``handle id (uint64) using `base64decode` `` 。

    ```shell
    $ tidb-ctl base64decode AAAAAAAAAAE=
    hex: 0000000000000001
    uint64: 1
    ```

4.  `base64decode`を使用して行データをデコードします。

    ```shell
    $ ./tidb-ctl base64decode test.t CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk=
    a:      1
    b:      哈哈 hello
    c is NULL
    d:      2019-03-28 05:35:30
    e not found in data

    # if the table id of test.t is 60, you can also use below command to do the same thing.
    $ ./tidb-ctl base64decode 60 CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk=
    a:      1
    b:      哈哈 hello
    c is NULL
    d:      2019-03-28 05:35:30
    e not found in data
    ```

### <code>decoder</code>コマンド {#the-code-decoder-code-command}

-   次の例は、インデックス キーのデコードと同様に、行キーをデコードする方法を示しています。

    ```shell
    $ ./tidb-ctl decoder "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    format: table_row
    table_id: -9223372036854775780      table_id: -9223372036854775780
    row_id: -9223372036854775558        row_id: -9223372036854775558
    ```

-   次の例は、 `value`をデコードする方法を示しています。

    ```shell
    $ ./tidb-ctl decoder AhZoZWxsbyB3b3JsZAiAEA==
    format: index_value
    type: bigint, value: 1024       index_value[0]: {type: bytes, value: hello world}
    index_value[1]: {type: bigint, value: 1024}
    ```

### <code>etcd</code>コマンド {#the-code-etcd-code-command}

-   `tidb-ctl etcd ddlinfo`はDDL情報を取得するために使用されます。

-   `tidb-ctl etcd putkey KEY VALUE`は、etcd に KEY VALUE を追加するために使用されます (すべての KEY が`/tidb/ddl/all_schema_versions/`ディレクトリに追加されます)。

    ```shell
    tidb-ctl etcd putkey "foo" "bar"
    ```

    実際、キーと値のペアは、 KEY が`/tidb/ddl/all_schema_versions/foo` 、 VALUE が`bar`である etcd に追加されます。

-   `tidb-ctl etcd delkey` etcd 内の KEY を削除します。 `/tidb/ddl/fg/owner/`または`/tidb/ddl/all_schema_versions/`プレフィックスを持つ KEY のみを削除できます。

    ```shell
    tidb-ctl etcd delkey "/tidb/ddl/fg/owner/foo"
    tidb-ctl etcd delkey "/tidb/ddl/all_schema_versions/bar"
    ```

### <code>log</code>コマンド {#the-code-log-code-command}

TiDB エラー ログのスタック情報は 1 行形式です。 `tidb-ctl log`使用すると、形式を複数行に変更できます。

### <code>keyrange</code>コマンド {#the-code-keyrange-code-command}

`keyrange`サブコマンドは、グローバルまたはテーブル関連のキー範囲情報をクエリするために使用され、16 進形式で出力されます。

-   `tidb-ctl keyrange`コマンドを実行して、グローバル キー範囲情報を確認します。

    ```shell
    tidb-ctl keyrange
    ```

        global ranges:
          meta: (6d, 6e)
          table: (74, 75)

-   エンコードされたキーを表示する`--encode`オプションを追加します (TiKV および PD と同じ形式)。

    ```shell
    tidb-ctl keyrange --encode
    ```

        global ranges:
          meta: (6d00000000000000f8, 6e00000000000000f8)
          table: (7400000000000000f8, 7500000000000000f8)

-   `tidb-ctl keyrange --database={db} --table={tbl}`コマンドを実行して、グローバルおよびテーブル関連のキー範囲情報を確認します。

    ```shell
    tidb-ctl keyrange --database test --table ttt
    ```

        global ranges:
          meta: (6d, 6e)
          table: (74, 75)
        table ttt ranges: (NOTE: key range might be changed after DDL)
          table: (74800000000000002f, 748000000000000030)
          table indexes: (74800000000000002f5f69, 74800000000000002f5f72)
            index c2: (74800000000000002f5f698000000000000001, 74800000000000002f5f698000000000000002)
            index c3: (74800000000000002f5f698000000000000002, 74800000000000002f5f698000000000000003)
            index c4: (74800000000000002f5f698000000000000003, 74800000000000002f5f698000000000000004)
          table rows: (74800000000000002f5f72, 748000000000000030)
