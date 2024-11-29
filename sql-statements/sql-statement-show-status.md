---
title: SHOW [GLOBAL|SESSION] STATUS | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW [GLOBAL|SESSION] STATUS の使用法の概要。
---

# [グローバル|セッション]ステータスを表示 {#show-global-session-status}

このステートメントは、MySQL との互換性のために含まれています。TiDB は、ほとんどのメトリックに対して`SHOW STATUS`ではなく、集中メトリック収集に Prometheus と Grafana を使用します。

変数の詳細な説明は、こちらでご覧いただけます: [ステータス変数](/status-variables.md)

## 概要 {#synopsis}

```ebnf+diagram
ShowStatusStmt ::=
    'SHOW' Scope? 'STATUS' ShowLikeOrWhere?

Scope ::=
    ( 'GLOBAL' | 'SESSION' )

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
mysql> SHOW SESSION STATUS;
+-------------------------------+--------------------------------------+
| Variable_name                 | Value                                |
+-------------------------------+--------------------------------------+
| Compression                   | OFF                                  |
| Compression_algorithm         |                                      |
| Compression_level             | 0                                    |
| Ssl_cipher                    |                                      |
| Ssl_cipher_list               |                                      |
| Ssl_server_not_after          |                                      |
| Ssl_server_not_before         |                                      |
| Ssl_verify_mode               | 0                                    |
| Ssl_version                   |                                      |
| Uptime                        | 1409                                 |
| ddl_schema_version            | 116                                  |
| last_plan_binding_update_time | 0000-00-00 00:00:00                  |
| server_id                     | 61160e73-ab80-40ff-8f33-27d55d475fd1 |
+-------------------------------+--------------------------------------+
13 rows in set (0.00 sec)

mysql> SHOW GLOBAL STATUS;
+-----------------------+--------------------------------------+
| Variable_name         | Value                                |
+-----------------------+--------------------------------------+
| Ssl_cipher            |                                      |
| Ssl_cipher_list       |                                      |
| Ssl_server_not_after  |                                      |
| Ssl_server_not_before |                                      |
| Ssl_verify_mode       | 0                                    |
| Ssl_version           |                                      |
| Uptime                | 1413                                 |
| ddl_schema_version    | 116                                  |
| server_id             | 61160e73-ab80-40ff-8f33-27d55d475fd1 |
+-----------------------+--------------------------------------+
9 rows in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

-   このステートメントは MySQL と互換性があります。

## 参照 {#see-also}

-   [フラッシュステータス](/sql-statements/sql-statement-flush-status.md)
-   [サーバーステータス変数](/status-variables.md)
