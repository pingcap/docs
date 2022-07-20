---
title: TiDB Binlog Configuration File
summary: Learn the configuration items of TiDB Binlog.
---

# BinlogConfiguration / コンフィグレーションファイル {#tidb-binlog-configuration-file}

このドキュメントでは、 Binlogの構成項目を紹介します。

## Pump {#pump}

このセクションでは、 Pumpの構成項目を紹介します。完全なPump構成ファイルの例については、 [PumpConfiguration / コンフィグレーション](https://github.com/pingcap/tidb-binlog/blob/master/cmd/pump/pump.toml)を参照してください。

### addr {#addr}

-   HTTPAPIのリスニングアドレスを`host:port`の形式で指定します。
-   デフォルト値： `127.0.0.1:8250`

### advertise-addr {#advertise-addr}

-   外部からアクセス可能なHTTPAPIアドレスを指定します。このアドレスは、 `host:port`の形式でPDに登録されます。
-   デフォルト値： `127.0.0.1:8250`

### ソケット {#socket}

-   HTTPAPIがリッスンするUnixソケットアドレス。
-   デフォルト値： &quot;&quot;

### pd-urls {#pd-urls}

-   PDURLのコンマ区切りリストを指定します。複数のアドレスが指定されている場合、PDクライアントが1つのアドレスへの接続に失敗すると、PDクライアントは自動的に別のアドレスへの接続を試みます。
-   デフォルト値： `http://127.0.0.1:2379`

### data-dir {#data-dir}

-   binlogとそのインデックスがローカルに保存されるディレクトリを指定します。
-   デフォルト値： `data.pump`

### ハートビート間隔 {#heartbeat-interval}

-   最新のステータスがPDに報告されるハートビート間隔（秒単位）を指定します。
-   デフォルト値： `2`

### gen-binlog-interval {#gen-binlog-interval}

-   データが偽のbinlogに書き込まれる間隔（秒単位）を指定します。
-   デフォルト値： `3`

### gc {#gc}

-   binlogをローカルに保存できる日数（整数）を指定します。指定した日数より長く保存されたビンログは自動的に削除されます。
-   デフォルト値： `7`

### ログファイル {#log-file}

-   ログファイルが保存されるパスを指定します。パラメータが空の値に設定されている場合、ログファイルは保存されません。
-   デフォルト値： &quot;&quot;

### ログレベル {#log-level}

-   ログレベルを指定します。
-   デフォルト値： `info`

### node-id {#node-id}

-   PumpノードIDを指定します。このIDを使用すると、このPumpプロセスをクラスタで識別できます。
-   デフォルト値： `hostname:port number` 。たとえば、 `node-1:8250` 。

### 安全 {#security}

このセクションでは、セキュリティに関連する構成項目を紹介します。

#### ssl-ca {#ssl-ca}

-   トラステッドSSL証明書リストまたはCAリストのファイルパスを指定します。たとえば、 `/path/to/ca.pem` 。
-   デフォルト値： &quot;&quot;

#### ssl-cert {#ssl-cert}

-   プライバシー強化メール（PEM）形式でエンコードされたX509証明書ファイルのパスを指定します。たとえば、 `/path/to/pump.pem` 。
-   デフォルト値： &quot;&quot;

#### ssl-key {#ssl-key}

-   PEM形式でエンコードされたX509キーファイルのパスを指定します。たとえば、 `/path/to/pump-key.pem` 。
-   デフォルト値： &quot;&quot;

### 保管所 {#storage}

このセクションでは、ストレージに関連する構成項目を紹介します。

#### 同期ログ {#sync-log}

-   データの安全性を確保するために、binlogへの各**バッチ**書き込みの後に`fsync`を使用するかどうかを指定します。
-   デフォルト値： `true`

#### kv_chan_cap {#kv-chan-cap}

-   Pumpがこれらの要求を受信する前に、バッファーが保管できる書き込み要求の数を指定します。
-   デフォルト値： `1048576` （つまり、2の20乗）

#### slow_write_threshold {#slow-write-threshold}

-   しきい値（秒単位）。この指定されたしきい値よりも単一のbinlogファイルの書き込みに時間がかかる場合、書き込みは低速書き込みと見なされ、 `"take a long time to write binlog"`がログに出力されます。
-   デフォルト値： `1`

#### stop-write-at-available-space {#stop-write-at-available-space}

-   使用可能なストレージ容量がこの指定された値を下回ると、 Binlog書き込み要求は受け入れられなくなります。 `900 MB`などの形式を使用して、 `12 GiB`スペースを指定でき`5 GB` 。クラスタに複数のPumpノードがある場合、スペースが不足しているためにPumpノードが書き込み要求を拒否すると、TiDBは自動的に他のPumpノードにbinlogを書き込みます。
-   デフォルト値： `10 GiB`

#### kv {#kv}

現在、 Pumpのストレージは[GoLevelDB](https://github.com/syndtr/goleveldb)に基づいて実装されています。 `storage`の下には、GoLevel構成を調整するために使用される`kv`のサブグループもあります。サポートされている構成項目は次のとおりです。

-   ブロックキャッシュ容量
-   block-restart-interval
-   ブロックサイズ
-   圧縮-L0トリガー
-   圧縮テーブルサイズ
-   圧縮-合計サイズ
-   圧縮-合計サイズ-乗数
-   書き込みバッファ
-   書き込み-L0-一時停止-トリガー
-   書き込み-L0-スローダウン-トリガー

上記の項目の詳細については、 [GoLevelDBドキュメント](https://godoc.org/github.com/syndtr/goleveldb/leveldb/opt#Options)を参照してください。

## Drainer {#drainer}

このセクションでは、 Drainerの構成項目を紹介します。完全なDrainer構成ファイルの例については、 [DrainerConfiguration / コンフィグレーション](https://github.com/pingcap/tidb-binlog/blob/master/cmd/drainer/drainer.toml)を参照してください。

### addr {#addr}

-   HTTPAPIのリスニングアドレスを`host:port`の形式で指定します。
-   デフォルト値： `127.0.0.1:8249`

### advertise-addr {#advertise-addr}

-   外部からアクセス可能なHTTPAPIアドレスを指定します。このアドレスは、 `host:port`の形式でPDに登録されます。
-   デフォルト値： `127.0.0.1:8249`

### ログファイル {#log-file}

-   ログファイルが保存されるパスを指定します。パラメータが空の値に設定されている場合、ログファイルは保存されません。
-   デフォルト値： &quot;&quot;

### ログレベル {#log-level}

-   ログレベルを指定します。
-   デフォルト値： `info`

### node-id {#node-id}

-   DrainerノードIDを指定します。このIDを使用すると、このDrainerプロセスをクラスタで識別できます。
-   デフォルト値： `hostname:port number` 。たとえば、 `node-1:8249` 。

### data-dir {#data-dir}

-   Drainerの操作中に保存する必要のあるファイルを保存するために使用するディレクトリを指定します。
-   デフォルト値： `data.drainer`

### 検出間隔 {#detect-interval}

-   PDがPump情報を更新する間隔（秒単位）を指定します。
-   デフォルト値： `5`

### pd-urls {#pd-urls}

-   PDURLのコンマ区切りのリスト。複数のアドレスが指定されている場合、1つのアドレスへの接続中にエラーが発生すると、PDクライアントは自動的に別のアドレスへの接続を試みます。
-   デフォルト値： `http://127.0.0.1:2379`

### initial-commit-ts {#initial-commit-ts}

-   トランザクションのどのコミットタイムスタンプからレプリケーションプロセスを開始するかを指定します。この構成は、初めてレプリケーションプロセスにあるDrainerノードにのみ適用できます。チェックポイントがダウンストリームにすでに存在する場合、レプリケーションはチェックポイントに記録された時間に従って実行されます。
-   commit ts（コミットタイムスタンプ）は、TiDBでの[取引](/transaction-overview.md#transactions)のコミットの特定の時点です。これは、現在のトランザクションの一意のIDとして、グローバルに一意であり、PDから増加するタイムスタンプです。次の一般的な方法で`initial-commit-ts`の構成を取得できます。
    -   BRを使用する場合、BR（backupmeta）によってバックアップされたメタデータに記録されたバックアップTSから`initial-commit-ts`を取得できます。
    -   Dumplingを使用する場合、Dumpling（メタデータ）によってバックアップされたメタデータに記録されたPosから`initial-commit-ts`を取得できます。
    -   PD Controlを使用する場合、 `tso`コマンドの出力に`initial-commit-ts`が含まれます。
-   デフォルト値： `-1` 。 Drainerは、開始時刻としてPDから新しいタイムスタンプを取得します。これは、レプリケーションプロセスが現在の時刻から開始されることを意味します。

### 同期チェック時間 {#synced-check-time}

-   HTTP APIを介して`/status`のパスにアクセスし、 Drainerレプリケーションのステータスを照会できます。 `synced-check-time`は、最後に成功したレプリケーションから`synced`分、つまりレプリケーションが完了したと見なされる分数を指定します。
-   デフォルト値： `5`

### コンプレッサー {#compressor}

-   PumpとDrainer間のデータ転送に使用される圧縮アルゴリズムを指定します。現在、 `gzip`のアルゴリズムのみがサポートされています。
-   デフォルト値： &quot;&quot;、これは圧縮なしを意味します。

### 安全 {#security}

このセクションでは、セキュリティに関連する構成項目を紹介します。

#### ssl-ca {#ssl-ca}

-   トラステッドSSL証明書リストまたはCAリストのファイルパスを指定します。たとえば、 `/path/to/ca.pem` 。
-   デフォルト値： &quot;&quot;

#### ssl-cert {#ssl-cert}

-   PEM形式でエンコードされたX509証明書ファイルのパスを指定します。たとえば、 `/path/to/drainer.pem` 。
-   デフォルト値： &quot;&quot;

#### ssl-key {#ssl-key}

-   PEM形式でエンコードされたX509キーファイルのパスを指定します。たとえば、 `/path/to/pump-key.pem` 。
-   デフォルト値： &quot;&quot;

### シンカー {#syncer}

`syncer`セクションには、ダウンストリームに関連する構成アイテムが含まれています。

#### db-type {#db-type}

現在、次のダウンストリームタイプがサポートされています。

-   `mysql`
-   `tidb`
-   `kafka`
-   `file`

デフォルト値： `mysql`

#### sql-mode {#sql-mode}

-   ダウンストリームが`mysql`または`tidb`タイプの場合のSQLモードを指定します。複数のモードがある場合は、コンマを使用してそれらを区切ります。
-   デフォルト値： &quot;&quot;

#### 無視-txn-commit-ts {#ignore-txn-commit-ts}

-   binlogが無視されるコミットタイムスタンプを`[416815754209656834, 421349811963822081]`などで指定します。
-   デフォルト値： `[]`

#### 無視-スキーマ {#ignore-schemas}

-   レプリケーション中に無視されるデータベースを指定します。無視するデータベースが複数ある場合は、コンマを使用してそれらを区切ります。 binlogファイル内のすべての変更がフィルタリングされると、binlogファイル全体が無視されます。
-   デフォルト値： `INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql`

#### 無視テーブル {#ignore-table}

レプリケーション中に指定されたテーブルの変更を無視します。 `toml`のファイルで無視する複数のテーブルを指定できます。例えば：

{{< copyable "" >}}

```toml
[[syncer.ignore-table]]
db-name = "test"
tbl-name = "log"

[[syncer.ignore-table]]
db-name = "test"
tbl-name = "audit"
```

binlogファイル内のすべての変更がフィルタリングされると、binlogファイル全体が無視されます。

デフォルト値： `[]`

#### レプリケート-do-db {#replicate-do-db}

-   複製するデータベースを指定します。たとえば、 `[db1, db2]` 。
-   デフォルト値： `[]`

#### 複製-実行-テーブル {#replicate-do-table}

複製するテーブルを指定します。例えば：

{{< copyable "" >}}

```toml
[[syncer.replicate-do-table]]
db-name ="test"
tbl-name = "log"

[[syncer.replicate-do-table]]
db-name ="test"
tbl-name = "~^a.*"
```

デフォルト値： `[]`

#### txn-バッチ {#txn-batch}

-   ダウンストリームが`mysql`または`tidb`タイプの場合、DML操作は異なるバッチで実行されます。このパラメーターは、各トランザクションに含めることができるDML操作の数を指定します。
-   デフォルト値： `20`

#### 労働者数 {#worker-count}

-   ダウンストリームが`mysql`または`tidb`タイプの場合、DML操作は同時に実行されます。このパラメーターは、DML操作の同時実行数を指定します。
-   デフォルト値： `16`

#### disable-dispatch {#disable-dispatch}

-   同時実行を無効にし、 `worker-count`から`1`に強制的に設定します。
-   デフォルト値： `false`

#### セーフモード {#safe-mode}

セーフモードが有効になっている場合、 Drainerはレプリケーションの更新を次のように変更します。

-   `Insert`は`Replace Into`に変更されます
-   `Update`は`Delete`プラス`Replace Into`に変更されます

デフォルト値： `false`

### syncer.to {#syncer-to}

`syncer.to`のセクションでは、構成タイプに応じて、さまざまなタイプのダウンストリーム構成アイテムを紹介します。

#### mysql / tidb {#mysql-tidb}

次の構成項目は、ダウンストリームデータベースへの接続に関連しています。

-   `host` ：この項目が設定されていない場合、 Binlogはデフォルトで`localhost`である`MYSQL_HOST`環境変数をチェックしようとします。
-   `port` ：この項目が設定されていない場合、 Binlogはデフォルトで`3306`である`MYSQL_PORT`環境変数をチェックしようとします。
-   `user` ：この項目が設定されていない場合、 Binlogはデフォルトで`root`である`MYSQL_USER`環境変数をチェックしようとします。
-   `password` ：この項目が設定されていない場合、 Binlogはデフォルトで`""`である`MYSQL_PSWD`環境変数をチェックしようとします。

#### ファイル {#file}

-   `dir` ：binlogファイルが保存されるディレクトリを指定します。この項目が設定されていない場合、 `data-dir`が使用されます。

#### カフカ {#kafka}

ダウンストリームがKafkaの場合、有効な構成項目は次のとおりです。

-   `zookeeper-addrs`
-   `kafka-addrs`
-   `kafka-version`
-   `kafka-max-messages`
-   `kafka-max-message-size`
-   `topic-name`

### syncer.to.checkpoint {#syncer-to-checkpoint}

-   `type` ：レプリケーションの進行状況を保存する方法を指定します。現在、使用可能なオプションは`mysql` 、および`tidb` `file` 。

    この構成項目は、デフォルトでダウンストリームタイプと同じです。たとえば、ダウンストリームが`file`の場合、チェックポイントの進行状況はローカルファイル`<data-dir>/savepoint`に保存されます。ダウンストリームが`mysql`の場合、進行状況はダウンストリームデータベースに保存されます。進行状況を保存するために`mysql`または`tidb`を使用して明示的に指定する必要がある場合は、次の構成を行います。

-   デフォルトでは`schema` ： `"tidb_binlog"` 。

    > **ノート：**
    >
    > 同じTiDBクラスタに複数のDrainerノードをデプロイする場合は、ノードごとに異なるチェックポイントスキーマを指定する必要があります。そうしないと、2つのインスタンスのレプリケーションの進行状況が相互に上書きされます。

-   `host`

-   `user`

-   `password`

-   `port`
