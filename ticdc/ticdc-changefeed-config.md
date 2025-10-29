---
title: CLI and Configuration Parameters of TiCDC Changefeeds
summary: TiCDC 変更フィードの CLI と構成パラメータの定義について学習します。
---

# TiCDC 変更フィードの CLI とコンフィグレーションパラメータ {#cli-and-configuration-parameters-of-ticdc-changefeeds}

## Changefeed CLI パラメータ {#changefeed-cli-parameters}

このセクションでは、レプリケーション (changefeed) タスクを作成する方法を示しながら、TiCDC changefeed のコマンドライン パラメータを紹介します。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2025-08-14T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.5.3"}
```

-   `--changefeed-id` : レプリケーションタスクのID。形式は正規表現`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`に一致する必要があります。このIDが指定されていない場合、TiCDCは自動的にUUID（バージョン4形式）をIDとして生成します。

-   `--sink-uri` : レプリケーションタスクのダウンストリームアドレス`--sink-uri`以下の形式で設定してください。現在、このスキームは`mysql` 、 `tidb` 、 `kafka`をサポートしています。

        [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]

    シンク URI パラメータに`! * ' ( ) ; : @ & = + $ , / ? % # [ ]`などの特殊文字が含まれている場合は、 [URIエンコーダ](https://www.urlencoder.org/)のように特殊文字をエスケープする必要があります。

-   `--start-ts` : チェンジフィードの開始TSOを指定します。このTSOから、TiCDCクラスターはデータのプルを開始します。デフォルト値は現在時刻です。

-   `--target-ts` : チェンジフィードの終了TSOを指定します。このTSOまで、TiCDCクラスターはデータのプルを停止します。デフォルト値は空で、TiCDCはデータのプルを自動的に停止しません。

-   `--config` : changefeed の構成ファイルを指定します。

## Changefeed 設定パラメータ {#changefeed-configuration-parameters}

このセクションでは、レプリケーション タスクの構成について説明します。

### <code>memory-quota</code> {#code-memory-quota-code}

-   シンクマネージャーがキャプチャサーバーで使用できるメモリクォータ（バイト単位）を指定します。この値を超えた場合、過剰に使用された部分はGoランタイムによってリサイクルされます。
-   デフォルト値: `1073741824` (1 GiB)

### <code>case-sensitive</code> {#code-case-sensitive-code}

-   設定ファイル内のデータベース名とテーブルで大文字と小文字を区別するかどうかを指定します。v6.5.6、v7.1.3、v7.5.0以降では、デフォルト値は`true`から`false`に変更されます。
-   この構成項目は、フィルターとシンクに関連する構成に影響します。
-   デフォルト値: `false`

### <code>force-replicate</code> {#code-force-replicate-code}

-   強制的に[有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)するかどうかを指定します。
-   デフォルト値: `false`

### <code>enable-sync-point</code><span class="version-mark">バージョン 6.3.0 の新機能</span> {#code-enable-sync-point-code-span-class-version-mark-new-in-v6-3-0-span}

