---
title: TiDB Cloud FAQs
summary: TiDB Cloudに関するよくある質問 (FAQ) について説明します。
---

# TiDB Cloudに関するよくある質問 {#tidb-cloud-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、 TiDB Cloudに関してよく寄せられる質問が記載されています。

## 一般的なよくある質問 {#general-faqs}

### TiDB Cloudとは何ですか? {#what-is-tidb-cloud}

TiDB Cloudは、直感的なコンソールから操作できるフルマネージドクラウドインスタンスを提供することで、TiDBクラスタの導入、管理、保守をさらに簡素化します。Amazon Web Services（AWS）、Google Cloud、Microsoft Azureに簡単に導入でき、ミッションクリティカルなアプリケーションを迅速に構築できます。

TiDB Cloud は、トレーニングをほとんど受けていない、あるいは全く受けていない開発者やデータベース管理者でも、かつては複雑だったインフラストラクチャ管理やクラスタの導入といったタスクを容易に処理できるようにし、データベースの複雑さに煩わされることなく、アプリケーションに集中できるようにします。また、ボタンをクリックするだけで TiDB クラスタをスケールイン/スケールアウトできるため、必要な量と期間だけデータベースをプロビジョニングできるため、高価なリソースを無駄にすることがなくなります。

### TiDB とTiDB Cloudの関係は何ですか? {#what-is-the-relationship-between-tidb-and-tidb-cloud}

TiDB はオープンソース データベースであり、独自のデータ センター、自己管理型クラウド環境、またはその 2 つのハイブリッドで TiDB Self-Managed を実行したい組織にとって最適なオプションです。

TiDB Cloudは、TiDBのフルマネージドクラウドDatabase as a Service（DBaaS）です。使いやすいWebベースの管理コンソールを備えており、ミッションクリティカルな本番環境向けのTiDBクラスターを管理できます。

### TiDB Cloud はMySQL と互換性がありますか? {#is-tidb-cloud-compatible-with-mysql}

現在、 TiDB Cloudは、トリガー、ストアドプロシージャ、ユーザー定義関数を除き、 MySQL 5.7およびMySQL 8.0の構文の大部分をサポートしています。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)ご覧ください。

### TiDB Cloudを操作するために使用できるプログラミング言語は何ですか? {#what-programming-languages-can-i-use-to-work-with-tidb-cloud}

MySQL クライアントまたはドライバーでサポートされている任意の言語を使用できます。

### TiDB Cloud はどこで実行できますか? {#where-can-i-run-tidb-cloud}

TiDB Cloudは現在、Amazon Web Services (AWS)、Google Cloud、Microsoft Azure で利用できます。

### TiDB Cloud は、異なるクラウド サービス プロバイダー間の VPC ピアリングをサポートしていますか? {#does-tidb-cloud-support-vpc-peering-between-different-cloud-service-providers}

いいえ。

### TiDB Cloudではどのバージョンの TiDB がサポートされていますか? {#what-versions-of-tidb-are-supported-on-tidb-cloud}

-   2025 年 1 月 2 日以降、新しいTiDB Cloud Dedicated クラスターのデフォルトの TiDB バージョンは[バージョン8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)なります。
-   2024 年 2 月 21 日以降、 TiDB Cloud Serverless クラスターの TiDB バージョンは[バージョン7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3)なります。

詳細については[TiDB Cloudリリースノート](/tidb-cloud/tidb-cloud-release-notes.md)参照してください。

### TiDB またはTiDB Cloud を本番で使用している企業はどれですか? {#what-companies-are-using-tidb-or-tidb-cloud-in-production}

