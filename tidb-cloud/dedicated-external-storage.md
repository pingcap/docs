---
title: 配置 TiDB Cloud Dedicated 的外部存储访问
summary: 了解如何配置 Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS) 和 Azure Blob Storage 的访问权限。
aliases: ['/tidb-cloud/config-s3-and-gcs-access']
---

# 配置 TiDB Cloud Dedicated 的外部存储访问

如果你的源数据存储在 Amazon S3 桶、Azure Blob 存储容器或 Google Cloud Storage (GCS) 桶中，在导入或迁移数据到 TiDB Cloud 之前，你需要配置跨账户访问这些桶。本文档描述了如何为 TiDB Cloud Dedicated 集群进行配置。

如果你需要为 TiDB Cloud Serverless 集群配置这些外部存储，请参见 [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md)。

## 配置 Amazon S3 访问

为了让 TiDB Cloud Dedicated 集群访问你的 Amazon S3 桶中的源数据，可以通过以下任意方法配置桶访问权限：

- [使用 Role ARN](#configure-amazon-s3-access-using-a-role-arn)（推荐）：使用 Role ARN 访问你的 Amazon S3 桶。
- [使用 AWS 访问密钥](#configure-amazon-s3-access-using-an-aws-access-key)：使用 IAM 用户的访问密钥访问你的 Amazon S3 桶。

### 使用 Role ARN 配置 Amazon S3 访问

按照以下步骤配置 TiDB Cloud 的桶访问权限并获取 Role ARN：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，获取目标 TiDB 集群的对应 TiDB Cloud 账户 ID 和外部 ID。

    1. 进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称，进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

    3. 选择 **Import data from Cloud Storage**，然后点击 **Amazon S3**。

    4. 在 **Import Data from Amazon S3** 页面，点击 **Role ARN** 下的链接。将显示 **Add New Role ARN** 对话框。

    5. 展开 **Create Role ARN manually**，获取 TiDB Cloud 账户 ID 和 TiDB Cloud 外部 ID。记下这些 ID 以备后续使用。

2. 在 AWS 管理控制台中，为你的 Amazon S3 桶创建托管策略。

    1. 登录 AWS 管理控制台，打开 [Amazon S3 控制台](https://console.aws.amazon.com/s3/)。
    2. 在 **Buckets** 列表中，选择你的源数据桶的名称，然后点击 **Copy ARN** 获取你的 S3 桶 ARN（例如，`arn:aws:s3:::tidb-cloud-source-data`）。记下桶 ARN 以备后续使用。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. 打开 [IAM 控制台](https://console.aws.amazon.com/iam/)，点击左侧导航栏的 **Policies**，然后点击 **Create Policy**。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4. 在 **Create policy** 页面，点击 **JSON** 标签页。
    5. 复制以下访问策略模板，粘贴到策略文本框中。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion"
                    ],
                    "Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket"
                    ],
                    "Resource": "<Your S3 bucket ARN>"
                }
            ]
        }
        ```

        在策略文本框中，根据实际情况更新以下配置。

        - `"Resource": "<Your S3 bucket ARN>/<Directory of your source data>/*"`

            例如，如果你的源数据存储在 `tidb-cloud-source-data` 桶的根目录，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`。如果存储在 `mydata` 目录下，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`。确保在目录后添加 `/*`，以便 TiDB Cloud 可以访问该目录下的所有文件。

        - `"Resource": "<Your S3 bucket ARN>"`

            例如，`"Resource": "arn:aws:s3:::tidb-cloud-source-data"`。

        - 如果启用了 AWS KMS 密钥（SSE-KMS）客户管理密钥加密，确保策略中包含以下配置。`"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` 是桶的示例 KMS 密钥。

            ```json
            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }
            ```

            如果桶中的对象是从另一个加密桶复制而来，KMS 密钥值需要包含两个桶的密钥。例如，`"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`。

    6. 点击 **Next**。
    7. 设置策略名称，添加标签（可选），然后点击 **Create policy**。

3. 在 AWS 管理控制台中，为 TiDB Cloud 创建访问角色并获取角色 ARN。

    1. 在 [IAM 控制台](https://console.aws.amazon.com/iam/) 中，点击左侧导航栏的 **Roles**，然后点击 **Create role**。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2. 填写以下信息以创建角色：

        - 在 **Trusted entity type** 下选择 **AWS account**。
        - 在 **An AWS account** 下选择 **Another AWS account**，并在 **Account ID** 字段中粘贴 TiDB Cloud 账户 ID。
        - 在 **Options** 中，点击 **Require external ID**，以避免 [confused deputy problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)，然后在 **External ID** 字段中粘贴 TiDB Cloud 外部 ID。如果没有勾选 **Require external ID**，任何拥有你的 S3 桶 URI 和 IAM 角色 ARN 的人都可能访问你的 Amazon S3 桶。如果同时设置了账户 ID 和外部 ID，只有在相同项目和区域内运行的 TiDB 集群才能访问该桶。

    3. 点击 **Next**，选择刚刚创建的策略，然后点击 **Next**。
    4. 在 **Role details** 中，为角色命名，然后点击右下角的 **Create role**。角色创建完成后，角色列表会显示出来。
    5. 在角色列表中，点击刚刚创建的角色名称，进入其概要页面，然后复制角色 ARN。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4. 在 TiDB Cloud 控制台中，进入 **Data Import** 页面，获取 TiDB Cloud 账户 ID 和外部 ID，然后将角色 ARN 粘贴到 **Role ARN** 字段。

### 使用 AWS 访问密钥配置 Amazon S3 访问

建议你使用 IAM 用户（而非 AWS 账户根用户）创建访问密钥。

按照以下步骤配置访问密钥：

1. 创建一个具有以下策略的 IAM 用户：

   - `AmazonS3ReadOnlyAccess`
   - [`CreateOwnAccessKeys`（必需）和 `ManageOwnAccessKeys`（可选）](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions)

   建议这些策略仅对存储源数据的桶生效。

   更多信息请参见 [创建 IAM 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)。

2. 使用你的 AWS 账户 ID 或别名，以及 IAM 用户名和密码登录 [IAM 控制台](https://console.aws.amazon.com/iam)。

3. 创建访问密钥。详细步骤请参见 [为 IAM 用户创建访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

> **注意：**
>
> TiDB Cloud 不会存储你的访问密钥。建议在导入完成后，删除该访问密钥 [删除访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

## 配置 GCS 访问

为了让 TiDB Cloud 访问你的 GCS 桶中的源数据，你需要为该桶配置 GCS 访问权限。一旦为某个项目中的一个 TiDB 集群完成配置，项目中的所有 TiDB 集群都可以访问该 GCS 桶。

1. 在 TiDB Cloud 控制台，获取目标 TiDB 集群的 Google Cloud Service Account ID。

    1. 进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称，进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

    3. 选择 **Import data from Cloud Storage**，然后点击 **Google Cloud Storage**。

    4. 点击 **Show Google Cloud Server Account ID**，复制 Service Account ID 以备后续使用。

2. 在 Google Cloud 控制台中，为你的 GCS 桶创建 IAM 角色。

    1. 登录 [Google Cloud 控制台](https://console.cloud.google.com/)。
    2. 进入 [Roles](https://console.cloud.google.com/iam-admin/roles) 页面，点击 **CREATE ROLE**。

        ![Create a role](/media/tidb-cloud/gcp-create-role.png)

    3. 输入角色的名称、描述、ID 和启动阶段。角色创建后，角色名称不可更改。
    4. 点击 **ADD PERMISSIONS**。
    5. 添加以下只读权限，然后点击 **Add**。

        - storage.buckets.get
        - storage.objects.get
        - storage.objects.list

        你可以将权限名称复制到 **Enter property name or value** 字段作为过滤条件，选择过滤结果中的名称。添加三个权限时，可以用 **OR** 连接权限名称。

        ![Add permissions](/media/tidb-cloud/gcp-add-permissions.png)

3. 进入 [Bucket](https://console.cloud.google.com/storage/browser) 页面，点击你想让 TiDB Cloud 访问的 GCS 桶名称。

4. 在 **Bucket details** 页面，点击 **PERMISSIONS** 标签，然后点击 **GRANT ACCESS**。

    ![Grant Access to the bucket ](/media/tidb-cloud/gcp-bucket-permissions.png)

5. 填写以下信息以授予访问权限，然后点击 **SAVE**。

    - 在 **New Principals** 字段中，粘贴目标 TiDB 集群的 Google Cloud Service Account ID。
    - 在 **Select a role** 下拉列表中，输入你刚创建的 IAM 角色名称，然后从过滤结果中选择。

    > **注意：**
    >
    > 若要撤销对 TiDB Cloud 的访问，只需删除你已授予的权限即可。

6. 在 **Bucket details** 页面，点击 **OBJECTS** 标签。

    如果你想复制文件的 gsutil URI，选择文件后，点击 **Open object overflow menu**，然后点击 **Copy gsutil URI**。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri01.png)

    如果你想使用文件夹的 gsutil URI，打开文件夹后，点击文件夹名称后面的复制按钮，复制文件夹名称。之后在名称前加 `gs://`，末尾加 `/`，即可得到正确的文件夹 URI。

    例如，文件夹名称为 `tidb-cloud-source-data`，应使用 `gs://tidb-cloud-source-data/` 作为 URI。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7. 在 TiDB Cloud 控制台，进入 **Data Import** 页面，将获取到的 Google Cloud Service Account ID 和 GCS 桶的 gsutil URI 粘贴到对应字段。例如，粘贴 `gs://tidb-cloud-source-data/`。

## 配置 Azure Blob 存储访问

为了让 TiDB Cloud Dedicated 访问你的 Azure Blob 容器，你需要为容器配置 Azure Blob 访问权限。可以使用账户 SAS 令牌配置容器访问：

1. 在 [Azure Storage 账户](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts) 页面，点击你的存储账户。

2. 在存储账户的导航窗格中，点击 **Security + networking** > **Shared access signature**。

    ![sas-position](/media/tidb-cloud/dedicated-external-storage/azure-sas-position.png)

3. 在 **Shared access signature** 页面，创建具有必要权限的 [账户 SAS 令牌](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)，步骤如下：

    1. 在 **Allowed services** 下选择 **Blob**。
    2. 在 **Allowed resource types** 下选择 **Container** 和 **Object**。
    3. 在 **Allowed permissions** 下选择所需权限。例如，导入数据到 TiDB Cloud Dedicated 需要 **Read** 和 **List**。
    4. 根据需要调整 **Start and expiry date/time**。出于安全考虑，建议设置与数据导入时间线一致的到期日期。
    5. 保持其他设置的默认值。

    ![sas-create](/media/tidb-cloud/dedicated-external-storage/azure-sas-create.png)

4. 点击 **Generate SAS and connection string** 生成 SAS 令牌。

5. 复制生成的 **SAS Token**，在配置 TiDB Cloud 数据导入时需要用到。

> **注意：**
>
> 在开始数据导入之前，建议测试连接和权限，确保 TiDB Cloud Dedicated 能访问指定的 Azure Blob 容器和文件。
