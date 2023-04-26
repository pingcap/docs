---
title: Integrate TiDB Cloud with New Relic
summary: Learn how to monitor your TiDB cluster with the New Relic integration.
---

# TiDB CloudをNew Relic と統合する {#integrate-tidb-cloud-with-new-relic}

TiDB クラスターのメトリック データを[ニューレリック](https://newrelic.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリクスを New Relic ダッシュボードで直接表示できます。

## 前提条件 {#prerequisites}

-   TiDB Cloudを New Relic と統合するには、New Relic アカウントと[New Relic API キー](https://one.newrelic.com/admin-portal/api-keys/home?)が必要です。 New Relic アカウントを最初に作成すると、New Relic から API キーが付与されます。

    New Relic アカウントをお持ちでない場合は、サインアップしてください[ここ](https://newrelic.com/signup) 。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への**組織所有者**アクセス権、またはTiDB Cloudのターゲット プロジェクトへの<strong>プロジェクト メンバー</strong>アクセス権が必要です。

## 制限 {#limitation}

[Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)で New Relic 統合を使用することはできません。

## 手順 {#steps}

### ステップ 1. New Relic API キーと統合する {#step-1-integrate-with-your-new-relic-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ペインで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えてから、 **[管理]** &gt; <strong>[統合]</strong>をクリックします。
    -   プロジェクトが 1 つしかない場合は、 **[管理]** &gt; <strong>[統合]</strong>をクリックします。

3.  **Integration to New Relic を**クリックします。

4.  New Relic の API キーを入力し、New Relic のサイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、**確認**ボタンが表示されます。
    -   テストが失敗すると、エラー メッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **[確認]**をクリックして統合を完了します。

### ステップ 2. New Relic にTiDB Cloudダッシュボードを追加する {#step-2-add-tidb-cloud-dashboard-in-new-relic}

1.  [ニューレリック](https://one.newrelic.com/)にログインします。
2.  **Add Data を**クリックし、 `TiDB Cloud`を検索してから、 <strong>TiDB Cloud Monitoring</strong>ページに移動します。または、 [リンク](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e)クリックしてページに直接アクセスすることもできます。
3.  アカウント ID を選択し、New Relic でダッシュボードを作成します。

## 事前構築済みのダッシュボード {#pre-built-dashboard}

統合の**New Relic**カードで<strong>[ダッシュボード]</strong>リンクをクリックします。 TiDB クラスターの事前構築済みダッシュボードが表示されます。

## New Relic で利用可能なメトリクス {#metrics-available-to-new-relic}

New Relic は、TiDB クラスターの次のメトリック データを追跡します。

| 指標名                                        | 指標タイプ | ラベル                                                                                                                                  | 説明                                                                                                          |
| :----------------------------------------- | :---- | :----------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| tidb_cloud.db_database_time                | ゲージ   | sql_type: 選択|挿入|...<br/><br/>クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                        | すべてのプロセスの CPU 時間と非アイドル待機時間を含む、TiDB で実行されているすべての SQL ステートメントによって消費された 1 秒あたりの合計時間。                           |
| tidb_cloud.db_query_per_second             | ゲージ   | タイプ: 選択|挿入|...<br/><br/>クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                             | `SELECT` 、 `INSERT` 、 `UPDATE` 、およびその他のタイプのステートメントに従ってカウントされる、すべての TiDB インスタンスで 1 秒あたりに実行される SQL ステートメントの数。 |
| tidb_cloud.db_average_query_duration       | ゲージ   | sql_type: 選択|挿入|...<br/><br/>クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                        | クライアントのネットワーク要求が TiDB に送信されてから、TiDB が要求を実行した後に要求がクライアントに返されるまでの時間。                                          |
| tidb_cloud.db_failed_queries               | ゲージ   | タイプ: エグゼキューター:xxxx|パーサー:xxxx|...<br/><br/>クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`           | 各 TiDB インスタンスで 1 秒あたりに発生した SQL 実行エラーに基づく、エラーの種類 (構文エラーや主キーの競合など) の統計。                                       |
| tidb_cloud.db_total_connection             | ゲージ   | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | TiDBサーバーの現在の接続数。                                                                                            |
| tidb_cloud.db_active_connections           | ゲージ   | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | アクティブな接続の数。                                                                                                 |
| tidb_cloud.db_disconnections               | ゲージ   | 結果: OK|エラー|不明<br/><br/>クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                              | 切断されたクライアントの数。                                                                                              |
| tidb_cloud.db_command_per_second           | ゲージ   | タイプ: クエリ|StmtPrepare|...<br/><br/>クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                   | コマンド実行結果の成否で分類した、1秒間にTiDBが処理したコマンド数。                                                                        |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ   | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | [プラン キャッシュ](/sql-prepared-plan-cache.md)秒あたり 1 件を使用したクエリの統計。実行プラン キャッシュは、プリペアドステートメントコマンドのみをサポートします。        |
| tidb_cloud.db_transaction_per_second       | ゲージ   | txn_mode:悲観的|楽観的<br/><br/>タイプ: 中止|コミット|...<br/><br/>クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb` | 1 秒あたりに実行されたトランザクションの数。                                                                                     |
| tidb_cloud.node_storage_used_bytes         | ゲージ   | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tiflash                          | TiKV/ TiFlashノードのディスク使用量 (バイト単位)。                                                                           |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ   | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tiflash                          | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                            |
| tidb_cloud.node_cpu_seconds_total          | カウント  | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                             |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ   | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                           |
| tidb_cloud.node_memory_used_bytes          | ゲージ   | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの使用メモリ(バイト単位)。                                                                         |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ   | クラスタ名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                                        |
