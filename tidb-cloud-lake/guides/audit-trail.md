---
title: 監査証跡
summary: "{{{ .lake }}} system history tables automatically capture detailed records of database activities, providing a complete audit trail for compliance and security monitoring."
---

# 監査証跡

{{{ .lake }}} の system history tables は、データベースアクティビティの詳細な記録を自動的に取得し、コンプライアンス対応とセキュリティ監視のための完全な監査証跡を提供します。

ユーザーに対して次の監査を実行できます。

- **Query execution** - SQL 実行の完全な監査証跡 (`query_history`)
- **Data access** - データベースオブジェクトへのアクセスと変更 (`access_history`)
- **Authentication** - ログイン試行とセッショントラッキング (`login_history`)

## 利用可能な監査テーブル {#available-audit-tables}

{{{ .lake }}} は、データベースアクティビティのさまざまな側面を記録する 5 つの system history tables を提供します。

| テーブル | 目的 | 主なユースケース |
|-------|---------|---------------|
| [query_history](/tidb-cloud-lake/sql/system-history-query-history.md) | SQL 実行の完全な監査証跡 | パフォーマンス監視、セキュリティ監査、コンプライアンスレポート |
| [access_history](/tidb-cloud-lake/sql/system-history-access-history.md) | データベースオブジェクトへのアクセスと変更 | データリネージの追跡、コンプライアンス監査、変更管理 |
| [login_history](/tidb-cloud-lake/sql/system-history-login-history.md) | 認証試行とセッション | セキュリティ監視、ログイン失敗の検出、アクセスパターン分析 |

## 監査のユースケースと例 {#audit-use-cases-examples}

### セキュリティ監視 {#security-monitoring}

**ログイン失敗の試行を監視する**

認証失敗を追跡して、潜在的なセキュリティ脅威や不正アクセスの試行を特定します。

```sql
-- Check for failed login attempts (security audit)
SELECT event_time, user_name, client_ip, error_message
FROM system_history.login_history
WHERE event_type = 'LoginFailed'
ORDER BY event_time DESC;
```

出力例:

```
event_time: 2025-06-03 06:07:32.512021
user_name: root1
client_ip: 127.0.0.1:62050
error_message: UnknownUser. Code: 2201, Text = User 'root1'@'%' does not exist.
```

### コンプライアンスレポート {#compliance-reporting}

**データベーススキーマの変更を追跡する**

コンプライアンスおよび変更管理の要件に対応するため、DDL 操作を監視します。

```sql
-- Audit DDL operations (compliance tracking)
SELECT query_id, query_start, user_name, object_modified_by_ddl
FROM system_history.access_history
WHERE object_modified_by_ddl != '[]'
ORDER BY query_start DESC;
```

`CREATE TABLE` 操作の例:

```
query_id: c2c1c7be-cee4-4868-a28e-8862b122c365
query_start: 2025-06-12 03:31:19.042128
user_name: root
object_modified_by_ddl: [{"object_domain":"Table","object_name":"default.default.t","operation_type":"Create"}]
```

**データアクセスパターンを監査する**

コンプライアンスとデータガバナンスのために、誰がいつどのデータにアクセスしたかを追跡します。

```sql
-- Track data access for compliance
SELECT query_id, query_start, user_name, base_objects_accessed
FROM system_history.access_history
WHERE base_objects_accessed != '[]'
ORDER BY query_start DESC;
```

### 運用監視 {#operational-monitoring}

**完全なクエリ実行監査**

ユーザー情報と実行時間情報を含めて、すべての SQL 操作の包括的な記録を管理します。

```sql
-- Complete query audit with user and timing information
SELECT query_id, sql_user, query_text, query_start_time, query_duration_ms, client_address
FROM system_history.query_history
WHERE event_date >= TODAY() - INTERVAL 7 DAY
ORDER BY query_start_time DESC;
```

出力例:

```
query_id: 4e1f50a9-bce2-45cc-86e4-c7a36b9b8d43
sql_user: root
query_text: SELECT * FROM t
query_start_time: 2025-06-12 03:31:35.041725
query_duration_ms: 94
client_address: 127.0.0.1
```

<!--
For detailed information about each audit table and their specific fields, see the [System History Tables](/tidb-cloud-lake/sql/system-history-tables.md) reference documentation.
-->