---
title: Organization SSO Authentication
summary: Learn how to log in to the TiDB Cloud console via your customized organization authentication.
---

# Organization SSO Authentication

Single Sign-On (SSO) is an authentication method that allows members in your TiDB Cloud organization to access TiDB Cloud with identities from an identity providers (IdP) instead of emails and passwords.

TiDB Cloud provides the following two types of SSO authentication:

- Basic SSO: members can log in to the [TiDB Cloud console](https://tidbcloud.com/) using their GitHub, Google, or Microsoft accounts, which is quick and convenient. The basic SSO is enabled by default.

- Cloud Organization SSO: members can log in to a custom login page of TiDB Cloud using the authentication methods specified by your organization, which provides more flexibility and customization for your security and compliance requirements. The Cloud Organization SSO is disabled by default. After it is enabled, you can
customize the authentication method displayed your organization, specify the allowed email address domains for login, and connect to your identity provider (IdP) using OpenID Connect (OIDC) identity protocols.

## Prerequisites

Before enabling organization SSO, you need to check and confirm the the following information.

> **Note:**
>
> - Once Cloud Organization SSO is enabled, it cannot be disabled.
> - If your current TiDB login URL is not `https://tidbcloud.com/`, it means that Cloud Organization SSO is already enabled for your organization.

### Decide a custom URL for your organization's TiDB Cloud login page

Once Cloud Organization SSO is enabled, your members must log into your TiDB Cloud organization using your customized URL instead of the public login URL at `https://tidbcloud.com`.

Because the custom URL cannot be changed after the enablement, you need to decide what URL to be used in advance.

For example:

`https://tidbcloud.com/your-company-name`

### Decide authentication methods for your organization members

TiDB Cloud provides the following authentication methods for Organization SSO.

- Google
- GitHub
- Microsoft
- OIDC

When you enable Cloud Organization SSO, the first three methods are enabled by default.

Because the enabled authentication methods will be displayed on the customized TiDB Cloud login page, you need to decide which authentication methods to be enabled in advance.

As TiDB Cloud uses email address to identify your members, ensure that their email addresses in your TiDB Cloud organization match those in your IdPs. For members with multiple SSO authentication options, ensure that their email addresses match across all methods.

### Decide whether to enable autoprovisioning

Auto provisioning is a feature that allows members to automatically join an organization without requiring an invitation from an existing member or organization owner. In TiDB Cloud, it is disabled by default for all the supported authentication methods.

- When auto provisioning is enabled, new members are assigned a default `member` role within the organization. It makes it easier for new members to join an organization. For security consideration, if you choose to enable auto provisioning, it is recommended to limit the allowed email domains for authentication.

- When auto provisioning is disabled, to log in to TiDB Cloud using SSO,  a member's email address must exist in the SSO IdP and an Organization owner must have invited the member to the TiDB Cloud organization beforehand.

### Notify your members about the Cloud Organization SSO plan

Before enabling Cloud Organization SSO, communicate your members about the following:

- Provide your members with the custom login URL and let them know when to start using it.
- Specify which authentication methods are available and whether autoprovisioning is enabled.
- For members who sign in using an authentication method with autoprovisioning enabled, TiDB Cloud will add them automatically. For other members, you will need to re-invite them to the organization. If they have the org owner role before the migration, you will need to re-grant the role to them again.

You can get a full list of members who need to be re-invited and re-join the organization in the dialog box for enabling Cloud Organization SSO.

### Ensure that at least one organization Owner belongs to no other TiDB Cloud organization

To ensure the success migration from basic SSO or organization SSO, make sure that at least one Organization Owner belongs exclusively to the TiDB Cloud organization to be migrated.

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

Enabling an authentication method in TiDB Cloud allows members to log in using that method. Members can use any enabled authentication method as long as they use the same email address across all enabled methods.

After enabling Cloud Organization Cloud, you can configure Google, GitHub, or Microsoft authentication methods as follows:

1. On the **Organization Settings** page, enable or disable the Google, GitHub, or Microsoft authentication methods according to your need.
2. For an enabled authentication method, you can click <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> to configure the method details.
3. In the method details, you can configure the following:

    - [**Auto-provision Accounts**](#decide-whether-to-enable-autoprovisioning)

        It is disabled by default. You can enable it according to your need. For security consideration, if you choose to enable auto provisioning, it is recommended to limit the allowed email domains for authentication.

    - **Allowed Email Domains**

        After this field is configured, only the specified email domains of this authentication method can log into the custom URL the TiDB Cloud. When you fill in domain names, you need to exclude the @ symbol and separate them with commas. For example, `pingcap.com,tikv.com`.

        > **Note:**
        >
        > If you have configured domain names, before confirming the settings, make sure that you add the email domain that you use to sign in, to avoid that you are locked out by TiDB Cloud.

4. Click **Confirm**.

### Configure the OIDC authentication method

In TiDB Cloud, the OIDC authentication method is disabled by default.

After enabling Cloud Organization Cloud, you can enable and configure the OIDC authentication method as follows if needed:

1. Get the following information from your IdP for TiDB Cloud Organization SSO:

    - Issuer URL
    - Client ID
    - Client secret

2. On the **Organization Settings** page, enable or disable the OIDC authentication methods according to your need.
3. In the row of OIDC, click <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> to configure the method details.
4. In the method details, you can configure the following:

    - **Name**

        Specify a name the OIDC authentication method to be displayed on your custom login page.

    - **Issuer URL**, **Client ID**, and **Client Secret**

        Paste the corresponding values that you get from your IdP.

    - [**Auto-provision Accounts**](#decide-whether-to-enable-autoprovisioning)

        It is disabled by default. You can enable it according to your need. For security consideration, if you choose to enable auto provisioning, it is recommended to limit the allowed email domains for authentication.

    - **Allowed Email Domains**

        After this field is configured, only the specified email domains of this authentication method can log into the custom URL the TiDB Cloud. When you fill in domain names, you need to exclude the @ symbol and separate them with commas. For example, `pingcap.com,tikv.com`.

        > **Note:**
        >
        > If you have configured domain names, before confirming the settings, make sure that you add the email domain that you use to sign in, to avoid that you are locked out by TiDB Cloud.

5. Click **Save**.