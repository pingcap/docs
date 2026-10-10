---
title: ウィンドウ関数
summary: ウィンドウ関数は、関連する行の集合に対して計算を実行しながら、入力行ごとに 1 つの結果を返します。集約関数とは異なり、ウィンドウ関数は行を 1 つの出力にまとめません。
---

# ウィンドウ関数

## 概要 {#overview}

ウィンドウ関数は、関連する行の集合に対して計算を実行しながら、入力行ごとに 1 つの結果を返します。集約関数とは異なり、ウィンドウ関数は行を 1 つの出力にまとめません。

**主な特徴:**

- 現在の行に関連する行の「ウィンドウ」に対して動作します
- 入力行ごとに 1 つの値を返します（グループ化や集約による行の圧縮は行いません）
- ウィンドウ内の他の行の値にアクセスできます
- 柔軟な計算のためにパーティション分割と並び替えをサポートします

**Note on SQL examples in this documentation:**

- ✅ **Complete SQL statements** は {{{ .lake }}} に対して検証済みです
- ⚠️ **Syntax examples** はウィンドウフレームのパターンを示します（完全な文ではありません）
- 📋 すべての例は {{{ .lake }}} がサポートする標準 SQL 構文を使用しています
- 🔍 "Complete example" と記載された例はそのまま実行可能です

## ウィンドウ関数のカテゴリ {#window-function-categories}

{{{ .lake }}} は、ウィンドウ関数の 2 つの主要カテゴリをサポートしています。

### 1. Dedicated ウィンドウ関数 {#1-dedicated-window-functions}

これらの関数は、ウィンドウ操作向けに特別に設計されています。

**ランキング関数:**

| Function | 説明 | 同順位の扱い | 出力例 |
|----------|-------------|---------------|----------------|
| [ROW_NUMBER](/tidb-cloud-lake/sql/row-number.md) | 連番を付与 | 常に一意 | `1, 2, 3, 4, 5` |
| [RANK](/tidb-cloud-lake/sql/rank.md) | ギャップありの順位付け | 同順位は同じ順位、その後にギャップ | `1, 2, 2, 4, 5` |
| [DENSE_RANK](/tidb-cloud-lake/sql/dense-rank.md) | ギャップなしの順位付け | 同順位は同じ順位、ギャップなし | `1, 2, 2, 3, 4` |

**分布関数:**

| Function | 説明 | 範囲 | 出力例 |
|----------|-------------|-------|----------------|
| [PERCENT_RANK](/tidb-cloud-lake/sql/percent-rank.md) | パーセンテージとしての相対順位 | 0.0 から 1.0 | `0.0, 0.25, 0.5, 0.75, 1.0` |
| [CUME_DIST](/tidb-cloud-lake/sql/cume-dist.md) | 累積分布 | 0.0 から 1.0 | `0.2, 0.4, 0.6, 0.8, 1.0` |
| [NTILE](/tidb-cloud-lake/sql/ntile.md) | N 個のバケットに分割 | 1 から N | `1, 1, 2, 2, 3, 3` |

**値アクセス関数:**

| Function | 説明 | ユースケース |
|----------|-------------|----------|
| [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md) | ウィンドウ内の最初の値 | 最大値 / 最も早い値を取得 |
| [LAST_VALUE](/tidb-cloud-lake/sql/last-value.md) | ウィンドウ内の最後の値 | 最小値 / 最新の値を取得 |
| [NTH_VALUE](/tidb-cloud-lake/sql/nth-value.md) | ウィンドウ内の N 番目の値 | 特定位置の値を取得 |
| [LAG](/tidb-cloud-lake/sql/lag.md) | 前の行の値 | 前の値と比較 |
| [LEAD](/tidb-cloud-lake/sql/lead.md) | 次の行の値 | 次の値と比較 |

**エイリアス:**

| 関数 | 別名 |
|----------|----------|
| [FIRST](/tidb-cloud-lake/sql/first.md) | FIRST_VALUE |
| [LAST](/tidb-cloud-lake/sql/last.md) | LAST_VALUE |

### 2. ウィンドウ関数として使用される集約関数 {#2-aggregate-functions-used-as-window-functions}

これらは標準の集約関数で、OVER 句とともに使用することでウィンドウ操作を実行できます。

