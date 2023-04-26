---
title: Upstream Database Configuration File of TiDB Data Migration
summary: Learn the configuration file of the upstream database
---

# TiDB データ移行のアップストリーム データベースコンフィグレーションファイル {#upstream-database-configuration-file-of-tidb-data-migration}

このドキュメントでは、構成ファイル テンプレートと、このファイル内の各構成パラメーターの説明を含む、アップストリーム データベースの構成ファイルを紹介します。

## コンフィグレーションファイルのテンプレート {#configuration-file-template}

以下は、アップストリーム データベースの構成ファイル テンプレートです。

```yaml
source-id: "mysql-replica-01"

# Whether to enable GTID.
enable-gtid: false

# Whether to enable relay log.
enable-relay: false       # Since DM v2.0.2, this configuration item is deprecated. To enable the relay log feature, use the `start-relay` command instead.
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

> **ノート：**
>
> DM v2.0.1 では、 `enable-gtid`と`enable-relay` ～ `true`同時に設定しないでください。そうしないと、増分データが失われる可能性があります。

## コンフィグレーションパラメータ {#configuration-parameters}

このセクションでは、構成ファイル内の各構成パラメーターについて説明します。

### グローバル構成 {#global-configuration}

| パラメータ               | 説明                                                                                                                                                                                         |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `source-id`         | MySQL インスタンス ID を表します。                                                                                                                                                                     |
| `enable-gtid`       | GTID を使用して上流からbinlogをプルするかどうかを決定します。デフォルト値は`false`です。通常、 `enable-gtid`手動で構成する必要はありません。ただし、アップストリーム データベースで GTID が有効になっており、プライマリ/セカンダリ スイッチが必要な場合は、 `enable-gtid`を`true`に設定する必要があります。       |
| `enable-relay`      | リレー ログ機能を有効にするかどうかを決定します。デフォルト値は`false`です。 DM v2.0.2 以降、この構成アイテムは廃止されました。 [リレーログ機能を有効にする](/dm/relay-log.md#start-and-stop-the-relay-log-feature)には、代わりに`start-relay`コマンドを使用します。            |
| `relay-binlog-name` | DM-worker がbinlogのプルを開始するファイル名を指定します。たとえば、 `"mysql-bin.000002"`です。 `enable_gtid`が`false`の場合にのみ機能します。このパラメーターが指定されていない場合、DM-worker はバイナリログを最新のものからプルします。                                    |
| `relay-binlog-gtid` | DM-worker がbinlog のプルを開始する GTID を指定します。たとえば、 `"e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849"`です。 `enable_gtid`が`true`の場合にのみ機能します。このパラメーターが指定されていない場合、DM-worker は最新の GTID から始まるバイナリログをプルします。 |
| `relay-dir`         | リレー ログ ディレクトリを指定します。                                                                                                                                                                       |
| `host`              | アップストリーム データベースのホストを指定します。                                                                                                                                                                 |
| `port`              | アップストリーム データベースのポートを指定します。                                                                                                                                                                 |
| `user`              | アップストリーム データベースのユーザー名を指定します。                                                                                                                                                               |
| `password`          | アップストリーム データベースのユーザー パスワードを指定します。 dmctl で暗号化されたパスワードを使用することをお勧めします。                                                                                                                        |
| `security`          | アップストリーム データベースの TLS 構成を指定します。構成された証明書のファイル パスは、すべてのノードからアクセスできる必要があります。構成されたファイル パスがローカル パスである場合、クラスター内のすべてのノードは、証明書のコピーを各ホストの同じパスに格納する必要があります。                                           |

### リレー ログのクリーンアップ戦略の構成 ( <code>purge</code> ) {#relay-log-cleanup-strategy-configuration-code-purge-code}

通常、大量のリレー ログがあり、ディスク容量が不十分でない限り、これらのパラメータを手動で設定する必要はありません。

| パラメータ          | 説明                                                                                                                    | デフォルト値 |
| :------------- | :-------------------------------------------------------------------------------------------------------------------- | :----- |
| `interval`     | リレー ログの有効期限が定期的にチェックされる時間間隔を秒単位で設定します。                                                                                | `3600` |
| `expires`      | リレー ログの有効期限を時間単位で設定します。中継処理部で書き込まれず、既存のデータ移行タスクで読み込む必要のない中継ログは、有効期限を過ぎた場合DMで削除されます。このパラメーターが指定されていない場合、自動パージは実行されません。 | `0`    |
| `remain-space` | 空きディスク容量の最小量をギガバイト単位で設定します。使用可能なディスク容量がこの値よりも小さい場合、DM-worker はリレー ログを削除しようとします。                                       | `15`   |

> **ノート：**
>
> 自動データ消去戦略は、 `interval`が 0 ではなく、2 つの構成アイテム`expires`と`remain-space`の少なくとも 1 つが 0 でない場合にのみ有効になります。

### タスクステータスチェッカー構成 ( <code>checker</code> ) {#task-status-checker-configuration-code-checker-code}

DM は、現在のタスクのステータスとエラー メッセージを定期的にチェックして、タスクを再開することでエラーが解消されるかどうかを判断します。必要に応じて、DM はタスクの再開を自動的に再試行します。 DM は、指数バックオフ戦略を使用してチェック間隔を調整します。その動作は、次の構成によって調整できます。

| パラメータ              | 説明                                                              |
| :----------------- | :-------------------------------------------------------------- |
| `check-enable`     | この機能を有効にするかどうか。                                                 |
| `backoff-rollback` | バックオフ戦略の現在のチェック間隔がこの値よりも大きく、タスク ステータスが正常である場合、DM は間隔を短縮しようとします。 |
| `backoff-max`      | バックオフ戦略のチェック間隔の最大値は、1 秒より大きくする必要があります。                          |

### Binlogイベント フィルター {#binlog-event-filter}

DM v2.0.2 以降では、ソース構成ファイルでbinlogイベント フィルターを構成できます。

| パラメータ            | 説明                                                                                                                               |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `case-sensitive` | フィルタリング ルールで大文字と小文字を区別するかどうかを決定します。デフォルト値は`false`です。                                                                             |
| `filters`        | binlogイベントのフィルタリング ルールを設定します。詳細については、 [Binlogイベント フィルタ パラメータの説明](/dm/dm-binlog-event-filter.md#parameter-descriptions)を参照してください。 |
