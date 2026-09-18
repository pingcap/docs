---
title: TiDB Cloud Filesystem トークンを管理する
summary: TiDB Cloud Filesystem のアクセストークンをインポート、生成、スコープ設定、確認、無効化、更新、取り消しする方法を学びます。
---

# TiDB Cloud Filesystem トークンを管理する

Filesystem トークンを使用すると、TiDB Cloud API 認証情報を共有せずに、ユーザーや自動化処理に TiDB Cloud Filesystem へのアクセスを付与できます。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- オーナートークンの生成および TiDB Cloud 認証によるトークン管理を行うには、TiDB Cloud API 認証情報を設定し、Filesystem ID を取得します。
- スコープ付きトークンの生成または bearer 認証によるトークン管理を行うには、オーナー FS トークンを取得します。`--fs-token` で渡すか、`TI_FS_TOKEN` を設定するか、明示的に選択した Filesystem 用に保存されたローカルトークンを使用できます。

> **Note:**
>
> セキュリティリスクを避けるため、トークンの平文は秘密情報として扱ってください。トークンの作成およびローテーションのコマンドは、トークン発行時にのみ平文を返します。後からその平文を取得することはできません。

## 既存のトークンをインポートする {#import-an-existing-token}

`import-file-system-token` を実行すると、CLI はトークン形式を検証し、その中に埋め込まれた Filesystem ID を抽出し、リモートの stat リクエストを送信して接続性を確認し、トークンをローカルの認証情報ディレクトリに保存します。

```shell
ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
```

## トークンを生成する {#generate-a-token}

TiDB Cloud API 認証情報を使用して、別のオーナートークンを生成します。CLI は生成されたトークンをデフォルトではローカルに保存しないため、一度だけ返される平文レスポンスを安全に保存する必要があります。

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h > ./ci-token.json
```

CLI に生成したトークンをローカル保存させるには、`--store-locally` を追加します。この Filesystem に対して別のトークンがすでに保存されている場合は、`--replace` を使用します。

最小権限のアクセスを実現するには、オーナートークンからパスと操作が制限されたトークンを生成します。

```shell
ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --ttl 24h \
  --allow /workspace:read,list > ./scoped-token.json
```

## トークンの状態を確認および変更する {#inspect-and-change-token-status}

秘密情報を含まないトークンメタデータを一覧表示します。

```shell
ti fs list-file-system-tokens --file-system-id "<file-system-id>"
```

トークンを一時的に停止するには [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) を使用し、再び有効にするには [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) を使用します。

## トークンをローテーションまたは取り消しする {#rotate-or-revoke-a-token}

トークンをローテーションするには [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) を使用します。ローカルに保存されたトークンを更新すると、CLI はローカルの認証情報ファイルを自動的に更新します。`--fs-token` または `TI_FS_TOKEN` で渡されたトークンを更新すると、CLI は新しいトークンを保存せずにコマンド出力として返します。

> **Note:**
>
> refresh は冪等ではありません。リクエストが成功した可能性はあるもののレスポンスが失われた場合、古いトークンで再試行しないでください。代わりに、TiDB Cloud 認証情報を使用して新しいオーナートークンを生成してください。

トークンを完全に取り消すには [`delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md) を使用します。削除されたトークンがローカルに保存されているトークンと一致する場合、CLI はローカル認証情報を自動的に削除します。

> **Note:**
>
> アクティブなローカルマウントで使用中のトークンをローテーション、無効化、または削除する前に、[`drain-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount) を実行し、その後 [`unmount-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount) を実行してください。CLI は既知のアクティブなマウントを確認し、トークンがまだ使用中であれば操作を拒否します。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem を複数のマシン間で共有する](/ai/ti/guides/ti-share-filesystem-across-machines-example.md)
- [Agent Sandbox で TiDB Cloud Filesystem を使用する](/ai/ti/guides/ti-agent-sandbox-example.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
