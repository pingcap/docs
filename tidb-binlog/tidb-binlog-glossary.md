---
title: TiDB Binlog Glossary
summary: Learn the terms used in TiDB Binlog.
---

# TiDBBinlog用語集 {#tidb-binlog-glossary}

このドキュメントでは、TiDB Binlogのログ、モニタリング、構成、およびドキュメントで使用される用語をリストします。

## Binlog {#binlog}

TiDB Binlogでは、binlog は TiDB からのバイナリ ログ データを指します。また、 Drainer がKafka またはファイルに書き込むバイナリ ログ データも参照します。前者と後者は形式が異なります。さらに、TiDB のバイナリログと MySQL のバイナリログも異なる形式です。

## Binlogイベント {#binlog-event}

TiDB の DML バイナリログには、 `INSERT` 、 `UPDATE` 、および`DELETE`の 3 種類のイベントがあります。 Drainerの監視ダッシュボードでは、レプリケーション データに対応するさまざまなイベントの数を確認できます。

## チェックポイント {#checkpoint}

チェックポイントは、レプリケーション タスクが一時停止して再開される位置、または停止して再開される位置を示します。これは、Drainerがダウンストリームにレプリケートするコミット t を記録します。再起動すると、 Drainer はチェックポイントを読み取り、対応する commit-ts からデータの複製を開始します。

## セーフモード {#safe-mode}

セーフ モードは、増分レプリケーション タスクのテーブル スキーマに主キーまたは一意のインデックスが存在する場合に、DML の冪等インポートをサポートするモードを指します。

このモードでは、 `INSERT`ステートメントは`REPLACE`として書き換えられ、 `UPDATE`ステートメントは`DELETE`および`REPLACE`として書き換えられます。その後、書き換えられたステートメントが下流に実行されます。セーフ モードは、 Drainerの起動後 5 分以内に自動的に有効になります。設定ファイルの`safe-mode`パラメータを変更することでこのモードを手動で有効にすることができますが、この設定はダウンストリームが MySQL または TiDB の場合にのみ有効です。
