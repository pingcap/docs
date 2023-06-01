---
title: SQL or Transaction Issues
summary: Learn how to troubleshoot SQL or transaction issues that might occur during application development.
---

# SQL またはトランザクションの問題 {#sql-or-transaction-issues}

このドキュメントでは、アプリケーション開発中に発生する可能性のある問題と関連ドキュメントを紹介します。

## SQL クエリの問題のトラブルシューティング {#troubleshoot-sql-query-problems}

SQL クエリのパフォーマンスを向上させたい場合は、 [<a href="/develop/dev-guide-optimize-sql-overview.md">SQL性能チューニング</a>](/develop/dev-guide-optimize-sql-overview.md)の手順に従って、テーブル全体のスキャンやインデックスの欠落などのパフォーマンスの問題を解決します。

<CustomContent platform="tidb">

それでもパフォーマンスの問題が解決しない場合は、次のドキュメントを参照してください。

-   [<a href="/analyze-slow-queries.md">遅いクエリを分析する</a>](/analyze-slow-queries.md)
-   [<a href="/dashboard/top-sql.md">Top SQLを使用して負荷の高いクエリを特定する</a>](/dashboard/top-sql.md)

SQL 操作に関する質問がある場合は、 [<a href="/faq/sql-faq.md">SQL FAQ</a>](/faq/sql-faq.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

SQL 操作に関する質問がある場合は、 [<a href="https://docs.pingcap.com/tidb/stable/sql-faq">SQL FAQ</a>](https://docs.pingcap.com/tidb/stable/sql-faq)を参照してください。

</CustomContent>

## トランザクションの問題のトラブルシューティング {#troubleshoot-transaction-issues}

[<a href="/develop/dev-guide-transaction-troubleshoot.md">トランザクションエラーを処理する</a>](/develop/dev-guide-transaction-troubleshoot.md)を参照してください。

## こちらも参照 {#see-also}

-   [<a href="/mysql-compatibility.md#unsupported-features">サポートされていない機能</a>](/mysql-compatibility.md#unsupported-features)

<CustomContent platform="tidb">

-   [<a href="/faq/manage-cluster-faq.md">クラスタ管理に関するよくある質問</a>](/faq/manage-cluster-faq.md)
-   [<a href="/faq/tidb-faq.md">TiDB よくある質問</a>](/faq/tidb-faq.md)

</CustomContent>
