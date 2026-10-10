---
title: 変換関数
summary: このページでは、{{{ .lake }}} の変換関数について、参照しやすいように機能別に整理して包括的に説明します。
---

# 変換関数

このページでは、{{{ .lake }}} の変換関数について、参照しやすいように機能別に整理して包括的に説明します。

## 型変換関数 {#type-conversion-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [CAST](/tidb-cloud-lake/sql/cast.md) | 値を指定したデータ型に変換します | `CAST('123' AS INT)` → `123` |
| [TRY_CAST](/tidb-cloud-lake/sql/try-cast.md) | 値を指定したデータ型に安全に変換し、失敗した場合は NULL を返します | `TRY_CAST('abc' AS INT)` → `NULL` |
| [TO_BOOLEAN](/tidb-cloud-lake/sql/to-boolean.md) | 値を BOOLEAN 型に変換します | `TO_BOOLEAN('true')` → `true` |
| [TO_STRING](/tidb-cloud-lake/sql/to-string.md) | 値を STRING 型に変換します | `TO_STRING(123)` → `'123'` |
| [TO_VARCHAR](/tidb-cloud-lake/sql/to-varchar.md) | 値を VARCHAR 型に変換します | `TO_VARCHAR(123)` → `'123'` |
| [TO_TEXT](/tidb-cloud-lake/sql/to-text.md) | 値を TEXT 型に変換します | `TO_TEXT(123)` → `'123'` |

## 数値変換関数 {#numeric-conversion-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [TO_INT8](/tidb-cloud-lake/sql/to-int8.md) | 値を INT8 型に変換します | `TO_INT8('123')` → `123` |
| [TO_INT16](/tidb-cloud-lake/sql/to-int16.md) | 値を INT16 型に変換します | `TO_INT16('123')` → `123` |
| [TO_INT32](/tidb-cloud-lake/sql/to-int32.md) | 値を INT32 型に変換します | `TO_INT32('123')` → `123` |
| [TO_INT64](/tidb-cloud-lake/sql/to-int64.md) | 値を INT64 型に変換します | `TO_INT64('123')` → `123` |
| [TO_UINT8](/tidb-cloud-lake/sql/to-uint8.md) | 値を UINT8 型に変換します | `TO_UINT8('123')` → `123` |
| [TO_UINT16](/tidb-cloud-lake/sql/to-uint16.md) | 値を UINT16 型に変換します | `TO_UINT16('123')` → `123` |
| [TO_UINT32](/tidb-cloud-lake/sql/to-uint32.md) | 値を UINT32 型に変換します | `TO_UINT32('123')` → `123` |
| [TO_UINT64](/tidb-cloud-lake/sql/to-uint64.md) | 値を UINT64 型に変換します | `TO_UINT64('123')` → `123` |
| [TO_FLOAT32](/tidb-cloud-lake/sql/to-float32.md) | 値を FLOAT32 型に変換します | `TO_FLOAT32('123.45')` → `123.45` |
| [TO_FLOAT64](/tidb-cloud-lake/sql/to-float64.md) | 値を FLOAT64 型に変換します | `TO_FLOAT64('123.45')` → `123.45` |

## バイナリおよび特殊変換関数 {#binary-and-specialized-conversion-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [TO_BINARY](/tidb-cloud-lake/sql/to-binary.md) | 値を BINARY 型に変換します | `TO_BINARY('abc')` → `binary value` |
| [TRY_TO_BINARY](/tidb-cloud-lake/sql/try-to-binary.md) | 値を BINARY 型に安全に変換し、失敗した場合は NULL を返します | `TRY_TO_BINARY('abc')` → `binary value` |
| [TO_HEX](/tidb-cloud-lake/sql/to-hex.md) | 値を 16 進文字列に変換します | `TO_HEX(255)` → `'FF'` |
| [TO_VARIANT](/tidb-cloud-lake/sql/to-variant.md) | 値を VARIANT 型に変換します | `TO_VARIANT('{"a": 1}')` → `{"a": 1}` |
| [BUILD_BITMAP](/tidb-cloud-lake/sql/build-bitmap.md) | 整数の配列からビットマップを構築します | `BUILD_BITMAP([1,2,3])` → `bitmap value` |
| [TO_BITMAP](/tidb-cloud-lake/sql/to-bitmap.md) | 値を BITMAP 型に変換します | `TO_BITMAP([1,2,3])` → `bitmap value` |

値をある型から別の型に変換する際は、次の点に注意してください。

- 浮動小数点数、10 進数、または文字列から整数、あるいは小数部を持つ 10 進数に変換する場合、{{{ .lake }}} は値を最も近い整数に丸めます。これは、数値キャスト操作の動作を制御する設定 `numeric_cast_option`（デフォルトは 'rounding'）によって決まります。`numeric_cast_option` を明示的に 'truncating' に設定すると、{{{ .lake }}} は小数部を切り捨て、端数を破棄します。

    ```sql title='Example:'
    SELECT CAST('0.6' AS DECIMAL(10, 0)), CAST(0.6 AS DECIMAL(10, 0)), CAST(1.5 AS INT);

    ┌──────────────────────────────────────────────────────────────────────────────────┐
    │ cast('0.6' as decimal(10, 0)) │ cast(0.6 as decimal(10, 0)) │ cast(1.5 as int32) │
    ├───────────────────────────────┼─────────────────────────────┼────────────────────┤
    │                             1 │                           1 │                  2 │
    └──────────────────────────────────────────────────────────────────────────────────┘

    SET numeric_cast_option = 'truncating';

    SELECT CAST('0.6' AS DECIMAL(10, 0)), CAST(0.6 AS DECIMAL(10, 0)), CAST(1.5 AS INT);

    ┌──────────────────────────────────────────────────────────────────────────────────┐
    │ cast('0.6' as decimal(10, 0)) │ cast(0.6 as decimal(10, 0)) │ cast(1.5 as int32) │
    ├───────────────────────────────┼─────────────────────────────┼────────────────────┤
    │                             0 │                           0 │                  1 │
    └──────────────────────────────────────────────────────────────────────────────────┘
    ```

    次の表は、数値キャスト操作の概要を示したもので、異なるソース数値データ型とターゲット数値データ型の間で可能なキャストをまとめています。なお、String から Integer へのキャストでは、ソース文字列に整数値が含まれている必要があります。

    | ソース型    | ターゲット型 |
    |----------------|-------------|
    | String         | Decimal     |
    | Float          | Decimal     |
    | Decimal        | Decimal     |
    | Float          | Int         |
    | Decimal        | Int         |
    | String (Int)   | Int         |

- {{{ .lake }}} では、式をさまざまな日付および時刻形式に変換するための関数も多数提供しています。詳細は、[日付・時刻関数](/tidb-cloud-lake/sql/date-time-functions.md) を参照してください。