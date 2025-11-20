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
    --sink-uri="kafka://127.0.0.1:9092,127.0.0.1:9093,127.0.0.1:9094/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"kafka://127.0.0.1:9092,127.0.0.1:9093,127.0.0.1:9094/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1","opts":{},"create-time":"2023-11-28T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":false,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

-   `--server` : TiCDC クラスター内の任意の TiCDCサーバーのアドレス。
-   `--changefeed-id` : レプリケーションタスクのID。形式は正規表現`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`に一致する必要があります。このIDが指定されていない場合、TiCDCは自動的にUUID（バージョン4形式）をIDとして生成します。
-   `--sink-uri` : レプリケーションタスクのダウンストリームアドレス。詳細は[`kafka`でシンクURIを設定する](#configure-sink-uri-for-kafka)参照してください。
-   `--start-ts` : チェンジフィードの開始TSOを指定します。このTSOから、TiCDCクラスターはデータのプルを開始します。デフォルト値は現在時刻です。
-   `--target-ts` : チェンジフィードの終了TSOを指定します。このTSOまで、TiCDCクラスターはデータのプルを停止します。デフォルト値は空で、TiCDCはデータのプルを自動的に停止しません。
-   `--config` : changefeed設定ファイルを指定します。詳細は[TiCDC Changefeedコンフィグレーションパラメータ](/ticdc/ticdc-changefeed-config.md)参照してください。

## サポートされているKafkaのバージョン {#supported-kafka-versions}

次の表は、各 TiCDC バージョンでサポートされる最小の Kafka バージョンを示しています。

| TiCDCバージョン                     | サポートされている最小の Kafka バージョン |
| :----------------------------- | :----------------------- |
| TiCDC &gt;= v8.1.0             | 2.1.0                    |
| v7.6.0 &lt;= TiCDC &lt; v8.1.0 | 2.4.0                    |
| v7.5.2 &lt;= TiCDC &lt; v8.0.0 | 2.1.0                    |
| v7.5.0 &lt;= TiCDC &lt; v7.5.2 | 2.4.0                    |
| v6.5.0 &lt;= TiCDC &lt; v7.5.0 | 2.1.0                    |
| v6.1.0 &lt;= TiCDC &lt; v6.5.0 | 2.0.0                    |

## Kafka のシンク URI を構成する {#configure-sink-uri-for-kafka}

シンクURIは、TiCDCターゲットシステムの接続情報を指定するために使用されます。形式は次のとおりです。

```shell
[scheme]://[host]:[port][/path]?[query_parameters]
```

> **ヒント：**
>
> 下流のKafkaに複数のホストまたはポートがある場合は、シンクURIに複数の`[host]:[port]`設定できます。例：
>
> ```shell
> [scheme]://[host]:[port],[host]:[port],[host]:[port][/path]?[query_parameters]
> ```

サンプル構成:

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

以下は、Kafka に設定できるシンク URI パラメータと値の説明です。

| パラメータ/パラメータ値                         | 説明                                                                                                                                                                                                                                                                                                                                                                                          |
| :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `host`                               | ダウンストリーム Kafka サービスの IP アドレス。                                                                                                                                                                                                                                                                                                                                                               |
| `port`                               | ダウンストリーム Kafka のポート。                                                                                                                                                                                                                                                                                                                                                                        |
| `topic-name`                         | 変数。Kafka トピックの名前。                                                                                                                                                                                                                                                                                                                                                                           |
| `protocol`                           | Kafka にメッセージを出力するプロトコル。値のオプションは[`canal-json`](/ticdc/ticdc-canal-json.md) 、 [`open-protocol`](/ticdc/ticdc-open-protocol.md) 、 [`avro`](/ticdc/ticdc-avro-protocol.md) 、 [`debezium`](/ticdc/ticdc-debezium.md) 、 [`simple`](/ticdc/ticdc-simple-protocol.md)です。                                                                                                                            |
| `kafka-version`                      | ダウンストリーム Kafka のバージョン。この値は、ダウンストリーム Kafka の実際のバージョンと一致している必要があります。                                                                                                                                                                                                                                                                                                                          |
| `kafka-client-id`                    | レプリケーション タスクの Kafka クライアント ID を指定します (オプション。デフォルトは`TiCDC_sarama_producer_replication ID` )。                                                                                                                                                                                                                                                                                                 |
| `partition-num`                      | ダウンストリーム Kafka パーティションの数 (オプション。値は実際のパーティション数**以下に**する必要があります。そうでない場合、レプリケーション タスクを正常に作成できません。デフォルトは`3` )。                                                                                                                                                                                                                                                                                  |
| `max-message-bytes`                  | Kafkaブローカーに毎回送信されるデータの最大サイズ（オプション、デフォルトは`10MB` 、最大値は`100MB` ）。v5.0.6およびv4.0.6以降、デフォルト値は`64MB`および`256MB`から`10MB`に変更されました。                                                                                                                                                                                                                                                                    |
| `replication-factor`                 | 保存できるKafkaメッセージレプリカの数（オプション、デフォルトは`1` ）。この値はKafkaの[`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas)の値である必要があります。                                                                                                                                                                                                                    |
| `required-acks`                      | `Produce`リクエストで使用されるパラメータ。ブローカーが応答するまでに受信する必要があるレプリカ確認応答の数を通知します。値のオプションは`0` ( `NoResponse` : 応答なし、 `TCP ACK`のみ提供)、 `1` ( `WaitForLocal` : ローカルコミットが正常に送信された後にのみ応答)、および`-1` ( `WaitForAll` : すべての複製レプリカが正常にコミットされた後に応答) です。複製レプリカの最小数は、ブローカーの[`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas)設定項目を使用して設定できます。(オプション、デフォルト値は`-1` )。 |
| `compression`                        | メッセージを送信する際に使用する圧縮アルゴリズム（値の選択肢は`none` 、 `lz4` 、 `gzip` 、 `snappy` 、 `zstd` 。デフォルトは`none` ）。Snappy圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他のSnappy圧縮形式はサポートされていません。                                                                                                                                                                                            |
| `auto-create-topic`                  | 渡された`topic-name` Kafka クラスターに存在しない場合に、TiCDC がトピックを自動的に作成するかどうかを決定します (オプション、デフォルトは`true` )。                                                                                                                                                                                                                                                                                                 |
| `enable-tidb-extension`              | オプション。デフォルトは`false` 。出力プロトコルが`canal-json`場合、値が`true`であれば、TiCDC は[ウォーターマークイベント](/ticdc/ticdc-canal-json.md#watermark-event)送信し、Kafka メッセージに[TiDB拡張フィールド](/ticdc/ticdc-canal-json.md#tidb-extension-field)を追加します。v6.1.0 以降では、このパラメータは`avro`プロトコルにも適用されます。値が`true`の場合、TiCDC は Kafka メッセージに[3つのTiDB拡張フィールド](/ticdc/ticdc-avro-protocol.md#tidb-extension-fields)追加します。                          |
| `max-batch-size`                     | v4.0.9 の新機能。メッセージプロトコルが 1 つの Kafka メッセージに複数のデータ変更を出力することをサポートしている場合、このパラメータは 1 つの Kafka メッセージに含まれるデータ変更の最大数を指定します。現在、このパラメータは Kafka の`protocol`が`open-protocol` （オプション、デフォルトは`16` ）の場合にのみ有効です。                                                                                                                                                                                              |
| `enable-tls`                         | ダウンストリーム Kafka インスタンスに接続するために TLS を使用するかどうか (オプション、デフォルトは`false` )。                                                                                                                                                                                                                                                                                                                         |
| `ca`                                 | ダウンストリーム Kafka インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                     |
| `cert`                               | ダウンストリーム Kafka インスタンスに接続するために必要な証明書ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                         |
| `key`                                | ダウンストリーム Kafka インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                      |
| `insecure-skip-verify`               | ダウンストリーム Kafka インスタンスに接続するときに証明書の検証をスキップするかどうか (オプション、デフォルトは`false` )。                                                                                                                                                                                                                                                                                                                      |
| `sasl-user`                          | ダウンストリーム Kafka インスタンスに接続するために必要な SASL/PLAIN または SASL/SCRAM 認証の ID (authcid) (オプション)。                                                                                                                                                                                                                                                                                                        |
| `sasl-password`                      | 下流のKafkaインスタンスに接続するために必要なSASL/PLAINまたはSASL/SCRAM認証のパスワード（オプション）。特殊文字が含まれている場合は、URLエンコードする必要があります。                                                                                                                                                                                                                                                                                           |
| `sasl-mechanism`                     | 下流のKafkaインスタンスに接続するために必要なSASL認証の名前。値は`plain` 、 `scram-sha-256` 、 `scram-sha-512` 、または`gssapi`です。                                                                                                                                                                                                                                                                                            |
| `sasl-gssapi-auth-type`              | gssapi認証タイプ。値は`user`または`keytab` （オプション）です。                                                                                                                                                                                                                                                                                                                                                  |
| `sasl-gssapi-keytab-path`            | gssapi キータブ パス (オプション)。                                                                                                                                                                                                                                                                                                                                                                     |
| `sasl-gssapi-kerberos-config-path`   | gssapi kerberos 構成パス (オプション)。                                                                                                                                                                                                                                                                                                                                                               |
| `sasl-gssapi-service-name`           | gssapi サービス名 (オプション)。                                                                                                                                                                                                                                                                                                                                                                       |
| `sasl-gssapi-user`                   | gssapi 認証のユーザー名 (オプション)。                                                                                                                                                                                                                                                                                                                                                                    |
| `sasl-gssapi-password`               | gssapi認証のパスワード（オプション）。特殊文字が含まれている場合は、URLエンコードする必要があります。                                                                                                                                                                                                                                                                                                                                     |
| `sasl-gssapi-realm`                  | gssapi 領域名 (オプション)。                                                                                                                                                                                                                                                                                                                                                                         |
| `sasl-gssapi-disable-pafxfast`       | gssapi PA-FX-FAST を無効にするかどうか (オプション)。                                                                                                                                                                                                                                                                                                                                                       |
| `dial-timeout`                       | 下流のKafkaとの接続を確立する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                                                                                                                   |
| `read-timeout`                       | 下流のKafkaから返されるレスポンスを取得する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                                                                                                            |
| `write-timeout`                      | 下流のKafkaへのリクエスト送信のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                                                                                                                    |
| `avro-decimal-handling-mode`         | `avro`プロトコルでのみ有効です。Avro が DECIMAL フィールドを処理する方法を指定します。値は`string`または`precise`で、DECIMAL フィールドを文字列または正確な浮動小数点数にマッピングすることを示します。                                                                                                                                                                                                                                                                  |
| `avro-bigint-unsigned-handling-mode` | `avro`プロトコルでのみ有効です。Avro が BIGINT UNSIGNED フィールドを処理する方法を指定します。値は`string`または`long`で、BIGINT UNSIGNED フィールドを 64 ビットの符号付き数値または文字列にマッピングすることを示します。                                                                                                                                                                                                                                                |

### ベストプラクティス {#best-practices}

-   独自のKafkaトピックを作成することをお勧めします。少なくとも、トピックがKafkaブローカーに送信できる各メッセージの最大データ量と、下流のKafkaパーティションの数を設定する必要があります。チェンジフィードを作成する場合、これらの2つの設定はそれぞれ`max-message-bytes`と`partition-num`に対応します。
-   まだ存在しないトピックでチェンジフィードを作成した場合、TiCDCは`partition-num`と`replication-factor`パラメータを使用してトピックを作成しようとします。これらのパラメータは明示的に指定することをお勧めします。
-   ほとんどの場合、 `canal-json`プロトコルを使用することをお勧めします。
-   TiCDCにおけるアップストリームデータの変更頻度が低い場合（例えば、10分以上データの変更がないなど）、Kafkaブローカー設定ファイルでKafka接続アイドルタイムアウトを増やすことをお勧めします。詳細については、 [TiCDC の Kafka へのレプリケーション タスクが`broken pipe`エラーで頻繁に失敗する理由](/ticdc/ticdc-faq.md#why-do-ticdc-replication-tasks-to-kafka-often-fail-with-broken-pipe-errors)参照してください。

> **注記：**
>
> `protocol`が`open-protocol`場合、TiCDC は複数のイベントを 1 つの Kafka メッセージにエンコードし、 `max-message-bytes`で指定された長さを超えるメッセージの生成を回避します。1 行の変更イベントのエンコード結果が`max-message-bytes`を超える場合、changefeed はエラーを報告し、ログを出力。

### TiCDCはKafkaの認証と認可を使用します {#ticdc-uses-the-authentication-and-authorization-of-kafka}

以下は、Kafka SASL 認証を使用する場合の例です。

-   SASL/プレーン

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-user=alice-user&sasl-password=alice-secret&sasl-mechanism=plain"
    ```

-   SASL/スクラム

    SCRAM-SHA-256とSCRAM-SHA-512はPLAIN方式に似ています。対応する認証方式として`sasl-mechanism`指定するだけです。

-   SASL/GSSAPI

    SASL/GSSAPI `user`認証:

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=user&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-password=alice-secret&sasl-gssapi-realm=example.com"
    ```

    `sasl-gssapi-user`と`sasl-gssapi-realm`の値は、Kerberos で指定されている[原理](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html)と関連しています。例えば、プリンシパルが`alice/for-kafka@example.com`に設定されている場合、 `sasl-gssapi-user`と`sasl-gssapi-realm`はそれぞれ`alice/for-kafka`と`example.com`として指定されます。

    SASL/GSSAPI `keytab`認証:

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=keytab&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-keytab-path=/var/lib/secret/alice.key&sasl-gssapi-realm=example.com"
    ```

    SASL/GSSAPI 認証方式の詳細については、 [GSSAPIの設定](https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html)参照してください。

-   TLS/SSL暗号化

    KafkaブローカーでTLS/SSL暗号化が有効になっている場合は、 `--sink-uri`に`-enable-tls=true`パラメータを追加する必要があります。自己署名証明書を使用する場合は、 `--sink-uri`に`ca` 、 `cert` 、 `key`指定する必要があります。

-   ACL認証

    TiCDC が適切に機能するために必要な最小限の権限セットは次のとおりです。

    -   トピック[リソースタイプ](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)の`Create` 、 `Write` 、および`Describe`権限。
    -   クラスタリソース タイプに対する`DescribeConfig`の権限。

    各権限の使用シナリオは次のとおりです。

    | リソースタイプ | 操作の種類            | シナリオ                         |
    | :------ | :--------------- | :--------------------------- |
    | クラスタ    | `DescribeConfig` | 変更フィードの実行中にクラスターのメタデータを取得します |
    | トピック    | `Describe`       | チェンジフィードの開始時にトピックを作成しようとします  |
    | トピック    | `Create`         | チェンジフィードの開始時にトピックを作成しようとします  |
    | トピック    | `Write`          | トピックにデータを送信します               |

    変更フィードを作成または開始するときに、指定された Kafka トピックがすでに存在する場合は、 `Describe`および`Create`権限を無効にすることができます。

### TiCDC を Kafka Connect (Confluent Platform) と統合する {#integrate-ticdc-with-kafka-connect-confluent-platform}

Confluent が提供する[データコネクタ](https://docs.confluent.io/current/connect/managing/connectors.html)を使用してリレーショナル データベースまたは非リレーショナル データベースにデータをストリーミングするには、 [`avro`プロトコル](/ticdc/ticdc-avro-protocol.md)を使用し、 `schema-registry`で[Confluent スキーマレジストリ](https://www.confluent.io/product/confluent-platform/data-compatibility/)の URL を指定する必要があります。

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

v7.4.0以降、TiCDCは、ユーザーがデータレプリケーションに[アブロプロトコル](/ticdc/ticdc-avro-protocol.md)選択した場合、スキーマレジストリとして[AWS Glue スキーマレジストリ](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html)使用をサポートします。設定例は次のとおりです。

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

上記の設定では、 `region`と`registry-name`は必須フィールドですが、 `access-key` 、 `secret-access-key` 、 `token`はオプションフィールドです。AWS認証情報は、changefeed設定ファイルではなく、環境変数として設定するか、 `~/.aws/credentials`ファイルに保存するのがベストプラクティスです。

詳細については、 [Go V2 用公式 AWS SDK ドキュメント](https://aws.github.io/aws-sdk-go-v2/docs/configuring-sdk/#specifying-credentials)を参照してください。

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

-   マッチャールールに一致するテーブルは、対応するトピック式で指定されたポリシーに従ってディスパッチされます。例えば、テーブル`test3.aa`は「トピック式2」に従ってディスパッチされ、テーブル`test5.aa`は「トピック式3」に従ってディスパッチされます。
-   複数のマッチャールールに一致するテーブルの場合、最初に一致するトピック式に従ってディスパッチされます。例えば、 `test1.aa`テーブルは「トピック式 1」に従ってディスパッチされます。
-   どのマッチャールールにも一致しないテーブルの場合、対応するデータ変更イベントは`--sink-uri`で指定されたデフォルトトピックに送信されます。例えば、 `test10.aa`テーブルはデフォルトトピックに送信されます。
-   マッチャールールに一致するもののトピックディスパッチャーを指定していないテーブルの場合、対応するデータ変更は`--sink-uri`で指定されたデフォルトトピックに送信されます。例えば、 `test6.aa`テーブルはデフォルトトピックに送信されます。

### トピックディスパッチャ {#topic-dispatchers}

topic = &quot;xxx&quot; を使用してトピックディスパッチャを指定し、トピック式を使用して柔軟なトピックディスパッチポリシーを実装できます。トピックの総数は1000未満にすることを推奨します。

Topic 式の形式は`[prefix]{schema}[middle][{table}][suffix]`です。

-   `prefix` : オプション。トピック名のプレフィックスを示します。
-   `{schema}` : 必須。スキーマ名を一致させるために使用されます。v7.1.4以降、このパラメータはオプションです。
-   `middle` : オプション。スキーマ名とテーブル名の間の区切り文字を示します。
-   `{table}` : オプション。テーブル名と一致させるために使用されます。
-   `suffix` : オプション。トピック名の接尾辞を示します。

`prefix` 、 `middle` 、 `suffix`は、 `a-z` 、 `A-Z` 、 `0-9` 、 `.` 、 `_` 、 `-`の文字のみを使用できます。 `{schema}`と`{table}`はどちらも小文字です。 `{Schema}`や`{TABLE}`などのプレースホルダーは無効です。

例:

-   `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    -   `test1.table1`に対応するデータ変更イベントは、 `hello_test1_table1`という名前のトピックに送信されます。
    -   `test2.table2`に対応するデータ変更イベントは、 `hello_test2_table2`という名前のトピックに送信されます。
-   `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    -   `test3`内のすべてのテーブルに対応するデータ変更イベントは、 `hello_test3_world`という名前のトピックに送信されます。
    -   `test4`内のすべてのテーブルに対応するデータ変更イベントは、 `hello_test4_world`という名前のトピックに送信されます。
-   `matcher = ['test5.*, 'test6.*'], topic = "hard_code_topic_name"`
    -   `test5`と`test6`のすべてのテーブルに対応するデータ変更イベントは、トピック`hard_code_topic_name`に送信されます。トピック名は直接指定できます。
-   `matcher = ['*.*'], topic = "{schema}_{table}"`
    -   TiCDC が監視するすべてのテーブルは、「schema_table」ルールに従って個別のトピックにディスパッチされます。例えば、テーブル`test.account`の場合、TiCDC はデータ変更ログを`test_account`という名前のトピックにディスパッチします。

### DDLイベントをディスパッチする {#dispatch-ddl-events}

#### スキーマレベルのDDL {#schema-level-ddls}

特定のテーブルに関連しないDDLは、スキーマレベルDDLと呼ばれます（ `create database`や`drop database`など）。スキーマレベルDDLに対応するイベントは、 `--sink-uri`で指定されたデフォルトトピックに送信されます。

#### テーブルレベルのDDL {#table-level-ddls}

特定のテーブルに関連するDDLは、テーブルレベルDDLと呼ばれます（ `alter table`や`create table`など）。テーブルレベルDDLに対応するイベントは、ディスパッチャの設定に従って対応するトピックに送信されます。

たとえば、 `matcher = ['test.*'], topic = {schema}_{table}`ようなディスパッチャの場合、DDL イベントは次のようにディスパッチされます。

-   DDLイベントに単一のテーブルが関係している場合、DDLイベントは対応するトピックにそのまま送信されます。例えば、DDLイベント`drop table test.table1`の場合、イベントは`test_table1`という名前のトピックに送信されます。
-   DDLイベントに複数のテーブルが関係する場合（ `rename table` / `drop table` / `drop view`複数のテーブルに関係する可能性があります）、DDLイベントは複数のイベントに分割され、対応するトピックに送信されます。例えば、DDLイベント`rename table test.table1 to test.table10, test.table2 to test.table20`の場合、イベント`rename table test.table1 to test.table10`はトピック`test_table1`に送信され、イベント`rename table test.table2 to test.table20`はトピック`test.table2`に送信されます。

### パーティションディスパッチャ {#partition-dispatchers}

`partition = "xxx"`パーティションディスパッチャを指定するために使用できます。5つのディスパッチャ（ `default` 、 `index-value` 、 `columns` 、 `table` 、 `ts`をサポートします。ディスパッチャのルールは次のとおりです。

-   `default` : デフォルトで`table`ディスパッチャルールを使用します。スキーマ名とテーブル名に基づいてパーティション番号を計算し、テーブルからのデータが必ず同じパーティションに送信されるようにします。その結果、1つのテーブルからのデータは1つのパーティションにのみ存在し、順序付けが保証されます。ただし、このディスパッチャルールは送信スループットを制限し、コンシューマーを追加しても消費速度を向上させることはできません。
-   `index-value` : 主キー、一意のインデックス、または`index`で明示的に指定されたインデックスのいずれかを使用してパーティション番号を計算し、テーブルデータを複数のパーティションに分散します。単一のテーブルのデータは複数のパーティションに送信され、各パーティションのデータは順序付けされます。コンシューマーを追加することで、消費速度を向上させることができます。このディスパッチャは、同じ行への更新が同じパーティションに送信されるようにすることで、その行の順序付けされた処理を保証します。
-   `columns` : 明示的に指定された列の値を使用してパーティション番号を計算し、テーブルデータを複数のパーティションに分散します。単一のテーブルのデータは複数のパーティションに送信され、各パーティションのデータは順序付けされます。コンシューマーを追加することで、消費速度を向上させることができます。このディスパッチャは、同じ行への更新が同じパーティションに送信されるようにすることで、その行の順序付けされた処理を保証します。
-   `table` : スキーマ名とテーブル名を使用してパーティション番号を計算します。
-   `ts` : 行変更のコミットタイムを用いてパーティション番号を計算し、テーブルデータを複数のパーティションに分散します。単一テーブルのデータは複数のパーティションに送信され、各パーティションのデータは順序付けされます。コンシューマーを追加することで、消費速度を向上させることができます。ただし、データ項目の複数の変更が異なるパーティションに送信され、各コンシューマーのコンシューマー処理の進行状況が異なる場合があり、データの不整合が発生する可能性があります。そのため、コンシューマーは複数のパーティションからのデータを消費する前に、コミットタイムでソートする必要があります。

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

-   `test`データベース内のテーブルは`index-value`ディスパッチャを使用し、主キーまたは一意のインデックスの値を使用してパーティション番号を計算します。主キーが存在する場合は主キーが使用され、存在しない場合は最短の一意のインデックスが使用されます。
-   `test1`テーブル内のテーブルは`index-value`ディスパッチャを使用し、 `index1`という名前のインデックスに含まれるすべての列の値を使用してパーティション番号を計算します。指定されたインデックスが存在しない場合はエラーが報告されます`index`で指定されたインデックスは一意のインデックスである必要があります。
-   `test2`データベース内のテーブルは`columns`ディスパッチャを使用し、列`id`と`a`の値を使用してパーティション番号を計算します。いずれかの列が存在しない場合は、エラーが報告されます。
-   `test3`データベース内のテーブルは`table`ディスパッチャーを使用します。
-   `test4`データベース内のテーブルは、前述のルールのいずれにも一致しないため、 `default`ディスパッチャ、つまり`table`ディスパッチャを使用します。

テーブルが複数のディスパッチャ ルールに一致する場合、最初に一致するルールが優先されます。

> **注記：**
>
> バージョン6.1.0以降、設定の意味を明確にするため、パーティションディスパッチャを指定するための設定が`dispatcher`から`partition`に変更されました。5 `partition` `dispatcher`の別名です。例えば、次の2つのルールは全く同じ意味です。
>
>     [sink]
>     dispatchers = [
>        {matcher = ['*.*'], dispatcher = "index-value"},
>        {matcher = ['*.*'], partition = "index-value"},
>     ]
>
> ただし、 `dispatcher`と`partition`同じルール内に出現させることはできません。例えば、次のルールは無効です。
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
-   `test`データベース内のテーブル ( `t1`テーブルを除く) の場合、 `b`を除くすべての列が送信されます。
-   表`test1.t1`の場合、 `column1`を除く、 `column`で始まるすべての列が送信されます。
-   表`test3.t`の場合、 `column1`を除く、 `column`で始まる 7 文字の列が送信されます。
-   どのルールにも一致しないテーブルの場合、すべての列が送信されます。

> **注記：**
>
> `column-selectors`ルールでフィルタリングされた後、テーブル内のデータは、複製される主キーまたは一意キーを持っている必要があります。そうでない場合、変更フィードは作成時または実行時にエラーを報告します。

## 単一の大きなテーブルの負荷を複数の TiCDC ノードにスケールアウトする {#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes}

この機能は、単一の大規模テーブルのデータレプリケーション範囲を、データ量と1分あたりの変更行数に応じて複数の範囲に分割し、各範囲でレプリケーションされるデータ量と変更行数をほぼ同じにします。この機能は、これらの範囲を複数のTiCDCノードに分散してレプリケーションすることで、複数のTiCDCノードが同時に単一の大規模テーブルをレプリケーションできるようにします。この機能により、以下の2つの問題を解決できます。

-   単一の TiCDC ノードでは、大きな単一のテーブルを時間内に複製することはできません。
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

次の SQL ステートメントを使用して、テーブルに含まれる地域の数を照会できます。

```sql
SELECT COUNT(*) FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS WHERE DB_NAME="database1" AND TABLE_NAME="table1" AND IS_INDEX=0;
```

## Kafka トピックの制限を超えるメッセージを処理する {#handle-messages-that-exceed-the-kafka-topic-limit}

Kafkaトピックは、受信できるメッセージのサイズに制限を設定します。この制限はパラメータ[`max.message.bytes`](https://kafka.apache.org/documentation/#topicconfigs_max.message.bytes)によって制御されます。TiCDC Kafkaシンクがこの制限を超えるデータを送信した場合、チェンジフィードはエラーを報告し、データのレプリケーションを続行できません。この問題を解決するために、TiCDCは新しい設定`large-message-handle-option`を追加し、以下のソリューションを提供します。

現在、この機能はCanal-JSONとOpen Protocolの2つのエンコーディングプロトコルをサポートしています。Canal-JSONプロトコルを使用する場合は、 `sink-uri`のうち`enable-tidb-extension=true`指定する必要があります。

### TiCDCデータ圧縮 {#ticdc-data-compression}

バージョン7.4.0以降、TiCDC Kafkaシンクは、エンコード直後にデータを圧縮し、圧縮データのサイズとメッセージサイズ制限を比較する機能をサポートしています。この機能により、サイズ制限を超えるメッセージの発生を効果的に削減できます。

構成例は次のとおりです。

```toml
[sink.kafka-config.large-message-handle]
# This configuration is introduced in v7.4.0.
# "none" by default, which means that the compression feature is disabled.
# Possible values are "none", "lz4", and "snappy". The default value is "none".
large-message-handle-compression = "none"
```

`large-message-handle-compression`有効になっている場合、コンシューマーが受信するメッセージは特定の圧縮プロトコルを使用してエンコードされ、コンシューマー アプリケーションは指定された圧縮プロトコルを使用してデータをデコードする必要があります。

この機能は、Kafka プロデューサーの圧縮機能とは異なります。

-   `large-message-handle-compression`で指定された圧縮アルゴリズムは、単一のKafkaメッセージを圧縮します。圧縮は、メッセージサイズの制限と比較する前に実行されます。
-   同時に、 [`sink-uri`](#configure-sink-uri-for-kafka)の`compression`パラメータを使用して圧縮アルゴリズムを設定することもできます。この圧縮アルゴリズムは、複数のKafkaメッセージを含むデータ送信リクエスト全体に適用されます。

`large-message-handle-compression`設定した場合、TiCDC はメッセージを受信すると、まずメッセージサイズ制限パラメータの値と比較し、サイズ制限を超えるメッセージを圧縮します。5 に`compression` [`sink-uri`](#configure-sink-uri-for-kafka)設定した場合、TiCDC は`sink-uri`設定に基づいて、送信データ要求全体をシンクレベルで再度圧縮します。

前述の 2 つの圧縮方法の圧縮率は次のように計算されます`compression ratio = size before compression / size after compression * 100` 。

### ハンドルキーのみ送信 {#send-handle-keys-only}

v7.3.0以降、TiCDC Kafkaシンクは、メッセージサイズが制限を超えた場合にハンドルキーのみを送信することをサポートします。これにより、メッセージサイズが大幅に削減され、Kafkaトピックの制限を超えたメッセージサイズに起因するチェンジフィードエラーやタスクの失敗を回避できます。ハンドルキーとは、以下のものを指します。

-   複製するテーブルに主キーがある場合、主キーがハンドル キーになります。
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

ハンドル キーのみを含むメッセージ形式は次のとおりです。

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
        "commitTs": 429918007904436226,  // A TiDB TSO timestamp
        "onlyHandleKey": true
    }
}
```

Kafkaコンシューマーはメッセージを受信すると、まず`onlyHandleKey`フィールドをチェックします。このフィールドが存在し、値が`true`場合、メッセージには完全なデータのハンドルキーのみが含まれていることを意味します。この場合、完全なデータを取得するには、上流のTiDBにクエリを実行し、 [履歴データを読み取るための`tidb_snapshot`](/read-historical-data.md)使用する必要があります。

> **警告：**
>
> Kafkaコンシューマーがデータを処理してTiDBにクエリを実行すると、GCによってデータが削除される可能性があります。この状況を回避するには、 [TiDBクラスタのGCライフタイムを変更する](/system-variables.md#tidb_gc_life_time-new-in-v50)より大きい値に設定する必要があります。

### 大きなメッセージを外部storageに送信する {#send-large-messages-to-external-storage}

バージョン7.4.0以降、TiCDC Kafkaシンクは、メッセージサイズが制限を超えた場合に、大きなメッセージを外部storageに送信することをサポートします。同時に、TiCDCは外部storage内の大きなメッセージのアドレスを含むメッセージをKafkaに送信します。これにより、メッセージサイズがKafkaトピックの制限を超えたことによる変更フィードの失敗を回避できます。

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

`large-message-handle-option` `"claim-check"`に設定する場合、 `claim-check-storage-uri`有効な外部storageアドレスに設定する必要があります。そうでない場合、チェンジフィードの作成は失敗します。

> **ヒント**
>
> TiCDC における Amazon S3、GCS、Azure Blob Storage の URI パラメータの詳細については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

TiCDCは外部storageサービス上のメッセージをクリーンアップしません。データ利用者は外部storageサービスを独自に管理する必要があります。

### 外部storageから大きなメッセージを消費する {#consume-large-messages-from-external-storage}

Kafkaコンシューマーは、外部storage内の大きなメッセージのアドレスを含むメッセージを受信します。メッセージの形式は次のとおりです。

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
        "commitTs": 429918007904436226,  // A TiDB TSO timestamp
        "claimCheckLocation": "s3:/claim-check-bucket/${uuid}.json"
    }
}
```

メッセージに`claimCheckLocation`フィールドが含まれている場合、Kafka コンシューマーは、フィールドで指定されたアドレスに従って、JSON 形式で保存された大きなメッセージデータを読み取ります。メッセージの形式は次のとおりです。

```json
{
  key: "xxx",
  value: "xxx",
}
```

`key`と`value`フィールドは、Kafka メッセージ内の同名のフィールドに対応しています。コンシューマーは、これらの 2 つのフィールドのデータを解析することで、元の大きなメッセージを取得できます。オープンプロトコルでエンコードされた Kafka メッセージのみが、 `key`フィールドに有効なコンテンツを含みます。TiCDC は、 `key`と`value`両方を単一の JSON オブジェクトにエンコードして、完全なメッセージを一度に配信します。他のプロトコルでは、 `key`フィールドは常に空です。

#### <code>value</code>フィールドを外部storageにのみ送信する {#send-the-code-value-code-field-to-external-storage-only}

バージョン8.4.0以降、TiCDCはKafkaメッセージの`value`フィールドのみを外部storageに送信できるようになりました。この機能は、Open Protocol以外のシナリオにのみ適用されます。この機能は、 `claim-check-raw-value`パラメータ（デフォルトは`false`を設定することで制御できます。

> **注記：**
>
> オープンプロトコルを使用する場合、 `claim-check-raw-value` ～ `true`に設定するとエラーが発生します。

`claim-check-raw-value` `true`に設定すると、チェンジフィードは Kafka メッセージの`value`フィールドを、 `key`と`value`の追加の JSON シリアル化なしで外部storageに直接送信します。これにより CPU オーバーヘッドが削減されます。さらに、コンシューマーは外部storageから直接消費可能なデータを読み取ることができるため、デシリアライゼーションのオーバーヘッドが削減されます。

構成例は次のとおりです。

```toml
protocol = "simple"

[sink.kafka-config.large-message-handle]
large-message-handle-option = "claim-check"
claim-check-storage-uri = "s3://claim-check-bucket"
claim-check-raw-value = true
```
