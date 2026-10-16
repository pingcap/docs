---
title: TiDB Cloud BYOC 多 Region 部署
summary: 本文档概述了在多个 AWS Region 中部署 TiDB Cloud BYOC 的流程。
---

# TiDB Cloud BYOC 多 Region 部署

TiDB Cloud BYOC 支持跨 **多个 AWS Region** 的部署。相同的 IAM 角色可以在不同 Region 之间复用，因此在启用额外 Region 时，无需重新创建 BYOC IAM 角色。

多 Region 部署适用于以下两种场景：

| 场景 | 描述 | 脚本 |
| ----- | ----- | ----- |
| 新的多 Region 部署 | 尚未部署任何 BYOC Region，并且从一开始就计划部署多个 Region。 | `tidbcloud-byoc-setup.sh` |
| 向现有部署添加 Region | 已经部署了一个或多个 BYOC Region，并计划后续再启用额外的 Region。 | `tidbcloud-byoc-update.sh` |

* 对于一开始就规划了多个 Region 的新部署，请参见 [场景 1：新的多 Region 部署](#scenario-1-new-multi-region-deployment)。
* 如需向现有 BYOC 部署添加 Region，请参见 [场景 2：向现有 BYOC 部署添加 Region](#scenario-2-add-a-region-to-an-existing-byoc-deployment)。

## 资源规划：共享资源与专用资源 {#resource-planning-shared-and-dedicated-resources}

在配置多个 Region 之前，请先确定以下基础资源是在各 Region 之间共享，还是为每个 Region 单独配置：

* AWS private certificate authority (PCA)
* TiDB 的 Route 53 hosted zone

### 共享资源 {#shared-resources}

同一个 PCA 和 TiDB hosted zone 可以在所有已启用的 Region 之间共享。

在这种配置下，通过标准参数提供主 Region 的 PCA 和 TiDB hosted zone，并省略对应的 `--additional-*` 参数。

### 专用资源 {#dedicated-resources}

你可以为每个额外 Region 准备独立的 PCA 和 TiDB hosted zone。

主 Region 的资源通过以下标准参数提供：

* `--pca-arn`
* `--tidb-hz-id`

额外 Region 的资源通过以下参数提供：

* `--additional-pca-arns`
* `--additional-tidb-hz-ids`

如果有两个或更多额外 Region，请按相同的 Region 顺序，以逗号分隔列表的形式提供这些值。

### 混合资源 {#mixed-resources}

共享资源和专用资源可以组合使用。

例如，所有 Region 可以共享同一个 PCA，同时使用各自独立的 TiDB hosted zone。

每个额外资源参数都是独立的。如果对应资源继续与主 Region 共享，则省略该参数。

## 场景 1：新的多 Region 部署 {#scenario-1-new-multi-region-deployment}

如果你尚未部署任何 BYOC Region，并计划从一开始就部署多个 Region，请使用本节。

运行 `tidbcloud-byoc-setup.sh` 以初始化 BYOC 环境并配置所需资源。

### 所有 Region 共享相同资源 {#all-regions-share-the-same-resources}

当所有 Region 共享同一个 PCA 和 TiDB hosted zone 时，运行标准初始化命令：

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <SharedTidbHostedZoneId> \
  --pca-arn <SharedPCAArn>
```

不需要 `--additional-*` 参数。

### 额外 Region 使用专用资源 {#additional-regions-use-dedicated-resources}

通过标准参数提供主 Region 的资源，并通过 `--additional-*` 参数提供额外 Region 的资源：

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <Region1TidbHostedZoneId> \
  --pca-arn <Region1PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn>
```

所有逗号分隔列表中的值都必须遵循相同的 Region 顺序。例如：

* 第一个值表示 Region 2。
* 第二个值表示 Region 3。

### 混合使用共享资源和专用资源 {#mixed-shared-and-dedicated-resources}

以下示例中，所有 Region 共享一个 PCA，但使用各自独立的 TiDB hosted zone：

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <Region1TidbHostedZoneId> \
  --pca-arn <SharedPCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId>
```

由于 PCA 是共享的，因此省略了 `--additional-pca-arns`。

## 场景 2：向现有 BYOC 部署添加 Region {#scenario-2-add-a-region-to-an-existing-byoc-deployment}

如果已经部署了一个或多个 BYOC Region，并且你希望再添加一个或多个新 Region，请使用本节。

不要再次运行 `tidbcloud-byoc-setup.sh`。

请使用 `tidbcloud-byoc-update.sh` 来更新现有的 CloudFormation 堆栈。现有 IAM 角色和之前已配置的堆栈参数将被复用。

### 添加 Region 之前 {#before-adding-the-region}

在运行更新脚本之前：

1. 确认要添加的 AWS Region。
2. 为新 Region 选择可用区。一个 Region 资源池至少需要三个符合条件的可用区。如果你计划在新 Region 中创建 Region 资源池，请为该 Region 至少选择三个符合条件的可用区。
3. 为每个新 Region 规划 O11Y CIDR，以及你计划创建的资源池所使用的资源池 CIDR。不同 Region 可以使用相同的 O11Y CIDR。但是，如果你使用 metric integration 将 Grafana 连接到多个 Region，请为这些 Region 使用互不重叠的 O11Y CIDR。
4. 确认每个新 Region 是否将：
    * 共享现有的 PCA 和 TiDB hosted zone，或
    * 使用专用的 PCA 和 TiDB hosted zone。
5. 检查并提高每个新 Region 中的 AWS service quotas。
6. 将新 Region 的相关信息提供给你的 TiDB Cloud 代表。

对于每个新 Region，O11Y CIDR 和资源池 CIDR 不能与以下任一项重叠：

* 同一 Region 中的 O11Y CIDR；
* 同一 Region 中任何现有的资源池 CIDR；
* 将通过 VPC Peering 或 VPN 连接的现有 application VPC、本地网络或 VPN 网络；或
* 如果资源池将参与跨 Region 副本，则不能与其他 Region 中的资源池 CIDR 重叠。

不同 Region 中的资源池 CIDR 可以重叠。但是，对于需要跨 Region 连通性或副本的资源池，请使用互不重叠的 CIDR。

### 共享现有的 PCA 和 TiDB hosted zone {#share-an-existing-pca-and-tidb-hosted-zone}

如果所有新 Region 都将共享现有部署已使用的 PCA 和 TiDB hosted zone，请使用此选项。

不需要额外的资源参数：

```shell
bash tidbcloud-byoc-update.sh \
  --stack all
```

现有资源将继续供所有已启用的 Region 使用。

当不需要新的多 Region 资源值时，直接使用 \--stack all 进行更新是安全的。

### 为新 Region 使用专用资源 {#use-dedicated-resources-for-the-new-regions}

如果新 Region 需要专用的 PCA 或 TiDB hosted zone，请使用此选项。

通过对应的 `--additional-*` 参数为新 Region 提供资源：

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId>

```

每个参数都是独立的。如果对应资源继续与现有 Region 共享，则省略该参数。

所有逗号分隔列表中的值都必须遵循相同的 Region 顺序。例如：

* 每个列表中的第一个值表示 Region 2。
* 每个列表中的第二个值表示 Region 3。

### 混合使用共享资源和专用资源 {#use-a-mix-of-shared-and-dedicated-resources}

新 Region 可以共享部分现有资源，同时对其他资源使用专用资源。

例如，要共享现有 PCA，同时为新 Region 使用专用的 TiDB hosted zone：

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId>
```

由于现有 PCA 是共享的，因此省略了 `--additional-pca-arns`。

不同新 Region 之间的资源策略也可以不同。不过，为每个 `--additional-*` 参数提供的值仍必须与相同的 Region 顺序保持一致。

### 当已存在多个 Region 时添加 Region {#add-regions-when-multiple-regions-already-exist}

当现有部署已经包含多个 Region 时，使用相同的修改流程继续添加更多 Region。

多 Region 的资源值会存储在 CloudFormation 堆栈中，并在后续修改时复用。运行修改命令时，请提供新增 Region 所需的任何新增或变更的资源值。

例如，如果 Region 1 是主 Region，Region 2 已经配置完成，并且正在为 Region 3 添加专用资源：

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId>
```

请确保此前已配置的资源值和新添加的资源值都保持正确的 Region 顺序。

### 完成 Region 部署 {#complete-the-regional-deployment}

修改 CloudFormation 堆栈会准备新 Region 所需的账户级权限和资源配置，但这本身并不会完成 Region 基础设施部署。

修改成功后：

1. 将脚本执行结果分享给你的 TiDB Cloud 对接人员。
2. TiDB Cloud 会验证已修改的 IAM 和 Region 资源配置。
3. TiDB Cloud 会为新 Region 启动自动化基础设施预配。
4. 预配完成后，请针对每个新 Region 执行第 5 节中描述的联合验证。