-   バージョン 6.3.0 以降でサポートされ、デフォルトでは無効になっている Syncpoint 機能を有効にするかどうかを指定します。
-   v6.4.0 以降では、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`権限を持つ changefeed のみが TiCDC Syncpoint 機能を使用できます。
-   この構成項目は、ダウンストリームが TiDB の場合にのみ有効になります。
-   デフォルト値: `false`

### <code>sync-point-interval</code> {#code-sync-point-interval-code}

-   Syncpoint が上流スナップショットと下流スナップショットを調整する間隔を指定します。
-   この構成項目は、ダウンストリームが TiDB の場合にのみ有効になります。
-   形式は`"h m s"`です。たとえば、 `"1h30m30s"` 。
-   デフォルト値: `"10m"`
-   最小値: `"30s"`

### <code>sync-point-retention</code> {#code-sync-point-retention-code}

-   下流テーブルにおける同期ポイントによるデータの保持期間を指定します。この期間を超過すると、データはクリーンアップされます。
-   この構成項目は、ダウンストリームが TiDB の場合にのみ有効になります。
-   形式は`"h m s"`です。たとえば、 `"24h30m30s"` 。
-   デフォルト値: `"24h"`

### <code>sql-mode</code> <span class="version-mark">v6.5.6、v7.1.3、v7.5.0 の新機能</span> {#code-sql-mode-code-span-class-version-mark-new-in-v6-5-6-v7-1-3-and-v7-5-0-span}

-   DDL文を解析する際に使用する[SQLモード](/sql-mode.md)指定します。複数のモードはカンマで区切られます。
-   デフォルト値: `"ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"` 、これは TiDB のデフォルトの SQL モードと同じです。

### <code>bdr-mode</code> {#code-bdr-mode-code}

-   TiCDCを使用してBDR（双方向レプリケーション）クラスターをセットアップするには、このパラメータを`true`に変更し、TiDBクラスターをBDRモードに設定します。詳細については、 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md#bidirectional-replication)参照してください。
-   デフォルト値: `false` 、双方向レプリケーション (BDR) モードが有効になっていないことを示します

### <code>changefeed-error-stuck-duration</code> {#code-changefeed-error-stuck-duration-code}

-   内部エラーまたは例外が発生したときに、変更フィードが自動的に再試行できる期間を指定します。
-   変更フィードで内部エラーまたは例外が発生し、このパラメータで設定された期間よりも長く継続すると、変更フィードは失敗状態になります。
-   変更フィードが失敗した状態の場合、回復のために変更フィードを手動で再起動する必要があります。
-   形式は`"h m s"`です。たとえば、 `"1h30m30s"` 。
-   デフォルト値: `"30m"`

### マウンター {#mounter}

#### <code>worker-num</code> {#code-worker-num-code}

-   マウンタが KV データをデコードするスレッドの数を指定します。
-   デフォルト値: `16`

### フィルター {#filter}

#### <code>ignore-txn-start-ts</code> {#code-ignore-txn-start-ts-code}

-   指定された start_ts のトランザクションを無視します。

<!-- Example: `[1, 2]` -->

#### <code>rules</code> {#code-rules-code}

-   フィルタルールを指定します。詳細については、 [構文](/table-filter.md#syntax)参照してください。

<!-- Example: `['*.*', '!test.*']` -->

#### filter.イベントフィルター {#filter-event-filters}

詳細については[イベントフィルタールール](/ticdc/ticdc-filter.md#event-filter-rules)参照してください。

##### <code>matcher</code> {#code-matcher-code}

-   `matcher`許可リストです。2 `matcher = ["test.worker"]`このルールが`test`データベース内の`worker`テーブルにのみ適用されることを意味します。

##### <code>ignore-event</code> {#code-ignore-event-code}

-   `ignore-event = ["insert"]` `INSERT`イベントを無視します。
-   `ignore-event = ["drop table", "delete"]` 、 `DROP TABLE` DDL イベントと`DELETE` DML イベントを無視します。TiDB でクラスター化インデックス列の値が更新されると、TiCDC は`UPDATE`イベントを`DELETE`つと`INSERT`イベントに分割することに注意してください。TiCDC はこれらのイベントを`UPDATE`イベントとして識別できないため、正しくフィルタリングできません。

##### <code>ignore-sql</code> {#code-ignore-sql-code}

-   `ignore-sql = ["^drop", "add column"]` `DROP`で始まるか`ADD COLUMN`含む DDL を無視します。

##### <code>ignore-delete-value-expr</code> {#code-ignore-delete-value-expr-code}

-   `ignore-delete-value-expr = "name = 'john'"`条件`name = 'john'`含む`DELETE` DML を無視します。

##### <code>ignore-insert-value-expr</code> {#code-ignore-insert-value-expr-code}

-   `ignore-insert-value-expr = "id >= 100"`条件`id >= 100`含む`INSERT` DMLを無視します

##### <code>ignore-update-old-value-expr</code> {#code-ignore-update-old-value-expr-code}

-   `ignore-update-old-value-expr = "age < 18"`古い値に`age < 18`含まれる`UPDATE` DMLを無視します。

##### <code>ignore-update-new-value-expr</code> {#code-ignore-update-new-value-expr-code}

-   `ignore-update-new-value-expr = "gender = 'male'"`新しい値に`gender = 'male'`含まれる`UPDATE` DMLを無視します。

### スケジューラ {#scheduler}

#### <code>enable-table-across-nodes</code> {#code-enable-table-across-nodes-code}

-   リージョンごとにレプリケーションを行うために、テーブルを複数の TiCDC ノードに割り当てます。

-   この構成項目は Kafka 変更フィードにのみ影響し、MySQL 変更フィードではサポートされません。

-   `enable-table-across-nodes`が有効な場合、割り当てモードは 2 つあります。

    1.  リージョン数に基づいてテーブルを割り当てます。これにより、各TiCDCノードはほぼ同数のリージョンを処理します。テーブルのリージョン数が[`region-threshold`](#region-threshold)を超える場合、テーブルはレプリケーションのために複数のノードに割り当てられます。デフォルト値は`region-threshold`ですが、現在は`100000`です。
    2.  書き込みトラフィックに基づいてテーブルを割り当て、各TiCDCノードがほぼ同数の変更行を処理できるようにします。この割り当ては、テーブル内の1分あたりの変更行数が[`write-key-threshold`](#write-key-threshold)を超えた場合にのみ有効になります。

    2つのモードのうち1つだけを設定する必要があります。1と`region-threshold` `write-key-threshold`両方が設定されている場合、TiCDCはトラフィック割り当てモード（つまり`write-key-threshold`を優先します。

-   デフォルトの値は`false`です。この機能を有効にするには`true`に設定してください。

-   デフォルト値: `false`

#### <code>region-threshold</code> {#code-region-threshold-code}

-   デフォルト値: `100000`

#### <code>write-key-threshold</code> {#code-write-key-threshold-code}

-   デフォルト値: `0` 、これはトラフィック割り当てモードがデフォルトでは使用されないことを意味します

### シンク {#sink}

<!-- MQ sink configuration items -->

#### <code>dispatchers</code> {#code-dispatchers-code}

-   MQ タイプのシンクの場合、ディスパッチャーを使用してイベント ディスパッチャーを構成できます。
-   v6.1.0 以降、TiDB はパーティションとトピックの 2 種類のイベント ディスパッチャーをサポートしています。
-   マッチャーの一致構文は、フィルター ルール構文と同じです。
-   この構成項目は、ダウンストリームが MQ の場合にのみ有効になります。
-   下流のMQがPulsarの場合、 `partition`のルーティングルール`index-value` `ts` `default`いずれにも指定されていない場合、各Pulsarメッセージはキーとして設定した文字列を使用してルーティングされます。例えば、あるマッチャーのルーティングルールを文字列`code`に`table`すると、そのマッチャーに一致するすべてのPulsarメッセージは`code`をキーとしてルーティングされます。

#### <code>column-selectors</code> <span class="version-mark">v7.5.0 の新機能</span> {#code-column-selectors-code-span-class-version-mark-new-in-v7-5-0-span}

-   レプリケーションする特定の列を選択します。これは、ダウンストリームがKafkaの場合にのみ有効です。

#### <code>protocol</code> {#code-protocol-code}

-   メッセージのエンコードに使用するプロトコル形式を指定します。
-   この構成項目は、ダウンストリームが Kafka、Pulsar、またはstorageサービスの場合にのみ有効になります。
-   ダウンストリームが Kafka の場合、プロトコルは canal-json、avro、debezium、open-protocol、または simple になります。
-   ダウンストリームが Pulsar の場合、プロトコルは canal-json のみになります。
-   ダウンストリームがstorageサービスの場合、プロトコルは canal-json または csv のみになります。

<!-- Example: `"canal-json"` -->

#### <code>delete-only-output-handle-key-columns</code><span class="version-mark">バージョン7.2.0の新機能</span> {#code-delete-only-output-handle-key-columns-code-span-class-version-mark-new-in-v7-2-0-span}

-   DELETEイベントの出力を指定します。このパラメータは、canal-jsonおよびopen-protocolプロトコルでのみ有効です。
-   このパラメータは`force-replicate`と互換性がありません。このパラメータと`force-replicate`両方が`true`に設定されている場合、TiCDC は変更フィードの作成時にエラーを報告します。
-   Avro プロトコルはこのパラメータによって制御されず、常に主キー列または一意のインデックス列のみを出力します。
-   CSV プロトコルはこのパラメータによって制御されず、常にすべての列を出力します。
-   デフォルト値: `false` 、すべての列を出力することを意味します
-   `true`に設定すると、主キー列または一意のインデックス列のみが出力されます。

#### <code>schema-registry</code> {#code-schema-registry-code}

-   スキーマ レジストリ URL を指定します。
-   この構成項目は、ダウンストリームが MQ の場合にのみ有効になります。

<!-- Example: `"http://localhost:80801/subjects/{subject-name}/versions/{version-number}/schema"` -->

#### <code>encoder-concurrency</code> {#code-encoder-concurrency-code}

-   データをエンコードするときに使用するエンコーダー スレッドの数を指定します。
-   この構成項目は、ダウンストリームが MQ の場合にのみ有効になります。
-   デフォルト値: `32`

#### <code>enable-kafka-sink-v2</code> {#code-enable-kafka-sink-v2-code}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   kafka-go シンク ライブラリを使用する kafka-sink-v2 を有効にするかどうかを指定します。
-   この構成項目は、ダウンストリームが MQ の場合にのみ有効になります。
-   デフォルト値: `false`

#### <code>only-output-updated-columns</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-only-output-updated-columns-code-span-class-version-mark-new-in-v7-1-0-span}

-   更新された列のみを出力するかどうかを指定します。
-   この構成項目は、open-protocol と canal-json を使用する MQ ダウンストリームにのみ適用されます。
-   デフォルト値: `false`

<!-- Storage sink configuration items -->

#### <code>terminator</code> {#code-terminator-code}

-   この構成項目は、データをstorageシンクに複製する場合にのみ使用され、データを MQ または MySQL シンクに複製する場合は無視できます。
-   2 つのデータ変更イベントを区切るために使用される行ターミネータを指定します。
-   デフォルト値: `""` 、つまり`\r\n`が使用される

#### <code>date-separator</code> {#code-date-separator-code}

-   ファイルディレクトリで使用する日付区切り文字の種類を指定します。詳細については、 [データ変更記録](/ticdc/ticdc-sink-to-cloud-storage.md#data-change-records)参照してください。
-   この構成項目は、ダウンストリームがstorageサービスの場合にのみ有効になります。
-   デフォルト値: `day` 、これはファイルを日ごとに分けることを意味します
-   `month` `year` `day` : `none`

#### <code>enable-partition-separator</code> {#code-enable-partition-separator-code}

-   パーティションを区切り文字列として使用するかどうかを制御します。
-   この構成項目は、ダウンストリームがstorageサービスの場合にのみ有効になります。
-   デフォルト値: `true` 、テーブル内のパーティションが別々のディレクトリに保存されることを意味します
-   この設定は将来のバージョンでは非推奨となり、強制的に`true`に設定されます。下流のパーティションテーブルでのデータ損失を防ぐため、この設定はデフォルト値のままにしておくことをお勧めします。詳細については[問題 #11979](https://github.com/pingcap/tiflow/issues/11979)参照してください。使用例については[データ変更記録](/ticdc/ticdc-sink-to-cloud-storage.md#data-change-records)参照してください。

#### <code>debezium-disable-schema</code> {#code-debezium-disable-schema-code}

-   スキーマ情報の出力を無効にするかどうかを制御します。
-   デフォルト値: `false` 、スキーマ情報の出力を有効にすることを意味します
-   このパラメータは、シンク タイプが MQ で、出力プロトコルが Debezium の場合にのみ有効です。

#### sink.csv<span class="version-mark">バージョン6.5.0の新機能</span> {#sink-csv-span-class-version-mark-new-in-v6-5-0-span}

バージョン6.5.0以降、TiCDCはデータの変更をCSV形式でstorageサービスに保存できるようになりました。MQまたはMySQLシンクにデータをレプリケートする場合は、以下の設定を無視してください。

##### <code>delimiter</code> {#code-delimiter-code}

-   CSVファイル内のフィールドを区切るために使用される文字を指定します。値はASCII文字である必要があります。
-   デフォルト値: `,`

##### <code>quote</code> {#code-quote-code}

-   CSVファイル内のフィールドを囲むために使用する引用符を指定します。値が空の場合、引用符は使用されません。
-   デフォルト値: `"`

