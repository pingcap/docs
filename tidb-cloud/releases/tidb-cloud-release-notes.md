---
title: TiDB Cloud Release Notes in 2026
summary: TiDB Cloudの2026年のリリースノートについてご確認ください。
aliases: ['/ja/tidbcloud/supported-tidb-versions','/ja/tidbcloud/release-notes']
---

# TiDB Cloud 2026年のリリースノート {#tidb-cloud-release-notes-in-2026}

このページには、2026年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリースノートが掲載されています。

## 2026年4月8日 {#april-8-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタにおけるクラウドstorageデータのインポートエクスペリエンスを向上させます。

        インポートプロセスは、接続、宛先マッピング、事前チェックの3ステップウィザードに簡素化され、Amazon S3、Google Cloud Storage、Azure Blob Storageに対応した**クラウドストレージからのデータインポートの**エントリポイントが統一されました。新しいフローでは、単一ファイルURIとワイルドカードパターンによる手動ファイルマッピングがサポートされ、事前チェックステップではインポート実行前にソースファイルをスキャンしてマッピングをプレビューするため、構成上の問題を早期に発見し、インポートの失敗を減らすことができます。

        詳細については、以下の資料を参照してください。

        -   [クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)
        -   [クラウドストレージからTiDB Cloud DedicatedにApache Parquetファイルをインポートする](/tidb-cloud/import-parquet-files.md)

## 2026年3月31日 {#march-31-2026}

**全般的な変更**

