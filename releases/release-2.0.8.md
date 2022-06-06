---
title: TiDB 2.0.8 Release Notes
---

# TiDB2.0.8リリースノート {#tidb-2-0-8-release-notes}

2018年10月16日、TiDB2.0.8がリリースされました。 TiDB 2.0.7と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   改善
    -   `Update`ステートメントが対応するAUTO-INCREMENT列[＃7846](https://github.com/pingcap/tidb/pull/7846)を変更しない場合は、AUTO-IDの増加速度を遅くします。
-   バグの修正
    -   PDリーダーがダウンしたときにサービスを回復するための新しいetcdセッションをすばやく作成します[＃7810](https://github.com/pingcap/tidb/pull/7810)
    -   `DateTime`タイプのデフォルト値が計算されるときにタイムゾーンが考慮されない問題を修正します[＃7672](https://github.com/pingcap/tidb/pull/7672)
    -   `duplicate key update`特定の条件で値が正しく挿入されない問題を修正します[＃7685](https://github.com/pingcap/tidb/pull/7685)
    -   `UnionScan`の述語条件がプッシュダウンされない問題を修正します[＃7726](https://github.com/pingcap/tidb/pull/7726)
    -   `TIMESTAMP`インデックス[＃7812](https://github.com/pingcap/tidb/pull/7812)を追加すると、タイムゾーンが正しく処理されない問題を修正します。
    -   一部の条件で統計モジュールによって引き起こされるメモリリークの問題を修正します[＃7864](https://github.com/pingcap/tidb/pull/7864)
    -   一部の異常状態で`ANALYZE`の結果が得られない問題を修正[＃7871](https://github.com/pingcap/tidb/pull/7871)
    -   返された結果が正しいことを確認するために、関数`SYSDATE`を折りたたまないでください[＃7894](https://github.com/pingcap/tidb/pull/7894)
    -   いくつかの条件で`substring_index`パニックの問題を修正します[＃7896](https://github.com/pingcap/tidb/pull/7896)
    -   一部の条件で`OUTER JOIN`が誤って`INNER JOIN`に変換される問題を修正します[＃7899](https://github.com/pingcap/tidb/pull/7899)

## TiKV {#tikv}

-   バグ修正
    -   ノードがダウンしたときに`EntryCache`によって消費されるメモリが増加し続ける問題を修正します[＃3529](https://github.com/tikv/tikv/pull/3529)
