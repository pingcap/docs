---
title: Upstream Database Configuration File of TiDB Data Migration
summary: アップストリームデータベースの設定ファイルを学ぶ
---

# TiDB データ移行の上流データベースコンフィグレーションファイル {#upstream-database-configuration-file-of-tidb-data-migration}

このドキュメントでは、アップストリーム データベースの構成ファイルについて紹介します。これには、構成ファイル テンプレートと、このファイル内の各構成パラメータの説明が含まれます。

## コンフィグレーションファイルテンプレート {#configuration-file-template}

以下は、アップストリーム データベースの構成ファイル テンプレートです。

```yaml
source-id: "mysql-replica-01"

# Whether to enable GTID.
enable-gtid: false

# Whether to enable relay log.
enable-relay: false
relay-binlog-name: ""     # The file name from which DM-worker starts to pull the binlog.
relay-binlog-gtid: ""     # The GTID from which DM-worker starts to pull the binlog.
# relay-dir: "relay-dir"  # The directory used to store relay log. The default value is "relay-dir". This configuration item is marked as deprecated since v6.1 and replaced by a parameter of the same name in the dm-worker configuration.


from:
  host: "127.0.0.1"
  port: 3306
  user: "root"
  password: "ZqMLjZ2j5khNelDEfDoUhkD5aV5fIJOe0fiog9w=" # The user password of the upstream database. It is recommended to use the password encrypted with dmctl.
  security:                       # The TLS configuration of the upstream database
    ssl-ca: "/path/to/ca.pem"
    ssl-cert: "/path/to/cert.pem"
    ssl-key: "/path/to/key.pem"

# purge:
#   interval: 3600
#   expires: 0
#   remain-space: 15

# checker:
#   check-enable: true
#   backoff-rollback: 5m0s
#   backoff-max: 5m0s       # The maximum value of backoff, should be larger than 1s

# Configure binlog event filters. New in DM v2.0.2
# case-sensitive: false
# filters:
# - schema-pattern: dmctl
#   table-pattern: t_1
#   events: []
#   sql-pattern:
#   - alter table .* add column `aaa` int
#   action: Ignore
```

> **注記：**
>
> DM v2.0.1では、 `enable-gtid`と`enable-relay`を同時に`true`に設定しないでください。そうしないと、増分データが失われる可能性があります。

## コンフィグレーションパラメータ {#configuration-parameters}

このセクションでは、構成ファイル内の各構成パラメータについて説明します。

### グローバル構成 {#global-configuration}

#### <code>source-id</code> {#code-source-id-code}

-   MySQL インスタンス ID を表します。

#### <code>enable-gtid</code> {#code-enable-gtid-code}

-   GTID を使用してアップストリームからbinlogをプルするかどうかを決定します。
-   通常、 `enable-gtid`手動で設定する必要はありません。ただし、上流データベースでGTIDが有効になっていて、プライマリ/セカンダリスイッチが必要な場合は、 `enable-gtid`を`true`に設定する必要があります。
-   デフォルト値: `false`

#### <code>enable-relay</code> {#code-enable-relay-code}

