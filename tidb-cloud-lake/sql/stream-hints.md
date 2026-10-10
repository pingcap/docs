---
title: WITH Stream Hints
summary: ヒントを使用してさまざまなストリーム設定オプションを指定し、ストリームの処理方法を制御します。
---

# WITH Stream Hints

ヒントを使用してさまざまなストリーム設定オプションを指定し、ストリームの処理方法を制御します。

関連情報: [WITH CONSUME](/tidb-cloud-lake/sql/with-consume.md)

## 構文 {#syntax}

```sql
SELECT ...
FROM <stream_name> WITH (<hint1> = <value1>[, <hint2> = <value2>, ...])
```

以下に、利用可能なヒント、その説明、およびストリーム処理を最適化するための推奨される使用方法を示します。

| Hint             | 説明                                                                                                                                                                               |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `CONSUME`        | このクエリがストリームを消費するかどうかを指定します。デフォルトは `False` です。                                                                                                                |
| `MAX_BATCH_SIZE` | ストリームから処理される各バッチの最大行数を定義します。<br/>- 指定しない場合、ストリーム内のすべての行が処理されます。<br/>- 同一のストリームに対して、1つのトランザクション内で `MAX_BATCH_SIZE` を変更することはできず、エラーになります。<br/>- 長期間消費されていないストリームのように、変更のバックログが大量にあるストリームでは、`MAX_BATCH_SIZE` を設定すること、または小さい値を使用することは、キャプチャ効率を低下させる可能性があるため、*推奨されません*。 |

## 例 {#examples}

デモの前に、テーブルを作成し、その上にストリームを定義して、2 行のデータを挿入します。

```sql
CREATE TABLE t1(a int);
CREATE STREAM s ON TABLE t1;
INSERT INTO t1 values(1);
INSERT INTO t1 values(2);
```

以下は、ストリームをクエリする際に `MAX_BATCH_SIZE` ヒントが各バッチで処理される行数にどのように影響するかを示しています。`MAX_BATCH_SIZE` を 1 に設定すると、各バッチには 1 行のみが含まれます。一方、2 に設定すると、2 行とも 1 つのバッチで処理されます。

```sql
SELECT * FROM s WITH (CONSUME = FALSE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 1
   change$action: INSERT
change$is_update: false
   change$row_id: de75bebeeb6b4a54bfe05d4d14c83757000000

SELECT * FROM s WITH (CONSUME = FALSE, MAX_BATCH_SIZE = 2);

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│        a        │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│               2 │ INSERT        │ false            │ d2c02e411db84d269dc9f6e32d8444bc000000 │
│               1 │ INSERT        │ false            │ de75bebeeb6b4a54bfe05d4d14c83757000000 │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

以下は、ストリームをクエリする際に `CONSUME` ヒントがどのように動作するかを示しています。`CONSUME = TRUE` かつ `MAX_BATCH_SIZE = 1` の場合、各クエリはストリームから 1 行を消費します。

```sql
SELECT * FROM s WITH (CONSUME = TRUE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 1
   change$action: INSERT
change$is_update: false
   change$row_id: de75bebeeb6b4a54bfe05d4d14c83757000000

SELECT * FROM s WITH (CONSUME = TRUE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 2
   change$action: INSERT
change$is_update: false
   change$row_id: d2c02e411db84d269dc9f6e32d8444bc000000
```