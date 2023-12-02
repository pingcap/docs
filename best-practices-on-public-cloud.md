---
title: TiDB Best Practices on Public Cloud
summary: Learn about the best practices for deploying TiDB on public cloud.
---

# パブリック クラウドにおける TiDB のベスト プラクティス {#tidb-best-practices-on-public-cloud}

パブリック クラウド インフラストラクチャは、TiDB の導入と管理のための選択肢としてますます人気が高まっています。ただし、TiDB をパブリック クラウドに展開するには、パフォーマンスのチューニング、コストの最適化、信頼性、スケーラビリティなど、いくつかの重要な要素を慎重に検討する必要があります。

このドキュメントでは、 Raft Engineの専用ディスクの使用、KV RocksDB でのコンパクション I/O フローの削減、クロス AZ トラフィックのコストの最適化、Google Cloud ライブ マイグレーション イベントの軽減など、パブリック クラウドに TiDB をデプロイするためのさまざまな重要なベスト プラクティスについて説明します。大規模なクラスター内の PDサーバーを微調整します。これらのベスト プラクティスに従うことで、パブリック クラウド上での TiDB 導入のパフォーマンス、コスト効率、信頼性、拡張性を最大化できます。

## Raft Engineには専用ディスクを使用する {#use-a-dedicated-disk-for-raft-engine}

