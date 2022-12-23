---
title: Password Authentication
summary: Learn how to manage TiDB Cloud console passwords and how to enable multi-factor authentication (MFA).
---

# Password Authentication

This document describes how to manage TiDB Cloud console passwords and how to enable multi-factor authentication (MFA). It is applicable to users who [sign up](https://tidbcloud.com/free-trial) for TiDB Cloud with emails and passwords.

## Sign up

If you want to manage your TiDB Cloud passwords using the TiDB Cloud console, you can sign up for a TiDB Cloud account using your email and password. 

1. Go to the TiDB Cloud [sign up](https://tidbcloud.com/signup) page and fill in the registration information. 

2. Read Privacy Policy and Services Agreement

3. Check the box to agree **I agree to the Privacy Policy and Services Agreement**

4. Click **Sign up** to complete your account registration

You will receive a verification email for TiDB Cloud, when you check your Email address and confirm in order to complete the whole registration process.

## Setp2: sign in and sign out

### Sign In

1. Go to the TiDB Cloud login page: **www.tidbcloud.com**

2. Fill in your **Email** and **Password**

3. Click **Sign In**

4. Login is successful, jump to TiDB Cloud Console

### Sign Out

1. Click the account name in the upper-right corner of the TiDB Cloud console

2. Click **Logout**

## Password Policy

TiDB Cloud sets a default password policy for registered users. If your password does not meet the policy, you will get a prompt when you set the password.

A strong password policy is as follows:

- At least 8 characters in length.
- At least 1 uppercase letter(A-Z).
- At least 1 lowercase letter(a-z).
- At least 1 numbers(0-9).
- A new password must not be the same as any of the previous four passwords.

## Reset a password

If you forget your password, you can reset it by email. The steps are as follows:

1. Go to the TiDB Cloud login page: **www.tidbcloud.com**

2. Click **Forgot password**, and then check your Email for the link to reset the password

> **Note:**
    >
    > This section is only applicable to TiDB Cloud registration with email and password. If you sign up for TiDB Cloud with Google SSO or GitHub SSO, your password is managed by Google or GitHub and you cannot change it using the TiDB Cloud console.

## Change a password

Support password expiration reminder function. If you sign up for TiDB Cloud with email and password, it is recommended that you reset your password every 90 days. To change the password take the following steps: 

1. Click the account name in the upper-right corner of the TiDB Cloud console

2. Click **Account**

3. Click the **Change Password** tab, and then check your Email for TiDB Cloud to reset the password

> **Note:**
    >
    > If your password is not changed within 90 days, you will get a prompt to change your password when you login to TiDB Cloud. It is recommended that you follow the prompt to change password.

## Enables MFA (optional)

After logging in to TiDB Cloud, you can enable multi-factor authentication(MFA ) in accordance with laws and regulations.

Two factor authentication adds additional security by requiring an Authenticator app to generate a one-time password for login. You can use any Authenticator app from the iOS or Android App Store to generate this password, such as Google Authenticator and Authy.

### Enable MFA

The steps to enable MFA are as follows:

1. Click <MDSvgIcon name="icon-top-account-settings" /> **Account** in the upper-right corner of the TiDB Cloud console.

2. Click **Account settings**.

3. Click the **Two Factor Authentication** tab.

4. Click **Enable**.

### Disable MFA

1. Click **Account**

2. Click the **Two Factor Authentication** tab

3. Click the **Disable** tab

> **Note:**
>
> Only users who [sign up](https://tidbcloud.com/free-trial) for TiDB Cloud with emails and passwords can enable MFA in TiDB Cloud, and SSO login users are not supported. If you log in with Google SSO or GitHub SSO, you can enable MFA on your identity management platform, such as GitHub or Google Workspace.