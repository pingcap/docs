---
title: 仅迁移 MySQL 兼容数据库的增量数据到 TiDB Cloud（使用 Data Migration）
summary: 了解如何使用 Data Migration，将托管于 Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL、Azure Database for MySQL、阿里云 RDS，或本地 MySQL 实例的 MySQL 兼容数据库的增量数据迁移到 TiDB Cloud。
---

# 仅迁移 MySQL 兼容数据库的增量数据到 TiDB Cloud（使用 Data Migration）

本文档介绍如何使用 TiDB Cloud 控制台的 Data Migration 功能，将云服务商（Amazon Aurora MySQL、Amazon Relational Database Service (RDS)、Google Cloud SQL for MySQL、Azure Database for MySQL、阿里云 RDS）或自建源数据库中的增量数据，迁移到 <CustomContent plan="dedicated">TiDB Cloud Dedicated</CustomContent><CustomContent plan="essential">TiDB Cloud Essential</CustomContent>。

<CustomContent plan="essential">

> **注意：**
>
> 目前，Data Migration 功能在 TiDB Cloud Essential 上处于 beta 阶段。

</CustomContent>

如需迁移已有数据或同时迁移已有数据和增量数据，请参见 [使用 Data Migration 将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

## 限制

> **注意**：
>
> 本节仅包含增量数据迁移相关的限制。建议你同时阅读通用限制，详见 [限制](/tidb-cloud/migrate-from-mysql-using-data-migration.md#limitations)。

- 如果目标数据库中尚未创建目标表，迁移任务会报错并失败。此时，你需要手动创建目标表，然后重试迁移任务。错误示例如下：

    ```sql
    startLocation: [position: (mysql_bin.000016, 5122), gtid-set:
    00000000-0000-0000-0000-00000000000000000], endLocation:
    [position: (mysql_bin.000016, 5162), gtid-set: 0000000-0000-0000
    0000-0000000000000:0]: cannot fetch downstream table schema of
    zm`.'table1' to initialize upstream schema 'zm'.'table1' in schema
    tracker Raw Cause: Error 1146: Table 'zm.table1' doesn't exist
    ```

- 如果上游有部分行被删除或修改（如：修改行），而下游没有对应的行，则在同步上游的 `DELETE` 和 `UPDATE` DML 操作时，迁移任务会检测到没有可删除或可修改的行。

如果你指定 GTID 作为增量数据迁移的起始位置，请注意以下限制：

- 确保源数据库已开启 GTID 模式。
- 如果源数据库为 MySQL，MySQL 版本必须为 5.6 或更高，且 storage engine 必须为 InnoDB。
- 如果迁移任务连接到上游的从库，则无法迁移 `REPLICATE CREATE TABLE ... SELECT` 事件。原因是该 statement 会被切分为两个 transaction（`CREATE TABLE` 和 `INSERT`），并分配相同的 GTID，导致从库会忽略 `INSERT` statement。

## 前置条件

> **注意**：
>
> 本节仅包含增量数据迁移相关的前置条件。建议你同时阅读[通用前置条件](/tidb-cloud/migrate-from-mysql-using-data-migration.md#prerequisites)。

如果你希望使用 GTID 指定起始位置，请确保源数据库已开启 GTID。具体操作因数据库类型而异。

### 针对 Amazon RDS 和 Amazon Aurora MySQL

对于 Amazon RDS 和 Amazon Aurora MySQL，你需要创建一个新的可修改 parameter group（即非默认 parameter group），在该 parameter group 中修改以下参数，并重启实例以使配置生效。

- `gtid_mode`
- `enforce_gtid_consistency`

你可以通过执行以下 SQL 语句检查 GTID 模式是否已成功开启：

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

如果结果为 `ON` 或 `ON_PERMISSIVE`，则 GTID 模式已成功开启。

更多信息请参见 [Parameters for GTID-based replication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/mysql-replication-gtid.html#mysql-replication-gtid.parameters)。

### 针对 Google Cloud SQL for MySQL

Google Cloud SQL for MySQL 默认已开启 GTID 模式。你可以通过执行以下 SQL 语句检查 GTID 模式是否已成功开启：

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

如果结果为 `ON` 或 `ON_PERMISSIVE`，则 GTID 模式已成功开启。

### 针对 Azure Database for MySQL

Azure Database for MySQL（5.7 及以上版本）默认已开启 GTID 模式，且不支持关闭 GTID 模式。

此外，请确保 `binlog_row_image` server parameter 设置为 `FULL`。你可以通过执行以下 SQL 语句进行检查：

```sql
SHOW VARIABLES LIKE 'binlog_row_image';
```

如果结果不是 `FULL`，你需要通过 [Azure portal](https://portal.azure.com/) 或 [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/) 配置该参数。

### 针对阿里云 RDS MySQL

阿里云 RDS MySQL 默认已开启 GTID 模式。你可以通过执行以下 SQL 语句检查 GTID 模式是否已成功开启：

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

如果结果为 `ON` 或 `ON_PERMISSIVE`，则 GTID 模式已成功开启。

此外，请确保 `binlog_row_image` server parameter 设置为 `FULL`。你可以通过执行以下 SQL 语句进行检查：

```sql
SHOW VARIABLES LIKE 'binlog_row_image';
```

如果结果不是 `FULL`，你需要通过 [RDS 控制台](https://rds.console.aliyun.com/) 配置该参数。

### 针对自建 MySQL 实例

> **注意**：
>
> 具体步骤和命令可能因 MySQL 版本和配置不同而有所差异。请确保你了解开启 GTID 的影响，并在非生产环境中充分测试和验证后再进行操作。

要为自建 MySQL 实例开启 GTID 模式，请按以下步骤操作：

1. 使用具有相应权限的 MySQL client 连接到 MySQL server。

2. 执行以下 SQL 语句以开启 GTID 模式：

    ```sql
    -- Enable the GTID mode
    SET GLOBAL gtid_mode = ON;

    -- Enable `enforce_gtid_consistency`
    SET GLOBAL enforce_gtid_consistency = ON;

    -- Reload the GTID configuration
    RESET MASTER;
    ```

3. 重启 MySQL server 以确保配置生效。

4. 通过执行以下 SQL 语句检查 GTID 模式是否已成功开启：

    ```sql
    SHOW VARIABLES LIKE 'gtid_mode';
    ```

    如果结果为 `ON` 或 `ON_PERMISSIVE`，则 GTID 模式已成功开启。

## 步骤 1：进入 Data Migration 页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以通过左上角的下拉框切换 organization、project 和 cluster。

2. 点击目标 cluster 的名称，进入其概览页面，然后在左侧导航栏点击 **Data** > **Data Migration**。

3. 在 **Data Migration** 页面，点击右上角的 **Create Migration Job**。此时会进入 **Create Migration Job** 页面。

## 步骤 2：配置源和目标连接

在 **Create Migration Job** 页面，配置源和目标连接信息。

1. 输入任务名称，必须以字母开头，且长度小于 60 个字符。可包含字母（A-Z, a-z）、数字（0-9）、下划线（_）和连字符（-）。

2. 填写源连接信息。

    - **Data source**：数据源类型。
    - **Region**：数据源的 Region，仅云数据库必填。
    - **Connectivity method**：数据源的连接方法。<CustomContent plan="dedicated">目前，你可以根据连接方法选择 public IP、VPC Peering 或 Private Link。</CustomContent><CustomContent plan="essential">你可以根据连接方法选择 public IP 或 Private Link。</CustomContent>

    <CustomContent plan="dedicated">

    - **Hostname or IP address**（适用于 public IP 和 VPC Peering）：数据源的主机名或 IP 地址。
    - **Service Name**（适用于 Private Link）：endpoint service 名称。

    </CustomContent>
    <CustomContent plan="essential">

    - **Hostname or IP address**（适用于 public IP）：数据源的主机名或 IP 地址。
    - **Private Link Connection**（适用于 Private Link）：你在 [Private Link Connections](/tidb-cloud/serverless-private-link-connection.md) 部分创建的 private link 连接。

    </CustomContent>

    - **Port**：数据源的端口。
    - **Username**：数据源的用户名。
    - **Password**：用户名对应的密码。
    - **SSL/TLS**：如启用 SSL/TLS，需要上传数据源的证书，可包括以下任意一种：
        - 仅 CA 证书
        - client 证书和 client key
        - CA 证书、client 证书和 client key

3. 填写目标连接信息。

   - **Username**：输入 TiDB Cloud 目标 cluster 的用户名。
   - **Password**：输入 TiDB Cloud 用户名的密码。

4. 点击 **Validate Connection and Next** 验证你填写的信息。

5. 根据提示信息进行操作：

    <CustomContent plan="dedicated">

    - 如果你使用 Public IP 或 VPC Peering，需要将 Data Migration service 的 IP 地址添加到源数据库和防火墙（如有）的 IP Access List。
    - 如果你使用 AWS Private Link，系统会提示你接受 endpoint request。请前往 [AWS VPC 控制台](https://us-west-2.console.aws.amazon.com/vpc/home)，点击 **Endpoint services** 接受 endpoint request。

    </CustomContent>
    <CustomContent plan="essential">

    如果你使用 Public IP，需要将 Data Migration service 的 IP 地址添加到源数据库和防火墙（如有）的 IP Access List。

    </CustomContent>

## 步骤 3：选择迁移任务类型

如需仅将源数据库的增量数据迁移到 TiDB Cloud，请选择 **Incremental data migration**，不要选择 **Existing data migration**。这样，迁移任务只会迁移源数据库的实时变更到 TiDB Cloud。

在 **Start Position** 区域，你可以为增量数据迁移指定以下任一类型的起始位置：

- 增量迁移任务启动的时间
- GTID
- Binlog 文件名和位置

迁移任务启动后，起始位置不可更改。

### 增量迁移任务启动的时间

如果选择此选项，迁移任务只会迁移迁移任务启动后在源数据库中产生的增量数据。

### 指定 GTID

选择此选项可指定源数据库的 GTID，例如 `3E11FA47-71CA-11E1-9E33-C80AA9429562:1-23`。迁移任务会同步不包含在指定 GTID 集合中的 transaction，将源数据库的实时变更迁移到 TiDB Cloud。

你可以运行以下命令查看源数据库的 GTID：

```sql
SHOW MASTER STATUS;
```

关于如何开启 GTID，参见[前置条件](#prerequisites)。

### 指定 binlog 文件名和位置

选择此选项可指定源数据库的 binlog 文件名（如 `binlog.000001`）和 binlog 位置（如 `1307`）。迁移任务将从指定的 binlog 文件名和位置开始，将源数据库的实时变更迁移到 TiDB Cloud。

你可以运行以下命令查看源数据库的 binlog 文件名和位置：

```sql
SHOW MASTER STATUS;
```

如果目标数据库中已有数据，请确保 binlog 位置正确。否则，现有数据和增量数据可能发生冲突。如果发生冲突，迁移任务会失败。如果你希望用源数据库的数据覆盖冲突记录，可以恢复迁移任务。

## 步骤 4：选择要迁移的对象

1. 在 **Choose Objects to Migrate** 页面，选择要迁移的对象。你可以点击 **All** 选择全部对象，或点击 **Customize**，然后勾选对象名称旁的复选框选择对象。

2. 点击 **Next**。

## 步骤 5：前置检查

在 **Precheck** 页面，你可以查看前置检查结果。如果前置检查失败，请根据 **Failed** 或 **Warning** 详情进行操作，然后点击 **Check again** 重新检查。

如果仅有部分检查项为 warning，你可以评估风险，决定是否忽略 warning。如果所有 warning 均被忽略，迁移任务会自动进入下一步。

更多错误及解决方法，参见 [前置检查错误及解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions)。

更多前置检查项说明，参见 [Migration Task Precheck](https://docs.pingcap.com/tidb/stable/dm-precheck)。

如果所有检查项均为 **Pass**，点击 **Next**。

<CustomContent plan="essential">

## 步骤 6：查看迁移进度

迁移任务创建后，你可以在 **Migration Job Details** 页面查看迁移进度。迁移进度显示在 **Stage and Status** 区域。

你可以在任务运行时暂停或删除迁移任务。

如果迁移任务失败，解决问题后可以恢复任务。

你可以在任意状态下删除迁移任务。

如迁移过程中遇到问题，参见 [迁移错误及解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)。

</CustomContent>

<CustomContent plan="dedicated">

## 步骤 6：选择规格并启动迁移

在 **Choose a Spec and Start Migration** 页面，根据你的性能需求选择合适的迁移规格。关于规格详情，参见 [Data Migration 规格说明](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)。

选择规格后，点击 **Create Job and Start** 启动迁移。

## 步骤 7：查看迁移进度

迁移任务创建后，你可以在 **Migration Job Details** 页面查看迁移进度。迁移进度显示在 **Stage and Status** 区域。

你可以在任务运行时暂停或删除迁移任务。

如果迁移任务失败，解决问题后可以恢复任务。

你可以在任意状态下删除迁移任务。

如迁移过程中遇到问题，参见 [迁移错误及解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)。

</CustomContent>