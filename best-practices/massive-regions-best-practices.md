---
title: Best Practices for TiKV Performance Tuning with Massive Regions
summary: Learn how to tune the performance of TiKV with a massive amount of Regions.
---

# 大規模な領域での TiKV性能チューニングのベスト プラクティス {#best-practices-for-tikv-performance-tuning-with-massive-regions}

TiDB では、データはリージョンに分割され、それぞれのリージョンに特定のキー範囲のデータが保存されます。これらのリージョンは、複数の TiKV インスタンスに分散されます。データがクラスターに書き込まれると、数百万のリージョンが作成される可能性があります。単一の TiKV インスタンス上のリージョンが多すぎると、クラスターに大きな負担がかかり、パフォーマンスに影響を与える可能性があります。

このドキュメントでは、 Raftstore (TiKV のコア モジュール) のワークフローを紹介し、大量のリージョンがパフォーマンスに影響を与える理由を説明し、TiKV のパフォーマンスを調整する方法を提供します。

## Raftstoreのワークフロー {#raftstore-workflow}

TiKV インスタンスには複数のリージョンがあります。 Raftstoreモジュールは、 Raftステート マシンを駆動してリージョンメッセージを処理します。これらのメッセージには、リージョンでの読み取りまたは書き込みリクエストの処理、 Raftログの永続化または複製、 Raftハートビートの処理が含まれます。ただし、リージョンの数が増加すると、クラスター全体のパフォーマンスに影響を与える可能性があります。これを理解するには、次のようなRaftstoreのワークフローを学習する必要があります。

![Raftstore Workflow](/media/best-practices/raft-process.png)

> **注記：**
>
> この図はRaftstoreのワークフローを示すだけであり、実際のコード構造を表すものではありません。

上の図から、TiDB サーバーからのリクエストは、gRPC とstorageモジュールを通過した後、KV (キーと値) の読み取りおよび書き込みメッセージとなり、対応するリージョンに送信されることがわかります。これらのメッセージはすぐには処理されず、一時的に保存されます。 Raftstore はポーリングして、各リージョンに処理するメッセージがあるかどうかを確認します。リージョンに処理すべきメッセージがある場合、 Raftstore はこのリージョンのRaftステート マシンを駆動してこれらのメッセージを処理し、これらのメッセージの状態変化に従って後続の操作を実行します。たとえば、書き込みリクエストが受信されると、 Raftステート マシンはログをディスクに保存し、他のリージョンレプリカにログを送信します。ハートビート間隔に達すると、 Raftステート マシンはハートビート情報を他のリージョンレプリカに送信します。

## パフォーマンスの問題 {#performance-problem}

Raftstoreワークフロー図から、各リージョンのメッセージは 1 つずつ処理されます。多数のリージョンが存在する場合、 Raftstore がこれらのリージョンのハートビートを処理するのに時間がかかり、遅延が発生する可能性があります。その結果、一部の読み取りおよび書き込みリクエストは時間内に処理されません。読み取りおよび書き込みの負荷が高い場合、 Raftstoreスレッドの CPU 使用率がボトルネックになりやすく、遅延がさらに増大し、パフォーマンスに影響を与える可能性があります。

一般に、ロードされたRaftstoreの CPU 使用率が 85% 以上に達すると、 Raftstore はビジー状態になり、ボトルネックになります。同時に、 `propose wait duration`数百ミリ秒にもなる可能性があります。

> **注記：**
>
> -   Raftstoreの CPU 使用率については、前述の通り、 Raftstore はシングルスレッドです。 Raftstoreがマルチスレッドの場合は、それに比例して CPU 使用率のしきい値 (85%) を増やすことができます。
> -   Raftstoreスレッドには I/O 操作が存在するため、CPU 使用率が 100% に達することはできません。

### パフォーマンス監視 {#performance-monitoring}

Grafana の**TiKV ダッシュボード**で次の監視メトリクスを確認できます。

-   **スレッド CPU**パネルの`Raft store CPU`

    参考値： `raftstore.store-pool-size * 85%`未満。

    ![Check Raftstore CPU](/media/best-practices/raft-store-cpu.png)

-   **Raftの提案**パネルの`Propose wait duration`

    `Propose wait duration`は、リクエストがRaftstoreに送信される時間と、 Raftstore が実際にリクエストの処理を開始する時間との間の遅延です。長い遅延は、 Raftstore がビジーであるか、追加ログの処理に時間がかかり、 Raftstore が時間内にリクエストを処理できないことを意味します。

    参考値：クラスタサイズに応じて50~100ms未満

    ![Check Propose wait duration](/media/best-practices/propose-wait-duration.png)

