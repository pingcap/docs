---
title: Filter DML Events Using SQL Expressions
summary: Learn how to filter DML events using SQL expressions.
---

# SQL式を使用してDMLイベントをフィルタリングする {#filter-dml-events-using-sql-expressions}

このドキュメントでは、DMを使用して継続的な増分データレプリケーションを実行するときに、SQL式を使用してbinlogイベントをフィルタリングする方法を紹介します。詳細なレプリケーション手順については、次のドキュメントを参照してください。

-   [小さなデータセットのMySQLをTiDBに移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットのMySQLをTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模なデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

インクリメンタルデータレプリケーションを実行する場合、 [Binlogイベントフィルター](/filter-binlog-event.md)を使用して特定のタイプのbinlogイベントをフィルタリングできます。たとえば、アーカイブや監査などの目的で、 `DELETE`のイベントをダウンストリームに複製しないことを選択できます。ただし、 Binlog Event Filterは、より細かい粒度が必要な行の`DELETE`イベントをフィルタリングするかどうかを決定できません。

この問題に対処するために、v2.0.5以降、DMは増分データレプリケーションで`binlog value filter`を使用してデータをフィルタリングすることをサポートしています。 DMでサポートされている`ROW`形式のbinlogの中で、binlogイベントはすべての列の値を伝達し、これらの値に基づいてSQL式を構成できます。式が行の変更を`TRUE`として計算する場合、DMはこの行の変更をダウンストリームに複製しません。

[Binlogイベントフィルター](/filter-binlog-event.md)と同様に、タスク構成ファイルで`binlog value filter`を構成する必要があります。詳細については、次の構成例を参照してください。高度なタスク構成と説明については、 [DM高度なタスク構成ファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を参照してください。

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

上記の構成例では、 `even_c`ルールが構成され、データソース`mysql-replica-01`によって参照されます。このルールによれば、 `expr_filter`スキーマの`tb1`テーブルの場合、偶数が`c`列（ `c % 2 = 0` ）に挿入されると、この`insert`ステートメントはダウンストリームに複製されません。次の例は、このルールの効果を示しています。

次のデータをアップストリームデータソースに段階的に挿入します。

```sql
INSERT INTO tbl(id, c) VALUES (1, 1), (2, 2), (3, 3), (4, 4);
```

次に、ダウンストリームの`tb1`のテーブルをクエリします。 `c`の奇数の行のみが複製されていることがわかります。

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

## Configuration / コンフィグレーションパラメーターと説明 {#configuration-parameters-and-description}

-   `schema` ：一致するアップストリームスキーマの名前。ワイルドカードマッチングまたは通常のマッチングはサポートされていません。
-   `table` ：照合するアップストリームテーブルの名前。ワイルドカードマッチングまたは通常のマッチングはサポートされていません。
-   `insert-value-expr` ： `INSERT`のタイプのbinlogイベント（WRITE_ROWS_EVENT）によって運ばれる値に影響を与える式を構成します。この式を同じ構成`delete-value-expr`で`update-old-value-expr` 、または`update-new-value-expr`と一緒に使用することはできません。
-   `update-old-value-expr` ： `UPDATE`のタイプのbinlogイベント（UPDATE_ROWS_EVENT）によって運ばれる古い値に影響を与える式を構成します。この式を同じ構成アイテムで`insert-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `update-new-value-expr` ： `UPDATE`のタイプのbinlogイベント（UPDATE_ROWS_EVENT）によって運ばれる新しい値に影響を与える式を構成します。この式を同じ構成アイテムで`insert-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `delete-value-expr` ： `DELETE`のタイプのbinlogイベント（DELETE_ROWS_EVENT）によって運ばれる値に影響を与える式を構成します。この式を`insert-value-expr` 、または`update-old-value-expr`と一緒に使用することはできませ`update-new-value-expr` 。

> **ノート：**
>
> -   `update-old-value-expr`と`update-new-value-expr`を一緒に構成できます。
> -   `update-old-value-expr`と`update-new-value-expr`が一緒に構成されている場合、「更新+古い値」が`update-old-value-expr`**に**一致し、「更新+新しい値」が`update-new-value-expr`に一致する行がフィルター処理されます。
> -   `update-old-value-expr`と`update-new-value-expr`のいずれかが構成されている場合、構成された式は**、行の変更全体**をフィルター処理するかどうかを決定します。つまり、古い値の削除と新しい値の挿入が全体としてフィルター処理されます。

SQL式は、1つの列または複数の列で使用できます。 `c % 2 = 0`などの`a*a + b*b = c*c`でサポートされているSQL関数を使用することもでき`ts > NOW()` 。

`TIMESTAMP`のデフォルトのタイムゾーンは、タスク構成ファイルで指定されたタイムゾーンです。デフォルト値は、ダウンストリームのタイムゾーンです。 `c_timestamp = '2021-01-01 12:34:56.5678+08:00'`のようにタイムゾーンを明示的に指定できます。

`expression-filter`の構成項目で複数のフィルタリングルールを構成できます。アップストリームデータソースは、 `expression-filters`の必要なルールを参照して、それを有効にします。複数のルールが使用されている場合、**いずれ**かのルールが一致すると、行の変更全体がフィルタリングされます。

> **ノート：**
>
> 構成する式フィルタリングルールが多すぎると、DMの計算オーバーヘッドが増加し、データレプリケーションが遅くなります。
