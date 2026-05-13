---
title: TiDB Cloud FAQs
summary: TiDB Cloudに関するよくある質問（FAQ）について学びましょう。
---

# TiDB Cloudよくある質問 {#tidb-cloud-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、TiDB Cloudに関してよく寄せられる質問を一覧にしています。

## よくある質問 {#general-faqs}

### TiDB Cloudとは何ですか？ {#what-is-tidb-cloud}

TiDB Cloud、直感的なコンソールを通じて制御できるフルマネージドのクラウド インスタンスにより、TiDB クラスターのデプロイ、管理、保守がさらに簡単になります。 <CustomContent language="en,zh">Amazon Web Services (AWS)、Google Cloud、Microsoft Azure、またはAlibaba Cloudに簡単にデプロイして、ミッションクリティカルなアプリケーションを迅速に構築できます。</CustomContent> <CustomContent language="ja">Amazon Web Services (AWS)、Google Cloud、またはMicrosoft Azureに簡単にデプロイすることで、ミッションクリティカルなアプリケーションを迅速に構築できます。</CustomContent>

TiDB Cloud を利用すれば、開発者や DBA は、トレーニングをほとんど受けていないか、全く受けていない場合でも、インフラストラクチャ管理やクラスタのデプロイといった、かつては複雑だったタスクを容易に処理できるようになり、データベースの複雑さではなく、アプリケーションの開発に集中できます。また、ボタンをクリックするだけで TiDB クラスタをスケールインまたはスケールアウトできるため、必要な量と期間だけデータベースをプロビジョニングでき、高価なリソースを無駄に消費することがなくなります。

### TiDBとTiDB Cloudの関係は何ですか？ {#what-is-the-relationship-between-tidb-and-tidb-cloud}

TiDBはオープンソースのデータベースであり、自社のデータセンター、自己管理型のクラウド環境、またはその両方を組み合わせたハイブリッド環境でTiDB Self-Managedを実行したい組織にとって最適な選択肢です。

TiDB Cloudは、TiDBが提供するフルマネージド型のクラウドデータベースサービスです。使いやすいWebベースの管理コンソールを備えており、ミッションクリティカルな本番環境向けのTiDBクラスタを管理できます。

### TiDB CloudはMySQLと互換性がありますか？ {#is-tidb-cloud-compatible-with-mysql}

現在、 TiDB Cloudは、トリガー、ストアドプロシージャ、ユーザー定義関数を除き、 MySQL 5.7およびMySQL 8.0の構文の大部分をサポートしています。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)を参照してください。

### TiDB Cloudを操作するには、どのようなプログラミング言語を使用できますか？ {#what-programming-languages-can-i-use-to-work-with-tidb-cloud}

MySQLクライアントまたはドライバがサポートする言語であれば、どれでも使用できます。

### TiDB Cloudはどこで実行できますか？ {#where-can-i-run-tidb-cloud}

<CustomContent language="en,zh">TiDB Cloudは現在、Amazon Web Services（AWS）、Google Cloud、Microsoft Azure、およびAlibaba Cloudで利用可能です。</CustomContent> <CustomContent language="ja">TiDB Cloudは現在、Amazon Web Services（AWS）、Google Cloud、およびMicrosoft Azureで利用可能です。</CustomContent>

### TiDB Cloudは、異なるクラウドサービスプロバイダー間でのVPCピアリングをサポートしていますか？ {#does-tidb-cloud-support-vpc-peering-between-different-cloud-service-providers}

いいえ。

### TiDB Cloudでは、どのバージョンのTiDBがサポートされていますか？ {#what-versions-of-tidb-are-supported-on-tidb-cloud}

