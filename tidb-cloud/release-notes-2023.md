---
title: TiDB Cloud Release Notes in 2023
summary: 2023 年のTiDB Cloudのリリース ノートについて説明します。
---

# 2023年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2023}

このページには、2023 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2023年12月5日 {#december-5-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)使用すると、失敗した変更フィードを再開できるため、新しい変更フィードを再作成する手間が省けます。

    詳細については[チェンジフィードの状態](/tidb-cloud/changefeed-overview.md#changefeed-states)参照してください。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)の接続エクスペリエンスを強化します。

    **接続**ダイアログのインターフェースを改良し、 TiDB Cloud Serverless ユーザーにとってよりスムーズで効率的な接続エクスペリエンスを提供します。さらに、 TiDB Cloud Serverless ではより多くのクライアントタイプが導入され、接続するブランチを選択できるようになりました。

    詳細については[TiDB Cloud Serverless に接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)参照してください。

## 2023年11月28日 {#november-28-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)バックアップからの SQL バインディングの復元をサポートします。

    TiDB Cloud Dedicated は、バックアップからの復元時に、ユーザーアカウントと SQL バインディングをデフォルトで復元するようになりました。この機能強化はバージョン 6.2.0 以降のクラスターで利用可能で、データ復元プロセスを効率化します。SQL バインディングの復元により、クエリ関連の設定と最適化がスムーズに再統合され、より包括的で効率的なリカバリエクスペリエンスが実現します。

    詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) SQL ステートメントの RU コストの監視をサポートします。

    TiDB Cloud Serverless は、各 SQL ステートメントの詳細な分析情報を提供するようになりました[リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit)ステートメントごとの**合計 RU**コストと**平均 RU**コストの両方を表示できます。この機能は RU コストの特定と分析に役立ち、運用における潜在的なコスト削減の機会を提供します。

    SQL ステートメントの RU の詳細を確認するには、 [TiDB Cloudサーバーレスクラスター](https://tidbcloud.com/project/clusters)の**診断**ページに移動し、 **SQL ステートメント**タブをクリックします。

## 2023年11月21日 {#november-21-2023}

**一般的な変更**

-   [データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 、Google Cloud にデプロイされた TiDB クラスタの高速物理モードをサポートします。

    AWSおよびGoogle CloudにデプロイされたTiDBクラスタで物理モードがご利用いただけるようになりました。物理モードの移行速度は最大110MiB/sに達し、論理モードの2.4倍の速度です。このパフォーマンス向上は、大規模なデータセットをTiDB Cloudに迅速に移行するのに最適となります。

    詳細については[既存データと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)参照してください。

## 2023年11月14日 {#november-14-2023}

**一般的な変更**

-   TiDB Cloud Dedicated クラスターからデータを復元する場合のデフォルトの動作が、ユーザー アカウントなしでの復元からすべてのユーザー アカウントを使用しての復元に変更されました。

    詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

-   変更フィード用のイベント フィルターを導入します。

    この機能強化により、 [TiDB Cloudコンソール](https://tidbcloud.com/)を通じて直接変更フィードのイベント フィルターを簡単に管理できるようになり、変更フィードから特定のイベントを除外するプロセスが効率化され、下流のデータ レプリケーションをより適切に制御できるようになります。

    詳細については[チェンジフィード](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)参照してください。

## 2023年11月7日 {#november-7-2023}

**一般的な変更**

-   以下のリソース使用状況アラートを追加します。新しいアラートはデフォルトで無効になっています。必要に応じて有効にできます。

    -   TiDB ノード全体の最大メモリ使用率が 10 分間 70% を超えました
    -   TiKVノード全体の最大メモリ使用率が10分間70%を超えました
    -   TiDBノード全体の最大CPU使用率が10分間80%を超えました
    -   TiKVノード全体の最大CPU使用率が10分間80%を超えました

    詳細については[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md#resource-usage-alerts)参照してください。

## 2023年10月31日 {#october-31-2023}

**一般的な変更**

-   営業担当者に連絡せずに、 TiDB Cloudコンソールでエンタープライズ サポート プランに直接アップグレードできます。

    詳細については[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)参照してください。

## 2023年10月25日 {#october-25-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 、Google Cloud でのデュアルリージョン バックアップ (ベータ版) をサポートします。

    Google Cloud でホストされるTiDB Cloud Dedicated クラスタは、Google Cloud Storage とシームレスに連携します。Google Cloud Storage の[デュアルリージョン](https://cloud.google.com/storage/docs/locations#location-dr)機能と同様に、 TiDB Cloud Dedicated のデュアルリージョンで使用するリージョンのペアは、同じマルチリージョン内になければなりません。例えば、東京と大阪は同じマルチリージョン`ASIA`内にあるため、デュアルリージョンstorageとして一緒に使用できます。

    詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)参照してください。

-   [データ変更ログをApache Kafkaにストリーミングする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)の機能は現在、一般提供 (GA) になっています。

    10ヶ月間のベータトライアルを経て、 TiDB CloudからApache Kafkaへのデータ変更ログのストリーミング機能が一般提供となりました。TiDBからメッセージキューへのデータストリーミングは、データ統合シナリオにおいて一般的なニーズです。Kafkaシンクを使用することで、他のデータ処理システム（Snowflakeなど）との統合や、ビジネス利用のサポートが可能になります。

    詳細については[チェンジフィードの概要](/tidb-cloud/changefeed-overview.md)参照してください。

## 2023年10月11日 {#october-11-2023}

**一般的な変更**

-   AWS にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのうち[デュアルリージョンバックアップ（ベータ版）](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)サポートします。

    クラウドプロバイダー内の地理的リージョン間でバックアップを複製できるようになりました。この機能により、データ保護と災害復旧機能がさらにレイヤーされます。

    詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

-   データ移行では、既存のデータの移行に物理モードと論理モードの両方がサポートされるようになりました。

    物理モードでは、移行速度は最大110 MiB/秒に達します。論理モードの45 MiB/秒と比較すると、移行パフォーマンスが大幅に向上しています。

    詳細については[既存データと増分データを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)参照してください。

## 2023年10月10日 {#october-10-2023}

**一般的な変更**

-   TiDB Cloud Vercel 統合により、 [Vercel プレビュー デプロイメント](https://vercel.com/docs/deployments/preview-deployments)でのTiDB Cloud Serverless ブランチの使用をサポートします。

    詳細については[TiDB Cloud Serverless ブランチに接続](/tidb-cloud/integrate-tidbcloud-with-vercel.md#connect-with-tidb-cloud-serverless-branching)参照してください。

## 2023年9月28日 {#september-28-2023}

**APIの変更**

-   特定の組織の特定の月の請求書を取得するためのTiDB Cloud Billing API エンドポイントを導入します。

    このBilling APIエンドポイントは、 TiDB Cloudの最新APIバージョンであるTiDB Cloud API v1beta1でリリースされています。詳細については、 [APIドキュメント（v1beta1）](https://docs.pingcap.com/tidbcloud/api/v1beta1#tag/Billing)をご覧ください。

## 2023年9月19日 {#september-19-2023}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターから 2 つの vCPU TiDB ノードと TiKV ノードを削除します。

    2 vCPU オプションは**、 [クラスタの作成]**ページまたは**[クラスタの変更]**ページで使用できなくなりました。

-   JavaScript のリリース[TiDB Cloudサーバーレス ドライバー (ベータ版)](/tidb-cloud/serverless-driver.md) 。

    TiDB CloudのJavaScript用サーバーレスドライバーを使用すると、HTTPS経由で[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに接続できます。特に、TCP接続数が[Vercelエッジ関数](https://vercel.com/docs/functions/edge-functions)や[Cloudflareワーカー](https://workers.cloudflare.com/)など制限されているエッジ環境で役立ちます。

    詳細については[TiDB Cloudサーバーレス ドライバー (ベータ版)](/tidb-cloud/serverless-driver.md)参照してください。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの場合、 **「今月の使用量**」パネルまたは支出限度額の設定時にコストの見積もりを取得できます。

## 2023年9月5日 {#september-5-2023}

**一般的な変更**

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service) 、さまざまな状況での特定のレート制限要件を満たすために、各 API キーのレート制限をカスタマイズすることがサポートされています。

    キーを[作成する](/tidb-cloud/data-service-api-key.md#create-an-api-key)または[編集](/tidb-cloud/data-service-api-key.md#edit-an-api-key)すると、API キーのレート制限を調整できます。

    詳細については[レート制限](/tidb-cloud/data-service-api-key.md#rate-limiting)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい AWS リージョンをサポートします: サンパウロ (sa-east-1)。

-   各[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの IP アクセス リストに最大 100 個の IP アドレスを追加することをサポートします。

    詳細については[IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md)参照してください。

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

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに対して Google Cloud [プライベートサービスコネクト](https://cloud.google.com/vpc/docs/private-service-connect)サポートします。

    プライベート エンドポイントを作成し、Google Cloud でホストされているTiDB Cloud Dedicated クラスタへの安全な接続を確立できるようになりました。

    主な利点:

    -   直感的な操作: わずか数ステップでプライベート エンドポイントを作成できます。
    -   強化されたセキュリティ: データを保護するために安全な接続を確立します。
    -   パフォーマンスの向上: 低遅延かつ高帯域幅の接続を実現します。

    詳細については[プライベートエンドポイント経由で Google Cloud に接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターから[Google クラウド ストレージ (GCS)](https://cloud.google.com/storage)にデータをストリーミングするための変更フィードの使用をサポートします。

    ご自身のアカウントのバケットを使用し、適切にカスタマイズされた権限を付与することで、 TiDB Cloudから GCS にデータをストリーミングできるようになりました。GCS にデータを複製した後、データの変更を自由に分析できます。

    詳細については[クラウドストレージに保存](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

## 2023年8月15日 {#august-15-2023}

**一般的な変更**

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service)開発エクスペリエンスを向上させるために`GET`リクエストのページ分割をサポートします。

    `GET`リクエストの場合、**アドバンスプロパティ**で**ページネーションを**有効にし、エンドポイントを呼び出す際にクエリパラメータとして`page`と`page_size`指定することで、結果をページ分けできます。例えば、1 ページあたり 10 項目の 2 ページ目を取得するには、次のコマンドを使用します。

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>?page=2&page_size=10'
    ```

    この機能は、最後のクエリが`SELECT`ステートメントである`GET`リクエストに対してのみ使用できることに注意してください。

    詳細については[エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)参照してください。

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service) 、指定された有効期間 (TTL) にわたって`GET`要求のエンドポイント応答のキャッシュをサポートします。

    この機能により、データベースの負荷が軽減され、エンドポイントのレイテンシーが最適化されます。

    `GET`リクエスト メソッドを使用するエンドポイントの場合、**キャッシュ レスポンス**を有効にし、 **Advance Properties**でキャッシュの TTL 期間を設定できます。

    詳細については[高度なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)参照してください。

-   AWS でホストされ、2023 年 8 月 15 日以降に作成された[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの負荷分散の改善を無効にします。これには以下が含まれます。

    -   AWS でホストされている TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することを無効にします。
    -   AWS でホストされている TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することを無効にします。

    この変更により、ハイブリッド展開におけるリソース競合が回避され、この改善が有効になっている既存のクラスターには影響しません。新しいクラスターで負荷分散の改善を有効にする場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## 2023年8月8日 {#august-8-2023}

**一般的な変更**

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service)では基本認証がサポートされるようになりました。

    [「基本」HTTP認証](https://datatracker.ietf.org/doc/html/rfc7617)使用して、リクエストで公開鍵をユーザー名として、秘密鍵をパスワードとして提供できます。ダイジェスト認証と比較して、基本認証はよりシンプルで、データ サービス エンドポイントを呼び出すときに簡単に使用できます。

    詳細については[エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)参照してください。

## 2023年8月1日 {#august-1-2023}

**一般的な変更**

-   TiDB Cloud [データサービス](https://tidbcloud.com/project/data-service)でデータ アプリの OpenAPI 仕様をサポートします。

    TiDB Cloud Data Service は、各データアプリ向けに自動生成された OpenAPI ドキュメントを提供します。ドキュメントでは、エンドポイント、パラメータ、レスポンスを確認し、エンドポイントを試すことができます。

    データアプリとそのデプロイされたエンドポイントのOpenAPI仕様（OAS）をYAMLまたはJSON形式でダウンロードすることもできます。OASは標準化されたAPIドキュメント、簡素化された統合、そして容易なコード生成を提供し、開発の迅速化とコラボレーションの向上を実現します。

    詳細については、 [OpenAPI仕様を使用する](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification)および[Next.js で OpenAPI 仕様を使用する](/tidb-cloud/data-service-oas-with-nextjs.md)参照してください。

-   [郵便配達員](https://www.postman.com/)でデータ アプリの実行をサポートします。

    Postman統合により、データアプリのエンドポイントをコレクションとして、お好みのワークスペースにインポートできます。PostmanのWebアプリとデスクトップアプリの両方をサポートすることで、強化されたコラボレーションとシームレスなAPIテストのメリットを享受できます。

    詳細については[Postmanでデータアプリを実行する](/tidb-cloud/data-service-postman-integration.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに新しい**一時停止**ステータスを導入し、この期間中は料金なしでコスト効率の高い一時停止を可能にします。

    TiDB Cloud Dedicated クラスターで**「一時停止」**をクリックすると、クラスターはまず「**一時停止中」**状態になります。一時停止操作が完了すると、クラスターのステータスは**「一時停止」**に変わります。

    クラスターは、ステータスが**[一時停止]**に遷移した後にのみ再開できます。これにより、 **[一時停止]**と**[再開] を**素早くクリックすることで発生する異常な再開の問題が解決されます。

    詳細については[TiDB Cloud Dedicated クラスターを一時停止または再開する](/tidb-cloud/pause-or-resume-tidb-cluster.md)参照してください。

## 2023年7月26日 {#july-26-2023}

**一般的な変更**

-   TiDB Cloud [データサービス](https://tidbcloud.com/project/data-service)の強力な機能、自動エンドポイント生成を紹介します。

    開発者は、最小限のクリックと設定でHTTPエンドポイントを簡単に作成できるようになりました。繰り返しの定型コードを排除し、エンドポイントの作成を簡素化・高速化し、潜在的なエラーを削減します。

    この機能の使用方法の詳細については、 [エンドポイントを自動的に生成する](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)参照してください。

-   TiDB Cloud [データサービス](https://tidbcloud.com/project/data-service)のエンドポイントの`PUT`および`DELETE`リクエスト メソッドをサポートします。

    -   `UPDATE`ステートメントと同様に、 `PUT`メソッドを使用してデータを更新または変更します。
    -   `DELETE`ステートメントと同様に、 `DELETE`メソッドを使用してデータを削除します。

    詳細については[プロパティを構成する](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)参照してください。

-   TiDB Cloud [データサービス](https://tidbcloud.com/project/data-service)で`POST` `PUT` `DELETE`メソッドの**バッチ操作**をサポートします。

    エンドポイントで**バッチ操作**を有効にすると、単一のリクエストで複数の行に対する操作を実行できるようになります。例えば、単一のリクエスト`POST`で複数行のデータを挿入できます。

    詳細については[高度なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)参照してください。

## 2023年7月25日 {#july-25-2023}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)から[バージョン7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)にアップグレードします。

**コンソールの変更**

-   サポートエントリを最適化することで、 TiDB CloudユーザーのPingCAPサポートへのアクセスを簡素化します。改善点は以下のとおりです。

    -   **サポート**用の入り口を追加<mdsvgicon name="icon-top-organization">左下隅にあります。</mdsvgicon>
    -   [TiDB Cloudコンソール](https://tidbcloud.com/)の右下隅にある**?**アイコンのメニューを改良して、より直感的に操作できるようにします。

    詳細については[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)参照してください。

## 2023年7月18日 {#july-18-2023}

**一般的な変更**

-   組織レベルとプロジェクトレベルの両方でロールベースのアクセス制御を調整することで、ユーザーに最小限の権限を持つロールを付与し、セキュリティ、コンプライアンス、生産性を向上させることができます。

    -   組織の役割には、 `Organization Owner` 、 `Organization Billing Admin` 、 `Organization Console Audit Admin` 、 `Organization Member`含まれます。
    -   プロジェクト ロールには`Project Owner` 、 `Project Data Access Read-Write` 、 `Project Data Access Read-Only`含まれます。
    -   プロジェクト内のクラスターを管理するには (クラスターの作成、変更、削除など)、ロール`Organization Owner`または`Project Owner`である必要があります。

    さまざまなロールの権限の詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)参照してください。

-   AWS でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して、カスタマー管理暗号化キー (CMEK) 機能 (ベータ版) をサポートします。

    AWS KMS ベースの CMEK を作成し、 TiDB Cloudコンソールから直接 EBS および S3 に保存されているデータを暗号化できます。これにより、顧客データは顧客が管理するキーで暗号化されるため、セキュリティが強化されます。

    この機能にはまだ制限があり、リクエストに応じてのみご利用いただけます。この機能を申請するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)ご連絡ください。

-   TiDB Cloudのインポート機能を最適化し、データのインポートエクスペリエンスを向上させました。以下の改善が行われました。

    -   TiDB Cloud Serverless の統合インポート エントリ: データのインポートのエントリを統合し、ローカル ファイルのインポートと Amazon S3 からのファイルのインポートをシームレスに切り替えることができます。
    -   合理化された構成: Amazon S3 からのデータのインポートは 1 つのステップだけで済むため、時間と労力を節約できます。
    -   強化された CSV 構成: CSV 構成設定がファイル タイプ オプションの下に配置されるようになり、必要なパラメータを簡単にすばやく構成できるようになりました。
    -   ターゲットテーブルの選択機能強化：チェックボックスをクリックすることで、データインポートの対象となるターゲットテーブルを選択できるようになりました。この改善により、複雑な式を入力する必要がなくなり、ターゲットテーブルの選択が簡素化されます。
    -   表示情報の改良：インポート処理中に表示される不正確な情報に関する問題を解決しました。また、不完全なデータ表示や誤解を招く情報の表示を防ぐため、プレビュー機能を削除しました。
    -   ソースファイルマッピングの改善：ソースファイルとターゲットテーブル間のマッピング関係の定義をサポートします。これにより、特定の命名要件を満たすためにソースファイル名を変更するという課題に対処できます。

## 2023年7月11日 {#july-11-2023}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)が一般公開されました。

-   多言語サポート、24 時間 365 日のリアルタイム応答、統合ドキュメント アクセスを提供する OpenAI 搭載チャットボット、TiDB Bot (ベータ版) をご紹介します。

    TiDB Bot には次のような利点があります。

    -   継続的なサポート: いつでもサポートを提供して質問に回答し、サポート エクスペリエンスを向上させます。
    -   効率性の向上: 自動応答によりレイテンシーが短縮され、全体的な操作が改善されます。
    -   シームレスなドキュメント アクセス: TiDB Cloudドキュメントに直接アクセスして、情報を簡単に取得し、問題を迅速に解決できます。

    TiDB Bot を使用するには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下隅にある**[?]**をクリックし、 **[TiDB Bot に質問]**を選択してチャットを開始します。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに対して[分岐機能（ベータ版）](/tidb-cloud/branch-overview.md)サポートします。

    TiDB Cloud、 TiDB Cloud Serverless クラスターのブランチを作成できます。クラスターのブランチとは、元のクラスターから分岐したデータのコピーを含む独立したインスタンスです。これにより分離された環境が提供され、元のクラスターへの影響を心配することなく、自由に接続して実験を行うことができます。

    [TiDB Cloudコンソール](/tidb-cloud/branch-manage.md)または[TiDB CloudCLI](/tidb-cloud/ticloud-branch-create.md)いずれかを使用して、2023 年 7 月 5 日以降に作成されたTiDB Cloud Serverless クラスターのブランチを作成できます。

    アプリケーション開発にGitHubをご利用の場合、 TiDB Cloud Serverlessブランチ機能をGitHub CI/CDパイプラインに統合することで、本番のデータベースに影響を与えることなく、ブランチを使用してプルリクエストを自動的にテストできます。詳細については、 [TiDB Cloud Serverless Branching（ベータ版）をGitHubと統合する](/tidb-cloud/branch-github-integration.md)ご覧ください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタの週次バックアップをサポートします。詳細については、 [TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)参照してください。

## 2023年7月4日 {#july-4-2023}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに対してポイントインタイムリカバリ (PITR) (ベータ版) をサポートします。

    TiDB Cloud Serverless クラスターを過去90日間の任意の時点に復元できるようになりました。この機能により、 TiDB Cloud Serverless クラスターのデータ復旧能力が強化されます。例えば、データ書き込みエラーが発生し、データを以前の状態に復元したい場合、PITR を使用できます。

    詳細については[TiDB Cloud Serverless データのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md#restore)参照してください。

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのクラスター概要ページの**「今月の使用状況」**パネルを拡張し、現在のリソース使用状況をより明確に表示します。

-   次の変更を加えることで、全体的なナビゲーション エクスペリエンスが向上します。

    -   統合する<mdsvgicon name="icon-top-organization">**組織**と<mdsvgicon name="icon-top-account-settings">右上隅の**アカウントを**左のナビゲーション バーに移動します。</mdsvgicon></mdsvgicon>
    -   統合する<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg>左のナビゲーションバーの**管理者**に<mdsvgicon name="icon-left-projects">左ナビゲーションバーの**「プロジェクト」を**クリックし、左上隅の☰ホバーメニューを削除します。これで、<mdsvgicon name="icon-left-projects">プロジェクト間を切り替えたり、プロジェクト設定を変更したりします。</mdsvgicon></mdsvgicon>
    -   ドキュメント、対話型チュートリアル、自習型トレーニング、サポート エントリなど、 TiDB Cloudのすべてのヘルプとサポート情報を、右下隅の**[?]**アイコンのメニューに統合します。

-   TiDB Cloudコンソールは、より快適で目に優しいダークモードをサポートするようになりました。左ナビゲーションバーの下部から、ライトモードとダークモードを切り替えることができます。

## 2023年6月27日 {#june-27-2023}

**一般的な変更**

-   新しく作成された[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの事前構築されたサンプル データセットを削除します。

## 2023年6月20日 {#june-20-2023}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)から[バージョン6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)にアップグレードします。

## 2023年6月13日 {#june-13-2023}

**一般的な変更**

-   changefeed を使用してデータを Amazon S3 にストリーミングすることをサポートします。

    これにより、 TiDB CloudとAmazon S3のシームレスな統合が可能になります。1 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタからAmazon S3へのリアルタイムのデータキャプチャとレプリケーションが可能になり、下流のアプリケーションと分析機能が最新のデータにアクセスできるようになります。

    詳細については[クラウドストレージにstorage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの 16 vCPU TiKV の最大ノードstorageを4 TiB から 6 TiB に増加します。

    この機能強化により、 TiDB Cloud Dedicated クラスターのデータstorage容量が増加し、ワークロードのスケーリング効率が向上し、増大するデータ要件に対応できるようになります。

    詳細については[クラスターのサイズ](/tidb-cloud/size-your-cluster.md)参照してください。

-   [監視メトリクスの保持期間](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) for [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターを 3 日から 7 日に延長します。

    メトリクスの保持期間を延長することで、より多くの履歴データにアクセスできるようになります。これにより、クラスターの傾向やパターンを特定し、より適切な意思決定と迅速なトラブルシューティングが可能になります。

**コンソールの変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[**キービジュアライザー**](/tidb-cloud/tune-performance.md#key-visualizer)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャにより、 **Key Visualizer**ページ内を簡単にナビゲートし、より直感的かつ効率的に必要な情報にアクセスできるようになりました。また、新しいインフラストラクチャはUXに関する多くの問題を解決し、SQL診断プロセスをよりユーザーフレンドリーなものにしています。

## 2023年6月6日 {#june-6-2023}

**一般的な変更**

-   [インデックスインサイト（ベータ版）](/tidb-cloud/index-insight.md) for [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを導入します。これは、遅いクエリに対してインデックスの推奨を提供することで、クエリ パフォーマンスを最適化します。

    Index Insight を使用すると、次の方法でアプリケーション全体のパフォーマンスとデータベース操作の効率を向上させることができます。

    -   強化されたクエリ パフォーマンス: Index Insight は、遅いクエリを識別し、適切なインデックスを提案します。これにより、クエリの実行が高速化され、応答時間が短縮され、ユーザー エクスペリエンスが向上します。
    -   コスト効率：Index Insight を使用してクエリパフォーマンスを最適化することで、追加のコンピューティングリソースの必要性が軽減され、既存のインフラストラクチャをより効率的に活用できるようになります。これにより、運用コストの削減につながる可能性があります。
    -   簡素化された最適化プロセス：Index Insightは、インデックスの改善点の特定と実装を簡素化し、手作業による分析や推測作業の必要性を排除します。その結果、正確なインデックス推奨によって時間と労力を節約できます。
    -   アプリケーション効率の向上: Index Insight を使用してデータベース パフォーマンスを最適化することで、 TiDB Cloudで実行されるアプリケーションはより大きなワークロードを処理し、より多くのユーザーに同時にサービスを提供できるようになり、アプリケーションのスケーリング操作がより効率的になります。

    Index Insight を使用するには、 TiDB Cloud Dedicated クラスターの**診断**ページに移動し、 **Index Insight BETA**タブをクリックします。

    詳細については[Index Insight（ベータ版）を使用する](/tidb-cloud/index-insight.md)参照してください。

-   登録やインストールなしで TiDB の全機能を体験できるインタラクティブ プラットフォーム[TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes)をご紹介します。

    TiDB Playground は、スケーラビリティ、MySQL 互換性、リアルタイム分析などの TiDB の機能をワンストップで探索できるエクスペリエンスを提供するように設計されたインタラクティブ プラットフォームです。

    TiDB Playground を使用すると、複雑な構成のない制御された環境で TiDB の機能をリアルタイムで試すことができるため、TiDB の機能を理解するのに最適です。

    TiDB Playground を使い始めるには、 [**TiDB プレイグラウンド**](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes)ページに移動し、探索する機能を選択して探索を開始します。

## 2023年6月5日 {#june-5-2023}

**一般的な変更**

-   [データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app) GitHub に接続することをサポートします。

    [データアプリをGitHubに接続する](/tidb-cloud/data-service-manage-github-connection.md)により、データ アプリのすべての構成を Github 上の[コードファイル](/tidb-cloud/data-service-app-config-files.md)として管理できるようになり、 TiDB Cloudデータ サービスをシステムアーキテクチャおよび DevOps プロセスとシームレスに統合できます。

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

-   簡素化と明確化を目指し、製品名を更新しました。

    -   「TiDB Cloud Serverless Tier」は「TiDB Cloud Serverless」という名前になりました。
    -   「TiDB Cloud Dedicated Tier」は「TiDB Cloud Dedicated」という名前になりました。
    -   「TiDB On-Premises」は「TiDB Self-Managed」という名前になりました。

    刷新された名前でも、変わらぬ素晴らしいパフォーマンスをお楽しみください。お客様の体験こそが私たちの最優先事項です。

## 2023年5月30日 {#may-30-2023}

**一般的な変更**

-   TiDB Cloudのデータ移行機能の増分データ移行のサポートを強化します。

    binlogの位置またはグローバルトランザクション識別子（GTID）を指定して、指定した位置以降に生成された増分データのみをTiDB Cloudに複製できるようになりました。この機能強化により、お客様の特定の要件に合わせて必要なデータを選択し、複製する柔軟性が向上します。

    詳細は[データ移行を使用して、MySQL 互換データベースからTiDB Cloudに増分データのみを移行する](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)を参照。

-   [**イベント**](/tidb-cloud/tidb-cloud-events.md)ページに新しいイベントタイプ（ `ImportData` ）を追加します。

-   TiDB Cloudコンソールから**Playground**を削除します。

    最適化されたエクスペリエンスを備えた新しいスタンドアロン プレイグラウンドにご期待ください。

## 2023年5月23日 {#may-23-2023}

**一般的な変更**

-   CSVファイルをTiDBにアップロードする際、列名には英数字だけでなく、中国語や日本語などの文字も使用できます。ただし、特殊文字についてはアンダースコア（ `_` ）のみがサポートされています。

    詳細は[ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)を参照。

## 2023年5月16日 {#may-16-2023}

**コンソールの変更**

-   専用層とサーバーレス層の両方において、機能カテゴリ別に整理された左側のナビゲーション エントリを導入します。

    新しいナビゲーションにより、機能エントリをより簡単に、より直感的に見つけられるようになりました。新しいナビゲーションを表示するには、クラスターの概要ページにアクセスしてください。

-   Dedicated Tierクラスターの**診断**ページの次の 2 つのタブに新しいネイティブ Web インフラストラクチャをリリースします。

    -   [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)
    -   [SQL文](/tidb-cloud/tune-performance.md#statement-analysis)

    新しいインフラストラクチャにより、2つのタブを簡単に切り替え、より直感的かつ効率的に必要な情報にアクセスできます。また、ユーザーエクスペリエンスも向上し、SQL診断プロセスがよりユーザーフレンドリーになります。

## 2023年5月9日 {#may-9-2023}

**一般的な変更**

-   2023 年 4 月 26 日以降に作成された GCP ホスト クラスタのノード サイズの変更をサポートします。

    この機能により、需要の増加に合わせて高パフォーマンスノードにアップグレードしたり、コスト削減のために低パフォーマンスノードにダウングレードしたりできます。この柔軟性の向上により、ワークロードに合わせてクラスターのキャパシティを調整し、コストを最適化できます。

    詳細な手順については、 [ノードサイズを変更する](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)参照してください。

-   圧縮ファイルのインポート`.zstd`サポートします。CSVファイルとSQLファイルの`.zst`は、 `.gzip` `.gz` 。この機能により、より効率的`.snappy`コスト効率の高いデータインポートが可能になり、データ転送コストを削減できます。

    詳細については、 [クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)および[サンプルデータのインポート](/tidb-cloud/import-sample-data.md)参照してください。

-   TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの新しいネットワーク アクセス管理オプションとして、AWS PrivateLink を利用したエンドポイント接続をサポートします。

    プライベートエンドポイント接続では、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続はCIDR重複をサポートしており、ネットワーク管理が容易になります。

    詳細については[プライベートエンドポイント接続を設定する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのバックアップ、復元、および changefeed アクションを記録するために、 [**イベント**](/tidb-cloud/tidb-cloud-events.md)ページに新しいイベント タイプを追加します。

    記録できるイベントの完全なリストについては、 [記録されたイベント](/tidb-cloud/tidb-cloud-events.md#logged-events)参照してください。

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの[**SQL診断**](/tidb-cloud/tune-performance.md)ページに**SQL ステートメント**タブを導入します。

    **「SQL ステートメント」**タブには次の内容が表示されます。

    -   TiDB データベースによって実行されるすべての SQL ステートメントの包括的な概要により、遅いクエリを簡単に識別して診断できます。
    -   クエリ時間、実行プラン、データベースサーバーの応答など、各 SQL ステートメントの詳細情報が提供され、データベースのパフォーマンスの最適化に役立ちます。
    -   大量のデータを簡単に並べ替え、フィルタリング、検索できるユーザーフレンドリーなインターフェースにより、最も重要なクエリに集中できます。

    詳細については[ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)参照してください。

## 2023年5月6日 {#may-6-2023}

**一般的な変更**

-   TiDB [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターが配置されているリージョンの[データサービスエンドポイント](/tidb-cloud/tidb-cloud-glossary.md#endpoint)の直接アクセスをサポートします。

    新しく作成されたServerless Tierクラスターのエンドポイント URL にクラスターのリージョン情報が含まれるようになりました。リージョンドメイン`<region>.data.tidbcloud.com`リクエストすることで、TiDB クラスターが配置されているリージョンのエンドポイントに直接アクセスできます。

    あるいは、リージョンを指定せずにグローバルドメイン`data.tidbcloud.com`リクエストすることもできます。この場合、 TiDB Cloud は内部的にリクエストをターゲットリージョンにリダイレクトしますが、レイテンシーが増加する可能性があります。この方法を選択する場合は、エンドポイントを呼び出す際に curl コマンドに`--location-trusted`オプションを追加してください。

    詳細については[エンドポイントを呼び出す](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)参照してください。

## 2023年4月25日 {#april-25-2023}

**一般的な変更**

-   組織内の最初の 5 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターについては、 TiDB Cloud は次のようにクラスターごとに無料使用量割り当てを提供します。

    -   行storage: 5 GiB
    -   [リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月間5,000万RU

    2023年5月31日まで、Serverless Tierのクラスターは引き続き無料で、100%割引となります。それ以降は、無料枠を超えた使用量に対して料金が発生します。

    クラスターの**概要**ページの**「今月の使用量」**エリアで簡単に[クラスターの使用状況を監視するか、使用量の割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#manage-spending-limit-for-tidb-cloud-serverless-scalable-clusters)確認できます。クラスターの無料クォータに達すると、クォータを増やすか、新しい月の開始時に使用量がリセットされるまで、このクラスターの読み取りおよび書き込み操作は制限されます。

    さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク送信など) の RU 消費量、価格の詳細、スロットル情報の詳細については、 [TiDB CloudServerless Tierの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)参照してください。

-   TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのバックアップと復元をサポートします。

    詳細については[TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md)参照してください。

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)から[バージョン6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)にアップグレードします。

-   メンテナンス ウィンドウ機能を提供して、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの計画されたメンテナンス アクティビティを簡単にスケジュールおよび管理できるようにします。

    メンテナンス ウィンドウとは、 TiDB Cloudサービスの信頼性、セキュリティ、パフォーマンスを確保するために、オペレーティング システムの更新、セキュリティ パッチ、インフラストラクチャのアップグレードなどの計画されたメンテナンス アクティビティが自動的に実行される指定された期間です。

    メンテナンス期間中は、一時的な接続中断やQPSの変動が発生する可能性がありますが、クラスタは引き続き利用可能であり、SQL操作、既存のデータインポート、バックアップ、リストア、移行、レプリケーションタスクは通常通り実行されます。メンテナンス中は[許可された操作と許可されていない操作のリスト](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)ご覧ください。

    メンテナンスの頻度を最小限に抑えるよう努めます。メンテナンス期間が予定されている場合、デフォルトの開始時間は対象週の水曜日午前3時（ TiDB Cloud組織のタイムゾーンに基づく）です。サービス中断の可能性を回避するために、メンテナンススケジュールをご確認いただき、それに応じて運用を計画していただくことが重要です。

    -   最新情報をお届けするために、 TiDB Cloud はメンテナンス ウィンドウごとに 3 つの電子メール通知を送信します。1 つはメンテナンス タスクの前、1 つは開始時、もう 1 つはメンテナンス タスクの後です。
    -   メンテナンスの影響を最小限に抑えるには、 **「メンテナンス」**ページでメンテナンスの開始時刻を希望の時間に変更したり、メンテナンス アクティビティを延期したりすることができます。

    詳細については[メンテナンスウィンドウを構成する](/tidb-cloud/configure-maintenance-window.md)参照してください。

-   AWS でホストされ、2023 年 4 月 25 日以降に作成された[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの TiDB ノードをスケーリングするときに、TiDB の負荷分散を改善し、接続の切断を減らします。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は AWS でホストされているすべてのDedicated Tierクラスターに提供されています。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャにより、 [監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ目から簡単にナビゲートし、より直感的かつ効率的に必要な情報にアクセスできます。また、UXに関する多くの問題も解決され、監視プロセスがよりユーザーフレンドリーになります。

## 2023年4月18日 {#april-18-2023}

**一般的な変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して[データ移行ジョブの仕様](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)スケールアップまたはスケールダウンをサポートします。

    この機能を使用すると、仕様を拡大して移行のパフォーマンスを向上させたり、仕様を縮小してコストを削減したりできます。

    詳細については[データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)参照してください。

**コンソールの変更**

-   UI を改良して[クラスターの作成](https://tidbcloud.com/clusters/create-cluster)をさらにユーザーフレンドリーにし、数回クリックするだけでクラスターを作成および構成できるようになりました。

    新しいデザインは、シンプルさを重視し、視覚的な煩雑さを軽減し、明確な指示を提供します。クラスター作成ページで**「作成」を**クリックすると、クラスターの作成が完了するのを待たずに、クラスターの概要ページに移動します。

    詳細については[クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。

-   **請求**ページに**割引**タブを導入し、組織の所有者と請求管理者向けの割引情報を表示します。

    詳細については[割引](/tidb-cloud/tidb-cloud-billing.md#discounts)参照してください。

## 2023年4月11日 {#april-11-2023}

**一般的な変更**

-   AWS でホストされている[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの TiDB ノードをスケーリングするときに、TiDB の負荷分散を改善し、接続の切断を減らします。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は AWS `Oregon (us-west-2)`リージョンでホストされているDedicated Tierクラスターに対してのみ提供されています。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して[ニューレリック](https://newrelic.com/)統合をサポートします。

    New Relicとの連携により、 TiDB Cloudを設定してTiDBクラスターのメトリックデータを[ニューレリック](https://newrelic.com/)に送信できます。これにより、 [ニューレリック](https://newrelic.com/)でアプリケーションパフォーマンスとTiDBデータベースパフォーマンスの両方を監視・分析できます。この機能により、潜在的な問題を迅速に特定してトラブルシューティングし、解決時間を短縮できます。

    統合手順と利用可能なメトリックについては、 [TiDB CloudとNew Relicの統合](/tidb-cloud/monitor-new-relic-integration.md)参照してください。

-   Dedicated Tierクラスターの Prometheus 統合に次の[チェンジフィード](/tidb-cloud/changefeed-overview.md)メトリックを追加します。

    -   `tidbcloud_changefeed_latency`
    -   `tidbcloud_changefeed_replica_rows`

    [TiDB CloudとPrometheusを統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)お持ちの場合は、これらのメトリクスを使用して、変更フィードのパフォーマンスと健全性をリアルタイムで監視できます。さらに、Prometheus を使用してメトリクスを監視するためのアラートを簡単に作成できます。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページを[ノードレベルのリソースメトリック](/tidb-cloud/built-in-monitoring.md#server)使用するように更新します。

    ノード レベルのリソース メトリックを使用すると、リソース消費量をより正確に表示して、購入したサービスの実際の使用状況をよりよく理解できます。

    これらのメトリックにアクセスするには、クラスターの[監視](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページに移動し、 **[メトリック]**タブの**[サーバー]**カテゴリを確認します。

-   **プロジェクト別概要**と**サービス別概要**の請求項目を再編成して[請求する](/tidb-cloud/tidb-cloud-billing.md#billing-details)ページを最適化し、請求情報をより明確にします。

## 2023年4月4日 {#april-4-2023}

**一般的な変更**

-   誤検知を防ぐため、 [TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions)から以下の 2 つのアラートを削除します。これは、ノードの 1 つで一時的なオフラインまたはメモリ不足 (OOM) が発生しても、クラスター全体の健全性に大きな影響を与えないためです。

    -   クラスター内の少なくとも 1 つの TiDB ノードでメモリ不足が発生しました。
    -   1 つ以上のクラスター ノードがオフラインです。

**コンソールの変更**

-   各Dedicated Tierクラスターのアクティブなアラートとクローズされたアラートの両方を一覧表示する、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[アラート](/tidb-cloud/monitor-built-in-alerting.md)ページを導入します。

    **アラート**ページには次の内容が表示されます。

    -   直感的で使いやすいユーザーインターフェース。アラート通知メールを購読していない場合でも、このページでクラスターのアラートを確認できます。
    -   高度なフィルタリングオプションにより、アラートの重大度、ステータス、その他の属性に基づいて、アラートを素早く検索・並べ替えることができます。また、過去7日間の履歴データを表示できるため、アラート履歴の追跡が容易になります。
    -   **ルール編集**機能。クラスターの特定のニーズに合わせてアラートルール設定をカスタマイズできます。

    詳細については[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)参照してください。

-   TiDB Cloudのヘルプ関連の情報とアクションを 1 か所に統合​​します。

    これで、 [TiDB Cloudコンソール](https://tidbcloud.com/)右下隅にある**[?]**をクリックして、 [TiDB Cloudヘルプ情報](/tidb-cloud/tidb-cloud-support.md)すべて取得し、サポートに問い合わせることができます。

-   TiDB Cloudについて理解を深めるのに役立つ[はじめる](https://tidbcloud.com/getting-started)ページを紹介します。

    **「はじめに」**ページでは、インタラクティブなチュートリアル、必須ガイド、役立つリンクを提供しています。インタラクティブなチュートリアルに従うことで、業界固有のデータセット（SteamゲームデータセットとS&amp;P 500データセット）を活用し、 TiDB Cloudの機能とHTAP機能を簡単に体験できます。

    **「はじめに」**ページにアクセスするには、 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> [TiDB Cloudコンソール](https://tidbcloud.com/)の左側のナビゲーションバーにある**「Getting Started」をクリックしてください**。このページでは、 **「Query Sample Dataset」**をクリックしてインタラクティブチュートリアルを開いたり、他のリンクをクリックしてTiDB Cloudを探索したりできます。または、右下隅の**「?」**をクリックして**「Interactive Tutorials」**をクリックすることもできます。

## 2023年3月29日 {#march-29-2023}

**一般的な変更**

-   [データサービス（ベータ版）](/tidb-cloud/data-service-overview.md) 、データ アプリに対するよりきめ細かいアクセス制御がサポートされます。

    データアプリの詳細ページで、クラスタをデータアプリにリンクし、各APIキーのロールを指定できるようになりました。ロールは、APIキーがリンクされたクラスタへのデータの読み取りまたは書き込みを許可するかどうかを制御し、 `ReadOnly`または`ReadAndWrite`に設定できます。この機能により、データアプリに対してクラスタレベルおよび権限レベルのアクセス制御が可能になり、ビジネスニーズに応じてアクセス範囲をより柔軟に制御できるようになります。

    詳細については、 [リンクされたクラスターを管理する](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)および[APIキーを管理する](/tidb-cloud/data-service-api-key.md)参照してください。

## 2023年3月28日 {#march-28-2023}

**一般的な変更**

-   [チェンジフィード](/tidb-cloud/changefeed-overview.md)に 2 RCU、4 RCU、8 RCU 仕様を追加し、 [チェンジフィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)ときに希望の仕様を選択できるようにサポートします。

    これらの新しい仕様を使用すると、以前は 16 個の RCU が必要だったシナリオと比較して、データ複製コストを最大 87.5% 削減できます。

-   2023 年 3 月 28 日以降に作成された[チェンジフィード](/tidb-cloud/changefeed-overview.md)スケールアップまたはスケールダウン仕様をサポートします。

    より高い仕様を選択するとレプリケーションのパフォーマンスが向上し、より低い仕様を選択するとレプリケーションのコストが削減されます。

    詳細については[チェンジフィードをスケールする](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)参照してください。

-   AWS の[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターから同じプロジェクトおよび同じリージョン内の[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターへの増分データのリアルタイム複製をサポートします。

    詳細については[TiDB Cloudにシンク](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)参照してください。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能に対して 2 つの新しい GCP リージョン ( `Singapore (asia-southeast1)`と`Oregon (us-west1)`をサポートします。

    これらの新しいリージョンにより、 TiDB Cloudへのデータ移行の選択肢が広がります。アップストリームデータがこれらのリージョン内またはその付近に保存されている場合、GCP からTiDB Cloudへのより高速で信頼性の高いデータ移行を活用できるようになります。

    詳細については[データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの[遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    この新しいインフラストラクチャにより、 [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ページ目を簡単にナビゲートし、より直感的かつ効率的に必要な情報にアクセスできます。また、UXに関する多くの問題も解決され、SQL診断プロセスがよりユーザーフレンドリーになります。

## 2023年3月21日 {#march-21-2023}

**一般的な変更**

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service) for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターを導入すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でデータにアクセスできるようになります。

    Data Service を使用すると、 TiDB Cloud をHTTPS 対応のあらゆるアプリケーションやサービスとシームレスに統合できます。一般的なシナリオを以下に示します。

    -   モバイル アプリケーションまたは Web アプリケーションから TiDB クラスターのデータベースに直接アクセスします。
    -   サーバーレス エッジ関数を使用してエンドポイントを呼び出し、データベース接続プールによって発生するスケーラビリティの問題を回避します。
    -   データ サービスをデータ ソースとして使用して、 TiDB Cloud をデータ視覚化プロジェクトと統合します。
    -   MySQL インターフェースがサポートしていない環境からデータベースに接続します。

    さらに、 TiDB Cloud は、AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェースである[Chat2Query API](/tidb-cloud/use-chat2query-api.md)提供します。

    データサービスにアクセスするには、左側のナビゲーションペインの[**データサービス**](https://tidbcloud.com/project/data-service)ページ目に移動します。詳細については、以下のドキュメントをご覧ください。

    -   [データサービスの概要](/tidb-cloud/data-service-overview.md)
    -   [データサービスを始める](/tidb-cloud/data-service-get-started.md)
    -   [Chat2Query APIを使い始める](/tidb-cloud/use-chat2query-api.md)

-   AWS でホストされ、2022 年 12 月 31 日以降に作成される[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでスケールするために、TiDB、TiKV、およびTiFlashノードのサイズを縮小することをサポートします。

    ノード サイズを[TiDB Cloudコンソール経由](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)または[TiDB Cloud API（ベータ版）経由](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)減らすことができます。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能に対して新しい GCP リージョンをサポートします: `Tokyo (asia-northeast1)` 。

    この機能を使用すると、Google Cloud Platform (GCP) の MySQL 互換データベースから TiDB クラスタにデータを簡単かつ効率的に移行できます。

    詳細については[データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

**コンソールの変更**

-   クラスターの主な変更の記録を提供する、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの**イベント**ページを紹介します。

    このページでは、過去7日間のイベント履歴を表示し、トリガー時刻やアクションを開始したユーザーなどの重要な詳細を追跡できます。例えば、クラスターが一時停止された時刻や、クラスターのサイズを変更したユーザーなどのイベントを確認できます。

    詳細については[TiDB Cloudクラスター イベント](/tidb-cloud/tidb-cloud-events.md)参照してください。

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの**[監視]**ページに**[データベース ステータス]**タブを追加します。ここには、次のデータベース レベルのメトリックが表示されます。

    -   DBあたりのQPS
    -   DBあたりの平均クエリ実行時間
    -   DBあたりの失敗したクエリ数

    これらのメトリックを使用すると、個々のデータベースのパフォーマンスを監視し、データに基づいて意思決定を行い、アプリケーションのパフォーマンスを向上させるためのアクションを実行できます。

    詳細については[Serverless Tierクラスターのモニタリングメトリクス](/tidb-cloud/built-in-monitoring.md)参照してください。

## 2023年3月14日 {#march-14-2023}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0)から[バージョン6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)にアップグレードします。

-   ヘッダー行を含むローカル CSV ファイルをアップロードするときに、 TiDB Cloudによって作成されるターゲット テーブルの列名の変更をサポートします。

    ヘッダー行を含むローカルCSVファイルを[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスタにインポートする際、 TiDB Cloudでターゲットテーブルを作成する必要があり、ヘッダー行の列名がTiDB Cloudの列命名規則に従っていない場合、対応する列名の横に警告アイコンが表示されます。この警告を解決するには、アイコンの上にカーソルを移動し、メッセージに従って既存の列名を編集するか、新しい列名を入力してください。

    列の命名規則については、 [ローカルファイルをインポートする](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)参照してください。

## 2023年3月7日 {#march-7-2023}

**一般的な変更**

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのデフォルトの TiDB バージョンを[バージョン6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)から[バージョン6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)にアップグレードします。

## 2023年2月28日 {#february-28-2023}

**一般的な変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに[SQL診断](/tidb-cloud/tune-performance.md)機能を追加します。

    SQL診断を使用すると、SQL関連の実行時ステータスに関する詳細な分析情報を取得できるため、SQLパフォーマンスチューニングの効率が向上します。現在、Serverless TierのSQL診断機能は、低速クエリデータのみを提供しています。

    SQL 診断を使用するには、 Serverless Tierクラスター ページの左側のナビゲーション バーで**[SQL 診断] を**クリックします。

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

    コンソール監査ログ機能は、ロール`Owner`または`Audit Admin`ユーザーのみに表示され、デフォルトでは無効になっています。有効にするには、<mdsvgicon name="icon-top-organization"> [TiDB Cloudコンソール](https://tidbcloud.com/)の右上隅にある**[組織]** &gt; **[コンソール監査ログ] を選択します**。</mdsvgicon>

    コンソール監査ログを分析することで、組織内で実行された不審な操作を特定し、組織のリソースとデータのセキュリティを向上させることができます。

    詳細については[コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)参照してください。

**CLIの変更**

-   [TiDB CloudCLI](/tidb-cloud/cli-reference.md)に新しいコマンド`ticloud cluster connect-info`を追加します。

    `ticloud cluster connect-info` 、クラスターの接続文字列を取得できるコマンドです。このコマンドを使用するには、 [`ticloud`を更新する](/tidb-cloud/ticloud-upgrade.md)からv0.3.2以降のバージョンが必要です。

## 2023年2月21日 {#february-21-2023}

**一般的な変更**

-   TiDB Cloudにデータをインポートするときに、 IAMユーザーの AWS アクセスキーを使用して Amazon S3 バケットにアクセスすることをサポートします。

    この方法はロールARNを使用するよりも簡単です。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)を参照してください。

-   [監視メトリクスの保持期間](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 2 日からより長い期間に延長します。

    -   Dedicated Tierクラスターの場合、過去 7 日間のメトリック データを表示できます。
    -   Serverless Tierクラスターの場合、過去 3 日間のメトリック データを表示できます。

    メトリクスの保持期間を延長することで、より多くの履歴データにアクセスできるようになります。これにより、クラスターの傾向やパターンを特定し、より適切な意思決定と迅速なトラブルシューティングが可能になります。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの監視ページで新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャにより、モニタリングページを簡単に操作し、より直感的かつ効率的に必要な情報にアクセスできるようになりました。また、新しいインフラストラクチャはUXに関する多くの問題を解決し、モニタリングプロセスを大幅にユーザーフレンドリーなものにしています。

## 2023年2月17日 {#february-17-2023}

**CLIの変更**

-   [TiDB CloudCLI](/tidb-cloud/cli-reference.md)に新しいコマンド[`ticloud connect`](/tidb-cloud/ticloud-serverless-shell.md)を追加します。

    `ticloud connect` 、SQL クライアントをインストールすることなく、ローカルマシンからTiDB Cloudクラスターに接続できるコマンドです。TiDB TiDB Cloudクラスターに接続した後、 TiDB Cloud CLI で SQL ステートメントを実行できます。

## 2023年2月14日 {#february-14-2023}

**一般的な変更**

-   TiDB [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでスケールするために TiKV ノードとTiFlashノードの数を減らすことをサポートします。

    ノード番号を[TiDB Cloudコンソール経由](/tidb-cloud/scale-tidb-cluster.md#change-node-number)または[TiDB Cloud API（ベータ版）経由](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)減らすことができます。

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの**監視**ページを紹介します。

    **モニタリング**ページには、1 秒あたりに実行される SQL ステートメントの数、クエリの平均実行時間、失敗したクエリの数など、さまざまなメトリックとデータが提供され、 Serverless Tierクラスター内の SQL ステートメントの全体的なパフォーマンスをよりよく理解するのに役立ちます。

    詳細については[TiDB Cloud組み込み監視](/tidb-cloud/built-in-monitoring.md)参照してください。

## 2023年2月2日 {#february-2-2023}

**CLIの変更**

-   TiDB Cloud CLI クライアント[`ticloud`](/tidb-cloud/cli-reference.md)を紹介します。

    `ticloud`使用すると、ターミナルやその他の自動ワークフローから数行のコマンドでTiDB Cloudリソースを簡単に管理できます。特にGitHub Actionsについては、 `ticloud`簡単に設定できるように[`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli)提供しています。

    詳細については、 [TiDB Cloud CLI クイックスタート](/tidb-cloud/get-started-with-cli.md)および[TiDB CloudCLI リファレンス](/tidb-cloud/cli-reference.md)参照してください。

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
    -   [TiDB クラスタ データのバックアップと復元](/tidb-cloud/backup-and-restore.md)

## 2023年1月10日 {#january-10-2023}

**一般的な変更**

-   ローカル CSV ファイルから TiDB にデータをインポートする機能を最適化し、 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのユーザー エクスペリエンスを向上させます。

    -   CSV ファイルをアップロードするには、**インポート**ページのアップロード領域にドラッグ アンド ドロップするだけです。
    -   インポートタスクを作成する際に、対象のデータベースまたはテーブルが存在しない場合は、名前を入力することでTiDB Cloudが自動的に作成します。作成する対象テーブルには、主キーを指定するか、複数のフィールドを選択して複合主キーを形成することができます。
    -   インポートが完了したら、 **「Chat2Query でデータを探索」**をクリックするか、タスク リストでターゲット テーブル名をクリックすると、 [AI搭載のChat2Query](/tidb-cloud/explore-data-with-chat2query.md)でデータを探索できます。

    詳細については[ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)参照してください。

**コンソールの変更**

-   特定のクラスターに対するサポートを要求するプロセスを簡素化するために、各クラスターに**「サポートの取得」**オプションを追加します。

    クラスターのサポートは、次のいずれかの方法でリクエストできます。

    -   プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページで、クラスターの行にある**[...]**をクリックし、 **[サポートを受ける]**を選択します。
    -   クラスターの概要ページで、右上隅の**[...]**をクリックし、 **[サポートを受ける]**を選択します。

## 2023年1月5日 {#january-5-2023}

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの SQL Editor (ベータ) の名前を Chat2Query (ベータ) に変更し、AI を使用した SQL クエリの生成をサポートします。

    Chat2Query では、AI に SQL クエリを自動的に生成させたり、SQL クエリを手動で記述したり、ターミナルなしでデータベースに対して SQL クエリを実行したりできます。

    Chat2Query にアクセスするには、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、クラスター名をクリックして、左側のナビゲーション ペインで**Chat2Query を**クリックします。

## 2023年1月4日 {#january-4-2023}

**一般的な変更**

-   AWS でホストされ、2022 年 12 月 31 日以降に作成されたTiDB Cloud Dedicated クラスターの**ノード サイズ (vCPU + RAM) を**増やすことで、TiDB、TiKV、およびTiFlashノードのスケールアップをサポートします。

    ノード サイズを[TiDB Cloudコンソールを使用する](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)または[TiDB Cloud API（ベータ版）を使用する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)増やすことができます。

-   [**監視**](/tidb-cloud/built-in-monitoring.md)ページのメトリックの保持期間を 2 日間に延長します。

    これで、過去 2 日間のメトリック データにアクセスできるようになり、クラスターのパフォーマンスと傾向をより柔軟かつ明確に把握できるようになります。

    この改善は追加費用なしで、クラスターの[**監視**](/tidb-cloud/built-in-monitoring.md)ページ目の**「診断」**タブからアクセスできます。これにより、パフォーマンスの問題を特定してトラブルシューティングし、クラスター全体の健全性をより効果的に監視できるようになります。

-   Prometheus 統合のための Grafana ダッシュボード JSON のカスタマイズをサポートします。

    [TiDB CloudとPrometheusを統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)お持ちの場合は、事前に構築されたGrafanaダッシュボードをインポートしてTiDB Cloudクラスターを監視し、ニーズに合わせてダッシュボードをカスタマイズできるようになりました。この機能により、 TiDB Cloudクラスターを簡単かつ迅速に監視し、パフォーマンスの問題を迅速に特定できるようになります。

    詳細については[Grafana GUIダッシュボードを使用してメトリックを視覚化する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)参照してください。

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのデフォルトのTiDBバージョンを[バージョン6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[バージョン6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。Serverless Serverless Tierコールドスタートの問題が解決されました。

**コンソールの変更**

-   [**クラスター**](https://tidbcloud.com/project/clusters)ページ目とクラスター概要ページの表示を簡素化します。

    -   [**クラスター**](https://tidbcloud.com/project/clusters)ページのクラスター名をクリックすると、クラスターの概要ページに入り、クラスターの操作を開始できます。
    -   クラスター概要ページから**「接続」ペイン**と**「インポート」**ペインを削除します。右上隅の**「接続」**をクリックすると接続情報が表示され、左側のナビゲーションペインの**「インポート」を**クリックするとデータをインポートできます。
