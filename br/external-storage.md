---
title: External Storages
summary: Describes the storage URL format used in BR, TiDB Lightning, and Dumpling.
---

<!--This doc is temporarily removed from TOC because it duplicates with backup-and-restore-storages.md but some descriptions about Lightning and Dumpling should be remained for successful references. Will extract Lightning and Dumpling content and add it to Lightning and Dumpling docs when bandwidth is sufficient.-->

# 外部ストレージ {#external-storages}

br コマンドライン ツール、 TiDB Lightning、およびDumplingは、ローカル ファイル システムと Amazon S3 でのデータの読み取りと書き込みをサポートします。 br コマンドライン ツールは、Google Cloud Storage (GCS) と Azure Blob Storage (Azblob) でのデータの読み取りと書き込みもサポートしています。これらは、 br コマンドライン ツールに渡される`--storage` ( `-s` ) パラメータ、 TiDB Lightningに渡される`-d`パラメータ、およびDumplingに渡される`--output` ( `-o` ) パラメータの URL スキームによって区別されます。

## スキーム {#schemes}

次のサービスがサポートされています。

| サービス                        | 図式       | URL の例                                   |
| --------------------------- | -------- | ---------------------------------------- |
| すべてのノードに分散されたローカル ファイル システム | ローカル     | `local:///path/to/dest/`                 |
| Amazon S3 と互換性のあるサービス       | s3       | `s3://bucket-name/prefix/of/dest/`       |
| Google クラウド ストレージ (GCS)     | gcs、gs   | `gcs://bucket-name/prefix/of/dest/`      |
| Azure ブロブ ストレージ             | 紺碧、アズブロブ | `azure://container-name/prefix/of/dest/` |
| どこにも書き込みません (ベンチマーク専用)      | ヌープ      | `noop://`                                |

## URL パラメータ {#url-parameters}

S3、GCS、Azblob などのクラウド ストレージでは、接続のために追加の構成が必要になる場合があります。このような構成のパラメーターを指定できます。例えば：

-   Dumplingを使用してデータを S3 にエクスポートします。

    ```bash
    ./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
        -o 's3://my-bucket/sql-backup'
    ```

-   TiDB Lightningを使用して S3 からデータをインポートします。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'
    ```

-   TiDB Lightningを使用して S3 からデータをインポートします (パス スタイルのリクエストを使用)。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

-   TiDB Lightningを使用して S3 からデータをインポートします (特定のIAMロールを使用して S3 データにアクセスします)。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

-   br コマンドライン ツールを使用して、データを GCS にバックアップします。

    ```bash
    ./br backup full -u 127.0.0.1:2379 \
        -s 'gcs://bucket-name/prefix'
    ```

-   br コマンドライン ツールを使用して、データを Azblob にバックアップします。

    ```bash
    ./br backup full -u 127.0.0.1:2379 \
        -s 'azure://container-name/prefix'
    ```

### S3 URL パラメータ {#s3-url-parameters}

| URL パラメータ                 | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `access-key`              | アクセスキー                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `secret-access-key`       | シークレット アクセス キー                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `use-accelerate-endpoint` | Amazon S3 で加速エンドポイントを使用するかどうか (デフォルトは`false` )                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `endpoint`                | S3 互換サービスのカスタム エンドポイントの URL (例: `https://s3.example.com/` )                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `force-path-style`        | 仮想ホスト スタイルのリクエストではなく、パス スタイルのリクエストを使用します (デフォルトは`true` )。                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `storage-class`           | アップロードされたオブジェクトのストレージ クラス (例: `STANDARD` 、 `STANDARD_IA` )                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `sse`                     | アップロードの暗号化に使用されるサーバー側の暗号化アルゴリズム (空、 `AES256`または`aws:kms` )                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `sse-kms-key-id`          | `sse`が`aws:kms`に設定されている場合、KMS ID を指定します                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `acl`                     | アップロードされたオブジェクトの既定の ACL (例: `private` 、 `authenticated-read` )                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `role-arn`                | 指定された[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)を使用してサードパーティから Amazon S3 データにアクセスする必要がある場合、 `arn:aws:iam::888888888888:role/my-role`などの`role-arn`パラメータを使用してIAMロールの対応する[Amazon リソースネーム (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)を指定できます。詳細については、 [サードパーティが所有する AWS アカウントへのアクセスを提供する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)を参照してください。                        |
| `external-id`             | サードパーティから Amazon S3 データにアクセスする場合、正しい[外部 ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html)を指定して[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)を想定する必要がある場合があります。この場合、この`external-id`の URL クエリ パラメータを使用して、外部 ID を指定できます。外部 ID は、Amazon S3 データにアクセスするためにIAMロール ARN とともにサードパーティによって提供される任意の文字列です。 IAMロールを引き受ける際の外部 ID の提供はオプションです。つまり、サードパーティがIAMロールの外部 ID を指定していない場合、ロールを引き受けて、このパラメーターを提供しなくても対応する S3 データにアクセスできます。 |

