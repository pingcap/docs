---
title: SQL Optimization Process
summary: TiDB での SQL の論理的および物理的な最適化について学習します。
---

# SQL最適化プロセス {#sql-optimization-process}

TiDB では、クエリを入力してから最終実行プランに従って実行結果を取得するまでのプロセスは次のように示されます。

![SQL Optimization Process](/media/sql-optimization.png)

TiDBは、元のクエリテキストを`parser`で解析し、簡単な妥当性チェックを行った後、まずクエリに論理的に同等の変更を加えます。詳細な変更については、 [SQL論理最適化](/sql-logical-optimization.md)参照してください。

これらの等価変更により、このクエリは論理実行プランで処理しやすくなります。等価変更が完了すると、TiDBは元のクエリと等価なクエリプラン構造を取得し、その後、データ分布と演算子の具体的な実行コストに基づいて最終的な実行プランを取得します。詳細については、 [SQL物理最適化](/sql-physical-optimization.md)参照してください。

同時に、TiDBが[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントを実行する際に、キャッシュを有効にするかどうかを選択できます。これにより、TiDBでの実行計画生成のコストを削減できます。詳細については、 [実行プランキャッシュ](/sql-prepared-plan-cache.md)参照してください。
