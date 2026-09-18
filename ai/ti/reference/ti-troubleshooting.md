---
title: TiDB Cloud CLI のトラブルシューティング
summary: TiDB Cloud CLI の認証、プロジェクト、Filesystem の選択、companion、クォータ、SQL ユーザー、マウント、中断されたクリーンアップ失敗を診断します。
---

# TiDB Cloud CLI のトラブルシューティング

このリファレンスを使用して、現在よくある TiDB Cloud CLI の障害を診断します。`--debug` は必要な場合にのみ追加してください。デバッグ出力では機密情報はマスクされますが、共有する前に必ず内容を確認してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## API 認証が失敗する {#api-authentication-fails}

症状としては、認証情報の欠落、Digest 認証の失敗、または権限拒否などがあります。

両方の環境変数がセットで設定されていることを確認してください。

```bash
test -n "$TIDB_CLOUD_PUBLIC_KEY"
test -n "$TIDB_CLOUD_PRIVATE_KEY"
```

保存済みの認証情報を使用する場合は、両方の変数を unset してから、プロファイルを確認してください。

```bash
unset TIDB_CLOUD_PUBLIC_KEY TIDB_CLOUD_PRIVATE_KEY
ti db list-db-clusters --db-cluster-type starter --profile default
```

API キーで認証自体は成功しても、コマンドが要求する権限を持っていない場合があります。その操作に必要なアクセス権を持つキーを使用してください。`ti configure` は TiDB Cloud に接続せずにローカル値を検証して保存するため、認証情報の失敗は最初にリモートコマンド実行時に現れます。

## Filesystem トークンが見つからない {#filesystem-token-is-missing}

クリーンなサンドボックスでは、トークンとリージョンを指定してください。`ti` はトークンから file system ID を導出します。

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
ti fs check-file-system
```

FS トークンは TiDB Cloud API private key ではありません。トークンが指定されている場合、`TI_FS_FILE_SYSTEM_ID` は任意です。別途配布された ID がトークンと一致することを `ti` に検証させたい場合にのみ設定してください。

トークンは分かっているが現在のマシンに保存されていない場合は、それをインポートしてから、導出された ID を選択してください。

```bash
# Store a known token without requiring TiDB Cloud API keys.
chmod 600 ./fs-token
ti fs import-file-system-token --from-file ./fs-token --region <filesystem-region-code>
ti fs list-files --file-system-id <file-system-id> --path /
```

既知のトークンがすべて失われた、または失効された場合は、TiDB Cloud API キーを使用して別のオーナートークンを生成してください。

```bash
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name recovery \
  --ttl 24h
```

新しい平文のトークンはレスポンスに一度だけ表示されます。安全に保管するか、`--store-locally` を追加して現在のマシンで選択してください。

## Filesystem トークンが拒否される {#filesystem-token-is-rejected}

データプレーンの HTTP 401 では、トークンが無効化されたのか、有効期限切れなのか、別のマシンで更新されたのか、または失効されたのかを区別できません。TiDB Cloud API キーを使用してリモートメタデータを確認してください。

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --include-expired \
  --output text
```

トークン名は一意ではありません。enable、disable、または delete 操作には、この出力にある不変の `token_id` を使用してください。トークンライフサイクルのメタデータなしで作成またはインポートされた古い認証情報は引き続き有効な場合がありますが、`ti` は対応する一覧行を安全に特定できないため、一致を推測することはありません。

enable、disable、delete、または refresh の後は、認証キャッシュが収束するまで約 10 秒待ってください。refresh が `fs.token_refresh_ambiguous` を返した場合、レスポンスが失われたとしてもサーバー側でトークンがローテーションされた可能性があります。結果は不明です。refresh がコミットされていなければ古いトークンは引き続き使える可能性がありますが、すでに無効になっている可能性もあります。コミット済みの refresh の置き換えトークンは、レスポンスが失われているため復元できません。古いトークンで refresh を再試行しないでください。代わりに、TiDB Cloud 認証情報を使用して独立したオーナートークンを生成してください。

トークンの変更操作で `fs.token_mount_active` が報告された場合は、エラー内の正確なマウントパスを使用してください。

```bash
ti fs drain-file-system --mount-path /path/to/workspace
ti fs unmount-file-system --mount-path /path/to/workspace
```

その後、トークン操作を再試行してください。別のマシン上のマウントはローカルからは見えないため、そのマシンとのローテーション調整は別途行ってください。

## Filesystem の選択がない {#filesystem-selection-is-missing}

TiDB Cloud API キーを使用して、設定済みリージョン内のリモートリソースを一覧表示し、1 つを明示的に選択してください。

```bash
ti fs list-file-systems --output text
ti fs list-files --file-system-id <file-system-id> --path /
```

または、現在のシェルで以降のコマンド用に Filesystem を選択します。

