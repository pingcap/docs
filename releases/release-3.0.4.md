---
title: TiDB 3.0.4 Release Notes
---

# TiDB3.0.4リリースノート {#tidb-3-0-4-release-notes}

発売日：2019年10月8日

TiDBバージョン：3.0.4

TiDB Ansibleバージョン：3.0.4

-   新機能
    -   SQLレベルでパフォーマンスの問題をトラブルシューティングするために`performance_schema.events_statements_summary_by_digest`のシステムテーブルを追加します
    -   TiDBの`SHOW TABLE REGIONS`構文に`WHERE`句を追加します
    -   Reparoに`worker-count`と`txn-batch`の構成アイテムを追加して、回復速度を制御します
-   改善点
    -   分割パフォーマンスを向上させるために、TiKVでバッチリージョン分割コマンドと空の分割コマンドをサポートする
    -   リバーススキャンのパフォーマンスを向上させるために、TiKVでRocksDBの二重リンクリストをサポートする
    -   TiDB Ansibleに2つのパフォーマンスツール`iosnoop`と`funcslower`を追加して、クラスタの状態をより適切に診断します
    -   冗長フィールドを削除して、TiDBの遅いクエリログの出力を最適化します
-   動作の変更
    -   デフォルト値の`txn-local-latches.enable`から`false`を更新して、TiDBでローカルトランザクションの競合をチェックするデフォルトの動作を無効にします
    -   TiDBにグローバルスコープの`tidb_txn_mode`のシステム変数を追加し、ペシミスティックロックの使用を許可します。 TiDBは引き続きデフォルトで楽観的ロックを採用していることに注意してください
    -   低速クエリログの使いやすさを向上させるために、TiDB低速クエリログの`Index_ids`フィールドを`Index_names`に置き換えます
    -   TiDB構成ファイルに`split-region-max-num`パラメーターを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。
    -   SQLの実行がメモリ制限を超えたときにリンクを切断する代わりに、 `Out Of Memory Quota`エラーを返します
    -   誤操作を避けるために、TiDBの列の`AUTO_INCREMENT`属性を削除することを禁止します。この属性を削除するには、 `tidb_allow_remove_auto_inc`システム変数を変更します
-   修正された問題
    -   コメント化されていないTiDB固有の構文`PRE_SPLIT_REGIONS`により、データ複製中にダウンストリームデータベースでエラーが発生する可能性がある問題を修正します
    -   カーソルを使用して`PREPARE` + `EXECUTE`の結果を取得すると、遅いクエリログが正しくないというTiDBの問題を修正します。
    -   隣接する小さなリージョンをマージできないというPDの問題を修正します
    -   アイドル状態のクラスターでのファイル記述子のリークにより、プロセスが長時間実行されるとTiKVプロセスが異常終了する可能性があるというTiKVの問題を修正します。
