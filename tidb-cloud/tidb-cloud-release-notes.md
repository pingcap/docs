---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2023 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2023}

このページには 2023 年[<a href="https://www.pingcap.com/tidb-cloud/">TiDB Cloud</a>](https://www.pingcap.com/tidb-cloud/)のリリースノートが記載されています。

## 2023 年 6 月 6 日 {#june-6-2023}

-   [<a href="/tidb-cloud/index-insight.md">インデックスインサイト（ベータ版）</a>](/tidb-cloud/index-insight.md) for [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">TiDB専用</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターを導入します。これは、遅いクエリに対してインデックスの推奨を提供することでクエリのパフォーマンスを最適化します。

    Index Insight を使用すると、次の方法でアプリケーション全体のパフォーマンスとデータベース操作の効率を向上させることができます。

    -   クエリのパフォーマンスの強化: Index Insight は遅いクエリを特定し、それらに適切なインデックスを提案します。これにより、クエリの実行が高速化され、応答時間が短縮され、ユーザー エクスペリエンスが向上します。
    -   コスト効率: Index Insight を使用してクエリ パフォーマンスを最適化すると、追加のコンピューティング リソースの必要性が減り、既存のインフラストラクチャをより効果的に使用できるようになります。これにより、運用コストの削減につながる可能性があります。
    -   簡素化された最適化プロセス: Index Insight は、インデックスの改善点の特定と実装を簡素化し、手動による分析や推測の必要性を排除します。その結果、正確なインデックス推奨により時間と労力を節約できます。
    -   アプリケーション効率の向上: Index Insight を使用してデータベースのパフォーマンスを最適化することで、 TiDB Cloud上で実行されるアプリケーションはより大きなワークロードを処理し、より多くのユーザーに同時にサービスを提供できるため、アプリケーションのスケーリング操作がより効率的になります。

    Index Insight を使用するには、TiDB 専用クラスターの**[診断]**ページに移動し、 **[Index Insight BETA]**タブをクリックします。

    詳細については、 [<a href="/tidb-cloud/index-insight.md">Index Insight を使用する (ベータ版)</a>](/tidb-cloud/index-insight.md)を参照してください。

-   登録やインストールを行わずに TiDB の全機能を体験できる対話型プラットフォーム[<a href="https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes">TiDB プレイグラウンド</a>](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes)を紹介します。

    TiDB Playground は、スケーラビリティ、MySQL 互換性、リアルタイム分析などの TiDB の機能を探索するためのワンストップ ショップ エクスペリエンスを提供するように設計された対話型プラットフォームです。

    TiDB Playground を使用すると、複雑な構成を必要とせず、制御された環境で TiDB の機能をリアルタイムで試すことができるため、TiDB の機能を理解するのに最適です。

    TiDB Playground の使用を開始するには、 [<a href="https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes">**TiDB プレイグラウンド**</a>](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_release_notes)ページに移動し、探索したい機能を選択して、探索を開始します。

## 2023 年 6 月 5 日 {#june-5-2023}

-   [<a href="/tidb-cloud/tidb-cloud-glossary.md#data-app">データアプリ</a>](/tidb-cloud/tidb-cloud-glossary.md#data-app)の GitHub への接続をサポートします。

    [<a href="/tidb-cloud/data-service-manage-github-connection.md">データ アプリを GitHub に接続する</a>](/tidb-cloud/data-service-manage-github-connection.md)により、データ アプリのすべての構成を Github 上で[<a href="/tidb-cloud/data-service-app-config-files.md">コードファイル</a>](/tidb-cloud/data-service-app-config-files.md)として管理できるようになり、 TiDB Cloudデータ サービスがシステムアーキテクチャおよび DevOps プロセスとシームレスに統合されます。

    この機能を使用すると、次のタスクを簡単に実行できるため、データ アプリ開発の CI/CD エクスペリエンスが向上します。

    -   GitHub を使用して Data App の変更を自動的にデプロイします。
    -   バージョン管理を使用して、GitHub 上のデータ アプリ変更の CI/CD パイプラインを構成します。
    -   接続されている GitHub リポジトリから切断します。
    -   導入前にエンドポイントの変更を確認します。
    -   導入履歴をビュー、障害が発生した場合に必要なアクションを実行します。
    -   コミットを再デプロイして、以前のデプロイメントにロールバックします。

    詳細については、 [<a href="/tidb-cloud/data-service-manage-github-connection.md">GitHub を使用してデータ アプリを自動的にデプロイ</a>](/tidb-cloud/data-service-manage-github-connection.md)を参照してください。

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

    詳細は[<a href="/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md">データ移行を使用して、MySQL 互換データベースからTiDB Cloudに増分データのみを移行する</a>](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)を参照してください。

-   新しいイベント タイプ ( `ImportData` ) を[<a href="/tidb-cloud/tidb-cloud-events.md">**イベント**</a>](/tidb-cloud/tidb-cloud-events.md)ページに追加します。

-   TiDB Cloudコンソールから**Playground**を削除します。

    最適化されたエクスペリエンスを備えた新しいスタンドアロン プレイグラウンドにご期待ください。

## 2023 年 5 月 23 日 {#may-23-2023}

**一般的な変更点**

-   CSV ファイルを TiDB にアップロードする場合、列名を定義するために英語の文字と数字だけでなく、中国語や日本語などの文字も使用できます。ただし、特殊文字の場合は、アンダースコア ( `_` ) のみがサポートされます。

    詳細は[<a href="/tidb-cloud/tidb-cloud-import-local-files.md">ローカル ファイルをTiDB Cloudにインポートする</a>](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

## 2023 年 5 月 16 日 {#may-16-2023}

**コンソールの変更**

-   専用層とサーバーレス層の両方について、機能カテゴリ別に整理された左側のナビゲーション エントリを紹介します。

    新しいナビゲーションにより、機能エントリをより簡単かつ直感的に見つけることができるようになります。新しいナビゲーションを表示するには、クラスターの概要ページにアクセスします。

-   Dedicated Tierクラスターの**[診断]**ページの次の 2 つのタブに対して、新しいネイティブ Web インフラストラクチャをリリースします。

    -   [<a href="/tidb-cloud/tune-performance.md#slow-query">遅いクエリ</a>](/tidb-cloud/tune-performance.md#slow-query)
    -   [<a href="/tidb-cloud/tune-performance.md#statement-analysis">SQL文</a>](/tidb-cloud/tune-performance.md#statement-analysis)

    新しいインフラストラクチャを使用すると、2 つのタブを簡単に移動して、より直観的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャによりユーザー エクスペリエンスも向上し、SQL 診断プロセスがより使いやすくなりました。

## 2023 年 5 月 9 日 {#may-9-2023}

**一般的な変更点**

-   2023 年 4 月 26 日以降に作成された GCP ホスト型クラスターのノード サイズの変更をサポートします。

    この機能を使用すると、需要の増加に合わせてより高性能のノードにアップグレードしたり、コストを節約するためにより低いパフォーマンスのノードにダウングレードしたりできます。この柔軟性の追加により、クラスターの容量をワークロードに合わせて調整し、コストを最適化することができます。

    詳細な手順については、 [<a href="/tidb-cloud/scale-tidb-cluster.md#change-node-size">ノードサイズの変更</a>](/tidb-cloud/scale-tidb-cluster.md#change-node-size)を参照してください。

-   圧縮ファイルのインポートをサポートします。 CSV および SQL ファイルは、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、および`.snappy`の形式でインポートできます。この機能は、データをインポートするためのより効率的かつコスト効率の高い方法を提供し、データ転送コストを削減します。

    詳細については、 [<a href="/tidb-cloud/import-csv-files.md">Amazon S3 または GCS からTiDB Cloudに CSV ファイルをインポート</a>](/tidb-cloud/import-csv-files.md)および[<a href="/tidb-cloud/import-sample-data.md">サンプルデータのインポート</a>](/tidb-cloud/import-sample-data.md)を参照してください。

-   TiDB Cloud [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターの新しいネットワーク アクセス管理オプションとして、AWS PrivateLink を利用したエンドポイント接続をサポートします。

    プライベート エンドポイント接続では、データがパブリック インターネットに公開されません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

    詳細については、 [<a href="/tidb-cloud/set-up-private-endpoint-connections.md">プライベートエンドポイント接続のセットアップ</a>](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。

**コンソールの変更**

-   新しいイベント タイプを[<a href="/tidb-cloud/tidb-cloud-events.md">**イベント**</a>](/tidb-cloud/tidb-cloud-events.md)ページに追加して、 [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのバックアップ、復元、変更フィード アクションを記録します。

    記録できるイベントの完全なリストを取得するには、 [<a href="/tidb-cloud/tidb-cloud-events.md#logged-events">記録されたイベント</a>](/tidb-cloud/tidb-cloud-events.md#logged-events)を参照してください。

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)のクラスターの[<a href="/tidb-cloud/tune-performance.md">**SQL診断**</a>](/tidb-cloud/tune-performance.md)ページに**[SQL ステートメント]**タブを導入します。

    **[SQL ステートメント]**タブには次のものが表示されます。

    -   TiDB データベースによって実行されるすべての SQL ステートメントの包括的な概要。これにより、遅いクエリを簡単に特定して診断できます。
    -   クエリ時間、実行計画、データベースサーバーの応答など、各 SQL ステートメントに関する詳細情報を提供し、データベースのパフォーマンスの最適化に役立ちます。
    -   ユーザーフレンドリーなインターフェイスにより、大量のデータの並べ替え、フィルター、検索が簡単になり、最も重要なクエリに集中できるようになります。

    詳細については、 [<a href="/tidb-cloud/tune-performance.md#statement-analysis">ステートメント分析</a>](/tidb-cloud/tune-performance.md#statement-analysis)を参照してください。

## 2023 年 5 月 6 日 {#may-6-2023}

**一般的な変更点**

-   TiDB [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターが配置されているリージョン内の[<a href="/tidb-cloud/tidb-cloud-glossary.md#endpoint">データサービスエンドポイント</a>](/tidb-cloud/tidb-cloud-glossary.md#endpoint)への直接アクセスをサポートします。

    新しく作成されたServerless Tierクラスターの場合、エンドポイント URL にクラスターのリージョン情報が含まれるようになりました。リージョン ドメイン`<region>.data.tidbcloud.com`をリクエストすると、TiDB クラスターが配置されているリージョンのエンドポイントに直接アクセスできます。

    あるいは、リージョンを指定せずにグローバル ドメイン`data.tidbcloud.com`をリクエストすることもできます。この方法で、 TiDB Cloudはリクエストを内部的にターゲット リージョンにリダイレクトしますが、これにより追加のレイテンシーが発生する可能性があります。この方法を選択した場合は、エンドポイントを呼び出すときに必ず`--location-trusted`オプションをcurl コマンドに追加してください。

    詳細については、 [<a href="/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint">エンドポイントを呼び出す</a>](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)を参照してください。

## 2023 年 4 月 25 日 {#april-25-2023}

**一般的な変更点**

-   組織内の最初の 5 つの[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターに対して、 TiDB Cloud は各クラスターに次のように無料の使用クォータを提供します。

    -   行storage: 5 GiB
    -   [<a href="/tidb-cloud/tidb-cloud-glossary.md#request-unit">リクエストユニット (RU)</a>](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月あたり 5,000 万 RU

    2023 年 5 月 31 日まで、Serverless Tierクラスターは引き続き無料で、100% 割引になります。それ以降、無料枠を超えた使用には料金が発生します。

    クラスターの**概要**ページの**[今月の使用量]**領域で簡単に[<a href="/tidb-cloud/manage-serverless-spend-limit.md#manage-spend-limit-for-tidb-serverless-clusters">クラスターの使用状況を監視するか、使用量クォータを増やします</a>](/tidb-cloud/manage-serverless-spend-limit.md#manage-spend-limit-for-tidb-serverless-clusters)できます。クラスターの無料クォータに達すると、クォータを増やすか、新しい月の初めに使用量がリセットされるまで、このクラスターでの読み取りおよび書き込み操作は抑制されます。

    さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク下りなど) の RU 消費量、料金の詳細、および調整された情報の詳細については、 [<a href="https://www.pingcap.com/tidb-cloud-serverless-pricing-details">TiDB CloudServerless Tierの料金詳細</a>](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

-   TiDB Cloud [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターのバックアップと復元をサポートします。

    詳細については、 [<a href="/tidb-cloud/backup-and-restore.md#tidb-serverless">TiDBクラスタデータのバックアップと復元</a>](/tidb-cloud/backup-and-restore.md#tidb-serverless)を参照してください。

-   新しい[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[<a href="https://docs.pingcap.com/tidb/v6.5/release-6.5.1">v6.5.1</a>](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)から[<a href="https://docs.pingcap.com/tidb/v6.5/release-6.5.2">v6.5.2</a>](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)にアップグレードします。

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの計画されたメンテナンス アクティビティを簡単にスケジュールおよび管理できるようにするメンテナンス ウィンドウ機能を提供します。

    メンテナンス ウィンドウとは、 TiDB Cloudサービスの信頼性、セキュリティ、パフォーマンスを確保するために、オペレーティング システムのアップデート、セキュリティ パッチ、インフラストラクチャのアップグレードなどの計画されたメンテナンス アクティビティが自動的に実行される指定された時間枠です。

    メンテナンス期間中は、一時的な接続の中断や QPS の変動が発生する可能性がありますが、クラスターは引き続き使用可能であり、SQL 操作、既存のデータのインポート、バックアップ、復元、移行、およびレプリケーションのタスクは通常どおり実行できます。メンテナンス中は[<a href="/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window">許可される操作と禁止される操作のリスト</a>](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)を参照してください。

    メンテナンスの頻度を最小限に抑えるよう努めてまいります。メンテナンス期間が計画されている場合、デフォルトの開始時刻は対象週の水曜日の 03:00 ( TiDB Cloud組織のタイムゾーンに基づく) です。潜在的な中断を回避するには、メンテナンスのスケジュールを認識し、それに応じて運用を計画することが重要です。

    -   常に最新の情報を入手できるように、 TiDB Cloudはメンテナンス期間ごとに 3 回の電子メール通知を送信します (メンテナンス タスクの前に 1 回、メンテナンス タスクの開始前に 1 回、メンテナンス タスクの後に 1 回)。
    -   メンテナンスの影響を最小限に抑えるために、 **[メンテナンス]**ページでメンテナンスの開始時刻を希望の時刻に変更するか、メンテナンス アクティビティを延期することができます。

    詳細については、 [<a href="/tidb-cloud/configure-maintenance-window.md">メンテナンスウィンドウの構成</a>](/tidb-cloud/configure-maintenance-window.md)を参照してください。

-   AWS でホストされ、2023 年 4 月 25 日以降に作成された[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの TiDB ノードをスケーリングするときに、TiDB のロード バランシングを改善し、接続ドロップを削減します。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は、AWS でホストされているすべてのDedicated Tierクラスターに提供されています。

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの[<a href="/tidb-cloud/built-in-monitoring.md#view-the-metrics-page">モニタリング</a>](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャを使用すると、 [<a href="/tidb-cloud/built-in-monitoring.md#view-the-metrics-page">モニタリング</a>](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページ内を簡単に移動し、より直感的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは、UX に関する多くの問題も解決し、監視プロセスをより使いやすくしています。

## 2023 年 4 月 18 日 {#april-18-2023}

**一般的な変更点**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターに対して[<a href="/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration">データ移行ジョブの仕様</a>](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)スケールアップまたはスケールダウンをサポートします。

    この機能を使用すると、仕様をスケールアップして移行パフォーマンスを向上させたり、仕様をスケールダウンしてコストを削減したりできます。

    詳細については、 [<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification">データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)を参照してください。

**コンソールの変更**

-   UI を刷新して[<a href="https://tidbcloud.com/console/clusters/create-cluster">クラスターの作成</a>](https://tidbcloud.com/console/clusters/create-cluster)エクスペリエンスをさらに使いやすくし、数回クリックするだけでクラスターを作成および構成できるようにしました。

    新しいデザインはシンプルさを重視し、視覚的な煩雑さを軽減し、明確な指示を提供します。クラスター作成ページで**「作成」**をクリックすると、クラスターの作成が完了するまで待つことなく、クラスターの概要ページに移動します。

    詳細については、 [<a href="/tidb-cloud/create-tidb-cluster.md">クラスターを作成する</a>](/tidb-cloud/create-tidb-cluster.md)を参照してください。

-   **[請求**] ページに**[割引]**タブを導入して、組織の所有者と請求管理者向けの割引情報を表示します。

    詳細については、 [<a href="/tidb-cloud/tidb-cloud-billing.md#discounts">割引</a>](/tidb-cloud/tidb-cloud-billing.md#discounts)を参照してください。

## 2023 年 4 月 11 日 {#april-11-2023}

**一般的な変更点**

-   TiDB のロード バランスを改善し、AWS でホストされている[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの TiDB ノードをスケールする際の接続ドロップを削減します。

    -   TiDB ノードをスケールアウトするときに、既存の接続を新しい TiDB ノードに自動的に移行することをサポートします。
    -   TiDB ノードをスケールインするときに、既存の接続を利用可能な TiDB ノードに自動的に移行することをサポートします。

    現在、この機能は、AWS `Oregon (us-west-2)`リージョンでホストされているDedicated Tierクラスターに対してのみ提供されています。

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターに対して[<a href="https://newrelic.com/">ニューレリック</a>](https://newrelic.com/)統合をサポートします。

    New Relic の統合を使用すると、TiDB クラスターのメトリクス データを[<a href="https://newrelic.com/">ニューレリック</a>](https://newrelic.com/)に送信するようにTiDB Cloudを構成できます。その後、アプリケーションのパフォーマンスと TiDB データベースのパフォーマンスの両方を[<a href="https://newrelic.com/">ニューレリック</a>](https://newrelic.com/)で監視および分析できます。この機能は、潜在的な問題を迅速に特定してトラブルシューティングし、解決時間を短縮するのに役立ちます。

    統合手順と利用可能なメトリクスについては、 [<a href="/tidb-cloud/monitor-new-relic-integration.md">TiDB Cloudと New Relic を統合する</a>](/tidb-cloud/monitor-new-relic-integration.md)を参照してください。

-   次の[<a href="/tidb-cloud/changefeed-overview.md">チェンジフィード</a>](/tidb-cloud/changefeed-overview.md)メトリクスを、Dedicated Tierクラスターの Prometheus 統合に追加します。

    -   `tidbcloud_changefeed_latency`
    -   `tidbcloud_changefeed_replica_rows`

    [<a href="/tidb-cloud/monitor-prometheus-and-grafana-integration.md">TiDB Cloudと Prometheus を統合</a>](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)がある場合は、これらのメトリクスを使用して、変更フィードのパフォーマンスと健全性をリアルタイムで監視できます。さらに、Prometheus を使用してメトリクスを監視するアラートを簡単に作成できます。

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの[<a href="/tidb-cloud/built-in-monitoring.md#view-the-metrics-page">モニタリング</a>](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページを[<a href="/tidb-cloud/built-in-monitoring.md#server">ノードレベルのリソースメトリック</a>](/tidb-cloud/built-in-monitoring.md#server)を使用するように更新します。

    ノードレベルのリソースメトリクスを使用すると、リソース消費をより正確に表示して、購入したサービスの実際の使用状況をより深く理解できます。

    これらのメトリックにアクセスするには、クラスターの[<a href="/tidb-cloud/built-in-monitoring.md#view-the-metrics-page">モニタリング</a>](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)ページに移動し、 **[メトリック]**タブの [**サーバー]**カテゴリを確認します。

-   **「プロジェクト別集計」**と**「サービス別集計」**の請求項目を再整理し、請求内容をよりわかりやすく[<a href="/tidb-cloud/tidb-cloud-billing.md#billing-details">請求する</a>](/tidb-cloud/tidb-cloud-billing.md#billing-details)ページを最適化しました。

## 2023 年 4 月 4 日 {#april-4-2023}

**一般的な変更点**

-   誤検知を防ぐために、次の 2 つのアラートを[<a href="/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions">TiDB Cloudの組み込みアラート</a>](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions)から削除します。これは、ノードの 1 つで一時的にオフラインまたはメモリ不足 (OOM) の問題が発生しても、クラスター全体の健全性には大きな影響を与えないためです。

    -   クラスター内の少なくとも 1 つの TiDB ノードでメモリが不足しました。
    -   1 つ以上のクラスター ノードがオフラインです。

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの[<a href="/tidb-cloud/monitor-built-in-alerting.md">アラート</a>](/tidb-cloud/monitor-built-in-alerting.md)ページを導入します。このページには、各Dedicated Tierクラスターのアクティブなアラートとクローズされたアラートの両方がリストされます。

    **[アラート]**ページには次の内容が表示されます。

    -   直感的でユーザーフレンドリーなユーザーインターフェイス。アラート通知メールを購読していない場合でも、このページでクラスターのアラートを表示できます。
    -   高度なフィルタリング オプションにより、重大度、ステータス、その他の属性に基づいてアラートを迅速に検索して並べ替えることができます。また、過去 7 日間の履歴データを表示できるため、アラート履歴の追跡が容易になります。
    -   **ルールの編集**機能。クラスター固有のニーズに合わせてアラート ルール設定をカスタマイズできます。

    詳細については、 [<a href="/tidb-cloud/monitor-built-in-alerting.md">TiDB Cloudの組み込みアラート</a>](/tidb-cloud/monitor-built-in-alerting.md)を参照してください。

-   TiDB Cloudのヘルプ関連の情報とアクションを 1 か所に統合します。

    これで、 [<a href="/tidb-cloud/tidb-cloud-support.md#get-help-information">TiDB Cloudのヘルプ情報</a>](/tidb-cloud/tidb-cloud-support.md#get-help-information)すべて取得し、 **「?」**をクリックしてサポートに問い合わせることができます。 [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)の右下隅にあります。

-   TiDB Cloudについて学ぶのに役立つ[<a href="https://tidbcloud.com/console/getting-started">入門</a>](https://tidbcloud.com/console/getting-started)ページを紹介します。

    **「はじめに」**ページでは、インタラクティブなチュートリアル、重要なガイド、便利なリンクが提供されます。インタラクティブなチュートリアルに従うことで、事前に構築された業界固有のデータセット (Steam ゲーム データセットおよび S&amp;P 500 データセット) を使用してTiDB Cloud機能と HTAP 機能を簡単に探索できます。

    **「はじめに」**ページにアクセスするには、 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)の左側のナビゲーション バーにある**「はじめに**」。このページでは、 **「クエリ サンプル データセット」**をクリックして対話型チュートリアルを開いたり、他のリンクをクリックしてTiDB Cloudを探索したりできます。または、 **「?」**をクリックすることもできます。右下隅の をクリックし、 **「対話型チュートリアル」**をクリックします。

## 2023 年 3 月 29 日 {#march-29-2023}

**一般的な変更点**

-   [<a href="/tidb-cloud/data-service-overview.md">データサービス（ベータ版）</a>](/tidb-cloud/data-service-overview.md)データ アプリのより詳細なアクセス制御をサポートします。

    データ アプリの詳細ページで、クラスターをデータ アプリにリンクし、各 API キーのロールを指定できるようになりました。このロールは、API キーがリンクされたクラスターに対してデータの読み取りまたは書き込みができるかどうかを制御し、 `ReadOnly`または`ReadAndWrite`に設定できます。この機能は、データ アプリに対してクラスター レベルおよびアクセス許可レベルのアクセス制御を提供し、ビジネス ニーズに応じてアクセス スコープをより柔軟に制御できるようにします。

    詳細については、 [<a href="/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources">リンクされたクラスターを管理する</a>](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)および[<a href="/tidb-cloud/data-service-api-key.md">APIキーを管理する</a>](/tidb-cloud/data-service-api-key.md)を参照してください。

## 2023 年 3 月 28 日 {#march-28-2023}

**一般的な変更点**

-   [<a href="/tidb-cloud/changefeed-overview.md">変更フィード</a>](/tidb-cloud/changefeed-overview.md)に 2 RCU、4 RCU、8 RCU の仕様を追加し、 [<a href="/tidb-cloud/changefeed-overview.md#create-a-changefeed">変更フィードを作成する</a>](/tidb-cloud/changefeed-overview.md#create-a-changefeed)場合に希望の仕様の選択をサポートします。

    これらの新しい仕様を使用すると、以前は 16 個の RCU が必要だったシナリオと比較して、データ レプリケーション コストを最大 87.5% 削減できます。

-   2023 年 3 月 28 日以降に作成された[<a href="/tidb-cloud/changefeed-overview.md">変更フィード</a>](/tidb-cloud/changefeed-overview.md)仕様のスケールアップまたはスケールダウンをサポートします。

    より高い仕様を選択することでレプリケーションのパフォーマンスを向上させることができ、より低い仕様を選択することでレプリケーションのコストを削減することができます。

    詳細については、 [<a href="/tidb-cloud/changefeed-overview.md#scale-a-changefeed">チェンジフィードをスケールする</a>](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)を参照してください。

-   AWS の[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターから同じプロジェクトおよび同じリージョンの[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターへの増分データのリアルタイムのレプリケートをサポートします。

    詳細については、 [<a href="/tidb-cloud/changefeed-sink-to-tidb-cloud.md">TiDB Cloudへのシンク</a>](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)を参照してください。

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスタの[<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md">データ移行</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md)の機能に対して 2 つの新しい GCP リージョン ( `Singapore (asia-southeast1)`と`Oregon (us-west1)`をサポートします。

    これらの新しいリージョンを使用すると、データをTiDB Cloudに移行するためのオプションが増えます。アップストリーム データがこれらのリージョンまたはその近くに保存されている場合は、GCP からTiDB Cloudへのより高速で信頼性の高いデータ移行を利用できるようになります。

    詳細については、 [<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md">データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターの[<a href="/tidb-cloud/tune-performance.md#slow-query">遅いクエリ</a>](/tidb-cloud/tune-performance.md#slow-query)ページ用の新しいネイティブ Web インフラストラクチャをリリースします。

    この新しいインフラストラクチャを使用すると、 [<a href="/tidb-cloud/tune-performance.md#slow-query">遅いクエリ</a>](/tidb-cloud/tune-performance.md#slow-query)ページ内を簡単に移動し、より直観的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは UX に関する多くの問題も解決し、SQL 診断プロセスをより使いやすくしています。

## 2023 年 3 月 21 日 {#march-21-2023}

**一般的な変更点**

-   [<a href="https://tidbcloud.com/console/data-service">データサービス（ベータ版）</a>](https://tidbcloud.com/console/data-service)クラスターを導入すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でデータ[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)アクセスできるようになります。

    Data Service を使用すると、 TiDB Cloud をHTTPS と互換性のあるアプリケーションまたはサービスとシームレスに統合できます。以下に、一般的なシナリオをいくつか示します。

    -   モバイルまたは Web アプリケーションから TiDB クラスターのデータベースに直接アクセスします。
    -   サーバーレス エッジ関数を使用してエンドポイントを呼び出し、データベース接続プーリングによって引き起こされるスケーラビリティの問題を回避します。
    -   Data Service をデータ ソースとして使用して、 TiDB Cloudをデータ視覚化プロジェクトと統合します。
    -   MySQL インターフェースがサポートしていない環境からデータベースに接続します。

    さらに、 TiDB Cloud は、AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェイス[<a href="/tidb-cloud/use-chat2query-api.md">Chat2Query API</a>](/tidb-cloud/use-chat2query-api.md)を提供します。

    Data Service にアクセスするには、左側のナビゲーション ペインの[<a href="https://tidbcloud.com/console/data-service">**データサービス**</a>](https://tidbcloud.com/console/data-service)ページに移動します。詳細については、次のドキュメントを参照してください。

    -   [<a href="/tidb-cloud/data-service-overview.md">データサービスの概要</a>](/tidb-cloud/data-service-overview.md)
    -   [<a href="/tidb-cloud/data-service-get-started.md">データサービスを始めてみる</a>](/tidb-cloud/data-service-get-started.md)
    -   [<a href="/tidb-cloud/use-chat2query-api.md">Chat2Query API を使ってみる</a>](/tidb-cloud/use-chat2query-api.md)

-   AWS でホストされ、2022 年 12 月 31 日以降に作成された[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)のクラスターにスケールインするために、TiDB、TiKV、およびTiFlashノードのサイズを縮小することをサポートします。

    ノード サイズを[<a href="/tidb-cloud/scale-tidb-cluster.md#change-node-size">TiDB Cloudコンソール経由</a>](/tidb-cloud/scale-tidb-cluster.md#change-node-size)または[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">TiDB CloudAPI (ベータ版) 経由</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)減らすことができます。

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)のクラスタの[<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md">データ移行</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能に対して新しい GCP リージョンをサポートします: `Tokyo (asia-northeast1)` 。

    この機能は、Google Cloud Platform (GCP) の MySQL 互換データベースから TiDB クラスターにデータを簡単かつ効率的に移行するのに役立ちます。

    詳細については、 [<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md">データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの**「イベント」**ページを導入します。このページには、クラスターに対する主な変更の記録が表示されます。

    このページでは、過去 7 日間のイベント履歴を表示し、トリガー時間やアクションを開始したユーザーなどの重要な詳細を追跡できます。たとえば、クラスターがいつ一時停止されたか、誰がクラスター サイズを変更したかなどのイベントを表示できます。

    詳細については、 [<a href="/tidb-cloud/tidb-cloud-events.md">TiDB Cloudクラスター イベント</a>](/tidb-cloud/tidb-cloud-events.md)を参照してください。

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターの**[監視]**ページに**[データベース ステータス]**タブを追加します。これには、次のデータベース レベルのメトリックが表示されます。

    -   DBごとのQPS
    -   DBごとの平均クエリ継続時間
    -   DBごとの失敗したクエリ数

    これらのメトリクスを使用すると、個々のデータベースのパフォーマンスを監視し、データに基づいて意思決定を行い、アプリケーションのパフォーマンスを向上させるためのアクションを実行できます。

    詳細については、 [<a href="/tidb-cloud/built-in-monitoring.md">Serverless Tierクラスターのモニタリングメトリクス</a>](/tidb-cloud/built-in-monitoring.md)を参照してください。

## 2023 年 3 月 14 日 {#march-14-2023}

**一般的な変更点**

-   新しい[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[<a href="https://docs.pingcap.com/tidb/v6.5/release-6.5.0">v6.5.0</a>](https://docs.pingcap.com/tidb/v6.5/release-6.5.0)から[<a href="https://docs.pingcap.com/tidb/v6.5/release-6.5.1">v6.5.1</a>](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)にアップグレードします。

-   ヘッダー行を含むローカル CSV ファイルをアップロードするときに、 TiDB Cloudによって作成されるターゲット テーブルの列名の変更をサポートします。

    ヘッダー行を含むローカル CSV ファイルを[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターにインポートするときに、ターゲット テーブルの作成にTiDB Cloudが必要で、ヘッダー行の列名がTiDB Cloud列の命名規則に従っていない場合は、次に警告アイコンが表示されます。対応する列名に。この警告を解決するには、アイコンの上にカーソルを移動し、メッセージに従って既存の列名を編集するか、新しい列名を入力します。

    列の命名規則については、 [<a href="/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files">ローカルファイルをインポートする</a>](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)を参照してください。

## 2023 年 3 月 7 日 {#march-7-2023}

**一般的な変更点**

-   すべての[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターのデフォルトの TiDB バージョンを[<a href="https://docs.pingcap.com/tidb/v6.4/release-6.4.0">v6.4.0</a>](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)から[<a href="https://docs.pingcap.com/tidb/v6.6/release-6.6.0">v6.6.0</a>](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)にアップグレードします。

## 2023 年 2 月 28 日 {#february-28-2023}

**一般的な変更点**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターに[<a href="/tidb-cloud/tune-performance.md">SQL診断</a>](/tidb-cloud/tune-performance.md)機能を追加します。

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

    詳細については、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import">APIドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import)を参照してください。

## 2023 年 2 月 22 日 {#february-22-2023}

**一般的な変更点**

-   [<a href="/tidb-cloud/tidb-cloud-console-auditing.md">コンソール監査ログ</a>](/tidb-cloud/tidb-cloud-console-auditing.md)機能を使用して、組織内のメンバーが実行するさまざまなアクティビティを追跡することをサポートします。 [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/) .

    コンソール監査ログ機能は、ロール`Owner`または`Audit Admin`を持つユーザーのみに表示され、デフォルトでは無効になっています。有効にするには、<mdsvgicon name="icon-top-organization"> [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)の右上隅にある**[組織]** &gt; **[コンソール監査ログ]** 。</mdsvgicon>

    コンソール監査ログを分析すると、組織内で実行された不審な操作を特定できるため、組織のリソースとデータのセキュリティが向上します。

    詳細については、 [<a href="/tidb-cloud/tidb-cloud-console-auditing.md">コンソール監査ログ</a>](/tidb-cloud/tidb-cloud-console-auditing.md)を参照してください。

**CLIの変更**

-   新しいコマンド[<a href="/tidb-cloud/ticloud-cluster-connect-info.md">`ticloud cluster connect-info`</a>](/tidb-cloud/ticloud-cluster-connect-info.md) for [<a href="/tidb-cloud/cli-reference.md">TiDB CloudCLI</a>](/tidb-cloud/cli-reference.md)を追加します。

    `ticloud cluster connect-info`は、クラスターの接続文字列を取得できるコマンドです。このコマンドを使用するには、 [<a href="/tidb-cloud/ticloud-update.md">`ticloud`を更新する</a>](/tidb-cloud/ticloud-update.md) ～ v0.3.2 以降のバージョンが必要です。

## 2023 年 2 月 21 日 {#february-21-2023}

**一般的な変更点**

-   データをTiDB Cloudにインポートするときに、 IAMユーザーの AWS アクセス キーを使用して Amazon S3 バケットにアクセスすることをサポートします。

    この方法は、ロール ARN を使用するよりも簡単です。詳細については、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access">Amazon S3 アクセスを構成する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

-   [<a href="/tidb-cloud/built-in-monitoring.md#metrics-retention-policy">モニタリングメトリクスの保持期間</a>](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 2 日間からさらに長い期間に延長します。

    -   Dedicated Tierクラスターの場合、過去 7 日間のメトリック データを表示できます。
    -   Serverless Tierクラスターの場合、過去 3 日間のメトリック データを表示できます。

    メトリクスの保持期間を延長することで、より多くの履歴データにアクセスできるようになりました。これは、クラスターの傾向とパターンを特定して、より適切な意思決定と迅速なトラブルシューティングを行うのに役立ちます。

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターの [監視] ページで新しいネイティブ Web インフラストラクチャをリリースします。

    新しいインフラストラクチャを使用すると、[監視] ページを簡単に移動して、より直観的かつ効率的な方法で必要な情報にアクセスできます。新しいインフラストラクチャは UX に関する多くの問題も解決し、監視プロセスをより使いやすくしています。

## 2023 年 2 月 17 日 {#february-17-2023}

**CLIの変更**

-   新しいコマンド[<a href="/tidb-cloud/ticloud-connect.md">`ticloud connect`</a>](/tidb-cloud/ticloud-connect.md) for [<a href="/tidb-cloud/cli-reference.md">TiDB CloudCLI</a>](/tidb-cloud/cli-reference.md)を追加します。

    `ticloud connect`は、SQL クライアントをインストールせずにローカル マシンからTiDB Cloudクラスターに接続できるようにするコマンドです。 TiDB Cloudクラスターに接続した後、 TiDB Cloud CLI で SQL ステートメントを実行できます。

## 2023 年 2 月 14 日 {#february-14-2023}

**一般的な変更点**

-   TiDB [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスター内でスケールするために TiKV およびTiFlashノードの数を減らすことをサポートします。

    ノード番号[<a href="/tidb-cloud/scale-tidb-cluster.md#change-node-number">TiDB Cloudコンソール経由</a>](/tidb-cloud/scale-tidb-cluster.md#change-node-number)または[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">TiDB CloudAPI (ベータ版) 経由</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)を減らすことができます。

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)のクラスターの**モニタリング**ページを紹介します。

    [**モニタリング]**ページには、1 秒あたりに実行された SQL ステートメントの数、クエリの平均継続時間、失敗したクエリの数など、さまざまなメトリックとデータが表示されます。これは、Serverless Tierにおける SQL ステートメントの全体的なパフォーマンスをより深く理解するのに役立ちます。集まる。

    詳細については、 [<a href="/tidb-cloud/built-in-monitoring.md">TiDB Cloudの組み込みモニタリング</a>](/tidb-cloud/built-in-monitoring.md)を参照してください。

## 2023 年 2 月 2 日 {#february-2-2023}

**CLIの変更**

-   TiDB Cloud CLI クライアントの紹介[<a href="/tidb-cloud/cli-reference.md">`ticloud`</a>](/tidb-cloud/cli-reference.md) 。

    `ticloud`を使用すると、数行のコマンドでターミナルまたはその他の自動ワークフローからTiDB Cloudリソースを簡単に管理できます。特に GitHub Actions については、 `ticloud`簡単にセットアップできるように[<a href="https://github.com/marketplace/actions/set-up-tidbcloud-cli">`setup-tidbcloud-cli`</a>](https://github.com/marketplace/actions/set-up-tidbcloud-cli)用意しました。

    詳細については、 [<a href="/tidb-cloud/get-started-with-cli.md">TiDB CloudCLI クイック スタート</a>](/tidb-cloud/get-started-with-cli.md)および[<a href="/tidb-cloud/cli-reference.md">TiDB CloudCLI リファレンス</a>](/tidb-cloud/cli-reference.md)を参照してください。

## 2023 年 1 月 18 日 {#january-18-2023}

**一般的な変更点**

-   Microsoft アカウントで[<a href="https://tidbcloud.com/free-trial">サインアップ</a>](https://tidbcloud.com/free-trial) TiDB Cloudをサポートします。

## 2023 年 1 月 17 日 {#january-17-2023}

**一般的な変更点**

-   新しい[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[<a href="https://docs.pingcap.com/tidb/stable/release-6.1.3">v6.1.3</a>](https://docs.pingcap.com/tidb/stable/release-6.1.3)から[<a href="https://docs.pingcap.com/tidb/stable/release-6.5.0">v6.5.0</a>](https://docs.pingcap.com/tidb/stable/release-6.5.0)にアップグレードします。

-   新規サインアップ ユーザーの場合、 TiDB Cloud は無料の[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターを自動的に作成するため、 TiDB Cloudを使用したデータ探索の旅をすぐに開始できます。

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの新しい AWS リージョンをサポートします: `Seoul (ap-northeast-2)` 。

    このリージョンでは次の機能が有効になっています。

    -   [<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md">データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    -   [<a href="/tidb-cloud/changefeed-overview.md">チェンジフィードを使用してTiDB Cloudから他のデータ サービスにデータをストリーミングする</a>](/tidb-cloud/changefeed-overview.md)
    -   [<a href="/tidb-cloud/backup-and-restore.md">TiDB クラスターデータのバックアップと復元</a>](/tidb-cloud/backup-and-restore.md)

## 2023 年 1 月 10 日 {#january-10-2023}

**一般的な変更点**

-   ローカル CSV ファイルから TiDB にデータをインポートする機能を最適化し、 [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターのユーザー エクスペリエンスを向上させます。

    -   CSV ファイルをアップロードするには、**インポート**ページのアップロード領域にドラッグ アンド ドロップするだけで済みます。
    -   インポート タスクを作成するときに、ターゲット データベースまたはテーブルが存在しない場合は、名前を入力すると、 TiDB Cloudによって自動的に作成されます。作成するターゲット テーブルでは、主キーを指定するか、複数のフィールドを選択して複合主キーを形成できます。
    -   インポートが完了したら、 **「Chat2Query でデータを探索」**をクリックするか、タスク リストでターゲット テーブル名をクリックすると、 [<a href="/tidb-cloud/explore-data-with-chat2query.md">AI を活用した Chat2Query</a>](/tidb-cloud/explore-data-with-chat2query.md)でデータを探索できます。

    詳細については、 [<a href="/tidb-cloud/tidb-cloud-import-local-files.md">ローカル ファイルをTiDB Cloudにインポートする</a>](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

**コンソールの変更**

-   各クラスターに**[Get Support]**オプションを追加して、特定のクラスターのサポートをリクエストするプロセスを簡素化します。

    次のいずれかの方法でクラスターのサポートをリクエストできます。

    -   プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページで、クラスターの行にある**[...]**をクリックし、 **[Get Support]**を選択します。
    -   クラスターの概要ページで、右上隅にある**[...]**をクリックし、 **[サポートを受ける]**を選択します。

## 2023 年 1 月 5 日 {#january-5-2023}

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターの SQL Editor (ベータ) の名前を Chat2Query (ベータ) に変更し、AI を使用した SQL クエリの生成をサポートします。

    Chat2Query では、AI に SQL クエリを自動的に生成させることも、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することもできます。

    Chat2Query にアクセスするには、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動し、クラスター名をクリックして、左側のナビゲーション ウィンドウで**[Chat2Query]**をクリックします。

## 2023 年 1 月 4 日 {#january-4-2023}

**一般的な変更点**

-   AWS でホストされ、2022 年 12 月 31 日以降に作成された TiDB 専用クラスターの**ノード サイズ (vCPU + RAM)**を増やすことで、TiDB、TiKV、およびTiFlashノードのスケールアップをサポートします。

    ノード サイズを[<a href="/tidb-cloud/scale-tidb-cluster.md#change-node-size">TiDB Cloudコンソールの使用</a>](/tidb-cloud/scale-tidb-cluster.md#change-node-size)または[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">TiDB CloudAPI (ベータ版) を使用する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)に増やすことができます。

-   [<a href="/tidb-cloud/built-in-monitoring.md">**モニタリング**</a>](/tidb-cloud/built-in-monitoring.md)ページのメトリクスの保持期間を 2 日に延長します。

    過去 2 日間のメトリクス データにアクセスできるようになり、クラスターのパフォーマンスと傾向をより柔軟に把握できるようになりました。

    この改善には追加コストはかからず、クラスターの[<a href="/tidb-cloud/built-in-monitoring.md">**モニタリング**</a>](/tidb-cloud/built-in-monitoring.md)ページの**[診断]**タブからアクセスできます。これは、パフォーマンスの問題を特定してトラブルシューティングし、クラスター全体の状態をより効果的に監視するのに役立ちます。

-   Prometheus 統合のための Grafana ダッシュボード JSON のカスタマイズをサポートします。

    [<a href="/tidb-cloud/monitor-prometheus-and-grafana-integration.md">TiDB Cloudと Prometheus を統合</a>](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)お持ちの場合は、事前に構築された Grafana ダッシュボードをインポートしてTiDB Cloudクラスターを監視し、ニーズに合わせてダッシュボードをカスタマイズできるようになりました。この機能により、 TiDB Cloudクラスターの簡単かつ迅速なモニタリングが可能になり、パフォーマンスの問題を迅速に特定するのに役立ちます。

    詳細については、 [<a href="/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics">Grafana GUI ダッシュボードを使用してメトリクスを視覚化する</a>](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)を参照してください。

-   すべての[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターのデフォルトの TiDB バージョンを[<a href="https://docs.pingcap.com/tidb/v6.3/release-6.3.0">v6.3.0</a>](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[<a href="https://docs.pingcap.com/tidb/v6.4/release-6.4.0">v6.4.0</a>](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。Serverless Tierクラスターのデフォルトの TiDB バージョンを v6.4.0 にアップグレードした後のコールド スタートの問題は解決されました。

**コンソールの変更**

-   [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページとクラスター概要ページの表示を簡素化します。

    -   [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページのクラスター名をクリックすると、クラスターの概要ページに移動し、クラスターの操作を開始できます。
    -   クラスターの概要ページから**[接続] ペイン**と**[インポート]**ペインを削除します。右上隅の**「接続」**をクリックして接続情報を取得し、左側のナビゲーション・ペインで**「インポート」**をクリックしてデータをインポートできます。
