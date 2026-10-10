---
title: SET
summary: 現在のセッションのシステム設定の値を変更します。現在のすべての設定を表示するには、SHOW SETTINGS を使用します。
---

# SET

現在のセッションのシステム設定の値を変更します。現在のすべての設定を表示するには、[SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md) を使用します。

関連情報:

- [SETTINGS 句](/tidb-cloud-lake/sql/settings-clause.md)
- [SET_VAR](/tidb-cloud-lake/sql/set-var.md)
- [UNSET](/tidb-cloud-lake/sql/unset.md)

## 構文 {#syntax}

```sql
SET [ SESSION | GLOBAL ] <setting_name> = <new_value>
```

| Parameter | 説明 |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SESSION   | セッションレベルで設定変更を適用します。省略した場合、デフォルトでセッションレベルに適用されます。                                                                                        |
| GLOBAL    | 現在のセッションだけでなく、グローバルレベルで設定変更を適用します。設定レベルの詳細については、[Setting Levels](/tidb-cloud-lake/sql/show-settings.md#setting-levels) を参照してください。 |

## 例 {#examples}

次の例では、`max_memory_usage` 設定を `4 GB` に設定します。

```sql
SET max_memory_usage = 1024*1024*1024*4;
```

次の例では、`max_threads` 設定を `4` に設定します。

```sql
SET max_threads = 4;
```

次の例では、`max_threads` 設定を `4` に設定し、それをグローバルレベルの設定に変更します。

```sql
SET GLOBAL max_threads = 4;
```