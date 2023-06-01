---
title: SQL Logical Optimization
---

# SQL論理最適化 {#sql-logical-optimization}

この章では、TiDB が最終的なクエリ プランを生成する方法を理解するのに役立ついくつかの重要なロジックの書き換えについて説明します。たとえば、TiDB で`select * from t where t.a in (select t1.a from t1 where t1.b=t.b)`クエリを実行すると、TiDB がここでいくつかの書き換えを行っているため、 `IN`サブクエリ`t.a in (select t1.a from t1 where t1.b=t.b)`が存在しないことがわかります。

この章では、次の主要な書き換えを紹介します。

-   [<a href="/subquery-optimization.md">サブクエリ関連の最適化</a>](/subquery-optimization.md)
-   [<a href="/column-pruning.md">カラムの剪定</a>](/column-pruning.md)
-   [<a href="/correlated-subquery-optimization.md">相関サブクエリの相関解除</a>](/correlated-subquery-optimization.md)
-   [<a href="/max-min-eliminate.md">最大値/最小値の削除</a>](/max-min-eliminate.md)
-   [<a href="/predicate-push-down.md">Predicate Push Down</a>](/predicate-push-down.md)
-   [<a href="/partition-pruning.md">パーティションのプルーニング</a>](/partition-pruning.md)
-   [<a href="/topn-limit-push-down.md">TopN およびリミット演算子のプッシュダウン</a>](/topn-limit-push-down.md)
-   [<a href="/join-reorder.md">結合したテーブルの再配置</a>](/join-reorder.md)
