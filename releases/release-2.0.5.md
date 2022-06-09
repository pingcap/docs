---
title: TiDB 2.0.5 Release Notes
---

# TiDB2.0.5リリースノート {#tidb-2-0-5-release-notes}

2018年7月6日、TiDB2.0.5がリリースされました。 TiDB 2.0.4と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   新機能
    -   トランザクションの自動再試行を無効にするために使用される`tidb_disable_txn_auto_retry`のシステム変数を追加します[＃6877](https://github.com/pingcap/tidb/pull/6877)
-   改善
    -   `Selection`のコスト計算を最適化して、結果をより正確にします[＃6989](https://github.com/pingcap/tidb/pull/6989)
    -   一意のインデックスまたは主キーと完全に一致するクエリ条件をクエリパスとして直接選択します[＃6966](https://github.com/pingcap/tidb/pull/6966)
    -   サービスの開始に失敗した場合は、必要なクリーンアップを実行してください[＃6964](https://github.com/pingcap/tidb/pull/6964)
    -   `Load Data`ステートメント[＃6962](https://github.com/pingcap/tidb/pull/6962)で`\N`をNULLとして処理します。
    -   CBO1の[＃6953](https://github.com/pingcap/tidb/pull/6953)構造を最適化する
    -   サービスを開始するときに、監視メトリックを早期に報告する[＃6931](https://github.com/pingcap/tidb/pull/6931)
    -   SQLステートメントの改行を削除し、ユーザー情報を追加して、低速クエリの形式を最適化します[＃6920](https://github.com/pingcap/tidb/pull/6920)
    -   コメント[＃6858](https://github.com/pingcap/tidb/pull/6858)で複数のアスタリスクをサポートする
-   バグの修正
    -   `KILL QUERY`には常にSUPER特権[＃7003](https://github.com/pingcap/tidb/pull/7003)が必要であるという問題を修正します
    -   ユーザー数が1024を超えるとユーザーがログインに失敗する可能性がある問題を修正します[＃6986](https://github.com/pingcap/tidb/pull/6986)
    -   署名されて[＃6940](https://github.com/pingcap/tidb/pull/6940)ない`float`データの挿入に関する問題を修正する`double`
    -   `COM_FIELD_LIST`コマンドの互換性を修正して、一部のMariaDBクライアントのパニックの問題を解決します[＃6929](https://github.com/pingcap/tidb/pull/6929)
    -   `CREATE TABLE IF NOT EXISTS LIKE`の動作を修正[＃6928](https://github.com/pingcap/tidb/pull/6928)
    -   TopNプッシュダウン[＃6923](https://github.com/pingcap/tidb/pull/6923)のプロセスの問題を修正します
    -   `Add Index` [＃6903](https://github.com/pingcap/tidb/pull/6903)の実行中にエラーが発生した場合に、現在処理中の行のIDレコードの問題を修正します。

## PD {#pd}

-   一部のシナリオで、レプリカの移行によってTiKVディスクスペースが消費される問題を修正します
-   `AdjacentRegionScheduler`によって引き起こされるクラッシュの問題を修正します

## TiKV {#tikv}

-   10進演算で発生する可能性のあるオーバーフローの問題を修正
-   マージの過程で発生する可能性のあるダーティリードの問題を修正します
