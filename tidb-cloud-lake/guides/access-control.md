---
title: 访问控制
summary: 了解 TiDB Cloud Lake 中的访问控制。它结合使用基于角色的访问控制（RBAC）和自主访问控制（DAC）来管理数据库、表、视图等数据对象的权限。
---

# 访问控制

{{{ .lake }}} 的访问控制功能同时采用了 [Role-Based Access Control (RBAC)](https://en.wikipedia.org/wiki/Role-based_access_control) 和 [Discretionary Access Control (DAC)](https://en.wikipedia.org/wiki/Discretionary_access_control) 模型。当用户访问 {{{ .lake }}} 中的数据对象时，必须被授予适当的权限或角色，或者拥有该数据对象的所有权。数据对象可以指多种元素，例如数据库、表、视图、stage 或 UDF。

![Access control](/media/tidb-cloud-lake/access-control-1.png)

| 概念   | 描述                                              |
|-----------|------------------------------------------------------------|
| 权限 | 权限在与 {{{ .lake }}} 中的数据对象交互时起着关键作用。这些权限（如读、写和执行）能够对用户操作进行精细控制，从而确保符合用户需求并维护数据安全。                                                                 |
| 角色      | 角色可简化访问控制。角色是分配给用户的预定义权限集合，可简化权限管理。管理员可以根据职责对用户进行分类，从而高效授予权限，而无需逐一进行单独配置。                                                        |
| 所有权 | 所有权是一种用于控制数据访问的特殊权限。当用户拥有某个数据对象时，他们具有最高级别的控制权，可以决定访问权限。这种直接的所有权模型使用户能够管理自己的数据，并控制在 {{{ .lake }}} 环境中谁可以访问或修改这些数据。 |

本指南介绍相关概念，并提供如何在 {{{ .lake }}} 中管理访问控制的说明：

- [权限](/tidb-cloud-lake/guides/privileges.md)
- [角色](/tidb-cloud-lake/guides/roles.md)
- [所有权](/tidb-cloud-lake/guides/ownership.md)