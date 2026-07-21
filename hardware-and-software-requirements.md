---
title: TiDB Software and Hardware Requirements
summary: TiDBの導入と実行に関するソフトウェアおよびハードウェアの推奨事項を学びましょう。
---

# TiDBのソフトウェアおよびハードウェア要件 {#tidb-software-and-hardware-requirements}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

このドキュメントでは、TiDBデータベースのデプロイと実行に必要なソフトウェアおよびハードウェア要件について説明します。TiDBは、高性能なオープンソースの分散型SQLデータベースであり、Intelアーキテクチャサーバー、ARMアーキテクチャサーバー、および主要な仮想化環境にデプロイして良好に動作します。TiDBは、主要なハードウェアネットワークとLinuxオペレーティングシステムのほとんどをサポートしています。

## OSおよびプラットフォームの要件 {#os-and-platform-requirements}

TiDBはv8.5 LTSにおいて、様々なオペレーティングシステムとCPUアーキテクチャの組み合わせに対して、多段階の品質基準を保証します。

-   TiDBは、以下のオペレーティングシステムとCPUアーキテクチャの組み合わせにおいて、**エンタープライズレベルの本番品質を提供し**、製品機能は包括的かつ体系的に検証されています。

    <table><thead><tr><th>オペレーティングシステム</th><th>サポートされているCPUアーキテクチャ</th></tr></thead><tbody><tr><td>Red Hat Enterprise Linux 9.4 以降の 9.x バージョン</td><td><ul><li>x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> Red Hat Enterprise Linux 8.6 以降の 8.x バージョン</td><td><ul><li>x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> Amazon Linux 2</td><td><ul><li> x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> Amazon Linux 2023</td><td><ul><li> x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> Rocky Linux 9.1以降</td><td><ul><li>x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> Kylin V10 SP1/SP2/SP3（SP3はv7.5.5以降でサポートされています）</td><td><ul><li> x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> UnionTech OS (UOS) V20</td><td><ul><li> x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> openEuler 22.03 LTS SP1/SP3</td><td><ul><li> x86_64</li><li> ARM 64</li></ul></td></tr></tbody></table>

    > **Warning:**
    >
    > -   [CentOS Linux サポート終了](https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/)よると、CentOS Linux 7 のアップストリーム サポートは 2024 年 6 月 30 日に終了しました。
    >     -   TiDBをアップグレードする前に、オペレーティングシステムのバージョンを確認してください。TiDB v8.4.0 DMRおよびv8.5.0では、glibc 2.17のサポートが終了し、CentOS Linux 7のサポートとテストも終了しました。Rocky Linux 9.1以降のバージョンを使用することをお勧めします。CentOS 7上のTiDBクラスタをv8.4.0またはv8.5.0にアップグレードすると、クラスタが利用できなくなるリスクがあります。
    >     -   CentOS Linux 7 をまだ使用しているユーザーを支援するために、v8.5.1 以降、TiDB は glibc 2.17 のサポートを再開し、CentOS Linux 7 のテストを再開し、CentOS Linux 7 と互換性を持つようになりました。ただし、CentOS Linux の EOL ステータスのため、CentOS Linux 7 の[公式発表およびセキュリティに関するガイダンス](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol)を確認し、Rocky Linux 9.1 や TiDB が本番用にサポートするオペレーティング システムに移行することを強くお勧めします。 後で。
    > -   [Red Hat Enterprise Linux ライフサイクル](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)によると、Red Hat Enterprise Linux 7 のメンテナンスサポートは 2024 年 6 月 30 日に終了しました。TiDB は、8.4 DMR バージョン以降、Red Hat Enterprise Linux 7 のサポートを終了します。Rocky Linux 9.1 以降のバージョンを使用することをお勧めします。Red Hat Enterprise Linux 7 上の TiDB クラスタを v8.4.0 以降にアップグレードすると、クラスタが使用できなくなります。TiDB をアップグレードする前に、オペレーティングシステムのバージョンを確認してください。

    > **Note:**
    >
    > Red Hat Enterprise Linux 9.x のサポートは[TiUP](https://github.com/pingcap/tiup/releases) v1.16.5 から開始されます。

-   以下のオペレーティングシステムとCPUアーキテクチャの組み合わせであれば、TiDBのコンパイル、ビルド、デプロイが可能です。さらに、OLTP、OLAP、およびデータツールの基本機能も利用できます。ただし、これらの組み合わせは包括的かつ体系的なテストを受けていないため、TiDBは**エンタープライズレベルの本番品質を保証するものではありません**。

    <table><thead><tr><th>オペレーティングシステム</th><th>サポートされているCPUアーキテクチャ</th></tr></thead><tbody><tr><td>macOS 12 (Monterey) 以降</td><td><ul><li>x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> Oracle Enterprise Linux 8以降</td><td>x86_64</td></tr><tr><td> Ubuntu LTS 20.04以降</td><td>x86_64</td></tr><tr><td> CentOS Stream 8</td><td><ul><li> x86_64</li><li> ARM 64</li></ul></td></tr><tr><td> Debian 10 (Buster) 以降</td><td>x86_64</td></tr><tr><td> Fedora 38以降</td><td>x86_64</td></tr><tr><td> openSUSE Leap v15.5以降（Tumbleweedを除く）</td><td> x86_64</td></tr><tr><td> SUSE Linux Enterprise Server 15</td><td> x86_64</td></tr></tbody></table>

    > **Note:**
    >
    > -   Oracle Enterprise Linuxの場合、TiDBはRed Hat互換カーネル（RHCK）をサポートしており、Oracle Enterprise Linuxが提供するUnbreakable Enterprise Kernelはサポートしていません。
    > -   TiDBの今後のバージョンでは、Ubuntu 16.04のサポートは終了します。Ubuntu 18.04以降へのアップグレードを強くお勧めします。
    > -   CentOS Stream 8 は、2024 年 5 月 31 日に[ビルド終了](https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/)。

-   前述の 2 つの表に記載されているオペレーティングシステムの 32 ビット版を使用している場合、TiDB は 32 ビットオペレーティングシステムおよび対応する CPUアーキテクチャ上でコンパイル、ビルド、またはデプロイできることが**保証されません**。また、TiDB は 32 ビットオペレーティングシステムに積極的に対応しません。

-   上記に記載されていない他のオペレーティングシステムバージョンでも動作する可能性はありますが、公式にはサポートされていません。

### TiDBのコンパイルと実行に必要なライブラリ {#libraries-required-for-compiling-and-running-tidb}

| TiDBのコンパイルと実行に必要なライブラリ | バージョン              |
| :--------------------- | :----------------- |
| Golang                 | 1.25以降             |
| Rust                     | nightly - 2025年2月28日以降 |
| GCC                    | 7.x                |
| LLVM                   | バージョン17.0以降        |

TiDBの実行に必要なライブラリ：glibc（バージョン2.28-151.el8）

### Dockerイメージの依存関係 {#docker-image-dependencies}

以下のCPUアーキテクチャがサポートされています。

-   x86_64。 TiDB v6.6.0 以降では、 [x86-64-v2命令セット](https://developers.redhat.com/blog/2021/01/05/building-red-hat-enterprise-linux-9-for-the-x86-64-v2-microarchitecture-level)が必要です。
-   ARM 64

## ソフトウェア要件 {#software-requirements}

### 制御機械 {#control-machine}

| ソフトウェア  | バージョン       |
| :------ | :---------- |
| sshpass | バージョン1.06以降 |
| TiUP    | 1.5.0以降     |

> **Note:**
>
> TiDB クラスターを運用および管理するには、 [制御マシンにTiUPをデプロイする](/production-deployment-using-tiup.md#step-2-deploy-tiup-on-the-control-machine)必要があります。

### ターゲットマシン {#target-machines}

| ソフトウェア  | バージョン       |
| :------ | :---------- |
| sshpass | バージョン1.06以降 |
| NUMA     | 2.0.12以降    |
| tar     | 任意        |

## サーバー要件 {#server-requirements}

TiDBは、Intel x86-64アーキテクチャの64ビット汎用ハードウェアサーバープラットフォーム、またはARMアーキテクチャのハードサーバープラットフォームにデプロイして実行できます。開発、テスト、および本番環境におけるサーバーハードウェア構成に関する要件と推奨事項（オペレーティングシステム自体が占めるリソースは除く）は以下のとおりです。

### 開発環境およびテスト環境 {#development-and-test-environments}

|    成分   |   CPU  |   メモリ  |           ローカルストレージ           |     ネットワーク     |     インスタンス数（最小要件）    |
| :-----: | :----: | :----: | :---------------------------: | :------------: | :------------------: |
|   TiDB  |  8コア以上 | 16GB以上 | [保管要件](#storage-requirements) | ギガビットネットワークカード |   1（PDと同じマシンに展開可能）   |
|    PD   |  4コア以上 |  8GB以上 |          SAS、200GB以上          | ギガビットネットワークカード | 1（TiDBと同じマシンにデプロイ可能） |
|   TiKV  |  8コア以上 | 32GB以上 |          SAS、200GB以上          | ギガビットネットワークカード |           3          |
| TiFlash | 32コア以上 | 64GB以上 |          SSD、200GB以上          | ギガビットネットワークカード |           1          |
|  TiCDC  |  8コア以上 | 16GB以上 |          SAS、200GB以上          | ギガビットネットワークカード |           1          |
| TiProxy |  4コア以上 |  8GB以上 |              SAS              | ギガビットネットワークカード |           1          |

> **Note:**
>
> -   テスト環境では、TiDBとPDのインスタンスを同じサーバーにデプロイできます。
> -   性能関連のテストにおいては、テスト結果の正確性を保証するため、性能の低いストレージおよびネットワークハードウェア構成を使用しないでください。
> -   TiKVサーバーには、読み書き速度を向上させるためにNVMe SSDの使用をお勧めします。
> -   機能をテストして確認するだけの場合は、 [TiDB クイックスタートガイド](/quick-start-with-tidb.md)に従って単一マシンに TiDB を展開してください。
> -   バージョン 6.3.0 以降、Linux AMD64アーキテクチャでTiFlash をデプロイするには、CPU が AVX2 命令セットをサポートしている必要があります。 `grep avx2 /proc/cpuinfo`に出力があることを確認してください。Linux ARM64アーキテクチャでTiFlash をデプロイするには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。 `grep 'crc32' /proc/cpuinfo | grep 'asimd'`に出力があることを確認してください。命令セット拡張機能を使用することで、TiFlash のベクトル化エンジンはより優れたパフォーマンスを発揮できます。

### 生産環境 {#production-environment}

|    成分   |   CPU  |   メモリ   | ハードディスクの種類 |         ネットワーク         | インスタンス数（最小要件） |
| :-----: | :----: | :-----: | :--------: | :--------------------: | :-----------: |
|   TiDB  | 16コア以上 |  48GB以上 |     SSD    | 10ギガビットネットワークカード（2枚推奨） |       2       |
|    PD   |  8コア以上 |  16GB以上 |     SSD    | 10ギガビットネットワークカード（2枚推奨） |       3       |
|   TiKV  | 16コア以上 |  64GB以上 |     SSD    | 10ギガビットネットワークカード（2枚推奨） |       3       |
| TiFlash | 48コア以上 | 128GB以上 |  1つ以上のSSD  | 10ギガビットネットワークカード（2枚推奨） |       2       |
|  TiCDC  | 16コア以上 |  64GB以上 |     SSD    | 10ギガビットネットワークカード（2枚推奨） |       2       |
|   モニター  |  8コア以上 |  16GB以上 |     SAS    |     ギガビットネットワークカード     |       1       |
| TiProxy |  8コア以上 |  16GB以上 |     SAS    | 10ギガビットネットワークカード（2枚推奨） |       2       |

> **Note:**
>
> -   本番環境では、TiDBとPDのインスタンスを同じサーバーにデプロイできます。ただし、より高いパフォーマンスと信頼性を求める場合は、それぞれを別々にデプロイすることをお勧めします。
> -   本番環境では、TiDB、TiKV、およびTiFlashをそれぞれ最低8コアのCPUで構成することを強く推奨します。より高いパフォーマンスを得るには、さらに高い構成をお勧めします。
> -   PCIe SSDを使用する場合はTiKVハードディスクの容量を4TB以内に、通常のSSDを使用する場合は1.5TB以内に抑えることをお勧めします。
> -   AWS、Google Cloud、Azureなどのクラウドプロバイダー上にTiDBクラスタをデプロイする場合は、インスタンスストアではなくクラウドディスクをTiKVノードに使用することをお勧めします。
>
>     -   インスタンスストアボリュームのデータ耐久性は比較的低いです。インスタンスストアのライフサイクルは仮想マシンのライフサイクルと連動しています。インスタンスの再起動、停止、移行、ハードウェア障害、またはメンテナンスが行われると、データが失われる可能性があります。ほとんどのクラウドプロバイダーは、インスタンスストアを一時的なstorageとして明示的に分類しています。たとえば、 [AWSドキュメント](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Storage.html)によると、「インスタンスストアボリューム上のデータは、関連付けられたインスタンスの存続期間中のみ保持されます。インスタンスを停止、休止状態、または終了すると、インスタンスストアボリューム上のデータはすべて失われます。」
>     -   インスタンスストアボリュームは通常、スナップショットやノード間・リージョン間のレプリケーションをサポートしていません。そのため、データの破損やハードウェア障害が発生した場合、迅速なデータ復旧は困難です。
>     -   インスタンスストアの容量はインスタンスタイプに紐づいており、個別にスケーリングすることはできません。

TiFlashを導入する前に、以下の項目に注意してください。

-   TiFlash は[複数のディスクに展開されています](/tiflash/tiflash-configuration.md#multi-disk-deployment)。
-   TiFlashデータディレクトリの最初のディスクとして、TiKVデータのリアルタイムレプリケーションをバッファリングするために、高性能SSDを使用することをお勧めします。このディスクの性能は、PCIe SSDなど、TiKVと同等以上である必要があります。ディスク容量は、総容量の10%以上でなければなりません。そうでない場合、このノードのボトルネックになる可能性があります。他のディスクには通常のSSDを使用することもできますが、より高性能なPCIe SSDを使用すると、パフォーマンスが向上することに注意してください。
-   TiFlashはTiKVとは別のノードにデプロイすることをお勧めします。どうしても同じノードにTiFlashとTiKVをデプロイする必要がある場合は、CPUコア数とメモリ容量を増やし、互いに干渉しないようにTiFlashとTiKVを異なるディスクにデプロイするようにしてください。
-   TiFlashディスクの総容量は、次のように計算されます: `the data volume of the entire TiKV cluster to be replicated / the number of TiKV replicas * the number of TiFlash replicas` 。たとえば、TiKV の計画容量が 1 TB、TiKV レプリカ数が 3、 TiFlashレプリカ数が 2 の場合、推奨されるTiFlashの総容量は`1024 GB / 3 * 2`です。一部のテーブルのデータのみを複製することもできます。その場合は、複製するテーブルのデータ量に応じてTiFlash の容量を決定します。

TiCDCを導入する前に、500GB以上のPCIe SSDディスクにTiCDCを導入することを推奨します。

## ネットワーク要件 {#network-requirements}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

オープンソースの分散型SQLデータベースであるTiDBは、動作に以下のネットワークポート設定が必要です。実際の環境におけるTiDBの導入状況に応じて、管理者はネットワーク側とホスト側で関連するポートを開放することができます。

|        成分       | デフォルトポート | 説明                                               |
| :-------------: | :------: | :----------------------------------------------- |
|       TiDB      |   4000   | アプリケーションおよびDBAツール用の通信ポート                         |
|       TiDB      |   10080  | TiDBの状態を報告するための通信ポート                             |
|       TiKV      |   20160  | TiKV通信ポート                                        |
|       TiKV      |   20180  | TiKVの状態を報告するための通信ポート                             |
|        PD       |   2379   | TiDBとPD間の通信ポート                                   |
|        PD       |   2380   | PDクラスタ内のノード間通信ポート                                |
|     TiFlash     |   9000   | TiFlash TCPサービスポート                               |
|     TiFlash     |   3930   | TiFlash RAFTおよびコプロセッサーサービスポート                    |
|     TiFlash     |   20170  | TiFlashプロキシサービスポート                               |
|     TiFlash     |   20292  | PrometheusがTiFlashプロキシのメトリクスを取得するためのポート          |
|     TiFlash     |   8234   | PrometheusがTiFlashのメトリクスを取得するためのポート              |
|      TiCDC      |   8300   | TiCDC通信ポート                                       |
|        監視       |   9090   | Prometheusサービス用の通信ポート                            |
|        監視       |   12020  | NgMonitoringサービス用の通信ポート                          |
|    Node Exporter   |   9100   | 各TiDBクラスタノードのシステム情報を報告するための通信ポート                 |
| Blackbox Exporter |   9115   | TiDBクラスタ内のポートを監視するために使用されるBlackbox_exporter通信ポート |
|      Grafana      |   3000   | 外部Web監視サービスおよびクライアント（ブラウザ）アクセス用のポート              |
|    Alertmanager   |   9093   | アラートWebサービスのポート                                  |
|    Alertmanager   |   9094   | アラート通信ポート                                        |

## 保管要件 {#storage-requirements}

<table><thead><tr><th>コンポーネント</th><th>ディスク容量要件</th><th>ディスク使用率は良好です</th></tr></thead><tbody><tr><td>TiDB</td><td><ul><li>ログディスクには最低30GBが必要です</li><li>バージョン6.5.0以降、インデックスの追加などのDDL操作を高速化するために、Fast Online DDL（<a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_ddl_enable_fast_reorg-new-in-v630">tidb_ddl_enable_fast_reorg</a>変数で制御）がデフォルトで有効になっています。アプリケーションで大きなオブジェクトを含むDDL操作がある場合、または<a href="https://docs.pingcap.com/tidb/dev/sql-statement-import-into">IMPORT INTO</a>を使用してデータをインポートする場合は、TiDB用にSSDディスク領域を追加で用意することを強くお勧めします（100GB以上）。詳細な設定手順については、 <a href="https://docs.pingcap.com/tidb/dev/check-before-deployment#set-temporary-spaces-for-tidb-instances-recommended">「TiDBインスタンスの一時領域を設定する」を</a>参照してください。</li></ul></td><td> 90%未満</td></tr><tr><td>PD</td><td>データディスクとログディスクにはそれぞれ最低20GBの容量が必要です。</td><td> 90%未満</td></tr><tr><td>TiKV</td><td>データディスクとログディスクにはそれぞれ最低100GBが必要です。</td><td> 80%未満</td></tr><tr><td>TiFlash</td><td>データディスクには最低100GB、ログディスクには最低30GBが必要です。</td><td> 80%未満</td></tr><tr><td>TiUP</td><td><ul><li>コントロールマシン：単一バージョンのTiDBクラスターをデプロイする場合、必要な容量は1GB以下です。複数のバージョンのTiDBクラスターをデプロイする場合は、必要な容量が増加します。</li><li>デプロイメントサーバー（TiDBコンポーネントが実行されるマシン）： TiFlashは約700MBの容量を占有し、その他のコンポーネント（PD、TiDB、TiKVなど）はそれぞれ約200MBの容量を占有します。クラスターのデプロイメントプロセス中、 TiUPクラスターは一時ファイルを保存するために1MB未満の一時領域（ <code>/tmp</code>ディレクトリ）を必要とします。</li></ul></td><td>該当なし</td></tr><tr><td>モニタリング</td><td><ul><li>Conprof: 3 x 1 GB x コンポーネント数（各コンポーネントは1日あたり約1 GB、合計3日間）+ 20 GBの予約済みスペース</li><li>Top SQL：30 x 50MB x コンポーネント数（各コンポーネントは1日あたり約50MBを占有し、合計30日間）</li><li> ConprofとTop SQLは予約スペースを共有しています。</li></ul></td><td>該当なし</td></tr></tbody></table>

TiDBはXFSおよびExt4ファイルシステムをサポートしています。その他のファイルシステムは、本番は推奨されません。

## ウェブブラウザの要件 {#web-browser-requirements}

TiDBは、データベースメトリクスの可視化に[Grafana](https://grafana.com/)利用しています。JavaScriptが有効になっている最新バージョンのMicrosoft Edge、Safari、Chrome、またはFirefoxがあれば十分です。

## TiFlashの分離型ストレージおよびコンピューティングアーキテクチャに必要なハードウェアおよびソフトウェア要件 {#hardware-and-software-requirements-for-tiflash-disaggregated-storage-and-compute-architecture}

前述のTiFlashソフトウェアおよびハードウェア要件は、結合されたストレージとコンピューティングアーキテクチャに関するものです。 v7.0.0 以降、 TiFlash は[分散型ストレージおよびコンピューティングアーキテクチャ](/tiflash/tiflash-disaggregated-and-s3.md)をサポートします。このアーキテクチャでは、 TiFlash は書き込みノードと計算ノードの 2 種類のノードに分割されます。これらのノードの要件は次のとおりです。

-   ソフトウェア: 結合されたストレージとコンピューティングアーキテクチャと同じままです。 [OSおよびプラットフォームの要件](#os-and-platform-requirements)を参照してください。
-   ネットワーク ポート: 結合されたストレージとコンピューティングアーキテクチャと同じままです。[ネットワーク](#network-requirements)を参照してください。
-   ディスク容量:
    -   TiFlash書き込みノード： TiFlashレプリカの追加時およびリージョンレプリカの移行時に、データをAmazon S3にアップロードする前にローカルバッファとして使用されるディスク容量は、少なくとも200GB以上設定することをお勧めします。また、Amazon S3と互換性のあるオブジェクトストレージが必要です。
    -   TiFlash Compute Node：パフォーマンス向上のため、主にWrite Nodeから読み取ったデータをキャッシュする目的で、最低でも100GBのディスク容量を設定することをお勧めします。Compute Nodeのキャッシュが満杯になる場合がありますが、これは正常な動作です。
-   CPUとメモリの要件については、以下のセクションで説明します。

### 開発環境およびテスト環境 {#development-and-test-environments}

| 成分                   | CPU    | メモリ    | ローカルストレージ   | ネットワーク      | インスタンス数（最小要件） |
| -------------------- | ------ | ------ | ----------- | ----------- | ------------- |
| TiFlash書き込みノード       | 16コア以上 | 32GB以上 | SSD、200GB以上 | ギガビットイーサネット | 1             |
| TiFlash Compute Node | 16コア以上 | 32GB以上 | SSD、100GB以上 | ギガビットイーサネット | 0（以下の注記を参照）   |

### 生産環境 {#production-environment}

| 成分                   | CPU    | メモリ    | ディスクの種類  | ネットワーク                | インスタンス数（最小要件） |
| -------------------- | ------ | ------ | -------- | --------------------- | ------------- |
| TiFlash書き込みノード       | 32コア以上 | 64GB以上 | 1つ以上のSSD | 10ギガビットイーサネット（2ポート推奨） | 1             |
| TiFlash Compute Node | 32コア以上 | 64GB以上 | 1つ以上のSSD | 10ギガビットイーサネット（2ポート推奨） | 0（以下の注記を参照）   |

> **Note:**
>
> TiUPなどのデプロイメントツールを使用すると、 `[0, +inf]`の範囲内でTiFlash Compute Nodeを迅速にスケールインまたはスケールアウトできます。
