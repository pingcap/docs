---
title: Replicate Data to MySQL-compatible Databases
summary: TiCDCを使用して、データをTiDBまたはMySQLに複製する方法を学びましょう。
---

# データをMySQL互換データベースに複製する {#replicate-data-to-mysql-compatible-databases}

このドキュメントでは、TiCDCを使用して増分データを下流のTiDBデータベースまたはその他のMySQL互換データベースにレプリケートする方法について説明します。また、災害発生時のシナリオで結果整合性レプリケーション機能を使用する方法についても紹介します。

## レプリケーションタスクを作成する {#create-a-replication-task}

次のコマンドを実行して、レプリケーションタスクを作成します。

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

-   `--server` : TiCDCクラスタ内の任意のTiCDCサーバーのアドレス。
-   `--changefeed-id` : レプリケーションタスクのID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現に一致する必要があります。このIDが指定されていない場合、TiCDCは自動的にUUID（バージョン4形式）をIDとして生成します。
-   `--sink-uri` : レプリケーション タスクのダウンストリーム アドレス。詳細については、[シンクURIを`mysql` / `tidb`で設定します](#configure-sink-uri-for-mysql-or-tidb)を参照してください。
-   `--start-ts` : 変更フィードの開始TSOを指定します。TiCDCクラスタはこのTSOからデータの取得を開始します。デフォルト値は現在時刻です。
-   `--target-ts` : 変更フィードの終了TSOを指定します。このTSOに達すると、TiCDCクラスタはデータのプルを停止します。デフォルト値は空で、これはTiCDCが自動的にデータのプルを停止しないことを意味します。
-   `--config` : チェンジフィード構成ファイルを指定します。詳細については、 [TiCDC Changefeedコンフィグレーションパラメータ](/ticdc/ticdc-changefeed-config.md)を参照してください。

> **Note:**
>
> -   TiCDCは増分データのみを複製します。完全なデータを初期化するには、 Dumpling/ TiDB LightningまたはBRを使用してください。
> -   完全なデータ初期化が完了したら、アップストリームバックアップを実行する際に`start-ts`をTSOとして指定する必要があります。例えば、 Dumplingディレクトリ内のメタデータファイルにある`pos`の値、またはBRがバックアップを完了した後のログ出力にある`backupTS`の値などです。

## MySQLまたはTiDBのシンクURIを設定します {#configure-sink-uri-for-mysql-or-tidb}

シンクURIは、TiCDCターゲットシステムの接続情報を指定するために使用されます。フォーマットは以下のとおりです。

    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]

> **Note:**
>
> `/path`は MySQL シンクには使用されません。

MySQLの設定例：

```shell
--sink-uri="mysql://root:12345678@127.0.0.1:3306"
```

以下は、MySQLまたはTiDB用に構成可能なシンクURIパラメータとパラメータ値の説明です。

