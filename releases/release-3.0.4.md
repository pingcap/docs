---
title: TiDB 3.0.4 Release Notes
---

# TiDB 3.0.4 リリースノート {#tidb-3-0-4-release-notes}

発売日：2019年10月8日

TiDB バージョン: 3.0.4

TiDB Ansible バージョン: 3.0.4

-   新機能
    -   SQL レベルでパフォーマンスの問題をトラブルシューティングするには、 `performance_schema.events_statements_summary_by_digest`システム テーブルを追加します。
    -   TiDB の`SHOW TABLE REGIONS`構文に`WHERE`句を追加します。
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御します
-   改善点
    -   TiKV でバッチリージョン分割コマンドと空の分割コマンドをサポートし、分割パフォーマンスを向上させます
    -   TiKV の RocksDB のダブルリンク リストをサポートし、逆スキャンのパフォーマンスを向上させます。
    -   クラスターの状態をより適切に診断するために、TiDB Ansible に 2 つのパフォーマンス ツール`iosnoop`と`funcslower`を追加します。
    -   冗長なフィールドを削除して、TiDB の低速クエリ ログの出力を最適化します。
-   変化した行動
    -   デフォルト値の`txn-local-latches.enable`を`false`に更新して、TiDB でのローカル トランザクションの競合をチェックするデフォルトの動作を無効にします。
    -   TiDB にグローバル スコープの`tidb_txn_mode`システム変数を追加し、悲観的ロックの使用を許可します。 TiDB は依然としてデフォルトで楽観的ロックを採用していることに注意してください。
    -   TiDB スロー クエリ ログの`Index_ids`フィールドを`Index_names`に置き換えて、スロー クエリ ログの使いやすさを向上させます。
    -   TiDB 構成ファイルに`split-region-max-num`パラメータを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。
    -   SQL の実行がメモリ制限を超えた場合、リンクを切断する代わりに`Out Of Memory Quota`エラーを返します。
    -   誤操作を避けるために、TiDB の列の`AUTO_INCREMENT`属性を削除しないようにします。この属性を削除するには、システム変数`tidb_allow_remove_auto_inc`を変更します。
-   修正された問題
    -   コメント化されていない TiDB 固有の構文`PRE_SPLIT_REGIONS`により、データ レプリケーション中にダウンストリーム データベースでエラーが発生する可能性がある問題を修正します。
    -   カーソルを使用して`PREPARE` + `EXECUTE`の結果を取得するときにスロー クエリ ログが正しくないという TiDB の問題を修正しました。
    -   隣接する小さなリージョンをマージできないというPDの問題を修正
    -   プロセスが長時間実行されると、アイドル状態のクラスターでのファイル記述子のリークにより、TiKV プロセスが異常終了する可能性があるという TiKV の問題を修正します。
