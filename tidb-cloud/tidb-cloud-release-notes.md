---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2023 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2023}

このページでは、2023 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートを一覧表示します。

## 2023 年 4 月 25 日 {#april-25-2023}

**一般的な変更**

-   組織内の最初の 5 つの[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターについて、 TiDB Cloud は、次のようにそれぞれに無料の使用量クォータを提供します。

    -   行storage: 5 GiB
    -   [リクエスト ユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 1 か月あたり 5,000 万 RU

    2023 年 5 月 30 日まで、Serverless Tierクラスターは引き続き無料で、100% 割引になります。それ以降は、無料枠を超えた分は課金されます。

    クラスターの**[概要]**ページの<strong>[今月の使用状況]</strong>領域で簡単に[クラスターの使用状況を監視するか、使用クォータを増やします](/tidb-cloud/manage-serverless-spend-limit.md#manage-spend-limit-for-serverless-tier-clusters)できます。クラスターの無料クォータに達すると、このクラスターの読み取りおよび書き込み操作は、クォータを増やすか、新しい月の開始時に使用量がリセットされるまで調整されます。

    さまざまなリソース (読み取り、書き込み、SQL CPU、およびネットワーク エグレスを含む) の RU 消費、料金の詳細、調整された情報について詳しくは、 [TiDB CloudServerless Tierの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

-   TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのバックアップと復元をサポートします。

    詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#serverless-tier)を参照してください。

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターのデフォルトの TiDB バージョンを[v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)から[v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)にアップグレードします。

-   メンテナンス ウィンドウ機能を提供して、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの計画されたメンテナンス アクティビティを簡単にスケジュールおよび管理できるようにします。

    メンテナンス ウィンドウは、 TiDB Cloudサービスの信頼性、セキュリティ、およびパフォーマンスを確保するために、オペレーティング システムの更新、セキュリティ パッチ、インフラストラクチャのアップグレードなどの計画されたメンテナンス アクティビティが自動的に実行される指定された時間枠です。

    メンテナンス期間中は、一時的な接続の中断や QPS の変動が発生する可能性がありますが、クラスターは引き続き使用でき、SQL 操作、既存のデータのインポート、バックアップ、復元、移行、およびレプリケーション タスクは引き続き正常に実行できます。メンテナンス中は[許可された操作と許可されていない操作のリスト](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)を参照してください。

    メンテナンスの頻度を最小限に抑えるよう努めます。メンテナンスウィンドウが計画されている場合、デフォルトの開始時間は、対象の週の ( TiDB Cloud組織のタイムゾーンに基づく) 水曜日の 03:00 です。潜在的な混乱を避けるために、メンテナンス スケジュールを認識し、それに応じて操作を計画することが重要です。

    -   通知を受け取るために、 TiDB Cloud はメンテナンス ウィンドウごとに 3 つの電子メール通知を送信します。1 つはメンテナンス タスクの前、もう 1 つは開始中、もう 1 つはメンテナンス タスクの後です。
    -   メンテナンスの影響を最小限に抑えるために、**メンテナンス**ページでメンテナンスの開始時間を希望の時間に変更するか、メンテナンス アクティビティを延期することができます。

    詳細については、 [メンテナンス ウィンドウの構成](/tidb-cloud/configure-maintenance-window.md)を参照してください。

-   AWS でホストされている[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの TiDB ノードをスケーリングすると、TiDB の負荷分散が改善され、接続のドロップが減少します。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を使用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は、AWS でホストされているすべてのDedicated Tierクラスターに提供されています。

**コンソールの変更**

-   [モニタリング](/tidb-cloud/built-in-monitoring.md#view-the-monitoring-page)ページ オブ[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタ用の新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャにより、 [モニタリング](/tidb-cloud/built-in-monitoring.md#view-the-monitoring-page)ページを簡単にナビゲートし、より直感的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは、UX に関する多くの問題も解決し、監視プロセスをよりユーザーフレンドリーにします。

## 2023 年 4 月 18 日 {#april-18-2023}

**一般的な変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターに対して[データ移行ジョブの仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)スケールアップまたはスケールダウンをサポートします。

    この機能により、スペックをスケールアップすることでマイグレーション性能を向上させたり、スペックをスケールダウンすることでコストを削減したりできます。

    詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)を参照してください。

**コンソールの変更**

-   UI を刷新して[クラスターの作成](https://tidbcloud.com/console/clusters/create-cluster)エクスペリエンスをより使いやすくし、数回クリックするだけでクラスターを作成および構成できるようにします。

    新しいデザインはシンプルさに重点を置いており、視覚的な煩雑さを減らし、明確な指示を提供します。クラスター作成ページで**[作成]**をクリックすると、クラスターの作成が完了するのを待たずに、クラスターの概要ページに移動します。

    詳細については、 [クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

-   **[請求**] ページに<strong>[割引]</strong>タブを導入して、組織の所有者と請求管理者向けの割引情報を表示します。

    詳細については、 [割引](/tidb-cloud/tidb-cloud-billing.md#discounts)を参照してください。

## 2023 年 4 月 11 日 {#april-11-2023}

**一般的な変更**

-   AWS でホストされている[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの TiDB ノードをスケーリングすると、TiDB の負荷バランスが改善され、接続のドロップが減少します。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を使用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は、AWS `Oregon (us-west-2)`リージョンでホストされているDedicated Tierクラスターに対してのみ提供されています。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタに対して[ニューレリック](https://newrelic.com/)統合をサポートします。

    New Relic の統合により、TiDB クラスターのメトリクス データを[ニューレリック](https://newrelic.com/)に送信するようにTiDB Cloudを構成できます。次に、アプリケーションのパフォーマンスと TiDB データベースのパフォーマンスの両方を[ニューレリック](https://newrelic.com/)で監視および分析できます。この機能は、潜在的な問題を迅速に特定してトラブルシューティングし、解決時間を短縮するのに役立ちます。

    統合の手順と利用可能な指標については、 [TiDB CloudをNew Relic と統合する](/tidb-cloud/monitor-new-relic-integration.md)を参照してください。

-   次の[チェンジフィード](/tidb-cloud/changefeed-overview.md)メトリクスをDedicated Tierクラスターの Prometheus 統合に追加します。

    -   `tidbcloud_changefeed_latency`
    -   `tidbcloud_changefeed_replica_rows`

    [TiDB Cloudと Prometheus の統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)をお持ちの場合は、これらのメトリクスを使用してリアルタイムで変更フィードのパフォーマンスと正常性を監視できます。さらに、Prometheus を使用してメトリックを監視するためのアラートを簡単に作成できます。

**コンソールの変更**

-   [ノードレベルのリソース メトリック](/tidb-cloud/built-in-monitoring.md#server)を使用するように[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの[モニタリング](/tidb-cloud/built-in-monitoring.md#view-the-monitoring-page)ページを更新します。

    ノードレベルのリソース メトリクスを使用すると、リソース消費のより正確な表現を確認して、購入したサービスの実際の使用状況をよりよく理解できます。

    これらのメトリクスにアクセスするには、クラスターの[モニタリング](/tidb-cloud/built-in-monitoring.md#view-the-monitoring-page)ページに移動し、 **[メトリクス]**タブの<strong>[サーバー]</strong>カテゴリを確認します。

-   **プロジェクト別集計**と<strong>サービス別集計</strong>の請求項目を整理して[請求する](/tidb-cloud/tidb-cloud-billing.md#billing-details)ページを最適化し、請求情報をより明確にします。

## 2023 年 4 月 4 日 {#april-4-2023}

**一般的な変更**

-   誤検知を防ぐために、次の 2 つのアラートを[TiDB Cloudの組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions)から削除します。これは、ノードの 1 つでの一時的なオフラインまたはメモリ不足 (OOM) の問題が、クラスターの全体的な正常性に大きな影響を与えないためです。

    -   クラスタ内の少なくとも 1 つの TiDB ノードでメモリが不足しています。
    -   1 つ以上のクラスター ノードがオフラインです。

**コンソールの変更**

-   各Dedicated Tierクラスターのアクティブなアラートとクローズされたアラートの両方を一覧表示する、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)のクラスターの[アラート](/tidb-cloud/monitor-built-in-alerting.md)ページを導入します。

    **アラート**ページには、次の情報が表示されます。

    -   直感的で使いやすいユーザー インターフェイス。アラート通知メールを購読していない場合でも、このページでクラスターのアラートを表示できます。
    -   重大度、ステータス、およびその他の属性に基づいてアラートをすばやく見つけて並べ替えるのに役立つ高度なフィルタリング オプション。また、過去 7 日間の履歴データを表示できるため、アラート履歴の追跡が容易になります。
    -   **ルールの編集**機能。アラート ルールの設定をカスタマイズして、クラスター固有のニーズを満たすことができます。

    詳細については、 [TiDB Cloudの組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)を参照してください。

-   TiDB Cloudのヘルプ関連情報とアクションを 1 つの場所に統合します。

    これで、すべての[TiDB Cloudヘルプ情報](/tidb-cloud/tidb-cloud-support.md#get-help-information)取得して、 **[?]**をクリックしてサポートに連絡できます。 [TiDB Cloudコンソール](https://tidbcloud.com/)の右下隅にあります。

-   TiDB Cloudについて学ぶのに役立つ[入門](https://tidbcloud.com/console/getting-started)ページを紹介します。

    **はじめに**ページには、インタラクティブなチュートリアル、重要なガイド、および便利なリンクが用意されています。インタラクティブなチュートリアルに従うことで、事前に構築された業界固有のデータセット (Steam ゲーム データセットと S&amp;P 500 データセット) を使用して、 TiDB Cloudの機能と HTAP 機能を簡単に調べることができます。

    **[はじめに**] ページにアクセスするには、 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> [TiDB Cloudコンソール](https://tidbcloud.com/)の左側のナビゲーション バーにある<strong>[はじめに]</strong> 。このページでは、 <strong>Query Sample Dataset</strong>をクリックしてインタラクティブなチュートリアルを開くか、他のリンクをクリックしてTiDB Cloudを探索できます。または、 <strong>?</strong>をクリックすることもできます。をクリックし、<strong>インタラクティブ チュートリアル</strong>をクリックします。

## 2023 年 3 月 29 日 {#march-29-2023}

**一般的な変更**

-   [データ サービス (ベータ)](/tidb-cloud/data-service-overview.md) Data Apps のよりきめ細かいアクセス制御をサポートします。

    データ アプリの詳細ページで、クラスターをデータ アプリにリンクし、各 API キーのロールを指定できるようになりました。ロールは、API キーがリンクされたクラスターに対してデータを読み書きできるかどうかを制御し、 `ReadOnly`または`ReadAndWrite`に設定できます。この機能は、データ アプリのクラスター レベルおよびアクセス許可レベルのアクセス制御を提供し、ビジネス ニーズに応じてアクセス スコープをより柔軟に制御できるようにします。

    詳細については、 [リンクされたクラスターを管理する](/tidb-cloud/data-service-manage-data-app.md#manage-linked-clusters)および[API キーの管理](/tidb-cloud/data-service-api-key.md)を参照してください。

## 2023 年 3 月 28 日 {#march-28-2023}

**一般的な変更**

-   [チェンジフィード](/tidb-cloud/changefeed-overview.md)に 2 RCU、4 RCU、8 RCU の仕様を追加し、 [チェンジフィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)の場合の希望の仕様の選択をサポートします。

    これらの新しい仕様を使用すると、以前は 16 個の RCU が必要だったシナリオと比較して、データ複製コストを最大 87.5% 削減できます。

-   2023年3月28日以降に作成された[チェンジフィード](/tidb-cloud/changefeed-overview.md)拡大縮小仕様に対応。

    より高い仕様を選択することで複製のパフォーマンスを向上させたり、より低い仕様を選択することで複製コストを削減したりできます。

    詳細については、 [変更フィードをスケーリングする](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)を参照してください。

-   AWS の[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターから同じプロジェクトと同じリージョンの[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターへのリアルタイムでの増分データのレプリケートをサポートします。

    詳細については、 [TiDB Cloudにシンク](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)を参照してください。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)の機能について、2 つの新しい GCP リージョンをサポートします: `Singapore (asia-southeast1)`と`Oregon (us-west1)` 。

    これらの新しいリージョンにより、データをTiDB Cloudに移行するためのオプションが増えました。アップストリーム データがこれらのリージョンまたはその近くに保存されている場合、GCP からTiDB Cloudへのより高速で信頼性の高いデータ移行を利用できるようになりました。

    詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

**コンソールの変更**

-   [スロークエリ](/tidb-cloud/tune-performance.md#slow-query)ページ オブ[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスタ用の新しいネイティブ Web インフラストラクチャをリリースします。

    この新しいインフラストラクチャにより、 [スロークエリ](/tidb-cloud/tune-performance.md#slow-query)ページを簡単にナビゲートし、より直感的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは、UX に関する多くの問題も解決し、SQL 診断プロセスをよりユーザーフレンドリーにします。

## 2023 年 3 月 21 日 {#march-21-2023}

**一般的な変更**

-   カスタム API エンドポイントを使用して、HTTPS リクエスト経由でデータにアクセスできるようにする[データ サービス (ベータ)](https://tidbcloud.com/console/data-service)対[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターを導入します。

    Data Service を使用すると、HTTPS と互換性のある任意のアプリケーションまたはサービスとTiDB Cloudをシームレスに統合できます。次に、一般的なシナリオをいくつか示します。

    -   モバイルまたは Web アプリケーションから TiDB クラスターのデータベースに直接アクセスします。
    -   サーバーレス エッジ関数を使用してエンドポイントを呼び出し、データベース接続プールによって引き起こされるスケーラビリティの問題を回避します。
    -   Data Service をデータ ソースとして使用して、 TiDB Cloudをデータ視覚化プロジェクトと統合します。
    -   MySQL インターフェイスがサポートしていない環境からデータベースに接続します。

    さらに、 TiDB Cloud は、AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェイスである[Chat2Query API](/tidb-cloud/use-chat2query-api.md)提供します。

    Data Service にアクセスするには、左側のナビゲーション ペインで[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。詳細については、次のドキュメントを参照してください。

    -   [データ サービスの概要](/tidb-cloud/data-service-overview.md)
    -   [データ サービスを開始する](/tidb-cloud/data-service-get-started.md)
    -   [Chat2Query API を使ってみる](/tidb-cloud/use-chat2query-api.md)

-   AWS でホストされ、2022 年 12 月 31 日以降に作成された[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)のクラスターでスケーリングするために、TiDB、TiKV、およびTiFlashノードのサイズを縮小することをサポートします。

    ノード サイズを[TiDB Cloudコンソール経由](/tidb-cloud/scale-tidb-cluster.md#change-node-size)または[TiDB Cloud API (ベータ版) 経由](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)減らすことができます。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)のクラスタの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能である新しい GCP リージョンをサポートします: `Tokyo (asia-northeast1)` 。

    この機能は、Google Cloud Platform (GCP) の MySQL 互換データベースから TiDB クラスターにデータを簡単かつ効率的に移行するのに役立ちます。

    詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの**[イベント]**ページを紹介します。これは、クラスターへの主な変更の記録を提供します。

    このページでは、過去 7 日間のイベント履歴を表示し、トリガー時刻やアクションを開始したユーザーなどの重要な詳細を追跡できます。たとえば、クラスターが一時停止された時期やクラスター サイズを変更したユーザーなどのイベントを表示できます。

    詳細については、 [TiDB Cloudクラスター イベント](/tidb-cloud/tidb-cloud-events.md)を参照してください。

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターの**[監視]**ページに<strong>[データベース ステータス]</strong>タブを追加します。このページには、次のデータベース レベルのメトリックが表示されます。

    -   DB あたりの QPS
    -   DB あたりの平均クエリ時間
    -   DB あたりの失敗したクエリ

    これらのメトリックを使用して、個々のデータベースのパフォーマンスを監視し、データ主導の意思決定を行い、アプリケーションのパフォーマンスを改善するためのアクションを実行できます。

    詳細については、 [Serverless Tierクラスターのモニタリング指標](/tidb-cloud/built-in-monitoring.md)を参照してください。

## 2023 年 3 月 14 日 {#march-14-2023}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターのデフォルトの TiDB バージョンを[v6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0)から[v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)にアップグレードします。

-   ヘッダー行を含むローカル CSV ファイルをアップロードするときに、 TiDB Cloudによって作成されるターゲット テーブルの列名の変更をサポートします。

    ヘッダー行を含むローカル CSV ファイルを[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターにインポートするときに、 TiDB Cloudでターゲット テーブルを作成する必要があり、ヘッダー行の列名がTiDB Cloud列の命名規則に従っていない場合は、次に警告アイコンが表示されます。対応する列名に。警告を解決するには、アイコンの上にカーソルを移動し、メッセージに従って既存の列名を編集するか、新しい列名を入力します。

    列の命名規則については、 [ローカル ファイルのインポート](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)を参照してください。

## 2023 年 3 月 7 日 {#march-7-2023}

**一般的な変更**

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのデフォルトの TiDB バージョンを[v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)から[v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)にアップグレードします。

## 2023 年 2 月 28 日 {#february-28-2023}

**一般的な変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターに[SQL 診断](/tidb-cloud/tune-performance.md)機能を追加します。

    SQL 診断を使用すると、SQL 関連のランタイム ステータスを詳細に把握できるため、SQL パフォーマンス チューニングがより効率的になります。現在、Serverless Tierの SQL 診断機能は、スロー クエリ データのみを提供します。

    SQL 診断を使用するには、Serverless Tierクラスター ページの左側のナビゲーション バーで**[SQL 診断]**をクリックします。

**コンソールの変更**

-   左のナビゲーションを最適化します。

    次の例のように、より効率的にページをナビゲートできます。

    -   マウスを左上隅に置くと、クラスターまたはプロジェクトをすばやく切り替えることができます。
    -   **Clusters**ページと<strong>Admin</strong>ページを切り替えることができます。

**API の変更**

-   データ インポート用のいくつかのTiDB Cloud API エンドポイントをリリースします。

    -   すべてのインポート タスクを一覧表示する
    -   インポート タスクを取得する
    -   インポート タスクを作成する
    -   インポート タスクを更新する
    -   インポート タスク用のローカル ファイルをアップロードする
    -   インポート タスクを開始する前にデータをプレビューする
    -   インポート タスクのロール情報を取得する

    詳細については、 [API ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import)を参照してください。

## 2023 年 2 月 22 日 {#february-22-2023}

**一般的な変更**

-   [コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)機能を使用して、組織内のメンバーが実行したさまざまなアクティビティを[TiDB Cloudコンソール](https://tidbcloud.com/)で追跡することをサポートします。

    コンソール監査ログ機能は、ロール`Owner`または`Audit Admin`を持つユーザーにのみ表示され、デフォルトでは無効になっています。有効にするには、<mdsvgicon name="icon-top-organization"> [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある**[Organization]** &gt; <strong>[Console Audit Logging]</strong> 。</mdsvgicon>

    コンソール監査ログを分析することで、組織内で実行された疑わしい操作を特定できるため、組織のリソースとデータのセキュリティが向上します。

    詳細については、 [コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)を参照してください。

**CLI の変更**

-   新しいコマンド[`ticloud cluster connect-info`](/tidb-cloud/ticloud-cluster-connect-info.md) for [TiDB CloudCLI](/tidb-cloud/cli-reference.md)を追加します。

    `ticloud cluster connect-info`は、クラスターの接続文字列を取得できるコマンドです。このコマンドを使用するには、 [`ticloud`](/tidb-cloud/ticloud-update.md)から v0.3.2 以降のバージョンにします。

## 2023 年 2 月 21 日 {#february-21-2023}

**一般的な変更**

-   TiDB Cloudにデータをインポートするときに、 IAMユーザーの AWS アクセス キーを使用して Amazon S3 バケットにアクセスすることをサポートします。

    この方法は、Role ARN を使用するよりも簡単です。詳細については、 [Amazon S3 アクセスの構成](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

-   [監視メトリクスの保存期間](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 2 日からより長い期間に延長します。

    -   Dedicated Tierクラスターの場合、過去 7 日間のメトリック データを表示できます。
    -   Serverless Tierクラスターの場合、過去 3 日間のメトリック データを表示できます。

    指標の保持期間を延長することで、より多くの履歴データにアクセスできるようになりました。これにより、クラスターの傾向とパターンを特定して、より適切な意思決定と迅速なトラブルシューティングを行うことができます。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターの [監視] ページで、新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャを使用すると、[監視] ページを簡単にナビゲートし、より直感的かつ効率的な方法で必要な情報にアクセスできます。また、新しいインフラストラクチャは、UX に関する多くの問題を解決し、監視プロセスをよりユーザーフレンドリーにします。

## 2023 年 2 月 17 日 {#february-17-2023}

**CLI の変更**

-   新しいコマンド[`ticloud connect`](/tidb-cloud/ticloud-connect.md) for [TiDB CloudCLI](/tidb-cloud/cli-reference.md)を追加します。

    `ticloud connect`は、SQL クライアントをインストールせずに、ローカル マシンからTiDB Cloudクラスターに接続できるようにするコマンドです。 TiDB Cloudクラスターに接続したら、 TiDB Cloud CLI で SQL ステートメントを実行できます。

## 2023 年 2 月 14 日 {#february-14-2023}

**一般的な変更**

-   TiDB [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターでスケーリングするために TiKV およびTiFlashノードの数を減らすことをサポートします。

    ノード番号[TiDB Cloudコンソール経由](/tidb-cloud/scale-tidb-cluster.md#change-node-number)または[TiDB Cloud API (ベータ版) 経由](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)を減らすことができます。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)のクラスタの**モニタリング**ページを紹介します。

    **[監視]**ページには、1 秒あたりに実行された SQL ステートメントの数、クエリの平均実行時間、失敗したクエリの数など、さまざまなメトリックとデータが表示され、Serverless Tierでの SQL ステートメントの全体的なパフォーマンスをよりよく理解するのに役立ちます。集まる。

    詳細については、 [TiDB Cloud組み込みモニタリング](/tidb-cloud/built-in-monitoring.md)を参照してください。

## 2023 年 2 月 2 日 {#february-2-2023}

**CLI の変更**

-   TiDB Cloud CLI クライアントを紹介します[`ticloud`](/tidb-cloud/cli-reference.md) 。

    `ticloud`を使用すると、数行のコマンドを使用して、ターミナルまたはその他の自動ワークフローからTiDB Cloudリソースを簡単に管理できます。特に GitHub Actions については、簡単にセットアップできるように[`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli)用意しました`ticloud` 。

    詳細については、 [TiDB CloudCLI クイック スタート](/tidb-cloud/get-started-with-cli.md)および[TiDB CloudCLI リファレンス](/tidb-cloud/cli-reference.md)を参照してください。

## 2023 年 1 月 18 日 {#january-18-2023}

**一般的な変更**

-   Microsoft アカウントで[サインアップ](https://tidbcloud.com/free-trial) TiDB Cloudをサポートします。

## 2023 年 1 月 17 日 {#january-17-2023}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターのデフォルトの TiDB バージョンを[v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3)から[v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0)にアップグレードします。

-   新規サインアップ ユーザーの場合、 TiDB Cloud は無料の[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターを自動的に作成するため、 TiDB Cloudでデータ探索の旅をすぐに開始できます。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスター: `Seoul (ap-northeast-2)`の新しい AWS リージョンをサポートします。

    このリージョンでは、次の機能が有効になっています。

    -   [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    -   [changefeed を使用してTiDB Cloudから他のデータ サービスにデータをストリーミングする](/tidb-cloud/changefeed-overview.md)
    -   [TiDB クラスター データのバックアップと復元](/tidb-cloud/backup-and-restore.md)

## 2023 年 1 月 10 日 {#january-10-2023}

**一般的な変更**

-   ローカル CSV ファイルから TiDB にデータをインポートする機能を最適化して、 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのユーザー エクスペリエンスを向上させます。

    -   CSV ファイルをアップロードするには、**インポート**ページのアップロード エリアにドラッグ アンド ドロップするだけです。
    -   インポート タスクを作成するときに、ターゲット データベースまたはテーブルが存在しない場合は、名前を入力して、 TiDB Cloud が自動的に作成できるようにすることができます。作成するターゲット テーブルでは、主キーを指定するか、複数のフィールドを選択して複合主キーを形成できます。
    -   インポートが完了したら、 **[Chat2Query でデータを探索]**をクリックするか、タスク リストで対象のテーブル名をクリックして、 [AI 搭載の Chat2Query](/tidb-cloud/explore-data-with-chat2query.md)でデータを探索できます。

    詳細については、 [ローカル ファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

**コンソールの変更**

-   各クラスターに**Get Support**オプションを追加して、特定のクラスターのサポートを要求するプロセスを簡素化します。

    次のいずれかの方法で、クラスターのサポートをリクエストできます。

    -   プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページで、クラスターの行にある**...**をクリックし、 <strong>Get Support</strong>を選択します。
    -   クラスターの概要ページで、右上隅にある**[...]**をクリックし、 <strong>[サポートを受ける]</strong>を選択します。

## 2023 年 1 月 5 日 {#january-5-2023}

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターの SQL エディター (ベータ) の名前を Chat2Query (ベータ) に変更し、AI を使用した SQL クエリの生成をサポートします。

    Chat2Query では、AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で記述して、端末なしでデータベースに対して SQL クエリを実行することができます。

    Chat2Query にアクセスするには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、クラスター名をクリックしてから、左側のナビゲーション ペインで**[Chat2Query]**をクリックします。

## 2023 年 1 月 4 日 {#january-4-2023}

**一般的な変更**

-   AWS でホストされ、2022 年 12 月 31 日以降に作成された TiDB Dedicated Tierクラスターの**ノード サイズ (vCPU + RAM)**を増やすことで、TiDB、TiKV、およびTiFlashノードのスケールアップをサポートします。

    ノード サイズを[TiDB Cloudコンソールの使用](/tidb-cloud/scale-tidb-cluster.md#change-node-size)または[TiDB CloudAPI (ベータ版) を使用する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)増やすことができます。

-   [**モニタリング**](/tidb-cloud/built-in-monitoring.md)ページのメトリクスの保持期間を 2 日間に延長します。

    過去 2 日間のメトリクス データにアクセスできるようになり、クラスターのパフォーマンスと傾向に対する柔軟性と可視性が向上しました。

    この改善は追加料金なしで提供され、クラスターの[**モニタリング**](/tidb-cloud/built-in-monitoring.md)ページの**[診断]**タブでアクセスできます。これは、パフォーマンスの問題を特定してトラブルシューティングし、クラスターの全体的な状態をより効果的に監視するのに役立ちます。

-   Prometheus 統合のための Grafana ダッシュボード JSON のカスタマイズをサポートします。

    [TiDB Cloudと Prometheus の統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)お持ちの場合は、ビルド済みの Grafana ダッシュボードをインポートして、 TiDB Cloudクラスターを監視し、必要に応じてダッシュボードをカスタマイズできます。この機能により、 TiDB Cloudクラスターの簡単かつ迅速な監視が可能になり、パフォーマンスの問題をすばやく特定するのに役立ちます。

    詳細については、 [Grafana GUI ダッシュボードを使用してメトリックを視覚化する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)を参照してください。

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのデフォルトの TiDB バージョンを[v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。Serverless Tierクラスターのデフォルトの TiDB バージョンを v6.4.0 にアップグレードした後のコールド スタートの問題が解決されました。

**コンソールの変更**

-   [**クラスター**](https://tidbcloud.com/console/clusters)ページとクラスター概要ページの表示を簡素化します。

    -   [**クラスター**](https://tidbcloud.com/console/clusters)ページでクラスター名をクリックすると、クラスターの概要ページに入り、クラスターの操作を開始できます。
    -   クラスターの概要ページから**[接続] ペイン**と<strong>[インポート]</strong>ペインを削除します。右上隅の<strong>[接続]</strong>をクリックして接続情報を取得し、左側のナビゲーション ペインで<strong>[インポート]</strong>をクリックしてデータをインポートできます。