TiDBは、金融サービス、ゲーム、eコマースなど、様々な業界の1,500社を超えるグローバル企業から信頼されています。ユーザーには、Square（米国）、Shopee（シンガポール）、China UnionPay（中国）などが名を連ねています。詳細は[ケーススタディ](https://www.pingcap.com/customers/)ご覧ください。

### SLA とはどのようなものですか? {#what-does-the-sla-look-like}

TiDB Cloudは99.99%のSLAを提供します。詳細は[TiDB Cloudサービスのサービス レベル契約](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)ご覧ください。

### TiDB Cloudにおける BETA とはどういう意味ですか? {#what-does-beta-mean-in-tidb-cloud}

BETA は、 TiDB Cloud の機能またはサービスが一般公開 (GA) される前のパブリック プレビュー ステージです。

### TiDB Cloudについて詳しく知るにはどうすればいいですか? {#how-can-i-learn-more-about-tidb-cloud}

TiDB Cloudについて学ぶ最良の方法は、ステップバイステップのチュートリアルに従うことです。まずは以下のトピックをご覧ください。

-   [TiDB Cloudの紹介](/tidb-cloud/tidb-cloud-intro.md)
-   [始める](/tidb-cloud/tidb-cloud-quickstart.md)
-   [TiDB Cloudサーバーレスクラスタを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)

### クラスターを削除するときに<code>XXX&#39;s Org/default project/Cluster0</code>何を参照しますか? {#what-does-code-xxx-s-org-default-project-cluster0-code-refer-to-when-deleting-a-cluster}

TiDB Cloudでは、クラスターは組織名、プロジェクト名、クラスター名の組み合わせによって一意に識別されます。削除するクラスターが意図したクラスターであることを確認するには、そのクラスターの完全修飾名（例： `XXX's Org/default project/Cluster0` ）を指定する必要があります。

## アーキテクチャに関するよくある質問 {#architecture-faqs}

### TiDBクラスターにはさまざまなコンポーネントがあります。TiDB、TiKV、 TiFlashノードとは何ですか？ {#there-are-different-components-in-my-tidb-cluster-what-are-tidb-tikv-and-tiflash-nodes}

TiDBは、TiKVまたはTiFlashストアから返されたクエリからデータを集約するSQLコンピューティングレイヤーです。TiDBは水平方向にスケーラブルであり、TiDBノードの数を増やすと、クラスターが処理できる同時クエリ数が増加します。

TiKVは、OLTPデータの保存に使用されるトランザクションストアです。TiKV内のすべてのデータは複数のレプリカ（デフォルトでは3つのレプリカ）に自動的に保持されるため、TiKVはネイティブの高可用性を備え、自動フェイルオーバーをサポートします。TiKVは水平方向にスケーラブルであり、トランザクションストアの数を増やすことでOLTPスループットが向上します。

TiFlashは、トランザクションストア（TiKV）からデータをリアルタイムに複製し、リアルタイムOLAPワークロードをサポートする分析storageです。TiKVとは異なり、 TiFlashはデータを列形式で保存することで分析処理を高速化します。また、 TiFlashは水平方向にも拡張可能で、 TiFlashノードを増やすことでOLAPstorageとコンピューティング能力を増強できます。

PD（配置Driver）は、TiDBクラスタ全体の「頭脳」であり、クラスタのメタデータを保存します。TiKVノードからリアルタイムに報告されるデータ分散状態に基づき、特定のTiKVノードにデータスケジューリングコマンドを送信します。TiDB TiDB Cloudでは、各クラスタのPDはPingCAPによって管理されており、ユーザーが確認したりメンテナンスしたりすることはできません。

### TiDB はどのようにして TiKV ノード間でデータを複製しますか? {#how-does-tidb-replicate-data-between-the-tikv-nodes}

TiKVはキーと値の空間をキー範囲に分割し、各キー範囲を「リージョン」として扱います。TiKVでは、データはクラスター内のすべてのノードに分散され、リージョンを基本単位として使用します。PDは、クラスター内のすべてのノードにリージョンを可能な限り均等に分散（スケジュール）する役割を担います。

TiDBは、 Raftコンセンサスアルゴリズムを使用して、リージョンごとにデータを複製します。異なるノードに保存されたリージョンの複数のレプリカがRaftグループを形成します。

各データの変更はRaftログとして記録されます。Raftログレプリケーションにより、データはRaftグループの複数のノードに安全かつ確実に複製されます。

## 高可用性に関するFAQ {#high-availability-faq}

### TiDB Cloud はどのようにして高可用性を確保するのでしょうか? {#how-does-tidb-cloud-ensure-high-availability}

TiDBはRaftコンセンサスアルゴリズムを使用し、データの高可用性とRaftグループ内のstorage全体への安全なレプリケーションを実現します。データはTiKVノード間で冗長コピーされ、異なるアベイラビリティゾーンに配置されるため、マシンやデータセンターの障害から保護されます。自動フェイルオーバー機能により、TiDBはサービスの常時稼働を保証します。

SaaS（Software as a Service）プロバイダーとして、私たちはデータセキュリティを非常に重視しています。1 で求められる厳格な情報セキュリティポリシーと手順を確立しています。これにより、お客様のデータの安全性、可用性、機密[サービス組織コントロール（SOC）2タイプ1コンプライアンス](https://www.pingcap.com/press-release/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud/)を確保しています。

## 移行に関するFAQ {#migration-faq}

### 別の RDBMS からTiDB Cloudへの簡単な移行パスはありますか? {#is-there-an-easy-migration-path-from-another-rdbms-to-tidb-cloud}

TiDBはMySQLとの互換性が非常に高く、MySQL互換データベースであれば、セルフホスト型MySQLインスタンスからでもパブリッククラウドのRDSサービスからでも、TiDBへのデータ移行がスムーズに行えます。詳細については、 [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)ご覧ください。

## バックアップと復元に関するFAQ {#backup-and-restore-faq}

### TiDB Cloud は増分バックアップをサポートしていますか? {#does-tidb-cloud-support-incremental-backups}

いいえ。クラスターのバックアップ保持期間内の任意の時点にデータを復元する必要がある場合は、PITR（ポイントインタイムリカバリ）を使用できます。詳細については、 [TiDB Cloud Dedicated クラスタで PITR を使用する](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)または[TiDB Cloud Serverless クラスターで PITR を使用する](/tidb-cloud/backup-and-restore-serverless.md#restore)ご覧ください。

## HTAPに関するよくある質問 {#htap-faqs}

### TiDB Cloud の HTAP 機能をどのように活用すればよいですか? {#how-do-i-make-use-of-tidb-cloud-s-htap-capabilities}

従来、データベースにはオンライントランザクション処理（OLTP）データベースとオンライン分析処理（OLAP）データベースの2種類があります。OLTPリクエストとOLAPリクエストは、多くの場合、それぞれ異なる独立したデータベースで処理されます。この従来のアーキテクチャでは、OLTPデータベースからOLAP用のデータウェアハウスまたはデータレイクへのデータ移行は、時間がかかり、エラーが発生しやすいプロセスです。

ハイブリッドトランザクション分析処理（HTAP）データベースであるTiDB Cloudは、OLTP（TiKV）ストアとOLAP（ TiFlash ）ストア間でデータを自動的に確実に複製することで、システムアーキテクチャの簡素化、メンテナンスの複雑さの軽減、トランザクションデータのリアルタイム分析をサポートします。HTAPの代表的なユースケースとしては、ユーザーパーソナライゼーション、AIレコメンデーション、不正検出、ビジネスインテリジェンス、リアルタイムレポートなどが挙げられます。

その他の HTAP シナリオについては、 [データプラットフォームを簡素化するHTAPデータベースの構築方法](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)を参照してください。

### データをTiFlashに直接インポートできますか? {#can-i-import-my-data-directly-to-tiflash}

いいえ。TiDB TiDB Cloudにデータをインポートすると、データは TiKV にもインポートされます。インポートが完了したら、SQL 文を使用してTiFlashに複製するテーブルを指定できます。その後、TiDB は指定されたテーブルのレプリカをTiFlashに作成します。詳細については、 [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)ご覧ください。

### TiFlashデータを CSV 形式でエクスポートできますか? {#can-i-export-tiflash-data-in-the-csv-format}

いいえ。TiFlashTiFlashはエクスポートできません。

## Securityよくある質問 {#security-faqs}

### TiDB Cloud は安全ですか? {#is-tidb-cloud-secure}

TiDB Cloudでは、保存されているすべてのデータが暗号化され、すべてのネットワーク トラフィックは Transport Layer Security (TLS) を使用して暗号化されます。

-   保存データの暗号化は、暗号化されたstorageボリュームを使用して自動化されます。
-   クライアントとクラスター間で転送されるデータの暗号化は、TiDB Cloud WebサーバーTLS と TiDB クラスター TLS を使用して自動化されます。

### TiDB Cloud はビジネスデータをどのように暗号化しますか? {#how-does-tidb-cloud-encrypt-my-business-data}

TiDB Cloud は、データベースデータやバックアップデータなど、保存中のビジネスデータに対して、デフォルトでstorageボリューム暗号化を使用します。TiDB TiDB Cloud、転送中のデータに TLS 暗号化を適用するほか、TiDB、PD、TiKV、 TiFlash間のデータベースクラスター内のデータにもコンポーネントレベルの TLS 暗号化を適用する必要があります。

TiDB Cloudにおけるビジネス データ暗号化の詳しい情報については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

### TiDB Cloud はどのバージョンの TLS をサポートしていますか? {#what-versions-of-tls-does-tidb-cloud-support}

TiDB Cloud はTLS 1.2 または TLS 1.3 をサポートしています。

### VPC でTiDB Cloudを実行できますか? {#can-i-run-tidb-cloud-in-my-vpc}

いいえ。TiDB TiDB Cloudは Database-as-a-Service (DBaaS) であり、 TiDB Cloud VPC 内でのみ動作します。クラウドコンピューティングのマネージドサービスであるTiDB Cloud は、物理的なハードウェアのセットアップやソフトウェアのインストールを必要とせずにデータベースへのアクセスを提供します。

### TiDB クラスターは安全ですか? {#is-my-tidb-cluster-secure}

TiDB Cloudでは、ニーズに応じてTiDB Cloud Dedicated クラスターまたはTiDB Cloud Serverless クラスターのいずれかを使用できます。

TiDB Cloud Dedicated クラスターの場合、 TiDB Cloud は次の対策でクラスターのセキュリティを確保します。

-   各クラスターに独立したサブアカウントと VPC を作成します。
-   外部接続を分離するためのファイアウォール ルールを設定します。
-   転送中のクラスター データを暗号化するために、各クラスターのサーバー側 TLS 証明書とコンポーネント レベルの TLS 証明書を作成します。
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

TiDB Cloudは、金融サービス、eコマース、エンタープライズアプリケーション、ゲームなど、1,500社以上のグローバル企業のミッションクリティカルなユースケースを運用してきたTiDBと同じチームによってサポートされています。TiDB TiDB Cloudは、ユーザーごとに無料の基本サポートプランを提供しており、拡張サービスをご希望の場合は有料プランにアップグレードできます。詳細については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)ご覧ください。

### TiDB Cloudがダウンしているかどうかを確認するにはどうすればよいですか? {#how-do-i-check-if-tidb-cloud-is-down}

TiDB Cloudの現在の稼働状況を[システムステータス](https://status.tidbcloud.com/)ページで確認できます。
