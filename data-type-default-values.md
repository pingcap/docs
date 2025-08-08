---
title: TiDB Data Type
summary: TiDB のデータ型のデフォルト値について学習します。
---

# デフォルト値 {#default-values}

データ型仕様の`DEFAULT`値句は、列のデフォルト値を示します。

すべてのデータ型にデフォルト値を設定できます。通常、デフォルト値は定数でなければならず、関数や式は使用できませんが、いくつか例外があります。

-   時間型の場合、 `TIMESTAMP`と`DATETIME`列のデフォルト値として`NOW` 、 `CURRENT_TIMESTAMP` 、 `LOCALTIME` 、 `LOCALTIMESTAMP`関数を使用できます。
-   整数型の場合、 `NEXT VALUE FOR`関数を使用してシーケンスの次の値を列の既定値として設定し、 [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md)関数を使用してランダムな浮動小数点値を列の既定値として生成できます。
-   文字列型の場合、 [`UUID()`](/functions-and-operators/miscellaneous-functions.md)関数を使用して、列のデフォルト値として[ユニバーサルユニーク識別子 (UUID)](/best-practices/uuid.md)生成できます。
-   バイナリ型の場合、 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md)関数を使用して UUID をバイナリ形式に変換し、変換された値を列のデフォルト値として設定できます。
-   v8.0.0 以降、TiDB は[`BLOB`](/data-type-string.md#blob-type) 、 [`TEXT`](/data-type-string.md#text-type) 、 [`JSON`](/data-type-json.md#json-data-type)データ型に対して[デフォルト値を指定する](#specify-expressions-as-default-values)追加でサポートしますが、それらに対して[デフォルト値](#default-values)設定するには式のみを使用できます。

列定義に明示的な`DEFAULT`値が含まれていない場合、TiDB は次のようにデフォルト値を決定します。

-   列が値として`NULL`取ることができる場合、列は明示的な`DEFAULT NULL`句で定義されます。
-   列が値として`NULL`取ることができない場合は、TiDB は明示的な`DEFAULT`句なしで列を定義します。

明示的な`DEFAULT`節のない`NOT NULL`列へのデータ入力の場合、 `INSERT`または`REPLACE`ステートメントに列の値が含まれていないと、TiDB はその時点で有効な SQL モードに従って列を処理します。

-   厳密なSQLモードが有効になっている場合、トランザクションテーブルではエラーが発生し、文はロールバックされます。非トランザクションテーブルではエラーが発生します。
-   厳密モードが有効になっていない場合、TiDB は列を列データ型の暗黙的なデフォルト値に設定します。

暗黙のデフォルトは次のように定義されます。

-   数値型の場合、デフォルトは 0 です。1 `AUTO_INCREMENT`で宣言された場合、デフォルトはシーケンス内の次の値になります。
-   `TIMESTAMP`以外の日付と時刻型の場合、デフォルト値はその型に適切な「ゼロ」値です。3 `TIMESTAMP`場合、デフォルト値は現在の日付と時刻です。
-   `ENUM`以外の文字列型の場合、デフォルト値は空文字列です。3 `ENUM`場合、デフォルト値は最初の列挙値です。

## 式をデフォルト値として指定する {#specify-expressions-as-default-values}

MySQL 8.0.13以降では、 `DEFAULT`のデフォルト値として式を指定できるようになりました。詳細については、 [MySQL 8.0.13以降の明示的なデフォルト処理](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html#data-type-defaults-explicit)参照してください。

TiDB は、 `DEFAULT`句のデフォルト値として次の式を指定することをサポートしています。

-   `UPPER(SUBSTRING_INDEX(USER(), '@', 1))`
-   `REPLACE(UPPER(UUID()), '-', '')`
-   次の形式の`DATE_FORMAT`式:
    -   `DATE_FORMAT(NOW(), '%Y-%m')`
    -   `DATE_FORMAT(NOW(), '%Y-%m-%d')`
    -   `DATE_FORMAT(NOW(), '%Y-%m-%d %H.%i.%s')`
    -   `DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')`
-   `STR_TO_DATE('1980-01-01', '%Y-%m-%d')`
-   [`CURRENT_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md) ：どちらもデフォルト[`CURRENT_DATE()`](/functions-and-operators/date-and-time-functions.md)小数秒精度（fsp）を使用します
-   [`JSON_OBJECT()`](/functions-and-operators/json-functions.md) [`JSON_ARRAY()`](/functions-and-operators/json-functions.md) [`JSON_QUOTE()`](/functions-and-operators/json-functions.md)
-   [`NEXTVAL()`](/functions-and-operators/sequence-functions.md#nextval)
-   [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md)
-   [`UUID()`](/functions-and-operators/miscellaneous-functions.md#uuid) [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md#uuid_to_bin)
-   [`VEC_FROM_TEXT()`](/vector-search/vector-search-functions-and-operators.md#vec_from_text)

TiDBは、 `BLOB` 、 `TEXT` 、 `JSON`データ型にデフォルト値を割り当てることができます。ただし、これらのデータ型のデフォルト値を定義するには、リテラルではなく式のみを使用できます。以下は`BLOB`の例です。

```sql
CREATE TABLE t2 (
  b BLOB DEFAULT (RAND())
);
```

UUID の使用例:

```sql
CREATE TABLE t3 (
  uuid BINARY(16) DEFAULT (UUID_TO_BIN(UUID())),
  name VARCHAR(255)
);
```

UUID の使用方法の詳細については、 [UUIDを主キーとして使用するベストプラクティス](/best-practices/uuid.md)参照してください。

`JSON`使用例:

```sql
CREATE TABLE t4 (
  id bigint AUTO_RANDOM PRIMARY KEY,
  j json DEFAULT (JSON_OBJECT("a", 1, "b", 2))
);
```

`JSON`に許可されないものの例:

```sql
CREATE TABLE t5 (
  id bigint AUTO_RANDOM PRIMARY KEY,
  j json DEFAULT ('{"a": 1, "b": 2}')
);
```

最後の 2 つの例は同様のデフォルトを示していますが、リテラルではなく式を使用しているため、最初の例のみが有効です。
