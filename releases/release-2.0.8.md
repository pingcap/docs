---
title: TiDB 2.0.8 Release Notes
---

# TiDB 2.0.8 リリースノート {#tidb-2-0-8-release-notes}

2018 年 10 月 16 日に、TiDB 2.0.8 がリリースされました。 TiDB 2.0.7 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   改善
    -   `Update`ステートメントが対応する AUTO-INCREMENT カラム[#7846](https://github.com/pingcap/tidb/pull/7846)を変更しない場合、AUTO-ID の増加速度を遅くします。
-   バグの修正
    -   PD リーダーがダウンしたときにサービスを回復するために、新しい etcd セッションをすばやく作成します[#7810](https://github.com/pingcap/tidb/pull/7810)
    -   `DateTime`タイプのデフォルト値を計算する際にタイムゾーンが考慮されない問題を修正[#7672](https://github.com/pingcap/tidb/pull/7672)
    -   `duplicate key update`一部の条件で値が正しく挿入されない問題を修正[#7685](https://github.com/pingcap/tidb/pull/7685)
    -   `UnionScan`の述語条件がプッシュダウンされない問題を修正[#7726](https://github.com/pingcap/tidb/pull/7726)
    -   `TIMESTAMP`インデックス[#7812](https://github.com/pingcap/tidb/pull/7812)を追加するとタイムゾーンが正しく処理されない問題を修正
    -   一部の状況で統計モジュールによって引き起こされるメモリリークの問題を修正[#7864](https://github.com/pingcap/tidb/pull/7864)
    -   一部の異常状態[#7871](https://github.com/pingcap/tidb/pull/7871)において`ANALYZE`の結果が得られない問題を修正
    -   返される結果が正しいことを確認するため、関数`SYSDATE`折り畳まないでください[#7894](https://github.com/pingcap/tidb/pull/7894)
    -   一部の状況での`substring_index`panicの問題を修正[#7896](https://github.com/pingcap/tidb/pull/7896)
    -   一部の条件で`OUTER JOIN`が誤って`INNER JOIN`に変換されてしまう問題を修正[#7899](https://github.com/pingcap/tidb/pull/7899)

## TiKV {#tikv}

-   バグ修正
    -   ノードがダウンするとRaftstore `EntryCache`が消費するメモリが増加し続ける問題を修正[#3529](https://github.com/tikv/tikv/pull/3529)
