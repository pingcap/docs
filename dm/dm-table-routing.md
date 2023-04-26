---
title: TiDB Data Migration Table Routing
summary: Learn the usage and precautions of table routing in DM.
---

# TiDB データ移行テーブル ルーティング {#tidb-data-migration-table-routing}

TiDB Data Migration (DM) を使用してデータを移行する場合、アップストリームの MySQL または MariaDB インスタンスの特定のテーブルをダウンストリームの指定されたテーブルに移行するようにテーブル ルーティングを構成できます。

> **ノート：**
>
> -   1 つのテーブルに対して複数の異なるルーティング ルールを構成することはサポートされていません。
> -   スキーマの一致ルールは、セクション[テーブル ルーティングの構成](#configure-table-routing)の`rule-2`に示すように、移行`CREATE/DROP SCHEMA xx`に使用される個別に設定する必要があります。

## テーブル ルーティングの構成 {#configure-table-routing}

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

単純なシナリオでは、スキーマとテーブルの一致にワイルドカードを使用することをお勧めします。ただし、次のバージョンの違いに注意してください。

-   DM v1.0.5 以降のバージョンの場合、テーブル ルーティングは[ワイルドカードマッチ](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)サポートしますが、ワイルドカード式で指定できるのは`*`**だけ**であり、<strong>最後に</strong>`*`を配置する必要があります。

-   v1.0.5 より前のバージョンの DM では、テーブル ルーティングはワイルドカードをサポートしますが、 `[...]`と`[!...]`式はサポートしません。

## パラメータの説明 {#parameter-descriptions}

-   DM は、 [テーブル セレクターによって提供される`schema-pattern` / <code>table-pattern</code>ルール](/dm/table-selector.md)に一致する上流の MySQL または MariaDB インスタンス テーブルを下流の`target-schema` / `target-table`に移行します。
-   `schema-pattern`ルールに一致するシャード テーブルの場合、DM `table-pattern` `extract-table`を使用してテーブル名を抽出します。 `table-regexp`正規表現、 `extract-schema`を使用したスキーマ名。 `schema-regexp`正規表現、および`extract-source`を使用したソース情報。 `source-regexp`正規表現。次に、DM は、抽出された情報を下流のマージされたテーブルの対応する`target-column`に書き込みます。

## 使用例 {#usage-examples}

このセクションでは、4 つの異なるシナリオでの使用例を示します。

小さなデータセットの MySQL シャードを TiDB に移行してマージする必要がある場合は、 [このチュートリアル](/migrate-small-mysql-shards-to-tidb.md)を参照してください。

### シャードされたスキーマとテーブルをマージする {#merge-sharded-schemas-and-tables}

シャードされたスキーマとテーブルのシナリオで、 `test_{1,2,3...}`を移行すると仮定します。 `test`への 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`テーブル。ダウンストリーム TiDB インスタンスの`t`テーブル。

アップストリーム インスタンスをダウンストリームに移行するには`test` . `t`では、次のルーティング ルールを作成する必要があります。

-   `rule-1` 、 `schema-pattern: "test_*"`と`table-pattern: "t_*"`に一致するテーブルの DML または DDL ステートメントをダウンストリーム`test`に移行するために使用されます。 `t` .
-   `rule-2` 、 `CREATE/DROP SCHEMA xx`などの`schema-pattern: "test_*"`に一致するスキーマの DDL ステートメントを移行するために使用されます。

> **ノート：**
>
> -   ダウンストリーム`schema: test`既に存在し、削除しない場合は、 `rule-2`省略できます。
> -   ダウンストリーム`schema: test`存在せず、 `rule-1`のみが構成されている場合、移行中に`schema test doesn't exist`エラーが報告されます。

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

### テーブル、スキーマ、およびソース情報を抽出し、マージされたテーブルに書き込みます {#extract-table-schema-and-source-information-and-write-into-the-merged-table}

シャードされたスキーマとテーブルのシナリオで、 `test_{1,2,3...}`を移行すると仮定します。 `test`への 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`テーブル。ダウンストリーム TiDB インスタンスの`t`テーブル。同時に、シャードされたテーブルのソース情報を抽出し、それをダウンストリームのマージされたテーブルに書き込みたいと考えています。

アップストリーム インスタンスをダウンストリームに移行するには`test` . `t`では、前のセクション[シャードされたスキーマとテーブルをマージする](#merge-sharded-schemas-and-tables)と同様のルーティング ルールを作成する必要があります。さらに、 `extract-table` 、 `extract-schema` 、および`extract-source`構成を追加する必要があります。

-   `extract-table` : `schema-pattern`と`table-pattern`に一致するシャード テーブルの場合、DM は`table-regexp`使用してシャード テーブル名を抽出し、マージされたテーブルの`target-column` 、つまり`c_table`列に`t_`の部分を除いた名前サフィックスを書き込みます。
-   `extract-schema` : `schema-pattern`と`table-pattern`に一致するシャード スキーマの場合、DM は`schema-regexp`使用してシャード スキーマ名を抽出し、マージされたテーブルの`target-column` 、つまり`c_schema`列に`test_`の部分を除いた名前サフィックスを書き込みます。
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

アップストリームのシャード テーブルのソース情報をダウンストリームのマージされたテーブルに抽出するには、**移行を開始する前に、ダウンストリームでマージされたテーブルを手動で作成する必要があります**。結合されたテーブルには、ソース情報の指定に使用される 3 つの`target-columns` ( `c_table` 、 `c_schema` 、および`c_source` ) が含まれている必要があります。さらに、これらの列は<strong>最後の列であり、<a href="/data-type-string.md">文字列型</a>である必要があります</strong>。

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

アップストリームに次の 2 つのデータ ソースがあるとします。

データ ソース`mysql-01` :

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

データ ソース`mysql-02` :

```sql
mysql> select * from test_13.t_3;
+---+
| a |
+---+
| 4 |
+---+
```

DM を使用して移行した後、マージされたテーブルのデータは次のようになります。

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

#### マージされたテーブルを作成する間違った例 {#incorrect-examples-of-creating-merged-tables}

> **ノート：**
>
> 以下のいずれかのエラーが発生した場合、シャード テーブルおよびスキーマのソース情報がマージ テーブルに書き込まれない可能性があります。

-   最後の 3 列に`c-table`ありません。

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

-   `c_schema`は文字列型ではありません:

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema int(11) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL,
);
```

### シャードされたスキーマをマージする {#merge-sharded-schemas}

シャード スキーマのシナリオで、 `test_{1,2,3...}`を移行すると仮定します。 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`テーブルから`test` .ダウンストリームの TiDB インスタンスに`t_{1,2,3...}`テーブル。

アップストリーム スキーマをダウンストリームに移行するには`test` . `t_[1,2,3]`では、ルーティング ルールを 1 つだけ作成する必要があります。

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

### 不適切なテーブル ルーティング {#incorrect-table-routing}

次の 2 つのルーティング ルールが`test_1_bak`されていると仮定します。 `t_1_bak` `rule-1`と`rule-2`の両方に一致する場合、テーブル ルーティング構成が数の制限に違反しているため、エラーが報告されます。

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
