---
title: TiDB 4.0.7 Release Notes
summary: TiDB 4.0.7は2020年9月29日にリリースされました。新機能には、PDクライアントへの「GetAllMembers」関数の追加と、TiDBダッシュボードでのメトリクス関係グラフの生成のサポートが含まれます。TiDB、TiKV、PD、 TiFlash、および各種ツールに改善が行われました。また、TiDB、TiKV、PD、 TiFlash、およびBackup & RestoreやDumplingなどのツールのバグ修正も実装されました。
---

# TiDB 4.0.7 リリースノート {#tidb-4-0-7-release-notes}

発売日：2020年9月29日

TiDB バージョン: 4.0.7

## 新機能 {#new-features}

-   PD

    -   PDクライアントにPDメンバー情報を取得する`GetAllMembers`機能を追加する[＃2980](https://github.com/pingcap/pd/pull/2980)

-   TiDBダッシュボード

    -   メトリック関係グラフの生成をサポート[＃760](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)

## 改善点 {#improvements}

-   TiDB

    -   `join`演算子[＃20093](https://github.com/pingcap/tidb/pull/20093)実行時情報を追加します
    -   `EXPLAIN ANALYZE` [＃19972](https://github.com/pingcap/tidb/pull/19972)にコプロセッサキャッシュのヒット率情報を追加
    -   `ROUND`機能をTiFlash [＃19967](https://github.com/pingcap/tidb/pull/19967)にプッシュダウンするサポート
    -   `ANALYZE` [＃19927](https://github.com/pingcap/tidb/pull/19927)にデフォルト値`CMSketch`を追加します
    -   エラーメッセージの感度調整[＃20004](https://github.com/pingcap/tidb/pull/20004)
    -   MySQL 8.0 [＃19959](https://github.com/pingcap/tidb/pull/19959)のコネクタを使用してクライアントからの接続を受け入れる

-   TiKV

    -   JSONログ形式[＃8382](https://github.com/tikv/tikv/pull/8382)サポート

-   PD

    -   スケジュールオペレータを、追加ではなく終了時にカウントします[＃2983](https://github.com/pingcap/pd/pull/2983)
    -   `make-up-replica`オペレータを高優先度[＃2977](https://github.com/pingcap/pd/pull/2977)に設定する

-   TiFlash

    -   読み取り中に発生するリージョンメタ変更のエラー処理を改善しました

-   ツール

    -   TiCDC

        -   古い値機能が有効になっている場合に、MySQL シンクでより実行効率の高い SQL 文を変換する機能をサポート[＃955](https://github.com/pingcap/tiflow/pull/955)

    -   バックアップと復元 (BR)

        -   バックアップ[＃508](https://github.com/pingcap/br/pull/508)中に接続が切断された場合に接続再試行を追加

    -   TiDB Lightning

        -   HTTPインターフェース[＃393](https://github.com/pingcap/tidb-lightning/pull/393)を介してログレベルを動的に更新する機能をサポート

## バグ修正 {#bug-fixes}

-   TiDB

    -   ショートカット`COALESCE` [＃20092](https://github.com/pingcap/tidb/pull/20092) `and`化バグ`or`修正
    -   copタスクストアが異なるタイプであってもプランダイジェストが同じになる問題を修正[＃20076](https://github.com/pingcap/tidb/pull/20076)
    -   `!= any()`関数[＃20062](https://github.com/pingcap/tidb/pull/20062)の誤った動作を修正
    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正[＃20051](https://github.com/pingcap/tidb/pull/20051)
    -   コンテキストがキャンセルされたときにリージョン要求が再試行され続ける問題を修正[＃20031](https://github.com/pingcap/tidb/pull/20031)
    -   ストリーミングリクエストで`cluster_slow_query`のテーブルの時間型をクエリするとエラーが発生する可能性がある問題を修正しました[＃19943](https://github.com/pingcap/tidb/pull/19943)
    -   `case when`使用する DML ステートメントがスキーマ変更[＃20095](https://github.com/pingcap/tidb/pull/20095)引き起こす可能性がある問題を修正しました
    -   スローログの`prev_stmt`情報が感度低下しない問題を修正[＃20048](https://github.com/pingcap/tidb/pull/20048)
    -   tidb-server が異常終了した際にテーブルロックを解除しない問題を修正[＃20020](https://github.com/pingcap/tidb/pull/20020)
    -   `ENUM`と`SET`タイプ[＃19950](https://github.com/pingcap/tidb/pull/19950)のデータを挿入するときに発生する誤ったエラーメッセージを修正しました
    -   いくつかの状況における`IsTrue`関数の誤った動作を修正[＃19903](https://github.com/pingcap/tidb/pull/19903)
    -   PDのスケールインまたはスケールアウト後に`CLUSTER_INFO`システムテーブルが正常に動作しない可能性がある問題を修正しました[＃20026](https://github.com/pingcap/tidb/pull/20026)
    -   `control`式[＃19910](https://github.com/pingcap/tidb/pull/19910)で定数を折り畳むときに不要な警告やエラーを回避する
    -   メモリ不足（OOM）を回避するために統計情報の更新方法を更新します[＃20013](https://github.com/pingcap/tidb/pull/20013)

-   TiKV

    -   TLSハンドシェイクが失敗したときにステータスAPIが利用できない問題を修正[＃8649](https://github.com/tikv/tikv/pull/8649)
    -   潜在的な未定義の動作を修正する[＃7782](https://github.com/tikv/tikv/pull/7782)
    -   `UnsafeDestroyRange` [＃8681](https://github.com/tikv/tikv/pull/8681)実行時にスナップショットを生成することで発生する可能性のあるpanicを修正

-   PD

    -   `balance-region`有効になっているときに、一部のリージョンにLeaderがいない場合、PD がpanic可能性があるバグを修正しました[＃2994](https://github.com/pingcap/pd/pull/2994)
    -   リージョンマージ[＃2985](https://github.com/pingcap/pd/pull/2985)後のリージョンサイズとリージョンキーの統計的偏差を修正
    -   ホットスポット統計の誤りを修正[＃2991](https://github.com/pingcap/pd/pull/2991)
    -   `redirectSchedulerDelete` [＃2974](https://github.com/pingcap/pd/pull/2974)に`nil`チェックインがない問題を修正

-   TiFlash

    -   右外部結合の誤った結果を修正

-   ツール

    -   バックアップと復元 (BR)

        -   復元プロセス後にTiDB構成が変更されるバグを修正[＃509](https://github.com/pingcap/br/pull/509)

    -   Dumpling

        -   一部の変数が`NULL` [＃150](https://github.com/pingcap/dumpling/pull/150)場合にDumplingがメタデータを解析できない問題を修正しました
