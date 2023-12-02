---
title: Replicate Data to Pulsar
summary: Learn how to replicate data to Pulsar using TiCDC.
---

# Pulsar へのデータの複製 {#replicate-data-to-pulsar}

このドキュメントでは、TiCDC を使用して増分データを Pulsar にレプリケートするチェンジフィードを作成する方法について説明します。

## レプリケーション タスクを作成して増分データを Pulsar にレプリケートする {#create-a-replication-task-to-replicate-incremental-data-to-pulsar}

次のコマンドを実行して、レプリケーション タスクを作成します。

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
Info: {"upstream_id":7277814241002263370,"namespace":"default","id":"simple-replication-task","sink_uri":"pulsar://127.0.0.1:6650/consumer-test?protocol=canal-json","create_time":"2023-11-28T14:42:32.000904+08:00","start_ts":444203257406423044,"config":{"memory_quota":1073741824,"case_sensitive":false,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"bdr_mode":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["pulsar_test.*"]},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false,"binary_encoding_method":"base64"},"dispatchers":[{"matcher":["pulsar_test.*"],"partition":"","topic":"test_{schema}_{table}"}],"encoder_concurrency":16,"terminator":"\r\n","date_separator":"day","enable_partition_separator":true,"enable_kafka_sink_v2":false,"only_output_updated_columns":false,"delete_only_output_handle_key_columns":false,"pulsar_config":{"connection-timeout":30,"operation-timeout":30,"batching-max-messages":1000,"batching-max-publish-delay":10,"send-timeout":30},"advance_timeout":150},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"use_file_backend":false},"scheduler":{"enable_table_across_nodes":false,"region_threshold":100000,"write_key_threshold":0},"integrity":{"integrity_check_level":"none","corruption_handle_level":"warn"}},"state":"normal","creator_version":"v7.5.0","resolved_ts":444203257406423044,"checkpoint_ts":444203257406423044,"checkpoint_time":"2023-09-12 14:42:31.410"}
```

各パラメータの意味は次のとおりです。

-   `--server` : TiCDC クラスター内の TiCDCサーバーのアドレス。
-   `--changefeed-id` : レプリケーション タスクの ID。形式は正規表現`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`と一致する必要があります。 ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。
-   `--sink-uri` : レプリケーションタスクの下流アドレス。 [シンク URI を使用して Pulsar を構成する](#sink-uri)を参照してください。
-   `--start-ts` : チェンジフィードの開始 TSO。 TiCDC クラスターは、この TSO からのデータのプルを開始します。デフォルト値は現在時刻です。
-   `--target-ts` : チェンジフィードのターゲット TSO。 TiCDC クラスターは、この TSO でデータのプルを停止します。デフォルトでは空です。これは、TiCDC がデータのプルを自動的に停止しないことを意味します。
-   `--config` : チェンジフィード構成ファイル。 [TiCDC チェンジフィード構成パラメータ](/ticdc/ticdc-changefeed-config.md)を参照してください。

## シンク URI と変更フィード構成を使用して Pulsar を構成する {#use-sink-uri-and-changefeed-config-to-configure-pulsar}

シンク URI を使用して TiCDC ターゲット システムの接続情報を指定し、changefeed config を使用して Pulsar に関連するパラメーターを構成できます。

### シンク URI {#sink-uri}

シンク URI は次の形式に従います。

```shell
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

コンフィグレーション例1：

```shell
--sink-uri="pulsar://127.0.0.1:6650/persistent://abc/def/yktest?protocol=canal-json"
```

コンフィグレーション例2：

```shell
--sink-uri="pulsar://127.0.0.1:6650/yktest?protocol=canal-json"
```

URI で構成可能なパラメータは次のとおりです。

| パラメータ                         | 説明                                                                                                                                                                                    |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `127.0.0.1`                   | ダウンストリーム Pulsar がサービスを提供する IP アドレス。                                                                                                                                                   |
| `6650`                        | ダウンストリーム Pulsar の接続ポート。                                                                                                                                                               |
| `persistent://abc/def/yktest` | 前述の構成例 1 に示すように、このパラメーターは、Pulsar のテナント、名前空間、およびトピックを指定するために使用されます。                                                                                                                    |
| `yktest`                      | 前述の構成例 2 に示すように、指定するトピックが Pulsar のデフォルト テナント`public`のデフォルト ネームスペース`default`にある場合は、トピック名のみを使用して URI を構成できます (例: `yktest` )。これは、トピックを`persistent://public/default/yktest`として指定するのと同じです。 |

### 変更フィード構成パラメータ {#changefeed-config-parameters}

