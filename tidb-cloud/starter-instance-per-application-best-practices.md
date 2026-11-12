---
title: Best Practices for One {{{ .starter }}} Instance per Application
summary: Onboard a platform that gives each website, app, or tenant its own {{{ .starter }}} instance by planning instance capacity, provisioning, region, network, SQL users, connections, spending limits, and lifecycle, and then running a pre-launch check.
---

# Best Practices for One {{{ .starter }}} Instance per Application

Platforms that generate or host many applications, such as website builders, AI app builders, agent platforms, and SaaS products, often give each application its own {{{ .starter }}} instance. This model keeps the data, credentials, usage, and lifecycle of each application separate. This guide describes the decisions to make when you onboard such a platform, and ends with a pre-launch check that you can run before production traffic arrives.

Make these decisions during the proof of concept (PoC), with the same compute environment, network path, and provisioning rate that you plan to use in production. This guide applies to MySQL-compatible {{{ .starter }}} instances.

## Step 1. Decide whether each application needs its own instance

Before you write provisioning code, decide how applications map to instances. Changing the model after launch requires migrating data.

| Consideration | One instance per application | One database per application in a shared instance |
| --- | --- | --- |
| Data and credential isolation | Each instance has its own SQL users with a unique user name prefix. | Applications share an instance and are separated by databases and privileges. |
| Usage and cost | Each instance has its own Request Units (RUs), storage, and spending limit. | Applications share the RUs, storage, and spending limit of the instance. |
| Lifecycle | Deleting an application deletes its instance. | Deleting an application drops its database. |
| Branches and backups | Each application can be branched and restored on its own. | Branches and restores apply to all applications in the instance. |
| Scale | Limited by the instance capacity of your organization. See [Step 2](#step-2-plan-instance-capacity). | Limited by the number of databases and tables in an instance. See [Handle Millions of Tables in SaaS Multi-Tenant Scenarios](/best-practices/saas-best-practices.md). |

Choose one instance per application when applications are created by different end users, when an application might run code that you do not control, such as code written by an AI agent, or when you need per-application spending limits. Choose a shared instance for a large number of small applications that you operate yourself.

## Step 2. Plan instance capacity

Check the instance capacity of your organization before launch, because it limits how many applications you can serve:

- By default, each organization can create up to five free {{{ .starter }}} instances. The first five instances in an organization receive a free usage quota.
- After you add a credit card and set a monthly spending limit, a paid organization can create up to 100 {{{ .starter }}} instances and branches in total. Each branch counts as a separate instance.
- By default, each organization can create a maximum of five branches across all instances.
- If your platform needs more instances or branches, apply for the [Instance Capacity Plan](/tidb-cloud/select-cluster-tier.md#instance-capacity-plan). You receive an email notification after the application is approved. Apply early so that approval does not block your launch.

Estimate the number of instances that you need at launch and after growth, and include instances that are kept for deleted applications during a grace period, pre-created instances, and branches.

## Step 3. Provision instances outside the request path

Creating an instance is a control-plane operation that requires TiDB Cloud API credentials. Run it from a trusted provisioning service, not from the application runtime, and keep the API key in a secret manager that only this service can read.

The following example creates an instance with a monthly spending limit and waits until it becomes active:

```shell
ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name "app-<application-id>" \
  --monthly-spending-limit-usd-cents 1000 \
  --wait
```

You can also provision instances with [Terraform](/tidb-cloud/terraform-use-serverless-cluster-resource.md).

Follow these practices:

- Measure creation time during the PoC. If an application must be ready faster than an instance can be created, create a pool of instances ahead of demand, assign one when an application is created, and refill the pool in the background.
- Make provisioning idempotent. Record the request in your own database before you create the instance, and retry failed creations without creating duplicates.
- Keep a mapping from each application to its instance ID, region, creation time, and state in your own database. Use instance names that identify the application, and do not put personal data or credentials in names.
- Use `--dry-run` to validate requests in automation before you run them.

## Step 4. Choose a region and network path

Create each instance in the region that is closest to the compute that runs the application, such as your application servers, serverless functions, or agent sandboxes. If the application also stores files in TiDB Cloud Filesystem, create the instance and the file system in the same region when both services are available there. For regions that are available to the TiDB Cloud CLI, see [Supported regions](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions).

Choose the network path based on where the application runs:

- **Private endpoint:** if the application runs in your own AWS VPC or Alibaba Cloud VPC, connect through a private endpoint so that traffic stays on the private network of the cloud provider. For more information, see [Connect via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) and [Connect via Private Endpoint with Alibaba Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md).
- **Public endpoint:** if the application runs outside your VPC, connect through the public endpoint. Connections require TLS. By default, all IP addresses are allowed, so restrict access to the egress IP addresses of your platform with [firewall rules](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md). Firewall rules do not apply to private endpoints.
- **Serverless and edge runtimes:** if the application runs where long-lived TCP connections are not available, such as edge functions, use the [TiDB Cloud serverless driver](/develop/serverless-driver.md), which connects over HTTPS through the public endpoint.

Measure query latency from the production compute environment, not from a laptop.

## Step 5. Create SQL users for each role

Each {{{ .starter }}} instance has a unique user name prefix, so credentials for one instance do not work on another instance. Within an instance, create separate SQL users for each role instead of sharing the default `<prefix>.root` user:

- Use an administrative user only in your provisioning service, for schema changes and user management.
- Give the application a read-write user that can access only the databases of that application.
- Give analytics jobs, support tools, and exploratory AI agents a read-only user.

With the TiDB Cloud CLI, you can create admin, read-write, and read-only users for an instance, and then generate the connection settings for one role:

```shell
ti db create-db-sql-users --db-cluster-id "<instance-id>"
ti db format-db-connection-string \
  --db-cluster-id "<instance-id>" \
  --read-write \
  --format env
```

Store generated credentials in a secret manager and inject them into the application at startup. Do not commit them to the application code that you generate for end users. For more information about users and roles, see [Manage Database Users and Roles](/tidb-cloud/configure-sql-users.md).

## Step 6. Configure connections

Configure the connection pool of each application for the following limits:

- A {{{ .starter }}} instance accepts up to 400 concurrent connections. If you set a spending limit, this limit increases to 5,000. If many processes or serverless functions connect to the same instance, keep the total pool size of all processes under the limit.
- A connection that remains open for more than 30 minutes can be terminated when a TiDB server restarts or undergoes maintenance. Set a maximum connection lifetime, starting with 5 minutes.
- On AWS, the idle timeout of a public endpoint connection is 340 seconds, and TCP keep-alive packets do not keep the connection open. Set the pool idle timeout below 340 seconds, or validate connections before use.
- A transaction cannot last longer than 30 minutes.
- Retry connection errors and transaction conflicts with backoff.

For more information, see [Configure Connection Pools and Connection Parameters](/develop/dev-guide-connection-parameters.md) and [Limitations and Quotas](/tidb-cloud/serverless-limitations.md).

## Step 7. Set spending limits and watch usage

The first five {{{ .starter }}} instances in an organization each receive a monthly free usage quota of 5 GiB of row-based storage, 5 GiB of columnar storage, and 50 million RUs. When an instance reaches its quota or spending limit, it denies new connections until you increase the limit or the usage resets at the start of the next month. Existing connections remain active but are throttled.

- Set a monthly spending limit for each instance that matches the plan of the application, for example, a lower limit for free-tier applications and a higher limit for paid applications. For more information, see [Manage Spending Limit for {{{ .starter }}} Instances](/tidb-cloud/manage-serverless-spend-limit.md).
- Review [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/) to estimate RU consumption for reads, writes, SQL CPU, and network egress.
- Built-in alerting is not available for {{{ .starter }}}. Watch [built-in metrics](/tidb-cloud/built-in-monitoring.md) during the PoC, and make your platform detect and report rejected connections so that you can raise a spending limit before users notice.

## Step 8. Plan backups, branches, and deletion

- Automatic backup retention is one day for a free instance. For an instance with a spending limit greater than 0, you can set retention from 1 to 30 days, with a default of 14 days. Set retention based on how long you need to recover from application mistakes. For more information, see [Back Up and Restore {{{ .starter }}} Data](/tidb-cloud/backup-and-restore-serverless.md).
- Use [branches](/tidb-cloud/branch-overview.md) to test schema changes for one application without affecting its production data. Branches are intended for short-term development and functional testing, not performance testing.
- A deleted {{{ .starter }}} instance cannot be restored. When a user deletes an application, keep the instance for a grace period, and [export its data](/tidb-cloud/serverless-export.md) if you might need it later. Then delete the instance:

    ```shell
    ti db delete-db-cluster --db-cluster-id "<instance-id>" --dry-run
    ti db delete-db-cluster --db-cluster-id "<instance-id>" --wait
    ```

- Run a periodic job that compares instances with the applications in your database, and reports instances that have no owner. Review each report before you delete an instance.

## Step 9. Run a pre-launch check

Before production traffic arrives, run the following checks from the production environment and record the results.

| Area | Check | How to verify |
| --- | --- | --- |
| Model | The application-to-instance model is chosen and documented. | Review the decision from Step 1. |
| Capacity | Instance and branch capacity covers expected growth. | Compare your estimate with the organization limits, or confirm Instance Capacity Plan approval. |
| Provisioning | Creating an application does not wait for instance creation, or the wait is acceptable. | Measure instance creation time and pool refill time at the expected peak rate. |
| Provisioning | Provisioning retries do not create duplicate instances. | Interrupt a creation and retry it. |
| Region | Instances are in the same region as their compute. | Compare the instance region with the compute region. |
| Network | Only the expected network path can reach the instance. | Connect through the private endpoint, or confirm that a connection from an IP address outside the firewall rules fails. |
| Credentials | The application uses a non-admin user that cannot access other applications. | Connect with the application user and run a statement against another database. |
| Connections | Pool size, maximum lifetime, and idle timeout are within the limits. | Review the pool configuration and run a load test at the expected peak. |
| Spending | Every instance has a spending limit, and rejected connections are reported. | Review spending limits and test the alert path. |
| Recovery | You can restore an application after a mistake. | Restore a test instance from a backup. |
| Deletion | Deleted applications are exported, if needed, and their instances are removed. | Run the deletion workflow against a test application. |

When you contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md), include the instance ID, region, the operation or SQL statement, the time of the failure, and the error message. Do not include passwords or API keys.

## What's next

- [Select Your Plan](/tidb-cloud/select-cluster-tier.md)
- [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md)
- [Connect to Your {{{ .starter }}} Instance](/tidb-cloud/connect-to-tidb-cluster-serverless.md)
