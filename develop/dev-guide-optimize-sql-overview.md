---
title: Overview of Optimizing SQL Performance
summary: TiDB アプリケーション開発者向けに、SQL パフォーマンス チューニングの概要を説明します。
---

# SQL パフォーマンスの最適化の概要 {#overview-of-optimizing-sql-performance}

このドキュメントでは、TiDB で SQL ステートメントのパフォーマンスを最適化する方法を紹介します。良好なパフォーマンスを得るには、まず次の点に注意してください。

-   SQLパフォーマンスチューニング
-   スキーマ設計: アプリケーションのワークロード パターンに基づいて、トランザクションの競合やホット スポットを回避するためにテーブル スキーマを変更する必要がある場合があります。

## SQLパフォーマンスチューニング {#sql-performance-tuning}

良好な SQL ステートメントのパフォーマンスを得るには、次のガイドラインに従ってください。

-   スキャンする行数はできるだけ少なくしてください。必要なデータのみをスキャンし、余分なデータのスキャンは避けることをお勧めします。
-   適切なインデックスを使用します。SQL の`WHERE`句の列に対応するインデックスがあることを確認します。そうでない場合、ステートメントは完全なテーブル スキャンを必要とするため、パフォーマンスが低下します。
-   適切な結合タイプを使用します。クエリに含まれるテーブルの相対的なサイズに基づいて、適切な結合タイプを選択することが重要です。通常、TiDB のコストベースのオプティマイザーは、パフォーマンスが最も優れた結合タイプを選択します。ただし、場合によっては、より適切な結合タイプを手動で指定する必要があります。
-   適切なstorageエンジンを使用します。ハイブリッド OLTP および OLAP ワークロードの場合、 TiFlashエンジンが推奨されます。詳細については、 [HTAP クエリ](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)参照してください。

## スキーマ設計 {#schema-design}

[SQLパフォーマンスのチューニング](#sql-performance-tuning)を過ぎてもアプリケーションのパフォーマンスがまだ良好でない場合は、次の問題を回避するためにスキーマ設計とデータ アクセス パターンを確認する必要がある可能性があります。

<CustomContent platform="tidb">

-   トランザクションの競合。トランザクションの競合を診断して解決する方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)参照してください。
-   ホットスポット。ホットスポットを診断して解決する方法については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   トランザクションの競合。トランザクションの競合を診断して解決する方法については、 [ロック競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)参照してください。
-   ホットスポット。ホットスポットを診断して解決する方法については、 [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)参照してください。

</CustomContent>

### 参照 {#see-also}

<CustomContent platform="tidb">

-   [SQL性能チューニング](/sql-tuning-overview.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [SQL性能チューニング](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)

</CustomContent>
