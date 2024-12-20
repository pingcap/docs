---
title: Integrate TiDB Cloud with Datadog (Beta)
summary: Datadog 統合を使用して TiDB クラスターを監視する方法を学習します。
---

# TiDB Cloudと Datadog を統合する (ベータ版) {#integrate-tidb-cloud-with-datadog-beta}

TiDB Cloud はDatadog 統合 (ベータ版) をサポートしています。TiDB TiDB Cloudを設定して、TiDB クラスターに関するメトリック データを[データドッグ](https://www.datadoghq.com/)に送信できます。その後、これらのメトリックを Datadog ダッシュボードで直接表示できます。

## 前提条件 {#prerequisites}

-   TiDB Cloud をDatadog と統合するには、Datadog アカウントと[Datadog API キー](https://app.datadoghq.com/organization-settings/api-keys)が必要です。Datadog アカウントを初めて作成すると、Datadog から API キーが付与されます。

    Datadog アカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`アクセス権またはTiDB Cloudの対象プロジェクトへの`Project Member`アクセス権が必要です。

## 制限 {#limitation}

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターでは Datadog 統合を使用できません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Datadog 統合は使用できません。

## 手順 {#steps}

### ステップ1. Datadog APIキーとの統合 {#step-1-integrate-with-your-datadog-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定]**をクリックします。</mdsvgicon>

3.  プロジェクトの「**プロジェクト設定」**ページで、左側のナビゲーション ペインの**「統合」**をクリックし、 **「Datadog への統合 (ベータ版)」**をクリックします。

4.  Datadog の API キーを入力し、Datadog のサイトを選択します。

5.  **「統合のテスト」**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストが失敗した場合は、エラー メッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  統合を完了するには、 **「確認」**をクリックします。

### ステップ2. DatadogにTiDB Cloud統合をインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

1.  [データドッグ](https://app.datadoghq.com)にログインします。
2.  Datadogの**TiDB Cloud Integration**ページ（ [https://app.datadoghq.com/account/settings#integrations/tidb-cloud](https://app.datadoghq.com/account/settings#integrations/tidb-cloud) ）に移動します。
3.  **「コンフィグレーション」**タブで、 **「統合のインストール」**をクリックします。 [**TiDBCloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードが[**ダッシュボードリスト**](https://app.datadoghq.com/dashboard/lists)に表示されます。

## 事前構築されたダッシュボード {#pre-built-dashboard}

統合の**Datadog**カードにある**ダッシュボード**リンクをクリックします。TiDB クラスターの事前構築されたダッシュボードが表示されます。

## Datadog で利用可能なメトリクス {#metrics-available-to-datadog}

Datadog は、TiDB クラスターの次のメトリック データを追跡します。

| メトリック名                                     | メトリックタイプ | ラベル                                                                                                               | 説明                                                                                               |
| :----------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| tidb_cloud.db_データベース時間                     | ゲージ      | sql_type: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | すべてのプロセスの CPU 時間とアイドル状態ではない待機時間を含む、TiDB で実行されているすべての SQL ステートメントによって 1 秒あたりに消費される合計時間。           |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                        | すべての TiDB インスタンスで 1 秒あたりに実行される SQL ステートメントの数。SELECT、INSERT、UPDATE などのステートメントの種類に応じてカウントされます。     |
| tidb_cloud.db_平均クエリ期間                      | ゲージ      | sql_type: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | クライアントのネットワーク要求が TiDB に送信されてから、TiDB が要求を実行した後にクライアントに返されるまでの期間。                                  |
| tidb_cloud.db_失敗したクエリ                      | ゲージ      | タイプ: executor:xxxx|parser:xxxx|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`    | 各 TiDB インスタンスで 1 秒あたりに発生する SQL 実行エラーに応じたエラー タイプ (構文エラーや主キーの競合など) の統計。                            |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | TiDBサーバー内の現在の接続数。                                                                                |
| tidb_cloud.db_アクティブ接続                      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | アクティブな接続の数。                                                                                      |
| tidb_cloud.db_切断                           | ゲージ      | 結果: OK|エラー|未確定<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                        | 切断されたクライアントの数。                                                                                   |
| tidb_cloud.db_コマンド/秒                       | ゲージ      | タイプ: Query|StmtPrepare|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`            | TiDB が 1 秒あたりに処理するコマンドの数。コマンド実行結果の成功または失敗によって分類されます。                                             |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | 1 秒あたり[プランキャッシュ](/sql-prepared-plan-cache.md)使用するクエリの統計。実行プラン キャッシュは、プリペアドステートメントコマンドのみをサポートします。 |
| tidb_cloud.db_トランザクション/秒                   | ゲージ      | txn_mode:悲観的|楽観的<br/>タイプ: 中止|コミット|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb` | 1 秒あたりに実行されるトランザクションの数。                                                                          |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク使用量（バイト単位）。                                                                 |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                 |
| tidb_cloud.node_cpu_秒数_合計                  | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                  |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの使用済みメモリ(バイト単位)。                                                            |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                             |
