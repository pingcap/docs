---
title: TiDB 3.0.4 Release Notes
---

# TiDB 3.0.4 リリースノート {#tidb-3-0-4-release-notes}

発売日：2019年10月8日

TiDB バージョン: 3.0.4

TiDB アンシブル バージョン: 3.0.4

-   新機能
    -   `performance_schema.events_statements_summary_by_digest`システム テーブルを追加して、SQL レベルでパフォーマンスの問題をトラブルシューティングします。
    -   TiDB の`SHOW TABLE REGIONS`構文に`WHERE`句を追加します
    -   Reparoに`worker-count`と`txn-batch`構成項目を追加して、回復速度を制御します
-   改良点
    -   分割パフォーマンスを向上させるために、TiKV でバッチリージョン分割コマンドと空の分割コマンドをサポートします
    -   リバース スキャンのパフォーマンスを向上させるために、TiKV で RocksDB の二重リンク リストをサポートします。
    -   TiDB Ansible に 2 つのパフォーマンス ツール`iosnoop`と`funcslower`を追加して、クラスターの状態をより適切に診断します。
    -   冗長なフィールドを削除することで、TiDB のスロー クエリ ログの出力を最適化します
-   行動の変化
    -   デフォルト値の`txn-local-latches.enable`から`false`を更新して、TiDB でローカル トランザクションの競合をチェックするデフォルトの動作を無効にします
    -   TiDB にグローバル スコープのシステム変数を`tidb_txn_mode`追加し、悲観的ロックの使用を許可します。 TiDB は依然としてデフォルトで楽観的ロックを採用していることに注意してください。
    -   TiDB スロー クエリ ログの`Index_ids`フィールドを`Index_names`に置き換えて、スロー クエリ ログの使いやすさを向上させます
    -   TiDB 構成ファイルに`split-region-max-num`パラメーターを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。
    -   SQL 実行がメモリ制限を超えた場合、リンクを切断する代わりに`Out Of Memory Quota`エラーを返します
    -   誤操作を避けるために、TiDB の列の`AUTO_INCREMENT`属性のドロップを禁止します。この属性を削除するには、システム変数`tidb_allow_remove_auto_inc`を変更します。
-   修正された問題
    -   コメント化されていない TiDB 固有の構文`PRE_SPLIT_REGIONS`が、データ複製中にダウンストリーム データベースでエラーを引き起こす可能性があるという問題を修正します。
    -   TiDB で、カーソルを使用して`PREPARE` + `EXECUTE`の結果を取得すると、スロー クエリ ログが正しくない問題を修正します。
    -   隣接する小さなリージョンをマージできない PD の問題を修正
    -   プロセスが長時間実行されている場合、アイドル クラスタでのファイル記述子のリークにより、TiKV プロセスが異常終了する可能性があるという TiKV の問題を修正します。
