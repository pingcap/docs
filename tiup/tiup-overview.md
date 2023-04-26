---
title: TiUP Overview
summary: Introduce the TiUP tool and its ecosystem.
---

# TiUPの概要 {#tiup-overview}

TiDB 4.0 から、パッケージ マネージャーとしてのTiUP、TiDB エコシステム内のさまざまなクラスター コンポーネントの管理がはるかに簡単になります。これで、たった 1 行のTiUPコマンドで任意のコンポーネントを実行できます。

## TiUPをインストールする {#install-tiup}

Darwin と Linux オペレーティング システムの両方で、1 つのコマンドでTiUPをインストールできます。

{{< copyable "" >}}

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

このコマンドは、 TiUP を`$HOME/.tiup`フォルダーにインストールします。インストールされたコンポーネントと、その操作によって生成されたデータもこのフォルダーに配置されます。このコマンドはまた、シェル`.profile`ファイルの`PATH`環境変数に`$HOME/.tiup/bin`自動的に追加するため、 TiUP を直接使用できます。

インストール後、 TiUPのバージョンを確認できます。

{{< copyable "" >}}

```bash
tiup --version
```

> **ノート：**
>
> v1.11.3 以降のTiUPバージョンでは、新たに展開されたTiUPではテレメトリがデフォルトで無効になっており、使用状況に関する情報は収集されず、PingCAP と共有されません。詳細については、 [テレメトリー](/telemetry.md)を参照してください。

## TiUPエコシステム紹介 {#tiup-ecosystem-introduction}

TiUPは、TiDB エコシステムにおける単なるパッケージ マネージャーではありません。その究極の使命は、独自のエコシステムを構築することにより、誰もが TiDB エコシステム ツールを**これまで以上に簡単に**使用できるようにすることです。これには、 TiUPエコシステムを充実させるために追加のパッケージを導入する必要があります。

この一連のTiUPドキュメントでは、これらのパッケージの機能と使用方法を紹介します。

TiUPエコシステムでは、 TiUP自体のヘルプ情報を取得する次のコマンドのように、任意のコマンドに`--help`追加することでヘルプ情報を取得できます。

{{< copyable "" >}}

```bash
tiup --help
```

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
```

出力は長いですが、注目できるのは次の 2 つの部分だけです。

-   利用可能なコマンド
    -   install: コンポーネントのインストールに使用
    -   list: 利用可能なコンポーネントのリストを表示するために使用されます
    -   uninstall: コンポーネントのアンインストールに使用
    -   update:コンポーネントのバージョンを更新するために使用されます
    -   status: コンポーネントの実行履歴を表示するために使用されます
    -   clean: コンポーネントの実行ログをクリアするために使用されます
    -   mirror: 公式ミラーからプライベート ミラーを複製するために使用されます。
    -   help: ヘルプ情報を出力するために使用されます
-   利用可能なコンポーネント
    -   プレイグラウンド: TiDB クラスターをローカルで開始するために使用されます
    -   クライアント: ローカル マシンの TiDB クラスターに接続するために使用されます
    -   クラスター:本番環境用の TiDB クラスターをデプロイするために使用されます
    -   ベンチ: データベースのストレステストに使用

> **ノート：**
>
> -   利用可能なコンポーネントの数は増え続けます。最新の対応コンポーネントを確認するには、 `tiup list`コマンドを実行します。
> -   コンポーネントの利用可能なバージョンのリストも増え続けます。サポートされているコンポーネントの最新バージョンを確認するには、 `tiup list <component>`コマンドを実行します。

TiUPコマンドは TiUP の内部コードに実装され、パッケージ管理操作に使用されますが、 TiUPコンポーネントはTiUPコマンドによってインストールされる独立したコンポーネントパッケージです。

たとえば、 `tiup list`コマンドを実行すると、 TiUP は独自の内部コードを直接実行します。 `tiup playground`コマンドを実行すると、 TiUP は最初に「playground」という名前のローカル パッケージがあるかどうかを確認し、ない場合、 TiUP はミラーからパッケージをダウンロードして実行します。
