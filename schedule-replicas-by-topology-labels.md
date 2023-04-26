---
title: Schedule Replicas by Topology Labels
summary: Learn how to schedule replicas by topology labels.
---

# トポロジ ラベルごとにレプリカをスケジュールする {#schedule-replicas-by-topology-labels}

> **ノート：**
>
> TiDB v5.3.0 では[SQL の配置規則](/placement-rules-in-sql.md)が導入されています。これにより、テーブルとパーティションの配置を構成するためのより便利な方法が提供されます。 SQL の配置ルールは、将来のリリースで配置構成を PD に置き換える可能性があります。

TiDB クラスターの高可用性と災害復旧機能を向上させるには、TiKV ノードを物理的にできるだけ分散させることをお勧めします。たとえば、TiKV ノードは、異なるラックや異なるデータ センターに分散することもできます。 TiKV のトポロジー情報に従って、PD スケジューラーはバックグラウンドで自動的にスケジューリングを実行して、リージョンの各レプリカを可能な限り分離し、災害復旧の機能を最大化します。

このメカニズムを有効にするには、デプロイ時にクラスターのトポロジー情報、特に TiKV の位置情報が PD に報告されるように、TiKV と PD を適切に構成する必要があります。始める前に、まず[TiUPを使用して TiDBをデプロイ](/production-deployment-using-tiup.md)を参照してください。

## クラスター トポロジに基づいて<code>labels</code>構成する {#configure-code-labels-code-based-on-the-cluster-topology}

### TiKV およびTiFlashの<code>labels</code>を構成する {#configure-code-labels-code-for-tikv-and-tiflash}

コマンドライン フラグを使用するか、TiKV またはTiFlash構成ファイルを設定して、キーと値のペアの形式でいくつかの属性をバインドできます。これらの属性は`labels`と呼ばれます。 TiKV とTiFlashが開始されると、ユーザーは TiKV とTiFlashノードの場所を特定できるように、 `labels` PD に報告します。

トポロジーにゾーン &gt; データセンター (DC) &gt; ラック &gt; ホストの 4 つのレイヤーがあり、これらのラベル (ゾーン、DC、ラック、ホスト) を使用して TiKV およびTiFlashの場所を設定できるとします。 TiKV およびTiFlashのラベルを設定するには、次のいずれかの方法を使用できます。

-   コマンドライン フラグを使用して、TiKV インスタンスを開始します。

    ```shell
    tikv-server --labels zone=<zone>,dc=<dc>,rack=<rack>,host=<host>
    ```

-   TiKV 構成ファイルで構成します。

    ```toml
    [server]
    [server.labels]
    zone = "<zone>"
    dc = "<dc>"
    rack = "<rack>"
    host = "<host>"
    ```

TiFlashのラベルを設定するには、tiflash-proxy の構成ファイルである`tiflash-learner.toml`ファイルを使用できます。

```toml
[server]
[server.labels]
zone = "<zone>"
dc = "<dc>"
rack = "<rack>"
host = "<host>"
```

### (オプション) TiDB の<code>labels</code>を構成する {#optional-configure-code-labels-code-for-tidb}

[Followerの読み取り](/follower-read.md)が有効になっている場合、TiDB が同じリージョンからデータを読み取ることを優先する場合は、TiDB ノードに`labels`を構成する必要があります。

構成ファイルを使用して、TiDB に`labels`を設定できます。

```toml
[labels]
zone = "<zone>"
dc = "<dc>"
rack = "<rack>"
host = "<host>"
```

