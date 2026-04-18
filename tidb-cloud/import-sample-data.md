---
title: 从云存储导入示例数据（SQL 文件）到 TiDB Cloud Dedicated
summary: 了解如何通过 UI 将示例数据导入到 TiDB Cloud Dedicated。
---

# 从云存储导入示例数据（SQL 文件）到 TiDB Cloud Dedicated

本文档介绍如何通过 UI 将示例数据（SQL 文件）导入到 TiDB Cloud Dedicated。所用的示例数据为 Capital Bikeshare 的系统数据，根据 Capital Bikeshare 数据许可协议发布。在导入示例数据之前，你需要拥有一个 TiDB 集群。

<SimpleTab>
<div label="Amazon S3">

1. 打开目标 TiDB Cloud Dedicated 集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，并进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，提供以下信息：

    - **Storage Provider**：选择 **Amazon S3**。
    - **Source URI**：输入示例数据的 URI `s3://tidbcloud-sample-data/data-ingestion/`。
    - **Credentials**：选择 **AWS Role ARN**，然后输入 `arn:aws:iam::801626783489:role/import-sample-access`。
        - **AWS Access Key**：对于示例数据跳过此项。

4. 点击 **Next**。

5. 在 **Destination Mapping** 部分，保持选中 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping**，然后选择 **SQL** 作为数据格式。

6. 点击 **Next**。TiDB Cloud 会扫描源文件。

7. 查看扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示为 **Completed** 时，检查已导入的表。

</div>
<div label="Google Cloud">

1. 打开目标 TiDB Cloud Dedicated 集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，并进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，提供以下信息：

    - **Storage Provider**：选择 **Google Cloud Storage**。
    - **Source URI**：输入示例数据的 URI `gs://tidbcloud-samples-us-west1/`。
    - **Google Cloud Service Account ID**：TiDB Cloud 会在此页面显示一个 Google Cloud Service Account ID。使用示例数据 URI 时，你可以直接继续。

4. 点击 **Next**。

5. 在 **Destination Mapping** 部分，保持选中 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping**，然后选择 **SQL** 作为数据格式。

6. 点击 **Next**。TiDB Cloud 会扫描源文件。

7. 查看扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示为 **Completed** 时，检查已导入的表。

</div>

<div label="Azure Blob Storage">

1. 打开目标 TiDB Cloud Dedicated 集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，并进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 点击 **Import data from Cloud Storage**。

