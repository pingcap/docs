---
title: ファイルシステムトークンの管理
summary: ユーザーや自動化のアクセス制御のために、ファイルシステムトークンをインポート、作成、スコープ設定、確認、ローテーション、失効する方法を学びます。
aliases: ['/ja/ai/manage-filesystem-tokens']
---

# ファイルシステムトークンの管理

TiDB Cloud Filesystem では、TiDB Cloud API 認証情報を共有せずに、ファイルシステムトークンを使用してユーザー、アプリケーション、自動化にファイルシステムへのアクセスを付与できます。

- [owner token](/tidb-cloud-filesystem/filesystem-authorization.md#owner-tokens) は、ファイルシステムへのフルアクセスを付与します。
- [scoped token](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens) は、特定のパスと操作にアクセスを制限します。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- TiDB Cloud Filesystem 内の既存のファイルシステムにアクセスできること。まだ持っていない場合は、[コンソールによるクイックスタート](/tidb-cloud-filesystem/filesystem-quick-start-console.md) または [CLI によるクイックスタート](/tidb-cloud-filesystem/filesystem-quick-start.md) に従って作成してください。
- CLI 操作の場合は、[TiDB Cloud CLI をインストール](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli) してください。

CLI でトークンを一覧表示、有効化、無効化、または削除するには、`TI_FS_TOKEN` または `--fs-token` を通じて owner token を指定するか、明示的な `--file-system-id` とともに TiDB Cloud API 認証情報を使用します。これらの操作では、ローカルに保存されたトークンは自動的には使用されません。scoped token の生成では、ローカルに保存された owner token を使用できます。追加要件がある場合は、以下の各セクションで説明します。

> **Note:**
>
> ファイルシステムトークンは安全に保管してください。トークンを作成または更新すると、その平文は一度だけ返され、後から取得することはできません。

## 既存のトークンをインポートする {#import-an-existing-token}

TiDB Cloud コンソールでファイルシステムを作成したときに表示されるデフォルトの owner token を含め、すでにファイルシステムトークンを持っている場合は、その平文を安全なファイルに保存し、ローカルの CLI 認証情報ストアにインポートします。

```shell
ti fs import-file-system-token --from-file ./fs-token --region "<file-system-region>"
```

CLI はトークンを検証し、そこからファイルシステム ID を抽出し、接続性を確認して、トークンをローカルに保存します。トークンがまだ `TI_FS_TOKEN` から利用可能であれば、インポートしなくても CLI コマンドで使用できます。

## owner token を生成する {#generate-an-owner-token}

TiDB Cloud コンソールでは、ファイルシステム作成時に owner token が提供されます。追加の owner token を生成するには、CLI を使用します。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

TiDB Cloud コンソールは、ファイルシステム作成時にデフォルトの owner token を作成します。その平文は **Your File System is Ready!** ダイアログにのみ表示されます。

追加の owner token が必要な場合は、**CLI** タブを使用してください。

</div>

<div label="CLI" value="cli">

CLI でファイルシステムを作成すると、期限切れにならない owner token が返され、ローカルに保存され、以後のコマンドで使用されます。

別の信頼できる環境にフルアクセスが必要な場合は、追加の owner token を生成します。

追加の owner token を生成するには、TiDB Cloud API 認証情報を設定し、ファイルシステム ID を取得します。

トークンを生成し、一度だけ返される平文レスポンスを安全に保存します。

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h \
  --query fs_token \
  --output text > ./ci-token
```

`--query fs_token --output text` はトークン値のみを出力します。これは `import-file-system-token --from-file` が期待する形式です。これらのオプションを付けない場合、コマンドは完全な JSON レスポンスを書き出すため、そのファイルのインポートは `invalid FS token format` で失敗します。後でトークンを失効させるために必要なトークン ID は、`ti fs list-file-system-tokens` からいつでも取得できます。

CLI は、生成したトークンをデフォルトではローカルに保存しません。ローカルに保存するには、前述のコマンドに `--store-locally` を追加します。このファイルシステムに対して別のトークンがすでに保存されている場合は、`--replace` も追加してください。

</div>

</SimpleTab>

## scoped token を生成して委任する {#generate-and-delegate-a-scoped-token}

TiDB Cloud コンソールまたは TiDB Cloud CLI を使用して scoped token を生成し、それを別のユーザー、アプリケーション、またはエージェントに渡すことができます。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

トークンを特定のディレクトリに制限したい場合は、トークンを生成する前にそのディレクトリを作成してください。

1. TiDB Cloud コンソールで [**File Systems**](https://tidbcloud.com/filesystems) ページに移動し、クラウドプロバイダーとリージョンを選択してから、対象のファイルシステム名をクリックします。
2. ファイルシステムの概要ページで、左側のナビゲーションペインにある **Access Tokens** をクリックします。
3. 右上隅の **Create Token** をクリックします。
4. 以下の情報を入力してトークンを設定します。

    - **Token name**: トークン名を入力します。
    - **Access path (optional)**: トークンのアクセスを特定のディレクトリに制限するためのアクセスパスを指定します。パスを空のままにすると、トークンは `/` に適用されます。
    - **Expiration**: トークンの有効期限を選択します。デフォルトは 1 時間です。
    - **Permission**: トークンに必要な操作のみを選択します。詳細は [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens) を参照してください。

5. **Create** をクリックします。
6. 表示されたダイアログで、**Done** をクリックする前にトークンをコピーして安全に保管します。平文は一度しか表示されません。

受信側の環境には、トークンとファイルシステムのリージョンを渡してください。ディレクトリに制限されたトークンでマウントする場合は、CLI の `--remote-path` オプションをそのディレクトリに設定します。

</div>

<div label="CLI" value="cli">

信頼できるマシン上で、owner token を使用して scoped token を生成します。owner token は `--fs-token` または `TI_FS_TOKEN` で指定するか、選択したファイルシステム用にローカルに保存された owner token を使用します。

この例を使用する前に、リモートの `/workspace` ディレクトリが存在しない場合は作成してください。ローカルに保存された owner token を使用して、エージェントにそのディレクトリ内のファイルの読み取り、一覧表示、書き込み権限を付与します。

```shell
SCOPED_TOKEN="$(ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --subject report-agent \
  --ttl 24h \
  --allow /workspace:read,list,write \
  --query fs_token --output text)"
```

シークレットマネージャーを通じてトークンを転送します。受信側の環境では、scoped token とファイルシステムのリージョンを指定します。

```shell
export TI_FS_TOKEN="<scoped-token>"
export TI_REGION_CODE="<filesystem-region-code>"

ti fs list-files --path /workspace
```

`--allow` の値は `<path>:<comma-separated-operations>` 形式を使用します。サポートされる操作は `read`、`list`、`search`、`write`、`delete` です。`search` には `read` が必要です。この例では、トークンは `/workspace` 配下で `read`、`list`、`write` 操作を許可します。

このトークンでディレクトリをマウントするには、`--remote-path /workspace` を指定します。`/workspace` に制限されたトークンでは、ファイルシステムルート `/` をマウントできません。

scoped 権限と認証情報の選択の詳細については、[Authorization](/tidb-cloud-filesystem/filesystem-authorization.md) を参照してください。

</div>

</SimpleTab>

## トークンの状態を確認および変更する {#inspect-and-change-token-status}

TiDB Cloud コンソールまたは TiDB Cloud CLI を使用して、トークンの詳細を表示し、トークンを有効化または無効化できます。

> **Warning:**
>
> アクティブなマウントで使用されているトークンを無効化、ローテーション、または削除する前に、そのマウントに書き込みを行っているアプリケーションを停止し、正常にアンマウントしてください。CLI は既知のローカルマウントは検出できますが、他のマシン上のマウントは検出できません。トークンを変更する前に、それらのマシンと調整してください。詳細は [安全に終了する](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) を参照してください。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. TiDB Cloud コンソールで [**File Systems**](https://tidbcloud.com/filesystems) ページに移動し、クラウドプロバイダーとリージョンを選択してから、対象のファイルシステム名をクリックします。
2. ファイルシステムの概要ページで、左側のナビゲーションペインにある **Access Tokens** をクリックします。
3. **Access Tokens** ページでは、各トークンの ID、状態、アクセスパス、権限、有効期限、作成時刻を確認できます。
4. トークンを一時停止するには、対象トークンの行にある **...** をクリックし、**Deactivate** を選択します。無効化されたトークンを復元するには、**...** をクリックしてから **Activate** を選択します。

</div>

<div label="CLI" value="cli">

owner token のみを使用する環境では、以下のコマンドを実行する前に、`TI_FS_TOKEN` に owner token を、`TI_REGION_CODE` にファイルシステムのリージョンを設定します。管理用認証情報は、受信者に渡す scoped token とは分離して管理してください。scoped token では他のトークンを管理できません。

ファイルシステムトークンのシークレットではないメタデータを一覧表示します。

```shell
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --output text
```

出力にはトークンの平文は含まれません。owner token を失った場合は、TiDB Cloud API 認証情報を使用して置き換えを生成してください。トークンを一覧表示しても元のトークンを復元することはできません。

[`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) を使用してトークンを一時停止し、[`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) を使用して復元します。これらはコンソールの **Deactivate** と **Activate** に対応します。

owner token 認証では、これら 2 つのコマンドで変更できるのは scoped token のみです。owner token を有効化または無効化するには、TiDB Cloud API 認証情報を使用し、`--file-system-id` を指定し、`TI_FS_TOKEN` が API 認証情報を上書きしないように unset してください。そのリクエストでは `--fs-token` を指定しないでください。変更が反映されるまで約 10 秒待ってからアクセスを確認してください。

</div>

</SimpleTab>

## トークンをローテーションまたは失効する {#rotate-or-revoke-a-token}

トークンをローテーションするには、TiDB Cloud コンソールでは `refresh-file-system-token` 操作が提供されていないため、CLI を使用します。トークンを失効するには、CLI またはコンソールのいずれかを使用できます。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

TiDB Cloud コンソールでスコープ付きトークンを置き換えるには、必要なパス、権限、有効期限を指定して[新しいトークンを作成](#generate-and-delegate-a-scoped-token)します。古いトークンを廃止する前に、新しいトークンを配布して検証してください。次に、対象ファイルシステムの **Access Tokens** ページに移動し、古いトークンの行を見つけて **...** をクリックし、**Delete** を選択します。

owner トークンを置き換えるには、TiDB Cloud コンソールで古いトークンを削除する前に、[CLI でもう 1 つ owner トークンを生成](#generate-an-owner-token)してください。

</div>

<div label="CLI" value="cli">

ファイルシステムトークンをローテーションするには、[`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) を使用します。

ローカルに保存されたトークンを更新すると、CLI はローカル認証情報を自動的に更新します。`--fs-token` または `TI_FS_TOKEN` を通じて提供されたトークンを更新すると、CLI は新しいトークンをローカルに保存せず、コマンド出力で返します。

> **Note:**
>
> 更新リクエストがタイムアウトした場合、サービス側ではトークンがローテーションされていても、新しい値が返されていない可能性があります。古いトークンで再試行しないでください。TiDB Cloud API 認証情報を使用して、新しい owner トークンを生成してください。

トークンを廃止する前に、その置き換え用トークンを配布して検証してください。次に、トークン ID を指定して古いトークンを失効します。

```shell
ti fs delete-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-id "<token-id>"
```

削除されたトークンがローカルに保存されているトークンと一致する場合、CLI はローカル認証情報を自動的に削除します。トークンの変更が認可キャッシュ全体に反映されるまでには時間がかかることがあります。

owner トークンを無効化または失効しても、そこから生成されたスコープ付きトークンは自動的には失効されません。必要に応じて、それらのスコープ付きトークンも個別に確認して失効してください。

</div>

</SimpleTab>

## 次のステップ {#what-s-next}

- [ファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md)
- [自動化と AI エージェントのワークフローを確認する](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)