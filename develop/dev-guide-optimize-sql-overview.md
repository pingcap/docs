---
title: Overview of Optimizing SQL Performance
summary: TiDB アプリケーション開発者向けに、SQL パフォーマンス チューニングの概要を説明します。
aliases: ['/ja/tidb/stable/dev-guide-optimize-sql-overview/','/ja/tidbcloud/dev-guide-optimize-sql-overview/']
---

# SQLパフォーマンスの最適化の概要 {#overview-of-optimizing-sql-performance}

このドキュメントでは、TiDBにおけるSQL文のパフォーマンスを最適化する方法を紹介します。良好なパフォーマンスを得るには、まず以下の点に着目してください。

-   SQLパフォーマンスチューニング
-   スキーマ設計: アプリケーションのワークロード パターンに基づいて、トランザクションの競合やホット スポットを回避するためにテーブル スキーマを変更する必要がある場合があります。

## SQLパフォーマンスチューニング {#sql-performance-tuning}

良好な SQL ステートメントのパフォーマンスを得るには、次のガイドラインに従ってください。

-   スキャンする行数はできるだけ少なくしてください。必要なデータのみをスキャンし、余分なデータのスキャンは避けることをお勧めします。
-   適切なインデックスを使用してください。SQLの`WHERE`節の列に対応するインデックスがあることを確認してください。インデックスがない場合、文はフルテーブルスキャンを必要とし、パフォーマンスが低下します。
-   適切な結合タイプを使用してください。クエリに含まれるテーブルの相対的なサイズに基づいて、適切な結合タイプを選択することが重要です。通常、TiDBのコストベースオプティマイザは、パフォーマンスが最も高い結合タイプを選択します。ただし、場合によっては、より適切な結合タイプを手動で指定する必要があることもあります。
-   適切なstorageエンジンを使用してください。OLTPとOLAPのハイブリッドワークロードには、 TiFlashエンジンが推奨されます。詳細については、 [HTAPクエリ](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)参照してください。

## スキーマ設計 {#schema-design}

[SQLパフォーマンスのチューニング](#sql-performance-tuning)後もアプリケーションのパフォーマンスがまだ良好でない場合は、次の問題を回避するためにスキーマ設計とデータ アクセス パターンを確認する必要がある可能性があります。

-   トランザクションの競合。トランザクションの競合を診断して解決する方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)参照してください。
-   ホットスポット。ホットスポットの診断と解決方法については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。

### 参照 {#see-also}

-   [TiDB Cloudの SQL性能チューニング](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)
-   [TiDBセルフマネージドのSQL性能チューニング](/sql-tuning-overview.md)

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
