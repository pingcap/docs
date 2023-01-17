---
title: Manage TiCDC Cluster and Replication Tasks
summary: Learn how to manage a TiCDC cluster and replication tasks.
---

# TiCDCクラスタとレプリケーション タスクの管理 {#manage-ticdc-cluster-and-replication-tasks}

このドキュメントでは、TiUP を使用してTiUPクラスターをアップグレードし、TiCDC クラスターの構成を変更する方法、およびコマンドライン ツールを使用して TiCDC クラスターとレプリケーション タスクを管理する方法について説明します`cdc cli` 。

HTTP インターフェイス (TiCDC OpenAPI 機能) を使用して、TiCDC クラスターとレプリケーション タスクを管理することもできます。詳細については、 [TiCDC OpenAPI](/ticdc/ticdc-open-api.md)を参照してください。

## TiUP を使用してTiUPをアップグレードする {#upgrade-ticdc-using-tiup}

このセクションでは、TiUP を使用してTiUPクラスターをアップグレードする方法を紹介します。次の例では、TiCDC と TiDB クラスター全体を v5.4.3 にアップグレードする必要があると想定しています。

{{< copyable "" >}}

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> v5.4.3
```

### バージョンアップ時の注意事項 {#notes-for-upgrade}

-   `changefeed`の構成は、TiCDC v4.0.2 で変更されました。詳細は[構成ファイルの互換性に関する注意事項](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)を参照してください。
-   問題が発生した場合は、 [TiUP を使用してTiUPをアップグレードする -FAQ](/upgrade-tidb-using-tiup.md#faq)を参照してください。

## TiUP を使用してTiUP構成を変更する {#modify-ticdc-configuration-using-tiup}

このセクションでは、 TiUPの[`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用して、TiCDC クラスターの構成を変更する方法を紹介します。次の例では、値`gc-ttl`をデフォルトの`86400`から`3600` 、つまり 1 時間に変更します。

まず、次のコマンドを実行します。 `<cluster-name>`を実際のクラスター名に置き換える必要があります。

{{< copyable "" >}}

```shell
tiup cluster edit-config <cluster-name>
```

次に、vi エディター ページに入り、 [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs)の下の`cdc`構成を変更します。構成を以下に示します。

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

変更後、 `tiup cluster reload -R cdc`コマンドを実行して設定をリロードします。

## TLS を使用する {#use-tls}

暗号化データ転送 (TLS) の使用について詳しくは、 [TiDB コンポーネント間の TLS を有効にする](/enable-tls-between-components.md)を参照してください。

## <code>cdc cli</code>を使用してクラスターのステータスとデータ複製タスクを管理する {#use-code-cdc-cli-code-to-manage-cluster-status-and-data-replication-task}

このセクションでは、 `cdc cli`を使用して TiCDC クラスターとデータ複製タスクを管理する方法を紹介します。 `cdc cli`は、 `cdc`バイナリを使用して実行される`cli`サブコマンドです。以下の説明では、次のことを前提としています。

-   `cli`コマンドは`cdc`バイナリを使用して直接実行されます。
-   PD は`10.0.10.25`でリッスンし、ポートは`2379`です。

> **ノート：**
>
> PD が listen する IP アドレスとポートは、 `pd-server`始動時に指定された`advertise-client-urls`パラメーターに対応します。複数の`pd-server`には複数の`advertise-client-urls`パラメータがあり、1 つまたは複数のパラメータを指定できます。たとえば、 `--pd=http://10.0.10.25:2379`または`--pd=http://10.0.10.25:2379,http://10.0.10.26:2379,http://10.0.10.27:2379`です。

TiUP を使用してTiUPをデプロイする場合は、次のコマンドの`cdc cli`を`tiup ctl:<cluster-version> cdc`に置き換えます。

### TiCDC サービスの進行状況を管理する ( <code>capture</code> ) {#manage-ticdc-service-progress-code-capture-code}

-   `capture`のリストをクエリします。

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

    -   `id` : サービス プロセスの ID。
    -   `is-owner` : サービスプロセスがオーナーノードかどうかを示します。
    -   `address` : サービス プロセスが外部へのインターフェイスを提供するためのアドレス。

### レプリケーション タスクの管理 ( <code>changefeed</code> ) {#manage-replication-tasks-code-changefeed-code}

#### レプリケーション タスクの状態転送 {#state-transfer-of-replication-tasks}

レプリケーション タスクの状態は、レプリケーション タスクの実行ステータスを表します。 TiCDC の実行中に、レプリケーション タスクがエラーで失敗したり、手動で一時停止、再開したり、指定された`TargetTs`に達したりする場合があります。これらの動作により、レプリケーション タスクの状態が変化する可能性があります。このセクションでは、TiCDC レプリケーション タスクの状態と、状態間の転送関係について説明します。

