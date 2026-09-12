---
title: system.build_options
summary: 此系统表描述当前 {{{ .lake }}} 发布版本的构建选项。
---

# system.build_options

此系统表描述当前 {{{ .lake }}} 发布版本的构建选项。

- `cargo_features`：已启用的包特性，列在 `Cargo.toml` 的 `[features]` 部分中。
- `target_features`：为当前编译目标启用的平台特性。参考：[Conditional Compilation - `target_feature`](https://doc.rust-lang.org/reference/conditional-compilation.html#target_feature)。

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