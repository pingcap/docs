---
title: Overview of TiProxy for TiDB Cloud
summary: TiDB Cloud向け TiProxy の利用シナリオについて学びましょう。
---

# TiDB Cloud向けTiProxyの概要 {#overview-of-tiproxy-for-tidb-cloud}

TiProxyはPingCAPの公式プロキシコンポーネントです。クライアントとTiDBサーバーの間に配置され、TiDBの負荷分散、接続の維持、その他の機能を提供します。

詳細については、 [TiProxyの概要](https://docs.pingcap.com/tidb/stable/tiproxy-overview)をご覧ください。

> **注記：**
>
> TiProxyは現在、AWS上にデプロイされたTiDB Cloud Dedicatedクラスターでのみ利用可能です。

## シナリオ {#scenarios}

TiProxyは、以下のシナリオに適しています。

-   接続の維持：TiDBサーバーがスケールイン、ローリングアップグレード、またはローリング再起動を実行すると、クライアント接続が切断され、エラーが発生します。クライアントに冪等なエラー再試行メカニズムがない場合、エラーを手動で確認して修正する必要があり、運用上のオーバーヘッドが大幅に増加します。TiProxyはクライアント接続を維持できるため、クライアントはエラーを報告しません。
-   頻繁なスケールインとスケールアウト：アプリケーションのワークロードは定期的に変化する可能性があります。コストを削減するために、TiDBをクラウドにデプロイし、ワークロードに応じてTiDBサーバーを自動的にスケールインおよびスケールアウトすることができます。ただし、スケールインによってクライアントが切断される可能性があり、スケールアウトによって負荷が不均衡になる可能性があります。TiProxyはクライアント接続を維持し、負荷分散を実現できます。
-   CPU負荷の不均衡：バックグラウンドタスクが大量のCPUリソースを消費したり、接続間のワークロードが大きく変動してCPU負荷が不均衡になった場合、TiProxyはCPU使用率に基づいて接続を移行して負荷分散を実現できます。詳細については、 [CPUベースの負荷分散](https://docs.pingcap.com/tidb/stable/tiproxy-load-balance#cpu-based-load-balancing)参照してください。

その他のシナリオについては、 [TiProxyのユーザーシナリオ](https://docs.pingcap.com/tidb/stable/tiproxy-overview#user-scenarios)を参照してください。

## 制限事項 {#limitations}

TiProxyは、以下のシナリオではクライアント接続を維持できません。

-   AWS EKS、Azure AKS、Google Cloud GKE、またはAlibaba Cloud ACKのアップグレード。
-   TiProxyの無効化、スケールイン、アップグレード、または再起動。
-   単一のステートメントまたはトランザクションの実行時間が20秒を超える場合。アプリケーションでより長いタイムアウトが必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

その他のシナリオについては、 [TiProxyの制限事項](https://docs.pingcap.com/tidb/stable/tiproxy-overview#limitations)を参照してください。

## 請求する {#billing}

TiProxyでは、2種類のコストが導入されています。

-   ノードのコスト。詳細については、 [ノードコスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)を参照してください。
-   データ転送コスト。詳細については、 [データ転送コスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost)を参照してください。TiProxy は、同じアベイラビリティゾーン (AZ) 内の TiDB ノードへのトラフィックルーティングを優先します。ただし、TiDB のワークロードが不均一な場合は、他の AZ にもトラフィックをルーティングするため、追加のデータ転送コストが発生する可能性があります。

TiProxy の請求書は、 **[請求]**ページで確認できます。詳細については、 [TiProxyの請求書をビュー](/tidb-cloud/tiproxy-management.md#view-tiproxy-bills)参照してください。

## SLAへの影響 {#sla-impact}

TiProxyはSLAに影響を与えません。
