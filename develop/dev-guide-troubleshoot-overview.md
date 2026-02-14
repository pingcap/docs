---
title: SQL or Transaction Issues
summary: アプリケーション開発中に発生する可能性のある SQL またはトランザクションの問題をトラブルシューティングする方法を学習します。
aliases: ['/ja/tidb/stable/dev-guide-troubleshoot-overview/','/ja/tidbcloud/dev-guide-troubleshoot-overview/']
---

# SQLまたはトランザクションの問題 {#sql-or-transaction-issues}

このドキュメントでは、アプリケーション開発中に発生する可能性のある問題と関連ドキュメントについて説明します。

## SQLクエリの問題のトラブルシューティング {#troubleshoot-sql-query-problems}

SQL クエリのパフォーマンスを向上させる場合は、 [SQL性能チューニング](/develop/dev-guide-optimize-sql-overview.md)手順に従って、完全なテーブル スキャンやインデックスの欠落などのパフォーマンスの問題を解決してください。

それでもパフォーマンスの問題が発生する場合は、次のドキュメントを参照してください。

<SimpleTab groupId="platform">

<div label="TiDB Cloud" value="tidb-cloud">

-   [遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)
-   [ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)
-   [キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)

</div>

<div label="TiDB Self-Managed" value="tidb">

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [Top SQLを使用してコストの高いクエリを特定する](/dashboard/top-sql.md)

</div>
</SimpleTab>

SQL 操作について質問がある場合は、 [SQLに関するよくある質問](/faq/sql-faq.md)参照してください。

## 取引に関する問題のトラブルシューティング {#troubleshoot-transaction-issues}

[トランザクションエラーを処理する](/develop/dev-guide-transaction-troubleshoot.md)参照。

## 参照 {#see-also}

-   [サポートされていない機能](/mysql-compatibility.md#unsupported-features)
-   [TiDB Cloudに関するよくある質問](/tidb-cloud/tidb-cloud-faq.md)
-   [TiDBセルフマネージドに関するFAQ](/faq/faq-overview.md)

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
