---
title: TiDB Cloud BYOC IAM 権限を設定する
summary: このドキュメントでは、TiDB Cloud BYOC コントローラーのアクセスに必要な IAM 設定について説明します。
---

# TiDB Cloud BYOC IAM 権限を設定する

AWS 環境の準備が完了したら、TiDB Cloud コントロールプレーンがお客様のアカウント内のリソースを管理できるように認可する必要があります。これは、最小権限の原則に基づいて必要な IAM ロールを作成するブートストラップスクリプトを実行することで実現します。

## 準備 {#preparation}

スクリプトを実行する前に、以下を確認してください。

1. **AWS CLI のインストール:** CLI は、IAM ロールとポリシーを作成する権限を持つ Access Key で設定されている必要があります。
2. **TiDB Cloud のアカウント情報:** **Control Plane Account ID** と **Clinic Account ID** を取得するために、TiDB Cloud のサポート担当者に連絡してください。

## パラメーターを収集する {#gather-parameters}

以下の表を使用して、スクリプトに必要なパラメーターを対応付けてください。

| パラメーター | ソース | 説明 |
| :---- | :---- | :---- |
| `<ControlPlaneAccountId>` | **TiDB Support** | TiDB コントロールプレーンの AWS Account ID。 |
| `<ClinicAccountId>` | **TiDB Support** | TiDB Clinic サービス用の AWS Account ID。 |
| `<TidbHostedZoneId>` | [必要な情報](/tidb-cloud/byoc/byoc-prepare-environment-aws.md#summary-required-information) | 作成した TiDB クラスターのホストゾーンの ID。 |
| `<TidbPCAArn>` | [必要な情報](/tidb-cloud/byoc/byoc-prepare-environment-aws.md#summary-required-information) | 作成した Private CA の ARN。 |

## ブートストラップスクリプトを実行する {#execute-bootstrapping-script}

1. [PingCAP の GitHub リポジトリ](https://github.com/tidbcloud/byoc-account-setup/tree/main) からスクリプトをダウンロードします。

2. ターミナルで次のコマンドを実行します。プレースホルダーは実際の値に置き換えてください。

    ```bash
    sh tidbcloud-byoc-setup.sh \
        --control-plane-id <ControlPlaneAccountId> \
        --clinic-id <ClinicAccountId> \
        --tidb-hz-id <TidbHostedZoneId> \
        --pca-arn <TidbPCAArn>
    ```

3. 実行状況を監視します。スクリプトを実行すると、AWS CloudFormation が開始され、リソースのプロビジョニングと更新が行われます。ターミナルには、`waiting for changeset to be created` や `successfully created/updated stack` などのステータスメッセージを含むログストリームが表示されます。

<!--To confirm: whether to add image-->

## 検証 {#verification}

実行後、スクリプトは作成された IAM ロールの ARN を出力します。

**必要な対応:** **実行結果/ログ** を TiDB Cloud の担当者に共有してください。

## 次のステップ {#what-s-next}

TiDB Cloud が IAM ロールを確認したら、[TiDB Cloud BYOC の自動リージョンデプロイ](/tidb-cloud/byoc/byoc-automated-deployment.md) に進んでください。TiDB Cloud が自動リージョンデプロイを開始します。