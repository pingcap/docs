---
title: Software and Hardware Requirements for TiDB Data Migration
summary: Learn the software and hardware requirements for DM cluster.
---

# TiDB データ移行のソフトウェアおよびハードウェア要件 {#software-and-hardware-requirements-for-tidb-data-migration}

TiDB データ移行 (DM) は、主流の Linux オペレーティング システムをサポートしています。特定のバージョン要件については、次の表を参照してください。

| Linux OS              |   バージョン  |
| :-------------------- | :------: |
| レッドハット エンタープライズ リナックス |   7.3以降  |
| CentOS                |   7.3以降  |
| オラクル エンタープライズ Linux   |   7.3以降  |
| Ubuntu LTS            | 16.04 以降 |

DM は、Intelアーキテクチャサーバーおよび主流の仮想化環境に展開して実行できます。

## 推奨されるサーバー要件 {#recommended-server-requirements}

DM は、64 ビットの汎用ハードウェアサーバープラットフォーム (Intel x86-64アーキテクチャ) に展開して実行できます。このセクションでは、開発、テスト、および本番環境で使用されるサーバーについて、推奨されるハードウェア構成を示します (これらには、オペレーティング システムで使用されるリソースは含まれません)。

### 開発およびテスト環境 {#development-and-test-environments}

| 成分     | CPU  | メモリー   | ローカルストレージ                       | 通信網              | インスタンス数 (最小要件)          |
| ------ | ---- | ------ | ------------------------------- | ---------------- | ----------------------- |
| DMマスター | 4コア+ | 8GB以上  | SAS、200GB+                      | ギガビット ネットワーク カード | 1                       |
| DMワーカー | 8コア+ | 16GB以上 | SAS、200 GB+ (移行されたデータのサイズより大きい) | ギガビット ネットワーク カード | アップストリーム MySQL インスタンスの数 |

> **ノート：**
>
> -   テスト環境では、機能検証に使用する DM-master と DM-worker を同じサーバーに配置できます。
> -   パフォーマンス テストの結果の精度が損なわれないようにするために、パフォーマンスの低いstorageおよびネットワーク ハードウェア構成を使用することは**お勧めしません**。
> -   機能のみを確認する必要がある場合は、DM マスターを 1 台のマシンにデプロイできます。デプロイされる DM-worker の数は、上流の MySQL インスタンスの数以上である必要があります。高可用性を確保するには、より多くの DM-worker をデプロイすることをお勧めします。
> -   DM-worker は、 `dump`と`load`フェーズで完全なデータを保存します。したがって、DM-worker のディスク容量は、移行するデータの総量よりも大きくする必要があります。移行タスクでリレー ログが有効になっている場合、DM-worker は上流のbinlogデータを保存するために追加のディスク領域を必要とします。

### 本番環境 {#production-environment}

| 成分     | CPU   | メモリー   | ハードディスクの種類                      | 通信網                 | インスタンス数 (最小要件)               |
| ------ | ----- | ------ | ------------------------------- | ------------------- | ---------------------------- |
| DMマスター | 4コア+  | 8GB以上  | SAS、200GB+                      | ギガビット ネットワーク カード    | 3                            |
| DMワーカー | 16コア+ | 32GB以上 | SSD、200 GB+ (移行されたデータのサイズより大きい) | 10 ギガビット ネットワーク カード | アップストリームの MySQL インスタンスの数より多い |
| モニター   | 8コア+  | 16GB以上 | SAS、200GB+                      | ギガビット ネットワーク カード    | 1                            |

> **ノート：**
>
> -   本番環境では、DM-master と DM-worker を同じサーバーに展開して実行することはお勧めしません。DM-worker がデータをディスクに書き込むと、DM-master の高可用性コンポーネントによるディスクの使用が妨げられる可能性があるためです。 .
> -   パフォーマンスの問題が発生した場合は、 [DM のコンフィグレーションを最適化する](/dm/dm-tune-configuration.md)ドキュメントに従ってタスク構成ファイルを変更することをお勧めします。構成ファイルを調整してもパフォーマンスが効果的に最適化されない場合は、サーバーのハードウェアのアップグレードを試みることができます。

## ダウンストリームのstorage容量要件 {#downstream-storage-space-requirements}

ターゲットの TiKV クラスターには、インポートされたデータを保存するのに十分なディスク容量が必要です。 [標準のハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲット TiKV クラスターのstorage容量は**、データ ソースのサイズ x レプリカの数 x 2**より大きくなければなりません。たとえば、クラスターがデフォルトで 3 つのレプリカを使用する場合、ターゲット TiKV クラスターには、データ ソースのサイズの 6 倍を超えるstorageスペースが必要です。次の理由により、式は`x 2`になります。

-   インデックスは余分なスペースを必要とする場合があります。
-   RocksDB には空間増幅効果があります。

次の SQL ステートメントを使用して`data-length`のフィールドを要約することにより、データ量を見積もることができます。

-   すべてのスキーマのサイズを MiB で計算します。 `${schema_name}`スキーマ名に置き換えます。

    {{< copyable "" >}}

    ```sql
    select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_schema;
    ```

-   最大テーブルのサイズを MiB で計算します。 ${schema_name} をスキーマ名に置き換えます。

    {{< copyable "" >}}

    ```sql
    select table_name,table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_name,table_schema order by sum desc limit 5;
    ```
