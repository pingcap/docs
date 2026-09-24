---
title: エージェントに File System Vault シークレットを委任する
summary: シークレットを保存し、1 つのフィールドへのアクセス権をエージェントに付与し、プロセスに注入し、アクセスを監査し、付与を取り消します。
---

# エージェントに File System Vault シークレットを委任する

このワークフローでは、file system オーナートークンや完全なシークレットを共有することなく、エージェントに 1 つのシークレットフィールドへの一時的なアクセス権を付与できます。エージェントが 1 つのタスクのために認証情報を必要とする一方で、その値をプロンプト、`.env` ファイル、またはサンドボックスイメージに保持すべきでない場合に使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 仕組み {#how-it-works}

file system オーナーはシークレットを一度だけ保存し、必要なフィールドにスコープを限定した短期間有効な grant を作成します。エージェントは委任された vault トークンのみを受け取り、許可された値を子プロセスに注入できます。オーナーは監査イベントを確認し、file system オーナー認証情報をローテーションしたり公開したりすることなく grant を取り消せます。

## このアプローチを使う理由 {#why-use-this-approach}

通常の環境変数やファイルでもシークレットを渡すことはできますが、スコープが限定され有効期限付きの委任や、アクセス監査証跡は作成できません。file system オーナートークンを共有すると、1 つのシークレットフィールドに必要な範囲を超える広いアクセス権も付与されます。別のクラウドシークレットマネージャーでも同様の制御は可能ですが、各サンドボックスごとに別の ID、ポリシー、統合経路が必要になります。

## 前提条件 {#prerequisites}

- オーナーアクセス権のある file system を選択します。
- `jq` をインストールします。
- 元のシークレット値を保護されたファイルに保存します。

## ステップ 1. シークレットを作成する {#step-1-create-a-secret}

```bash
ti fs-vault create-secret \
  --secret-name service-demo \
  --field ENDPOINT=https://service.example \
  --field API_TOKEN=@./api-token.txt
```

## ステップ 2. 最小権限の grant を作成する {#step-2-create-a-narrow-grant}

```bash
umask 077
set -o noclobber
ti fs-vault create-grant \
  --agent-id example-agent \
  --scope service-demo/ENDPOINT \
  --permission read \
  --ttl 10m \
  --label-hint example > ./vault-grant.json
set +o noclobber

export TI_VAULT_TOKEN="$(jq -r '.token' ./vault-grant.json)"
export GRANT_ID="$(jq -r '.grant_id' ./vault-grant.json)"
```

この保護されたファイルには、トークンを表示せずに 2 つのワンタイム値の両方が保存されます。トークンはシークレットマネージャーに保存し、grant を取り消せるように `GRANT_ID` は保持してください。

## ステップ 3. 委任されたフィールドを使用する {#step-3-use-the-delegated-field}

```bash
ti fs-vault read-secret \
  --secret-name service-demo \
  --field ENDPOINT \
  --format raw
```

許可されたフィールドをコマンドに注入します。

```bash
ti fs-vault run-with-secret \
  --secret-path /n/vault/service-demo \
  -- sh -c 'test -n "$ENDPOINT"'
```

`/n/vault/` プレフィックスは、完全なシークレットパスを受け付けるコマンドに対して Vault 名前空間を識別します。`service-demo` はステップ 1 で作成したシークレットを指します。`run-with-secret` は許可されたフィールドを読み取り、それらを子プロセス内の環境変数として設定し、その後 `--` の後ろのコマンドを実行します。このテストは、値を表示せずに `ENDPOINT` が存在する場合に正常終了します。すべての環境変数の値を表示するコマンドは使用しないでください。

## ステップ 4. 監査して取り消す {#step-4-audit-and-revoke}

```bash
ti fs-vault list-audit-events \
  --secret-name service-demo \
  --agent-id example-agent \
  --limit 20

ti fs-vault delete-grant \
  --grant-id "$GRANT_ID" \
  --revoked-by operator \
  --reason task-complete
```

ローカルトークンを unset します。

```bash
unset TI_VAULT_TOKEN
```

## クリーンアップ {#cleanup}

```bash
ti fs-vault delete-secret --secret-name service-demo
rm -f ./api-token.txt ./vault-grant.json
```

## セキュリティおよび運用上の注意 {#security-and-operational-notes}

- grant のスコープは、必要最小限のフィールドセットと、実用上最短の TTL に限定してください。
- 取り消されたトークンは新しい読み取りを認可できませんが、プロセスがすでに読み取った値を消去することはできません。
- プロセス一覧やシェル履歴に残る可能性があるため、シークレットをフラグで渡すことは避けてください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
- [TiDB Cloud CLI のリージョン、セキュリティ、および制限事項](/ai/ti/reference/ti-regions-security-and-limitations.md)
