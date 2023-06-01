---
title: Developer Guide Overview
summary: Introduce the overview of the developer guide.
---

# 開発者ガイドの概要 {#developer-guide-overview}

このガイドはアプリケーション開発者向けに書かれていますが、TiDB の内部動作に興味がある場合、または TiDB 開発に参加したい場合は、TiDB の詳細については[TiDB カーネル開発ガイド](https://pingcap.github.io/tidb-dev-guide/)をお読みください。

<CustomContent platform="tidb">

このチュートリアルでは、TiDB を使用してアプリケーションを迅速に構築する方法、TiDB の考えられる使用例、および一般的な問題の処理方法を示します。

このページを読む前に、 [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)を読んでおくことをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

このチュートリアルでは、 TiDB Cloudを使用してアプリケーションを迅速に構築する方法、 TiDB Cloudの考えられる使用例、および一般的な問題の処理方法を示します。

</CustomContent>

## TiDB の基本 {#tidb-basics}

TiDB の使用を開始する前に、TiDB がどのように機能するかに関するいくつかの重要なメカニズムを理解する必要があります。

-   TiDB でトランザクションがどのように機能するかを理解するには[アプリケーション開発者向けのトランザクションノート](/develop/dev-guide-transaction-overview.md)を確認してください。
-   [アプリケーションが TiDB と対話する方法](#the-way-applications-interact-with-tidb)を理解する。
-   分散データベース TiDB およびTiDB Cloudを構築するためのコア コンポーネントと概念を学習するには、無料のオンライン コース[TiDB の概要](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)を参照してください。

## TiDB トランザクション メカニズム {#tidb-transaction-mechanisms}

TiDB は分散トランザクションをサポートし、 [悲観的取引](/pessimistic-transaction.md)の両方のモードを提供します。 TiDB の現在のバージョンは、デフォルトで**悲観的トランザクション**モードを使用します。これにより、従来のモノリシック データベース (MySQL など) と同じように TiDB でトランザクションを実行できます。

[`ROLLBACK`](/sql-statements/sql-statement-rollback.md) ) することができます。

TiDB は、 `BEGIN`の開始から`COMMIT`または`ROLLBACK`の終了までのすべてのステートメントのアトミック性を保証します。つまり、この期間中に実行されるすべてのステートメントは、全体として成功するか失敗します。これは、アプリケーション開発に必要なデータの一貫性を確保するために使用されます。

<CustomContent platform="tidb">

**楽観的トランザクションが**何であるかわからない場合は、まだ使用し***ない***でください。**楽観的トランザクション**では、アプリケーションが`COMMIT`ステートメントによって返される[すべてのエラー](/error-codes.md)正しく処理できる必要があるためです。アプリケーションがそれらをどのように処理するかわからない場合は、代わりに**悲観的トランザクション**を使用してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

**楽観的トランザクションが**何であるかわからない場合は、まだ使用し***ない***でください。**楽観的トランザクション**では、アプリケーションが`COMMIT`ステートメントによって返される[すべてのエラー](https://docs.pingcap.com/tidb/stable/error-codes)正しく処理できる必要があるためです。アプリケーションがそれらをどのように処理するかわからない場合は、代わりに**悲観的トランザクション**を使用してください。

</CustomContent>

## アプリケーションが TiDB と対話する方法 {#the-way-applications-interact-with-tidb}

TiDB は MySQL プロトコルとの互換性が高く、 [ほとんどの MySQL 構文と機能](/mysql-compatibility.md)をサポートしているため、ほとんどの MySQL 接続ライブラリは TiDB と互換性があります。アプリケーション フレームワークまたは言語が PingCAP から正式に適応されていない場合は、MySQL のクライアント ライブラリを使用することをお勧めします。 TiDB のさまざまな機能を積極的にサポートするサードパーティ ライブラリが増えています。

TiDB は MySQL プロトコルおよび MySQL 構文と互換性があるため、MySQL をサポートするほとんどの ORM も TiDB と互換性があります。

## 続きを読む {#read-more}

<CustomContent platform="tidb">

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [Driverまたは ORM を選択してください](/develop/dev-guide-choose-driver-or-orm.md)
-   [TiDB に接続する](/develop/dev-guide-connect-to-tidb.md)
-   [データベーススキーマの設計](/develop/dev-guide-schema-design-overview.md)
-   [データの書き込み](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [トランザクション](/develop/dev-guide-transaction-overview.md)
-   [最適化](/develop/dev-guide-optimize-sql-overview.md)
-   [アプリケーション例](/develop/dev-guide-sample-application-java-spring-boot.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [Driverまたは ORM を選択してください](/develop/dev-guide-choose-driver-or-orm.md)
-   [データベーススキーマの設計](/develop/dev-guide-schema-design-overview.md)
-   [データの書き込み](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [トランザクション](/develop/dev-guide-transaction-overview.md)
-   [最適化](/develop/dev-guide-optimize-sql-overview.md)
-   [アプリケーション例](/develop/dev-guide-sample-application-java-spring-boot.md)

</CustomContent>
