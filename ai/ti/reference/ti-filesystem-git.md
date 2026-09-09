---
title: TiDB Cloud Filesystem Git CLI Command Reference
summary: Reference every `ti fs-git` command for cloning, hydrating, and managing linked Git worktrees.
---

# TiDB Cloud Filesystem Git CLI Command Reference

`ti fs-git` accelerates Git workspace setup on mounted TiDB Cloud Filesystem paths. Continue to use ordinary `git` commands for status, edit, add, commit, fetch, and push.

## Commands

| Command | Description |
|---|---|
| [`clone-git-workspace`](/ai/ti/reference/commands/fs-git/ti-fs-git-clone-git-workspace.md) | Clones a repository into a mounted Filesystem path. |
| [`hydrate-git-workspace`](/ai/ti/reference/commands/fs-git/ti-fs-git-hydrate-git-workspace.md) | Materializes clean Git data for an existing fast or blobless workspace. |
| [`add-git-worktree`](/ai/ti/reference/commands/fs-git/ti-fs-git-add-git-worktree.md) | Creates a linked worktree from a base workspace. |
| [`remove-git-worktree`](/ai/ti/reference/commands/fs-git/ti-fs-git-remove-git-worktree.md) | Removes a linked worktree. |

## See also

- [Manage Git Workspaces on TiDB Cloud Filesystem](/ai/ti/guides/manage-git-workspaces.md)
- [Prepare a Git Workspace for Agents on TiDB Cloud Filesystem](/ai/ti/reference/ti-git-workspace-for-agents-example.md)
