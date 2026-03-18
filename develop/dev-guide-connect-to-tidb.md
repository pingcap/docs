---
title: Connect to TiDB
summary: An overview of methods to connect to TiDB.
aliases: ['/tidb/stable/dev-guide-connect-to-tidb/','/tidb/dev/dev-guide-connect-to-tidb/']
---

# Connect to TiDB

TiDB is highly compatible with the MySQL protocol, so you can connect to it using most MySQL tools, drivers, and ORMs.

- To execute SQL manually (for connectivity testing, debugging, or quick verification), start with [MySQL CLI tools](/develop/dev-guide-mysql-tools.md).

- To connect using a visual interface, refer to the documents of the following popular GUI tools:

    - [JetBrains DataGrip](/develop/dev-guide-gui-datagrip.md)
    - [DBeaver](/develop/dev-guide-gui-dbeaver.md)
    - [VS Code](/develop/dev-guide-gui-vscode-sqltools.md)
    - [MySQL Workbench](/develop/dev-guide-gui-mysql-workbench.md)
    - [Navicat](/develop/dev-guide-gui-navicat.md)

- To build applications on TiDB, [choose a driver or ORM](/develop/dev-guide-choose-driver-or-orm.md) based on your programming language and framework.

- To connect to {{{ .starter }}} or {{{ .essential }}} clusters from edge environments via HTTP, use the [TiDB Cloud Serverless Driver](/develop/serverless-driver.md). Note that the serverless driver is in beta and only applicable to {{{ .starter }}} or {{{ .essential }}} clusters.

## Need help?

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
