---
title: Serverless Tier FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud Serverless Tier.
---

# Serverless Tierよくある質問 {#serverless-tier-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、 TiDB Cloud Serverless Tierに関して最もよく寄せられる質問を一覧表示します。

## 一般的なよくある質問 {#general-faqs}

### Serverless Tierとは? {#what-is-serverless-tier}

TiDB Cloud Serverless Tier は、完全な HTAP 機能を備えた TiDB データベースをあなたとあなたの組織に提供します。これは、TiDB の完全に管理された自動スケーリング展開であり、データベースの使用をすぐに開始し、基盤となるノードを気にせずにアプリケーションを開発および実行し、アプリケーションのワークロードの変化に基づいて自動的にスケーリングできます。

### Serverless Tierの使用を開始するにはどうすればよいですか? {#how-do-i-get-started-with-serverless-tier}

5 分間の[TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md)から始めます。

### ベータ期間中、Serverless Tierは無料ですか? {#is-serverless-tier-free-during-beta}

2023 年 5 月 30 日まで、Serverless Tierクラスターは引き続き無料で、100% 割引になります。それ以降は、無料枠を超えた分は課金されます。クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、 [クォータを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit)または新しい月の開始時に使用量がリセットされるまで調整されます。

詳細については、 [Serverless Tierの使用量割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)を参照してください。

### ベータ版リリースとはどういう意味ですか? {#what-does-it-mean-for-beta-release}

Serverless Tierはベータ版であり、一般公開される前に新しい機能を継続的に追加し、既存の機能を改善しています。ベータ版製品には SLA を提供しません。したがって、Serverless Tierは現在、本番では使用し**ない**でください。

### ベータ版のServerless Tierクラスターにはどのような制限がありますか? {#what-are-the-limitations-of-a-serverless-tier-cluster-in-beta}

TiDB Cloudの組織ごとに、デフォルトで最大 5 つのServerless Tierクラスターを作成できます。さらにServerless Tierクラスターを作成するには、クレジット カードを追加し、使用量を[使用制限](/tidb-cloud/tidb-cloud-glossary.md#spend-limit)に設定する必要があります。

一部のTiDB Cloud機能は、Serverless Tierで部分的にサポートされているか、サポートされていません。詳細は[Serverless Tierの制限と割り当て](/tidb-cloud/serverless-tier-limitations.md)を参照してください。

### Serverless Tier は何に使用できますか? {#what-can-serverless-tier-be-used-for}

Serverless Tierクラスターは、プロトタイプ アプリケーション、開発環境、ハッカソン、アカデミック コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

### Serverless Tier が利用可能になる前に、 Developer Tierクラスターを作成しました。クラスターを引き続き使用できますか? {#i-created-a-developer-tier-cluster-before-serverless-tier-was-available-can-i-still-use-my-cluster}

はい、 Developer TierクラスターはまもなくServerless Tierクラスターに自動的に移行されます。クラスターを使用する機能に影響はなく、同じようにServerless Tierのユーザー エクスペリエンスが向上します。

## Securityよくある質問 {#security-faqs}

### Serverless Tierは共有ですか、それとも専用ですか? {#is-my-serverless-tier-shared-or-dedicated}

サーバーレス テクノロジはマルチテナンシー向けに設計されており、すべてのクラスターで使用されるリソースが共有されます。分離されたインフラストラクチャとリソースを備えたマネージド TiDB サービスを取得するには、それを[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)にアップグレードできます。

### TiDB Serverless Tier はどのようにセキュリティを確保しますか? {#how-does-tidb-serverless-tier-ensure-security}

-   接続はトランスポート レイヤーSecurity(TLS) によって暗号化されます。 TLS を使用してServerless Tierに接続する方法の詳細については、 [Serverless Tierへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)を参照してください。
-   Serverless Tierで保持されるすべてのデータは、クラスターが実行されているクラウド プロバイダーのツールを使用して保存時に暗号化されます。

## メンテナンスに関するFAQ {#maintenance-faq}

### クラスターが実行されている TiDB のバージョンをアップグレードできますか? {#can-i-upgrade-the-version-of-tidb-that-my-cluster-is-running-on}

いいえTiDB Cloudで新しい TiDB バージョンを展開すると、Serverless Tierクラスターは自動的にアップグレードされます。 [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)または最新の[リリースノート](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes)で、クラスターが実行している TiDB のバージョンを確認できます。または、クラスターに接続し、 `SELECT version()`または`SELECT tidb_version()`を使用して TiDB のバージョンを確認することもできます。
