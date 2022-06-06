---
title: SQL Optimization Process
summary: Learn about the logical and physical optimization of SQL in TiDB.
---

# SQL最適化プロセス {#sql-optimization-process}

TiDBでは、クエリの入力から最終的な実行プランに従って実行結果を取得するまでのプロセスを次のように示します。

![SQL Optimization Process](/media/sql-optimization.png)

元のクエリテキストを`parser`で解析し、いくつかの簡単な妥当性チェックを行った後、TiDBは最初にクエリに論理的に同等の変更を加えます。詳細な変更については、 [SQL論理最適化](/sql-logical-optimization.md)を参照してください。

これらの同等の変更により、このクエリは論理実行プランで処理しやすくなります。同等の変更が行われた後、TiDBは元のクエリと同等のクエリプラン構造を取得し、データ分散とオペレーターの特定の実行コストに基づいて最終的な実行プランを取得します。詳細については、 [SQLの物理的最適化](/sql-physical-optimization.md)を参照してください。

同時に、TiDBが[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントを実行するときに、キャッシュを有効にして、TiDBで実行プランを生成するコストを削減することを選択できます。詳細については、 [実行プランキャッシュ](/sql-prepared-plan-cache.md)を参照してください。
