---
title: SQL Optimization Process
summary: Learn about the logical and physical optimization of SQL in TiDB.
---

# SQL最適化プロセス {#sql-optimization-process}

TiDB では、クエリの入力から最終的な実行計画に従って実行結果を取得するまでのプロセスは次のように図示されます。

![SQL Optimization Process](/media/sql-optimization.png)

元のクエリ テキストを`parser`で解析し、いくつかの簡単な有効性チェックを行った後、TiDB はまず論理的に同等の変更をクエリにいくつか加えます。詳しい変更点は[SQL論理最適化](/sql-logical-optimization.md)を参照してください。

これらの同等の変更により、このクエリは論理実行プランでの処理が容易になります。同等の変更が行われた後、TiDB は元のクエリと同等のクエリ プラン構造を取得し、データ分布とオペレーターの具体的な実行コストに基づいて最終的な実行プランを取得します。詳細は[SQLの物理的な最適化](/sql-physical-optimization.md)を参照してください。

同時に、TiDB が[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントを実行するときに、TiDB で実行プランを生成するコストを削減するためにキャッシュを有効にすることを選択できます。詳細は[実行計画キャッシュ](/sql-prepared-plan-cache.md)を参照してください。
