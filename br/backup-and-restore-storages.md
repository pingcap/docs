---
title: External Storages
summary: Describes the storage URL format used in BR, TiDB Lightning, and Dumpling.
---

# 外部ストレージ {#external-storages}

Backup＆Restore（BR）、TiDB Lighting、およびDumplingは、ローカルファイルシステムとAmazonS3でのデータの読み取りと書き込みをサポートします。 BRは、Google Cloud Storage（GCS）および[Azure Blob Storage（Azblob）](/br/backup-and-restore-azblob.md)でのデータの読み取りと書き込みもサポートしています。これらは、BRに渡される`--storage`パラメーター、TiDB Lightningに渡される`-d`パラメーター、およびDumplingに渡される`--output` （ `-o` ）パラメーターのURLスキームによって区別されます。

## スキーム {#schemes}

次のサービスがサポートされています。

| サービス                      | スキーム      | URLの例                                    |
| ------------------------- | --------- | ---------------------------------------- |
| すべてのノードに分散されたローカルファイルシステム | ローカル      | `local:///path/to/dest/`                 |
| AmazonS3と互換性のあるサービス       | s3        | `s3://bucket-name/prefix/of/dest/`       |
| Google Cloud Storage（GCS） | gcs、gs    | `gcs://bucket-name/prefix/of/dest/`      |
| Azure Blob Storage        | 紺碧、azblob | `azure://container-name/prefix/of/dest/` |
| どこにも書きません（ベンチマークのみ）       | noop      | `noop://`                                |

## URLパラメータ {#url-parameters}

S3、GCS、Azblobなどのクラウドストレージでは、接続のために追加の構成が必要になる場合があります。このような構成のパラメーターを指定できます。例えば：

-   Dumplingを使用してデータをS3にエクスポートします。

    {{< copyable "" >}}

    ```bash
    ./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
        -o 's3://my-bucket/sql-backup?region=us-west-2'
    ```

-   TiDB Lightningを使用して、S3からデータをインポートします。

    {{< copyable "" >}}

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?region=us-west-2'
    ```

-   TiDB Lightningを使用してS3からデータをインポートします（リクエストモードでパススタイルを使用）：

    {{< copyable "" >}}

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

-   BRを使用してデータをGCSにバックアップします。

    {{< copyable "" >}}

    ```bash
    ./br backup full -u 127.0.0.1:2379 \
        -s 'gcs://bucket-name/prefix'
    ```

-   BRを使用してデータをAzblobにバックアップします。

    {{< copyable "" >}}

    ```bash
    ./br backup full -u 127.0.0.1:2379 \
        -s 'azure://container-name/prefix'
    ```

### S3URLパラメータ {#s3-url-parameters}

| URLパラメータ                  | 説明                                                         |
| :------------------------ | :--------------------------------------------------------- |
| `access-key`              | アクセスキー                                                     |
| `secret-access-key`       | 秘密のアクセスキー                                                  |
| `region`                  | Amazon S3のサービスリージョン（デフォルトは`us-east-1` ）                    |
| `use-accelerate-endpoint` | Amazon S3でアクセラレーションエンドポイントを使用するかどうか（デフォルトは`false` ）        |
| `endpoint`                | S3互換サービスのカスタムエンドポイントのURL（たとえば、 `https://s3.example.com/` ） |
| `force-path-style`        | 仮想ホストスタイルアクセスではなく、パススタイルアクセスを使用します（デフォルトは`false` ）         |
| `storage-class`           | アップロードされたオブジェクトのストレージクラス（ `STANDARD_IA` `STANDARD`         |
| `sse`                     | アップロードの暗号化に使用されるサーバー側の暗号化アルゴリズム（空、 `AES256`または`aws:kms` ）  |
| `sse-kms-key-id`          | `sse`が`aws:kms`に設定されている場合、KMSIDを指定します                      |
| `acl`                     | アップロードされたオブジェクトの`authenticated-read` `private`             |

> **ノート：**
>
> アクセスキーとシークレットアクセスキーはプレーンテキストで記録されるため、ストレージURLに直接渡すことはお勧めしません。移行ツールは、次の順序で環境からこれらのキーを推測しようとします。

