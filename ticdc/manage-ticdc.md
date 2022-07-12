---
title: Manage TiCDC Cluster and Replication Tasks
summary: Learn how to manage a TiCDC cluster and replication tasks.
---

# TiCDCクラスターおよびレプリケーションタスクの管理 {#manage-ticdc-cluster-and-replication-tasks}

このドキュメントでは、TiUPを使用してTiCDCクラスタの構成を変更する方法と、コマンドラインツールを使用してTiCDCクラスタとレプリケーションタスクを管理する方法について説明します`cdc cli` 。

HTTPインターフェイス（TiCDC OpenAPI機能）を使用して、TiCDCクラスタおよびレプリケーションタスクを管理することもできます。詳細については、 [TiCDC OpenAPI](/ticdc/ticdc-open-api.md)を参照してください。

## TiUPを使用してTiCDCをアップグレードする {#upgrade-ticdc-using-tiup}

このセクションでは、TiUPを使用してTiCDCクラスタをアップグレードする方法を紹介します。次の例では、TiCDCとTiDBクラスタ全体をv6.1.0にアップグレードする必要があると想定しています。

{{< copyable "" >}}

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> v6.1.0
```

### アップグレードに関する注意事項 {#notes-for-upgrade}

-   `changefeed`の構成はTiCDCv4.0.2で変更されました。詳細については、 [構成ファイルの互換性に関する注意事項](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)を参照してください。
-   問題が発生した場合は、 [TiUPを使用してTiDBをアップグレードするFAQ](/upgrade-tidb-using-tiup.md#faq)を参照してください。

## TiUPを使用してTiCDC構成を変更する {#modify-ticdc-configuration-using-tiup}

このセクションでは、TiUPの[`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用してTiCDCクラスタの構成を変更する方法を紹介します。次の例では、 `gc-ttl`の値をデフォルトの`86400`から`3600` 、つまり1時間に変更します。

まず、次のコマンドを実行します。 `<cluster-name>`を実際のクラスタ名に置き換える必要があります。

{{< copyable "" >}}

```shell
tiup cluster edit-config <cluster-name>
```

次に、viエディターページに入り、 [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs)の下の`cdc`構成を変更します。構成を以下に示します。

```shell
 server_configs:
  tidb: {}
  tikv: {}
  pd: {}
  tiflash: {}
  tiflash-learner: {}
  pump: {}
  drainer: {}
  cdc:
    gc-ttl: 3600
```

変更後、 `tiup cluster reload -R cdc`コマンドを実行して構成を再ロードします。

## TLSを使用する {#use-tls}

暗号化データ伝送（TLS）の使用の詳細については、 [TiDBコンポーネント間のTLSを有効にする](/enable-tls-between-components.md)を参照してください。

## <code>cdc cli</code>を使用して、クラスタステータスとデータレプリケーションタスクを管理します {#use-code-cdc-cli-code-to-manage-cluster-status-and-data-replication-task}

このセクションでは、 `cdc cli`を使用してTiCDCクラスタおよびデータレプリケーションタスクを管理する方法を紹介します。 `cdc cli`は、 `cdc`バイナリを使用して実行される`cli`サブコマンドです。次の説明は、次のことを前提としています。

-   `cli`コマンドは`cdc`バイナリを使用して直接実行されます。
-   PDは`10.0.10.25`でリッスンし、ポートは`2379`です。

> **ノート：**
>
> PDがリッスンするIPアドレスとポートは、 `pd-server`の起動時に指定された`advertise-client-urls`つのパラメーターに対応します。複数の`pd-server`には複数の`advertise-client-urls`のパラメーターがあり、1つまたは複数のパラメーターを指定できます。たとえば、 `--pd=http://10.0.10.25:2379`または`--pd=http://10.0.10.25:2379,http://10.0.10.26:2379,http://10.0.10.27:2379` 。

TiUPを使用してTiCDCを展開する場合は、次のコマンドの`cdc cli`を`tiup ctl cdc`に置き換えます。

### TiCDCサービスの進捗状況を管理する（ <code>capture</code> ） {#manage-ticdc-service-progress-code-capture-code}

-   `capture`のリストを照会します。

    {{< copyable "" >}}

    ```shell
    cdc cli capture list --pd=http://10.0.10.25:2379
    ```

    ```
    [
      {
        "id": "806e3a1b-0e31-477f-9dd6-f3f2c570abdd",
        "is-owner": true,
        "address": "127.0.0.1:8300"
      },
      {
        "id": "ea2a4203-56fe-43a6-b442-7b295f458ebc",
        "is-owner": false,
        "address": "127.0.0.1:8301"
      }
    ]
    ```

    -   `id` ：サービスプロセスのID。
    -   `is-owner` ：サービスプロセスが所有者ノードであるかどうかを示します。
    -   `address` ：サービスプロセスが外部へのインターフェイスを提供するために使用するアドレス。

### レプリケーションタスクの管理（ <code>changefeed</code> ） {#manage-replication-tasks-code-changefeed-code}

#### レプリケーションタスクの状態転送 {#state-transfer-of-replication-tasks}

レプリケーションタスクの状態は、レプリケーションタスクの実行ステータスを表します。 TiCDCの実行中に、レプリケーションタスクがエラーで失敗したり、手動で一時停止、再開したり、指定された`TargetTs`に到達したりする場合があります。これらの動作は、レプリケーションタスクの状態の変化につながる可能性があります。このセクションでは、TiCDCレプリケーションタスクの状態と状態間の転送関係について説明します。

![TiCDC state transfer](/media/ticdc/ticdc-state-transfer.png)

上記の状態転送図の状態は、次のように説明されています。

-   `Normal` ：レプリケーションタスクは正常に実行され、checkpoint-tsは正常に進行します。
-   `Stopped` ：ユーザーが手動でチェンジフィードを一時停止したため、レプリケーションタスクが停止しました。この状態のチェンジフィードは、GC操作をブロックします。
-   `Error` ：レプリケーションタスクはエラーを返します。回復可能なエラーが原因で、レプリケーションを続行できません。この状態のチェンジフィードは、状態が`Normal`に移行するまで再開を試み続けます。この状態のチェンジフィードは、GC操作をブロックします。
-   `Finished` ：レプリケーションタスクが終了し、プリセット`TargetTs`に到達しました。この状態のチェンジフィードは、GC操作をブロックしません。
-   `Failed` ：レプリケーションタスクは失敗します。一部の回復不能なエラーが原因で、レプリケーションタスクを再開できず、回復できません。この状態のチェンジフィードは、GC操作をブロックしません。

