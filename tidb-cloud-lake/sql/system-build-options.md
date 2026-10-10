---
title: system.build_options
summary: このシステムテーブルは、現在の {{{ .lake }}} リリースのビルドオプションを説明します。
---

# system.build_options

このシステムテーブルは、現在の {{{ .lake }}} リリースのビルドオプションを説明します。

- `cargo_features`: `Cargo.toml` の `[features]` セクションに記載されている、有効化されたパッケージ機能です。
- `target_features`: 現在のコンパイルターゲットに対して有効化されているプラットフォーム機能です。参考: [Conditional Compilation - `target_feature`](https://doc.rust-lang.org/reference/conditional-compilation.html#target_feature) 。

```sql
SELECT * FROM system.build_options;
+----------------+---------------------+
| cargo_features | target_features     |
+----------------+---------------------+
| default        | fxsr                |
|                | llvm14-builtins-abi |
|                | sse                 |
|                | sse2                |
+----------------+---------------------+
4 rows in set (0.031 sec)
```