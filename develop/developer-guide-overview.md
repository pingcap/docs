---
title: Developer Guide Overview
summary: Described the outline of the developer's guide is listed.
---

# Developer Guide Overview

This guide will show you how to quickly build an application on TiDB. Before reading this page, we recommend that you read the [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md) and install the Driver or use the ORM framework.

## Guide contents

- [Overview](#tidb-basics)
- [Choose a Driver or ORM](/develop/choose-driver-or-orm.md)
- [Connect to TiDB](/develop/connect-to-tidb.md)
- [Design a Database Schema](/develop/schema-design-overview.md)
- [Write Data](/develop/insert-data.md)
- [Read Data](/develop/get-data-from-single-table.md)
- [Transaction](/develop/transaction-overview.md)

## TiDB Basics

Before you start working with TiDB, you need to understand the important mechanics of TiDB as follows:

- Read the [TiDB Transaction Overview](/transaction-overview.md) to understand how TiDB transactions work, or check out the [Transaction Notes for Application Developers](/develop/transaction-overview.md) to see what you need to know about TiDB transactions.
- Understand [the way applications interact with TiDB](#the-way-applications-interact-with-tidb).

The following sections are written for application developers, but if you are interested in the inner workings of TiDB or want to get involved in TiDB development, then go read the [TiDB Kernel Development Guide](https://pingcap.github.io/tidb-dev-guide/) for more information about TiDB.

## TiDB Transaction Mechanism

TiDB supports distributed transactions and offers both [optimistic transaction](/optimistic-transaction.md) and [pessimistic transaction](/pessimistic-transaction.md) modes. Currently, TiDB defaults to the **pessimistic transaction** mode, which allows you to use transactions in TiDB as you would with a traditional monolithic database (for example, MySQL).

You can start a transaction using [`BEGIN`](/common/sql-statements/sql-statement-begin.md), explicitly specify a **pessimistic transaction** using `BEGIN PESSIMISTIC`, or explicitly specify an **optimistic transaction** using `BEGIN OPTIMISTIC`. After that, you can commit ([`COMMIT`](/common/sql-statements/sql-statement-commit.md)) or roll back ([`ROLLBACK`](/common/sql-statements/sql-statement-rollback.md)) the transaction.

TiDB guarantees atomicity for all statements between `BEGIN` and `COMMIT` or `ROLLBACK`, which means statements executed during this period either all succeed or all fail. This ensures data consistency for your application development.

If you are not sure what an **optimistic transaction** is, do ***NOT*** use it yet. Because **optimistic transactions** require that the application correctly handles [all errors](/error-codes.md) returned by the `COMMIT` statement. If you are not sure how your application handles the errors, use **pessimistic transactions** instead.

## The way applications interact with TiDB

TiDB is highly compatible with the MySQL protocol and supports [most MySQL syntax and features](https://docs.pingcap.com/zh/tidb/stable/mysql-compatibility). Therefore, most MySQL connection libraries are compatible with TiDB. If your application framework or the programming language you use does not have an official adaptation from PingCAP, we recommend that you use MySQL's client libraries. More and more third-party databases actively supports TiDB's unique features.

Because TiDB is compatible with the MySQL protocol and syntax, most ORMs that support MySQL are also compatible with TiDB.
