---
title: Replicate Data to MySQL-compatible Databases
summary: TiCDC を使用してデータを TiDB または MySQL に複製する方法を学習します。
---

# MySQL互換データベースにデータを複製する {#replicate-data-to-mysql-compatible-databases}

このドキュメントでは、TiCDC を使用して、下流の TiDB データベースまたはその他の MySQL 互換データベースに増分データをレプリケートする方法について説明します。また、災害シナリオで最終的に一貫性のあるレプリケーション機能を使用する方法についても紹介します。

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
-   `--changefeed-id` : レプリケーション タスクの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。
-   `--sink-uri` : レプリケーションタスクのダウンストリームアドレス。詳細については、 [`mysql` / `tidb`でシンクURIを設定する](#configure-sink-uri-for-mysql-or-tidb)参照してください。
-   `--start-ts` : 変更フィードの開始 TSO を指定します。この TSO から、TiCDC クラスターはデータのプルを開始します。デフォルト値は現在の時刻です。
-   `--target-ts` : 変更フィード終了 TSO を指定します。この TSO まで、TiCDC クラスターはデータのプルを停止します。デフォルト値は空です。つまり、TiCDC はデータのプルを自動的に停止しません。
-   `--config` : changefeed設定ファイルを指定します。詳細については[TiCDC Changefeedコンフィグレーションパラメータ](/ticdc/ticdc-changefeed-config.md)参照してください。

> **注記：**
>
> -   TiCDC は増分データのみを複製します。完全なデータを初期化するには、 Dumpling/ TiDB LightningまたはBRを使用します。
> -   完全なデータが初期化された後、アップストリーム バックアップを実行するときに、TSO として`start-ts`指定する必要があります。たとえば、 Dumplingディレクトリの下のメタデータ ファイルの値`pos` 、またはBRがバックアップを完了した後のログ出力の値`backupTS`です。

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

以下は、MySQL または TiDB 用に構成できるシンク URI パラメータとパラメータ値の説明です。

| パラメータ/パラメータ値                | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root`                      | ダウンストリーム データベースのユーザー名。TiDB またはその他の MySQL 互換データベースにデータを複製するには、ダウンストリーム データベース ユーザーに[特定の権限](#permissions-required-for-the-downstream-database-user)あることを確認します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `123456`                    | ダウンストリーム データベースのパスワード (Base64 を使用してエンコードできます)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `127.0.0.1`                 | ダウンストリーム データベースの IP アドレス。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `3306`                      | ダウンストリーム データベースのポート。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `worker-count`              | ダウンストリームに対して同時に実行できる SQL ステートメントの数 (オプション、デフォルト値は`16` 、最大値は`1024` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `cache-prep-stmts`          | ダウンストリームで SQL を実行するときに準備済みステートメントを使用するかどうか、およびクライアント側でプリペアドステートメントキャッシュを有効にするかどうかを制御します (オプション、デフォルトは`true` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `max-txn-row`               | ダウンストリームに実行される SQL ステートメントのバッチ サイズ (オプション、デフォルト値は`256` 、最大値は`2048` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `max-multi-update-row`      | バッチ書き込み（ `batch-dml-enable` ）が有効な場合に下流に実行される`UPDATE ROWS` SQL文のバッチサイズ。常に`max-txn-row`未満です（オプション、デフォルト値は`40` 、最大値は`256` ）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `max-multi-update-row-size` | バッチ書き込み（ `batch-dml-enable` ）が有効な場合に下流に実行される`UPDATE ROWS` SQL文のサイズ制限。サイズがこの制限を超えると、各行は個別のSQL文として実行されます（オプション、デフォルト値は`1024` 、最大値は`8192` ）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `ssl-ca`                    | ダウンストリーム MySQL インスタンスに接続するために必要な CA 証明書ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ssl-cert`                  | ダウンストリーム MySQL インスタンスに接続するために必要な証明書ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `ssl-key`                   | ダウンストリーム MySQL インスタンスに接続するために必要な証明書キー ファイルのパス (オプション)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `time-zone`                 | ダウンストリーム MySQL インスタンスに接続するときに使用するタイムゾーン。v4.0.8 以降で有効です。これはオプションのパラメータです。このパラメータを指定しない場合は、TiCDC サービス プロセスのタイムゾーンが使用されます。このパラメータを空の値 ( `time-zone=""`など) に設定すると、TiCDC がダウンストリーム MySQL インスタンスに接続するときにタイムゾーンは指定されず、ダウンストリームのデフォルトのタイムゾーンが使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `transaction-atomicity`     | トランザクションのアトミック性レベル。これはオプションのパラメータで、デフォルト値は`none`です。値が`table`場合、TiCDC は単一テーブル トランザクションのアトミック性を保証します。値が`none`の場合、TiCDC は単一テーブル トランザクションを分割します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `batch-dml-enable`          | バッチ書き込み (batch-dml) 機能を有効にします (オプション、デフォルト値は`true` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `read-timeout`              | go-sql-driver パラメータ、 [I/O 読み取りタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-readtimeout) (オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `write-timeout`             | go-sql-driver パラメータ、 [I/O書き込みタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-writetimeout) (オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `timeout`                   | go-sql-driver パラメータ[接続を確立するためのタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-timeout)はダイヤル タイムアウトとも呼ばれます (オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `tidb-txn-mode`             | [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)環境変数を指定します (オプション、デフォルト値は`optimistic` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `safe-mode`                 | ダウンストリームにデータをレプリケートするときに、 TiCDC が`INSERT`および`UPDATE`ステートメントを処理する方法を指定します。 `true`の場合、 TiCDC はアップストリームの`INSERT`ステートメントをすべて`REPLACE INTO`ステートメントに変換し、 `UPDATE`ステートメントをすべて`DELETE` + `REPLACE INTO`ステートメントに変換します。 v6.1.3 より前では、このパラメーターのデフォルト値は`true`です。 v6.1.3 以降では、デフォルト値は`false`に変更されています。 TiCDC が起動すると、現在のタイムスタンプ`ThresholdTs`を取得します。 `CommitTs`が`ThresholdTs`より小さい`INSERT`および`UPDATE`ステートメントの場合、 TiCDC はそれらをそれぞれ`REPLACE INTO`ステートメントと`DELETE` + `REPLACE INTO`ステートメントに変換します。 `CommitTs`が`ThresholdTs`以上である`INSERT`および`UPDATE`ステートメントの場合、 `INSERT`ステートメントはダウンストリームに直接レプリケートされますが、 `UPDATE`ステートメントの動作は[UPDATE イベントを分割する際の TiCDC の動作](/ticdc/ticdc-split-update-behavior.md)に従います。 |

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
> シンク URI に`! * ' ( ) ; : @ & = + $ , / ? % # [ ]`などの特殊文字が含まれている場合は、 [URI エンコーダ](https://www.urlencoder.org/)のように特殊文字をエスケープする必要があります。

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

[`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md)ダウンストリーム TiDB に複製するには、ダウンストリーム データベース ユーザーにも`Super`権限が必要です。

ダウンストリーム TiDB クラスターで[読み取り専用モード](/system-variables.md#tidb_restricted_read_only-new-in-v520)有効になっている場合、ダウンストリーム データベース ユーザーには`RESTRICTED_REPLICA_WRITER_ADMIN`権限も必要です。

## 災害シナリオにおける最終的に一貫性のあるレプリケーション {#eventually-consistent-replication-in-disaster-scenarios}

この機能は v6.1.1 から GA になります。v5.3.0 以降、TiCDC はアップストリーム TiDB クラスターからダウンストリーム クラスターのオブジェクトstorageまたは NFS への増分データのバックアップをサポートします。アップストリーム クラスターが災害に遭遇して使用できなくなった場合、TiCDC はダウンストリーム データを最新の最終的に一貫性のある状態に復元できます。これが TiCDC が提供する最終的に一貫性のあるレプリケーション機能です。この機能を使用すると、アプリケーションをダウンストリーム クラスターにすばやく切り替えることができ、長時間のダウンタイムを回避してサービスの継続性を向上させることができます。

現在、TiCDC は、TiDB クラスターから別の TiDB クラスターまたは MySQL 互換データベース システム ( Aurora、MySQL、MariaDB を含む) に増分データを複製できます。上流クラスターがクラッシュした場合、TiCDC がクラッシュ前にデータを正常に複製し、レプリケーション ラグが小さいという条件であれば、TiCDC は 5 分以内に下流クラスターにデータを復元できます。最大 10 秒のデータ損失が許容されます。つまり、RTO &lt;= 5 分、P95 RPO &lt;= 10 秒です。

次のシナリオでは、TiCDC レプリケーション ラグが増加します。

-   短時間でTPSが大幅に向上します。
-   アップストリームで大規模または長時間のトランザクションが発生します。
-   アップストリームの TiKV または TiCDC クラスターが再ロードまたはアップグレードされます。
-   `add index`などの時間のかかる DDL ステートメントは、アップストリームで実行されます。
-   PD は積極的なスケジュール戦略で構成されているため、リージョンリーダーの頻繁な転送、またはリージョンの頻繁なマージやリージョンの分割が発生します。

> **注記：**
>
> v6.1.1 以降、TiCDC の最終的に整合性のあるレプリケーション機能は、Amazon S3 互換のオブジェクトstorageをサポートします。v6.1.4 以降、この機能は GCS および Azure 互換のオブジェクトstorageをサポートします。

### 前提条件 {#prerequisites}

-   TiCDC のリアルタイム増分データ バックアップ ファイルを保存するための高可用性オブジェクトstorageまたは NFS を準備します。アップストリームで災害が発生した場合、これらのファイルにアクセスできます。
-   災害シナリオで最終的な一貫性を保つ必要がある変更フィードに対してこの機能を有効にします。これを有効にするには、変更フィード構成ファイルに次の構成を追加します。

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

プライマリ クラスターで災害が発生した場合は、 `cdc redo`コマンドを実行してセカンダリ クラスターで手動で復旧する必要があります。復旧プロセスは次のとおりです。

1.  すべての TiCDC プロセスが終了していることを確認します。これは、データ復旧中にプライマリ クラスターがサービスを再開したり、TiCDC がデータ同期を再開したりするのを防ぐためです。
2.  データの回復には cdc バイナリを使用します。次のコマンドを実行します。

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

このコマンドでは、

-   `tmp-dir` : TiCDC 増分データ バックアップ ファイルをダウンロードするための一時ディレクトリを指定します。
-   `storage` : TiCDC 増分データ バックアップ ファイルを保存するアドレス (オブジェクトstorageの URI または NFS ディレクトリ) を指定します。
-   `sink-uri` : データを復元するセカンダリ クラスター アドレスを指定します。スキームは`mysql`のみにすることができます。
