---
title: SYSTEM ENABLE / DISABLE EXCEPTION_BACKTRACE
summary: "{{{ .lake }}} における Rust バックトレースの生成を制御します。SYSTEM ENABLE EXCEPTION_BACKTRACE は、panic 発生時にデバッグ目的でバックトレースを有効にし、SYSTEM DISABLE EXCEPTION_BACKTRACE は、追加のオーバーヘッドや機密情報の露出を避けるためにこれを無効にします。"
---

# SYSTEM ENABLE / DISABLE EXCEPTION_BACKTRACE

{{{ .lake }}} における Rust バックトレースの生成を制御します。SYSTEM ENABLE EXCEPTION_BACKTRACE は、panic 発生時にデバッグ目的でバックトレースを有効にし、SYSTEM DISABLE EXCEPTION_BACKTRACE は、追加のオーバーヘッドや機密情報の露出を避けるためにこれを無効にします。

## 構文 {#syntax}

```sql
-- Enable Rust backtraces
SYSTEM ENABLE EXCEPTION_BACKTRACE

-- Disable Rust backtraces
SYSTEM DISABLE EXCEPTION_BACKTRACE
```