---
title: TiDB Binlog Glossary
summary: Learn the terms used in TiDB Binlog.
---

# TiDB Binlog用語集 {#tidb-binlog-glossary}

このドキュメントでは、TiDB Binlogのログ、監視、構成、およびドキュメントで使用される用語を一覧表示します。

## Binlog {#binlog}

TiDB Binlogでは、binlog は TiDB からのバイナリ ログ データを参照します。また、 Drainer がKafka またはファイルに書き込むバイナリ ログ データも参照します。前者と後者では形式が異なります。さらに、TiDB のバイナリログと MySQL のバイナリログも異なる形式です。

## Binlogイベント {#binlog-event}

TiDB の DML バイナリログには、 `INSERT` 、 `UPDATE` 、および`DELETE`の 3 種類のイベントがあります。 Drainerの監視ダッシュボードでは、レプリケーション データに対応するさまざまなイベントの数を確認できます。

## チェックポイント {#checkpoint}

チェックポイントは、レプリケーション タスクが一時停止されてから再開されるか、または停止されてから再開される位置を示します。 Drainerがダウンストリームにレプリケートする commit-ts を記録します。再起動すると、 Drainer はチェックポイントを読み取り、対応する commit-ts からデータの複製を開始します。

## セーフモード {#safe-mode}

セーフ モードとは、増分レプリケーション タスクのテーブル スキーマに主キーまたは一意のインデックスが存在する場合に、DML のべき等インポートをサポートするモードを指します。

このモードでは、ステートメント`INSERT`は`REPLACE`として書き換えられ、ステートメント`UPDATE`は`DELETE`および`REPLACE`として書き換えられます。次に、書き直されたステートメントが下流に実行されます。 Drainerの起動後、5 分以内にセーフ モードが自動的に有効になります。構成ファイルの`safe-mode`パラメータを変更することで手動でモードを有効にすることができますが、この構成はダウンストリームが MySQL または TiDB の場合にのみ有効です。