-   2026年4月14日以降、新規のTiDB Cloud DedicatedクラスターのデフォルトのTiDBバージョンは[v8.5.6](https://docs.pingcap.com/tidb/v8.5/release-8.5.6)となります。
-   TiDB Cloud Starterインスタンスの場合、2026年2月10日以降はTiDBのバージョンは[v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3)となります。
-   TiDB Cloud Essentialインスタンスの場合、2025年4月22日以降、TiDBのバージョンは[v7.5.2](https://docs.pingcap.com/tidb/stable/release-7.5.2)となります。

詳細については、 [TiDB Cloudリリースノート](/tidb-cloud/releases/tidb-cloud-release-notes.md)を参照してください。

### TiDBまたはTiDB Cloudを本番で使用している企業はどこですか？ {#what-companies-are-using-tidb-or-tidb-cloud-in-production}

TiDBは、金融サービス、ゲーム、eコマースなど、さまざまな業界の1500社以上のグローバル企業から信頼されています。ユーザーには、Square（米国）、Shopee（シンガポール）、China UnionPay（中国）などが含まれます。詳細については、[事例研究](https://www.pingcap.com/customers/)ご覧ください。

### SLA（サービスレベル契約）はどのような内容ですか？ {#what-does-the-sla-look-like}

TiDB Cloudは99.99% の SLA を提供します。詳細については、 [TiDB Cloudサービスのサービスレベル契約](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)を参照してください。

### TiDB Cloudにおける「BETA」とはどういう意味ですか？ {#what-does-beta-mean-in-tidb-cloud}

BETAとは、 TiDB Cloudの機能またはサービスが一般提供（GA）される前に、一般公開されるプレビュー段階のことです。

### TiDB Cloudについてもっと詳しく知るにはどうすればよいですか？ {#how-can-i-learn-more-about-tidb-cloud}

TiDB Cloudについて学ぶ最良の方法は、ステップバイステップのチュートリアルに従うことです。まずは以下のトピックをご覧ください。

-   [TiDB Cloudの概要](/tidb-cloud/tidb-cloud-intro.md)
-   [さあ始めましょう](/tidb-cloud/tidb-cloud-quickstart.md)
-   [TiDB Cloud StarterまたはEssentialインスタンスを作成します。](/tidb-cloud/create-tidb-cluster-serverless.md)
-   [TiDB Cloud Premiumインスタンスを作成する](/tidb-cloud/premium/create-tidb-instance-premium.md)
-   [TiDB Cloud Dedicatedクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)

### クラスターを削除する際に、 <code>XXX&#39;s Org/default project/Cluster0</code>何を指しているのでしょうか？ {#what-does-code-xxx-s-org-default-project-cluster0-code-refer-to-when-deleting-a-cluster}

TiDB Cloudでは、クラスターは組織名、プロジェクト名、クラスター名の組み合わせによって一意に識別されます。意図したクラスターを削除していることを確認するには、 `XXX's Org/default project/Cluster0`のように、そのクラスターの完全修飾名を指定する必要があります。

## アーキテクチャよくある質問 {#architecture-faqs}

### 私のTiDBクラスタには様々なコンポーネントがあります。TiDB、TiKV、 TiFlashノードとは何ですか？ {#there-are-different-components-in-my-tidb-cluster-what-are-tidb-tikv-and-tiflash-nodes}

TiDBは、TiKVまたはTiFlashストアから返されたクエリのデータを集約するSQLコンピューティングレイヤーです。TiDBは水平方向に拡張可能であり、TiDBノードの数を増やすことで、クラスタが処理できる同時クエリの数を増やすことができます。

TiKVは、OLTPデータを格納するために使用されるトランザクションストアです。TiKV内のすべてのデータは、複数のレプリカ（デフォルトでは3つのレプリカ）で自動的に管理されるため、TiKVはネイティブな高可用性を備え、自動フェイルオーバーをサポートします。TiKVは水平方向に拡張可能であり、トランザクションストアの数を増やすことでOLTPスループットが向上します。

TiFlashは、トランザクションストア（TiKV）からリアルタイムでデータを複製し、リアルタイムOLAPワークロードをサポートする分析用storageです。TiKVとは異なり、 TiFlashはデータを列形式で格納することで分析処理を高速化します。また、 TiFlashは水平方向に拡張可能であり、 TiFlashノードを増やすことでOLAPstorageとコンピューティング能力が向上します。

配置Driver（PD）は、クラスターのメタデータを格納するため、TiDBクラスター全体の「頭脳」と言えます。PDは、TiKVノードからリアルタイムで報告されるデータ分散状態に基づいて、特定のTiKVノードにデータスケジューリングコマンドを送信します。TiDB TiDB Cloudでは、各クラスターのPDはPingCAPによって管理されるため、ユーザーはPDを確認したり、メンテナンスしたりすることはできません。

### TiDBはTiKVノード間でどのようにデータを複製するのですか？ {#how-does-tidb-replicate-data-between-the-tikv-nodes}

TiKVはキーと値のペアの空間をキー範囲に分割し、各キー範囲を「リージョン」として扱います。TiKVでは、データはクラスタ内のすべてのノードに分散され、リージョンを基本単位として使用します。PDは、リージョンをクラスタ内のすべてのノードにできるだけ均等に分散（スケジューリング）する役割を担います。

TiDBは、 Raftコンセンサスアルゴリズムを使用して、リージョンごとにデータを複製します。異なるノードに保存されたリージョンの複数のレプリカがRaftグループを形成します。

データの変更はすべてRaftログとして記録されます。Raftログのレプリケーションにより、データはRaftグループの複数のノードに安全かつ確実に複製されます。

## 高可用性に関するFAQ {#high-availability-faq}

### TiDB Cloudはどのようにして高可用性を確保しているのですか？ {#how-does-tidb-cloud-ensure-high-availability}

TiDBはRaftコンセンサスアルゴリズムを採用し、 Raftグループ内のstorage全体にデータの高い可用性と安全な複製を確保します。データはTiKVノード間で冗長的にコピーされ、異なるアベイラビリティゾーンに配置されることで、マシンやデータセンターの障害から保護されます。自動フェイルオーバー機能により、TiDBはサービスの常時稼働を保証します。

Software as a Service (SaaS) プロバイダーとして、当社はデータのセキュリティを真剣に考えています。当社は[サービス組織管理（SOC）2タイプ1準拠](https://www.pingcap.com/press-release/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud/)によって要求される厳格な情報セキュリティポリシーと手順を確立しています。これにより、データの安全性、可用性、機密性が確保されます。

## 移行に関するFAQ {#migration-faq}

### 他のRDBMSからTiDB Cloudへの簡単な移行方法はありますか？ {#is-there-an-easy-migration-path-from-another-rdbms-to-tidb-cloud}

TiDB は MySQL と高い互換性があります。データがセルフホスト型 MySQL インスタンスからのものであっても、パブリック クラウドによって提供される RDS サービスからのものであっても、MySQL 互換データベースから TiDB にスムーズにデータを移行できます。詳細については、 [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

## バックアップと復元に関するFAQ {#backup-and-restore-faq}

### TiDB Cloudは増分バックアップをサポートしていますか？ {#does-tidb-cloud-support-incremental-backups}

いいえ。バックアップ保持期間内の任意の時点にデータを復元する必要がある場合は、PITR (Point-in-time Recovery) を使用できます。詳細については、 [TiDB Cloud DedicatedクラスターでPITRを使用する](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)または[TiDB Cloud EssentialインスタンスでPITRを使用する](/tidb-cloud/backup-and-restore-serverless.md#restore)を参照してください。

## HTAPに関するよくある質問 {#htap-faqs}

### TiDB CloudのHTAP機能を利用するにはどうすればよいですか？ {#how-do-i-make-use-of-tidb-cloud-s-htap-capabilities}

従来、データベースにはオンライン・トランザクション処理（OLTP）データベースとオンライン分析処理（OLAP）データベースの2種類がありました。OLTPとOLAPのリクエストは、多くの場合、それぞれ独立したデータベースで処理されます。このような従来のアーキテクチャでは、OLTPデータベースからOLAP用のデータウェアハウスやデータレイクへデータを移行するには、時間がかかり、エラーが発生しやすいプロセスとなります。

TiDB Cloudは、ハイブリッドトランザクション分析処理（HTAP）データベースとして、OLTP（TiKV）ストアとOLAP（ TiFlash ）ストア間でデータを自動的に確実に複製することで、システムアーキテクチャの簡素化、メンテナンスの複雑さの軽減、トランザクションデータに対するリアルタイム分析のサポートを実現します。HTAPの一般的なユースケースとしては、ユーザーパーソナライゼーション、AIによるレコメンデーション、不正検出、ビジネスインテリジェンス、リアルタイムレポートなどが挙げられます。

HTAP シナリオの詳細については、 [データプラットフォームを簡素化するHTAPデータベースの構築方法](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)を参照してください。

### TiFlashにデータを直接インポートできますか？ {#can-i-import-my-data-directly-to-tiflash}

いいえ。TiDB TiDB Cloudにデータをインポートすると、データはTiKVにインポートされます。インポートが完了したら、SQLステートメントを使用して、 TiFlashにレプリケートするテーブルを指定できます。その後、TiDBは指定されたテーブルのレプリカをTiFlashに作成します。詳細については、 [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)参照してください。.

### TiFlashのデータをCSV形式でエクスポートできますか？ {#can-i-export-tiflash-data-in-the-csv-format}

いいえ。TiFlashのデータはエクスポートできません。

## Securityよくある質問 {#security-faqs}

### TiDB Cloudは安全ですか？ {#is-tidb-cloud-secure}

TiDB Cloudでは、保存されているすべてのデータは暗号化され、すべてのネットワークトラフィックはトランスポート層Security（TLS）を使用して暗号化されます。

-   保存データの暗号化は、暗号化されたstorageボリュームを使用して自動化されます。
-   クライアントとTiDBクラスタまたはインスタンス間のデータ転送における暗号化は、 TiDB CloudウェブサーバーのTLSとTiDBクラスタのTLSを使用して自動化されています。

### TiDB Cloudはどのようにして私のビジネスデータを暗号化するのですか？ {#how-does-tidb-cloud-encrypt-my-business-data}

TiDB Cloudは、データベースデータやバックアップデータを含む、保存されているビジネスデータに対して、デフォルトでstorageボリューム暗号化を使用します。TiDB TiDB Cloudは、転送中のデータに対してTLS暗号化を要求し、さらに、TiDB、PD、TiKV、 TiFlash間のデータベースクラスタ内のデータに対して、コンポーネントレベルのTLS暗号化も要求します。

TiDB Cloudにおけるビジネスデータ暗号化に関するより詳細な情報については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

### TiDB CloudはどのバージョンのTLSをサポートしていますか？ {#what-versions-of-tls-does-tidb-cloud-support}

TiDB CloudはTLS 1.2またはTLS 1.3をサポートしています。

### TiDB Cloudを自分のVPC内で実行できますか？ {#can-i-run-tidb-cloud-in-my-vpc}

いいえ。TiDB TiDB Cloudはデータベース・アズ・ア・サービス（DBaaS）であり、 TiDB Cloud VPC内でのみ動作します。クラウドコンピューティングのマネージドサービスとして、 TiDB Cloudは物理ハードウェアのセットアップやソフトウェアのインストールを必要とせずにデータベースへのアクセスを提供します。

### 私のTiDB Cloudのリソースは安全ですか？ {#is-my-tidb-cloud-resource-secure}

TiDB Cloudでは、ニーズに応じて、 TiDB Cloud Dedicatedクラスター、 TiDB Cloud Premiumインスタンス、 TiDB Cloud Starterインスタンス、またはTiDB Cloud Essentialインスタンスを使用できます。

TiDB Cloud Dedicatedクラスタの場合、 TiDB Cloudは以下の対策によってクラスタのセキュリティを確保します。

-   各クラスターごとに独立したサブアカウントとVPCを作成します。
-   外部接続を隔離するためのファイアウォールルールを設定します。
-   各クラスターに対して、サーバー側のTLS証明書とコンポーネントレベルのTLS証明書を作成し、転送中のクラスターデータを暗号化します。
-   各クラスターに対してIPアクセスルールを設定し、許可された送信元IPアドレスのみがクラスターにアクセスできるようにします。

TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスの場合、 TiDB Cloudは以下の対策によってインスタンスのセキュリティを確保します。

-   各インスタンスごとに独立したサブアカウントを作成します。
-   外部接続を隔離するためのファイアウォールルールを設定します。
-   インスタンスサーバーのTLS証明書を提供し、転送中のインスタンスデータを暗号化します。

### TiDBでデータベースに接続するにはどうすればよいですか？ {#how-do-i-connect-to-my-database-in-tidb}

<SimpleTab>
<div label="TiDB Cloud Dedicated">

TiDB Cloud Dedicatedクラスターの場合、クラスターへの接続手順は以下のように簡略化されています。

1.  ネットワークを認証してください。
2.  データベースのユーザーとログイン認証情報を設定してください。
3.  クラスタサーバー用にTLSをダウンロードして設定してください。
4.  SQLクライアントを選択し、 TiDB Cloud UIに自動生成された接続文字列を表示させた後、その文字列を使用してSQLクライアント経由でクラスターに接続します。

詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

</div>

<div label="TiDB Cloud Starter/Essential">

TiDB Cloud StarterまたはEssentialインスタンスの場合、インスタンスへの接続手順は以下のように簡略化されています。

1.  データベースユーザーとログイン認証情報を設定します。
2.  SQLクライアントを選択し、 TiDB Cloud UIに自動生成された接続文字列を表示させた後、その文字列を使用してSQLクライアント経由でTiDB Cloud StarterまたはEssentialインスタンスに接続します。

詳細については、 [TiDB Cloud StarterまたはEssentialインスタンスに接続します](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。

</div>
</SimpleTab>

## サポートに関するFAQ {#support-faq}

### 顧客向けにはどのようなサポートが提供されていますか？ {#what-support-is-available-for-customers}

TiDB Cloudは、金融サービス、eコマース、エンタープライズアプリケーション、ゲームなど、さまざまな業界の1500社以上のグローバル企業でミッションクリティカルなユースケースを支えてきたTiDBの開発チームによってサポートされています。TiDB TiDB Cloudは、ユーザーごとに無料の基本サポートプランを提供しており、より高度なサービスをご希望の場合は有料プランにアップグレードできます。詳細については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)をご覧ください。

### TiDB Cloudがダウンしているかどうかを確認するにはどうすればよいですか？ {#how-do-i-check-if-tidb-cloud-is-down}

TiDB Cloudの現在の稼働状況は[システムステータス](https://status.tidbcloud.com/)ページで確認できます。
