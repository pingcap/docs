---
title: TiDB 2.0.5 Release Notes
---

# TiDB 2.0.5 リリースノート {#tidb-2-0-5-release-notes}

2018 年 7 月 6 日に、TiDB 2.0.5 がリリースされました。 TiDB 2.0.4 と比較すると、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   新機能
    -   トランザクションの自動再試行を無効にするために使用される`tidb_disable_txn_auto_retry`システム変数を追加します[#6877](https://github.com/pingcap/tidb/pull/6877)
-   改良点
    -   `Selection`のコスト計算を最適化して結果をより正確にする[#6989](https://github.com/pingcap/tidb/pull/6989)
    -   ユニークインデックスまたは主キーに完全一致するクエリ条件を直接クエリパスとして選択[#6966](https://github.com/pingcap/tidb/pull/6966)
    -   サービスの起動に失敗した場合に必要なクリーンアップを実行する[#6964](https://github.com/pingcap/tidb/pull/6964)
    -   `Load Data`ステートメント[#6962](https://github.com/pingcap/tidb/pull/6962)で`\N` NULL として処理する
    -   CBO [#6953](https://github.com/pingcap/tidb/pull/6953)のコード構造を最適化する
    -   サービス[#6931](https://github.com/pingcap/tidb/pull/6931)の開始時にモニタリング メトリックを早期に報告する
    -   SQL ステートメントの改行を削除し、ユーザー情報を追加して、スロー クエリの形式を最適化する[#6920](https://github.com/pingcap/tidb/pull/6920)
    -   コメントでの複数のアスタリスクのサポート[#6858](https://github.com/pingcap/tidb/pull/6858)
-   バグの修正
    -   `KILL QUERY`が常に SUPER 権限を必要とする問題を修正[#7003](https://github.com/pingcap/tidb/pull/7003)
    -   ユーザー数が 1024 を超えると、ユーザーがログインに失敗することがある問題を修正します[#6986](https://github.com/pingcap/tidb/pull/6986)
    -   符号なし`float` / `double`データの挿入に関する問題を修正[#6940](https://github.com/pingcap/tidb/pull/6940)
    -   `COM_FIELD_LIST`コマンドの互換性を修正して、一部の MariaDB クライアントでのpanicの問題を解決します[#6929](https://github.com/pingcap/tidb/pull/6929)
    -   `CREATE TABLE IF NOT EXISTS LIKE`動作を修正する[#6928](https://github.com/pingcap/tidb/pull/6928)
    -   TopN プッシュダウン[#6923](https://github.com/pingcap/tidb/pull/6923)のプロセスの問題を修正
    -   `Add Index` [#6903](https://github.com/pingcap/tidb/pull/6903)の実行でエラーが発生した場合、現在処理中の行の ID レコードの問題を修正します。

## PD {#pd}

-   一部のシナリオで、レプリカの移行が TiKV ディスク領域を使い果たす問題を修正します
-   `AdjacentRegionScheduler`によって引き起こされたクラッシュの問題を修正

## TiKV {#tikv}

-   10 進演算で発生する可能性があるオーバーフローの問題を修正
-   マージの過程で発生する可能性のあるダーティ リードの問題を修正します。
