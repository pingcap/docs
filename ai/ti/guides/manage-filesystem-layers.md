---
title: TiDB Cloud Filesystem のレイヤーとチェックポイントを管理する
summary: TiDB Cloud Filesystem のレイヤーを安全に作成、確認、フォーク、チェックポイント、ロールバック、コミット、パック、復元する方法を学びます。
---

# TiDB Cloud Filesystem のレイヤーとチェックポイントを管理する

レイヤーを使用すると、変更をコミットまたは破棄する前に、Filesystem のベースパス上で分離された変更を記録できます。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- `--file-system-id` を渡す、`TI_FS_FILE_SYSTEM_ID` を設定する、または Filesystem を識別する FS トークンを指定して、Filesystem を選択します。
- `--fs-token`、`TI_FS_TOKEN`、または選択した Filesystem 用に保存されているローカル認証情報を使用して、必要な読み取りまたは書き込み権限を持つ FS トークンを指定します。
- レイヤーがオーバーレイするデータのベースパスを選択します。

## レイヤーを作成して確認する {#create-and-inspect-a-layer}

```shell
ti fs create-layer \
  --base-root-path /workspace \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

返されたレイヤー ID を使用して、変更を書き込み、確認します。

```shell
ti fs copy-file \
  --from-local ./proposal.md \
  --to-remote /workspace/proposal.md \
  --layer-id "<layer-id>"

ti fs describe-layer --layer-id "<layer-id>"
ti fs diff-layer --layer-id "<layer-id>"
```

> **Note:**
>
> `--layer-id` を指定した `copy-file` は、再帰コピーをサポートしていません。ディレクトリツリーをレイヤーに投入するには、レイヤーを書き込み可能な FUSE マウントとしてマウントし、そのマウントパス経由でファイルをコピーしてください。

同じ書き込み可能レイヤーを、複数のローカルパスに同時にマウントしないでください。既存のマウントを再利用するか、別の場所にレイヤーをマウントする前にアンマウントしてください。

## チェックポイントを作成してレイヤーをフォークする {#create-a-checkpoint-and-fork-a-layer}

```shell
ti fs create-layer-checkpoint \
  --layer-id "<layer-id>" \
  --checkpoint-id seed \
  --label "before review"

ti fs fork-layer \
  --parent-layer-ref "<layer-id>" \
  --layer-name experiment \
  --checkpoint-id seed
```

`list-layer-chain` を使用して、フォークの固定された祖先チェーンを確認します。

```shell
ti fs list-layer-chain --layer-ref experiment
```

チェックポイントマウントは読み取り専用です。チェックポイントから作業を続けるには、そこから新しい書き込み可能レイヤーをフォークしてください。

## レイヤーでの作業を完了する {#finish-work-in-a-layer}

> **Warning:**
>
> 書き込み可能な FUSE マウントを持つレイヤーのチェックポイントを作成する前に、[`drain-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount) を実行してください。チェックポイントには、サービスに到達した変更のみが含まれます。レイヤーをロールバックまたはコミットする前に、drain を実行してから [`unmount-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount) を実行してください。CLI はこれらの手順を自動では実行しません。

レイヤーに対して、次のいずれかの操作を選択します。

- レイヤーをロールバックして変更を破棄する場合:

    ```shell
    ti fs rollback-layer --layer-id "<layer-id>"
    ```

- レイヤーをコミットして変更をベースパスに適用する場合:

    ```shell
    ti fs commit-layer --layer-id "<layer-id>"
    ```

> **Note:**
>
> 同じレイヤーに対して、`rollback-layer` と `commit-layer` の両方を続けて実行しないでください。

## ローカル状態を別のマシンに移動する {#move-local-state-to-another-machine}

FUSE マウントが write-back キャッシュを使用している場合、一部のデータがローカルのオーバーレイディレクトリに残ることがあります。このローカル状態を別のマシンに移動するには、明示的なリモートアーカイブパスにパックします。

```shell
ti fs pack-file-system \
  --mount-path /path/to/workspace \
  --archive-path /workspace-overlay.tar.gz
```

移動先のマシンでは、アーカイブをローカルオーバーレイルートに復元します。

```shell
ti fs unpack-file-system \
  --local-root /path/to/local-overlay \
  --remote-root /workspace \
  --mount-profile portable \
  --archive-path /workspace-overlay.tar.gz
```

移動先のマシンで Filesystem をマウントするときは、同じローカルオーバーレイルートを使用してください。pack と unpack のすべてのオプションについては、[`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) および [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) のリファレンスを参照してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem をマウントする](/ai/ti/guides/mount-filesystem.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
