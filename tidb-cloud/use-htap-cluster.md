---
title: Use an HTAP Cluster
summary: Learn how to use HTAP cluster in TiDB Cloud.
---

# HTAPクラスタを使用する {#use-an-htap-cluster}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)はハイブリッド トランザクション/分析処理を意味します。 TiDB Cloudの HTAP クラスターは、トランザクション処理用に設計された行ベースのストレージ エンジン[TiKV](https://tikv.org)と、分析処理用に設計された列型ストレージ エンジン[ティフラッシュ](https://docs.pingcap.com/tidb/stable/tiflash-overview)で構成されます。アプリケーション データはまず TiKV に保存され、次にRaftコンセンサス アルゴリズムを介して TiFlash に複製されます。つまり、行ストアから列ストアへのリアルタイム レプリケーションです。

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つ以上の TiFlash ノードを指定することで、HTAP クラスターを簡単に作成できます。クラスターの作成時に TiFlash ノード数が指定されていない場合、またはさらに TiFlash ノードを追加する場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

> **ノート：**
>
> サーバーレス層クラスターでは、TiFlash は常に有効になっています。無効にすることはできません。

デフォルトでは、TiKV データは TiFlash に複製されません。次の SQL ステートメントを使用して、TiFlash にレプリケートするテーブルを選択できます。

{{< copyable "" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA 1;
```

レプリカ カウントの数は、TiFlash ノードの数を超えてはなりません。レプリカの数を`0`に設定すると、TiFlash 内のレプリカが削除されます。

レプリケーションの進行状況を確認するには、次のコマンドを使用します。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

## TiDB を使用して TiFlash レプリカを読み取る {#use-tidb-to-read-tiflash-replicas}

データが TiFlash にレプリケートされた後、次の 3 つの方法のいずれかを使用して TiFlash レプリカを読み取り、分析コンピューティングを高速化できます。

### スマートセレクション {#smart-selection}

TiFlash レプリカを含むテーブルの場合、TiDB オプティマイザは、コストの見積もりに基づいて TiFlash レプリカを使用するかどうかを自動的に決定します。例えば：

{{< copyable "" >}}

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

`cop[tiflash]`は、タスクが処理のために TiFlash に送信されることを意味します。クエリで TiFlash レプリカが選択されていない場合は、 `analyze table`ステートメントを使用して統計を更新してから、 `explain analyze`ステートメントを使用して結果を確認してください。

### エンジンの分離 {#engine-isolation}

エンジンの分離は、 `tidb_isolation_read_engines`変数を構成することによって、すべてのクエリが指定されたエンジンのレプリカを使用することを指定することです。オプションのエンジンは、「tikv」、「tidb」(一部の TiDB システム テーブルを格納し、ユーザーが積極的に使用できない TiDB の内部メモリ テーブル領域を示します)、および「tiflash」です。

{{< copyable "" >}}

```sql
set @@session.tidb_isolation_read_engines = "engine list separated by commas";
```

### 手動ヒント {#manual-hint}

手動ヒントは、TiDB が、エンジンの分離を満たすという前提で、1 つ以上の特定のテーブルに対して指定されたレプリカを使用するように強制することができます。手動ヒントの使用例を次に示します。

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

TiFlash の詳細については、ドキュメント[ここ](https://docs.pingcap.com/tidb/stable/tiflash-overview/)を参照してください。
