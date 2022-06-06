---
title: TiDB Cloud FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud.
---

# TiDBクラウドに関するFAQ {#tidb-cloud-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDBCloudに関して最もよくある質問がリストされています。

## TiDBクラウドとは何ですか？ {#what-is-tidb-cloud}

TiDB Cloudは、直感的なコンソールを介して制御するフルマネージドクラウドインスタンスを使用して、TiDBクラスターの展開、管理、および保守をさらに簡単にします。アマゾンウェブサービスまたはGoogleCloudに簡単にデプロイして、ミッションクリティカルなアプリケーションをすばやく構築できます。

TiDB Cloudを使用すると、トレーニングをほとんどまたはまったく受けていない開発者とDBAは、インフラストラクチャ管理やクラスタ展開などのかつては複雑だったタスクを簡単に処理し、データベースの複雑さではなく、アプリケーションに集中できます。また、ボタンをクリックするだけでTiDBクラスターをスケールインまたはスケールアウトすることで、必要な量と期間のデータベースを正確にプロビジョニングできるため、コストのかかるリソースを無駄にすることがなくなります。

## TiDBとTiDBCloudの関係は何ですか？ {#what-is-the-relationship-between-tidb-and-tidb-cloud}

TiDBはオープンソースデータベースであり、自社のデータセンター、自己管理型クラウド環境、またはその2つのハイブリッドでオンプレミスでTiDBを実行したい組織に最適なオプションです。

TiDB Cloudは、TiDBのサービスとしてのフルマネージドクラウドデータベースです。使いやすいWebベースの管理コンソールを備えているため、ミッションクリティカルな本番環境のTiDBクラスターを管理できます。

## TiDB CloudはMySQLと互換性がありますか？ {#is-tidb-cloud-compatible-with-mysql}

