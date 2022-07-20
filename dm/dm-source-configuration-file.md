---
title: Upstream Database Configuration File
summary: Learn the configuration file of the upstream database
---

# アップストリームデータベースConfiguration / コンフィグレーションファイル {#upstream-database-configuration-file}

このドキュメントでは、アップストリームデータベースの構成ファイルを紹介します。これには、構成ファイルテンプレートと、このファイルの各構成パラメーターの説明が含まれます。

## Configuration / コンフィグレーションファイルテンプレート {#configuration-file-template}

次に、アップストリームデータベースの構成ファイルテンプレートを示します。

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
> DM v2.0.1では、 `enable-gtid`と`enable-relay`を同時に`true`に設定しないでください。そうしないと、増分データが失われる可能性があります。

## Configuration / コンフィグレーションパラメーター {#configuration-parameters}

このセクションでは、構成ファイルの各構成パラメーターについて説明します。

### グローバル構成 {#global-configuration}

| パラメータ               | 説明                                                                                                                                                                                       |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `source-id`         | MySQLインスタンスIDを表します。                                                                                                                                                                      |
| `enable-gtid`       | GTIDを使用してアップストリームからbinlogをプルするかどうかを決定します。デフォルト値は`false`です。一般に、 `enable-gtid`を手動で構成する必要はありません。ただし、アップストリームデータベースでGTIDが有効になっていて、プライマリ/セカンダリスイッチが必要な場合は、 `enable-gtid`から`true`に設定する必要があります。 |
| `enable-relay`      | リレーログ機能を有効にするかどうかを決定します。デフォルト値は`false`です。 DM v2.0.2以降、この構成アイテムは非推奨になりました。 [リレーログ機能を有効にする](/dm/relay-log.md#start-and-stop-the-relay-log-feature)にするには、代わりに`start-relay`コマンドを使用します。       |
| `relay-binlog-name` | DM-workerがbinlogのプルを開始するファイル名を指定します。たとえば、 `"mysql-bin.000002"` 。 `enable_gtid`が`false`の場合にのみ機能します。このパラメーターが指定されていない場合、DM-workerは最新のbinlogから開始してbinlogをプルします。                             |
| `relay-binlog-gtid` | DMワーカーがbinlogのプルを開始するGTIDを指定します。たとえば、 `"e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849"` 。 `enable_gtid`が`true`の場合にのみ機能します。このパラメーターが指定されていない場合、DM-workerは最新のGTIDから開始してbinlogをプルします。         |
| `relay-dir`         | リレーログディレクトリを指定します。                                                                                                                                                                       |
| `host`              | アップストリームデータベースのホストを指定します。                                                                                                                                                                |
| `port`              | アップストリームデータベースのポートを指定します。                                                                                                                                                                |
| `user`              | アップストリームデータベースのユーザー名を指定します。                                                                                                                                                              |
| `password`          | アップストリームデータベースのユーザーパスワードを指定します。 dmctlで暗号化されたパスワードを使用することをお勧めします。                                                                                                                         |
| `security`          | アップストリームデータベースのTLS構成を指定します。証明書の構成済みファイルパスは、すべてのノードからアクセスできる必要があります。構成されたファイルパスがローカルパスである場合、クラスタのすべてのノードは、各ホストの同じパスに証明書のコピーを格納する必要があります。                                                  |

### リレーログクリーンアップ戦略の構成（ <code>purge</code> ） {#relay-log-cleanup-strategy-configuration-code-purge-code}

通常、大量のリレーログがあり、ディスク容量が不十分でない限り、これらのパラメータを手動で設定する必要はありません。

| パラメータ          | 説明                                                                                                                                  | デフォルト値 |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :----- |
| `interval`     | リレーログの有効期限が定期的にチェックされる時間間隔を秒単位で設定します。                                                                                               | `3600` |
| `expires`      | リレーログの有効期限を時間単位で設定します。リレー処理装置によって書き込まれない、または既存のデータ移行タスクによって読み取る必要のないリレーログは、有効期限を超えるとDMによって削除されます。このパラメーターが指定されていない場合、自動パージは実行されません。 | `0`    |
| `remain-space` | ギガバイト単位で、空きディスク容量の最小量を設定します。使用可能なディスク容量がこの値よりも小さい場合、DM-workerはリレーログを削除しようとします。                                                      | `15`   |

> **ノート：**
>
> 自動データパージ戦略は、 `interval`が0でなく、2つの構成項目`expires`および`remain-space`の少なくとも1つが0でない場合にのみ有効になります。

### タスクステータスチェッカー構成（ <code>checker</code> ） {#task-status-checker-configuration-code-checker-code}

DMは、現在のタスクのステータスとエラーメッセージを定期的にチェックして、タスクを再開することでエラーが解消されるかどうかを判断します。必要に応じて、DMは自動的に再試行してタスクを再開します。 DMは、指数バックオフ戦略を使用してチェック間隔を調整します。その動作は、次の構成で調整できます。

| パラメータ              | 説明                                                            |
| :----------------- | :------------------------------------------------------------ |
| `check-enable`     | この機能を有効にするかどうか。                                               |
| `backoff-rollback` | バックオフ戦略の現在のチェック間隔がこの値よりも大きく、タスクステータスが正常である場合、DMは間隔を短くしようとします。 |
| `backoff-max`      | バックオフ戦略のチェック間隔の最大値は、1秒より大きくなければなりません。                         |

### Binlogイベントフィルター {#binlog-event-filter}

DM v2.0.2以降では、ソース構成ファイルでbinlogイベントフィルターを構成できます。

| パラメータ            | 説明                                                                                                                       |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `case-sensitive` | フィルタリングルールで大文字と小文字が区別されるかどうかを決定します。デフォルト値は`false`です。                                                                     |
| `filters`        | binlogイベントフィルタリングルールを設定します。詳細については、 [Binlogイベントフィルターパラメーターの説明](/dm/dm-key-features.md#parameter-explanation-2)を参照してください。 |
