---
title: Use the `tidbcloud_serverless_cluster` Resource
summary: tidbcloud_serverless_cluster` リソースを使用してTiDB Cloud Essential クラスターを作成および変更する方法を学習します。
---

# <code>tidbcloud_serverless_cluster</code>リソースを使用する {#use-the-code-tidbcloud-serverless-cluster-code-resource}

このドキュメントでは、 `tidbcloud_serverless_cluster`リソースを使用して[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターを管理する方法について説明します。

また、 `tidbcloud_projects`データ ソースを使用して必要な情報を取得する方法も学習します。

`tidbcloud_serverless_cluster`リソースの機能は次のとおりです。

-   TiDB Cloud Essential クラスターを作成します。
-   TiDB Cloud Essential クラスターを変更します。
-   TiDB Cloud Essential クラスターをインポートします。
-   TiDB Cloud Essential クラスターを削除します。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.2以降。

## <code>tidbcloud_projects</code>データソースを使用してプロジェクト ID を取得する {#get-project-ids-using-the-code-tidbcloud-projects-code-data-source}

各TiDBクラスタはプロジェクトに属します。TiDB TiDB Cloud Essentialクラスタを作成する前に、クラスタを作成するプロジェクトのIDを取得する必要があります。1 `project_id`指定されていない場合は、デフォルトのプロジェクトが使用されます。

利用可能なすべてのプロジェクトに関する情報を取得するには、次のように`tidbcloud_projects`データ ソースを使用します。

1.  [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md)で作成した`main.tf`ファイルに、次のように`data`と`output`ブロックを追加します。

        terraform {
          required_providers {
            tidbcloud = {
              source = "tidbcloud/tidbcloud"
            }
          }
        }

        provider "tidbcloud" {
          public_key = "your_public_key"
          private_key = "your_private_key"
        }

        data "tidbcloud_projects" "example_project" {
          page      = 1
          page_size = 10
        }

        output "projects" {
          value = data.tidbcloud_projects.example_project.items
        }

    -   `data`ブロックを使用して、データ ソース タイプやデータ ソース名など、 TiDB Cloudのデータ ソースを定義します。

        -   プロジェクト データ ソースを使用するには、データ ソース タイプを`tidbcloud_projects`に設定します。
        -   データソース名は必要に応じて定義できます。例： `"example_project"` 。
        -   `tidbcloud_projects`データ ソースの場合、 `page`および`page_size`属性を使用して、チェックするプロジェクトの最大数を制限できます。

    -   `output`ブロックを使用して、出力に表示されるデータ ソース情報を定義し、他の Terraform 構成が使用できるように情報を公開します。

        `output`ブロックはプログラミング言語の戻り値と同様の動作をします。詳細は[Terraformドキュメント](https://www.terraform.io/language/values/outputs)参照してください。

    リソースとデータ ソースに使用可能なすべての構成を取得するには、 [Terraform プロバイダーの構成ドキュメント](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)参照してください。

2.  設定を適用するには、コマンド`terraform apply`を実行してください。続行するには、確認プロンプトで`yes`と入力してください。

    プロンプトをスキップするには、 `terraform apply --auto-approve`使用します。

    ```shell
    $ terraform apply --auto-approve

    Changes to Outputs:
      + projects = [
          + {
              + cluster_count    = 0
              + create_timestamp = "1649154426"
              + id               = "1372813089191000000"
              + name             = "test1"
              + org_id           = "1372813089189000000"
              + user_count       = 1
            },
          + {
              + cluster_count    = 1
              + create_timestamp = "1640602740"
              + id               = "1372813089189000000"
              + name             = "default project"
              + org_id           = "1372813089189000000"
              + user_count       = 1
            },
        ]

    You can apply this plan to save these new output values to the Terraform state, without changing any real infrastructure.

    Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

    Outputs:

    projects = tolist([
      {
        "cluster_count" = 0
        "create_timestamp" = "1649154426"
        "id" = "1372813089100000000"
        "name" = "test1"
        "org_id" = "1372813089100000000"
        "user_count" = 1
      },
      {
        "cluster_count" = 1
        "create_timestamp" = "1640602740"
        "id" = "1372813089100000001"
        "name" = "default project"
        "org_id" = "1372813089100000000"
        "user_count" = 1
      },
    ])
    ```

これで、出力から利用可能なすべてのプロジェクトを取得できます。必要なプロジェクトIDを1つコピーしてください。

## TiDB Cloud Essential クラスターを作成する {#create-a-tidb-cloud-essential-cluster}

`tidbcloud_serverless_cluster`リソースを使用して、 TiDB Cloud Essential クラスターを作成できます。

1.  クラスターのディレクトリを作成してそこに入ります。

2.  `cluster.tf`ファイルを作成します。

    以下は`cluster.tf`ファイルの例です。

        terraform {
          required_providers {
            tidbcloud = {
              source = "tidbcloud/tidbcloud"
            }
          }
        }

        provider "tidbcloud" {
          public_key = "your_public_key"
          private_key = "your_private_key"
        }

        resource "tidbcloud_serverless_cluster" "example" {
          project_id = "1372813089454000000"
          display_name = "test-tf"
          auto_scaling = {
            min_rcu = 3000
            max_rcu = 4000
          }
          region = {
            name = "regions/aws-us-east-1"
          }
        }

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細など、 TiDB Cloudのリソースを定義します。

    -   `tidbcloud_serverless_cluster`リソースを使用するには、リソース タイプを`tidbcloud_serverless_cluster`に設定します。
    -   リソース名は必要に応じて定義できます。例： `example` 。
    -   リソースの詳細は、プロジェクトIDと[`tidbcloud_serverless_cluster`仕様](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_cluster)に応じて設定できます。TiDB TiDB Cloud Essentialクラスターを作成するには、リソース詳細で`auto_scaling`属性を指定する必要があります。

3.  `terraform apply`コマンドを実行します。リソースを適用する場合は`terraform apply --auto-approve`の使用は推奨されません。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

        # tidbcloud_serverless_cluster.example will be created
        + resource "tidbcloud_serverless_cluster" "example" {
            + annotations             = (known after apply)
            + automated_backup_policy = (known after apply)
            + cluster_id              = (known after apply)
            + create_time             = (known after apply)
            + created_by              = (known after apply)
            + display_name            = "test-tf"
            + encryption_config       = (known after apply)
            + endpoints               = (known after apply)
            + labels                  = (known after apply)
            + project_id              = "1372813089454000000"
            + region                  = {
                + cloud_provider = (known after apply)
                + display_name   = (known after apply)
                + name           = "regions/aws-us-east-1"
                + region_id      = (known after apply)
            }
            + auto_scaling            = {
                + max_rcu = 4000
                + min_rcu = 3000
            }
            + state                   = (known after apply)
            + update_time             = (known after apply)
            + user_prefix             = (known after apply)
            + version                 = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value:
    ```

    上記の結果では、Terraform によって実行プランが生成され、Terraform が実行するアクションが記述されています。

    -   構成と状態の違いを確認できます。
    -   `apply`の結果も確認できます。新しいリソースが追加されますが、リソースは変更または破棄されません。
    -   `known after apply` `apply`後の対応する値が取得されることを示します。

