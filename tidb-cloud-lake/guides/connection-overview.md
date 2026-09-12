---
title: 连接到 TiDB Cloud Lake
summary: TiDB Cloud Lake 支持多种连接方法，以适应不同的使用场景。以下所有选项同时适用于 **TiDB Cloud Lake** 和 **self-hosted {{{ .lake }}}**。
---

# 连接到 TiDB Cloud Lake

{{{ .lake }}} 支持多种连接方法，以适应不同的使用场景。

## 快速选择 {#quick-selection}

| 我想要... | 推荐 |
|-------------|-------------|
| 以交互方式运行 SQL 查询 | **LakeSQL** (CLI) |
| 构建应用程序 | 特定语言的 **Driver** |
| 创建仪表板和报表 | **BI/可视化工具** |

## 连接字符串 {#connection-strings}

| 部署 | 格式 |
|------------|--------|
| **{{{ .lake }}}** | `lake://<user>:<pass>@<tenant>.gw.<region>.default.tidbcloud.com:443/<db>?warehouse=<name>` |

> **提示：**
>
> **{{{ .lake }}}**：登录 → 点击 **Connect** → 复制生成的 DSN

## SQL 客户端 {#sql-clients}

| 工具 | 类型 | 最适用场景 |
|------|------|----------|
| [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) | CLI | 开发者、脚本编写、自动化 |

## 驱动 {#drivers}

| 语言 | 指南 | 使用场景 |
|----------|-------|----------|
| Go | [Golang 驱动程序](/tidb-cloud-lake/guides/connect-using-golang.md) | 后端服务、微服务 |
| Python | [Python 连接器](/tidb-cloud-lake/guides/connect-using-python.md) | 数据科学、分析、机器学习 |
| Node.js | [Node.js 驱动程序](/tidb-cloud-lake/guides/connect-using-node-js.md) | Web 应用程序 |
| Java | [JDBC 驱动程序](/tidb-cloud-lake/guides/connect-using-java.md) | 企业应用程序 |
| Rust | [Rust 驱动程序](/tidb-cloud-lake/guides/connect-using-rust.md) | 系统编程 |

## 可视化工具 {#visualization-tools}

| 工具 | 类型 |
|------|------|
| [Tableau](/tidb-cloud-lake/guides/tableau.md) | 商业智能 |
| [Deepnote](/tidb-cloud-lake/guides/deepnote.md) | 协作式 Notebook |