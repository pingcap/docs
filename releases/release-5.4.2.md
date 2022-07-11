---
title: TiDB 5.4.2 Release Notes
---

# TiDB5.4.2リリースノート {#tidb-5-4-2-release-notes}

リリース日：2022年7月8日

TiDBバージョン：5.4.2

## 改善 {#improvements}

-   TiDB

    -   可用性を向上させるために、異常なTiKVノードにリクエストを送信しないでください[＃34906](https://github.com/pingcap/tidb/issues/34906)

-   TiKV

    -   可用性を向上させるために、更新ごとにTLS証明書を自動的に再ロードします[＃12546](https://github.com/tikv/tikv/issues/12546)
    -   ヘルスチェックを改善して、使用できないRaftstoreを検出し、TiKVクライアントが時間[＃12398](https://github.com/tikv/tikv/issues/12398)でリージョンキャッシュを更新できるようにします。
    -   リーダーシップをCDCオブザーバーに移して、レイテンシージッターを減らす[＃12111](https://github.com/tikv/tikv/issues/12111)

-   PD

    -   デフォルトでSwaggerサーバーのコンパイルを無効にする[＃4932](https://github.com/tikv/pd/issues/4932)

-   ツール

    -   TiDB Lightning

        -   スキャッターリージョンプロセスの安定性を向上させるために、スキャッターリージョンをバッチモードに最適化する[＃33618](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   TiDB

    -   バイナリプロトコルにキャッシュされた間違ったTableDualプランの問題を修正し[＃34678](https://github.com/pingcap/tidb/issues/34678) [＃34690](https://github.com/pingcap/tidb/issues/34690)
    -   EqualAllケース[＃34584](https://github.com/pingcap/tidb/issues/34584)での`firstrow`集約関数の誤って推測されたnullフラグの問題を修正します
    -   プランナーがTiFlash1に対して誤った2フェーズ集約プランを生成する問題を修正し[＃34682](https://github.com/pingcap/tidb/issues/34682)
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`が有効になっているときに発生するプランナーの誤った動作を修正します[＃34465](https://github.com/pingcap/tidb/issues/34465)
    -   プランキャッシュが削除されたときに使用される間違ったメモリ使用量の値を修正します[＃34613](https://github.com/pingcap/tidb/issues/34613)
    -   `LOAD DATA`ステートメント[＃35198](https://github.com/pingcap/tidb/issues/35198)で列リストが機能しない問題を修正します。
    -   悲観的なトランザクションで`WriteConflict`エラーを報告することは避けてください[＃11612](https://github.com/tikv/tikv/issues/11612)
    -   リージョンエラーとネットワークの問題が発生したときに、事前書き込み要求がべき等ではないという問題を修正します[＃34875](https://github.com/pingcap/tidb/issues/34875)
    -   ロールバックされる非同期コミットトランザクションがアトミック性[＃33641](https://github.com/pingcap/tidb/issues/33641)を満たさない可能性がある問題を修正します
    -   以前は、ネットワーク接続の問題が発生したときに、TiDBが切断されたセッションによって保持されているリソースを常に正しく解放するとは限りませんでした。この問題は修正され、開いているトランザクションをロールバックしたり、他の関連リソースを解放したりできるようになりました。 [＃34722](https://github.com/pingcap/tidb/issues/34722)
    -   TiDBが[＃33965](https://github.com/pingcap/tidb/issues/33965)でビューをクエリすると、 `references invalid table`のエラーが誤って報告される可能性がある問題を修正します。
    -   `fatal error: concurrent map read and map write`エラー[＃35340](https://github.com/pingcap/tidb/issues/35340)によって引き起こされるpanicの問題を修正します

-   TiKV

    -   `max_sample_size`が[＃11192](https://github.com/tikv/tikv/issues/11192)に設定されているときに統計を分析することによって引き起こされるpanicの問題を修正し`0`
    -   TiKV1を終了するときに誤ってTiKVパニックを報告する潜在的な問題を修正し[＃12231](https://github.com/tikv/tikv/issues/12231)
    -   リージョンマージプロセスでソースピアがスナップショットによってログをキャッチするときに発生する可能性があるpanicの問題を修正します[＃12663](https://github.com/tikv/tikv/issues/12663)
    -   ピアが分割され、同時に破壊されているときに発生する可能性のあるpanicの問題を修正します[＃12825](https://github.com/tikv/tikv/issues/12825)
    -   PDクライアントがエラー[＃12345](https://github.com/tikv/tikv/issues/12345)に遭遇したときに発生する頻繁なPDクライアント再接続の問題を修正します
    -   `DATETIME`の値に小数部と[＃12739](https://github.com/tikv/tikv/issues/12739)が含まれている場合に発生する時間解析エラーの問題を修正し`Z`
    -   空の文字列の型変換を実行するときにTiKVがパニックになる問題を修正します[＃12673](https://github.com/tikv/tikv/issues/12673)
    -   非同期コミットが有効になっている場合に、悲観的なトランザクションで重複する可能性のあるコミットレコードを修正します[＃12615](https://github.com/tikv/tikv/issues/12615)
    -   FollowerRead3を使用するとTiKVが`invalid store ID 0`エラーを報告する問題を修正し[＃12478](https://github.com/tikv/tikv/issues/12478)
    -   ピアの破壊とリージョン[＃12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされるTiKVpanicの問題を修正します
    -   文字列の一致が正しくないためにtikv-ctlが誤った結果を返す問題を修正します[＃12329](https://github.com/tikv/tikv/issues/12329)
    -   AUFS1でTiKVを開始できない問題を修正し[＃12543](https://github.com/tikv/tikv/issues/12543)

-   PD

    -   13の間違ったステータス`not leader`を修正し[＃4797](https://github.com/tikv/pd/issues/4797)
    -   ホットリージョンにリーダーがない場合に発生するPDpanicを修正する[＃5005](https://github.com/tikv/pd/issues/5005)
    -   PDリーダーの転送直後にスケジューリングを開始できない問題を修正します[＃4769](https://github.com/tikv/pd/issues/4769)
    -   一部のコーナーケースでのTSOフォールバックのバグを修正[＃4884](https://github.com/tikv/pd/issues/4884)

-   TiFlash

    -   状況によっては、クラスター化インデックスを含むテーブルの列を削除した後にTiFlashがクラッシュする問題を修正します[＃5154](https://github.com/pingcap/tiflash/issues/5154)
    -   多くのINSERTおよびDELETE操作後の潜在的なデータの不整合を修正します[＃4956](https://github.com/pingcap/tiflash/issues/4956)
    -   コーナーケース[＃4512](https://github.com/pingcap/tiflash/issues/4512)の誤った小数比較結果を修正

-   ツール

    -   バックアップと復元（BR）

        -   BRがRawKVモード[＃35279](https://github.com/pingcap/tidb/issues/35279)で`ErrRestoreTableIDMismatch`を報告するバグを修正します
        -   ファイルの保存中にエラーが発生したときにBRが再試行しないバグを修正します[＃34865](https://github.com/pingcap/tidb/issues/34865)
        -   BRが実行されているときのpanicの問題を修正します[＃34956](https://github.com/pingcap/tidb/issues/34956)
        -   BRがS3内部エラーを処理できない問題を修正します[＃34350](https://github.com/pingcap/tidb/issues/34350)
        -   復元操作で回復不能なエラーが発生したときにBRがスタックするバグを修正します[＃33200](https://github.com/pingcap/tidb/issues/33200)

    -   TiCDC

        -   特別なインクリメンタルスキャンシナリオで発生するデータ損失を修正する[＃5468](https://github.com/pingcap/tiflow/issues/5468)
        -   ログを書き込む前にREDOログマネージャーがログをフラッシュするバグを修正します[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルがREDOライターによって維持されていない場合に、解決されたtsの移動が速すぎるというバグを修正します[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   ファイル名の競合がデータ損失を引き起こす可能性がある問題を修正します[＃5486](https://github.com/pingcap/tiflow/issues/5486)
        -   リージョンリーダーが欠落していて、再試行が制限を超えたときに発生するレプリケーションの中断を修正します[＃5230](https://github.com/pingcap/tiflow/issues/5230)
        -   MySQLSinkが間違ったチェックポイントを保存する可能性があるバグを修正します[＃5107](https://github.com/pingcap/tiflow/issues/5107)
        -   HTTPサーバーでゴルーチンリークを引き起こす可能性のあるバグを修正します[＃5303](https://github.com/pingcap/tiflow/issues/5303)
        -   メタリージョンの変更がレイテンシーの増加につながる可能性がある問題を修正し[＃4762](https://github.com/pingcap/tiflow/issues/4762) [＃4756](https://github.com/pingcap/tiflow/issues/4756)

    -   TiDBデータ移行（DM）

        -   タスクが自動的に再開した後、DMがより多くのディスクスペースを占有する問題を修正します[＃5344](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合に大文字のテーブルを複製できない問題を修正します[＃5255](https://github.com/pingcap/tiflow/issues/5255)
