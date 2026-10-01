---
title: TiDB Cloud Data Pipeline 用の外部 stage を設定する (Alibaba Cloud)
summary: RAM ユーザーとアクセスキーを含め、Alibaba Cloud OSS バケットを TiDB Cloud Data Pipeline の外部 stage として設定する方法を説明します。
---

# TiDB Cloud Data Pipeline 用の外部 stage を設定する (Alibaba Cloud)

このガイドでは、[TiDB Cloud Data Pipeline](/tidb-cloud/data-pipeline.md) の外部 stage として Alibaba Cloud Object Storage Service (OSS) バケットを準備する方法を説明します。外部 stage は、TiDB Cloud がエクスポートしたスナップショットと行変更を書き込み、TiDB Cloud Lake がそこから読み取って対象の Warehouse にデータをロード (load) するための中間バケットです。

TiDB Cloud は増分データとスナップショットを OSS バケットに書き込み、TiDB Cloud Lake はそのバケットからデータを読み取ります。

> **Restriction:**
>
> - サポートされる認証方式は **Access Key** のみです。OSS では Role ARN は使用できません。
> - SQS を使用したイベント駆動の取り込みはサポートされていません。パイプラインはポーリングのみを使用します。

## 前提条件 {#prerequisites}

- OSS と RAM リソースを管理する権限を持つ Alibaba Cloud アカウント
- TiDB Cloud Lake の Warehouse を持つ TiDB Cloud アカウント

## ステップ 1. OSS バケットを作成する {#step-1-create-an-oss-bucket}

> **Tip:**
>
> すでに使用可能な OSS バケットがある場合は、この手順をスキップしてください。TiDB Cloud インスタンスと同じリージョンを使用することを推奨しますが、OSS では必須ではありません。

1. [OSS Console](https://oss.console.aliyun.com/) を開き、新しいバケットを作成します。
2. リージョンを選択します。TiDB Cloud インスタンスと同じリージョンを使用することを推奨します。
3. 必要に応じて、バケット内にフォルダー (プレフィックス) を作成し、TiDB Cloud データを整理します (例: `oss://tidb-cloud-lake-data/my-cluster/`)。
4. 後続の手順で必要になるため、次の値を記録しておきます。

    - **Bucket Name:** 例: `tidb-cloud-lake-data`
    - **OSS URI (with prefix):** 例: `oss://tidb-cloud-lake-data/my-cluster/`

## ステップ 2. RAM ユーザーと AccessKey ペアを作成する {#step-2-create-a-ram-user-and-accesskey-pair}

1. [RAM Console](https://ram.console.aliyun.com/) を開き、**Users > Create user** に移動します。
2. 表示名 (例: `tidb-cloud-lake-user`) を入力し、アクセス方法として **OpenAPI calling** を選択します。
3. **Next** をクリックし、**AccessKey ID** と **AccessKey Secret** をコピーして保存します。

    > **Note:**
    >
    > AccessKey Secret は作成時に一度だけ表示されます。必ずすぐに保存してください。

4. **Users** ページに戻り、作成したユーザー名をクリックして **Permissions** タブに移動し、**Add permissions** をクリックします。
5. **Custom policy** を選択し、**Create policy** をクリックしてから、**Script** タブを選択し、次の JSON からポリシーを作成します。

    ```json
    {
      "Version": "1",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "oss:HeadBucket",
            "oss:ListObjects",
            "oss:GetObject",
            "oss:PutObject",
            "oss:DeleteObject",
            "oss:GetBucketLocation"
          ],
          "Resource": [
            "acs:oss:*:*:YOUR_BUCKET_NAME",
            "acs:oss:*:*:YOUR_BUCKET_NAME/*"
          ]
        }
      ]
    }
    ```

    > **Note:** `YOUR_BUCKET_NAME` を OSS バケット名に置き換えてください。

6. ポリシー名 (例: `tidb-cloud-lake-access`) を入力し、**OK** をクリックします。
7. このポリシーを RAM ユーザーにアタッチします。
8. TiDB Cloud の設定時に必要になるため、次の値を記録しておきます。
    - **Access Key ID:** 例: `LTAI5t...`
    - **Access Key Secret:** 作成時に保存した値

## 次のステップ {#what-s-next}

Alibaba Cloud の設定が完了すると、External Stage の設定に必要な値がすべてそろいます。

- **OSS URI**: [ステップ 1](#step-1-create-an-oss-bucket) で取得
- **Access Key ID** と **Access Key Secret**: [ステップ 2](#step-2-create-a-ram-user-and-accesskey-pair) で取得

[TiDB Cloud コンソール](https://tidbcloud.com) で、対象の TiDB Cloud インスタンスの Data Pipeline 設定ページに移動し、**External Stage** 設定にこれらの値を入力して、データパイプラインの設定を完了してください。
