---
title: TiDB Software and Hardware Requirements
summary: TiDB を展開および実行するためのソフトウェアとハードウェアの推奨事項について説明します。
---

# TiDB のソフトウェアおよびハードウェア要件 {#tidb-software-and-hardware-requirements}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

このドキュメントでは、TiDBデータベースの導入と実行に必要なソフトウェアおよびハードウェア要件について説明します。TiDBは、高性能なオープンソースの分散SQLデータベースであり、Intelアーキテクチャサーバー、ARMアーキテクチャサーバー、および主要な仮想化環境に導入でき、良好な動作を実現します。TiDBは、主要なハードウェアネットワークとLinuxオペレーティングシステムのほとんどをサポートしています。

## OSおよびプラットフォームの要件 {#os-and-platform-requirements}

v8.5 LTS では、TiDB はオペレーティング システムと CPU アーキテクチャのさまざまな組み合わせに対して複数レベルの品質標準を保証します。

-   TiDB は、次のオペレーティング システムと CPU アーキテクチャの組み合わせに対して**エンタープライズ レベルの本番品質を提供し**、製品機能は包括的かつ体系的に検証されています。

    <table><thead><tr><th>オペレーティングシステム</th><th>サポートされているCPUアーキテクチャ</th></tr></thead><tbody><tr><td>Red Hat Enterprise Linux 8.4 以降の 8.x バージョン</td><td><ul><li>x86_64</li><li> ARM64</li></ul></td></tr><tr><td>アマゾン リナックス 2</td><td><ul><li> x86_64</li><li> ARM64</li></ul></td></tr><tr><td> Amazon Linux 2023</td><td><ul><li> x86_64</li><li> ARM64</li></ul></td></tr><tr><td> Rocky Linux 9.1 以降</td><td><ul><li>x86_64</li><li> ARM64</li></ul></td></tr><tr><td> Kylin V10 SP1/SP2/SP3 (SP3はv7.5.5以降でサポートされます)</td><td><ul><li> x86_64</li><li> ARM64</li></ul></td></tr><tr><td>ユニオンテック OS (UOS) V20</td><td><ul><li> x86_64</li><li> ARM64</li></ul></td></tr><tr><td>オープンオイラー 22.03 LTS SP1/SP3</td><td><ul><li> x86_64</li><li> ARM64</li></ul></td></tr></tbody></table>

    > **警告：**
    >
    > -   [CentOS Linux のサポート終了](https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/)によると、CentOS Linux 7 のアップストリームサポートは 2024 年 6 月 30 日に終了しました。
    >     -   TiDBをアップグレードする前に、オペレーティングシステムのバージョンを必ずご確認ください。TiDB v8.4.0 DMRおよびv8.5.0では、glibc 2.17のサポートが削除され、CentOS Linux 7でのサポートとテストも終了しました。Rocky Linux 9.1以降のバージョンを使用することをお勧めします。CentOS 7上のTiDBクラスターをv8.4.0またはv8.5.0にアップグレードすると、クラスターが利用できなくなるリスクがあります。
    >     -   v8.5.1 以降、CentOS Linux 7 を引き続き使用しているユーザーを支援するために、TiDB は glibc 2.17 のサポートを再開し、CentOS Linux 7 のテストも再開し、CentOS Linux 7 と互換性を持つようになりました。ただし、CentOS Linux は EOL 状態であるため、CentOS Linux 7 の[公式発表とセキュリティガイダンス](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol)確認し、本番での使用には Rocky Linux 9.1 以降など、TiDB がサポートするオペレーティング システムに移行することを強くお勧めします。
    > -   [Red Hat Enterprise Linux ライフサイクル](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)によると、Red Hat Enterprise Linux 7のメンテナンスサポートは2024年6月30日に終了しました。TiDBは、8.4 DMRバージョン以降のRed Hat Enterprise Linux 7のサポートを終了します。Rocky Linux 9.1以降のバージョンの使用をお勧めします。Red Hat Enterprise Linux 7上のTiDBクラスタをv8.4.0以降にアップグレードすると、クラスタが使用できなくなります。TiDBをアップグレードする前に、オペレーティングシステムのバージョンを確認してください。

