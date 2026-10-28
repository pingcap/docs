---
title: TiDB Cloud と New Relic を統合する (PREVIEW)
summary: New Relic 統合を使用して TiDB Cloud インスタンスを監視する方法を学びます。
---

# TiDB Cloud と New Relic を統合する (PREVIEW)

TiDB Cloud は New Relic との統合をサポートしています。TiDB Cloud を設定して、<CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> インスタンスのメトリクスを [New Relic](https://newrelic.com/) に送信できます。その後、これらのメトリクスを New Relic のダッシュボードで直接表示できます。

## 前提条件 {#prerequisites}

- TiDB Cloud を New Relic と統合するには、[New Relic](https://newrelic.com/) アカウントを所有し、`Ingest - License` タイプの [New Relic APIキーを作成](https://one.newrelic.com/admin-portal/api-keys/home?) している必要があります。

    New Relic アカウントを持っていない場合は、[https://newrelic.com/signup](https://newrelic.com/signup) でサインアップしてください。

- TiDB Cloud のサードパーティメトリクス統合を設定するには、TiDB Cloud で `Organization Owner`、`Project Owner`、または `Instance Manager` のアクセス権限が必要です。統合ページを表示するには、TiDB Cloud の組織配下にある対象の <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> インスタンスにアクセスできる、少なくとも `Project Viewer` または `Instance Viewer` ロールが必要です。

## 制限事項 {#limitations}

- New Relic 統合は [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) インスタンスでは利用できません。
- <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> インスタンスのステータスが **CREATING**、**RESTORING**、**PAUSED**、または **RESUMING** の場合、New Relic 統合は利用できません。
- New Relic 統合が設定されたインスタンスを削除すると、関連付けられた統合サービスも削除されます。

## 手順 {#steps}

### ステップ 1. 事前構築済みの New Relic ダッシュボードをインポートする {#step-1-import-the-pre-built-new-relic-dashboard}

現在、<CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> 用の TiDB Cloud ダッシュボードは、まだ New Relic マーケットプレイスでは利用できません。公開されるまでは、ダッシュボード JSON ファイルを手動でダウンロードし、New Relic にインポートする必要があります。

1. インスタンスタイプに応じた New Relic ダッシュボード JSON ファイルをダウンロードします。

    <CustomContent plan="essential">

    - 2026 年 7 月 1 日以降に作成された TiDB Cloud Essential インスタンスの場合は、この JSON ファイルをダウンロードします: <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-essential-v2.json>。`v2` サフィックスは、ダッシュボード JSON ファイルのバージョンのみを示します。
    - 2026 年 7 月 1 日より前に作成された TiDB Cloud Essential インスタンスの場合は、この JSON ファイルをダウンロードします: <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-essential.json>。

    </CustomContent>

    <CustomContent plan="premium">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-premium.json>

    </CustomContent>

2. JSON ファイル内のすべての `"accountIds": []` フィールドに、[New Relic アカウント ID](https://docs.newrelic.com/docs/accounts/accounts-billing/account-structure/account-id/) を追加します。

    例:

    ```json
    "accountIds": [
      1234567
    ],
    ```

    > **Note:**
    >
    > 統合エラーを回避するため、JSON ファイル内のすべての `"accountIds"` フィールドにアカウント ID が追加されていることを確認してください。

3. [New Relic](https://one.newrelic.com/) にログインし、左側のナビゲーションバーで **Dashboards** をクリックしてから、右上隅の **Import dashboard** をクリックします。

4. 表示されたダイアログで、準備した JSON ファイルの内容をテキストエリアに貼り付け、権限設定を選択してから **Save** をクリックします。

### ステップ 2. New Relic APIキーと統合する {#step-2-integrate-with-your-new-relic-api-key}

<CustomContent plan="essential">

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .essential }}} インスタンス名をクリックして概要ページを開きます。
2. 左側のナビゲーションペインで **Integrations** をクリックします。
3. **Integrations** ページで **New Relic (PREVIEW)** 統合を見つけ、**Connect** をクリックします。
4. New Relic APIキーを入力し、New Relic アカウントがホストされているリージョンを選択してから、**Test Integration** をクリックします。

    - テストが成功すると、**Confirm** ボタンが表示されます。
    - テストが失敗すると、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

5. **Confirm** をクリックして統合を完了します。

</CustomContent>

<CustomContent plan="premium">

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .premium }}} インスタンス名をクリックして概要ページを開きます。
2. 左側のナビゲーションペインで **Settings** > **Integrations** をクリックします。
3. **Integrations** ページで **New Relic (PREVIEW)** 統合を見つけ、**Connect** をクリックします。
4. New Relic APIキーを入力し、New Relic アカウントがホストされているリージョンを選択してから、**Test Integration** をクリックします。

    - テストが成功すると、**Confirm** ボタンが表示されます。
    - テストが失敗すると、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

