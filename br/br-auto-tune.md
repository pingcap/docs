---
title: BR Auto-Tune
summary: Learn about the auto-feature of BR, which automatically limits the resources used by backups to reduce the impact on the cluster in case of high cluster resource usage.
---

# BRAuto- <span class="version-mark">Tunev5.4.0の新機能</span> {#br-auto-tune-span-class-version-mark-new-in-v5-4-0-span}

TiDB v5.4.0より前では、BRを使用してデータをバックアップする場合、バックアップに使用されるスレッドの数は論理CPUコアの75％を占めます。速度制限がないと、バックアッププロセスで大量のクラスタリソースが消費される可能性があり、オンラインクラスタのパフォーマンスに大きな影響を及ぼします。スレッドプールのサイズを調整することでバックアップの影響を減らすことができますが、CPUの負荷を監視し、スレッドプールのサイズを手動で調整するのは面倒な作業です。

TiDB v5.4.0以降、クラスタへのバックアップタスクの影響を減らすために、BRでは自動調整機能が導入されています。クラスタリソースの使用率が高い場合、BRはバックアップタスクで使用されるリソースを自動的に制限し、それによってクラスタへの影響を減らします。自動調整機能はデフォルトで有効になっています。

## ユーザーシナリオ {#user-scenario}

クラスタへのバックアップタスクの影響を減らしたい場合は、自動調整機能を有効にすることができます。この機能を有効にすると、BRは、クラスタに過度の影響を与えることなく、バックアップタスクを可能な限り高速に実行します。

または、TiKV構成項目[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)またはパラメーター`--ratelimit`を使用して、バックアップ速度を制限することもできます。

## オートチューンを使用する {#use-auto-tune}

自動調整機能は、追加の構成なしでデフォルトで有効になっています。

> **ノート：**
>
> v5.3.xからv5.4.0以降のバージョンにアップグレードするクラスターの場合、自動調整機能はデフォルトで無効になっています。手動で有効にする必要があります。

自動調整機能を手動で有効にするには、TiKV構成項目[`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)を`true`に設定する必要があります。

TiKVは、自動調整機能の動的構成をサポートしています。クラスタを再起動せずに、この機能を有効または無効にできます。自動調整機能を動的に有効または無効にするには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
tikv-ctl modify-tikv-config -n backup.enable-auto-tune -v <true|false>
```

オフラインクラスタでバックアップタスクを実行する場合、バックアップを高速化するために、 `tikv-ctl`を使用して`backup.num-threads`の値をより大きな数に変更できます。

## 制限事項 {#limitations}

自動調整は、バックアップ速度を制限するための大まかなソリューションです。手動チューニングの必要性を減らします。ただし、きめ細かい制御ができないため、自動調整ではクラスタへのバックアップの影響を完全に取り除くことができない場合があります。

自動調整機能には、次の問題と対応する解決策があります。

-   問題1：**書き込みが多いクラスター**の場合、自動調整によってワークロードとバックアップタスクが「正のフィードバックループ」に陥る可能性があります。バックアップタスクが使用するリソースが多すぎるため、クラスタが使用するリソースが少なくなります。この時点で、オートチューンは、クラスタに大きなワークロードがかかっていないことを誤って想定し、BRの実行速度を上げる可能性があります。このような場合、自動調整は効果がありません。

    -   解決策：バックアップタスクで使用されるスレッドの数を制限するには、手動で`backup.num-threads`を小さい数に調整します。動作原理は次のとおりです。

        バックアッププロセスには、CPUリソースを消費する、多くのSSTデコード、エンコード、圧縮、および解凍が含まれます。さらに、以前のテストケースでは、バックアッププロセス中、バックアップに使用されるスレッドプールのCPU使用率が100％に近いことが示されています。これは、バックアップタスクが多くのCPUリソースを消費することを意味します。バックアップタスクで使用されるスレッドの数を調整することにより、TiKVはバックアップタスクで使用されるCPUコアを制限し、クラスタのパフォーマンスに対するバックアップタスクの影響を減らすことができます。

-   問題2：ホットスポットのある**クラスターの場合、ホットスポット**のあるTiKVノードでのバックアップタスクが過度に制限され、バックアッププロセス全体の速度が低下する可能性があります。

    -   解決策：ホットスポットノードを削除するか、ホットスポットノードの自動調整を無効にします（これにより、クラスタのパフォーマンスが低下する可能性があります）。

-   問題3：**トラフィックジッターが高い**シナリオでは、自動調整によって一定の間隔（デフォルトでは1分）で制限速度が調整されるため、トラフィックジッターが高い場合は処理できない可能性があります。詳細については、 [`auto-tune-refresh-interval`](#implementation)を参照してください。

    -   解決策：自動調整を無効にします。

## 実装 {#implementation}

Auto-tuneは、BRを使用したバックアップタスクで使用されるスレッドプールのサイズを調整して、クラスタの全体的なCPU使用率が特定のしきい値を超えないようにします。

この機能には、TiKV構成ファイルにリストされていない2つの関連する構成項目があります。これらの2つの構成項目は、内部調整専用です。バックアップタスクを実行するときに、これら2つの構成項目を構成する必要はありませ**ん**。

-   `backup.auto-tune-remain-threads` ：

    -   Auto-tuneは、バックアップタスクで使用されるリソースを制御し、同じノード上の他のタスクで少なくとも`backup.auto-tune-remain-threads`のコアが使用できるようにします。
    -   デフォルト値： `round(0.2 * vCPU)`

-   `backup.auto-tune-refresh-interval` ：

    -   `backup.auto-tune-refresh-interval`分ごとに、自動調整によって統計が更新され、バックアップタスクが使用できるCPUコアの最大数が再計算されます。
    -   デフォルト値： `1m`

以下は、自動調整がどのように機能するかの例です。 `*`は、バックアップタスクで使用されるCPUコアを示します。 `^`は、他のタスクで使用されるCPUコアを示します。 `-`はアイドル状態のCPUコアを示します。

```
|--------| The server has 8 logical CPU cores.
|****----| By default, `backup.num-threads` is `4`. Note that auto-tune makes sure that the thread pool size is never larger than `backup.num-threads`.
|^^****--| By default, `auto-tune-remain-threads` = round(8 * 0.2) = 2. Auto-tune adjusts the size of the thread pool to `4`.
|^^^^**--| Because the cluster workload gets higher, auto-tune adjusts the size of the thread pool to `2`. After that, the cluster still has 2 idle CPU cores.
```

[**バックアップCPU使用率**]パネルで、自動調整によって調整されたスレッドプールのサイズを確認できます。

![Grafana dashboard example of backup auto-tune metrics](/media/br/br-auto-throttle.png)

上の画像では、黄色の半透明の領域がバックアップタスクに使用できるスレッドを表しています。バックアップタスクのCPU使用率が黄色の領域を超えていないことがわかります。
