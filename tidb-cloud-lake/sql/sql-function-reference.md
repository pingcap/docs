---
title: SQL 関数リファレンス
summary: "{{{ .lake }}} は、あらゆる種類のデータ処理に対応する包括的な SQL 関数を提供します。関数は重要度と使用頻度ごとに整理されています。"
---

# SQL 関数リファレンス

{{{ .lake }}} は、あらゆる種類のデータ処理に対応する包括的な SQL 関数を提供します。関数は重要度と使用頻度ごとに整理されています。

> **Tip:**
>
> **必要な関数が見つかりませんか？** 以下の組み込み関数で目的のロジックを実現できない場合は、[User-Defined Functions (UDFs)](/tidb-cloud-lake/sql/user-defined-function.md) を使用して独自の関数を定義できます。UDF を使うと、SQL 式、Python、または JavaScript を使用して、カスタムのスカラー関数、集計関数、テーブル関数を実装し、他の組み込み関数と同じように呼び出せます。詳細は、以下の[User-Defined Functions による拡張](#extending-with-user-defined-functions)を参照してください。

## コアデータ関数 {#core-data-functions}

| カテゴリ | 説明 |
|----------|-------------|
| [数値関数](/tidb-cloud-lake/sql/numeric-functions.md) | 数学演算と計算 |
| [文字列関数](/tidb-cloud-lake/sql/string-functions-overview.md) | テキスト操作と文字列処理 |
| [日付・時刻関数](/tidb-cloud-lake/sql/date-time-functions.md) | 日付、時刻、および時間関連の操作 |
| [変換関数](/tidb-cloud-lake/sql/conversion-functions.md) | 型キャストとデータ形式の変換 |
| [条件関数](/tidb-cloud-lake/sql/conditional-functions.md) | ロジックおよび制御フローの操作 |

## 分析関数 {#analytics-functions}

| カテゴリ | 説明 |
|----------|-------------|
| [集計関数](/tidb-cloud-lake/sql/aggregate-functions.md) | 複数行にまたがる統計計算 |
| [ウィンドウ関数](/tidb-cloud-lake/sql/window-functions-overview.md) | ウィンドウ操作による高度な分析 |

## 構造化データと半構造化データ {#structured-semi-structured-data}

| カテゴリ | 説明 |
|----------|-------------|
| [Structured & Semi-Structured Functions](/tidb-cloud-lake/sql/structured-semi-structured-functions.md) | JSON、配列、オブジェクト、およびネストされたデータの処理 |

## 検索関数 {#search-functions}

| カテゴリ | 説明 |
|----------|-------------|
| [全文検索関数](/tidb-cloud-lake/sql/full-text-search-functions.md) | 全文検索と関連度スコアリング |

## ベクトル関数 {#vector-functions}

| カテゴリ | 説明 |
|----------|-------------|
| [ベクトル関数](/tidb-cloud-lake/sql/vector-functions.md) | ベクトル類似度と距離の計算 |

## 地理空間関数 {#geospatial-functions}

| カテゴリ | 説明 |
|----------|-------------|
| [Geospatial Functions](/tidb-cloud-lake/sql/geospatial-functions.md) | Geometry、GeoHash、および H3 の空間操作 |

## データ管理 {#data-management}

| カテゴリ | 説明 |
|----------|-------------|
| [Table Functions](/tidb-cloud-lake/sql/table-functions.md) | ファイル検査、データ生成、およびシステム情報 |
| [システム関数](/tidb-cloud-lake/sql/system-functions.md) | システム情報および管理操作 |
| [コンテキスト関数](/tidb-cloud-lake/sql/context-functions.md) | 現在のセッション、ユーザー、およびデータベース情報 |

## セキュリティと整合性 {#security-integrity}

| カテゴリ | 説明 |
|----------|-------------|
| [Hash Functions](/tidb-cloud-lake/sql/hash-functions.md) | データのハッシュ化と整合性検証 |
| [Bitmap Functions](/tidb-cloud-lake/sql/bitmap-functions.md) | 高性能なビットマップ操作と分析 |
| [UUID 関数](/tidb-cloud-lake/sql/uuid-functions.md) | Universally unique identifier の生成 |
| [IP Address Functions](/tidb-cloud-lake/sql/ip-address-functions.md) | ネットワークアドレスの操作と検証 |

## ユーティリティ関数 {#utility-functions}

| カテゴリ | 説明 |
|----------|-------------|
| [Interval Functions](/tidb-cloud-lake/sql/interval-functions.md) | 時間単位の変換と interval の作成 |
| [シーケンス関数](/tidb-cloud-lake/sql/sequence-functions-overview.md) | 自動増分シーケンス値の生成 |
| [データ匿名化関数](/tidb-cloud-lake/sql/data-anonymization-functions.md) | データマスキングと匿名化のユーティリティ |
| [テスト関数](/tidb-cloud-lake/sql/test-functions.md) | テストおよびデバッグ用ユーティリティ |
| [その他の関数](/tidb-cloud-lake/sql/other-functions.md) | 各種ヘルパーおよびユーティリティ |

## User-Defined Functions による拡張 {#extending-with-user-defined-functions}

上記の組み込み関数で特定のロジックを実現できない場合は、[User-Defined Functions (UDFs)](/tidb-cloud-lake/sql/user-defined-function.md) を使用して独自の関数を定義できます。作成後、UDF はクエリ内で組み込み関数とまったく同じように呼び出せます。

| 関数タイプ                                                                                 | 使用する場面                                                                  |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [Scalar Function (SQL)](/tidb-cloud-lake/sql/create-scalar-function.md)              | SQL 式をクエリ間で再利用したい場合（数式、文字列フォーマットなど）。 |
| [Scalar Function (Python/JavaScript)](/tidb-cloud-lake/sql/create-scalar-function.md) | 制御フロー、外部ライブラリ、または高度なアルゴリズムがロジックに必要な場合。   |
| [Aggregate Function](/tidb-cloud-lake/sql/create-aggregate-function.md)       | 組み込みの集計では表現できないカスタム集計が必要な場合。        |
| [Table Function](/tidb-cloud-lake/sql/create-table-function.md)               | 結果セットを返す、再利用可能でパラメータ化されたクエリが必要な場合。          |

UDF の種類と構文の完全な比較については、[User-Defined Function](/tidb-cloud-lake/sql/user-defined-function.md) を参照してください。