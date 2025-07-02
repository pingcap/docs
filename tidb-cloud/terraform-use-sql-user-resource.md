---
title: Use SQL User Resource
summary: SQL ユーザー リソースを使用してTiDB Cloud SQL ユーザーを作成および変更する方法を学習します。
---

# SQL ユーザー リソースを使用する {#use-sql-user-resource}

このドキュメントでは、 `tidbcloud_sql_user`リソースを使用してTiDB Cloud SQL ユーザーを管理する方法について説明します。

`tidbcloud_sql_user`リソースの機能は次のとおりです。

-   TiDB Cloud SQL ユーザーを作成します。
-   TiDB Cloud SQL ユーザーを変更します。
-   TiDB Cloud SQL ユーザーをインポートします。
-   TiDB Cloud SQL ユーザーを削除します。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0以降。
-   [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)または[TiDB Cloudサーバーレスクラスター](/tidb-cloud/create-tidb-cluster-serverless.md) 。

## SQLユーザーを作成する {#create-a-sql-user}

`tidbcloud_sql_user`リソースを使用して SQL ユーザーを作成できます。

次の例は、TiDB Cloud SQL ユーザーを作成する方法を示しています。

1.  SQL ユーザーのディレクトリを作成してそこに入ります。

2.  `sql_user.tf`ファイルを作成します。

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

        resource "tidbcloud_sql_user" "example" {
          cluster_id   = "your_cluster_id"
          user_name    = "example_user"
          password     = "example_password"
          builtin_role = "role_admin"
        }

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細など、 TiDB Cloudのリソースを定義します。

    -   SQL ユーザー リソースを使用するには、リソース タイプを`tidbcloud_sql_user`に設定します。
    -   リソース名は必要に応じて定義できます。例： `example` 。
    -   TiDB Cloud Serverless クラスター内の SQL ユーザーの場合、 `user_name`と組み込みロール`role_readonly`および`role_readwrite`ユーザー プレフィックスで始まる必要があり、 `tidbcloud_serverless_cluster`データ ソースを実行することでユーザー プレフィックスを取得できます。
    -   SQL ユーザー指定情報を取得するには、 [`tidbcloud_sql_user` (リソース)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/sql_user)参照してください。