| パラメータ/パラメータ値                | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| :-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root`                      | ダウンストリーム データベースのユーザー名。データを TiDB または他の MySQL 互換データベースにレプリケートするには、ダウンストリーム データベース ユーザーが[特定の権限](#permissions-required-for-the-downstream-database-user)持っていることを確認してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `12345678`                  | 下流データベースのパスワード（Base64でエンコード可能）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `127.0.0.1`                 | 下流データベースのIPアドレス。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `3306`                      | 下流データベースへのポート番号。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `worker-count`              | ダウンストリームで同時に実行できる SQL ステートメントの数 (オプション、デフォルト値は`16` 、最大値は`1024`です)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `cache-prep-stmts`          | ダウンストリームで SQL を実行する際にプリペアド ステートメントを使用するかどうか、およびクライアント側でプリペアドステートメントキャッシュを有効にするかどうかを制御します (オプション、デフォルトは`true` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `multi-stmt-enable`         | 下流で実行される SQL ステートメントが、セミコロンで区切られた複数の SQL ステートメントをサポートするかどうかを制御します (オプション、デフォルト値は`true`です)。 `false`に設定されている場合、各 SQL ステートメントは個別のトランザクションとして実行されます。 `true`に設定されている場合、 `cache-prep-stmts`有効になりません。                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `max-txn-row`               | ダウンストリームに実行される SQL ステートメントのバッチ サイズ (オプション、デフォルト値は`256` 、最大値は`2048`です)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `max-multi-update-row`      | バッチ書き込み ( `UPDATE ROWS` ) が有効になっている場合にダウンストリームで実行される`batch-dml-enable` SQL ステートメントのバッチサイズは、常に`max-txn-row`より小さくなります (オプション、デフォルト値は`40`で、最大値は`256`です)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `max-multi-update-row-size` | バッチ書き込み ( `batch-dml-enable` ) が有効になっている場合、このパラメーターは、下流で実行される`UPDATE ROWS` SQL ステートメントのバッチ処理サイズ (バイト単位) を制御します。単一行の平均サイズがこのしきい値を超えると、各行は独立した SQL ステートメントとして実行されます (オプション、デフォルト値は`1024` 、最大値は`8192`です)。                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `ssl-ca`                    | 下流のMySQLインスタンスに接続するために必要なCA証明書ファイルのパス（オプション）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `ssl-cert`                  | 下流のMySQLインスタンスに接続するために必要な証明書ファイルのパス（オプション）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ssl-key`                   | 下流のMySQLインスタンスに接続するために必要な証明書キーファイルのパス（オプション）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `time-zone`                 | ダウンストリームの MySQL および TiDB インスタンスに接続する際に使用されるタイムゾーン名 (つまり、ダウンストリーム接続セッションの`time_zone` 。v4.0.8 以降で有効です。これはオプションのパラメータです。このパラメータが指定されていない場合、TiCDC サービス プロセスのタイムゾーンが使用されます。このパラメータが`time-zone=""`などの空の値に設定されている場合、TiCDC が接続する際にセッション タイムゾーンが指定されておらず、ダウンストリームのデフォルトのタイムゾーンが使用されることを意味します。                                                                                                                                                                                                                                                                                                                                                                  |
| `transaction-atomicity`     | トランザクションのアトミック性レベル。これはオプションのパラメータで、デフォルト値は`none`です。値が`table`の場合、TiCDC は単一テーブル トランザクションのアトミック性を保証します。値が`none`の場合、TiCDC は単一テーブル トランザクションを分割します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `batch-dml-enable`          | バッチ書き込み（バッチ dml）機能を有効にします（オプション、デフォルト値は`true`です）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `read-timeout`              | go-sql-driver パラメーター、 [入出力読み取りタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-readtimeout)(オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `write-timeout`             | go-sql-driver パラメーター、 [I/O書き込みタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-writetimeout)(オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `timeout`                   | go-sql-driver パラメータの[接続確立のタイムアウト](https://pkg.go.dev/github.com/go-sql-driver/mysql#readme-timeout)。ダイヤル タイムアウトとも呼ばれます (オプション、デフォルト値は`2m` )。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `tidb-txn-mode`             | [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)環境変数を指定します (オプション、デフォルト値は`optimistic`です)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `safe-mode`                 | TiCDC がデータを下流に複製する際に`INSERT`および`UPDATE`ステートメントをどのように処理するかを指定します。 `true`の場合、TiCDC は上流のすべての`INSERT`ステートメントを`REPLACE INTO`ステートメントに変換し、すべての`UPDATE`ステートメントを`DELETE` + `REPLACE INTO`ステートメントに変換します。v6.1.3 より前は、このパラメーターのデフォルト値は`true`です。バージョン 6.1.3 以降、デフォルト値は`false`に変更されます。TiCDC が起動すると、現在のタイムスタンプ`ThresholdTs`を取得します。 `INSERT`と`UPDATE`ステートメントで`CommitTs`が`ThresholdTs`より小さい場合、TiCDC はそれぞれ`REPLACE INTO`ステートメントと`DELETE` + `REPLACE INTO`ステートメントに変換します。 `INSERT`が`UPDATE`以上である`CommitTs`および`ThresholdTs`ステートメントの場合、 `INSERT`ステートメントはダウンストリームに直接レプリケートされますが、 `UPDATE`ステートメントの動作は[TiCDCにおけるUPDATEイベント分割時の動作](/ticdc/ticdc-split-update-behavior.md)に従います。 |

> **Note:**
>
> -   `time-zone`は`mysql`および`tidb`シンクでのみ有効です。TiCDC がダウンストリームとの接続を確立した後、セッションの`time_zone`を設定します。この`time_zone`は、ダウンストリームが DDL および DML ステートメントを実行する際に、 `TIMESTAMP`などのタイムゾーンの影響を受ける時間値を解析するために使用されます。 `DATETIME` 、 `DATE` 、および`TIME`データ型は、タイムゾーン設定の影響を受けません。
> -   タイムゾーン設定の不一致によって発生するデータの不整合を回避するために、 `time-zone`明示的に設定し、その値が TiCDC サーバーの`--tz`パラメータおよび下流データベースのタイムゾーンと一致していることを確認することをお勧めします。

シンクURI内のデータベースパスワードをBase64でエンコードするには、次のコマンドを使用します。

```shell
echo -n '12345678' | base64   # '12345678' is the password to be encoded.
```

エンコードされたパスワードは以下のとおりです。

```shell
MTIzNDU2Nzg=
```

> **Note:**
>
> シンク URI パラメータに`! * ' ( ) ; : @ & = + $ , / ? % # [ ]`などの特殊文字が含まれている場合は、 [URIエンコーダー](https://www.urlencoder.org/)のように特殊文字をエスケープする必要があります。
>
> 例えば、ダウンストリームデータベースへの接続に使用するユーザー名が`R&D (2)`で、証明書ファイルのパスが`/data1/R&D (2).pem`の場合、これらのパラメータを次のようにエスケープする必要があります。
>
> ```shell
> --sink-uri="mysql://R%26D%20%282%29:MTIzNDU2Nzg%3D@127.0.0.1:3306/?ssl-cert=/data1/R%26D%20%282%29.pem"
> #                    ^~~ ^~~^~~ ^~~            ^~~                                  ^~~ ^~~^~~ ^~~
> ```

## 下流データベースユーザーに必要な権限 {#permissions-required-for-the-downstream-database-user}

TiDBまたはその他のMySQL互換データベースにデータを複製するには、下流のデータベースユーザーに以下の権限が必要です。

-   `Select`
-   `Index`
-   `Insert`
-   `Update`
-   `Delete`
-   `Create`
-   `References`
-   `Drop`
-   `Alter`
-   `Create View`

[`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md)下流の TiDB に複製するには、下流のデータベース ユーザーは`Super`権限も必要とします。

ダウンストリーム TiDB クラスターで[読み取り専用モード](/system-variables.md#tidb_restricted_read_only-new-in-v520)が有効になっている場合、ダウンストリーム データベース ユーザーには`RESTRICTED_REPLICA_WRITER_ADMIN`権限も必要です。

## 災害シナリオにおける結果整合性レプリケーション {#eventually-consistent-replication-in-disaster-scenarios}

TiCDC の最終整合性レプリケーション機能は、リドゥログを使用して、アップストリームで障害が発生した場合でもデータの一貫性を確保します。この機能は、バージョン 6.1.1 から一般提供 (GA) となります。バージョン 5.3.0 から、TiCDC は、アップストリーム TiDB クラスタからダウンストリーム クラスタのオブジェクトストレージまたは NFS への増分データのバックアップをサポートします。アップストリーム クラスタで障害が発生して利用できなくなった場合、TiCDC はダウンストリーム データを最新の最終整合性状態に復元できます。この機能により、アプリケーションをダウンストリーム クラスタに迅速に切り替えることができ、長時間のダウンタイムを回避し、サービスの継続性を向上させることができます。

現在、TiCDCは、TiDBクラスタから別のTiDBクラスタまたはMySQL互換データベースシステム（ Aurora、MySQL、MariaDBを含む）へ増分データを複製できます。上流クラスタがクラッシュした場合、TiCDCがクラッシュ前に正常にデータを複製し、複製遅延が小さいという条件を満たせば、TiCDCは下流クラスタで5分以内にデータを復元できます。データ損失は最大10秒まで許容され、RTOは5分以下、P95 RPOは10秒以下となります。

TiCDCのレプリケーション遅延は、以下のシナリオで増加します。

-   TPSは短時間で大幅に増加する。
-   上流工程では、大規模または長時間のトランザクションが発生する。
-   アップストリームのTiKVまたはTiCDCクラスタが再ロードまたはアップグレードされます。
-   `add index`のような時間のかかる DDL ステートメントは、上流で実行されます。
-   PDは積極的なスケジューリング戦略で構成されており、その結果、リージョンリーダーの頻繁な異動、あるいはリージョンの統合や分割が頻繁に発生します。

> **Note:**
>
> バージョン6.1.1以降、TiCDCの最終整合性レプリケーション機能はAmazon S3互換のオブジェクトストレージをサポートしています。バージョン6.1.4以降、この機能はGCSおよびAzure互換のオブジェクトストレージもサポートしています。

### 前提条件 {#prerequisites}

-   TiCDCのリアルタイム増分データバックアップファイルを保存するために、高可用性のオブジェクトストレージまたはNFSを準備してください。これらのファイルは、上流側で災害が発生した場合にアクセスできます。
-   災害発生時に最終的な整合性が必要な変更フィードに対して、この機能を有効にしてください。有効にするには、変更フィードの設定ファイルに以下の設定を追加します。

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

### 災害リカバリ {#disaster-recovery}

プライマリクラスタで障害が発生した場合は、 `cdc redo`コマンドを実行してセカンダリクラスタで手動で復旧する必要があります。リカバリ手順は以下のとおりです。

1.  TiCDCのすべてのプロセスが終了していることを確認してください。これは、データリカバリ中にプライマリクラスタがサービスを再開したり、TiCDCがデータ同期を再開したりするのを防ぐためです。
2.  データリカバリにはcdcバイナリを使用してください。以下のコマンドを実行してください。

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

このコマンドでは：

-   `tmp-dir` : TiCDC増分データバックアップファイルをダウンロードするための一時ディレクトリを指定します。
-   `storage` : TiCDC増分データバックアップファイルを保存するアドレスを指定します。オブジェクトストレージのURIまたはNFSディレクトリのいずれかを指定します。
-   `sink-uri` : データを復元するセカンダリクラスタアドレスを指定します。スキームは`mysql`のみ可能です。
