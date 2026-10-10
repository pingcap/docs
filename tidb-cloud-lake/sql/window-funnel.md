---
title: WINDOW_FUNNEL
summary: ファネル分析。
---

# WINDOW_FUNNEL

`WINDOW_FUNNEL` 関数は、ClickHouse の `windowFunnel` と同様に（同じ作者によって作成されています）、スライディング時間ウィンドウ内でイベントチェーンを検索し、そのチェーン内で成立したイベントの最大数を計算します。

この関数は、次のアルゴリズムに従って動作します。

- 関数は、チェーン内の最初の条件を満たすデータを検索し、イベントカウンターを 1 に設定します。これがスライディングウィンドウの開始時点です。

- チェーン内のイベントがウィンドウ内で順番どおりに発生した場合、カウンターが増加します。イベントの順序が途切れた場合、カウンターは増加しません。

- データに、完了段階の異なる複数のイベントチェーンが含まれている場合、この関数は最も長いチェーンの長さのみを出力します。

```sql
WINDOW_FUNNEL( <window> )( <timestamp>, <cond1>, <cond2>, ..., <condN> )
```

**Arguments**

- `<timestamp>` — タイムスタンプを含むカラム名です。サポートされるデータ型: 整数型および datetime 型。
- `<cond>` — イベントチェーンを表す条件またはデータです。`Boolean` データ型である必要があります。

**Parameters**

- `<window>` — スライディングウィンドウの長さで、最初の条件と最後の条件の間の時間間隔です。`window` の単位は `timestamp` 自体に依存し、状況によって異なります。`timestamp of cond1 <= timestamp of cond2 <= ... <= timestamp of condN <= timestamp of cond1 + window` という式によって決定されます。

**Returned value**

スライディング時間ウィンドウ内で、チェーンから連続して成立した条件の最大数です。選択されたすべてのチェーンが分析されます。

型: `UInt8`。

**Example**

オンラインストアで、ユーザーがスマートフォンを SELECT して 2 回購入するのに、一定の時間が十分かどうかを判定します。

次のイベントチェーンを設定します。

1. ユーザーがストアのアカウントにログインした (`event_name = 'login'`)。
2. ユーザーがページにアクセスした (`event_name = 'visit'`)。
3. ユーザーがショッピングカートに追加した (`event_name = 'cart'`)。
4. ユーザーが購入を完了した (`event_name = 'purchase'`)。

```sql
CREATE TABLE events(user_id BIGINT, event_name VARCHAR, event_timestamp TIMESTAMP);

INSERT INTO events VALUES(100123, 'login', '2022-05-14 10:01:00');
INSERT INTO events VALUES(100123, 'visit', '2022-05-14 10:02:00');
INSERT INTO events VALUES(100123, 'cart', '2022-05-14 10:04:00');
INSERT INTO events VALUES(100123, 'purchase', '2022-05-14 10:10:00');

INSERT INTO events VALUES(100125, 'login', '2022-05-15 11:00:00');
INSERT INTO events VALUES(100125, 'visit', '2022-05-15 11:01:00');
INSERT INTO events VALUES(100125, 'cart', '2022-05-15 11:02:00');

INSERT INTO events VALUES(100126, 'login', '2022-05-15 12:00:00');
INSERT INTO events VALUES(100126, 'visit', '2022-05-15 12:01:00');
```

入力テーブル:

```sql
+---------+------------+----------------------------+
| user_id | event_name | event_timestamp            |
+---------+------------+----------------------------+
|  100123 | login      | 2022-05-14 10:01:00.000000 |
|  100123 | visit      | 2022-05-14 10:02:00.000000 |
|  100123 | cart       | 2022-05-14 10:04:00.000000 |
|  100123 | purchase   | 2022-05-14 10:10:00.000000 |
|  100125 | login      | 2022-05-15 11:00:00.000000 |
|  100125 | visit      | 2022-05-15 11:01:00.000000 |
|  100125 | cart       | 2022-05-15 11:02:00.000000 |
|  100126 | login      | 2022-05-15 12:00:00.000000 |
|  100126 | visit      | 2022-05-15 12:01:00.000000 |
+---------+------------+----------------------------+
```

1 時間のスライディングウィンドウ内で、ユーザー `user_id` がチェーンのどこまで到達できたかを調べます。

クエリ:

```sql
SELECT
    level,
    count() AS count
FROM
(
    SELECT
        user_id,
        window_funnel(3600000000)(event_timestamp, event_name = 'login', event_name = 'visit', event_name = 'cart', event_name = 'purchase') AS level
    FROM events
    GROUP BY user_id
)
GROUP BY level ORDER BY level ASC;
```

> **Tip:**
>
> `event_timestamp` の型は timestamp であり、`3600000000` は 1 時間の時間ウィンドウです。

結果:

```sql
+-------+-------+
| level | count |
+-------+-------+
|     2 |     1 |
|     3 |     1 |
|     4 |     1 |
+-------+-------+
```

- ユーザー `100126` の level は 2 (`login -> visit`) です。
- ユーザー `100125` の level は 3 (`login -> visit -> cart`) です。
- ユーザー `100123` の level は 4 (`login -> visit -> cart -> purchase`) です。