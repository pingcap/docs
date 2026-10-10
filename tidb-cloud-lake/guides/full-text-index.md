---
title: Full-Text Index
summary: Full-text indexes (inverted indexes) は、用語をドキュメントに対応付けることで、大規模なドキュメントコレクション全体に対する超高速なテキスト検索を自動的に実現し、低速なテーブルスキャンを不要にします。
---

# Full-Text Index

> **Note:**
>
> 実践的な手順をお探しですか？[JSON & Search Guide](/tidb-cloud-lake/guides/json-search.md) を参照してください。

## Full-Text Index: 自動で実現する超高速テキスト検索 {#full-text-index-automatic-lightning-fast-text-search}

Full-text indexes（転置インデックス）は、用語をドキュメントに対応付けることで、大規模なドキュメントコレクション全体に対する超高速なテキスト検索を自動的に実現し、低速なテーブルスキャンを不要にします。

## どのような問題を解決するのか？ {#what-problem-does-it-solve}

大規模データセットに対するテキスト検索処理には、重大なパフォーマンス上の課題があります。

| 問題 | 影響 | Full-Text Index による解決策 |
|---------|--------|-------------------------|
| **低速な LIKE クエリ** | `WHERE content LIKE '%keyword%'` はテーブル全体をスキャンする | 用語を直接検索し、無関係なドキュメントをスキップ |
| **フルテーブルスキャン** | すべてのテキスト検索で全行を読み取る | 検索語を含むドキュメントだけを読み取る |
| **検索体験の低下** | ユーザーは検索結果を得るまでに数秒から数分待たされる | サブ秒レベルの検索応答時間 |
| **限定的な検索機能** | 基本的なパターンマッチングのみ | あいまい検索、関連度スコアリングなどの高度な機能 |
| **高いリソース使用量** | テキスト検索で過剰な CPU/メモリ を消費する | インデックス付き検索では最小限のリソースで済む |

**例**: 1000 万件のログエントリから "kubernetes error" を検索する場合、full-text index がなければ 1000 万行すべてをスキャンします。full-text index があれば、約 1000 件の一致するドキュメントを即座に直接見つけられます。

## 仕組み {#how-it-works}

full-text index は、用語からドキュメントへの転置マッピングを作成します。

| 用語 | ドキュメント ID |
|------|-------------|
| "kubernetes" | 101, 205, 1847 |
| "error" | 101, 892, 1847 |
| "pod" | 205, 1847, 2901 |

"kubernetes error" を検索すると、インデックスはテーブル全体をスキャンすることなく、両方の用語を含むドキュメント（101、1847）を見つけます。

## クイックセットアップ {#quick-setup}

```sql
-- Create table with text content
CREATE TABLE logs(id INT, message TEXT, timestamp TIMESTAMP);

-- Create full-text index - automatically indexes new data
CREATE INVERTED INDEX logs_message_idx ON logs(message);

-- One-time refresh needed only for existing data before index creation
REFRESH INVERTED INDEX logs_message_idx ON logs;

-- Search using MATCH function - fully automatic optimization
SELECT * FROM logs WHERE MATCH(message, 'error kubernetes');
```

**自動インデックス管理**:

- **新規データ**: 挿入時に自動でインデックス化されるため、手動操作は不要
- **既存データ**: インデックス作成前から存在していたデータに対してのみ、1 回の refresh が必要
- **継続的な管理**: {{{ .lake }}} が最適な検索パフォーマンスを自動的に管理

## 検索関数 {#search-functions}

| 関数 | 用途 | 例 |
|----------|---------|---------|
| `MATCH(column, 'terms')` | 基本的なテキスト検索 | `MATCH(content, 'database performance')` |
| `QUERY('column:terms')` | 高度なクエリ構文 | `QUERY('title:"full text" AND content:search')` |
| `SCORE()` | 関連度スコアリング | `SELECT *, SCORE() FROM docs WHERE MATCH(...)` |

## 高度な検索機能 {#advanced-search-features}

### あいまい検索 {#fuzzy-search}

```sql
-- Find documents even with typos (fuzziness=1 allows 1 character difference)
SELECT * FROM logs WHERE MATCH(message, 'kubernetes', 'fuzziness=1');
```

### 関連度スコアリング {#relevance-scoring}

```sql
-- Get results with relevance scores, filter by minimum score
SELECT id, message, SCORE() as relevance
FROM logs
WHERE MATCH(message, 'critical error') AND SCORE() > 0.5
ORDER BY SCORE() DESC;
```

### 複雑なクエリ {#complex-queries}

```sql
-- Advanced query syntax with boolean operators
SELECT * FROM docs WHERE QUERY('title:"user guide" AND content:(tutorial OR example)');
```

## Complete Example {#complete-example}

この例では、Kubernetes のログデータにフルテキスト検索インデックスを作成し、さまざまな関数を使って検索する方法を示します。

