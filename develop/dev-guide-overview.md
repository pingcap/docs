---
title: Developer Guide Overview
summary: 開発者ガイドの概要を紹介します。
---

# 開発者ガイドの概要 {#developer-guide-overview}

このガイドはアプリケーション開発者向けに書かれていますが、TiDB の内部動作に興味がある場合や TiDB 開発に参加したい場合は、TiDB の詳細については[TiDB カーネル開発ガイド](https://pingcap.github.io/tidb-dev-guide/)お読みください。

<CustomContent platform="tidb">

このチュートリアルでは、TiDB を使用してアプリケーションをすばやく構築する方法、TiDB の考えられる使用例、一般的な問題の処理方法を説明します。

このページを読む前に、 [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)読むことをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

このチュートリアルでは、 TiDB Cloudを使用してアプリケーションをすばやく構築する方法、 TiDB Cloudの考えられる使用例、および一般的な問題の処理方法を説明します。

</CustomContent>

## TiDBの基礎 {#tidb-basics}

TiDB の使用を開始する前に、TiDB の動作に関するいくつかの重要なメカニズムを理解する必要があります。

-   TiDB でのトランザクションの仕組みを理解するには[TiDBトランザクションの概要](/transaction-overview.md) 、アプリケーション開発に必要なトランザクションの知識については[アプリケーション開発者向けトランザクションノート](/develop/dev-guide-transaction-overview.md)を読んでください。
-   [アプリケーションがTiDBとやりとりする方法](#the-way-applications-interact-with-tidb)理解する。
-   分散データベース TiDB およびTiDB Cloudを構築するためのコア コンポーネントと概念を学習するには、無料のオンライン コース[TiDB の紹介](https://eng.edu.pingcap.com/catalog/info/id:203/?utm_source=docs-dev-guide)を参照してください。

## TiDB トランザクション メカニズム {#tidb-transaction-mechanisms}

TiDB は分散トランザクションをサポートし、モード[楽観的取引](/optimistic-transaction.md)と[悲観的取引](/pessimistic-transaction.md)の両方を提供します。現在のバージョンの TiDB では、デフォルトで**悲観的トランザクション**モードが使用され、従来のモノリシック データベース (MySQL など) と同様に TiDB でトランザクションを実行できます。

[`BEGIN`](/sql-statements/sql-statement-begin.md)を使用してトランザクションを開始したり、 `BEGIN PESSIMISTIC`使用して**悲観的トランザクション**を明示的に指定したり、 `BEGIN OPTIMISTIC`を使用して**楽観的トランザクション**を明示的に指定したりできます。その後、トランザクションをコミット ( [`COMMIT`](/sql-statements/sql-statement-commit.md) ) するか、ロールバック ( [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) ) することができます。

TiDB は、 `BEGIN`の開始から`COMMIT`または`ROLLBACK`の終了までのすべてのステートメントのアトミック性を保証します。つまり、この期間中に実行されるすべてのステートメントは、全体として成功するか失敗します。これは、アプリケーション開発に必要なデータの一貫性を確保するために使用されます。

<CustomContent platform="tidb">

**楽観的トランザクション**が何であるかよくわからない場合は、まだ使用***しない***でください。楽観的トランザクションでは、アプリケーションが`COMMIT`ステートメントによって返された[すべてのエラー](/error-codes.md)を正しく処理できることが求められるためです。アプリケーションが**楽観的トランザクション**をどのように処理するかよくわからない場合は、代わりに**悲観的トランザクション**を使用してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

**楽観的トランザクション**が何であるかよくわからない場合は、まだ使用***しない***でください。楽観的トランザクションでは、アプリケーションが`COMMIT`ステートメントによって返された[すべてのエラー](https://docs.pingcap.com/tidb/stable/error-codes)を正しく処理できることが求められるためです。アプリケーションが**楽観的トランザクション**をどのように処理するかよくわからない場合は、代わりに**悲観的トランザクション**を使用してください。

</CustomContent>

## アプリケーションがTiDBとやりとりする方法 {#the-way-applications-interact-with-tidb}

TiDB は MySQL プロトコルとの互換性が高く、 [ほとんどのMySQL構文と機能](/mysql-compatibility.md)サポートしているため、ほとんどの MySQL 接続ライブラリは TiDB と互換性があります。アプリケーション フレームワークまたは言語に PingCAP からの公式の適応がない場合は、MySQL のクライアント ライブラリを使用することをお勧めします。ますます多くのサードパーティ ライブラリが、TiDB のさまざまな機能を積極的にサポートしています。

TiDB は MySQL プロトコルおよび MySQL 構文と互換性があるため、MySQL をサポートする ORM のほとんどは TiDB とも互換性があります。

## 続きを読む {#read-more}

<CustomContent platform="tidb">

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [DriverまたはORMを選択](/develop/dev-guide-choose-driver-or-orm.md)
-   [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)
-   [データベーススキーマ設計](/develop/dev-guide-schema-design-overview.md)
-   [データの書き込み](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [トランザクション](/develop/dev-guide-transaction-overview.md)
-   [最適化する](/develop/dev-guide-optimize-sql-overview.md)
-   [アプリケーション例](/develop/dev-guide-sample-application-java-spring-boot.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

ここでは、 TiDB Cloudに接続、管理、開発するための追加リソースを見つけることができます。

**データを探索するには**

-   [クイックスタート](/develop/dev-guide-build-cluster-in-cloud.md)
-   [AI支援SQLエディタを使用する](/tidb-cloud/explore-data-with-chat2query.md)
-   [VSコード](/develop/dev-guide-gui-vscode-sqltools.md) [DBeaver](/develop/dev-guide-gui-dbeaver.md) [データグリップ](/develop/dev-guide-gui-datagrip.md)クライアントツールに接続します

**アプリケーションを構築するには**

-   [DriverまたはORMを選択](/develop/dev-guide-choose-driver-or-orm.md)
-   [TiDB Cloud Data API<sup>ベータ版</sup>を使用する](/tidb-cloud/data-service-overview.md)

**クラスターを管理するには**

-   [TiDB Cloudコマンドライン ツール](/tidb-cloud/get-started-with-cli.md)
-   [TiDB Cloud管理 API](/tidb-cloud/api-overview.md)

**TiDBについて詳しく知るには**

-   [データベーススキーマ設計](/develop/dev-guide-schema-design-overview.md)
-   [データの書き込み](/develop/dev-guide-insert-data.md)
-   [データの読み取り](/develop/dev-guide-get-data-from-single-table.md)
-   [トランザクション](/develop/dev-guide-transaction-overview.md)
-   [最適化する](/develop/dev-guide-optimize-sql-overview.md)

</CustomContent>

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
