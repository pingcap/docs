---
title: Use TiDB to Read TiFlash Replicas
summary: Learn how to use TiDB to read TiFlash replicas.
---

# TiDBを使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

このドキュメントでは、TiDBを使用してTiFlashレプリカを読み取る方法を紹介します。

TiDBは、TiFlashレプリカを読み取る3つの方法を提供します。エンジン構成なしでTiFlashレプリカを追加した場合、デフォルトでCBO（コストベースの最適化）モードが使用されます。

## スマートセレクション {#smart-selection}

TiFlashレプリカを含むテーブルの場合、TiDBオプティマイザは、コスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。 `desc`または`explain analyze`ステートメントを使用して、TiFlashレプリカが選択されているかどうかを確認できます。例えば：

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
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | time:43ms, loops:1                                                   | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]`は、タスクが処理のためにTiFlashに送信されることを意味します。 TiFlashレプリカを選択していない場合は、 `analyze table`ステートメントを使用して統計を更新し、 `explain analyze`ステートメントを使用して結果を確認できます。

テーブルにTiFlashレプリカが1つしかなく、関連ノードがサービスを提供できない場合、CBOモードのクエリは繰り返し再試行することに注意してください。この状況では、エンジンを指定するか、手動ヒントを使用してTiKVレプリカからデータを読み取る必要があります。

## エンジンの分離 {#engine-isolation}

エンジンの分離とは、対応する変数を構成することにより、すべてのクエリが指定されたエンジンのレプリカを使用するように指定することです。オプションのエンジンは、「tikv」、「tidb」（一部のTiDBシステムテーブルを格納し、ユーザーがアクティブに使用できないTiDBの内部メモリテーブル領域を示します）、および「tiflash」で、次の2つの構成レベルがあります。

-   TiDBインスタンスレベル、つまりINSTANCEレベル。 TiDB構成ファイルに次の構成項目を追加します。

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **INSTANCEレベルのデフォルト設定は`[&quot;tikv&quot;, &quot;tidb&quot;, &quot;tiflash&quot;]`です。**

-   SESSIONレベル。次のステートメントを使用して構成します。

    {{< copyable "" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    また

    {{< copyable "" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    SESSIONレベルのデフォルト構成は、TiDBINSTANCEレベルの構成を継承します。

最終的なエンジン構成はセッションレベルの構成です。つまり、セッションレベルの構成はインスタンスレベルの構成をオーバーライドします。たとえば、INSTANCEレベルで「tikv」を構成し、SESSIONレベルで「tiflash」を構成した場合、TiFlashレプリカが読み取られます。最終的なエンジン構成が「tikv」と「tiflash」の場合、TiKVとTiFlashのレプリカが両方とも読み取られ、オプティマイザーは実行するのに適したエンジンを自動的に選択します。

> **ノート：**
>
> [TiDBダッシュボード](/dashboard/dashboard-intro.md)およびその他のコンポーネントは、TiDBメモリテーブル領域に格納されている一部のシステムテーブルを読み取る必要があるため、常に「tidb」エンジンをインスタンスレベルのエンジン構成に追加することをお勧めします。

クエリされたテーブルに指定されたエンジンのレプリカがない場合（たとえば、エンジンが「tiflash」として構成されているが、テーブルにTiFlashレプリカがない場合）、クエリはエラーを返します。

## 手動ヒント {#manual-hint}

手動のヒントにより、TiDBは、エンジンの分離を満たすことを前提として、特定のテーブルに指定されたレプリカを使用するように強制できます。手動ヒントの使用例を次に示します。

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

クエリステートメントでテーブルにエイリアスを設定する場合は、ヒントを有効にするためのヒントを含むエイリアスをステートメントで使用する必要があります。例えば：

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上記のステートメントで、 `tiflash[]`はオプティマイザにTiFlashレプリカを読み取るように促します。 `tikv[]`を使用して、必要に応じてオプティマイザにTiKVレプリカを読み取るように求めることもできます。ヒント構文の詳細については、 [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を参照してください。

ヒントで指定されたテーブルに指定されたエンジンのレプリカがない場合、ヒントは無視され、警告が報告されます。さらに、ヒントはエンジン分離の前提でのみ有効になります。ヒントで指定されたエンジンがエンジン分離リストにない場合、ヒントも無視され、警告が報告されます。

> **ノート：**
>
> 5.7.7以前のバージョンのMySQLクライアントは、デフォルトでオプティマイザヒントをクリアします。これらの初期バージョンでヒント構文を使用するには、 `--comments`オプション（たとえば、 `mysql -h 127.0.0.1 -P 4000 -uroot --comments` ）でクライアントを起動します。

## スマートセレクション、エンジン分離、および手動ヒントの関係 {#the-relationship-of-smart-selection-engine-isolation-and-manual-hint}

上記の3つのTiFlashレプリカの読み取り方法では、エンジン分離により、エンジンの使用可能なレプリカの全体的な範囲が指定されます。この範囲内で、手動ヒントは、よりきめ細かいステートメントレベルおよびテーブルレベルのエンジン選択を提供します。最後に、CBOが決定を下し、指定されたエンジンリスト内のコスト見積もりに基づいてエンジンのレプリカを選択します。

> **ノート：**
>
> `UPDATE ...`より前では、非読み取り専用SQLステートメント（たとえば、 `INSERT INTO ... SELECT` ）での`SELECT ... FOR UPDATE`レプリカからの読み取りの`DELETE ...`は定義されていません。 v4.0.3以降のバージョンでは、内部的にTiDBは非読み取り専用SQLステートメントのTiFlashレプリカを無視して、データの正確性を保証します。つまり、 [スマートセレクション](#smart-selection)の場合、TiDBは非TiFlashレプリカを自動的に選択します。 TiFlashレプリカ**のみ**を指定する[エンジンの分離](#engine-isolation)の場合、TiDBはエラーを報告します。 [手動ヒント](#manual-hint)の場合、TiDBはヒントを無視します。
