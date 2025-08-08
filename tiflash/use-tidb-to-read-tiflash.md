---
title: Use TiDB to Read TiFlash Replicas
summary: TiDB を使用してTiFlashレプリカを読み取る方法を学習します。
---

# TiDB を使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

このドキュメントでは、TiDB を使用してTiFlashレプリカを読み取る方法を紹介します。

TiDBは、 TiFlashレプリカを読み取る3つの方法を提供します。エンジン設定なしでTiFlashレプリカを追加した場合、デフォルトでCBO（コストベース最適化）モードが使用されます。

## スマートな選択 {#smart-selection}

TiFlashレプリカを持つテーブルの場合、TiDBオプティマイザーはコスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。1または`desc` `explain analyze`ステートメントを使用して、 TiFlashレプリカが選択されているかどうかを確認できます。例：

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

`cop[tiflash]` 、タスクが処理のためにTiFlashに送信されることを意味します。TiFlash レプリカを選択してTiFlashない場合は、 `analyze table`ステートメントを使用して統計情報を更新し、 `explain analyze`ステートメントを使用して結果を確認できます。

テーブルにTiFlashレプリカが1つしか存在せず、関連ノードがサービスを提供できない場合、CBOモードのクエリは繰り返し再試行されることに注意してください。このような状況では、エンジンを指定するか、手動ヒントを使用してTiKVレプリカからデータを読み取る必要があります。

## エンジン分離 {#engine-isolation}

エンジン分離とは、対応する変数を設定することで、すべてのクエリが指定されたエンジンのレプリカを使用するように指定することです。オプションのエンジンは、「tikv」、「tidb」（TiDBの内部メモリテーブル領域を示し、一部のTiDBシステムテーブルが格納されており、ユーザーが積極的に使用することはできません）、および「tiflash」です。

<CustomContent platform="tidb">

次の 2 つの構成レベルでエンジンを指定できます。

-   TiDBインスタンスレベル、つまりINSTANCEレベル。TiDB設定ファイルに以下の設定項目を追加します。

        [isolation-read]
        engines = ["tikv", "tidb", "tiflash"]

    **INSTANCE レベルのデフォルト設定は`[&quot;tikv&quot;, &quot;tidb&quot;, &quot;tiflash&quot;]`です。**

-   SESSIONレベル。設定するには次のステートメントを使用します。

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    または

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    SESSION レベルのデフォルト構成は、TiDB INSTANCE レベルの構成を継承します。

最終的なエンジン構成はセッションレベルの構成です。つまり、セッションレベルの構成はインスタンスレベルの構成をオーバーライドします。例えば、インスタンスレベルで「tikv」を設定し、セッションレベルで「tiflash」を設定した場合、 TiFlashレプリカが読み込まれます。最終的なエンジン構成が「tikv」と「tiflash」の場合、TiKVレプリカとTiFlashレプリカの両方が読み込まれ、オプティマイザーはより適切なエンジンを自動的に選択して実行します。

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

クエリされたテーブルに指定されたエンジンのレプリカがない場合 (たとえば、エンジンが「tiflash」として設定されているが、テーブルにTiFlashレプリカがない場合)、クエリはエラーを返します。

## 手動ヒント {#manual-hint}

手動ヒントを使用すると、エンジン分離が満たされていることを前提に、特定のテーブルに対して指定されたレプリカを使用するようにTiDBに強制できます。以下は手動ヒントの使用例です。

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

クエリ文でテーブルに別名を設定した場合、ヒントを有効にするには、ヒントを含む文でもその別名を使用する必要があります。例:

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上記の文では、 `tiflash[]`オプティマイザにTiFlashレプリカの読み取りを指示します。また、 `tikv[]`使用すると、必要に応じてオプティマイザに TiKV レプリカの読み取りを指示できます。ヒント構文の詳細については、 [ストレージからの読み取り](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を参照してください。

ヒントで指定されたテーブルに指定されたエンジンのレプリカが存在しない場合、ヒントは無視され、警告が報告されます。また、ヒントはエンジン分離を前提としてのみ有効です。ヒントで指定されたエンジンがエンジン分離リストに含まれていない場合も、ヒントは無視され、警告が報告されます。

> **注記：**
>
> MySQLクライアント5.7.7以前のバージョンでは、オプティマイザヒントがデフォルトでクリアされます。これらの初期バージョンのヒント構文を使用するには、クライアントを`--comments`オプション（例： `mysql -h 127.0.0.1 -P 4000 -uroot --comments` ）で起動してください。

## スマート選択、エンジン分離、手動ヒントの関係 {#the-relationship-of-smart-selection-engine-isolation-and-manual-hint}

上記の 3 つのTiFlashレプリカの読み取り方法では、エンジン分離によって、使用可能なエンジンのレプリカの全体的な範囲が指定されます。この範囲内で、手動ヒントによって、よりきめ細かなステートメント レベルおよびテーブル レベルのエンジン選択が提供されます。最後に、CBO が決定を下し、指定されたエンジン リスト内のコスト見積もりに基づいてエンジンのレプリカを選択します。

> **注記：**
>
> -   v4.0.3 より前では、読み取り専用でない SQL ステートメント (たとえば、 `INSERT INTO ... SELECT` 、 `SELECT ... FOR UPDATE` 、 `UPDATE ...` 、 `DELETE ...` ) でTiFlashレプリカから読み取る動作は未定義です。
> -   v4.0.3 から v6.2.0 までのバージョンでは、TiDB はデータの正確性を保証するために、非読み取り専用 SQL 文のTiFlashレプリカを内部的に無視します。つまり、 [スマートな選択](#smart-selection)場合、TiDB はTiFlash以外のレプリカを自動的に選択します。 [エンジン分離](#engine-isolation) （ TiFlashレプリカ**のみを**指定）の場合、TiDB はエラーを報告します。 [手動ヒント](#manual-hint)の場合、TiDB はヒントを無視します。
> -   バージョン v6.3.0 から v7.0.0 では、 TiFlashレプリカが有効になっている場合、 [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)変数を使用して、TiDB が非読み取り専用 SQL ステートメントにTiFlashレプリカを使用するかどうかを制御できます。
> -   v7.1.0 以降、 TiFlashレプリカが有効になっていて、現在のセッションの[SQLモード](/sql-mode.md)厳密でない場合 (つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`または`STRICT_ALL_TABLES`含まれていない場合)、TiDB はコスト見積もりに基づいて、非読み取り専用 SQL ステートメントにTiFlashレプリカを使用するかどうかを自動的に決定します。
