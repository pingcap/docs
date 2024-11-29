---
title: Use TiDB to Read TiFlash Replicas
summary: TiDB を使用してTiFlashレプリカを読み取る方法を学習します。
---

# TiDB を使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

このドキュメントでは、TiDB を使用してTiFlashレプリカを読み取る方法について説明します。

TiDB は、 TiFlashレプリカを読み取る 3 つの方法を提供します。エンジン構成なしでTiFlashレプリカを追加した場合、デフォルトで CBO (コストベースの最適化) モードが使用されます。

## スマートな選択 {#smart-selection}

TiFlashレプリカを持つテーブルの場合、TiDB オプティマイザーはコスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。1 または`desc` `explain analyze`ステートメントを使用して、 TiFlashレプリカが選択されているかどうかを確認できます。例:

```sql
desc select count(*) from test.t;
```

    +--------------------------+---------+--------------+---------------+--------------------------------+
    | id                       | estRows | task         | access object | operator info                  |
    +--------------------------+---------+--------------+---------------+--------------------------------+
    | StreamAgg_9              | 1.00    | root         |               | funcs:count(1)->Column#4       |
    | └─TableReader_17         | 1.00    | root         |               | data:TableFullScan_16          |
    |   └─TableFullScan_16     | 1.00    | cop[tiflash] | table:t       | keep order:false, stats:pseudo |
    +--------------------------+---------+--------------+---------------+--------------------------------+
    3 rows in set (0.00 sec)

```sql
explain analyze select count(*) from test.t;
```

    +--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
    | id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
    +--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
    | StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
    | └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
    |   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | tiflash_task:{time:43ms, loops:1, threads:1}, tiflash_scan:{...}     | keep order:false, stats:pseudo | N/A       | N/A  |
    +--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+

`cop[tiflash]`タスクが処理のためにTiFlashに送信されることを意味します。TiFlash レプリカを選択していない場合は、 `analyze table`ステートメントを使用して統計を更新し、 `explain analyze`ステートメントを使用して結果を確認できます。

テーブルにTiFlashレプリカが 1 つしかなく、関連するノードがサービスを提供できない場合、CBO モードのクエリは繰り返し再試行されることに注意してください。この状況では、エンジンを指定するか、手動ヒントを使用して TiKV レプリカからデータを読み取る必要があります。

## エンジン分離 {#engine-isolation}

エンジン分離とは、対応する変数を設定することで、すべてのクエリが指定されたエンジンのレプリカを使用するように指定することです。オプションのエンジンは、「tikv」、「tidb」（TiDB の内部メモリテーブル領域を示します。一部の TiDB システム テーブルが格納され、ユーザーがアクティブに使用することはできません）、および「tiflash」です。

<CustomContent platform="tidb">

次の 2 つの構成レベルでエンジンを指定できます。

-   TiDB インスタンス レベル、つまり INSTANCE レベル。TiDB 構成ファイルに次の構成項目を追加します。

        [isolation-read]
        engines = ["tikv", "tidb", "tiflash"]

    **INSTANCE レベルのデフォルト設定は`[&quot;tikv&quot;, &quot;tidb&quot;, &quot;tiflash&quot;]`です。**

-   SESSION レベル。次のステートメントを使用して構成します。

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    または

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    SESSION レベルのデフォルト構成は、TiDB INSTANCE レベルの構成を継承します。

最終的なエンジン構成はセッション レベルの構成です。つまり、セッション レベルの構成はインスタンス レベルの構成をオーバーライドします。たとえば、INSTANCE レベルで「tikv」を構成し、SESSION レベルで「tiflash」を構成した場合、 TiFlashレプリカが読み取られます。最終的なエンジン構成が「tikv」と「tiflash」の場合、TiKV レプリカとTiFlashレプリカの両方が読み取られ、オプティマイザーはより適切なエンジンを自動的に選択して実行します。

> **注記：**
>
> [TiDBダッシュボード](/dashboard/dashboard-intro.md)およびその他のコンポーネントは、TiDBメモリテーブル領域に格納されている一部のシステム テーブルを読み取る必要があるため、インスタンス レベルのエンジン構成に常に「tidb」エンジンを追加することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