現在、TiDB Cloudは、トリガー、ストアドプロシージャ、ユーザー定義関数、および外部キーを除いて、MySQL5.7構文の大部分をサポートしています。詳細については、 [MySQLとの互換性](https://docs.pingcap.com/tidb/stable/mysql-compatibility)を参照してください。

## TiDB Cloudを操作するために使用できるプログラミング言語は何ですか？ {#what-programming-languages-can-i-use-to-work-with-tidb-cloud}

MySQLクライアントまたはドライバーでサポートされている任意の言語を使用できます。

## TiDB Cloudはどこで実行できますか？ {#where-can-i-run-tidb-cloud}

TiDB Cloudは現在、AmazonWebServicesとGoogleCloudで利用できます。

## TiDB CloudでサポートされているTiDBのバージョンは何ですか？ {#what-versions-of-tidb-are-supported-on-tidb-cloud}

現在サポートされているTiDBバージョンについては、 [TiDBクラウドリリースノート](/tidb-cloud/release-notes-2022.md)を参照してください。

## TiDB Cloudについて詳しく知るにはどうすればよいですか？ {#how-can-i-learn-more-about-tidb-cloud}

TiDB Cloudについて学ぶ最良の方法は、ステップバイステップのチュートリアルに従うことです。開始するには、次のトピックを確認してください。

-   [TiDBクラウドの紹介](/tidb-cloud/tidb-cloud-intro.md)
-   [はじめに](/tidb-cloud/tidb-cloud-quickstart.md)
-   [TiDBクラスターを作成する](/tidb-cloud/create-tidb-cluster.md)

## どの企業が本番環境でTiDBまたはTiDBCloudを使用していますか？ {#what-companies-are-using-tidb-or-tidb-cloud-in-production}

TiDBは、金融サービス、ゲーム、eコマースなどのさまざまな業界の1500を超えるグローバル企業から信頼されています。ユーザーには、Square（米国）、PayPay（日本）、Shopee（シンガポール）、China UnionPay（中国）が含まれます。具体的な詳細については、 [ケーススタディ](https://en.pingcap.com/customers/)を参照してください。

## TiDBクラウドはどのようにして高可用性を保証しますか？ {#how-does-tidb-cloud-ensure-high-availability}

TiDBは、Raftコンセンサスアルゴリズムを使用して、データの可用性が高く、Raftグループのストレージ全体に安全に複製されるようにします。データはTiKVノード間で冗長的にコピーされ、マシンまたはデータセンターの障害から保護するために異なるアベイラビリティーゾーンに配置されます。自動フェイルオーバーにより、TiDBはサービスが常にオンになっていることを保証します。

Software as a Service（SaaS）プロバイダーとして、私たちはデータセキュリティを真剣に受け止めています。私たちは、 [サービス組織管理（SOC）2タイプ1コンプライアンス](https://pingcap.com/blog/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud)が要求する厳格な情報セキュリティポリシーと手順を確立しました。これにより、データの安全性、可用性、機密性が確保されます。

## お客様はどのようなサポートを利用できますか？ {#what-support-is-available-for-customers}

TiDB Cloudは、金融サービス、eコマース、エンタープライズアプリケーション、ゲームなど、業界全体で1500を超えるグローバル企業向けにミッションクリティカルなユースケースを実行しているTiDBの背後にある同じチームによってサポートされています。 TiDBCloudユーザーは24時間年中無休でサポートを利用できます。

## 私のTiDBクラスターにはさまざまなコンポーネントがあります。 PD、TiDB、TiKV、およびTiFlashノードとは何ですか？ {#there-are-different-components-in-my-tidb-cluster-what-are-pd-tidb-tikv-and-tiflash-nodes}

PD、配置ドライバーは、クラスタのメタデータを格納するため、TiDBクラスタ全体の「頭脳」です。 TiKVノードからリアルタイムで報告されたデータ配信状態に応じて、特定のTiKVノードにデータスケジューリングコマンドを送信します。

TiDBは、TiKVまたはTiFlashストアから返されたクエリからのデータを集約するSQLコンピューティングレイヤーです。 TiDBは水平方向にスケーラブルです。 TiDBノードの数を増やすと、クラスタが処理できる同時クエリの数が増えます。

TiKVは、OLTPデータを格納するために使用されるトランザクションストアです。 TiKVのすべてのデータは、複数のレプリカ（デフォルトでは3つのレプリカ）で自動的に維持されるため、TiKVはネイティブの高可用性を備え、自動フェイルオーバーをサポートします。 TiKVは水平方向にスケーラブルです。トランザクションストアの数を増やすと、OLTPスループットが向上します。

TiFlashは、トランザクションストア（TiKV）からのデータをリアルタイムで複製し、リアルタイムのOLAPワークロードをサポートする分析ストレージです。 TiKVとは異なり、TiFlashは分析処理を高速化するためにデータを列に格納します。 TiFlashは水平方向にもスケーラブルです。 TiFlashノードを増やすと、OLAPストレージとコンピューティング容量が増えます。

## TiDBはTiKVノード間でどのようにデータを複製しますか？ {#how-does-tidb-replicate-data-between-the-tikv-nodes}

TiKVは、キー値スペースをキー範囲に分割し、各キー範囲は「領域」として扱われます。 TiKVでは、データはクラスタのすべてのノードに分散され、リージョンを基本単位として使用します。 PDは、クラスタのすべてのノードにリージョンを可能な限り均等に分散（スケジューリング）する責任があります。

TiDBは、Raftコンセンサスアルゴリズムを使用して、リージョンごとにデータを複製します。異なるノードに格納されているリージョンの複数のレプリカは、ラフトグループを形成します。

各データ変更は、Raftログとして記録されます。 Raftログレプリケーションにより、データはRaftグループの複数のノードに安全かつ確実にレプリケートされます。

## TiDB CloudのHTAP機能を利用するにはどうすればよいですか？ {#how-do-i-make-use-of-tidb-cloud-s-htap-capabilities}

従来、データベースには、オンライントランザクション処理（OLTP）データベースとオンライン分析処理（OLAP）データベースの2種類があります。 OLTPおよびOLAP要求は、多くの場合、異なる分離されたデータベースで処理されます。この従来のアーキテクチャでは、OLTPデータベースからOLAPのデータウェアハウスまたはデータレイクにデータを移行することは、長くてエラーが発生しやすいプロセスです。

ハイブリッドトランザクション分析処理（HTAP）データベースとして、TiDB Cloudは、OLTP（TiKV）ストアとOLAP（TiFlash）の間でデータを自動的に確実に複製することにより、システムアーキテクチャを簡素化し、メンテナンスの複雑さを軽減し、トランザクションデータのリアルタイム分析をサポートします。お店。典型的なHTAPの使用例は、ユーザーのパーソナライズ、AIの推奨、不正の検出、ビジネスインテリジェンス、およびリアルタイムのレポートです。

その他のHTAPシナリオについては、 [データプラットフォームを簡素化するHTAPデータベースの構築方法](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)を参照してください。

## 別のRDBMSからTiDBCloudへの簡単な移行パスはありますか？ {#is-there-an-easy-migration-path-from-another-rdbms-to-tidb-cloud}

TiDBは、MySQLデータベースからデータを移行するためのTiDBLightningとデータ移行ツールを提供します。 TiDBはMySQLワイヤープロトコルを実装しており、MySQLクライアントをTiDBに使用できます。また、Java、Go、Rust、Pythonなどのプログラミング言語でTiKVAPIを使用してデータにアクセスすることもできます。

## TiDBはどのようにしてデータのプライバシーを保護し、セキュリティを確保しますか？ {#how-does-tidb-protect-data-privacy-and-ensure-security}

保管時の暗号化には、トランスポート層セキュリティ（TLS）と透過的データ暗号化（TDE）が含まれています。 2つの異なるネットワークプレーンがあります。TiDBサーバーへのアプリケーションとデータ通信用のプレーンです。証明書の検証用のサブジェクト代替名と内部通信用のTLSコンテキストを比較するための拡張構文が含まれています。
