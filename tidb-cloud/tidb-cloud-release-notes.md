---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2023 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2023}

このページには 2023 年[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリースノートが記載されています。

## 2023 年 12 月 5 日 {#december-5-2023}

**一般的な変更点**

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)を指定すると、失敗した変更フィードを再開できるため、新しい変更フィードを再作成する手間が省けます。

    詳細については、 [フィード状態の変更](/tidb-cloud/changefeed-overview.md#changefeed-states)を参照してください。

**コンソールの変更**

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)の接続エクスペリエンスを強化します。

    [接続**] ダイアログ**インターフェイスを改良して、TiDB サーバーレス ユーザーに、よりスムーズで効率的な接続エクスペリエンスを提供します。さらに、TiDB サーバーレスでは、より多くのクライアント タイプが導入され、接続に必要なブランチを選択できるようになります。

    詳細については、 [TiDB サーバーレスに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)を参照してください。

## 2023年11月28日 {#november-28-2023}

**一般的な変更点**

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)バックアップからの SQL バインディングの復元をサポートします。

    TiDB D dedicated は、バックアップから復元するときに、デフォルトでユーザー アカウントと SQL バインディングを復元するようになりました。この拡張機能は v6.2.0 以降のバージョンのクラスターで利用でき、データ復元プロセスを合理化します。 SQL バインディングの復元により、クエリ関連の構成と最適化がスムーズに再統合され、より包括的で効率的なリカバリ エクスペリエンスが提供されます。

    詳細については、 [TiDB 専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

**コンソールの変更**

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless) SQL ステートメントの RU コストの監視をサポートします。

    TiDB サーバーレスは、 [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) SQL ステートメントの詳細な洞察を提供するようになりました。 SQL ステートメントごとの**合計 RU**コストと**平均 RU**コストの両方を表示できます。この機能は、RU コストの特定と分析に役立ち、運用における潜在的なコスト削減の機会を提供します。

    SQL ステートメント RU の詳細を確認するには、 [TiDB サーバーレス クラスター](https://tidbcloud.com/console/clusters)の**[診断]**ページに移動し、 **[SQL ステートメント]**タブをクリックします。

## 2023 年 11 月 21 日 {#november-21-2023}

**一般的な変更点**

-   [データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md) Google Cloud にデプロイされた TiDB クラスタの高速物理モードをサポートします。

    AWS および Google Cloud にデプロイされた TiDB クラスターに物理モードを使用できるようになりました。物理モードの移行速度は最大 110 MiB/秒に達し、論理モードの 2.4 倍です。向上したパフォーマンスは、大規模なデータセットをTiDB Cloudに迅速に移行するのに適しています。

    詳細については、 [既存のデータと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)を参照してください。

## 2023 年 11 月 14 日 {#november-14-2023}

**一般的な変更点**

-   TiDB 専用クラスターからデータを復元する場合、デフォルトの動作が、ユーザー アカウントなしでの復元から、 `cloud_admin@'%'`アカウントを含むすべてのユーザー アカウントを使用した復元に変更されました。

    詳細については、 [TiDB 専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

-   変更フィード用のイベント フィルターを導入します。

    この機能強化により、変更フィードのイベント フィルターを直接[TiDB Cloudコンソール](https://tidbcloud.com/)を通じて簡単に管理できるようになり、変更フィードから特定のイベントを除外するプロセスが合理化され、ダウンストリームのデータ レプリケーションをより適切に制御できるようになります。

    詳細については、 [チェンジフィード](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)を参照してください。

## 2023 年 11 月 7 日 {#november-7-2023}

**一般的な変更点**

-   次のリソース使用量アラートを追加します。新しいアラートはデフォルトでは無効になっています。必要に応じて有効にできます。

    -   TiDB ノード全体の最大メモリ使用率が 10 分間で 70% を超えました
    -   TiKV ノード全体の最大メモリ使用率が 10 分間で 70% を超えました
    -   TiDB ノード全体の最大 CPU 使用率が 10 分間で 80% を超えました
    -   TiKV ノード全体の最大 CPU 使用率が 10 分間で 80% を超えました

    詳細については、 [TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md#resource-usage-alerts)を参照してください。

## 2023年10月31日 {#october-31-2023}

**一般的な変更点**

-   営業担当者に連絡せずに、 TiDB Cloudコンソールでエンタープライズ サポート プランへの直接アップグレードをサポートします。

    詳細については、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)を参照してください。

## 2023 年 10 月 25 日 {#october-25-2023}

**一般的な変更点**

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) Google Cloud でのデュアル リージョン バックアップ（ベータ版）をサポートします。

    Google Cloud でホストされている TiDB 専用クラスターは、Google Cloud Storage とシームレスに連携します。 Google Cloud Storage の[デュアルリージョン](https://cloud.google.com/storage/docs/locations#location-dr)機能と同様に、TiDB Dended のデュアル リージョンに使用するリージョンのペアは、同じマルチリージョン内にある必要があります。たとえば、東京と大阪は同じマルチリージョン`ASIA`にあるため、デュアルリージョンstorageとして一緒に使用できます。

    詳細については、 [TiDB 専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup-beta)を参照してください。

-   [データ変更ログを Apache Kafka にストリーミングする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)の機能は現在一般提供 (GA) されています。

    10 か月のベータ版トライアルが成功した後、 TiDB Cloudから Apache Kafka へのデータ変更ログのストリーミング機能が一般利用可能になります。 TiDB からメッセージ キューへのデータのストリーミングは、データ統合シナリオでは一般的なニーズです。 Kafka シンクを使用して、他のデータ処理システム (Snowflake など) と統合したり、ビジネス利用をサポートしたりできます。

    詳細については、 [チェンジフィードの概要](/tidb-cloud/changefeed-overview.md)を参照してください。

## 2023 年 10 月 11 日 {#october-11-2023}

**一般的な変更点**

-   AWS にデプロイされた[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターに対して[デュアル リージョン バックアップ (ベータ版)](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup-beta)サポートします。

    クラウド プロバイダー内の地理的リージョン間でバックアップをレプリケートできるようになりました。この機能は、データ保護および災害復旧機能の追加レイヤーを提供します。

    詳細については、 [TiDB 専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

-   データ移行では、既存のデータを移行するために物理モードと論理モードの両方がサポートされるようになりました。

    物理モードでは、移行速度は最大 110 MiB/秒に達します。論理モードの 45 MiB/s と比較して、移行パフォーマンスは大幅に向上しました。

    詳細については、 [既存のデータと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)を参照してください。

## 2023 年 10 月 10 日 {#october-10-2023}

**一般的な変更点**

-   TiDB Cloud Vercel 統合による[Vercel のプレビュー展開](https://vercel.com/docs/deployments/preview-deployments)の TiDB サーバーレス ブランチの使用をサポートします。

    詳細については、 [TiDB サーバーレス ブランチで接続する](/tidb-cloud/integrate-tidbcloud-with-vercel.md#connect-with-tidb-serverless-branching)を参照してください。

## 2023年9月28日 {#september-28-2023}

**APIの変更**

-   TiDB Cloud Billing API エンドポイントを導入して、特定の組織の特定の月の請求書を取得します。

    この Billing API エンドポイントは、 TiDB Cloudの最新 API バージョンである TiDB TiDB Cloud API v1beta1 でリリースされています。詳細については、 [API ドキュメント (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1#tag/Billing)を参照してください。

## 2023 年 9 月 19 日 {#september-19-2023}

**一般的な変更点**

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターから 2 つの vCPU TiDB ノードと TiKV ノードを削除します。

    2 vCPU オプションは、 **[クラスタの作成]**ページまたは [**クラスタの変更]**ページでは使用できなくなりました。

-   JavaScript のリリース[TiDB Cloudサーバーレス ドライバー (ベータ版)](/tidb-cloud/serverless-driver.md) 。

    JavaScript 用TiDB Cloudサーバーレス ドライバーを使用すると、HTTPS 経由で[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターに接続できます。これは、TCP 接続が[バーセルエッジ機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare ワーカー](https://workers.cloudflare.com/)などに制限されているエッジ環境で特に役立ちます。

    詳細については、 [TiDB Cloudサーバーレス ドライバー (ベータ版)](/tidb-cloud/serverless-driver.md)を参照してください。

**コンソールの変更**

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの場合、 **「今月の使用量」**パネルで、または支出制限の設定中にコストの見積もりを取得できます。

## 2023 年 9 月 5 日 {#september-5-2023}

**一般的な変更点**

-   [データサービス（ベータ版）](https://tidbcloud.com/console/data-service) 、さまざまな状況での特定のレート制限要件を満たすために、各 API キーのレート制限をカスタマイズすることをサポートします。

    API キーを[作成する](/tidb-cloud/data-service-api-key.md#create-an-api-key)または[編集](/tidb-cloud/data-service-api-key.md#edit-an-api-key)にすると、そのレート制限を調整できます。

    詳細については、 [レート制限](/tidb-cloud/data-service-api-key.md#rate-limiting)を参照してください。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの新しい AWS リージョンをサポートします: サンパウロ (sa-east-1)。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)つのクラスターごとに、IP アクセス リストへの最大 100 個の IP アドレスの追加をサポートします。

    詳細については、 [IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md)を参照してください。

**コンソールの変更**

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの**「イベント」**ページを導入します。このページには、クラスターに対する主な変更の記録が表示されます。

    このページでは、過去 7 日間のイベント履歴を表示し、トリガー時間やアクションを開始したユーザーなどの重要な詳細を追跡できます。

    詳細については、 [TiDB Cloudクラスター イベント](/tidb-cloud/tidb-cloud-events.md)を参照してください。

**APIの変更**

-   [AWS プライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)または[Google Cloud プライベート サービス コネクト](https://cloud.google.com/vpc/docs/private-service-connect) for [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターを管理するためのいくつかのTiDB CloudAPI エンドポイントをリリースします。

    -   クラスターのプライベート エンドポイント サービスを作成する
    -   クラスターのプライベート エンドポイント サービス情報を取得する
    -   クラスターのプライベート エンドポイントを作成する
    -   クラスターのすべてのプライベート エンドポイントを一覧表示する
    -   プロジェクト内のすべてのプライベート エンドポイントを一覧表示する
    -   クラスターのプライベート エンドポイントを削除する

    詳細については、 [APIドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster)を参照してください。

## 2023 年 8 月 23 日 {#august-23-2023}

**一般的な変更点**

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの Google Cloud [プライベートサービス接続](https://cloud.google.com/vpc/docs/private-service-connect)をサポートします。

    プライベート エンドポイントを作成し、Google Cloud でホストされている TiDB 専用クラスタへの安全な接続を確立できるようになりました。

    主な利点：

    -   直感的な操作: わずか数ステップでプライベート エンドポイントを作成できます。
    -   セキュリティの強化: 安全な接続を確立してデータを保護します。
    -   パフォーマンスの向上: 低遅延で高帯域幅の接続を提供します。

    詳細については、 [プライベート エンドポイント経由で Google Cloud に接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)を参照してください。

-   チェンジフィードを使用した[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターから[Google クラウド ストレージ (GCS)](https://cloud.google.com/storage)へのデータのストリーミングをサポートします。

    自分のアカウントのバケットを使用し、正確に調整された権限を提供することで、 TiDB Cloudから GCS にデータをストリーミングできるようになりました。データを GCS にレプリケートした後、必要に応じてデータの変更を分析できます。

    詳細については、 [クラウドストレージにシンクする](/tidb-cloud/changefeed-sink-to-cloud-storage.md)を参照してください。

## 2023 年 8 月 15 日 {#august-15-2023}

**一般的な変更点**

-   [データサービス（ベータ版）](https://tidbcloud.com/console/data-service)開発エクスペリエンスを向上させるために`GET`リクエストのページネーションをサポートします。

    `GET`リクエストの場合、**事前プロパティ**で**ページネーションを**有効にし、エンドポイントを呼び出すときにクエリ パラメーターとして`page`と`page_size`を指定することで、結果をページネーションできます。たとえば、1 ページあたり 10 個のアイテムを含む 2 ページ目を取得するには、次のコマンドを使用できます。

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>?page=2&page_size=10'
    ```

    この機能は、最後のクエリが`SELECT`ステートメントである`GET`リクエストに対してのみ使用できることに注意してください。

    詳細については、 [エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)を参照してください。

-   [データサービス（ベータ版）](https://tidbcloud.com/console/data-service)指定された存続時間 (TTL) 期間にわたる`GET`のリクエストのエンドポイント応答のキャッシュをサポートします。

    この機能により、データベースの負荷が軽減され、エンドポイントのレイテンシーが最適化されます。

    `GET`リクエスト メソッドを使用するエンドポイントの場合、**キャッシュ レスポンス**を有効にし、 **[詳細プロパティ]**でキャッシュの TTL 期間を構成できます。

    詳細については、 [高度なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)を参照してください。

-   AWS でホストされ、2023 年 8 月 15 日以降に作成された次の[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの負荷分散の改善を無効にします。

    -   AWS でホストされている TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することを無効にします。
    -   AWS でホストされている TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することを無効にします。

    この変更により、ハイブリッド展開のリソース競合が回避され、この改善が有効になっている既存のクラスターには影響しません。新しいクラスターの負荷分散の改善を有効にしたい場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## 2023 年 8 月 8 日 {#august-8-2023}

**一般的な変更点**

-   [データサービス（ベータ版）](https://tidbcloud.com/console/data-service)では Basic 認証がサポートされるようになりました。

    [「基本」HTTP 認証](https://datatracker.ietf.org/doc/html/rfc7617)を使用して、リクエストで公開キーをユーザー名として、秘密キーをパスワードとして指定できます。ダイジェスト認証と比較して、基本認証はシンプルであり、データ サービス エンドポイントを呼び出すときにより簡単に使用できます。

    詳細については、 [エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)を参照してください。

## 2023 年 8 月 1 日 {#august-1-2023}

**一般的な変更点**

-   TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)のデータ アプリの OpenAPI 仕様をサポートします。

    TiDB Cloudデータ サービスは、各データ アプリに対して自動生成された OpenAPI ドキュメントを提供します。ドキュメントでは、エンドポイント、パラメーター、応答を表示し、エンドポイントを試すことができます。

    データ アプリとそのデプロイされたエンドポイントの OpenAPI 仕様 (OAS) を YAML または JSON 形式でダウンロードすることもできます。 OAS は、標準化された API ドキュメント、簡素化された統合、および簡単なコード生成を提供し、より迅速な開発とコラボレーションの向上を可能にします。

    詳細については、 [OpenAPI仕様を使用する](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification)および[Next.js で OpenAPI 仕様を使用する](/tidb-cloud/data-service-oas-with-nextjs.md)を参照してください。

-   [郵便屋さん](https://www.postman.com/)でデータ アプリの実行をサポートします。

    Postman の統合により、データ アプリのエンドポイントをコレクションとして好みのワークスペースにインポートできるようになります。これにより、Postman Web アプリとデスクトップ アプリの両方をサポートする強化されたコラボレーションとシームレスな API テストの恩恵を受けることができます。

    詳細については、 [Postman でデータ アプリを実行する](/tidb-cloud/data-service-postman-integration.md)を参照してください。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターに新しい**一時停止**ステータスが導入され、この期間中は料金が発生せず、コスト効率の高い一時停止が可能になります。

    TiDB 専用クラスターの**「一時停止」**をクリックすると、クラスターは最初に**「一時停止」**ステータスになります。一時停止操作が完了すると、クラスターのステータスは**[一時停止]**に移行します。

    クラスターはステータスが**一時停止**に移行した後にのみ再開できます。これにより、**一時停止**と**再開**を素早くクリックすることによって引き起こされる異常な再開の問題が解決されます。

    詳細については、 [TiDB 専用クラスターの一時停止または再開](/tidb-cloud/pause-or-resume-tidb-cluster.md)を参照してください。

## 2023 年 7 月 26 日 {#july-26-2023}

**一般的な変更点**

-   TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)の強力な機能、つまり自動エンドポイント生成を紹介します。

    開発者は、最小限のクリックと構成で HTTP エンドポイントを簡単に作成できるようになりました。反復的な定型コードを排除し、エンドポイントの作成を簡素化および高速化して、潜在的なエラーを削減します。

    この機能の使用方法の詳細については、 [エンドポイントを自動的に生成する](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)を参照してください。

-   TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)のエンドポイントに対して`PUT`および`DELETE`リクエスト メソッドをサポートします。

    -   データを更新または変更するには、 `UPDATE`ステートメントと同様に`PUT`メソッドを使用します。
    -   データを削除するには、 `DELETE`ステートメントと同様に`DELETE`メソッドを使用します。

    詳細については、 [プロパティの構成](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)を参照してください。

-   TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)の`POST` 、 `PUT` 、および`DELETE`リクエスト メソッドの**バッチ操作**をサポートします。

    エンドポイントに対して**バッチ操作が**有効になっている場合、単一のリクエストで複数の行に対して操作を実行できるようになります。たとえば、単一の`POST`リクエストを使用して複数行のデータを挿入できます。

    詳細については、 [高度なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)を参照してください。

## 2023 年 7 月 25 日 {#july-25-2023}

**一般的な変更点**

-   新しい[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)から[v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)にアップグレードします。

**コンソールの変更**

-   サポート エントリを最適化することで、 TiDB Cloudユーザーの PingCAP サポートへのアクセスを簡素化します。改善内容は次のとおりです。

    -   に**サポート**の入り口を追加します。<mdsvgicon name="icon-top-organization">左下隅にあります。</mdsvgicon>
    -   **?**のメニューを刷新。 [TiDB Cloudコンソール](https://tidbcloud.com/)の右下隅にある アイコンを使用すると、より直感的に操作できるようになります。

    詳細については、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)を参照してください。

## 2023 年 7 月 18 日 {#july-18-2023}

**一般的な変更点**

-   組織レベルとプロジェクト レベルの両方でロールベースのアクセス制御を洗練することで、セキュリティ、コンプライアンス、生産性を向上させるために、最小限の権限を持つロールをユーザーに付与できます。

    -   組織の役割には、 `Organization Owner` 、 `Organization Billing Admin` 、 `Organization Console Audit Admin` 、および`Organization Member`が含まれます。
    -   プロジェクトの役割には、 `Project Owner` 、 `Project Data Access Read-Write` 、および`Project Data Access Read-Only`が含まれます。
    -   プロジェクト内のクラスターを管理 (クラスターの作成、変更、削除など) するには、 `Organization Owner`または`Project Owner`ロールに属する必要があります。

    さまざまな役割の権限の詳細については、 [ユーザーの役割](/tidb-cloud/manage-user-access.md#user-roles)を参照してください。

-   AWS でホストされる[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターに対して顧客管理の暗号化キー (CMEK) 機能 (ベータ版) をサポートします。

    AWS KMS に基づいて CMEK を作成し、EBS および S3 に保存されているデータをTiDB Cloudコンソールから直接暗号化できます。これにより、顧客データは顧客が管理するキーで暗号化され、セキュリティが強化されます。

    この機能には依然として制限があり、リクエストがあった場合にのみ利用できることに注意してください。この機能を申請するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

-   データ インポート エクスペリエンスの向上を目的として、 TiDB Cloudのインポート機能を最適化します。次の改善が行われました。

    -   TiDB サーバーレスの統合インポート エントリ: データをインポートするためのエントリを統合し、ローカル ファイルのインポートと Amazon S3 からのファイルのインポートをシームレスに切り替えることができます。
    -   合理化された構成: Amazon S3 からのデータのインポートには 1 つのステップのみが必要となり、時間と労力を節約できます。
    -   CSV 構成の強化: CSV 構成設定がファイル タイプ オプションの下に配置されるようになり、必要なパラメーターをすばやく簡単に構成できるようになりました。
    -   強化されたターゲット テーブルの選択: チェックボックスをクリックして、データ インポートに必要なターゲット テーブルの選択をサポートします。この改善により、複雑な式が不要になり、ターゲット テーブルの選択が簡素化されました。
    -   表示情報の改良: インポート プロセス中に表示される不正確な情報に関連する問題を解決します。さらに、不完全なデータ表示を防ぎ、誤解を招く情報を避けるために、プレビュー機能が削除されました。
    -   ソース ファイル マッピングの改善: ソース ファイルとターゲット テーブルの間のマッピング関係の定義をサポートします。これは、特定の命名要件を満たすためにソース ファイル名を変更するという課題に対処します。

## 2023 年 7 月 11 日 {#july-11-2023}

**一般的な変更点**

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)が一般提供になりました。

-   TiDB Bot (ベータ版) は、多言語サポート、年中無休のリアルタイム応答、統合されたドキュメント アクセスを提供する OpenAI 搭載チャットボットです。

    TiDB ボットには次の利点があります。

    -   継続的なサポート: 強化されたサポート エクスペリエンスを実現するために、いつでもお客様の質問に答え、サポートを提供します。
    -   効率の向上: 自動応答によりレイテンシーが短縮され、全体的な運用が向上します。
    -   シームレスなドキュメント アクセス: TiDB Cloudドキュメントに直接アクセスして、情報を簡単に取得し、問題を迅速に解決できます。

    TiDB ボットを使用するには、 **「?」**をクリックします。 [TiDB Cloudコンソール](https://tidbcloud.com)の右下隅にある**[TiDB Bot にチャットを開始するよう依頼する]**を選択します。

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターに対して[分岐機能 (ベータ版)](/tidb-cloud/branch-overview.md)サポートします。

    TiDB Cloudすると、TiDB サーバーレス クラスターのブランチを作成できます。クラスターのブランチは、元のクラスターからのデータの分岐コピーを含む別個のインスタンスです。隔離された環境を提供するため、元のクラスターへの影響を心配することなく、接続して自由に実験できます。

    [TiDB Cloudコンソール](/tidb-cloud/branch-manage.md)または[TiDB CloudCLI](/tidb-cloud/ticloud-branch-create.md)のいずれかを使用して、2023 年 7 月 5 日以降に作成された TiDB サーバーレス クラスターのブランチを作成できます。

    アプリケーション開発に GitHub を使用する場合は、TiDB サーバーレス ブランチを GitHub CI/CD パイプラインに統合できます。これにより、本番データベースに影響を与えることなく、ブランチを使用してプル リクエストを自動的にテストできます。詳細については、 [TiDB サーバーレス ブランチング (ベータ版) を GitHub と統合する](/tidb-cloud/branch-github-integration.md)を参照してください。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの毎週のバックアップをサポートします。詳細については、 [TiDB 専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)を参照してください。

## 2023 年 7 月 4 日 {#july-4-2023}

**一般的な変更点**

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのポイントインタイム リカバリ (PITR) (ベータ版) をサポートします。

    TiDB サーバーレス クラスターを過去 90 日以内の任意の時点に復元できるようになりました。この機能は、TiDB サーバーレス クラスターのデータ回復機能を強化します。たとえば、データ書き込みエラーが発生し、データを以前の状態に復元する必要がある場合に、PITR を使用できます。

    詳細については、 [TiDB サーバーレス データのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md#restore)を参照してください。

**コンソールの変更**

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのクラスター概要ページにある**[今月の使用量]**パネルを強化して、現在のリソース使用量をより明確に表示します。

-   次の変更を加えて、全体的なナビゲーション エクスペリエンスを強化します。

    -   統合する<mdsvgicon name="icon-top-organization">**組織**と<mdsvgicon name="icon-top-account-settings">右上隅の**アカウントを**左側のナビゲーション バーに移動します。</mdsvgicon></mdsvgicon>
    -   統合する<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg>左側のナビゲーションバーの**「管理者**」<mdsvgicon name="icon-left-projects">左側のナビゲーション バーに**投影し**、左上隅にある ☰ ホバー メニューを削除します。クリックできるようになりました<mdsvgicon name="icon-left-projects">プロジェクト間を切り替え、プロジェクト設定を変更します。</mdsvgicon></mdsvgicon>
    -   TiDB Cloudのすべてのヘルプとサポート情報を**?**のメニューに統合します。右下隅のアイコン (ドキュメント、インタラクティブなチュートリアル、セルフペース トレーニング、サポート エントリなど)。

-   TiDB Cloudコンソールは、より快適で目に優しいエクスペリエンスを提供するダーク モードをサポートするようになりました。左側のナビゲーション バーの下部からライト モードとダーク モードを切り替えることができます。

## 2023 年 6 月 27 日 {#june-27-2023}

**一般的な変更点**

-   新しく作成された[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの事前構築済みサンプル データセットを削除します。

## 2023 年 6 月 20 日 {#june-20-2023}

**一般的な変更点**

-   新しい[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)から[v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)にアップグレードします。

## 2023 年 6 月 13 日 {#june-13-2023}

**一般的な変更点**

-   Amazon S3 にデータをストリーミングするための変更フィードの使用をサポートします。

    これにより、 TiDB Cloudと Amazon S3 間のシームレスな統合が可能になります。これにより、 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターから Amazon S3 へのリアルタイムのデータのキャプチャとレプリケーションが可能になり、ダウンストリームのアプリケーションと分析が最新のデータに確実にアクセスできるようになります。

    詳細については、 [クラウドstorageにシンクする](/tidb-cloud/changefeed-sink-to-cloud-storage.md)を参照してください。

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの 16 vCPU TiKV の最大ノードstorageを4 TiB から 6 TiB に増加します。

    この機能強化により、TiDB 専用クラスターのデータstorage容量が増加し、ワークロードのスケーリング効率が向上し、増大するデータ要件に対応できます。

    詳細については、 [クラスターのサイズを調整する](/tidb-cloud/size-your-cluster.md)を参照してください。

-   [モニタリングメトリクスの保持期間](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) for [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターを 3 日間から 7 日間に延長します。

    メトリクスの保持期間を延長することで、より多くの履歴データにアクセスできるようになりました。これは、クラスターの傾向とパターンを特定して、より適切な意思決定と迅速なトラブルシューティングを行うのに役立ちます。

**コンソールの変更**

-   [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの[**キービジュアライザー**](/tidb-cloud/tune-performance.md#key-visualizer)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャを使用すると、 **Key Visualizer**ページを簡単に移動して、より直観的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは UX に関する多くの問題も解決し、SQL 診断プロセスをより使いやすくしています。

## 2023 年 6 月 6 日 {#june-6-2023}

**一般的な変更点**

-   [インデックスインサイト（ベータ版）](/tidb-cloud/index-insight.md) for [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターを導入します。これは、遅いクエリに対してインデックスの推奨を提供することでクエリのパフォーマンスを最適化します。

    Index Insight を使用すると、次の方法でアプリケーション全体のパフォーマンスとデータベース操作の効率を向上させることができます。

    -   クエリのパフォーマンスの強化: Index Insight は遅いクエリを特定し、それらに適切なインデックスを提案します。これにより、クエリの実行が高速化され、応答時間が短縮され、ユーザー エクスペリエンスが向上します。
    -   コスト効率: Index Insight を使用してクエリ パフォーマンスを最適化すると、追加のコンピューティング リソースの必要性が減り、既存のインフラストラクチャをより効果的に使用できるようになります。これにより、運用コストの削減につながる可能性があります。
    -   簡素化された最適化プロセス: Index Insight は、インデックスの改善点の特定と実装を簡素化し、手動による分析や推測の必要性を排除します。その結果、正確なインデックス推奨により時間と労力を節約できます。
    -   アプリケーション効率の向上: Index Insight を使用してデータベースのパフォーマンスを最適化することで、 TiDB Cloud上で実行されるアプリケーションはより大きなワークロードを処理し、より多くのユーザーに同時にサービスを提供できるため、アプリケーションのスケーリング操作がより効率的になります。

    Index Insight を使用するには、TiDB 専用クラスターの**[診断]**ページに移動し、 **[Index Insight BETA]**タブをクリックします。

    詳細については、 [Index Insight を使用する (ベータ版)](/tidb-cloud/index-insight.md)を参照してください。

-   登録やインストールを行わずに TiDB の全機能を体験できる対話型プラットフォーム[TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes)を紹介します。

    TiDB Playground は、スケーラビリティ、MySQL 互換性、リアルタイム分析などの TiDB の機能を探索するためのワンストップ ショップ エクスペリエンスを提供するように設計された対話型プラットフォームです。

    TiDB Playground を使用すると、複雑な構成を必要とせず、制御された環境で TiDB の機能をリアルタイムで試すことができるため、TiDB の機能を理解するのに最適です。

    TiDB Playground の使用を開始するには、 [**TiDB プレイグラウンド**](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes)ページに移動し、探索したい機能を選択して、探索を開始します。

## 2023 年 6 月 5 日 {#june-5-2023}

**一般的な変更点**

-   [データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)の GitHub への接続をサポートします。

    [データ アプリを GitHub に接続する](/tidb-cloud/data-service-manage-github-connection.md)により、データ アプリのすべての構成を Github 上で[コードファイル](/tidb-cloud/data-service-app-config-files.md)として管理できるようになり、 TiDB Cloudデータ サービスがシステムアーキテクチャおよび DevOps プロセスとシームレスに統合されます。

    この機能を使用すると、次のタスクを簡単に実行できるため、データ アプリ開発の CI/CD エクスペリエンスが向上します。

    -   GitHub を使用して Data App の変更を自動的にデプロイします。
    -   バージョン管理を使用して、GitHub 上のデータ アプリ変更の CI/CD パイプラインを構成します。
    -   接続されている GitHub リポジトリから切断します。
    -   導入前にエンドポイントの変更を確認します。
    -   導入履歴をビュー、障害が発生した場合に必要なアクションを実行します。
    -   コミットを再デプロイして、以前のデプロイメントにロールバックします。

    詳細については、 [GitHub を使用してデータ アプリを自動的にデプロイ](/tidb-cloud/data-service-manage-github-connection.md)を参照してください。

## 2023 年 6 月 2 日 {#june-2-2023}

**一般的な変更点**

-   簡素化と明確化を追求するため、製品名を更新しました。

    -   「TiDB CloudServerless Tier」は「TiDB サーバーレス」と呼ばれるようになりました。
    -   「TiDB CloudDedicated Tier」は「TiDB 専用」と呼ばれるようになりました。
    -   「TiDB オンプレミス」は「TiDB セルフホスト」と呼ばれるようになりました。

    新しくなった名前で、これまでと同じ素晴らしいパフォーマンスをお楽しみください。私たちはあなたの経験を最優先に考えています。

## 2023 年 5 月 30 日 {#may-30-2023}

**一般的な変更点**

-   TiDB Cloudのデータ移行機能の増分データ移行のサポートを強化します。

    binlog位置またはグローバル トランザクション識別子 (GTID) を指定して、指定された位置以降に生成された増分データのみをTiDB Cloudに複製できるようになりました。この機能強化により、特定の要件に合わせて、必要なデータをより柔軟に選択して複製できるようになります。

    詳細は[データ移行を使用して、MySQL 互換データベースからTiDB Cloudに増分データのみを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)を参照してください。

-   新しいイベント タイプ ( `ImportData` ) を[**イベント**](/tidb-cloud/tidb-cloud-events.md)ページに追加します。

-   TiDB Cloudコンソールから**Playground**を削除します。

    最適化されたエクスペリエンスを備えた新しいスタンドアロン プレイグラウンドにご期待ください。

## 2023 年 5 月 23 日 {#may-23-2023}

**一般的な変更点**

-   CSV ファイルを TiDB にアップロードする場合、列名を定義するために英語の文字と数字だけでなく、中国語や日本語などの文字も使用できます。ただし、特殊文字の場合は、アンダースコア ( `_` ) のみがサポートされます。

    詳細は[ローカル ファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

## 2023 年 5 月 16 日 {#may-16-2023}

**コンソールの変更**

-   専用層とサーバーレス層の両方について、機能カテゴリ別に整理された左側のナビゲーション エントリを紹介します。

    新しいナビゲーションにより、機能エントリをより簡単かつ直感的に見つけることができるようになります。新しいナビゲーションを表示するには、クラスターの概要ページにアクセスします。

-   Dedicated Tierクラスターの**[診断]**ページの次の 2 つのタブに対して、新しいネイティブ Web インフラストラクチャをリリースします。

    -   [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)
    -   [SQL文](/tidb-cloud/tune-performance.md#statement-analysis)

    新しいインフラストラクチャを使用すると、2 つのタブを簡単に移動して、より直観的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャによりユーザー エクスペリエンスも向上し、SQL 診断プロセスがより使いやすくなりました。

## 2023 年 5 月 9 日 {#may-9-2023}

**一般的な変更点**

-   2023 年 4 月 26 日以降に作成された GCP ホスト型クラスターのノード サイズの変更をサポートします。

    この機能を使用すると、需要の増加に合わせてより高性能のノードにアップグレードしたり、コストを節約するためにより低いパフォーマンスのノードにダウングレードしたりできます。この柔軟性の追加により、クラスターの容量をワークロードに合わせて調整し、コストを最適化することができます。

    詳細な手順については、 [ノードサイズの変更](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)を参照してください。

-   圧縮ファイルのインポートをサポートします。 CSV および SQL ファイルは、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、および`.snappy`の形式でインポートできます。この機能は、データをインポートするためのより効率的かつコスト効率の高い方法を提供し、データ転送コストを削減します。

    詳細については、 [Amazon S3 または GCS からTiDB Cloudに CSV ファイルをインポート](/tidb-cloud/import-csv-files.md)および[サンプルデータのインポート](/tidb-cloud/import-sample-data.md)を参照してください。

-   TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの新しいネットワーク アクセス管理オプションとして、AWS PrivateLink を利用したエンドポイント接続をサポートします。

    プライベート エンドポイント接続では、データがパブリック インターネットに公開されません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

    詳細については、 [プライベートエンドポイント接続のセットアップ](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。

**コンソールの変更**

-   新しいイベント タイプを[**イベント**](/tidb-cloud/tidb-cloud-events.md)ページに追加して、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのバックアップ、復元、変更フィード アクションを記録します。

    記録できるイベントの完全なリストを取得するには、 [記録されたイベント](/tidb-cloud/tidb-cloud-events.md#logged-events)を参照してください。

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)のクラスターの[**SQL診断**](/tidb-cloud/tune-performance.md)ページに**[SQL ステートメント]**タブを導入します。

    **[SQL ステートメント]**タブには次のものが表示されます。

    -   TiDB データベースによって実行されるすべての SQL ステートメントの包括的な概要。これにより、遅いクエリを簡単に特定して診断できます。
    -   クエリ時間、実行計画、データベースサーバーの応答など、各 SQL ステートメントに関する詳細情報を提供し、データベースのパフォーマンスの最適化に役立ちます。
    -   ユーザーフレンドリーなインターフェイスにより、大量のデータの並べ替え、フィルター、検索が簡単になり、最も重要なクエリに集中できるようになります。

    詳細については、 [ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)を参照してください。

## 2023 年 5 月 6 日 {#may-6-2023}

**一般的な変更点**

-   TiDB [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターが配置されているリージョン内の[データサービスエンドポイント](/tidb-cloud/tidb-cloud-glossary.md#endpoint)への直接アクセスをサポートします。

    新しく作成されたServerless Tierクラスターの場合、エンドポイント URL にクラスターのリージョン情報が含まれるようになりました。リージョン ドメイン`<region>.data.tidbcloud.com`をリクエストすると、TiDB クラスターが配置されているリージョンのエンドポイントに直接アクセスできます。

    あるいは、リージョンを指定せずにグローバル ドメイン`data.tidbcloud.com`をリクエストすることもできます。この方法で、 TiDB Cloudはリクエストを内部的にターゲット リージョンにリダイレクトしますが、これにより追加のレイテンシーが発生する可能性があります。この方法を選択した場合は、エンドポイントを呼び出すときに必ず`--location-trusted`オプションをcurl コマンドに追加してください。

    詳細については、 [エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)を参照してください。

## 2023 年 4 月 25 日 {#april-25-2023}

**一般的な変更点**

-   組織内の最初の 5 つの[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターに対して、 TiDB Cloud は各クラスターに次のように無料の使用クォータを提供します。

    -   行storage: 5 GiB
    -   [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月あたり 5,000 万 RU

    2023 年 5 月 31 日まで、Serverless Tierクラスターは引き続き無料で、100% 割引になります。それ以降、無料枠を超えた使用には料金が発生します。

    クラスターの**概要**ページの**[今月の使用量]**領域で簡単に[クラスターの使用状況を監視するか、使用量クォータを増やします](/tidb-cloud/manage-serverless-spend-limit.md#manage-spending-limit-for-tidb-serverless-clusters)できます。クラスターの無料クォータに達すると、クォータを増やすか、新しい月の初めに使用量がリセットされるまで、このクラスターでの読み取りおよび書き込み操作は抑制されます。

    さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク下りなど) の RU 消費量、料金の詳細、および調整された情報の詳細については、 [TiDB CloudServerless Tierの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

-   TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのバックアップと復元をサポートします。

    詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md)を参照してください。

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)から[v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)にアップグレードします。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの計画されたメンテナンス アクティビティを簡単にスケジュールおよび管理できるようにするメンテナンス ウィンドウ機能を提供します。

    メンテナンス ウィンドウとは、 TiDB Cloudサービスの信頼性、セキュリティ、パフォーマンスを確保するために、オペレーティング システムのアップデート、セキュリティ パッチ、インフラストラクチャのアップグレードなどの計画されたメンテナンス アクティビティが自動的に実行される指定された時間枠です。

    メンテナンス期間中は、一時的な接続の中断や QPS の変動が発生する可能性がありますが、クラスターは引き続き使用可能であり、SQL 操作、既存のデータのインポート、バックアップ、復元、移行、およびレプリケーションのタスクは通常どおり実行できます。メンテナンス中は[許可される操作と禁止される操作のリスト](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)を参照してください。

    メンテナンスの頻度を最小限に抑えるよう努めてまいります。メンテナンス期間が計画されている場合、デフォルトの開始時刻は対象週の水曜日の 03:00 ( TiDB Cloud組織のタイムゾーンに基づく) です。潜在的な中断を回避するには、メンテナンスのスケジュールを認識し、それに応じて運用を計画することが重要です。

    -   常に最新の情報を入手できるように、 TiDB Cloudはメンテナンス期間ごとに 3 回の電子メール通知を送信します (メンテナンス タスクの前に 1 回、メンテナンス タスクの開始前に 1 回、メンテナンス タスクの後に 1 回)。
    -   メンテナンスの影響を最小限に抑えるために、 **[メンテナンス]**ページでメンテナンスの開始時刻を希望の時刻に変更するか、メンテナンス アクティビティを延期することができます。

    詳細については、 [メンテナンスウィンドウの構成](/tidb-cloud/configure-maintenance-window.md)を参照してください。

-   AWS でホストされ、2023 年 4 月 25 日以降に作成された[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの TiDB ノードをスケーリングするときに、TiDB のロード バランシングを改善し、接続ドロップを削減します。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は、AWS でホストされているすべてのDedicated Tierクラスターに提供されています。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャを使用すると、 [監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ内を簡単に移動し、より直感的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは、UX に関する多くの問題も解決し、監視プロセスをより使いやすくしています。

## 2023 年 4 月 18 日 {#april-18-2023}

**一般的な変更点**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターに対して[データ移行ジョブの仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)スケールアップまたはスケールダウンをサポートします。

    この機能を使用すると、仕様をスケールアップして移行パフォーマンスを向上させたり、仕様をスケールダウンしてコストを削減したりできます。

    詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)を参照してください。

**コンソールの変更**

-   UI を刷新して[クラスターの作成](https://tidbcloud.com/console/clusters/create-cluster)エクスペリエンスをさらに使いやすくし、数回クリックするだけでクラスターを作成および構成できるようにしました。

    新しいデザインはシンプルさを重視し、視覚的な煩雑さを軽減し、明確な指示を提供します。クラスター作成ページで**「作成」**をクリックすると、クラスターの作成が完了するまで待つことなく、クラスターの概要ページに移動します。

    詳細については、 [クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

-   **[請求**] ページに**[割引]**タブを導入して、組織の所有者と請求管理者向けの割引情報を表示します。

    詳細については、 [割引](/tidb-cloud/tidb-cloud-billing.md#discounts)を参照してください。

## 2023 年 4 月 11 日 {#april-11-2023}

**一般的な変更点**

-   TiDB のロード バランスを改善し、AWS でホストされている[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの TiDB ノードをスケールする際の接続ドロップを削減します。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は、AWS `Oregon (us-west-2)`リージョンでホストされているDedicated Tierクラスターに対してのみ提供されています。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターに対して[ニューレリック](https://newrelic.com/)統合をサポートします。

    New Relic の統合を使用すると、TiDB クラスターのメトリクス データを[ニューレリック](https://newrelic.com/)に送信するようにTiDB Cloudを構成できます。その後、アプリケーションのパフォーマンスと TiDB データベースのパフォーマンスの両方を[ニューレリック](https://newrelic.com/)で監視および分析できます。この機能は、潜在的な問題を迅速に特定してトラブルシューティングし、解決時間を短縮するのに役立ちます。

    統合手順と利用可能なメトリクスについては、 [TiDB Cloudと New Relic を統合する](/tidb-cloud/monitor-new-relic-integration.md)を参照してください。

-   次の[チェンジフィード](/tidb-cloud/changefeed-overview.md)メトリクスを、Dedicated Tierクラスターの Prometheus 統合に追加します。

    -   `tidbcloud_changefeed_latency`
    -   `tidbcloud_changefeed_replica_rows`

    [TiDB Cloudと Prometheus を統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)がある場合は、これらのメトリクスを使用して、変更フィードのパフォーマンスと健全性をリアルタイムで監視できます。さらに、Prometheus を使用してメトリクスを監視するアラートを簡単に作成できます。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページを更新して、 [ノードレベルのリソースメトリック](/tidb-cloud/built-in-monitoring.md#server)を使用します。

    ノードレベルのリソースメトリクスを使用すると、リソース消費をより正確に表示して、購入したサービスの実際の使用状況をより深く理解できます。

    これらのメトリックにアクセスするには、クラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページに移動し、 **[メトリック]**タブの [**サーバー]**カテゴリを確認します。

-   **「プロジェクト別集計」**と**「サービス別集計」**の請求項目を再整理し、請求内容をよりわかりやすく[請求する](/tidb-cloud/tidb-cloud-billing.md#billing-details)ページを最適化しました。

## 2023 年 4 月 4 日 {#april-4-2023}

**一般的な変更点**

-   誤検知を防ぐために、次の 2 つのアラートを[TiDB Cloudの組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions)から削除します。これは、ノードの 1 つで一時的にオフラインまたはメモリ不足 (OOM) の問題が発生しても、クラスター全体の健全性には大きな影響を与えないためです。

    -   クラスター内の少なくとも 1 つの TiDB ノードでメモリが不足しました。
    -   1 つ以上のクラスター ノードがオフラインです。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの[アラート](/tidb-cloud/monitor-built-in-alerting.md)ページを導入します。このページには、各Dedicated Tierクラスターのアクティブなアラートとクローズされたアラートの両方がリストされます。

    **[アラート]**ページには次の情報が表示されます。

    -   直感的でユーザーフレンドリーなユーザーインターフェイス。アラート通知メールを購読していない場合でも、このページでクラスターのアラートを表示できます。
    -   高度なフィルタリング オプションにより、重大度、ステータス、その他の属性に基づいてアラートを迅速に検索して並べ替えることができます。また、過去 7 日間の履歴データを表示できるため、アラート履歴の追跡が容易になります。
    -   **ルールの編集**機能。クラスター固有のニーズに合わせてアラート ルール設定をカスタマイズできます。

    詳細については、 [TiDB Cloudの組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)を参照してください。

-   TiDB Cloudのヘルプ関連の情報とアクションを 1 か所に統合​​します。

    これで、 [TiDB Cloudのヘルプ情報](/tidb-cloud/tidb-cloud-support.md)すべて取得し、 **「?」**をクリックしてサポートに問い合わせることができます。 [TiDB Cloudコンソール](https://tidbcloud.com/)の右下隅にあります。

-   TiDB Cloudについて学ぶのに役立つ[はじめる](https://tidbcloud.com/console/getting-started)ページを紹介します。

    **「はじめに」**ページでは、インタラクティブなチュートリアル、重要なガイド、便利なリンクが提供されます。インタラクティブなチュートリアルに従うことで、事前に構築された業界固有のデータセット (Steam ゲーム データセットおよび S&amp;P 500 データセット) を使用してTiDB Cloud機能と HTAP 機能を簡単に探索できます。

    **「はじめに」**ページにアクセスするには、 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> [TiDB Cloudコンソール](https://tidbcloud.com/)の左側のナビゲーション バーにある**「はじめに**」。このページでは、 **「クエリ サンプル データセット」**をクリックして対話型チュートリアルを開いたり、他のリンクをクリックしてTiDB Cloudを探索したりできます。または、 **「?」**をクリックすることもできます。右下隅の をクリックし、 **「対話型チュートリアル」**をクリックします。

## 2023 年 3 月 29 日 {#march-29-2023}

**一般的な変更点**

-   [データサービス（ベータ版）](/tidb-cloud/data-service-overview.md)データ アプリのより詳細なアクセス制御をサポートします。

    データ アプリの詳細ページで、クラスターをデータ アプリにリンクし、各 API キーのロールを指定できるようになりました。このロールは、API キーがリンクされたクラスターに対してデータの読み取りまたは書き込みができるかどうかを制御し、 `ReadOnly`または`ReadAndWrite`に設定できます。この機能は、データ アプリに対してクラスター レベルおよびアクセス許可レベルのアクセス制御を提供し、ビジネス ニーズに応じてアクセス スコープをより柔軟に制御できるようにします。

    詳細については、 [リンクされたクラスターを管理する](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)および[APIキーを管理する](/tidb-cloud/data-service-api-key.md)を参照してください。

## 2023 年 3 月 28 日 {#march-28-2023}

**一般的な変更点**

-   [変更フィード](/tidb-cloud/changefeed-overview.md)に 2 RCU、4 RCU、8 RCU の仕様を追加し、 [変更フィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)場合に希望の仕様の選択をサポートします。

    これらの新しい仕様を使用すると、以前は 16 個の RCU が必要だったシナリオと比較して、データ レプリケーション コストを最大 87.5% 削減できます。

-   2023 年 3 月 28 日以降に作成された[変更フィード](/tidb-cloud/changefeed-overview.md)仕様のスケールアップまたはスケールダウンをサポートします。

    より高い仕様を選択することでレプリケーションのパフォーマンスを向上させることができ、より低い仕様を選択することでレプリケーションのコストを削減することができます。

    詳細については、 [チェンジフィードをスケールする](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)を参照してください。

-   AWS の[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターから同じプロジェクトおよび同じリージョンの[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターへの増分データのリアルタイムのレプリケートをサポートします。

    詳細については、 [TiDB Cloudへのシンク](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)を参照してください。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスタの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)の機能に対して 2 つの新しい GCP リージョン ( `Singapore (asia-southeast1)`と`Oregon (us-west1)`をサポートします。

    これらの新しいリージョンを使用すると、データをTiDB Cloudに移行するためのオプションが増えます。アップストリーム データがこれらのリージョンまたはその近くに保存されている場合は、GCP からTiDB Cloudへのより高速で信頼性の高いデータ移行を利用できるようになります。

    詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの[遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    この新しいインフラストラクチャを使用すると、 [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ページ内を簡単に移動し、より直観的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは UX に関する多くの問題も解決し、SQL 診断プロセスをより使いやすくしています。

## 2023 年 3 月 21 日 {#march-21-2023}

**一般的な変更点**

-   [データサービス（ベータ版）](https://tidbcloud.com/console/data-service)クラスター[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)導入すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でデータにアクセスできるようになります。

    Data Service を使用すると、 TiDB Cloud をHTTPS と互換性のあるアプリケーションまたはサービスとシームレスに統合できます。以下に、一般的なシナリオをいくつか示します。

    -   モバイルまたは Web アプリケーションから TiDB クラスターのデータベースに直接アクセスします。
    -   サーバーレス エッジ関数を使用してエンドポイントを呼び出し、データベース接続プーリングによって引き起こされるスケーラビリティの問題を回避します。
    -   Data Service をデータ ソースとして使用して、 TiDB Cloudをデータ視覚化プロジェクトと統合します。
    -   MySQL インターフェースがサポートしていない環境からデータベースに接続します。

    さらに、 TiDB Cloud は、AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェイス[Chat2Query API](/tidb-cloud/use-chat2query-api.md)を提供します。

    Data Service にアクセスするには、左側のナビゲーション ペインの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。詳細については、次のドキュメントを参照してください。

    -   [データサービスの概要](/tidb-cloud/data-service-overview.md)
    -   [データサービスを始めてみる](/tidb-cloud/data-service-get-started.md)
    -   [Chat2Query API を使ってみる](/tidb-cloud/use-chat2query-api.md)

-   AWS でホストされ、2022 年 12 月 31 日以降に作成された[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)のクラスターにスケールインするために、TiDB、TiKV、およびTiFlashノードのサイズを縮小することをサポートします。

    ノード サイズを[TiDB Cloudコンソール経由](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)または[TiDB CloudAPI (ベータ版) 経由](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)減らすことができます。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)のクラスタの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能に対して新しい GCP リージョンをサポートします: `Tokyo (asia-northeast1)` 。

    この機能は、Google Cloud Platform (GCP) の MySQL 互換データベースから TiDB クラスターにデータを簡単かつ効率的に移行するのに役立ちます。

    詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの**「イベント」**ページを導入します。このページには、クラスターに対する主な変更の記録が表示されます。

    このページでは、過去 7 日間のイベント履歴を表示し、トリガー時間やアクションを開始したユーザーなどの重要な詳細を追跡できます。たとえば、クラスターがいつ一時停止されたか、誰がクラスター サイズを変更したかなどのイベントを表示できます。

    詳細については、 [TiDB Cloudクラスター イベント](/tidb-cloud/tidb-cloud-events.md)を参照してください。

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの**[監視]**ページに**[データベース ステータス]**タブを追加します。これには、次のデータベース レベルのメトリックが表示されます。

    -   DBごとのQPS
    -   DBごとの平均クエリ継続時間
    -   DBごとの失敗したクエリ数

    これらのメトリクスを使用すると、個々のデータベースのパフォーマンスを監視し、データに基づいて意思決定を行い、アプリケーションのパフォーマンスを向上させるためのアクションを実行できます。

    詳細については、 [Serverless Tierクラスターのモニタリングメトリクス](/tidb-cloud/built-in-monitoring.md)を参照してください。

## 2023 年 3 月 14 日 {#march-14-2023}

**一般的な変更点**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0)から[v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)にアップグレードします。

-   ヘッダー行を含むローカル CSV ファイルをアップロードするときに、 TiDB Cloudによって作成されるターゲット テーブルの列名の変更をサポートします。

    ヘッダー行を含むローカル CSV ファイルを[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターにインポートするときに、ターゲット テーブルの作成にTiDB Cloudが必要で、ヘッダー行の列名がTiDB Cloud列の命名規則に従っていない場合は、次に警告アイコンが表示されます。対応する列名に。この警告を解決するには、アイコンの上にカーソルを移動し、メッセージに従って既存の列名を編集するか、新しい列名を入力します。

    列の命名規則については、 [ローカルファイルをインポートする](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)を参照してください。

## 2023 年 3 月 7 日 {#march-7-2023}

**一般的な変更点**

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのデフォルトの TiDB バージョンを[v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)から[v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)にアップグレードします。

## 2023 年 2 月 28 日 {#february-28-2023}

**一般的な変更点**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターに[SQL診断](/tidb-cloud/tune-performance.md)機能を追加します。

    SQL 診断を使用すると、SQL 関連のランタイム ステータスについて深い洞察を得ることができ、SQL パフォーマンス チューニングをより効率的に行うことができます。現在、Serverless Tierの SQL 診断機能は低速クエリ データのみを提供します。

    SQL 診断を使用するには、Serverless Tierクラスター ページの左側のナビゲーション バーで**[SQL 診断]**をクリックします。

**コンソールの変更**

-   左側のナビゲーションを最適化します。

    たとえば、次のようにページをより効率的に移動できます。

    -   左上隅にマウスを置くと、クラスターまたはプロジェクトをすばやく切り替えることができます。
    -   **「クラスター」**ページと**「管理者」**ページを切り替えることができます。

**APIの変更**

-   データインポート用にいくつかのTiDB Cloud API エンドポイントをリリース：

    -   すべてのインポートタスクをリストする
    -   インポートタスクを取得する
    -   インポートタスクを作成する
    -   インポートタスクを更新する
    -   インポートタスク用のローカルファイルをアップロードする
    -   インポートタスクを開始する前にデータをプレビューする
    -   インポートタスクのロール情報を取得する

    詳細については、 [APIドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import)を参照してください。

## 2023 年 2 月 22 日 {#february-22-2023}

**一般的な変更点**

-   [コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)機能を使用して、組織内のメンバーが実行するさまざまなアクティビティを追跡することをサポートします。 [TiDB Cloudコンソール](https://tidbcloud.com/) .

    コンソール監査ログ機能は、ロール`Owner`または`Audit Admin`を持つユーザーのみに表示され、デフォルトでは無効になっています。有効にするには、<mdsvgicon name="icon-top-organization"> [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある**[組織]** &gt; **[コンソール監査ログ]** 。</mdsvgicon>

    コンソール監査ログを分析すると、組織内で実行された不審な操作を特定できるため、組織のリソースとデータのセキュリティが向上します。

    詳細については、 [コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)を参照してください。

**CLIの変更**

-   新しいコマンド[`ticloud cluster connect-info`](/tidb-cloud/ticloud-cluster-connect-info.md) for [TiDB CloudCLI](/tidb-cloud/cli-reference.md)を追加します。

    `ticloud cluster connect-info`は、クラスターの接続文字列を取得できるコマンドです。このコマンドを使用するには、 [`ticloud`を更新する](/tidb-cloud/ticloud-update.md) ～ v0.3.2 以降のバージョンが必要です。

## 2023 年 2 月 21 日 {#february-21-2023}

**一般的な変更点**

-   データをTiDB Cloudにインポートするときに、 IAMユーザーの AWS アクセス キーを使用して Amazon S3 バケットにアクセスすることをサポートします。

    この方法は、ロール ARN を使用するよりも簡単です。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

-   [モニタリングメトリクスの保持期間](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 2 日間からさらに長い期間に延長します。

    -   Dedicated Tierクラスターの場合、過去 7 日間のメトリック データを表示できます。
    -   Serverless Tierクラスターの場合、過去 3 日間のメトリック データを表示できます。

    メトリクスの保持期間を延長することで、より多くの履歴データにアクセスできるようになりました。これは、クラスターの傾向とパターンを特定して、より適切な意思決定と迅速なトラブルシューティングを行うのに役立ちます。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの [監視] ページで新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャを使用すると、[監視] ページを簡単に移動して、より直観的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは UX に関する多くの問題も解決し、監視プロセスをより使いやすくしています。

## 2023 年 2 月 17 日 {#february-17-2023}

**CLIの変更**

-   新しいコマンド[`ticloud connect`](/tidb-cloud/ticloud-connect.md) for [TiDB CloudCLI](/tidb-cloud/cli-reference.md)を追加します。

    `ticloud connect`は、SQL クライアントをインストールせずにローカル マシンからTiDB Cloudクラスターに接続できるようにするコマンドです。 TiDB Cloudクラスターに接続した後、 TiDB Cloud CLI で SQL ステートメントを実行できます。

## 2023 年 2 月 14 日 {#february-14-2023}

**一般的な変更点**

-   TiDB [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスター内でスケールするために TiKV およびTiFlashノードの数を減らすことをサポートします。

    ノード番号[TiDB Cloudコンソール経由](/tidb-cloud/scale-tidb-cluster.md#change-node-number)または[TiDB CloudAPI (ベータ版) 経由](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)を減らすことができます。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)のクラスターの**モニタリング**ページを紹介します。

    [**モニタリング]**ページには、1 秒あたりに実行された SQL ステートメントの数、クエリの平均継続時間、失敗したクエリの数など、さまざまなメトリックとデータが表示されます。これは、Serverless Tierにおける SQL ステートメントの全体的なパフォーマンスをより深く理解するのに役立ちます。集まる。

    詳細については、 [TiDB Cloudの組み込みモニタリング](/tidb-cloud/built-in-monitoring.md)を参照してください。

## 2023 年 2 月 2 日 {#february-2-2023}

**CLIの変更**

-   TiDB Cloud CLI クライアントの紹介[`ticloud`](/tidb-cloud/cli-reference.md) 。

    `ticloud`を使用すると、数行のコマンドでターミナルまたはその他の自動ワークフローからTiDB Cloudリソースを簡単に管理できます。特に GitHub Actions については、 `ticloud`簡単にセットアップできるように[`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli)用意しました。

    詳細については、 [TiDB CloudCLI クイック スタート](/tidb-cloud/get-started-with-cli.md)および[TiDB CloudCLI リファレンス](/tidb-cloud/cli-reference.md)を参照してください。

## 2023 年 1 月 18 日 {#january-18-2023}

**一般的な変更点**

-   Microsoft アカウントで[サインアップ](https://tidbcloud.com/free-trial) TiDB Cloudをサポートします。

## 2023 年 1 月 17 日 {#january-17-2023}

**一般的な変更点**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3)から[v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0)にアップグレードします。

-   新規サインアップ ユーザーの場合、 TiDB Cloud は無料の[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターを自動的に作成するため、 TiDB Cloudを使用したデータ探索の旅をすぐに開始できます。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの新しい AWS リージョンをサポートします: `Seoul (ap-northeast-2)` 。

    このリージョンでは次の機能が有効になっています。

    -   [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    -   [チェンジフィードを使用してTiDB Cloudから他のデータ サービスにデータをストリーミングする](/tidb-cloud/changefeed-overview.md)
    -   [TiDB クラスターデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)

## 2023 年 1 月 10 日 {#january-10-2023}

**一般的な変更点**

-   ローカル CSV ファイルから TiDB にデータをインポートする機能を最適化し、 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのユーザー エクスペリエンスを向上させます。

    -   CSV ファイルをアップロードするには、**インポート**ページのアップロード領域にドラッグ アンド ドロップするだけで済みます。
    -   インポート タスクを作成するときに、ターゲット データベースまたはテーブルが存在しない場合は、名前を入力すると、 TiDB Cloudによって自動的に作成されます。作成するターゲット テーブルでは、主キーを指定するか、複数のフィールドを選択して複合主キーを形成できます。
    -   インポートが完了したら、 **「Chat2Query でデータを探索」**をクリックするか、タスク リストでターゲット テーブル名をクリックすると、 [AI を活用した Chat2Query](/tidb-cloud/explore-data-with-chat2query.md)でデータを探索できます。

    詳細については、 [ローカル ファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

**コンソールの変更**

-   各クラスターに**[Get Support]**オプションを追加して、特定のクラスターのサポートをリクエストするプロセスを簡素化します。

    次のいずれかの方法でクラスターのサポートをリクエストできます。

    -   プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページで、クラスターの行にある**[...]**をクリックし、 **[Get Support]**を選択します。
    -   クラスターの概要ページで、右上隅にある**[...]**をクリックし、 **[サポートを受ける]**を選択します。

## 2023 年 1 月 5 日 {#january-5-2023}

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの SQL Editor (ベータ) の名前を Chat2Query (ベータ) に変更し、AI を使用した SQL クエリの生成をサポートします。

    Chat2Query では、AI に SQL クエリを自動的に生成させることも、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することもできます。

    Chat2Query にアクセスするには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、クラスター名をクリックして、左側のナビゲーション ウィンドウで**[Chat2Query]**をクリックします。

## 2023 年 1 月 4 日 {#january-4-2023}

**一般的な変更点**

-   AWS でホストされ、2022 年 12 月 31 日以降に作成された TiDB 専用クラスターの**ノード サイズ (vCPU + RAM)**を増やすことで、TiDB、TiKV、およびTiFlashノードのスケールアップをサポートします。

    ノード サイズを[TiDB Cloudコンソールの使用](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)または[TiDB CloudAPI (ベータ版) を使用する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)に増やすことができます。

-   [**監視**](/tidb-cloud/built-in-monitoring.md)ページのメトリクスの保持期間を 2 日に延長します。

    過去 2 日間のメトリクス データにアクセスできるようになり、クラスターのパフォーマンスと傾向をより柔軟に把握できるようになりました。

    この改善には追加コストはかからず、クラスターの[**監視**](/tidb-cloud/built-in-monitoring.md)ページの**[診断]**タブからアクセスできます。これは、パフォーマンスの問題を特定してトラブルシューティングし、クラスター全体の状態をより効果的に監視するのに役立ちます。

-   Prometheus 統合のための Grafana ダッシュボード JSON のカスタマイズをサポートします。

    [TiDB Cloudと Prometheus を統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)お持ちの場合は、事前に構築された Grafana ダッシュボードをインポートしてTiDB Cloudクラスターを監視し、ニーズに合わせてダッシュボードをカスタマイズできるようになりました。この機能により、 TiDB Cloudクラスターの簡単かつ迅速なモニタリングが可能になり、パフォーマンスの問題を迅速に特定するのに役立ちます。

    詳細については、 [Grafana GUI ダッシュボードを使用してメトリクスを視覚化する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)を参照してください。

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのデフォルトの TiDB バージョンを[v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。Serverless Tierクラスターのデフォルトの TiDB バージョンを v6.4.0 にアップグレードした後のコールド スタートの問題は解決されました。

**コンソールの変更**

-   [**クラスター**](https://tidbcloud.com/console/clusters)ページとクラスター概要ページの表示を簡素化します。

    -   [**クラスター**](https://tidbcloud.com/console/clusters)ページのクラスター名をクリックすると、クラスターの概要ページに移動し、クラスターの操作を開始できます。
    -   クラスターの概要ページから**[接続] ペイン**と**[インポート]**ペインを削除します。右上隅の**「接続」**をクリックして接続情報を取得し、左側のナビゲーション・ペインで**「インポート」**をクリックしてデータをインポートできます。
