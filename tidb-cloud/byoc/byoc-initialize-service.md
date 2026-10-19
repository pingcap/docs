---
title: TiDB Cloud BYOC インスタンスを初めて作成する
summary: このドキュメントでは、TiDB Cloud BYOC インスタンスを作成し、安全なアクセスを設定する手順について説明します。
---

# TiDB Cloud BYOC インスタンスを初めて作成する

BYOC インフラストラクチャをデプロイした後、リソースプールを作成し、そのリソースプール内に最初の {{{ .byoc }}} インスタンスを作成して、安全な管理アクセスを設定します。

## BYOC インスタンスを作成する {#create-a-byoc-instance}

これで、TiDB Cloud コンソールから直接リソースプールと TiDB インスタンスをプロビジョニングできます。

1. [TiDB Cloud コンソール](https://tidbcloud.com/) にログインし、[リソースプールを作成する](/tidb-cloud/byoc/create-resource-pool-byoc.md) の手順に従って、対象のクラウドプロバイダーとリージョンにリソースプールを作成します。 

    >**Note:**
    >
    > リソースプールを作成する際は、ワークロード要件に応じて **Zonal** または **Regional** の高可用性を選択してください。リソースプール内で作成または復元された {{{ .byoc }}} インスタンスは、そのプールの高可用性モードを継承します。

2. リソースプールが **Active** になったら、[{{{ .byoc }}} インスタンスを作成する](/tidb-cloud/byoc/create-tidb-instance-byoc.md) の手順に従って、リソースプール内に新しいインスタンスを作成します。

    * 初期セットアップ時間: リージョン内で **最初のリソースプール** を作成する場合、システムが Kubernetes 環境を初期化するため、約 **1 時間** かかることがあります。
    * 追加インスタンス: アクティブなリソースプール内で追加のインスタンスを作成する場合、通常は数分で完了します。

3. 初期接続テストおよび機能テストに適した Request Unit (RU) 設定を決定するため、TiDB Cloud の担当者に相談してください。テスト要件に基づいて、適切な設定が推奨されます。

## Amazon S3 から新しい BYOC インスタンスにデータを復元する {#restore-data-from-amazon-s3-to-a-new-byoc-instance}

Amazon S3 にバックアップファイルを準備した後、アクティブなリソースプール内の新しい {{{ .byoc }}} インスタンスにデータを復元できます。

1. Amazon S3 アクセス (AK/SK) を設定します。

    TiDB Cloud が S3 バックアップを読み取れるようにするには、適切な S3 読み取り権限を持つ AWS Access Key ID と Secret Access Key (AK/SK) を生成して、外部ストレージアクセスを設定する必要があります。

    詳細な手順については、[AWS Access Key を使用して Amazon S3 アクセスを設定する](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access-using-an-aws-access-key) を参照してください。

2. 復元プロセスを実行します。

    アクセスキーの設定が完了したら、TiDB Cloud コンソールから復元ジョブを開始できます。

    復元時には、対象のクラウドプロバイダーとリージョン内で、十分な vCPU 容量を持つアクティブなリソースプールを選択してください。復元されたインスタンスは、選択したリソースプールの高可用性モードを継承します。

    選択したリソースプールが Pool vCPU Limit に達している場合は、制限を引き上げるか無効にするか、続行する前に別のリソースプールを選択してください。これは、新しい {{{ .byoc }}} インスタンスへの復元によって、プロビジョニング済み vCPU の合計が Pool vCPU Limit を超え、同じプール内のすべての {{{ .byoc }}} インスタンスのパフォーマンスに影響する可能性があるためです。

    手順ごとの復元方法については、[クラウドストレージからバックアップを復元する](/tidb-cloud/premium/backup-and-restore-premium.md#restore-backups-from-cloud-storage) を参照してください。

## 安全な管理アクセスを設定する {#configure-secure-administrative-access}

TiDB Cloud Support がトラブルシューティングやオブザーバビリティの支援を行えるようにするため、VPC 内に強化された踏み台ホストをデプロイして、安全なアクセスチャネルを設定できます。

> **Note:**
>
> - この手順は **任意** です。管理のために独自の安全なログイン方法を提供することもできます。
> - 踏み台ホストはトラブルシューティングのためにのみ使用され、永続的な接続を維持する必要はありません。このチャネルはいつでも終了できます。

デプロイおよび検証の手順については、[{{{ .byoc }}} の踏み台ホストを設定する](/tidb-cloud/byoc/byoc-configure-bastion-host.md) を参照してください。

## 次のステップ {#what-s-next}

最初のリソースプールと {{{ .byoc }}} インスタンスを作成し、安全な管理アクセスを設定したら、[TiDB Cloud BYOC 共同検証](/tidb-cloud/byoc/joint-validation.md) に進み、接続性、オブザーバビリティ、セキュリティ、アラートを検証してください。