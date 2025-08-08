---
title: PD Microservices
summary: PD のマイクロサービス モードを有効にしてサービス品質を向上させる方法を学習します。
---

# PDマイクロサービス {#pd-microservices}

バージョン8.0.0以降、PDはマイクロサービスモードをサポートします。このモードでは、PDのタイムスタンプ割り当て機能とクラスタスケジューリング関数が、独立してデプロイされた以下の2つのマイクロサービスに分割されます。これにより、これらの2つの関数はPDのルーティング機能から分離され、PDはメタデータのルーティングサービスに集中できるようになります。

-   `tso`マイクロサービス: クラスター全体に対して単調に増加するタイムスタンプ割り当てを提供します。
-   `scheduling`マイクロサービス: 負荷分散、ホットスポット処理、レプリカ修復、レプリカ配置など、クラスター全体のスケジュール関数を提供します。

各マイクロサービスは独立したプロセスとしてデプロイされます。マイクロサービスに複数のレプリカを設定すると、マイクロサービスはプライマリ/セカンダリフォールトトレラントモードを自動的に実装し、サービスの高可用性と信頼性を確保します。

> **警告：**
>
> 現在、PDマイクロサービス機能は実験的です。本番環境でのご利用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/tikv/pd/issues)報告を行ってください。

## 使用シナリオ {#usage-scenarios}

PDマイクロサービスは通常、PDにおけるパフォーマンスのボトルネックを解消し、PDサービスの品質を向上させるために使用されます。この機能により、以下の問題を回避できます。

-   PD クラスターの過剰な圧力により、TSO 割り当てにおけるロングテールのレイテンシーまたはジッターが発生する
-   スケジューリングモジュールの障害により、クラスタ全体のサービスが利用できなくなります
-   PDのみに起因するボトルネックの問題

さらに、スケジューリング モジュールが変更された場合、PD を再起動せずに`scheduling`マイクロサービスを個別に更新できるため、クラスターのサービス全体への影響を回避できます。

> **注記：**
>
> クラスターのパフォーマンスボトルネックの原因が PD ではない場合は、マイクロサービスを有効にする必要はありません。マイクロサービスを使用するとコンポーネントの数が増え、運用コストが上昇するからです。

## 制限 {#restrictions}

-   現在、マイクロサービス`tso`動的な起動と停止をサポートしていません。マイクロサービス`tso`有効化または無効化した後、変更を有効にするには PD クラスターを再起動する必要があります。
-   TiDBコンポーネントのみがサービス検出を通じて`tso`マイクロサービスへの直接接続をサポートしますが、他のコンポーネントはタイムスタンプを取得するために PD を通じて`tso`マイクロサービスにリクエストを転送する必要があります。
-   マイクロサービスは[データレプリケーション自動同期（DR自動同期）](/two-data-centers-in-one-city-deployment.md)機能と互換性がありません。
-   マイクロサービスは TiDB システム変数[`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)と互換性がありません。
-   [休止状態領域](/tikv-configuration-file.md#hibernate-regions)クラスター内に存在する可能性があるため、 `scheduling`マイクロサービスのプライマリおよびセカンダリの切り替え中に、冗長なスケジュールを回避するために、クラスターのスケジュール機能が一定期間 (最大[`peer-stale-state-check-interval`](/tikv-configuration-file.md#peer-stale-state-check-interval) 、デフォルトでは 5 分) 使用できなくなる可能性があります。

## 使用法 {#usage}

PD マイクロサービスは[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/)または[TiUP](/tiup/tiup-overview.md)使用してデプロイできます。

<SimpleTab>
<div label="TiDB Operator">

TiDB Operatorを使用してデプロイされた TiDB クラスターの場合は、次のドキュメントに従って PD マイクロサービスをデプロイおよび構成できます。

-   [PDマイクロサービスのデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#enable-pd-microservices)
-   [PDマイクロサービスを構成する](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#configure-pd-microservices)
-   [PDマイクロサービスの変更](https://docs.pingcap.com/tidb-in-kubernetes/stable/modify-tidb-configuration#modify-pd-microservice-configuration)
-   [PDマイクロサービスコンポーネントのスケール](https://docs.pingcap.com/tidb-in-kubernetes/stable/scale-a-tidb-cluster#scale-pd-microservice-components)

</div>
<div label="TiUP">

TiUPを使用してデプロイされた TiDB クラスターの場合、次のドキュメントに従って PD マイクロサービスをデプロイおよび構成できます。

-   [PDマイクロサービスのデプロイ](/pd-microservices-deployment-topology.md)
-   [PDマイクロサービスノードのスケール](/scale-microservices-using-tiup.md)
-   `tso`マイクロサービスを構成する
    -   [設定ファイルで設定する](/tso-configuration-file.md)
    -   [コマンドラインフラグで設定する](/command-line-flags-for-tso-configuration.md)
-   `scheduling`マイクロサービスを構成する
    -   [設定ファイルで設定する](/scheduling-configuration-file.md)
    -   [コマンドラインフラグで設定する](/command-line-flags-for-scheduling-configuration.md)

</div>
<div label="TiUP Playground">

TiUP Playground を使用して TiDB ローカル クラスターに PD マイクロサービスをデプロイおよび構成するには、次のドキュメントを参照してください。

-   [PDマイクロサービスのデプロイ](/tiup/tiup-playground.md#deploy-pd-microservices)

</div>
</SimpleTab>

## 注記 {#notes}

PD マイクロサービスをデプロイして使用する場合、次の点に注意してください。

-   マイクロサービスを有効にしてクラスターのPDを再起動すると、PDはクラスターへのTSOの割り当てを停止します。そのため、マイクロサービスを有効にする際には、クラスターに`tso`マイクロサービスをデプロイする必要があります。
-   `scheduling`マイクロサービスがクラスターにデプロイされている場合、クラスターのスケジューリング機能は`scheduling`マイクロサービスによって提供されます。5 `scheduling`マイクロサービスがデプロイされていない場合でも、クラスターのスケジューリング機能はPDによって提供されます。
-   `scheduling`マイクロサービスは動的スイッチングをサポートしており、これはデフォルトで有効になっています（ `enable-scheduling-fallback`デフォルトで`true`に設定されています）。7 `scheduling`サービスのプロセスが終了した場合、PD はデフォルトでクラスターのスケジューリングサービスを継続します。

    `scheduling`マイクロサービスと PD のバイナリバージョンが異なる場合、スケジューリングロジックの変更を防ぐため、 `pd-ctl config set enable-scheduling-fallback false`実行して`scheduling`マイクロサービスの動的切り替え機能を無効化できます。この機能を無効化すると、 `scheduling`マイクロサービスのプロセスが終了しても PD はスケジューリングサービスを引き継ぎません。つまり、 `scheduling`マイクロサービスが再起動されるまで、クラスターのスケジューリングサービスは利用できなくなります。

## ツールの互換性 {#tool-compatibility}

マイクロサービスは、データのインポート、エクスポート、その他のレプリケーション ツールの通常の使用には影響しません。

## よくある質問 {#faqs}

-   PD がパフォーマンスのボトルネックになるかどうかをどのように判断すればよいですか?

    クラスターが正常な状態であれば、Grafana PDパネルで監視メトリクスを確認できます。1 `TiDB - PD server TSO handle time`メトリクスでレイテンシーが著しく増加している場合、または`Heartbeat - TiKV side heartbeat statistics`メトリクスで保留中の項目が多数表示されている場合は、PDがパフォーマンスのボトルネックになっていることを示しています。
