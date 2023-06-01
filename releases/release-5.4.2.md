---
title: TiDB 5.4.2 Release Notes
---

# TiDB 5.4.2 リリースノート {#tidb-5-4-2-release-notes}

リリース日：2022年7月8日

TiDB バージョン: 5.4.2

> **警告：**
>
> このバージョンには既知のバグがあるため、v5.4.2 の使用はお勧めできません。詳細は[<a href="https://github.com/tikv/tikv/issues/12934">#12934</a>](https://github.com/tikv/tikv/issues/12934)を参照してください。このバグは v5.4.3 で修正されました。 [<a href="/releases/release-5.4.3.md">v5.4.3</a>](/releases/release-5.4.3.md)を使用することをお勧めします。

## 改善点 {#improvements}

-   TiDB

    -   可用性を向上させるために、異常な TiKV ノードへのリクエストの送信を回避します[<a href="https://github.com/pingcap/tidb/issues/34906">#34906</a>](https://github.com/pingcap/tidb/issues/34906)

-   TiKV

    -   可用性を向上させるために更新ごとに TLS 証明書を自動的にリロードする[<a href="https://github.com/tikv/tikv/issues/12546">#12546</a>](https://github.com/tikv/tikv/issues/12546)
    -   ヘルスチェックを改善して、利用できないRaftstoreを検出し、TiKV クライアントが時間内にリージョンキャッシュを更新できるようにします[<a href="https://github.com/tikv/tikv/issues/12398">#12398</a>](https://github.com/tikv/tikv/issues/12398)
    -   リーダーシップを CDC オブザーバーに移管して、レイテンシージッター[<a href="https://github.com/tikv/tikv/issues/12111">#12111</a>](https://github.com/tikv/tikv/issues/12111)を削減します。

-   PD

    -   Swaggerサーバーのコンパイルをデフォルトで無効にする[<a href="https://github.com/tikv/pd/issues/4932">#4932</a>](https://github.com/tikv/pd/issues/4932)

-   ツール

    -   TiDB Lightning

        -   散乱リージョンプロセスの安定性を向上させるために、散乱リージョンをバッチ モードに最適化します[<a href="https://github.com/pingcap/tidb/issues/33618">#33618</a>](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   TiDB

    -   バイナリ プロトコルでキャッシュされた間違った TableDual プランの問題を修正[<a href="https://github.com/pingcap/tidb/issues/34690">#34690</a>](https://github.com/pingcap/tidb/issues/34690) [<a href="https://github.com/pingcap/tidb/issues/34678">#34678</a>](https://github.com/pingcap/tidb/issues/34678)
    -   EqualAll ケース[<a href="https://github.com/pingcap/tidb/issues/34584">#34584</a>](https://github.com/pingcap/tidb/issues/34584)におけるTiFlash `firstrow`集計関数の null フラグが誤って推論される問題を修正
    -   プランナーがTiFlash [<a href="https://github.com/pingcap/tidb/issues/34682">#34682</a>](https://github.com/pingcap/tidb/issues/34682)に対して間違った 2 フェーズ集約プランを生成する問題を修正
    -   `tidb_opt_agg_push_down`と`tidb_enforce_mpp`が有効になっている場合に発生するプランナーの誤った動作を修正します[<a href="https://github.com/pingcap/tidb/issues/34465">#34465</a>](https://github.com/pingcap/tidb/issues/34465)
    -   プラン キャッシュが削除されるときに使用される間違ったメモリ使用量の値を修正します[<a href="https://github.com/pingcap/tidb/issues/34613">#34613</a>](https://github.com/pingcap/tidb/issues/34613)
    -   `LOAD DATA`ステートメント[<a href="https://github.com/pingcap/tidb/issues/35198">#35198</a>](https://github.com/pingcap/tidb/issues/35198)で列リストが機能しない問題を修正
    -   悲観的トランザクションでのエラーの報告を避ける`WriteConflict` [<a href="https://github.com/tikv/tikv/issues/11612">#11612</a>](https://github.com/tikv/tikv/issues/11612)
    -   リージョンエラーやネットワークの問題が発生した場合に事前書き込みリクエストがべき等にならない問題を修正[<a href="https://github.com/pingcap/tidb/issues/34875">#34875</a>](https://github.com/pingcap/tidb/issues/34875)
    -   ロールバックされる非同期コミットトランザクションがアトミック性[<a href="https://github.com/pingcap/tidb/issues/33641">#33641</a>](https://github.com/pingcap/tidb/issues/33641)を満たさない可能性がある問題を修正
    -   以前は、ネットワーク接続の問題が発生した場合、TiDB は切断されたセッションによって保持されているリソースを常に正しく解放するとは限りませんでした。この問題は修正され、開いているトランザクションをロールバックして、その他の関連リソースを解放できるようになりました。 [<a href="https://github.com/pingcap/tidb/issues/34722">#34722</a>](https://github.com/pingcap/tidb/issues/34722)
    -   TiDB が CTE [<a href="https://github.com/pingcap/tidb/issues/33965">#33965</a>](https://github.com/pingcap/tidb/issues/33965)でビューをクエリするときに`references invalid table`エラーが誤って報告される可能性がある問題を修正
    -   `fatal error: concurrent map read and map write`エラー[<a href="https://github.com/pingcap/tidb/issues/35340">#35340</a>](https://github.com/pingcap/tidb/issues/35340)によって引き起こされるpanicの問題を修正

-   TiKV

    -   `max_sample_size`が`0` [<a href="https://github.com/tikv/tikv/issues/11192">#11192</a>](https://github.com/tikv/tikv/issues/11192)に設定されている場合に統計を分析することによって引き起こされるpanicの問題を修正
    -   TiKV [<a href="https://github.com/tikv/tikv/issues/12231">#12231</a>](https://github.com/tikv/tikv/issues/12231)を終了するときに TiKV パニックを誤って報告する潜在的な問題を修正
    -   リージョンマージ プロセス[<a href="https://github.com/tikv/tikv/issues/12663">#12663</a>](https://github.com/tikv/tikv/issues/12663)でソース ピアがスナップショットによってログを追いつくときに発生する可能性があるpanicの問題を修正します。
    -   ピアの分割と破棄が同時に行われるときに発生する可能性があるpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/12825">#12825</a>](https://github.com/tikv/tikv/issues/12825)
    -   PD クライアントでエラー[<a href="https://github.com/tikv/tikv/issues/12345">#12345</a>](https://github.com/tikv/tikv/issues/12345)が発生したときに発生する PD クライアントの再接続が頻繁に発生する問題を修正します。
    -   `DATETIME`値に小数と`Z` [<a href="https://github.com/tikv/tikv/issues/12739">#12739</a>](https://github.com/tikv/tikv/issues/12739)が含まれる場合に発生する時刻解析エラーの問題を修正します。
    -   空の文字列の型変換を実行すると TiKV がパニックになる問題を修正[<a href="https://github.com/tikv/tikv/issues/12673">#12673</a>](https://github.com/tikv/tikv/issues/12673)
    -   非同期コミットが有効になっている場合に、悲観的トランザクションで発生する可能性のある重複コミット レコードを修正します[<a href="https://github.com/tikv/tikv/issues/12615">#12615</a>](https://github.com/tikv/tikv/issues/12615)
    -   Follower Read [<a href="https://github.com/tikv/tikv/issues/12478">#12478</a>](https://github.com/tikv/tikv/issues/12478)を使用すると TiKV が`invalid store ID 0`エラーを報告する問題を修正
    -   ピアの破棄とリージョン[<a href="https://github.com/tikv/tikv/issues/12368">#12368</a>](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされる TiKVpanicの問題を修正します。
    -   間違った文字列一致[<a href="https://github.com/tikv/tikv/issues/12329">#12329</a>](https://github.com/tikv/tikv/issues/12329)が原因で tikv-ctl が間違った結果を返す問題を修正
    -   AUFS [<a href="https://github.com/tikv/tikv/issues/12543">#12543</a>](https://github.com/tikv/tikv/issues/12543)で TiKV の起動に失敗する問題を修正

-   PD

    -   `not leader` [<a href="https://github.com/tikv/pd/issues/4797">#4797</a>](https://github.com/tikv/pd/issues/4797)の間違ったステータス コードを修正
    -   ホット リージョンにリーダー[<a href="https://github.com/tikv/pd/issues/5005">#5005</a>](https://github.com/tikv/pd/issues/5005)がない場合に発生する PDpanicを修正しました。
    -   PDリーダー転送[<a href="https://github.com/tikv/pd/issues/4769">#4769</a>](https://github.com/tikv/pd/issues/4769)直後にスケジューリングが開始できない問題を修正
    -   いくつかの特殊なケースにおける TSO フォールバックのバグを修正[<a href="https://github.com/tikv/pd/issues/4884">#4884</a>](https://github.com/tikv/pd/issues/4884)

-   TiFlash

    -   状況によっては、クラスター化インデックスを持つテーブルの列を削除した後にTiFlash がクラッシュする問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/5154">#5154</a>](https://github.com/pingcap/tiflash/issues/5154)
    -   多数の INSERT および DELETE 操作後の潜在的なデータの不整合を修正[<a href="https://github.com/pingcap/tiflash/issues/4956">#4956</a>](https://github.com/pingcap/tiflash/issues/4956)
    -   特殊なケースでの間違った 10 進比較結果を修正[<a href="https://github.com/pingcap/tiflash/issues/4512">#4512</a>](https://github.com/pingcap/tiflash/issues/4512)

-   ツール

    -   バックアップと復元 (BR)

        -   RawKVモード[<a href="https://github.com/pingcap/tidb/issues/35279">#35279</a>](https://github.com/pingcap/tidb/issues/35279)でBRが`ErrRestoreTableIDMismatch`を報告するバグを修正
        -   ファイル保存時にエラーが発生した場合にBRがリトライしないバグを修正[<a href="https://github.com/pingcap/tidb/issues/34865">#34865</a>](https://github.com/pingcap/tidb/issues/34865)
        -   BR実行時のpanicの問題を修正[<a href="https://github.com/pingcap/tidb/issues/34956">#34956</a>](https://github.com/pingcap/tidb/issues/34956)
        -   BR がS3 内部エラーを処理できない問題を修正[<a href="https://github.com/pingcap/tidb/issues/34350">#34350</a>](https://github.com/pingcap/tidb/issues/34350)
        -   復元操作で回復不能なエラーが発生した場合にBR がスタックするバグを修正[<a href="https://github.com/pingcap/tidb/issues/33200">#33200</a>](https://github.com/pingcap/tidb/issues/33200)

    -   TiCDC

        -   特別な増分スキャン シナリオ[<a href="https://github.com/pingcap/tiflow/issues/5468">#5468</a>](https://github.com/pingcap/tiflow/issues/5468)で発生するデータ損失を修正します。
        -   REDO ログ マネージャーがログを書き込む前にログをフラッシュするバグを修正[<a href="https://github.com/pingcap/tiflow/issues/5486">#5486</a>](https://github.com/pingcap/tiflow/issues/5486)
        -   一部のテーブルが REDO ライターによって維持されていない場合、解決された ts の移動が速すぎるバグを修正します[<a href="https://github.com/pingcap/tiflow/issues/5486">#5486</a>](https://github.com/pingcap/tiflow/issues/5486)
        -   ファイル名の競合によりデータ損失が発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/5486">#5486</a>](https://github.com/pingcap/tiflow/issues/5486)
        -   リージョンリーダーが見つからず、再試行が制限[<a href="https://github.com/pingcap/tiflow/issues/5230">#5230</a>](https://github.com/pingcap/tiflow/issues/5230)を超えた場合に発生するレプリケーションの中断を修正しました。
        -   MySQL シンクが間違ったチェックポイント Ts [<a href="https://github.com/pingcap/tiflow/issues/5107">#5107</a>](https://github.com/pingcap/tiflow/issues/5107)を保存する可能性があるバグを修正
        -   HTTPサーバーで goroutine リークを引き起こす可能性があるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/5303">#5303</a>](https://github.com/pingcap/tiflow/issues/5303)
        -   メタリージョンの変更によりレイテンシーが増加する可能性がある問題を修正[<a href="https://github.com/pingcap/tiflow/issues/4756">#4756</a>](https://github.com/pingcap/tiflow/issues/4756) [<a href="https://github.com/pingcap/tiflow/issues/4762">#4762</a>](https://github.com/pingcap/tiflow/issues/4762)

    -   TiDB データ移行 (DM)

        -   タスクが自動的に再開された後、DM がより多くのディスク領域を占有する問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/5344">#5344</a>](https://github.com/pingcap/tiflow/issues/5344)
        -   `case-sensitive: true`が設定されていない場合、大文字のテーブルが複製できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/5255">#5255</a>](https://github.com/pingcap/tiflow/issues/5255)
