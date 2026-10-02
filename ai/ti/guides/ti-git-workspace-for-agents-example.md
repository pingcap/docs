---
title: TiDB Cloud Filesystem 上でエージェント向けの Git ワークスペースを準備する
summary: 大規模な Git リポジトリのダウンロードが完了する前にエージェントタスクを開始し、マシンを削除する前に作業を保持する方法を学びます。
---

# TiDB Cloud Filesystem 上でエージェント向けの Git ワークスペースを準備する

大規模なリポジトリのダウンロードが完了する前にエージェントタスクを開始します。一時的なマシン上のエージェントがすぐにファイルを調査または編集する必要がある場合は、バックグラウンド hydration を有効にした blobless Git ワークスペースを使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 仕組み {#how-it-works}

`ti fs-git clone-git-workspace --blobless --hydrate background` は Git ワークスペースを登録し、すべてのクリーンブロブのダウンロードが完了する前にそのファイルツリーを公開します。`ti` が残りのクリーンなファイル内容をダウンロードしてローカル Git オブジェクトデータベースにデータを格納している間に、エージェントは作業を開始できます。hydration と呼ばれるこのバックグラウンドプロセスにより、繰り返し発生するオンデマンドフェッチが減ります。hydration が完了する前の読み取りでは、不足しているデータを取得するために Git の lazy fetch が使用されます。

置き換え後のエージェントランタイムは、登録済みのワークスペースにアクセスできます。元のマシンを破棄する前に、以下のクリーンアップガイダンスで説明されているように、ローカル Git 履歴を保持してください。ファイルの編集には通常のツールを使用し、コミット、フェッチ、プッシュには Git コマンドを使用します。

## 前提条件 {#prerequisites}

- ファイルシステムを選択します。
- Linux FUSE、または macFUSE を使用した macOS と明示的な `--driver fuse` を使用します。Git ワークスペースは、リモート Git ツリーとワークスペースの変更をマウントパスに統合するために FUSE に依存します。WebDAV マウントではこの統合は提供されません。
- Git をインストールし、リポジトリ認証を設定します。

## ステップ 1. ワークスペースをマウントする {#step-1-mount-a-workspace}

```bash
mkdir -p /path/to/workspace
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse \
  --mount-profile coding-agent
```

## ステップ 2. ワークスペースを作成し、バックグラウンドで hydrate する {#step-2-create-the-workspace-and-hydrate-in-the-background}

```bash
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate background
```

これでワークスペースツリーが利用可能になり、hydration はバックグラウンドで継続します。エージェントには通常のコマンドで作業を開始させます。

```bash
find /path/to/workspace/tidb -maxdepth 2 -type f | head
git -C /path/to/workspace/tidb status
```

決定的なベンチマークを実行する前、またはマウントを drain する前に、必要に応じて明示的に hydration の完了を待機できます。

```bash
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

## ステップ 3. エージェント worktree を作成する {#step-3-create-an-agent-worktree}

```bash
ti fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-agent-task \
  --branch-name agent-task
```

これでエージェントは通常のツールを使用できます。

```bash
git -C /path/to/workspace/tidb-agent-task status
```

worktree を削除する前に、必要な変更をコミットしてください。マシンを破棄する前に、プッシュまたはローカル Git メタデータの検証済みバックアップを使用して、[Git 履歴を保持して検証](/tidb-cloud-filesystem/manage-git-workspaces.md#preserve-work-before-leaving-a-machine)してください。

## クリーンアップ {#cleanup}

```bash
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-agent-task

ti fs unmount-file-system --mount-path /path/to/workspace
```

未コミットの変更を破棄してよい場合にのみ、worktree の削除で `--force` を使用してください。ファイルシステムのアンマウントでは自動的にグレースフルな drain が実行されます。アンマウントせずにリモート作業をフラッシュする必要がある場合にのみ、`ti fs drain-file-system` を個別に使用してください。

## セキュリティおよび運用上の注意 {#security-and-operational-notes}

- リポジトリ認証情報は `ti` ではなく Git によって管理されます。
- `coding-agent` マウントプロファイルは、パフォーマンスのために Git メタデータ、依存関係ディレクトリ、キャッシュ、ビルド出力、およびその他の生成ファイルをローカルマシン上に保持します。
- `coding-agent` プロファイルによってローカルに保持されるファイルは、一時的なマシンとともに消えます。ローカルコミットだけでは、マシン間で Git 履歴は保持されません。必要なコミットはプッシュして検証し、再構築できないその他のローカルファイルを保持するには、明示的な `--path` 値を指定して [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) を使用してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem Git CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-git.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