上記の状態転送図の番号は次のとおりです。

-   `changefeed pause`コマンドを実行する
-   `changefeed resume`コマンドを実行してレプリケーションタスクを再開します
-   ③1 `changefeed`の動作で回復可能なエラーが発生し、自動的に動作を再開します。
-   `changefeed resume`コマンドを実行してレプリケーションタスクを再開します
-   ⑤1 `changefeed`の操作で回復可能なエラーが発生する
-   `TargetTs` `changefeed`到達し、レプリケーションが自動的に停止します。
-   `changefeed`は`gc-ttl`で指定された期間より長く中断され、再開できません。
-   `changefeed`は、自動回復を実行しようとしたときに回復不能なエラーが発生しました。

#### レプリケーションタスクを作成する {#create-a-replication-task}

次のコマンドを実行して、レプリケーションタスクを作成します。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

-   `--changefeed-id` ：レプリケーションタスクのID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`の正規表現と一致する必要があります。このIDが指定されていない場合、TiCDCはIDとしてUUID（バージョン4形式）を自動的に生成します。

-   `--sink-uri` ：レプリケーションタスクのダウンストリームアドレス。次の形式に従って`--sink-uri`を構成します。現在、この`kafka`は`mysql` `local` `pulsar`して`s3` `tidb` 。

    {{< copyable "" >}}

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    URIに特殊文字が含まれている場合、URLエンコードを使用してこれらの特殊文字を処理する必要があります。

-   `--start-ts` ： `changefeed`の開始TSOを指定します。このTSOから、TiCDCクラスタはデータのプルを開始します。デフォルト値は現在の時刻です。

-   `--target-ts` ： `changefeed`の終了TSOを指定します。このTSOに対して、TiCDCクラスタはデータのプルを停止します。デフォルト値は空です。これは、TiCDCがデータのプルを自動的に停止しないことを意味します。

-   `--sort-engine` ： `changefeed`のソートエンジンを指定します。 TiDBとTiKVは分散アーキテクチャを採用しているため、TiCDCはデータの変更をシンクに書き込む前にソートする必要があります。このオプションは、 `unified` （デフォルト）/ `memory` / `file`をサポートします。

    -   `unified` ： `unified`が使用されている場合、TiCDCはメモリ内のデータの並べ替えを優先します。メモリが不足している場合、TiCDCは自動的にディスクを使用して一時データを保存します。これはデフォルト値の`--sort-engine`です。
    -   `memory` ：メモリ内のデータ変更をソートします。大量のデータを複製するとOOMが簡単にトリガーされるため、この並べ替えエンジンの使用は**お勧めしません**。
    -   `file` ：ディスクを完全に使用して一時データを保存します。この機能は**廃止され**ました。<strong>いかなる</strong>状況でも使用することは<strong>お勧めしません</strong>。

-   `--config` ： `changefeed`の構成ファイルを指定します。

-   `sort-dir` ：ソートエンジンが使用する一時ファイルディレクトリを指定します。 **TiDB v4.0.13、v5.0.3、およびv5.1.0以降、このオプションはサポートされていないことに注意してください。もう使用しないでください**。

#### <code>mysql</code> / <code>tidb</code>を使用してシンクURIを構成します {#configure-sink-uri-with-code-mysql-code-code-tidb-code}

構成例：

{{< copyable "" >}}

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000"
```

以下は、 `mysql` / `tidb`のシンクURIに設定できるパラメータとパラメータ値の説明です。

