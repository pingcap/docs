---
title: INSPECTION_SUMMARY
summary: INSPECTION_SUMMARY` 検査概要テーブルについて説明します。
---

# 検査概要 {#inspection-summary}

シナリオによっては、特定のリンクまたはモジュールの監視サマリーのみに注目する必要がある場合もあります。例えば、スレッドプール内のコプロセッサーのスレッド数が8に設定されている場合、コプロセッサーのCPU使用率が750%に達した場合、リスクが存在し、コプロセッサーがボトルネックになる可能性があることを事前に判断できます。しかし、監視メトリックによっては、ユーザーのワークロードの違いによって大きく変化するため、具体的なしきい値を定義することは困難です。このようなシナリオでは、問題のトラブルシューティングが重要であるため、TiDBはリンクサマリー用のテーブルを`inspection_summary`提供しています。

> **注記：**
>
> このテーブルは TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

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

-   `RULE` : 要約ルール。新しいルールは継続的に追加されるため、 `select * from inspection_rules where type='summary'`ステートメントを実行すると最新のルールリストを照会できます。
-   `INSTANCE` : 監視対象インスタンス。
-   `METRICS_NAME` : 監視メトリック名。
-   `QUANTILE` : `QUANTILE`含む監視テーブルに有効です。述語をプッシュダウンすることで、複数のパーセンタイルを指定できます。例えば、 `select * from inspection_summary where rule='ddl' and quantile in (0.80, 0.90, 0.99, 0.999)`実行してDDL関連の監視メトリックを要約し、P80/P90/P99/P999の結果を照会できます。6 、 `MIN_VALUE` 、 `MAX_VALUE` `AVG_VALUE` 、集計の平均値、最小値、最大値を示します。
-   `COMMENT` : 対応する監視メトリックに関するコメント。

> **注記：**
>
> すべての結果を要約するとオーバーヘッドが発生するため、SQL述語で特定の`rule`表示してオーバーヘッドを削減することをお勧めします。例えば、 `select * from inspection_summary where rule in ('read-link', 'ddl')`実行すると、読み取りリンクとDDL関連の監視メトリックが要約されます。

使用例:

診断結果表と診断監視サマリー表はどちらも、 `hint`を使用して診断時間範囲を指定できます。3 `select /*+ time_range('2020-03-07 12:00:00','2020-03-07 13:00:00') */* from inspection_summary` 、 `2020-03-07 12:00:00` ～ `2020-03-07 13:00:00`期間の監視サマリーです。監視サマリー表と同様に、 `inspection_summary`表を使用すると、異なる2期間のデータを比較することで、差異の大きい監視項目を素早く見つけることができます。

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
