---
title: TiDB Cloud Filesystem 上で Git ワークスペースを管理する
summary: マウントされた TiDB Cloud Filesystem 上で Git ワークスペースをクローン、hydrate、リンクされた worktree の作成、削除を行う方法を学びます。
---

# TiDB Cloud Filesystem 上で Git ワークスペースを管理する

マウントされた TiDB Cloud Filesystem 上で Git ワークスペースのセットアップを高速化するには `ti fs-git` を使用します。日常的な作業では、引き続き通常の Git コマンドを使用できます。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- FUSE を使用して [TiDB Cloud Filesystem をマウントする](/ai/ti/guides/mount-filesystem.md)。
- `--file-system-id` を渡す、`TI_FS_FILE_SYSTEM_ID` を設定する、または対象の Filesystem を識別する FS トークンを指定して、マウント済み Filesystem を選択します。Git ワークスペース権限を持つ FS トークンを指定してください。
- Git をインストールし、リポジトリの認証情報を個別に設定します。

## ワークスペースをクローンする {#clone-a-workspace}

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

大規模なリポジトリの場合は、`--blobless --hydrate background` を追加すると、ディレクトリツリーをすぐに利用できるようになります。CLI は、clone コマンドの実行完了後に、クリーンなファイル内容と Git オブジェクトをダウンロードするバックグラウンドプロセスを開始します。コマンドが終了する前に hydration を完了させる必要があるワークフローでは、`--hydrate sync` を使用します。

## 既存のワークスペースを hydrate する {#hydrate-an-existing-workspace}

ワークスペースを `--blobless` 付きで clone した場合は、`hydrate-git-workspace` を実行して不足している Git オブジェクトを明示的に取得できます。

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

hydration は、作業ツリーの変更を破棄することなく、リモートリポジトリから不足している blob データを取得します。

## リンクされた worktree を追加して使用する {#add-and-use-a-linked-worktree}

```shell
ti fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-feature \
  --branch-name feature-x
```

作成後は、リンクされた worktree 内で通常の Git コマンドを使用します。

## worktree を削除する {#remove-a-worktree}

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature
```

CLI はコミットされていない変更があるかどうかを確認し、worktree がダーティな場合は削除を拒否します。`--force` は、worktree 内のローカル変更を破棄してよいと判断した場合にのみ使用してください。

> **Note:**
>
> 一時的なマシンを終了する前に、必要な変更を保存し、不要な worktree を削除して、Filesystem を正常にアンマウントしてください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem 上でエージェント向けの Git ワークスペースを準備する](/ai/ti/guides/ti-git-workspace-for-agents-example.md)
- [TiDB Cloud Filesystem Git CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-git.md)
