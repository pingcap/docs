---
title: Use an HTAP Cluster
summary: Learn how to use HTAP cluster in TiDB Cloud.
---

# HTAPクラスターを使用する {#use-an-htap-cluster}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)は、ハイブリッドトランザクション/分析処理を意味します。 TiDB CloudのHTAPクラスタは、トランザクション処理用に設計された行ベースのストレージエンジンである[TiKV](https://tikv.org)と、分析処理用に設計された列型ストレージである[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)<sup>ベータ</sup>で構成されています。アプリケーションデータは最初にTiKVに保存され、次にRaftコンセンサスアルゴリズムを介してTiFlash<sup>ベータ</sup>に複製されます。つまり、行ストアから列ストアへのリアルタイムレプリケーションです。

TiDB Cloudでは、HTAPワークロードに応じて1つ以上のTiFlash<sup>ベータ</sup>ノードを指定することで、HTAPクラスタを簡単に作成できます。クラスタの作成時にTiFlash<sup>ベータ</sup>ノード数が指定されていない場合、またはTiFlash<sup>ベータ</sup>ノードをさらに追加する場合は、ノード数を[クラスタのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

> **ノート：**
>
> 開発者層クラスタには、デフォルトで1つのTiFlash<sup>ベータ</sup>ノードがあり、その数を変更することはできません。

デフォルトでは、TiKVデータはTiFlash<sup>ベータ</sup>に複製されません。次のSQLステートメントを使用して、TiFlash<sup>ベータ</sup>に複製するテーブルを選択できます。

{{< copyable "" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA 1;
```

レプリカ数は、TiFlash<sup>ベータ</sup>ノードの数よりも少なくする必要があります。レプリカの数を`0`に設定すると、TiFlash<sup>ベータ版</sup>のレプリカが削除されます。

レプリケーションの進行状況を確認するには、次のコマンドを使用します。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

## TiDBを使用してTiFlash<sup>ベータ</sup>レプリカを読み取る {#use-tidb-to-read-tiflash-sup-beta-sup-replicas}

データがTiFlash<sup>ベータ</sup>に複製された後、次の3つの方法のいずれかを使用してTiFlash<sup>ベータ</sup>レプリカを読み取り、分析コンピューティングを高速化できます。

### スマートセレクション {#smart-selection}

TiFlash<sup>ベータ</sup>レプリカを含むテーブルの場合、TiDBオプティマイザは、コスト見積もりに基づいてTiFlash<sup>ベータ</sup>レプリカを使用するかどうかを自動的に決定します。例えば：

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

`cop[tiflash]`は、タスクが処理のためにTiFlash<sup>ベータ</sup>に送信されることを意味します。クエリでTiFlash<sup>ベータ</sup>レプリカが選択されていない場合は、 `analyze table`ステートメントを使用して統計を更新してから、 `explain analyze`ステートメントを使用して結果を確認してください。

### エンジンの分離 {#engine-isolation}

エンジンの分離とは、 `tidb_isolation_read_engines`の変数を構成することにより、すべてのクエリが指定されたエンジンのレプリカを使用するように指定することです。オプションのエンジンは、「tikv」、「tidb」（一部のTiDBシステムテーブルを格納し、ユーザーがアクティブに使用できないTiDBの内部メモリテーブル領域を示します）、および「tiflash」です。

{{< copyable "" >}}

```sql
set @@session.tidb_isolation_read_engines = "engine list separated by commas";
```

### 手動ヒント {#manual-hint}

手動のヒントにより、TiDBは、エンジンの分離を満たすことを前提として、1つ以上の特定のテーブルに指定されたレプリカを使用するように強制できます。手動ヒントの使用例を次に示します。

{{< copyable "" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

TiFlash<sup>ベータ</sup>の詳細については、ドキュメント[ここ](https://docs.pingcap.com/tidb/stable/tiflash-overview/)を参照してください。
