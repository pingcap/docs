---
title: 平台与 Region
summary: 了解 TiDB Cloud Lake 支持的云平台和 Region。
---

# 平台与 Region

{{{ .lake }}} 是一种云原生解决方案，目前支持以下云服务提供商和 Region：

| Cloud Provider | Region Name              | Region ID      |
|----------------|--------------------------|----------------|
| AWS            | US West (Oregon)         | us-west-2      |
| AWS            | Asia Pacific (Tokyo)     | ap-northeast-1 |
| AWS            | US East (N. Virginia)    | us-east-1      |
| AWS            | Asia Pacific (Singapore) | ap-southeast-1 |
| AWS            | Asia Pacific (Mumbai)    | ap-south-1     |
| Alibaba Cloud  | Japan (Tokyo)            | ap-northeast-1 |

> **注意：**
>
> 为确保高效且稳定的数据同步与导入，我们强烈建议你选择与当前正在使用的云服务提供商和 Region 相匹配的云服务。这样可以有效避免跨网络数据传输可能带来的网络延迟和数据丢失风险，保障数据传输过程的安全与顺畅，同时显著提升数据同步与导入的效率和稳定性。
> {{{ .lake }}} 计划扩展对更多云服务提供商和 Region 的支持。如果你当前使用的云服务提供商或 Region 尚未受支持，请点击 [Contact Sales](https://www.pingcap.com/contact-us/) 与 {{{ .lake }}} 团队联系。

当你注册 {{{ .lake }}} 账户时，需要选择一个云平台和 Region。账户创建成功后，所选的云平台和 Region 将无法更改。