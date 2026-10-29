---
title: TiDB Cloud Built-in Alerting
summary: TiDB Cloudからアラート通知を受け取ることで、 TiDB Cloudリソースを監視する方法を学びましょう。
---

# TiDB Cloudの組み込みアラート機能 {#tidb-cloud-built-in-alerting}

TiDB Cloud を使用すると、アラートの表示、アラートルールの編集、アラート通知の購読を簡単に行うことができます。

このドキュメントでは、これらの操作を実行する方法について説明し、参考としてTiDB Cloudに組み込まれているアラート条件を示します。

> **Note:**
>
> 現在、アラート購読は、[TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) インスタンス、[TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) インスタンス、[TiDB Cloud BYOC](/tidb-cloud/select-cluster-tier.md#byoc) インスタンス、および [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) クラスターで利用できます。

## アラートを確認する {#view-alerts}

<CustomContent plan="essential,dedicated">

TiDB Cloudでは、**Alerts**ページでアクティブなアラートとクローズされたアラートの両方を表示できます。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず対象の組織に切り替えてください。

2. 対象の {{{ .essential }}} インスタンスまたは TiDB Cloud Dedicated クラスターの名前をクリックして、その概要ページに移動します。
3. 左側のナビゲーションペインで **Alerts** をクリックします。
4. **Alerts** ページには、デフォルトでアクティブなアラートが表示されます。各アクティブアラートについて、アラート名、トリガー時刻、継続時間などの情報を確認できます。
5. クローズされたアラートも表示するには、**Status** ドロップダウンリストをクリックし、**Closed** または **All** を選択します。

</CustomContent>

<CustomContent plan="premium,byoc">

TiDB Cloudでは、**Alerts**ページでアクティブなアラートとクローズされたアラートの両方を表示できます。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず対象の組織に切り替えてください。

2. 対象の {{{ .premium }}} または {{{ .byoc }}} インスタンスの名前をクリックして、その概要ページに移動します。
3. 左側のナビゲーションペインで **Alerts** をクリックします。
4. **Alerts** ページには、デフォルトでアクティブなアラートが表示されます。各アクティブアラートについて、アラート名、トリガー時刻、継続時間などの情報を確認できます。
5. クローズされたアラートも表示するには、**Status** ドロップダウンリストをクリックし、**Closed** または **All** を選択します。

</CustomContent>

## アラートルールを編集する {#edit-alert-rules}

TiDB Cloudでは、アラートを無効化または有効化したり、アラートのしきい値を更新したりすることで、アラートルールを編集できます。

1. **Alerts**ページで、 **Edit Rules**をクリックします。
2. 必要に応じてアラートルールを無効化または有効化してください。
3. アラートルールのしきい値を更新するには、 **Edit**をクリックします。

    > **Tip:**
    >
    > 現在、 TiDB Cloudでは、アラートルール編集の機能が限定的に提供されています。一部のアラートルールは編集をサポートしていません。異なるトリガー条件や頻度を構成したい場合、または[PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/)などのダウンストリームサービスでアラートによってアクションを自動的にトリガーしたい場合は、[サードパーティの監視およびアラートとの統合](/tidb-cloud/third-party-monitoring-integrations.md)の使用を検討してください。

## アラート通知を購読する {#subscribe-to-alert-notifications}

TiDB Cloudでは、以下のいずれかの方法でアラート通知を購読できます。

- [メール](/tidb-cloud/monitor-alert-email.md)
- [Slack](/tidb-cloud/monitor-alert-slack.md)
- [Zoom](/tidb-cloud/monitor-alert-zoom.md)
- [Flashduty](/tidb-cloud/monitor-alert-flashduty.md)
- [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md)
- [Webhook](/tidb-cloud/monitor-alert-webhook.md)
- [Lark](/tidb-cloud/monitor-alert-lark.md)

## TiDB Cloudに組み込まれたアラート条件 {#tidb-cloud-built-in-alert-conditions}

以下の表は、TiDB Cloudに組み込まれているアラート条件と、それに対応する推奨アクションを示しています。

> **Note:**
>
> - これらのアラート条件は必ずしも問題が発生していることを意味するものではありませんが、多くの場合、新たな問題が発生する兆候を示しています。したがって、推奨される対策を講じることをお勧めします。
> - TiDB Cloudコンソールでアラートのしきい値を編集できます。
> - 一部のアラートルールはデフォルトで無効になっています。必要に応じて有効にできます。

TiDB Cloudは、そのプランで利用可能な[機能](/tidb-cloud/features.md)に基づいて、 [TiDB Cloudプラン](/tidb-cloud/select-cluster-tier.md)ごとに異なるアラートルールを提供します。

<CustomContent plan="dedicated">

### リソース使用状況アラート {#resource-usage-alerts}

| 条件                                       | 推奨アクション                                                                                                                                           |
| :--------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| Total TiDB node memory utilization across cluster exceeded 70% for 10 minutes | 現在のワークロードにおけるメモリ使用率を削減するために、TiDBのノード数またはノードサイズを増やすことを検討してください。                                                                                    |
| Total TiKV node memory utilization across cluster exceeded 70% for 10 minutes | 現在のワークロードにおけるメモリ使用率を削減するために、TiKVのノード数またはノードサイズを増やすことを検討してください。                                                                                    |
| Total TiFlash node memory utilization across cluster exceeded 70% for 10 minutes | 現在のワークロードにおけるメモリ使用率を低減するために、 TiFlashのノード数またはノードサイズを増やすことを検討してください。                                                                                |
| Total TiDB node CPU utilization exceeded 80% for 10 minutes | 現在のワークロードにおけるCPU使用率を低減するために、TiDBのノード数またはノードサイズを増やすことを検討してください。                                                                                    |
| Total TiKV node CPU utilization exceeded 80% for 10 minutes | 現在のワークロードにおけるCPU使用率を低減するために、TiKVのノード数またはノードサイズを増やすことを検討してください。                                                                                    |
| Total TiFlash node CPU utilization exceeded 80% for 10 minutes | 現在のワークロードにおけるCPU使用率を低減するために、 TiFlashのノード数またはノードサイズを増やすことを検討してください。                                                                                |
| TiKV storage utilization exceeds 80% | ストレージ容量を増やすには、TiKVのノード数またはノードのストレージサイズを増やすことを検討してください。TiKVのストレージ使用率が80%を超えると、レイテンシーの急上昇が発生する可能性があり、使用率が高くなるとリクエストが失敗する場合があります。              |
| TiFlash storage utilization exceeds 80% | TiFlashのストレージ容量を増やすには、ノード数またはノードのストレージサイズを増やすことを検討してください。すべてのTiFlashノードのストレージ使用率が80%に達すると、 TiFlashレプリカを追加するDDL文は永久にハングアップします。         |
| Max memory utilization across TiDB nodes exceeded 70% for 10 minutes | クラスター内に[ホットスポット](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues)がないか確認するか、TiDBのノード数またはノードサイズを増やして、現在のワークロードのメモリ使用率を削減することを検討してください。 |
| Max memory utilization across TiKV nodes exceeded 70% for 10 minutes | クラスター内に[ホットスポット](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues)がないか確認するか、TiKVのノード数またはノードサイズを増やして、現在のワークロードのメモリ使用率を削減することを検討してください。 |
| Max CPU utilization across TiDB nodes exceeded 80% for 10 minutes | クラスター内に[ホットスポット](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues)がないか確認するか、TiDBのノード数またはノードサイズを増やして、現在のワークロードのCPU使用率を下げることを検討してください。  |
| Max CPU utilization across TiKV nodes exceeded 80% for 10 minutes | クラスター内に[ホットスポット](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues)がないか確認するか、TiKVのノード数またはノードサイズを増やして、現在のワークロードのCPU使用率を下げることを検討してください。  |

### データ移行アラート {#data-migration-alerts}

| 条件                                    | 推奨アクション                                                                                                                                                                                                                                                 |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Data migration job met error during data export | エラーを確認し、ヘルプについては[データ移行のトラブルシューティング](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)を参照してください。                                                                                                                  |
| Data migration job met error during data import | エラーを確認し、ヘルプについては[データ移行のトラブルシューティング](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)を参照してください。                                                                                                                  |
| Data migration job met error during incremental migration | エラーを確認し、ヘルプについては[データ移行のトラブルシューティング](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)を参照してください。                                                                                                                  |
| Data migration job has been paused for more than 6 hours during incremental migration | データの増分移行中に、データ移行ジョブが 6時間以上一時停止されました。アップストリームデータベースのbinlogがパージされる可能性があり (データベースのbinlogパージ戦略によって異なります)、増分移行が失敗する可能性があります。ヘルプについては[データ移行のトラブルシューティング](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)を参照してください。 |
| Replication lag is larger than 10 minutes and still increasing for more than 20 minutes | ヘルプについては[データ移行のトラブルシューティング](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)を参照してください。                                                                                                                          |

### TiDB Cloud Dedicatedの変更フィードアラート {#changefeed-alerts-for-tidb-cloud-dedicated}

| 条件                                   | 推奨アクション                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| The changefeed latency exceeds 600 seconds. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。このアラートが発生する原因として、次のようなものがあります。<ul><li>アップストリーム全体のトラフィックが増加し、既存の changefeed のスペックでは処理しきれなくなっている。トラフィックの増加が一時的な場合、トラフィックが正常に戻ると changefeed のレイテンシーは自動的に回復します。トラフィックの増加が継続的な場合は、changefeed をスケールアップする必要があります。</li><li>ダウンストリームまたはネットワークに異常がある。この場合は、まずその異常を解消してください。</li><li>ダウンストリームが RDS の場合、テーブルにインデックスが不足している可能性があり、書き込み性能の低下と高レイテンシーの原因になることがあります。この場合は、アップストリームまたはダウンストリームに必要なインデックスを追加する必要があります。</li></ul>問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。 |
| The changefeed status is `FAILED`. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| The changefeed status is `WARNING`. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|

</CustomContent>

<CustomContent plan="premium">

### {{{ .premium }}} のパフォーマンス概要アラート {#performance-overview-alerts-for-premium}

| 条件 | 推奨アクション |
|:--- |:--- |
| Request units per second (RU/s) exceed 80% of the maximum RCU | <ol><li>RU メトリクスを確認し、増加が緩やかなものか、急激なスパイクかを判断します。</li><li>増加が緩やかな場合は、クエリ実行時間が増加していないか確認します。増加している場合、現在の最大 RCU では不足している可能性があります。</li><li>TiDB Cloud コンソールで最大 RCU を手動で増やして、キャパシティをスケールします。</li></ol>問題を解決できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| RCU consumption (Request Unit/s) exceeds 100,000 RCUs | <ol><li>RU メトリクスでトラフィックパターンを確認し、増加が緩やかなものか、急激なスパイクかを判断します。</li><li>Elastic Mode では、TiDB Cloud はワークロードに応じてバックエンドキャパシティを自動的にスケールします。この使用量レベルが想定内である場合は、ワークロードに合わせてアラートしきい値を調整します。高い RU/s が継続するとコストが増加する可能性があることに注意してください。</li><li>この使用量レベルが想定外である場合は、Top RU 機能を使用して、最も多くの RU を消費しているクエリを特定し、最適化します。</li></ol>問題を解決できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| QPS drops by 80% | <ol><li>低下の原因がクエリのレイテンシー増加によるものか確認します。</li><li>アプリケーションが正常に動作していることを確認します。低下が意図的なものであれば、このアラートは無視してください。意図しない低下であり、根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。</li></ol>|
| Query P99 latency exceeds 200 ms | <ol><li>低速クエリを調査します。Slow Query ページに移動し、直近の時間範囲でフィルタリングして、新たに発生したクエリや実行が遅くなったクエリを特定します。</li><li>トラフィックパターンに影響した可能性がある、アプリケーションのデプロイ、スキーマ変更、データインポートジョブなどの最近の変更を確認します。</li></ol>根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| Query P95 latency exceeds 200 ms | <ol><li>低速クエリを調査します。Slow Query ページに移動し、直近の時間範囲でフィルタリングして、新たに発生したクエリや実行が遅くなったクエリを特定します。</li><li>トラフィックパターンに影響した可能性がある、アプリケーションのデプロイ、スキーマ変更、データインポートジョブなどの最近の変更を確認します。</li></ol>根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| Request error rate exceeds 10% | 最近のエラーと、クラスター全体のステートメント実行状況を確認します。|
| More than 20 SQL statements exceed a latency threshold of 256 ms within one minute | 最近のスキーマまたはインデックスの変更がないか確認します。TiDB Cloud コンソールで低速クエリの一覧を確認します。対応する低速クエリの記録が表示されるまでに数分かかる場合があります。根本原因を特定できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| More than 20 SQL statements exceed a latency threshold of 512 ms within one minute | 最近のスキーマまたはインデックスの変更がないか確認します。TiDB Cloud コンソールで低速クエリの一覧を確認します。対応する低速クエリの記録が表示されるまでに数分かかる場合があります。根本原因を特定できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| More than 20 SQL statements exceed a latency threshold of 4,096 ms within one minute | 最近のスキーマまたはインデックスの変更がないか確認します。TiDB Cloud コンソールで低速クエリの一覧を確認します。対応する低速クエリの記録が表示されるまでに数分かかる場合があります。根本原因を特定できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|

### {{{ .premium }}} の Changefeed アラート {#changefeed-alerts-for-premium}

| 条件                                   | 推奨アクション                   |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| The changefeed latency exceeds 600 seconds. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。このアラートが発生する原因として、次のようなものがあります。<ul><li>アップストリーム全体のトラフィックが増加し、既存の changefeed のスペックでは処理しきれなくなっている。トラフィックの増加が一時的な場合、トラフィックが正常に戻ると changefeed のレイテンシーは自動的に回復します。トラフィックの増加が継続的な場合は、changefeed をスケールアップする必要があります。</li><li>ダウンストリームまたはネットワークに異常がある。この場合は、まずその異常を解消してください。</li><li>ダウンストリームが RDS の場合、テーブルにインデックスが不足している可能性があり、書き込み性能の低下と高レイテンシーの原因になることがあります。この場合は、アップストリームまたはダウンストリームに必要なインデックスを追加する必要があります。</li></ul>問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。 |
| The changefeed status is `FAILED`. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| The changefeed status is `WARNING`. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|

</CustomContent>

<CustomContent plan="byoc">

### {{{ .byoc }}} のパフォーマンス概要アラート {#performance-overview-alerts-for-byoc}

| 条件 | 推奨アクション |
|:---|:---|
| Request units per second (RU/s) exceed 80% of the maximum RCU | <ol><li>RU メトリクスを確認し、増加が緩やかなものか、急激なスパイクかを判断します。</li><li>増加が緩やかな場合は、クエリ実行時間が増加していないか確認します。増加している場合、現在の最大 RCU では不足している可能性があります。</li><li>TiDB Cloud コンソールで最大 RCU を手動で増やして、キャパシティをスケールします。</li></ol>問題を解決できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| QPS drops by 80% | <ol><li>低下の原因がクエリのレイテンシー増加によるものか確認します。</li><li>アプリケーションが正常に動作していることを確認します。低下が意図的なものであれば、このアラートは無視してください。意図しない低下であり、根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。</li></ol>|
| Query P95 latency exceeds 200 ms | <ol><li>低速クエリを調査します。Slow Query ページに移動し、直近の時間範囲でフィルタリングして、新たに発生したクエリや実行が遅くなったクエリを特定します。</li><li>トラフィックパターンに影響した可能性がある、アプリケーションのデプロイ、スキーマ変更、データインポートジョブなどの最近の変更を確認します。</li></ol>根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| Query P99 latency exceeds 200 ms | <ol><li>低速クエリを調査します。Slow Query ページに移動し、直近の時間範囲でフィルタリングして、新たに発生したクエリや実行が遅くなったクエリを特定します。</li><li>トラフィックパターンに影響した可能性がある、アプリケーションのデプロイ、スキーマ変更、データインポートジョブなどの最近の変更を確認します。</li></ol>根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| Request error rate exceeds 10% | 最近のエラーと、クラスター全体のステートメント実行状況を確認します。|
| More than 20 SQL statements exceed a latency threshold of 256 ms within one minute | 最近のスキーマまたはインデックスの変更がないか確認します。TiDB Cloud コンソールで低速クエリの一覧を確認します。対応する低速クエリの記録が表示されるまでに数分かかる場合があります。根本原因を特定できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| More than 20 SQL statements exceed a latency threshold of 512 ms within one minute | 最近のスキーマまたはインデックスの変更がないか確認します。TiDB Cloud コンソールで低速クエリの一覧を確認します。対応する低速クエリの記録が表示されるまでに数分かかる場合があります。根本原因を特定できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| More than 20 SQL statements exceed a latency threshold of 4,096 ms within one minute | 最近のスキーマまたはインデックスの変更がないか確認します。TiDB Cloud コンソールで低速クエリの一覧を確認します。対応する低速クエリの記録が表示されるまでに数分かかる場合があります。根本原因を特定できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|

### {{{ .byoc }}} の Resource Pool vCPU 上限アラート {#resource-pool-vcpu-limit-alerts-for-byoc}

これらのアラートは、リソースプールの追加スケーリングに使える容量が限られている場合、またはスケーリング操作が **Pool vCPU Limit** によってブロックされた場合に通知します。

割り当て率は、リソースプール内のすべてのインスタンスにまたがる、データベース関連リソース向けにプロビジョニングされた vCPU の合計を **Pool vCPU Limit** で割った値です。Admin ノードおよび Observability ノードの vCPU は含まれません。これらのアラートは、**Pool vCPU Limit** が設定されている場合にのみ適用されます。

| アラート | 条件 | 推奨アクション |
|:---|:---|:---|
| Resource Pool vCPU allocation is high | 割り当て率が、設定されたしきい値以上の状態で、設定された期間継続した場合。デフォルトは 10 分間で 80% です。 | リソースプール内の各インスタンスにおける最近のワークロード変更と容量使用状況を確認してください。追加のスケーリング容量が必要な場合は、**Pool vCPU Limit** を引き上げてください。問題を解決できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。 |
| Resource Pool vCPU allocation is approaching the limit | 割り当て率が、設定されたしきい値以上の状態で、設定された期間継続した場合。デフォルトは 5 分間で 95% です。 | **Pool vCPU Limit** を引き上げてください。リソースプール内の各インスタンスの容量使用状況を確認し、最近のトラフィックスパイク、インポートジョブ、または異常なワークロード変化を調査してください。問題を解決できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。 |
| Resource Pool scaling was blocked by the vCPU limit | 要求された容量が **Pool vCPU Limit** を超えるため、スケーリング操作が拒否された場合。 | **Pool vCPU Limit** を引き上げるか、不要にプロビジョニングされている容量を削減してください。リソースプール内の各インスタンスにおけるワークロードと容量使用状況を確認してください。問題を解決できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。 |

2 つの割り当て率アラートはデフォルトで有効になっています。各インスタンスの **Edit Rules** ページで、しきい値と継続時間を変更するか、無効化できます。**Resource Pool vCPU allocation is high** のしきい値は、**Resource Pool vCPU allocation is approaching the limit** のしきい値より低く設定する必要があります。設定はインスタンスごとに適用されますが、割り当て率は共有リソースプール全体で測定されます。

**Resource Pool scaling was blocked by the vCPU limit** は無効化できません。これは、共有リソースプール内のスケーリング要求が、**Pool vCPU Limit** を超えるため拒否されたことを示します。このアラートは、同じリソースプール内の別のインスタンスがブロックされたスケーリング操作を要求した場合でも、あるインスタンスの **Alerts** ページに表示されることがあります。

### {{{ .byoc }}} の Changefeed アラート {#changefeed-alerts-for-byoc}

| 条件 | 推奨アクション |
|:---|:---|
| The changefeed latency exceeds 600 seconds. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。このアラートが発生する原因として、次のようなものがあります。<ul><li>アップストリーム全体のトラフィックが増加し、既存の changefeed のスペックでは処理しきれなくなっている。トラフィックの増加が一時的な場合、トラフィックが正常に戻ると changefeed のレイテンシーは自動的に回復します。トラフィックの増加が継続的な場合は、changefeed をスケールアップする必要があります。</li><li>ダウンストリームまたはネットワークに異常がある。この場合は、まずその異常を解消してください。</li><li>ダウンストリームが RDS の場合、テーブルにインデックスが不足している可能性があり、書き込み性能の低下と高レイテンシーの原因になることがあります。この場合は、アップストリームまたはダウンストリームに必要なインデックスを追加する必要があります。</li></ul>問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。 |
| The changefeed status is `FAILED`. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| The changefeed status is `WARNING`. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|

</CustomContent>

<CustomContent plan="essential">

### {{{ .essential }}} のパフォーマンス概要アラート {#performance-overview-alerts-for-essential}

| 条件 | 推奨アクション |
|:--- |:--- |
| Request units per second (RU/s) exceed 80% of the maximum RCU | <ol><li>RU メトリクスを確認し、増加が緩やかなものか、急激なスパイクかを判断します。</li><li>増加が緩やかな場合は、クエリ実行時間が増加していないか確認します。増加している場合、現在の最大 RCU では不足している可能性があります。</li><li>TiDB Cloud コンソールで最大 RCU を手動で増やして、キャパシティをスケールします。</li></ol>問題を解決できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| RCU consumption (Request Unit/s) exceeds 100,000 RCUs | <ol><li>RU メトリクスでトラフィックパターンを確認し、増加が緩やかなものか、急激なスパイクかを判断します。</li><li>Elastic Mode では、TiDB Cloud はワークロードに応じてバックエンドキャパシティを自動的にスケールします。この使用量レベルが想定内で、消費量が 100,000 RCU を超えた状態が続く場合は、パフォーマンスのボトルネックを避けるため TiDB Cloud Premium へのアップグレードを検討してください。高い RU/s が継続するとコストが増加する可能性があることに注意してください。</li><li>この使用量レベルが想定外である場合は、Top RU 機能を使用して、最も多くの RU を消費しているクエリを特定し、最適化します。</li></ol>問題を解決できない場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| QPS drops by 80% | <ol><li>低下の原因がクエリのレイテンシー増加によるものか確認します。</li><li>アプリケーションが正常に動作していることを確認します。低下が意図的なものであれば、このアラートは無視してください。意図しない低下であり、根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。</li></ol>|
| Query P99 latency exceeds 200 ms | <ol><li>低速クエリを調査します。Slow Query ページに移動し、直近の時間範囲でフィルタリングして、新たに発生したクエリや実行が遅くなったクエリを特定します。</li><li>トラフィックパターンに影響した可能性がある、アプリケーションのデプロイ、スキーマ変更、データインポートジョブなどの最近の変更を確認します。</li></ol>根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| Query P95 latency exceeds 200 ms | <ol><li>低速クエリを調査します。Slow Query ページに移動し、直近の時間範囲でフィルタリングして、新たに発生したクエリや実行が遅くなったクエリを特定します。</li><li>トラフィックパターンに影響した可能性がある、アプリケーションのデプロイ、スキーマ変更、データインポートジョブなどの最近の変更を確認します。</li></ol>根本原因を特定できない場合は、直ちに [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| Request error rate exceeds 10% | 最近のエラーと、クラスター全体のステートメント実行状況を確認します。|

### {{{ .essential }}} の Changefeed アラート {#changefeed-alerts-for-essential}

| 条件                                   | 推奨アクション                   |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| The changefeed latency exceeds 600 seconds. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。このアラートが発生する原因として、次のようなものがあります。<ul><li>アップストリーム全体のトラフィックが増加し、既存の changefeed のスペックでは処理しきれなくなっている。トラフィックの増加が一時的な場合、トラフィックが正常に戻ると changefeed のレイテンシーは自動的に回復します。トラフィックの増加が継続的な場合は、changefeed をスケールアップする必要があります。</li><li>ダウンストリームまたはネットワークに異常がある。この場合は、まずその異常を解消してください。</li><li>ダウンストリームが RDS の場合、テーブルにインデックスが不足している可能性があり、書き込み性能の低下と高レイテンシーの原因になることがあります。この場合は、アップストリームまたはダウンストリームに必要なインデックスを追加する必要があります。</li></ul>問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。 |
| The changefeed status is `FAILED`. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|
| The changefeed status is `WARNING`. | TiDB Cloud コンソールの **Changefeed** ページおよび **Changefeed Detail** ページで changefeed のステータスを確認してください。問題の診断に役立つエラーメッセージを確認できます。問題をお客様側で解決できない場合は、追加のサポートについて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。|

</CustomContent>
