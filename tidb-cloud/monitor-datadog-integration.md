---
title: Datadog Integration (Third-Party Monitoring Service)
summary: Learn how to monitor your TiDB cluster with the Datadog integration.
---

# Datadog 統合 {#datadog-integration}

TiDB クラスターに関するメトリック データを[データドッグ](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリクスを Datadog ダッシュボードで直接表示できます。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Datadog と統合するには、Datadog アカウントと[Datadog API キー](https://app.datadoghq.com/organization-settings/api-keys)が必要です。初めて Datadog アカウントを作成すると、Datadog は API キーを付与します。

    Datadog アカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`つのアクセス権またはTiDB Cloudのターゲット プロジェクトへの`Project Member`のアクセス権が必要です。

## 制限 {#limitation}

[開発者層のクラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)で Datadog 統合を使用することはできません。

## 手順 {#steps}

### ステップ 1. Datadog API キーと統合する {#step-1-integrate-with-your-datadog-api-key}

1.  TiDB Cloudコンソールで、Datadog 統合のターゲット プロジェクトを選択し、[**プロジェクト設定**] タブをクリックします。

2.  左ペインで [**統合**] をクリックします。

3.  **Datadog への統合 を**クリックします。

4.  Datadog の API キーを入力し、Datadog のサイトを選択します。

5.  [**統合のテスト]**をクリックします。

    -   テストが成功すると、**確認**ボタンが表示されます。
    -   テストが失敗すると、エラー メッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  [**確認]**をクリックして統合を完了します。

### ステップ 2. Datadog にTiDB Cloud統合をインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

1.  [データドッグ](https://app.datadoghq.com)にログインします。
2.  Datadog の**TiDB Cloud統合**ページ ( [https://app.datadoghq.com/account/settings#integrations/tidb-cloud](https://app.datadoghq.com/account/settings#integrations/tidb-cloud) ) に移動します。
3.  [**Configuration / コンフィグレーション**] タブで、 [<strong>統合のインストール</strong>] をクリックします。 [**TiDBCloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードが[**ダッシュボード一覧**](https://app.datadoghq.com/dashboard/lists)に表示されます。

## 事前構築済みのダッシュボード {#pre-built-dashboard}

統合の**Datadog**カードで [<strong>ダッシュボード</strong>] リンクをクリックします。 TiDB クラスターの事前構築済みダッシュボードが表示されます。

## Datadog で利用可能なメトリクス {#metrics-available-to-datadog}

Datadog は、TiDB クラスターの次のメトリクス データを追跡します。

| 指標名                                    | 指標タイプ  | ラベル                                                                                                                  | 説明                              |
| :------------------------------------- | :----- | :------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| tidb_cloud.db_queries_total            | カウント   | sql_type: `Select\|Insert\|...`<br/>クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | 実行されたステートメントの総数                 |
| tidb_cloud.db_failed_queries_total     | カウント   | タイプ: `planner:xxx\|executor:2345\|...`<br/>クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb` | 実行エラーの総数                        |
| tidb_cloud.db_connections              | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`                                            | TiDBサーバーの現在の接続数                 |
| tidb_cloud.db_query_duration_seconds   | ヒストグラム | sql_type: `Select\|Insert\|...`<br/>クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | ステートメントの期間ヒストグラム                |
| tidb_cloud.node_storage_used_bytes     | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`            | TiKV/TiFlash ノードのディスク使用量バイト     |
| tidb_cloud.node_storage_capacity_bytes | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`            | TiKV/TiFlash ノードのディスク容量バイト      |
| tidb_cloud.node_cpu_seconds_total      | カウント   | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/TiFlash ノードの CPU 使用率  |
| tidb_cloud.node_cpu_capacity_cores     | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/TiFlash ノードの CPU 制限コア |
| tidb_cloud.node_memory_used_bytes      | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/TiFlash ノードの使用メモリバイト数 |
| tidb_cloud.node_memory_capacity_bytes  | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/TiFlash ノードのメモリ容量バイト  |
