---
title: Software and Hardware Requirements for TiDB Data Migration
summary: Learn the software and hardware requirements for DM cluster.
---

# TiDB データ移行のソフトウェアおよびハードウェア要件 {#software-and-hardware-requirements-for-tidb-data-migration}

TiDB データ マイグレーション (DM) は、主流の Linux オペレーティング システムをサポートします。特定のバージョン要件については、次の表を参照してください。

| Linux OS              |  バージョン  |
| :-------------------- | :-----: |
| レッドハット エンタープライズ リナックス |  7.3以降  |
| CentOS                |  7.3以降  |
| Oracle エンタープライズ Linux |  7.3以降  |
| Ubuntu LTS            | 16.04以降 |

DM は、Intelアーキテクチャのサーバーおよび主流の仮想化環境に導入して実行できます。

## 推奨サーバー要件 {#recommended-server-requirements}

DM は、64 ビットの汎用ハードウェアサーバープラットフォーム (Intel x86-64アーキテクチャ) 上で展開して実行できます。このセクションでは、開発、テスト、本番環境で使用されるサーバーについて、推奨されるハードウェア構成を示します (これらには、オペレーティング システムで使用されるリソースは含まれません)。

### 開発およびテスト環境 {#development-and-test-environments}

| 成分     | CPU   | メモリ    | ローカルストレージ                       | 通信網            | インスタンスの数 (最小要件)    |
| ------ | ----- | ------ | ------------------------------- | -------------- | ------------------ |
| DMマスター | 4コア以上 | 8GB以上  | SAS、200GB以上                     | ギガビットネットワークカード | 1                  |
| DMワーカー | 8コア以上 | 16GB以上 | SAS、200 GB+ (移行されたデータのサイズより大きい) | ギガビットネットワークカード | 上流の MySQL インスタンスの数 |

> **注記：**
>
> -   テスト環境では、機能検証に使用するDM-masterとDM-workerを同一サーバー上に配置できます。
> -   パフォーマンス テスト結果の精度への干渉を防ぐため、低パフォーマンスのstorageおよびネットワーク ハードウェア構成を使用することは**お勧めできません**。
> -   機能のみを検証する必要がある場合は、単一のマシンに DM マスターをデプロイできます。デプロイされる DM ワーカーの数は、上流の MySQL インスタンスの数以上である必要があります。高可用性を確保するには、より多くの DM ワーカーをデプロイすることをお勧めします。
> -   DM-worker は、 `dump`と`load`フェーズで完全なデータを保存します。したがって、DM-worker のディスク容量は、移行するデータの総量よりも大きい必要があります。移行タスクに対してリレー ログが有効になっている場合、DM ワーカーにはアップストリームのbinlogデータを保存するための追加のディスク領域が必要です。

### 本番環境 {#production-environment}

| 成分     | CPU    | メモリ    | ハードディスクの種類                      | 通信網              | インスタンスの数 (最小要件)         |
| ------ | ------ | ------ | ------------------------------- | ---------------- | ----------------------- |
| DMマスター | 4コア以上  | 8GB以上  | SAS、200GB以上                     | ギガビットネットワークカード   | 3                       |
| DMワーカー | 16コア以上 | 32GB以上 | SSD、200 GB+ (移行されたデータのサイズより大きい) | 10ギガビットネットワークカード | 上流の MySQL インスタンスの数より大きい |
| モニター   | 8コア以上  | 16GB以上 | SAS、200GB以上                     | ギガビットネットワークカード   | 1                       |

> **注記：**
>
> -   本番環境では、DM マスターと DM ワーカーを同じサーバーにデプロイして実行することはお勧めできません。DM ワーカーがデータをディスクに書き込むと、DM マスターの高可用性コンポーネントによるディスクの使用が妨げられる可能性があるためです。 。
> -   パフォーマンスの問題が発生した場合は、 [DMのコンフィグレーションを最適化する](/dm/dm-tune-configuration.md)ドキュメントに従ってタスク構成ファイルを変更することをお勧めします。構成ファイルを調整してもパフォーマンスが効果的に最適化されない場合は、サーバーのハードウェアをアップグレードしてみることができます。

## ダウンストリームのstorageスペース要件 {#downstream-storage-space-requirements}

ターゲット TiKV クラスターには、インポートされたデータを保存するのに十分なディスク容量が必要です。 [標準的なハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲット TiKV クラスターのstorage容量は**、データ ソースのサイズ x レプリカの数 x 2**より大きくなければなりません。たとえば、クラスターがデフォルトで 3 つのレプリカを使用する場合、ターゲット TiKV クラスターにはデータ ソースのサイズの 6 倍を超えるstorageスペースが必要です。この式に`x 2`含まれるのは、次の理由からです。

-   インデックスには余分なスペースが必要になる場合があります。
-   RocksDB には空間増幅効果があります。

次の SQL ステートメントを使用して`DATA_LENGTH`フィールドを要約することで、データ量を見積もることができます。

```sql
-- Calculate the size of all schemas
SELECT
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(DATA_LENGTH)) AS 'Data Size',
  FORMAT_BYTES(SUM(INDEX_LENGTH)) 'Index Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_SCHEMA;

-- Calculate the 5 largest tables
SELECT 
  TABLE_NAME,
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(data_length)) AS 'Data Size',
  FORMAT_BYTES(SUM(index_length)) AS 'Index Size',
  FORMAT_BYTES(SUM(data_length+index_length)) AS 'Total Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_NAME,
  TABLE_SCHEMA
ORDER BY
  SUM(DATA_LENGTH+INDEX_LENGTH) DESC
LIMIT
  5;
```