5. **Confirm** をクリックして統合を完了します。

</CustomContent>

## 事前構築済みダッシュボードを表示する {#view-the-pre-built-dashboard}

統合後に事前構築済みダッシュボードを表示するには、[New Relic](https://one.newrelic.com/) で **Dashboards** > **Dashboard List** に移動し、[ステップ 1](#step-1-import-the-pre-built-new-relic-dashboard) でインポートしたダッシュボードを選択します。ダッシュボードページでは、対象のインスタンス名またはインスタンス ID でフィルタリングして、メトリクスを表示できます。

[TiDB Cloud コンソール](https://tidbcloud.com/) から New Relic の **Dashboard List** ページにアクセスすることもできます。対象インスタンスの **Integrations** ページに移動し、**New Relic (PREVIEW)** をクリックしてから **Dashboard** をクリックします。

## New Relic で利用可能なメトリクス {#metrics-available-to-new-relic}

New Relic は、<CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> インスタンスについて、以下のメトリクスを追跡します。

<CustomContent plan="essential">

> **Note:**
>
> `tidb_cloud.cdc_changefeed_*` メトリクスは、2026 年 7 月 1 日以降に作成された TiDB Cloud Essential インスタンスでのみ利用できます。

| メトリクス名 | メトリクスタイプ | ラベル | 説明 |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB サーバー内の現在の接続数 |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | アクティブな接続数 |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 接続結果ごとに切断されたクライアント数 |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB で実行中のすべての SQL 文が 1 秒あたりに消費した合計時間。すべてのプロセスの CPU 時間と、アイドル状態ではない待機時間を含みます |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 文のタイプ別に集計された、1 秒あたりに実行された SQL 文の数 |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | SQL 文の実行時に 1 秒あたりに発生するエラータイプ（構文エラーや主キー競合など）の統計 |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB が 1 秒あたりに処理したコマンド数 |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 実行プランキャッシュにヒットしたクエリの 1 秒あたりの数 |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | ネットワークリクエストが TiDB に送信されてから、レスポンスがクライアントに返されるまでの時間 |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 1 秒あたりに実行されたトランザクション数 |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} インスタンスの行ベースストレージサイズ（バイト） |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .essential }}} インスタンスの列指向ストレージサイズ（バイト）。TiFlash が有効になっていない場合は 0 を返します |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 消費された合計 Request Units/s (RU/s) |
| `tidb_cloud.cdc_changefeed_latency` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed の上流と下流の間のデータレプリケーションレイテンシー |
| `tidb_cloud.cdc_changefeed_status` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed のステータス:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>

<CustomContent plan="premium">

| メトリクス名 | メトリクスタイプ | ラベル | 説明 |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB サーバー内の現在の接続数 |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | アクティブな接続数 |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 接続結果ごとに切断されたクライアント数 |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB で実行中のすべての SQL 文が 1 秒あたりに消費した合計時間。すべてのプロセスの CPU 時間と、アイドル状態ではない待機時間を含みます |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 文のタイプ別に集計された、1 秒あたりに実行された SQL 文の数 |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | SQL 文の実行時に 1 秒あたりに発生するエラータイプ（構文エラーや主キー競合など）の統計 |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | TiDB が 1 秒あたりに処理したコマンド数 |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 実行プランキャッシュにヒットしたクエリの 1 秒あたりの数 |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | ネットワークリクエストが TiDB に送信されてから、レスポンスがクライアントに返されるまでの時間 |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 1 秒あたりに実行されたトランザクション数 |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} インスタンスの行ベースストレージサイズ（バイト） |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | {{{ .premium }}} インスタンスの列指向ストレージサイズ（バイト） |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | 消費された合計 Request Units/s (RU/s) |
| `tidb_cloud.cdc_changefeed_latency` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | changefeed の上流と下流の間のデータレプリケーションレイテンシー |
| `tidb_cloud.cdc_changefeed_status` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed のステータス:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>