TiKV の[Raft Engine](/glossary.md#raft-engine)は、従来のデータベースの先行書き込みログ (WAL) と同様の重要な役割を果たします。最適なパフォーマンスと安定性を実現するには、TiDB をパブリック クラウドに展開するときにRaft Engineに専用のディスクを割り当てることが重要です。次の`iostat`書き込みの多いワークロードを伴う TiKV ノードの I/O 特性を示しています。

    Device            r/s     rkB/s       w/s     wkB/s      f/s  aqu-sz  %util
    sdb           1649.00 209030.67   1293.33 304644.00    13.33    5.09  48.37
    sdd           1033.00   4132.00   1141.33  31685.33   571.00    0.94 100.00

デバイス`sdb`は KV RocksDB に使用され、デバイス`sdd`はRaft Engineログの復元に使用されます。 `sdd`デバイスの 1 秒あたりに完了したフラッシュ リクエストの数を表す`f/s`値よりも大幅に大きいことに注意してください。 Raft Engineでは、バッチ内の書き込みが同期としてマークされると、バッチ リーダーは書き込み後に`fdatasync()`を呼び出し、バッファされたデータがstorageにフラッシュされることを保証します。 Raft Engineに専用ディスクを使用することで、TiKV はリクエストの平均キュー長を短縮し、最適で安定した書き込みレイテンシーを確保します。

さまざまなクラウド プロバイダーが、IOPS や MBPS などのさまざまなパフォーマンス特性を持つさまざまなディスク タイプを提供しています。したがって、ワークロードに基づいて、適切なクラウド プロバイダー、ディスク タイプ、ディスク サイズを選択することが重要です。

### パブリック クラウド上のRaft Engineに適切なディスクを選択する {#choose-appropriate-disks-for-raft-engine-on-public-clouds}

このセクションでは、さまざまなパブリック クラウド上でRaft Engineに適切なディスクを選択するためのベスト プラクティスについて概説します。パフォーマンス要件に応じて、2 種類の推奨ディスクが用意されています。

#### ミドルレンジディスク {#middle-range-disk}

以下は、さまざまなパブリック クラウドに推奨されるミドルレンジ ディスクです。

-   AWS では[GP3](https://aws.amazon.com/ebs/general-purpose/)が推奨されます。 gp3 ボリュームは、ボリューム サイズに関係なく、3000 IOPS と 125 MB/秒のスループットの無料割り当てを提供します。通常、 Raft Engineにはこれで十分です。

-   Google Cloud では、 [PD-SSD](https://cloud.google.com/compute/docs/disks#disk-types/)が推奨されます。 IOPS と MBPS は、割り当てられたディスク サイズによって異なります。パフォーマンス要件を満たすために、 Raft Engineに 200 GB を割り当てることをお勧めします。 Raft Engine はそれほど大きなスペースを必要としませんが、最適なパフォーマンスを保証します。

-   Azure では[プレミアムSSD v2](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#premium-ssd-v2)が推奨されます。 AWS gp3 と同様に、Premium SSD v2 は、ボリューム サイズに関係なく、3000 IOPS と 125 MB/秒のスループットの無料割り当てを提供します。通常、これはRaft Engineには十分です。

#### ハイエンドディスク {#high-end-disk}

Raft Engineのレイテンシーがさらに低いことが期待される場合は、ハイエンド ディスクの使用を検討してください。以下は、さまざまなパブリック クラウドに推奨されるハイエンド ディスクです。

-   AWS では[io2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)が推奨されます。ディスク サイズと IOPS は、特定の要件に応じてプロビジョニングできます。

-   Google Cloud では、 [pd-エクストリーム](https://cloud.google.com/compute/docs/disks#disk-types/)が推奨されます。ディスク サイズ、IOPS、MBPS をプロビジョニングできますが、これは 64 個を超える CPU コアを備えたインスタンスでのみ使用できます。

-   Azure では[ウルトラディスク](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#ultra-disks)が推奨されます。ディスク サイズ、IOPS、MBPS は、特定の要件に応じてプロビジョニングできます。

### 例 1: AWS でソーシャル ネットワーク ワークロードを実行する {#example-1-run-a-social-network-workload-on-aws}

AWS は、20 GB [GP3](https://aws.amazon.com/ebs/general-purpose/)ボリュームに対して 3000 IOPS と 125 MBPS/秒を提供します。

書き込み集中型のソーシャル ネットワーク アプリケーションのワークロードに AWS 上の専用の 20 GB [GP3](https://aws.amazon.com/ebs/general-purpose/) Raft Engineディスクを使用すると、次のような改善が見られますが、推定コストは 0.4% しか増加しません。

-   QPS (1 秒あたりのクエリ数) が 17.5% 増加
-   挿入ステートメントの平均レイテンシーが 18.7% 減少
-   挿入ステートメントの p99レイテンシーが 45.6% 減少しました。

| メトリック              | 共有Raft Engineディスク | Raft Engine専用ディスク | 違い （％） |
| ------------------ | ----------------- | ----------------- | ------ |
| QPS (K/秒)          | 8.0               | 9.4               | 17.5   |
| AVG 挿入レイテンシー (ミリ秒) | 11.3              | 9.2               | -18.7  |
| P99 挿入遅延 (ミリ秒)     | 29.4              | 16.0              | -45.6  |

### 例 2: Azure で TPC-C/Sysbench ワークロードを実行する {#example-2-run-tpc-c-sysbench-workload-on-azure}

Azure 上のRaft Engineに専用の 32 GB [ウルトラディスク](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#ultra-disks)を使用すると、次の改善が見られます。

-   Sysbench `oltp_read_write`ワークロード: QPS が 17.8% 増加し、平均レイテンシーが 15.6% 減少しました。
-   TPC-C ワークロード: QPS が 27.6% 増加し、平均レイテンシーが 23.1% 減少しました。

| メトリック            | ワークロード                   | 共有Raft Engineディスク | Raft Engine専用ディスク | 違い （％） |
| ---------------- | ------------------------ | ----------------- | ----------------- | ------ |
| QPS (K/秒)        | システムベンチ`oltp_read_write` | 60.7              | 71.5              | 17.8   |
| QPS (K/秒)        | TPC-C                    | 23.9              | 30.5              | 27.6   |
| AVG レイテンシー (ミリ秒) | システムベンチ`oltp_read_write` | 4.5               | 3.8               | -15.6  |
| AVG レイテンシー (ミリ秒) | TPC-C                    | 3.9               | 3.0               | -23.1  |

### 例 3: TiKV マニフェストのRaft Engine用に Google Cloud に専用の pd-ssd ディスクを接続する {#example-3-attach-a-dedicated-pd-ssd-disk-on-google-cloud-for-raft-engine-on-tikv-manifest}

次の TiKV 構成例は、追加の 512 GB [PD-SSD](https://cloud.google.com/compute/docs/disks#disk-types/)ディスクを[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable)によってデプロイされた Google Cloud 上のクラスタに接続する方法を示しています。この特定のディスクにRaft Engineログを保存するように`raft-engine.dir`が構成されています。

    tikv:
        config: |
          [raft-engine]
            dir = "/var/lib/raft-pv-ssd/raft-engine"
            enable = true
            enable-log-recycle = true
        requests:
          storage: 4Ti
        storageClassName: pd-ssd
        storageVolumes:
        - mountPath: /var/lib/raft-pv-ssd
          name: raft-pv-ssd
          storageSize: 512Gi

## KV RocksDB のコンパクション I/O フローを削減する {#reduce-compaction-i-o-flow-in-kv-rocksdb}

TiKV のstorageエンジンとして、ユーザー データの保存に[ロックスDB](https://rocksdb.org/)が使用されます。クラウド EBS でプロビジョニングされた IO スループットは通常、コストを考慮して制限されているため、RocksDB では高い書き込み増幅が発生し、ディスク スループットがワークロードのボトルネックになる可能性があります。その結果、保留中の圧縮バイトの合計数が時間の経過とともに増加し、フロー制御がトリガーされます。これは、TiKV にはフォアグラウンド書き込みフローに対応するのに十分なディスク帯域幅が不足していることを示しています。

ディスク スループットの制限によって引き起こされるボトルネックを軽減するには、RocksDB の圧縮レベルを上げ、ディスク スループットを下げることでパフォーマンスを向上させることができます。たとえば、次の例を参照して、デフォルトのカラムファミリーのすべての圧縮レベルを`zstd`に増やすことができます。

    [rocksdb.defaultcf]
    compression-per-level = ["zstd", "zstd", "zstd", "zstd", "zstd", "zstd", "zstd"]

## クロス AZ ネットワーク トラフィックのコストを最適化する {#optimize-cost-for-cross-az-network-traffic}

TiDB を複数のアベイラビリティ ゾーン (AZ) にまたがって展開すると、AZ 間のデータ転送料金によりコストが増加する可能性があります。コストを最適化するには、クロス AZ ネットワーク トラフィックを削減することが重要です。

クロス AZ 読み取りトラフィックを削減するには、 [Follower Read機能](/follower-read.md)有効にします。これにより、TiDB が同じアベイラビリティ ゾーン内のレプリカを優先的に選択できるようになります。この機能を有効にするには、変数[`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)を`closest-replicas`または`closest-adaptive`に設定します。

TiKV インスタンスでのクロス AZ 書き込みトラフィックを削減するには、ネットワーク経由で送信する前にデータを圧縮する gRPC 圧縮機能を有効にします。次の設定例は、TiKV の gzip gRPC 圧縮を有効にする方法を示しています。

    server_configs:
      tikv:
        server.grpc-compression-type: gzip

TiFlash MPP タスクのデータ シャッフルによって発生するネットワーク トラフィックを削減するには、複数のTiFlashインスタンスを同じアベイラビリティ ゾーン (AZ) にデプロイすることをお勧めします。 v6.6.0 以降、デフォルトで[圧縮交換](/explain-mpp.md#mpp-version-and-exchange-data-compression)が有効になり、MPP データ シャッフルによって発生するネットワーク トラフィックが軽減されます。

## Google Cloud でのライブ マイグレーション メンテナンス イベントを軽減する {#mitigate-live-migration-maintenance-events-on-google-cloud}

Google Cloud の[ライブマイグレーション機能](https://cloud.google.com/compute/docs/instances/live-migration-process)により、ダウンタイムを発生させることなく VM をホスト間でシームレスに移行できます。ただし、これらの移行イベントは、頻度は低いものの、TiDB クラスター内で実行されている VM を含む VM のパフォーマンスに大きな影響を与える可能性があります。このようなイベントが発生すると、影響を受ける VM のパフォーマンスが低下し、TiDB クラスターでのクエリの処理時間が長くなる可能性があります。

Google Cloud によって開始されたライブ マイグレーション イベントを検出し、これらのイベントによるパフォーマンスへの影響を軽減するために、TiDB は Google のメタデータに基づいて[スクリプトを見ている](https://github.com/PingCAP-QE/tidb-google-maintenance)を提供します[例](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/metadata/main.py) 。このスクリプトを TiDB、TiKV、および PD ノードにデプロイして、メンテナンス イベントを検出できます。メンテナンス イベントが検出されると、中断を最小限に抑え、クラスターの動作を最適化するために、次のように適切なアクションが自動的に実行されます。

-   TiDB: TiDB ノードを遮断し、TiDB ポッドを削除することで、TiDB ノードをオフラインにします。これは、TiDB インスタンスのノード プールが自動スケールに設定されており、TiDB 専用であることを前提としています。ノード上で実行されている他のポッドで中断が発生する可能性があり、封鎖されたノードはオートスケーラーによって再利用されることが予想されます。
-   TiKV: メンテナンス中に、影響を受ける TiKV ストアのリーダーを排除します。
-   PD: 現在の PD インスタンスが PD リーダーである場合、リーダーを辞任します。

この監視スクリプトは、Kubernetes 環境で TiDB の管理機能を強化する[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/dev/tidb-operator-overview)使用してデプロイされた TiDB クラスター用に特別に設計されていることに注意することが重要です。

監視スクリプトを利用し、メンテナンス イベント中に必要なアクションを実行することで、TiDB クラスタは Google Cloud でのライブ マイグレーション イベントをより適切に処理し、クエリ処理と応答時間への影響を最小限に抑えながら、よりスムーズな操作を保証できます。

## 高い QPS を備えた大規模 TiDB クラスター向けに PD を調整する {#tune-pd-for-a-large-scale-tidb-cluster-with-high-qps}

TiDB クラスターでは、TSO (Timestamp Oracle) の提供やリクエストの処理などの重要なタスクを処理するために、単一のアクティブな配置Driver(PD)サーバーが使用されます。ただし、単一のアクティブな PDサーバーに依存すると、TiDB クラスターのスケーラビリティが制限される可能性があります。

### PD制限の症状 {#symptoms-of-pd-limitation}

次の図は、それぞれ 56 個の CPU を搭載した 3 台の PD サーバーで構成される大規模 TiDB クラスターの症状を示しています。これらの図から、1 秒あたりのクエリ (QPS) が 100 万を超え、1 秒あたりの TSO (Timestamp Oracle) リクエストが 162,000 を超えると、CPU 使用率が約 4,600% に達することがわかります。この高い CPU 使用率は、PD リーダーに重大な負荷がかかっており、利用可能な CPU リソースが不足していることを示しています。

![pd-server-cpu](/media/performance/public-cloud-best-practice/baseline_cpu.png) ![pd-server-metrics](/media/performance/public-cloud-best-practice/baseline_metrics.png)

### PD パフォーマンスを調整する {#tune-pd-performance}

PDサーバーの CPU 使用率が高い問題に対処するには、次のチューニング調整を行うことができます。

#### PD構成を調整する {#adjust-pd-configuration}

[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) : このパラメータは、PDサーバーが物理 TSO バッチを更新する間隔を制御します。間隔を短くすることで、PDサーバーはTSO バッチをより頻繁に割り当てることができるため、次の割り当てまでの待ち時間が短縮されます。

    tso-update-physical-interval = "10ms" # default: 50ms

#### TiDB グローバル変数を調整する {#adjust-a-tidb-global-variable}

PD 構成に加えて、TSO クライアントのバッチ待機機能を有効にすると、TSO クライアントの動作をさらに最適化できます。この機能を有効にするには、グローバル変数[`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)をゼロ以外の値に設定します。

    set global tidb_tso_client_batch_max_wait_time = 2; # default: 0

#### TiKV 構成を調整する {#adjust-tikv-configuration}

リージョンの数を減らし、システムのハートビートオーバーヘッドを軽減するには、TiKV 構成のリージョンサイズを`96MB`から`256MB`に増やすことをお勧めします。

    [coprocessor]
      region-split-size = "256MB"

## チューニング後 {#after-tuning}

調整後、次の効果が観察されます。

-   1 秒あたりの TSO リクエストは 64,800 に減少します。
-   CPU 使用率は約 4,600% から 1,400% に大幅に減少します。
-   P999 値`PD server TSO handle time`は 2ms から 0.5ms に減少します。

これらの改善は、チューニング調整により、安定した TSO 処理パフォーマンスを維持しながら、PDサーバーの CPU 使用率を削減することに成功したことを示しています。

![pd-server-cpu](/media/performance/public-cloud-best-practice/after_tuning_cpu.png) ![pd-server-metrics](/media/performance/public-cloud-best-practice/after_tuning_metrics.png)
