---
title: DROP WAREHOUSE
summary: Warehouse を削除し、それに関連付けられたリソースを解放します。
---

# DROP WAREHOUSE

Warehouse を削除し、それに関連付けられたリソースを解放します。

## 構文 {#syntax}

```sql
DROP WAREHOUSE [ IF EXISTS ] <warehouse_name>
```

| パラメータ      | 説明                                                                                                                                                 |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IF EXISTS`    | 任意。指定した場合、Warehouse が存在しなくてもコマンドはエラーにならず正常に完了します。これを指定しない場合、Warehouse が存在しないとコマンドは失敗します。 |
| warehouse_name | 削除する Warehouse の名前です。                                                                                                                     |

## 例 {#examples}

Warehouse を削除します。

```sql
DROP WAREHOUSE my_warehouse;
```

Warehouse が存在する場合にのみ削除します。

```sql
DROP WAREHOUSE IF EXISTS my_warehouse;
```