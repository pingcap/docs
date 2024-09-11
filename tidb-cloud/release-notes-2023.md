---
title: TiDB Cloud Release Notes in 2023
summary: 2023 年のTiDB Cloudのリリース ノートについて説明します。
---

# 2023 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2023}

このページには、2023 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2023年12月5日 {#december-5-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)すると、失敗した変更フィードを再開できるため、新しい変更フィードを再作成する手間が省けます。

    詳細については[チェンジフィードの状態](/tidb-cloud/changefeed-overview.md#changefeed-states)参照してください。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)の接続エクスペリエンスを強化します。

    **接続**ダイアログ インターフェースを改良し、 TiDB Cloud Serverless ユーザーに、よりスムーズで効率的な接続エクスペリエンスを提供します。さらに、 TiDB Cloud Serverless では、より多くのクライアント タイプが導入され、接続に必要なブランチを選択できるようになりました。

    詳細については[TiDB Cloud Serverlessに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)参照してください。

## 2023年11月28日 {#november-28-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)バックアップからの SQL バインディングの復元をサポートします。

    TiDB Cloud Dedicated では、バックアップから復元するときに、デフォルトでユーザー アカウントと SQL バインディングが復元されるようになりました。この機能強化は、v6.2.0 以降のバージョンのクラスターで利用でき、データ復元プロセスを効率化します。SQL バインディングの復元により、クエリ関連の構成と最適化がスムーズに再統合され、より包括的で効率的な復元エクスペリエンスが提供されます。

    詳細については[TiDB Cloud Dedicatedデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) SQL ステートメントの RU コストの監視をサポートします。

    TiDB Cloud Serverless では、 [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) SQL ステートメントの詳細な分析情報が提供されるようになりました。SQL ステートメントごとの合計**RU**コストと**平均 RU**コストの両方を表示できます。この機能は、RU コストを特定して分析するのに役立ち、運用における潜在的なコスト削減の機会を提供します。

    SQL ステートメントの RU の詳細を確認するには、 [TiDB Cloud Serverless クラスター](https://tidbcloud.com/console/clusters)の**診断**ページに移動し、 **SQL ステートメント**タブをクリックします。

## 2023年11月21日 {#november-21-2023}

**一般的な変更**

-   [データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 、Google Cloud にデプロイされた TiDB クラスタの高速物理モードをサポートします。

    AWS および Google Cloud にデプロイされた TiDB クラスターに物理モードを使用できるようになりました。物理モードの移行速度は最大 110 MiB/s に達し、論理モードの 2.4 倍の速度です。パフォーマンスが向上したため、大規模なデータセットをTiDB Cloudに迅速に移行できます。

    詳細については[既存データと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)参照してください。

## 2023年11月14日 {#november-14-2023}

**一般的な変更**

-   TiDB Cloud Dedicated クラスターからデータを復元する場合、デフォルトの動作が、ユーザー アカウントなしでの復元からすべてのユーザー アカウントでの復元に変更されました。

    詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

-   変更フィード用のイベント フィルターを導入します。

    この機能強化により、 [TiDB Cloudコンソール](https://tidbcloud.com/)を介して直接変更フィードのイベント フィルターを簡単に管理できるようになり、変更フィードから特定のイベントを除外するプロセスが効率化され、下流のデータ レプリケーションをより適切に制御できるようになります。

    詳細については[チェンジフィード](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)参照してください。

## 2023年11月7日 {#november-7-2023}

**一般的な変更**

-   次のリソース使用状況アラートを追加します。新しいアラートはデフォルトでは無効になっています。必要に応じて有効にすることができます。

    -   TiDB ノード全体の最大メモリ使用率が 10 分間 70% を超えました
    -   TiKV ノード全体の最大メモリ使用率が 10 分間 70% を超えました
    -   TiDB ノード全体の最大 CPU 使用率が 10 分間 80% を超えました
    -   TiKV ノード全体の最大 CPU 使用率が 10 分間 80% を超えました

    詳細については[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md#resource-usage-alerts)参照してください。

## 2023年10月31日 {#october-31-2023}

**一般的な変更**

-   営業担当者に連絡せずに、 TiDB Cloudコンソールでエンタープライズ サポート プランに直接アップグレードできます。

    詳細については[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)参照してください。

## 2023年10月25日 {#october-25-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 、Google Cloud でのデュアル リージョン バックアップ (ベータ版) をサポートします。

    Google Cloud でホストされているTiDB Cloud Dedicated クラスタは、Google Cloud Storage とシームレスに連携します。Google Cloud Storage の[デュアルリージョン](https://cloud.google.com/storage/docs/locations#location-dr)機能と同様に、 TiDB Cloud Dedicated のデュアルリージョンに使用するリージョンのペアは、同じマルチリージョン内にある必要があります。たとえば、東京と大阪は同じマルチリージョン`ASIA`内にあるため、デュアルリージョンstorageに一緒に使用できます。

    詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)参照してください。

-   [データ変更ログを Apache Kafka にストリーミングする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)の機能は現在、一般提供 (GA) になっています。

    10 か月のベータ トライアルが成功した後、 TiDB Cloudから Apache Kafka にデータ変更ログをストリーミングする機能が一般公開されました。TiDB からメッセージ キューにデータをストリーミングすることは、データ統合シナリオでよく必要なことです。Kafka シンクを使用して、他のデータ処理システム (Snowflake など) と統合したり、ビジネス消費をサポートしたりできます。

    詳細については[チェンジフィードの概要](/tidb-cloud/changefeed-overview.md)参照してください。

## 2023年10月11日 {#october-11-2023}

**一般的な変更**

-   AWS にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスターのうち[デュアルリージョンバックアップ（ベータ版）](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)をサポートします。

    クラウド プロバイダー内の地理的リージョン間でバックアップを複製できるようになりました。この機能により、データ保護と災害復旧機能のレイヤーが追加されます。

    詳細については[TiDB Cloud Dedicatedデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

-   データ移行では、既存のデータの移行に物理モードと論理モードの両方がサポートされるようになりました。

    物理モードでは、移行速度は最大 110 MiB/秒に達します。論理モードの 45 MiB/秒と比較すると、移行パフォーマンスが大幅に向上しています。

    詳細については[既存データと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)参照してください。

## 2023年10月10日 {#october-10-2023}

**一般的な変更**

-   TiDB Cloud Vercel 統合により、 [Vercel プレビュー デプロイメント](https://vercel.com/docs/deployments/preview-deployments)でのTiDB Cloud Serverless ブランチの使用をサポートします。

    詳細については[TiDB Cloud Serverlessブランチに接続](/tidb-cloud/integrate-tidbcloud-with-vercel.md#connect-with-tidb-cloud-serverless-branching)参照してください。

## 2023年9月28日 {#september-28-2023}

**APIの変更**

-   特定の組織の特定の月の請求書を取得するためのTiDB Cloud Billing API エンドポイントを導入します。

    この Billing API エンドポイントは、 TiDB Cloudの最新の API バージョンであるTiDB Cloud API v1beta1 でリリースされています。詳細については、 [API ドキュメント (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1#tag/Billing)を参照してください。

## 2023年9月19日 {#september-19-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターから 2 つの vCPU TiDB ノードと TiKV ノードを削除します。

    2 vCPU オプションは**、 [クラスタの作成]**ページまたは**[クラスタの変更]**ページで使用できなくなりました。

-   JavaScript のリリース[TiDB Cloudサーバーレス ドライバー (ベータ版)](/tidb-cloud/serverless-driver.md) 。

    JavaScript 用のTiDB Cloudサーバーレス ドライバーを使用すると、HTTPS 経由で[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに接続できます。これは、 [Vercelエッジ機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare ワーカー](https://workers.cloudflare.com/)など、TCP 接続が制限されているエッジ環境で特に役立ちます。

    詳細については[TiDB Cloudサーバーレス ドライバー (ベータ版)](/tidb-cloud/serverless-driver.md)参照してください。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの場合、 **「今月の使用量」**パネルまたは支出限度額の設定時にコストの見積もりを取得できます。

## 2023年9月5日 {#september-5-2023}

**一般的な変更**

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)では、さまざまな状況での特定のレート制限要件を満たすために、各 API キーのレート制限をカスタマイズすることがサポートされています。

    キーを[作成する](/tidb-cloud/data-service-api-key.md#create-an-api-key)または[編集](/tidb-cloud/data-service-api-key.md#edit-an-api-key)すると、API キーのレート制限を調整できます。

    詳細については[レート制限](/tidb-cloud/data-service-api-key.md#rate-limiting)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい AWS リージョンをサポートします: サンパウロ (sa-east-1)。

-   1 つ[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターごとに最大 100 個の IP アドレスを IP アクセス リストに追加することをサポートします。

    詳細については[IPアクセスリストを構成する](/tidb-cloud/configure-ip-access-list.md)参照してください。

**コンソールの変更**

-   クラスターの主な変更の記録を提供する、 [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの**イベント**ページを紹介します。

    このページでは、過去 7 日間のイベント履歴を表示し、トリガー時間やアクションを開始したユーザーなどの重要な詳細を追跡できます。

    詳細については[TiDB Cloudクラスター イベント](/tidb-cloud/tidb-cloud-events.md)参照してください。

**APIの変更**

-   [AWS プライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)または[Google Cloud プライベート サービス接続](https://cloud.google.com/vpc/docs/private-service-connect) for [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを管理するためのTiDB Cloud API エンドポイントをいくつかリリースします。

    -   クラスターのプライベート エンドポイント サービスを作成する
    -   クラスターのプライベート エンドポイント サービス情報を取得する
    -   クラスターのプライベートエンドポイントを作成する
    -   クラスターのすべてのプライベートエンドポイントを一覧表示する
    -   プロジェクト内のすべてのプライベート エンドポイントを一覧表示する
    -   クラスターのプライベートエンドポイントを削除する

    詳細については、 [APIドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster)を参照してください。

## 2023年8月23日 {#august-23-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに対して Google Cloud [プライベートサービス接続](https://cloud.google.com/vpc/docs/private-service-connect)をサポートします。

    プライベート エンドポイントを作成し、Google Cloud でホストされているTiDB Cloud Dedicated クラスタへの安全な接続を確立できるようになりました。

    主な利点:

    -   直感的な操作: わずか数ステップでプライベート エンドポイントを作成できます。
    -   強化されたセキュリティ: 安全な接続を確立してデータを保護します。
    -   パフォーマンスの向上: 低遅延かつ高帯域幅の接続を実現します。

    詳細については[プライベートエンドポイント経由で Google Cloud に接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターから[Google クラウド ストレージ (GCS)](https://cloud.google.com/storage)クラスターにデータをストリーミングするための変更フィードの使用をサポートします。

    自分のアカウントのバケットを使用し、正確に調整された権限を提供することで、 TiDB Cloudから GCS にデータをストリーミングできるようになりました。データを GCS に複製した後、必要に応じてデータの変更を分析できます。

    詳細については[クラウドストレージに保存](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

## 2023年8月15日 {#august-15-2023}

**一般的な変更**

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)開発エクスペリエンスを向上させるために`GET`のリクエストのページネーションをサポートします。

    `GET`リクエストの場合、 **Advance Properties**で**ページ分割**を有効にし、エンドポイントを呼び出すときにクエリ パラメータとして`page`と`page_size`を指定することにより、結果をページ分割できます。たとえば、1 ページあたり 10 項目の 2 ページ目を取得するには、次のコマンドを使用します。

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>?page=2&page_size=10'
    ```

    この機能は、最後のクエリが`SELECT`ステートメントである`GET`リクエストに対してのみ使用できることに注意してください。

    詳細については[エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)参照してください。

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service) 、指定された有効期間 (TTL) にわたって`GET`の要求のエンドポイント応答をキャッシュすることをサポートします。

    この機能により、データベースの負荷が軽減され、エンドポイントのレイテンシーが最適化されます。

    `GET`リクエスト メソッドを使用するエンドポイントの場合、**キャッシュ レスポンス**を有効にし、**詳細プロパティ**でキャッシュの TTL 期間を設定できます。

    詳細については[高度なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)参照してください。

-   AWS でホストされ、2023 年 8 月 15 日以降に作成された[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの負荷分散の改善を無効にします。これには以下が含まれます。

    -   AWS でホストされている TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行するのを無効にします。
    -   AWS でホストされている TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行するのを無効にします。

    この変更により、ハイブリッド展開のリソース競合が回避され、この改善が有効になっている既存のクラスターには影響しません。新しいクラスターで負荷分散の改善を有効にする場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## 2023年8月8日 {#august-8-2023}

**一般的な変更**

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)では Basic 認証がサポートされるようになりました。

    [「基本」HTTP認証](https://datatracker.ietf.org/doc/html/rfc7617)を使用して、リクエストで公開キーをユーザー名として、秘密キーをパスワードとして提供できます。ダイジェスト認証と比較して、基本認証はよりシンプルで、データ サービス エンドポイントを呼び出すときに簡単に使用できます。

    詳細については[エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)参照してください。

## 2023年8月1日 {#august-1-2023}

**一般的な変更**

-   TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)のデータ アプリの OpenAPI 仕様をサポートします。

    TiDB Cloudデータ サービスは、各データ アプリに対して自動生成された OpenAPI ドキュメントを提供します。ドキュメントでは、エンドポイント、パラメーター、応答を表示し、エンドポイントを試すことができます。

    また、データ アプリとそのデプロイされたエンドポイントの OpenAPI 仕様 (OAS) を YAML または JSON 形式でダウンロードすることもできます。OAS は標準化された API ドキュメント、簡素化された統合、簡単なコード生成を提供し、開発の迅速化とコラボレーションの向上を実現します。

    詳細については[OpenAPI仕様を使用する](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification)および[Next.js で OpenAPI 仕様を使用する](/tidb-cloud/data-service-oas-with-nextjs.md)を参照してください。

-   [郵便配達員](https://www.postman.com/)でデータ アプリの実行をサポートします。

    Postman 統合により、データ アプリのエンドポイントをコレクションとして、好みのワークスペースにインポートできるようになります。その後、Postman Web アプリとデスクトップ アプリの両方のサポートにより、強化されたコラボレーションとシームレスな API テストのメリットを享受できます。

    詳細については[Postmanでデータアプリを実行する](/tidb-cloud/data-service-postman-integration.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに新しい**一時停止**ステータスを導入し、この期間中は料金なしでコスト効率の高い一時停止を可能にします。

    TiDB Cloud Dedicated クラスターの**「一時停止」を**クリックすると、クラスターはまず「**一時停止中」**ステータスになります。一時停止操作が完了すると、クラスターのステータスは**「一時停止」**に変わります。

    クラスターは、ステータスが [一時**停止**] に遷移した後にのみ再開できます。これにより、 **[一時停止**] と**[再開] を**すばやくクリックすることで発生する異常な再開の問題が解決されます。

    詳細については[TiDB Cloud Dedicated クラスターを一時停止または再開する](/tidb-cloud/pause-or-resume-tidb-cluster.md)参照してください。

## 2023年7月26日 {#july-26-2023}

**一般的な変更**

-   TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)の強力な機能「自動エンドポイント生成」を紹介します。

    開発者は、最小限のクリックと構成で HTTP エンドポイントを簡単に作成できるようになりました。繰り返しの定型コードを排除し、エンドポイントの作成を簡素化および高速化し、潜在的なエラーを減らします。

    この機能の使用方法の詳細については、 [エンドポイントを自動的に生成する](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)を参照してください。

-   TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)のエンドポイントに対して`PUT`および`DELETE`リクエスト メソッドをサポートします。

    -   `UPDATE`ステートメントと同様に、 `PUT`メソッドを使用してデータを更新または変更します。
    -   `DELETE`ステートメントと同様に、 `DELETE`メソッドを使用してデータを削除します。

    詳細については[プロパティを構成する](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)参照してください。

-   TiDB Cloud `DELETE` `POST` `PUT`の**バッチ操作を**[データサービス](https://tidbcloud.com/console/data-service)します。

    エンドポイントで**バッチ操作**を有効にすると、1 回のリクエストで複数の行に対して操作を実行できるようになります。たとえば、1 回の`POST`リクエストを使用して複数行のデータを挿入できます。

    詳細については[高度なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)参照してください。

## 2023年7月25日 {#july-25-2023}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)から[バージョン7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)にアップグレードします。

**コンソールの変更**

-   サポート エントリを最適化することで、 TiDB Cloudユーザーの PingCAP サポートへのアクセスを簡素化します。改善点は次のとおりです。

    -   **サポート**用の入り口を追加する<mdsvgicon name="icon-top-organization">左下隅にあります。</mdsvgicon>
    -   [TiDB Cloudコンソール](https://tidbcloud.com/)の右下隅にある**?**アイコンのメニューを改良して、より直感的に操作できるようにします。

    詳細については[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)参照してください。

## 2023年7月18日 {#july-18-2023}

**一般的な変更**

-   組織レベルとプロジェクト レベルの両方でロールベースのアクセス制御を調整することで、ユーザーに最小限の権限を持つロールを付与し、セキュリティ、コンプライアンス、生産性を向上させることができます。

    -   組織の役割には、 `Organization Owner` 、 `Organization Billing Admin` 、 `Organization Console Audit Admin` 、 `Organization Member`が含まれます。
    -   プロジェクトロールには`Project Owner` 、 `Project Data Access Read-Write` 、 `Project Data Access Read-Only`が含まれます。
    -   プロジェクト内のクラスターを管理するには (クラスターの作成、変更、削除など)、ロール`Organization Owner`または`Project Owner`が必要です。

    さまざまなロールの権限の詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)参照してください。

-   AWS でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して、カスタマー管理暗号化キー (CMEK) 機能 (ベータ版) をサポートします。

    AWS KMS をベースに CMEK を作成し、EBS および S3 に保存されているデータをTiDB Cloudコンソールから直接暗号化できます。これにより、顧客データは顧客が管理するキーで暗号化されるため、セキュリティが強化されます。

    この機能にはまだ制限があり、リクエストがあった場合にのみ利用できることに注意してください。この機能を申請するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

-   データのインポートエクスペリエンスを向上させることを目的として、 TiDB Cloudのインポート機能を最適化しました。次の改善が行われました。

    -   TiDB Cloud Serverless の統合インポート エントリ: データのインポート エントリを統合し、ローカル ファイルのインポートと Amazon S3 からのファイルのインポートをシームレスに切り替えることができます。
    -   合理化された構成: Amazon S3 からのデータのインポートは 1 つのステップのみで済むため、時間と労力を節約できます。
    -   強化された CSV 構成: CSV 構成設定がファイル タイプ オプションの下に配置されるようになり、必要なパラメータをすばやく構成しやすくなりました。
    -   強化されたターゲット テーブルの選択: チェックボックスをクリックして、データのインポートに必要なターゲット テーブルを選択できるようになりました。この改善により、複雑な式が不要になり、ターゲット テーブルの選択が簡素化されます。
    -   表示情報の改良: インポート プロセス中に表示される不正確な情報に関連する問題を解決しました。さらに、不完全なデータの表示を防ぎ、誤解を招く情報を回避するために、プレビュー機能が削除されました。
    -   改善されたソース ファイル マッピング: ソース ファイルとターゲット テーブル間のマッピング関係の定義をサポートします。特定の命名要件を満たすようにソース ファイル名を変更するという課題に対処します。

## 2023年7月11日 {#july-11-2023}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)一般公開されました。

-   多言語サポート、24 時間 365 日のリアルタイム応答、統合ドキュメント アクセスを提供する OpenAI 搭載チャットボット、TiDB Bot (ベータ版) を紹介します。

    TiDB Bot には次のような利点があります。

    -   継続的なサポート: 常にサポートを提供し、質問に回答してサポート エクスペリエンスを向上させます。
    -   効率性の向上: 自動応答によりレイテンシーが短縮され、全体的な操作が改善されます。
    -   シームレスなドキュメント アクセス: TiDB Cloudドキュメントに直接アクセスして、情報を簡単に取得し、問題を迅速に解決できます。

    TiDB Bot を使用するには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下隅にある**[?]**をクリックし、 **[TiDB Bot に質問]**を選択してチャットを開始します。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに対して[分岐機能（ベータ版）](/tidb-cloud/branch-overview.md)サポートします。

    TiDB Cloudを使用すると、 TiDB Cloud Serverless クラスターのブランチを作成できます。クラスターのブランチは、元のクラスターから分岐したデータのコピーを含む別のインスタンスです。分離された環境が提供されるため、元のクラスターへの影響を心配することなく、自由に接続して実験することができます。

    [TiDB Cloudコンソール](/tidb-cloud/branch-manage.md)または[TiDB CloudCLI](/tidb-cloud/ticloud-branch-create.md)いずれかを使用して、2023 年 7 月 5 日以降に作成されたTiDB Cloud Serverless クラスターのブランチを作成できます。

    アプリケーション開発に GitHub を使用する場合は、 TiDB Cloud Serverless ブランチを GitHub CI/CD パイプラインに統合できます。これにより、本番データベースに影響を与えることなく、ブランチを使用してプル リクエストを自動的にテストできます。詳細については、 [TiDB Cloud Serverless Branching (ベータ版) を GitHub と統合する](/tidb-cloud/branch-github-integration.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの週次バックアップをサポートします。詳細については、 [TiDB Cloud Dedicatedデータのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)を参照してください。

## 2023年7月4日 {#july-4-2023}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに対してポイントインタイムリカバリ (PITR) (ベータ版) をサポートします。

    TiDB Cloud Serverless クラスターを過去 90 日間の任意の時点に復元できるようになりました。この機能により、 TiDB Cloud Serverless クラスターのデータ復旧機能が強化されます。たとえば、データ書き込みエラーが発生し、データを以前の状態に復元したい場合に PITR を使用できます。

    詳細については[TiDB Cloud Serverless データのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md#restore)参照してください。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのクラスター概要ページの**「今月の使用状況」**パネルを強化し、現在のリソース使用状況をより明確に表示します。

-   次の変更を加えることで、全体的なナビゲーション エクスペリエンスが向上します。

    -   統合する<mdsvgicon name="icon-top-organization">**組織**と<mdsvgicon name="icon-top-account-settings">右上隅の**アカウント**を左のナビゲーション バーに移動します。</mdsvgicon></mdsvgicon>
    -   統合する<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg>左のナビゲーションバーの**管理者**に<mdsvgicon name="icon-left-projects">左のナビゲーションバーの**プロジェクトを**クリックし、左上隅の☰ホバーメニューを削除します。これで、<mdsvgicon name="icon-left-projects">プロジェクトを切り替えたり、プロジェクト設定を変更したりします。</mdsvgicon></mdsvgicon>
    -   ドキュメント、インタラクティブ チュートリアル、自分のペースで進められるトレーニング、サポート エントリなど、TiDB Cloudのすべてのヘルプとサポート情報を、右下隅の**[?]**アイコンのメニューに統合します。

-   TiDB Cloudコンソールは、より快適で目に優しいエクスペリエンスを提供するダーク モードをサポートするようになりました。左側のナビゲーション バーの下部から、ライト モードとダーク モードを切り替えることができます。

## 2023年6月27日 {#june-27-2023}

**一般的な変更**

-   新しく作成された[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの事前構築されたサンプル データセットを削除します。

## 2023年6月20日 {#june-20-2023}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)から[バージョン6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)にアップグレードします。

## 2023年6月13日 {#june-13-2023}

**一般的な変更**

-   changefeed を使用してデータを Amazon S3 にストリーミングすることをサポートします。

    これにより、 TiDB Cloudと Amazon S3 のシームレスな統合が可能になります。1 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターから Amazon S3 へのリアルタイムのデータキャプチャとレプリケーションが可能になり、下流のアプリケーションと分析が最新のデータにアクセスできるようになります。

    詳細については[クラウドstorageに保存](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの 16 vCPU TiKV の最大ノードstorageを4 TiB から 6 TiB に増加します。

    この機能強化により、 TiDB Cloud Dedicated クラスターのデータstorage容量が増加し、ワークロードのスケーリング効率が向上し、増大するデータ要件に対応できるようになります。

    詳細については[クラスターのサイズを決める](/tidb-cloud/size-your-cluster.md)参照してください。

-   [モニタリング指標の保存期間](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) for [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターを 3 日から 7 日に延長します。

    メトリクスの保持期間を延長することで、より多くの履歴データにアクセスできるようになります。これにより、クラスターの傾向とパターンを特定し、より適切な意思決定とより迅速なトラブルシューティングが可能になります。

**コンソールの変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスターの[**キービジュアライザー**](/tidb-cloud/tune-performance.md#key-visualizer)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャにより、 **Key Visualizer**ページを簡単にナビゲートし、より直感的かつ効率的に必要な情報にアクセスできるようになります。また、新しいインフラストラクチャでは UX に関する多くの問題が解決され、SQL 診断プロセスがよりユーザーフレンドリーになります。

## 2023年6月6日 {#june-6-2023}

**一般的な変更**

-   [インデックスインサイト（ベータ版）](/tidb-cloud/index-insight.md) for [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを導入し、遅いクエリに対してインデックスの推奨を提供することでクエリ パフォーマンスを最適化します。

    Index Insight を使用すると、次の方法でアプリケーション全体のパフォーマンスとデータベース操作の効率を向上させることができます。

    -   強化されたクエリ パフォーマンス: Index Insight は、遅いクエリを識別し、適切なインデックスを提案します。これにより、クエリの実行が高速化され、応答時間が短縮され、ユーザー エクスペリエンスが向上します。
    -   コスト効率: Index Insight を使用してクエリ パフォーマンスを最適化すると、追加のコンピューティング リソースの必要性が減り、既存のインフラストラクチャをより効率的に使用できるようになります。これにより、運用コストの削減につながる可能性があります。
    -   簡素化された最適化プロセス: Index Insight は、インデックスの改善の特定と実装を簡素化し、手動分析や推測の必要性を排除します。その結果、正確なインデックスの推奨事項により、時間と労力を節約できます。
    -   アプリケーション効率の向上: Index Insight を使用してデータベース パフォーマンスを最適化することで、 TiDB Cloudで実行されるアプリケーションはより大きなワークロードを処理し、より多くのユーザーに同時にサービスを提供できるようになり、アプリケーションのスケーリング操作がより効率的になります。

    Index Insight を使用するには、 TiDB Cloud Dedicated クラスターの**診断**ページに移動し、 **Index Insight BETA**タブをクリックします。

    詳細については[Index Insight (ベータ版) を使用する](/tidb-cloud/index-insight.md)参照してください。

-   登録やインストールなしで TiDB の全機能を体験できるインタラクティブ プラットフォーム[TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes)を紹介します。

    TiDB Playground は、スケーラビリティ、MySQL 互換性、リアルタイム分析などの TiDB の機能をワンストップで探索できるエクスペリエンスを提供するように設計されたインタラクティブ プラットフォームです。

    TiDB Playground を使用すると、複雑な構成のない制御された環境で TiDB の機能をリアルタイムで試すことができるため、TiDB の機能を理解するのに最適です。

    TiDB Playground を使い始めるには、 [**TiDB プレイグラウンド**](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes)ページに移動し、探索する機能を選択して探索を開始します。

## 2023年6月5日 {#june-5-2023}

**一般的な変更**

-   [データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app) GitHub に接続することをサポートします。

    [データアプリをGitHubに接続する](/tidb-cloud/data-service-manage-github-connection.md)により、データ アプリのすべての構成を Github 上の[コードファイル](/tidb-cloud/data-service-app-config-files.md)として管理できるようになり、 TiDB Cloud Data Service がシステムアーキテクチャおよび DevOps プロセスとシームレスに統合されます。

    この機能を使用すると、次のタスクを簡単に実行できるため、データ アプリの開発における CI/CD エクスペリエンスが向上します。

    -   GitHub を使用してデータ アプリの変更を自動的にデプロイします。
    -   バージョン管理を使用して、GitHub でデータ アプリの変更の CI/CD パイプラインを構成します。
    -   接続されている GitHub リポジトリから切断します。
    -   展開前にエンドポイントの変更を確認します。
    -   デプロイメント履歴をビュー、障害が発生した場合に必要なアクションを実行します。
    -   コミットを再デプロイして、以前のデプロイにロールバックします。

    詳細については[GitHub でデータ アプリを自動的にデプロイ](/tidb-cloud/data-service-manage-github-connection.md)参照してください。

## 2023年6月2日 {#june-2-2023}

**一般的な変更**

-   簡素化と明確化を目指して、当社では製品名を更新しました。

    -   「TiDB Cloud Serverless Tier」は「TiDB Cloud Serverless」という名前になりました。
    -   「TiDB Cloud Dedicated Tier」は「TiDB Cloud Dedicated」という名前になりました。
    -   「TiDB On-Premises」は「TiDB Self-Managed」という名前になりました。

    新しくなった名前でも、同じ素晴らしいパフォーマンスをお楽しみください。お客様の体験が私たちの最優先事項です。

## 2023年5月30日 {#may-30-2023}

**一般的な変更**

-   TiDB Cloudのデータ移行機能の増分データ移行のサポートを強化します。

    binlogの位置またはグローバル トランザクション ID (GTID) を指定して、指定した位置以降に生成された増分データのみをTiDB Cloudに複製できるようになりました。この機能強化により、特定の要件に合わせて必要なデータを選択して複製する柔軟性が向上します。

    詳細は[データ移行を使用して、MySQL 互換データベースから増分データのみをTiDB Cloudに移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)を参照。

-   [**イベント**](/tidb-cloud/tidb-cloud-events.md)ページに新しいイベントタイプ ( `ImportData` ) を追加します。

-   TiDB Cloudコンソールから**Playground を**削除します。

    最適化されたエクスペリエンスを備えた新しいスタンドアロン プレイグラウンドにご期待ください。

## 2023年5月23日 {#may-23-2023}

**一般的な変更**

-   CSV ファイルを TiDB にアップロードする場合、列名の定義には英語の文字や数字だけでなく、中国語や日本語などの文字も使用できます。ただし、特殊文字についてはアンダースコア ( `_` ) のみがサポートされています。

    詳細は[ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)を参照。

## 2023年5月16日 {#may-16-2023}

**コンソールの変更**

-   専用層とサーバーレス層の両方で、機能カテゴリ別に整理された左側のナビゲーション エントリを導入します。

    新しいナビゲーションにより、機能エントリをより簡単に、より直感的に見つけられるようになりました。新しいナビゲーションを表示するには、クラスターの概要ページにアクセスしてください。

-   Dedicated Tierクラスターの**診断**ページの次の 2 つのタブに新しいネイティブ Web インフラストラクチャをリリースします。

    -   [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)
    -   [SQL文](/tidb-cloud/tune-performance.md#statement-analysis)

    新しいインフラストラクチャにより、2 つのタブを簡単にナビゲートし、より直感的かつ効率的に必要な情報にアクセスできます。また、新しいインフラストラクチャによりユーザー エクスペリエンスが向上し、SQL 診断プロセスがよりユーザー フレンドリになります。

## 2023年5月9日 {#may-9-2023}

**一般的な変更**

-   2023 年 4 月 26 日以降に作成された GCP ホスト クラスタのノード サイズの変更をサポートします。

    この機能を使用すると、需要の増加に応じてより高性能なノードにアップグレードしたり、コスト削減のためにより低性能なノードにダウングレードしたりできます。柔軟性が増すため、ワークロードに合わせてクラスターの容量を調整し、コストを最適化できます。

    詳細な手順については[ノードサイズの変更](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)参照してください。

-   圧縮ファイルのインポートをサポートします。CSV および SQL ファイルを次の形式でインポートできます: `.gzip` 、 `.zst` `.snappy`この機能により`.gz`より効率的で`.zstd`効率の高い方法でデータをインポートでき、データ転送コストが削減されます。

    詳細については[Amazon S3 または GCS から CSV ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md)および[サンプルデータのインポート](/tidb-cloud/import-sample-data.md)を参照してください。

-   TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの新しいネットワーク アクセス管理オプションとして、AWS PrivateLink を利用したエンドポイント接続をサポートします。

    プライベート エンドポイント接続では、データがパブリック インターネットに公開されることはありません。また、エンドポイント接続では CIDR の重複がサポートされており、ネットワーク管理が容易になります。

    詳細については[プライベートエンドポイント接続を設定する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのバックアップ、復元、および changefeed アクションを記録するために、 [**イベント**](/tidb-cloud/tidb-cloud-events.md)ページに新しいイベント タイプを追加します。

    記録できるイベントの完全なリストについては、 [記録されたイベント](/tidb-cloud/tidb-cloud-events.md#logged-events)を参照してください。

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの[**SQL診断**](/tidb-cloud/tune-performance.md)ページに**SQL ステートメント**タブを導入します。

    **SQL ステートメント**タブには次の内容が表示されます。

    -   TiDB データベースによって実行されるすべての SQL ステートメントの包括的な概要により、遅いクエリを簡単に識別して診断できます。
    -   クエリ時間、実行プラン、データベースサーバーの応答など、各 SQL ステートメントの詳細な情報が提供され、データベースのパフォーマンスの最適化に役立ちます。
    -   大量のデータを簡単に並べ替え、フィルタリング、検索できるユーザーフレンドリーなインターフェースにより、最も重要なクエリに集中できます。

    詳細については[ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)参照してください。

## 2023年5月6日 {#may-6-2023}

**一般的な変更**

-   TiDB [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターが配置されているリージョンの[データサービスエンドポイント](/tidb-cloud/tidb-cloud-glossary.md#endpoint)への直接アクセスをサポートします。

    新しく作成されたServerless Tierクラスターの場合、エンドポイント URL にクラスターのリージョン情報が含まれるようになりました。リージョン ドメイン`<region>.data.tidbcloud.com`を要求すると、TiDB クラスターが配置されているリージョンのエンドポイントに直接アクセスできます。

    あるいは、リージョンを指定せずにグローバル ドメイン`data.tidbcloud.com`を要求することもできます。この方法では、 TiDB Cloud は内部的に要求をターゲット リージョンにリダイレクトしますが、これにより追加のレイテンシーが発生する可能性があります。この方法を選択する場合は、エンドポイントを呼び出すときに、curl コマンドに`--location-trusted`オプションを追加するようにしてください。

    詳細については[エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)参照してください。

## 2023年4月25日 {#april-25-2023}

**一般的な変更**

-   組織内の最初の 5 つ[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターについては、 TiDB Cloud はそれぞれに次の無料使用量割り当てを提供します。

    -   行storage: 5 GiB
    -   [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 毎月5000万RU

    2023 年 5 月 31 日まで、 Serverless Tierクラスターは 100% 割引で引き続き無料です。それ以降は、無料割り当てを超えた使用量に対して料金が発生します。

    クラスターの**概要**ページの**「今月の使用量」**領域で簡単に[クラスターの使用状況を監視するか、使用クォータを増やす](/tidb-cloud/manage-serverless-spend-limit.md#manage-spending-limit-for-tidb-cloud-serverless-scalable-clusters)確認できます。クラスターの無料割り当て量に達すると、割り当て量を増やすか、新しい月の開始時に使用量がリセットされるまで、このクラスターの読み取りおよび書き込み操作は制限されます。

    さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク送信など) の RU 消費量、価格の詳細、スロットル情報の詳細については、 [TiDB CloudServerless Tierの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

-   TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのバックアップと復元をサポートします。

    詳細については[TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md)参照してください。

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)から[バージョン6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)にアップグレードします。

-   メンテナンス ウィンドウ機能を提供して、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの計画されたメンテナンス アクティビティを簡単にスケジュールおよび管理できるようにします。

    メンテナンス ウィンドウとは、 TiDB Cloudサービスの信頼性、セキュリティ、パフォーマンスを確保するために、オペレーティング システムの更新、セキュリティ パッチ、インフラストラクチャのアップグレードなどの計画されたメンテナンス アクティビティが自動的に実行される指定された期間です。

    メンテナンス期間中は、一時的な接続の中断や QPS の変動が発生する可能性がありますが、クラスターは引き続き利用可能であり、SQL 操作、既存のデータのインポート、バックアップ、復元、移行、およびレプリケーション タスクは引き続き正常に実行できます。メンテナンス中は[許可された操作と許可されていない操作のリスト](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)参照してください。

    メンテナンスの頻度を最小限に抑えるよう努めます。メンテナンス期間が計画されている場合、デフォルトの開始時間は対象週の水曜日の午前 3 時 ( TiDB Cloud組織のタイム ゾーンに基づく) です。潜在的な中断を回避するには、メンテナンス スケジュールを把握し、それに応じて操作を計画することが重要です。

    -   最新情報をお知らせするため、 TiDB Cloud はメンテナンス ウィンドウごとに 3 つの電子メール通知を送信します。1 つはメンテナンス タスクの前、1 つは開始時、もう 1 つはメンテナンス タスクの後です。
    -   メンテナンスの影響を最小限に抑えるには、 **「メンテナンス」**ページでメンテナンスの開始時刻を希望の時間に変更したり、メンテナンス アクティビティを延期したりすることができます。

    詳細については[メンテナンスウィンドウを構成する](/tidb-cloud/configure-maintenance-window.md)参照してください。

-   2023 年 4 月 25 日以降に作成され、AWS でホストされている[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスターの TiDB ノードをスケーリングするときに、TiDB の負荷分散を改善し、接続の切断を減らします。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は AWS でホストされているすべてのDedicated Tierクラスターに提供されています。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャにより、 [監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ内を簡単に移動し、より直感的かつ効率的に必要な情報にアクセスできます。また、新しいインフラストラクチャは UX に関する多くの問題を解決し、監視プロセスをよりユーザーフレンドリーにします。

## 2023年4月18日 {#april-18-2023}

**一般的な変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して[データ移行ジョブの仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)スケールアップまたはスケールダウンをサポートします。

    この機能を使用すると、仕様をスケールアップして移行パフォーマンスを向上させたり、仕様をスケールダウンしてコストを削減したりできます。

    詳細については[データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)参照してください。

**コンソールの変更**

-   UI を刷新して、 [クラスターの作成](https://tidbcloud.com/console/clusters/create-cluster)をさらにユーザーフレンドリーにし、数回クリックするだけでクラスターを作成および構成できるようになりました。

    新しいデザインは、シンプルさを重視し、視覚的な混乱を減らし、明確な指示を提供します。クラスター作成ページで**[作成] を**クリックすると、クラスターの作成が完了するのを待たずに、クラスターの概要ページに移動します。

    詳細については[クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。

-   **請求**ページに**割引**タブを導入し、組織の所有者と請求管理者向けの割引情報を表示します。

    詳細については[割引](/tidb-cloud/tidb-cloud-billing.md#discounts)参照してください。

## 2023年4月11日 {#april-11-2023}

**一般的な変更**

-   AWS でホストされている[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの TiDB ノードをスケーリングするときに、TiDB の負荷分散を改善し、接続の切断を減らします。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は AWS `Oregon (us-west-2)`リージョンでホストされているDedicated Tierクラスターにのみ提供されています。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して[ニューレリック](https://newrelic.com/)統合をサポートします。

    New Relic 統合により、TiDB クラスターのメトリック データを[ニューレリック](https://newrelic.com/)に送信するようにTiDB Cloudを設定できます。その後、 [ニューレリック](https://newrelic.com/)でアプリケーション パフォーマンスと TiDB データベース パフォーマンスの両方を監視および分析できます。この機能により、潜在的な問題を迅速に特定してトラブルシューティングし、解決時間を短縮できます。

    統合手順と利用可能なメトリックについては、 [TiDB CloudとNew Relicを統合する](/tidb-cloud/monitor-new-relic-integration.md)参照してください。

-   Dedicated Tierクラスターの Prometheus 統合に次の[チェンジフィード](/tidb-cloud/changefeed-overview.md)メトリックを追加します。

    -   `tidbcloud_changefeed_latency`
    -   `tidbcloud_changefeed_replica_rows`

    [TiDB CloudとPrometheusを統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)お持ちの場合は、これらのメトリックを使用して、変更フィードのパフォーマンスと健全性をリアルタイムで監視できます。さらに、Prometheus を使用してメトリックを監視するアラートを簡単に作成できます。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページを更新して[ノードレベルのリソースメトリック](/tidb-cloud/built-in-monitoring.md#server)を使用します。

    ノードレベルのリソース メトリックを使用すると、リソース消費量をより正確に表示して、購入したサービスの実際の使用状況をよりよく理解できます。

    これらのメトリックにアクセスするには、クラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページに移動し、 **[メトリック]**タブの**[サーバー]**カテゴリを確認します。

-   **プロジェクト別概要**と**サービス別概要**の請求項目を再編成して[請求する](/tidb-cloud/tidb-cloud-billing.md#billing-details)ページを最適化し、請求情報をより明確にします。

## 2023年4月4日 {#april-4-2023}

**一般的な変更**

-   誤検知を防ぐために、次の 2 つのアラートを[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions)から削除します。これは、ノードの 1 つで一時的にオフラインまたはメモリ不足 (OOM) の問題が発生しても、クラスターの全体的な健全性に大きな影響を与えないためです。

    -   クラスター内の少なくとも 1 つの TiDB ノードでメモリが発生しました。
    -   1 つ以上のクラスター ノードがオフラインです。

**コンソールの変更**

-   各Dedicated Tierクラスターのアクティブなアラートとクローズされたアラートの両方を一覧表示する、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[アラート](/tidb-cloud/monitor-built-in-alerting.md)ページを導入します。

    **アラート**ページには次の内容が表示されます。

    -   直感的で使いやすいユーザー インターフェース。アラート通知メールを購読していない場合でも、このページでクラスターのアラートを表示できます。
    -   高度なフィルタリング オプションを使用すると、アラートの重大度、ステータス、その他の属性に基づいてアラートをすばやく検索して並べ替えることができます。また、過去 7 日間の履歴データを表示できるため、アラート履歴の追跡が容易になります。
    -   **ルールの編集**機能。クラスターの特定のニーズに合わせてアラート ルール設定をカスタマイズできます。

    詳細については[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)参照してください。

-   TiDB Cloudのヘルプ関連の情報とアクションを 1 か所に統合​​します。

    これで、 [TiDB Cloudコンソール](https://tidbcloud.com/)の右下隅にある**[?]**をクリックして、 [TiDB Cloudヘルプ情報](/tidb-cloud/tidb-cloud-support.md)をすべて取得し、サポートに問い合わせることができます。

-   TiDB Cloudについて理解を深めるのに役立つ[はじめる](https://tidbcloud.com/console/getting-started)ページを紹介します。

    **「はじめに」**ページには、インタラクティブなチュートリアル、必須ガイド、便利なリンクが用意されています。インタラクティブなチュートリアルに従うことで、事前に構築された業界固有のデータセット (Steam ゲーム データセットと S&amp;P 500 データセット) を使用して、 TiDB Cloud の機能と HTAP 機能を簡単に探索できます。

    **「はじめに**」ページにアクセスするには、 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> [TiDB Cloudコンソール](https://tidbcloud.com/)の左側のナビゲーション バーで [はじめに]**をクリックします**。このページでは、 **[サンプル データセットのクエリ]**をクリックして対話型チュートリアルを開いたり、他のリンクをクリックしてTiDB Cloudを探索したりできます。または、右下隅の**[?]**をクリックして**[対話型チュートリアル]**をクリックすることもできます。

## 2023年3月29日 {#march-29-2023}

**一般的な変更**

-   [データ サービス (ベータ版)](/tidb-cloud/data-service-overview.md) 、データ アプリに対するよりきめ細かいアクセス制御がサポートされます。

    データアプリの詳細ページで、クラスタをデータアプリにリンクし、各 API キーのロールを指定できるようになりました。ロールは、リンクされたクラスタに対して API キーがデータを読み書きできるかどうかを制御し、 `ReadOnly`または`ReadAndWrite`に設定できます。この機能により、データアプリのクラスタレベルおよび権限レベルのアクセス制御が可能になり、ビジネスニーズに応じてアクセス範囲をより柔軟に制御できるようになります。

    詳細については[リンクされたクラスターを管理する](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)および[APIキーを管理する](/tidb-cloud/data-service-api-key.md)を参照してください。

## 2023年3月28日 {#march-28-2023}

**一般的な変更**

-   [チェンジフィード](/tidb-cloud/changefeed-overview.md)に 2 RCU、4 RCU、8 RCU の仕様を追加し、 [チェンジフィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)ときに希望の仕様を選択できるようにサポートします。

    これらの新しい仕様を使用すると、以前は 16 個の RCU が必要だったシナリオと比較して、データ複製コストを最大 87.5% 削減できます。

-   2023 年 3 月 28 日以降に作成された[チェンジフィード](/tidb-cloud/changefeed-overview.md)スケールアップまたはスケールダウン仕様をサポートします。

    より高い仕様を選択するとレプリケーションのパフォーマンスが向上し、より低い仕様を選択するとレプリケーション コストが削減されます。

    詳細については[チェンジフィードをスケールする](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)参照してください。

-   AWS の[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターから同じプロジェクトおよび同じリージョンの[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターへの増分データのリアルタイム複製をサポートします。

    詳細については[TiDB Cloudにシンク](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)参照してください。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能に対して 2 つの新しい GCP リージョン ( `Singapore (asia-southeast1)`と`Oregon (us-west1)`をサポートします。

    これらの新しいリージョンにより、データをTiDB Cloudに移行するためのオプションが増えます。アップストリーム データがこれらのリージョン内またはその付近に保存されている場合は、GCP からTiDB Cloudへのより高速で信頼性の高いデータ移行を活用できるようになります。

    詳細については[データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)のクラスターの[遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    この新しいインフラストラクチャにより、 [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ページ内を簡単に移動し、より直感的かつ効率的に必要な情報にアクセスできます。また、新しいインフラストラクチャは UX に関する多くの問題を解決し、SQL 診断プロセスをよりユーザーフレンドリーにします。

## 2023年3月21日 {#march-21-2023}

**一般的な変更**

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service) for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターを導入すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でデータにアクセスできるようになります。

    Data Service を使用すると、 TiDB Cloud をHTTPS と互換性のある任意のアプリケーションまたはサービスとシームレスに統合できます。次に、一般的なシナリオをいくつか示します。

    -   モバイル アプリケーションまたは Web アプリケーションから直接 TiDB クラスターのデータベースにアクセスします。
    -   サーバーレス エッジ関数を使用してエンドポイントを呼び出し、データベース接続プールによって発生するスケーラビリティの問題を回避します。
    -   データ サービスをデータ ソースとして使用して、 TiDB Cloudをデータ視覚化プロジェクトと統合します。
    -   MySQL インターフェースがサポートしていない環境からデータベースに接続します。

    さらに、 TiDB Cloud は、AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェースである[チャット2クエリAPI](/tidb-cloud/use-chat2query-api.md)提供します。

    データ サービスにアクセスするには、左側のナビゲーション ペインの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。詳細については、次のドキュメントを参照してください。

    -   [データサービスの概要](/tidb-cloud/data-service-overview.md)
    -   [データサービスを始める](/tidb-cloud/data-service-get-started.md)
    -   [Chat2Query APIを使い始める](/tidb-cloud/use-chat2query-api.md)

-   AWS でホストされ、2022 年 12 月 31 日以降に作成される[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでスケーリングするために、TiDB、TiKV、およびTiFlashノードのサイズを縮小することをサポートします。

    ノード サイズを[TiDB Cloudコンソール経由](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)または[TiDB Cloud API (ベータ版) 経由](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)減らすことができます。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスターの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能に対して新しい GCP リージョンをサポートします: `Tokyo (asia-northeast1)` 。

    この機能を使用すると、Google Cloud Platform (GCP) の MySQL 互換データベースから TiDB クラスタにデータを簡単かつ効率的に移行できます。

    詳細については[データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

**コンソールの変更**

-   クラスターの主な変更の記録を提供する、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの**イベント**ページを紹介します。

    このページでは、過去 7 日間のイベント履歴を表示し、トリガー時間やアクションを開始したユーザーなどの重要な詳細を追跡できます。たとえば、クラスターが一時停止された時間やクラスターのサイズを変更したユーザーなどのイベントを表示できます。

    詳細については[TiDB Cloudクラスター イベント](/tidb-cloud/tidb-cloud-events.md)参照してください。

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの**[監視]**ページに [**データベース ステータス]**タブを追加します。このタブには、次のデータベース レベルのメトリックが表示されます。

    -   DB あたりの QPS
    -   DB あたりの平均クエリ時間
    -   DB ごとの失敗したクエリ数

    これらのメトリックを使用すると、個々のデータベースのパフォーマンスを監視し、データに基づいた意思決定を行い、アプリケーションのパフォーマンスを向上させるためのアクションを実行できます。

    詳細については[Serverless Tierクラスターのメトリクスの監視](/tidb-cloud/built-in-monitoring.md)参照してください。

## 2023年3月14日 {#march-14-2023}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0)から[バージョン6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)にアップグレードします。

-   ヘッダー行を含むローカル CSV ファイルをアップロードするときに、 TiDB Cloudによって作成されるターゲット テーブルの列名の変更をサポートします。

    ヘッダー行を含むローカル CSV ファイルを[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターにインポートする場合、 TiDB Cloud でターゲット テーブルを作成する必要があり、ヘッダー行の列名がTiDB Cloud の列命名規則に従っていない場合は、対応する列名の横に警告アイコンが表示されます。警告を解決するには、アイコンの上にカーソルを移動し、メッセージに従って既存の列名を編集するか、新しい列名を入力します。

    列の命名規則については、 [ローカルファイルをインポートする](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)参照してください。

## 2023年3月7日 {#march-7-2023}

**一般的な変更**

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのデフォルトの TiDB バージョンを[バージョン6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)から[バージョン6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)にアップグレードします。

## 2023年2月28日 {#february-28-2023}

**一般的な変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに[SQL診断](/tidb-cloud/tune-performance.md)機能を追加します。

    SQL 診断を使用すると、SQL 関連の実行時ステータスに関する詳細な情報を取得できるため、SQL パフォーマンス チューニングがより効率的になります。現在、Serverless Tierの SQL 診断機能では、低速クエリ データのみが提供されます。

    SQL 診断を使用するには、 Serverless Tierクラスター ページの左側のナビゲーション バーで**[SQL 診断]**をクリックします。

**コンソールの変更**

-   左側のナビゲーションを最適化します。

    たとえば、次のようにページをより効率的にナビゲートできます。

    -   左上隅にマウスを移動すると、クラスターまたはプロジェクト間をすばやく切り替えることができます。
    -   **クラスター**ページと**管理**ページを切り替えることができます。

**APIの変更**

-   データインポート用のTiDB Cloud APIエンドポイントをいくつかリリース：

    -   すべてのインポートタスクを一覧表示する
    -   インポートタスクを取得する
    -   インポートタスクを作成する
    -   インポートタスクを更新する
    -   インポートタスク用のローカルファイルをアップロードする
    -   インポートタスクを開始する前にデータをプレビューする
    -   インポートタスクのロール情報を取得する

    詳細については、 [APIドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import)を参照してください。

## 2023年2月22日 {#february-22-2023}

**一般的な変更**

-   [コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)機能を使用して、 [TiDB Cloudコンソール](https://tidbcloud.com/)で組織内のメンバーが実行したさまざまなアクティビティを追跡することをサポートします。

    コンソール監査ログ機能は、 `Owner`または`Audit Admin`ロールを持つユーザーにのみ表示され、デフォルトでは無効になっています。有効にするには、<mdsvgicon name="icon-top-organization"> [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある**[組織**] &gt; **[コンソール監査ログ] を選択します**。</mdsvgicon>

    コンソール監査ログを分析することで、組織内で実行された疑わしい操作を特定し、組織のリソースとデータのセキュリティを向上させることができます。

    詳細については[コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)参照してください。

**CLIの変更**

-   [TiDB CloudCLI](/tidb-cloud/cli-reference.md)に新しいコマンド`ticloud cluster connect-info`を追加します。

    `ticloud cluster connect-info`は、クラスターの接続文字列を取得できるコマンドです。このコマンドを使用するには、 [`ticloud`更新](/tidb-cloud/ticloud-update.md)から v0.3.2 以降のバージョンが必要です。

## 2023年2月21日 {#february-21-2023}

**一般的な変更**

-   TiDB Cloudにデータをインポートするときに、 IAMユーザーの AWS アクセスキーを使用して Amazon S3 バケットにアクセスすることをサポートします。

    この方法は、ロール ARN を使用するよりも簡単です。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

-   [モニタリング指標の保存期間](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 2 日からより長い期間に延長します。

    -   Dedicated Tierクラスターの場合、過去 7 日間のメトリック データを表示できます。
    -   Serverless Tierクラスターの場合、過去 3 日間のメトリック データを表示できます。

    メトリクスの保持期間を延長することで、より多くの履歴データにアクセスできるようになります。これにより、クラスターの傾向とパターンを特定し、より適切な意思決定とより迅速なトラブルシューティングが可能になります。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)のクラスターの監視ページで新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャにより、監視ページを簡単にナビゲートし、より直感的かつ効率的に必要な情報にアクセスできるようになります。また、新しいインフラストラクチャでは UX に関する多くの問題が解決され、監視プロセスがはるかにユーザーフレンドリーになります。

## 2023年2月17日 {#february-17-2023}

**CLIの変更**

-   [TiDB CloudCLI](/tidb-cloud/cli-reference.md)に新しいコマンド[`ticloud connect`](/tidb-cloud/ticloud-serverless-shell.md)を追加します。

    `ticloud connect` 、SQL クライアントをインストールせずにローカル マシンからTiDB Cloudクラスターに接続できるコマンドです。TiDB TiDB Cloudクラスターに接続した後、 TiDB Cloud CLI で SQL ステートメントを実行できます。

## 2023年2月14日 {#february-14-2023}

**一般的な変更**

-   TiDB [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでスケールするために TiKV ノードとTiFlashノードの数を減らすことをサポートします。

    ノード番号を[TiDB Cloudコンソール経由](/tidb-cloud/scale-tidb-cluster.md#change-node-number)または[TiDB Cloud API (ベータ版) 経由](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)減らすことができます。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの**監視**ページを紹介します。

    **モニタリング**ページには、1 秒あたりに実行される SQL ステートメントの数、クエリの平均実行時間、失敗したクエリの数など、さまざまなメトリックとデータが提供され、 Serverless Tierクラスター内の SQL ステートメントの全体的なパフォーマンスをよりよく理解するのに役立ちます。

    詳細については[TiDB Cloud組み込み監視](/tidb-cloud/built-in-monitoring.md)参照してください。

## 2023年2月2日 {#february-2-2023}

**CLIの変更**

-   TiDB Cloud CLI クライアント[`ticloud`](/tidb-cloud/cli-reference.md)を紹介します。

    `ticloud`使用すると、数行のコマンドでターミナルやその他の自動ワークフローからTiDB Cloudリソースを簡単に管理できます。特に GitHub Actions については、 `ticloud`簡単にセットアップできるように[`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli)提供しています。

    詳細については[TiDB CloudCLI クイック スタート](/tidb-cloud/get-started-with-cli.md)および[TiDB CloudCLI リファレンス](/tidb-cloud/cli-reference.md)を参照してください。

## 2023年1月18日 {#january-18-2023}

**一般的な変更**

-   Microsoft アカウントで[サインアップ](https://tidbcloud.com/free-trial) TiDB Cloudをサポートします。

## 2023年1月17日 {#january-17-2023}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3)から[バージョン6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0)にアップグレードします。

-   新規サインアップ ユーザーの場合、 TiDB Cloud は自動的に[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターを無料で作成し、 TiDB Cloudを使用したデータ探索をすぐに開始できるようにします。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい AWS リージョンをサポートします: `Seoul (ap-northeast-2)` 。

    この地域では次の機能が有効になっています:

    -   [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    -   [変更フィードを使用してTiDB Cloudから他のデータ サービスにデータをストリーミングする](/tidb-cloud/changefeed-overview.md)
    -   [TiDB クラスター データのバックアップと復元](/tidb-cloud/backup-and-restore.md)

## 2023年1月10日 {#january-10-2023}

**一般的な変更**

-   ローカル CSV ファイルから TiDB にデータをインポートする機能を最適化し、 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのユーザー エクスペリエンスを向上させます。

    -   CSV ファイルをアップロードするには、**インポート**ページのアップロード領域にドラッグ アンド ドロップするだけです。
    -   インポート タスクを作成するときに、ターゲット データベースまたはテーブルが存在しない場合は、名前を入力してTiDB Cloudに自動的に作成させることができます。作成するターゲット テーブルに対して、主キーを指定するか、複数のフィールドを選択して複合主キーを形成できます。
    -   インポートが完了したら、 **「Chat2Query でデータを探索」を**クリックするか、タスク リストでターゲット テーブル名をクリックして、 [AI搭載Chat2Query](/tidb-cloud/explore-data-with-chat2query.md)でデータを探索できます。

    詳細については[ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)参照してください。

**コンソールの変更**

-   特定のクラスターに対するサポートをリクエストするプロセスを簡素化するために、各クラスターに「**サポートの取得」**オプションを追加します。

    クラスターのサポートは、次のいずれかの方法でリクエストできます。

    -   プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページで、クラスターの行にある**[...]**をクリックし、 **[サポートを受ける]**を選択します。
    -   クラスターの概要ページで、右上隅の**[...]**をクリックし、 **[サポートを受ける]**を選択します。

## 2023年1月5日 {#january-5-2023}

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの SQL エディター (ベータ版) の名前を Chat2Query (ベータ版) に変更し、AI を使用した SQL クエリの生成をサポートします。

    Chat2Query では、AI に SQL クエリを自動的に生成させたり、SQL クエリを手動で記述したり、ターミナルなしでデータベースに対して SQL クエリを実行したりできます。

    Chat2Query にアクセスするには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、クラスター名をクリックして、左側のナビゲーション ペインで**Chat2Query を**クリックします。

## 2023年1月4日 {#january-4-2023}

**一般的な変更**

-   AWS でホストされ、2022 年 12 月 31 日以降に作成されたTiDB Cloud Dedicated クラスターの**ノード サイズ (vCPU + RAM)**を増やすことで、TiDB、TiKV、およびTiFlashノードのスケールアップをサポートします。

    ノード サイズを[TiDB Cloudコンソールを使用する](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)または[TiDB Cloud API (ベータ版) の使用](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)増やすことができます。

-   [**監視**](/tidb-cloud/built-in-monitoring.md)ページのメトリックの保持期間を 2 日間に延長します。

    これで、過去 2 日間のメトリック データにアクセスできるようになり、クラスターのパフォーマンスと傾向をより柔軟かつ詳細に把握できるようになります。

    この改善は追加費用なしで提供され、クラスターの[**監視**](/tidb-cloud/built-in-monitoring.md)ページの**[診断]**タブからアクセスできます。これにより、パフォーマンスの問題を特定してトラブルシューティングし、クラスターの全体的な状態をより効果的に監視できるようになります。

-   Prometheus 統合用の Grafana ダッシュボード JSON のカスタマイズをサポートします。

    [TiDB CloudとPrometheusを統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)お持ちの場合は、事前に構築された Grafana ダッシュボードをインポートしてTiDB Cloudクラスターを監視し、ダッシュボードをニーズに合わせてカスタマイズできるようになりました。この機能により、 TiDB Cloudクラスターを簡単かつ迅速に監視できるようになり、パフォーマンスの問題を迅速に特定できるようになります。

    詳細については[Grafana GUIダッシュボードを使用してメトリックを視覚化する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)参照してください。

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのデフォルトの TiDB バージョンを[バージョン6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[バージョン6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。Serverless Serverless Tierクラスターのデフォルトの TiDB バージョンを v6.4.0 にアップグレードした後のコールド スタートの問題が解決されました。

**コンソールの変更**

-   [**クラスター**](https://tidbcloud.com/console/clusters)ページ目とクラスター概要ページの表示を簡素化します。

    -   [**クラスター**](https://tidbcloud.com/console/clusters)ページのクラスター名をクリックすると、クラスターの概要ページに入り、クラスターの操作を開始できます。
    -   クラスターの概要ページから**[接続] ペイン**と**[インポート]**ペインを削除します。右上隅の**[接続]**をクリックして接続情報を取得し、左側のナビゲーション ペインの**[インポート]**をクリックしてデータをインポートできます。
