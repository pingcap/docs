---
title: Data Migration Configuration File Overview
summary: This document gives an overview of Data Migration configuration files.
---

# データ移行コンフィグレーションファイルの概要 {#data-migration-configuration-file-overview}

このドキュメントでは、DM (Data Migration) の構成ファイルの概要について説明します。

## DM プロセス構成ファイル {#dm-process-configuration-files}

-   `dm-master.toml` : DM-master プロセスを実行する構成ファイル。DM-master のトポロジ情報とログが含まれます。詳細については、 [DMマスターコンフィグレーションファイル](/dm/dm-master-configuration-file.md)を参照してください。
-   `dm-worker.toml` : DM-worker プロセスを実行する構成ファイル。DM-worker のトポロジー情報とログが含まれます。詳細については、 [DM-workerコンフィグレーションファイル](/dm/dm-worker-configuration-file.md)を参照してください。
-   `source.yaml` : MySQL や MariaDB などのアップストリーム データベースの構成。詳細については、 [アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

## DM 移行タスクの構成 {#dm-migration-task-configuration}

### データ移行タスクの作成 {#data-migration-task-creation}

次の手順を実行して、データ移行タスクを作成できます。

1.  [dmctl を使用してデータ ソース構成を DM クラスタにロードします。](/dm/dm-manage-source.md#operate-data-source) .
2.  [タスクコンフィグレーションガイド](/dm/dm-task-configuration-guide.md)の説明を参照して、構成ファイルを作成します`your_task.yaml` 。
3.  [dmctl を使用してデータ移行タスクを作成する](/dm/dm-create-task.md) .

### 重要な概念 {#important-concepts}

このセクションでは、いくつかの重要な概念について説明します。

| コンセプト       | 説明                                                                                    | コンフィグレーションファイル                                           |
| :---------- | :------------------------------------------------------------------------------------ | :------------------------------------------------------- |
| `source-id` | MySQL または MariaDB インスタンス、またはプライマリ - セカンダリ構造を持つ移行グループを一意に表します。 `source-id`の最大長は 32 です。 | `source.yaml`の`source_id` ;<br/> `source-id` `task.yaml` |
| DMマスターID    | DM マスターを一意に表します ( `dm-master.toml`の`master-addr`パラメーターによって)                           | `master-addr`の`dm-master.toml`                           |
| DMワーカーID    | DM-worker を一意に表します ( `dm-worker.toml`の`worker-addr`パラメーターによって)                        | `worker-addr`の`dm-worker.toml`                           |
