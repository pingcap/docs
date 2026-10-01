---
title: TiDB Cloud Lake 向け Data Pipeline SQL 互換性
summary: TiDB Cloud Data Pipeline における DDL、DML、および TiDB から TiDB Cloud Lake への型マッピング動作のリファレンスです。
---

# TiDB Cloud Lake 向け Data Pipeline SQL 互換性

このドキュメントでは、TiDB Cloud Data Pipeline が TiDB Cloud Lake にデータをレプリケートする際の DDL、DML、およびカラム型のサポートについて説明します。パイプラインの計画、スキーマ互換性の検証、または型変換のトラブルシューティングに利用してください。

> **Note:**
>
> サポートされる動作は、使用している TiCDC と TiDB Cloud Lake のバージョンによって異なります。異なる動作が見られる場合は、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。

## DDL サポートの概要 {#ddl-support-summary}

| DDL 操作 | ステータス | 注記 |
| -------------------- | -----: | ----- |
| `CREATE TABLE` | ✅ |  |
| `ADD COLUMN` | ✅ |  |
| `ADD COLUMN ... NOT NULL DEFAULT ...` | ✅ |  |
| `DROP COLUMN` | ✅ |  |
| `RENAME COLUMN` | ✅ |  |
| `MODIFY COLUMN` | ⚠️ 部分サポート | 以下に示す Schema Evolution のケースのみサポートされます。その他の変換は保証されず、下流での取り込みをブロックする可能性があります。 |

### サポートされる `MODIFY COLUMN` 変換 {#supported-modify-column-conversions}

| 変換元 | 変換先 | 注記 |
| ---- | -- | ----- |
| `VARCHAR` | `TEXT` | Schema Evolution 中によくある拡張変換です。 |
| `TINYINT` | `INT` | 整数の格納幅を拡張します。 |
| `INT` | `BIGINT` | Schema Evolution 中によくある拡張変換です。 |
| `INT` | `VARCHAR` / `TEXT` | ターゲット型が文字列表現に変換される場合に使用されます。 |

ここに記載されていない DDL 操作はパイプラインで処理されず、影響を受けるテーブルの後続の取り込みをブロックする可能性があります。また、単一の `ALTER TABLE` 文で複数の変更を組み合わせることはサポートされていません。

## DML サポートの概要 {#dml-support-summary}

| DML 操作 | ステータス |
| ------------ | -----: |
| `INSERT` | ✅ |
| `UPDATE` | ✅ |
| `DELETE` | ✅ |

ここに記載されていない DML 操作は宛先に伝播されません。

## 型マッピングリファレンス {#type-mapping-reference}

### 整数型 {#integer-types}

| TiDB 型 | TiDB Cloud Lake 型 |
| --------- | -------------------- |
| `TINYINT` | `INT8` |
| `TINYINT UNSIGNED` | `UINT8` |
| `SMALLINT` | `INT16` |
| `SMALLINT UNSIGNED` | `UINT16` |
| `MEDIUMINT` | `INT32` |
| `INT` / `INTEGER` | `INT32` |
| `MEDIUMINT UNSIGNED` / `INT UNSIGNED` / `INTEGER UNSIGNED` | `UINT32` |
| `BIGINT` | `INT64` |
| `BIGINT UNSIGNED` | `UINT64` |

### 浮動小数点型 {#floating-point-types}

| TiDB 型 | TiDB Cloud Lake 型 |
| --------- | -------------------- |
| `FLOAT` | `FLOAT32` |
| `DOUBLE` / `REAL` | `FLOAT64` |

### 固定小数点型 {#exact-numeric-types}

| TiDB 型 | TiDB Cloud Lake 型 | 注記 |
| --------- | -------------------- | ----- |
| `DECIMAL(P,S)` | `DECIMAL(P,S)` | 精度とスケールはそのまま正確に保持されます。これは `NUMERIC(P,S)` にも同様に適用されます。 |
| `DECIMAL` (精度指定なし) | `DECIMAL(76,30)` | 暗黙の切り捨てを避けるため、有効な最大精度まで自動的に拡張されます。 |
| `NUMERIC` (精度指定なし) | `DECIMAL(76,30)` | 上記と同じです。 |

### 日付と時刻の型 {#date-and-time-types}

| TiDB 型 | TiDB Cloud Lake 型 | 注記 |
| --------- | -------------------- | ----- |
| `DATE` | `DATE` |  |
| `DATETIME` / `DATETIME(n)` | `TIMESTAMP` | 秒未満の精度がサポートされます。 |
| `TIMESTAMP` / `TIMESTAMP(n)` | `TIMESTAMP` | 秒未満の精度がサポートされます。 |
| `TIME` | `VARCHAR` | TiDB Cloud Lake には独立した `TIME` 型がないため、テキストとして保存されます。 |
| `YEAR` | `INT16` | 日付/時刻型ではなく整数としてマッピングされます。 |

### 文字列型 {#string-types}

| TiDB 型 | TiDB Cloud Lake 型 | 注記 |
| --------- | -------------------- | ----- |
| `CHAR` / `VARCHAR` | `VARCHAR` | 長さは保持されません。 |
| `TINYTEXT` / `TEXT` / `MEDIUMTEXT` / `LONGTEXT` | `VARCHAR` |  |
| `ENUM` | `VARCHAR` | enum のテキストを保持するには、`content-compatible=true` の changefeed が必要です。 |
| `SET` | `VARCHAR` | 要素のテキストを保持するには、`content-compatible=true` の changefeed が必要です。 |

### バイナリ型 {#binary-types}

| TiDB 型 | TiDB Cloud Lake 型 |
| --------- | -------------------- |
| `BINARY` / `VARBINARY` | `BINARY` |
| `TINYBLOB` / `BLOB` / `MEDIUMBLOB` / `LONGBLOB` | `BINARY` |

### その他の型 {#other-types}

| TiDB 型 | TiDB Cloud Lake 型 | 注記 |
| --------- | -------------------- | ----- |
| `BOOLEAN` / `BOOL` | `BOOLEAN` |  |
| `BIT` | `UINT64` | 常に符号なしとしてマッピングされます。すべて 1 の `BIT(64)` は、符号付き `INT64` の範囲を超えます。 |
| `JSON` | `VARIANT` |  |
| 不明な型 / 記載のない型 | `VARCHAR` | フォールバックマッピングです。型としてのセマンティクスは失われます。 |
