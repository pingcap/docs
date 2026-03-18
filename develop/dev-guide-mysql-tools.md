---
title: Connect to TiDB with MySQL Tools
summary: Learn how to connect to TiDB using MySQL tools.
---

# Connect to TiDB with MySQL Tools

TiDB is highly compatible with the MySQL protocol. For a full list of client link parameters, see [MySQL Client Options](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html).

TiDB supports the [MySQL Client/Server Protocol](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html), which allows most client drivers and ORM frameworks to connect to TiDB just as they connect to MySQL.

You can choose to use MySQL Client or MySQL Shell based on your personal preferences.

<SimpleTab>

<div label="MySQL Client">

You can connect to TiDB using MySQL Client, which can be used as a command-line tool for TiDB. To install MySQL Client, follow the instructions below for YUM based Linux distributions.

```shell
sudo yum install mysql
```

After the installation, you can connect to TiDB using the following command:

```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

The MySQL v9.0 client on macOS cannot correctly load the `mysql_native_password` plugin, causing the error `ERROR 2059 (HY000): Authentication plugin 'mysql_native_password' cannot be loaded` when connecting to TiDB. To address this issue, it is recommended to install and use the MySQL v8.0 client to connect to TiDB. Run the following commands to install it:

```shell
brew install mysql-client@8.0
brew unlink mysql
brew link mysql-client@8.0
```

If you still encounter errors, you can specify the installation path of the MySQL v8.0 client to connect to TiDB. Run the following command:

```shell
/opt/homebrew/opt/mysql-client@8.0/bin/mysql --comments --host ${YOUR_IP_ADDRESS} --port ${YOUR_PORT_NUMBER} -u ${your_user_name} -p
```

Replace `/opt/homebrew/opt/mysql-client@8.0/bin/mysql` in the preceding command with the installation path of the MySQL v8.0 client in your actual environment.

</div>

<div label="MySQL Shell">

You can connect to TiDB using MySQL Shell, which can be used as a command-line tool for TiDB. To install MySQL Shell, follow the instructions in the [MySQL Shell documentation](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html). After the installation, you can connect to TiDB using the following command:

```shell
mysqlsh --sql mysql://root@<tidb_server_host>:4000
```

</div>

</SimpleTab>

## Need help?

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
