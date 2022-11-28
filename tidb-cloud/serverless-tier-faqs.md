---
title: Serverless Tier FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud Serverless Tier.
---

# サーバーレス層に関するよくある質問 {#serverless-tier-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、 TiDB Cloud Tier に関して最もよく寄せられる質問の一覧を示します。

## 一般的なよくある質問 {#general-faqs}

### サーバーレス層とは何ですか? {#what-is-serverless-tier}

TiDB Cloud Tier は、完全な HTAP 機能を備えた TiDB データベースをあなたとあなたの組織に提供します。これは、TiDB の完全に管理された自動スケーリング展開であり、データベースの使用をすぐに開始し、基盤となるノードを気にせずにアプリケーションを開発および実行し、アプリケーションのワークロードの変化に基づいて自動的にスケーリングできます。

### サーバーレス層の使用を開始するにはどうすればよいですか? {#how-do-i-get-started-with-serverless-tier}

5 分間の[TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md)から始めます。

### ベータ期間中、サーバーレス層は無料ですか? {#is-serverless-tier-free-during-beta}

はい。 Serverless Tier は、ベータ段階では無料で使用できます。今後数か月以内に、無料のスターター プランの提供を継続しながら、追加のリソースとパフォーマンスの向上のために使用量ベースの課金プランを提供する予定です。

### ベータ版リリースとはどういう意味ですか? {#what-does-it-mean-for-beta-release}

Serverless Tier はベータ版であり、一般公開される前に新しい機能を継続的に追加し、既存の機能を改善しています。ベータ版製品には SLA を提供しません。したがって、サーバーレス層は現在、本番環境では使用し**ない**でください。

### 無料ベータ版の Serverless Tier クラスターにはどのような制限がありますか? {#what-are-the-limitations-of-a-serverless-tier-cluster-in-free-beta}

-   TiDB Cloudアカウントごとに、ベータ段階で無料のサーバーレス層クラスターを 1 つ作成できます。新しい Serverless Tier クラスターを作成するには、最初に既存のクラスターを削除する必要があります。
-   各サーバーレス層クラスターには次の制限があります。
    -   ストレージ サイズは、OLTP ストレージの 5 GiB (論理サイズ) と OLAP ストレージの 5 GiB に制限されています。
    -   コンピューティング リソースは、1 つの vCPU と 1 GiB RAM に制限されています。
    -   **注**: 今後数か月以内に、無料のスターター プランの提供を継続しながら、リソースの追加とパフォーマンスの向上のために使用量ベースの課金プランを提供する予定です。今後のリリースでは、無料のサーバーレス層の制限が変更される可能性があります。
-   一部のTiDB Cloud機能は、サーバーレス層では部分的にサポートされているか、サポートされていません。詳細は[サーバーレス層の制限](/tidb-cloud/serverless-tier-limitations.md)を参照してください。

### Serverless Tier は何に使用できますか? {#what-can-serverless-tier-be-used-for}

サーバーレス層クラスターは、プロトタイプ アプリケーション、開発環境、ハッカソン、アカデミック コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

### Serverless Tier が利用可能になる前に、Developer Tier クラスターを作成しました。クラスターを引き続き使用できますか? {#i-created-a-developer-tier-cluster-before-serverless-tier-was-available-can-i-still-use-my-cluster}

はい、無料の Developer Tier クラスターは、まもなく Serverless Tier クラスターに自動的に移行されます。クラスターを使用する機能に影響はなく、同じようにサーバーレス層のユーザー エクスペリエンスが向上します。

## セキュリティに関するよくある質問 {#security-faqs}

### サーバーレス ティアは共有ですか、それとも専用ですか? {#is-my-serverless-tier-shared-or-dedicated}

サーバーレス テクノロジはマルチテナンシー向けに設計されており、すべてのクラスターで使用されるリソースが共有されます。分離されたインフラストラクチャとリソースを備えたマネージド TiDB サービスを取得するには、それを[専用ティア](/tidb-cloud/select-cluster-tier.md#dedicated-tier)にアップグレードできます。

### TiDB Serverless Tier はどのようにセキュリティを確保しますか? {#how-does-tidb-serverless-tier-ensure-security}

-   接続はトランスポート レイヤー セキュリティ (TLS) によって暗号化されます。 TLS を使用してサーバーレス層に接続する方法の詳細については、 [サーバーレス層クラスターへのセキュリティ接続](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)を参照してください。
-   Serverless Tier で保持されるすべてのデータは、クラスターが実行されているクラウド プロバイダーのツールを使用して保存時に暗号化されます。

## メンテナンスFAQ {#maintenance-faq}

### クラスターが実行されている TiDB のバージョンをアップグレードできますか? {#can-i-upgrade-the-version-of-tidb-that-my-cluster-is-running-on}

いいえTiDB Cloudで新しい TiDB バージョンを展開すると、サーバーレス層クラスターは自動的にアップグレードされます。 [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)または最新の[リリースノート](https://docs.pingcap.com/tidbcloud/release-notes)で、クラスターが実行している TiDB のバージョンを確認できます。または、クラスターに接続し、 `SELECT version()`または`SELECT tidb_version()`を使用して TiDB のバージョンを確認することもできます。
