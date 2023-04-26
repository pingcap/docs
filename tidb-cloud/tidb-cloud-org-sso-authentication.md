---
title: Organization SSO Authentication
summary: Learn how to log in to the TiDB Cloud console via your customized organization authentication.
---

# Organization SSO Authentication

Single Sign-On (SSO) is an authentication method that allows members in your TiDB Cloud organization to access TiDB Cloud with identities from an identity providers (IdP) instead of email and password.

TiDB Cloud provides the following two types of SSO authentication:

- Basic SSO: members can log in to the TiDB Cloud console using their GitHub, Google, or Microsoft accounts, which is quick and convenient. The basic SSO is enabled by default.

- Cloud organization SSO: members can log in to a custom login page of TiDB Cloud using the authentication method specified by your organization, which provides more flexibility and customization for your security and compliance requirements. The Cloud Organization SSO is disabled by default. After it is enabled, you can restrict the email addresses that can log in using a given method, and connect to your identity provider (IdP) using OpenID Connect (OIDC) identity protocols.

This document describes how to log in to the [TiDB Cloud console](https://tidbcloud.com/) via Cloud organization SSO.

> **Tip:**
>
> If your TiDB login page is a URL other than https://tidbcloud.com/, Cloud Organization SSO is already enabled for your organization.

## Prerequisites

Before enabling organization SSO, you need to check and confirm the the following information.

> **Note:**
>
> Once Cloud Organization SSO is enabled, it cannot be disabled.

### Decide TiDB Cloud login URL for your organization

After Organization SSO is enabled, your members need to sign in TiDB Cloud at your customized login URL instead of the public login URL at `https://tidbcloud.com`.

Enabling Cloud Organization SSO requires you configuring a unique custom URL for your members to access TiDB Cloud.

For example:

`https://tidbcloud.com/unique-company`

You need to decide what URL to be used and share this URL with your members beforehand.

Once a URL is configured for organization SSO, your members must use this URL to log into TiDB Cloud. If you need to change the configured URL, contact TiDB Cloud Support for assistance.

### Decide authentication methods for your members

TiDB Cloud provides the following authentication methods for Organization SSO.

- Google
- GitHub
- Microsoft
- OIDC

When you enable Cloud Organization SSO, the first three methods are enabled by default.

You need to decide which authentication methods to be enabled. Only the enabled authentication methods will be displayed on the customized TiDB Cloud login page. As TiDB Cloud uses email address to identify your members, ensure that their email addresses in your TiDB Cloud organization match those in your IdPs. For members with multiple SSO authentication options, ensure that their email addresses match across all methods.

### Decide whether to enable autoprovisioning

To log in to TiDB Cloud using SSO without autoprovisioning:

        - A member's email address must exist in the SSO IdP.
        - An Orgnization owner must have already invited the member to the TiDB Cloud organization.

        Auto provisioning allows members to access your organization without an invitation. Members are assigned the Organization member role by default. If you enable auto provisioning, TiDB Cloud recommends that you also limit the allowed email domains for the authentication method.

### Notify your members about the Organization SSO plan

Before enabling Cloud Organization SSO, inform your members about the following:

- Provide your members with the custom login URL and let them know when to start using it.
- Specify which authentication methods are available and if autoprovisioning is enabled.
- For members who sign in using an authentication method with autoprovisioning enabled, they will be automatically added. Otherwise, you will need to re-invite them to the organization. If they had the org owner role before, you will need to re-grant the role to them again.
- For members that are also in other organizations, you need to re-add them to your organization. If they sign in using an authentication method with autoprovisioning enabled, TiDB Cloud will add them automatically. Otherwise, you need to be re-invite them. If they had the Org Administrator role before,  you will need to re-grant the role to them again.


"The following users will have to re-invite and re-join the organization once Cloud organization SSO is enabled."

A list of affected members will be displayed during the feature's enablement, and each member will be notified individually.

### Ensure that at least one organization Owner belongs to no other TiDB Cloud organization

To ensure the success of your migration from basic SSO or organization SSO, make sure that at least one Organization Owner belongs exclusively to the TiDB Cloud organization to be migrated.

If all organization Owners belong to multiple organizations, the migration will fail, and you will get the `Cloud Organization SSO cannot be enabled` error.

## Step 1. Enable Cloud Organization SSO

To enable Cloud Organization SSO:

1. Log in to [TiDB Cloud console](https://tidbcloud.com) as a user with the organization owner role.
2. In the upper-right corner of the TiDB Cloud console, click <MDSvgIcon name="icon-top-organization" /> > **Organization Settings**.
3. On the **Organization Settings** page, click the **Authentication** tab, and then click **Enable**.
4. In the dialog, fill in the custom URL for your organization, which must be unique in TiDB Cloud.

    > **Note:**
    >
    > - The URL cannot be changed once Cloud Organization SSO is enabled. Members in your organization will only be able to log into TiDB Cloud using your custom URL. If you need to change the configured URL later, contact TiDB Cloud Support for assistance.
    > - If the dialog includes a list of users to be re-invited and re-join the organization once Cloud organization SSO is enabled, check the list and learn the impact.

5. Click the **I understand and confirm** check box, and then click **Enable**.

Cloud Organization SSO is enabled, and members can sign in by using the custom URL and selecting any enabled authentication method.

## Step 2. Configure authentication methods

### Configure Google, GitHub, or Microsoft authentication methods

When an authentication method is enabled, members can log into TiDB Cloud using that authentication method. A member can log in using any enabled authentication method, as long as the email address for the member is the same across all enabled methods.

To authentication methods:

1. Log in to TiDB Cloud Console as a user with the Organization Owner role.
2. Go to Organization Settings > Authentication..
3. To enable or disable the authentication method, toggle Enable / Disable
4. To configure an authentication method, click the edit icon and fill in the details.
5. Edit the following:
    - Configure Auto provisioning.
    By default, auto provisioning is disabled.

    - Configure allowed email domains for an authentication method

        Set Allowed Email Domains to a comma-separated list of email domains. Each domain should begin with a @. To ensure that you are not locked out of TiDB Cloud while you are configuring Cloud Organization SSO, be sure to allow access to the email domain that you use to sign in.
6. Click Save.

### Configure OIDC authentication method

To configure a custom OIDC authentication method:

1. Log in to your IdP and gather the following information, which you will use to configure TiDB Cloud SSO:

    - Issuer URL
    - Client ID
    - Client secret
    - Callback URL

2. In a separate browser, log in to TiDB Cloud Console as a user with the Orgnization Owner role.
3. Go to Organization Settings > Authentication.
4. Next to Authentication Methods, click Edit icon of OIDB.
5. Set Configuration to OIDC (OpenID Connect).
6. Paste the values from your IdP for the Issuer URL, Client ID, Client Secret, and Callback URL.
5. Edit the following:

    - Configure Auto provisioning.
    By default, auto provisioning is disabled.

    - Configure allowed email domains for an authentication method

        Set Allowed Email Domains to a comma-separated list of email domains. Each domain should begin with a @. To ensure that you are not locked out of TiDB Cloud while you are configuring Cloud Organization SSO, be sure to allow access to the email domain that you use to sign in
6. Click Save.
7. The authentication method has been added but is disabled. To enable it, toggle Enable.
8. Click Test. If errors are shown, edit the configuration to fix the problems and try again.
9. Optionally, configure advanced settings for the new authentication method.