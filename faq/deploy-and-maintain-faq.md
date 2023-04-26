---
title: TiDB Deployment FAQs
summary: Learn about the FAQs related to TiDB deployment.
---

# TiDB 展開に関するよくある質問 {#tidb-deployment-faqs}

このドキュメントは、TiDB の展開に関連する FAQ をまとめたものです。

## ソフトウェアおよびハードウェア要件 {#software-and-hardware-requirements}

### TiDB はどのオペレーティング システムをサポートしていますか? {#what-operating-systems-does-tidb-support}

TiDB がサポートするオペレーティング システムについては、 [ソフトウェアおよびハードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

### 開発、テスト、または本番環境で TiDB クラスターに推奨されるハードウェア構成は何ですか? {#what-is-the-recommended-hardware-configuration-for-a-tidb-cluster-in-the-development-test-or-production-environment}

TiDB は、Intel x86-64アーキテクチャの 64 ビット汎用ハードウェアサーバープラットフォーム、または ARMアーキテクチャのハードサーバープラットフォームにデプロイして実行できます。開発、テスト、および本番環境のサーバーハードウェア構成に関する要件と推奨事項については、 [ソフトウェアおよびハードウェアの推奨事項 - サーバーの推奨事項](/hardware-and-software-requirements.md#server-recommendations)を参照してください。

### 10 ギガビットの 2 枚のネットワーク カードの目的は何ですか? {#what-s-the-purposes-of-2-network-cards-of-10-gigabit}

PD は一意のタイムスタンプを配布する必要があるため、分散クラスターとして、特に PD の場合、TiDB は時間の要求が高くなります。 PD サーバーの時刻が一致していないと、PDサーバーの切り替え時に待ち時間が長くなります。 2 枚のネットワーク カードを結合することでデータ転送の安定性が保証され、10 ギガビットが転送速度を保証します。ギガビット ネットワーク カードはボトルネックになりやすいため、10 ギガビット ネットワーク カードを使用することを強くお勧めします。

### SSD に RAID を使用しなければ実現可能ですか? {#is-it-feasible-if-we-don-t-use-raid-for-ssd}

リソースが十分にある場合は、SSD に RAID 10 を使用することをお勧めします。リソースが不十分な場合は、SSD に RAID を使用しなくてもかまいません。

### TiDB コンポーネントの推奨構成は何ですか? {#what-s-the-recommended-configuration-of-tidb-components}

-   TiDB には、CPU とメモリに関する高い要件があります。 TiDB Binlogを有効にする必要がある場合は、サービス ボリュームの見積もりと GC 操作の所要時間に基づいて、ローカル ディスク領域を増やす必要があります。ただし、SSD ディスクは必須ではありません。
-   PD はクラスター メタデータを格納し、頻繁な読み取りおよび書き込み要求を行います。高 I/O ディスクが必要です。パフォーマンスの低いディスクは、クラスター全体のパフォーマンスに影響します。 SSD ディスクの使用をお勧めします。さらに、リージョンの数が多いほど、CPU とメモリの要件が高くなります。
-   TiKV には、CPU、メモリ、およびディスクに対する高い要件があります。 SSDを使用するために必要です。

詳細については、 [ソフトウェアおよびハードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

## インストールと展開 {#installation-and-deployment}

本番環境では、 [TiUP](/tiup/tiup-overview.md)を使用して TiDB クラスターをデプロイすることをお勧めします。 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)を参照してください。

### TiKV/PD の変更された<code>toml</code>構成が有効にならないのはなぜですか? {#why-the-modified-code-toml-code-configuration-for-tikv-pd-does-not-take-effect}

`toml`設定を有効にするには、TiKV/PD で`--config`パラメータを設定する必要があります。デフォルトでは、TiKV/PD は構成を読み取りません。現在、この問題は Binary を使用してデプロイする場合にのみ発生します。 TiKV の場合は、構成を編集してサービスを再起動します。 PD の場合、設定ファイルは PD が初めて起動されたときにのみ読み込まれます。その後、pd-ctl を使用して設定を変更できます。詳細については、 [PD Controlユーザー ガイド](/pd-control.md)を参照してください。

### TiDB 監視フレームワーク (Prometheus + Grafana) をスタンドアロン マシンまたは複数のマシンにデプロイする必要がありますか?推奨される CPU とメモリは? {#should-i-deploy-the-tidb-monitoring-framework-prometheus-grafana-on-a-standalone-machine-or-on-multiple-machines-what-is-the-recommended-cpu-and-memory}

監視マシンは、スタンドアロン展開を使用することをお勧めします。 16 GB 以上のメモリと 500 GB 以上のハードディスクを備えた 8 コア CPU を使用することをお勧めします。

### モニターがすべてのメトリックを表示できないのはなぜですか? {#why-the-monitor-cannot-display-all-metrics}

モニターのマシン時刻とクラスター内時刻の時差を確認します。サイズが大きい場合は、時間を修正すると、モニターにすべてのメトリックが表示されます。

### supervise/svc/svstat サービスの機能は何ですか? {#what-is-the-function-of-supervise-svc-svstat-service}

-   supervise: プロセスを管理するためのデーモン プロセス
-   svc: サービスの開始と停止
-   svstat: プロセスのステータスを確認する

### inventory.ini 変数の説明 {#description-of-inventory-ini-variables}

| 変数                      | 説明                                                                                                                   |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `cluster_name`          | クラスターの名前、調整可能                                                                                                        |
| `tidb_version`          | TiDB のバージョン                                                                                                          |
| `deployment_method`     | デプロイの方法、デフォルトではバイナリ、オプションの Docker                                                                                    |
| `process_supervision`   | プロセスの監視方法、デフォルトで systemd、supervise オプション                                                                             |
| `timezone`              | 管理対象ノード`set_timezone` `Asia/Shanghai`で使用                                                                             |
| `set_timezone`          | 管理対象ノードのタイムゾーンを編集します。デフォルトは True です。 False は閉じることを意味します                                                              |
| `enable_elk`            | 現在サポートされていません                                                                                                        |
| `enable_firewalld`      | デフォルトで閉じられているファイアウォールを有効にする                                                                                          |
| `enable_ntpd`           | 管理対象ノードの NTP サービスを監視するには、デフォルトで True。閉じないでください                                                                       |
| `machine_benchmark`     | 管理対象ノードのディスク IOPS を監視するには、デフォルトで True。閉じないでください                                                                      |
| `set_hostname`          | IP に基づいて管理対象ノードのホスト名を編集するには、デフォルトで False                                                                             |
| `enable_binlog`         | Pumpをデプロイしてbinlogを有効にするかどうか。デフォルトでは False で、Kafka クラスターに依存します。 `zookeeper_addrs`変数を参照してください                          |
| `zookeeper_addrs`       | binlog Kafka クラスターの ZooKeeper アドレス                                                                                   |
| `enable_slow_query_log` | TiDB のスロー クエリ ログを 1 つのファイル ({{ deploy_dir }}/log/tidb_slow_query.log) に記録します。デフォルトでは False で、TiDB ログに記録します           |
| `deploy_without_tidb`   | Key-Value モードでは、PD、TiKV、および監視サービスのみを展開し、TiDB は展開しません。 `inventory.ini`のファイルで tidb_servers ホスト グループの IP を null に設定します。 |

### 低速クエリ ログを TiDB に個別に記録する方法は?遅いクエリ SQL ステートメントを見つける方法は? {#how-to-separately-record-the-slow-query-log-in-tidb-how-to-locate-the-slow-query-sql-statement}

1.  TiDB のスロー クエリの定義は、TiDB 構成ファイルにあります。 `slow-threshold: 300`パラメータは、スロー クエリのしきい値を設定するために使用されます (単位: ミリ秒)。

2.  スロー クエリが発生した場合、Grafana を使用してスロー クエリが発生した`tidb-server`インスタンスとスロー クエリの時点を特定し、該当するノードのログに記録された SQL ステートメント情報を見つけることができます。

3.  ログに加えて、 `ADMIN SHOW SLOW`コマンドを使用してスロー クエリを表示することもできます。詳細については、 [`ADMIN SHOW SLOW`コマンド](/identify-slow-queries.md#admin-show-slow-command)を参照してください。

### 初めて TiDB クラスターをデプロイしたときに TiKV の<code>label</code>構成されていなかった場合、 <code>label</code>構成を追加する方法を教えてください。 {#how-to-add-the-code-label-code-configuration-if-code-label-code-of-tikv-was-not-configured-when-i-deployed-the-tidb-cluster-for-the-first-time}

TiDB `label`の構成は、クラスター展開アーキテクチャに関連しています。これは、PD がグローバルな管理とスケジューリングを実行するための重要な基盤です。以前にクラスターを展開するときに`label`構成しなかった場合は、PD 管理ツール`pd-ctl`を使用して手動で`location-labels`情報を追加することにより、展開構造を調整する必要があります 7 、たとえば、 `config set location-labels "zone,rack,host"` (実用的な`label`レベル名に基づいて構成する必要があります)。

`pd-ctl`の使い方は[PD Controlユーザー ガイド](/pd-control.md)を参照。

### ディスク テストの<code>dd</code>コマンドが<code>oflag=direct</code>オプションを使用するのはなぜですか? {#why-does-the-code-dd-code-command-for-the-disk-test-use-the-code-oflag-direct-code-option}

ダイレクト モードは、書き込み要求を I/O コマンドにラップし、このコマンドをディスクに送信して、ファイル システム キャッシュをバイパスし、ディスクの実際の I/O 読み取り/書き込みパフォーマンスを直接テストします。

### <code>fio</code>コマンドを使用して TiKV インスタンスのディスク パフォーマンスをテストする方法を教えてください。 {#how-to-use-the-code-fio-code-command-to-test-the-disk-performance-of-the-tikv-instance}

-   ランダム読み取りテスト:

    {{< copyable "" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randread -size=10G -filename=fio_randread_test.txt -name='fio randread test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_result.json
    ```

-   順次書き込みとランダム読み取りの混合テスト:

    {{< copyable "" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randrw -percentage_random=100,0 -size=10G -filename=fio_randread_write_test.txt -name='fio mixed randread and sequential write test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_write_test.json
    ```

## TiDB が現在サポートしているパブリック クラウド ベンダーは? {#what-public-cloud-vendors-are-currently-supported-by-tidb}

TiDB は[Google GKE](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-gcp-gke) 、 [AWS EKS](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-aws-eks) 、および[アリババクラウド ACK](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-alibaba-cloud)での展開をサポートしています。

さらに、TiDB は現在、JD Cloud と UCloud で利用できます。
