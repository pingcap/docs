---
title: Filter DML Events Using SQL Expressions
summary: SQL 式を使用して DML イベントをフィルター処理する方法を学習します。
---

# SQL 式を使用して DML イベントをフィルタリングする {#filter-dml-events-using-sql-expressions}

このドキュメントでは、DMを使用して継続的な増分データレプリケーションを実行する際に、SQL式を使用してbinlogイベントをフィルタリングする方法を紹介します。レプリケーションの詳細な手順については、以下のドキュメントを参照してください。

-   [小規模データセットをMySQLからTiDBに移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模データセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模データセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

増分データレプリケーションを実行する際に、 [Binlogイベントフィルター](/filter-binlog-event.md)使用して特定の種類のbinlogイベントをフィルタリングできます。例えば、アーカイブや監査などの目的で、 `DELETE`イベントを下流に複製しないように選択できます。ただし、 Binlogイベントフィルタは、より細かい粒度が求められる行の`DELETE`のイベントをフィルタリングするかどうかを判断できません。

この問題に対処するため、DM v2.0.5以降では、増分データレプリケーションにおいて`binlog value filter`使用したデータのフィルタリングをサポートしています。DM対応の`ROW`形式のbinlogでは、binlogイベントはすべての列の値を保持しており、これらの値に基づいてSQL式を設定できます。式で行の変更が`TRUE`と計算された場合、DMはこの行の変更を下流に複製しません。

[Binlogイベントフィルター](/filter-binlog-event.md)と同様に、タスク設定ファイルで`binlog value filter`設定する必要があります。詳細については、以下の設定例を参照してください。詳細なタスク設定と説明については、 [DM 高度なタスク構成ファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を参照してください。

```yaml
name: test
task-mode: all

mysql-instances:
  - source-id: "mysql-replica-01"
    expression-filters: ["even_c"]

expression-filter:
  even_c:
    schema: "expr_filter"
    table: "tbl"
    insert-value-expr: "c % 2 = 0"
```

上記の設定例では、ルール`even_c`が設定され、データソース`mysql-replica-01`によって参照されています。このルールによれば、スキーマ`expr_filter`のテーブル`tb1`において、列`c` （ `c % 2 = 0` ）に偶数が挿入された場合、この文`insert`は下流に複製されません。次の例は、このルールの効果を示しています。

次のデータをアップストリーム データ ソースに増分挿入します。

```sql
INSERT INTO tbl(id, c) VALUES (1, 1), (2, 2), (3, 3), (4, 4);
```

次に、下流のテーブル`tb1`に対してクエリを実行します。3 `c`奇数行のみがレプリケートされていることがわかります。

```sql
MySQL [test]> select * from tbl;
+------+------+
| id   | c    |
+------+------+
|    1 |    1 |
|    3 |    3 |
+------+------+
2 rows in set (0.001 sec)
```

## コンフィグレーションパラメータと説明 {#configuration-parameters-and-description}

-   `schema` : 一致させる上流スキーマの名前。ワイルドカード一致や通常の一致はサポートされていません。
-   `table` : 照合するアップストリームテーブルの名前。ワイルドカードによる照合や通常の照合はサポートされていません。
-   `insert-value-expr` : `INSERT`種類のbinlogイベント (WRITE_ROWS_EVENT) によって伝達される値に適用される式を設定します。この式は、同じ設定項目内で`update-old-value-expr` 、 `update-new-value-expr` 、または`delete-value-expr`と同時に使用することはできません。
-   `update-old-value-expr` : `UPDATE`種類のbinlogイベント（UPDATE_ROWS_EVENT）によって保持される古い値に適用される式を設定します。この式は、同じ設定項目内で`insert-value-expr`または`delete-value-expr`と同時に使用することはできません。
-   `update-new-value-expr` : `UPDATE`種類のbinlogイベント（UPDATE_ROWS_EVENT）によって送信される新しい値に適用される式を設定します。この式は、同じ設定項目内で`insert-value-expr`または`delete-value-expr`と同時に使用することはできません。
-   `delete-value-expr` : `DELETE`種類のbinlogイベント (DELETE_ROWS_EVENT) によって伝達される値に適用される式を設定します。この式は`insert-value-expr` 、 `update-old-value-expr` 、または`update-new-value-expr`と同時に使用することはできません。

> **注記：**
>
> -   `update-old-value-expr`と`update-new-value-expr`一緒に設定できます。
> -   `update-old-value-expr`と`update-new-value-expr`一緒に設定されている場合、「更新 + 古い値」が`update-old-value-expr`一致し**、** 「更新 + 新しい値」が`update-new-value-expr`一致する行がフィルタリングされます。
> -   `update-old-value-expr`と`update-new-value-expr`のいずれかが設定されている場合、設定された式によって**行の変更全体**をフィルタリングするかどうかが決定されます。つまり、古い値の削除と新しい値の挿入が全体としてフィルタリングされます。

SQL式は1つの列でも複数の列でも使用できます。また、TiDBでサポートされているSQL関数（ `c % 2 = 0` 、 `a*a + b*b = c*c` 、 `ts > NOW()`など）も使用できます。

`TIMESTAMP`デフォルトタイムゾーンは、タスク設定ファイルで指定されたタイムゾーンです。デフォルト値はダウンストリームのタイムゾーンです。3 `c_timestamp = '2021-01-01 12:34:56.5678+08:00'`ように明示的にタイムゾーンを指定することもできます。

`expression-filter`設定項目で複数のフィルタリングルールを設定できます。上流データソースは、 `expression-filters`の必要なルールを参照してルールを有効にします。複数のルールを使用する場合、**いずれ**かのルールに一致すると、行の変更全体がフィルタリングされます。

> **注記：**
>
> 式フィルタリング ルールを多く設定しすぎると、DM の計算オーバーヘッドが増加し、データ複製が遅くなります。
