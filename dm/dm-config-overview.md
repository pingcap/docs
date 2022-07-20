---
title: Data Migration Configuration File Overview
summary: This document gives an overview of Data Migration configuration files.
---

# データ移行Configuration / コンフィグレーションファイルの概要 {#data-migration-configuration-file-overview}

このドキュメントでは、DM（データ移行）の構成ファイルの概要を説明します。

## DMプロセス構成ファイル {#dm-process-configuration-files}

-   `dm-master.toml` ：DMマスタープロセスを実行するための構成ファイル。トポロジー情報とDMマスターのログが含まれます。詳細については、 [DMマスターConfiguration / コンフィグレーションファイル](/dm/dm-master-configuration-file.md)を参照してください。
-   `dm-worker.toml` ：DM-workerプロセスを実行するための構成ファイル。トポロジー情報とDM-workerのログが含まれます。詳細については、 [DM-workerConfiguration / コンフィグレーションファイル](/dm/dm-worker-configuration-file.md)を参照してください。
-   `source.yaml` ：MySQLやMariaDBなどのアップストリームデータベースの構成。詳細については、 [アップストリームデータベースConfiguration / コンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

## DM移行タスクの構成 {#dm-migration-task-configuration}

### データ移行タスクの作成 {#data-migration-task-creation}

次の手順を実行して、データ移行タスクを作成できます。

1.  [dmctlを使用してデータソース構成をDMクラスタにロードします](/dm/dm-manage-source.md#operate-data-source) 。
2.  [タスクConfiguration / コンフィグレーションガイド](/dm/dm-task-configuration-guide.md)の説明を参照して、構成ファイル`your_task.yaml`を作成します。
3.  [dmctlを使用してデータ移行タスクを作成します](/dm/dm-create-task.md) 。

### 重要な概念 {#important-concepts}

このセクションでは、いくつかの重要な概念について説明します。

| 概念          | 説明                                                                           | Configuration / コンフィグレーションファイル                              |
| :---------- | :--------------------------------------------------------------------------- | :---------------------------------------------------------- |
| `source-id` | MySQLまたはMariaDBインスタンス、またはプライマリ-セカンダリ構造の移行グループを一意に表します。 `source-id`の最大長は32です。 | `source_id` of `source.yaml` ;<br/> `source-id` `task.yaml` |
| DMマスターID    | DMマスターを一意に表します（ `dm-master.toml`の`master-addr`パラメーターによる）                     | `master-addr` of `dm-master.toml`                           |
| DM-ワーカーID   | DMワーカーを一意に表します（ `dm-worker.toml`の`worker-addr`パラメーターによる）                     | `worker-addr` of `dm-worker.toml`                           |
