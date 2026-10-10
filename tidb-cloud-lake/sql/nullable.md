---
title: TO_NULLABLE
summary: 値を nullable な等価値に変換します。
---

# TO_NULLABLE

値を nullable な等価値に変換します。

この関数を値に適用すると、その値がすでに NULL 値を保持できるかどうかを確認します。値がすでに NULL 値を保持できる場合、この関数は変更を加えずにその値を返します。

一方、値が NULL 値を保持できない場合、TO_NULLABLE 関数はその値を NULL 値を保持できるように変更します。これは、NULL 値を保持できる構造でその値をラップすることで実現され、以後その値は NULL 値を保持できるようになります。

## 構文 {#syntax}

```sql
TO_NULLABLE(x);
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------------------|
| x         | 元の値です。        |

## 戻り値の型 {#return-type}

入力値と同じデータ型の値を返します。ただし、入力値がすでに nullable でない場合は、nullable コンテナでラップされます。

## 例 {#examples}

```sql
SELECT typeof(3), TO_NULLABLE(3), typeof(TO_NULLABLE(3));

typeof(3)       |to_nullable(3)|typeof(to_nullable(3))|
----------------+--------------+----------------------+
TINYINT UNSIGNED|             3|TINYINT UNSIGNED NULL |

```