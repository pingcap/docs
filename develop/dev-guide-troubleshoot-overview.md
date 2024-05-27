---
title: SQL or Transaction Issues
summary: アプリケーション開発中に発生する可能性のある SQL またはトランザクションの問題をトラブルシューティングする方法を学習します。
---

# SQL またはトランザクションの問題 {#sql-or-transaction-issues}

このドキュメントでは、アプリケーション開発中に発生する可能性のある問題と関連ドキュメントについて説明します。

## SQLクエリの問題のトラブルシューティング {#troubleshoot-sql-query-problems}

SQL クエリのパフォーマンスを向上させる場合は、 [SQL性能チューニング](/develop/dev-guide-optimize-sql-overview.md)の手順に従って、完全なテーブル スキャンやインデックスの欠落などのパフォーマンスの問題を解決します。

<CustomContent platform="tidb">

それでもパフォーマンスの問題が発生する場合は、次のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [Top SQLを使用してコストの高いクエリを特定する](/dashboard/top-sql.md)

SQL 操作に関する質問がある場合は、 [SQLに関するよくある質問](/faq/sql-faq.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

SQL 操作に関する質問がある場合は、 [SQLに関するよくある質問](https://docs.pingcap.com/tidb/stable/sql-faq)参照してください。

</CustomContent>

## 取引に関する問題のトラブルシューティング {#troubleshoot-transaction-issues}

[トランザクションエラーの処理](/develop/dev-guide-transaction-troubleshoot.md)参照。

## 参照 {#see-also}

-   [サポートされていない機能](/mysql-compatibility.md#unsupported-features)

<CustomContent platform="tidb">

-   [クラスタ管理に関するよくある質問](/faq/manage-cluster-faq.md)
-   [TiDB に関するよくある質問](/faq/tidb-faq.md)

</CustomContent>
