---
title: Filter DMLs Using SQL Expressions
---

# SQL式を使用したDMLのフィルタリング {#filter-dmls-using-sql-expressions}

## 概要 {#overview}

増分データ移行のプロセスでは、 [Binlogイベントのフィルタリング](/filter-binlog-event.md)機能を使用して特定の種類のbinlogイベントをフィルターできます。たとえば、アーカイブまたは監査の目的で、データをダウンストリームに移行するときに`DELETE`イベントをフィルターで除外できます。ただし、 Binlogイベント フィルターは、 `DELETE`のイベントの特定の行をフィルターで除外するかどうかをより詳細に判断できません。

上記の問題を解決するために、DM は v2.0.5 以降、 `binlog value filter`使用した増分移行中のデータのフィルタリングをサポートしています。 DM でサポートされている`ROW`形式のbinlogには、binlogイベントのすべての列の値が含まれています。これらの値に従って SQL 式を構成できます。 SQL 式が行変更を`TRUE`と評価した場合、DM は行変更をダウンストリームに移行しません。

詳細な操作と実装については、 [SQL式を使用したDMLイベントのフィルタリング](/filter-dml-event.md)を参照してください。
