---
title: TiDB Cloud Premium 的内核版本管理
summary: 了解 TiDB Cloud Premium 的数据库内核版本规则和格式。
---

# TiDB Cloud Premium 的内核版本管理

本文介绍 TiDB Cloud Premium 所使用的底层数据库内核的版本管理规则。

> **Note:**
>
> 本文档中介绍的内核版本管理规则仅适用于 TiDB Cloud Premium。其他 TiDB Cloud 方案使用不同的内核版本模型：
>
> - TiDB Cloud Starter 实例运行在基于经典 TiDB v8.5.3 内核定制的 TiDB X engine 上。该内核与 TiDB Cloud Premium 的内核略有不同。
> - TiDB Cloud Essential 实例默认运行在基于经典 TiDB v8.5.3 内核定制的 TiDB X engine 上。如果你希望 TiDB Cloud Essential 实例运行与 TiDB Cloud Premium 相同的内核，请联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。
> - TiDB Cloud Dedicated 集群运行在经典 TiDB 内核上，其内核版本与 TiDB Self-Managed 版本直接对应。

## 内核版本管理 {#kernel-versioning}

TiDB Cloud Premium 的内核版本采用以下基于时间的格式：

```text
TiDB-X-CLOUD.YYYYMM.x
```

例如：

```text
TiDB-X-CLOUD.202510.1
```

其中：

- `YYYYMM` 表示用于开发该内核的基线代码分支。例如，`202510` 表示该基线分支创建于 2025 年 10 月。它并不表示该内核版本的发布时间。
- `x` 表示该基线分支的补丁发布编号。

例如，`TiDB-X-CLOUD.202510.1` 表示该内核基于 2025 年 10 月创建的分支，并且是从该分支构建的第一个补丁版本。

由于内核开发与发布时间表彼此独立，因此某个内核版本可能会在其基线分支创建数月后才发布。

由于 TiDB Cloud Premium 遵循自身的内核发布节奏，[TiDB Cloud Premium release notes](/tidb-cloud/releases/tidb-x-cloud.202510.1.md) 与 [TiDB Self-Managed release notes](https://docs.pingcap.com/releases/tidb-self-managed/) 分开发布。

## FAQ {#faq}

### 我可以为我的 TiDB Cloud Premium 实例选择内核版本吗？ {#can-i-choose-the-kernel-version-for-my-tidb-cloud-premium-instance}

不可以。TiDB Cloud 会管理 TiDB Cloud Premium 的整个内核生命周期。

TiDB Cloud 会自动为新的部署提供经过验证的内核版本，并在适当时执行托管升级。这有助于确保安全性、稳定性、兼容性，以及在无需手动维护的情况下访问最新功能和改进。