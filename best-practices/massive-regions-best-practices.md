---
title: Best Practices for TiKV Performance Tuning with Massive Regions
summary: Learn how to tune the performance of TiKV with a massive amount of Regions.
---

# 大規模なリージョンでのTiKV性能チューニングのベストプラクティス {#best-practices-for-tikv-performance-tuning-with-massive-regions}

TiDBでは、データはリージョンに分割され、各リージョンには特定のキー範囲のデータが格納されます。これらのリージョンは、複数のTiKVインスタンスに分散されています。データがクラスタに書き込まれると、数百万または数千万のリージョンが作成されます。 1つのTiKVインスタンスのリージョンが多すぎると、クラスターに大きな負担がかかり、クラスタのパフォーマンスに影響を与える可能性があります。

このドキュメントでは、Raftstore（TiKVのコアモジュール）のワークフローを紹介し、大量のリージョンがパフォーマンスに影響を与える理由を説明し、TiKVのパフォーマンスを調整する方法を提供します。

## Raftstoreワークフロー {#raftstore-workflow}

TiKVインスタンスには、複数のリージョンがあります。 Raftstoreモジュールは、Raftステートマシンを駆動してRegionメッセージを処理します。これらのメッセージには、リージョンでの読み取りまたは書き込み要求の処理、Raftログの永続化または複製、およびRaftハートビートの処理が含まれます。ただし、リージョンの数が増えると、クラスタ全体のパフォーマンスに影響を与える可能性があります。これを理解するには、次のようなRaftstoreのワークフローを学ぶ必要があります。

![Raftstore Workflow](/media/best-practices/raft-process.png)

> **ノート：**
>
> この図は、Raftstoreのワークフローを示しているだけであり、実際のコード構造を表すものではありません。

上の図から、TiDBサーバーからのリクエストは、gRPCおよびストレージモジュールを通過した後、KV（キー値）の読み取りおよび書き込みメッセージになり、対応するリージョンに送信されることがわかります。これらのメッセージはすぐには処理されませんが、一時的に保存されます。 Raftstoreはポーリングして、各リージョンに処理するメッセージがあるかどうかを確認します。リージョンに処理するメッセージがある場合、RaftstoreはこのリージョンのRaftステートマシンを駆動してこれらのメッセージを処理し、これらのメッセージの状態変化に従って後続の操作を実行します。たとえば、書き込み要求が着信すると、Raftステートマシンはログをディスクに保存し、他のリージョンレプリカにログを送信します。ハートビート間隔に達すると、ラフトステートマシンはハートビート情報を他のリージョンレプリカに送信します。

## パフォーマンスの問題 {#performance-problem}

Raftstoreワークフロー図から、各リージョンのメッセージが1つずつ処理されます。リージョンが多数存在する場合、Raftstoreがこれらのリージョンのハートビートを処理するのに時間がかかり、遅延が発生する可能性があります。その結果、一部の読み取りおよび書き込み要求は時間内に処理されません。読み取りと書き込みの負荷が高い場合、RaftstoreスレッドのCPU使用率がボトルネックになりやすく、遅延がさらに増加し、パフォーマンスに影響を与える可能性があります。

一般に、ロードされたRaftstoreのCPU使用率が85％以上に達すると、Raftstoreはビジー状態になり、ボトルネックになります。同時に、 `propose wait duration`は数百ミリ秒にもなる可能性があります。

> **ノート：**
>
> -   上記のRaftstoreのCPU使用率については、Raftstoreはシングルスレッドです。 Raftstoreがマルチスレッドの場合、CPU使用率のしきい値（85％）を比例して増やすことができます。
> -   I / O操作はRaftstoreスレッドに存在するため、CPU使用率を100％に到達させることはできません。

### パフォーマンス監視 {#performance-monitoring}

Grafanaの**TiKVダッシュボード**で次のモニタリング指標を確認できます。

-   **スレッドCPU**パネルの`Raft store CPU`

    基準値： `raftstore.store-pool-size * 85%`未満。

    ![Check Raftstore CPU](/media/best-practices/raft-store-cpu.png)

-   **RaftPropose**パネルの`Propose wait duration`

    `Propose wait duration`は、リクエストがRaftstoreに送信されてから、Raftstoreが実際にリクエストの処理を開始するまでの遅延です。遅延が長いということは、Raftstoreがビジーであるか、追加ログの処理に時間がかかり、Raftstoreが時間内にリクエストを処理できないことを意味します。

    基準値：クラスタサイズに応じて50〜100ms未満

    ![Check Propose wait duration](/media/best-practices/propose-wait-duration.png)

