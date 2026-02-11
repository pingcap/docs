---
title: TiDB basics for Developers
summary: トランザクション メカニズムやアプリケーションが TiDB と対話する方法など、開発者向けの TiDB の基礎を学習します。
---

# 開発者向けTiDBの基礎 {#tidb-basics-for-developers}

TiDB を使い始める前に、TiDB がどのように動作するかに関するいくつかの重要なメカニズムを理解する必要があります。

-   TiDB でのトランザクションの仕組みを理解するには[TiDBトランザクションの概要](/transaction-overview.md) 、アプリケーション開発に必要なトランザクションの知識については[アプリケーション開発者向けトランザクションノート](/develop/dev-guide-transaction-overview.md)をお読みください。
-   [アプリケーションがTiDBと対話する方法](#the-way-applications-interact-with-tidb)理解する。
-   分散データベース TiDB およびTiDB Cloud を構築するためのコア コンポーネントと概念を学習するには、無料のオンライン コース[TiDBの紹介](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)を参照してください。

## TiDBトランザクションメカニズム {#tidb-transaction-mechanisms}

TiDBは分散トランザクションをサポートし、モード[楽観的取引](/optimistic-transaction.md)とモード[悲観的取引](/pessimistic-transaction.md)の両方を提供しています。現在のバージョンのTiDBでは、デフォルトで**悲観的トランザクション**モードが採用されており、従来のモノリシックデータベース（MySQLなど）と同様にTiDBでトランザクションを実行できます。

[`BEGIN`](/sql-statements/sql-statement-begin.md)でトランザクションを開始するか、 `BEGIN PESSIMISTIC`で**悲観的トランザクションを**明示的に指定するか、 `BEGIN OPTIMISTIC`で**楽観的トランザクション**を明示的に指定することができます。その後、トランザクションをコミット（ [`COMMIT`](/sql-statements/sql-statement-commit.md) ）またはロールバック（ [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) ）することができます。

TiDBは、 `BEGIN`の開始から`COMMIT`または`ROLLBACK`の終了までのすべてのステートメントのアトミック性を保証します。つまり、この期間中に実行されるすべてのステートメントは、全体として成功するか失敗するかのいずれかになります。これは、アプリケーション開発に必要なデータの一貫性を確保するために使用されます。

**楽観的トランザクション**が何なのかわからない場合は、まだ使用***しないで***ください。**楽観的トランザクション**では、アプリケーションが`COMMIT`文によって返される[すべてのエラー](https://docs.pingcap.com/tidb/v8.5/error-codes/)正しく処理できる必要があります。アプリケーションがどのように処理するかわからない場合は、代わりに**悲観的トランザクションを**使用してください。

## アプリケーションがTiDBと対話する方法 {#the-way-applications-interact-with-tidb}

TiDBはMySQLプロトコルとの互換性が高く、 [ほとんどのMySQL構文と機能](/mysql-compatibility.md)サポートしているため、ほとんどのMySQL接続ライブラリはTiDBと互換性があります。アプリケーションフレームワークまたは言語にPingCAPからの公式な対応がない場合は、MySQLのクライアントライブラリを使用することをお勧めします。ますます多くのサードパーティ製ライブラリがTiDBの様々な機能を積極的にサポートしています。

TiDB は MySQL プロトコルおよび MySQL 構文と互換性があるため、MySQL をサポートするほとんどの ORM も TiDB と互換性があります。

## 続きを読む {#read-more}

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [DriverまたはORMを選択](/develop/dev-guide-choose-driver-or-orm.md)
-   [TiDBに接続する](https://docs.pingcap.com/tidb/v8.5/dev-guide-connect-to-tidb/)
-   [データベーススキーマ設計](/develop/dev-guide-schema-design-overview.md)
-   [データの書き込み](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [トランザクション](/develop/dev-guide-transaction-overview.md)
-   [最適化する](/develop/dev-guide-optimize-sql-overview.md)
-   [アプリケーション例](/develop/dev-guide-sample-application-java-spring-boot.md)

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
