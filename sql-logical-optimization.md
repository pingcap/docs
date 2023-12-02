---
title: SQL Logical Optimization
---

# SQL論理最適化 {#sql-logical-optimization}

この章では、TiDB が最終的なクエリ プランを生成する方法を理解するのに役立ついくつかの重要なロジックの書き換えについて説明します。たとえば、TiDB で`select * from t where t.a in (select t1.a from t1 where t1.b=t.b)`クエリを実行すると、TiDB がここでいくつかの書き換えを行っているため、 `IN`サブクエリ`t.a in (select t1.a from t1 where t1.b=t.b)`が存在しないことがわかります。

この章では、次の主要な書き換えを紹介します。

-   [サブクエリ関連の最適化](/subquery-optimization.md)
-   [カラムの剪定](/column-pruning.md)
-   [相関サブクエリの相関解除](/correlated-subquery-optimization.md)
-   [最大値/最小値の削除](/max-min-eliminate.md)
-   [Predicate Push Down](/predicate-push-down.md)
-   [パーティションのプルーニング](/partition-pruning.md)
-   [TopN およびリミット演算子のプッシュダウン](/topn-limit-push-down.md)
-   [結合したテーブルの再配置](/join-reorder.md)
