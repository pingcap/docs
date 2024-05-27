---
title: TiDB Distributed eXecution Framework (DXF)
summary: TiDB Distributed eXecution Framework (DXF) の使用例、制限、使用方法、実装の原則について学習します。
---

# TiDB 分散実行フレームワーク (DXF) {#tidb-distributed-execution-framework-dxf}

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

TiDB は、優れたスケーラビリティと弾力性を備えたコンピューティングとストレージの分離アーキテクチャを採用しています。v7.1.0 以降、TiDB は分散アーキテクチャのリソースの利点をさらに活用するために、分散実行フレームワーク (DXF) を導入しています。DXF の目標は、タスクの統一されたスケジュールと分散実行を実装し、全体と個々のタスクの両方に統一されたリソース管理機能を提供することです。これにより、リソース使用に関するユーザーの期待をよりよく満たすことができます。

このドキュメントでは、DXF の使用例、制限事項、使用方法、実装の原則について説明します。

## ユースケース {#use-cases}

データベース管理システムには、コアとなるトランザクション処理 (TP) と分析処理 (AP) のワークロードに加えて、DDL 操作、IMPORT INTO、TTL、分析、バックアップ/復元などの重要なタスクがあります。これらのタスクは、データベース オブジェクト (テーブル) 内の大量のデータを処理する必要があるため、通常は次の特性があります。

-   スキーマまたはデータベース オブジェクト (テーブル) 内のすべてのデータを処理する必要があります。
-   定期的に実行する必要があるかもしれませんが、頻度は低くなければなりません。
-   リソースが適切に制御されていない場合、TP および AP タスクに影響を与え、データベース サービスの品質が低下する可能性があります。

DXF を有効にすると上記の問題が解決され、次の 3 つの利点があります。

-   このフレームワークは、高いスケーラビリティ、高可用性、高パフォーマンスを実現する統合機能を提供します。
-   DXF はタスクの分散実行をサポートしており、TiDB クラスター全体の利用可能なコンピューティング リソースを柔軟にスケジュールできるため、TiDB クラスター内のコンピューティング リソースをより有効に活用できます。
-   DXF は、全体タスクと個々のタスクの両方に対して、統合されたリソースの使用および管理機能を提供します。

現在、DXF は`ADD INDEX`と`IMPORT INTO`のステートメントの分散実行をサポートしています。

-   `ADD INDEX`インデックスを作成するために使用される DDL ステートメントです。例:

    ```sql
    ALTER TABLE t1 ADD INDEX idx1(c1);
    CREATE INDEX idx1 ON table t1(c1);
    ```

-   `IMPORT INTO`は、 `CSV` 、 `SQL` 、 `PARQUET`などの形式のデータを空のテーブルにインポートするために使用されます。詳細については、 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)を参照してください。

## 制限 {#limitation}

DXF では、最大 16 個のタスク ( `ADD INDEX`タスクと`IMPORT INTO`タスクを含む) を同時にスケジュールできます。

## <code>ADD INDEX</code>制限 {#code-add-index-code-limitation}

-   各クラスターでは、一度に 1 つ`ADD INDEX`タスクのみを分散実行できます。現在の`ADD INDEX`の分散タスクが完了する前に新しい`ADD INDEX`タスクが送信された場合、新しい`ADD INDEX`タスクは DXF によってスケジュールされるのではなく、トランザクションを通じて実行されます。
-   DXF を介して`TIMESTAMP`データ型の列にインデックスを追加することは、インデックスとデータの間に不整合が生じる可能性があるため、サポートされていません。

## 前提条件 {#prerequisites}

DXF を使用して`ADD INDEX`タスクを実行する前に、 [高速オンラインDDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)モードを有効にする必要があります。

<CustomContent platform="tidb">

1.  高速オンライン DDL に関連する次のシステム変数を調整します。

    -   [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) : 高速オンライン DDL モードを有効にするために使用されます。TiDB v6.5.0 以降ではデフォルトで有効になっています。
    -   [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630) : 高速オンライン DDL モードで使用できるローカル ディスクの最大クォータを制御するために使用されます。

2.  高速オンライン DDL に関連する次の構成項目を調整します。

    -   [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) : 高速オンライン DDL モードで使用できるローカル ディスク パスを指定します。

> **注記：**
>
> TiDB `temp-dir`ディレクトリ用に少なくとも 100 GiB の空き領域を用意することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

高速オンライン DDL に関連する次のシステム変数を調整します。

-   [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) : 高速オンライン DDL モードを有効にするために使用されます。TiDB v6.5.0 以降ではデフォルトで有効になっています。
-   [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630) : 高速オンライン DDL モードで使用できるローカル ディスクの最大クォータを制御するために使用されます。

