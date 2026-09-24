---
title: TiDB Cloud CLI を使い始める
summary: TiDB Cloud CLI をインストールして設定し、その後ファイルシステムを作成して使用するか、TiDB Cloud Starter データベースを管理してクエリします。
---

# TiDB Cloud CLI を使い始める

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) は、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) インスタンスおよび [TiDB Cloud Filesystem 内のファイルシステム](/ai/ti/ti-overview.md#tidb-cloud-filesystem) を管理するためのコマンドラインツールです。対話的な利用と自動化の両方をサポートしており、コマンドのデフォルト出力形式は JSON です。

このガイドでは、TiDB Cloud CLI (`ti`) のインストールと設定を行い、その後 TiDB Cloud Starter または TiDB Cloud Filesystem を使った基本的なワークフローを完了する方法を説明します。CLI の概要、機能、サポートされるワークフローについては、[TiDB Cloud CLI (`ti`) の概要](/ai/ti/ti-overview.md) を参照してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 前提条件 {#prerequisites}

開始する前に、[TiDB Cloud コンソール](https://tidbcloud.com/) の [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) ページから TiDB Cloud API public キーと private キーを取得してください。これらのキーには、組織に対する `Organization Owner` アクセス権が必要です。

## Step 1. TiDB Cloud CLI をインストールする {#step-1-install-tidb-cloud-cli}

お使いのオペレーティングシステムに応じて、以下の手順で TiDB Cloud CLI をインストールします。

<SimpleTab>

<div label="macOS or Linux">

1. macOS または Linux で、次のコマンドを実行して TiDB Cloud CLI をインストールします。

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. 現在のシェルで `ti` を使えるようにし、確認します。

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"
    ti --version
    ```

3. 新しいターミナルでも `ti` を使えるようにするため、`export PATH="$HOME/.ti/bin:$PATH"` をシェルプロファイルに追加します。

    たとえば、`zsh` を使用している場合は、次のコマンドを実行します。

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

</div>

<div label="Windows PowerShell">

1. Windows PowerShell で、次のコマンドを実行して TiDB Cloud CLI をインストールします。

    ```powershell
    $script = "$env:TEMP\install-ti.ps1"
    iwr https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
    powershell -ExecutionPolicy Bypass -File $script -Yes
    ```

2. 現在の PowerShell セッションで `ti` を使えるようにし、確認します。

    ```powershell
    $env:Path = "$HOME\.ti\bin;$env:Path"
    ti --version
    ```

3. 新しい PowerShell セッションでも `ti` を使えるようにするため、ユーザーの `PATH` に `$HOME\.ti\bin` を追加します。

    ```powershell
    $tiBin = "$HOME\.ti\bin"
    [Environment]::SetEnvironmentVariable("Path", "$tiBin;$([Environment]::GetEnvironmentVariable('Path', 'User'))", "User")
    ```

</div>
</SimpleTab>

## Step 2. TiDB Cloud CLI を設定する {#step-2-configure-tidb-cloud-cli}

1. 対話型設定を実行します。

    ```bash
    ti configure
    ```

2. 次の情報を入力します。

    - CLI 操作のデフォルトリージョン。リージョンコード（`aws-us-west-2` など）で指定します。TiDB Cloud CLI がサポートするリージョンの一覧については、[サポートされるリージョン](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions) を参照してください。
    - TiDB Cloud API public キーと private キー。

3. 読み取り専用コマンドを実行し、保存した認証情報を使用して CLI が TiDB Cloud にアクセスできることを確認します。

    ```bash
    ti fs list-file-systems
    ```

    出力例:

    ```bash
    {
      "region_code": "aws-us-west-2",
      "file_systems": []
    }
    ```

## Step 3. ワークフローを選択する {#step-3-choose-a-workflow}

ニーズに応じて、以下のいずれかのワークフローに進みます。

- [オプション A: TiDB Cloud Filesystem](/ai/ti/ti-quick-start.md#option-a-tidb-cloud-filesystem)
- [オプション B: TiDB Cloud Starter](/ai/ti/ti-quick-start.md#option-b-tidb-cloud-starter)

### オプション A: TiDB Cloud Filesystem {#option-a-tidb-cloud-filesystem}

TiDB Cloud Filesystem は、ローカルマシン、CI ジョブ、サンドボックス、その他の一時的な環境で利用できる、永続的かつ共有可能なクラウドファイルシステムです。

以下の例では、ある環境でファイルシステムを作成し、同じ環境または別の環境からそれにアクセスする方法を示します。たとえば、AI エージェントのサンドボックス（タスクの後に破棄される可能性がある一時的な環境）からアクセスできます。

1. ローカルマシン、または TiDB Cloud API 認証情報が設定された別の環境で、ファイルシステムを作成し、その owner token を取得します。

    ```bash
    export TI_FS_TOKEN="$(ti fs create-file-system --display-name agent-workspace --wait --query fs_token --output text --region aws-us-west-2)"
    ```

    > **Tip:**
    >
    > このクイックスタートでは、簡単にするために、ファイルシステムの作成時に返される owner token を使用します。最小権限アクセスを実現するには、スコープ付きトークンを生成して、特定のパスと操作へのアクセスを制限できます。詳細については、[ファイルシステムトークンを管理する](/tidb-cloud-filesystem/manage-filesystem-tokens.md) を参照してください。

2. ファイルシステムを使用する環境で、前の手順の owner token を `TI_FS_TOKEN` として設定し、次のようにファイルシステムをローカルパスにマウントします。この環境は、ファイルシステムを作成した同じマシン、別のマシン、または AI エージェントのサンドボックスのいずれでもかまいません。

    ```bash
    export TI_FS_TOKEN="<owner-token>" # Skip this line if you are continuing in the same terminal as step 1, where TI_FS_TOKEN is already set.
    mkdir ~/mnt-test
    ti fs mount-file-system --mount-path ~/mnt-test --region aws-us-west-2
    echo 'Hello from TiDB Cloud Filesystem' >> ~/mnt-test/hello.txt
    ls -l ~/mnt-test/hello.txt
    ```

    マウント後は、標準的なローカルファイル操作を使用してファイルを扱うことができます。

3. その環境でマウントしたファイルシステムの使用が終わったら、アンマウントします。

    ```bash
    ti fs unmount-file-system --mount-path ~/mnt-test --region aws-us-west-2
    ```

    アンマウントするとローカルマウントは削除されますが、ファイルは TiDB Cloud Filesystem に残り、同じ環境または別の環境から再度アクセスできます。

### オプション B: TiDB Cloud Starter {#option-b-tidb-cloud-starter}

1. TiDB Cloud Starter インスタンスを作成し、その ID を保存します。

    ```bash
    export TI_DB_CLUSTER_ID="$(ti db create-db-cluster \
      --db-cluster-type starter \
      --db-cluster-name quickstart-db \
      --wait \
      --query id \
      --output text)"
    ```

2. SQL ユーザーを作成し、読み取り専用クエリを実行して接続を確認します。

    ```bash
    ti db create-db-sql-users \
      --db-cluster-id "$TI_DB_CLUSTER_ID"

    ti db execute-sql-statement \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --read-only \
      --sql "SELECT 1 AS ready" \
      --output text
    ```

    `ti db execute-sql-statement` コマンドは、HTTPS SQL API を介してクエリを実行します。出力には `ready = 1` が含まれます。

3. 接続文字列を生成します。

    ```bash
    export DATABASE_URL="$(ti db format-db-connection-string \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --read-write --query connection_string \
      --output text)"
    ```

## 次のステップ {#what-s-next}

- [TiDB Cloud CLI (`ti`) の概要](/ai/ti/ti-overview.md) を読んで、`ti` が何を管理するのか、またどのような場合に使用するのかを理解してください。
- タスクガイドに従って、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) または [TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) を管理してください。
- コマンドグループ、グローバルオプション、共通の CLI 動作については、[TiDB Cloud CLI (`ti`) コマンドリファレンス](/ai/ti/reference/ti-cli-reference.md) を参照してください。
- 複数のプロファイルや非対話型認証を設定するには、[TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md) を参照してください。
