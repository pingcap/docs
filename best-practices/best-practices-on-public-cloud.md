---
title: TiDB Best Practices on Public Cloud
summary: パブリック クラウドに TiDB をデプロイするためのベスト プラクティスについて説明します。
aliases: ['/ja/tidb/stable/best-practices-on-public-cloud/','/ja/tidb/dev/best-practices-on-public-cloud/']
---

# パブリッククラウドに TiDB を導入するためのベストプラクティス {#best-practices-for-deploying-tidb-on-public-cloud}

パブリッククラウドインフラストラクチャは、TiDBの導入と管理においてますます人気の選択肢となっています。しかし、パブリッククラウドにTiDBを導入するには、パフォーマンスチューニング、コスト最適化、信頼性、スケーラビリティなど、いくつかの重要な要素を慎重に検討する必要があります。

このドキュメントでは、KV RocksDB におけるコンパクション I/O フローの削減、 Raft Engine専用ディスクの使用、AZ 間トラフィックのコスト最適化、Google Cloud ライブマイグレーションイベントの軽減、大規模クラスタにおける PDサーバーの微調整など、パブリッククラウドへの TiDB の導入に関する様々な重要なベストプラクティスを解説します。これらのベストプラクティスに従うことで、パブリッククラウドにおける TiDB 導入のパフォーマンス、コスト効率、信頼性、スケーラビリティを最大限に高めることができます。

## KV RocksDB の圧縮 I/O フローを削減 {#reduce-compaction-i-o-flow-in-kv-rocksdb}

