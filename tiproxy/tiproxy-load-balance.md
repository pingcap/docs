---
title: TiProxy Load Balancing Policies
summary: TiProxy の負荷分散ポリシーとその適用可能なシナリオを紹介します。
---

# TiProxy 負荷分散ポリシー {#tiproxy-load-balancing-policies}

TiProxy v1.0.0 は、TiDB サーバーに対してステータスベースおよび接続数ベースの負荷分散ポリシーのみをサポートしています。v1.1.0 以降では、ラベルベース、ヘルスベース、メモリベース、CPU ベース、ロケーションベースの 5 つの負荷分散ポリシーが追加されています。

デフォルトでは、TiProxy は次の優先順位でこれらのポリシーを適用します。

1.  ステータスベースの負荷分散: TiDBサーバーがシャットダウンすると、TiProxy はその TiDBサーバーからオンラインの TiDBサーバーに接続を移行します。
2.  ラベルベースの負荷分散: TiProxy は、TiProxy インスタンスと同じラベルを共有する TiDB サーバーへのルーティング要求を優先し、コンピューティングレイヤーでのリソースの分離を可能にします。
3.  ヘルスベースの負荷分散: TiDBサーバーのヘルスが異常な場合、TiProxy はその TiDBサーバーから正常な TiDBサーバーに接続を移行します。
4.  メモリベースの負荷分散: TiDBサーバーがメモリ不足 (OOM) になる危険がある場合、TiProxy はその TiDBサーバーからメモリ使用量の少ない TiDBサーバーに接続を移行します。
5.  CPU ベースの負荷分散: TiDBサーバーの CPU 使用率が他の TiDB サーバーよりもはるかに高い場合、TiProxy はその TiDBサーバーから CPU 使用率の低い TiDBサーバーに接続を移行します。
6.  ロケーションベースの負荷分散: TiProxy は、TiProxy に地理的に最も近い TiDBサーバーへのルーティング要求を優先します。
7.  接続数ベースの負荷分散: TiDBサーバーの接続数が他の TiDB サーバーよりも大幅に多い場合、TiProxy はその TiDBサーバーから接続数の少ない TiDBサーバーに接続を移行します。

