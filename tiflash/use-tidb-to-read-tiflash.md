---
title: Use TiDB to Read TiFlash Replicas
summary: Learn how to use TiDB to read TiFlash replicas.
---

# TiDB を使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

このドキュメントでは、TiDB を使用してTiFlashレプリカを読み取る方法を紹介します。

TiDB には、 TiFlashレプリカを読み取る 3 つの方法が用意されています。エンジン設定を行わずにTiFlashレプリカを追加した場合、デフォルトで CBO (コストベースの最適化) モードが使用されます。

## 賢い選択 {#smart-selection}

TiFlashレプリカを含むテーブルの場合、TiDB オプティマイザーはコスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。 `desc`または`explain analyze`ステートメントを使用して、 TiFlashレプリカが選択されているかどうかを確認できます。例えば：

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

`cop[tiflash]` 、タスクが処理のためにTiFlashに送信されることを意味します。 TiFlashレプリカを選択していない場合は、 `analyze table`ステートメントを使用して統計の更新を試み、 `explain analyze`ステートメントを使用して結果を確認します。

テーブルにTiFlashレプリカが 1 つしかなく、関連ノードがサービスを提供できない場合、CBO モードでのクエリは繰り返し再試行されることに注意してください。この状況では、エンジンを指定するか、手動ヒントを使用して TiKV レプリカからデータを読み取る必要があります。

## エンジンの隔離 {#engine-isolation}

エンジンの分離では、対応する変数を構成することで、すべてのクエリが指定されたエンジンのレプリカを使用するように指定します。オプションのエンジンは、「tikv」、「tidb」（一部の TiDB システム テーブルを保存し、ユーザーが積極的に使用できない TiDB の内部メモリテーブル領域を示します）、および「tiflash」です。

<CustomContent platform="tidb">

次の 2 つの構成レベルでエンジンを指定できます。

-   TiDB インスタンス レベル、つまり INSTANCE レベル。 TiDB 構成ファイルに次の構成項目を追加します。

        [isolation-read]
        engines = ["tikv", "tidb", "tiflash"]

    **INSTANCE レベルのデフォルト構成は`[&quot;tikv&quot;, &quot;tidb&quot;, &quot;tiflash&quot;]`です。**

-   セッションレベル。次のステートメントを使用して構成します。

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    または

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    SESSION レベルのデフォルト構成は、TiDB INSTANCE レベルの構成を継承します。

最終的なエンジン設定はセッション レベルの設定です。つまり、セッション レベルの設定はインスタンス レベルの設定をオーバーライドします。たとえば、INSTANCE レベルで「tikv」を設定し、SESSION レベルで「tiflash」を設定した場合、 TiFlashレプリカが読み取られます。最終的なエンジン構成が「tikv」と「tiflash」の場合、TiKV とTiFlash のレプリカが両方とも読み取られ、オプティマイザーは実行するより適切なエンジンを自動的に選択します。

> **注記：**
>
> [TiDB ダッシュボード](/dashboard/dashboard-intro.md)およびその他のコンポーネントは、TiDBメモリテーブル領域に格納されているいくつかのシステム テーブルを読み取る必要があるため、常に「tidb」エンジンをインスタンス レベルのエンジン構成に追加することをお勧めします。

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

## 手動ヒント {#manual-hint}

手動ヒントでは、エンジン分離を満たすことを前提として、TiDB が特定のテーブルに指定されたレプリカを使用するように強制できます。手動ヒントの使用例を次に示します。

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

クエリ ステートメントでテーブルに別名を設定する場合、ヒントを有効にするために、ヒントを含むステートメントで別名を使用する必要があります。例えば：

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上記のステートメントで、 `tiflash[]`オプティマイザにTiFlashレプリカを読み取るように指示します。 `tikv[]`使用して、必要に応じてオプティマイザーに TiKV レプリカを読み取るように指示することもできます。ヒント構文の詳細については、 [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を参照してください。

ヒントで指定されたテーブルに指定されたエンジンのレプリカがない場合、ヒントは無視され、警告が報告されます。また、ヒントはエンジン隔離を前提としてのみ有効となります。ヒントで指定されたエンジンがエンジン分離リストにない場合も、ヒントは無視され、警告が報告されます。

> **注記：**
>
> 5.7.7 以前のバージョンの MySQL クライアントは、デフォルトでオプティマイザー ヒントをクリアします。これらの初期バージョンでヒント構文を使用するには、 `--comments`オプション (たとえば`mysql -h 127.0.0.1 -P 4000 -uroot --comments`を指定してクライアントを起動します。

## スマート選択、エンジン分離、および手動ヒントの関係 {#the-relationship-of-smart-selection-engine-isolation-and-manual-hint}

TiFlashレプリカを読み取る上記の 3 つの方法では、エンジンの分離により、利用可能なエンジンのレプリカの全体範囲が指定されます。この範囲内では、手動ヒントにより、より詳細なステートメント レベルおよびテーブル レベルのエンジン選択が提供されます。最後に、CBO が決定を下し、指定されたエンジン リスト内のコスト見積もりに基づいてエンジンのレプリカを選択します。

> **注記：**
>
> v4.0.3 より前では、読み取り専用以外の SQL ステートメント (たとえば、 `INSERT INTO ... SELECT` 、 `SELECT ... FOR UPDATE` 、 `UPDATE ...` 、 `DELETE ...` ) でTiFlashレプリカから読み取る動作は未定義です。 v4.0.3 以降のバージョンでは、データの正確性を保証するために、TiDB は内部的に読み取り専用以外の SQL ステートメントのTiFlashレプリカを無視します。つまり、 [賢い選択](#smart-selection)場合、TiDB は非TiFlashレプリカを自動的に選択します。 TiFlashレプリカ**のみ**を指定する[エンジンの隔離](#engine-isolation)の場合、TiDB はエラーを報告します。 [手動ヒント](#manual-hint)の場合、TiDB はヒントを無視します。
