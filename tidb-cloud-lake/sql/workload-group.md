---
title: Workload Group
summary: Workload group は、異なるユーザーグループに CPU、メモリのクォータを割り当て、同時実行クエリ数を制限することで、{{{ .lake }}} におけるリソース管理とクエリ同時実行制御を可能にします。
---

# Workload Group

Workload group は、異なるユーザーグループに CPU、メモリのクォータを割り当て、同時実行クエリ数を制限することで、{{{ .lake }}} におけるリソース管理とクエリ同時実行制御を可能にします。

## 仕組み {#how-it-works}

1. CPU、メモリ、同時実行数の制限など、特定のリソースクォータを持つ **workload group を作成** します
2. `ALTER USER` を使用して **ユーザーを workload group に割り当て** ます
3. **クエリ実行時** には、ユーザーに基づいて workload group のリソース制限が自動的に適用されます

## クイック例 {#quick-example}

```sql
-- Create workload group
CREATE WORKLOAD GROUP analytics WITH cpu_quota = '50%', memory_quota = '30%', max_concurrency = 5;

-- Create role and grant permissions
CREATE ROLE analyst_role;
GRANT ALL ON *.* TO ROLE analyst_role;
CREATE USER analyst IDENTIFIED BY 'password' WITH DEFAULT_ROLE = 'analyst_role';
GRANT ROLE analyst_role TO analyst;

-- Assign user to workload group
ALTER USER analyst WITH SET WORKLOAD GROUP = 'analytics';

-- Remove user from workload group (user will use default unlimited resources)
ALTER USER analyst WITH UNSET WORKLOAD GROUP;
```

## コマンドリファレンス {#command-reference}

### 管理 {#management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE WORKLOAD GROUP](/tidb-cloud-lake/sql/create-workload-group.md) | リソースクォータを持つ新しい workload group を作成します |
| [ALTER WORKLOAD GROUP](/tidb-cloud-lake/sql/alter-workload-group.md) | workload group の設定を変更します |
| [DROP WORKLOAD GROUP](/tidb-cloud-lake/sql/drop-workload-group.md) | workload group を削除します |
| [RENAME WORKLOAD GROUP](/tidb-cloud-lake/sql/rename-workload-group.md) | workload group の名前を変更します |

### 情報 {#information}

| コマンド | 説明 |
|---------|-------------|
| [SHOW WORKLOAD GROUPS](/tidb-cloud-lake/sql/show-workload-groups.md) | すべての workload group とその設定を一覧表示します |

> **Tip:**
>
> リソースクォータは、1 つの Warehouse 内のすべての workload group 間で正規化されます。たとえば、2 つのグループに 60% と 40% の CPU クォータが設定されている場合、それぞれ実際のリソースの 60% と 40% が割り当てられます。