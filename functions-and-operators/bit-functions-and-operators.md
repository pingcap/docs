---
title: Bit Functions and Operators
summary: Learn about the bit functions and operators.
aliases: ['/docs/dev/functions-and-operators/bit-functions-and-operators/','/docs/dev/reference/sql/functions-and-operators/bit-functions-and-operators/']
---

# Bit Functions and Operators

TiDB supports all of the [bit functions and operators](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html) available in MySQL 8.0.

**Bit functions and operators:**

| Name | Description |
| :------| :------------- |
| [`BIT_COUNT()`](#bit_count) | Return the number of bits that are set as 1 |
| [&](#bitwise-and-) | Bitwise AND |
| [~](#bitwise-inversion-) | Bitwise inversion |
| [\|](#bitwise-or-) | Bitwise OR |
| [^](#bitwise-xor- | Bitwise XOR |
| [<<](#left-shift-) | Left shift |
| [>>](#right-shift-) | Right shift |

## [`BIT_COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#function_bit-count)

The `BIT_COUNT(expr)` function returns the number of bits of `expr` that are set to 1.

```sql
SELECT BIT_COUNT(b'00101001');
```

```
+------------------------+
| BIT_COUNT(b'00101001') |
+------------------------+
|                      3 |
+------------------------+
1 row in set (0.00 sec)
```

> **Note:**
>
> In the example above a bit-literal is used. Using a regular string with `0`'s' and `1`'s will give a different result.

The following example is similar to the example above, but it uses a hex-literal instead of a bit-literal. The `CONV()` function shows that `0x29` (hex, base 16) is the same as `00101001` (binary, base 2).

```sql
SELECT BIT_COUNT(0x29), CONV(0x29,16, 2);
```

```
+-----------------+------------------+
| BIT_COUNT(0x29) | CONV(0x29,16, 2) |
+-----------------+------------------+
|               3 | 101001           |
+-----------------+------------------+
1 row in set (0.00 sec)
```

A practical use of this function is to convert a netmask to a [CIDR](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation. In this example the `255.255.255.0` netmask is converted to `/24`.

```sql
SELECT BIT_COUNT(INET_ATON('255.255.255.0'));
```

```
+---------------------------------------+
| BIT_COUNT(INET_ATON('255.255.255.0')) |
+---------------------------------------+
|                                    24 |
+---------------------------------------+
1 row in set (0.00 sec)
```

## [Bitwise AND: &](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-and)

The `&` operator does a bitwise-and operation.

For example, if we do a bitwise-and between `1010` and `1100` the result is `1000` because the only bit that is set by both is the left-most bit.

```
1010
1100
----
1000
```

And now the same example, but with using SQL:

```sql
SELECT CONV(b'1010' & b'1000',10,2);
```

```
+------------------------------+
| CONV(b'1010' & b'1000',10,2) |
+------------------------------+
| 1000                         |
+------------------------------+
1 row in set (0.00 sec)
```

With the `&` operator and the `INET_NTOA()` and `INET_ATON()` functions one can do a bitwise and of an IP-address and a network mask to get the network address. This can be used to tell if multiple IP-addresses are in the same network or not.

```sql
SELECT INET_NTOA(INET_ATON('192.168.1.1') & INET_ATON('255.255.255.0'));
```

```
+------------------------------------------------------------------+
| INET_NTOA(INET_ATON('192.168.1.1') & INET_ATON('255.255.255.0')) |
+------------------------------------------------------------------+
| 192.168.1.0                                                      |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT INET_NTOA(INET_ATON('192.168.1.2') & INET_ATON('255.255.255.0'));
```

```
+------------------------------------------------------------------+
| INET_NTOA(INET_ATON('192.168.1.2') & INET_ATON('255.255.255.0')) |
+------------------------------------------------------------------+
| 192.168.1.0                                                      |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [Bitwise inversion: ~](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-invert)

The `~` operator does a bitwise inversion of the given value.

The value is expanded to 64 bits before the operation.

In this example you can see the expansion to 64-bits and the inversion:

```
value:                                                    1111000011110000
inverted: 1111111111111111111111111111111111111111111111110000111100001111
```

The same inversion and expansion, but in SQL:

```
SELECT CONV(~ b'1111000011110000',10,2);
+------------------------------------------------------------------+
| CONV(~ b'1111000011110000',10,2)                                 |
+------------------------------------------------------------------+
| 1111111111111111111111111111111111111111111111110000111100001111 |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

Note that this operation can be reversed by inverting the result again:

```sql
SELECT CONV(~ b'1111111111111111111111111111111111111111111111110000111100001111',10,2);
```

```
+----------------------------------------------------------------------------------+
| CONV(~ b'1111111111111111111111111111111111111111111111110000111100001111',10,2) |
+----------------------------------------------------------------------------------+
| 1111000011110000                                                                 |
+----------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [Bitwise OR: \|](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-or)

The `|` operator does a bitwise-or.

For example a bitwise-or of `1010` and `1100` returns `1110` as the first 3 bits are set in either the first or second value but neither value sets the last bit.

```
1010
1100
----
1110
```

An the same in SQL:

```sql
SELECT CONV(b'1010' | b'1100',10,2);
```

```
+------------------------------+
| CONV(b'1010' | b'1100',10,2) |
+------------------------------+
| 1110                         |
+------------------------------+
1 row in set (0.00 sec)
```

## [Bitwise XOR: ^](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-xor)

The `^` operator does an bitwise-xor (exclusive or).

For example:

```
1010
1100
----
0110
```

The same in SQL:

```sql
SELECT CONV(b'1010' ^ b'1100',10,2);
```

```
+------------------------------+
| CONV(b'1010' ^ b'1100',10,2) |
+------------------------------+
| 110                          |
+------------------------------+
1 row in set (0.00 sec)
```

Here the value is shown as `110` instead of `0110` as leading zero's are removed.

## [Left shift: <<](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_left-shift)

The `<<` operator does a left shift operation.

In the following example we use `1<<n` to move a value of `1` `n` places to the left.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT 0 AS n
    UNION ALL
    SELECT 1+n FROM cte WHERE n<10
)
SELECT n,1<<n,LPAD(CONV(1<<n,10,2),11,0) FROM cte;
```

```
+------+------+----------------------------+
| n    | 1<<n | LPAD(CONV(1<<n,10,2),11,0) |
+------+------+----------------------------+
|    0 |    1 | 00000000001                |
|    1 |    2 | 00000000010                |
|    2 |    4 | 00000000100                |
|    3 |    8 | 00000001000                |
|    4 |   16 | 00000010000                |
|    5 |   32 | 00000100000                |
|    6 |   64 | 00001000000                |
|    7 |  128 | 00010000000                |
|    8 |  256 | 00100000000                |
|    9 |  512 | 01000000000                |
|   10 | 1024 | 10000000000                |
+------+------+----------------------------+
11 rows in set (0.00 sec)
```

## [Right shift: >>](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_right-shift)

The `>>` operator does a right shift operation.

In the following example we use `1024>>n` to move a value of `1024` (`10000000000` in binary) `n` places to the right.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT 0 AS n
    UNION ALL
    SELECT n+1 FROM cte WHERE n<11
)
SELECT n,1024>>n,LPAD(CONV(1024>>n,10,2),11,0) FROM cte;
```

```
+------+---------+-------------------------------+
| n    | 1024>>n | LPAD(CONV(1024>>n,10,2),11,0) |
+------+---------+-------------------------------+
|    0 |    1024 | 10000000000                   |
|    1 |     512 | 01000000000                   |
|    2 |     256 | 00100000000                   |
|    3 |     128 | 00010000000                   |
|    4 |      64 | 00001000000                   |
|    5 |      32 | 00000100000                   |
|    6 |      16 | 00000010000                   |
|    7 |       8 | 00000001000                   |
|    8 |       4 | 00000000100                   |
|    9 |       2 | 00000000010                   |
|   10 |       1 | 00000000001                   |
|   11 |       0 | 00000000000                   |
+------+---------+-------------------------------+
12 rows in set (0.00 sec)
```

Another example of the right shift operator can be found in how a UNIX timestamp can be extracted from a TiDB [`TSO`](/tso.md) timestamp.

## MySQL compatibility

There are some differences between MySQL 8.0 and earlier versions of MySQL in handling bit functions and operators. TiDB aims to follow the behavior of MySQL 8.0.

## Known issues

In the following cases, the query results in TiDB are the same as MySQL 5.7 but different from MySQL 8.0.

- Bitwise operations with binary arguments. For more information, see [#30637](https://github.com/pingcap/tidb/issues/30637).
- The result of the `BIT_COUNT()` function. For more information, see [#44621](https://github.com/pingcap/tidb/issues/44621).
