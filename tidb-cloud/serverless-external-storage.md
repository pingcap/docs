---
title: 配置 TiDB Cloud Serverless 外部存储访问
summary: 了解如何配置 Amazon Simple Storage Service (Amazon S3) 访问权限。
---

# 为 TiDB Cloud Serverless 配置外部存储访问

如果你希望在 TiDB Cloud Serverless 集群中从外部存储导入数据或将数据导出到外部存储，你需要配置跨账号访问。本文档介绍如何为 TiDB Cloud Serverless 集群配置外部存储访问权限。

如果你需要为 TiDB Cloud Dedicated 集群配置这些外部存储，请参见 [为 TiDB Cloud Dedicated 配置外部存储访问](/tidb-cloud/dedicated-external-storage.md)。

## 配置 Amazon S3 访问

为了让 TiDB Cloud Serverless 集群访问你 Amazon S3 存储桶中的源数据，可以通过以下任一方式为集群配置存储桶访问权限：

- [使用 Role ARN](#configure-amazon-s3-access-using-a-role-arn)：使用 Role ARN 访问你的 Amazon S3 存储桶。
- [使用 AWS 访问密钥](#configure-amazon-s3-access-using-an-aws-access-key)：使用 IAM 用户的访问密钥访问你的 Amazon S3 存储桶。

### 使用 Role ARN 配置 Amazon S3 访问

推荐使用 [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) 创建 Role ARN。请按照以下步骤创建：

> **Note:**
>
> 仅当集群的云服务商为 AWS 时，才支持通过 Role ARN 访问 Amazon S3。如果你使用其他云服务商，请改用 AWS 访问密钥。更多信息请参见 [使用 AWS 访问密钥配置 Amazon S3 访问](#configure-amazon-s3-access-using-an-aws-access-key)。

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 打开 **Add New ARN** 对话框。

    - 如果你想从 Amazon S3 导入数据，按如下方式打开 **Add New ARN** 对话框：

        1. 点击 **Import from S3**。
        2. 填写 **File URI** 字段。
        3. 选择 **AWS Role ARN**，并点击 **Click here to create new one with AWS CloudFormation**。

    - 如果你想将数据导出到 Amazon S3，按如下方式打开 **Add New ARN** 对话框：

        1. 点击 **Export data to...**  > **Amazon S3**。如果你的集群之前未导入或导出过任何数据，请点击页面底部的 **Click here to export data to...** > **Amazon S3**。
        2. 填写 **Folder URI** 字段。
        3. 选择 **AWS Role ARN**，并点击 **Click here to create new one with AWS CloudFormation**。

3. 使用 AWS CloudFormation 模板创建 Role ARN。

    1. 在 **Add New ARN** 对话框中，点击 **AWS Console with CloudFormation Template**。

    2. 登录 [AWS 管理控制台](https://console.aws.amazon.com)，你将被重定向到 AWS CloudFormation 的 **Quick create stack** 页面。

    3. 填写 **Role Name**。

    4. 确认创建新角色并点击 **Create stack** 以创建 Role ARN。

    5. CloudFormation stack 执行完成后，你可以点击 **Outputs** 标签页，在 **Value** 列中找到 Role ARN 的值。

        ![img.png](/media/tidb-cloud/serverless-external-storage/serverless-role-arn.png)

如果你在使用 AWS CloudFormation 创建 Role ARN 时遇到问题，可以按照以下步骤手动创建：

<details>
<summary>点击此处查看详细步骤</summary>

1. 在前述步骤描述的 **Add New ARN** 对话框中，点击 **Having trouble? Create Role ARN manually**。你将获得 **TiDB Cloud Account ID** 和 **TiDB Cloud External ID**。

2. 在 AWS 管理控制台中，为你的 Amazon S3 存储桶创建托管策略。

    1. 登录 [AWS 管理控制台](https://console.aws.amazon.com/)，打开 [Amazon S3 控制台](https://console.aws.amazon.com/s3/)。

    2. 在 **Buckets** 列表中，选择包含源数据的存储桶名称，然后点击 **Copy ARN** 获取你的 S3 存储桶 ARN（例如，`arn:aws:s3:::tidb-cloud-source-data`）。请记录该存储桶 ARN 以备后用。

        ![Copy bucket ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. 打开 [IAM 控制台](https://console.aws.amazon.com/iam/)，在左侧导航栏点击 **Policies**，然后点击 **Create Policy**。

        ![Create a policy](/media/tidb-cloud/aws-create-policy.png)

    4. 在 **Create policy** 页面，点击 **JSON** 标签。

    5. 根据你的需求在策略文本框中配置策略。以下示例可用于从 TiDB Cloud Serverless 集群导出数据和导入数据。

        - 从 TiDB Cloud Serverless 集群导出数据需要 **s3:PutObject** 和 **s3:ListBucket** 权限。
        - 向 TiDB Cloud Serverless 集群导入数据需要 **s3:GetObject**、**s3:GetObjectVersion** 和 **s3:ListBucket** 权限。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:PutObject"
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

        在策略文本框中，将以下配置替换为你自己的值。

        - `"Resource": "<Your S3 bucket ARN>/<Directory of the source data>/*"`。例如：

            - 如果你的源数据存储在 `tidb-cloud-source-data` 存储桶的根目录下，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`。
            - 如果你的源数据存储在存储桶的 `mydata` 目录下，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`。

          请确保目录末尾添加了 `/*`，以便 TiDB Cloud 能访问该目录下的所有文件。

        - `"Resource": "<Your S3 bucket ARN>"`，例如，`"Resource": "arn:aws:s3:::tidb-cloud-source-data"`。

        - 如果你启用了 AWS Key Management Service 密钥（SSE-KMS）并使用客户管理密钥加密，请确保策略中包含以下配置。`"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` 是该存储桶的一个示例 KMS 密钥。

            ```
            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }
            ```

        - 如果你的存储桶中的对象是从另一个加密存储桶复制过来的，KMS 密钥值需要包含两个存储桶的密钥。例如，`"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`。

    6. 点击 **Next**。

    7. 设置策略名称，添加策略标签（可选），然后点击 **Create policy**。

3. 在 AWS 管理控制台中，为 TiDB Cloud 创建访问角色并获取 Role ARN。

    1. 在 [IAM 控制台](https://console.aws.amazon.com/iam/)中，点击左侧导航栏的 **Roles**，然后点击 **Create role**。

        ![Create a role](/media/tidb-cloud/aws-create-role.png)

    2. 创建角色时，填写以下信息：

        - 在 **Trusted entity type** 中选择 **AWS account**。
        - 在 **An AWS account** 中选择 **Another AWS account**，然后将 TiDB Cloud account ID 粘贴到 **Account ID** 字段。
        - 在 **Options** 中，点击 **Require external ID (Best practice when a third party will assume this role)**，然后将 TiDB Cloud External ID 粘贴到 **External ID** 字段。如果创建角色时未勾选 Require external ID，则该项目下所有 TiDB 集群都可以使用同一个 Role ARN 访问你的 Amazon S3 存储桶。如果使用 account ID 和 external ID 创建角色，则只有对应的 TiDB 集群可以访问该存储桶。

    3. 点击 **Next** 打开策略列表，选择你刚刚创建的策略，然后点击 **Next**。

    4. 在 **Role details** 中设置角色名称，然后点击右下角的 **Create role**。角色创建完成后，会显示角色列表。

    5. 在角色列表中，点击你刚刚创建的角色名称进入其概览页面，然后你可以获取 Role ARN。

        ![Copy AWS role ARN](/media/tidb-cloud/aws-role-arn.png)

</details>

### 使用 AWS 访问密钥配置 Amazon S3 访问

推荐使用 IAM 用户（而不是 AWS 账号 root 用户）来创建访问密钥。

请按照以下步骤配置访问密钥：

1. 创建 IAM 用户。更多信息请参见 [创建 IAM 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)。

2. 使用你的 AWS 账号 ID 或账号别名，以及 IAM 用户名和密码登录 [IAM 控制台](https://console.aws.amazon.com/iam)。

3. 创建访问密钥。更多信息请参见 [为 IAM 用户创建访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

> **Note:**
>
> TiDB Cloud 不会存储你的访问密钥。建议在导入或导出完成后 [删除访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

## 配置 GCS 访问

为了让 TiDB Cloud Serverless 集群访问你的 GCS 存储桶，你需要为存储桶配置 GCS 访问权限。你可以使用服务账号密钥来配置存储桶访问：

请按照以下步骤配置服务账号密钥：

1. 在 Google Cloud [服务账号页面](https://console.cloud.google.com/iam-admin/serviceaccounts)点击 **CREATE SERVICE ACCOUNT** 创建服务账号。更多信息请参见 [创建服务账号](https://cloud.google.com/iam/docs/creating-managing-service-accounts)。

    1. 输入服务账号名称。
    2. 可选：输入服务账号描述。
    3. 点击 **CREATE AND CONTINUE** 创建服务账号。
    4. 在 `Grant this service account access to project` 中，选择具有所需权限的 [IAM 角色](https://cloud.google.com/iam/docs/understanding-roles)。

        - 从 TiDB Cloud Serverless 集群导出数据需要具有 `storage.objects.create` 权限的角色。
        - 向 TiDB Cloud Serverless 集群导入数据需要具有 `storage.buckets.get`、`storage.objects.get` 和 `storage.objects.list` 权限的角色。

    5. 点击 **Continue** 进入下一步。
    6. 可选：在 `Grant users access to this service account` 中，选择需要 [将服务账号附加到其他资源](https://cloud.google.com/iam/docs/attach-service-accounts) 的成员。
    7. 点击 **Done** 完成服务账号创建。

   ![service-account](/media/tidb-cloud/serverless-external-storage/gcs-service-account.png)

2. 点击服务账号，然后在 `KEYS` 页面点击 **ADD KEY** 创建服务账号密钥。

   ![service-account-key](/media/tidb-cloud/serverless-external-storage/gcs-service-account-key.png)

3. 选择默认的 `JSON` 密钥类型，然后点击 **CREATE** 下载 Google Cloud 凭证文件。该文件包含你在为 TiDB Cloud Serverless 集群配置 GCS 访问时需要使用的服务账号密钥。

## 配置 Azure Blob Storage 访问

为了让 TiDB Cloud Serverless 访问你的 Azure Blob 容器，你需要为容器创建服务 SAS token。

你可以使用 [Azure ARM 模板](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview)（推荐）或手动配置来创建 SAS token。

要使用 Azure ARM 模板创建 SAS token，请按照以下步骤操作：

1. 打开目标集群的 **Import** 页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Data** > **Import**。

2. 打开 **Generate New SAS Token via ARM Template Deployment** 对话框。
        
    1. 点击 **Export data to...**  > **Azure Blob Storage**。如果你的集群之前未导入或导出过任何数据，请点击页面底部的 **Click here to export data to...** > **Azure Blob Storage**。
   
    2. 向下滚动到 **Azure Blob Storage Settings** 区域，然后在 SAS Token 字段下点击 **Click here to create a new one with Azure ARM template**。
   
3. 使用 Azure ARM 模板创建 SAS token。

    1. 在 **Generate New SAS Token via ARM Template Deployment** 对话框中，点击 **Click to open the Azure Portal with the pre-configured ARM template**。
   
    2. 登录 Azure 后，你将被重定向到 Azure **Custom deployment** 页面。

    3. 在 **Custom deployment** 页面填写 **Resource group** 和 **Storage Account Name**。你可以在容器所在的存储账号概览页面获取所有信息。

        ![azure-storage-account-overview](/media/tidb-cloud/serverless-external-storage/azure-storage-account-overview.png)

    4. 点击 **Review + create** 或 **Next** 以审核部署。点击 **Create** 开始部署。
   
    5. 部署完成后，你将被重定向到部署概览页面。前往 **Outputs** 区域获取 SAS token。

如果你在使用 Azure ARM 模板创建 SAS token 时遇到问题，请按照以下步骤手动创建：

<details>
<summary>点击此处查看详细步骤</summary>

1. 在 [Azure Storage account](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts) 页面，点击包含容器的存储账号。
   
2. 在 **Storage account** 页面，点击 **Security+network**，然后点击 **Shared access signature**。

   ![sas-position](/media/tidb-cloud/serverless-external-storage/azure-sas-position.png)

3. 在 **Shared access signature** 页面，按如下方式创建具有所需权限的服务 SAS token。更多信息请参见 [创建服务 SAS token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)。

    1. 在 **Allowed services** 区域，选择 **Blob** 服务。
    2. 在 **Allowed Resource types** 区域，选择 **Container** 和 **Object**。
    3. 在 **Allowed permissions** 区域，根据需要选择权限。

        - 从 TiDB Cloud Serverless 集群导出数据需要 **Read** 和 **Write** 权限。
        - 向 TiDB Cloud Serverless 集群导入数据需要 **Read** 和 **List** 权限。

    4. 根据需要调整 **Start and expiry date/time**。
    5. 其他设置可保持默认值。

   ![sas-create](/media/tidb-cloud/serverless-external-storage/azure-sas-create.png)

4. 点击 **Generate SAS and connection string** 生成 SAS token。

</details>

## 配置阿里云对象存储服务（OSS）访问

为了让 TiDB Cloud Serverless 访问你的阿里云 OSS 存储桶，你需要为存储桶创建 AccessKey 对。

请按照以下步骤配置 AccessKey 对：

1. 创建 RAM 用户并获取 AccessKey 对。更多信息请参见 [创建 RAM 用户](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)。
    
    在 **Access Mode** 区域，选择 **Using permanent AccessKey to access**。

2. 创建具有所需权限的自定义策略。更多信息请参见 [创建自定义策略](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)。
    
    - 在 **Effect** 区域，选择 **Allow**。
    - 在 **Service** 区域，选择 **Object Storage Service**。
    - 在 **Action** 区域，根据需要选择权限。
   
        向 TiDB Cloud Serverless 集群导入数据时，授予 **oss:GetObject**、**oss:GetBucketInfo** 和 **oss:ListObjects** 权限。

        从 TiDB Cloud Serverless 集群导出数据时，授予 **oss:PutObject**、**oss:GetBucketInfo** 和 **oss:ListBuckets** 权限。
        
    - 在 **Resource** 区域，选择存储桶及其内的对象。

3. 将自定义策略附加到 RAM 用户。更多信息请参见 [为 RAM 用户授权](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)。