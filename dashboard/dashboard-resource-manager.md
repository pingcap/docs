---
title: TiDB Dashboard Resource Manager Page
summary: Introduce how to use the Resource Manager page in TiDB Dashboard to view the information about resource control, so you can estimate cluster capacity before resource planning and allocate resources more effectively.
---

# TiDB ダッシュボードのリソース マネージャー ページ {#tidb-dashboard-resource-manager-page}

[リソース制御](/tidb-resource-control.md)機能を使用してリソース分離を実装するには、クラスター管理者はリソース グループを作成し、各グループのクォータを設定できます。リソースを計画する前に、クラスターの全体的な容量を把握する必要があります。このドキュメントは、リソース制御に関する情報を表示するのに役立ちます。これにより、リソース計画の前にクラスターの容量を見積もり、より効果的にリソースを割り当てることができます。

## ページにアクセスする {#access-the-page}

次の 2 つの方法のいずれかを使用して、[リソース マネージャー] ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで**[リソース マネージャー]**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/resource_manager](http://127.0.0.1:2379/dashboard/#/resource_manager)にアクセスしてください。 `127.0.0.1:2379`を実際の PD インスタンスのアドレスとポートに置き換えます。

## リソースマネージャーページ {#resource-manager-page}

次の図は、リソース マネージャーの詳細ページを示しています。

![TiDB Dashboard: Resource Manager](/media/dashboard/dashboard-resource-manager-info.png)

「リソース マネージャー」ページには、次の 3 つのセクションが含まれています。

-   コンフィグレーション: このセクションには、TiDB の`RESOURCE_GROUPS`テーブルから取得したデータが表示されます。すべてのリソース グループに関する情報が含まれます。詳細については、 [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md)を参照してください。

-   容量の見積もり: リソースを計画する前に、クラスターの全体的な容量を把握する必要があります。次のいずれかの方法を使用できます。

    -   [実際のワークロードに基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
    -   [ハードウェア導入に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

-   メトリック: パネル上のメトリックを観察することで、クラスターの現在の全体的なリソース消費ステータスを理解できます。

## 容量の見積もり {#estimate-capacity}

リソースを計画する前に、クラスターの全体的な容量を把握する必要があります。 TiDB は、現在のクラスター内の[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru#what-is-request-unit-ru)の容量を見積もるための 2 つの方法を提供します。

-   [ハードウェア導入に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

    TiDB は次のワークロード タイプを受け入れます。

    -   `tpcc` : 大量のデータ書き込みを伴うワークロードに適用されます。これは、 `TPC-C`と同様のワークロード モデルに基づいて推定されます。
    -   `oltp_write_only` : 大量のデータ書き込みを伴うワークロードに適用されます。これは、 `sysbench oltp_write_only`と同様のワークロード モデルに基づいて推定されます。
    -   `oltp_read_write` : データの読み取りと書き込みが均等なワークロードに適用されます。これは、 `sysbench oltp_read_write`と同様のワークロード モデルに基づいて推定されます。
    -   `oltp_read_only` : 大量のデータを読み取るワークロードに適用されます。これは、 `sysbench oltp_read_only`と同様のワークロード モデルに基づいて推定されます。

    ![Calibrate by Hardware](/media/dashboard/dashboard-resource-manager-calibrate-by-hardware.png)

    **ユーザー リソース グループの合計 RU は、** `default`リソース グループを除く、すべてのユーザー リソース グループの RU の合計量を表します。この値が推定容量より小さい場合、システムはアラートをトリガーします。デフォルトでは、システムは事前定義された`default`リソース グループに無制限の使用量を割り当てます。すべてのユーザーが`default`リソース グループに属している場合、リソース制御が無効な場合と同じ方法でリソースが割り当てられます。

-   [実際のワークロードに基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)

    ![Calibrate by Workload](/media/dashboard/dashboard-resource-manager-calibrate-by-workload.png)

    推定の時間範囲は 10 分から 24 時間の範囲で選択できます。使用されるタイム ゾーンは、フロントエンド ユーザーのタイム ゾーンと同じです。

    -   時間枠の範囲が 10 分から 24 時間の範囲に収まらない場合、次のエラーが表示されます`ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s` 。

    -   [実際のワークロードに基づいた容量の見積もり](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)機能のモニタリング メトリックには、 `tikv_cpu_quota` 、 `tidb_server_maxprocs` 、 `resource_manager_resource_unit` 、および`process_cpu_usage`が含まれます。 CPU クォータ監視データが空の場合、対応する監視メトリック名 (たとえば、 `Error 1105 (HY000): There is no CPU quota metrics, metrics 'tikv_cpu_quota' is empty`でエラーが発生します。

    -   時間枠内のワークロードが低すぎる場合、または`resource_manager_resource_unit`および`process_cpu_usage`監視データが欠落している場合は、エラーが報告されます`Error 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead` 。さらに、TiKV は macOS 上の CPU 使用率を監視しないため、実際のワークロードに基づく容量の見積もりをサポートせず、このエラーも報告します。

    [メトリクス](#metrics)セクションの**CPU 使用率**を使用して、適切な時間範囲を選択できます。

## メトリクス {#metrics}

パネル上のメトリックを観察することで、クラスターの現在の全体的なリソース消費ステータスを理解できます。監視メトリクスとその意味は次のとおりです。

-   消費された合計 RU: リアルタイムでカウントされたリクエスト ユニットの合計消費量。
-   リソース グループによって消費された RU: リソース グループによってリアルタイムで消費されたリクエスト ユニットの数。
-   TiDB
    -   CPU クォータ: TiDB の最大 CPU 使用量。
    -   CPU 使用率: すべての TiDB インスタンスの合計 CPU 使用率。
-   TiKV
    -   CPU クォータ: TiKV の最大 CPU 使用量。
    -   CPU 使用率: すべての TiKV インスタンスの合計 CPU 使用率。
    -   IO MBps: すべての TiKV インスタンスの合計 I/O スループット。
