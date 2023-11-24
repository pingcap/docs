---
title: Replicate Data to MySQL-compatible Databases
summary: Learn how to replicate data to TiDB or MySQL using TiCDC.
---

# MySQL 互換データベースへのデータのレプリケーション {#replicate-data-to-mysql-compatible-databases}

このドキュメントでは、TiCDC を使用して増分データをダウンストリーム TiDB データベースまたは他の MySQL 互換データベースにレプリケートする方法について説明します。また、災害シナリオで結果整合性のあるレプリケーション機能を使用する方法も紹介します。

## レプリケーションタスクを作成する {#create-a-replication-task}

次のコマンドを実行して、レプリケーション タスクを作成します。

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="mysql://root:123456@127.0.0.1:3306/" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

-   `--server` : TiCDC クラスター内の任意の TiCDCサーバーのアドレス。
-   `--changefeed-id` : レプリケーション タスクの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は UUID (バージョン 4 形式) を ID として自動的に生成します。
-   `--sink-uri` : レプリケーションタスクの下流アドレス。詳細は[`mysql` / `tidb`でシンク URI を設定する](#configure-sink-uri-for-mysql-or-tidb)を参照してください。
-   `--start-ts` : チェンジフィードの開始 TSO を指定します。この TSO から、TiCDC クラスターはデータのプルを開始します。デフォルト値は現在時刻です。
-   `--target-ts` : チェンジフィードの終了 TSO を指定します。この TSO に対して、TiCDC クラスターはデータのプルを停止します。デフォルト値は空です。これは、TiCDC がデータのプルを自動的に停止しないことを意味します。
-   `--config` : チェンジフィード構成ファイルを指定します。詳細は[TiCDC Changefeedコンフィグレーションパラメータ](/ticdc/ticdc-changefeed-config.md)を参照してください。

## MySQL または TiDB のシンク URI を構成する {#configure-sink-uri-for-mysql-or-tidb}

シンク URI は、TiCDC ターゲット システムの接続情報を指定するために使用されます。形式は次のとおりです。

    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]

> **注記：**
>
> `/path`は MySQL シンクには使用されません。

MySQL のサンプル構成:

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306"
```

以下は、MySQL または TiDB 用に構成できるシンク URI パラメーターとパラメーター値の説明です。

| パラメータ/パラメータ値            | 説明                                                                                                                                                                                                                                                   |
| :---------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root`                  | ダウンストリーム データベースのユーザー名。                                                                                                                                                                                                                               |
| `123456`                | ダウンストリーム データベースのパスワード (Base64 を使用してエンコード可能)。                                                                                                                                                                                                         |
| `127.0.0.1`             | ダウンストリーム データベースの IP アドレス。                                                                                                                                                                                                                            |
| `3306`                  | ダウンストリーム データ用のポート。                                                                                                                                                                                                                                   |
| `worker-count`          | ダウンストリームに対して同時に実行できる SQL ステートメントの数 (オプション、デフォルトでは`16` )。                                                                                                                                                                                             |
| `cache-prep-stmts`      | ダウンストリームで SQL を実行するときにプリペアド ステートメントを使用し、クライアント側でプリペアドステートメントキャッシュを有効にするかどうかを制御します (オプション、デフォルトでは`true` )。                                                                                                                                            |
| `max-txn-row`           | ダウンストリームに対して実行できるトランザクション バッチのサイズ (オプション、デフォルトでは`256` )。                                                                                                                                                                                             |
| `ssl-ca`                | ダウンストリーム MySQL インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)。                                                                                                                                                                                              |
| `ssl-cert`              | ダウンストリーム MySQL インスタンスに接続するために必要な証明書ファイルのパス (オプション)。                                                                                                                                                                                                  |
| `ssl-key`               | ダウンストリーム MySQL インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)。                                                                                                                                                                                               |
| `time-zone`             | ダウンストリーム MySQL インスタンスに接続するときに使用されるタイム ゾーン。v4.0.8 以降で有効です。これはオプションのパラメータです。このパラメータが指定されていない場合は、TiCDC サービス プロセスのタイム ゾーンが使用されます。このパラメータが`time-zone=""`などの空の値に設定されている場合、TiCDC がダウンストリーム MySQL インスタンスに接続するときにタイム ゾーンは指定されず、ダウンストリームのデフォルトのタイム ゾーンが使用されます。 |
| `transaction-atomicity` | トランザクションの原子性レベル。これはオプションのパラメーターであり、デフォルト値は`none`です。値が`table`場合、TiCDC は単一テーブル トランザクションのアトミック性を保証します。値が`none`の場合、TiCDC は単一テーブル トランザクションを分割します。                                                                                                         |

Base64 を使用してシンク URI のデータベース パスワードをエンコードするには、次のコマンドを使用します。

```shell
echo -n '123456' | base64   # '123456' is the password to be encoded.
```