4.  計画の内容がすべて問題ない場合は、「 `yes`と入力して続行します。

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_cluster.example: Creating...
    tidbcloud_serverless_cluster.example: Still creating... [10s elapsed]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5.  リソースの状態を確認するには、コマンド`terraform show`または`terraform state show tidbcloud_serverless_cluster.${resource-name}`使用します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

    ```shell
    $ terraform state show tidbcloud_serverless_cluster.example

    # tidbcloud_serverless_cluster.example:
    resource "tidbcloud_serverless_cluster" "example" {
        annotations             = {
            "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
            "tidb.cloud/has-set-password"   = "false"
        }
        automated_backup_policy = {
            retention_days = 14
            start_time     = "07:00"
        }
        cluster_id              = "10145794214536000000"
        create_time             = "2025-06-16T07:04:41Z"
        created_by              = "apikey-S2000000"
        display_name            = "test-tf"
        encryption_config       = {
            enhanced_encryption_enabled = false
        }
        endpoints               = {
            private = {
                aws  = {
                    availability_zone = [
                        "use1-az6",
                    ]
                    service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000"
                }
                host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com"
                port = 4000
            }
            public  = {
                disabled = false
                host     = "gateway01.us-east-1.prod.aws.tidbcloud.com"
                port     = 4000
            }
        }
        labels                  = {
            "tidb.cloud/organization" = "1372813089187000000"
            "tidb.cloud/project"      = "1372813089454000000"
        }
        project_id              = "1372813089454000000"
        region                  = {
            cloud_provider = "aws"
            display_name   = "N. Virginia (us-east-1)"
            name           = "regions/aws-us-east-1"
            region_id      = "us-east-1"
        }
        auto_scaling = {
            min_rcu = 3000
            max_rcu = 4000
        }
        state                   = "ACTIVE"
        update_time             = "2025-06-16T07:04:48Z"
        user_prefix             = "KhSDGqQ3P000000"
        version                 = "v7.5.2"
    }
    ```