以下は、changefeed 構成パラメーターの例です。

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
# The certificate path for Pulsar TLS encrypted authentication.
auth-tls-certificate-path="/data/pulsar/certificate"
# The private key path for Pulsar TLS encrypted authentication.
auth-tls-private-key-path="/data/pulsar/certificate.key"
# Path to trusted certificate file of the Pulsar TLS encrypted authentication.
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
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

-   変更フィードを作成するときは、 `protocol`パラメーターを指定する必要があります。現在、Pulsar へのデータの複製では`canal-json`プロトコルのみがサポートされています。
-   `pulsar-producer-cache-size`パラメータは、Pulsar クライアントにキャッシュされたプロデューサーの数を示します。 Pulsar の各プロデューサーは 1 つのトピックにのみ対応できるため、TiCDC は LRU 方式を採用してプロデューサーをキャッシュし、デフォルトの制限は 10240 です。複製する必要があるトピックの数がデフォルト値より大きい場合は、その数を増やす必要があります。 。

### Pulsar の TiCDC 認証と認可 {#ticdc-authentication-and-authorization-for-pulsar}

以下は、Pulsar でトークン認証を使用する場合のサンプル構成です。

-   トークン

    シンク URI:

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    設定パラメータ:

    ```shell
    [sink.pulsar-config]
    authentication-token = "xxxxxxxxxxxxx"
    ```

-   ファイルからのトークン

    シンク URI:

    ```shell
    --sink-uri="pulsar://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    設定パラメータ:

    ```toml
    [sink.pulsar-config]
    # Pulsar uses tokens for authentication on the Pulsar server. Specify the path to the token file, which will be read from the TiCDC server.
    token-from-file="/data/pulsar/token-file.txt"
    ```

-   TLS暗号化認証

    シンク URI:

    ```shell
    --sink-uri="pulsar+ssl://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    構成パラメータ:

    ```toml
    [sink.pulsar-config]
    # Certificate path of the Pulsar TLS encrypted authentication
    auth-tls-certificate-path="/data/pulsar/certificate"
    # Private key path of the Pulsar TLS encrypted authentication
    auth-tls-private-key-path="/data/pulsar/certificate.key"
    # Path to trusted certificate file of the Pulsar TLS encrypted authentication
    tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
    ```

-   OAuth2認証

    シンク URI:

    ```shell
    --sink-uri="pulsar+ssl://127.0.0.1:6650/persistent://public/default/yktest?protocol=canal-json"
    ```

    構成パラメータ:

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

## Pulsar シンクのトピックとパーティションのディスパッチ ルールをカスタマイズする {#customize-the-dispatching-rules-for-topics-and-partitions-in-pulsar-sink}

### Matcher のマッチング ルール {#matching-rules-for-matcher}

例として、次のサンプル構成ファイルの`dispatchers`構成項目を取り上げます。

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

-   マッチャー ルールに一致するテーブルは、対応するトピック式で指定されたポリシーに従ってディスパッチされます。たとえば、テーブル`test3.aa`は`Topic expression 2`に従ってディスパッチされ、テーブル`test5.aa`は`Topic expression 3`に従ってディスパッチされます。
-   複数のマッチャー ルールに一致するテーブルの場合、最初に一致したトピック式に従ってテーブルがディスパッチされます。たとえば、テーブル`test1.aa`は`Topic expression 1`に従ってディスパッチされます。
-   どのマッチャーにも一致しないテーブルの場合、対応するデータ変更イベントは`-sink-uri`で指定されたデフォルトのトピックに送信されます。たとえば、テーブル`test10.aa`はデフォルトのトピックに送信されます。
-   マッチャー ルールに一致するがトピック ディスパッチャーが指定されていないテーブルの場合、対応するデータ変更は`-sink-uri`で指定されたデフォルトのトピックに送信されます。たとえば、テーブル`test6.abc`はデフォルトのトピックに送信されます。

### トピックディスパッチャー {#topic-dispatcher}

`topic = "xxx"`を使用してトピック ディスパッチャを指定し、トピック式を使用して柔軟なトピック ディスパッチ ポリシーを実装できます。トピックの総数は 1000 未満にすることをお勧めします。

トピック式の形式は`[prefix]{schema}[middle][{table}][suffix]`です。各部分の意味は次のとおりです。

-   `prefix` : オプション。トピック名のプレフィックスを表します。
-   `{schema}` : オプション。データベース名を表します。
-   `middle` : オプション。データベース名とテーブル名の間の区切り文字を表します。
-   `{table}` : オプション。テーブル名を表します。
-   `suffix` : オプション。トピック名の接尾辞を表します。

