---
title: TiDB 4.0.7 Release Notes
---

# TiDB 4.0.7 リリースノート {#tidb-4-0-7-release-notes}

発売日：2020年9月29日

TiDB バージョン: 4.0.7

## 新機能 {#new-features}

-   PD

    -   PD メンバー情報を取得する`GetAllMembers`関数を PD クライアントに追加します[#2980](https://github.com/pingcap/pd/pull/2980)

-   TiDB ダッシュボード

    -   メトリクス関係グラフ[#760](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)の生成をサポート

## 改善点 {#improvements}

-   TiDB

    -   `join`オペレーター[#20093](https://github.com/pingcap/tidb/pull/20093)のランタイム情報を追加します。
    -   `EXPLAIN ANALYZE` [#19972](https://github.com/pingcap/tidb/pull/19972)にコプロセッサキャッシュのヒット率情報を追加
    -   `ROUND`機能をTiFlash [#19967](https://github.com/pingcap/tidb/pull/19967)にプッシュダウンするサポート
    -   `ANALYZE` [#19927](https://github.com/pingcap/tidb/pull/19927)にデフォルト値の`CMSketch`を追加します。
    -   エラーメッセージの感度を下げる[#20004](https://github.com/pingcap/tidb/pull/20004)を調整する
    -   MySQL 8.0 のコネクタを使用してクライアントからの接続を受け入れる[#19959](https://github.com/pingcap/tidb/pull/19959)

-   TiKV

    -   JSONログ形式[#8382](https://github.com/tikv/tikv/pull/8382)のサポート

-   PD

    -   スケジュール演算子を追加するのではなく、終了時にカウントする[#2983](https://github.com/pingcap/pd/pull/2983)
    -   `make-up-replica`オペレータを高優先度[#2977](https://github.com/pingcap/pd/pull/2977)に設定します

-   TiFlash

    -   読み取り中に発生するリージョンメタ変更のエラー処理を改善します。

-   ツール

    -   TiCDC

        -   古い値機能が有効になっている場合、MySQL シンクでより実行効率の高い SQL ステートメントの変換をサポートします[#955](https://github.com/pingcap/tiflow/pull/955)

    -   バックアップと復元 (BR)

        -   バックアップ中に接続が切断された場合の接続の再試行を追加[#508](https://github.com/pingcap/br/pull/508)

    -   TiDB Lightning

        -   HTTP インターフェイスを介したログ レベルの動的更新のサポート[#393](https://github.com/pingcap/tidb-lightning/pull/393)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ショートカット[#20092](https://github.com/pingcap/tidb/pull/20092)によって引き起こされる`and` / `or` / `COALESCE`のベクトル化バグを修正
    -   cop タスク ストアのタイプが異なる場合にプラン ダイジェストが同じになる問題を修正します[#20076](https://github.com/pingcap/tidb/pull/20076)
    -   `!= any()`関数[#20062](https://github.com/pingcap/tidb/pull/20062)の誤った動作を修正します。
    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正[#20051](https://github.com/pingcap/tidb/pull/20051)
    -   コンテキストがキャンセルされたときにリージョンリクエストが再試行し続ける問題を修正します[#20031](https://github.com/pingcap/tidb/pull/20031)
    -   ストリーミングリクエストでテーブル`cluster_slow_query`の時刻型をクエリするとエラー[#19943](https://github.com/pingcap/tidb/pull/19943)が発生することがある問題を修正
    -   `case when`を使用する DML ステートメントによってスキーマ変更が発生する可能性がある問題を修正します[#20095](https://github.com/pingcap/tidb/pull/20095)
    -   スローログの`prev_stmt`情報が感度解除されない問題を修正[#20048](https://github.com/pingcap/tidb/pull/20048)
    -   tidb-server が異常終了したときにテーブル ロックを解放しない問題を修正します[#20020](https://github.com/pingcap/tidb/pull/20020)
    -   `ENUM`および`SET`タイプ[#19950](https://github.com/pingcap/tidb/pull/19950)のデータを挿入するときに発生する誤ったエラー メッセージを修正しました。
    -   状況によっては`IsTrue`関数の誤った動作を修正します[#19903](https://github.com/pingcap/tidb/pull/19903)
    -   PD をスケールインまたはスケールアウトした後、 `CLUSTER_INFO`システム テーブルが正常に動作しなくなることがある問題を修正します[#20026](https://github.com/pingcap/tidb/pull/20026)
    -   定数を式`control`に折りたたむときに不要な警告やエラーが発生するのを回避します[#19910](https://github.com/pingcap/tidb/pull/19910)
    -   メモリ不足 (OOM) [#20013](https://github.com/pingcap/tidb/pull/20013)を回避するために統計の更新方法を更新します。

-   TiKV

    -   TLS ハンドシェイクが失敗した場合にステータス API が利用できない問題を修正[#8649](https://github.com/tikv/tikv/pull/8649)
    -   潜在的な未定義の動作を修正します[#7782](https://github.com/tikv/tikv/pull/7782)
    -   `UnsafeDestroyRange` [#8681](https://github.com/tikv/tikv/pull/8681)の実行時にスナップショットを生成することによって発生する可能性のあるpanicを修正しました。

-   PD

    -   `balance-region`を有効にした場合、一部のリージョンにLeaderがいない場合に PD がパニックになる可能性があるバグを修正[#2994](https://github.com/pingcap/pd/pull/2994)
    -   リージョンマージ[#2985](https://github.com/pingcap/pd/pull/2985)後のリージョンサイズとリージョンキーの統計的偏差を修正
    -   間違ったホットスポット統計を修正します[#2991](https://github.com/pingcap/pd/pull/2991)
    -   `redirectSchedulerDelete` [#2974](https://github.com/pingcap/pd/pull/2974)で`nil`チェックが無い問題を修正

-   TiFlash

    -   右外部結合の間違った結果を修正

-   ツール

    -   バックアップと復元 (BR)

        -   復元プロセス[#509](https://github.com/pingcap/br/pull/509)後に TiDB 構成が変更されるバグを修正しました。

    -   Dumpling

        -   一部の変数が`NULL` [#150](https://github.com/pingcap/dumpling/pull/150)の場合、 Dumpling がメタデータの解析に失敗する問題を修正
