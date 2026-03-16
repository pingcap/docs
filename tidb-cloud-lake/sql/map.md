---
title: Map
sidebar_position: 10
---

## Overview

`MAP(K, V)` stores key-value pairs internally as `ARRAY(TUPLE(key, value))`. Define the key type `K` up front (Boolean, numeric, decimal, string, date, or timestamp). Keys must be non-null and unique; values can be any type, including nested structures. Use map literals (`{key: value}`) or the `MAP(keys, values)` function to build a map expression.

```sql
SELECT
  {'k1': 1, 'k2': 2}                      AS literal_map,
  MAP(['x', 'y'], [10, 20])               AS from_arrays;
```

Result:
```
┌───────────────────────┬──────────────────┐
│ literal_map           │ from_arrays      │
├───────────────────────┼──────────────────┤
│ {'k1':1,'k2':2}       │ {'x':10,'y':20}  │
└───────────────────────┴──────────────────┘
```

## Examples

### Create and Query

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

Result:
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

Result:
```
┌─────────────┬────────┐
│ ip_address  │ visits │
├─────────────┼────────┤
│ 192.168.1.1 │      2 │
│ 192.168.1.2 │      1 │
└─────────────┴────────┘
```

### Bloom Filter Index

Map columns automatically maintain a bloom filter for supported value types (numeric, string, timestamp, date). Filtering on `map['key']` skips blocks quickly when the value is absent.

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

Result:
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

Result:
```
┌────┬────┐
│ id │ log │
├────┼────┤
└────┴────┘
```