> **ノート：**
>
> アクセス キーとシークレット アクセス キーをストレージ URL に直接渡すことはお勧めしません。これらのキーはプレーン テキストとして格納されるためです。

アクセスキーとシークレットアクセスキー、またはIAMロール ARN ( `role-arn` ) と外部 ID ( `external-id` ) のいずれも提供されていない場合、移行ツールは次の順序で環境からこれらのキーを検索します。

1.  `$AWS_ACCESS_KEY_ID`および`$AWS_SECRET_ACCESS_KEY`の環境変数
2.  `$AWS_ACCESS_KEY`および`$AWS_SECRET_KEY`の環境変数
3.  `$AWS_SHARED_CREDENTIALS_FILE`環境変数で指定されたパスにあるツール ノード上の共有資格情報ファイル
4.  `~/.aws/credentials`のツール ノード上の共有資格情報ファイル
5.  Amazon EC2 コンテナの現在のIAMロール
6.  Amazon ECS タスクの現在のIAMロール

### GCS URL パラメータ {#gcs-url-parameters}

| URL パラメータ          | 説明                                                           |
| :----------------- | :----------------------------------------------------------- |
| `credentials-file` | ツール ノードの資格情報 JSON ファイルへのパス                                   |
| `storage-class`    | アップロードされたオブジェクトのストレージ クラス (例: `STANDARD` 、 `COLDLINE` )      |
| `predefined-acl`   | アップロードされたオブジェクトの定義済み ACL (例: `private` 、 `project-private` ) |

`credentials-file`が指定されていない場合、移行ツールは次の順序で環境から資格情報を検索します。

1.  `$GOOGLE_APPLICATION_CREDENTIALS`環境変数で指定されたパスにあるツール ノード上のファイルの内容
2.  `~/.config/gcloud/application_default_credentials.json`のツール ノード上のファイルの内容
3.  GCE または GAE で実行している場合、資格情報はメタデータサーバーから取得されます。

### Azblob URL パラメーター {#azblob-url-parameters}

| URL パラメータ      | 説明                                                                                                          |
| :------------- | :---------------------------------------------------------------------------------------------------------- |
| `account-name` | ストレージのアカウント名                                                                                                |
| `account-key`  | アクセスキー                                                                                                      |
| `access-tier`  | アップロードされたオブジェクトのアクセス層 (例: `Hot` 、 `Cool` 、 `Archive` )。 `access-tier`が設定されていない (値が空である) 場合、デフォルトの値は`Hot`です。 |

TiKV と br が同じストレージ アカウントを使用するようにするために、 br は`account-name`の値を決定します。つまり、デフォルトで`send-credentials-to-tikv = true`が設定されています。 br は、次の順序で環境からこれらのキーを検索します。

