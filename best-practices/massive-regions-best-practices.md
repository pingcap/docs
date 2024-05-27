---
title: Best Practices for TiKV Performance Tuning with Massive Regions
summary: TiKV パフォーマンス チューニングには、リージョンとメッセージの数の削減、 Raftstore の同時実行性の向上、Hibernateリージョンとリージョンマージの有効化、 Raftベースのティック間隔の調整、TiKV インスタンスの増加、リージョンサイズの調整が含まれます。その他の問題としては、PD リーダーの切り替えが遅いことや、PD ルーティング情報が古くなっていることなどがあります。
---

# 大規模リージョンでの TiKV性能チューニングのベスト プラクティス {#best-practices-for-tikv-performance-tuning-with-massive-regions}

TiDB では、データはリージョンに分割され、各リージョンには特定のキー範囲のデータが格納されます。これらのリージョンは、複数の TiKV インスタンスに分散されます。データがクラスターに書き込まれると、数百万のリージョンが作成されることがあります。単一の TiKV インスタンス上のリージョンが多すぎると、クラスターに大きな負荷がかかり、パフォーマンスに影響する可能性があります。

このドキュメントでは、 Raftstore (TiKV のコア モジュール) のワークフローを紹介し、大量のリージョンがパフォーマンスに影響を与える理由を説明し、TiKV のパフォーマンスを調整する方法を示します。

## Raftstoreワークフロー {#raftstore-workflow}

TiKV インスタンスには複数のリージョンがあります。Raftstore モジュールは、 Raftステート マシンを駆動してリージョンメッセージを処理します。これらのメッセージには、リージョンでの読み取りまたは書き込み要求の処理、 Raftログの永続化または複製、 Raftハートビートの処理が含まれます。ただし、リージョンの数が増えると、クラスター全体のパフォーマンスに影響する可能性があります。これを理解するには、次に示すRaftstoreのワークフローを理解する必要があります。

![Raftstore Workflow](/media/best-practices/raft-process.png)

> **注記：**
>
> この図はRaftstoreのワークフローを示すものであり、実際のコード構造を表すものではありません。

上の図から、TiDB サーバーからのリクエストは、gRPC およびstorageモジュールを通過した後、KV (キーと値) の読み取りおよび書き込みメッセージになり、対応するリージョンに送信されることがわかります。これらのメッセージはすぐに処理されるのではなく、一時的に保存されます。Raftstoreは、各リージョンに処理するメッセージがあるかどうかをポーリングして確認します。リージョンに処理するメッセージがある場合、 Raftstore はこのリージョンのRaftステート マシンを駆動してこれらのメッセージを処理し、これらのメッセージの状態変化に応じて後続の操作を実行します。たとえば、書き込みリクエストが着信すると、 Raftステート マシンはログをディスクに保存し、他のリージョンレプリカにログを送信します。ハートビート間隔に達すると、 Raftステート マシンはハートビート情報を他のリージョンレプリカに送信します。

## パフォーマンスの問題 {#performance-problem}

Raftstoreワークフロー図から、各リージョンのメッセージは 1 つずつ処理されます。リージョンの数が多い場合、 Raftstore がこれらのリージョンのハートビートを処理するのに時間がかかり、遅延が発生する可能性があります。その結果、一部の読み取りおよび書き込み要求が時間内に処理されません。読み取りおよび書き込みの負荷が高い場合、 Raftstoreスレッドの CPU 使用率がボトルネックになりやすく、遅延がさらに増加し​​てパフォーマンスに影響する可能性があります。

通常、ロードされたRaftstoreの CPU 使用率が 85% 以上になると、 Raftstore がビジー状態になり、ボトルネックになります。同時に、 `propose wait duration`数百ミリ秒にまで高くなることもあります。

> **注記：**
>
> -   前述のように、 Raftstoreの CPU 使用率については、 Raftstoreはシングルスレッドです。Raftstoreがマルチスレッドの場合は、CPU 使用率のしきい値 (85%) を比例して増やすことができます。
> -   I/O 操作はRaftstoreスレッド内に存在するため、CPU 使用率は 100% に達することはありません。

### パフォーマンス監視 {#performance-monitoring}

Grafana の**TiKV ダッシュボード**では、次の監視メトリックを確認できます。

-   **スレッドCPU**パネルの`Raft store CPU`

    基準値: `raftstore.store-pool-size * 85%`未満。

    ![Check Raftstore CPU](/media/best-practices/raft-store-cpu.png)

