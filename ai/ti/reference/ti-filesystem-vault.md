---
title: TiDB Cloud Filesystem Vault CLI コマンドリファレンス
summary: シークレット、委任アクセス、監査イベント、プロセスインジェクション、およびマウントに関するすべての `ti fs-vault` コマンドのリファレンスです。
---

# TiDB Cloud Filesystem Vault CLI コマンドリファレンス

TiDB Cloud Filesystem でシークレットと委任アクセスを管理するには、`ti fs-vault` を使用します。

ほとんどのシークレット管理コマンドでは、`db-prod` のようにシークレットを名前で識別します。一方、`replace-secret` と `run-with-secret` では、正規の Vault パス `/n/vault/<secret-name>` を指定する必要があります。`/n/vault/` は Vault 名前空間のルートであるため、`/n/vault/db-prod` とシークレット名 `db-prod` は同じシークレットを指します。

## コマンド {#commands}

| コマンド | 説明 |
|---|---|
| [`create-secret`](/ai/ti/reference/ti-fs-vault-create-secret.md) | シークレットを作成します。 |
| [`replace-secret`](/ai/ti/reference/ti-fs-vault-replace-secret.md) | シークレットを置き換えます。 |
| [`read-secret`](/ai/ti/reference/ti-fs-vault-read-secret.md) | シークレットを読み取ります。 |
| [`list-secrets`](/ai/ti/reference/ti-fs-vault-list-secrets.md) | シークレットを一覧表示します。 |
| [`delete-secret`](/ai/ti/reference/ti-fs-vault-delete-secret.md) | シークレットを削除します。 |
| [`create-grant`](/ai/ti/reference/ti-fs-vault-create-grant.md) | シークレットへの制限付きアクセスを委任します。 |
| [`delete-grant`](/ai/ti/reference/ti-fs-vault-delete-grant.md) | 委任されたアクセスを取り消します。 |
| [`list-audit-events`](/ai/ti/reference/ti-fs-vault-list-audit-events.md) | Vault の監査イベントを一覧表示します。 |
| [`run-with-secret`](/ai/ti/reference/ti-fs-vault-run-with-secret.md) | シークレットをプロセスに注入します。 |
| [`mount-vault`](/ai/ti/reference/ti-fs-vault-mount-vault.md) | 読み取り専用の Vault ビューをマウントします。 |
| [`unmount-vault`](/ai/ti/reference/ti-fs-vault-unmount-vault.md) | Vault ビューをアンマウントします。 |

## 関連情報 {#see-also}

- [TiDB Cloud Filesystem Vault Secrets を管理する](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md)
- [TiDB Cloud Filesystem Vault シークレットを Agent に委任する](/ai/ti/guides/ti-vault-agent-secrets-example.md)
