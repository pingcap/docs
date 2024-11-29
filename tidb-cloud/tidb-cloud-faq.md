---
title: TiDB Cloud FAQs
summary: TiDB Cloudに関するよくある質問 (FAQ) について説明します。
---

# TiDB Cloudよくある質問 {#tidb-cloud-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、 TiDB Cloudに関するよくある質問が記載されています。

## 一般的なよくある質問 {#general-faqs}

### TiDB Cloudとは何ですか? {#what-is-tidb-cloud}

TiDB Cloud は、直感的なコンソールから制御できる完全に管理されたクラウド インスタンスを使用して、TiDB クラスターの導入、管理、保守をさらに簡単にします。Amazon Web Services または Google Cloud に簡単に導入して、ミッション クリティカルなアプリケーションを迅速に構築できます。

TiDB Cloud を使用すると、ほとんどトレーニングを受けていない開発者や DBA でも、インフラストラクチャ管理やクラスターの展開など、かつては複雑だったタスクを簡単に処理できるため、データベースの複雑さではなくアプリケーションに集中できます。また、ボタンをクリックするだけで TiDB クラスターをスケールインまたはスケールアウトできるため、必要な量と期間だけデータベースをプロビジョニングできるため、高価なリソースを無駄にすることがなくなります。

### TiDB とTiDB Cloudの関係は何ですか? {#what-is-the-relationship-between-tidb-and-tidb-cloud}

TiDB はオープンソース データベースであり、独自のデータ センター、自己管理型クラウド環境、またはその 2 つのハイブリッドで TiDB Self-Managed を実行したい組織にとって最適なオプションです。

TiDB Cloud は、TiDB の完全に管理されたクラウド データベース サービスです。使いやすい Web ベースの管理コンソールを備えており、ミッション クリティカルな本番環境の TiDB クラスターを管理できます。

### TiDB Cloud はMySQL と互換性がありますか? {#is-tidb-cloud-compatible-with-mysql}

現在、 TiDB Cloud は、トリガー、ストアド プロシージャ、およびユーザー定義関数を除く、 MySQL 5.7および MySQL 8.0 構文の大部分をサポートしています。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)参照してください。

### TiDB Cloudを操作するために使用できるプログラミング言語は何ですか? {#what-programming-languages-can-i-use-to-work-with-tidb-cloud}

MySQL クライアントまたはドライバーでサポートされている任意の言語を使用できます。

### TiDB Cloud はどこで実行できますか? {#where-can-i-run-tidb-cloud}

TiDB Cloudは現在、Amazon Web Services と Google Cloud で利用できます。

### TiDB Cloud は、異なるクラウド サービス プロバイダー間の VPC ピアリングをサポートしていますか? {#does-tidb-cloud-support-vpc-peering-between-different-cloud-service-providers}

いいえ。

### TiDB Cloudではどのバージョンの TiDB がサポートされていますか? {#what-versions-of-tidb-are-supported-on-tidb-cloud}

-   2024 年 11 月 26 日以降、新しいTiDB Cloud Dedicated クラスターのデフォルトの TiDB バージョンは v8.1.1 になります。
-   2024 年 2 月 21 日より、 TiDB Cloud Serverless クラスターの TiDB バージョンは v7.1.3 になります。

詳細については[TiDB Cloudリリースノート](/tidb-cloud/tidb-cloud-release-notes.md)参照してください。

### どの企業が TiDB またはTiDB Cloud を本番で使用していますか? {#what-companies-are-using-tidb-or-tidb-cloud-in-production}