-   **Raft Propose**パネルの`Propose wait duration`

    `Propose wait duration`は、リクエストがRaftstoreに送信されてからRaftstore が実際にリクエストの処理を開始するまでの遅延です。遅延が長いということは、 Raftstore がビジー状態であるか、追加ログの処理に時間がかかり、 Raftstore が時間内にリクエストを処理できないことを意味します。

    基準値: クラスターサイズに応じて50～100ms未満

    ![Check Propose wait duration](/media/best-practices/propose-wait-duration.png)

## パフォーマンスチューニング方法 {#performance-tuning-methods}

パフォーマンスの問題の原因を突き止めたら、次の 2 つの側面から解決を試みてください。

-   単一の TiKV インスタンス上のリージョンの数を減らす
-   単一リージョンのメッセージ数を減らす

### 方法1: Raftstoreの同時実行性を高める {#method-1-increase-raftstore-concurrency}

Raftstore はTiDB v3.0 以降、マルチスレッド モジュールにアップグレードされており、 Raftstoreスレッドがボトルネックになる可能性が大幅に減少しています。

デフォルトでは、 Raftstoreでは`raftstore.store-pool-size`から`2`に設定されています。Raftstore でボトルネックが発生する場合は、実際の状況に応じてこの設定項目の値を適切に増やすことができます。ただし、不要なスレッド切り替えのオーバーヘッドが発生しないように、この値を高く設定しすぎないことをお勧めします。

### 方法2: 休止状態リージョンを有効にする {#method-2-enable-hibernate-region}

実際の状況では、読み取りおよび書き込み要求はすべてのリージョンに均等に分散されるわけではなく、いくつかの Region に集中しています。そのため、一時的にアイドル状態の Region のRaftリーダーとフォロワー間のメッセージ数を最小限に抑えることができます。これは Hibernate リージョンの機能です。この機能では、 Raftstore は必要がない場合、アイドル状態の Region のRaftステート マシンにティック メッセージを送信しません。そのため、これらのRaftステート マシンはハートビートメッセージを生成するためにトリガーされず、 Raftstoreのワークロードを大幅に削減できます。

