---
title: Use Cluster Resource
summary: Learn how to use the cluster resource to create and modify a TiDB Cloud cluster.
---

# クラスタリソースの使用 {#use-cluster-resource}

このドキュメントでは、 `tidbcloud_cluster`リソースを使用してTiDB Cloudクラスターを管理する方法を学習できます。

さらに、 `tidbcloud_projects`と`tidbcloud_cluster_specs`データ ソースを使用して必要な情報を取得する方法も学習します。

`tidbcloud_cluster`リソースの特徴は次のとおりです。

-   TiDB サーバーレス クラスターと TiDB 専用クラスターを作成します。
-   TiDB 専用クラスターを変更します。
-   TiDB サーバーレス クラスターと TiDB 専用クラスターを削除します。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) 。

## <code>tidbcloud_projects</code>データ ソースを使用してプロジェクト ID を取得する {#get-project-ids-using-the-code-tidbcloud-projects-code-data-source}

各 TiDB クラスターはプロジェクト内にあります。 TiDB クラスターを作成する前に、クラスターを作成するプロジェクトの ID を取得する必要があります。

利用可能なすべてのプロジェクトの情報を表示するには、次のように`tidbcloud_projects`データ ソースを使用します。

1.  [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md)のときに作成される`main.tf`ファイルに、次のように`data`と`output`ブロックを追加します。

    ```
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
    ```

    -   `data`ブロックを使用して、データ ソース タイプとデータ ソース名を含むTiDB Cloudのデータ ソースを定義します。

        -   プロジェクト データ ソースを使用するには、データ ソース タイプを`tidbcloud_projects`に設定します。
        -   データソース名については、必要に応じて定義できます。たとえば、「example_project」などです。
        -   `tidbcloud_projects`データ ソースの場合、 `page`と`page_size`属性を使用して、チェックするプロジェクトの最大数を制限できます。

    -   `output`ブロックを使用して、出力に表示されるデータ ソース情報を定義し、他の Terraform 構成で使用する情報を公開します。

        `output`ブロックは、プログラミング言語の戻り値と同様に機能します。詳細については、 [Terraform ドキュメント](https://www.terraform.io/language/values/outputs)参照してください。

    リソースとデータ ソースで使用可能なすべての構成を取得するには、この[設定ドキュメント](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)参照してください。

2.  `terraform apply`コマンドを実行して構成を適用します。続行するには、確認プロンプトで`yes`入力する必要があります。

    プロンプトをスキップするには、 `terraform apply --auto-approve`を使用します。

    ```
    $ terraform apply --auto-approve

    Changes to Outputs:
      + projects = [
          + {
              + cluster_count    = 0
              + create_timestamp = "1649154426"
              + id               = "1372813089191121286"
              + name             = "test1"
              + org_id           = "1372813089189921287"
              + user_count       = 1
            },
          + {
              + cluster_count    = 1
              + create_timestamp = "1640602740"
              + id               = "1372813089189561287"
              + name             = "default project"
              + org_id           = "1372813089189921287"
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
        "id" = "1372813089191121286"
        "name" = "test1"
        "org_id" = "1372813089189921287"
        "user_count" = 1
      },
      {
        "cluster_count" = 1
        "create_timestamp" = "1640602740"
        "id" = "1372813089189561287"
        "name" = "default project"
        "org_id" = "1372813089189921287"
        "user_count" = 1
      },
    ])
    ```

これで、利用可能なすべてのプロジェクトを出力から取得できるようになりました。必要なプロジェクト ID の 1 つをコピーします。

## <code>tidbcloud_cluster_specs</code>データ ソースを使用してクラスター仕様情報を取得する {#get-cluster-specification-information-using-the-code-tidbcloud-cluster-specs-code-data-source}

クラスターを作成する前に、クラスター仕様情報を取得する必要があります。これには、使用可能なすべての構成値 (サポートされているクラウド プロバイダー、リージョン、ノード サイズなど) が含まれています。

クラスター仕様情報を取得するには、次のように`tidbcloud_cluster_specs`データ ソースを使用できます。

1.  `main.tf`ファイルを次のように編集します。

    ```
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
    data "tidbcloud_cluster_specs" "example_cluster_spec" {
    }
    output "cluster_spec" {
      value = data.tidbcloud_cluster_specs.example_cluster_spec.items
    }
    ```

2.  `terraform apply --auto-approve`コマンドを実行すると、クラスターの仕様情報が取得されます。

    次の行をクリックすると、結果例の一部が参照用に表示されます。

    <details><summary>クラスタ仕様</summary>

    ```
    {
        "cloud_provider" = "AWS"
        "cluster_type" = "DEDICATED"
        "region" = "eu-central-1"
        "tidb" = tolist([
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "2C8G"
          },
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "4C16G"
          },
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "8C16G"
          },
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "16C32G"
          },
        ])
        "tiflash" = tolist([
          {
            "node_quantity_range" = {
              "min" = 0
              "step" = 1
            }
            "node_size" = "8C64G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 0
              "step" = 1
            }
            "node_size" = "16C128G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 500
            }
          },
        ])
        "tikv" = tolist([
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "2C8G"
            "storage_size_gib_range" = {
              "max" = 500
              "min" = 200
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "4C16G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 200
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "8C32G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "8C64G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "16C64G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
        ])
      }
    ```

    </details>

結果は次のとおりです。

-   `cloud_provider`は、TiDB クラスターをホストできるクラウド プロバイダーです。
-   `region`は`cloud_provider`の領域です。
-   `node_quantity_range`最小ノード番号とノードをスケーリングするステップを示します。
-   `node_size`はノードのサイズです。
-   `storage_size_gib_range`ノードに設定できる最小および最大storageサイズを示します。

## クラスターリソースを使用してクラスターを作成する {#create-a-cluster-using-the-cluster-resource}

> **ノート：**
>
> 始める前に、 TiDB Cloudコンソールでプロジェクト CIDR を設定していることを確認してください。詳細については、 [プロジェクトCIDRを設定する](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr)を参照してください。

`tidbcloud_cluster`リソースを使用してクラスターを作成できます。

次の例は、TiDB 専用クラスターを作成する方法を示しています。

1.  クラスター用のディレクトリを作成し、そこに入ります。

2.  `cluster.tf`ファイルを作成します。

    ```
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

    resource "tidbcloud_cluster" "example_cluster" {
      project_id     = "1372813089189561287"
      name           = "firstCluster"
      cluster_type   = "DEDICATED"
      cloud_provider = "AWS"
      region         = "eu-central-1"
      config = {
        root_password = "Your_root_password1."
        port = 4000
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 1
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500,
            node_quantity : 3
          }
        }
      }
    }
    ```

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細を含むTiDB Cloudのリソースを定義します。

    -   クラスター リソースを使用するには、リソース タイプを`tidbcloud_cluster`に設定します。
    -   リソース名については、必要に応じて定義できます。たとえば、 `example_cluster` 。
    -   リソースの詳細は、プロジェクトIDとクラスタ仕様情報に従って設定できます。

3.  `terraform apply`コマンドを実行します。リソースを適用するときに`terraform apply --auto-approve`使用することはお勧めできません。

    ```shell
    $ terraform apply

    Terraform will perform the following actions:

      # tidbcloud_cluster.example_cluster will be created
      + resource "tidbcloud_cluster" "example_cluster" {
          + cloud_provider = "AWS"
          + cluster_type   = "DEDICATED"
          + config         = {
              + components     = {
                  + tidb = {
                      + node_quantity = 1
                      + node_size     = "8C16G"
                    }
                  + tikv = {
                      + node_quantity    = 3
                      + node_size        = "8C32G"
                      + storage_size_gib = 500
                    }
                }
              + ip_access_list = [
                  + {
                      + cidr        = "0.0.0.0/0"
                      + description = "all"
                    },
                ]
              + port           = 4000
              + root_password  = "Your_root_password1."
            }
          + id             = (known after apply)
          + name           = "firstCluster"
          + project_id     = "1372813089189561287"
          + region         = "eu-central-1"
          + status         = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

    上記の結果のように、Terraform は実行プランを生成します。これには、Terraform が実行するアクションが記述されています。

    -   設定と状態の違いを確認できます。
    -   この`apply`の結果も確認できます。新しいリソースが追加されますが、リソースが変更されたり破棄されたりすることはありません。
    -   `known after apply` `apply`の後の値を取得することを示します。

4.  計画にすべて問題がない場合は、 `yes`と入力して続行します。

    ```
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_cluster.example_cluster: Creating...
    tidbcloud_cluster.example_cluster: Creation complete after 1s [id=1379661944630234067]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

    ```

5.  `terraform show`または`terraform state show tidbcloud_cluster.${resource-name}`コマンドを使用して、リソースの状態を検査します。前者は、すべてのリソースとデータ ソースの状態を表示します。

    ```shell
    $ terraform state show tidbcloud_cluster.example_cluster

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tikv = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "CREATING"
    }
    ```

    クラスターのステータスは`CREATING`です。この場合、 `AVAILABLE`に変更されるまで待つ必要があります。通常は少なくとも 10 分かかります。

6.  最新の状態を確認したい場合は、 `terraform refresh`コマンドを実行して状態を更新し、 `terraform state show tidbcloud_cluster.${resource-name}`コマンドを実行して状態を表示します。

    ```
    $ terraform refresh

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    $ terraform state show tidbcloud_cluster.example_cluste

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tikv = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "AVAILABLE"
    }
    ```

ステータスが`AVAILABLE`の場合、TiDB クラスターが作成され、使用する準備ができていることを示します。

## TiDB 専用クラスターを変更する {#modify-a-tidb-dedicated-cluster}

TiDB 専用クラスターの場合、Terraform を使用して次のようにクラスター リソースを管理できます。

-   TiFlashコンポーネントをクラスターに追加します。
-   クラスターをスケーリングします。
-   クラスターを一時停止または再開します。

### TiFlashコンポーネントを追加する {#add-a-tiflash-component}

1.  [クラスターを作成する](#create-a-cluster-using-the-cluster-resource)実行するときに使用される`cluster.tf`ファイルで、 `tiflash`構成を`components`フィールドに追加します。

    例えば：

    ```
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 1
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500
            node_quantity : 3
          }
          tiflash = {
            node_size : "8C64G"
            storage_size_gib : 500
            node_quantity : 1
          }
        }
    ```

2.  `terraform apply`コマンドを実行します。

    ```
    $ terraform apply

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_cluster.example_cluster will be updated in-place
      ~ resource "tidbcloud_cluster" "example_cluster" {
          ~ config         = {
              ~ components     = {
                  + tiflash = {
                      + node_quantity    = 1
                      + node_size        = "8C64G"
                      + storage_size_gib = 500
                    }
                    # (2 unchanged attributes hidden)
                }
                # (3 unchanged attributes hidden)
            }
            id             = "1379661944630234067"
            name           = "firstCluster"
          ~ status         = "AVAILABLE" -> (known after apply)
            # (4 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:

    ```

    上記の実行計画と同様に、 TiFlashが追加され、リソースが 1 つ変更されます。

3.  計画にすべて問題がない場合は、 `yes`と入力して続行します。

    ```
      Enter a value: yes

    tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
    tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4.  ステータスを表示するには`terraform state show tidbcloud_cluster.${resource-name}`を使用します。

    ```
    $ terraform state show tidbcloud_cluster.example_cluster

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb    = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 1
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "MODIFYING"
    }
    ```

ステータス`MODIFYING`は、クラスターが現在変更中であることを示します。ちょっと待ってください。ステータスは`AVAILABLE`に変更されます。

### TiDB クラスターをスケールする {#scale-a-tidb-cluster}

TiDB クラスターのステータスが`AVAILABLE`の場合、TiDB クラスターをスケーリングできます。

1.  [クラスターを作成する](#create-a-cluster-using-the-cluster-resource)のときに使用する`cluster.tf`ファイルで、 `components`構成を編集します。

    たとえば、TiDB にノードを 1 つ追加し、TiKV にノードを 3 つ追加するには (ステップが 3 であるため、TiKV ノードの数は 3 の倍数である必要があります[この情報はクラスター仕様から取得します。](#get-cluster-specification-information-using-the-tidbcloud_cluster_specs-data-source)にすることができます)、 TiFlashにノードをもう 1 つ追加するには、編集できます。構成は次のとおりです。

    ```
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 2
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500
            node_quantity : 6
          }
          tiflash = {
            node_size : "8C64G"
            storage_size_gib : 500
            node_quantity : 2
          }
        }
    ```

2.  `terraform apply`コマンドを実行し、確認のために`yes`を入力します。

    ```
    $ terraform apply

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_cluster.example_cluster will be updated in-place
      ~ resource "tidbcloud_cluster" "example_cluster" {
          ~ config         = {
              ~ components     = {
                  ~ tidb    = {
                      ~ node_quantity = 1 -> 2
                        # (1 unchanged attribute hidden)
                    }
                  ~ tiflash = {
                      ~ node_quantity    = 1 -> 2
                        # (2 unchanged attributes hidden)
                    }
                  ~ tikv    = {
                      ~ node_quantity    = 3 -> 6
                        # (2 unchanged attributes hidden)
                    }
                }
                # (3 unchanged attributes hidden)
            }
            id             = "1379661944630234067"
            name           = "firstCluster"
          ~ status         = "AVAILABLE" -> (known after apply)
            # (4 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
    tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

ステータスが`MODIFYING`から`AVAILABLE`に変わるまで待ちます。

### クラスターを一時停止または再開する {#pause-or-resume-a-cluster}

クラスターのステータスが`AVAILABLE`場合はクラスターを一時停止し、ステータスが`PAUSED`の場合はクラスターを再開できます。

-   クラスターを一時停止するには`paused = true`を設定します。
-   クラスターを再開するには`paused = false`を設定します。

1.  [クラスターを作成する](#create-a-cluster-using-the-cluster-resource)のときに使用される`cluster.tf`ファイルで、 `config`構成に`pause = true`を追加します。

    ```
    config = {
        paused = true
        root_password = "Your_root_password1."
        port          = 4000
        ...
      }
    ```

2.  `terraform apply`コマンドを実行し、確認後に`yes`を入力します。

    ```
    $ terraform apply

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_cluster.example_cluster will be updated in-place
      ~ resource "tidbcloud_cluster" "example_cluster" {
          ~ config         = {
              + paused         = true
                # (4 unchanged attributes hidden)
            }
            id             = "1379661944630234067"
            name           = "firstCluster"
          ~ status         = "AVAILABLE" -> (known after apply)
            # (4 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
    tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

3.  `terraform state show tidbcloud_cluster.${resource-name}`コマンドを使用してステータスを確認します。

    ```
    $ terraform state show tidbcloud_cluster.example_cluster

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb    = {
                    node_quantity = 2
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 2
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 6
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            paused         = true
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "PAUSED"
    }
    ```

4.  クラスターを再開する必要がある場合は、 `paused = false`を設定します。

    ```
    config = {
        paused = false
        root_password = "Your_root_password1."
        port          = 4000
        ...
      }
    ```

5.  `terraform apply`コマンドを実行し、確認のために`yes`を入力します。 `terraform state show tidbcloud_cluster.${resource-name}`コマンドを使用してステータスを確認すると、ステータスが`RESUMING`に変わることがわかります。

    ```
    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb    = {
                    node_quantity = 2
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 2
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 6
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            paused         = false
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "RESUMING"
    }
    ```

6.  しばらく待ってから、 `terraform refersh`コマンドを使用して状態を更新します。最終的にステータスは`AVAILABLE`になります。

これで、Terraform を使用して TiDB 専用クラスターを作成および管理できました。次に、 [バックアップリソース](/tidb-cloud/terraform-use-backup-resource.md)によってクラスターのバックアップを作成してみてください。

## クラスターをインポートする {#import-a-cluster}

Terraform によって管理されていない TiDB クラスターの場合は、インポートするだけで Terraform を使用して管理できます。

たとえば、Terraform によって作成されていないクラスターをインポートしたり、 [復元リソースを使用して作成された](/tidb-cloud/terraform-use-restore-resource.md#create-a-restore-task)のクラスターをインポートしたりできます。

1.  次のように`import_cluster.tf`ファイルを作成します。

    ```
    terraform {
     required_providers {
       tidbcloud = {
         source = "tidbcloud/tidbcloud"
       }
     }
    }
    resource "tidbcloud_cluster" "import_cluster" {}
    ```

2.  `terraform import tidbcloud_cluster.import_cluster projectId,clusterId`でクラスターをインポートします。

    例えば：

    ```
    $ terraform import tidbcloud_cluster.import_cluster 1372813089189561287,1379661944630264072

    tidbcloud_cluster.import_cluster: Importing from ID "1372813089189561287,1379661944630264072"...
    tidbcloud_cluster.import_cluster: Import prepared!
      Prepared tidbcloud_cluster for import
    tidbcloud_cluster.import_cluster: Refreshing state... [id=1379661944630264072]

    Import successful!

    The resources that were imported are shown above. These resources are now in
    your Terraform state and will henceforth be managed by Terraform.
    ```

3.  `terraform state show tidbcloud_cluster.import_cluster`コマンドを実行してクラスターのステータスを確認します。

    ```
    $ terraform state show tidbcloud_cluster.import_cluster

    # tidbcloud_cluster.import_cluster:
    resource "tidbcloud_cluster" "import_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components = {
                tidb    = {
                    node_quantity = 2
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 2
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 6
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            port       = 4000
        }
        id             = "1379661944630264072"
        name           = "restoreCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "AVAILABLE"
    }
    ```

4.  Terraform を使用してクラスターを管理するには、前のステップの出力を構成ファイルにコピーします。 `id`と`status`の行は Terraform によって制御されるため、削除する必要があることに注意してください。

    ```
    resource "tidbcloud_cluster" "import_cluster" {
          cloud_provider = "AWS"
          cluster_type   = "DEDICATED"
          config         = {
              components = {
                  tidb    = {
                      node_quantity = 2
                      node_size     = "8C16G"
                  }
                  tiflash = {
                      node_quantity    = 2
                      node_size        = "8C64G"
                      storage_size_gib = 500
                  }
                  tikv    = {
                      node_quantity    = 6
                      node_size        = "8C32G"
                      storage_size_gib = 500
                  }
              }
              port       = 4000
          }
          name           = "restoreCluster"
          project_id     = "1372813089189561287"
          region         = "eu-central-1"
    }
    ```

5.  `terraform fmt`を使用して構成ファイルをフォーマットできます。

    ```
    $ terraform fmt
    ```

6.  構成と状態の一貫性を確保するには、 `terraform plan`または`terraform apply`を実行します。 `No changes`が表示されれば、インポートは成功しています。

    ```
    $ terraform apply

    tidbcloud_cluster.import_cluster: Refreshing state... [id=1379661944630264072]

    No changes. Your infrastructure matches the configuration.

    Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

    Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
    ```

これで、Terraform を使用してクラスターを管理できるようになりました。

## クラスターを削除する {#delete-a-cluster}

クラスターを削除するには、対応する`cluster.tf`ファイルが存在するクラスター ディレクトリに移動し、 `terraform destroy`コマンドを実行してクラスター リソースを破棄します。

```
$ terraform destroy

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes
```

ここで`terraform show`コマンドを実行しても、リソースがクリアされているため、何も得られません。

```
$ terraform show
```
