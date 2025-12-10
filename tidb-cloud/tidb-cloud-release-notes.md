---
title: TiDB Cloud Release Notes in 2025
summary: 2025 年のTiDB Cloudのリリース ノートについて説明します。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2025年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2025}

このページには、2025 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2025年12月9日 {#december-9-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/)から[バージョン8.5.4](https://docs.pingcap.com/tidb/v8.5/release-8.5.4/)にアップグレードします。

**コンソールの変更**

-   **TiDB Cloud Starter とTiDB Cloud Essential**

    -   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)および[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターのクラスター レベルで**統合された統合**ページを追加します。

        -   クラスターの**「統合」**ページで、すべてのサードパーティ統合を統合します。以下のリストは、ユースケース別にまとめたこれらの統合の概要です。
            -   **デプロイ**: AWS Lambda、Cloudflare Workers、Gitpod、Netlify、Terraform、WordPress
            -   **データ**: Airbyte、Amazon AppFlow、dbt Labs、Looker Studio、n8n、Zapier
            -   **GUI** : DBeaver、JetBrains DataGrip、MySQL Workbench、Navicat、ProxySQL、Visual Studio Code
            -   **Java** : JDBC、Hibernate、MyBatis、Spring Boot
            -   **Go** : Go-MySQL-Driver、GORM
            -   **Python** : Django、mysqlclient、MySQL Connector/Python、peewee、PyMySQL、SQLAlchemy
            -   **Node.js** : mysql.js、Next.js、node-mysql2、Prisma、Sequelize、TypeORM
            -   **Ruby** : mysql2、Rails
        -   検出可能性を向上させるために、統合エントリ[ヴェルセル](/tidb-cloud/integrate-tidbcloud-with-vercel.md)と[AWS ベッドロック](/tidb-cloud/vector-search-integrate-with-amazon-bedrock.md)クラスター レベルに移動します。
        -   新しい統合をリクエストするための**「統合の提案」**を追加します。

**APIの変更**

-   TiDB Cloud IAM API (v1beta1) は、コンソール監査ログの一覧表示をサポートしています。

    [監査ログの一覧表示](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam/#tag/Audit-Log/paths/~1auditLogs/get)エンドポイントは、コンソール監査ログへのプログラムによるアクセスを提供します。このエンドポイントを使用することで、監査ログを自動的に取得し、セキュリティとコンプライアンスの要件を満たすために定期的なバックアップをスケジュールできます。

    詳細については[TiDB CloudIAM API](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam/)参照してください。

## 2025年12月2日 {#december-2-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   Prometheus 統合は現在、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して一般提供 (GA) されています。

        TiDB Cloudは、Prometheusとの連携をクラスターレベルで管理するようになり、よりきめ細かな制御と設定が可能になります。この機能により、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのメトリクスをシームレスにPrometheusに送信できるようになり、統合プラットフォームで高度なアラート機能を実現できます。

        統合手順については、 [TiDB Cloud をPrometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)参照してください。

        既存の Prometheus 統合をクラスター レベルに移行するには、 [Prometheus統合の移行](/tidb-cloud/migrate-prometheus-metrics-integrations.md)参照してください。

## 2025年11月18日 {#november-18-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   完全な構成の詳細を含めるように変更フィードの概要を拡張します。

        以前は、変更フィードを一時停止して設定を確認し、再開する必要がありました。**変更フィード**ページでは、サマリービューに完全な設定が直接表示されるようになりました。今回のアップデートでは、編集モードと表示モードの一貫性を維持し、レイアウトを再設計して読みやすさを向上させました。これにより、現在の設定をより効率的に確認できます。

        詳細については[チェンジフィードの概要](/tidb-cloud/changefeed-overview.md)参照してください。

## 2025年11月11日 {#november-11-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   バックアップから[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを新しいクラスターに復元するときに、デフォルトのstorageタイプを使用する代わりに、 [標準storage](/tidb-cloud/size-your-cluster.md#standard-storage)などの新しいクラスターのノードstorageタイプを選択できるようになりました。

        この機能を使用すると、元の構成を正確に復元するか、ニーズに合った別のstorageタイプを選択できます。

        詳細については[新しいクラスターにデータを復元する](/tidb-cloud/backup-and-restore.md#restore-data-to-a-new-cluster)参照してください。

## 2025年11月4日 {#november-4-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   Google Cloud でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに VPC ピアリング経由で接続する場合、 [TiDB Cloudコンソール](https://tidbcloud.com/)で`/16` ～ `/18` IP 範囲サイズを直接設定できるようになりました。この設定についてTiDB Cloudサポートに連絡する必要がなくなりました。

        詳細については[VPC ピアリング経由でTiDB Cloud Dedicated に接続する](/tidb-cloud/set-up-vpc-peering-connections.md)参照してください。

    -   TiDB Cloud Dedicated では、4 vCPU ノードサイズに関するガイダンスとメッセージがより明確になりました。このノードサイズは、非本番環境でのTiDB Cloud機能のテスト、学習、および探索にのみ使用してください。

        詳細については[TiDBのサイズを決定する](/tidb-cloud/size-your-cluster.md)参照してください。

## 2025年10月28日 {#october-28-2025}

**一般的な変更**

-   **TiDB Cloud Starter とTiDB Cloud Essential**

    接続の安定性を向上させ、TiDBサーバーの再起動またはメンテナンス中に予期しない切断を防ぐには、データベース接続の最大有効期間を 30 分未満に設定することをお勧めします。

    詳細については[接続の有効期間を設定する](/develop/dev-guide-connection-parameters.md#configure-the-lifetime-of-connections)参照してください。

**APIの変更**

-   **TiDB Cloud専用**

    サードパーティの監視統合を管理するための次の[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) API エンドポイントを導入します。

    -   統合の一覧
    -   統合を作成する
    -   統合を削除する

    詳細については[TiDB Cloud専用API](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated/)参照してください。

## 2025年10月21日 {#october-21-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)では、 [チェンジフィード](/tidb-cloud/changefeed-overview.md)プライベート エンドポイント機能が強化され、構成が簡素化され、セキュリティが向上し、データ シンクの柔軟性が向上します。

        -   **簡素化された構成**: プライベート エンドポイントの作成が変更フィードの作成から独立し、同じプロジェクト内の複数の変更フィードが単一のプライベート エンドポイントを共有できるようになり、冗長な構成が削減されます。
        -   **MySQL のプライベート リンク シンク**: MySQL にデータをシンクするためのより安全な方法を提供し、プライベート リンク経由で別のTiDB Cloud Dedicated クラスターにデータを直接シンクすることもサポートするようになりました。
        -   **カスタム ドメインのサポート**: セルフホスト型 Kafka サービスを使用する場合、データ シンクのカスタム ドメインを構成して、セキュリティを強化し、サーバーの再起動を必要とせずに、アドバタイズされたリスナーの更新をより柔軟に行うことができます。

        詳細については[Changefeeds のプライベート エンドポイントを設定する](/tidb-cloud/set-up-sink-private-endpoint.md)参照してください。

    -   現在、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して[Prometheus 統合（プレビュー）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)が使用可能です。

        TiDB Cloudは、Prometheusとの連携をクラスターレベルで管理するようになり、よりきめ細かな制御と設定が可能になります。この機能により、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのメトリクスをシームレスにPrometheusに送信できるようになり、統合プラットフォームで高度なアラート機能を実現できます。

        詳細については[TiDB Cloud をPrometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)参照してください。

## 2025年10月14日 {#october-14-2025}

**一般的な変更**

-   **TiDB Cloudスターター**

    -   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)ではデータベース監査ログはサポートされなくなりました。

        現在、データベース監査ログをサポートしているのは[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)と[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のみです。データベース監査ログを使用している既存のTiDB Cloud Starter クラスターには影響しません。

    -   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)インプレースリストア機能が削除され、バックアップを同じクラスタに直接リストアできなくなります。この変更により、アクティブな本番本番データの誤った上書きや潜在的なデータ損失を防ぐことができます。

        データを復元するには、 [バックアップを新しいクラスターに復元する](/tidb-cloud/backup-and-restore-serverless.md#perform-the-restore) . 復元されたデータを検証した後、アプリケーションを新しいクラスターに切り替えます。既存のクラスターに復元されたデータはそのまま残り、新たな復元を実行しない限り、何もする必要はありません。

        より安全で制御性と柔軟性に優れた復元および移行ワークフローを実現するには、 [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)使用を検討してください。

    -   [**メトリクス**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ[TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)では、より迅速な診断と容量計画のために次のメトリックが追加されます。

        -   `Lock-wait (P95/P99)` : ロック待機時間のパーセンタイルを監視して競合ホットスポットを表面化させます。
        -   `Idle Connection Duration (P99 incl. not/in txn)` : プーラーの制限とタイムアウトを調整するために、トランザクション中とトランザクション外での長時間アイドル状態の接続を識別します。

-   **TiDB Cloudエッセンシャル**

    -   [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)はAWSでパブリックプレビュー中です<customcontent language="en,zh">アリババクラウド</customcontent>。

        ワークロードが増加し、リアルタイムの拡張性を必要とするアプリケーションに対して、 TiDB Cloud Essential はビジネスの成長に対応できる柔軟性とパフォーマンスを提供します。

        <CustomContent language="en,zh">

        詳細については[TiDB Cloud Essential が AWS と Alibaba Cloud でパブリックプレビューとして利用可能になりました](https://www.pingcap.com/blog/tidb-cloud-essential-now-available-public-preview-aws-alibaba-cloud/)参照してください。

        </CustomContent>

    -   データベース監査ログがTiDB Cloud Essential [TiDB Cloudコンソール](https://tidbcloud.com)で利用できるようになりました。また、ローテーション設定のカスタマイズもサポートされます。

        データベース監査ログをTiDB Cloud、Amazon S3、Google Cloud Storage、Azure Blob Storage、または Alibaba Cloud OSS に保存するように構成できます。

        現在、この機能はベータ版です。詳細については、 [TiDB Cloud Essential のデータベース監査ログ](/tidb-cloud/essential-database-audit-logging.md)ご覧ください。

    -   TiDB Cloud Essential では、クラスターのリクエスト容量単位 (RCU) 消費量が 1 時間以内に設定された最大値に複数回達したときに通知する新しいイベント`ResourceLimitation`が追加されました。

        使用量の上限を超えると、処理能力が制限される可能性があります。サービスへの影響を避けるため、最大RCUを増やすことをご検討ください。

        イベントの詳細については、 [TiDB Cloudクラスタイベント](/tidb-cloud/tidb-cloud-events.md)参照してください。

    -   [**メトリクス**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)では、より迅速な診断と容量計画のために次のメトリックが追加されます。

        -   `Capacity vs Usage (RU/s)` : プロビジョニングされたリクエスト ユニット (RU) 容量と実際の RU 消費量を視覚化して、余裕を見つけて自動スケーリングを調整します。
        -   `Lock-wait (P95/P99)` : ロック待機時間のパーセンタイルを監視して競合ホットスポットを表面化させます。
        -   `Idle Connection Duration (P99 incl. not/in txn)` : プーラーの制限とタイムアウトを調整するために、トランザクション中とトランザクション外での長時間アイドル状態の接続を識別します。

        詳細については[TiDB Cloud組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)参照してください。

## 2025年9月30日 {#september-30-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   Datadog と New Relic の統合が[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して一般提供 (GA) されました。

        TiDB Cloudは、DatadogとNew Relicの連携をクラスターレベルで管理できるようになり、よりきめ細かな制御と設定が可能になります。この機能により、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのメトリクスをDatadogまたはNew Relicにシームレスに送信できるようになり、統合プラットフォームで高度なアラート機能を実現できます。

        統合手順については、 [TiDB CloudとDatadogの統合](/tidb-cloud/monitor-datadog-integration.md)と[TiDB CloudとNew Relicの統合](/tidb-cloud/monitor-new-relic-integration.md)を参照してください。

        既存の Datadog と New Relic の統合をクラスター レベルに移行するには、 [DatadogとNew Relicの統合の移行](/tidb-cloud/migrate-metrics-integrations.md)参照してください。

## 2025年9月23日 {#september-23-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   `UPDATE`イベントを[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)変更フィードに分割するユーザー制御をサポートします。

        TiDB Cloud Dedicated クラスターでは、 `UPDATE`イベントを生イベントとして保持するか、 `DELETE`と`INSERT`イベントに分割するかを設定できます。この機能により、高度なレプリケーションシナリオにおいて柔軟性が向上します。

        この機能は[クラウドストレージに保存](/tidb-cloud/changefeed-sink-to-cloud-storage.md) [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md) [アパッチパルサーに沈む](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)てください。

        分割動作の詳細については、 [MySQL以外のシンクの主キーまたは一意キーの`UPDATE`イベントを分割する](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)参照してください。

    -   Google Cloud でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに新しいノード サイズ`32 vCPU, 64 GiB`指定します。

        この新しいノード サイズは、TiDB ノードで使用できます。

## 2025年9月16日 {#september-16-2025}

**一般的な変更**

-   **TiDB Cloud専用**

    -   顧客管理の暗号化キー (CMEK) を使用した保存時の暗号化は、 Azure でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで利用できます。

        この機能により、ユーザーが管理する暗号化キーを使用して、保存データを保護できます。CMEK には次のような利点があります。

        -   データ セキュリティ: 暗号化キーを所有および管理することで、データが保護され、制御されることが保証されます。
        -   コンプライアンス: CMEK を使用すると、データ暗号化に関する規制およびコンプライアンスの要件を満たすことができます。
        -   柔軟性: プロジェクトを作成するときに CMEK を有効にし、クラスタを作成する前に CMEK 構成を完了できます。

        この機能を有効にするには、次の手順を実行します。

        1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、CMEK 対応プロジェクトを作成します。
        2.  プロジェクトの CMEK 構成を完了します。
        3.  CMEK 構成と同じリージョンの Azure でホストされるTiDB Cloud Dedicated クラスターを作成します。

        詳細については[Azure での顧客管理の暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md)参照してください。

## 2025年9月9日 {#september-9-2025}

**高可用性の変更**

-   **TiDB Cloudスターター**

    -   新しく作成された[TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)クラスターでは、ゾーン高可用性のみが有効になっており、構成することはできません。
    -   **2025 年 9 月 9 日**より前にリージョン高可用性が有効にされた既存のTiDB Cloud Starter クラスターの場合、リージョン高可用性は引き続きサポートされ、影響を受けません。

<CustomContent language="en,zh">

-   **TiDB Cloudエッセンシャル**

    -   新しく作成された[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターでは、リージョン高可用性がデフォルトで有効になっており、クラスターの作成時に必要に応じてゾーン高可用性に変更できます。

    詳細については[TiDB Cloud StarterとEssentialの高可用性](/tidb-cloud/serverless-high-availability.md)参照してください。

</CustomContent>

## 2025年9月2日 {#september-2-2025}

**一般的な変更**

<CustomContent language="en,zh">

-   **TiDB Cloudエッセンシャル**

    -   [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターに対して`Jakarta (ap-southeast-5)` `Mexico (na-south-1)` 3 つの新しい Alibaba Cloud リージョン`Tokyo (ap-northeast-1)`サポートします。

-   **TiDB Cloud専用**

    -   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2/)から[バージョン8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/)にアップグレードします。

</CustomContent>

<CustomContent language="ja">

-   **TiDB Cloud専用**

    -   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2/)から[バージョン8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/)にアップグレードします。

</CustomContent>

## 2025年8月26日 {#august-26-2025}

**一般的な変更**

-   **TiDB Cloudスターター**

    -   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)で自動埋め込み（ベータ版）を導入しました。これにより、追加の設定なしでテキストをベクターに変換するのが簡単になります。この機能により、TiDB Cloudにおけるセマンティック検索、RAG、リランキング、分類の開発を、統合オーバーヘッドの削減と迅速化の両方で実現できます。

        -   **人気の LLM プロバイダーによる自動埋め込み**: Amazon Titan、OpenAI、Cohere、Gemini、Jina AI、Hugging Face、NVIDIA NIM。
        -   **AWS Bedrock とのネイティブ統合**: AWS Bedrock の Amazon Titan および Cohere テキスト埋め込みモデルを含む、無料クォータで管理される埋め込みモデル。
        -   **SQL および Python のサポート**、埋め込みの作成、保存、クエリのコード例。

        詳細については[自動埋め込み](https://docs.pingcap.com/tidbcloud/vector-search-auto-embedding-overview/?plan=starter)参照してください。

-   **TiDB Cloud専用**

    -   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)では Index Insight (ベータ) 機能はサポートされなくなりました。

        代わりに、TiDB v8.5.0 以降のバージョンで利用可能な[インデックスアドバイザー](/index-advisor.md)使用することをお勧めします。Index Advisor では`RECOMMEND INDEX` SQL ステートメントが導入されており、クエリのパフォーマンスを向上させるインデックスを推奨することで、ワークロードの最適化に役立ちます。

    -   週次バックアップが有効になっている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで、ポイントインタイム リストア機能を手動で無効にできるようになりました。

        この機能強化により、高 RPO 保護のためのポイントインタイム リストアを必要としないクラスターのコストが削減されます。

        詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

## 2025年8月12日 {#august-12-2025}

**一般的な変更**

<CustomContent language="en,zh">

-   **TiDB Cloudスターター**

    -   「TiDB Cloud Serverless」の名前を「TiDB Cloud Starter」に変更します。

        オートスケーリングのエントリープランは、新規ユーザーにとっての役割をより明確にするため、「TiDB Cloud Starter」に名称が変更されました。すべての機能、料金、無料利用枠に変更はありません。

        2025年8月12日（PDT）より、既存のサーバーレスクラスターは[TiDB Cloudコンソール](https://tidbcloud.com)にスターターとして表示されます。接続文字列、エンドポイント、データは変更されないため、コードを変更したり、ダウンタイムをスケジュールしたりする必要はありません。

    -   TiDB Cloud Starter は Alibaba Cloud でプレビュー中です。

-   **TiDB Cloudエッセンシャル**

    [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)は Alibaba Cloud でプレビュー中です。

    TiDB Cloud Essential on Alibaba Cloud は、2025年5月から限定公開プレビューを実施しています。Essential がリリースノートに公式に掲載されるのは今回が初めてです。現段階では、Essential on Alibaba Cloud は、Alibaba Cloud シンガポールリージョンで利用可能な Starter と同等の機能セットを提供しています。

    試す方法:

    -   [TiDB Cloudコンソール](https://tidbcloud.com/)から、クラスターを作成するときにクラウド プロバイダーとして Alibaba Cloud を選択して、Essential オプションを表示します。
    -   [Alibaba Cloud Marketplaceへの掲載](https://www.alibabacloud.com/en/marketplace/tidb?_p_lc=1)経由で Essential にアクセスすることもできます。

    今後は、Alibaba Cloud のリージョン カバレッジを拡大し、AWS サポートを追加する予定です。

    このプレビュー期間中に Essential on Alibaba Cloud をお試しいただくと、Web コンソールからフィードバックを共有したり、 [スラック](https://tidbcommunity.slack.com/archives/CH7TTLL7P)または[不和](https://discord.gg/ukhXbn69Nx)コミュニティに参加したりできます。

-   **TiDB Cloud専用**

    -   Google Cloud の .NET Framework [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)では、NAT サブネット割り当て戦略を最適化することで、リージョンごとに 8 個を超える Google Private Service Connect (PSC) 接続がサポートされるようになりました。

        詳細については[Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions)参照してください。

    -   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)指標を最適化:

        -   [**高度な**](/tidb-cloud/built-in-monitoring.md#advanced)カテゴリでは、**影響を受ける行**、**Leader数**、および**リージョン数の**メトリックを追加して診断を改善します。
        -   [**サーバ**](/tidb-cloud/built-in-monitoring.md#server)カテゴリでは、 **TiKV IO Bps**メトリックを改良して、精度と一貫性を向上させます。

        詳細については[TiDB Cloud組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)参照してください。

</CustomContent>

<CustomContent language="ja">

-   **TiDB Cloudスターター**

    「TiDB Cloud Serverless」の名前を「TiDB Cloud Starter」に変更します。

    オートスケーリングのエントリープランは、新規ユーザーにとっての役割をより明確にするため、「TiDB Cloud Starter」に名称が変更されました。すべての機能、料金、無料利用枠に変更はありません。

    2025年8月12日（PDT）より、既存のサーバーレスクラスターは[TiDB Cloudコンソール](https://tidbcloud.com)にスターターとして表示されます。接続文字列、エンドポイント、データは変更されないため、コードを変更したり、ダウンタイムをスケジュールしたりする必要はありません。

-   **TiDB Cloud専用**

    -   Google Cloud の .NET Framework [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)では、NAT サブネット割り当て戦略を最適化することで、リージョンごとに 8 個を超える Google Private Service Connect (PSC) 接続がサポートされるようになりました。

        詳細については[Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions)参照してください。

    -   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)指標を最適化:

        -   [**高度な**](/tidb-cloud/built-in-monitoring.md#advanced)カテゴリでは、**影響を受ける行**、**Leader数**、および**リージョン数の**メトリックを追加して診断を改善します。
        -   [**サーバ**](/tidb-cloud/built-in-monitoring.md#server)カテゴリでは、 **TiKV IO Bps**メトリックを改良して、精度と一貫性を向上させます。

        詳細については[TiDB Cloud組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)参照してください。

</CustomContent>

**APIの変更**

-   以下のリソースを自動的かつ効率的に管理するためのTiDB Cloud専用 API (v1beta1) を導入します。

    -   **クラスタ**: TiDB Cloud Dedicated クラスターをより柔軟に管理します。
    -   **リージョン**: TiDB Cloud Dedicated クラスターをデプロイできるすべてのクラウド リージョンを表示します。
    -   **プライベート エンドポイント接続**: クラスターの安全でプライベートな接続を設定します。
    -   **インポート**: クラスターのデータ インポート タスクを管理します。

    詳細については[TiDB Cloud専用API](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated/)参照してください。

-   以下のリソースを自動的かつ効率的に管理するためのTiDB Cloud Starter および Essential API (v1beta1) を導入します。

    -   **クラスタ**: TiDB Cloud Starter または Essential クラスターをより柔軟に管理します。
    -   **ブランチ**: クラスターのブランチを管理します。
    -   **エクスポート**: クラスターのデータ エクスポート タスクを管理します。
    -   **インポート**: クラスターのデータ インポート タスクを管理します。

    詳細については[TiDB Cloudスターターと基本 API](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless/)参照してください。

-   TiDB Cloud IAM API (v1beta1) は、組織レベルとプロジェクトレベルの両方で API キー管理のロールベースのアクセス制御 (RBAC) をサポートします。

    セキュリティとアクセス制御を強化するために、組織レベルまたはプロジェクト レベルで API キーのロールを設定できます。

    詳細については[TiDB CloudIAM API](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam/)参照してください。

## 2025年7月31日 {#july-31-2025}

**一般的な変更**

-   強化された Datadog と New Relic の統合がプレビューで利用できるようになりました。

    主な機能強化:

    -   メトリックのギャップを最小限に抑えるために、最適化された分離アーキテクチャを使用して統合バックエンドを再構築します。
    -   ユーザーのニーズに基づいて監視メトリックを追加します。
    -   一貫性を高めるためにメトリック ルールを調整します。

    これらの機能強化により、より正確な監視が可能になり、Datadog と New Relic の統合の信頼性が強化されます。

    展開計画:

    このプレビュー版は、Datadog または New Relic との連携がまだない組織にご利用いただけます。既に Datadog または New Relic との連携をご利用いただいている組織には、来月中に適切な移行プランとスケジュールを調整するために、積極的にご連絡いたします。

    詳細については、 [TiDB Cloudと Datadog の統合 (プレビュー)](/tidb-cloud/monitor-datadog-integration.md)および[TiDB Cloudと New Relic の統合（プレビュー）](/tidb-cloud/monitor-new-relic-integration.md)を参照してください。

## 2025年7月22日 {#july-22-2025}

**一般的な変更**

-   Google Cloud でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに新しいノード サイズ`32 vCPU, 128 GiB`指定します。

    この新しいサイズは、TiDB、TiKV、およびTiFlashノードで使用できます。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)の TiKV スケーリング プロセスを改善して、クラスターの安定性を強化します。

    TiKV ノードの[vCPUとRAMのサイズを変更する](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)追加すると、 TiDB Cloud は、クラスターの内部サービスに新しい構成をサポートするために追加の容量が必要かどうかを自動的に確認します。

    -   拡張が必要な​​場合は、 TiDB Cloud は続行する前に確認を求めます。
    -   スケーリング後の現在の内部サービス容量がすでに必要なサイズよりも大きい場合、 TiDB Cloud は、クラスターの安定性に影響を与える可能性のある不要な変更を回避するために、内部サービスの既存の構成を保持します。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)クラスターのクラウドstorageデータのインポート エクスペリエンスを強化します。

    インポートプロセスは、インテリジェントな事前チェック機能を備えた3ステップのウィザードに簡素化されました。この新しいウィザードは、接続設定、ファイルマッピング、バケットスキャンをガイドします。スキャン機能により、 TiDB Cloudはインポート前にインポートされるファイルとその保存先を正確に表示するため、設定の複雑さが大幅に軽減され、インポートの失敗を防止できます。

    詳細については、次のドキュメントを参照してください。

    -   [サンプルデータをTiDB Cloud Serverlessにインポートする](/tidb-cloud/import-sample-data-serverless.md)
    -   [クラウド ストレージからTiDB Cloud Serverless に CSV ファイルをインポートする](/tidb-cloud/import-csv-files-serverless.md)
    -   [Cloud Storage からTiDB Cloud Serverless に Apache Parquet ファイルをインポートする](/tidb-cloud/import-parquet-files-serverless.md)

## 2025年7月15日 {#july-15-2025}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン8.1.2](https://docs.pingcap.com/tidb/stable/release-8.1.2/)から[バージョン8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/)にアップグレードします。

    v8.1.2 と比較して、v8.5.2 には、 [v8.2.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.2.0/) 、 [v8.3.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.3.0/) 、 [v8.4.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.4.0/) 、 [バージョン8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/) 、 [バージョン8.5.1](https://docs.pingcap.com/tidb/stable/release-8.5.1/) 、および[バージョン8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/)でリリースされた新機能、改善、およびバグ修正が含まれています。

-   バックアップ アクティビティのコンソール監査ログを強化するために、 `BackupCompleted`イベントの監査をサポートします。

    この機能強化により、セキュリティとコンプライアンスの要件を満たすためにバックアップ完了アクティビティをログに記録できます。

    詳細については[コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)変更フィード内の列値のフィルタリングをサポートします。

    式を使用して変更フィード内の特定の列値をフィルタリングし、ソースで無関係なデータを除外できるようになりました。この機能により、DMLイベントのきめ細かなフィルタリングが可能になり、リソース消費を削減し、パフォーマンスを向上させることができます。

    詳細については[チェンジフィード](/tidb-cloud/changefeed-overview.md)参照してください。

## 2025年6月24日 {#june-24-2025}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)データベース監査ログ（ベータ版）がリクエストに応じて利用可能になりました。この機能を使用すると、ユーザーアクセスの詳細（実行されたSQL文など）の履歴をログに記録できます。

    この機能をリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポートをリクエスト」**をクリックします。次に、「説明」フィールドに「 TiDB Cloud Serverless データベース監査ログの申請」と入力し、 **「送信」を**クリックします。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)ユーザー制御のログ編集をサポートします。

    TiDB Cloud Dedicated クラスターのログ編集を有効または無効にして、クラスター ログの編集ステータスを自分で管理できるようになりました。

    詳細については[ユーザー制御のログ編集](/tidb-cloud/tidb-cloud-log-redaction.md)参照してください。

-   カスタマー管理の暗号化キー (CMEK) を使用した保存時の暗号化が、AWS でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで一般提供 (GA) されました。

    この機能を使用すると、キー管理サービス (KMS) を通じて管理する対称暗号化キーを活用して、保存中のデータを保護できます。

    詳細については[AWS での顧客管理の暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)参照してください。

## 2025年6月17日 {#june-17-2025}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの場合、16 vCPU および 32 vCPU を持つ TiKV ノードの最大storageサイズが**6144 GiB**から**4096 GiB**に変更されます。

    詳細については[TiKVノードのstorageサイズ](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)参照してください。

**コンソールの変更**

-   左側のナビゲーション ペインを改良して、全体的なナビゲーション エクスペリエンスを向上させます。

    -   新しい<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg>アイコンが左上隅に表示されるようになりました。これにより、必要に応じて左側のナビゲーション ペインを簡単に非表示または表示できます。

    -   左上隅にコンボ ボックスが追加され、組織、プロジェクト、クラスターを 1 つの中央の場所から簡単に切り替えられるようになりました。

        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    -   左側のナビゲーション ペインに表示されるエントリは、コンボ ボックスの現在の選択内容に応じて動的に調整されるようになり、最も関連性の高い機能に集中できるようになります。

    -   すぐにアクセスできるように、**サポート**、**通知**、アカウント エントリが、すべてのコンソール ページの左側のナビゲーション ペインの下部に常に表示されるようになりました。

## 2025年6月4日 {#june-4-2025}

**一般的な変更**

-   Microsoft Azure の[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)がパブリック プレビューで利用できるようになりました。

    このリリースにより、 TiDB Cloud はAWS、Google Cloud、Azure の 3 つの主要なパブリック クラウド プラットフォームすべてをサポートするようになり、ビジネス ニーズとクラウド戦略に最適な場所にTiDB Cloud Dedicated クラスターを展開できるようになりました。

    -   AWS および Google Cloud で利用可能なすべてのコア機能は、Azure で完全にサポートされています。
    -   Azure サポートは現在、米国東部 2、東日本、東南アジアの 3 つのリージョンで利用可能であり、近日中にさらに多くのリージョンで利用可能になる予定です。
    -   Azure 上のTiDB Cloud Dedicated クラスターには、TiDB バージョン v7.5.3 以降が必要です。

    Azure でTiDB Cloud Dedicated をすぐに使い始めるには、次のドキュメントを参照してください。

    -   [Azure 上にTiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)
    -   [Azure プライベート エンドポイント経由でTiDB Cloud専用クラスタを接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)
    -   [Azure 上のTiDB Cloud専用クラスタにデータをインポートする](/tidb-cloud/import-csv-files.md)

-   Prometheus 統合により、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの監視機能を強化するためのメトリックがさらに提供されます。

    これで、 `tidbcloud_disk_read_latency`や`tidbcloud_kv_request_duration`などの追加のメトリックを Prometheus に統合して、 TiDB Cloud Dedicated のパフォーマンスのより多くの側面を追跡できるようになりました。

    利用可能なメトリックと、既存ユーザーと新規ユーザーの両方に対してメトリックを有効にする方法の詳細については、 [TiDB Cloud をPrometheus および Grafana と統合する (ベータ版)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)参照してください。

-   TiKV [標準](/tidb-cloud/size-your-cluster.md#standard-storage)および[パフォーマンス](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage)storageの価格が正式に発表されました。

    割引期間は**2025年6月5日 UTC 00:00**に終了します。その後、価格は通常価格に戻ります。TiDB TiDB Cloud Dedicated の価格については、 [TiDB Cloud専用料金の詳細](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)ご覧ください。

**コンソールの変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのTiFlashノードのサイズを構成する際のインタラクティブ エクスペリエンスを強化します。

    TiDB Cloud Dedicated クラスターを作成するときに、トグル スイッチを使用してTiFlash構成を制御できるようになりました。これにより、構成エクスペリエンスがより直感的でシームレスになります。

## 2025年5月27日 {#may-27-2025}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの変更フィードを使用して[アパッチパルサー](https://pulsar.apache.org)へのデータのストリーミングをサポートします。

    この機能により、 TiDB Cloud Dedicated クラスタをより幅広い下流システムと統合できるようになり、追加のデータ統合要件にも対応できます。この機能を使用するには、 TiDB Cloud Dedicated クラスタのバージョンが v7.5.1 以降であることを確認してください。

    詳細については[アパッチパルサーに沈む](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)参照してください。

## 2025年5月13日 {#may-13-2025}

**一般的な変更**

-   AI アプリケーション向けのフルテキスト検索 (ベータ版) が[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)で利用可能になりました。

    TiDB Cloud Serverlessは、全文検索（ベータ版）をサポートしました。これにより、AIおよび検索拡張生成（RAG）アプリケーションは、正確なキーワードでコンテンツを検索できるようになります。これは、意味的類似性に基づいてコンテンツを検索するベクトル検索を補完するものです。両方の手法を組み合わせることで、RAGワークフローにおける検索精度と回答品質が大幅に向上します。主な機能は以下のとおりです。

    -   直接テキスト検索: 埋め込みを必要とせずに文字列列を直接クエリします。
    -   多言語サポート: 言語指定を必要とせずに、同じテーブル内でも複数の言語のテキストを自動的に検出して分析します。
    -   関連性に基づくランキング: 関連性を最適にするために、結果は業界標準の BM25 アルゴリズムを使用してランク付けされます。
    -   ネイティブ SQL 互換性: フィルタリング、グループ化、フルテキスト検索との結合などの SQL 機能をシームレスに使用します。

    開始するには、 [SQLによる全文検索](/tidb-cloud/vector-search-full-text-search-sql.md)または[Pythonによる全文検索](/tidb-cloud/vector-search-full-text-search-python.md)を参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの最大TiFlashノードstorageを増やします。

    -   8 vCPU TiFlashの場合、2048 GiBから4096 GiB
    -   32 vCPU TiFlashの場合、4096 GiBから8192 GiB

    この機能強化により、TiDB Cloud Dedicated クラスターの分析データstorage容量が増加し、ワークロードのスケーリング効率が向上し、増大するデータ要件に対応できるようになります。

    詳細については[TiFlashノードstorage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)参照してください。

-   メンテナンス タスクを構成および再スケジュールするための直感的なオプションを提供することで、メンテナンス ウィンドウの構成エクスペリエンスを強化します。

    詳細については[メンテナンスウィンドウを構成する](/tidb-cloud/configure-maintenance-window.md)参照してください。

-   TiKV [標準](/tidb-cloud/size-your-cluster.md#standard-storage)および[パフォーマンス](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage)storageタイプの割引期間を延長します。プロモーションは2025年6月5日に終了します。この日以降は、価格が標準料金に戻ります。

**コンソールの変更**

-   **バックアップ設定**ページのレイアウトを調整して、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのバックアップ構成エクスペリエンスを向上させます。

    詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

## 2025年4月22日 {#april-22-2025}

**一般的な変更**

-   Alibaba Cloud OSS へのデータエクスポートがサポートされるようになりました。

    [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)クラスターは、 [アクセスキーペア](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)を使用して[Alibaba Cloud オブジェクト ストレージ サービス (OSS)](https://www.alibabacloud.com/en/product/object-storage-service)にデータをエクスポートできるようになりました。

    詳細については[TiDB Cloud Serverlessからデータをエクスポート](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)クラスターの TiDB バージョンを[バージョン7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3)から[バージョン7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)にアップグレードします。

## 2025年4月15日 {#april-15-2025}

**一般的な変更**

-   [Alibaba Cloud オブジェクト ストレージ サービス (OSS)](https://www.alibabacloud.com/en/product/object-storage-service)クラスターから[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)クラスターへのデータのインポートをサポートします。

    この機能により、TiDB Cloud Serverlessへのデータ移行が簡素化されます。認証にはAccessKeyペアを使用できます。

    詳細については、次のドキュメントを参照してください。

    -   [Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud OSS から CSV ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-csv-files-serverless.md)
    -   [Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud OSS から Apache Parquet ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-parquet-files-serverless.md)

## 2025年4月1日 {#april-1-2025}

**一般的な変更**

-   [TiDBノードグループ](/tidb-cloud/tidb-node-group-overview.md)機能が、AWS と Google Cloud でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して一般提供 (GA) されました。

    この機能により、単一クラスター内で**きめ細かなコンピューティング リソースの分離**が可能になり、マルチテナントまたはマルチワークロードのシナリオでパフォーマンスとリソース割り当てを最適化できます。

    **主な利点:**

    -   **リソースの分離**:

        -   TiDB ノードを論理的に分離されたユニットにグループ化し、1 つのグループのワークロードが他のグループに影響を与えないようにします。
        -   アプリケーションまたはビジネス ユニット間のリソース競合を防止します。

    -   **簡素化された管理**：

        -   すべてのノード グループを単一のクラスター内で管理し、運用オーバーヘッドを削減します。
        -   需要に応じてグループを個別にスケールします。

    メリットの詳細については[技術ブログ](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)ご覧ください。開始するには[TiDBノードグループの管理](/tidb-cloud/tidb-node-group-management.md)ご覧ください。

-   AWS でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスター内の TiKV ノードに[標準storage](/tidb-cloud/size-your-cluster.md#standard-storage)タイプを導入します。

    標準storageタイプは、パフォーマンスとコスト効率のバランスが取れているため、ほとんどのワークロードに最適です。

    **主な利点:**

    -   **パフォーマンスの向上**: Raftログに十分なディスク リソースを予約し、 Raftとデータstorage間の I/O 競合を減らして、TiKV の読み取りと書き込みのパフォーマンスを向上させます。
    -   **強化された安定性**: 重要なRaft操作をデータ ワークロードから分離し、より予測可能なパフォーマンスを確保します。
    -   **コスト効率**: 従来のstorageタイプと比較して、競争力のある価格でより高いパフォーマンスを実現します。

    **可用性：**

    標準storageタイプは、2025年4月1日以降に作成され、AWSでホストされ、サポート対象バージョン（バージョン7.5.5、8.1.2、または8.5.0以上）の新規クラスター[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)に自動的に適用されます。既存のクラスターは引き続き以前の[基本的なstorage](/tidb-cloud/size-your-cluster.md#basic-storage)タイプを使用しているため、移行は不要です。

    スタンダードstorageの料金はベーシックstorageの料金とは異なります。詳しくは[価格](https://www.pingcap.com/tidb-dedicated-pricing-details/)ご覧ください。

## 2025年3月25日 {#march-25-2025}

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)クラスター内のパブリック エンドポイントのファイアウォール ルールをサポートします。

    TiDB Cloud Serverless クラスターのファイアウォールルールを設定して、パブリックエンドポイント経由のアクセスを制御できるようになりました。1 [TiDB Cloudコンソール](https://tidbcloud.com/)許可する IP アドレスまたは範囲を直接指定することで、セキュリティを強化できます。

    詳細については[パブリックエンドポイント用のTiDB Cloudサーバーレス ファイアウォール ルールを構成する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)参照してください。

## 2025年3月18日 {#march-18-2025}

**一般的な変更**

-   リソース管理の柔軟性を高めるために、Google Cloud にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに対して TiDB ノード グループの作成をサポートします。

    詳細については[TiDBノードグループの概要](/tidb-cloud/tidb-node-group-overview.md)参照してください。

-   AWS にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのTiDB Cloudにデータベース監査ログ ファイルを保存することをサポートします。

    これらの監査ログファイルは、 TiDB Cloudから直接ダウンロードできます。この機能はリクエストに応じてのみ利用可能であることにご注意ください。

    詳細については[データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)参照してください。

-   多要素認証（MFA）の管理を改善することで、 TiDB Cloudアカウントのセキュリティを強化します。この機能は、TiDB Cloudのパスワードベースのログインに適用されます。

    詳細については[パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)参照してください。

## 2025年2月18日 {#february-18-2025}

**コンソールの変更**

-   TiDB Cloudの新しいサポート サービスである Connected Care を紹介します。

    Connected Care サービスは、最新のコミュニケーション ツール、プロアクティブなサポート、高度な AI 機能を通じてTiDB Cloudとの接続を強化し、シームレスで顧客中心のエクスペリエンスを実現するように設計されています。

    Connected Care サービスでは、次の機能が導入されています。

    -   **クリニック サービス**: パフォーマンスを最適化するための高度な監視と診断。
    -   **IM での AI チャット**: インスタント メッセージ (IM) ツールを通じて AI による即時サポートを受けることができます。
    -   **アラートとチケット更新の IM サブスクリプション**: IM 経由でアラートとチケットの進行状況に関する最新情報を入手します。
    -   **サポート チケットの IM 対話**: IM ツールを使用してサポート チケットを作成し、対話します。

    詳細については[コネクテッドケアの概要](/tidb-cloud/connected-care-overview.md)参照してください。

-   GCS および Azure Blob Storage から[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)クラスターへのデータのインポートをサポートします。

    TiDB Cloud Serverless は、Google Cloud Storage (GCS) および Azure Blob Storage からのデータのインポートをサポートするようになりました。認証には、Google Cloud サービス アカウント キーまたは Azure Shared Access Signature (SAS) トークンを使用できます。この機能により、TiDB Cloud Serverless へのデータ移行が簡素化されます。

    詳細については、 [Amazon S3、GCS、または Azure Blob Storage からTiDB Cloud Serverless に CSV ファイルをインポートする](/tidb-cloud/import-csv-files-serverless.md)および[Amazon S3、GCS、または Azure Blob Storage から Apache Parquet ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-parquet-files-serverless.md)を参照してください。

## 2025年1月21日 {#january-21-2025}

**コンソールの変更**

-   タスクあたり最大 250 MiB の単一のローカル CSV ファイルを[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)クラスターにインポートできるようになりました。これは、以前の 50 MiB の制限から増加されました。

    詳細については[ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)参照してください。

## 2025年1月14日 {#january-14-2025}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい AWS リージョンをサポートします: `Jakarta (ap-southeast-3)` 。

-   通知機能を導入すると、 [TiDB Cloudコンソール](https://tidbcloud.com/)を通じてTiDB Cloud の更新とアラートに関する最新情報を即座に入手できます。

    詳細については[通知](/tidb-cloud/notifications.md)参照してください。

## 2025年1月2日 {#january-2-2025}

**一般的な変更**

-   リソース管理の柔軟性を高めるために、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの TiDB ノード グループの作成をサポートします。

    詳細については[TiDBノードグループの概要](/tidb-cloud/tidb-node-group-overview.md)参照してください。

-   Private Connect (ベータ版) を介して[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを AWS および Google Cloud の汎用 Kafka に接続することをサポートします。

    Private Connect は、クラウドプロバイダーの Private Link または Private Service Connect テクノロジーを活用し、 TiDB Cloud VPC 内の変更フィードがプライベート IP アドレスを使用してお客様の VPC 内の Kafka に接続できるようにします。これにより、Kafka がTiDB Cloud VPC 内で直接ホストされているかのように扱われます。この機能は、VPC CIDR の競合を防止し、セキュリティコンプライアンス要件を満たすのに役立ちます。

    -   AWS の Apache Kafka の場合は、 [AWS でセルフホスト型 Kafka プライベートリンク サービスをセットアップする](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md)手順に従ってネットワーク接続を構成します。

    -   Google Cloud の Apache Kafka の場合は、 [Google Cloud でセルフホスト型 Kafka プライベート サービス接続を設定する](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)手順に従ってネットワーク接続を構成します。

    この機能を使用すると、追加の[プライベートデータリンクのコスト](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)が発生することに注意してください。

    詳細については[Apache Kafka への Changefeed シンク](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)参照してください。

-   Kafka の変更フィードに追加の構成可能なオプションを導入します。

    -   Debeziumプロトコルのサポート。Debeziumはデータベースの変更をキャプチャするためのツールです。キャプチャされたデータベースの変更はイベントと呼ばれるメッセージに変換され、Kafkaに送信されます。詳細については、 [TiCDC デベジウムプロトコル](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)参照してください。

    -   すべてのテーブルに対して単一のパーティション ディスパッチャーを定義することも、テーブルごとに異なるパーティション ディスパッチャーを定義することもサポートします。

    -   Kafka メッセージのパーティション分散用に、タイムスタンプと列値という 2 つの新しいディスパッチャ タイプを導入しました。

    詳細については[Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)参照してください。

-   TiDB Cloudでの役割の強化:

    -   TiDB Cloudでのきめ細かなアクセス制御を強化するために、ロール`Project Viewer`と`Organization Billing Viewer`を導入します。

    -   次のロールの名前を変更します。

        -   `Organization Member`から`Organization Viewer`
        -   `Organization Billing Admin`から`Organization Billing Manager`
        -   `Organization Console Audit Admin`から`Organization Console Audit Manager`

    詳細については[アイデンティティアクセス管理](/tidb-cloud/manage-user-access.md#organization-roles)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)クラスターのリージョン高可用性 (ベータ版)。

    この機能は、最大限のインフラストラクチャ冗長性とビジネス継続性を必要とするワークロード向けに設計されています。主な関数は次のとおりです。

    -   ノードは複数の可用性ゾーンに分散され、ゾーン障害が発生した場合でも高可用性が確保されます。
    -   PD や TiKV などの重要な OLTP (オンライン トランザクション処理) コンポーネントは、冗長性を確保するために可用性ゾーン全体に複製されます。
    -   自動フェイルオーバーにより、プライマリ ゾーンの障害時のサービス中断が最小限に抑えられます。

    この機能は現在、AWS 東京 (ap-northeast-1) リージョンでのみ利用可能で、クラスターの作成時にのみ有効にできます。

    詳細については[TiDB Cloud Serverless の高可用性](/tidb-cloud/serverless-high-availability.md)参照してください。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1)から[バージョン8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)にアップグレードします。

**コンソールの変更**

-   データエクスポートサービスの強化:

    -   [TiDB Cloudコンソール](https://tidbcloud.com/)を介して[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#starter)から Google Cloud Storage および Azure Blob Storage へのデータのエクスポートをサポートします。

    -   [TiDB Cloudコンソール](https://tidbcloud.com/)を介して Parquet ファイルでデータのエクスポートをサポートします。

    詳細については、 [TiDB Cloud Serverlessからデータをエクスポート](/tidb-cloud/serverless-export.md)および[TiDB Cloud Serverless の外部ストレージアクセスを構成する](/tidb-cloud/configure-external-storage-access.md)を参照してください。
