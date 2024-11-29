---
title: Server Status Variables
summary: ステータス変数を使用してシステムとセッションのステータスを確認する
---

# サーバーステータス変数 {#server-status-variables}

サーバー ステータス変数は、サーバーのグローバル ステータスと TiDB の現在のセッションのステータスに関する情報を提供します。これらの変数のほとんどは、MySQL と互換性があるように設計されています。

[グローバルステータスを表示](/sql-statements/sql-statement-show-status.md)コマンドを使用してグローバル ステータスを取得し、 [セッションステータスを表示](/sql-statements/sql-statement-show-status.md)コマンドを使用して現在のセッションのステータスを取得できます。

さらに、MySQL との互換性のために[フラッシュステータス](/sql-statements/sql-statement-flush-status.md)コマンドがサポートされています。

## 変数参照 {#variable-reference}

### 圧縮 {#compression}

-   スコープ: セッション
-   タイプ: ブール値
-   MySQL プロトコルが圧縮を使用するかどうかを示します。

### 圧縮アルゴリズム {#compression-algorithm}

-   スコープ: セッション
-   タイプ: 文字列
-   MySQL プロトコルに使用される圧縮アルゴリズムを示します。

### 圧縮レベル {#compression-level}

-   スコープ: セッション
-   タイプ: 整数
-   MySQL プロトコルに使用される圧縮レベル。

### SSL暗号 {#ssl-cipher}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   使用中の TLS 暗号。

### SSL暗号リスト {#ssl-cipher-list}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   サーバーがサポートする TLS 暗号のリスト。

### SSL_サーバーが無効 {#ssl-server-not-after}

-   範囲: セッション | グローバル
-   タイプ: 日付
-   TLS 接続に使用されるサーバーの X.509 証明書の有効期限。

### SSL_サーバーが以前ではない {#ssl-server-not-before}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   TLS 接続に使用されるサーバーの X.509 証明書の開始日。

### SSL検証モード {#ssl-verify-mode}

-   範囲: セッション | グローバル
-   タイプ: 整数
-   TLS 検証モードのビットマスク。

### SSLバージョン {#ssl-version}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   使用されるTLSプロトコルのバージョン

### 稼働時間 {#uptime}

-   範囲: セッション | グローバル
-   タイプ: 整数
-   サーバーの稼働時間（秒単位）。

### ddl_schema_version {#ddl-schema-version}

-   範囲: セッション | グローバル
-   タイプ: 整数
-   使用される DDL スキーマのバージョン。

### last_plan_binding_update_time <span class="version-mark">v5.2.0 の新機能</span> {#last-plan-binding-update-time-span-class-version-mark-new-in-v5-2-0-span}

-   スコープ: セッション
-   タイプ: タイムスタンプ
-   プラン バインディングの最終更新の日時。

### サーバーID {#server-id}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   サーバーの UUID。

### tidb_gc_最終実行時間 {#tidb-gc-last-run-time}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   [GC](/garbage-collection-overview.md)の最後の実行のタイムスタンプ。

### tidb_gc_leader_desc {#tidb-gc-leader-desc}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   ホスト名とプロセス ID (pid) を含む、 [GC](/garbage-collection-overview.md)リーダーに関する情報。

### tidb_gc_leader_lease {#tidb-gc-leader-lease}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   [GC](/garbage-collection-overview.md)リースのタイムスタンプ。

### tidb_gc_leader_uuid {#tidb-gc-leader-uuid}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   [GC](/garbage-collection-overview.md)リーダーの UUID。

### tidb_gc_safe_point {#tidb-gc-safe-point}

-   範囲: セッション | グローバル
-   タイプ: 文字列
-   [GC](/garbage-collection-overview.md)セーフ ポイントのタイムスタンプ。