-   **TiDB Cloud Essential**

    -   プライベートエンドポイントの許可リストの設定をサポートします。

        [TiDB Cloudコンソール](https://tidbcloud.com)で許可リストを設定することで、プライベートエンドポイントへのアクセスをより簡単に保護および管理できるようになりました。 許可リストでは、接続を許可するAWS VPCエンドポイントIDとAlibaba CloudエンドポイントIDを指定できます。

        詳細については、以下の資料を参照してください。

        -   [AWS のプライベートエンドポイント経由で接続します](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
        -   [Alibaba Cloudとプライベートエンドポイント経由で接続](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

    -   Prometheusメトリクス統合を有効にする（プレビュー）。

        [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)クラスターレベルでPrometheusとの連携を管理します。この機能により、 TiDB Cloud EssentialクラスターからPrometheusへメトリクスをシームレスに送信でき、統合プラットフォーム上で高度なアラート機能を実現できます。

        統合手順については、 [TiDB CloudをPrometheusおよびGrafanaと統合する](/tidb-cloud/prometheus-grafana-integration.md)参照してください。

## 2026年3月24日 {#march-24-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   セキュリティ追跡を改善するために、 TiDB Cloudの [コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)に**パブリック エンドポイント**ステータスを追加します。

**コンソールの変更**

-   値のばらつきが大きい指標の視覚化を向上させるため、対数Y軸をサポートします。高値域と低値域の変動が明確に表示されるため、異常値を特定しやすくなります。

## 2026年3月10日 {#march-10-2026}

**全般的な変更**

-   **TiDB Cloud Essential**

    -   データフローシナリオにおけるプライベートリンク接続でのAmazon MSK Provisionedをサポートします。

        [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 、 [Amazon MSK プロビジョニング済み](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html)クラスターへのプライベート リンク接続の作成をサポートするようになりました。この機能により、トラフィックを公共のインターネットに公開することなく、Amazon MSK プロビジョニングされたクラスターへの変更フィードのプライベート ネットワーク接続が可能になります。

        詳細については、 [プライベートリンク接続を介してAmazon MSK Provisionedに接続します](/tidb-cloud/serverless-private-link-connection-to-amazon-msk.md)参照してください。

## 2026年3月3日 {#march-3-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   Amazon S3シンクの変更フィードは、認証にAWSロールARNを使用することをサポートしています。

        [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでは、既存の AK/SK 認証方法に加え、 IAMロール ARN を使用して Amazon S3 シンクの変更フィードを設定できるようになりました。この機能により、有効期限の短い認証情報と自動ローテーションが可能になり、セキュリティが強化されるとともに、シークレット管理が簡素化され、最小権限の原則がサポートされます。

        詳細については、 [クラウドストレージへのシンク](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

    -   TiKVおよびTiFlashのstorage使用量計算を改善します。

        メトリクスおよびアラートシステムにおけるTiKVおよびTiFlashstorage使用量の計算に、WALファイルと一時ファイルが組み込まれるようになり、より正確な容量および使用状況の監視が可能になりました。

        詳細については、 [TiDB Cloud の組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)を参照してください。

## 2026年2月10日 {#february-10-2026}

**全般的な変更**

-   **TiDB Cloud Starter**

    -   新しい[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)クラスターのデフォルトの TiDB バージョンを[v7.5.6](https://docs.pingcap.com/tidb/stable/release-7.5.6)から[v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3)にアップグレードします。

-   **TiDB Cloud Essential**

    -   組み込みアラート機能をサポートします。

        組み込みのアラート機能を使用すると、メール、Slack、Zoom、Flashduty、PagerDutyを通じて即座にアラートを受信できます。また、アラートの種類ごとに特定のしきい値を定義することで、アラートをカスタマイズすることも可能です。

        詳細については、 [TiDB Cloudの組み込みアラート機能](https://docs.pingcap.com/tidbcloud/monitor-built-in-alerting/?plan=essential)を参照してください。

-   **TiDB Cloud Dedicated**

    -   Azure Blob Storageからのデータインポートにおけるプライベートリンク接続をサポートします。

        Azure Blob Storage から[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターにデータをインポートする際、接続方法としてプライベートリンクを選択し、パブリックインターネットではなく Azure プライベートエンドポイント経由で接続できるようになりました。この機能により、パブリックアクセスが制限されているstorageアカウントに対して、安全でネットワーク分離されたデータインポートが可能になります。

        詳細については、[クラウドストレージからサンプルデータ（SQLファイル）をインポートする](/tidb-cloud/import-sample-data.md)[クラウドストレージからCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)[クラウドストレージからApache Parquetファイルをインポートする](/tidb-cloud/import-parquet-files.md)参照してください。

    -   セキュリティ追跡を強化するため、 TiDB Cloudのコンソール監査ログに「パブリックエンドポイントの有効化/無効化」イベントを追加します。

## 2026年2月3日 {#february-3-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   変更フィードデータをAzure Blob Storageにシンクすることをサポートします。

        [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 、変更フィードデータをAzure Blob Storageに直接保存する機能をサポートするようになりました。この機能により、Azureベースのユーザーは、変更データを効率的にアーカイブして、下流の分析や長期保存に活用できます。また、中間メッセージキューが不要になるためコスト削減にもつながり、既存のAmazon S3およびGoogle Cloud Storage（GCS）シンクとのフォーマット互換性も維持されます。

        詳細については、 [クラウドストレージへのシンク](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

## 2026年1月27日 {#january-27-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   FlashDutyとPagerDutyをアラート購読チャネルとしてサポートします。

        これらの統合機能は、インシデント管理プロセスを効率化し、運用上の信頼性を向上させるように設計されています。

        詳細については、 [Flashduty経由で購読する](/tidb-cloud/monitor-alert-flashduty.md)および[PagerDuty経由で購読する](/tidb-cloud/monitor-alert-pagerduty.md)を参照してください。

## 2026年1月20日 {#january-20-2026}

**全般的な変更**

-   **TiDB Cloud Starter**

    -   実際のクライアント IP アドレスを [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)と[`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)テーブル (ベータ版) に表示します。

        TiDB CloudはクライアントIPパススルーをサポートするようになり、スロークエリビューと`INFORMATION_SCHEMA.PROCESSLIST`テーブルで、ロードバランサー（LB）のIPアドレスではなく、実際のクライアントIPアドレスを表示できるようになりました。この機能により、データベースリクエストの真の送信元を正確に特定し、トラブルシューティングと分析を改善できます。

        現在、この機能はベータ版であり、AWSリージョン`Frankfurt (eu-central-1)`でのみ利用可能です。

-   **TiDB Cloud Essential**

    -   データ移行をサポートします（ベータ版）。

        [TiDB Cloudコンソール](https://tidbcloud.com)のデータ移行機能を使用すると、MySQL 互換データベースから[TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)クラスターへデータをシームレスに移行できます。

        -   サポートされているソースデータベースには、セルフホスト型MySQL、Amazon RDS、Alibaba Cloud RDS、PolarDBなど、さまざまなMySQL互換システムが含まれます。
        -   データ移行にサポートされている接続方法には、使いやすさとエンタープライズグレードのセキュリティの両方を確保するために、パブリック接続とPrivateLinkが含まれます。

            -   **パブリック接続**：安全で暗号化されたチャネルを使用して、インターネット経由でソースデータベースに迅速に接続します。
            -   **PrivateLink** ：ソースVPCとTiDB Cloud間の安全でプライベートな接続を確立し、パブリックインターネットをバイパスすることで、最大限のデータプライバシーとネットワークレイテンシーの低減を実現します。

        現在、データ移行機能は論理モードのみをサポートしています。

        詳細については、 [データ移行を使用して既存データと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)[データ移行を使用して増分データを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)を参照してください。

    -   [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)監査、および[`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)テーブル (ベータ版) に実際のクライアント IP アドレスを表示します[DB監査ログ](/tidb-cloud/essential-database-audit-logging.md)

        TiDB CloudはクライアントIPパススルーをサポートするようになり、スロークエリビュー、DB監査ログ、および`INFORMATION_SCHEMA.PROCESSLIST`テーブルで、ロードバランサー（LB）のIPアドレスではなく、実際のクライアントIPアドレスを表示できるようになりました。この機能により、データベースリクエストの真の発生源を正確に特定し、トラブルシューティングと分析を改善できます。

        現在、この機能はベータ版であり、AWSリージョン`Frankfurt (eu-central-1)`でのみ利用可能です。

**コンソールの変更**

-   プランに応じたサポートオプションで、サポート体験を向上させましょう。

    [TiDB Cloudコンソール](https://tidbcloud.com/)すべてのサブスクリプションプランにおいてサポート体験を向上させるため、プランに応じたサポートオプションを提供開始しました。これらのアップデートには以下が含まれます。

    -   **プランに応じたサポートのリダイレクト**：クラスタ概要ページで、 **[アクション]**列の**[サポートを受ける]**を選択すると、サブスクリプションプランに基づいて最も適切なリソースにリダイレクトされます。ベーシックプランのユーザーは**サポートプラン**パネルに、有料プランのユーザーは**サポートポータル**に誘導されます。
    -   **ヘルプセンターメニューの改善**：ヘルプメニュー項目名を**「サポートオプション」**と**「サポートチケット」**に変更し、利用可能なサービスをより適切に反映させます。また、有料プランでのみテクニカルサポートチケットが利用できることを明確にするツールチップを追加します。
    -   **明確なコミュニティ サポート アクセス**:**サポート プラン**オプション内では、Slack と Discord がベーシック プラン ユーザーの主要なテクニカル サポート チャネルとして明確に識別されます。次のドキュメントは、サポート チャネル ポリシーとコミュニティ アクセスを明確にするために合理化されています: [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)、[コネクテッドケアの概要](/tidb-cloud/connected-care-overview.md)、および[コネクテッドケアの詳細](/tidb-cloud/connected-care-detail.md)。
    -   **アクション指向のサポートプランUI** ：**サポートプラン**ウィンドウを再設計し、一般的なプラン比較ではなく、現在ご利用のプランで利用可能なサポートオプションを優先的に表示するようにしました。この変更により、現在ご利用のプランに基づいてサポートを受ける方法をすばやく特定できます。

    詳細については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)を参照してください。

## 2026年1月15日 {#january-15-2026}

**全般的な変更**

-   **TiDB Cloud Dedicated**

    -   新しい[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[v8.5.4](https://docs.pingcap.com/tidb/stable/release-8.5.4/)から[v8.5.5](https://docs.pingcap.com/tidb/stable/release-8.5.5/)にアップグレードします。