TiDB は、金融サービス、ゲーム、電子商取引など、さまざまな業界の 1,500 社を超えるグローバル企業から信頼されています。当社のユーザーには、Square (米国)、Shopee (シンガポール)、China UnionPay (中国) などがあります。詳細については、 [ケーススタディ](https://www.pingcap.com/customers/)ご覧ください。

### SLA とはどのようなものですか? {#what-does-the-sla-look-like}

TiDB Cloud は99.99% の SLA を提供します。詳細については[TiDB Cloudサービスのサービス レベル契約](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)参照してください。

### TiDB Cloudについて詳しく知るにはどうすればいいですか? {#how-can-i-learn-more-about-tidb-cloud}

TiDB Cloudについて学ぶ最良の方法は、ステップバイステップのチュートリアルに従うことです。まずは以下のトピックを確認してください。

-   [TiDB Cloudの紹介](/tidb-cloud/tidb-cloud-intro.md)
-   [始める](/tidb-cloud/tidb-cloud-quickstart.md)
-   [TiDB Cloudサーバーレスクラスタを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)

### クラスターを削除するときに、 <code>XXX&#39;s Org/default project/Cluster0</code>何を参照しますか? {#what-does-code-xxx-s-org-default-project-cluster0-code-refer-to-when-deleting-a-cluster}

TiDB Cloudでは、クラスターは組織名、プロジェクト名、クラスター名の組み合わせによって一意に識別されます。 目的のクラスターを確実に削除するには、そのクラスターの完全修飾名 (例: `XXX's Org/default project/Cluster0` ) を指定する必要があります。

## アーキテクチャよくある質問 {#architecture-faqs}

### TiDB クラスターにはさまざまなコンポーネントがあります。TiDB、TiKV、およびTiFlashノードとは何ですか? {#there-are-different-components-in-my-tidb-cluster-what-are-tidb-tikv-and-tiflash-nodes}

TiDB は、TiKV またはTiFlashストアから返されたクエリからデータを集約する SQL コンピューティングレイヤーです。TiDB は水平方向にスケーラブルです。TiDB ノードの数を増やすと、クラスターが処理できる同時クエリの数が増えます。

TiKV は、OLTP データを保存するために使用されるトランザクション ストアです。TiKV 内のすべてのデータは複数のレプリカ (デフォルトでは 3 つのレプリカ) に自動的に保持されるため、TiKV はネイティブの高可用性を備え、自動フェイルオーバーをサポートします。TiKV は水平方向にスケーラブルであり、トランザクション ストアの数を増やすと OLTP スループットが向上します。

TiFlashは、トランザクション ストア (TiKV) からデータをリアルタイムで複製し、リアルタイム OLAP ワークロードをサポートする分析storageです。TiKV とは異なり、 TiFlash はデータを列に格納して分析処理を高速化します。TiFlash は水平方向にも拡張可能で、 TiFlashノードを増やすとTiFlashstorageとコンピューティング容量が増加します。

PD、Placement Driver は、クラスターのメタデータを保存するため、TiDB クラスター全体の「頭脳」です。TiKV ノードからリアルタイムで報告されるデータ分散状態に応じて、特定の TiKV ノードにデータ スケジューリング コマンドを送信します。TiDB TiDB Cloudでは、各クラスターの PD は PingCAP によって管理されており、表示または保守することはできません。

### TiDB は TiKV ノード間でデータをどのように複製しますか? {#how-does-tidb-replicate-data-between-the-tikv-nodes}

TiKV はキーと値の空間をキー範囲に分割し、各キー範囲は「リージョン」として扱われます。TiKV では、データはクラスター内のすべてのノードに分散され、リージョンが基本単位として使用されます。PD は、クラスター内のすべてのノードにリージョンを可能な限り均等に分散 (スケジュール) する役割を担います。

TiDB は、 Raftコンセンサス アルゴリズムを使用して、リージョンごとにデータを複製します。異なるノードに保存されているリージョンの複数のレプリカがRaftグループを形成します。

各データの変更はRaftログとして記録されます。RaftRaftのレプリケーションにより、データはRaftグループの複数のノードに安全かつ確実に複製されます。

## 高可用性に関するFAQ {#high-availability-faq}

### TiDB Cloud はどのようにして高可用性を確保するのでしょうか? {#how-does-tidb-cloud-ensure-high-availability}

TiDB はRaftコンセンサス アルゴリズムを使用して、データの可用性を高め、 Raftグループのstorage全体に安全に複製できるようにします。データは TiKV ノード間で冗長的にコピーされ、マシンまたはデータ センターの障害から保護するために異なるアベイラビリティ ゾーンに配置されます。自動フェイルオーバーにより、TiDB はサービスの常時稼働を保証します。

SaaS (Software as a Service) プロバイダーとして、当社はデータ セキュリティを真剣に受け止めています。1 [サービス組織コントロール (SOC) 2 タイプ 1 準拠](https://www.pingcap.com/press-release/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud/)要求される厳格な情報セキュリティ ポリシーと手順を確立しています。これにより、お客様のデータの安全性、可用性、機密性が確保されます。

## 移行に関するFAQ {#migration-faq}

### 別の RDBMS からTiDB Cloudへの簡単な移行パスはありますか? {#is-there-an-easy-migration-path-from-another-rdbms-to-tidb-cloud}

TiDB は MySQL と高い互換性があります。自社ホストの MySQL インスタンスのデータでも、パブリック クラウドが提供する RDS サービスのデータでも、MySQL 互換データベースから TiDB にデータをスムーズに移行できます。詳細については、 [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

## バックアップと復元に関するFAQ {#backup-and-restore-faq}

### TiDB Cloud は増分バックアップをサポートしていますか? {#does-tidb-cloud-support-incremental-backups}

いいえ。クラスターのバックアップ保持期間内の任意の時点にデータを復元する必要がある場合は、PITR (ポイントインタイムリカバリ) を使用できます。詳細については、 [TiDB Cloud Dedicated クラスタで PITR を使用する](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)または[TiDB Cloud Serverless クラスターで PITR を使用する](/tidb-cloud/backup-and-restore-serverless.md#restore)参照してください。

## HTAP に関するよくある質問 {#htap-faqs}

### TiDB Cloud の HTAP 機能をどのように活用すればよいですか? {#how-do-i-make-use-of-tidb-cloud-s-htap-capabilities}

従来、データベースには、オンライン トランザクション処理 (OLTP) データベースとオンライン分析処理 (OLAP) データベースの 2 種類があります。OLTP リクエストと OLAP リクエストは、多くの場合、異なる分離されたデータベースで処理されます。この従来のアーキテクチャでは、OLTP データベースから OLAP のデータ ウェアハウスまたはデータ レイクにデータを移行することは、時間がかかり、エラーが発生しやすいプロセスです。

ハイブリッド トランザクション分析処理 (HTAP) データベースであるTiDB Cloudは、OLTP (TiKV) ストアと OLAP ( TiFlash ) ストア間でデータを確実に自動複製することで、システムアーキテクチャを簡素化し、メンテナンスの複雑さを軽減し、トランザクション データのリアルタイム分析をサポートします。一般的な HTAP の使用例は、ユーザーのパーソナライゼーション、AI による推奨、不正検出、ビジネス インテリジェンス、リアルタイム レポートです。

その他の HTAP シナリオについては、 [データプラットフォームを簡素化する HTAP データベースの構築方法](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)を参照してください。

### データをTiFlashに直接インポートできますか? {#can-i-import-my-data-directly-to-tiflash}

いいえ。TiDB TiDB Cloudにデータをインポートすると、そのデータは TiKV にインポートされます。インポートが完了したら、SQL ステートメントを使用して、 TiFlashに複製するテーブルを指定できます。その後、TiDB はそれに応じて、指定されたテーブルのレプリカをTiFlashに作成します。詳細については、 [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)参照してください。

### TiFlashデータを CSV 形式でエクスポートできますか? {#can-i-export-tiflash-data-in-the-csv-format}

いいえ。TiFlash データはエクスポートできません。

## Securityよくある質問 {#security-faqs}

### TiDB Cloud は安全ですか? {#is-tidb-cloud-secure}

TiDB Cloudでは、保存されているすべてのデータが暗号化され、すべてのネットワーク トラフィックは Transport Layer Security (TLS) を使用して暗号化されます。

-   保存データの暗号化は、暗号化されたstorageボリュームを使用して自動化されます。
-   クライアントとクラスター間で転送されるデータの暗号化は、 TiDB Cloud WebサーバーTLS と TiDB クラスター TLS を使用して自動化されます。

### TiDB Cloud はビジネスデータをどのように暗号化しますか? {#how-does-tidb-cloud-encrypt-my-business-data}

TiDB Cloud は、データベース データやバックアップ データなどの保存中のビジネス データに対して、デフォルトでstorage暗号化を使用します。TiDB TiDB Cloud、転送中のデータに対して TLS 暗号化が必要であり、TiDB、PD、TiKV、 TiFlash間のデータベース クラスター内のデータに対してもコンポーネント レベルの TLS 暗号化が必要です。

TiDB Cloudにおけるビジネス データ暗号化に関する詳しい情報については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

### TiDB Cloud はどのバージョンの TLS をサポートしていますか? {#what-versions-of-tls-does-tidb-cloud-support}

TiDB Cloud はTLS 1.2 または TLS 1.3 をサポートしています。

### VPC でTiDB Cloud を実行できますか? {#can-i-run-tidb-cloud-in-my-vpc}

いいえ。TiDB TiDB Cloudは Database-as-a-Service (DBaaS) であり、 TiDB Cloud VPC 内でのみ実行されます。クラウド コンピューティング管理サービスであるTiDB Cloud は、物理ハードウェアのセットアップやソフトウェアのインストールを必要とせずにデータベースへのアクセスを提供します。

### TiDB クラスターは安全ですか? {#is-my-tidb-cluster-secure}

TiDB Cloudでは、ニーズに応じてTiDB Cloud Dedicated クラスターまたはTiDB Cloud Serverless クラスターのいずれかを使用できます。

TiDB Cloud Dedicated クラスターの場合、 TiDB Cloud は次の対策でクラスターのセキュリティを確保します。

-   各クラスターに独立したサブアカウントと VPC を作成します。
-   外部接続を分離するためのファイアウォール ルールを設定します。
-   転送中のクラスター データを暗号化するために、各クラスターに対してサーバー側の TLS 証明書とコンポーネント レベルの TLS 証明書を作成します。
-   許可された送信元 IP アドレスのみがクラスターにアクセスできるように、各クラスターに IP アクセス ルールを指定します。

TiDB Cloud Serverless クラスターの場合、 TiDB Cloud は次の対策でクラスターのセキュリティを確保します。

-   各クラスターに独立したサブアカウントを作成します。
-   外部接続を分離するためのファイアウォール ルールを設定します。
-   転送中のクラスター データを暗号化するためのクラスターサーバーTLS 証明書を提供します。

### TiDB クラスター内のデータベースに接続するにはどうすればよいですか? {#how-do-i-connect-to-my-database-in-a-tidb-cluster}

<SimpleTab>
<div label="TiDB Cloud Dedicated">

TiDB Cloud Dedicated クラスターの場合、クラスターに接続する手順は次のように簡略化されます。

1.  ネットワークを承認します。
2.  データベース ユーザーとログイン資格情報を設定します。
3.  クラスターサーバー用の TLS をダウンロードして構成します。
4.  SQL クライアントを選択し、 TiDB Cloud UI に表示される自動生成された接続文字列を取得し、その文字列を使用して SQL クライアント経由でクラスターに接続します。

詳細については[TiDB Cloud専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

</div>

<div label="TiDB Cloud Serverless">

TiDB Cloud Serverless クラスターの場合、クラスターに接続する手順は次のように簡略化されます。

1.  データベース ユーザーとログイン資格情報を設定します。
2.  SQL クライアントを選択し、 TiDB Cloud UI に表示される自動生成された接続文字列を取得し、その文字列を使用して SQL クライアント経由でクラスターに接続します。

詳細については[TiDB Cloudサーバーレスクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。

</div>
</SimpleTab>

## サポートFAQ {#support-faq}

### 顧客にはどのようなサポートが提供されますか? {#what-support-is-available-for-customers}

TiDB Cloud Cloud は、金融サービス、電子商取引、エンタープライズ アプリケーション、ゲームなど、さまざまな業界の 1,500 社を超えるグローバル企業のミッション クリティカルなユース ケースを実行してきた TiDB と同じチームによってサポートされています。TiDB TiDB Cloud は、各ユーザーに無料の基本サポート プランを提供しており、有料プランにアップグレードしてサービスを拡張できます。詳細については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)参照してください。

### TiDB Cloudがダウンしているかどうかを確認するにはどうすればよいですか? {#how-do-i-check-if-tidb-cloud-is-down}

TiDB Cloudの現在の稼働状況を[システムステータス](https://status.tidbcloud.com/)ページで確認できます。
