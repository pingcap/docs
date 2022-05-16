---
title: Developer Overview
summary: Described the outline of the developer's guide is listed.
---

# Developer Overview

This guide is written for application developers, but if you are interested in the inner workings of TiDB or want to get involved in TiDB development, then go read the [TiDB Kernel Development Guide](https://pingcap.github.io/tidb-dev-guide/) for more information about TiDB.

We will show how to quickly build an application using TiDB. Therefore, before reading this page, we recommend that you read the [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md) and install the Driver or use the ORM framework.

## TiDB Basics

Before you start working with TiDB, you need to understand some important mechanics of how TiDB databases work:

- Read the [TiDB Transaction Overview](/transaction-overview.md) to understand how TiDB transactions work or check out the [Transaction Notes for Application Developers](/develop/dev-guide-transaction-overview.md) to see what application developers need to know about the part of the transaction.
- In addition, you need to understand [The way applications interact with TiDB](#the-way-applications-interact-with-tidb)

## TiDB Transaction Mechanism

TiDB supports distributed transactions and offers both [optimistic transaction](/optimistic-transaction.md) and [pessimistic transaction](/pessimistic-transaction.md) modes. the current version of TiDB defaults to the **pessimistic transaction** mode, which allows you to transact with TiDB as you would with a traditional monolithic database (e.g., MySQL).

You can open a transaction using [BEGIN](/common/sql-statements/sql-statement-begin.md). Or explicitly specify a **pessimistic transaction** using `BEGIN PESSIMISTIC`, an **optimistic transaction** using `BEGIN OPTIMISTIC`. Then, [COMMIT](/common/sql-statements/sql-statement-commit.md) or [ROLLBACK](/common/sql-statements/sql-statement-rollback.md) the transaction.

TiDB guarantees atomicity for you for all statements between the start of `BEGIN` and the end of `COMMIT` or `ROLLBACK`, that is, all statements during this period succeed or fail. This is used to ensure the data consistency you need for application development.

If you are not sure what an **optimistic transaction** is, do ***NOT*** use it yet. Because the **optimistic transactions** require that the application can correctly handle [all errors](/error-codes.md) returned by the `COMMIT` statement. If you are not sure how your application will handle them, just use a **pessimistic transaction**.

## The way applications interact with TiDB

TiDB is highly compatible with MySQL protocol, TiDB supports [most MySQL syntax and features](https://docs.pingcap.com/zh/tidb/stable/mysql-compatibility), so most MySQL connection libraries are compatible with TiDB. If your application framework or language does not have an official PingCAP adaptation, then we recommend that you use MySQL's client libraries. At the same time, more and more three-party databases are actively supporting TiDB's different features.

Since TiDB is compatible with MySQL protocol and MySQL syntax, most of the ORMs that support MySQL are also compatible with TiDB.

## Read More

- [Quick Start](/develop/dev-guide-build-cluster-in-cloud.md)
- [Choose Driver or ORM](/develop/dev-guide-choose-driver-or-orm.md)
- [Connect to TiDB](/develop/dev-guide-connect-to-tidb.md)
- [Database Schema Design](/develop/dev-guide-schema-design-overview.md)
- [Write Data](/develop/dev-guide-insert-data.md)
- [Read Data](/develop/dev-guide-get-data-from-single-table.md)
- [Transaction](/develop/dev-guide-transaction-overview.md)
- [Optimize](/develop/dev-guide-optimize-sql-overview.md)
- [Example Applications](/develop/dev-guide-sample-application-spring-boot.md)