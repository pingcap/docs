---
title: SSO Authentication
summary: Learn how to sign in via your Google workspace account and your Github Accounts in TiDB Cloud Web console.
---
# SSO(single sign-on) Authentication

This document describes how to quickly log in to TiDB Cloud Console via Googol workspace and GitHub accounts. 

If you log into TiDB Cloud via SSO authentication, because your identity is centrally hosted on the third-party Google and GitHub platforms, you will not be able to modify your account password and enable MFA in the TiDB console. If you want to log into TiDB Cloud through username and password, see [Password Authentication](/tidb-cloud/tidb-cloud-password-authentication.md)

## Sign in with Google SSO 

To sign in with your Google Workspace account, take the following steps:

1. Go to the TiDB Cloud [login](https://tidbcloud.com/) page.

2. Click **Sign in With Google**. You will be directed to the Google Workspace Console.

3. Follow the on-screen instructions to enter your Google username and password. 

4. Login is successful, jump to Choose to agree to "Privacy Policy, Terms of Service"

5. Jump back to your TiDB Cloud wecome page for first login successful,and then jump back to your cluster management console.

Note:

This is a secure and convenient way to log in TiDB Cloud Web Console, as your user ID and credentials are stored in a third-party platform database that you can manage its.

## Sign in with Github SSO

To Sign in with your Github, perform these steps:

1. Go to the TiDB Cloud login page: [www.tidbcloud.com](https://tidbcloud.com/).

2. In TiDB Cloud Console, click Sign in With Github.

3. Jump to Github Console, enter your Github Username and Password to login.

4. Login is successful, jump to Choose to agree to "Privacy Policy, Terms of Service"

5. Jump back to your TiDB Cloud wecome page for first login successful,and then jump back to your cluster management console.

Note:

If MFA is enabled on your Google Workspace or GitHub account, please enter your MFA Code to log in successfully,and don't support enable MFA and change password in TiDB Cloud.