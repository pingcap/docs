---
title: TiDB Binlog Configuration File
summary: Learn the configuration items of TiDB Binlog.
---

# TiDB Binlogコンフィグレーションファイル {#tidb-binlog-configuration-file}

このドキュメントでは、TiDB Binlogの構成項目を紹介します。

## Pump {#pump}

このセクションでは、 Pumpの設定項目を紹介します。完全なPump構成ファイルの例については、 [Pumpコンフィグレーション](https://github.com/pingcap/tidb-binlog/blob/master/cmd/pump/pump.toml)を参照してください。

### アドレス {#addr}

-   HTTP API のリッスン アドレスを`host:port`の形式で指定します。
-   デフォルト値: `127.0.0.1:8250`

### 広告アドレス {#advertise-addr}

-   外部からアクセス可能な HTTP API アドレスを指定します。このアドレスは`host:port`の形式で PD に登録されます。
-   デフォルト値: `127.0.0.1:8250`

### ソケット {#socket}

-   HTTP API がリッスンする Unix ソケット アドレス。
-   デフォルト値: &quot;&quot;

### pd-url {#pd-urls}

-   PD URL のコンマ区切りリストを指定します。複数のアドレスが指定されている場合、PD クライアントが 1 つのアドレスへの接続に失敗すると、自動的に別のアドレスへの接続を試みます。
-   デフォルト値: `http://127.0.0.1:2379`

### データディレクトリ {#data-dir}

-   binlog とそのインデックスがローカルに保存されるディレクトリを指定します。
-   デフォルト値: `data.pump`

### ハートビート間隔 {#heartbeat-interval}

-   最新のステータスが PD に報告されるハートビート間隔 (秒単位) を指定します。
-   デフォルト値: `2`

### gen-binlog-interval {#gen-binlog-interval}

-   データが fake binlogに書き込まれる間隔 (秒単位) を指定します。
-   デフォルト値: `3`

### GC {#gc}

-   binlog をローカルに保存できる日数 (整数) を指定します。指定した日数を超えて保存されたバイナリログは自動的に削除されます。
-   デフォルト値: `7`

### ログファイル {#log-file}

-   ログ ファイルが保存されるパスを指定します。パラメータが空の値に設定されている場合、ログ ファイルは保存されません。
-   デフォルト値: &quot;&quot;

### ログレベル {#log-level}

-   ログ レベルを指定します。
-   デフォルト値: `info`

### ノード ID {#node-id}

-   Pumpノード ID を指定します。この ID を使用して、このPumpプロセスをクラスター内で識別できます。
-   デフォルト値: `hostname:port number` 。たとえば、 `node-1:8250`です。

### 安全 {#security}

セキュリティに関する設定項目を紹介します。

#### SSL CA {#ssl-ca}

-   信頼できる SSL 証明書リストまたは CA リストのファイル パスを指定します。たとえば、 `/path/to/ca.pem`です。
-   デフォルト値: &quot;&quot;

#### SSL証明書 {#ssl-cert}

-   Privacy Enhanced Mail (PEM) 形式でエンコードされた X509 証明書ファイルのパスを指定します。たとえば、 `/path/to/pump.pem`です。
-   デフォルト値: &quot;&quot;

#### SSL キー {#ssl-key}

-   PEM 形式でエンコードされた X509 キー ファイルのパスを指定します。たとえば、 `/path/to/pump-key.pem`です。
-   デフォルト値: &quot;&quot;

### storage {#storage}

storageに関する設定項目を紹介します。

#### 同期ログ {#sync-log}

-   データの安全性を確保するために、 binlogへの各**バッチ**書き込みの後に`fsync`を使用するかどうかを指定します。
-   デフォルト値: `true`

#### kv_chan_cap {#kv-chan-cap}

-   Pumpがこれらの要求を受信する前に、バッファが格納できる書き込み要求の数を指定します。
-   デフォルト値: `1048576` (つまり、2 の 20 乗)

#### slow_write_threshold {#slow-write-threshold}

-   しきい値 (秒単位)。この指定されたしきい値よりも 1 つのbinlogファイルの書き込みに時間がかかる場合、書き込みは低速書き込みと見なされ、ログに`"take a long time to write binlog"`が出力されます。
-   デフォルト値: `1`

#### 使用可能なスペースで書き込みを停止 {#stop-write-at-available-space}

-   使用可能なstorage容量がこの指定値を下回ると、 Binlog書き込みリクエストは受け入れられなくなります。 `900 MB` 、 `5 GB` 、 `12 GiB`などの形式を使用して、storage領域を指定できます。クラスター内に複数のPumpノードがある場合、容量不足のためにPumpノードが書き込み要求を拒否すると、TiDB はバイナリログを他のPumpノードに自動的に書き込みます。
-   デフォルト値: `10 GiB`

#### kv {#kv}

現在、 Pumpのstorageは[GoLevelDB](https://github.com/syndtr/goleveldb)に基づいて実装されています。 `storage`の下には、GoLevel 構成を調整するために使用される`kv`サブグループもあります。サポートされている構成アイテムは次のとおりです。

-   ブロックキャッシュ容量
-   ブロック再起動間隔
-   ブロックサイズ
-   圧縮-L0-トリガー
-   圧縮テーブルのサイズ
-   圧縮合計サイズ
-   圧縮合計サイズ乗数
-   書き込みバッファ
-   書き込み-L0-一時停止トリガー
-   書き込み-L0-スローダウン-トリガー

上記の項目の詳細な説明については、 [GoLevelDB ドキュメント](https://godoc.org/github.com/syndtr/goleveldb/leveldb/opt#Options)を参照してください。

## Drainer {#drainer}

Drainerの設定項目を紹介します。完全なDrainer構成ファイルの例については、 [Drainerコンフィグレーション](https://github.com/pingcap/tidb-binlog/blob/master/cmd/drainer/drainer.toml)を参照してください。

### アドレス {#addr}

-   HTTP API のリッスン アドレスを`host:port`の形式で指定します。
-   デフォルト値: `127.0.0.1:8249`

### 広告アドレス {#advertise-addr}

-   外部からアクセス可能な HTTP API アドレスを指定します。このアドレスは`host:port`の形式で PD に登録されます。
-   デフォルト値: `127.0.0.1:8249`

### ログファイル {#log-file}

-   ログ ファイルが保存されるパスを指定します。パラメータが空の値に設定されている場合、ログ ファイルは保存されません。
-   デフォルト値: &quot;&quot;

### ログレベル {#log-level}

-   ログ レベルを指定します。
-   デフォルト値: `info`

### ノード ID {#node-id}

-   Drainerノード ID を指定します。この ID を使用して、このDrainerプロセスをクラスター内で識別できます。
-   デフォルト値: `hostname:port number` 。たとえば、 `node-1:8249`です。

### データディレクトリ {#data-dir}

-   Drainer操作中に保存する必要があるファイルを格納するために使用されるディレクトリを指定します。
-   デフォルト値: `data.drainer`

### 検出間隔 {#detect-interval}

-   PD がPump情報を更新する間隔 (秒単位) を指定します。
-   デフォルト値: `5`

### pd-url {#pd-urls}

-   PD URL のコンマ区切りリスト。複数のアドレスが指定されている場合、1 つのアドレスへの接続時にエラーが発生すると、PD クライアントは自動的に別のアドレスへの接続を試みます。
-   デフォルト値: `http://127.0.0.1:2379`

### 初期コミット ts {#initial-commit-ts}

-   レプリケーション プロセスを開始するトランザクションのコミット タイムスタンプを指定します。この構成は、初めてレプリケーション プロセスにあるDrainerノードにのみ適用されます。ダウンストリームにチェックポイントがすでに存在する場合、チェックポイントに記録された時間に従ってレプリケーションが実行されます。
-   commit ts (コミット タイムスタンプ) は、TiDB での[取引](/transaction-overview.md#transactions)コミットの特定の時点です。これは、現在のトランザクションの一意の ID として PD からグローバルに一意で増加するタイムスタンプです。次の一般的な方法で`initial-commit-ts`構成を取得できます。
    -   BRを使用した場合、 BRがバックアップするメタデータ (backupmeta) に記録されているバックアップ TS から`initial-commit-ts`取得できます。
    -   Dumplingを利用した場合、 Dumplingがバックアップするメタデータ(メタデータ)に記録されているPosから`initial-commit-ts`取得でき、
    -   PD Controlが使用されている場合、 `initial-commit-ts`は`tso`コマンドの出力になります。
-   デフォルト値: `-1` 。 Drainer は、開始時刻として PD から新しいタイムスタンプを取得します。これは、レプリケーション プロセスが現在の時刻から開始されることを意味します。

### 同期チェック時刻 {#synced-check-time}

-   HTTP API 経由で`/status`パスにアクセスして、 Drainerレプリケーションのステータスを照会できます。 `synced-check-time`最後に複製が成功してから何分後に`synced`と見なされるかを指定します。つまり、複製が完了したと見なされます。
-   デフォルト値: `5`

### コンプレッサー {#compressor}

-   PumpとDrainer間のデータ転送に使用される圧縮アルゴリズムを指定します。現在、 `gzip`アルゴリズムのみがサポートされています。
-   デフォルト値: &quot;&quot;。これは圧縮なしを意味します。

### 安全 {#security}

セキュリティに関する設定項目を紹介します。

#### SSL CA {#ssl-ca}

-   信頼できる SSL 証明書リストまたは CA リストのファイル パスを指定します。たとえば、 `/path/to/ca.pem`です。
-   デフォルト値: &quot;&quot;

#### SSL証明書 {#ssl-cert}

-   PEM 形式でエンコードされた X509 証明書ファイルのパスを指定します。たとえば、 `/path/to/drainer.pem`です。
-   デフォルト値: &quot;&quot;

#### SSL キー {#ssl-key}

-   PEM 形式でエンコードされた X509 キー ファイルのパスを指定します。たとえば、 `/path/to/pump-key.pem`です。
-   デフォルト値: &quot;&quot;

### シンカー {#syncer}

`syncer`セクションには、ダウンストリームに関連する構成項目が含まれます。

#### データベースタイプ {#db-type}

現在、次のダウンストリーム タイプがサポートされています。

-   `mysql`
-   `tidb`
-   `kafka`
-   `file`

デフォルト値: `mysql`

#### SQL モード {#sql-mode}

-   ダウンストリームが`mysql`または`tidb`タイプの場合の SQL モードを指定します。複数のモードがある場合は、カンマで区切ります。
-   デフォルト値: &quot;&quot;

#### 無視-txn-コミット-ts {#ignore-txn-commit-ts}

-   binlogが無視されるコミット タイムスタンプ ( `[416815754209656834, 421349811963822081]`など) を指定します。
-   デフォルト値: `[]`

#### 無視スキーマ {#ignore-schemas}

-   レプリケーション中に無視するデータベースを指定します。無視するデータベースが複数ある場合は、カンマで区切ります。 binlogファイル内のすべての変更がフィルター処理された場合、 binlogファイル全体が無視されます。
-   デフォルト値: `INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql`

#### 無視テーブル {#ignore-table}

レプリケーション中に指定されたテーブルの変更を無視します。 `toml`のファイルで無視するテーブルを複数指定できます。例えば：

{{< copyable "" >}}

```toml
[[syncer.ignore-table]]
db-name = "test"
tbl-name = "log"

[[syncer.ignore-table]]
db-name = "test"
tbl-name = "audit"
```

binlogファイル内のすべての変更がフィルター処理された場合、 binlogファイル全体が無視されます。

デフォルト値: `[]`

#### レプリケート-do-db {#replicate-do-db}

-   レプリケートするデータベースを指定します。たとえば、 `[db1, db2]`です。
-   デフォルト値: `[]`

#### レプリケート DO テーブル {#replicate-do-table}

レプリケートするテーブルを指定します。例えば：

{{< copyable "" >}}

```toml
[[syncer.replicate-do-table]]
db-name ="test"
tbl-name = "log"

[[syncer.replicate-do-table]]
db-name ="test"
tbl-name = "~^a.*"
```

デフォルト値: `[]`

#### txn-バッチ {#txn-batch}

-   ダウンストリームが`mysql`または`tidb`タイプの場合、DML 操作は別のバッチで実行されます。このパラメーターは、各トランザクションに含めることができる DML 操作の数を指定します。
-   デフォルト値: `20`

#### ワーカー数 {#worker-count}

-   ダウンストリームが`mysql`または`tidb`タイプの場合、DML操作は並行して実行されます。このパラメーターは、DML 操作の同時実行数を指定します。
-   デフォルト値: `16`

#### ディスパッチを無効にする {#disable-dispatch}

-   同時実行を無効にし、強制的に`worker-count`から`1`に設定します。
-   デフォルト値: `false`

#### セーフモード {#safe-mode}

セーフ モードが有効になっている場合、 Drainer はレプリケーションの更新を次のように変更します。

-   `Insert`は`Replace Into`に変更されます
-   `Update`は`Delete`プラス`Replace Into`に変更されます

デフォルト値: `false`

### syncer.to {#syncer-to}

`syncer.to`セクションでは、構成の種類に応じて、さまざまな種類のダウンストリーム構成項目を紹介します。

#### mysql/tidb {#mysql-tidb}

次の構成項目は、ダウンストリーム データベースへの接続に関連しています。

-   `host` : この項目が設定されていない場合、TiDB Binlog はデフォルトで`localhost`である`MYSQL_HOST`環境変数をチェックしようとします。
-   `port` : この項目が設定されていない場合、TiDB Binlog はデフォルトで`3306`である`MYSQL_PORT`環境変数をチェックしようとします。
-   `user` : この項目が設定されていない場合、TiDB Binlog はデフォルトで`root`である`MYSQL_USER`環境変数をチェックしようとします。
-   `password` : この項目が設定されていない場合、TiDB Binlog はデフォルトで`""`である`MYSQL_PSWD`環境変数をチェックしようとします。
-   `read-timeout` : ダウンストリーム データベース接続の I/O 読み取りタイムアウトを指定します。デフォルト値は`1m`です。時間がかかる一部の DDL でDrainer が失敗し続ける場合は、この構成をより大きな値に設定できます。

#### ファイル {#file}

-   `dir` : binlogファイルが保存されるディレクトリを指定します。この項目が設定されていない場合は、 `data-dir`が使用されます。

#### カフカ {#kafka}

ダウンストリームが Kafka の場合、有効な構成項目は次のとおりです。

-   `zookeeper-addrs`
-   `kafka-addrs`
-   `kafka-version`
-   `kafka-max-messages`
-   `kafka-max-message-size`
-   `topic-name`

### syncer.to.checkpoint {#syncer-to-checkpoint}

-   `type` : レプリケーションの進行状況を保存する方法を指定します。現在、使用可能なオプションは`mysql` 、 `tidb` 、および`file`です。

    この構成項目は、既定ではダウンストリーム タイプと同じです。たとえば、ダウンストリームが`file`の場合、チェックポイントの進行状況はローカル ファイル`<data-dir>/savepoint`に保存されます。ダウンストリームが`mysql`の場合、進行状況はダウンストリーム データベースに保存されます。進行状況を保存するために`mysql`または`tidb`を使用して明示的に指定する必要がある場合は、次の構成を行います。

-   `schema` : デフォルトでは`"tidb_binlog"`です。

    > **ノート：**
    >
    > 複数のDrainerノードを同じ TiDB クラスターにデプロイする場合、ノードごとに異なるチェックポイント スキーマを指定する必要があります。そうしないと、2 つのインスタンスのレプリケーションの進行状況が互いに上書きされます。

-   `host`

-   `user`

-   `password`

-   `port`