エンコードされたパスワードは`MTIzNDU2`です。

```shell
MTIzNDU2
```

> **注記：**
>
> シンク URI に`! * ' ( ) ; : @ & = + $ , / ? % # [ ]`などの特殊文字が含まれている場合は、特殊文字をエスケープする必要があります (たとえば、 [URIエンコーダ](https://www.urlencoder.org/) 。

## 災害シナリオにおける最終的に整合性のあるレプリケーション {#eventually-consistent-replication-in-disaster-scenarios}

v6.1.1 以降、この機能は GA になります。 v5.3.0 以降、TiCDC は、アップストリーム TiDB クラスターからダウンストリーム クラスターのオブジェクトstorageまたは NFS への増分データのバックアップをサポートします。アップストリーム クラスターが災害に遭遇して使用できなくなった場合、TiCDC はダウンストリーム データを最近の結果的に整合性のある状態に復元できます。これは、TiCDC によって提供される結果的に整合性のあるレプリケーション機能です。この機能を使用すると、アプリケーションをダウンストリーム クラスターに迅速に切り替えることができるため、長時間のダウンタイムが回避され、サービスの継続性が向上します。

現在、TiCDC は、TiDB クラスターから別の TiDB クラスターまたは MySQL 互換データベース システム ( Aurora、MySQL、MariaDB を含む) に増分データをレプリケートできます。アップストリーム クラスターがクラッシュした場合、TiCDC がクラッシュ前にデータを正常にレプリケートし、レプリケーション ラグが小さいという条件があれば、TiCDC は 5 分以内にダウンストリーム クラスターにデータを復元できます。最大 10 秒のデータ損失が許容されます。つまり、RTO &lt;= 5 分、P95 RPO &lt;= 10 秒です。

TiCDC レプリケーション ラグは、次のシナリオで増加します。

-   TPSは短時間で大幅に増加します。
-   大規模または長時間のトランザクションは上流で発生します。
-   アップストリームの TiKV または TiCDC クラスターがリロードまたはアップグレードされます。
-   `add index`などの時間のかかる DDL ステートメントは、アップストリームで実行されます。
-   PD は積極的なスケジューリング戦略を使用して構成されているため、リージョンリーダーの頻繁な異動、またはリージョンのマージまたはリージョンの分割が頻繁に発生します。

> **注記：**
>
> v6.1.1 以降、TiCDC の結果整合性のあるレプリケーション機能は、Amazon S3 互換のオブジェクトstorageをサポートします。 v6.1.4 以降、この機能は GCS および Azure 互換のオブジェクトstorageをサポートします。

### 前提条件 {#prerequisites}

-   TiCDC のリアルタイム増分データ バックアップ ファイルを保存するために、高可用性オブジェクトstorageまたは NFS を準備します。これらのファイルは、上流で災害が発生した場合にアクセスできます。
-   災害シナリオで結果整合性が必要な変更フィードに対してこの機能を有効にします。これを有効にするには、次の構成を変更フィード構成ファイルに追加します。

```toml
[consistent]
# Consistency level. Options include:
# - none: the default value. In a non-disaster scenario, eventual consistency is only guaranteed if and only if finished-ts is specified.
# - eventual: Uses redo log to guarantee eventual consistency in case of the primary cluster disasters.
level = "eventual"

# Individual redo log file size, in MiB. By default, it's 64. It is recommended to be no more than 128.
max-log-size = 64

# The interval for flushing or uploading redo logs to Amazon S3, in milliseconds. It is recommended that this configuration be equal to or greater than 2000.
flush-interval = 2000

# The path under which redo log backup is stored. The scheme can be nfs (NFS directory), or Amazon S3, GCS, and Azure (uploaded to object storage).
storage = "$SCHEME://logbucket/test-changefeed?endpoint=http://$ENDPOINT/"
```

### 災害からの回復 {#disaster-recovery}

プライマリ クラスタで災害が発生した場合は、 `cdc redo`コマンドを実行してセカンダリ クラスタで手動で回復する必要があります。回復プロセスは次のとおりです。

1.  すべての TiCDC プロセスが終了していることを確認します。これは、データリカバリ中にプライマリクラスターがサービスを再開しないようにし、TiCDC がデータ同期を再開しないようにするためです。
2.  データ回復には cdc バイナリを使用します。次のコマンドを実行します。

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

このコマンドでは次のようになります。

-   `tmp-dir` : TiCDC 増分データ バックアップ ファイルをダウンロードするための一時ディレクトリを指定します。
-   `storage` : TiCDC 増分データ バックアップ ファイルを保存するアドレス (オブジェクトstorageの URI または NFS ディレクトリのいずれか) を指定します。
-   `sink-uri` : データを復元するセカンダリ クラスター アドレスを指定します。スキームは`mysql`のみです。
