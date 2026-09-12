---
title: Map
summary: `MAP(K, V)` 以 `ARRAY(TUPLE(key, value))` 的形式在内部存储键值对。需要预先定义键类型 `K`（Boolean、numeric、decimal、string、date 或 timestamp）。键必须为非空且唯一；值可以是任意类型，包括嵌套结构。可以使用 map 字面量（`{key: value}`）或 `MAP(keys, values)` 函数来构建 map 表达式。
---

# Map

## 概述 {#overview}

`MAP(K, V)` 以 `ARRAY(TUPLE(key, value))` 的形式在内部存储键值对。需要预先定义键类型 `K`（Boolean、numeric、decimal、string、date 或 timestamp）。键必须为非空且唯一；值可以是任意类型，包括嵌套结构。可以使用 map 字面量（`{key: value}`）或 `MAP(keys, values)` 函数来构建 map 表达式。

```sql
SELECT
  {'k1': 1, 'k2': 2}                      AS literal_map,
  MAP(['x', 'y'], [10, 20])               AS from_arrays;
```

结果：

```
┌───────────────────────┬──────────────────┐
│ literal_map           │ from_arrays      │
├───────────────────────┼──────────────────┤
│ {'k1':1,'k2':2}       │ {'x':10,'y':20}  │
└───────────────────────┴──────────────────┘
```

## 示例 {#examples}

### 创建和查询 {#create-and-query}

```sql
CREATE TABLE web_traffic_data (
  id INT64,
  traffic_info MAP(STRING, STRING)
);

INSERT INTO web_traffic_data VALUES
  (1, {'ip': '192.168.1.1', 'url': 'example.com/home'}),
  (2, {'ip': '192.168.1.2', 'url': 'example.com/about'}),
  (3, {'ip': '192.168.1.1', 'url': 'example.com/contact'});

SELECT
  id,
  traffic_info['ip']  AS ip_address,
  traffic_info['url'] AS url
FROM web_traffic_data;
```

结果：

```
┌────┬─────────────┬───────────────────────┐
│ id │ ip_address  │ url                   │
├────┼─────────────┼───────────────────────┤
│ 1  │ 192.168.1.1 │ example.com/home      │
│ 2  │ 192.168.1.2 │ example.com/about     │
│ 3  │ 192.168.1.1 │ example.com/contact   │
└────┴─────────────┴───────────────────────┘
```

```sql
SELECT
  traffic_info['ip'] AS ip_address,
  COUNT(*)           AS visits
FROM web_traffic_data
GROUP BY traffic_info['ip']
ORDER BY visits DESC;
```

结果：

```
┌─────────────┬────────┐
│ ip_address  │ visits │
├─────────────┼────────┤
│ 192.168.1.1 │      2 │
│ 192.168.1.2 │      1 │
└─────────────┴────────┘
```

### 布隆过滤器索引 {#bloom-filter-index}

Map 列会针对受支持的值类型（numeric、string、timestamp、date）自动维护布隆过滤器。在 `map['key']` 上进行过滤时，如果该值不存在，可以快速跳过数据块。

```sql
CREATE TABLE nginx_log (
  id INT,
  log MAP(STRING, STRING)
);

INSERT INTO nginx_log VALUES
  (1, {'ip': '205.91.162.148', 'url': 'test-1'}),
  (2, {'ip': '205.91.162.141', 'url': 'test-2'});
```

```sql
SELECT *
FROM nginx_log
WHERE log['ip'] = '205.91.162.148';
```

结果：

```
┌────┬─────────────────────────────────────────┐
│ id │ log                                     │
├────┼─────────────────────────────────────────┤
│ 1  │ {'ip':'205.91.162.148','url':'test-1'}  │
└────┴─────────────────────────────────────────┘
```

```sql
SELECT *
FROM nginx_log
WHERE log['ip'] = '205.91.162.200';
```

结果：

```
┌────┬────┐
│ id │ log │
├────┼────┤
└────┴────┘
```