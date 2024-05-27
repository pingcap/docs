---
title: TiDB 2.0.8 Release Notes
summary: TiDB 2.0.8 は、システムの互換性と安定性の向上を伴い、2018 年 10 月 16 日にリリースされました。このリリースには、TiDB と TiKV のさまざまなバグ修正が含まれており、AUTO-ID、etcd セッション回復、タイム ゾーン処理、メモリリーク、結合変換に関連する問題に対処しています。TiKV のバグ修正により、ノードがダウンしたときにRaftstore EntryCache によって増加するメモリ消費が解決されます。
---

# TiDB 2.0.8 リリースノート {#tidb-2-0-8-release-notes}

2018 年 10 月 16 日に、TiDB 2.0.8 がリリースされました。TiDB 2.0.7 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## ティビ {#tidb}

-   改善
    -   `Update`文が対応する AUTO-INCREMENT 列[＃7846](https://github.com/pingcap/tidb/pull/7846)を変更しない場合は、AUTO-ID の増加速度を遅くします。
-   バグの修正
    -   PDリーダーがダウンしたときにサービスを回復するための新しいetcdセッションを素早く作成する[＃7810](https://github.com/pingcap/tidb/pull/7810)
    -   `DateTime`型のデフォルト値を計算する際にタイムゾーンが考慮されない問題を修正[＃7672](https://github.com/pingcap/tidb/pull/7672)
    -   `duplicate key update`一部の条件で値が誤って挿入される問題を修正[＃7685](https://github.com/pingcap/tidb/pull/7685)
    -   `UnionScan`の述語条件が[＃7726](https://github.com/pingcap/tidb/pull/7726)にプッシュダウンされない問題を修正
    -   `TIMESTAMP`インデックス[＃7812](https://github.com/pingcap/tidb/pull/7812)を追加したときにタイムゾーンが正しく処理されない問題を修正
    -   特定の状況で統計モジュールによって発生するメモリリークの問題を修正[＃7864](https://github.com/pingcap/tidb/pull/7864)
    -   [＃7871](https://github.com/pingcap/tidb/pull/7871)一部の異常な状況で`ANALYZE`の結果が得られない問題を修正
    -   関数`SYSDATE`折り返さないで、返される結果が正しいことを確認します[＃7894](https://github.com/pingcap/tidb/pull/7894)
    -   特定の状況で発生するpanic問題`substring_index`を修正[＃7896](https://github.com/pingcap/tidb/pull/7896)
    -   いくつかの条件で`OUTER JOIN`が誤って`INNER JOIN`に変換される問題を修正しました[＃7899](https://github.com/pingcap/tidb/pull/7899)

## ティクヴ {#tikv}

-   バグ修正
    -   ノードがダウンするとRaftstore `EntryCache`のメモリ消費量が増加し続ける問題を修正[＃3529](https://github.com/tikv/tikv/pull/3529)
