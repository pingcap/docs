---
title: TiUP Overview
summary: Introduce the TiUP tool and its ecosystem.
---

# TiUPの概要 {#tiup-overview}

TiDB 4.0以降、パッケージマネージャーとしてのTiUPにより、TiDBエコシステム内のさまざまなクラスタコンポーネントの管理がはるかに簡単になります。これで、1行のTiUPコマンドだけで任意のコンポーネントを実行できます。

## TiUPをインストールします {#install-tiup}

ダーウィンとLinuxの両方のオペレーティングシステムに、1つのコマンドでTiUPをインストールできます。

{{< copyable "" >}}

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

このコマンドは、TiUPを`$HOME/.tiup`フォルダーにインストールします。インストールされたコンポーネントとそれらの操作によって生成されたデータもこのフォルダーに配置されます。このコマンドは、Shell `.profile`ファイルの`PATH`環境変数に`$HOME/.tiup/bin`を自動的に追加するため、TiUPを直接使用できます。

インストール後、TiUPのバージョンを確認できます。

{{< copyable "" >}}

```bash
tiup --version
```

> **ノート：**
>
> デフォルトでは、TiUPは使用法の詳細をPingCAPと共有して、製品を改善する方法を理解するのに役立ちます。共有される内容と共有を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。

## TiUPエコシステムの紹介 {#tiup-ecosystem-introduction}

TiUPは、TiDBエコシステムのパッケージマネージャーだけではありません。その究極の使命は、独自のエコシステムを構築することにより、誰**もがこれまでになく簡単に**TiDBエコシステムツールを使用できるようにすることです。これには、TiUPエコシステムを充実させるために追加のパッケージを導入する必要があります。

この一連のTiUPドキュメントでは、これらのパッケージの機能と使用方法を紹介しています。

TiUPエコシステムでは、TiUP自体のヘルプ情報を取得する次のコマンドなど、任意のコマンドに`--help`を追加することで、ヘルプ情報を取得できます。

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
  -B, --binary <component>[:version]   Print binary path of a specific version of a component <component>[:version]
                                       and the latest version installed will be selected if no version specified
      --binpath string                 Specify the binary path of component instance
  -h, --help                           help for tiup
      --skip-version-check             Skip the strict version check, by default a version must be a valid SemVer string
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

出力は長いですが、2つの部分にのみ焦点を当てることができます。

-   使用可能なコマンド
    -   インストール：コンポーネントのインストールに使用
    -   リスト：使用可能なコンポーネントのリストを表示するために使用されます
    -   アンインストール：コンポーネントをアンインストールするために使用されます
    -   更新：コンポーネントのバージョンを更新するために使用されます
    -   ステータス：コンポーネントの実行履歴を表示するために使用されます
    -   clean：コンポーネントの実行ログをクリアするために使用されます
    -   ミラー：公式ミラーからプライベートミラーのクローンを作成するために使用されます
    -   ヘルプ：ヘルプ情報を印刷するために使用されます
-   利用可能なコンポーネント
    -   遊び場：TiDBクラスタをローカルで開始するために使用されます
    -   クライアント：ローカルマシンのTiDBクラスタに接続するために使用されます
    -   クラスタ：実稼働環境用のTiDBクラスタのデプロイに使用されます
    -   ベンチ：データベースのストレステストに使用

> **ノート：**
>
> -   利用可能なコンポーネントの数は増え続けます。サポートされている最新のコンポーネントを確認するには、 `tiup list`コマンドを実行します。
> -   コンポーネントの利用可能なバージョンのリストも増え続けます。サポートされている最新のコンポーネントバージョンを確認するには、 `tiup list <component>`コマンドを実行します。

TiUPコマンドはTiUPの内部コードに実装され、パッケージ管理操作に使用されますが、TiUPコンポーネントはTiUPコマンドによってインストールされる独立したコンポーネントパッケージです。

たとえば、 `tiup list`コマンドを実行すると、TiUPは独自の内部コードを直接実行します。 `tiup playground`コマンドを実行すると、TiUPは最初に「playground」という名前のローカルパッケージがあるかどうかを確認し、ない場合は、TiUPがミラーからパッケージをダウンロードしてから実行します。
