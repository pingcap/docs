---
title: SQL or Transaction Issues
summary: Learn how to troubleshoot SQL or transaction issues that might occur during application development.
---

# SQL またはトランザクションの問題 {#sql-or-transaction-issues}

このドキュメントでは、アプリケーション開発中に発生する可能性のある問題と関連ドキュメントを紹介します。

## SQL クエリの問題のトラブルシューティング {#troubleshoot-sql-query-problems}

SQL クエリのパフォーマンスを向上させたい場合は、 [SQL性能チューニング](/develop/dev-guide-optimize-sql-overview.md)の手順に従って、テーブル全体のスキャンやインデックスの欠落などのパフォーマンスの問題を解決してください。

<CustomContent platform="tidb">

それでもパフォーマンスの問題がある場合は、次のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [Top SQLを使用して高価なクエリを特定する](/dashboard/top-sql.md)

SQL 操作について質問がある場合は、 [SQL に関するよくある質問](/faq/sql-faq.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

SQL 操作について質問がある場合は、 [SQL に関するよくある質問](https://docs.pingcap.com/tidb/stable/sql-faq)を参照してください。

</CustomContent>

## 取引に関する問題のトラブルシューティング {#troubleshoot-transaction-issues}

[トランザクション エラーの処理](/develop/dev-guide-transaction-troubleshoot.md)を参照してください。

## こちらもご覧ください {#see-also}

-   [サポートされていない機能](/mysql-compatibility.md#unsupported-features)

<CustomContent platform="tidb">

-   [クラスタ管理に関するよくある質問](/faq/manage-cluster-faq.md)
-   [TiDB よくある質問](/faq/tidb-faq.md)

</CustomContent>
