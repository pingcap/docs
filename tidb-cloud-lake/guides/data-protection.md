---
title: TiDB Cloud Lake におけるデータ保護
summary: TiDB Cloud Lake の Continuous Data Protection (CDP) は、ミス、悪意のある操作、ソフトウェアの問題からデータを安全に保つための使いやすい機能を提供します。これにより、データが意図的または偶発的に変更、消失、破損した場合でも、常にリカバリできることを保証します。
---

# TiDB Cloud Lake におけるデータ保護

{{{ .lake }}} の Continuous Data Protection (CDP) は、ミス、悪意のある操作、ソフトウェアの問題からデータを安全に保つための使いやすい機能を提供します。これにより、データが意図的または偶発的に変更、消失、破損した場合でも、常に復元できるようにします。

## {{{ .lake }}} の CDP 機能 {#cdp-features-in-lake}

- [ネットワークポリシー](/tidb-cloud-lake/guides/network-policy.md)
    - インターネットアドレスに基づいて、だれが {{{ .lake }}} にアクセスできるかを設定します。データの安全性向上に役立ちます。

- [アクセス制御](/tidb-cloud-lake/guides/access-control.md)
    - {{{ .lake }}} のさまざまな部分を、だれが閲覧または利用できるかを決定します。整理された安全な運用に役立ちます。

<!--
- [Time Travel & Fail-safe](/tidb-cloud-lake/guides/data-recovery.md)
    - Get back old or lost data.
    - Time Travel lets you look at and bring back past data.
    - Fail-safe is for big emergencies, used by {{{ .lake }}} to recover data when there's a serious problem.
-->