---
title: Prerequisites for using TiDB Lightning
summary: Learn prerequisites for running TiDB Lightning.
---

# TiDBLightningを使用するための前提条件 {#prerequisites-for-using-tidb-lightning}

TiDB Lightningを使用する前に、環境が要件を満たしているかどうかを確認する必要があります。これにより、インポート中のエラーが減り、インポートが確実に成功します。

## ダウンストリーム特権要件 {#downstream-privilege-requirements}

インポートモードと有効な機能に基づいて、ダウンストリームデータベースユーザーに異なる権限を付与する必要があります。次の表に参照を示します。

<table border="1"><tr><td></td><td>特徴</td><td>範囲</td><td>必要な特権</td><td>備考</td></tr><tr><td rowspan="2">必須</td><td rowspan="2">基本機能</td><td>ターゲットテーブル</td><td>CREATE、SELECT、INSERT、UPDATE、DELETE、DROP、ALTER</td><td> DROPは、tidb-lightning-ctlがcheckpoint-destroy-allコマンドを実行する場合にのみ必要です。</td></tr><tr><td>ターゲットデータベース</td><td>作成</td><td></td></tr><tr><td rowspan="4">必須</td><td>tidb-バックエンド</td><td>information_schema.columns</td><td>選択する</td><td></td></tr><tr><td  rowspan="3">ローカルバックエンド</td><td>mysql.tidb</td><td>選択する</td><td></td></tr><tr><td>-</td><td>素晴らしい</td><td></td></tr><tr><td>-</td><td> RESTRICTED_VARIABLES_ADMIN、RESTRICTED_TABLES_ADMIN</td><td>ターゲットTiDBがSEMを有効にする場合に必要</td></tr><tr><td>おすすめされた</td><td>競合の検出、最大エラー</td><td>lightning.task-info-schema-name用に構成されたスキーマ</td><td>SELECT、INSERT、UPDATE、DELETE、CREATE、DROP</td><td>不要な場合は、値を「」に設定する必要があります</td></tr><tr><td>オプション</td><td>並列インポート</td><td>lightning.meta-schema-name用に構成されたスキーマ</td><td>SELECT、INSERT、UPDATE、DELETE、CREATE、DROP</td><td>不要な場合は、値を「」に設定する必要があります</td></tr><tr><td>オプション</td><td>checkpoint.driver =“ mysql”</td><td> checkpoint.schema設定</td><td>SELECT、INSERT、UPDATE、DELETE、CREATE、DROP</td><td>チェックポイント情報がファイルではなくデータベースに保存されている場合に必要</td></tr></table>

## ダウンストリームストレージスペースの要件 {#downstream-storage-space-requirements}

ターゲットTiKVクラスタには、インポートされたデータを格納するのに十分なディスク容量が必要です。 [標準のハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲットTiKVクラスタのストレージスペースは**、データソースのサイズxレプリカの数x2**よりも大きくする必要があります。たとえば、クラスタがデフォルトで3つのレプリカを使用する場合、ターゲットTiKVクラスタには、データソースのサイズの6倍を超えるストレージスペースが必要です。数式にはx2があります。理由は次のとおりです。

-   インデックスには余分なスペースが必要になる場合があります。
-   RocksDBにはスペース増幅効果があります。

MySQLからDumplingによってエクスポートされた正確なデータ量を計算することは困難です。ただし、次のSQLステートメントを使用してinformation_schema.tablesテーブルのデータ長フィールドを要約することにより、データ量を見積もることができます。

MiBですべてのスキーマのサイズを計算します。 ${schema_name}をスキーマ名に置き換えます。

```sql
select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_schema;
```

最大のテーブルのサイズをMiBで計算します。 ${schema_name}をスキーマ名に置き換えます。

{{< copyable "" >}}

```sql
select table_name,table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_name,table_schema order by sum  desc limit 5;
```

## リソース要件 {#resource-requirements}

**オペレーティングシステム**：このドキュメントの例では、新しいCentOS7インスタンスを使用しています。仮想マシンは、ローカルホストまたはクラウドのいずれかにデプロイできます。 TiDB Lightningはデフォルトで必要なだけのCPUリソースを消費するため、専用サーバーにデプロイすることをお勧めします。これが不可能な場合は、他のTiDBコンポーネント（tikv-serverなど）と一緒に単一のサーバーにデプロイしてから、TiDBLightningからのCPU使用率を制限するように`region-concurrency`を構成できます。通常、サイズは論理CPUの75％に設定できます。

**メモリとCPU** ：

TiDB Lightningが消費するCPUとメモリは、バックエンドモードによって異なります。使用するバックエンドに基づいて最適なインポートパフォーマンスをサポートする環境でTiDBLightningを実行します。

-   ローカルバックエンド：TiDB lightningは、このモードで多くのCPUとメモリを消費します。 32コアを超えるCPUと64GiBを超えるメモリを割り当てることをお勧めします。

> **注**：
>
> インポートするデータが大きい場合、1回の並列インポートで約2GiBのメモリを消費する可能性があります。この場合、合計メモリ使用量は`region-concurrency` x2GiBになります。 `region-concurrency`は論理CPUの数と同じです。メモリサイズ（GiB）がCPUの2倍未満であるか、インポート中にOOMが発生する場合は、 `region-concurrency`を減らしてOOMをアドレス指定できます。

-   TiDBバックエンド：このモードでは、パフォーマンスのボトルネックはTiDBにあります。 TiDBLightningには4コアCPUと8GiBメモリを割り当てることをお勧めします。 TiDBクラスタがインポートで書き込みしきい値に達しない場合は、 `region-concurrency`を増やすことができます。
-   インポーターバックエンド：このモードでは、リソース消費量はローカルバックエンドの場合とほぼ同じです。インポーターバックエンドは推奨されません。特に要件がない場合は、ローカルバックエンドを使用することをお勧めします。

**記憶域スペース**： `sorted-kv-dir`構成項目は、ソートされたKey-Valueファイルの一時記憶域ディレクトリーを指定します。ディレクトリは空である必要があり、ストレージスペースはインポートするデータセットのサイズよりも大きい必要があります。インポートのパフォーマンスを向上させるには、 `data-source-dir`とは異なるディレクトリを使用し、そのディレクトリにフラッシュストレージと排他的I/Oを使用することをお勧めします。