##### <code>null</code> {#code-null-code}

-   CSV 列が NULL の場合に表示される文字を指定します。
-   デフォルト値: `\N`

##### <code>include-commit-ts</code> {#code-include-commit-ts-code}

-   CSV 行にコミット ts を含めるかどうかを制御します。
-   デフォルト値: `false`

##### <code>binary-encoding-method</code> {#code-binary-encoding-method-code}

-   バイナリデータのエンコード方法を指定します。
-   デフォルト値: `base64`
-   `hex`オプション: `base64`

##### <code>output-handle-key</code> {#code-output-handle-key-code}

-   ハンドルキー情報を出力するかどうかを制御します。この設定パラメータは内部実装のみに使用されるため、設定することは推奨されません。
-   デフォルト値: `false`

##### <code>output-old-value</code> {#code-output-old-value-code}

-   行データが変更される前に値を出力するかどうかを制御します。デフォルト値は false です。
-   有効にすると ( `true`に設定)、 `UPDATE`イベントは 2 行のデータを出力します。最初の行は変更前のデータを出力する`DELETE`イベントで、2 番目の行は変更されたデータを出力する`INSERT`イベントです。
-   有効にすると、データ変更のある列の前に列`"is-update"`が追加されます。この追加された列は、現在の行のデータ変更が`UPDATE`番目のイベントによるものか、それとも元の`INSERT`または`DELETE`番目のイベントによるものかを識別するために使用されます。現在の行のデータ変更が`UPDATE`番目のイベントによるものかを判断するために、列`"is-update"`の値は`true`になります。それ以外の場合は、列`false`になります。
-   デフォルト値: `false`