## TiDB Cloud Essential クラスターを変更する {#modify-a-tidb-cloud-essential-cluster}

TiDB Cloud Essential クラスタでは、Terraform を使用してリソースを管理できます。変更可能な引数は次のとおりです。

-   `display_name` : クラスターの表示名。
-   `auto_scaling` : クラスターの自動スケーリング構成。
-   `endpoints.public.disabled` : パブリックエンドポイントを無効にするかどうか。
-   `automated_backup_policy.start_time` : 自動バックアップが開始される時点の UTC 時刻 ( `HH:mm`形式)。

TiDB Cloud Essentialクラスターを変更するには、 `tidbcloud_serverless_cluster`のリソースの設定を変更し、 `terraform apply`コマンドを使用して変更を適用します。例えば、 `display_name`と`auto_scaling`リソースを次のように変更できます。

    resource "tidbcloud_serverless_cluster" "example" {
      project_id = "1372813089454000000"
      display_name = "test-tf-modified"
      auto_scaling = {
        min_rcu = 4000
        max_rcu = 5000
      }
      region = {
        name = "regions/aws-us-east-1"
      }
    }

次に、 `terraform apply`コマンドを実行して変更を適用します。

```shell
$ terraform apply

tidbcloud_serverless_cluster.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # tidbcloud_serverless_cluster.example will be updated in-place
  ~ resource "tidbcloud_serverless_cluster" "example" {
      ~ annotations             = {
          - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
          - "tidb.cloud/has-set-password"   = "false"
        } -> (known after apply)
      ~ display_name            = "test-tf" -> "test-tf-modified"
      ~ labels                  = {
          - "tidb.cloud/organization" = "1372813089187041280"
          - "tidb.cloud/project"      = "1372813089454543324"
        } -> (known after apply)
      ~ auto_scaling            = {
          ~ min_rcu = 3000 -> 4000
          ~ max_rcu = 4000 -> 5000
        }
      ~ state                   = "ACTIVE" -> (known after apply)
      ~ update_time             = "2025-06-16T07:04:57Z" -> (known after apply)
      ~ version                 = "v7.5.2" -> (known after apply)
        # (9 unchanged attributes hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_cluster.example: Modifying...
tidbcloud_serverless_cluster.example: Modifications complete after 8s

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

次に、コマンド`terraform show`または`terraform state show tidbcloud_serverless_cluster.${resource-name}`使用してリソースの状態を確認します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

```shell
$ terraform state show tidbcloud_serverless_cluster.example
# tidbcloud_serverless_cluster.example:
resource "tidbcloud_serverless_cluster" "example" {
    annotations             = {
        "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
        "tidb.cloud/has-set-password"   = "false"
    }
    automated_backup_policy = {
        retention_days = 14
        start_time     = "07:00"
    }
    cluster_id              = "10145794214536000000"
    create_time             = "2025-06-16T07:04:41Z"
    created_by              = "apikey-S2000000"
    display_name            = "test-tf-modified"
    encryption_config       = {
        enhanced_encryption_enabled = false
    }
    endpoints               = {
        private = {
            aws  = {
                availability_zone = [
                    "use1-az6",
                ]
                service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000"
            }
            host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com"
            port = 4000
        }
        public  = {
            disabled = false
            host     = "gateway01.us-east-1.prod.aws.tidbcloud.com"
            port     = 4000
        }
    }
    labels                  = {
        "tidb.cloud/organization" = "1372813089187000000"
        "tidb.cloud/project"      = "1372813089454000000"
    }
    project_id              = "1372813089454000000"
    region                  = {
        cloud_provider = "aws"
        display_name   = "N. Virginia (us-east-1)"
        name           = "regions/aws-us-east-1"
        region_id      = "us-east-1"
    }
    auto_scaling = {
        min_rcu = 4000
        max_rcu = 5000
    }
    state                   = "ACTIVE"
    update_time             = "2025-06-16T07:04:57Z"
    user_prefix             = "KhSDGqQ3P000000"
    version                 = "v7.5.2"
}
```

## TiDB Cloud Essential クラスターをインポートする {#import-a-tidb-cloud-essential-cluster}

Terraform によって管理されていないTiDB Cloud Essential クラスターの場合は、インポートすることで Terraform の管理下に置くことができます。

1.  新しい`tidbcloud_serverless_cluster`リソースのインポート ブロックを追加します。

    次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}`クラスター ID に置き換えます。

        import {
          to = tidbcloud_serverless_cluster.example
          id = "${id}"
        }

