---
title: CREATE WORKLOAD GROUP
summary: 指定したクォータ設定で workload group を作成します。workload group はユーザーにバインドすることで、リソース割り当てとクエリ同時実行数を制御します。ユーザーがクエリを送信すると、そのユーザーに割り当てられたグループに基づいて workload group の制限が適用されます。
---

# CREATE WORKLOAD GROUP

指定したクォータ設定で workload group を作成します。workload group はユーザーにバインドすることで、リソース割り当てとクエリ同時実行数を制御します。ユーザーがクエリを送信すると、そのユーザーに割り当てられたグループに基づいて workload group の制限が適用されます。

## 構文 {#syntax}

```sql
CREATE WORKLOAD GROUP [IF NOT EXISTS] <group_name>
[WITH cpu_quota = '<percentage>', query_timeout = '<duration>']
```

## パラメータ {#parameters}

| パラメータ              | 型     | 必須 | デフォルト      | 説明                                                                 |
|------------------------|----------|----------|--------------|-----------------------------------------------------------------------------|
| `cpu_quota`            | string   | いいえ       | (unlimited)  | パーセンテージ文字列で指定する CPU リソースクォータ（例: `"20%"`）                      |
| `query_timeout`        | duration | いいえ       | (unlimited)  | クエリタイムアウト時間（単位: `s`/`sec`=秒、`m`/`min`=分、`h`/`hour`=時間、`d`/`day`=日、`ms`=ミリ秒、単位なし=秒） |
| `memory_quota`         | string or integer   | いいえ       | (unlimited)  | ワークロードグループの最大メモリ使用量制限（パーセンテージまたは絶対値） |
| `max_concurrency`      | integer  | いいえ       | (unlimited)  | ワークロードグループの最大同時実行数                               |
| `query_queued_timeout` | duration | いいえ       | (unlimited)  | ワークロードグループが最大同時実行数を超えた場合の最大キュー待機時間（単位: `s`/`sec`=秒、`m`/`min`=分、`h`/`hour`=時間、`d`/`day`=日、`ms`=ミリ秒、単位なし=秒）      |

## 例 {#examples}

### 基本例 {#basic-example}

```sql
-- Create workload groups
CREATE WORKLOAD GROUP IF NOT EXISTS interactive_queries
WITH cpu_quota = '30%', memory_quota = '20%', max_concurrency = 2;

CREATE WORKLOAD GROUP IF NOT EXISTS batch_processing
WITH cpu_quota = '70%', memory_quota = '80%', max_concurrency = 10;
```

### ユーザー割り当て {#user-assignment}

リソース制限を有効にするには、ユーザーを workload group に割り当てる必要があります。ユーザーがクエリを実行すると、システムは workload group の制限を自動的に適用します。

```sql
-- Create role and grant permissions
CREATE ROLE analytics_role;
GRANT ALL ON *.* TO ROLE analytics_role;
CREATE USER analytics_user IDENTIFIED BY 'password123' WITH DEFAULT_ROLE = 'analytics_role';
GRANT ROLE analytics_role TO analytics_user;

-- Assign user to workload group
ALTER USER analytics_user WITH SET WORKLOAD GROUP = 'interactive_queries';

-- Reassign to different workload group
ALTER USER analytics_user WITH SET WORKLOAD GROUP = 'batch_processing';

-- Remove from workload group (user will use default unlimited resources)
ALTER USER analytics_user WITH UNSET WORKLOAD GROUP;

-- Check user's workload group
DESC USER analytics_user;
```

## リソースクォータの正規化 {#resource-quota-normalization}

### クォータ制限 {#quota-limits}

- 各 workload group の `cpu_quota` と `memory_quota` は最大 `100%`（1.0）まで設定できます
- workload group 全体にわたるすべてのクォータの合計は 100% を超えることができます
- 実際のリソース割り当ては、相対的な比率に基づいて**正規化**されます

### クォータ正規化の仕組み {#how-quota-normalization-works}

リソースは、全体に対する各グループのクォータの比率に基づいて比例配分されます。

```
Actual Allocation = (Group Quota) / (Sum of All Group Quotas) × 100%
```

**例 1: クォータ合計 = 100%**

- Group A: 30% quota → リソースの 30% を取得（30/100）
- Group B: 70% quota → リソースの 70% を取得（70/100）

**例 2: クォータ合計 > 100%**

- Group A: 60% quota → リソースの 40% を取得（60/150）
- Group B: 90% quota → リソースの 60% を取得（90/150）
- クォータ合計: 150%

**例 3: クォータ合計 < 100%**

- Group A: 20% quota → リソースの 67% を取得（20/30）
- Group B: 10% quota → リソースの 33% を取得（10/30）
- クォータ合計: 30%

**特別なケース:** workload group が 1 つしか存在しない場合、設定されたクォータに関係なく、そのグループは Warehouse リソースの 100% を取得します。