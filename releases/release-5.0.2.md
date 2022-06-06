---
title: TiDB 5.0.2 Release Notes
---

# TiDB5.0.2リリースノート {#tidb-5-0-2-release-notes}

発売日：2021年6月10日

TiDBバージョン：5.0.2

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   `cdc cli changefeed`コマンドの`--sort-dir`を非推奨にします。代わりに、ユーザーは`cdc server`コマンドで`--sort-dir`を設定できます。 [＃1795](https://github.com/pingcap/tiflow/pull/1795)

## 新機能 {#new-features}

-   TiKV

    -   デフォルトで休止状態機能を有効にする[＃10266](https://github.com/tikv/tikv/pull/10266)

## 改善 {#improvements}

-   TiDB

    -   キャッシュされた統計が最新の場合は、CPU使用率が高くなるのを避けるために、 `mysql.stats_histograms`テーブルを頻繁に[＃24317](https://github.com/pingcap/tidb/pull/24317)ことは避けてください。

-   TiKV

    -   BRは、仮想ホストアドレッシングモード[＃10243](https://github.com/tikv/tikv/pull/10243)を使用してS3互換ストレージをサポートするようになりました。
    -   TiCDCのスキャン速度[＃10151](https://github.com/tikv/tikv/pull/10151)の背圧をサポートする
    -   TiCDCの初期スキャンのメモリ使用量を減らす[＃10133](https://github.com/tikv/tikv/pull/10133)
    -   悲観的なトランザクションでのTiCDCの古い値機能のキャッシュヒット率を改善する[＃10089](https://github.com/tikv/tikv/pull/10089)
    -   ホットスポット書き込みがある場合にリージョンサイズの増加がスプリット速度を超えるという問題を軽減するために、リージョンをより均等に分割します[＃9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   テーブルロックを最適化して、DDLジョブとデータ読み取りが相互にブロックしないようにします
    -   `INTEGER`または`REAL`タイプから`REAL`タイプへのキャストをサポート

-   ツール

    -   TiCDC

        -   テーブルのメモリ消費量の監視メトリックを追加する[＃1885](https://github.com/pingcap/tiflow/pull/1885)
        -   ソート段階[＃1863](https://github.com/pingcap/tiflow/pull/1863)でメモリとCPUの使用量を最適化する
        -   ユーザーの混乱を引き起こす可能性のある不要なログ情報を削除する[＃1759](https://github.com/pingcap/tiflow/pull/1759)

    -   バックアップと復元（BR）

        -   いくつかのあいまいなエラーメッセージを明確にする[＃1132](https://github.com/pingcap/br/pull/1132)
        -   バックアップのクラスタバージョンのチェックをサポート[＃1091](https://github.com/pingcap/br/pull/1091)
        -   `mysql` [＃1078](https://github.com/pingcap/br/pull/1078) [＃1143](https://github.com/pingcap/br/pull/1143)でのシステムテーブルのバックアップと復元のサポート

    -   Dumpling

        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正します[＃280](https://github.com/pingcap/dumpling/pull/280)

## バグの修正 {#bug-fixes}

-   TiDB

    -   場合によっては[＃24717](https://github.com/pingcap/tidb/issues/24717)インデックスとインデックス結合を使用することによって引き起こされるパニックの問題を修正し[＃24547](https://github.com/pingcap/tidb/issues/24547) [＃24716](https://github.com/pingcap/tidb/issues/24716)
    -   準備されたプランキャッシュ`point get`がトランザクション[＃24741](https://github.com/pingcap/tidb/issues/24741)の`point get`ステートメントによって誤って使用される問題を修正します。
    -   照合順序が`ascii_bin`または[＃24569](https://github.com/pingcap/tidb/issues/24569)の場合に間違ったプレフィックスインデックス値を書き込む問題を修正し`latin1_bin`
    -   進行中のトランザクションがGCワーカーによって中断される可能性があるという問題を修正します[＃24591](https://github.com/pingcap/tidb/issues/24591)
    -   `new-collation`が有効になっているが、 `new-row-format`が無効になっている場合に、クラスター化インデックスでポイントクエリが間違ってしまう可能性があるバグを修正します[＃24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフルハッシュ結合[＃24490](https://github.com/pingcap/tidb/pull/24490)のパーティションキーの変換をリファクタリングします
    -   `HAVING`節[＃24045](https://github.com/pingcap/tidb/issues/24045)を含むクエリの計画を作成するときに発生するパニックの問題を修正します
    -   列プルーニングの改善により、 `Apply`および`Join`オペレーターの結果が正しくなくなる問題を修正します[＃23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックされたプライマリロックを解決できないバグを修正します[＃24384](https://github.com/pingcap/tidb/issues/24384)
    -   fm-sketchレコードの重複を引き起こす可能性のある統計のGCの問題を修正します[＃24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観的ロックが`ErrKeyExists`エラー[＃23799](https://github.com/pingcap/tidb/issues/23799)を受け取った場合、不必要な悲観的ロールバックを回避します。
    -   sql_modeに`ANSI_QUOTES`が含まれていると、数値リテラルが認識されない問題を修正し[＃24429](https://github.com/pingcap/tidb/issues/24429) 。
    -   リストされていないパーティションからデータを読み取るための`INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`などのステートメントの禁止[＃24746](https://github.com/pingcap/tidb/issues/24746)
    -   SQLステートメントに`GROUP BY`と[＃24281](https://github.com/pingcap/tidb/issues/24281)の両方が含まれている場合の潜在的な`index out of range`エラーを修正し`UNION` 。
    -   `CONCAT`関数が照合順序[＃24296](https://github.com/pingcap/tidb/issues/24296)を誤って処理する問題を修正します
    -   `collation_server`グローバル変数が新しいセッションで有効にならない問題を修正します[＃24156](https://github.com/pingcap/tidb/pull/24156)

-   TiKV

    -   古い値の読み取りによって引き起こされる[＃9981](https://github.com/tikv/tikv/issues/9981)の問題を修正します[＃9996](https://github.com/tikv/tikv/issues/9996)
    -   照合順序が`latin1_bin`の場合に、クラスター化された主キー列の2次インデックスの値が空になる問題を修正し[＃24548](https://github.com/pingcap/tidb/issues/24548) 。
    -   パニックが発生したときにTiKVがコアダンプファイルを生成できるようにする`abort-on-panic`の構成を追加します。ユーザーは、コアダンプ[＃10216](https://github.com/tikv/tikv/pull/10216)を有効にするために環境を正しく構成する必要があります。
    -   TiKVがビジーでないときに発生する`point get`クエリのパフォーマンスリグレッションの問題を修正します[＃10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗が多い場合にPDリーダーの再選が遅くなる問題を修正[＃3697](https://github.com/tikv/pd/issues/3697)
    -   存在しないストアからエビクトリーダースケジューラを削除するときに発生するパニックの問題を修正します[＃3660](https://github.com/tikv/pd/issues/3660)
    -   オフラインピアがマージされた後に統計が更新されない問題を修正します[＃3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   共有デルタインデックスを同時に複製した場合の誤った結果の問題を修正
    -   TiFlashが不完全なデータで再起動できないという潜在的な問題を修正します
    -   古いdmファイルが自動的に削除されない問題を修正します
    -   圧縮フィルター機能が有効になっているときに発生する可能性のあるパニックを修正します
    -   `ExchangeSender`が重複データを送信するという潜在的な問題を修正します
    -   TiFlashが非同期コミットからフォールバックされたロックを解決できない問題を修正します
    -   `TIMEZONE`タイプのキャスト結果に`TIMESTAMP`タイプが含まれている場合に誤った結果が返される問題を修正しました
    -   セグメント分割中に発生するTiFlashパニックの問題を修正します
    -   非ルートMPPタスクに関する実行情報が正確でない問題を修正します

-   ツール

    -   TiCDC

        -   Avro出力[＃1712](https://github.com/pingcap/tiflow/pull/1712)でタイムゾーン情報が失われる問題を修正します
        -   Unified Sorterで古い一時ファイルのクリーンアップをサポートし、 `sort-dir`ディレクトリの共有を禁止します[＃1742](https://github.com/pingcap/tiflow/pull/1742)
        -   多くの古いリージョンが存在する場合に発生するKVクライアントのデッドロックバグを修正します[＃1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[＃1697](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正します
        -   [＃1750](https://github.com/pingcap/tiflow/pull/1750)にデータを複製するときに`SUPER`特権を必要とする`explicit_defaults_for_timestamp`の更新を元に戻します。
        -   シンクフロー制御をサポートして、メモリオーバーフローのリスクを軽減します[＃1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブルを移動するときにレプリケーションタスクが停止する可能性があるバグを修正します[＃1828](https://github.com/pingcap/tiflow/pull/1828)
        -   TiCDCチェンジフィードチェックポイント[＃1759](https://github.com/pingcap/tiflow/pull/1759)の停滞により、TiKVGCセーフポイントがブロックされる問題を修正します。

    -   バックアップと復元（BR）

        -   ログの復元中に`DELETE`のイベントが失われる問題を修正します[＃1063](https://github.com/pingcap/br/issues/1063)
        -   BRがTiKV1にあまりにも多くの役に立たないRPC要求を送信する原因となるバグを修正し[＃1037](https://github.com/pingcap/br/pull/1037)
        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正します[＃1043](https://github.com/pingcap/br/pull/1043)

    -   TiDB Lightning

        -   KVデータの生成時に発生するTiDBLightningパニックの問題を修正します[＃1127](https://github.com/pingcap/br/pull/1127)
        -   自動コミットが無効になっている場合、TiDBバックエンドモードのTiDBLightningがデータを読み込めない問題を修正します[＃1104](https://github.com/pingcap/br/issues/1104)
        -   データのインポート中にキーの合計サイズがラフトエントリの制限を超えたためにバッチ分割リージョンが失敗するバグを修正します[＃969](https://github.com/pingcap/br/issues/969)
