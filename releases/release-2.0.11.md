---
title: TiDB 2.0.11 Release Notes
summary: TiDB 2.0.11 および TiDB Ansible 2.0.11 は、2019 年 1 月 3 日にリリースされました。このリリースには、システムの互換性と安定性の向上が含まれています。修正には、PD が異常な状態にある場合のエラー処理、MySQL との互換性の問題、エラー メッセージの報告、プレフィックス インデックスの範囲、UPDATE` ステートメントのpanicの問題が含まれます。TiKV では、リージョンマージに関連する 2 つの問題も修正されました。
---

# TiDB 2.0.11 リリースノート {#tidb-2-0-11-release-notes}

2019 年 1 月 3 日に、TiDB 2.0.11 がリリースされました。対応する TiDB Ansible 2.0.11 もリリースされました。TiDB 2.0.10 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## ティビ {#tidb}

-   PDが異常な状態にあるときにエラーが適切に処理されない問題を修正[＃8764](https://github.com/pingcap/tidb/pull/8764)
-   TiDBのテーブルに対する`Rename`操作がMySQL [＃8809](https://github.com/pingcap/tidb/pull/8809)の操作と互換性がない問題を修正
-   `ADD INDEX`ステートメント[＃8750](https://github.com/pingcap/tidb/pull/8750)の実行中に`ADMIN CHECK TABLE`操作が実行されると、エラー メッセージが誤って報告される問題を修正しました。
-   プレフィックスインデックスの範囲が間違っている場合がある問題を修正[＃8877](https://github.com/pingcap/tidb/pull/8877)
-   場合によっては列が追加されたときに`UPDATE`ステートメントがpanic問題を修正[＃8904](https://github.com/pingcap/tidb/pull/8904)

## ティクヴ {#tikv}

-   リージョンマージ[＃4003](https://github.com/tikv/tikv/pull/4003)に関する2つ[＃4004](https://github.com/tikv/tikv/pull/4004)問題を修正
