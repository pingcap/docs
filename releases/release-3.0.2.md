---
title: TiDB 3.0.2 Release Notes
---

# TiDB 3.0.2 リリースノート {#tidb-3-0-2-release-notes}

発売日：2019年8月7日

TiDB バージョン: 3.0.2

TiDB Ansible バージョン: 3.0.2

## TiDB {#tidb}

-   SQLオプティマイザー
    -   クエリ内で同じテーブルが複数回発生し、論理的にクエリ結果が常に空になる場合に、「スキーマ内に列が見つかりません」というメッセージが報告される問題を修正します[#11247](https://github.com/pingcap/tidb/pull/11247)
    -   場合によっては`TIDB_INLJ`ヒントが正しく機能しないことが原因でクエリ プランが期待を満たさない問題 ( `explain select /*+ TIDB_INLJ(t1) */ t1.b, t2.a from t t1, t t2 where t1.b = t2.a`など) を修正します[#11362](https://github.com/pingcap/tidb/pull/11362)
    -   場合によってはクエリ結果の列名が間違っている問題を修正します ( `SELECT IF(1,c,c) FROM t`など) [#11379](https://github.com/pingcap/tidb/pull/11379)
    -   場合によっては`LIKE`の式が暗黙的に 0 に変換されるため、 `SELECT 0 LIKE 'a string'`のような一部のクエリが`TRUE`返す問題を修正します[#11411](https://github.com/pingcap/tidb/pull/11411)
    -   `SHOW`ステートメント内のサブクエリ ( `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [#11459](https://github.com/pingcap/tidb/pull/11459)など) をサポートします。
    -   集計関数の関連列が見つからず、 `outerJoinElimination`の別名を正しく処理しない最適化ルールが原因でエラーが報告される問題を修正します。最適化プロセスでのエイリアス解析を改善し、 [#11377](https://github.com/pingcap/tidb/pull/11377)多くのクエリ タイプを最適化でカバーできるようにします。
    -   Window 関数で構文制限に違反した場合にエラーが報告されない問題を修正しました (たとえば、Frame 定義の最後に`UNBOUNDED PRECEDING`を指定することは許可されません) [#11543](https://github.com/pingcap/tidb/pull/11543)
    -   `ERROR 3593 (HY000): You cannot use the window function FUNCTION_NAME in this context`エラー メッセージの`FUNCTION_NAME`が大文字であり、MySQL [#11535](https://github.com/pingcap/tidb/pull/11535)との非互換性を引き起こす問題を修正します。
    -   Window 関数で実装されていない`IGNORE NULLS`構文が使用されているが、エラーが報告されない問題を修正します[#11593](https://github.com/pingcap/tidb/pull/11593)
    -   オプティマイザーが時間均等条件[#11512](https://github.com/pingcap/tidb/pull/11512)を正しく推定しない問題を修正します。
    -   フィードバック情報に基づいた上位 N 統計の更新をサポート[#11507](https://github.com/pingcap/tidb/pull/11507)
-   SQL実行エンジン
    -   `INSERT`関数のパラメータ[#11248](https://github.com/pingcap/tidb/pull/11248)に`NULL`が含まれる場合、戻り値が`NULL`にならない問題を修正
    -   `ADMIN CHECKSUM`オペレーション[#11266](https://github.com/pingcap/tidb/pull/11266)でパーティションテーブルをチェックすると計算結果が不正になる場合がある問題を修正
    -   INDEX JOIN で接頭辞インデックス[#11246](https://github.com/pingcap/tidb/pull/11246)を使用すると結果が不正になる場合がある問題を修正
    -   `DATE_ADD`関数がマイクロ秒[#11288](https://github.com/pingcap/tidb/pull/11288)を含む日付数値の減算を行う場合、分数の位置が正しくないために結果が間違っている可能性がある問題を修正します。
    -   `DATE_ADD`関数が`INTERVAL` [#11325](https://github.com/pingcap/tidb/pull/11325)の負の数を誤って処理することによって引き起こされる間違った結果を修正しました。
    -   `Mod(%)` 、 `Multiple(*)`または`Minus(-)` 0 を返し、小数部の桁数が大きい ( `select 0.000 % 0.11234500000000000000`など) 場合、 `Mod(%)` 、 `Multiple(*)`または`Minus(-)`によって返される小数[#11251](https://github.com/pingcap/tidb/pull/11251)の桁数が MySQL の桁数と異なる問題を修正します。
    -   `CONCAT`と`CONCAT_WS`の関数で返される結果の長さが`max_allowed_packet` [#11275](https://github.com/pingcap/tidb/pull/11275)を超える場合、警告付きの`NULL`誤って返される問題を修正
    -   `SUBTIME`関数のパラメータが無効な場合、警告付きの`NULL`が誤って返される問題`ADDTIME`修正[#11337](https://github.com/pingcap/tidb/pull/11337)
    -   `CONVERT_TZ`関数のパラメータが無効な場合に誤って`NULL`が返される問題を修正[#11359](https://github.com/pingcap/tidb/pull/11359)
    -   `EXPLAIN ANALYZE`によって返された結果に`MEMORY`列を追加して、このクエリのメモリ使用量を表示します[#11418](https://github.com/pingcap/tidb/pull/11418)
    -   `EXPLAIN` [#11429](https://github.com/pingcap/tidb/pull/11429)の結果に`CARTESIAN`結合を追加します。
    -   float 型と double 型の自動インクリメント列の不正なデータを修正[#11385](https://github.com/pingcap/tidb/pull/11385)
    -   疑似統計がダンプされるときに`nil`情報によって引き起こされるpanicの問題を修正します[#11460](https://github.com/pingcap/tidb/pull/11460)
    -   定数フォールディングの最適化による誤ったクエリ結果`SELECT … CASE WHEN … ELSE NULL ...`修正します[#11441](https://github.com/pingcap/tidb/pull/11441)
    -   `floatStrToIntStr`が`+999.9999e2` [#11473](https://github.com/pingcap/tidb/pull/11473)などの入力を正しく解析しない問題を修正
    -   `DATE_ADD`と`DATE_SUB`関数の結果が[#11476](https://github.com/pingcap/tidb/pull/11476)をオーバーフローした場合、 `NULL`が返されない場合がある問題を修正
    -   長い文字列を整数[#11469](https://github.com/pingcap/tidb/pull/11469)に変換する際、文字列に無効な文字が含まれる場合、変換結果がMySQLと異なる問題を修正
    -   この関数の大文字と小文字の区別が原因で、関数`REGEXP BINARY`の結果が MySQL と互換性がないという問題を修正します[#11504](https://github.com/pingcap/tidb/pull/11504)
    -   `GRANT ROLE`ステートメントが`CURRENT_ROLE`受け取るとエラーが報告される問題を修正します。 `REVOKE ROLE`ステートメントが`mysql.default_role`特権[#11356](https://github.com/pingcap/tidb/pull/11356)を正しく取り消さない問題を修正します。
    -   `SELECT ADDDATE('2008-01-34', -1)` [#11447](https://github.com/pingcap/tidb/pull/11447)のようなステートメント実行時の`Incorrect datetime value`警告情報の表示形式の問題を修正
    -   JSON データの浮動小数点フィールドが整数[#11534](https://github.com/pingcap/tidb/pull/11534)に変換されるときに結果がオーバーフローした場合、エラー メッセージが`constant … overflows float`ではなく`constant … overflows bigint`を報告する問題を修正します。
    -   `DATE_ADD`関数が`FLOAT` 、 `DOUBLE` 、 `DECIMAL`列パラメータを受け取った場合、不正な型変換により結果が間違っている可能性がある問題を修正[#11527](https://github.com/pingcap/tidb/pull/11527)
    -   `DATE_ADD`関数[#11615](https://github.com/pingcap/tidb/pull/11615)の INTERVAL 分数の符号の処理が間違っていることによって引き起こされる間違った結果を修正しました。
    -   `Ranger`がプレフィックス インデックスを正しく処理していないことが原因で、インデックス ルックアップ結合にプレフィックス インデックスが含まれている場合の誤ったクエリ結果を修正します[#11565](https://github.com/pingcap/tidb/pull/11565)
    -   `NAME_CONST`の 2 番目のパラメータが負の数[#11268](https://github.com/pingcap/tidb/pull/11268)であるときに`NAME_CONST`関数が実行されると、「NAME_CONST の引数が正しくありません」というメッセージが報告される問題を修正します。
    -   SQL ステートメントに現在時刻の計算が含まれ、値が複数回フェッチされる場合、結果が MySQL と互換性がないという問題を修正します。同じ SQL ステートメントの現在時刻を取得する場合は、同じ値を使用します[#11394](https://github.com/pingcap/tidb/pull/11394)
    -   `baseExecutor`の`Close`エラーを報告した場合、 `ChildExecutor`に対して`Close`が呼び出されない問題を修正します。この問題は、 `KILL`ステートメントが有効にならず、 `ChildExecutor`が閉じられていない場合に、Goroutine リークを引き起こす可能性があります[#11576](https://github.com/pingcap/tidb/pull/11576)
-   サーバ
    -   CSV ファイルの欠落している`TIMESTAMP`フィールドを`LOAD DATA`で処理するときに、現在のタイムスタンプではなく自動追加される値が 0 になる問題を修正します[#11250](https://github.com/pingcap/tidb/pull/11250)
    -   `SHOW CREATE USER`ステートメントが関連する権限を正しくチェックしない問題、および`SHOW CREATE USER CURRENT_USER()`によって返される`USER`と`HOST`間違っている可能性がある問題を修正[#11229](https://github.com/pingcap/tidb/pull/11229)
    -   JDBC [#11290](https://github.com/pingcap/tidb/pull/11290)で`executeBatch`を使用した場合に返される結果が間違っている場合がある問題を修正
    -   TiKVサーバーのポート[#11370](https://github.com/pingcap/tidb/pull/11370)を変更する際のストリーミングクライアントのログ情報の印刷を削減します。
    -   ストリーミング クライアントが長時間ブロックされないように、ストリーミング クライアントを TiKVサーバーに再接続するロジックを最適化します[#11372](https://github.com/pingcap/tidb/pull/11372)
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [#11350](https://github.com/pingcap/tidb/pull/11350)に`REGION_ID`を追加
    -   リージョン数が多い場合に PD タイムアウトにより TiDB API `http://{TiDBIP}:10080/regions/hot`が呼び出された場合にリージョン情報取得のタイムアウト時間を解除します[#11383](https://github.com/pingcap/tidb/pull/11383)
    -   リージョン関連のリクエストが HTTP API [#11466](https://github.com/pingcap/tidb/pull/11466)のパーティションテーブル関連のリージョンを返さない問題を修正します。
    -   ユーザーが手動で悲観的ロック[#11521](https://github.com/pingcap/tidb/pull/11521)を検証するときに、操作の遅さによって引き起こされるロック タイムアウトの可能性を減らすために、次の変更を加えます。
        -   悲観的ロックのデフォルト TTL を 30 秒から 40 秒に増やします。
        -   最大 TTL を 60 秒から 120 秒に増加します
        -   最初の`LockKeys`のリクエストから悲観的ロック期間を計算します
    -   TiKV クライアントの`SendRequest`関数ロジックを変更します。接続を構築できない場合に待機し続けるのではなく、すぐに別のピアに接続するようにします[#11531](https://github.com/pingcap/tidb/pull/11531)
    -   リージョンキャッシュを最適化します。同じアドレスで別のストアがオンラインになっている間にストアが移動された場合、削除されたストアに無効のラベルを付けて、キャッシュ内のストア情報をできるだけ早く更新します[#11567](https://github.com/pingcap/tidb/pull/11567)
    -   `http://{TiDB_ADDRESS:TIDB_IP}/mvcc/key/{db}/{table}/{handle}` API によって返された結果にリージョンID を追加します[#11557](https://github.com/pingcap/tidb/pull/11557)
    -   散布表 API が範囲キー[#11298](https://github.com/pingcap/tidb/pull/11298)をエスケープしないために発生する散布表が機能しない問題を修正します。
    -   リージョンキャッシュを最適化します。このストアへのアクセスによるクエリ パフォーマンスの低下を避けるために、対応するストアにアクセスできない場合、リージョンが存在するストアに無効のラベルを付けます[#11498](https://github.com/pingcap/tidb/pull/11498)
    -   同じ名前のデータベースを複数回削除した後でも、HTTP API を介してテーブル スキーマを取得できるというエラーを修正します[#11585](https://github.com/pingcap/tidb/pull/11585)
-   DDL
    -   長さ 0 の非文字列列にインデックスを付けるときにエラーが発生する問題を修正します[#11214](https://github.com/pingcap/tidb/pull/11214)
    -   外部キー制約とフルテキスト インデックスを持つ列の変更を禁止します (注: TiDB は引き続き構文で外部キー制約とフルテキスト インデックスをサポートします) [#11274](https://github.com/pingcap/tidb/pull/11274)
    -   `ALTER TABLE`ステートメントで変更した位置とカラムのデフォルト値を併用するため、カラムのインデックスオフセットが誤る可能性がある問題を修正[#11346](https://github.com/pingcap/tidb/pull/11346)
    -   JSON ファイルの解析時に発生する 2 つの問題を修正します。
        -   `int64`は`uint64` in `ConvertJSONToFloat`の中間解析結果として使用され、精度オーバーフロー エラー[#11433](https://github.com/pingcap/tidb/pull/11433)が発生します。
        -   `int64`は`uint64` in `ConvertJSONToInt`の中間解析結果として使用され、精度オーバーフロー エラー[#11551](https://github.com/pingcap/tidb/pull/11551)が発生します。
    -   自動インクリメント列が誤った結果を取得する可能性を避けるために、自動インクリメント列のインデックスの削除を禁止します[#11399](https://github.com/pingcap/tidb/pull/11399)
    -   次の問題を修正します[#11492](https://github.com/pingcap/tidb/pull/11492) :
        -   照合順序を明示的に指定したが文字照合順序を指定しなかった場合、文字セットと列の照合順序順序が一致しません。
        -   `ALTER TABLE … MODIFY COLUMN`で指定された文字セットと照合順序の間に矛盾がある場合、エラーは正しく報告されません。
        -   `ALTER TABLE … MODIFY COLUMN`を使用して文字セットと照合順序を複数回指定する場合の MySQL との非互換性
    -   サブクエリのトレース詳細を`TRACE`クエリの結果に追加します[#11458](https://github.com/pingcap/tidb/pull/11458)
    -   `ADMIN CHECK TABLE`の実行パフォーマンスを最適化し、実行時間を大幅に短縮します[#11547](https://github.com/pingcap/tidb/pull/11547)
    -   `SPLIT TABLE … REGIONS/INDEX`によって返された結果を加算し、 `TOTAL_SPLIT_REGION`と`SCATTER_FINISH_RATIO`にタイムアウト前に正常に分割されたリージョンの数を結果[#11484](https://github.com/pingcap/tidb/pull/11484)に表示させます。
    -   列属性に`ON UPDATE CURRENT_TIMESTAMP`指定し、float 精度を[#11591](https://github.com/pingcap/tidb/pull/11591)に指定した場合、 `SHOW CREATE TABLE`のようなステートメントで表示される精度が不完全になる問題を修正
    -   仮想生成列の式に別の仮想生成列が含まれる場合、その列のインデックス結果が正しく計算できない問題を修正します[#11475](https://github.com/pingcap/tidb/pull/11475)
    -   `ALTER TABLE … ADD PARTITION …`ステートメント[#11581](https://github.com/pingcap/tidb/pull/11581)の`VALUE LESS THAN`の後にマイナス記号を追加できない問題を修正します。
-   モニター
    -   `TiKVTxnCmdCounter`監視メトリクスが登録されていないため、データが収集およびレポートされない問題を修正します[#11316](https://github.com/pingcap/tidb/pull/11316)
    -   バインド情報[#11467](https://github.com/pingcap/tidb/pull/11467)に`BindUsageCounter` 、 `BindTotalGauge` 、および`BindMemoryUsage`監視メトリックを追加します。

## TiKV {#tikv}

-   Raftログが時間内に書き込まれないとTiKVがパニックになるバグを修正[#5160](https://github.com/tikv/tikv/pull/5160)
-   TiKVパニック後にpanic情報がログファイルに書き込まれないバグを修正[#5198](https://github.com/tikv/tikv/pull/5198)
-   悲観的トランザクション[#5203](https://github.com/tikv/tikv/pull/5203)でInsert操作が誤って実行される場合があるバグを修正
-   手動介入を必要としない一部のログの出力レベルを INFO [#5193](https://github.com/tikv/tikv/pull/5193)に下げます。
-   storageエンジン サイズの監視精度の向上[#5200](https://github.com/tikv/tikv/pull/5200)
-   tikv-ctl [#5195](https://github.com/tikv/tikv/pull/5195)のリージョンサイズの精度を向上させます。
-   悲観的ロック[#5192](https://github.com/tikv/tikv/pull/5192)のデッドロック検出器のパフォーマンスを向上させます。
-   Titanstorageエンジン[#5197](https://github.com/tikv/tikv/pull/5197)の GC のパフォーマンスを向上させます。

## PD {#pd}

-   Scatter リージョンスケジューラが動作しないバグを修正[#1642](https://github.com/pingcap/pd/pull/1642)
-   pd-ctl [#1653](https://github.com/pingcap/pd/pull/1653)でリージョンのリージョン操作ができないバグを修正
-   pd-ctl [#1651](https://github.com/pingcap/pd/pull/1651)でremove-tombstone操作ができない不具合を修正
-   スキャンリージョン操作[#1648](https://github.com/pingcap/pd/pull/1648)を実行すると、キースコープと重なっているリージョンが見つからない問題を修正
-   メンバーが PD [#1643](https://github.com/pingcap/pd/pull/1643)に正常に追加されたことを確認するための再試行メカニズムを追加します。

## ツール {#tools}

TiDBBinlog

-   起動時に構成項目チェック機能を追加します。これにより、 Binlogサービスが停止され、無効な項目が見つかった場合にエラーが報告されます[#687](https://github.com/pingcap/tidb-binlog/pull/687)
-   Drainerに`node-id`構成を追加して、 Drainer [#684](https://github.com/pingcap/tidb-binlog/pull/684)で使用される特定のロジックを指定します

TiDB Lightning

-   2つのチェックサムを同時に実行している場合、 `tikv_gc_life_time`元の値に戻すことができない問題を修正[#218](https://github.com/pingcap/tidb-lightning/pull/218)
-   起動時に構成項目チェック機能を追加します。これにより、 Binlogサービスが停止され、無効な項目が見つかった場合にエラーが報告されます[#217](https://github.com/pingcap/tidb-lightning/pull/217)

## TiDB Ansible {#tidb-ansible}

-   ディスクパフォ​​ーマンスモニターが秒をミリ秒として扱う単位エラーを修正[#840](https://github.com/pingcap/tidb-ansible/pull/840)
-   Spark [#841](https://github.com/pingcap/tidb-ansible/pull/841)に`log4j`構成ファイルを追加します
-   Binlog が有効で、Kafka または ZooKeeper が構成されている場合に、Prometheus 構成ファイルが間違った形式で生成される問題を修正します[#844](https://github.com/pingcap/tidb-ansible/pull/844)
-   生成された TiDB 構成ファイル[#850](https://github.com/pingcap/tidb-ansible/pull/850)で`pessimistic-txn`構成パラメーターが省略される問題を修正します。
-   TiDB ダッシュボードでメトリクスを追加および最適化する[#853](https://github.com/pingcap/tidb-ansible/pull/853)
-   TiDBダッシュボード[#854](https://github.com/pingcap/tidb-ansible/pull/854)に各監視項目の説明を追加
-   TiDB サマリー ダッシュボードを追加して、クラスターのステータスをより適切に表示し、問題のトラブルシューティングを行います[#855](https://github.com/pingcap/tidb-ansible/pull/855)
-   TiKV ダッシュボード[#857](https://github.com/pingcap/tidb-ansible/pull/857)のアロケーター統計監視項目を更新します。
-   ノード エクスポーターのアラート式[#860](https://github.com/pingcap/tidb-ansible/pull/860)単位エラーを修正しました。
-   TiSpark jar パッケージを v2.1.2 にアップグレードする[#862](https://github.com/pingcap/tidb-ansible/pull/862)
-   Ansible タスク機能[#867](https://github.com/pingcap/tidb-ansible/pull/867)の説明を更新
-   TiDB ダッシュボード[#874](https://github.com/pingcap/tidb-ansible/pull/874)上のローカル リーダー リクエスト監視項目の式を更新します。
-   概要ダッシュボードの TiKV メモリ監視項目の表現を更新し、監視[#879](https://github.com/pingcap/tidb-ansible/pull/879)が誤って表示される問題を修正しました。
-   Kafka モード[#878](https://github.com/pingcap/tidb-ansible/pull/878)でのBinlogサポートの削除
-   `rolling_update.yml`オペレーション[#887](https://github.com/pingcap/tidb-ansible/pull/887)実行時に PD がLeaderの転送に失敗する問題を修正
