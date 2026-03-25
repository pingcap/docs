---
title: TiDB Cloud Release Notes in 2026
summary: TiDB Cloudの2026年のリリースノートについてご確認ください。
aliases: ['/ja/tidbcloud/supported-tidb-versions','/ja/tidbcloud/release-notes']
---

# TiDB Cloud 2026年のリリースノート {#tidb-cloud-release-notes-in-2026}

このページには、2026年版[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリースノートが掲載されています。

## 2026年3月24日 {#march-24-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   TiDB Cloudで**パブリックエンドポイントの**ステータスを[コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)に設定して、セキュリティ追跡を改善します。

**コンソールの変更**

-   値のばらつきが大きい指標の視覚化を向上させるため、対数Y軸をサポートします。高値域と低値域の変動が明確に表示されるため、異常値を特定しやすくなります。

## 2026年3月10日 {#march-10-2026}

**全般的な変更**

-   **TiDB Cloud Essential**

    -   データフローシナリオにおけるプライベートリンク接続でのAmazon MSK Provisionedをサポートします。

        バージョン[TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)では、バージョン[Amazon MSK プロビジョニング済み](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html)クラスターへのプライベートリンク接続の作成がサポートされるようになりました。この機能により、変更フィードをAmazon MSKプロビジョニング済みクラスターにプライベートネットワーク接続することが可能になり、トラフィックをパブリックインターネットに公開することなく利用できます。

        詳細については、 [プライベートリンク接続を介してAmazon MSK Provisionedに接続します](/tidb-cloud/serverless-private-link-connection-to-amazon-msk.md)参照してください。

## 2026年3月3日 {#march-3-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   Amazon S3シンクのChangefeedsは、認証にAWSロールARNを使用することをサポートしています。

        Amazon S3 シンクの変更フィードを、既存の AK/SK 認証方法に加え、 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでIAMロール ARN を使用して設定できるようになりました。この機能により、有効期限の短い認証情報と自動ローテーションが可能になり、セキュリティが強化されるとともに、シークレット管理が簡素化され、最小権限の原則がサポートされます。

        詳細については、 [クラウドストレージへのシンク](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

    -   TiKVおよびTiFlashのstorage使用量計算を改善します。

        メトリクスおよびアラートシステムにおけるTiKVおよびTiFlashstorage使用量の計算に、WALファイルと一時ファイルが組み込まれるようになり、より正確な容量および使用状況の監視が可能になりました。

        詳細については、 [TiDB Cloud の組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)参照してください。

## 2026年2月10日 {#february-10-2026}

**全般的な変更**

-   **TiDB Cloud Starter**

    -   新規クラスター[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)のデフォルトのTiDBバージョンを[v7.5.6](https://docs.pingcap.com/tidb/stable/release-7.5.6)から[v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3)にアップグレードします。

-   **TiDB Cloud Essential**

    -   組み込みアラート機能をサポートします。

        組み込みのアラート機能を使用すると、メール、Slack、Zoom、Flashduty、PagerDutyを通じて即座にアラートを受信できます。また、アラートの種類ごとに特定のしきい値を定義することで、アラートをカスタマイズすることも可能です。

        詳細については、 [TiDB Cloudの組み込みアラート機能](https://docs.pingcap.com/tidbcloud/monitor-built-in-alerting/?plan=essential)参照してください。

-   **TiDB Cloud Dedicated**

    -   Azure Blob Storageからのデータインポートにおけるプライベートリンク接続をサポートします。

        Azure Blob Storage から[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)にデータをインポートする際に、接続方法としてプライベートリンクを選択し、パブリックインターネットではなく Azure プライベートエンドポイント経由で接続できるようになりました。この機能により、パブリックアクセスが制限されているstorageアカウントに対して、安全でネットワーク分離されたデータインポートが可能になります。

        詳細については、 [クラウドストレージからサンプルデータ（SQLファイル）をインポートする](/tidb-cloud/import-sample-data.md) [クラウドストレージからCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)および[クラウドストレージからApache Parquetファイルをインポートする](/tidb-cloud/import-parquet-files.md)を参照してください。

    -   セキュリティ追跡を強化するため、 TiDB Cloudのコンソール監査ログに「パブリックエンドポイントの有効化/無効化」イベントを追加します。

## 2026年2月3日 {#february-3-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   変更フィードデータをAzure Blob Storageにシンクすることをサポートします。

        バージョン[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)では、変更フィードデータをAzure Blob Storageに直接保存できるようになりました。この機能により、Azureベースのユーザーは、変更データを効率的にアーカイブして、下流の分析や長期保存に活用できます。また、中間メッセージキューが不要になるためコスト削減にもつながり、既存のAmazon S3およびGoogle Cloud Storage（GCS）シンクとのフォーマット互換性も維持されます。

        詳細については、 [クラウドストレージへのシンク](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

## 2026年1月27日 {#january-27-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   FlashDutyとPagerDutyをアラート購読チャネルとしてサポートします。

        これらの統合機能は、インシデント管理プロセスを効率化し、運用上の信頼性を向上させるように設計されています。

        詳細については、 [Flashduty経由で購読する](/tidb-cloud/monitor-alert-flashduty.md)と[PagerDuty経由で購読する](/tidb-cloud/monitor-alert-pagerduty.md)参照してください。

## 2026年1月20日 {#january-20-2026}

**全般的な変更**

-   **TiDB Cloud Starter**

    -   [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)番目のビューと[`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)テーブルに実際のクライアントIPアドレスを表示します（ベータ版）。

        TiDB CloudはクライアントIPパススルーをサポートするようになり、スロークエリビューと`INFORMATION_SCHEMA.PROCESSLIST`テーブルで、ロードバランサー（LB）のIPアドレスではなく、実際のクライアントIPアドレスを表示できるようになりました。この機能により、データベースリクエストの真の送信元を正確に特定し、トラブルシューティングと分析を改善できます。

        現在、この機能はベータ版であり、AWSリージョン`Frankfurt (eu-central-1)`でのみ利用可能です。

-   **TiDB Cloud Essential**

    -   データ移行をサポートします（ベータ版）。

        これで、 [TiDB Cloudコンソール](https://tidbcloud.com)データ移行機能を使用して、MySQL 互換データベースから[TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)クラスターへデータをシームレスに移行できるようになりました。

        -   サポートされているソースデータベースには、セルフホスト型MySQL、Amazon RDS、Alibaba Cloud RDS、PolarDBなど、さまざまなMySQL互換システムが含まれます。
        -   データ移行にサポートされている接続方法には、使いやすさとエンタープライズグレードのセキュリティの両方を確保するために、パブリック接続とPrivateLinkが含まれます。

            -   **パブリック接続**：安全で暗号化されたチャネルを使用して、インターネット経由でソースデータベースに迅速に接続します。
            -   **PrivateLink** ：ソースVPCとTiDB Cloud間の安全でプライベートな接続を確立し、パブリックインターネットをバイパスすることで、最大限のデータプライバシーとネットワークレイテンシーの低減を実現します。

        現在、データ移行機能は論理モードのみをサポートしています。

        詳細については、 [データ移行を使用して既存データと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)と[データ移行を使用して増分データを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)参照してください。

    -   [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ビュー、 [DB監査ログ](/tidb-cloud/essential-database-audit-logging.md) 、および[`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)テーブルに実際のクライアントIPアドレスを表示します（ベータ版）

        TiDB CloudはクライアントIPパススルーをサポートするようになり、スロークエリビュー、DB監査ログ、および`INFORMATION_SCHEMA.PROCESSLIST`テーブルで、ロードバランサー（LB）のIPアドレスではなく、実際のクライアントIPアドレスを表示できるようになりました。この機能により、データベースリクエストの真の発生源を正確に特定し、トラブルシューティングと分析を改善できます。

        現在、この機能はベータ版であり、AWSリージョン`Frankfurt (eu-central-1)`でのみ利用可能です。

**コンソールの変更**

-   プランに応じたサポートオプションで、サポート体験を向上させましょう。

    [TiDB Cloudコンソール](https://tidbcloud.com/)では、すべてのサブスクリプションプランでサポート体験を向上させるため、プランに応じたサポートオプションが提供されるようになりました。これらのアップデートには以下が含まれます。

    -   **プランに応じたサポートのリダイレクト**：クラスタ概要ページで、 **[アクション]**列の**[サポートを受ける]**を選択すると、サブスクリプションプランに基づいて最も適切なリソースにリダイレクトされます。ベーシックプランのユーザーは**サポートプラン**パネルに、有料プランのユーザーは**サポートポータル**に誘導されます。
    -   **ヘルプセンターメニューの改善**：ヘルプメニュー項目名を**「サポートオプション」**と**「サポートチケット」**に変更し、利用可能なサービスをより適切に反映させます。また、有料プランでのみテクニカルサポートチケットが利用できることを明確にするツールチップを追加します。
    -   **明確なコミュニティサポートへのアクセス**：**サポートプランの**オプション内で、SlackとDiscordがベーシックプランユーザーの主要なテクニカルサポートチャネルとして明確に示されています。サポートチャネルのポリシーとコミュニティへのアクセスを明確にするために、以下のドキュメントが簡潔化されています： [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) [コネクテッドケアの概要](/tidb-cloud/connected-care-overview.md)および[コネクテッドケアの詳細](/tidb-cloud/connected-care-detail.md) 。
    -   **アクション指向のサポートプランUI** ：**サポートプラン**ウィンドウを再設計し、一般的なプラン比較ではなく、現在ご利用のプランで利用可能なサポートオプションを優先的に表示するようにしました。この変更により、現在ご利用のプランに基づいてサポートを受ける方法をすばやく特定できます。

    詳細については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)参照してください。

## 2026年1月15日 {#january-15-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   新規クラスター[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のデフォルトのTiDBバージョンを[v8.5.4](https://docs.pingcap.com/tidb/stable/release-8.5.4/)から[v8.5.5](https://docs.pingcap.com/tidb/stable/release-8.5.5/)にアップグレードします。