-   寄稿者

    このリリースに協力してくれたコミュニティの次の貢献者に感謝します。

    -   [スドゥージ](https://github.com/sduzh)
    -   [リジェンダ](https://github.com/lizhenda)

## TiDB {#tidb}

-   SQL オプティマイザー
    -   フィードバック[#12170](https://github.com/pingcap/tidb/pull/12170)で分割すると、無効なクエリ範囲が返される可能性がある問題を修正します。
    -   結果に無効なキーが含まれている場合にエラーを返すのではなく、 `SHOW STATS_BUCKETS`ステートメントの返されたエラーを[#12094](https://github.com/pingcap/tidb/pull/12094)進数で表示します。
    -   クエリに`SLEEP`関数 (たとえば、 `select 1 from (select sleep(1)) t;)` ) が含まれている場合、クエリ[#11953](https://github.com/pingcap/tidb/pull/11953)で列のプルーニングによって無効な`sleep(1)`が発生する問題を修正します。
    -   クエリがテーブル データではなく列数のみに関係する場合は、インデックス スキャンを使用して IO を削減します[#12112](https://github.com/pingcap/tidb/pull/12112)
    -   MySQL [#12100](https://github.com/pingcap/tidb/pull/12100)との互換性を保つために、 `use index()`でインデックスが指定されていない場合は、インデックスを使用しないでください。
    -   `CMSketch`統計の`TopN`レコードの数を厳密に制限して、ステートメント数がトランザクションのサイズに関する TiDB の制限を超えているために`ANALYZE`ステートメントが失敗するという問題を修正します[#11914](https://github.com/pingcap/tidb/pull/11914)
    -   `Update`ステートメント[#12483](https://github.com/pingcap/tidb/pull/12483)に含まれるサブクエリを変換するときに発生したエラーを修正します。
    -   Limit 演算子を`IndexLookUpReader`実行ロジック[#12378](https://github.com/pingcap/tidb/pull/12378)まで押し下げて、 `select ... limit ... offset ...`ステートメントの実行パフォーマンスを最適化します。
-   SQL 実行エンジン
    -   `PREPARED`ステートメントが誤って実行された場合、ログに SQL ステートメントを出力します[#12191](https://github.com/pingcap/tidb/pull/12191)
    -   `UNIX_TIMESTAMP`関数を使用してパーティショニング[#12169](https://github.com/pingcap/tidb/pull/12169)を実装する場合、パーティションのプルーニングをサポートします。
    -   `AUTO_INCREMENT` `MAX int64`と`MAX uint64` [#12162](https://github.com/pingcap/tidb/pull/12162)を誤って割り当てた場合にエラーが報告されない問題を修正
    -   `SHOW TABLE … REGIONS`と`SHOW TABLE .. INDEX … REGIONS`構文に`WHERE`句を追加します[#12123](https://github.com/pingcap/tidb/pull/12123)
    -   SQL 実行がメモリ制限を超えた場合、リンクを切断する代わりに`Out Of Memory Quota`エラーを返します[#12127](https://github.com/pingcap/tidb/pull/12127)
    -   `JSON_UNQUOTE`関数が JSON テキスト[#11955](https://github.com/pingcap/tidb/pull/11955)を処理すると、誤った結果が返される問題を修正
    -   1 行目の`AUTO_INCREMENT`列に値を代入すると`LAST INSERT ID`が正しくない問題を修正 (例: `insert into t (pk, c) values (1, 2), (NULL, 3)` ) [#12002](https://github.com/pingcap/tidb/pull/12002)
    -   `PREPARE`文[#12351](https://github.com/pingcap/tidb/pull/12351)で`GROUPBY`構文解析規則が正しくない問題を修正
    -   ポイントクエリで権限チェックが正しくない問題を修正[#12340](https://github.com/pingcap/tidb/pull/12340)
    -   `PREPARE`ステートメントの期間が`sql_type`監視レコードに表示されない問題を修正します[#12331](https://github.com/pingcap/tidb/pull/12331)
    -   ポイント クエリでのテーブルのエイリアスの使用をサポート (例: `select * from t tmp where a = "aa"` ) [#12282](https://github.com/pingcap/tidb/pull/12282)
    -   BIT型カラムに負数を挿入する際、負数を符号なしとして扱わないとエラーが発生する問題を修正[#12423](https://github.com/pingcap/tidb/pull/12423)
    -   時間の誤った丸めを修正します (たとえば、 `2019-09-11 11:17:47.999999666` `2019-09-11 11:17:48`に丸める必要があります)。 [#12258](https://github.com/pingcap/tidb/pull/12258)
    -   式ブロックリストの使用法を改善します (たとえば、 `<`は`It`に相当します。) [#11975](https://github.com/pingcap/tidb/pull/11975)
    -   存在しない関数エラーのメッセージにデータベース接頭辞を追加します (例: `[expression:1305]FUNCTION test.std_samp does not exist` ) [#12111](https://github.com/pingcap/tidb/pull/12111)
-   サーバ
    -   スロー クエリ ログに`Prev_stmt`フィールドを追加して、最後のステートメントが`COMMIT` [#12180](https://github.com/pingcap/tidb/pull/12180)のときに前のステートメントを出力します。
    -   冗長なフィールドを削除して、スロー クエリ ログの出力を最適化する[#12144](https://github.com/pingcap/tidb/pull/12144)
    -   デフォルト値の`txn-local-latches.enable`から`false`を更新して、TiDB [#12095](https://github.com/pingcap/tidb/pull/12095)でローカル トランザクションの競合をチェックするデフォルトの動作を無効にします
    -   TiDB スロー クエリ ログの`Index_ids`フィールドを`Index_names`に置き換えて、スロー クエリ ログの使いやすさを向上させます[#12061](https://github.com/pingcap/tidb/pull/12061)
    -   TiDB にグローバル スコープのシステム変数を`tidb_txn_mode`追加し、悲観的ロックの使用を許可する[#12049](https://github.com/pingcap/tidb/pull/12049)
    -   スロー クエリ ログに`Backoff`フィールドを追加して、2PC [#12335](https://github.com/pingcap/tidb/pull/12335)のコミット フェーズでバックオフ情報を記録します。
    -   カーソルを使用して`PREPARE` + `EXECUTE`の結果を取得すると、スロー クエリ ログが正しくない問題を修正 (例: `PREPARE stmt1FROM SELECT * FROM t WHERE a > ?; EXECUTE stmt1 USING @variable` ) [#12392](https://github.com/pingcap/tidb/pull/12392)
    -   サポート`tidb_enable_stmt_summary` 。この機能を有効にすると、TiDB は SQL ステートメントをカウントし、システム テーブルを使用して結果をクエリできます`performance_schema.events_statements_summary_by_digest` [#12308](https://github.com/pingcap/tidb/pull/12308)
    -   tikv-client の一部のログのレベルを調整します (たとえば、ログ レベル`batchRecvLoop fails`を`ERROR`から`INFO`に変更します) [#12383](https://github.com/pingcap/tidb/pull/12383)
-   DDL
    -   `tidb_allow_remove_auto_inc`変数を追加します。列の`AUTO INCREMENT`属性のドロップはデフォルトで無効になっています[#12145](https://github.com/pingcap/tidb/pull/12145)
    -   コメント化されていない TiDB 固有の構文`PRE_SPLIT_REGIONS`が、データ レプリケーション中にダウンストリーム データベースでエラーを引き起こす可能性があるという問題を修正します[#12120](https://github.com/pingcap/tidb/pull/12120)
    -   構成ファイルに`split-region-max-num`変数を追加して、リージョンの最大許容数を調整できるようにします[#12097](https://github.com/pingcap/tidb/pull/12079)
    -   リージョンを複数のリージョンに分割することをサポートし、リージョンの分散中のタイムアウトの問題を修正します[#12343](https://github.com/pingcap/tidb/pull/12343)
    -   `AUTO_INCREMENT`列を含むインデックスが 2 つのインデックスから参照されると、 `drop index`ステートメントが失敗する問題を修正します[#12344](https://github.com/pingcap/tidb/pull/12344)
-   モニター
    -   `connection_transient_failure_count`モニタリング メトリックを追加して、 `tikvclient` [#12093](https://github.com/pingcap/tidb/pull/12093)の gRPC 接続エラーの数をカウントします

## TiKV {#tikv}

-   Raftstore
    -   Raftstore が空のリージョン[#5414](https://github.com/tikv/tikv/pull/5414)のキーの数を不正確にカウントする問題を修正します。
    -   リバース スキャンのパフォーマンスを向上させるために、RocksDB の二重リンク リストをサポートします[#5368](https://github.com/tikv/tikv/pull/5368)
    -   バッチリージョン分割コマンドと空の分割コマンドをサポートして、分割パフォーマンスを向上させます[#5470](https://github.com/tikv/tikv/pull/5470)
-   サーバ
    -   `-V`コマンドの出力形式が 2.X [#5501](https://github.com/tikv/tikv/pull/5501)の形式と一致しない問題を修正
    -   Titan を 3.0 ブランチ[#5517](https://github.com/tikv/tikv/pull/5517)の最新バージョンにアップグレードします。
    -   grpcio を v0.4.5 にアップグレード[#5523](https://github.com/tikv/tikv/pull/5523)
    -   gRPC コアダンプの問題を修正し、共有メモリをサポートして OOM [#5524](https://github.com/tikv/tikv/pull/5524)を回避します
    -   プロセスが長時間実行されている場合、アイドル状態のクラスターでのファイル記述子のリークにより、TiKV プロセスが異常終了する可能性があるという TiKV の問題を修正します[#5567](https://github.com/tikv/tikv/pull/5567)
-   保管所
    -   `txn_heart_beat` TiDB の悲観的ロックを MySQL の悲観的ロックと可能な限り一致させる API をサポートします[#5507](https://github.com/tikv/tikv/pull/5507)
    -   一部の状況でポイント クエリのパフォーマンスが低下する問題を修正します。 [#5495](https://github.com/tikv/tikv/pull/5495) [#5463](https://github.com/tikv/tikv/pull/5463)

## PD {#pd}

-   隣接する小さなリージョンをマージできない問題を修正[#1726](https://github.com/pingcap/pd/pull/1726)
-   `pd-ctl`の TLS 有効化パラメーターが無効であるという問題を修正します[#1738](https://github.com/pingcap/pd/pull/1738)
-   PD 演算子が誤って削除されるというスレッド セーフの問題を修正します[#1734](https://github.com/pingcap/pd/pull/1734)
-   リージョン syncer [#1739](https://github.com/pingcap/pd/pull/1739)の TLS をサポート

## ツール {#tools}

-   TiDBBinlog
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して、回復速度を制御します[#746](https://github.com/pingcap/tidb-binlog/pull/746)
    -   Drainerのメモリ使用量を最適化して同時実行の効率を高める[#737](https://github.com/pingcap/tidb-binlog/pull/737)
-   TiDB Lightning
    -   チェックポイントからデータを再インポートすると、 TiDB Lightning がpanicになる可能性がある問題を修正します[#237](https://github.com/pingcap/tidb-lightning/pull/237)
    -   `AUTO_INCREMENT`のアルゴリズムを最適化して、 `AUTO_INCREMENT`列がオーバーフローするリスクを減らします[#227](https://github.com/pingcap/tidb-lightning/pull/227)

## TiDB アンシブル {#tidb-ansible}

-   TiSpark を v2.2.0 にアップグレードする[#926](https://github.com/pingcap/tidb-ansible/pull/926)
-   TiDB 構成項目のデフォルト値を`pessimistic_txn`から`true` [#933](https://github.com/pingcap/tidb-ansible/pull/933)に更新します
-   `node_exporter` [#938](https://github.com/pingcap/tidb-ansible/pull/938)にさらにシステム レベルのモニタリング メトリックを追加する
-   TiDB Ansible に 2 つのパフォーマンス ツール`iosnoop`と`funcslower`を追加して、クラスターの状態をより適切に診断します[#946](https://github.com/pingcap/tidb-ansible/pull/946)
-   パスワードの有効期限が切れるなどの状況での長い待機時間に対処するために、raw モジュールをシェル モジュールに置き換えます[#949](https://github.com/pingcap/tidb-ansible/pull/949)
-   TiDB 構成項目`txn_local_latches`のデフォルト値を`false`に更新します
-   Grafana ダッシュボードのモニタリング メトリックとアラート ルールを最適化する[#962](https://github.com/pingcap/tidb-ansible/pull/962) [#963](https://github.com/pingcap/tidb-ansible/pull/963) [#969](https://github.com/pingcap/tidb-ansible/pull/963)
-   展開とアップグレードの前に構成ファイルを確認する[#934](https://github.com/pingcap/tidb-ansible/pull/934) [#972](https://github.com/pingcap/tidb-ansible/pull/972)
