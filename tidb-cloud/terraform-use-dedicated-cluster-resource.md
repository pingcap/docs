---
title: Use TiDB Cloud Dedicated Cluster Resource
summary: TiDB Cloud Dedicated クラスター リソースを使用して、 TiDB Cloud Dedicated クラスターを作成および変更する方法を学習します。
---

# TiDB Cloud専用クラスタリソースを使用する {#use-tidb-cloud-dedicated-cluster-resource}

このドキュメントでは、 `tidbcloud_dedicated_cluster`リソースを使用して[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを管理する方法について説明します。

さらに、 `tidbcloud_projects`データ ソースで必要な情報を取得し、 `tidbcloud_dedicated_node_group`リソースを使用してTiDB Cloud Dedicated クラスターの TiDB ノード グループを管理する方法も学習します。

`tidbcloud_dedicated_cluster`リソースの機能は次のとおりです。

-   TiDB Cloud Dedicated クラスターを作成します。
-   TiDB Cloud Dedicated クラスターを変更します。
-   TiDB Cloud Dedicated クラスターをインポートします。
-   TiDB Cloud Dedicated クラスターを削除します。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0以降。

## <code>tidbcloud_projects</code>データソースを使用してプロジェクト ID を取得する {#get-project-ids-using-the-code-tidbcloud-projects-code-data-source}

各TiDB Cloud Dedicatedクラスタはプロジェクトに属します。TiDB TiDB Cloud Dedicatedクラスタを作成する前に、クラスタを作成するプロジェクトのIDを取得する必要があります。1 `project_id`指定されていない場合は、デフォルトのプロジェクトが使用されます。

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

        `output`ブロックは、プログラミング言語の戻り値と同様に機能します。詳細については、 [Terraform ドキュメント](https://www.terraform.io/language/values/outputs)参照してください。

    リソースとデータ ソースの使用可能なすべての構成を取得するには、 [Terraform プロバイダーの構成ドキュメント](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)参照してください。

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

## TiDB Cloud専用クラスタを作成する {#create-a-tidb-cloud-dedicated-cluster}

> **注記：**
>
> -   始める前に、 [TiDB Cloudコンソール](https://tidbcloud.com)で CIDR が設定されていることを確認してください。詳細については、 [CIDRを設定する](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)参照してください。
> -   CIDR を管理するには[`dedicated_network_container`リソースを作成する](/tidb-cloud/terraform-use-dedicated-network-container-resource.md)も使用できます。

次のように、 `tidbcloud_dedicated_cluster`リソースを使用してTiDB Cloud Dedicated クラスターを作成できます。

1.  クラスターのディレクトリを作成してそこに入ります。

2.  `cluster.tf`ファイルを作成します。

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

        resource "tidbcloud_dedicated_cluster" "example_cluster" {
          display_name  = "your_display_name"
          region_id     = "your_region_id"
          port          = 4000
          root_password = "your_root_password"
          tidb_node_setting = {
           node_spec_key = "2C4G"
           node_count    = 1
          }
          tikv_node_setting = {
           node_spec_key   = "2C4G"
           node_count      = 3
           storage_size_gi = 60
           storage_type    = "Standard"
          }
        }

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細など、 TiDB Cloudのリソースを定義します。

    -   TiDB Cloud Dedicated クラスター リソースを使用するには、リソース タイプを`tidbcloud_dedicated_cluster`に設定します。
    -   リソース名は必要に応じて定義できます。例： `example_cluster` 。
    -   リソースの詳細については、プロジェクト ID とTiDB Cloud Dedicated クラスタの仕様情報に従って設定できます。
    -   TiDB Cloud Dedicated クラスタの仕様情報を取得するには、 [tidbcloud_dedicated_cluster (リソース)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_cluster)参照してください。

3.  `terraform apply`コマンドを実行します。リソースを適用する場合は`terraform apply --auto-approve`の使用は推奨されません。

    ```shell
    $ terraform apply

    Terraform will perform the following actions:

      # tidbcloud_dedicated_cluster.example_cluster will be created
      + resource "tidbcloud_dedicated_cluster" "example_cluster" {
          + annotations         = (known after apply)
          + cloud_provider      = (known after apply)
          + cluster_id          = (known after apply)
          + create_time         = (known after apply)
          + created_by          = (known after apply)
          + display_name        = "test-tf"
          + labels              = (known after apply)
          + pause_plan          = (known after apply)
          + port                = 4000
          + project_id          = (known after apply)
          + region_display_name = (known after apply)
          + region_id           = "aws-us-west-2"
          + state               = (known after apply)
          + tidb_node_setting   = {
              + endpoints               = (known after apply)
              + is_default_group        = (known after apply)
              + node_count              = 1
              + node_group_display_name = (known after apply)
              + node_group_id           = (known after apply)
              + node_spec_display_name  = (known after apply)
              + node_spec_key           = "2C4G"
              + public_endpoint_setting = (known after apply)
              + state                   = (known after apply)
            }
          + tikv_node_setting   = {
              + node_count             = 3
              + node_spec_display_name = (known after apply)
              + node_spec_key          = "2C4G"
              + storage_size_gi        = 60
              + storage_type           = "Standard"
            }
          + update_time         = (known after apply)
          + version             = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

    上記の結果では、Terraform によって実行されるアクションを記述した実行プランが生成されます。

    -   構成と状態の違いを確認できます。
    -   `apply`の結果も確認できます。新しいリソースが追加されますが、リソースは変更または破棄されません。
    -   `known after apply` 、 `apply`後の値が取得されることを示します。

4.  計画の内容がすべて問題ない場合は、「 `yes`と入力して続行します。

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Creating...
    tidbcloud_dedicated_cluster.example_cluster: Still creating... [10s elapsed]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

    通常、 TiDB Cloud Dedicated クラスターの作成には少なくとも 10 分かかります。

5.  リソースの状態を確認するには、コマンド`terraform show`または`terraform state show tidbcloud_dedicated_cluster.${resource-name}`使用します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

    ```shell
    $ terraform state show tidbcloud_dedicated_cluster.example_cluster

    # tidbcloud_dedicated_cluster.example_cluster:
    resource "tidbcloud_dedicated_cluster" "example_cluster" {
        annotations         = {
            "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
            "tidb.cloud/has-set-password"   = "false"
        }
        cloud_provider      = "aws"
        cluster_id          = "1379661944600000000"
        create_time         = "2025-06-06 06:25:29.878 +0000 UTC"
        created_by          = "apikey-XXXXXXXX"
        display_name        = "test-tf"
        labels              = {
            "tidb.cloud/organization" = "60000"
            "tidb.cloud/project"      = "3100000"
        }
        port                = 4000
        project_id          = "3100000"
        region_display_name = "Oregon (us-west-2)"
        region_id           = "aws-us-west-2"
        state               = "ACTIVE"
        tidb_node_setting   = {
            endpoints               = [
                {
                    connection_type = "PUBLIC"
                    host            = "tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "VPC_PEERING"
                    host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "PRIVATE_ENDPOINT"
                    host            = null
                    port            = 4000
                },
            ]
            is_default_group        = true
            node_count              = 1
            node_group_display_name = "DefaultGroup"
            node_group_id           = "1931960832833000000"
            node_spec_display_name  = "2 vCPU, 4 GiB beta"
            node_spec_key           = "2C4G"
            state                   = "ACTIVE"
        }
        tikv_node_setting   = {
            node_count             = 3
            node_spec_display_name = "2 vCPU, 4 GiB"
            node_spec_key          = "2C4G"
            storage_size_gi        = 60
            storage_type           = "Standard"
        }
        update_time         = "2025-06-06 06:31:42.974 +0000 UTC"
        version             = "v7.5.6"
    }
    ```

6.  リモートから状態を同期する場合は、 `terraform refresh`コマンドを実行して状態を更新し、 `terraform state show tidbcloud_dedicated_cluster.${resource-name}`コマンドを実行して状態を表示します。

    ```shell
    $ terraform refresh

    tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

    $ terraform state show tidbcloud_dedicated_cluster.example_cluster

    # tidbcloud_dedicated_cluster.example_cluster:
    resource "tidbcloud_dedicated_cluster" "example_cluster" {
        annotations         = {
            "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
            "tidb.cloud/has-set-password"   = "false"
        }
        cloud_provider      = "aws"
        cluster_id          = "10528940229200000000"
        create_time         = "2025-06-06 06:25:29.878 +0000 UTC"
        created_by          = "apikey-XXXXXXXX"
        display_name        = "test-tf"
        labels              = {
            "tidb.cloud/organization" = "60000"
            "tidb.cloud/project"      = "3190000"
        }
        port                = 4000
        project_id          = "3190000"
        region_display_name = "Oregon (us-west-2)"
        region_id           = "aws-us-west-2"
        state               = "ACTIVE"
        tidb_node_setting   = {
            endpoints               = [
                {
                    connection_type = "PUBLIC"
                    host            = "tidb.taiqixxxxxxx.clusters.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "VPC_PEERING"
                    host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
                {
                    connection_type = "PRIVATE_ENDPOINT"
                    host            = "privatelink-19319608.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                    port            = 4000
                },
            ]
            is_default_group        = true
            node_count              = 1
            node_group_display_name = "DefaultGroup"
            node_group_id           = "1931960832800000000"
            node_spec_display_name  = "2 vCPU, 4 GiB beta"
            node_spec_key           = "2C4G"
            public_endpoint_setting = {
                enabled        = false
                ip_access_list = []
            }
            state                   = "ACTIVE"
        }
        tikv_node_setting   = {
            node_count             = 3
            node_spec_display_name = "2 vCPU, 4 GiB"
            node_spec_key          = "2C4G"
            storage_size_gi        = 60
            storage_type           = "Standard"
        }
        update_time         = "2025-06-06 06:31:42.974 +0000 UTC"
        version             = "v7.5.6"
    }
    ```

## TiDB Cloud Dedicated クラスターを変更する {#modify-a-tidb-cloud-dedicated-cluster}

TiDB Cloud Dedicated クラスターの場合、Terraform を使用して次のようにリソースを管理できます。

-   クラスターにTiFlashコンポーネントを追加します。
-   クラスターをスケールします。
-   クラスターを一時停止または再開します。
-   クラスターに[TiDBノードグループ](/tidb-cloud/tidb-node-group-overview.md)追加します。
-   クラスターの TiDB ノード グループを更新します。
-   クラスターの TiDB ノード グループを削除します。

### TiFlashコンポーネントを追加する {#add-a-tiflash-component}

1.  [クラスターを作成する](#create-a-tidb-cloud-dedicated-cluster)実行するときに使用する`cluster.tf`ファイルに、 `tiflash_node_setting`構成を追加します。

    例えば：

        tiflash_node_setting = {
          node_spec_key = "2C4G"
          node_count = 3
          storage_size_gi = 60
        }

2.  `terraform apply`コマンドを実行します。

    ```shell
    $ terraform apply

    tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_dedicated_cluster.example_cluster will be updated in-place
      ~ resource "tidbcloud_dedicated_cluster" "example_cluster" {
          ~ annotations          = {
              - "tidb.cloud/available-features" = "DELEGATE_USER,DISABLE_PUBLIC_LB,PRIVATELINK"
              - "tidb.cloud/has-set-password"   = "false"
            } -> (known after apply)
          ~ labels               = {
              - "tidb.cloud/organization" = "60000"
              - "tidb.cloud/project"      = "3190000"
            } -> (known after apply)
          + pause_plan           = (known after apply)
          ~ state                = "ACTIVE" -> (known after apply)
          ~ tidb_node_setting    = {
              ~ endpoints               = [
                  - {
                      - connection_type = "PUBLIC"
                      - host            = "tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                  - {
                      - connection_type = "VPC_PEERING"
                      - host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                  - {
                      - connection_type = "PRIVATE_ENDPOINT"
                      - host            = "privatelink-19320029.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                      - port            = 4000
                    },
                ] -> (known after apply)
              ~ node_spec_display_name  = "2 vCPU, 4 GiB" -> (known after apply)
              ~ state                   = "ACTIVE" -> (known after apply)
                # (6 unchanged attributes hidden)
            }
          + tiflash_node_setting = {
              + node_count             = 3
              + node_spec_display_name = (known after apply)
              + node_spec_key          = "2C4G"
              + storage_size_gi        = 60
              + storage_type           = (known after apply)
            }
          ~ tikv_node_setting    = {
              ~ node_spec_display_name = "2 vCPU, 4 GiB" -> (known after apply)
              ~ storage_type           = "Standard" -> (known after apply)
                # (3 unchanged attributes hidden)
            }
          ~ update_time          = "2025-06-06 09:19:01.548 +0000 UTC" -> (known after apply)
          ~ version              = "v7.5.6" -> (known after apply)
            # (9 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes
    ```

    上記の実行プランでは、 TiFlashが追加され、1 つのリソースが変更されます。

3.  計画の内容がすべて問題ない場合は、「 `yes`と入力して続行します。

    ```shell
      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Modifying...
    tidbcloud_dedicated_cluster.example_cluster: Still modifying... [10s elapsed]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4.  `terraform state show tidbcloud_dedicated_cluster.${resource-name}`使用して状態を確認します。

        $ terraform state show tidbcloud_dedicated_cluster.example_cluster

        # tidbcloud_dedicated_cluster.example_cluster:
        resource "tidbcloud_dedicated_cluster" "example_cluster" {
            annotations         = {
                "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
                "tidb.cloud/has-set-password"   = "false"
            }
            cloud_provider      = "aws"
            cluster_id          = "1379661944600000000"
            create_time         = "2025-06-06 06:25:29.878 +0000 UTC"
            created_by          = "apikey-XXXXXXXX"
            display_name        = "test-tf"
            labels              = {
                "tidb.cloud/organization" = "60000"
                "tidb.cloud/project"      = "3100000"
            }
            port                = 4000
            project_id          = "3100000"
            region_display_name = "Oregon (us-west-2)"
            region_id           = "aws-us-west-2"
            state               = "ACTIVE"
            tidb_node_setting   = {
                endpoints               = [
                    {
                        connection_type = "PUBLIC"
                        host            = "tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                        port            = 4000
                    },
                    {
                        connection_type = "VPC_PEERING"
                        host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                        port            = 4000
                    },
                    {
                        connection_type = "PRIVATE_ENDPOINT"
                        host            = null
                        port            = 4000
                    },
                ]
                is_default_group        = true
                node_count              = 1
                node_group_display_name = "DefaultGroup"
                node_group_id           = "1931960832833000000"
                node_spec_display_name  = "2 vCPU, 4 GiB beta"
                node_spec_key           = "2C4G"
                state                   = "ACTIVE"
            }
            tiflash_node_setting = {
                node_count             = 3
                node_spec_display_name = "2 vCPU, 4 GiB"
                node_spec_key          = "2C4G"
                storage_size_gi        = 60
                storage_type           = "Basic"
            }
            tikv_node_setting   = {
                node_count             = 3
                node_spec_display_name = "2 vCPU, 4 GiB"
                node_spec_key          = "2C4G"
                storage_size_gi        = 60
                storage_type           = "Standard"
            }
            update_time         = "2025-06-06 08:31:42.974 +0000 UTC"
            version             = "v7.5.6"
        }

状態`MODIFYING`は、クラスターが変更中であることを示します。変更が完了すると、状態は`ACTIVE`に変わります。

### クラスターをスケールする {#scale-a-cluster}

状態が`ACTIVE`の場合、 TiDB Cloud Dedicated クラスターをスケーリングできます。

1.  [クラスターを作成する](#create-a-tidb-cloud-dedicated-cluster)際に使用する`cluster.tf`ファイルで、 `tidb_node_setting` 、 `tikv_node_setting` 、 `tiflash_node_setting`の設定を編集します。

    たとえば、TiDB ノードを 1 つ、TiKV ノードを 3 つ (スケーリング ステップが 3 であるため、TiKV ノードの数は 3 の倍数である必要があります)、およびTiFlashノードを 1 つ追加するには、次のように構成を編集します。

         tidb_node_setting = {
           node_spec_key = "8C16G"
           node_count = 2
         }
         tikv_node_setting = {
           node_spec_key = "8C32G"
           node_count = 6
           storage_size_gi = 200
         }
         tiflash_node_setting = {
           node_spec_key = "8C64G"
           node_count = 4
           storage_size_gi = 200
         }

2.  `terraform apply`コマンドを実行し、確認のために`yes`入力します。

        tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

        Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
          ~ update in-place

        Terraform will perform the following actions:

          # tidbcloud_dedicated_cluster.example_cluster will be updated in-place
          ~ resource "tidbcloud_dedicated_cluster" "example_cluster" {
              ~ annotations          = {
                  - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
                  - "tidb.cloud/has-set-password"   = "false"
                } -> (known after apply)
              ~ labels               = {
                  - "tidb.cloud/organization" = "60205"
                  - "tidb.cloud/project"      = "3199728"
                } -> (known after apply)
              + pause_plan           = (known after apply)
              ~ state                = "ACTIVE" -> (known after apply)
              ~ tidb_node_setting    = {
                  ~ endpoints               = [
                      - {
                          - connection_type = "PUBLIC"
                          - host            = "tidb.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                          - port            = 4000
                        },
                      - {
                          - connection_type = "VPC_PEERING"
                          - host            = "private-tidb.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                          - port            = 4000
                        },
                      - {
                          - connection_type = "PRIVATE_ENDPOINT"
                          - host            = "privatelink-19320029.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                          - port            = 4000
                        },
                    ] -> (known after apply)
                  ~ node_count              = 3 -> 2
                  ~ node_spec_display_name  = "8 vCPU, 16 GiB" -> (known after apply)
                  ~ state                   = "ACTIVE" -> (known after apply)
                    # (5 unchanged attributes hidden)
                }
              ~ tiflash_node_setting = {
                  ~ node_count             = 3 -> 4
                  ~ node_spec_display_name = "8 vCPU, 64 GiB" -> (known after apply)
                  ~ storage_type           = "Basic" -> (known after apply)
                    # (2 unchanged attributes hidden)
                }
              ~ tikv_node_setting    = {
                  ~ node_count             = 3 -> 6
                  ~ node_spec_display_name = "8 vCPU, 32 GiB" -> (known after apply)
                  ~ storage_type           = "Standard" -> (known after apply)
                    # (2 unchanged attributes hidden)
                }
              ~ update_time          = "2025-06-09 09:29:25.678 +0000 UTC" -> (known after apply)
              ~ version              = "v7.5.6" -> (known after apply)
                # (9 unchanged attributes hidden)
            }

        Plan: 0 to add, 1 to change, 0 to destroy.

        Do you want to perform these actions?
          Terraform will perform the actions described above.
          Only 'yes' will be accepted to approve.

          Enter a value: yes

        tidbcloud_dedicated_cluster.example_cluster: Modifying...
        tidbcloud_dedicated_cluster.example_cluster: Still modifying... [10s elapsed]

        Apply complete! Resources: 0 added, 1 changed, 0 destroyed.

プロセスが完了するまでお待ちください。スケーリングが完了すると状態が`ACTIVE`に変わります。

### クラスターを一時停止または再開する {#pause-or-resume-a-cluster}

クラスターの状態が`ACTIVE`ときにクラスターを一時停止し、状態が`PAUSED`ときにクラスターを再開することができます。

-   クラスターを一時停止するには`paused = true`設定します。
-   クラスターを再開するには`paused = false`設定します。

1.  [クラスターを作成する](#create-a-tidb-cloud-dedicated-cluster)実行するときに使用する`cluster.tf`ファイルで、構成に`pause = true`追加します。

        paused = true

2.  `terraform apply`コマンドを実行し、プランを確認した後、 `yes`入力します。

    ```shell
    $ terraform apply

     tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

     Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
       ~ update in-place

     Terraform will perform the following actions:

       # tidbcloud_dedicated_cluster.example_cluster will be updated in-place
       ~ resource "tidbcloud_dedicated_cluster" "example_cluster" {
           ~ annotations          = {
               - "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
               - "tidb.cloud/has-set-password"   = "false"
             } -> (known after apply)
           ~ labels               = {
               - "tidb.cloud/organization" = "60205"
               - "tidb.cloud/project"      = "3199728"
             } -> (known after apply)
           + pause_plan           = (known after apply)
           + paused               = true
           ~ state                = "ACTIVE" -> (known after apply)
           ~ tidb_node_setting    = {
               ~ endpoints               = [
                   - {
                       - connection_type = "PUBLIC"
                       - host            = "tidb.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                       - port            = 4000
                     },
                   - {
                       - connection_type = "VPC_PEERING"
                       - host            = "private-tidb.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                       - port            = 4000
                     },
                   - {
                       - connection_type = "PRIVATE_ENDPOINT"
                       - host            = "privatelink-19320029.nwdkyh1smmxk.clusters.dev.tidb-cloud.com"
                       - port            = 4000
                     },
                 ] -> (known after apply)
               ~ node_spec_display_name  = "8 vCPU, 16 GiB" -> (known after apply)
               ~ state                   = "ACTIVE" -> (known after apply)
                 # (6 unchanged attributes hidden)
             }
           ~ tiflash_node_setting = {
               ~ node_spec_display_name = "8 vCPU, 64 GiB" -> (known after apply)
               ~ storage_type           = "Basic" -> (known after apply)
                 # (3 unchanged attributes hidden)
             }
           ~ tikv_node_setting    = {
               ~ node_spec_display_name = "8 vCPU, 32 GiB" -> (known after apply)
               ~ storage_type           = "Standard" -> (known after apply)
                 # (3 unchanged attributes hidden)
             }
           ~ update_time          = "2025-06-09 10:01:59.65 +0000 UTC" -> (known after apply)
           ~ version              = "v7.5.6" -> (known after apply)
             # (9 unchanged attributes hidden)
       }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Modifying...
    tidbcloud_dedicated_cluster.example_cluster: Still modifying... [10s elapsed]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

3.  状態を確認するには、 `terraform state show tidbcloud_dedicated_cluster.${resource-name}`コマンドを使用します。

        $ terraform state show tidbcloud_dedicate_cluster.example_cluster

        resource "tidbcloud_dedicated_cluster" "example_cluster" {
             annotations         = {
                 "tidb.cloud/available-features" = "DISABLE_PUBLIC_LB,PRIVATELINK,DELEGATE_USER"
                 "tidb.cloud/has-set-password"   = "false"
             }
             cloud_provider      = "aws"
             cluster_id          = "1379661944600000000"
             create_time         = "2025-06-06 06:25:29.878 +0000 UTC"
             created_by          = "apikey-XXXXXXXX"
             display_name        = "test-tf"
             labels              = {
                 "tidb.cloud/organization" = "60000"
                 "tidb.cloud/project"      = "3100000"
             } 
             paused              = true
             port                = 4000
             project_id          = "3100000"
             region_display_name = "Oregon (us-west-2)"
             region_id           = "aws-us-west-2"
             state               = "PAUSED"
             tidb_node_setting   = {
                 endpoints               = [
                     {
                         connection_type = "PUBLIC"
                         host            = "tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                         port            = 4000
                     },
                     {
                         connection_type = "VPC_PEERING"
                         host            = "private-tidb.taiqixxxxxxx.clusters.dev.tidb-cloud.com"
                         port            = 4000
                     },
                     {
                         connection_type = "PRIVATE_ENDPOINT"
                         host            = null
                         port            = 4000
                     },
                 ]
                 is_default_group        = true
                 node_count              = 1
                 node_group_display_name = "DefaultGroup"
                 node_group_id           = "1931960832833000000"
                 node_spec_display_name  = "2 vCPU, 4 GiB beta"
                 node_spec_key           = "2C4G"
                 state                   = "ACTIVE"
             }
             tikv_node_setting   = {
                 node_count             = 3
                 node_spec_display_name = "2 vCPU, 4 GiB"
                 node_spec_key          = "2C4G"
                 storage_size_gi        = 60
                 storage_type           = "Standard"
             }
             update_time         = "2025-06-06 06:31:42.974 +0000 UTC"
             version             = "v7.5.6"
         }

4.  クラスターを再開する必要がある場合は、 `paused = false`設定します。

        paused = false

5.  `terraform apply`コマンドを実行し、確認のために`yes`入力します。しばらく待つと、最終的に状態が`ACTIVE`に変更されます。

### クラスターにTiDBノードグループを追加する {#add-a-tidb-node-group-to-the-cluster}

状態が`ACTIVE`の場合、TiDB ノード グループをクラスターに追加できます。

1.  [クラスターを作成する](#create-a-tidb-cloud-dedicated-cluster)実行するときに使用する`cluster.tf`ファイルに、 `tidbcloud_dedicated_node_group`構成を追加します。

    たとえば、3 つのノードを持つ TiDB ノード グループを追加するには、次のように構成を編集します。

        resource "tidbcloud_dedicated_node_group" "example_group" {
            cluster_id = tidbcloud_dedicated_cluster.example_cluster.cluster_id
            node_count = 3
            display_name = "test-node-group"
        }

2.  `terraform apply`コマンドを実行し、確認のために`yes`入力します。

    ```shell
    $ terraform apply
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
     + create

    Terraform will perform the following actions:

     # tidbcloud_dedicated_node_group.example_group will be created
     + resource "tidbcloud_dedicated_node_group" "example_group" {
         + cluster_id              = "10526169210080596964"
         + display_name            = "test-node-group2"
         + endpoints               = (known after apply)
         + is_default_group        = (known after apply)
         + node_count              = 3
         + node_group_id           = (known after apply)
         + node_spec_display_name  = (known after apply)
         + node_spec_key           = (known after apply)
         + public_endpoint_setting = (known after apply)
         + state                   = (known after apply)
       }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
     Terraform will perform the actions described above.
     Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_node_group.example_group: Creating...
    tidbcloud_dedicated_node_group.example_group: Still creating... [10s elapsed]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

3.  状態を確認するには、 `terraform state show tidbcloud_dedicated_node_group.${resource-name}`コマンドを使用します。

    ```shell
    $ terraform state show tidbcloud_dedicated_node_group.example_group
    tidbcloud_dedicated_node_group.example_group:
    resource "tidbcloud_dedicated_node_group" "example_group" {
        cluster_id             = "10526169210000000000"
        display_name           = "test-node-group"
        endpoints              = [
            {
                connection_type = "PUBLIC"
                host            = null
                port            = 0
            },
            {
                connection_type = "VPC_PEERING"
                host            = "private-tidb.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                port            = 4000
            },
            {
                connection_type = "PRIVATE_ENDPOINT"
                host            = "privatelink-19320383.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                port            = 4000
            },
        ]
        is_default_group       = false
        node_count             = 3
        node_group_id          = "1932038361900000000"
        node_spec_display_name = "8 vCPU, 16 GiB"
        node_spec_key          = "8C16G"
        state                  = "ACTIVE"
    }
    ```

### クラスターのTiDBノードグループを更新する {#update-a-tidb-node-group-of-the-cluster}

クラスターの TiDB ノード グループの状態が`ACTIVE`場合、そのグループを更新できます。

1.  [クラスターを作成する](#create-a-tidb-cloud-dedicated-cluster)際に使用する`cluster.tf`ファイルで、 `tidbcloud_dedicated_node_group`の設定を編集します。

    たとえば、ノード数を`1`に変更するには、次のように構成を編集します。

        resource "tidbcloud_dedicated_node_group" "example_group" {
            cluster_id = tidbcloud_dedicated_cluster.example_cluster.cluster_id
            node_count = 1
            display_name = "test-node-group"
        }

2.  `terraform apply`コマンドを実行し、確認のために`yes`入力します。

    ```shell
    $ terraform apply
    tidbcloud_dedicated_node_group.example_group: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_dedicated_node_group.example_group will be updated in-place
      ~ resource "tidbcloud_dedicated_node_group" "example_group" {
          ~ endpoints               = [
              - {
                  - connection_type = "PUBLIC"
                  - port            = 0
                    # (1 unchanged attribute hidden)
                },
              - {
                  - connection_type = "VPC_PEERING"
                  - host            = "private-tidb.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                  - port            = 4000
                },
              - {
                  - connection_type = "PRIVATE_ENDPOINT"
                  - host            = "privatelink-19320383.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                  - port            = 4000
                },
            ] -> (known after apply)
          ~ node_count              = 3 -> 1
          ~ node_spec_display_name  = "8 vCPU, 16 GiB" -> (known after apply)
          ~ node_spec_key           = "8C16G" -> (known after apply)
          ~ state                   = "ACTIVE" -> (known after apply)
            # (5 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_node_group.example_group: Modifying...
    tidbcloud_dedicated_node_group.example_group: Still modifying... [10s elapsed]
    tidbcloud_dedicated_node_group.example_group: Modifications complete after 24s

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

### クラスターの TiDB ノード グループを削除します {#delete-a-tidb-node-group-of-the-cluster}

クラスターの TiDB ノード グループを削除するには、 `dedicated_node_group`リソースの構成を削除し、 `terraform apply`コマンドを使用してリソースを破棄します。

```shell
  $ terraform apply
  tidbcloud_dedicated_node_group.example_group: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy

  Terraform will perform the following actions:

    # tidbcloud_dedicated_node_group.example_group will be destroyed
    # (because tidbcloud_dedicated_node_group.example_group is not in configuration)
    - resource "tidbcloud_dedicated_node_group" "example_group" {
        - cluster_id              = "10526169210000000000" -> null
        - display_name            = "test-node-group" -> null
        - endpoints               = [
            - {
                - connection_type = "PUBLIC"
                - port            = 0
                  # (1 unchanged attribute hidden)
              },
            - {
                - connection_type = "VPC_PEERING"
                - host            = "private-tidb.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                - port            = 4000
              },
            - {
                - connection_type = "PRIVATE_ENDPOINT"
                - host            = "privatelink-19320383.pvqmzrxxxxxx.clusters.dev.tidb-cloud.com"
                - port            = 4000
              },
          ] -> null
        - is_default_group        = false -> null
        - node_count              = 1 -> null
        - node_group_id           = "1932038361900000000" -> null
        - node_spec_display_name  = "8 vCPU, 16 GiB" -> null
        - node_spec_key           = "8C16G" -> null
        - public_endpoint_setting = {
            - enabled        = false -> null
            - ip_access_list = [] -> null
          } -> null
        - state                   = "PAUSED" -> null
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.

    Enter a value: yes

  tidbcloud_dedicated_node_group.example_group: Destroying...
  tidbcloud_dedicated_node_group.example_group: Destruction complete after 3s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

ここで、コマンド`terraform show`実行すると、リソースがクリアされているため何も表示されません。

    $ terraform show

## クラスターをインポートする {#import-a-cluster}

Terraform で管理されていない TiDB クラスターの場合は、インポートするだけで Terraform を使用して管理できます。

次のように、Terraform によって作成されていないクラスターをインポートします。

1.  新しいTiDB Cloud Dedicated クラスター リソースのインポート ブロックを追加します。

    次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}`クラスター ID に置き換えます。

        import {
          to = tidbcloud_dedicated_cluster.example_cluster
          id = "${id}"
        }

2.  新しい構成ファイルを生成します。

    インポート ブロックに従って、新しいTiDB Cloud Dedicated クラスター リソースの新しい構成ファイルを生成します。

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

3.  生成された構成を確認して適用します。

    生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

    次に、 `terraform apply`実行してインフラストラクチャをインポートします。適用後の出力例は次のとおりです。

    ```shell
    tidbcloud_dedicated_cluster.example_cluster: Importing... 
    tidbcloud_dedicated_cluster.example_cluster: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

これで、インポートしたクラスターを Terraform で管理できるようになりました。

## TiDB Cloud Dedicated クラスターを削除する {#delete-a-tidb-cloud-dedicated-cluster}

TiDB Cloud Dedicated クラスターを削除するには、 `tidbcloud_dedicated_cluster`リソースの構成を削除してから、 `terraform apply`コマンドを使用してリソースを破棄します。

```shell
  $ terraform apply
  tidbcloud_dedicated_cluster.example_cluster: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy
   Terraform will perform the following actions:

    # tidbcloud_dedicated_cluster.example_cluster will be destroyed
    # (because tidbcloud_dedicated_cluster.example_cluster is not in configuration)
    - resource "tidbcloud_dedicated_cluster" "example_cluster" {
        - annotations          = {
            - "tidb.cloud/available-features" = "DELEGATE_USER,DISABLE_PUBLIC_LB,PRIVATELINK"
            - "tidb.cloud/has-set-password"   = "false"
          } -> null
        - cloud_provider       = "aws" -> null
        - cluster_id           = "10526169210000000000" -> null
        - create_time          = "2025-06-06 09:12:55.396 +0000 UTC" -> null
        - created_by           = "apikey-K1R3JIC0" -> null
        - display_name         = "test-tf" -> null
        - labels               = {
            - "tidb.cloud/organization" = "60000"
            - "tidb.cloud/project"      = "3100000"
          } -> null
        - paused               = false -> null
        - port                 = 4000 -> null
        - project_id           = "3100000" -> null
        - region_display_name  = "Oregon (us-west-2)" -> null
        - region_id            = "aws-us-west-2" -> null
        - state                = "ACTIVE" -> null
        - tidb_node_setting    = {
            - endpoints               = [
                - {
                    - connection_type = "PUBLIC"
                    - host            = "tidb.nwdkyhxxxxxx.clusters.dev.tidb-cloud.com"
                    - port            = 4000
                  },
                - {
                    - connection_type = "VPC_PEERING"
                    - host            = "private-tidb.nwdkyhxxxxxx.clusters.dev.tidb-cloud.com"
                    - port            = 4000
                  },
                - {
                    - connection_type = "PRIVATE_ENDPOINT"
                    - host            = "privatelink-19320000.nwdkyhxxxxxx.clusters.dev.tidb-cloud.com"
                    - port            = 4000
                  },
              ] -> null
            - is_default_group        = true -> null
            - node_count              = 2 -> null
            - node_group_display_name = "DefaultGroup" -> null
            - node_group_id           = "1932002964533000000" -> null
            - node_spec_display_name  = "8 vCPU, 16 GiB" -> null
            - node_spec_key           = "8C16G" -> null
            - public_endpoint_setting = {
                - enabled        = true -> null
                - ip_access_list = [
                    - {
                        - cidr_notation = "0.0.0.0/32"
                          # (1 unchanged attribute hidden)
                      },
                  ] -> null
              } -> null
            - state                   = "ACTIVE" -> null
          } -> null
        - tiflash_node_setting = {
            - node_count             = 4 -> null
            - node_spec_display_name = "8 vCPU, 64 GiB" -> null
            - node_spec_key          = "8C64G" -> null
            - storage_size_gi        = 200 -> null
            - storage_type           = "Basic" -> null
          } -> null
        - tikv_node_setting    = {
            - node_count             = 6 -> null
            - node_spec_display_name = "8 vCPU, 32 GiB" -> null
            - node_spec_key          = "8C32G" -> null
            - storage_size_gi        = 200 -> null
            - storage_type           = "Standard" -> null
          } -> null
        - update_time          = "2025-06-06 14:15:29.609 +0000 UTC" -> null
        - version              = "v7.5.6" -> null
      }

    Plan: 0 to add, 0 to change, 1 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_cluster.example_cluster: Destroying...
    tidbcloud_dedicated_cluster.example_cluster: Destruction complete after 3s

    Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

ここで、 `terraform show`コマンドを実行すると、リソースがクリアされているため、管理対象リソースは表示されません。

    $ terraform show
