---
title: Software and Hardware Requirements for TiDB Data Migration
summary: DM クラスターのソフトウェアおよびハードウェア要件について説明します。
---

# TiDBデータ移行のソフトウェアおよびハードウェア要件 {#software-and-hardware-requirements-for-tidb-data-migration}

TiDB Data Migration (DM) は、主要な Linux オペレーティングシステムをサポートしています。具体的なバージョン要件については、次の表をご覧ください。

| Linux OS              |  バージョン  |
| :-------------------- | :-----: |
| レッドハットエンタープライズリナックス   |  7.3以降  |
| セントOS                 |  7.3以降  |
| Oracle エンタープライズ Linux |  7.3以降  |
| Ubuntu LTS            | 16.04以降 |

DM は、Intelアーキテクチャサーバーおよび主流の仮想化環境に導入および実行できます。

## 推奨サーバー要件 {#recommended-server-requirements}

DMは、64ビット汎用ハードウェアサーバープラットフォーム（Intel x86-64アーキテクチャ）上で導入および実行できます。開発環境、テスト環境、および本番環境で使用されるサーバーについて、このセクションでは推奨されるハードウェア構成を示します（これらにはオペレーティングシステムが使用するリソースは含まれません）。

### 開発およびテスト環境 {#development-and-test-environments}

| 成分     | CPU   | メモリ    | ローカルストレージ                    | ネットワーク         | インスタンス数（最小要件）         |
| ------ | ----- | ------ | ---------------------------- | -------------- | --------------------- |
| DMマスター | 4コア以上 | 8GB以上  | SAS、200 GB以上                 | ギガビットネットワークカード | 1                     |
| DMワーカー | 8コア以上 | 16GB以上 | SAS、200 GB以上（移行データのサイズより大きい） | ギガビットネットワークカード | アップストリームMySQLインスタンスの数 |

> **注記：**
>
> -   テスト環境では、機能検証に使用する DM-master と DM-worker を同じサーバー上に配置できます。
> -   パフォーマンス テスト結果の精度を損なわないようにするために、低パフォーマンスのstorageおよびネットワーク ハードウェア構成を使用することは**お勧めしません**。
> -   機能の検証のみが必要な場合は、DMマスターを1台のマシンにデプロイできます。デプロイするDMワーカーの数は、上流のMySQLインスタンスの数以上である必要があります。高可用性を確保するには、より多くのDMワーカーをデプロイすることをお勧めします。
> -   DM-workerはフェーズ`dump`とフェーズ`load`で全データを保存します。そのため、DM-workerのディスク容量は、移行するデータの総量よりも大きくする必要があります。移行タスクでリレーログが有効になっている場合、DM-workerは上流のbinlogデータを保存するために追加のディスク容量を必要とします。

### 生産環境 {#production-environment}

| 成分     | CPU    | メモリ     | ハードディスクの種類                   | ネットワーク           | インスタンス数（最小要件）               |
| ------ | ------ | ------- | ---------------------------- | ---------------- | --------------------------- |
| DMマスター | 4コア以上  | 8GB以上   | SAS、200 GB以上                 | ギガビットネットワークカード   | 3                           |
| DMワーカー | 16コア以上 | 32 GB以上 | SSD、200 GB以上（移行データのサイズより大きい） | 10ギガビットネットワークカード | アップストリームのMySQLインスタンスの数より大きい |
| モニター   | 8コア以上  | 16GB以上  | SAS、200 GB以上                 | ギガビットネットワークカード   | 1                           |

> **注記：**
>
> -   本番環境では、DM-master と DM-worker を同じサーバーに導入して実行することは推奨されません。DM-worker がディスクにデータを書き込むと、DM-master の高可用性コンポーネントによるディスクの使用が妨げられる可能性があるためです。
> -   パフォーマンスの問題が発生した場合は、ドキュメント[DMのコンフィグレーションを最適化する](/dm/dm-tune-configuration.md)に従ってタスク設定ファイルを変更することをお勧めします。設定ファイルを調整してもパフォーマンスが効果的に最適化されない場合は、サーバーのハードウェアをアップグレードしてみてください。

## 下流のstorageスペース要件 {#downstream-storage-space-requirements}

ターゲットTiKVクラスターには、インポートしたデータを保存するための十分なディスク容量が必要です。1 に加え[標準的なハードウェア要件](/hardware-and-software-requirements.md) 、ターゲットTiKVクラスターのstorage容量**は、データソースのサイズ × レプリカ数 × 2**よりも大きくなければなりません。例えば、クラスターがデフォルトで3つのレプリカを使用する場合、ターゲットTiKVクラスターには、データソースのサイズの6倍よりも大きなstorage容量が必要です。式に`x 2`含まれているのは、以下の理由からです。

-   インデックスは余分なスペースを占める可能性があります。
-   RocksDB には空間増幅効果があります。

次の SQL ステートメントを使用して`DATA_LENGTH`フィールドを要約すると、データ量を見積もることができます。

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
