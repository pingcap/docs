---
title: TiDB 2.0.2 Release Notes
summary: TiDB 2.0.2は2018年5月21日にリリースされ、システムの安定性が向上しました。このリリースには、小数除算式の修正、Delete`ステートメントでの`USE INDEX`構文のサポート、TiDBへのBinlog書き込みのタイムアウトメカニズムが含まれています。PDは、バランスリーダースケジューラで切断されたノードをフィルタリングし、転送リーダーオペレータのタイムアウトを修正し、スケジューリングの問題を修正しました。TiKVは、 Raftログ出力を修正し、gRPCパラメータの設定、リーダー選出タイムアウト範囲のサポート、スナップショット中間ファイル削除の問題を解決しました。
---

# TiDB 2.0.2 リリースノート {#tidb-2-0-2-release-notes}

2018年5月21日にTiDB 2.0.2がリリースされました。このリリースでは、TiDB 2.0.1と比較して、システムの安定性が大幅に向上しています。

## TiDB {#tidb}

-   小数点以下の除算式を押し下げる問題を修正
-   Support using the `USE INDEX` syntax in the `Delete` statement
-   `Auto-Increment`列目では`shard_row_id_bits`機能の使用を禁止する
-   Binlog書き込みのタイムアウト機構を追加する

## PD {#pd}

-   バランスリーダースケジューラが切断されたノードをフィルタリングするようにする
-   転送リーダーオペレータのタイムアウトを10秒に変更します
-   クラスターのリージョンが異常な状態にあるときにラベル スケジューラがスケジュールを実行しない問題を修正しました
-   Fix the improper scheduling issue of `evict leader scheduler`

## TiKV {#tikv}

-   Raftログが印刷されない問題を修正
-   より多くの gRPC 関連パラメータの設定をサポート
-   リーダー選出のタイムアウト範囲の設定をサポート
-   古くなった学習者が削除されない問題を修正
-   Fix the issue that the snapshot intermediate file is mistakenly deleted
