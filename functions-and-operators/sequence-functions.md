---
title: Sequence Functions
summary: このドキュメントでは、TiDB でサポートされているシーケンス関数について説明します。
---

# シーケンス関数 {#sequence-functions}

TiDB のシーケンス関数は、 [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)ステートメントを使用して作成されたシーケンス オブジェクトの値を返すか設定するために使用されます。

| 関数名                                 | 説明                                   |
| :---------------------------------- | :----------------------------------- |
| [`NEXTVAL()`](#nextval)             | シーケンスの次の値を返します。                      |
| [`NEXT VALUE FOR`](#next-value-for) | シーケンスの次の値を返します ( `NEXTVAL()`のエイリアス)。 |
| [`SETVAL()`](#setval)               | シーケンスの現在の値を設定します。                    |
| [`LASTVAL()`](#lastval)             | 現在のセッションでシーケンスによって生成された最後の値を返します。    |

## <code>NEXTVAL()</code> {#code-nextval-code}

`NEXTVAL()`関数は、シーケンスの次の値を返します。

例：

`s1`という名前のシーケンスを作成します。

```sql
CREATE SEQUENCE s1;
```

`s1`から次の値を取得します。

```sql
SELECT NEXTVAL(s1);
```

出力は次のようになります。

    +-------------+
    | NEXTVAL(s1) |
    +-------------+
    |           1 |
    +-------------+
    1 row in set (0.00 sec)

## <code>NEXT VALUE FOR</code> {#code-next-value-for-code}

`NEXT VALUE FOR`関数は[`NEXTVAL()`](#nextval)エイリアスです。

例：

`NEXTVAL()`を使用して`s1`から次の値を取得します。

```sql
SELECT NEXTVAL(s1);
```

出力は次のようになります。

    +-------------+
    | NEXTVAL(s1) |
    +-------------+
    |           2 |
    +-------------+
    1 row in set (0.00 sec)

`NEXT VALUE FOR`を使用して`s1`から次の値を取得します。

```sql
SELECT NEXT VALUE FOR s1;
```

出力は次のようになります。

    +-------------------+
    | NEXT VALUE FOR s1 |
    +-------------------+
    |                 3 |
    +-------------------+
    1 row in set (0.00 sec)

## <code>SETVAL()</code> {#code-setval-code}

`SETVAL(n)`関数は、シーケンスの現在の値を設定します。

例：

`s1`から次の値を取得します。

```sql
SELECT NEXTVAL(s1);
```

出力は次のようになります。

    +-------------+
    | NEXTVAL(s1) |
    +-------------+
    |           4 |
    +-------------+
    1 row in set (0.00 sec)

現在の値`s1`を`10`に設定します。

```sql
SELECT SETVAL(s1, 10);
```

出力は次のようになります。

    +----------------+
    | SETVAL(s1, 10) |
    +----------------+
    |             10 |
    +----------------+
    1 row in set (0.00 sec)

`10`に設定した後、次の値を確認します。

```sql
SELECT NEXTVAL(s1);
```

出力は次のようになります。

    +-------------+
    | NEXTVAL(s1) |
    +-------------+
    |          11 |
    +-------------+
    1 row in set (0.00 sec)

## <code>LASTVAL()</code> {#code-lastval-code}

`LASTVAL()`関数は**、現在のセッションで**シーケンスによって生成された最後の値を返します。

例：

現在のセッションで`s1`によって生成された最後の値を取得します。

```sql
SELECT LASTVAL(s1);
```

出力は次のようになります。

    +-------------+
    | LASTVAL(s1) |
    +-------------+
    |          11 |
    +-------------+
    1 row in set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

MySQL は、 [ISO/IEC 9075-2](https://www.iso.org/standard/76584.html)で定義されているシーケンスを作成および操作するための関数とステートメントをサポートしていません。
