---
title: SYSTEM ENABLE / DISABLE EXCEPTION_BACKTRACE
summary: 控制 {{{ .lake }}} 中 Rust backtrace 的生成。SYSTEM ENABLE EXCEPTION_BACKTRACE 会在发生 panic 时启用 backtrace 以便调试，而 SYSTEM DISABLE EXCEPTION_BACKTRACE 会禁用 backtrace，以避免额外开销或敏感信息暴露。
---

# SYSTEM ENABLE / DISABLE EXCEPTION_BACKTRACE

控制 {{{ .lake }}} 中 Rust backtrace 的生成。SYSTEM ENABLE EXCEPTION_BACKTRACE 会在发生 panic 时启用 backtrace 以便调试，而 SYSTEM DISABLE EXCEPTION_BACKTRACE 会禁用 backtrace，以避免额外开销或敏感信息暴露。

## 语法 {#syntax}

```sql
-- Enable Rust backtraces
SYSTEM ENABLE EXCEPTION_BACKTRACE

-- Disable Rust backtraces
SYSTEM DISABLE EXCEPTION_BACKTRACE
```