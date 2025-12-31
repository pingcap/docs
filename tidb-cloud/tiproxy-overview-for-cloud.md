---
title: Overview of TiProxy for TiDB Cloud
summary: TiDB Cloud用の TiProxy の使用シナリオについて説明します。
---

# TiDB Cloud向け TiProxy の概要 {#overview-of-tiproxy-for-tidb-cloud}

TiProxyはPingCAPの公式プロキシコンポーネントです。クライアントとTiDBサーバーの間に配置され、負荷分散、接続の持続性、その他のTiDB機能を提供します。

詳細については[TiProxy の概要](https://docs.pingcap.com/tidb/stable/tiproxy-overview)参照してください。

> **注記：**
>
> TiProxy はベータ版であり、現在は AWS にデプロイされたTiDB Cloud Dedicated クラスターでのみ利用できます。

## シナリオ {#scenarios}

TiProxy は次のシナリオに適しています。

-   接続の持続性：TiDBサーバーがスケールイン、ローリングアップグレード、またはローリングリスタートを実行すると、クライアント接続が切断され、エラーが発生します。クライアントに冪等なエラーリトライメカニズムがない場合、手動でエラーを確認して修正する必要があり、運用オーバーヘッドが大幅に増加します。TiProxyはクライアント接続を維持できるため、クライアントはエラーを報告しません。
-   頻繁なスケールインとスケールアウト：アプリケーションのワークロードは定期的に変化する可能性があります。コスト削減のため、クラウドにTiDBを導入し、ワークロードに応じてTiDBサーバーを自動的にスケールインおよびスケールアウトすることができます。ただし、スケールインはクライアントの接続を切断する可能性があり、スケールアウトは負荷の不均衡を引き起こす可能性があります。TiProxyはクライアントとの接続を維持し、負荷分散を実現します。
-   CPU負荷の不均衡：バックグラウンドタスクが大量のCPUリソースを消費したり、接続間のワークロードが大きく変動してCPU負荷の不均衡が生じたりした場合、TiProxyはCPU使用率に基づいて接続を移行することで負荷分散を実現します。詳細については、 [CPUベースの負荷分散](https://docs.pingcap.com/tidb/stable/tiproxy-load-balance#cpu-based-load-balancing)参照してください。

その他のシナリオについては、 [TiProxy ユーザーシナリオ](https://docs.pingcap.com/tidb/stable/tiproxy-overview#user-scenarios)参照してください。

## 制限事項 {#limitations}

TiProxy は次のシナリオではクライアント接続を維持できません。

-   AWS EKS、Azure AKS、Google Cloud GKE、または Alibaba Cloud ACK のアップグレード。
-   TiProxy を無効化、スケールイン、アップグレード、または再起動します。
-   単一のステートメントまたはトランザクションが20秒以上実行された場合。アプリケーションでより長いタイムアウトが必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

その他のシナリオについては、 [TiProxy の制限](https://docs.pingcap.com/tidb/stable/tiproxy-overview#limitations)参照してください。

## 請求する {#billing}

TiProxy では、次の 2 種類のコストが発生します。

-   ノードコスト。詳細については、 [ノードコスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)参照してください。
-   データ転送コスト。詳細については、 [データ転送コスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost)参照してください。TiProxy は、同じアベイラビリティゾーン (AZ) 内の TiDB ノードへのトラフィックルーティングを優先します。ただし、TiDB のワークロードが不均一な場合は、他の AZ にもトラフィックがルーティングされるため、追加のデータ転送コストが発生する可能性があります。

TiProxyの請求書は**「請求」**ページでご確認いただけます。詳しくは[TiProxyの請求書をビュー](/tidb-cloud/tiproxy-management.md#view-tiproxy-bills)ご覧ください。

## SLAの影響 {#sla-impact}

TiProxy は SLA に影響を与えません。
