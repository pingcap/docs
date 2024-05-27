---
title: Create a Data Source for TiDB Data Migration
summary: データ移行 (DM) のデータ ソースを作成する方法を学習します。
---

# TiDB データ移行用のデータ ソースを作成する {#create-a-data-source-for-tidb-data-migration}

> **注記：**
>
> データ ソースを作成する前に、 [TiUPを使用して DMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)実行する必要があります。

このドキュメントでは、TiDB データ移行 (DM) のデータ移行タスク用のデータ ソースを作成する方法について説明します。

データ ソースには、上流の移行タスクにアクセスするための情報が含まれています。データ移行タスクは、アクセスの構成情報を取得するために、対応するデータ ソースを参照する必要があるため、データ移行タスクを作成する前に、タスクのデータ ソースを作成する必要があります。具体的なデータ ソース管理コマンドについては、 [データソース構成の管理](/dm/dm-manage-source.md)を参照してください。

## ステップ1: データソースを構成する {#step-1-configure-the-data-source}

1.  (オプション) データソースのパスワードを暗号化する

    DM 構成ファイルでは、dmctl で暗号化されたパスワードを使用することをお勧めします。以下の例に従って、データ ソースの暗号化されたパスワードを取得し、後で構成ファイルを書き込むときに使用できます。

    v8.0.0 以降では、 `tiup dmctl encrypt`コマンドを使用する前に、DM-master に[`secret-key-path`](/dm/dm-master-configuration-file.md)設定する必要があります。

    ```bash
    tiup dmctl encrypt 'abc!@#123'
    ```

        MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=

2.  データソースの設定ファイルを書き込む

    データ ソースごとに、個別の構成ファイルを作成して作成する必要があります。以下の例に従って、ID が「mysql-01」のデータ ソースを作成します。まず、構成ファイル`./source-mysql-01.yaml`を作成します。

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

## ステップ2: データソースを作成する {#step-2-create-a-data-source}

次のコマンドを使用してデータ ソースを作成できます。

```bash
tiup dmctl --master-addr <master-addr> operate-source create ./source-mysql-01.yaml
```

その他の設定パラメータについては[アップストリームデータベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

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

## ステップ3: 作成したデータソースをクエリする {#step-3-query-the-data-source-you-created}

データ ソースを作成したら、次のコマンドを使用してデータ ソースをクエリできます。

-   データ ソースの`source-id`がわかっている場合は、 `dmctl config source <source-id>`コマンドを使用してデータ ソースの構成を直接確認できます。

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

-   `source-id`がわからない場合は、 `dmctl operate-source show`コマンドを使用してソース データベース リストを確認し、そこから対応するデータ ソースを見つけることができます。

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
