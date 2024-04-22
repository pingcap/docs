---
title: Server Status Variables
summary: サーバーステータス変数は、サーバーのグローバルステータスとTiDBの現在のセッションのステータスに関する情報を提供します。これらの変数のほとんどは、MySQLと互換性があります。グローバルステータスを表示コマンドを使用するとグローバルステータスを取得でき、セッションステータスを表示コマンドを使用すると現在のセッションのステータスを取得できます。さらに、MySQLとの互換性のためにフラッシュステータスコマンドがサポートされています。SSL_cipher、ssl_cipher_list、ssl_server_not_afterなどの変数があります。それぞれの変数には範囲、タイプ、使用目的が記載されています。
---

# サーバーステータス変数 {#server-status-variables}

サーバー ステータス変数は、サーバーのグローバル ステータスと TiDB の現在のセッションのステータスに関する情報を提供します。これらの変数のほとんどは、MySQL と互換性があるように設計されています。

[グローバルステータスを表示](/sql-statements/sql-statement-show-status.md)コマンドを使用するとグローバル ステータスを取得でき、 [セッションステータスを表示](/sql-statements/sql-statement-show-status.md)コマンドを使用すると現在のセッションのステータスを取得できます。

さらに、MySQL との互換性のために[フラッシュステータス](/sql-statements/sql-statement-flush-status.md)コマンドがサポートされています。

## 変数参照 {#variable-reference}

### SSL_cipher {#ssl-cipher}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   使用中の TLS 暗号。

### ssl_cipher_list {#ssl-cipher-list}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   サーバーがサポートする TLS 暗号のリスト。

### ssl_server_not_after {#ssl-server-not-after}

-   範囲: セッション |グローバル
-   タイプ: 日付
-   TLS 接続に使用されるサーバーの X.509 証明書の有効期限。

### ssl_server_not_before {#ssl-server-not-before}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   TLS 接続に使用されるサーバーの X.509 証明書の開始日。

### SSL_verify_mode {#ssl-verify-mode}

-   範囲: セッション |グローバル
-   タイプ: 整数
-   TLS 検証モードのビットマスク。

### SSL_バージョン {#ssl-version}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   使用されているTLSプロトコルのバージョン

### 稼働時間 {#uptime}

-   範囲: セッション |グローバル
-   タイプ: 整数
-   サーバーの稼働時間 (秒単位)。

### ddl_schema_version {#ddl-schema-version}

-   範囲: セッション |グローバル
-   タイプ: 整数
-   使用される DDL スキーマのバージョン。

### last_plan_binding_update_time <span class="version-mark">v5.2.0 の新機能</span> {#last-plan-binding-update-time-span-class-version-mark-new-in-v5-2-0-span}

-   範囲: セッション
-   タイプ: タイムスタンプ
-   プラン バインディングが最後に更新された日時。

### サーバーID {#server-id}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   サーバーの UUID。

### tidb_gc_last_run_time {#tidb-gc-last-run-time}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   [GC](/garbage-collection-overview.md)の最後の実行のタイムスタンプ。

### tidb_gc_leader_desc {#tidb-gc-leader-desc}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   ホスト名とプロセス ID (pid) を含む、 [GC](/garbage-collection-overview.md)のリーダーに関する情報。

### tidb_gc_leader_lease {#tidb-gc-leader-lease}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   [GC](/garbage-collection-overview.md)リースのタイムスタンプ。

### tidb_gc_leader_uuid {#tidb-gc-leader-uuid}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   [GC](/garbage-collection-overview.md)リーダーの UUID。

### tidb_gc_safe_point {#tidb-gc-safe-point}

-   範囲: セッション |グローバル
-   タイプ: 文字列
-   [GC](/garbage-collection-overview.md)の安全ポイントのタイムスタンプ。
