---
title: Schedule Replicas by Topology Labels
summary: Learn how to schedule replicas by topology labels.
---

# トポロジーラベルごとにレプリカをスケジュールする {#schedule-replicas-by-topology-labels}

> **注記：**
>
> TiDB v5.3.0 では[SQL の配置ルール](/placement-rules-in-sql.md)が導入されています。これにより、テーブルとパーティションの配置を構成するためのより便利な方法が提供されます。将来のリリースでは、SQL の配置ルールによって配置構成が PD に置き換えられる可能性があります。

TiDB クラスターの高可用性と災害復旧機能を向上させるには、TiKV ノードを可能な限り物理的に分散させることをお勧めします。たとえば、TiKV ノードを異なるラックに分散したり、異なるデータ センターに分散したりすることもできます。 TiKV のトポロジー情報に従って、PD スケジューラーがバックグラウンドで自動的にスケジューリングを実行し、リージョンの各レプリカを可能な限り分離し、災害復旧の能力を最大化します。

このメカニズムを有効にするには、展開中にクラスターのトポロジー情報、特に TiKV の位置情報が PD に報告されるように、TiKV と PD を適切に構成する必要があります。始める前に、まず[TiUPを使用して TiDBをデプロイ](/production-deployment-using-tiup.md)を参照してください。

## クラスタートポロジに基づいて<code>labels</code>構成する {#configure-code-labels-code-based-on-the-cluster-topology}

### TiKV およびTiFlashの<code>labels</code>を構成する {#configure-code-labels-code-for-tikv-and-tiflash}

コマンドライン フラグを使用するか、TiKV またはTiFlash構成ファイルを設定して、キーと値のペアの形式で一部の属性をバインドできます。これらの属性は`labels`と呼ばれます。 TiKV およびTiFlashが開始されると、それらの`labels` PD に報告されるため、ユーザーは TiKV およびTiFlashノードの場所を特定できます。

トポロジにはゾーン &gt; データ センター (DC) &gt; ラック &gt; ホストの 4 つの層があると仮定します。これらのラベル (ゾーン、DC、ラック、ホスト) を使用して TiKV およびTiFlashの場所を設定できます。 TiKV およびTiFlashのラベルを設定するには、次のいずれかの方法を使用できます。

-   TiKV インスタンスを開始するには、コマンドライン フラグを使用します。

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

TiFlashのラベルを設定するには、 tflash-proxy の構成ファイルである`tiflash-learner.toml`ファイルを使用できます。

```toml
[server]
[server.labels]
zone = "<zone>"
dc = "<dc>"
rack = "<rack>"
host = "<host>"
```

### (オプション) TiDB の<code>labels</code>を構成する {#optional-configure-code-labels-code-for-tidb}

[Followerが読んだ](/follower-read.md)が有効な場合、TiDB が同じリージョンからのデータの読み取りを優先するようにするには、TiDB ノードに対して`labels`を構成する必要があります。

構成ファイルを使用して、TiDB に`labels`を設定できます。

```toml
[labels]
zone = "<zone>"
dc = "<dc>"
rack = "<rack>"
host = "<host>"
```

