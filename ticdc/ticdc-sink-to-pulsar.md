---
title: Replicate Data to Pulsar
summary: TiCDC を使用してデータを Pulsar に複製する方法を学びます。
---

# Pulsarにデータを複製する {#replicate-data-to-pulsar}

このドキュメントでは、TiCDC を使用して増分データを Pulsar に複製する変更フィードを作成する方法について説明します。

## 増分データをPulsarに複製するレプリケーションタスクを作成する {#create-a-replication-task-to-replicate-incremental-data-to-pulsar}

次のコマンドを実行してレプリケーション タスクを作成します。

```shell
cdc cli changefeed create \
    --server=http://127.0.0.1:8300 \
--sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json" \
--config=./t_changefeed.toml \
--changefeed-id="simple-replication-task"
```

```shell

Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7277814241002263370,"namespace":"default","id":"simple-replication-task","sink_uri":"pulsar://127.0.0.1:6650/consumer-test?protocol=canal-json","create_time":"2024-12-26T14:42:32.000904+08:00","start_ts":444203257406423044,"config":{"memory_quota":1073741824,"case_sensitive":false,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"bdr_mode":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["pulsar_test.*"]},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false,"binary_encoding_method":"base64"},"dispatchers":[{"matcher":["pulsar_test.*"],"partition":"","topic":"test_{schema}_{table}"}],"encoder_concurrency":16,"terminator":"\r\n","date_separator":"day","enable_partition_separator":true,"only_output_updated_columns":false,"delete_only_output_handle_key_columns":false,"pulsar_config":{"connection-timeout":30,"operation-timeout":30,"batching-max-messages":1000,"batching-max-publish-delay":10,"send-timeout":30},"advance_timeout":150},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"use_file_backend":false},"scheduler":{"enable_table_across_nodes":false,"region_threshold":100000,"write_key_threshold":0},"integrity":{"integrity_check_level":"none","corruption_handle_level":"warn"}},"state":"normal","creator_version":"v8.1.2","resolved_ts":444203257406423044,"checkpoint_ts":444203257406423044,"checkpoint_time":"2024-12-26 14:42:31.410"}
```

各パラメータの意味は次のとおりです。

