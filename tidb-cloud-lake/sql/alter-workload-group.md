---
title: ALTER WORKLOAD GROUP
summary: 指定したクォータ設定でワークロードグループを更新します。
---

# ALTER WORKLOAD GROUP

指定したクォータ設定でワークロードグループを更新します。

## 構文 {#syntax}

```sql
ALTER WORKLOAD GROUP <group_name>
[SET cpu_quota = '<percentage>', query_timeout = '<duration>']
```

## パラメータ {#parameters}

| パラメータ | 型 | 必須 | デフォルト | 説明 |
|------------------------|----------|----------|--------------|-----------------------------------------------------------------------------|
| `cpu_quota`            | string   | いいえ       | (unlimited)  | パーセンテージ文字列で指定する CPU リソースクォータ（例: `"20%"`）                      |
| `query_timeout`        | duration | いいえ       | (unlimited)  | クエリタイムアウト時間（単位: `s`/`sec`=秒、`m`/`min`=分、`h`/`hour`=時間、`d`/`day`=日、`ms`=ミリ秒、単位なし=秒） |
| `memory_quota`         | string or integer   | いいえ       | (unlimited)  | ワークロードグループの最大メモリ使用量制限（パーセンテージまたは絶対値） |
| `max_concurrency`      | integer  | いいえ       | (unlimited)  | ワークロードグループの最大同時実行数                               |
| `query_queued_timeout` | duration | いいえ       | (unlimited)  | ワークロードグループが最大同時実行数を超えた場合の最大キュー待機時間（単位: `s`/`sec`=秒、`m`/`min`=分、`h`/`hour`=時間、`d`/`day`=日、`ms`=ミリ秒、単位なし=秒）      |

## 例 {#examples}

```sql
ALTER WORKLOAD GROUP analytics SET cpu_quota = '20%', query_timeout = '10m';
```