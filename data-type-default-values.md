---
title: TiDB Data Type
summary: TiDB のデータ型のデフォルト値について学習します。
---

# デフォルト値 {#default-values}

データ型仕様の`DEFAULT`値句は、列のデフォルト値を示します。

すべてのデータ型にデフォルト値を設定できます。通常、デフォルト値は定数である必要があり、関数や式にすることはできませんが、例外がいくつかあります。

-   時間型の場合、 `TIMESTAMP`と`DATETIME`列のデフォルト値として`NOW` 、 `CURRENT_TIMESTAMP` 、 `LOCALTIME` 、および`LOCALTIMESTAMP`関数を使用できます。
-   整数型の場合、 `NEXT VALUE FOR`関数を使用してシーケンスの次の値を列のデフォルト値として設定し、 [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md)関数を使用してランダムな浮動小数点値を列のデフォルト値として生成できます。
-   文字列型の場合、 [`UUID()`](/functions-and-operators/miscellaneous-functions.md)関数を使用して、列のデフォルト値として[ユニバーサルユニーク識別子 (UUID)](/best-practices/uuid.md)を生成できます。
-   バイナリ型の場合、 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md)関数を使用して UUID をバイナリ形式に変換し、変換された値を列のデフォルト値として設定できます。
-   v8.0.0 以降、TiDB は[`BLOB`](/data-type-string.md#blob-type) 、 [`TEXT`](/data-type-string.md#text-type) 、および[`JSON`](/data-type-json.md#json-type)データ型に対して[デフォルト値を指定する](#specify-expressions-as-default-values)追加でサポートしますが、それらに対して[デフォルト値](#default-values)を設定するには式のみを使用できます。

列定義に明示的な`DEFAULT`値が含まれていない場合、TiDB は次のようにデフォルト値を決定します。

-   列が値として`NULL`を取ることができる場合、列は明示的な`DEFAULT NULL`句で定義されます。
-   列が値として`NULL`を取ることができない場合、TiDB は明示的な`DEFAULT`句なしで列を定義します。

明示的な`DEFAULT`句のない`NOT NULL`列へのデータ入力の場合、 `INSERT`または`REPLACE`ステートメントに列の値が含まれていない場合、TiDB はその時点で有効な SQL モードに従って列を処理します。

-   厳密な SQL モードが有効になっている場合、トランザクション テーブルではエラーが発生し、ステートメントはロールバックされます。非トランザクション テーブルではエラーが発生します。
-   厳密モードが有効になっていない場合、TiDB は列を列データ型の暗黙的なデフォルト値に設定します。

暗黙のデフォルトは次のように定義されます。

-   数値型の場合、デフォルトは`AUTO_INCREMENT`です。1 属性で宣言された場合、デフォルトはシーケンス内の次の値になります。
-   `TIMESTAMP`以外の日付と時刻の型の場合、デフォルトはその型に適切な「ゼロ」値です。 `TIMESTAMP`の場合、デフォルト値は現在の日付と時刻です。
-   `ENUM`以外の文字列型の場合、デフォルト値は空の文字列です。 `ENUM`の場合、デフォルト値は最初の列挙値です。

## 式をデフォルト値として指定する {#specify-expressions-as-default-values}

MySQL 8.0.13 以降では、 `DEFAULT`句でデフォルト値として式を指定できるようになりました。詳細については、 [MySQL 8.0.13 以降の明示的なデフォルト処理](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html#data-type-defaults-explicit)を参照してください。

v8.0.0 以降、TiDB は`DEFAULT`句のデフォルト値として次の式を指定することもサポートします。

-   `UPPER(SUBSTRING_INDEX(USER(), '@', 1))`
-   `REPLACE(UPPER(UUID()), '-', '')`
-   次の形式の`DATE_FORMAT`式:
    -   `DATE_FORMAT(NOW(), '%Y-%m')`
    -   `DATE_FORMAT(NOW(), '%Y-%m-%d')`
    -   `DATE_FORMAT(NOW(), '%Y-%m-%d %H.%i.%s')`
    -   `DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')`
-   `STR_TO_DATE('1980-01-01', '%Y-%m-%d')`

v8.0.0 以降、TiDB は`BLOB` 、 `TEXT` 、 `JSON`データ型にデフォルト値を割り当てることもサポートしています。ただし、これらのデータ型のデフォルト値を設定するには、式のみを使用できます。以下は`BLOB`の例です。

```sql
CREATE TABLE t2 (b BLOB DEFAULT (RAND()));
```
