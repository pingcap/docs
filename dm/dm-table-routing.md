---
title: TiDB Data Migration Table Routing
summary: DM におけるテーブル ルーティングの使用方法と注意事項を学びます。
---

# TiDBデータ移行テーブルルーティング {#tidb-data-migration-table-routing}

TiDB データ移行 (DM) を使用してデータを移行する場合、テーブル ルーティングを構成して、アップストリーム MySQL または MariaDB インスタンスの特定のテーブルをダウンストリームの指定されたテーブルに移行できます。

> **注記：**
>
> -   1 つのテーブルに対して複数の異なるルーティング ルールを構成することはサポートされていません。
> -   セクション[テーブルルーティングを構成する](#configure-table-routing)の`rule-2`に示すように、 `CREATE/DROP SCHEMA xx`移行するために使用されるスキーマの一致ルールを個別に構成する必要があります。

## テーブルルーティングを構成する {#configure-table-routing}

```yaml
routes:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
    # extract-table, extract-schema, and extract-source are optional and
    # are required only when you need to extract information about sharded
    # tables, sharded schemas, and source datatabase information.
    extract-table:
      table-regexp: "t_(.*)"
      target-column: "c_table"
    extract-schema:
      schema-regexp: "test_(.*)"
      target-column: "c_schema"
    extract-source:
      source-regexp: "(.*)"
      target-column: "c_source"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

データベース名とテーブル名のマッチングには、正規表現とワイルドカードがサポートされています。シンプルなシナリオでは、スキーマとテーブルのマッチングにワイルドカードを使用することをお勧めします。ただし、以下の点にご注意ください。

-   `*` `[]`含むワイルドカードがサポートされています。ワイルドカードマッチでは`*`記号は1 `?`だけ使用でき、末尾になければなりません。例えば、 `table-pattern: "t_*"`の場合、 `"t_*"` `t_`で始まるすべてのテーブルを表します。詳細は[ワイルドカードマッチング](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)参照してください。

-   `table-regexp` 、 `schema-regexp` 、 `source-regexp`正規表現のみをサポートし、 `~`記号で始まることはできません。

-   `schema-pattern`と`table-pattern`ワイルドカードと正規表現の両方をサポートします。正規表現は`~`で始まる必要があります。

## パラメータの説明 {#parameter-descriptions}

-   DM は`target-table` [テーブルセレクターによって提供される`schema-pattern` / `table-pattern`ルール](/dm/table-selector.md)一致するアップストリーム MySQL または MariaDB インスタンス テーブルをダウンストリーム`target-schema`に移行します。
-   `schema-pattern` / `table-pattern`ルールに一致するシャードテーブルについては、DM は`extract-table` . `table-regexp`正規表現を使用してテーブル名、 `extract-schema` . `schema-regexp`正規表現を使用してスキーマ名、 `extract-source` . `source-regexp`正規表現を使用してソース情報を抽出します。その後、DM は抽出した情報を下流のマージ済みテーブルの対応する`target-column`に書き込みます。

## 使用例 {#usage-examples}

このセクションでは、4 つの異なるシナリオでの使用例を示します。

小さなデータセットの MySQL シャードを TiDB に移行してマージする必要がある場合は、 [このチュートリアル](/migrate-small-mysql-shards-to-tidb.md)を参照してください。

### シャード化されたスキーマとテーブルをマージする {#merge-sharded-schemas-and-tables}

シャードされたスキーマとテーブルのシナリオを想定して、2 つのアップストリーム MySQL インスタンスの`test_{1,2,3...}`テーブル`t_{1,2,3...}`ダウンストリーム TiDB インスタンスの`test` `t`に移行します。

アップストリームインスタンスをダウンストリーム`test` . `t`に移行するには、次のルーティングルールを作成する必要があります。

-   `rule-1` 、 `schema-pattern: "test_*"`および`table-pattern: "t_*"`一致するテーブルの DML または DDL ステートメントをダウンストリーム`test` 。 `t`に移行するために使用されます。
-   `rule-2` 、 `CREATE/DROP SCHEMA xx`など、 `schema-pattern: "test_*"`一致するスキーマの DDL ステートメントを移行するために使用されます。

> **注記：**
>
> -   下流`schema: test`がすでに存在し、削除しない場合は`rule-2`省略できます。
> -   ダウンストリーム`schema: test`が存在せず、 `rule-1`のみが構成されている場合、移行中に`schema test doesn't exist`エラーが報告されます。

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

### テーブル、スキーマ、ソース情報を抽出し、結合されたテーブルに書き込みます {#extract-table-schema-and-source-information-and-write-into-the-merged-table}

シャード化されたスキーマとテーブルのシナリオを想定し、2つの上流MySQLインスタンスの`test_{1,2,3...}`テーブル`t_{1,2,3...}`下流TiDBインスタンスの`test`テーブルに移行します。同時に`t`シャード化されたテーブルのソース情報を抽出し、下流のマージされたテーブルに書き込みます。

`t`ストリームインスタンスをダウンストリームインスタンス`test`に移行するには、前のセクション[シャード化されたスキーマとテーブルをマージする](#merge-sharded-schemas-and-tables)と同様のルーティングルールを作成する必要があります。さらに、 `extract-table` 、 `extract-schema` 、および`extract-source`設定を追加する必要があります。

-   `extract-table` : `schema-pattern`と`table-pattern`一致するシャード テーブルの場合、DM は`table-regexp`を使用してシャード テーブル名を抽出し、 `t_`部分を除いた名前サフィックスを結合されたテーブルの`target-column` (つまり、 `c_table`列目) に書き込みます。
-   `extract-schema` : `schema-pattern`と`table-pattern`一致するシャード スキーマの場合、DM は`schema-regexp`を使用してシャード スキーマ名を抽出し、 `test_`部分を除いた名前サフィックスを、結合されたテーブルの`target-column` (つまり、 `c_schema`列目) に書き込みます。
-   `extract-source` : `schema-pattern`と`table-pattern`一致するシャード テーブルの場合、DM はソース インスタンス情報をマージされたテーブルの`target-column` 、つまり`c_source`列に書き込みます。

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
    extract-table:
      table-regexp: "t_(.*)"
      target-column: "c_table"
    extract-schema:
      schema-regexp: "test_(.*)"
      target-column: "c_schema"
    extract-source:
      source-regexp: "(.*)"
      target-column: "c_source"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

上流のシャードテーブルのソース情報を下流のマージテーブルに抽出するには、**移行を開始する前に、下流にマージテーブルを手動で作成する必要があります**。マージテーブルには、ソース情報を指定するために使用する3つ`target-columns` （ `c_table` 、 `c_schema` 、 `c_source` ）が含まれている必要があります。また、これらの列は**最後の列であり、<a href="/data-type-string.md">文字列型</a>である必要があります**。

```sql
CREATE TABLE `test`.`t` (
    a int PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

アップストリームに次の 2 つのデータ ソースがあると仮定します。

データソース`mysql-01` :

```sql
mysql> select * from test_11.t_1;
+---+
| a |
+---+
| 1 |
+---+
mysql> select * from test_11.t_2;
+---+
| a |
+---+
| 2 |
+---+
mysql> select * from test_12.t_1;
+---+
| a |
+---+
| 3 |
+---+
```

データソース`mysql-02` :

```sql
mysql> select * from test_13.t_3;
+---+
| a |
+---+
| 4 |
+---+
```

DM を使用して移行すると、マージされたテーブル内のデータは次のようになります。

```sql
mysql> select * from test.t;
+---+---------+----------+----------+
| a | c_table | c_schema | c_source |
+---+---------+----------+----------+
| 1 | 1       | 11       | mysql-01 |
| 2 | 2       | 11       | mysql-01 |
| 3 | 1       | 12       | mysql-01 |
| 4 | 3       | 13       | mysql-02 |
+---+---------+----------+----------+
```

#### 結合テーブルの作成の誤った例 {#incorrect-examples-of-creating-merged-tables}

> **注記：**
>
> 次のいずれかのエラーが発生した場合、シャードされたテーブルとスキーマのソース情報がマージされたテーブルに書き込まれない可能性があります。

-   最後の 3 列に`c-table`がありません。

```sql
CREATE TABLE `test`.`t` (
    c_table varchar(10) DEFAULT NULL,
    a int PRIMARY KEY,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

-   `c-source`は存在しません:

```sql
CREATE TABLE `test`.`t` (
    a int PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
);
```

-   `c_schema`は文字列型ではありません:

```sql
CREATE TABLE `test`.`t` (
    a int PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema int DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL,
);
```

### シャードスキーマをマージする {#merge-sharded-schemas}

シャード スキーマのシナリオを想定して、2 つのアップストリーム MySQL インスタンスの`test_{1,2,3...}`テーブル`t_{1,2,3...}`ダウンストリーム TiDB インスタンスの`test` `t_{1,2,3...}`に移行します。

アップストリーム スキーマをダウンストリーム`test` . `t_[1,2,3]`に移行するには、ルーティング ルールを 1 つだけ作成する必要があります。

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

### テーブルルーティングが正しくありません {#incorrect-table-routing}

次の 2 つのルーティング ルールが設定されていて、 `test_1_bak` `t_1_bak` `rule-1`と`rule-2`両方に一致する場合、テーブル ルーティング設定が数値制限に違反するためエラーが報告されます。

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_1_bak"
    table-pattern: "t_1_bak"
    target-schema: "test"
    target-table: "t_bak"
```
