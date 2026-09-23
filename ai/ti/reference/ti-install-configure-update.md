---
title: TiDB Cloud CLI のインストール、設定、および更新
summary: TiDB Cloud CLI のリリースをインストールし、プロファイルを設定し、バージョンを確認し、更新を適用し、CLI をアンインストールします。
---

# TiDB Cloud CLI のインストール、設定、および更新

このガイドでは、TiDB Cloud CLI (`ti`) のインストールと設定、更新の確認と適用、必要に応じた CLI のアンインストールについて説明します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 前提条件 {#prerequisites}

TiDB Cloud CLI を設定するには、まず TiDB Cloud コンソールの [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) ページから TiDB Cloud API public キーと private キーを取得してください。

> **Note:**
>
> 以前に TiDB Cloud CLI `tdc` v0.1.x を使用していた場合は、`tdc` によって開始された file system または Vault のマウントをすべてアンマウントし、`ti` をインストールする前に [tdc から TiDB Cloud CLI への移行](/ai/ti/reference/ti-migrate-from-tdc.md) を確認してください。

## TiDB Cloud CLI をインストールする {#install-tidb-cloud-cli}

使用しているオペレーティングシステムに応じて、以下の手順で TiDB Cloud CLI をインストールしてください。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. macOS または Linux で、次のコマンドを実行して TiDB Cloud CLI をインストールします。

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. 現在のシェルで `ti` を使えるようにし、確認します。

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"
    ti --version
    ```

3. 新しいターミナルセッションでも `ti` を使えるようにするには、シェルプロファイルに追加します。たとえば、`zsh` を使用している場合は、次のコマンドを実行します。

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

    Bash を使用している場合は、同じ `export` コマンドを、ターミナルで使用される起動ファイルに追加してください。通常は Linux では `~/.bashrc`、macOS では `~/.bash_profile` です。

</div>

<div label="Windows PowerShell" value="windows-powershell">

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

3. 新しい PowerShell セッションでも `ti` を使えるようにするには、`$HOME\.ti\bin` をユーザーの `PATH` に追加します。

    ```powershell
    $tiBin = "$HOME\.ti\bin"
    [Environment]::SetEnvironmentVariable("Path", "$tiBin;$([Environment]::GetEnvironmentVariable('Path', 'User'))", "User")
    ```

</div>
</SimpleTab>

インストーラーはホームディレクトリに書き込みを行い、昇格された権限は必要ありません。

インストーラーは、匿名使用テレメトリーに関する通知と、オプトアウト方法も表示します。インストール時にテレメトリーの選択を行う必要はありません。詳細は、[匿名テレメトリー](/ai/ti/reference/ti-configuration-and-credentials.md#anonymous-telemetry) を参照してください。

## プロファイルを設定する {#configure-a-profile}

プロファイルとは、TiDB Cloud API public キー、private キー、およびリージョンコードの名前付きセットです。

このセクションでは、TiDB Cloud CLI 用のプロファイルを設定する方法を説明します。

### 対話形式で設定する {#configure-interactively}

デフォルトでは、`ti configure` はプロファイルの設定に必要な情報の入力を求めます。

```bash
ti configure
```

`ti configure` は、TiDB Cloud API public キー、private キー、およびデフォルトのリージョンコードの入力を求めます。CLI は、個別のコマンドで上書きしない限り、このリージョンをコマンド実行時に使用します。利用可能なリージョンについては、[サポートされているリージョン](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions) を参照してください。

このコマンドは入力形式をローカルで検証し、TiDB Cloud へのリクエストを行わずにプロファイルを保存します。認証情報は、TiDB Cloud にアクセスするコマンドを実行したときに検証されます。デフォルトプロファイルを変更するには、再度 `ti configure` を実行してください。名前付きプロファイルを変更するには、たとえば `ti configure --profile staging` のように、その名前を指定します。

### 名前付きプロファイルを設定する {#configure-a-named-profile}

`--profile` を指定して、名前付きプロファイルを設定します。

```bash
ti configure --profile staging
```

### 自動化向けに設定する {#configure-for-automation}

CI またはその他の非対話型環境では、環境変数の使用を推奨します。

```bash
TIDB_CLOUD_PUBLIC_KEY="<public-key>" \
TIDB_CLOUD_PRIVATE_KEY="<private-key>" \
TI_REGION_CODE="aws-us-east-1" \
ti configure --profile ci --non-interactive
```

`--tidb-cloud-public-key`、`--tidb-cloud-private-key`、および `--region-code` を指定することもできますが、シークレットを含むフラグはシェル履歴やプロセス一覧に残る可能性があります。

## プロファイルを選択し、そのリージョンを上書きする {#select-a-profile-and-override-its-region}

名前付きプロファイルを使用し、1 つのコマンドに対してのみそのデフォルトリージョンを上書きするには、グローバルオプションの `--profile` と `--region` を使用します。

```bash
ti --profile staging --region aws-us-west-2 db list-db-clusters --db-cluster-type starter
```

プロファイル、認証情報、およびリージョンの優先順位ルールの詳細については、[TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md) を参照してください。

## ヘルプの取得とバージョンの確認 {#get-help-and-check-the-version}

コマンドを確認するには `help` または `--help` を使用し、インストール済みバージョンを確認するには `--version` を使用します。

```bash
ti help
ti fs help
ti --version
```

コマンドグループと CLI の規約については、[TiDB Cloud CLI コマンドリファレンス](/ai/ti/reference/ti-cli-reference.md) を参照してください。

## TiDB Cloud CLI を更新する {#update-tidb-cloud-cli}

ファイルを変更せずに確認します。

```bash
ti update --check
```

自動化環境では、新しいバージョンが利用可能な場合に終了コード `1` を返します。

```bash
ti update --check --fail-if-update-available
```

更新内容を事前確認します。

```bash
ti update --dry-run
```

> **Note:**
>
> アクティブな file system または Vault のマウントがある場合は、`ti` と file system ランタイムが一緒に更新されるように、更新前にライターを停止してアンマウントしてください。例:
>
> ```bash
> ti fs unmount-file-system --mount-path <mount-path>
> ```
>
> Vault マウントの場合は、`ti fs-vault unmount-vault --mount-path <mount-path>` を使用します。詳細は、[ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) および [ファイルシステムの Vault シークレットを管理する](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md) を参照してください。

最新の更新を適用します。

```bash
ti update
```

特定のリリースをインストールします。

```bash
ti update --target-version <version>
```

更新コマンドは、ユーザー所有のインストールにおいて `ti` と `ti-drive9` の両方を置き換えます。保護された場所やパッケージマネージャー管理下の場所にあるインストールは変更しません。古い `/usr/local/bin` のインストールを `~/.ti/bin` に移行するには、インストーラーを一度実行してください。

## tdc v0.1.x から移行する {#migrate-from-tdc-v01-x}

`tdc` v0.1.x を一度も使用したことがない場合は、このセクションをスキップしてください。

以前に `tdc` v0.1.x を使用していた場合、`ti` は `~/.tdc/` から `~/.ti/` へ、サポートされているローカルプロファイル、認証情報、設定、および file system の状態を移行できます。`ti` をインストールする前に、`tdc` によって開始された file system または Vault のマウントをすべてアンマウントしてください。

移行される状態と除外される状態、ディレクトリ競合の解決、レガシー環境変数との互換性を含む完全な移行手順については、[tdc から TiDB Cloud CLI への移行](/ai/ti/reference/ti-migrate-from-tdc.md) を参照してください。

## TiDB Cloud CLI のアンインストール {#uninstall-tidb-cloud-cli}

アンインストールする前に、writer を停止し、アクティブな file system または Vault のマウントをすべてアンマウントしてください。

たとえば、マウントの種類に応じて次のコマンドを実行します。

```bash
# file system mount
ti fs unmount-file-system --mount-path <filesystem-mount-path>

# Vault mount
ti fs-vault unmount-vault --mount-path <vault-mount-path>
```

詳細は、[ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) および [ファイルシステムの Vault シークレットを管理する](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md) を参照してください。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. バイナリを削除します。

    ```bash
    rm -f "$HOME/.ti/bin/ti" "$HOME/.ti/bin/ti-drive9"
    ```

2. インストール時にシェルプロファイルへ追加した `~/.ti/bin` のエントリを削除します。

</div>

<div label="Windows PowerShell" value="windows-powershell">

1. バイナリを削除します。

    ```powershell
    Remove-Item "$HOME\.ti\bin\ti.exe", "$HOME\.ti\bin\ti-drive9.exe"
    ```

2. ユーザーの `PATH` から `$HOME\.ti\bin` を削除します。

    ```powershell
    $tiBin = "$HOME\.ti\bin"
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $newPath = (($userPath -split ";") | Where-Object { $_ -and $_ -ne $tiBin }) -join ";"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    ```

</div>
</SimpleTab>

### ローカル状態の削除 {#remove-local-state}

バイナリを削除しても、プロファイル、認証情報、file system の登録、DB SQL 認証情報、ログ、およびマウントロケーターは保持されます。

> **Note:**
>
> すべてのローカル TiDB Cloud CLI 状態を完全に削除する意図がある場合にのみ、`~/.ti/` を削除してください。ローカル状態を削除しても、リモートの TiDB Cloud Starter インスタンスや file system リソースは削除されません。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

macOS または Linux の場合:

```bash
rm -rf "$HOME/.ti"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

Windows PowerShell の場合:

```powershell
Remove-Item "$HOME\.ti" -Recurse -Force
```

</div>
</SimpleTab>

## 関連情報 {#see-also}

- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)