3.  `terraform apply`コマンドを実行します。リソースを適用する場合は`terraform apply --auto-approve`の使用は推奨されません。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # tidbcloud_sql_user.example will be created
      + resource "tidbcloud_sql_user" "example" {
          + auth_method  = (known after apply)
          + builtin_role = "role_admin"
          + cluster_id   = "10423692645600000000"
          + password     = (sensitive value)
          + user_name    = "example_user"
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

    上記の結果では、Terraform によって実行プランが生成され、Terraform が実行するアクションが記述されます。

    -   構成と状態の違いを確認できます。
    -   `apply`の結果も確認できます。新しいリソースが追加されますが、リソースは変更または破棄されません。
    -   `known after apply` `apply`後の対応する値が取得されることを示します。

4.  計画の内容がすべて問題ない場合は、「 `yes`と入力して続行します。

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_sql_user.example: Creating...
    tidbcloud_sql_user.example: Creation complete after 2s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5.  リソースの状態を確認するには、コマンド`terraform show`または`terraform state show tidbcloud_sql_user.${resource-name}`使用します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

    ```shell
    $ terraform state show tidbcloud_sql_user.example                 
      # tidbcloud_sql_user.example:
      resource "tidbcloud_sql_user" "example" {
          builtin_role = "role_admin"
          cluster_id   = "10423692645600000000"
          password     = (sensitive value)
          user_name    = "example_user"
      }
    ```

## SQL ユーザーのパスワードまたはユーザー ロールを変更する {#change-the-password-or-user-roles-of-a-sql-user}

次のように、Terraform を使用して SQL ユーザーのパスワードまたはユーザー ロールを変更できます。

1.  [SQLユーザーを作成する](#create-a-sql-user)実行するときに使用する`sql_user.tf`ファイルで、 `password` 、 `builtin_role` 、および`custom_roles` (該当する場合) を変更します。

    例えば：

        resource "tidbcloud_sql_user" "example" {
          cluster_id = 10423692645600000000
          user_name = "example_user"
          password = "updated_example_password"
          builtin_role = "role_readonly"
        }

2.  `terraform apply`コマンドを実行します。

    ```shell
    $ terraform apply

    tidbcloud_sql_user.example: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_sql_user.example will be updated in-place
      ~ resource "tidbcloud_sql_user" "example" {
          + auth_method  = (known after apply)
          ~ builtin_role = "role_admin" -> "role_readonly"
          ~ password     = (sensitive value)
            # (2 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    ```

    上記の実行プランでは、パスワードと組み込みロールが変更されます。

3.  計画の内容がすべて問題ない場合は、「 `yes`と入力して続行します。

    ```shell
      Enter a value: yes

    tidbcloud_sql_user.example: Modifying...
    tidbcloud_sql_user.example: Modifications complete after 2s

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4.  `terraform state show tidbcloud_sql_user.${resource-name}`使用して状態を確認します。

        $ terraform state show tidbcloud_sql_user.example
        # tidbcloud_sql_user.example:
        resource "tidbcloud_sql_user" "example" {
            builtin_role = "role_readonly"
            cluster_id   = "10423692645600000000"
            password     = (sensitive value)
            user_name    = "example_user"
        }

`builtin_role` `role_readonly`に変更されます。5 `password`センシティブな値であるため表示されません。

## SQLユーザーをインポートする {#import-a-sql-user}

Terraform で管理されていないTiDB Cloud SQL ユーザーの場合は、Terraform を使用してインポートすることで管理できます。

たとえば、Terraform によって作成されていない SQL ユーザーを次のようにインポートできます。

1.  新しいSQLユーザーリソースのインポートブロックを追加する

    次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}` `cluster_id,user_name`の形式に置き換えます。

        import {
          to = tidbcloud_sql_user.example
          id = "${id}"
        }

2.  新しい設定ファイルを生成する

    インポート ブロックに従って、新しい SQL ユーザー リソースの新しい構成ファイルを生成します。

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

    その後、カレントディレクトリに`generated.tf`ファイルが作成され、そこにインポートされたリソースの設定が含まれます。ただし、必須の引数`password`設定されていないため、プロバイダーはエラーをスローします。生成された設定ファイルで、引数`password`の値を`tidbcloud_sql_user`リソースに置き換えることができます。

3.  生成された構成を確認して適用する

    生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

    次に、 `terraform apply`実行してインフラストラクチャをインポートします。適用後の出力例は次のとおりです。

    ```shell
    tidbcloud_sql_user.example: Importing... [id=10423692645600000000,example_user]
    tidbcloud_sql_user.example: Import complete [id=10423692645600000000,example_user]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

これで、インポートした SQL ユーザーを Terraform で管理できるようになりました。

## SQLユーザーを削除する {#delete-a-sql-user}

SQL ユーザーを削除するには、 `tidbcloud_sql_user`リソースの構成を削除し、 `terraform apply`コマンドを使用してリソースを破棄します。

```shell
  $ terraform apply
  tidbcloud_sql_user.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy

  Terraform will perform the following actions:

    # tidbcloud_sql_user.example will be destroyed
    # (because tidbcloud_sql_user.example is not in configuration)
    - resource "tidbcloud_sql_user" "example" {
        - builtin_role = "role_readonly" -> null
        - cluster_id   = "10423692645600000000" -> null
        - password     = (sensitive value) -> null
        - user_name    = "example_user" -> null
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.

    Enter a value: yes

  tidbcloud_sql_user.example: Destroying...
  tidbcloud_sql_user.example: Destruction complete after 3s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

ここで、コマンド`terraform show`実行すると、リソースがクリアされているため何も表示されません。

    $ terraform show
