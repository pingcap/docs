---
title: Integrate TiDB Cloud with Datadog (Beta)
summary: Datadog 統合を使用して TiDB クラスターを監視する方法を学習します。
---

# TiDB Cloudと Datadog の統合 (ベータ版) {#integrate-tidb-cloud-with-datadog-beta}

TiDB CloudはDatadogとの連携（ベータ版）をサポートしています。TiDB TiDB Cloudを設定して、TiDBクラスターのメトリクスデータを[データドッグ](https://www.datadoghq.com/)に送信できます。その後、これらのメトリクスをDatadogダッシュボードで直接確認できるようになります。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Datadog と統合するには、Datadog アカウントと[Datadog APIキー](https://app.datadoghq.com/organization-settings/api-keys)必要です。Datadog アカウントを初めて作成すると、Datadog から API キーが付与されます。

    Datadog アカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`アクセス権またはTiDB Cloudの対象プロジェクトへの`Project Member`アクセス権が必要です。

## 制限 {#limitation}

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターでは Datadog 統合を使用できません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Datadog 統合は使用できません。

## 手順 {#steps}

### ステップ1. Datadog APIキーとの統合 {#step-1-integrate-with-your-datadog-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[統合]**をクリックします。

3.  **[統合]**ページで、 **[Datadog への統合 (ベータ版)]**をクリックします。

4.  Datadog の API キーを入力し、Datadog のサイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストに失敗した場合はエラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

### ステップ2. DatadogにTiDB Cloud統合をインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

1.  [データドッグ](https://app.datadoghq.com)にログインします。
2.  Datadogの**TiDB Cloud統合**ページ（ [https://app.datadoghq.com/account/settings#integrations/tidb-cloud](https://app.datadoghq.com/account/settings#integrations/tidb-cloud) ）に移動します。
3.  **「コンフィグレーション」**タブで、 **「統合をインストール」を**クリックします。 [**TiDBCloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードが[**ダッシュボードリスト**](https://app.datadoghq.com/dashboard/lists)に表示されます。

## 事前に構築されたダッシュボード {#pre-built-dashboard}

統合の**Datadog**カードにある**「ダッシュボード**」リンクをクリックします。TiDBクラスターの事前構築済みダッシュボードが表示されます。

## Datadogで利用可能なメトリクス {#metrics-available-to-datadog}

Datadog は、TiDB クラスターの次のメトリック データを追跡します。

| メトリック名                                     | メトリックタイプ | ラベル                                                                                                               | 説明                                                                                           |
| :----------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| tidb_cloud.db_database_time                | ゲージ      | sql_type: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | すべてのプロセスの CPU 時間とアイドル状態ではない待機時間を含む、TiDB で実行されているすべての SQL ステートメントによって 1 秒あたりに消費される合計時間。       |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                        | すべての TiDB インスタンスで 1 秒あたりに実行された SQL ステートメントの数。SELECT、INSERT、UPDATE などのステートメントの種類に応じてカウントされます。 |
| tidb_cloud.db_平均クエリ実行時間                    | ゲージ      | sql_type: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | クライアントのネットワーク要求が TiDB に送信されてから、TiDB が要求を実行した後にクライアントに返されるまでの期間。                              |
| tidb_cloud.db_failed_queries               | ゲージ      | タイプ: executor:xxxx|parser:xxxx|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`    | 各 TiDB インスタンスで 1 秒あたりに発生する SQL 実行エラーに応じたエラー タイプ (構文エラーや主キーの競合など) の統計。                        |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | TiDBサーバーの現在の接続数。                                                                             |
| tidb_cloud.db_active_connections           | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | アクティブな接続の数。                                                                                  |
| tidb_cloud.db_disconnections               | ゲージ      | 結果: OK|エラー|未定<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                         | 切断されたクライアントの数。                                                                               |
| tidb_cloud.db_command_per_second           | ゲージ      | タイプ: Query|StmtPrepare|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`            | TiDB が 1 秒あたりに処理したコマンドの数。コマンド実行結果の成功または失敗によって分類されます。                                         |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | [プランキャッシュ](/sql-prepared-plan-cache.md)回使用するクエリの統計。実行プランキャッシュは、プリペアドステートメントコマンドのみをサポートします。   |
| tidb_cloud.db_transaction_per_second       | ゲージ      | txn_mode:悲観的|楽観的<br/>タイプ: 中止|コミット|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb` | 1 秒あたりに実行されるトランザクションの数。                                                                      |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク使用量（バイト単位）。                                                             |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                             |
| tidb_cloud.node_cpu_seconds_total          | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                              |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                            |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの使用済みメモリ(バイト単位)。                                                        |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                         |
