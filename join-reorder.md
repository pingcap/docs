---
title: Introduction to Join Reorder
summary: Use the Join Reorder algorithm to join multiple tables in TiDB.
---

# 再注文に結合したテーブルの再配置ための概要 {#introduction-to-join-reorder}

実際のアプリケーションシナリオでは、複数のテーブルを結合するのが一般的です。結合の実行効率は、各テーブルが結合する順序に関連しています。

例えば：

{{< copyable "" >}}

```sql
SELECT * FROM t1, t2, t3 WHERE t1.a=t2.a AND t3.a=t2.a;
```

このクエリでは、テーブルを次の2つの順序で結合できます。

-   t1はt2に結合し、次にt3に結合します
-   t2はt3に結合し、次にt1に結合します

t1とt3のデータ量と分散は異なるため、これら2つの実行順序は異なるパフォーマンスを示す可能性があります。

したがって、オプティマイザには、結合順序を決定するためのアルゴリズムが必要です。現在、TiDBは、欲張りアルゴリズムとも呼ばれる結合したテーブルの再配置アルゴリズムを使用しています。

## 結合したテーブルの再配置アルゴリズムのインスタンス {#instance-of-join-reorder-algorithm}

上記の3つの表（t1、t2、およびt3）を例として取り上げます。

まず、TiDBは結合操作に参加するすべてのノードを取得し、行番号の昇順でノードをソートします。

![join-reorder-1](/media/join-reorder-1.png)

その後、行数が最も少ないテーブルが選択され、他の2つのテーブルとそれぞれ結合されます。 TiDBは、出力結果セットのサイズを比較することにより、結果セットが小さいペアを選択します。

![join-reorder-2](/media/join-reorder-2.png)

次に、TiDBは次の選択ラウンドに入ります。 4つのテーブルを結合しようとすると、TiDBは引き続き出力結果セットのサイズを比較し、結果セットが小さいペアを選択します。

この場合、結合されるテーブルは3つだけなので、TiDBは最終的な結合結果を取得します。

![join-reorder-3](/media/join-reorder-3.png)

上記のプロセスは、現在TiDBで使用されている結合したテーブルの再配置アルゴリズムです。

## 結合したテーブルの再配置アルゴリズムの制限 {#limitations-of-join-reorder-algorithm}

現在の結合したテーブルの再配置アルゴリズムには、次の制限があります。

-   結果セットの計算方法によって制限されるため、アルゴリズムは最適な結合順序を選択することを保証できません。

現在、結合順序を強制するために`STRAIGHT_JOIN`構文がTiDBでサポートされています。詳細については、 [構文要素の説明](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)を参照してください。
