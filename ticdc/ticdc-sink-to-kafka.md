---
title: Replicate Data to Kafka
summary: TiCDC を使用して Apache Kafka にデータを複製する方法を学習します。
---

# Kafka にデータを複製する {#replicate-data-to-kafka}

このドキュメントでは、TiCDC を使用して増分データを Apache Kafka に複製する変更フィードを作成する方法について説明します。

## レプリケーションタスクを作成する {#create-a-replication-task}

次のコマンドを実行してレプリケーション タスクを作成します。

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1","opts":{},"create-time":"2023-11-28T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":false,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

-   `--server` : TiCDC クラスター内の任意の TiCDCサーバーのアドレス。
-   `--changefeed-id` : レプリケーション タスクの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。
-   `--sink-uri` : レプリケーションタスクのダウンストリームアドレス。詳細については、 [`kafka`でシンク URI を設定する](#configure-sink-uri-for-kafka)を参照してください。
-   `--start-ts` : 変更フィードの開始 TSO を指定します。この TSO から、TiCDC クラスターはデータのプルを開始します。デフォルト値は現在の時刻です。
-   `--target-ts` : 変更フィード終了 TSO を指定します。この TSO まで、TiCDC クラスターはデータのプルを停止します。デフォルト値は空です。つまり、TiCDC はデータのプルを自動的に停止しません。
-   `--config` : changefeed設定ファイルを指定します。詳細については[TiCDC Changefeedコンフィグレーションパラメータ](/ticdc/ticdc-changefeed-config.md)を参照してください。

## サポートされている Kafka バージョン {#supported-kafka-versions}

次の表は、各 TiCDC バージョンでサポートされる最小 Kafka バージョンを示しています。

| TiCDC バージョン                    | サポートされている最小の Kafka バージョン |
| :----------------------------- | :----------------------- |
| TiCDC &gt;= v8.1.0             | 2.1.0                    |
| v7.6.0 &lt;= TiCDC &lt; v8.1.0 | 2.4.0                    |
| v7.5.2 &lt;= TiCDC &lt; v8.0.0 | 2.1.0                    |
| v7.5.0 &lt;= TiCDC &lt; v7.5.2 | 2.4.0                    |
| v6.5.0 &lt;= TiCDC &lt; v7.5.0 | 2.1.0                    |
| v6.1.0 &lt;= TiCDC &lt; v6.5.0 | 2.0.0                    |

## Kafka のシンク URI を構成する {#configure-sink-uri-for-kafka}

シンク URI は、TiCDC ターゲット システムの接続情報を指定するために使用されます。形式は次のとおりです。

```shell
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

サンプル構成:

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

以下は、Kafka に設定できるシンク URI パラメータと値の説明です。

| パラメータ/パラメータ値                         | 説明                                                                                                                                                                                                                                                                                                                                                                                                                     |
| :----------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `127.0.0.1`                          | ダウンストリーム Kafka サービスの IP アドレス。                                                                                                                                                                                                                                                                                                                                                                                          |
| `9092`                               | ダウンストリーム Kafka のポート。                                                                                                                                                                                                                                                                                                                                                                                                   |
| `topic-name`                         | 変数。Kafka トピックの名前。                                                                                                                                                                                                                                                                                                                                                                                                      |
| `kafka-version`                      | ダウンストリーム Kafka のバージョン。この値は、ダウンストリーム Kafka の実際のバージョンと一致している必要があります。                                                                                                                                                                                                                                                                                                                                                     |
| `kafka-client-id`                    | レプリケーション タスクの Kafka クライアント ID を指定します (オプション。デフォルトは`TiCDC_sarama_producer_replication ID` )。                                                                                                                                                                                                                                                                                                                            |
| `partition-num`                      | ダウンストリーム Kafka パーティションの数 (オプション。値は実際のパーティション数**以下に**する必要があります。そうでない場合、レプリケーション タスクを正常に作成できません。デフォルトは`3` )。                                                                                                                                                                                                                                                                                                             |
| `max-message-bytes`                  | Kafka ブローカーに毎回送信されるデータの最大サイズ (オプション、デフォルトは`10MB` )。v5.0.6 および v4.0.6 から、デフォルト値は`64MB`と`256MB`から`10MB`に変更されました。                                                                                                                                                                                                                                                                                                         |
| `replication-factor`                 | 保存できる Kafka メッセージ レプリカの数 (オプション、デフォルトは`1` )。この値は、Kafka の値[`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas)以上である必要があります。                                                                                                                                                                                                                                        |
| `required-acks`                      | `Produce`リクエストで使用されるパラメータ。ブローカーが応答する前に受信する必要があるレプリカ確認応答の数を通知します。値のオプションは、 `0` ( `NoResponse` : 応答なし、 `TCP ACK`のみが提供されます)、 `1` ( `WaitForLocal` : ローカルコミットが正常に送信された後にのみ応答します)、および`-1` ( `WaitForAll` : すべてのレプリケートされたレプリカが正常にコミットされた後に応答します。ブローカーの[`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas)構成項目を使用して、レプリケートされたレプリカの最小数を設定できます) です。(オプション、デフォルト値は`-1`です)。 |
| `compression`                        | メッセージを送信するときに使用する圧縮アルゴリズム (値のオプションは`none` 、 `lz4` 、 `gzip` 、 `snappy` 、 `zstd`で、デフォルトは`none`です)。Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。Snappy 圧縮の他のバリアントはサポートされていません。                                                                                                                                                                                                              |
| `protocol`                           | メッセージが Kafka に出力されるプロトコル。値のオプションは`canal-json` 、 `open-protocol` 、 `avro`です。                                                                                                                                                                                                                                                                                                                                            |
| `auto-create-topic`                  | 渡された`topic-name` Kafka クラスターに存在しない場合に、TiCDC がトピックを自動的に作成するかどうかを決定します (オプション、デフォルトは`true` )。                                                                                                                                                                                                                                                                                                                            |
| `enable-tidb-extension`              | オプション。デフォルトは`false` 。出力プロトコルが`canal-json`の場合、値が`true`であれば、TiCDC は[ウォーターマークイベント](/ticdc/ticdc-canal-json.md#watermark-event)を送信し、 [TiDB拡張フィールド](/ticdc/ticdc-canal-json.md#tidb-extension-field)を Kafka メッセージに追加します。v6.1.0 以降では、このパラメータは`avro`プロトコルにも適用されます。値が`true`の場合、TiCDC は[3つのTiDB拡張フィールド](/ticdc/ticdc-avro-protocol.md#tidb-extension-fields) Kafka メッセージに追加します。                                                 |
| `max-batch-size`                     | v4.0.9 の新機能。メッセージ プロトコルが 1 つの Kafka メッセージに複数のデータ変更を出力することをサポートしている場合、このパラメーターは 1 つの Kafka メッセージ内のデータ変更の最大数を指定します。現在、Kafka の`protocol`が`open-protocol` (オプション、デフォルトは`16` ) の場合にのみ有効になります。                                                                                                                                                                                                                               |
| `enable-tls`                         | ダウンストリーム Kafka インスタンスに接続するために TLS を使用するかどうか (オプション、デフォルトは`false` )。                                                                                                                                                                                                                                                                                                                                                    |
| `ca`                                 | ダウンストリーム Kafka インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                |
| `cert`                               | ダウンストリーム Kafka インスタンスに接続するために必要な証明書ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                    |
| `key`                                | ダウンストリーム Kafka インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                 |
| `insecure-skip-verify`               | ダウンストリーム Kafka インスタンスに接続するときに証明書の検証をスキップするかどうか (オプション、デフォルトは`false` )。                                                                                                                                                                                                                                                                                                                                                 |
| `sasl-user`                          | ダウンストリーム Kafka インスタンスに接続するために必要な SASL/PLAIN または SASL/SCRAM 認証の ID (authcid) (オプション)。                                                                                                                                                                                                                                                                                                                                   |
| `sasl-password`                      | ダウンストリーム Kafka インスタンスに接続するために必要な SASL/PLAIN または SASL/SCRAM 認証のパスワード (オプション)。特殊文字が含まれている場合は、URL エンコードする必要があります。                                                                                                                                                                                                                                                                                                         |
| `sasl-mechanism`                     | ダウンストリーム Kafka インスタンスに接続するために必要な SASL 認証の名前。値は`plain` 、 `scram-sha-256` 、 `scram-sha-512` 、または`gssapi`になります。                                                                                                                                                                                                                                                                                                           |
| `sasl-gssapi-auth-type`              | gssapi 認証タイプ。値は`user`または`keytab` (オプション) です。                                                                                                                                                                                                                                                                                                                                                                           |
| `sasl-gssapi-keytab-path`            | gssapi キータブ パス (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                |
| `sasl-gssapi-kerberos-config-path`   | gssapi kerberos 構成パス (オプション)。                                                                                                                                                                                                                                                                                                                                                                                          |
| `sasl-gssapi-service-name`           | gssapi サービス名 (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                  |
| `sasl-gssapi-user`                   | gssapi 認証のユーザー名 (オプション)。                                                                                                                                                                                                                                                                                                                                                                                               |
| `sasl-gssapi-password`               | gssapi 認証のパスワード (オプション)。特殊文字が含まれている場合は、URL エンコードする必要があります。                                                                                                                                                                                                                                                                                                                                                             |
| `sasl-gssapi-realm`                  | gssapi レルム名 (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                   |
| `sasl-gssapi-disable-pafxfast`       | gssapi PA-FX-FAST を無効にするかどうか (オプション)。                                                                                                                                                                                                                                                                                                                                                                                  |
| `dial-timeout`                       | ダウンストリーム Kafka との接続を確立する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                                                                                                                                       |
| `read-timeout`                       | ダウンストリーム Kafka から返される応答を取得する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                                                                                                                                   |
| `write-timeout`                      | ダウンストリーム Kafka にリクエストを送信する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                                                                                                                                     |
| `avro-decimal-handling-mode`         | `avro`プロトコルでのみ有効です。Avro が DECIMAL フィールドを処理する方法を決定します。値は`string`または`precise`で、DECIMAL フィールドを文字列または正確な浮動小数点数にマッピングすることを示します。                                                                                                                                                                                                                                                                                             |
| `avro-bigint-unsigned-handling-mode` | `avro`プロトコルでのみ有効です。Avro が BIGINT UNSIGNED フィールドを処理する方法を決定します。値は`string`または`long`で、BIGINT UNSIGNED フィールドを 64 ビットの符号付き数値または文字列にマッピングすることを示します。                                                                                                                                                                                                                                                                           |

### ベストプラクティス {#best-practices}

-   独自の Kafka Topic を作成することをお勧めします。少なくとも、Topic が Kafka ブローカーに送信できる各メッセージの最大データ量と、下流の Kafka パーティションの数を設定する必要があります。changefeed を作成する場合、これら 2 つの設定はそれぞれ`max-message-bytes`と`partition-num`に対応します。
-   まだ存在しないトピックで changefeed を作成すると、TiCDC は`partition-num`と`replication-factor`パラメータを使用してトピックを作成しようとします。これらのパラメータを明示的に指定することをお勧めします。
-   ほとんどの場合、 `canal-json`プロトコルを使用することをお勧めします。

> **注記：**
>
> `protocol`が`open-protocol`の場合、TiCDC は長さが`max-message-bytes`超えるメッセージを生成しないようにします。ただし、行が非常に大きく、単一の変更だけで長さが`max-message-bytes`を超える場合は、サイレント エラーを回避するために、TiCDC はこのメッセージを出力し、ログに警告を出力。

### TiCDCはKafkaの認証と認可を使用します {#ticdc-uses-the-authentication-and-authorization-of-kafka}

以下は、Kafka SASL 認証を使用する場合の例です。

-   SASL/プレーン

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-user=alice-user&sasl-password=alice-secret&sasl-mechanism=plain"
    ```

-   SASL/SCRAM

    SCRAM-SHA-256 と SCRAM-SHA-512 は PLAIN 方式に似ています。対応する認証方法として`sasl-mechanism`指定するだけです。

-   SASL/GSSAPI

    SASL/GSSAPI `user`認証:

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=user&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-password=alice-secret&sasl-gssapi-realm=example.com"
    ```

    `sasl-gssapi-user`と`sasl-gssapi-realm`の値は、Kerberos で指定された[原理](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html)に関連しています。たとえば、プリンシパルが`alice/for-kafka@example.com`に設定されている場合、 `sasl-gssapi-user`と`sasl-gssapi-realm`それぞれ`alice/for-kafka`と`example.com`として指定されます。

    SASL/GSSAPI `keytab`認証:

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=keytab&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-keytab-path=/var/lib/secret/alice.key&sasl-gssapi-realm=example.com"
    ```

    SASL/GSSAPI 認証方式の詳細については、 [GSSAPI の設定](https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html)参照してください。

-   TLS/SSL暗号化

    Kafka ブローカーで TLS/SSL 暗号化が有効になっている場合は、 `--sink-uri`に`-enable-tls=true`パラメータを追加する必要があります。自己署名証明書を使用する場合は、 `--sink-uri`に`ca` 、 `cert` 、および`key`指定する必要があります。

-   ACL 認証

    TiCDC が適切に機能するために必要な最小限の権限セットは次のとおりです。

    -   トピック[リソースタイプ](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)の`Create` 、 `Write` 、および`Describe`権限。
    -   クラスタリソース タイプに対する`DescribeConfigs`権限。

### TiCDC を Kafka Connect (Confluent Platform) と統合する {#integrate-ticdc-with-kafka-connect-confluent-platform}

Confluent が提供する[データコネクタ](https://docs.confluent.io/current/connect/managing/connectors.html)を使用してリレーショナル データベースまたは非リレーショナル データベースにデータをストリーミングするには、 `avro`プロトコルを使用し、 `schema-registry`で[Confluent スキーマ レジストリ](https://www.confluent.io/product/confluent-platform/data-compatibility/)の URL を指定する必要があります。

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

詳細な統合ガイドについては、 [TiDB と Confluent Platform の統合に関するクイック スタート ガイド](/ticdc/integrate-confluent-using-ticdc.md)参照してください。

### TiCDC を AWS Glue スキーマレジストリと統合する {#integrate-ticdc-with-aws-glue-schema-registry}

v7.4.0 以降、TiCDC は、ユーザーがデータ レプリケーションに Avro プロトコルを選択した場合に、スキーマ レジストリとして[AWS Glue スキーマレジストリ](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html)を使用することをサポートします。構成例は次のとおりです。

```shell
./cdc cli changefeed create --server=127.0.0.1:8300 --changefeed-id="kafka-glue-test" --sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --config changefeed_glue.toml
```

```toml
[sink]
[sink.kafka-config.glue-schema-registry-config]
region="us-west-1"  
registry-name="ticdc-test"
access-key="xxxx"
secret-access-key="xxxx"
token="xxxx"
```

上記の設定では、 `region`と`registry-name`必須フィールドですが、 `access-key` 、 `secret-access-key` 、 `token`はオプションフィールドです。ベストプラクティスは、AWS 認証情報を環境変数として設定するか、changefeed 設定ファイルで設定するのではなく、 `~/.aws/credentials`ファイルに保存することです。

詳細については、 [Go V2 向け公式 AWS SDK ドキュメント](https://aws.github.io/aws-sdk-go-v2/docs/configuring-sdk/#specifying-credentials)を参照してください。

## Kafka シンクのトピックおよびパーティションディスパッチャーのルールをカスタマイズする {#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink}

### マッチャールール {#matcher-rules}

`dispatchers`の次の構成を例に挙げます。

```toml
[sink]
dispatchers = [
  {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
  {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
  {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
  {matcher = ['test6.*'], partition = "ts"}
]
```

-   マッチャー ルールに一致するテーブルについては、対応するトピック式で指定されたポリシーに従ってディスパッチされます。たとえば、 `test3.aa`テーブルは「トピック式 2」に従ってディスパッチされ、 `test5.aa`テーブルは「トピック式 3」に従ってディスパッチされます。
-   複数のマッチャールールに一致するテーブルの場合、最初に一致するトピック式に従ってディスパッチされます。たとえば、 `test1.aa`テーブルは「トピック式 1」に従ってディスパッチされます。
-   どのマッチャールールにも一致しないテーブルの場合、対応するデータ変更イベントは`--sink-uri`で指定されたデフォルトのトピックに送信されます。たとえば、 `test10.aa`テーブルはデフォルトのトピックに送信されます。
-   マッチャー ルールに一致するがトピック ディスパッチャーを指定していないテーブルの場合、対応するデータ変更は`--sink-uri`で指定されたデフォルト トピックに送信されます。たとえば、 `test6.aa`テーブルはデフォルト トピックに送信されます。

### トピックディスパッチャ {#topic-dispatchers}

topic = &quot;xxx&quot; を使用してトピック ディスパッチャーを指定し、トピック式を使用して柔軟なトピック ディスパッチ ポリシーを実装できます。トピックの合計数は 1000 未満にすることをお勧めします。

Topic 式の形式は`[prefix][{schema}][middle][{table}][suffix]`です。

-   `prefix` : オプション。トピック名のプレフィックスを示します。
-   `[{schema}]` : オプション。スキーマ名を一致させるために使用されます。
-   `middle` : オプション。スキーマ名とテーブル名の間の区切り文字を示します。
-   `{table}` : オプション。テーブル名を一致させるために使用されます。
-   `suffix` : オプション。トピック名の接尾辞を示します。

`prefix` 、 `middle` 、 `suffix`は、 `a-z` 、 `A-Z` 、 `0-9` 、 `.` 、 `_` 、 `-`の文字のみを含めることができます。 `{schema}`と`{table}`両方とも小文字です。 `{Schema}`や`{TABLE}`などのプレースホルダーは無効です。

いくつかの例：

-   `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    -   `test1.table1`に対応するデータ変更イベントは、 `hello_test1_table1`という名前のトピックに送信されます。
    -   `test2.table2`に対応するデータ変更イベントは、 `hello_test2_table2`という名前のトピックに送信されます。
-   `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    -   `test3`内のすべてのテーブルに対応するデータ変更イベントは、 `hello_test3_world`という名前のトピックに送信されます。
    -   `test4`内のすべてのテーブルに対応するデータ変更イベントは、 `hello_test4_world`という名前のトピックに送信されます。
-   `matcher = ['test5.*, 'test6.*'], topic = "hard_code_topic_name"`
    -   `test5`と`test6`のすべてのテーブルに対応するデータ変更イベントは、 `hard_code_topic_name`名前のトピックに送信されます。トピック名を直接指定できます。
-   `matcher = ['*.*'], topic = "{schema}_{table}"`
    -   TiCDC がリッスンするすべてのテーブルは、「schema_table」ルールに従って個別のトピックにディスパッチされます。たとえば、 `test.account`テーブルの場合、TiCDC はデータ変更ログを`test_account`という名前のトピックにディスパッチします。

### DDLイベントをディスパッチする {#dispatch-ddl-events}

#### スキーマレベルの DDL {#schema-level-ddls}

特定のテーブルに関連しない DDL は、 `create database`や`drop database`などのスキーマ レベル DDL と呼ばれます。スキーマ レベル DDL に対応するイベントは、 `--sink-uri`で指定されたデフォルト トピックに送信されます。

#### テーブルレベルの DDL {#table-level-ddls}

特定のテーブルに関連する DDL は、 `alter table`や`create table`などのテーブル レベル DDL と呼ばれます。テーブル レベル DDL に対応するイベントは、ディスパッチャ構成に従って対応するトピックに送信されます。

たとえば、 `matcher = ['test.*'], topic = {schema}_{table}`ようなディスパッチャーの場合、DDL イベントは次のようにディスパッチされます。

-   DDL イベントに 1 つのテーブルが関係している場合、DDL イベントはそのまま対応するトピックに送信されます。たとえば、DDL イベント`drop table test.table1`の場合、イベントは`test_table1`という名前のトピックに送信されます。
-   DDL イベントに複数のテーブルが関係する場合 ( `rename table` / `drop table` / `drop view`には複数のテーブルが関係する可能性があります)、DDL イベントは複数のイベントに分割され、対応するトピックに送信されます。たとえば、DDL イベント`rename table test.table1 to test.table10, test.table2 to test.table20`の場合、イベント`rename table test.table1 to test.table10`はトピック`test_table1`に送信され、イベント`rename table test.table2 to test.table20`はトピック`test.table2`に送信されます。

### パーティションディスパッチャ {#partition-dispatchers}

`partition = "xxx"`使用してパーティション ディスパッチャーを指定できます。 `default` 、 `index-value` 、 `columns` 、 `table` 、および`ts` 5 つのディスパッチャーがサポートされています。ディスパッチャーのルールは次のとおりです。

-   `default` : デフォルトで`table`ディスパッチャ ルールを使用します。スキーマ名とテーブル名を使用してパーティション番号を計算し、テーブルのデータが同じパーティションに送信されるようにします。その結果、1 つのテーブルのデータは 1 つのパーティションにのみ存在し、順序付けが保証されます。ただし、このディスパッチャ ルールは送信スループットを制限し、コンシューマーを追加しても消費速度を向上させることはできません。
-   `index-value` : 主キー、一意のインデックス、または`index`で明示的に指定されたインデックスのいずれかを使用してパーティション番号を計算し、テーブル データを複数のパーティションに分散します。1 つのテーブルのデータは複数のパーティションに送信され、各パーティションのデータは順序付けされます。コンシューマーを追加することで、消費速度を向上させることができます。
-   `columns` : 明示的に指定された列の値を使用してパーティション番号を計算し、テーブル データを複数のパーティションに分散します。単一のテーブルのデータは複数のパーティションに送信され、各パーティションのデータは順序付けされます。コンシューマーを追加することで、消費速度を向上させることができます。
-   `table` : スキーマ名とテーブル名を使用してパーティション番号を計算します。
-   `ts` : 行変更の commitTs を使用してパーティション番号を計算し、テーブル データを複数のパーティションに分散します。単一のテーブルからのデータは複数のパーティションに送信され、各パーティションのデータは順序付けされます。コンシューマーを追加することで、消費速度を向上させることができます。ただし、データ項目の複数の変更が異なるパーティションに送信され、異なるコンシューマーのコンシューマーの進行状況が異なる場合があり、データの不整合が発生する可能性があります。したがって、コンシューマーは、消費する前に、複数のパーティションからのデータを commitTs で並べ替える必要があります。

`dispatchers`の次の構成を例に挙げます。

```toml
[sink]
dispatchers = [
    {matcher = ['test.*'], partition = "index-value"},
    {matcher = ['test1.*'], partition = "index-value", index = "index1"},
    {matcher = ['test2.*'], partition = "columns", columns = ["id", "a"]},
    {matcher = ['test3.*'], partition = "table"},
]
```

-   `test`データベース内のテーブルは`index-value`ディスパッチャを使用し、主キーまたは一意のインデックスの値を使用してパーティション番号を計算します。主キーが存在する場合は、主キーが使用されます。それ以外の場合は、最短の一意のインデックスが使用されます。
-   `test1`テーブル内のテーブルは`index-value`ディスパッチャを使用し、 `index1`という名前のインデックス内のすべての列の値を使用してパーティション番号を計算します。指定されたインデックスが存在しない場合は、エラーが報告されます。 `index`で指定されたインデックスは一意のインデックスである必要があることに注意してください。
-   `test2`データベース内のテーブルは`columns`ディスパッチャを使用し、列`id`と`a`の値を使用してパーティション番号を計算します。いずれかの列が存在しない場合は、エラーが報告されます。
-   `test3`データベース内のテーブルは`table`ディスパッチャーを使用します。
-   `test4`データベース内のテーブルは、前述のルールのいずれにも一致しないため、 `default`ディスパッチャー、つまり`table`ディスパッチャーを使用します。

テーブルが複数のディスパッチャー ルールに一致する場合、最初に一致するルールが優先されます。

> **注記：**
>
> v6.1.0 以降、構成の意味を明確にするために、パーティション ディスパッチャーを指定するために使用される構成が`dispatcher`から`partition`に変更され、 `partition`は`dispatcher`の別名になりました。たとえば、次の 2 つのルールはまったく同じです。
>
>     [sink]
>     dispatchers = [
>        {matcher = ['*.*'], dispatcher = "index-value"},
>        {matcher = ['*.*'], partition = "index-value"},
>     ]
>
> ただし、 `dispatcher`と`partition`同じルールに出現させることはできません。たとえば、次のルールは無効です。
>
>     {matcher = ['*.*'], dispatcher = "index-value", partition = "table"},

## カラムセレクター {#column-selectors}

列セレクター機能は、イベントから列を選択し、それらの列に関連するデータの変更のみをダウンストリームに送信することをサポートします。

`column-selectors`の次の構成を例に挙げます。

```toml
[sink]
column-selectors = [
    {matcher = ['test.t1'], columns = ['a', 'b']},
    {matcher = ['test.*'], columns = ["*", "!b"]},
    {matcher = ['test1.t1'], columns = ['column*', '!column1']},
    {matcher = ['test3.t'], columns = ["column?", "!column1"]},
]
```

-   表`test.t1`の場合、列`a`と`b`のみが送信されます。
-   `test`データベース内のテーブル ( `t1`テーブルを除く) の場合、 `b`列を除くすべての列が送信されます。
-   表`test1.t1`の場合、 `column1`を除く`column`で始まるすべての列が送信されます。
-   表`test3.t`の場合、 `column1`を除く、 `column`で始まる 7 文字の列が送信されます。
-   どのルールにも一致しないテーブルの場合、すべての列が送信されます。

> **注記：**
>
> `column-selectors`ルールでフィルタリングされた後、テーブル内のデータには、複製される主キーまたは一意のキーが必要です。そうでない場合、変更フィードは作成時または実行時にエラーを報告します。

## 単一の大きなテーブルの負荷を複数の TiCDC ノードにスケールアウトする {#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes}

この機能は、1 つの大きなテーブルのデータ レプリケーション範囲を、データ量と 1 分あたりの変更行数に応じて複数の範囲に分割し、各範囲でレプリケートされるデータ量と変更行数をほぼ同じにします。この機能は、これらの範囲を複数の TiCDC ノードに分散してレプリケーションするため、複数の TiCDC ノードが同時に 1 つの大きなテーブルをレプリケートできます。この機能により、次の 2 つの問題を解決できます。

-   単一の TiCDC ノードでは、単一の大きなテーブルを時間内に複製することはできません。
-   TiCDC ノードによって消費されるリソース (CPU やメモリなど) は均等に分散されません。

> **警告：**
>
> TiCDC v7.0.0 は、Kafka 変更フィード上の大きな単一テーブルの負荷のスケールアウトのみをサポートします。

サンプル構成:

```toml
[scheduler]
# The default value is "false". You can set it to "true" to enable this feature.
enable-table-across-nodes = true
# When you enable this feature, it only takes effect for tables with the number of regions greater than the `region-threshold` value.
region-threshold = 100000
# When you enable this feature, it takes effect for tables with the number of rows modified per minute greater than the `write-key-threshold` value.
# Note:
# * The default value of `write-key-threshold` is 0, which means that the feature does not split the table replication range according to the number of rows modified in a table by default.
# * You can configure this parameter according to your cluster workload. For example, if it is configured as 30000, it means that the feature will split the replication range of a table when the number of modified rows per minute in the table exceeds 30000.
# * When `region-threshold` and `write-key-threshold` are configured at the same time:
#   TiCDC will check whether the number of modified rows is greater than `write-key-threshold` first.
#   If not, next check whether the number of Regions is greater than `region-threshold`.
write-key-threshold = 30000
```

次の SQL ステートメントを使用して、テーブルに含まれるリージョンの数を照会できます。

```sql
SELECT COUNT(*) FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS WHERE DB_NAME="database1" AND TABLE_NAME="table1" AND IS_INDEX=0;
```

## Kafkaトピックの制限を超えるメッセージを処理する {#handle-messages-that-exceed-the-kafka-topic-limit}

Kafka トピックは、受信できるメッセージのサイズに制限を設定します。この制限は、 [`max.message.bytes`](https://kafka.apache.org/documentation/#topicconfigs_max.message.bytes)パラメータによって制御されます。TiCDC Kafka シンクがこの制限を超えるデータを送信すると、変更フィードはエラーを報告し、データのレプリケーションを続行できません。この問題を解決するために、TiCDC は新しい構成`large-message-handle-option`を追加し、次のソリューションを提供します。

現在、この機能は Canal-JSON と Open Protocol の 2 つのエンコード プロトコルをサポートしています。Canal-JSON プロトコルを使用する場合は、 `sink-uri`のうち`enable-tidb-extension=true`指定する必要があります。

### TiCDC データ圧縮 {#ticdc-data-compression}

v7.4.0 以降、TiCDC Kafka シンクは、エンコード直後にデータを圧縮し、圧縮されたデータ サイズをメッセージ サイズ制限と比較することをサポートします。この機能により、サイズ制限を超えるメッセージの発生を効果的に減らすことができます。

構成例は次のとおりです。

```toml
[sink.kafka-config.large-message-handle]
# This configuration is introduced in v7.4.0.
# "none" by default, which means that the compression feature is disabled.
# Possible values are "none", "lz4", and "snappy". The default value is "none".
large-message-handle-compression = "none"
```

この機能は、Kafka プロデューサーの圧縮機能とは異なります。

-   `large-message-handle-compression`で指定された圧縮アルゴリズムは、単一の Kafka メッセージを圧縮します。圧縮は、メッセージ サイズの制限と比較する前に実行されます。
-   `sink-uri`で圧縮アルゴリズムを設定できます。圧縮は、複数の Kafka メッセージを含むデータ送信リクエスト全体に適用されます。圧縮は、メッセージ サイズの制限と比較した後に実行されます。

`large-message-handle-compression`が有効になっている場合、コンシューマーが受信したメッセージは特定の圧縮プロトコルを使用してエンコードされ、コンシューマー アプリケーションは指定された圧縮プロトコルを使用してデータをデコードする必要があります。

### ハンドルキーのみ送信 {#send-handle-keys-only}

v7.3.0 以降、TiCDC Kafka シンクは、メッセージ サイズが制限を超えた場合にハンドル キーのみの送信をサポートします。これにより、メッセージ サイズが大幅に削減され、メッセージ サイズが Kafka トピック制限を超えたために発生する変更フィード エラーやタスクの失敗を回避できます。ハンドル キーとは、次のものを指します。

-   複製するテーブルに主キーがある場合、主キーはハンドル キーになります。
-   テーブルに主キーがなく、NOT NULL 一意キーがある場合、NOT NULL 一意キーがハンドル キーになります。

サンプル構成は次のとおりです。

```toml
[sink.kafka-config.large-message-handle]
# large-message-handle-option is introduced in v7.3.0.
# Defaults to "none". When the message size exceeds the limit, the changefeed fails.
# When set to "handle-key-only", if the message size exceeds the limit, only the handle key is sent in the data field. If the message size still exceeds the limit, the changefeed fails.
large-message-handle-option = "claim-check"
```

### ハンドルキーのみでメッセージを消費する {#consume-messages-with-handle-keys-only}

ハンドル キーのみのメッセージ形式は次のとおりです。

```json
{
    "id": 0,
    "database": "test",
    "table": "tp_int",
    "pkNames": [
        "id"
    ],
    "isDdl": false,
    "type": "INSERT",
    "es": 1639633141221,
    "ts": 1639633142960,
    "sql": "",
    "sqlType": {
        "id": 4
    },
    "mysqlType": {
        "id": "int"
    },
    "data": [
        {
          "id": "2"
        }
    ],
    "old": null,
    "_tidb": {     // TiDB extension fields
        "commitTs": 163963314122145239,
        "onlyHandleKey": true
    }
}
```

Kafka コンシューマーがメッセージを受信すると、まず`onlyHandleKey`フィールドをチェックします。このフィールドが存在し、 `true`である場合、メッセージには完全なデータのハンドル キーのみが含まれていることを意味します。この場合、完全なデータを取得するには、上流の TiDB をクエリして[履歴データを読み取るための`tidb_snapshot`](/read-historical-data.md)を使用する必要があります。

> **警告：**
>
> Kafka コンシューマーがデータを処理し、TiDB にクエリを実行すると、GC によってデータが削除される可能性があります。この状況を回避するには、 [TiDBクラスタのGCライフタイムを変更する](/system-variables.md#tidb_gc_life_time-new-in-v50)より大きい値に設定する必要があります。

### 大きなメッセージを外部storageに送信する {#send-large-messages-to-external-storage}

v7.4.0 以降、TiCDC Kafka シンクは、メッセージ サイズが制限を超えた場合に、大きなメッセージを外部storageに送信することをサポートします。一方、TiCDC は、外部storage内の大きなメッセージのアドレスを含むメッセージを Kafka に送信します。これにより、メッセージ サイズが Kafka トピック制限を超えたために発生する変更フィード障害を回避できます。

構成例は次のとおりです。

```toml
[sink.kafka-config.large-message-handle]
# large-message-handle-option is introduced in v7.3.0.
# Defaults to "none". When the message size exceeds the limit, the changefeed fails.
# When set to "handle-key-only", if the message size exceeds the limit, only the handle key is sent in the data field. If the message size still exceeds the limit, the changefeed fails.
# When set to "claim-check", if the message size exceeds the limit, the message is sent to external storage.
large-message-handle-option = "claim-check"
claim-check-storage-uri = "s3://claim-check-bucket"
```

`large-message-handle-option` `"claim-check"`に設定する場合、 `claim-check-storage-uri`有効な外部storageアドレスに設定する必要があります。そうしないと、変更フィードの作成は失敗します。

> **ヒント**
>
> TiCDC における Amazon S3、GCS、Azure Blob Storage の URI パラメータの詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

TiCDC は外部storageサービス上のメッセージをクリーンアップしません。データ コンシューマーは外部storageサービスを独自に管理する必要があります。

### 外部storageから大きなメッセージを消費する {#consume-large-messages-from-external-storage}

Kafka コンシューマーは、外部storage内の大きなメッセージのアドレスを含むメッセージを受信します。メッセージの形式は次のとおりです。

```json
{
    "id": 0,
    "database": "test",
    "table": "tp_int",
    "pkNames": [
        "id"
    ],
    "isDdl": false,
    "type": "INSERT",
    "es": 1639633141221,
    "ts": 1639633142960,
    "sql": "",
    "sqlType": {
        "id": 4
    },
    "mysqlType": {
        "id": "int"
    },
    "data": [
        {
          "id": "2"
        }
    ],
    "old": null,
    "_tidb": {     // TiDB extension fields
        "commitTs": 163963314122145239,
        "claimCheckLocation": "s3:/claim-check-bucket/${uuid}.json"
    }
}
```

メッセージに`claimCheckLocation`フィールドが含まれている場合、Kafka コンシューマーは、フィールドによって提供されるアドレスに従って、JSON 形式で保存された大きなメッセージ データを読み取ります。メッセージの形式は次のとおりです。

```json
{
  key: "xxx",
  value: "xxx",
}
```

`key`フィールドと`value`フィールドには、エンコードされた大きなメッセージが含まれており、これは Kafka メッセージの対応するフィールドに送信されるはずです。コンシューマーは、これらの 2 つの部分のデータを解析して、大きなメッセージの内容を復元できます。
