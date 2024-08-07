---
title: SQL Logical Optimization
summary: SQL 論理最適化の章では、TiDB クエリ プラン生成における主要なロジックの書き換えについて説明します。たとえば、IN` サブクエリ `ta in (select t1.a from t1 where t1.b=tb)` は、TiDB の書き換えにより存在しません。主要な書き換えには、サブクエリ関連の最適化、カラムの剪定、相関サブクエリの非相関化、最大値/最小値の除去、Predicate Push Down、パーティションのプルーニング、TopN および Limit 演算子のプッシュ ダウン、結合したテーブルの再配置が含まれます。
---

# SQL 論理最適化 {#sql-logical-optimization}

この章では、TiDB が最終的なクエリ プランを生成する方法を理解するのに役立つ、いくつかの重要なロジックの書き換えについて説明します。たとえば、TiDB で`select * from t where t.a in (select t1.a from t1 where t1.b=t.b)`クエリを実行すると、TiDB がここでいくつかの書き換えを行ったため、 `IN`サブクエリ`t.a in (select t1.a from t1 where t1.b=t.b)`が存在しないことがわかります。

この章では、次の重要な書き換えについて説明します。

-   [サブクエリ関連の最適化](/subquery-optimization.md)
-   [カラムの剪定](/column-pruning.md)
-   [相関サブクエリの非相関](/correlated-subquery-optimization.md)
-   [最大/最小を排除](/max-min-eliminate.md)
-   [Predicate Push Down](/predicate-push-down.md)
-   [パーティションのプルーニング](/partition-pruning.md)
-   [TopN と Limit 演算子のプッシュダウン](/topn-limit-push-down.md)
-   [結合したテーブルの再配置](/join-reorder.md)
-   [ウィンドウ関数から TopN または Limit を導出する](/derive-topn-from-window.md)
