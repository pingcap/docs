---
title: TiDB Cloud FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud.
---

# TiDB Cloudよくある質問 {#tidb-cloud-faqs}

このドキュメントには、 TiDB Cloudに関してよくある質問がリストされています。

## 一般的な FAQ {#general-faqs}

### TiDB Cloudとは何ですか? {#what-is-tidb-cloud}

TiDB Cloud、直感的なコンソールを通じて制御できるフルマネージドのクラウド インスタンスにより、TiDB クラスターのデプロイ、管理、保守がさらに簡単になります。アマゾン ウェブ サービスや Google Cloud に簡単にデプロイして、ミッションクリティカルなアプリケーションを迅速に構築できます。

TiDB Cloud を使用すると、ほとんどまたはまったくトレーニングを受けていない開発者や DBA が、インフラストラクチャ管理やクラスター展開など、かつては複雑だったタスクを簡単に処理できるようになり、データベースの複雑さではなくアプリケーションに集中できるようになります。また、ボタンをクリックするだけで TiDB クラスターをスケールインまたはスケールアウトすることで、必要な量と期間を正確にデータベースをプロビジョニングできるため、高価なリソースを無駄にすることがなくなります。

### TiDB とTiDB Cloudの関係は何ですか? {#what-is-the-relationship-between-tidb-and-tidb-cloud}

TiDB はオープンソース データベースであり、TiDB セルフホスト型を自社のデータ センター、自己管理型のクラウド環境、またはその 2 つのハイブリッドで実行したい組織にとって最適なオプションです。

TiDB Cloud は、TiDB のサービスとしてのフルマネージド クラウド データベースです。使いやすい Web ベースの管理コンソールを備えており、ミッションクリティカルな本番環境の TiDB クラスターを管理できます。

### TiDB Cloud はMySQL と互換性がありますか? {#is-tidb-cloud-compatible-with-mysql}

