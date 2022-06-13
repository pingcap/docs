---
title: Create a Data Source
summary: Learn how to create a data source for Data Migration (DM).
---

# データソースを作成する {#create-a-data-source}

> **ノート：**
>
> データソースを作成する前に、 [TiUPを使用してDMクラスターをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md)を行う必要があります。

このドキュメントでは、TiDBデータ移行（DM）のデータ移行タスク用のデータソースを作成する方法について説明します。

データソースには、アップストリーム移行タスクにアクセスするための情報が含まれています。データ移行タスクでは、アクセスの構成情報を取得するために対応するデータソースを参照する必要があるため、データ移行タスクを作成する前に、タスクのデータソースを作成する必要があります。特定のデータソース管理コマンドについては、 [データソース構成の管理](/dm/dm-manage-source.md)を参照してください。

## ステップ1：データソースを構成する {#step-1-configure-the-data-source}

1.  （オプション）データソースのパスワードを暗号化する

    DM構成ファイルでは、dmctlで暗号化されたパスワードを使用することをお勧めします。以下の例に従って、データソースの暗号化されたパスワードを取得できます。このパスワードは、後で構成ファイルを書き込むために使用できます。

    {{< copyable "" >}}

    ```bash
    tiup dmctl encrypt 'abc!@#123'
    ```

    ```
    MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=
    ```

2.  データソースの構成ファイルを書き込みます

    データソースごとに、それを作成するための個別の構成ファイルが必要です。以下の例に従って、IDが「mysql-01」であるデータソースを作成できます。最初に構成ファイルを作成します`./source-mysql-01.yaml` ：

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

## ステップ2：データソースを作成する {#step-2-create-a-data-source}

次のコマンドを使用して、データソースを作成できます。

{{< copyable "" >}}

```bash
tiup dmctl --master-addr <master-addr> operate-source create ./source-mysql-01.yaml
```

その他の構成パラメーターについては、 [アップストリームデータベースConfiguration / コンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

返される結果は次のとおりです。

{{< copyable "" >}}

```
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
```

## ステップ3：作成したデータソースをクエリする {#step-3-query-the-data-source-you-created}

データソースを作成したら、次のコマンドを使用してデータソースをクエリできます。

-   データソースの`source-id`を知っている場合は、 `dmctl config source <source-id>`コマンドを使用して、データソースの構成を直接確認できます。

    {{< copyable "" >}}

    ```bash
    tiup dmctl --master-addr <master-addr> config source mysql-01
    ```

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
    ```

-   `source-id`がわからない場合は、 `dmctl operate-source show`コマンドを使用して、対応するデータソースを見つけることができるソースデータベースリストを確認できます。

    {{< copyable "" >}}

    ```bash
    tiup dmctl --master-addr <master-addr> operate-source show
    ```

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
    ```
