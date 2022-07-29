---
title: Wrong Index Solution
summary: Learn how to solve the wrong index issue.
---

# インデックス問題の解決方法 {#wrong-index-solution}

一部のクエリの実行速度が期待に達していないことがわかった場合、オプティマイザはクエリを実行するために間違ったインデックスを選択する可能性があります。

最初に統計で[テーブルのヘルス状態](/statistics.md#health-state-of-tables)を表示してから、さまざまなヘルス状態に従ってこの問題を解決できます。

## 低健康状態 {#low-health-state}

ヘルス状態が低いということは、TiDBが`ANALYZE`ステートメントを長い間実行していないことを意味します。 `ANALYZE`コマンドを実行すると、統計を更新できます。更新後もオプティマイザが間違ったインデックスを使用している場合は、次のセクションを参照してください。

## ほぼ100％の健康状態 {#near-100-health-state}

ほぼ100％のヘルス状態は、 `ANALYZE`のステートメントが完了したばかりか、少し前に完了したことを示しています。この場合、間違ったインデックスの問題は、行数のTiDBの推定ロジックに関連している可能性があります。

等価クエリの場合、原因は[カウント-最小スケッチ](/statistics.md#count-min-sketch)である可能性があります。 Count-Min Sketchが原因であるかどうかを確認し、対応する解決策をとることができます。

上記の原因が問題に当てはまらない場合は、 `USE_INDEX`または`use index`のオプティマイザーヒントを使用してインデックスを強制的に選択できます（詳細については[USE_INDEX](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)を参照）。また、邪魔にならない方法で[SQL計画管理](/sql-plan-management.md)を使用することにより、クエリの動作を変更できます。

## その他の状況 {#other-situations}

前述の状況とは別に、誤ったインデックスの問題は、すべてのインデックスを適用できなくなるデータの更新によっても発生する可能性があります。このような場合、条件とデータ分散の分析を実行して、新しいインデックスがクエリを高速化できるかどうかを確認する必要があります。その場合は、 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)コマンドを実行して新しいインデックスを追加できます。
