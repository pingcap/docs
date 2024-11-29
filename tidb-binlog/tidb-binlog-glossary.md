---
title: TiDB Binlog Glossary
summary: TiDB Binlogで使用される用語を学習します。
---

# TiDBBinlog用語集 {#tidb-binlog-glossary}

このドキュメントでは、 TiDB Binlogのログ、監視、構成、およびドキュメントで使用される用語をリストします。

## Binlog {#binlog}

TiDB Binlogでは、binlog は TiDB からのバイナリ ログ データを指します。また、 Drainer がKafka またはファイルに書き込むバイナリ ログ データも指します。前者と後者は形式が異なります。また、TiDB の binlog と MySQL の binlog も形式が異なります。

## Binlogイベント {#binlog-event}

Drainerからの DML バイナリログには、 `INSERT` 、 `UPDATE` 、 `DELETE` 3 種類のイベントがあります。Drainer の監視ダッシュボードでは、レプリケーション データに対応するさまざまなイベントの数を確認できます。

## チェックポイント {#checkpoint}

チェックポイントは、レプリケーション タスクが一時停止されて再開される位置、または停止されて再起動される位置を示します。チェックポイントは、 Drainer がダウンストリームにレプリケートする commit-ts を記録します。再起動すると、 Drainer はチェックポイントを読み取り、対応する commit-ts からデータのレプリケートを開始します。

## セーフモード {#safe-mode}

セーフ モードとは、増分レプリケーション タスクのテーブル スキーマに主キーまたは一意のインデックスが存在する場合に、DML のべき等インポートをサポートするモードを指します。

このモードでは、 `INSERT`ステートメントは`REPLACE`に、 `UPDATE`ステートメントは`DELETE`と`REPLACE`に書き換えられ、書き換えられたステートメントが下流に実行されます。セーフ モードは、 Drainerの起動後 5 分以内に自動的に有効になります。設定ファイルの`safe-mode`パラメータを変更することで、このモードを手動で有効にできますが、この設定は下流が MySQL または TiDB の場合にのみ有効です。
