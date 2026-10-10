---
title: USE WAREHOUSE
summary: 現在のセッションを特定の Warehouse にバインドします。以降、このセッション内のクエリは実行時にこの Warehouse を使用します。
---

# USE WAREHOUSE

現在のセッションを特定の Warehouse にバインドします。以降、このセッション内のクエリは実行時にこの Warehouse を使用します。

## 構文 {#syntax}

```sql
USE WAREHOUSE <warehouse_name>
```

| パラメータ | 説明 |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| warehouse_name | 使用する Warehouse の名前です。このコマンドは、その Warehouse が存在し、アクセス可能であることを検証します。 |

## 例 {#examples}

現在のセッションで Warehouse をアクティブに設定します。

```sql
USE WAREHOUSE 'my-warehouse';
```