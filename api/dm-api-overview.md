---
title: Data Migration API Overview
summary: データ移行 (DM) の API を学習します。
---

# データ移行APIの概要 {#data-migration-api-overview}

[TiDBデータ移行](/dm/dm-overview.md) (DM) は、MySQL 互換データベース (MySQL、MariaDB、 Aurora MySQL など) から TiDB への完全なデータ移行と増分データレプリケーションをサポートする統合データ移行タスク管理プラットフォームです。

DM は、 [dmctlツール](/dm/dmctl-introduction.md)と同様に、DM クラスターのクエリと操作を行うための OpenAPI を提供します。

DM API を使用して、DM クラスターで次のメンテナンス操作を実行できます。

-   [クラスタ管理](/dm/dm-open-api.md#apis-for-managing-clusters) : DM マスター ノードと DM ワーカー ノードに関する情報を取得したり、停止したりします。
-   [データソース管理](/dm/dm-open-api.md#apis-for-managing-data-sources) : データ ソースを作成、更新、削除、有効化、無効化し、リレー ログ機能を管理し、データ ソースと DM ワーカー間のバインディングを変更します。
-   [レプリケーションタスク管理](/dm/dm-open-api.md#apis-for-managing-replication-tasks) : レプリケーション タスクを作成、更新、削除、開始、または停止し、スキーマと移行ルールを管理します。

リクエストパラメータ、レスポンス例、使用方法など、各 API の詳細については、 [OpenAPI を使用して DM クラスターを管理](/dm/dm-open-api.md)参照してください。
