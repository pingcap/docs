---
title: TiDB 5.3.2 Release Notes
---

# TiDB5.3.2リリースノート {#tidb-5-3-2-release-notes}

リリース日：2022年6月29日

TiDBバージョン：5.3.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   自動IDが範囲[＃29483](https://github.com/pingcap/tidb/issues/29483)から外れると、 `REPLACE`ステートメントが他の行を誤って変更する問題を修正します。

-   PD

    -   デフォルトでSwaggerサーバーのコンパイルを無効にする[＃4932](https://github.com/tikv/pd/issues/4932)

## 改善 {#improvements}

-   TiKV

    -   Raftクライアントによるシステムコールを減らし、CPU効率を向上させます[＃11309](https://github.com/tikv/tikv/issues/11309)
    -   ヘルスチェックを改善して、使用できないRaftstoreを検出し、TiKVクライアントが時間[＃12398](https://github.com/tikv/tikv/issues/12398)でリージョンキャッシュを更新できるようにします。
    -   リーダーシップをCDCオブザーバーに移して、レイテンシージッターを減らす[＃12111](https://github.com/tikv/tikv/issues/12111)
    -   モジュール[＃11374](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定するために、 Raftログのガベージコレクションモジュールのメトリックを追加します。

-   ツール

    -   TiDBデータ移行（DM）

        -   `/tmp`ではなくDM-workerの作業ディレクトリを使用して内部ファイルを書き込み、タスクの停止後にディレクトリをクリーンアップするSyncerをサポートします[＃4107](https://github.com/pingcap/tiflow/issues/4107)

    -   TiDB Lightning

        -   スキャッターリージョンプロセスの安定性を向上させるために、スキャッターリージョンをバッチモードに最適化する[＃33618](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   TiDB

    -   AmazonS3が圧縮データのサイズを正しく計算できない問題を修正します[＃30534](https://github.com/pingcap/tidb/issues/30534)
    -   楽観的なトランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータインデックスの不整合の問題を修正します
    -   JSON型の列が`CHAR`型の列に結合するとSQL操作がキャンセルされる問題を修正します[＃29401](https://github.com/pingcap/tidb/issues/29401)
    -   以前は、ネットワーク接続の問題が発生したときに、TiDBが切断されたセッションによって保持されているリソースを常に正しく解放するとは限りませんでした。この問題は修正され、開いているトランザクションをロールバックしたり、他の関連リソースを解放したりできるようになりました。 [＃34722](https://github.com/pingcap/tidb/issues/34722)
    -   Binlogを有効にして重複値を挿入するときに発生する`data and columnID count not match`エラーの問題を修正します[＃33608](https://github.com/pingcap/tidb/issues/33608)
    -   プランキャッシュがRC分離レベル[＃34447](https://github.com/pingcap/tidb/issues/34447)で開始されたときに、クエリ結果が間違っている可能性がある問題を修正します。
    -   MySQLバイナリプロトコルでテーブルスキーマを変更した後にプリペアドステートメントを実行するときに発生するセッションpanicを修正します[＃33509](https://github.com/pingcap/tidb/issues/33509)
    -   新しいパーティションが追加されたときにテーブル属性がインデックスに登録されない問題と、パーティションが変更されたときにテーブル範囲情報が更新されない問題を修正します[＃33929](https://github.com/pingcap/tidb/issues/33929)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`のテーブルが照会されたときにTiDBサーバーのメモリが不足する可能性がある問題を修正します。この問題は、Grafanaダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックしたときに発生する可能性があります
    -   クラスタのPDノードが置き換えられた後、一部のDDLステートメントが一定期間スタックする可能性がある問題を修正します[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   [＃33588](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`の特権の付与が失敗する可能性がある問題を修正します。
    -   `left join`を使用して複数のテーブルのデータを削除した誤った結果を[＃31321](https://github.com/pingcap/tidb/issues/31321)
    -   TiDBが重複タスクをTiFlash1にディスパッチする可能性があるバグを修正し[＃32814](https://github.com/pingcap/tidb/issues/32814)
    -   TiDBのバックグラウンドHTTPサービスが正常に終了せず、クラスタが異常な状態になる可能性がある問題を修正します[＃30571](https://github.com/pingcap/tidb/issues/30571)
    -   `fatal error: concurrent map read and map write`エラー[＃35340](https://github.com/pingcap/tidb/issues/35340)によって引き起こされるpanicの問題を修正します

-   TiKV

    -   PDクライアントがエラー[＃12345](https://github.com/tikv/tikv/issues/12345)に遭遇したときに発生する頻繁なPDクライアント再接続の問題を修正します
    -   `DATETIME`の値に小数部と[＃12739](https://github.com/tikv/tikv/issues/12739)が含まれている場合に発生する時間解析エラーの問題を修正し`Z`
    -   空の文字列の型変換を実行するときにTiKVがパニックになる問題を修正します[＃12673](https://github.com/tikv/tikv/issues/12673)
    -   非同期コミットが有効になっている場合に、悲観的なトランザクションで重複する可能性のあるコミットレコードを修正します[＃12615](https://github.com/tikv/tikv/issues/12615)
    -   FollowerRead3を使用するとTiKVが`invalid store ID 0`エラーを報告するバグを修正し[＃12478](https://github.com/tikv/tikv/issues/12478)
    -   ピアの破壊とリージョン[＃12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされるTiKVpanicの問題を修正します
    -   ネットワークが貧弱な場合に、正常にコミットされた楽観的なトランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します[＃34066](https://github.com/pingcap/tidb/issues/34066)
    -   マージするターゲットリージョンが無効な場合にTiKVがパニックになり、ピアを予期せず破壊する問題を修正します[＃12232](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージが原因でTiKVがpanicになるバグを修正します[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリックのオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足（OOM）の問題を修正します[＃12160](https://github.com/tikv/tikv/issues/12160)
    -   TiKVが[＃9765](https://github.com/tikv/tikv/issues/9765)でプロファイリングを実行するときに発生する可能性のあるpanicの問題を修正します。
    -   文字列の一致が正しくないためにtikv-ctlが誤った結果を返す問題を修正します[＃12329](https://github.com/tikv/tikv/issues/12329)
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[＃12109](https://github.com/tikv/tikv/issues/12109)
    -   ターゲットピアがリージョン[＃12048](https://github.com/tikv/tikv/issues/12048)のマージ時に初期化されずに破棄されたピアに置き換えられたときに発生するTiKVpanicの問題を修正します。
    -   TiKVが2年以上実行されている場合にpanicになる可能性があるバグを修正します[＃11940](https://github.com/tikv/tikv/issues/11940)

-   PD

    -   ホットリージョンにリーダーがない場合に発生するPDpanicを修正する[＃5005](https://github.com/tikv/pd/issues/5005)
    -   PDリーダーの転送直後にスケジューリングを開始できない問題を修正します[＃4769](https://github.com/tikv/pd/issues/4769)
    -   PDリーダーの転送後に削除されたトゥームストーンストアが再び表示される問題を修正します[＃4941](https://github.com/tikv/pd/issues/4941)
    -   一部のコーナーケースでのTSOフォールバックのバグを修正[＃4884](https://github.com/tikv/pd/issues/4884)
    -   大容量のストア（たとえば2T）が存在する場合、完全に割り当てられた小さなストアを検出できず、バランス演算子が生成されないという問題を修正します[＃4805](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator`が[＃4946](https://github.com/tikv/pd/issues/4946)に設定されているとスケジューラが機能しない問題を修正し`1`
    -   ラベル分布のメトリックにラベルが残っている問題を修正します[＃4825](https://github.com/tikv/pd/issues/4825)

-   TiFlash

    -   無効なストレージディレクトリ構成が予期しない動作につながるバグを修正します[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   `NOT NULL`列が追加されたときに報告される[＃4596](https://github.com/pingcap/tiflash/issues/4596) `TiFlash_schema_error`
    -   `commit state jump backward`のエラーによって引き起こされる繰り返しのクラッシュを修正します[＃2576](https://github.com/pingcap/tiflash/issues/2576)
    -   多くのINSERTおよびDELETE操作後の潜在的なデータの不整合を修正します[＃4956](https://github.com/pingcap/tiflash/issues/4956)
    -   ローカルトンネルが有効になっている場合、MPPクエリをキャンセルすると、タスクが永久にハングする可能性があるバグを修正します[＃4229](https://github.com/pingcap/tiflash/issues/4229)
    -   TiFlashがリモート読み取りを使用する場合の一貫性のないTiFlashバージョンの誤ったレポートを修正[＃3713](https://github.com/pingcap/tiflash/issues/3713)
    -   ランダムなgRPCキープアライブタイムアウトが原因でMPPクエリが失敗する可能性があるバグを修正します[＃4662](https://github.com/pingcap/tiflash/issues/4662)
    -   Exchangeレシーバー[＃3444](https://github.com/pingcap/tiflash/issues/3444)で再試行が行われると、MPPクエリが永久にハングする可能性があるバグを修正します。
    -   `DATETIME`から[＃4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正し`DECIMAL`
    -   `FLOAT`から[＃3998](https://github.com/pingcap/tiflash/issues/3998)をキャストするときに発生するオーバーフローを修正し`DECIMAL`
    -   空の文字列[＃2705](https://github.com/pingcap/tiflash/issues/2705)で`json_length`を呼び出す場合の潜在的な`index out of bounds`エラーを修正します
    -   コーナーケース[＃4512](https://github.com/pingcap/tiflash/issues/4512)の誤った小数比較結果を修正
    -   結合ビルドステージ[＃4195](https://github.com/pingcap/tiflash/issues/4195)でクエリが失敗した場合、MPPクエリが永久にハングする可能性があるバグを修正します。
    -   クエリに`where <string>`句[＃3447](https://github.com/pingcap/tiflash/issues/3447)が含まれている場合に発生する可能性のある誤った結果を修正
    -   `CastStringAsReal`の動作がTiFlashとTiDBまたはTiKV3で一貫していない問題を修正し[＃3475](https://github.com/pingcap/tiflash/issues/3475)
    -   文字列を日時[＃3556](https://github.com/pingcap/tiflash/issues/3556)にキャストするときの誤った`microsecond`を修正
    -   多くの削除操作があるテーブルでクエリを実行するときに発生する可能性のあるエラーを修正する[＃4747](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが多くの「キープアライブウォッチドッグ起動」エラーをランダムに報告するバグを修正します[＃4192](https://github.com/pingcap/tiflash/issues/4192)
    -   どの領域範囲にも一致しないデータがTiFlashノード[＃4414](https://github.com/pingcap/tiflash/issues/4414)に残るバグを修正します
    -   MPPタスクがスレッドを永久にリークする可能性があるバグを修正します[＃4238](https://github.com/pingcap/tiflash/issues/4238)
    -   GC1の後に空のセグメントをマージできないバグを修正し[＃4511](https://github.com/pingcap/tiflash/issues/4511)
    -   TLSが有効になっているときに発生するpanicの問題を修正します[＃4196](https://github.com/pingcap/tiflash/issues/4196)
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正します[＃4146](https://github.com/pingcap/tiflash/issues/4146)
    -   無効なストレージディレクトリ構成が予期しない動作につながるバグを修正します[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないというバグを修正します[＃4101](https://github.com/pingcap/tiflash/issues/4101)
    -   読み取りワークロードが重い場合に列を追加した後の潜在的なクエリエラーを修正する[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   マイクロ秒[＃3557](https://github.com/pingcap/tiflash/issues/3557)を解析するときに、 `STR_TO_DATE()`関数が先行ゼロを誤って処理するバグを修正します。
    -   TiFlashが再起動後に`EstablishMPPConnection`エラーを返す可能性がある問題を修正します[＃3615](https://github.com/pingcap/tiflash/issues/3615)

-   ツール

    -   バックアップと復元（BR）

        -   インクリメンタル復元後にレコードをテーブルに挿入するときに重複する主キーを修正する[＃33596](https://github.com/pingcap/tidb/issues/33596)
        -   BRまたはTiDB Lightningが異常終了した後にスケジューラが再開しない問題を修正します[＃33546](https://github.com/pingcap/tidb/issues/33546)
        -   空のクエリ[＃33322](https://github.com/pingcap/tidb/issues/33322)を使用したDDLジョブが原因で、BRインクリメンタルリストアが誤ってエラーを返すバグを修正します。
        -   復元中にリージョンに一貫性がない場合にBRが十分な回数再試行しない問題を修正します[＃33419](https://github.com/pingcap/tidb/issues/33419)
        -   復元操作で回復不能なエラーが発生したときにBRがスタックするバグを修正します[＃33200](https://github.com/pingcap/tidb/issues/33200)
        -   BRがRawKV1のバックアップに失敗する問題を修正し[＃32607](https://github.com/pingcap/tidb/issues/32607)
        -   BRがS3内部エラーを処理できない問題を修正します[＃34350](https://github.com/pingcap/tidb/issues/34350)

    -   TiCDC

        -   所有者の変更によって引き起こされた誤ったメトリックを修正する[＃4774](https://github.com/pingcap/tiflow/issues/4774)
        -   ログを書き込む前にREDOログマネージャーがログをフラッシュするバグを修正します[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルがREDOライターによって維持されていない場合に、解決されたtsの移動が速すぎるというバグを修正します[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   UUIDサフィックスをREDOログファイル名に追加して、ファイル名の競合によりデータが失われる可能性があるという問題を修正します[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   MySQLSinkが間違ったチェックポイントを保存する可能性があるバグを修正します[＃5107](https://github.com/pingcap/tiflow/issues/5107)
        -   アップグレード後にTiCDCクラスターがpanicになる可能性がある問題を修正します[＃5266](https://github.com/pingcap/tiflow/issues/5266)
        -   テーブルが同じノードで繰り返しスケジュールされている場合にchangefeedがスタックする問題を修正します[＃4464](https://github.com/pingcap/tiflow/issues/4464)
        -   TLSを有効にした後、 `--pd`に設定された最初のPDが使用できない場合にTiCDCが起動しない問題を修正します[＃4777](https://github.com/pingcap/tiflow/issues/4777)
        -   PDノードが異常な場合にオープンAPIを介したステータスのクエリがブロックされる可能性があるバグを修正します[＃4778](https://github.com/pingcap/tiflow/issues/4778)
        -   UnifiedSorter1で使用されるworkerpoolの安定性の問題を修正し[＃4447](https://github.com/pingcap/tiflow/issues/4447)
        -   シーケンスが誤って複製される場合があるバグを修正します[＃4563](https://github.com/pingcap/tiflow/issues/4552)

    -   TiDBデータ移行（DM）

        -   タスクが自動的に再開した後、DMがより多くのディスクスペースを占有する問題を修正します[＃3734](https://github.com/pingcap/tiflow/issues/3734) [＃5344](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合に大文字のテーブルを複製できない問題を修正します[＃5255](https://github.com/pingcap/tiflow/issues/5255)
        -   場合によっては、ダウンストリームでフィルター処理されたDDLを手動で実行すると、タスクの再開が失敗する可能性があるという問題を修正します[＃5272](https://github.com/pingcap/tiflow/issues/5272)
        -   `SHOW CREATE TABLE`ステートメント[＃5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの最初に主キーがない場合に発生するDMワーカーのpanicの問題を修正します。
        -   GTIDを有効にした場合、またはタスクが自動的に再開された場合に、CPU使用率が増加し、大量のログが出力される可能性がある問題を修正します[＃5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DMマスターの再起動後にリレーログが無効になる可能性がある問題を修正します[＃4803](https://github.com/pingcap/tiflow/issues/4803)

    -   TiDB Lightning

        -   `auto_increment`列[＃27937](https://github.com/pingcap/tidb/issues/27937)の範囲外のデータが原因で発生するローカルバックエンドのインポートエラーの問題を修正します。
        -   事前チェックでローカルディスクリソースとクラスタの可用性がチェックされない問題を修正します[＃34213](https://github.com/pingcap/tidb/issues/34213)
        -   チェックサムエラー「GCの有効期間がトランザクション期間より短い」を修正[＃32733](https://github.com/pingcap/tidb/issues/32733)
