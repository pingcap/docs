---
title: Best Practices for TiDB Security Configuration
summary: This guide introduces best practices for securing TiDB configurations to help mitigate potential security risks.
---

# Best Practices for TiDB Security Configuration

The security of TiDB is crucial for protecting data integrity and confidentiality. This document provides guidelines for configuring TiDB clusters securely during deployment. By following these best practices, you can effectively reduce potential security risks, prevent data breaches, and ensure that the TiDB database system operates continuously, stably, and reliably.

> **Note：**
>
> This document offers general advice on TiDB security configurations. PingCAP does not guarantee the completeness or accuracy of the information, and it assumes no responsibility for any issues arising from the use of this guide. Users should assess these recommendations based on their specific needs and consult professionals for tailored advice.
## Set the Initial Password for the Root User

By default, the root user in a newly created TiDB cluster has no password, which poses a potential security risk. Anyone can attempt to log in to the TiDB database as the root user, potentially gaining access to and modifying data.

To avoid this risk, it is recommended to set a root password during deployment:

- For deployments using TiUP, refer to [Deploy TiDB Cluster Using TiUP](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)to generate a random password for the root user.
- For deployments using TiDB Operator, refer to [Initializing Accounts and Passwords](https://docs.pingcap.com/tidb-in-kubernetes/stable/initialize-a-cluster#set-the-cluster-namespace-and-name) to set the root password.

## Enable Password Complexity Checks

By default, TiDB does not enforce password complexity policies, which may lead to the use of weak or empty passwords, increasing security risks.

To ensure that database users create strong passwords, it is recommended to configure a reasonable [password complexity policy](/password-management.md#password-complexity-policy). For example, require passwords to include a combination of uppercase letters, lowercase letters, numbers, and special characters. Enforcing password complexity improves database security by preventing brute force attacks, reducing internal threats, ensuring compliance with regulations, lowering the risk of data breaches, and enhancing overall security.

## Change the Default Grafana Password

TiDB installation includes the Grafana component by default, and the default username and password are typically `admin/admin`. If not changed promptly, attackers could exploit this to gain control of the system.

It is recommended to immediately change the Grafana password to a strong one during the TiDB deployment, and regularly update the password to ensure system security. Here are the steps to change the Grafana password:

- Upon first login to Grafana, follow the prompts to complete the password change.

  ![Grafana Password Reset Guide](/media/grafana-password-reset1.png)

- Access the Grafana personal configuration center to change the password.

  ![Grafana Password Reset Guide](/media/grafana-password-reset2.png)

## Enhance TiDB Dashboard Security

### Use a Least Privilege User

TiDB Dashboard shares the account system with TiDB SQL users, and TiDB Dashboard authorization is based on TiDB SQL user permissions. TiDB Dashboard requires minimal permissions and can even operate with read-only access.

To enhance security, it is recommended to create a [least-privilege SQL user](/dashboard/dashboard-user.md) for accessing the TiDB Dashboard and to avoid using high-privilege users.

### Restrict Access Control

By default, TiDB Dashboard is designed for trusted users. The default port includes additional API interfaces besides TiDB Dashboard. If you intend to allow access to TiDB Dashboard from external networks or untrusted users, you need to take the following measures to avoid security vulnerabilities:

- Use a firewall or other means to restrict the default `2379` port to trusted domains, preventing access by external users.

  > **Note:**
  >
  > TiDB, TiKV, and other components need to communicate with the PD component via the PD client port. Blocking internal network access for components will render the cluster unavailable.
- [Configure a reverse proxy](/dashboard/dashboard-ops-reverse-proxy.md#use-tidb-dashboard-behind-a-reverse-proxy) to securely provide TiDB Dashboard services to external users on a different port.

## Protect Internal Ports

TiDB’s default installation includes several privileged interfaces for inter-component communication. These ports typically do not need to be accessible to users, as they are primarily for internal communication. Exposing these ports on public networks increases the attack surface, violates the principle of least privilege, and raises the risk of security vulnerabilities. The table below lists the default listening ports in a TiDB cluster:

| Component                | Default Port | Protocol       |
|-------------------|-------------|------------|
| TiDB              | 4000        | MySQL      |
| TiDB              | 10080       | HTTP       |
| TiKV              | 20160       | Protocol   |
| TiKV              | 20180       | HTTP       |
| PD                | 2379        | HTTP/Protocol|
| PD                | 2380        | Protocol   |
| TiFlash           | 3930        | Protocol   |
| TiFlash           | 20170       | Protocol   |
| TiFlash           | 20292       | HTTP       |
| TiFlash           | 8234        | HTTP       |
| TiFlow            |  8261 | HTTP  |
| TiFlow            |  8291 | HTTP  |
| TiFlow            |  8262     | HTTP  |
| TiFlow            |  8300    | HTTP       |
| TiDB Lightning    | 8289        | HTTP       |
| TiDB Operator     | 6060        | HTTP       |
| TiDB Dashboard    | 2379        | HTTP       |
| TiDB Binlog       |  8250  | HTTP       |
| TiDB Binlog       |  8249 | HTTP      |
| TMS               | 8082        | HTTP       |
| TEM               | 8080        | HTTP       |
| TEM               | 8000        | HTTP       |
| TEM               | 4110        | HTTP       |
| TEM               | 4111        | HTTP       |
| TEM               | 4112        | HTTP       |
| TEM               | 4113        | HTTP       |
| TEM               | 4124        | HTTP       |
| Prometheus        | 9090        | HTTP       |
| Grafana           | 3000        | HTTP       |
| AlertManager      | 9093        | HTTP       |
| AlertManager      | 9094        | Protocol   |
| Node Exporter     | 9100        | HTTP       |
| Blackbox Exporter | 9115       | HTTP       |
| NG Monitoring     | 12020       | HTTP       |

It is recommended to only expose the `4000` port for the database and the `9000` port for the Grafana dashboard to general users, while restricting other ports using network security policies or firewalls. Here’s an example of using `iptables` to limit port access:

```shell
# Allow internal port communication from the whitelist of component IP addresses
sudo iptables -A INPUT -s internal IP address range -j ACCEPT

# Only open ports 4000 and 9000 to external users
sudo iptables -A INPUT -p tcp --dport 4000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9000 -j ACCEPT

# Default deny all other traffic
sudo iptables -P INPUT DROP
```

If you need to access TiDB Dashboard, it is recommended to [configure a reverse proxy](/dashboard/dashboard-ops-reverse-proxy.md#use-tidb-dashboard-behind-a-reverse-proxy) to securely provide services to external networks on a separate port.

## Resolving False Positives from Third-Party MySQL Vulnerability Scanners

Most vulnerability scanners detect MySQL vulnerabilities based on version information. Since TiDB is MySQL protocol-compatible but not MySQL itself, version-based vulnerability scans may lead to false positives. It is recommended that vulnerability scans focus on principle-based scanning. If compliance scanning tools require a MySQL version, you can [modify the server version number](/faq/high-reliability-faq.md#does-tidb-support-modifying-the-mysql-version-string-of-the-server-to-a-specific-one-that-is-required-by-the-security-vulnerability-scanning-tool) to meet the requirement.

By changing the server version number, you can avoid false positives from vulnerability scanners. The [`server-version`](/tidb-configuration-file.md#server-version) value is used by TiDB nodes to verify the current TiDB version. Before upgrading the TiDB cluster, ensure that the `server-version` value is set to empty or the real version of TiDB to avoid unexpected behavior.