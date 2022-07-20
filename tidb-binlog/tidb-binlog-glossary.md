---
title: TiDB Binlog Glossary
summary: Learn the terms used in TiDB Binlog.
---

# Binlog用語集 {#tidb-binlog-glossary}

このドキュメントには、TiDB Binlogのログ、監視、構成、およびドキュメントで使用される用語がリストされています。

## Binlog {#binlog}

TiDB Binlogでは、binlogはTiDBからのバイナリログデータを参照します。また、 DrainerがKafkaまたはファイルに書き込むバイナリログデータも参照します。前者と後者は異なる形式です。さらに、TiDBのbinlogとMySQLのbinlogも異なる形式になっています。

## Binlogイベント {#binlog-event}

TiDBのDMLbinlogには、 `INSERT` 、および`DELETE`の`UPDATE`種類のイベントがあります。 Drainerの監視ダッシュボードでは、レプリケーションデータに対応するさまざまなイベントの数を確認できます。

## チェックポイント {#checkpoint}

チェックポイントは、レプリケーションタスクが一時停止して再開する位置、または停止して再開する位置を示します。 Drainerがダウンストリームに複製するコミットを記録します。再起動すると、 Drainerはチェックポイントを読み取り、対応するコミットからデータの複製を開始します。

## セーフモード {#safe-mode}

セーフモードとは、インクリメンタルレプリケーションタスクのテーブルスキーマに主キーまたは一意のインデックスが存在する場合に、DMLのべき等インポートをサポートするモードを指します。

このモードでは、 `INSERT`ステートメントは`REPLACE`として書き直され、 `UPDATE`ステートメントは`DELETE`および`REPLACE`として書き直されます。次に、書き直されたステートメントがダウンストリームに対して実行されます。セーフモードは、 Drainerの起動後5分以内に自動的に有効になります。構成ファイルの`safe-mode`パラメーターを変更することでモードを手動で有効にできますが、この構成は、ダウンストリームがMySQLまたはTiDBの場合にのみ有効です。