-   `--server` : TiCDC クラスター内の TiCDCサーバーのアドレス。
-   `--changefeed-id` : レプリケーション タスクの ID。形式は正規表現`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`と一致する必要があります。ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。
-   `--sink-uri` : レプリケーションタスクのダウンストリームアドレス。2 [シンクURIを使用してPulsarを構成する](#sink-uri)参照してください。
-   `--start-ts` : 変更フィードの開始 TSO。TiCDC クラスターはこの TSO からデータの取得を開始します。デフォルト値は現在の時刻です。
-   `--target-ts` : 変更フィードのターゲット TSO。TiCDC クラスターはこの TSO でデータのプルを停止します。デフォルトでは空であり、TiCDC はデータのプルを自動的に停止しないことを意味します。
-   `--config` : changefeed 構成ファイル。2 [TiCDC チェンジフィード構成パラメータ](/ticdc/ticdc-changefeed-config.md)参照してください。

## Pulsar を構成するには、Sink URI と changefeed config を使用します。 {#use-sink-uri-and-changefeed-config-to-configure-pulsar}

Sink URI を使用して TiCDC ターゲット システムの接続情報を指定し、changefeed config を使用して Pulsar に関連するパラメータを構成できます。

### シンクURI {#sink-uri}

シンク URI は次の形式に従います。

```shell
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

コンフィグレーション例1:

```shell
--sink-uri="pulsar://127.0.0.1:6650/persistent://abc/def/yktest?protocol=canal-json"
```

コンフィグレーション例2:

```shell
--sink-uri="pulsar://127.0.0.1:6650/yktest?protocol=canal-json"
```

URI で設定可能なパラメータは次のとおりです。

| パラメータ                         | 説明                                                                                                                                                                               |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pulsar`                      | 下流の Pulsar のスキーム。値は`pulsar`または`pulsar+ssl`です。                                                                                                                                    |
| `127.0.0.1`                   | ダウンストリーム Pulsar がサービスを提供する IP アドレス。                                                                                                                                              |
| `6650`                        | 下流の Pulsar の接続ポート。                                                                                                                                                               |
| `persistent://abc/def/yktest` | 前の構成例 1 に示されているように、このパラメータは Pulsar のテナント、名前空間、およびトピックを指定するために使用されます。                                                                                                             |
| `yktest`                      | 前の設定例 2 に示すように、指定するトピックが Pulsar のデフォルト テナント`public`のデフォルト名前空間`default`にある場合は、トピック名のみを使用して URI を設定できます (例: `yktest` )。これは、トピックを`persistent://public/default/yktest`として指定するのと同じです。 |

### Changefeed 設定パラメータ {#changefeed-config-parameters}

以下は changefeed 構成パラメータの例です。

```toml
[sink]
# `dispatchers` is used to specify matching rules.
# Note: When the downstream MQ is Pulsar, if the routing rule for `partition` is not specified as any of `ts`, `index-value`, `table`, or `default`, each Pulsar message will be routed using the string you set as the key.
# For example, if you specify the routing rule for a matcher as the string `code`, then all Pulsar messages that match that matcher will be routed with `code` as the key.
# dispatchers = [
#    {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
#    {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
#    {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
#    {matcher = ['test6.*'], partition = "default"},
#    {matcher = ['test7.*'], partition = "test123"}
# ]

# `protocol` is used to specify the protocol format for encoding messages.
# When the downstream is Pulsar, the protocol can only be canal-json.
# protocol = "canal-json"

# The following parameters only take effect when the downstream is Pulsar.
[sink.pulsar-config]
# Authentication on the Pulsar server is done using a token. Specify the value of the token.
authentication-token = "xxxxxxxxxxxxx"
# When you use a token for Pulsar server authentication, specify the path to the file where the token is located.
token-from-file="/data/pulsar/token-file.txt"
# Pulsar uses the basic account and password to authenticate the identity. Specify the account.
basic-user-name="root"
# Pulsar uses the basic account and password to authenticate the identity. Specify the password.
basic-password="password"
# The certificate path on the client, which is required when Pulsar enables the mTLS authentication.
auth-tls-certificate-path="/data/pulsar/certificate"
# The private key path on the client, which is required when Pulsar enables the mTLS authentication.
auth-tls-private-key-path="/data/pulsar/certificate.key"
# The path to the trusted certificate file of the Pulsar TLS authentication, which is required when Pulsar enables the mTLS authentication or TLS encrypted transmission.
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
# The path to the encrypted private key on the client, which is required when Pulsar enables TLS encrypted transmission.
tls-key-file-path="/data/pulsar/tls-key-file"
# The path to the encrypted certificate file on the client, which is required when Pulsar enables TLS encrypted transmission.
tls-certificate-file="/data/pulsar/tls-certificate-file"
# Pulsar oauth2 issuer-url. For more information, see the Pulsar website: https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication
oauth2.oauth2-issuer-url="https://xxxx.auth0.com"
# Pulsar oauth2 audience
oauth2.oauth2-audience="https://xxxx.auth0.com/api/v2/"
# Pulsar oauth2 private-key
oauth2.oauth2-private-key="/data/pulsar/privateKey"
# Pulsar oauth2 client-id
oauth2.oauth2-client-id="0Xx...Yyxeny"
# Pulsar oauth2 oauth2-scope
oauth2.oauth2-scope="xxxx"
# The number of cached Pulsar producers in TiCDC. The value is 10240 by default. Each Pulsar producer corresponds to one topic. If the number of topics you need to replicate is larger than the default value, you need to increase the number.
pulsar-producer-cache-size=10240
# Pulsar data compression method. No compression is used by default. Optional values are "lz4", "zlib", and "zstd".
compression-type=""
# The timeout for the Pulsar client to establish a TCP connection with the server. The value is 5 seconds by default.
connection-timeout=5
# The timeout for Pulsar clients to initiate operations such as creating and subscribing to a topic. The value is 30 seconds by default.
operation-timeout=30
# The maximum number of messages in a single batch for a Pulsar producer to send. The value is 1000 by default.
batching-max-messages=1000
# The interval at which Pulsar producer messages are saved for batching. The value is 10 milliseconds by default.
batching-max-publish-delay=10
# The timeout for a Pulsar producer to send a message. The value is 30 seconds by default.
send-timeout=30
```

### ベストプラクティス {#best-practice}

-   チェンジフィードを作成するときは、 `protocol`パラメータを指定する必要があります。現在、Pulsar へのデータの複製には`canal-json`プロトコルのみがサポートされています。
-   `pulsar-producer-cache-size`パラメータは、Pulsar クライアントにキャッシュされるプロデューサーの数を示します。Pulsar の各プロデューサーは 1 つのトピックにしか対応できないため、TiCDC はプロデューサーをキャッシュするために LRU 方式を採用しており、デフォルトの制限は 10240 です。複製する必要があるトピックの数がデフォルト値より大きい場合は、数を増やす必要があります。

### TLS暗号化送信 {#tls-encrypted-transmission}

v7.5.1 および v8.0.0 以降、TiCDC は Pulsar の TLS 暗号化伝送をサポートします。設定例は次のとおりです。

シンクURI:

```shell
--sink-uri="pulsar+ssl://127.0.0.1:6651/persistent://public/default/yktest?protocol=canal-json"
```

コンフィグレーション：

```toml
[sink.pulsar-config]
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
```

Pulsarサーバーに`tlsRequireTrustedClientCertOnConnect=true`パラメータが設定されている場合は、changefeed 設定ファイルで`tls-key-file-path`と`tls-certificate-file`パラメータも設定する必要があります。例:

```toml
[sink.pulsar-config]
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
tls-certificate-file="/data/pulsar/tls-certificate-file"
tls-key-file-path="/data/pulsar/tls-key-file"
```

### Pulsar の TiCDC 認証と承認 {#ticdc-authentication-and-authorization-for-pulsar}

以下は、Pulsar でトークン認証を使用する場合のサンプル構成です。

-   トークン

    シンクURI:

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    設定パラメータ:

    ```shell
    [sink.pulsar-config]
    authentication-token = "xxxxxxxxxxxxx"
    ```

-   ファイルからのトークン

    シンクURI:

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    設定パラメータ:

    ```toml
    [sink.pulsar-config]
    # Pulsar uses tokens for authentication on the Pulsar server. Specify the path to the token file, which will be read from the TiCDC server.
    token-from-file="/data/pulsar/token-file.txt"
    ```

-   mTLS認証

    シンクURI:

    ```shell
    --sink-uri="pulsar+ssl://127.0.0.1:6651/persistent://public/default/yktest?protocol=canal-json"
    ```

    設定パラメータ:

    ```toml
    [sink.pulsar-config]
    # Certificate path of the Pulsar mTLS authentication
    auth-tls-certificate-path="/data/pulsar/certificate"
    # Private key path of the Pulsar mTLS authentication
    auth-tls-private-key-path="/data/pulsar/certificate.key"
    # Path to the trusted certificate file of the Pulsar mTLS authentication
    tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
    ```

-   OAuth2認証

    v7.5.1 および v8.0.0 以降、TiCDC は Pulsar の OAuth2 認証をサポートします。

    シンクURI:

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    設定パラメータ:

    ```toml
    [sink.pulsar-config]
    # Pulsar oauth2 issuer-url. For more information, see the Pulsar website: https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#oauth2-authentication
    oauth2.oauth2-issuer-url="https://xxxx.auth0.com"
    # Pulsar oauth2 audience
    oauth2.oauth2-audience="https://xxxx.auth0.com/api/v2/"
    # Pulsar oauth2 private-key
    oauth2.oauth2-private-key="/data/pulsar/privateKey"
    # Pulsar oauth2 client-id
    oauth2.oauth2-client-id="0Xx...Yyxeny"
    # Pulsar oauth2 oauth2-scope
    oauth2.oauth2-scope="xxxx"
    ```

## Pulsar Sink のトピックとパーティションのディスパッチルールをカスタマイズする {#customize-the-dispatching-rules-for-topics-and-partitions-in-pulsar-sink}

### Matcherのマッチングルール {#matching-rules-for-matcher}

次のサンプル構成ファイルの`dispatchers`構成項目を例に挙げます。

```toml
[sink]
dispatchers = [
  {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
  {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
  {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
  {matcher = ['test6.*'], partition = "default"},
  {matcher = ['test7.*'], partition = "test123"}
]
```

-   マッチャールールに一致するテーブルは、対応するトピック式で指定されたポリシーに従ってディスパッチされます。たとえば、テーブル`test3.aa` `Topic expression 2`に従ってディスパッチされ、テーブル`test5.aa`は`Topic expression 3`に従ってディスパッチされます。
-   複数のマッチャールールに一致するテーブルの場合、最初に一致するトピック式に従ってディスパッチされます。たとえば、テーブル`test1.aa`は`Topic expression 1`に従ってディスパッチされます。
-   どのマッチャーにも一致しないテーブルの場合、対応するデータ変更イベントは`-sink-uri`で指定されたデフォルトのトピックに送信されます。たとえば、テーブル`test10.aa`はデフォルトのトピックに送信されます。
-   マッチャー ルールに一致するがトピック ディスパッチャーが指定されていないテーブルの場合、対応するデータ変更は`-sink-uri`で指定されたデフォルト トピックに送信されます。たとえば、テーブル`test6.abc`はデフォルト トピックに送信されます。

### トピックディスパッチャ {#topic-dispatcher}

`topic = "xxx"`使用してトピック ディスパッチャーを指定し、トピック式を使用して柔軟なトピック ディスパッチ ポリシーを実装できます。トピックの合計数は 1000 未満にすることをお勧めします。

トピック表現の形式は`[tenant_and_namespace][prefix]{schema}[middle][{table}][suffix]`です。各部分の意味は次のとおりです。

-   `tenant_and_namespace` ：オプション。トピックのテナントと名前空間を表します（例： `persistent://abc/def/` ）。設定されていない場合は、トピックがPulsarのデフォルトテナント`public`の下のデフォルト名前空間`default`にあることを意味します。
-   `prefix` : オプション。トピック名のプレフィックスを表します。
-   `{schema}` : オプション。データベース名を表します。
-   `middle` : オプション。データベース名とテーブル名の間の区切り文字を表します。
-   `{table}` : オプション。テーブル名を表します。
-   `suffix` : オプション。トピック名のサフィックスを表します。

`prefix` 、 `middle` 、 `suffix` 、大文字と小文字 ( `a-z` 、 `A-Z` )、数字 ( `0-9` )、ドット ( `.` )、アンダースコア ( `_` )、ハイフン ( `-` ) のみをサポートします。 `{schema}`と`{table}`小文字にする必要があります。 `{Schema}`や`{TABLE}`などの大文字を含むプレースホルダーは無効です。

以下に例をいくつか示します。

-   `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    -   テーブル`test1.table1`に対応するデータ変更イベントは、 `hello_test1_table1`という名前のトピックに送信されます。
    -   テーブル`test2.table2`に対応するデータ変更イベントは、 `hello_test2_table2`という名前のトピックに送信されます。

-   `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    -   `test3`の下にあるすべてのテーブルのデータ変更イベントは、 `hello_test3_world`という名前のトピックに送信されます。
    -   `test4`の下にあるすべてのテーブルのデータ変更イベントは、 `hello_test4_world`という名前のトピックに送信されます。

-   `matcher = ['*.*'], topic = "{schema}_{table}"`
    -   TiCDC がリッスンするすべてのテーブルは、 `databaseName_tableName`ルールに従って個別のトピックに送信されます。たとえば、テーブル`test.account`の場合、TiCDC はデータ変更ログを`test_account`という名前のトピックに送信します。

### DDLイベントをディスパッチする {#dispatch-ddl-events}

#### データベースレベルのDDLイベント {#database-level-ddl-events}

`CREATE DATABASE`や`DROP DATABASE`のように特定のテーブルに関連しない DDL 文をデータベース レベルの DDL 文と呼びます。データベース レベルの DDL 文に対応するイベントは、 `--sink-uri`で指定したデフォルト トピックにディスパッチされます。

#### テーブルレベルの DDL イベント {#table-level-ddl-events}

`ALTER TABLE`や`CREATE TABLE`のように特定のテーブルに関連するDDL文をテーブルレベルDDL文と呼びます。テーブルレベルDDL文に対応するイベントは、 `dispatchers`の設定に従って適切なトピックにディスパッチされます。

たとえば、 `matcher = ['test.*'], topic = {schema}_{table}`ような`dispatchers`構成の場合、DDL イベントは次のように送信されます。

-   DDL イベントが 1 つのテーブルのみに関係する場合、DDL イベントはそのまま適切なトピックにディスパッチされます。たとえば、DDL イベント`DROP TABLE test.table1`の場合、イベントは`test_table1`という名前のトピックにディスパッチされます。

-   DDL イベントに複数のテーブルが関係する場合 ( `RENAME TABLE` 、 `DROP TABLE` 、および`DROP VIEW`すべて複数のテーブルが関係する可能性があります)、単一の DDL イベントが複数に分割され、適切なトピックにディスパッチされます。たとえば、DDL イベント`RENAME TABLE test.table1 TO test.table10, test.table2 TO test.table20`の場合、処理は次のようになります。

    -   `RENAME TABLE test.table1 TO test.table10`の DDL イベントを`test_table1`という名前のトピックにディスパッチします。
    -   `RENAME TABLE test.table2 TO test.table20`の DDL イベントを`test_table2`という名前のトピックにディスパッチします。

### パーティションディスパッチャ {#partition-dispatcher}

現在、TiCDC は、排他的サブスクリプション モデルを使用してメッセージを消費するコンシューマーのみをサポートしています。つまり、各コンシューマーはトピック内のすべてのパーティションからメッセージを消費できます。

`partition = "xxx"`でパーティションディスパッチャを指定できます。サポートされているパーティションディスパッチは`default` 、 `ts` 、 `index-value` 、および`table` 。他の文字列を入力すると、TiCDC はその文字列を Pulsarサーバーに送信されるメッセージの`key`として渡します。

発送ルールは以下のとおりです。

-   `default` : デフォルトでは、スキーマ名とテーブル名によってイベントがディスパッチされます。これは、 `table`指定した場合と同じです。
-   `ts` : 行変更の commitT を使用してハッシュ計算を実行し、イベントをディスパッチします。
-   `index-value` : テーブルの主キーまたは一意のインデックスの値を使用してハッシュ計算を実行し、イベントをディスパッチします。
-   `table` : スキーマ名とテーブル名を使用してハッシュ計算を実行し、イベントをディスパッチします。
-   その他の自己定義文字列: 自己定義文字列は Pulsar メッセージのキーとして直接使用され、Pulsar プロデューサーはこのキー値をディスパッチに使用します。
