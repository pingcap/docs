---
title: Back Up and Restore Data on Amazon S3 Using BR
summary: Learn how to use BR to back up data to and restore data from Amazon S3 storage.
---

# BR を使用して Amazon S3 でデータをバックアップおよび復元する {#back-up-and-restore-data-on-amazon-s3-using-br}

バックアップと復元 (BR) ツールは、Amazon S3 またはその他の Amazon S3 互換ファイル ストレージを、データのバックアップと復元用の外部ストレージとして使用することをサポートしています。

> **ノート：**
>
> オブジェクト ロックが有効になっている S3 バケットにデータをバックアップするには、TiDB クラスターが v6.3.0 以降であることを確認してください。

## アプリケーション シナリオ {#application-scenarios}

Amazon S3 を使用すると、Amazon EC2 にデプロイされた TiDB クラスターのデータを Amazon S3 にすばやくバックアップしたり、Amazon S3 のバックアップ データから TiDB クラスターをすばやく復元したりできます。

## S3 にアクセスする権限を設定する {#configure-privileges-to-access-s3}

S3 を使用してバックアップまたは復元を実行する前に、S3 へのアクセスに必要な権限を構成する必要があります。

### S3 ディレクトリへのアクセスを構成する {#configure-access-to-the-s3-directory}

バックアップの前に、S3 のバックアップ ディレクトリにアクセスするために次の権限を設定します。

-   バックアップ中に TiKV および BR が`s3:ListBucket` 、 `s3:PutObject` 、および`s3:AbortMultipartUpload`のバックアップ ディレクトリにアクセスするための最小権限
-   TiKV と BR が復元時に`s3:ListBucket`と`s3:GetObject`のバックアップ ディレクトリにアクセスするための最小限の権限

バックアップ ディレクトリをまだ作成していない場合は、 [AWS 公式ドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照して、指定したリージョンに S3 バケットを作成します。必要に応じて、 [AWS 公式ドキュメント - フォルダーの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してバケットにフォルダーを作成することもできます。

### S3 にアクセスするようにユーザーを構成する {#configure-a-user-to-access-s3}

次のいずれかの方法を使用して、S3 へのアクセスを構成することをお勧めします。

-   S3 にアクセスできるIAMロールを、TiKV および BR ノードが実行される EC2 インスタンスに関連付けます。関連付け後、BR は S3 のバックアップ ディレクトリにアクセスできます。

    {{< copyable "" >}}

    ```shell
    br backup full --pd "${PDIP}:2379" --storage "s3://${Bucket}/${Folder}"
    ```

-   `br` CLI で S3 にアクセスするために`access-key`と`secret-access-key`を設定し、 `--send-credentials-to-tikv=true`を設定して BR から各 TiKV にアクセス キーを渡します。

    {{< copyable "" >}}

    ```shell
    br backup full --pd "${PDIP}:2379" --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" --send-credentials-to-tikv=true
    ```

コマンドのアクセス キーは漏洩しやすいため、 IAMロールを EC2 インスタンスに関連付けて S3 にアクセスすることをお勧めします。

## データを S3 にバックアップする {#back-up-data-to-s3}

{{< copyable "" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" \
    --send-credentials-to-tikv=true \
    --ratelimit 128 \
    --log-file backuptable.log
```

前述のコマンドでは:

-   `--send-credentials-to-tikv` : アクセス キーが TiKV ノードに渡されることを指定します。

## S3 からデータを復元する {#restore-data-from-s3}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}?access-key=${accessKey}&secret-access-key=${secretAccessKey}" \
    --ratelimit 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
```

## こちらもご覧ください {#see-also}

BR がサポートする外部ストレージの詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。