-   寄稿者

    このリリースを支援してくれたコミュニティからの次の貢献者に感謝します。

    -   [sduzh](https://github.com/sduzh)
    -   [リゼンダ](https://github.com/lizhenda)

## TiDB {#tidb}

-   SQLオプティマイザー
    -   フィードバックによって分割されたときに無効なクエリ範囲が発生する可能性がある問題を修正します[＃12170](https://github.com/pingcap/tidb/pull/12170)
    -   結果に無効なキーが含まれている場合にエラーを返すのではなく、 `SHOW STATS_BUCKETS`ステートメントの返されたエラーを16進数で表示します[＃12094](https://github.com/pingcap/tidb/pull/12094)
    -   クエリに`SLEEP`関数（たとえば、 `select 1 from (select sleep(1)) t;)` ）が含まれている場合、列のプルーニングによってクエリ[＃11953](https://github.com/pingcap/tidb/pull/11953)中に無効な`sleep(1)`が発生する問題を修正します。
    -   クエリがテーブルデータではなく列数のみに関係する場合は、インデックススキャンを使用してIOを下げます[＃12112](https://github.com/pingcap/tidb/pull/12112)
    -   MySQL [＃12100](https://github.com/pingcap/tidb/pull/12100)と互換性があるために、 `use index()`にインデックスが指定されていない場合は、インデックスを使用しないでください。
    -   `CMSketch`の統計の`TopN`のレコードの数を厳密に制限して、ステートメントの数がトランザクションのサイズに関するTiDBの制限を超えているために`ANALYZE`のステートメントが失敗する問題を修正します[＃11914](https://github.com/pingcap/tidb/pull/11914)
    -   `Update`ステートメント[＃12483](https://github.com/pingcap/tidb/pull/12483)に含まれるサブクエリを変換するときに発生したエラーを修正します。
    -   Limit演算子を`IndexLookUpReader`の実行ロジック[＃12378](https://github.com/pingcap/tidb/pull/12378)にプッシュすることにより、 `select ... limit ... offset ...`のステートメントの実行パフォーマンスを最適化します。
-   SQL実行エンジン
    -   `PREPARED`ステートメントが正しく実行されなかった場合にSQLステートメントをログに出力します[＃12191](https://github.com/pingcap/tidb/pull/12191)
    -   `UNIX_TIMESTAMP`関数を使用してパーティショニング[＃12169](https://github.com/pingcap/tidb/pull/12169)を実装する場合は、パーティションプルーニングをサポートします。
    -   `AUTO_INCREMENT`が`MAX int64`と[＃12162](https://github.com/pingcap/tidb/pull/12162)を誤って割り当てたときにエラーが報告されないという問題を修正し`MAX uint64` 。
    -   `SHOW TABLE … REGIONS`および`SHOW TABLE .. INDEX … REGIONS`構文に`WHERE`句を追加します[＃12123](https://github.com/pingcap/tidb/pull/12123)
    -   SQLの実行がメモリ制限を超えたときにリンクを切断する代わりに`Out Of Memory Quota`エラーを返します[＃12127](https://github.com/pingcap/tidb/pull/12127)
    -   `JSON_UNQUOTE`の関数がJSONテキストを処理すると誤った結果が返される問題を修正します[＃11955](https://github.com/pingcap/tidb/pull/11955)
    -   最初の行の`AUTO_INCREMENT`列に値を割り当てるときに`LAST INSERT ID`が正しくないという問題を修正します（たとえば、 `insert into t (pk, c) values (1, 2), (NULL, 3)` ） [＃12002](https://github.com/pingcap/tidb/pull/12002)
    -   `PREPARE`ステートメント[＃12351](https://github.com/pingcap/tidb/pull/12351)で`GROUPBY`解析ルールが正しくない問題を修正します。
    -   ポイントクエリで特権チェックが正しくない問題を修正します[＃12340](https://github.com/pingcap/tidb/pull/12340)
    -   `PREPARE`ステートメントの期間が`sql_type`で、監視レコード[＃12331](https://github.com/pingcap/tidb/pull/12331)に表示されない問題を修正します。
    -   ポイントクエリでのテーブルのエイリアスの使用のサポート（たとえば、 `select * from t tmp where a = "aa"` ） [＃12282](https://github.com/pingcap/tidb/pull/12282)
    -   BITタイプの列に負の数を挿入するときに負の値を符号なしとして処理しないときに発生したエラーを修正します[＃12423](https://github.com/pingcap/tidb/pull/12423)
    -   時間の誤った丸めを修正します（たとえば、 `2019-09-11 11:17:47.999999666`を`2019-09-11 11:17:48`に丸める必要があります） [＃12258](https://github.com/pingcap/tidb/pull/12258)
    -   式ブロックリストの使用法を調整します（たとえば、 `<`は`It`と同等です） [＃11975](https://github.com/pingcap/tidb/pull/11975)
    -   存在しない関数エラーのメッセージにデータベースプレフィックスを追加します（たとえば、 `[expression:1305]FUNCTION test.std_samp does not exist` ） [＃12111](https://github.com/pingcap/tidb/pull/12111)
-   サーバ
    -   最後のステートメントが[＃12180](https://github.com/pingcap/tidb/pull/12180)の場合、遅いクエリログに`Prev_stmt`フィールドを追加して、前のステートメントを出力し`COMMIT` 。
    -   冗長フィールドを削除して、遅いクエリログの出力を最適化します[＃12144](https://github.com/pingcap/tidb/pull/12144)
    -   デフォルト値の`txn-local-latches.enable`を`false`に更新して、TiDB5でローカルトランザクションの競合をチェックするデフォルトの動作を無効にし[＃12095](https://github.com/pingcap/tidb/pull/12095) 。
    -   低速クエリログの使いやすさを向上させるために、TiDB低速クエリログの`Index_ids`フィールドを`Index_names`に置き換えます[#12061](https://github.com/pingcap/tidb/pull/12061)
    -   TiDBにグローバルスコープの`tidb_txn_mode`のシステム変数を追加し、ペシミスティックロック[＃12049](https://github.com/pingcap/tidb/pull/12049)の使用を許可します
    -   低速クエリログに`Backoff`フィールドを追加して、 [＃12335](https://github.com/pingcap/tidb/pull/12335)のコミットフェーズでのバックオフ情報を記録します。
    -   カーソル（たとえば、 `PREPARE stmt1FROM SELECT * FROM t WHERE a > ?; EXECUTE stmt1 USING @variable` ）を使用して`PREPARE` + `EXECUTE`の結果を取得すると、遅いクエリログが正しくないという問題を修正します[＃12392](https://github.com/pingcap/tidb/pull/12392)
    -   サポート`tidb_enable_stmt_summary` 。この機能を有効にすると、 [＃12308](https://github.com/pingcap/tidb/pull/12308)はSQLステートメントをカウントし、システムテーブル35を使用して結果を照会でき`performance_schema.events_statements_summary_by_digest` 。
    -   tikv-clientの一部のログのレベルを調整します（たとえば、 `batchRecvLoop fails`のログレベルを`ERROR`から`INFO`に変更します） [＃12383](https://github.com/pingcap/tidb/pull/12383)
-   DDL
    -   `tidb_allow_remove_auto_inc`の変数を追加します。列の`AUTO INCREMENT`属性の削除は、デフォルトで無効になっています[＃12145](https://github.com/pingcap/tidb/pull/12145)
    -   コメント化されていないTiDB固有の構文`PRE_SPLIT_REGIONS`が、データ複製[＃12120](https://github.com/pingcap/tidb/pull/12120)中にダウンストリームデータベースでエラーを引き起こす可能性があるという問題を修正します。
    -   リージョンの最大許容数が調整可能になるように、構成ファイルに`split-region-max-num`の変数を追加します[＃12097](https://github.com/pingcap/tidb/pull/12079)
    -   リージョンを複数のリージョンに分割することをサポートし、リージョンの分散中のタイムアウトの問題を修正します[＃12343](https://github.com/pingcap/tidb/pull/12343)
    -   2つのインデックスによって参照される`AUTO_INCREMENT`列を含むインデックスの場合に`drop index`ステートメントが失敗する問題を修正します[＃12344](https://github.com/pingcap/tidb/pull/12344)
-   モニター
    -   `connection_transient_failure_count`のモニタリングメトリックを追加して、35の[＃12093](https://github.com/pingcap/tidb/pull/12093)接続エラーの数をカウントし`tikvclient` 。

## TiKV {#tikv}

-   ラフトストア
    -   Raftstoreが空のリージョン[＃5414](https://github.com/tikv/tikv/pull/5414)のキーの数を不正確にカウントする問題を修正します
    -   RocksDBの二重リンクリストをサポートして、リバーススキャンのパフォーマンスを向上させます[＃5368](https://github.com/tikv/tikv/pull/5368)
    -   分割パフォーマンスを向上させるために、バッチリージョン分割コマンドと空の分割コマンドをサポートする[＃5470](https://github.com/tikv/tikv/pull/5470)
-   サーバ
    -   `-V`コマンドの出力形式が2.X3の形式と一致しない問題を修正し[＃5501](https://github.com/tikv/tikv/pull/5501)
    -   Titanを3.0ブランチの最新バージョンにアップグレードする[＃5517](https://github.com/tikv/tikv/pull/5517)
    -   grpcioをv0.4.5にアップグレードします[＃5523](https://github.com/tikv/tikv/pull/5523)
    -   gRPCコアダンプの問題を修正し、共有メモリをサポートしてOOM1を回避し[＃5524](https://github.com/tikv/tikv/pull/5524)
    -   アイドル状態のクラスターでのファイル記述子のリークにより、プロセスが長時間実行されるとTiKVプロセスが異常終了する可能性があるというTiKVの問題を修正します[＃5567](https://github.com/tikv/tikv/pull/5567)
-   保管所
    -   `txn_heart_beat` APIをサポートして、TiDBの悲観的ロックをMySQLの悲観的ロックと可能な限り一致させます[＃5507](https://github.com/tikv/tikv/pull/5507)
    -   一部の状況でポイントクエリのパフォーマンスが低下する問題を修正し[＃5463](https://github.com/tikv/tikv/pull/5463) [＃5495](https://github.com/tikv/tikv/pull/5495)

## PD {#pd}

-   隣接する小さなリージョンをマージできない問題を修正します[＃1726](https://github.com/pingcap/pd/pull/1726)
-   `pd-ctl`のTLS有効化パラメーターが無効である問題を修正します[＃1738](https://github.com/pingcap/pd/pull/1738)
-   PDオペレーターが誤って削除されるというスレッドセーフの問題を修正します[＃1734](https://github.com/pingcap/pd/pull/1734)
-   リージョンシンカー[＃1739](https://github.com/pingcap/pd/pull/1739)のTLSをサポート

## ツール {#tools}

-   TiDB Binlog
    -   Reparoに`worker-count`と`txn-batch`の構成項目を追加して、回復速度を制御します[＃746](https://github.com/pingcap/tidb-binlog/pull/746)
    -   Drainerのメモリ使用量を最適化して、同時実行の効率を高めます[＃737](https://github.com/pingcap/tidb-binlog/pull/737)
-   TiDB Lightning
    -   チェックポイントからデータを再インポートすると、 TiDB Lightningがpanicになる可能性がある問題を修正します[＃237](https://github.com/pingcap/tidb-lightning/pull/237)
    -   `AUTO_INCREMENT`のアルゴリズムを最適化して、 `AUTO_INCREMENT`列がオーバーフローするリスクを減らします[＃227](https://github.com/pingcap/tidb-lightning/pull/227)

## TiDB Ansible {#tidb-ansible}

-   TiSparkをv2.2.0にアップグレードする[＃926](https://github.com/pingcap/tidb-ansible/pull/926)
-   [＃933](https://github.com/pingcap/tidb-ansible/pull/933)構成項目`pessimistic_txn`のデフォルト値を35に更新し`true` 。
-   システムレベルの監視メトリックを`node_exporter`に追加し[＃938](https://github.com/pingcap/tidb-ansible/pull/938)
-   TiDB Ansibleに2つのパフォーマンスツール`iosnoop`と`funcslower`を追加して、クラスタの状態[＃946](https://github.com/pingcap/tidb-ansible/pull/946)をより適切に診断します。
-   パスワードの有効期限が切れるなどの状況での長い待機時間に対処するために、rawモジュールをシェルモジュールに置き換えます[＃949](https://github.com/pingcap/tidb-ansible/pull/949)
-   TiDB構成項目`txn_local_latches`のデフォルト値を`false`に更新します
-   [＃962](https://github.com/pingcap/tidb-ansible/pull/962) [＃969](https://github.com/pingcap/tidb-ansible/pull/963)ボードのモニタリングメトリックとアラートルールを最適化する[＃963](https://github.com/pingcap/tidb-ansible/pull/963)
-   展開および[＃972](https://github.com/pingcap/tidb-ansible/pull/972)の前に構成ファイルを確認してください[＃934](https://github.com/pingcap/tidb-ansible/pull/934)