| パラメータ/パラメータ値   | 説明                                                                                                                                                                                                                          |
| :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root`         | ダウンストリームデータベースのユーザー名                                                                                                                                                                                                        |
| `123456`       | ダウンストリームデータベースのパスワード                                                                                                                                                                                                        |
| `127.0.0.1`    | ダウンストリームデータベースのIPアドレス                                                                                                                                                                                                       |
| `3306`         | ダウンストリームデータのポート                                                                                                                                                                                                             |
| `worker-count` | ダウンストリームに対して同時に実行できるSQLステートメントの数（オプション、デフォルトでは`16` ）                                                                                                                                                                        |
| `max-txn-row`  | ダウンストリームで実行できるトランザクションバッチのサイズ（オプション、デフォルトで`256` ）                                                                                                                                                                           |
| `ssl-ca`       | ダウンストリームMySQLインスタンスに接続するために必要なCA証明書ファイルのパス（オプション）                                                                                                                                                                           |
| `ssl-cert`     | ダウンストリームのMySQLインスタンスに接続するために必要な証明書ファイルのパス（オプション）                                                                                                                                                                            |
| `ssl-key`      | ダウンストリームのMySQLインスタンスに接続するために必要な証明書キーファイルのパス（オプション）                                                                                                                                                                          |
| `time-zone`    | ダウンストリームのMySQLインスタンスに接続するときに使用されるタイムゾーン。v4.0.8以降で有効です。これはオプションのパラメーターです。このパラメーターが指定されていない場合、TiCDCサービスプロセスのタイムゾーンが使用されます。このパラメーターが空の値に設定されている場合、TiCDCがダウンストリームのMySQLインスタンスに接続するときにタイムゾーンが指定されず、ダウンストリームのデフォルトのタイムゾーンが使用されます。 |

#### <code>kafka</code>を使用してシンクURIを構成する {#configure-sink-uri-with-code-kafka-code}

構成例：

{{< copyable "" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

以下は、 `kafka`を使用してシンクURIに構成できるパラメーターとパラメーター値の説明です。

| パラメータ/パラメータ値                         | 説明                                                                                                                                                                                                      |
| :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `127.0.0.1`                          | ダウンストリームKafkaサービスのIPアドレス                                                                                                                                                                                |
| `9092`                               | 下流のカフカの港                                                                                                                                                                                                |
| `topic-name`                         | 変数。カフカトピックの名前                                                                                                                                                                                           |
| `kafka-version`                      | ダウンストリームKafkaのバージョン（オプション、デフォルトで`2.4.0`現在、サポートされている最も古いKafkaバージョンは`0.11.0.2`で、最新のバージョンは`2.7.0`です。この値はダウンストリームKafkaの実際のバージョンと一致している必要があります）                                                              |
| `kafka-client-id`                    | レプリケーションタスクのKafkaクライアントIDを指定します（オプション。デフォルトでは`TiCDC_sarama_producer_replication ID` ）。                                                                                                                  |
| `partition-num`                      | ダウンストリームKafkaパーティションの数（オプション。値は実際のパーティション数を**超えてはなりません**。そうでない場合、レプリケーションタスクを正常に作成できません。デフォルトでは`3` ）                                                                                                    |
| `max-message-bytes`                  | 毎回Kafkaブローカーに送信されるデータの最大サイズ（オプション、デフォルトでは`10MB` ）。 v5.0.6およびv4.0.6から、デフォルト値が64MBおよび256MBから10MBに変更されました。                                                                                                 |
| `replication-factor`                 | 保存できるKafkaメッセージレプリカの数（オプション、デフォルトで`1` ）                                                                                                                                                                 |
| `protocol`                           | メッセージがKafkaに出力されるプロトコル。値の`maxwell`は、 `canal-json` 、 `avro` `canal` `open-protocol` 。                                                                                                                    |
| `auto-create-topic`                  | 渡された`topic-name`がKafkaクラスタに存在しない場合にTiCDCがトピックを自動的に作成するかどうかを決定します（オプション、デフォルトでは`true` ）                                                                                                                  |
| `enable-tidb-extension`              | オプション。デフォルトでは`false` 。出力プロトコルが`canal-json`の場合、値が`true`の場合、TiCDCはResolvedイベントを送信し、TiDB拡張フィールドをKafkaメッセージに追加します。 v6.1.0以降、このパラメーターは`avro`プロトコルにも適用できます。値が`true`の場合、TiCDCは3つのTiDB拡張フィールドをKafkaメッセージに追加します。 |
| `max-batch-size`                     | v4.0.9の新機能。メッセージプロトコルが1つのKafkaメッセージへの複数のデータ変更の出力をサポートしている場合、このパラメーターは1つのKafkaメッセージでのデータ変更の最大数を指定します。現在、Kafkaの`protocol`が`open-protocol`の場合にのみ有効になります。 （オプション、デフォルトで`16` ）                               |
| `enable-tls`                         | TLSを使用してダウンストリームKafkaインスタンスに接続するかどうか（オプション、デフォルトで`false` ）                                                                                                                                              |
| `ca`                                 | ダウンストリームのKafkaインスタンスに接続するために必要なCA証明書ファイルのパス（オプション）                                                                                                                                                      |
| `cert`                               | ダウンストリームのKafkaインスタンスに接続するために必要な証明書ファイルのパス（オプション）                                                                                                                                                        |
| `key`                                | ダウンストリームのKafkaインスタンスに接続するために必要な証明書キーファイルのパス（オプション）                                                                                                                                                      |
| `sasl-user`                          | ダウンストリームのKafkaインスタンスに接続するために必要なSASL/PLAINまたはSASL/SCRAM認証のID（authcid）（オプション）                                                                                                                             |
| `sasl-password`                      | ダウンストリームのKafkaインスタンスに接続するために必要なSASL/PLAINまたはSASL/SCRAM認証のパスワード（オプション）                                                                                                                                   |
| `sasl-mechanism`                     | ダウンストリームのKafkaインスタンスに接続するために必要なSASL認証の名前。 `scram-sha-256`は、 `plain` 、または`scram-sha-512`にすることができ`gssapi` 。                                                                                               |
| `sasl-gssapi-auth-type`              | gssapi認証タイプ。値は`user`または`keytab`にすることができます（オプション）                                                                                                                                                        |
| `sasl-gssapi-keytab-path`            | gssapiキータブパス（オプション）                                                                                                                                                                                     |
| `sasl-gssapi-kerberos-config-path`   | gssapi kerberos構成パス（オプション）                                                                                                                                                                              |
| `sasl-gssapi-service-name`           | gssapiサービス名（オプション）                                                                                                                                                                                      |
| `sasl-gssapi-user`                   | gssapi認証のユーザー名（オプション）                                                                                                                                                                                   |
| `sasl-gssapi-password`               | gssapi認証のパスワード（オプション）                                                                                                                                                                                   |
| `sasl-gssapi-realm`                  | gssapiレルム名（オプション）                                                                                                                                                                                       |
| `sasl-gssapi-disable-pafxfast`       | gssapi PA-FX-FASTを無効にするかどうか（オプション）                                                                                                                                                                      |
| `dial-timeout`                       | ダウンストリームKafkaとの接続を確立する際のタイムアウト。デフォルト値は`10s`です                                                                                                                                                           |
| `read-timeout`                       | ダウンストリームのKafkaから返される応答を取得する際のタイムアウト。デフォルト値は`10s`です                                                                                                                                                      |
| `write-timeout`                      | ダウンストリームKafkaにリクエストを送信する際のタイムアウト。デフォルト値は`10s`です                                                                                                                                                         |
| `avro-decimal-handling-mode`         | `avro`のプロトコルでのみ有効です。 AvroがDECIMALフィールドを処理する方法を決定します。値は`string`または`precise`で、DECIMALフィールドを文字列または正確な浮動小数点数にマッピングすることを示します。                                                                                |
| `avro-bigint-unsigned-handling-mode` | `avro`のプロトコルでのみ有効です。 AvroがBIGINTUNSIGNEDフィールドを処理する方法を決定します。値は`string`または`long`で、BIGINTUNSIGNEDフィールドを64ビットの符号付き数値または文字列にマッピングすることを示します。                                                                  |

ベストプラクティス：

-   独自のKafkaトピックを作成することをお勧めします。少なくとも、トピックがKafkaブローカーに送信できる各メッセージのデータの最大量と、ダウンストリームのKafkaパーティションの数を設定する必要があります。チェンジフィードを作成する場合、これら2つの設定はそれぞれ`max-message-bytes`と`partition-num`に対応します。
-   まだ存在しないトピックを使用してチェンジフィードを作成する場合、TiCDCは`partition-num`および`replication-factor`パラメーターを使用してトピックを作成しようとします。これらのパラメーターを明示的に指定することをお勧めします。
-   ほとんどの場合、 `canal-json`プロトコルを使用することをお勧めします。

> **ノート：**
>
> `protocol`が`open-protocol`の場合、TiCDCは長さが`max-message-bytes`を超えるメッセージの生成を回避しようとします。ただし、行が大きすぎて1回の変更だけで長さが`max-message-bytes`を超える場合、サイレント障害を回避するために、TiCDCはこのメッセージを出力しようとし、ログに警告を出力します。

#### TiCDCはKafkaの認証と承認を使用します {#ticdc-uses-the-authentication-and-authorization-of-kafka}

以下は、KafkaSASL認証を使用する場合の例です。

-   SASL / PLAIN

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-user=alice-user&sasl-password=alice-secret&sasl-mechanism=plain"
    ```

