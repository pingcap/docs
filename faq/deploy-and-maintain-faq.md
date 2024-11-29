---
title: TiDB Deployment FAQs
summary: TiDB のデプロイメントに関連する FAQ について説明します。
---

# TiDB 導入に関する FAQ {#tidb-deployment-faqs}

このドキュメントでは、TiDB のデプロイメントに関連する FAQ をまとめています。

## ソフトウェアおよびハードウェアの要件 {#software-and-hardware-requirements}

### TiDB はどのオペレーティング システムをサポートしていますか? {#what-operating-systems-does-tidb-support}

TiDB がサポートするオペレーティング システムについては、 [ソフトウェアとハードウェアの推奨事項](/hardware-and-software-requirements.md)参照してください。

### 開発、テスト、または本番環境における TiDB クラスターの推奨ハードウェア構成は何ですか? {#what-is-the-recommended-hardware-configuration-for-a-tidb-cluster-in-the-development-test-or-production-environment}

TiDB は、Intel x86-64アーキテクチャの 64 ビット汎用ハードウェアサーバープラットフォームまたは ARMアーキテクチャのハードウェアサーバープラットフォームに導入して実行できます。開発、テスト、および本番環境のサーバーハードウェア構成に関する要件と推奨事項については、 [ソフトウェアとハードウェアの推奨事項 - サーバーの推奨事項](/hardware-and-software-requirements.md#server-recommendations)参照してください。

### 10 ギガビットのネットワーク カード 2 枚の目的は何ですか? {#what-s-the-purposes-of-2-network-cards-of-10-gigabit}

分散型クラスタである TiDB は、特に PD に対して高い時間要件を要求します。これは、PD が一意のタイムスタンプを配布する必要があるためです。PD サーバーの時間が一致していないと、PDサーバーを切り替えるときに待機時間が長くなります。2 つのネットワーク カードの結合により、データ転送の安定性が保証され、10 ギガビットにより転送速度が保証されます。ギガビット ネットワーク カードはボトルネックになりやすいため、10 ギガビット ネットワーク カードを使用することを強くお勧めします。

### SSD に RAID を使用しない場合は実現可能でしょうか? {#is-it-feasible-if-we-don-t-use-raid-for-ssd}

リソースが十分である場合は、SSD に RAID 10 を使用することをお勧めします。リソースが不十分な場合は、SSD に RAID を使用しなくてもかまいません。

### TiDB コンポーネントの推奨構成は何ですか? {#what-s-the-recommended-configuration-of-tidb-components}

-   TiDB は CPU とメモリに対する要件が高くなります。TiDB Binlog を有効にする必要がある場合は、サービス ボリュームの見積もりと GC 操作の時間要件に基づいて、ローカル ディスク領域を増やす必要があります。ただし、SSD ディスクは必須ではありません。
-   PD はクラスターのメタデータを保存し、読み取りおよび書き込み要求が頻繁に発生します。高 I/O ディスクが必要です。パフォーマンスの低いディスクは、クラスター全体のパフォーマンスに影響します。SSD ディスクの使用をお勧めします。また、リージョンの数が多いほど、CPU とメモリの要件が高くなります。
-   TiKV は CPU、メモリ、ディスクに対して高い要件があります。SSD を使用する必要があります。

詳細は[ソフトウェアとハードウェアの推奨事項](/hardware-and-software-requirements.md)参照。

## インストールと展開 {#installation-and-deployment}

本番環境では、 [TiUP](/tiup/tiup-overview.md)使用して TiDB クラスターをデプロイすることをお勧めします[TiUP を使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。

### TiKV/PD 用に変更された<code>toml</code>構成が有効にならないのはなぜですか? {#why-the-modified-code-toml-code-configuration-for-tikv-pd-does-not-take-effect}

`toml`設定を有効にするには、TiKV/PD で`--config`パラメータを設定する必要があります。TiKV/PD はデフォルトでは設定を読み取りません。現在、この問題はバイナリを使用してデプロイする場合にのみ発生します。TiKV の場合は、設定を編集してサービスを再起動してください。PD の場合は、PD が初めて起動されたときにのみ設定ファイルが読み取られ、その後は pd-ctl を使用して設定を変更できます。詳細については、 [PD Controlユーザー ガイド](/pd-control.md)参照してください。

### TiDB 監視フレームワーク (Prometheus + Grafana) はスタンドアロン マシンにデプロイする必要がありますか、それとも複数のマシンにデプロイする必要がありますか? 推奨される CPU とメモリは何ですか? {#should-i-deploy-the-tidb-monitoring-framework-prometheus-grafana-on-a-standalone-machine-or-on-multiple-machines-what-is-the-recommended-cpu-and-memory}

監視マシンはスタンドアロン展開を使用することをお勧めします。16 GB 以上のメモリと 500 GB 以上のハードディスクを搭載した 8 コア CPU を使用することをお勧めします。

### モニターがすべてのメトリックを表示できないのはなぜですか? {#why-the-monitor-cannot-display-all-metrics}

モニターのマシン時間とクラスター内の時間差を確認します。時間差が大きい場合は、時間を修正すると、モニターにすべてのメトリックが表示されます。

### supervise/svc/svstat サービスの機能は何ですか? {#what-is-the-function-of-supervise-svc-svstat-service}

-   監視: デーモンプロセス、プロセスを管理する
-   svc: サービスを開始および停止する
-   svstat: プロセスの状態を確認する

### inventory.ini 変数の説明 {#description-of-inventory-ini-variables}

| 変数                      | 説明                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| `cluster_name`          | クラスターの名前（調整可能）                                                                                          |
| `tidb_version`          | TiDBのバージョン                                                                                              |
| `deployment_method`     | 展開方法、デフォルトはバイナリ、Dockerはオプション                                                                            |
| `process_supervision`   | プロセスの監視方法、systemdがデフォルト、superviseはオプション                                                                 |
| `timezone`              | 管理対象ノードのタイムゾーン。 `set_timezone` `Asia/Shanghai`とともに使用される。                                                |
| `set_timezone`          | 管理対象ノードのタイムゾーンを編集します。デフォルトではTrueです。Falseの場合は閉じます。                                                       |
| `enable_elk`            | 現在サポートされていません                                                                                           |
| `enable_firewalld`      | ファイアウォールを有効にする（デフォルトでは閉じている）                                                                            |
| `enable_ntpd`           | 管理対象ノードのNTPサービスを監視する。デフォルトではTrue。閉じないでください。                                                             |
| `machine_benchmark`     | 管理対象ノードのディスクIOPSを監視する。デフォルトではTrue。閉じないでください。                                                            |
| `set_hostname`          | IPに基づいて管理対象ノードのホスト名を編集します。デフォルトではFalseです。                                                               |
| `enable_binlog`         | Pumpをデプロイしてbinlogを有効にするかどうか。デフォルトではFalse。Kafkaクラスタに依存します。1 `zookeeper_addrs`変数を参照してください。                |
| `zookeeper_addrs`       | binlog Kafka クラスターの ZooKeeper アドレス                                                                      |
| `enable_slow_query_log` | TiDBのスロークエリログを1つのファイルに記録します: ({{ deploy_dir }}/log/tidb_slow_query.log)。デフォルトではFalseで、TiDBログに記録されます。    |
| `deploy_without_tidb`   | キーバリューモードでは、PD、TiKV、監視サービスのみ`inventory.ini`デプロイし、TiDBはデプロイしません。1ファイルでtidb_serversホストグループのIPをnullに設定します。 |

### TiDB でスロー クエリ ログを個別に記録するにはどうすればよいですか? スロー クエリ SQL ステートメントを見つけるにはどうすればよいでしょうか? {#how-to-separately-record-the-slow-query-log-in-tidb-how-to-locate-the-slow-query-sql-statement}

1.  TiDB のスロー クエリ定義は、TiDB 構成ファイルにあります。1 `tidb_slow_log_threshold: 300`は、スロー クエリのしきい値 (単位: ミリ秒) を構成するために使用されます。

2.  スロークエリが発生した場合、Grafana を使用してスロークエリが発生している`tidb-server`インスタンスとスロークエリの時点を特定し、対応するノードのログに記録されている SQL ステートメント情報を見つけることができます。

3.  ログに加えて、 `ADMIN SHOW SLOW`コマンドを使用してスロークエリを表示することもできます。詳細については、 [`ADMIN SHOW SLOW`コマンド](/identify-slow-queries.md#admin-show-slow-command)参照してください。

### TiDB クラスターを初めてデプロイしたときに TiKV の<code>label</code>が構成されていなかった場合、 <code>label</code>構成を追加するにはどうすればよいですか? {#how-to-add-the-code-label-code-configuration-if-code-label-code-of-tikv-was-not-configured-when-i-deployed-the-tidb-cluster-for-the-first-time}

TiDB `label`の設定は、クラスターのデプロイメントアーキテクチャに関連しています。これは重要であり、PD がグローバル管理とスケジュールを実行するための基礎となります。以前にクラスターをデプロイしたときに`label`設定しなかった場合は、PD 管理ツール`pd-ctl`使用して`location-labels`情報を手動で追加して、デプロイメント構造を調整する必要があります (例: `config set location-labels "zone,rack,host"` ) (実際の`label`レベル名に基づいて設定する必要があります)。

`pd-ctl`の使い方については[PD Controlユーザー ガイド](/pd-control.md)参照してください。

### ディスク テストの<code>dd</code>コマンドが<code>oflag=direct</code>オプションを使用するのはなぜですか? {#why-does-the-code-dd-code-command-for-the-disk-test-use-the-code-oflag-direct-code-option}

ダイレクト モードでは、書き込み要求が I/O コマンドにラップされ、このコマンドがディスクに送信されてファイル システム キャッシュがバイパスされ、ディスクの実際の I/O 読み取り/書き込みパフォーマンスが直接テストされます。

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

TiDB は[Google クラウド GKE](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-gcp-gke) 、 [AWS の](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-aws-eks) 、 [アリババクラウドACK](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-alibaba-cloud)でのデプロイメントをサポートします。

さらに、TiDB は現在 JD Cloud と UCloud でも利用可能です。
