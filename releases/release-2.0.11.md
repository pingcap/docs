---
title: TiDB 2.0.11 Release Notes
summary: TiDB 2.0.11およびTiDB Ansible 2.0.11は、2019年1月3日にリリースされました。このリリースでは、システムの互換性と安定性が向上しています。PDが異常状態にある場合のエラー処理、MySQLとの互換性の問題、エラーメッセージの報告、プレフィックスインデックスの範囲、およびUPDATE`ステートメントのpanic問題などが修正されています。TiKVでは、リージョンマージに関連する2つの問題も修正されています。
---

# TiDB 2.0.11 リリースノート {#tidb-2-0-11-release-notes}

2019年1月3日にTiDB 2.0.11がリリースされました。対応するTiDB Ansible 2.0.11もリリースされました。TiDB 2.0.10と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   PDが異常状態にあるときにエラーが適切に処理されない問題を修正[＃8764](https://github.com/pingcap/tidb/pull/8764)
-   TiDBのテーブルに対する`Rename`操作がMySQL [＃8809](https://github.com/pingcap/tidb/pull/8809)と互換性がない問題を修正しました。
-   `ADD INDEX`文[＃8750](https://github.com/pingcap/tidb/pull/8750)実行中に`ADMIN CHECK TABLE`操作が実行されると、エラー メッセージが誤って報告される問題を修正しました。
-   Fix the issue that the prefix index range is incorrect in some cases [#8877](https://github.com/pingcap/tidb/pull/8877)
-   列が追加された場合に発生する`UPDATE`文のpanic問題を修正[＃8904](https://github.com/pingcap/tidb/pull/8904)

## TiKV {#tikv}

-   リージョンマージ[＃4003](https://github.com/tikv/tikv/pull/4003)に関する2つの問題[＃4004](https://github.com/tikv/tikv/pull/4004)修正
