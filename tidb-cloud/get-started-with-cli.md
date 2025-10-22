---
title: TiDB Cloud CLI Quick Start
summary: TiDB Cloud CLI を使用してTiDB Cloudリソースを管理する方法を学習します。
---

# TiDB Cloud CLI クイックスタート {#tidb-cloud-cli-quick-start}

TiDB Cloudは、ターミナルから数行のコマンドでTiDB Cloudを操作できるコマンドラインインターフェース（CLI） [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli)提供しています。例えば、 `ticloud`使用して以下の操作を簡単に実行できます。

-   クラスターを作成、削除、一覧表示します。
-   クラスターにデータをインポートします。
-   クラスターからデータをエクスポートします。

> **注記：**
>
> TiDB Cloud CLI はベータ版です。

## 始める前に {#before-you-begin}

-   TiDB Cloudアカウントをお持ちであること。お持ちでない場合は、 [無料トライアルにサインアップ](https://tidbcloud.com/free-trial) 。

## インストール {#installation}

<SimpleTab>
<div label="macOS/Linux">

macOS または Linux の場合、次のいずれかの方法で`ticloud`インストールできます。

-   スクリプト経由でインストールする（推奨）

    ```shell
    curl https://raw.githubusercontent.com/tidbcloud/tidbcloud-cli/main/install.sh | sh
    ```

-   [TiUP](https://tiup.io/)経由でインストール

    ```shell
    tiup install cloud
    ```

-   手動でインストールする

    [リリース](https://github.com/tidbcloud/tidbcloud-cli/releases/latest)ページからコンパイル済みのバイナリをダウンロードし、インストール先の場所にコピーします。

-   GitHub Actionsにインストール

    GitHub Action で`ticloud`設定するには、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)使用します。

MySQLコマンドラインクライアントがインストールされていない場合はインストールしてください。パッケージマネージャーからインストールできます。

-   Debian ベースのディストリビューション:

    ```shell
    sudo apt-get install mysql-client
    ```

-   RPM ベースのディストリビューション:

    ```shell
    sudo yum install mysql
    ```

-   macOS:

    ```shell
    brew install mysql-client
    ```

</div>

<div label="Windows">

Windows の場合、次のいずれかの方法で`ticloud`インストールできます。

-   手動でインストールする

    [リリース](https://github.com/tidbcloud/tidbcloud-cli/releases/latest)ページからコンパイル済みのバイナリをダウンロードし、インストール先の場所にコピーします。

-   GitHub Actionsにインストール

    GitHub Actions で`ticloud`設定するには、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)使用します。

MySQLコマンドラインクライアントがインストールされていない場合は、インストールしてください。インストール手順については、 [Windows用MySQLインストーラ](https://dev.mysql.com/doc/refman/8.0/en/mysql-installer.html)の手順を参照してください。Windowsで`ticloud connect`起動するには、PATH環境変数に`mysql.exe`含むディレクトリを追加する必要があります。

</div>
</SimpleTab>

## クイックスタート {#quick-start}

[TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter) TiDB Cloudを使い始めるのに最適な方法です。このセクションでは、 TiDB Cloud CLIを使用してTiDB Cloud Starterクラスターを作成する方法を学びます。

### ユーザープロファイルを作成するか、 TiDB Cloudにログインしてください {#create-a-user-profile-or-log-into-tidb-cloud}

TiDB Cloud CLI を使用してクラスターを作成する前に、ユーザー プロファイルを作成するか、 TiDB Cloudにログインする必要があります。

-   [TiDB CloudAPIキー](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)でユーザープロフィールを作成します:

    ```shell
    ticloud config create
    ```

    > **警告：**
    >
    > プロファイル名には`.`含める**ことはできません**。

-   認証を使用してTiDB Cloudにログインします。

    ```shell
    ticloud auth login
    ```

    ログインに成功すると、OAuthトークンが現在のプロファイルに割り当てられます。プロファイルが存在しない場合は、トークンは`default`名前のプロファイルに割り当てられます。

> **注記：**
>
> 上記の2つの方法では、 TiDB Cloud APIキーがOAuthトークンよりも優先されます。両方利用可能な場合は、APIキーが使用されます。

### TiDB Cloud Starter クラスターを作成する {#create-a-tidb-cloud-starter-cluster}

TiDB Cloud Starter クラスターを作成するには、次のコマンドを入力し、CLI プロンプトに従って必要な情報を入力します。

```shell
ticloud serverless create
```

## TiDB CloudCLIを使用する {#use-the-tidb-cloud-cli}

利用可能なすべてのコマンドをビュー。

```shell
ticloud --help
```

最新バージョンを使用していることを確認してください。

```shell
ticloud version
```

そうでない場合は、最新バージョンに更新してください。

```shell
ticloud update
```

### TiUP経由でTiDB Cloud CLI を使用する {#use-the-tidb-cloud-cli-through-tiup}

TiDB Cloud CLI は、コンポーネント名が`cloud`である[TiUP](https://tiup.io/)からも利用できます。

利用可能なすべてのコマンドをビュー。

```shell
tiup cloud --help
```

`tiup cloud <command>`を付けてコマンドを実行します。例:

```shell
tiup cloud serverless create
```

TiUPによる最新バージョンへのアップデート:

```shell
tiup update cloud
```

## 次は何か {#what-s-next}

TiDB Cloud CLI のその他の機能については、 [CLIリファレンス](/tidb-cloud/cli-reference.md)ご覧ください。

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
