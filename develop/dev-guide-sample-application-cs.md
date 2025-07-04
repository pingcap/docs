---
title: Connect to TiDB with C#
summary: Learn how to connect to TiDB using C#. This tutorial provides sample C# code snippets for interacting with TiDB.
---

# Connect to TiDB with C\#

C# (pronounced "C-Sharp") is one of the programming languages in the .NET family, developed by Microsoft. Other .NET languages include VB.NET and F#. In this tutorial, you will use C# along with MySQL Connector/NET to connect a C# application to TiDB using the MySQL protocol. This works because TiDB is highly [compatible with MySQL](/mysql-compatibility.md).

While .NET is commonly used on Windows, it is also available for macOS and Linux. Across all platforms, the commands and code are largely the same, with only minor differences in prompts and file paths.

## Prerequisites

- Download the [.NET 9.0 SDK](https://dotnet.microsoft.com/en-us/download).
- This tutorial uses the `dotnet` command-line tool. Alternatively, you can use the Visual Studio Code IDE to work with C# code.
- To complete this tutorial, you need access to a TiDB instance. You can use a [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier/#tidb-cloud-serverless) or [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated) cluster on TiDB Cloud, or a TiDB Self-Managed cluster, such as one started using `tiup playground`.

## Step 1. Set up a console project

Create a new project using the `console` template. This will generate a new directory named `tidb_cs`. Before running the following command, either navigate to the location where you want this directory to be created, or specify a full path.

```
$ dotnet new console -o tidb_cs
The template "Console App" was created successfully.

Processing post-creation actions...
Restoring /home/dvaneeden/tidb_cs/tidb_cs.csproj:
Restore succeeded.
```

## Step 2. Add the MySql.Data package

The package manager for .NET is called NuGet. The NuGet package name for MySQL Connector/NET is [MySql.Data](https://www.nuget.org/packages/MySql.Data), which provides support for the MySQL protocol in .NET applications. If you do not specify a version, NuGet installs the latest stable version (for example, version 9.3.0).

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

## Step 3. Update the code

Replace the "Hello World" example in `Program.cs` with the following code.

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

This connects to a TiDB instance on the specified IP and port. If you use TiDB Cloud, replace connection string parameters (such as hostname, port, user, and password) with the details provided in the [TiDB Cloud console](https://tidbcloud.com/).

The code connects to the database, prints its version, then executes a SQL query using [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version) to retrieve more detailed version information, and finally prints this result.

## Step 4. Run the program

```
$ dotnet run
Connecting to TiDB...

Connected to: 8.0.11-TiDB-v8.5.2

Version details:
Release Version: v8.5.2
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
