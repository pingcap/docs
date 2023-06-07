---
title: TiDB Serverless FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Serverless.
---

# TiDB サーバーレスに関するよくある質問 {#tidb-serverless-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDB サーバーレスに関して最もよくある質問がリストされています。

## 一般的な FAQ {#general-faqs}

### TiDB サーバーレスとは​​何ですか? {#what-is-tidb-serverless}

TiDB サーバーレスは、あなたとあなたの組織に、完全な HTAP 機能を備えた TiDB データベースを提供します。これは TiDB のフルマネージドで自動スケーリングのデプロイメントであり、データベースの使用をすぐに開始し、基盤となるノードを気にせずにアプリケーションを開発および実行し、アプリケーションのワークロードの変化に基づいて自動的にスケーリングすることができます。

### TiDB サーバーレスを使い始めるにはどうすればよいですか? {#how-do-i-get-started-with-tidb-serverless}

5 分間から始めましょう[<a href="/tidb-cloud/tidb-cloud-quickstart.md">TiDB Cloudクイック スタート</a>](/tidb-cloud/tidb-cloud-quickstart.md) 。

### TiDB サーバーレスはベータ版の間は無料ですか? {#is-tidb-serverless-free-during-beta}

2023 年 5 月 31 日まで、TiDB サーバーレス クラスターは引き続き無料で、100% 割引です。それ以降、無料枠を超えた使用には料金が発生します。クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、新しい月の初めに使用量が[<a href="/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit">割り当てを増やす</a>](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit)されるまでスロットルされます。

詳細については、 [<a href="/tidb-cloud/select-cluster-tier.md#usage-quota">TiDB サーバーレスの使用量割り当て</a>](/tidb-cloud/select-cluster-tier.md#usage-quota)を参照してください。

### ベータ版リリースとは何を意味しますか? {#what-does-it-mean-for-beta-release}

TiDB Serverless はベータ版であり、一般公開される前に継続的に新機能の追加と既存の機能の改善を行っています。ベータ製品には SLA は提供されません。したがって、TiDB サーバーレスは現在本番で使用し**ない**でください。

### ベータ版の TiDB サーバーレス クラスターの制限は何ですか? {#what-are-the-limitations-of-a-tidb-serverless-cluster-in-beta}

TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB サーバーレス クラスターを作成できます。さらに TiDB サーバーレス クラスターを作成するには、クレジット カードを追加し、使用量を[<a href="/tidb-cloud/tidb-cloud-glossary.md#spend-limit">支出制限</a>](/tidb-cloud/tidb-cloud-glossary.md#spend-limit)に設定する必要があります。

TiDB Cloud機能の一部は、TiDB サーバーレスで部分的にサポートされているか、サポートされていません。詳細については[<a href="/tidb-cloud/serverless-tier-limitations.md">TiDB サーバーレスの制限とクォータ</a>](/tidb-cloud/serverless-tier-limitations.md)を参照してください。

### TiDB サーバーレスは何に使用できますか? {#what-can-tidb-serverless-be-used-for}

TiDB サーバーレス クラスターは、プロトタイプ アプリケーション、開発環境、ハッカソン、学術コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

### TiDB サーバーレスが利用可能になる前に、Developer Tierクラスターを作成しました。クラスターを引き続き使用できますか? {#i-created-a-developer-tier-cluster-before-tidb-serverless-was-available-can-i-still-use-my-cluster}

はい、Developer Tierクラスターは間もなく TiDB サーバーレス クラスターに自動的に移行されます。クラスターを使用する能力には影響はなく、同様に改善された TiDB サーバーレス ユーザー エクスペリエンスが得られます。

## Securityよくある質問 {#security-faqs}

### 私の TiDB サーバーレスは共有ですか、それとも専用ですか? {#is-my-tidb-serverless-shared-or-dedicated}

サーバーレス テクノロジーはマルチテナンシー向けに設計されており、すべてのクラスターで使用されるリソースが共有されます。分離されたインフラストラクチャとリソースを使用してマネージド TiDB サービスを利用するには、サービスを[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">TiDB専用</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)にアップグレードします。

### TiDB サーバーレスはどのようにセキュリティを確保しますか? {#how-does-tidb-serverless-ensure-security}

-   接続は Transport Layer Security (TLS) によって暗号化されます。 TLS を使用して TiDB サーバーレスに接続する方法の詳細については、 [<a href="/tidb-cloud/secure-connections-to-serverless-tier-clusters.md">TiDB サーバーレスへの TLS 接続</a>](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)を参照してください。
-   TiDB サーバーレス上のすべての永続データは、クラスターが実行されているクラウド プロバイダーのツールを使用して保存時に暗号化されます。

## メンテナンスに関するFAQ {#maintenance-faq}

### クラスターが実行されている TiDB のバージョンをアップグレードできますか? {#can-i-upgrade-the-version-of-tidb-that-my-cluster-is-running-on}

いいえ。TiDB サーバーレス クラスターは、 TiDB Cloudで新しい TiDB バージョンを展開すると自動的にアップグレードされます。クラスターが実行している TiDB のバージョンは[<a href="https://tidbcloud.com/console/clusters">TiDB Cloudコンソール</a>](https://tidbcloud.com/console/clusters)または最新の[<a href="https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes">リリースノート</a>](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes)で確認できます。あるいは、クラスターに接続し、 `SELECT version()`または`SELECT tidb_version()`を使用して TiDB バージョンを確認することもできます。
