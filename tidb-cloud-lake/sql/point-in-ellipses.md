---
title: POINT_IN_ELLIPSES
summary: 如果该点位于所提供的任意椭圆内，则返回 1；否则返回 0。
---

# POINT_IN_ELLIPSES

如果该点位于所提供的任意椭圆内，则返回 1；否则返回 0。每个椭圆由一个中心点及其半长轴和半短轴定义。

## 语法 {#syntax}

```sql
POINT_IN_ELLIPSES(x, y, x1, y1, a1, b1 [, x2, y2, a2, b2, ...])
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `x`, `y` | 要测试的点的坐标。 |
| `x1`, `y1` | 第一个椭圆的中心。 |
| `a1`, `b1` | 第一个椭圆的半长轴和半短轴长度。 |
| `x2`, `y2`, `a2`, `b2`, ... | 可选的其他椭圆，定义方式相同。 |

## 返回类型 {#return-type}

UInt8（1 表示 true，0 表示 false）。

## 示例 {#examples}

```sql
SELECT POINT_IN_ELLIPSES(10, 10, 10, 9.1, 1, 0.9999) AS inside;

╭────────╮
│ inside │
├────────┤
│      1 │
╰────────╯
```