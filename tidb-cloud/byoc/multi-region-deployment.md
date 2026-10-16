---
title: TiDB Cloud BYOC マルチリージョンデプロイ
summary: このドキュメントでは、複数の AWS リージョンにまたがって TiDB Cloud BYOC をデプロイする手順について説明します。
---

# TiDB Cloud BYOC マルチリージョンデプロイ

TiDB Cloud BYOC は、**複数の AWS リージョン**にまたがるデプロイをサポートしています。同じ IAM ロールをリージョン間で再利用できるため、追加のリージョンを有効化する際に BYOC IAM ロールを再作成する必要はありません。

マルチリージョンデプロイには、次の 2 つのシナリオがあります。

| シナリオ | 説明 | スクリプト |
| ----- | ----- | ----- |
| 新規マルチリージョンデプロイ | まだどの BYOC リージョンもデプロイされておらず、最初から複数リージョンでの運用を計画している場合。 | `tidbcloud-byoc-setup.sh` |
| 既存デプロイへのリージョン追加 | すでに 1 つ以上の BYOC リージョンがデプロイされており、後から追加のリージョンを有効化する場合。 | `tidbcloud-byoc-update.sh` |

* 複数リージョンを前提とした新規デプロイについては、[シナリオ 1: 新規マルチリージョンデプロイ](#scenario-1-new-multi-region-deployment) を参照してください。
* 既存の BYOC デプロイにリージョンを追加する場合は、[シナリオ 2: 既存の BYOC デプロイへのリージョン追加](#scenario-2-add-a-region-to-an-existing-byoc-deployment) を参照してください。

## リソース計画: 共有リソースと専用リソース {#resource-planning-shared-and-dedicated-resources}

複数リージョンを設定する前に、次の基盤リソースをリージョン間で共有するか、各リージョン専用にするかを決定してください。

* AWS private certificate authority (PCA)
* TiDB 用の Route 53 hosted zone

### 共有リソース {#shared-resources}

同じ PCA と TiDB hosted zone を、すべての有効化されたリージョンで共有できます。

この構成では、標準パラメータを使用してプライマリ PCA と TiDB hosted zone を指定し、対応する `--additional-*` パラメータは省略します。

### 専用リソース {#dedicated-resources}

追加リージョンごとに、個別の PCA と TiDB hosted zone を用意できます。

プライマリリージョンのリソースは、標準パラメータで指定します。

* `--pca-arn`
* `--tidb-hz-id`

追加リージョンのリソースは、次のパラメータで指定します。

* `--additional-pca-arns`
* `--additional-tidb-hz-ids`

追加リージョンが 2 つ以上ある場合は、同じリージョン順でカンマ区切りのリストとして値を指定してください。

### 混在リソース {#mixed-resources}

共有リソースと専用リソースは組み合わせて使用できます。

たとえば、すべてのリージョンで同じ PCA を共有しつつ、TiDB hosted zone はリージョンごとに分けることができます。

各追加リソースパラメータは独立しています。対応するリソースをプライマリリージョンと共有する場合は、そのパラメータを省略してください。

## シナリオ 1: 新規マルチリージョンデプロイ {#scenario-1-new-multi-region-deployment}

まだどの BYOC リージョンもデプロイしておらず、最初から複数リージョンをデプロイする予定がある場合は、このセクションを使用してください。

`tidbcloud-byoc-setup.sh` を実行して、BYOC 環境を初期化し、必要なリソースを設定します。

### すべてのリージョンで同じリソースを共有する {#all-regions-share-the-same-resources}

すべてのリージョンで同じ PCA と TiDB hosted zone を共有する場合は、標準のセットアップコマンドを実行します。

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <SharedTidbHostedZoneId> \
  --pca-arn <SharedPCAArn>
```

`--additional-*` パラメータは不要です。

### 追加リージョンで専用リソースを使用する {#additional-regions-use-dedicated-resources}

プライマリリージョンのリソースは標準パラメータで指定し、追加リージョンのリソースは `--additional-*` パラメータで指定します。

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <Region1TidbHostedZoneId> \
  --pca-arn <Region1PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId> \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn>
```

すべてのカンマ区切りリスト内の値は、同じリージョン順に従う必要があります。たとえば、次のとおりです。

* 1 番目の値は Region 2 を表します。
* 2 番目の値は Region 3 を表します。

### 共有リソースと専用リソースを混在させる {#mixed-shared-and-dedicated-resources}

次の例では、1 つの PCA をすべてのリージョンで共有しつつ、TiDB hosted zone は専用にしています。

```shell
bash tidbcloud-byoc-setup.sh \
  --control-plane-id <ControlPlaneAccountId> \
  --clinic-id <ClinicAccountId> \
  --tidb-hz-id <Region1TidbHostedZoneId> \
  --pca-arn <SharedPCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId>
```

PCA は共有されるため、`--additional-pca-arns` は省略します。

## シナリオ 2: 既存の BYOC デプロイへのリージョン追加 {#scenario-2-add-a-region-to-an-existing-byoc-deployment}

すでに 1 つ以上の BYOC リージョンがデプロイされており、1 つ以上の新しいリージョンを追加したい場合は、このセクションを使用してください。

`tidbcloud-byoc-setup.sh` を再度実行しないでください。

既存の CloudFormation スタックを更新するには、`tidbcloud-byoc-update.sh` を使用します。既存の IAM ロールと、以前に設定したスタックパラメータが再利用されます。

### リージョンを追加する前に {#before-adding-the-region}

更新スクリプトを実行する前に、次の点を確認してください。

1. 追加する AWS リージョンを確認します。
2. 新しいリージョンの Availability Zone を選択します。リージョンリソースプールには、少なくとも 3 つの利用可能な Availability Zone が必要です。新しいリージョンでリージョンリソースプールを作成する予定がある場合は、そのリージョンに対して少なくとも 3 つの利用可能な Availability Zone を選択してください。
3. 各新規リージョンの O11Y CIDR と、作成予定のリソースプール用の resource pool CIDR を計画します。異なるリージョンで同じ O11Y CIDR を使用することは可能です。ただし、metric integration を使用して Grafana を複数リージョンに接続する場合は、それらのリージョンでは重複しない O11Y CIDR を使用してください。
4. 各新規リージョンについて、次のいずれにするかを確認します。
    * 既存の PCA と TiDB hosted zone を共有する
    * 専用の PCA と TiDB hosted zone を使用する
5. 各新規リージョンで AWS service quota を確認し、必要に応じて引き上げます。
6. 新規リージョンに関する情報を TiDB Cloud の担当者に共有します。

各新規リージョンについて、O11Y CIDR と resource pool CIDR は次のいずれとも重複してはいけません。

* 同じリージョン内の O11Y CIDR
* 同じリージョン内の既存の resource pool CIDR
* VPC Peering または VPN を通じて接続される既存の application VPC、オンプレミスネットワーク、または VPN ネットワーク
* リソースプールがクロスリージョンレプリケーションに参加する場合、他リージョンの resource pool CIDR

異なるリージョンの resource pool CIDR は重複していてもかまいません。ただし、クロスリージョン接続またはレプリケーションが必要なリソースプールには、重複しない CIDR を使用してください。

### 既存の PCA と TiDB hosted zone を共有する {#share-an-existing-pca-and-tidb-hosted-zone}

新しいすべてのリージョンで、既存デプロイですでに使用している PCA と TiDB hosted zone を共有する場合は、このオプションを使用します。

追加のリソースパラメータは不要です。

```shell
bash tidbcloud-byoc-update.sh \
  --stack all
```

既存のリソースは、すべての有効化されたリージョンで引き続き使用されます。

新しいマルチリージョン用リソース値が不要な場合、単純な \--stack all 更新は安全です。

### 新しいリージョンで専用リソースを使用する {#use-dedicated-resources-for-the-new-regions}

新しいリージョンで専用の PCA または TiDB hosted zone が必要な場合は、このオプションを使用します。

新しいリージョン用のリソースを、対応する `--additional-*` パラメータで指定します。

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId>

```

各パラメータは独立しています。対応するリソースを既存リージョンと共有する場合は、そのパラメータを省略してください。

すべてのカンマ区切りリスト内の値は、同じリージョン順に従う必要があります。たとえば、次のとおりです。

* 各リストの 1 番目の値は Region 2 を表します。
* 各リストの 2 番目の値は Region 3 を表します。

### 共有リソースと専用リソースを組み合わせて使用する {#use-a-mix-of-shared-and-dedicated-resources}

新しいリージョンでは、一部の既存リソースを共有しつつ、他のリソースには専用リソースを使用できます。

たとえば、既存の PCA を共有しながら、新しいリージョンには専用の TiDB hosted zone を使用する場合は、次のようにします。

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId>
```

既存の PCA は共有されるため、`--additional-pca-arns` は省略します。

リソース戦略は新しいリージョンごとに異なっていてもかまいません。ただし、各 `--additional-*` パラメータに指定する値は、同じリージョン順に対応している必要があります。

### 複数のリージョンがすでに存在する場合にリージョンを追加する {#add-regions-when-multiple-regions-already-exist}

既存のデプロイにすでに複数のリージョンが含まれている場合は、同じ更新手順を使用してさらにリージョンを追加します。

マルチリージョンのリソース値は CloudFormation スタックに保存され、今後の更新時に再利用されます。更新コマンドを実行する際は、追加するリージョンで必要となる新規または変更済みのリソース値を指定してください。

たとえば、リージョン 1 がプライマリリージョンで、リージョン 2 はすでに設定済み、さらに専用リソースを使用してリージョン 3 を追加する場合は、次のようになります。

```shell
bash tidbcloud-byoc-update.sh \
  --stack all \
  --additional-pca-arns <Region2PCAArn>,<Region3PCAArn> \
  --additional-tidb-hz-ids <Region2TidbHostedZoneId>,<Region3TidbHostedZoneId>
```

以前に設定したリソース値と新たに追加したリソース値が、正しいリージョン順のままになっていることを確認してください。

### リージョンのデプロイを完了する {#complete-the-regional-deployment}

CloudFormation スタックを更新すると、新しいリージョンに必要なアカウントレベルの権限とリソース設定が準備されます。ただし、これだけではリージョンのインフラストラクチャのデプロイは完了しません。

更新が成功したら、次の手順を実行します。

1. スクリプトの実行結果を TiDB Cloud の担当者に共有します。
2. TiDB Cloud が更新された IAM とリージョンのリソース設定を検証します。
3. TiDB Cloud が新しいリージョン向けの自動インフラストラクチャプロビジョニングを開始します。
4. プロビジョニングの完了後、各新規リージョンについてセクション 5 で説明されている共同検証を実施します。