---
title: Software and Hardware Recommendations
summary: TiDB を導入および実行するためのソフトウェアとハードウェアの推奨事項について説明します。
---

# ソフトウェアとハードウェアの推奨事項 {#software-and-hardware-recommendations}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

TiDB は、高性能なオープンソースの分散 SQL データベースとして、Intelアーキテクチャサーバー、ARMアーキテクチャサーバー、および主要な仮想化環境に導入でき、適切に動作します。TiDB は、ほとんどの主要なハードウェア ネットワークと Linux オペレーティング システムをサポートしています。

## OSおよびプラットフォームの要件 {#os-and-platform-requirements}

v7.5 LTS では、TiDB はオペレーティング システムと CPU アーキテクチャのさまざまな組み合わせに対して複数レベルの品質標準を保証します。

-   TiDB は、次のオペレーティング システムと CPU アーキテクチャの組み合わせに対して**エンタープライズ レベルの本番品質を提供し**、製品機能は包括的かつ体系的に検証されています。

    <table><thead><tr><th>オペレーティングシステム</th><th>サポートされているCPUアーキテクチャ</th></tr></thead><tbody><tr><td>Red Hat Enterprise Linux 8.4 以降の 8.x バージョン</td><td><ul><li>64ビット</li><li>アーム64</li></ul></td></tr><tr><td><ul><li> Red Hat Enterprise Linux 7.3 以降の 7.x バージョン</li><li>CentOS 7.3 またはそれ以降の 7.x バージョン (TiDB は 8.5 LTS でサポートを終了します)</li></ul></td><td><ul><li> 64ビット</li><li>アーム64</li></ul></td></tr><tr><td>アマゾン リナックス 2</td><td><ul><li> 64ビット</li><li>アーム64</li></ul></td></tr><tr><td> Rocky Linux 9.1 以降</td><td><ul><li>64ビット</li><li>アーム64</li></ul></td></tr><tr><td>キリン オイラー V10 SP1/SP2</td><td><ul><li> 64ビット</li><li>アーム64</li></ul></td></tr><tr><td>ユニオンテック OS (UOS) V20</td><td><ul><li> 64ビット</li><li>アーム64</li></ul></td></tr><tr><td> openEuler 22.03 LTS SP1/SP3</td><td><ul><li> 64ビット</li><li>アーム64</li></ul></td></tr></tbody></table>

    > **注記：**
    >
    > -   [CentOS Linux のサポート終了](https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/)によると、CentOS Linux 7 のアップストリームサポートは 2024 年 6 月 30 日に終了します。TiDB は 8.5 LTS バージョンで CentOS 7 のサポートを終了します。Rocky Linux 9.1 以降のバージョンを使用することをお勧めします。
    > -   [CentOS Linux のサポート終了](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 8 のアップストリームサポートは 2021 年 12 月 31 日に終了しました。アップストリーム[CentOS Stream 8のサポート](https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/)は 2024 年 5 月 31 日に終了しました。CentOS Stream 9 は CentOS 組織によって引き続きサポートされます。

-   次のオペレーティング システムと CPU アーキテクチャの組み合わせでは、TiDB をコンパイル、ビルド、およびデプロイできます。また、OLTP、OLAP、およびデータ ツールの基本機能も使用できます。ただし、TiDB は**エンタープライズ レベルの本番品質を保証するものではありません**。

    <table><thead><tr><th>オペレーティングシステム</th><th>サポートされているCPUアーキテクチャ</th></tr></thead><tbody><tr><td>macOS 12 (Monterey) 以降</td><td><ul><li>64ビット</li><li>アーム64</li></ul></td></tr><tr><td> Oracle Enterprise Linux 7.3 以降の 7.x バージョン</td><td>64ビット</td></tr><tr><td>Ubuntu LTS 18.04 以降</td><td>64ビット</td></tr><tr><td>CentOS 8 ストリーム</td><td><ul><li>64ビット</li><li>アーム64</li></ul></td></tr><tr><td> Debian 9 (Stretch) 以降</td><td>64ビット</td></tr><tr><td>Fedora 35以降</td><td>64ビット</td></tr><tr><td>openSUSE Leap v15.3 以降 (Tumbleweed を除く)</td><td> 64ビット</td></tr><tr><td>SUSE Linux Enterprise Server 15</td><td> 64ビット</td></tr></tbody></table>

    > **注記：**
    >
    > -   Oracle Enterprise Linux の場合、TiDB は Red Hat 互換カーネル (RHCK) をサポートしますが、Oracle Enterprise Linux が提供する Unbreakable Enterprise Kernel はサポートしません。
    > -   Ubuntu 16.04 のサポートは、TiDB の将来のバージョンでは削除されます。Ubuntu 18.04 以降にアップグレードすることを強くお勧めします。

-   前の 2 つの表に記載されているオペレーティング システムの 32 ビット バージョンを使用している場合、TiDB が 32 ビット オペレーティング システムおよび対応する CPUアーキテクチャ上でコンパイル、ビルド、またはデプロイ可能であることは**保証されません。**または、TiDB は 32 ビット オペレーティング システムに積極的に適応しません。

-   上記に記載されていない他のオペレーティング システム バージョンも動作する可能性がありますが、正式にはサポートされていません。

> **注記：**
>
> -   Oracle Enterprise Linux の場合、TiDB は Red Hat 互換カーネル (RHCK) をサポートしており、Oracle Enterprise Linux が提供する Unbreakable Enterprise Kernel はサポートしていません。
> -   [CentOS Linux のサポート終了](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 8 のアップストリームサポートは 2021 年 12 月 31 日で終了しました。CentOS Stream 8 は CentOS 組織によって引き続きサポートされます。
> -   Ubuntu 16.04 のサポートは、TiDB の将来のバージョンでは削除されます。Ubuntu 18.04 以降にアップグレードすることを強くお勧めします。
> -   前の表に記載されているオペレーティング システムの 32 ビット バージョンを使用している場合、TiDB が 32 ビット オペレーティング システムおよび対応する CPUアーキテクチャ上でコンパイル、ビルド、またはデプロイ可能であることは**保証されません。**または、TiDB は 32 ビット オペレーティング システムに積極的に適応しません。
> -   上記に記載されていない他のオペレーティング システム バージョンも動作する可能性がありますが、正式にはサポートされていません。

### TiDB のコンパイルと実行に必要なライブラリ {#libraries-required-for-compiling-and-running-tidb}

| TiDB のコンパイルと実行に必要なライブラリ | バージョン                 |
| :---------------------- | :-------------------- |
| Golang                  | 1.21以降                |
| さび                      | nightly-2022-07-31 以降 |
| 湾岸協力会議                  | 7.x                   |
| LLVM                    | 13.0以降                |

TiDB を実行するために必要なライブラリ: glibc (2.28-151.el8 バージョン)

### Dockerイメージの依存関係 {#docker-image-dependencies}

次の CPU アーキテクチャがサポートされています。

-   x86_64。TiDB v6.6.0 以降では、 [x86-64-v2 命令セット](https://developers.redhat.com/blog/2021/01/05/building-red-hat-enterprise-linux-9-for-the-x86-64-v2-microarchitecture-level)必要です。
-   アーム64

## ソフトウェアの推奨事項 {#software-recommendations}

### 制御機 {#control-machine}

| ソフトウェア  | バージョン   |
| :------ | :------ |
| sshpass | 1.06以降  |
| TiUP    | 1.5.0以降 |

> **注記：**
>
> TiDB クラスターを操作および管理する必要があり[制御マシンにTiUPを展開する](/production-deployment-using-tiup.md#step-2-deploy-tiup-on-the-control-machine) 。

### ターゲットマシン {#target-machines}

| ソフトウェア  | バージョン    |
| :------ | :------- |
| sshpass | 1.06以降   |
| 沼       | 2.0.12以降 |
| タール     | どれでも     |

## サーバーの推奨事項 {#server-recommendations}

TiDB は、Intel x86-64アーキテクチャの 64 ビット汎用ハードウェアサーバープラットフォーム、または ARMアーキテクチャのハードウェアサーバープラットフォームに導入して実行できます。開発、テスト、および本番環境におけるサーバーハードウェア構成に関する要件と推奨事項 (オペレーティング システム自体が占有するリソースは無視) は次のとおりです。

### 開発およびテスト環境 {#development-and-test-environments}

|    成分   |   CPU  |   メモリ  |               ローカルストレージ              |       通信網      |      インスタンス数（最小要件）     |
| :-----: | :----: | :----: | :----------------------------------: | :------------: | :--------------------: |
|   ティビ   |  8コア以上 | 16GB以上 | [ディスク容量要件](#disk-space-requirements) | ギガビットネットワークカード |    1 (PDと同じマシンに展開可能)   |
|    PD   |  4コア以上 |  8GB以上 |             SAS、200 GB以上             | ギガビットネットワークカード | 1 (TiDB と同じマシンにデプロイ可能) |
|   ティクヴ  |  8コア以上 | 32GB以上 |             SAS、200 GB以上             | ギガビットネットワークカード |            3           |
| TiFlash | 32コア以上 | 64GB以上 |             SSD、200 GB以上             | ギガビットネットワークカード |            1           |
|  ティCDC  |  8コア以上 | 16GB以上 |             SAS、200 GB以上             | ギガビットネットワークカード |            1           |

> **注記：**
>
> -   テスト環境では、TiDB インスタンスと PD インスタンスを同じサーバーにデプロイできます。
> -   パフォーマンス関連のテストでは、テスト結果の正確性を保証するために、低パフォーマンスのstorageおよびネットワーク ハードウェア構成を使用しないでください。
> -   TiKVサーバーでは、読み取りと書き込みを高速化するために NVMe SSD を使用することをお勧めします。
> -   機能のテストと検証のみを行う場合は、手順[TiDB クイック スタート ガイド](/quick-start-with-tidb.md)に従って、単一のマシンに TiDB をデプロイします。
> -   v6.3.0 以降、Linux AMD64アーキテクチャでTiFlashを展開するには、CPU が AVX2 命令セットをサポートしている必要があります。1 `cat /proc/cpuinfo | grep avx2`出力されていることを確認してください。Linux ARM64アーキテクチャでTiFlash を展開するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。3 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`出力されていることを確認してください。命令セット拡張を使用することで、TiFlash のベクトル化エンジンはより優れたパフォーマンスを提供できます。

### 本番環境 {#production-environment}

|    成分   |   CPU  |    メモリ   |  ハードディスクタイプ  |             通信網             | インスタンス数（最小要件） |
| :-----: | :----: | :------: | :----------: | :-------------------------: | :-----------: |
|   ティビ   | 16コア以上 |  48GB以上  | ソリッドステートドライブ | 10 ギガビット ネットワーク カード (2 枚推奨) |       2       |
|    PD   |  8コア以上 |  16GB以上  | ソリッドステートドライブ | 10 ギガビット ネットワーク カード (2 枚推奨) |       3       |
|   ティクヴ  | 16コア以上 |  64GB以上  | ソリッドステートドライブ | 10 ギガビット ネットワーク カード (2 枚推奨) |       3       |
| TiFlash | 48コア以上 | 128 GB以上 |   1台以上のSSD   | 10 ギガビット ネットワーク カード (2 枚推奨) |       2       |
|  ティCDC  | 16コア以上 |  64GB以上  | ソリッドステートドライブ | 10 ギガビット ネットワーク カード (2 枚推奨) |       2       |
|   モニター  |  8コア以上 |  16GB以上  |   スカンジナビア航空  |        ギガビットネットワークカード       |       1       |

> **注記：**
>
> -   本番環境では、TiDB インスタンスと PD インスタンスを同じサーバーにデプロイできます。パフォーマンスと信頼性の要件が高い場合は、別々にデプロイしてみてください。
> -   本番環境では、TiDB、TiKV、 TiFlashをそれぞれ少なくとも 8 個の CPU コアで構成することを強くお勧めします。パフォーマンスを向上させるには、より高い構成をお勧めします。
> -   PCIe SSD を使用している場合は TiKV ハードディスクのサイズを 4 TB 以内に抑え、通常の SSD を使用している場合は 1.5 TB 以内に抑えることをお勧めします。

TiFlashを展開する前に、次の点に注意してください。

-   TiFlash は[複数のディスクに展開](/tiflash/tiflash-configuration.md#multi-disk-deployment)になります。
-   TiKV データのリアルタイム レプリケーションをバッファリングするには、 TiFlashデータ ディレクトリの最初のディスクとして高性能 SSD を使用することをお勧めします。このディスクのパフォーマンスは、PCIe SSD など、TiKV のパフォーマンスよりも低くしてはなりません。ディスク容量は、総容量の 10% 以上である必要があります。そうでない場合、このノードのボトルネックになる可能性があります。他のディスクには通常の SSD を展開できますが、より高性能な PCIe SSD を使用するとパフォーマンスが向上することに注意してください。
-   TiFlash はTiKV とは異なるノードにデプロイすることをお勧めします。TiFlash と TiKVを同じノードにデプロイする必要がある場合は、CPU コアとメモリの数を増やし、相互の干渉を避けるためにTiFlashと TiKV を異なるディスクにデプロイするようにしてください。
-   TiFlashディスクの合計容量は、次のように計算されます: `the data volume of the entire TiKV cluster to be replicated / the number of TiKV replicas * the number of TiFlash replicas` 。たとえば、TiKV の全体の計画容量が 1 TB、TiKV レプリカの数が 3、 TiFlashレプリカの数が 2 の場合、 TiFlashの推奨合計容量は`1024 GB / 3 * 2`です。一部のテーブルのデータのみをレプリケートできます。このような場合は、レプリケートするテーブルのデータ量に応じてTiFlash容量を決定します。

TiCDC を展開する前に、500 GB を超える PCIe SSD ディスクに TiCDC を展開することが推奨されることに注意してください。

## ネットワーク要件 {#network-requirements}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

オープンソースの分散 SQL データベースである TiDB を実行するには、次のネットワーク ポート構成が必要です。実際の環境での TiDB の展開に基づいて、管理者はネットワーク側とホスト側で関連するポートを開くことができます。

|        成分       | デフォルトポート | 説明                                                  |
| :-------------: | :------: | :-------------------------------------------------- |
|       ティビ       |   4000   | アプリケーションとDBAツールの通信ポート                               |
|       ティビ       |   10080  | TiDBステータスを報告するための通信ポート                              |
|       ティクヴ      |   20160  | TiKV通信ポート                                           |
|       ティクヴ      |   20180  | TiKVステータスを報告するための通信ポート                              |
|        PD       |   2379   | TiDBとPD間の通信ポート                                      |
|        PD       |   2380   | PDクラスタ内のノード間通信ポート                                   |
|     TiFlash     |   9000   | TiFlash TCP サービスポート                                 |
|     TiFlash     |   3930   | TiFlash RAFTおよびコプロセッサーサービスポート                       |
|     TiFlash     |   20170  | TiFlashプロキシ サービス ポート                                |
|     TiFlash     |   20292  | PrometheusがTiFlash Proxyメトリックを取得するためのポート            |
|     TiFlash     |   8234   | PrometheusがTiFlashメトリックを取得するためのポート                  |
|       Pump      |   8250   | Pump通信ポート                                           |
|     Drainer     |   8249   | Drainer通信ポート                                        |
|      ティCDC      |   8300   | TiCDC通信ポート                                          |
|        監視       |   9090   | Prometheusサービスの通信ポート                                |
|        監視       |   12020  | NgMonitoring サービスの通信ポート                             |
|    ノードエクスポーター   |   9100   | 各TiDBクラスタノードのシステム情報を報告するための通信ポート                    |
| ブラックボックスエクスポーター |   9115   | TiDB クラスタ内のポートを監視するために使用される Blackbox_exporter 通信ポート |
|      グラファナ      |   3000   | 外部Web監視サービスおよびクライアント（ブラウザ）アクセス用のポート                 |
|    アラートマネージャー   |   9093   | アラートウェブサービスのポート                                     |
|    アラートマネージャー   |   9094   | アラート通信ポート                                           |

## ディスク容量要件 {#disk-space-requirements}

<table><thead><tr><th>成分</th><th>ディスク容量要件</th><th>健全なディスク使用率</th></tr></thead><tbody><tr><td>ティビ</td><td><ul><li>ログディスク用に少なくとも30 GB</li><li> v6.5.0 以降では、インデックスの追加などの DDL 操作を高速化するために、Fast Online DDL ( <a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_ddl_enable_fast_reorg-new-in-v630">tidb_ddl_enable_fast_reorg</a>変数によって制御) がデフォルトで有効になっています。アプリケーションに大きなオブジェクトを含む DDL 操作がある場合、または<a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into">IMPORT INTO</a>を使用してデータをインポートする場合は、TiDB 用に追加の SSD ディスク領域 (100 GB 以上) を用意することを強くお勧めします。詳細な構成手順については、 <a href="https://docs.pingcap.com/tidb/v7.5/check-before-deployment#set-temporary-spaces-for-tidb-instances-recommended">「TiDB インスタンスの一時領域の設定」</a>を参照してください。</li></ul></td><td> 90%未満</td></tr><tr><td>PD</td><td>データディスクとログディスクにはそれぞれ少なくとも20 GB</td><td> 90%未満</td></tr><tr><td>ティクヴ</td><td>データディスクとログディスクにはそれぞれ少なくとも100 GB</td><td> 80%未満</td></tr><tr><td>TiFlash</td><td>データディスクには少なくとも100 GB、ログディスクには少なくとも30 GB</td><td> 80%未満</td></tr><tr><td>TiUP</td><td><ul><li>制御マシン: 単一バージョンの TiDB クラスターをデプロイするには、1 GB を超えるスペースは必要ありません。複数のバージョンの TiDB クラスターをデプロイする場合は、必要なスペースが増加します。</li><li>デプロイメント サーバー (TiDB コンポーネントが実行されるマシン): TiFlash は約 700 MB のスペースを占有し、その他のコンポーネント (PD、TiDB、TiKV など) はそれぞれ約 200 MB のスペースを占有します。クラスターのデプロイメント プロセス中、 TiUPクラスターは一時ファイルを保存するために 1 MB 未満の一時スペース ( <code>/tmp</code>ディレクトリ) を必要とします。</li></ul></td><td>該当なし</td></tr><tr><td>モニタリング</td><td><ul><li>コンポーネント: 3 x 1 GB x コンポーネント数 (各コンポーネントは 1 日あたり約 1 GB、合計 3 日間) + 20 GB の予約済みスペース</li><li>Top SQL: 30 x 50 MB x コンポーネント数 (各コンポーネントは1 日あたり約 50 MB を占有し、合計 30 日間)</li><li> ConprofとTop SQLは予約スペースを共有します</li></ul></td><td>該当なし</td></tr></tbody></table>

## Webブラウザの要件 {#web-browser-requirements}

TiDB は、データベース メトリックの視覚化を提供するために[グラファナ](https://grafana.com/)に依存しています。Javascript が有効になっている最新バージョンの Internet Explorer、Chrome、または Firefox で十分です。

## TiFlash分散storageおよびコンピューティングアーキテクチャのハードウェアおよびソフトウェア要件 {#hardware-and-software-requirements-for-tiflash-disaggregated-storage-and-compute-architecture}

上記のTiFlashソフトウェアおよびハードウェア要件は、結合されたstorageおよびコンピューティングアーキテクチャ用です。v7.0.0 以降、 TiFlash は[分散型storageとコンピューティングアーキテクチャ](/tiflash/tiflash-disaggregated-and-s3.md)サポートします。このアーキテクチャでは、 TiFlash は書き込みノードとコンピューティング ノードの 2 種類のノードに分かれています。これらのノードの要件は次のとおりです。

-   ソフトウェア: 結合されたstorageとコンピューティングアーキテクチャと同じままです ( [OSおよびプラットフォームの要件](#os-and-platform-requirements)参照)。
-   ネットワーク ポート: 結合されたstorageおよびコンピューティングアーキテクチャと同じままです ( [通信網](#network-requirements)参照)。
-   ディスクスペース：
    -   TiFlash書き込みノード: データを Amazon S3 にアップロードする前に、 TiFlashレプリカを追加したり、リージョンレプリカを移行したりするときにローカルバッファとして使用されるディスク領域を少なくとも 200 GB 構成することをお勧めします。また、Amazon S3 と互換性のあるオブジェクトstorageが必要です。
    -   TiFlashコンピューティング ノード: 少なくとも 100 GB のディスク領域を構成することをお勧めします。これは主に、パフォーマンスを向上させるために書き込みノードから読み取られたデータをキャッシュするために使用されます。コンピューティング ノードのキャッシュが完全に使用される場合がありますが、これは正常です。
-   CPU とメモリの要件については、次のセクションで説明します。

### 開発およびテスト環境 {#development-and-test-environments}

| 成分                  | CPU    | メモリ    | ローカルストレージ    | 通信網         | インスタンス数（最小要件） |
| ------------------- | ------ | ------ | ------------ | ----------- | ------------- |
| TiFlash書き込みノード      | 16コア以上 | 32GB以上 | SSD、200 GB以上 | ギガビットイーサネット | 1             |
| TiFlashコンピューティングノード | 16コア以上 | 32GB以上 | SSD、100 GB以上 | ギガビットイーサネット | 0（下記注記参照）     |

### 本番環境 {#production-environment}

| 成分                  | CPU    | メモリ    | ディスクタイプ  | 通信網                      | インスタンス数（最小要件） |
| ------------------- | ------ | ------ | -------- | ------------------------ | ------------- |
| TiFlash書き込みノード      | 32コア以上 | 64GB以上 | 1台以上のSSD | 10 ギガビット イーサネット (2 個を推奨) | 1             |
| TiFlashコンピューティングノード | 32コア以上 | 64GB以上 | 1台以上のSSD | 10 ギガビット イーサネット (2 個を推奨) | 0（下記注記参照）     |

> **注記：**
>
> TiUPなどのデプロイメント ツールを使用して、 `[0, +inf]`の範囲内でTiFlashコンピューティング ノードを迅速にスケールインまたはスケールアウトできます。
