---
title: Filter DMLs Using SQL Expressions
---

# SQL式を使用してDMLをフィルタリングする {#filter-dmls-using-sql-expressions}

## 概要 {#overview}

増分データ移行のプロセスでは、 [Binlogイベントをフィルタリングする](/filter-binlog-event.md)機能を使用して特定のタイプのbinlogイベントをフィルタリングできます。たとえば、アーカイブまたは監査の目的で、データをダウンストリームに移行するときに`DELETE`のイベントを除外できます。ただし、Binlog Event Filterは、 `DELETE`のイベントの特定の行を除外するかどうかをより詳細に判断することはできません。

上記の問題を解決するために、DMはv2.0.5以降の`binlog value filter`を使用した増分移行中のデータのフィルタリングをサポートしています。 DMでサポートされている`ROW`形式のbinlogには、binlogイベントのすべての列の値があります。これらの値に従ってSQL式を構成できます。 SQL式が行の変更を`TRUE`と評価した場合、DMは行の変更をダウンストリームに移行しません。

詳細な操作と実装については、 [SQL式を使用してDMLイベントをフィルタリングする](/filter-dml-event.md)を参照してください。
