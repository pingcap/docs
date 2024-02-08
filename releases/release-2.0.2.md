---
title: TiDB 2.0.2 Release Notes
summary: TiDB 2.0.2 was released on May 21, 2018, with improvements in system stability. The release includes fixes for Decimal division expression, support for `USE INDEX` syntax in `Delete` statement, and timeout mechanism for writing Binlog in TiDB. PD now filters disconnected nodes in balance leader scheduler, modifies transfer leader operator timeout, and fixes scheduling issues. TiKV fixes Raft log printing, supports configuring gRPC parameters, leader election timeout range, and resolves snapshot intermediate file deletion issue.
---

# TiDB 2.0.2 リリースノート {#tidb-2-0-2-release-notes}

2018 年 5 月 21 日に、TiDB 2.0.2 がリリースされました。 TiDB 2.0.1 と比較して、このリリースではシステムの安定性が大幅に向上しています。

## TiDB {#tidb}

-   10 進数の除算式を押し下げる問題を修正
-   `Delete`ステートメントでの`USE INDEX`構文の使用のサポート
-   `Auto-Increment`列で`shard_row_id_bits`機能を使用することを禁止します
-   Binlogを書き込むためのタイムアウト メカニズムを追加する

## PD {#pd}

-   バランス リーダー スケジューラが切断されたノードをフィルタリングするようにする
-   転送リーダー オペレーターのタイムアウトを 10 秒に変更します。
-   クラスターのリージョンが異常な状態にある場合、ラベル スケジューラーがスケジュールを実行しない問題を修正します。
-   `evict leader scheduler`の不適切なスケジュールの問題を修正します。

## TiKV {#tikv}

-   Raftログが印刷されない問題を修正
-   より多くの gRPC 関連パラメーターの構成をサポート
-   リーダー選出のタイムアウト範囲の構成をサポート
-   廃止された学習者が削除されない問題を修正
-   スナップショット中間ファイルが誤って削除される問題を修正