Hibernate リージョン は[TiKVマスター](https://github.com/tikv/tikv/tree/master)ではデフォルトで有効になっています。この機能は必要に応じて設定できます。詳細については[Hibernateリージョンを構成する](/tikv-configuration-file.md)を参照してください。

### 方法3: <code>Region Merge</code>を有効にする {#method-3-enable-code-region-merge-code}

> **注記：**
>
> TiDB v3.0 以降では`Region Merge`がデフォルトで有効になっています。

`Region Merge`を有効にすることで、リージョンの数を減らすこともできます。 `Region Split`とは異なり、 `Region Merge` 、スケジュール設定によって隣接する小さなリージョンを結合するプロセスです。データを削除した後、または`Drop Table`または`Truncate Table`ステートメントを実行した後、小さなリージョンや空のリージョンを結合して、リソースの消費を減らすことができます。

次のパラメータを設定して`Region Merge`有効にします。

    config set max-merge-region-size 20
    config set max-merge-region-keys 200000
    config set merge-schedule-limit 8

詳細については、 [リージョン結合](https://tikv.org/docs/4.0/tasks/configure/region-merge/)および[PD 設定ファイル](/pd-configuration-file.md#schedule)の次の 3 つの構成パラメータを参照してください。

-   [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size)
-   [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys)
-   [`merge-schedule-limit`](/pd-configuration-file.md#merge-schedule-limit)

`Region Merge`パラメータのデフォルト設定はかなり保守的です。 [PD スケジュールのベスト プラクティス](/best-practices/pd-scheduling-best-practices.md#region-merge-is-slow)で提供されている方法を参照することで、 `Region Merge`プロセスを高速化できます。

### 方法4: TiKVインスタンスの数を増やす {#method-4-increase-the-number-of-tikv-instances}

I/O リソースと CPU リソースが十分な場合は、単一のマシンに複数の TiKV インスタンスをデプロイして、単一の TiKV インスタンス上のリージョンの数を減らすか、TiKV クラスター内のマシンの数を増やすことができます。

### 方法5: <code>raft-base-tick-interval</code>を調整する {#method-5-adjust-code-raft-base-tick-interval-code}

リージョンの数を減らすことに加えて、単位時間あたりのリージョンごとのメッセージ数を減らすことで、 Raftstoreへの負荷を軽減することもできます。たとえば、 `raft-base-tick-interval`構成項目の値を適切に増やすことができます。

    [raftstore]
    raft-base-tick-interval = "2s"

上記の構成では、 `raft-base-tick-interval` Raftstoreが各リージョンのRaftステートマシンを駆動する時間間隔です。つまり、この時間間隔で、 Raftstore はRaftステートマシンに tick メッセージを送信します。この間隔を増やすと、 Raftstoreからのメッセージの数を効果的に減らすことができます。

ティック メッセージ間のこの間隔によって、 `election timeout`と`heartbeat`の間の間隔も決まることに注意してください。次の例を参照してください。

    raft-election-timeout = raft-base-tick-interval * raft-election-timeout-ticks
    raft-heartbeat-interval = raft-base-tick-interval * raft-heartbeat-ticks

リージョンフォロワーが`raft-election-timeout`間隔以内にリーダーからハートビートを受信しなかった場合、これらのフォロワーはリーダーが失敗したと判断し、新しい選出を開始します。3 `raft-heartbeat-interval` 、リーダーがフォロワーにハートビートを送信する間隔です。したがって、 `raft-base-tick-interval`の値を増やすと、 Raftステート マシンから送信されるネットワーク メッセージの数を減らすことができますが、 Raftステート マシンがリーダーの障害を検出する時間が長くなります。

### 方法6:リージョンのサイズを調整する {#method-6-adjust-region-size}

リージョンのデフォルト サイズは 96 MiB ですが、リージョンをより大きなサイズに設定することでリージョンの数を減らすことができます。詳細については、 [リージョンパフォーマンスの調整](/tune-region-performance.md)参照してください。

> **警告：**
>
> 現在、カスタマイズされたリージョンサイズは、TiDB v6.1.0 で導入された実験的機能です。本番環境での使用は推奨されません。リスクは次のとおりです。
>
> -   パフォーマンスのジッタが発生する可能性があります。
> -   特に広範囲のデータを扱うクエリの場合、クエリのパフォーマンスが低下する可能性があります。
> -   リージョンのスケジュールが遅くなります。

## その他の問題と解決策 {#other-problems-and-solutions}

このセクションでは、その他の問題と解決策について説明します。

### PDLeaderの切り替えが遅い {#switching-pd-leader-is-slow}

PD は、PDLeaderノードを切り替えた後に PD がすぐにリージョンルーティング サービスを再開できるように、etcd にリージョンメタ情報を保持する必要があります。リージョンの数が増えると、etcd のパフォーマンス問題が発生し、PD がLeaderを切り替えるときに PD が etcd からリージョンメタ情報を取得するのが遅くなります。数百万のリージョンがある場合、etcd からメタ情報を取得するのに 10 秒以上、場合によっては数十秒かかることがあります。

この問題に対処するため、TiDB v3.0 以降、PD ではデフォルトで`use-region-storage`有効になっています。この機能を有効にすると、PD はリージョンメタ情報をローカル LevelDB に保存し、他のメカニズムを通じて PD ノード間で情報を同期します。

### PDルーティング情報が時間内に更新されない {#pd-routing-information-is-not-updated-in-time}

TiKV では、pd-worker が定期的にリージョンメタ情報を PD に報告します。TiKV が再起動されるかリージョンリーダーが切り替わると、PD は統計情報を通じてリージョン`approximate size / keys`を再計算する必要があります。そのため、リージョンの数が多いと、シングル スレッドの pd-worker がボトルネックになり、タスクが積み重なって時間内に処理されなくなる可能性があります。この状況では、PD は特定のリージョンメタ情報を時間内に取得できないため、ルーティング情報が時間内に更新されません。この問題は実際の読み取りと書き込みには影響しませんが、PD のスケジュールが不正確になり、TiDB がリージョンキャッシュを更新するときに複数のラウンド トリップが必要になる可能性があります。

**TiKV Grafana**パネルの**[タスク]**の下にある**[Worker の保留中のタスク]**をチェックして、pd-worker にタスクが積み重なっているかどうかを確認できます。通常、 `pending tasks`比較的低い値に維持する必要があります。

![Check pd-worker](/media/best-practices/pd-worker-metrics.png)

pd-worker は[バージョン3.0.5](/releases/release-3.0.5.md#tikv)以降、パフォーマンスが向上するように最適化されています。同様の問題が発生した場合は、最新バージョンにアップグレードすることをお勧めします。

### Prometheusはメトリクスのクエリが遅い {#prometheus-is-slow-to-query-metrics}

大規模クラスターでは、TiKV インスタンスの数が増えるにつれて、Prometheus がメトリックをクエリする圧力が大きくなり、Grafana がこれらのメトリックを表示する速度が遅くなります。この問題を軽減するために、v3.0 以降ではメトリックの事前計算が構成されています。
