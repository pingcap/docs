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

    -   デフォルトで休止状態リージョン機能を有効にする[#10266](https://github.com/tikv/tikv/pull/10266)

## 改善点 {#improvements}

-   TiDB

    -   `mysql.stats_histograms`キャッシュされた統計が最新の場合は、CPU 使用率が高くなるのを避けるためにテーブルを頻繁に読み取らないようにします[#24317](https://github.com/pingcap/tidb/pull/24317)

-   TiKV

    -   BR は、仮想ホスト アドレッシング モード[#10243](https://github.com/tikv/tikv/pull/10243)を使用した S3 互換storageをサポートするようになりました。
    -   TiCDC のスキャン速度[#10151](https://github.com/tikv/tikv/pull/10151)のバック プレッシャーをサポート
    -   TiCDC の初期スキャン[#10133](https://github.com/tikv/tikv/pull/10133)のメモリ使用量を削減します。
    -   悲観的トランザクション[#10089](https://github.com/tikv/tikv/pull/10089)における TiCDC の古い値機能のキャッシュ ヒット率を改善します。
    -   ホットスポット書き込みがある場合にリージョンサイズの増加が分割速度を超える問題を軽減するために、リージョンをより均等に分割します[#9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   テーブル ロックを最適化して、DDL ジョブとデータ読み取りが相互にブロックしないようにします。
    -   `INTEGER`または`REAL`タイプから`REAL`タイプへのキャストをサポート

-   ツール

    -   TiCDC

        -   テーブルのメモリ消費量の監視メトリクスを追加[#1885](https://github.com/pingcap/tiflow/pull/1885)
        -   ソート段階[#1863](https://github.com/pingcap/tiflow/pull/1863)でのメモリと CPU の使用量を最適化します。
        -   ユーザーの混乱を引き起こす可能性のある不要なログ情報を削除します[#1759](https://github.com/pingcap/tiflow/pull/1759)

    -   バックアップと復元 (BR)

        -   いくつかのあいまいなエラー メッセージを明確にする[#1132](https://github.com/pingcap/br/pull/1132)
        -   バックアップのクラスター バージョンの確認のサポート[#1091](https://github.com/pingcap/br/pull/1091)
        -   `mysql`スキーマ[#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)でのシステム テーブルのバックアップと復元のサポート

    -   Dumpling

        -   バックアップ失敗時にエラーが出力されない問題を修正[#280](https://github.com/pingcap/dumpling/pull/280)

## バグの修正 {#bug-fixes}

-   TiDB

    -   場合によってはプレフィックスインデックスとインデックスジョインの使用によって引き起こされるpanicの問題を修正[#24547](https://github.com/pingcap/tidb/issues/24547) [#24716](https://github.com/pingcap/tidb/issues/24716) [#24717](https://github.com/pingcap/tidb/issues/24717)
    -   準備されたプラン キャッシュ`point get`がトランザクション[#24741](https://github.com/pingcap/tidb/issues/24741)の`point get`ステートメントによって誤って使用される問題を修正します。
    -   照合順序が`ascii_bin`または`latin1_bin` [#24569](https://github.com/pingcap/tidb/issues/24569)場合に、間違ったプレフィックス インデックス値が書き込まれる問題を修正します。
    -   進行中のトランザクションが GC ワーカーによって中断される可能性がある問題を修正します[#24591](https://github.com/pingcap/tidb/issues/24591)
    -   `new-collation`が有効で`new-row-format`が無効な場合、クラスター化インデックスでポイント クエリが誤る可能性があるバグを修正[#24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフル ハッシュ結合[#24490](https://github.com/pingcap/tidb/pull/24490)パーティション キーの変換をリファクタリングします。
    -   `HAVING`節[#24045](https://github.com/pingcap/tidb/issues/24045)を含むクエリのプランを構築するときに発生するpanicの問題を修正します。
    -   列枝刈りの改善により`Apply`と`Join`演算子の結果がおかしくなる問題を修正[#23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックしたプライマリロックが解決できないバグを修正[#24384](https://github.com/pingcap/tidb/issues/24384)
    -   fm-sketch レコードの重複を引き起こす可能性がある統計の GC 問題を修正[#24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観的的ロックが`ErrKeyExists`エラー[#23799](https://github.com/pingcap/tidb/issues/23799)を受け取った場合、不必要な悲観的的ロールバックを回避します。
    -   sql_mode に`ANSI_QUOTES` [#24429](https://github.com/pingcap/tidb/issues/24429)が含まれる場合、数値リテラルが認識されない問題を修正
    -   `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`のようなステートメントによる、リストされていないパーティションからのデータの読み取りを禁止します[#24746](https://github.com/pingcap/tidb/issues/24746)
    -   SQL ステートメントに`GROUP BY`と`UNION`両方が含まれる場合に発生する可能性のある`index out of range`エラーを修正[#24281](https://github.com/pingcap/tidb/issues/24281)
    -   `CONCAT`関数が照合照合順序[#24296](https://github.com/pingcap/tidb/issues/24296)を正しく処理しない問題を修正します。
    -   `collation_server`グローバル変数が新しいセッション[#24156](https://github.com/pingcap/tidb/pull/24156)で有効にならない問題を修正します。

-   TiKV

    -   古い値の読み取りによって発生する TiCDC OOM 問題を修正[#9996](https://github.com/tikv/tikv/issues/9996) [#9981](https://github.com/tikv/tikv/issues/9981)
    -   照合順序が`latin1_bin` [#24548](https://github.com/pingcap/tidb/issues/24548)の場合に、クラスター化された主キー列のセカンダリ インデックスに空の値が表示される問題を修正します。
    -   `abort-on-panic`構成を追加します。これにより、panic発生時に TiKV がコア ダンプ ファイルを生成できるようになります。ユーザーは、コア ダンプ[#10216](https://github.com/tikv/tikv/pull/10216)を有効にするために環境を正しく構成する必要があります。
    -   TiKV がビジーでないときに発生する`point get`クエリのパフォーマンス低下の問題を修正します[#10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多い場合、PDLeaderの再選出が遅い問題を修正[#3697](https://github.com/tikv/pd/issues/3697)
    -   存在しないストア[#3660](https://github.com/tikv/pd/issues/3660)からエビクト リーダー スケジューラを削除するときに発生するpanicの問題を修正します。
    -   オフラインピアのマージ後に統計が更新されない問題を修正[#3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   共有デルタインデックスを同時にクローン作成するときに誤った結果が発生する問題を修正
    -   TiFlash が不完全なデータで再起動できないという潜在的な問題を修正
    -   古いDMファイルが自動的に削除されない問題を修正
    -   圧縮フィルター機能が有効になっているときに発生する可能性のあるpanicを修正しました。
    -   `ExchangeSender`重複したデータを送信するという潜在的な問題を修正
    -   TiFlash が非同期コミットからフォールバックしたロックを解決できない問題を修正
    -   `TIMEZONE`型のキャスト結果に`TIMESTAMP`型が含まれる場合に誤った結果が返される問題を修正
    -   セグメント分割中に発生するTiFlashpanic問題を修正
    -   非ルート MPP タスクの実行情報が正確ではない問題を修正

-   ツール

    -   TiCDC

        -   Avro 出力[#1712](https://github.com/pingcap/tiflow/pull/1712)でタイムゾーン情報が失われる問題を修正
        -   統合ソーターでの古い一時ファイルのクリーンアップをサポートし、ディレクトリ`sort-dir`の共有を禁止します[#1742](https://github.com/pingcap/tiflow/pull/1742)
        -   古いリージョンが多数存在する場合に発生する KV クライアントのデッドロック バグを修正[#1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[#1697](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正
        -   データを MySQL [#1750](https://github.com/pingcap/tiflow/pull/1750)にレプリケートするときに`SUPER`権限が必要な`explicit_defaults_for_timestamp`の更新を元に戻します。
        -   シンク フロー制御をサポートしてメモリオーバーフローのリスクを軽減します[#1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブル[#1828](https://github.com/pingcap/tiflow/pull/1828)の移動時にレプリケーションタスクが停止する場合があるバグを修正
        -   TiCDC チェンジフィード チェックポイント[#1759](https://github.com/pingcap/tiflow/pull/1759)の停滞により TiKV GC セーフ ポイントがブロックされる問題を修正

    -   バックアップと復元 (BR)

        -   ログの復元中に`DELETE`イベントが失われる問題を修正[#1063](https://github.com/pingcap/br/issues/1063)
        -   BR がTiKV [#1037](https://github.com/pingcap/br/pull/1037)に無駄な RPC リクエストを送信しすぎる原因となるバグを修正
        -   バックアップ失敗時にエラーが出力されない問題を修正[#1043](https://github.com/pingcap/br/pull/1043)

    -   TiDB Lightning

        -   KV データ[#1127](https://github.com/pingcap/br/pull/1127)の生成時に発生するTiDB Lightningpanicの問題を修正
        -   自動コミットが無効になっている場合、TiDB バックエンド モードのTiDB Lightning がデータをロードできない問題を修正します[#1104](https://github.com/pingcap/br/issues/1104)
        -   データインポート時に合計キーサイズがraftエントリ制限を超えたためバッチ分割リージョンが失敗するバグを修正[#969](https://github.com/pingcap/br/issues/969)
