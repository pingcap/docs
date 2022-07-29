---
title: Upgrade and After Upgrade FAQs
summary: Learn about some FAQs and the solutions during and after upgrading TiDB.
---

# アップグレードおよびアップグレード後のFAQ {#upgrade-and-after-upgrade-faqs}

このドキュメントでは、TiDBをアップグレードするときまたはアップグレードした後のいくつかのFAQとその解決策を紹介します。

## アップグレードに関するよくある質問 {#upgrade-faqs}

このセクションでは、TiDBをアップグレードする際のいくつかのFAQとその解決策を示します。

### ローリングアップデートの効果は何ですか？ {#what-are-the-effects-of-rolling-updates}

ローリング更新をTiDBサービスに適用すると、実行中のアプリケーションはさまざまな程度で影響を受けます。したがって、ビジネスのピーク時にローリング更新を実行することはお勧めしません。最小クラスタトポロジ（TiDB * 2、PD * 3、TiKV * 3）を構成する必要があります。PumpまたはDrainerサービスがクラスタに含まれている場合は、更新をローリングする前にDrainerを停止することをお勧めします。 TiDBをアップグレードすると、 Pumpもアップグレードされます。

### DDL実行中にTiDBクラスタをアップグレードできますか？ {#can-i-upgrade-the-tidb-cluster-during-the-ddl-execution}

DDLステートメントがクラスタで実行されているときは**TiDB**クラスタをアップグレードしないでください（通常、 `ADD INDEX`などの時間のかかるDDLステートメントや列タイプの変更の場合）。

アップグレードする前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDBクラスタに進行中のDDLジョブがあるかどうかを確認することをお勧めします。クラスタにDDLジョブがある場合、クラスタをアップグレードするには、DDLの実行が終了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用してDDLジョブをキャンセルしてからクラスタをアップグレードします。

さらに、クラスタのアップグレード中は、DDLステートメントを実行し**ない**でください。そうしないと、未定義動作の問題が発生する可能性があります。

### バイナリを使用してTiDBをアップグレードするにはどうすればよいですか？ {#how-to-upgrade-tidb-using-the-binary}

バイナリを使用してTiDBをアップグレードすることはお勧めしません。代わりに、バージョンの一貫性と互換性の両方を保証する[TiUPを使用してTiDBをアップグレードする](/upgrade-tidb-using-tiup.md)または[KubernetesでTiDBクラスタをアップグレードする](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)にすることをお勧めします。

## アップグレード後のよくある質問 {#after-upgrade-faqs}

このセクションでは、TiDBをアップグレードした後のいくつかのFAQとその解決策を示します。

### DDL操作の実行時に文字セット（文字セット）エラーが発生する {#the-character-set-charset-errors-when-executing-ddl-operations}

v2.1.0以前のバージョン（v2.0のすべてのバージョンを含む）では、TiDBの文字セットはデフォルトでUTF-8です。ただし、v2.1.1以降、デフォルトの文字セットはUTF8MB4に変更されました。

新しく作成されたテーブルの文字セットをv2.1.0以前のバージョンでUTF-8として明示的に指定すると、TiDBをv2.1.1にアップグレードした後にDDL操作の実行に失敗する可能性があります。

この問題を回避するには、次の点に注意する必要があります。

-   v2.1.3より前では、TiDBは列の文字セットの変更をサポートしていません。したがって、DDL操作を実行するときは、新しい列の文字セットが元の列の文字セットと一致していることを確認する必要があります。

-   v2.1.3より前では、列の文字セットがテーブルの文字セットと異なっていても、 `show create table`は列の文字セットを表示しません。ただし、次の例に示すように、HTTPAPIを介してテーブルのメタデータを取得することで表示できます。

#### <code>unsupported modify column charset utf8mb4 not match origin utf8</code> {#code-unsupported-modify-column-charset-utf8mb4-not-match-origin-utf8-code}

