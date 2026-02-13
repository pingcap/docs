---
title: Best Practices for Tuning TiKV Performance with Massive Regions
summary: TiKVのパフォーマンスチューニングには、リージョンとメッセージ数の削減、 Raftstoreの同時実行性の向上、Hibernateリージョンとリージョンマージの有効化、 Raftベースのティック間隔の調整、TiKVインスタンスの増加、リージョンサイズの調整が含まれます。その他の問題としては、PDリーダーの切り替え速度の低下やPDルーティング情報の古さなどが挙げられます。
aliases: ['/ja/tidb/stable/massive-regions-best-practices/','/ja/tidb/dev/massive-regions-best-practices/']
---

# 大規模リージョンでの TiKV パフォーマンスのチューニングに関するベストプラクティス {#best-practices-for-tuning-tikv-performance-with-massive-regions}

TiDBでは、データはリージョンに分割され、各リージョンには特定のキー範囲のデータが格納されます。これらのリージョンは複数のTiKVインスタンスに分散されています。データがクラスターに書き込まれると、数百万ものリージョンが作成されることがあります。単一のTiKVインスタンスにリージョンが多すぎると、クラスターに大きな負荷がかかり、パフォーマンスに影響を与える可能性があります。

このドキュメントでは、 Raftstore (TiKV のコア モジュール) のワークフローを紹介し、大量のリージョンがパフォーマンスに影響を与える理由を説明し、TiKV のパフォーマンスを調整する方法を示します。

## Raftstoreワークフロー {#raftstore-workflow}

TiKVインスタンスには複数のリージョンが存在します。RaftstoreRaftstoreはRaftステートマシンを駆動し、リージョンメッセージを処理します。これらのメッセージには、リージョンに対する読み取りまたは書き込みリクエストの処理、 Raftログの永続化または複製、 Raftハートビートの処理が含まれます。ただし、リージョン数の増加はクラスター全体のパフォーマンスに影響を与える可能性があります。これを理解するには、以下に示すRaftstoreのワークフローを理解する必要があります。

![Raftstore Workflow](/media/best-practices/raft-process.png)

> **注記：**
>
> この図はRaftstoreのワークフローを示すものであり、実際のコード構造を表すものではありません。

上の図から、TiDB サーバーからのリクエストは、gRPC モジュールとstorageモジュールを通過した後、KV (キーと値のペア) の読み取りおよび書き込みメッセージになり、対応するリージョンに送信されることがわかります。これらのメッセージはすぐに処理されず、一時的に保存されます。Raftstoreは、各リージョンに処理するメッセージがあるかどうかをポーリングして確認します。リージョンに処理するメッセージがある場合、 Raftstore はこのリージョンのRaftステート マシンを駆動してこれらのメッセージを処理し、これらのメッセージの状態変化に応じて後続の操作を実行します。たとえば、書き込みリクエストが到着すると、 Raftステート マシンはログをディスクに保存し、他のリージョンのレプリカにログを送信します。ハートビート間隔に達すると、 Raftステート マシンはハートビート情報を他のリージョンのレプリカに送信します。

## パフォーマンスの問題 {#performance-problem}

Raftstore のワークフロー図から、各リージョンのメッセージは1つずつ処理されます。リージョンの数が多い場合、 Raftstore は各リージョンのハートビートを処理するのに時間がかかり、遅延が発生する可能性があります。その結果、一部の読み取りおよび書き込みリクエストが時間内に処理されない場合があります。読み取りおよび書き込みの負荷が高い場合、 Raftstoreスレッドの CPU 使用率がボトルネックになりやすく、遅延がさらに増加し​​てパフォーマンスに影響を及ぼします。

一般的に、ロードされたRaftstoreのCPU使用率が85%以上に達すると、 Raftstoreはビジー状態になり、ボトルネックとなります。同時に、 `propose wait duration`数百ミリ秒に達することもあります。

> **注記：**
>
> -   前述のRaftstoreのCPU使用率についてですが、 Raftstoreはシングルスレッドです。Raftstoreがマルチスレッドの場合は、CPU使用率のしきい値（85%）を比例的に増やすことができます。
> -   Raftstoreスレッドには I/O 操作が存在するため、CPU 使用率は 100% に達することはありません。

### パフォーマンス監視 {#performance-monitoring}

Grafana の**TiKV ダッシュボード**では、次の監視メトリックを確認できます。

-   **スレッドCPU**パネルの`Raft store CPU`

    基準値： `raftstore.store-pool-size * 85%`未満。

    ![Check Raftstore CPU](/media/best-practices/raft-store-cpu.png)

-   **Raft Propose**パネルの`Propose wait duration`

    `Propose wait duration`は、リクエストがRaftstoreに送信されてからRaftstore が実際にリクエストの処理を開始するまでの遅延です。遅延が長い場合は、 Raftstoreがビジー状態であるか、ログ追加処理に時間がかかり、 Raftstore がリクエストを時間内に処理できないことを意味します。

    基準値: クラスターサイズに応じて50～100ms未満

    ![Check Propose wait duration](/media/best-practices/propose-wait-duration.png)

