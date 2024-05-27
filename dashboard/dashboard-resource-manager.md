---
title: TiDB Dashboard Resource Manager Page
summary: TiDB ダッシュボード リソース マネージャー ページは、クラスター管理者がリソース グループを作成し、クォータを設定することでリソース分離を実装するのに役立ちます。クラスター容量を推定し、リソース消費を監視する方法を提供します。このページには、TiDB ダッシュボードまたはブラウザーからアクセスします。このページには、構成、容量推定、およびメトリックのセクションがあります。容量推定方法には、ハードウェアの展開と実際のワークロードが含まれます。監視メトリックには、消費された合計 RU、リソース グループによって消費された RU、TiDB CPU クォータと使用量、TiKV CPU クォータと使用量、および TiKV IO MBps が含まれます。
---

# TiDB ダッシュボード リソース マネージャー ページ {#tidb-dashboard-resource-manager-page}

[リソース管理](/tidb-resource-control.md)機能を使用してリソース分離を実装するには、クラスター管理者がリソース グループを作成し、各グループにクォータを設定できます。リソースを計画する前に、クラスターの全体的な容量を知っておく必要があります。このドキュメントでは、リソース制御に関する情報を表示して、リソースを計画する前にクラスターの容量を見積もり、リソースをより効果的に割り当てることができます。

## ページにアクセスする {#access-the-page}

リソース マネージャー ページにアクセスするには、次の 2 つの方法のいずれかを使用できます。

-   TiDB ダッシュボードにログインしたら、左側のナビゲーション メニューで**[リソース マネージャー]**をクリックします。

-   ブラウザで[http://127.0.0.1:2379/ダッシュボード/#/リソースマネージャー](http://127.0.0.1:2379/dashboard/#/resource_manager)アクセスします。3 `127.0.0.1:2379`実際の PD インスタンスのアドレスとポートに置き換えます。

## リソース マネージャー ページ {#resource-manager-page}

次の図は、リソース マネージャーの詳細ページを示しています。

![TiDB Dashboard: Resource Manager](/media/dashboard/dashboard-resource-manager-info.png)

リソース マネージャー ページには、次の 3 つのセクションが含まれています。

-   コンフィグレーション: このセクションには、TiDB の`RESOURCE_GROUPS`テーブルから取得されたデータが表示されます。すべてのリソース グループに関する情報が含まれています。詳細については、 [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md)を参照してください。

-   容量の見積もり: リソース計画を立てる前に、クラスターの全体的な容量を把握しておく必要があります。次のいずれかの方法を使用できます。

    -   [実際の作業負荷に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
    -   [ハードウェアの展開に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

-   メトリクス: パネル上のメトリクスを観察することで、クラスターの現在の全体的なリソース消費状況を把握できます。

## 容量の見積り {#estimate-capacity}

リソース計画を立てる前に、クラスターの全体的な容量を把握しておく必要があります。TiDB では[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru#what-is-request-unit-ru)現在のクラスターの容量を見積もる 2 つの方法を提供しています。

-   [ハードウェアの展開に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

    TiDB は次のワークロード タイプを受け入れます。

    -   `tpcc` : 大量のデータ書き込みを伴うワークロードに適用されます。 `TPC-C`と同様のワークロード モデルに基づいて推定されます。
    -   `oltp_write_only` : 大量のデータ書き込みを伴うワークロードに適用されます。 `sysbench oltp_write_only`と同様のワークロード モデルに基づいて推定されます。
    -   `oltp_read_write` : 偶数データの読み取りと書き込みのワークロードに適用されます。 `sysbench oltp_read_write`と同様のワークロード モデルに基づいて推定されます。
    -   `oltp_read_only` : 大量のデータ読み取りが行われるワークロードに適用されます。 `sysbench oltp_read_only`と同様のワークロード モデルに基づいて推定されます。

    ![Calibrate by Hardware](/media/dashboard/dashboard-resource-manager-calibrate-by-hardware.png)

    **ユーザー リソース グループの合計 RU は**、 `default`リソース グループを除くすべてのユーザー リソース グループの RU の合計量を表します。この値が推定容量より少ない場合、システムはアラートをトリガーします。デフォルトでは、システムは定義済みの`default`リソース グループに無制限の使用を割り当てます。すべてのユーザーが`default`リソース グループに属している場合、リソースはリソース制御が無効になっている場合と同じ方法で割り当てられます。

-   [実際の作業負荷に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)

    ![Calibrate by Workload](/media/dashboard/dashboard-resource-manager-calibrate-by-workload.png)

    推定する時間範囲は 10 分から 24 時間まで選択できます。使用されるタイムゾーンはフロントエンド ユーザーのタイムゾーンと同じです。

    -   時間ウィンドウの範囲が 10 分から 24 時間の範囲外の場合、次のエラーが表示されます`ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s` 。

    -   [実際の作業負荷に基づく容量推定](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)機能の監視メトリックには、 `tikv_cpu_quota` 、 `tidb_server_maxprocs` 、 `resource_manager_resource_unit` 、および`process_cpu_usage`含まれます。CPU クォータ監視データが空の場合、対応する監視メトリック名 (例: `Error 1105 (HY000): There is no CPU quota metrics, metrics 'tikv_cpu_quota' is empty` ) にエラーが発生します。

    -   時間枠内のワークロードが低すぎる場合、または`resource_manager_resource_unit`と`process_cpu_usage`監視データが欠落している場合は、エラーが報告されます`Error 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead` 。また、TiKV は macOS 上の CPU 使用率を監視しないため、実際のワークロードに基づく容量推定をサポートしておらず、このエラーも報告されます。

    [メトリクス](#metrics)セクションの**CPU 使用率**を使用して適切な時間範囲を選択できます。

## メトリクス {#metrics}

パネル上のメトリックを観察することで、クラスターの現在の全体的なリソース消費状況を把握できます。監視メトリックとその意味は次のとおりです。

-   消費された RU の合計: リアルタイムでカウントされた要求ユニットの合計消費量。
-   リソース グループによって消費された RU: リソース グループによってリアルタイムで消費された要求ユニットの数。
-   ティビ
    -   CPU クォータ: TiDB の最大 CPU 使用量。
    -   CPU 使用率: すべての TiDB インスタンスの合計 CPU 使用率。
-   ティクヴ
    -   CPU クォータ: TiKV の最大 CPU 使用量。
    -   CPU 使用率: すべての TiKV インスタンスの合計 CPU 使用率。
    -   IO MBps: すべての TiKV インスタンスの合計 I/O スループット。
