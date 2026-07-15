---
title: TiDB CloudとDatadogを統合する (PREVIEW)
summary: Datadog integration を使用して TiDB Cloud インスタンスを監視する方法を学びます。
---

# TiDB CloudとDatadogを統合する (PREVIEW)

TiDB Cloud は Datadog との統合をサポートしています。TiDB Cloud を設定して、<CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> インスタンスのメトリクスを [Datadog](https://www.datadoghq.com/) に送信できます。設定後は、これらのメトリクスを Datadog のダッシュボードで直接表示できます。

## 前提条件 {#prerequisites}

- TiDB Cloud を Datadog と統合するには、Datadog アカウントと [Datadog API key](https://app.datadoghq.com/organization-settings/api-keys) が必要です。Datadog アカウントを初めて作成すると、Datadog から API key が付与されます。

    Datadog アカウントを持っていない場合は、[https://app.datadoghq.com/signup](https://app.datadoghq.com/signup) でサインアップしてください。

- TiDB Cloud でサードパーティメトリクス統合を設定するには、TiDB Cloud で `Organization Owner`、`Project Owner`、または `Instance Manager` のアクセス権限が必要です。統合ページを表示するには、少なくとも `Project Viewer` または `Instance Viewer` ロールが必要であり、TiDB Cloud の組織配下にある対象の <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> インスタンスにアクセスできる必要があります。

## 制限事項 {#limitations}

- Datadog integration は [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) インスタンスでは利用できません。
- 対象の <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> インスタンスのステータスが **CREATING**、**RESTORING**、**PAUSED**、または **RESUMING** の場合、Datadog integration は利用できません。

## 手順 {#steps}

### 手順 1. 事前構築済み Datadog ダッシュボードをインポートする {#step-1-import-the-pre-built-datadog-dashboard}

現在、<CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 用の TiDB Cloud ダッシュボードは、Datadog integration marketplace ではまだ利用できません。ダッシュボード JSON ファイルを手動でダウンロードし、Datadog にインポートする必要があります。

1. インスタンスタイプに対応する Datadog ダッシュボード JSON ファイルをダウンロードします。

    <CustomContent plan="essential">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-datadog-integration-tidb-cloud-dynamic-tracker-essential.json>

    </CustomContent>

    <CustomContent plan="premium">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-datadog-integration-tidb-cloud-dynamic-tracker-premium.json>

    </CustomContent>

2. [Datadog](https://app.datadoghq.com) にログインし、**Dashboards** > **Dashboard List** に移動します。

3. 右上の **+ New Dashboard** をクリックします。ダッシュボード名を入力し、**Start from blank dashboard** を選択します。

4. 新しいダッシュボードで、右上の歯車アイコン (**Configure**) をクリックし、**Import dashboard JSON...** を選択します。

5. 表示されるダイアログで、JSON の内容を貼り付けるか、JSON ファイルをドラッグアンドドロップします。

6. **Yes, Replace** をクリックしてインポートを確定します。

### 手順 2. Datadog API key と統合する {#step-2-integrate-with-your-datadog-api-key}

<CustomContent plan="essential">

1. [TiDB Cloud console](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .essential }}} インスタンス名をクリックして概要ページを開きます。
2. 左側のナビゲーションペインで、**Integrations** をクリックします。
3. **Integrations** ページで、**Datadog (PREVIEW)** 統合を見つけて **Connect** をクリックします。
4. Datadog API key を入力し、Datadog リージョンを選択してから、**Test Integration** をクリックします。

    - テストが成功すると、**Confirm** ボタンが表示されます。
    - テストが失敗すると、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、再度統合を試してください。

5. **Confirm** をクリックして統合を完了します。

</CustomContent>

<CustomContent plan="premium">

1. [TiDB Cloud console](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .premium }}} インスタンス名をクリックして概要ページを開きます。
2. 左側のナビゲーションペインで、**Settings** > **Integrations** をクリックします。
3. **Integrations** ページで、**Datadog (PREVIEW)** 統合を見つけて **Connect** をクリックします。
4. Datadog API key を入力し、Datadog リージョンを選択してから、**Test Integration** をクリックします。

    - テストが成功すると、**Confirm** ボタンが表示されます。
    - テストが失敗すると、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、再度統合を試してください。

