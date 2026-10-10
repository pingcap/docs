---
title: Map
summary: MAP(K, V) は、キーと値のペアを内部的に ARRAY(TUPLE(key, value)) として格納します。キー型 K は事前に定義する必要があり、Boolean、numeric、decimal、string、date、timestamp を指定できます。キーは NULL 不可かつ一意である必要があり、値にはネストした構造を含む任意の型を使用できます。マップ式を構築するには、マップリテラル ({key value}) または MAP(keys, values) 関数を使用します。
---

# Map

## 概要 {#overview}

`MAP(K, V)` は、キーと値のペアを内部的に `ARRAY(TUPLE(key, value))` として格納します。キー型 `K` は事前に定義する必要があり、Boolean、numeric、decimal、string、date、timestamp を指定できます。キーは NULL 不可かつ一意である必要があります。値には、ネストした構造を含む任意の型を使用できます。マップ式を構築するには、マップリテラル（`{key: value}`）または `MAP(keys, values)` 関数を使用します。

```sql
SELECT
  {'k1': 1, 'k2': 2}                      AS literal_map,
  MAP(['x', 'y'], [10, 20])               AS from_arrays;
```

結果:

```
┌───────────────────────┬──────────────────┐
│ literal_map           │ from_arrays      │
├───────────────────────┼──────────────────┤
│ {'k1':1,'k2':2}       │ {'x':10,'y':20}  │
└───────────────────────┴──────────────────┘
```

## 例 {#examples}

### 作成とクエリ {#create-and-query}

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

結果:

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

結果:

```
┌─────────────┬────────┐
│ ip_address  │ visits │
├─────────────┼────────┤
│ 192.168.1.1 │      2 │
│ 192.168.1.2 │      1 │
└─────────────┴────────┘
```

### ブルームフィルターインデックス {#bloom-filter-index}

Map カラムは、サポートされている値型（numeric、string、timestamp、date）に対して自動的にブルームフィルターを管理します。`map['key']` によるフィルタリングでは、値が存在しない場合にブロックをすばやくスキップできます。

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

結果:

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

結果:

```
┌────┬────┐
│ id │ log │
├────┼────┤
└────┴────┘
```