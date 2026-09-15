---
title: MySQL - Credentials
summary: 本页面介绍如何创建 `MySQL - Credentials` 数据源。该数据源存储访问 MySQL 所需的连接信息，并可在多个 MySQL 集成任务中复用。
---

# MySQL - Credentials

本页面介绍如何创建 `MySQL - Credentials` 数据源。该数据源存储访问 MySQL 所需的连接信息，并可在多个 MySQL 集成任务中复用。

## 使用场景 {#use-cases}

- 为多个 MySQL 同步任务集中管理主机、端口和账户信息
- 避免在每个任务中重复输入相同的数据库连接设置
- 当数据库端点或账户发生变化时，可在一个位置统一修改所有依赖任务

## 创建 MySQL - Credentials {#create-mysql-credentials}

1. 进入 **Data** > **Data Sources**，然后点击 **Create Data Source**。
2. 选择 **MySQL - Credentials** 作为服务类型，然后填写连接详情：

    | 字段 | 必填 | 说明 |
    |-------|----------|-------------|
    | **Name** | 是 | 此数据源的描述性名称 |
    | **Hostname** | 是 | MySQL 服务器主机名或 IP 地址 |
    | **Port Number** | 是 | MySQL 服务器端口（默认值：`3306`） |
    | **DB Username** | 是 | 用于访问 MySQL 的用户名 |
    | **DB Password** | 是 | MySQL 用户的密码 |
    | **Database Name** | 是 | 源数据库名称 |
    | **DB Charset** | 否 | 字符集（默认值：`utf8mb4`） |
    | **Server ID** | 否 | 唯一的 binlog 复制标识符。如果未提供，则自动生成 |

3. 点击 **Test Connectivity** 以验证连接。如果测试成功，点击 **OK** 保存数据源。

## 使用建议 {#usage-recommendations}

- 使用专用的 MySQL 账户，而不是与应用负载共享同一个账户
- 如果你计划创建 `CDC Only` 或 `Snapshot + CDC` 任务，请确保该账户具有与复制相关的权限
- 在创建下游任务之前，先验证网络访问、binlog 配置和权限

## 后续步骤 {#next-steps}

创建此数据源后，你可以使用它来创建 [MySQL Integration Task](/tidb-cloud-lake/guides/integrate-with-mysql.md)。
