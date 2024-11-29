---
title: TiDB 5.4.2 Release Notes
summary: TiDB 5.4.2 は 2022 年 7 月 8 日にリリースされました。既知のバグがあるため、このバージョンの使用は推奨されません。このバグは v5.4.3 で修正されています。このリリースには、TiDB、TiKV、PD、およびさまざまなツールの改善と、各コンポーネントのバグ修正が含まれています。これらのバグ修正により、安定性、パフォーマンス、およびエラー処理に関連する問題が解決されます。
---

# TiDB 5.4.2 リリースノート {#tidb-5-4-2-release-notes}

リリース日：2022年7月8日

TiDB バージョン: 5.4.2

> **警告：**
>
> このバージョンには既知のバグがあるため、v5.4.2 の使用は推奨されません。詳細については、 [＃12934](https://github.com/tikv/tikv/issues/12934)参照してください。このバグは v5.4.3 で修正されています。3 [バージョン5.4.3](/releases/release-5.4.3.md)使用することをお勧めします。

## 改善点 {#improvements}

-   ティビ

    -   可用性を向上させるために、不健全な TiKV ノードへのリクエストの送信を避ける[＃34906](https://github.com/pingcap/tidb/issues/34906)

-   ティクヴ

    -   可用性を向上させるために、更新ごとに TLS 証明書を自動的に再読み込みします[＃12546](https://github.com/tikv/tikv/issues/12546)
    -   ヘルスチェックを改善して、利用できないRaftstore を検出し、TiKV クライアントが時間内にリージョンキャッシュを更新できるようにします[＃12398](https://github.com/tikv/tikv/issues/12398)
    -   レイテンシージッターを減らすためにリーダーシップをCDCオブザーバーに移譲する[＃12111](https://github.com/tikv/tikv/issues/12111)

-   PD

    -   デフォルトで Swaggerサーバーのコンパイルを無効にする[＃4932](https://github.com/tikv/pd/issues/4932)

-   ツール

    -   TiDB Lightning

        -   散布リージョンをバッチモードに最適化して、散布リージョンプロセスの安定性を向上させる[＃33618](https://github.com/pingcap/tidb/issues/33618)

## バグ修正 {#bug-fixes}

-   ティビ

    -   バイナリプロトコル[＃34690](https://github.com/pingcap/tidb/issues/34690) [＃34678](https://github.com/pingcap/tidb/issues/34678)に間違った TableDual プランがキャッシュされる問題を修正
    -   EqualAll ケース[＃34584](https://github.com/pingcap/tidb/issues/34584)でTiFlash `firstrow`集計関数の null フラグが誤って推論される問題を修正
    -   プランナーがTiFlash [＃34682](https://github.com/pingcap/tidb/issues/34682)に対して間違った 2 フェーズ集計プランを生成する問題を修正しました。
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`が有効になっているときに発生するプランナーの誤った動作を修正[＃34465](https://github.com/pingcap/tidb/issues/34465)
    -   プランキャッシュが削除されたときに使用される間違ったメモリ使用量の値を修正[＃34613](https://github.com/pingcap/tidb/issues/34613)
    -   `LOAD DATA`ステートメント[＃35198](https://github.com/pingcap/tidb/issues/35198)で列リストが機能しない問題を修正
    -   悲観的トランザクション[＃11612](https://github.com/tikv/tikv/issues/11612)で`WriteConflict`エラーを報告しないようにする
    -   リージョンエラーやネットワークの問題が発生した場合に事前書き込み要求が冪等性を持たない問題を修正[＃34875](https://github.com/pingcap/tidb/issues/34875)
    -   ロールバックされる非同期コミットトランザクションがアトミック性を満たさない可能性がある問題を修正[＃33641](https://github.com/pingcap/tidb/issues/33641)
    -   以前は、ネットワーク接続の問題が発生すると、TiDB は切断されたセッションによって保持されたリソースを正しく解放できないことがありました。この問題は修正され、開いているトランザクションをロールバックし、その他の関連リソースを解放できるようになりました[＃34722](https://github.com/pingcap/tidb/issues/34722)
    -   TiDBがCTE [＃33965](https://github.com/pingcap/tidb/issues/33965)のビューをクエリするときに`references invalid table`エラーが誤って報告される可能性がある問題を修正しました。
    -   `fatal error: concurrent map read and map write`エラー[＃35340](https://github.com/pingcap/tidb/issues/35340)によるpanic問題を修正

-   ティクヴ

    -   `max_sample_size`が`0` [＃11192](https://github.com/tikv/tikv/issues/11192)に設定されている場合に統計を分析すると発生するpanic問題を修正しました
    -   TiKV [＃12231](https://github.com/tikv/tikv/issues/12231)を終了するときに誤って TiKV パニックを報告する潜在的な問題を修正しました。
    -   リージョンマージプロセス[＃12663](https://github.com/tikv/tikv/issues/12663)でソースピアがスナップショットによってログをキャッチアップするときに発生する可能性のあるpanic問題を修正しました。
    -   ピアが同時に分割され、破棄されたときに発生する可能性のあるpanic問題を修正しました[＃12825](https://github.com/tikv/tikv/issues/12825)
    -   PDクライアントがエラー[＃12345](https://github.com/tikv/tikv/issues/12345)に遭遇したときに発生するPDクライアントの頻繁な再接続の問題を修正
    -   `DATETIME`値に小数点が含まれ、 `Z` [＃12739](https://github.com/tikv/tikv/issues/12739)場合に発生する時間解析エラーの問題を修正しました。
    -   空の文字列の型変換を実行するときに TiKV がパニックになる問題を修正[＃12673](https://github.com/tikv/tikv/issues/12673)
    -   非同期コミットが有効な場合の悲観的トランザクションにおけるコミットレコードの重複の可能性を修正[＃12615](https://github.com/tikv/tikv/issues/12615)
    -   Follower Read [＃12478](https://github.com/tikv/tikv/issues/12478)使用時に TiKV が`invalid store ID 0`エラーを報告する問題を修正
    -   ピアの破壊とリージョン[＃12368](https://github.com/tikv/tikv/issues/12368)バッチ分割の競合によって発生する TiKVpanicの問題を修正しました。
    -   tikv-ctl が間違った文字列一致のために誤った結果を返す問題を修正[＃12329](https://github.com/tikv/tikv/issues/12329)
    -   AUFS [＃12543](https://github.com/tikv/tikv/issues/12543)でTiKVを起動できない問題を修正

-   PD

    -   `not leader` [＃4797](https://github.com/tikv/pd/issues/4797)の間違ったステータスコードを修正
    -   ホット領域にリーダーがない場合に発生するPDpanicを修正[＃5005](https://github.com/tikv/pd/issues/5005)
    -   PDリーダー移行後すぐにスケジュールを開始できない問題を修正[＃4769](https://github.com/tikv/pd/issues/4769)
    -   いくつかのコーナーケースでの TSO フォールバックのバグを修正[＃4884](https://github.com/tikv/pd/issues/4884)

-   TiFlash

    -   状況によっては、クラスター化インデックスを持つテーブルの列を削除した後にTiFlash がクラッシュする問題を修正[＃5154](https://github.com/pingcap/tiflash/issues/5154)
    -   多数のINSERTおよびDELETE操作後に発生する可能性のあるデータの不整合を修正[＃4956](https://github.com/pingcap/tiflash/issues/4956)
    -   コーナーケース[＃4512](https://github.com/pingcap/tiflash/issues/4512)での誤った小数比較結果を修正

-   ツール

    -   バックアップと復元 (BR)

        -   RawKVモード[＃35279](https://github.com/pingcap/tidb/issues/35279)でBRが`ErrRestoreTableIDMismatch`報告するバグを修正
        -   ファイルの保存時にエラーが発生したときにBRが再試行しないバグを修正[＃34865](https://github.com/pingcap/tidb/issues/34865)
        -   BR実行中のpanic問題を修正[＃34956](https://github.com/pingcap/tidb/issues/34956)
        -   BRがS3内部エラーを処理できない問題を修正[＃34350](https://github.com/pingcap/tidb/issues/34350)
        -   復元操作中に回復不可能なエラーが発生するとBR が停止するバグを修正[＃33200](https://github.com/pingcap/tidb/issues/33200)

    -   ティCDC

        -   特別な増分スキャンシナリオで発生するデータ損失を修正[＃5468](https://github.com/pingcap/tiflow/issues/5468)
        -   ログを書き込む前にREDOログマネージャがログをフラッシュするバグを修正[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルがREDOライターによってメンテナンスされていない場合に、解決されたTSが速く動きすぎるというバグを修正しました[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   ファイル名の競合によりデータ損失が発生する可能性がある問題を修正[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   リージョンリーダーが見つからず再試行が制限を超えた場合に発生するレプリケーション中断を修正[＃5230](https://github.com/pingcap/tiflow/issues/5230)
        -   MySQL Sink が間違ったチェックポイントを保存する可能性があるバグを修正しました[＃5107](https://github.com/pingcap/tiflow/issues/5107)
        -   HTTPサーバー[＃5303](https://github.com/pingcap/tiflow/issues/5303)で goroutine リークを引き起こす可能性のあるバグを修正
        -   メタリージョンの変更によりレイテンシーが増加する可能性がある問題を修正[＃4756](https://github.com/pingcap/tiflow/issues/4756) [＃4762](https://github.com/pingcap/tiflow/issues/4762)

    -   TiDB データ移行 (DM)

        -   タスクが自動的に再開された後に DM がより多くのディスク領域を占有する問題を修正[＃5344](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合、大文字テーブルを複製できない問題を修正[＃5255](https://github.com/pingcap/tiflow/issues/5255)
