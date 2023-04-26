---
title: Developer Guide Overview
summary: Introduce the overview of the developer guide.
---

# 開発者ガイドの概要 {#developer-guide-overview}

このガイドはアプリケーション開発者向けに書かれていますが、TiDB の内部動作に興味がある場合、または TiDB 開発に参加したい場合は、TiDB の詳細について[TiDB カーネル開発ガイド](https://pingcap.github.io/tidb-dev-guide/)をお読みください。

<CustomContent platform="tidb">

このチュートリアルでは、TiDB を使用してアプリケーションを迅速に構築する方法、TiDB の使用例、および一般的な問題の処理方法を示します。

このページを読む前に、 [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)を読むことをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

このチュートリアルでは、 TiDB Cloudを使用してアプリケーションを迅速に構築する方法、 TiDB Cloudの使用例、および一般的な問題の処理方法を示します。

</CustomContent>

## TiDB の基本 {#tidb-basics}

TiDB を使い始める前に、TiDB がどのように機能するかのいくつかの重要なメカニズムを理解する必要があります。

-   [TiDBトランザクションの概要](/transaction-overview.md)を読んで TiDB でのトランザクションの仕組みを理解するか、 [アプリケーション開発者向けのトランザクションメモ](/develop/dev-guide-transaction-overview.md)を調べてアプリケーション開発に必要なトランザクションの知識を学んでください。
-   理解する[アプリケーションが TiDB と対話する方法](#the-way-applications-interact-with-tidb) ．
-   分散データベース TiDB およびTiDB Cloudを構築するためのコア コンポーネントと概念については、無料のオンライン コース[TiDB の紹介](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)を参照してください。

## TiDB トランザクション メカニズム {#tidb-transaction-mechanisms}

TiDB は分散トランザクションをサポートし、 [楽観的取引](/optimistic-transaction.md)と[悲観的取引](/pessimistic-transaction.md)の両方のモードを提供します。 TiDB の現在のバージョンでは、デフォルトで**悲観的トランザクション**モードが使用されます。これにより、従来のモノリシック データベース (MySQL など) と同じように TiDB でトランザクションを行うことができます。

[`BEGIN`](/sql-statements/sql-statement-begin.md)を使用してトランザクションを開始するか、 `BEGIN PESSIMISTIC`使用して**悲観的トランザクションを**明示的に指定するか、または`BEGIN OPTIMISTIC`を使用して<strong>楽観的トランザクション</strong>を明示的に指定できます。その後、トランザクションをコミット ( [`COMMIT`](/sql-statements/sql-statement-commit.md) ) またはロールバック ( [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) ) できます。

TiDB は、 `BEGIN`の開始と`COMMIT`または`ROLLBACK`の終了の間のすべてのステートメントの原子性を保証します。つまり、この期間中に実行されるすべてのステートメントは、全体として成功または失敗します。これは、アプリケーション開発に必要なデータの一貫性を確保するために使用されます。

<CustomContent platform="tidb">

**楽観的トランザクション**が何であるかわからない場合は、まだ使用し*<strong>ない</strong>*でください。<strong>楽観的トランザクション</strong>では、アプリケーションが`COMMIT`ステートメントによって返される[すべてのエラー](/error-codes.md)正しく処理できる必要があるためです。アプリケーションがそれらをどのように処理するかわからない場合は、代わりに<strong>悲観的トランザクション</strong>を使用してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

**楽観的トランザクション**が何であるかわからない場合は、まだ使用し*<strong>ない</strong>*でください。<strong>楽観的トランザクション</strong>では、アプリケーションが`COMMIT`ステートメントによって返される[すべてのエラー](https://docs.pingcap.com/tidb/stable/error-codes)正しく処理できる必要があるためです。アプリケーションがそれらをどのように処理するかわからない場合は、代わりに<strong>悲観的トランザクション</strong>を使用してください。

</CustomContent>

## アプリケーションが TiDB と対話する方法 {#the-way-applications-interact-with-tidb}

TiDB は MySQL プロトコルとの互換性が高く、 [ほとんどの MySQL 構文と機能](/mysql-compatibility.md)をサポートしているため、ほとんどの MySQL 接続ライブラリは TiDB と互換性があります。アプリケーション フレームワークまたは言語に PingCAP からの公式の適応がない場合は、MySQL のクライアント ライブラリを使用することをお勧めします。ますます多くのサードパーティ ライブラリが、TiDB のさまざまな機能を積極的にサポートしています。

TiDB は MySQL プロトコルおよび MySQL 構文と互換性があるため、MySQL をサポートするほとんどの ORM は TiDB とも互換性があります。

## 続きを読む {#read-more}

<CustomContent platform="tidb">

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [Driverまたは ORM を選択](/develop/dev-guide-choose-driver-or-orm.md)
-   [TiDB に接続する](/develop/dev-guide-connect-to-tidb.md)
-   [データベース スキーマの設計](/develop/dev-guide-schema-design-overview.md)
-   [書き込みデータ](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [トランザクション](/develop/dev-guide-transaction-overview.md)
-   [最適化](/develop/dev-guide-optimize-sql-overview.md)
-   [応用例](/develop/dev-guide-sample-application-spring-boot.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [Driverまたは ORM を選択](/develop/dev-guide-choose-driver-or-orm.md)
-   [データベース スキーマの設計](/develop/dev-guide-schema-design-overview.md)
-   [書き込みデータ](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [トランザクション](/develop/dev-guide-transaction-overview.md)
-   [最適化](/develop/dev-guide-optimize-sql-overview.md)
-   [応用例](/develop/dev-guide-sample-application-spring-boot.md)

</CustomContent>
