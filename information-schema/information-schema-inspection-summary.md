---
title: INSPECTION_SUMMARY
summary: INSPECTION_SUMMARY 検査概要テーブルについて学習します。
---

# 検査概要 {#inspection-summary}

シナリオによっては、特定のリンクまたはモジュールの監視サマリーのみに注意を払う必要がある場合があります。たとえば、スレッド プール内のコプロセッサーのスレッド数は 8 に設定されています。コプロセッサーの CPU 使用率が 750% に達した場合、リスクが存在し、コプロセッサーがボトルネックになる可能性があることを事前に判断できます。ただし、一部の監視メトリックはユーザー ワークロードの違いにより大きく異なるため、特定のしきい値を定義することは困難です。このシナリオでは問題のトラブルシューティングが重要であるため、TiDB はリンク サマリーの`inspection_summary`テーブルを提供します。

> **注記：**
>
> この表は TiDB Self-Hosted にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

`information_schema.inspection_summary`検査概要表の構造は次のとおりです。

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

-   `RULE` : 要約ルール。新しいルールが継続的に追加されるため、 `select * from inspection_rules where type='summary'`ステートメントを実行して最新のルール リストを照会できます。
-   `INSTANCE` : 監視対象インスタンス。
-   `METRICS_NAME` : 監視メトリック名。
-   `QUANTILE` : `QUANTILE`を含む監視テーブルに有効です。述語をプッシュダウンすることで、複数のパーセンタイルを指定できます。たとえば、 `select * from inspection_summary where rule='ddl' and quantile in (0.80, 0.90, 0.99, 0.999)`を実行して DDL 関連の監視メトリックを要約し、P80/P90/P99/P999 の結果を照会できます。 `AVG_VALUE` 、 `MIN_VALUE` 、および`MAX_VALUE` 、それぞれ集計の平均値、最小値、および最大値を示します。
-   `COMMENT` : 対応する監視メトリックに関するコメント。

> **注記：**
>
> すべての結果を要約するとオーバーヘッドが発生するため、オーバーヘッドを削減するには、SQL 述語で特定の`rule`表示することをお勧めします。たとえば、 `select * from inspection_summary where rule in ('read-link', 'ddl')`を実行すると、読み取りリンクと DDL 関連の監視メトリックが要約されます。

使用例:

診断結果テーブルと診断監視サマリーテーブルはどちらも`hint`使用して診断時間範囲を指定できます。 `select /*+ time_range('2020-03-07 12:00:00','2020-03-07 13:00:00') */* from inspection_summary` `2020-03-07 12:00:00` ～ `2020-03-07 13:00:00`期間の監視サマリーです。 監視サマリーテーブルと同様に、 `inspection_summary`テーブルを使用すると、2 つの異なる期間のデータを比較して、差異の大きい監視項目をすばやく見つけることができます。

次の例では、2 つの期間における読み取りリンクの監視メトリックを比較します。

-   `(2020-01-16 16:00:54.933, 2020-01-16 16:10:54.933)`
-   `(2020-01-16 16:10:54.933, 2020-01-16 16:20:54.933)`

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
