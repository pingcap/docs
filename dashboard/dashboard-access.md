---
title: Access TiDB Dashboard
summary: To access TiDB Dashboard, visit the specified URL in your browser. For multiple PD instances, replace the address with any PD instance address and port. Use Chrome, Firefox, or Edge browsers of newer versions. Sign in with the TiDB root account or a user-defined SQL user. The session remains valid for 24 hours. Switch between English and Chinese languages. To log out, click the user name and then the Logout button.
aliases: ['/docs/dev/dashboard/dashboard-access/']
---

# Access TiDB Dashboard

To access TiDB Dashboard, visit <http://127.0.0.1:2379/dashboard> via your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

> **Note:**
>
> TiDB v6.5.0 (and later) and TiDB Operator v1.4.0 (and later) support deploying TiDB Dashboard as an independent Pod on Kubernetes. Using TiDB Operator, you can access the IP address of this Pod to start TiDB Dashboard. For details, see [Deploy TiDB Dashboard independently in TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently).

## Access TiDB Dashboard when multiple PD instances are deployed

When multiple multiple PD instances are deployed in your cluster and you can directly access **every** PD instance and port, you can simply replace `127.0.0.1:2379` in the <http://127.0.0.1:2379/dashboard/> address with **any** PD instance address and port.

> **Note:**
>
> If a firewall or reverse proxy is configured and you cannot directly access every PD instance, you might not be able to access TiDB Dashboard. Usually, this is because the firewall or reverse proxy is not correctly configured. See [Use TiDB Dashboard behind Reverse Proxy](/dashboard/dashboard-ops-reverse-proxy.md) and [Secure TiDB Dashboard](/dashboard/dashboard-ops-security.md) to learn how to correctly configure the firewall or reverse proxy when multiple PD instances are deployed.

## Browser compatibility

You can use TiDB Dashboard in the following common desktop browsers of a relatively newer version:

- Chrome >= 77
- Firefox >= 68
- Edge >= 17

> **Note:**
>
> If you use the browsers above of earlier versions or other browsers to access TiDB Dashboard, some functions might not work properly.

## Sign in

After accessing TiDB Dashboard, you will be directed to the user login interface, as shown in the image below.

- You can sign in to TiDB Dashboard using the TiDB `root` account.
- If you have created a [User-defined SQL User](/dashboard/dashboard-user.md), you can sign in using this account and the corresponding password.

![Login interface](/media/dashboard/dashboard-access-login.png)

If one of the following situations exists, the login might fail:

- TiDB `root` user does not exist.
- PD is not started or cannot be accessed.
- TiDB is not started or cannot be accessed.
- Wrong `root` password.

Once you have signed in, the session remains valid within the next 24 hours. To learn how to sign out, refer to the [Logout](#logout) section.

## Switch language

The following languages are supported in TiDB Dashboard:

- English
- Chinese (simplified)

In the **SQL User Sign In** page, you can click the **Switch Language** drop-down list to switch the interface language.

![Switch language](/media/dashboard/dashboard-access-switch-language.png)

## Logout

Once you have logged in, click the login user name in the left navigation bar to switch to the user page. Click the **Logout** button on the user page to log out the current user. After logging out, you need to re-enter your username and password.

![Logout](/media/dashboard/dashboard-access-logout.png)
