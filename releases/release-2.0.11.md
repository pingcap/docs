---
title: TiDB 2.0.11 Release Notes
---

# TiDB2.0.11リリースノート {#tidb-2-0-11-release-notes}

2019年1月3日、TiDB2.0.11がリリースされました。対応するTiDBAnsible2.0.11もリリースされています。 TiDB 2.0.10と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   PDが異常な状態のときにエラーが適切に処理されない問題を修正します[＃8764](https://github.com/pingcap/tidb/pull/8764)
-   TiDBのテーブルに対する`Rename`の操作がMySQL3の操作と互換性がないという問題を修正し[＃8809](https://github.com/pingcap/tidb/pull/8809)
-   `ADD INDEX`ステートメント[＃8750](https://github.com/pingcap/tidb/pull/8750)の実行プロセスで`ADMIN CHECK TABLE`操作を実行すると、エラーメッセージが誤って報告される問題を修正します。
-   プレフィックスインデックス範囲が正しくない場合がある問題を修正します[＃8877](https://github.com/pingcap/tidb/pull/8877)
-   場合によっては列が追加されたときの`UPDATE`ステートメントのpanicの問題を修正します[＃8904](https://github.com/pingcap/tidb/pull/8904)

## TiKV {#tikv}

-   リージョンマージ[＃4003](https://github.com/tikv/tikv/pull/4003)に関する2つの問題を修正し[＃4004](https://github.com/tikv/tikv/pull/4004)
