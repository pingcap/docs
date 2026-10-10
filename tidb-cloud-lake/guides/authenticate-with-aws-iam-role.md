---
title: AWS IAM Role による認証
summary: クラウドネイティブな ID 委任（AWS IAM Role、Azure Managed Identity、Google Service Account federation など）により、{{{ .lake }}} は生の access key を扱うことなく、オブジェクトストレージに対する短期間有効な認証情報を取得できます。これにより、データプレーンへのアクセスはクラウドプロバイダーのコントロールプレーン内で管理され、すべての権限の所有権は引き続きお客様が保持できます。
---

# AWS IAM Role による認証

クラウドネイティブな ID 委任（AWS IAM Role、Azure Managed Identity、Google Service Account federation など）により、{{{ .lake }}} は生の access key を扱うことなく、オブジェクトストレージに対する短期間有効な認証情報を取得できます。これにより、データプレーンへのアクセスはクラウドプロバイダーのコントロールプレーン内で管理され、すべての権限の所有権は引き続きお客様が保持できます。

## IAM role の利点 {#iam-role-benefits}

- 静的キーが不要: 一時的な認証情報により、ローテーションや漏えい対策が必要な長期間有効なシークレットを排除できます。
- 最小権限: きめ細かなポリシーにより、{{{ .lake }}} がアクセスできるバケットや実行できる操作を、承認したもののみに制限できます。
- 一元的なガバナンス: 既存の IAM ワークフローを通じて、引き続きアクセスの監査や取り消しを行えます。
- 自動ローテーション: クラウドプロバイダーがトークンを更新するため、チーム変更があっても統合は継続して動作します。

## 仕組み {#how-it-works}

{{{ .lake }}} サポートから組織向けの信頼されたプリンシパル情報が共有された後、クラウドアカウント内で IAM role/identity を作成し、必要なオブジェクトストレージ操作（たとえば一連のバケットの読み取り）を許可するポリシーをアタッチします。さらに、固有の external ID を使用して {{{ .lake }}} のみがその role を引き受けられるように信頼ポリシーを設定します。その後、{{{ .lake }}} は必要に応じてその role を引き受け、一時的な認証情報を使ってストレージにアクセスし、セッションの有効期限が切れると自動的にログアウトします。

## IAM role を使用する {#use-iam-role}

1. サポートチケットを起票し、{{{ .lake }}} 組織用の IAM role ARN を取得します。

   例: `arn:aws:iam::123456789012:role/xxxxxxx/tnabcdefg/xxxxxxx-tnabcdefg`

2. AWS Console に移動します。

   <https://us-east-2.console.aws.amazon.com/iam/home?region=us-east-2#/policies>

   `Create policy` をクリックし、`Custom trust policy` を選択して、S3 バケットアクセス用のポリシードキュメントを入力します。

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "s3:ListBucket",
         "Resource": "arn:aws:s3:::test-bucket-123"
       },
       {
         "Effect": "Allow",
         "Action": "s3:*Object",
         "Resource": "arn:aws:s3:::test-bucket-123/*"
       }
     ]
   }
   ```

   `Next` をクリックし、ポリシー名 `lake-test` を入力して、`Create policy` をクリックします。

3. AWS Console に移動します。

   <https://us-east-2.console.aws.amazon.com/iam/home?region=us-east-2#/roles>

   `Create role` をクリックし、`Trusted entity type` で `Custom trust policy` を選択します。

   ![Create Role](/media/tidb-cloud-lake/create-role.png)

   信頼ポリシードキュメントを入力します。

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "AWS": "arn:aws:iam::123456789012:role/xxxxxxx/tnabcdefg/xxxxxxx-tnabcdefg"
         },
         "Condition": {
           "StringEquals": {
             "sts:ExternalId": "my-external-id-123"
           }
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

   `Next` をクリックし、先ほど作成したポリシー `lake-test` を選択します。

   `Next` をクリックし、role 名 `lake-test` を入力します。

   `View Role` をクリックし、role ARN `arn:aws:iam::987654321987:role/lake-test` を記録します。

4. 次の SQL 文を {{{ .lake }}} cloud worksheet または `LakeSQL` で実行します。

   ```sql
   CREATE CONNECTION lake_test STORAGE_TYPE = 's3' ROLE_ARN = 'arn:aws:iam::987654321987:role/lake-test' EXTERNAL_ID = 'my-external-id-123';

   CREATE STAGE lake_test URL = 's3://test-bucket-123' CONNECTION = (CONNECTION_NAME = 'lake_test');

   SELECT * FROM @lake_test/test.parquet LIMIT 1;
   ```

> **Note:**
>
> これで、IAM Role を使用して {{{ .lake }}} からご自身の AWS S3 バケットにアクセスできるようになりました。