現在、 TiDB Cloud は、トリガー、ストアド プロシージャ、ユーザー定義関数、および外部キーを除く、 MySQL 5.7構文の大部分をサポートしています。詳細については、 [MySQLとの互換性](https://docs.pingcap.com/tidb/stable/mysql-compatibility)を参照してください。

### TiDB Cloudを操作するにはどのようなプログラミング言語を使用できますか? {#what-programming-languages-can-i-use-to-work-with-tidb-cloud}

MySQL クライアントまたはドライバーでサポートされている任意の言語を使用できます。

### TiDB Cloud はどこで実行できますか? {#where-can-i-run-tidb-cloud}

TiDB Cloudは現在、アマゾン ウェブ サービスと Google Cloud で利用できます。

### TiDB Cloud は、異なるクラウド サービス プロバイダー間の VPC ピアリングをサポートしていますか? {#does-tidb-cloud-support-vpc-peering-between-different-cloud-service-providers}

いいえ。

### TiDB Cloudではどのバージョンの TiDB がサポートされていますか? {#what-versions-of-tidb-are-supported-on-tidb-cloud}

-   2023 年 7 月 25 日以降、新しい TiDB 専用クラスターのデフォルトの TiDB バージョンは v7.1.1 になります。
-   2023 年 3 月 7 日以降、新しい TiDB サーバーレス クラスターのデフォルトの TiDB バージョンは v6.6.0 になります。

詳細については、 [TiDB Cloudリリースノート](/tidb-cloud/tidb-cloud-release-notes.md)を参照してください。

### TiDB またはTiDB Cloud を本番で使用しているのはどの企業ですか? {#what-companies-are-using-tidb-or-tidb-cloud-in-production}

TiDB は、金融サービス、ゲーム、電子商取引など、さまざまな業界の 1,500 社を超えるグローバル企業から信頼されています。当社のユーザーには、Square (米国)、Shopee (シンガポール)、および China UnionPay (中国) が含まれます。具体的な詳細については[ケーススタディ](https://en.pingcap.com/customers/)参照してください。

### SLA はどのようなものですか? {#what-does-the-sla-look-like}

TiDB Cloudは99.99% の SLA を提供します。詳細は[TiDB Cloudサービスのサービス レベル契約](https://en.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)を参照してください。

### TiDB Cloudについてさらに詳しく知るにはどうすればよいですか? {#how-can-i-learn-more-about-tidb-cloud}

TiDB Cloudについて学ぶ最良の方法は、ステップバイステップのチュートリアルに従うことです。開始するには、次のトピックを確認してください。

-   [TiDB Cloudの紹介](/tidb-cloud/tidb-cloud-intro.md)
-   [始めましょう](/tidb-cloud/tidb-cloud-quickstart.md)
-   [TiDB サーバーレスクラスタの作成](/tidb-cloud/create-tidb-cluster-serverless.md)

### クラスターを削除する場合、 <code>XXX&#39;s Org/default project/Cluster0</code>は何を参照しますか? {#what-does-code-xxx-s-org-default-project-cluster0-code-refer-to-when-deleting-a-cluster}

TiDB Cloudでは、クラスターは組織名、プロジェクト名、クラスター名の組み合わせによって一意に識別されます。目的のクラスターを確実に削除するには、そのクラスターの完全修飾名 ( `XXX's Org/default project/Cluster0`など) を指定する必要があります。

## アーキテクチャに関するよくある質問 {#architecture-faqs}

### 私の TiDB クラスターにはさまざまなコンポーネントがあります。 TiDB、TiKV、 TiFlashノードとは何ですか? {#there-are-different-components-in-my-tidb-cluster-what-are-tidb-tikv-and-tiflash-nodes}

TiDB は、TiKV またはTiFlashストアから返されたクエリからのデータを集約する SQL コンピューティングレイヤーです。 TiDB は水平方向にスケーラブルです。 TiDB ノードの数を増やすと、クラスターが処理できる同時クエリの数が増加します。

TiKV は、OLTP データを保存するために使用されるトランザクション ストアです。 TiKV 内のすべてのデータは複数のレプリカ (デフォルトでは 3 つのレプリカ) で自動的に維持されるため、TiKV はネイティブの高可用性を備え、自動フェイルオーバーをサポートします。 TiKV は水平方向にスケーラブルです。トランザクション ストアの数を増やすと、OLTP スループットが向上します。

TiFlashは、トランザクション ストア (TiKV) からデータをリアルタイムでレプリケートし、リアルタイム OLAP ワークロードをサポートする分析storageです。 TiKV とは異なり、 TiFlash は分析処理を高速化するためにデータを列に保存します。 TiFlash は水平方向にも拡張可能です。 TiFlashノードを増やすと、OLAPstorageとコンピューティング容量が増加します。

PD、Placement Driver は、クラスターのメタデータを保存するため、TiDB クラスター全体の「頭脳」です。 TiKV ノードからリアルタイムで報告されるデータ分散状態に従って、データ スケジューリング コマンドを特定の TiKV ノードに送信します。 TiDB Cloudでは、各クラスターの PD は PingCAP によって管理されており、確認したり保守したりすることはできません。

### TiDB は TiKV ノード間でデータをどのように複製しますか? {#how-does-tidb-replicate-data-between-the-tikv-nodes}

TiKV は、キーと値の空間をキー範囲に分割し、各キー範囲は「リージョン」として扱われます。 TiKV では、データはクラスター内のすべてのノードに分散され、リージョンを基本単位として使用します。 PD は、クラスター内のすべてのノードにできるだけ均等にリージョンを分散 (スケジューリング) する責任があります。

TiDB は、 Raftコンセンサス アルゴリズムを使用して、リージョンごとにデータを複製します。異なるノードに保存されているリージョンの複数のレプリカがRaftグループを形成します。

各データ変更はRaftログとして記録されます。 Raftログ レプリケーションを通じて、データはRaftグループの複数のノードに安全かつ確実にレプリケートされます。

## 高可用性に関するFAQ {#high-availability-faq}

### TiDB Cloudはどのようにして高可用性を確保しますか? {#how-does-tidb-cloud-ensure-high-availability}

TiDB は、 Raftコンセンサス アルゴリズムを使用して、データの可用性が高く、 Raftグループ内のstorage全体に安全に複製されることを保証します。データは TiKV ノード間で冗長的にコピーされ、異なるアベイラビリティーゾーンに配置されて、マシンまたはデータセンターの障害から保護されます。 TiDB は自動フェイルオーバーにより、サービスが常に稼働していることを保証します。

Software as a Service (SaaS) プロバイダーとして、当社はデータのセキュリティを真剣に考えています。当社は、 [Service Organization Control (SOC) 2 タイプ 1 準拠](https://en.pingcap.com/press-release/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud/)に要求される厳格な情報セキュリティポリシーと手順を確立しています。これにより、データの安全性、可用性、機密性が確保されます。

## 移行に関するFAQ {#migration-faq}

### 別の RDBMS からTiDB Cloudへの簡単な移行パスはありますか? {#is-there-an-easy-migration-path-from-another-rdbms-to-tidb-cloud}

TiDB は MySQL と高い互換性があります。データがセルフホスト型 MySQL インスタンスからのものであっても、パブリック クラウドによって提供される RDS サービスからのものであっても、MySQL 互換データベースから TiDB にスムーズにデータを移行できます。詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

## バックアップと復元に関するFAQ {#backup-and-restore-faq}

### TiDB Cloud は増分バックアップをサポートしていますか? {#does-tidb-cloud-support-incremental-backups}

いいえ。クラスターのバックアップ保持期間内の任意の時点にデータを復元する必要がある場合は、PITR (Point-in-time Recovery) を使用できます。詳細については、 [TiDB 専用クラスターで PITR を使用する](/tidb-cloud/backup-and-restore.md#automatic-backup)または[TiDB サーバーレスクラスターで PITR を使用する](/tidb-cloud/backup-and-restore-serverless.md#restore)を参照してください。

## HTAPに関するよくある質問 {#htap-faqs}

### TiDB Cloud の HTAP 機能を利用するにはどうすればよいですか? {#how-do-i-make-use-of-tidb-cloud-s-htap-capabilities}

従来、データベースには、オンライン トランザクション処理 (OLTP) データベースとオンライン分析処理 (OLAP) データベースの 2 種類があります。 OLTP リクエストと OLAP リクエストは、多くの場合、異なる分離されたデータベースで処理されます。この従来のアーキテクチャでは、OLTP データベースから OLAP のデータ ウェアハウスまたはデータ レイクへのデータの移行は、時間がかかり、エラーが発生しやすいプロセスになります。

ハイブリッド トランザクション分析処理 (HTAP) データベースとして、 TiDB Cloudは、OLTP (TiKV) ストアと OLAP ( TiFlash ) の間でデータを確実に自動的に複製することにより、システムアーキテクチャを簡素化し、メンテナンスの複雑さを軽減し、トランザクション データのリアルタイム分析をサポートします。店。典型的な HTAP の使用例には、ユーザーのパーソナライゼーション、AI 推奨、不正検出、ビジネス インテリジェンス、リアルタイム レポートなどがあります。

HTAP シナリオの詳細については、 [データ プラットフォームを簡素化する HTAP データベースの構築方法](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)を参照してください。

### データをTiFlashに直接インポートできますか? {#can-i-import-my-data-directly-to-tiflash}

いいえ。データをTiDB Cloudにインポートすると、データは TiKV にインポートされます。インポートが完了したら、SQL ステートメントを使用して、どのテーブルをTiFlashにレプリケートするかを指定できます。次に、TiDB は指定されたテーブルのレプリカをTiFlashに作成します。詳細については、 [TiFlashレプリカの作成](/tiflash/create-tiflash-replicas.md)を参照してください。

### TiFlashデータを CSV 形式でエクスポートできますか? {#can-i-export-tiflash-data-in-the-csv-format}

いいえ、 TiFlashデータはエクスポートできません。

## Securityよくある質問 {#security-faqs}

### TiDB Cloudは安全ですか? {#is-tidb-cloud-secure}

TiDB Cloudでは、保存されているすべてのデータが暗号化され、すべてのネットワーク トラフィックが Transport Layer Security (TLS) を使用して暗号化されます。

-   保存データの暗号化は、暗号化されたstorageボリュームを使用して自動化されます。
-   クライアントとクラスターの間で転送されるデータの暗号化は、 TiDB CloudWebサーバーTLS と TiDB クラスター TLS を使用して自動化されます。

### TiDB Cloud はビジネス データをどのように暗号化しますか? {#how-does-tidb-cloud-encrypt-my-business-data}

TiDB Cloudは、データベース データやバックアップ データなどの保存中のビジネス データに対して、デフォルトでstorageボリューム暗号化を使用します。 TiDB Cloud、転送中のデータに対して TLS 暗号化が必要であり、TiDB、PD、TiKV、 TiFlash間のデータベース クラスター内のデータに対してコンポーネント レベルの TLS 暗号化も必要です。

TiDB Cloudでのビジネス データの暗号化に関する詳細情報を入手するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

### TiDB Cloudはどのバージョンの TLS をサポートしていますか? {#what-versions-of-tls-does-tidb-cloud-support}

TiDB CloudはTLS 1.2 または TLS 1.3 をサポートします。

### VPC でTiDB Cloudを実行できますか? {#can-i-run-tidb-cloud-in-my-vpc}

いいえ。TiDB TiDB Cloud はDatabase-as-a-Service (DBaaS) であり、 TiDB Cloud VPC 内でのみ実行されます。クラウド コンピューティングのマネージド サービスとして、 TiDB Cloud は物理ハードウェアのセットアップやソフトウェアのインストールを必要とせずにデータベースへのアクセスを提供します。

### 私の TiDB クラスターは安全ですか? {#is-my-tidb-cluster-secure}

TiDB Cloudでは、ニーズに応じて TiDB 専用クラスターまたは TiDB サーバーレス クラスターのいずれかを使用できます。

TiDB 専用クラスターの場合、 TiDB Cloud は次の手段でクラスターのセキュリティを確保します。

-   クラスターごとに独立したサブアカウントと VPC を作成します。
-   外部接続を分離するファイアウォール ルールを設定します。
-   転送中のクラスター データを暗号化するために、クラスターごとにサーバー側 TLS 証明書とコンポーネント レベルの TLS 証明書を作成します。
-   各クラスターに IP アクセス ルールを指定して、許可された送信元 IP アドレスのみがクラスターにアクセスできるようにします。

TiDB サーバーレス クラスターの場合、 TiDB Cloudは次の手段でクラスターのセキュリティを確保します。

-   クラスターごとに独立したサブアカウントを作成します。
-   外部接続を分離するファイアウォール ルールを設定します。
-   転送中のクラスター データを暗号化するためのクラスターサーバーTLS 証明書を提供します。

### TiDB クラスター内のデータベースに接続するにはどうすればよいですか? {#how-do-i-connect-to-my-database-in-a-tidb-cluster}

<SimpleTab>
  <div label="TiDB Dedicated">
    TiDB 専用クラスターの場合、クラスターに接続する手順は次のように簡略化されます。

    1.  ネットワークを認証します。
    2.  データベース ユーザーとログイン資格情報を設定します。
    3.  クラスタサーバー用に TLS をダウンロードして構成します。
    4.  SQL クライアントを選択し、 TiDB CloudUI に表示される自動生成された接続文字列を取得し、その文字列を使用して SQL クライアント経由でクラスターに接続します。

    詳細については、 [TiDB 専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。
  </div>

  <div label="TiDB Serverless">
    TiDB サーバーレス クラスターの場合、クラスターに接続する手順は次のように簡略化されます。

    1.  データベース ユーザーとログイン資格情報を設定します。
    2.  SQL クライアントを選択し、 TiDB CloudUI に表示される自動生成された接続文字列を取得し、その文字列を使用して SQL クライアント経由でクラスターに接続します。

    詳細については、 [TiDB サーバーレスクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)を参照してください。
  </div>
</SimpleTab>

## サポートに関するFAQ {#support-faq}

### 顧客はどのようなサポートを受けられますか? {#what-support-is-available-for-customers}

TiDB Cloud は、金融サービス、電子商取引、エンタープライズ アプリケーション、ゲームなどの業界にわたる 1500 以上のグローバル企業のミッション クリティカルなユースケースを実行してきた TiDB と同じチームによってサポートされています。 TiDB Cloud は、各ユーザーに無料の基本サポート プランを提供しており、拡張サービスの有料プランにアップグレードすることができます。詳細については、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)を参照してください。
