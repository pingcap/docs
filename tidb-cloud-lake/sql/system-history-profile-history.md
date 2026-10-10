---
title: system_history.profile_history
summary: profiles フィールドを使用して、特定の情報を抽出できます。たとえば、すべての物理プランの OutputRows 値を取得するには、次のクエリを使用できます sql SELECT jq('[.[] | {id, output_rows.statistics[4]}]', profiles) AS result FROM system_history.profile_history LIMIT 1;.
---

# system_history.profile_history

**クエリパフォーマンスの詳細分析** - すべての SQL クエリに対する詳細な実行プロファイルと統計情報。主な用途は次のとおりです。

- **パフォーマンス最適化**: ボトルネックを特定し、低速なクエリを最適化します
- **リソース計画**: メモリ、CPU、I/O の使用パターンを把握します
- **実行分析**: クエリプランと実行統計を分析します
- **キャパシティ管理**: 時系列でリソース消費の傾向を監視します

## フィールド {#fields}

| フィールド | 型      | 説明                                                                 |
|-----------------|-----------|-----------------------------------------------------------------------------|
| timestamp       | TIMESTAMP | プロファイルが記録されたタイムスタンプ                                 |
| query_id        | VARCHAR   | このプロファイルに関連付けられたクエリの ID                            |
| profiles        | VARIANT   | 詳細な実行プロファイル情報を含む JSON オブジェクト             |
| statistics_desc | VARIANT   | 統計情報の形式を説明する JSON オブジェクト                                  |

## 例 {#examples}

`profiles` フィールドを使用して、特定の情報を抽出できます。たとえば、すべての物理プランの `OutputRows` 値を取得するには、次のクエリを使用できます。

```sql
SELECT jq('[.[] | {id, output_rows: .statistics[4]}]', profiles ) AS result FROM system_history.profile_history LIMIT 1;

*************************** 1. row ***************************
result: [{"id":0,"output_rows":1},{"id":3,"output_rows":8},{"id":1,"output_rows":1},{"id":2,"output_rows":1}]
```