TiCDCはv8.0.0以降、シンプルメッセージエンコーディングプロトコルをサポートしています。シンプルプロトコルの設定パラメータは以下のとおりです。プロトコルの詳細については、 [TiCDCシンプルプロトコル](/ticdc/ticdc-simple-protocol.md)参照してください。

次の構成パラメータは、ブートストラップ メッセージの送信動作を制御します。

#### <code>send-bootstrap-interval-in-sec</code> {#code-send-bootstrap-interval-in-sec-code}

-   ブートストラップ メッセージを送信する時間間隔を秒単位で制御します。
-   デフォルト値: `120` 、これは各テーブルに対して120秒ごとにブートストラップメッセージが送信されることを意味します。
-   単位: 秒

#### <code>send-bootstrap-in-msg-count</code> {#code-send-bootstrap-in-msg-count-code}

-   ブートストラップを送信するためのメッセージ間隔をメッセージ数で制御します。
-   デフォルト値: `10000` 。これは、各テーブルで 10000 行の変更メッセージごとにブートストラップ メッセージが送信されることを意味します。
-   ブートストラップ メッセージの送信を無効にする場合は、 [`send-bootstrap-interval-in-sec`](#send-bootstrap-interval-in-sec)と`send-bootstrap-in-msg-count`両方を`0`に設定します。

#### <code>send-bootstrap-to-all-partition</code> {#code-send-bootstrap-to-all-partition-code}

-   すべてのパーティションにブートストラップ メッセージを送信するかどうかを制御します。
-   `false`に設定すると、ブートストラップ メッセージは対応するテーブル トピックの最初のパーティションにのみ送信されます。
-   デフォルト値: `true` 、これは、対応するテーブルトピックのすべてのパーティションにブートストラップメッセージが送信されることを意味します。

#### sink.kafka-config.codec-config {#sink-kafka-config-codec-config}

##### <code>encoding-format</code> {#code-encoding-format-code}

-   シンプルプロトコルメッセージのエンコード形式を制御します。現在、シンプルプロトコルメッセージはエンコード形式`json`と`avro`サポートしています。
-   デフォルト値: `json`
-   値`avro`オプション: `json`

#### シンク.オープン {#sink-open}

##### <code>output-old-value</code> {#code-output-old-value-code}

-   行データが変更される前に値を出力するかどうかを制御します。デフォルト値はtrueです。無効にすると、 `UPDATE`イベントは「p」フィールドを出力しません。
-   デフォルト値: `true`

#### sink.debezium {#sink-debezium}

##### <code>output-old-value</code> {#code-output-old-value-code}

-   行データが変更される前の値を出力するかどうかを制御します。デフォルト値はtrueです。無効にすると、 `UPDATE`イベントは「before」フィールドを出力しません。
-   デフォルト値: `true`

### 一貫性のある {#consistent}

REDOログを使用する場合の変更フィードのレプリケーション整合性設定を指定します。詳細については、 [災害シナリオにおける結果整合性のあるレプリケーション](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)参照してください。

注意: 一貫性関連の構成項目は、ダウンストリームがデータベースであり、REDO ログ機能が有効になっている場合にのみ有効になります。

#### <code>level</code> {#code-level-code}

-   データ整合性レベル`"none"`は、REDO ログが無効であることを意味します。
-   デフォルト値: `"none"`
-   値`"eventual"`オプション: `"none"`

#### <code>max-log-size</code> {#code-max-log-size-code}

-   最大REDOログサイズ。
-   デフォルト値: `64`
-   単位: MiB

#### <code>flush-interval</code> {#code-flush-interval-code}

-   REDO ログのフラッシュ間隔。
-   デフォルト値: `2000`
-   単位: ミリ秒

#### <code>storage</code> {#code-storage-code}

-   再実行ログのstorageURI。
-   デフォルト値: `""`

#### <code>use-file-backend</code> {#code-use-file-backend-code}

-   再実行ログをローカル ファイルに保存するかどうかを指定します。
-   デフォルト値: `false`

#### <code>encoding-worker-num</code> {#code-encoding-worker-num-code}

-   再実行モジュール内のエンコードおよびデコード ワーカーの数。
-   デフォルト値: `16`

#### <code>flush-worker-num</code> {#code-flush-worker-num-code}

-   再実行モジュール内のフラッシュワーカーの数。
-   デフォルト値: `8`

#### <code>compression</code> <span class="version-mark">v6.5.6、v7.1.3、v7.5.1、v7.6.0 の新機能</span> {#code-compression-code-span-class-version-mark-new-in-v6-5-6-v7-1-3-v7-5-1-and-v7-6-0-span}

-   REDO ログ ファイルを圧縮する動作。
-   デフォルト値: `""` （圧縮なし）
-   値`"lz4"`オプション: `""`

#### <code>flush-concurrency</code> <span class="version-mark">v6.5.6、v7.1.3、v7.5.1、v7.6.0 の新機能</span> {#code-flush-concurrency-code-span-class-version-mark-new-in-v6-5-6-v7-1-3-v7-5-1-and-v7-6-0-span}

-   単一の REDO ファイルをアップロードするための同時実行性。
-   デフォルト値: `1` 、同時実行が無効であることを意味します

### 誠実さ {#integrity}

#### <code>integrity-check-level</code> {#code-integrity-check-level-code}

-   単一行データのチェックサム検証を有効にするかどうかを制御します。
-   デフォルト値: `"none"` 、これは機能を無効にすることを意味します
-   値`"correctness"`オプション: `"none"`

#### <code>corruption-handle-level</code> {#code-corruption-handle-level-code}

-   単一行データのチェックサム検証が失敗した場合の変更フィードのログ レベルを指定します。
-   デフォルト値: `"warn"`
-   値`"error"`オプション: `"warn"`

### sink.kafka-config {#sink-kafka-config}

以下の設定項目は、ダウンストリームが Kafka の場合にのみ有効になります。

#### <code>sasl-mechanism</code> {#code-sasl-mechanism-code}

-   Kafka SASL 認証のメカニズムを指定します。
-   デフォルト値: `""` 、SASL認証が使用されないことを示します

<!-- Example: `OAUTHBEARER` -->

#### <code>sasl-oauth-client-id</code> {#code-sasl-oauth-client-id-code}

-   Kafka SASL OAUTHBEARER認証におけるクライアントIDを指定します。このパラメータは、OAUTHBEARER認証を使用する場合に必須です。
-   デフォルト値: `""`

#### <code>sasl-oauth-client-secret</code> {#code-sasl-oauth-client-secret-code}

-   Kafka SASL OAUTHBEARER認証におけるクライアントシークレットを指定します。このパラメータは、OAUTHBEARER認証を使用する場合に必須です。
-   デフォルト値: `""`

#### <code>sasl-oauth-token-url</code> {#code-sasl-oauth-token-url-code}

-   トークンを取得するためのKafka SASL OAUTHBEARER認証のtoken-urlを指定します。このパラメータは、OAUTHBEARER認証を使用する場合に必須です。
-   デフォルト値: `""`

#### <code>sasl-oauth-scopes</code> {#code-sasl-oauth-scopes-code}

-   Kafka SASL OAUTHBEARER認証のスコープを指定します。OAUTHBEARER認証を使用する場合、このパラメータはオプションです。
-   デフォルト値: `""`

#### <code>sasl-oauth-grant-type</code> {#code-sasl-oauth-grant-type-code}

-   Kafka SASL OAUTHBEARER認証における付与タイプを指定します。OAUTHBEARER認証を使用する場合、このパラメータはオプションです。
-   デフォルト値: `"client_credentials"`

#### <code>sasl-oauth-audience</code> {#code-sasl-oauth-audience-code}

-   Kafka SASL OAUTHBEARER認証におけるオーディエンスを指定します。OAUTHBEARER認証を使用する場合、このパラメータはオプションです。
-   デフォルト値: `""`

<!-- Example: `"kafka"` -->

#### <code>output-raw-change-event</code> {#code-output-raw-change-event-code}

-   元のデータ変更イベントを出力するかどうかを制御します。詳細については、 [主キーまたは一意キーの`UPDATE`イベントを分割するかどうかを制御する](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events)参照してください。
-   デフォルト値: `false`

### sink.kafka-config.glue-schema-registry-config {#sink-kafka-config-glue-schema-registry-config}

次の設定は、プロトコルとして Avro を使用し、AWS Glue スキーマレジストリを使用する場合にのみ必要です。

```toml
region="us-west-1"
registry-name="ticdc-test"
access-key="xxxx"
secret-access-key="xxxx"
token="xxxx"
```

詳細については[TiCDC を AWS Glue スキーマレジストリと統合する](/ticdc/ticdc-sink-to-kafka.md#integrate-ticdc-with-aws-glue-schema-registry)参照してください。

### sink.pulsar-config {#sink-pulsar-config}

以下のパラメータは、ダウンストリームが Pulsar の場合にのみ有効になります。

#### <code>authentication-token</code> {#code-authentication-token-code}

-   Pulsarサーバーでの認証はトークンを使用して行われます。トークンの値を指定してください。

#### <code>token-from-file</code> {#code-token-from-file-code}

-   Pulsarサーバー認証にトークンを使用する場合は、トークンが配置されているファイルへのパスを指定します。

#### <code>basic-user-name</code> {#code-basic-user-name-code}

-   Pulsarは基本アカウントとパスワードを使用して本人認証を行います。アカウントを指定してください。

#### <code>basic-password</code> {#code-basic-password-code}

-   Pulsarは基本アカウントとパスワードを使用して本人認証を行います。パスワードを指定してください。

#### <code>auth-tls-certificate-path</code> {#code-auth-tls-certificate-path-code}

-   Pulsar TLS 暗号化認証の証明書パスを指定します。

#### <code>auth-tls-private-key-path</code> {#code-auth-tls-private-key-path-code}

-   Pulsar TLS 暗号化認証の秘密鍵パスを指定します。

#### <code>tls-trust-certs-file-path</code> {#code-tls-trust-certs-file-path-code}

-   Pulsar TLS 暗号化認証の信頼できる証明書ファイルへのパスを指定します。

#### <code>oauth2.oauth2-issuer-url</code> {#code-oauth2-oauth2-issuer-url-code}

-   Pulsar oauth2 発行者 URL。
-   詳細については[Pulsarドキュメントウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)参照してください。

#### <code>oauth2.oauth2-audience</code> {#code-oauth2-oauth2-audience-code}

-   Pulsar oauth2 オーディエンス。
-   詳細については、 [パルサーのウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)参照してください。

#### <code>oauth2.oauth2-private-key</code> {#code-oauth2-oauth2-private-key-code}

-   Pulsar oauth2 秘密鍵。
-   詳細については、 [パルサーのウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)参照してください。

#### <code>oauth2.oauth2-client-id</code> {#code-oauth2-oauth2-client-id-code}

-   Pulsar oauth2 クライアントID
-   詳細については、 [パルサーのウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)参照してください。

#### <code>oauth2.oauth2-scope</code> {#code-oauth2-oauth2-scope-code}

-   Pulsar oauth2 oauth2 スコープ。
-   詳細については、 [パルサーのウェブサイト](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication)参照してください。

#### <code>pulsar-producer-cache-size</code> {#code-pulsar-producer-cache-size-code}

-   TiCDC にキャッシュされる Pulsar プロデューサーの数を指定します。各 Pulsar プロデューサーは 1 つのトピックに対応します。複製する必要があるトピックの数がデフォルト値より多い場合は、この数を増やす必要があります。
-   デフォルト値: `10240`

#### <code>compression-type</code> {#code-compression-type-code}

-   Pulsar データ圧縮方式。
-   デフォルト値: `""` 、圧縮は使用されないことを意味します
-   `"zstd"` `"zlib"`オプション: `"lz4"`

#### <code>connection-timeout</code> {#code-connection-timeout-code}

-   Pulsar クライアントがサーバーとの TCP 接続を確立するまでのタイムアウト。
-   デフォルト値: `5` (秒)

#### <code>operation-timeout</code> {#code-operation-timeout-code}

-   Pulsar クライアントがトピックの作成やサブスクライブなどの操作を開始するまでのタイムアウト。
-   デフォルト値: `30` (秒)

#### <code>batching-max-messages</code> {#code-batching-max-messages-code}

-   Pulsar プロデューサーが単一バッチで送信するメッセージの最大数。
-   デフォルト値: `1000`

#### <code>batching-max-publish-delay</code> {#code-batching-max-publish-delay-code}

-   Pulsar プロデューサー メッセージがバッチ処理用に保存される間隔。
-   デフォルト値: `10` (ミリ秒)

#### <code>send-timeout</code> {#code-send-timeout-code}

-   Pulsar プロデューサーがメッセージを送信するまでのタイムアウト。
-   デフォルト値: `30` (秒)

#### <code>output-raw-change-event</code> {#code-output-raw-change-event-code}

-   元のデータ変更イベントを出力するかどうかを制御します。詳細については、 [主キーまたは一意キーの`UPDATE`イベントを分割するかどうかを制御する](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events)参照してください。
-   デフォルト値: `false`

### sink.cloud-storage-config {#sink-cloud-storage-config}

#### <code>worker-count</code> {#code-worker-count-code}

-   ダウンストリームのクラウドstorageにデータ変更を保存するための同時実行。
-   デフォルト値: `16`

#### <code>flush-interval</code> {#code-flush-interval-code}

-   下流のクラウドstorageにデータを保存する間隔が変更されます。
-   デフォルト値: `"2s"`

#### <code>file-size</code> {#code-file-size-code}

-   データ変更ファイルは、このファイル内のバイト数が`file-size`を超えるとクラウドstorageに保存されます。
-   デフォルト値: `67108864` 、つまり 64 MiB

#### <code>file-expiration-days</code> {#code-file-expiration-days-code}

-   ファイルを保持する期間`date-separator`が`day`に設定されている場合にのみ有効になります。
-   デフォルト値: `0` 、ファイルのクリーンアップが無効であることを意味します
-   `file-expiration-days = 1`と`file-cleanup-cron-spec = "0 0 0 * * *"`仮定すると、TiCDCは24時間を超えて保存されたファイルに対して毎日00:00:00にクリーンアップを実行します。例えば、2023年12月2日の00:00:00に、TiCDCは2023年12月1日より前に生成されたファイルをクリーンアップしますが、2023年12月1日に生成されたファイルは影響を受けません。

#### <code>file-cleanup-cron-spec</code> {#code-file-cleanup-cron-spec-code}

-   crontab 構成と互換性のある、スケジュールされたクリーンアップ タスクの実行サイクル。
-   フォーマットは`<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`
-   デフォルト値: `"0 0 2 * * *"` 、これはクリーンアップタスクが毎日午前2時に実行されることを意味します

#### <code>flush-concurrency</code> {#code-flush-concurrency-code}

-   1 つのファイルをアップロードする際の同時実行性。
-   デフォルト値: `1` 、同時実行が無効であることを意味します

#### <code>output-raw-change-event</code> {#code-output-raw-change-event-code}

-   元のデータ変更イベントを出力するかどうかを制御します。詳細については、 [主キーまたは一意キーの`UPDATE`イベントを分割するかどうかを制御する](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events)参照してください。
-   デフォルト値: `false`
