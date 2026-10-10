---
title: Amazon S3 - Credentials
summary: このページでは、`Amazon S3 - Credentials` データソースを作成する方法について説明します。このデータソースには、Amazon S3 へのアクセスに必要な認証情報が保存され、複数の S3 統合タスクで再利用できます。
---

# Amazon S3 - Credentials

このページでは、`Amazon S3 - Credentials` データソースを作成する方法について説明します。このデータソースには、Amazon S3 へのアクセスに必要な認証情報が保存され、複数の S3 統合タスクで再利用できます。

## ユースケース {#use-cases}

- 複数の S3 インポートタスクに対して、1 組の AWS Access Key と Secret Key 認証情報を管理する
- すべてのタスクで同じ S3 アクセス認証情報を毎回再入力する手間を省く
- 認証情報がローテーションされた際に、一元的に更新する

## Amazon S3 - Credentials を作成する {#create-amazon-s3-credentials}

1. **Data** > **Data Sources** に移動し、**Create Data Source** をクリックします。
2. サービスタイプとして **Amazon S3 - Credentials** を選択し、認証情報を入力します。

    | フィールド | 必須 | 説明 |
    |-------|----------|-------------|
    | **Name** | はい | このデータソースのわかりやすい名前 |
    | **Access Key** | はい | AWS Access Key ID |
    | **Secret Key** | はい | AWS Secret Access Key |

3. **Test Connectivity** をクリックして認証情報を検証します。テストが成功したら、**OK** をクリックしてデータソースを保存します。

## 権限要件 {#permission-requirements}

AWS 認証情報には、対象の S3 バケットに対する読み取り権限が必要です。後続のタスクで **Clean Up Original Files** を有効にする場合は、認証情報に書き込み権限と削除権限も必要です。

## 次のステップ {#next-steps}

このデータソースを作成した後は、これを使用して [Amazon S3 統合タスク](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) を作成できます。