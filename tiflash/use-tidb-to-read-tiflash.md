---
title: Use TiDB to Read TiFlash Replicas
summary: Learn how to use TiDB to read TiFlash replicas.
---

# TiDB を使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

このドキュメントでは、TiDB を使用してTiFlashレプリカを読み取る方法を紹介します。

TiDB は、 TiFlashレプリカを読み取る 3 つの方法を提供します。エンジン構成なしでTiFlashレプリカを追加した場合、CBO (コストベースの最適化) モードがデフォルトで使用されます。

## スマートセレクション {#smart-selection}

TiFlashレプリカを含むテーブルの場合、TiDB オプティマイザは、コストの見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。 `desc`または`explain analyze`ステートメントを使用して、 TiFlashレプリカが選択されているかどうかを確認できます。例えば：

{{< copyable "" >}}

```sql
desc select count(*) from test.t;
```

```
+--------------------------+---------+--------------+---------------+--------------------------------+
| id                       | estRows | task         | access object | operator info                  |
+--------------------------+---------+--------------+---------------+--------------------------------+
| StreamAgg_9              | 1.00    | root         |               | funcs:count(1)->Column#4       |
| └─TableReader_17         | 1.00    | root         |               | data:TableFullScan_16          |
|   └─TableFullScan_16     | 1.00    | cop[tiflash] | table:t       | keep order:false, stats:pseudo |
+--------------------------+---------+--------------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
explain analyze select count(*) from test.t;
```

```
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | tiflash_task:{time:43ms, loops:1, threads:1}, tiflash_scan:{...}     | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` 、タスクが処理のためにTiFlashに送信されることを意味します。 TiFlashレプリカを選択していない場合は、 `analyze table`ステートメントを使用して統計を更新してから、 `explain analyze`ステートメントを使用して結果を確認できます。

テーブルにTiFlashレプリカが 1 つしかなく、関連するノードがサービスを提供できない場合、CBO モードのクエリは繰り返し再試行されることに注意してください。この状況では、エンジンを指定するか、手動ヒントを使用して TiKV レプリカからデータを読み取る必要があります。

## エンジンの分離 {#engine-isolation}

エンジンの分離とは、対応する変数を構成することにより、すべてのクエリが指定されたエンジンのレプリカを使用することを指定することです。オプションのエンジンは、「tikv」、「tidb」(一部の TiDB システム テーブルを格納し、ユーザーが積極的に使用できない TiDB の内部メモリテーブル領域を示します)、および「tiflash」です。

<CustomContent platform="tidb">

次の 2 つの構成レベルでエンジンを指定できます。

-   TiDB インスタンス レベル、つまり INSTANCE レベル。 TiDB 構成ファイルに次の構成項目を追加します。

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **INSTANCE レベルのデフォルト設定は`[&quot;tikv&quot;, &quot;tidb&quot;, &quot;tiflash&quot;]`です。**

-   セッションレベル。次のステートメントを使用して構成します。

    {{< copyable "" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    また

    {{< copyable "" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    SESSION レベルのデフォルト構成は、TiDB INSTANCE レベルの構成を継承しています。

最終的なエンジン構成はセッション レベルの構成です。つまり、セッション レベルの構成がインスタンス レベルの構成をオーバーライドします。たとえば、INSTANCE レベルで「tikv」を構成し、SESSION レベルで「tiflash」を構成した場合、 TiFlashレプリカが読み取られます。最終的なエンジン構成が「tikv」および「tiflash」である場合、TiKV およびTiFlashレプリカの両方が読み取られ、オプティマイザーは実行するより適切なエンジンを自動的に選択します。

> **ノート：**
>
> [TiDB ダッシュボード](/dashboard/dashboard-intro.md)およびその他のコンポーネントは、TiDBメモリテーブル領域に格納されているシステム テーブルを読み取る必要があるため、インスタンス レベルのエンジン構成に常に「tidb」エンジンを追加することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

次のステートメントを使用してエンジンを指定できます。

```sql
set @@session.tidb_isolation_read_engines = "engine list separated by commas";
```

また

```sql
set SESSION tidb_isolation_read_engines = "engine list separated by commas";
```

</CustomContent>

照会されたテーブルに指定されたエンジンのレプリカがない場合 (たとえば、エンジンが「tiflash」として構成されているが、テーブルにTiFlashレプリカがない場合)、クエリはエラーを返します。

## 手動ヒント {#manual-hint}

手動ヒントは、TiDB が特定のテーブルに対して指定されたレプリカを使用するように強制することができます。手動ヒントの使用例を次に示します。

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

クエリ ステートメントでテーブルにエイリアスを設定する場合、ヒントを有効にするには、ヒントを含むステートメントでエイリアスを使用する必要があります。例えば：

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上記のステートメントで、 `tiflash[]`オプティマイザーにTiFlashレプリカを読み取るように促します。 `tikv[]`使用して、オプティマイザーに必要に応じて TiKV レプリカを読み取るように指示することもできます。ヒント構文の詳細については、 [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を参照してください。

ヒントで指定されたテーブルに指定されたエンジンのレプリカがない場合、ヒントは無視され、警告が報告されます。また、ヒントはエンジン分離前提でのみ有効です。ヒントで指定されたエンジンがエンジン分離リストにない場合、ヒントも無視され、警告が報告されます。

> **ノート：**
>
> 5.7.7 以前のバージョンの MySQL クライアントは、デフォルトでオプティマイザ ヒントをクリアします。これらの初期バージョンでヒント構文を使用するには、クライアントを`--comments`オプション (例: `mysql -h 127.0.0.1 -P 4000 -uroot --comments`で起動します。

## スマートセレクション、エンジンアイソレーション、マニュアルヒントの関係 {#the-relationship-of-smart-selection-engine-isolation-and-manual-hint}

上記の 3 つのTiFlashレプリカの読み取り方法では、エンジンの分離により、エンジンの使用可能なレプリカの全体的な範囲が指定されます。この範囲内では、手動ヒントにより、よりきめ細かいステートメント レベルおよびテーブル レベルのエンジン選択が提供されます。最後に、CBO が決定を下し、指定されたエンジン リスト内のコスト見積もりに基づいてエンジンのレプリカを選択します。

> **ノート：**
>
> v4.0.3 より前では、読み取り専用ではない SQL ステートメント (たとえば、 `INSERT INTO ... SELECT` 、 `SELECT ... FOR UPDATE` 、 `UPDATE ...` 、 `DELETE ...` ) でのTiFlashレプリカからの読み取りの動作は定義されていません。 v4.0.3 以降のバージョンでは、データの正確性を保証するために、TiDB は非読み取り専用 SQL ステートメントのTiFlashレプリカを内部的に無視します。つまり、 [スマートセレクション](#smart-selection)場合、TiDB は非TiFlashレプリカを自動的に選択します。 TiFlashレプリカ**のみ**を指定する[エンジン分離](#engine-isolation)の場合、TiDB はエラーを報告します。 [手動ヒント](#manual-hint)の場合、TiDB はヒントを無視します。
