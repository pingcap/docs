---
title: Upgrade and After Upgrade FAQs
summary: Learn about some FAQs and the solutions during and after upgrading TiDB.
---

# アップグレードおよびアップグレード後のよくある質問 {#upgrade-and-after-upgrade-faqs}

このドキュメントでは、TiDB のアップグレード時またはアップグレード後のいくつかの FAQ とその解決策を紹介します。

## アップグレードに関するよくある質問 {#upgrade-faqs}

このセクションでは、TiDB をアップグレードする際のいくつかの FAQ とその解決策を示します。

### ローリングアップデートの影響は何ですか? {#what-are-the-effects-of-rolling-updates}

TiDB サービスにローリング アップデートを適用すると、実行中のアプリケーションはさまざまな程度の影響を受けます。したがって、ビジネスのピーク時間中にローリング アップデートを実行することはお勧めできません。最小のクラスタトポロジ（TiDB * 2、PD * 3、TiKV * 3）を構成する必要があります。 PumpサービスまたはDrainerサービスがクラスターに関与している場合は、ローリング アップデートの前にDrainer を停止することをお勧めします。 TiDB をアップグレードすると、 Pumpもアップグレードされます。

### DDL の実行中に TiDB クラスターをアップグレードできますか? {#can-i-upgrade-the-tidb-cluster-during-the-ddl-execution}

