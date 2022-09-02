---
title: Introduction to Join Reorder
summary: Use the Join Reorder algorithm to join multiple tables in TiDB.
---

# 結合したテーブルの再配置の概要 {#introduction-to-join-reorder}

実際のアプリケーション シナリオでは、複数のテーブルを結合するのが一般的です。結合の実行効率は、各テーブルが結合する順序に関連付けられています。

例えば：

{{< copyable "" >}}

```sql
SELECT * FROM t1, t2, t3 WHERE t1.a=t2.a AND t3.a=t2.a;
```

このクエリでは、次の 2 つの順序でテーブルを結合できます。

-   t1 は t2 に参加し、次に t3 に参加します
-   t2 は t3 に参加し、次に t1 に参加します

t1 と t3 はデータ量と分布が異なるため、これら 2 つの実行順序は異なるパフォーマンスを示す可能性があります。

したがって、オプティマイザには結合順序を決定するためのアルゴリズムが必要です。現在、TiDB は、欲張りアルゴリズムとも呼ばれる結合したテーブルの再配置 Reorder アルゴリズムを使用しています。

## 結合したテーブルの再配置アルゴリズムのインスタンス {#instance-of-join-reorder-algorithm}

上記の 3 つのテーブル (t1、t2、および t3) を例に取ります。

まず、TiDB は結合操作に参加するすべてのノードを取得し、ノードを行番号の昇順に並べ替えます。

![join-reorder-1](/media/join-reorder-1.png)

その後、行数が最も少ないテーブルが選択され、他の 2 つのテーブルとそれぞれ結合されます。出力結果セットのサイズを比較することにより、TiDB は結果セットが小さいペアを選択します。

![join-reorder-2](/media/join-reorder-2.png)

その後、TiDB は次の選択ラウンドに入ります。 4 つのテーブルを結合しようとすると、TiDB は引き続き出力結果セットのサイズを比較し、結果セットが小さいペアを選択します。

この場合、3 つのテーブルのみが結合されるため、TiDB は最終的な結合結果を取得します。

![join-reorder-3](/media/join-reorder-3.png)

上記のプロセスは、現在 TiDB で使用されている結合したテーブルの再配置 Reorder アルゴリズムです。

## 結合したテーブルの再配置アルゴリズムの制限 {#limitations-of-join-reorder-algorithm}

現在の結合したテーブルの再配置アルゴリズムには、次の制限があります。

-   結果セットの計算方法によって制限されるため、アルゴリズムは最適な結合順序を選択することを保証できません。
-   現在、 結合したテーブルの再配置アルゴリズムの Outer Join のサポートは、デフォルトで無効になっています。有効にするには、システム変数[`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)の値を`ON`に設定します。

現在、結合順序を強制するために`STRAIGHT_JOIN`構文が TiDB でサポートされています。詳細については、 [構文要素の説明](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)を参照してください。