1.  `$AWS_ACCESS_KEY_ID`および`$AWS_SECRET_ACCESS_KEY`の環境変数
2.  `$AWS_ACCESS_KEY`および`$AWS_SECRET_KEY`の環境変数
3.  `$AWS_SHARED_CREDENTIALS_FILE`環境変数で指定されたパスにあるツールノードの共有クレデンシャルファイル
4.  `~/.aws/credentials`のツールノードにある共有クレデンシャルファイル
5.  AmazonEC2コンテナの現在のIAMの役割
6.  AmazonECSタスクの現在のIAMの役割

### GCSURLパラメータ {#gcs-url-parameters}

| URLパラメータ           | 説明                                                 |
| :----------------- | :------------------------------------------------- |
| `credentials-file` | ツールノードのクレデンシャルJSONファイルへのパス                         |
| `storage-class`    | アップロードされたオブジェクトのストレージクラス（ `COLDLINE` `STANDARD`    |
| `predefined-acl`   | アップロードされたオブジェクトの事前定義された`project-private` `private` |

`credentials-file`が指定されていない場合、移行ツールは次の順序で環境から資格情報を推測しようとします。

1.  `$GOOGLE_APPLICATION_CREDENTIALS`環境変数で指定されたパスにあるツールノード上のファイルの内容
2.  `~/.config/gcloud/application_default_credentials.json`のツールノード上のファイルの内容
3.  GCEまたはGAEで実行している場合、メタデータサーバーから取得した資格情報。

### AzblobURLパラメーター {#azblob-url-parameters}

| URLパラメータ       | 説明                                                                                            |
| :------------- | :-------------------------------------------------------------------------------------------- |
| `account-name` | ストレージのアカウント名                                                                                  |
| `account-key`  | アクセスキー                                                                                        |
| `access-tier`  | アップロードされたオブジェクトの`Archive`層（ `Cool` 、 `Hot` ）。 `access-tier`が設定されていない（値が空の）場合、値はデフォルトで`Hot`です。 |

TiKVとBRが同じストレージアカウントを使用することを保証するために、BRは`account-name`の値を決定します。つまり、デフォルトでは`send-credentials-to-tikv = true`が設定されています。 BRは、次の順序で環境からこれらのキーを推測します。

