---
title: CLUSTERING_INFORMATION
summary: 返回表的聚簇信息。
---

# CLUSTERING_INFORMATION

返回表的聚簇信息。

## 语法 {#syntax}

```sql
CLUSTERING_INFORMATION('<database_name>', '<table_name>')
```

## 示例 {#examples}

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

| 参数                | 描述                                                                                                             |
|------------------------- |------------------------------------------------------------------------------------------------------------------------ |
| cluster_key          | 已定义的 cluster key。                                                                                                |
| total_block_count        | 当前块的数量。                                                                                            |
| constant_block_count     | min/max 值相等的块数量，这意味着每个块仅包含一个（一组）cluster_key 值。  |
| unclustered_block_count  | 尚未完成聚簇的块数量。                                                                   |
| average_overlaps         | 给定范围内重叠块的平均比例。                                                           |
| average_depth            | cluster key 的重叠分区的平均深度。                                                        |
| block_depth_histogram    | 每个深度级别上的分区数量。较低深度上的分区越集中，表示表聚簇效果越好。                                                                           |