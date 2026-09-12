---
title: TiDB Cloud Lake 中的数据保护
summary: TiDB Cloud Lake 的 Continuous Data Protection (CDP) 提供易于使用的功能，帮助你的数据免受误操作、恶意行为和软件问题的影响。即使数据因意外或人为原因被更改、丢失或损坏，也能确保始终可以恢复。
---

# TiDB Cloud Lake 中的数据保护

{{{ .lake }}} 的 Continuous Data Protection (CDP) 提供易于使用的功能，帮助你的数据免受误操作、恶意行为和软件问题的影响。即使数据因意外或人为原因被更改、丢失或损坏，也能确保始终可以恢复。

## {{{ .lake }}} 中的 CDP 功能 {#cdp-features-in-lake}

- [网络策略](/tidb-cloud-lake/guides/network-policy.md)
    - 根据互联网地址设置谁可以访问 {{{ .lake }}}。这有助于保护你的数据安全。

- [访问控制](/tidb-cloud-lake/guides/access-control.md)
    - 决定谁可以查看或使用 {{{ .lake }}} 的不同部分。帮助保持有序并确保安全。

<!--
- [Time Travel & Fail-safe](/tidb-cloud-lake/guides/data-recovery.md)
    - 恢复旧数据或丢失的数据。
    - Time Travel 可让你查看并恢复过去的数据。
    - Fail-safe 用于重大紧急情况，由 {{{ .lake }}} 在发生严重问题时用于恢复数据。
-->