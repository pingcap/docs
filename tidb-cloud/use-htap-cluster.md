---
title: Use an HTAP Cluster
summary: TiDB Cloudで HTAP クラスターを使用する方法を学習します。
---

# HTAPクラスタを使用する {#use-an-htap-cluster}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)ハイブリッドトランザクション／分析処理を意味します。TiDB TiDB Cloudの HTAP クラスターは、トランザクション処理用に設計された行ベースのstorageエンジン[TiKV](https://tikv.org)と、分析処理用に設計された列指向storage[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)で構成されています。アプリケーションデータはまず TiKV に保存され、その後Raftコンセンサスアルゴリズムを介してTiFlashに複製されます。つまり、行ストアから列指向ストアへのリアルタイムレプリケーションが実現されます。

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つまたは複数のTiFlashノードを指定するだけで、HTAP クラスターを簡単に作成できます。クラスター作成時にTiFlashノード数を指定していない場合、またはTiFlashノードを追加したい場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

> **注記：**
>
> TiFlashは、 TiDB Cloud StarterおよびTiDB Cloud Essentialクラスタでは常に有効になっています。無効にすることはできません。

TiKVデータはデフォルトではTiFlashに複製されません。次のSQL文を使用して、 TiFlashに複製するテーブルを選択できます。

```sql
ALTER TABLE table_name SET TIFLASH REPLICA 1;
```

レプリカ数はTiFlashノード数以下にする必要があります。レプリカ数を`0`に設定すると、 TiFlash内のレプリカが削除されます。

レプリケーションの進行状況を確認するには、次のコマンドを使用します。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

## TiDBを使用してTiFlashレプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

データがTiFlashに複製された後、次の 3 つの方法のいずれかを使用してTiFlashレプリカを読み取り、分析コンピューティングを高速化できます。

### スマートな選択 {#smart-selection}

TiFlashレプリカを持つテーブルの場合、TiDBオプティマイザーはコスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。例：

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

`cop[tiflash]` 、タスクが処理のためにTiFlashに送信されることを意味します。クエリでTiFlashレプリカが選択されていない場合は、 `analyze table`のステートメントを使用して統計情報を更新し、 `explain analyze`ステートメントを使用して結果を確認してください。

### エンジン分離 {#engine-isolation}

エンジン分離とは、 `tidb_isolation_read_engines`変数を設定することで、すべてのクエリが指定されたエンジンのレプリカを使用するように指定することです。オプションのエンジンは、「tikv」、「tidb」（TiDBの内部メモリテーブル領域を示し、一部のTiDBシステムテーブルが格納されており、ユーザーが積極的に使用することはできません）、および「tiflash」です。

```sql
set @@session.tidb_isolation_read_engines = "engine list separated by commas";
```

### 手動ヒント {#manual-hint}

手動ヒントを使用すると、エンジン分離が満たされていることを前提に、TiDB が特定のテーブルに対して指定したレプリカを使用するように強制できます。手動ヒントの使用例を以下に示します。

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

TiFlashの詳細については、ドキュメント[ここ](https://docs.pingcap.com/tidb/stable/tiflash-overview/)を参照してください。
