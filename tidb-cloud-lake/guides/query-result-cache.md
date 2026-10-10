---
title: クエリ結果キャッシュ
summary: "{{{ .lake }}} は、有効化されている場合、実行された各クエリの結果をキャッシュして永続化します。これにより、回答を得るまでの時間を大幅に短縮できます。"
---

# クエリ結果キャッシュ

{{{ .lake }}} は、有効化されている場合、実行された各クエリの結果をキャッシュして永続化します。これにより、回答を得るまでの時間を大幅に短縮できます。

## キャッシュの使用条件 {#cache-usage-conditions}

クエリ結果は、**すべて**の条件を満たした場合にのみキャッシュから再利用されます。

| 条件 | 要件 |
|-----------|-------------|
| **キャッシュ有効** | 現在のセッションで `enable_query_result_cache = 1` |
| **同一クエリ** | クエリテキストが完全に一致している必要があります（大文字と小文字を区別） |
| **実行時間** | 元のクエリ実行時間 ≥ `query_result_cache_min_execute_secs` |
| **結果サイズ** | キャッシュされる結果 ≤ `query_result_cache_max_bytes` |
| **TTL 有効** | キャッシュの経過時間 < `query_result_cache_ttl_secs` |
| **データ整合性** | キャッシュ作成以降にテーブルデータが変更されていないこと（`query_result_cache_allow_inconsistent = 1` の場合を除く） |
| **セッションスコープ** | キャッシュはセッション固有です |

> **Note:**
>
> デフォルトでは（`query_result_cache_allow_inconsistent = 0`）、基になるテーブルデータが変更されると、キャッシュされた結果は自動的に無効化されます。これによりデータ整合性は確保されますが、頻繁に更新されるテーブルではキャッシュの効果が低下する可能性があります。

## クイックスタート {#quick-start}

セッションでクエリ結果キャッシュを有効にします。

```sql
-- Enable query result cache
SET enable_query_result_cache = 1;

-- Optional: Cache all queries (including fast ones)
SET query_result_cache_min_execute_secs = 0;
```

## 設定 {#configuration-settings}

| 設定 | デフォルト | 説明 |
|---------|---------|-------------|
| `enable_query_result_cache` | 0 | クエリ結果キャッシュを有効化/無効化します |
| `query_result_cache_allow_inconsistent` | 0 | 基になるデータが変更されていてもキャッシュ結果を許可します |
| `query_result_cache_max_bytes` | 1048576 | 単一のキャッシュ結果に対する最大サイズ（バイト） |
| `query_result_cache_min_execute_secs` | 1 | キャッシュ対象となるまでの最小実行時間 |
| `query_result_cache_ttl_secs` | 300 | キャッシュの有効期限（5 分） |

## パフォーマンス例 {#performance-example}

この例では、TPC-H Q1 クエリをキャッシュする方法を示します。

### 1. キャッシュを有効化する {#1-enable-caching}

```sql
SET enable_query_result_cache = 1;
SET query_result_cache_min_execute_secs = 0;
```

### 2. 1 回目の実行（キャッシュなし） {#2-first-execution-no-cache}

```sql
SELECT
    l_returnflag,
    l_linestatus,
    sum(l_quantity) as sum_qty,
    sum(l_extendedprice) as sum_base_price,
    sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
    sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
    avg(l_quantity) as avg_qty,
    avg(l_extendedprice) as avg_price,
    avg(l_discount) as avg_disc,
    count(*) as count_order
FROM lineitem
WHERE l_shipdate <= add_days(to_date('1998-12-01'), -90)
GROUP BY l_returnflag, l_linestatus
ORDER BY l_returnflag, l_linestatus;
```

**結果**: 4 行、**21.492 秒**（6 億行を処理）

### 3. キャッシュエントリを確認する {#3-verify-cache-entry}

```sql
SELECT sql, query_id, result_size, num_rows FROM system.query_cache;
```

### 4. 2 回目の実行（キャッシュから） {#4-second-execution-from-cache}

同じクエリを再度実行します。

**結果**: 4 行、**0.164 秒**（処理行数 0）

## キャッシュ管理 {#cache-management}

### キャッシュ使用状況を監視する {#monitor-cache-usage}

```sql
SELECT * FROM system.query_cache;
```

### キャッシュされた結果にアクセスする {#access-cached-results}

```sql
SELECT * FROM RESULT_SCAN(LAST_QUERY_ID());
```

### キャッシュのライフサイクル {#cache-lifecycle}

キャッシュされた結果は、次の場合に自動的に削除されます。

- **TTL の期限切れ**（デフォルト: 5 分）
- **結果サイズが上限を超過**（デフォルト: 1MB）
- **セッション終了**（キャッシュはセッションスコープ）
- **基になるデータの変更**（整合性のため自動的に無効化）
- **テーブル構造の変更**（スキーマ変更によりキャッシュが無効化）

> **Note:**
>
> クエリ結果キャッシュはセッションスコープです。各セッションは独自のキャッシュを管理し、セッション終了時に自動的にクリーンアップされます。