![TiCDC state transfer](/media/ticdc/ticdc-state-transfer.png)

上記の状態遷移図の状態は、次のように説明されています。

-   `Normal` : レプリケーション タスクは正常に実行され、checkpoint-ts は正常に進行します。
-   `Stopped` : ユーザーが変更フィードを手動で一時停止したため、レプリケーション タスクは停止されています。この状態の変更フィードは、GC 操作をブロックします。
-   `Error` : レプリケーション タスクはエラーを返します。いくつかの回復可能なエラーが原因で、レプリケーションを続行できません。この状態の changefeed は、状態が`Normal`に移行するまで再開を試み続けます。この状態の変更フィードは、GC 操作をブロックします。
-   `Finished` : レプリケーション タスクが完了し、プリセット`TargetTs`に達しました。この状態の変更フィードは、GC 操作をブロックしません。
-   `Failed` : レプリケーション タスクは失敗します。一部の回復不能なエラーが原因で、レプリケーション タスクを再開できず、回復できません。この状態の変更フィードは、GC 操作をブロックしません。

上記の状態遷移図の番号は、次のように記述されます。

-   ① `changefeed pause`コマンドを実行します。
-   ② `changefeed resume`コマンドを実行し、レプリケーションタスクを再開します。
-   ③ `changefeed`動作中に回復可能なエラーが発生し、自動的に動作が再開されます。
-   ④ `changefeed resume`コマンドを実行して、レプリケーションタスクを再開します。
-   ⑤ `changefeed`目の操作で回復不可能なエラーが発生した。
-   ⑥ `changefeed`がプリセット`TargetTs`に到達し、レプリケーションが自動的に停止されます。
-   ⑦ `changefeed`は`gc-ttl`で指定された期間を超えて停止し、再開することはできません。
-   ⑧ `changefeed`は、自動回復を実行しようとしたときに、回復不能なエラーが発生しました。

#### レプリケーション タスクを作成する {#create-a-replication-task}

次のコマンドを実行して、レプリケーション タスクを作成します。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

-   `--changefeed-id` : レプリケーション タスクの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`の正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。

-   `--sink-uri` : レプリケーション タスクのダウンストリーム アドレス。 `--sink-uri`を次の形式に従って構成します。現在、スキームは`mysql` / `tidb` / `kafka` / `pulsar` / `s3` / `local`をサポートしています。

    {{< copyable "" >}}

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    URI に特殊文字が含まれている場合、URL エンコーディングを使用してこれらの特殊文字を処理する必要があります。

-   `--start-ts` : `changefeed`の開始 TSO を指定します。この TSO から、TiCDC クラスターはデータのプルを開始します。デフォルト値は現在の時刻です。

-   `--target-ts` : `changefeed`の終了 TSO を指定します。この TSO に対して、TiCDC クラスターはデータのプルを停止します。デフォルト値は空です。これは、TiCDC がデータのプルを自動的に停止しないことを意味します。

-   `--sort-engine` : `changefeed`のソート エンジンを指定します。 TiDB と TiKV は分散アーキテクチャを採用しているため、TiCDC はデータの変更をシンクに書き込む前にソートする必要があります。このオプションは`unified` (デフォルト)/ `memory` / `file`をサポートします。

    -   `unified` : `unified`を使用すると、TiCDC はメモリ内でのデータの並べ替えを優先します。メモリが不足している場合、TiCDC は自動的にディスクを使用して一時データを保存します。これはデフォルト値の`--sort-engine`です。
    -   `memory` : メモリ内のデータ変更をソートします。大量のデータをレプリケートすると OOM が簡単にトリガーされるため、この並べ替えエンジンの使用は**お勧めしません**。
    -   `file` : ディスクを完全に使用して一時データを格納します。この機能は**非推奨です**。<strong>どの</strong>ような状況でも使用することは<strong>お勧めしません</strong>。

-   `--config` : `changefeed`の構成ファイルを指定します。

-   `sort-dir` : ソート エンジンが使用する一時ファイル ディレクトリを指定します。**このオプションは、TiDB v4.0.13、v5.0.3、および v5.1.0 以降ではサポートされていないことに注意してください。もう使用しないでください**。

#### <code>mysql</code> / <code>tidb</code>でシンク URI を構成する {#configure-sink-uri-with-code-mysql-code-code-tidb-code}

サンプル構成:

{{< copyable "" >}}

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000"
```

以下は、 `mysql` / `tidb`を使用してシンク URI に構成できるパラメーターとパラメーター値の説明です。

