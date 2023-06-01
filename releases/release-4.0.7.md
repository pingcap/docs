---
title: TiDB 4.0.7 Release Notes
---

# TiDB 4.0.7 リリースノート {#tidb-4-0-7-release-notes}

発売日：2020年9月29日

TiDB バージョン: 4.0.7

## 新機能 {#new-features}

-   PD

    -   PD メンバー情報を取得する`GetAllMembers`関数を PD クライアントに追加します[<a href="https://github.com/pingcap/pd/pull/2980">#2980</a>](https://github.com/pingcap/pd/pull/2980)

-   TiDB ダッシュボード

    -   メトリクス関係グラフ[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/760">#760</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)の生成をサポート

## 改善点 {#improvements}

-   TiDB

    -   `join`オペレーター[<a href="https://github.com/pingcap/tidb/pull/20093">#20093</a>](https://github.com/pingcap/tidb/pull/20093)のランタイム情報を追加します。
    -   `EXPLAIN ANALYZE` [<a href="https://github.com/pingcap/tidb/pull/19972">#19972</a>](https://github.com/pingcap/tidb/pull/19972)にコプロセッサキャッシュのヒット率情報を追加
    -   `ROUND`機能をTiFlash [<a href="https://github.com/pingcap/tidb/pull/19967">#19967</a>](https://github.com/pingcap/tidb/pull/19967)にプッシュダウンするサポート
    -   `ANALYZE` [<a href="https://github.com/pingcap/tidb/pull/19927">#19927</a>](https://github.com/pingcap/tidb/pull/19927)にデフォルト値の`CMSketch`を追加します。
    -   エラーメッセージの感度を下げる[<a href="https://github.com/pingcap/tidb/pull/20004">#20004</a>](https://github.com/pingcap/tidb/pull/20004)を調整する
    -   MySQL 8.0 のコネクタを使用してクライアントからの接続を受け入れる[<a href="https://github.com/pingcap/tidb/pull/19959">#19959</a>](https://github.com/pingcap/tidb/pull/19959)

-   TiKV

    -   JSONログ形式[<a href="https://github.com/tikv/tikv/pull/8382">#8382</a>](https://github.com/tikv/tikv/pull/8382)のサポート

-   PD

    -   スケジュール演算子を追加するのではなく、終了時にカウントする[<a href="https://github.com/pingcap/pd/pull/2983">#2983</a>](https://github.com/pingcap/pd/pull/2983)
    -   `make-up-replica`オペレータを高優先度[<a href="https://github.com/pingcap/pd/pull/2977">#2977</a>](https://github.com/pingcap/pd/pull/2977)に設定します

-   TiFlash

    -   読み取り中に発生するリージョンメタ変更のエラー処理を改善します。

-   ツール

    -   TiCDC

        -   古い値機能が有効になっている場合、MySQL シンクでより実行効率の高い SQL ステートメントの変換をサポートします[<a href="https://github.com/pingcap/tiflow/pull/955">#955</a>](https://github.com/pingcap/tiflow/pull/955)

    -   バックアップと復元 (BR)

        -   バックアップ中に接続が切断された場合の接続の再試行を追加[<a href="https://github.com/pingcap/br/pull/508">#508</a>](https://github.com/pingcap/br/pull/508)

    -   TiDB Lightning

        -   HTTP インターフェイスを介したログ レベルの動的更新のサポート[<a href="https://github.com/pingcap/tidb-lightning/pull/393">#393</a>](https://github.com/pingcap/tidb-lightning/pull/393)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ショートカット[<a href="https://github.com/pingcap/tidb/pull/20092">#20092</a>](https://github.com/pingcap/tidb/pull/20092)によって引き起こされる`and` / `or` / `COALESCE`のベクトル化バグを修正
    -   cop タスク ストアのタイプが異なる場合にプラン ダイジェストが同じになる問題を修正します[<a href="https://github.com/pingcap/tidb/pull/20076">#20076</a>](https://github.com/pingcap/tidb/pull/20076)
    -   `!= any()`関数[<a href="https://github.com/pingcap/tidb/pull/20062">#20062</a>](https://github.com/pingcap/tidb/pull/20062)の誤った動作を修正します。
    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正[<a href="https://github.com/pingcap/tidb/pull/20051">#20051</a>](https://github.com/pingcap/tidb/pull/20051)
    -   コンテキストがキャンセルされたときにリージョンリクエストが再試行し続ける問題を修正します[<a href="https://github.com/pingcap/tidb/pull/20031">#20031</a>](https://github.com/pingcap/tidb/pull/20031)
    -   ストリーミングリクエストでテーブル`cluster_slow_query`の時刻型をクエリするとエラー[<a href="https://github.com/pingcap/tidb/pull/19943">#19943</a>](https://github.com/pingcap/tidb/pull/19943)が発生することがある問題を修正
    -   `case when`を使用する DML ステートメントによってスキーマ変更が発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/20095">#20095</a>](https://github.com/pingcap/tidb/pull/20095)
    -   スローログの`prev_stmt`情報が感度解除されない問題を修正[<a href="https://github.com/pingcap/tidb/pull/20048">#20048</a>](https://github.com/pingcap/tidb/pull/20048)
    -   tidb-server が異常終了したときにテーブル ロックを解放しない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/20020">#20020</a>](https://github.com/pingcap/tidb/pull/20020)
    -   `ENUM`および`SET`タイプ[<a href="https://github.com/pingcap/tidb/pull/19950">#19950</a>](https://github.com/pingcap/tidb/pull/19950)のデータを挿入するときに発生する誤ったエラー メッセージを修正しました。
    -   状況によっては`IsTrue`関数の誤った動作を修正します[<a href="https://github.com/pingcap/tidb/pull/19903">#19903</a>](https://github.com/pingcap/tidb/pull/19903)
    -   PD をスケールインまたはスケールアウトした後、 `CLUSTER_INFO`システム テーブルが正常に動作しなくなることがある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/20026">#20026</a>](https://github.com/pingcap/tidb/pull/20026)
    -   定数を式`control`に折りたたむときに不要な警告やエラーが発生するのを回避します[<a href="https://github.com/pingcap/tidb/pull/19910">#19910</a>](https://github.com/pingcap/tidb/pull/19910)
    -   メモリ不足 (OOM) [<a href="https://github.com/pingcap/tidb/pull/20013">#20013</a>](https://github.com/pingcap/tidb/pull/20013)を回避するために統計の更新方法を更新します。

-   TiKV

    -   TLS ハンドシェイクが失敗した場合にステータス API が利用できない問題を修正[<a href="https://github.com/tikv/tikv/pull/8649">#8649</a>](https://github.com/tikv/tikv/pull/8649)
    -   潜在的な未定義の動作を修正します[<a href="https://github.com/tikv/tikv/pull/7782">#7782</a>](https://github.com/tikv/tikv/pull/7782)
    -   `UnsafeDestroyRange` [<a href="https://github.com/tikv/tikv/pull/8681">#8681</a>](https://github.com/tikv/tikv/pull/8681)の実行時にスナップショットを生成することによって発生する可能性のあるpanicを修正しました。

-   PD

    -   `balance-region`を有効にした場合、一部のリージョンにLeaderがいない場合に PD がパニックになる可能性があるバグを修正[<a href="https://github.com/pingcap/pd/pull/2994">#2994</a>](https://github.com/pingcap/pd/pull/2994)
    -   リージョンマージ[<a href="https://github.com/pingcap/pd/pull/2985">#2985</a>](https://github.com/pingcap/pd/pull/2985)後のリージョンサイズとリージョンキーの統計的偏差を修正
    -   間違ったホットスポット統計を修正します[<a href="https://github.com/pingcap/pd/pull/2991">#2991</a>](https://github.com/pingcap/pd/pull/2991)
    -   `redirectSchedulerDelete` [<a href="https://github.com/pingcap/pd/pull/2974">#2974</a>](https://github.com/pingcap/pd/pull/2974)で`nil`チェックが無い問題を修正

-   TiFlash

    -   右外部結合の間違った結果を修正

-   ツール

    -   バックアップと復元 (BR)

        -   復元プロセス[<a href="https://github.com/pingcap/br/pull/509">#509</a>](https://github.com/pingcap/br/pull/509)後に TiDB 構成が変更されるバグを修正しました。

    -   Dumpling

        -   一部の変数が`NULL` [<a href="https://github.com/pingcap/dumpling/pull/150">#150</a>](https://github.com/pingcap/dumpling/pull/150)の場合、 Dumpling がメタデータの解析に失敗する問題を修正
