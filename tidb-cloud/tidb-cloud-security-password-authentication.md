---
title: Password Authentication
summary: Learn how to manage passwords and enable multi-factor authentication (MFA) in the TiDB Cloud console.
---

# Password Authentication

This document describes how to manage passwords and enable multi-factor authentication (MFA) in the TiDB Cloud console. The description is applicable to users who [sign up](https://tidbcloud.com/free-trial) for TiDB Cloud with emails and passwords.

## Sign up

After you sign up an account in the TiDB Cloud console, you can manage the password, including reseting and changing the password.

1. Go to the TiDB Cloud [sign up](https://tidbcloud.com/signup) page and fill in the registration information. 

2. Read Privacy Policy and Services Agreement.

3. Select **I agree to the Privacy Policy and Services Agreement**.

4. Click **Sign up**.

You will receive a verification email for TiDB Cloud. To complete the whole registration process, check your email box and confirm the registration.

## Sign in or sign out

### Sign in

1. Go to the TiDB Cloud [login](https://tidbcloud.com/) page.

2. Fill in your email and password.

3. Click **Sign In**.

If the login is successful, you will be directed to the TiDB Cloud console page.

### Sign out

1. Click <MDSvgIcon name="icon-top-account-settings" /> **Account** in the upper-right corner of the TiDB Cloud console.

2. Click **Logout**.

## Password policy

TiDB Cloud sets a default password policy for registered users. If your password does not meet the policy, you will get a prompt when you set the password.

The default password policy is as follows:

- At least 8 characters in length.
- At least 1 uppercase letter (A-Z).
- At least 1 lowercase letter (a-z).
- At least 1 number (0-9).
- A new password must not be the same as any of the previous four passwords.

## Reset a password

If you forget your password, you can reset it by email. The steps are as follows:

1. Go to the TiDB Cloud [login](https://tidbcloud.com/) page.

2. Click **Forgot password**, and then check your email for the link to reset the password.

> **Note:**
>
> This section is only applicable to TiDB Cloud registration with email and password. If you sign up for TiDB Cloud with Google SSO or GitHub SSO, your password is managed by Google or GitHub and you cannot change it using the TiDB Cloud console.

## Change a password

TiDB Cloud sends password expiration reminders. If you sign up for TiDB Cloud with email and password, it is recommended that you reset your password every 90 days. 

To change the password, take the following steps: 

1. Click <MDSvgIcon name="icon-top-account-settings" /> **Account** in the upper-right corner of the TiDB Cloud console.

2. Click **Account Settings**.

3. Click the **Change Password** tab, click **Change Password**, and then check your email for TiDB Cloud to reset the password.

> **Note:**
>
> If your password is not changed within 90 days, you will get a prompt to change your password when you log in to TiDB Cloud. It is recommended that you follow the prompt to change your password.

## Enable or disable MFA (optional)

After logging in to TiDB Cloud, you can enable MFA in accordance with laws and regulations.

Two-factor authentication adds additional security by requiring an Authenticator app to generate a one-time password for login. You can use any Authenticator app from the iOS or Android App Store to generate this password, such as Google Authenticator and Authy.

> **Note:**
>
> This section applies only when you [sign up](https://tidbcloud.com/free-trial) for TiDB Cloud with emails and passwords. If you sign up for TiDB Cloud with Google SSO or GitHub SSO, you can enable MFA on your identity management platform, such as GitHub or Google Workspace.

### Enable MFA

1. Click <MDSvgIcon name="icon-top-account-settings" /> **Account** in the upper-right corner of the TiDB Cloud console.

2. Click **Account settings**.

3. Click the **Two Factor Authentication** tab.

4. Click **Enable**.

### Disable MFA

1. Click <MDSvgIcon name="icon-top-account-settings" /> **Account** in the upper-right corner of the TiDB Cloud console.

2. Click **Account settings**.

3. Click the **Two Factor Authentication** tab.

4. Click **Disable**.
