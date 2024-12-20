---
title: TiDB 3.0.2 Release Notes
summary: TiDB 3.0.2 は、さまざまな修正と改善を加えて 2019 年 8 月 7 日にリリースされました。このリリースには、SQL オプティマイザー、SQL 実行エンジン、サーバー、DDL、モニター、TiKV、PD、TiDB Binlog、 TiDB Lightning、および TiDB Ansible の修正が含まれています。修正には、クエリ プラン、クエリ結果、エラー メッセージ、およびパフォーマンスの最適化に関する問題が含まれます。
---

# TiDB 3.0.2 リリースノート {#tidb-3-0-2-release-notes}

発売日: 2019年8月7日

TiDB バージョン: 3.0.2

TiDB Ansible バージョン: 3.0.2

## ティビ {#tidb}

-   SQL オプティマイザー
    -   クエリ内で同じテーブルが複数回出現し、論理的にクエリ結果が常に空である場合に「スキーマ内に列が見つかりません」というメッセージが報告される問題を修正しました[＃11247](https://github.com/pingcap/tidb/pull/11247)
    -   `TIDB_INLJ`ヒントが一部のケース（ `explain select /*+ TIDB_INLJ(t1) */ t1.b, t2.a from t t1, t t2 where t1.b = t2.a`など）で正しく機能しないことが原因でクエリプランが期待どおりに動作しない問題を修正しました[＃11362](https://github.com/pingcap/tidb/pull/11362)
    -   クエリ結果の列名が間違っている場合がある問題を修正しました（ `SELECT IF(1,c,c) FROM t`など） [＃11379](https://github.com/pingcap/tidb/pull/11379)
    -   `SELECT 0 LIKE 'a string'`ようなクエリが`TRUE`返す問題を修正しました。これは、 `LIKE`式が暗黙的に 0 に変換される場合があるためです[＃11411](https://github.com/pingcap/tidb/pull/11411)
    -   `SHOW`ステートメント内のサブクエリをサポートします (例: `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [＃11459](https://github.com/pingcap/tidb/pull/11459)
    -   `outerJoinElimination`最適化ルールが列エイリアスを正しく処理していないために、集計関数の関連列が見つからずエラーが報告される問題を修正しました。最適化プロセスでのエイリアス解析を改善し、最適化がより多くのクエリタイプをカバーするようにします[＃11377](https://github.com/pingcap/tidb/pull/11377)
    -   ウィンドウ関数で構文制限に違反した場合にエラーが報告されない問題を修正（例えば、フレーム定義の最後に`UNBOUNDED PRECEDING`出現することは許可されていない） [＃11543](https://github.com/pingcap/tidb/pull/11543)
    -   `ERROR 3593 (HY000): You cannot use the window function FUNCTION_NAME in this context`エラーメッセージで`FUNCTION_NAME`大文字になっている問題を修正しました。これにより、MySQL [＃11535](https://github.com/pingcap/tidb/pull/11535)との互換性が失われます。
    -   ウィンドウ関数で実装されていない`IGNORE NULLS`構文が使用されているにもかかわらずエラーが報告されない問題を修正[＃11593](https://github.com/pingcap/tidb/pull/11593)
    -   オプティマイザーが時間等条件[＃11512](https://github.com/pingcap/tidb/pull/11512)を正しく推定しない問題を修正
    -   フィードバック情報に基づくトップN統計の更新をサポート[＃11507](https://github.com/pingcap/tidb/pull/11507)
-   SQL実行エンジン
    -   `INSERT`関数のパラメータ[＃11248](https://github.com/pingcap/tidb/pull/11248)に`NULL`含まれている場合に、返される値が`NULL`ならない問題を修正しました。
    -   パーティションテーブルを`ADMIN CHECKSUM`操作[＃11266](https://github.com/pingcap/tidb/pull/11266)でチェックすると計算結果が間違っている可能性がある問題を修正
    -   INDEX JOIN がプレフィックスインデックス[＃11246](https://github.com/pingcap/tidb/pull/11246)を使用すると結果が間違ってしまう可能性がある問題を修正しました。
    -   `DATE_ADD`関数がマイクロ秒を含む日付数値の減算を行うときに分数が誤って揃えられることで結果が間違っている可能性がある問題を修正しました[＃11288](https://github.com/pingcap/tidb/pull/11288)
    -   `DATE_ADD`関数が`INTERVAL` [＃11325](https://github.com/pingcap/tidb/pull/11325)の負の数を誤って処理することで発生する誤った結果を修正しました。
    -   `Mod(%)` `Multiple(*)` 0 を返し、小数点以下の桁数が大きい場合 ( `Minus(-)` `select 0.000 % 0.11234500000000000000` )、 `Mod(%)` 、 `Multiple(*)` 、 `Minus(-)`で返される小数点以下の桁数が MySQL と異なる問題を修正しました[＃11251](https://github.com/pingcap/tidb/pull/11251)
    -   `CONCAT`と`CONCAT_WS`関数によって返される結果の長さが`max_allowed_packet` [＃11275](https://github.com/pingcap/tidb/pull/11275)と、警告付きの`NULL`誤って返される問題を修正しました。
    -   `SUBTIME`と`ADDTIME`関数のパラメータが無効な場合に警告付きの`NULL`が誤って返される問題を修正しました[＃11337](https://github.com/pingcap/tidb/pull/11337)
    -   `CONVERT_TZ`関数のパラメータが無効な場合に`NULL`が誤って返される問題を修正しました[＃11359](https://github.com/pingcap/tidb/pull/11359)
    -   このクエリのメモリ使用量を表示するには、 `EXPLAIN ANALYZE`によって返された結果に`MEMORY`列を追加します[＃11418](https://github.com/pingcap/tidb/pull/11418)
    -   `EXPLAIN` [＃11429](https://github.com/pingcap/tidb/pull/11429)の結果に`CARTESIAN` Joinを加える
    -   float 型と double 型の自動増分列の不正なデータを修正[＃11385](https://github.com/pingcap/tidb/pull/11385)
    -   疑似統計がダンプされるときに`nil`の情報によって発生するpanic問題を修正[＃11460](https://github.com/pingcap/tidb/pull/11460)
    -   定数畳み込み最適化[＃11441](https://github.com/pingcap/tidb/pull/11441)によって発生した`SELECT … CASE WHEN … ELSE NULL ...`の誤ったクエリ結果を修正
    -   `floatStrToIntStr` `+999.9999e2` [＃11473](https://github.com/pingcap/tidb/pull/11473)などの入力を正しく解析しない問題を修正
    -   `DATE_ADD`と`DATE_SUB`関数の結果が[＃11476](https://github.com/pingcap/tidb/pull/11476)超える場合に`NULL`が返されない場合がある問題を修正しました。
    -   長い文字列を整数に変換するときに、文字列に無効な文字が含まれていると、変換結果がMySQLと異なる問題を修正しました[＃11469](https://github.com/pingcap/tidb/pull/11469)
    -   この関数[＃11504](https://github.com/pingcap/tidb/pull/11504)の大文字と小文字の区別が原因で、関数`REGEXP BINARY`の結果が MySQL と互換性がない問題を修正しました。
    -   `GRANT ROLE`文が`CURRENT_ROLE`受け取ったときにエラーが報告される問題を修正します。5 文`REVOKE ROLE` `mysql.default_role`権限[＃11356](https://github.com/pingcap/tidb/pull/11356)を正しく取り消さない問題を修正します。
    -   `SELECT ADDDATE('2008-01-34', -1)` [＃11447](https://github.com/pingcap/tidb/pull/11447)のような文を実行する際の`Incorrect datetime value`警告情報の表示形式の問題を修正
    -   JSON データの float フィールドを整数[＃11534](https://github.com/pingcap/tidb/pull/11534)に変換するときに結果がオーバーフローすると、エラー メッセージに`constant … overflows bigint`ではなく`constant … overflows float`報告される問題を修正しました。
    -   `DATE_ADD`関数が`FLOAT` 、 `DOUBLE` 、 `DECIMAL`列のパラメータを受け取ったときに、誤った型変換によって結果が間違っている可能性がある問題を修正しました[＃11527](https://github.com/pingcap/tidb/pull/11527)
    -   `DATE_ADD`関数[＃11615](https://github.com/pingcap/tidb/pull/11615)の区間分数の符号を誤って処理することで発生する誤った結果を修正しました。
    -   プレフィックスインデックスが正しく処理されていないために、 `Ranger`ルックアップ結合にプレフィックスインデックスが含まれている場合に誤ったクエリ結果が発生する問題を修正しました[＃11565](https://github.com/pingcap/tidb/pull/11565)
    -   `NAME_CONST`の 2 番目のパラメータが負の数のときに`NAME_CONST`関数を実行すると、「NAME_CONST への引数が正しくありません」というメッセージが報告される問題を修正しました[＃11268](https://github.com/pingcap/tidb/pull/11268)
    -   SQL 文に現在時刻の計算が含まれており、その値が複数回取得される場合に結果が MySQL と互換性がない問題を修正しました。同じ SQL 文で現在時刻を取得する場合は同じ値を使用します[＃11394](https://github.com/pingcap/tidb/pull/11394)
    -   `baseExecutor`の`Close`がエラーを報告したときに`ChildExecutor`に対して`Close`が呼び出されない問題を修正しました。この問題により、 `KILL`ステートメントが有効にならず、 `ChildExecutor`が閉じられていない場合に Goroutine リークが発生する可能性があります[＃11576](https://github.com/pingcap/tidb/pull/11576)
-   サーバ
    -   CSVファイル[＃11250](https://github.com/pingcap/tidb/pull/11250)内の欠落している`TIMESTAMP`フィールドを処理するときに、自動的に追加された値が現在のタイムスタンプではなく`LOAD DATA`になる問題を修正しました。
    -   `SHOW CREATE USER`文が関連する権限を正しくチェックせず、 `SHOW CREATE USER CURRENT_USER()`によって返される`USER`と`HOST`間違っている可能性がある問題を修正しました[＃11229](https://github.com/pingcap/tidb/pull/11229)
    -   JDBC [＃11290](https://github.com/pingcap/tidb/pull/11290)で`executeBatch`使用すると返される結果が間違っている可能性がある問題を修正しました
    -   TiKVサーバーのポート[＃11370](https://github.com/pingcap/tidb/pull/11370)変更するときにストリーミングクライアントのログ情報の出力を減らす
    -   ストリーミングクライアントが長時間ブロックされないように、ストリーミングクライアントを TiKVサーバーに再接続するロジックを最適化します[＃11372](https://github.com/pingcap/tidb/pull/11372)
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [＃11350](https://github.com/pingcap/tidb/pull/11350)に`REGION_ID`加える
    -   PD APIからのリージョン情報取得のタイムアウト期間を解除し、リージョン数が多い場合にPDタイムアウトによりTiDB API `http://{TiDBIP}:10080/regions/hot`が呼び出されたときにリージョン情報の取得が失敗しないようにする[＃11383](https://github.com/pingcap/tidb/pull/11383)
    -   リージョン関連のリクエストがHTTP API [＃11466](https://github.com/pingcap/tidb/pull/11466)でパーティションテーブル関連のリージョンを返さない問題を修正
    -   ユーザーが手動で悲観的ロック[＃11521](https://github.com/pingcap/tidb/pull/11521)を検証するときに、遅い操作によって発生するロック タイムアウトの可能性を減らすには、次の変更を行います。
        -   悲観的ロックのデフォルト TTL を 30 秒から 40 秒に増やす
        -   最大TTLを60秒から120秒に増やす
        -   最初の`LockKeys`リクエストから悲観的ロック期間を計算する
    -   TiKVクライアントの`SendRequest`機能ロジックを変更:接続が構築できない場合に待機し続けるのではなく、すぐに別のピアに接続しようとします[＃11531](https://github.com/pingcap/tidb/pull/11531)
    -   リージョンキャッシュを最適化します。ストアが移動され、別のストアが同じアドレスでオンラインになったときに、削除されたストアを無効としてラベル付けし、キャッシュ内のストア情報をできるだけ早く更新します[＃11567](https://github.com/pingcap/tidb/pull/11567)
    -   `http://{TiDB_ADDRESS:TIDB_IP}/mvcc/key/{db}/{table}/{handle}` API [＃11557](https://github.com/pingcap/tidb/pull/11557)によって返される結果にリージョンIDを追加します。
    -   Scatter Table API が Range キー[＃11298](https://github.com/pingcap/tidb/pull/11298)をエスケープしないために Scatter Table が動作しない問題を修正しました。
    -   リージョンキャッシュを最適化します。対応するストアにアクセスできない場合は、リージョンが存在するストアを無効としてラベル付けし、このストアにアクセスすることによって発生するクエリパフォーマンスの低下を回避します[＃11498](https://github.com/pingcap/tidb/pull/11498)
    -   同じ名前のデータベースを複数回削除した後でも、HTTP API 経由でテーブル スキーマを取得できるというエラーを修正しました[＃11585](https://github.com/pingcap/tidb/pull/11585)
-   DDL
    -   長さがゼロの非文字列列をインデックスするときにエラーが発生する問題を修正[＃11214](https://github.com/pingcap/tidb/pull/11214)
    -   外部キー制約とフルテキストインデックスを持つ列の変更を禁止します（注：TiDBは構文で外部キー制約とフルテキストインデックスを引き続きサポートします） [＃11274](https://github.com/pingcap/tidb/pull/11274)
    -   `ALTER TABLE`ステートメントによって変更された位置と列のデフォルト値が同時に使用されるため、列のインデックスオフセットが間違っている可能性がある問題を修正しました[＃11346](https://github.com/pingcap/tidb/pull/11346)
    -   JSON ファイルを解析するときに発生する 2 つの問題を修正します。
        -   `int64`は`ConvertJSONToFloat`の`uint64`の中間解析結果として使用され、精度オーバーフローエラー[＃11433](https://github.com/pingcap/tidb/pull/11433)が発生します。
        -   `int64`は`ConvertJSONToInt`の`uint64`の中間解析結果として使用され、精度オーバーフローエラー[＃11551](https://github.com/pingcap/tidb/pull/11551)が発生します。
    -   自動インクリメント列で誤った結果が返されるのを避けるため、自動インクリメント列のインデックスの削除を禁止します[＃11399](https://github.com/pingcap/tidb/pull/11399)
    -   次の問題を修正しました[＃11492](https://github.com/pingcap/tidb/pull/11492) :
        -   照合順序を明示的に指定し、文字セットを指定していない場合、列の文字セットと照合順序が一致しません。
        -   `ALTER TABLE … MODIFY COLUMN`で指定された文字セットと照合順序の間に矛盾がある場合、エラーは正しく報告されません。
        -   `ALTER TABLE … MODIFY COLUMN`使用して文字セットと照合順序を複数回指定すると、MySQL との互換性がなくなる
    -   サブクエリのトレースの詳細を`TRACE`クエリ[＃11458](https://github.com/pingcap/tidb/pull/11458)の結果に追加します
    -   `ADMIN CHECK TABLE`の実行パフォーマンスを最適化し、実行時間を大幅に短縮する[＃11547](https://github.com/pingcap/tidb/pull/11547)
    -   `SPLIT TABLE … REGIONS/INDEX`で返された結果を追加し、 `TOTAL_SPLIT_REGION`と`SCATTER_FINISH_RATIO`に、結果[＃11484](https://github.com/pingcap/tidb/pull/11484)のタイムアウト前に正常に分割されたリージョンの数を表示するようにします。
    -   列属性が`ON UPDATE CURRENT_TIMESTAMP`で float 精度が指定されている場合に、 `SHOW CREATE TABLE`のようなステートメントで表示される精度が不完全になる問題を修正しました[＃11591](https://github.com/pingcap/tidb/pull/11591)
    -   仮想生成列の式に別の仮想生成列[＃11475](https://github.com/pingcap/tidb/pull/11475)が含まれている場合に、列のインデックス結果が正しく計算されない問題を修正しました。
    -   `ALTER TABLE … ADD PARTITION …`文[＃11581](https://github.com/pingcap/tidb/pull/11581)の`VALUE LESS THAN`後にマイナス記号を追加できない問題を修正
-   モニター
    -   `TiKVTxnCmdCounter`監視メトリックが登録されていないため、データが収集およびレポートされない問題を修正[＃11316](https://github.com/pingcap/tidb/pull/11316)
    -   Bind Info `BindMemoryUsage` `BindUsageCounter` `BindTotalGauge`を追加します[＃11467](https://github.com/pingcap/tidb/pull/11467)

## ティクヴ {#tikv}

-   Raftログが時間内に書き込まれない場合に TiKV がパニックになるバグを修正しました[＃5160](https://github.com/tikv/tikv/pull/5160)
-   TiKV パニック後にpanic情報がログファイルに書き込まれないバグを修正[＃5198](https://github.com/tikv/tikv/pull/5198)
-   悲観的トランザクション[＃5203](https://github.com/tikv/tikv/pull/5203)で挿入操作が誤って実行される可能性があるバグを修正
-   手動介入を必要としない一部のログの出力レベルをINFO [＃5193](https://github.com/tikv/tikv/pull/5193)に下げる
-   storageエンジンサイズの監視精度の向上[＃5200](https://github.com/tikv/tikv/pull/5200)
-   tikv-ctl [＃5195](https://github.com/tikv/tikv/pull/5195)のリージョンサイズの精度を向上
-   悲観的ロックのデッドロック検出器のパフォーマンスを向上[＃5192](https://github.com/tikv/tikv/pull/5192)
-   Titanstorageエンジン[＃5197](https://github.com/tikv/tikv/pull/5197)のGCのパフォーマンスを向上

## PD {#pd}

-   Scatter リージョンスケジューラが動作しないバグを修正[＃1642](https://github.com/pingcap/pd/pull/1642)
-   pd-ctl [＃1653](https://github.com/pingcap/pd/pull/1653)でリージョンのマージ操作が実行できないバグを修正
-   pd-ctl [＃1651](https://github.com/pingcap/pd/pull/1651)で削除トゥームストーン操作が実行できないバグを修正
-   スキャンリージョン操作[＃1648](https://github.com/pingcap/pd/pull/1648)を実行するときに、キー スコープと重複するリージョンが見つからない問題を修正しました。
-   PD [＃1643](https://github.com/pingcap/pd/pull/1643)にメンバーが正常に追加されたことを確認するための再試行メカニズムを追加します。

## ツール {#tools}

TiDBBinlog

-   起動時に構成項目チェック機能を追加し、無効な項目が見つかった場合にBinlogサービスを停止し、エラーを報告します[＃687](https://github.com/pingcap/tidb-binlog/pull/687)
-   Drainer [＃684](https://github.com/pingcap/tidb-binlog/pull/684)で使用される特定のロジックを指定するには、 Drainerに`node-id`構成を追加します。

TiDB Lightning

-   2つのチェックサムが同時に実行されているときに`tikv_gc_life_time`元の値に戻らない問題を修正しました[＃218](https://github.com/pingcap/tidb-lightning/pull/218)
-   起動時に構成項目チェック機能を追加し、無効な項目が見つかった場合にBinlogサービスを停止し、エラーを報告します[＃217](https://github.com/pingcap/tidb-lightning/pull/217)

## TiDB アンシブル {#tidb-ansible}

-   ディスクパフォーマンスモニターが秒をミリ秒として扱う単位エラーを修正[＃840](https://github.com/pingcap/tidb-ansible/pull/840)
-   Spark [＃841](https://github.com/pingcap/tidb-ansible/pull/841)に`log4j`設定ファイルを追加する
-   Binlogが有効で Kafka または ZooKeeper が構成されている場合に Prometheus 構成ファイルが間違った形式で生成される問題を修正[＃844](https://github.com/pingcap/tidb-ansible/pull/844)
-   生成されたTiDB構成ファイル[＃850](https://github.com/pingcap/tidb-ansible/pull/850)で構成パラメータ`pessimistic-txn`が省略される問題を修正
-   TiDBダッシュボード[＃853](https://github.com/pingcap/tidb-ansible/pull/853)にメトリックを追加して最適化する
-   TiDBダッシュボード[＃854](https://github.com/pingcap/tidb-ansible/pull/854)の各監視項目の説明を追加する
-   TiDB サマリー ダッシュボードを追加して、クラスターの状態をより適切に表示し、問題をトラブルシューティングします[＃855](https://github.com/pingcap/tidb-ansible/pull/855)
-   TiKVダッシュボード[＃857](https://github.com/pingcap/tidb-ansible/pull/857)のアロケータ統計監視項目を更新します。
-   ノードエクスポーターの警告式[＃860](https://github.com/pingcap/tidb-ansible/pull/860)の単位エラーを修正
-   TiSpark jarパッケージをv2.1.2にアップグレードする[＃862](https://github.com/pingcap/tidb-ansible/pull/862)
-   Ansibleタスク機能[＃867](https://github.com/pingcap/tidb-ansible/pull/867)の説明を更新
-   TiDBダッシュボード[＃874](https://github.com/pingcap/tidb-ansible/pull/874)のローカルリーダーリクエスト監視項目の表現を更新します。
-   概要ダッシュボードの TiKV メモリ監視項目の表現を更新し、監視[＃879](https://github.com/pingcap/tidb-ansible/pull/879)が誤って表示される問題を修正しました。
-   Kafka モード[＃878](https://github.com/pingcap/tidb-ansible/pull/878)でBinlogサポートを削除する
-   `rolling_update.yml`操作[＃887](https://github.com/pingcap/tidb-ansible/pull/887)実行するときにPDがLeaderの転送に失敗する問題を修正
