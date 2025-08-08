---
title: TiDB 5.0.2 Release Notes
summary: TiDB 5.0.2は2021年6月10日にリリースされました。この新バージョンには、互換性の変更、新機能、改善、バグ修正、そしてTiKV、 TiFlash、PD、TiCDC、Backup & Restore（BR）、 TiDB Lightningなどの各種ツールのアップデートが含まれています。注目すべき変更点としては、TiCDCにおける--sort-dir`の廃止、TiKVにおけるHibernate リージョン機能の有効化、TiDB、TiKV、PD、 TiFlash、そしてTiCDC、 BR、 TiDB Lightningなどのツールにおける各種バグ修正などが挙げられます。
---

# TiDB 5.0.2 リリースノート {#tidb-5-0-2-release-notes}

発売日：2021年6月10日

TiDB バージョン: 5.0.2

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   `cdc cli changefeed`コマンドの`--sort-dir`非推奨です。代わりに、 `cdc server`コマンドの`--sort-dir`設定できます[＃1795](https://github.com/pingcap/tiflow/pull/1795)

## 新機能 {#new-features}

-   TiKV

    -   Hibernate リージョン機能をデフォルトで有効にする[＃10266](https://github.com/tikv/tikv/pull/10266)

## 改善点 {#improvements}

-   TiDB

    -   キャッシュされた統計が最新の場合は、CPU使用率の上昇を避けるために、 `mysql.stats_histograms`テーブルを頻繁に読み取らないようにします[＃24317](https://github.com/pingcap/tidb/pull/24317)

-   TiKV

    -   BRは、仮想ホストアドレス指定モード[＃10243](https://github.com/tikv/tikv/pull/10243)を使用してS3互換storageをサポートするようになりました。
    -   TiCDCのスキャン速度[＃10151](https://github.com/tikv/tikv/pull/10151)バックプレッシャーをサポート
    -   TiCDCの初期スキャン[＃10133](https://github.com/tikv/tikv/pull/10133)のメモリ使用量を削減
    -   悲観的トランザクション[＃10089](https://github.com/tikv/tikv/pull/10089)におけるTiCDCの古い値機能のキャッシュヒット率を改善
    -   ホットスポット書き込みがあるときに、リージョンサイズの増加が分割速度を超える問題を軽減するために、リージョンをより均等に分割します[＃9785](https://github.com/tikv/tikv/issues/9785)

-   TiFlash

    -   テーブルロックを最適化して、DDLジョブとデータ読み取りが互いにブロックされないようにする
    -   `INTEGER`または`REAL`型から`REAL`型へのキャストをサポート

-   ツール

    -   TiCDC

        -   テーブルメモリ消費量の監視メトリックを追加する[＃1885](https://github.com/pingcap/tiflow/pull/1885)
        -   ソート段階[＃1863](https://github.com/pingcap/tiflow/pull/1863)におけるメモリとCPUの使用を最適化する
        -   ユーザーの混乱を招く可能性のある不要なログ情報を削除する[＃1759](https://github.com/pingcap/tiflow/pull/1759)

    -   バックアップと復元 (BR)

        -   曖昧なエラーメッセージを明確にする[＃1132](https://github.com/pingcap/br/pull/1132)
        -   バックアップ[＃1091](https://github.com/pingcap/br/pull/1091)のクラスタ バージョンの確認をサポート
        -   `mysql`スキーマ[＃1143](https://github.com/pingcap/br/pull/1143) [＃1078](https://github.com/pingcap/br/pull/1078)のシステムテーブルのバックアップと復元をサポート

    -   Dumpling

        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正[＃280](https://github.com/pingcap/dumpling/pull/280)

## バグ修正 {#bug-fixes}

-   TiDB

    -   一部のケースでプレフィックスインデックスとインデックス結合を使用することで発生するpanic問題を修正[＃24547](https://github.com/pingcap/tidb/issues/24547) [＃24716](https://github.com/pingcap/tidb/issues/24716) [＃24717](https://github.com/pingcap/tidb/issues/24717)
    -   `point get`の準備されたプランキャッシュがトランザクション[＃24741](https://github.com/pingcap/tidb/issues/24741)の`point get`文によって誤って使用される問題を修正しました。
    -   照合順序が`ascii_bin`または`latin1_bin`場合に間違ったプレフィックスインデックス値を書き込む問題を修正しました[＃24569](https://github.com/pingcap/tidb/issues/24569)
    -   GCワーカー[＃24591](https://github.com/pingcap/tidb/issues/24591)によって進行中のトランザクションが中断される可能性がある問題を修正
    -   `new-collation`が有効で`new-row-format`無効の場合、クラスター化インデックスでポイントクエリが間違って実行される可能性があるバグを修正しました[＃24541](https://github.com/pingcap/tidb/issues/24541)
    -   シャッフルハッシュ結合[＃24490](https://github.com/pingcap/tidb/pull/24490)パーティションキーの変換をリファクタリングする
    -   `HAVING`句[＃24045](https://github.com/pingcap/tidb/issues/24045)を含むクエリのプランを構築するときに発生するpanic問題を修正しました。
    -   列プルーニングの改善により、演算子`Apply`と`Join`結果が間違ってしまう問題を修正しました[＃23887](https://github.com/pingcap/tidb/issues/23887)
    -   非同期コミットからフォールバックしたプライマリロックが解決できないバグを修正[＃24384](https://github.com/pingcap/tidb/issues/24384)
    -   fm-sketch レコードの重複を引き起こす可能性のある統計の GC 問題を修正しました[＃24357](https://github.com/pingcap/tidb/pull/24357)
    -   悲観的ロックが`ErrKeyExists`エラー[＃23799](https://github.com/pingcap/tidb/issues/23799)を受け取ったときに不要な悲観的ロールバックを回避する
    -   sql_modeに`ANSI_QUOTES` [＃24429](https://github.com/pingcap/tidb/issues/24429)が含まれている場合に数値リテラルが認識されない問題を修正しました
    -   `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE`ような文は、リストされていないパーティション[＃24746](https://github.com/pingcap/tidb/issues/24746)からデータを読み取ることを禁止します。
    -   SQL文に`GROUP BY`と`UNION`両方が含まれている場合に発生する可能性のある`index out of range`エラーを修正します[＃24281](https://github.com/pingcap/tidb/issues/24281)
    -   `CONCAT`関数が照合順序[＃24296](https://github.com/pingcap/tidb/issues/24296)誤って処理する問題を修正しました
    -   `collation_server`グローバル変数が新しいセッション[＃24156](https://github.com/pingcap/tidb/pull/24156)で有効にならない問題を修正しました

-   TiKV

    -   古い値の読み取りによって引き起こされる TiCDC OOM 問題を修正[＃9996](https://github.com/tikv/tikv/issues/9996) [＃9981](https://github.com/tikv/tikv/issues/9981)
    -   照合順序が`latin1_bin` [＃24548](https://github.com/pingcap/tidb/issues/24548)場合にクラスター化主キー列のセカンダリインデックスに空の値が含まれる問題を修正しました
    -   `abort-on-panic`設定を追加すると、panic発生時にTiKVがコアダンプファイルを生成できるようになります。コアダンプ[＃10216](https://github.com/tikv/tikv/pull/10216)を有効にするには、ユーザーは環境を正しく設定する必要があります。
    -   TiKVがビジーでないときに発生する`point get`クエリのパフォーマンス回帰の問題を修正しました[＃10046](https://github.com/tikv/tikv/issues/10046)

-   PD

    -   店舗数が多い場合にPDLeaderの再選出が遅くなる問題を修正[＃3697](https://github.com/tikv/pd/issues/3697)
    -   存在しないストア[＃3660](https://github.com/tikv/pd/issues/3660)からエビクト リーダー スケジューラを削除するときに発生するpanic問題を修正しました
    -   オフラインピアがマージされた後に統計が更新されない問題を修正[＃3611](https://github.com/tikv/pd/issues/3611)

-   TiFlash

    -   共有デルタインデックスを同時にクローン化する際に誤った結果が生成される問題を修正しました
    -   TiFlashが不完全なデータで再起動に失敗する潜在的な問題を修正
    -   古いdmファイルが自動的に削除されない問題を修正
    -   圧縮フィルタ機能が有効になっているときに発生する可能性のあるpanicを修正しました
    -   `ExchangeSender`重複したデータを送信する潜在的な問題を修正
    -   TiFlash が非同期コミットからフォールバックしたロックを解決できない問題を修正しました
    -   `TIMEZONE`型のキャスト結果に`TIMESTAMP`型が含まれている場合に誤った結果が返される問題を修正しました
    -   セグメント分割中に発生するTiFlashpanic問題を修正
    -   非ルート MPP タスクの実行情報が正確ではない問題を修正しました

-   ツール

    -   TiCDC

        -   Avro出力[＃1712](https://github.com/pingcap/tiflow/pull/1712)でタイムゾーン情報が失われる問題を修正
        -   Unified Sorter 内の古い一時ファイルのクリーンアップをサポートし、 `sort-dir`ディレクトリ[＃1742](https://github.com/pingcap/tiflow/pull/1742)共有を禁止します。
        -   多くの古いリージョンが存在する場合に発生する KV クライアントのデッドロックバグを修正[＃1599](https://github.com/pingcap/tiflow/issues/1599)
        -   `--cert-allowed-cn`フラグ[＃1697](https://github.com/pingcap/tiflow/pull/1697)の間違ったヘルプ情報を修正
        -   MySQL [＃1750](https://github.com/pingcap/tiflow/pull/1750)にデータを複製する際に`SUPER`権限を必要とする`explicit_defaults_for_timestamp`の更新を元に戻す
        -   シンクフロー制御をサポートし、メモリオーバーフローのリスクを軽減します[＃1840](https://github.com/pingcap/tiflow/pull/1840)
        -   テーブル[＃1828](https://github.com/pingcap/tiflow/pull/1828)移動する際にレプリケーションタスクが停止する可能性があるバグを修正
        -   TiCDC チェンジフィード チェックポイント[＃1759](https://github.com/pingcap/tiflow/pull/1759)の停滞により TiKV GC セーフ ポイントがブロックされる問題を修正しました

    -   バックアップと復元 (BR)

        -   ログの復元中に`DELETE`イベントが失われる問題を修正しました[＃1063](https://github.com/pingcap/br/issues/1063)
        -   BR がTiKV [＃1037](https://github.com/pingcap/br/pull/1037)に無駄な RPC リクエストを大量に送信してしまうバグを修正しました
        -   バックアップ操作が失敗したときにエラーが出力されない問題を修正[＃1043](https://github.com/pingcap/br/pull/1043)

    -   TiDB Lightning

        -   KVデータ生成時に発生するTiDB Lightning panicの問題を修正[＃1127](https://github.com/pingcap/br/pull/1127)
        -   自動コミットが無効になっていると、TiDB バックエンド モードのTiDB Lightningでデータをロードできない問題を修正しました[＃1104](https://github.com/pingcap/br/issues/1104)
        -   データインポート中にキーの合計サイズがラフトエントリ制限を超えたためにバッチ分割リージョンが失敗するバグを修正[＃969](https://github.com/pingcap/br/issues/969)
