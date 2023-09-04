---
title: Integrate TiDB Cloud with Datadog (Beta)
summary: Learn how to monitor your TiDB cluster with the Datadog integration.
---

# TiDB Cloudと Datadog を統合する (ベータ版) {#integrate-tidb-cloud-with-datadog-beta}

TiDB Cloud はDatadog 統合 (ベータ版) をサポートしています。 TiDB クラスターに関するメトリック データを[データドッグ](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリクスを Datadog ダッシュボードで直接表示できるようになります。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Datadog と統合するには、Datadog アカウントと[Datadog API キー](https://app.datadoghq.com/organization-settings/api-keys)が必要です。 Datadog は、最初に Datadog アカウントを作成するときに API キーを付与します。

    Datadog アカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`アクセス権、またはTiDB Cloudのターゲット プロジェクトへの`Project Member`アクセス権が必要です。

## 制限 {#limitation}

-   [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターでは Datadog 統合を使用できません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Datadog 統合は使用できません。

## ステップ {#steps}

### ステップ 1. Datadog API キーと統合する {#step-1-integrate-with-your-datadog-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">複数のプロジェクトがある場合は、左下隅でターゲット プロジェクトに切り替え、 **[プロジェクト設定]**をクリックします。</mdsvgicon>

3.  プロジェクトの [**プロジェクト設定]**ページで、左側のナビゲーション ペインで**[統合]**をクリックし、 **[Datadog への統合 (ベータ)]**をクリックします。

4.  Datadog の API キーを入力し、Datadog のサイトを選択します。

5.  **「統合のテスト」**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストが失敗した場合は、エラー メッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

### ステップ 2. Datadog にTiDB Cloud統合をインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

1.  [データドッグ](https://app.datadoghq.com)にログインします。
2.  Datadog の**TiDB Cloud統合**ページ ( [https://app.datadoghq.com/account/settings#integrations/tidb-cloud](https://app.datadoghq.com/account/settings#integrations/tidb-cloud) ) に移動します。
3.  **「コンフィグレーション」**タブで、 **「統合のインストール」を**クリックします。 [**TiDBCloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードが[**ダッシュボードリスト**](https://app.datadoghq.com/dashboard/lists)に表示されます。

## 事前に構築されたダッシュボード {#pre-built-dashboard}

統合の**Datadog**カードにある**[ダッシュボード]**リンクをクリックします。 TiDB クラスターの事前構築されたダッシュボードを確認できます。

## Datadog で利用できるメトリクス {#metrics-available-to-datadog}

Datadog は、TiDB クラスターの次のメトリック データを追跡します。

| メトリクス名                                     | メトリックタイプ | ラベル                                                                                                               | 説明                                                                                                    |
| :----------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| tidb_cloud.db_database_time                | ゲージ      | sql_type: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | TiDB で実行されているすべての SQL ステートメントによって消費された 1 秒あたりの合計時間 (すべてのプロセスの CPU 時間と非アイドル待機時間を含む)。                   |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                        | すべての TiDB インスタンスで 1 秒あたりに実行された SQL ステートメントの数。これは、SELECT、INSERT、UPDATE、およびその他のタイプのステートメントに従ってカウントされます。 |
| tidb_cloud.db_average_query_duration       | ゲージ      | sql_type: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | クライアントのネットワーク リクエストが TiDB に送信されてから、TiDB がリクエストを実行した後にリクエストがクライアントに返されるまでの期間。                          |
| tidb_cloud.db_failed_queries               | ゲージ      | タイプ: 実行者:xxxx|パーサー:xxxx|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`           | 各 TiDB インスタンスで 1 秒あたりに発生する SQL 実行エラーに応じたエラー タイプ (構文エラーや主キーの競合など) の統計。                                 |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | TiDBサーバー内の現在の接続の数。                                                                                    |
| tidb_cloud.db_active_connections           | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | アクティブな接続の数。                                                                                           |
| tidb_cloud.db_disconnections               | ゲージ      | 結果: OK|エラー|未定<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                         | 切断されたクライアントの数。                                                                                        |
| tidb_cloud.db_command_per_second           | ゲージ      | タイプ: クエリ|StmtPrepare|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`              | TiDB によって 1 秒あたりに処理されたコマンドの数。コマンドの実行結果の成功または失敗に従って分類されます。                                             |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | [プランキャッシュ](/sql-prepared-plan-cache.md)秒あたり 1 を使用したクエリの統計。実行プラン キャッシュは、プリペアドステートメントコマンドのみをサポートします。    |
| tidb_cloud.db_transaction_per_second       | ゲージ      | txn_mode:悲観的|楽観的<br/>タイプ: 中止|コミット|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb` | 1 秒あたりに実行されるトランザクションの数。                                                                               |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tflash                 | TiKV/ TiFlashノードのディスク使用量 (バイト単位)。                                                                     |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tflash                 | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                      |
| tidb_cloud.node_cpu_seconds_total          | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tflash              | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                       |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tflash-0…<br/>コンポーネント: tidb|tikv|tflash               | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                     |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tflash-0…<br/>コンポーネント: tidb|tikv|tflash               | TiDB/TiKV/ TiFlashノードの使用済みメモリ(バイト単位)。                                                                 |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tflash-0…<br/>コンポーネント: tidb|tikv|tflash               | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                                  |
