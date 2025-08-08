---
title: TiDB 3.0.4 Release Notes
summary: TiDB 3.0.4は2019年10月8日にリリースされました。SQLパフォーマンスの問題をトラブルシューティングするためのシステムテーブル、分割パフォーマンスと逆スキャンの改善、スロークエリログとデータレプリケーションに関連する問題の修正などの新機能が含まれています。また、コミュニティからの貢献と、TiDB、TiKV、PD、TiDB Ansibleのアップデートも含まれています。
---

# TiDB 3.0.4 リリースノート {#tidb-3-0-4-release-notes}

発売日：2019年10月8日

TiDB バージョン: 3.0.4

TiDB Ansible バージョン: 3.0.4

-   新機能
    -   SQL レベルでパフォーマンスの問題をトラブルシューティングするために`performance_schema.events_statements_summary_by_digest`システム テーブルを追加します。
    -   TiDBの`SHOW TABLE REGIONS`構文に`WHERE`句を追加する
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御します
-   改善点
    -   TiKV でバッチリージョン分割コマンドと空分割コマンドをサポートし、分割パフォーマンスを向上
    -   TiKV で RocksDB の二重リンクリストをサポートし、逆スキャンのパフォーマンスを向上
    -   クラスタの状態をより適切に診断するために、TiDB Ansibleに2つのperfツール`iosnoop`と`funcslower`追加します。
    -   冗長なフィールドを削除して、TiDB のスロークエリログの出力を最適化します。
-   行動の変化
    -   デフォルト値の`txn-local-latches.enable`を`false`に更新して、TiDB のローカルトランザクションの競合をチェックするデフォルトの動作を無効にします。
    -   TiDBにグローバルスコープのシステム変数を`tidb_txn_mode`追加し、悲観的ロックの使用を許可します。ただし、TiDBはデフォルトで依然として楽観的ロックを採用していることに注意してください。
    -   TiDB スロー クエリ ログの`Index_ids`フィールドを`Index_names`に置き換えて、スロー クエリ ログの使いやすさを向上させます。
    -   TiDB構成ファイルに`split-region-max-num`パラメータを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。
    -   SQL実行がメモリ制限を超えたときにリンクを切断する代わりに`Out Of Memory Quota`エラーを返します
    -   誤操作を避けるため、TiDBの列の`AUTO_INCREMENT`の属性の削除を禁止します。この属性を削除するには、 `tidb_allow_remove_auto_inc`のシステム変数を変更します。
-   修正された問題
    -   コメントされていない TiDB 固有の構文`PRE_SPLIT_REGIONS`データ複製中に下流データベースでエラーを引き起こす可能性がある問題を修正しました。
    -   カーソルを使用して`PREPARE` + `EXECUTE`の結果を取得するときに、遅いクエリログが正しくないという TiDB の問題を修正しました。
    -   PDで隣接する小さな領域を結合できない問題を修正
    -   TiKV の問題を修正しました。アイドル状態のクラスターでファイル記述子がリークすると、プロセスの実行時間が長くなると TiKV プロセスが異常終了することがあります。
