---
title: Serverless Tier FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud Serverless Tier.
---

# Serverless Tierよくある質問 {#serverless-tier-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、 TiDB CloudServerless Tierに関する最もよくある質問がリストされています。

## 一般的な FAQ {#general-faqs}

### Serverless Tierとは何ですか? {#what-is-serverless-tier}

TiDB CloudServerless Tierは、お客様とお客様の組織に、完全な HTAP 機能を備えた TiDB データベースを提供します。これは TiDB のフルマネージドで自動スケーリングのデプロイメントであり、データベースの使用をすぐに開始し、基盤となるノードを気にせずにアプリケーションを開発および実行し、アプリケーションのワークロードの変化に基づいて自動的にスケーリングすることができます。

### Serverless Tierの使用を開始するにはどうすればよいですか? {#how-do-i-get-started-with-serverless-tier}

5 分間から始めましょう[<a href="/tidb-cloud/tidb-cloud-quickstart.md">TiDB Cloudクイック スタート</a>](/tidb-cloud/tidb-cloud-quickstart.md) 。

### Serverless Tierはベータ期間中は無料ですか? {#is-serverless-tier-free-during-beta}

はい。Serverless Tierは、ベータ段階では無料で使用できます。今後数か月間、無料のスターター プランの提供を継続しながら、追加のリソースとより高いパフォーマンスを実現するための従量制の料金プランを提供する予定です。

### ベータ版リリースとは何を意味しますか? {#what-does-it-mean-for-beta-release}

Serverless Tierはベータ版であり、一般提供される前に継続的に新機能の追加と既存の機能の改善が行われます。ベータ製品には SLA は提供されません。したがって、Serverless Tierは現在本番では使用し**ない**でください。

### 無料ベータ版のServerless Tierクラスターの制限は何ですか? {#what-are-the-limitations-of-a-serverless-tier-cluster-in-free-beta}

-   TiDB Cloudアカウントごとに、ベータ段階で最大 5 つの無料のServerless Tierクラスターを作成できます。
-   各Serverless Tierクラスターには次の制限があります。
    -   storageサイズは、OLTPstorageの場合は 5 GiB (論理サイズ)、OLAPstorageの場合は 5 GiB に制限されます。
    -   コンピューティング リソースは 1 vCPU と 1 GiB RAM に制限されます。
    -   単一トランザクションの合計サイズは、ベータ段階ではServerless Tierで 10 MB 以下に設定されます。
    -   **注**: 今後数か月間、無料のスターター プランの提供を継続しながら、追加のリソースとより高いパフォーマンスを目的とした従量制の料金プランを提供する予定です。今後のリリースでは、無料のServerless Tierの制限が変更される可能性があります。
-   TiDB Cloud機能の一部は、Serverless Tierで部分的にサポートされているか、サポートされていません。詳細については[<a href="/tidb-cloud/serverless-tier-limitations.md">Serverless Tierの制限</a>](/tidb-cloud/serverless-tier-limitations.md)を参照してください。

### Serverless Tierは何に使用できますか? {#what-can-serverless-tier-be-used-for}

Serverless Tierクラスターは、プロトタイプ アプリケーション、開発環境、ハッカソン、学術コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

### Serverless Tierが利用可能になる前に、Developer Tierクラスターを作成しました。クラスターを引き続き使用できますか? {#i-created-a-developer-tier-cluster-before-serverless-tier-was-available-can-i-still-use-my-cluster}

はい、無料のDeveloper Tierクラスターは間もなくServerless Tierクラスターに自動的に移行されます。クラスターの使用能力には影響はなく、Serverless Tierのユーザー エクスペリエンスも同様に向上します。

## Securityよくある質問 {#security-faqs}

### 私のServerless Tierは共有ですか、それとも専用ですか? {#is-my-serverless-tier-shared-or-dedicated}

サーバーレス テクノロジーはマルチテナンシー向けに設計されており、すべてのクラスターで使用されるリソースが共有されます。分離されたインフラストラクチャとリソースを使用してマネージド TiDB サービスを利用するには、サービスを[<a href="/tidb-cloud/select-cluster-tier.md#dedicated-tier">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#dedicated-tier)にアップグレードできます。

### TiDBServerless Tierはセキュリティをどのように確保しますか? {#how-does-tidb-serverless-tier-ensure-security}

-   接続は Transport Layer Security (TLS) によって暗号化されます。 TLS を使用してServerless Tierに接続する方法の詳細については、 [<a href="/tidb-cloud/secure-connections-to-serverless-tier-clusters.md">Serverless Tierクラスターへのセキュリティ接続</a>](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)を参照してください。
-   Serverless Tier上のすべての永続化データは、クラスターが実行されているクラウド プロバイダーのツールを使用して保存時に暗号化されます。

## メンテナンスに関するFAQ {#maintenance-faq}

### クラスターが実行されている TiDB のバージョンをアップグレードできますか? {#can-i-upgrade-the-version-of-tidb-that-my-cluster-is-running-on}

いいえ。Serverless Tierクラスターは、 TiDB Cloudで新しい TiDB バージョンを展開すると自動的にアップグレードされます。クラスターが実行している TiDB のバージョンは[<a href="https://tidbcloud.com/console/clusters">TiDB Cloudコンソール</a>](https://tidbcloud.com/console/clusters)または最新の[<a href="https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes">リリースノート</a>](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes)で確認できます。あるいは、クラスターに接続し、 `SELECT version()`または`SELECT tidb_version()`を使用して TiDB バージョンを確認することもできます。