負荷分散ポリシーの優先順位を調整するには、 [負荷分散ポリシーを構成する](#configure-load-balancing-policies)参照してください。

## ステータスベースの負荷分散 {#status-based-load-balancing}

TiProxy は、SQL ポートとステータス ポートを使用して、TiDBサーバーがオフラインになっているか、シャットダウンしているかどうかを定期的に確認します。

## ラベルベースの負荷分散 {#label-based-load-balancing}

ラベルベースの負荷分散は、TiProxyと同じラベルを持つTiDBサーバーへのルーティング接続を優先し、コンピューティングレイヤーでのリソース分離を可能にします。このポリシーはデフォルトで無効になっており、ワークロードでコンピューティングリソースの分離が必要な場合にのみ有効にする必要があります。

ラベルベースの負荷分散を有効にするには、次の操作を行う必要があります。

-   一致するラベル名を[`balance.label-name`](/tiproxy/tiproxy-configuration.md#label-name)で指定します。
-   TiProxy で[`labels`](/tiproxy/tiproxy-configuration.md#labels)構成項目を構成します。
-   TiDB サーバーで[`labels`](/tidb-configuration-file.md#labels)構成項目を構成します。

設定後、TiProxy は`balance.label-name`で指定されたラベル名を使用して、一致するラベル値を持つ TiDB サーバーへの接続をルーティングします。

トランザクションとBIの両方のワークロードを処理するアプリケーションを考えてみましょう。これらのワークロードが互いに干渉しないようにするには、クラスターを次のように構成します。

1.  TiProxy で[`balance.label-name`](/tiproxy/tiproxy-configuration.md#label-name)を`"app"`に設定すると、TiDB サーバーはラベル名`"app"`によって照合され、接続は一致するラベル値を持つ TiDB サーバーにルーティングされます。
2.  少なくとも 2 つの TiProxy インスタンスをデプロイ。トランザクション ワークロードに使用する TiProxy インスタンスを[`labels`](/tiproxy/tiproxy-configuration.md#labels)で`{"app": "Order"}`に設定し、BI ワークロードに使用するインスタンスを[`labels`](/tiproxy/tiproxy-configuration.md#labels)で`{"app": "BI"}`に設定します。
3.  オプション：高可用性を実現するには、少なくとも4つのTiProxyインスタンスを導入し、ワークロードごとに異なる仮想IPアドレスを設定します。例えば、トランザクションワークロード用のTiProxyインスタンス2つを仮想IP `10.0.1.10/24`に設定し、BIワークロード用のインスタンス2つを仮想IP `10.0.1.20/24`に設定します。この機能を使用するには、TiProxy v1.3.1以降が必要です。
4.  TiDB インスタンスを 2 つのグループに分割し、それぞれ[`labels`](/tidb-configuration-file.md#labels)設定します。一方のグループに`"app": "Order"`ラベルを追加し、もう一方のグループに`"app": "BI"`ラベルを追加します。
5.  オプション:storageレイヤーの分離の場合は、 [配置ルール](/configure-placement-rules.md)または[リソース管理](/tidb-resource-control-ru-groups.md)構成します。
6.  仮想IPが設定されている場合、トランザクションクライアントとBIクライアントはそれぞれ2つの仮想IPアドレスに接続します。仮想IPが設定されていない場合、トランザクションクライアントとBIクライアントはそれぞれ2つのTiProxyアドレスに接続します。

<img src="https://docs-download.pingcap.com/media/images/docs/tiproxy/tiproxy-balance-label-v2.png" alt="ラベルベースの負荷分散" width="600" />

このトポロジの構成例:

```yaml
component_versions:
  tiproxy: "v1.3.1"
server_configs:
  tiproxy:
    balance.label-name: "app"
  tidb:
    graceful-wait-before-shutdown: 30
tiproxy_servers:
  - host: tiproxy-host-1
    config:
      labels: {"app": "Order"}
      ha.virtual-ip: "10.0.1.10/24"
      ha.interface: "eth0"
  - host: tiproxy-host-2
    config:
      labels: {"app": "Order"}
      ha.virtual-ip: "10.0.1.10/24"
      ha.interface: "eth0"
  - host: tiproxy-host-3
    config:
      labels: {"app": "BI"}
      ha.virtual-ip: "10.0.1.20/24"
      ha.interface: "eth0"
  - host: tiproxy-host-4
    config:
      labels: {"app": "BI"}
      ha.virtual-ip: "10.0.1.20/24"
      ha.interface: "eth0"
tidb_servers:
  - host: tidb-host-1
    config:
      labels: {"app": "Order"}
  - host: tidb-host-2
    config:
      labels: {"app": "Order"}
  - host: tidb-host-3
    config:
      labels: {"app": "BI"}
  - host: tidb-host-4
    config:
      labels: {"app": "BI"}
tikv_servers:
  - host: tikv-host-1
  - host: tikv-host-2
  - host: tikv-host-3
pd_servers:
  - host: pd-host-1
  - host: pd-host-2
  - host: pd-host-3
```

## ヘルスベースの負荷分散 {#health-based-load-balancing}

TiProxyは、TiDBサーバーの健全性を判断します。他のサーバーが正常なのに、あるTiDBサーバーの健全性に異常がある場合、TiProxyはそのサーバーから正常なTiDBサーバーへ接続を移行し、自動フェイルオーバーを実現します。

このポリシーは、次のシナリオに適しています。

-   TiDBサーバーはTiKV へのリクエストの送信に頻繁に失敗し、SQL 実行の失敗が頻繁に発生します。
-   TiDBサーバーはPD へのリクエストの送信に頻繁に失敗し、SQL 実行の失敗が頻繁に発生します。

## メモリベースの負荷分散 {#memory-based-load-balancing}

TiProxy は TiDB サーバのメモリ使用量を照会します。TiDBサーバーのメモリ使用量が急増したり、高いレベルに達したりした場合、TiProxy はそのサーバーからメモリ使用量の低い TiDBサーバーに接続を移行し、OOM による不要な接続切断を防止します。TiProxy は、TiDB サーバ間でメモリ使用量が同一であることを保証するものではありません。このポリシーは、TiDBサーバーがOOM の危険にさらされている場合にのみ有効になります。

TiDBサーバーがOOMの危険にさらされている場合、TiProxyはそのサーバーからすべての接続を移行しようとします。通常、OOMの原因が暴走クエリである場合、進行中の暴走クエリは別のTiDBサーバーに移行されて再実行されることはありません。これは、これらの接続はトランザクションが完了した後にのみ移行できるためです。

このポリシーには次の制限があります。

-   TiDBサーバーのメモリ使用量が急激に増加し、30 秒以内に OOM に達した場合、TiProxy は OOM のリスクを時間内に検出できず、接続が終了する可能性があります。
-   TiProxyは、クライアント接続を切断することなく維持することを目的としており、TiDBサーバーのメモリ使用量を削減してOOMを回避することを目的としているわけではありません。そのため、TiDBサーバーは依然としてOOMに遭遇する可能性があります。
-   このポリシーはTiDBサーバーv8.0.0以降のバージョンにのみ適用されます。それより前のバージョンのTiDBサーバーでは、このポリシーは適用されません。

## CPUベースの負荷分散 {#cpu-based-load-balancing}

TiProxyはTiDBサーバーのCPU使用率を照会し、CPU使用率の高いTiDBサーバーから使用率の低いサーバーへ接続を移行することで、全体的なレイテンシーを削減します。TiProxyはTiDBサーバー間でCPU使用率が同一であることを保証するものではありませんが、CPU使用率の差が最小限に抑えられるようにします。

このポリシーは、次のシナリオに適しています。

-   バックグラウンド タスク ( `ANALYZE`など) が大量の CPU リソースを消費すると、これらのタスクを実行する TiDB サーバーの CPU 使用率が高くなります。
-   異なる接続でのワークロードが大きく異なる場合、各 TiDBサーバーの接続数が似ていても、CPU 使用率が大幅に異なる可能性があります。
-   クラスター内の TiDB サーバーの CPU リソース構成が異なる場合、接続数が均衡していても、実際の CPU 使用率は不均衡になる可能性があります。

## ロケーションベースの負荷分散 {#location-based-load-balancing}

TiProxy は、TiProxy サーバーと TiDB サーバーの場所に基づいて、地理的に近い TiDB サーバーへのルーティング接続を優先します。

このポリシーは、次のシナリオに適しています。

-   TiDB クラスターがクラウド内のアベイラビリティ ゾーン全体に展開されている場合、TiProxy と TiDB サーバー間のアベイラビリティ ゾーン間のトラフィック コストを削減するために、TiProxy は同じアベイラビリティ ゾーン内の TiDB サーバーへのルーティング要求を優先します。
-   TiDB クラスターがデータ センター全体に展開されている場合、TiProxy と TiDB サーバー間のネットワークレイテンシーを削減するために、TiProxy は同じデータ センター内の TiDB サーバーへのルーティング要求を優先します。

デフォルトでは、このポリシーの優先度は、ヘルスベース、メモリベース、CPUベースの負荷分散ポリシーよりも低くなっています。優先度を[`policy`](/tiproxy/tiproxy-configuration.md#policy)から`location`に設定することで、優先度を上げることができます。可用性とパフォーマンスを維持するには、少なくとも3台のTiDBサーバーを同じ場所に配置することを推奨します。

TiProxyは、ラベル`zone`に基づいて自身とTiDBサーバの場所を決定します。以下の設定項目を設定する必要があります。

-   TiDBサーバーの設定項目[`labels`](/tidb-configuration-file.md#labels)で、 `zone`現在のアベイラビリティゾーンに設定します。設定の詳細については、 [TiDBのラベルを構成する](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)参照してください。
-   TiProxy の[`labels`](/tiproxy/tiproxy-configuration.md#labels)の構成項目で、 `zone`現在の可用性ゾーンに設定します。

TiDB Operatorを使用してデプロイされたクラスターについては、 [データの高可用性](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data)参照してください。

以下はクラスタ構成の例です。

```yaml
component_versions:
  tiproxy: "v1.1.0"
server_configs:
  tidb:
    graceful-wait-before-shutdown: 30
tiproxy_servers:
  - host: tiproxy-host-1
    config:
      labels:
        zone: east
  - host: tiproxy-host-2
    config:
      labels:
        zone: west
tidb_servers:
  - host: tidb-host-1
    config:
      labels:
        zone: east
  - host: tidb-host-2
    config:
      labels:
        zone: west
tikv_servers:
  - host: tikv-host-1
  - host: tikv-host-2
  - host: tikv-host-3
pd_servers:
  - host: pd-host-1
  - host: pd-host-2
  - host: pd-host-3
```

上記の構成では、 `tiproxy-host-1`の`zone`設定が`tidb-host-1`と同じであるため、 `tiproxy-host-1`の TiProxy インスタンスは`tidb-host-1` TiDBサーバーへのルーティング要求を優先します。同様に、 `tiproxy-host-2`の TiProxy インスタンスは`tidb-host-2`の TiDBサーバーへのルーティング要求を優先します。

## 接続数ベースの負荷分散 {#connection-count-based-load-balancing}

TiProxyは、接続数の多いTiDBサーバーから接続数の少ないサーバーへ接続を移行します。このポリシーは変更できず、優先度は最も低くなります。

通常、TiProxy は CPU 使用率に基づいて TiDB サーバーの負荷を特定します。このポリシーは通常、以下のシナリオで有効になります。

-   TiDB クラスターの起動直後は、すべての TiDB サーバーの CPU 使用率は 0 に近くなります。この場合、このポリシーにより、起動時の負荷の不均衡が防止されます。
-   [CPUベースの負荷分散](#cpu-based-load-balancing)が有効になっていない場合、このポリシーは負荷分散を保証します。

## 負荷分散ポリシーを構成する {#configure-load-balancing-policies}

TiProxy では、 [`policy`](/tiproxy/tiproxy-configuration.md#policy)構成項目を通じて負荷分散ポリシーの組み合わせと優先順位を設定できます。

-   `resource` : リソース優先度ポリシーは、ステータス、ラベル、ヘルス、メモリ、CPU、場所、接続数の優先順位に基づいて負荷分散を実行します。
-   `location` : 場所の優先順位ポリシーは、ステータス、ラベル、場所、正常性、メモリ、CPU、接続数の優先順位に基づいて負荷分散を実行します。
-   `connection` : 最小接続数ポリシーは、ステータス、ラベル、接続数の優先順位に基づいて負荷分散を実行します。

## その他のリソース {#more-resources}

TiProxy の負荷分散ポリシーの詳細については、 [設計書](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-02-01-multi-factor-based-balance.md)参照してください。