```sql
-- Create a table with a computed column
CREATE TABLE k8s_logs (
    event_id INT,
    event_data VARIANT,
    event_timestamp TIMESTAMP,
    event_message VARCHAR AS (event_data['message']::VARCHAR) STORED
);

-- Create an inverted index on the "event_message" column
CREATE INVERTED INDEX event_message_fulltext ON k8s_logs(event_message);

-- Insert comprehensive sample data
INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (1,
    PARSE_JSON('{
        "message": "Pod scheduled",
        "object_type": "Pod",
        "name": "frontend-1",
        "namespace": "production",
        "node": "node-01",
        "status": "Scheduled"
    }'),
    '2024-04-08T08:00:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (2,
    PARSE_JSON('{
        "message": "Deployment scaled",
        "object_type": "Deployment",
        "name": "backend",
        "namespace": "development",
        "replicas": 3
    }'),
    '2024-04-08T09:15:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (3,
    PARSE_JSON('{
        "message": "Node condition changed",
        "object_type": "Node",
        "name": "node-02",
        "condition": "Ready",
        "status": "True"
    }'),
    '2024-04-08T10:30:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (4,
    PARSE_JSON('{
        "message": "ConfigMap updated",
        "object_type": "ConfigMap",
        "name": "app-config",
        "namespace": "default",
        "change": "data update"
    }'),
    '2024-04-08T11:45:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (5,
    PARSE_JSON('{
        "message": "PersistentVolume claim created",
        "object_type": "PVC",
        "name": "storage-claim",
        "namespace": "storage",
        "status": "Bound",
        "volume": "pv-logs"
    }'),
    '2024-04-08T12:00:00Z');

-- Basic search for events containing "PersistentVolume"
SELECT
  event_id,
  event_message
FROM
  k8s_logs
WHERE
  MATCH(event_message, 'PersistentVolume');

-[ RECORD 1 ]-----------------------------------
     event_id: 5
event_message: PersistentVolume claim created

-- Verify index usage with EXPLAIN
EXPLAIN SELECT event_id, event_message FROM k8s_logs WHERE MATCH(event_message, 'PersistentVolume');

-[ EXPLAIN ]-----------------------------------
Filter
├── output columns: [k8s_logs.event_id (#0), k8s_logs.event_message (#3)]
├── filters: [k8s_logs._search_matched (#4)]
├── estimated rows: 5.00
└── TableScan
    ├── table: default.default.k8s_logs
    ├── output columns: [event_id (#0), event_message (#3), _search_matched (#4)]
    ├── read rows: 1
    ├── read size: < 1 KiB
    ├── partitions total: 5
    ├── partitions scanned: 1
    ├── pruning stats: [segments: <range pruning: 5 to 5>, blocks: <range pruning: 5 to 5, inverted pruning: 5 to 1>]
    ├── push downs: [filters: [k8s_logs._search_matched (#4)], limit: NONE]
    └── estimated rows: 5.00

-- Advanced search with relevance scoring
SELECT
  event_id,
  event_message,
  event_timestamp,
  SCORE()
FROM
  k8s_logs
WHERE
  SCORE() > 0.5
  AND QUERY('event_message:"PersistentVolume claim created"');

-[ RECORD 1 ]-----------------------------------
       event_id: 5
  event_message: PersistentVolume claim created
event_timestamp: 2024-04-08 12:00:00
        score(): 0.86304635

-- Fuzzy search example (handles typos)
SELECT
    event_id, event_message, event_timestamp
FROM
    k8s_logs
WHERE
    match('event_message', 'PersistentVolume claim create', 'fuzziness=1');

-[ RECORD 1 ]-----------------------------------
       event_id: 5
  event_message: PersistentVolume claim created
event_timestamp: 2024-04-08 12:00:00
```

**この例のポイント:**

- `inverted pruning: 5 to 1` は、インデックスによってスキャン対象のブロック数が 5 から 1 に削減されたことを示します
- 関連度スコアリングにより、一致品質に基づいて結果を順位付けできます
- あいまい検索では、タイプミスがあっても結果を見つけられます（`"create"` と `"created"` など）

## Best Practices {#best-practices}

| ベストプラクティス | 利点 |
|----------|---------|
| **頻繁に検索されるカラムにインデックスを作成する** | 検索クエリで使用されるカラムに重点を置けます |
| **LIKE ではなく MATCH を使用する** | 自動インデックスのパフォーマンスを活用できます |
| **インデックス使用状況を監視する** | EXPLAIN を使用してインデックスが活用されていることを確認できます |
| **複数のインデックスを検討する** | 異なるカラムに個別のインデックスを作成できます |

## Essential Commands {#essential-commands}

| Command | 用途 | 使用するタイミング |
|---------|---------|-------------|
| `CREATE INVERTED INDEX name ON table(column)` | 新しいフルテキストインデックスを作成する | 初期セットアップ時 - 新しいデータには自動的に適用されます |
| `REFRESH INVERTED INDEX name ON table` | 既存データをインデックス化する | インデックス作成前から存在していたデータに対して一度だけ実行します |
| `DROP INVERTED INDEX name ON table` | インデックスを削除する | インデックスが不要になったとき |

## Important Notes {#important-notes}

**フルテキストインデックスを使用する場面:**

- 大規模なテキストデータセット（ドキュメント、ログ、コメント）
- 頻繁なテキスト検索操作
- 高度な検索機能（あいまい検索、スコアリング）が必要な場合
- パフォーマンスが重要な検索アプリケーション

**使用しないほうがよい場面:**

- 小規模なテキストデータセット
- 完全一致の文字列マッチングのみが必要な場合
- 検索操作の頻度が低い場合

## Index Limitations {#index-limitations}

- 各カラムは 1 つの inverted index にしか含められません
- データ挿入後に refresh が必要です（インデックス作成前からデータが存在していた場合）
- インデックスデータ用に追加のストレージ領域を使用します

---

*フルテキストインデックスは、大規模なドキュメントコレクション全体に対して高速で高度なテキスト検索機能を必要とするアプリケーションに不可欠です。*