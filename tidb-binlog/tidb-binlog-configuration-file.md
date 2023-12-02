---
title: TiDB Binlog Configuration File
summary: Learn the configuration items of TiDB Binlog.
---

# TiDBBinlogコンフィグレーションファイル {#tidb-binlog-configuration-file}

本書では、TiDB Binlogの設定項目を紹介します。

## Pump {#pump}

このセクションでは、 Pumpの設定項目を紹介します。完全なPump構成ファイルの例については、 [Pumpコンフィグレーション](https://github.com/pingcap/tidb-binlog/blob/release-7.5/cmd/pump/pump.toml)を参照してください。

### アドレス {#addr}

-   HTTP APIのリスニングアドレスを`host:port`の形式で指定します。
-   デフォルト値: `127.0.0.1:8250`

### アドバタイズアドレス {#advertise-addr}

-   外部からアクセス可能なHTTP APIアドレスを指定します。このアドレスは`host:port`の形式で PD に登録されます。
-   デフォルト値: `127.0.0.1:8250`

### ソケット {#socket}

-   HTTP API がリッスンする Unix ソケット アドレス。
-   デフォルト値: &quot;&quot;

### pd-url {#pd-urls}

-   PD URL のカンマ区切りリストを指定します。複数のアドレスが指定されている場合、PD クライアントは 1 つのアドレスへの接続に失敗すると、自動的に別のアドレスへの接続を試みます。
-   デフォルト値: `http://127.0.0.1:2379`

### データディレクトリ {#data-dir}

-   binlog とそのインデックスがローカルに保存されるディレクトリを指定します。
-   デフォルト値: `data.pump`

### ハートビート間隔 {#heartbeat-interval}

-   最新のステータスを PD に報告するハートビート間隔 (秒単位) を指定します。
-   デフォルト値: `2`

### gen-binlog-interval {#gen-binlog-interval}

-   データが偽のbinlogに書き込まれる間隔 (秒単位) を指定します。
-   デフォルト値: `3`

### GC {#gc}

-   バイナリログをローカルに保存できる日数 (整数) を指定します。指定した日数を超えて保存されたバイナリログは自動的に削除されます。
-   デフォルト値: `7`

### ログファイル {#log-file}

-   ログファイルが保存されるパスを指定します。パラメータが空の値に設定されている場合、ログ ファイルは保存されません。
-   デフォルト値: &quot;&quot;

### ログレベル {#log-level}

-   ログレベルを指定します。
-   デフォルト値: `info`

### ノードID {#node-id}

-   Pumpノード ID を指定します。この ID により、クラスター内でこのPumpプロセスを識別できます。
-   デフォルト値: `hostname:port number` 。たとえば、 `node-1:8250` 。

### 安全 {#security}

セキュリティに関する設定項目を紹介します。

#### ssl-ca {#ssl-ca}

-   信頼できる SSL 証明書リストまたは CA リストのファイル パスを指定します。たとえば、 `/path/to/ca.pem` 。
-   デフォルト値: &quot;&quot;

#### ssl-cert {#ssl-cert}

-   Privacy Enhanced Mail (PEM) 形式でエンコードされた X509 証明書ファイルのパスを指定します。たとえば、 `/path/to/pump.pem` 。
-   デフォルト値: &quot;&quot;

#### SSLキー {#ssl-key}

-   PEM 形式でエンコードされた X509 キー ファイルのパスを指定します。たとえば、 `/path/to/pump-key.pem` 。
-   デフォルト値: &quot;&quot;

### storage {#storage}

このセクションでは、storageに関する設定項目を紹介します。

#### 同期ログ {#sync-log}

-   データの安全性を確保するために、 binlogへの各**バッチ**書き込み後に`fsync`を使用するかどうかを指定します。
-   デフォルト値: `true`

#### kv_chan_cap {#kv-chan-cap}

-   Pumpがこれらのリクエストを受信するまでにバッファーが保存できる書き込みリクエストの数を指定します。
-   デフォルト値: `1048576` (つまり、2の20乗)

#### low_write_threshold {#slow-write-threshold}

-   しきい値 (秒単位)。 1 つのbinlogファイルの書き込みにこの指定されたしきい値よりも長い時間がかかる場合、その書き込みは低速書き込みとみなされ、ログに`"take a long time to write binlog"`が出力されます。
-   デフォルト値: `1`

#### 利用可能なスペースで書き込みを停止 {#stop-write-at-available-space}

-   利用可能なstorage容量がこの指定値を下回る場合、Binlog書き込みリクエストは受け付けられなくなります。 `900 MB` 、 `5 GB` 、 `12 GiB`などの形式を使用してstorageスペースを指定できます。クラスター内に複数のPumpノードがある場合、スペース不足のためにPumpノードが書き込みリクエストを拒否すると、TiDB は自動的にバイナリログを他のPumpノードに書き込みます。
-   デフォルト値: `10 GiB`

#### kv {#kv}

現在、Pumpのstorageは[GoLevelDB](https://github.com/syndtr/goleveldb)に基づいて実装されています。 `storage`の下には、GoLevel 構成を調整するために使用される`kv`サブグループもあります。サポートされている設定項目は以下のとおりです。

-   ブロックキャッシュ容量
-   ブロック再起動間隔
-   ブロックサイズ
-   圧縮-L0-トリガー
-   圧縮テーブルのサイズ
-   圧縮の合計サイズ
-   圧縮合計サイズ乗数
-   書き込みバッファ
-   書き込み-L0-一時停止トリガー
-   書き込み-L0-スローダウントリガー

上記項目の詳細については、 [GoLevelDB ドキュメント](https://godoc.org/github.com/syndtr/goleveldb/leveldb/opt#Options)を参照してください。

## Drainer {#drainer}

ここでは、 Drainerの設定項目を紹介します。完全なDrainer構成ファイルの例については、 [Drainerコンフィグレーション](https://github.com/pingcap/tidb-binlog/blob/release-7.5/cmd/drainer/drainer.toml)を参照してください。

### アドレス {#addr}

-   HTTP APIのリスニングアドレスを`host:port`の形式で指定します。
-   デフォルト値: `127.0.0.1:8249`

### アドバタイズアドレス {#advertise-addr}

-   外部からアクセス可能なHTTP APIアドレスを指定します。このアドレスは`host:port`の形式で PD に登録されます。
-   デフォルト値: `127.0.0.1:8249`

### ログファイル {#log-file}

-   ログファイルが保存されるパスを指定します。パラメータが空の値に設定されている場合、ログ ファイルは保存されません。
-   デフォルト値: &quot;&quot;

### ログレベル {#log-level}

-   ログレベルを指定します。
-   デフォルト値: `info`

### ノードID {#node-id}

-   DrainerノードIDを指定します。この ID により、クラスター内でこのDrainerプロセスを識別できます。
-   デフォルト値: `hostname:port number` 。たとえば、 `node-1:8249` 。

### データディレクトリ {#data-dir}

-   Drainer の操作中に保存する必要があるファイルを保存するために使用するディレクトリを指定します。
-   デフォルト値: `data.drainer`

### 検出間隔 {#detect-interval}

-   PD がPump情報を更新する間隔 (秒単位) を指定します。
-   デフォルト値: `5`

### pd-url {#pd-urls}

-   PD URL のカンマ区切りのリスト。複数のアドレスが指定されている場合、1 つのアドレスへの接続時にエラーが発生した場合、PD クライアントは自動的に別のアドレスへの接続を試みます。
-   デフォルト値: `http://127.0.0.1:2379`

### 初期コミット-ts {#initial-commit-ts}

-   トランザクションのどのコミット タイムスタンプからレプリケーション プロセスを開始するかを指定します。この構成は、初めてレプリケーション プロセスにあるDrainerノードにのみ適用されます。ダウンストリームにチェックポイントがすでに存在する場合、レプリケーションはチェックポイントに記録された時間に従って実行されます。
-   commit ts (コミット タイムスタンプ) は、TiDB における[取引](/transaction-overview.md#transactions)コミットの特定の時点です。これは、現在のトランザクションの一意の ID として PD から取得される、グローバルに一意で増加するタイムスタンプです。 `initial-commit-ts`構成は、次の一般的な方法で取得できます。
    -   BRを使用した場合、 BRでバックアップされたメタデータ(backupmeta)に記録されているバックアップTSから`initial-commit-ts`を取得できます。
    -   Dumplingを使用すると、 Dumplingでバックアップされたメタデータ(メタデータ)に記録されているPosから`initial-commit-ts`を取得でき、
    -   PD Controlが使用されている場合、 `tso`コマンドの出力には`initial-commit-ts`が含まれます。
-   デフォルト値: `-1` 。 Drainer は開始時刻として PD から新しいタイムスタンプを取得します。これは、レプリケーション プロセスが現在の時刻から開始されることを意味します。

### 同期チェック時間 {#synced-check-time}

-   HTTP API を介して`/status`パスにアクセスして、 Drainerレプリケーションのステータスをクエリできます。 `synced-check-time`最後に成功したレプリケーションから何分後を`synced` 、つまりレプリケーションが完了したとみなすかを指定します。
-   デフォルト値: `5`

### コンプレッサー {#compressor}

-   PumpとDrainer間のデータ転送に使用される圧縮アルゴリズムを指定します。現在、 `gzip`アルゴリズムのみがサポートされています。
-   デフォルト値: &quot;&quot;、圧縮なしを意味します。

### 安全 {#security}

セキュリティに関する設定項目を紹介します。

#### ssl-ca {#ssl-ca}

-   信頼できる SSL 証明書リストまたは CA リストのファイル パスを指定します。たとえば、 `/path/to/ca.pem` 。
-   デフォルト値: &quot;&quot;

#### ssl-cert {#ssl-cert}

-   PEM 形式でエンコードされた X509 証明書ファイルのパスを指定します。たとえば、 `/path/to/drainer.pem` 。
-   デフォルト値: &quot;&quot;

#### SSLキー {#ssl-key}

-   PEM 形式でエンコードされた X509 キー ファイルのパスを指定します。たとえば、 `/path/to/pump-key.pem` 。
-   デフォルト値: &quot;&quot;

### シンクロ {#syncer}

`syncer`セクションには、ダウンストリームに関連する設定項目が含まれます。

#### データベースタイプ {#db-type}

現在、次のダウンストリーム タイプがサポートされています。

-   `mysql`
-   `tidb`
-   `kafka`
-   `file`

デフォルト値: `mysql`

#### SQLモード {#sql-mode}

-   下流が`mysql`型または`tidb`型の場合のSQLモードを指定します。複数のモードがある場合は、カンマを使用して区切ります。
-   デフォルト値: &quot;&quot;

#### 無視-txn-コミット-ts {#ignore-txn-commit-ts}

-   binlogが無視されるコミット タイムスタンプ ( `[416815754209656834, 421349811963822081]`など) を指定します。
-   デフォルト値: `[]`

#### スキーマを無視する {#ignore-schemas}

-   レプリケーション中に無視するデータベースを指定します。無視するデータベースが複数ある場合は、カンマを使用してそれらを区切ります。 binlogファイル内のすべての変更がフィルタリングされる場合、 binlogファイル全体が無視されます。
-   デフォルト値: `INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql`

#### 無視テーブル {#ignore-table}

レプリケーション中に指定されたテーブルの変更を無視します。 `toml`ファイル内で無視する複数のテーブルを指定できます。例えば：

```toml
[[syncer.ignore-table]]
db-name = "test"
tbl-name = "log"

[[syncer.ignore-table]]
db-name = "test"
tbl-name = "audit"
```

binlogファイル内のすべての変更がフィルタリングされる場合、 binlogファイル全体が無視されます。

デフォルト値: `[]`

#### レプリケート-do-db {#replicate-do-db}

-   レプリケートするデータベースを指定します。たとえば、 `[db1, db2]` 。
-   デフォルト値: `[]`

#### 複製実行テーブル {#replicate-do-table}

レプリケートするテーブルを指定します。例えば：

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

-   下流が`mysql`または`tidb`の場合、DML 操作は別のバッチで実行されます。このパラメータは、各トランザクションに含めることができる DML 操作の数を指定します。
-   デフォルト値: `20`

#### ワーカー数 {#worker-count}

-   下流が`mysql`または`tidb`の場合、DML 操作は並行して実行されます。このパラメータは、DML 操作の同時実行数を指定します。
-   デフォルト値: `16`

#### ディスパッチを無効にする {#disable-dispatch}

-   同時実行を無効にし、強制的に`worker-count` ～ `1`に設定します。
-   デフォルト値: `false`

#### セーフモード {#safe-mode}

セーフ モードが有効な場合、 Drainer は次の方法でレプリケーションの更新を変更します。

-   `Insert`は`Replace Into`に変更されます
-   `Update`は`Delete`プラス`Replace Into`に変更されます

デフォルト値: `false`

### 同期者.to {#syncer-to}

`syncer.to`セクションでは、構成タイプに応じて、さまざまなタイプのダウンストリーム構成項目を紹介します。

#### mysql/tidb {#mysql-tidb}

次の構成項目は、ダウンストリーム データベースへの接続に関連しています。

-   `host` : この項目が設定されていない場合、TiDB Binlog は`MYSQL_HOST`環境変数 (デフォルトでは`localhost`をチェックしようとします。
-   `port` : この項目が設定されていない場合、TiDB Binlog は`MYSQL_PORT`環境変数 (デフォルトでは`3306`をチェックしようとします。
-   `user` : この項目が設定されていない場合、TiDB Binlog は`MYSQL_USER`環境変数 (デフォルトでは`root`をチェックしようとします。
-   `password` : この項目が設定されていない場合、TiDB Binlog は`MYSQL_PSWD`環境変数 (デフォルトでは`""`をチェックしようとします。
-   `read-timeout` : ダウンストリーム データベース接続の I/O 読み取りタイムアウトを指定します。デフォルト値は`1m`です。長時間かかる一部の DDL でDrainer が失敗し続ける場合は、この構成をより大きな値に設定できます。

#### ファイル {#file}

-   `dir` : binlogファイルが保存されるディレクトリを指定します。この項目が設定されていない場合は、 `data-dir`が使用されます。

#### カフカ {#kafka}

ダウンストリームが Kafka の場合、有効な設定項目は次のとおりです。

-   `zookeeper-addrs`
-   `kafka-addrs`
-   `kafka-version`
-   `kafka-max-messages`
-   `kafka-max-message-size`
-   `topic-name`

### チェックポイントへの同期 {#syncer-to-checkpoint}

-   `type` : レプリケーションの進行状況を保存する方法を指定します。現在、使用可能なオプションは`mysql` 、 `tidb` 、および`file`です。

    この設定項目はデフォルトでは下流タイプと同じです。たとえば、ダウンストリームが`file`の場合、チェックポイントの進行状況はローカル ファイル`<data-dir>/savepoint`に保存されます。ダウンストリームが`mysql`の場合、進行状況はダウンストリーム データベースに保存されます。進行状況を保存するために`mysql`または`tidb`を使用して明示的に指定する必要がある場合は、次の構成を行います。

-   デフォルトでは`schema` : `"tidb_binlog"`です。

    > **注記：**
    >
    > 同じ TiDB クラスターに複数のDrainerノードをデプロイする場合、ノードごとに異なるチェックポイント スキーマを指定する必要があります。そうしないと、2 つのインスタンスのレプリケーションの進行状況が互いに上書きされます。

-   `host`

-   `user`

-   `password`

-   `port`
