---
title: TiDB Cloud FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud.
---

# TiDB Cloudに関するよくある質問 {#tidb-cloud-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、 TiDB Cloudに関してよく寄せられる質問を一覧表示しています。

## 一般的なよくある質問 {#general-faqs}

### TiDB Cloudとは？ {#what-is-tidb-cloud}

TiDB Cloudは、直感的なコンソールを介して制御する完全に管理されたクラウド インスタンスを使用して、TiDB クラスターの展開、管理、および保守をさらに簡単にします。 Amazon Web Services または Google Cloud に簡単にデプロイして、ミッション クリティカルなアプリケーションをすばやく構築できます。

TiDB Cloudを使用すると、開発者と DBA は、トレーニングをほとんどまたはまったく受けなくても、インフラストラクチャ管理やクラスター展開など、かつては複雑だったタスクを簡単に処理し、データベースの複雑さではなく、アプリケーションに集中できます。また、ボタンをクリックするだけで TiDB クラスターをスケールインまたはスケールアウトすることで、コストのかかるリソースを無駄にする必要がなくなります。必要な量と期間を正確にデータベースにプロビジョニングできるからです。

### TiDB とTiDB Cloudの関係は? {#what-is-the-relationship-between-tidb-and-tidb-cloud}

TiDB はオープンソース データベースであり、TiDB を自社のデータ センター、セルフマネージド クラウド環境、または 2 つのハイブリッド環境でオンプレミスで実行したい組織にとって最適なオプションです。

TiDB Cloudは、TiDB のサービスとしての完全に管理されたクラウド データベースです。使いやすい Web ベースの管理コンソールを備えており、ミッション クリティカルな運用環境の TiDB クラスターを管理できます。

### TiDB Cloudは MySQL と互換性がありますか? {#is-tidb-cloud-compatible-with-mysql}

