---
title: Wrong Index Solution
summary: Learn how to solve the wrong index issue.
---

# インデックス問題の解決方法 {#wrong-index-solution}

一部のクエリの実行速度が期待に達していないことが判明した場合、オプティマイザはクエリを実行するために間違ったインデックスを選択する可能性があります。

まず統計の[テーブルの健全性状態](/statistics.md#health-state-of-tables)確認してから、さまざまな健康状態に応じてこの問題を解決できます。

## 健康状態が低い {#low-health-state}

健全性状態が低いということは、TiDB が`ANALYZE`ステートメントを長期間実行していないことを意味します。 `ANALYZE`コマンドを実行すると、統計を更新できます。更新後もオプティマイザーが間違ったインデックスを使用する場合は、次のセクションを参照してください。

## 100% に近い健康状態 {#near-100-health-state}

ほぼ 100% の健全性状態は、 `ANALYZE`ステートメントが完了したばかりか、少し前に完了したことを示しています。この場合、間違ったインデックスの問題は、TiDB の行数の推定ロジックに関連している可能性があります。

等価性クエリの場合、原因は[カウントミニスケッチ](/statistics.md#count-min-sketch)である可能性があります。 Count-Min Sketch が原因かどうかを確認し、対応する解決策を講じることができます。

上記の原因が問題に当てはまらない場合は、 `USE_INDEX`または`use index`オプティマイザー ヒントを使用してインデックスを強制的に選択できます (詳細については[USE_INDEX](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)を参照)。また、非侵入的な方法で[SQL計画管理](/sql-plan-management.md)を使用してクエリの動作を変更することもできます。

## その他の状況 {#other-situations}

前述の状況とは別に、間違ったインデックスの問題は、すべてのインデックスが適用できなくなるデータ更新によって引き起こされる可能性もあります。このような場合は、条件とデータ分布を分析して、新しいインデックスによってクエリが高速化できるかどうかを確認する必要があります。その場合は、 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)コマンドを実行して新しいインデックスを追加できます。