-   以下のオペレーティングシステムとCPUアーキテクチャの組み合わせでは、TiDBをコンパイル、ビルド、デプロイできます。また、OLTP、OLAP、およびデータツールの基本機能もご利用いただけます。ただし、これらの組み合わせは包括的かつ体系的なテストが行​​われていないため、TiDBは**エンタープライズレベルの本番品質を保証するものではありません**。

    <table><thead><tr><th>オペレーティングシステム</th><th>サポートされているCPUアーキテクチャ</th></tr></thead><tbody><tr><td>macOS 12 (Monterey) 以降</td><td><ul><li>x86_64</li><li> ARM64</li></ul></td></tr><tr><td> Oracle Enterprise Linux 8以降</td><td>x86_64</td></tr><tr><td> Ubuntu LTS 20.04以降</td><td>x86_64</td></tr><tr><td> CentOS ストリーム 8</td><td><ul><li> x86_64</li><li> ARM64</li></ul></td></tr><tr><td> Debian 10 (Buster) 以降</td><td>x86_64</td></tr><tr><td> Fedora 38以降</td><td>x86_64</td></tr><tr><td> openSUSE Leap v15.5 以降 (Tumbleweed は含みません)</td><td> x86_64</td></tr><tr><td> SUSE Linux Enterprise Server 15</td><td> x86_64</td></tr></tbody></table>

    > **注記：**
    >
    > -   Oracle Enterprise Linux の場合、TiDB は Red Hat Compatible Kernel (RHCK) をサポートしており、Oracle Enterprise Linux が提供する Unbreakable Enterprise Kernel はサポートしていません。
    > -   Ubuntu 16.04のサポートは、TiDBの将来のバージョンでは削除される予定です。Ubuntu 18.04以降へのアップグレードを強くお勧めします。
    > -   CentOS Stream 8 は、2024 年 5 月 31 日に[ビルドの終了](https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/)到達します。

-   前の 2 つの表に記載されているオペレーティング システムの 32 ビット バージョンを使用している場合、TiDB が 32 ビット オペレーティング システムおよび対応する CPUアーキテクチャ上でコンパイル、ビルド、または展開可能であること**は保証されません**。つまり、TiDB は 32 ビット オペレーティング システムに積極的に適応しません。

-   上記に記載されていない他のオペレーティング システム バージョンも動作する可能性がありますが、公式にはサポートされていません。

### TiDBのコンパイルと実行に必要なライブラリ {#libraries-required-for-compiling-and-running-tidb}

| TiDBのコンパイルと実行に必要なライブラリ | バージョン                 |
| :--------------------- | :-------------------- |
| Golang                 | 1.23以降                |
| さび                     | nightly-2023-12-28 以降 |
| GCC                    | 7.x                   |
| LLVM                   | 17.0以降                |

TiDB の実行に必要なライブラリ: glibc (2.28-151.el8 バージョン)

### Dockerイメージの依存関係 {#docker-image-dependencies}

次の CPU アーキテクチャがサポートされています。

