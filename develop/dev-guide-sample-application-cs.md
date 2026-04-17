---
title: Connect to TiDB with C#
summary: C# を使用して TiDB に接続する方法を学びましょう。このチュートリアルでは、TiDB とやり取りするための C# コードのサンプルを提供します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-cs/','/ja/tidb/dev/dev-guide-sample-application-cs/','/ja/tidbcloud/dev-guide-sample-application-cs/']
---

# C#を使用してTiDBに接続する {#connect-to-tidb-with-c}

C#（「シーシャープ」と発音）は、Microsoftが開発した.NETファミリーのプログラミング言語の1つです。他の.NET言語には、VB.NETとF#があります。このチュートリアルでは、C#とMySQL Connector/NETを使用して、MySQLプロトコルを使用してC#アプリケーションをTiDBに接続します。これは、TiDBが[MySQLと互換性あり](/mysql-compatibility.md)高いためです。 ありがとうございます。

.NETはWindowsで広く利用されていますが、macOSやLinuxでも利用可能です。どのプラットフォームでもコマンドやコードはほぼ同じで、プロンプトやファイルパスにわずかな違いがあるだけです。

## 前提条件 {#prerequisites}

-   [.NET 9.0 SDK](https://dotnet.microsoft.com/en-us/download)をダウンロードしてください。
-   このチュートリアルでは`dotnet`コマンドラインツールを使用します。あるいは、Visual Studio Code IDE を使用して C# コードを操作することもできます。
-   このチュートリアルを完了するには、TiDB インスタンスへのアクセスが必要です。TiDB Cloud上の[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)インスタンスまたは[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)クラスター、あるいは`tiup playground`を使用して起動した TiDB Self-Managed クラスターを使用できます。

## ステップ1. コンソールプロジェクトを設定する {#step-1-set-up-a-console-project}

`console`テンプレートを使用して新しいプロジェクトを作成します。これにより`tidb_cs`という名前の新しいディレクトリが生成されます。次のコマンドを実行する前に、このディレクトリを作成する場所に移動するか、完全なパスを指定してください。

    $ dotnet new console -o tidb_cs
    The template "Console App" was created successfully.

    Processing post-creation actions...
    Restoring /home/dvaneeden/tidb_cs/tidb_cs.csproj:
    Restore succeeded.

## ステップ2. MySql.Dataパッケージを追加する {#step-2-add-the-mysql-data-package}

.NET のパッケージマネージャは NuGet と呼ばれます。MySQL Connector/NET の NuGet パッケージ名は[MySql.Data](https://www.nuget.org/packages/MySql.Data)で、.NET アプリケーションで MySQL プロトコルをサポートします。バージョンを指定しない場合、NuGet は最新の安定版 (例えば、バージョン 9.3.0) をインストールします。

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

## ステップ3. コードを更新する {#step-3-update-the-code}

`Program.cs`内の「Hello World」の例を次のコードに置き換えてください。

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

これは、指定されたIPアドレスとポート番号のTiDBインスタンスに接続します。TiDB Cloudを使用する場合は、接続文字列パラメータ（ホスト名、ポート番号、ユーザー名、パスワードなど）を[TiDB Cloudコンソール](https://tidbcloud.com/)で提供されている詳細情報に置き換えてください。 。

このコードはデータベースに接続し、そのバージョンを出力後、 [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version)を使用して SQL クエリを実行し、より詳細なバージョン情報を取得し、最後にその結果を出力。

## ステップ4．プログラムを実行する {#step-4-run-the-program}

    $ dotnet run
    Connecting to TiDB...

    Connected to: 8.0.11-TiDB-v8.5.4

    Version details:
    Release Version: v8.5.4
    Edition: Community
    Git Commit Hash: f43a13324440f92209e2a9f04c0bbe9cf763978d
    Git Branch: HEAD
    UTC Build Time: 2025-05-29 03:30:55
    GoVersion: go1.23.8
    Race Enabled: false
    Check Table Before Drop: false
    Store: tikv
    Done.