```bash
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

TiDB Cloud CLI は、ローカル認証情報の数から Filesystem を推測しないよう意図的に設計されています。これは認証情報が 1 つしかない場合も含みます。ID、または埋め込み ID を導出できる FS トークンを指定してください。

## Filesystem リージョンがサポートされていない {#filesystem-region-is-unsupported}

設定された TiDB Cloud リージョンが、インストール済みの TiDB Cloud CLI リリースに組み込まれている Filesystem エンドポイントのいずれにも含まれていない可能性があります。[現在の Filesystem リージョン](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions) と比較してください。有効なプロファイルまたはコマンドスコープの `--region` を使って配置先を変更してください。生のサーバー URL は設定しないでください。

## companion が見つからない、または互換性がない {#companion-is-missing-or-incompatible}

リリースインストーラーは、Filesystem コマンド用の companion runtime である `ti-drive9` を `ti` の隣に配置します。`ti-drive9` を直接呼び出すことはありません。TiDB Cloud CLI が companion の欠落を報告した場合は、現在のインストーラーを再実行してください。

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

`PATH` が期待する `ti` を解決していることを確認してください。

```bash
command -v ti
ti --version
```

任意のスタンドアロン Drive9 バイナリをその場所にコピーしないでください。

## Starter または Filesystem の作成がクォータに達する {#starter-or-filesystem-creation-reaches-quota}

クォータおよび容量エラーは、組織が無料の Starter 上限に達したことを意味する場合があります。新しく作成する前に、既存のリソースを一覧表示してください。

```bash
ti db list-db-clusters --db-cluster-type starter --output text
ti fs list-file-systems --output text
```

自動化を通すために無関係なリソースを削除しないでください。Starter の利用上限により、課金の設定が必要になる場合があります。

## SQL 認証情報が見つからない {#sql-credentials-are-missing}

対象のクラスターに対して、ユーザーを準備または修復してください。

```bash
ti db create-db-sql-users --db-cluster-id "<cluster-id>"
```

その後、明示的なロールを指定して再試行してください。

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT 1"
```

`~/.ti/db_users/<cluster-id>/credentials` を削除すると、ローカルパスワードも削除されます。認証情報を作り出すのではなく、create/repair コマンドを実行してください。

## マウントが準備完了にならない {#mount-does-not-become-ready}

バックグラウンドマウントが成功した場合、TiDB Cloud CLI の結果は出力されますが、Drive9 の起動メッセージは表示されません。起動が失敗またはタイムアウトした場合は、エラー内にある companion のログパスを確認してください。次の点を確認します。

- マウントパスが存在し、書き込み可能であること。
- 既存のマウントがそのパスを覆っていないこと。
- FS トークンとリージョンが有効であること。
- FUSE の前提条件または WebDAV helper がインストールされていること。
- リモートリージョンに到達可能であること。

macOS ではデフォルトで WebDAV を使用します。macFUSE をインストールした後に FUSE を要求するには、次を実行します。

```bash
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux では FUSE3 と `/dev/fuse` へのアクセスが必要です。Filesystem および Vault マウントは Windows ではサポートされていません。代わりに `ti fs` のデータプレーンコマンド、またはマウントを使わない Vault コマンドを使用してください。

## Ubuntu 26.04 は `/workspace` 配下での FUSE マウントを拒否します {#ubuntu-2604-rejects-a-fuse-mount-under-workspace}

Ubuntu 26.04 では、`fusermount3` に AppArmor プロファイルが適用されます。デフォルトのマウントパス許可リストには `/workspace` が含まれていないため、root ユーザーと非 root ユーザーの両方で次のエラーが発生することがあります。

```text
/usr/bin/fusermount3: mount failed: Permission denied
```

拒否されたことを確認するには、次を実行します。

```bash
sudo journalctl -k --since "10 minutes ago" |
  grep 'profile="fusermount3"'
```

`operation="mount"`、`name="/workspace/"`、`info="failed mntpnt match"` を含むエントリがあれば、この制限が原因です。代わりに `$HOME` または `/mnt` 配下にマウントしてください。

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace"
```

`/workspace` のオーナーやモードを変更しても、AppArmor は回避できません。パスを変更できない場合は、[TiDB Cloud Filesystem をマウントする](/ai/ti/guides/mount-filesystem.md#ubuntu-2604-mount-paths) で説明されているように、`/etc/apparmor.d/local/fusermount3` に `/workspace` 用の明示的なマウントおよびアンマウントルールを追加してください。

## プロセスクラッシュ後にマウントが無効になります {#mount-becomes-stale-after-a-process-crash}

companion が正常にアンマウントされないまま強制終了されると、FUSE アクセスで `EIO` または `Transport endpoint is not connected` が返されることがあります。開いているファイルを持つプロセスを停止してから、次を試してください。

```bash
ti fs unmount-file-system \
  --mount-path /path/to/workspace \
  --force
```

ロケーターが残っていない場合でもクリーンアップを成功扱いにしたいときは、`--ignore-absent` を使用します。強制的なクリーンアップでは、削除されたローカルディスク上にある保留中の書き込みのリカバリは保証されません。

## アンマウント時にビジーが報告されます {#unmount-reports-busy}

エディタ、作業ディレクトリがマウント内にあるシェル、その他の開いているファイルハンドルを閉じてから、再試行してください。

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
```

アンマウントでは、正常な FUSE drain が自動的に実行されます。`drain-file-system` を個別に実行しても、ファイルディスクリプタは閉じられず、busy なマウントも解消されません。これを使うのは、マウントをオンラインのままにして保留中の処理をフラッシュしたい場合だけにしてください。drain は WebDAV ではサポートされていません。

## 中断されたコマンドによってリソースが残ります {#an-interrupted-command-leaves-resources}

リソースを一覧表示し、自分のワークフローで作成されたものだけを特定してください。削除前に describe を使用します。

```bash
ti db describe-db-cluster --db-cluster-id "<cluster-id>"
ti fs describe-file-system --file-system-id "<file-system-id>"
```

サポートされているクリーンアップ内容を事前確認するには、次を実行します。

```bash
ti db delete-db-cluster --db-cluster-id "<cluster-id>" --dry-run
ti fs delete-file-system \
  --file-system-id "<file-system-id>" \
  --dry-run
```

## 問題を報告する {#report-a-problem}

TiDB Cloud CLI のバージョン、OS とアーキテクチャ、コマンド名、安定したエラーコード、および秘匿情報を除去したログを含めてください。API キー、FS または vault トークン、DB パスワード、機密データを含む SQL、またはファイル内容は絶対に含めないでください。問題の報告先は [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues) です。