| パラメータ/パラメータ値   | 説明                                                                                                                                                                                                                                     |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root`         | ダウンストリーム データベースのユーザー名                                                                                                                                                                                                                  |
| `123456`       | ダウンストリーム データベースのパスワード                                                                                                                                                                                                                  |
| `127.0.0.1`    | ダウンストリーム データベースの IP アドレス                                                                                                                                                                                                               |
| `3306`         | ダウンストリーム データのポート                                                                                                                                                                                                                       |
| `worker-count` | ダウンストリームに対して同時に実行できる SQL ステートメントの数 (オプション、既定では`16` )                                                                                                                                                                                   |
| `max-txn-row`  | ダウンストリームに対して実行できるトランザクション バッチのサイズ (オプション、既定では`256` )                                                                                                                                                                                   |
| `ssl-ca`       | ダウンストリームの MySQL インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)                                                                                                                                                                                |
| `ssl-cert`     | ダウンストリームの MySQL インスタンスに接続するために必要な証明書ファイルのパス (オプション)                                                                                                                                                                                    |
| `ssl-key`      | ダウンストリームの MySQL インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)                                                                                                                                                                                 |
| `time-zone`    | ダウンストリームの MySQL インスタンスに接続するときに使用されるタイム ゾーン。v4.0.8 以降で有効です。これはオプションのパラメーターです。このパラメーターが指定されていない場合、TiCDC サービス プロセスのタイム ゾーンが使用されます。このパラメータが空の値に設定されている場合、TiCDC がダウンストリームの MySQL インスタンスに接続するときにタイム ゾーンが指定されず、ダウンストリームのデフォルトのタイム ゾーンが使用されます。 |

#### <code>kafka</code>でシンク URI を構成する {#configure-sink-uri-with-code-kafka-code}

サンプル構成:

{{< copyable "" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

以下は、 `kafka`のシンク URI に構成できるパラメーターとパラメーター値の説明です。

| パラメータ/パラメータ値            | 説明                                                                                                                                                                                |
| :---------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `127.0.0.1`             | ダウンストリーム Kafka サービスの IP アドレス                                                                                                                                                      |
| `9092`                  | 下流の Kafka のポート                                                                                                                                                                    |
| `topic-name`            | 変数。 Kafka トピックの名前                                                                                                                                                                 |
| `kafka-version`         | ダウンストリーム Kafka のバージョン (オプション、デフォルトでは`2.4.0`現在、サポートされている最も古い Kafka バージョンは`0.11.0.2`で、最新のものは`3.1.0`です。この値は、ダウンストリーム Kafka の実際のバージョンと一致する必要があります)                                    |
| `kafka-client-id`       | レプリケーション タスクの Kafka クライアント ID を指定します (オプション。既定では`TiCDC_sarama_producer_replication ID` )。                                                                                         |
| `partition-num`         | ダウンストリーム Kafka パーティションの数 (オプション。値は実際のパーティション数を**超えてはなりません**。そうでない場合、レプリケーション タスクは正常に作成されません。デフォルトでは`3` )                                                                          |
| `max-message-bytes`     | 毎回 Kafka ブローカーに送信されるデータの最大サイズ (オプション、デフォルトでは`10MB` )。 v5.0.6 および v4.0.6 から、デフォルト値が 64MB および 256MB から 10MB に変更されました。                                                               |
| `replication-factor`    | 保存できる Kafka メッセージ レプリカの数 (オプション、既定では`1` )                                                                                                                                         |
| `compression`           | メッセージの送信時に使用される圧縮アルゴリズム (値のオプションは`none` 、 `lz4` 、 `gzip` 、 `snappy` 、および`zstd`で、デフォルトでは`none`です)。                                                                                 |
| `protocol`              | メッセージが Kafka に出力されるプロトコル。値のオプションは`canal-json` 、 `open-protocol` 、 `canal` 、 `avro` 、および`maxwell`です。                                                                               |
| `auto-create-topic`     | 渡された`topic-name`が Kafka クラスターに存在しない場合に、TiCDC がトピックを自動的に作成するかどうかを決定します (オプション、デフォルトでは`true` )。                                                                                     |
| `enable-tidb-extension` | 出力プロトコルが`canal-json`の場合、値が`true`の場合、TiCDC は Resolved イベントを送信し、TiDB 拡張フィールドを Kafka メッセージに追加します。 (オプション、デフォルトで`false` )                                                             |
| `max-batch-size`        | v4.0.9 の新機能。メッセージ プロトコルが 1 つの Kafka メッセージへの複数のデータ変更の出力をサポートしている場合、このパラメーターは 1 つの Kafka メッセージ内のデータ変更の最大数を指定します。現在、Kafka の`protocol`が`open-protocol`の場合にのみ有効です。 (オプション、デフォルトで`16` ) |
| `ca`                    | ダウンストリーム Kafka インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)                                                                                                                            |
| `cert`                  | ダウンストリームの Kafka インスタンスに接続するために必要な証明書ファイルのパス (オプション)                                                                                                                               |
| `key`                   | ダウンストリーム Kafka インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)                                                                                                                             |
| `sasl-user`             | ダウンストリームの Kafka インスタンスに接続するために必要な SASL/SCRAM 認証の ID (authcid) (オプション)                                                                                                             |
| `sasl-password`         | ダウンストリームの Kafka インスタンスに接続するために必要な SASL/SCRAM 認証のパスワード (オプション)                                                                                                                     |
| `sasl-mechanism`        | ダウンストリームの Kafka インスタンスに接続するために必要な SASL/SCRAM 認証の名前 (オプション)                                                                                                                        |

ベストプラクティス：

-   独自の Kafka トピックを作成することをお勧めします。少なくとも、トピックが Kafka ブローカーに送信できる各メッセージの最大データ量と、ダウンストリーム Kafka パーティションの数を設定する必要があります。 changefeed を作成すると、これら 2 つの設定はそれぞれ`max-message-bytes`と`partition-num`に対応します。
-   まだ存在しないトピックで変更フィードを作成すると、TiCDC は`partition-num`と`replication-factor`のパラメーターを使用してトピックを作成しようとします。これらのパラメーターを明示的に指定することをお勧めします。
-   ほとんどの場合、 `canal-json`プロトコルを使用することをお勧めします。

> **ノート：**
>
> `protocol`が`open-protocol`の場合、TiCDC は長さが`max-message-bytes`を超えるメッセージの生成を回避しようとします。ただし、1 つの変更だけで長さが`max-message-bytes`を超えるほど行が大きい場合、サイレント エラーを回避するために、TiCDC はこのメッセージを出力しようとし、ログに警告を出力します。

#### TiCDC を Kafka Connect (コンフルエント プラットフォーム) と統合する {#integrate-ticdc-with-kafka-connect-confluent-platform}

> **警告：**
>
> これはまだ実験的機能です。本番環境では使用し**ない**でください。

サンプル構成:

{{< copyable "" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&protocol=avro&partition-num=6&max-message-bytes=67108864&replication-factor=1"
--opts registry="http://127.0.0.1:8081"
```

