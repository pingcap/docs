---
title: TiDB Best Practices on Public Cloud
summary: Learn about the best practices for deploying TiDB on public cloud.
---

# パブリッククラウドにおける TiDB のベストプラクティス {#tidb-best-practices-on-public-cloud}

パブリック クラウド インフラストラクチャは、TiDB の導入と管理の選択肢としてますます人気が高まっています。ただし、パブリック クラウドに TiDB を導入するには、パフォーマンス チューニング、コストの最適化、信頼性、スケーラビリティなど、いくつかの重要な要素を慎重に考慮する必要があります。

このドキュメントでは、 Raft Engine専用ディスクの使用、KV RocksDB での圧縮 I/O フローの削減、AZ 間トラフィックのコストの最適化、Google Cloud ライブ マイグレーション イベントの緩和、大規模クラスタでの PDサーバーの微調整など、パブリック クラウドに TiDB をデプロイするためのさまざまな重要なベスト プラクティスについて説明します。これらのベスト プラクティスに従うことで、パブリック クラウドでの TiDB デプロイのパフォーマンス、コスト効率、信頼性、スケーラビリティを最大限に高めることができます。

## Raft Engine専用のディスクを使用する {#use-a-dedicated-disk-for-raft-engine}

TiKV の[Raft Engine](/glossary.md#raft-engine) 、従来のデータベースの先行書き込みログ (WAL) と同様の重要な役割を果たします。最適なパフォーマンスと安定性を実現するには、パブリック クラウドに TiDB を展開するときに、 Raft Engine専用のディスクを割り当てることが重要です。次の`iostat`書き込み負荷の高いワークロードを持つ TiKV ノードの I/O 特性を示しています。

    Device            r/s     rkB/s       w/s     wkB/s      f/s  aqu-sz  %util
    sdb           1649.00 209030.67   1293.33 304644.00    13.33    5.09  48.37
    sdd           1033.00   4132.00   1141.33  31685.33   571.00    0.94 100.00

デバイス`sdb`は KV RocksDB に使用され、 `sdd` Raft Engineログの復元に使用されます。5 には、デバイスの 1 秒あたりに完了したフラッシュ要求の数を表す`sdd` `f/s`値が大幅に高いことに注意してください。Raft Raft Engineでは、バッチ内の書き込みが同期としてマークされている場合、バッチ リーダーは書き込み後に`fdatasync()`呼び出し、バッファリングされたデータがstorageにフラッシュされることを保証します。Raft Raft Engine専用のディスクを使用することで、TiKV は要求の平均キュー長を短縮し、最適で安定した書き込みレイテンシーを保証します。

クラウド プロバイダーによって、IOPS や MBPS などのパフォーマンス特性が異なるさまざまなディスク タイプが提供されています。したがって、ワークロードに基づいて適切なクラウド プロバイダー、ディスク タイプ、ディスク サイズを選択することが重要です。

### パブリッククラウド上のRaft Engineに適したディスクを選択する {#choose-appropriate-disks-for-raft-engine-on-public-clouds}

このセクションでは、さまざまなパブリック クラウド上のRaft Engineに適したディスクを選択するためのベスト プラクティスについて説明します。パフォーマンス要件に応じて、2 種類の推奨ディスクが利用可能です。

#### ミドルレンジディスク {#middle-range-disk}

さまざまなパブリック クラウドに推奨されるミドルレンジ ディスクは次のとおりです。

-   AWS では、 [GP3 の](https://aws.amazon.com/ebs/general-purpose/)が推奨されます。gp3 ボリュームは、ボリューム サイズに関係なく、3000 IOPS と 125 MB/秒のスループットの無料割り当てを提供し、通常はRaft Engineには十分です。

-   Google Cloud では、 [pd-ssd](https://cloud.google.com/compute/docs/disks#disk-types/)が推奨されています。IOPS と MBPS は、割り当てられたディスク サイズによって異なります。パフォーマンス要件を満たすには、 Raft Engineに 200 GB を割り当てることをお勧めします。Raft Raft Engine はそれほど大きなスペースを必要としませんが、最適なパフォーマンスを保証します。

-   Azure では、 [プレミアム SSD v2](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#premium-ssd-v2)が推奨されます。AWS gp3 と同様に、Premium SSD v2 はボリューム サイズに関係なく、3000 IOPS と 125 MB/秒のスループットの無料割り当てを提供し、通常はRaft Engineには十分です。

#### ハイエンドディスク {#high-end-disk}

Raft Engineのレイテンシーをさらに低くしたい場合は、ハイエンド ディスクの使用を検討してください。以下は、さまざまなパブリック クラウドに推奨されるハイエンド ディスクです。

-   AWS では[io2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)推奨されます。ディスク サイズと IOPS は、特定の要件に応じてプロビジョニングできます。

-   Google Cloud では、 [pd-エクストリーム](https://cloud.google.com/compute/docs/disks#disk-types/)が推奨されます。ディスク サイズ、IOPS、MBPS をプロビジョニングできますが、64 個を超える CPU コアを持つインスタンスでのみ使用できます。

-   Azure では、 [ウルトラディスク](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#ultra-disks)が推奨されます。ディスク サイズ、IOPS、および MBPS は、特定の要件に応じてプロビジョニングできます。

### 例 1: AWS でソーシャル ネットワーク ワークロードを実行する {#example-1-run-a-social-network-workload-on-aws}

AWS は、20 GB [GP3 の](https://aws.amazon.com/ebs/general-purpose/)ボリュームに対して 3000 IOPS と 125 MBPS/秒を提供します。

書き込み集中型のソーシャル ネットワーク アプリケーション ワークロードに AWS 上の専用の 20 GB [GP3 の](https://aws.amazon.com/ebs/general-purpose/) Raft Engineディスクを使用すると、次のような改善が見られますが、推定コストは 0.4% しか増加しません。

-   QPS（1秒あたりのクエリ数）が17.5%増加
-   挿入文の平均レイテンシーが18.7%減少
-   挿入ステートメントの p99レイテンシーが 45.6% 減少しました。

| メトリック          | 共有Raft Engineディスク | 専用Raft Engineディスク | 違い （％） |
| -------------- | ----------------- | ----------------- | ------ |
| QPS (K/秒)      | 8.0               | 9.4               | 17.5   |
| 平均挿入遅延時間 (ミリ秒) | 11.3              | 9.2               | -18.7  |
| P99 挿入遅延 (ms)  | 29.4              | 16.0              | -45.6  |

### 例 2: Azure で TPC-C/Sysbench ワークロードを実行する {#example-2-run-tpc-c-sysbench-workload-on-azure}

Azure 上のRaft Engineに専用の 32 GB [ウルトラディスク](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#ultra-disks)を使用すると、次の改善が見られます。

-   Sysbench `oltp_read_write`ワークロード: QPS が 17.8% 増加し、平均レイテンシーが 15.6% 減少しました。
-   TPC-C ワークロード: QPS が 27.6% 増加し、平均レイテンシーが 23.1% 減少しました。

| メトリック        | 作業負荷                     | 共有Raft Engineディスク | 専用Raft Engineディスク | 違い （％） |
| ------------ | ------------------------ | ----------------- | ----------------- | ------ |
| QPS (K/秒)    | システムベンチ`oltp_read_write` | 60.7              | 71.5              | 17.8   |
| QPS (K/秒)    | TPC-C                    | 23.9              | 30.5              | 27.6   |
| 平均レイテンシ（ミリ秒） | システムベンチ`oltp_read_write` | 4.5               | 3.8               | -15.6  |
| 平均レイテンシ（ミリ秒） | TPC-C                    | 3.9               | 3.0               | -23.1  |

### 例 3: TiKV マニフェストのRaft Engine用に Google Cloud に専用の pd-ssd ディスクを接続する {#example-3-attach-a-dedicated-pd-ssd-disk-on-google-cloud-for-raft-engine-on-tikv-manifest}

次の TiKV 構成例は、 [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable)によってデプロイされた Google Cloud 上のクラスタに追加の 512 GB [pd-ssd](https://cloud.google.com/compute/docs/disks#disk-types/)ディスクを接続し、この特定のディスクにRaft Engineログを保存するように`raft-engine.dir`構成する方法を示しています。

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

## KV RocksDB の圧縮 I/O フローを削減 {#reduce-compaction-i-o-flow-in-kv-rocksdb}

TiKV のstorageエンジンとして、 [ロックスDB](https://rocksdb.org/)ユーザー データの保存に使用されます。クラウド EBS にプロビジョニングされた IO スループットは、通常、コスト上の理由から制限されるため、RocksDB は高い書き込み増幅を示し、ディスク スループットがワークロードのボトルネックになる可能性があります。その結果、保留中の圧縮バイトの総数は時間の経過とともに増加し、フロー制御がトリガーされます。これは、TiKV がフォアグラウンド書き込みフローに対応するのに十分なディスク帯域幅を持っていないことを示しています。

ディスク スループットの制限によって発生するボトルネックを軽減するには、RocksDB の圧縮レベルを上げてディスク スループットを下げることでパフォーマンスを向上させることができます。たとえば、次の例を参考にして、デフォルトのカラムファミリーのすべての圧縮レベルを`zstd`に上げることができます。

    [rocksdb.defaultcf]
    compression-per-level = ["zstd", "zstd", "zstd", "zstd", "zstd", "zstd", "zstd"]

## AZ間ネットワークトラフィックのコストを最適化する {#optimize-cost-for-cross-az-network-traffic}

複数のアベイラビリティ ゾーン (AZ) にまたがって TiDB を展開すると、AZ 間のデータ転送料金によりコストが増加する可能性があります。コストを最適化するには、AZ 間のネットワーク トラフィックを削減することが重要です。

AZ 間の読み取りトラフィックを削減するには、 [Follower Read機能](/follower-read.md)を有効にします。これにより、TiDB は同じアベイラビリティーゾーン内のレプリカの選択を優先できます。この機能を有効にするには、 [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)変数を`closest-replicas`または`closest-adaptive`に設定します。

TiKV インスタンスの AZ 間書き込みトラフィックを削減するには、データをネットワーク経由で送信する前に圧縮する gRPC 圧縮機能を有効にします。次の設定例は、TiKV で gzip gRPC 圧縮を有効にする方法を示しています。

    server_configs:
      tikv:
        server.grpc-compression-type: gzip

TiFlash MPP タスクのデータ シャッフルによって発生するネットワーク トラフィックを削減するには、同じアベイラビリティ ゾーン (AZ) に複数のTiFlashインスタンスをデプロイすることをお勧めします。v6.6.0 以降では、デフォルトで[圧縮交換](/explain-mpp.md#mpp-version-and-exchange-data-compression)が有効になっており、MPP データ シャッフルによって発生するネットワーク トラフィックが削減されます。

## Google Cloud でのライブ マイグレーション メンテナンス イベントを軽減する {#mitigate-live-migration-maintenance-events-on-google-cloud}

Google Cloud の[ライブマイグレーション機能](https://cloud.google.com/compute/docs/instances/live-migration-process)を使用すると、ダウンタイムを発生させることなく、ホスト間で VM をシームレスに移行できます。ただし、これらの移行イベントは、頻度は低いものの、TiDB クラスタで実行されている VM を含む VM のパフォーマンスに大きな影響を与える可能性があります。このようなイベントが発生すると、影響を受ける VM のパフォーマンスが低下し、TiDB クラスタでのクエリ処理時間が長くなる可能性があります。

Google Cloud によって開始されたライブ マイグレーション イベントを検出し、これらのイベントによるパフォーマンスへの影響を軽減するために、TiDB は Google のメタデータ[例](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/metadata/main.py)に基づいた[スクリプトを見る](https://github.com/PingCAP-QE/tidb-google-maintenance)を提供します。このスクリプトを TiDB、TiKV、PD ノードにデプロイして、メンテナンス イベントを検出できます。メンテナンス イベントが検出されると、中断を最小限に抑え、クラスタの動作を最適化するために、次のように適切なアクションが自動的に実行されます。

-   TiDB: TiDB ノードをオフラインにし、TiDB ポッドを削除します。これは、TiDB インスタンスのノード プールが自動スケールに設定され、TiDB 専用になっていることを前提としています。ノードで実行されている他のポッドは中断される可能性があり、閉鎖されたノードは自動スケーラーによって再利用されることが予想されます。
-   TiKV: メンテナンス中に影響を受ける TiKV ストアのリーダーを削除します。
-   PD: 現在の PD インスタンスが PD リーダーである場合、リーダーを辞任します。

この監視スクリプトは、Kubernetes 環境での TiDB の強化された管理機能を提供する[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/dev/tidb-operator-overview)を使用してデプロイされた TiDB クラスター用に特別に設計されていることに注意してください。

監視スクリプトを活用し、メンテナンス イベント中に必要なアクションを実行することで、TiDB クラスタは Google Cloud 上のライブ マイグレーション イベントをより適切に処理し、クエリ処理と応答時間への影響を最小限に抑えながら、よりスムーズな操作を実現できます。

## 高QPSの大規模TiDBクラスタのPDをチューニングする {#tune-pd-for-a-large-scale-tidb-cluster-with-high-qps}

TiDB クラスターでは、TSO (Timestamp Oracle) の提供やリクエストの処理などの重要なタスクを処理するために、単一のアクティブな Placement Driver (PD)サーバーが使用されます。ただし、単一のアクティブな PDサーバーに依存すると、TiDB クラスターのスケーラビリティが制限される可能性があります。

### PD制限の症状 {#symptoms-of-pd-limitation}

次の図は、それぞれ 56 個の CPU を搭載した 3 台の PD サーバーで構成された大規模 TiDB クラスターの症状を示しています。これらの図から、1 秒あたりのクエリ (QPS) が 100 万を超え、1 秒あたりの TSO (Timestamp Oracle) リクエストが 162,000 を超えると、CPU 使用率が約 4,600% に達することがわかります。この高い CPU 使用率は、PD リーダーに大きな負荷がかかっており、利用可能な CPU リソースが不足していることを示しています。

![pd-server-cpu](/media/performance/public-cloud-best-practice/baseline_cpu.png) ![pd-server-metrics](/media/performance/public-cloud-best-practice/baseline_metrics.png)

### PDパフォーマンスの調整 {#tune-pd-performance}

PDサーバーでの CPU 使用率が高い問題を解決するには、次のチューニング調整を行うことができます。

#### PD設定を調整する {#adjust-pd-configuration}

[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) : このパラメータは、PDサーバーが物理 TSO バッチを更新する間隔を制御します。間隔を短くすると、PDサーバーはTSO バッチをより頻繁に割り当てることができ、次の割り当ての待機時間を短縮できます。

    tso-update-physical-interval = "10ms" # default: 50ms

#### TiDBグローバル変数を調整する {#adjust-a-tidb-global-variable}

PD 構成に加えて、TSO クライアント バッチ待機機能を有効にすると、TSO クライアントの動作をさらに最適化できます。この機能を有効にするには、グローバル変数[`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)ゼロ以外の値に設定します。

    set global tidb_tso_client_batch_max_wait_time = 2; # default: 0

#### TiKV設定を調整する {#adjust-tikv-configuration}

リージョンの数を減らし、システムのハートビートビートのオーバーヘッドを軽減するには、TiKV 構成のリージョンサイズを`96MB`から`256MB`に増やすことをお勧めします。

    [coprocessor]
      region-split-size = "256MB"

## チューニング後 {#after-tuning}

チューニング後、次の効果が見られます。

-   1 秒あたりの TSO リクエストは 64,800 に減少します。
-   CPU 使用率は約 4,600% から 1,400% に大幅に削減されます。
-   P999 値`PD server TSO handle time`が 2ms から 0.5ms に減少します。

これらの改善は、チューニング調整によって、安定した TSO 処理パフォーマンスを維持しながら、PDサーバーの CPU 使用率を正常に削減できたことを示しています。

![pd-server-cpu](/media/performance/public-cloud-best-practice/after_tuning_cpu.png) ![pd-server-metrics](/media/performance/public-cloud-best-practice/after_tuning_metrics.png)
