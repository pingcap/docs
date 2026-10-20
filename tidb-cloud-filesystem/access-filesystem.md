---
title: 既存のファイルシステムにアクセスする
summary: 現在のマシン、別のマシン、CI ジョブ、またはエージェント環境から既存のファイルシステムにアクセスする方法を説明します。
---

# 既存のファイルシステムにアクセスする

TiDB Cloud Filesystem では、ローカルに保存されたトークン、または別のマシンや環境向けに提供されたトークンのいずれかを使用して、既存のファイルシステムにアクセスできます。

- 現在のマシンで TiDB Cloud CLI (`ti`) を使用してファイルシステムを作成した場合、またはそのトークンをインポートした場合、CLI は保存済みのトークンを使用できます。
- 別のマシン、CI ジョブ、またはエージェント環境で作業している場合は、その環境用のファイルシステムトークンとリージョンを指定します。

## 前提条件 {#prerequisites}

開始する前に、[TiDB Cloud CLI をインストール](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)し、ファイルシステムにアクセスできることを確認してください。オーナートークンとスコープ付きトークン、およびそれらの権限については、[認可](/tidb-cloud-filesystem/filesystem-authorization.md) を参照してください。

## 同じマシンでファイルシステムを引き続き使用する {#continue-using-a-file-system-on-the-same-machine}

現在のマシンで `ti` を使用してファイルシステムを作成した場合、または以前にそのトークンをインポートした場合、CLI にはすでにトークンがローカルに保存されています。

環境変数 `TI_FS_TOKEN` と `TI_REGION_CODE` は、ローカルに保存されたトークンとリージョンを上書きします。

これらの上書きをクリアしてから、トークンがローカルに保存されているファイルシステムを選択します。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_TOKEN TI_REGION_CODE
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:TI_REGION_CODE -ErrorAction SilentlyContinue
$env:TI_FS_FILE_SYSTEM_ID = "<file-system-id>"
```

</div>

</SimpleTab>

ファイルシステムのルートを一覧表示します。保存済みトークンが特定のディレクトリにスコープされている場合は、`/` をそのディレクトリのパスに置き換えてください。

```shell
ti fs list-files --path /
```

`TI_FS_FILE_SYSTEM_ID` を設定すると、現在のシェルで以降に実行するコマンドの対象ファイルシステムが選択されます。これは、ファイルシステムトークンを変更または失効させるものではありません。

または、個別のコマンドごとにファイルシステムを選択することもできます。

```shell
ti fs list-files --file-system-id "<file-system-id>" --path /
```

## 別の環境からファイルシステムにアクセスする {#access-a-file-system-from-another-environment}

別の環境では、トークンとリージョンを指定します。CI またはエージェントでは、シークレットマネージャーから `TI_FS_TOKEN` を注入し、各プロセスで `TI_REGION_CODE` を設定します。入力プロンプトはスキップし、以前のファイルシステム選択を解除するために `TI_FS_FILE_SYSTEM_ID` をクリアします。

対話型ターミナルでは、プロンプトでトークンを入力します。入力内容は表示されません。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_FILE_SYSTEM_ID
export TI_REGION_CODE="<filesystem-region-code>"
printf 'File system token: '
read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_FILE_SYSTEM_ID -ErrorAction SilentlyContinue
$env:TI_REGION_CODE = "<filesystem-region-code>"
$env:TI_FS_TOKEN = [System.Net.NetworkCredential]::new(
  "", (Read-Host "File system token" -AsSecureString)
).Password
```

</div>

</SimpleTab>

トークンはファイルシステムを識別します。ファイルアクセスのために、別途ファイルシステム ID、設定済みの CLI プロファイル、または TiDB Cloud API キーは必要ありません。

その後、トークンで許可されているコマンドを実行できます。例:

```shell
ti fs list-files --path "<allowed-path>"
```

スコープ付きトークンは、そのスコープに含まれるパスと操作にのみアクセスできます。別のユーザーまたは管理者からトークンを受け取った場合は、使用が許可されているパスと操作を確認してください。

別の環境用のトークンを作成する必要がある場合は、[ファイルシステムトークンの管理](/tidb-cloud-filesystem/manage-filesystem-tokens.md) を参照してください。

## ファイルシステムを切り替える {#switch-between-file-systems}

ローカルに保存されたトークン間で切り替えるには、トークンとリージョンの上書きをクリアし、ファイルシステム ID を変更します。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_TOKEN TI_REGION_CODE
export TI_FS_FILE_SYSTEM_ID="<another-file-system-id>"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:TI_REGION_CODE -ErrorAction SilentlyContinue
$env:TI_FS_FILE_SYSTEM_ID = "<another-file-system-id>"
```

</div>

</SimpleTab>

CLI は、選択したファイルシステム用に保存されているトークンとリージョンを使用します。`TI_FS_TOKEN` と `TI_REGION_CODE` はそれらの値を上書きするため、どちらか一方でも別のファイルシステムまたはリージョン向けの値が設定されたままだと不一致が発生します。

1 つのファイルシステムには複数のリモートトークンを持たせることができますが、各 CLI プロファイルには各ファイルシステムにつき最大 1 つの選択済みローカルトークンのみが保存されます。CLI が使用するファイルシステムまたはローカルトークンを変更しても、他のリモートトークンが無効化または失効されることはありません。

## 認証情報の選択 {#credential-selection}

ほとんどのワークフローでは、すべてのコマンドで毎回認証情報を指定するのではなく、上記のいずれかの方法を使用してください。

複数のトークンソースが利用可能な場合、`ti` は次の順序でトークンを選択します。

1. `--fs-token`
2. `TI_FS_TOKEN`
3. 選択したファイルシステム用にローカルに保存されたトークン

ファイルシステムと認証情報の選択ルールの完全な説明については、[TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md#file-system-credentials-and-remote-inventory) を参照してください。

## 次のステップ {#what-s-next}

- [ファイルとディレクトリを操作する](/tidb-cloud-filesystem/work-with-filesystem-data.md)
- [ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md)
- [ファイルシステムトークンの管理](/tidb-cloud-filesystem/manage-filesystem-tokens.md)