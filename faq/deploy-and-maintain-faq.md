---
title: TiDB Deployment FAQs
summary: Learn about the FAQs related to TiDB deployment.
---

# TiDB 導入に関するよくある質問 {#tidb-deployment-faqs}

このドキュメントには、TiDB 導入に関連する FAQ がまとめられています。

## ソフトウェアとハ​​ードウェアの要件 {#software-and-hardware-requirements}

### TiDB はどのオペレーティング システムをサポートしていますか? {#what-operating-systems-does-tidb-support}

TiDB がサポートするオペレーティング システムについては、 [ソフトウェアとハ​​ードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

### 開発、テスト、または本番環境における TiDB クラスターの推奨ハードウェア構成は何ですか? {#what-is-the-recommended-hardware-configuration-for-a-tidb-cluster-in-the-development-test-or-production-environment}

TiDB は、Intel x86-64アーキテクチャの 64 ビット汎用ハードウェアサーバープラットフォーム、または ARMアーキテクチャのハードサーバープラットフォームに展開して実行できます。開発、テスト、本番環境のサーバーハードウェア構成に関する要件と推奨事項については、 [ソフトウェアおよびハードウェアの推奨事項 - サーバーの推奨事項](/hardware-and-software-requirements.md#server-recommendations)を参照してください。

### 10 ギガビットのネットワーク カード 2 枚の目的は何ですか? {#what-s-the-purposes-of-2-network-cards-of-10-gigabit}

TiDB は分散クラスターとして、PD が一意のタイムスタンプを配布する必要があるため、特に PD に対して時間に対する要求が高くなります。 PDサーバの時刻が一定していないと、PDサーバーを切り替える際の待ち時間が長くなります。 2 枚のネットワーク カードの結合によりデータ伝送の安定性が保証され、10 ギガビットで伝送速度が保証されます。ギガビット ネットワーク カードはボトルネックに遭遇しやすいため、10 ギガビット ネットワーク カードを使用することを強くお勧めします。

### SSD に RAID を使用しない場合でも実現可能ですか? {#is-it-feasible-if-we-don-t-use-raid-for-ssd}

リソースが十分にある場合は、SSD に RAID 10 を使用することをお勧めします。リソースが不十分な場合は、SSD に RAID を使用しなくても問題ありません。

### TiDB コンポーネントの推奨構成は何ですか? {#what-s-the-recommended-configuration-of-tidb-components}

-   TiDB には、CPU とメモリに対する高い要件があります。 TiDB Binlogを有効にする必要がある場合は、サービス量の見積もりと GC 操作の所要時間に基づいてローカル ディスク領域を増やす必要があります。ただし、SSD ディスクは必須ではありません。
-   PD はクラスターのメタデータを保存し、頻繁に読み取りおよび書き込みリクエストを行います。高い I/O ディスクが必要です。ディスクのパフォーマンスが低いと、クラスター全体のパフォーマンスに影響します。 SSD ディスクの使用をお勧めします。さらに、リージョンの数が増えると、CPU とメモリの要件も高くなります。
-   TiKV には、CPU、メモリ、ディスクに対する高い要件があります。 SSDを使用するために必要です。

詳細は[ソフトウェアとハ​​ードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

## インストールと展開 {#installation-and-deployment}

本番環境では、 [TiUP](/tiup/tiup-overview.md)を使用して TiDB クラスターをデプロイすることをお勧めします。 [TiUPを使用した TiDBクラスタのデプロイ](/production-deployment-using-tiup.md)を参照してください。

### TiKV/PD 用に変更された<code>toml</code>構成が有効にならないのはなぜですか? {#why-the-modified-code-toml-code-configuration-for-tikv-pd-does-not-take-effect}

`toml`設定を有効にするには、TiKV/PD で`--config`パラメータを設定する必要があります。 TiKV/PD はデフォルトでは構成を読み取りません。現在、この問題はバイナリを使用して展開する場合にのみ発生します。 TiKV の場合は、構成を編集し、サービスを再起動します。 PD の場合、構成ファイルは PD の初回起動時にのみ読み取られ、その後は pd-ctl を使用して構成を変更できます。詳細は[PD Controlユーザーガイド](/pd-control.md)を参照してください。

### TiDB モニタリング フレームワーク (Prometheus + Grafana) をスタンドアロン マシンにデプロイする必要がありますか? それとも複数のマシンにデプロイする必要がありますか?推奨のCPUとメモリは何ですか? {#should-i-deploy-the-tidb-monitoring-framework-prometheus-grafana-on-a-standalone-machine-or-on-multiple-machines-what-is-the-recommended-cpu-and-memory}

監視マシンはスタンドアロン展開を使用することをお勧めします。 16 GB 以上のメモリと 500 GB 以上のハードディスクを備えた 8 コア CPU を使用することをお勧めします。

### モニターがすべてのメトリクスを表示できないのはなぜですか? {#why-the-monitor-cannot-display-all-metrics}

モニターのマシン時刻とクラスタ内の時刻との時差を確認してください。それが大きい場合は、時間を修正すると、モニターにすべてのメトリックが表示されます。

### supervise/svc/svstat サービスの機能は何ですか? {#what-is-the-function-of-supervise-svc-svstat-service}

-   監視: デーモンプロセス、プロセスを管理する
-   svc: サービスを開始および停止します。
-   svstat: プロセスのステータスを確認する

### inventory.ini 変数の説明 {#description-of-inventory-ini-variables}

| 変数                      | 説明                                                                                                                          |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `cluster_name`          | クラスターの名前 (調整可能)                                                                                                             |
| `tidb_version`          | TiDB のバージョン                                                                                                                 |
| `deployment_method`     | デプロイメント方法、デフォルトではバイナリ、Docker はオプション                                                                                         |
| `process_supervision`   | プロセスの監視方法、デフォルトでは systemd、監視はオプション                                                                                          |
| `timezone`              | 管理対象ノードのタイムゾーン、調整可能、デフォルトは`Asia/Shanghai` 、変数`set_timezone`で使用                                                              |
| `set_timezone`          | 管理対象ノードのタイムゾーンを編集するには、デフォルトで True。 False は閉じることを意味します                                                                       |
| `enable_elk`            | 現在サポートされていません                                                                                                               |
| `enable_firewalld`      | ファイアウォールを有効にするには、デフォルトで閉じます                                                                                                 |
| `enable_ntpd`           | 管理対象ノードの NTP サービスを監視する場合、デフォルトでは True。閉じないでください                                                                             |
| `machine_benchmark`     | 管理対象ノードのディスク IOPS を監視するには、デフォルトで True。閉じないでください                                                                             |
| `set_hostname`          | IP に基づいて管理対象ノードのホスト名を編集するには、デフォルトで False                                                                                    |
| `enable_binlog`         | Pumpをデプロイしてbinlogを有効にするかどうか。デフォルトでは False。Kafka クラスターに応じて異なります。 `zookeeper_addrs`変数を参照してください                                |
| `zookeeper_addrs`       | binlog Kafka クラスターの ZooKeeper アドレス                                                                                          |
| `enable_slow_query_log` | TiDB のスロー クエリ ログを単一のファイルに記録します: ({{deploy_dir }}/log/tidb_slow_query.log)。デフォルトでは False、TiDB ログに記録します。                      |
| `deploy_without_tidb`   | Key-Value モードでは、PD、TiKV、およびモニタリング サービスのみをデプロイし、TiDB はデプロイしません。 `inventory.ini`ファイルで tidb_servers ホスト グループの IP を null に設定します |

### TiDB にスロークエリログを個別に記録するにはどうすればよいですか?遅いクエリ SQL ステートメントを見つけるにはどうすればよいですか? {#how-to-separately-record-the-slow-query-log-in-tidb-how-to-locate-the-slow-query-sql-statement}

1.  TiDB のスロー クエリ定義は、TiDB 構成ファイルにあります。 `tidb_slow_log_threshold: 300`パラメータはスロークエリの閾値（単位：ミリ秒）を設定するために使用されます。

2.  スロークエリが発生した場合、Grafana を使用してスロークエリが発生している`tidb-server`のインスタンスとスロークエリの時点を特定し、対応するノードのログに記録されている SQL ステートメント情報を見つけることができます。

3.  ログに加えて、 `ADMIN SHOW SLOW`コマンドを使用してスロー クエリを表示することもできます。詳細は[`ADMIN SHOW SLOW`コマンド](/identify-slow-queries.md#admin-show-slow-command)を参照してください。

### TiDB クラスターを初めてデプロイしたときに TiKV の<code>label</code>が構成されていなかった場合、 <code>label</code>構成を追加するにはどうすればよいですか? {#how-to-add-the-code-label-code-configuration-if-code-label-code-of-tikv-was-not-configured-when-i-deployed-the-tidb-cluster-for-the-first-time}

TiDB `label`の構成は、クラスター展開アーキテクチャに関連しています。これは PD がグローバルな管理とスケジューリングを実行するための重要なものであり、その基礎となります。以前にクラスターをデプロイするときに`label`構成しなかった場合は、PD 管理ツール`pd-ctl`を使用して`location-labels`情報 (たとえば`config set location-labels "zone,rack,host"`を手動で追加して、デプロイメント構造を調整する必要があります (実際の`label`レベル名に基づいて構成する必要があります)。

`pd-ctl`の使用方法については、 [PD Controlユーザーガイド](/pd-control.md)を参照してください。

### ディスク テストの<code>dd</code>コマンドで<code>oflag=direct</code>オプションが使用されるのはなぜですか? {#why-does-the-code-dd-code-command-for-the-disk-test-use-the-code-oflag-direct-code-option}

ダイレクト モードでは、書き込みリクエストを I/O コマンドにラップし、このコマンドをディスクに送信して、ファイル システム キャッシュをバイパスし、ディスクの実際の I/O 読み取り/書き込みパフォーマンスを直接テストします。

### <code>fio</code>コマンドを使用して TiKV インスタンスのディスク パフォーマンスをテストするにはどうすればよいですか? {#how-to-use-the-code-fio-code-command-to-test-the-disk-performance-of-the-tikv-instance}

-   ランダム読み取りテスト:

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randread -size=10G -filename=fio_randread_test.txt -name='fio randread test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_result.json
    ```

-   シーケンシャル書き込みとランダム読み取りの混合テスト:

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randrw -percentage_random=100,0 -size=10G -filename=fio_randread_write_test.txt -name='fio mixed randread and sequential write test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_write_test.json
    ```

## 現在 TiDB でサポートされているパブリック クラウド ベンダーは何ですか? {#what-public-cloud-vendors-are-currently-supported-by-tidb}

TiDB は[Google Cloud GKE](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-gcp-gke) 、 [AWS EKS](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-aws-eks) 、および[アリババクラウドACK](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-alibaba-cloud)でのデプロイメントをサポートします。

さらに、TiDB は現在、JD Cloud と UCloud で利用できます。
