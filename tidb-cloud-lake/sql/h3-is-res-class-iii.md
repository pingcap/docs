---
title: H3_IS_RES_CLASS_III
summary: 指定された H3 インデックスの解像度が Class III の向きかどうかを確認します。
---

# H3_IS_RES_CLASS_III

指定された [H3](https://eng.uber.com/h3/) インデックスの解像度が Class III の向きかどうかを確認します。

## 構文 {#syntax}

```sql
H3_IS_RES_CLASS_III(h3)
```

## 例 {#examples}

```sql
SELECT H3_IS_RES_CLASS_III(635318325446452991);

┌─────────────────────────────────────────┐
│ h3_is_res_class_iii(635318325446452991) │
├─────────────────────────────────────────┤
│ true                                    │
└─────────────────────────────────────────┘
```