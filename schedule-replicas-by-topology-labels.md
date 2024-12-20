---
title: Schedule Replicas by Topology Labels
summary: トポロジ ラベルによってレプリカをスケジュールする方法を学習します。
---

# トポロジラベルによるレプリカのスケジュール {#schedule-replicas-by-topology-labels}

> **注記：**
>
> TiDB v5.3.0 では[SQL の配置ルール](/placement-rules-in-sql.md)が導入されました。これにより、テーブルとパーティションの配置を構成するためのより便利な方法が提供されます。将来のリリースでは、SQL の配置ルールによって PD による配置構成が置き換えられる可能性があります。

TiDB クラスターの高可用性と災害復旧機能を向上させるには、TiKV ノードを可能な限り物理的に分散させることが推奨されます。たとえば、TiKV ノードは、異なるラックや異なるデータセンターに分散できます。PD スケジューラは、TiKV のトポロジ情報に従って、バックグラウンドで自動的にスケジューリングを実行し、リージョンの各レプリカを可能な限り分離して、災害復旧機能を最大限に高めます。

このメカニズムを有効にするには、クラスターのトポロジ情報、特に TiKV の位置情報などがデプロイメント中に PD に報告されるように、TiKV と PD を適切に構成する必要があります。始める前に、まず[TiUPを使用して TiDB をデプロイ](/production-deployment-using-tiup.md)参照してください。

## TiKV、 TiFlash、TiDBの<code>labels</code>を構成する {#configure-code-labels-code-for-tikv-tiflash-and-tidb}

クラスター トポロジに基づいて、TiKV、 TiFlash、および TiDB に`labels`設定できます。

### TiUP を使用してクラスターを構成する (推奨) {#configure-a-cluster-using-tiup-recommended}

TiUP を使用してクラスターをデプロイする場合、 [初期化設定ファイル](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)で TiKV の場所を設定できます。TiUPは、デプロイ中に TiDB、TiKV、PD、およびTiFlashの対応する設定ファイルを生成します。

次の例では、2 層トポロジ`zone/host`が定義されています。クラスターの TiDB ノード、TiKV ノード、およびTiFlashノードは、3 つのゾーン z1、z2、および z3 に分散されています。

-   各ゾーンには、TiDB インスタンスがデプロイされているホストが 2 つあり、各ホストには個別の TiDB インスタンスがデプロイされています。
-   各ゾーンには、TiKV インスタンスがデプロイされているホストが 2 つあります。z1 では、各ホストに 2 つの TiKV インスタンスがデプロイされています。z2 と z3 では、各ホストに個別の TiKV インスタンスがデプロイされています。
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
> 構成ファイルで`replication.location-labels`設定していない場合、このトポロジ ファイルを使用してクラスターをデプロイするとエラーが発生する可能性があります。クラスターをデプロイする前に、構成ファイルで`replication.location-labels`設定されていることを確認することをお勧めします。

### コマンドラインまたは構成ファイルを使用してクラスターを構成する {#configure-a-cluster-using-command-lines-or-configuration-files}

#### TiKVとTiFlashの<code>labels</code>を設定する {#configure-code-labels-code-for-tikv-and-tiflash}

コマンドライン フラグを使用するか、TiKV またはTiFlash構成ファイルを設定して、キーと値のペアの形式でいくつかの属性をバインドできます。これらの属性は`labels`呼ばれます。TiKV とTiFlashが起動すると、PD に`labels`が報告され、ユーザーは TiKV ノードとTiFlashノードの場所を識別できるようになります。

トポロジにゾーン &gt; データセンター (DC) &gt; ラック &gt; ホストの 4 つのレイヤーがあり、これらのラベル (ゾーン、DC、ラック、ホスト) を使用して TiKV およびTiFlashの場所を設定できると仮定します。TiKV およびTiFlashのラベルを設定するには、次のいずれかの方法を使用できます。

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

