---
title: TiDB 4.0.7 Release Notes
---

# TiDB4.0.7リリースノート {#tidb-4-0-7-release-notes}

発売日：2020年9月29日

TiDBバージョン：4.0.7

## 新機能 {#new-features}

-   PD

    -   PDクライアントに`GetAllMembers`関数を追加して、PDメンバー情報を取得します[＃2980](https://github.com/pingcap/pd/pull/2980)

-   TiDBダッシュボード

    -   メトリック関係グラフの生成をサポート[＃760](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)

## 改善 {#improvements}

-   TiDB

    -   `join`オペレーター[＃20093](https://github.com/pingcap/tidb/pull/20093)のランタイム情報を追加します
    -   コプロセッサキャッシュのヒット率情報を[＃19972](https://github.com/pingcap/tidb/pull/19972)に追加し`EXPLAIN ANALYZE`
    -   `ROUND`機能を[＃19967](https://github.com/pingcap/tidb/pull/19967)にプッシュダウンすることをサポート
    -   [＃19927](https://github.com/pingcap/tidb/pull/19927)にデフォルト値の`CMSketch`を追加し`ANALYZE`
    -   エラーメッセージの感度低下を調整する[＃20004](https://github.com/pingcap/tidb/pull/20004)
    -   MySQL8.0のコネクタを使用してクライアントからの接続を受け入れる[＃19959](https://github.com/pingcap/tidb/pull/19959)

-   TiKV

    -   JSONログ形式をサポートする[＃8382](https://github.com/tikv/tikv/pull/8382)

-   PD

    -   スケジュール演算子を追加するのではなく、終了時にカウントします[＃2983](https://github.com/pingcap/pd/pull/2983)
    -   `make-up-replica`演算子を高優先度[＃2977](https://github.com/pingcap/pd/pull/2977)に設定します

-   TiFlash

    -   読み取り中に発生するRegionメタ変更のエラー処理を改善します

-   ツール

    -   TiCDC

        -   古い値機能が有効になっている場合に、MySQLシンクでより実行効率の高いSQLステートメントの変換をサポートする[＃955](https://github.com/pingcap/tiflow/pull/955)

    -   バックアップと復元（BR）

        -   バックアップ中に接続が切断された場合の接続再試行を追加[＃508](https://github.com/pingcap/br/pull/508)

    -   TiDB Lightning

        -   HTTPインターフェースを介したログレベルの動的更新のサポート[＃393](https://github.com/pingcap/tidb-lightning/pull/393)

## バグの修正 {#bug-fixes}

-   TiDB

    -   [＃20092](https://github.com/pingcap/tidb/pull/20092) `COALESCE`引き起こされる`and`からのベクトル化のバグを修正し`or`
    -   警官のタスクストアが異なるタイプの場合、プランダイジェストが同じであるという問題を修正します[＃20076](https://github.com/pingcap/tidb/pull/20076)
    -   `!= any()`関数[＃20062](https://github.com/pingcap/tidb/pull/20062)の間違った動作を修正します
    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正します[＃20051](https://github.com/pingcap/tidb/pull/20051)
    -   コンテキストがキャンセルされたときにリージョンリクエストが再試行し続ける問題を修正します[＃20031](https://github.com/pingcap/tidb/pull/20031)
    -   ストリーミングリクエストで`cluster_slow_query`テーブルの時間タイプをクエリすると、エラー[＃19943](https://github.com/pingcap/tidb/pull/19943)が発生する可能性がある問題を修正します
    -   `case when`を使用するDMLステートメントがスキーマ変更[＃20095](https://github.com/pingcap/tidb/pull/20095)を引き起こす可能性がある問題を修正します
    -   遅いログの`prev_stmt`情報が鈍感にならない問題を修正します[＃20048](https://github.com/pingcap/tidb/pull/20048)
    -   tidb-serverが異常終了したときにテーブルロックを解放しない問題を修正します[＃20020](https://github.com/pingcap/tidb/pull/20020)
    -   `ENUM`および`SET`タイプ[＃19950](https://github.com/pingcap/tidb/pull/19950)のデータを挿入するときに発生する誤ったエラーメッセージを修正します
    -   状況によっては、 `IsTrue`関数の誤った動作を修正してください[＃19903](https://github.com/pingcap/tidb/pull/19903)
    -   PDがスケールインまたはスケールアウトされた後に`CLUSTER_INFO`システムテーブルが正常に機能しない可能性がある問題を修正します[＃20026](https://github.com/pingcap/tidb/pull/20026)
    -   `control`式で定数を折りたたむときの不要な警告やエラーを回避する[＃19910](https://github.com/pingcap/tidb/pull/19910)
    -   メモリ不足（OOM） [＃20013](https://github.com/pingcap/tidb/pull/20013)を回避するために、統計を更新する方法を更新します。

-   TiKV

    -   TLSハンドシェイクが失敗したときにステータスAPIが使用できない問題を修正します[＃8649](https://github.com/tikv/tikv/pull/8649)
    -   潜在的な未定義動作を修正する[＃7782](https://github.com/tikv/tikv/pull/7782)
    -   `UnsafeDestroyRange`の実行時にスナップショットを生成することによって発生する可能性のあるpanicを修正し[＃8681](https://github.com/tikv/tikv/pull/8681)

-   PD

    -   `balance-region`が有効になっているときに一部のリージョンにリーダーがない場合にPDがpanicになる可能性があるバグを修正します[＃2994](https://github.com/pingcap/pd/pull/2994)
    -   リージョンマージ後のリージョンサイズとリージョンキーの統計的偏差を修正[＃2985](https://github.com/pingcap/pd/pull/2985)
    -   誤ったホットスポット統計を修正する[＃2991](https://github.com/pingcap/pd/pull/2991)
    -   35に`nil` [＃2974](https://github.com/pingcap/pd/pull/2974)チェックがないという問題を修正し`redirectSchedulerDelete`

-   TiFlash

    -   右外部結合の誤った結果を修正

-   ツール

    -   バックアップと復元（BR）

        -   復元プロセス後にTiDB構成が変更される原因となるバグを修正します[＃509](https://github.com/pingcap/br/pull/509)

    -   Dumpling

        -   一部の変数が`NULL`の場合、 Dumplingがメタデータの解析に失敗する問題を修正し[＃150](https://github.com/pingcap/dumpling/pull/150) 。
