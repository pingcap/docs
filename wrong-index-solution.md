---
title: Wrong Index Solution
summary: Learn how to solve the wrong index issue.
---

# インデックス問題の解決方法 {#wrong-index-solution}

一部のクエリの実行速度が期待に達していないことがわかった場合、オプティマイザはクエリを実行するために間違ったインデックスを選択する可能性があります。

最初に統計で[テーブルのヘルス状態](/statistics.md#health-state-of-tables)表示してから、さまざまな健康状態に応じてこの問題を解決できます。

## 低健康状態 {#low-health-state}

低ヘルス状態は、TiDB が`ANALYZE`ステートメントを長期間実行していないことを意味します。 `ANALYZE`コマンドを実行して、統計を更新できます。更新後、オプティマイザーがまだ間違ったインデックスを使用している場合は、次のセクションを参照してください。

## ほぼ 100% の健康状態 {#near-100-health-state}

ほぼ 100% の正常性状態は、 `ANALYZE`ステートメントが完了したばかりか、少し前に完了したことを示しています。この場合、間違ったインデックスの問題は、TiDB の行数の見積もりロジックに関連している可能性があります。

等価クエリの場合、原因は[カウントミンスケッチ](/statistics.md#count-min-sketch)である可能性があります。 Count-Min Sketch が原因であるかどうかを確認し、対応する解決策を講じることができます。

上記の原因が問題に当てはまらない場合は、 `USE_INDEX`または`use index`オプティマイザー ヒントを使用してインデックスを強制選択できます (詳細については、 [USE_INDEX](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)参照してください)。また、邪魔にならない方法で[SQL計画管理](/sql-plan-management.md)を使用して、クエリの動作を変更することもできます。

## その他の状況 {#other-situations}

前述の状況とは別に、不適切なインデックスの問題は、すべてのインデックスが適用できなくなるデータ更新によって引き起こされる場合もあります。このような場合、条件とデータ分布を分析して、新しいインデックスがクエリを高速化できるかどうかを確認する必要があります。その場合は、 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)コマンドを実行して新しいインデックスを追加できます。
