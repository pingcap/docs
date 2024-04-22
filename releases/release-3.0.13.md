---
title: TiDB 3.0.13 Release Notes
summary: TiDB 3.0.13が2020年4月22日にリリースされました。このバージョンでは、複数行の重複データを挿入する際のトランザクション内でのステートメント誤りの問題や、`Region Merge`を繰り返し実行するとシステムが固まる問題が修正されています。TiDBの修正には、`MemBuffer` `INSERT ... ON DUPLICATE KEY UPDATE`チェックによって引き起こされる問題が含まれます。TiKVの修正には、サービスが利用できなくなる問題が含まれます。
---

# TiDB 3.0.13 リリースノート {#tidb-3-0-13-release-notes}

発売日：2020年4月22日

TiDB バージョン: 3.0.13

## バグの修正 {#bug-fixes}

-   TiDB

    -   ユーザーが複数行の重複データを挿入する必要がある場合に、トランザクション内でステートメントが誤って実行される可能性がある`MemBuffer` `INSERT ... ON DUPLICATE KEY UPDATE`チェックによって引き起こされる問題を修正します[#16690](https://github.com/pingcap/tidb/pull/16690)

-   TiKV

    -   `Region Merge`を繰り返し実行するとシステムが固まりサービスが利用できなくなる場合がある問題を修正[#7612](https://github.com/tikv/tikv/pull/7612)
