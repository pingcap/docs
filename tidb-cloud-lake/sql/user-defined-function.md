---
title: ユーザー定義関数
summary: {{{ .lake }}} の User-Defined Functions (UDFs) を使用すると、特定のデータ処理ニーズに合わせたカスタム操作を作成できます。このページでは、最もよく使用するコマンドを紹介し、ユースケースに適した関数タイプを選ぶのに役立ちます。
---

# ユーザー定義関数

{{{ .lake }}} の User-Defined Functions (UDFs) を使用すると、特定のデータ処理ニーズに合わせたカスタム操作を作成できます。このページでは、最もよく使用するコマンドを紹介し、ユースケースに適した関数タイプを選ぶのに役立ちます。

> **Tip:**
>
> **まず組み込み関数を確認してください。** {{{ .lake }}} には、数学、文字列、日付、JSON、集計 などをカバーする数百の組み込み関数が用意されています。UDF を作成する前に、[SQL 関数リファレンス](/tidb-cloud-lake/sql/sql-function-reference.md) を参照して、必要な処理をすでに実現できる関数がないか確認してください。組み込み関数ではロジックを表現できない場合に、UDF の使用を検討してください。

## 関数管理コマンド {#function-management-commands}

| コマンド | 説明 |
|---------|-------------|
| [CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md) | スクリプト UDAF（JavaScript/Python ランタイム） |
| [CREATE TABLE FUNCTION](/tidb-cloud-lake/sql/create-table-function.md) | 結果セットを返す SQL 専用のテーブル関数 |
| [SHOW USER FUNCTIONS](/tidb-cloud-lake/sql/show-user-functions.md) | すべてのユーザー定義関数を一覧表示します |
| [ALTER FUNCTION](/tidb-cloud-lake/sql/alter-function.md) | 既存の関数を変更します |
| [DROP FUNCTION](/tidb-cloud-lake/sql/drop-function.md) | 関数を削除します |

## 関数タイプの比較 {#function-type-comparison}

| 機能 | Scalar (SQL) | Scalar (Python/JavaScript) | Aggregate (Script) | Tabular SQL |
|---------|-------------|----------------------------|--------------------|------------|
| **戻り値の型** | 単一値 | 単一値 | 単一値 | テーブル/ResultSet |
| **言語** | SQL 式 | Python/JavaScript | JavaScript/Python ランタイム | SQL クエリ |
| **パフォーマンス** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Enterprise 必須** | いいえ | Python ランタイムのみ | Python ランタイムのみ | いいえ |
| **パッケージサポート** | いいえ | Python: はい (PACKAGES) | Python: はい (PACKAGES) | いいえ |
| **最適な用途** | 数学計算<br/>文字列操作<br/>データ整形 | 高度なアルゴリズム<br/>外部ライブラリ<br/>制御フローロジック | スクリプトロジックを必要とするカスタム集計 | 複雑なクエリ<br/>複数行の結果<br/>データ変換 |

## 統一構文 {#unified-syntax}

すべてのローカル UDF タイプでは、一貫して `$$` 構文を使用します。

```sql
-- Scalar Function
CREATE FUNCTION func_name(param TYPE) RETURNS TYPE AS $$ expression $$;

-- Tabular Function
CREATE FUNCTION func_name(param TYPE) RETURNS TABLE(...) AS $$ query $$;

-- Scalar Function (Python/JavaScript)
CREATE FUNCTION func_name(param TYPE) RETURNS TYPE
LANGUAGE python
HANDLER = 'handler' AS $$ code $$;
```