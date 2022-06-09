---
title: Software and Hardware Recommendations
summary: Learn the software and hardware recommendations for deploying and running TiDB.
---

# ソフトウェアとハードウェアの推奨事項 {#software-and-hardware-recommendations}

高性能のオープンソース分散NewSQLデータベースとして、TiDBはIntelアーキテクチャサーバー、ARMアーキテクチャサーバー、および主要な仮想化環境に導入でき、適切に動作します。 TiDBは、主要なハードウェアネットワークとLinuxオペレーティングシステムのほとんどをサポートしています。

## LinuxOSのバージョン要件 {#linux-os-version-requirements}

|         Linux OS         |     バージョン     |
| :----------------------: | :-----------: |
| Red Hat Enterprise Linux | 7.3以降の7.xリリース |
|          CentOS          | 7.3以降の7.xリリース |
|  Oracle Enterprise Linux | 7.3以降の7.xリリース |
|        Ubuntu LTS        |    16.04以降    |

> **ノート：**
>
> -   Oracle Enterprise Linuxの場合、TiDBはRed Hat互換カーネル（RHCK）をサポートし、OracleEnterpriseLinuxが提供するUnbreakableEnterpriseカーネルをサポートしません。
> -   多数のTiDBテストがCentOS7.3システムで実行されており、私たちのコミュニティには、LinuxオペレーティングシステムにTiDBをデプロイするための多くのベストプラクティスがあります。したがって、CentOS7.3以降にTiDBをデプロイすることをお勧めします。
> -   上記のLinuxオペレーティングシステムのサポートには、物理サーバーだけでなく、VMware、KVM、XENなどの主要な仮想化環境での展開と操作が含まれます。
> -   Red Hat Enterprise Linux 8.0、CentOS 8 Stream、およびOracle Enterprise Linux 8.0は、これらのプラットフォームのテストが進行中であるため、まだサポートされていません。
> -   CentOS 8 Linuxのサポートは、そのアップストリームサポートが2021年12月31日に終了するため、計画されていません。
> -   Ubuntu 16.04のサポートは、TiDBの将来のバージョンで削除される予定です。 Ubuntu18.04以降にアップグレードすることを強くお勧めします。

DebianLinuxやFedoraLinuxなどの他のLinuxOSバージョンは動作する可能性がありますが、公式にはサポートされていません。

## ソフトウェアの推奨事項 {#software-recommendations}

### 制御機 {#control-machine}

| ソフトウェア  | バージョン   |
| :------ | :------ |
| sshpass | 1.06以降  |
| TiUP    | 1.5.0以降 |

