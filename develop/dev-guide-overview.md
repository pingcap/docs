---
title: Developer Overview
summary: Introduce the overview of the developer guide.
aliases: ['/appdev/dev/app-dev-overview','/tidb/stable/dev-guide-outdated-for-laravel']
---

# 開発者ガイドの概要 {#developer-guide-overview}

このガイドはアプリケーション開発者向けに書かれていますが、TiDBの内部動作に興味がある場合、またはTiDB開発に参加したい場合は、TiDBの詳細について[TiDBカーネル開発ガイド](https://pingcap.github.io/tidb-dev-guide/)をお読みください。

このチュートリアルでは、TiDBを使用してアプリケーションをすばやく構築する方法、TiDBの考えられる使用例、および一般的な問題を処理する方法を示します。したがって、このページを読む前に、 [TiDBデータベースプラットフォームのクイックスタートガイド](/quick-start-with-tidb.md)を読むことをお勧めします。

## TiDBの基本 {#tidb-basics}

TiDBの使用を開始する前に、TiDBがどのように機能するかについてのいくつかの重要なメカニズムを理解する必要があります。

-   [TiDBトランザクションの概要](/transaction-overview.md)を読んでTiDBでトランザクションがどのように機能するかを理解するか、 [アプリケーション開発者向けのトランザクションノート](/develop/dev-guide-transaction-overview.md)をチェックしてアプリケーション開発に必要なトランザクションの知識について学びます。
-   [アプリケーションがTiDBと対話する方法](#the-way-applications-interact-with-tidb)を理解します。

## TiDBトランザクションメカニズム {#tidb-transaction-mechanisms}

TiDBは分散トランザクションをサポートし、 [楽観的なトランザクション](/optimistic-transaction.md)モードと[悲観的な取引](/pessimistic-transaction.md)モードの両方を提供します。現在のバージョンのTiDBは、デフォルトで**ペシミスティックトランザクション**モードを使用します。これにより、従来のモノリシックデータベース（MySQLなど）と同じようにTiDBとトランザクションを実行できます。

[`BEGIN`](/sql-statements/sql-statement-begin.md)を使用してトランザクションを開始するか、 `BEGIN PESSIMISTIC`を使用して**悲観的なトランザクション**を明示的に指定するか、 `BEGIN OPTIMISTIC`を使用して<strong>楽観的なトランザクション</strong>を明示的に指定することができます。その後、トランザクションをコミット（ [`COMMIT`](/sql-statements/sql-statement-commit.md) ）またはロールバック（ [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) ）することができます。

TiDBは、 `BEGIN`の開始から`COMMIT`または`ROLLBACK`の終了までのすべてのステートメントのアトミック性を保証します。つまり、この期間中に実行されるすべてのステートメントは、全体として成功または失敗します。これは、アプリケーション開発に必要なデータの一貫性を確保するために使用されます。

**楽観的なトランザクション**が何かわから*<strong>ない</strong>*場合は、まだ使用しないでください。<strong>楽観的なトランザクション</strong>では、アプリケーションが`COMMIT`ステートメントによって返される[すべてのエラー](/error-codes.md)を正しく処理できる必要があるためです。アプリケーションがそれらをどのように処理するかわからない場合は、代わりに<strong>悲観的なトランザクション</strong>を使用してください。

## アプリケーションがTiDBと対話する方法 {#the-way-applications-interact-with-tidb}

TiDBはMySQLプロトコルとの互換性が高く、 [ほとんどのMySQLの構文と機能](https://docs.pingcap.com/zh/tidb/stable/mysql-compatibility)をサポートしているため、ほとんどのMySQL接続ライブラリはTiDBと互換性があります。アプリケーションフレームワークまたは言語にPingCAPからの正式な適応がない場合は、MySQLのクライアントライブラリを使用することをお勧めします。ますます多くのサードパーティライブラリがTiDBのさまざまな機能を積極的にサポートしています。

TiDBはMySQLプロトコルおよびMySQL構文と互換性があるため、MySQLをサポートするほとんどのORMはTiDBとも互換性があります。

## 続きを読む {#read-more}

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [DriverまたはORMを選択します](/develop/dev-guide-choose-driver-or-orm.md)
-   [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)
-   [データベーススキーマの設計](/develop/dev-guide-schema-design-overview.md)
-   [データの書き込み](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [取引](/develop/dev-guide-transaction-overview.md)
-   [最適化](/develop/dev-guide-optimize-sql-overview.md)
-   [アプリケーション例](/develop/dev-guide-sample-application-spring-boot.md)
