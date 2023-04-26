---
title: TiDB 2.0.8 Release Notes
---

# TiDB 2.0.8 リリースノート {#tidb-2-0-8-release-notes}

2018 年 10 月 16 日に、TiDB 2.0.8 がリリースされました。 TiDB 2.0.7 と比較すると、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   改善
    -   `Update`ステートメントが対応する AUTO-INCREMENT 列を変更しない場合、AUTO-ID の増加速度を遅くします[#7846](https://github.com/pingcap/tidb/pull/7846)
-   バグの修正
    -   PD リーダーがダウンしたときにサービスを回復するために、新しい etcd セッションをすばやく作成します[#7810](https://github.com/pingcap/tidb/pull/7810)
    -   `DateTime`型のデフォルト値を計算する際にタイムゾーンが考慮されない問題を修正[#7672](https://github.com/pingcap/tidb/pull/7672)
    -   `duplicate key update`一部の条件で値が正しく挿入されない問題を修正[#7685](https://github.com/pingcap/tidb/pull/7685)
    -   `UnionScan`の述語条件が押されない問題を修正[#7726](https://github.com/pingcap/tidb/pull/7726)
    -   `TIMESTAMP`インデックス[#7812](https://github.com/pingcap/tidb/pull/7812)を追加すると、タイム ゾーンが正しく処理されない問題を修正します。
    -   一部の条件で統計モジュールが原因で発生するメモリリークの問題を修正します[#7864](https://github.com/pingcap/tidb/pull/7864)
    -   一部の異常状態で`ANALYZE`の結果が得られない問題を修正[#7871](https://github.com/pingcap/tidb/pull/7871)
    -   返される結果が正しいことを確認するために、関数を折りたたまないでください`SYSDATE` [#7894](https://github.com/pingcap/tidb/pull/7894)
    -   一部の条件での`substring_index`panicの問題を修正[#7896](https://github.com/pingcap/tidb/pull/7896)
    -   一部条件で`OUTER JOIN`が`INNER JOIN`に変換されてしまう問題を修正[#7899](https://github.com/pingcap/tidb/pull/7899)

## TiKV {#tikv}

-   バグ修正
    -   Raftstore `EntryCache`の消費メモリがノードダウン時に増加し続ける問題を修正[#3529](https://github.com/tikv/tikv/pull/3529)