3. 在 **Import Data from Cloud Storage** 页面，提供以下信息：

    - **Storage Provider**：选择 **Azure Blob Storage**。
    - **Source URI**：输入示例数据的 URI `https://tcidmsampledata.blob.core.windows.net/sql/`。
    - **Connectivity Method**：选择 TiDB Cloud 连接到 Azure Blob Storage 的方式。导入示例数据时，可以使用默认连接方式。

        - **Public**（默认）：通过公共互联网连接。当存储账户允许公共网络访问时，使用此选项。
        - **Private Link**：通过 Azure 私有端点连接，以实现网络隔离访问。当存储账户阻止公共访问，或者你的安全策略要求使用私有连接时，使用此选项。如果选择 **Private Link**，你还需要填写额外字段 **Azure Blob Storage Resource ID**。要查找资源 ID，请执行以下操作：

            1. 前往 [Azure 门户](https://portal.azure.com/)。
            2. 导航到你的存储账户，然后点击 **Overview** > **JSON View**。
            3. 复制 `id` 属性的值。资源 ID 的格式为 `/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<account_name>`。

    - **SAS Token**：

        - 对于示例数据，使用以下 **SAS Token**：`sv=2015-04-05&ss=b&srt=co&sp=rl&se=2099-03-01T00%3A00%3A01.0000000Z&sig=cQHvaofmVsUJEbgyf4JFkAwTJGsFOmbQHx03GvVMrNc%3D`。
        - 对于你自己的数据，可以使用 SAS token 访问你的 Azure Blob Storage。更多信息，参见 [Configure Azure Blob Storage access](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

4. 点击 **Next**。

    如果你选择 **Private Link** 作为连接方式，TiDB Cloud 会为你的存储账户创建一个私有端点。你需要先在 Azure 门户中批准此端点请求，连接才能继续：

    1. 前往 [Azure 门户](https://portal.azure.com/)，并导航到你的存储账户。
    2. 点击 **Networking** > **Private endpoint connections**。
    3. 找到来自 TiDB Cloud 的待处理连接请求，然后点击 **Approve**。
    4. 返回 [TiDB Cloud 控制台](https://tidbcloud.com/)。端点获批后，导入向导会自动继续。

    > **Note:**
    >
    > 如果端点尚未获批，TiDB Cloud 会显示一条消息，指示连接正在等待批准。请在 [Azure 门户](https://portal.azure.com/) 中批准该请求，然后重试。

5. 在 **Destination Mapping** 部分，保持选中 **Use [TiDB file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping**，然后选择 **SQL** 作为数据格式。

6. 点击 **Next**。TiDB Cloud 会扫描源文件。

7. 查看扫描结果，检查找到的数据文件及其对应的目标表，然后点击 **Start Import**。

8. 当导入进度显示为 **Completed** 时，检查已导入的表。

</div>
</SimpleTab>

当数据导入进度显示为 **Completed** 时，说明你已成功将示例数据和数据库 schema 导入到 TiDB Cloud 的数据库中。

连接到集群后，你可以在终端中运行一些查询来检查结果，例如：

1. 获取起点为 "12th & U St NW" 的行程记录：

    ```sql
    use bikeshare;
    ```

    ```sql
    select * from `trips` where start_station_name='12th & U St NW' limit 10;
    ```

    ```sql
    +-----------------+---------------+---------------------+---------------------+--------------------+------------------+-------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    | ride_id         | rideable_type | started_at          | ended_at            | start_station_name | start_station_id | end_station_name                          | end_station_id | start_lat | start_lng  | end_lat   | end_lng    | member_casual |
    +-----------------+---------------+---------------------+---------------------+--------------------+------------------+-------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    | E291FF5018      | classic_bike  | 2021-01-02 11:12:38 | 2021-01-02 11:23:47 | 12th & U St NW     |            31268 | 7th & F St NW / National Portrait Gallery |          31232 | 38.916786 |  -77.02814 |  38.89728 | -77.022194 | member        |
    | E76F3605D0      | docked_bike   | 2020-09-13 00:44:11 | 2020-09-13 00:59:38 | 12th & U St NW     |            31268 | 17th St & Massachusetts Ave NW            |          31267 | 38.916786 |  -77.02814 | 38.908142 |  -77.03836 | casual        |
    | FFF0B75414      | docked_bike   | 2020-09-28 16:47:53 | 2020-09-28 16:57:30 | 12th & U St NW     |            31268 | 17th St & Massachusetts Ave NW            |          31267 | 38.916786 |  -77.02814 | 38.908142 |  -77.03836 | casual        |
    | C3F2C16949      | docked_bike   | 2020-09-13 00:42:03 | 2020-09-13 00:59:43 | 12th & U St NW     |            31268 | 17th St & Massachusetts Ave NW            |          31267 | 38.916786 |  -77.02814 | 38.908142 |  -77.03836 | casual        |
    | 1C7EC91629      | docked_bike   | 2020-09-28 16:47:49 | 2020-09-28 16:57:26 | 12th & U St NW     |            31268 | 17th St & Massachusetts Ave NW            |          31267 | 38.916786 |  -77.02814 | 38.908142 |  -77.03836 | member        |
    | A3A38BCACA      | classic_bike  | 2021-01-14 09:52:53 | 2021-01-14 10:00:51 | 12th & U St NW     |            31268 | 10th & E St NW                            |          31256 | 38.916786 |  -77.02814 | 38.895912 |  -77.02606 | member        |
    | EC4943257E      | electric_bike | 2021-01-28 10:06:52 | 2021-01-28 10:16:28 | 12th & U St NW     |            31268 | 10th & E St NW                            |          31256 | 38.916843 | -77.028206 |  38.89607 |  -77.02608 | member        |
    | D4070FBFA7      | classic_bike  | 2021-01-12 09:50:51 | 2021-01-12 09:59:41 | 12th & U St NW     |            31268 | 10th & E St NW                            |          31256 | 38.916786 |  -77.02814 | 38.895912 |  -77.02606 | member        |
    | 6EABEF3CAB      | classic_bike  | 2021-01-09 15:00:43 | 2021-01-09 15:18:30 | 12th & U St NW     |            31268 | 1st & M St NE                             |          31603 | 38.916786 |  -77.02814 | 38.905697 | -77.005486 | member        |
    | 2F5CC89018      | electric_bike | 2021-01-02 01:47:07 | 2021-01-02 01:58:29 | 12th & U St NW     |            31268 | 3rd & H St NE                             |          31616 | 38.916836 |  -77.02815 |  38.90074 |  -77.00219 | member        |
    +-----------------+---------------+---------------------+---------------------+--------------------+------------------+-------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    ```

2. 获取使用电动自行车的行程记录：

    ```sql
    use bikeshare;
    ```

    ```sql
    select * from `trips` where rideable_type="electric_bike" limit 10;
    ```

    ```sql
    +------------------+---------------+---------------------+---------------------+----------------------------------------+------------------+-------------------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    | ride_id          | rideable_type | started_at          | ended_at            | start_station_name                     | start_station_id | end_station_name                                      | end_station_id | start_lat | start_lng  | end_lat   | end_lng    | member_casual |
    +------------------+---------------+---------------------+---------------------+----------------------------------------+------------------+-------------------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    | AF15B12839DA4367 | electric_bike | 2021-01-23 14:50:46 | 2021-01-23 14:59:55 | Columbus Circle / Union Station        |            31623 | 15th & East Capitol St NE                             |          31630 |   38.8974 |  -77.00481 | 38.890    | 76.98354   | member        |
    | 7173E217338C4752 | electric_bike | 2021-01-15 08:28:38 | 2021-01-15 08:33:49 | 37th & O St NW / Georgetown University |            31236 | 34th St & Wisconsin Ave NW                            |          31226 | 38.907825 | -77.071655 | 38.916    | -77.0683   | member        |
    | E665505ED621D1AB | electric_bike | 2021-01-05 13:25:47 | 2021-01-05 13:35:58 | N Lynn St & Fairfax Dr                 |            31917 | 34th St & Wisconsin Ave NW                            |          31226 |  38.89359 |  -77.07089 | 38.916    | 77.06829   | member        |
    | 646AFE266A6375AF | electric_bike | 2021-01-16 00:08:10 | 2021-01-16 00:35:58 | 7th St & Massachusetts Ave NE          |            31647 | 34th St & Wisconsin Ave NW                            |          31226 | 38.892235 | -76.996025 |  38.91    | 7.068245   | member        |
    | 40CDDA0378E45736 | electric_bike | 2021-01-03 11:14:50 | 2021-01-03 11:26:04 | N Lynn St & Fairfax Dr                 |            31917 | 34th St & Wisconsin Ave NW                            |          31226 | 38.893734 |  -77.07096 | 38.916    | 7.068275   | member        |
    | E0A7DDB0CE680C01 | electric_bike | 2021-01-05 18:18:17 | 2021-01-05 19:04:11 | Maine Ave & 7th St SW                  |            31609 | Smithsonian-National Mall / Jefferson Dr & 12th St SW |          31248 | 38.878727 |  -77.02304 |   38.8    | 7.028755   | casual        |
    | 71BDF35029AF0039 | electric_bike | 2021-01-07 10:23:57 | 2021-01-07 10:59:43 | 10th & K St NW                         |            31263 | East West Hwy & Blair Mill Rd                         |          32019 |  38.90279 |  -77.02633 | 38.990    | 77.02937   | member        |
    | D5EACDF488260A61 | electric_bike | 2021-01-13 20:57:23 | 2021-01-13 21:04:19 | 8th & H St NE                          |            31661 | 15th & East Capitol St NE                             |          31630 |  38.89985 | -76.994835 |  38.88    | 76.98345   | member        |
    | 211D449363FB7EE3 | electric_bike | 2021-01-15 17:22:02 | 2021-01-15 17:35:49 | 7th & K St NW                          |            31653 | 15th & East Capitol St NE                             |          31630 |  38.90216 |   -77.0211 |  38.88    | 76.98357   | casual        |
    | CE667578A7291701 | electric_bike | 2021-01-15 16:55:12 | 2021-01-15 17:38:26 | East West Hwy & 16th St                |            32056 | East West Hwy & Blair Mill Rd                         |          32019 | 38.995674 |  -77.03868 | 38.990    | 77.02953   | casual        |
    +------------------+---------------+---------------------+---------------------+----------------------------------------+------------------+-------------------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    ```