-   **Raft IO**パネルの`Commit log duration`

    `Commit log duration`は、 Raftstore が各リージョン内の大多数のメンバーにRaftログをコミットするのにかかる時間です。この指標の値が大きく変動する理由としては、以下が考えられます。

    -   Raftstoreの作業負荷は大きいです。
    -   ログ追加操作が遅いです。
    -   ネットワークの混雑により、 Raftログをタイムリーにコミットできません。

    基準値: 200～500ms未満。

    ![Check Commit log duration](/media/best-practices/commit-log-duration.png)

## パフォーマンスチューニング方法 {#performance-tuning-methods}

パフォーマンスの問題の原因を突き止めたら、次の 2 つの側面から解決を試みてください。

-   単一の TiKV インスタンス上のリージョン数を減らす
-   単一リージョンのメッセージ数を減らす

### 方法1: Raftstoreの同時実行性を高める {#method-1-increase-raftstore-concurrency}

Raftstore はTiDB v3.0 以降、マルチスレッド モジュールにアップグレードされており、 Raftstoreスレッドがボトルネックになる可能性が大幅に減少しています。

TiKVでは、デフォルトで`raftstore.store-pool-size`から`2`に設定されています。Raftstoreでボトルネックが発生する場合は、実際の状況に応じてこの設定項目の値を適切に増やすことができます。ただし、不要なスレッド切り替えのオーバーヘッドを回避するため、この値を高くしすぎないことをお勧めします。

### 方法2: 休止状態リージョンを有効にする {#method-2-enable-hibernate-region}

実際の状況では、読み取りおよび書き込みリクエストはすべてのリージョンに均等に分散されるわけではなく、一部のリージョンに集中します。そのため、一時的にアイドル状態のリージョンにおけるRaftリーダーとフォロワー間のメッセージ数を最小限に抑えることができます。これはHibernate リージョンの機能です。この機能により、 Raftstoreはアイドル状態のリージョンのRaftステートマシンに、必要がない限りティックメッセージを送信しません。そのため、これらのRaftステートマシンはハートビートメッセージを生成するためにトリガーされることがなくなり、 Raftstoreのワークロードを大幅に軽減できます。

