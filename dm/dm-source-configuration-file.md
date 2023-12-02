---
title: Upstream Database Configuration File of TiDB Data Migration
summary: Learn the configuration file of the upstream database
---

# TiDB データ移行の上流データベースコンフィグレーションファイル {#upstream-database-configuration-file-of-tidb-data-migration}

このドキュメントでは、構成ファイル テンプレートとこのファイル内の各構成パラメータの説明を含む、アップストリーム データベースの構成ファイルについて説明します。

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

> **注記：**
>
> DM v2.0.1 では、 `enable-gtid`と`enable-relay` ～ `true`同時に設定しないでください。そうしないと、増分データが失われる可能性があります。

## コンフィグレーションパラメータ {#configuration-parameters}

このセクションでは、構成ファイル内の各構成パラメータについて説明します。

### グローバル構成 {#global-configuration}

| パラメータ               | 説明                                                                                                                                                                                                     |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `source-id`         | MySQL インスタンス ID を表します。                                                                                                                                                                                 |
| `enable-gtid`       | GTID を使用してアップストリームからbinlogをプルするかどうかを決定します。デフォルト値は`false`です。通常、 `enable-gtid`手動で構成する必要はありません。ただし、GTID がアップストリーム データベースで有効になっており、プライマリ/セカンダリ スイッチが必要な場合は、 `enable-gtid` ～ `true`を設定する必要があります。            |
| `enable-relay`      | リレーログ機能を有効にするかどうかを決定します。デフォルト値は`false`です。 DM v2.0.2 以降、この構成項目は非推奨になりました。 [リレーログ機能を有効にする](/dm/relay-log.md#enable-and-disable-relay-log)にするには、代わりに`start-relay`コマンドを使用します。                              |
| `relay-binlog-name` | DM-worker がbinlogの取得を開始するファイル名を指定します。たとえば、 `"mysql-bin.000002"` 。 `enable_gtid`が`false`の場合にのみ機能します。このパラメータが指定されていない場合、DM ワーカーはレプリケートされている最も古いbinlogファイルから取得を開始します。通常、手動構成は必要ありません。                     |
| `relay-binlog-gtid` | DM ワーカーがbinlogの取得を開始する GTID を指定します。たとえば、 `"e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849"` 。 `enable_gtid`が`true`の場合にのみ機能します。このパラメータが指定されていない場合、DM ワーカーはレプリケートされている最新の GTID からの取得を開始します。通常、手動構成は必要ありません。 |
| `relay-dir`         | リレーログのディレクトリを指定します。                                                                                                                                                                                    |
| `host`              | 上流データベースのホストを指定します。                                                                                                                                                                                    |
| `port`              | 上流データベースのポートを指定します。                                                                                                                                                                                    |
| `user`              | 上流データベースのユーザー名を指定します。                                                                                                                                                                                  |
| `password`          | 上流データベースのユーザーパスワードを指定します。 dmctlで暗号化したパスワードを使用することを推奨します。                                                                                                                                               |
| `security`          | アップストリーム データベースの TLS 構成を指定します。証明書の構成されたファイル パスは、すべてのノードからアクセスできる必要があります。構成されたファイル パスがローカル パスの場合、クラスター内のすべてのノードは、各ホストの同じパスに証明書のコピーを保存する必要があります。                                                         |

### リレーログのクリーンアップ戦略の構成 ( <code>purge</code> ) {#relay-log-cleanup-strategy-configuration-code-purge-code}

通常、大量のリレーログがありディスク容量が不足しない限り、これらのパラメータを手動で設定する必要はありません。

| パラメータ          | 説明                                                                                                                             | デフォルト値 |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------- | :----- |
| `interval`     | リレーログの有効期限を定期的にチェックする時間間隔を秒単位で設定します。                                                                                           | `3600` |
| `expires`      | リレーログの有効期限を時間単位で設定します。中継処理部で書き込まれていない中継ログ、または既存のデータ移行タスクで読み込む必要のない中継ログは、有効期限を過ぎるとDMにより削除されます。このパラメータが指定されていない場合、自動パージは実行されません。 | `0`    |
| `remain-space` | ディスクの空き容量の最小量をギガバイト単位で設定します。使用可能なディスク容量がこの値より小さい場合、DM ワーカーはリレー ログの削除を試行します。                                                    | `15`   |

> **注記：**
>
> 自動データ消去戦略は、 `interval`が 0 ではなく、2 つの構成項目`expires`と`remain-space`の少なくとも 1 つが 0 ではない場合にのみ有効になります。

### タスクステータスチェッカーの設定 ( <code>checker</code> ) {#task-status-checker-configuration-code-checker-code}

DM は現在のタスクのステータスとエラー メッセージを定期的にチェックし、タスクを再開するとエラーが解消されるかどうかを判断します。必要に応じて、DM はタスクの再開を自動的に再試行します。 DM は、指数バックオフ戦略を使用してチェック間隔を調整します。以下の設定により動作を調整できます。

| パラメータ              | 説明                                                            |
| :----------------- | :------------------------------------------------------------ |
| `check-enable`     | この機能を有効にするかどうか。                                               |
| `backoff-rollback` | バックオフ戦略の現在のチェック間隔がこの値より大きく、タスクのステータスが正常である場合、DM は間隔を減らそうとします。 |
| `backoff-max`      | バックオフ戦略のチェック間隔の最大値は 1 秒より大きくなければなりません。                        |

### Binlogイベントフィルター {#binlog-event-filter}

DM v2.0.2 以降、ソース構成ファイルでbinlogイベント フィルターを構成できるようになりました。

| パラメータ            | 説明                                                                                                                       |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `case-sensitive` | フィルタリング ルールで大文字と小文字が区別されるかどうかを決定します。デフォルト値は`false`です。                                                                    |
| `filters`        | binlogイベントフィルタリングルールを設定します。詳細は[Binlogイベントフィルターパラメーターの説明](/dm/dm-binlog-event-filter.md#parameter-descriptions)を参照してください。 |
