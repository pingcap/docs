---
title: TiDB Cloud Release Notes in 2022
summary: Learn about the release notes of TiDB Cloud in 2022.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2022年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2022}

このページには、2022年の[TiDB Cloud](https://en.pingcap.com/tidb-cloud/)のリリースノートがリストされています。

## 2022年5月24日 {#may-24-2022}

-   専用層クラスタを作成または復元するときに、TiDBポート番号のカスタマイズをサポートする

## 2022年5月19日 {#may-19-2022}

-   開発者層クラスタの作成のためにAWSリージョン`Frankfurt`のサポートを追加します

## 2022年5月18日 {#may-18-2022}

-   GitHubアカウントで[サインアップ](https://tidbcloud.com/signup)つのTiDB Cloudをサポートする

## 2022年5月13日 {#may-13-2022}

-   Googleアカウントで[サインアップ](https://tidbcloud.com/signup)つのTiDB Cloudをサポートする

## 2022年5月1日 {#may-1-2022}

-   クラスタを作成または復元するときに、TiDB、TiKV、およびTiFlash<sup>ベータ</sup>のvCPUサイズの構成をサポートする
-   クラスタ作成のためのAWSリージョン`Mumbai`のサポートを追加します
-   コンピューティング、ストレージ、およびデータ転送のコストを[TiDB Cloud課金](/tidb-cloud/tidb-cloud-billing.md)に更新します

## 2022年4月7日 {#april-7-2022}

-   開発者層向けにTiDBCloudを[TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr)にアップグレードします

## 2022年3月31日 {#march-31-2022}

TiDBCloudが一般提供になりました。 [サインアップ](https://tidbcloud.com/signup)を選択して、次のいずれかのオプションを選択できます。

-   開発者層を無料で始めましょう
-   14日間のPoCトライアルを無料で申し込む
-   専用層でフルアクセスを取得

## 2022年3月25日 {#march-25-2022}

新機能：

-   サポート[TiDB Cloudの組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)

    TiDB Cloudの組み込みアラート機能を使用すると、プロジェクト内のTiDBCloudクラスタがTiDBCloudの組み込みアラート条件の1つをトリガーするたびに、電子メールで通知を受けることができます。

## 2022年3月15日 {#march-15-2022}

一般的な変更：

-   固定クラスタサイズのクラスタ層はもうありません。 TiDB、TiKV、およびTiFlash<sup>ベータ</sup>のクラスタサイズを簡単にカスタマイズできます。
-   TiFlashを使用しない既存のクラスタへのTiFlash<sup>ベータ</sup>ノードの追加をサポートします。
-   新しいクラスタを作成するときに、ストレージサイズ（500〜2048 GiB）の指定をサポートします。クラスタの作成後にストレージサイズを変更することはできません。
-   新しいパブリックリージョンを導入します： `eu-central-1` 。
-   8 vCPU TiFlash<sup>ベータ版</sup>を廃止し、16vCPUTiFlashを提供します。
-   CPUとストレージの価格を分けてください（どちらも30％のパブリックプレビュー割引があります）。
-   [課金情報](/tidb-cloud/tidb-cloud-billing.md)と[価格表](https://en.pingcap.com/tidb-cloud/#pricing)を更新します。

新機能：

-   サポート[PrometheusとGrafanaの統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)

    PrometheusとGrafanaの統合により、TiDB Cloudエンドポイントから主要なメトリックを読み取り、 [Grafana](https://grafana.com/)を使用してメトリックを表示するように[プロメテウス](https://prometheus.io/)のサービスを構成できます。

-   新しいクラスタの選択したリージョンに基づいたデフォルトのバックアップ時間の割り当てをサポート

    詳細については、 [TiDBクラスターデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

## 2022年3月4日 {#march-04-2022}

新機能：

-   サポート[Datadogの統合](/tidb-cloud/monitor-datadog-integration.md)

    Datadog統合を使用すると、TiDBクラスターに関するメトリックデータを[Datadog](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリックをDatadogダッシュボードで直接表示できます。

## 2022年2月15日 {#february-15-2022}

一般的な変更：

-   開発者層向けにTiDBCloudを[TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0)にアップグレードします

改善：

-   [CSVファイル](/tidb-cloud/import-csv-files.md)または[ApacheParquetファイル](/tidb-cloud/import-parquet-files.md)をTiDBCloudにインポートする際のカスタムファイル名の使用をサポート

## 2022年1月11日 {#january-11-2022}

一般的な変更：

-   TiDB Operatorを[v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)にアップグレードします

改善：

-   [**接続**]ページのMySQLクライアントに推奨オプション`--connect-timeout 15`を追加します

バグの修正：

-   パスワードに一重引用符が含まれている場合、ユーザーがクラスタを作成できない問題を修正します
-   組織に所有者が1人しかいない場合でも、所有者を削除したり、別の役割に変更したりできるという問題を修正します