次のステートメントを使用してエンジンを指定できます。

```sql
set @@session.tidb_isolation_read_engines = "engine list separated by commas";
```

または

```sql
set SESSION tidb_isolation_read_engines = "engine list separated by commas";
```

</CustomContent>

クエリされたテーブルに指定されたエンジンのレプリカがない場合 (たとえば、エンジンが「tiflash」として構成されているが、テーブルにTiFlashレプリカがない場合)、クエリはエラーを返します。

## マニュアルのヒント {#manual-hint}

手動ヒントを使用すると、エンジン分離を満たすという前提で、特定のテーブルに対して指定されたレプリカを TiDB が使用するように強制できます。手動ヒントの使用例を次に示します。

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

クエリ ステートメントでテーブルに別名を設定する場合、ヒントを有効にするには、ヒントを含むステートメントで別名を使用する必要があります。例:

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上記のステートメントでは、 `tiflash[]`​​オプティマイザにTiFlashレプリカの読み取りを指示します。 `tikv[]`使用して、必要に応じてオプティマイザに TiKV レプリカの読み取りを指示することもできます。 ヒント構文の詳細については、 [ストレージからの読み取り](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を参照してください。

ヒントで指定されたテーブルに指定されたエンジンのレプリカがない場合、ヒントは無視され、警告が報告されます。また、ヒントはエンジン分離を前提としてのみ有効です。ヒントで指定されたエンジンがエンジン分離リストにない場合も、ヒントは無視され、警告が報告されます。

> **注記：**
>
> 5.7.7 以前のバージョンの MySQL クライアントは、デフォルトでオプティマイザヒントをクリアします。これらの初期バージョンのヒント構文を使用するには、 `--comments`オプション (例: `mysql -h 127.0.0.1 -P 4000 -uroot --comments` ) でクライアントを起動します。

## スマート選択、エンジン分離、手動ヒントの関係 {#the-relationship-of-smart-selection-engine-isolation-and-manual-hint}

上記の 3 つのTiFlashレプリカの読み取り方法では、エンジン分離によって、使用可能なエンジンのレプリカの全体的な範囲が指定されます。この範囲内で、手動ヒントによって、よりきめ細かいステートメント レベルおよびテーブル レベルのエンジン選択が提供されます。最後に、CBO が決定を下し、指定されたエンジン リスト内のコスト見積もりに基づいてエンジンのレプリカを選択します。

> **注記：**
>
> -   v4.0.3 より前では、読み取り専用でない SQL ステートメント (たとえば、 `INSERT INTO ... SELECT` 、 `SELECT ... FOR UPDATE` 、 `UPDATE ...` 、 `DELETE ...` ) でTiFlashレプリカから読み取る動作は未定義です。
> -   バージョン v4.0.3 から v6.2.0 では、データの正確性を保証するために、 TiDB は非読み取り専用 SQL ステートメントのTiFlashレプリカを内部的に無視します。つまり、 [賢い選択](#smart-selection)場合、 TiDB は非TiFlashレプリカを自動的に選択し、 TiFlashレプリカ**のみ**を指定する[エンジン分離](#engine-isolation)の場合、 TiDB はエラーを報告し、 [マニュアルのヒント](#manual-hint)の場合、 TiDB はヒントを無視します。
> -   バージョン v6.3.0 から v7.0.0 では、 TiFlashレプリカが有効になっている場合、 [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)変数を使用して、TiDB が読み取り専用でない SQL ステートメントにTiFlashレプリカを使用するかどうかを制御できます。
> -   v7.1.0 以降では、 TiFlashレプリカが有効になっていて、現在のセッションの[SQL モード](/sql-mode.md)が厳密でない場合 (つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`または`STRICT_ALL_TABLES`含まれていない場合)、TiDB はコスト見積もりに基づいて、非読み取り専用 SQL ステートメントにTiFlashレプリカを使用するかどうかを自動的に決定します。
