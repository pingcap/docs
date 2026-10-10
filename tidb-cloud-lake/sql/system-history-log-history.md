---
title: system_history.log_history
summary: Note このテーブルには、他の特化した履歴テーブルに取り込まれる生のログデータが含まれます。その他のテーブルは、このデータの構造化されたクエリ固有のビューを提供します。
---

# system_history.log_history

**システム操作の監査証跡** - すべての {{{ .lake }}} ノードおよびコンポーネントからの生ログリポジトリ。運用インテリジェンスの基盤:

- **システム監視**: システムの健全性、パフォーマンス、リソース使用状況を追跡します
- **トラブルシューティング**: 詳細なエラーログとシステムイベントを使用して問題をデバッグします
- **運用分析**: システム動作のパターンと傾向を分析します
- **根本原因分析**: システム障害とパフォーマンスのボトルネックを調査します

> **Note:** このテーブルには、他の特化した履歴テーブルに取り込まれる生のログデータが含まれます。その他のテーブルは、このデータの構造化されたクエリ固有のビューを提供します。

## フィールド {#fields}

| フィールド        | 型      | 説明                                      |
|--------------|-----------|--------------------------------------------------|
| timestamp    | TIMESTAMP | ログエントリが記録されたタイムスタンプ           |
| path         | VARCHAR   | ログのソースファイルパスと行番号                 |
| target       | VARCHAR   | ログの対象モジュールまたはコンポーネント         |
| log_level    | VARCHAR   | ログレベル（例: `INFO`, `ERROR`）                |
| cluster_id   | VARCHAR   | クラスターの識別子                               |
| node_id      | VARCHAR   | ノードの識別子                                   |
| warehouse_id | VARCHAR   | Warehouse の識別子                               |
| query_id     | VARCHAR   | ログに関連付けられたクエリ ID                    |
| message      | VARCHAR   | ログメッセージの内容                             |
| fields       | VARIANT   | 追加フィールド（JSON オブジェクトとして格納）    |
| batch_number | BIGINT    | 内部使用向けであり、特別な意味はありません       |

Note: `message` フィールドにはプレーンテキストのログが格納され、`fields` フィールドには JSON 形式のログが格納されます。

たとえば、あるログエントリの `fields` フィールドは次のようになります。

```
fields: {"node_id":"8R5ZMF8q0HHE6x9H7U1gr4","query_id":"72d2319a-b6d6-4b1d-8694-670137a40d87","session_id":"189fd3e2-e6ac-48c3-97ef-73094c141312","sql":"select * from system_history.log_history"}
```

別のログエントリの `message` フィールドは、次のように表示される場合があります。

```
message: [HTTP-QUERY] Preparing to plan SQL query
```