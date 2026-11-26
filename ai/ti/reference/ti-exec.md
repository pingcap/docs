---
title: ti exec
summary: TiDB Cloud Filesystem に対してローカルで Filesystem をマウントせずにリモートコマンドを実行し、ワークスペースファイルを保持し、実行オプションを選択して、安全に障害に対処します。
---

# ti exec

`ti exec` は、Filesystem をローカルにマウントせずに、TiDB Cloud Filesystem に対してコマンドを実行します。出力はターミナルにストリーミングされ、リモートの終了ステータスは保持されます。

> **Note:**
>
> Runtime は AWS Oregon (`us-west-2`) と AWS N. Virginia (`us-east-1`) でのみ利用できます。CLI のリージョンコードとして `aws-us-west-2` または `aws-us-east-1` を使用してください。これらのリージョンのいずれかに Runtime が有効な Filesystem が必要です。`ti exec` の CLI サポートによって、サーバー側で Runtime が有効になるわけではありません。

> **Warning:**
>
> プレビュー機能である `ti exec` の検証はまだ完全ではありません。タイムアウトまたはキャンセル要求により、コマンドが停止したかどうかを確認できないまま、不明な結果 (`255`) が返されることがあります。コマンドを再実行するかどうかを判断する前に、結果を確認してください。

## 前提条件 {#prerequisites}

- 最新の `ti-drive9` companion を含む TiDB Cloud CLI **v0.2.11 以降**をインストールします。これより前の `ti` リリースには `ti exec` は含まれていません。インストール済みバージョンを確認するには `ti --version` を実行します。
- サポートされているリージョンで [Filesystem を作成](/ai/ti/reference/ti-fs-create-file-system.md) し、その ID とオーナートークンを控えておきます。
- その ID 用にローカルに保存されたトークンを使用するか、環境変数に `TI_FS_TOKEN` を設定します。引数にトークンを露出させないため、`--fs-token` より環境変数の使用を推奨します。委任された Vault トークンではコマンドを実行できません。パススコープトークンではサンドボックスをマウントできません。
- `ti exec --help` はローカルコマンドが存在することだけを確認します。companion やリモート Runtime は検証しません。両方が exec をサポートしている必要があります。

### 既存インストールのアップグレード {#upgrade-an-existing-installation}

アップグレード前に、ライターを停止し、Filesystem または Vault のマウントをすべてアンマウントしてください。macOS または Linux でユーザー所有の `ti` インストールを使用している場合は、最新リリースに更新し、バージョンを確認します。

```bash
ti update
ti --version
ti exec --help
```

`ti update` によって別バージョンの `ti` がインストールされる場合、`ti-drive9` companion も置き換えられます。`ti` がすでに要求されたバージョンである場合、アップデーターは companion を更新しません。macOS または Linux で古い companion を更新するには、シェルインストーラーを再実行してください。カスタムのインストールディレクトリを維持するには `--install-dir` を使用します。