## パフォーマンスのチューニング方法 {#performance-tuning-methods}

パフォーマンスの問題の原因を特定したら、次の 2 つの側面から問題の解決を試みます。

-   単一の TiKV インスタンス上のリージョンの数を減らす
-   単一リージョンのメッセージ数を減らす

### 方法 1: Raftstore の同時実行数を増やす {#method-1-increase-raftstore-concurrency}

Raftstore はTiDB v3.0 以降マルチスレッド モジュールにアップグレードされ、 Raftstoreスレッドがボトルネックになる可能性が大幅に減少しました。

デフォルトでは、TiKV では`raftstore.store-pool-size` `2`に設定されています。 Raftstoreでボトルネックが発生した場合は、状況に応じてこの設定項目の値を適切に増やすことができます。ただし、不必要なスレッド切り替えオーバーヘッドの発生を避けるために、この値をあまり高く設定しないことをお勧めします。

### 方法 2: Hibernateリージョンを有効にする {#method-2-enable-hibernate-region}

実際の状況では、読み取りおよび書き込みリクエストはすべてのリージョンに均等に分散されません。代わりに、それらはいくつかの地域に集中しています。その後、 Raftリーダーと、一時的にアイドル状態になっているリージョンのフォロワー間のメッセージの数を最小限に抑えることができます。これが Hibernateリージョンの機能です。この機能では、 Raftstore は、必要がない場合、アイドル状態のリージョンのRaftステート マシンにティック メッセージを送信しません。そうすれば、これらのRaftステート マシンはハートビートメッセージを生成するためにトリガーされなくなり、 Raftstoreのワークロードを大幅に軽減できます。

