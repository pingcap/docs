---
title: Replicate Data to MySQL-compatible Databases
summary: TiCDC を使用して TiDB または MySQL にデータを複製する方法を学習します。
---

# MySQL互換データベースにデータを複製する {#replicate-data-to-mysql-compatible-databases}

このドキュメントでは、TiCDCを使用して、下流のTiDBデータベースまたはその他のMySQL互換データベースに増分データをレプリケーションする方法について説明します。また、災害シナリオにおいて結果整合性レプリケーション機能を使用する方法についても紹介します。

## レプリケーションタスクを作成する {#create-a-replication-task}

次のコマンドを実行してレプリケーション タスクを作成します。

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="mysql://root:123456@127.0.0.1:3306/" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2023-11-28T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":false,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

-   `--server` : TiCDC クラスター内の任意の TiCDCサーバーのアドレス。
-   `--changefeed-id` : レプリケーションタスクのID。形式は正規表現`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`に一致する必要があります。このIDが指定されていない場合、TiCDCは自動的にUUID（バージョン4形式）をIDとして生成します。
-   `--sink-uri` : レプリケーションタスクのダウンストリームアドレス。詳細は[`mysql` / `tidb`でシンクURIを設定する](#configure-sink-uri-for-mysql-or-tidb)参照してください。
-   `--start-ts` : チェンジフィードの開始TSOを指定します。このTSOから、TiCDCクラスターはデータのプルを開始します。デフォルト値は現在時刻です。
-   `--target-ts` : チェンジフィードの終了TSOを指定します。このTSOまで、TiCDCクラスターはデータのプルを停止します。デフォルト値は空で、TiCDCはデータのプルを自動的に停止しません。
-   `--config` : changefeed設定ファイルを指定します。詳細は[TiCDC Changefeedコンフィグレーションパラメータ](/ticdc/ticdc-changefeed-config.md)参照してください。

> **注記：**
>
> -   TiCDCは増分データのみを複製します。完全なデータを初期化するには、 Dumpling/ TiDB LightningまたはBRを使用してください。
> -   フルデータが初期化された後、上流バックアップを実行する際にTSOとして`start-ts`指定する必要があります。例えば、 Dumplingディレクトリ下のメタデータファイル内の値`pos` 、またはBRがバックアップを完了した後に出力されるログ内の値`backupTS`です。

## MySQL または TiDB のシンク URI を構成する {#configure-sink-uri-for-mysql-or-tidb}

シンクURIは、TiCDCターゲットシステムの接続情報を指定するために使用されます。形式は次のとおりです。

    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]

> **注記：**
>
> `/path`は MySQL シンクには使用されません。