[TiKVマスター](https://github.com/tikv/tikv/tree/master)では、Hibernate リージョン がデフォルトで有効になっています。この機能は必要に応じて設定できます。詳細は[Hibernateリージョンを構成する](/tikv-configuration-file.md)を参照してください。

### 方法3: <code>Region Merge</code>を有効にする {#method-3-enable-code-region-merge-code}

> **注記：**
>
> TiDB v3.0 以降では`Region Merge`がデフォルトで有効になっています。

`Region Merge`有効にすることで、Regionの数を減らすこともできます。3 `Region Split`は異なり、 `Region Merge`スケジュール設定によって隣接する小さなRegionを結合するプロセスです。データを削除した後、または`Drop Table`もしくは`Truncate Table`ステートメントを実行した後、小さなRegion、あるいは空のRegionを結合することで、リソース消費を削減できます。

次のパラメータを設定して`Region Merge`有効にします。

    config set max-merge-region-size 54
    config set max-merge-region-keys 540000
    config set merge-schedule-limit 8

詳細については、 [リージョン結合](https://tikv.org/docs/4.0/tasks/configure/region-merge/)および[PD設定ファイル](/pd-configuration-file.md#schedule)の次の 3 つの構成パラメータを参照してください。

-   [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size)
-   [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys)
-   [`merge-schedule-limit`](/pd-configuration-file.md#merge-schedule-limit)

`Region Merge`パラメータのデフォルト設定はかなり保守的です。5 [PDスケジュールのベストプラクティス](/best-practices/pd-scheduling-best-practices.md#region-merge-is-slow)記載されている方法を参考にすれば、 `Region Merge`プロセスを高速化できます。

### 方法4: TiKVインスタンスの数を増やす {#method-4-increase-the-number-of-tikv-instances}

I/O リソースと CPU リソースが十分な場合は、単一のマシンに複数の TiKV インスタンスをデプロイして、単一の TiKV インスタンス上のリージョンの数を減らすことも、TiKV クラスター内のマシンの数を増やすこともできます。

### 方法5: <code>raft-base-tick-interval</code>を調整する {#method-5-adjust-code-raft-base-tick-interval-code}

リージョン数を減らすだけでなく、単位時間あたりに各リージョンに送信されるメッセージ数を減らすことで、 Raftstoreへの負荷を軽減することもできます。例えば、 `raft-base-tick-interval`設定項目の値を適切に増やすことができます。

    [raftstore]
    raft-base-tick-interval = "2s"

上記の設定では、 `raft-base-tick-interval` Raftstore が各リージョンのRaftステートマシンを駆動する時間間隔です。つまり、この時間間隔でRaftstore はRaftステートマシンに tick メッセージを送信します。この間隔を長くすることで、 Raftstoreからのメッセージ数を効果的に減らすことができます。

ティックメッセージ間のこの間隔は、 `election timeout`と`heartbeat`の間の間隔も決定することに注意してください。次の例をご覧ください。

    raft-election-timeout = raft-base-tick-interval * raft-election-timeout-ticks
    raft-heartbeat-interval = raft-base-tick-interval * raft-heartbeat-ticks

リージョンフォロワーが`raft-election-timeout`間隔以内にリーダーからのハートビートを受信しなかった場合、これらのフォロワーはリーダーが故障したと判断し、新たな選出を開始します。3 `raft-heartbeat-interval` 、リーダーがフォロワーにハートビートを送信する間隔です。したがって、この値を`raft-base-tick-interval`に増やすと、 Raftステートマシンから送信されるネットワークメッセージの数は減りますが、 Raftステートマシンがリーダーの故障を検出するまでの時間が長くなります。

### 方法6:リージョンのサイズを調整する {#method-6-adjust-region-size}

リージョンのデフォルトサイズは256MiBです。リージョンのサイズを大きくすることで、リージョンの数を減らすことができます。詳細については、 [リージョンパフォーマンスの調整](/tune-region-performance.md)ご覧ください。

> **注記：**
>
> v8.4.0以降、デフォルトのリージョンサイズが96MiBから256MiBに増加しました。リージョンサイズを手動で変更していない場合、TiKVクラスターをv8.4.0以降にアップグレードすると、TiKVクラスターのデフォルトのリージョンサイズは自動的に256MiBに更新されます。

> **注記：**
>
> リージョンサイズのカスタマイズは、TiDB v6.5.0 より前のバージョンでは実験的機能です。リージョンサイズを変更する必要がある場合は、v6.5.0 以降にアップグレードすることをお勧めします。

### 方法7: Raft通信の最大接続数を増やす {#method-7-increase-the-maximum-number-of-connections-for-raft-communication}

TiKVノード間のRaft通信に使用される最大接続数を調整するには、 [`server.grpc-raft-conn-num`](/tikv-configuration-file.md#grpc-raft-conn-num)設定項目を変更します。この数を増やすと、多数のリージョンによる通信負荷の増大によって発生するブロックの問題を軽減できます。

> **注記：**
>
> 不要なスレッド切り替えのオーバーヘッドを削減し、バッチ処理による潜在的な悪影響を軽減するには、数値を`[1, 4]`の範囲内に設定することをお勧めします。

## その他の問題と解決策 {#other-problems-and-solutions}

このセクションでは、その他の問題と解決策について説明します。

### PDLeaderの切り替えが遅い {#switching-pd-leader-is-slow}

PDは、PDLeaderノードの切り替え後、迅速にリージョンルーティングサービスを再開できるように、etcdにリージョンメタ情報を保持する必要があります。リージョン数が増えると、etcdのパフォーマンス問題が発生し、PDがリーダーLeaderを切り替える際に、etcdからリージョンメタ情報を取得するのに時間がかかります。数百万のリージョンが存在する場合、etcdからメタ情報を取得するのに10秒以上、場合によっては数十秒かかることがあります。

この問題に対処するため、TiDB v3.0以降、PDではデフォルトで`use-region-storage`有効になっています。この機能を有効にすると、PDはリージョンメタ情報をローカルLevelDBに保存し、他のメカニズムを通じてPDノード間で情報を同期します。

### PDルーティング情報が時間内に更新されない {#pd-routing-information-is-not-updated-in-time}

TiKVでは、pd-workerが定期的にリージョンメタ情報をPDに報告します。TiKVが再起動されたり、リージョンリーダーが切り替わったりすると、PDは統計情報に基づいてリージョン`approximate size / keys`を再計算する必要があります。そのため、リージョン数が多い場合、シングルスレッドのpd-workerがボトルネックとなり、タスクが滞留して処理が間に合わない可能性があります。このような状況では、PDは特定のリージョンメタ情報を時間内に取得できず、ルーティング情報が時間内に更新されません。この問題は実際の読み取りや書き込みには影響しませんが、PDのスケジューリングが不正確になり、TiDBがリージョンキャッシュを更新する際に複数のラウンドトリップが必要になる可能性があります。

**TiKV Grafana**パネルの**「Task」**の下にある**「Worker pending tasks」**を確認することで、pd-workerにタスクが蓄積されているかどうかを確認できます。一般的に、 `pending tasks`値は比較的低い値に抑えておく必要があります。

![Check pd-worker](/media/best-practices/pd-worker-metrics.png)

pd-workerは[バージョン3.0.5](/releases/release-3.0.5.md#tikv)以降、パフォーマンス向上のために最適化されています。同様の問題が発生した場合は、最新バージョンへのアップグレードをお勧めします。

### Prometheusはメトリクスのクエリが遅い {#prometheus-is-slow-to-query-metrics}

大規模クラスターでは、TiKVインスタンスの数が増えるにつれて、Prometheusがメトリクスをクエリする負荷が高まり、Grafanaによるメトリクスの表示速度が低下します。この問題を軽減するために、v3.0以降ではメトリクスの事前計算が設定されています。
