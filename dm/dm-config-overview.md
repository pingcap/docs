---
title: Data Migration Configuration File Overview
summary: このドキュメントでは、データ移行構成ファイルの概要を説明します。
---

# データ移行コンフィグレーションファイルの概要 {#data-migration-configuration-file-overview}

このドキュメントでは、DM (データ移行) の構成ファイルの概要を説明します。

## DMプロセス構成ファイル {#dm-process-configuration-files}

- `dm-master.toml` : DM-masterプロセスの実行に関する設定ファイル。DM-masterのトポロジ情報とログが含まれます。詳細については、 [DM-masterコンフィグレーションファイル](/dm/dm-master-configuration-file.md)を参照してください。
- `dm-worker.toml` : DM-workerプロセスの実行に関する設定ファイル。DM-workerのトポロジ情報とログが含まれます。詳細は[DM-workerコンフィグレーションファイル](/dm/dm-worker-configuration-file.md)を参照してください。
- `source.yaml` : MySQLやMariaDBなどの上流データベースの設定。詳細は[上流データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

## DM移行タスクの構成 {#dm-migration-task-configuration}

### データ移行タスクの作成 {#data-migration-task-creation}

データ移行タスクを作成するには、次の手順に従います。

1. [dmctl を使用してデータソース構成を DM クラスターにロードします](/dm/dm-manage-source.md#operate-data-source) 。
2. [タスクコンフィグレーションガイド](/dm/dm-task-configuration-guide.md)の説明を参考に設定ファイル`your_task.yaml`を作成します。
3. [dmctlを使用してデータ移行タスクを作成する](/dm/dm-create-task.md) 。

### 重要な概念 {#important-concepts}

このセクションでは、いくつかの重要な概念について説明します。

| 概念           | 説明                                                                          | コンフィグレーションファイル                                             |
| :---------- | :-------------------------------------------------------------------------- | :--------------------------------------------------------- |
| `source-id` | MySQLまたはMariaDBインスタンス、あるいはプライマリ/セカンダリ構造の移行グループを一意に表します。`source-id`の最大長は32です。 | `source_id` / `source.yaml` ;<br/> `task.yaml`中`source-id` |
| DM-masterID    | DM-masterを一意に表す（ `dm-master.toml`の`master-addr`パラメータによって）                      | `master-addr` / `dm-master.toml`                           |
| DM-workerID    | DM-workerを一意に表す（ `dm-worker.toml`の`worker-addr`のパラメータによって）                     | `worker-addr` / `dm-worker.toml`                           |
