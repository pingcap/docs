---
title: CLI and Configuration Parameters of TiCDC Changefeeds
summary: TiCDCチェンジフィードのCLIの定義と設定パラメータについて学びましょう。
---

# TiCDC ChangefeedsのCLIとコンフィグレーションパラメータ {#cli-and-configuration-parameters-of-ticdc-changefeeds}

## 変更フィードCLIパラメータ {#changefeed-cli-parameters}

このセクションでは、TiCDCチェンジフィードのコマンドラインパラメータについて、レプリケーション（チェンジフィード）タスクの作成方法を示すことで紹介します。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2025-11-27T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.5.4"}
```

-   `--changefeed-id` : レプリケーションタスクのID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現に一致する必要があります。このIDが指定されていない場合、TiCDCは自動的にUUID（バージョン4形式）をIDとして生成します。

-   `--sink-uri` : レプリケーション タスクのダウンストリーム アドレス。 `--sink-uri`は、次の形式に従って設定します。現在、このスキームは`mysql` 、 `tidb` 、および`kafka`をサポートしています。

        [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]

    シンク URI パラメータに`! * ' ( ) ; : @ & = + $ , / ? % # [ ]`などの特殊文字が含まれている場合は、 [URIエンコーダー](https://www.urlencoder.org/)のように特殊文字をエスケープする必要があります。

-   `--start-ts` : 変更フィードの開始TSOを指定します。TiCDCクラスタはこのTSOからデータの取得を開始します。デフォルト値は現在時刻です。

-   `--target-ts` : 変更フィードの終了TSOを指定します。このTSOに達すると、TiCDCクラスタはデータのプルを停止します。デフォルト値は空で、これはTiCDCが自動的にデータのプルを停止しないことを意味します。

-   `--config` : 変更フィードの設定ファイルを指定します。

## 変更フィードの設定パラメータ {#changefeed-configuration-parameters}

このセクションでは、レプリケーションタスクの設定について説明します。

### <code>memory-quota</code> {#code-memory-quota-code}

-   シンクマネージャがキャプチャサーバーで使用できるメモリ割り当て量（バイト単位）を指定します。この値を超過した場合、超過した部分はGoランタイムによって再利用されます。
-   デフォルト値: `1073741824` (1 GiB)

### <code>case-sensitive</code> {#code-case-sensitive-code}

-   構成ファイル内のデータベース名とテーブルが大文字と小文字を区別するかどうかを指定します。v6.5.6、v7.1.3、v7.5.0 以降、デフォルト値は`true`から`false`に変更されます。
-   この設定項目は、フィルターとシンクに関連する設定に影響します。
-   デフォルト値: `false`

### <code>force-replicate</code> {#code-force-replicate-code}

-   [有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)かどうかを指定します。
-   デフォルト値: `false`

### <code>enable-sync-point</code> <span class="version-mark">v6.3.0で追加</span> {#code-enable-sync-point-code-span-class-version-mark-new-in-v6-3-0-span}

