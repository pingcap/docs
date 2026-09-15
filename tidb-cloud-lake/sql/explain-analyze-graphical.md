---
title: EXPLAIN ANALYZE GRAPHICAL
summary: 在浏览器中通过交互式可视化表示分析查询性能。仅在 LakeSQL v0.22.2+ 中可用。
---

# EXPLAIN ANALYZE GRAPHICAL

在浏览器中通过交互式可视化表示分析查询性能。仅在 LakeSQL v0.22.2+ 中可用。

## 语法 {#syntax}

```sql
EXPLAIN ANALYZE GRAPHICAL <statement>
```

## 配置 {#configuration}

将以下内容添加到你的 LakeSQL 配置文件 `~/.config/lakesql/config.toml` 中：

```toml
[server]
bind_address = "127.0.0.1"
auto_open_browser = true
```

## 示例 {#example}

```sql
EXPLAIN ANALYZE GRAPHICAL SELECT l_returnflag, COUNT(*)
FROM lineitem
WHERE l_shipdate <= '1998-09-01'
GROUP BY l_returnflag;
```

输出：

```bash
View graphical online: http://127.0.0.1:8080?perf_id=1
```

这会打开一个交互式视图，显示执行计划、operator 运行时和数据流。

![Graphical Analysis](/media/tidb-cloud-lake/explain-graphical.png)