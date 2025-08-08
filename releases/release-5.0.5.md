---
title: TiDB 5.0.5 Release Note
summary: TiDB 5.0.5は2021年12月3日にリリースされました。TiKVのバグ修正では、複数のキーで呼び出された場合に「GcKeys」タスクが機能せず、コンパクションフィルタGCでMVCC削除情報が削除されない問題が修正されています。詳細はGitHubのIssue #11217をご覧ください。
---

# TiDB 5.0.5 リリースノート {#tidb-5-0-5-release-note}

発売日：2021年12月3日

TiDB バージョン: 5.0.5

## バグ修正 {#bug-fix}

-   TiKV

    -   `GcKeys`のタスクが複数のキーで呼び出された場合に動作しない問題を修正しました。この問題により、コンパクションフィルタGCがMVCC削除情報を削除しない可能性があります[＃11217](https://github.com/tikv/tikv/issues/11217)
