---
title: LOCK TABLES and UNLOCK TABLES
summary: TiDB データベースの LOCK TABLES および UNLOCK TABLES の使用法の概要。
---

# テーブルのロックとテーブルのロック解除 {#lock-tables-and-unlock-tables}

> **警告：**
>
> `LOCK TABLES`と`UNLOCK TABLES`現在のバージョンにおける実験的機能です。本番環境での使用は推奨されません。

TiDBでは、クライアントセッションがテーブルロックを取得して、他のセッションと連携してテーブルにアクセスしたり、他のセッションによるテーブルの変更を防止したりできます。セッションは、自身のロックのみを取得または解放できます。あるセッションが別のセッションのロックを取得したり、別のセッションが保持しているロックを解放したりすることはできません。

`LOCK TABLES` 、現在のクライアントセッションのテーブルロックを取得します。ロック対象となる各オブジェクトに対して`LOCK TABLES`および`SELECT`権限を持っている場合は、共通テーブルのテーブルロックを取得できます。

`UNLOCK TABLES` 、現在のセッションによって保持されているすべてのテーブル ロックを明示的に解放します。2 `LOCK TABLES` 、新しいロックを取得する前に、現在のセッションによって保持されているすべてのテーブル ロックを暗黙的に解放します。

テーブルロックは、他のセッションによる読み取りや書き込みから保護します。1 ロックを保持しているセッションは、 `WRITE`や`TRUNCATE TABLE` `DROP TABLE`のテーブルレベルの操作を実行できます。

> **注記：**
>
> テーブル ロック機能はデフォルトで無効になっています。
>
> -   TiDB Self-Managed の場合、テーブル ロック機能を有効にするには、すべての TiDB インスタンスの構成ファイルで[`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) ～ `true`設定する必要があります。
> -   TiDB Cloud Dedicated の場合、テーブル ロック機能を有効にするには、 [TiDB Cloudサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)連絡して[`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400)を`true`に設定する必要があります。
> -   [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合、 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400)から`true`設定はサポートされていません。

## 概要 {#synopsis}

```ebnf+diagram
LockTablesDef
         ::= 'LOCK' ( 'TABLES' | 'TABLE' ) TableName LockType ( ',' TableName LockType)*


UnlockTablesDef
         ::= 'UNLOCK' 'TABLES'

LockType
         ::= 'READ' ('LOCAL')?
           | 'WRITE' ('LOCAL')?
```

## テーブルロックを取得する {#acquire-table-locks}

`LOCK TABLES`ステートメントを使用すると、現在のセッション内でテーブルロックを取得できます。使用可能なロックの種類は次のとおりです。

`READ`ロック:

-   このロックを保持しているセッションはテーブルを読み取ることはできますが、書き込むことはできません。
-   複数のセッションが同時に同じテーブルから`READ`ロックを取得できます。
-   他のセッションは、 `READ`ロックを明示的に取得せずにテーブルを読み取ることができます。

`READ LOCAL`ロックは MySQL との構文互換性のためだけのものであり、サポートされていません。

`WRITE`ロック:

-   このロックを保持しているセッションは、テーブルを読み書きできます。
-   このロックを保持しているセッションのみがテーブルにアクセスできます。ロックが解除されるまで、他のセッションはテーブルにアクセスできません。

`WRITE LOCAL`ロック:

-   このロックを保持しているセッションは、テーブルを読み書きできます。
-   このロックを保持しているセッションのみがテーブルにアクセスできます。他のセッションはテーブルを読み取ることはできますが、書き込むことはできません。

`LOCK TABLES`ステートメントに必要なロックが別のセッションによって保持されている場合、 `LOCK TABLES`ステートメントは待機する必要があり、このステートメントの実行時にエラーが返されます。次に例を示します。

```sql
> LOCK TABLES t1 READ;
ERROR 8020 (HY000): Table 't1' was locked in WRITE by server: f4799bcb-cad7-4285-8a6d-23d3555173f1_session: 2199023255959
```

上記のエラーメッセージは、TiDB `f4799bcb-cad7-4285-8a6d-23d3555173f1`の ID `2199023255959`のセッションが既にテーブル`t1`の`WRITE`ロックを保持していることを示しています。したがって、現在のセッションはテーブル`t1`の`READ`ロックを取得できません。

`LOCK TABLES`つのステートメントで同じテーブル ロックを複数回取得することはできません。

```sql
> LOCK TABLES t WRITE, t READ;
ERROR 1066 (42000): Not unique table/alias: 't'
```

## テーブルロックを解除する {#release-table-locks}

セッションによって保持されているテーブルロックが解放されると、それらはすべて同時に解放されます。セッションは、明示的または暗黙的にロックを解放できます。

-   セッションは`UNLOCK TABLES`使用して明示的にロックを解除できます。
-   セッションがすでにロックを保持しているときにロックを取得するために`LOCK TABLES`ステートメントを発行すると、新しいロックが取得される前に既存のロックが暗黙的に解放されます。

クライアントセッションの接続が正常終了か異常終了かにかかわらず終了した場合、TiDB はセッションで保持されていたすべてのテーブルロックを暗黙的に解放します。クライアントが再接続すると、ロックは無効になります。そのため、クライアント側で自動再接続を有効にすることは推奨されません。自動再接続を有効にすると、再接続が発生してもクライアントには通知されず、すべてのテーブルロックまたは現在のトランザクションが失われます。一方、自動再接続が無効になっている場合、接続が切断されると、次のステートメントが発行されるときにエラーが発生します。クライアントはエラーを検出し、ロックの再取得やトランザクションのやり直しなどの適切なアクションを実行できます。

## テーブルロックの制限と条件 {#table-locking-restrictions-and-conditions}

テーブル ロックを保持しているセッションを安全に終了するには、 `KILL`使用できます。

次のデータベース内のテーブルに対してテーブル ロックを取得することはできません。

-   `INFORMATION_SCHEMA`
-   `PERFORMANCE_SCHEMA`
-   `METRICS_SCHEMA`
-   `mysql`

## MySQLの互換性 {#mysql-compatibility}

### テーブルロックの取得 {#table-lock-acquisition}

-   TiDBでは、セッションAが既にテーブルロックを保持している場合、セッションBがそのテーブルに書き込みを試みるとエラーが返されます。MySQLでは、セッションBの書き込み要求はセッションAがテーブルロックを解放するまでブロックされ、他のセッションからのテーブルロック要求は現在のセッションが`WRITE`ロックを解放するまでブロックされます。
-   TiDBでは、 `LOCK TABLES`文に必要なロックが別のセッションによって保持されている場合、 `LOCK TABLES`の文は待機する必要があり、この文の実行時にエラーが返されます。MySQLでは、この文はロックが取得されるまでブロックされます。
-   TiDBでは、 `LOCK TABLES`文はクラスタ全体で有効です。MySQLでは、この文は現在のMySQLサーバーでのみ有効であり、NDBクラスタとは互換性がありません。

### テーブルロックの解除 {#table-lock-release}

TiDB セッションでトランザクションが明示的に開始されると (たとえば、 `BEGIN`ステートメントを使用)、TiDB はセッションによって保持されているテーブル ロックを暗黙的に解放しませんが、MySQL は解放します。
