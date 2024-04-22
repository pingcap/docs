---
title: Software and Hardware Recommendations
summary: TiDBは、Intelアーキテクチャサーバー、ARMアーキテクチャサーバー、および主要な仮想化環境に導入でき、ほとんどの主要なハードウェアネットワークとLinuxオペレーティングシステムをサポートしています。TiDBは、オペレーティングシステムとCPUアーキテクチャのさまざまな組み合わせに対してマルチレベルの品質基準を保証し、エンタープライズレベルの本番品質を提供します。また、TiDBのコンパイルと実行にはGolang 1.21以降、さび夜間-2022-07-31以降、GCC 7.x、LLVM 13.0以降が必要です。TiDBの実行にはglibc (2.28-151.el8バージョン)が必要です。
---

# ソフトウェアとハ​​ードウェアの推奨事項 {#software-and-hardware-recommendations}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

TiDB は、高性能のオープンソース分散 SQL データベースとして、Intelアーキテクチャサーバー、ARMアーキテクチャサーバー、および主要な仮想化環境に導入でき、良好に動作します。 TiDB は、ほとんどの主要なハードウェア ネットワークと Linux オペレーティング システムをサポートしています。

## OS とプラットフォームの要件 {#os-and-platform-requirements}

v7.5 LTS では、TiDB はオペレーティング システムと CPU アーキテクチャのさまざまな組み合わせに対してマルチレベルの品質基準を保証します。