Windows では、PowerShell インストーラーを再実行してください。インプレースでの自己更新はサポートされていません。インストール手順については、[TiDB Cloud CLI をインストールする](/ai/ti/reference/ti-install-configure-update.md#install-tidb-cloud-cli) を参照してください。

## 構文と実行 {#syntax-and-execution}

```text
ti exec [options] [--] command [arg...]
ti exec [options] 'shell command line'
```

`ti` のオプションはリモートコマンドの前に置きます。その後ろの引数（`--help` を含む）はリモートコマンドに属します。単一のシェルコマンドラインは `/bin/sh -c` によって解釈され、複数の引数は直接渡されます。

サーバーが実行バックエンドを選択します。軽量シェルエグゼキューターがサポートするコマンドは、サンドボックスを起動せずに実行できます。それ以外のコマンドでは、実行開始前にサンドボックスが使用されます。シェル構文だけではバックエンドは決まりません。一度開始したコマンドは、失敗後に別のバックエンドで再試行されることはありません。

Filesystem は `/workspace` で利用できます。`/workspace` の外側のファイルは一時的です。`--fresh` は Filesystem のデータを保持したまま新しいサンドボックスを開始します。`-w` は作業ディレクトリを選択しますが、そのディレクトリへのアクセスを制限するものではありません。

## 例: ファイルを処理して読み戻す {#example-process-and-read-back-a-file}

ローカルでは POSIX 互換シェル、リモートでは Python 3 が必要です。

```bash
export TI_REGION_CODE=aws-us-east-1
export TI_FS_FILE_SYSTEM_ID='<file-system-id>'
workdir="runtime-demo-$(date +%s)"
ti fs create-directory --path "/$workdir"

# Inspect the directory without permitting writes.
ti exec --read-only -w "$workdir" ls

# Process data remotely and save the result in the Filesystem.
ti exec -w "$workdir" python3 -c \
  'from pathlib import Path; Path("result.txt").write_text("total=42\n")'

# Start a new sandbox and read the saved result.
ti exec --fresh -w "$workdir" cat result.txt
```

想定される出力:

```text
total=42
```

個別に確認してから、例のディレクトリを削除します。

```bash
ti fs read-file --path "/$workdir/result.txt"
ti fs delete-file --path "/$workdir" --recursive
```

## オプション {#options}

| オプション | 説明 |
| --- | --- |
| `--file-system-id ID` | Filesystem を選択します。代わりに `TI_FS_FILE_SYSTEM_ID` を設定するか、ID を含むトークンを指定することもできます。 |
| `--fs-token TOKEN` | トークンを指定します。`TI_FS_TOKEN` の使用を推奨します。それ以外の場合は、選択した Filesystem のローカル保存トークンを使用します。 |
| `-w`, `--workspace PATH` | リモートの作業ディレクトリを選択します。デフォルトは、一致するローカル FUSE ディレクトリ、または Filesystem ルートです。 |
| `-C`, `--cwd DIR` | その作業ディレクトリ内のサブディレクトリを選択します。 |
| `-e`, `--env KEY[=VALUE]` | リモート変数を設定します。キーのみを指定した場合はローカル値をコピーします。繰り返し指定できます。 |
| `-t`, `--timeout DURATION` | `30s` や `10m` などの期限を設定します。サーバーがより短い制限を課す場合があります。 |
| `--fresh` | 既存のサンドボックスを再利用せず、新しいサンドボックスを開始します。 |
| `--layer REF` | レイヤー ID、名前、またはタグ参照を使用します。 |
| `--read-only` | 実行中の Filesystem への書き込みを防止します。 |
| `-v`, `--verbose` | 標準エラーに実行の詳細を表示します。 |

一致する `ti` 作成の FUSE マウント内では、`-w` を省略すると、保留中のローカル書き込みがアップロードされ、現在のディレクトリが追従されます。明示的に `-w` を指定した場合、先にローカル変更はアップロードされません。WebDAV マウントでは、`-w` を明示的に指定してください。

## 障害と制限事項 {#failures-and-limitations}

完了したコマンドは、その正確な終了ステータスを返します。最新の `ti-drive9` companion を使用している場合は、以下のステータスをエラーメッセージとあわせて解釈してください。

| 終了ステータス | 意味 |
| --- | --- |
| `124` | コマンドがタイムアウトし、停止されました。 |
| `125` | エグゼキューターが失敗しました。出力または書き込みが部分的である可能性があります。 |
| `126` | コマンドは実行可能ではありません。 |
| `127` | コマンドが見つかりませんでした。 |
| `130` | 実行前のキャンセル、確認済みのキャンセル、または 2 回目の Ctrl-C 後の切断です。このステータスだけでは、リモートコマンドが停止したことは証明できません。 |
| `255` | 結果が不明です。タイムアウトまたはキャンセル要求の後にも発生することがあります。 |

コマンド自体がこれらの数値を返すこともあるため、終了ステータスだけでは原因を特定できません。

- リモートの標準入力と対話型ターミナルはサポートされていません。`--output`、`--query`、`--dry-run` はサポートされていません。
- Ctrl-C を 1 回押すとキャンセルを要求し、確認を待ちます。もう一度押すと切断されます。その場合でもコマンドは実行中の可能性があります。
- 結果が不明な場合は、コマンドを再実行するか判断する前に Filesystem を確認してください。切断や実行レコードの欠如は、実行が停止したことの証明にはなりません。`ti exec` が自動的に再試行することはありません。