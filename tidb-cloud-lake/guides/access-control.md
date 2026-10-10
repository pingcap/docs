---
title: アクセス制御
summary: データベース、テーブル、ビューなどのデータオブジェクトに対する権限を管理するために、Role-Based Access Control (RBAC) と Discretionary Access Control (DAC) の両方を使用する TiDB Cloud Lake のアクセス制御について説明します。
---

# アクセス制御

{{{ .lake }}} は、アクセス制御機能として [Role-Based Access Control (RBAC)](https://en.wikipedia.org/wiki/Role-based_access_control) と [Discretionary Access Control (DAC)](https://en.wikipedia.org/wiki/Discretionary_access_control) の両方のモデルを採用しています。ユーザーが {{{ .lake }}} 内のデータオブジェクトにアクセスするには、適切な権限またはロールが付与されている必要があるか、そのデータオブジェクトの所有者である必要があります。データオブジェクトには、データベース、テーブル、ビュー、stage、または UDF などのさまざまな要素が含まれます。

![Access control](/media/tidb-cloud-lake/access-control-1.png)

| 概念   | 説明                                              |
|-----------|------------------------------------------------------------|
| 権限 | 権限は、{{{ .lake }}} でデータオブジェクトを操作する際に重要な役割を果たします。読み取り、書き込み、実行などのこれらの許可により、ユーザーの操作をきめ細かく制御でき、ユーザー要件との整合性を確保しながらデータセキュリティを維持できます。                                                                 |
| ロール      | ロールはアクセス制御を簡素化します。ロールはユーザーに割り当てられる、あらかじめ定義された権限のセットであり、権限管理を効率化します。管理者は責任に基づいてユーザーを分類し、個別に設定することなく効率的に権限を付与できます。                                                        |
| 所有権 | 所有権は、データアクセスを制御するための特別な権限です。ユーザーがデータオブジェクトを所有している場合、そのユーザーは最高レベルの制御権を持ち、アクセス権限を決定できます。このシンプルな所有権モデルにより、ユーザーは {{{ .lake }}} 環境内で自分のデータを管理し、誰がアクセスまたは変更できるかを制御できます。 |

このガイドでは、関連する概念を説明し、{{{ .lake }}} でアクセス制御を管理する方法を案内します。

- [権限](/tidb-cloud-lake/guides/privileges.md)
- [ロール](/tidb-cloud-lake/guides/roles.md)
- [Ownership](/tidb-cloud-lake/guides/ownership.md)