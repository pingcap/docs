---
title: Deployment FAQs
summary: Learn about the FAQs related to TiDB deployment.
---

# 展開に関するFAQ {#deployment-faqs}

このドキュメントは、TiDBの展開に関連するFAQをまとめたものです。

## オペレーティングシステム要件 {#operating-system-requirements}

### 必要なオペレーティングシステムのバージョンは何ですか？ {#what-are-the-required-operating-system-versions}

|         Linux OS         |     バージョン     |
| :----------------------: | :-----------: |
| Red Hat Enterprise Linux | 7.3以降の7.xリリース |
|          CentOS          | 7.3以降の7.xリリース |
|  Oracle Enterprise Linux | 7.3以降の7.xリリース |
|       Amazon Linux       |       2       |
|        Ubuntu LTS        |    16.04以降    |

### CentOS 7にTiDBクラスタをデプロイすることが推奨されるのはなぜですか？ {#why-it-is-recommended-to-deploy-the-tidb-cluster-on-centos-7}

高性能のオープンソース分散NewSQLデータベースとして、TiDBはIntelアーキテクチャサーバーおよび主要な仮想化環境に展開でき、適切に実行されます。 TiDBは、ほとんどの主要なハードウェアネットワークとLinuxオペレーティングシステムをサポートしています。詳細については、TiDBの展開について[公式の展開要件](/hardware-and-software-requirements.md)を参照してください。

多くのTiDBテストがCentOS7.3で実行され、多くの展開のベストプラクティスがCentOS7.3に蓄積されています。したがって、TiDBをデプロイするときは、CentOS7.3+Linuxオペレーティングシステムを使用することをお勧めします。

## サーバー要件 {#server-requirements}

Intelx86-64アーキテクチャの64ビット汎用ハードウェアサーバープラットフォームにTiDBを展開して実行できます。開発、テスト、および実稼働環境のサーバーハードウェア構成に関する要件と推奨事項は次のとおりです。

### 開発およびテスト環境 {#development-and-testing-environments}

|    成分   |  CPU  |   メモリー  |   ローカルストレージ  |       通信網      |     インスタンス番号（最小要件）     |
| :-----: | :---: | :-----: | :----------: | :------------: | :--------------------: |
|   TiDB  |  8コア+ |  16GB以上 | SAS、200 GB + | ギガビットネットワークカード |   1（PDと同じマシンに展開できます）   |
|    PD   |  4コア+ |  8GB以上  | SAS、200 GB + | ギガビットネットワークカード | 1（TiDBと同じマシンにデプロイできます） |
|   TiKV  |  8コア+ | 32 GB + | SAS、200 GB + | ギガビットネットワークカード |            3           |
| TiFlash | 32コア+ |  64GB以上 | SSD、200 GB + | ギガビットネットワークカード |            1           |
|  TiCDC  |  8コア+ |  16GB以上 | SAS、200 GB + | ギガビットネットワークカード |            1           |
|         |       |         |              |     サーバーの総数    |            6           |

### 本番環境 {#production-environment}

|    成分   |  CPU  |   メモリー   | ハードディスクの種類 |           通信網          | インスタンス番号（最小要件） |
| :-----: | :---: | :------: | :--------: | :--------------------: | :------------: |
|   TiDB  | 16コア+ |  48 GB + |     SAS    | 10ギガビットネットワークカード（2枚推奨） |        2       |
|    PD   |  8コア+ |  16GB以上  |     SSD    | 10ギガビットネットワークカード（2枚推奨） |        3       |
|   TiKV  | 16コア+ |  64GB以上  |     SSD    | 10ギガビットネットワークカード（2枚推奨） |        3       |
| TiFlash | 48コア+ | 128 GB + |  1つ以上のSSD  | 10ギガビットネットワークカード（2枚推奨） |        2       |
|  TiCDC  | 16コア+ |  64GB以上  |     SSD    | 10ギガビットネットワークカード（2枚推奨） |        2       |
|   モニター  |  8コア+ |  16GB以上  |     SAS    |     ギガビットネットワークカード     |        1       |
|         |       |          |            |         サーバーの総数        |       13       |

### 10ギガビットの2つのネットワークカードの目的は何ですか？ {#what-s-the-purposes-of-2-network-cards-of-10-gigabit}