Confluent が提供する[データ コネクタ](https://docs.confluent.io/current/connect/managing/connectors.html)を使用してデータをリレーショナル データベースまたは非リレーショナル データベースにストリーミングするには、 `avro`プロトコルを使用して[コンフルエント スキーマ レジストリ](https://www.confluent.io/product/confluent-platform/data-compatibility/) in `opts`の URL を提供する必要があります。 `avro`プロトコルと Confluent の統合は**実験的**ものであることに注意してください。

詳細な統合ガイドについては、 [TiDB と Confluent Platform の統合に関するクイック スタート ガイド](/ticdc/integrate-confluent-using-ticdc.md)を参照してください。

#### <code>pulsar</code>でシンク URI を構成する {#configure-sink-uri-with-code-pulsar-code}

> **警告：**
>
> これはまだ実験的機能です。本番環境では使用し**ない**でください。

サンプル構成:

{{< copyable "" >}}

```shell
--sink-uri="pulsar://127.0.0.1:6650/topic-name?connectionTimeout=2s"
```

以下は、 `pulsar`でシンク URI に構成できるパラメーターの説明です。

| パラメータ                        | 説明                                                                                                                                   |
| :--------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `connectionTimeout`          | ダウンストリーム Pulsar への接続を確立するためのタイムアウト。これはオプションであり、デフォルトは 30 (秒) です。                                                                     |
| `operationTimeout`           | ダウンストリーム Pulsar で操作を実行するためのタイムアウト。これはオプションであり、デフォルトは 30 (秒) です。                                                                      |
| `tlsTrustCertsFilePath`      | ダウンストリームの Pulsar インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)                                                                             |
| `tlsAllowInsecureConnection` | TLS が有効になった後に暗号化されていない接続を許可するかどうかを決定します (オプション)                                                                                      |
| `tlsValidateHostname`        | ダウンストリーム Pulsar からの証明書のホスト名を検証するかどうかを決定します (オプション)                                                                                   |
| `maxConnectionsPerBroker`    | 単一のダウンストリーム Pulsar ブローカーに許可される接続の最大数。これはオプションで、デフォルトは 1 です。                                                                          |
| `auth.tls`                   | TLS モードを使用して、下流のパルサーを検証します (オプション)。たとえば、 `auth=tls&auth.tlsCertFile=/path/to/cert&auth.tlsKeyFile=/path/to/key`です。                   |
| `auth.token`                 | トークン モードを使用して、下流のパルサーを検証します (オプション)。たとえば、 `auth=token&auth.token=secret-token`または`auth=token&auth.file=path/to/secret-token-file`です。 |
| `name`                       | TiCDC のパルサー プロデューサーの名前 (オプション)                                                                                                       |
| `protocol`                   | メッセージがパルサーに出力されるプロトコル。値のオプションは`canal-json` 、 `open-protocol` 、 `canal` 、 `avro` 、および`maxwell`です。                                     |
| `maxPendingMessages`         | 保留中のメッセージ キューの最大サイズを設定します。これはオプションで、デフォルトは 1000 です。たとえば、Pulsar からの確認メッセージを保留します。                                                     |
| `disableBatching`            | バッチでのメッセージの自動送信を無効にします (オプション)                                                                                                       |
| `batchingMaxPublishDelay`    | 送信されたメッセージがバッチ化される期間を設定します (デフォルト: 10ms)                                                                                             |
| `compressionType`            | メッセージの送信に使用される圧縮アルゴリズムを設定します (オプション)。値のオプションは`NONE` 、 `LZ4` 、 `ZLIB` 、および`ZSTD`です。 (デフォルトでは`NONE` )                                  |
| `hashingScheme`              | メッセージの送信先のパーティションを選択するために使用されるハッシュ アルゴリズム (オプション)。値のオプションは`JavaStringHash` (デフォルト) と`Murmur3`です。                                     |
| `properties.*`               | TiCDC の Pulsar プロデューサーに追加されたカスタマイズされたプロパティ (オプション)。たとえば、 `properties.location=Hangzhou`です。                                           |

