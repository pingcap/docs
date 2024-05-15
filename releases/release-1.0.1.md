---
title: TiDB 1.0.1 Release Notes
summary: TiDB 1.0.1 was released on November 1, 2017. Updates include support for canceling DDL Job, optimizing the `IN` expression, correcting the result type of the `Show` statement, supporting log slow query into a separate log file, and fixing bugs. TiKV now supports flow control with write bytes, reduces Raft allocation, increases coprocessor stack size to 10MB, and removes the useless log from the coprocessor.
---

# TiDB 1.0.1 リリースノート {#tidb-1-0-1-release-notes}

2017 年 11 月 1 日に、次の更新を含む TiDB 1.0.1 がリリースされました。

## ティビ {#tidb}

-   DDL ジョブのキャンセルをサポートします。
-   `IN`式を最適化します。
-   `Show`ステートメントの結果の型を修正します。
-   遅いクエリを別のログ ファイルに記録することをサポートします。
-   バグを修正しました。

## ティクヴ {#tikv}

-   書き込みバイトによるフロー制御をサポートします。
-   Raft の割り当てを減らします。
-   コプロセッサのスタック サイズを 10 MB に増やします。
-   コプロセッサから不要なログを削除します。
