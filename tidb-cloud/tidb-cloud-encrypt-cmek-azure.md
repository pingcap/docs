---
title: 在 Azure 上使用客户管理的加密密钥进行静态数据加密
summary: 了解如何使用客户管理的加密密钥（CMEK）对托管在 Azure 上的 TiDB Cloud 集群中的数据进行加密。
---

# 在 Azure 上使用客户管理的加密密钥进行静态数据加密

客户管理的加密密钥（Customer-Managed Encryption Key，CMEK）允许你通过使用完全由你控制的对称加密密钥，来保护 TiDB Cloud Dedicated 集群中的静态数据。该密钥被称为 CMEK 密钥。

一旦为项目启用 CMEK，该项目下创建的所有集群都会使用 CMEK 密钥对其静态数据进行加密。此外，这些集群生成的任何备份数据也会使用同一密钥进行加密。如果未启用 CMEK，TiDB Cloud 会使用托管密钥（escrow key）对你集群中的所有静态数据进行加密。

## 限制

- 目前，TiDB Cloud 仅支持使用 AWS KMS 和 Azure Key Vault 提供 CMEK。
- 若要使用 CMEK，你需要在创建项目时启用 CMEK，并在创建集群前完成 CMEK 相关配置。你无法为已有项目启用 CMEK。
- 目前，在已启用 CMEK 的项目中，只能创建托管在 AWS 和 Azure 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。
- 目前，在已启用 CMEK 的项目中，不支持 [双区域备份](/tidb-cloud/backup-and-restore-concepts.md#dual-region-backup)。
- 目前，在已启用 CMEK 的项目中，你可以在 AWS 和 Azure 上启用 CMEK。对于每个云服务提供商，你可以为每个区域配置一个唯一的加密密钥。你只能在已为所选云服务提供商配置加密密钥的区域创建集群。

## 启用 CMEK

如果你希望使用自己账户拥有的加密密钥对数据进行加密，请按照以下步骤操作。

### 步骤 1. 创建支持 CMEK 的项目

如果你在组织中拥有 `Organization Owner` 角色，可以通过以下步骤创建支持 CMEK 的项目：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏中，点击 **Projects**。
3. 在 **Projects** 页面，点击右上角的 **Create New Project**。
4. 填写项目名称。
5. 选择启用项目的 CMEK 功能。
6. 点击 **Confirm** 完成项目创建。

### 步骤 2. 完成项目的 CMEK 配置

你可以通过 TiDB Cloud 控制台，结合 Azure 门户或 Azure Resource Manager，完成项目的 CMEK 配置。

> **注意：**
>
> - 请确保密钥的策略符合要求，并且没有权限不足或账户问题等错误。这些错误可能导致使用该密钥创建集群失败。
> - Azure 托管磁盘的跨租户客户管理密钥（CMK）功能目前处于预览阶段，仅在部分 Azure 区域可用。目前仅支持可用性区域。更多信息请参见 [使用跨租户客户管理密钥加密托管磁盘](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-cross-tenant-customer-managed-keys?tabs=azure-portal#preview-regional-availability)。

<SimpleTab groupId="method">
<div label="Use Azure portal" value="console">

要通过 TiDB Cloud 控制台和 Azure 门户配置 CMEK，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，使用左上角的下拉框切换到目标项目。

2. 在左侧导航栏中，点击 **Project Settings** > **Encryption Access**。

3. 在 **Encryption Access** 页面，点击 **Create Encryption Key**。

4. 在 **Key Management Service** 下，选择 **Azure Key Vault**，并选择将要使用加密密钥的区域。

5. 如果你的租户中尚未存在 TiDB 提供的企业应用的 Service Principal，请创建一个。TiDB Cloud 控制台会显示 **Microsoft Entra Application Name** 和 **ID**，你在本步骤及后续步骤中需要用到。要创建 Service Principal，请在 **Create Service Principal** 部分运行以下命令：

    ```shell
    az ad sp create --id {Microsoft_Entra_Application_ID}
    ```

    更多信息请参见 [Microsoft Entra ID 中的应用程序和服务主体对象](https://learn.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)。

6. 在你的 Azure 账户中创建一个 Key Vault，或选择已有的 Key Vault。确保：

    * 已启用 **Purge protection**。
    * **region** 与集群的区域一致。

7. 在 TiDB Cloud 控制台中，输入 Key Vault 名称和 Key 名称。TiDB Cloud 会为密钥名称添加唯一后缀以增强安全性。复制完整密钥名称，并在 Azure 门户中创建加密密钥。更多信息请参见 [创建你的加密密钥](https://learn.microsoft.com/en-us/azure/key-vault/keys/quick-create-portal)。

8. 为当前用户分配 **Key Vault Crypto Officer** 角色：

    1. 在 [Azure 门户](https://portal.azure.com/) 中，导航到你的 Key Vault。
    2. 点击 **Access control (IAM)**，然后点击 **Add** > **Add role assignment**。
    3. 搜索并选择 **Key Vault Crypto Officer** 角色，然后点击 **Next**。
    4. 在 **Members** 标签页，将 **Assign access to** 设置为 **User, group, or service principal**。
    5. 点击 **+ Select members**，搜索并选择当前用户作为成员。然后点击 **Select**。
    6. 检查设置后，点击 **Review + assign**。

9. 为加密密钥分配 **Key Vault Crypto Service Encryption User** 角色给 TiDB 提供的企业应用：

    1. 在你的 Key Vault 中，进入你创建的加密密钥对象。
    2. 点击 **Add** > **Add role assignment**。
    3. 搜索并选择 **Key Vault Crypto Service Encryption User** 角色，然后点击 **Next**。
    4. 在 **Members** 标签页，将 **Assign access to** 设置为 **User, group, or service principal**。
    5. 点击 **+ Select members**，输入 TiDB 提供的 **Enterprise Application Name**，并选择为成员。然后点击 **Select**。
    6. 检查配置后，点击 **Review + assign**。

10. 在 TiDB Cloud 控制台中，点击 **Test Encryption Key and Create** 以验证配置并创建加密密钥。

</div>
<div label="Use Azure Resource Manager" value="arm">

要通过 TiDB Cloud 控制台和 Azure Resource Manager 配置 CMEK，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，使用左上角的下拉框切换到目标项目。

2. 在左侧导航栏中，进入 **Project Settings** > **Encryption Access**。

3. 在 **Encryption Access** 页面，点击 **Create Encryption Key**。

4. 在 **Key Management Service** 下，选择 **Azure Key Vault**，并指定加密密钥可用的区域。

5. 如果你的租户中尚未存在 TiDB 提供的企业应用的 Service Principal，请创建一个。要创建 Service Principal，请在 **Create Service Principal** 部分运行以下命令：

    ```shell
    az ad sp create --id {Microsoft_Entra_Application_ID}
    ```

    更多信息请参见 [Microsoft Entra ID 中的应用程序和服务主体对象](https://learn.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)。

6. 在 Azure 门户中打开 [TiDB 针对 Azure Resource Manager 的自定义部署模板](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Ftcidm.blob.core.windows.net%2Fcmek%2Fazure_cmek_rmt.json%3Fsv%3D2015-04-05%26ss%3Db%26srt%3Dco%26sp%3Drl%26se%3D2029-03-01T00%3A00%3A01.0000000Z%26sig%3DIA02CymcFpYCwoTsqCSJVD%2F8Khh%2F0UAPrkKDeLMIIFc%3D)。选择你的 **Subscription** 和 **Resource Group**，然后在 **Instance Details** 部分按如下填写：

    - **Region**：选择你希望创建 Key Vault 的位置。该区域必须与你的集群区域一致。
    - **Key Vault Name**：输入你的 Azure Key Vault 名称。
    - **Key Name**：填写将在 Key Vault 中创建的完整密钥名称。在 TiDB Cloud 控制台中输入密钥名前缀并点击 **Copy** 获取完整密钥名称。
    - **Enterprise App Service Principal ID**：输入 TiDB 提供的企业应用的 Service Principal ID。要获取 **Service Principal ID**，请运行以下命令（将 `{microsoft_enterprise_app_id}` 替换为 TiDB Cloud 控制台显示的实际 ID）：
     
    ```shell
    az ad sp show --id {microsoft_enterprise_app_id} --query id -o tsv
    ```

</div>
</SimpleTab>

> **注意：**
>
> 该功能未来会进一步增强，后续功能可能需要额外的权限。因此，该策略要求可能会发生变化。

### 步骤 3. 创建集群

在 [步骤 1](#step-1-create-a-cmek-enabled-project) 创建的项目下，创建一个托管在 Azure 上的 TiDB Cloud Dedicated 集群。详细步骤请参见 [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。

当你选择云服务提供商和区域时，系统会自动匹配相应的加密密钥。如果所选云服务提供商和区域没有可用密钥，控制台会显示提示，帮助你创建密钥。

> **注意：**
>
> 启用 CMEK 后，TiDB Cloud 会使用 CMEK 对集群节点使用的 Premium SSD v2 以及集群备份的存储 blob 进行加密。

## 轮换 CMEK

你可以在 Azure Key Vault 中配置 [加密密钥自动轮换](https://learn.microsoft.com/en-us/azure/key-vault/keys/how-to-configure-key-rotation)。启用轮换后，无需在 TiDB Cloud 项目的 **Encryption Access** 设置中进行更新。

## 禁用和重新启用 CMEK

如果你需要临时撤销 TiDB Cloud 对 CMEK 的访问权限，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，暂停项目中的对应集群。
2. 在 Azure Key Vault 控制台中，右键点击加密密钥并选择 **Disable**。

> **注意：**
>
> 在 Azure Key Vault 中禁用 CMEK 后，你的运行中集群将在几分钟内变为不可用，因为它们无法再访问 CMEK。

在禁用 TiDB Cloud 对 CMEK 的访问后，如果需要恢复访问权限，请按照以下步骤操作：

1. 在 Azure Key Vault 控制台中，选择加密密钥并点击 **Enable**。
2. 在 TiDB Cloud 控制台中，恢复项目中的对应集群。