2.  新しい構成ファイルを生成します。

    インポート ブロックに従って、新しい`tidbcloud_serverless_cluster`リソースの新しい構成ファイルを生成します。

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

3.  生成された構成を確認して適用します。

    生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

    次に、 `terraform apply`実行してインフラストラクチャをインポートします。適用後、出力例は次のようになります。

    ```shell
    tidbcloud_serverless_cluster.example: Importing... 
    tidbcloud_serverless_cluster.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

これで、インポートしたクラスターを Terraform で管理できるようになりました。

## TiDB Cloud Essential クラスターを削除する {#delete-a-tidb-cloud-essential-cluster}

TiDB Cloud Essential クラスターを削除するには、 `tidbcloud_serverless_cluster`リソースの構成を削除し、 `terraform apply`コマンドを使用してリソースを破棄します。

```shell
$ terraform apply
tidbcloud_serverless_cluster.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # tidbcloud_serverless_cluster.example will be destroyed
  # (because tidbcloud_serverless_cluster.example is not in configuration)
  - resource "tidbcloud_serverless_cluster" "example" {
      - annotations             = {
          - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,DELEGATE_USER"
          - "tidb.cloud/has-set-password"   = "false"
        } -> null
      - automated_backup_policy = {
          - retention_days = 14 -> null
          - start_time     = "07:00" -> null
        } -> null
      - cluster_id              = "10145794214536000000" -> null
      - create_time             = "2025-06-16T07:04:41Z" -> null
      - created_by              = "apikey-S2000000" -> null
      - display_name            = "test-tf-modified" -> null
      - encryption_config       = {
          - enhanced_encryption_enabled = false -> null
        } -> null
      - endpoints               = {
          - private = {
              - aws  = {
                  - availability_zone = [
                      - "use1-az6",
                    ] -> null
                  - service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000" -> null
                } -> null
              - host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com" -> null
              - port = 4000 -> null
            } -> null
          - public  = {
              - disabled = false -> null
              - host     = "gateway01.us-east-1.prod.aws.tidbcloud.com" -> null
              - port     = 4000 -> null
            } -> null
        } -> null
      - labels                  = {
          - "tidb.cloud/organization" = "1372813089187000000"
          - "tidb.cloud/project"      = "1372813089454000000"
        } -> null
      - project_id              = "1372813089454000000" -> null
      - region                  = {
          - cloud_provider = "aws" -> null
          - display_name   = "N. Virginia (us-east-1)" -> null
          - name           = "regions/aws-us-east-1" -> null
          - region_id      = "us-east-1" -> null
        } -> null
      - auto_scaling            = {
          - min_rcu = 4000 -> null
          - max_rcu = 5000 -> null
        } -> null
      - state                   = "ACTIVE" -> null
      - update_time             = "2025-06-16T07:04:57Z" -> null
      - user_prefix             = "KhSDGqQ3P000000" -> null
      - version                 = "v7.5.2" -> null
    }

Plan: 0 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_cluster.example: Destroying...
tidbcloud_serverless_cluster.example: Destruction complete after 1s

Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

ここで、 `terraform show`コマンドを実行すると、リソースが破棄されているため、管理対象リソースは表示されません。

    $ terraform show
