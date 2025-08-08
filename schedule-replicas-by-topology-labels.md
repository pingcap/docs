---
title: Schedule Replicas by Topology Labels
summary: トポロジ ラベルによってレプリカをスケジュールする方法を学習します。
---

# トポロジラベルによるレプリカのスケジュール {#schedule-replicas-by-topology-labels}

> **注記：**
>
> TiDB v5.3.0 では[SQLの配置ルール](/placement-rules-in-sql.md)が導入されました。これにより、テーブルとパーティションの配置をより簡単に設定できるようになります。将来のリリースでは、SQL の配置ルールが PD による配置設定に置き換えられる可能性があります。

TiDBクラスターの高可用性と災害復旧能力を向上させるには、TiKVノードを可能な限り物理的に分散させることが推奨されます。例えば、TiKVノードを異なるラックや異なるデータセンターに分散配置することも可能です。PDスケジューラは、TiKVのトポロジ情報に基づいて、リージョン内の各レプリカを可能な限り分離するようにバックグラウンドで自動的にスケジューリングを行い、災害復旧能力を最大限に高めます。

このメカニズムを有効にするには、TiKVとPDを適切に設定し、クラスターのトポロジ情報、特にTiKVの位置情報（特にデプロイメント中にPDに報告される）が適切に送信されるようにする必要があります。開始する前に、まず[TiUPを使用して TiDBをデプロイ](/production-deployment-using-tiup.md)ご確認ください。

## TiKV、 TiFlash、TiDBの<code>labels</code>を構成する {#configure-code-labels-code-for-tikv-tiflash-and-tidb}

クラスター トポロジに基づいて、TiKV、 TiFlash、および TiDB に`labels`設定できます。

### TiUPを使用してクラスターを構成する (推奨) {#configure-a-cluster-using-tiup-recommended}

