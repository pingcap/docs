---
title: TiDB 5.0.2 Release Notes
---

# TiDB 5.0.2 リリースノート {#tidb-5-0-2-release-notes}

発売日：2021年6月10日

TiDB バージョン: 5.0.2

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   `cdc cli changefeed`コマンドの`--sort-dir`非推奨にします。代わりに、ユーザーは`cdc server`コマンドで`--sort-dir`を設定できます。 [#1795](https://github.com/pingcap/tiflow/pull/1795)

## 新機能 {#new-features}

-   TiKV

    -   デフォルトで Hibernate リージョン機能を有効にする[#10266](https://github.com/tikv/tikv/pull/10266)

## 改良点 {#improvements}

-   TiDB

    -   CPU 使用率が高くならないように、キャッシュされた統計が最新の場合は`mysql.stats_histograms`テーブルを頻繁に読み取らないようにしてください[#24317](https://github.com/pingcap/tidb/pull/24317)

-   TiKV

    -   BR は、仮想ホスト アドレッシング モード[#10243](https://github.com/tikv/tikv/pull/10243)を使用して S3 互換storageをサポートするようになりました
    -   TiCDC のスキャン速度[#10151](https://github.com/tikv/tikv/pull/10151)のバック プレッシャーをサポート
    -   TiCDC の初期スキャン[#10133](https://github.com/tikv/tikv/pull/10133)のメモリ使用量を減らす
    -   悲観的トランザクション[#10089](https://github.com/tikv/tikv/pull/10089)での TiCDC の Old Value 機能のキャッシュ ヒット率を改善する
    -   リージョンをより均等に分割して、ホットスポット書き込みがある場合にリージョンサイズの増加が分割速度を超えるという問題を軽減します[#9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   テーブル ロックを最適化して、DDL ジョブとデータ読み取りが相互にブロックされないようにする
    -   `INTEGER`型、 `REAL`型から`REAL`型へのキャスティング対応

-   ツール

    -   TiCDC

        -   テーブルメモリ消費量のモニタリング メトリックを追加します[#1885](https://github.com/pingcap/tiflow/pull/1885)
        -   並べ替えステージ[#1863](https://github.com/pingcap/tiflow/pull/1863)でメモリと CPU の使用を最適化する
        -   ユーザーの混乱を招く可能性のある不要なログ情報を削除します[#1759](https://github.com/pingcap/tiflow/pull/1759)

    -   バックアップと復元 (BR)

        -   いくつかのあいまいなエラー メッセージを明確にします[#1132](https://github.com/pingcap/br/pull/1132)
        -   バックアップのクラスタ バージョンの確認をサポート[#1091](https://github.com/pingcap/br/pull/1091)
        -   `mysql`スキーマでのシステム テーブルのバックアップと復元のサポート[#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)

    -   Dumpling

        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正[#280](https://github.com/pingcap/dumpling/pull/280)

## バグの修正 {#bug-fixes}

-   TiDB

    -   場合によっては、プレフィックス インデックスとインデックス結合を使用することによって引き起こさpanicの問題を修正します。 [#24547](https://github.com/pingcap/tidb/issues/24547) [#24716](https://github.com/pingcap/tidb/issues/24716) [#24717](https://github.com/pingcap/tidb/issues/24717)
    -   トランザクション[#24741](https://github.com/pingcap/tidb/issues/24741)の`point get`ステートメントで、 `point get`の準備済みプラン キャッシュが誤って使用される問題を修正します。
    -   照合順序が`ascii_bin`または`latin1_bin` [#24569](https://github.com/pingcap/tidb/issues/24569)の場合に間違ったプレフィックス インデックス値を書き込む問題を修正します。
    -   進行中のトランザクションが GC ワーカーによって中断される可能性がある問題を修正します[#24591](https://github.com/pingcap/tidb/issues/24591)
    -   `new-collation`が有効で`new-row-format`が無効の場合、クラスタ化インデックスでポイントクエリが間違っている可能性があるバグを修正[#24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフル ハッシュ結合[#24490](https://github.com/pingcap/tidb/pull/24490)のパーティション キーの変換をリファクタリングする
    -   `HAVING`句[#24045](https://github.com/pingcap/tidb/issues/24045)を含むクエリのプランを作成するときに発生するpanicの問題を修正します。
    -   列のプルーニングの改善により、 `Apply`と`Join`演算子の結果が正しくない問題を修正します[#23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックしたプライマリ ロックが解決できないバグを修正[#24384](https://github.com/pingcap/tidb/issues/24384)
    -   重複した fm-sketch レコードを引き起こす可能性のある統計の GC の問題を修正します[#24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観悲観的ロックが`ErrKeyExists`エラー[#23799](https://github.com/pingcap/tidb/issues/23799)を受け取ったときに、不要な悲観悲観的ロールバックを回避します。
    -   sql_mode に`ANSI_QUOTES` [#24429](https://github.com/pingcap/tidb/issues/24429)含まれている場合、数値リテラルが認識されない問題を修正します。
    -   リストされていないパーティションからデータを読み取る`INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`などのステートメントを禁止します[#24746](https://github.com/pingcap/tidb/issues/24746)
    -   SQL ステートメントに`GROUP BY`と`UNION` [#24281](https://github.com/pingcap/tidb/issues/24281)の両方が含まれている場合に発生する可能性のある`index out of range`エラーを修正します。
    -   `CONCAT`関数が照合順序[#24296](https://github.com/pingcap/tidb/issues/24296)を正しく処理しない問題を修正
    -   `collation_server`グローバル変数が新しいセッションで有効にならない問題を修正[#24156](https://github.com/pingcap/tidb/pull/24156)

-   TiKV

    -   古い値を読み取ることによって発生する TiCDC OOM の問題を修正します[#9996](https://github.com/tikv/tikv/issues/9996) [#9981](https://github.com/tikv/tikv/issues/9981)
    -   照合順序が`latin1_bin` [#24548](https://github.com/pingcap/tidb/issues/24548)の場合にクラスター化された主キー列のセカンダリ インデックスに空の値が表示される問題を修正します。
    -   panicが発生したときに TiKV がコア ダンプ ファイルを生成できるようにする`abort-on-panic`構成を追加します。コア ダンプ[#10216](https://github.com/tikv/tikv/pull/10216)を有効にするには、ユーザーが環境を正しく構成する必要があります。
    -   TiKV がビジーでないときに発生する`point get`クエリのパフォーマンス低下の問題を修正します[#10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多い場合、PDLeaderの再選が遅い問題を修正[#3697](https://github.com/tikv/pd/issues/3697)
    -   存在しないストアから evict リーダー スケジューラを削除するときに発生するpanicの問題を修正します[#3660](https://github.com/tikv/pd/issues/3660)
    -   オフライン ピアがマージされた後、統計が更新されない問題を修正します[#3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   共有デルタ インデックスを同時に複製するときの誤った結果の問題を修正します。
    -   TiFlashが不完全なデータで再起動に失敗する潜在的な問題を修正
    -   古い dm ファイルが自動的に削除されない問題を修正
    -   圧縮フィルター機能が有効になっているときに発生する可能性のあるpanicを修正します
    -   `ExchangeSender`が重複したデータを送信する潜在的な問題を修正します
    -   TiFlash が非同期コミットからフォールバックしたロックを解決できない問題を修正
    -   `TIMEZONE`型のキャスト結果に`TIMESTAMP`型が含まれている場合に誤った結果が返される問題を修正
    -   セグメント分割中に発生するTiFlashpanicの問題を修正
    -   非ルート MPP タスクの実行情報が正確でない問題を修正

-   ツール

    -   TiCDC

        -   Avro 出力[#1712](https://github.com/pingcap/tiflow/pull/1712)でタイム ゾーン情報が失われる問題を修正します。
        -   Unified Sorter の古い一時ファイルのクリーンアップをサポートし、 `sort-dir`ディレクトリの共有を禁止します[#1742](https://github.com/pingcap/tiflow/pull/1742)
        -   多くの古いリージョンが存在する場合に発生する KV クライアントのデッドロック バグを修正します[#1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[#1697](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正
        -   データを MySQL [#1750](https://github.com/pingcap/tiflow/pull/1750)に複製するときに`SUPER`特権を必要とする`explicit_defaults_for_timestamp`の更新を元に戻します
        -   シンク フロー制御をサポートして、メモリオーバーフローのリスクを軽減します[#1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブル移動時にレプリケーションタスクが停止することがある不具合を修正[#1828](https://github.com/pingcap/tiflow/pull/1828)
        -   TiCDC changefeed チェックポイント[#1759](https://github.com/pingcap/tiflow/pull/1759)の停滞により、TiKV GC セーフポイントがブロックされる問題を修正

    -   バックアップと復元 (BR)

        -   ログの復元中に`DELETE`イベントが失われる問題を修正します[#1063](https://github.com/pingcap/br/issues/1063)
        -   BRが無駄な RPC リクエストを TiKV [#1037](https://github.com/pingcap/br/pull/1037)に送信しすぎるバグを修正
        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正[#1043](https://github.com/pingcap/br/pull/1043)

    -   TiDB Lightning

        -   KVデータ生成時にTiDB Lightningpanicが発生する問題を修正[#1127](https://github.com/pingcap/br/pull/1127)
        -   自動コミットが無効になっている場合、TiDB バックエンド モードのTiDB Lightning がデータを読み込めない問題を修正します[#1104](https://github.com/pingcap/br/issues/1104)
        -   データのインポート時にキーの合計サイズが raft エントリの制限を超えたために、リージョンのバッチ分割が失敗するバグを修正します[#969](https://github.com/pingcap/br/issues/969)
