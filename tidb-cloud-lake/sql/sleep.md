---
title: SLEEP
summary: 在每个数据块上休眠 `seconds` 秒。
---

# SLEEP

在每个数据块上休眠 `seconds` 秒。

> **注意：**
>
> 仅用于需要 sleep 的测试场景。

## 语法 {#syntax}

```sql
SLEEP(seconds)
```

## 参数 {#arguments}

| 参数 | 描述 |
| ----------- | ----------- |
| seconds  | 必须是任意非负数或 float 的常数列。｜

## 返回类型 {#return-type}

UInt8

## 示例 {#examples}

```sql
SELECT sleep(2);
+----------+
| sleep(2) |
+----------+
|        0 |
+----------+
```