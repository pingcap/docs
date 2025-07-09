---
title: PingCAP Documentation
hide_sidebar: true
hide_commit: true
hide_leftNav: true
summary: TiDBドキュメントでは、データ移行やアプリケーション構築など、 TiDB CloudとTiDB Self-Managedの使用方法に関するガイドとリファレンスを提供しています。TiDB TiDB Cloudは、クラウドネイティブな分散SQLデータベースのパワーに簡単にアクセスできる、フルマネージドのDatabase-as-a-Service（データベース・アズ・ア・サービス）です。TiDBは、MySQLとの互換性、水平スケーラビリティ、高可用性を備えたオープンソースの分散SQLデータベースです。開発者は、アプリケーション開発に関するドキュメントにアクセスしたり、TiDB Playground、PingCAP Education、コミュニティ参加の機会などの追加リソースを活用したりできます。
---

<DocHomeContainer title="TiDB ドキュメント" subTitle="Explore the how-to guides and references you need to use {{{ .starter }}}, TiDB Cloud Dedicated and TiDB Self-Managed, migrate data, and build your applications on the database." ctaLabel="Start {{{ .starter }}} for Free" ctaLink="https://tidbcloud.com/free-trial">

<DocHomeSection label="TiDB Cloud" anchor="tidb-cloud" id="tidb-cloud">

TiDB Cloud は、TiDB の優れた機能すべてをクラウドに提供する、完全に管理された Database-as-a-Service (DBaaS) であり、データベースの複雑さではなくアプリケーションに集中できます。

<DocHomeCardContainer>

<DocHomeCard href="/tidbcloud/tidb-cloud-intro" label="What is TiDB Cloud" icon="cloud-product-mauve">

使いやすいデータベースとしてのTiDB Cloudとその主な機能について学びます。

</DocHomeCard>

<DocHomeCard href="/tidbcloud/tidb-cloud-quickstart" label="Get started with {{{ .starter }}}" icon="cloud-getstarted-mauve">

TiDB Cloudを簡単に使い始めるためのガイド。

</DocHomeCard>

<DocHomeCard href="/tidbcloud/dev-guide-overview" label="Developer Guide" icon="cloud-developer-mauve">

アプリケーションを好みの言語やフレームワークに接続します。

</DocHomeCard>

<DocHomeCard href="/tidbcloud/vector-search-overview" label="Vector Search in {{{ .starter }}} (Beta)" icon="cloud-vector-mauve">

AI アプリケーションを構築するには、 {{{{ .starter }}} の Vector Search のネイティブ サポートを調べてください。

</DocHomeCard>

</DocHomeCardContainer>

</DocHomeSection>

<DocHomeSection label="TiDB Self-Managed" anchor="tidb-self-managed" id="tidb-self-managed">

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

TiDBは、ハイブリッドトランザクションおよび分析処理（HTAP）ワークロードをサポートするオープンソースの分散SQLデータベースです。MySQLと互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。TiDBは、セルフホスト環境またはクラウド上に導入できます。

<DocHomeCardContainer>

<DocHomeCard href="/tidb/stable/overview" label="What is TiDB Self-Managed" icon="oss-product-blue">

TiDB Self-Managed とその主な機能について説明します。

</DocHomeCard>

<DocHomeCard href="/tidb/stable/quick-start-with-tidb" label="Get started with TiDB Self-Managed" icon="oss-getstarted-blue">

TiDB Self-Managed を使い始めるための最も簡単な方法を説明します。

</DocHomeCard>

<DocHomeCard href="/tidb/stable/production-deployment-using-tiup" label="Deploy a Local TiDB Cluster" icon="oss-deploy-blue">

本番環境で TiDB をローカルにデプロイする方法を学習します。

</DocHomeCard>

<DocHomeCard href="/tidb/stable/dev-guide-overview" label="Developer Guide" icon="oss-developer-blue">

TiDB Self-Managed を使用するアプリケーション開発者向け。

</DocHomeCard>

<DocHomeCard href="/tidb/stable/mysql-compatibility" label="MySQL Compatibility" icon="oss-mysql-blue">

TiDB は、MySQL プロトコルおよびMySQL 5.7と MySQL 8.0 の共通機能と構文と高い互換性があります。

</DocHomeCard>

<DocHomeCard href="/tidb/dev/tidb-roadmap" label="TiDB Self-Managed Roadmap" icon="oss-roadmap-blue">

TiDB Self-Managed の計画されている機能とリリース日。

</DocHomeCard>

</DocHomeCardContainer>

オープンソースの TiDB プラットフォームは Apache 2.0 ライセンスの下でリリースされ、コミュニティによってサポートされています[GitHubでビュー](https://github.com/pingcap/tidb)

</DocHomeSection>

<DocHomeSection label="More Resources" anchor="resources" id="resources">

<DocHomeCardContainer>

<DocHomeCard href="https://www.pingcap.com/education/" label="Learning Center" icon="global-tidb-education">

適切に設計されたオンライン コースとインストラクター主導のトレーニングを通じて、 TiDB Cloudと TiDB Self-Managed を学習します。

</DocHomeCard>

<DocHomeCard href="https://www.pingcap.com/blog/" label="Blog" icon="global-tidb-blog">

TiDB Cloudと TiDB Self-Managed に関する優れた記事をお読みください。

</DocHomeCard>

<DocHomeCard href="https://www.pingcap.com/event/" label="Events" icon="global-tidb-events">

PingCAP とコミュニティが主催するイベントについて学びます。

</DocHomeCard>

<DocHomeCard href="https://www.pingcap.com/ebook-whitepaper/" label="eBooks & Papers" icon="global-tidb-ebook">

電子書籍と論文をダウンロードしてください。

</DocHomeCard>

<DocHomeCard href="https://www.pingcap.com/videos/" label="Videos" icon="global-tidb-video">

TiDB とさまざまな使用例を説明する短いビデオのコンピレーションをご覧ください。

</DocHomeCard>

<DocHomeCard href="https://ossinsight.io/" label="OSS Insight" icon="global-tidb-ossinsight">

TiDB Cloudを活用した、あらゆる GitHub リポジトリの詳細な分析を提供する強力な洞察ツールです。

</DocHomeCard>

<DocHomeCard href="https://play.tidbcloud.com/?utm_source=docs&utm_medium=home_more_resources" label="Playground" icon="global-tidb-playground">

登録なしで TiDB の機能を体験してください。

</DocHomeCard>

<DocHomeCard href="https://discord.gg/DQZ2dy3cuc?utm_source=doc" label="Join our community on Discord" icon="global-tidb-discord" colspan="2" actionBtnLabel="Join Community" ctaGraphic="global-iso-hand">

Discord に参加するか、貢献者になってください。

</DocHomeCard>

</DocHomeCardContainer>

</DocHomeSection>

</DocHomeContainer>
