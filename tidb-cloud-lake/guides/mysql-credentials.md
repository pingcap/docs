---
title: MySQL - Credentials
summary: このページでは、`MySQL - Credentials` データソースを作成する方法について説明します。このデータソースには、MySQL へのアクセスに必要な接続情報が保存され、複数の MySQL 統合タスクで再利用できます。
---

# MySQL - Credentials

このページでは、`MySQL - Credentials` データソースを作成する方法について説明します。このデータソースには、MySQL へのアクセスに必要な接続情報が保存され、複数の MySQL 統合タスクで再利用できます。

## ユースケース {#use-cases}

- 複数の MySQL 同期タスクに対するホスト、ポート、アカウント情報を一元管理する
- すべてのタスクで同じデータベース接続設定を毎回入力し直す手間を避ける
- データベースのエンドポイントまたはアカウントが変更されたときに、依存するすべてのタスクを 1 か所で更新する

## MySQL - Credentials を作成する {#create-mysql-credentials}

1. **Data** > **Data Sources** に移動し、**Create Data Source** をクリックします。
2. サービスタイプとして **MySQL - Credentials** を選択し、接続の詳細を入力します。

    | フィールド | 必須 | 説明 |
    |-------|----------|-------------|
    | **Name** | はい | このデータソースの説明的な名前 |
    | **Hostname** | はい | MySQL サーバーのホスト名または IP アドレス |
    | **Port Number** | はい | MySQL サーバーのポート（デフォルト: `3306`） |
    | **DB Username** | はい | MySQL へのアクセスに使用するユーザー名 |
    | **DB Password** | はい | MySQL ユーザーのパスワード |
    | **Database Name** | はい | ソースデータベース名 |
    | **DB Charset** | いいえ | 文字セット（デフォルト: `utf8mb4`） |
    | **Server ID** | いいえ | 一意の Binlog レプリケーション識別子。指定しない場合は自動生成されます |

3. **Test Connectivity** をクリックして接続を検証します。テストが成功したら、**OK** をクリックしてデータソースを保存します。

## 使用上の推奨事項 {#usage-recommendations}

- アプリケーションのワークロードと共有するのではなく、専用の MySQL アカウントを使用する
- `CDC Only` または `Snapshot + CDC` タスクを作成する予定がある場合は、そのアカウントにレプリケーション関連の権限があることを確認する
- 下流タスクを作成する前に、ネットワークアクセス、binlog 設定、および権限を確認する

## 次のステップ {#next-steps}

このデータソースを作成した後は、これを使用して [MySQL Integration Task](/tidb-cloud-lake/guides/integrate-with-mysql.md) を作成できます。