[Followerが読んだ](/follower-read.md)が有効になっている場合、TiDB が同じリージョンからのデータを優先的に読み取るようにするには、TiDB ノードに`labels`設定する必要があります。

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
> 現在、TiDB は`zone`ラベルに依存して、同じリージョンにあるレプリカを一致させて選択します。この機能を使用するには、 [PD の`location-labels`の設定](#configure-location-labels-for-pd)ときに`zone`含め、 TiDB、TiKV、およびTiFlashの`labels`構成するときに`zone`構成する必要があります。詳細については、 [TiKVとTiFlashの`labels`を設定する](#configure-labels-for-tikv-and-tiflash)参照してください。

## PDの<code>location-labels</code>を設定する {#configure-code-location-labels-code-for-pd}

上記の説明によると、ラベルは TiKV 属性を記述するために使用される任意のキーと値のペアにすることができます。ただし、PD は場所関連のラベルとこれらのラベルのレイヤー関係を識別できません。そのため、PD が TiKV ノードのトポロジを理解できるように、次の構成を行う必要があります。

文字列の配列として定義され、 `location-labels` PD の構成です。この構成の各項目は、TiKV `labels`のキーに対応します。また、各キーのシーケンスは、異なるラベルのレイヤー関係を表します (分離レベルは左から右に向かって減少します)。

設定にはデフォルト値がないため、 `location-labels`の値を`zone` 、 `rack` 、 `host`などにカスタマイズできます。また、この設定では、TiKVサーバーのラベルと一致している限り、ラベル レベルの数に制限は**あり**ません (3 レベルは必須ではありません)。

> **注記：**
>
> -   設定を有効にするには、PD に`location-labels` 、TiKV に`labels`同時に設定する必要があります。そうしないと、PD はトポロジに従ってスケジュールを実行しません。
> -   SQL の配置ルールを使用する場合は、TiKV に対して`labels`のみを構成する必要があります。現在、SQL の配置ルールは PD の`location-labels`構成と互換性がなく、この構成は無視されます。5 と SQL の配置ルールを同時に使用することはお勧めしません。そうしないと、予期しない結果が発生する`location-labels`性があります。

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

## PDの<code>isolation-level</code>を設定する {#configure-code-isolation-level-code-for-pd}

`location-labels`設定されている場合は、PD 設定ファイルで`isolation-level`設定することで、TiKV クラスターのトポロジ分離要件をさらに強化できます。

上記の手順に従って`location-labels`ゾーン -&gt; ラック -&gt; ホストに設定して 3 層クラスタ トポロジを作成したと仮定すると、 `isolation-level` ～ `zone`次のように設定できます。

```toml
[replication]
isolation-level = "zone"
```

PD クラスターがすでに初期化されている場合は、pd-ctl ツールを使用してオンラインで変更を行う必要があります。

```bash
pd-ctl config set isolation-level zone
```

`location-level`構成は文字列の配列であり、 `location-labels`のキーに対応している必要があります。このパラメータは、TiKV トポロジ クラスターの最小および必須の分離レベル要件を制限します。

> **注記：**
>
> `isolation-level`はデフォルトでは空です。つまり、分離レベルに必須の制限はありません。これを設定するには、PD に`location-labels`設定し、 `isolation-level`の値が`location-labels`の名前のいずれかであることを確認する必要があります。

## トポロジラベルに基づくPDスケジュール {#pd-schedules-based-on-topology-label}

PD はラベルレイヤーに従ってレプリカをスケジュールし、同じデータの異なるレプリカが可能な限り分散されるようにします。

前のセクションのトポロジを例に挙げます。

クラスターレプリカの数が 3 ( `max-replicas=3` ) であると仮定します。合計 3 つのゾーンがあるため、PD は各リージョンの 3 つのレプリカがそれぞれ z1、z2、z3 に配置されるようにしています。このようにして、1 つのゾーンに障害が発生しても TiDB クラスターは引き続き利用できます。

次に、クラスターレプリカの数が 5 ( `max-replicas=5` ) であると仮定します。合計で 3 つのゾーンしかないため、PD はゾーンレベルで各レプリカの分離を保証することはできません。この状況では、PD スケジューラはホストレベルでレプリカの分離を保証します。つまり、リージョンの複数のレプリカが同じゾーンに分散されている可能性がありますが、同じホスト上には分散されていない可能性があります。

5 レプリカ構成の場合、z3 に障害が発生するか、z3 全体が分離され、一定期間 ( `max-store-down-time`で制御) 後に回復できない場合、PD はスケジュールによって 5 つのレプリカを構成します。この時点では、使用可能なホストは 4 つだけです。つまり、ホスト レベルの分離は保証されず、複数のレプリカが同じホストにスケジュールされる可能性があります。ただし、 `isolation-level`値が空のままではなく`zone`に設定されている場合、これはリージョンレプリカの最小の物理的分離要件を指定します。つまり、PD は、同じリージョンのレプリカが異なるゾーンに分散していることを保証します。この分離制限に従うことで複数のレプリカの`max-replicas`の要件が満たされない場合でも、PD は対応するスケジュールを実行しません。

`isolation-level`設定が`zone`に設定されている場合、これは物理レベルでのリージョンレプリカの最小分離要件を指定します。この場合、PD は常に同じリージョンのレプリカが異なるゾーンに分散されることを保証します。この分離制限に従うことで`max-replicas`のマルチレプリカ要件が満たされない場合でも、PD はそれに応じてスケジュールを設定しません。3 つのデータ ゾーン (z1、z2、z3) に分散された TiKV クラスターを例にとると、各リージョンに 3 つのレプリカが必要な場合、PD は同じリージョンの 3 つのレプリカをそれぞれこれらの 3 つのデータ ゾーンに分散します。z1 で停電が発生し、一定時間 (デフォルトでは 30 分、 [`max-store-down-time`](/pd-configuration-file.md#max-store-down-time)によって制御) が経過しても回復できない場合、PD は z1 のリージョンレプリカが使用できなくなったと判断します。ただし、 `isolation-level`が`zone`に設定されているため、PD は、同じリージョンの異なるレプリカが同じデータ ゾーンにスケジュールされないことを厳密に保証する必要があります。 z2 と z3 の両方にすでにレプリカがあるため、現時点でレプリカが 2 つしかない場合でも、PD は最小分離レベル制限`isolation-level`の下ではスケジュールを実行しません。

同様に、 `isolation-level` `rack`に設定すると、同じデータセンター内の異なるラックに最小分離レベルが適用されます。この構成では、可能であれば、まずゾーンレイヤーでの分離が保証されます。ゾーン レベルでの分離を保証できない場合、PD は同じゾーン内の同じラックに異なるレプリカをスケジュールしないようにします。 `isolation-level`を`host`に設定した場合も、同様にスケジュールが機能し、PD は最初にラックの分離レベルを保証し、次にホストのレベルを保証しています。

要約すると、PD は現在のトポロジに応じてクラスターの災害復旧を最大化します。したがって、一定レベルの災害復旧を実現したい場合は、トポロジに応じて異なるサイトに`max-replicas`台以上のマシンを展開します。TiDB は、さまざまなシナリオに応じてデータのトポロジ分離レベルをより柔軟に制御できるように、 `isolation-level`などの必須構成項目も提供します。
