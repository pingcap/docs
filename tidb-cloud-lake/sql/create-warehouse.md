---
title: CREATE WAREHOUSE
summary: コンピュートリソース用の新しい Warehouse を作成します。
---

# CREATE WAREHOUSE

コンピュートリソース用の新しい Warehouse を作成します。

## 構文 {#syntax}

```sql
CREATE WAREHOUSE [ IF NOT EXISTS ] <warehouse_name>
    [ WITH ] warehouse_size = <size>
    [ WITH ] auto_suspend = <nullable_unsigned_number>
    [ WITH ] initially_suspended = <bool>
    [ WITH ] auto_resume = <bool>
    [ WITH ] max_cluster_count = <nullable_unsigned_number>
    [ WITH ] min_cluster_count = <nullable_unsigned_number>
    [ WITH ] comment = '<string_literal>'
    [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] )
```

| パラメーター | 説明 |
| --------------- | --------------------------------------------------------------------------------------------- |
| `IF NOT EXISTS` | 任意。指定した場合、Warehouse がすでに存在していても変更を加えずにコマンドは成功します。 |
| warehouse_name  | 3～63 文字で、使用できる文字は `A-Z`、`a-z`、`0-9`、`-` のみです。 |

## オプション {#options}

| オプション | 型 / 値 | デフォルト | 説明 |
| --------------------- | -------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `WAREHOUSE_SIZE`      | `XSmall`, `Small`, `Medium`, `Large`, `XLarge`, `2XLarge`–`6XLarge`（大文字小文字を区別しない） | `Small`       | コンピュートサイズを制御します。 |
| `AUTO_SUSPEND`        | `NULL`、`0`、または 300 秒以上                                                           | `600` seconds | 自動サスペンドまでのアイドルタイムアウトです。`0`/`NULL` はサスペンドしないことを意味し、300 未満の値は拒否されます。 |
| `INITIALLY_SUSPENDED` | Boolean                                                                                | `FALSE`       | `TRUE` の場合、Warehouse は作成後に明示的に再開されるまでサスペンド状態のままになります。 |
| `AUTO_RESUME`         | Boolean                                                                                | `TRUE`        | 受信したクエリによって Warehouse を自動的に起動するかどうかを制御します。 |
| `MAX_CLUSTER_COUNT`   | `NULL` または 0 以上の整数                                                         | `0`           | オートスケーリングするクラスター数の上限です。`0` はオートスケールを無効にします。 |
| `MIN_CLUSTER_COUNT`   | `NULL` または 0 以上の整数                                                         | `0`           | オートスケーリングするクラスター数の下限です。`MAX_CLUSTER_COUNT` 以下である必要があります。 |
| `COMMENT`             | String                                                                                 | Empty         | `SHOW WAREHOUSES` で表示される自由形式のテキストです。 |
| `TAG`                 | キーと値のペア: `TAG ( key1 = 'value1', key2 = 'value2' )`                            | None          | 分類および整理のためのリソースタグです（AWS tags に類似）。コスト配分、環境の識別、またはチーム所有者の管理に使用されます。 |

- オプションは任意の順序で指定でき、重複して指定することもできます（後に指定した値が優先されます）。
- `AUTO_SUSPEND`、`MAX_CLUSTER_COUNT`、`MIN_CLUSTER_COUNT` は `= NULL` を受け付け、`0` にリセットします。

## 例 {#examples}

次の例では、オートスケーリングとカスタム設定を備えた XLarge Warehouse を作成します。

```sql
CREATE WAREHOUSE IF NOT EXISTS 'etl-wh'
    WITH warehouse_size = XLarge
    auto_suspend = 600
    initially_suspended = TRUE
    auto_resume = FALSE
    max_cluster_count = 4
    min_cluster_count = 2
    comment = 'Nightly ETL warehouse'
    TAG (environment = 'production', team = 'data-engineering', cost_center = 'analytics');
```

次の例では、基本的な Small Warehouse を作成します。

```sql
CREATE WAREHOUSE 'my-warehouse'
    WITH warehouse_size = Small;
```