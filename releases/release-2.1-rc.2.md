---
title: TiDB 2.1 RC2 Release Notes
---

# TiDB 2.1 RC2 リリースノート {#tidb-2-1-rc2-release-notes}

2018 年 9 月 14 日に、TiDB 2.1 RC2 がリリースされました。 TiDB 2.1 RC1 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   次世代プランナーの提案[#7543](https://github.com/pingcap/tidb/pull/7543)
    -   定数伝播の最適化ルールを改善[#7276](https://github.com/pingcap/tidb/pull/7276)
    -   `Range`の計算ロジックを強化して、複数の`IN`または`EQUAL`条件を同時に処理できるようにします[#7577](https://github.com/pingcap/tidb/pull/7577)
    -   `Range`が空の場合、 `TableScan`の推定結果が正しくない問題を修正[#7583](https://github.com/pingcap/tidb/pull/7583)
    -   `UPDATE`ステートメントの`PointGet`演算子をサポートします[#7586](https://github.com/pingcap/tidb/pull/7586)
    -   一部の条件での`FirstRow`関数の実行プロセス中のpanicの問題を修正[#7624](https://github.com/pingcap/tidb/pull/7624)
-   SQL実行エンジン
    -   `HashJoin`オペレーターがエラー[#7554](https://github.com/pingcap/tidb/pull/7554)を検出した場合の潜在的な`DataRace`問題を修正します。
    -   `HashJoin`演算子に内部テーブルを読み取り、同時にハッシュ テーブルを構築させる[#7544](https://github.com/pingcap/tidb/pull/7544)
    -   ハッシュ集計演算子のパフォーマンスを最適化する[#7541](https://github.com/pingcap/tidb/pull/7541)
    -   結合演算子[#7493](https://github.com/pingcap/tidb/pull/7493) 、 [#7433](https://github.com/pingcap/tidb/pull/7433)のパフォーマンスを最適化します。
    -   結合順序を変更した場合、 `UPDATE JOIN`の結果が正しくなくなる問題を修正[#7571](https://github.com/pingcap/tidb/pull/7571)
    -   チャンクのイテレータ[#7585](https://github.com/pingcap/tidb/pull/7585)のパフォーマンスを向上させます。
-   統計
    -   自動分析作業が統計[#7550](https://github.com/pingcap/tidb/pull/7550)を繰り返し分析する問題を修正します。
    -   統計に変更がない場合に発生する統計更新エラーを修正[#7530](https://github.com/pingcap/tidb/pull/7530)
    -   `Analyze`リクエスト[#7496](https://github.com/pingcap/tidb/pull/7496)を構築するときは、RC 分離レベルと低優先度を使用します。
    -   1 日の特定の期間における統計の自動分析の有効化のサポート[#7570](https://github.com/pingcap/tidb/pull/7570)
    -   統計情報のログ記録時のpanicの問題を修正[#7588](https://github.com/pingcap/tidb/pull/7588)
    -   `ANALYZE TABLE WITH BUCKETS`ステートメント[#7619](https://github.com/pingcap/tidb/pull/7619)を使用したヒストグラム内のバケット数の構成のサポート
    -   空のヒストグラムを更新するときのpanicの問題を修正[#7640](https://github.com/pingcap/tidb/pull/7640)
    -   統計情報[#7657](https://github.com/pingcap/tidb/pull/7657)を利用した更新`information_schema.tables.data_length`
-   サーバ
    -   トレース関連の依存関係を追加[#7532](https://github.com/pingcap/tidb/pull/7532)
    -   Golang [#7512](https://github.com/pingcap/tidb/pull/7512)の`mutex profile`機能を有効にする
    -   `Admin`ステートメントには`Super_priv`権限が必要です[#7486](https://github.com/pingcap/tidb/pull/7486)
    -   ユーザーに重要なシステム`Drop`へのアクセスを禁止する[#7471](https://github.com/pingcap/tidb/pull/7471)
    -   `juju/errors`から`pkg/errors` [#7151](https://github.com/pingcap/tidb/pull/7151)に切り替える
    -   SQL トレース[#7016](https://github.com/pingcap/tidb/pull/7016)の機能プロトタイプを完成させる
    -   goroutine プール[#7564](https://github.com/pingcap/tidb/pull/7564)を削除します。
    -   `USER1`シグナル[#7587](https://github.com/pingcap/tidb/pull/7587)を使用した goroutine 情報の表示のサポート
    -   TiDB の起動中に内部 SQL を高優先度に設定します[#7616](https://github.com/pingcap/tidb/pull/7616)
    -   異なるラベルを使用して、監視メトリクス[#7631](https://github.com/pingcap/tidb/pull/7631)で内部 SQL とユーザー SQL をフィルタリングします。
    -   先週の上位 30 件の遅いクエリを TiDBサーバー[#7646](https://github.com/pingcap/tidb/pull/7646)に保存します。
    -   TiDB クラスターのグローバル システム タイム ゾーンを設定する提案を提出する[#7656](https://github.com/pingcap/tidb/pull/7656)
    -   「GC ライフタイムがトランザクション期間よりも短いです」というエラー メッセージを強化します[#7658](https://github.com/pingcap/tidb/pull/7658)
    -   TiDB クラスターの起動時にグローバル システム タイム ゾーンを設定します[#7638](https://github.com/pingcap/tidb/pull/7638)
-   互換性
    -   `Year`タイプ[#7542](https://github.com/pingcap/tidb/pull/7542)の符号なしフラグを追加します。
    -   `Prepare` / `Execute`モード[#7525](https://github.com/pingcap/tidb/pull/7525)で`Year`タイプの結果の長さを設定する問題を修正
    -   `Prepare` / `Execute`モードでゼロのタイムスタンプを挿入する問題を修正[#7506](https://github.com/pingcap/tidb/pull/7506)
    -   整数除算[#7492](https://github.com/pingcap/tidb/pull/7492)のエラー処理問題を修正
    -   `ComStmtSendLongData` [#7485](https://github.com/pingcap/tidb/pull/7485)処理時の互換性の問題を修正
    -   文字列を整数[#7483](https://github.com/pingcap/tidb/pull/7483)に変換するプロセス中のエラー処理の問題を修正しました。
    -   `information_schema.columns_in_table`テーブルの値の精度を最適化する[#7463](https://github.com/pingcap/tidb/pull/7463)
    -   MariaDB クライアント[#7573](https://github.com/pingcap/tidb/pull/7573)を使用してデータの文字列型を書き込みまたは更新するときの互換性の問題を修正します。
    -   戻り値[#7600](https://github.com/pingcap/tidb/pull/7600)のエイリアスの互換性の問題を修正
    -   `information_schema.COLUMNS`テーブル[#7602](https://github.com/pingcap/tidb/pull/7602)のfloat型の`NUMERIC_SCALE`値が間違っている問題を修正
    -   単一行のコメントが空の場合にパーサーがエラーを報告する問題を修正します[#7612](https://github.com/pingcap/tidb/pull/7612)
-   式
    -   `insert`関数[#7528](https://github.com/pingcap/tidb/pull/7528)の`max_allowed_packet`の値を確認します。
    -   組み込み関数のサポート`json_contains` [#7443](https://github.com/pingcap/tidb/pull/7443)
    -   組み込み関数のサポート`json_contains_path` [#7596](https://github.com/pingcap/tidb/pull/7596)
    -   組み込み関数のサポート`encode/decode` [#7622](https://github.com/pingcap/tidb/pull/7622)
    -   一部の時間関連関数がMySQL の動作と互換性がない場合がある問題を修正します[#7636](https://github.com/pingcap/tidb/pull/7636)
    -   文字列[#7654](https://github.com/pingcap/tidb/pull/7654)のデータの時間型を解析する際の互換性の問題を修正します。
    -   `DateTime`データ[#7655](https://github.com/pingcap/tidb/pull/7655)のデフォルト値を計算する際にタイムゾーンが考慮されない問題を修正
-   DML
    -   `InsertOnDuplicateUpdate`ステートメントに正しい`last_insert_id`を設定します[#7534](https://github.com/pingcap/tidb/pull/7534)
    -   `auto_increment_id`カウンタ[#7515](https://github.com/pingcap/tidb/pull/7515)を更新するケースを減らす
    -   `Duplicate Key` [#7495](https://github.com/pingcap/tidb/pull/7495)のエラーメッセージを最適化
    -   `insert...select...on duplicate key update`問題を解決する[#7406](https://github.com/pingcap/tidb/pull/7406)
    -   `LOAD DATA IGNORE LINES`ステートメント[#7576](https://github.com/pingcap/tidb/pull/7576)をサポートします
-   DDL
    -   DDL ジョブ タイプと現在のスキーマ バージョン情報をモニター[#7472](https://github.com/pingcap/tidb/pull/7472)に追加します。
    -   `Admin Restore Table`機能[#7383](https://github.com/pingcap/tidb/pull/7383)のデザインを完成させる
    -   `Bit`タイプのデフォルト値が128を超える問題を修正[#7249](https://github.com/pingcap/tidb/pull/7249)
    -   `Bit`タイプのデフォルト値を`NULL` [#7604](https://github.com/pingcap/tidb/pull/7604)にできない問題を修正
    -   DDL キューのチェック`CREATE TABLE/DATABASE`の間隔を短縮します[#7608](https://github.com/pingcap/tidb/pull/7608)
    -   `ddl/owner/resign` HTTP インターフェイスを使用して、DDL 所有者を解放し、新しい所有者の選択を開始します[#7649](https://github.com/pingcap/tidb/pull/7649)
-   TiKV Go クライアント
    -   `Seek`操作で`Key` [#7419](https://github.com/pingcap/tidb/pull/7419)しか取得できない問題をサポート
-   [テーブルパーティション](https://github.com/pingcap/tidb/projects/6) (Experimental)
    -   `Bigint`タイプをパーティションキー[#7520](https://github.com/pingcap/tidb/pull/7520)として使用できない問題を修正
    -   パーティションテーブルへのインデックスの追加中に問題が発生した場合のロールバック操作をサポートします[#7437](https://github.com/pingcap/tidb/pull/7437)

## PD {#pd}

-   特徴
    -   `GetAllStores`インターフェイス[#1228](https://github.com/pingcap/pd/pull/1228)をサポート
    -   シミュレータ[#1218](https://github.com/pingcap/pd/pull/1218)にスケジューリング見積もりの​​統計を追加
-   改善点
    -   ダウンストアの処理プロセスを最適化し、できるだけ早くレプリカを作成します[#1222](https://github.com/pingcap/pd/pull/1222)
    -   コーディネーターの起動を最適化し、PD [#1225](https://github.com/pingcap/pd/pull/1225)の再起動によって生じる不必要なスケジューリングを削減します。
    -   メモリ使用量を最適化して、ハートビートによるオーバーヘッドを削減します[#1195](https://github.com/pingcap/pd/pull/1195)
    -   エラー処理を最適化し、ログ情報を改善します[#1227](https://github.com/pingcap/pd/pull/1227)
    -   pd-ctl [#1231](https://github.com/pingcap/pd/pull/1231)での特定のストアのリージョン情報のクエリのサポート
    -   pd-ctl [#1233](https://github.com/pingcap/pd/pull/1233)のバージョン比較に基づいて、topNリージョン情報のクエリをサポートします。
    -   pd-ctl [#1242](https://github.com/pingcap/pd/pull/1242)でより正確な TSO デコードをサポート
-   バグ修正
    -   pd-ctl が`hot store`コマンドを使用して誤って終了する問題を修正します[#1244](https://github.com/pingcap/pd/pull/1244)

## TiKV {#tikv}

-   パフォーマンス
    -   I/O コストを削減するための統計推定に基づいたリージョン分割のサポート[#3511](https://github.com/tikv/tikv/pull/3511)
    -   トランザクション スケジューラ[#3530](https://github.com/tikv/tikv/pull/3530)でクローンを削減する
-   改善点
    -   多数の組み込み関数に対するプッシュダウンのサポートを追加します。
    -   `leader-transfer-max-log-lag`構成を追加して、特定のシナリオ[#3507](https://github.com/tikv/tikv/pull/3507)におけるリーダーのスケジューリングの失敗の問題を修正します。
    -   `max-open-engines`構成を追加して、 `tikv-importer`によって同時に開かれるエンジンの数を制限します[#3496](https://github.com/tikv/tikv/pull/3496)
    -   `snapshot apply` [#3547](https://github.com/tikv/tikv/pull/3547)への影響を軽減するために、ガベージ データのクリーンアップ速度を制限します。
    -   不要な遅延を避けるために、重要なRaftメッセージのコミット メッセージをブロードキャストします[#3592](https://github.com/tikv/tikv/pull/3592)
-   バグの修正
    -   新しく分割されたリージョン[#3557](https://github.com/tikv/tikv/pull/3557)の`PreVote`メッセージの破棄によって引き起こされるリーダー選出の問題を修正
    -   リージョン[#3573](https://github.com/tikv/tikv/pull/3573)を統合した後のフォロワー関連の統計を修正
    -   ローカル リーダーが古いリージョン情報[#3565](https://github.com/tikv/tikv/pull/3565)を使用する問題を修正します。
