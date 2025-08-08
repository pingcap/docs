---
title: TiDB 2.0.8 Release Notes
summary: TiDB 2.0.8は2018年10月16日にリリースされ、システムの互換性と安定性が向上しました。このリリースには、TiDBとTiKVの様々なバグ修正が含まれており、AUTO-ID、etcdセッションリカバリ、タイムゾーン処理、メモリリーク、結合変換に関する問題が修正されています。TiKVのバグ修正により、ノードダウン時にRaftstore EntryCacheによるメモリ消費が増加する問題が解決されています。
---

# TiDB 2.0.8 リリースノート {#tidb-2-0-8-release-notes}

2018年10月16日にTiDB 2.0.8がリリースされました。TiDB 2.0.7と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   改善
    -   `Update`文が対応するAUTO-INCREMENT列[＃7846](https://github.com/pingcap/tidb/pull/7846)を変更しない場合は、AUTO-IDの増加速度を遅くします。
-   バグ修正
    -   PDリーダーがダウンしたときにサービスを回復するための新しいetcdセッションを素早く作成する[＃7810](https://github.com/pingcap/tidb/pull/7810)
    -   `DateTime`型のデフォルト値を計算する際にタイムゾーンが考慮されない問題を修正[＃7672](https://github.com/pingcap/tidb/pull/7672)
    -   `duplicate key update`一部の条件で値が誤って挿入される問題を修正[＃7685](https://github.com/pingcap/tidb/pull/7685)
    -   `UnionScan`の述語条件がプッシュダウンされない問題を修正[＃7726](https://github.com/pingcap/tidb/pull/7726)
    -   `TIMESTAMP`インデックス[＃7812](https://github.com/pingcap/tidb/pull/7812)を追加したときにタイムゾーンが正しく処理されない問題を修正しました
    -   一部の状況で統計モジュールによって発生するメモリリークの問題を修正[＃7864](https://github.com/pingcap/tidb/pull/7864)
    -   [＃7871](https://github.com/pingcap/tidb/pull/7871)一部の異常な状況で`ANALYZE`の結果が取得できない問題を修正
    -   関数`SYSDATE`折り畳まないでください。返される結果が正しいことを確認するためです[＃7894](https://github.com/pingcap/tidb/pull/7894)
    -   いくつかの状況でpanic`substring_index`問題を修正[＃7896](https://github.com/pingcap/tidb/pull/7896)
    -   一部の状況で`OUTER JOIN`が誤って`INNER JOIN`に変換される問題を修正[＃7899](https://github.com/pingcap/tidb/pull/7899)

## TiKV {#tikv}

-   バグ修正
    -   ノードがダウンするとRaftstore `EntryCache`のメモリ消費量が増加し続ける問題を修正[＃3529](https://github.com/tikv/tikv/pull/3529)
