---
title: TiDB 4.0.7 Release Notes
---

# TiDB 4.0.7 リリースノート {#tidb-4-0-7-release-notes}

発売日：2020年9月29日

TiDB バージョン: 4.0.7

## 新機能 {#new-features}

-   PD

    -   PD クライアントに`GetAllMembers`関数を追加して、PD メンバー情報を取得します[#2980](https://github.com/pingcap/pd/pull/2980)

-   TiDB ダッシュボード

    -   メトリクス関係グラフの生成をサポート[#760](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)

## 改良点 {#improvements}

-   TiDB

    -   `join`オペレーター[#20093](https://github.com/pingcap/tidb/pull/20093)のランタイム情報を追加します。
    -   コプロセッサキャッシュのヒット率情報を`EXPLAIN ANALYZE` [#19972](https://github.com/pingcap/tidb/pull/19972)に追加
    -   `ROUND`機能のTiFlash [#19967](https://github.com/pingcap/tidb/pull/19967)へのプッシュダウンをサポート
    -   `ANALYZE` [#19927](https://github.com/pingcap/tidb/pull/19927)のデフォルト値`CMSketch`を追加します
    -   エラーメッセージの減感作を絞り込む[#20004](https://github.com/pingcap/tidb/pull/20004)
    -   MySQL 8.0 [#19959](https://github.com/pingcap/tidb/pull/19959)のコネクタを使用してクライアントからの接続を受け入れる

-   TiKV

    -   JSON ログ形式[#8382](https://github.com/tikv/tikv/pull/8382)をサポート

-   PD

    -   追加ではなく終了時にスケジュール オペレーターをカウントする[#2983](https://github.com/pingcap/pd/pull/2983)
    -   `make-up-replica`オペレータを高優先度[#2977](https://github.com/pingcap/pd/pull/2977)に設定

-   TiFlash

    -   読み取り中に発生するリージョンメタ変更のエラー処理を改善する

-   ツール

    -   TiCDC

        -   古い値機能が有効になっている場合、MySQL シンクでより実行効率の高い SQL ステートメントの変換をサポートします[#955](https://github.com/pingcap/tiflow/pull/955)

    -   バックアップと復元 (BR)

        -   バックアップ中に接続が切断された場合の接続リトライを追加[#508](https://github.com/pingcap/br/pull/508)

    -   TiDB Lightning

        -   HTTP インターフェイスを介したログ レベルの動的更新のサポート[#393](https://github.com/pingcap/tidb-lightning/pull/393)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ショートカット[#20092](https://github.com/pingcap/tidb/pull/20092)による`and` / `or` / `COALESCE`からのベクトル化のバグを修正
    -   警官タスク ストアのタイプが異なる場合に、プラン ダイジェストが同じになる問題を修正します[#20076](https://github.com/pingcap/tidb/pull/20076)
    -   `!= any()`関数の間違った動作を修正[#20062](https://github.com/pingcap/tidb/pull/20062)
    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正[#20051](https://github.com/pingcap/tidb/pull/20051)
    -   コンテキストがキャンセルされたときにリージョンリクエストが再試行し続ける問題を修正します[#20031](https://github.com/pingcap/tidb/pull/20031)
    -   ストリーミング リクエストで`cluster_slow_query`テーブルの時間型をクエリすると、エラー[#19943](https://github.com/pingcap/tidb/pull/19943)が発生する可能性がある問題を修正します。
    -   `case when`を使用する DML ステートメントがスキーマの変更を引き起こす可能性がある問題を修正します[#20095](https://github.com/pingcap/tidb/pull/20095)
    -   `prev_stmt`スローログの情報が鈍感にならない問題を修正[#20048](https://github.com/pingcap/tidb/pull/20048)
    -   tidb-server が異常終了時にテーブルロックを解除しない問題を修正[#20020](https://github.com/pingcap/tidb/pull/20020)
    -   `ENUM`および`SET`タイプ[#19950](https://github.com/pingcap/tidb/pull/19950)のデータを挿入するときに発生する誤ったエラー メッセージを修正します。
    -   状況によっては`IsTrue`関数の間違った動作を修正します[#19903](https://github.com/pingcap/tidb/pull/19903)
    -   PD のスケールインまたはスケールアウト後に`CLUSTER_INFO`システム テーブルが正常に動作しない場合がある問題を修正します[#20026](https://github.com/pingcap/tidb/pull/20026)
    -   `control`式で定数を折り畳む際の不要な警告やエラーを回避する[#19910](https://github.com/pingcap/tidb/pull/19910)
    -   Out of Memory (OOM) を回避するために、統計の更新方法を更新します[#20013](https://github.com/pingcap/tidb/pull/20013)

-   TiKV

    -   TLS ハンドシェイクが失敗したときに Status API を使用できない問題を修正します[#8649](https://github.com/tikv/tikv/pull/8649)
    -   潜在的な未定義の動作を修正します[#7782](https://github.com/tikv/tikv/pull/7782)
    -   `UnsafeDestroyRange` [#8681](https://github.com/tikv/tikv/pull/8681)の実行時にスナップショットの生成によって引き起こされる可能性があるpanicを修正します。

-   PD

    -   `balance-region`が有効な場合、一部のリージョンにLeaderがない場合、PD がpanicになる可能性があるバグを修正します[#2994](https://github.com/pingcap/pd/pull/2994)
    -   リージョンマージ後のリージョンサイズとリージョンキーの統計偏差を修正[#2985](https://github.com/pingcap/pd/pull/2985)
    -   誤ったホットスポット統計を修正する[#2991](https://github.com/pingcap/pd/pull/2991)
    -   `redirectSchedulerDelete` [#2974](https://github.com/pingcap/pd/pull/2974)で`nil`チェックがない問題を修正

-   TiFlash

    -   右外部結合の間違った結果を修正

-   ツール

    -   バックアップと復元 (BR)

        -   復元プロセス[#509](https://github.com/pingcap/br/pull/509)の後に TiDB 構成が変更される原因となるバグを修正します。

    -   Dumpling

        -   一部の変数が`NULL` [#150](https://github.com/pingcap/dumpling/pull/150)の場合にDumpling がメタデータの解析に失敗する問題を修正します