TiKVのstorageエンジンである[ロックスDB](https://rocksdb.org/) 、ユーザーデータの保存に使用されます。クラウドEBSのプロビジョニングされたIOスループットは通常、コスト上の理由から制限されているため、RocksDBは書き込み増幅率が高くなり、ディスクスループットがワークロードのボトルネックになる可能性があります。その結果、保留中のコンパクションバイトの総数は時間の経過とともに増加し、フロー制御がトリガーされます。これは、TiKVがフォアグラウンド書き込みフローに対応するための十分なディスク帯域幅を欠いていることを示しています。

ディスクスループットの制限によるボトルネックを軽減するには、パフォーマンスを[タイタンを有効にする](#enable-titan)向上させることができます。平均行サイズが 512 バイト未満の場合は、Titan は適用できません。この場合、パフォーマンスを[すべての圧縮レベルを上げる](#increase-all-the-compression-levels)向上させることができます。

### タイタンを有効にする {#enable-titan}

[タイタン](/storage-engine/titan-overview.md)は、キーと値の分離のための高性能な[ロックスDB](https://github.com/facebook/rocksdb)プラグインであり、大きな値が使用されるときに RocksDB での書き込み増幅を減らすことができます。

平均行サイズが 512 バイトより大きい場合は、次のように`min-blob-size` `"512B"`または`"1KB"`に設定し、 `blob-file-compression`を`"zstd"`に設定して、Titan による圧縮 I/O フローの削減を有効にすることができます。

```toml
[rocksdb.titan]
enabled = true
[rocksdb.defaultcf.titan]
min-blob-size = "1KB"
blob-file-compression = "zstd"
```

> **注記：**
>
> Titanを有効にすると、主キーの範囲スキャンのパフォーマンスが若干低下する可能性があります。詳細については、 [`min-blob-size`がパフォーマンスに与える影響](/storage-engine/titan-overview.md#impact-of-min-blob-size-on-performance)参照してください。

### すべての圧縮レベルを上げる {#increase-all-the-compression-levels}

平均行サイズが 512 バイトより小さい場合は、次のようにして、デフォルトのカラムファミリーのすべての圧縮レベルを`"zstd"`に増やすことができます。

```toml
[rocksdb.defaultcf]
compression-per-level = ["zstd", "zstd", "zstd", "zstd", "zstd", "zstd", "zstd"]
```

## Raft Engine専用のディスクを使用する {#use-a-dedicated-disk-for-raft-engine}

TiKVの[Raft Engine](/glossary.md#raft-engine) 、従来のデータベースにおける先行書き込みログ（WAL）と同様の重要な役割を果たします。最適なパフォーマンスと安定性を実現するには、パブリッククラウドにTiDBをデプロイする際に、 Raft Engine専用のディスクを割り当てることが不可欠です。次の`iostat` 、書き込み負荷の高いワークロードにおけるTiKVノードのI/O特性を示しています。

    Device            r/s     rkB/s       w/s     wkB/s      f/s  aqu-sz  %util
    sdb           1649.00 209030.67   1293.33 304644.00    13.33    5.09  48.37
    sdd           1033.00   4132.00   1141.33  31685.33   571.00    0.94 100.00

デバイス`sdb`はKV RocksDBに使用され、 `sdd` Raft Engineのログを復元するために使用されます`sdd`には、デバイスの1秒あたりのフラッシュ要求完了数を表す`f/s`値が大幅に高いことに注目してください。Raft Raft Engineでは、バッチ内の書き込みが同期としてマークされている場合、バッチリーダーは書き込み後に`fdatasync()`呼び出し、バッファリングされたデータがstorageにフラッシュされることを保証します。Raft Raft Engine専用のディスクを使用することで、TiKVはリクエストの平均キュー長を短縮し、最適で安定した書き込みレイテンシーを保証します。

クラウドプロバイダーによって、IOPSやMBPSなどのパフォーマンス特性が異なる様々なディスクタイプが提供されています。そのため、ワークロードに応じて適切なクラウドプロバイダー、ディスクタイプ、ディスクサイズを選択することが重要です。

### パブリッククラウド上のRaft Engineに適したディスクを選択する {#choose-appropriate-disks-for-raft-engine-on-public-clouds}

このセクションでは、さまざまなパブリッククラウド上でRaft Engineに適したディスクを選択するためのベストプラクティスについて説明します。パフォーマンス要件に応じて、2種類の推奨ディスクが用意されています。

#### ミドルレンジディスク {#middle-range-disk}

さまざまなパブリック クラウドに推奨されるミドルレンジ ディスクは次のとおりです。

-   AWSでは[gp3](https://aws.amazon.com/ebs/general-purpose/)推奨されます。gp3ボリュームは、ボリュームサイズに関係なく、3000 IOPSと125 MB/秒のスループットを無料で割り当てることができ、通常はRaft Engineに十分な値です。

-   Google Cloudでは[pd-ssd](https://cloud.google.com/compute/docs/disks#disk-types/)推奨されています。IOPSとMBPSは割り当てられたディスクサイズによって異なります。パフォーマンス要件を満たすには、 Raft Engineに200GBを割り当てることを推奨します。Raft Raft Engineはそれほど大きな容量を必要としませんが、最適なパフォーマンスを確保できます。

-   Azureでは[プレミアム SSD v2](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#premium-ssd-v2)推奨されます。AWS gp3と同様に、Premium SSD v2はボリュームサイズに関係なく、3000 IOPSと125 MB/秒のスループットを無料で割り当てることができ、通常はRaft Engineに十分です。

#### ハイエンドディスク {#high-end-disk}

Raft Engineのレイテンシーをさらに低減したい場合は、ハイエンドディスクの使用を検討してください。以下は、各パブリッククラウドで推奨されるハイエンドディスクです。

-   AWSでは[io2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)が推奨されます。ディスクサイズとIOPSは、お客様の特定の要件に応じてプロビジョニングできます。

-   Google Cloud では[pd-extreme](https://cloud.google.com/compute/docs/disks#disk-types/)推奨されます。ディスクサイズ、IOPS、MBPS をプロビジョニングできますが、64 個以上の CPU コアを持つインスタンスでのみ利用可能です。

-   Azure では[ウルトラディスク](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#ultra-disks)が推奨されます。ディスクサイズ、IOPS、MBPS は、お客様の特定の要件に応じてプロビジョニングできます。

### 例 1: AWS でソーシャル ネットワーク ワークロードを実行する {#example-1-run-a-social-network-workload-on-aws}

AWS は、20 GB [gp3](https://aws.amazon.com/ebs/general-purpose/)ボリュームに対して 3000 IOPS と 125 MBPS/s を提供します。

書き込み集中型のソーシャル ネットワーク アプリケーション ワークロードに AWS 上の専用の 20 GB [gp3](https://aws.amazon.com/ebs/general-purpose/) Raft Engineディスクを使用すると、次のような改善が見られますが、推定コストはわずか 0.4% しか増加しません。

-   QPS（1秒あたりのクエリ数）が17.5%増加
-   挿入文の平均レイテンシーが18.7%減少
-   挿入ステートメントの p99レイテンシーが 45.6% 減少しました。

| メトリック            | 共有Raft Engineディスク | 専用Raft Engineディスク | 違い （％） |
| ---------------- | ----------------- | ----------------- | ------ |
| QPS（K/秒）         | 8.0               | 9.4               | 17.5   |
| 平均挿入レイテンシ（ミリ秒）   | 11.3              | 9.2               | -18.7  |
| P99 挿入レイテンシ (ms) | 29.4              | 16.0              | -45.6  |

### 例 2: Azure で TPC-C/Sysbench ワークロードを実行する {#example-2-run-tpc-c-sysbench-workload-on-azure}

Azure 上のRaft Engineに専用の 32 GB [ウルトラディスク](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#ultra-disks)使用すると、次の改善が見られます。

-   Sysbench `oltp_read_write`ワークロード: QPS が 17.8% 増加し、平均レイテンシーが 15.6% 減少しました。
-   TPC-C ワークロード: QPS が 27.6% 増加し、平均レイテンシーが 23.1% 減少しました。

| メトリック        | 作業負荷                     | 共有Raft Engineディスク | 専用Raft Engineディスク | 違い （％） |
| ------------ | ------------------------ | ----------------- | ----------------- | ------ |
| QPS（K/秒）     | システムベンチ`oltp_read_write` | 60.7              | 71.5              | 17.8   |
| QPS（K/秒）     | TPC-C                    | 23.9              | 30.5              | 27.6   |
| 平均レイテンシ（ミリ秒） | システムベンチ`oltp_read_write` | 4.5               | 3.8               | -15.6  |
| 平均レイテンシ（ミリ秒） | TPC-C                    | 3.9               | 3.0               | -23.1  |

### 例 3: TiKV マニフェストのRaft Engine用に Google Cloud に専用の pd-ssd ディスクを接続する {#example-3-attach-a-dedicated-pd-ssd-disk-on-google-cloud-for-raft-engine-on-tikv-manifest}

次の TiKV 構成例は、 [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable)によってデプロイされた Google Cloud 上のクラスタに 512 GB の追加のディスク[pd-ssd](https://cloud.google.com/compute/docs/disks#disk-types/)を接続し、この特定のディスクにRaft Engineログを保存するように`raft-engine.dir`構成する方法を示しています。

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

## AZ間ネットワークトラフィックのコストを最適化する {#optimize-cost-for-cross-az-network-traffic}

TiDBを複数のアベイラビリティゾーン（AZ）にまたがってデプロイすると、AZ間のデータ転送料金によりコストが増加する可能性があります。コストを最適化するには、AZ間のネットワークトラフィックを削減することが重要です。

AZ間の読み取りトラフィックを削減するには、 [Follower Read機能](/follower-read.md)を有効にします。これにより、TiDBは同じアベイラビリティゾーン内のレプリカを優先的に選択します。この機能を有効にするには、 [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)変数を`closest-replicas`または`closest-adaptive`に設定します。

TiFlash MPPタスクのデータシャッフルによって発生するネットワークトラフィックを削減するため、複数のTiFlashインスタンスを同じアベイラビリティゾーン（AZ）にデプロイすることをお勧めします。v6.6.0以降では、 [圧縮交換](/explain-mpp.md#mpp-version-and-exchange-data-compression)デフォルトで有効になっており、MPPデータシャッフルによって発生するネットワークトラフィックを削減します。

## Google Cloud でのライブ マイグレーション メンテナンス イベントを軽減する {#mitigate-live-migration-maintenance-events-on-google-cloud}

Google Cloud の[ライブマイグレーション機能](https://cloud.google.com/compute/docs/instances/live-migration-process)は、ダウンタイムを発生させることなく、ホスト間でVMをシームレスに移行できます。しかし、これらの移行イベントは頻度は低いものの、TiDBクラスタで実行されているVMを含むVMのパフォーマンスに重大な影響を与える可能性があります。このようなイベントが発生すると、影響を受けるVMのパフォーマンスが低下し、TiDBクラスタでのクエリ処理時間が長くなる可能性があります。

Google Cloud によって開始されたライブマイグレーション イベントを検出し、これらのイベントによるパフォーマンスへの影響を軽減するために、TiDB は Google のメタデータ[例](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/metadata/main.py)に基づく[スクリプトを見る](https://github.com/PingCAP-QE/tidb-google-maintenance)提供します。このスクリプトを TiDB、TiKV、PD ノードにデプロイして、メンテナンス イベントを検出できます。メンテナンス イベントが検出されると、中断を最小限に抑え、クラスタの動作を最適化するために、次のように適切なアクションが自動的に実行されます。

-   TiDB: TiDBノードをオフラインにし、TiDBポッドを削除します。これは、TiDBインスタンスのノードプールが自動スケールに設定され、TiDB専用になっていることを前提としています。ノード上で実行されている他のポッドに中断が発生する可能性があり、切断されたノードは自動スケーラーによって回収されることが想定されます。
-   TiKV: メンテナンス中に、影響を受ける TiKV ストアのリーダーを削除します。
-   PD: 現在の PD インスタンスが PD リーダーである場合、リーダーを辞任します。

この監視スクリプトは、Kubernetes 環境での TiDB の強化された管理機能を提供する[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.6/tidb-operator-overview)を使用してデプロイされた TiDB クラスター用に特別に設計されていることに注意することが重要です。

監視スクリプトを活用し、メンテナンス イベント中に必要なアクションを実行することで、TiDB クラスタは Google Cloud 上のライブ マイグレーション イベントをより適切に処理し、クエリ処理と応答時間への影響を最小限に抑えながら、よりスムーズな操作を実現できます。

## 高QPSの大規模TiDBクラスタのPDをチューニングする {#tune-pd-for-a-large-scale-tidb-cluster-with-high-qps}

TiDBクラスタでは、TSO（Timestamp Oracle）の提供やリクエストの処理といった重要なタスクを、単一のアクティブなPlacement Driver （PD）サーバーで処理します。しかし、単一のアクティブなPDサーバーに依存すると、TiDBクラスタのスケーラビリティが制限される可能性があります。

### PD制限の症状 {#symptoms-of-pd-limitation}

以下の図は、それぞれ56個のCPUを搭載した3台のPDサーバーで構成される大規模TiDBクラスターの症状を示しています。これらの図から、1秒あたりのクエリ数（QPS）が100万を超え、1秒あたりのTSO（Timestamp Oracle）リクエスト数が162,000を超えると、CPU使用率が約4,600%に達することがわかります。この高いCPU使用率は、PDリーダーに大きな負荷がかかっており、利用可能なCPUリソースが不足していることを示しています。

![pd-server-cpu](/media/performance/public-cloud-best-practice/baseline_cpu.png) ![pd-server-metrics](/media/performance/public-cloud-best-practice/baseline_metrics.png)

### PDパフォーマンスの調整 {#tune-pd-performance}

PDサーバーでの CPU 使用率が高い問題を解決するには、次のチューニング調整を行うことができます。

#### PD設定を調整する {#adjust-pd-configuration}

[`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) : このパラメータは、PDサーバーが物理TSOバッチを更新する間隔を制御します。間隔を短くすることで、PDサーバーはTSOバッチをより頻繁に割り当てることができ、次の割り当てまでの待ち時間を短縮できます。

    tso-update-physical-interval = "10ms" # default: 50ms

#### TiDBグローバル変数を調整する {#adjust-a-tidb-global-variable}

PD設定に加えて、TSOクライアントのバッチ待機機能を有効にすると、TSOクライアントの動作をさらに最適化できます。この機能を有効にするには、グローバル変数[`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530) 0以外の値に設定します。

    set global tidb_tso_client_batch_max_wait_time = 2; # default: 0

#### TiKV設定を調整する {#adjust-tikv-configuration}

リージョンの数を減らし、システムのハートビートビートのオーバーヘッドを軽減するには、 [リージョンのサイズを調整する](/best-practices/massive-regions-best-practices.md#method-6-adjust-region-size)を参照して、TiKV 構成でリージョンのサイズを適度に増やすことができます。

    [coprocessor]
      region-split-size = "288MiB"

### チューニング後 {#after-tuning}

チューニング後、次の効果が見られます。

-   1 秒あたりの TSO リクエストは 64,800 に減少します。
-   CPU 使用率は約 4,600% から 1,400% に大幅に減少しました。
-   P999 値`PD server TSO handle time`が 2ms から 0.5ms に減少します。

これらの改善は、チューニング調整によって、安定した TSO 処理パフォーマンスを維持しながら、PDサーバーの CPU 使用率を正常に削減できたことを示しています。

![pd-server-cpu](/media/performance/public-cloud-best-practice/after_tuning_cpu.png) ![pd-server-metrics](/media/performance/public-cloud-best-practice/after_tuning_metrics.png)