-   リレーログ機能を有効にするかどうかを指定します。このパラメータはバージョン5.4以降で有効になります。また、コマンド`start-relay`を使用して[リレーログを動的に有効にする](/dm/relay-log.md#enable-and-disable-relay-log)実行することもできます。
-   デフォルト値: `false`

#### <code>relay-binlog-name</code> {#code-relay-binlog-name-code}

-   DM-workerがbinlogの取得を開始するファイル名を指定します。例： `"mysql-bin.000002"` 。
-   [`enable-gtid`](#enable-gtid)が`false`場合にのみ機能します。このパラメータが指定されていない場合、DM-workerは複製される最も古いbinlogファイルからプルを開始します。通常、手動設定は必要ありません。

#### <code>relay-binlog-gtid</code> {#code-relay-binlog-gtid-code}

-   DMワーカーがbinlogのプルを開始するGTIDを指定します。例： `"e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849"` 。
-   [`enable-gtid`](#enable-gtid)が`true`場合にのみ機能します。このパラメータが指定されていない場合、DMワーカーはレプリケーション中の最新のGTIDからプルを開始します。通常、手動設定は必要ありません。

#### <code>relay-dir</code> {#code-relay-dir-code}

-   リレー ログ ディレクトリを指定します。
-   デフォルト値: `"./relay_log"`

#### <code>host</code> {#code-host-code}

-   アップストリーム データベースのホストを指定します。

#### <code>port</code> {#code-port-code}

-   アップストリーム データベースのポートを指定します。

#### <code>user</code> {#code-user-code}

-   アップストリーム データベースのユーザー名を指定します。

#### <code>password</code> {#code-password-code}

-   アップストリームデータベースのユーザーパスワードを指定します。dmctlで暗号化されたパスワードを使用することをお勧めします。

#### <code>security</code> {#code-security-code}

-   アップストリームデータベースのTLS設定を指定します。証明書のファイルパスは、すべてのノードからアクセスできる必要があります。ファイルパスがローカルパスの場合、クラスター内のすべてのノードは、各ホストの同じパスに証明書のコピーを保存する必要があります。

### リレーログクリーンアップ戦略の構成（ <code>purge</code> ） {#relay-log-cleanup-strategy-configuration-code-purge-code}

通常、リレーログが大量に存在し、ディスク容量が不足している場合を除き、これらのパラメータを手動で設定する必要はありません。

#### <code>interval</code> {#code-interval-code}

-   リレー ログの有効期限を定期的にチェックする間隔 (秒単位) を指定します。
-   デフォルト値: `3600`
-   単位: 秒

#### <code>expires</code> {#code-expires-code}

-   リレー ログの有効期限を指定します。
-   リレー処理ユニットによって書き込まれていない、または既存のデータ移行タスクによって読み取る必要がないリレーログは、有効期限を過ぎるとDMによって削除されます。このパラメータが指定されていない場合、自動パージは実行されません。
-   デフォルト値: `0`
-   単位: 時間

#### <code>remain-space</code> {#code-remain-space-code}

-   空きディスク容量の最小値をギガバイト単位で指定します。使用可能なディスク容量がこの値より小さい場合、DM-workerはリレーログを削除しようとします。
-   デフォルト値: `15`
-   単位: GiB

> **注記：**
>
> 自動データ消去戦略は、 [`interval`](#interval) `0`でなく、 2 つの構成項目[`expires`](#expires)と[`remain-space`](#remain-space)うち少なくとも 1 つが`0`でない場合にのみ有効になります。

### タスクステータスチェッカーの設定（ <code>checker</code> ） {#task-status-checker-configuration-code-checker-code}

DMは定期的に現在のタスクステータスとエラーメッセージを確認し、タスクを再開することでエラーが解消されるかどうかを判断します。必要に応じて、DMは自動的にタスクの再開を再試行します。DMは指数バックオフ戦略を使用してチェック間隔を調整します。DMの動作は、以下の設定で調整できます。

#### <code>check-enable</code> {#code-check-enable-code}

-   この機能を有効にするかどうか。

#### <code>backoff-rollback</code> {#code-backoff-rollback-code}

-   バックオフ戦略の現在のチェック間隔がこの値より大きく、タスクのステータスが正常である場合、DM は間隔を短縮しようとします。

#### <code>backoff-max</code> {#code-backoff-max-code}

-   バックオフ戦略のチェック間隔の最大値は 1 秒より大きくなければなりません。

### Binlogイベントフィルター {#binlog-event-filter}

DM v2.0.2 以降では、ソース構成ファイルでbinlogイベント フィルターを構成できます。

#### <code>case-sensitive</code> {#code-case-sensitive-code}

-   フィルタリング ルールで大文字と小文字を区別するかどうかを決定します。
-   デフォルト値: `false`

#### <code>filters</code> {#code-filters-code}

-   binlogイベントのフィルタリングルールを指定します。詳細については[Binlogイベントフィルターパラメータの説明](/dm/dm-binlog-event-filter.md#parameter-descriptions)参照してください。
