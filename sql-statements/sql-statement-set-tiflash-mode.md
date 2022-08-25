---
title: ALTER TABLE ... SET TIFLASH MODE ...
summary: An overview of the usage of ALTER TABLE ... SET TIFLASH MODE ... for the TiDB database.
---

# <code>ALTER TABLE ... SET TIFLASH MODE ...</code> {#code-alter-table-set-tiflash-mode-code}

> **警告：**
>
> このステートメントは実験的であり、その形式と使用法は後続のバージョンで変更される可能性があります。

`ALTER TABLE...SET TIFLASH MODE...`ステートメントを使用して、TiFlash の対応するテーブルで FastScan を有効または無効にできます。

-   `Normal Mode` : デフォルトのオプション。このモードでは、FastScan が無効になり、クエリ結果の精度とデータの一貫性が保証されます。
-   `Fast Mode` : このモードでは、FastScan が有効になります。 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度とデータの一貫性を保証するものではありません。

`ALTER TABLE ... SET TIFLASH MODE ...`を実行しても、既存の SQL ステートメントがブロックされたり、トランザクション、DDL、GC などの他の TiDB 機能が中断されたりすることはありません。同時に、SQL ステートメントを介してアクセスされるデータは変更されません。モードを切り替えると、このステートメントは正常に終了します。

このステートメントは、TiFlash 内のテーブルの FastScan オプションを切り替えるためにのみ実行できます。したがって、オプションの変更は、TiFlash の読み取りテーブルにのみ影響します。

FastScan スイッチは、テーブルに TiFlash レプリカがある場合にのみ有効になります。オプションを切り替えたときに TiFlash レプリカが存在しない場合、オプションは TiFlash レプリカが構成された後にのみ有効になります。 [`ALTER TABLE ... SET TIFLASH REPLICA ...`](/sql-statements/sql-statement-alter-table.md)を使用して、TiFlash レプリカを構成できます。

システム テーブル`information_schema.tiflash_replica`を使用して、対応するテーブルの現在の TiFlash テーブル スイッチを照会できます。

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableSetTiFlashModeStmt ::=
    'ALTER' 'TABLE' TableName 'SET' 'TIFLASH' 'MODE' mode
```

## 例 {#example}

`test`テーブルに TiFlash レプリカがあるとします。

```sql
USE TEST;
CREATE TABLE test (a INT NOT NULL, b INT);
ALTER TABLE test SET TIFLASH REPLICA 1;
```

`test`テーブルのデフォルト オプションは通常モードです。次のステートメントを使用して、テーブル オプションをクエリできます。

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'test' AND table_schema = 'test'
```

```
+------------+
| table_mode |
+------------+
| NORMAL     |
+------------+
```

`test`テーブルに対して FastScan を有効にするには、次のステートメントを実行し、このテーブルに対して FastScan が有効になっているかどうかを確認します。

```sql
ALTER TABLE test SET tiflash mode FAST
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'test' AND table_schema = 'test'
```

```
+------------+
| table_mode |
+------------+
| FAST       |
+------------+
```

FastScan を無効にするには、次のステートメントを実行します。

```sql
ALTER TABLE test SET tiflash mode NORMAL
```

## MySQL の互換性 {#mysql-compatibility}

`ALTER TABLE ... SET TiFLASH MODE ...`は、TiDB によって導入された標準 SQL 構文の拡張です。同等の MySQL 構文はありませんが、MySQL クライアントから、または MySQL プロトコルに従うデータベース ドライバーから、このステートメントを実行できます。

## TiDB Binlogと TiCDC の互換性 {#tidb-binlog-and-ticdc-compatibility}

下流も TiDB の場合、 `ALTER TABLE ... SET TiFLASH MODE ...`は TiDB Binlogによって下流に同期されます。他のシナリオでは、TiDB Binlogはこのステートメントを同期しません。

FastScan は TiCDC をサポートしていません。

## こちらもご覧ください {#see-also}

-   [他の机](/sql-statements/sql-statement-alter-table.md)