分散クラスタとして、PDは一意のタイムスタンプを配布する必要があるため、TiDBは、特にPDに対して時間に対する需要が高くなります。 PDサーバーの時間が一定していないと、PDサーバーの切り替え時の待ち時間が長くなります。 2枚のネットワークカードを結合することでデータ伝送の安定性が保証され、10ギガビットが伝送速度を保証します。ギガビットネットワークカードはボトルネックになりやすいため、10ギガビットネットワークカードを使用することを強くお勧めします。

### SSDにRAIDを使用しない場合は可能ですか？ {#is-it-feasible-if-we-don-t-use-raid-for-ssd}

リソースが十分な場合は、SSDにRAID10を使用することをお勧めします。リソースが不十分な場合は、SSDにRAIDを使用しないことをお勧めします。

### TiDBコンポーネントの推奨構成は何ですか？ {#what-s-the-recommended-configuration-of-tidb-components}

-   TiDBには、CPUとメモリに対する高い要件があります。 TiDB Binlogを有効にする必要がある場合は、サービスボリュームの見積もりとGC操作の時間要件に基づいて、ローカルディスク容量を増やす必要があります。ただし、SSDディスクは必須ではありません。
-   PDはクラスタメタデータを格納し、頻繁に読み取りおよび書き込み要求を行います。高いI/Oディスクが必要です。パフォーマンスの低いディスクは、クラスタ全体のパフォーマンスに影響します。 SSDディスクの使用をお勧めします。さらに、リージョンの数が多いほど、CPUとメモリに対する要件が高くなります。
-   TiKVには、CPU、メモリ、およびディスクに対する高い要件があります。 SSDを使用する必要があります。