-   アップグレードする前に、v2.1.0以前のバージョンでは次の操作が実行されます。

    {{< copyable "" >}}

    ```sql
    create table t(a varchar(10)) charset=utf8;
    ```

    ```
    Query OK, 0 rows affected
    Time: 0.106s
    ```

    {{< copyable "" >}}

    ```sql
    show create table t;
    ```

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
    ```

-   アップグレード後、v2.1.1およびv2.1.2では次のエラーが報告されますが、v2.1.3以降のバージョンではそのようなエラーはありません。

    {{< copyable "" >}}

    ```sql
    alter table t change column a a varchar(20);
    ```

    ```
    ERROR 1105 (HY000): unsupported modify column charset utf8mb4 not match origin utf8
    ```

解決：

列の文字セットを元の文字セットと同じように明示的に指定できます。

{{< copyable "" >}}

```sql
alter table t change column a a varchar(22) character set utf8;
```

-   ポイント1によると、列の文字セットを指定しない場合、デフォルトでUTF8MB4が使用されるため、元の文字セットと一致するように列の文字セットを指定する必要があります。

-   ポイント2によると、HTTP APIを介してテーブルのメタデータを取得し、列名とキーワード「Charset」を検索することで列の文字セットを見つけることができます。

    {{< copyable "" >}}

    ```sh
    curl "http://$IP:10080/schema/test/t" | python -m json.tool
    ```

    ここでは、Pythonツールを使用してJSONをフォーマットします。これは必須ではなく、コメントを追加するためだけに使用されます。

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

-   アップグレードする前に、v2.1.1およびv2.1.2では次の操作が実行されます。

    {{< copyable "" >}}

    ```sql
    create table t(a varchar(10)) charset=utf8;
    ```

    ```
    Query OK, 0 rows affected
    Time: 0.109s
    ```

    {{< copyable "" >}}

    ```sql
    show create table t;
    ```

    ```
    +-------+-------------------------------------------------------+
    | Table | Create Table                                          |
    +-------+-------------------------------------------------------+
    | t     | CREATE TABLE `t` (                                    |
    |       |   `a` varchar(10) DEFAULT NULL                        |
    |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
    +-------+-------------------------------------------------------+
    ```

    上記の例では、 `show create table`はテーブルの文字セットのみを示していますが、列の文字セットは実際にはUTF8MB4であり、HTTPAPIを介してスキーマを取得することで確認できます。ただし、新しいテーブルが作成されると、列の文字セットはテーブルの文字セットと一致している必要があります。このバグはv2.1.3で修正されています。

-   アップグレード後、v2.1.3以降のバージョンでは次の操作が実行されます。

    {{< copyable "" >}}

    ```sql
    show create table t;
    ```

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
    ```

    {{< copyable "" >}}

    ```sql
    alter table t change column a a varchar(20);
    ```

    ```
    ERROR 1105 (HY000): unsupported modify charset from utf8mb4 to utf8
    ```

解決：

-   v2.1.3以降、TiDBは列とテーブルの文字セットの変更をサポートしているため、テーブルの文字セットをUTF8MB4に変更することをお勧めします。

    {{< copyable "" >}}

    ```sql
    alter table t convert to character set utf8mb4;
    ```

-   問題＃1で行ったように列文字セットを指定して、元の列文字セット（UTF8MB4）との整合性を保つこともできます。

    {{< copyable "" >}}

    ```sql
    alter table t change column a a varchar(20) character set utf8mb4;
    ```

#### <code>ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a</code> {#code-error-1366-hy000-incorrect-utf8-value-f09f8c80-for-column-a-code}

TiDB v2.1.1以前のバージョンでは、文字セットがUTF-8の場合、挿入された4バイトデータに対するUTF-8Unicodeエンコーディングチェックはありません。ただし、v2.1.2以降のバージョンでは、このチェックが追加されています。

-   アップグレードする前に、v2.1.1以前のバージョンでは次の操作が実行されます。

    {{< copyable "" >}}

    ```sql
    create table t(a varchar(100) charset utf8);
    ```

    ```
    Query OK, 0 rows affected
    ```

    {{< copyable "" >}}

    ```sql
    insert t values (unhex('f09f8c80'));
    ```

    ```
    Query OK, 1 row affected
    ```

-   アップグレード後、v2.1.2以降のバージョンでは次のエラーが報告されます。

    {{< copyable "" >}}

    ```sql
    insert t values (unhex('f09f8c80'));
    ```

    ```
    ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a
    ```

解決：

-   v2.1.2の場合：このバージョンは列文字セットの変更をサポートしていないため、UTF-8チェックをスキップする必要があります。

    {{< copyable "" >}}

    ```sql
    set @@session.tidb_skip_utf8_check=1;
    ```

    ```
    Query OK, 0 rows affected
    ```

    {{< copyable "" >}}

    ```sql
    insert t values (unhex('f09f8c80'));
    ```

    ```
    Query OK, 1 row affected
    ```

-   v2.1.3以降のバージョン：列の文字セットをUTF8MB4に変更することをお勧めします。または、 `tidb_skip_utf8_check`を設定してUTF-8チェックをスキップすることもできます。ただし、チェックをスキップすると、MySQLがチェックを実行するため、TiDBからMySQLへのデータの複製に失敗する可能性があります。

    {{< copyable "" >}}

    ```sql
    alter table t change column a a varchar(100) character set utf8mb4;
    ```

    ```
    Query OK, 0 rows affected
    ```

    {{< copyable "" >}}

    ```sql
    insert t values (unhex('f09f8c80'));
    ```

    ```
    Query OK, 1 row affected
    ```

    具体的には、変数`tidb_skip_utf8_check`を使用して、データの正当なUTF-8およびUTF8MB4チェックをスキップできます。ただし、チェックをスキップすると、MySQLがチェックを実行するため、TiDBからMySQLへのデータの複製に失敗する可能性があります。

    UTF-8チェックのみをスキップする場合は、 `tidb_check_mb4_value_in_utf8`を設定できます。この変数はv2.1.3の`config.toml`ファイルに追加され、構成ファイルの`check-mb4-value-in-utf8`を変更してから、クラスタを再起動して有効にすることができます。

    v2.1.5以降、HTTPAPIとセッション変数を介して`tidb_check_mb4_value_in_utf8`を設定できます。

    -   HTTP API（HTTP APIは単一のサーバーでのみ有効にできます）

        -   HTTP APIを有効にするには：

            {{< copyable "" >}}

            ```sh
            curl -X POST -d "check_mb4_value_in_utf8=1" http://{TiDBIP}:10080/settings
            ```

        -   HTTP APIを無効にするには：

            {{< copyable "" >}}

            ```sh
            curl -X POST -d "check_mb4_value_in_utf8=0" http://{TiDBIP}:10080/settings
            ```

    -   セッション変数

        -   セッション変数を有効にするには：

            {{< copyable "" >}}

            ```sql
            set @@session.tidb_check_mb4_value_in_utf8 = 1;
            ```

        -   セッション変数を無効にするには：

            {{< copyable "" >}}

            ```sql
            set @@session.tidb_check_mb4_value_in_utf8 = 0;
            ```
