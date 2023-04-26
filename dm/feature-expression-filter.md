---
title: Filter DMLs Using SQL Expressions
---

# SQL 式を使用した DML のフィルタリング {#filter-dmls-using-sql-expressions}

## 概要 {#overview}

増分データ移行のプロセスでは、 [Binlogイベントのフィルタリング](/filter-binlog-event.md)機能を使用して特定のタイプのbinlogイベントをフィルタリングできます。たとえば、アーカイブまたは監査の目的で、データをダウンストリームに移行するときに`DELETE`イベントを除外できます。ただし、 Binlog Event Filter は、 `DELETE`のイベントの特定の行をフィルターで除外するかどうかをより細かく判断することはできません。

上記の問題を解決するために、DM は v2.0.5 以降、 `binlog value filter`使用した増分移行中のデータのフィルタリングをサポートしています。 DM でサポートされている`ROW`形式のbinlogには、 binlogイベントのすべての列の値があります。これらの値に従って、SQL 式を構成できます。 SQL 式が行の変更を`TRUE`と評価する場合、DM は行の変更をダウンストリームに移行しません。

詳細な操作と実装については、 [SQL 式を使用した DML イベントのフィルタリング](/filter-dml-event.md)を参照してください。
