---
title: TiDB Cloud FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud.
---

# TiDB Cloudよくある質問 {#tidb-cloud-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、 TiDB Cloudに関してよく寄せられる質問を一覧表示しています。

## 一般的なよくある質問 {#general-faqs}

### TiDB Cloudとは？ {#what-is-tidb-cloud}

TiDB Cloud は、直感的なコンソールを介して制御する完全に管理されたクラウド インスタンスを使用して、TiDB クラスターの展開、管理、および保守をさらに簡単にします。 Amazon Web Services または Google Cloud に簡単にデプロイして、ミッション クリティカルなアプリケーションをすばやく構築できます。

TiDB Cloud を使用すると、開発者と DBA は、トレーニングをほとんどまたはまったく受けなくても、インフラストラクチャ管理やクラスター展開など、かつては複雑だったタスクを簡単に処理し、データベースの複雑さではなく、アプリケーションに集中できます。また、ボタンをクリックするだけで TiDB クラスターをスケールインまたはスケールアウトすることで、コストのかかるリソースを無駄にする必要がなくなります。必要な量と期間を正確にデータベースにプロビジョニングできるからです。

### TiDB とTiDB Cloudの関係は? {#what-is-the-relationship-between-tidb-and-tidb-cloud}

TiDB はオープンソース データベースであり、TiDB を自社のデータ センター、セルフマネージド クラウド環境、または 2 つのハイブリッド環境でオンプレミスで実行したい組織にとって最適なオプションです。

TiDB Cloud は、TiDB のサービスとしての完全に管理されたクラウド データベースです。使いやすい Web ベースの管理コンソールを備えており、ミッション クリティカルな本番環境の TiDB クラスターを管理できます。

### TiDB Cloud はMySQL と互換性がありますか? {#is-tidb-cloud-compatible-with-mysql}

