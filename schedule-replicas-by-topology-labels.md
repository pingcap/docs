---
title: Schedule Replicas by Topology Labels
summary: Learn how to schedule replicas by topology labels.
---

# トポロジラベルによるレプリカのスケジュール {#schedule-replicas-by-topology-labels}

> **ノート：**
>
> TiDB v5.3.0では、 [SQLの配置ルール](/placement-rules-in-sql.md)の実験的サポートが導入されています。これにより、テーブルとパーティションの配置を構成するためのより便利な方法が提供されます。 SQLの配置ルールは、将来のリリースで配置構成をPDに置き換える可能性があります。

TiDBクラスターの高可用性と障害復旧機能を向上させるために、TiKVノードを可能な限り物理的に分散させることをお勧めします。たとえば、TiKVノードは、さまざまなラックに分散したり、さまざまなデータセンターに分散したりすることができます。 TiKVのトポロジ情報に従って、PDスケジューラはバックグラウンドで自動的にスケジューリングを実行して、リージョンの各レプリカを可能な限り分離します。これにより、ディザスタリカバリの機能が最大化されます。

このメカニズムを有効にするには、TiKVとPDを適切に構成して、クラスタのトポロジー情報、特にTiKVロケーション情報が展開中にPDに報告されるようにする必要があります。始める前に、まず[TiUPを使用してTiDBをデプロイ](/production-deployment-using-tiup.md)を参照してください。

## クラスタトポロジに基づいて<code>labels</code>を構成する {#configure-code-labels-code-based-on-the-cluster-topology}

### TiKVの<code>labels</code>を構成する {#configure-code-labels-code-for-tikv}

コマンドラインフラグを使用するか、TiKV構成ファイルを設定して、キーと値のペアの形式でいくつかの属性をバインドできます。これらの属性は`labels`と呼ばれます。 TiKVが開始されると、その`labels`がPDに報告されるため、ユーザーはTiKVノードの場所を特定できます。

トポロジにゾーン&gt;ラック&gt;ホストの3つの層があり、これらのラベル（ゾーン、ラック、ホスト）を使用して、次のいずれかの方法でTiKVの場所を設定できると想定します。

-   コマンドラインフラグを使用して、TiKVインスタンスを開始します。

    {{< copyable "" >}}

    ```
    tikv-server --labels zone=<zone>,rack=<rack>,host=<host>
    ```

-   TiKV構成ファイルで構成します。

    {{< copyable "" >}}

    ```toml
    [server]
    labels = "zone=<zone>,rack=<rack>,host=<host>"
    ```

### PD <code>location-labels</code>を設定する {#configure-code-location-labels-code-for-pd}

上記の説明によると、ラベルはTiKV属性を説明するために使用される任意のキーと値のペアにすることができます。ただし、PDは、場所に関連するラベルとこれらのラベルのレイヤー関係を識別できません。したがって、PDがTiKVノードトポロジを理解するには、次の設定を行う必要があります。

文字列の配列として定義され、 `location-labels`はPDの構成です。この構成の各項目は、TiKV3のキーに対応してい`labels` 。さらに、各キーのシーケンスは、異なるラベルのレイヤー関係を表します（分離レベルは左から右に向かって減少します）。

構成にはデフォルト値がない`host` 、 `zone`などの`location-labels`の値をカスタマイズでき`rack` 。また、この構成では、TiKVサーバーのラベルと一致する限り、ラベルレベルの数に制限はあり**ませ**ん（3レベルでは必須ではありません）。

> **ノート：**
>
> -   設定を有効にするには、PD用に`location-labels`つ、TiKV用に`labels`を同時に設定する必要があります。それ以外の場合、PDはトポロジに従ってスケジューリングを実行しません。
> -   SQLで配置ルールを使用する場合は、TiKV用に`labels`を構成するだけで済みます。現在、SQLの配置ルールはPDの`location-labels`構成と互換性がなく、この構成を無視します。 SQLで`location-labels`と配置ルールを同時に使用することはお勧めしません。そうしないと、予期しない結果が発生する可能性があります。

`location-labels`を構成するには、クラスタの状況に応じて次のいずれかの方法を選択します。

-   PDクラスタが初期化されていない場合は、PD構成ファイルで`location-labels`を構成します。

    {{< copyable "" >}}

    ```toml
    [replication]
    location-labels = ["zone", "rack", "host"]
    ```

-   PDクラスタがすでに初期化されている場合は、pd-ctlツールを使用してオンラインで変更を加えます。

    {{< copyable "" >}}

    ```bash
    pd-ctl config set location-labels zone,rack,host
    ```

### PD <code>isolation-level</code>を構成する {#configure-code-isolation-level-code-for-pd}

`location-labels`が構成されている場合は、PD構成ファイルで`isolation-level`を構成することにより、TiKVクラスターのトポロジー分離要件をさらに強化できます。

上記の手順に従って`location-labels`を構成することにより、3層クラスタトポロジーを作成したと想定します。ゾーン-&gt;ラック-&gt;ホスト、次のように`isolation-level`から`zone`を構成できます。

{{< copyable "" >}}

```toml
[replication]
isolation-level = "zone"
```

PDクラスタがすでに初期化されている場合は、pd-ctlツールを使用してオンラインで変更を加える必要があります。

{{< copyable "" >}}

