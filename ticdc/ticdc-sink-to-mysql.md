---
title: Replicate Data to MySQL-compatible Databases
summary: Learn how to replicate data to TiDB or MySQL using TiCDC.
---

# MySQL 互換データベースへのデータの複製 {#replicate-data-to-mysql-compatible-databases}

このドキュメントでは、TiCDC を使用して、増分データを下流の TiDB データベースまたはその他の MySQL 互換データベースに複製する方法について説明します。また、災害シナリオで結果整合性レプリケーション機能を使用する方法も紹介します。

## レプリケーション タスクを作成する {#create-a-replication-task}

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

-   `--changefeed-id` : レプリケーション タスクの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。
-   `--sink-uri` : レプリケーション タスクのダウンストリーム アドレス。詳細については、 [`mysql` / <code>tidb</code>でシンク URI を構成する](#configure-sink-uri-for-mysql-or-tidb)を参照してください。
-   `--start-ts` : 変更フィードの開始 TSO を指定します。この TSO から、TiCDC クラスターはデータのプルを開始します。デフォルト値は現在の時刻です。
-   `--target-ts` : changefeed の終了 TSO を指定します。この TSO に対して、TiCDC クラスターはデータのプルを停止します。デフォルト値は空です。これは、TiCDC がデータのプルを自動的に停止しないことを意味します。
-   `--config` : changefeed 構成ファイルを指定します。詳細については、 [TiCDC Changefeedコンフィグレーションパラメータ](/ticdc/ticdc-changefeed-config.md)を参照してください。

## MySQL または TiDB のシンク URI を構成する {#configure-sink-uri-for-mysql-or-tidb}

シンク URI は、TiCDC ターゲット システムの接続情報を指定するために使用されます。形式は次のとおりです。

```
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

> **ノート：**
>
> `/path`は MySQL シンクには使用されません。

MySQL の設定例:

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306"
```

以下は、MySQL または TiDB 用に構成できるシンク URI パラメーターとパラメーター値の説明です。

| パラメータ/パラメータ値            | 説明                                                                                                                                                                                                                                     |
| :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root`                  | ダウンストリーム データベースのユーザー名。                                                                                                                                                                                                                 |
| `123456`                | ダウンストリーム データベースのパスワード (Base64 を使用してエンコードできます)。                                                                                                                                                                                         |
| `127.0.0.1`             | ダウンストリーム データベースの IP アドレス。                                                                                                                                                                                                              |
| `3306`                  | ダウンストリーム データのポート。                                                                                                                                                                                                                      |
| `worker-count`          | ダウンストリームに対して同時に実行できる SQL ステートメントの数 (オプション、既定では`16` )。                                                                                                                                                                                  |
| `max-txn-row`           | ダウンストリームに対して実行できるトランザクション バッチのサイズ (オプション、既定では`256` )。                                                                                                                                                                                  |
| `ssl-ca`                | ダウンストリームの MySQL インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)。                                                                                                                                                                               |
| `ssl-cert`              | ダウンストリームの MySQL インスタンスに接続するために必要な証明書ファイルのパス (オプション)。                                                                                                                                                                                   |
| `ssl-key`               | ダウンストリームの MySQL インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)。                                                                                                                                                                                |
| `time-zone`             | ダウンストリームの MySQL インスタンスに接続するときに使用されるタイム ゾーン。v4.0.8 以降で有効です。これはオプションのパラメーターです。このパラメーターが指定されていない場合、TiCDC サービス プロセスのタイム ゾーンが使用されます。このパラメータが空の値に設定されている場合、TiCDC がダウンストリームの MySQL インスタンスに接続するときにタイム ゾーンが指定されず、ダウンストリームのデフォルトのタイム ゾーンが使用されます。 |
| `transaction-atomicity` | トランザクションの原子性レベル。これはオプションのパラメーターで、デフォルト値は`none`です。値が`table`場合、TiCDC は単一テーブル トランザクションの原子性を保証します。値が`none`の場合、TiCDC は単一テーブル トランザクションを分割します。                                                                                                |

Base64 を使用してシンク URI のデータベース パスワードをエンコードするには、次のコマンドを使用します。

```shell
echo -n '123456' | base64   # '123456' is the password to be encoded.
```

エンコードされたパスワードは`MTIzNDU2`です:

```shell
MTIzNDU2
```

> **ノート：**
>
> シンク URI に`! * ' ( ) ; : @ & = + $ , / ? % # [ ]`などの特殊文字が含まれている場合は、特殊文字をエスケープする必要があります (たとえば、 [URI エンコーダー](https://meyerweb.com/eric/tools/dencoder/)など)。

## 災害シナリオにおける結果整合性レプリケーション {#eventually-consistent-replication-in-disaster-scenarios}

v6.1.1 以降、この機能は GA になります。 v5.3.0 以降、TiCDC はアップストリーム TiDB クラスターからオブジェクトstorageまたはダウンストリーム クラスターの NFS への増分データのバックアップをサポートします。アップストリーム クラスターが災害に遭遇して利用できなくなった場合、TiCDC はダウンストリーム データを最新の結果整合性のある状態に復元できます。これは、TiCDC が提供する結果整合性のあるレプリケーション機能です。この機能を使用すると、アプリケーションをダウンストリーム クラスターにすばやく切り替えて、長時間のダウンタイムを回避し、サービスの継続性を向上させることができます。

現在、TiCDC は、TiDB クラスターから別の TiDB クラスターまたは MySQL 互換データベース システム ( Aurora、MySQL、および MariaDB を含む) に増分データを複製できます。アップストリーム クラスターがクラッシュした場合、クラッシュ前に TiCDC がデータを正常にレプリケートし、レプリケーション ラグが小さいという条件があれば、TiCDC は 5 分以内にダウンストリーム クラスターのデータを復元できます。最大で 10 秒のデータ損失が許容されます。つまり、RTO &lt;= 5 分、および P95 RPO &lt;= 10 秒です。

次のシナリオでは、TiCDC のレプリケーション ラグが増加します。

-   短時間でTPSが大幅に上昇します。
-   アップストリームで大規模または長いトランザクションが発生します。
-   アップストリームの TiKV または TiCDC クラスターがリロードまたはアップグレードされます。
-   `add index`などの時間のかかる DDL ステートメントは、アップストリームで実行されます。
-   PD は積極的なスケジューリング戦略で構成されているため、リージョンのリーダーが頻繁に移動したり、リージョンのリージョンや分割が頻繁に発生したりします。

> **ノート：**
>
> v6.1.1 以降、TiCDC の結果整合性レプリケーション機能は、Amazon S3 互換のオブジェクトstorageをサポートします。 v6.1.4 以降、この機能は GCS および Azure 互換のオブジェクトstorageをサポートします。

### 前提条件 {#prerequisites}

-   TiCDC のリアルタイム増分データ バックアップ ファイルを格納するために、高可用性オブジェクトstorageまたは NFS を準備します。これらのファイルは、上流で災害が発生した場合にアクセスできます。
-   災害シナリオで結果整合性を確保する必要がある変更フィードに対して、この機能を有効にします。これを有効にするには、changefeed 構成ファイルに次の構成を追加します。

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
-   `storage` : TiCDC 増分データ バックアップ ファイルを格納するためのアドレスを、オブジェクトstorageの URI または NFS ディレクトリのいずれかで指定します。
-   `sink-uri` : データを復元するセカンダリ クラスタ アドレスを指定します。スキームは`mysql`のみです。
