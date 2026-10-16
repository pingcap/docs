---
title: ファイルシステムの Vault シークレットを管理する
summary: Vault シークレットの保存とローテーション、特定フィールドへの一時的なアクセス権の付与、プロセスでの利用、アクセス権の取り消し方法を学びます。
aliases: ['/ja/ai/manage-filesystem-vault-secrets']
---

# ファイルシステムの Vault シークレットを管理する

TiDB Cloud Filesystem では、通常のファイルシステムファイルの代わりに、ファイルシステム Vault を使用して認証情報やその他の機密値を保存できます。アプリケーション、自動化、またはエージェントには、ファイルシステム全体への広範なアクセス権を与えることなく、必要なフィールドにのみ一時的なアクセス権を付与できます。

委任されたワークフローは、それらのフィールドを読み取り、プロセスに注入したり、読み取り専用マウント経由でアクセスしたりできます。所有者はアクセスを監査し、取り消すことができます。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- [TiDB Cloud CLI をインストールする](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- テスト用ファイルシステムにアクセスできること。`ti fs-vault list-secrets` を実行して、`db-prod` シークレットがすでに存在するか確認してください。存在する場合は別の名前を選び、以下の名前、パス、付与スコープ内の `db-prod` を一貫して置き換えるか、別のテスト用ファイルシステムを使用してください。
- Bash または Zsh を使用すること。以下で作成する一時ディレクトリをクリーンアップ手順で使用できるよう、所有者のシェルは開いたままにしてください。
- ファイルシステムとその owner token を `ti` から利用できるようにすること。詳細は [既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) を参照してください。

owner token は、シークレットの作成と置換、grant の作成と取り消し、監査イベントの表示に使用されます。委任された Vault token は、その grant で許可されたシークレットアクセスのみを提供します。

owner token と委任された Vault token は、どちらも認証情報として扱ってください。ログ、ソース管理、共有ターミナル出力、コマンドライン引数に公開しないでください。

## シークレットを作成する {#create-a-secret}

Vault シークレットには、複数の名前付きフィールドを含めることができます。たとえば、データベースシークレットには接続 URL とパスワードを含めることができます。

まず各フィールド値をそれぞれ別のローカルファイルに書き込み、その後 `@` プレフィックスを付けてそれらのファイルを `create-secret` に渡します。各値は `read -r -s` で変数に読み込み、`printf '%s'` で書き込んでください。これにより、値がシェル履歴に残らず、末尾に改行も追加されません。`create-secret` と `replace-secret` は末尾が改行で終わる値も受け付けて成功を返しますが、後で [`run-with-secret`](#inject-a-secret-into-a-process) が `refusing to inject (EACCES)` としてその値の注入を拒否します。エディタや `echo` は末尾に改行を追加しますが、`printf '%s'` は追加しません。

```shell
umask 077
secret_dir="$(mktemp -d)"

printf 'DB_URL: ' >&2
read -r -s DB_URL_VALUE
printf '\n' >&2
printf '%s' "$DB_URL_VALUE" > "$secret_dir/DB_URL"

printf 'PASSWORD: ' >&2
read -r -s PASSWORD_VALUE
printf '\n' >&2
printf '%s' "$PASSWORD_VALUE" > "$secret_dir/PASSWORD"

unset DB_URL_VALUE PASSWORD_VALUE
```

`db-prod` という名前のシークレットを作成します。

```shell
ti fs-vault create-secret \
  --secret-name db-prod \
  --field "DB_URL=@$secret_dir/DB_URL" \
  --field "PASSWORD=@$secret_dir/PASSWORD"
```

`@` プレフィックスは、フィールド値をローカルファイルから読み取るよう `ti` に指示します。`--field DB_URL=mysql://example` のように値を直接書くと、シェル履歴やプロセス一覧に表示されるため、すべてのフィールドでこの方法を使うことを推奨します。

Vault コマンドの中には、`db-prod` のように名前でシークレットを識別するものがあります。一方、`replace-secret` や `run-with-secret` のように特定のシークレットパスを対象とするコマンドでは、代わりに完全な Vault パスを使用します。たとえば、`db-prod` の Vault パスは `/n/vault/db-prod` です。

### シークレット値を読み取る {#read-a-secret-value}

`read-secret` は平文のシークレット値を返します。値そのものが直接必要な場合にのみ使用し、その出力がログやその他の意図しない場所に書き込まれないようにしてください。

たとえば、`DB_URL` フィールドだけを読み取るには、次のようにします。

```shell
ti fs-vault read-secret \
  --secret-name db-prod \
  --field DB_URL \
  --format raw
```

アプリケーションがシークレットを必要とする場合は、平文の値を自分で読み取って扱うのではなく、[プロセスに注入する](#inject-a-secret-into-a-process)方法を優先してください。

## シークレットをローテーションする {#rotate-a-secret}

`replace-secret` は、値が変更されたフィールドだけでなく、シークレット内のすべてのフィールドを置き換えます。

`DB_URL` をローテーションするには、[シークレットを作成する](#create-a-secret) と同じ `read -r -s` と `printf '%s'` のパターンを使って、一時ディレクトリ内のファイルを上書きします。置換後もそのフィールドを保持できるよう、`PASSWORD` ファイルは残しておいてください。

```shell
printf 'New DB_URL: ' >&2
read -r -s DB_URL_VALUE
printf '\n' >&2
printf '%s' "$DB_URL_VALUE" > "$secret_dir/DB_URL"
unset DB_URL_VALUE

ti fs-vault replace-secret \
  --secret-path /n/vault/db-prod \
  --from-directory "$secret_dir"
```

ディレクトリ内の各ファイルは、置換後のシークレット内の 1 つのフィールドになります。ディレクトリに含まれていない既存フィールドは保持されません。`replace-secret` は末尾が改行で終わる値も受け付けて成功を返しますが、失敗は後で `run-with-secret` がその値の注入を拒否したときに現れます。そのため、ここでも `echo` やエディタではなく、引き続き `printf '%s'` を使用してください。

これらのローカルファイルはソース管理に含めず、不要になったら削除してください。詳細は [`replace-secret` リファレンス](/ai/ti/reference/ti-fs-vault-replace-secret.md) を参照してください。

## 制限付きアクセスを委任する {#delegate-limited-access}

ファイルシステム owner token を共有する代わりに、別のユーザー、アプリケーション、またはエージェントが必要とするシークレットフィールドだけに対して、短期間有効な grant を作成します。

たとえば、次の grant は `deploy-agent` に対して `DB_URL` フィールドのみの読み取りを 10 分間許可します。

```shell
ti fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m
```

このコマンドは、委任された Vault token と grant ID を返します。委任された token はシークレットを必要とするワークフローにのみ渡し、必要に応じて有効期限前に grant を取り消せるよう、grant ID は保持しておいてください。

委任されたシークレットを使用する別の環境では、token を `TI_VAULT_TOKEN` として利用できるようにします。また、`TI_FS_FILE_SYSTEM_ID` をファイルシステム ID に、`TI_REGION_CODE` をそのリージョンコードに設定してください。委任された Vault token だけではファイルシステムを識別できません。コマンド引数はシェル履歴やプロセス一覧に表示される可能性があるため、token をコマンドライン引数に直接書かないでください。

## シークレットをプロセスに注入する {#inject-a-secret-into-a-process}

アプリケーションが環境変数経由で認証情報を受け取れる場合は、`run-with-secret` を使用して、許可されたシークレットフィールドだけを子プロセスで利用可能にします。

```shell
ti fs-vault run-with-secret \
  --secret-path /n/vault/db-prod \
  -- <command>
```

許可された各シークレットフィールドは、同じ名前の環境変数になります。この例の `db-prod/DB_URL` grant では、`ti` は `DB_URL` を子プロセスに注入しますが、`PASSWORD` は注入しません。

`ti` が使用する Vault credential は子プロセスには渡されません。これにより、アプリケーションは平文の値をファイルに書き出すことなくシークレットを使用できます。

`run-with-secret` で使用するフィールド名は `[A-Z_][A-Z0-9_]*` に一致している必要があります。プロセスに注入する予定のシークレットには、大文字の環境変数形式のフィールド名を使用してください。

## シークレットを読み取り専用ファイルとしてマウントする {#mount-secrets-as-read-only-files}

アプリケーションが環境変数ではなくファイルとして認証情報を必要とする場合は、Linux または macOS 上の読み取り専用 FUSE マウントを通じて、許可された Vault フィールドを必要に応じて公開できます。

このオプションは、grant を取り消す前かつその token がまだ有効な間に使用してください。`mount-vault` は、owner token を保持しているかどうかにかかわらず、常に委任された Vault token を必要とします。owner token しか持っていない場合は、まず [制限付きアクセスを委任する](#delegate-limited-access) で説明したように、自分自身に対する grant を作成してください。ファイルシステム ID とリージョンを前述のとおり設定したうえで、委任された token を `TI_VAULT_TOKEN` として利用できるようにします。その後、ローカルのマウントディレクトリを作成して Vault をマウントします。

```shell
mkdir -p /path/to/vault

ti fs-vault mount-vault \
  --mount-path /path/to/vault
```

許可されたシークレットフィールドは、マウントパス配下のファイルとして利用できます。たとえば次のとおりです。

```text
/path/to/vault/db-prod/DB_URL
```

マウントにアクセスできるプロセスは許可されたシークレット値を読み取れるため、マウントへのアクセスは意図したワークロードのみに制限してください。

アンマウントする前に、マウントされたシークレットを使用しているプロセスを停止してください。

```shell
ti fs-vault unmount-vault \
  --mount-path /path/to/vault
```

Vault マウントには FUSE が必要であり、Windows では利用できません。シークレットの直接読み取りと `run-with-secret` にはマウントは不要です。

## アクセスを監査して取り消す {#audit-and-revoke-access}

所有者の環境に戻り、`deploy-agent` による `db-prod` への最近のアクセスを確認します。

```shell
ti fs-vault list-audit-events \
  --secret-name db-prod \
  --agent-id deploy-agent \
  --since 24h \
  --limit 20
```

委任されたアクセスが不要になったら、`create-grant` が返した grant ID を使って grant を取り消します。

```shell
ti fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason task-complete
```

grant を取り消すと、委任された token は新しい操作の認可に使えなくなります。ただし、プロセスがすでに読み取ったシークレット値を取り除くことはできません。

grant を廃止済みとして扱う前に、委任先の環境から取り消しを確認してください。`TI_VAULT_TOKEN` に委任された token を設定しているシェルで、認証キャッシュが更新されるまで約 10 秒待ってから、同じ token で許可されていた操作を再試行します。

```shell
ti fs-vault run-with-secret \
  --secret-path /n/vault/db-prod \
  -- printenv DB_URL
```

認証または認可エラー（たとえば `unauthorized`、`permission denied`、または `grant revoked`）が返ることを確認してください。コマンドがまだシークレット値を返す場合は、`delete-grant` に正しい grant ID を渡したことを確認し、キャッシュ間隔より長く待ってから再試行してください。ネットワークエラー、タイムアウト、または file system が見つからないエラーでは、取り消しは確認できません。明示的な認証失敗だけが確認になります。

grant が Vault マウント経由のアクセスを許可していた場合は、まず委任先の Vault マウントをアンマウントし、同じ token で再マウントしてください。稼働中の Vault マウントは委任先で認可状態を保持しており、読み取りのたびに grant を再確認しません。

## 例のクリーンアップ {#clean-up-the-example}

例の grant をアンマウントして取り消した後、テスト用の secret と一時ファイルを削除します。

```shell
ti fs-vault delete-secret --secret-name db-prod
rm "$secret_dir/DB_URL" "$secret_dir/PASSWORD"
rmdir "$secret_dir"
```

## セキュリティに関する推奨事項 {#security-recommendations}

- ワークフローで必要な secret フィールドにのみアクセスを許可し、実用上可能な限り短い TTL を使用してください。
- アプリケーションが環境変数を通じて認証情報を受け取れる場合は、`run-with-secret` を優先してください。
- owner トークンや delegated トークンを、ログ、ソース管理、またはコマンドライン引数に公開しないでください。
- タスクが完了したとき、またはアクセスが不要になったときは、grant を取り消してください。

## 次のステップ {#what-s-next}

- [File System Vault Secrets を Agent に委任する](/ai/ti/guides/ti-vault-agent-secrets-example.md)
- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)