詳細については、 [ソフトウェアとハードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

## インストールと展開 {#installation-and-deployment}

実稼働環境では、 [TiUP](/tiup/tiup-overview.md)を使用してTiDBクラスタをデプロイすることをお勧めします。 [TiUPを使用してTiDBクラスターをデプロイする](/production-deployment-using-tiup.md)を参照してください。

### TiKV / PDの変更された<code>toml</code>構成が有効にならないのはなぜですか？ {#why-the-modified-code-toml-code-configuration-for-tikv-pd-does-not-take-effect}

`toml`の構成を有効にするには、TiKV/PDで`--config`つのパラメーターを設定する必要があります。 TiKV / PDは、デフォルトでは構成を読み取りません。現在、この問題はBinaryを使用してデプロイする場合にのみ発生します。 TiKVの場合は、構成を編集してサービスを再起動します。 PDの場合、構成ファイルはPDが初めて開始されたときにのみ読み取られ、その後pd-ctlを使用して構成を変更できます。詳細については、 [PD Controlユーザーガイド](/pd-control.md)を参照してください。

### TiDBモニタリングフレームワーク（Prometheus + Grafana）をスタンドアロンマシンまたは複数のマシンにデプロイする必要がありますか？推奨されるCPUとメモリは何ですか？ {#should-i-deploy-the-tidb-monitoring-framework-prometheus-grafana-on-a-standalone-machine-or-on-multiple-machines-what-is-the-recommended-cpu-and-memory}

監視マシンは、スタンドアロン展開を使用することをお勧めします。 16GB以上のメモリと500GB以上のハードディスクを備えた8コアCPUを使用することをお勧めします。

### モニターがすべてのメトリックを表示できないのはなぜですか？ {#why-the-monitor-cannot-display-all-metrics}

モニターのマシン時間とクラスタ内の時間の時間差を確認してください。大きい場合は、時間を修正すると、モニターにすべてのメトリックが表示されます。

### supervise / svc / svstatサービスの機能は何ですか？ {#what-is-the-function-of-supervise-svc-svstat-service}

-   監督：プロセスを管理するためのデーモンプロセス
-   svc：サービスを開始および停止します
-   svstat：プロセスステータスを確認します

### Inventory.ini変数の説明 {#description-of-inventory-ini-variables}

| 変数                      | 説明                                                                                                         |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- |
| `cluster_name`          | クラスタの名前、調整可能                                                                                               |
| `tidb_version`          | TiDBのバージョン                                                                                                 |
| `deployment_method`     | デプロイ方法、デフォルトではバイナリ、Dockerはオプション                                                                            |
| `process_supervision`   | プロセスの監視方法（デフォルトではsystemd）、オプションの監視                                                                         |
| `timezone`              | 管理対象ノードのタイムゾーン、調整可能、デフォルトでは`Asia/Shanghai`変数で`set_timezone`                                                |
| `set_timezone`          | 管理対象ノードのタイムゾーンを編集します。デフォルトではTrueです。 Falseは閉じることを意味します                                                      |
| `enable_elk`            | 現在サポートされていません                                                                                              |
| `enable_firewalld`      | ファイアウォールを有効にするには、デフォルトで閉じています                                                                              |
| `enable_ntpd`           | 管理対象ノードのNTPサービスを監視します。デフォルトではTrueです。閉じないでください                                                              |
| `machine_benchmark`     | 管理対象ノードのディスクIOPSを監視します。デフォルトではTrueです。閉じないでください                                                             |
| `set_hostname`          | IPに基づいて管理対象ノードのホスト名を編集するには、デフォルトではFalseです。                                                                 |
| `enable_binlog`         | Kafkaクラスタに応じて、 Pumpをデプロイしてbinlogを有効にするかどうか（デフォルトではFalse）。 `zookeeper_addrs`変数を参照してください                     |
| `zookeeper_addrs`       | binlogKafkaクラスタのZooKeeperアドレス                                                                              |
| `enable_slow_query_log` | TiDBの遅いクエリログを単一のファイルに記録するには：（{{deploy_dir}} / log / tidb_slow_query.log）。デフォルトではFalseで、TiDBログに記録します        |
| `deploy_without_tidb`   | Key-Valueモードでは、PD、TiKV、および監視サービスのみを展開し、TiDBは展開しません。 `inventory.ini`のファイルでtidb_serversホストグループのIPをnullに設定します |

### 遅いクエリログをTiDBに個別に記録するにはどうすればよいですか？遅いクエリのSQLステートメントを見つける方法は？ {#how-to-separately-record-the-slow-query-log-in-tidb-how-to-locate-the-slow-query-sql-statement}

1.  TiDBの低速クエリ定義は、TiDB構成ファイルにあります。 `slow-threshold: 300`パラメーターは、低速クエリのしきい値（単位：ミリ秒）を構成するために使用されます。

2.  遅いクエリが発生した場合、Grafanaを使用して、遅いクエリがある`tidb-server`つのインスタンスと遅いクエリの時点を特定し、対応するノードのログに記録されているSQLステートメント情報を見つけることができます。

3.  ログに加えて、 `admin show slow`コマンドを使用して遅いクエリを表示することもできます。詳細については、 [`admin show slow`コマンド](/identify-slow-queries.md#admin-show-slow-command)を参照してください。

### TiDBクラスタを初めてデプロイしたときにTiKVの<code>label</code>が構成されていない場合、 <code>label</code>構成を追加するにはどうすればよいですか？ {#how-to-add-the-code-label-code-configuration-if-code-label-code-of-tikv-was-not-configured-when-i-deployed-the-tidb-cluster-for-the-first-time}

TiDB `label`の構成は、クラスタ展開アーキテクチャに関連しています。これは重要であり、PDがグローバルな管理とスケジューリングを実行するための基礎となります。以前にクラスタをデプロイするときに`label`を構成しなかった場合は、PD管理ツール`pd-ctl` （たとえば、 `config set location-labels "zone,rack,host"` ）を使用して`location-labels`の情報を手動で追加することにより、デプロイメント構造を調整する必要があります（実際の`label`レベル名に基づいて構成する必要があります）。

`pd-ctl`の使用法については、 [PD Controlユーザーガイド](/pd-control.md)を参照してください。

### ディスクテストの<code>dd</code>コマンドが<code>oflag=direct</code>オプションを使用するのはなぜですか？ {#why-does-the-code-dd-code-command-for-the-disk-test-use-the-code-oflag-direct-code-option}

ダイレクトモードは、書き込み要求をI / Oコマンドにラップし、このコマンドをディスクに送信して、ファイルシステムキャッシュをバイパスし、ディスクの実際のI/O読み取り/書き込みパフォーマンスを直接テストします。

### <code>fio</code>コマンドを使用してTiKVインスタンスのディスクパフォーマンスをテストするにはどうすればよいですか？ {#how-to-use-the-code-fio-code-command-to-test-the-disk-performance-of-the-tikv-instance}

-   ランダム読み取りテスト：

    {{< copyable "" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randread -size=10G -filename=fio_randread_test.txt -name='fio randread test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_result.json
    ```

-   シーケンシャル書き込みとランダム読み取りの混合テスト：

    {{< copyable "" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randrw -percentage_random=100,0 -size=10G -filename=fio_randread_write_test.txt -name='fio mixed randread and sequential write test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_write_test.json
    ```
