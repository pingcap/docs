---
title: TiDB 5.3.2 Release Notes
summary: TiDB 5.3.2 は 2022 年 6 月 29 日にリリースされました。既知のバグがあるため、このバージョンの使用は推奨されません。このバグは v5.3.3 で修正されています。このリリースには、TiDB、PD、TiKV、 TiFlashのほか、TiDB Data Migration、 TiDB Lightning、Backup & Restore、TiCDC、TiDB Data Migration などのさまざまなツールの互換性の変更、改善、バグ修正が含まれています。
---

# TiDB 5.3.2 リリースノート {#tidb-5-3-2-release-notes}

リリース日：2022年6月29日

TiDB バージョン: 5.3.2

> **警告：**
>
> このバージョンには既知のバグがあるため、v5.3.2 の使用は推奨されません。詳細については、 [＃12934](https://github.com/tikv/tikv/issues/12934)参照してください。このバグは v5.3.3 で修正されています。3 [バージョン5.3.3](/releases/release-5.3.3.md)使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   自動IDが範囲外の場合に`REPLACE`文が他の行を誤って変更する問題を修正[＃29483](https://github.com/pingcap/tidb/issues/29483)

-   PD

    -   デフォルトで Swaggerサーバーのコンパイルを無効にする[＃4932](https://github.com/tikv/pd/issues/4932)

## 改善点 {#improvements}

-   ティクヴ

    -   Raftクライアントによるシステムコールを減らしCPU効率を上げる[＃11309](https://github.com/tikv/tikv/issues/11309)
    -   ヘルスチェックを改善して、利用できないRaftstore を検出し、TiKV クライアントが時間内にリージョンキャッシュを更新できるようにします[＃12398](https://github.com/tikv/tikv/issues/12398)
    -   レイテンシージッターを減らすためにリーダーシップをCDCオブザーバーに移譲する[＃12111](https://github.com/tikv/tikv/issues/12111)
    -   モジュール[＃11374](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定するために、 Raftログのガベージコレクションモジュールのメトリックを追加します。

-   ツール

    -   TiDB データ移行 (DM)

        -   Syncer が`/tmp`ではなく DM ワーカーの作業ディレクトリを使用して内部ファイルを書き込み、タスクが停止した後にディレクトリを消去するのをサポートします[＃4107](https://github.com/pingcap/tiflow/issues/4107)

    -   TiDB Lightning

        -   散布リージョンをバッチモードに最適化して、散布リージョンプロセスの安定性を向上させる[＃33618](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   ティビ

    -   Amazon S3 が圧縮データのサイズを正しく計算できない問題を修正[＃30534](https://github.com/pingcap/tidb/issues/30534)
    -   楽観的トランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)でデータインデックスの不整合が発生する可能性がある問題を修正
    -   JSON 型の列が`CHAR`型の列[＃29401](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正しました。
    -   以前は、ネットワーク接続の問題が発生すると、TiDB は切断されたセッションによって保持されたリソースを正しく解放できないことがありました。この問題は修正され、開いているトランザクションをロールバックし、その他の関連リソースを解放できるようになりました[＃34722](https://github.com/pingcap/tidb/issues/34722)
    -   TiDB Binlogを有効にして重複した値を挿入すると発生する`data and columnID count not match`エラーの問題を修正[＃33608](https://github.com/pingcap/tidb/issues/33608)
    -   RC分離レベル[＃34447](https://github.com/pingcap/tidb/issues/34447)でプランキャッシュが開始されるとクエリ結果が間違っている可能性がある問題を修正しました
    -   MySQL バイナリ プロトコル[＃33509](https://github.com/pingcap/tidb/issues/33509)でテーブル スキーマを変更した後にプリペアドステートメントを実行するときに発生するセッションpanicを修正しました。
    -   新しいパーティションが追加されたときにテーブル属性がインデックス化されない問題と、パーティションが変更されたときにテーブル範囲情報が更新されない問題を修正しました[＃33929](https://github.com/pingcap/tidb/issues/33929)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリしたときに TiDBサーバーのメモリが不足する可能性がある問題を修正しました。この問題は、Grafana ダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックしたときに発生する可能性があります。
    -   クラスターの PD ノードが置き換えられた後、一部の DDL ステートメントが一定期間停止する可能性がある問題を修正しました[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   v4.0 [＃33588](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`権限の付与が失敗する可能性がある問題を修正しました。
    -   `left join` [＃31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDBが重複したタスクをTiFlash [＃32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になる問題を修正しました[＃30571](https://github.com/pingcap/tidb/issues/30571)
    -   `fatal error: concurrent map read and map write`エラー[＃35340](https://github.com/pingcap/tidb/issues/35340)によって発生するpanic問題を修正

-   ティクヴ

    -   PDクライアントがエラー[＃12345](https://github.com/tikv/tikv/issues/12345)に遭遇したときに発生するPDクライアントの頻繁な再接続の問題を修正
    -   `DATETIME`値に小数点と`Z` [＃12739](https://github.com/tikv/tikv/issues/12739)が含まれている場合に発生する時間解析エラーの問題を修正しました。
    -   空の文字列の型変換を実行するときに TiKV がパニックになる問題を修正[＃12673](https://github.com/tikv/tikv/issues/12673)
    -   非同期コミットが有効な場合の悲観的トランザクションにおけるコミットレコードの重複の可能性を修正[＃12615](https://github.com/tikv/tikv/issues/12615)
    -   Follower Read [＃12478](https://github.com/tikv/tikv/issues/12478)使用時に TiKV が`invalid store ID 0`エラーを報告するバグを修正
    -   ピアの破壊とリージョン[＃12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の競合によって発生する TiKVpanicの問題を修正しました。
    -   ネットワークが貧弱な場合に、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正しました[＃34066](https://github.com/pingcap/tidb/issues/34066)
    -   マージ対象のリージョンが無効な場合に TiKV がパニックを起こしてピアを予期せず破棄する問題を修正[＃12232](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージにより TiKV がpanicを起こすバグを修正[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリックのオーバーフローによって発生する断続的なパケット損失とメモリ不足 (OOM) の問題を修正しました[＃12160](https://github.com/tikv/tikv/issues/12160)
    -   Ubuntu 18.04 [＃9765](https://github.com/tikv/tikv/issues/9765)でTiKVがプロファイリングを実行するときに発生する潜在的なpanic問題を修正
    -   tikv-ctl が間違った文字列一致のために誤った結果を返す問題を修正[＃12329](https://github.com/tikv/tikv/issues/12329)
    -   レプリカ読み取りが線形化可能性[＃12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   リージョン[＃12048](https://github.com/tikv/tikv/issues/12048)をマージする際に、ターゲットピアが初期化されずに破棄されたピアに置き換えられたときに発生するTiKVpanicの問題を修正しました。
    -   TiKV が 2 年以上実行されている場合にpanicが発生する可能性があるバグを修正[＃11940](https://github.com/tikv/tikv/issues/11940)

-   PD

    -   ホット領域にリーダーがない場合に発生するPDpanicを修正[＃5005](https://github.com/tikv/pd/issues/5005)
    -   PDリーダー移行後すぐにスケジュールを開始できない問題を修正[＃4769](https://github.com/tikv/pd/issues/4769)
    -   PDリーダーの移転後に削除された墓石ストアが再び表示される問題を修正[＃4941](https://github.com/tikv/pd/issues/4941)
    -   いくつかのコーナーケースでの TSO フォールバックのバグを修正[＃4884](https://github.com/tikv/pd/issues/4884)
    -   大容量のストア（たとえば 2T）が存在する場合、完全に割り当てられた小さなストアを検出できず、バランス演算子が生成されない問題を修正しました[＃4805](https://github.com/tikv/pd/issues/4805)
    -   `SchedulerMaxWaitingOperator` `1` [＃4946](https://github.com/tikv/pd/issues/4946)に設定するとスケジューラが動作しない問題を修正
    -   ラベル分布にメトリック[＃4825](https://github.com/tikv/pd/issues/4825)残余ラベルがある問題を修正

-   TiFlash

    -   無効なstorageディレクトリ構成が予期しない動作を引き起こすバグを修正[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   `NOT NULL`列追加時に報告される修正`TiFlash_schema_error` [＃4596](https://github.com/pingcap/tiflash/issues/4596)
    -   `commit state jump backward`エラー[＃2576](https://github.com/pingcap/tiflash/issues/2576)による繰り返しのクラッシュを修正
    -   多数のINSERTおよびDELETE操作後に発生する可能性のあるデータの不整合を修正[＃4956](https://github.com/pingcap/tiflash/issues/4956)
    -   ローカルトンネルが有効になっている場合、キャンセルされた MPP クエリによってタスクが永久にハングアップする可能性があるバグを修正[＃4229](https://github.com/pingcap/tiflash/issues/4229)
    -   TiFlash がリモート読み取り[＃3713](https://github.com/pingcap/tiflash/issues/3713)を使用するときに、 TiFlashのバージョンが一致しないという誤ったレポートを修正しました。
    -   ランダムな gRPC キープアライブ タイムアウトにより MPP クエリが失敗する可能性があるバグを修正[＃4662](https://github.com/pingcap/tiflash/issues/4662)
    -   交換レシーバー[＃3444](https://github.com/pingcap/tiflash/issues/3444)で再試行があると MPP クエリが永久にハングする可能性があるバグを修正しました。
    -   `DATETIME`を`DECIMAL` [＃4151](https://github.com/pingcap/tiflash/issues/4151)にキャストするときに発生する誤った結果を修正
    -   `FLOAT`を`DECIMAL` [＃3998](https://github.com/pingcap/tiflash/issues/3998)にキャストするときに発生するオーバーフローを修正
    -   空の文字列[＃2705](https://github.com/pingcap/tiflash/issues/2705)で`json_length`呼び出す場合に発生する可能性のある`index out of bounds`エラーを修正
    -   コーナーケース[＃4512](https://github.com/pingcap/tiflash/issues/4512)での誤った 10 進数比較結果を修正
    -   結合ビルドステージ[＃4195](https://github.com/pingcap/tiflash/issues/4195)でクエリが失敗した場合に MPP クエリが永久にハングする可能性があるバグを修正しました。
    -   クエリに`where <string>`句[＃3447](https://github.com/pingcap/tiflash/issues/3447)が含まれている場合に発生する可能性のある誤った結果を修正
    -   `CastStringAsReal`動作がTiFlashと TiDB または TiKV [＃3475](https://github.com/pingcap/tiflash/issues/3475)で一致しない問題を修正
    -   文字列を datetime [＃3556](https://github.com/pingcap/tiflash/issues/3556)にキャストする際の誤った`microsecond`修正
    -   削除操作が多数あるテーブルをクエリするときに発生する可能性のあるエラーを修正[＃4747](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが「Keepalive watchdog fired」エラーをランダムに多数報告するバグを修正[＃4192](https://github.com/pingcap/tiflash/issues/4192)
    -   領域範囲に一致しないデータがTiFlashノード[＃4414](https://github.com/pingcap/tiflash/issues/4414)に残るバグを修正
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[＃4238](https://github.com/pingcap/tiflash/issues/4238)
    -   GC [＃4511](https://github.com/pingcap/tiflash/issues/4511)後に空のセグメントをマージできないバグを修正
    -   TLS が有効になっているときに発生するpanic問題を修正[＃4196](https://github.com/pingcap/tiflash/issues/4196)
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正[＃4146](https://github.com/pingcap/tiflash/issues/4146)
    -   無効なstorageディレクトリ構成が予期しない動作を引き起こすバグを修正[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないバグを修正[＃4101](https://github.com/pingcap/tiflash/issues/4101)
    -   読み取り負荷が高い状態で列を追加した後に発生する可能性のあるクエリエラーを修正[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   `STR_TO_DATE()`関数がマイクロ秒を解析するときに先頭のゼロを誤って処理するバグを修正[＃3557](https://github.com/pingcap/tiflash/issues/3557)
    -   TiFlashが再起動後に`EstablishMPPConnection`エラーを返す可能性がある問題を修正しました[＃3615](https://github.com/pingcap/tiflash/issues/3615)

-   ツール

    -   バックアップと復元 (BR)

        -   増分復元後にテーブルにレコードを挿入するときに重複する主キーを修正する[＃33596](https://github.com/pingcap/tidb/issues/33596)
        -   BRまたはTiDB Lightning が異常終了した後にスケジューラが再開しない問題を修正[＃33546](https://github.com/pingcap/tidb/issues/33546)
        -   BR増分リストアが空のクエリ[＃33322](https://github.com/pingcap/tidb/issues/33322)を含む DDL ジョブにより誤ってエラーを返すバグを修正しました。
        -   復元中にリージョンが一致していない場合にBR が十分な回数再試行しない問題を修正[＃33419](https://github.com/pingcap/tidb/issues/33419)
        -   復元操作中に回復不可能なエラーが発生するとBR が停止するバグを修正[＃33200](https://github.com/pingcap/tidb/issues/33200)
        -   BRがRawKV [＃32607](https://github.com/pingcap/tidb/issues/32607)バックアップに失敗する問題を修正
        -   BRがS3内部エラーを処理できない問題を修正[＃34350](https://github.com/pingcap/tidb/issues/34350)

    -   ティCDC

        -   所有者の変更によって生じた誤ったメトリックを修正[＃4774](https://github.com/pingcap/tiflow/issues/4774)
        -   ログを書き込む前にREDOログマネージャがログをフラッシュするバグを修正[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルがREDOライターによってメンテナンスされていない場合に、解決されたTSが速く動きすぎるというバグを修正しました[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   ファイル名の競合によりデータが失われる可能性がある問題を修正するために、REDOログファイル名にUUIDサフィックスを追加します[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   MySQL Sink が間違ったチェックポイントを保存する可能性があるバグを修正しました[＃5107](https://github.com/pingcap/tiflow/issues/5107)
        -   アップグレード後に TiCDC クラスターがpanicになる可能性がある問題を修正[＃5266](https://github.com/pingcap/tiflow/issues/5266)
        -   同じノード[＃4464](https://github.com/pingcap/tiflow/issues/4464)でテーブルが繰り返しスケジュールされると、changefeed が停止する問題を修正しました。
        -   TLS [＃4777](https://github.com/pingcap/tiflow/issues/4777)を有効にした後、 `--pd`で設定した最初の PD が利用できない場合に TiCDC が起動に失敗する問題を修正しました。
        -   PDノードが異常な場合にオープンAPI経由でステータスを照会するとブロックされることがあるバグを修正[＃4778](https://github.com/pingcap/tiflow/issues/4778)
        -   Unified Sorter [＃4447](https://github.com/pingcap/tiflow/issues/4447)で使用されるワーカープールの安定性の問題を修正
        -   一部のケースでシーケンスが誤って複製されるバグを修正[＃4552](https://github.com/pingcap/tiflow/issues/4552)

    -   TiDB データ移行 (DM)

        -   タスクが自動的に再開された後にDMがより多くのディスク領域を占有する問題を修正[＃3734](https://github.com/pingcap/tiflow/issues/3734) [＃5344](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合、大文字テーブルが複製できない問題を修正[＃5255](https://github.com/pingcap/tiflow/issues/5255)
        -   下流でフィルタリングされた DDL を手動で実行すると、タスク再開が失敗する場合がある問題を修正しました[＃5272](https://github.com/pingcap/tiflow/issues/5272)
        -   `SHOW CREATE TABLE`ステートメント[＃5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーpanicの問題を修正しました。
        -   GTID が有効になっている場合やタスクが自動的に再開された場合に CPU 使用率が上昇し、大量のログが出力される問題を修正しました[＃5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DMマスターの再起動後にリレーログが無効になる可能性がある問題を修正[＃4803](https://github.com/pingcap/tiflow/issues/4803)

    -   TiDB Lightning

        -   `auto_increment`列目[＃27937](https://github.com/pingcap/tidb/issues/27937)の範囲外データによるローカルバックエンドインポート失敗の問題を修正
        -   事前チェックでローカルディスクリソースとクラスターの可用性がチェックされない問題を修正[＃34213](https://github.com/pingcap/tidb/issues/34213)
        -   チェックサムエラー「GC の有効期間がトランザクション期間より短い」を修正[＃32733](https://github.com/pingcap/tidb/issues/32733)