-   アップグレード前の TiDB バージョンが v7.1.0 より前の場合:

    -   DDL ステートメントがクラスター内で実行されているときは、TiDB クラスターをアップグレードし**ないでください**(通常は、 `ADD INDEX`や列タイプの変更など、時間のかかる DDL ステートメントの場合)。アップグレードの前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDB クラスターに進行中の DDL ジョブがあるかどうかを確認することをお勧めします。クラスターに DDL ジョブがある場合、クラスターをアップグレードするには、DDL の実行が完了するまで待つか、クラスターをアップグレードする前に[`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルします。

    -   クラスターのアップグレード中は、DDL ステートメントを実行し**ないでください**。そうしないと、未定義の動作の問題が発生する可能性があります。

-   アップグレード前の TiDB バージョンが v7.1.0 以降の場合:

    -   以前のバージョンから v7.1.0 にアップグレードする場合の制限に従う必要はありません。つまり、TiDB はアップグレード中にユーザーの DDL タスクを受け取ることができます。詳細は[TiDB のスムーズなアップグレード](/smooth-upgrade-tidb.md)を参照してください。

### バイナリを使用して TiDB をアップグレードするにはどうすればよいですか? {#how-to-upgrade-tidb-using-the-binary}

バイナリを使用して TiDB をアップグレードすることはお勧めできません。代わりに、バージョンの一貫性と互換性の両方を保証する[TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)または[Kubernetes 上の TiDB クラスターをアップグレードする](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)をお勧めします。

## アップグレード後のよくある質問 {#after-upgrade-faqs}

このセクションでは、TiDB をアップグレードした後のいくつかの FAQ とその解決策をリストします。

### DDL 操作実行時の文字セット (charset) エラー {#the-character-set-charset-errors-when-executing-ddl-operations}

v2.1.0 以前のバージョン (v2.0 のすべてのバージョンを含む) では、TiDB の文字セットはデフォルトで UTF-8 です。ただし、v2.1.1 からは、デフォルトの文字セットが UTF8MB4 に変更されました。

v2.1.0 以前のバージョンで新しく作成したテーブルの文字セットを UTF-8 として明示的に指定した場合、TiDB を v2.1.1 にアップグレードした後に DDL 操作の実行に失敗する可能性があります。

この問題を回避するには、次の点に注意する必要があります。

-   v2.1.3 より前では、TiDB は列の文字セットの変更をサポートしていません。したがって、DDL 操作を実行するときは、新しい列の文字セットが元の列の文字セットと一致していることを確認する必要があります。

-   v2.1.3 より前では、列の文字セットがテーブルの文字セットと異なっていても、 `show create table`は列の文字セットを示しません。ただし、次の例に示すように、HTTP API を通じてテーブルのメタデータを取得することで表示できます。

#### <code>unsupported modify column charset utf8mb4 not match origin utf8</code> {#code-unsupported-modify-column-charset-utf8mb4-not-match-origin-utf8-code}

-   v2.1.0以前のバージョンでは、アップグレード前に以下の操作が実行されます。

    ```sql
    create table t(a varchar(10)) charset=utf8;
    ```

        Query OK, 0 rows affected
        Time: 0.106s

    ```sql
    show create table t;
    ```

        +-------+-------------------------------------------------------+
        | Table | Create Table                                          |
        +-------+-------------------------------------------------------+
        | t     | CREATE TABLE `t` (                                    |
        |       |   `a` varchar(10) DEFAULT NULL                        |
        |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
        +-------+-------------------------------------------------------+
        1 row in set
        Time: 0.006s

-   アップグレード後、v2.1.1 および v2.1.2 では次のエラーが報告されますが、v2.1.3 以降のバージョンではそのようなエラーは発生しません。

    ```sql
    alter table t change column a a varchar(20);
    ```

        ERROR 1105 (HY000): unsupported modify column charset utf8mb4 not match origin utf8

解決：

列の文字セットを元の文字セットと同じものとして明示的に指定できます。

```sql
alter table t change column a a varchar(22) character set utf8;
```

-   ポイント #1 によると、列の文字セットを指定しない場合、デフォルトで UTF8MB4 が使用されるため、元の文字セットと一致させるために列の文字セットを指定する必要があります。

-   ポイント #2 によると、HTTP API を通じてテーブルのメタデータを取得し、列名とキーワード「Charset」を検索することで列の文字セットを見つけることができます。

    ```sh
    curl "http://$IP:10080/schema/test/t" | python -m json.tool
    ```

    ここでは Python ツールを使用して JSON をフォーマットしていますが、これは必須ではなく、コメントを追加するためだけに使用されています。

    ```json
    {
        "ShardRowIDBits": 0,
        "auto_inc_id": 0,
        "charset": "utf8",   # The charset of the table.
        "collate": "",
        "cols": [            # The relevant information about the columns.
            {
                ...
                "id": 1,
                "name": {
                    "L": "a",
                    "O": "a"   # The column name.
                },
                "offset": 0,
                "origin_default": null,
                "state": 5,
                "type": {
                    "Charset": "utf8",   # The charset of column a.
                    "Collate": "utf8_bin",
                    "Decimal": 0,
                    "Elems": null,
                    "Flag": 0,
                    "Flen": 10,
                    "Tp": 15
                }
            }
        ],
        ...
    }
    ```

#### <code>unsupported modify charset from utf8mb4 to utf8</code> {#code-unsupported-modify-charset-from-utf8mb4-to-utf8-code}

-   アップグレード前に、v2.1.1 および v2.1.2 では次の操作が実行されます。

    ```sql
    create table t(a varchar(10)) charset=utf8;
    ```

        Query OK, 0 rows affected
        Time: 0.109s

    ```sql
    show create table t;
    ```

        +-------+-------------------------------------------------------+
        | Table | Create Table                                          |
        +-------+-------------------------------------------------------+
        | t     | CREATE TABLE `t` (                                    |
        |       |   `a` varchar(10) DEFAULT NULL                        |
        |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
        +-------+-------------------------------------------------------+

    上記の例では、 `show create table`テーブルの文字セットのみを示していますが、実際には列の文字セットは UTF8MB4 であり、HTTP API を通じてスキーマを取得することで確認できます。ただし、新しいテーブルを作成する場合、列の文字セットはテーブルの文字セットと一貫性を保つ必要があります。このバグは v2.1.3 で修正されました。

-   バージョンアップ後、v2.1.3 以降では以下の操作が実行されます。

    ```sql
    show create table t;
    ```

        +-------+--------------------------------------------------------------------+
        | Table | Create Table                                                       |
        +-------+--------------------------------------------------------------------+
        | t     | CREATE TABLE `t` (                                                 |
        |       |   `a` varchar(10) CHARSET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL |
        |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin              |
        +-------+--------------------------------------------------------------------+
        1 row in set
        Time: 0.007s

    ```sql
    alter table t change column a a varchar(20);
    ```

        ERROR 1105 (HY000): unsupported modify charset from utf8mb4 to utf8

解決：

-   v2.1.3 以降、TiDB は列とテーブルの文字セットの変更をサポートするため、テーブルの文字セットを UTF8MB4 に変更することをお勧めします。

    ```sql
    alter table t convert to character set utf8mb4;
    ```

-   問題 #1 で行ったように列の文字セットを指定して、元の列の文字セット (UTF8MB4) との一貫性を保つこともできます。

    ```sql
    alter table t change column a a varchar(20) character set utf8mb4;
    ```

#### <code>ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a</code> {#code-error-1366-hy000-incorrect-utf8-value-f09f8c80-for-column-a-code}

TiDB v2.1.1 以前のバージョンでは、文字セットが UTF-8 の場合、挿入された 4 バイト データに対する UTF-8 Unicode エンコード チェックは行われません。ただし、v2.1.2以降ではこのチェックが追加されています。

-   v2.1.1以前のバージョンでは、アップグレード前に以下の操作が実行されます。

    ```sql
    create table t(a varchar(100) charset utf8);
    ```

        Query OK, 0 rows affected

    ```sql
    insert t values (unhex('f09f8c80'));
    ```

        Query OK, 1 row affected

-   アップグレード後、v2.1.2 以降のバージョンでは次のエラーが報告されます。

    ```sql
    insert t values (unhex('f09f8c80'));
    ```

        ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a

解決：

-   v2.1.2: このバージョンは列の文字セットの変更をサポートしていないため、UTF-8 チェックをスキップする必要があります。

    ```sql
    set @@session.tidb_skip_utf8_check=1;
    ```

        Query OK, 0 rows affected

    ```sql
    insert t values (unhex('f09f8c80'));
    ```

        Query OK, 1 row affected

-   v2.1.3 以降のバージョン: 列の文字セットを UTF8MB4 に変更することをお勧めします。または、 `tidb_skip_utf8_check`を設定して UTF-8 チェックをスキップすることもできます。ただし、チェックをスキップすると、MySQL がチェックを実行するため、TiDB から MySQL へのデータの複製に失敗する可能性があります。

    ```sql
    alter table t change column a a varchar(100) character set utf8mb4;
    ```

        Query OK, 0 rows affected

    ```sql
    insert t values (unhex('f09f8c80'));
    ```

        Query OK, 1 row affected

    具体的には、変数`tidb_skip_utf8_check`を使用して、データの正当な UTF-8 および UTF8MB4 チェックをスキップできます。ただし、チェックをスキップすると、MySQL がチェックを実行するため、TiDB から MySQL へのデータの複製に失敗する可能性があります。

    UTF-8 チェックのみをスキップしたい場合は、 `tidb_check_mb4_value_in_utf8`を設定できます。この変数は v2.1.3 の`config.toml`ファイルに追加されており、構成ファイル内の`check-mb4-value-in-utf8`変更してクラスターを再起動して有効にすることができます。

    v2.1.5 以降、HTTP API およびセッション変数を通じて`tidb_check_mb4_value_in_utf8`を設定できます。

    -   HTTP API（HTTP APIは単一サーバーでのみ有効にできます）

        -   HTTP API を有効にするには:

            ```sh
            curl -X POST -d "check_mb4_value_in_utf8=1" http://{TiDBIP}:10080/settings
            ```

        -   HTTP API を無効にするには:

            ```sh
            curl -X POST -d "check_mb4_value_in_utf8=0" http://{TiDBIP}:10080/settings
            ```

    -   セッション変数

        -   セッション変数を有効にするには:

            ```sql
            set @@session.tidb_check_mb4_value_in_utf8 = 1;
            ```

        -   セッション変数を無効にするには:

            ```sql
            set @@session.tidb_check_mb4_value_in_utf8 = 0;
            ```