1.  `account-name`**と**`account-key`の両方が指定されている場合、このパラメーターで指定されたキーが使用されます。
2.  `account-key`が指定されていない場合、BRはBRのノード上の環境変数から関連する資格情報を読み取ろうとします。
    -   BRは、最初に`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`を読み取り`$AZURE_CLIENT_SECRET` 。同時に、BRを使用すると、TiKVは上記の3つの環境変数をそれぞれのノードから読み取り、Azure AD（Azure Active Directory）を使用してアクセスできます。
        -   `$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`は、 `$AZURE_CLIENT_SECRET` AzureアプリケーションのアプリケーションID `client_id` 、テナントID `tenant_id` 、およびクライアントパスワード`client_secret`を参照します。
        -   オペレーティングシステムが`$AZURE_CLIENT_ID` 、および`$AZURE_TENANT_ID`を構成しているかどうかを確認する方法、またはこれらの変数をパラメーターとして構成する必要がある場合は、 `$AZURE_CLIENT_SECRET`を参照して[環境変数をパラメーターとして構成する](/br/backup-and-restore-azblob.md#configure-environment-variables-as-parameters) 。
3.  上記の3つの環境変数がBRノードで構成されていない場合、BRはアクセスキーを使用して`$AZURE_STORAGE_KEY`を読み取ろうとします。

> **ノート：**
>
> Azure Blob Storageを外部ストレージとして使用する場合は、 `send-credentials-to-tikv = true` （デフォルトで設定）を設定する必要があります。そうしないと、バックアップタスクが失敗します。

## コマンドラインパラメータ {#command-line-parameters}

URLパラメーターに加えて、BRとDumplingは、コマンドラインパラメーターを使用したこれらの構成の指定もサポートしています。例えば：

{{< copyable "" >}}

```bash
./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
    -o 's3://my-bucket/sql-backup' \
    --s3.region 'us-west-2'
```

URLパラメーターとコマンドラインパラメーターを同時に指定した場合、URLパラメーターはコマンドラインパラメーターによって上書きされます。

### S3コマンドラインパラメータ {#s3-command-line-parameters}

| コマンドラインパラメータ          | 説明                                                                   |
| :-------------------- | :------------------------------------------------------------------- |
| `--s3.region`         | AmazonS3のサービスリージョン。デフォルトは`us-east-1`です。                              |
| `--s3.endpoint`       | S3互換サービスのカスタムエンドポイントのURL。たとえば、 `https://s3.example.com/` 。           |
| `--s3.storage-class`  | アップロードオブジェクトのストレージクラス。たとえば、 `STANDARD`と`STANDARD_IA` 。               |
| `--s3.sse`            | アップロードの暗号化に使用されるサーバー側の暗号化アルゴリズム。値のオプションは空で、 `AES256`と`aws:kms`です。    |
| `--s3.sse-kms-key-id` | `--s3.sse`が`aws:kms`として設定されている場合、このパラメータはKMSIDを指定するために使用されます。        |
| `--s3.acl`            | アップロードオブジェクトの固定ACL。たとえば、 `private`と`authenticated-read` 。            |
| `--s3.provider`       | S3互換サービスのタイプ。サポートされている`other`は、 `aws` 、 `netease` `ceph` `alibaba` 。 |

AWS S3以外のクラウドストレージにデータをエクスポートするには、クラウドプロバイダーと`virtual-hosted style`を使用するかどうかを指定します。次の例では、データがAlibabaCloudOSSストレージにエクスポートされます。

-   Dumplingを使用してAlibabaCloudOSSにデータをエクスポートします：

    {{< copyable "" >}}

    ```bash
    ./dumpling -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
       -o "s3://my-bucket/dumpling/" \
       --s3.endpoint="http://oss-cn-hangzhou-internal.aliyuncs.com" \
       --s3.provider="alibaba" \
       -r 200000 -F 256MiB
    ```

-   BRを使用してAlibabaCloudOSSにデータをバックアップします。

    {{< copyable "" >}}

    ```bash
    ./br backup full --pd "127.0.0.1:2379" \
        --storage "s3://my-bucket/full/" \
        --s3.endpoint="http://oss-cn-hangzhou-internal.aliyuncs.com" \
        --s3.provider="alibaba" \
        --send-credentials-to-tikv=true \
        --ratelimit 128 \
        --log-file backuptable.log
    ```

-   TiDBLightningを使用してAlibabaCloudOSSにデータをエクスポートします。 YAML形式の構成ファイルで次のコンテンツを指定する必要があります。

    {{< copyable "" >}}

    ```
    [mydumper]
    data-source-dir = "s3://my-bucket/dumpling/?endpoint=http://oss-cn-hangzhou-internal.aliyuncs.com&provider=alibaba"
    ```

### GCSコマンドラインパラメータ {#gcs-command-line-parameters}

| コマンドラインパラメータ             | 説明                                                     |
| :----------------------- | :----------------------------------------------------- |
| `--gcs.credentials-file` | ツールノード上のJSON形式のクレデンシャルのパス。                             |
| `--gcs.storage-class`    | `STANDARD`や`COLDLINE`などのアップロードオブジェクトのストレージタイプ。         |
| `--gcs.predefined-acl`   | `private`や`project-private`などのアップロードオブジェクトの事前定義されたACL。 |

### Azblobコマンドラインパラメーター {#azblob-command-line-parameters}

|コマンドラインパラメータ|説明| | `--azblob.account-name` |ストレージのアカウント名| | `--azblob.account-key` |アクセスキー| | `--azblob.access-tier` |アップロードされたオブジェクトの`Archive` `Cool` `Hot` `access-tier`が設定されていない（値が空の）場合、値はデフォルトで`Hot`です。 |

## BRがTiKVにクレデンシャルを送信 {#br-sending-credentials-to-tikv}

デフォルトでは、S3、GCS、またはAzblob宛先を使用する場合、BRはセットアップの複雑さを軽減するためにすべてのTiKVノードにクレデンシャルを送信します。

ただし、これは、すべてのノードが独自の役割と権限を持っているクラウド環境には適していません。このような場合、 `--send-credentials-to-tikv=false` （または短縮形`-c=0` ）で送信するクレデンシャルを無効にする必要があります。

{{< copyable "" >}}

```bash
./br backup full -c=0 -u pd-service:2379 -s 's3://bucket-name/prefix'
```

[バックアップ](/sql-statements/sql-statement-backup.md)および[戻す](/sql-statements/sql-statement-restore.md)データにSQLステートメントを使用する場合、 `SEND_CREDENTIALS_TO_TIKV = FALSE`のオプションを追加できます。

{{< copyable "" >}}

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

2つのアプリケーションは現在スタンドアロンであるため、このオプションはTiDBLightningおよびDumplingではサポートされていません。