-   Syncpoint機能を有効にするかどうかを指定します。この機能はバージョン6.3.0以降でサポートされており、デフォルトでは無効になっています。
-   バージョン6.4.0以降、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`の権限を持つチェンジフィードのみがTiCDC Syncpoint機能を使用できます。
-   この設定項目は、ダウンストリームがTiDBの場合にのみ有効になります。
-   デフォルト値: `false`

### <code>sync-point-interval</code> {#code-sync-point-interval-code}

-   Syncpointがアップストリームとダウンストリームのスナップショットを同期させる間隔を指定します。
-   この設定項目は、ダウンストリームがTiDBの場合にのみ有効になります。
-   形式は`"h m s"`です。例えば、 `"1h30m30s"`です。
-   デフォルト値: `"10m"`
-   最小値: `"30s"`

### <code>sync-point-retention</code> {#code-sync-point-retention-code}

-   Syncpointがダウンストリームテーブルにデータを保持する期間を指定します。この期間を超えると、データは削除されます。
-   この設定項目は、ダウンストリームがTiDBの場合にのみ有効になります。
-   形式は`"h m s"`です。例えば、 `"24h30m30s"`です。
-   デフォルト値: `"24h"`

### <code>sql-mode</code> <span class="version-mark">v6.5.6、v7.1.3、v7.5.0 で新たに追加されました。</span> {#code-sql-mode-code-span-class-version-mark-new-in-v6-5-6-v7-1-3-and-v7-5-0-span}

-   DDLステートメントを解析する際に使用する[SQLモード](/sql-mode.md)を指定します。複数のモードを指定する場合は、カンマで区切ります。
-   デフォルト値： `"ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"` 。これはTiDBのデフォルトのSQLモードと同じです。

### <code>bdr-mode</code> {#code-bdr-mode-code}

-   TiCDC を使用して BDR (双方向レプリケーション) クラスターをセットアップするには、このパラメーターを`true`に変更し、TiDB クラスターを BDR モードに設定します。詳細については、 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md#bidirectional-replication)参照してください。
-   デフォルト値： `false` 。双方向レプリケーション（BDR）モードが有効になっていないことを示します。

### <code>changefeed-error-stuck-duration</code> {#code-changefeed-error-stuck-duration-code}

-   内部エラーや例外が発生した場合に、チェンジフィードが自動的に再試行できる期間を指定します。
-   変更フィード内で内部エラーまたは例外が発生し、このパラメータで設定された期間よりも長く継続した場合、変更フィードは失敗状態になります。
-   変更フィードが障害状態になった場合は、リカバリのために変更フィードを手動で再起動する必要があります。
-   形式は`"h m s"`です。例えば、 `"1h30m30s"`です。
-   デフォルト値: `"30m"`

### マウンター {#mounter}

#### <code>worker-num</code> {#code-worker-num-code}

-   マウンターがKVデータをデコードする際に使用するスレッド数を指定します。
-   デフォルト値: `16`

### フィルター {#filter}

#### <code>ignore-txn-start-ts</code> {#code-ignore-txn-start-ts-code}

-   指定されたstart_tsのトランザクションを無視します。

<!-- Example: `[1, 2]` -->

#### <code>rules</code> {#code-rules-code}

-   フィルタルールを指定します。詳細については、[構文](/table-filter.md#syntax)を参照してください。

<!-- Example: `['*.*', '!test.*']` -->

#### フィルター.イベントフィルター {#filter-event-filters}

詳細については、 [イベントフィルタルール](/ticdc/ticdc-filter.md#event-filter-rules)を参照してください。

##### <code>matcher</code> {#code-matcher-code}

-   `matcher`は許可リストです。 `matcher = ["test.worker"]`は、このルールが`worker`データベース内の`test`テーブルにのみ適用されることを意味します。

##### <code>ignore-event</code> {#code-ignore-event-code}

-   `ignore-event = ["insert"]`は`INSERT`イベントを無視します。
-   `ignore-event = ["drop table", "delete"]`は`DROP TABLE` DDL イベントと`DELETE` DML イベントを無視します。 TiDB でクラスタ化インデックス列の値が更新されると、TiCDC は`UPDATE`イベントを`DELETE`イベントと`INSERT`イベントに分割することに注意してください。 TiCDC はこれらのイベントを`UPDATE`イベントとして識別できないため、これらのイベントを正しくフィルタリングできません。

##### <code>ignore-sql</code> {#code-ignore-sql-code}

-   `ignore-sql = ["^drop", "add column"]` `DROP`で始まる、または`ADD COLUMN`を含む DDL を無視します。

##### <code>ignore-delete-value-expr</code> {#code-ignore-delete-value-expr-code}

-   `ignore-delete-value-expr = "name = 'john'"`は、条件`DELETE`を含む`name = 'john'` DML を無視します。

##### <code>ignore-insert-value-expr</code> {#code-ignore-insert-value-expr-code}

-   `ignore-insert-value-expr = "id >= 100"`は、条件`INSERT`を含む`id >= 100` DML を無視します。

##### <code>ignore-update-old-value-expr</code> {#code-ignore-update-old-value-expr-code}

-   `ignore-update-old-value-expr = "age < 18"`は、古い値に`UPDATE`が含まれる`age < 18` DML を無視します。

##### <code>ignore-update-new-value-expr</code> {#code-ignore-update-new-value-expr-code}

-   `ignore-update-new-value-expr = "gender = 'male'"`は、新しい値に`UPDATE`が含まれる`gender = 'male'` DML を無視します。

### スケジューラ {#scheduler}

#### <code>enable-table-across-nodes</code> {#code-enable-table-across-nodes-code}

-   リージョンごとに、複数のTiCDCノードにテーブルを割り当ててレプリケーションを実行します。

-   [TiCDCクラシックアーキテクチャ](/ticdc/ticdc-classic-architecture.md)では、この構成項目は Kafka 変更フィードでのみ有効であり、MySQL 変更フィードではサポートされません。

-   [TiCDCの新アーキテクチャ](/ticdc/ticdc-architecture.md)では、この設定項目はあらゆる種類のダウンストリーム変更フィードで機能します。詳細については、 [新機能](/ticdc/ticdc-architecture.md#new-features)を参照してください。

-   `enable-table-across-nodes`が有効になっている場合、割り当てモードは2つあります。

    1.  リージョン数に基づいてテーブルを割り当て、各TiCDCノードがほぼ同数のリージョンを処理するようにします。テーブルのリージョン数が[`region-threshold`](#region-threshold)の値を超えると、そのテーブルはレプリケーションのために複数のノードに割り当てられます。
    2.  書き込みトラフィックに基づいてテーブルを割り当て、各TiCDCノードがほぼ同じ数の変更行を処理するようにします。この割り当ては、テーブル内の1分あたりの変更行数が[`write-key-threshold`](#write-key-threshold)の値を超えた場合にのみ有効になります。

    2 つのモードのうち、いずれか 1 つだけを設定すれば十分です。 `region-threshold`と`write-key-threshold`の両方が設定されている場合、TiCDC はトラフィック割り当てモード、つまり`write-key-threshold`を優先します。

-   デフォルト値は`false`です。この機能を有効にするには、 `true`に設定してください。

-   デフォルト値: `false`

#### <code>region-count-per-span</code> <span class="version-mark">v8.5.4の新機能）</span> {#code-region-count-per-span-code-span-class-version-mark-new-in-v8-5-4-span}

-   [TiCDCの新アーキテクチャ](/ticdc/ticdc-architecture.md)で紹介されました。チェンジフィードの初期化中に、TiCDC はこのパラメーターに従って分割条件を満たすテーブルを分割します。分割後、各サブテーブルには最大で`region-count-per-span`個のリージョンが含まれます。
-   デフォルト値: `100`

#### <code>region-threshold</code> {#code-region-threshold-code}

-   デフォルト値: [TiCDCの新アーキテクチャ](/ticdc/ticdc-architecture.md)の場合、デフォルト値は`10000`です。 [TiCDCクラシックアーキテクチャ](/ticdc/ticdc-classic-architecture.md)の場合、デフォルト値は`100000`です。

#### <code>write-key-threshold</code> {#code-write-key-threshold-code}

-   デフォルト値： `0` 。これは、トラフィック割り当てモードがデフォルトでは使用されないことを意味します。

### シンク {#sink}

<!-- MQ sink configuration items -->

#### <code>dispatchers</code> {#code-dispatchers-code}

-   MQタイプのシンクの場合、ディスパッチャを使用してイベントディスパッチャを設定できます。
-   バージョン6.1.0以降、TiDBはパーティションとトピックという2種類のイベントディスパッチャをサポートしています。
-   マッチャーのマッチング構文は、フィルタルールの構文と同じです。
-   この設定項目は、ダウンストリームがMQの場合にのみ有効になります。
-   ダウンストリーム MQ が Pulsar の場合、 `partition`のルーティング ルールが`ts` 、 `index-value` 、 `table` 、または`default`にも指定されていない場合、各 Pulsar メッセージは、キーとして設定した文字列を使用してルーティングされます。たとえば、マッチャーのルーティング ルールを文字列`code`として指定した場合、そのマッチャーに一致するすべての Pulsar メッセージは`code`をキーとしてルーティングされます。

#### <code>column-selectors</code> <span class="version-mark">v7.5.0の新機能）</span> {#code-column-selectors-code-span-class-version-mark-new-in-v7-5-0-span}

-   レプリケーション対象とする特定の列を選択します。この設定は、ダウンストリームがKafkaの場合にのみ有効です。

#### <code>protocol</code> {#code-protocol-code}

-   メッセージのエンコードに使用されるプロトコル形式を指定します。
-   この設定項目は、ダウンストリームがKafka、Pulsar、またはstorageサービスの場合にのみ有効になります。
-   ダウンストリームがKafkaの場合、プロトコルはcanal-json、avro、debezium、open-protocol、またはsimpleのいずれかになります。
-   ダウンストリームがPulsarの場合、プロトコルはcanal-jsonのみとなります。
-   ダウンストリームがstorageサービスの場合、プロトコルはcanal-jsonまたはcsvのみとなります。

<!-- Example: `"canal-json"` -->

#### <code>delete-only-output-handle-key-columns</code> <span class="version-mark">v7.2.0の新機能</span> {#code-delete-only-output-handle-key-columns-code-span-class-version-mark-new-in-v7-2-0-span}

-   DELETEイベントの出力を指定します。このパラメータは、canal-jsonおよびopen-protocolプロトコルでのみ有効です。
-   このパラメータは`force-replicate`と互換性がありません。このパラメータと`force-replicate`の両方が`true`に設定されている場合、TiCDC は変更フィードを作成する際にエラーを報告します。
-   Avroプロトコルはこのパラメータによって制御されず、常に主キー列または一意インデックス列のみを出力します。
-   CSVプロトコルはこのパラメータによって制御されず、常にすべての列を出力します。
-   デフォルト値： `false`これは、すべての列を出力することを意味します。
-   `true`に設定すると、主キー列または一意インデックス列のみが出力されます。

#### <code>schema-registry</code> {#code-schema-registry-code}

-   スキーマレジストリのURLを指定します。
-   この設定項目は、ダウンストリームがMQの場合にのみ有効になります。

<!-- Example: `"http://localhost:80801/subjects/{subject-name}/versions/{version-number}/schema"` -->

#### <code>encoder-concurrency</code> {#code-encoder-concurrency-code}

-   データのエンコード時に使用するエンコーダースレッドの数を指定します。
-   この設定項目は、ダウンストリームがMQの場合にのみ有効になります。
-   デフォルト値: `32`

#### <code>enable-kafka-sink-v2</code> {#code-enable-kafka-sink-v2-code}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   kafka-goシンクライブラリを使用するkafka-sink-v2を有効にするかどうかを指定します。
-   この設定項目は、ダウンストリームがMQの場合にのみ有効になります。
-   デフォルト値: `false`

#### <code>only-output-updated-columns</code> <span class="version-mark">v7.1.0の新機能</span> {#code-only-output-updated-columns-code-span-class-version-mark-new-in-v7-1-0-span}

-   更新された列のみを出力するかどうかを指定します。
-   この設定項目は、open-protocolとcanal-jsonを使用するMQダウンストリームにのみ適用されます。
-   デフォルト値: `false`

<!-- Storage sink configuration items -->

#### <code>terminator</code> {#code-terminator-code}

-   この構成項目は、データをstorageシンクにレプリケートする場合にのみ使用され、MQまたはMySQLシンクにデータをレプリケートする場合は無視できます。
-   2つのデータ変更イベントを区切るために使用される行終端文字を指定します。
-   デフォルト値: `""` 、つまり`\r\n`が使用されます。

#### <code>date-separator</code> {#code-date-separator-code}

-   ファイル ディレクトリで使用される日付区切り文字のタイプを指定します。詳細については、 [データ変更記録](/ticdc/ticdc-sink-to-cloud-storage.md#data-change-records)参照してください。
-   この設定項目は、ダウンストリームがstorageサービスである場合にのみ有効になります。
-   デフォルト値: `day` 、ファイルを日付ごとに分割することを意味します。
-   値のオプション: `none` 、 `year` 、 `month` 、 `day`

#### <code>enable-partition-separator</code> {#code-enable-partition-separator-code}

-   パーティションを区切り文字として使用するかどうかを制御します。
-   この設定項目は、ダウンストリームがstorageサービスである場合にのみ有効になります。
-   デフォルト値： `true` 。これは、テーブル内のパーティションが別々のディレクトリに保存されることを意味します。
-   この設定は将来のバージョンで非推奨となり、 `true`に強制的に設定されますのでご注意ください。下流のパーティションテーブルでのデータ損失を防ぐため、この設定はデフォルト値のままにしておくことをお勧めします。詳細については、 [第11979号](https://github.com/pingcap/tiflow/issues/11979)を参照してください。使用例については、データ[データ変更記録](/ticdc/ticdc-sink-to-cloud-storage.md#data-change-records)参照してください。

#### <code>debezium-disable-schema</code> {#code-debezium-disable-schema-code}

-   スキーマ情報の出力を無効にするかどうかを制御します。
-   デフォルト値： `false` 。これは、スキーマ情報の出力を有効にすることを意味します。
-   このパラメータは、シンクタイプがMQで、出力プロトコルがDebeziumの場合にのみ有効です。

#### sink.csv は<span class="version-mark">v6.5.0 で追加されました。</span> {#sink-csv-span-class-version-mark-new-in-v6-5-0-span}

バージョン6.5.0以降、TiCDCはデータ変更をCSV形式でstorageサービスに保存することをサポートしています。データをMQまたはMySQLシンクにレプリケートする場合は、以下の設定は無視してください。

##### <code>delimiter</code> {#code-delimiter-code}

-   CSVファイル内のフィールドを区切る文字を指定します。値はASCII文字である必要があります。
-   デフォルト値: `,`

##### <code>quote</code> {#code-quote-code}

-   CSVファイル内のフィールドを囲むために使用する引用符を指定します。値が空の場合は、引用符は使用されません。
-   デフォルト値: `"`

