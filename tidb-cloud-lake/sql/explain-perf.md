---
title: EXPLAIN PERF
summary: 对查询 CPU 使用情况进行性能分析，并返回一个从当前集群所有节点收集的 HTML 火焰图。
---

# EXPLAIN PERF

`EXPLAIN PERF` 通过捕获堆栈跟踪来执行 CPU 性能分析。该命令会返回一个 HTML 文件，其中包含基于从当前集群所有节点收集的数据生成的火焰图。你可以直接在浏览器中打开此 HTML 文件。

它有助于分析查询性能并帮助识别瓶颈。

## 语法 {#syntax}

```sql
EXPLAIN PERF <statement>
```

## 示例 {#examples}

```shell
lakesql --quote-style never --query="EXPLAIN PERF SELECT avg(number) FROM numbers(10000000)" > demo.html
```

然后，你可以在浏览器中打开 `demo.html` 文件以查看火焰图。

如果查询完成得非常快，可能无法收集到足够的数据，从而导致火焰图为空。