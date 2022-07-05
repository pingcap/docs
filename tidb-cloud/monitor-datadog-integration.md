---
title: Datadog Integration (Third-Party Monitoring Service)
summary: Learn how to monitor your TiDB cluster with the Datadog integration.
---

# Datadogの統合 {#datadog-integration}

TiDBクラスターに関するメトリックデータを[Datadog](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリックをDatadogダッシュボードで直接表示できます。

## 前提条件 {#prerequisites}

-   TiDB CloudをDatadogと統合するには、Datadogアカウントと[DatadogAPIキー](https://app.datadoghq.com/organization-settings/api-keys)が必要です。 Datadogは、最初にDatadogアカウントを作成するときにAPIキーを付与します。

    Datadogアカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`つのアクセス、またはTiDB Cloudのターゲットプロジェクトへの`Project Member`のアクセスが必要です。

## 制限 {#limitation}

[開発者層クラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)ではDatadog統合を使用できません。

## 手順 {#steps}

### ステップ1.DatadogAPIキーと統合する {#step-1-integrate-with-your-datadog-api-key}

1.  TiDB Cloudコンソールで、Datadog統合のターゲットプロジェクトを選択し、[**プロジェクト設定**]タブをクリックします。

2.  左側のペインで、[**統合**]をクリックします。

3.  [ **Datadogへの統合]を**クリックします。

4.  DatadogのAPIキーを入力し、Datadogのサイトを選択します。

5.  [**統合のテスト]**をクリックします。

    -   テストが成功すると、[**確認**]ボタンが表示されます。
    -   テストが失敗すると、エラーメッセージが表示されます。トラブルシューティングのメッセージに従って、統合を再試行してください。

6.  [**確認]**をクリックして統合を完了します。

### ステップ2.DatadogにTiDB Cloud統合をインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

1.  [Datadog](https://app.datadoghq.com)にログインします。
2.  Datadogの**TiDB Cloud**ページ（ [https://app.datadoghq.com/account/settings#integrations/tidb-cloud](https://app.datadoghq.com/account/settings#integrations/tidb-cloud) ）に移動します。
3.  [**Configuration / コンフィグレーション**]タブで、[<strong>統合のインストール</strong>]をクリックします。 [**TiDBCloudクラスターの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードが[**ダッシュボードリスト**](https://app.datadoghq.com/dashboard/lists)に表示されます。

## 構築済みのダッシュボード {#pre-built-dashboard}

統合の**Datadog**カードの[<strong>ダッシュボード</strong>]リンクをクリックします。 TiDBクラスターの構築済みダッシュボードを確認できます。

## Datadogで利用可能なメトリック {#metrics-available-to-datadog}

Datadogは、TiDBクラスターの次のメトリックデータを追跡します。

| メトリック名                                 | メトリックタイプ | ラベル                                                                                                                          | 説明                              |
| :------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| tidb_cloud.db_queries_total            | カウント     | sql_type： `Select\|Insert\|...`<br/> cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…`<br/>コンポーネント： `tidb`        | 実行されたステートメントの総数                 |
| tidb_cloud.db_failed_queries_total     | カウント     | タイプ： `planner:xxx\|executor:2345\|...`<br/> cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…`<br/>コンポーネント： `tidb` | 実行エラーの総数                        |
| tidb_cloud.db_connections              | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…`<br/>コンポーネント： `tidb`                                             | TiDBサーバーの現在の接続数                 |
| tidb_cloud.db_query_duration_seconds   | ヒストグラム   | sql_type： `Select\|Insert\|...`<br/> cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…`<br/>コンポーネント： `tidb`        | ステートメントの期間ヒストグラム                |
| tidb_cloud.node_storage_used_bytes     | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント： `tikv\|tiflash`             | TiKV/TiFlashノードのディスク使用量バイト      |
| tidb_cloud.node_storage_capacity_bytes | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント： `tikv\|tiflash`             | TiKV/TiFlashノードのディスク容量バイト       |
| tidb_cloud.node_cpu_seconds_total      | カウント     | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント： `tidb\|tikv\|tiflash`         | TiDB / TiKV/TiFlashノードのCPU使用率   |
| tidb_cloud.node_cpu_capacity_cores     | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント： `tidb\|tikv\|tiflash`         | TiDB / TiKV/TiFlashノードのCPU制限コア  |
| tidb_cloud.node_memory_used_bytes      | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント： `tidb\|tikv\|tiflash`         | TiDB / TiKV/TiFlashノードの使用メモリバイト |
| tidb_cloud.node_memory_capacity_bytes  | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント： `tidb\|tikv\|tiflash`         | TiDB / TiKV/TiFlashノードのメモリ容量バイト |
