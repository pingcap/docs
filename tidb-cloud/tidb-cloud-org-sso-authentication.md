---
title: 组织 SSO 认证
summary: 了解如何通过自定义的组织认证登录 TiDB Cloud 控制台。
---

# 组织 SSO 认证

单点登录（SSO）是一种认证方案，使你 TiDB Cloud [组织](/tidb-cloud/tidb-cloud-glossary.md#organization)中的成员能够使用身份提供商（IdP）中的身份登录 TiDB Cloud，而无需使用邮箱地址和密码。

TiDB Cloud 支持以下两种 SSO 认证类型：

- [标准 SSO](/tidb-cloud/tidb-cloud-sso-authentication.md)：成员可以使用 GitHub、Google 或 Microsoft 的认证方式登录 [TiDB Cloud 控制台](https://tidbcloud.com/)。标准 SSO 默认对 TiDB Cloud 中的所有组织启用。

- 云组织 SSO：成员可以使用你组织指定的认证方式，通过 TiDB Cloud 的自定义登录页面登录。云组织 SSO 默认处于禁用状态。

与标准 SSO 相比，云组织 SSO 提供了更高的灵活性和自定义能力，可以更好地满足你组织的安全和合规要求。例如，你可以指定登录页面上显示哪些认证方式，限制允许登录的邮箱地址域名，并允许你的成员通过使用 [OpenID Connect (OIDC)](https://openid.net/connect/) 或 [Security Assertion Markup Language (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) 身份协议的身份提供商（IdP）登录 TiDB Cloud。

本文档将指导你如何将组织的认证方案从标准 SSO 迁移到云组织 SSO。

> **注意：**
>
> 云组织 SSO 功能仅对付费组织开放。

## 开始前的准备

在迁移到云组织 SSO 之前，请为你的组织检查并确认本节中的各项内容。

> **注意：**
>
> - 云组织 SSO 启用后无法禁用。
> - 启用云组织 SSO 需要你拥有 TiDB Cloud 组织的 `Organization Owner` 角色。关于角色的更多信息，参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

### 确定组织 TiDB Cloud 登录页面的自定义 URL

启用云组织 SSO 后，你的成员必须使用自定义 URL 登录 TiDB Cloud，而不能再使用公共登录 URL（`https://tidbcloud.com`）。

自定义 URL 启用后无法更改，因此你需要提前确定要使用的 URL。

自定义 URL 的格式为 `https://tidbcloud.com/enterprise/signin/your-company-name`，其中 `your-company-name` 可自定义为你的公司名称。

### 确定组织成员的认证方式

TiDB Cloud 为组织 SSO 提供以下认证方式：

- 用户名和密码
- Google
- GitHub
- Microsoft
- OIDC
- SAML

启用云组织 SSO 时，前四种方式默认启用。如果你希望强制组织成员使用 SSO，可以禁用用户名和密码认证方式。

所有已启用的认证方式都会显示在你的自定义 TiDB Cloud 登录页面上，因此你需要提前决定哪些认证方式需要启用或禁用。

### 决定是否启用自动加入（Auto-provision）

自动加入是一项允许成员无需 `Organization Owner` 或 `Project Owner` 邀请即可自动加入组织的功能。在 TiDB Cloud 中，所有支持的认证方式默认禁用自动加入。

- 当某认证方式未启用自动加入时，只有被 `Organization Owner` 或 `Project Owner` 邀请的用户才能通过自定义 URL 登录。
- 当某认证方式启用自动加入时，任何使用该认证方式的用户都可以通过自定义 URL 登录。登录后，他们会被自动分配为组织内的默认 `Organization Viewer` 角色。

出于安全考虑，如果你选择启用自动加入，建议在[配置认证方式详情](#step-2-配置认证方式)时限制允许认证的邮箱域名。

### 通知成员关于云组织 SSO 迁移计划

在启用云组织 SSO 之前，请确保告知你的成员以下内容：

- TiDB Cloud 的自定义登录 URL
- 何时开始使用自定义登录 URL 替代 `https://tidbcloud.com` 进行登录
- 可用的认证方式
- 成员登录自定义 URL 是否需要邀请

## Step 1. 启用云组织 SSO

要启用云组织 SSO，请按照以下步骤操作：

1. 以拥有 `Organization Owner` 角色的用户身份登录 [TiDB Cloud 控制台](https://tidbcloud.com)，然后通过左上角的下拉框切换到目标组织。
2. 在左侧导航栏，点击 **Organization Settings** > **Authentication**。
3. 在 **Authentication** 页面，点击 **Enable**。
4. 在弹窗中输入你组织的自定义 URL，该 URL 在 TiDB Cloud 中必须唯一。

    > **注意：**
    >
    > 云组织 SSO 启用后，URL 无法更改。你组织的成员只能通过自定义 URL 登录 TiDB Cloud。如果后续需要更改已配置的 URL，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 获取帮助。

5. 勾选 **I understand and confirm** 复选框，然后点击 **Enable**。

    > **注意：**
    >
    > 如果弹窗中包含需要重新邀请和重新加入云组织 SSO 的用户列表，TiDB Cloud 会在你启用云组织 SSO 后自动向这些用户发送邀请邮件。收到邀请邮件后，每位用户需点击邮件中的链接验证身份，随后会显示自定义登录页面。

## Step 2. 配置认证方式

在 TiDB Cloud 中启用某认证方式后，使用该方式的成员可以通过你的自定义 URL 登录 TiDB Cloud。

### 配置用户名和密码、Google、GitHub 或 Microsoft 认证方式

启用云组织 SSO 后，你可以按如下方式配置用户名和密码、Google、GitHub 或 Microsoft 认证方式：

1. 在 **Organization Settings** 页面，根据需要启用或禁用 Google、GitHub 或 Microsoft 认证方式。
2. 对于已启用的认证方式，你可以点击 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> 配置该方式的详细信息。
3. 在认证方式详情中，你可以配置以下内容：

    - [**Auto-provision Accounts**](#决定是否启用自动加入auto-provision)

        默认禁用。你可以根据需要启用。出于安全考虑，如果你选择启用自动加入，建议限制允许认证的邮箱域名。

    - **Allowed Email Domains**

        配置该字段后，只有指定邮箱域名的用户才能通过自定义 URL 使用该认证方式登录 TiDB Cloud。填写域名时需去除 `@` 符号，并用英文逗号分隔。例如：`company1.com,company2.com`。

        > **注意：**
        >
        > 如果你已配置邮箱域名，在保存设置前，请确保添加了你当前用于登录的邮箱域名，以避免被 TiDB Cloud 锁定无法登录。

4. 点击 **Save**。

### 配置 OIDC 认证方式

如果你有使用 OIDC 身份协议的身份提供商，可以为 TiDB Cloud 登录启用 OIDC 认证方式。

在 TiDB Cloud 中，OIDC 认证方式默认禁用。启用云组织 SSO 后，你可以按如下方式启用并配置 OIDC 认证方式：

1. 从你的身份提供商获取 TiDB Cloud 组织 SSO 所需的以下信息：

    - Issuer URL
    - Client ID
    - Client secret

2. 在 **Organization Settings** 页面，点击 **Authentication** 标签页，在 **Authentication Methods** 区域找到 OIDC 行，然后点击 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> 展开 OIDC 方式详情。
3. 在认证方式详情中，你可以配置以下内容：

    - **Name**

        指定 OIDC 认证方式在自定义登录页面上显示的名称。

    - **Issuer URL**、**Client ID** 和 **Client Secret**

        粘贴你从 IdP 获取的对应值。

    - [**Auto-provision Accounts**](#决定是否启用自动加入auto-provision)

        默认禁用。你可以根据需要启用。出于安全考虑，如果你选择启用自动加入，建议限制允许认证的邮箱域名。

    - **Allowed Email Domains**

        配置该字段后，只有指定邮箱域名的用户才能通过自定义 URL 使用该认证方式登录 TiDB Cloud。填写域名时需去除 `@` 符号，并用英文逗号分隔。例如：`company1.com,company2.com`。

        > **注意：**
        >
        > 如果你已配置邮箱域名，在保存设置前，请确保添加了你当前用于登录的邮箱域名，以避免被 TiDB Cloud 锁定无法登录。

4. 点击 **Save**。

### 配置 SAML 认证方式

如果你有使用 SAML 身份协议的身份提供商，可以为 TiDB Cloud 登录启用 SAML 认证方式。

> **注意：**
>
> TiDB Cloud 以邮箱地址作为不同用户的唯一标识。因此，请确保你组织成员的 `email` 属性已在身份提供商中配置。

在 TiDB Cloud 中，SAML 认证方式默认禁用。启用云组织 SSO 后，你可以按如下方式启用并配置 SAML 认证方式：

1. 从你的身份提供商获取 TiDB Cloud 组织 SSO 所需的以下信息：

    - Sign on URL
    - Signing Certificate

2. 在 **Organization Settings** 页面，点击左侧导航栏的 **Authentication** 标签页，在 **Authentication Methods** 区域找到 SAML 行，然后点击 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> 展开 SAML 方式详情。
3. 在认证方式详情中，你可以配置以下内容：

    - **Name**

        指定 SAML 认证方式在自定义登录页面上显示的名称。

    - **Sign on URL**

        粘贴你从 IdP 获取的 URL。

    - **Signing Certificate**

        粘贴你从 IdP 获取的完整签名证书，包括起始行 `---begin certificate---` 和结束行 `---end certificate---`。

    - [**Auto-provision Accounts**](#决定是否启用自动加入auto-provision)

        默认禁用。你可以根据需要启用。出于安全考虑，如果你选择启用自动加入，建议限制允许认证的邮箱域名。

    - **Allowed Email Domains**

        配置该字段后，只有指定邮箱域名的用户才能通过自定义 URL 使用该认证方式登录 TiDB Cloud。填写域名时需去除 `@` 符号，并用英文逗号分隔。例如：`company1.com,company2.com`。

        > **注意：**
        >
        > 如果你已配置邮箱域名，在保存设置前，请确保添加了你当前用于登录的邮箱域名，以避免被 TiDB Cloud 锁定无法登录。

    - **SCIM Provisioning Accounts**

        默认禁用。如果你希望通过身份提供商集中自动化管理 TiDB Cloud 组织用户和用户组的创建、删除和身份管理，可以启用该选项。详细配置步骤见 [配置 SCIM 自动化管理](#配置-scim-自动化管理)。

4. 点击 **Save**。

#### 配置 SCIM 自动化管理

[跨域身份管理系统（SCIM）](https://www.rfc-editor.org/rfc/rfc7644) 是一种开放标准，用于自动化在身份域和 IT 系统之间交换用户身份信息。通过配置 SCIM 自动化管理，你可以将身份提供商中的用户组自动同步到 TiDB Cloud，并在 TiDB Cloud 中集中管理这些组的角色。

> **注意：**
>
> SCIM 自动化管理仅可在 [SAML 认证方式](#配置-saml-认证方式) 上启用。

1. 在 TiDB Cloud 中，启用 [SAML 认证方式](#配置-saml-认证方式) 的 **SCIM Provisioning Accounts** 选项，并记录以下信息以备后续使用。

    - SCIM connector base URL
    - 用户唯一标识字段
    - 认证模式

2. 在你的身份提供商中，为 TiDB Cloud 配置 SCIM 自动化管理。

    1. 在身份提供商中，为你的 TiDB Cloud 组织的 SAML 应用集成添加 SCIM 自动化管理。

        例如，如果你的身份提供商是 Okta，参见 [为应用集成添加 SCIM 自动化管理](https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_scim.htm)。

    2. 在身份提供商中，将 SAML 应用集成分配给所需的用户组，使组内成员可以访问和使用该应用集成。

        例如，如果你的身份提供商是 Okta，参见 [将应用集成分配给用户组](https://help.okta.com/en-us/content/topics/provisioning/lcm/lcm-assign-app-groups.htm)。

   3. 将身份提供商中的用户组推送到 TiDB Cloud。

        例如，如果你的身份提供商是 Okta，参见 [管理用户组推送](https://help.okta.com/en-us/content/topics/users-groups-profiles/usgp-group-push-main.htm)。

3. 在 TiDB Cloud 中查看从身份提供商推送的用户组。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，通过左上角下拉框切换到目标组织。
    2. 在左侧导航栏，点击 **Organization Settings** > **Authentication**。
    3. 点击 **Groups** 标签页。你可以看到从身份提供商同步过来的用户组。
    4. 如需查看某个组内的用户，点击 **View**。

4. 在 TiDB Cloud 中为从身份提供商推送的用户组分配角色。

    > **注意：**
    >
    > 为用户组分配角色意味着组内所有成员都将获得该角色。如果某个组包含已在 TiDB Cloud 组织中的成员，这些成员也会获得该组的新角色。

    1. 如需为用户组分配组织角色，点击 **By organization**，然后在 **Organization Role** 列中配置角色。关于组织角色的权限，参见 [组织角色](/tidb-cloud/manage-user-access.md#organization-roles)。
    2. 如需为用户组分配项目角色，点击 **By project**，然后在 **Project Role** 列中配置角色。关于项目角色的权限，参见 [项目角色](/tidb-cloud/manage-user-access.md#project-roles)。

5. 如果你在身份提供商中更改了推送组的成员，这些更改会动态同步到 TiDB Cloud 中对应的用户组。

    - 如果在身份提供商中为组新增成员，这些成员会获得对应组的角色。
    - 如果在身份提供商中移除组成员，这些成员也会从 TiDB Cloud 中对应的用户组移除。