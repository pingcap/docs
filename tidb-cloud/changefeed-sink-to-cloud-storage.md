---
title: Sink to Cloud Storage
summary: 本文档介绍如何创建 changefeed，将数据从 TiDB Cloud 流式同步到 Amazon S3、Google Cloud Storage (GCS) 或 Azure Blob Storage。内容包括限制、目标端配置、同步及规范配置，以及启动同步流程。
---

# Sink to Cloud Storage

本文档描述如何创建 changefeed，将数据从 TiDB Cloud 流式同步到云存储。目前支持 Amazon S3、Google Cloud Storage (GCS) 和 Azure Blob Storage。

> **注意：**
>
> - 若要将数据流式同步到云存储，请确保你的 TiDB 集群版本为 v7.1.1 或更高。如需将 TiDB Cloud Dedicated 集群升级到 v7.1.1 或更高版本，请[联系 TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。
> - 对于 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 和 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群，changefeed 功能不可用。

## 限制

- 每个 TiDB Cloud 集群最多可创建 100 个 changefeed。
- 由于 TiDB Cloud 使用 TiCDC 建立 changefeed，因此具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果待同步的表没有主键或非空唯一索引，则在同步过程中由于缺乏唯一约束，在某些重试场景下可能会导致下游插入重复数据。

## 步骤 1. 配置目标端

进入目标 TiDB 集群的集群总览页面。在左侧导航栏点击 **Data** > **Changefeed**，点击 **Create Changefeed**，并选择 **Amazon S3**、**GCS** 或 **Azure Blob Storage** 作为目标端。具体配置流程根据所选目标端不同而有所区别。

<SimpleTab>
<div label="Amazon S3">

对于 **Amazon S3**，填写 **S3 Endpoint** 区域：`S3 URI`、`Access Key ID` 和 `Secret Access Key`。请确保 S3 bucket 与 TiDB 集群处于同一区域。

![s3_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-s3-endpoint.jpg)

</div>
<div label="GCS">

对于 **GCS**，在填写 **GCS Endpoint** 之前，需要先授予 GCS bucket 访问权限。请按照以下步骤操作：

1. 在 TiDB Cloud 控制台，记录下 **Service Account ID**，该 ID 用于授予 TiDB Cloud 访问你的 GCS bucket 的权限。

    ![gcs_endpoint](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-endpoint.png)

2. 在 Google Cloud 控制台，为你的 GCS bucket 创建一个 IAM 角色。

    1. 登录 [Google Cloud 控制台](https://console.cloud.google.com/)。
    2. 进入 [Roles](https://console.cloud.google.com/iam-admin/roles) 页面，然后点击 **Create role**。

        ![Create a role](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-create-role.png)

    3. 输入角色的名称、描述、ID 及角色发布阶段。角色名称创建后不可更改。
    4. 点击 **Add permissions**，为该角色添加以下权限，然后点击 **Add**。

        - storage.buckets.get
        - storage.objects.create
        - storage.objects.delete
        - storage.objects.get
        - storage.objects.list
        - storage.objects.update

    ![Add permissions](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-assign-permission.png)

3. 进入 [Bucket](https://console.cloud.google.com/storage/browser) 页面，选择你希望 TiDB Cloud 访问的 GCS bucket。请注意，GCS bucket 必须与 TiDB 集群处于同一区域。

4. 在 **Bucket details** 页面，点击 **Permissions** 标签页，然后点击 **Grant access**。

    ![Grant Access to the bucket ](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-grant-access-1.png)

5. 填写以下信息以授予 bucket 访问权限，然后点击 **Save**。

    - 在 **New Principals** 字段中，粘贴之前记录的目标 TiDB 集群的 **Service Account ID**。
    - 在 **Select a role** 下拉列表中，输入刚刚创建的 IAM 角色名称，并从筛选结果中选择该名称。

    > **注意：**
    >
    > 若需移除 TiDB Cloud 的访问权限，只需移除你已授予的访问权限即可。

6. 在 **Bucket details** 页面，点击 **Objects** 标签页。

    - 获取 bucket 的 gsutil URI：点击复制按钮，并在前面加上 `gs://` 前缀。例如，若 bucket 名为 `test-sink-gcs`，则 URI 为 `gs://test-sink-gcs/`。

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri01.png)

    - 获取文件夹的 gsutil URI：进入文件夹，点击复制按钮，并在前面加上 `gs://` 前缀。例如，若 bucket 名为 `test-sink-gcs`，文件夹名为 `changefeed-xxx`，则 URI 为 `gs://test-sink-gcs/changefeed-xxx/`。

        ![Get bucket URI](/media/tidb-cloud/changefeed/sink-to-cloud-storage-gcs-uri02.png)

7. 回到 TiDB Cloud 控制台，在 Changefeed 的 **Configure Destination** 页面，填写 **bucket gsutil URI** 字段。

</div>
<div label="Azure Blob Storage">

对于 **Azure Blob Storage**，你需要先在 Azure 门户配置容器并获取 SAS token。请按照以下步骤操作：

1. 在 [Azure 门户](https://portal.azure.com/) 创建一个用于存储 changefeed 数据的容器。

    1. 在左侧导航栏点击 **Storage Accounts**，然后选择你的存储账户。
    2. 在存储账户导航菜单中，选择 **Data storage** > **Containers**，然后点击 **+ Container**。
    3. 输入新容器的名称，设置匿名访问级别（推荐级别为 **Private**），然后点击 **Create**。

2. 获取目标容器的 URL。

    1. 在容器列表中，选择你的目标容器。
    2. 点击容器的 **...**，然后选择 **Container properties**。
    3. 保存 **URL** 值以备后用，例如 `https://<storage_account>.blob.core.windows.net/<container>`。

3. 生成 SAS token。

    1. 在存储账户导航菜单中，选择 **Security + networking** > **Shared access signature**。
    2. 在 **Allowed services** 区域，选择 **Blob**。
    3. 在 **Allowed resource types** 区域，选择 **Container** 和 **Object**。
    4. 在 **Allowed permissions** 区域，选择 **Read**、**Write**、**Delete**、**List** 和 **Create**。
    5. 为 SAS token 指定一个足够长的有效期，以满足你的需求。

        > **注意：**
        >
        > - changefeed 会持续写入事件，因此请确保 SAS token 的有效期足够长。出于安全考虑，建议每 6 到 12 个月更换一次 token。
        > - 生成的 SAS token 无法回收，因此请谨慎设置其有效期。
        > - 为保证持续可用性，请在 SAS token 过期前重新生成并更新 token。

    6. 点击 **Generate SAS and connection string**，然后保存 **SAS token**。

        ![Generate a SAS token](/media/tidb-cloud/changefeed/sink-to-cloud-storage-azure-signature.png)

4. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 的 Changefeed **Configure Destination** 页面，填写以下字段：

    - **Blob URL**：输入第 2 步获取的容器 URL，可选添加前缀。
    - **SAS Token**：输入第 3 步获取的 SAS token。

</div>
</SimpleTab>

点击 **Next**，建立 TiDB Cloud Dedicated 集群与 Amazon S3、GCS 或 Azure Blob Storage 的连接。TiDB Cloud 会自动测试并验证连接是否成功。

- 若连接成功，将进入下一步配置。
- 若连接失败，会显示连接错误，你需要处理该错误。错误解决后，点击 **Next** 重新尝试连接。

## 步骤 2. 配置同步

1. 自定义 **Table Filter**，筛选你希望同步的表。规则语法详见 [table filter rules](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters)。

    ![the table filter of changefeed](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    - **Case Sensitive**：你可以设置过滤规则中数据库和表名的匹配是否大小写敏感。默认情况下，匹配为大小写不敏感。
    - **Filter Rules**：你可以在此列设置过滤规则。默认有一条规则 `*.*`，表示同步所有表。添加新规则后，TiDB Cloud 会查询 TiDB 中所有表，并仅在右侧框中显示匹配规则的表。最多可添加 100 条过滤规则。
    - **Tables with valid keys**：此列显示具有有效键（包括主键或唯一索引）的表。
    - **Tables without valid keys**：此列显示缺少主键或唯一键的表。这些表在同步时存在挑战，因为缺乏唯一标识符，在处理下游重复事件时可能导致数据不一致。为保证数据一致性，建议在启动同步前为这些表添加唯一键或主键，或通过过滤规则排除这些表。例如，可通过规则 `"!test.tbl1"` 排除表 `test.tbl1`。

2. 自定义 **Event Filter**，筛选你希望同步的事件。

    - **Tables matching**：你可以在此列设置事件过滤器将应用于哪些表。规则语法与前述 **Table Filter** 区域相同。每个 changefeed 最多可添加 10 条事件过滤规则。
    - **Event Filter**：你可以使用以下事件过滤器，从 changefeed 中排除特定事件：
        - **Ignore event**：排除指定类型的事件。
        - **Ignore SQL**：排除匹配指定表达式的 DDL 事件。例如，`^drop` 排除以 `DROP` 开头的语句，`add column` 排除包含 `ADD COLUMN` 的语句。
        - **Ignore insert value expression**：排除满足特定条件的 `INSERT` 语句。例如，`id >= 100` 排除 `id` 大于等于 100 的 `INSERT` 语句。
        - **Ignore update new value expression**：排除新值满足指定条件的 `UPDATE` 语句。例如，`gender = 'male'` 排除将 `gender` 修改为 `male` 的更新。
        - **Ignore update old value expression**：排除旧值满足指定条件的 `UPDATE` 语句。例如，`age < 18` 排除旧值 `age` 小于 18 的更新。
        - **Ignore delete value expression**：排除满足指定条件的 `DELETE` 语句。例如，`name = 'john'` 排除 `name` 为 `'john'` 的删除。

3. 在 **Start Replication Position** 区域，选择以下同步起始位置之一：

    - 从现在开始同步
    - 从指定的 [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso) 开始同步
    - 从指定时间点开始同步

4. 在 **Data Format** 区域，选择 **CSV** 或 **Canal-JSON** 格式。

    <SimpleTab>
    <div label="Configure CSV format">

    配置 **CSV** 格式时，填写以下字段：

    - **Binary Encode Method**：二进制数据的编码方法。可选择 **base64**（默认）或 **hex**。如需与 AWS DMS 集成，请选择 **hex**。
    - **Date Separator**：按年、月、日轮转数据，或选择不轮转。
    - **Delimiter**：指定 CSV 文件中用于分隔值的字符。逗号（`,`）是最常用的分隔符。
    - **Quote**：指定用于包裹包含分隔符或特殊字符的值的字符。通常使用双引号（`"`）作为引用字符。
    - **Null/Empty Values**：指定在 CSV 文件中如何表示空值或空字符串。这对于正确处理和解析数据非常重要。
    - **Include Commit Ts**：控制是否在 CSV 行中包含 [`commit-ts`](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#replicate-change-data-to-storage-services)。

    </div>
    <div label="Configure Canal-JSON format">

    Canal-JSON 是一种纯 JSON 文本格式。配置时填写以下字段：

    - **Date Separator**：按年、月、日轮转数据，或选择不轮转。
    - **Enable TiDB Extension**：启用后，TiCDC 会发送 [WATERMARK 事件](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#watermark-event) 并在 Canal-JSON 消息中添加 [TiDB 扩展字段](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field)。

    </div>
    </SimpleTab>

5. 在 **Flush Parameters** 区域，你可以配置以下两项：

    - **Flush Interval**：默认 60 秒，可在 2 秒至 10 分钟范围内调整；
    - **File Size**：默认 64 MB，可在 1 MB 至 512 MB 范围内调整。

    ![Flush Parameters](/media/tidb-cloud/changefeed/sink-to-cloud-storage-flush-parameters.jpg)

    > **注意：**
    >
    > 这两个参数会影响每个数据库表在云存储中生成的对象数量。如果表数量较多，使用相同配置会增加生成对象的数量，并提升调用云存储 API 的成本。因此，建议根据你的恢复点目标（RPO）和成本需求合理配置这些参数。

6. 在 **Split Event** 区域，选择是否将 `UPDATE` 事件切分为单独的 `DELETE` 和 `INSERT` 事件，或保持为原始 `UPDATE` 事件。详细信息参见 [Split primary or unique key UPDATE events for non-MySQL sinks](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)。

## 步骤 3. 配置规范

点击 **Next**，配置 changefeed 规范。

1. 在 **Changefeed Specification** 区域，指定 changefeed 使用的 Replication Capacity Units (RCUs) 数量。
2. 在 **Changefeed Name** 区域，指定 changefeed 的名称。

## 步骤 4. 审核配置并启动同步

点击 **Next**，审核 changefeed 配置。

- 如果你已确认所有配置无误，点击 **Create** 以创建 changefeed。
- 如果需要修改配置，点击 **Previous** 返回并进行相应更改。

sink 很快会启动，你会看到 sink 状态从 **Creating** 变为 **Running**。

点击 changefeed 名称可进入详情页面。在该页面，你可以查看更多关于 changefeed 的信息，包括 checkpoint 状态、同步延时及其他相关统计/指标（信息）。