---
title: Integrate TiDB Cloud with New Relic (Beta)
summary: Learn how to monitor your TiDB cluster with the New Relic integration.
---

# TiDB Cloudと New Relic を統合 (ベータ版) {#integrate-tidb-cloud-with-new-relic-beta}

TiDB Cloud はNew Relic 統合 (ベータ) をサポートしています。 TiDB クラスターのメトリック データを[ニューレリック](https://newrelic.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリクスを New Relic ダッシュボードで直接表示できるようになります。

## 前提条件 {#prerequisites}

-   TiDB Cloudを New Relic と統合するには、New Relic アカウントと[New Relic APIキー](https://one.newrelic.com/admin-portal/api-keys/home?)が必要です。 New Relic では、最初に New Relic アカウントを作成するときに API キーを付与します。

    New Relic アカウントをお持ちでない場合は、サインアップしてください[ここ](https://newrelic.com/signup) 。

-   TiDB Cloudのサードパーティ統合設定を編集するには、**組織所有者が**組織にアクセスできるか、**プロジェクト メンバーが**TiDB Cloudのターゲット プロジェクトにアクセスできる必要があります。

## 制限 {#limitation}

[TiDB サーバーレスクラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)では New Relic 統合を使用できません。

## ステップ {#steps}

### ステップ 1. New Relic API キーと統合する {#step-1-integrate-with-your-new-relic-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">複数のプロジェクトがある場合は、左下隅でターゲット プロジェクトに切り替え、 **[プロジェクト設定]**をクリックします。</mdsvgicon>

3.  プロジェクトの [**プロジェクト設定]**ページで、左側のナビゲーション ペインで**[統合]**をクリックし、 **[New Relic への統合 (ベータ)]**をクリックします。

4.  New Relic の API キーを入力し、New Relic のサイトを選択します。

5.  **「統合のテスト」**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストが失敗した場合は、エラー メッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

### ステップ 2. New Relic にTiDB Cloudダッシュボードを追加する {#step-2-add-tidb-cloud-dashboard-in-new-relic}

1.  [ニューレリック](https://one.newrelic.com/)にログインします。
2.  **[データの追加]**をクリックし、 `TiDB Cloud`を検索して、 **TiDB Cloudモニタリング**ページに移動します。または、 [リンク](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e)クリックしてページに直接アクセスすることもできます。
3.  アカウント ID を選択し、New Relic でダッシュボードを作成します。

## 事前に構築されたダッシュボード {#pre-built-dashboard}

統合の**New Relic**カードにある**[ダッシュボード]**リンクをクリックします。 TiDB クラスターの事前構築されたダッシュボードを確認できます。

## New Relic で利用可能なメトリクス {#metrics-available-to-new-relic}

New Relic は、TiDB クラスターの次のメトリクス データを追跡します。

| メトリクス名                                     | メトリックタイプ | ラベル                                                                                                                                   | 説明                                                                                                            |
| :----------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------ |
| tidb_cloud.db_database_time                | ゲージ      | sql_type: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                        | TiDB で実行されているすべての SQL ステートメントによって消費された 1 秒あたりの合計時間 (すべてのプロセスの CPU 時間と非アイドル待機時間を含む)。                           |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                             | すべての TiDB インスタンスで 1 秒あたりに実行される SQL ステートメントの数。 `SELECT` 、 `INSERT` 、 `UPDATE` 、およびその他のタイプのステートメントに従ってカウントされます。 |
| tidb_cloud.db_average_query_duration       | ゲージ      | sql_type: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                        | クライアントのネットワーク リクエストが TiDB に送信されてから、TiDB がリクエストを実行した後にリクエストがクライアントに返されるまでの期間。                                  |
| tidb_cloud.db_failed_queries               | ゲージ      | タイプ: 実行者:xxxx|パーサー:xxxx|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                | 各 TiDB インスタンスで 1 秒あたりに発生する SQL 実行エラーに応じたエラー タイプ (構文エラーや主キーの競合など) の統計。                                         |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | TiDBサーバー内の現在の接続の数。                                                                                            |
| tidb_cloud.db_active_connections           | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | アクティブな接続の数。                                                                                                   |
| tidb_cloud.db_disconnections               | ゲージ      | 結果: OK|エラー|未定<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                              | 切断されたクライアントの数。                                                                                                |
| tidb_cloud.db_command_per_second           | ゲージ      | タイプ: クエリ|StmtPrepare|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                   | TiDB によって 1 秒あたりに処理されたコマンドの数。コマンドの実行結果の成功または失敗に従って分類されます。                                                     |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | [プランキャッシュ](/sql-prepared-plan-cache.md)秒あたり 1 を使用したクエリの統計。実行プラン キャッシュは、プリペアドステートメントコマンドのみをサポートします。            |
| tidb_cloud.db_transaction_per_second       | ゲージ      | txn_mode:悲観的|楽観的<br/><br/>タイプ: 中止|コミット|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb` | 1 秒あたりに実行されるトランザクションの数。                                                                                       |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tflash                           | TiKV/ TiFlashノードのディスク使用量 (バイト単位)。                                                                             |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tflash                           | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                              |
| tidb_cloud.node_cpu_seconds_total          | カウント     | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tflash-0…<br/><br/>コンポーネント: tidb|tikv|tflash                         | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                               |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tflash-0…<br/><br/>コンポーネント: tidb|tikv|tflash                         | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                             |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tflash-0…<br/><br/>コンポーネント: tidb|tikv|tflash                         | TiDB/TiKV/ TiFlashノードの使用済みメモリ(バイト単位)。                                                                         |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tflash-0…<br/><br/>コンポーネント: tidb|tikv|tflash                         | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                                          |