##### <code>null</code> {#code-null-code}

-   CSV列がNULLの場合に表示される文字を指定します。
-   デフォルト値: `\N`

##### <code>include-commit-ts</code> {#code-include-commit-ts-code}

-   CSV行にコミットTを含めるかどうかを制御します。
-   デフォルト値: `false`

##### <code>binary-encoding-method</code> {#code-binary-encoding-method-code}

-   バイナリデータのエンコード方法を指定します。
-   デフォルト値: `base64`
-   値オプション: `base64` 、 `hex`

##### <code>output-handle-key</code> {#code-output-handle-key-code}

-   ハンドルキー情報を出力するかどうかを制御します。この設定パラメータは内部実装専用であるため、設定することは推奨されません。
-   デフォルト値: `false`

##### <code>output-old-value</code> {#code-output-old-value-code}

-   行データが変更される前の値を出力するかどうかを制御します。デフォルト値はfalseです。
-   有効にすると（ `true`に設定すると）、 `UPDATE`イベントは 2 行のデータを出力します。1 行目は、変更前のデータを出力する`DELETE`イベントです。2 行目は、変更後のデータを出力する`INSERT`イベントです。
-   有効にすると、データ変更のある列の前に`"is-update"`列が追加されます。この追加された列は、現在の行のデータ変更が`UPDATE`イベントによるものか、元の`INSERT`イベントまたは`DELETE`イベントによるものかを識別するために使用されます。現在の行のデータ変更が`UPDATE`イベントによるものである場合、 `"is-update"`列の値は`true`になります。それ以外の場合は、 `false`になります。
-   デフォルト値: `false`

