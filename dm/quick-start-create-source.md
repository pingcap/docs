---
title: Create a Data Source for TiDB Data Migration
summary: Learn how to create a data source for Data Migration (DM).
---

# TiDB データ移行用のデータ ソースの作成 {#create-a-data-source-for-tidb-data-migration}

> **注記：**
>
> データ ソースを作成する前に、 [TiUPを使用した DMクラスタのデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)を行う必要があります。

このドキュメントでは、TiDB Data Migration (DM) のデータ移行タスク用のデータ ソースを作成する方法について説明します。

データ ソースには、上流の移行タスクにアクセスするための情報が含まれています。データ移行タスクでは、アクセスの構成情報を取得するために対応するデータ ソースを参照する必要があるため、データ移行タスクを作成する前にタスクのデータ ソースを作成する必要があります。特定のデータ ソース管理コマンドについては、 [データソース構成の管理](/dm/dm-manage-source.md)を参照してください。

## ステップ 1: データソースを構成する {#step-1-configure-the-data-source}

1.  (オプション) データソースのパスワードを暗号化します。

    DM 設定ファイルでは、dmctl で暗号化されたパスワードを使用することをお勧めします。以下の例に従って、データ ソースの暗号化されたパスワードを取得できます。このパスワードは、後で構成ファイルを書き込むために使用できます。

    ```bash
    tiup dmctl encrypt 'abc!@#123'
    ```

        MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=

2.  データソースの設定ファイルを書き込む

    データ ソースごとに、それを作成するための個別の構成ファイルが必要です。以下の例に従って、ID が「mysql-01」のデータ ソースを作成できます。まず構成ファイル`./source-mysql-01.yaml`を作成します。

    ```yaml
    source-id: "mysql-01"    # The ID of the data source, you can refer this source-id in the task configuration and dmctl command to associate the corresponding data source.

    from:
      host: "127.0.0.1"
      port: 3306
      user: "root"
      password: "MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=" # The user password of the upstream data source. It is recommended to use the password encrypted with dmctl.
      security:                                        # The TLS configuration of the upstream data source. If not necessary, it can be deleted.
        ssl-ca: "/path/to/ca.pem"
        ssl-cert: "/path/to/cert.pem"
        ssl-key: "/path/to/key.pem"
    ```

## ステップ 2: データソースを作成する {#step-2-create-a-data-source}

次のコマンドを使用してデータ ソースを作成できます。

```bash
tiup dmctl --master-addr <master-addr> operate-source create ./source-mysql-01.yaml
```

その他の設定パラメータについては、 [アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

返される結果は次のとおりです。

    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-01",
                "worker": "dm-worker-1"
            }
        ]
    }

## ステップ 3: 作成したデータ ソースをクエリする {#step-3-query-the-data-source-you-created}

データ ソースを作成した後、次のコマンドを使用してデータ ソースをクエリできます。

-   データ ソースの`source-id`わかっている場合は、 `dmctl config source <source-id>`コマンドを使用してデータ ソースの構成を直接確認できます。

    ```bash
    tiup dmctl --master-addr <master-addr> config source mysql-01
    ```

        {
          "result": true,
          "msg": "",
          "cfg": "enable-gtid: false
            flavor: mysql
            source-id: mysql-01
            from:
              host: 127.0.0.1
              port: 3306
              user: root
              password: '******'
        }

-   `source-id`がわからない場合は、 `dmctl operate-source show`コマンドを使用してソース データベースのリストを確認し、そこから対応するデータ ソースを見つけることができます。

    ```bash
    tiup dmctl --master-addr <master-addr> operate-source show
    ```

        {
            "result": true,
            "msg": "",
            "sources": [
                {
                    "result": true,
                    "msg": "source is added but there is no free worker to bound",
                    "source": "mysql-02",
                    "worker": ""
                },
                {
                    "result": true,
                    "msg": "",
                    "source": "mysql-01",
                    "worker": "dm-worker-1"
                }
            ]
        }