-   以下のオペレーティング システムと CPU アーキテクチャの組み合わせに対して、TiDB は**エンタープライズ レベルの本番品質を提供し**、製品機能は包括的かつ体系的に検証されています。

    <table><thead><tr><th>オペレーティングシステム</th><th>サポートされている CPU アーキテクチャ</th></tr></thead><tbody><tr><td>Red Hat Enterprise Linux 8.4 以降の 8.x バージョン</td><td><ul><li>x86_64</li><li>アーム64</li></ul></td></tr><tr><td><ul><li> Red Hat Enterprise Linux 7.3 以降の 7.x バージョン</li><li>CentOS 7.3 以降 7.x バージョン</li></ul></td><td><ul><li>x86_64</li><li>アーム64</li></ul></td></tr><tr><td>アマゾン リナックス 2</td><td><ul><li> x86_64</li><li>アーム64</li></ul></td></tr><tr><td> Rocky Linux 9.1以降</td><td><ul><li>x86_64</li><li>アーム64</li></ul></td></tr><tr><td>キリン オイラー V10 SP1/SP2</td><td><ul><li> x86_64</li><li>アーム64</li></ul></td></tr><tr><td>ユニオンテック OS (UOS) V20</td><td><ul><li> x86_64</li><li>アーム64</li></ul></td></tr><tr><td> openEuler 22.03 LTS SP1</td><td><ul><li> x86_64</li><li>アーム64</li></ul></td></tr></tbody></table>

    > **注記：**
    >
    > [CentOS Linux EOL](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 8 のアップストリーム サポートは 2021 年 12 月 31 日に終了しました。CentOS Stream 8 は引き続き CentOS 組織によってサポートされます。

-   以下のオペレーティング システムと CPU アーキテクチャの組み合わせでは、TiDB をコンパイル、構築、展開できます。さらに、OLTP、OLAP、データ ツールの基本機能も使用できます。ただし、TiDB は**エンタープライズ レベルの本番品質を保証しません**。

    <table><thead><tr><th>オペレーティングシステム</th><th>サポートされている CPU アーキテクチャ</th></tr></thead><tbody><tr><td>macOS 12 (モントレー) 以降</td><td><ul><li>x86_64</li><li>アーム64</li></ul></td></tr><tr><td> Oracle Enterprise Linux 7.3 以降の 7.x バージョン</td><td>x86_64</td></tr><tr><td> Ubuntu LTS 18.04以降</td><td>x86_64</td></tr><tr><td> CentOS 8 ストリーム</td><td><ul><li>x86_64</li><li>アーム64</li></ul></td></tr><tr><td> Debian 9 (ストレッチ) 以降</td><td>x86_64</td></tr><tr><td> Fedora 35 以降</td><td>x86_64</td></tr><tr><td> openSUSE Leap v15.3 以降 (Tumbleweed を除く)</td><td> x86_64</td></tr><tr><td> SUSE Linux エンタープライズ サーバー 15</td><td> x86_64</td></tr></tbody></table>

    > **注記：**
    >
    > -   Oracle Enterprise Linux の場合、TiDB は Red Hat Compatibility Kernel (RHCK) をサポートしますが、Oracle Enterprise Linux が提供する Unbreakable Enterprise Kernel はサポートしません。
    > -   Ubuntu 16.04 のサポートは、TiDB の将来のバージョンでは削除される予定です。 Ubuntu 18.04 以降にアップグレードすることを強くお勧めします。

-   前の 2 つの表にリストされているオペレーティング システムの 32 ビット バージョンを使用している場合、TiDB が 32 ビット オペレーティング システムおよび対応する CPUアーキテクチャ上でコンパイル可能、ビルド可能、またはデプロイ可能で**あることは保証されません。**そうでない場合、TiDB は積極的に適応しません。 32 ビット オペレーティング システムに対応します。

-   上記以外のオペレーティング システムのバージョンは動作する可能性がありますが、正式にはサポートされていません。

> **注記：**
>
> -   Oracle Enterprise Linux の場合、TiDB は Red Hat 互換カーネル (RHCK) をサポートしますが、Oracle Enterprise Linux が提供する Unbreakable Enterprise Kernel はサポートしません。
> -   [CentOS Linux EOL](https://www.centos.org/centos-linux-eol/)によると、CentOS Linux 8 のアップストリーム サポートは 2021 年 12 月 31 日に終了しました。CentOS Stream 8 は引き続き CentOS 組織によってサポートされます。
> -   Ubuntu 16.04 のサポートは、TiDB の将来のバージョンでは削除される予定です。 Ubuntu 18.04 以降にアップグレードすることを強くお勧めします。
> -   前の表にリストされているオペレーティング システムの 32 ビット バージョンを使用している場合、TiDB が 32 ビット オペレーティング システムおよび対応する CPUアーキテクチャ上でコンパイル可能、ビルド可能、またはデプロイ可能である**ことは保証されません**。または、TiDB は積極的に適応しません。 32 ビット オペレーティング システム。
> -   上記以外のオペレーティング システムのバージョンは動作する可能性がありますが、正式にはサポートされていません。

### TiDB のコンパイルと実行に必要なライブラリ {#libraries-required-for-compiling-and-running-tidb}

| TiDB のコンパイルと実行に必要なライブラリ | バージョン            |
| :---------------------- | :--------------- |
| Golang                  | 1.21以降           |
| さび                      | 夜間-2022-07-31 以降 |
| GCC                     | 7.x              |
| LLVM                    | 13.0以降           |

TiDB の実行に必要なライブラリ: glibc (2.28-151.el8 バージョン)

### Docker イメージの依存関係 {#docker-image-dependencies}

次の CPU アーキテクチャがサポートされています。

-   x86_64。 TiDB v6.6.0 以降では、 [x84-64-v2 命令セット](https://developers.redhat.com/blog/2021/01/05/building-red-hat-enterprise-linux-9-for-the-x86-64-v2-microarchitecture-level)が必須になります。
-   アーム64

## ソフトウェアの推奨事項 {#software-recommendations}

### 制御機 {#control-machine}

| ソフトウェア | バージョン   |
| :----- | :------ |
| SSHパス  | 1.06以降  |
| TiUP   | 1.5.0以降 |

> **注記：**
>
> TiDB クラスターを操作[制御マシンにTiUPを展開する](/production-deployment-using-tiup.md#step-2-deploy-tiup-on-the-control-machine)管理する必要があります。

### 対象マシン {#target-machines}

| ソフトウェア | バージョン    |
| :----- | :------- |
| SSHパス  | 1.06以降   |
| 沼      | 2.0.12以降 |
| タール    | どれでも     |

## サーバーの推奨事項 {#server-recommendations}

TiDB は、Intel x86-64アーキテクチャの 64 ビット汎用ハードウェアサーバープラットフォーム、または ARMアーキテクチャのハードサーバープラットフォームに展開して実行できます。開発、テスト、本番環境のサーバーハードウェア構成に関する要件と推奨事項 (オペレーティング システム自体が占有するリソースは無視します) は次のとおりです。

### 開発およびテスト環境 {#development-and-test-environments}

|    成分   |   CPU  |   メモリ  |               ローカルストレージ               |       通信網      |     インスタンスの数 (最小要件)    |
| :-----: | :----: | :----: | :-----------------------------------: | :------------: | :--------------------: |
|   TiDB  |  8コア以上 | 16GB以上 | [ディスク容量の要件](#disk-space-requirements) | ギガビットネットワークカード |  1 (PD と同じマシンにデプロイ可能)  |
|    PD   |  4コア以上 |  8GB以上 |              SAS、200GB以上              | ギガビットネットワークカード | 1 (TiDB と同じマシンにデプロイ可能) |
|   TiKV  |  8コア以上 | 32GB以上 |              SAS、200GB以上              | ギガビットネットワークカード |            3           |
| TiFlash | 32コア以上 | 64GB以上 |              SSD、200GB以上              | ギガビットネットワークカード |            1           |
|  TiCDC  |  8コア以上 | 16GB以上 |              SAS、200GB以上              | ギガビットネットワークカード |            1           |

> **注記：**
>
> -   テスト環境では、TiDB インスタンスと PD インスタンスを同じサーバーにデプロイできます。
> -   パフォーマンス関連のテストでは、テスト結果の正確性を保証するために、低パフォーマンスのstorageとネットワーク ハードウェア構成を使用しないでください。
> -   TiKVサーバーの場合、読み取りと書き込みを高速化するために NVMe SSD を使用することをお勧めします。
> -   機能をテストして検証するだけの場合は、 [TiDB クイック スタート ガイド](/quick-start-with-tidb.md)に従って単一マシンに TiDB をデプロイします。
> -   v6.3.0 以降、Linux AMD64アーキテクチャでTiFlash を展開するには、CPU が AVX2 命令セットをサポートする必要があります。 `cat /proc/cpuinfo | grep avx2`に出力があることを確認します。 Linux ARM64アーキテクチャでTiFlashを導入するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`に出力があることを確認します。命令セット拡張を使用することにより、TiFlash のベクトル化エンジンはより優れたパフォーマンスを実現できます。

### 本番環境 {#production-environment}

|    成分   |   CPU  |   メモリ   | ハードディスクの種類 |              通信網             | インスタンスの数 (最小要件) |
| :-----: | :----: | :-----: | :--------: | :--------------------------: | :-------------: |
|   TiDB  | 16コア以上 |  48GB以上 |     SSD    | 10 ギガビット ネットワーク カード (2 枚を推奨) |        2        |
|    PD   |  8コア以上 |  16GB以上 |     SSD    | 10 ギガビット ネットワーク カード (2 枚を推奨) |        3        |
|   TiKV  | 16コア以上 |  64GB以上 |     SSD    | 10 ギガビット ネットワーク カード (2 枚を推奨) |        3        |
| TiFlash | 48コア以上 | 128GB以上 | 1 つ以上の SSD | 10 ギガビット ネットワーク カード (2 枚を推奨) |        2        |
|  TiCDC  | 16コア以上 |  64GB以上 |     SSD    | 10 ギガビット ネットワーク カード (2 枚を推奨) |        2        |
|   モニター  |  8コア以上 |  16GB以上 |     SAS    |        ギガビットネットワークカード        |        1        |

> **注記：**
>
> -   本番環境では、TiDB インスタンスと PD インスタンスを同じサーバーにデプロイできます。パフォーマンスと信頼性に対してより高い要件がある場合は、それらを個別に導入してみてください。
> -   本番環境では、TiDB、TiKV、およびTiFlashをそれぞれ少なくとも 8 個の CPU コアで構成することを強くお勧めします。より良いパフォーマンスを得るには、より高い構成をお勧めします。
> -   TiKV ハードディスクのサイズは、PCIe SSD を使用している場合は 4 TB 以内、通常の SSD を使用している場合は 1.5 TB 以内にすることをお勧めします。

TiFlashを展開する前に、次の点に注意してください。

-   TiFlash は[複数のディスクに展開される](/tiflash/tiflash-configuration.md#multi-disk-deployment)にすることができます。
-   TiKV データのリアルタイム レプリケーションをバッファリングするために、 TiFlashデータ ディレクトリの最初のディスクとして高性能 SSD を使用することをお勧めします。このディスクのパフォーマンスは、PCIe SSD などの TiKV のパフォーマンスよりも低くてはなりません。ディスク容量は総容量の 10% 以上である必要があります。そうしないと、このノードのボトルネックになる可能性があります。他のディスクに通常の SSD を導入することもできますが、より優れた PCIe SSD の方がパフォーマンスが向上することに注意してください。
-   TiFlash をTiKV とは別のノードにデプロイすることをお勧めします。 TiFlashと TiKV を同じノードに展開する必要がある場合は、CPU コアとメモリの数を増やし、相互の干渉を避けるためにTiFlashと TiKV を異なるディスクに展開してみてください。
-   TiFlashディスクの総容量は`the data volume of the entire TiKV cluster to be replicated / the number of TiKV replicas * the number of TiFlash replicas`のように計算されます。たとえば、TiKV の計画全体容量が 1 TB、TiKV レプリカの数が 3、 TiFlashレプリカの数が 2 の場合、 TiFlashの推奨合計容量は`1024 GB / 3 * 2`です。一部のテーブルのデータのみを複製できます。この場合、複製するテーブルのデータ量に応じてTiFlashの容量を決定してください。

TiCDC を展開する前に、500 GB を超える PCIe SSD ディスクに TiCDC を展開することが推奨されることに注意してください。

## ネットワーク要件 {#network-requirements}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

オープンソースの分散 SQL データベースである TiDB を実行するには、次のネットワーク ポート構成が必要です。実際の環境での TiDB 導入に基づいて、管理者はネットワーク側とホスト側で関連するポートを開くことができます。

|        成分       | デフォルトのポート | 説明                                                     |
| :-------------: | :-------: | :----------------------------------------------------- |
|       TiDB      |    4000   | アプリケーションとDBAツール用の通信ポート                                 |
|       TiDB      |   10080   | TiDB ステータスを報告するための通信ポート                                |
|       TiKV      |   20160   | TiKV通信ポート                                              |
|       TiKV      |   20180年  | TiKV ステータスを報告するための通信ポート                                |
|        PD       |    2379   | TiDB と PD 間の通信ポート                                      |
|        PD       |    2380   | PDクラスタ内のノード間通信ポート                                      |
|     TiFlash     |    9000   | TiFlash TCP サービス ポート                                   |
|     TiFlash     |    3930   | TiFlash RAFT およびコプロセッサーサービス ポート                        |
|     TiFlash     |   20170年  | TiFlashプロキシ サービス ポート                                   |
|     TiFlash     |   20292   | Prometheus がTiFlashプロキシ メトリクスをプルするためのポート               |
|     TiFlash     |    8234   | Prometheus がTiFlashメトリクスをプルするためのポート                    |
|       Pump      |    8250   | Pump通信ポート                                              |
|     Drainer     |    8249   | Drainer通信ポート                                           |
|      TiCDC      |    8300   | TiCDC 通信ポート                                            |
|        監視       |    9090   | Prometheus サービスの通信ポート                                  |
|        監視       |   12020   | NgMonitoring サービスの通信ポート                                |
|    ノードエクスポーター   |    9100   | すべての TiDB クラスター ノードのシステム情報を報告するための通信ポート                |
| ブラックボックスエクスポーター |    9115   | Blackbox_exporter 通信ポート。TiDB クラスター内のポートを監視するために使用されます。 |
|      グラファナ      |    3000   | 外部 Web 監視サービスおよびクライアント (ブラウザ) アクセス用のポート                |
|    アラートマネージャー   |    9093   | アラート Web サービスのポート                                      |
|    アラートマネージャー   |    9094   | アラート通信ポート                                              |

## ディスク容量の要件 {#disk-space-requirements}

<table><thead><tr><th>成分</th><th>ディスク容量の要件</th><th>健全なディスク使用量</th></tr></thead><tbody><tr><td>TiDB</td><td><ul><li>ログディスク用に少なくとも 30 GB</li><li> v6.5.0 以降、Fast Online DDL ( <a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_ddl_enable_fast_reorg-new-in-v630">tidb_ddl_enable_fast_reorg</a>変数によって制御される) がデフォルトで有効になり、インデックスの追加などの DDL 操作が高速化されます。大きなオブジェクトを含む DDL 操作がアプリケーションに存在する場合、または<a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into">IMPORT INTO</a>を使用してデータをインポートする場合は、TiDB 用に追加の SSD ディスク領域 (100 GB 以上) を準備することを強くお勧めします。詳細な構成手順については、 <a href="https://docs.pingcap.com/tidb/v7.5/check-before-deployment#set-temporary-spaces-for-tidb-instances-recommended">「TiDB インスタンスの一時スペースを設定する」</a>を参照してください。</li></ul></td><td> 90%未満</td></tr><tr><td>PD</td><td>データ ディスクとログ ディスクにそれぞれ少なくとも 20 GB</td><td> 90%未満</td></tr><tr><td>TiKV</td><td>データ ディスクとログ ディスクにそれぞれ少なくとも 100 GB</td><td> 80%未満</td></tr><tr><td>TiFlash</td><td>データ ディスクには少なくとも 100 GB、ログ ディスクには少なくとも 30 GB それぞれ</td><td>80%未満</td></tr><tr><td>TiUP</td><td><ul><li>コントロール マシン: 単一バージョンの TiDB クラスターをデプロイするのに必要なスペースは 1 GB 以内です。複数のバージョンの TiDB クラスターをデプロイする場合、必要なスペースが増加します。</li><li>デプロイメントサーバー (TiDB コンポーネントが実行されるマシン): TiFlash は約 700 MB のスペースを占有し、他のコンポーネント (PD、TiDB、TiKV など) は約 200 MB のスペースをそれぞれ占有します。クラスター展開プロセス中、 TiUPクラスターは一時ファイルを保存するために 1 MB 未満の一時領域 ( <code>/tmp</code>ディレクトリ) を必要とします。</li></ul></td><td>該当なし</td></tr><tr><td>NGモニタリング</td><td><ul><li>Conprof: 3 x 1 GB x コンポーネントの数 (各コンポーネントは1 日あたり約 1 GB、合計 3 日を占有します) + 20 GB の予約スペース</li><li>Top SQL: 30 x 50 MB x コンポーネントの数 (各コンポーネントは1 日あたり約 50 MB、合計 30 日を占有します)</li><li> Conprof とTop SQL は予約スペースを共有します</li></ul></td><td>該当なし</td></tr></tbody></table>

## Web ブラウザの要件 {#web-browser-requirements}

TiDB は[グラファナ](https://grafana.com/)に依存してデータベース メトリックの視覚化を提供します。 Javascript が有効になっている最新バージョンの Internet Explorer、Chrome、または Firefox で十分です。

## TiFlashの分散storageおよびコンピューティングアーキテクチャのハードウェアおよびソフトウェア要件 {#hardware-and-software-requirements-for-tiflash-disaggregated-storage-and-compute-architecture}

前述のTiFlashソフトウェアおよびハードウェア要件は、結合されたstorageとコンピューティングアーキテクチャに関するものです。 v7.0.0 以降、 TiFlash は[細分化されたstorageとコンピューティングアーキテクチャ](/tiflash/tiflash-disaggregated-and-s3.md)をサポートします。このアーキテクチャでは、 TiFlash は書き込みノードと計算ノードの 2 種類のノードに分割されます。これらのノードの要件は次のとおりです。

-   ソフトウェア: 結合されたstorageとコンピューティングアーキテクチャと同じままです[OS とプラットフォームの要件](#os-and-platform-requirements)を参照してください。
-   ネットワーク ポート: 結合されたstorageとコンピューティングアーキテクチャと同じままです。1 [通信網](#network-requirements)参照してください。
-   ディスクスペース：
    -   TiFlash書き込みノード: データを Amazon S3 にアップロードする前に、 TiFlashレプリカを追加したりリージョンレプリカを移行したりするときにローカル バッファとして使用される、少なくとも 200 GB のディスク領域を設定することをお勧めします。また、Amazon S3 と互換性のあるオブジェクトstorageが必要です。
    -   TiFlashコンピューティング ノード: 少なくとも 100 GB のディスク領域を構成することをお勧めします。これは主に、パフォーマンスを向上させるために書き込みノードから読み取ったデータをキャッシュするために使用されます。計算ノードのキャッシュが完全に使用される場合がありますが、これは正常です。
-   CPU とメモリの要件については、次のセクションで説明します。

### 開発およびテスト環境 {#development-and-test-environments}

| 成分                   | CPU    | メモリ    | ローカルストレージ   | 通信網         | インスタンスの数 (最小要件) |
| -------------------- | ------ | ------ | ----------- | ----------- | --------------- |
| TiFlash書き込みノード       | 16コア以上 | 32GB以上 | SSD、200GB以上 | ギガビットイーサネット | 1               |
| TiFlashコンピューティング ノード | 16コア以上 | 32GB以上 | SSD、100GB以上 | ギガビットイーサネット | 0 (次の注を参照)      |

### 本番環境 {#production-environment}

| 成分                   | CPU    | メモリ    | ディスクの種類    | 通信網                      | インスタンスの数 (最小要件) |
| -------------------- | ------ | ------ | ---------- | ------------------------ | --------------- |
| TiFlash書き込みノード       | 32コア以上 | 64GB以上 | 1 つ以上の SSD | 10 ギガビット イーサネット (2 つを推奨) | 1               |
| TiFlashコンピューティング ノード | 32コア以上 | 64GB以上 | 1 つ以上の SSD | 10 ギガビット イーサネット (2 つを推奨) | 0 (次の注を参照)      |

> **注記：**
>
> TiUPなどのデプロイメント ツールを使用すると、 TiFlashコンピューティング ノードを`[0, +inf]`の範囲内で迅速にスケールインまたはスケールアウトできます。