`prefix` 、 `middle` 、および`suffix` 、大文字と小文字 ( `a-z` 、 `A-Z` )、数字 ( `0-9` )、ドット ( `.` )、アンダースコア ( `_` )、およびハイフン ( `-` ) のみをサポートします。 `{schema}`と`{table}`小文字でなければなりません。 `{Schema}`や`{TABLE}`などの大文字を含むプレースホルダーは無効です。

以下にいくつかの例を示します。

-   `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    -   テーブル`test1.table1`に対応するデータ変更イベントは、 `hello_test1_table1`という名前のトピックに送出されます。
    -   テーブル`test2.table2`に対応するデータ変更イベントは、 `hello_test2_table2`という名前のトピックに送出されます。

-   `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    -   `test3`の下のすべてのテーブルのデータ変更イベントは、 `hello_test3_world`という名前のトピックに送出されます。
    -   `test4`の下のすべてのテーブルのデータ変更イベントは、 `hello_test4_world`という名前のトピックに送出されます。

-   `matcher = ['*.*'], topic = "{schema}_{table}"`
    -   TiCDC がリッスンするすべてのテーブルについては、ルール`databaseName_tableName`に従って別のトピックにディスパッチされます。たとえば、テーブル`test.account`の場合、TiCDC はデータ変更ログを`test_account`という名前のトピックに送信します。

### DDL イベントをディスパッチする {#dispatch-ddl-events}

#### データベースレベルのDDLイベント {#database-level-ddl-events}

`CREATE DATABASE`や`DROP DATABASE`など、特定のテーブルに関連しない DDL ステートメントは、データベース レベルの DDL ステートメントと呼ばれます。データベースレベルの DDL ステートメントに対応するイベントは、 `--sink-uri`で指定されたデフォルトのトピックにディスパッチされます。

#### テーブルレベルのDDLイベント {#table-level-ddl-events}

特定のテーブルに関連する`ALTER TABLE`や`CREATE TABLE`などの DDL ステートメントは、テーブル レベルの DDL ステートメントと呼ばれます。テーブルレベルの DDL ステートメントに対応するイベントは、 `dispatchers`の構成に従って適切なトピックにディスパッチされます。

たとえば、 `matcher = ['test.*'], topic = {schema}_{table}`のような`dispatchers`構成の場合、DDL イベントは次のように送出されます。

-   DDL イベントに 1 つのテーブルのみが関与する場合、DDL イベントはそのまま適切なトピックにディスパッチされます。たとえば、DDL イベント`DROP TABLE test.table1`の場合、イベントは`test_table1`という名前のトピックにディスパッチされます。

-   DDL イベントに複数のテーブルが関与する場合 ( `RENAME TABLE` 、 `DROP TABLE` 、および`DROP VIEW`はすべて複数のテーブルに関与する可能性があります)、単一の DDL イベントは複数の DDL イベントに分割され、適切なトピックにディスパッチされます。たとえば、DDL イベント`RENAME TABLE test.table1 TO test.table10, test.table2 TO test.table20`の場合、処理は次のようになります。

    -   `RENAME TABLE test.table1 TO test.table10`の DDL イベントを`test_table1`という名前のトピックにディスパッチします。
    -   `RENAME TABLE test.table2 TO test.table20`の DDL イベントを`test_table2`という名前のトピックにディスパッチします。

### パーティションディスパッチャー {#partition-dispatcher}

現在、TiCDC は、コンシューマが排他的サブスクリプション モデルを使用してメッセージを消費することのみをサポートしています。つまり、各コンシューマはトピック内のすべてのパーティションからメッセージを消費できます。

`partition = "xxx"`を使用してパーティション ディスパッチャを指定できます。次のパーティション ディスパッチがサポートされています: `default` 、 `ts` 、 `index-value` 、および`table` 。他の文字列を入力すると、TiCDC はその文字列を Pulsarサーバーに送信されるメッセージのメッセージの`key`として渡します。

派遣ルールは以下の通りです。

-   `default` : デフォルトでは、 `table`を指定した場合と同じスキーマ名とテーブル名によってイベントが送出されます。
-   `ts` : 行変更の commitT を使用してハッシュ計算を実行し、イベントをディスパッチします。
-   `index-value` : テーブルの主キーまたは一意のインデックスの値を使用して、ハッシュ計算を実行し、イベントをディスパッチします。
-   `table` : スキーマ名とテーブル名を使用してハッシュ計算を実行し、イベントをディスパッチします。
-   その他の自己定義文字列: 自己定義文字列は Pulsar メッセージのキーとして直接使用され、Pulsar プロデューサはこのキー値をディスパッチに使用します。
