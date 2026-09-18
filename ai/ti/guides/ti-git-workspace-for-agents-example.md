---
title: TiDB Cloud Filesystem 上でエージェント向けの Git ワークスペースを準備する
summary: 大規模な Git ワークスペースをすばやく利用可能にし、クリーンオブジェクトをバックグラウンドで hydrate して、完全なダウンロードが終わる前にエージェントが作業を開始できるようにします。
---

# TiDB Cloud Filesystem 上でエージェント向けの Git ワークスペースを準備する

このワークフローでは、エージェントタスクの開始におけるクリティカルパスから、大規模リポジトリのクローンを取り除きます。完全なダウンロードが完了する前に、一時的なエージェントが大規模リポジトリを調査または変更する必要がある場合に使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 仕組み {#how-it-works}

`ti fs-git clone-git-workspace --blobless --hydrate background` は、置き換え可能なエージェントランタイム間で共有できる Git ワークスペースを登録し、すべてのクリーン ブロブのダウンロードが完了する前にそのファイルツリーを公開します。このコマンドはすぐに戻るため、`ti` がバックグラウンドでクリーンツリーとローカル Git オブジェクトデータベースを hydrate している間に、エージェントはパスを調査して作業を開始できます。通常の clone とは異なり、初期オブジェクト転送はワークフロー全体をブロックしません。ネイティブの blobless partial clone のみを使う場合と異なり、バックグラウンド hydration により、エージェントのクリティカルパス上で繰り返し発生するオンデマンドフェッチを減らせます。hydration の完了前に到着した読み取りは、正確性を保つために引き続き Git の lazy fetch にフォールバックします。編集、commit、fetch、push は通常どおり Git が担当します。

## 前提条件 {#prerequisites}

- Filesystem を選択します。
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

worktree を削除する前に、必要な変更を commit または push してください。

## クリーンアップ {#cleanup}

```bash
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-agent-task

ti fs unmount-file-system --mount-path /path/to/workspace
```

未コミットの変更を破棄してよい場合にのみ、worktree の削除で `--force` を使用してください。Filesystem のアンマウントでは自動的にグレースフルな drain が実行されます。アンマウントせずにリモート作業をフラッシュする必要がある場合にのみ、`ti fs drain-file-system` を個別に使用してください。

## セキュリティおよび運用上の注意 {#security-and-operational-notes}

- リポジトリ認証情報は `ti` ではなく Git によって管理されます。
- `coding-agent` マウントプロファイルは、パフォーマンスのために Git メタデータ、依存関係ディレクトリ、キャッシュ、ビルド出力、およびその他の生成ファイルをローカルマシン上に保持します。
- `coding-agent` プロファイルによってローカルに保持されるファイルは、一時的なマシンとともに消えます。必要な Git の変更は commit または push し、再構築できないその他のローカルファイルを保持するには、明示的な `--path` 値を指定して [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) を使用してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem Git CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-git.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
