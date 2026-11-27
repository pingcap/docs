---
title: Best Practices for One {{{ .starter }}} Instance per Application
summary: Onboard a platform that gives each website, app, or tenant its own {{{ .starter }}} instance by choosing the instance model, planning capacity and cost, provisioning instances, storing and delivering credentials, configuring network access, SQL users, and connections, and running a pre-launch check.
---

# Best Practices for One {{{ .starter }}} Instance per Application

Platforms that generate or host many applications, such as website builders, AI app builders, agent platforms, and SaaS products, often give each application its own {{{ .starter }}} instance. Before you onboard such a platform, decide whether each application needs its own instance, how many instances your organization can hold, how instances are created ahead of demand, where connection credentials are stored and how each application receives them, and how applications connect, recover, and are deleted.

Make these decisions during the proof of concept (PoC), with the same compute environment, network path, and provisioning rate that you plan to use in production. This guide applies to MySQL-compatible {{{ .starter }}} instances.

## Before you begin

### Prepare your TiDB Cloud account and organization

1. If you do not have a TiDB Cloud account, [sign up](https://tidbcloud.com/free-trial) and log in to the [TiDB Cloud console](https://tidbcloud.com/).
2. Select the organization that will own the instances. If you belong to several organizations, click the combo box in the upper-left corner of the console and select the target organization. For more information, see [View and switch between organizations](/tidb-cloud/manage-user-access.md#view-and-switch-between-organizations).
3. If you plan to create more than five instances, add a credit card to the organization on the [**Billing**](https://tidbcloud.com/org-settings/billing/payments) page. An organization without a credit card can create only five free instances.

### Check the required roles

| Task | Required role or credential |
| --- | --- |
| Create TiDB Cloud API keys and add a payment method | The `Organization Owner` role in the organization |
| Create, list, update, and delete instances and branches with the TiDB Cloud CLI or API | A TiDB Cloud API key with `Organization Owner` access |
| Create SQL users and grant database privileges | A SQL user with the `role_admin` built-in role, such as the admin user that `ti db create-db-sql-users` creates |

For more information about roles, see [Identity Access Management](/tidb-cloud/manage-user-access.md).

### Create and store a TiDB Cloud API key

1. Go to the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page of your organization and create an API key with `Organization Owner` access.
2. Save the public key and the private key in a secret manager that only your provisioning service can read. Do not put the keys in source code, container images, CI logs, or the environment of an application runtime.
3. In the provisioning service, provide the keys through environment variables:

    ```shell
    export TIDB_CLOUD_PUBLIC_KEY="<public-key>"
    export TIDB_CLOUD_PRIVATE_KEY="<private-key>"
    ```

### Install the TiDB Cloud CLI

The commands in this guide were verified with TiDB Cloud CLI (`ti`) v0.2.11. Install `ti` v0.2.11 or later on the machine that runs your provisioning service:

```shell
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
export PATH="$HOME/.ti/bin:$PATH"
ti --version
```

If `ti --version` reports an earlier version, run `ti update`. To confirm that the API key works, run `ti db list-db-clusters --db-cluster-type starter --region <region-code>`. For more information, see [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).

You can also call the [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless/) directly with the same API key.

### Placeholders used in this guide

| Placeholder | Meaning | How to get it |
| --- | --- | --- |
| `<region-code>` | The region of the instance, such as `aws-us-west-2` | Choose from [Supported regions](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions). |
| `<application-id>` | The ID of a website, app, or tenant in your platform | Use the ID from your own platform database. |
| `<instance-id>` | The ID of a {{{ .starter }}} instance | Read the `id` field returned by `ti db create-db-cluster`, or run `ti db list-db-clusters --db-cluster-type starter`. |
| `<prefix>` | The user name prefix of an instance | Read the `user_prefix` field returned by `ti db describe-db-cluster --db-cluster-id <instance-id>`. |
| `<password>` | The password of a SQL user that you create | Generate a random password in your provisioning service and store it in your secret manager. |

## Step 1. Decide whether each application needs its own instance

Before you write provisioning code, decide how applications map to instances. Changing the model after launch requires migrating data.

### Problems when applications share an instance

When many applications share one {{{ .starter }}} instance, each with its own database, the following limits apply to all of them together:

- **Quota and spending limit:** Request Units (RUs), storage, and the spending limit belong to the instance. When the instance reaches its quota or spending limit, it denies new connections for every application in it, and existing connections are throttled. One busy application can make all the others unavailable.
- **Connection limit:** an instance accepts up to 400 concurrent connections, or 5,000 with a spending limit. All applications in the instance share this limit.
- **Recovery:** {{{ .starter }}} restores a backup snapshot only to a new instance and does not support point-in-time restore. To recover one application, you restore the data of every application in the instance to a new instance, and then copy that application's database back.
- **Access control:** the built-in roles, such as `role_readwrite`, apply to every database in the instance. An application that uses such a user, a mistyped grant, or a SQL injection in generated code can read or change the data of other applications.
- **Branches:** a branch copies the whole instance, so testing a schema change for one application copies the data of all applications. A branch cannot be created when the instance is larger than 100 GiB.
- **Cost attribution and deletion:** usage is billed per instance, so you must meter each application yourself, and deleting an application means dropping its databases and users without affecting the others.

With one instance per application, each of these limits applies to one application only: an application that exhausts its quota, loses data, or is compromised does not affect others, and deleting an application deletes its instance.

### Choose a model

| Consideration | One instance per application | One database per application in a shared instance |
| --- | --- | --- |
| Data and credential isolation | Each instance has its own SQL users with a unique user name prefix. | Applications share an instance and are separated by databases and privileges. |
| Usage and cost | Each instance has its own RUs, storage, and spending limit. | Applications share the RUs, storage, and spending limit of the instance. |
| Lifecycle | Deleting an application deletes its instance. | Deleting an application drops its databases and users. |
| Branches and backups | Each application can be branched and restored on its own. | Branches and restores apply to all applications in the instance. |
| Scale | Limited by the instance capacity of your organization. See [Step 2](#step-2-plan-instance-capacity-and-cost). | Limited by the number of databases and tables in an instance. See [Handle Millions of Tables in SaaS Multi-Tenant Scenarios](/best-practices/saas-best-practices.md). |

Choose one instance per application when applications are created by different end users, when an application might run code that you do not control, such as code written by an AI agent, or when you need per-application spending limits. Choose a shared instance for a large number of small applications that you operate yourself and that need to query each other's data.

## Step 2. Plan instance capacity and cost

Check the instance capacity of your organization before launch, because it limits how many applications you can serve:

- By default, each organization can create up to five free {{{ .starter }}} instances. The first five instances in an organization receive a monthly free usage quota.
- After an organization has five free instances, creating another instance without a spending limit fails with a quota error. Set a spending limit when you create the instance, for example, with `--monthly-spending-limit-usd-cents`.
- A paid organization can create up to 100 {{{ .starter }}} instances and branches in total. Each branch counts as a separate instance.
- By default, each organization can create a maximum of five branches across all instances.
- If your platform needs more instances or branches, apply for the [Instance Capacity Plan](/tidb-cloud/select-cluster-tier.md#instance-capacity-plan). The plan is intended for platforms that create databases on behalf of their users, and its pricing and limits are agreed with TiDB Cloud sales. An instance capacity charge might apply above 100 active instances and branches, and it is shown in billing separately from usage charges. Apply early so that approval does not block your launch.

Estimate the number of instances that you need at launch and after growth, and include instances that are kept for deleted applications during a grace period, pre-created instances, and branches.

Estimate cost per instance as well. {{{ .starter }}} charges for RUs and for row-based and columnar storage above the free quota. Storage is billed per GiB-month, so instances that keep data but receive little traffic still add storage cost. Delete the instances of abandoned applications instead of keeping them indefinitely. For more information, see [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/).

## Step 3. Provision instances outside the request path

Creating an instance is a control-plane operation that requires TiDB Cloud API credentials. Run it from a trusted provisioning service, not from the application runtime.

The following example creates an instance with a monthly spending limit and waits until it becomes active:

```shell
ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name "app-<application-id>" \
  --monthly-spending-limit-usd-cents 1000 \
  --wait
```

The TiDB Cloud API provides the same operation as [`CreateCluster`](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless/#tag/Cluster/operation/ClusterService_CreateCluster). You can also provision instances with [Terraform](/tidb-cloud/terraform-use-serverless-cluster-resource.md).

Follow these practices:

- Measure creation time during the PoC. If an application must be ready faster than an instance can be created, create a pool of instances ahead of demand, assign one when an application is created, and refill the pool in the background.
- To fill a pool or handle a large number of new applications, create instances in batches with the [`BatchCreateClusters`](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless/#tag/Cluster/operation/ClusterService_BatchCreateClusters) API instead of calling the create operation once per instance. One request can create up to 1,000 instances. A batch request is atomic: either all instances in the batch are created or none are, so retry a failed batch as a whole.
- Make provisioning idempotent. Record the request in your own database before you create the instance, and retry failed creations without creating duplicates.
- Use instance names that identify the application, and do not put personal data or credentials in names.
- Use `--dry-run` to validate requests in automation before you run them.

## Step 4. Store and deliver connection credentials

TiDB Cloud does not return a complete connection string when it creates an instance. The create response, and `ti db describe-db-cluster`, contain the instance ID, the public endpoint host and port, and the user name prefix. Passwords exist only where you set or generate them:

- If you pass `rootPassword` to the `CreateCluster` API, the password is the one you generated. TiDB Cloud does not return it later.
- If you run `ti db create-db-sql-users`, `ti` generates the passwords and stores them in `~/.ti/db_users/<instance-id>/credentials` on the machine that runs the command. Copy the credentials that an application needs into your secret manager. Do not rely on this local file in production.

Store connection information in two places:

- In your platform database, keep one row per application with the non-secret connection settings and a reference to the secret. For example:

    ```sql
    CREATE TABLE app_databases (
        application_id VARCHAR(64) PRIMARY KEY,
        instance_id VARCHAR(32) NOT NULL,
        region_code VARCHAR(32) NOT NULL,
        host VARCHAR(255) NOT NULL,
        port INT NOT NULL,
        db_user VARCHAR(64) NOT NULL,
        db_name VARCHAR(64) NOT NULL,
        secret_ref VARCHAR(255) NOT NULL,
        state VARCHAR(16) NOT NULL,
        created_at DATETIME NOT NULL
    );
    ```

    `secret_ref` points to the password in your secret manager, and `state` records whether the instance is pooled, assigned, or being deleted.

- In your secret manager, keep the password of each SQL user. Do not store passwords in plain text in the platform database.

Deliver credentials to each application when its runtime starts, such as when you deploy the website or start the agent sandbox that runs it. Your platform looks up the application ID, reads the password from the secret manager, and injects the settings as environment variables. The application code reads only those variables. For example, the environment of a website can contain the following variables, which use the same names as the output of `ti db format-db-connection-string --format env`:

```shell
TIDB_HOST=gateway01.<aws-region>.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=<prefix>.app
TIDB_PASSWORD=<password>
TIDB_DATABASE=app
TIDB_SSL_MODE=VERIFY_IDENTITY
```

Do not let application code look up its own credentials in a shared database by tenant ID, user ID, or project ID. That code would need credentials for the shared database, so any application, including code written by an AI agent, could read the credentials of every other application.

When you generate connection settings with `ti`, write them to a file that only the current user can read instead of printing them to a log, and then move them to your secret manager:

```shell
umask 077
ti db format-db-connection-string \
  --db-cluster-id "<instance-id>" \
  --read-write \
  --format env > app.env
```

To rotate a password, change it with `ALTER USER`, update the secret, and restart or redeploy the application so that it reads the new value.

## Step 5. Choose a region and network path

Create each instance in the region that is closest to the compute that runs the application, such as your application servers, serverless functions, or agent sandboxes. If the application also stores files in TiDB Cloud Filesystem, create the instance and the file system in the same region when both services are available there. For regions that are available to the TiDB Cloud CLI, see [Supported regions](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions).

Choose the network path based on where the application runs:

- **Private endpoint:** if the application runs in your own AWS VPC or Alibaba Cloud VPC, connect through a private endpoint so that traffic stays on the private network of the cloud provider. For more information, see [Connect via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) and [Connect via Private Endpoint with Alibaba Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md). A new instance also accepts connections from all public IP addresses, so disable the public endpoint or restrict it with firewall rules when the application uses only the private endpoint.
- **Public endpoint:** if the application runs outside your VPC, connect through the public endpoint. Connections require TLS. By default, all IP addresses are allowed, so restrict access to the egress IP addresses of your platform with [firewall rules](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md). Firewall rules do not apply to private endpoints.
- **Serverless and edge runtimes:** if the application runs where long-lived TCP connections are not available, such as edge functions, use the [TiDB Cloud serverless driver](/develop/serverless-driver.md), which connects over HTTPS through the public endpoint.

Measure query latency from the production compute environment, not from a laptop.

## Step 6. Create SQL users for each role

Each {{{ .starter }}} instance has a unique user name prefix, so credentials for one instance do not work on another instance. Within an instance, create separate SQL users for each role instead of sharing the default `<prefix>.root` user:

- Use an administrative user only in your provisioning service, for schema changes and user management.
- Give the application a read-write user that can access only the databases of that application.
- Give analytics jobs, support tools, and exploratory AI agents a read-only user.

With the TiDB Cloud CLI, you can create admin, read-write, and read-only users for an instance:

```shell
ti db create-db-sql-users --db-cluster-id "<instance-id>"
```

These users are instance-level users, not per-application users. The read-write user has the built-in `role_readwrite` role, which can change data and create tables in every database of the instance. To limit an application to its own database, use the administrative user to create a dedicated user and grant privileges on that database only:

```sql
CREATE USER '<prefix>.app' IDENTIFIED BY '<password>';
GRANT SELECT, INSERT, UPDATE, DELETE ON `app`.* TO '<prefix>.app';
```

In database-level grants, `_` and `%` are wildcards. If a database name contains either character, escape it with a backslash. Otherwise, the grant also matches other databases. For example, a grant on `app_1` without escaping also matches `appX1`. The following statement grants privileges on the `app_1` database only:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON `app\_1`.* TO '<prefix>.app1';
```

For more information, see [Privilege Management](/privilege-management.md).

Run these statements from your provisioning service over a database connection, so that the password does not appear in shell history or process listings. For more information about users and roles, see [Manage Database Users and Roles](/tidb-cloud/configure-sql-users.md).

## Step 7. Configure connections

Configure the connection pool of each application for the following limits:

- A {{{ .starter }}} instance accepts up to 400 concurrent connections. If you set a spending limit, this limit increases to 5,000. If many processes or serverless functions connect to the same instance, keep the total pool size of all processes under the limit.
- A connection that remains open for more than 30 minutes can be terminated when a TiDB server restarts or undergoes maintenance. Set a maximum connection lifetime, starting with 5 minutes.
- On AWS, the idle timeout of a public endpoint connection is 340 seconds, and TCP keep-alive packets do not keep the connection open. Set the pool idle timeout below 340 seconds, or validate connections before use.
- A transaction cannot last longer than 30 minutes.
- Retry transaction conflicts with backoff.
- Retry connection errors only for reads and idempotent writes. A connection error during a write can occur after TiDB commits the transaction, so retrying a non-idempotent write can apply it twice.

For more information, see [Configure Connection Pools and Connection Parameters](/develop/dev-guide-connection-parameters.md) and [Limitations and Quotas](/tidb-cloud/serverless-limitations.md).

## Step 8. Set spending limits and watch usage

The first five {{{ .starter }}} instances in an organization each receive a monthly free usage quota of 5 GiB of row-based storage, 5 GiB of columnar storage, and 50 million RUs. When an instance reaches its quota or spending limit, it denies new connections until you increase the limit or the usage resets at the start of the next month. Existing connections remain active but are throttled.

- Set a monthly spending limit for each instance that matches the plan of the application, for example, a lower limit for free-tier applications and a higher limit for paid applications. For more information, see [Manage Spending Limit for {{{ .starter }}} Instances](/tidb-cloud/manage-serverless-spend-limit.md).
- Review [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/) to estimate RU consumption for reads, writes, SQL CPU, and network egress.
- Built-in alerting is not available for {{{ .starter }}}. Watch [built-in metrics](/tidb-cloud/built-in-monitoring.md) during the PoC, and make your platform detect and report rejected connections so that you can raise a spending limit before users notice.

## Step 9. Plan backups, branches, and deletion

- Automatic backup retention is one day for a free instance. For an instance with a spending limit greater than 0, you can set retention from 1 to 30 days, with a default of 14 days. Set retention based on how long you need to recover from application mistakes. For more information, see [Back Up and Restore {{{ .starter }}} Data](/tidb-cloud/backup-and-restore-serverless.md).
- A restore creates a new instance with a new instance ID and user name prefix. After a restore, create or update the SQL users of the application, update its row in your platform database, and redeploy the application with the new connection settings.
- Use [branches](/tidb-cloud/branch-overview.md) to test schema changes for one application without affecting its production data. Branches are intended for short-term development and functional testing, not performance testing. A branch has its own user name prefix, so connect to it with user names that use the branch prefix.
- A deleted {{{ .starter }}} instance cannot be restored. When a user deletes an application, keep the instance for a grace period, and [export its data](/tidb-cloud/serverless-export.md) if you might need it later. Delete the branches of the instance before you delete the instance, and then delete the instance:

    ```shell
    ti db delete-db-cluster --db-cluster-id "<instance-id>" --dry-run
    ti db delete-db-cluster --db-cluster-id "<instance-id>" --wait
    ```

- Run a periodic job that compares instances with the applications in your platform database, and reports instances that have no owner. Review each report before you delete an instance.

## Step 10. Run a pre-launch check

Before production traffic arrives, run the following checks from the production environment and record the results.

| Area | Check | How to verify |
| --- | --- | --- |
| Model | The application-to-instance model is chosen and documented. | Review the decision from Step 1. |
| Capacity | Instance and branch capacity covers expected growth. | Compare your estimate with the organization limits, or confirm Instance Capacity Plan approval. |
| Provisioning | Creating an application does not wait for instance creation, or the wait is acceptable. | Measure instance creation time and pool refill time at the expected peak rate. |
| Provisioning | Provisioning retries do not create duplicate instances. | Interrupt a creation and retry it. |
| Credentials | Passwords are stored only in the secret manager, and each application receives only its own credentials. | Inspect the platform database and the environment of a running application. |
| Region | Instances are in the same region as their compute. | Compare the instance region with the compute region. |
| Network | Only the expected network path can reach the instance. | Connect through the expected endpoint. Then try to connect from an IP address outside the firewall rules, or through the public endpoint if you use only the private endpoint, and confirm that the connection fails. |
| Credentials | The application uses a non-admin user that cannot access other applications. | Connect with the application user and run a statement against another database. Expect a `command denied` error. |
| Connections | Pool size, maximum lifetime, and idle timeout are within the limits. | Review the pool configuration and run a load test at the expected peak. |
| Spending | Every instance has a spending limit, and rejected connections are reported. | Review spending limits and test the alert path. |
| Recovery | You can restore an application after a mistake. | Restore a test instance from a backup. Recreate its SQL users and permissions, update the application mapping and connection settings, and verify that the application can connect. |
| Deletion | Deleted applications are exported, if needed, and their instances are removed. | Run the deletion workflow against a test application. |

When you contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md), include the instance ID, region, the operation or SQL statement, the time of the failure, and the error message. Do not include passwords or API keys.

## What's next

- [Select Your Plan](/tidb-cloud/select-cluster-tier.md)
- [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md)
- [Connect to Your {{{ .starter }}} Instance](/tidb-cloud/connect-to-tidb-cluster-serverless.md)
