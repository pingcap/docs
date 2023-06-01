---
title: TiDB 2.1 RC2 Release Notes
---

# TiDB 2.1 RC2 リリースノート {#tidb-2-1-rc2-release-notes}

2018 年 9 月 14 日に、TiDB 2.1 RC2 がリリースされました。 TiDB 2.1 RC1 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   次世代プランナーの提案[<a href="https://github.com/pingcap/tidb/pull/7543">#7543</a>](https://github.com/pingcap/tidb/pull/7543)
    -   定数伝播の最適化ルールを改善[<a href="https://github.com/pingcap/tidb/pull/7276">#7276</a>](https://github.com/pingcap/tidb/pull/7276)
    -   `Range`の計算ロジックを強化して、複数の`IN`または`EQUAL`条件を同時に処理できるようにします[<a href="https://github.com/pingcap/tidb/pull/7577">#7577</a>](https://github.com/pingcap/tidb/pull/7577)
    -   `Range`が空の場合、 `TableScan`の推定結果が正しくない問題を修正[<a href="https://github.com/pingcap/tidb/pull/7583">#7583</a>](https://github.com/pingcap/tidb/pull/7583)
    -   `UPDATE`ステートメントの`PointGet`演算子をサポートします[<a href="https://github.com/pingcap/tidb/pull/7586">#7586</a>](https://github.com/pingcap/tidb/pull/7586)
    -   一部の条件での`FirstRow`関数の実行プロセス中のpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/7624">#7624</a>](https://github.com/pingcap/tidb/pull/7624)
-   SQL実行エンジン
    -   `HashJoin`オペレーターがエラー[<a href="https://github.com/pingcap/tidb/pull/7554">#7554</a>](https://github.com/pingcap/tidb/pull/7554)を検出した場合の潜在的な`DataRace`問題を修正します。
    -   `HashJoin`演算子に内部テーブルを読み取り、同時にハッシュ テーブルを構築させる[<a href="https://github.com/pingcap/tidb/pull/7544">#7544</a>](https://github.com/pingcap/tidb/pull/7544)
    -   ハッシュ集計演算子のパフォーマンスを最適化する[<a href="https://github.com/pingcap/tidb/pull/7541">#7541</a>](https://github.com/pingcap/tidb/pull/7541)
    -   結合演算子[<a href="https://github.com/pingcap/tidb/pull/7493">#7493</a>](https://github.com/pingcap/tidb/pull/7493) 、 [<a href="https://github.com/pingcap/tidb/pull/7433">#7433</a>](https://github.com/pingcap/tidb/pull/7433)のパフォーマンスを最適化します。
    -   結合順序を変更した場合、 `UPDATE JOIN`の結果が正しくなくなる問題を修正[<a href="https://github.com/pingcap/tidb/pull/7571">#7571</a>](https://github.com/pingcap/tidb/pull/7571)
    -   チャンクのイテレータ[<a href="https://github.com/pingcap/tidb/pull/7585">#7585</a>](https://github.com/pingcap/tidb/pull/7585)のパフォーマンスを向上させます。
-   統計
    -   自動分析作業が統計[<a href="https://github.com/pingcap/tidb/pull/7550">#7550</a>](https://github.com/pingcap/tidb/pull/7550)を繰り返し分析する問題を修正します。
    -   統計に変更がない場合に発生する統計更新エラーを修正[<a href="https://github.com/pingcap/tidb/pull/7530">#7530</a>](https://github.com/pingcap/tidb/pull/7530)
    -   `Analyze`リクエスト[<a href="https://github.com/pingcap/tidb/pull/7496">#7496</a>](https://github.com/pingcap/tidb/pull/7496)を構築するときは、RC 分離レベルと低優先度を使用します。
    -   1 日の特定の期間における統計の自動分析の有効化のサポート[<a href="https://github.com/pingcap/tidb/pull/7570">#7570</a>](https://github.com/pingcap/tidb/pull/7570)
    -   統計情報のログ記録時のpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/7588">#7588</a>](https://github.com/pingcap/tidb/pull/7588)
    -   `ANALYZE TABLE WITH BUCKETS`ステートメント[<a href="https://github.com/pingcap/tidb/pull/7619">#7619</a>](https://github.com/pingcap/tidb/pull/7619)を使用したヒストグラム内のバケット数の構成のサポート
    -   空のヒストグラムを更新するときのpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/7640">#7640</a>](https://github.com/pingcap/tidb/pull/7640)
    -   統計情報[<a href="https://github.com/pingcap/tidb/pull/7657">#7657</a>](https://github.com/pingcap/tidb/pull/7657)を利用した更新`information_schema.tables.data_length`
-   サーバ
    -   トレース関連の依存関係を追加[<a href="https://github.com/pingcap/tidb/pull/7532">#7532</a>](https://github.com/pingcap/tidb/pull/7532)
    -   Golang [<a href="https://github.com/pingcap/tidb/pull/7512">#7512</a>](https://github.com/pingcap/tidb/pull/7512)の`mutex profile`機能を有効にする
    -   `Admin`ステートメントには`Super_priv`権限が必要です[<a href="https://github.com/pingcap/tidb/pull/7486">#7486</a>](https://github.com/pingcap/tidb/pull/7486)
    -   ユーザーに重要なシステム`Drop`へのアクセスを禁止する[<a href="https://github.com/pingcap/tidb/pull/7471">#7471</a>](https://github.com/pingcap/tidb/pull/7471)
    -   `juju/errors`から`pkg/errors` [<a href="https://github.com/pingcap/tidb/pull/7151">#7151</a>](https://github.com/pingcap/tidb/pull/7151)に切り替える
    -   SQL トレース[<a href="https://github.com/pingcap/tidb/pull/7016">#7016</a>](https://github.com/pingcap/tidb/pull/7016)の機能プロトタイプを完成させる
    -   goroutine プール[<a href="https://github.com/pingcap/tidb/pull/7564">#7564</a>](https://github.com/pingcap/tidb/pull/7564)を削除します。
    -   `USER1`シグナル[<a href="https://github.com/pingcap/tidb/pull/7587">#7587</a>](https://github.com/pingcap/tidb/pull/7587)を使用した goroutine 情報の表示のサポート
    -   TiDB の起動中に内部 SQL を高優先度に設定します[<a href="https://github.com/pingcap/tidb/pull/7616">#7616</a>](https://github.com/pingcap/tidb/pull/7616)
    -   異なるラベルを使用して、監視メトリクス[<a href="https://github.com/pingcap/tidb/pull/7631">#7631</a>](https://github.com/pingcap/tidb/pull/7631)で内部 SQL とユーザー SQL をフィルタリングします。
    -   先週の上位 30 件の遅いクエリを TiDBサーバー[<a href="https://github.com/pingcap/tidb/pull/7646">#7646</a>](https://github.com/pingcap/tidb/pull/7646)に保存します。
    -   TiDB クラスターのグローバル システム タイム ゾーンを設定する提案を提出する[<a href="https://github.com/pingcap/tidb/pull/7656">#7656</a>](https://github.com/pingcap/tidb/pull/7656)
    -   「GC ライフタイムがトランザクション期間よりも短いです」というエラー メッセージを強化します[<a href="https://github.com/pingcap/tidb/pull/7658">#7658</a>](https://github.com/pingcap/tidb/pull/7658)
    -   TiDB クラスターの起動時にグローバル システム タイム ゾーンを設定します[<a href="https://github.com/pingcap/tidb/pull/7638">#7638</a>](https://github.com/pingcap/tidb/pull/7638)
-   互換性
    -   `Year`タイプ[<a href="https://github.com/pingcap/tidb/pull/7542">#7542</a>](https://github.com/pingcap/tidb/pull/7542)の符号なしフラグを追加します。
    -   `Prepare` / `Execute`モード[<a href="https://github.com/pingcap/tidb/pull/7525">#7525</a>](https://github.com/pingcap/tidb/pull/7525)で`Year`タイプの結果の長さを設定する問題を修正
    -   `Prepare` / `Execute`モードでゼロのタイムスタンプを挿入する問題を修正[<a href="https://github.com/pingcap/tidb/pull/7506">#7506</a>](https://github.com/pingcap/tidb/pull/7506)
    -   整数除算[<a href="https://github.com/pingcap/tidb/pull/7492">#7492</a>](https://github.com/pingcap/tidb/pull/7492)のエラー処理問題を修正
    -   `ComStmtSendLongData` [<a href="https://github.com/pingcap/tidb/pull/7485">#7485</a>](https://github.com/pingcap/tidb/pull/7485)処理時の互換性の問題を修正
    -   文字列を整数[<a href="https://github.com/pingcap/tidb/pull/7483">#7483</a>](https://github.com/pingcap/tidb/pull/7483)に変換するプロセス中のエラー処理の問題を修正しました。
    -   `information_schema.columns_in_table`テーブルの値の精度を最適化する[<a href="https://github.com/pingcap/tidb/pull/7463">#7463</a>](https://github.com/pingcap/tidb/pull/7463)
    -   MariaDB クライアント[<a href="https://github.com/pingcap/tidb/pull/7573">#7573</a>](https://github.com/pingcap/tidb/pull/7573)を使用してデータの文字列型を書き込みまたは更新するときの互換性の問題を修正します。
    -   戻り値[<a href="https://github.com/pingcap/tidb/pull/7600">#7600</a>](https://github.com/pingcap/tidb/pull/7600)のエイリアスの互換性の問題を修正
    -   `information_schema.COLUMNS`テーブル[<a href="https://github.com/pingcap/tidb/pull/7602">#7602</a>](https://github.com/pingcap/tidb/pull/7602)のfloat型の`NUMERIC_SCALE`値が間違っている問題を修正
    -   単一行のコメントが空の場合にパーサーがエラーを報告する問題を修正します[<a href="https://github.com/pingcap/tidb/pull/7612">#7612</a>](https://github.com/pingcap/tidb/pull/7612)
-   式
    -   `insert`関数[<a href="https://github.com/pingcap/tidb/pull/7528">#7528</a>](https://github.com/pingcap/tidb/pull/7528)の`max_allowed_packet`の値を確認します。
    -   組み込み関数のサポート`json_contains` [<a href="https://github.com/pingcap/tidb/pull/7443">#7443</a>](https://github.com/pingcap/tidb/pull/7443)
    -   組み込み関数のサポート`json_contains_path` [<a href="https://github.com/pingcap/tidb/pull/7596">#7596</a>](https://github.com/pingcap/tidb/pull/7596)
    -   組み込み関数のサポート`encode/decode` [<a href="https://github.com/pingcap/tidb/pull/7622">#7622</a>](https://github.com/pingcap/tidb/pull/7622)
    -   一部の時間関連関数がMySQL の動作と互換性がない場合がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/7636">#7636</a>](https://github.com/pingcap/tidb/pull/7636)
    -   文字列[<a href="https://github.com/pingcap/tidb/pull/7654">#7654</a>](https://github.com/pingcap/tidb/pull/7654)のデータの時間型を解析する際の互換性の問題を修正します。
    -   `DateTime`データ[<a href="https://github.com/pingcap/tidb/pull/7655">#7655</a>](https://github.com/pingcap/tidb/pull/7655)のデフォルト値を計算する際にタイムゾーンが考慮されない問題を修正
-   DML
    -   `InsertOnDuplicateUpdate`ステートメントに正しい`last_insert_id`を設定します[<a href="https://github.com/pingcap/tidb/pull/7534">#7534</a>](https://github.com/pingcap/tidb/pull/7534)
    -   `auto_increment_id`カウンタ[<a href="https://github.com/pingcap/tidb/pull/7515">#7515</a>](https://github.com/pingcap/tidb/pull/7515)を更新するケースを減らす
    -   `Duplicate Key` [<a href="https://github.com/pingcap/tidb/pull/7495">#7495</a>](https://github.com/pingcap/tidb/pull/7495)のエラーメッセージを最適化
    -   `insert...select...on duplicate key update`問題を解決する[<a href="https://github.com/pingcap/tidb/pull/7406">#7406</a>](https://github.com/pingcap/tidb/pull/7406)
    -   `LOAD DATA IGNORE LINES`ステートメント[<a href="https://github.com/pingcap/tidb/pull/7576">#7576</a>](https://github.com/pingcap/tidb/pull/7576)をサポートします
-   DDL
    -   DDL ジョブ タイプと現在のスキーマ バージョン情報をモニター[<a href="https://github.com/pingcap/tidb/pull/7472">#7472</a>](https://github.com/pingcap/tidb/pull/7472)に追加します。
    -   `Admin Restore Table`機能[<a href="https://github.com/pingcap/tidb/pull/7383">#7383</a>](https://github.com/pingcap/tidb/pull/7383)のデザインを完成させる
    -   `Bit`タイプのデフォルト値が128を超える問題を修正[<a href="https://github.com/pingcap/tidb/pull/7249">#7249</a>](https://github.com/pingcap/tidb/pull/7249)
    -   `Bit`タイプのデフォルト値を`NULL` [<a href="https://github.com/pingcap/tidb/pull/7604">#7604</a>](https://github.com/pingcap/tidb/pull/7604)にできない問題を修正
    -   DDL キューのチェック`CREATE TABLE/DATABASE`の間隔を短縮します[<a href="https://github.com/pingcap/tidb/pull/7608">#7608</a>](https://github.com/pingcap/tidb/pull/7608)
    -   `ddl/owner/resign` HTTP インターフェイスを使用して、DDL 所有者を解放し、新しい所有者の選択を開始します[<a href="https://github.com/pingcap/tidb/pull/7649">#7649</a>](https://github.com/pingcap/tidb/pull/7649)
-   TiKV Go クライアント
    -   `Seek`操作で`Key` [<a href="https://github.com/pingcap/tidb/pull/7419">#7419</a>](https://github.com/pingcap/tidb/pull/7419)しか取得できない問題をサポート
-   [<a href="https://github.com/pingcap/tidb/projects/6">テーブルパーティション</a>](https://github.com/pingcap/tidb/projects/6) (Experimental)
    -   `Bigint`タイプをパーティションキー[<a href="https://github.com/pingcap/tidb/pull/7520">#7520</a>](https://github.com/pingcap/tidb/pull/7520)として使用できない問題を修正
    -   パーティションテーブルへのインデックスの追加中に問題が発生した場合のロールバック操作をサポートします[<a href="https://github.com/pingcap/tidb/pull/7437">#7437</a>](https://github.com/pingcap/tidb/pull/7437)

## PD {#pd}

-   特徴
    -   `GetAllStores`インターフェイス[<a href="https://github.com/pingcap/pd/pull/1228">#1228</a>](https://github.com/pingcap/pd/pull/1228)をサポート
    -   シミュレータ[<a href="https://github.com/pingcap/pd/pull/1218">#1218</a>](https://github.com/pingcap/pd/pull/1218)にスケジューリング見積もりの統計を追加
-   改善点
    -   ダウンストアの処理プロセスを最適化し、できるだけ早くレプリカを作成します[<a href="https://github.com/pingcap/pd/pull/1222">#1222</a>](https://github.com/pingcap/pd/pull/1222)
    -   コーディネーターの起動を最適化し、PD [<a href="https://github.com/pingcap/pd/pull/1225">#1225</a>](https://github.com/pingcap/pd/pull/1225)の再起動によって生じる不必要なスケジューリングを削減します。
    -   メモリ使用量を最適化して、ハートビートによるオーバーヘッドを削減します[<a href="https://github.com/pingcap/pd/pull/1195">#1195</a>](https://github.com/pingcap/pd/pull/1195)
    -   エラー処理を最適化し、ログ情報を改善します[<a href="https://github.com/pingcap/pd/pull/1227">#1227</a>](https://github.com/pingcap/pd/pull/1227)
    -   pd-ctl [<a href="https://github.com/pingcap/pd/pull/1231">#1231</a>](https://github.com/pingcap/pd/pull/1231)での特定のストアのリージョン情報のクエリのサポート
    -   pd-ctl [<a href="https://github.com/pingcap/pd/pull/1233">#1233</a>](https://github.com/pingcap/pd/pull/1233)のバージョン比較に基づいて、topNリージョン情報のクエリをサポートします。
    -   pd-ctl [<a href="https://github.com/pingcap/pd/pull/1242">#1242</a>](https://github.com/pingcap/pd/pull/1242)でより正確な TSO デコードをサポート
-   バグ修正
    -   pd-ctl が`hot store`コマンドを使用して誤って終了する問題を修正します[<a href="https://github.com/pingcap/pd/pull/1244">#1244</a>](https://github.com/pingcap/pd/pull/1244)

## TiKV {#tikv}

-   パフォーマンス
    -   I/O コストを削減するための統計推定に基づいたリージョン分割のサポート[<a href="https://github.com/tikv/tikv/pull/3511">#3511</a>](https://github.com/tikv/tikv/pull/3511)
    -   トランザクション スケジューラ[<a href="https://github.com/tikv/tikv/pull/3530">#3530</a>](https://github.com/tikv/tikv/pull/3530)でクローンを削減する
-   改善点
    -   多数の組み込み関数に対するプッシュダウンのサポートを追加します。
    -   `leader-transfer-max-log-lag`構成を追加して、特定のシナリオ[<a href="https://github.com/tikv/tikv/pull/3507">#3507</a>](https://github.com/tikv/tikv/pull/3507)におけるリーダーのスケジューリングの失敗の問題を修正します。
    -   `max-open-engines`構成を追加して、 `tikv-importer`によって同時に開かれるエンジンの数を制限します[<a href="https://github.com/tikv/tikv/pull/3496">#3496</a>](https://github.com/tikv/tikv/pull/3496)
    -   `snapshot apply` [<a href="https://github.com/tikv/tikv/pull/3547">#3547</a>](https://github.com/tikv/tikv/pull/3547)への影響を軽減するために、ガベージ データのクリーンアップ速度を制限します。
    -   不要な遅延を避けるために、重要なRaftメッセージのコミット メッセージをブロードキャストします[<a href="https://github.com/tikv/tikv/pull/3592">#3592</a>](https://github.com/tikv/tikv/pull/3592)
-   バグの修正
    -   新しく分割されたリージョン[<a href="https://github.com/tikv/tikv/pull/3557">#3557</a>](https://github.com/tikv/tikv/pull/3557)の`PreVote`メッセージの破棄によって引き起こされるリーダー選出の問題を修正
    -   リージョン[<a href="https://github.com/tikv/tikv/pull/3573">#3573</a>](https://github.com/tikv/tikv/pull/3573)を統合した後のフォロワー関連の統計を修正
    -   ローカル リーダーが古いリージョン情報[<a href="https://github.com/tikv/tikv/pull/3565">#3565</a>](https://github.com/tikv/tikv/pull/3565)を使用する問題を修正します。
