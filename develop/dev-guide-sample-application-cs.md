---
title: 使用 C# 连接 TiDB
summary: 学习如何使用 C# 连接 TiDB。本教程提供了与 TiDB 交互的 C# 代码示例片段。
---

# 使用 C\# 连接 TiDB

C#（发音为 “C-Sharp”）是 .NET 家族中的一种编程语言，由 Microsoft 开发。其他 .NET 语言还包括 VB.NET 和 F#。在本教程中，你将使用 C# 结合 MySQL Connector/NET，通过 MySQL 协议将 C# 应用程序连接到 TiDB。这是可行的，因为 TiDB 高度 [兼容 MySQL](/mysql-compatibility.md)。

虽然 .NET 通常在 Windows 上使用，但它同样适用于 macOS 和 Linux。在所有平台上，命令和代码基本相同，仅在提示符和文件路径上有细微差别。

## 前置条件

- 下载 [.NET 9.0 SDK](https://dotnet.microsoft.com/en-us/download)。
- 本教程使用 `dotnet` 命令行工具。你也可以使用 Visual Studio Code IDE 来编写 C# 代码。
- 要完成本教程，你需要有一个 TiDB 实例的访问权限。你可以使用 TiDB Cloud 上的 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 或 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated) 集群，或者使用自建的 TiDB 集群，例如通过 `tiup playground` 启动的集群。

## 步骤 1. 创建控制台项目

使用 `console` 模板创建一个新项目。这会生成一个名为 `tidb_cs` 的新目录。在运行以下命令前，请先切换到你希望创建该目录的位置，或者直接指定完整路径。

```
$ dotnet new console -o tidb_cs
The template "Console App" was created successfully.

Processing post-creation actions...
Restoring /home/dvaneeden/tidb_cs/tidb_cs.csproj:
Restore succeeded.
```

## 步骤 2. 添加 MySql.Data 包

.NET 的包管理器称为 NuGet。MySQL Connector/NET 的 NuGet 包名称为 [MySql.Data](https://www.nuget.org/packages/MySql.Data)，它为 .NET 应用程序提供了对 MySQL 协议的支持。如果你未指定版本，NuGet 会安装最新的稳定版本（例如 9.3.0 版本）。

```
$ cd tidb_cs
$ dotnet add package MySql.Data

Build succeeded in 1.0s
info : X.509 certificate chain validation will use the system certificate bundle at '/etc/pki/ca-trust/extracted/pem/objsign-ca-bundle.pem'.
info : X.509 certificate chain validation will use the fallback certificate bundle at '/usr/lib64/dotnet/sdk/9.0.106/trustedroots/timestampctl.pem'.
info : Adding PackageReference for package 'MySql.Data' into project '/home/dvaneeden/tidb_cs/tidb_cs.csproj'.
info :   GET https://api.nuget.org/v3/registration5-gz-semver2/mysql.data/index.json
info :   OK https://api.nuget.org/v3/registration5-gz-semver2/mysql.data/index.json 133ms
info : Restoring packages for /home/dvaneeden/tidb_cs/tidb_cs.csproj...
info :   GET https://api.nuget.org/v3/vulnerabilities/index.json
info :   OK https://api.nuget.org/v3/vulnerabilities/index.json 98ms
info :   GET https://api.nuget.org/v3-vulnerabilities/2025.06.18.05.40.02/vulnerability.base.json
info :   GET https://api.nuget.org/v3-vulnerabilities/2025.06.18.05.40.02/2025.06.19.11.40.05/vulnerability.update.json
info :   OK https://api.nuget.org/v3-vulnerabilities/2025.06.18.05.40.02/vulnerability.base.json 32ms
info :   OK https://api.nuget.org/v3-vulnerabilities/2025.06.18.05.40.02/2025.06.19.11.40.05/vulnerability.update.json 64ms
info : Package 'MySql.Data' is compatible with all the specified frameworks in project '/home/dvaneeden/tidb_cs/tidb_cs.csproj'.
info : PackageReference for package 'MySql.Data' version '9.3.0' added to file '/home/dvaneeden/tidb_cs/tidb_cs.csproj'.
info : Generating MSBuild file /home/dvaneeden/tidb_cs/obj/tidb_cs.csproj.nuget.g.targets.
info : Writing assets file to disk. Path: /home/dvaneeden/tidb_cs/obj/project.assets.json
log  : Restored /home/dvaneeden/tidb_cs/tidb_cs.csproj (in 551 ms).
```

## 步骤 3. 更新代码

将 `Program.cs` 中的 “Hello World” 示例替换为以下代码。

```cs
using System;
using MySql.Data.MySqlClient;
public class Tutorial1
{
    public static void Main()
    {
        // For production, always use strong, unique passwords.
        string connStr = "server=127.0.0.1;user=root;database=test;port=4000;AllowUserVariables=true";
        MySqlConnection conn = new MySqlConnection(connStr);
        try
        {
            Console.WriteLine("Connecting to TiDB...\n");
            conn.Open();
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.ToString());
            Environment.Exit(1);
        }

        Console.WriteLine("Connected to: " + conn.ServerVersion);

        MySqlCommand cmd = new MySqlCommand("SELECT TIDB_VERSION()", conn);

        MySqlDataReader rdr = cmd.ExecuteReader();

        rdr.Read();
        Console.WriteLine("\nVersion details:\n" + rdr[0]);
        rdr.Close();

        conn.Close();
        Console.WriteLine("Done.");
    }
}
```

这段代码会连接到指定 IP 和端口的 TiDB 实例。如果你使用 TiDB Cloud，请将连接字符串参数（如主机名、端口、用户和密码）替换为 [TiDB Cloud 控制台](https://tidbcloud.com/) 中提供的详细信息。

该代码会连接到数据库，打印其版本信息，然后通过执行 SQL 查询 [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version) 获取更详细的版本信息，并最终输出该结果。

## 步骤 4. 运行程序

```
$ dotnet run
Connecting to TiDB...

Connected to: 8.0.11-TiDB-v8.5.3

Version details:
Release Version: v8.5.3
Edition: Community
Git Commit Hash: f43a13324440f92209e2a9f04c0bbe9cf763978d
Git Branch: HEAD
UTC Build Time: 2025-05-29 03:30:55
GoVersion: go1.23.8
Race Enabled: false
Check Table Before Drop: false
Store: tikv
Done.
```