-   SASL / SCRAM

    SCRAM-SHA-256およびSCRAM-SHA-512は、PLAINメソッドに似ています。対応する認証方法として`sasl-mechanism`を指定する必要があります。

-   SASL / GSSAPI

    SASL / GSSAPI `user`認証：

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=user&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-password=alice-secret&sasl-gssapi-realm=example.com"
    ```

    `sasl-gssapi-user`と`sasl-gssapi-realm`の値は、Kerberosで指定された[原理](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html)に関連しています。たとえば、原則が`alice/for-kafka@example.com`に設定されている場合、 `sasl-gssapi-user`と`sasl-gssapi-realm`はそれぞれ`alice/for-kafka`と`example.com`として指定されます。

    SASL / GSSAPI `keytab`認証：

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=keytab&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-keytab-path=/var/lib/secret/alice.key&sasl-gssapi-realm=example.com"
    ```

    SASL / GSSAPI認証方式の詳細については、 [GSSAPIの構成](https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html)を参照してください。

-   TLS/SSL暗号化

    KafkaブローカーでTLS/SSL暗号化が有効になっている場合は、 `-enable-tls=true`パラメーターを`--sink-uri`に追加する必要があります。自己署名証明書を使用する場合は、 `cert` `ca`および`key`も指定する必要があり`--sink-uri` 。

