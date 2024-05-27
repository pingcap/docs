---
title: TiDB Data Migration Table Routing
summary: DM におけるテーブル ルーティングの使用方法と注意事項を学びます。
---

# TiDB データ移行テーブルルーティング {#tidb-data-migration-table-routing}

TiDB データ移行 (DM) を使用してデータを移行する場合、テーブル ルーティングを構成して、アップストリーム MySQL または MariaDB インスタンスの特定のテーブルをダウンストリームの指定されたテーブルに移行できます。

> **注記：**
>
> -   単一のテーブルに対して複数の異なるルーティング ルールを構成することはサポートされていません。
> -   [テーブルルーティングを構成する](#configure-table-routing)のセクションの`rule-2`に示すように、移行`CREATE/DROP SCHEMA xx`に使用されるスキーマの一致ルールを個別に構成する必要があります。

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

データベース名とテーブル名の一致には、正規表現とワイルドカードがサポートされています。単純なシナリオでは、スキーマとテーブルの一致にワイルドカードを使用することをお勧めします。ただし、次の点に注意してください。

-   `*` 、 `?` 、 `[]`などのワイルドカードがサポートされています。ワイルドカードの一致には`*`記号が 1 つだけ存在でき、末尾に配置する必要があります。たとえば、 `table-pattern: "t_*"`では、 `"t_*"` `t_`で始まるすべてのテーブルを示します。詳細については[ワイルドカードマッチング](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)を参照してください。

-   `table-regexp` 、 `schema-regexp` 、 `source-regexp`正規表現のみをサポートし、 `~`記号で始まることはできません。

-   `schema-pattern`と`table-pattern`ワイルドカードと正規表現の両方をサポートします。正規表現は`~`記号で始まる必要があります。

## パラメータの説明 {#parameter-descriptions}

-   DM は`target-table` [テーブルセレクターによって提供される`schema-pattern` / `table-pattern`ルール](/dm/table-selector.md)に一致するアップストリーム MySQL または MariaDB インスタンス テーブルをダウンストリーム`target-schema`に移行します。
-   `schema-pattern` / `table-pattern`ルールに一致するシャード テーブルの場合、DM は`extract-table` . `table-regexp`正規表現を使用してテーブル名を抽出し、 `extract-schema` . `schema-regexp`正規表現を使用してスキーマ名を抽出し、 `extract-source` . `source-regexp`正規表現を使用してソース情報を抽出します。次に、DM は抽出した情報を下流のマージされたテーブルの対応する`target-column`に書き込みます。

## 使用例 {#usage-examples}

このセクションでは、4 つの異なるシナリオでの使用例を示します。

小さなデータセットの MySQL シャードを TiDB に移行してマージする必要がある場合は、 [このチュートリアル](/migrate-small-mysql-shards-to-tidb.md)を参照してください。

### シャード化されたスキーマとテーブルをマージする {#merge-sharded-schemas-and-tables}

シャード化されたスキーマとテーブルのシナリオを想定して、2 つ`t` `test_{1,2,3...}` `t_{1,2,3...}` `test`します。

アップストリームインスタンスをダウンストリーム`test` . `t`に移行するには、次のルーティングルールを作成する必要があります。

-   `rule-1`は、 `schema-pattern: "test_*"`および`table-pattern: "t_*"`に一致するテーブルの DML または DDL ステートメントをダウンストリーム`test` . `t`に移行するために使用されます。
-   `rule-2`は、 `CREATE/DROP SCHEMA xx`など、 `schema-pattern: "test_*"`に一致するスキーマの DDL ステートメントを移行するために使用されます。

> **注記：**
>
> -   下流`schema: test`すでに存在し、削除しない場合は`rule-2`省略できます。
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

### テーブル、スキーマ、ソース情報を抽出し、マージされたテーブルに書き込みます。 {#extract-table-schema-and-source-information-and-write-into-the-merged-table}

シャードされたスキーマとテーブルのシナリオを想定して、 `t_{1,2,3...}` `test_{1,2,3...}`をダウンストリーム TiDB インスタンスの`test`テーブルに移行します。同時に、シャードされたテーブルのソース情報を抽出し、それをダウン`t`のマージされたテーブルに書き込みます。

アップストリームインスタンスをダウンストリーム`test`に移行するには、前のセクション[シャード化されたスキーマとテーブルをマージする](#merge-sharded-schemas-and-tables)と同様のルーティングルールを作成する必要があります。 `t` 、 `extract-table` 、 `extract-schema` 、および`extract-source`構成を追加する必要があります。

-   `extract-table` : `schema-pattern`と`table-pattern`に一致するシャード テーブルの場合、DM は`table-regexp`を使用してシャード テーブル名を抽出し、 `t_`部分を除いた名前サフィックスをマージされたテーブルの`target-column` 、つまり`c_table`列に書き込みます。
-   `extract-schema` : `schema-pattern`と`table-pattern`に一致するシャード スキーマの場合、DM は`schema-regexp`を使用してシャード スキーマ名を抽出し、 `test_`部分を除いた名前サフィックスをマージされたテーブルの`target-column` 、つまり`c_schema`列に書き込みます。
-   `extract-source` : `schema-pattern`と`table-pattern`に一致するシャード テーブルの場合、DM はソース インスタンス情報をマージされたテーブルの`target-column` 、つまり`c_source`列に書き込みます。

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

アップストリームのシャードテーブルのソース情報をダウンストリームのマージテーブルに抽出するには、**移行を開始する前に、ダウンストリームにマージテーブルを手動で作成する必要があります**。マージテーブルには、ソース情報を指定するために使用される 3 つの`target-columns` ( `c_table` 、 `c_schema` 、および`c_source` ) が含まれている必要があります。また、これらの列は**最後の列であり、<a href="/data-type-string.md">文字列型</a>である必要があります**。

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
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

#### 結合テーブルを作成する際の誤った例 {#incorrect-examples-of-creating-merged-tables}

> **注記：**
>
> 次のいずれかのエラーが発生した場合、シャードされたテーブルとスキーマのソース情報がマージされたテーブルに書き込まれない可能性があります。

-   最後の 3 列に`c-table`がありません。

```sql
CREATE TABLE `test`.`t` (
    c_table varchar(10) DEFAULT NULL,
    a int(11) PRIMARY KEY,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

-   `c-source`は存在しません:

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
);
```

-   `c_schema`文字列型ではありません:

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema int(11) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL,
);
```

### 分割されたスキーマをマージする {#merge-sharded-schemas}

シャードされたスキーマのシナリオを想定して、2 つ`t_{1,2,3...}` `test_{1,2,3...}` `t_{1,2,3...}` `test`します。

アップストリーム スキーマをダウンストリーム`test` . `t_[1,2,3]`に移行するには、ルーティング ルールを 1 つだけ作成する必要があります。

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

### テーブルルーティングが正しくありません {#incorrect-table-routing}

次の 2 つのルーティング ルールが設定されており、 `test_1_bak` . `t_1_bak` `rule-1`と`rule-2`両方に一致すると、テーブル ルーティング設定が数値制限に違反するためエラーが報告されます。

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
