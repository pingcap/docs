---
title: Transactions
summary: TiDB Cloudのトランザクション概念について学習します。
---

# 取引 {#transactions}

TiDB は完全な分散トランザクションを提供し、モデルには[Google パーコレーター](https://research.google.com/pubs/pub36726.html)に基づいたいくつかの最適化が施されています。

## 楽観的トランザクションモード {#optimistic-transaction-mode}

TiDBの楽観的トランザクションモデルは、コミットフェーズまで競合を検出しません。競合が発生した場合、トランザクションは再試行する必要があります。しかし、競合が深刻な場合、再試行前の操作は無効となり、再度実行する必要があるため、このモデルは非効率的です。

データベースをカウンターとして使用する場合を考えてみましょう。同時アクセス数が多いと深刻な競合が発生し、複数回の再試行やタイムアウトが発生する可能性があります。したがって、深刻な競合が発生するシナリオでは、悲観的トランザクションモードを使用するか、Redisにカウンターを配置するなど、システムアーキテクチャレベルで問題を解決することをお勧めします。ただし、アクセス競合がそれほど深刻でない場合は、楽観的トランザクションモデルが効率的です。

詳細については[TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)参照してください。

## 悲観的なトランザクションモード {#pessimistic-transaction-mode}

TiDBでは、悲観的トランザクションモードはMySQLとほぼ同じ動作をします。トランザクションは実行フェーズでロックを適用し、競合状況での再試行を回避し、高い成功率を保証します。悲観的ロックを適用することで、 `SELECT FOR UPDATE`使用して事前にデータをロックすることもできます。

ただし、アプリケーション シナリオの競合が少ない場合は、楽観的トランザクション モデルの方がパフォーマンスが向上します。

詳細については[TiDB 悲観的トランザクションモード](/pessimistic-transaction.md)参照してください。

## トランザクション分離レベル {#transaction-isolation-levels}

トランザクション分離は、データベーストランザクション処理の基盤の一つです。分離は、トランザクションの4つの主要な特性（一般的に[ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)と呼ばれます）の一つです。

TiDBはスナップショット分離（SI）一貫性を実装しており、MySQLとの互換性のために`REPEATABLE-READ`として宣伝されています。これはSI [ANSI繰り返し読み取り分離レベル](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read)やSI [MySQL 繰り返し読み取りレベル](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)とは異なります。

詳細については[TiDBトランザクション分離レベル](/transaction-isolation-levels.md)参照してください。

## 非トランザクションDMLステートメント {#non-transactional-dml-statements}

非トランザクションDML文とは、複数のSQL文（つまり複数のバッチ）に分割され、順番に実行されるDML文です。トランザクションの原子性と独立性を犠牲にして、バッチデータ処理のパフォーマンスと使いやすさを向上させます。

通常、メモリを大量に消費するトランザクションは、トランザクションサイズ制限を回避するために複数のSQL文に分割する必要があります。非トランザクションDML文は、このプロセスをTiDBカーネルに統合することで、同様の効果を実現します。SQL文を分割することで、非トランザクションDML文の効果を理解するのに役立ちます`DRY RUN`構文を使用すると、分割された文をプレビューできます。

詳細については[非トランザクションDML文](/non-transactional-dml.md)参照してください。
