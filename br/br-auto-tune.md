---
title: Backup Auto-Tune
summary: Learn about the auto-tune feature of TiDB backup and restore, which automatically limits the resources used by backups to reduce the impact on the cluster in case of high cluster resource usage.
---

# バックアップ自動調整<span class="version-mark">v5.4.0 の新機能</span> {#backup-auto-tune-span-class-version-mark-new-in-v5-4-0-span}

TiDB v5.4.0 より前では、バックアップと復元 (BR) を使用してデータをバックアップする場合、バックアップに使用されるスレッドの数は論理 CPU コアの 75% を占めていました。速度制限がないと、バックアップ プロセスで大量のクラスター リソースが消費される可能性があり、オンライン クラスターのパフォーマンスに大きな影響を与えます。スレッド プールのサイズを調整することでバックアップの影響を軽減できますが、CPU 負荷を観察してスレッド プール サイズを手動で調整するのは面倒な作業です。

クラスターに対するバックアップ タスクの影響を軽減するために、TiDB v5.4.0 では自動調整機能が導入されており、これはデフォルトで有効になっています。クラスターのリソース使用率が高い場合、 BR はバックアップ タスクで使用されるリソースを自動的に制限し、クラスターへの影響を軽減します。自動調整機能はデフォルトで有効になっています。

## 利用シーン {#usage-scenario}

クラスターに対するバックアップ タスクの影響を軽減したい場合は、自動調整機能を有効にすることができます。この機能を有効にすると、TiDB はクラスターに過度の影響を与えることなく、可能な限り高速にバックアップ タスクを実行します。

あるいは、TiKV 構成項目[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)またはパラメーター`--ratelimit`を使用して、バックアップ速度を制限することもできます。

## 自動調整を使用する {#use-auto-tune}

自動調整機能は、追加の構成を行わなくても、デフォルトで有効になっています。

> **注記：**
>
> v5.3.x から v5.4.0 以降のバージョンにアップグレードするクラスターの場合、自動調整機能はデフォルトで無効になっています。手動で有効にする必要があります。

自動調整機能を手動で有効にするには、TiKV 構成項目[`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540) ～ `true`を設定する必要があります。

TiKV は、自動調整機能の動的構成をサポートしています。クラスターを再起動せずに、この機能を有効または無効にすることができます。自動調整機能を動的に有効または無効にするには、次のコマンドを実行します。

```shell
tikv-ctl modify-tikv-config -n backup.enable-auto-tune -v <true|false>
```

オフライン クラスターでバックアップ タスクを実行する場合、バックアップを高速化するために、 `tikv-ctl`を使用して`backup.num-threads`の値をより大きな数値に変更できます。

## 制限事項 {#limitations}

自動調整は、バックアップ速度を制限するための粗粒度のソリューションです。これにより、手動調整の必要性が軽減されます。ただし、きめ細かい制御ができないため、自動調整ではクラスターに対するバックアップの影響を完全に除去できない可能性があります。

自動調整機能には次の問題とそれに対応する解決策があります。

-   問題 1:**書き込み負荷の高いクラスター**の場合、自動チューニングによってワークロードとバックアップ タスクが「正のフィードバック ループ」に陥る可能性があります。バックアップ タスクが多くのリソースを消費するため、クラスターで使用されるリソースが少なくなります。この時点で、自動調整はクラスターに大きなワークロードがかかっていないと誤って判断する可能性があり、そのためバックアップがより高速に実行される可能性があります。このような場合、オートチューニングは効果がありません。

    -   解決策: バックアップ タスクで使用されるスレッドの数を制限するには、 `backup.num-threads`をより小さい数値に手動で調整します。動作原理は次のとおりです。

        バックアップ プロセスには多くの SST デコード、エンコード、圧縮、解凍が含まれており、CPU リソースを消費します。さらに、以前のテスト ケースでは、バックアップ プロセス中に、バックアップに使用されるスレッド プールの CPU 使用率が 100% に近いことが示されています。これは、バックアップ タスクが大量の CPU リソースを消費することを意味します。バックアップ タスクで使用されるスレッドの数を調整することで、TiKV はバックアップ タスクで使用される CPU コアを制限し、クラスターのパフォーマンスに対するバックアップ タスクの影響を軽減できます。

-   問題 2:**ホットスポットのあるクラスター**の場合、ホットスポットのある TiKV ノード上のバックアップ タスクが過度に制限される可能性があり、これによりバックアップ プロセス全体が遅くなります。

    -   解決策: ホットスポット ノードを削除するか、ホットスポット ノードの自動調整を無効にします (クラスターのパフォーマンスが低下する可能性があります)。

-   問題 3:**トラフィック ジッターが高い**シナリオの場合、自動調整は一定の間隔 (デフォルトでは 1 分) で速度制限を調整するため、トラフィック ジッターが大きい場合は処理できない可能性があります。詳細は[`auto-tune-refresh-interval`](#implementation)を参照してください。

    -   解決策: 自動調整を無効にします。

## 実装 {#implementation}

自動調整は、クラスターの全体的な CPU 使用率が特定のしきい値を超えないように、バックアップ タスクで使用されるスレッド プールのサイズを調整します。

この機能には、TiKV 構成ファイルにリストされていない 2 つの関連構成項目があります。これら 2 つの設定項目は内部チューニング専用です。バックアップ タスクを実行する場合、これら 2 つの構成項目を構成する必要はありませ**ん**。

-   `backup.auto-tune-remain-threads` :

    -   自動調整は、バックアップ タスクで使用されるリソースを制御し、同じノード上の他のタスクで少なくとも`backup.auto-tune-remain-threads`コアが使用できるようにします。
    -   デフォルト値: `round(0.2 * vCPU)`

-   `backup.auto-tune-refresh-interval` :

    -   自動調整は`backup.auto-tune-refresh-interval`分ごとに統計を更新し、バックアップ タスクが使用できる CPU コアの最大数を再計算します。
    -   デフォルト値: `1m`

以下は、自動調整がどのように機能するかの例です。 `*`バックアップタスクで使用される CPU コアを示します。 `^`他のタスクが使用するＣＰＵコアである。 `-`アイドル状態のＣＰＵコアを示す。

    |--------| The server has 8 logical CPU cores.
    |****----| By default, `backup.num-threads` is `4`. Note that auto-tune makes sure that the thread pool size is never larger than `backup.num-threads`.
    |^^****--| By default, `auto-tune-remain-threads` = round(8 * 0.2) = 2. Auto-tune adjusts the size of the thread pool to `4`.
    |^^^^**--| Because the cluster workload gets higher, auto-tune adjusts the size of the thread pool to `2`. After that, the cluster still has 2 idle CPU cores.

**[バックアップ CPU 使用率]**パネルで、自動調整によって調整されたスレッド プールのサイズを確認できます。

![Grafana dashboard example of backup auto-tune metrics](/media/br/br-auto-throttle.png)

上の画像では、黄色の半透明の領域はバックアップ タスクに使用できるスレッドを表しています。バックアップ タスクの CPU 使用率が黄色の領域を超えていないことがわかります。