v8.0.0 以降、TiCDC はシンプル メッセージ エンコーディング プロトコルをサポートします。以下は、Simple プロトコルの構成パラメータです。プロトコルの詳細については、 [TiCDCシンプルプロトコル](/ticdc/ticdc-simple-protocol.md)を参照してください。

以下の設定パラメータは、ブートストラップメッセージの送信動作を制御します。

#### <code>send-bootstrap-interval-in-sec</code> {#code-send-bootstrap-interval-in-sec-code}

-   ブートストラップメッセージを送信する時間間隔を秒単位で制御します。
-   デフォルト値： `120` 。これは、各テーブルに対して120秒ごとにブートストラップメッセージが送信されることを意味します。
-   単位：秒

#### <code>send-bootstrap-in-msg-count</code> {#code-send-bootstrap-in-msg-count-code}

-   ブートストラップを送信するメッセージ間隔をメッセージ数で制御します。
-   デフォルト値： `10000` 。これは、各テーブルで10000行変更メッセージごとにブートストラップメッセージが送信されることを意味します。
-   ブートストラップ メッセージの送信を無効にする場合は、 [`send-bootstrap-interval-in-sec`](#send-bootstrap-interval-in-sec)と`send-bootstrap-in-msg-count`の両方を`0`に設定してください。

#### <code>send-bootstrap-to-all-partition</code> {#code-send-bootstrap-to-all-partition-code}

-   ブートストラップメッセージをすべてのパーティションに送信するかどうかを制御します。
-   `false`に設定すると、ブートストラップメッセージは対応するテーブルトピックの最初のパーティションにのみ送信されます。
-   デフォルト値： `true` 。これは、ブートストラップメッセージが対応するテーブルトピックのすべてのパーティションに送信されることを意味します。

#### sink.kafka-config.codec-config {#sink-kafka-config-codec-config}

##### <code>encoding-format</code> {#code-encoding-format-code}

-   Simpleプロトコルメッセージのエンコード形式を制御します。現在、Simpleプロトコルメッセージは`json`と`avro`エンコード形式をサポートしています。
-   デフォルト値: `json`
-   値のオプション: `json` 、 `avro`

#### シンクを開く {#sink-open}

##### <code>output-old-value</code> {#code-output-old-value-code}

-   行データが変更される前に値を出力するかどうかを制御します。デフォルト値は true です。無効にすると、 `UPDATE`イベントは「p」フィールドを出力しません。
-   デフォルト値: `true`

#### シンク.デベジウム {#sink-debezium}

##### <code>output-old-value</code> {#code-output-old-value-code}

-   行データが変更される前の値を出力するかどうかを制御します。デフォルト値は true です。無効にすると、 `UPDATE`イベントは「変更前」フィールドを出力しません。
-   デフォルト値: `true`

### 一貫性のある {#consistent}

REDO ログを使用する場合の変更フィードのレプリケーション整合性構成を指定します。詳細については、 [最終的には災害シナリオにおける一貫した再現](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)参照してください。

注：整合性関連の設定項目は、ダウンストリームがデータベースであり、かつリドゥログ機能が有効になっている場合にのみ有効になります。

#### <code>level</code> {#code-level-code}

-   データの一貫性レベル。 `"none"`は、リドゥログが無効になっていることを意味します。
-   デフォルト値: `"none"`
-   値のオプション: `"none"` 、 `"eventual"`

#### <code>max-log-size</code> {#code-max-log-size-code}

-   最大リドゥログサイズ。
-   デフォルト値: `64`
-   単位: MiB

#### <code>flush-interval</code> {#code-flush-interval-code}

-   リドゥログのフラッシュ間隔。
-   デフォルト値: `2000`
-   単位：ミリ秒

#### <code>storage</code> {#code-storage-code}

-   リドゥログのstorageURI。
-   デフォルト値: `""`

#### <code>use-file-backend</code> {#code-use-file-backend-code}

-   リドゥログをローカルファイルに保存するかどうかを指定します。
-   デフォルト値: `false`

#### <code>encoding-worker-num</code> {#code-encoding-worker-num-code}

-   リドゥモジュール内のエンコードワーカーとデコードワーカーの数。
-   デフォルト値: `16`

#### <code>flush-worker-num</code> {#code-flush-worker-num-code}

-   再実行モジュール内のフラッシングワーカーの数。
-   デフォルト値: `8`

#### <code>compression</code> <span class="version-mark">v6.5.6、v7.1.3、v7.5.1、v7.6.0で新たに追加されました。</span> {#code-compression-code-span-class-version-mark-new-in-v6-5-6-v7-1-3-v7-5-1-and-v7-6-0-span}

-   リドゥログファイルを圧縮する動作。
-   デフォルト値： `""` 、これは圧縮なしを意味します。
-   値のオプション: `""` 、 `"lz4"`

#### <code>flush-concurrency</code><span class="version-mark">は、v6.5.6、v7.1.3、v7.5.1、およびv7.6.0で追加されました。</span> {#code-flush-concurrency-code-span-class-version-mark-new-in-v6-5-6-v7-1-3-v7-5-1-and-v7-6-0-span}

-   単一のリドゥファイルをアップロードする際の同時実行数。
-   デフォルト値： `1` 。これは同時実行が無効になっていることを意味します。

### 誠実さ {#integrity}

#### <code>integrity-check-level</code> {#code-integrity-check-level-code}

-   単一行データに対するチェックサム検証を有効にするかどうかを制御します。
-   デフォルト値： `"none"`これは、機能を無効にすることを意味します。
-   値のオプション: `"none"` 、 `"correctness"`

#### <code>corruption-handle-level</code> {#code-corruption-handle-level-code}

-   単一行データのチェックサム検証が失敗した場合の変更フィードのログレベルを指定します。
-   デフォルト値: `"warn"`
-   値のオプション: `"warn"` 、 `"error"`

### sink.kafka-config {#sink-kafka-config}

以下の設定項目は、ダウンストリームがKafkaの場合にのみ有効になります。

#### <code>sasl-mechanism</code> {#code-sasl-mechanism-code}

-   Kafka SASL認証のメカニズムを指定します。
-   デフォルト値： `""`これは、SASL認証が使用されていないことを示します。

<!-- Example: `OAUTHBEARER` -->

#### <code>sasl-oauth-client-id</code> {#code-sasl-oauth-client-id-code}

-   Kafka SASL OAUTHBEARER認証におけるクライアントIDを指定します。OAUTHBEARER認証を使用する場合は、このパラメータが必須です。
-   デフォルト値: `""`

#### <code>sasl-oauth-client-secret</code> {#code-sasl-oauth-client-secret-code}

-   Kafka SASL OAUTHBEARER認証におけるクライアントシークレットを指定します。OAUTHBEARER認証を使用する場合は、このパラメータが必須です。
-   デフォルト値: `""`

#### <code>sasl-oauth-token-url</code> {#code-sasl-oauth-token-url-code}

-   Kafka SASL OAUTHBEARER認証において、トークンを取得するためのトークンURLを指定します。OAUTHBEARER認証を使用する場合は、このパラメータが必須です。
-   デフォルト値: `""`

#### <code>sasl-oauth-scopes</code> {#code-sasl-oauth-scopes-code}

-   Kafka SASL OAUTHBEARER認証におけるスコープを指定します。OAUTHBEARER認証を使用する場合、このパラメータは省略可能です。
-   デフォルト値: `""`

#### <code>sasl-oauth-grant-type</code> {#code-sasl-oauth-grant-type-code}

-   Kafka SASL OAUTHBEARER認証におけるグラントタイプを指定します。OAUTHBEARER認証を使用する場合、このパラメータは省略可能です。
-   デフォルト値: `"client_credentials"`

#### <code>sasl-oauth-audience</code> {#code-sasl-oauth-audience-code}

-   Kafka SASL OAUTHBEARER認証におけるオーディエンスを指定します。OAUTHBEARER認証を使用する場合、このパラメータは省略可能です。
-   デフォルト値: `""`

<!-- Example: `"kafka"` -->

#### <code>output-raw-change-event</code> {#code-output-raw-change-event-code}

-   元のデータ変更イベントを出力するかどうかを制御します。詳細については、 [プライマリキーまたはユニークキーの`UPDATE`イベントを分割するかどうかを制御します](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events)参照してください。
-   デフォルト値: `false`

### sink.kafka-config.glue-schema-registry-config {#sink-kafka-config-glue-schema-registry-config}

以下の設定は、プロトコルとしてAvroを使用し、AWS Glue Schema Registryを使用する場合にのみ必要です。

```toml
region="us-west-1"
registry-name="ticdc-test"
access-key="xxxx"
secret-access-key="xxxx"
token="xxxx"
```

詳細については、 [TiCDCをAWS Glueスキーマレジストリと統合する](/ticdc/ticdc-sink-to-kafka.md#integrate-ticdc-with-aws-glue-schema-registry)参照してください。

### sink.pulsar-config {#sink-pulsar-config}

以下のパラメータは、下流側がPulsarの場合にのみ有効になります。

#### <code>authentication-token</code> {#code-authentication-token-code}

-   Pulsarサーバーでの認証はトークンを使用して行われます。トークンの値を指定してください。

#### <code>token-from-file</code> {#code-token-from-file-code}

-   Pulsarサーバー認証にトークンを使用する場合は、トークンが格納されているファイルのパスを指定してください。

#### <code>basic-user-name</code> {#code-basic-user-name-code}

-   Pulsarは、基本アカウントとパスワードを使用して本人確認を行います。アカウントを指定してください。

#### <code>basic-password</code> {#code-basic-password-code}

-   Pulsarは、基本アカウントとパスワードを使用して本人確認を行います。パスワードを指定してください。

#### <code>auth-tls-certificate-path</code> {#code-auth-tls-certificate-path-code}

-   Pulsar TLS暗号化認証に使用する証明書のパスを指定します。

#### <code>auth-tls-private-key-path</code> {#code-auth-tls-private-key-path-code}

-   Pulsar TLS暗号化認証用の秘密鍵のパスを指定します。

#### <code>tls-trust-certs-file-path</code> {#code-tls-trust-certs-file-path-code}

-   Pulsar TLS暗号化認証で使用される信頼済み証明書ファイルへのパスを指定します。

#### <code>oauth2.oauth2-issuer-url</code> {#code-oauth2-oauth2-issuer-url-code}

-   Pulsar oauth2 発行者 URL。
-   詳細については、 [Pulsarのドキュメントウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)を参照してください。

#### <code>oauth2.oauth2-audience</code> {#code-oauth2-oauth2-audience-code}

-   Pulsar OAuth2 オーディエンス。
-   詳細については、 [Pulsarのウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)をご覧ください。

#### <code>oauth2.oauth2-private-key</code> {#code-oauth2-oauth2-private-key-code}

-   Pulsar oauth2 プライベートキー。
-   詳細については、 [Pulsarのウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)をご覧ください。

#### <code>oauth2.oauth2-client-id</code> {#code-oauth2-oauth2-client-id-code}

-   Pulsar oauth2 クライアントID
-   詳細については、 [Pulsarのウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)をご覧ください。

#### <code>oauth2.oauth2-scope</code> {#code-oauth2-oauth2-scope-code}

-   Pulsar oauth2 oauth2-scope。
-   詳細については、 [Pulsarのウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)をご覧ください。

#### <code>pulsar-producer-cache-size</code> {#code-pulsar-producer-cache-size-code}

-   TiCDCでキャッシュされるPulsarプロデューサーの数を指定します。各Pulsarプロデューサーは1つのトピックに対応します。レプリケートする必要のあるトピックの数がデフォルト値よりも多い場合は、数を増やす必要があります。
-   デフォルト値: `10240`

#### <code>compression-type</code> {#code-compression-type-code}

-   パルサーデータ圧縮方式。
-   デフォルト値： `""` 。これは圧縮が使用されないことを意味します。
-   値のオプション: `"lz4"` 、 `"zlib"` 、 `"zstd"`

#### <code>connection-timeout</code> {#code-connection-timeout-code}

-   PulsarクライアントがサーバーとのTCP接続を確立するためのタイムアウト時間。
-   デフォルト値: `5` (秒)

#### <code>operation-timeout</code> {#code-operation-timeout-code}

-   Pulsarクライアントがトピックの作成や購読などの操作を開始するためのタイムアウト時間。
-   デフォルト値: `30` (秒)

#### <code>batching-max-messages</code> {#code-batching-max-messages-code}

-   Pulsarプロデューサーが1回のバッチで送信できるメッセージの最大数。
-   デフォルト値: `1000`

#### <code>batching-max-publish-delay</code> {#code-batching-max-publish-delay-code}

-   Pulsarプロデューサーメッセージがバッチ処理のために保存される間隔。
-   デフォルト値: `10` (ミリ秒)

#### <code>send-timeout</code> {#code-send-timeout-code}

-   Pulsarプロデューサーがメッセージを送信するまでのタイムアウト時間。
-   デフォルト値: `30` (秒)

#### <code>output-raw-change-event</code> {#code-output-raw-change-event-code}

-   元のデータ変更イベントを出力するかどうかを制御します。詳細については、 [プライマリキーまたはユニークキーの`UPDATE`イベントを分割するかどうかを制御します](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events)参照してください。
-   デフォルト値: `false`

### sink.cloud-storage-config {#sink-cloud-storage-config}

#### <code>worker-count</code> {#code-worker-count-code}

-   ダウンストリームのクラウドstorageの同時実行性が変更されます。
-   デフォルト値: `16`

#### <code>flush-interval</code> {#code-flush-interval-code}

-   下流のクラウドstorageにデータを保存する間隔が変更されます。
-   デフォルト値: `"2s"`

#### <code>file-size</code> {#code-file-size-code}

-   このファイルのバイト数`file-size`を超えると、データ変更ファイルがクラウドstorageに保存されます。
-   デフォルト値： `67108864` 、つまり64MiB

#### <code>file-expiration-days</code> {#code-file-expiration-days-code}

-   ファイルを保持する期間。これは、 `date-separator`が`day`に設定されている場合にのみ有効になります。
-   デフォルト値： `0` 。これは、ファイルクリーンアップが無効になっていることを意味します。
-   `file-expiration-days = 1`と`file-cleanup-cron-spec = "0 0 0 * * *"`を仮定すると、TiCDC は 24 時間を超えて保存されたファイルに対して、毎日 00:00:00 にクリーンアップを実行します。たとえば、2023/12/02 の 00:00:00 に、TiCDC は 2023/12/01 より前に生成されたファイルをクリーンアップしますが、2023/12/01 に生成されたファイルは影響を受けません。

#### <code>file-cleanup-cron-spec</code> {#code-file-cleanup-cron-spec-code}

-   crontabの設定に対応した、スケジュールされたクリーンアップタスクの実行サイクル。
-   フォーマットは`<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`です
-   デフォルト値： `"0 0 2 * * *"` 。これは、クリーンアップタスクが毎日午前2時に実行されることを意味します。

#### <code>flush-concurrency</code> {#code-flush-concurrency-code}

-   単一ファイルのアップロードにおける同時実行数。
-   デフォルト値： `1` 。これは同時実行が無効になっていることを意味します。

#### <code>output-raw-change-event</code> {#code-output-raw-change-event-code}

-   元のデータ変更イベントを出力するかどうかを制御します。詳細については、 [プライマリキーまたはユニークキーの`UPDATE`イベントを分割するかどうかを制御します](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events)参照してください。
-   デフォルト値: `false`
