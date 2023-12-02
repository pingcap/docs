---
title: TiUP Overview
summary: Introduce the TiUP tool and its ecosystem.
---

# TiUPの概要 {#tiup-overview}

TiDB 4.0 以降、パッケージ マネージャーとしてのTiUPにより、TiDB エコシステム内のさまざまなクラスター コンポーネントの管理がはるかに簡単になります。たった 1 行のTiUPコマンドで任意のコンポーネントを実行できるようになりました。

## TiUPをインストールする {#install-tiup}

TiUP は、 Darwin と Linux の両方のオペレーティング システムで 1 つのコマンドでインストールできます。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

このコマンドは、 TiUP を`$HOME/.tiup`フォルダーにインストールします。インストールされたコンポーネントとその操作によって生成されたデータもこのフォルダーに配置されます。このコマンドは、Shell `.profile`ファイルの`PATH`環境変数に`$HOME/.tiup/bin`自動的に追加するため、 TiUP を直接使用できます。

インストール後、 TiUPのバージョンを確認できます。

```bash
tiup --version
```

> **注記：**
>
> v1.11.3 以降のTiUPバージョンの場合、新しく展開されたTiUPではテレメトリはデフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。共有内容と共有を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。

## TiUPエコシステムの紹介 {#tiup-ecosystem-introduction}

TiUP は、 TiDB エコシステムの単なるパッケージ マネージャーではありません。その究極の使命は、独自のエコシステムを構築することで、誰もが**これまでより簡単に**TiDB エコシステム ツールを使用できるようにすることです。これには、 TiUPエコシステムを強化するために追加のパッケージを導入する必要があります。

この一連のTiUPドキュメントでは、これらのパッケージの機能とその使用方法を紹介します。

TiUPエコシステムでは、任意のコマンドに`--help`を追加することでヘルプ情報を取得できます。たとえば、 TiUP自体のヘルプ情報を取得するには次のコマンドがあります。

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

    Available Commands:
      install     Install a specific version of a component
      list        List the available TiDB components or versions
      uninstall   Uninstall components or versions of a component
      update      Update tiup components to the latest version
      status      List the status of instantiated components
      clean       Clean the data of instantiated components
      mirror      Manage a repository mirror for TiUP components
      help        Help about any command or component

    Components Manifest:
      use "tiup list" to fetch the latest components manifest

    Flags:
          --binary <component>[:version]   Print binary path of a specific version of a component <component>[:version]
                                           and the latest version installed will be selected if no version specified
          --binpath string                 Specify the binary path of component instance
      -h, --help                           help for tiup
      -T, --tag string                     Specify a tag for component instance
      -v, --version                        version for tiup

    Component instances with the same "tag" will share a data directory ($TIUP_HOME/data/$tag):
      $ tiup --tag mycluster playground

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

    Use "tiup [command] --help" for more information about a command.

出力は長いですが、次の 2 つの部分のみに注目してください。

-   利用可能なコマンド
    -   install: コンポーネントのインストールに使用されます
    -   list: 利用可能なコンポーネントのリストを表示するために使用されます。
    -   アンインストール: コンポーネントのアンインストールに使用されます
    -   update:コンポーネントのバージョンを更新するために使用されます
    -   ステータス: コンポーネントの実行履歴を表示するために使用されます。
    -   clean: コンポーネントの実行ログをクリアするために使用されます。
    -   ミラー: 公式ミラーからプライベート ミラーを複製するために使用されます。
    -   help: ヘルプ情報を出力するために使用されます。
-   利用可能なコンポーネント
    -   プレイグラウンド: TiDB クラスターをローカルで起動するために使用されます。
    -   クライアント: ローカル マシンの TiDB クラスターに接続するために使用されます。
    -   クラスター:本番環境に TiDB クラスターをデプロイするために使用されます。
    -   ベンチ: データベースのストレス テストに使用されます

> **注記：**
>
> -   利用可能なコンポーネントの数は今後も増加し続けます。最新のサポートされているコンポーネントを確認するには、 `tiup list`コマンドを実行します。
> -   利用可能なコンポーネントのバージョンのリストも増え続けます。サポートされているコンポーネントの最新バージョンを確認するには、 `tiup list <component>`コマンドを実行します。

TiUPコマンドは TiUP の内部コードに実装され、パッケージ管理操作に使用されます。一方、 TiUPコンポーネントは、 TiUPコマンドによってインストールされる独立したコンポーネントパッケージです。

たとえば、 `tiup list`コマンドを実行すると、 TiUP は独自の内部コードを直接実行します。 `tiup playground`コマンドを実行すると、 TiUP はTiUP「playground」という名前のローカル パッケージがあるかどうかを確認し、ない場合はミラーからパッケージをダウンロードして実行します。
