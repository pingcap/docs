---
title: Use an HTAP Cluster
summary: Learn how to use HTAP cluster in TiDB Cloud.
---

# HTAPクラスタを使用する {#use-an-htap-cluster}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)ハイブリッド トランザクション/分析処理を意味します。 TiDB Cloudの HTAP クラスターは、トランザクション処理用に設計された行ベースのstorageエンジン[TiKV](https://tikv.org)と、分析処理用に設計されたカラム型storage[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)で構成されます。アプリケーション データは最初に TiKV に保存され、次にRaftコンセンサス アルゴリズムを介してTiFlashにレプリケートされます。つまり、行ストアから列ストアへのリアルタイム レプリケーションです。

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つ以上のTiFlashノードを指定することで、HTAP クラスターを簡単に作成できます。クラスターの作成時にTiFlashノード数が指定されていない場合、またはTiFlashノードをさらに追加したい場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

> **注記：**
>
> TiFlash は、 TiDB サーバーレス クラスターに対して常に有効になっています。無効にすることはできません。

TiKV データは、デフォルトではTiFlashにレプリケートされません。次の SQL ステートメントを使用して、 TiFlashにレプリケートするテーブルを選択できます。

```sql
ALTER TABLE table_name SET TIFLASH REPLICA 1;
```

レプリカの数は、 TiFlashノードの数を超えてはなりません。レプリカの数を`0`に設定することは、 TiFlash内のレプリカを削除することを意味します。

レプリケーションの進行状況を確認するには、次のコマンドを使用します。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

## TiDB を使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

データがTiFlashにレプリケートされた後、次の 3 つの方法のいずれかを使用してTiFlashレプリカを読み取り、分析コンピューティングを高速化できます。

### 賢い選択 {#smart-selection}

TiFlashレプリカを含むテーブルの場合、TiDB オプティマイザーはコスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。例えば：

```sql
explain analyze select count(*) from test.t;
```

```sql
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | time:43ms, loops:1                                                   | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` 、タスクが処理のためにTiFlashに送信されることを意味します。クエリでTiFlashレプリカが選択されていない場合は、 `analyze table`ステートメントを使用して統計を更新し、 `explain analyze`ステートメントを使用して結果を確認してください。

### エンジンの隔離 {#engine-isolation}

エンジンの分離では、変数`tidb_isolation_read_engines`を構成して、すべてのクエリが指定されたエンジンのレプリカを使用するように指定します。オプションのエンジンは、「tikv」、「tidb」（一部の TiDB システム テーブルを保存し、ユーザーが積極的に使用できない TiDB の内部メモリテーブル領域を示します）、および「tiflash」です。

```sql
set @@session.tidb_isolation_read_engines = "engine list separated by commas";
```

### 手動ヒント {#manual-hint}

手動ヒントでは、エンジン分離を満たすことを前提として、TiDB が 1 つ以上の特定のテーブルに対して指定されたレプリカを使用するように強制できます。手動ヒントの使用例を次に示します。

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

TiFlashの詳細については、ドキュメント[ここ](https://docs.pingcap.com/tidb/stable/tiflash-overview/)を参照してください。
