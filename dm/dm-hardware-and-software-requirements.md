---
title: Software and Hardware Requirements
summary: Learn the software and hardware requirements for DM cluster.
---

# ソフトウェアとハードウェアの要件 {#software-and-hardware-requirements}

TiDBデータ移行（DM）は、主流のLinuxオペレーティングシステムをサポートします。特定のバージョン要件については、次の表を参照してください。

| Linux OS                 |  バージョン  |
| :----------------------- | :-----: |
| Red Hat Enterprise Linux |  7.3以降  |
| CentOS                   |  7.3以降  |
| Oracle Enterprise Linux  |  7.3以降  |
| Ubuntu LTS               | 16.04以降 |

DMは、Intelアーキテクチャサーバーおよび主流の仮想化環境に展開して実行できます。

## 推奨されるサーバー要件 {#recommended-server-requirements}

DMは、64ビットの汎用ハードウェアサーバープラットフォーム（Intel x86-64アーキテクチャ）に展開して実行できます。開発、テスト、および実稼働環境で使用されるサーバーの場合、このセクションでは、推奨されるハードウェア構成を示します（これらには、オペレーティングシステムで使用されるリソースは含まれていません）。

### 開発およびテスト環境 {#development-and-test-environments}

| 成分     | CPU  | メモリー    | ローカルストレージ                        | 通信網            | インスタンスの数（最小要件）        |
| ------ | ---- | ------- | -------------------------------- | -------------- | --------------------- |
| DMマスター | 4コア+ | 8GB以上   | SAS、200GB以上                      | ギガビットネットワークカード | 1                     |
| DMワーカー | 8コア+ | 16 GB + | SAS、200 GB以上（移行されたデータのサイズよりも大きい） | ギガビットネットワークカード | アップストリームMySQLインスタンスの数 |

> **ノート：**
>
> -   テスト環境では、機能検証に使用されるDM-masterとDM-workerを同じサーバーにデプロイできます。
> -   パフォーマンステスト結果の精度への干渉を防ぐために、パフォーマンスの低いストレージおよびネットワークハードウェア構成を使用することは**お勧め**しません。
> -   機能のみを検証する必要がある場合は、DMマスターを単一のマシンに展開できます。デプロイされるDM-workerの数は、アップストリームのMySQLインスタンスの数以上である必要があります。高可用性を確保するには、より多くのDMワーカーをデプロイすることをお勧めします。
> -   DM-workerは、 `dump`フェーズと`load`フェーズで完全なデータを保存します。したがって、DM-workerのディスク容量は、移行するデータの合計量よりも大きい必要があります。移行タスクでリレーログが有効になっている場合、DM-workerはアップストリームのbinlogデータを保存するために追加のディスクスペースを必要とします。

### 本番環境 {#production-environment}

| 成分     | CPU   | メモリー    | ハードディスクの種類                       | 通信網              | インスタンスの数（最小要件）             |
| ------ | ----- | ------- | -------------------------------- | ---------------- | -------------------------- |
| DMマスター | 4コア+  | 8GB以上   | SAS、200GB以上                      | ギガビットネットワークカード   | 3                          |
| DMワーカー | 16コア+ | 32 GB + | SSD、200 GB以上（移行されたデータのサイズよりも大きい） | 10ギガビットネットワークカード | アップストリームMySQLインスタンスの数よりも多い |
| モニター   | 8コア+  | 16 GB + | SAS、200GB以上                      | ギガビットネットワークカード   | 1                          |

> **ノート：**
>
> -   実稼働環境では、DM-masterとDM-workerを同じサーバーにデプロイして実行することはお勧めしません。これは、DM-workerがデータをディスクに書き込むときに、DM-masterの高可用性コンポーネントによるディスクの使用を妨げる可能性があるためです。 。
> -   パフォーマンスの問題が発生した場合は、 [DMのConfiguration / コンフィグレーションを最適化する](/dm/dm-tune-configuration.md)のドキュメントに従ってタスク構成ファイルを変更することをお勧めします。構成ファイルを調整してもパフォーマンスが効果的に最適化されない場合は、サーバーのハードウェアのアップグレードを試みることができます。

## ダウンストリームストレージスペースの要件 {#downstream-storage-space-requirements}

ターゲットTiKVクラスタには、インポートされたデータを格納するのに十分なディスク容量が必要です。 [標準のハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲットTiKVクラスタのストレージスペースは**、データソースのサイズxレプリカの数x2**よりも大きくする必要があります。たとえば、クラスタがデフォルトで3つのレプリカを使用する場合、ターゲットTiKVクラスタには、データソースのサイズの6倍を超えるストレージスペースが必要です。数式には`x 2`あります。理由は次のとおりです。

-   インデックスには余分なスペースが必要になる場合があります。
-   RocksDBにはスペース増幅効果があります。

次のSQLステートメントを使用して`data-length`フィールドを要約すると、データ量を見積もることができます。

-   MiBですべてのスキーマのサイズを計算します。 `${schema_name}`をスキーマ名に置き換えます。

    {{< copyable "" >}}

    ```sql
    select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_schema;
    ```

-   最大のテーブルのサイズをMiBで計算します。 ${schema_name}をスキーマ名に置き換えます。

    {{< copyable "" >}}

    ```sql
    select table_name,table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_name,table_schema order by sum  desc limit 5;
    ```
