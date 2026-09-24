---
title: TiDB Cloud Filesystem Git CLI コマンドリファレンス
summary: クローン、hydrate、リンクされた Git worktree の管理を行う各 `ti fs-git` コマンドのリファレンスです。
---

# TiDB Cloud Filesystem Git CLI コマンドリファレンス

`ti fs-git` は、マウントされた TiDB Cloud Filesystem パス上での Git ワークスペースのセットアップを高速化します。status、edit、add、commit、fetch、push には、引き続き通常の `git` コマンドを使用してください。

## コマンド {#commands}

| コマンド | 説明 |
|---|---|
| [`clone-git-workspace`](/ai/ti/reference/ti-fs-git-clone-git-workspace.md) | リポジトリをマウントされた file system パスにクローンします。 |
| [`hydrate-git-workspace`](/ai/ti/reference/ti-fs-git-hydrate-git-workspace.md) | 既存の fast または blobless ワークスペースに対して、クリーンな Git データを実体化します。 |
| [`add-git-worktree`](/ai/ti/reference/ti-fs-git-add-git-worktree.md) | ベースワークスペースからリンクされた worktree を作成します。 |
| [`remove-git-worktree`](/ai/ti/reference/ti-fs-git-remove-git-worktree.md) | リンクされた worktree を削除します。 |

## 関連情報 {#see-also}

- [TiDB Cloud Filesystem 上で Git ワークスペースを管理する](/tidb-cloud-filesystem/manage-git-workspaces.md)
- [TiDB Cloud Filesystem 上で Agents 用の Git ワークスペースを準備する](/ai/ti/guides/ti-git-workspace-for-agents-example.md)