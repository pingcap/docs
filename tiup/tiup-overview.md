---
title: TiUP Overview
summary: TiUPツールとそのエコシステムを紹介します。
---

# TiUPの概要 {#tiup-overview}

TiDB 4.0 以降、パッケージ マネージャーとしてのTiUPにより、TiDB エコシステム内のさまざまなクラスター コンポーネントの管理がはるかに簡単になりました。これで、1 行のTiUPコマンドだけで任意のコンポーネントを実行できます。

## TiUPをインストールする {#install-tiup}

Darwin と Linux の両方のオペレーティング システムで、1 つのコマンドを使用してTiUPをインストールできます。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

このコマンドは、 TiUP を`$HOME/.tiup`フォルダーにインストールします。インストールされたコンポーネントとそれらの操作によって生成されたデータもこのフォルダーに配置されます。このコマンドは、Shell `.profile`ファイルの`PATH`環境変数に`$HOME/.tiup/bin`自動的に追加するため、 TiUP を直接使用できます。

インストール後、 TiUPのバージョンを確認できます。

```bash
tiup --version
```

```bash
1.14.0 tiup
Go Version: go1.21.4
Git Ref: v1.14.0
GitHash: c3e9fc518aea0da66a37f82ee5a516171de9c372
```

> **注記：**
>
> v1.11.3 以降のTiUPバージョンでは、新しく導入されたTiUPでテレメトリがデフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。共有される内容と共有を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)参照してください。

## TiUPエコシステムの紹介 {#tiup-ecosystem-introduction}

TiUP は、TiDB エコシステムのパッケージ マネージャーだけではありません。その究極の使命は、独自のエコシステムを構築することで、誰もが TiDB エコシステム ツールを**これまで以上に簡単に**使用できるようにすることです。そのためには、 TiUPエコシステムを充実させる追加のパッケージを導入する必要があります。

この一連のTiUPドキュメントでは、これらのパッケージの機能とその使用方法について説明します。

TiUPエコシステムでは、任意のコマンドに`--help`追加することでヘルプ情報を取得できます。たとえば、 TiUP自体のヘルプ情報を取得するには、次のコマンドを実行します。

```bash
tiup --help
```

    TiUP is a command-line component management tool that can help to download and install
    TiDB platform components to the local system. You can run a specific version of a component via
    "tiup <component>[:version]". If no version number is specified, the latest version installed
    locally will be used. If the specified component does not have any version installed locally,
    the latest stable version will be downloaded from the repository.

    Usage:
      tiup [flags] <command> [args...]
      tiup [flags] <component> [args...]
      tiup [command]

    Examples:
      $ tiup playground                    # Quick start
      $ tiup playground nightly            # Start a playground with the latest nightly version
      $ tiup install <component>[:version] # Install a component of specific version
      $ tiup update --all                  # Update all installed components to the latest version
      $ tiup update --nightly              # Update all installed components to the nightly version
      $ tiup update --self                 # Update the "tiup" to the latest version
      $ tiup list                          # Fetch the latest supported components list
      $ tiup status                        # Display all running/terminated instances
      $ tiup clean <name>                  # Clean the data of running/terminated instance (Kill process if it's running)
      $ tiup clean --all                   # Clean the data of all running/terminated instances

    Available Commands:
      install     Install a specific version of a component
      list        List the available TiDB components or versions
      uninstall   Uninstall components or versions of a component
      update      Update tiup components to the latest version
      status      List the status of instantiated components
      clean       Clean the data of instantiated components
      mirror      Manage a repository mirror for TiUP components
      telemetry   Controls things about telemetry
      env         Show the list of system environment variable that related to TiUP
      history     Display the historical execution record of TiUP, displays 100 lines by default
      link        Link component binary to $TIUP_HOME/bin/
      unlink      Unlink component binary to $TIUP_HOME/bin/
      help        Help about any command
      completion  Generate the autocompletion script for the specified shell

    Flags:
          --binary <component>[:version]   Print binary path of a specific version of a component <component>[:version]
                                           and the latest version installed will be selected if no version specified
          --binpath string                 Specify the binary path of component instance
      -h, --help                           help for tiup
      -T, --tag string                     [Deprecated] Specify a tag for component instance
      -v, --version                        Print the version of tiup

    Use "tiup [command] --help" for more information about a command.

出力は長くなりますが、次の 2 つの部分だけに注目してください。

-   利用可能なコマンド
    -   インストール:コンポーネントの特定のバージョンをインストールするために使用されます
    -   リスト: 利用可能な TiDB コンポーネントまたはコンポーネントの利用可能なバージョンのリストを表示するために使用されます。
    -   アンインストール: コンポーネントまたはコンポーネントのバージョンをアンインストールするために使用されます
    -   更新:コンポーネントのバージョンを更新するために使用されます
    -   ステータス: コンポーネントの実行履歴を表示するために使用されます
    -   clean: コンポーネントの実行ログをクリアするために使用されます
    -   ミラー: 公式ミラーからプライベートミラーを複製するために使用されます
    -   テレメトリ: テレメトリ機能を制御するために使用
    -   env: TiUPに関連するシステム環境変数のリストを表示するために使用されます
    -   history: TiUPの履歴実行記録を表示するために使用されます (デフォルトでは 100 行)
    -   link:コンポーネントバイナリを $TIUP_HOME/bin/ にリンクするために使用されます。
    -   unlink:コンポーネントバイナリを$TIUP_HOME/bin/からリンク解除するために使用されます。
    -   ヘルプ: ヘルプ情報を出力するために使用されます
    -   補完: 指定されたシェル (bash、zsh、fish、powershell を含む) のコマンドライン自動補完スクリプトを生成するために使用されます。
-   利用可能なコンポーネント
    -   プレイグラウンド: TiDB クラスターをローカルで起動するために使用されます
    -   client: TiUP Playground への接続に使用するクライアント
    -   クラスター: 本番環境用の TiDB クラスターを本番ために使用されます。
    -   ベンチ: データベースのストレステストに使用

> **注記：**
>
> -   利用可能なコンポーネントの数は今後も増え続けます。サポートされている最新のコンポーネントを確認するには、 `tiup list`コマンドを実行してください。
> -   利用可能なコンポーネントのバージョンのリストも増え続けます。サポートされている最新のコンポーネントバージョンを確認するには、 `tiup list <component>`コマンドを実行します。

TiUPコマンドは TiUP の内部コードに実装され、パッケージ管理操作に使用されますが、 TiUPコンポーネントはTiUPコマンドによってインストールされる独立したコンポーネントパッケージです。

たとえば、 `tiup list`コマンドを実行すると、 TiUP は独自の内部コードを直接実行します。3 コマンドを実行すると、 TiUP はまず「playground」という名前のローカル パッケージがあるかどうかを確認し、ない場合はTiUPからパッケージをダウンロード`tiup playground`て実行します。
