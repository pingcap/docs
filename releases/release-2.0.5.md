---
title: TiDB 2.0.5 Release Notes
summary: TiDB 2.0.5は2018年7月6日にリリースされ、システムの互換性と安定性が向上しました。新機能には、tidb_disable_txn_auto_retry`システム変数が含まれます。バグ修正では、ユーザーログイン、データ挿入、コマンド互換性に関する問題が修正されました。PDとTiKVについても、様々な問題が修正されました。
---

# TiDB 2.0.5 リリースノート {#tidb-2-0-5-release-notes}

2018年7月6日にTiDB 2.0.5がリリースされました。このリリースでは、TiDB 2.0.4と比較して、システムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   新機能
    -   トランザクション自動再試行を無効にするために使用される`tidb_disable_txn_auto_retry`システム変数を追加します [＃6877](https://github.com/pingcap/tidb/pull/6877)
-   改善点
    -   `Selection`のコスト計算を最適化して、結果をより正確にする[＃6989](https://github.com/pingcap/tidb/pull/6989)
    -   クエリパスとして、一意インデックスまたは主キーに完全に一致するクエリ条件を直接選択します。 [＃6966](https://github.com/pingcap/tidb/pull/6966)
    -   サービス起動に失敗した場合に必要なクリーンアップを実行する [＃6964](https://github.com/pingcap/tidb/pull/6964)
    -   `Load Data`文で`\N` を NULL として処理する [＃6962](https://github.com/pingcap/tidb/pull/6962)
    -   CBO のコード構造を最適化する [＃6953](https://github.com/pingcap/tidb/pull/6953)
    -   サービスを開始するときに監視メトリックを早めに報告する [＃6931](https://github.com/pingcap/tidb/pull/6931)
    -   SQL文の改行を削除し、ユーザー情報を追加することで、スロークエリの形式を最適化します[＃6920](https://github.com/pingcap/tidb/pull/6920)
    -   コメントで複数のアスタリスクをサポート [＃6858](https://github.com/pingcap/tidb/pull/6858)
-   バグ修正
    -   `KILL QUERY`常に SUPER 権限必要となる問題を修正 [＃7003](https://github.com/pingcap/tidb/pull/7003)
    -   ユーザー数が1024を超えるとログインに失敗する可能性がある問題を修正しました[＃6986](https://github.com/pingcap/tidb/pull/6986)
    -   符号なし`float`データ`double`挿入に関する問題を修正[＃6940](https://github.com/pingcap/tidb/pull/6940)
    -   一部のMariaDBクライアントのpanic問題を解決するために`COM_FIELD_LIST`コマンドの互換性を修正しました [＃6929](https://github.com/pingcap/tidb/pull/6929)
    -   `CREATE TABLE IF NOT EXISTS LIKE`の動作を修正する [＃6928](https://github.com/pingcap/tidb/pull/6928)
    -   TopNプッシュダウンのプロセスにおける問題を修正 [＃6923](https://github.com/pingcap/tidb/pull/6923)
    -   `Add Index` の実行中にエラーが発生した場合に、現在処理中の行の ID レコードの問題を修正しました。 [＃6903](https://github.com/pingcap/tidb/pull/6903)

## PD {#pd}

-   一部のシナリオでレプリカの移行によって TiKV ディスク領域が消費される問題を修正しました
-   `AdjacentRegionScheduler`によって引き起こされたクラッシュの問題を修正

## TiKV {#tikv}

-   小数点演算における潜在的なオーバーフローの問題を修正
-   マージのプロセスで発生する可能性のあるダーティリードの問題を修正しました
