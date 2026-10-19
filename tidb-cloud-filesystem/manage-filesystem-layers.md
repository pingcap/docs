---
title: ファイルシステムのレイヤーとチェックポイントを管理する
summary: ファイルシステムのレイヤーを作成し、変更をチェックポイント化してフォークし、分離を検証し、作業をコミットまたは破棄する方法を学びます。
aliases: ['/ja/ai/manage-filesystem-layers']
---

# ファイルシステムのレイヤーとチェックポイントを管理する

TiDB Cloud Filesystem では、レイヤーは、コミットするまでファイルの変更をベースファイルシステムから分離します。チェックポイントを使用すると中間状態を保持でき、フォークを使用すると変更を独立して検証できます。基礎となる概念については、[レイヤーとチェックポイント](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) を参照してください。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- [TiDB Cloud CLI をインストールする](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 既存のディレクトリに対して `read,list,write,delete` 権限を持つオーナートークンまたはスコープ付きトークンを用意します。この例では、その配下に子ディレクトリを作成して削除します。
- ファイルシステムを選択し、そのトークンを `ti` から利用できるようにします。利用可能なアクセス方法については、[既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) を参照してください。
- Bash または Zsh を使用し、例の実行中は同じシェルを開いたままにします。

## レイヤーを作成する {#create-a-layer}

トークンのスコープ内にある既存のディレクトリを選択します。オーナートークンを使用する場合は `/` を使い、スコープ付きトークンを使用する場合は `/workspace` のように、そのトークンで許可されたディレクトリに置き換えてください。例用に一意な子ディレクトリを作成します。

```shell
parent_path="/"
base_path="${parent_path%/}/layer-example-$(date +%s)-$$"
ti fs create-directory --path "$base_path"
```

次に、レイヤーを作成します。

```shell
ti fs create-layer \
  --base-root-path "$base_path" \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

`--base-root-path` は、レイヤーがベースファイルシステムのどの部分にオーバーレイされるかを決定します。

現在の CLI で受け付けられる `--durability-mode` の値は `restore-safe` のみです。利用可能なすべてのオプションについては、[`create-layer` コマンドリファレンス](/ai/ti/reference/ti-fs-create-layer.md) を参照してください。

以降のコマンドで使用するため、返された `layer_id` を保存します。

```shell
layer_id="<returned-layer-id>"
```

一意でない可能性があるレイヤー名ではなく、ID を使用してください。

## レイヤーの変更を操作して確認する {#work-with-and-inspect-layer-changes}

返されたレイヤー ID を使用して、サンプルファイルをレイヤーに書き込みます。

```shell
printf 'Layer review proposal\n' | ti fs copy-file \
  --from-stdin \
  --to-remote "$base_path/proposal.md" \
  --layer-id "$layer_id"
```

レイヤーとその変更を確認します。

```shell
ti fs describe-layer --layer-id "$layer_id"
ti fs diff-layer --layer-id "$layer_id"
```

選択したファイルシステム内のすべてのレイヤーを一覧表示します。

```shell
ti fs list-layers --output text
```

コミットされていない変更はレイヤー内に残ります。レイヤーを選択しないファイル操作はベースファイルシステムにアクセスするため、未コミットの変更は表示されません。

`--layer-id` を受け取るのは `copy-file`、`find-files`、`search-file-content` のみです。`read-file`、`list-files`、`describe-file`、`delete-file`、`move-file`、`create-directory` は常にベースファイルシステムに対して動作します。レイヤー内のファイル内容を読み取るには、[書き込み可能なレイヤーをマウントする](#mount-a-writable-layer) で説明するようにレイヤーをマウントするか、[チェックポイントのファイル内容を検証する](#create-a-checkpoint) を参照してください。

> **Note:**
>
> `--layer-id` を指定した `copy-file` は再帰コピーをサポートしません。ディレクトリツリーをレイヤーにコピーするには、レイヤーを[マウント](#mount-a-writable-layer)して書き込み可能な FUSE マウントとして使用し、マウントパス経由でファイルをコピーしてください。
>
> 同じ書き込み可能レイヤーを複数のローカルパスに同時にマウントしないでください。既存のマウントを再利用するか、別の場所にマウントする前にアンマウントしてください。
>
> マウントコマンドでは `--layer-ref` でレイヤーを指定しますが、上記のファイルコマンドでは `--layer-id` を使用します。どちらも同じレイヤー識別子の値を受け付けます。

### 書き込み可能なレイヤーをマウントする {#mount-a-writable-layer}

ローカルツールを使用するには、[FUSE の前提条件](/tidb-cloud-filesystem/filesystem-mount.md#choose-a-mount-method) を満たしたうえでレイヤーをマウントします。WebDAV はレイヤーまたはチェックポイントをサポートしていません。

```shell
layer_mount="$(mktemp -d "$HOME/ti-fs-layer.XXXXXX")"
ti fs mount-file-system \
  --mount-path "$layer_mount" \
  --remote-path "$base_path" \
  --layer-ref "$layer_id" \
  --driver fuse
cat "$layer_mount/proposal.md"
```

想定される出力は `Layer review proposal` です。分離を検証するには、レイヤーを選択せずにベースファイルシステムから読み取ります。

```shell
ti fs read-file --path "$base_path/proposal.md"
```

レイヤーはまだコミットされていないため、not-found エラーになるはずです。ベース側でファイルが見える場合は、先に進む前に処理を止めてレイヤー選択を確認してください。

## チェックポイントを作成する {#create-a-checkpoint}

チェックポイントは、レイヤーの永続的な履歴内のある時点を保持します。

レイヤーに書き込み可能な FUSE マウントがある場合は、チェックポイントを作成する前に書き込みを停止し、開いているファイルを閉じて、マウントを drain してください。

```shell
ti fs drain-file-system \
  --mount-path "$layer_mount"
```

次に、チェックポイントを作成します。

```shell
ti fs create-layer-checkpoint \
  --layer-id "$layer_id" \
  --checkpoint-id seed \
  --label "before review"
```

チェックポイントのファイル内容を検証するには、別のローカルパスにマウントします。

```shell
checkpoint_mount="$(mktemp -d "$HOME/ti-fs-checkpoint.XXXXXX")"
ti fs mount-file-system \
  --mount-path "$checkpoint_mount" \
  --remote-path "$base_path" \
  --layer-ref "$layer_id" \
  --checkpoint-id seed \
  --driver fuse
cat "$checkpoint_mount/proposal.md"
ti fs unmount-file-system --mount-path "$checkpoint_mount"
```

想定される出力は `Layer review proposal` です。チェックポイントのマウントは読み取り専用です。読み取りがハングする場合は、[マウントのトラブルシューティング](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs) に従ってください。

> **Warning:**
>
> `ti` v0.2.6、およびバンドルされたランタイム `60b63d6` を使用する v0.2.7 のインストールでは、バックグラウンドプロセスが異常終了していても、チェックポイントのアンマウントで `unmounted` が返ることがあります。続行する前にマウントログを確認してください。シャットダウンが異常だった場合は、キャッシュを保持したままチェックポイントの内容を再検証してください。ログの場所とリカバリ手順については、[アンマウントは成功を返すが、マウントプロセスが異常終了する](/tidb-cloud-filesystem/filesystem-troubleshooting.md#unmount-returns-success-but-the-mount-process-exits-abnormally) を参照してください。

## レイヤーをフォークする {#fork-a-layer}

チェックポイントから独立して作業を続けたい場合は、新しい書き込み可能レイヤーをフォークします。そうでない場合は、[レイヤーの変更をコミットまたは破棄する](#commit-or-discard-layer-changes) に進んでください。

```shell
ti fs fork-layer \
  --parent-layer-ref "$layer_id" \
  --layer-name experiment \
  --checkpoint-id seed
```

フォークで返された `layer_id` は別に保存します。

```shell
forked_layer_id="<returned-forked-layer-id>"
```

フォークの固定された祖先チェーンを確認するには、次を実行します。

```shell
ti fs list-layer-chain --layer-ref "$forked_layer_id"
```

フォークが作成された後は、親レイヤーと子レイヤーで行った変更は互いに独立します。

## レイヤーの変更をコミットまたは破棄する {#commit-or-discard-layer-changes}

レイヤーに書き込み可能な FUSE マウントがある場合は、結果を選択する前に、書き込みプロセスを停止し、開いているファイルを閉じて、アンマウントしてください。

```shell
ti fs unmount-file-system \
  --mount-path "$layer_mount"
```

正常なアンマウントでは、保留中の書き込みは自動的にフラッシュされます。

> **Warning:**
>
> `ti` v0.2.6、およびバンドルされたランタイム `60b63d6` を使用する v0.2.7 のインストールでは、バックグラウンドプロセスが異常終了した場合でも、レイヤーのアンマウントが `unmounted` を返すことがあります。レイヤーをコミットまたは破棄する前にマウントログを確認してください。シャットダウンが異常だった場合は、キャッシュを保持し、必要なファイルを先に確認してください。ログの場所とリカバリ手順については、[アンマウントは成功を返すが、マウントプロセスが異常終了する](/tidb-cloud-filesystem/filesystem-troubleshooting.md#unmount-returns-success-but-the-mount-process-exits-abnormally) を参照してください。

結果を 1 つ選択します。**コミット** は変更をベースファイルシステムに適用し、**ロールバック** は変更を破棄します。コミットするには、次を実行します。

```shell
ti fs commit-layer --layer-id "$layer_id"
```

コミットが成功したら、ベースファイルシステムを通じて内容を確認します。

```shell
ti fs read-file --path "$base_path/proposal.md"
```

想定される出力: `Layer review proposal`。

コミットは、レイヤーの実効的な変更をベースファイルシステムに適用します。レイヤーが別のレイヤーをフォークして作成された場合でも、これをコミットしても変更は親レイヤーにはマージされません。

ベースファイルシステムに競合する変更が含まれている場合、コミットは自動マージされずに失敗することがあります。どのように進めるかを判断する前に、レイヤーを保持したまま、その変更内容とベースファイルシステムを確認してください。

変更を破棄する場合は、コミットの代わりに次のコマンドを実行します。

```shell
ti fs rollback-layer --layer-id "$layer_id"
```

ロールバックは現在のレイヤーの変更を破棄します。レイヤーを以前のチェックポイントにリセットするものではありません。チェックポイントから続行するには、そのチェックポイントから新しいレイヤーをフォークしてください。

## レイヤーを削除する {#delete-a-layer}

フォークを作成した場合は、親より先にそれを削除してください。

```shell
ti fs delete-layer --layer-ref "$forked_layer_id"
```

次に、親レイヤーを削除します。

```shell
ti fs delete-layer --layer-ref "$layer_id"
```

レイヤーを削除すると、そのレイヤーは放棄されますが、履歴のすべてが直ちに消去されるわけではありません。レイヤーにアクティブな子孫レイヤーがある場合、このコマンドはデフォルトで失敗します。

または、レイヤーとそのアクティブな子孫レイヤーをまとめて放棄するには、`--cascade` を使用します。

```shell
ti fs delete-layer \
  --layer-ref "$layer_id" \
  --cascade
```

`--cascade` は、子孫レイヤーも放棄する意図がある場合にのみ使用してください。

サンプルのマウントをアンマウントし、サンプルのレイヤーを削除した後、ベースディレクトリを削除します。

```shell
ti fs delete-file --path "${base_path:?Set the example directory first}" --recursive
ti fs describe-file --path "$base_path"
```

`describe-file` から not-found エラーが返ることを確認してください。アンマウントが成功した後、`rmdir "$layer_mount"` と `rmdir "$checkpoint_mount"` を使用して作成したローカルディレクトリを削除します。サンプルファイルを削除しても、放棄されたレイヤーの履歴が直ちに消去されるわけではありません。

## 次のステップ {#what-s-next}

- [ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)