> **ノート：**
>
> [制御マシンにTiUPを展開します](/production-deployment-using-tiup.md#step-2-install-tiup-on-the-control-machine)クラスターを運用および管理する必要があります。

### ターゲットマシン {#target-machines}

| ソフトウェア  | バージョン    |
| :------ | :------- |
| sshpass | 1.06以降   |
| numa    | 2.0.12以降 |
| タール     | どれか      |

## サーバーの推奨事項 {#server-recommendations}

TiDBは、Intel x86-64アーキテクチャの64ビット汎用ハードウェアサーバープラットフォーム、またはARMアーキテクチャのハードウェアサーバープラットフォームにデプロイして実行できます。開発、テスト、および実稼働環境でのサーバーハードウェア構成（オペレーティングシステム自体が占有するリソースを無視する）に関する要件と推奨事項は次のとおりです。

### 開発およびテスト環境 {#development-and-test-environments}

|    成分   |  CPU  |   メモリー  |   ローカルストレージ  |       通信網      |     インスタンス番号（最小要件）     |
| :-----: | :---: | :-----: | :----------: | :------------: | :--------------------: |
|   TiDB  |  8コア+ | 16 GB + |  特別な要件はありません | ギガビットネットワークカード |  1（PDと同じマシンにデプロイできます）  |
|    PD   |  4コア+ |  8GB以上  |  SAS、200GB以上 | ギガビットネットワークカード | 1（TiDBと同じマシンにデプロイできます） |
|   TiKV  |  8コア+ | 32 GB + |  SAS、200GB以上 | ギガビットネットワークカード |            3           |
| TiFlash | 32コア+ | 64 GB + | SSD、200 GB + | ギガビットネットワークカード |            1           |
|  TiCDC  |  8コア+ | 16 GB + |  SAS、200GB以上 | ギガビットネットワークカード |            1           |

> **ノート：**
>
> -   テスト環境では、TiDBインスタンスとPDインスタンスを同じサーバーにデプロイできます。
> -   パフォーマンス関連のテストでは、テスト結果の正確性を保証するために、パフォーマンスの低いストレージおよびネットワークハードウェア構成を使用しないでください。
> -   TiKVサーバーの場合、読み取りと書き込みを高速化するためにNVMeSSDを使用することをお勧めします。
> -   機能のテストと検証のみを行う場合は、 [TiDBのクイックスタートガイド](/quick-start-with-tidb.md)に従ってTiDBを単一のマシンに展開します。
> -   TiDBサーバーはディスクを使用してサーバーログを保存するため、テスト環境でのディスクの種類と容量に関する特別な要件はありません。

### 本番環境 {#production-environment}

|    成分   |  CPU  |   メモリー   | ハードディスクの種類 |           通信網          | インスタンス番号（最小要件） |
| :-----: | :---: | :------: | :--------: | :--------------------: | :------------: |
|   TiDB  | 16コア+ |  48 GB + |     SAS    | 10ギガビットネットワークカード（2枚推奨） |        2       |
|    PD   |  8コア+ |  16 GB + |     SSD    | 10ギガビットネットワークカード（2枚推奨） |        3       |
|   TiKV  | 16コア+ |  64 GB + |     SSD    | 10ギガビットネットワークカード（2枚推奨） |        3       |
| TiFlash | 48コア+ | 128 GB + |  1つ以上のSSD  | 10ギガビットネットワークカード（2枚推奨） |        2       |
|  TiCDC  | 16コア+ |  64 GB + |     SSD    | 10ギガビットネットワークカード（2枚推奨） |        2       |
|   モニター  |  8コア+ |  16 GB + |     SAS    |     ギガビットネットワークカード     |        1       |

> **ノート：**
>
> -   実稼働環境では、TiDBインスタンスとPDインスタンスを同じサーバーにデプロイできます。パフォーマンスと信頼性に対する要件が高い場合は、それらを別々に展開してみてください。
> -   実稼働環境では、より高い構成を使用することを強くお勧めします。
> -   PCIeSSDを使用している場合はTiKVハードディスクのサイズを2TB以内に、通常のSSDを使用している場合は1.5TB以内に保つことをお勧めします。

TiFlashを展開する前に、次の点に注意してください。

-   TiFlashは[複数のディスクに展開](/tiflash/tiflash-configuration.md#multi-disk-deployment)にすることができます。
-   TiKVデータのリアルタイムレプリケーションをバッファリングするために、TiFlashデータディレクトリの最初のディスクとして高性能SSDを使用することをお勧めします。このディスクのパフォーマンスは、PCI-ESSDなどのTiKVのパフォーマンスより低くすることはできません。ディスク容量は、合計容量の10％以上である必要があります。そうしないと、このノードのボトルネックになる可能性があります。通常のSSDを他のディスクに展開できますが、PCI-ESSDが優れているとパフォーマンスが向上することに注意してください。
-   TiKVとは異なるノードにTiFlashを展開することをお勧めします。 TiFlashとTiKVを同じノードにデプロイする必要がある場合は、CPUコアとメモリの数を増やし、TiFlashとTiKVを異なるディスクにデプロイして、相互に干渉しないようにしてください。
-   TiFlashディスクの総容量は次のように計算されます： `the data volume of the entire TiKV cluster to be replicated / the number of TiKV replicas * the number of TiFlash replicas` 。たとえば、TiKVの全体的な計画容量が1 TB、TiKVレプリカの数が3、TiFlashレプリカの数が2の場合、TiFlashの推奨される合計容量は`1024 GB / 3 * 2`です。一部のテーブルのデータのみを複製できます。このような場合は、複製するテーブルのデータ量に応じてTiFlashの容量を決定してください。

TiCDCを展開する前に、1TBを超えるPCIe-SSDディスクにTiCDCを展開することをお勧めします。

## ネットワーク要件 {#network-requirements}

オープンソースの分散NewSQLデータベースとして、TiDBを実行するには次のネットワークポート構成が必要です。管理者は、実際の環境でのTiDBの展開に基づいて、ネットワーク側とホスト側で関連するポートを開くことができます。

|         成分        | デフォルトポート | 説明                                              |
| :---------------: | :------: | :---------------------------------------------- |
|        TiDB       |   4000   | アプリケーションおよびDBAツールの通信ポート                         |
|        TiDB       |   10080  | TiDBステータスを報告するための通信ポート                          |
|        TiKV       |   20160  | TiKV通信ポート                                       |
|        TiKV       |   20180  | TiKVステータスを報告するための通信ポート                          |
|         PD        |   2379   | TiDBとPD間の通信ポート                                  |
|         PD        |   2380   | PDクラスタ内のノード間通信ポート                               |
|      TiFlash      |   9000   | TiFlashTCPサービスポート                               |
|      TiFlash      |   8123   | TiFlashHTTPサービスポート                              |
|      TiFlash      |   3930   | TiFlashRAFTおよびコプロセッサーサービスポート                    |
|      TiFlash      |   20170  | TiFlashプロキシサービスポート                              |
|      TiFlash      |   20292  | PrometheusがTiFlashプロキシメトリックをプルするためのポート          |
|      TiFlash      |   8234   | PrometheusがTiFlashメトリックをプルするためのポート              |
|        ポンプ        |   8250   | ポンプ通信ポート                                        |
|       ドレイナー       |   8249   | ドレイナー通信ポート                                      |
|       TiCDC       |   8300   | TiCDC通信ポート                                      |
|       プロメテウス      |   9090   | Prometheusサービスの通信ポート                            |
|   Node_exporter   |   9100   | すべてのTiDBクラスタノードのシステム情報を報告するための通信ポート             |
| Blackbox_exporter |   9115   | TiDBクラスタのポートを監視するために使用されるBlackbox_exporter通信ポート |
|      Grafana      |   3000   | 外部Web監視サービスおよびクライアント（ブラウザ）アクセス用のポート             |
|    Alertmanager   |   9093   | アラートWebサービスのポート                                 |
|    Alertmanager   |   9094   | アラート通信ポート                                       |

## Webブラウザの要件 {#web-browser-requirements}

TiDBは、データベースメトリックの視覚化を提供するために[Grafana](https://grafana.com/)に依存しています。 Javascriptが有効になっているInternetExplorer、Chrome、またはFirefoxの最近のバージョンで十分です。
