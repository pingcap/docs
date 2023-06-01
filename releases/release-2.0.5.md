---
title: TiDB 2.0.5 Release Notes
---

# TiDB 2.0.5 リリースノート {#tidb-2-0-5-release-notes}

2018 年 7 月 6 日に、TiDB 2.0.5 がリリースされました。 TiDB 2.0.4 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   新機能
    -   トランザクションの自動再試行を無効にするために使用される`tidb_disable_txn_auto_retry`システム変数を追加します[<a href="https://github.com/pingcap/tidb/pull/6877">#6877</a>](https://github.com/pingcap/tidb/pull/6877)
-   改善点
    -   `Selection`のコスト計算を最適化して結果をより正確にします[<a href="https://github.com/pingcap/tidb/pull/6989">#6989</a>](https://github.com/pingcap/tidb/pull/6989)
    -   一意のインデックスまたは主キーに完全に一致するクエリ条件をクエリ パスとして直接選択します[<a href="https://github.com/pingcap/tidb/pull/6966">#6966</a>](https://github.com/pingcap/tidb/pull/6966)
    -   サービスの起動に失敗した場合に必要なクリーンアップを実行[<a href="https://github.com/pingcap/tidb/pull/6964">#6964</a>](https://github.com/pingcap/tidb/pull/6964)
    -   `Load Data`ステートメント[<a href="https://github.com/pingcap/tidb/pull/6962">#6962</a>](https://github.com/pingcap/tidb/pull/6962)で`\N` NULL として処理します。
    -   CBO [<a href="https://github.com/pingcap/tidb/pull/6953">#6953</a>](https://github.com/pingcap/tidb/pull/6953)のコード構造を最適化
    -   サービスの開始時に監視メトリクスを早期にレポートする[<a href="https://github.com/pingcap/tidb/pull/6931">#6931</a>](https://github.com/pingcap/tidb/pull/6931)
    -   SQL ステートメントの改行を削除し、ユーザー情報[<a href="https://github.com/pingcap/tidb/pull/6920">#6920</a>](https://github.com/pingcap/tidb/pull/6920)を追加することで、遅いクエリの形式を最適化します。
    -   コメントでの複数のアスタリスクのサポート[<a href="https://github.com/pingcap/tidb/pull/6858">#6858</a>](https://github.com/pingcap/tidb/pull/6858)
-   バグの修正
    -   `KILL QUERY`は常に SUPER 権限[<a href="https://github.com/pingcap/tidb/pull/7003">#7003</a>](https://github.com/pingcap/tidb/pull/7003)が必要になる問題を修正
    -   ユーザー数が1024 [<a href="https://github.com/pingcap/tidb/pull/6986">#6986</a>](https://github.com/pingcap/tidb/pull/6986)超えるとログインに失敗する場合がある問題を修正1
    -   符号なし`float` / `double`データの挿入に関する問題を修正[<a href="https://github.com/pingcap/tidb/pull/6940">#6940</a>](https://github.com/pingcap/tidb/pull/6940)
    -   一部の MariaDB クライアントでのpanicの問題を解決するために`COM_FIELD_LIST`コマンドの互換性を修正しました[<a href="https://github.com/pingcap/tidb/pull/6929">#6929</a>](https://github.com/pingcap/tidb/pull/6929)
    -   `CREATE TABLE IF NOT EXISTS LIKE`動作を修正する[<a href="https://github.com/pingcap/tidb/pull/6928">#6928</a>](https://github.com/pingcap/tidb/pull/6928)
    -   TopN プッシュダウン[<a href="https://github.com/pingcap/tidb/pull/6923">#6923</a>](https://github.com/pingcap/tidb/pull/6923)のプロセスの問題を修正
    -   `Add Index` [<a href="https://github.com/pingcap/tidb/pull/6903">#6903</a>](https://github.com/pingcap/tidb/pull/6903)の実行中にエラーが発生した場合の、現在処理中の行の ID レコードの問題を修正しました。

## PD {#pd}

-   一部のシナリオでレプリカの移行が TiKV ディスク領域を消費する問題を修正
-   `AdjacentRegionScheduler`によって引き起こされるクラッシュの問題を修正

## TiKV {#tikv}

-   10 進数演算における潜在的なオーバーフローの問題を修正
-   マージのプロセスで発生する可能性のあるダーティ リードの問題を修正します。
