---
title: SQL Logical Optimization
---

# SQL論理最適化 {#sql-logical-optimization}

この章では、TiDBが最終的なクエリプランを生成する方法を理解するのに役立つ、いくつかの重要なロジックの書き直しについて説明します。たとえば、TiDBで`select * from t where t.a in (select t1.a from t1 where t1.b=t.b)`のクエリを実行すると、TiDBがここでいくつかの書き換えを行ったため、 `IN`つのサブクエリ`t.a in (select t1.a from t1 where t1.b=t.b)`が存在しないことがわかります。

この章では、次の主要な書き直しを紹介します。

-   [サブクエリ関連の最適化](/subquery-optimization.md)
-   [カラムの剪定](/column-pruning.md)
-   [相関サブクエリの無相関化](/correlated-subquery-optimization.md)
-   [最大/最小を排除する](/max-min-eliminate.md)
-   [Predicate Push Down](/predicate-push-down.md)
-   [パーティションの剪定](/partition-pruning.md)
-   [TopNおよびLimitOperatorプッシュダウン](/topn-limit-push-down.md)
-   [結合したテーブルの再配置](/join-reorder.md)
