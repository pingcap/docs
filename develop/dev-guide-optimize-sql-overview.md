---
title: Overview of Optimizing SQL Performance
summary: Provides an overview of SQL performance tuning for TiDB application developers.
---

# SQL パフォーマンスの最適化の概要 {#overview-of-optimizing-sql-performance}

このドキュメントでは、TiDB で SQL ステートメントのパフォーマンスを最適化する方法を紹介します。良好なパフォーマンスを得るには、次の点から始めることができます。

-   SQLパフォーマンスのチューニング
-   スキーマ設計: アプリケーションのワークロード パターンに基づいて、トランザクションの競合やホット スポットを回避するためにテーブル スキーマの変更が必要になる場合があります。

## SQLパフォーマンスのチューニング {#sql-performance-tuning}

SQL ステートメントのパフォーマンスを向上させるには、次のガイドラインに従うことができます。

-   できるだけ少ない行をスキャンします。必要なデータのみをスキャンし、余分なデータをスキャンしないことをお勧めします。
-   適切なインデックスを使用してください。 SQL の`WHERE`句の列に対応するインデックスがあることを確認してください。そうでない場合、ステートメントはテーブル全体のスキャンを必要とするため、パフォーマンスが低下します。
-   適切な結合タイプを使用してください。クエリに含まれるテーブルの相対的なサイズに基づいて、適切な結合タイプを選択することが重要です。一般に、TiDB のコストベースのオプティマイザーは、最もパフォーマンスの高い結合タイプを選択します。ただし、場合によっては、より適切な結合タイプを手動で指定する必要がある場合があります。
-   適切なstorageエンジンを使用してください。ハイブリッド OLTP および OLAP ワークロードの場合は、 TiFlashエンジンが推奨されます。詳細は[HTAPクエリ](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)を参照してください。

## スキーマ設計 {#schema-design}

[SQLパフォーマンスのチューニング](#sql-performance-tuning)の後でもアプリケーションが良好なパフォーマンスを得ることができない場合は、次の問題を回避するためにスキーマ設計とデータ アクセス パターンを確認する必要がある場合があります。

<CustomContent platform="tidb">

-   トランザクションの競合。トランザクション競合を診断して解決する方法については、 [ロックの競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。
-   ホットスポット。ホット スポットを診断して解決する方法については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   トランザクションの競合。トランザクション競合を診断して解決する方法については、 [ロックの競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)を参照してください。
-   ホットスポット。ホット スポットを診断して解決する方法については、 [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)を参照してください。

</CustomContent>

### こちらも参照 {#see-also}

<CustomContent platform="tidb">

-   [SQL性能チューニング](/sql-tuning-overview.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [SQL性能チューニング](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)

</CustomContent>