Pulsar のその他のパラメータについては、 [pulsar-client-go ClientOptions](https://godoc.org/github.com/apache/pulsar-client-go/pulsar#ClientOptions)および[pulsar-client-go ProducerOptions](https://godoc.org/github.com/apache/pulsar-client-go/pulsar#ProducerOptions)を参照してください。

#### タスク構成ファイルを使用する {#use-the-task-configuration-file}

レプリケーション構成の詳細 (単一テーブルのレプリケーションを指定するなど) については、 [タスク構成ファイル](#task-configuration-file)を参照してください。

構成ファイルを使用して、次の方法でレプリケーション タスクを作成できます。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --config changefeed.toml
```

上記のコマンドで、 `changefeed.toml`はレプリケーション タスクの構成ファイルです。

#### レプリケーション タスク リストを照会する {#query-the-replication-task-list}

次のコマンドを実行して、レプリケーション タスク リストを照会します。

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

-   `checkpoint`は、この時点より前に TiCDC が既にデータをダウンストリームにレプリケートしたことを示します。
-   `state`は、レプリケーション タスクの状態を示します。
    -   `normal` : レプリケーション タスクは正常に実行されます。
    -   `stopped` : レプリケーション タスクは停止しています (手動で一時停止)。
    -   `error` : レプリケーション タスクは (エラーにより) 停止されました。
    -   `removed` : レプリケーション タスクは削除されます。この状態のタスクは、オプション`--all`を指定した場合にのみ表示されます。このオプションが指定されていない場合にこれらのタスクを表示するには、 `changefeed query`コマンドを実行します。
    -   `finished` : レプリケーション タスクが完了しました (データは`target-ts`にレプリケートされます)。この状態のタスクは、オプション`--all`を指定した場合にのみ表示されます。このオプションが指定されていない場合にこれらのタスクを表示するには、 `changefeed query`コマンドを実行します。

#### 特定のレプリケーション タスクを照会する {#query-a-specific-replication-task}

特定のレプリケーション タスクを照会するには、 `changefeed query`コマンドを実行します。クエリ結果には、タスク情報とタスク状態が含まれます。 `--simple`または`-s`引数を指定して、基本的なレプリケーション状態とチェックポイント情報のみを含むクエリ結果を簡素化できます。この引数を指定しない場合、詳細なタスク構成、レプリケーション状態、およびレプリケーション テーブル情報が出力されます。

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

上記のコマンドと結果:

-   `state`は、現在の`changefeed`の複製状態です。各状態は`changefeed list`の状態と一致している必要があります。
-   `tso`は、現在の`changefeed`でダウンストリームに正常に複製された最大のトランザクション TSO を表します。
-   `checkpoint`は、ダウンストリームに正常に複製された現在の`changefeed`の最大トランザクション TSO の対応する時間を表します。
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

上記のコマンドと結果:

-   `info`は、照会された`changefeed`の複製構成です。
-   `status`は、照会された`changefeed`の複製状態です。
    -   `resolved-ts` : 現在の`changefeed`の中で最大のトランザクション`TS` 。この`TS`は TiKV から TiCDC に正常に送信されていることに注意してください。
    -   `checkpoint-ts` : 現在の`changefeed`の中で最大のトランザクション`TS` 。この`TS`はダウンストリームに正常に書き込まれていることに注意してください。
    -   `admin-job-type` : `changefeed`のステータス:
        -   `0` : 状態は正常です。
        -   `1` : タスクは一時停止されています。タスクが一時停止すると、レプリケートされたすべての`processor`が終了します。タスクの構成とレプリケーション ステータスが保持されるため、タスクを`checkpiont-ts`から再開できます。
        -   `2` : タスクは再開されます。レプリケーション タスクは`checkpoint-ts`から再開します。
        -   `3` : タスクは削除されます。タスクが削除されると、複製されたすべての`processor`が終了し、複製タスクの構成情報がクリアされます。以降のクエリでは、レプリケーション ステータスのみが保持されます。
-   `task-status`は、照会された`changefeed`の各複製サブタスクの状態を示します。

#### レプリケーション タスクを一時停止する {#pause-a-replication-task}

次のコマンドを実行して、レプリケーション タスクを一時停止します。

{{< copyable "" >}}

```shell
cdc cli changefeed pause --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

上記のコマンドで:

-   `--changefeed-id=uuid`は、一時停止するレプリケーション タスクに対応する`changefeed`の ID を表します。

#### レプリケーション タスクを再開する {#resume-a-replication-task}

次のコマンドを実行して、一時停止したレプリケーション タスクを再開します。

{{< copyable "" >}}

```shell
cdc cli changefeed resume --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

上記のコマンドで:

-   `--changefeed-id=uuid`は、再開するレプリケーション タスクに対応する`changefeed`の ID を表します。

#### レプリケーション タスクを削除する {#remove-a-replication-task}

次のコマンドを実行して、レプリケーション タスクを削除します。

{{< copyable "" >}}

```shell
cdc cli changefeed remove --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

上記のコマンドで:

-   `--changefeed-id=uuid`は、削除するレプリケーション タスクに対応する`changefeed`の ID を表します。

### タスク構成の更新 {#update-task-configuration}

v4.0.4 以降、TiCDC はレプリケーション タスクの構成の変更をサポートしています (動的ではありません)。 `changefeed`構成を変更するには、タスクを一時停止し、構成を変更してから、タスクを再開します。

{{< copyable "" >}}

```shell
cdc cli changefeed pause -c test-cf --pd=http://10.0.10.25:2379
cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

現在、次の構成項目を変更できます。

-   `changefeed`の`sink-uri` 。
-   `changefeed`の構成ファイルと、ファイル内のすべての構成アイテム。
-   ファイルの並べ替え機能と並べ替えディレクトリを使用するかどうか。
-   `changefeed`の`target-ts` 。

### レプリケーション サブタスクの処理単位を管理する ( <code>processor</code> ) {#manage-processing-units-of-replication-sub-tasks-code-processor-code}

-   `processor`のリストをクエリします。

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

-   特定のレプリケーション タスクのステータスに対応する特定の`changefeed`を照会します。

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

    上記のコマンドでは:

    -   `status.tables` : 各キー番号はレプリケーション テーブルの ID を表し、TiDB のテーブルの`tidb_table_id`に対応します。
    -   `resolved-ts` : 現在のプロセッサでソートされたデータの中で最大の TSO。
    -   `checkpoint-ts` : 現在のプロセッサでダウンストリームに正常に書き込まれた最大の TSO。

## タスク構成ファイル {#task-configuration-file}

このセクションでは、レプリケーション タスクの構成について説明します。

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
# Supports four dispatchers: default, ts, rowid, and table.
# The dispatcher rules are as follows:
# - default: When multiple unique indexes (including the primary key) exist or the Old Value feature is enabled, events are dispatched in the table mode. When only one unique index (or the primary key) exists, events are dispatched in the rowid mode.
# - ts: Use the commitTs of the row change to create Hash and dispatch events.
# - index-value: Use the value of the primary key or the unique index of the table to create Hash and dispatch events.
# - table: Use the schema name of the table and the table name to create Hash and dispatch events.
# The matching syntax of matcher is the same as the filter rule syntax.
dispatchers = [
    {matcher = ['test1.*', 'test2.*'], dispatcher = "ts"},
    {matcher = ['test3.*', 'test4.*'], dispatcher = "rowid"},
]
# For the sink of MQ type, you can specify the protocol format of the message.
# Currently the following protocols are supported: canal-json, open-protocol, canal, avro, and maxwell.
protocol = "canal-json"

```

### 互換性に関する注意事項 {#notes-for-compatibility}

-   TiCDC v4.0.0 では、 `ignore-txn-commit-ts`が削除され、 `ignore-txn-start-ts`が追加され、start_ts を使用してトランザクションをフィルタリングします。
-   TiCDC v4.0.2 では、 `db-dbs` / `db-tables` / `ignore-dbs` / `ignore-tables`が削除され、データベースとテーブルに新しいフィルター ルールを使用する`rules`が追加されました。詳細なフィルター構文については、 [テーブル フィルター](/table-filter.md)を参照してください。

## 行変更イベントの履歴値を出力<span class="version-mark">v4.0.5 の新機能</span> {#output-the-historical-value-of-a-row-changed-event-span-class-version-mark-new-in-v4-0-5-span}

デフォルトの構成では、レプリケーション タスクの TiCDC Open Protocol 出力の Row Changed Event には、変更前の値ではなく、変更された値のみが含まれます。したがって、出力値は、TiCDC Open Protocol のコンシューマー側で行変更イベントの履歴値として使用することはできません。

v4.0.5 以降、TiCDC は行変更イベントの履歴値の出力をサポートしています。この機能を有効にするには、ルート レベルの`changefeed`の構成ファイルで次の構成を指定します。

{{< copyable "" >}}

```toml
enable-old-value = true
```

この機能は、v5.0 以降、デフォルトで有効になっています。この機能を有効にした後の TiCDC Open Protocol の出力形式については、 [TiCDC オープン プロトコル - 行変更イベント](/ticdc/ticdc-open-protocol.md#row-changed-event)を参照してください。

## 照合の新しいフレームワークを有効にしてテーブルを複製する {#replicate-tables-with-the-new-framework-for-collations-enabled}

v4.0.15、v5.0.4、v5.1.1、および v5.2.0 以降、TiCDC は[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にしたテーブルをサポートします。

## 有効なインデックスのないテーブルをレプリケートする {#replicate-tables-without-a-valid-index}

v4.0.8 以降、TiCDC は、タスク構成を変更することにより、有効なインデックスを持たないテーブルの複製をサポートします。この機能を有効にするには、 `changefeed`構成ファイルで次のように構成します。

{{< copyable "" >}}

```toml
enable-old-value = true
force-replicate = true
```

> **警告：**
>
> 有効なインデックスのないテーブルの場合、 `INSERT`や`REPLACE`などの操作は再入可能ではないため、データの冗長性が生じるリスクがあります。 TiCDC は、レプリケーション プロセス中に少なくとも 1 回だけデータが分散されることを保証します。したがって、この機能を有効にして、有効なインデックスなしでテーブルをレプリケートすると、確実にデータの冗長性が生じます。データの冗長性を受け入れない場合は、 `AUTO RANDOM`属性を持つ主キー列を追加するなど、効果的なインデックスを追加することをお勧めします。

## ユニファイドソーター {#unified-sorter}

ユニファイド ソーターは、TiCDC のソーティング エンジンです。次のシナリオによって発生する OOM の問題を軽減できます。

-   TiCDC のデータ レプリケーション タスクは長時間一時停止されます。その間、大量の増分データが蓄積され、レプリケートする必要があります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要があります。

v4.0.13 以降の`cdc cli`を使用して作成された変更フィードの場合、Unified Sorter はデフォルトで有効になっています。 v4.0.13 より前に存在していた変更フィードについては、以前の構成が使用されます。

ユニファイド ソーター機能が変更フィードで有効になっているかどうかを確認するには、次のコマンド例を実行します (PD インスタンスの IP アドレスが`http://10.0.10.25:2379`であると仮定します)。

{{< copyable "" >}}

```shell
cdc cli --pd="http://10.0.10.25:2379" changefeed query --changefeed-id=simple-replication-task | grep 'sort-engine'
```

上記のコマンドの出力で、値`sort-engine`が「unified」の場合、変更フィードでユニファイド ソーターが有効になっていることを意味します。

> **ノート：**
>
> -   サーバーが機械式ハード ドライブまたはその他のストレージ デバイスを使用しており、レイテンシーが大きいか帯域幅が限られている場合は、統合ソーターを慎重に使用してください。
> -   デフォルトでは、Unified Sorter は`data_dir`を使用して一時ファイルを保存します。空きディスク容量が 500 GiB 以上であることを確認することをお勧めします。本番環境では、各ノードの空きディスク容量が (ビジネスで許容される最大`checkpoint-ts`遅延) * (ビジネス ピーク時のアップストリーム書き込みトラフィック) より大きいことを確認することをお勧めします。また、 `changefeed`の作成後に大量の履歴データをレプリケートする予定がある場合は、各ノードの空き容量がレプリケートされたデータの量よりも多いことを確認してください。
> -   統合ソーターはデフォルトで有効になっています。サーバーが上記の要件に一致せず、統合ソーターを無効にする場合は、changefeed の`sort-engine`から`memory`を手動で設定する必要があります。
> -   `memory`を使用してソートする既存の変更フィードでユニファイド ソーターを有効にするには、 [タスクの中断後に TiCDC が再起動された後に発生する OOM を処理するにはどうすればよいですか?](/ticdc/troubleshoot-ticdc.md#what-should-i-do-to-handle-the-oom-that-occurs-after-ticdc-is-restarted-after-a-task-interruption)で提供されているメソッドを参照してください。

## 災害シナリオにおける結果整合性レプリケーション {#eventually-consistent-replication-in-disaster-scenarios}

> **警告：**
>
> v5.3.0 および v5.4.0 では、災害シナリオで結果整合性レプリケーションを使用することはお勧めしません。詳細については、 [#6189](https://github.com/pingcap/tiflow/issues/6189)を参照してください。この問題は v6.1.1 以降で修正されています。したがって、v6.1.1 以降のバージョンを使用することをお勧めします。

v5.3.0 以降、TiCDC はアップストリームの TiDB クラスターから S3 ストレージまたはダウンストリーム クラスターの NFS ファイル システムへの増分データのバックアップをサポートします。アップストリーム クラスターが災害に遭遇して利用できなくなった場合、TiCDC はダウンストリーム データを最新の結果整合性のある状態に復元できます。これは、TiCDC が提供する結果整合性のあるレプリケーション機能です。この機能を使用すると、アプリケーションをダウンストリーム クラスターにすばやく切り替えて、長時間のダウンタイムを回避し、サービスの継続性を向上させることができます。

現在、TiCDC は、TiDB クラスターから別の TiDB クラスターまたは MySQL 互換データベース システム ( Aurora、MySQL、および MariaDB を含む) に増分データを複製できます。アップストリーム クラスターがクラッシュした場合、災害前の TiCDC のレプリケーション ステータスが正常であり、レプリケーション ラグが小さいという条件を考えると、TiCDC は 5 分以内にダウンストリーム クラスターのデータを復元できます。最大で 10 秒のデータ損失が許容されます。つまり、RTO &lt;= 5 分、および P95 RPO &lt;= 10 秒です。

次のシナリオでは、TiCDC のレプリケーション ラグが増加します。

-   短時間でTPSが大幅に上昇
-   アップストリームで大規模または長時間のトランザクションが発生する
-   アップストリームの TiKV または TiCDC クラスターがリロードまたはアップグレードされている
-   `add index`などの時間のかかる DDL ステートメントはアップストリームで実行されます。
-   PD は積極的なスケジューリング戦略で構成されているため、リージョンリーダーが頻繁に異動したり、リージョンの合併やリージョンの分割が頻繁に発生したりします。

### 前提条件 {#prerequisites}

-   TiCDC のリアルタイム増分データ バックアップ ファイルを格納するために、高可用性 Amazon S3 ストレージまたは NFS システムを準備します。これらのファイルには、プライマリ クラスタの障害が発生した場合にアクセスできます。
-   災害シナリオで結果整合性を確保する必要がある変更フィードに対して、この機能を有効にします。これを有効にするには、changefeed 構成ファイルに次の構成を追加します。

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

主クラスタで障害が発生した場合、 `cdc redo`コマンドを実行して副クラスタで手動で復旧する必要があります。回復プロセスは次のとおりです。

1.  すべての TiCDC プロセスが終了していることを確認します。これは、データ リカバリ中にプライマリ クラスタがサービスを再開するのを防ぎ、TiCDC がデータ同期を再開するのを防ぐためです。
2.  データの回復には cdc バイナリを使用します。次のコマンドを実行します。

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

このコマンドでは:

-   `tmp-dir` : TiCDC 増分データ バックアップ ファイルをダウンロードするための一時ディレクトリを指定します。
-   `storage` : Amazon S3 ストレージまたは NFS ディレクトリのいずれかで、TiCDC 増分データ バックアップ ファイルを保存するためのアドレスを指定します。
-   `sink-uri` : データを復元するセカンダリ クラスタ アドレスを指定します。スキームは`mysql`のみです。
