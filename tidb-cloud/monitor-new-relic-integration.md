---
title: Integrate TiDB Cloud with New Relic (Beta)
summary: New Relic 統合を使用して TiDB クラスターを監視する方法を学習します。
---

# TiDB Cloud をNew Relic と統合する (ベータ版) {#integrate-tidb-cloud-with-new-relic-beta}

TiDB Cloud はNew Relic 統合 (ベータ版) をサポートしています。TiDB TiDB Cloudを設定して、TiDB クラスターのメトリック データを[ニューレリック](https://newrelic.com/)に送信できます。その後、これらのメトリックを New Relic ダッシュボードで直接表示できます。

## 前提条件 {#prerequisites}

-   TiDB Cloud をNew Relic と統合するには、New Relic アカウントと[New Relic APIキー](https://one.newrelic.com/admin-portal/api-keys/home?)必要です。New Relic アカウントを初めて作成すると、New Relic から API キーが付与されます。

    New Relic アカウントをお持ちでない場合は、サインアップしてください[ここ](https://newrelic.com/signup) 。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織に対する**組織所有者**アクセス権、またはTiDB Cloudの対象プロジェクトに対する**プロジェクト メンバー**アクセス権が必要です。

## 制限 {#limitation}

[TiDB Cloudサーバーレス クラスター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)では New Relic 統合は使用できません。

## 手順 {#steps}

### ステップ1. New Relic APIキーとの統合 {#step-1-integrate-with-your-new-relic-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定]**をクリックします。</mdsvgicon>

3.  プロジェクトの**プロジェクト設定**ページで、左側のナビゲーション ペインの**[統合]**をクリックし、 **[New Relic への統合 (ベータ版)]**をクリックします。

4.  New Relic の API キーを入力し、New Relic のサイトを選択します。

5.  **「統合のテスト」**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストが失敗した場合は、エラー メッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  統合を完了するには、 **「確認」**をクリックします。

### ステップ2. New RelicにTiDB Cloudダッシュボードを追加する {#step-2-add-tidb-cloud-dashboard-in-new-relic}

1.  [ニューレリック](https://one.newrelic.com/)にログインします。
2.  **「データの追加」**をクリックし、 `TiDB Cloud`を検索して、 **TiDB Cloud監視**ページに移動します。または、 [リンク](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e)をクリックしてページに直接アクセスすることもできます。
3.  アカウント ID を選択し、New Relic でダッシュボードを作成します。

## 事前構築されたダッシュボード {#pre-built-dashboard}

統合の**New Relic**カードの**ダッシュボード**リンクをクリックします。TiDB クラスターの事前構築されたダッシュボードが表示されます。

## New Relicで利用可能なメトリクス {#metrics-available-to-new-relic}

New Relic は、TiDB クラスターの次のメトリック データを追跡します。

| メトリック名                                     | メトリックタイプ | ラベル                                                                                                                                   | 説明                                                                                                          |
| :----------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------- |
| tidb_cloud.db_データベース時間                     | ゲージ      | sql_type: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                        | すべてのプロセスの CPU 時間とアイドル状態ではない待機時間を含む、TiDB で実行されているすべての SQL ステートメントによって 1 秒あたりに消費される合計時間。                      |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                             | すべての TiDB インスタンスで 1 秒あたりに実行された SQL ステートメントの数`SELECT` 、 `INSERT` 、 `UPDATE` 、およびその他のタイプのステートメントに従ってカウントされます。 |
| tidb_cloud.db_平均クエリ期間                      | ゲージ      | sql_type: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                        | クライアントのネットワーク要求が TiDB に送信されてから、TiDB が要求を実行した後にクライアントに返されるまでの期間。                                             |
| tidb_cloud.db_失敗したクエリ                      | ゲージ      | タイプ: executor:xxxx|parser:xxxx|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`         | 各 TiDB インスタンスで 1 秒あたりに発生する SQL 実行エラーに応じたエラー タイプ (構文エラーや主キーの競合など) の統計。                                       |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | TiDBサーバー内の現在の接続数。                                                                                           |
| tidb_cloud.db_アクティブ接続                      | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | アクティブな接続の数。                                                                                                 |
| tidb_cloud.db_切断                           | ゲージ      | 結果: OK|エラー|未確定<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                             | 切断されたクライアントの数。                                                                                              |
| tidb_cloud.db_コマンド/秒                       | ゲージ      | タイプ: Query|StmtPrepare|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                 | TiDB が 1 秒あたりに処理するコマンドの数。コマンド実行結果の成功または失敗によって分類されます。                                                        |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | 1 秒あたり[プランキャッシュ](/sql-prepared-plan-cache.md)使用するクエリの統計。実行プラン キャッシュは、プリペアドステートメントコマンドのみをサポートします。            |
| tidb_cloud.db_トランザクション/秒                   | ゲージ      | txn_mode:悲観的|楽観的<br/><br/>タイプ: 中止|コミット|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb` | 1 秒あたりに実行されるトランザクションの数。                                                                                     |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tiflash                          | TiKV/ TiFlashノードのディスク使用量（バイト単位）。                                                                            |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tiflash                          | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                            |
| tidb_cloud.node_cpu_秒数_合計                  | カウント     | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                             |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                           |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの使用済みメモリ(バイト単位)。                                                                       |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                                        |
