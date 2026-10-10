---
title: 条件関数
summary: このページでは、{{{ .lake }}} の条件関数について、機能別に整理して包括的に紹介します。
---

# 条件関数

このページでは、{{{ .lake }}} の条件関数について、機能別に整理して包括的に紹介します。

## 基本的な条件関数 {#basic-conditional-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [IF](/tidb-cloud-lake/sql/if.md) / [IFF](/tidb-cloud-lake/sql/iff.md) | 条件に基づいて値を返します | `IF(1 > 0, 'yes', 'no')` → `'yes'` |
| [CASE](/tidb-cloud-lake/sql/case.md) | 条件を評価し、一致する結果を返します | `CASE WHEN 1 > 0 THEN 'yes' ELSE 'no' END` → `'yes'` |
| [DECODE](/tidb-cloud-lake/sql/decode.md) | 式を検索値と比較し、結果を返します | `DECODE(2, 1, 'one', 2, 'two', 'other')` → `'two'` |
| [COALESCE](/tidb-cloud-lake/sql/coalesce.md) | 最初の非 NULL 式を返します | `COALESCE(NULL, 'hello', 'world')` → `'hello'` |
| [NULLIF](/tidb-cloud-lake/sql/nullif.md) | 2 つの式が等しい場合は NULL を返し、それ以外の場合は最初の式を返します | `NULLIF(5, 5)` → `NULL` |
| [IFNULL](/tidb-cloud-lake/sql/ifnull.md) | 最初の式が NULL でない場合はそれを返し、そうでない場合は 2 番目の式を返します | `IFNULL(NULL, 'default')` → `'default'` |
| [NVL](/tidb-cloud-lake/sql/nvl.md) | 最初の非 NULL 式を返します | `NVL(NULL, 'default')` → `'default'` |
| [NVL2](/tidb-cloud-lake/sql/nvl2.md) | expr1 が NULL でない場合は expr2 を返し、そうでない場合は expr3 を返します | `NVL2('value', 'not null', 'is null')` → `'not null'` |

## 比較関数 {#comparison-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [GREATEST](/tidb-cloud-lake/sql/greatest.md) | リスト内の最大値を返します | `GREATEST(1, 5, 3)` → `5` |
| [LEAST](/tidb-cloud-lake/sql/least.md) | リスト内の最小値を返します | `LEAST(1, 5, 3)` → `1` |
| [GREATEST_IGNORE_NULLS](/tidb-cloud-lake/sql/greatest-ignore-nulls.md) | NULL 以外の最大値を返します | `GREATEST_IGNORE_NULLS(NULL, 5, 3)` → `5` |
| [LEAST_IGNORE_NULLS](/tidb-cloud-lake/sql/least-ignore-nulls.md) | NULL 以外の最小値を返します | `LEAST_IGNORE_NULLS(NULL, 5, 3)` → `3` |
| [BETWEEN](/tidb-cloud-lake/sql/between.md) | 値が範囲内にあるかどうかを確認します | `5 BETWEEN 1 AND 10` → `true` |
| [IN](/tidb-cloud-lake/sql/in.md) | 値がリスト内のいずれかの値に一致するかどうかを確認します | `5 IN (1, 5, 10)` → `true` |

## NULL およびエラーハンドリング関数 {#null-and-error-handling-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [IS_NULL](/tidb-cloud-lake/sql/is-null.md) | 値が NULL かどうかを確認します | `IS_NULL(NULL)` → `true` |
| [IS_NOT_NULL](/tidb-cloud-lake/sql/is-not-null.md) | 値が NULL でないかどうかを確認します | `IS_NOT_NULL('value')` → `true` |
| [IS_DISTINCT_FROM](/tidb-cloud-lake/sql/is-distinct-from.md) | 2 つの値が異なるかどうかを確認します。NULL は等しいものとして扱います | `NULL IS DISTINCT FROM 0` → `true` |
| [IS_ERROR](/tidb-cloud-lake/sql/is-error.md) | 式の評価結果がエラーになったかどうかを確認します | `IS_ERROR(1/0)` → `true` |
| [IS_NOT_ERROR](/tidb-cloud-lake/sql/is-not-error.md) | 式の評価結果がエラーにならなかったかどうかを確認します | `IS_NOT_ERROR(1/1)` → `true` |
| [ERROR_OR](/tidb-cloud-lake/sql/error-or.md) | 最初の式がエラーでない場合はそれを返し、そうでない場合は 2 番目の式を返します | `ERROR_OR(1/0, 0)` → `0` |