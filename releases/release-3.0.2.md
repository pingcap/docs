---
title: TiDB 3.0.2 Release Notes
---

# TiDB 3.0.2 リリースノート {#tidb-3-0-2-release-notes}

発売日：2019年8月7日

TiDB バージョン: 3.0.2

TiDB アンシブル バージョン: 3.0.2

## TiDB {#tidb}

-   SQL オプティマイザー
    -   クエリで同じテーブルが複数回発生し、論理的にクエリ結果が常に空である場合、「スキーマ内の列が見つかりません」というメッセージが報告される問題を修正します[#11247](https://github.com/pingcap/tidb/pull/11247)
    -   `TIDB_INLJ`ヒントが正しく機能しないことが原因で、クエリ プランが期待どおりにならない問題を修正します ( `explain select /*+ TIDB_INLJ(t1) */ t1.b, t2.a from t t1, t t2 where t1.b = t2.a`など) [#11362](https://github.com/pingcap/tidb/pull/11362)
    -   クエリ結果の列名が間違っている場合がある問題を修正 ( `SELECT IF(1,c,c) FROM t`など) [#11379](https://github.com/pingcap/tidb/pull/11379)
    -   `LIKE`式が場合によっては暗黙的に 0 に変換されるため、 `SELECT 0 LIKE 'a string'`などの一部のクエリが`TRUE`返す問題を修正します[#11411](https://github.com/pingcap/tidb/pull/11411)
    -   `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [#11459](https://github.com/pingcap/tidb/pull/11459)のように、 `SHOW`ステートメントでサブクエリをサポートする
    -   集計関数の関連する列が見つからず、 `outerJoinElimination`の最適化ルールが列の別名を正しく処理していないためにエラーが報告される問題を修正します。最適化プロセスでのエイリアス解析を改善して、最適化がより多くのクエリ タイプをカバーできるようにする[#11377](https://github.com/pingcap/tidb/pull/11377)
    -   Window関数で構文制限に違反した場合にエラーが報告されない問題を修正 (たとえば、Frame定義の最後に`UNBOUNDED PRECEDING`を使用することはできません) [#11543](https://github.com/pingcap/tidb/pull/11543)
    -   `ERROR 3593 (HY000): You cannot use the window function FUNCTION_NAME in this context`エラー メッセージで`FUNCTION_NAME`が大文字で、MySQL [#11535](https://github.com/pingcap/tidb/pull/11535)との非互換性を引き起こす問題を修正します。
    -   Window 関数で実装されていない`IGNORE NULLS`構文が使用されているが、エラーが報告されない問題を修正します[#11593](https://github.com/pingcap/tidb/pull/11593)
    -   オプティマイザーが時間と等しい条件を正しく推定しない問題を修正します[#11512](https://github.com/pingcap/tidb/pull/11512)
    -   フィードバック情報に基づく上位 N 統計の更新のサポート[#11507](https://github.com/pingcap/tidb/pull/11507)
-   SQL 実行エンジン
    -   `INSERT`関数のパラメーター[#11248](https://github.com/pingcap/tidb/pull/11248)に`NULL`が含まれている場合、戻り値が`NULL`ではない問題を修正します。
    -   `ADMIN CHECKSUM`操作[#11266](https://github.com/pingcap/tidb/pull/11266)でパーティションテーブルをチェックすると計算結果がおかしくなることがある問題を修正
    -   INDEX JOIN で接頭辞インデックス[#11246](https://github.com/pingcap/tidb/pull/11246)を使用すると、結果が正しくない場合がある問題を修正
    -   `DATE_ADD`関数がマイクロ秒を含む日付数値の減算を行うと、分数の位置合わせが正しくないために結果が正しくない場合がある問題を修正します[#11288](https://github.com/pingcap/tidb/pull/11288)
    -   `DATE_ADD`関数が`INTERVAL` [#11325](https://github.com/pingcap/tidb/pull/11325)の負の数を誤って処理することによって引き起こされた誤った結果を修正します。
    -   `Mod(%)` 、 `Multiple(*)`または`Minus(-)` 0 を返し、小数桁数が大きい場合 ( `select 0.000 % 0.11234500000000000000`など) に、 `Mod(%)` 、 `Multiple(*)`または`Minus(-)`によって返される小数桁数が MySQL のそれと異なる問題を修正します[#11251](https://github.com/pingcap/tidb/pull/11251)
    -   `CONCAT`と`CONCAT_WS`の関数が返す結果の長さが`max_allowed_packet` [#11275](https://github.com/pingcap/tidb/pull/11275)を超えると、警告付きの`NULL`誤って返される問題を修正
    -   `SUBTIME`と`ADDTIME`の関数のパラメータが無効な場合、警告付きの`NULL`誤って返される問題を修正[#11337](https://github.com/pingcap/tidb/pull/11337)
    -   `CONVERT_TZ`関数のパラメータが無効な場合に`NULL`が誤って返される問題を修正[#11359](https://github.com/pingcap/tidb/pull/11359)
    -   `EXPLAIN ANALYZE`によって返された結果に`MEMORY`列を追加して、このクエリのメモリ使用量を表示します[#11418](https://github.com/pingcap/tidb/pull/11418)
    -   `EXPLAIN` [#11429](https://github.com/pingcap/tidb/pull/11429)の結果に`CARTESIAN` Join を加算します。
    -   float 型と double 型の自動インクリメント列の誤ったデータを修正します[#11385](https://github.com/pingcap/tidb/pull/11385)
    -   `nil`疑似統計がダンプされるときの情報によって引き起こされるpanicの問題を修正します[#11460](https://github.com/pingcap/tidb/pull/11460)
    -   定数折り畳みの最適化によって引き起こされた`SELECT … CASE WHEN … ELSE NULL ...`の誤ったクエリ結果を修正します[#11441](https://github.com/pingcap/tidb/pull/11441)
    -   `floatStrToIntStr`が`+999.9999e2` [#11473](https://github.com/pingcap/tidb/pull/11473)などの入力を正しく解析しない問題を修正
    -   `DATE_ADD`と`DATE_SUB`関数の結果がオーバーフローした場合に`NULL`が返されない場合がある問題を修正[#11476](https://github.com/pingcap/tidb/pull/11476)
    -   長い文字列を整数に変換する際、文字列に無効な文字が含まれていると変換結果がMySQLと異なる問題を修正[#11469](https://github.com/pingcap/tidb/pull/11469)
    -   この関数の大文字と小文字の区別が原因で、 `REGEXP BINARY`関数の結果が MySQL と互換性がないという問題を修正します[#11504](https://github.com/pingcap/tidb/pull/11504)
    -   `GRANT ROLE`ステートメントが`CURRENT_ROLE`受け取ったときにエラーが報告される問題を修正します。 `REVOKE ROLE`ステートメントが`mysql.default_role`特権を正しく取り消さないという問題を修正します[#11356](https://github.com/pingcap/tidb/pull/11356)
    -   `SELECT ADDDATE('2008-01-34', -1)` [#11447](https://github.com/pingcap/tidb/pull/11447)のようなステートメントを実行したときの`Incorrect datetime value`警告情報の表示形式の問題を修正します。
    -   JSON データの float フィールドが整数[#11534](https://github.com/pingcap/tidb/pull/11534)に変換されたときに結果がオーバーフローした場合、エラー メッセージが`constant … overflows float`ではなく`constant … overflows bigint`を報告する問題を修正します。
    -   `DATE_ADD`関数が`FLOAT` 、 `DOUBLE`および`DECIMAL`列のパラメーターを受け取ったときに、間違った型変換が原因で結果が間違っている可能性がある問題を修正します[#11527](https://github.com/pingcap/tidb/pull/11527)
    -   `DATE_ADD`関数の INTERVAL 分数の符号を正しく処理しないことによる誤った結果を修正します[#11615](https://github.com/pingcap/tidb/pull/11615)
    -   インデックス ルックアップ ジョインに`Ranger`インデックスが含まれている場合の不適切なクエリ結果を修正します[#11565](https://github.com/pingcap/tidb/pull/11565)
    -   `NAME_CONST`の 2 番目のパラメーターが負の数[#11268](https://github.com/pingcap/tidb/pull/11268)の場合に`NAME_CONST`関数を実行すると、&quot;Incorrect arguments to NAME_CONST&quot; メッセージが報告される問題を修正します。
    -   SQL ステートメントで現在時刻の計算が行われ、値が複数回フェッチされる場合、結果が MySQL と互換性がないという問題を修正します。同じ SQL ステートメントの現在時刻を取得するときに同じ値を使用する[#11394](https://github.com/pingcap/tidb/pull/11394)
    -   `Close` of `baseExecutor`がエラーを報告するとき、 `Close`が`ChildExecutor`に対して呼び出されないという問題を修正します。この問題は、 `KILL`ステートメントが有効にならず、 `ChildExecutor`閉じられていない場合に、Goroutine リークにつながる可能性があります[#11576](https://github.com/pingcap/tidb/pull/11576)
-   サーバ
    -   `LOAD DATA`が CSV ファイルの欠落している`TIMESTAMP`フィールドを処理すると、現在のタイムスタンプではなく、自動追加された値が 0 になる問題を修正します[#11250](https://github.com/pingcap/tidb/pull/11250)
    -   `SHOW CREATE USER`ステートメントが関連する権限を正しくチェックしない問題を修正し、 `SHOW CREATE USER CURRENT_USER()`によって返される`USER`と`HOST`間違っている可能性がある[#11229](https://github.com/pingcap/tidb/pull/11229)
    -   JDBC [#11290](https://github.com/pingcap/tidb/pull/11290)で`executeBatch`を使用すると返される結果が間違っている場合がある問題を修正
    -   TiKV サーバーのポート[#11370](https://github.com/pingcap/tidb/pull/11370)を変更するときのストリーミング クライアントのログ情報の出力を減らします。
    -   ストリーミング クライアントが長時間ブロックされないように、ストリーミング クライアントを TiKVサーバーに再接続するロジックを最適化します[#11372](https://github.com/pingcap/tidb/pull/11372)
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [#11350](https://github.com/pingcap/tidb/pull/11350)に`REGION_ID`を加える
    -   リージョン数が多い場合に PD タイムアウトで TiDB API `http://{TiDBIP}:10080/regions/hot`を呼び出した際に、リージョン情報の取得に失敗しないように、PD API からのリージョン情報の取得のタイムアウト時間を解除[#11383](https://github.com/pingcap/tidb/pull/11383)
    -   リージョン関連のリクエストが、HTTP API でパーティションテーブル関連の Region を返さない問題を修正します[#11466](https://github.com/pingcap/tidb/pull/11466)
    -   ユーザーが悲観的・ロックを手動で検証する際に、低速操作によってロック・タイムアウトが発生する可能性を減らすには、次の変更を行います[#11521](https://github.com/pingcap/tidb/pull/11521) :
        -   悲観的ロックのデフォルトの TTL を 30 秒から 40 秒に増やします
        -   最大 TTL を 60 秒から 120 秒に増やします
        -   最初の`LockKeys`のリクエストから悲観的ロック期間を計算する
    -   TiKV クライアントの`SendRequest`関数ロジックを変更します。接続を確立できない場合に待機し続けるのではなく、すぐに別のピアに接続しようとします[#11531](https://github.com/pingcap/tidb/pull/11531)
    -   リージョンキャッシュの最適化: ストアが移動され、別のストアが同じアドレスでオンラインになっている場合、削除されたストアに無効のラベルを付けて、できるだけ早くキャッシュ内のストア情報を更新します[#11567](https://github.com/pingcap/tidb/pull/11567)
    -   `http://{TiDB_ADDRESS:TIDB_IP}/mvcc/key/{db}/{table}/{handle}` API によって返された結果にリージョンID を追加します[#11557](https://github.com/pingcap/tidb/pull/11557)
    -   Scatter Table API が Range キー[#11298](https://github.com/pingcap/tidb/pull/11298)をエスケープしないことが原因で、Scatter Table が機能しない問題を修正します。
    -   リージョンキャッシュの最適化: 対応するストアにアクセスできない場合、リージョンが存在するストアに無効のラベルを付けて、このストアへのアクセスによるクエリ パフォーマンスの低下を回避します[#11498](https://github.com/pingcap/tidb/pull/11498)
    -   同じ名前のデータベースを[#11585](https://github.com/pingcap/tidb/pull/11585)回ドロップした後でも、HTTP API を使用してテーブル スキーマを取得できるというエラーを修正します。
-   DDL
    -   長さがゼロの非文字列列にインデックスを付けるとエラーが発生する問題を修正します[#11214](https://github.com/pingcap/tidb/pull/11214)
    -   外部キー制約とフルテキスト インデックスを使用して列を変更できないようにする (注: TiDB は、構文で外部キー制約とフルテキスト インデックスを引き続きサポートしています) [#11274](https://github.com/pingcap/tidb/pull/11274)
    -   `ALTER TABLE`ステートメントによって変更された位置と列のデフォルト値が同時に使用されるため、列のインデックス オフセットが間違っている可能性がある問題を修正します[#11346](https://github.com/pingcap/tidb/pull/11346)
    -   JSON ファイルの解析時に発生する 2 つの問題を修正します。
        -   `uint64` in `ConvertJSONToFloat`の中間解析結果として`int64`が使用されるため、精度オーバーフロー エラー[#11433](https://github.com/pingcap/tidb/pull/11433)が発生します。
        -   `uint64` in `ConvertJSONToInt`の中間解析結果として`int64`が使用されるため、精度オーバーフロー エラー[#11551](https://github.com/pingcap/tidb/pull/11551)が発生します。
    -   自動インクリメント列のインデックスの削除を禁止して、自動インクリメント列が誤った結果を取得するのを回避します[#11399](https://github.com/pingcap/tidb/pull/11399)
    -   次の問題を修正します[#11492](https://github.com/pingcap/tidb/pull/11492) :
        -   文字セットではなく照合順序を明示的に指定すると、列の文字セットと照合順序が一致しません。
        -   `ALTER TABLE … MODIFY COLUMN`で指定された文字セットと照合順序の間に競合がある場合、エラーは正しく報告されません。
        -   `ALTER TABLE … MODIFY COLUMN`を使用して文字セットと照合順序を複数回指定する場合の MySQL との非互換性
    -   `TRACE`クエリの結果にサブクエリのトレースの詳細を追加します[#11458](https://github.com/pingcap/tidb/pull/11458)
    -   実行のパフォーマンスを最適化`ADMIN CHECK TABLE`し、実行時間を大幅に短縮[#11547](https://github.com/pingcap/tidb/pull/11547)
    -   `SPLIT TABLE … REGIONS/INDEX`で返された結果を追加し、 `TOTAL_SPLIT_REGION`と`SCATTER_FINISH_RATIO`にタイムアウト前に正常に分割されたリージョンの数を結果[#11484](https://github.com/pingcap/tidb/pull/11484)に表示するようにします
    -   `ON UPDATE CURRENT_TIMESTAMP`が列属性で浮動小数点精度が指定されている場合、 `SHOW CREATE TABLE`のようなステートメントで表示される精度が不完全である問題を修正[#11591](https://github.com/pingcap/tidb/pull/11591)
    -   仮想生成列の式に別の仮想生成列が含まれている場合、列のインデックス結果が正しく計算されない問題を修正します[#11475](https://github.com/pingcap/tidb/pull/11475)
    -   `ALTER TABLE … ADD PARTITION …`文の`VALUE LESS THAN`後にマイナス記号が付けられない問題を修正[#11581](https://github.com/pingcap/tidb/pull/11581)
-   モニター
    -   `TiKVTxnCmdCounter`監視メトリックが登録されていないため、データが収集および報告されない問題を修正します[#11316](https://github.com/pingcap/tidb/pull/11316)
    -   Bind Info [#11467](https://github.com/pingcap/tidb/pull/11467)の`BindUsageCounter` 、 `BindTotalGauge` 、および`BindMemoryUsage`モニタリング メトリックを追加します。

## TiKV {#tikv}

-   Raftログが時間内に書き込まれないと TiKV がパニックになるバグを修正[#5160](https://github.com/tikv/tikv/pull/5160)
-   TiKVがパニックした後、ログファイルにpanic情報が書き込まれない不具合を修正[#5198](https://github.com/tikv/tikv/pull/5198)
-   悲観的トランザクションで Insert 操作が正しく実行されない可能性があるバグを修正[#5203](https://github.com/tikv/tikv/pull/5203)
-   INFO [#5193](https://github.com/tikv/tikv/pull/5193)への手動介入を必要としない一部のログの出力レベルを下げます
-   storageエンジンのサイズを監視する精度を向上させる[#5200](https://github.com/tikv/tikv/pull/5200)
-   tikv-ctl [#5195](https://github.com/tikv/tikv/pull/5195)のリージョンサイズの精度を向上
-   悲観的ロック[#5192](https://github.com/tikv/tikv/pull/5192)のデッドロック検出器のパフォーマンスを向上させます。
-   Titanstorageエンジン[#5197](https://github.com/tikv/tikv/pull/5197)で GC のパフォーマンスを向上させる

## PD {#pd}

-   Scatter リージョンスケジューラが動作しないバグを修正[#1642](https://github.com/pingcap/pd/pull/1642)
-   pd-ctl [#1653](https://github.com/pingcap/pd/pull/1653)でリージョンのリージョン操作ができない不具合を修正
-   pd-ctl [#1651](https://github.com/pingcap/pd/pull/1651)でremove-tombstone操作ができない不具合を修正
-   スキャンリージョン操作[#1648](https://github.com/pingcap/pd/pull/1648)を実行すると、キー スコープと重なるリージョンが見つからないという問題を修正します。
-   再試行メカニズムを追加して、メンバーが PD [#1643](https://github.com/pingcap/pd/pull/1643)に正常に追加されたことを確認します

## ツール {#tools}

TiDBBinlog

-   起動時に設定項目チェック機能を追加します。これにより、 Binlogサービスが停止し、無効な項目が見つかった場合にエラーが報告されます[#687](https://github.com/pingcap/tidb-binlog/pull/687)
-   Drainerに`node-id`構成を追加して、 Drainer [#684](https://github.com/pingcap/tidb-binlog/pull/684)で使用される特定のロジックを指定します。

TiDB Lightning

-   2 つのチェックサムが同時に実行されている場合、 `tikv_gc_life_time`が元の値に戻されない問題を修正します[#218](https://github.com/pingcap/tidb-lightning/pull/218)
-   起動時に設定項目チェック機能を追加します。これにより、 Binlogサービスが停止し、無効な項目が見つかった場合にエラーが報告されます[#217](https://github.com/pingcap/tidb-lightning/pull/217)

## TiDB アンシブル {#tidb-ansible}

-   ディスク パフォーマンス モニタが秒をミリ秒として扱う単位エラーを修正します[#840](https://github.com/pingcap/tidb-ansible/pull/840)
-   Spark [#841](https://github.com/pingcap/tidb-ansible/pull/841)に`log4j`構成ファイルを追加します。
-   Binlog が有効で、Kafka または ZooKeeper が構成されている場合に、Prometheus 構成ファイルが間違った形式で生成される問題を修正します[#844](https://github.com/pingcap/tidb-ansible/pull/844)
-   生成された TiDB 構成ファイルで`pessimistic-txn`構成パラメーターが除外される問題を修正します[#850](https://github.com/pingcap/tidb-ansible/pull/850)
-   TiDB ダッシュボードにメトリックを追加して最適化する[#853](https://github.com/pingcap/tidb-ansible/pull/853)
-   TiDBダッシュボードに各監視項目の説明を追加[#854](https://github.com/pingcap/tidb-ansible/pull/854)
-   TiDB サマリー ダッシュボードを追加して、クラスターのステータスをより適切に表示し、問題をトラブルシューティングします[#855](https://github.com/pingcap/tidb-ansible/pull/855)
-   TiKV ダッシュボードの Allocator Stats 監視項目を更新します[#857](https://github.com/pingcap/tidb-ansible/pull/857)
-   Node Exporter のアラート式[#860](https://github.com/pingcap/tidb-ansible/pull/860)の単位エラーを修正します。
-   TiSpark jar パッケージを v2.1.2 にアップグレードする[#862](https://github.com/pingcap/tidb-ansible/pull/862)
-   Ansible Task 機能の説明を更新します[#867](https://github.com/pingcap/tidb-ansible/pull/867)
-   TiDB ダッシュボード[#874](https://github.com/pingcap/tidb-ansible/pull/874)のローカル リーダー リクエスト監視項目の式を更新します。
-   概要ダッシュボードの TiKV メモリ監視項目の表現を更新し、監視が誤って表示される問題を修正[#879](https://github.com/pingcap/tidb-ansible/pull/879)
-   Kafka モード[#878](https://github.com/pingcap/tidb-ansible/pull/878)でのBinlogサポートの削除
-   `rolling_update.yml`操作[#887](https://github.com/pingcap/tidb-ansible/pull/887)の実行時に PD がLeaderの転送に失敗する問題を修正