TiUPを使用してクラスターをデプロイする場合、 [初期化設定ファイル](/production-deployment-using-tiup.md#step-3-initialize-the-cluster-topology-file)で TiKV の場所を設定できます。TiUPは、デプロイ中に TiDB、TiKV、PD、およびTiFlashの対応する設定ファイルを生成します。

以下の例では、2層トポロジ（ `zone/host`が定義されています。クラスターのTiDBノード、TiKVノード、およびTiFlashノードは、3つのゾーン（z1、z2、z3）に分散されています。

-   各ゾーンには、TiDB インスタンスがデプロイされているホストが 2 つあり、各ホストには個別の TiDB インスタンスがデプロイされています。
-   各ゾーンには、TiKVインスタンスがデプロイされたホストが2つあります。z1では、各ホストに2つのTiKVインスタンスがデプロイされています。z2とz3では、各ホストに個別のTiKVインスタンスがデプロイされています。
-   各ゾーンには、 TiFlashインスタンスがデプロイされているホストが 2 つあり、各ホストには個別のTiFlashインスタンスがデプロイされています。

次の例では、 `tidb-host-machine-n` `n`番目の TiDB ノードの IP アドレスを表し、 `tikv-host-machine-n` `n`番目の TiKV ノードの IP アドレスを表し、 `tiflash-host-machine-n` `n`番目のTiFlashノードの IP アドレスを表します。

    server_configs:
      pd:
        replication.location-labels: ["zone", "host"]
    tidb_servers:
    # z1
      - host: tidb-host-machine-1
        config:
          labels:
            zone: z1
            host: tidb-host-machine-1
      - host: tidb-host-machine-2
        config:
          labels:
            zone: z1
            host: tidb-host-machine-2
    # z2
      - host: tidb-host-machine-3
        config:
          labels:
            zone: z2
            host: tidb-host-machine-3
      - host: tikv-host-machine-4
        config:
          labels:
            zone: z2
            host: tidb-host-machine-4
    # z3
      - host: tidb-host-machine-5
        config:
          labels:
            zone: z3
            host: tidb-host-machine-5
      - host: tidb-host-machine-6
        config:
          labels:
            zone: z3
            host: tidb-host-machine-6
    tikv_servers:
    # z1
      # machine-1 on z1
      - host: tikv-host-machine-1
        port: 20160
        config:
          server.labels:
            zone: z1
            host: tikv-host-machine-1
      - host: tikv-host-machine-1
        port: 20161
        config:
          server.labels:
            zone: z1
            host: tikv-host-machine-1
      # machine-2 on z1
      - host: tikv-host-machine-2
        port: 20160
        config:
          server.labels:
            zone: z1
            host: tikv-host-machine-2
      - host: tikv-host-machine-2
        port: 20161
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

詳細は[地理的に分散した展開トポロジ](/geo-distributed-deployment-topology.md)参照。

> **注記：**
>
> 設定ファイルで`replication.location-labels`設定されていない場合、このトポロジファイルを使用してクラスタをデプロイするとエラーが発生する可能性があります。クラスタをデプロイする前に、設定ファイルで`replication.location-labels`が設定されていることを確認することをお勧めします。

### コマンドラインまたは構成ファイルを使用してクラスターを構成する {#configure-a-cluster-using-command-lines-or-configuration-files}

#### TiKVとTiFlashの<code>labels</code>を設定する {#configure-code-labels-code-for-tikv-and-tiflash}

コマンドラインフラグを使用するか、TiKVまたはTiFlash構成ファイルを設定すると、キーと値のペアの形式でいくつかの属性をバインドできます。これらの属性は`labels`呼ばれます。TiKVとTiFlashは起動後、PDに`labels`報告し、ユーザーがTiKVノードとTiFlashノードの位置を特定できるようにします。

トポロジがゾーン &gt; データセンター（DC） &gt; ラック &gt; ホストの4層で構成されており、これらのラベル（ゾーン、DC、ラック、ホスト）を使用してTiKVとTiFlashの位置を設定できます。TiKVとTiFlashのラベルを設定するには、次のいずれかの方法を使用します。

-   コマンドラインフラグを使用して TiKV インスタンスを起動します。

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

TiFlashのラベルを設定するには、tiflash-proxy の設定ファイルである`tiflash-learner.toml`ファイルを使用できます。

```toml
[server]
[server.labels]
zone = "<zone>"
dc = "<dc>"
rack = "<rack>"
host = "<host>"
```

#### (オプション) TiDBの<code>labels</code>を構成する {#optional-configure-code-labels-code-for-tidb}

[Followerが読んだ](/follower-read.md)有効になっている場合、TiDB が同じリージョンからのデータを優先的に読み取るようにするには、TiDB ノードに対して`labels`設定する必要があります。

構成ファイルを使用して、TiDB に`labels`設定できます。

```toml
[labels]
zone = "<zone>"
dc = "<dc>"
rack = "<rack>"
host = "<host>"
```

> **注記：**
>
> 現在、TiDBは、同じリージョンにあるレプリカのマッチングと選択に`zone`ラベルを使用しています。この機能を使用するには、 [PDの`location-labels`設定](#configure-location-labels-for-pd)設定する際に`zone`追加し、TiDB、TiKV、 TiFlashを設定する際に`labels`設定する際に`zone`追加する必要があります。詳細については、 [TiKVとTiFlashの`labels`を設定する](#configure-labels-for-tikv-and-tiflash)参照してください。

## PDの<code>location-labels</code>を設定する {#configure-code-location-labels-code-for-pd}

上記の説明によると、ラベルはTiKV属性を記述するために使用される任意のキーと値のペアです。しかし、PDは位置関連のラベルとそれらのラベルのレイヤー関係を識別できません。そのため、PDがTiKVノードのトポロジを理解できるように、以下の設定を行う必要があります。

文字列の配列として定義され、 `location-labels` PDの設定です。この設定の各項目はTiKV `labels`のキーに対応しています。また、各キーの順序は異なるラベルのレイヤー関係を表します（分離レベルは左から右に向かって減少します）。

この設定にはデフォルト値がないため、 `location-labels`の値は`zone` 、 `rack` 、 `host`など、自由にカスタマイズできます。また、この設定では、TiKVサーバーのラベルと一致している限り、ラベルレベル数に制限はありませ**ん**（3レベルは必須ではありません）。

> **注記：**
>
> -   設定を有効にするには、PDに`location-labels` 、TiKVに`labels`同時に設定する必要があります。そうしないと、PDはトポロジに従ってスケジューリングを実行しません。
> -   SQL の配置ルールを使用する場合、TiKV の場合は`labels`のみ設定する必要があります。現在、SQL の配置ルールは PD の`location-labels`設定と互換性がなく、この設定は無視されます。5 `location-labels` SQL の配置ルールを同時に使用することは推奨されません。予期しない結果が発生する可能性があります。

`location-labels`構成するには、クラスターの状況に応じて次のいずれかの方法を選択します。

-   PD クラスターが初期化されていない場合は、PD 構成ファイルで`location-labels`構成します。

    ```toml
    [replication]
    location-labels = ["zone", "rack", "host"]
    ```

-   PD クラスターがすでに初期化されている場合は、pd-ctl ツールを使用してオンラインで変更を加えます。

    ```bash
    pd-ctl config set location-labels zone,rack,host
    ```

## PDの<code>isolation-level</code>を設定する {#configure-code-isolation-level-code-for-pd}

`location-labels`が設定されている場合は、PD 設定ファイルで`isolation-level`設定することで、TiKV クラスターのトポロジ分離要件をさらに強化できます。

上記の手順に従って`location-labels`ゾーン -&gt; ラック -&gt; ホストと設定して 3 層クラスタ トポロジを作成したと仮定すると、 `isolation-level` ～ `zone`次のように設定できます。

```toml
[replication]
isolation-level = "zone"
```

PD クラスターがすでに初期化されている場合は、pd-ctl ツールを使用してオンラインで変更を行う必要があります。

```bash
pd-ctl config set isolation-level zone
```

`location-level`設定は文字列の配列であり、キー`location-labels`に対応している必要があります。このパラメータは、TiKVトポロジクラスタにおける最小および必須の分離レベル要件を制限します。

> **注記：**
>
> `isolation-level`はデフォルトで空です。つまり、分離レベルに必須の制限はありません。分離レベルを設定するには、PD に`location-labels`設定し、 `isolation-level`値が`location-labels`名前のいずれかであることを確認する必要があります。

## トポロジラベルに基づくPDスケジュール {#pd-schedules-based-on-topology-label}

PD はラベルレイヤーに従ってレプリカをスケジュールし、同じデータの異なるレプリカが可能な限り分散されるようにします。

前のセクションのトポロジを例に挙げます。

クラスタのレプリカ数が3（ `max-replicas=3` ）であると仮定します。合計3つのゾーンがあるため、PDは各リージョンの3つのレプリカがそれぞれz1、z2、z3に配置されるように保証します。これにより、1つのゾーンに障害が発生してもTiDBクラスタは引き続き利用可能です。

次に、クラスタレプリカの数が5（ `max-replicas=5` ）であると仮定します。ゾーンは合計3つしかないため、PDはゾーンレベルで各レプリカの分離を保証することができません。この場合、PDスケジューラはホストレベルでレプリカの分離を保証します。つまり、リージョンの複数のレプリカが同じゾーンに分散されていても、同じホスト上には分散されていない可能性があります。

5 つのレプリカ構成の場合、z3 に障害が発生するか、z3 全体が分離され、一定期間 ( `max-store-down-time`で制御) 後に回復できない場合、PD はスケジュールによって 5 つのレプリカを構成します。この時点では、使用できるホストは 4 つだけです。つまり、ホストレベルの分離は保証されず、複数のレプリカが同じホストにスケジュールされる可能性があります。ただし、 `isolation-level`値が空のままではなく`zone`に設定されている場合、これはリージョンレプリカの最小の物理的な分離要件を指定します。つまり、PD は同じリージョンのレプリカが異なるゾーンに分散されていることを保証します。この分離制限に従っても、複数のレプリカの`max-replicas`の要件が満たされない場合でも、PD は対応するスケジュールを実行しません。

`isolation-level`設定が`zone`に設定されている場合、これは物理レベルでのリージョンレプリカの最小分離要件を指定します。この場合、PD は常に同じリージョンのレプリカが異なるゾーンに分散されることを保証します。この分離制限に従うことで`max-replicas`のマルチレプリカ要件が満たされない場合でも、PD はそれに応じてスケジュールを設定しません。3 つのデータ ゾーン (z1、z2、z3) に分散された TiKV クラスターを例にとると、各リージョンに 3 つのレプリカが必要な場合、PD は同じリージョンの 3 つのレプリカをそれぞれこれらの 3 つのデータ ゾーンに分散します。z1 で停電が発生し、一定時間 (デフォルトでは 30 分、 [`max-store-down-time`](/pd-configuration-file.md#max-store-down-time)によって制御) が経過しても回復できない場合、PD は z1 のリージョンレプリカが使用できなくなったと判断します。ただし、 `isolation-level` `zone`に設定されているため、PD は、同じリージョンの異なるレプリカが同じデータ ゾーンにスケジュールされないことを厳密に保証する必要があります。 z2 と z3 の両方にすでにレプリカがあるため、現時点でレプリカが 2 つしかない場合でも、PD は最小分離レベル制限`isolation-level`の下ではスケジュールを実行しません。

同様に、 `isolation-level` `rack`に設定すると、同一データセンター内の異なるラックに最小分離レベルが適用されます。この構成では、ゾーンレイヤーでの分離が可能な限り最初に保証されます。ゾーンレベルでの分離が保証できない場合、PD は同じゾーン内の同じラックに異なるレプリカがスケジュールされることを避けようとします。5 `host` `isolation-level`設定した場合も同様にスケジューリングが行われ、PD はまずラックの分離レベルを保証し、次にホストの分離レベルを保証します。

要約すると、PDは現在のトポロジに応じてクラスターの災害復旧を最大化します。したがって、一定レベルの災害復旧を実現したい場合は、トポロジに応じて、異なるサイトに`max-replicas`台以上のマシンを展開する必要があります。TiDBは、 `isolation-level`などの必須構成項目も提供しており、さまざまなシナリオに応じてデータのトポロジ分離レベルをより柔軟に制御できます。
