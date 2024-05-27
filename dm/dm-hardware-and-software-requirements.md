---
title: Software and Hardware Requirements for TiDB Data Migration
summary: DM クラスターのソフトウェアおよびハードウェア要件について学習します。
---

# TiDB データ移行のソフトウェアおよびハードウェア要件 {#software-and-hardware-requirements-for-tidb-data-migration}

TiDB データ移行 (DM) は、主流の Linux オペレーティング システムをサポートしています。特定のバージョン要件については、次の表を参照してください。

| Linux OS              |  バージョン  |
| :-------------------- | :-----: |
| レッドハットエンタープライズリナックス   |  7.3以降  |
| セントOS                 |  7.3以降  |
| Oracle エンタープライズ Linux |  7.3以降  |
| Ubuntu 16.04 リリース     | 16.04以降 |

DM は、Intelアーキテクチャサーバーおよび主流の仮想化環境に導入して実行できます。

## 推奨サーバー要件 {#recommended-server-requirements}

DM は、64 ビットの汎用ハードウェアサーバープラットフォーム (Intel x86-64アーキテクチャ) に導入して実行できます。開発、テスト、および本番環境で使用されるサーバーの場合、このセクションでは推奨されるハードウェア構成を示します (これらには、オペレーティング システムによって使用されるリソースは含まれません)。

### 開発およびテスト環境 {#development-and-test-environments}

| 成分     | CPU   | メモリ    | ローカルストレージ                       | 通信網            | インスタンス数（最小要件）         |
| ------ | ----- | ------ | ------------------------------- | -------------- | --------------------- |
| DMマスター | 4コア以上 | 8GB以上  | SAS、200 GB以上                    | ギガビットネットワークカード | 1                     |
| DMワーカー | 8コア以上 | 16GB以上 | SAS、200 GB以上（移行されたデータのサイズより大きい） | ギガビットネットワークカード | アップストリームMySQLインスタンスの数 |

> **注記：**
>
> -   テスト環境では、機能検証に使用する DM-master と DM-worker を同じサーバー上に配置できます。
> -   パフォーマンス テスト結果の精度に影響が及ばないように、低パフォーマンスのstorageおよびネットワーク ハードウェア構成の使用はお**勧めしません**。
> -   機能の検証のみが必要な場合は、単一のマシンに DM マスターをデプロイできます。デプロイする DM ワーカーの数は、アップストリーム MySQL インスタンスの数以上である必要があります。高可用性を確保するには、より多くの DM ワーカーをデプロイすることをお勧めします。
> -   DM-worker はフェーズ`dump`と`load`で全データを保存します。したがって、DM-worker のディスク容量は、移行するデータの合計量よりも大きくする必要があります。移行タスクでリレー ログが有効になっている場合、DM-worker にはアップストリームbinlogデータを保存するための追加のディスク容量が必要です。

### 本番環境 {#production-environment}

| 成分     | CPU    | メモリ    | ハードディスクタイプ                   | 通信網              | インスタンス数（最小要件）               |
| ------ | ------ | ------ | ---------------------------- | ---------------- | --------------------------- |
| DMマスター | 4コア以上  | 8GB以上  | SAS、200 GB以上                 | ギガビットネットワークカード   | 3                           |
| DMワーカー | 16コア以上 | 32GB以上 | SSD、200 GB以上（移行データのサイズより大きい） | 10ギガビットネットワークカード | アップストリームのMySQLインスタンスの数より大きい |
| モニター   | 8コア以上  | 16GB以上 | SAS、200 GB以上                 | ギガビットネットワークカード   | 1                           |

> **注記：**
>
> -   本番環境では、DM-master と DM-worker を同じサーバーにデプロイして実行することは推奨されません。DM-worker がディスクにデータを書き込むと、DM-master の高可用性コンポーネントによるディスクの使用が妨げられる可能性があるためです。
> -   パフォーマンスの問題が発生した場合は、 [DMのコンフィグレーションを最適化する](/dm/dm-tune-configuration.md)ドキュメントに従ってタスク構成ファイルを変更することをお勧めします。構成ファイルを調整してもパフォーマンスが効果的に最適化されない場合は、サーバーのハードウェアをアップグレードしてみてください。

## 下流のstorageスペース要件 {#downstream-storage-space-requirements}

ターゲット TiKV クラスターには、インポートされたデータを保存するのに十分なディスク容量が必要です。 [標準ハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲット TiKV クラスターのstorage容量**は、データ ソースのサイズ x レプリカの数 x 2**よりも大きくする必要があります。たとえば、クラスターがデフォルトで 3 つのレプリカを使用する場合、ターゲット TiKV クラスターには、データ ソースのサイズの 6 倍よりも大きいstorage容量が必要です。次の理由により、式には`x 2`含まれます。

-   インデックスは余分なスペースを占める可能性があります。
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
