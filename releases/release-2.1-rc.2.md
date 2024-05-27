---
title: TiDB 2.1 RC2 Release Notes
summary: TiDB 2.1 RC2 は、安定性、SQL オプティマイザー、統計、実行エンジンの改善を伴い、2018 年 9 月 14 日にリリースされました。このリリースには、SQL オプティマイザー、SQL 実行エンジン、統計、サーバー、互換性、式、DML、DDL、TiKV Go クライアント、およびテーブル パーティションの機能強化が含まれています。PD 機能、改善、バグ修正も含まれています。TiKV のパフォーマンス、改善、バグ修正もこのリリースの一部です。
---

# TiDB 2.1 RC2 リリースノート {#tidb-2-1-rc2-release-notes}

2018 年 9 月 14 日に、TiDB 2.1 RC2 がリリースされました。TiDB 2.1 RC1 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー
    -   次世代プランナー[＃7543](https://github.com/pingcap/tidb/pull/7543)の提案
    -   定数伝播の最適化ルールを改善する[＃7276](https://github.com/pingcap/tidb/pull/7276)
    -   `Range`の計算ロジックを強化して、複数の`IN`または`EQUAL`条件を同時に処理できるようにします[＃7577](https://github.com/pingcap/tidb/pull/7577)
    -   `Range`空の場合に`TableScan`の推定結果が正しくない問題を修正[＃7583](https://github.com/pingcap/tidb/pull/7583)
    -   `UPDATE`ステートメント[＃7586](https://github.com/pingcap/tidb/pull/7586)の`PointGet`演算子をサポートする
    -   いくつかの条件で`FirstRow`集計関数を実行するプロセス中に発生するpanic問題を修正しました[＃7624](https://github.com/pingcap/tidb/pull/7624)
-   SQL実行エンジン
    -   `HashJoin`オペレータがエラー[＃7554](https://github.com/pingcap/tidb/pull/7554)に遭遇したときに発生する可能性のある`DataRace`問題を修正します
    -   `HashJoin`演算子で内部テーブルを読み取り、同時にハッシュテーブルを構築する[＃7544](https://github.com/pingcap/tidb/pull/7544)
    -   ハッシュ集計演算子のパフォーマンスを最適化する[＃7541](https://github.com/pingcap/tidb/pull/7541)
    -   Join演算子[＃7493](https://github.com/pingcap/tidb/pull/7493) [＃7433](https://github.com/pingcap/tidb/pull/7433)パフォーマンスを最適化する
    -   結合順序が変更されると`UPDATE JOIN`の結果が正しくなくなる問題を修正[＃7571](https://github.com/pingcap/tidb/pull/7571)
    -   チャンクのイテレータ[＃7585](https://github.com/pingcap/tidb/pull/7585)のパフォーマンスを向上させる
-   統計
    -   自動分析作業で統計[＃7550](https://github.com/pingcap/tidb/pull/7550)が繰り返し分析される問題を修正
    -   統計情報の変更がない場合に発生する統計情報更新エラーを修正[＃7530](https://github.com/pingcap/tidb/pull/7530)
    -   `Analyze`リクエスト[＃7496](https://github.com/pingcap/tidb/pull/7496)を構築するときはRC分離レベルと低優先度を使用する
    -   [＃7570](https://github.com/pingcap/tidb/pull/7570)日の特定の期間の統計の自動分析を有効にするサポート 1
    -   統計情報を記録する際のpanic問題を修正[＃7588](https://github.com/pingcap/tidb/pull/7588)
    -   `ANALYZE TABLE WITH BUCKETS`ステートメント[＃7619](https://github.com/pingcap/tidb/pull/7619)を使用してヒストグラム内のバケット数の設定をサポートします。
    -   空のヒストグラムを更新するときにpanicが発生する問題を修正[＃7640](https://github.com/pingcap/tidb/pull/7640)
    -   統計情報[＃7657](https://github.com/pingcap/tidb/pull/7657)を使用した更新`information_schema.tables.data_length`
-   サーバ
    -   トレース関連の依存関係[＃7532](https://github.com/pingcap/tidb/pull/7532)を追加する
    -   Golang [＃7512](https://github.com/pingcap/tidb/pull/7512)の`mutex profile`機能を有効にする
    -   `Admin`文には`Super_priv`権限[＃7486](https://github.com/pingcap/tidb/pull/7486)必要です
    -   `Drop`重要なシステムテーブル[＃7471](https://github.com/pingcap/tidb/pull/7471)へのアクセスを禁止する
    -   `juju/errors`から`pkg/errors` [＃7151](https://github.com/pingcap/tidb/pull/7151)に切り替える
    -   SQLトレース[＃7016](https://github.com/pingcap/tidb/pull/7016)の機能プロトタイプを完成させる
    -   ゴルーチンプール[＃7564](https://github.com/pingcap/tidb/pull/7564)削除する
    -   `USER1`シグナル[＃7587](https://github.com/pingcap/tidb/pull/7587)を使用したゴルーチン情報の表示をサポート
    -   TiDBの起動中に内部SQLを高優先度に設定する[＃7616](https://github.com/pingcap/tidb/pull/7616)
    -   監視メトリクスで内部SQLとユーザーSQLをフィルタリングするために異なるラベルを使用する[＃7631](https://github.com/pingcap/tidb/pull/7631)
    -   過去1週間の最も遅いクエリ上位30件をTiDBサーバー[＃7646](https://github.com/pingcap/tidb/pull/7646)に保存する
    -   TiDBクラスタ[＃7656](https://github.com/pingcap/tidb/pull/7656)のグローバルシステムタイムゾーンを設定する提案を提出する
    -   「GCの有効期間がトランザクション期間より短い」というエラーメッセージを充実させる[＃7658](https://github.com/pingcap/tidb/pull/7658)
    -   TiDBクラスタ[＃7638](https://github.com/pingcap/tidb/pull/7638)を起動するときにグローバルシステムタイムゾーンを設定する
-   互換性
    -   `Year`型[＃7542](https://github.com/pingcap/tidb/pull/7542)に符号なしフラグを追加
    -   `Prepare`モード[＃7525](https://github.com/pingcap/tidb/pull/7525)で`Year`型の結果の長さ`Execute`設定する問題を修正
    -   `Prepare`モードでゼロタイムスタンプ`Execute`挿入される問題を修正[＃7506](https://github.com/pingcap/tidb/pull/7506)
    -   整数除算[＃7492](https://github.com/pingcap/tidb/pull/7492)のエラー処理の問題を修正
    -   `ComStmtSendLongData` [＃7485](https://github.com/pingcap/tidb/pull/7485)の処理時の互換性の問題を修正
    -   文字列を整数[＃7483](https://github.com/pingcap/tidb/pull/7483)に変換するプロセス中のエラー処理の問題を修正
    -   `information_schema.columns_in_table`表[＃7463](https://github.com/pingcap/tidb/pull/7463)の値の精度を最適化する
    -   MariaDB クライアント[＃7573](https://github.com/pingcap/tidb/pull/7573)を使用して文字列型のデータを書き込んだり更新したりする際の互換性の問題を修正しました
    -   戻り値[＃7600](https://github.com/pingcap/tidb/pull/7600)のエイリアスの互換性の問題を修正
    -   `information_schema.COLUMNS`表[＃7602](https://github.com/pingcap/tidb/pull/7602)の float 型の`NUMERIC_SCALE`値が正しくない問題を修正しました
    -   1行コメントが空の場合にパーサーがエラーを報告する問題を修正[＃7612](https://github.com/pingcap/tidb/pull/7612)
-   表現
    -   `insert`関数[＃7528](https://github.com/pingcap/tidb/pull/7528)の`max_allowed_packet`の値を確認する
    -   組み込み関数`json_contains` [＃7443](https://github.com/pingcap/tidb/pull/7443)をサポート
    -   組み込み関数`json_contains_path` [＃7596](https://github.com/pingcap/tidb/pull/7596)をサポート
    -   組み込み関数`encode/decode` [＃7622](https://github.com/pingcap/tidb/pull/7622)をサポート
    -   一部の時間関連関数がMySQLの動作と互換性がないことがある問題を修正[＃7636](https://github.com/pingcap/tidb/pull/7636)
    -   文字列[＃7654](https://github.com/pingcap/tidb/pull/7654)の時刻型データの解析に関する互換性の問題を修正
    -   `DateTime`データ[＃7655](https://github.com/pingcap/tidb/pull/7655)のデフォルト値を計算するときにタイムゾーンが考慮されない問題を修正しました
-   DMML の
    -   `InsertOnDuplicateUpdate`文[＃7534](https://github.com/pingcap/tidb/pull/7534)の`last_insert_id`正しく設定する
    -   `auto_increment_id`カウンタ[＃7515](https://github.com/pingcap/tidb/pull/7515)を更新するケースを減らす
    -   `Duplicate Key` [＃7495](https://github.com/pingcap/tidb/pull/7495)のエラーメッセージを最適化
    -   `insert...select...on duplicate key update`問題を修正[＃7406](https://github.com/pingcap/tidb/pull/7406)
    -   `LOAD DATA IGNORE LINES`ステートメント[＃7576](https://github.com/pingcap/tidb/pull/7576)を支持する
-   DDL
    -   モニター[＃7472](https://github.com/pingcap/tidb/pull/7472)にDDLジョブタイプと現在のスキーマバージョン情報を追加します。
    -   `Admin Restore Table`機能[＃7383](https://github.com/pingcap/tidb/pull/7383)の設計を完了する
    -   `Bit`型のデフォルト値が128を超える問題を修正[＃7249](https://github.com/pingcap/tidb/pull/7249)
    -   `Bit`型のデフォルト値が`NULL` [＃7604](https://github.com/pingcap/tidb/pull/7604)にならない問題を修正
    -   DDLキュー[＃7608](https://github.com/pingcap/tidb/pull/7608)のチェック間隔`CREATE TABLE/DATABASE`減らす
    -   `ddl/owner/resign` HTTPインターフェースを使用してDDL所有者を解放し、新しい所有者の選出を開始します[＃7649](https://github.com/pingcap/tidb/pull/7649)
-   TiKV Go クライアント
    -   `Seek`操作で`Key` [＃7419](https://github.com/pingcap/tidb/pull/7419)しか得られないという問題をサポートする
-   [テーブルパーティション](https://github.com/pingcap/tidb/projects/6) (Experimental)
    -   `Bigint`型をパーティションキー[＃7520](https://github.com/pingcap/tidb/pull/7520)として使用できない問題を修正
    -   パーティションテーブル[＃7437](https://github.com/pingcap/tidb/pull/7437)にインデックスを追加する際に問題が発生した場合のロールバック操作をサポートする

## PD {#pd}

-   特徴
    -   `GetAllStores`インターフェース[＃1228](https://github.com/pingcap/pd/pull/1228)サポート
    -   シミュレータ[＃1218](https://github.com/pingcap/pd/pull/1218)にスケジュール見積もりの​​統計を追加する
-   改善点
    -   ダウンストアの処理プロセスを最適化し、できるだけ早くレプリカを作成します[＃1222](https://github.com/pingcap/pd/pull/1222)
    -   PD [＃1225](https://github.com/pingcap/pd/pull/1225)の再起動によって発生する不要なスケジュールを削減するためにコーディネーターの起動を最適化します。
    -   メモリ使用量を最適化してハートビートによるオーバーヘッドを削減する[＃1195](https://github.com/pingcap/pd/pull/1195)
    -   エラー処理を最適化し、ログ情報を改善する[＃1227](https://github.com/pingcap/pd/pull/1227)
    -   pd-ctl [＃1231](https://github.com/pingcap/pd/pull/1231)で特定のストアのリージョン情報を照会する機能をサポート
    -   pd-ctl [＃1233](https://github.com/pingcap/pd/pull/1233)のバージョン比較に基づいて、topNリージョン情報を照会する機能をサポート
    -   pd-ctl [＃1242](https://github.com/pingcap/pd/pull/1242)でより正確な TSO デコードをサポート
-   バグ修正
    -   pd-ctlが`hot store`コマンドを使用して誤って終了する問題を修正しました[＃1244](https://github.com/pingcap/pd/pull/1244)

## ティクヴ {#tikv}

-   パフォーマンス
    -   I/Oコストを削減するために統計推定に基づいて領域を分割するサポート[＃3511](https://github.com/tikv/tikv/pull/3511)
    -   トランザクションスケジューラ[＃3530](https://github.com/tikv/tikv/pull/3530)クローンを削減
-   改善点
    -   多数の組み込み関数にプッシュダウンのサポートを追加
    -   特定のシナリオでのリーダースケジューリングの失敗の問題を修正するために`leader-transfer-max-log-lag`構成を追加します[＃3507](https://github.com/tikv/tikv/pull/3507)
    -   同時に`tikv-importer`開くエンジンの数を制限するために`max-open-engines`構成を追加します[＃3496](https://github.com/tikv/tikv/pull/3496)
    -   ゴミデータのクリーンアップ速度を制限して、 `snapshot apply` [＃3547](https://github.com/tikv/tikv/pull/3547)への影響を軽減します。
    -   重要なRaftメッセージのコミットメッセージをブロードキャストして、不要な遅延を回避する[＃3592](https://github.com/tikv/tikv/pull/3592)
-   バグの修正
    -   新しく分割されたリージョン[＃3557](https://github.com/tikv/tikv/pull/3557)の`PreVote`メッセージを破棄することによって発生するリーダー選出の問題を修正しました。
    -   地域[＃3573](https://github.com/tikv/tikv/pull/3573)を統合した後のフォロワー関連の統計を修正
    -   ローカルリーダーが古いリージョン情報を使用する問題を修正[＃3565](https://github.com/tikv/tikv/pull/3565)
