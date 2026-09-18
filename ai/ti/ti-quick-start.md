---
title: TiDB Cloud CLI を使い始める
summary: TiDB Cloud CLI をインストールして設定し、その後 TiDB Cloud Filesystem を作成して使用するか、TiDB Cloud Starter データベースをクエリします。
---

# TiDB Cloud CLI を使い始める

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) は、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) インスタンスおよび [TiDB Cloud Filesystems](/ai/ti/ti-overview.md#tidb-cloud-filesystem) を管理するためのコマンドラインツールです。対話的な利用と自動化の両方をサポートしており、コマンドのデフォルト出力形式は JSON です。

このガイドでは、TiDB Cloud CLI (`ti`) のインストールと設定を行い、その後 TiDB Cloud Starter または TiDB Cloud Filesystem を使った基本的なワークフローを完了する方法を説明します。CLI の概要、機能、サポートされるワークフローについては、[TiDB Cloud CLI (`ti`) の概要](/ai/ti/ti-overview.md) を参照してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 前提条件 {#prerequisites}

開始する前に、[TiDB Cloud コンソール](https://tidbcloud.com/) の [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) ページから TiDB Cloud API public キーと private キーを取得してください。

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

    - CLI 操作のデフォルトリージョン。リージョンコード（`aws-us-east-1` など）で指定します。TiDB Cloud CLI がサポートするリージョンの一覧については、[サポートされるリージョン](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions) を参照してください。
    - TiDB Cloud API public キーと private キー。

3. 読み取り専用コマンドを実行し、保存した認証情報を使用して CLI が TiDB Cloud にアクセスできることを確認します。

    ```bash
    ti db list-db-clusters --db-cluster-type starter --output text
    ```

    出力例:

    ```bash
    {
      "profile": "default",
      "region_code": "aws-us-east-1",
      "credentials_stored": true
    }
    ```

## Step 3. ワークフローを選択する {#step-3-choose-a-workflow}

以下のいずれかのワークフローを完了してください。

- [Option A: Filesystem を作成して使用する](/ai/ti/ti-quick-start.md#option-a-create-and-use-a-filesystem)
- [Option B: TiDB Cloud Starter インスタンスを作成してデータベースをクエリする](/ai/ti/ti-quick-start.md#option-b-create-a-tidb-cloud-starter-instance-and-query-the-database)

### Option A: Filesystem を作成して使用する {#option-a-create-and-use-a-filesystem}

TiDB Cloud Filesystem は、ローカルマシン、CI ジョブ、サンドボックス、その他の一時的な環境で利用できる、永続的かつ共有可能なクラウドファイルシステムです。

1. Filesystem を作成し、準備完了まで待機して、サーバーによって割り当てられた ID を保存します。

    ```bash
    export TI_FS_FILE_SYSTEM_ID="$(ti fs create-file-system \
      --wait \
      --query file_system_id \
      --output text)"
    ```

    `ti` は Filesystem の認証情報をローカルに保存するため、以降のファイル操作で再度指定する必要はありません。

2. Filesystem にファイルを書き込み、その後ファイルを読み取ります。

    ```bash
    printf 'hello from ti\n' | ti fs copy-file \
      --from-stdin \
      --to-remote /hello.txt

    ti fs read-file \
      --path /hello.txt
    ```

    期待される出力:

    ```text
    hello from ti
    ```

3. Filesystem を削除します。

    ```bash
    ti fs delete-file-system \
      --file-system-id "$TI_FS_FILE_SYSTEM_ID"
    unset TI_FS_FILE_SYSTEM_ID
    ```

### Option B: TiDB Cloud Starter インスタンスを作成してデータベースをクエリする {#option-b-create-a-tidb-cloud-starter-instance-and-query-the-database}

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

3. TiDB Cloud Starter インスタンスを削除します。

    ```bash
    ti db delete-db-cluster \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --wait
    unset TI_DB_CLUSTER_ID
    ```

## 次のステップ {#what-s-next}

- [TiDB Cloud CLI (`ti`) の概要](/ai/ti/ti-overview.md) を読んで、`ti` が何を管理するのか、またどのような場合に使用するのかを理解してください。
- タスクガイドに従って、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) または [Filesystem リソース](/ai/ti/guides/manage-filesystem-resources.md) を管理してください。
- コマンドグループ、グローバルオプション、共通の CLI 動作については、[TiDB Cloud CLI (`ti`) コマンドリファレンス](/ai/ti/reference/ti-cli-reference.md) を参照してください。
- 複数のプロファイルや非対話型認証を設定するには、[TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md) を参照してください。
