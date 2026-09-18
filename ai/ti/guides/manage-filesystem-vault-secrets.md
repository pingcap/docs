---
title: TiDB Cloud Filesystem Vault Secrets を管理する
summary: TiDB Cloud Filesystem Vault を使用して、シークレットを安全に保存、読み取り、委任、注入、監査、失効、およびマウントする方法を学びます。
---

# TiDB Cloud Filesystem Vault Secrets を管理する

TiDB Cloud Filesystem Vault を使用すると、シークレットを保存し、ユーザーまたはエージェントに対してスコープを限定し有効期限付きのアクセスを委任し、平文をディスクに書き込むことなく認証情報をプロセスに注入できます。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- `--file-system-id` を渡す、`TI_FS_FILE_SYSTEM_ID` を設定する、または Filesystem を識別する FS トークンを指定して、Filesystem を選択します。
- オーナー操作の場合は、`--fs-token`、`TI_FS_TOKEN`、または選択した Filesystem 用にローカルに保存された認証情報を通じて、オーナー FS トークンを指定します。

> **Note:**
>
> セキュリティリスクを避けるため、オーナートークンや委任されたトークンを表示、ログ出力、またはコミットしないでください。

## シークレットを作成して読み取る {#create-and-read-a-secret}

```shell
ti fs-vault create-secret \
  --secret-name db-prod \
  --field DB_URL=mysql://example \
  --field PASSWORD=@./password.txt

ti fs-vault read-secret --secret-name db-prod
```

> **Note:**
>
> デフォルトの JSON 形式を含むすべての `read-secret` 出力形式には、平文のシークレット値が含まれます。出力は意図したプロセスにのみ渡してください。

## 制限付きアクセスを委任する {#delegate-limited-access}

短期間有効な読み取り grant を作成し、そのトークンを取得します。

```shell
export TI_VAULT_TOKEN="$(ti fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m \
  --token-only)"
```

コマンドラインのトークンよりも `TI_VAULT_TOKEN` を使用することを推奨します。コマンドラインの値は、プロセス一覧やシェル履歴に残る可能性があるためです。

## シークレットをプロセスに注入する {#inject-a-secret-into-a-process}

CLI は、平文をディスクに書き込むことなく、子プロセスに対してシークレットフィールドを環境変数として注入できます。次のコマンドを実行すると、CLI はシークレットを読み取り、各フィールドを環境変数（たとえば `DB_URL`、`PASSWORD`）として設定し、自身の認証用環境変数を子プロセスから削除してから、指定されたコマンドを実行します。

```shell
ti fs-vault run-with-secret --secret-path /n/vault/db-prod -- <command>
```

平文をディスクに書き込むよりも、プロセス注入を推奨します。

`run-with-secret` によって注入されるフィールド名は、`[A-Z_][A-Z0-9_]*` に一致する必要があります。いずれかのフィールド名がこのパターンに一致しない場合、またはいずれかのフィールド値にサポートされていない制御文字が含まれる場合、コマンドは注入全体を拒否します。注入する予定のフィールドを作成する際は、大文字の環境変数形式の名前を使用してください。

## アクセスを監査して失効する {#audit-and-revoke-access}

```shell
ti fs-vault list-audit-events \
  --secret-name db-prod \
  --agent-id deploy-agent \
  --since 24h \
  --limit 20

ti fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason rotated
```

失効すると、新たな操作の認可を防止できますが、プロセスがすでに読み取った値を消去することはできません。

## 読み取り専用の Vault ビューをマウントする {#mount-a-read-only-vault-view}

macOS または FUSE をサポートする Linux では、Vault シークレットの読み取り専用 FUSE ビューをマウントできます。CLI はマウントを作成し、マウントパス配下のファイルとしてシークレットフィールドを提供します（たとえば、`/path/to/vault/db-prod/DB_URL`）。

マウントする前に、`TI_VAULT_TOKEN` を委任された Vault トークンに設定します。たとえば、[制限付きアクセスを委任する](#delegate-limited-access) で作成したトークンを使用できます。マウントコマンドには、`TI_VAULT_TOKEN` または `--vault-token` のいずれかが必要です。

```shell
mkdir -p /path/to/vault
ti fs-vault mount-vault \
  --mount-path /path/to/vault
```

アンマウントする前に、マウントを使用しているすべてのプロセスを停止してください。

```shell
ti fs-vault unmount-vault --mount-path /path/to/vault
```

Vault マウントは Windows では利用できません。シークレットの直接読み取りとプロセス注入には、マウントは不要です。

## セキュリティに関する推奨事項 {#security-recommendations}

- フィールドスコープは可能な限り最小にし、TTL は実用上可能な限り短くしてください。
- 委任されたトークンを CLI 設定や操作ログに保存しないでください。
- タスク完了後は grant を失効してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem Vault Secrets をエージェントに委任する](/ai/ti/guides/ti-vault-agent-secrets-example.md)
- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
