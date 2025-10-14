---
title: OAuth 2.0
summary: Learn about how to use OAuth 2.0 in TiDB Cloud.
---

# OAuth 2.0

This document describes how to access TiDB Cloud using OAuth 2.0.

OAuth, which stands for Open Authorization, is an open standard authentication protocol that allows secure access to resources on behalf of a user. It provides a way for third-party applications to access user resources without exposing their credentials.

[OAuth 2.0](https://oauth.net/2/), the latest version of OAuth, has become the industry-standard protocol for authorization. Key benefits of OAuth 2.0 include:

- Security: By using token-based authentication, OAuth 2.0 minimizes the risk of password theft and unauthorized access.
- Convenience: You can grant and revoke access to your data without managing multiple credentials.
- Access control: You can specify the exact level of access granted to third-party applications, ensuring only necessary permissions are given.

## OAuth grant types

The OAuth framework specifies several grant types for different use cases. TiDB Cloud supports two most common OAuth grant types: Device Code and Authorization Code.

### Device Code grant type

It is usually used by browserless or input-constrained devices in the device flow to exchange a previously obtained device code for an access token.

### Authorization Code grant type

It is the most common OAuth 2.0 grant type, which enables both web apps and native apps to get an access token after a user authorizes an app.

## Use OAuth to access TiDB Cloud

You can access TiDB Cloud CLI using the OAuth 2.0 Device Code grant type:

- [ticloud auth login](/tidb-cloud/ticloud-auth-login.md): Authenticate with TiDB Cloud
- [ticloud auth logout](/tidb-cloud/ticloud-auth-logout.md): Log out of TiDB Cloud

If your app needs to access TiDB Cloud using OAuth, submit a request to [become a Cloud & Technology Partner](https://www.pingcap.com/partners/become-a-partner/) (select **Cloud & Technology Partner** in **Partner Program**). We will reach out to you.

## View and revoke authorized OAuth apps

You can view the records for authorized OAuth applications in the TiDB Cloud console as follows:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner.
2. Click **Account Settings**.
3. Click the **Authorized OAuth Apps** tab. You can view authorized OAuth applications.

You can click **Revoke** to revoke your authorization at any time.
