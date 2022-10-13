---
title: SQL Logical Optimization
---

# SQL 論理最適化 {#sql-logical-optimization}

この章では、TiDB が最終的なクエリ プランを生成する方法を理解するのに役立つ、いくつかの重要なロジックの書き直しについて説明します。たとえば、TiDB で`select * from t where t.a in (select t1.a from t1 where t1.b=t.b)`クエリを実行すると、TiDB がここでいくつかの書き換えを行っているため、 `IN`サブクエリ`t.a in (select t1.a from t1 where t1.b=t.b)`が存在しないことがわかります。

この章では、次のキーの書き換えについて説明します。

-   [サブクエリ関連の最適化](/subquery-optimization.md)
-   [カラムの剪定](/column-pruning.md)
-   [相関サブクエリの非相関](/correlated-subquery-optimization.md)
-   [最大/最小を削除](/max-min-eliminate.md)
-   [Predicate Push Down](/predicate-push-down.md)
-   [パーティションのプルーニング](/partition-pruning.md)
-   [TopN および Limit オペレーターのプッシュダウン](/topn-limit-push-down.md)
-   [結合したテーブルの再配置](/join-reorder.md)