-   ACL認証

    TiCDCが正しく機能するために必要な最小限の権限セットは次のとおりです。

    -   トピック[リソースタイプ](https://docs.confluent.io/platform/current/kafka/authorization.html#resources)の`Create`および`Write`の権限。
    -   クラスターリソースタイプの`DescribeConfigs`のアクセス許可。

#### TiCDCをKafkaConnect（Confluent Platform）と統合する {#integrate-ticdc-with-kafka-connect-confluent-platform}

Confluentが提供する[データコネクタ](https://docs.confluent.io/current/connect/managing/connectors.html)を使用してデータをリレーショナルデータベースまたは非リレーショナルデータベースにストリーミングするには、 `avro`プロトコルを使用し、 `schema-registry`のURLを指定する必要があり[コンフルエントなスキーマレジストリ](https://www.confluent.io/product/confluent-platform/data-compatibility/) 。

構成例：

{{< copyable "" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --schema-registry="http://127.0.0.1:8081" --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

詳細な統合ガイドについては、 [TiDBとConfluentプラットフォームの統合に関するクイックスタートガイド](/ticdc/integrate-confluent-using-ticdc.md)を参照してください。

#### <code>pulsar</code>を使用してシンクURIを構成する {#configure-sink-uri-with-code-pulsar-code}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境では使用し**ない**でください。

構成例：

{{< copyable "" >}}

```shell
--sink-uri="pulsar://127.0.0.1:6650/topic-name?connectionTimeout=2s"
```

以下は、 `pulsar`を使用してシンクURIに構成できるパラメーターの説明です。

| パラメータ                        | 説明                                                                                                                                      |
| :--------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| `connectionTimeout`          | ダウンストリームパルサーへの接続を確立するためのタイムアウト。これはオプションで、デフォルトは30（秒）です。                                                                                 |
| `operationTimeout`           | ダウンストリームパルサーで操作を実行するためのタイムアウト。これはオプションで、デフォルトは30（秒）です。                                                                                  |
| `tlsTrustCertsFilePath`      | ダウンストリームPulsarインスタンスに接続するために必要なCA証明書ファイルのパス（オプション）                                                                                      |
| `tlsAllowInsecureConnection` | TLSを有効にした後に暗号化されていない接続を許可するかどうかを決定します（オプション）                                                                                            |
| `tlsValidateHostname`        | ダウンストリームパルサーからの証明書のホスト名を確認するかどうかを決定します（オプション）                                                                                           |
| `maxConnectionsPerBroker`    | 単一のダウンストリームPulsarブローカーに許可される接続の最大数。これはオプションであり、デフォルトは1です。                                                                               |
| `auth.tls`                   | TLSモードを使用して、ダウンストリームのパルサーを検証します（オプション）。たとえば、 `auth=tls&auth.tlsCertFile=/path/to/cert&auth.tlsKeyFile=/path/to/key` 。                   |
| `auth.token`                 | トークンモードを使用して、ダウンストリームのパルサーを検証します（オプション）。たとえば、 `auth=token&auth.token=secret-token`または`auth=token&auth.file=path/to/secret-token-file` 。 |
| `name`                       | TiCDCのパルサープロデューサーの名前（オプション）                                                                                                             |
| `protocol`                   | メッセージがパルサーに出力されるプロトコル。値の`maxwell`は、 `canal-json` 、 `avro` `canal` `open-protocol` 。                                                     |
| `maxPendingMessages`         | 保留中のメッセージキューの最大サイズを設定します。これはオプションで、デフォルトは1000です。たとえば、Pulsarからの確認メッセージの保留中です。                                                            |
| `disableBatching`            | メッセージをバッチで自動的に送信することを無効にします（オプション）                                                                                                      |
| `batchingMaxPublishDelay`    | 送信されたメッセージがバッチ処理される期間を設定します（デフォルト：10ms）                                                                                                 |
| `compressionType`            | メッセージの送信に使用される圧縮アルゴリズムを設定します（オプション）。値のオプションは、 `NONE` 、 `ZSTD` `ZLIB` `LZ4` （デフォルトでは`NONE` ）                                             |
| `hashingScheme`              | メッセージの送信先のパーティションを選択するために使用されるハッシュアルゴリズム（オプション）。値のオプションは`JavaStringHash` （デフォルト）と`Murmur3`です。                                           |
| `properties.*`               | TiCDCのパルサープロデューサーに追加されたカスタマイズされたプロパティ（オプション）。たとえば、 `properties.location=Hangzhou` 。                                                     |

パルサーのその他のパラメーターについては、 [pulsar-client-go ClientOptions](https://godoc.org/github.com/apache/pulsar-client-go/pulsar#ClientOptions)および[pulsar-client-go ProducerOptions](https://godoc.org/github.com/apache/pulsar-client-go/pulsar#ProducerOptions)を参照してください。

#### タスク構成ファイルを使用する {#use-the-task-configuration-file}

その他のレプリケーション構成（たとえば、単一のテーブルのレプリケーションを指定する）については、 [タスク構成ファイル](#task-configuration-file)を参照してください。

構成ファイルを使用して、次の方法でレプリケーションタスクを作成できます。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --config changefeed.toml
```

上記のコマンドで、 `changefeed.toml`はレプリケーションタスクの構成ファイルです。

#### レプリケーションタスクリストをクエリする {#query-the-replication-task-list}

次のコマンドを実行して、レプリケーションタスクリストを照会します。

{{< copyable "" >}}

```shell
cdc cli changefeed list --pd=http://10.0.10.25:2379
```

```shell
[{
    "id": "simple-replication-task",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

-   `checkpoint`は、この時点より前にTiCDCがすでにデータをダウンストリームに複製していることを示します。
-   `state`は、レプリケーションタスクの状態を示します。
    -   `normal` ：レプリケーションタスクは正常に実行されます。
    -   `stopped` ：レプリケーションタスクが停止します（手動で一時停止します）。
    -   `error` ：レプリケーションタスクは（エラーによって）停止されます。
    -   `removed` ：レプリケーションタスクが削除されます。この状態のタスクは、 `--all`オプションを指定した場合にのみ表示されます。このオプションが指定されていないときにこれらのタスクを表示するには、 `changefeed query`コマンドを実行します。
    -   `finished` ：レプリケーションタスクが終了します（データは`target-ts`にレプリケートされます）。この状態のタスクは、 `--all`オプションを指定した場合にのみ表示されます。このオプションが指定されていないときにこれらのタスクを表示するには、 `changefeed query`コマンドを実行します。

#### 特定のレプリケーションタスクをクエリする {#query-a-specific-replication-task}

特定のレプリケーションタスクをクエリするには、 `changefeed query`コマンドを実行します。クエリ結果には、タスク情報とタスク状態が含まれます。 `--simple`または`-s`引数を指定して、基本的なレプリケーション状態とチェックポイント情報のみを含むクエリ結果を簡略化できます。この引数を指定しない場合、詳細なタスク構成、レプリケーション状態、およびレプリケーションテーブル情報が出力されます。

{{< copyable "" >}}

```shell
cdc cli changefeed query -s --pd=http://10.0.10.25:2379 --changefeed-id=simple-replication-task
```

```
{
 "state": "normal",
 "tso": 419035700154597378,
 "checkpoint": "2020-08-27 10:12:19.579",
 "error": null
}
```

上記のコマンドと結果では、次のようになります。

-   `state`は、現在の`changefeed`の複製状態です。各状態は、 `changefeed list`の状態と一致している必要があります。
-   `tso`は、ダウンストリームに正常に複製された現在の`changefeed`の最大のトランザクションTSOを表します。
-   `checkpoint`は、ダウンストリームに正常に複製された、現在の`changefeed`の最大のトランザクションTSOの対応する時間を表します。
-   `error`は、現在の`changefeed`でエラーが発生したかどうかを記録します。

{{< copyable "" >}}

```shell
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id=simple-replication-task
```

```
{
  "info": {
    "sink-uri": "mysql://127.0.0.1:3306/?max-txn-row=20\u0026worker-number=4",
    "opts": {},
    "create-time": "2020-08-27T10:33:41.687983832+08:00",
    "start-ts": 419036036249681921,
    "target-ts": 0,
    "admin-job-type": 0,
    "sort-engine": "unified",
    "sort-dir": ".",
    "config": {
      "case-sensitive": true,
      "enable-old-value": false,
      "filter": {
        "rules": [
          "*.*"
        ],
        "ignore-txn-start-ts": null,
        "ddl-allow-list": null
      },
      "mounter": {
        "worker-num": 16
      },
      "sink": {
        "dispatchers": null,
      },
      "scheduler": {
        "type": "table-number",
        "polling-time": -1
      }
    },
    "state": "normal",
    "history": null,
    "error": null
  },
  "status": {
    "resolved-ts": 419036036249681921,
    "checkpoint-ts": 419036036249681921,
    "admin-job-type": 0
  },
  "count": 0,
  "task-status": [
    {
      "capture-id": "97173367-75dc-490c-ae2d-4e990f90da0f",
      "status": {
        "tables": {
          "47": {
            "start-ts": 419036036249681921
          }
        },
        "operation": null,
        "admin-job-type": 0
      }
    }
  ]
}
```

上記のコマンドと結果では、次のようになります。

-   `info`は、照会された`changefeed`の複製構成です。
-   `status`は、照会された`changefeed`の複製状態です。
    -   `resolved-ts` ：現在の`changefeed`で最大のトランザクション`TS` 。この`TS`はTiKVからTiCDCに正常に送信されていることに注意してください。
    -   `checkpoint-ts` ：現在の`changefeed`で最大のトランザクション`TS` 。この`TS`はダウンストリームに正常に書き込まれていることに注意してください。
    -   `admin-job-type` ： `changefeed`のステータス：
        -   `0` ：状態は正常です。
        -   `1` ：タスクは一時停止されています。タスクが一時停止されると、複製されたすべての`processor`が終了します。タスクの構成とレプリケーションステータスは保持されるため、 `checkpiont-ts`からタスクを再開できます。
        -   `2` ：タスクが再開されます。レプリケーションタスクは`checkpoint-ts`から再開します。
        -   `3` ：タスクは削除されます。タスクが削除されると、複製された`processor`がすべて終了し、複製タスクの構成情報がクリアされます。レプリケーションステータスのみが、後のクエリのために保持されます。
-   `task-status`は、クエリされた`changefeed`の各レプリケーションサブタスクの状態を示します。

#### レプリケーションタスクを一時停止します {#pause-a-replication-task}

次のコマンドを実行して、レプリケーションタスクを一時停止します。

{{< copyable "" >}}

```shell
cdc cli changefeed pause --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

上記のコマンドでは：

-   `--changefeed-id=uuid`は、一時停止するレプリケーションタスクに対応する`changefeed`のIDを表します。

#### レプリケーションタスクを再開します {#resume-a-replication-task}

次のコマンドを実行して、一時停止したレプリケーションタスクを再開します。

{{< copyable "" >}}

```shell
cdc cli changefeed resume --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

上記のコマンドでは：

-   `--changefeed-id=uuid`は、再開するレプリケーションタスクに対応する`changefeed`のIDを表します。

#### レプリケーションタスクを削除する {#remove-a-replication-task}

次のコマンドを実行して、レプリケーションタスクを削除します。

{{< copyable "" >}}

```shell
cdc cli changefeed remove --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

上記のコマンドでは：

-   `--changefeed-id=uuid`は、削除するレプリケーションタスクに対応する`changefeed`のIDを表します。

### タスク構成の更新 {#update-task-configuration}

v4.0.4以降、TiCDCはレプリケーションタスクの構成の変更をサポートします（動的ではありません）。 `changefeed`の構成を変更するには、タスクを一時停止し、構成を変更してから、タスクを再開します。

{{< copyable "" >}}

```shell
cdc cli changefeed pause -c test-cf --pd=http://10.0.10.25:2379
cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

現在、次の構成アイテムを変更できます。

-   `changefeed`の`sink-uri` 。
-   `changefeed`の構成ファイルとファイル内のすべての構成項目。
-   ファイルの並べ替え機能と並べ替えディレクトリを使用するかどうか。
-   `changefeed`のうちの`target-ts`つ。

### レプリケーションサブタスクの処理ユニットを管理する（ <code>processor</code> ） {#manage-processing-units-of-replication-sub-tasks-code-processor-code}

-   `processor`のリストを照会します。

    {{< copyable "" >}}

    ```shell
    cdc cli processor list --pd=http://10.0.10.25:2379
    ```

    ```
    [
            {
                    "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                    "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "changefeed-id": "simple-replication-task"
            }
    ]
    ```

-   特定のレプリケーションタスクのステータスに対応する特定の`changefeed`をクエリします。

    {{< copyable "" >}}

    ```shell
    cdc cli processor query --pd=http://10.0.10.25:2379 --changefeed-id=simple-replication-task --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
    ```

    ```
    {
      "status": {
        "tables": {
          "56": {    # ID of the replication table, corresponding to tidb_table_id of a table in TiDB
            "start-ts": 417474117955485702
          }
        },
        "operation": null,
        "admin-job-type": 0
      },
      "position": {
        "checkpoint-ts": 417474143881789441,
        "resolved-ts": 417474143881789441,
        "count": 0
      }
    }
    ```

    上記のコマンドでは：

    -   `status.tables` ：各キー番号は、TiDBのテーブルの`tidb_table_id`に対応するレプリケーションテーブルのIDを表します。
    -   `resolved-ts` ：現在のプロセッサでソートされたデータの中で最大のTSO。
    -   `checkpoint-ts` ：現在のプロセッサのダウンストリームに正常に書き込まれた最大のTSO。

## タスク構成ファイル {#task-configuration-file}

このセクションでは、レプリケーションタスクの構成を紹介します。

```toml
# Specifies whether the database names and tables in the configuration file are case-sensitive.
# The default value is true.
# This configuration item affects configurations related to filter and sink.
case-sensitive = true

# Specifies whether to output the old value. New in v4.0.5. Since v5.0, the default value is `true`.
enable-old-value = true

[filter]
# Ignores the transaction of specified start_ts.
ignore-txn-start-ts = [1, 2]

# Filter rules.
# Filter syntax: https://docs.pingcap.com/tidb/stable/table-filter#syntax.
rules = ['*.*', '!test.*']

[mounter]
# mounter thread counts, which is used to decode the TiKV output data.
worker-num = 16

[sink]
# For the sink of MQ type, you can use dispatchers to configure the event dispatcher.
# Since v6.1, TiDB supports two types of event dispatchers: partition and topic. For more information, see the following section.
# The matching syntax of matcher is the same as the filter rule syntax. For details about the matcher rules, see the following section.

dispatchers = [
    {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
    {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
    {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
    {matcher = ['test6.*'], partition = "ts"}
]
# For the sink of MQ type, you can specify the protocol format of the message.
# Currently the following protocols are supported: canal-json, open-protocol, canal, avro, and maxwell.
protocol = "canal-json"
```

### 互換性に関する注意 {#notes-for-compatibility}

-   TiCDC v4.0.0では、 `ignore-txn-commit-ts`が削除され、 `ignore-txn-start-ts`が追加されます。これは、start_tsを使用してトランザクションをフィルタリングします。
-   TiCDC v4.0.2では、 `db-dbs` / `db-tables` / `ignore-dbs` / `ignore-tables`が削除され、 `rules`が追加されました。これは、データベースとテーブルに新しいフィルタールールを使用します。フィルタ構文の詳細については、 [テーブルフィルター](/table-filter.md)を参照してください。

## KafkaSinkのトピックおよびパーティションディスパッチャのルールをカスタマイズします {#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink}

### マッチャールール {#matcher-rules}

前のセクションの例では：

-   マッチャールールに一致するテーブルの場合、対応するトピック式で指定されたポリシーに従ってディスパッチされます。たとえば、 `test3.aa`テーブルは「トピック式2」に従ってディスパッチされます。 `test5.aa`テーブルは「トピック式3」に従ってディスパッチされます。
-   複数のマッチャールールに一致するテーブルの場合、最初に一致するトピック式に従ってディスパッチされます。たとえば、 `test1.aa`テーブルは「トピック式1」に従って配布されます。
-   どのマッチャールールにも一致しないテーブルの場合、対応するデータ変更イベントは、 `--sink-uri`で指定されたデフォルトのトピックに送信されます。たとえば、 `test10.aa`テーブルはデフォルトのトピックに送信されます。
-   マッチャールールに一致するがトピックディスパッチャーを指定しないテーブルの場合、対応するデータ変更は`--sink-uri`で指定されたデフォルトトピックに送信されます。たとえば、 `test6.aa`テーブルはデフォルトのトピックに送信されます。

### トピックディスパッチャ {#topic-dispatchers}

topic = &quot;xxx&quot;を使用してトピックディスパッチャーを指定し、トピック式を使用して柔軟なトピックディスパッチポリシーを実装できます。トピックの総数は1000未満にすることをお勧めします。

トピック式の形式は`[prefix]{schema}[middle][{table}][suffix]`です。

-   `prefix` ：オプション。トピック名のプレフィックスを示します。
-   `{schema}` ：必須。スキーマ名と一致させるために使用されます。
-   `middle` ：オプション。スキーマ名とテーブル名の間の区切り文字を示します。
-   `{table}` ：オプション。テーブル名と一致させるために使用されます。
-   `suffix` ：オプション。トピック名のサフィックスを示します。

`prefix` 、および`suffix`には、 `middle` 、 `0-9` `A-Z`の`_`のみを`.`ことが`-` `a-z` 。 `{schema}`と`{table}`は両方とも小文字です。 `{Schema}`や`{TABLE}`などのプレースホルダーは無効です。

いくつかの例：

-   `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    -   `test1.table1`に対応するデータ変更イベントは、 `hello_test1_table1`という名前のトピックに送信されます。
    -   `test2.table2`に対応するデータ変更イベントは、 `hello_test2_table2`という名前のトピックに送信されます。
-   `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    -   `test3`のすべてのテーブルに対応するデータ変更イベントは、 `hello_test3_world`という名前のトピックに送信されます。
    -   `test4`のすべてのテーブルに対応するデータ変更イベントは、 `hello_test4_world`という名前のトピックに送信されます。
-   `matcher = ['*.*'], topic = "{schema}_{table}"`
    -   TiCDCによってリッスンされるすべてのテーブルは、「schema_table」ルールに従って個別のトピックにディスパッチされます。たとえば、 `test.account`テーブルの場合、TiCDCはデータ変更ログを`test_account`という名前のトピックにディスパッチします。

### DDLイベントをディスパッチします {#dispatch-ddl-events}

#### スキーマレベルのDDL {#schema-level-ddls}

特定のテーブルに関連しないDDLは、 `create database`や`drop database`などのスキーマレベルのDDLと呼ばれます。スキーマレベルのDDLに対応するイベントは、 `--sink-uri`で指定されたデフォルトのトピックに送信されます。

#### テーブルレベルのDDL {#table-level-ddls}

特定のテーブルに関連するDDLは、 `alter table`や`create table`などのテーブルレベルのDDLと呼ばれます。テーブルレベルのDDLに対応するイベントは、ディスパッチャの構成に従って対応するトピックに送信されます。

たとえば、 `matcher = ['test.*'], topic = {schema}_{table}`のようなディスパッチャの場合、DDLイベントは次のようにディスパッチャされます。

-   単一のテーブルがDDLイベントに関与している場合、DDLイベントは対応するトピックにそのまま送信されます。たとえば、DDLイベント`drop table test.table1`の場合、イベントは`test_table1`という名前のトピックに送信されます。
-   複数のテーブルがDDLイベントに関与している場合（ `rename table`は複数のテーブルに関与している可能性があり`drop table` ）、DDLイベントは複数のイベントに分割され、対応するトピックに送信され`drop view` 。たとえば、DDLイベント`rename table test.table1 to test.table10, test.table2 to test.table20`の場合、イベント`rename table test.table1 to test.table10`は`test_table1`という名前のトピックに送信され、イベント`rename table test.table2 to test.table20`は`test.table2`という名前のトピックに送信されます。

### パーティションディスパッチャ {#partition-dispatchers}

`partition = "xxx"`を使用して、パーティションディスパッチャーを指定できます。デフォルト、ts、インデックス値、テーブルの4つのディスパッチャをサポートします。ディスパッチャのルールは次のとおりです。

-   デフォルト：複数の一意のインデックス（主キーを含む）が存在する場合、または古い値機能が有効になっている場合、イベントはテーブルモードでディスパッチされます。一意のインデックス（または主キー）が1つしかない場合、イベントはインデックス値モードでディスパッチされます。
-   ts：行変更のcommitTを使用して、イベントをハッシュおよびディスパッチします。
-   index-value：主キーの値またはテーブルの一意のインデックスを使用して、イベントをハッシュおよびディスパッチします。
-   table：テーブルのスキーマ名とテーブル名を使用して、イベントをハッシュおよびディスパッチします。

> **ノート：**
>
> v6.1以降、構成の意味を明確にするために、パーティション・ディスパッチャーを指定するために使用される構成が`dispatcher`から`partition`に変更され、 `partition`は`dispatcher`のエイリアスになりました。たとえば、次の2つのルールはまったく同じです。
>
> ```
> [sink]
> dispatchers = [
>    {matcher = ['*.*'], dispatcher = "ts"},
>    {matcher = ['*.*'], partition = "ts"},
> ]
> ```
>
> ただし、 `dispatcher`と`partition`を同じルールに含めることはできません。たとえば、次のルールは無効です。
>
> ```
> {matcher = ['*.*'], dispatcher = "ts", partition = "table"},
> ```

## 行変更イベントの履歴値を出力する<span class="version-mark">v4.0.5の新機能</span> {#output-the-historical-value-of-a-row-changed-event-span-class-version-mark-new-in-v4-0-5-span}

デフォルトの構成では、レプリケーションタスクで出力されるTiCDC Open Protocolの行変更イベントには変更された値のみが含まれ、変更前の値は含まれません。したがって、出力値は、行変更イベントの履歴値としてTiCDCOpenProtocolのコンシューマー側で使用することはできません。

v4.0.5以降、TiCDCは行変更イベントの履歴値の出力をサポートします。この機能を有効にするには、ルートレベルの`changefeed`の構成ファイルで次の構成を指定します。

{{< copyable "" >}}

```toml
enable-old-value = true
```

この機能は、v5.0以降デフォルトで有効になっています。この機能を有効にした後のTiCDCOpenProtocolの出力形式については、 [TiCDCオープンプロトコル-行変更イベント](/ticdc/ticdc-open-protocol.md#row-changed-event)を参照してください。

## 照合用の新しいフレームワークを有効にしてテーブルを複製する {#replicate-tables-with-the-new-framework-for-collations-enabled}

v4.0.15、v5.0.4、v5.1.1、およびv5.2.0以降、TiCDCは[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にしたテーブルをサポートします。

## 有効なインデックスなしでテーブルを複製する {#replicate-tables-without-a-valid-index}

v4.0.8以降、TiCDCは、タスク構成を変更することにより、有効なインデックスを持たないテーブルの複製をサポートします。この機能を有効にするには、 `changefeed`の構成ファイルで次のように構成します。

{{< copyable "" >}}

```toml
enable-old-value = true
force-replicate = true
```

> **警告：**
>
> 有効なインデックスのないテーブルの場合、 `INSERT`や`REPLACE`などの操作は再入可能ではないため、データが冗長になるリスクがあります。 TiCDCは、レプリケーションプロセス中にデータが少なくとも1回だけ配布されることを保証します。したがって、この機能を有効にして有効なインデックスなしでテーブルを複製できるようにすると、データの冗長性が確実に発生します。データの冗長性を受け入れない場合は、 `AUTO RANDOM`属性を持つ主キー列を追加するなど、効果的なインデックスを追加することをお勧めします。

## ユニファイドソーター {#unified-sorter}

ユニファイドソーターは、TiCDCのソーティングエンジンです。次のシナリオによって引き起こされるOOMの問題を軽減できます。

-   TiCDCのデータ複製タスクは長時間一時停止されます。その間、大量の増分データが蓄積され、複製する必要があります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要があります。

v4.0.13以降に`cdc cli`を使用して作成されたチェンジフィードの場合、UnifiedSorterはデフォルトで有効になっています。 v4.0.13より前に存在していたチェンジフィードの場合、以前の構成が使用されます。

チェンジフィードでユニファイドソーター機能が有効になっているかどうかを確認するには、次のコマンド例を実行できます（PDインスタンスのIPアドレスが`http://10.0.10.25:2379`であると想定）。

{{< copyable "" >}}

```shell
cdc cli --pd="http://10.0.10.25:2379" changefeed query --changefeed-id=simple-replication-task | grep 'sort-engine'
```

上記のコマンドの出力で、値`sort-engine`が「unified」の場合、チェンジフィードでUnifiedSorterが有効になっていることを意味します。

> **ノート：**
>
> -   サーバーで、待ち時間が長いか帯域幅が制限されている機械式ハードドライブやその他のストレージデバイスを使用している場合は、統合ソーターの使用に注意してください。
> -   デフォルトでは、UnifiedSorterは`data_dir`を使用して一時ファイルを保存します。空きディスク容量が500GiB以上であることを確認することをお勧めします。実稼働環境では、各ノードの空きディスク容量が（ビジネスで許可されている最大`checkpoint-ts`の遅延）*（ビジネスのピーク時のアップストリーム書き込みトラフィック）よりも大きいことを確認することをお勧めします。さらに、 `changefeed`が作成された後に大量の履歴データを複製する場合は、各ノードの空き領域が複製されたデータの量よりも大きいことを確認してください。
> -   統合ソーターはデフォルトで有効になっています。サーバーが上記の要件に一致せず、統合ソーターを無効にする場合は、チェンジフィードに`sort-engine`から`memory`を手動で設定する必要があります。
> -   `memory`を使用してソートする既存のチェンジフィードでUnifiedSorterを有効にするには、 [タスクの中断後にTiCDCが再起動された後に発生するOOMを処理するにはどうすればよいですか？](/ticdc/troubleshoot-ticdc.md#what-should-i-do-to-handle-the-oom-that-occurs-after-ticdc-is-restarted-after-a-task-interruption)で提供されているメソッドを参照してください。

## 災害シナリオでの結果整合性レプリケーション {#eventually-consistent-replication-in-disaster-scenarios}

> **警告：**
>
> 現在、災害シナリオで結果整合性のあるレプリケーションを使用することはお勧めしません。詳細については、 [重大なバグ＃6189](https://github.com/pingcap/tiflow/issues/6189)を参照してください。

v5.3.0以降、TiCDCは、アップストリームTiDBクラスタからS3ストレージまたはダウンストリームクラスタのNFSファイルシステムへのインクリメンタルデータのバックアップをサポートします。アップストリームクラスタで災害が発生して使用できなくなった場合、TiCDCはダウンストリームデータを結果整合性のある最近の状態に復元できます。これは、TiCDCによって提供される結果整合性のあるレプリケーション機能です。この機能を使用すると、アプリケーションをダウンストリームクラスタにすばやく切り替えることができ、長時間のダウンタイムを回避し、サービスの継続性を向上させることができます。

現在、TiCDCは、増分データをTiDBクラスタから別のTiDBクラスタまたはMySQL互換データベースシステム（ Aurora、MySQL、MariaDBを含む）に複製できます。アップストリームクラスタがクラッシュした場合、災害前のTiCDCのレプリケーションステータスは正常であり、レプリケーションラグが小さいという条件で、TiCDCは5分以内にダウンストリームクラスタのデータを復元できます。これにより、最大で10秒のデータ損失が可能になります。つまり、RTO &lt;= 5分、P95 RPO&lt;=10秒です。

TiCDCレプリケーションラグは、次のシナリオで増加します。

-   TPSは短時間で大幅に増加します
-   大規模または長いトランザクションがアップストリームで発生します
-   アップストリームのTiKVまたはTiCDCクラスタがリロードまたはアップグレードされます
-   `add index`などの時間のかかるDDLステートメントはアップストリームで実行されます
-   PDは積極的なスケジューリング戦略で構成されているため、リージョンリーダーが頻繁に異動したり、リージョンのマージや分割が頻繁に行われたりします。

### 前提条件 {#prerequisites}

-   TiCDCのリアルタイムインクリメンタルデータバックアップファイルを保存するための高可用性AmazonS3ストレージまたはNFSシステムを準備します。これらのファイルは、プライマリクラスタの障害が発生した場合にアクセスできます。
-   災害シナリオで結果整合性が必要なチェンジフィードに対してこの機能を有効にします。これを有効にするには、チェンジフィード構成ファイルに次の構成を追加します。

```toml
[consistent]
# Consistency level. Options include:
# - none: the default value. In a non-disaster scenario, eventual consistency is only guaranteed if and only if finished-ts is specified.
# - eventual: Uses redo log to guarantee eventual consistency in case of the primary cluster disasters.
level = "eventual"

# Individual redo log file size, in MiB. By default, it's 64. It is recommended to be no more than 128.
max-log-size = 64

# The interval for flushing or uploading redo logs to S3, in milliseconds. By default, it's 1000. The recommended range is 500-2000.
flush-interval = 1000

# Form of storing redo log, including nfs (NFS directory) and S3 (uploading to S3).
storage = "s3://logbucket/test-changefeed?endpoint=http://$S3_ENDPOINT/"
```

### 災害からの回復 {#disaster-recovery}

プライマリクラスタで災害が発生した場合は、 `cdc redo`コマンドを実行してセカンダリクラスタで手動で回復する必要があります。復旧プロセスは以下のとおりです。

1.  すべてのTiCDCプロセスが終了したことを確認します。これは、データリカバリ中にプライマリクラスタがサービスを再開するのを防ぎ、TiCDCがデータ同期を再開するのを防ぐためです。
2.  データ回復にはcdcバイナリを使用します。次のコマンドを実行します。

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

このコマンドの場合：

-   `tmp-dir` ：TiCDCインクリメンタルデータバックアップファイルをダウンロードするための一時ディレクトリを指定します。
-   `storage` ：AmazonS3ストレージまたはNFSディレクトリのいずれかのTiCDCインクリメンタルデータバックアップファイルを保存するためのアドレスを指定します。
-   `sink-uri` ：データを復元するセカンダリクラスタアドレスを指定します。スキームは`mysql`のみです。
