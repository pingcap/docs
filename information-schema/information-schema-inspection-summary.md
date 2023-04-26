---
title: INSPECTION_SUMMARY
summary: Learn the `INSPECTION_SUMMARY` inspection summary table.
---

# INSPECTION_SUMMARY {#inspection-summary}

シナリオによっては、特定のリンクまたはモジュールの監視の概要だけに注意を払う必要がある場合があります。たとえば、スレッドプール内のコプロセッサーのスレッド数を 8 に設定すると、コプロセッサーの CPU 使用率が 750% に達した場合、リスクが存在し、コプロセッサーがボトルネックになる可能性があると事前に判断できます。ただし、一部の監視メトリックはユーザーのワークロードによって大きく異なるため、特定のしきい値を定義することは困難です。このシナリオでは問題のトラブルシューティングを行うことが重要であるため、TiDB はリンク サマリー用に`inspection_summary`表を提供します。

`information_schema.inspection_summary`検査集計表の構造は次のとおりです。

{{< copyable "" >}}

```sql
USE information_schema;
DESC inspection_summary;
```

```sql
+--------------+--------------+------+------+---------+-------+
| Field        | Type         | Null | Key  | Default | Extra |
+--------------+--------------+------+------+---------+-------+
| RULE         | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE     | varchar(64)  | YES  |      | NULL    |       |
| METRICS_NAME | varchar(64)  | YES  |      | NULL    |       |
| LABEL        | varchar(64)  | YES  |      | NULL    |       |
| QUANTILE     | double       | YES  |      | NULL    |       |
| AVG_VALUE    | double(22,6) | YES  |      | NULL    |       |
| MIN_VALUE    | double(22,6) | YES  |      | NULL    |       |
| MAX_VALUE    | double(22,6) | YES  |      | NULL    |       |
| COMMENT      | varchar(256) | YES  |      | NULL    |       |
+--------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

フィールドの説明:

-   `RULE` : 要約ルール。新しいルールは継続的に追加されているため、 `select * from inspection_rules where type='summary'`ステートメントを実行して最新のルール リストを照会できます。
-   `INSTANCE` : 監視対象インスタンス。
-   `METRICS_NAME` : モニタリング メトリック名。
-   `QUANTILE` : `QUANTILE`を含む監視テーブルに有効です。述語を押し下げて、複数のパーセンタイルを指定できます。たとえば、 `select * from inspection_summary where rule='ddl' and quantile in (0.80, 0.90, 0.99, 0.999)`実行して DDL 関連のモニタリング メトリックを要約し、P80/P90/P99/P999 の結果を照会できます。 `AVG_VALUE` `MIN_VALUE`それぞれ集計`MAX_VALUE`平均値、最小値、最大値を示す。
-   `COMMENT` : 対応するモニタリング メトリックに関するコメント。

> **ノート：**
>
> すべての結果を集計するとオーバーヘッドが発生するため、SQL 述語に特定の`rule`を表示してオーバーヘッドを削減することをお勧めします。たとえば、 `select * from inspection_summary where rule in ('read-link', 'ddl')`を実行すると、読み取りリンクと DDL 関連のモニタリング メトリックが要約されます。

使用例:

診断結果表、診断監視集計表ともに、診断時間範囲を`hint`で指定できます。 `select /*+ time_range('2020-03-07 12:00:00','2020-03-07 13:00:00') */* from inspection_summary`は`2020-03-07 12:00:00` ～ `2020-03-07 13:00:00`期のモニタリングまとめです。モニタリング集計表と同様に、2 つの異なる期間のデータを比較`inspection_summary`ことで、差異の大きいモニタリング項目をすばやく見つけることができます。

次の例では、2 つの期間における読み取りリンクのモニタリング メトリックを比較します。

-   `(2020-01-16 16:00:54.933, 2020-01-16 16:10:54.933)`
-   `(2020-01-16 16:10:54.933, 2020-01-16 16:20:54.933)`

{{< copyable "" >}}

```sql
SELECT
  t1.avg_value / t2.avg_value AS ratio,
  t1.*,
  t2.*
FROM
  (
    SELECT
      /*+ time_range("2020-01-16 16:00:54.933", "2020-01-16 16:10:54.933")*/ *
    FROM information_schema.inspection_summary WHERE rule='read-link'
  ) t1
  JOIN
  (
    SELECT
      /*+ time_range("2020-01-16 16:10:54.933", "2020-01-16 16:20:54.933")*/ *
    FROM information_schema.inspection_summary WHERE rule='read-link'
  ) t2
  ON t1.metrics_name = t2.metrics_name
  and t1.instance = t2.instance
  and t1.label = t2.label
ORDER BY
  ratio DESC;
```
