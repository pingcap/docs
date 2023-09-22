---
title: TiDB Data Migration Table Routing
summary: Learn the usage and precautions of table routing in DM.
---

# TiDB データ移行テーブルのルーティング {#tidb-data-migration-table-routing}

TiDB Data Migration (DM) を使用してデータを移行する場合、アップストリームの MySQL または MariaDB インスタンスの特定のテーブルをダウンストリームの指定されたテーブルに移行するようにテーブル ルーティングを構成できます。

> **注記：**
>
> -   1 つのテーブルに対して複数の異なるルーティング ルールを構成することはサポートされていません。
> -   スキーマの一致ルールは個別に構成する必要があります。これは、セクション[テーブルルーティングを構成する](#configure-table-routing)の`rule-2`に示すように、 `CREATE/DROP SCHEMA xx`の移行に使用されます。

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

データベース名とテーブル名を一致させるための正規表現とワイルドカードがサポートされています。単純なシナリオでは、スキーマとテーブルを一致させるためにワイルドカードを使用することをお勧めします。ただし、次の点に注意してください。

-   `*` 、 `?` 、および`[]`を含むワイルドカードがサポートされています。ワイルドカード一致では`*`シンボルは 1 つだけ使用でき、最後になければなりません。たとえば、 `table-pattern: "t_*"`では、 `"t_*"` `t_`で始まるすべてのテーブルを示します。詳細は[ワイルドカードマッチング](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)参照してください。

-   `table-regexp` 、 `schema-regexp` 、および`source-regexp`正規表現のみをサポートしており、 `~`記号で始めることはできません。

-   `schema-pattern`と`table-pattern` 、ワイルドカードと正規表現の両方をサポートします。正規表現は`~`記号で始まる必要があります。

## パラメータの説明 {#parameter-descriptions}

-   DM は、 [テーブル セレクターによって提供される`schema-pattern` / `table-pattern`ルール](/dm/table-selector.md)に一致するアップストリームの MySQL または MariaDB インスタンス テーブルをダウンストリーム`target-schema` `target-table`移行します。
-   `schema-pattern` / `table-pattern`ルールに一致するシャードテーブルの場合、DM は`extract-table`を使用してテーブル名を抽出します。 `table-regexp`正規表現、 `extract-schema`を使用したスキーマ名。 `schema-regexp`正規表現、および`extract-source`を使用したソース情報。 `source-regexp`の正規表現。次に、DM は抽出した情報を下流のマージされたテーブルの対応する`target-column`に書き込みます。

## 使用例 {#usage-examples}

このセクションでは、4 つの異なるシナリオでの使用例を示します。

小規模なデータセットの MySQL シャードを TiDB に移行してマージする必要がある場合は、 [このチュートリアル](/migrate-small-mysql-shards-to-tidb.md)を参照してください。

### シャードされたスキーマとテーブルをマージする {#merge-sharded-schemas-and-tables}

シャード化されたスキーマとテーブルのシナリオで、 `test_{1,2,3...}`を移行するとします。 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`テーブルを`test`にします。 `t`ダウンストリーム TiDB インスタンスのテーブル。

アップストリーム インスタンスをダウンストリームに移行するには、 `test`に従います。 `t`では、次のルーティング ルールを作成する必要があります。

-   `rule-1` 、 `schema-pattern: "test_*"`および`table-pattern: "t_*"`に一致するテーブルの DML または DDL ステートメントをダウンストリーム`test`に移行するために使用されます。 `t` ．
-   `rule-2` 、 `schema-pattern: "test_*"`一致するスキーマの DDL ステートメント ( `CREATE/DROP SCHEMA xx`など) を移行するために使用されます。

> **注記：**
>
> -   下流`schema: test`すでに存在し、削除しない場合は、 `rule-2`を省略できます。
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

### テーブル、スキーマ、ソース情報を抽出し、マージされたテーブルに書き込みます {#extract-table-schema-and-source-information-and-write-into-the-merged-table}

シャード化されたスキーマとテーブルのシナリオで、 `test_{1,2,3...}`を移行するとします。 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`テーブルを`test`にします。 `t`ダウンストリーム TiDB インスタンスのテーブル。同時に、シャードテーブルのソース情報を抽出し、それを下流のマージテーブルに書き込む必要があります。

アップストリーム インスタンスをダウンストリームに移行するには、 `test`に従います。 `t`前のセクション[シャードされたスキーマとテーブルをマージする](#merge-sharded-schemas-and-tables)と同様のルーティング ルールを作成する必要があります。さらに、 `extract-table` 、 `extract-schema` 、および`extract-source`構成を追加する必要があります。

-   `extract-table` : `schema-pattern`と`table-pattern`に一致するシャードテーブルの場合、DM は`table-regexp`を使用してシャードテーブル名を抽出し、 `t_`の部分を除いた名前サフィックスをマージされたテーブルの`target-column` 、つまり`c_table`列に書き込みます。
-   `extract-schema` : `schema-pattern`と`table-pattern`に一致するシャード スキーマの場合、DM は`schema-regexp`を使用してシャード スキーマ名を抽出し、 `test_`の部分を除いた名前サフィックスをマージされたテーブルの`target-column` 、つまり`c_schema`列に書き込みます。
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

アップストリームのシャードテーブルのソース情報をダウンストリームのマージテーブルに抽出するには、**移行を開始する前に、ダウンストリームにマージテーブルを手動で作成する必要があります**。マージされたテーブルには、ソース情報を指定するために使用される 3 つの`target-columns` ( `c_table` 、 `c_schema` 、および`c_source` ) が含まれている必要があります。さらに、これらの列は**最後の列であり、<a href="/data-type-string.md">文字列型</a>である必要があります**。

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

> **注記：**
>
> 次のいずれかのエラーが発生した場合、シャードされたテーブルおよびスキーマのソース情報がマージされたテーブルに書き込まれない可能性があります。

-   最後の 3 列には`c-table`ありません。

```sql
CREATE TABLE `test`.`t` (
    c_table varchar(10) DEFAULT NULL,
    a int(11) PRIMARY KEY,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

-   `c-source`が存在しない場合:

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
);
```

-   `c_schema`は文字列型ではありません。

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema int(11) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL,
);
```

### シャード化されたスキーマをマージする {#merge-sharded-schemas}

シャード化スキーマのシナリオでは、 `test_{1,2,3...}`を移行するとします。 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`テーブルを`test`にします。ダウンストリーム TiDB インスタンスに`t_{1,2,3...}`テーブル。

上流のスキーマを下流に移行するには、 `test`手順に従います。 `t_[1,2,3]` 、作成する必要があるのはルーティング ルールを 1 つだけです。

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

### 不正なテーブルルーティング {#incorrect-table-routing}

次の 2 つ`test_1_bak`ルーティング ルールが設定されていると仮定します。 `t_1_bak` `rule-1`と`rule-2`の両方に一致します。テーブル ルーティング構成が数の制限に違反しているため、エラーが報告されます。

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