-   貢献者

    このリリースにご協力いただいたコミュニティの次の貢献者に感謝します。

    -   [スドゥズ](https://github.com/sduzh)
    -   [リジェンダ](https://github.com/lizhenda)

## TiDB {#tidb}

-   SQLオプティマイザー
    -   フィードバック[#12170](https://github.com/pingcap/tidb/pull/12170)で分割すると無効なクエリ範囲が発生する場合がある問題を修正
    -   結果に無効なキーが含まれている場合、エラーを返すのではなく、ステートメント`SHOW STATS_BUCKETS`で返されたエラーを 16 進数で表示します[#12094](https://github.com/pingcap/tidb/pull/12094)
    -   クエリに`SLEEP`関数 (たとえば、 `select 1 from (select sleep(1)) t;)` ) が含まれている場合、列のプルーニングによってクエリ[#11953](https://github.com/pingcap/tidb/pull/11953)中に無効な`sleep(1)`が発生する問題を修正します。
    -   クエリがテーブル データではなく列数のみに関係する場合は、インデックス スキャンを使用して IO を削減します[#12112](https://github.com/pingcap/tidb/pull/12112)
    -   MySQL [#12100](https://github.com/pingcap/tidb/pull/12100)との互換性を保つために、 `use index()`でインデックスが指定されていない場合はインデックスを使用しないでください。
    -   `TopN`数が TiDB のトランザクション サイズ制限を超えているため、ステートメント`ANALYZE`が失敗する問題を修正するために、統計`CMSketch` 1 レコードの数を厳密に制限します[#11914](https://github.com/pingcap/tidb/pull/11914)
    -   `Update`ステートメント[#12483](https://github.com/pingcap/tidb/pull/12483)に含まれるサブクエリの変換時に発生したエラーを修正
    -   Limit 演算子を`IndexLookUpReader`実行ロジックにプッシュダウンすることで、 `select ... limit ... offset ...`ステートメントの実行パフォーマンスを最適化します[#12378](https://github.com/pingcap/tidb/pull/12378)
-   SQL実行エンジン
    -   `PREPARED`ステートメントが誤って実行された場合、ログに SQL ステートメントを出力します[#12191](https://github.com/pingcap/tidb/pull/12191)
    -   `UNIX_TIMESTAMP`関数を使用してパーティショニング[#12169](https://github.com/pingcap/tidb/pull/12169)を実装する場合、パーティション プルーニングをサポートします。
    -   `AUTO_INCREMENT` `MAX int64`と`MAX uint64`誤って割り当てた場合にエラーが報告されない問題を修正[#12162](https://github.com/pingcap/tidb/pull/12162)
    -   `SHOW TABLE … REGIONS`および`SHOW TABLE .. INDEX … REGIONS`構文に`WHERE`句を追加します[#12123](https://github.com/pingcap/tidb/pull/12123)
    -   SQL の実行がメモリ制限[#12127](https://github.com/pingcap/tidb/pull/12127)を超えた場合、リンクを切断する代わりに`Out Of Memory Quota`エラーを返します。
    -   `JSON_UNQUOTE`関数が JSON テキスト[#11955](https://github.com/pingcap/tidb/pull/11955)を処理すると、誤った結果が返される問題を修正
    -   最初の行の`AUTO_INCREMENT`列に値を割り当てるときに`LAST INSERT ID`が正しくない問題を修正します (たとえば、 `insert into t (pk, c) values (1, 2), (NULL, 3)` ) [#12002](https://github.com/pingcap/tidb/pull/12002)
    -   `PREPARE`ステートメント`GROUPBY`の解析ルールが正しくない問題を修正します[#12351](https://github.com/pingcap/tidb/pull/12351)
    -   ポイントクエリ[#12340](https://github.com/pingcap/tidb/pull/12340)における権限チェックが正しくない問題を修正
    -   監視レコード[#12331](https://github.com/pingcap/tidb/pull/12331)にステートメント`PREPARE`の`sql_type`による期間が表示されない問題を修正
    -   ポイント クエリでのテーブルのエイリアスの使用をサポート (例: `select * from t tmp where a = "aa"` ) [#12282](https://github.com/pingcap/tidb/pull/12282)
    -   BIT型列[#12423](https://github.com/pingcap/tidb/pull/12423)に負の数値を挿入する際、負の値を符号なしとして扱えない場合に発生するエラーを修正
    -   時刻の誤った丸めを修正します (たとえば、 `2019-09-11 11:17:47.999999666` `2019-09-11 11:17:48`に四捨五入する必要があります) [#12258](https://github.com/pingcap/tidb/pull/12258)
    -   式ブロックリストの使用法を調整します (たとえば、 `<`は`It`と同等です)。 [#11975](https://github.com/pingcap/tidb/pull/11975)
    -   存在しない関数エラーのメッセージにデータベース接頭辞を追加します (例: `[expression:1305]FUNCTION test.std_samp does not exist` ) [#12111](https://github.com/pingcap/tidb/pull/12111)
-   サーバ
    -   スロークエリログに`Prev_stmt`フィールドを追加して、最後のステートメントが`COMMIT` [#12180](https://github.com/pingcap/tidb/pull/12180)の場合に前のステートメントを出力します。
    -   冗長なフィールドを削除して、低速クエリ ログの出力を最適化します[#12144](https://github.com/pingcap/tidb/pull/12144)
    -   TiDB [#12095](https://github.com/pingcap/tidb/pull/12095)でローカル トランザクションの競合をチェックするデフォルトの動作を無効にするには、デフォルト値の`txn-local-latches.enable`を`false`に更新します。
    -   TiDB スロー クエリ ログの`Index_ids`フィールドを`Index_names`に置き換えて、スロー クエリ ログの使いやすさを向上させます[#12061](https://github.com/pingcap/tidb/pull/12061)
    -   TiDB にグローバル スコープのシステム変数`tidb_txn_mode`を追加し、悲観的ロック[#12049](https://github.com/pingcap/tidb/pull/12049)の使用を許可します。
    -   スロー クエリ ログに`Backoff`フィールドを追加して、2PC [#12335](https://github.com/pingcap/tidb/pull/12335)のコミット フェーズでバックオフ情報を記録します。
    -   カーソルを使用して`PREPARE` + `EXECUTE`の結果を取得する場合 (例: `PREPARE stmt1FROM SELECT * FROM t WHERE a > ?; EXECUTE stmt1 USING @variable` )、スロー クエリのログが正しくない問題を修正します[#12392](https://github.com/pingcap/tidb/pull/12392)
    -   サポート`tidb_enable_stmt_summary` ．この機能を有効にすると、TiDB は SQL ステートメントをカウントし、システム テーブルを使用して結果をクエリできるようになります`performance_schema.events_statements_summary_by_digest` [#12308](https://github.com/pingcap/tidb/pull/12308)
    -   tikv-client の一部のログのレベルを調整します (たとえば、ログ レベル`batchRecvLoop fails`を`ERROR`から`INFO`に変更します) [#12383](https://github.com/pingcap/tidb/pull/12383)
-   DDL
    -   `tidb_allow_remove_auto_inc`変数を追加します。列の`AUTO INCREMENT`属性の削除はデフォルトで無効になっています[#12145](https://github.com/pingcap/tidb/pull/12145)
    -   コメント化されていない TiDB 固有の構文`PRE_SPLIT_REGIONS`により、データ レプリケーション中にダウンストリーム データベースでエラーが発生する可能性がある問題を修正します[#12120](https://github.com/pingcap/tidb/pull/12120)
    -   設定ファイルに`split-region-max-num`変数を追加して、許容されるリージョンの最大数を調整できるようにします[#12097](https://github.com/pingcap/tidb/pull/12079)
    -   リージョンを複数のリージョンに分割することをサポートし、リージョンスキャッタリング中のタイムアウトの問題を修正します[#12343](https://github.com/pingcap/tidb/pull/12343)
    -   2 つのインデックスによって参照される`AUTO_INCREMENT`列を含むインデックスが存在する場合、 `drop index`ステートメントが失敗する問題を修正します[#12344](https://github.com/pingcap/tidb/pull/12344)
-   モニター
    -   `connection_transient_failure_count`監視メトリクスを追加して、 `tikvclient` [#12093](https://github.com/pingcap/tidb/pull/12093)の gRPC 接続エラーの数をカウントします。

## TiKV {#tikv}

-   Raftstore
    -   Raftstore が空のリージョン[#5414](https://github.com/tikv/tikv/pull/5414)のキーの数を不正確にカウントする問題を修正
    -   RocksDB のダブルリンクリストをサポートし、逆スキャン[#5368](https://github.com/tikv/tikv/pull/5368)のパフォーマンスを向上させます。
    -   バッチリージョン分割コマンドと空の分割コマンドをサポートして、分割パフォーマンスを向上させます[#5470](https://github.com/tikv/tikv/pull/5470)
-   サーバ
    -   `-V`コマンドの出力形式が2.X [#5501](https://github.com/tikv/tikv/pull/5501)の形式と一致しない問題を修正
    -   Titan を 3.0 ブランチ[#5517](https://github.com/tikv/tikv/pull/5517)の最新バージョンにアップグレードします。
    -   grpcio を v0.4.5 にアップグレードする[#5523](https://github.com/tikv/tikv/pull/5523)
    -   gRPC コアダンプの問題を修正し、OOM [#5524](https://github.com/tikv/tikv/pull/5524)を回避するために共有メモリをサポートします。
    -   アイドル状態のクラスターでのファイル記述子のリークにより、プロセスが長時間実行されると TiKV プロセスが異常終了する可能性があるという TiKV の問題を修正します[#5567](https://github.com/tikv/tikv/pull/5567)
-   ストレージ
    -   `txn_heart_beat` TiDB の悲観的ロックを MySQL の悲観的ロックと可能な限り一致させるための API をサポートします[#5507](https://github.com/tikv/tikv/pull/5507)
    -   一部の状況でポイントクエリのパフォーマンスが低下する問題を修正[#5495](https://github.com/tikv/tikv/pull/5495) [#5463](https://github.com/tikv/tikv/pull/5463)

## PD {#pd}

-   隣接する小さなリージョンを結合できない問題を修正[#1726](https://github.com/pingcap/pd/pull/1726)
-   `pd-ctl`のTLS有効化パラメータが無効である問題を修正[#1738](https://github.com/pingcap/pd/pull/1738)
-   PD オペレーターが誤って削除されるというスレッド セーフティの問題を修正します[#1734](https://github.com/pingcap/pd/pull/1734)
-   リージョン同期器[#1739](https://github.com/pingcap/pd/pull/1739)の TLS をサポート

## ツール {#tools}

-   TiDBBinlog
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御する[#746](https://github.com/pingcap/tidb-binlog/pull/746)
    -   Drainerのメモリ使用量を最適化し、同時実行の効率を向上[#737](https://github.com/pingcap/tidb-binlog/pull/737)
-   TiDB Lightning
    -   チェックポイントからデータを再インポートすると、 TiDB Lightning がpanicを引き起こす可能性がある問題を修正します[#237](https://github.com/pingcap/tidb-lightning/pull/237)
    -   `AUTO_INCREMENT`のアルゴリズムを最適化して`AUTO_INCREMENT`列がオーバーフローするリスクを軽減します[#227](https://github.com/pingcap/tidb-lightning/pull/227)

## TiDB Ansible {#tidb-ansible}

-   TiSpark を v2.2.0 にアップグレードする[#926](https://github.com/pingcap/tidb-ansible/pull/926)
-   TiDB 構成項目のデフォルト値を`pessimistic_txn`から`true`に更新します[#933](https://github.com/pingcap/tidb-ansible/pull/933)
-   システムレベルの監視メトリクスを`node_exporter` [#938](https://github.com/pingcap/tidb-ansible/pull/938)に追加します
-   TiDB Ansible に 2 つのパフォーマンス ツール`iosnoop`と`funcslower`を追加して、クラスターの状態をより適切に診断します[#946](https://github.com/pingcap/tidb-ansible/pull/946)
-   パスワードの有効期限が切れた場合などの長い待ち時間に対処するために、raw モジュールをシェル モジュールに置き換えます[#949](https://github.com/pingcap/tidb-ansible/pull/949)
-   TiDB 構成項目`txn_local_latches`のデフォルト値を`false`に更新します。
-   Grafana ダッシュボードの監視メトリクスとアラート ルールを最適化する[#962](https://github.com/pingcap/tidb-ansible/pull/962) [#963](https://github.com/pingcap/tidb-ansible/pull/963) [#969](https://github.com/pingcap/tidb-ansible/pull/963)
-   導入およびアップグレードの前に構成ファイルを確認してください[#934](https://github.com/pingcap/tidb-ansible/pull/934) [#972](https://github.com/pingcap/tidb-ansible/pull/972)
