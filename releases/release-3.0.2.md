---
title: TiDB 3.0.2 Release Notes
---

# TiDB3.0.2リリースノート {#tidb-3-0-2-release-notes}

発売日：2019年8月7日

TiDBバージョン：3.0.2

TiDB Ansibleバージョン：3.0.2

## TiDB {#tidb}

-   SQLオプティマイザー
    -   同じテーブルがクエリで複数回発生し、論理的にクエリ結果が常に空である場合に、「スキーマに列が見つかりません」というメッセージが報告される問題を修正します[＃11247](https://github.com/pingcap/tidb/pull/11247)
    -   場合によっては`TIDB_INLJ`ヒントが正しく機能しないためにクエリプランが期待を満たさないという問題を修正します（ `explain select /*+ TIDB_INLJ(t1) */ t1.b, t2.a from t t1, t t2 where t1.b = t2.a`など） [＃11362](https://github.com/pingcap/tidb/pull/11362)
    -   クエリ結果の列名が間違っている場合がある問題を修正します（ `SELECT IF(1,c,c) FROM t`など） [＃11379](https://github.com/pingcap/tidb/pull/11379)
    -   `LIKE`式が暗黙的に0に変換される場合があるため、 `SELECT 0 LIKE 'a string'`などの一部のクエリが`TRUE`を返す問題を修正します[＃11411](https://github.com/pingcap/tidb/pull/11411)
    -   `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')`のような`SHOW`ステートメントの[＃11459](https://github.com/pingcap/tidb/pull/11459)をサポートする
    -   集計関数の関連する列が見つからず、 `outerJoinElimination`の最適化ルールが列エイリアスを正しく処理しないためにエラーが報告される問題を修正します。最適化プロセスでのエイリアス解析を改善して、最適化がより多くのクエリタイプをカバーできるようにします[＃11377](https://github.com/pingcap/tidb/pull/11377)
    -   Window関数で構文制限に違反した場合にエラーが報告されない問題を修正します（たとえば、フレーム定義の最後に`UNBOUNDED PRECEDING`を表示することは許可されていません） [＃11543](https://github.com/pingcap/tidb/pull/11543)
    -   [＃11535](https://github.com/pingcap/tidb/pull/11535)との非互換性を引き起こす`ERROR 3593 (HY000): You cannot use the window function FUNCTION_NAME in this context`エラーメッセージで`FUNCTION_NAME`が大文字であるという問題を修正します。
    -   Window関数で実装されていない`IGNORE NULLS`構文が使用されているが、エラーが報告されないという問題を修正します[＃11593](https://github.com/pingcap/tidb/pull/11593)
    -   オプティマイザーが時間等しい条件を正しく推定しない問題を修正します[＃11512](https://github.com/pingcap/tidb/pull/11512)
    -   フィードバック情報に基づくTop-N統計の更新をサポート[＃11507](https://github.com/pingcap/tidb/pull/11507)
-   SQL実行エンジン
    -   `INSERT`関数のパラメーター[＃11248](https://github.com/pingcap/tidb/pull/11248)に`NULL`が含まれている場合、戻り値が`NULL`にならない問題を修正します。
    -   `ADMIN CHECKSUM`操作[＃11266](https://github.com/pingcap/tidb/pull/11266)でパーティションテーブルをチェックすると、計算結果が間違っている可能性がある問題を修正します。
    -   INDEXJOINがプレフィックスインデックス[＃11246](https://github.com/pingcap/tidb/pull/11246)を使用すると結果が間違っている可能性がある問題を修正します
    -   `DATE_ADD`関数がマイクロ秒[＃11288](https://github.com/pingcap/tidb/pull/11288)を含む日付数で減算を行うときに、分数を誤って整列することによって結果が間違っている可能性があるという問題を修正します。
    -   `DATE_ADD`関数が[＃11325](https://github.com/pingcap/tidb/pull/11325)の負の数を誤って処理することによって引き起こされる誤った結果を修正し`INTERVAL`
    -   `Mod(%)` 、または`Multiple(*)`が0を返し、小数桁の数が多い（ `Minus(-)`など） [＃11251](https://github.com/pingcap/tidb/pull/11251) 、 `Mod(%)` 、または`Multiple(*)`によって返される小数桁の数がMySQLの場合と異なる問題を修正し`Minus(-)` `select 0.000 % 0.11234500000000000000`
    -   `CONCAT`および`CONCAT_WS`関数によって返される結果の長さが[＃11275](https://github.com/pingcap/tidb/pull/11275)を超えると、警告付きの`NULL`が誤って返される問題を修正し`max_allowed_packet` 。
    -   `SUBTIME`および`ADDTIME`関数のパラメーターが無効な場合に警告付きの`NULL`が誤って返される問題を修正します[＃11337](https://github.com/pingcap/tidb/pull/11337)
    -   `CONVERT_TZ`関数のパラメーターが無効な場合に`NULL`が誤って返される問題を修正します[＃11359](https://github.com/pingcap/tidb/pull/11359)
    -   このクエリのメモリ使用量を示すために、 `EXPLAIN ANALYZE`によって返される結果に`MEMORY`列を追加します[＃11418](https://github.com/pingcap/tidb/pull/11418)
    -   [＃11429](https://github.com/pingcap/tidb/pull/11429)の結果に`CARTESIAN`結合を追加し`EXPLAIN`
    -   floatおよびdoubleタイプの自動インクリメント列の誤ったデータを修正します[＃11385](https://github.com/pingcap/tidb/pull/11385)
    -   疑似統計がダンプされたときにいくつかの情報によって引き起こされるパニックの問題を修正し[＃11460](https://github.com/pingcap/tidb/pull/11460) `nil`
    -   定数畳み込みの最適化によって引き起こされる`SELECT … CASE WHEN … ELSE NULL ...`の誤ったクエリ結果を修正します[＃11441](https://github.com/pingcap/tidb/pull/11441)
    -   `floatStrToIntStr`が[＃11473](https://github.com/pingcap/tidb/pull/11473)などの入力を正しく解析しない問題を修正し`+999.9999e2`
    -   `DATE_ADD`および`DATE_SUB`関数の結果がオーバーフローした場合に`NULL`が返されない場合があるという問題を修正します[＃11476](https://github.com/pingcap/tidb/pull/11476)
    -   長い文字列を整数[＃11469](https://github.com/pingcap/tidb/pull/11469)に変換するときに文字列に無効な文字が含まれている場合、変換結果がMySQLの結果と異なる問題を修正します。
    -   この関数の大文字と小文字の区別が原因で、 `REGEXP BINARY`の関数の結果がMySQLと互換性がないという問題を修正します[＃11504](https://github.com/pingcap/tidb/pull/11504)
    -   `GRANT ROLE`ステートメントが`CURRENT_ROLE`を受け取ったときにエラーが報告される問題を修正します。 `REVOKE ROLE`ステートメントが`mysql.default_role`特権を正しく取り消さないという問題を修正します[＃11356](https://github.com/pingcap/tidb/pull/11356)
    -   `SELECT ADDDATE('2008-01-34', -1)`のようなステートメントを実行するときの`Incorrect datetime value`警告情報の表示形式の問題を修正し[＃11447](https://github.com/pingcap/tidb/pull/11447)た
    -   JSONデータのfloatフィールドが整数[＃11534](https://github.com/pingcap/tidb/pull/11534)に変換されたときに結果がオーバーフローした場合、エラーメッセージが`constant … overflows bigint`ではなく`constant … overflows float`を報告する問題を修正します。
    -   `DATE_ADD`関数が`FLOAT` 、および`DOUBLE`列パラメーターを受け取ったときに誤った型変換が原因で結果が間違っている可能性があるという問題を修正し[＃11527](https://github.com/pingcap/tidb/pull/11527) `DECIMAL`
    -   `DATE_ADD`関数[＃11615](https://github.com/pingcap/tidb/pull/11615)のINTERVAL分数の符号を誤って処理することによって引き起こされる誤った結果を修正します。
    -   `Ranger`がプレフィックスインデックス[＃11565](https://github.com/pingcap/tidb/pull/11565)を正しく処理しないために発生したプレフィックスインデックスがインデックスルックアップ結合に含まれている場合の誤ったクエリ結果を修正します。
    -   `NAME_CONST`の2番目のパラメーターが負の数[＃11268](https://github.com/pingcap/tidb/pull/11268)のときに`NAME_CONST`関数が実行されると、「NAME_CONSTへの引数が正しくありません」というメッセージが報告される問題を修正します。
    -   SQLステートメントに現在時刻の計算が含まれ、値が複数回フェッチされる場合、結果がMySQLと互換性がないという問題を修正します。同じSQLステートメントの現在時刻をフェッチするときに同じ値を使用する[＃11394](https://github.com/pingcap/tidb/pull/11394)
    -   `baseExecutor`の`Close`がエラーを報告したときに`Close`が`ChildExecutor`に対して呼び出されない問題を修正します。この問題は、 `KILL`のステートメントが有効にならず、 `ChildExecutor`が閉じられていない場合に、Goroutineリークにつながる可能性があります[＃11576](https://github.com/pingcap/tidb/pull/11576)
-   サーバ
    -   `LOAD DATA`がCSVファイル[＃11250](https://github.com/pingcap/tidb/pull/11250)の欠落している`TIMESTAMP`フィールドを処理するときに、自動追加値が現在のタイムスタンプではなく0になる問題を修正します。
    -   `SHOW CREATE USER`ステートメントが関連する特権を正しくチェックせず、 `SHOW CREATE USER CURRENT_USER()`によって返される`USER`と`HOST`が間違っている可能性があるという問題を修正します[＃11229](https://github.com/pingcap/tidb/pull/11229)
    -   JDBC3で`executeBatch`を使用すると返される結果が間違っている可能性がある問題を修正し[＃11290](https://github.com/pingcap/tidb/pull/11290)
    -   TiKVサーバーのポートを変更するときにストリーミングクライアントのログ情報の印刷を減らす[＃11370](https://github.com/pingcap/tidb/pull/11370)
    -   ストリーミングクライアントをTiKVサーバーに再接続するロジックを最適化して、ストリーミングクライアントが長期間ブロックされないようにします[＃11372](https://github.com/pingcap/tidb/pull/11372)
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS`に`REGION_ID`を[＃11350](https://github.com/pingcap/tidb/pull/11350)
    -   PD APIからリージョン情報を取得するタイムアウト期間をキャンセルして、リージョン数が多い場合のPDタイムアウトが原因で`http://{TiDBIP}:10080/regions/hot`が呼び出されたときにリージョン情報の取得が失敗しないようにします[＃11383](https://github.com/pingcap/tidb/pull/11383)
    -   リージョン関連のリクエストがHTTPAPI1でパーティション化されたテーブル関連のリージョンを返さない問題を修正し[＃11466](https://github.com/pingcap/tidb/pull/11466)
    -   ユーザーがペシミスティックロックを手動で検証するときに、操作が遅いためにロックタイムアウトが発生する可能性を減らすために、次の変更を行います[＃11521](https://github.com/pingcap/tidb/pull/11521) ：
        -   悲観的ロックのデフォルトTTLを30秒から40秒に増やします
        -   最大TTLを60秒から120秒に増やします
        -   最初の`LockKeys`のリクエストから悲観的なロック期間を計算します
    -   TiKVクライアントの`SendRequest`機能ロジックを変更します。接続を構築できないときに待機するのではなく、すぐに別のピアに接続してみてください[＃11531](https://github.com/pingcap/tidb/pull/11531)
    -   リージョンキャッシュの最適化：別のストアが同じアドレスでオンラインになっているときにストアが移動された場合、削除されたストアに無効のラベルを付けて、キャッシュ内のストア情報をできるだけ早く更新します[＃11567](https://github.com/pingcap/tidb/pull/11567)
    -   `http://{TiDB_ADDRESS:TIDB_IP}/mvcc/key/{db}/{table}/{handle}`によって返される結果にリージョンIDを追加し[＃11557](https://github.com/pingcap/tidb/pull/11557)
    -   ScatterTableAPIがRangeキーをエスケープしないためにScatterTableが機能しない問題を修正します[＃11298](https://github.com/pingcap/tidb/pull/11298)
    -   リージョンキャッシュの最適化：コレスポンデントストアにアクセスできない場合、リージョンが存在するストアに無効のラベルを付けて、このストアへのアクセスによるクエリパフォーマンスの低下を回避します[＃11498](https://github.com/pingcap/tidb/pull/11498)
    -   同じ名前のデータベースを複数回ドロップした後でも、HTTPAPIを介してテーブルスキーマを取得できるというエラーを修正します[＃11585](https://github.com/pingcap/tidb/pull/11585)
-   DDL
    -   長さがゼロの非文字列列にインデックスが付けられているときにエラーが発生する問題を修正します[＃11214](https://github.com/pingcap/tidb/pull/11214)
    -   外部キー制約とフルテキストインデックスを使用した列の変更を禁止します（注：TiDBは、構文で外部キー制約とフルテキストインデックスを引き続きサポートします） [＃11274](https://github.com/pingcap/tidb/pull/11274)
    -   `ALTER TABLE`ステートメントによって変更された位置と列のデフォルト値が同時に使用されるために列のインデックスオフセットが間違っている可能性がある問題を修正します[＃11346](https://github.com/pingcap/tidb/pull/11346)
    -   JSONファイルの解析時に発生する2つの問題を修正します。
        -   `int64`は`uint64`の中間解析結果として使用され、精度オーバーフローエラー`ConvertJSONToFloat`につながり[＃11433](https://github.com/pingcap/tidb/pull/11433) 。
        -   `int64`は`uint64`の中間解析結果として使用され、精度オーバーフローエラー`ConvertJSONToInt`につながり[＃11551](https://github.com/pingcap/tidb/pull/11551) 。
    -   自動インクリメント列が誤った結果を取得する可能性を回避するために、自動インクリメント列へのインデックスの削除を禁止します[＃11399](https://github.com/pingcap/tidb/pull/11399)
    -   次の問題を修正します[＃11492](https://github.com/pingcap/tidb/pull/11492) ：
        -   照合順序を明示的に指定する場合、文字セットと列の照合順序は一貫していませんが、文字セットは指定していません
        -   `ALTER TABLE … MODIFY COLUMN`で指定された文字セットと照合順序の間に競合がある場合、エラーは正しく報告されません。
        -   `ALTER TABLE … MODIFY COLUMN`を使用して文字セットと照合を複数回指定する場合のMySQLとの非互換性
    -   サブクエリのトレースの詳細を`TRACE`のクエリの結果に追加します[＃11458](https://github.com/pingcap/tidb/pull/11458)
    -   実行`ADMIN CHECK TABLE`のパフォーマンスを最適化し、実行時間を大幅に短縮します[＃11547](https://github.com/pingcap/tidb/pull/11547)
    -   `SPLIT TABLE … REGIONS/INDEX`によって返された結果を追加し、 `TOTAL_SPLIT_REGION`と`SCATTER_FINISH_RATIO`に、結果[＃11484](https://github.com/pingcap/tidb/pull/11484)でタイムアウトする前に正常に分割されたリージョンの数を表示させます。
    -   `ON UPDATE CURRENT_TIMESTAMP`が列属性であり、float精度が指定されている場合、 `SHOW CREATE TABLE`などのステートメントによって表示される精度が不完全であるという問題を修正します[＃11591](https://github.com/pingcap/tidb/pull/11591)
    -   仮想生成列の式に別の仮想生成列[＃11475](https://github.com/pingcap/tidb/pull/11475)が含まれている場合、列のインデックス結果を正しく計算できない問題を修正します。
    -   `ALTER TABLE … ADD PARTITION …`ステートメント[＃11581](https://github.com/pingcap/tidb/pull/11581)の`VALUE LESS THAN`の後にマイナス記号を追加できない問題を修正します。
-   モニター
    -   `TiKVTxnCmdCounter`モニタリングメトリックが登録されていないためにデータが収集および報告されない問題を修正します[＃11316](https://github.com/pingcap/tidb/pull/11316)
    -   バインド情報`BindMemoryUsage` `BindUsageCounter` `BindTotalGauge`メトリックを追加し[＃11467](https://github.com/pingcap/tidb/pull/11467)

## TiKV {#tikv}

-   Raftログが時間[＃5160](https://github.com/tikv/tikv/pull/5160)に書き込まれない場合にTiKVがパニックになるバグを修正します
-   TiKVパニック後にパニック情報がログファイルに書き込まれないバグを修正します[＃5198](https://github.com/tikv/tikv/pull/5198)
-   悲観的なトランザクションで挿入操作が正しく実行されない可能性があるバグを修正します[＃5203](https://github.com/tikv/tikv/pull/5203)
-   INFO1への手動介入を必要としない一部のログの出力レベルを下げ[＃5193](https://github.com/tikv/tikv/pull/5193)
-   ストレージエンジンのサイズ[＃5200](https://github.com/tikv/tikv/pull/5200)の監視の精度を向上させる
-   tikv-ctl1のリージョンサイズの精度を向上させ[＃5195](https://github.com/tikv/tikv/pull/5195)
-   悲観的ロックのデッドロック検出器のパフォーマンスを向上させる[＃5192](https://github.com/tikv/tikv/pull/5192)
-   TitanストレージエンジンのGCのパフォーマンスを向上させる[＃5197](https://github.com/tikv/tikv/pull/5197)

## PD {#pd}

-   スキャッターリージョンスケジューラが機能しないバグを修正します[＃1642](https://github.com/pingcap/pd/pull/1642)
-   pd- [＃1653](https://github.com/pingcap/pd/pull/1653)でリージョンのマージ操作を実行できないバグを修正します。
-   pd- [＃1651](https://github.com/pingcap/pd/pull/1651)でtombstoneの削除操作を実行できないバグを修正します。
-   領域のスキャン操作を実行すると、キースコープと重複する領域が見つからない問題を修正します[＃1648](https://github.com/pingcap/pd/pull/1648)
-   再試行メカニズムを追加して、メンバーがPD1に正常に追加されていることを確認し[＃1643](https://github.com/pingcap/pd/pull/1643)

## ツール {#tools}

TiDB Binlog

-   起動時に構成アイテムチェック機能を追加します。これにより、Binlogサービスが停止し、無効なアイテムが見つかったときにエラーが報告されます[＃687](https://github.com/pingcap/tidb-binlog/pull/687)
-   Drainerに`node-id`の構成を追加して、Drainer3で使用される特定のロジックを指定し[＃684](https://github.com/pingcap/tidb-binlog/pull/684)

TiDB Lightning

-   2つのチェックサムが同時に実行されているときに`tikv_gc_life_time`が元の値に戻らないという問題を修正します[＃218](https://github.com/pingcap/tidb-lightning/pull/218)
-   起動時に構成アイテムチェック機能を追加します。これにより、Binlogサービスが停止し、無効なアイテムが見つかったときにエラーが報告されます[＃217](https://github.com/pingcap/tidb-lightning/pull/217)

## TiDB Ansible {#tidb-ansible}

-   ディスクパフォーマンスモニターが秒をミリ秒として処理するユニットエラーを修正します[＃840](https://github.com/pingcap/tidb-ansible/pull/840)
-   Spark3に`log4j`の構成ファイルを追加し[＃841](https://github.com/pingcap/tidb-ansible/pull/841)
-   Binlogが有効で、KafkaまたはZooKeeperが構成されている場合に、Prometheus構成ファイルが間違った形式で生成される問題を修正します[＃844](https://github.com/pingcap/tidb-ansible/pull/844)
-   生成されたTiDB構成ファイル[＃850](https://github.com/pingcap/tidb-ansible/pull/850)で`pessimistic-txn`の構成パラメーターが省略される問題を修正します。
-   TiDBダッシュボード[＃853](https://github.com/pingcap/tidb-ansible/pull/853)でメトリックを追加および最適化する
-   TiDBダッシュボード[＃854](https://github.com/pingcap/tidb-ansible/pull/854)に各監視項目の説明を追加します
-   TiDBサマリーダッシュボードを追加して、クラスタのステータスをより適切に表示し、問題のトラブルシューティングを行います[＃855](https://github.com/pingcap/tidb-ansible/pull/855)
-   TiKVダッシュボード[＃857](https://github.com/pingcap/tidb-ansible/pull/857)のアロケータ統計監視項目を更新します。
-   ノードエクスポータのアラート式[＃860](https://github.com/pingcap/tidb-ansible/pull/860)のユニットエラーを修正します。
-   TiSparkjarパッケージを[＃862](https://github.com/pingcap/tidb-ansible/pull/862)にアップグレードします。
-   Ansibleタスク機能の説明を更新する[＃867](https://github.com/pingcap/tidb-ansible/pull/867)
-   TiDBダッシュボード[＃874](https://github.com/pingcap/tidb-ansible/pull/874)のローカルリーダーリクエスト監視項目の式を更新します。
-   概要ダッシュボードのTiKVメモリ監視項目の表現を更新し、監視が誤って表示される問題を修正します[＃879](https://github.com/pingcap/tidb-ansible/pull/879)
-   Kafkaモード[＃878](https://github.com/pingcap/tidb-ansible/pull/878)でBinlogサポートを削除します
-   `rolling_update.yml`の操作を実行するときにPDがリーダーを転送できない問題を修正します[＃887](https://github.com/pingcap/tidb-ansible/pull/887)