Hibernateリージョンは[TiKVマスター](https://github.com/tikv/tikv/tree/master)ではデフォルトで有効になっています。この機能はニーズに応じて設定できます。詳細は[休止状態リージョンの構成](/tikv-configuration-file.md)を参照してください。

### 方法 3: <code>Region Merge</code>を有効にする {#method-3-enable-code-region-merge-code}

> **注記：**
>
> TiDB v3.0 以降、 `Region Merge`がデフォルトで有効になっています。

`Region Merge`を有効にしてリージョンの数を減らすこともできます。 `Region Split`とは逆に、 `Region Merge`スケジューリングによって隣接する小さなリージョンをマージするプロセスです。データを削除するか、 `Drop Table`または`Truncate Table`ステートメントを実行した後、小さなリージョンや空のリージョンをマージして、リソースの消費を削減できます。

次のパラメータを構成して`Region Merge`を有効にします。

    config set max-merge-region-size 20
    config set max-merge-region-keys 200000
    config set merge-schedule-limit 8

詳細については、 [リージョンのマージ](https://tikv.org/docs/4.0/tasks/configure/region-merge/)と、 [PD設定ファイル](/pd-configuration-file.md#schedule)の次の 3 つの構成パラメータを参照してください。

-   [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size)
-   [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys)
-   [`merge-schedule-limit`](/pd-configuration-file.md#merge-schedule-limit)

`Region Merge`パラメータのデフォルト設定はかなり保守的です。 [PD スケジュールのベスト プラクティス](/best-practices/pd-scheduling-best-practices.md#region-merge-is-slow)の方法を参考に`Region Merge`処理を高速化することができます。

### 方法 4: TiKV インスタンスの数を増やす {#method-4-increase-the-number-of-tikv-instances}

I/O リソースと CPU リソースが十分な場合は、単一のマシンに複数の TiKV インスタンスをデプロイして、単一の TiKV インスタンス上のリージョンの数を減らすことができます。または、TiKV クラスター内のマシンの数を増やすこともできます。

### 方法 5: <code>raft-base-tick-interval</code>を調整する {#method-5-adjust-code-raft-base-tick-interval-code}

リージョンの数を減らすことに加えて、単位時間内の各リージョンのメッセージ数を減らすことで、 Raftstoreへの負荷を軽減することもできます。たとえば、 `raft-base-tick-interval`構成項目の値を適切に増やすことができます。

    [raftstore]
    raft-base-tick-interval = "2s"

上記の構成では、 `raft-base-tick-interval`はRaftstore が各リージョンのRaftステート マシンを駆動する時間間隔です。これは、この時間間隔でRaftstore がRaftステート マシンにティック メッセージを送信することを意味します。この間隔を長くすると、 Raftstoreからのメッセージの数を効果的に減らすことができます。

このティック メッセージ間の間隔によって、 `election timeout`と`heartbeat`の間の間隔も決定されることに注意してください。次の例を参照してください。

    raft-election-timeout = raft-base-tick-interval * raft-election-timeout-ticks
    raft-heartbeat-interval = raft-base-tick-interval * raft-heartbeat-ticks

リージョンフォロワーが`raft-election-timeout`間隔以内にリーダーからハートビートを受信しなかった場合、これらのフォロワーはリーダーが失敗したと判断し、新しい選挙を開始します。 `raft-heartbeat-interval`は、リーダーがフォロワーにハートビートを送信する間隔です。したがって、値`raft-base-tick-interval`を増やすと、 Raftステート マシンから送信されるネットワーク メッセージの数を減らすことができますが、 Raftステート マシンがリーダーの障害を検出するまでの時間も長くなります。

### 方法 6:リージョンサイズを調整する {#method-6-adjust-region-size}

リージョンのデフォルトのサイズは 96 MiB ですが、リージョンをより大きなサイズに設定することでリージョンの数を減らすことができます。詳細については、 [リージョンのパフォーマンスを調整する](/tune-region-performance.md)を参照してください。

> **警告：**
>
> 現在、カスタマイズされたリージョンサイズは、TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めできません。リスクは次のとおりです。
>
> -   パフォーマンスのジッターが発生する可能性があります。
> -   クエリのパフォーマンス、特に広範囲のデータを処理するクエリのパフォーマンスが低下する可能性があります。
> -   リージョンのスケジュールが遅くなります。

## その他の問題と解決策 {#other-problems-and-solutions}

このセクションでは、その他の問題と解決策について説明します。

### PDLeaderの切り替えが遅い {#switching-pd-leader-is-slow}

PD は、PDLeaderノードの切り替え後にすぐにリージョンルーティング サービスの提供を再開できるように、etcd にリージョンメタ情報を永続化する必要があります。リージョンの数が増加すると、etcd のパフォーマンスの問題が発生し、PD がLeaderを切り替えるときに、PD が etcd からリージョンメタ情報を取得するのが遅くなります。リージョンが数百万ある場合、etcd からメタ情報を取得するのに 10 秒以上、場合によっては数十秒かかる場合があります。

この問題に対処するために、TiDB v3.0 以降、PD ではデフォルトで`use-region-storage`が有効になっています。この機能を有効にすると、PD はローカル LevelDB にリージョンメタ情報を保存し、他のメカニズムを通じて PD ノード間で情報を同期します。

### PD ルーティング情報の更新が間に合わない {#pd-routing-information-is-not-updated-in-time}

TiKV では、pd-worker がリージョンメタ情報を定期的に PD に報告します。 TiKV が再起動されるか、リージョンリーダーが切り替わる場合、PD はリージョン`approximate size / keys`からリージョンの統計を再計算する必要があります。したがって、リージョンの数が多いと、シングルスレッドの pd ワーカーがボトルネックとなり、タスクが山積みになり、処理が間に合わなくなる可能性があります。この状況では、PD は特定のリージョンメタ情報を時間内に取得できないため、ルーティング情報の更新が間に合わなくなります。この問題は実際の読み取りおよび書き込みには影響しませんが、PD スケジューリングが不正確になり、TiDB がリージョンキャッシュを更新するときに数回のラウンド トリップが必要になる可能性があります。

**TiKV Grafana**パネルの**タスク**の下にある**ワーカー保留タスクを**チェックして、pd-worker にタスクが積み重なっているかどうかを判断できます。一般に、 `pending tasks`比較的低い値に保つ必要があります。

![Check pd-worker](/media/best-practices/pd-worker-metrics.png)

pd-worker は、 [v3.0.5](/releases/release-3.0.5.md#tikv)以降、パフォーマンスが向上するように最適化されています。同様の問題が発生した場合は、最新バージョンにアップグレードすることをお勧めします。

### Prometheus はメトリクスのクエリが遅い {#prometheus-is-slow-to-query-metrics}

大規模なクラスターでは、TiKV インスタンスの数が増えると、Prometheus によるメトリクスのクエリに対するプレッシャーが大きくなり、Grafana によるこれらのメトリクスの表示が遅くなります。この問題を軽減するために、v3.0 以降、メトリクスの事前計算が構成されています。
