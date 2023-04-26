---
title: Backup Auto-Tune
summary: Learn about the auto-tune feature of TiDB backup and restore, which automatically limits the resources used by backups to reduce the impact on the cluster in case of high cluster resource usage.
---

# バックアップの自動調整<span class="version-mark">v5.4.0 の新機能</span> {#backup-auto-tune-span-class-version-mark-new-in-v5-4-0-span}

TiDB v5.4.0 より前では、Backup &amp; Restore (BR) を使用してデータをバックアップすると、バックアップに使用されるスレッドの数が論理 CPU コアの 75% を占めていました。速度制限がない場合、バックアップ プロセスは大量のクラスター リソースを消費する可能性があり、オンライン クラスターのパフォーマンスに大きな影響を与えます。スレッド プールのサイズを調整することでバックアップの影響を軽減できますが、CPU 負荷を観察して手動でスレッド プール サイズを調整するのは面倒な作業です。

クラスターに対するバックアップ タスクの影響を軽減するために、TiDB v5.4.0 では自動調整機能が導入されており、これはデフォルトで有効になっています。クラスター リソースの使用率が高い場合、 BR はバックアップ タスクで使用されるリソースを自動的に制限し、クラスターへの影響を軽減します。自動調整機能はデフォルトで有効になっています。

## 利用シーン {#usage-scenario}

クラスターに対するバックアップ タスクの影響を軽減する場合は、自動調整機能を有効にすることができます。この機能を有効にすると、TiDB はクラスターに過度の影響を与えることなく、可能な限り高速にバックアップ タスクを実行します。

または、TiKV 構成項目[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)またはパラメーター`--ratelimit`を使用して、バックアップ速度を制限することもできます。

## 自動調整を使用する {#use-auto-tune}

自動調整機能は、追加の構成なしでデフォルトで有効になっています。

> **ノート：**
>
> v5.3.x から v5.4.0 以降のバージョンにアップグレードするクラスターの場合、自動調整機能はデフォルトで無効になっています。手動で有効にする必要があります。

自動調整機能を手動で有効にするには、TiKV 構成項目[`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)から`true`を設定する必要があります。

TiKV は、自動調整機能の動的構成をサポートしています。クラスターを再起動せずに、この機能を有効または無効にすることができます。自動調整機能を動的に有効または無効にするには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
tikv-ctl modify-tikv-config -n backup.enable-auto-tune -v <true|false>
```

オフライン クラスターでバックアップ タスクを実行する場合、バックアップを高速化するために、 `tikv-ctl`を使用して`backup.num-threads`の値をより大きな数値に変更できます。

## 制限事項 {#limitations}

自動調整は、バックアップ速度を制限するための大まかなソリューションです。これにより、手動調整の必要性が軽減されます。ただし、きめ細かい制御ができないため、自動調整ではクラスターに対するバックアップの影響を完全に除去できない場合があります。

自動調整機能には、次の問題と対応する解決策があります。

-   問題 1:**書き込み負荷の高いクラスター**の場合、自動調整によりワークロードとバックアップ タスクが「正のフィードバック ループ」に陥る可能性があります。この時点で、オートチューンは、クラスターのワークロードが高くないことを誤って想定し、バックアップをより高速に実行できるようにする可能性があります。このような場合、オートチューンは効果がありません。

    -   解決策: バックアップ タスクで使用されるスレッドの数を制限するために、 `backup.num-threads`を手動でより小さな数に調整します。動作原理は次のとおりです。

        バックアップ プロセスには、CPU リソースを消費する多数の SST デコード、エンコード、圧縮、および圧縮解除が含まれます。さらに、以前のテスト ケースでは、バックアップ プロセス中に、バックアップに使用されるスレッド プールの CPU 使用率が 100% に近いことが示されています。これは、バックアップ タスクが多くの CPU リソースを消費することを意味します。バックアップ タスクで使用されるスレッドの数を調整することで、TiKV はバックアップ タスクで使用される CPU コアを制限できるため、バックアップ タスクがクラスターのパフォーマンスに与える影響を軽減できます。

-   問題 2:**ホットスポットのあるクラスター**の場合、ホットスポットのある TiKV ノードでのバックアップ タスクが過度に制限され、バックアップ プロセス全体が遅くなる可能性があります。

    -   解決策: ホットスポット ノードを削除するか、ホットスポット ノードの自動調整を無効にします (これにより、クラスターのパフォーマンスが低下する可能性があります)。

-   問題 3:**トラフィックのジッタが高い**シナリオの場合、自動調整は一定の間隔 (既定では 1 分) で速度制限を調整するため、トラフィックのジッタが大きい場合は処理できない可能性があります。詳細については、 [`auto-tune-refresh-interval`](#implementation)を参照してください。

    -   解決策: 自動調整を無効にします。

## 実装 {#implementation}

自動調整は、バックアップ タスクで使用されるスレッド プールのサイズを調整して、クラスターの全体的な CPU 使用率が特定のしきい値を超えないようにします。

この機能には、TiKV 構成ファイルにリストされていない 2 つの関連する構成項目があります。これら 2 つの構成アイテムは、内部チューニング専用です。バックアップ タスクを実行する場合、これら 2 つの構成項目を構成する必要はありませ**ん**。

-   `backup.auto-tune-remain-threads` :

    -   自動調整は、バックアップ タスクによって使用されるリソースを制御し、少なくとも`backup.auto-tune-remain-threads`コアが同じノード上の他のタスクに使用できるようにします。
    -   デフォルト値: `round(0.2 * vCPU)`

-   `backup.auto-tune-refresh-interval` :

    -   自動調整は`backup.auto-tune-refresh-interval`分ごとに統計を更新し、バックアップ タスクが使用できる CPU コアの最大数を再計算します。
    -   デフォルト値: `1m`

以下は、自動調整がどのように機能するかの例です。 `*`バックアップ タスクによって使用される CPU コアを示します。 `^`他のタスクが使用するＣＰＵコアである。 `-`アイドル状態の CPU コアを示します。

```
|--------| The server has 8 logical CPU cores.
|****----| By default, `backup.num-threads` is `4`. Note that auto-tune makes sure that the thread pool size is never larger than `backup.num-threads`.
|^^****--| By default, `auto-tune-remain-threads` = round(8 * 0.2) = 2. Auto-tune adjusts the size of the thread pool to `4`.
|^^^^**--| Because the cluster workload gets higher, auto-tune adjusts the size of the thread pool to `2`. After that, the cluster still has 2 idle CPU cores.
```

**[バックアップ CPU 使用率]**パネルで、自動調整によって調整されたスレッド プールのサイズを確認できます。

![Grafana dashboard example of backup auto-tune metrics](/media/br/br-auto-throttle.png)

上の画像では、黄色の半透明の領域は、バックアップ タスクに使用できるスレッドを表しています。バックアップ タスクの CPU 使用率が黄色の領域を超えていないことがわかります。
