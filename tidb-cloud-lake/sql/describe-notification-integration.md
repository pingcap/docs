---
title: DESCRIBE NOTIFICATION INTEGRATION
summary: 通知インテグレーションのプロパティを表示します。
---

# DESCRIBE NOTIFICATION INTEGRATION

通知インテグレーションのプロパティを表示します。

> **Note:**
>
> このコマンドを使用するには、cloud control が有効になっている必要があります。

## 構文 {#syntax}

```sql
DESCRIBE NOTIFICATION INTEGRATION <name>
```

`DESC NOTIFICATION INTEGRATION <name>` も同義語として使用できます。

## 出力 {#output}

結果には、通知の作成時刻、名前、識別子、タイプ、有効状態、webhook オプション、およびコメントが含まれます。

## 例 {#example}

```sql
DESCRIBE NOTIFICATION INTEGRATION SampleNotification;
```