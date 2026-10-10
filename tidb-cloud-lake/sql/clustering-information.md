---
title: CLUSTERING_INFORMATION
summary: テーブルのクラスタリング情報を返します。
---

# CLUSTERING_INFORMATION

テーブルのクラスタリング情報を返します。

## 構文 {#syntax}

```sql
CLUSTERING_INFORMATION('<database_name>', '<table_name>')
```

## 例 {#examples}

```sql
CREATE TABLE mytable(a int, b int) CLUSTER BY(a+1);

INSERT INTO mytable VALUES(1,1),(3,3);
INSERT INTO mytable VALUES(2,2),(5,5);
INSERT INTO mytable VALUES(4,4);

SELECT * FROM CLUSTERING_INFORMATION('default','mytable')\G
*************************** 1. row ***************************
            cluster_key: ((a + 1))
      total_block_count: 3
   constant_block_count: 1
unclustered_block_count: 0
       average_overlaps: 1.3333
          average_depth: 2.0
  block_depth_histogram: {"00002":3}
```

| パラメーター                | 説明                                                                                                             |
|------------------------- |------------------------------------------------------------------------------------------------------------------------ |
| cluster_key          | 定義されたクラスターキーです。                                                                                                |
| total_block_count        | 現在のブロック数です。                                                                                            |
| constant_block_count     | min/max 値が等しいブロックの数です。これは、各ブロックに cluster_key 値が 1 つ（または 1 グループ）のみ含まれることを意味します。  |
| unclustered_block_count  | まだクラスタリングされていないブロックの数です。                                                                   |
| average_overlaps         | 指定された範囲内で重複しているブロックの平均比率です。                                                           |
| average_depth            | クラスターキーに対する重複パーティションの平均深度です。                                                        |
| block_depth_histogram    | 各深度レベルにおけるパーティション数です。低い深度にパーティションがより集中しているほど、テーブルのクラスタリングがより効果的であることを示します。                                                                           |