---
title: Filter DML Events Using SQL Expressions
summary: Learn how to filter DML events using SQL expressions.
---

# SQL式を使用したDMLイベントのフィルタリング {#filter-dml-events-using-sql-expressions}

このドキュメントでは、DM を使用して継続的な増分データ レプリケーションを実行する場合に、SQL 式を使用してbinlogイベントをフィルタリングする方法を紹介します。レプリケーション手順の詳細については、次のドキュメントを参照してください。

-   [小規模なデータセットを MySQL から TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットを MySQL から TiDB に移行する](/migrate-large-mysql-to-tidb.md)
-   [小規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

増分データ レプリケーションを実行する場合、 [Binlogイベントフィルター](/filter-binlog-event.md)を使用して特定の種類のbinlogイベントをフィルターできます。たとえば、アーカイブや監査などの目的で`DELETE`イベントをダウンストリームにレプリケートしないことを選択できます。ただし、 Binlogイベント フィルターは、より細かい粒度が必要な行の`DELETE`のイベントをフィルターするかどうかを決定できません。

この問題に対処するために、DM は v2.0.5 以降、増分データ レプリケーションで`binlog value filter`を使用してデータをフィルタリングすることをサポートしています。 DM サポートおよび`ROW`形式のbinlogのうち、 binlogイベントはすべての列の値を保持し、これらの値に基づいて SQL 式を構成できます。式で行の変更が`TRUE`として計算される場合、DM はこの行の変更をダウンストリームにレプリケートしません。

[Binlogイベントフィルター](/filter-binlog-event.md)と同様に、タスク構成ファイルで`binlog value filter`を構成する必要があります。詳細については、以下の構成例を参照してください。高度なタスクの構成と説明については、 [DM 拡張タスク構成ファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を参照してください。

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

上記の構成例では、データソース`mysql-replica-01`からルール`even_c`が設定され参照されています。このルールに従って、スキーマ`expr_filter`のテーブル`tb1`場合、偶数が`c`列 ( `c % 2 = 0` ) に挿入されると、この`insert`ステートメントは下流に複製されません。次の例は、このルールの効果を示しています。

次のデータを上流のデータ ソースに増分挿入します。

```sql
INSERT INTO tbl(id, c) VALUES (1, 1), (2, 2), (3, 3), (4, 4);
```

次に、ダウンストリームの`tb1`テーブルをクエリします。 `c`の奇数の行のみが複製されていることがわかります。

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

-   `schema` : 照合する上流スキーマの名前。ワイルドカード一致または通常の一致はサポートされていません。
-   `table` : 照合する上流テーブルの名前。ワイルドカード一致または通常の一致はサポートされていません。
-   `insert-value-expr` : `INSERT`種類のbinlogイベント (WRITE_ROWS_EVENT) によって伝送される値に影響を与える式を構成します。この式を同じ構成アイテム内で`update-old-value-expr` 、 `update-new-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `update-old-value-expr` : `UPDATE`種類のbinlogイベント (UPDATE_ROWS_EVENT) によって伝えられる古い値に影響を与える式を構成します。この式を同じ構成アイテム内で`insert-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `update-new-value-expr` : `UPDATE`のタイプのbinlogイベント (UPDATE_ROWS_EVENT) によって伝えられる新しい値に影響を与える式を構成します。この式を同じ構成アイテム内で`insert-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `delete-value-expr` : `DELETE`種類のbinlogイベント (DELETE_ROWS_EVENT) によって伝送される値に影響を与える式を構成します。この式を`insert-value-expr` 、 `update-old-value-expr` 、または`update-new-value-expr`と一緒に使用することはできません。

> **注記：**
>
> -   `update-old-value-expr`と`update-new-value-expr`一緒に設定できます。
> -   `update-old-value-expr`と`update-new-value-expr`を同時に設定すると、「更新 + 古い値」が`update-old-value-expr`満たす行**と、** 「更新 + 新しい値」が`update-new-value-expr`を満たす行がフィルターされます。
> -   `update-old-value-expr`と`update-new-value-expr`のいずれかが設定されている場合、設定された式は**行の変更全体**をフィルタリングするかどうかを決定します。これは、古い値の削除と新しい値の挿入が全体としてフィルタリングされることを意味します。

SQL 式は 1 つの列または複数の列で使用できます。 TiDB でサポートされている SQL関数( `c % 2 = 0` 、 `a*a + b*b = c*c` 、 `ts > NOW()`など) を使用することもできます。

`TIMESTAMP`デフォルトのタイムゾーンは、タスク構成ファイルで指定されたタイムゾーンです。デフォルト値はダウンストリームのタイムゾーンです。 `c_timestamp = '2021-01-01 12:34:56.5678+08:00'`のような方法でタイムゾーンを明示的に指定できます。

`expression-filter`の設定項目の下に複数のフィルタリング ルールを設定できます。上流のデータ ソースは、 `expression-filters`で必要なルールを参照して有効にします。複数のルールが使用されている場合、**いずれ**かのルールが一致すると、行の変更全体がフィルタリングされます。

> **注記：**
>
> 構成する式フィルタリング ルールが多すぎると、DM の計算オーバーヘッドが増加し、データ レプリケーションの速度が低下します。