| Function | 説明 | ウィンドウフレームのサポート | 例 |
|----------|-------------|---------------------|---------|
| [SUM](/tidb-cloud-lake/sql/sum.md) | ウィンドウ全体の合計を計算 | ✓ | `SUM(sales) OVER (PARTITION BY region ORDER BY date)` |
| [AVG](/tidb-cloud-lake/sql/avg.md) | ウィンドウ全体の平均を計算 | ✓ | `AVG(score) OVER (ORDER BY id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` |
| [COUNT](/tidb-cloud-lake/sql/count.md) | ウィンドウ内の行数をカウント | ✓ | `COUNT(*) OVER (PARTITION BY department)` |
| [MIN](/tidb-cloud-lake/sql/min.md) | ウィンドウ内の最小値を返す | ✓ | `MIN(price) OVER (PARTITION BY category)` |
| [MAX](/tidb-cloud-lake/sql/max.md) | ウィンドウ内の最大値を返す | ✓ | `MAX(price) OVER (PARTITION BY category)` |
| [ARRAY_AGG](/tidb-cloud-lake/sql/array-agg.md) | 値を配列に収集 | | `ARRAY_AGG(product) OVER (PARTITION BY category)` |
| [STDDEV_POP](/tidb-cloud-lake/sql/stddev-pop.md) | 母標準偏差 | ✓ | `STDDEV_POP(value) OVER (PARTITION BY group)` |
| [STDDEV_SAMP](/tidb-cloud-lake/sql/stddev-samp.md) | 標本標準偏差 | ✓ | `STDDEV_SAMP(value) OVER (PARTITION BY group)` |
| [MEDIAN](/tidb-cloud-lake/sql/median.md) | 中央値 | ✓ | `MEDIAN(response_time) OVER (PARTITION BY server)` |

**条件付きバリアント**

| Function | 説明 | ウィンドウフレームのサポート | 例 |
|----------|-------------|---------------------|---------|
| [COUNT_IF](/tidb-cloud-lake/sql/count-if.md) | 条件付きカウント | ✓ | `COUNT_IF(status = 'complete') OVER (PARTITION BY dept)` |
| [SUM_IF](/tidb-cloud-lake/sql/sum-if.md) | 条件付き合計 | ✓ | `SUM_IF(amount, status = 'paid') OVER (PARTITION BY customer)` |
| [AVG_IF](/tidb-cloud-lake/sql/avg-if.md) | 条件付き平均 | ✓ | `AVG_IF(score, passed = true) OVER (PARTITION BY class)` |
| [MIN_IF](/tidb-cloud-lake/sql/min-if.md) | 条件付き最小値 | ✓ | `MIN_IF(temp, location = 'outside') OVER (PARTITION BY day)` |
| [MAX_IF](/tidb-cloud-lake/sql/max-if.md) | 条件付き最大値 | ✓ | `MAX_IF(speed, vehicle = 'car') OVER (PARTITION BY test)` |

## 基本構文 {#basic-syntax}

すべてのウィンドウ関数は、次のパターンに従います。

```sql
FUNCTION() OVER (
    [ PARTITION BY column ]
    [ ORDER BY column ]
    [ window_frame ]
)
```

- **PARTITION BY**: データをグループに分割します
- **ORDER BY**: 各パーティション内で行を並び替えます
- **window_frame**: 含める行を定義します（省略可能）

## ウィンドウフレームの指定 {#window-frame-specification}

ウィンドウフレームは、各行の計算に含まれる行を定義します。{{{ .lake }}} は 2 種類のウィンドウフレームをサポートしています。

### 1. ROWS BETWEEN {#1-rows-between}

物理的な行数を使用してウィンドウフレームを定義します。

**構文:**

```sql
ROWS BETWEEN frame_start AND frame_end
```

**例:**

- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - 累積合計
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` - 3 日移動平均
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` - 中心ウィンドウ

詳細な例と使用方法については、[ROWS BETWEEN](/tidb-cloud-lake/sql/rows-between.md) を参照してください。

### 2. RANGE BETWEEN {#2-range-between}

論理的な値の範囲を使用してウィンドウフレームを定義します。

**構文:**

```sql
RANGE BETWEEN frame_start AND frame_end
```

**例:**

- `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - 値に基づく累積
- `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW` - 7 日間ウィンドウ

詳細な例と使用方法については、[RANGE BETWEEN](/tidb-cloud-lake/sql/range-between.md) を参照してください。

## 一般的なユースケース {#common-use-cases}

- **ランキング**: リーダーボードや上位 N 件のリストを作成
- **分析**: 累積合計、移動平均、パーセンタイルを計算
- **比較**: 現在の値と前 / 次の値を比較
- **グループ化**: 詳細を失わずにデータをバケットに分割

詳細な構文と例については、上記の各関数のドキュメントを参照してください。