---
title: Filter DML Events Using SQL Expressions
summary: Learn how to filter DML events using SQL expressions.
---

# SQL 式を使用した DML イベントのフィルタリング {#filter-dml-events-using-sql-expressions}

このドキュメントでは、DM を使用して継続的な増分データ レプリケーションを実行するときに、SQL 式を使用してbinlogイベントをフィルター処理する方法を紹介します。詳細なレプリケーション手順については、次のドキュメントを参照してください。

-   [小さなデータセットの MySQL を TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットの MySQL を TiDB に移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

増分データ レプリケーションを実行する場合、 [Binlogイベント フィルター](/filter-binlog-event.md)を使用して特定の種類のbinlogイベントをフィルター処理できます。たとえば、アーカイブや監査などの目的で、 `DELETE`イベントをダウンストリームに複製しないことを選択できます。ただし、 Binlog Event Filter は、より細かい粒度が必要な行の`DELETE`イベントをフィルタリングするかどうかを判断できません。

この問題に対処するために、v2.0.5 以降、DM は増分データ レプリケーションで`binlog value filter`を使用してデータをフィルタリングすることをサポートしています。 DM がサポートする`ROW`形式のbinlogの中で、 binlogイベントはすべての列の値を保持し、これらの値に基づいて SQL 式を構成できます。式が行の変更を`TRUE`と計算する場合、DM はこの行の変更を下流にレプリケートしません。

[Binlogイベント フィルタ](/filter-binlog-event.md)と同様に、タスク構成ファイルで`binlog value filter`を構成する必要があります。詳細については、次の構成例を参照してください。高度なタスクの設定と説明については、 [DM 高度なタスク構成ファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を参照してください。

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

上記の構成例では、 `even_c`ルールが構成され、データソース`mysql-replica-01`によって参照されます。この規則に従って、 `expr_filter`スキーマの`tb1`テーブルでは、 `c`列に偶数が挿入された場合 ( `c % 2 = 0` )、この`insert`ステートメントは下流に複製されません。次の例は、このルールの効果を示しています。

アップストリーム データ ソースに次のデータを段階的に挿入します。

```sql
INSERT INTO tbl(id, c) VALUES (1, 1), (2, 2), (3, 3), (4, 4);
```

次に、ダウンストリームで`tb1`テーブルをクエリします。 `c`の奇数の行だけが複製されていることがわかります。

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

-   `schema` : 一致するアップストリーム スキーマの名前。ワイルドカード マッチングまたは通常のマッチングはサポートされていません。
-   `table` : 照合するアップストリーム テーブルの名前。ワイルドカード マッチングまたは通常のマッチングはサポートされていません。
-   `insert-value-expr` : `INSERT`種類のbinlogイベント (WRITE_ROWS_EVENT) によって運ばれる値に有効な式を構成します。この式を同じ構成アイテムで`update-old-value-expr` 、 `update-new-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `update-old-value-expr` : `UPDATE`のタイプのbinlogイベント (UPDATE_ROWS_EVENT) によって運ばれる古い値に有効な式を構成します。この式は、同じ構成アイテム内で`insert-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `update-new-value-expr` : `UPDATE`種類のbinlogイベント (UPDATE_ROWS_EVENT) によって運ばれる新しい値に有効な式を構成します。この式は、同じ構成アイテム内で`insert-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `delete-value-expr` : `DELETE`種類のbinlogイベント (DELETE_ROWS_EVENT) によって運ばれる値に有効な式を構成します。この式を`insert-value-expr` 、 `update-old-value-expr`または`update-new-value-expr`と一緒に使用することはできません。

> **ノート：**
>
> -   `update-old-value-expr`と`update-new-value-expr`一緒に設定できます。
> -   `update-old-value-expr`と`update-new-value-expr`を一緒に構成すると、「更新 + 古い値」が`update-old-value-expr`満たす行**と、** 「更新 + 新しい値」が`update-new-value-expr`を満たす行がフィルター処理されます。
> -   `update-old-value-expr`と`update-new-value-expr`のいずれかが構成されている場合、構成された式によって**行変更全体**をフィルター処理するかどうかが決定されます。つまり、古い値の削除と新しい値の挿入が全体としてフィルター処理されます。

1 つの列または複数の列で SQL 式を使用できます。 `c % 2 = 0` 、 `a*a + b*b = c*c` 、 `ts > NOW()`など、TiDB でサポートされている SQL関数を使用することもできます。

`TIMESTAMP`のデフォルトのタイム ゾーンは、タスク構成ファイルで指定されたタイム ゾーンです。デフォルト値は、ダウンストリームのタイム ゾーンです。 `c_timestamp = '2021-01-01 12:34:56.5678+08:00'`のような方法でタイムゾーンを明示的に指定できます。

`expression-filter`の設定項目で複数のフィルタリング ルールを設定できます。アップストリーム データ ソースは、 `expression-filters`で必要なルールを参照して有効にします。複数のルールが使用されている場合、**いずれ**かのルールが一致すると、行の変更全体がフィルター処理されます。

> **ノート：**
>
> 構成する式フィルタリング ルールが多すぎると、DM の計算オーバーヘッドが増加し、データ レプリケーションが遅くなります。
