---
title: SQL Optimization Process
summary: TiDB での SQL の論理的および物理的な最適化について学習します。
---

# SQL最適化プロセス {#sql-optimization-process}

TiDB では、クエリを入力してから最終実行プランに従って実行結果を取得するまでのプロセスは次のように示されます。

![SQL Optimization Process](/media/sql-optimization.png)

元のクエリ テキストを`parser`で解析し、簡単な妥当性チェックを行った後、TiDB はまずクエリに論理的に同等の変更を加えます。詳細な変更については、 [SQL 論理最適化](/sql-logical-optimization.md)を参照してください。

これらの等価変更により、このクエリは論理実行プランで扱いやすくなります。等価変更が行われた後、TiDB は元のクエリと等価なクエリプラン構造を取得し、データ分布と演算子の特定の実行コストに基づいて最終的な実行プランを取得します。詳細については、 [SQL 物理最適化](/sql-physical-optimization.md)を参照してください。

同時に、TiDB が[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントを実行するときに、キャッシュを有効にして、TiDB で実行プランを生成するコストを削減することを選択できます。詳細については、 [実行プランキャッシュ](/sql-prepared-plan-cache.md)を参照してください。
