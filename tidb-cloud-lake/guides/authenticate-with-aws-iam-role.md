---
title: 使用 AWS IAM Role 进行认证
summary: 云原生身份委派（AWS IAM Role、Azure Managed Identity、Google Service Account federation 等）使 {{{ .lake }}} 能够在无需处理原始访问密钥的情况下，获取访问对象存储的短期凭证。这样可以将数据平面的访问控制保留在云服务提供商的控制平面内，同时你仍然拥有每一项权限的所有权。
---

# 使用 AWS IAM Role 进行认证

云原生身份委派（AWS IAM Role、Azure Managed Identity、Google Service Account federation 等）使 {{{ .lake }}} 能够在无需处理原始访问密钥的情况下，获取访问对象存储的短期凭证。这样可以将数据平面的访问控制保留在云服务提供商的控制平面内，同时你仍然拥有每一项权限的所有权。

## IAM role 的优势 {#iam-role-benefits}

- 无静态密钥：临时凭证消除了需要轮转或可能泄漏的长期密钥。
- 最小权限：细粒度策略将 {{{ .lake }}} 限制为只能访问你批准的存储桶和执行你批准的操作。
- 集中治理：你可以继续通过现有的 IAM 工作流审计和撤销访问。
- 自动轮转：云服务提供商会刷新令牌，因此即使团队发生变化，集成也能持续工作。

## 工作原理 {#how-it-works}

在 {{{ .lake }}} 支持团队向你的组织提供受信任主体信息后，你需要在自己的云账户中创建一个 IAM role/identity，附加一个允许执行所需对象存储操作的策略（例如读取一组存储桶），并配置 trust policy，使得只有 {{{ .lake }}} 能够使用唯一的 external ID 来 assume 该 role。随后，{{{ .lake }}} 会按需 assume 该 role，使用临时凭证访问你的存储，并在会话过期后自动登出。

## 使用 IAM role {#use-iam-role}

1. 提交一个支持工单，以获取你的 {{{ .lake }}} 组织对应的 IAM role ARN：

   例如：`arn:aws:iam::123456789012:role/xxxxxxx/tnabcdefg/xxxxxxx-tnabcdefg`

2. 前往 AWS Console：

   <https://us-east-2.console.aws.amazon.com/iam/home?region=us-east-2#/policies>

   点击 `Create policy`，选择 `Custom trust policy`，然后输入用于 S3 存储桶访问的策略文档：

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "s3:ListBucket",
         "Resource": "arn:aws:s3:::test-bucket-123"
       },
       {
         "Effect": "Allow",
         "Action": "s3:*Object",
         "Resource": "arn:aws:s3:::test-bucket-123/*"
       }
     ]
   }
   ```

   点击 `Next`，输入策略名称：`lake-test`，然后点击 `Create policy`

3. 前往 AWS Console：

   <https://us-east-2.console.aws.amazon.com/iam/home?region=us-east-2#/roles>

   点击 `Create role`，并在 `Trusted entity type` 中选择 `Custom trust policy`：

   ![Create Role](/media/tidb-cloud-lake/create-role.png)

   输入 trust policy 文档：

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "AWS": "arn:aws:iam::123456789012:role/xxxxxxx/tnabcdefg/xxxxxxx-tnabcdefg"
         },
         "Condition": {
           "StringEquals": {
             "sts:ExternalId": "my-external-id-123"
           }
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

   点击 `Next`，选择之前创建的策略：`lake-test`

   点击 `Next`，输入 role 名称：`lake-test`

   点击 `View Role`，并记录 role ARN：`arn:aws:iam::987654321987:role/lake-test`

4. 在 {{{ .lake }}} cloud worksheet 或 `LakeSQL` 中运行以下 SQL 语句：

   ```sql
   CREATE CONNECTION lake_test STORAGE_TYPE = 's3' ROLE_ARN = 'arn:aws:iam::987654321987:role/lake-test' EXTERNAL_ID = 'my-external-id-123';

   CREATE STAGE lake_test URL = 's3://test-bucket-123' CONNECTION = (CONNECTION_NAME = 'lake_test');

   SELECT * FROM @lake_test/test.parquet LIMIT 1;
   ```

> **Note:**
>
> 恭喜！现在你已经可以在 {{{ .lake }}} 中通过 IAM Role 访问你自己的 AWS S3 存储桶。