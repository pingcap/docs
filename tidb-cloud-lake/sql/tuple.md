---
title: Tuple
summary: Tuple は、順序付けられた不変の型のコレクションです。
---

# Tuple

## 概要 {#overview}

`TUPLE(T1, T2, …)` は、宣言された要素型を持つ固定長の順序付き値リストを格納します。各タプル値には異種のデータ（たとえば `TUPLE(DATETIME, STRING)`）を保持でき、コンパクトな struct のように振る舞います。タプルは不変であるため、内容を変更する必要がある場合は、タプル値全体を挿入してください。

## 例 {#examples}

### 作成と挿入 {#create-and-insert}

```sql
CREATE TABLE events_tuple (
  event_info TUPLE(DATETIME, STRING)
);

INSERT INTO events_tuple VALUES
  (('2023-02-14 08:00:00', 'Valentine''s Day')),
  (('2023-03-17 19:30:00', 'Game Night'));

SELECT event_info FROM events_tuple;
```

結果:

```
┌──────────────────────────────────────────────────────┐
│ event_info                                           │
├──────────────────────────────────────────────────────┤
│ ["2023-02-14T08:00:00","Valentine's Day"]            │
│ ["2023-03-17T19:30:00","Game Night"]                 │
└──────────────────────────────────────────────────────┘
```

### 要素へのアクセス {#access-elements}

タプルのフィールドは、1 始まりの序数アクセス（`tuple_column.1`）を使用するか、要素に名前を付けた場合はエイリアスを使用します。

```sql
-- Ordinal access
SELECT
  event_info.1 AS event_time,
  event_info.2 AS description
FROM events_tuple;
```

結果:

```
┌──────────────────────────┬──────────────────┐
│ event_time               │ description      │
├──────────────────────────┼──────────────────┤
│ 2023-02-14T08:00:00      │ Valentine's Day  │
│ 2023-03-17T19:30:00      │ Game Night       │
└──────────────────────────┴──────────────────┘
```

タプルは、追加のテーブルカラムを導入せずに、グループ化された値を SQL 式の中で受け渡す必要がある場合に便利です。