## パフォーマンスチューニング方法 {#performance-tuning-methods}

パフォーマンスの問題の原因を突き止めたら、次の2つの側面から解決してみてください。

-   単一のTiKVインスタンス上のリージョンの数を減らします
-   単一のリージョンのメッセージ数を減らす

### 方法1：Raftstoreの同時実行性を増やす {#method-1-increase-raftstore-concurrency}

Raftstoreは、TiDB v3.0以降、マルチスレッドモジュールにアップグレードされました。これにより、Raftstoreスレッドがボトルネックになる可能性が大幅に減少します。

デフォルトでは、TiKVでは`raftstore.store-pool-size`が`2`に設定されています。 Raftstoreでボトルネックが発生した場合は、実際の状況に応じて、この構成アイテムの値を適切に増やすことができます。ただし、不要なスレッドスイッチングのオーバーヘッドが発生しないように、この値を高く設定しすぎないようにすることをお勧めします。

### 方法2：休止状態領域を有効にする {#method-2-enable-hibernate-region}

実際の状況では、読み取りおよび書き込み要求はすべてのリージョンに均等に分散されているわけではありません。代わりに、それらはいくつかの地域に集中しています。次に、一時的にアイドル状態のリージョンのRaftリーダーとフォロワー間のメッセージの数を最小限に抑えることができます。これはHibernateリージョンの機能です。この機能では、Raftstoreは、必要がない場合、アイドル状態のリージョンのRaftステートマシンにティックメッセージを送信します。その場合、これらのRaftステートマシンはトリガーされてハートビートメッセージを生成しません。これにより、Raftstoreのワークロードを大幅に削減できます。

