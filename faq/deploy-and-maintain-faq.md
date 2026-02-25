---
title: TiDB Deployment FAQs
summary: TiDB のデプロイメントに関連する FAQ について説明します。
---

# TiDB デプロイメントに関する FAQ {#tidb-deployment-faqs}

このドキュメントでは、TiDB のデプロイメントに関連する FAQ をまとめています。

## ソフトウェアとハ​​ードウェアの要件 {#software-and-hardware-requirements}

### TiDB はどのオペレーティング システムをサポートしていますか? {#what-operating-systems-does-tidb-support}

TiDB がサポートするオペレーティング システムについては、 [ソフトウェアとハ​​ードウェアの推奨事項](/hardware-and-software-requirements.md)参照してください。

### 開発、テスト、または本番環境における TiDB クラスターの推奨ハードウェア構成は何ですか? {#what-is-the-recommended-hardware-configuration-for-a-tidb-cluster-in-the-development-test-or-production-environment}

TiDBは、Intel x86-64アーキテクチャの64ビット汎用ハードウェア・サーバー・プラットフォーム、またはARMアーキテクチャのハードウェア・サーバー・プラットフォームに導入および実行できます。開発環境、テスト環境、および本番環境におけるサーバー・ハードウェア構成の要件と推奨事項については、 [ソフトウェアとハ​​ードウェアの推奨事項 - サーバー要件](/hardware-and-software-requirements.md#server-requirements)参照してください。

### 10 ギガビットのネットワーク カード 2 枚の目的は何ですか? {#what-s-the-purposes-of-2-network-cards-of-10-gigabit}

分散型クラスタであるTiDBは、特にPDに対して高い時間要件を要求します。これは、PDが一意のタイムスタンプを配布する必要があるためです。PDサーバーの時刻が一致していないと、PDサーバーを切り替える際に待機時間が長くなります。2枚のネットワークカードの結合によりデータ転送の安定性が保証され、10ギガビットの速度により転送速度が保証されます。ギガビットネットワークカードはボトルネックになりやすいため、10ギガビットネットワークカードの使用を強くお勧めします。

### SSD に RAID を使用しない場合は実現可能でしょうか? {#is-it-feasible-if-we-don-t-use-raid-for-ssd}

リソースが十分にある場合は、SSDにRAID 10を使用することをお勧めします。リソースが不十分な場合は、SSDにRAIDを使用しなくても問題ありません。

### TiDB コンポーネントの推奨構成は何ですか? {#what-s-the-recommended-configuration-of-tidb-components}

-   TiDB は CPU とメモリに対して高い要件があります。
-   PDはクラスタのメタデータを保存し、頻繁に読み取りおよび書き込みリクエストが発生します。そのため、高いI/Oディスクを必要とします。ディスクパフォ​​ーマンスが低いと、クラスタ全体のパフォーマンスに影響します。SSDディスクの使用をお勧めします。また、リージョン数が多いほど、CPUとメモリの要件が高くなります。
-   TiKVはCPU、メモリ、ディスクに対する要件が厳しく、SSDの使用が必須です。

詳細は[ソフトウェアとハ​​ードウェアの推奨事項](/hardware-and-software-requirements.md)参照。

## インストールと展開 {#installation-and-deployment}

本番環境では、 [TiUP](/tiup/tiup-overview.md)使用してTiDBクラスタをデプロイすることをお勧めします。3 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。

### TiKV/PD 用に変更された<code>toml</code>構成が有効にならないのはなぜですか? {#why-the-modified-code-toml-code-configuration-for-tikv-pd-does-not-take-effect}

`toml`設定を有効にするには、TiKV/PD で`--config`パラメータを設定する必要があります。TiKV/PD はデフォルトでは設定を読み取りません。現在、この問題はバイナリを使用してデプロイする場合にのみ発生します。TiKV の場合は、設定を編集してサービスを再起動してください。PD の場合は、設定ファイルは PD の初回起動時にのみ読み込まれ、その後は pd-ctl を使用して設定を変更できます。詳細は[PD Controlユーザー ガイド](/pd-control.md)参照してください。

### TiDB モニタリングフレームワーク (Prometheus + Grafana) はスタンドアロンマシンにデプロイするべきでしょうか、それとも複数のマシンにデプロイするべきでしょうか? 推奨される CPU とメモリはどれくらいでしょうか? {#should-i-deploy-the-tidb-monitoring-framework-prometheus-grafana-on-a-standalone-machine-or-on-multiple-machines-what-is-the-recommended-cpu-and-memory}

監視マシンはスタンドアロン構成での使用を推奨します。8コアCPU、16GB以上のメモリ、500GB以上のハードディスクを搭載することを推奨します。

### モニターがすべてのメトリックを表示できないのはなぜですか? {#why-the-monitor-cannot-display-all-metrics}

モニターのマシン時間とクラスター内の時間の差を確認してください。差が大きい場合は、時間を修正することでモニターにすべてのメトリックが表示されるようになります。

### TiDB でスロークエリログを個別に記録するにはどうすればよいですか? スロークエリの SQL ステートメントを見つけるにはどうすればよいでしょうか? {#how-to-separately-record-the-slow-query-log-in-tidb-how-to-locate-the-slow-query-sql-statement}

1.  TiDBのスロークエリの定義は、TiDB設定ファイルにあります。1 `tidb_slow_log_threshold: 300`は、スロークエリのしきい値（単位：ミリ秒）を設定するために使用されます。

2.  スロークエリが発生した場合、Grafana を使用してスロークエリが発生している`tidb-server`インスタンスとスロークエリの時刻を特定し、該当ノードのログに記録された SQL 文の情報を見つけることができます。

3.  ログに加えて、 `ADMIN SHOW SLOW`コマンドを使用してスロークエリも表示できます。詳細は[`ADMIN SHOW SLOW`コマンド](/identify-slow-queries.md#admin-show-slow-command)参照してください。

### TiDB クラスターを初めてデプロイしたときに TiKV の<code>label</code>が構成されていなかった場合、 <code>label</code>構成を追加するにはどうすればよいですか? {#how-to-add-the-code-label-code-configuration-if-code-label-code-of-tikv-was-not-configured-when-i-deployed-the-tidb-cluster-for-the-first-time}

TiDB `label`の設定は、クラスタのデプロイメントアーキテクチャに関連しています。これは重要であり、PDがグローバル管理とスケジューリングを実行するための基盤となります。以前のクラスタのデプロイメント時に`label`設定していない場合は、PD管理ツール`pd-ctl`を使用して`location-labels`情報を手動で追加し、デプロイメント構造を調整する必要があります（例： `config set location-labels "zone,rack,host"` ）。（実際の`label`レベル名に基づいて設定する必要があります）。

`pd-ctl`の使い方については[PD Controlユーザー ガイド](/pd-control.md)参照してください。

### ディスク テストの<code>dd</code>コマンドが<code>oflag=direct</code>オプションを使用するのはなぜですか? {#why-does-the-code-dd-code-command-for-the-disk-test-use-the-code-oflag-direct-code-option}

ダイレクト モードでは、書き込み要求を I/O コマンドにラップし、このコマンドをディスクに送信してファイル システム キャッシュをバイパスし、ディスクの実際の I/O 読み取り/書き込みパフォーマンスを直接テストします。

### <code>fio</code>コマンドを使用して TiKV インスタンスのディスク パフォーマンスをテストするにはどうすればよいですか? {#how-to-use-the-code-fio-code-command-to-test-the-disk-performance-of-the-tikv-instance}

以下の例では`ioengine=psync` （同期I/O）を使用しているため、 `iodepth`通常`1`に固定され、同時実行性は主に`numjobs`によって制御されます。ファイルシステムキャッシュをバイパスするには、 `direct=1`設定することをお勧めします。

-   ランダム読み取りテスト:

    ```bash
    ./fio -ioengine=psync -bs=32k -direct=1 -thread -rw=randread -time_based -size=10G -filename=fio_randread_test.txt -name='fio randread test' -iodepth=1 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_result.json
    ```

-   シーケンシャル書き込みとランダム読み取りの混合テスト:

    ```bash
    ./fio -ioengine=psync -bs=32k -direct=1 -thread -rw=randrw -percentage_random=100,0 -time_based -size=10G -filename=fio_randread_write_test.txt -name='fio mixed randread and sequential write test' -iodepth=1 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_write_test.json
    ```

## 現在 TiDB でサポートされているパブリック クラウド ベンダーは何ですか? {#what-public-cloud-vendors-are-currently-supported-by-tidb}

TiDB は[Google Cloud GKE](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-gcp-gke) 、 [AWS EKS](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-aws-eks) 、 [アリババクラウドACK](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-alibaba-cloud)でのデプロイメントをサポートします。

さらに、TiDB は現在 JD Cloud と UCloud でも利用可能です。
