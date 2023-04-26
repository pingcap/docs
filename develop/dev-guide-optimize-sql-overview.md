---
title: Overview of Optimizing SQL Performance
summary: Provides an overview of SQL performance tuning for TiDB application developers.
---

# SQL パフォーマンスの最適化の概要 {#overview-of-optimizing-sql-performance}

このドキュメントでは、TiDB で SQL ステートメントのパフォーマンスを最適化する方法を紹介します。優れたパフォーマンスを得るには、次の側面から始めることができます。

-   SQL パフォーマンスのチューニング
-   スキーマ設計: アプリケーションのワークロード パターンに基づいて、トランザクションの競合やホット スポットを回避するためにテーブル スキーマを変更する必要がある場合があります。

## SQL パフォーマンスのチューニング {#sql-performance-tuning}

優れた SQL ステートメントのパフォーマンスを得るには、次のガイドラインに従うことができます。

-   できるだけ少ない行をスキャンします。必要なデータのみをスキャンし、余分なデータをスキャンしないことをお勧めします。
-   適切なインデックスを使用してください。 SQL の`WHERE`句の列に対応するインデックスがあることを確認してください。そうでない場合、ステートメントは全表スキャンを伴うため、パフォーマンスが低下します。
-   正しい結合タイプを使用してください。クエリに含まれるテーブルの相対的なサイズに基づいて、適切な結合の種類を選択することが重要です。一般に、TiDB のコストベースのオプティマイザーは、最もパフォーマンスの高い結合タイプを選択します。ただし、場合によっては、より適切な結合タイプを手動で指定する必要があります。
-   適切なstorageエンジンを使用します。 OLTP と OLAP のハイブリッド ワークロードには、 TiFlashエンジンをお勧めします。詳細については、 [HTAP クエリ](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)を参照してください。

## スキーマ設計 {#schema-design}

[SQL パフォーマンスのチューニング](#sql-performance-tuning)の後、アプリケーションがまだ良好なパフォーマンスを得られない場合は、次の問題を回避するために、スキーマの設計とデータ アクセス パターンを確認する必要がある場合があります。

<CustomContent platform="tidb">

-   トランザクション競合。トランザクションの競合を診断して解決する方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。
-   ホットスポット。ホット スポットを診断して解決する方法については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   トランザクション競合。トランザクションの競合を診断して解決する方法については、 [ロック競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)を参照してください。
-   ホットスポット。ホット スポットを診断して解決する方法については、 [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)を参照してください。

</CustomContent>

### こちらもご覧ください {#see-also}

<CustomContent platform="tidb">

-   [SQL性能チューニング](/sql-tuning-overview.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [SQL性能チューニング](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)

</CustomContent>
