---
title: TiDB Cloud Release Notes in 2026
summary: 2026 年のTiDB Cloudのリリース ノートについて説明します。
aliases: ['/ja/tidbcloud/supported-tidb-versions','/ja/tidbcloud/release-notes']
---

# 2026年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2026}

このページには、2026 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2026年2月10日 {#february-10-2026}

**一般的な変更**

-   **TiDB Cloudスターター**

    -   新しい[TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.6](https://docs.pingcap.com/tidb/stable/release-7.5.6)から[バージョン8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3)にアップグレードします。

-   **TiDB Cloudエッセンシャル**

    -   組み込みアラートをサポートします。

        組み込みのアラート機能により、メール、Slack、Zoom、Flashduty、PagerDuty を通じて即時アラートを受信できます。また、アラートの種類ごとに特定のしきい値を定義して、アラートをカスタマイズすることもできます。

        詳細については[TiDB Cloud組み込みアラート](https://docs.pingcap.com/tidbcloud/monitor-built-in-alerting/?plan=essential)参照してください。

-   **TiDB Cloud専用**

    -   Azure Blob Storage からのデータ インポート用の Private Link 接続をサポートします。

        Azure Blob Storageから[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターにデータをインポートする際、接続方法として「Private Link」を選択できるようになりました。これにより、パブリックインターネットではなくAzureプライベートエンドポイント経由で接続できます。この機能により、パブリックアクセスが制限されているstorageアカウントでも、ネットワークから分離された安全なデータインポートが可能になります。

        詳細については、 [Cloud Storage からサンプルデータ (SQL ファイル) をインポートする](/tidb-cloud/import-sample-data.md) 、 [クラウドストレージからCSVファイルをインポートする](/tidb-cloud/import-csv-files.md) 、 [Cloud Storage から Apache Parquet ファイルをインポートする](/tidb-cloud/import-parquet-files.md)を参照してください。

    -   セキュリティ追跡を強化するために、 TiDB Cloudのコンソール監査ログに「パブリック エンドポイントの有効化/無効化」イベントを追加します。

## 2026年2月3日 {#february-3-2026}

**一般的な変更**

-   **TiDB Cloud専用**

    -   Azure Blob Storage への変更フィード データのシンクをサポートします。

        [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)では、Azure Blob Storageへの変更フィードデータの直接シンクがサポートされるようになりました。この機能により、Azureユーザーは変更データを効率的にアーカイブし、下流の分析や長期保存に活用できるようになります。また、中間メッセージキューが不要になるためコスト削減にもつながり、既存のAmazon S3およびGoogle Cloud Storage (GCS)シンクとのフォーマット互換性も維持されます。

        詳細については[クラウドストレージに保存](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

## 2026年1月27日 {#january-27-2026}

**一般的な変更**

-   **TiDB Cloud専用**

    -   アラートサブスクリプションチャネルとして Flashduty と PagerDuty をサポートします。

        これらの統合は、インシデント管理プロセスを合理化し、運用の信頼性を向上させるように設計されています。

        詳細については、 [Flashdutyで購読する](/tidb-cloud/monitor-alert-flashduty.md)および[PagerDuty経由で購読する](/tidb-cloud/monitor-alert-pagerduty.md)を参照してください。

## 2026年1月20日 {#january-20-2026}

**一般的な変更**

-   **TiDB Cloudスターター**

    -   実際のクライアント IP アドレスを[遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ビューと[`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)テーブル (ベータ版) に表示します。

        TiDB Cloud はクライアント IP パススルーをサポートしました。これにより、スロークエリビューと`INFORMATION_SCHEMA.PROCESSLIST`テーブルに、ロードバランサー (LB) IP ではなく実際のクライアント IP アドレスが表示されるようになりました。この機能により、データベースリクエストの実際の送信元を正確に特定し、トラブルシューティングと分析の精度が向上します。

        現在、この機能はベータ版であり、AWS リージョン`Frankfurt (eu-central-1)`でのみ利用できます。

-   **TiDB Cloudエッセンシャル**

    -   データ移行をサポートします（ベータ版）。

        これで、 [TiDB Cloudコンソール](https://tidbcloud.com)データ移行機能を使用して、MySQL 互換データベースから[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターにデータをシームレスに移行できるようになりました。

        -   サポートされているソース データベースには、セルフホスト MySQL、Amazon RDS、Alibaba Cloud RDS、PolarDB など、さまざまな MySQL 互換システムが含まれます。
        -   データ移行にサポートされている接続方法には、使いやすさとエンタープライズ レベルのセキュリティの両方を保証するパブリック接続と PrivateLink が含まれます。

            -   **パブリック接続**: 安全で暗号化されたチャネルを使用して、インターネット経由でソース データベースにすばやく接続します。
            -   **PrivateLink** : ソース VPC とTiDB Cloudの間に安全でプライベートな接続を確立し、パブリック インターネットをバイパスして、データのプライバシーを最大限に高め、ネットワークレイテンシーを削減します。

        現在、データ移行機能は論理モードのみをサポートしています。

        詳細については、 [データ移行を使用して既存データと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)および[データ移行を使用して増分データを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)を参照してください。

    -   [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ビュー、 [DB監査ログ](/tidb-cloud/essential-database-audit-logging.md)テーブルに実際のクライアント IP アドレスを表示します ( [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)版)

        TiDB Cloud はクライアント IP パススルーをサポートしました。これにより、スロークエリビュー、DB 監査ログ、および`INFORMATION_SCHEMA.PROCESSLIST`テーブルで、ロードバランサー (LB) IP ではなく実際のクライアント IP アドレスを表示できるようになりました。この機能により、データベースリクエストの実際の送信元を正確に特定し、トラブルシューティングと分析の精度が向上します。

        現在、この機能はベータ版であり、AWS リージョン`Frankfurt (eu-central-1)`でのみ利用できます。

**コンソールの変更**

-   プランに対応したサポート オプションでサポート エクスペリエンスを向上します。

    [TiDB Cloudコンソール](https://tidbcloud.com/)では、すべてのサブスクリプションプランでサポートエクスペリエンスを向上させるため、プランに応じたサポートオプションを追加しました。これらのアップデートには以下の内容が含まれます。

    -   **プランに応じたサポートリダイレクト**：クラスター概要ページの**「アクション」**列で**「サポートを受ける」**を選択すると、サブスクリプションプランに基づいて最も関連性の高いリソースにリダイレクトされます。ベーシックプランのユーザーは**「サポートプラン」**パネルに、有料プランのユーザーは「**サポートポータル」**にリダイレクトされます。
    -   **ヘルプセンターメニューの改良**：利用可能なサービスをより適切に反映するため、ヘルプメニュー項目の名前を**「サポートオプション」**と**「サポートチケット」**に変更しました。テクニカルサポートチケットは有料プランでのみ利用可能であることを明確に示すツールチップを追加しました。
    -   **明確なコミュニティサポートへのアクセス**：**サポートプランの**オプションでは、SlackとDiscordがベーシックプランユーザーの主要なテクニカルサポートチャネルとして明確に示されています。サポートチャネルのポリシーとコミュニティへのアクセスを明確にするために[コネクテッドケアの概要](/tidb-cloud/connected-care-overview.md)以下のドキュメントが簡素化されています： [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) [コネクテッドケアの詳細](/tidb-cloud/connected-care-detail.md)
    -   **アクション指向のサポートプランUI** ：**サポートプラン**ウィンドウのデザインを刷新し、一般的なプラン比較ではなく、現在のサブスクリプションで利用可能なサポートオプションを優先的に表示します。この変更により、アクティブなプランに基づいてサポートを受ける方法を素早く特定できるようになります。

    詳細については[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)参照してください。

## 2026年1月15日 {#january-15-2026}

**一般的な変更**

-   **TiDB Cloud専用**

    -   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン8.5.4](https://docs.pingcap.com/tidb/stable/release-8.5.4/)から[バージョン8.5.5](https://docs.pingcap.com/tidb/stable/release-8.5.5/)にアップグレードします。