> **ノート：**
>
> 現在、TiDB は`zone`のラベルに依存して、同じリージョンにあるレプリカを照合して選択します。この機能を使用するには、 [PD の`location-labels`の構成](#configure-location-labels-for-pd)の場合は`zone`含め、TiDB、TiKV、およびTiFlashの場合は`labels`構成する場合は`zone`を構成する必要があります。詳細については、 [TiKV およびTiFlashの`labels`を構成する](#configure-labels-for-tikv-and-tiflash)を参照してください。

### PD の<code>location-labels</code>を構成する {#configure-code-location-labels-code-for-pd}

上記の説明によると、ラベルは、TiKV 属性を記述するために使用される任意のキーと値のペアにすることができます。しかし、PD は位置関連のラベルとこれらのラベルのレイヤー関係を識別できません。したがって、TiKV ノード トポロジを理解するには、PD に対して次の構成を行う必要があります。

文字列の配列として定義され、 `location-labels`は PD の構成です。この構成の各項目は、TiKV `labels`のキーに対応しています。さらに、各キーのシーケンスは、異なるラベルのレイヤー関係を表します (分離レベルは左から右に減少します)。

構成にはデフォルト値がないため、 `location-labels`の値 ( `zone` 、 `rack` 、または`host`など) をカスタマイズできます。また、この構成では、TiKVサーバーラベルと一致する限り、ラベル レベルの数に制限**はありません**(3 レベルは必須ではありません)。

> **ノート：**
>
> -   構成を有効にするには、PD 用に`location-labels`構成し、TiKV 用に`labels`同時に構成する必要があります。そうしないと、PD はトポロジーに従ってスケジューリングを実行しません。
> -   SQL で配置ルールを使用する場合、TiKV に`labels`を設定するだけで済みます。現在、SQL の配置規則は PD の`location-labels`構成と互換性がなく、この構成を無視します。 SQL で`location-labels`と配置規則を同時に使用することはお勧めしません。そうしないと、予期しない結果が生じる可能性があります。

`location-labels`を構成するには、クラスターの状況に応じて次のいずれかの方法を選択します。

-   PD クラスターが初期化されていない場合は、PD 構成ファイルで`location-labels`を構成します。

    {{< copyable "" >}}

    ```toml
    [replication]
    location-labels = ["zone", "rack", "host"]
    ```

-   PD クラスタがすでに初期化されている場合は、pd-ctl ツールを使用してオンラインで変更します。

    {{< copyable "" >}}

    ```bash
    pd-ctl config set location-labels zone,rack,host
    ```

### PD の<code>isolation-level</code>を構成する {#configure-code-isolation-level-code-for-pd}

`location-labels`が構成されている場合、PD 構成ファイルで`isolation-level`構成することにより、TiKV クラスターのトポロジ分離要件をさらに強化できます。

上記の手順に従って`location-labels`構成して 3 層のクラスター トポロジを作成したと仮定します。ゾーン -&gt; ラック -&gt; ホスト、次のように`isolation-level`から`zone`を構成できます。

{{< copyable "" >}}

```toml
[replication]
isolation-level = "zone"
```

PD クラスタがすでに初期化されている場合は、pd-ctl ツールを使用してオンラインで変更する必要があります。

{{< copyable "" >}}

```bash
pd-ctl config set isolation-level zone
```

`location-level`構成は文字列の配列で、キー`location-labels`に対応する必要があります。このパラメータは、TiKV トポロジ クラスタの最小および必須の分離レベル要件を制限します。

> **ノート：**
>
> `isolation-level`はデフォルトで空です。これは、分離レベルに必須の制限がないことを意味します。これを設定するには、PD に`location-labels`設定し、値`isolation-level`が`location-labels`の名前の 1 つであることを確認する必要があります。

### TiUPを使用してクラスターを構成する (推奨) {#configure-a-cluster-using-tiup-recommended}

TiUPを使用してクラスターをデプロイする場合、TiKV の場所を[初期設定ファイル](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)で構成できます。 TiUP は、展開中に TiKV、PD、およびTiFlashに対応する構成ファイルを生成します。

次の例では、 `zone/host`の 2 層トポロジーが定義されています。クラスターの TiKV ノードは、z1、z2、および z3 の 3 つのゾーンに分散され、各ゾーンには h1、h2、h3、および h4 の 4 つのホストがあります。 z1 では、4 つの TiKV インスタンスが 2 つのホスト (h1 に`tikv-1`と`tikv-2` 、h2 に`tikv-3`と`tikv-4`にデプロイされます。 h3 に`tiflash-1` 、h4 に`tiflash-2` 2 つのTiFlashインスタンスが他の 2 つのホストにデプロイされます。 z2 と z3 では、2 つの TiKV インスタンスが 2 つのホストにデプロイされ、2 つのTiFlashインスタンスが他の 2 つのホストにデプロイされます。次の例では、 `tikv-n` `n`番目の TiKV ノードの IP アドレスを表し、 `tiflash-n` `n`番目のTiFlashノードの IP アドレスを表します。

```
server_configs:
  pd:
    replication.location-labels: ["zone", "host"]

tikv_servers:
# z1
  - host: tikv-1
    config:
      server.labels:
        zone: z1
        host: h1
   - host: tikv-2
    config:
      server.labels:
        zone: z1
        host: h1
  - host: tikv-3
    config:
      server.labels:
        zone: z1
        host: h2
  - host: tikv-4
    config:
      server.labels:
        zone: z1
        host: h2
# z2
  - host: tikv-5
    config:
      server.labels:
        zone: z2
        host: h1
   - host: tikv-6
    config:
      server.labels:
        zone: z2
        host: h2
# z3
  - host: tikv-7
    config:
      server.labels:
        zone: z3
        host: h1
  - host: tikv-8
    config:
      server.labels:
        zone: z3
        host: h2s
tiflash_servers:
# z1
  - host: tiflash-1
    learner_config:
      server.labels:
        zone: z1
        host: h3
   - host: tiflash-2
    learner_config:
      server.labels:
        zone: z1
        host: h4
# z2
  - host: tiflash-3
    learner_config:
      server.labels:
        zone: z2
        host: h3
   - host: tiflash-4
    learner_config:
      server.labels:
        zone: z2
        host: h4
# z3
  - host: tiflash-5
    learner_config:
      server.labels:
        zone: z3
        host: h3
  - host: tiflash-6
    learner_config:
      server.labels:
        zone: z3
        host: h4
```

詳細については、 [地理的に分散された配置トポロジ](/geo-distributed-deployment-topology.md)を参照してください。

> **ノート：**
>
> 構成ファイルで`replication.location-labels`構成していない場合、このトポロジー ファイルを使用してクラスターをデプロイすると、エラーが発生する可能性があります。クラスターをデプロイする前に、構成ファイルで`replication.location-labels`が構成されていることを確認することをお勧めします。

## トポロジ ラベルに基づく PD スケジュール {#pd-schedules-based-on-topology-label}

PD は、同じデータの異なるレプリカが可能な限り分散されるように、ラベルレイヤーに従ってレプリカをスケジュールします。

例として、前のセクションのトポロジを取り上げます。

クラスタ レプリカの数が 3 ( `max-replicas=3` ) であるとします。合計で 3 つのゾーンがあるため、PD は各リージョンの 3 つのレプリカがそれぞれ z1、z2、および z3 に配置されるようにします。このようにして、1 つのデータセンターに障害が発生した場合でも、TiDB クラスターは引き続き使用できます。

次に、クラスタ レプリカの数が 5 ( `max-replicas=5` ) であるとします。合計で 3 つのゾーンしかないため、PD はゾーン レベルでの各レプリカの分離を保証できません。この状況では、PD スケジューラはホスト レベルでレプリカの分離を保証します。つまり、リージョンの複数のレプリカが同じゾーンに分散されていても、同じホストには分散されていない可能性があります。

5 レプリカ構成の場合、z3 に障害が発生するか、全体として分離され、一定期間 ( `max-store-down-time`で制御) が経過しても回復できない場合、PD はスケジューリングによって 5 つのレプリカを構成します。現時点では、4 つのホストのみが利用可能です。これは、ホスト レベルの分離が保証されず、複数のレプリカが同じホストにスケジュールされる可能性があることを意味します。ただし、 `isolation-level`値を空のままにするのではなく`zone`に設定すると、リージョンレプリカの物理的な分離の最小要件が指定されます。つまり、PD は、同じリージョンのレプリカが異なるゾーンに分散されるようにします。 PD は、この分離制限に従うことが複数のレプリカに対する`max-replicas`の要件を満たさない場合でも、対応するスケジューリングを実行しません。

たとえば、TiKV クラスターは 3 つのデータ ゾーン z1、z2、および z3 に分散されています。各リージョンには必要に応じて 3 つのレプリカがあり、PD は同じリージョンの 3 つのレプリカをこれら 3 つのデータ ゾーンにそれぞれ配布します。 z1 で停電が発生し、一定期間 (デフォルトでは[`max-store-down-time`](/pd-configuration-file.md#max-store-down-time)分と 30 分で制御) 後に復旧できない場合、PD は z1 のリージョンレプリカが使用できなくなったと判断します。ただし、 `isolation-level`が`zone`に設定されているため、PD は、同じリージョンの異なるレプリカが同じデータ ゾーンでスケジュールされないことを厳密に保証する必要があります。 z2 と z3 の両方にすでにレプリカがあるため、現時点でレプリカが 2 つしかない場合でも、PD は最小分離レベルの制限である`isolation-level`の下ではスケジューリングを実行しません。

同様に、 `isolation-level`が`rack`に設定されている場合、最小分離レベルは同じデータ センター内の異なるラックに適用されます。この構成では、可能であればゾーンレイヤーでのアイソレーションが最初に保証されます。ゾーン レベルでの分離を保証できない場合、PD は、同じゾーン内の同じラックに異なるレプリカをスケジュールすることを回避しようとします。 PD が最初にラックの分離レベルを保証し、次にホストのレベルを保証する`isolation-level` `host`に設定されている場合、スケジューリングは同様に機能します。

要約すると、PD は現在のトポロジに従って、クラスターのディザスター リカバリーを最大化します。したがって、特定のレベルのディザスター リカバリーを達成したい場合は、トポロジーに従って、 `max-replicas`の数よりも多くのマシンを異なるサイトにデプロイします。 TiDB は、さまざまなシナリオに従ってデータのトポロジ分離レベルをより柔軟に制御するために、 `isolation-level`などの必須構成項目も提供します。