5. **Confirm** をクリックして統合を完了します。

</CustomContent>

## 事前構築済みダッシュボードを表示する {#view-the-pre-built-dashboard}

統合後に事前構築済みダッシュボードを表示するには、[Datadog](https://app.datadoghq.com) で **Dashboards** > **Dashboard List** に移動し、[手順 1](#step-1-import-the-pre-built-datadog-dashboard) でインポートしたダッシュボードを選択します。ダッシュボードページでは、対象のインスタンス名でフィルタリングしてメトリクスを表示できます。

また、[TiDB Cloud console](https://tidbcloud.com/) から Datadog の **Dashboard List** ページにアクセスすることもできます。対象インスタンスの **Integrations** ページに移動し、**Datadog (PREVIEW)** をクリックしてから **Dashboard** をクリックします。

## Datadog で利用可能なメトリクス {#metrics-available-to-datadog}

Datadog は、<CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> インスタンスについて、以下のメトリクスを追跡します。

<CustomContent plan="essential">

> **Note:**
>
> 現在、{{{ .essential }}} の changefeed 機能はリクエストベースでのみ利用可能であり、`tidb_cloud.changefeed_*` メトリクスは利用できません。

| メトリック名 | メトリックタイプ | ラベル | 説明 |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB server における現在の接続数 |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | アクティブな接続数 |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 接続結果ごとに切断されたクライアント数 |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB で実行中のすべての SQL 文が 1 秒あたりに消費した合計時間。すべてのプロセスの CPU 時間と、アイドル状態ではない待機時間を含みます |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 文の種類ごとに集計された、1 秒あたりに実行された SQL 文の数 |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | SQL 文の実行時に 1 秒あたりに発生したエラー種別（構文エラーや主キー競合など）の統計 |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB が 1 秒あたりに処理したコマンド数 |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 1 秒あたりに実行計画キャッシュにヒットしたクエリ数 |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | ネットワークリクエストが TiDB に送信されてから、レスポンスがクライアントに返されるまでの時間 |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 1 秒あたりに実行されたトランザクション数 |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} インスタンスの行ベースストレージサイズ（バイト） |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} インスタンスのカラムナー ストレージサイズ（バイト）。TiFlash が有効でない場合は 0 を返します |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 消費された合計 Request Units/s (RU/s) |

</CustomContent>

<CustomContent plan="premium">

| メトリック名 | メトリックタイプ | ラベル | 説明 |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB server における現在の接続数 |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | アクティブな接続数 |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 接続結果ごとに切断されたクライアント数 |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB で実行中のすべての SQL 文が 1 秒あたりに消費した合計時間。すべてのプロセスの CPU 時間と、アイドル状態ではない待機時間を含みます |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 文の種類ごとに集計された、1 秒あたりに実行された SQL 文の数 |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | SQL 文の実行時に 1 秒あたりに発生したエラー種別（構文エラーや主キー競合など）の統計 |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB が 1 秒あたりに処理したコマンド数 |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 1 秒あたりに実行計画キャッシュにヒットしたクエリ数 |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | ネットワークリクエストが TiDB に送信されてから、レスポンスがクライアントに返されるまでの時間 |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 1 秒あたりに実行されたトランザクション数 |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} インスタンスの行ベースストレージサイズ（バイト） |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} インスタンスのカラムナー ストレージサイズ（バイト） |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 消費された合計 Request Units/s (RU/s) |
| `tidb_cloud.changefeed_latency` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed の upstream と downstream 間のデータレプリケーション レイテンシー |
| `tidb_cloud.changefeed_status` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed のステータス:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>
