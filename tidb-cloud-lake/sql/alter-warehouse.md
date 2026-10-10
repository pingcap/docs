---
title: ALTER WAREHOUSE
summary: 既存のWarehouseを一時停止、再開、または設定変更します。
---

# ALTER WAREHOUSE

既存のWarehouseを一時停止、再開、または設定変更します。

## 構文 {#syntax}

```sql
-- Suspend or resume a warehouse
ALTER WAREHOUSE <warehouse_name> { SUSPEND | RESUME }

-- Modify warehouse settings
ALTER WAREHOUSE <warehouse_name>
    SET [ warehouse_size = <size> ]
    [ auto_suspend = <nullable_unsigned_number> ]
    [ auto_resume = <bool> ]
    [ max_cluster_count = <nullable_unsigned_number> ]
    [ min_cluster_count = <nullable_unsigned_number> ]
    [ comment = '<string_literal>' ]

ALTER WAREHOUSE <warehouse_name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER WAREHOUSE <warehouse_name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER WAREHOUSE <warehouse_name> RENAME TO <new_name>
```

| パラメーター | 説明                                                                       |
| --------- | ------------------------------------------------------------------------ |
| `SUSPEND` | Warehouseを即座に一時停止します。                                                |
| `RESUME`  | Warehouseを即座に再開します。                                                    |
| `SET`     | 1つ以上のWarehouseオプションを変更します。指定されていないフィールドは変更されません。 |

## オプション {#options}

`SET` 句では、[CREATE WAREHOUSE](/tidb-cloud-lake/sql/create-warehouse.md) と同じオプションを使用できます。

| オプション              | 型 / 値                                                              | 説明                                                                   |
| ------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `WAREHOUSE_SIZE`    | `XSmall`, `Small`, `Medium`, `Large`, `XLarge`, `2XLarge`–`6XLarge` | コンピュートサイズを変更します。                                                     |
| `AUTO_SUSPEND`      | `NULL`, `0`, または 300 秒以上                                            | 自動一時停止までのアイドルタイムアウトです。`NULL` は auto-suspend を無効にします。                 |
| `AUTO_RESUME`       | Boolean                                                             | 受信したクエリによってWarehouseを自動的に起動するかどうかを制御します。                              |
| `MAX_CLUSTER_COUNT` | `NULL` または 0 以上の整数                                                  | オートスケーリングされるクラスター数の上限です。                                             |
| `MIN_CLUSTER_COUNT` | `NULL` または 0 以上の整数                                                  | オートスケーリングされるクラスター数の下限です。                                             |
| `COMMENT`           | String                                                              | 自由形式のテキスト説明です。                                                       |

- 数値オプションでは、`NULL` を指定して値を `0` にリセットできます。
- オプションを指定せずに `SET` を指定すると、エラーになります。
- `SET TAG` は、1つ以上のタグを追加または更新します。複数のタグは、カンマ区切りで1つのステートメント内に設定できます。
- `UNSET TAG` は、キーを指定して1つ以上のタグを削除します。存在しないタグキーは無視されます。
- `RENAME TO` を使用するには、Warehouseが一時停止状態である必要があり、名前付けルールは `CREATE` と同じです。

## 例 {#examples}

Warehouseを一時停止します。

```sql
ALTER WAREHOUSE 'my-wh' SUSPEND;
```

Warehouseを再開します。

```sql
ALTER WAREHOUSE 'my-wh' RESUME;
```

Warehouseの設定を変更します。

```sql
ALTER WAREHOUSE 'my-wh'
    SET warehouse_size = Large
    auto_resume = TRUE
    comment = 'Serving tier';
```

auto-suspend を無効にします。

```sql
ALTER WAREHOUSE 'my-wh' SET auto_suspend = NULL;
```

タグを管理します。

```sql
ALTER WAREHOUSE 'wh-hot' SET TAG environment = 'production';
ALTER WAREHOUSE 'wh-hot' SET TAG environment = 'staging', owner = 'john', cost_center = 'eng';
ALTER WAREHOUSE 'wh-hot' UNSET TAG environment;
ALTER WAREHOUSE 'wh-hot' UNSET TAG environment, owner, cost_center;
```