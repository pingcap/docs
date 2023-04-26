---
title: TiDB 2.1 RC2 Release Notes
---

# TiDB 2.1 RC2 リリースノート {#tidb-2-1-rc2-release-notes}

2018 年 9 月 14 日に、TiDB 2.1 RC2 がリリースされました。 TiDB 2.1 RC1 と比較すると、このリリースでは、安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー
    -   次世代 Planner [#7543](https://github.com/pingcap/tidb/pull/7543)の提案を行う
    -   定数伝播の最適化ルールを改善する[#7276](https://github.com/pingcap/tidb/pull/7276)
    -   `Range`の計算ロジックを拡張して、複数の`IN`または`EQUAL`条件を同時に処理できるようにする[#7577](https://github.com/pingcap/tidb/pull/7577)
    -   `Range`が空の場合、 `TableScan`の推定結果が正しくない問題を修正[#7583](https://github.com/pingcap/tidb/pull/7583)
    -   `UPDATE`ステートメント[#7586](https://github.com/pingcap/tidb/pull/7586)の`PointGet`演算子をサポート
    -   一部の条件で`FirstRow`集約関数を実行するプロセス中のpanicの問題を修正します[#7624](https://github.com/pingcap/tidb/pull/7624)
-   SQL 実行エンジン
    -   `HashJoin`オペレーターがエラー[#7554](https://github.com/pingcap/tidb/pull/7554)に遭遇したときの潜在的な`DataRace`問題を修正します。
    -   `HashJoin`オペレーターに内部テーブルを読み取らせ、同時にハッシュ テーブルを構築します[#7544](https://github.com/pingcap/tidb/pull/7544)
    -   ハッシュ集計演算子のパフォーマンスを最適化する[#7541](https://github.com/pingcap/tidb/pull/7541)
    -   Join 演算子[#7493](https://github.com/pingcap/tidb/pull/7493) 、 [#7433](https://github.com/pingcap/tidb/pull/7433)のパフォーマンスを最適化する
    -   結合順序を変更すると`UPDATE JOIN`の結果が正しくない問題を修正[#7571](https://github.com/pingcap/tidb/pull/7571)
    -   チャンクのイテレータ[#7585](https://github.com/pingcap/tidb/pull/7585)のパフォーマンスを改善する
-   統計
    -   自動分析作業が統計を繰り返し分析する問題を修正します[#7550](https://github.com/pingcap/tidb/pull/7550)
    -   統計の変更がない場合に発生する統計更新エラーを修正します[#7530](https://github.com/pingcap/tidb/pull/7530)
    -   RC 分離レベルと低優先度を使用して`Analyze`リクエストを構築する[#7496](https://github.com/pingcap/tidb/pull/7496)
    -   [#7570](https://github.com/pingcap/tidb/pull/7570)日の特定の期間に統計の自動分析を有効にするサポート
    -   統計情報をログに記録するときのpanicの問題を修正します[#7588](https://github.com/pingcap/tidb/pull/7588)
    -   `ANALYZE TABLE WITH BUCKETS`ステートメント[#7619](https://github.com/pingcap/tidb/pull/7619)を使用したヒストグラム内のバケット数の構成をサポート
    -   空のヒストグラムを更新するときのpanicの問題を修正します[#7640](https://github.com/pingcap/tidb/pull/7640)
    -   統計情報を使用した更新`information_schema.tables.data_length` [#7657](https://github.com/pingcap/tidb/pull/7657)
-   サーバ
    -   Trace 関連の依存関係の追加[#7532](https://github.com/pingcap/tidb/pull/7532)
    -   Golang [#7512](https://github.com/pingcap/tidb/pull/7512)の`mutex profile`機能を有効にする
    -   `Admin`ステートメントには`Super_priv`特権[#7486](https://github.com/pingcap/tidb/pull/7486)が必要です
    -   `Drop`重要なシステム テーブルへのユーザーのアクセスを禁止する[#7471](https://github.com/pingcap/tidb/pull/7471)
    -   `juju/errors`から`pkg/errors`に切り替える[#7151](https://github.com/pingcap/tidb/pull/7151)
    -   SQL トレース[#7016](https://github.com/pingcap/tidb/pull/7016)の機能プロトタイプを完成させる
    -   ゴルーチン プール[#7564](https://github.com/pingcap/tidb/pull/7564)を削除する
    -   `USER1`シグナル[#7587](https://github.com/pingcap/tidb/pull/7587)を使用したゴルーチン情報の表示をサポート
    -   TiDB の起動中に内部 SQL を高優先度に設定する[#7616](https://github.com/pingcap/tidb/pull/7616)
    -   異なるラベルを使用して、メトリックの監視で内部 SQL とユーザー SQL をフィルター処理する[#7631](https://github.com/pingcap/tidb/pull/7631)
    -   先週の上位 30 件の遅いクエリを TiDBサーバーに保存します[#7646](https://github.com/pingcap/tidb/pull/7646)
    -   TiDB クラスターのグローバル システム タイム ゾーンを設定する提案を提出する[#7656](https://github.com/pingcap/tidb/pull/7656)
    -   「GC ライフタイムがトランザクション期間よりも短い」というエラーメッセージを充実させる[#7658](https://github.com/pingcap/tidb/pull/7658)
    -   TiDB クラスタの起動時にグローバル システム タイム ゾーンを設定する[#7638](https://github.com/pingcap/tidb/pull/7638)
-   互換性
    -   `Year`タイプ[#7542](https://github.com/pingcap/tidb/pull/7542)の unsigned フラグを追加します
    -   `Prepare` / `Execute`モード[#7525](https://github.com/pingcap/tidb/pull/7525)で`Year`型の結果の長さを構成する問題を修正します。
    -   `Prepare` / `Execute`モードでゼロのタイムスタンプを挿入する問題を修正[#7506](https://github.com/pingcap/tidb/pull/7506)
    -   整数除算[#7492](https://github.com/pingcap/tidb/pull/7492)のエラー処理の問題を修正
    -   `ComStmtSendLongData` [#7485](https://github.com/pingcap/tidb/pull/7485)処理時の互換性の問題を修正
    -   文字列を整数[#7483](https://github.com/pingcap/tidb/pull/7483)に変換する際のエラー処理の問題を修正
    -   `information_schema.columns_in_table`テーブルの値の精度を最適化する[#7463](https://github.com/pingcap/tidb/pull/7463)
    -   MariaDB クライアントを使用して文字列型のデータを書き込みまたは更新する際の互換性の問題を修正します[#7573](https://github.com/pingcap/tidb/pull/7573)
    -   戻り値[#7600](https://github.com/pingcap/tidb/pull/7600)のエイリアスの互換性の問題を修正
    -   `information_schema.COLUMNS`テーブル[#7602](https://github.com/pingcap/tidb/pull/7602)で float 型の`NUMERIC_SCALE`値が正しくない問題を修正
    -   1 行のコメントが空の場合にパーサーがエラーを報告する問題を修正します[#7612](https://github.com/pingcap/tidb/pull/7612)
-   式
    -   `insert`関数[#7528](https://github.com/pingcap/tidb/pull/7528)で`max_allowed_packet`の値を確認する
    -   内蔵機能をサポート`json_contains` [#7443](https://github.com/pingcap/tidb/pull/7443)
    -   内蔵機能をサポート`json_contains_path` [#7596](https://github.com/pingcap/tidb/pull/7596)
    -   内蔵機能をサポート`encode/decode` [#7622](https://github.com/pingcap/tidb/pull/7622)
    -   一部の時間関連の関数がMySQL の動作と互換性がない場合がある問題を修正します[#7636](https://github.com/pingcap/tidb/pull/7636)
    -   文字列[#7654](https://github.com/pingcap/tidb/pull/7654)のデータの時刻型を解析する際の互換性の問題を修正します
    -   `DateTime`データのデフォルト値を計算するときにタイム ゾーンが考慮されない問題を修正します[#7655](https://github.com/pingcap/tidb/pull/7655)
-   DML
    -   `InsertOnDuplicateUpdate`ステートメント[#7534](https://github.com/pingcap/tidb/pull/7534)に正しい`last_insert_id`を設定します
    -   `auto_increment_id`カウンタを更新するケースを減らす[#7515](https://github.com/pingcap/tidb/pull/7515)
    -   `Duplicate Key` [#7495](https://github.com/pingcap/tidb/pull/7495)のエラー メッセージを最適化する
    -   `insert...select...on duplicate key update`問題[#7406](https://github.com/pingcap/tidb/pull/7406)を修正します。
    -   `LOAD DATA IGNORE LINES`ステートメント[#7576](https://github.com/pingcap/tidb/pull/7576)をサポート
-   DDL
    -   DDL ジョブ タイプと現在のスキーマ バージョン情報をモニターに追加します[#7472](https://github.com/pingcap/tidb/pull/7472)
    -   `Admin Restore Table`機能[#7383](https://github.com/pingcap/tidb/pull/7383)の設計を完了する
    -   `Bit`型のデフォルト値が128を超える問題を修正[#7249](https://github.com/pingcap/tidb/pull/7249)
    -   `Bit`タイプのデフォルト値が`NULL` [#7604](https://github.com/pingcap/tidb/pull/7604)にならない問題を修正
    -   DDL キュー[#7608](https://github.com/pingcap/tidb/pull/7608)のチェック`CREATE TABLE/DATABASE`の間隔を減らす
    -   `ddl/owner/resign` HTTP インターフェイスを使用して DDL 所有者を解放し、新しい所有者の選択を開始します[#7649](https://github.com/pingcap/tidb/pull/7649)
-   TiKV Go クライアント
    -   `Seek`回の操作で`Key` [#7419](https://github.com/pingcap/tidb/pull/7419)しか得られない問題をサポート
-   [テーブル パーティション](https://github.com/pingcap/tidb/projects/6) (Experimental)
    -   `Bigint`タイプがパーティションキーとして使用できない問題を修正[#7520](https://github.com/pingcap/tidb/pull/7520)
    -   パーティションテーブルにインデックスを追加する際に問題が発生した場合のロールバック操作をサポートします[#7437](https://github.com/pingcap/tidb/pull/7437)

## PD {#pd}

-   特徴
    -   `GetAllStores`インターフェイス[#1228](https://github.com/pingcap/pd/pull/1228)をサポート
    -   シミュレータ[#1218](https://github.com/pingcap/pd/pull/1218)でのスケジューリング見積もりの統計を追加します。
-   改良点
    -   ダウン ストアの処理プロセスを最適化して、できるだけ早くレプリカを作成する[#1222](https://github.com/pingcap/pd/pull/1222)
    -   Coordinator の起動を最適化して、PD [#1225](https://github.com/pingcap/pd/pull/1225)の再起動によって発生する不要なスケジューリングを減らします
    -   メモリ使用量を最適化して、ハートビートによるオーバーヘッドを削減します[#1195](https://github.com/pingcap/pd/pull/1195)
    -   エラー処理を最適化し、ログ情報を改善する[#1227](https://github.com/pingcap/pd/pull/1227)
    -   pd-ctl [#1231](https://github.com/pingcap/pd/pull/1231)で特定のストアのリージョン情報のクエリをサポート
    -   pd-ctl [#1233](https://github.com/pingcap/pd/pull/1233)のバージョン比較に基づく topNリージョン情報のクエリをサポート
    -   pd-ctl [#1242](https://github.com/pingcap/pd/pull/1242)でより正確な TSO デコードをサポート
-   バグ修正
    -   pd-ctl が`hot store`コマンドを使用して誤って終了する問題を修正[#1244](https://github.com/pingcap/pd/pull/1244)

## TiKV {#tikv}

-   パフォーマンス
    -   I/O コストを削減するために、統計の推定に基づいてリージョンを分割することをサポートします[#3511](https://github.com/tikv/tikv/pull/3511)
    -   トランザクション スケジューラでクローンを減らす[#3530](https://github.com/tikv/tikv/pull/3530)
-   改良点
    -   多数の組み込み関数のプッシュダウン サポートを追加します。
    -   特定のシナリオでのリーダー スケジューリングの失敗の問題を修正するために`leader-transfer-max-log-lag`の構成を追加します[#3507](https://github.com/tikv/tikv/pull/3507)
    -   `max-open-engines`構成を追加して、同時に開くエンジンの数を`tikv-importer`に制限します[#3496](https://github.com/tikv/tikv/pull/3496)
    -   ガベージ データのクリーンアップ速度を制限して、 `snapshot apply` [#3547](https://github.com/tikv/tikv/pull/3547)への影響を軽減します。
    -   不必要な遅延を避けるために重要なRaftメッセージのコミット メッセージをブロードキャストする[#3592](https://github.com/tikv/tikv/pull/3592)
-   バグの修正
    -   新しく分割されたリージョン[#3557](https://github.com/tikv/tikv/pull/3557)の`PreVote`メッセージを破棄することによって引き起こされるリーダー選出の問題を修正します。
    -   Regions [#3573](https://github.com/tikv/tikv/pull/3573)のマージ後にフォロワー関連の統計を修正
    -   ローカル リーダーが古いリージョン情報を使用する問題を修正します[#3565](https://github.com/tikv/tikv/pull/3565)
