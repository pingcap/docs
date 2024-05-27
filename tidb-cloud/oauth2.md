---
title: OAuth 2.0
summary: Learn about how to use OAuth 2.0 in TiDB Cloud.
---

# OAuth 2.0

OAuth, which stands for Open Authorization, is an open standard authentication protocol commonly used to allow secure access to resources on behalf of a user. It provides a way for third-party applications to access a user's resources without exposing their credentials.

[OAuth 2.0](https://oauth.net/2/) is the industry-standard protocol for authorization. Key benefits of OAuth 2.0 include:

- Security: By using token-based authentication, OAuth 2.0 minimizes the risk of password theft and unauthorized access.
- Convenience: You can grant and revoke access to your data without managing multiple credentials.
- Control: You can specify the exact level of access granted to third-party applications, ensuring only necessary permissions are given.

## OAuth grant types

The OAuth framework specifies several grant types for different use cases. TiDB Cloud supports the most common OAuth grant types, device code and authorization code.

### Device Code grant

It is usually used by browserless or input-constrained devices in the device flow to exchange a previously obtained device code for an access token.

TiDB Cloud CLI supports OAuth 2.0 as follows:

- [ticloud auth login](/tidb-cloud/ticloud-auth-login.md): Authenticate with TiDB Cloud
- [ticloud auth logout](/tidb-cloud/ticloud-auth-logout.md): Log out of TiDB Cloud

### Authorization Code grant

It is the most common OAuth 2.0 grant type. You can use it for both web apps and native apps to get an access token after a user authorizes an app.

## Use OAuth to access TiDB Cloud

If your app needs access to TiDB Cloud by using OAuth, submit a request to [become a Cloud & Technology Partner](https://www.pingcap.com/partners/become-a-partner/). We will reach out to you.