---
title: Developer Guide Overview
summary: Introduce the overview of the developer guide.
---

# 開発者ガイドの概要 {#developer-guide-overview}

このガイドはアプリケーション開発者向けに書かれていますが、TiDB の内部動作に興味がある場合、または TiDB 開発に参加したい場合は、TiDB の詳細については[<a href="https://pingcap.github.io/tidb-dev-guide/">TiDB カーネル開発ガイド</a>](https://pingcap.github.io/tidb-dev-guide/)をお読みください。

<CustomContent platform="tidb">

このチュートリアルでは、TiDB を使用してアプリケーションを迅速に構築する方法、TiDB の考えられる使用例、および一般的な問題の処理方法を示します。

このページを読む前に、 [<a href="/quick-start-with-tidb.md">TiDB データベース プラットフォームのクイック スタート ガイド</a>](/quick-start-with-tidb.md)を読んでおくことをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

このチュートリアルでは、 TiDB Cloudを使用してアプリケーションを迅速に構築する方法、 TiDB Cloudの考えられる使用例、および一般的な問題の処理方法を示します。

</CustomContent>

## TiDB の基本 {#tidb-basics}

TiDB の使用を開始する前に、TiDB がどのように機能するかに関するいくつかの重要なメカニズムを理解する必要があります。

-   TiDB でトランザクションがどのように機能するかを理解するには[<a href="/transaction-overview.md">TiDBトランザクションの概要</a>](/transaction-overview.md)を読んでください。アプリケーション開発に必要なトランザクションの知識については[<a href="/develop/dev-guide-transaction-overview.md">アプリケーション開発者向けのトランザクションノート</a>](/develop/dev-guide-transaction-overview.md)を確認してください。
-   [<a href="#the-way-applications-interact-with-tidb">アプリケーションが TiDB と対話する方法</a>](#the-way-applications-interact-with-tidb)を理解する。
-   分散データベース TiDB およびTiDB Cloudを構築するためのコア コンポーネントと概念を学習するには、無料のオンライン コース[<a href="https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide">TiDB の概要</a>](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)を参照してください。

## TiDB トランザクション メカニズム {#tidb-transaction-mechanisms}

TiDB は分散トランザクションをサポートし、 [<a href="/optimistic-transaction.md">楽観的取引</a>](/optimistic-transaction.md)と[<a href="/pessimistic-transaction.md">悲観的取引</a>](/pessimistic-transaction.md)の両方のモードを提供します。 TiDB の現在のバージョンは、デフォルトで**悲観的トランザクション**モードを使用します。これにより、従来のモノリシック データベース (MySQL など) と同じように TiDB でトランザクションを実行できます。

[<a href="/sql-statements/sql-statement-begin.md">`BEGIN`</a>](/sql-statements/sql-statement-begin.md)を使用してトランザクションを開始するか、 `BEGIN PESSIMISTIC`使用して**悲観的トランザクションを**明示的に指定するか、 `BEGIN OPTIMISTIC`使用して**楽観的トランザクション**を明示的に指定できます。その後、トランザクションをコミット ( [<a href="/sql-statements/sql-statement-commit.md">`COMMIT`</a>](/sql-statements/sql-statement-commit.md) ) またはロールバック ( [<a href="/sql-statements/sql-statement-rollback.md">`ROLLBACK`</a>](/sql-statements/sql-statement-rollback.md) ) することができます。

TiDB は、 `BEGIN`の開始から`COMMIT`または`ROLLBACK`の終了までのすべてのステートメントのアトミック性を保証します。つまり、この期間中に実行されるすべてのステートメントは、全体として成功するか失敗します。これは、アプリケーション開発に必要なデータの一貫性を確保するために使用されます。

<CustomContent platform="tidb">

**楽観的トランザクションが**何であるかわからない場合は、まだ使用し***ない***でください。**楽観的トランザクション**では、アプリケーションが`COMMIT`ステートメントによって返される[<a href="/error-codes.md">すべてのエラー</a>](/error-codes.md)正しく処理できる必要があるためです。アプリケーションがそれらをどのように処理するかわからない場合は、代わりに**悲観的トランザクション**を使用してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

**楽観的トランザクションが**何であるかわからない場合は、まだ使用し***ない***でください。**楽観的トランザクション**では、アプリケーションが`COMMIT`ステートメントによって返される[<a href="https://docs.pingcap.com/tidb/stable/error-codes">すべてのエラー</a>](https://docs.pingcap.com/tidb/stable/error-codes)正しく処理できる必要があるためです。アプリケーションがそれらをどのように処理するかわからない場合は、代わりに**悲観的トランザクション**を使用してください。

</CustomContent>

## アプリケーションが TiDB と対話する方法 {#the-way-applications-interact-with-tidb}

TiDB は MySQL プロトコルとの互換性が高く、 [<a href="/mysql-compatibility.md">ほとんどの MySQL 構文と機能</a>](/mysql-compatibility.md)をサポートしているため、ほとんどの MySQL 接続ライブラリは TiDB と互換性があります。アプリケーション フレームワークまたは言語が PingCAP から正式に適応されていない場合は、MySQL のクライアント ライブラリを使用することをお勧めします。 TiDB のさまざまな機能を積極的にサポートするサードパーティ ライブラリが増えています。

TiDB は MySQL プロトコルおよび MySQL 構文と互換性があるため、MySQL をサポートするほとんどの ORM も TiDB と互換性があります。

## 続きを読む {#read-more}

<CustomContent platform="tidb">

-   [<a href="/develop/dev-guide-build-cluster-in-cloud.md">クイックスタート</a>](/develop/dev-guide-build-cluster-in-cloud.md)
-   [<a href="/develop/dev-guide-choose-driver-or-orm.md">Driverまたは ORM を選択してください</a>](/develop/dev-guide-choose-driver-or-orm.md)
-   [<a href="/develop/dev-guide-connect-to-tidb.md">TiDB に接続する</a>](/develop/dev-guide-connect-to-tidb.md)
-   [<a href="/develop/dev-guide-schema-design-overview.md">データベーススキーマの設計</a>](/develop/dev-guide-schema-design-overview.md)
-   [<a href="/develop/dev-guide-insert-data.md">データの書き込み</a>](/develop/dev-guide-insert-data.md)
-   [<a href="/develop/dev-guide-get-data-from-single-table.md">データの読み取り</a>](/develop/dev-guide-get-data-from-single-table.md)
-   [<a href="/develop/dev-guide-transaction-overview.md">トランザクション</a>](/develop/dev-guide-transaction-overview.md)
-   [<a href="/develop/dev-guide-optimize-sql-overview.md">最適化</a>](/develop/dev-guide-optimize-sql-overview.md)
-   [<a href="/develop/dev-guide-sample-application-java-spring-boot.md">アプリケーション例</a>](/develop/dev-guide-sample-application-java-spring-boot.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [<a href="/develop/dev-guide-build-cluster-in-cloud.md">クイックスタート</a>](/develop/dev-guide-build-cluster-in-cloud.md)
-   [<a href="/develop/dev-guide-choose-driver-or-orm.md">Driverまたは ORM を選択してください</a>](/develop/dev-guide-choose-driver-or-orm.md)
-   [<a href="/develop/dev-guide-schema-design-overview.md">データベーススキーマの設計</a>](/develop/dev-guide-schema-design-overview.md)
-   [<a href="/develop/dev-guide-insert-data.md">データの書き込み</a>](/develop/dev-guide-insert-data.md)
-   [<a href="/develop/dev-guide-get-data-from-single-table.md">データの読み取り</a>](/develop/dev-guide-get-data-from-single-table.md)
-   [<a href="/develop/dev-guide-transaction-overview.md">トランザクション</a>](/develop/dev-guide-transaction-overview.md)
-   [<a href="/develop/dev-guide-optimize-sql-overview.md">最適化</a>](/develop/dev-guide-optimize-sql-overview.md)
-   [<a href="/develop/dev-guide-sample-application-java-spring-boot.md">アプリケーション例</a>](/develop/dev-guide-sample-application-java-spring-boot.md)

</CustomContent>
