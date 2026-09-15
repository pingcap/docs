---
title: 使用 Tableau 连接到 TiDB Cloud Lake
summary: Tableau 是一个可视化分析平台，正在改变我们使用数据解决问题的方式。你可以通过 Tableau 的 **Other Databases (JDBC)** 接口，使用 lake-jdbc driver 连接到 TiDB Cloud Lake。
---

# 使用 Tableau 连接到 TiDB Cloud Lake

[Tableau](https://www.tableau.com/) 是一个可视化分析平台，正在改变我们使用数据解决问题的方式。你可以通过 Tableau 的 **Other Databases (JDBC)** 接口，使用 [lake-jdbc driver](https://github.com/tidbcloud/lake-jdbc) 连接到 {{{ .lake }}}。

为获得最佳兼容性，建议使用 Tableau 2022.3 或更高版本。

## 教程：集成 {{{ .lake }}} {#tutorial-integrating-with-lake}

本教程将指导你使用 `lake-jdbc` 将 Tableau Desktop 连接到 {{{ .lake }}}。

### 步骤 1. 获取连接信息 {#step-1-obtain-connection-information}

获取你的 {{{ .lake }}} 计算集群连接信息。更多详情，请参见[连接到计算集群](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse)。

### 步骤 2. 安装 lake-jdbc {#step-2-install-lake-jdbc}

1. 从以下任一位置下载 `0.4.6` 或更高版本的 `lake-jdbc`：

    - [lake-jdbc GitHub repository](https://github.com/tidbcloud/lake-jdbc)
    - [lake-jdbc on Maven Central](https://repo1.maven.org/maven2/com/tidbcloud/lake-jdbc/)

2. 将驱动 JAR 文件（例如 `lake-jdbc-0.4.6.jar`）移动到 Tableau 的驱动目录中。

    | 操作系统 | Tableau 的驱动程序文件夹          |
    | ---------------- | -------------------------------- |
    | MacOS            | ~/Library/Tableau/Drivers        |
    | Windows          | C:\Program Files\Tableau\Drivers |
    | Linux            | /opt/tableau/tableau_driver/jdbc |

### 步骤 3. 连接到 {{{ .lake }}} {#step-3-connect-to-lake}

1. 启动 Tableau Desktop，并在侧边栏中选择 **Other Databases (JDBC)**。

    ![Other Databases (JDBC)](/media/tidb-cloud-lake/bi-tableau-1.png)

2. 在窗口中填写你的 {{{ .lake }}} 连接信息，然后点击 **Sign In**。

    | 参数 | 描述                               | 本教程                                                   |
    | --------- | ----------------------------------------- | ------------------------------------------------------------------- |
    | URL       | 格式：`jdbc:lake://{user}:{password}@{host}:{port}/{database}` | `jdbc:lake://cloudapp:<your-password>@<your-host>:443/default` |
    | Dialect   | SQL 方言选择 "MySQL"。                    | MySQL                                                               |
    | Username  | 用于连接到 {{{ .lake }}} 的 SQL 用户      | cloudapp                                                            |
    | Password  | SQL 用户密码                              | 你的密码                                                            |

3. 当 Tableau 工作簿打开后，选择你要查询的数据库、schema 和表。对于本教程，**Database** 和 **Schema** 都选择 _default_。

至此，配置已完成！现在你可以将表拖到工作区中，开始进行查询和进一步分析。