> **注記：**
>
> 現在、TiDB は`zone`ラベルに依存して、同じリージョン内にあるレプリカを照合して選択します。この機能を使用するには、 [PD の`location-labels`の設定](#configure-location-labels-for-pd)の場合は`zone`を含める必要があり、 TiDB、TiKV、およびTiFlashに対して`labels`構成する場合は`zone`を構成する必要があります。詳細については、 [TiKV およびTiFlashの`labels`を構成する](#configure-labels-for-tikv-and-tiflash)を参照してください。

### PD の<code>location-labels</code>を構成する {#configure-code-location-labels-code-for-pd}

上記の説明によれば、ラベルは、TiKV 属性を記述するために使用される任意のキーと値のペアにすることができます。しかし、PD は位置関連のラベルとこれらのラベルのレイヤー関係を識別できません。したがって、PD が TiKV ノード トポロジを理解するには、次の設定を行う必要があります。

文字列の配列として定義され、 `location-labels`は PD の構成です。この設定の各項目は TiKV `labels`のキーに対応します。さらに、各キーのシーケンスは、異なるラベルのレイヤー関係を表します (分離レベルは左から右に減少します)。

構成にはデフォルト値がないため、 `location-labels`の値を`zone` 、 `rack` 、または`host`などにカスタマイズできます。また、この構成では、TiKVサーバーのラベルと一致する限り、ラベル レベルの数に制限はありませ**ん**(3 レベルは必須ではありません)。

> **注記：**
>
> -   構成を有効にするには、PD に`location-labels` 、TiKV に`labels`同時に構成する必要があります。それ以外の場合、PD はトポロジに従ってスケジューリングを実行しません。
> -   SQL で配置ルールを使用する場合、TiKV に`labels`を設定するだけで済みます。現在、SQL の配置ルールは PD の`location-labels`構成と互換性がなく、この構成は無視されます。 SQL で`location-labels`と配置ルールを同時に使用することはお勧めできません。そうしないと、予期しない結果が発生する可能性があります。

`location-labels`を構成するには、クラスターの状況に応じて次のいずれかの方法を選択します。

-   PD クラスターが初期化されていない場合は、PD 構成ファイルで`location-labels`を構成します。

    ```toml
    [replication]
    location-labels = ["zone", "rack", "host"]
    ```

-   PD クラスターがすでに初期化されている場合は、pd-ctl ツールを使用してオンラインで変更を加えます。

    ```bash
    pd-ctl config set location-labels zone,rack,host
    ```

### PD の<code>isolation-level</code>を構成する {#configure-code-isolation-level-code-for-pd}

`location-labels`が構成されている場合は、PD 構成ファイルで`isolation-level`構成することで、TiKV クラスターのトポロジー分離要件をさらに強化できます。

上記の手順に従って`location-labels`構成して 3 層クラスター トポロジ`zone` `isolation-level`次のように構成できます。

```toml
[replication]
isolation-level = "zone"
```

PD クラスターがすでに初期化されている場合は、pd-ctl ツールを使用してオンラインで変更を行う必要があります。

```bash
pd-ctl config set isolation-level zone
```

`location-level`構成は文字列の配列であり、キー`location-labels`に対応する必要があります。このパラメータは、TiKV トポロジ クラスタの最小および必須の分離レベル要件を制限します。

> **注記：**
>
> デフォルトでは`isolation-level`は空です。これは、分離レベルに必須の制限がないことを意味します。これを設定するには、PD に`location-labels`設定し、 `isolation-level`の値が`location-labels`の名前のいずれかであることを確認する必要があります。

### TiUPを使用してクラスターを構成する (推奨) {#configure-a-cluster-using-tiup-recommended}

TiUPを使用してクラスターをデプロイする場合、 [初期化設定ファイル](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)で TiKV の場所を構成できます。 TiUP は、展開中に TiKV、PD、およびTiFlashに対応する構成ファイルを生成します。

次の例では、2 層トポロジ`zone/host`が定義されています。クラスターの TiKV ノードとTiFlashノードは、z1、z2、および z3 の 3 つのゾーンに分散されます。

-   各ゾーンには、TiKV インスタンスがデプロイされたホストが 2 つあります。 z1 では、各ホストに 2 つの TiKV インスタンスがデプロイされています。 z2 および z3 では、各ホストに個別の TiKV インスタンスがデプロイされます。
-   各ゾーンには、 TiFlashインスタンスがデプロイされたホストが 2 つあり、各ホストには個別のTiFlashインスタンスがデプロイされています。

次の例では、 `tikv-host-machine-n` `n`番目の TiKV ノードの IP アドレスを表し、 `tiflash-host-machine-n` `n`番目のTiFlashノードの IP アドレスを表します。

    server_configs:
      pd:
        replication.location-labels: ["zone", "host"]

    tikv_servers:
    # z1
      # machine-1 on z1
      - host: tikv-host-machine-1
        port：20160
        config:
          server.labels:
            zone: z1
            host: tikv-host-machine-1
      - host: tikv-host-machine-1
        port：20161
        config:
          server.labels:
            zone: z1
            host: tikv-host-machine-1
      # machine-2 on z1
      - host: tikv-host-machine-2
        port：20160
        config:
          server.labels:
            zone: z1
            host: tikv-host-machine-2
      - host: tikv-host-machine-2
        port：20161
        config:
          server.labels:
            zone: z1
            host: tikv-host-machine-2
    # z2
      - host: tikv-host-machine-3
        config:
          server.labels:
            zone: z2
            host: tikv-host-machine-3
      - host: tikv-host-machine-4
        config:
          server.labels:
            zone: z2
            host: tikv-host-machine-4
    # z3
      - host: tikv-host-machine-5
        config:
          server.labels:
            zone: z3
            host: tikv-host-machine-5
      - host: tikv-host-machine-6
        config:
          server.labels:
            zone: z3
            host: tikv-host-machine-6

    tiflash_servers:
    # z1
      - host: tiflash-host-machine-1
        learner_config:
          server.labels:
            zone: z1
            host: tiflash-host-machine-1
      - host: tiflash-host-machine-2
        learner_config:
          server.labels:
            zone: z1
            host: tiflash-host-machine-2
    # z2
      - host: tiflash-host-machine-3
        learner_config:
          server.labels:
            zone: z2
            host: tiflash-host-machine-3
      - host: tiflash-host-machine-4
        learner_config:
          server.labels:
            zone: z2
            host: tiflash-host-machine-4
    # z3
      - host: tiflash-host-machine-5
        learner_config:
          server.labels:
            zone: z3
            host: tiflash-host-machine-5
      - host: tiflash-host-machine-6
        learner_config:
          server.labels:
            zone: z3
            host: tiflash-host-machine-6

詳細は[地理的に分散された導入トポロジ](/geo-distributed-deployment-topology.md)を参照してください。

> **注記：**
>
> 構成ファイルで`replication.location-labels`構成していない場合、このトポロジ ファイルを使用してクラスターをデプロイすると、エラーが発生する可能性があります。クラスターをデプロイする前に、構成ファイルで`replication.location-labels`が構成されていることを確認することをお勧めします。

## トポロジ ラベルに基づいた PD スケジュール {#pd-schedules-based-on-topology-label}

PD は、同じデータの異なるレプリカが可能な限り分散されるように、ラベルレイヤーに従ってレプリカをスケジュールします。

前のセクションのトポロジを例に挙げます。

クラスターのレプリカの数が 3 ( `max-replicas=3` ) であると仮定します。合計 3 つのゾーンがあるため、PD は各リージョンの 3 つのレプリカがそれぞれ z1、z2、および z3 に配置されるようにします。このようにして、1 つのゾーンに障害が発生した場合でも、TiDB クラスターは引き続き使用できます。

次に、クラスター レプリカの数が 5 ( `max-replicas=5` ) であると仮定します。ゾーンは合計で 3 つしかないため、PD はゾーン レベルでの各レプリカの分離を保証できません。この状況では、PD スケジューラはホスト レベルでレプリカの分離を保証します。つまり、リージョンの複数のレプリカが同じゾーン内に分散されている可能性がありますが、同じホスト上には分散されていない可能性があります。

5 レプリカ構成の場合、z3 に障害が発生するか全体として分離され、一定期間 ( `max-store-down-time`で制御) が経過しても回復できない場合、PD はスケジューリングを通じて 5 つのレプリカを構成します。現時点では、使用可能なホストは 4 つだけです。これは、ホスト レベルの分離が保証されず、複数のレプリカが同じホストにスケジュールされる可能性があることを意味します。ただし、 `isolation-level`値を空のままではなく`zone`に設定すると、リージョンレプリカの物理的分離の最小要件が指定されます。つまり、PD は、同じリージョンのレプリカが異なるゾーンに分散していることを保証します。この分離制限に従うことが複数のレプリカの`max-replicas`の要件を満たさない場合でも、PD は対応するスケジューリングを実行しません。

`isolation-level`設定が`zone`に設定されている場合、物理レベルでのリージョンレプリカの最小分離要件が指定されます。この場合、PD は、同じリージョンのレプリカが異なるゾーンに分散されていることを常に保証します。この分離制限に従っても`max-replicas`のマルチレプリカ要件を満たさない場合でも、PD はそれに応じてスケジュールを設定しません。 3 つのデータ ゾーン (z1、z2、および z3) に分散された TiKV クラスターを例にとると、各リージョンに 3 つのレプリカが必要な場合、PD は同じリージョンの 3 つのレプリカをこれら 3 つのデータ ゾーンにそれぞれ分散します。 z1 で停電が発生し、一定期間 (デフォルトでは 30 分、 [`max-store-down-time`](/pd-configuration-file.md#max-store-down-time)で制御) が経過しても回復できない場合、PD は z1 のリージョンレプリカが使用できなくなったと判断します。ただし、 `isolation-level`が`zone`に設定されているため、PD は、同じリージョンの異なるレプリカが同じデータ ゾーンにスケジュールされないことを厳密に保証する必要があります。 z2 と z3 の両方にすでにレプリカがあるため、現時点でレプリカが 2 つしかない場合でも、PD は最小分離レベル制限`isolation-level`の下ではスケジューリングを実行しません。

同様に、 `isolation-level`を`rack`に設定すると、最小分離レベルが同じデータセンター内の異なるラックに適用されます。この構成では、可能であれば、ゾーンレイヤーでの分離が最初に保証されます。ゾーン レベルでの分離が保証できない場合、PD は、同じゾーン内の同じラックに異なるレプリカをスケジュールすることを回避しようとします。 `isolation-level`を`host`に設定すると、スケジューリングは同様に機能します。この場合、PD は最初にラックの分離レベルを保証し、次にホストのレベルを保証します。

要約すると、PD は現在のトポロジに従ってクラスターの災害復旧を最大化します。したがって、一定レベルの災害復旧を実現したい場合は、トポロジに従って異なるサイトに`max-replicas`台よりも多くのマシンをデプロイします。 TiDB には、さまざまなシナリオに従ってデータのトポロジ分離レベルをより柔軟に制御できるように、 `isolation-level`などの必須構成項目も用意されています。