```bash
pd-ctl config set isolation-level zone
```

`location-level`構成は文字列の配列であり、 `location-labels`のキーに対応する必要があります。このパラメーターは、TiKVトポロジークラスターの最小および必須の分離レベル要件を制限します。

> **ノート：**
>
> デフォルトでは`isolation-level`は空です。これは、分離レベルに必須の制限がないことを意味します。これを設定するには、PD用に`location-labels`を構成し、 `isolation-level`の値が`location-labels`つの名前のいずれかであることを確認する必要があります。

### TiUPを使用してクラスタを構成する（推奨） {#configure-a-cluster-using-tiup-recommended}

TiUPを使用してクラスタをデプロイする場合、 [初期化構成ファイル](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)でTiKVの場所を構成できます。 TiUPは、展開中に対応するTiKVおよびPD構成ファイルを生成します。

次の例では、 `zone/host`の2層トポロジが定義されています。クラスタのTiKVノードは3つのゾーンに分散されており、各ゾーンには2つのホストがあります。 z1では、ホストごとに2つのTiKVインスタンスがデプロイされます。 z2およびz3では、ホストごとに1つのTiKVインスタンスがデプロイされます。次の例では、 `tikv-n`は`n`番目のTiKVノードのIPアドレスを表します。

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
```

詳細については、 [地理的に分散された展開トポロジ](/geo-distributed-deployment-topology.md)を参照してください。

> **ノート：**
>
> 構成ファイルで`replication.location-labels`を構成していない場合、このトポロジー・ファイルを使用してクラスタをデプロイすると、エラーが発生する可能性があります。クラスタをデプロイする前に、構成ファイルで`replication.location-labels`が構成されていることを確認することをお勧めします。

## トポロジーラベルに基づくPDスケジュール {#pd-schedules-based-on-topology-label}

PDは、ラベルレイヤーに従ってレプリカをスケジュールし、同じデータの異なるレプリカが可能な限り分散されるようにします。

前のセクションのトポロジーを例として取り上げます。

クラスタレプリカの数が3（ `max-replicas=3` ）であると想定します。合計で3つのゾーンがあるため、PDは、各リージョンの3つのレプリカがそれぞれz1、z2、およびz3に配置されるようにします。このようにして、1つのデータセンターに障害が発生した場合でも、TiDBクラスタを使用できます。

次に、クラスタレプリカの数が5（ `max-replicas=5` ）であると想定します。ゾーンは全部で3つしかないため、PDはゾーンレベルでの各レプリカの分離を保証できません。この状況では、PDスケジューラーはホストレベルでレプリカの分離を保証します。つまり、リージョンの複数のレプリカが同じゾーンに分散されている可能性がありますが、同じホストには分散されていない可能性があります。

5レプリカ構成の場合、z3が失敗するか、全体として分離され、一定期間（ `max-store-down-time`で制御）後に回復できない場合、PDはスケジューリングによって5つのレプリカを構成します。現時点では、4つのホストのみが使用可能です。これは、ホストレベルの分離が保証されておらず、複数のレプリカが同じホストにスケジュールされている可能性があることを意味します。ただし、 `isolation-level`の値が空のままではなく`zone`に設定されている場合、これはリージョンレプリカの最小の物理的分離要件を指定します。つまり、PDは、同じリージョンのレプリカが異なるゾーンに分散していることを確認します。この分離制限に従うことが複数のレプリカの`max-replicas`の要件を満たさない場合でも、PDは対応するスケジューリングを実行しません。

たとえば、TiKVクラスタは3つのデータゾーンz1、z2、およびz3に分散されています。各リージョンには必要に応じて3つのレプリカがあり、PDは同じリージョンの3つのレプリカをこれらの3つのデータゾーンにそれぞれ配布します。 z1で停電が発生し、一定期間（デフォルトでは[`max-store-down-time`](/pd-configuration-file.md#max-store-down-time)分と30分で制御）後に回復できない場合、PDはz1のリージョンレプリカが使用できなくなったと判断します。ただし、 `isolation-level`は`zone`に設定されているため、PDは、同じリージョンの異なるレプリカが同じデータゾーンでスケジュールされないことを厳密に保証する必要があります。 z2とz3の両方にすでにレプリカがあるため、現時点でレプリカが2つしかない場合でも、PDは最小分離レベル制限`isolation-level`の下でスケジューリングを実行しません。

同様に、 `isolation-level`が`rack`に設定されている場合、最小分離レベルは同じデータセンター内の異なるラックに適用されます。この構成では、可能であれば、ゾーン層での分離が最初に保証されます。ゾーンレベルでの分離が保証できない場合、PDは、同じゾーン内の同じラックに異なるレプリカをスケジュールすることを回避しようとします。 `isolation-level`が`host`に設定されている場合、スケジューリングは同様に機能します。ここで、PDは最初にラックの分離レベルを保証し、次にホストのレベルを保証します。

要約すると、PDは、現在のトポロジに従ってクラスタのディザスタリカバリを最大化します。したがって、一定レベルのディザスタリカバリを実現する場合は、トポロジに応じて、 `max-replicas`の数よりも多くのマシンをさまざまなサイトに展開します。 TiDBには、さまざまなシナリオに応じてデータのトポロジ分離レベルをより柔軟に制御するための`isolation-level`などの必須の構成項目も用意されています。