-   x86_64。TiDB v6.6.0以降では、 [x86-64-v2命令セット](https://developers.redhat.com/blog/2021/01/05/building-red-hat-enterprise-linux-9-for-the-x86-64-v2-microarchitecture-level)が必要です。
-   ARM64

## ソフトウェア要件 {#software-requirements}

### 制御機 {#control-machine}

| ソフトウェア | バージョン   |
| :----- | :------ |
| SSHパス  | 1.06以降  |
| TiUP   | 1.5.0以降 |

> **注記：**
>
> [制御マシンにTiUPを展開する](/production-deployment-using-tiup.md#step-2-deploy-tiup-on-the-control-machine)クラスターを操作および管理する必要があります。

### ターゲットマシン {#target-machines}

| ソフトウェア | バージョン    |
| :----- | :------- |
| SSHパス  | 1.06以降   |
| 沼      | 2.0.12以降 |
| タール    | どれでも     |

## サーバー要件 {#server-requirements}

TiDBは、Intel x86-64アーキテクチャの64ビット汎用ハードウェアサーバープラットフォーム、またはARMアーキテクチャのハードサーバープラットフォームに導入および実行できます。開発環境、テスト環境、および本番環境におけるサーバーハードウェア構成に関する要件と推奨事項（オペレーティングシステム自体が占有するリソースは除く）は次のとおりです。

### 開発およびテスト環境 {#development-and-test-environments}

|    成分   |   CPU  |   メモリ   |             ローカルストレージ            |     ネットワーク     |      インスタンス数（最小要件）     |
| :-----: | :----: | :-----: | :------------------------------: | :------------: | :--------------------: |
|   ティドブ  |  8コア以上 | 16 GB以上 | [ストレージ要件](#storage-requirements) | ギガビットネットワークカード |    1 (PDと同じマシンに展開可能)   |
|    PD   |  4コア以上 |  8GB以上  |           SAS、200 GB以上           | ギガビットネットワークカード | 1 (TiDB と同じマシンにデプロイ可能) |
|   ティクブ  |  8コア以上 | 32 GB以上 |           SAS、200 GB以上           | ギガビットネットワークカード |            3           |
| TiFlash | 32コア以上 | 64 GB以上 |           SSD、200 GB以上           | ギガビットネットワークカード |            1           |
|  TiCDC  |  8コア以上 | 16 GB以上 |           SAS、200 GB以上           | ギガビットネットワークカード |            1           |
| TiProxy |  4コア以上 |  8GB以上  |                SAS               | ギガビットネットワークカード |            1           |

> **注記：**
>
> -   テスト環境では、TiDB インスタンスと PD インスタンスを同じサーバーにデプロイできます。
> -   パフォーマンス関連のテストでは、テスト結果の正確性を保証するために、低パフォーマンスのstorageおよびネットワーク ハードウェア構成を使用しないでください。
> -   TiKVサーバーでは、読み取りと書き込みを高速化するために NVMe SSD を使用することをお勧めします。
> -   機能のテストと検証のみを行う場合は、手順[TiDB クイックスタートガイド](/quick-start-with-tidb.md)に従って、TiDB を 1 台のマシンにデプロイします。
> -   v6.3.0以降、Linux AMD64アーキテクチャでTiFlashを展開するには、CPUがAVX2命令セットをサポートしている必要があります。1 `grep avx2 /proc/cpuinfo`出力されていることを確認してください。Linux ARM64アーキテクチャでTiFlashを展開するには、CPUがARMv8命令セットアーキテクチャをサポートしている必要があります。3 `grep 'crc32' /proc/cpuinfo | grep 'asimd'`出力されていることを確認してください。命令セット拡張を使用することで、TiFlashのベクトル化エンジンはより優れたパフォーマンスを発揮できます。

### 生産環境 {#production-environment}

|    成分   |   CPU  |    メモリ   | ハードディスクの種類 |            ネットワーク            | インスタンス数（最小要件） |
| :-----: | :----: | :------: | :--------: | :--------------------------: | :-----------: |
|   ティドブ  | 16コア以上 |  48 GB以上 |     SSD    | 10 ギガビット ネットワーク カード (2 枚を推奨) |       2       |
|    PD   |  8コア以上 |  16 GB以上 |     SSD    | 10 ギガビット ネットワーク カード (2 枚を推奨) |       3       |
|   ティクブ  | 16コア以上 |  64 GB以上 |     SSD    | 10 ギガビット ネットワーク カード (2 枚を推奨) |       3       |
| TiFlash | 48コア以上 | 128 GB以上 |  1台以上のSSD  | 10 ギガビット ネットワーク カード (2 枚を推奨) |       2       |
|  TiCDC  | 16コア以上 |  64 GB以上 |     SSD    | 10 ギガビット ネットワーク カード (2 枚を推奨) |       2       |
|   モニター  |  8コア以上 |  16 GB以上 |     SAS    |        ギガビットネットワークカード        |       1       |
| TiProxy |  8コア以上 |  16 GB以上 |     SAS    | 10 ギガビット ネットワーク カード (2 枚を推奨) |       2       |

> **注記：**
>
> -   本番環境では、TiDBインスタンスとPDインスタンスを同じサーバーにデプロイできます。パフォーマンスと信頼性の要件が高い場合は、別々にデプロイすることをお勧めします。
> -   本番環境では、TiDB、TiKV、 TiFlash をそれぞれ少なくとも 8 個の CPU コアで構成することを強くお勧めします。パフォーマンスを向上させるには、より高い構成をお勧めします。
> -   PCIe SSD を使用している場合は TiKV ハード ディスクのサイズを 4 TB 以内に抑え、通常の SSD を使用している場合は 1.5 TB 以内に抑えることをお勧めします。
> -   AWS、Google Cloud、AzureなどのクラウドプロバイダーにTiKVをデプロイする場合は、TiKVノードにクラウドディスクを使用することをお勧めします。クラウド環境でTiKVインスタンスがクラッシュした場合、ローカルディスク上のデータが失われる可能性があります。

TiFlashを展開する前に、次の点に注意してください。

-   TiFlash は[複数のディスクに展開](/tiflash/tiflash-configuration.md#multi-disk-deployment)になります。
-   TiKVデータのリアルタイムレプリケーションをバッファリングするため、 TiFlashデータディレクトリの最初のディスクには高性能SSDを使用することをお勧めします。このディスクのパフォーマンスは、PCIe SSDなど、TiKVのパフォーマンスよりも低くてはなりません。ディスク容量は総容量の10%以上にする必要があります。そうでないと、このノードのボトルネックになる可能性があります。他のディスクには通常のSSDを使用できますが、高性能なPCIe SSDの方がパフォーマンスが向上することにご注意ください。
-   TiFlash はTiKV とは別のノードにデプロイすることをお勧めします。TiFlash とTiFlashを同じノードにデプロイする必要がある場合は、CPU コア数とメモリを増やし、 TiFlashと TiKV を異なるディスクにデプロイして相互干渉を回避するようにしてください。
-   TiFlashディスクの総容量は、次のように計算されます： `the data volume of the entire TiKV cluster to be replicated / the number of TiKV replicas * the number of TiFlash replicas` 。例えば、TiKV全体の計画容量が1 TB、TiKVレプリカ数が3、 TiFlashレプリカ数が2の場合、推奨されるTiFlashの総容量は`1024 GB / 3 * 2`です。一部のテーブルのデータのみをレプリケートすることもできます。その場合は、レプリケートするテーブルのデータ量に応じてTiFlashの容量を決定してください。

TiCDC を展開する前に、500 GB を超える PCIe SSD ディスクに TiCDC を展開することをお勧めします。

## ネットワーク要件 {#network-requirements}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

オープンソースの分散SQLデータベースであるTiDBを実行するには、以下のネットワークポート設定が必要です。管理者は、実際の環境でのTiDBの導入状況に基づいて、ネットワーク側とホスト側で適切なポートを開くことができます。

|        成分       | デフォルトポート | 説明                                                  |
| :-------------: | :------: | :-------------------------------------------------- |
|       ティドブ      |   4000   | アプリケーションとDBAツールの通信ポート                               |
|       ティドブ      |   10080  | TiDBステータスを報告するための通信ポート                              |
|       TiKV      |   20160  | TiKV通信ポート                                           |
|       ティクブ      |   20180  | TiKVステータスを報告するための通信ポート                              |
|        PD       |   2379   | TiDBとPD間の通信ポート                                      |
|        PD       |   2380   | PDクラスタ内のノード間通信ポート                                   |
|     TiFlash     |   9000   | TiFlash TCPサービスポート                                  |
|     TiFlash     |   3930   | TiFlash RAFTおよびコプロセッサーサービスポート                       |
|     TiFlash     |   20170  | TiFlashプロキシサービスポート                                  |
|     TiFlash     |   20292  | PrometheusがTiFlash Proxyメトリックを取得するためのポート            |
|     TiFlash     |   8234   | PrometheusがTiFlashメトリクスを取得するためのポート                  |
|      TiCDC      |   8300   | TiCDC通信ポート                                          |
|        監視       |   9090   | Prometheusサービスの通信ポート                                |
|        監視       |   12020  | NgMonitoringサービスの通信ポート                              |
|    ノードエクスポーター   |   9100   | 各TiDBクラスタノードのシステム情報を報告するための通信ポート                    |
| ブラックボックスエクスポーター |   9115   | TiDB クラスタ内のポートを監視するために使用される Blackbox_exporter 通信ポート |
|      グラファナ      |   3000   | 外部Web監視サービスとクライアント（ブラウザ）アクセス用のポート                   |
|    アラートマネージャー   |   9093   | アラートウェブサービスのポート                                     |
|    アラートマネージャー   |   9094   | 警報通信ポート                                             |

## ストレージ要件 {#storage-requirements}

<table><thead><tr><th>成分</th><th>ディスク容量要件</th><th>健全なディスク使用率</th></tr></thead><tbody><tr><td>ティドブ</td><td><ul><li>ログディスク用に少なくとも30 GB</li><li> v6.5.0以降では、インデックスの追加などのDDL操作を高速化するために、Fast Online DDL（<a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_ddl_enable_fast_reorg-new-in-v630">tidb_ddl_enable_fast_reorg</a>変数で制御）がデフォルトで有効になっています。アプリケーションに大きなオブジェクトを含むDDL操作がある場合、または<a href="https://docs.pingcap.com/tidb/dev/sql-statement-import-into">IMPORT INTO</a>を使用してデータをインポートする場合は、TiDB用に追加のSSDディスク容量（100GB以上）を用意することを強くお勧めします。詳細な設定手順については、 <a href="https://docs.pingcap.com/tidb/dev/check-before-deployment#set-temporary-spaces-for-tidb-instances-recommended">「TiDBインスタンスの一時領域の設定」を</a>ご覧ください。</li></ul></td><td> 90%未満</td></tr><tr><td>PD</td><td>データディスクとログディスクにはそれぞれ少なくとも20 GB</td><td> 90%未満</td></tr><tr><td>TiKV</td><td>データディスクとログディスクにはそれぞれ少なくとも100 GB</td><td> 80%未満</td></tr><tr><td>TiFlash</td><td>データディスクには少なくとも100 GB、ログディスクには少なくとも30 GB</td><td> 80%未満</td></tr><tr><td>TiUP</td><td><ul><li>制御マシン: 単一バージョンの TiDB クラスターをデプロイする場合、必要な空き容量は 1 GB 以下です。複数バージョンの TiDB クラスターをデプロイする場合は、必要な空き容量が増加します。</li><li>デプロイメントサーバー（TiDBコンポーネントが実行されるマシン）： TiFlashは約700MB、その他のコンポーネント（PD、TiDB、TiKVなど）はそれぞれ約200MBのスペースを占有します。クラスターのデプロイメントプロセス中、 TiUPクラスターは一時ファイルを保存するために1MB未満の一時スペース（ <code>/tmp</code>ディレクトリ）を必要とします。</li></ul></td><td>該当なし</td></tr><tr><td>Ngモニタリング</td><td><ul><li>コンプロフ: 3 x 1 GB x コンポーネント数 (各コンポーネントは1日あたり約1 GB、合計3日間) + 20 GB の予約済みスペース</li><li>Top SQL: 30 x 50 MB x コンポーネント数（各コンポーネントは1日あたり約50 MBを占有し、合計30日間）</li><li> ConprofとTop SQLは予約スペースを共有します</li></ul></td><td>該当なし</td></tr></tbody></table>

TiDBはXFSとExt4ファイルシステムをサポートしています。その他のファイルシステムは本番環境では推奨されません。

## Webブラウザの要件 {#web-browser-requirements}

TiDBはデータベースメトリクスの可視化に[グラファナ](https://grafana.com/)を使用しています。JavaScriptが有効になっている最新バージョンのMicrosoft Edge、Safari、Chrome、またはFirefoxで十分です。

## TiFlash分散storageおよびコンピューティングアーキテクチャのハードウェアおよびソフトウェア要件 {#hardware-and-software-requirements-for-tiflash-disaggregated-storage-and-compute-architecture}

上記のTiFlashソフトウェアおよびハードウェア要件は、storageとコンピューティングを組み合わせたアーキテクチャを対象としています。v7.0.0以降、 TiFlashは[分散型storageおよびコンピューティングアーキテクチャ](/tiflash/tiflash-disaggregated-and-s3.md)をサポートします。このアーキテクチャでは、 TiFlashは書き込みノードとコンピューティングノードの2種類のノードに分割されます。これらのノードの要件は次のとおりです。

-   ソフトウェア: 結合されたstorageとコンピューティングアーキテクチャと同じままです[OSおよびプラットフォームの要件](#os-and-platform-requirements)参照)。
-   ネットワーク ポート: 結合されたstorageおよびコンピューティングアーキテクチャと同じままです[ネットワーク](#network-requirements)参照)。
-   ディスク容量:
    -   TiFlash書き込みノード：少なくとも200GBのディスク容量を設定することをお勧めします。これは、 TiFlashレプリカの追加やリージョンレプリカの移行時に、Amazon S3にデータをアップロードする前にローカルバッファとして使用されます。また、Amazon S3と互換性のあるオブジェクトstorageが必要です。
    -   TiFlashコンピュートノード：少なくとも100GBのディスク容量を設定することをお勧めします。これは主に、書き込みノードから読み取ったデータをキャッシュしてパフォーマンスを向上させるために使用されます。コンピュートノードのキャッシュが完全に使用される場合もありますが、これは正常です。
-   CPU およびメモリの要件については、次のセクションで説明します。

### 開発およびテスト環境 {#development-and-test-environments}

| 成分                  | CPU    | メモリ     | ローカルストレージ    | ネットワーク      | インスタンス数（最小要件） |
| ------------------- | ------ | ------- | ------------ | ----------- | ------------- |
| TiFlash書き込みノード      | 16コア以上 | 32 GB以上 | SSD、200 GB以上 | ギガビットイーサネット | 1             |
| TiFlashコンピューティングノード | 16コア以上 | 32 GB以上 | SSD、100 GB以上 | ギガビットイーサネット | 0（以下の注記を参照）   |

### 生産環境 {#production-environment}

| 成分                  | CPU    | メモリ     | ディスクタイプ  | ネットワーク                   | インスタンス数（最小要件） |
| ------------------- | ------ | ------- | -------- | ------------------------ | ------------- |
| TiFlash書き込みノード      | 32コア以上 | 64 GB以上 | 1台以上のSSD | 10 ギガビット イーサネット (2 個を推奨) | 1             |
| TiFlashコンピューティングノード | 32コア以上 | 64 GB以上 | 1台以上のSSD | 10 ギガビット イーサネット (2 個を推奨) | 0（以下の注記を参照）   |

> **注記：**
>
> TiUPなどのデプロイメント ツールを使用して、 `[0, +inf]`範囲内でTiFlashコンピューティング ノードを迅速にスケールインまたはスケールアウトできます。
