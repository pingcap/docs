---
title: INSPECTION_SUMMARY
summary: Learn the `INSPECTION_SUMMARY` inspection summary table.
---

# 検査_概要 {#inspection-summary}

シナリオによっては、特定のリンクまたはモジュールの監視概要のみに注意を払う必要がある場合があります。たとえば、スレッド プール内のコプロセッサーのスレッド数は 8 に設定されます。コプロセッサーの CPU 使用率が 750% に達した場合、リスクが存在し、コプロセッサーがボトルネックになる可能性があると事前に判断できます。ただし、一部の監視メトリクスはユーザーのワークロードの違いにより大きく異なるため、特定のしきい値を定義するのは困難です。このシナリオでは問題のトラブルシューティングが重要であるため、TiDB はリンクの概要用の`inspection_summary`表を提供します。

> **注記：**
>
> このテーブルは TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

`information_schema.inspection_summary`検査集計表の構成は以下のとおりです。

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

-   `RULE` : 要約ルール。新しいルールは継続的に追加されるため、 `select * from inspection_rules where type='summary'`ステートメントを実行して最新のルール リストをクエリできます。
-   `INSTANCE` : 監視対象のインスタンス。
-   `METRICS_NAME` : 監視メトリクス名。
-   `QUANTILE` ： `QUANTILE`を含む監視テーブルに対して有効になります。述語をプッシュダウンすることで、複数のパーセンタイルを指定できます。たとえば、 `select * from inspection_summary where rule='ddl' and quantile in (0.80, 0.90, 0.99, 0.999)`を実行して DDL 関連の監視メトリックを要約し、P80/P90/P99/P999 の結果をクエリできます。 `AVG_VALUE` `MIN_VALUE`それぞれ集計`MAX_VALUE`平均値、最小値、最大値を示す。
-   `COMMENT` : 対応する監視メトリックに関するコメント。

> **注記：**
>
> すべての結果を要約するとオーバーヘッドが発生するため、SQL 述語に特定の`rule`を表示してオーバーヘッドを軽減することをお勧めします。たとえば、 `select * from inspection_summary where rule in ('read-link', 'ddl')`を実行すると、読み取りリンクと DDL 関連の監視メトリックが要約されます。

使用例：

診断結果テーブルと診断監視集計テーブルの両方で、 `hint`を使用して診断時間の範囲を指定できます。 `select /*+ time_range('2020-03-07 12:00:00','2020-03-07 13:00:00') */* from inspection_summary`は、 `2020-03-07 12:00:00`期から`2020-03-07 13:00:00`期までのモニタリングの概要でございます。 `inspection_summary`つの表は、監視集計表と同様に、異なる期間のデータを比較することで、差異が大きい監視項目を素早く見つけることができます。

次の例では、2 つの期間における読み取りリンクのモニタリング メトリックを比較します。

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
