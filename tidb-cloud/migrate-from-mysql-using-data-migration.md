---
title: 使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud
summary: 了解如何使用数据迁移功能，将你的 MySQL 数据库（包括 Amazon Aurora MySQL、Amazon RDS、Azure Database for MySQL - Flexible Server、Google Cloud SQL for MySQL 或自建 MySQL 实例）无缝迁移到 TiDB Cloud，并实现最小化停机时间。
aliases: ['/tidbcloud/migrate-data-into-tidb','/tidbcloud/migrate-incremental-data-from-mysql']
---

# 使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud

本文档将指导你如何在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，使用数据迁移功能将你的 MySQL 数据库（包括 Amazon Aurora MySQL、Amazon RDS、Azure Database for MySQL - Flexible Server、Google Cloud SQL for MySQL 或自建 MySQL 实例）迁移到 TiDB Cloud。

该功能支持将现有 MySQL 数据迁移到 TiDB Cloud，并持续实时同步 MySQL 兼容源数据库的变更（binlog），无论源库和目标库是否在同一区域，都能保证数据一致性。该流程无需单独的导出和导入操作，极大减少了停机时间，简化了从 MySQL 向更具扩展性的 TiDB Cloud 平台的迁移过程。

如果你只想将 MySQL 兼容数据库的 binlog 增量变更同步到 TiDB Cloud，请参见 [使用数据迁移将 MySQL 兼容数据库的增量数据迁移到 TiDB Cloud](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

## 限制

### 可用性

- 数据迁移功能仅适用于 **TiDB Cloud Dedicated** 集群。

- 如果你在 [TiDB Cloud 控制台](https://tidbcloud.com/)的 TiDB Cloud Dedicated 集群中未看到 [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md#step-1-go-to-the-data-migration-page) 入口，说明该功能在你所在的区域暂不可用。如需支持，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

- Amazon Aurora MySQL writer 实例支持现有数据和增量数据迁移。Amazon Aurora MySQL reader 实例仅支持现有数据迁移，不支持增量数据迁移。

### 迁移任务数量上限

每个组织最多可创建 200 个迁移任务。如需创建更多迁移任务，请 [提交支持工单](/tidb-cloud/tidb-cloud-support.md)。

### 被过滤和已删除的数据库

- 系统数据库会被自动过滤，即使你选择迁移所有数据库，也不会迁移到 TiDB Cloud。即 `mysql`、`information_schema`、`performance_schema` 和 `sys` 不会通过该功能迁移。

- 当你在 TiDB Cloud 中删除集群时，该集群下的所有迁移任务会被自动删除且无法恢复。

### 现有数据迁移的限制

- 在现有数据迁移过程中，如果目标数据库已存在待迁移的表且存在主键冲突，则会用新数据替换重复主键的行。

- 如果你的数据集小于 1 TiB，建议使用逻辑模式（默认模式）。如果数据集大于 1 TiB，或希望更快迁移现有数据，可以使用物理模式。详见 [迁移现有数据和增量数据](#migrate-existing-data-and-incremental-data)。

### 增量数据迁移的限制

- 在增量数据迁移过程中，如果目标数据库已存在待迁移的表且存在主键冲突，会报错并中断迁移。此时需确认 MySQL 源数据是否准确，如确认无误，可点击迁移任务的 "Restart" 按钮，迁移任务会用 MySQL 源数据替换 TiDB Cloud 集群中冲突的记录。

- 在增量同步（将实时变更迁移到集群）过程中，如果迁移任务从异常中恢复，可能会进入 60 秒的安全模式。在安全模式下，`INSERT` 语句会以 `REPLACE` 方式迁移，`UPDATE` 语句会以 `DELETE` 和 `REPLACE` 方式迁移，然后将这些事务同步到目标 TiDB Cloud 集群，以确保异常期间的数据能顺利迁移。在此场景下，如果 MySQL 源表没有主键或非空唯一索引，目标 TiDB Cloud 集群中可能会出现重复数据，因为数据可能被多次插入。

- 在以下场景中，如果迁移任务耗时超过 24 小时，请勿清理源数据库的 binary log，以保证数据迁移能获取连续的 binlog 进行增量同步：

    - 现有数据迁移期间。
    - 现有数据迁移完成后，首次启动增量数据迁移且延迟不为 0ms 时。

## 前置条件

在迁移前，请检查数据源是否受支持，确保 MySQL 兼容数据库已开启 binary log，保证网络连通性，并为源数据库和目标 TiDB Cloud 集群数据库授予所需权限。

### 确认数据源及版本受支持

数据迁移支持以下数据源及版本：

| 数据源 | 支持的版本 |
|:------------|:-------------------|
| 自建 MySQL（本地或公有云） | 8.0, 5.7, 5.6 |
| Amazon Aurora MySQL | 8.0, 5.7, 5.6 |
| Amazon RDS MySQL | 8.0, 5.7 |
| Azure Database for MySQL - Flexible Server | 8.0, 5.7 |
| Google Cloud SQL for MySQL | 8.0, 5.7, 5.6 |

### 在源 MySQL 兼容数据库中开启 binary log 以支持同步

要使用 DM 持续同步源 MySQL 兼容数据库的增量变更到 TiDB Cloud 目标集群，需在源数据库中进行如下配置以开启 binary log：

| 配置项 | 要求的值 | 说明 |
|:--------------|:---------------|:----|
| `log_bin` | `ON` | 启用 binary log，DM 用于同步变更到 TiDB |
| `binlog_format` | `ROW` | 精确捕获所有数据变更（其他格式可能遗漏边界场景）|
| `binlog_row_image` | `FULL` | 事件中包含所有列值，便于安全冲突处理 |
| `binlog_expire_logs_seconds` | ≥ `86400`（1 天），`604800`（7 天，推荐）| 确保迁移期间 DM 能访问连续的 binlog |

#### 检查当前值并配置源 MySQL 实例

要检查当前配置，连接到源 MySQL 实例并执行以下语句：

```sql
SHOW VARIABLES WHERE Variable_name IN
('log_bin','server_id','binlog_format','binlog_row_image',
'binlog_expire_logs_seconds','expire_logs_days');
```

如有必要，请将源 MySQL 实例配置修改为要求的值。

<details>
<summary> 配置自建 MySQL 实例 </summary>

1. 打开 `/etc/my.cnf`，添加如下内容：

    ```
    [mysqld]
    log_bin = mysql-bin
    binlog_format = ROW
    binlog_row_image = FULL
    binlog_expire_logs_seconds = 604800   # 7 天保留
    ```

2. 重启 MySQL 服务以应用更改：

    ```
    sudo systemctl restart mysqld
    ```

3. 再次运行 `SHOW VARIABLES` 语句，确认设置生效。

详细说明请参见 MySQL 官方文档：[MySQL Server System Variables](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html) 和 [The Binary Log](https://dev.mysql.com/doc/refman/8.0/en/binary-log.html)。

</details>

<details>
<summary> 配置 AWS RDS 或 Aurora MySQL </summary>

1. 在 AWS 管理控制台，打开 [Amazon RDS 控制台](https://console.aws.amazon.com/rds/)，点击左侧导航栏的 **Parameter groups**，创建或编辑自定义参数组。
2. 将上述四个参数设置为要求的值。
3. 将参数组关联到你的实例或集群，并重启以应用更改。
4. 重启后，连接实例并运行 `SHOW VARIABLES` 语句，验证配置。

详细说明请参见 AWS 官方文档：[Working with DB Parameter Groups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html) 和 [Configuring MySQL Binary Logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)。

</details>

<details>
<summary> 配置 Azure Database for MySQL - Flexible Server </summary>

1. 在 [Azure 门户](https://portal.azure.com/)中，搜索并选择 **Azure Database for MySQL servers**，点击你的实例名，然后在左侧导航栏点击 **Setting** > **Server parameters**。

2. 搜索每个参数并更新其值。

    大多数更改无需重启即可生效。如需重启，门户会有提示。

3. 运行 `SHOW VARIABLES` 语句，验证配置。

详细说明请参见 Microsoft Azure 官方文档：[Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-configure-server-parameters-portal)。

</details>

<details>
<summary> 配置 Google Cloud SQL for MySQL </summary>

1. 在 [Google Cloud 控制台](https://console.cloud.google.com/project/_/sql/instances)中，选择包含你的实例的项目，点击实例名，然后点击 **Edit**。
2. 添加或修改所需的 flags（`log_bin`、`binlog_format`、`binlog_row_image`、`binlog_expire_logs_seconds`）。
3. 点击 **Save**。如需重启，控制台会有提示。
4. 重启后，运行 `SHOW VARIABLES` 语句确认更改。

详细说明请参见 Google Cloud 官方文档：[Configure database flags](https://cloud.google.com/sql/docs/mysql/flags) 和 [Use point-in-time recovery](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr)。

</details>

### 确保网络连通性

在创建迁移任务前，你需要规划并建立源 MySQL 实例、TiDB Cloud 数据迁移（DM）服务与目标 TiDB Cloud 集群之间的网络连通性。

可用的连接方式如下：

| 连接方式 | 可用性 | 推荐场景 |
|:---------------------|:-------------|:----------------|
| 公网端点或 IP 地址 | 所有 TiDB Cloud 支持的云服务商 | 快速 PoC 迁移、测试或无法使用私有连接时 |
| 私有链路或私有端点 | 仅 AWS 和 Azure | 生产环境，避免数据暴露在公网 |
| VPC Peering | 仅 AWS 和 Google Cloud | 生产环境，需低延迟、同区域连接且 VPC/VNet CIDR 不重叠 |

请选择最适合你的云服务商、网络拓扑和安全需求的连接方式，并按照对应方式的设置说明进行配置。

#### 端到端 TLS/SSL 加密

无论采用哪种连接方式，强烈建议使用 TLS/SSL 实现端到端加密。私有端点和 VPC Peering 保障了网络路径安全，TLS/SSL 则保障了数据本身的安全，有助于满足合规要求。

<details>
<summary> 下载并保存云服务商的证书以支持 TLS/SSL 加密连接 </summary>

- Amazon Aurora MySQL 或 Amazon RDS MySQL: [Using SSL/TLS to encrypt a connection to a DB instance or cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html)
- Azure Database for MySQL - Flexible Server: [Connect with encrypted connections](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-connect-tls-ssl)
- Google Cloud SQL for MySQL: [Manage SSL/TLS certificates](https://cloud.google.com/sql/docs/mysql/manage-ssl-instance)

</details>

#### 公网端点或 IP 地址

使用公网端点时，你可以在现在和后续 DM 任务创建过程中验证网络连通性和访问权限。TiDB Cloud 会在该阶段提供具体的出口 IP 地址及相关操作提示。

> **注意**：
>
> 出口 IP 范围仅在创建数据迁移任务时可见，无法提前获取。请确保：
>
> - 你有权限修改防火墙规则。
> - 你可以在设置过程中访问云服务商控制台。
> - 你可以在任务创建流程中暂停以配置防火墙。

1. 确认并记录源 MySQL 实例的端点主机名（FQDN）或公网 IP 地址。
2. 确保你有权限修改数据库的防火墙或安全组规则。可参考以下云服务商文档：

    - Amazon Aurora MySQL 或 Amazon RDS MySQL: [Controlling access with security groups](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Overview.RDSSecurityGroups.html)。
    - Azure Database for MySQL - Flexible Server: [Public Network Access](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-networking-public)
    - Google Cloud SQL for MySQL: [Authorized Networks](https://cloud.google.com/sql/docs/mysql/configure-ip#authorized-networks)。

3. 可选：使用合适的证书，在有公网访问权限的机器上验证源数据库连通性：

    ```shell
    mysql -h <public-host> -P <port> -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. 后续在数据迁移任务设置过程中，TiDB Cloud 会提供出口 IP 范围。届时需将该 IP 范围添加到数据库的防火墙或安全组规则中，操作方式同上。

#### 私有链路或私有端点

如使用云服务商原生的私有链路或私有端点，请为源 MySQL 实例（RDS、Aurora 或 Azure Database for MySQL）创建私有端点。

<details>
<summary> 为 MySQL 源数据库设置 AWS PrivateLink 和私有端点 </summary>

AWS 不支持直接通过 PrivateLink 访问 RDS 或 Aurora。因此，你需要创建一个 Network Load Balancer（NLB），并将其作为端点服务关联到你的源 MySQL 实例。

1. 在 [Amazon EC2 控制台](https://console.aws.amazon.com/ec2/)中，在与 RDS 或 Aurora writer 相同的子网创建 NLB。为 NLB 配置 TCP 监听器（端口 `3306`），将流量转发到数据库端点。

    详细说明请参见 AWS 官方文档：[Create a Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html)。

2. 在 [Amazon VPC 控制台](https://console.aws.amazon.com/vpc/)中，点击左侧导航栏的 **Endpoint Services**，创建端点服务。设置过程中，选择上一步创建的 NLB 作为后端负载均衡器，并启用 **Require acceptance for endpoint** 选项。端点服务创建后，复制服务名（格式为 `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx`）以备后用。

    详细说明请参见 AWS 官方文档：[Create an endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html)。

3. 可选：在同一 VPC 或 VNet 内的堡垒机或客户端测试连通性：

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. 后续在配置 TiDB Cloud DM 通过 PrivateLink 连接时，你需要返回 AWS 控制台，批准 TiDB Cloud 到该私有端点的连接请求。

</details>

<details>
<summary> 为 MySQL 源数据库设置 Azure PrivateLink 和私有端点 </summary>

Azure Database for MySQL - Flexible Server 支持原生私有端点。你可以在创建 MySQL 实例时启用私有访问（VNet 集成），也可以后续添加私有端点。

如需添加新私有端点，操作如下：

1. 在 [Azure 门户](https://portal.azure.com/)中，搜索并选择 **Azure Database for MySQL servers**，点击你的实例名，然后点击左侧导航栏的 **Setting** > **Networking**。
2. 在 **Networking** 页面，向下滚动到 **Private endpoints** 区域，点击 **+ Create private endpoint**，并按照页面提示完成设置。

    设置过程中，在 **Virtual Network** 标签页选择 TiDB Cloud 可访问的虚拟网络和子网，在 **DNS** 标签页保持 **Private DNS integration** 启用。私有端点创建并部署后，点击 **Go to resource**，点击左侧导航栏的 **Settings** > **DNS configuration**，在 **Customer Visible FQDNs** 区域找到用于连接实例的主机名，通常格式为 `<your-instance-name>.mysql.database.azure.com`。

    详细说明请参见 Azure 官方文档：[Create a private endpoint via Private Link Center](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-networking-private-link-portal#create-a-private-endpoint-via-private-link-center)。

3. 可选：在同一 VPC 或 VNet 内的堡垒机或客户端测试连通性：

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. 在 [Azure 门户](https://portal.azure.com/)中，返回 MySQL Flexible Server 实例的概览页面（不是私有端点对象），点击 **Essentials** 区域的 **JSON View**，复制资源 ID 以备后用。资源 ID 格式为 `/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>`。你将在配置 TiDB Cloud DM 时使用该资源 ID（不是私有端点 ID）。

5. 后续在配置 TiDB Cloud DM 通过 PrivateLink 连接时，你需要返回 Azure 门户，批准 TiDB Cloud 到该私有端点的连接请求。

</details>

#### VPC Peering

如使用 AWS VPC Peering 或 Google Cloud VPC 网络 Peering，请参考以下说明配置网络。

<details>
<summary> 配置 AWS VPC Peering</summary>

如你的 MySQL 服务在 AWS VPC 中，操作如下：

1. [建立 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md)，连接 MySQL 服务所在 VPC 与 TiDB 集群所在 VPC。

2. 修改 MySQL 服务关联的安全组的入站规则。

    你必须将 [TiDB Cloud 集群所在区域的 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 添加到入站规则，允许 TiDB 集群流量访问 MySQL 实例。

3. 如 MySQL URL 包含 DNS 主机名，你需允许 TiDB Cloud 能解析 MySQL 服务的主机名。

    1. 按照 [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns) 步骤操作。
    2. 启用 **Accepter DNS resolution** 选项。

</details>

<details>
<summary> 配置 Google Cloud VPC 网络 Peering </summary>

如你的 MySQL 服务在 Google Cloud VPC 中，操作如下：

1. 如为自建 MySQL，可跳过此步。若为 Google Cloud SQL，需在 Google Cloud SQL 实例关联的 VPC 中暴露 MySQL 端点。你可能需要使用 Google 提供的 [Cloud SQL Auth proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy)。

2. [建立 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md)，连接你的 MySQL 服务所在 VPC 与 TiDB 集群所在 VPC。

3. 修改 MySQL 所在 VPC 的 ingress 防火墙规则。

    你必须将 [TiDB Cloud 集群所在区域的 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 添加到 ingress 防火墙规则，允许 TiDB 集群流量访问 MySQL 端点。

</details>

### 授权迁移所需权限

在开始迁移前，你需要在源数据库和目标数据库分别创建合适的数据库用户，并授予所需权限。这些权限用于让 TiDB Cloud DM 读取 MySQL 数据、同步变更并安全写入 TiDB Cloud 集群。由于迁移涉及现有数据的全量导出和增量变更的 binlog 同步，迁移用户需具备超出只读权限的特定权限。

#### 为源 MySQL 数据库的迁移用户授权

测试时可使用源 MySQL 数据库的管理员用户（如 `root`）。

生产环境建议为数据导出和同步专门创建用户，并仅授予必要权限：

| 权限 | 作用范围 | 说明 |
|:----------|:------|:--------|
| `SELECT` | 表 | 允许读取所有表数据 |
| `RELOAD` | 全局 | 确保全量导出时快照一致性 |
| `REPLICATION SLAVE` | 全局 | 启用 binlog 流式同步 |
| `REPLICATION CLIENT` | 全局 | 获取 binlog 位置和服务器状态 |

例如，可在源 MySQL 实例中执行如下 `GRANT` 语句：

```sql
GRANT SELECT, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'dm_source_user'@'%';
```

#### 为目标 TiDB Cloud 集群授权

测试时可使用 TiDB Cloud 集群的 `root` 账号。

生产环境建议为同步专门创建用户，并仅授予必要权限：

| 权限 | 作用范围 | 说明 |
|:----------|:------|:--------|
| `CREATE` | 数据库、表 | 在目标库创建 schema 对象 |
| `SELECT` | 表 | 迁移过程中校验数据 |
| `INSERT` | 表 | 写入迁移数据 |
| `UPDATE` | 表 | 增量同步时修改已有行 |
| `DELETE` | 表 | 同步或更新时删除行 |
| `ALTER`  | 表 | schema 变更时修改表结构 |
| `DROP`   | 数据库、表 | schema 同步时删除对象 |
| `INDEX`  | 表 | 创建和修改索引 |
| `CREATE VIEW`  | 视图 | 创建迁移所需视图 |

例如，可在目标 TiDB Cloud 集群中执行如下 `GRANT` 语句：

```sql
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE, ALTER, DROP, INDEX ON *.* TO 'dm_target_user'@'%';
```

## 第 1 步：进入数据迁移页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以通过左上角的下拉框切换组织、项目和集群。

2. 点击目标集群名称进入概览页，然后点击左侧导航栏的 **Data** > **Migration**。

3. 在 **Data Migration** 页面，点击右上角的 **Create Migration Job**。此时会进入 **Create Migration Job** 页面。

## 第 2 步：配置源和目标连接

在 **Create Migration Job** 页面，配置源和目标连接信息。

1. 输入任务名称，需以字母开头，且长度小于 60 个字符。可包含字母（A-Z, a-z）、数字（0-9）、下划线（_）和连字符（-）。

2. 填写源连接信息。

    - **Data source**：数据源类型。
    - **Connectivity method**：根据安全需求和云服务商选择连接方式：
        - **Public IP**：适用于所有云服务商（推荐用于测试和 PoC 迁移）。
        - **Private Link**：仅适用于 AWS 和 Azure（推荐生产环境需私有连接场景）。
        - **VPC Peering**：仅适用于 AWS 和 Google Cloud（推荐生产环境需低延迟、同区域、VPC/VNet CIDR 不重叠场景）。
    - 根据所选 **Connectivity method**，进行如下操作：
        - 选择 **Public IP** 或 **VPC Peering** 时，在 **Hostname or IP address** 字段填写数据源的主机名或 IP 地址。
        - 选择 **Private Link** 时，填写以下信息：
            - **Endpoint Service Name**（数据源为 AWS 时可用）：填写为 RDS 或 Aurora 实例创建的 VPC endpoint service 名称（格式：`com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx`）。
            - **Private Endpoint Resource ID**（数据源为 Azure 时可用）：填写 MySQL Flexible Server 实例的资源 ID（格式：`/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>`）。
    - **Port**：数据源端口。
    - **User Name**：数据源用户名。
    - **Password**：用户名对应密码。
    - **SSL/TLS**：启用 SSL/TLS 以实现端到端数据加密（强烈推荐所有迁移任务开启）。根据 MySQL 服务器的 SSL 配置上传相应证书。

        SSL/TLS 配置选项：

        - 选项 1：仅服务器认证

            - 若 MySQL 服务器仅配置服务器认证，只需上传 **CA Certificate**。
            - 此时，MySQL 服务器出示证书证明身份，TiDB Cloud 用 CA 验证服务器证书。
            - CA 证书可防止中间人攻击，且当 MySQL 服务器以 `require_secure_transport = ON` 启动时为必需。

        - 选项 2：客户端证书认证

            - 若 MySQL 服务器配置了客户端证书认证，需上传 **Client Certificate** 和 **Client private key**。
            - 此时，TiDB Cloud 向 MySQL 服务器出示证书进行认证，但 TiDB Cloud 不验证 MySQL 服务器证书。
            - 该选项通常用于 MySQL 服务器配置了 `REQUIRE SUBJECT '...'` 或 `REQUIRE ISSUER '...'` 且未配置 `REQUIRE X509`，允许仅校验客户端证书的特定属性而不做完整 CA 校验。
            - 该配置常用于 MySQL 服务器接受自签名或自建 PKI 环境下的客户端证书。注意此配置易受中间人攻击，除非有其他网络级安全保障，否则不推荐用于生产环境。

        - 选项 3：双向 TLS（mTLS）- 最高安全级别

            - 若 MySQL 服务器配置了双向 TLS（mTLS）认证，需上传 **CA Certificate**、**Client Certificate** 和 **Client private key**。
            - 此时，MySQL 服务器用客户端证书验证 TiDB Cloud 身份，TiDB Cloud 用 CA 证书验证 MySQL 服务器身份。
            - 当 MySQL 服务器为迁移用户配置了 `REQUIRE X509` 或 `REQUIRE SSL` 时，必须使用此选项。
            - 该选项适用于 MySQL 服务器要求客户端证书认证的场景。
            - 证书可通过以下方式获取：
                - 从云服务商下载（见 [TLS 证书链接](#end-to-end-encryption-over-tlsssl)）。
                - 使用组织内部 CA 证书。
                - 自签名证书（仅限开发/测试）。

3. 填写目标连接信息。

    - **User Name**：输入 TiDB Cloud 目标集群的用户名。
    - **Password**：输入 TiDB Cloud 用户名对应的密码。

4. 点击 **Validate Connection and Next** 验证所填信息。

5. 根据提示信息进行操作：

    - 若选择 **Public IP** 或 **VPC Peering** 作为连接方式，需要将数据迁移服务的 IP 地址添加到源数据库和防火墙（如有）的 IP 访问列表。
    - 若选择 **Private Link** 作为连接方式，需接受端点请求：
        - AWS：进入 [AWS VPC 控制台](https://us-west-2.console.aws.amazon.com/vpc/home)，点击 **Endpoint services**，接受来自 TiDB Cloud 的端点请求。
        - Azure：进入 [Azure 门户](https://portal.azure.com)，搜索你的 MySQL Flexible Server 名称，点击左侧导航栏的 **Setting** > **Networking**，在右侧 **Private endpoint** 区域批准 TiDB Cloud 的待处理连接请求。

## 第 3 步：选择迁移任务类型

在 **Choose the objects to be migrated** 步骤，你可以选择现有数据迁移、增量数据迁移或两者兼有。

### 迁移现有数据和增量数据

如需一次性将数据迁移到 TiDB Cloud，并保证源库与目标库数据一致，选择 **Existing data migration** 和 **Incremental data migration**。

你可以使用 **物理模式** 或 **逻辑模式** 迁移 **现有数据** 和 **增量数据**。

- 默认模式为 **逻辑模式**。该模式将 MySQL 源数据库数据导出为 SQL 语句并在 TiDB 执行。此模式下，目标表可为空或非空，但性能低于物理模式。

- 对于大数据集，推荐使用 **物理模式**。该模式将 MySQL 源数据库数据导出并编码为 KV 对，直接写入 TiKV，性能更高。此模式要求目标表在迁移前为空。以 16 RCU（Replication Capacity Units）规格为例，性能约为逻辑模式的 2.5 倍。其他规格性能较逻辑模式提升 20%~50%。注意性能数据仅供参考，实际场景可能有所不同。

> **注意：**
>
> - 使用物理模式时，现有数据迁移完成前，不能为该 TiDB 集群创建第二个迁移任务或导入任务。
> - 使用物理模式且迁移任务已启动后，**不要** 启用 PITR（时间点恢复）或在集群上有任何 changefeed，否则迁移任务会卡住。如需启用 PITR 或有 changefeed，建议使用逻辑模式迁移数据。

物理模式会尽可能快地导出 MySQL 源数据，不同规格对 MySQL 源数据库导出期间的 QPS 和 TPS 有不同影响。下表展示了各规格的性能回退情况。

| 迁移规格 | 最大导出速度 | MySQL 源数据库性能回退 |
|---------|-------------|--------|
| 2 RCUs   | 80.84 MiB/s  | 15.6% |
| 4 RCUs   | 214.2 MiB/s  | 20.0% |
| 8 RCUs   | 365.5 MiB/s  | 28.9% |
| 16 RCUs | 424.6 MiB/s  | 46.7% |

### 仅迁移现有数据

如只需将源数据库的现有数据迁移到 TiDB Cloud，选择 **Existing data migration**。

仅可使用逻辑模式迁移现有数据。详见 [迁移现有数据和增量数据](#migrate-existing-data-and-incremental-data)。

### 仅迁移增量数据

如只需将源数据库的增量数据迁移到 TiDB Cloud，选择 **Incremental data migration**。此时迁移任务不会迁移源数据库的现有数据，仅迁移任务明确指定的源数据库实时变更。

关于增量数据迁移的详细说明，请参见 [使用数据迁移将 MySQL 兼容数据库的增量数据迁移到 TiDB Cloud](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

## 第 4 步：选择要迁移的对象

1. 在 **Choose Objects to Migrate** 页面，选择要迁移的对象。你可以点击 **All** 选择全部对象，或点击 **Customize**，再勾选对象名称旁的复选框选择对象。

    - 点击 **All** 时，迁移任务会将整个源数据库实例的现有数据迁移到 TiDB Cloud，并在全量迁移后同步实时变更（前提是上一步已勾选 **Existing data migration** 和 **Incremental data migration**）。
    - 点击 **Customize** 并选择部分数据库时，迁移任务会将所选数据库的现有数据和实时变更迁移到 TiDB Cloud（前提是上一步已勾选 **Existing data migration** 和 **Incremental data migration**）。
    - 点击 **Customize** 并选择某数据库下的部分表时，迁移任务仅迁移所选表的现有数据和实时变更。后续在同一数据库中新建的表不会被迁移。

2. 点击 **Next**。

## 第 5 步：预检查

在 **Precheck** 页面，你可以查看预检查结果。如预检查失败，请根据 **Failed** 或 **Warning** 详情进行处理，然后点击 **Check again** 重新检查。

如仅有部分检查项为警告，你可评估风险决定是否忽略警告。若所有警告均被忽略，迁移任务会自动进入下一步。

关于错误及解决方案，详见 [预检查错误及解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions)。

关于预检查项说明，详见 [Migration Task Precheck](https://docs.pingcap.com/tidb/stable/dm-precheck)。

如所有检查项均为 **Pass**，点击 **Next**。

## 第 6 步：选择规格并启动迁移

在 **Choose a Spec and Start Migration** 页面，根据性能需求选择合适的迁移规格。关于规格说明，详见 [数据迁移规格](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)。

选择规格后，点击 **Create Job and Start** 启动迁移。

## 第 7 步：查看迁移进度

迁移任务创建后，你可以在 **Migration Job Details** 页面查看迁移进度。迁移进度显示在 **Stage and Status** 区域。

你可以在任务运行时暂停或删除迁移任务。

如迁移任务失败，解决问题后可恢复任务。

你可以在任意状态下删除迁移任务。

如迁移过程中遇到问题，请参见 [迁移错误及解决方案](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions)。

## 调整迁移任务规格

TiDB Cloud 支持根据不同场景的性能和成本需求，动态扩缩迁移任务规格。

不同迁移规格对应不同性能。你在不同阶段可能有不同性能需求。例如，现有数据迁移阶段希望尽快完成，可选择较大规格（如 8 RCU）；现有数据迁移完成后，增量同步对性能要求不高，可将规格从 8 RCU 缩小到 2 RCU 以节省成本。

调整迁移任务规格时需注意：

- 规格调整大约需要 5~10 分钟。
- 如调整失败，任务规格会保持调整前状态。

### 限制

- 仅可在任务处于 **Running** 或 **Paused** 状态时调整规格。
- 现有数据导出阶段不支持调整迁移任务规格。
- 调整规格会重启任务。如任务的源表无主键，可能会插入重复数据。
- 调整期间请勿清理源数据库的 binary log，也不要临时增大 MySQL 源数据库的 `expire_logs_days`，否则任务可能因无法获取连续 binlog 位置而失败。

### 调整流程

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

2. 点击目标集群名称进入概览页，然后点击左侧导航栏的 **Data** > **Migration**。

3. 在 **Data Migration** 页面，找到要调整的迁移任务，在 **Action** 列点击 **...** > **Scale Up/Down**。

4. 在 **Scale Up/Down** 窗口选择新的规格，点击 **Submit**。你可以在窗口底部查看新规格的价格。