1.  `account-name`**と**`account-key`の両方を指定すると、このパラメーターで指定されたキーが使用されます。
2.  `account-key`が指定されていない場合、br は br ノードの環境変数から関連する資格情報を読み取ろうとします。 br は、最初に`$AZURE_CLIENT_ID` 、 `$AZURE_TENANT_ID` 、および`$AZURE_CLIENT_SECRET`を読み取ります。同時に、br により、TiKV はこれら 3 つの環境変数をそれぞれのノードから読み取り、Azure AD (Azure Active Directory) を使用して変数にアクセスできるようになります。
3.  上記の 3 つの環境変数が br ノードで構成されていない場合、br はアクセス キーを使用して`$AZURE_STORAGE_KEY`を読み取ろうとします。

> **ノート：**
>
> -   Azure Blob Storage を外部ストレージとして使用する場合は、 `send-credentials-to-tikv = true`を設定する必要があります (既定で設定されています)。そうしないと、バックアップ タスクが失敗します。
> -   `$AZURE_CLIENT_ID`は、 `$AZURE_CLIENT_SECRET` Azure アプリケーションのアプリケーション ID `$AZURE_TENANT_ID` 、テナント ID `client_id` 、クライアント パスワード`tenant_id`を示し`client_secret` 。 3 つの環境変数の存在を確認する方法、または環境変数をパラメータとして設定する方法については、 [認証](/br/backup-and-restore-storages.md#authentication)を参照してください。

## コマンドライン パラメータ {#command-line-parameters}

URL パラメーターに加えて、br とDumplingは、コマンドライン パラメーターを使用したこれらの構成の指定もサポートしています。例えば：

{{< copyable "" >}}

```bash
./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
    -o 's3://my-bucket/sql-backup' \
    --s3.role-arn="arn:aws:iam::888888888888:role/my-role"
```

上記のコマンドは、次のコマンドと同等です。

```bash
./dumpling -u root -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
     -o 's3://my-bucket/sql-backup&role-arn=arn:aws:iam::888888888888:role/my-role'
```

URL パラメーターとコマンド ライン パラメーターを同時に指定した場合、URL パラメーターはコマンド ライン パラメーターによって上書きされます。

### S3 コマンドライン パラメータ {#s3-command-line-parameters}

| コマンドライン パラメータ         | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--s3.endpoint`       | S3 互換サービスのカスタム エンドポイントの URL (例: `https://s3.example.com/` )                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `--s3.storage-class`  | アップロード オブジェクトのストレージ クラス (例: `STANDARD`または`STANDARD_IA` )                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `--s3.sse`            | アップロードの暗号化に使用されるサーバー側の暗号化アルゴリズム (値のオプションは空、 `AES256`および`aws:kms` )                                                                                                                                                                                                                                                                                                                                                                                                                |
| `--s3.sse-kms-key-id` | `--s3.sse`が`aws:kms`として構成されている場合、このパラメーターを使用して KMS ID を指定します。                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `--s3.acl`            | アップロード オブジェクトの既定の ACL (例: `private`または`authenticated-read` )                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `--s3.provider`       | S3 互換サービスのタイプ (サポートされているタイプは`aws` 、 `alibaba` 、 `ceph` 、 `netease` 、および`other`です)                                                                                                                                                                                                                                                                                                                                                                                                 |
| `--s3.role-arn`       | 指定された[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)を使用してサードパーティから Amazon S3 データにアクセスする必要がある場合は、対応する[Amazon リソースネーム (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)のIAMロールを`--s3.role-arn`オプション ( `arn:aws:iam::888888888888:role/my-role`など) で指定できます。詳細については、 [AWS ドキュメント](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)を参照してください。                                    |
| `--s3.external-id`    | サードパーティから Amazon S3 データにアクセスする場合、正しい[外部 ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html)を指定して[IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)を想定する必要がある場合があります。この場合、この`--s3.external-id`オプションを使用して外部 ID を指定できます。外部 ID は、Amazon S3 データにアクセスするためにIAMロール ARN とともにサードパーティによって提供される任意の文字列です。 IAMロールを引き受ける際の外部 ID の提供はオプションです。つまり、サードパーティがIAMロールの外部 ID を指定していない場合、ロールを引き受けて、このパラメーターを提供しなくても対応する S3 データにアクセスできます。 |

非 AWS S3 クラウド ストレージにデータをエクスポートするには、クラウド プロバイダーと使用するかどうかを指定します`virtual-hosted style` 。次の例では、データは Alibaba Cloud OSS ストレージにエクスポートされます。

-   Dumplingを使用して Alibaba Cloud OSS にデータをエクスポートします。

    {{< copyable "" >}}

    ```bash
    ./dumpling -h 127.0.0.1 -P 3306 -B mydb -F 256MiB \
       -o "s3://my-bucket/dumpling/" \
       --s3.endpoint="http://oss-cn-hangzhou-internal.aliyuncs.com" \
       --s3.provider="alibaba" \
       -r 200000 -F 256MiB
    ```

-   br コマンドライン ツールを使用して、Alibaba Cloud OSS にデータをバックアップします。

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

-   TiDB Lightningを使用して Alibaba Cloud OSS にデータをエクスポートします。 YAML 構成ファイルで次の内容を指定する必要があります。

    {{< copyable "" >}}

    ```
    [mydumper]
    data-source-dir = "s3://my-bucket/dumpling/?endpoint=http://oss-cn-hangzhou-internal.aliyuncs.com&provider=alibaba"
    ```

### GCS コマンドライン パラメータ {#gcs-command-line-parameters}

| コマンドライン パラメータ            | 説明                                                           |
| :----------------------- | :----------------------------------------------------------- |
| `--gcs.credentials-file` | ツール ノードの資格情報 JSON ファイルへのパス                                   |
| `--gcs.storage-class`    | アップロード オブジェクトのストレージ クラス (例: `STANDARD`または`COLDLINE` )        |
| `--gcs.predefined-acl`   | アップロードされたオブジェクトの定義済み ACL (例: `private`または`project-private` ) |

### Azblob コマンド ライン パラメーター {#azblob-command-line-parameters}

| コマンドライン パラメータ           | 説明                                                                                                          |
| :---------------------- | :---------------------------------------------------------------------------------------------------------- |
| `--azblob.account-name` | ストレージのアカウント名                                                                                                |
| `--azblob.account-key`  | アクセスキー                                                                                                      |
| `--azblob.access-tier`  | アップロードされたオブジェクトのアクセス層 (例: `Hot` 、 `Cool` 、 `Archive` )。 `access-tier`が設定されていない (値が空である) 場合、デフォルトの値は`Hot`です。 |

## TiKV に資格情報を送信する br コマンドライン ツール {#br-command-line-tool-sending-credentials-to-tikv}

デフォルトでは、S3、GCS、または Azblob の宛先を使用する場合、br コマンドライン ツールはすべての TiKV ノードに資格情報を送信して、セットアップの複雑さを軽減します。

ただし、これは、すべてのノードが独自の役割と権限を持つクラウド環境には適していません。このような場合、 `--send-credentials-to-tikv=false` (または短い形式の`-c=0` ) を使用して資格情報の送信を無効にする必要があります。

{{< copyable "" >}}

```bash
./br backup full -c=0 -u pd-service:2379 -s 's3://bucket-name/prefix'
```

[バックアップする](/sql-statements/sql-statement-backup.md)と[戻す](/sql-statements/sql-statement-restore.md)のデータに SQL ステートメントを使用する場合、 `SEND_CREDENTIALS_TO_TIKV = FALSE`オプションを追加できます。

{{< copyable "" >}}

```sql
BACKUP DATABASE * TO 's3://bucket-name/prefix' SEND_CREDENTIALS_TO_TIKV = FALSE;
```

TiDB LightningおよびDumplingは現在スタンドアロンであるため、このオプションはサポートされていません。
