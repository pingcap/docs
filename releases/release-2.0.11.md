---
title: TiDB 2.0.11 Release Notes
---

# TiDB 2.0.11 リリースノート {#tidb-2-0-11-release-notes}

2019 年 1 月 3 日に、TiDB 2.0.11 がリリースされました。対応する TiDB Ansible 2.0.11 もリリースされています。 TiDB 2.0.10 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   PD異常[#8764](https://github.com/pingcap/tidb/pull/8764)時にエラー処理が正しく行われない問題を修正
-   TiDB のテーブルに対する`Rename`オペレーションが MySQL [#8809](https://github.com/pingcap/tidb/pull/8809)のオペレーションと互換性がないという問題を修正
-   `ADD INDEX`ステートメント[#8750](https://github.com/pingcap/tidb/pull/8750)の実行中に`ADMIN CHECK TABLE`操作を実行すると、エラー メッセージが誤って報告される問題を修正
-   プレフィックスインデックスの範囲が正しくない場合がある問題を修正[#8877](https://github.com/pingcap/tidb/pull/8877)
-   列が追加される場合に発生する`UPDATE`ステートメントのpanicの問題を修正[#8904](https://github.com/pingcap/tidb/pull/8904)

## TiKV {#tikv}

-   リージョンのマージ[#4003](https://github.com/tikv/tikv/pull/4003) 、 [#4004](https://github.com/tikv/tikv/pull/4004)に関する 2 つの問題を修正
