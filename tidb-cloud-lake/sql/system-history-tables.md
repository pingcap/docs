---
title: システム履歴テーブル
summary: "{{{ .lake }}} のシステム履歴テーブルは、コンプライアンス、セキュリティ監視、パフォーマンス分析のためにデータベースアクティビティを自動的に追跡し、データガバナンス機能を提供します。"
---

# システム履歴テーブル

{{{ .lake }}} のシステム履歴テーブルは、コンプライアンス、セキュリティ監視、パフォーマンス分析のためにデータベースアクティビティを自動的に追跡し、**データガバナンス**機能を提供します。

## 利用可能なテーブル {#available-tables}

| テーブル                                 | 目的                            | 主なユースケース                                                          |
| ------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------- |
| [query_history](/tidb-cloud-lake/sql/system-history-query-history.md)     | 完全な SQL 実行監査証跡            | パフォーマンス分析、コンプライアンス追跡、使用状況の監視              |
| [access_history](/tidb-cloud-lake/sql/system-history-access-history.md)   | データアクセスおよび変更ログ       | データリネージ、コンプライアンスレポート、変更管理                    |
| [login_history](/tidb-cloud-lake/sql/system-history-login-history.md)     | ユーザー認証の追跡                 | セキュリティ監査、ログイン失敗の監視、アクセスパターン分析            |
| [profile_history](/tidb-cloud-lake/sql/system-history-profile-history.md) | 詳細なクエリ実行プロファイル       | パフォーマンス最適化、リソース計画、ボトルネックの特定                |
| [log_history](/tidb-cloud-lake/sql/system-history-log-history.md)         | 生のシステムログおよびイベント     | システムトラブルシューティング、エラー分析、運用監視                  |

## 権限 {#permissions}

**アクセス制限:**

- `SELECT` および `DROP` 操作のみ許可されています
- すべてのユーザーに対して ALTER 操作は禁止されています
- 所有権は移譲できません

**必要な権限:**

システム履歴テーブルをクエリするには、ユーザーに次のいずれかが必要です。

- `GRANT SELECT ON *.*`（グローバルアクセス）
- `GRANT SELECT ON system_history.*`（データベースアクセス）
- `GRANT SELECT ON system_history.table_name`（テーブル単位のアクセス）

**例:**

```sql
-- Create audit role for compliance team
CREATE ROLE audit_team;
GRANT SELECT ON system_history.* TO ROLE audit_team;
CREATE USER compliance_officer IDENTIFIED BY 'secure_password' WITH DEFAULT_ROLE='audit_team';
GRANT ROLE audit_team TO USER compliance_officer;
```

## 設定 {#configuration}

### {{{ .lake }}} {#lake}

✅ **自動的に有効化** - すべてのシステム履歴テーブルは、追加の設定なしですぐに使用できます。