現在、 TiDB Cloudは、トリガー、ストアド プロシージャ、ユーザー定義関数、および外部キーを除いて、 MySQL 5.7構文の大部分をサポートしています。詳細については、 [MySQL との互換性](https://docs.pingcap.com/tidb/stable/mysql-compatibility)を参照してください。

### TiDB Cloudを操作するために使用できるプログラミング言語は何ですか? {#what-programming-languages-can-i-use-to-work-with-tidb-cloud}

MySQL クライアントまたはドライバーでサポートされている任意の言語を使用できます。

### TiDB Cloudはどこで実行できますか? {#where-can-i-run-tidb-cloud}

TiDB Cloudは現在、Amazon Web Services と Google Cloud で利用できます。

### TiDB Cloudは、異なるクラウド サービス プロバイダー間の VPC ピアリングをサポートしていますか? {#does-tidb-cloud-support-vpc-peering-between-different-cloud-service-providers}

いいえ。

### TiDB Cloudでサポートされている TiDB のバージョンは何ですか? {#what-versions-of-tidb-are-supported-on-tidb-cloud}

現在サポートされている TiDB のバージョンについては、 [TiDB Cloudリリースノート](/tidb-cloud/release-notes-2022.md)を参照してください。

### TiDB またはTiDB Cloudを本番環境で使用している企業は? {#what-companies-are-using-tidb-or-tidb-cloud-in-production}

TiDB は、金融サービス、ゲーム、e コマースなど、さまざまな業界の 1500 を超えるグローバル企業から信頼されています。当社のユーザーには、Square (米国)、Shopee (シンガポール)、および China UnionPay (中国) が含まれます。具体的な詳細については、 [ケーススタディ](https://en.pingcap.com/customers/)を参照してください。

### SLA はどのようなものですか? {#what-does-the-sla-look-like}

TiDB Cloudは 99.99% の SLA を提供します。詳細については、 [TiDB Cloudサービスのサービス レベル アグリーメント](https://en.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)を参照してください。

### TiDB Cloudについて詳しく知るにはどうすればよいですか? {#how-can-i-learn-more-about-tidb-cloud}

TiDB Cloudについて学ぶ最善の方法は、ステップバイステップのチュートリアルに従うことです。開始するには、次のトピックを確認してください。

-   [TiDB Cloudの紹介](/tidb-cloud/tidb-cloud-intro.md)
-   [始めましょう](/tidb-cloud/tidb-cloud-quickstart.md)
-   [TiDBクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)

## アーキテクチャに関するよくある質問 {#architecture-faqs}

### TiDB クラスターにはさまざまなコンポーネントがあります。 PD、TiDB、TiKV、 TiFlashノードとは何ですか? {#there-are-different-components-in-my-tidb-cluster-what-are-pd-tidb-tikv-and-tiflash-nodes}

PD、配置Driverは、TiDB クラスター全体の「頭脳」であり、クラスターのメタデータを格納します。 TiKV ノードからリアルタイムで報告されるデータ配信状態に従って、特定の TiKV ノードにデータ スケジューリング コマンドを送信します。

TiDB は、TiKV またはTiFlashストアから返されたクエリからのデータを集約する SQL コンピューティングレイヤーです。 TiDB は水平方向にスケーラブルです。 TiDB ノードの数を増やすと、クラスターが処理できる同時クエリの数が増えます。

TiKV は、OLTP データの保存に使用されるトランザクション ストアです。 TiKV のすべてのデータは、複数のレプリカ (デフォルトでは 3 つのレプリカ) で自動的に維持されるため、TiKV はネイティブの高可用性を備え、自動フェイルオーバーをサポートします。 TiKV は水平方向にスケーラブルです。トランザクション ストアの数を増やすと、OLTP スループットが向上します。

TiFlashは、トランザクション ストア (TiKV) からリアルタイムでデータをレプリケートし、リアルタイム OLAP ワークロードをサポートする分析ストレージです。 TiKV とは異なり、 TiFlashはデータを列に格納して分析処理を高速化します。 TiFlashは水平方向にもスケーラブルです。 TiFlashノードを増やすと、OLAP ストレージとコンピューティング容量が増加します。

### TiDB は TiKV ノード間でデータをどのように複製しますか? {#how-does-tidb-replicate-data-between-the-tikv-nodes}

TiKV はキー値空間をキー範囲に分割し、各キー範囲は「リージョン」として扱われます。 TiKV では、データはクラスター内のすべてのノードに分散され、リージョンが基本単位として使用されます。 PD は、クラスター内のすべてのノードにできるだけ均等にリージョンを分散 (スケジューリング) する役割を果たします。

TiDB は、 Raftコンセンサス アルゴリズムを使用して、リージョンごとにデータをレプリケートします。異なるノードに格納されたリージョンの複数のレプリカがRaftグループを形成します。

各データ変更はRaftログとして記録されます。 Raftログの複製により、データはRaftグループの複数のノードに安全かつ確実に複製されます。

## 高可用性FAQ {#high-availability-faq}

### TiDB Cloudはどのようにして高可用性を確保していますか? {#how-does-tidb-cloud-ensure-high-availability}

TiDB はRaftコンセンサス アルゴリズムを使用して、データの可用性を高め、 Raftグループ内のストレージ全体で安全に複製されるようにします。データは TiKV ノード間で重複してコピーされ、異なるアベイラビリティーゾーンに配置されて、マシンまたはデータセンターの障害から保護されます。自動フェールオーバーにより、TiDB はサービスが常にオンになっていることを保証します。

Software as a Service (SaaS) プロバイダーとして、当社はデータ セキュリティを真剣に考えています。私たちは、厳格な情報セキュリティポリシーと手順を確立し、 [Service Organization Control (SOC) 2 タイプ 1 準拠](https://en.pingcap.com/press-release/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud/) .これにより、データの安全性、可用性、および機密性が保証されます。

## 移行FAQ {#migration-faq}

### 別の RDBMS からTiDB Cloudへの簡単な移行パスはありますか? {#is-there-an-easy-migration-path-from-another-rdbms-to-tidb-cloud}

TiDB は MySQL との互換性が高いです。データが自己ホスト型の MySQL インスタンスからのものであろうと、パブリック クラウドによって提供される RDS サービスからのものであろうと、MySQL 互換データベースから TiDB にデータをスムーズに移行できます。詳細については、 [MySQL 互換データベースからデータを移行する](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。

## HTAP に関するよくある質問 {#htap-faqs}

### TiDB Cloud の HTAP 機能を利用するにはどうすればよいですか? {#how-do-i-make-use-of-tidb-cloud-s-htap-capabilities}

従来、データベースには、オンライン トランザクション処理 (OLTP) データベースとオンライン分析処理 (OLAP) データベースの 2 種類があります。 OLTP および OLAP 要求は、多くの場合、別々の分離されたデータベースで処理されます。この従来のアーキテクチャでは、OLTP データベースから OLAP 用のデータ ウェアハウスまたはデータ レイクへのデータの移行は、時間がかかり、エラーが発生しやすいプロセスです。

ハイブリッド トランザクション分析処理 (HTAP) データベースであるTiDB Cloudは、OLTP (TiKV) ストアと OLAP ( TiFlash ) の間でデータを確実に自動的に複製することにより、システムアーキテクチャを簡素化し、メンテナンスの複雑さを軽減し、トランザクション データのリアルタイム分析をサポートするのに役立ちます。お店。典型的な HTAP のユース ケースは、ユーザーのパーソナライズ、AI の推奨事項、不正行為の検出、ビジネス インテリジェンス、リアルタイム レポートです。

さらなる HTAP シナリオについては、 [データ プラットフォームを簡素化する HTAP データベースの構築方法](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)を参照してください。

### 自分のデータを直接TiFlashにインポートできますか? {#can-i-import-my-data-directly-to-tiflash}

いいえTiDB Cloudにデータをインポートすると、データは TiKV にインポートされます。インポートが完了したら、SQL ステートメントを使用して、どのテーブルをTiFlashにレプリケートするかを指定できます。次に、TiDB はそれに応じて指定されたテーブルのレプリカをTiFlashに作成します。詳細については、 [TiFlashレプリカの作成](/tiflash/create-tiflash-replicas.md)を参照してください。

### TiFlashデータを CSV 形式でエクスポートできますか? {#can-i-export-tiflash-data-in-the-csv-format}

いいえTiFlashデータはエクスポートできません。

## セキュリティに関するよくある質問 {#security-faqs}

### TiDB はどのようにしてデータのプライバシーを保護し、セキュリティを確保しますか? {#how-does-tidb-protect-data-privacy-and-ensure-security}

Transport Layer Security (TLS) と透過的データ暗号化 (TDE) は、保存時の暗号化のために含まれています。 2 つの異なるネットワーク プレーンがあります。TiDBサーバーへのアプリケーションとデータ通信用のプレーンです。証明書の検証用のサブジェクト代替名と内部通信用の TLS コンテキストを比較するための拡張構文が含まれています。

### VPC でTiDB Cloudを実行できますか? {#can-tidb-cloud-run-in-our-vpc}

いいえTiDB Cloudは PingCAP VPC で実行されますが、データとトラフィックはデフォルトで暗号化されます。したがって、データのプライバシーの問題について心配する必要はありません。

## サポートFAQ {#support-faq}

### 顧客はどのようなサポートを利用できますか? {#what-support-is-available-for-customers}

TiDB Cloudは、金融サービス、e コマース、エンタープライズ アプリケーション、ゲームなどの業界の 1500 を超えるグローバル企業のミッション クリティカルなユース ケースを実行してきた TiDB の背後にある同じチームによってサポートされています。 TiDB Cloudは、ユーザーごとに無料の基本サポート プランを提供し、拡張サービスの有料プランにアップグレードできます。詳細については、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)を参照してください。