-   寄稿者

    このリリースにご協力いただいたコミュニティの以下の貢献者の方々に感謝申し上げます。

    -   [スドゥズ](https://github.com/sduzh)
    -   [リジェンダ](https://github.com/lizhenda)

## TiDB {#tidb}

-   SQLオプティマイザー
    -   フィードバック[＃12170](https://github.com/pingcap/tidb/pull/12170)で分割すると無効なクエリ範囲が生成される可能性がある問題を修正しました
    -   結果に無効なキー[＃12094](https://github.com/pingcap/tidb/pull/12094)が含まれている場合はエラーを返すのではなく、 `SHOW STATS_BUCKETS`のステートメントの返されたエラーを16進数で表示します。
    -   クエリに`SLEEP`関数（たとえば`select 1 from (select sleep(1)) t;)` ）が含まれている場合、列プルーニングによってクエリ[＃11953](https://github.com/pingcap/tidb/pull/11953)中に無効な`sleep(1)`発生する問題を修正しました。
    -   クエリがテーブルデータではなく列数のみに関係する場合は、インデックススキャンを使用してIOを削減します[＃12112](https://github.com/pingcap/tidb/pull/12112)
    -   MySQL [＃12100](https://github.com/pingcap/tidb/pull/12100)との互換性を保つために、 `use index()`でインデックスが指定されていない場合はインデックスを使用しない
    -   `CMSketch`統計の`TopN`レコードの数を厳密に制限して、ステートメント数が TiDB のトランザクション[＃11914](https://github.com/pingcap/tidb/pull/11914)のサイズ制限を超えたために`ANALYZE`ステートメントが失敗する問題を修正します。
    -   `Update`文[＃12483](https://github.com/pingcap/tidb/pull/12483)に含まれるサブクエリを変換するときに発生したエラーを修正します
    -   Limit演算子を`IndexLookUpReader`実行ロジック[＃12378](https://github.com/pingcap/tidb/pull/12378)にプッシュすることで、 `select ... limit ... offset ...`文の実行パフォーマンスを最適化します。
-   SQL実行エンジン
    -   `PREPARED`文が正しく実行されなかった場合に、SQL文をログに出力します[＃12191](https://github.com/pingcap/tidb/pull/12191)
    -   `UNIX_TIMESTAMP`関数を使用してパーティショニング[＃12169](https://github.com/pingcap/tidb/pull/12169)実装する場合にパーティション プルーニングをサポートする
    -   `AUTO_INCREMENT` `MAX int64`と`MAX uint64`誤って割り当てた場合にエラーが報告されない問題を修正しました[＃12162](https://github.com/pingcap/tidb/pull/12162)
    -   `SHOW TABLE … REGIONS`と`SHOW TABLE .. INDEX … REGIONS`構文に`WHERE`節を追加する[＃12123](https://github.com/pingcap/tidb/pull/12123)
    -   SQL実行がメモリ制限[＃12127](https://github.com/pingcap/tidb/pull/12127)を超えたときにリンクを切断する代わりに`Out Of Memory Quota`エラーを返す
    -   `JSON_UNQUOTE`関数がJSONテキスト[＃11955](https://github.com/pingcap/tidb/pull/11955)を処理するときに誤った結果が返される問題を修正
    -   最初の行の`AUTO_INCREMENT`列に値を割り当てるときに`LAST INSERT ID`間違っているという問題を修正しました（たとえば、 `insert into t (pk, c) values (1, 2), (NULL, 3)` ） [＃12002](https://github.com/pingcap/tidb/pull/12002)
    -   `PREPARE`文[＃12351](https://github.com/pingcap/tidb/pull/12351)の`GROUPBY`解析ルールが間違っている問題を修正
    -   ポイントクエリ[＃12340](https://github.com/pingcap/tidb/pull/12340)で権限チェックが正しく行われない問題を修正
    -   監視レコード[＃12331](https://github.com/pingcap/tidb/pull/12331)に、ステートメント`PREPARE`の`sql_type`による期間が表示されない問題を修正しました。
    -   ポイントクエリ内のテーブルの別名の使用をサポートします（例： `select * from t tmp where a = "aa"` ） [＃12282](https://github.com/pingcap/tidb/pull/12282)
    -   BIT 型の列[＃12423](https://github.com/pingcap/tidb/pull/12423)に負の数を挿入するときに負の値を符号なしとして処理しない場合に発生するエラーを修正しました。
    -   時間の誤った丸めを修正します（たとえば、 `2019-09-11 11:17:47.999999666` `2019-09-11 11:17:48`に丸められる必要があります） [＃12258](https://github.com/pingcap/tidb/pull/12258)
    -   表現ブロックリストの使い方を改良します（例えば、 `<` `It`に相当します） [＃11975](https://github.com/pingcap/tidb/pull/11975)
    -   存在しない関数エラーのメッセージにデータベースプレフィックスを追加します（例： `[expression:1305]FUNCTION test.std_samp does not exist` ） [＃12111](https://github.com/pingcap/tidb/pull/12111)
-   サーバ
    -   最後のステートメントが`COMMIT` [＃12180](https://github.com/pingcap/tidb/pull/12180)ときに前のステートメントを出力するために、スロークエリログに`Prev_stmt`フィールドを追加します。
    -   冗長なフィールドを削除してスロークエリログの出力を最適化する[＃12144](https://github.com/pingcap/tidb/pull/12144)
    -   TiDB [＃12095](https://github.com/pingcap/tidb/pull/12095)のローカルトランザクションの競合をチェックするデフォルトの動作を無効にするには、デフォルト値の`txn-local-latches.enable`を`false`に更新します。
    -   TiDB スロークエリログの`Index_ids`フィールドを`Index_names`に置き換えて、スロークエリログ[＃12061](https://github.com/pingcap/tidb/pull/12061)の使いやすさを向上させます。
    -   TiDBにグローバルスコープのシステム変数`tidb_txn_mode`追加し、悲観的ロック[＃12049](https://github.com/pingcap/tidb/pull/12049)使用を許可します。
    -   スロークエリログに`Backoff`フィールドを追加して、2PC [＃12335](https://github.com/pingcap/tidb/pull/12335)のコミットフェーズのバックオフ情報を記録します。
    -   カーソルを使用して`PREPARE` + `EXECUTE`の結果を取得するときにスロークエリログが正しくない問題を修正しました（たとえば、 `PREPARE stmt1FROM SELECT * FROM t WHERE a > ?; EXECUTE stmt1 USING @variable` ） [＃12392](https://github.com/pingcap/tidb/pull/12392)
    -   サポート`tidb_enable_stmt_summary`この機能を有効にすると、TiDBはSQL文をカウントし、その結果はシステムテーブル`performance_schema.events_statements_summary_by_digest` [＃12308](https://github.com/pingcap/tidb/pull/12308)を使用して照会できます。
    -   tikv-client のログレベルを調整します（たとえば、ログレベル`batchRecvLoop fails`を`ERROR`から`INFO`に変更します） [＃12383](https://github.com/pingcap/tidb/pull/12383)
-   DDL
    -   `tidb_allow_remove_auto_inc`変数を追加します。列の`AUTO INCREMENT`属性の削除はデフォルトで無効になっています[＃12145](https://github.com/pingcap/tidb/pull/12145)
    -   コメントされていない TiDB 固有の構文`PRE_SPLIT_REGIONS`データ複製[＃12120](https://github.com/pingcap/tidb/pull/12120)中に下流データベースでエラーを引き起こす可能性がある問題を修正しました
    -   設定ファイルに`split-region-max-num`変数を追加して、リージョンの最大許容数を調整できるようにします[＃12097](https://github.com/pingcap/tidb/pull/12079)
    -   リージョンを複数のリージョンに分割する機能をサポートし、リージョン分散中のタイムアウトの問題を修正しました[＃12343](https://github.com/pingcap/tidb/pull/12343)
    -   2つのインデックス[＃12344](https://github.com/pingcap/tidb/pull/12344)によって参照される`AUTO_INCREMENT`列を含むインデックスの場合に`drop index`文が失敗する問題を修正
-   モニター
    -   `tikvclient` [＃12093](https://github.com/pingcap/tidb/pull/12093)の gRPC 接続エラーの数をカウントする`connection_transient_failure_count`監視メトリックを追加します。

## TiKV {#tikv}

-   Raftstore
    -   Raftstore が空のリージョン[＃5414](https://github.com/tikv/tikv/pull/5414)のキーの数を不正確にカウントする問題を修正しました
    -   RocksDB の二重リンクリストをサポートし、逆スキャン[＃5368](https://github.com/tikv/tikv/pull/5368)のパフォーマンスを向上しました。
    -   分割パフォーマンスを向上させるために、バッチリージョン分割コマンドと空分割コマンドをサポートします[＃5470](https://github.com/tikv/tikv/pull/5470)
-   サーバ
    -   `-V`コマンドの出力形式が2.X [＃5501](https://github.com/tikv/tikv/pull/5501)の形式と一致しない問題を修正
    -   Titanを3.0ブランチ[＃5517](https://github.com/tikv/tikv/pull/5517)の最新バージョンにアップグレードします
    -   grpcio を v0.4.5 [＃5523](https://github.com/tikv/tikv/pull/5523)にアップグレード
    -   gRPC コアダンプの問題を修正し、OOM [＃5524](https://github.com/tikv/tikv/pull/5524)回避するために共有メモリをサポートします。
    -   TiKV の問題を修正しました。アイドル状態のクラスターでファイル記述子がリークすると、プロセスの実行時間が長くなると TiKV プロセスが異常終了することがあります[＃5567](https://github.com/tikv/tikv/pull/5567)
-   ストレージ
    -   TiDBの悲観的ロックをMySQLのものと可能な限り一致させるために`txn_heart_beat` APIをサポートする[＃5507](https://github.com/tikv/tikv/pull/5507)
    -   ポイントクエリのパフォーマンスが一部の状況で低下する問題を修正[＃5495](https://github.com/tikv/tikv/pull/5495) [＃5463](https://github.com/tikv/tikv/pull/5463)

## PD {#pd}

-   隣接する小さな領域を結合できない問題を修正[＃1726](https://github.com/pingcap/pd/pull/1726)
-   `pd-ctl`のTLS有効化パラメータが無効である問題を修正[＃1738](https://github.com/pingcap/pd/pull/1738)
-   PD演算子が誤って削除されるスレッドセーフの問題を修正[＃1734](https://github.com/pingcap/pd/pull/1734)
-   リージョンシンカー[＃1739](https://github.com/pingcap/pd/pull/1739)のTLSをサポート

## ツール {#tools}

-   TiDBBinlog
    -   Reparoの設定項目`worker-count`と`txn-batch`追加して回復速度[＃746](https://github.com/pingcap/tidb-binlog/pull/746)制御します
    -   Drainerのメモリ使用量を最適化し、同時実行の効率を高めます[＃737](https://github.com/pingcap/tidb-binlog/pull/737)
-   TiDB Lightning
    -   チェックポイントからデータを再インポートするとTiDB Lightning がpanicを起こす可能性がある問題を修正[＃237](https://github.com/pingcap/tidb-lightning/pull/237)
    -   `AUTO_INCREMENT`のアルゴリズムを最適化して、 `AUTO_INCREMENT`列[＃227](https://github.com/pingcap/tidb-lightning/pull/227)のオーバーフローのリスクを軽減します。

## TiDB アンシブル {#tidb-ansible}

-   TiSparkをv2.2.0 [＃926](https://github.com/pingcap/tidb-ansible/pull/926)にアップグレード
-   TiDB構成項目`pessimistic_txn`のデフォルト値を`true` [＃933](https://github.com/pingcap/tidb-ansible/pull/933)に更新します。
-   `node_exporter` [＃938](https://github.com/pingcap/tidb-ansible/pull/938)にシステムレベルの監視メトリックを追加します
-   クラスタの状態をより適切に診断するために、TiDB Ansibleに2つのperfツール`iosnoop`と`funcslower`追加します[＃946](https://github.com/pingcap/tidb-ansible/pull/946)
-   パスワードの有効期限が切れた場合などに発生する長い待機時間に対処するために、rawモジュールをシェルモジュールに置き換えます[＃949](https://github.com/pingcap/tidb-ansible/pull/949)
-   TiDB構成項目`txn_local_latches`のデフォルト値を`false`に更新します
-   Grafanaダッシュボードの監視メトリックとアラートルールを最適化する[＃962](https://github.com/pingcap/tidb-ansible/pull/962) [＃963](https://github.com/pingcap/tidb-ansible/pull/963) [＃969](https://github.com/pingcap/tidb-ansible/pull/963)
-   展開およびアップグレードの前に構成ファイルを確認する[＃934](https://github.com/pingcap/tidb-ansible/pull/934) [＃972](https://github.com/pingcap/tidb-ansible/pull/972)
