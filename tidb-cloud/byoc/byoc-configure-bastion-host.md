---
title: "{{{ .byoc }}} の踏み台ホストを設定する"
summary: "{{{ .byoc }}} 環境で、安全なメンテナンスアクセスのために踏み台ホストをデプロイおよび管理する方法を説明します。"
---

# {{{ .byoc }}} の踏み台ホストを設定する

このドキュメントでは、{{{ .byoc }}} 環境向けに踏み台ホストをデプロイおよび管理する方法について説明します。踏み台ホストは、お客様の AWS アカウント内の TiDB および可観測性 EKS クラスターと安全にやり取りするための、制御されたアクセス経路を提供します。

TiDB Cloud は、承認されたトラブルシューティングおよびメンテナンスのシナリオでのみ踏み台ホストを使用します。踏み台ホストは、安全な Tailscale トンネルを介して TiDB Cloud に接続します。必要に応じて、このアクセスを取り消したり復元したりできます。

> **Note:**
>
> 踏み台ホストの設定は任意です。メンテナンスやトラブルシューティングのために、独自の安全なアクセス方法を提供することもできます。

## 始める前に {#before-you-begin}

踏み台ホストをデプロイする前に、次の要件を満たしていることを確認してください。

- Terraform がローカルにインストールされていること。
- AWS CLI が、お使いの AWS アカウントの認証情報で設定されていること。
- EC2、IAM、EKS リソースを含む、必要な AWS リソースを管理する権限を持っていること。
- {{{ .byoc }}} 環境がデプロイ済みであること。
- TiDB Cloud Support から次の情報を取得していること。
    - TiDB Cloud テナント ID。
    - {{{ .byoc }}} 環境がデプロイされている AWS リージョン ID。
    - TiDB および可観測性の EKS クラスター名。
    - デプロイする踏み台ホスト用の Tailscale 認証キー。
    - Single-AZ デプロイの場合、TiDB および可観測性 EKS クラスターのサブネット ID。

## 踏み台ホストをデプロイする {#deploy-bastion-hosts}

踏み台ホストをデプロイするには、次の手順を実行します。

1. [PingCAP の GitHub リポジトリ](https://github.com/tidbcloud/byoc-account-setup/tree/main/bastion) から踏み台ホストデプロイスクリプトをダウンロードします。

2. Terraform バックエンドを設定します。

    デフォルトのバックエンドは Amazon S3 です。`terraform.tf` で、S3 バックエンドの設定をお使いのバケット、ステートファイルのパス、リージョンで更新します。

    ```hcl
    terraform {
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 5.0"
        }
      }

      backend "s3" {
        bucket = "YOUR_S3_BUCKET"
        key    = "TF_STATE_FILE_PATH"
        region = "us-west-2"
      }
    }
    ```

    別の [Terraform バックエンド](https://developer.hashicorp.com/terraform/language/backend) を使用する場合は、それに応じて `terraform.tf` を更新してください。

3. Terraform を初期化します。

    ```shell
    terraform init
    ```

4. Terraform 変数ファイルを準備します。

    ```shell
    cp examples/terraform.tfvars.example ./terraform.tfvars
    vim ./terraform.tfvars
    ```

5. `terraform.tfvars` で、必要なフィールドを設定します。

    - `aws_region`: {{{ .byoc }}} 環境がデプロイされている AWS リージョン。たとえば `us-west-2`。
    - `tidbcloud_tenant_id`: TiDB Cloud テナント ID。
    - `bastions`: 踏み台ホストの設定。`tidb` と `o11y` の踏み台ホストを設定できます。
    - `<bastion_type>.eks_cluster_name`: 踏み台ホストの種類に対応する EKS クラスター名。たとえば `tidb.eks_cluster_name` または `o11y.eks_cluster_name`。
    - `<bastion_type>.auth_key`: TiDB Cloud から提供される Tailscale 認証キー。
    - `<bastion_type>.subnet_id`: Single-AZ デプロイでのみ使用する、対応する EKS クラスターのサブネット ID。

    次の例では、TiDB と可観測性の両方に対して踏み台ホストを設定しています。

    ```hcl
    aws_region = "us-west-2"

    tidbcloud_tenant_id = "your_tidbcloud_tenant_id"

    bastions = {
      tidb = {
        eks_cluster_name = "your-tidb-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
      o11y = {
        eks_cluster_name = "your-o11y-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
    }
    ```

    TiDB 用の踏み台ホストのみが必要な場合は、`tidb` エントリだけを設定します。

    ```hcl
    aws_region = "us-west-2"

    tidbcloud_tenant_id = "your_tidbcloud_tenant_id"

    bastions = {
      tidb = {
        eks_cluster_name = "your-tidb-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
    }
    ```

6. Terraform 設定を適用します。

    ```shell
    terraform apply
    ```

    Terraform plan を注意深く確認してください。確認してデプロイを続行するには、`yes` と入力します。

## デプロイを検証する {#validate-the-deployment}

デプロイが完了したら、Terraform の出力を取得します。

```shell
terraform output
```

出力は次のようになります。

```hcl
bastion_attributes = tomap({
  "bastion_name" = {
    "o11y" = "<bastion_o11y_name>"
    "tidb" = "<bastion_tidb_name>"
  }
  "instance_id" = {
    "o11y" = "<instance_o11y_id>"
    "tidb" = "<instance_tidb_id>"
  }
})
```

この出力を TiDB Cloud Support に提供してください。TiDB Cloud Support はこの出力を使用して接続性を確認し、必要なネットワーク設定を完了します。

## 踏み台ホストを管理する {#manage-bastion-hosts}

踏み台ホストのデプロイ後は、AWS Systems Manager (SSM) を使用して管理できます。

```shell
aws ssm start-session --region <region> --target <instance_id> --reason <reason>
```

TiDB Cloud から踏み台ホストへのアクセスを一時的に取り消すには、踏み台ホスト上で次のコマンドを実行します。

```shell
tailscale down
```

TiDB Cloud から踏み台ホストへのアクセスを復元するには、踏み台ホスト上で次のコマンドを実行します。

```shell
tailscale up
```

## 認証キーを管理する {#manage-authentication-keys}

TiDB Cloud が提供する Tailscale 認証キーは、1 回限りの一時的なものです。通常は 3 日後に期限切れになります。

キーの有効期限が切れても、すでにデプロイされ、有効なキーで設定済みの踏み台ホストには影響しません。ただし、新しい踏み台ホストを作成する場合や既存の踏み台ホストを再作成する場合など、キーの期限切れ後に `terraform apply` を再実行する必要がある場合は、TiDB Cloud Support に新しい認証キーをリクエストし、設定を適用する前に `terraform.tfvars` 内の `auth_key` の値を更新してください。

## 監査ログ {#audit-logs}

セキュリティとコンプライアンスのため、各踏み台ホストは [auditd サービス](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/security_guide/chap-system_auditing) を通じて、実行されたコマンドの詳細な監査証跡を収集するよう設定されています。

監査ログはローカルの `/var/log/audit/audit.log` に保存され、次の AWS CloudWatch Log Group に自動的に転送されます。

```text
/aws/eks/${eks_cluster_name}/byoc-bastion/audit
```

デフォルトでは、ログは CloudWatch に 90 日間保持されます。

CloudWatch への監査ログ転送を無効にするには、`cloudwatch_audit_enable` を `false` に設定します。

## 踏み台ホストをクリーンアップする {#clean-up-bastion-hosts}

Terraform 設定によって作成された踏み台ホストと関連リソースを削除するには、次のコマンドを実行します。

```shell
terraform destroy
```
