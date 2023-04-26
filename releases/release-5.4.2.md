---
title: TiDB 5.4.2 Release Notes
---

# TiDB 5.4.2 リリースノート {#tidb-5-4-2-release-notes}

リリース日：2022年7月8日

TiDB バージョン: 5.4.2

> **警告：**
>
> このバージョンには既知のバグがあるため、v5.4.2 の使用はお勧めしません。詳細については、 [#12934](https://github.com/tikv/tikv/issues/12934)を参照してください。このバグは v5.4.3 で修正されています。 [v5.4.3](/releases/release-5.4.3.md)を使用することをお勧めします。

## 改良点 {#improvements}

-   TiDB

    -   可用性を向上させるために、異常な TiKV ノードにリクエストを送信しないようにする[#34906](https://github.com/pingcap/tidb/issues/34906)

-   TiKV

    -   更新ごとに TLS 証明書を自動的にリロードして、可用性を向上させます[#12546](https://github.com/tikv/tikv/issues/12546)
    -   TiKV クライアントがリージョンキャッシュを時間[#12398](https://github.com/tikv/tikv/issues/12398)に更新できるように、ヘルス チェックを改善して利用できないRaftstoreを検出します。
    -   リーダーシップを CDC オブザーバーに移管し、レイテンシーのジッターを減らします[#12111](https://github.com/tikv/tikv/issues/12111)

-   PD

    -   デフォルトでswaggerサーバーのコンパイルを無効にする[#4932](https://github.com/tikv/pd/issues/4932)

-   ツール

    -   TiDB Lightning

        -   分散リージョンをバッチ モードに最適化して、分散リージョンプロセスの安定性を向上させます[#33618](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   TiDB

    -   バイナリ プロトコルで間違った TableDual プランがキャッシュされる問題を修正[#34690](https://github.com/pingcap/tidb/issues/34690) [#34678](https://github.com/pingcap/tidb/issues/34678)
    -   EqualAll ケース[#34584](https://github.com/pingcap/tidb/issues/34584)でTiFlash `firstrow`集約関数の null フラグが誤って推論される問題を修正
    -   プランナーがTiFlash [#34682](https://github.com/pingcap/tidb/issues/34682)の間違った 2 フェーズ集計プランを生成する問題を修正します。
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`が有効な場合に発生する Planner の誤った動作を修正します[#34465](https://github.com/pingcap/tidb/issues/34465)
    -   Plan Cache が削除されたときに使用される間違ったメモリ使用量の値を修正します[#34613](https://github.com/pingcap/tidb/issues/34613)
    -   `LOAD DATA`文[#35198](https://github.com/pingcap/tidb/issues/35198)でカラムリストが動かない問題を修正
    -   悲観的トランザクションでエラーを報告しない`WriteConflict` [#11612](https://github.com/tikv/tikv/issues/11612)
    -   リージョンエラーとネットワークの問題が発生した場合、事前書き込み要求がべき等ではない問題を修正します[#34875](https://github.com/pingcap/tidb/issues/34875)
    -   ロールバックされる非同期コミット トランザクションが原子性[#33641](https://github.com/pingcap/tidb/issues/33641)を満たしていない可能性がある問題を修正します。
    -   以前は、ネットワーク接続の問題が発生した場合、TiDB は切断されたセッションによって保持されていたリソースを常に正しく解放するとは限りませんでした。この問題は修正され、開いているトランザクションをロールバックし、関連する他のリソースを解放できるようになりました。 [#34722](https://github.com/pingcap/tidb/issues/34722)
    -   TiDB が CTE [#33965](https://github.com/pingcap/tidb/issues/33965)でビューを照会すると、 `references invalid table`エラーが誤って報告される可能性がある問題を修正します。
    -   `fatal error: concurrent map read and map write`エラー[#35340](https://github.com/pingcap/tidb/issues/35340)によって引き起こされるpanicの問題を修正します。

-   TiKV

    -   `max_sample_size`が`0` [#11192](https://github.com/tikv/tikv/issues/11192)に設定されている場合に統計を分析することによって引き起こされるpanicの問題を修正します
    -   TiKV [#12231](https://github.com/tikv/tikv/issues/12231)の終了時に TiKV パニックを誤って報告する潜在的な問題を修正
    -   ソース ピアがリージョンマージ プロセスでスナップショットによってログをキャッチするときに発生する可能性があるpanicの問題を修正します[#12663](https://github.com/tikv/tikv/issues/12663)
    -   ピアの分割と破棄が同時に行われると発生する可能性があるpanicの問題を修正します[#12825](https://github.com/tikv/tikv/issues/12825)
    -   PD クライアントがエラー[#12345](https://github.com/tikv/tikv/issues/12345)に遭遇したときに発生する PD クライアントの再接続が頻繁に発生する問題を修正します。
    -   `DATETIME`値に分数と`Z` [#12739](https://github.com/tikv/tikv/issues/12739)が含まれている場合に発生する時間解析エラーの問題を修正します。
    -   空の文字列の型変換を実行すると TiKV がパニックになる問題を修正します[#12673](https://github.com/tikv/tikv/issues/12673)
    -   悲観的トランザクションでコミット レコードが重複する可能性がある問題を修正します[#12615](https://github.com/tikv/tikv/issues/12615)
    -   Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)の使用時に TiKV が`invalid store ID 0`エラーを報告する問題を修正
    -   ピアの破棄とリージョン[#12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされる TiKVpanicの問題を修正します。
    -   間違った文字列の一致が原因で tikv-ctl が間違った結果を返す問題を修正します[#12329](https://github.com/tikv/tikv/issues/12329)
    -   AUFS [#12543](https://github.com/tikv/tikv/issues/12543)で TiKV の起動に失敗する問題を修正

-   PD

    -   `not leader` [#4797](https://github.com/tikv/pd/issues/4797)の間違ったステータス コードを修正
    -   ホット リージョンにリーダーがない場合に発生する PDpanicを修正します[#5005](https://github.com/tikv/pd/issues/5005)
    -   PD リーダーの転送[#4769](https://github.com/tikv/pd/issues/4769)の直後にスケジュールを開始できない問題を修正します。
    -   一部のまれなケースでの TSO フォールバックのバグを修正します[#4884](https://github.com/tikv/pd/issues/4884)

-   TiFlash

    -   状況によっては、クラスター化されたインデックスを含むテーブルの列を削除した後にTiFlash がクラッシュする問題を修正します[#5154](https://github.com/pingcap/tiflash/issues/5154)
    -   多数の INSERT 操作と DELETE 操作の後に発生する可能性のあるデータの不整合を修正します[#4956](https://github.com/pingcap/tiflash/issues/4956)
    -   コーナーケースで間違った小数比較結果を修正する[#4512](https://github.com/pingcap/tiflash/issues/4512)

-   ツール

    -   バックアップと復元 (BR)

        -   RawKV モード[#35279](https://github.com/pingcap/tidb/issues/35279)でBR が`ErrRestoreTableIDMismatch`を報告するバグを修正
        -   ファイル保存エラー時にBRがリトライしない不具合を修正[#34865](https://github.com/pingcap/tidb/issues/34865)
        -   BR実行中のpanicの問題を修正[#34956](https://github.com/pingcap/tidb/issues/34956)
        -   BR がS3 内部エラーを処理できない問題を修正します[#34350](https://github.com/pingcap/tidb/issues/34350)
        -   復元操作がいくつかの回復不能なエラーに遭遇したときにBR がスタックするバグを修正します[#33200](https://github.com/pingcap/tidb/issues/33200)

    -   TiCDC

        -   特別な増分スキャン シナリオで発生するデータ損失を修正します[#5468](https://github.com/pingcap/tiflow/issues/5468)
        -   REDO ログマネージャがログを書き込む前にログをフラッシュするバグを修正[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルが REDO ライターによって維持されていない場合、解決された ts の移動が速すぎるというバグを修正します[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   ファイル名の競合によりデータが失われる可能性がある問題を修正します[#5486](https://github.com/pingcap/tiflow/issues/5486)
        -   リージョンリーダーが見つからず、再試行が制限[#5230](https://github.com/pingcap/tiflow/issues/5230)を超えた場合に発生するレプリケーションの中断を修正します。
        -   MySQL Sink が誤ったチェックポイントを保存する可能性があるバグを修正Ts [#5107](https://github.com/pingcap/tiflow/issues/5107)
        -   HTTPサーバーでゴルーチン リークが発生する可能性があるバグを修正します[#5303](https://github.com/pingcap/tiflow/issues/5303)
        -   メタリージョンの変更によりレイテンシーが増加する可能性がある問題を修正します[#4756](https://github.com/pingcap/tiflow/issues/4756) [#4762](https://github.com/pingcap/tiflow/issues/4762)

    -   TiDB データ移行 (DM)

        -   タスクが自動的に再開された後、DM がより多くのディスク領域を占有する問題を修正します[#5344](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合に大文字のテーブルが複製できない問題を修正[#5255](https://github.com/pingcap/tiflow/issues/5255)
