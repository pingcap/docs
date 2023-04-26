---
title: Integrate TiDB Cloud with Datadog
summary: Learn how to monitor your TiDB cluster with the Datadog integration.
---

# TiDB Cloudと Datadog の統合 {#integrate-tidb-cloud-with-datadog}

TiDB クラスターに関するメトリック データを[データドッグ](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリクスを Datadog ダッシュボードで直接表示できます。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Datadog と統合するには、Datadog アカウントと[Datadog API キー](https://app.datadoghq.com/organization-settings/api-keys)が必要です。初めて Datadog アカウントを作成すると、Datadog は API キーを付与します。

    Datadog アカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`アクセス権またはTiDB Cloudのターゲット プロジェクトへの`Project Member`アクセス権が必要です。

## 制限 {#limitation}

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターで Datadog 統合を使用することはできません。

-   クラスターのステータスが**CREATING** 、 <strong>RESTORING</strong> 、 <strong>PAUSED</strong> 、または<strong>RESUMING</strong>の場合、Datadog 統合は利用できません。

## 手順 {#steps}

### ステップ 1. Datadog API キーと統合する {#step-1-integrate-with-your-datadog-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ペインで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えてから、 **[管理]** &gt; <strong>[統合]</strong>をクリックします。
    -   プロジェクトが 1 つしかない場合は、 **[管理]** &gt; <strong>[統合]</strong>をクリックします。

3.  **Datadog への統合 を**クリックします。

4.  Datadog の API キーを入力し、Datadog のサイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、**確認**ボタンが表示されます。
    -   テストが失敗すると、エラー メッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **[確認]**をクリックして統合を完了します。

### ステップ 2. Datadog にTiDB Cloud統合をインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

1.  [データドッグ](https://app.datadoghq.com)にログインします。
2.  Datadog の**TiDB Cloud統合**ページ ( [https://app.datadoghq.com/account/settings#integrations/tidb-cloud](https://app.datadoghq.com/account/settings#integrations/tidb-cloud) ) に移動します。
3.  **[コンフィグレーション]**タブで、 <strong>[統合のインストール]</strong>をクリックします。 [**TiDBCloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードが[**ダッシュボード一覧**](https://app.datadoghq.com/dashboard/lists)に表示されます。

## 事前構築済みのダッシュボード {#pre-built-dashboard}

統合の**Datadog**カードで<strong>[ダッシュボード]</strong>リンクをクリックします。 TiDB クラスターの事前構築済みダッシュボードが表示されます。

## Datadog で利用可能なメトリクス {#metrics-available-to-datadog}

Datadog は、TiDB クラスターの次のメトリクス データを追跡します。

| 指標名                                        | 指標タイプ | ラベル                                                                                                              | 説明                                                                                                   |
| :----------------------------------------- | :---- | :--------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| tidb_cloud.db_database_time                | ゲージ   | sql_type: 選択|挿入|...<br/>クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | すべてのプロセスの CPU 時間と非アイドル待機時間を含む、TiDB で実行されているすべての SQL ステートメントによって消費された 1 秒あたりの合計時間。                    |
| tidb_cloud.db_query_per_second             | ゲージ   | タイプ: 選択|挿入|...<br/>クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                        | SELECT、INSERT、UPDATE、およびその他のタイプのステートメントに従ってカウントされる、すべての TiDB インスタンスで 1 秒あたりに実行される SQL ステートメントの数。     |
| tidb_cloud.db_average_query_duration       | ゲージ   | sql_type: 選択|挿入|...<br/>クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | クライアントのネットワーク要求が TiDB に送信されてから、TiDB が要求を実行した後に要求がクライアントに返されるまでの時間。                                   |
| tidb_cloud.db_failed_queries               | ゲージ   | タイプ: エグゼキューター:xxxx|パーサー:xxxx|...<br/>クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`      | 各 TiDB インスタンスで 1 秒あたりに発生した SQL 実行エラーに基づく、エラーの種類 (構文エラーや主キーの競合など) の統計。                                |
| tidb_cloud.db_total_connection             | ゲージ   | クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | TiDBサーバーの現在の接続数。                                                                                     |
| tidb_cloud.db_active_connections           | ゲージ   | クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | アクティブな接続の数。                                                                                          |
| tidb_cloud.db_disconnections               | ゲージ   | 結果: OK|エラー|不明<br/>クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                         | 切断されたクライアントの数。                                                                                       |
| tidb_cloud.db_command_per_second           | ゲージ   | タイプ: クエリ|StmtPrepare|...<br/>クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`              | コマンド実行結果の成否で分類した、1秒間にTiDBが処理したコマンド数。                                                                 |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ   | クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | [プラン キャッシュ](/sql-prepared-plan-cache.md)秒あたり 1 件を使用したクエリの統計。実行プラン キャッシュは、プリペアドステートメントコマンドのみをサポートします。 |
| tidb_cloud.db_transaction_per_second       | ゲージ   | txn_mode:悲観的|楽観的<br/>タイプ: 中止|コミット|...<br/>クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb` | 1 秒あたりに実行されたトランザクションの数。                                                                              |
| tidb_cloud.node_storage_used_bytes         | ゲージ   | クラスタ名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク使用量 (バイト単位)。                                                                    |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ   | クラスタ名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                     |
| tidb_cloud.node_cpu_seconds_total          | カウント  | クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                      |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ   | クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                    |
| tidb_cloud.node_memory_used_bytes          | ゲージ   | クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの使用メモリ(バイト単位)。                                                                  |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ   | クラスタ名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                                 |
