---
title: Back Up and Restore Data on Amazon S3 Using BR
summary: Learn how to use BR to back up data to and restore data from Amazon S3 storage.
---

# BRを使用してAmazonS3でデータをバックアップおよび復元する {#back-up-and-restore-data-on-amazon-s3-using-br}

Backup＆Restore（BR）ツールは、データをバックアップおよび復元するための外部ストレージとして、AmazonS3または他のAmazonS3互換のファイルストレージの使用をサポートします。

## アプリケーションシナリオ {#application-scenarios}

Amazon S3を使用すると、AmazonEC2にデプロイされたTiDBクラスタのデータをAmazonS3にすばやくバックアップしたり、AmazonS3のバックアップデータからTiDBクラスタをすばやく復元したりできます。

## S3にアクセスするための特権を設定します {#configure-privileges-to-access-s3}

S3を使用してバックアップまたは復元を実行する前に、S3にアクセスするために必要な権限を設定する必要があります。

### S3ディレクトリへのアクセスを設定します {#configure-access-to-the-s3-directory}

バックアップする前に、S3のバックアップディレクトリにアクセスするために次の権限を設定します。

-   バックアップ中に`s3:ListBucket` 、および`s3:PutObject`のバックアップディレクトリにアクセスするための`s3:AbortMultipartUpload`およびBRの最小特権
-   復元中に`s3:ListBucket`と`s3:GetObject`のバックアップディレクトリにアクセスするためのTiKVとBRの最小権限

バックアップディレクトリをまだ作成していない場合は、 [AWS公式ドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照して、指定したリージョンにS3バケットを作成します。必要に応じて、 [AWS公式ドキュメント-フォルダの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してバケット内にフォルダを作成することもできます。

### S3にアクセスするようにユーザーを設定する {#configure-a-user-to-access-s3}

次のいずれかの方法を使用して、S3へのアクセスを設定することをお勧めします。

-   S3にアクセスできるIAMロールを、TiKVノードとBRノードが実行されているEC2インスタンスに関連付けます。アソシエーション後、BRはS3のバックアップディレクトリにアクセスできます。

    {{< copyable "" >}}

    ```shell
    br backup full --pd "${PDIP}:2379" --storage "s3://${Bucket}/${Folder}" --s3.region "${region}"
    ```

-   `br` CLIでS3にアクセスするために`access-key`と`secret-access-key`を設定し、BRから各TiKVにアクセスキーを渡すように`--send-credentials-to-tikv=true`を設定します。

    {{< copyable "" >}}

    ```shell
    br backup full --pd "${PDIP}:2379" --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" --s3.region "${region}" --send-credentials-to-tikv=true
    ```

コマンドのアクセスキーはリークに対して脆弱であるため、IAMロールをEC2インスタンスに関連付けてS3にアクセスすることをお勧めします。

## データをS3にバックアップします {#back-up-data-to-s3}

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" \
    --s3.region "${region}" \
    --send-credentials-to-tikv=true \
    --ratelimit 128 \
    --log-file backuptable.log
```

前のコマンドで：

-   `--s3.region` ：S3の領域を指定します。
-   `--send-credentials-to-tikv` ：アクセスキーがTiKVノードに渡されることを指定します。

## S3からデータを復元する {#restore-data-from-s3}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" \
    --s3.region "${region}" \
    --ratelimit 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
```

## も参照してください {#see-also}

BRでサポートされている外部ストレージの詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。
