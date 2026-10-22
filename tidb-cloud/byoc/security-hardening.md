---
title: TiDB Cloud BYOC のセキュリティ強化
summary: このドキュメントでは、TiDB Cloud BYOC デプロイのセキュリティ強化手順について説明します。
---

# TiDB Cloud BYOC のセキュリティ強化

BYOC 環境の提供が完了し、本番環境で稼働している場合は、クラウドセキュリティのベストプラクティスで推奨される **最小権限の原則** に従うために、インストール段階でのみ使用したブートストラップ権限を削除することを選択できます。

これらの権限には、次の 2 つの IAM ロールが関係します。

* **auto-deploy-cli**: VPC や EKS クラスターなどのインフラストラクチャを作成するために使用される、最も高い権限を持つロールです。
* **auto-deploy-sync-image**: TiDB Cloud からイメージを取得して同期するために使用されるロールです。

> **Important:**
>
> **複数リージョンおよび複数リソースプールの場合:** `auto-deploy-cli` と `auto-deploy-sync-image` の IAM ロールは、グローバル（アカウントレベル）のリソースです。複数の AWS リージョンで TiDB Cloud BYOC をデプロイする予定がある場合、またはアカウント内で物理的に分離された複数のリソースプールをプロビジョニングする予定がある場合は、すべての環境のデプロイが完了するまで、このセキュリティ強化手順を延期することを推奨します。

**自動アップグレード** に関する要件に応じて、次のいずれかのオプションを選択できます。

## オプション 1: 自動アップグレードを維持し、インフラデプロイ権限を削除する {#option-1-retain-automatic-upgrades-remove-infrastructure-deployment-permissions}

**目的:** `auto-deploy-cli` ロールを削除し、`auto-deploy-sync-image` ロールは保持します。

**影響:**

* セキュリティ: コントロールプレーンは、アカウント内に新しいインフラリソース（例: VPC）を作成できなくなります。
* 保守性: イメージ同期の権限は保持されるため、クラスターは引き続き自動アップグレードを実行できます。

**手順:**

1. デプロイ時に使用した CloudFormation テンプレート `tidbcloud-byoc-setup-deploy.yaml` を見つけます。

2. ファイルを編集します。`TiDBCloudAutoDeployRole` フィールドを見つけ、その行と配下のすべての内容を削除します。`TiDBCloudAutoDeploySyncImageRole` セクションはそのまま残してください。

3. ターミナルで更新したスクリプトを適用します。

    ```shell
    bash tidbcloud-byoc-update.sh --stack deploy
    ```

## オプション 2: すべてのブートストラップ権限を削除する（自動アップグレードは無効） {#option-2-remove-all-bootstrap-permissions-automatic-upgrades-disabled}

**目的:** `auto-deploy-cli` と `auto-deploy-sync-image` の両方のロールを削除します。

**影響:**

* 最大限のセキュリティ: ブートストラップフェーズで使用されたすべての IAM ロールが削除されます。
* 機能上の制限: 自動アップグレードは利用できなくなります。今後データベースコンポーネントをアップグレードするには、sync-image ロールを再デプロイする必要があります。

**手順:**

AWS CLI を使用して、対応する CloudFormation スタックを削除します。

```shell
aws cloudformation delete-stack --stack-name tidbcloud-byoc-setup-deploy
```

> **Important:**
>
> どのオプションを選択した場合でも、`dataplane` **または** `o11y` **サフィックスを持つスタックは削除しないでください**（たとえば `tidbcloud-byoc-setup-dataplane`）。これらは、クラスターの運用、監視、バックアップに必要なランタイム権限を提供するためです。