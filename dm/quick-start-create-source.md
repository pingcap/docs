---
title: Create a Data Source for TiDB Data Migration
summary: データ移行 (DM) のデータ ソースを作成する方法を学習します。
---

# TiDBデータ移行用のデータソースを作成する {#create-a-data-source-for-tidb-data-migration}

> **注記：**
>
> データ ソースを作成する前に、 [TiUPを使用して DMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)実行する必要があります。

このドキュメントでは、TiDB データ移行 (DM) のデータ移行タスク用のデータ ソースを作成する方法について説明します。

データソースには、上流の移行タスクにアクセスするための情報が含まれています。データ移行タスクは、アクセスの設定情報を取得するために、対応するデータソースを参照する必要があるため、データ移行タスクを作成する前に、タスクのデータソースを作成する必要があります。具体的なデータソース管理コマンドについては、 [データソース構成の管理](/dm/dm-manage-source.md)を参照してください。

## ステップ1: データソースを構成する {#step-1-configure-the-data-source}

1.  （オプション）データソースのパスワードを暗号化する

    DM設定ファイルでは、dmctlで暗号化されたパスワードを使用することをお勧めします。以下の例に従ってデータソースの暗号化されたパスワードを取得すれば、後で設定ファイルを書き込む際に使用できます。

    v8.0.0 以降では、 `tiup dmctl encrypt`コマンドを使用する前に、DM-master に[`secret-key-path`](/dm/dm-master-configuration-file.md)設定する必要があります。

    ```bash
    tiup dmctl encrypt 'abc!@#123'
    ```

        MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=

2.  データソースの設定ファイルを書き込む

    データソースごとに、個別の設定ファイルを作成する必要があります。以下の例に従って、IDが「mysql-01」のデータソースを作成します。まず、設定ファイル`./source-mysql-01.yaml`を作成します。

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

その他の設定パラメータについては[上流データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

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

-   `source-id`わからない場合は、 `dmctl operate-source show`コマンドを使用してソース データベース リストを確認し、そこから対応するデータ ソースを見つけることができます。

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