Hibernateリージョンはデフォルトで[TiKVマスター](https://github.com/tikv/tikv/tree/master)で有効になっています。この機能は、必要に応じて構成できます。詳しくは[Hibernateリージョンを構成する](/tikv-configuration-file.md)をご覧ください。

### 方法3： <code>Region Merge</code>有効にする {#method-3-enable-code-region-merge-code}

> **ノート：**
>
> TiDB v3.0以降、デフォルトで`Region Merge`が有効になっています。

`Region Merge`を有効にすることで、リージョンの数を減らすこともできます。 `Region Split`とは異なり、 `Region Merge`は、スケジューリングによって隣接する小さなリージョンをマージするプロセスです。データを削除するか、 `Drop Table`または`Truncate Table`ステートメントを実行した後、小さなリージョンまたは空のリージョンをマージして、リソースの消費を減らすことができます。

次のパラメータを設定して`Region Merge`を有効にします。

{{< copyable "" >}}

```
config set max-merge-region-size 20
config set max-merge-region-keys 200000
config set merge-schedule-limit 8
```

詳細については、 [リージョンマージ](https://tikv.org/docs/4.0/tasks/configure/region-merge/)および3の次の[PD構成ファイル](/pd-configuration-file.md#schedule)つの構成パラメーターを参照してください。

-   [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size)
-   [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys)
-   [`merge-schedule-limit`](/pd-configuration-file.md#merge-schedule-limit)

`Region Merge`つのパラメーターのデフォルト構成はかなり保守的です。 [PDスケジューリングのベストプラクティス](/best-practices/pd-scheduling-best-practices.md#region-merge-is-slow)で提供されている方法を参照することにより、 `Region Merge`のプロセスを高速化できます。

### 方法4：TiKVインスタンスの数を増やす {#method-4-increase-the-number-of-tikv-instances}

I / OリソースとCPUリソースが十分な場合は、単一のマシンに複数のTiKVインスタンスをデプロイして、単一のTiKVインスタンスのリージョンの数を減らすことができます。または、TiKVクラスタのマシンの数を増やすことができます。

### 方法5： <code>raft-base-tick-interval</code>調整する {#method-5-adjust-code-raft-base-tick-interval-code}

リージョンの数を減らすことに加えて、単位時間内に各リージョンのメッセージの数を減らすことで、Raftstoreへのプレッシャーを減らすこともできます。たとえば、 `raft-base-tick-interval`の構成アイテムの値を適切に増やすことができます。

{{< copyable "" >}}

```
[raftstore]
raft-base-tick-interval = "2s"
```

上記の構成では、 `raft-base-tick-interval`はRaftstoreが各リージョンのRaftステートマシンを駆動する時間間隔です。つまり、この時間間隔で、RaftstoreはティックメッセージをRaftステートマシンに送信します。この間隔を長くすると、Raftstoreからのメッセージの数を効果的に減らすことができます。

ティックメッセージ間のこの間隔は、 `election timeout`と`heartbeat`の間の間隔も決定することに注意してください。次の例を参照してください。

{{< copyable "" >}}

```
raft-election-timeout = raft-base-tick-interval * raft-election-timeout-ticks
raft-heartbeat-interval = raft-base-tick-interval * raft-heartbeat-ticks
```

リージョンフォロワーが`raft-election-timeout`間隔内にリーダーからハートビートを受信しなかった場合、これらのフォロワーはリーダーが失敗したと判断し、新しい選挙を開始します。 `raft-heartbeat-interval`は、リーダーがフォロワーにハートビートを送信する間隔です。したがって、値を`raft-base-tick-interval`に増やすと、Raftステートマシンから送信されるネットワークメッセージの数を減らすことができますが、Raftステートマシンがリーダーの障害を検出する時間が長くなります。

### 方法6：領域サイズを調整する {#method-6-adjust-region-size}

リージョンのデフォルトサイズは96MiBです。リージョンをより大きなサイズに設定することで、リージョンの数を減らすことができます。詳細については、 [リージョンのパフォーマンスを調整する](/tune-region-performance.md)を参照してください。

> **警告：**
>
> 現在、カスタマイズされたリージョンサイズは、TiDBv6.1.0で導入された実験的機能です。実稼働環境で使用することはお勧めしません。リスクは次のとおりです。
>
> -   パフォーマンスジッターが発生する可能性があります。
> -   特に広範囲のデータを処理するクエリの場合、クエリのパフォーマンスが低下する可能性があります。
> -   リージョンのスケジューリングが遅くなります。

## その他の問題と解決策 {#other-problems-and-solutions}

このセクションでは、その他の問題と解決策について説明します。

### PDリーダーの切り替えが遅い {#switching-pd-leader-is-slow}

PDは、PDリーダーノードを切り替えた後、PDがリージョンルーティングサービスの提供を迅速に再開できるように、etcdにリージョンメタ情報を保持する必要があります。リージョンの数が増えると、etcdのパフォーマンスの問題が発生し、PDがリーダーを切り替えているときにPDがetcdからリージョンメタ情報を取得するのが遅くなります。数百万のリージョンでは、etcdからメタ情報を取得するのに10秒以上または数十秒かかる場合があります。

この問題に対処するために、TiDB v3.0以降、PDではデフォルトで`use-region-storage`が有効になっています。この機能を有効にすると、PDはリージョンメタ情報をローカルLevelDBに保存し、他のメカニズムを介してPDノード間で情報を同期します。

### PDルーティング情報が時間内に更新されない {#pd-routing-information-is-not-updated-in-time}

TiKVでは、pd-workerはRegionMeta情報をPDに定期的に報告します。 TiKVが再起動されるか、リージョンリーダーが切り替わると、PDは統計を通じてリージョン`approximate size / keys`を再計算する必要があります。したがって、リージョンの数が多いと、シングルスレッドのpd-workerがボトルネックになり、タスクが積み重なって時間内に処理されない可能性があります。この状況では、PDは特定のRegion Meta情報を時間内に取得できないため、ルーティング情報は時間内に更新されません。この問題は実際の読み取りと書き込みには影響しませんが、不正確なPDスケジューリングを引き起こし、TiDBがリージョンキャッシュを更新するときに数回のラウンドトリップが必要になる可能性があります。

**TiKV Grafana**パネルの<strong>[タスク</strong>]で[<strong>ワーカーの保留中のタスク</strong>]を確認して、pd-workerにタスクが積み上げられているかどうかを確認できます。一般に、 `pending tasks`は比較的低い値に保つ必要があります。

![Check pd-worker](/media/best-practices/pd-worker-metrics.png)

pd-workerは、 [v3.0.5](/releases/release-3.0.5.md#tikv)以降、パフォーマンスが向上するように最適化されています。同様の問題が発生した場合は、最新バージョンにアップグレードすることをお勧めします。

### Prometheusはメトリックのクエリに時間がかかります {#prometheus-is-slow-to-query-metrics}

大規模なクラスタでは、TiKVインスタンスの数が増えると、Prometheusはメトリックのクエリに大きなプレッシャーをかけ、Grafanaがこれらのメトリックを表示するのが遅くなります。この問題を緩和するために、v3.0以降、メトリックの事前計算が構成されています。