現在、 TiDB Cloud は、トリガー、ストアド プロシージャ、ユーザー定義関数、および外部キーを除いて、 MySQL 5.7構文の大部分をサポートしています。詳細については、 [MySQL との互換性](https://docs.pingcap.com/tidb/stable/mysql-compatibility)を参照してください。

### TiDB Cloudを操作するために使用できるプログラミング言語は何ですか? {#what-programming-languages-can-i-use-to-work-with-tidb-cloud}

MySQL クライアントまたはドライバーでサポートされている任意の言語を使用できます。

### TiDB Cloud はどこで実行できますか? {#where-can-i-run-tidb-cloud}

TiDB Cloudは現在、Amazon Web Services と Google Cloud で利用できます。

### TiDB Cloud は、異なるクラウド サービス プロバイダー間の VPC ピアリングをサポートしていますか? {#does-tidb-cloud-support-vpc-peering-between-different-cloud-service-providers}

いいえ。

### TiDB Cloudでサポートされている TiDB のバージョンは何ですか? {#what-versions-of-tidb-are-supported-on-tidb-cloud}

現在サポートされている TiDB のバージョンについては、 [TiDB Cloudリリースノート](/tidb-cloud/tidb-cloud-release-notes.md)を参照してください。

### TiDB またはTiDB Cloud を本番で使用している企業は? {#what-companies-are-using-tidb-or-tidb-cloud-in-production}

TiDB は、金融サービス、ゲーム、e コマースなど、さまざまな業界の 1500 を超えるグローバル企業から信頼されています。当社のユーザーには、Square (米国)、Shopee (シンガポール)、および China UnionPay (中国) が含まれます。具体的な詳細については[ケーススタディ](https://en.pingcap.com/customers/)参照してください。

### SLA はどのようなものですか? {#what-does-the-sla-look-like}

TiDB Cloud は99.99% の SLA を提供します。詳細については、 [TiDB Cloudサービスのサービス レベル アグリーメント](https://en.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)を参照してください。

### TiDB Cloudについて詳しく知るにはどうすればよいですか? {#how-can-i-learn-more-about-tidb-cloud}

TiDB Cloudについて学ぶ最善の方法は、ステップバイステップのチュートリアルに従うことです。開始するには、次のトピックを確認してください。

-   [TiDB Cloudの紹介](/tidb-cloud/tidb-cloud-intro.md)
-   [始めましょう](/tidb-cloud/tidb-cloud-quickstart.md)
-   [TiDBクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)

## アーキテクチャに関するよくある質問 {#architecture-faqs}

### TiDB クラスターにはさまざまなコンポーネントがあります。 TiDB、TiKV、およびTiFlashノードとは何ですか? {#there-are-different-components-in-my-tidb-cluster-what-are-tidb-tikv-and-tiflash-nodes}

TiDB は、TiKV またはTiFlashストアから返されたクエリからのデータを集約する SQL コンピューティングレイヤーです。 TiDB は水平方向にスケーラブルです。 TiDB ノードの数を増やすと、クラスターが処理できる同時クエリの数が増えます。

TiKV は、OLTP データの保存に使用されるトランザクション ストアです。 TiKV のすべてのデータは、複数のレプリカ (デフォルトでは 3 つのレプリカ) で自動的に維持されるため、TiKV はネイティブの高可用性を備え、自動フェイルオーバーをサポートします。 TiKV は水平方向にスケーラブルです。トランザクション ストアの数を増やすと、OLTP スループットが向上します。

TiFlashは、トランザクション ストア (TiKV) からリアルタイムでデータをレプリケートし、リアルタイム OLAP ワークロードをサポートする分析storageです。 TiKV とは異なり、 TiFlash はデータを列に格納して分析処理を高速化します。 TiFlash は水平方向にもスケーラブルです。 TiFlashノードを増やすと、OLAPstorageとコンピューティング容量が増加します。

PD、配置Driverは、 TiDB クラスター全体の「頭脳」であり、クラスターのメタデータを格納します。 TiKV ノードからリアルタイムで報告されるデータ配信状態に従って、特定の TiKV ノードにデータ スケジューリング コマンドを送信します。 TiDB Cloudでは各クラスタの PD は PingCAP で管理されており、見ることも維持することもできません。

### TiDB は TiKV ノード間でデータをどのように複製しますか? {#how-does-tidb-replicate-data-between-the-tikv-nodes}

TiKV はキー値空間をキー範囲に分割し、各キー範囲は「リージョン」として扱われます。 TiKV では、データはクラスター内のすべてのノードに分散され、リージョンが基本単位として使用されます。 PD は、クラスター内のすべてのノードにできるだけ均等にリージョンを分散 (スケジューリング) する役割を果たします。

TiDB は、 Raftコンセンサス アルゴリズムを使用して、リージョンごとにデータをレプリケートします。異なるノードに格納されたリージョンの複数のレプリカがRaftグループを形成します。

各データ変更はRaftログとして記録されます。 Raftログの複製により、データはRaftグループの複数のノードに安全かつ確実に複製されます。

## 高可用性に関するFAQ {#high-availability-faq}

### TiDB Cloud はどのようにして高可用性を確保していますか? {#how-does-tidb-cloud-ensure-high-availability}

TiDB はRaftコンセンサス アルゴリズムを使用して、データの可用性を高め、 Raftグループ内のstorage全体で安全に複製されるようにします。データは TiKV ノード間で重複してコピーされ、異なるアベイラビリティーゾーンに配置されて、マシンまたはデータセンターの障害から保護されます。自動フェールオーバーにより、TiDB はサービスが常にオンになっていることを保証します。

Software as a Service (SaaS) プロバイダーとして、当社はデータ セキュリティを真剣に考えています。私たちは、厳格な情報セキュリティポリシーと手順を確立し、 [Service Organization Control (SOC) 2 タイプ 1 準拠](https://en.pingcap.com/press-release/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud/) .これにより、データの安全性、可用性、および機密性が保証されます。

## 移行に関するFAQ {#migration-faq}

### 別の RDBMS からTiDB Cloudへの簡単な移行パスはありますか? {#is-there-an-easy-migration-path-from-another-rdbms-to-tidb-cloud}

TiDB は MySQL との互換性が高いです。データが自己ホスト型の MySQL インスタンスからのものであろうと、パブリック クラウドによって提供される RDS サービスからのものであろうと、MySQL 互換データベースから TiDB にデータをスムーズに移行できます。詳細については、 [MySQL 互換データベースからデータを移行する](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。

## バックアップと復元に関するFAQ {#backup-and-restore-faq}

### TiDB Cloud は増分バックアップをサポートしていますか? {#does-tidb-cloud-support-incremental-backups}

いいえ。クラスターのバックアップ保持期間内の任意の時点にデータを復元する必要がある場合は、 [PITR (ポイントインタイム リカバリ) を使用する](/tidb-cloud/backup-and-restore.md#automatic-backup)ことができます。

## HTAP に関するよくある質問 {#htap-faqs}

### TiDB Cloud の HTAP 機能を利用するにはどうすればよいですか? {#how-do-i-make-use-of-tidb-cloud-s-htap-capabilities}

従来、データベースには、オンライン トランザクション処理 (OLTP) データベースとオンライン分析処理 (OLAP) データベースの 2 種類があります。 OLTP および OLAP 要求は、多くの場合、別々の分離されたデータベースで処理されます。この従来のアーキテクチャでは、OLTP データベースから OLAP 用のデータ ウェアハウスまたはデータ レイクへのデータの移行は、時間がかかり、エラーが発生しやすいプロセスです。

ハイブリッド トランザクション分析処理 (HTAP) データベースであるTiDB Cloudは、OLTP (TiKV) ストアと OLAP ( TiFlash ) の間でデータを確実に自動的に複製することにより、システムアーキテクチャを簡素化し、メンテナンスの複雑さを軽減し、トランザクション データのリアルタイム分析をサポートするのに役立ちます。店。典型的な HTAP のユース ケースは、ユーザーのパーソナライズ、AI の推奨事項、不正行為の検出、ビジネス インテリジェンス、リアルタイム レポートです。

さらなる HTAP シナリオについては、 [データ プラットフォームを簡素化する HTAP データベースの構築方法](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)を参照してください。

### 自分のデータを直接TiFlashにインポートできますか? {#can-i-import-my-data-directly-to-tiflash}

いいえ。TiDB TiDB Cloudにデータをインポートすると、データは TiKV にインポートされます。インポートが完了したら、SQL ステートメントを使用して、どのテーブルをTiFlashにレプリケートするかを指定できます。次に、TiDB はそれに応じて指定されたテーブルのレプリカをTiFlashに作成します。詳細については、 [TiFlashレプリカの作成](/tiflash/create-tiflash-replicas.md)を参照してください。

### TiFlashデータを CSV 形式でエクスポートできますか? {#can-i-export-tiflash-data-in-the-csv-format}

いいえTiFlashデータはエクスポートできません。

## Securityよくある質問 {#security-faqs}

### TiDB Cloudは安全ですか? {#is-tidb-cloud-secure}

TiDB Cloudでは、保管中のすべてのデータが暗号化され、すべてのネットワーク トラフィックが Transport Layer Security (TLS) を使用して暗号化されます。

-   保管中のデータの暗号化は、暗号化されたstorageボリュームを使用して自動化されます。
-   クライアントとクラスター間で転送中のデータの暗号化は、TiDB Cloud WebサーバーTLS と TiDB クラスター TLS を使用して自動化されます。

### TiDB Cloud はどのように私のビジネス データを暗号化しますか? {#how-does-tidb-cloud-encrypt-my-business-data}

TiDB Cloud は、データベース データやバックアップ データを含む保存中のビジネス データに対して、デフォルトでstorageボリューム暗号化を使用します。 TiDB Cloudでは、転送中のデータに TLS 暗号化が必要であり、TiDB、PD、TiKV、およびTiFlash間のデータベース クラスター内のデータにもコンポーネント レベルの TLS 暗号化が必要です。

TiDB Cloudでのビジネス データの暗号化に関するより具体的な情報については、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

### TiDB Cloudはどのバージョンの TLS をサポートしていますか? {#what-versions-of-tls-does-tidb-cloud-support}

TiDB CloudはTLS 1.2 または TLS 1.3 をサポートします。

### VPC でTiDB Cloudを実行できますか? {#can-i-run-tidb-cloud-in-my-vpc}

いいえ。TiDB TiDB Cloud はDatabase-as-a-Service (DBaaS) であり、 TiDB Cloud VPC でのみ実行されます。クラウド コンピューティングのマネージド サービスであるTiDB Cloud は、物理ハードウェアのセットアップやソフトウェアのインストールを必要とせずに、データベースへのアクセスを提供します。

### 私の TiDB クラスターは安全ですか? {#is-my-tidb-cluster-secure}

TiDB Cloudでは、必要に応じてDedicated TierクラスターまたはServerless Tierクラスターのいずれかを使用できます。

Dedicated Tierクラスターの場合、 TiDB Cloud は次の手段でクラスターのセキュリティを確保します。

-   クラスターごとに独立したサブアカウントと VPC を作成します。
-   外部接続を分離するためのファイアウォール ルールを設定します。
-   転送中のクラスター データを暗号化するために、クラスターごとにサーバー側の TLS 証明書とコンポーネント レベルの TLS 証明書を作成します。
-   各クラスターに IP アクセス ルールを提供して、許可されたソース IP アドレスのみがクラスターにアクセスできるようにします。

Serverless Tierクラスターの場合、 TiDB Cloud は次の手段でクラスターのセキュリティを確保します。

-   クラスタごとに独立したサブアカウントを作成します。
-   外部接続を分離するためのファイアウォール ルールを設定します。
-   転送中のクラスター データを暗号化するためのクラスターサーバーTLS 証明書を提供します。

### TiDB クラスター内のデータベースに接続するにはどうすればよいですか? {#how-do-i-connect-to-my-database-in-a-tidb-cluster}

Dedicated Tierクラスターの場合、クラスターに接続する手順は次のように簡略化されます。

1.  ネットワークを承認します。
2.  データベース ユーザーとログイン資格情報を設定します。
3.  クラスターサーバーの TLS をダウンロードして構成します。
4.  SQL クライアントを選択し、 TiDB Cloud UI に表示される自動生成された接続文字列を取得してから、その文字列を使用して SQL クライアントを介してクラスターに接続します。

Serverless Tierクラスターの場合、クラスターに接続する手順は次のように簡略化されます。

1.  データベース ユーザーとログイン資格情報を設定します。
2.  SQL クライアントを選択し、 TiDB Cloud UI に表示される自動生成された接続文字列を取得してから、その文字列を使用して SQL クライアントを介してクラスターに接続します。

詳細については、 [TiDBクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

### データベース クラスタのビジネス データにアクセスできるのは誰ですか? {#who-has-access-to-my-business-data-of-a-database-cluster}

自分の TiDB クラスター内のテーブル データにアクセスできるのは自分だけです。 TiDB Cloudサポートは、TiDB クラスター内のデータに直接アクセスすることはできません。唯一の例外は、製品を改善し、クラスター操作の問題を解決する必要がある場合、 TiDB Cloudサポートは、内部の一時的な承認を提供した後、クラスター操作データにアクセスできることです。すべての承認とアクセスの記録は、PCI-DSS、SOC2、ISO27701 などのサードパーティの監査機関によって毎年監査されます。

TiDB Cloud の運用データは[TiDB Cloudのプライバシー ポリシー](https://www.pingcap.com/privacy-policy/)と[TiDB Cloudデータ処理契約](https://www.pingcap.com/legal/data-processing-agreement-for-tidb-cloud-services/)に記載されています。

## サポートに関するFAQ {#support-faq}

### 顧客はどのようなサポートを利用できますか? {#what-support-is-available-for-customers}

TiDB Cloud は、金融サービス、e コマース、エンタープライズ アプリケーション、ゲームなどの業界の 1500 を超えるグローバル企業のミッション クリティカルなユース ケースを実行してきた TiDB の背後にある同じチームによってサポートされています。 TiDB Cloud は、ユーザーごとに無料の基本サポート プランを提供し、拡張サービスの有料プランにアップグレードできます。詳細については、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)を参照してください。
