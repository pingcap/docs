---
title: Replicate Data to Kafka
summary: Learn how to replicate data to Apache Kafka using TiCDC.
---

# データを Kafka にレプリケートする {#replicate-data-to-kafka}

このドキュメントでは、TiCDC を使用して増分データを Apache Kafka にレプリケートする変更フィードを作成する方法について説明します。

## レプリケーション タスクを作成する {#create-a-replication-task}

次のコマンドを実行して、レプリケーション タスクを作成します。

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

-   `--changefeed-id` : レプリケーション タスクの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。
-   `--sink-uri` : レプリケーション タスクのダウンストリーム アドレス。詳細については、 [`kafka`でシンク URI を構成する](#configure-sink-uri-for-kafka)を参照してください。
-   `--start-ts` : 変更フィードの開始 TSO を指定します。この TSO から、TiCDC クラスターはデータのプルを開始します。デフォルト値は現在の時刻です。
-   `--target-ts` : changefeed の終了 TSO を指定します。この TSO に対して、TiCDC クラスターはデータのプルを停止します。デフォルト値は空です。これは、TiCDC がデータのプルを自動的に停止しないことを意味します。
-   `--config` : changefeed 構成ファイルを指定します。詳細については、 [TiCDC Changefeedコンフィグレーションパラメータ](/ticdc/ticdc-changefeed-config.md)を参照してください。

## Kafka のシンク URI を構成する {#configure-sink-uri-for-kafka}

シンク URI は、TiCDC ターゲット システムの接続情報を指定するために使用されます。形式は次のとおりです。

```shell
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

サンプル構成:

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

以下は、Kafka 用に構成できるシンク URI パラメーターと値の説明です。

| パラメータ/パラメータ値                         | 説明                                                                                                                                                                                                                                                                          |
| :----------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `127.0.0.1`                          | ダウンストリーム Kafka サービスの IP アドレス。                                                                                                                                                                                                                                               |
| `9092`                               | ダウンストリーム Kafka のポート。                                                                                                                                                                                                                                                        |
| `topic-name`                         | 変数。 Kafka トピックの名前。                                                                                                                                                                                                                                                          |
| `kafka-version`                      | ダウンストリーム Kafka のバージョン (オプション、デフォルトでは`2.4.0`現在、サポートされている最も古い Kafka バージョンは`0.11.0.2`で、最新のものは`3.2.0`です。この値は、ダウンストリーム Kafka の実際のバージョンと一致する必要があります)。                                                                                                                             |
| `kafka-client-id`                    | レプリケーション タスクの Kafka クライアント ID を指定します (オプション。既定では`TiCDC_sarama_producer_replication ID` )。                                                                                                                                                                                   |
| `partition-num`                      | ダウンストリーム Kafka パーティションの数 (オプション。値は実際のパーティション数**を超えては**なりません。そうでない場合、レプリケーション タスクは正常に作成されません。デフォルトでは`3` )。                                                                                                                                                                   |
| `max-message-bytes`                  | 毎回 Kafka ブローカーに送信されるデータの最大サイズ (オプション、デフォルトでは`10MB` )。 v5.0.6 および v4.0.6 から、デフォルト値が`64MB`および`256MB`から`10MB`に変更されました。                                                                                                                                                         |
| `replication-factor`                 | 保存できる Kafka メッセージ レプリカの数 (オプション、既定では`1` )。                                                                                                                                                                                                                                  |
| `compression`                        | メッセージの送信時に使用される圧縮アルゴリズム (値のオプションは`none` 、 `lz4` 、 `gzip` 、 `snappy` 、および`zstd`で、デフォルトでは`none`です)。                                                                                                                                                                           |
| `protocol`                           | メッセージが Kafka に出力されるプロトコル。値のオプションは`canal-json` 、 `open-protocol` 、 `canal` 、 `avro`および`maxwell`です。                                                                                                                                                                           |
| `auto-create-topic`                  | 渡された`topic-name` Kafka クラスターに存在しない場合に、TiCDC が自動的にトピックを作成するかどうかを決定します (オプション、デフォルトでは`true` )。                                                                                                                                                                                |
| `enable-tidb-extension`              | オプション。デフォルトでは`false` 。出力プロトコルが`canal-json`の場合、値が`true`の場合、TiCDC は Resolved イベントを送信し、TiDB 拡張フィールドを Kafka メッセージに追加します。 v6.1.0 から、このパラメーターは`avro`プロトコルにも適用されます。値が`true`の場合、TiCDC は Kafka メッセージに[3 つの TiDB 拡張フィールド](/ticdc/ticdc-avro-protocol.md#tidb-extension-fields)を追加します。 |
| `max-batch-size`                     | v4.0.9 の新機能。メッセージ プロトコルが 1 つの Kafka メッセージへの複数のデータ変更の出力をサポートしている場合、このパラメーターは 1 つの Kafka メッセージ内のデータ変更の最大数を指定します。現在、Kafka の`protocol`が`open-protocol` (オプション、デフォルトでは`16` ) の場合にのみ有効です。                                                                                         |
| `enable-tls`                         | TLS を使用してダウンストリームの Kafka インスタンスに接続するかどうか (オプション、デフォルトでは`false` )。                                                                                                                                                                                                           |
| `ca`                                 | ダウンストリーム Kafka インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)。                                                                                                                                                                                                                     |
| `cert`                               | ダウンストリーム Kafka インスタンスに接続するために必要な証明書ファイルのパス (オプション)。                                                                                                                                                                                                                         |
| `key`                                | ダウンストリーム Kafka インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)。                                                                                                                                                                                                                      |
| `sasl-user`                          | ダウンストリーム Kafka インスタンスに接続するために必要な SASL/PLAIN または SASL/SCRAM 認証の ID (authcid) (オプション)。                                                                                                                                                                                        |
| `sasl-password`                      | ダウンストリーム Kafka インスタンスに接続するために必要な SASL/PLAIN または SASL/SCRAM 認証のパスワード (オプション)。                                                                                                                                                                                                |
| `sasl-mechanism`                     | ダウンストリーム Kafka インスタンスに接続するために必要な SASL 認証の名前。値は`plain` 、 `scram-sha-256` 、 `scram-sha-512` 、または`gssapi`です。                                                                                                                                                                   |
| `sasl-gssapi-auth-type`              | gssapi 認証タイプ。値は`user`または`keytab`です (オプション)。                                                                                                                                                                                                                                 |
| `sasl-gssapi-keytab-path`            | gssapi キータブ パス (オプション)。                                                                                                                                                                                                                                                     |
| `sasl-gssapi-kerberos-config-path`   | gssapi kerberos 構成パス (オプション)。                                                                                                                                                                                                                                               |
| `sasl-gssapi-service-name`           | gssapi サービス名 (オプション)。                                                                                                                                                                                                                                                       |
| `sasl-gssapi-user`                   | gssapi 認証のユーザー名 (オプション)。                                                                                                                                                                                                                                                    |
| `sasl-gssapi-password`               | gssapi 認証のパスワード (オプション)。                                                                                                                                                                                                                                                    |
| `sasl-gssapi-realm`                  | gssapi レルム名 (オプション)。                                                                                                                                                                                                                                                        |
| `sasl-gssapi-disable-pafxfast`       | gssapi PA-FX-FAST を無効にするかどうか (オプション)。                                                                                                                                                                                                                                       |
| `dial-timeout`                       | ダウンストリーム Kafka との接続を確立する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                            |
| `read-timeout`                       | ダウンストリーム Kafka から返された応答を取得する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                        |
| `write-timeout`                      | ダウンストリーム Kafka にリクエストを送信する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                          |
| `avro-decimal-handling-mode`         | `avro`プロトコルでのみ有効です。 Avro が DECIMAL フィールドを処理する方法を決定します。値は`string`または`precise`で、DECIMAL フィールドを文字列または正確な浮動小数点数にマッピングすることを示します。                                                                                                                                                 |
| `avro-bigint-unsigned-handling-mode` | `avro`プロトコルでのみ有効です。 Avro が BIGINT UNSIGNED フィールドを処理する方法を決定します。値は`string`または`long`で、BIGINT UNSIGNED フィールドを 64 ビットの符号付き数値または文字列にマッピングすることを示します。                                                                                                                               |

### ベストプラクティス {#best-practices}

-   独自の Kafka トピックを作成することをお勧めします。少なくとも、トピックが Kafka ブローカーに送信できる各メッセージの最大データ量と、ダウンストリーム Kafka パーティションの数を設定する必要があります。 changefeed を作成すると、これら 2 つの設定はそれぞれ`max-message-bytes`と`partition-num`に対応します。
-   まだ存在しないトピックで変更フィードを作成すると、TiCDC は`partition-num`と`replication-factor`パラメーターを使用してトピックを作成しようとします。これらのパラメーターを明示的に指定することをお勧めします。
-   ほとんどの場合、 `canal-json`プロトコルを使用することをお勧めします。

> **ノート：**
>
> `protocol`が`open-protocol`の場合、TiCDC は長さが`max-message-bytes`を超えるメッセージの生成を回避しようとします。ただし、1 つの変更だけで長さが`max-message-bytes`を超える行が非常に大きい場合、TiCDC はサイレント エラーを回避するために、このメッセージを出力しようとし、ログに警告を出力。

### TiCDC は Kafka の認証と承認を使用します {#ticdc-uses-the-authentication-and-authorization-of-kafka}

以下は、Kafka SASL 認証を使用する場合の例です。

-   SASL/プレーン

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-user=alice-user&sasl-password=alice-secret&sasl-mechanism=plain"
    ```

-   SASL/スクラム

    SCRAM-SHA-256 と SCRAM-SHA-512 は PLAIN メソッドに似ています。対応する認証方法として`sasl-mechanism`を指定するだけです。

-   SASL/GSSAPI

    SASL/GSSAPI `user`認証:

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=user&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-password=alice-secret&sasl-gssapi-realm=example.com"
    ```

    `sasl-gssapi-user`と`sasl-gssapi-realm`の値は、kerberos で指定された[原理](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html)に関連しています。たとえば、原則が`alice/for-kafka@example.com`に設定されている場合、 `sasl-gssapi-user`と`sasl-gssapi-realm`それぞれ`alice/for-kafka`と`example.com`として指定されます。

    SASL/GSSAPI `keytab`認証:

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=keytab&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-keytab-path=/var/lib/secret/alice.key&sasl-gssapi-realm=example.com"
    ```

    SASL/GSSAPI 認証方式の詳細については、 [GSSAPI の設定](https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html)を参照してください。

-   TLS/SSL 暗号化

    Kafka ブローカーで TLS/SSL 暗号化が有効になっている場合は、 `-enable-tls=true`パラメーターを`--sink-uri`に追加する必要があります。自己署名証明書を使用する場合は、 `--sink-uri`で`ca` 、 `cert` 、および`key`も指定する必要があります。

-   ACL 認可

    TiCDC が適切に機能するために必要な最小限のアクセス許可セットは次のとおりです。

    -   トピック[リソースタイプ](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)の`Create`と`Write`アクセス許可。
    -   クラスタリソース タイプの`DescribeConfigs`アクセス許可。

### TiCDC を Kafka Connect (コンフルエント プラットフォーム) と統合する {#integrate-ticdc-with-kafka-connect-confluent-platform}

Confluent が提供する[データ コネクタ](https://docs.confluent.io/current/connect/managing/connectors.html)使用してデータをリレーショナル データベースまたは非リレーショナル データベースにストリーミングするには、 `avro`プロトコルを使用して[コンフルエント スキーマ レジストリ](https://www.confluent.io/product/confluent-platform/data-compatibility/) in `schema-registry`の URL を提供する必要があります。

サンプル構成:

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --schema-registry="http://127.0.0.1:8081" --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

詳細な統合ガイドについては、 [TiDB と Confluent Platform の統合に関するクイック スタート ガイド](/ticdc/integrate-confluent-using-ticdc.md)を参照してください。

## Kafka Sink のトピックおよびパーティション ディスパッチャーのルールをカスタマイズする {#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink}

### マッチャーのルール {#matcher-rules}

前のセクションの例では:

-   マッチャー ルールに一致するテーブルについては、対応するトピック式で指定されたポリシーに従ってディスパッチされます。たとえば、 `test3.aa`テーブルは「トピック式 2」に従ってディスパッチされます。 `test5.aa`テーブルは「トピック式 3」に従ってディスパッチされます。
-   複数のマッチャー ルールに一致するテーブルの場合、最初に一致したトピック式に従ってディスパッチされます。たとえば、「トピック表現 1」に従って、 `test1.aa`テーブルが分散されます。
-   どのマッチャー ルールにも一致しないテーブルの場合、対応するデータ変更イベントが`--sink-uri`で指定されたデフォルト トピックに送信されます。たとえば、 `test10.aa`テーブルはデフォルト トピックに送信されます。
-   マッチャー ルールに一致するが、トピック ディスパッチャーが指定されていないテーブルの場合、対応するデータ変更は`--sink-uri`で指定されたデフォルト トピックに送信されます。たとえば、 `test6.aa`テーブルはデフォルト トピックに送信されます。

### トピック ディスパッチャ {#topic-dispatchers}

topic = &quot;xxx&quot; を使用してトピック ディスパッチャを指定し、トピック式を使用して柔軟なトピック ディスパッチ ポリシーを実装できます。トピックの総数は 1000 未満にすることをお勧めします。

Topic 式の形式は`[prefix]{schema}[middle][{table}][suffix]`です。

-   `prefix` : オプション。トピック名のプレフィックスを示します。
-   `{schema}` : 必須。スキーマ名と一致させるために使用されます。
-   `middle` : オプション。スキーマ名とテーブル名の間の区切り文字を示します。
-   `{table}` : オプション。テーブル名と一致させるために使用されます。
-   `suffix` : オプション。トピック名のサフィックスを示します。

`prefix` 、 `middle`および`suffix`には、次の文字のみを含めることができます: `a-z` 、 `A-Z` 、 `0-9` 、 `.` 、 `_` 、および`-` 。 `{schema}`と`{table}`は両方とも小文字です。 `{Schema}`や`{TABLE}`などのプレースホルダーは無効です。

いくつかの例：

-   `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    -   `test1.table1`に対応するデータ変更イベントは、 `hello_test1_table1`という名前のトピックに送信されます。
    -   `test2.table2`に対応するデータ変更イベントは、 `hello_test2_table2`という名前のトピックに送信されます。
-   `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    -   `test3`のすべてのテーブルに対応するデータ変更イベントは、 `hello_test3_world`という名前のトピックに送信されます。
    -   `test4`のすべてのテーブルに対応するデータ変更イベントは、 `hello_test4_world`という名前のトピックに送信されます。
-   `matcher = ['*.*'], topic = "{schema}_{table}"`
    -   TiCDC がリッスンするすべてのテーブルは、「schema_table」ルールに従って個別のトピックにディスパッチされます。たとえば、 `test.account`テーブルの場合、TiCDC はそのデータ変更ログを`test_account`という名前のトピックにディスパッチします。

### DDL イベントのディスパッチ {#dispatch-ddl-events}

#### スキーマレベルの DDL {#schema-level-ddls}

`create database`や`drop database`など、特定のテーブルに関連付けられていない DDL は、スキーマ レベルの DDL と呼ばれます。スキーマレベルの DDL に対応するイベントは、 `--sink-uri`で指定されたデフォルトのトピックに送信されます。

#### テーブルレベルの DDL {#table-level-ddls}

`alter table`や`create table`など、特定のテーブルに関連する DDL はテーブルレベル DDL と呼ばれます。テーブルレベルの DDL に対応するイベントは、ディスパッチャの構成に従って、対応するトピックに送信されます。

たとえば、 `matcher = ['test.*'], topic = {schema}_{table}`のようなディスパッチャーの場合、DDL イベントは次のようにディスパッチされます。

-   DDL イベントに含まれるテーブルが 1 つの場合、DDL イベントは対応するトピックにそのまま送信されます。たとえば、DDL イベント`drop table test.table1`の場合、イベントは`test_table1`という名前のトピックに送信されます。
-   DDL イベントに複数のテーブルが含まれる場合 ( `rename table` / `drop table` / `drop view`は複数のテーブルが含まれる場合があります)、DDL イベントは複数のイベントに分割され、対応するトピックに送信されます。たとえば、DDL イベント`rename table test.table1 to test.table10, test.table2 to test.table20`の場合、イベント`rename table test.table1 to test.table10` `test_table1`という名前のトピックに送信され、イベント`rename table test.table2 to test.table20` `test.table2`という名前のトピックに送信されます。

### 区画ディスパッチャー {#partition-dispatchers}

`partition = "xxx"`使用して、パーティション ディスパッチャーを指定できます。デフォルト、ts、インデックス値、およびテーブルの 4 つのディスパッチャがサポートされています。ディスパッチャのルールは次のとおりです。

-   デフォルト: 複数の一意のインデックス (主キーを含む) が存在する場合、または古い値機能が有効になっている場合、イベントはテーブル モードでディスパッチされます。一意のインデックス (または主キー) が 1 つだけ存在する場合、イベントはインデックス値モードで送出されます。
-   ts: 行変更の commitTs を使用して、イベントをハッシュおよびディスパッチします。
-   index-value: 主キーの値またはテーブルの一意のインデックスを使用して、イベントをハッシュしてディスパッチします。
-   table: テーブルのスキーマ名とテーブル名を使用して、イベントをハッシュしてディスパッチします。

> **ノート：**
>
> v6.1.0 以降、構成の意味を明確にするために、パーティション ディスパッチャを指定するために使用される構成が`dispatcher`から`partition`に変更されました`partition`は`dispatcher`のエイリアスです。たとえば、次の 2 つのルールはまったく同じです。
>
> ```
> [sink]
> dispatchers = [
>    {matcher = ['*.*'], dispatcher = "ts"},
>    {matcher = ['*.*'], partition = "ts"},
> ]
> ```
>
> ただし、 `dispatcher`と`partition`同じルールに含めることはできません。たとえば、次のルールは無効です。
>
> ```
> {matcher = ['*.*'], dispatcher = "ts", partition = "table"},
> ```
