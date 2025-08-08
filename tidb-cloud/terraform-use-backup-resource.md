---
title: Use Backup Resource
summary: バックアップ リソースを使用してTiDB Cloudクラスターのバックアップを作成する方法を学習します。
---

# バックアップリソースを使用する {#use-backup-resource}

このドキュメントでは、 `tidbcloud_backup`リソースを使用してTiDB Cloudクラスターのバックアップを作成する方法を学習できます。

`tidbcloud_backup`リソースの機能は次のとおりです。

-   TiDB Cloud Dedicated クラスターのバックアップを作成します。
-   TiDB Cloud Dedicated クラスターのバックアップを削除します。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) 。
-   バックアップと復元機能は、 TiDB Cloud Serverless クラスターではご利用いただけません。バックアップリソースを使用するには、 TiDB Cloud Dedicated クラスターを作成してください。

## バックアップリソースを使用してバックアップを作成する {#create-a-backup-with-the-backup-resource}

1.  バックアップ用のディレクトリを作成してそこに入ります。

2.  `backup.tf`ファイルを作成します。

    例えば：

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
        resource "tidbcloud_backup" "example_backup" {
          project_id  = "1372813089189561287"
          cluster_id  = "1379661944630234067"
          name        = "firstBackup"
          description = "create by terraform"
        }

    ファイル内のリソース値 (プロジェクト ID やクラスタ ID など) を独自のものに置き換える必要があります。

    Terraform を使用してクラスター リソース (たとえば、 `example_cluster` ) を管理している場合は、実際のプロジェクト ID とクラスター ID を指定せずに、次のようにバックアップ リソースを構成することもできます。

        resource "tidbcloud_backup" "example_backup" {
          project_id  = tidbcloud_cluster.example_cluster.project_id
          cluster_id  = tidbcloud_cluster.example_cluster.id
          name        = "firstBackup"
          description = "create by terraform"
        }

3.  `terraform apply`コマンドを実行します。

        $ terraform apply

        tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

        Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
          + create

        Terraform will perform the following actions:

          # tidbcloud_backup.example_backup will be created
          + resource "tidbcloud_backup" "example_backup" {
              + cluster_id       = "1379661944630234067"
              + create_timestamp = (known after apply)
              + description      = "create by terraform"
              + id               = (known after apply)
              + name             = "firstBackup"
              + project_id       = "1372813089189561287"
              + size             = (known after apply)
              + status           = (known after apply)
              + type             = (known after apply)
            }

        Plan: 1 to add, 0 to change, 0 to destroy.

        Do you want to perform these actions?
          Terraform will perform the actions described above.
          Only 'yes' will be accepted to approve.

          Enter a value:

4.  バックアップを作成するには`yes`と入力します。

    ```
      Enter a value: yes

    tidbcloud_backup.example_backup: Creating...
    tidbcloud_backup.example_backup: Creation complete after 2s [id=1350048]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

    ```

5.  `terraform state show tidbcloud_backup.${resource-name}`使用してバックアップのステータスを確認します。

        $ terraform state show tidbcloud_backup.example_backup

        # tidbcloud_backup.example_backup:
        resource "tidbcloud_backup" "example_backup" {
            cluster_id       = "1379661944630234067"
            create_timestamp = "2022-08-26T07:56:10Z"
            description      = "create by terraform"
            id               = "1350048"
            name             = "firstBackup"
            project_id       = "1372813089189561287"
            size             = "0"
            status           = "PENDING"
            type             = "MANUAL"
        }

6.  数分お待ちください。その後、 `terraform refersh`を使用してステータスを更新します。

        $ terraform refresh
        tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
        tidbcloud_backup.example_backup: Refreshing state... [id=1350048]
        $ terraform state show tidbcloud_backup.example_backup
        # tidbcloud_backup.example_backup:
        resource "tidbcloud_backup" "example_backup" {
            cluster_id       = "1379661944630234067"
            create_timestamp = "2022-08-26T07:56:10Z"
            description      = "create by terraform"
            id               = "1350048"
            name             = "firstBackup"
            project_id       = "1372813089189561287"
            size             = "198775"
            status           = "SUCCESS"
            type             = "MANUAL"
        }

ステータスが`SUCCESS`に変わると、クラスターのバックアップが作成されたことを示します。作成後はバックアップを更新できないことに注意してください。

これで、クラスターのバックアップが作成されました。このバックアップを使用してクラスターを復元する場合は、 [復元リソースを使用する](/tidb-cloud/terraform-use-restore-resource.md)実行できます。

## バックアップを更新する {#update-a-backup}

バックアップを更新できません。

## バックアップを削除する {#delete-a-backup}

バックアップを削除するには、対応する`backup.tf`ファイルが配置されているバックアップ ディレクトリに移動し、 `terraform destroy`コマンドを実行してバックアップ リソースを破棄します。

    $ terraform destroy

    Plan: 0 to add, 0 to change, 1 to destroy.

    Do you really want to destroy all resources?
    Terraform will destroy all your managed infrastructure, as shown above.
    There is no undo. Only 'yes' will be accepted to confirm.

    Enter a value: yes

ここで、コマンド`terraform show`実行すると、リソースがクリアされているため何も表示されません。

    $ terraform show