MySQL のサンプル構成:

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306"
```

以下は、MySQL または TiDB に対して構成できるシンク URI パラメータとパラメータ値の説明です。

| パラメータ/パラメータ値                | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root`                      | ダウンストリームデータベースのユーザー名。TiDBまたはその他のMySQL互換データベースにデータを複製するには、ダウンストリームデータベースのユーザーに[特定の権限](#permissions-required-for-the-downstream-database-user)あることを確認してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `123456`                    | ダウンストリーム データベースのパスワード (Base64 を使用してエンコードできます)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `127.0.0.1`                 | ダウンストリーム データベースの IP アドレス。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `3306`                      | ダウンストリーム データベースのポート。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `worker-count`              | ダウンストリームに対して同時に実行できる SQL 文の数 (オプション、デフォルト値は`16` 、最大値は`1024` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `cache-prep-stmts`          | ダウンストリームで SQL を実行するときに準備済みステートメントを使用するかどうか、およびクライアント側でプリペアドステートメントキャッシュを有効にするかどうかを制御します (オプション、デフォルトは`true` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `max-txn-row`               | ダウンストリームに対して実行される SQL ステートメントのバッチ サイズ (オプション、デフォルト値は`256` 、最大値は`2048` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `max-multi-update-row`      | バッチ書き込み( `batch-dml-enable` )が有効な場合に下流に実行される`UPDATE ROWS` SQL文のバッチサイズ。常に`max-txn-row`未満です(オプション、デフォルト値は`40` 、最大値は`256` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `max-multi-update-row-size` | バッチ書き込み（ `batch-dml-enable` ）が有効な場合、下流に実行されるSQL文のサイズ制限`UPDATE ROWS` 。このサイズ制限を超えると、各行は個別のSQL文として実行されます（オプション、デフォルト値は`1024` 、最大値は`8192` ）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `ssl-ca`                    | ダウンストリーム MySQL インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `ssl-cert`                  | ダウンストリーム MySQL インスタンスに接続するために必要な証明書ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `ssl-key`                   | ダウンストリーム MySQL インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `time-zone`                 | 下流のMySQLインスタンスへの接続時に使用するタイムゾーン。v4.0.8以降で有効です。これはオプションパラメータです。このパラメータが指定されていない場合は、TiCDCサービスプロセスのタイムゾーンが使用されます。このパラメータが空の値（ `time-zone=""`など）に設定されている場合、TiCDCが下流のMySQLインスタンスに接続する際にタイムゾーンは指定されず、下流のデフォルトのタイムゾーンが使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `transaction-atomicity`     | トランザクションのアトミック性レベル。これはオプションのパラメータで、デフォルト値は`none`です。値が`table`場合、TiCDC は単一テーブルトランザクションのアトミック性を保証します。値が`none`の場合、TiCDC は単一テーブルトランザクションを分割します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `batch-dml-enable`          | バッチ書き込み (batch-dml) 機能を有効にします (オプション、デフォルト値は`true` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `read-timeout`              | go-sql-driver パラメータ、 [I/O読み取りタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-readtimeout) (オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `write-timeout`             | go-sql-driver パラメータ、 [I/O書き込みタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-writetimeout) (オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `timeout`                   | go-sql-driver パラメータ[接続を確立するためのタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-timeout)はダイヤル タイムアウトとも呼ばれます (オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `tidb-txn-mode`             | [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)環境変数を指定します (オプション、デフォルト値は`optimistic` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `safe-mode`                 | TiCDC がダウンストリームにデータを複製するときに`INSERT`および`UPDATE`ステートメントを処理する方法を指定します。 `true`の場合、 TiCDC はアップストリームの`INSERT`ステートメントをすべて`REPLACE INTO`ステートメントに変換し、 `UPDATE`ステートメントをすべて`DELETE` + `REPLACE INTO`ステートメントに変換します。 v6.1.3 より前では、このパラメーターのデフォルト値は`true`です。 v6.1.3 以降では、デフォルト値は`false`に変更されます。 TiCDC が起動すると、現在のタイムスタンプ`ThresholdTs`取得します。 `CommitTs`が`ThresholdTs`より小さい`INSERT`および`UPDATE`ステートメントの場合、 TiCDC はそれらをそれぞれ`REPLACE INTO`ステートメントと`DELETE` + `REPLACE INTO`ステートメントに変換します。 `CommitTs`が`ThresholdTs`以上である`INSERT`および`UPDATE`ステートメントの場合、 `INSERT`ステートメントはダウンストリームに直接複製されますが、 `UPDATE`ステートメントの動作は[TiCDC の UPDATE イベントの分割動作](/ticdc/ticdc-split-update-behavior.md)に従います。 |

Base64 を使用してシンク URI 内のデータベース パスワードをエンコードするには、次のコマンドを使用します。

```shell
echo -n '123456' | base64   # '123456' is the password to be encoded.
```

エンコードされたパスワードは`MTIzNDU2`です:

```shell
MTIzNDU2
```

> **注記：**
>
> シンク URI に`! * ' ( ) ; : @ & = + $ , / ? % # [ ]`などの特殊文字が含まれている場合は、 [URIエンコーダ](https://www.urlencoder.org/)のように特殊文字をエスケープする必要があります。

## ダウンストリームデータベースユーザーに必要な権限 {#permissions-required-for-the-downstream-database-user}

TiDB またはその他の MySQL 互換データベースにデータを複製するには、ダウンストリーム データベース ユーザーに次の権限が必要です。

-   `Select`
-   `Index`
-   `Insert`
-   `Update`
-   `Delete`
-   `Create`
-   `Drop`
-   `Alter`
-   `Create View`

[`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md)ダウンストリーム TiDB に複製するには、ダウンストリーム データベース ユーザーに`Super`権限も必要です。

ダウンストリーム TiDB クラスターで[読み取り専用モード](/system-variables.md#tidb_restricted_read_only-new-in-v520)有効になっている場合、ダウンストリーム データベース ユーザーには`RESTRICTED_REPLICA_WRITER_ADMIN`権限も必要です。

## 災害シナリオにおける最終的に一貫性のあるレプリケーション {#eventually-consistent-replication-in-disaster-scenarios}

この機能はv6.1.1以降でGAとなります。v5.3.0以降、TiCDCは上流TiDBクラスターから下流クラスターのオブジェクトstorageまたはNFSへの増分データのバックアップをサポートします。上流クラスターが災害に見舞われて利用できなくなった場合でも、TiCDCは下流データを最新の結果整合性のある状態に復元できます。これは、TiCDCが提供する結果整合性のあるレプリケーション機能です。この機能により、アプリケーションを下流クラスターに迅速に切り替えることができ、長時間のダウンタイムを回避し、サービスの継続性を向上させることができます。

現在、TiCDCは、TiDBクラスタから別のTiDBクラスタ、またはMySQL互換データベースシステム（ Aurora、MySQL、MariaDBを含む）への増分データのレプリケーションが可能です。上流クラスタがクラッシュした場合、TiCDCがクラッシュ前に正常にデータをレプリケーションし、レプリケーション遅延が小さいという条件であれば、TiCDCは下流クラスタに5分以内にデータを復元できます。データ損失は最大10秒、つまりRTO &lt;= 5分、P95 RPO &lt;= 10秒を許容します。

次のシナリオでは、TiCDC レプリケーション ラグが増加します。

-   短時間でTPSが大幅に向上します。
-   アップストリームで大規模または長いトランザクションが発生します。
-   アップストリームの TiKV または TiCDC クラスターが再ロードまたはアップグレードされます。
-   `add index`などの時間のかかる DDL ステートメントは、アップストリームで実行されます。
-   PD は積極的なスケジュール戦略で構成されているため、リージョンリーダーの頻繁な転送、またはリージョンの頻繁なマージやリージョンの分割が発生します。

> **注記：**
>
> バージョン6.1.1以降、TiCDCの結果整合性レプリケーション機能はAmazon S3互換オブジェクトstorageをサポートします。バージョン6.1.4以降、この機能はGCSおよびAzure互換オブジェクトstorageをサポートします。

### 前提条件 {#prerequisites}

-   TiCDCのリアルタイム増分データバックアップファイルを格納するための高可用性オブジェクトstorageまたはNFSを用意してください。これらのファイルは、上流で災害が発生した場合でもアクセスできます。
-   災害シナリオにおいて最終的な一貫性を保つ必要がある変更フィードに対して、この機能を有効にします。この機能を有効にするには、変更フィード設定ファイルに以下の設定を追加します。

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

### 災害復旧 {#disaster-recovery}

プライマリクラスターで災害が発生した場合、 `cdc redo`コマンドを実行してセカンダリクラスターで手動で復旧する必要があります。復旧プロセスは以下のとおりです。

1.  すべてのTiCDCプロセスが終了していることを確認してください。これは、データ復旧中にプライマリクラスタがサービスを再開したり、TiCDCがデータ同期を再開したりするのを防ぐためです。
2.  データ復旧にはcdcバイナリを使用してください。以下のコマンドを実行してください。

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

このコマンドでは、

-   `tmp-dir` : TiCDC 増分データ バックアップ ファイルをダウンロードするための一時ディレクトリを指定します。
-   `storage` : TiCDC 増分データ バックアップ ファイルを保存するためのアドレス (オブジェクトstorageの URI または NFS ディレクトリ) を指定します。
-   `sink-uri` : データを復元するセカンダリクラスタアドレスを指定します。スキームは`mysql`のみに指定できます。