</CustomContent>

## 使用法 {#usage}

1.  DXF を有効にするには、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)の値を`ON`に設定します。v8.1.0 以降では、この変数はデフォルトで有効になっています。v8.1.0 以降のバージョンで新しく作成されたクラスターの場合は、この手順をスキップできます。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    DXF タスクの実行中、フレームワークでサポートされているステートメント ( [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)や[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)など) が分散方式で実行されます。すべての TiDB ノードはデフォルトで DXF タスクを実行します。

2.  一般に、DDL タスクの分散実行に影響を与える可能性のある次のシステム変数については、デフォルト値を使用することをお勧めします。

    -   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) : デフォルト値`4`を使用します。推奨される最大値は`16`です。
    -   [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    -   [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    -   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) : デフォルト値を使用します。推奨される最大値は`1024`です。

## タスクのスケジュール {#task-scheduling}

デフォルトでは、DXF はすべての TiDB ノードをスケジュールして分散タスクを実行します。v7.4.0 以降、TiDB セルフホスト クラスターでは、 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)構成することで、分散タスクを実行するように DXF によってスケジュールできる TiDB ノードを制御できます。

-   バージョン v7.4.0 から v8.0.0 の場合、 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)のオプションの値は`''`または`background`です。現在のクラスターに`tidb_service_scope = 'background'` TiDB ノードがある場合、DXF はこれらのノードにタスクの実行をスケジュールします。障害または通常のスケールインが原因で、現在のクラスターに`tidb_service_scope = 'background'` TiDB ノードがない場合、DXF は`tidb_service_scope = ''`のノードにタスクの実行をスケジュールします。

-   v8.1.0 以降では、 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)任意の有効な値に設定できます。分散タスクが送信されると、タスクは現在接続されている TiDB ノードの`tidb_service_scope`値にバインドされ、DXF は同じ`tidb_service_scope`値を持つ TiDB ノードにのみタスクの実行をスケジュールします。ただし、以前のバージョンとの構成の互換性のために、分散タスクが`tidb_service_scope = ''`ノードに送信され、現在のクラスターに`tidb_service_scope = 'background'` TiDB ノードがある場合、DXF は`tidb_service_scope = 'background'`の TiDB ノードにタスクの実行をスケジュールします。

タスク実行中に新しいノードが追加された場合、DXF は前述のルールに基づいて、新しいノードにタスクをスケジュールして実行するかどうかを決定します。新しく追加されたノードにタスクを実行させたくない場合は、事前にこれらのノードに`tidb_service_scope`設定することをお勧めします。

> **注記：**
>
> -   バージョン v7.4.0 から v8.0.0 の場合、複数の TiDB ノードを持つクラスターでは、2 つ以上の TiDB ノードに`tidb_service_scope`から`background`設定することを強くお勧めします。この変数が 1 つの TiDB ノードにのみ設定されている場合、そのノードが再起動または失敗すると、タスクは`tidb_service_scope = ''`の TiDB ノードに再スケジュールされ、これらの TiDB ノードで実行されているアプリケーションに影響します。
> -   分散タスクの実行中、 `tidb_service_scope`構成への変更は現在のタスクには適用されませんが、次のタスクからは適用されます。

## 実施原則 {#implementation-principles}

DXF のアーキテクチャは次のとおりです。

![Architecture of the DXF](/media/dist-task/dist-task-architect.jpg)

上の図に示すように、DXF でのタスクの実行は主に次のモジュールによって処理されます。

-   ディスパッチャ: 各タスクの分散実行プランを生成し、実行プロセスを管理し、タスク ステータスを変換し、実行時のタスク情報を収集してフィードバックします。
-   スケジューラ: TiDB ノード間で分散タスクの実行を複製し、タスク実行の効率を向上させます。
-   サブタスク エグゼキュータ: 分散サブタスクの実際の実行者。また、サブタスク エグゼキュータはサブタスクの実行ステータスをスケジューラに返し、スケジューラはサブタスクの実行ステータスを統一的に更新します。
-   リソース プール: 上記のモジュールのコンピューティング リソースをプールすることにより、リソースの使用状況と管理を定量化するための基礎を提供します。

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [DDL ステートメントの実行原則とベスト プラクティス](/ddl-introduction.md)

</CustomContent>
<CustomContent platform="tidb-cloud">

-   [DDL ステートメントの実行原則とベスト プラクティス](https://docs.pingcap.com/tidb/stable/ddl-introduction)

</CustomContent>
