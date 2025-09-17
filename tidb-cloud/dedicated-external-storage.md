---
title: 为 TiDB Cloud Dedicated 集群配置外部存储访问
summary: 了解如何配置 Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS) 和 Azure Blob Storage 的访问权限。
aliases: ['/tidb-cloud/config-s3-and-gcs-access']
---

# 为 TiDB Cloud Dedicated 集群配置外部存储访问

如果你的源数据存储在 Amazon S3 存储桶、Azure Blob Storage 容器或 Google Cloud Storage (GCS) 存储桶中，在将数据导入或迁移到 TiDB Cloud 之前，你需要为存储桶配置跨账号访问权限。本文档介绍了如何为 TiDB Cloud Dedicated 集群进行相关配置。

如果你需要为 TiDB Cloud Serverless 集群配置这些外部存储，请参见 [为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md)。

## 配置 Amazon S3 访问权限

要允许 TiDB Cloud Dedicated 集群访问你 Amazon S3 存储桶中的源数据，可以通过以下任一方式为集群配置存储桶访问权限：

- [使用 Role ARN](#configure-amazon-s3-access-using-a-role-arn)（推荐）：使用 Role ARN 访问你的 Amazon S3 存储桶。
- [使用 AWS 访问密钥](#configure-amazon-s3-access-using-an-aws-access-key)：使用 IAM 用户的访问密钥访问你的 Amazon S3 存储桶。

### 使用 Role ARN 配置 Amazon S3 访问权限

按照以下步骤为 TiDB Cloud 配置存储桶访问权限并获取 Role ARN：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，获取目标 TiDB 集群对应的 TiDB Cloud 账号 ID 和 External ID。

    1. 进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

    3. 选择 **Import data from Cloud Storage**，然后点击 **Amazon S3**。

    4. 在 **Import Data from Amazon S3** 页面，点击 **Role ARN** 下方的链接。此时会弹出 **Add New Role ARN** 对话框。

    5. 展开 **Create Role ARN manually**，获取 TiDB Cloud Account ID 和 TiDB Cloud External ID。请记录这些 ID，后续会用到。

2. 在 AWS 管理控制台中，为你的 Amazon S3 存储桶创建托管策略。

    1. 登录 AWS 管理控制台，并打开 Amazon S3 控制台 [https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/)。
    2. 在 **Buckets** 列表中，选择包含源数据的存储桶名称，然后点击 **Copy ARN** 获取你的 S3 存储桶 ARN（例如，`arn:aws:s3:::tidb-cloud-source-data`）。请记录该存储桶 ARN，后续会用到。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. 打开 IAM 控制台 [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)，在左侧导航栏点击 **Policies**，然后点击 **Create Policy**。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4. 在 **Create policy** 页面，点击 **JSON** 标签页。
    5. 复制以下访问策略模板，并粘贴到策略文本框中。

        ````json
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

        在策略文本框中，将以下配置项替换为你自己的值。

        - `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`

            例如，如果你的源数据存储在 `tidb-cloud-source-data` 存储桶的根目录下，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`。如果你的源数据存储在存储桶的 `mydata` 目录下，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`。请确保目录末尾添加了 `/*`，以便 TiDB Cloud 能访问该目录下的所有文件。

        - `"Resource": "<Your S3 bucket ARN>"`

            例如，`"Resource": "arn:aws:s3:::tidb-cloud-source-data"`。

        - 如果你启用了 AWS Key Management Service 密钥（SSE-KMS）并使用客户自管密钥加密，请确保策略中包含以下配置。`"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` 是存储桶的一个示例 KMS 密钥。

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

            如果你的存储桶中的对象是从另一个加密存储桶复制过来的，KMS 密钥值需要包含两个存储桶的密钥。例如，`"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`。

    6. 点击 **Next**。
    7. 设置策略名称，添加策略标签（可选），然后点击 **Create policy**。

3. 在 AWS 管理控制台中，为 TiDB Cloud 创建访问角色并获取 role ARN。

    1. 在 IAM 控制台 [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)，点击左侧导航栏的 **Roles**，然后点击 **Create role**。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2. 创建角色时，填写以下信息：

        - 在 **Trusted entity type** 下选择 **AWS account**。
        - 在 **An AWS account** 下选择 **Another AWS account**，并将 TiDB Cloud account ID 粘贴到 **Account ID** 字段。
        - 在 **Options** 下，点击 **Require external ID** 以避免 [confused deputy problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)，然后将 TiDB Cloud External ID 粘贴到 **External ID** 字段。如果创建角色时未勾选 "Require external ID"，任何拥有你 S3 存储桶 URI 和 IAM role ARN 的人都可能访问你的 Amazon S3 存储桶。如果同时配置了 account ID 和 external ID，只有运行在同一项目和同一区域的 TiDB 集群才能访问该存储桶。

    3. 点击 **Next** 打开策略列表，选择你刚刚创建的策略，然后点击 **Next**。
    4. 在 **Role details** 下设置角色名称，然后点击右下角的 **Create role**。角色创建完成后，会显示角色列表。
    5. 在角色列表中，点击你刚刚创建的角色名称进入其详情页，然后复制 role ARN。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

4. 回到 TiDB Cloud 控制台，在你获取 TiDB Cloud account ID 和 external ID 的 **Data Import** 页面，将 role ARN 粘贴到 **Role ARN** 字段。

### 使用 AWS 访问密钥配置 Amazon S3 访问权限

推荐使用 IAM 用户（而非 AWS 账号 root 用户）来创建访问密钥。

按照以下步骤配置访问密钥：

1. 创建一个具有以下策略的 IAM 用户：

   - `AmazonS3ReadOnlyAccess`
   - [`CreateOwnAccessKeys`（必需）和 `ManageOwnAccessKeys`（可选）](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions)

   建议这些策略仅对存储源数据的存储桶生效。

   详细信息请参见 [创建 IAM 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)。

2. 使用你的 AWS 账号 ID 或账号别名，以及 IAM 用户名和密码登录 [IAM 控制台](https://console.aws.amazon.com/iam)。

3. 创建访问密钥。详细步骤请参见 [为 IAM 用户创建访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

> **Note:**
>
> TiDB Cloud 不会存储你的访问密钥。建议在导入完成后 [删除访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

## 配置 GCS 访问权限

要允许 TiDB Cloud 访问你 GCS 存储桶中的源数据，需要为存储桶配置 GCS 访问权限。项目中任意一个 TiDB 集群完成配置后，该项目下所有 TiDB 集群都可以访问该 GCS 存储桶。

1. 在 TiDB Cloud 控制台获取目标 TiDB 集群的 Google Cloud Service Account ID。

    1. 进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Import**。

    3. 选择 **Import data from Cloud Storage**，然后点击 **Google Cloud Storage**。

    4. 点击 **Show Google Cloud Server Account ID**，复制 Service Account ID 以备后用。

2. 在 Google Cloud 控制台中，为你的 GCS 存储桶创建 IAM 角色。

    1. 登录 [Google Cloud 控制台](https://console.cloud.google.com/)。
    2. 进入 [Roles](https://console.cloud.google.com/iam-admin/roles) 页面，然后点击 **CREATE ROLE**。

        ![Create a role](/media/tidb-cloud/gcp-create-role.png)

    3. 输入角色的名称、描述、ID 和角色发布阶段。角色名称创建后不可更改。
    4. 点击 **ADD PERMISSIONS**。
    5. 为角色添加以下只读权限，然后点击 **Add**。

        - storage.buckets.get
        - storage.objects.get
        - storage.objects.list

        你可以将权限名称复制到 **Enter property name or value** 字段作为过滤条件，并在过滤结果中选择名称。要添加这三个权限，可以在权限名称之间使用 **OR**。

        ![Add permissions](/media/tidb-cloud/gcp-add-permissions.png)

3. 进入 [Bucket](https://console.cloud.google.com/storage/browser) 页面，点击你希望 TiDB Cloud 访问的 GCS 存储桶名称。

4. 在 **Bucket details** 页面，点击 **PERMISSIONS** 标签页，然后点击 **GRANT ACCESS**。

    ![Grant Access to the bucket ](/media/tidb-cloud/gcp-bucket-permissions.png)

5. 填写以下信息以授予存储桶访问权限，然后点击 **SAVE**。

    - 在 **New Principals** 字段，粘贴目标 TiDB 集群的 Google Cloud Service Account ID。
    - 在 **Select a role** 下拉列表中，输入你刚刚创建的 IAM 角色名称，并在过滤结果中选择该名称。

    > **Note:**
    >
    > 如果需要移除 TiDB Cloud 的访问权限，只需移除你已授予的访问即可。

6. 在 **Bucket details** 页面，点击 **OBJECTS** 标签页。

    如果你想复制文件的 gsutil URI，选择该文件，点击 **Open object overflow menu**，然后点击 **Copy gsutil URI**。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri01.png)

    如果你想使用文件夹的 gsutil URI，打开该文件夹，然后点击文件夹名称后面的复制按钮复制文件夹名称。之后，你需要在名称前加上 `gs://`，末尾加上 `/`，以获得正确的文件夹 URI。

    例如，如果文件夹名称为 `tidb-cloud-source-data`，你需要使用 `gs://tidb-cloud-source-data/` 作为 URI。

    ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7. 回到 TiDB Cloud 控制台，在你获取 Google Cloud Service Account ID 的 **Data Import** 页面，将 GCS 存储桶的 gsutil URI 粘贴到 **Bucket gsutil URI** 字段。例如，粘贴 `gs://tidb-cloud-source-data/`。

## 配置 Azure Blob Storage 访问权限

要允许 TiDB Cloud Dedicated 集群访问你的 Azure Blob 容器，需要为容器配置 Azure Blob 访问权限。你可以使用账户 SAS token 配置容器访问：

1. 在 [Azure Storage account](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts) 页面，点击包含目标容器的存储账户。

2. 在存储账户的导航栏中，点击 **Security + networking** > **Shared access signature**。

    ![sas-position](/media/tidb-cloud/dedicated-external-storage/azure-sas-position.png)

3. 在 **Shared access signature** 页面，按如下方式创建具有必要权限的 [account SAS token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)：

    1. 在 **Allowed services** 下选择 **Blob**。
    2. 在 **Allowed resource types** 下选择 **Container** 和 **Object**。
    3. 在 **Allowed permissions** 下选择所需权限。例如，导入数据到 TiDB Cloud Dedicated 集群需要 **Read** 和 **List**。
    4. 根据需要调整 **Start and expiry date/time**。出于安全考虑，建议设置与数据导入时间线相符的过期时间。
    5. 其他设置保持默认值。

    ![sas-create](/media/tidb-cloud/dedicated-external-storage/azure-sas-create.png)

4. 点击 **Generate SAS and connection string** 生成 SAS token。

5. 复制生成的 **SAS Token**。在 TiDB Cloud 配置数据导入时需要用到该 token 字符串。

> **Note:**
>
> 在开始数据导入前，请测试连接和权限，确保 TiDB Cloud Dedicated 集群能够访问指定的 Azure Blob 容器及文件。