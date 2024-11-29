---
title: PD Microservices
summary: PD のマイクロサービス モードを有効にしてサービス品質を向上させる方法を学習します。
---

# PD マイクロサービス {#pd-microservices}

v8.0.0 以降、PD はマイクロサービス モードをサポートします。このモードでは、PD のタイムスタンプ割り当て機能とクラスター スケジューリング関数が、独立してデプロイされた次の 2 つのマイクロサービスに分割されます。これにより、これら 2 つの関数がPD のルーティング機能から分離され、PD はメタデータのルーティング サービスに集中できるようになります。

-   `tso`マイクロサービス: クラスター全体に対して単調に増加するタイムスタンプ割り当てを提供します。
-   `scheduling`マイクロサービス: 負荷分散、ホットスポット処理、レプリカ修復、レプリカ配置など、クラスター全体のスケジュール関数を提供します。

各マイクロサービスは独立したプロセスとしてデプロイされます。マイクロサービスに複数のレプリカを構成すると、マイクロサービスはプライマリ/セカンダリ フォールト トレラント モードを自動的に実装し、サービスの高可用性と信頼性を確保します。

> **警告：**
>
> 現在、PD マイクロサービス機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/tikv/pd/issues)報告できます。

## 使用シナリオ {#usage-scenarios}

PD マイクロサービスは通常、PD のパフォーマンスのボトルネックを解決し、PD サービスの品質を向上させるために使用されます。この機能を使用すると、次の問題を回避できます。

-   PD クラスターの過度の圧力による TSO 割り当てのロングテールレイテンシーまたはジッター
-   スケジューリングモジュールの障害により、クラスタ全体のサービスが利用不可になる
-   PDのみに起因するボトルネックの問題

さらに、スケジューリング モジュールが変更された場合、PD を再起動せずに`scheduling`マイクロサービスを個別に更新できるため、クラスターの全体的なサービスへの影響を回避できます。

> **注記：**
>
> クラスターのパフォーマンスのボトルネックの原因が PD でない場合は、マイクロサービスを有効にする必要はありません。マイクロサービスを使用するとコンポーネントの数が増え、運用コストが上昇するためです。

## 制限 {#restrictions}

-   現在、マイクロサービス`tso`動的な開始と停止をサポートしていません。マイクロサービス`tso`を有効または無効にした後、変更を有効にするには PD クラスターを再起動する必要があります。
-   TiDBコンポーネントのみがサービス検出を通じて`tso`マイクロサービスへの直接接続をサポートしますが、他のコンポーネントはタイムスタンプを取得するために PD を通じて`tso`マイクロサービスにリクエストを転送する必要があります。
-   マイクロサービスは[データ レプリケーション自動同期 (DR 自動同期)](/two-data-centers-in-one-city-deployment.md)機能と互換性がありません。
-   マイクロサービスは TiDB システム変数[`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)と互換性がありません。
-   [休止状態領域](/tikv-configuration-file.md#hibernate-regions)クラスター内に存在する可能性があるため、 `scheduling`マイクロサービスのプライマリとセカンダリの切り替え中は、冗長なスケジューリングを回避するために、クラスターのスケジューリング機能が一定期間 (最大[`peer-stale-state-check-interval`](/tikv-configuration-file.md#peer-stale-state-check-interval) 、デフォルトでは 5 分) 使用できなくなる可能性があります。

## 使用法 {#usage}

現在、PD マイクロサービスはTiDB Operator を使用してデプロイできます。

TiDB Operator の使用に関する詳細については、次のドキュメントを参照してください。

-   [PDマイクロサービスのデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/configure-a-tidb-cluster#enable-pd-microservices)
-   [PDマイクロサービスを構成する](https://docs.pingcap.com/tidb-in-kubernetes/dev/configure-a-tidb-cluster#configure-pd-microservices)
-   [PDマイクロサービスの変更](https://docs.pingcap.com/tidb-in-kubernetes/dev/modify-tidb-configuration#modify-pd-microservice-configuration)
-   [PDマイクロサービスコンポーネントのスケール](https://docs.pingcap.com/tidb-in-kubernetes/dev/scale-a-tidb-cluster#scale-pd-microservice-components)

PD マイクロサービスをデプロイして使用するときは、次の点に注意してください。

-   マイクロサービスを有効にしてクラスターの PD を再起動すると、PD はクラスターへの TSO の割り当てを停止します。したがって、マイクロサービスを有効にするときは、クラスターに`tso`マイクロサービスをデプロイする必要があります。
-   `scheduling`マイクロサービスがクラスターにデプロイされている場合、クラスターのスケジューリング機能は`scheduling`のマイクロサービスによって提供されます。5 `scheduling`のマイクロサービスがデプロイされていない場合でも、クラスターのスケジューリング機能は PD によって提供されます。
-   `scheduling`マイクロサービスは動的切り替えをサポートしており、デフォルトで有効になっています ( `enable-scheduling-fallback`デフォルトは`true`です)。 `scheduling`マイクロサービスのプロセスが終了した場合、PD はデフォルトでクラスターのスケジューリング サービスを引き続き提供します。

    `scheduling`マイクロサービスと PD のバイナリ バージョンが異なる場合、スケジューリング ロジックの変更を防ぐために、 `pd-ctl config set enable-scheduling-fallback false`実行して`scheduling`マイクロサービスの動的切り替え機能を無効にできます。この機能を無効にすると、 `scheduling`マイクロサービスのプロセスが終了しても PD はスケジューリング サービスを引き継ぎません。つまり、 `scheduling`マイクロサービスが再起動されるまで、クラスターのスケジューリング サービスは利用できなくなります。

## ツールの互換性 {#tool-compatibility}

マイクロサービスは、データのインポート、エクスポート、およびその他のレプリケーション ツールの通常の使用には影響しません。

## よくある質問 {#faqs}

-   PD がパフォーマンスのボトルネックになるかどうかをどのように判断できますか?

    クラスターが正常な状態にある場合は、Grafana PD パネルで監視メトリックを確認できます。メトリック`TiDB - PD server TSO handle time`にレイテンシーの顕著な増加が見られる場合、またはメトリック`Heartbeat - TiKV side heartbeat statistics`に保留中の項目が多数見られる場合、PD がパフォーマンスのボトルネックになっていることを示しています。
