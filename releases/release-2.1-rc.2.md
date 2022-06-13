---
title: TiDB 2.1 RC2 Release Notes
---

# TiDB2.1RC2リリースノート {#tidb-2-1-rc2-release-notes}

2018年9月14日、TiDB2.1RC2がリリースされました。このリリースでは、TiDB 2.1 RC1と比較して、安定性、SQLオプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   次世代プランナー[＃7543](https://github.com/pingcap/tidb/pull/7543)の提案を提案する
    -   定数伝播の最適化ルールを改善する[＃7276](https://github.com/pingcap/tidb/pull/7276)
    -   `Range`のコンピューティングロジックを拡張して、複数の`IN`または`EQUAL`の条件を同時に処理できるようにします[＃7577](https://github.com/pingcap/tidb/pull/7577)
    -   `Range`が空の場合に`TableScan`の推定結果が正しくない問題を修正します[＃7583](https://github.com/pingcap/tidb/pull/7583)
    -   `UPDATE`ステートメント[＃7586](https://github.com/pingcap/tidb/pull/7586)の`PointGet`演算子をサポートします
    -   一部の条件で`FirstRow`集計関数を実行するプロセス中のパニックの問題を修正します[＃7624](https://github.com/pingcap/tidb/pull/7624)
-   SQL実行エンジン
    -   `HashJoin`オペレーターがエラー[＃7554](https://github.com/pingcap/tidb/pull/7554)に遭遇したときに発生する可能性のある`DataRace`の問題を修正します
    -   `HashJoin`オペレーターに内部テーブルを読み取らせ、同時にハッシュテーブルを作成します[＃7544](https://github.com/pingcap/tidb/pull/7544)
    -   ハッシュ集計演算子のパフォーマンスを最適化する[＃7541](https://github.com/pingcap/tidb/pull/7541)
    -   結合演算子のパフォーマンスを最適化[＃7433](https://github.com/pingcap/tidb/pull/7433) [＃7493](https://github.com/pingcap/tidb/pull/7493)
    -   結合順序が変更されたときに`UPDATE JOIN`の結果が正しくない問題を修正します[＃7571](https://github.com/pingcap/tidb/pull/7571)
    -   チャンクのイテレータ[＃7585](https://github.com/pingcap/tidb/pull/7585)のパフォーマンスを向上させる
-   統計
    -   自動分析作業が統計を繰り返し分析する問題を修正します[＃7550](https://github.com/pingcap/tidb/pull/7550)
    -   統計の変更がない場合に発生する統計更新エラーを修正します[＃7530](https://github.com/pingcap/tidb/pull/7530)
    -   `Analyze`のリクエストを作成するときは、RC分離レベルと低い優先度を使用します[＃7496](https://github.com/pingcap/tidb/pull/7496)
    -   1日の特定の期間の統計自動分析の有効化をサポート[＃7570](https://github.com/pingcap/tidb/pull/7570)
    -   統計情報をログに記録する際のパニックの問題を修正する[＃7588](https://github.com/pingcap/tidb/pull/7588)
    -   `ANALYZE TABLE WITH BUCKETS`ステートメント[＃7619](https://github.com/pingcap/tidb/pull/7619)を使用したヒストグラム内のバケット数の構成のサポート
    -   空のヒストグラムを更新するときのパニックの問題を修正します[＃7640](https://github.com/pingcap/tidb/pull/7640)
    -   統計情報を使用して`information_schema.tables.data_length`を更新します[＃7657](https://github.com/pingcap/tidb/pull/7657)
-   サーバ
    -   トレース関連の依存関係を追加する[＃7532](https://github.com/pingcap/tidb/pull/7532)
    -   [＃7512](https://github.com/pingcap/tidb/pull/7512)の`mutex profile`つの機能を有効にする
    -   `Admin`ステートメントには`Super_priv`特権[＃7486](https://github.com/pingcap/tidb/pull/7486)が必要です
    -   `Drop`の重要なシステムテーブルへのユーザーの禁止[＃7471](https://github.com/pingcap/tidb/pull/7471)
    -   `juju/errors`から[＃7151](https://github.com/pingcap/tidb/pull/7151)に切り替え`pkg/errors`
    -   SQLトレース[＃7016](https://github.com/pingcap/tidb/pull/7016)の機能プロトタイプを完成させる
    -   ゴルーチンプールを削除する[＃7564](https://github.com/pingcap/tidb/pull/7564)
    -   `USER1`信号[＃7587](https://github.com/pingcap/tidb/pull/7587)を使用したゴルーチン情報の表示をサポートします。
    -   TiDBの起動中に内部SQLを高優先度に設定する[＃7616](https://github.com/pingcap/tidb/pull/7616)
    -   異なるラベルを使用して、メトリックの監視で内部SQLとユーザーSQLをフィルタリングします[＃7631](https://github.com/pingcap/tidb/pull/7631)
    -   先週の遅いクエリの上位30件をTiDBサーバーに保存する[＃7646](https://github.com/pingcap/tidb/pull/7646)
    -   TiDBクラスタのグローバルシステムタイムゾーンを設定する提案を提出する[＃7656](https://github.com/pingcap/tidb/pull/7656)
    -   「GCの有効期間がトランザクション期間より短い」というエラーメッセージを充実させる[＃7658](https://github.com/pingcap/tidb/pull/7658)
    -   TiDBクラスタの起動時にグローバルシステムのタイムゾーンを設定する[＃7638](https://github.com/pingcap/tidb/pull/7638)
-   互換性
    -   `Year`タイプ[＃7542](https://github.com/pingcap/tidb/pull/7542)の符号なしフラグを追加します
    -   `Prepare`モード`Execute`で`Year`タイプの結果の長さを構成する問題を修正し[＃7525](https://github.com/pingcap/tidb/pull/7525)
    -   `Prepare` `Execute`でゼロタイムスタンプを挿入する問題を修正します[＃7506](https://github.com/pingcap/tidb/pull/7506)
    -   整数除算[＃7492](https://github.com/pingcap/tidb/pull/7492)のエラー処理の問題を修正しました
    -   `ComStmtSendLongData`を処理するときの互換性の問題を修正し[＃7485](https://github.com/pingcap/tidb/pull/7485)
    -   文字列を整数[＃7483](https://github.com/pingcap/tidb/pull/7483)に変換するプロセス中のエラー処理の問題を修正します
    -   `information_schema.columns_in_table`表[＃7463](https://github.com/pingcap/tidb/pull/7463)の値の精度を最適化する
    -   MariaDBクライアントを使用して文字列型のデータを書き込んだり更新したりするときの互換性の問題を修正します[＃7573](https://github.com/pingcap/tidb/pull/7573)
    -   戻り値[＃7600](https://github.com/pingcap/tidb/pull/7600)のエイリアスの互換性の問題を修正します
    -   `information_schema.COLUMNS`テーブル[＃7602](https://github.com/pingcap/tidb/pull/7602)でfloatタイプの`NUMERIC_SCALE`値が正しくない問題を修正します。
    -   1行のコメントが空の場合にパーサーがエラーを報告する問題を修正します[＃7612](https://github.com/pingcap/tidb/pull/7612)
-   式
    -   `insert`関数[＃7528](https://github.com/pingcap/tidb/pull/7528)で`max_allowed_packet`の値を確認します
    -   組み込み機能をサポートする`json_contains` [＃7443](https://github.com/pingcap/tidb/pull/7443)
    -   組み込み機能をサポートする`json_contains_path` [＃7596](https://github.com/pingcap/tidb/pull/7596)
    -   組み込み機能をサポートする`encode/decode` [＃7622](https://github.com/pingcap/tidb/pull/7622)
    -   一部の時間関連関数がMySQLの動作と互換性がない場合があるという問題を修正します[＃7636](https://github.com/pingcap/tidb/pull/7636)
    -   文字列[＃7654](https://github.com/pingcap/tidb/pull/7654)のデータの時間タイプを解析する互換性の問題を修正します
    -   `DateTime`データのデフォルト値を計算するときにタイムゾーンが考慮されない問題を修正します[＃7655](https://github.com/pingcap/tidb/pull/7655)
-   DML
    -   `InsertOnDuplicateUpdate`ステートメント[＃7534](https://github.com/pingcap/tidb/pull/7534)に正しい`last_insert_id`を設定します
    -   `auto_increment_id`カウンター[＃7515](https://github.com/pingcap/tidb/pull/7515)を更新するケースを減らします
    -   `Duplicate Key`のエラーメッセージを[＃7495](https://github.com/pingcap/tidb/pull/7495)化する
    -   `insert...select...on duplicate key update`の問題を修正[＃7406](https://github.com/pingcap/tidb/pull/7406)
    -   `LOAD DATA IGNORE LINES`ステートメント[＃7576](https://github.com/pingcap/tidb/pull/7576)をサポートする
-   DDL
    -   モニターにDDLジョブタイプと現在のスキーマバージョン情報を追加します[＃7472](https://github.com/pingcap/tidb/pull/7472)
    -   `Admin Restore Table`つの機能の設計を完了します[＃7383](https://github.com/pingcap/tidb/pull/7383)
    -   `Bit`タイプのデフォルト値が128を超える問題を修正します[＃7249](https://github.com/pingcap/tidb/pull/7249)
    -   `Bit`タイプのデフォルト値を[＃7604](https://github.com/pingcap/tidb/pull/7604)にできない問題を修正し`NULL`
    -   DDLキュー[＃7608](https://github.com/pingcap/tidb/pull/7608)のチェック`CREATE TABLE/DATABASE`の間隔を短くします。
    -   `ddl/owner/resign` HTTPインターフェースを使用して、DDL所有者を解放し、新しい所有者の選出を開始します[＃7649](https://github.com/pingcap/tidb/pull/7649)
-   TiKVGoクライアント
    -   `Seek` [＃7419](https://github.com/pingcap/tidb/pull/7419)操作で35しか得られないという問題をサポートし`Key`
-   [テーブルパーティション](https://github.com/pingcap/tidb/projects/6) （実験的）
    -   `Bigint`タイプがパーティションキー[＃7520](https://github.com/pingcap/tidb/pull/7520)として使用できない問題を修正します
    -   パーティションテーブルにインデックスを追加するときに問題が発生した場合のロールバック操作をサポートする[＃7437](https://github.com/pingcap/tidb/pull/7437)

## PD {#pd}

-   特徴
    -   `GetAllStores`インターフェース[＃1228](https://github.com/pingcap/pd/pull/1228)をサポート
    -   シミュレーター[＃1218](https://github.com/pingcap/pd/pull/1218)にスケジューリング見積もりの統計を追加します
-   改善
    -   ダウンストアの処理プロセスを最適化して、できるだけ早くレプリカを作成します[＃1222](https://github.com/pingcap/pd/pull/1222)
    -   コーディネーターの開始を最適化して、PD1の再起動によって発生する不要なスケジューリングを減らし[＃1225](https://github.com/pingcap/pd/pull/1225) 。
    -   メモリ使用量を最適化して、ハートビートによって引き起こされるオーバーヘッドを削減します[＃1195](https://github.com/pingcap/pd/pull/1195)
    -   エラー処理を最適化し、ログ情報を改善する[＃1227](https://github.com/pingcap/pd/pull/1227)
    -   pd-ctl1の特定のストアのリージョン情報のクエリをサポートし[＃1231](https://github.com/pingcap/pd/pull/1231)
    -   pd- [＃1233](https://github.com/pingcap/pd/pull/1233)のバージョン比較に基づくtopNリージョン情報のクエリをサポート
    -   pd- [＃1242](https://github.com/pingcap/pd/pull/1242)でより正確なTSOデコードをサポートする
-   バグ修正
    -   pd-ctlが`hot store`コマンドを使用して誤って終了する問題を修正します[＃1244](https://github.com/pingcap/pd/pull/1244)

## TiKV {#tikv}

-   パフォーマンス
    -   統計推定に基づくリージョンの分割をサポートして、I/Oコストを削減します[＃3511](https://github.com/tikv/tikv/pull/3511)
    -   トランザクションスケジューラのクローンを減らす[＃3530](https://github.com/tikv/tikv/pull/3530)
-   改善
    -   多数の組み込み関数のプッシュダウンサポートを追加します
    -   `leader-transfer-max-log-lag`の構成を追加して、特定のシナリオでのリーダースケジューリングの失敗の問題を修正します[＃3507](https://github.com/tikv/tikv/pull/3507)
    -   `max-open-engines`の構成を追加して、同時に開くエンジンの数を`tikv-importer`に制限します[＃3496](https://github.com/tikv/tikv/pull/3496)
    -   `snapshot apply` [＃3547](https://github.com/tikv/tikv/pull/3547)への影響を減らすために、ガベージデータのクリーンアップ速度を制限します。
    -   重要なRaftメッセージのコミットメッセージをブロードキャストして、不要な遅延を回避します[＃3592](https://github.com/tikv/tikv/pull/3592)
-   バグの修正
    -   新しく分割されたリージョン[＃3557](https://github.com/tikv/tikv/pull/3557)の`PreVote`のメッセージを破棄することによって引き起こされるリーダー選挙の問題を修正します
    -   リージョン[＃3573](https://github.com/tikv/tikv/pull/3573)をマージした後のフォロワー関連の統計を修正
    -   ローカルリーダーが廃止されたリージョン情報を使用する問題を修正します[＃3565](https://github.com/tikv/tikv/pull/3565)
