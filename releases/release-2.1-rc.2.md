---
title: TiDB 2.1 RC2 Release Notes
summary: TiDB 2.1 RC2は2018年9月14日にリリースされ、安定性、SQLオプティマイザ、統計、実行エンジンが改善されました。このリリースには、SQLオプティマイザ、SQL実行エンジン、統計、サーバー、互換性、式、DML、DDL、TiKV Goクライアント、テーブルパーティションの機能強化が含まれています。PD機能、改善、バグ修正も含まれています。TiKVのパフォーマンス、改善、バグ修正もこのリリースに含まれています。
---

# TiDB 2.1 RC2 リリースノート {#tidb-2-1-rc2-release-notes}

2018年9月14日にTiDB 2.1 RC2がリリースされました。TiDB 2.1 RC1と比較して、このリリースでは安定性、SQLオプティマイザー、統計情報、実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   次世代プランナーの提案 [＃7543](https://github.com/pingcap/tidb/pull/7543)
    -   定数伝播の最適化ルールを改善する[＃7276](https://github.com/pingcap/tidb/pull/7276)
    -   `Range`の計算ロジックを強化して、複数の`IN`または`EQUAL`条件を同時に処理できるようにします[＃7577](https://github.com/pingcap/tidb/pull/7577)
    -   `Range`が空の場合に`TableScan`の推定結果が正しくない問題を修正[＃7583](https://github.com/pingcap/tidb/pull/7583)
    -   `UPDATE`文の`PointGet`演算子をサポートする [＃7586](https://github.com/pingcap/tidb/pull/7586)
    -   いくつかの条件で`FirstRow`集計関数を実行するプロセス中にpanic問題を修正しました[＃7624](https://github.com/pingcap/tidb/pull/7624)
-   SQL実行エンジン
    -   `HashJoin`オペレータがエラーに遭遇した場合の潜在的な`DataRace`問題を修正します [＃7554](https://github.com/pingcap/tidb/pull/7554)
    -   `HashJoin`演算子で内部テーブルを読み取り、同時にハッシュテーブルを構築する[＃7544](https://github.com/pingcap/tidb/pull/7544)
    -   ハッシュ集計演算子のパフォーマンスを最適化する[＃7541](https://github.com/pingcap/tidb/pull/7541)
    -   Join演算子 パフォーマンスを最適化します [＃7433](https://github.com/pingcap/tidb/pull/7433) [＃7493](https://github.com/pingcap/tidb/pull/7493)
    -   結合順序が変更されると`UPDATE JOIN`の結果が正しくなくなる問題を修正[＃7571](https://github.com/pingcap/tidb/pull/7571)
    -   チャンクのイテレータのパフォーマンスを向上させる [＃7585](https://github.com/pingcap/tidb/pull/7585)
-   統計
    -   自動分析作業で統計を繰り返し分析する問題を修正 [＃7550](https://github.com/pingcap/tidb/pull/7550)
    -   統計情報に変更がない場合に発生する統計情報更新エラーを修正[＃7530](https://github.com/pingcap/tidb/pull/7530)
    -   `Analyze`リクエストを構築するときはRC分離レベルと低い優先度を使用する [＃7496](https://github.com/pingcap/tidb/pull/7496)
    -   1 日の特定の期間の統計を自動分析できるようにするサポート[＃7570](https://github.com/pingcap/tidb/pull/7570)
    -   統計情報のログ記録時に発生するpanic問題を修正[＃7588](https://github.com/pingcap/tidb/pull/7588)
    -   `ANALYZE TABLE WITH BUCKETS`文を使用してヒストグラム内のバケット数の設定をサポートします [＃7619](https://github.com/pingcap/tidb/pull/7619)
    -   空のヒストグラムを更新するときにpanic問題を修正[＃7640](https://github.com/pingcap/tidb/pull/7640)
    -   統計情報を使用して`information_schema.tables.data_length`を更新 [＃7657](https://github.com/pingcap/tidb/pull/7657)
-   サーバ
    -   トレース関連の依存関係を追加する [＃7532](https://github.com/pingcap/tidb/pull/7532)
    -   Golang の`mutex profile`機能を有効にする [＃7512](https://github.com/pingcap/tidb/pull/7512)
    -   `Admin`文には`Super_priv`権限が必要です [＃7486](https://github.com/pingcap/tidb/pull/7486)
    -   重要なシステムテーブルへの`Drop`アクセスを禁止する [＃7471](https://github.com/pingcap/tidb/pull/7471)
    -   `juju/errors`から`pkg/errors` に切り替える [＃7151](https://github.com/pingcap/tidb/pull/7151)
    -   SQLトレースの機能プロトタイプを完成させる [＃7016](https://github.com/pingcap/tidb/pull/7016)
    -   ゴルーチンプールを削除する [＃7564](https://github.com/pingcap/tidb/pull/7564)
    -   `USER1`シグナルを使用してゴルーチン情報の表示をサポート [＃7587](https://github.com/pingcap/tidb/pull/7587)
    -   TiDBの起動中に内部SQLを高優先度に設定する[＃7616](https://github.com/pingcap/tidb/pull/7616)
    -   監視メトリクスで内部SQLとユーザーSQLをフィルタリングするために異なるラベルを使用する [＃7631](https://github.com/pingcap/tidb/pull/7631)
    -   過去1週間のスロークエリ上位30件をTiDBサーバーに保存する [＃7646](https://github.com/pingcap/tidb/pull/7646)
    -   TiDBクラスタのグローバルシステムタイムゾーンを設定する提案を提出する [＃7656](https://github.com/pingcap/tidb/pull/7656)
    -   「GCの有効期間がトランザクション期間より短い」というエラーメッセージを充実させる[＃7658](https://github.com/pingcap/tidb/pull/7658)
    -   TiDBクラスタを起動するときにグローバルシステムのタイムゾーンを設定する [＃7638](https://github.com/pingcap/tidb/pull/7638)
-   互換性
    -   `Year`型に符号なしフラグを追加 [＃7542](https://github.com/pingcap/tidb/pull/7542)
    -   `Prepare`モードで`Year`型の結果の長さ`Execute`設定する問題を修正 [＃7525](https://github.com/pingcap/tidb/pull/7525)
    -   `Prepare`モードで`Execute`タイムスタンプを挿入する問題を修正[＃7506](https://github.com/pingcap/tidb/pull/7506)
    -   整数除算のエラー処理の問題を修正 [＃7492](https://github.com/pingcap/tidb/pull/7492)
    -   `ComStmtSendLongData` 処理時の互換性の問題を修正 [＃7485](https://github.com/pingcap/tidb/pull/7485)
    -   文字列を整数に変換するプロセス中のエラー処理の問題を修正 [＃7483](https://github.com/pingcap/tidb/pull/7483)
    -   `information_schema.columns_in_table`表の値の精度を最適化します [＃7463](https://github.com/pingcap/tidb/pull/7463)
    -   MariaDBクライアントを使用して文字列型のデータを書き込んだり更新したりする際の互換性の問題を修正しました [＃7573](https://github.com/pingcap/tidb/pull/7573)
    -   戻り値のエイリアスの互換性の問題を修正 [＃7600](https://github.com/pingcap/tidb/pull/7600)
    -   `information_schema.COLUMNS`表の float 型の`NUMERIC_SCALE`の値が正しくない問題を修正しました [＃7602](https://github.com/pingcap/tidb/pull/7602)
    -   1行コメントが空の場合にパーサーがエラーを報告する問題を修正しました[＃7612](https://github.com/pingcap/tidb/pull/7612)
-   表現
    -   `insert`関数の`max_allowed_packet`の値を確認する [＃7528](https://github.com/pingcap/tidb/pull/7528)
    -   組み込み関数`json_contains` をサポート [＃7443](https://github.com/pingcap/tidb/pull/7443)
    -   組み込み関数`json_contains_path` をサポート [＃7596](https://github.com/pingcap/tidb/pull/7596)
    -   組み込み関数`encode/decode` をサポート [＃7622](https://github.com/pingcap/tidb/pull/7622)
    -   一部の時間関連関数がMySQLの動作と互換性がないことがある問題を修正[＃7636](https://github.com/pingcap/tidb/pull/7636)
    -   文字列の時刻型データの解析に関する互換性の問題を修正しました [＃7654](https://github.com/pingcap/tidb/pull/7654)
    -   `DateTime`データのデフォルト値を計算するときにタイムゾーンが考慮されない問題を修正しました [＃7655](https://github.com/pingcap/tidb/pull/7655)
-   DML
    -   `InsertOnDuplicateUpdate`文の`last_insert_id`正しく設定する [＃7534](https://github.com/pingcap/tidb/pull/7534)
    -   `auto_increment_id`カウンタ更新するケースを減らす [＃7515](https://github.com/pingcap/tidb/pull/7515)
    -   `Duplicate Key` のエラーメッセージを最適化 [＃7495](https://github.com/pingcap/tidb/pull/7495)
    -   `insert...select...on duplicate key update`問題を修正[＃7406](https://github.com/pingcap/tidb/pull/7406)
    -   `LOAD DATA IGNORE LINES`ステートメントサポートする [＃7576](https://github.com/pingcap/tidb/pull/7576)
-   DDL
    -   モニターにDDLジョブタイプと現在のスキーマバージョン情報を追加します。 [＃7472](https://github.com/pingcap/tidb/pull/7472)
    -   `Admin Restore Table`機能の設計を完了する [＃7383](https://github.com/pingcap/tidb/pull/7383)
    -   `Bit`型のデフォルト値が128を超える問題を修正[＃7249](https://github.com/pingcap/tidb/pull/7249)
    -   `Bit`型のデフォルト値が`NULL` にできない問題を修正 [＃7604](https://github.com/pingcap/tidb/pull/7604)
    -   DDLキューのチェック間隔`CREATE TABLE/DATABASE`を減らす [＃7608](https://github.com/pingcap/tidb/pull/7608)
    -   `ddl/owner/resign` HTTPインターフェースを使用してDDL所有者を解放し、新しい所有者選出を開始します。 [＃7649](https://github.com/pingcap/tidb/pull/7649)
-   TiKV Goクライアント
    -   `Seek`操作で`Key` しか取得できないという問題をサポートします [＃7419](https://github.com/pingcap/tidb/pull/7419)
-   [テーブルパーティション](https://github.com/pingcap/tidb/projects/6) (Experimental)
    -   `Bigint`型をパーティションキーとして使用できない問題を修正 [＃7520](https://github.com/pingcap/tidb/pull/7520)
    -   パーティションテーブルにインデックスを追加する際に問題が発生した場合のロールバック操作をサポートします。 [＃7437](https://github.com/pingcap/tidb/pull/7437)

## PD {#pd}

-   特徴
    -   `GetAllStores`インターフェースサポート [＃1228](https://github.com/pingcap/pd/pull/1228)
    -   シミュレータにスケジュール見積もりの統計を追加する [＃1218](https://github.com/pingcap/pd/pull/1218)
-   改善点
    -   ダウンストアの処理プロセスを最適化して、できるだけ早くレプリカを作成します[＃1222](https://github.com/pingcap/pd/pull/1222)
    -   PD 再起動によって発生する不要なスケジュールを削減するためにコーディネーターの起動を最適化します。 [＃1225](https://github.com/pingcap/pd/pull/1225)
    -   メモリ使用量を最適化して、ハートビートによるオーバーヘッドを削減する[＃1195](https://github.com/pingcap/pd/pull/1195)
    -   エラー処理を最適化し、ログ情報を改善する[＃1227](https://github.com/pingcap/pd/pull/1227)
    -   pd-ctl で特定のストアのリージョン情報を照会する機能をサポート [＃1231](https://github.com/pingcap/pd/pull/1231)
    -   pd-ctl のバージョン比較に基づいて、トップ Nリージョン情報を照会する機能をサポート [＃1233](https://github.com/pingcap/pd/pull/1233)
    -   pd-ctl でより正確な TSO デコードをサポート [＃1242](https://github.com/pingcap/pd/pull/1242)
-   バグ修正
    -   pd-ctlが`hot store`コマンドを使用して誤って終了する問題を修正しました[＃1244](https://github.com/pingcap/pd/pull/1244)

## TiKV {#tikv}

-   パフォーマンス
    -   I/Oコストを削減するために統計推定に基づいてリージョンを分割する機能をサポート[＃3511](https://github.com/tikv/tikv/pull/3511)
    -   トランザクションスケジューラクローンを削減 [＃3530](https://github.com/tikv/tikv/pull/3530)
-   改善点
    -   多数の組み込み関数にプッシュダウンのサポートを追加
    -   特定のシナリオにおけるリーダースケジューリングの失敗の問題を修正するために`leader-transfer-max-log-lag`構成を追加します[＃3507](https://github.com/tikv/tikv/pull/3507)
    -   `max-open-engines`構成を追加して、同時に`tikv-importer`のエンジンが開く数を制限します[＃3496](https://github.com/tikv/tikv/pull/3496)
    -   ゴミデータのクリーンアップ速度を制限して、 `snapshot apply` への影響を軽減します。 [＃3547](https://github.com/tikv/tikv/pull/3547)
    -   重要なRaftメッセージのコミットメッセージをブロードキャストして、不要な遅延を回避する[＃3592](https://github.com/tikv/tikv/pull/3592)
-   バグ修正
    -   新しく分割されたリージョンの`PreVote`メッセージを破棄することによって発生するリーダー選出の問題を修正しました。 [＃3557](https://github.com/tikv/tikv/pull/3557)
    -   リージョンを統合した後のフォロワー関連の統計を修正 [＃3573](https://github.com/tikv/tikv/pull/3573)
    -   ローカルリーダーが古いリージョン情報を使用する問題を修正[＃3565](https://github.com/tikv/tikv/pull/3565)
