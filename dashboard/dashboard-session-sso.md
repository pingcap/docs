---
title: Configure SSO for TiDB Dashboard
summary: Learn how to enable SSO sign in for TiDB Dashboard
---

# Configure SSO for TiDB Dashboard

TiDB Dashboard supports [OIDC](https://openid.net/connect/) based Single Sign-On (SSO). After enabling the SSO feature of the TiDB Dashboard, users can authenticate with the configured SSO service and then use TiDB Dashboard without entering the SQL user password.

## Configure OIDC SSO

### Enable SSO

1. Sign into TiDB Dashboard.

2. Click the username in the left sidebar to access the configure page.

3. Under the **Single Sign-On** section, select **Enable to use SSO when sign into TiDB Dashboard** 。

4. Fill the **OIDC Client ID** and the **OIDC Discovery URL** fields in the form.

   Generally the two fields can be obtained from the SSO service provider:

   - OIDC Client ID: a.k.a. OIDC Token Issuer
   - OIDC Discovery URL: a.k.a. OIDC Token Audience

5. Click **Authorize Impersonation** and input the SQL password.

   TiDB Dashboard will store this SQL password and use it to impersonate a normal SQL sign-in after an SSO sign in is finished.

   ![Sample Step](/media/dashboard/dashboard-session-sso-enable-1.png)

   > **Note:**
   >
   > The password you entered will be encrypted and stored. The SSO sign-in will fail after the password of the SQL user is changed. In this case, you can re-enter the password to bring SSO back again.

6. Click **Authorize and Save**.

   ![Sample Step](/media/dashboard/dashboard-session-sso-enable-2.png)

7. Click **Update** (Update) to save the configuration.

   ![Sample Step](/media/dashboard/dashboard-session-sso-enable-3.png)

Now SSO sign in has been enabled for TiDB Dashboard.

> **Note:**
>
> For security, some SSO services requires additional configuration for the SSO service, like trusted sign in and sign out URIs. Please refer to the documentation of the SSO service for further information.

### Disable SSO

You can disable the SSO, which will completely erase the stored SQL password:

1. Sign into TiDB Dashboard.

2. Click the username in the left sidebar to access the configure page.

3. Under the **Single Sign-On** section, deselect **Enable to use SSO when sign into TiDB Dashboard** 。

4. Click **Update** (Update) to save the configuration.

   ![Sample Step](/media/dashboard/dashboard-session-sso-disable.png)

### Re-entering the Password after a Password Change

The SSO sign-in will fail once the password of the SQL user is changed. In this case, you can bring back the SSO sign-in by re-entering the SQL password:

1. Sign into TiDB Dashboard.

2. Click the username in the left sidebar to access the configure page.

3. Under the **Single Sign-On** section, Click **Authorize Impersonation** and input the updated SQL password.

   ![Sample Step](/media/dashboard/dashboard-session-sso-reauthorize.png)

4. Click **Authorize and Save**.

## Sign in with SSO

Once SSO is configured for the TiDB Dashboard, you can sign in via SSO by following steps below:

1. In the sign in page of TiDB Dashboard, click **Sign in via Company Account**.

   ![Sample Step](/media/dashboard/dashboard-session-sso-signin.png)

2. Sign in in the configured SSO service.

3. You will be redirected back to the TiDB Dashboard to finish the sign in.

## Sample: Use Okta for TiDB Dashboard SSO

[Okta](https://www.okta.com/) is an OIDC SSO identity service, which is compatible with the SSO feature of TiDB Dashboard. Steps below demostrates how to configure Okta and TiDB Dashboard so that Okta can be used as the TiDB Dashboard SSO provider.

### Step 1: Configure Okta

First, create an Okta Application Integration.

1. Access Okta admin site.

2. Navigate from left sidebar **Applications** > **Applications**.

3. Click **Create App Integration**。

   ![Sample Step](/media/dashboard/dashboard-session-sso-okta-1.png)

4. In the poped up dialog, choose **OIDC - OpenID Connect** in **Sign-in method**.

5. Choose **Single-Page Application** in **Application Type**.

6. Click **Next** button.

   ![Sample Step](/media/dashboard/dashboard-session-sso-okta-2.png)

7. Fill **Sign-in redirect URIs** as:

   ```
   http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
   ```

   Substitute `DASHBOARD_IP:PORT` with the actual domain (or IP address) and port that you use to access the TiDB Dashboard in the browser.

8. Fill **Sign-out redirect URIs** as:

   ```
   http://DASHBOARD_IP:PORT/dashboard/
   ```

   Similarly, substitute `DASHBOARD_IP:PORT` with the actual domain (or IP address) and port.

   ![Sample Step](/media/dashboard/dashboard-session-sso-okta-3.png)

9. Configure what kind of users in the organization is allowed to SSO sign in in the **Assignments** field, and then click **Save** to save the configuration.

   ![Sample Step](/media/dashboard/dashboard-session-sso-okta-4.png)

### Step 2: Obtain OIDC information and fill in TiDB Dashboard

1. In the Application Integration just created in Okta, click **Sign On**.

   ![Sample Step 1](/media/dashboard/dashboard-session-sso-okta-info-1.png)

2. Copy values of the **Issuer** and **Audience** fields from the **OpenID Connect ID Token** section.

   ![Sample Step 2](/media/dashboard/dashboard-session-sso-okta-info-2.png)

3. Open TiDB Dashboard configure page, fill **OIDC Client ID** with **Issuer** obtained from the last step and fill **OIDC Discovery URL** with **Audience**. Then finish the authorization and save configuration, as:

   ![Sample Step 3](/media/dashboard/dashboard-session-sso-okta-info-3.png)

Now TiDB Dashboard has been configured to use Okta SSO for signing in.
