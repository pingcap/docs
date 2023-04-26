---
title: TiDB 2.0.11 Release Notes
---

# TiDB 2.0.11 リリースノート {#tidb-2-0-11-release-notes}

2019 年 1 月 3 日に、TiDB 2.0.11 がリリースされました。対応する TiDB Ansible 2.0.11 もリリースされています。 TiDB 2.0.10 と比較すると、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   PDが異常状態の場合、エラーが適切に処理されない問題を修正[#8764](https://github.com/pingcap/tidb/pull/8764)
-   TiDB のテーブルに対する`Rename`操作が MySQL [#8809](https://github.com/pingcap/tidb/pull/8809)の操作と互換性がないという問題を修正します。
-   `ADD INDEX`文[#8750](https://github.com/pingcap/tidb/pull/8750)の実行中に`ADMIN CHECK TABLE`操作を行うと、エラーメッセージが誤って報告される問題を修正
-   場合によってはプレフィックス インデックスの範囲が正しくない問題を修正します[#8877](https://github.com/pingcap/tidb/pull/8877)
-   場合によっては列が追加されたときの`UPDATE`ステートメントのpanicの問題を修正します[#8904](https://github.com/pingcap/tidb/pull/8904)

## TiKV {#tikv}

-   リージョンのマージに関する 2 つの問題を修正[#4003](https://github.com/tikv/tikv/pull/4003) 、 [#4004](https://github.com/tikv/tikv/pull/4004)
