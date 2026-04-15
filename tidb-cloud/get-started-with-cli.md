---
title: TiDB Cloud CLI Quick Start
summary: TiDB Cloud CLI を使用して、TiDB Cloud StarterおよびEssentialインスタンスを管理する方法を学びましょう。
---

# TiDB Cloud CLI クイックスタート {#tidb-cloud-cli-quick-start}

TiDB Cloud は、ターミナルから数行のコマンドでTiDB Cloudとやり取りできるコマンドラインインターフェイス (CLI) [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli)を提供しています。たとえば、 `ticloud`を使用して、次の操作を簡単に実行できます。

-   TiDB Cloud StarterまたはEssentialインスタンスの作成、削除、一覧表示を行います。
-   TiDB Cloud StarterまたはEssentialインスタンスにデータをインポートします。
-   TiDB Cloud StarterまたはEssentialインスタンスからデータをエクスポートします。

> **注記：**
>
> TiDB Cloud CLIはベータ版です。

## 始める前に {#before-you-begin}

-   TiDB Cloudアカウントを持っていること。お持ちでない場合は、[無料トライアルに登録する](https://tidbcloud.com/free-trial)。

## インストール {#installation}

<SimpleTab>
<div label="macOS/Linux">

macOS または Linux の場合、 `ticloud`次のいずれかの方法を使用してインストールできます。

-   スクリプト経由でインストールする（推奨）

    ```shell
    curl https://raw.githubusercontent.com/tidbcloud/tidbcloud-cli/main/install.sh | sh
    ```

-   [TiUP](https://tiup.io/)経由でインストール

    ```shell
    tiup install cloud
    ```

-   手動でインストール

    [リリース](https://github.com/tidbcloud/tidbcloud-cli/releases/latest)ページからコンパイル済みのバイナリをダウンロードし、インストール先の任意の場所にコピーしてください。

-   GitHub Actionsにインストールする

    GitHub Actions で`ticloud`を設定するには、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)を使用します。

MySQLコマンドラインクライアントがインストールされていない場合は、インストールしてください。パッケージマネージャーを使用してインストールできます。

-   Debianベースのディストリビューション：

    ```shell
    sudo apt-get install mysql-client
    ```

-   RPMベースのディストリビューション：

    ```shell
    sudo yum install mysql
    ```

-   macOS:

    ```shell
    brew install mysql-client
    ```

</div>

<div label="Windows">

Windowsの場合、 `ticloud`以下のいずれかの方法でインストールできます。

-   手動でインストール

    [リリース](https://github.com/tidbcloud/tidbcloud-cli/releases/latest)ページからコンパイル済みのバイナリをダウンロードし、インストール先の場所にコピーしてください。

-   GitHub Actionsにインストールする

    GitHub Actions で`ticloud`を設定するには、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)を使用します。

MySQL コマンドライン クライアントがインストールされていない場合はインストールしてください。インストール方法については[Windows 用 MySQL インストーラー](https://dev.mysql.com/doc/refman/8.0/en/mysql-installer.html)手順を参照してください。Windows で`ticloud connect`を起動するには、 `mysql.exe`を含むディレクトリが PATH 環境変数に含まれている必要があります。

</div>
</SimpleTab>

## クイックスタート {#quick-start}

[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、 TiDB Cloudを始めるための最適な方法です。このセクションでは、 TiDB Cloud CLIを使用してTiDB Cloud Starterインスタンスを作成する方法を学びます。

### TiDB Cloudでユーザープロファイルを作成するか、ログインしてください。 {#create-a-user-profile-or-log-into-tidb-cloud}

TiDB Cloud CLI を使用して TiDB TiDB Cloud Starterインスタンスを作成する前に、ユーザー プロファイルを作成するか、 TiDB Cloudにログインする必要があります。

-   [TiDB Cloud APIキー](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)を使用してユーザープロファイルを作成します。

    ```shell
    ticloud config create
    ```

    > **警告：**
    >
    > プロファイル名には`.`を含めて**はいけません**。

-   TiDB Cloudに認証情報を使用してログインしてください。

    ```shell
    ticloud auth login
    ```

    ログインが成功すると、現在のプロファイルにOAuthトークンが割り当てられます。プロファイルが存在しない場合は、 `default`という名前のプロファイルにトークンが割り当てられます。

> **注記：**
>
> 上記2つの方法では、 TiDB Cloud APIキーがOAuthトークンよりも優先されます。両方が利用可能な場合は、APIキーが使用されます。

### TiDB Cloud Starterインスタンスを作成する {#create-a-tidb-cloud-starter-instance}

TiDB Cloud Starterインスタンスを作成するには、次のコマンドを入力し、CLIプロンプトに従って必要な情報を入力してください。

```shell
ticloud serverless create
```

## TiDB Cloud CLIを使用する {#use-the-tidb-cloud-cli}

利用可能なすべてのコマンドをビュー。

```shell
ticloud --help
```

最新バージョンを使用していることを確認してください。

```shell
ticloud version
```

そうでない場合は、最新バージョンにアップデートしてください。

```shell
ticloud update
```

### TiUP経由でTiDB Cloud CLIを使用する {#use-the-tidb-cloud-cli-through-tiup}

TiDB Cloud CLI は[TiUP](https://tiup.io/)からも利用可能で、コンポーネント名は`cloud`です。

利用可能なすべてのコマンドをビュー。

```shell
tiup cloud --help
```

`tiup cloud <command>`を使用してコマンドを実行します。例:

```shell
tiup cloud serverless create
```

TiUPによる最新バージョンへのアップデート：

```shell
tiup update cloud
```

## 次は？ {#what-s-next}

TiDB Cloud CLI の機能をさらに詳しく調べるには、 [CLIリファレンス](/tidb-cloud/cli-reference.md)をチェックしてください。

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がありましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)ご報告ください。また、皆様からの貢献も歓迎いたします。
