---
title: TiDB Control User Guide
summary: Use TiDB Control to obtain TiDB status information for debugging.
---

# TiDBControlユーザーガイド {#tidb-control-user-guide}

TiDB Controlは、TiDBのコマンドラインツールであり、通常、デバッグのためにTiDBのステータス情報を取得するために使用されます。このドキュメントでは、TiDBControlの機能とこれらの機能の使用方法を紹介します。

## TiDBコントロールを取得する {#get-tidb-control}

TiDB Controlは、TiUPを使用してインストールするか、ソースコードからコンパイルすることで入手できます。

> **ノート：**
>
> 使用するコントロールツールのバージョンは、クラスタのバージョンと一致していることをお勧めします。

### TiUPを使用してTiDBControlをインストールします {#install-tidb-control-using-tiup}

TiUPをインストールした後、 `tiup ctl tidb`のコマンドを使用してTiDBコントロールを取得および実行できます。

### ソースコードからコンパイルする {#compile-from-source-code}

-   コンパイル環境の要件： [行け](https://golang.org/)バージョン1.13以降
-   コンパイル手順： [TiDBコントロールプロジェクト](https://github.com/pingcap/tidb-ctl)のルートディレクトリに移動し、 `make`コマンドを使用してコンパイルし、 `tidb-ctl`を生成します。
-   コンパイルドキュメント：ヘルプファイルは`doc`ディレクトリにあります。ヘルプファイルが失われた場合、またはそれらを更新したい場合は、 `make doc`コマンドを使用してヘルプファイルを生成します。

## 使い方紹介 {#usage-introduction}

このセクションでは、 `tidb-ctl`でコマンド、サブコマンド、オプション、およびフラグを使用する方法について説明します。

-   コマンド： `-`または`--`のない文字
-   サブコマンド：コマンドに続く`-`または`--`のない文字
-   オプション： `-`または`--`の文字
-   フラグ：コマンド/サブコマンドまたはオプションの直後の文字、コマンド/サブコマンドまたはオプションに値を渡す

使用例： `tidb-ctl schema in mysql -n db`

-   `schema` ：コマンド
-   `in` ： `schema`のサブコマンド
-   `mysql` ： `in`のフラグ
-   `-n` ：オプション
-   `db` ： `-n`のフラグ

現在、TiDBControlには次のサブコマンドがあります。

-   `tidb-ctl base64decode` ： `BASE64`のデコードに使用
-   `tidb-ctl decoder` ： `KEY`のデコードに使用
-   `tidb-ctl etcd` ：etcdの操作に使用
-   `tidb-ctl log` ：単一行のスタック情報を展開するためにログファイルをフォーマットするために使用されます
-   `tidb-ctl mvcc` ：MVCC情報を取得するために使用されます
-   `tidb-ctl region` ：リージョン情報を取得するために使用されます
-   `tidb-ctl schema` ：スキーマ情報を取得するために使用されます
-   `tidb-ctl table` ：テーブル情報を取得するために使用されます

### 助けを得ます {#get-help}

`tidb-ctl -h/--help`を使用して使用情報を取得します。

TiDB Controlは、コマンドの複数のレイヤーで構成されています。各コマンド/サブコマンドの後に`-h/--help`を使用して、それぞれの使用法情報を取得できます。

次の例は、スキーマ情報を取得する方法を示しています。

`tidb-ctl schema -h`を使用して、使用法の詳細を取得します。 `schema`コマンド自体には、 `in`と`tid`の2つのサブコマンドがあります。

-   `in`は、データベース名を介してデータベース内のすべてのテーブルのテーブルスキーマを取得するために使用されます。
-   `tid`は、データベース全体で一意の`table_id`を使用してテーブルスキーマを取得するために使用されます。

### グローバルオプション {#global-options}

`tidb-ctl`には、次の接続関連のグローバルオプションがあります。

-   `--host` ：TiDBサービスアドレス（デフォルトは127.0.0.1）
-   `--port` ：TiDBステータスポート（デフォルトは10080）
-   `--pdhost` ：PDサービスアドレス（デフォルトは127.0.0.1）
-   `--pdport` ：PDサービスポート（デフォルトは2379）
-   `--ca` ：TLS接続に使用されるCAファイルパス
-   `--ssl-key` ：TLS接続に使用されるキーファイルパス
-   `--ssl-cert` ：TLS接続に使用される証明書ファイルのパス

`--pdhost`と`--pdport`は、主に`etcd`サブコマンドで使用されます。たとえば、 `tidb-ctl etcd ddlinfo` 。アドレスとポートを指定しない場合、次のデフォルト値が使用されます。

-   TiDBおよびPDのデフォルトのサービスアドレス： `127.0.0.1` 。サービスアドレスはIPアドレスである必要があります。
-   TiDBのデフォルトのサービスポート： `10080` 。
-   PDのデフォルトのサービスポート： `2379` 。

### <code>schema</code>コマンド {#the-code-schema-code-command}

#### <code>in</code>サブコマンド {#the-code-in-code-subcommand}

`in`は、データベース名を介してデータベース内のすべてのテーブルのテーブルスキーマを取得するために使用されます。

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

結果はJSON形式で表示されます。 （上記の出力は切り捨てられます。）

-   テーブル名を指定する場合は、 `tidb-ctl schema in <database> -n <table name>`を使用してフィルタリングします。

    たとえば、 `tidb-ctl schema in mysql -n db`は、 `mysql`データベース内の`db`テーブルのテーブルスキーマを返します。

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

    （上記の出力も切り捨てられます。）

    デフォルトのTiDBサービスアドレスとポートを使用したくない場合は、 `--host`と`--port`のオプションを使用して構成します。たとえば、 `tidb-ctl --host 172.16.55.88 --port 8898 schema in mysql -n db` 。

#### <code>tid</code>サブコマンド {#the-code-tid-code-subcommand}

`tid`は、データベース全体で一意の`table_id`を使用してテーブルスキーマを取得するために使用されます。 `in`サブコマンドを使用して特定のスキーマのすべてのテーブルIDを取得し、 `tid`サブコマンドを使用して詳細なテーブル情報を取得できます。

たとえば、 `mysql.stat_meta`のテーブルIDは`21`です。 `tidb-ctl schema tid -i 21`を使用して`mysql.stat_meta`の詳細を取得できます。

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

`in`サブコマンドと同様に、デフォルトのTiDBサービスアドレスとステータスポートを使用しない場合は、 `--host`と`--port`のオプションを使用してホストとポートを指定します。

#### <code>base64decode</code>コマンド {#the-code-base64decode-code-command}

`base64decode`は`base64`のデータをデコードするために使用されます。

```shell
tidb-ctl base64decode [base64_data]
tidb-ctl base64decode [db_name.table_name] [base64_data]
tidb-ctl base64decode [table_id] [base64_data]
```

1.  次のSQLステートメントを実行して、環境を準備します。

    ```sql
    use test;
    create table t (a int, b varchar(20),c datetime default current_timestamp , d timestamp default current_timestamp, unique index(a));
    insert into t (a,b,c) values(1,"哈哈 hello",NULL);
    alter table t add column e varchar(20);
    ```

2.  HTTPAPIインターフェースを使用したObtianMVCCデータ：

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

3.  ``handle id (uint64) using `base64decode` ``をデコードします。

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

-   次の例は、インデックスキーのデコードと同様に、行キーをデコードする方法を示しています。

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

-   `tidb-ctl etcd ddlinfo`は、DDL情報を取得するために使用されます。

-   `tidb-ctl etcd putkey KEY VALUE`は、キー値をetcdに追加するために使用されます（すべてのキーは`/tidb/ddl/all_schema_versions/`ディレクトリに追加されます）。

    ```shell
    tidb-ctl etcd putkey "foo" "bar"
    ```

    実際、KEYが`/tidb/ddl/all_schema_versions/foo`でVALUEが`bar`のetcdには、キーと値のペアが追加されます。

-   `tidb-ctl etcd delkey`はetcdのKEYを削除します。プレフィックスが`/tidb/ddl/fg/owner/`または`/tidb/ddl/all_schema_versions/`のKEYのみを削除できます。

    ```shell
    tidb-ctl etcd delkey "/tidb/ddl/fg/owner/foo"
    tidb-ctl etcd delkey "/tidb/ddl/all_schema_versions/bar"
    ```

### <code>log</code>コマンド {#the-code-log-code-command}

TiDBエラーログのスタック情報は1行形式です。 `tidb-ctl log`を使用して、フォーマットを複数行に変更できます。

### <code>keyrange</code>コマンド {#the-code-keyrange-code-command}

`keyrange`サブコマンドは、16進形式で出力されるグローバルまたはテーブル関連のキー範囲情報を照会するために使用されます。

-   `tidb-ctl keyrange`コマンドを実行して、グローバルキー範囲情報を確認します。

    {{< copyable "" >}}

    ```shell
    tidb-ctl keyrange
    ```

    ```
    global ranges:
      meta: (6d, 6e)
      table: (74, 75)
    ```

-   エンコードされたキーを表示する`--encode`のオプションを追加します（TiKVおよびPDと同じ形式で）：

    {{< copyable "" >}}

    ```shell
    tidb-ctl keyrange --encode
    ```

    ```
    global ranges:
      meta: (6d00000000000000f8, 6e00000000000000f8)
      table: (7400000000000000f8, 7500000000000000f8)
    ```

-   `tidb-ctl keyrange --database={db} --table={tbl}`コマンドを実行して、グローバルおよびテーブル関連のキー範囲情報を確認します。

    {{< copyable "" >}}

    ```shell
    tidb-ctl keyrange --database test --table ttt
    ```

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
    ```
