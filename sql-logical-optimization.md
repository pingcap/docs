---
title: SQL Logical Optimization
summary: SQL論理最適化の章では、TiDBクエリプラン生成における主要なロジック書き換えについて説明します。例えば、IN`サブクエリ「ta in (select t1.a from t1 where t1.b=tb)」はTiDB書き換えにより存在しません。主要な書き換えには、サブクエリ関連の最適化、カラムの剪定、相関サブクエリの非相関化、最大値/最小値の除去、Predicate Push Down、パーティションプルーニング、TopN演算子とLimit演算子のプッシュダウン、結合したテーブルの再配置などがあります。
---

# SQL論理最適化 {#sql-logical-optimization}

この章では、TiDBが最終的なクエリプランを生成する仕組みを理解するために、いくつかの重要なロジックの書き換えについて説明します。例えば、TiDBでクエリ`select * from t where t.a in (select t1.a from t1 where t1.b=t.b)`実行すると、TiDBがここで書き換えを行ったため、サブクエリ`IN` `t.a in (select t1.a from t1 where t1.b=t.b)`存在しないことがわかります。

この章では、次の重要な書き換えについて説明します。

-   [サブクエリ関連の最適化](/subquery-optimization.md)
-   [カラムの剪定](/column-pruning.md)
-   [相関サブクエリの非相関](/correlated-subquery-optimization.md)
-   [最大/最小を排除](/max-min-eliminate.md)
-   [Predicate Push Down](/predicate-push-down.md)
-   [パーティションプルーニング](/partition-pruning.md)
-   [TopN と Limit 演算子のプッシュダウン](/topn-limit-push-down.md)
-   [Join Reorder](/join-reorder.md)
-   [ウィンドウ関数からTopNまたはLimitを導出する](/derive-topn-from-window.md)
