---
title: CLI を使用して TiDB Cloud Filesystem を使い始める
summary: 永続的な TiDB Cloud ファイルシステムを作成し、ファイルの読み書きを行い、必要に応じてローカルマウント経由でアクセスする方法を学びます。
---

# CLI を使用して TiDB Cloud Filesystem を使い始める

[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) は、アプリケーション、自動化、AI エージェント向けの永続的で共有可能なクラウドファイルシステムです。ファイルは、それを作成したマシンやプロセスとは独立して利用可能な状態が維持されるため、セッションや環境をまたいでワークスペースを再利用できます。

このクイックスタートガイドでは、TiDB Cloud CLI を使用してファイルシステムを作成し、ファイルを書き込み・読み取りし、必要に応じてローカルディレクトリとしてマウントする方法を説明します。

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能やインターフェースは予告なく変更される場合があります。

## 前提条件 {#prerequisites}

開始する前に、[TiDB Cloud コンソール](https://tidbcloud.com/) の [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) ページから TiDB Cloud API の公開キーと秘密キーを取得してください。これらのキーには、組織に対する `Organization Owner` アクセス権が必要です。

すでに誰かからファイルシステムトークンを受け取っている場合は、リソースの作成をスキップして、[既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) に従ってください。

macOS および Linux では Bash または Zsh を、Windows では PowerShell を使用してください。チュートリアル全体を通して同じシェルを開いたままにしてください。エージェントがコマンドごとに新しいシェルを開始する場合は、環境変数と保存したパスの値を各シェルに渡してください。

## ステップ 1. TiDB Cloud CLI をインストールする {#step-1-install-tidb-cloud-cli}

使用するオペレーティングシステムを選択してください。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. TiDB Cloud CLI をインストールします。

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. `ti` をシェルで使えるようにし、バージョンを確認します。

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"

    ti --version
    ```

3. 新しいターミナルでも `ti` を使えるようにするには、シェルプロファイルに追加します。Zsh の場合は次のとおりです。

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    ```

    Bash の場合は、同じ `export` 行をターミナルが使用する起動ファイルに追加してください。一般的には Linux では `~/.bashrc`、macOS では `~/.bash_profile` です。

</div>

<div label="Windows PowerShell" value="windows-powershell">

1. TiDB Cloud CLI をインストールします。

    ```powershell
    $script = "$env:TEMP\install-ti.ps1"
    iwr https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
    powershell -ExecutionPolicy Bypass -File $script -Yes
    ```

2. `ti` を現在の PowerShell セッションで使えるようにし、バージョンを確認します。

    ```powershell
    $env:Path = "$HOME\.ti\bin;$env:Path"

    ti --version
    ```

</div>

</SimpleTab>

Windows での永続的な `PATH` 設定やその他のインストール方法については、[TiDB Cloud CLI のインストール、設定、および更新](/ai/ti/reference/ti-install-configure-update.md) を参照してください。

## ステップ 2. TiDB Cloud CLI を設定する {#step-2-configure-tidb-cloud-cli}

ファイルの保存先として使用する[サポートされるリージョン](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions)を選択します。たとえば `aws-us-west-2` です。無料利用枠では、1 リージョンあたり 1 つのファイルシステムを作成できます。組織ですでに 1 つ作成済みの場合は、それを[再利用する](/tidb-cloud-filesystem/access-filesystem.md)か、別のリージョンを選択するか、[支払い方法を追加](https://tidbcloud.com/org-settings/billing/payments)してください。

1. 対話形式の設定を実行します。

    ```bash
    ti configure
    ```

2. 次の情報を入力します。

    - 選択したリージョン
    - TiDB Cloud API の公開キーと秘密キー

CLI は認証情報とデフォルトリージョンをローカルに保存します。次のステップの作成コマンドでは、このリージョンが使用されます。

> **Tip:**
>
> CI やエージェントでは、代わりに非対話形式の設定を使用してください。シークレットマネージャーから `TIDB_CLOUD_PUBLIC_KEY` と `TIDB_CLOUD_PRIVATE_KEY` を注入し、`TI_REGION_CODE` を設定して、`ti configure --non-interactive` を実行します。詳細は、[自動化向けに設定する](/ai/ti/reference/ti-install-configure-update.md#configure-for-automation) を参照してください。

## ステップ 3. ファイルシステムを作成して使用する {#step-3-create-and-use-a-file-system}

1. ファイルシステムを作成します。

    ```bash
    ti fs create-file-system --display-name agent-workspace --wait
    ```

    次のステップで使用するため、返された `file_system_id` をコピーしてください。CLI はファイルシステムのオーナートークンとリージョンをローカルに保存するため、同じマシンでは再度トークンを入力する必要はありません。

    > **Note:**
    >
    > 別のマシンからファイルシステムにアクセスする必要がある場合は、返された `fs_token` と `region_code` も保存してください。オーナートークンはフルアクセス権を持ち、有効期限がないため、安全に保管してください。制限付きアクセスについては、[ファイルシステムトークンを管理する](/tidb-cloud-filesystem/manage-filesystem-tokens.md) を参照してください。

2. 新しいファイルシステムを選択します。`<file-system-id>` を返された `file_system_id` に置き換えてください。

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    ```bash
    export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    $env:TI_FS_FILE_SYSTEM_ID = "<file-system-id>"
    ```

    </div>

    </SimpleTab>

3. ディレクトリを作成し、サンプルファイルをアップロードして、読み戻します。

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    ```bash
    ti fs create-directory --path /quick-start
    printf 'Hello from TiDB Cloud Filesystem\n' | ti fs copy-file \
      --from-stdin --to-remote /quick-start/hello.txt
    ti fs read-file --path /quick-start/hello.txt
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    ti fs create-directory --path /quick-start
    "Hello from TiDB Cloud Filesystem" | ti fs copy-file `
      --from-stdin --to-remote /quick-start/hello.txt
    ti fs read-file --path /quick-start/hello.txt
    ```

    </div>

    </SimpleTab>

    `read-file` の想定出力は次のとおりです。

    ```text
    Hello from TiDB Cloud Filesystem
    ```

    これで、最初のファイルが TiDB Cloud Filesystem に保存されました。別の環境からアクセスするには、[既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) を参照してください。別のユーザー、アプリケーション、またはエージェントにアクセス権を付与するには、[ファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md) を参照してください。

## ステップ 4. ファイルシステムをマウントする（オプション） {#step-4-mount-the-file-system-optional}

アプリケーションでローカルファイルパスが必要な場合は、ファイルシステムをマウントします。Windows ではマウントはサポートされていません。Windows を使用している場合、または CLI アクセスのみが必要な場合は、[ステップ 5](#step-5-clean-up-the-example-optional) に進んでください。

1. マウント用の空のローカルディレクトリを作成します。

    ```bash
    mount_dir="$(mktemp -d "$HOME/ti-fs-quick-start.XXXXXX")"
    ```

2. 使用しているオペレーティングシステムに応じたコマンドで `/quick-start` ディレクトリをマウントします。

    <SimpleTab>

    <div label="macOS WebDAV">

    このコマンドは、macOS に組み込まれている WebDAV サポートを使用します。

    ```bash
    ti fs mount-file-system --remote-path /quick-start \
      --mount-path "$mount_dir" --driver webdav
    ```

    </div>

    <div label="Linux FUSE">

    Linux では `fuse3` パッケージと `/dev/fuse` へのアクセスが必要です。必要に応じて、マウントコマンドを実行する前に [FUSE ユーザースペースツールをインストールする](/tidb-cloud-filesystem/filesystem-mount-linux.md#install-fuse-userspace-tools) を参照してください。

    ```bash
    ti fs mount-file-system --remote-path /quick-start \
      --mount-path "$mount_dir" --driver fuse
    ```

    </div>

    </SimpleTab>

3. ローカルパスを使ってファイルを読み取ります。

    ```bash
    cat "$mount_dir/hello.txt"
    ```

    想定出力:

    ```text
    Hello from TiDB Cloud Filesystem
    ```

書き込みの検証とトラブルシューティングについては、[使用前にマウントを検証する](/tidb-cloud-filesystem/filesystem-mount.md#verify-a-mount-before-using-it) を参照してください。

## ステップ 5. サンプルをクリーンアップする（オプション） {#step-5-clean-up-the-example-optional}

ステップ 4 でディレクトリをマウントした場合は、それを使用しているアプリケーションを閉じてから、アンマウントし、空のローカルマウントディレクトリを削除します。

```bash
ti fs unmount-file-system --mount-path "$mount_dir"
rmdir "$mount_dir"
```

アンマウントに失敗した場合は、続行する前に [安全に終了する](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) を参照してください。

サンプルディレクトリとそのファイルを削除します。このコマンドは、サポートされているすべてのオペレーティングシステムで動作します。

```shell
ti fs delete-file --path /quick-start --recursive
```

ファイルシステムとそのトークンは、再利用できる状態のまま残ります。ファイルシステム全体を削除するには、[ファイルシステムを削除する](/tidb-cloud-filesystem/manage-filesystem-resources.md#delete-a-file-system) を参照してください。

## 次のステップ {#what-s-next}

- [既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) では、ローカルに保存された認証情報を再利用したり、別の環境から接続したりできます。
- [自動化向けに設定する](/ai/ti/reference/ti-install-configure-update.md#configure-for-automation) では、CI ジョブやエージェント用の CLI 認証情報を設定できます。
- [TiDB Cloud Filesystem でファイルシステムを管理する](/tidb-cloud-filesystem/manage-filesystem-resources.md) では、ファイルシステムの確認と管理を行えます。
- [ファイルシステムトークンを管理する](/tidb-cloud-filesystem/manage-filesystem-tokens.md) では、ファイルシステムアクセス用トークンの作成、確認、管理を行えます。
- [ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) では、ローカルディレクトリを通じてそのファイルにアクセスできます。
- [ファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md) では、同じファイルを別のマシン、ユーザー、アプリケーション、またはエージェントから利用できるようにできます。
- [ファイルシステムのレイヤーとチェックポイントを管理する](/tidb-cloud-filesystem/manage-filesystem-layers.md) では、ファイル変更の分離、確認、適用を行えます。