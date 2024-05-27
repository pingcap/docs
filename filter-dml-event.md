---
title: Filter DML Events Using SQL Expressions
summary: SQL 式を使用して DML イベントをフィルター処理する方法を学習します。
---

# SQL 式を使用して DML イベントをフィルタリングする {#filter-dml-events-using-sql-expressions}

このドキュメントでは、DM を使用して継続的な増分データ レプリケーションを実行するときに、SQL 式を使用してbinlogイベントをフィルター処理する方法を紹介します。詳細なレプリケーション手順については、次のドキュメントを参照してください。

-   [小規模データセットを MySQL から TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模データセットの MySQL シャードを TiDB に移行してマージする](/migrate-large-mysql-shards-to-tidb.md)

増分データ レプリケーションを実行する場合、 [Binlogイベントフィルター](/filter-binlog-event.md)使用して特定の種類のbinlogイベントをフィルターできます。たとえば、アーカイブや監査などの目的で、 `DELETE`イベントをダウンストリームにレプリケートしないように選択できます。ただし、 Binlogイベント フィルターでは、より細かい粒度が必要な行の`DELETE`のイベントをフィルターするかどうかを判断できません。

この問題に対処するため、バージョン 2.0.5 以降、DM は増分データ レプリケーションで`binlog value filter`使用してデータをフィルター処理することをサポートしています。DM がサポートする`ROW`形式のbinlogのうち、 binlogイベントはすべての列の値を保持し、これらの値に基づいて SQL 式を構成できます。式が行の変更を`TRUE`として計算した場合、DM はこの行の変更をダウンストリームに複製しません。

[Binlogイベントフィルター](/filter-binlog-event.md)と同様に、タスク設定ファイルで`binlog value filter`設定する必要があります。詳細については、次の設定例を参照してください。高度なタスク設定と説明については、 [DM 高度なタスク構成ファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を参照してください。

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

上記の設定例では、 `even_c`ルールが設定され、データ ソース`mysql-replica-01`によって参照されています。このルールによれば、 `expr_filter`スキーマの`tb1`テーブルで、 `c`列 ( `c % 2 = 0` ) に偶数が挿入されると、この`insert`ステートメントは下流に複製されません。次の例は、このルールの効果を示しています。

次のデータをアップストリーム データ ソースに増分的に挿入します。

```sql
INSERT INTO tbl(id, c) VALUES (1, 1), (2, 2), (3, 3), (4, 4);
```

次に、ダウンストリームの`tb1`テーブルをクエリします。3 `c`奇数行のみがレプリケートされていることがわかります。

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

-   `schema` : 一致するアップストリーム スキーマの名前。ワイルドカード一致または通常の一致はサポートされていません。
-   `table` : 一致させるアップストリーム テーブルの名前。ワイルドカード一致または通常の一致はサポートされていません。
-   `insert-value-expr` : `INSERT`種類のbinlogイベント (WRITE_ROWS_EVENT) によって運ばれる値に影響を及ぼす式を設定します。この式`update-new-value-expr`同じ設定項目内で`update-old-value-expr` 、または`delete-value-expr`と一緒に使用することはできません。
-   `update-old-value-expr` : `UPDATE`種類のbinlogイベント (UPDATE_ROWS_EVENT) によって保持される古い値に有効になる式を構成します。この式を同じ構成項目で`insert-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `update-new-value-expr` : `UPDATE`種類のbinlogイベント (UPDATE_ROWS_EVENT) によって伝達される新しい値に有効になる式を構成します。この式を同じ構成項目で`insert-value-expr`または`delete-value-expr`と一緒に使用することはできません。
-   `delete-value-expr` : `DELETE`種類のbinlogイベント (DELETE_ROWS_EVENT) によって伝達される値に影響を及ぼす式を設定します。この式は`insert-value-expr` 、 `update-old-value-expr` 、または`update-new-value-expr`と一緒に使用することはできません。

> **注記：**
>
> -   `update-old-value-expr`と`update-new-value-expr`一緒に設定できます。
> -   `update-old-value-expr`と`update-new-value-expr`が一緒に構成されている場合、「更新 + 古い値」が`update-old-value-expr`に一致し**、** 「更新 + 新しい値」が`update-new-value-expr`に一致する行がフィルタリングされます。
> -   `update-old-value-expr`と`update-new-value-expr`のいずれかが設定されている場合、設定された式によって**行の変更全体**をフィルタリングするかどうかが決定されます。つまり、古い値の削除と新しい値の挿入が全体としてフィルタリングされます。

SQL 式は 1 つの列または複数の列で使用できます。また、 `c % 2 = 0` 、 `a*a + b*b = c*c` 、 `ts > NOW()`など、TiDB でサポートされている SQL関数を使用することもできます。

`TIMESTAMP`デフォルトのタイムゾーンは、タスク構成ファイルで指定されたタイムゾーンです。デフォルト値はダウンストリームのタイムゾーンです。 `c_timestamp = '2021-01-01 12:34:56.5678+08:00'`のような方法でタイムゾーンを明示的に指定できます。

`expression-filter`構成項目の下に複数のフィルタリング ルールを設定できます。上流データ ソースは、 `expression-filters`の必要なルールを参照して有効にします。複数のルールを使用する場合、**いずれか**のルールが一致すると、行の変更全体がフィルタリングされます。

> **注記：**
>
> 式フィルタリング ルールを多すぎる数に設定すると、DM の計算オーバーヘッドが増加し、データのレプリケーションが遅くなります。
