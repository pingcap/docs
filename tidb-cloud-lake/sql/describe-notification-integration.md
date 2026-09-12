---
title: DESCRIBE NOTIFICATION INTEGRATION
summary: 显示通知集成的属性。
---

# DESCRIBE NOTIFICATION INTEGRATION

显示通知集成的属性。

> **Note:**
>
> 此命令要求启用 cloud control。

## 语法 {#syntax}

```sql
DESCRIBE NOTIFICATION INTEGRATION <name>
```

`DESC NOTIFICATION INTEGRATION <name>` 也可作为同义语法使用。

## 输出 {#output}

结果包括通知的创建时间、名称、标识符、类型、启用状态、webhook 选项和注释。

## 示例 {#example}

```sql
DESCRIBE NOTIFICATION INTEGRATION SampleNotification;
```