---
title: PostgreSQL - Credentials
summary: このページでは、`PostgreSQL - Credentials` データソースを作成する方法について説明します。このデータソースには、PostgreSQL へのアクセスに必要な接続情報が保存され、複数の PostgreSQL 統合タスクで再利用できます。
---

# PostgreSQL - Credentials

このページでは、`PostgreSQL - Credentials` データソースを作成する方法について説明します。このデータソースには、PostgreSQL へのアクセスに必要な接続情報が保存され、複数の PostgreSQL 統合タスクで再利用できます。

## ユースケース {#use-cases}

- 複数の PostgreSQL 同期タスクのホスト、ポート、アカウント情報を一元管理する
- すべてのタスクで同じデータベース接続設定を毎回入力し直す手間を避ける
- データベースのエンドポイントまたはアカウントが変更されたときに、依存するすべてのタスクを 1 か所で更新する

## PostgreSQL - Credentials を作成する {#create-postgresql-credentials}

1. **Data** > **Data Sources** に移動し、**Create Data Source** をクリックします。
2. サービスタイプとして **PostgreSQL - Credentials** を選択し、接続の詳細を入力します。

    | フィールド | 必須 | 説明 |
    |-------|----------|-------------|
    | **Name** | はい | このデータソースのわかりやすい名前 |
    | **Hostname** | はい | PostgreSQL サーバーのホスト名または IP アドレス |
    | **Port Number** | はい | PostgreSQL サーバーのポート（デフォルト: `5432`） |
    | **DB Username** | はい | PostgreSQL へのアクセスに使用するユーザー名 |
    | **DB Password** | はい | PostgreSQL ユーザーのパスワード |
    | **Database Name** | はい | ソースデータベース名 |
    | **SSL Mode** | いいえ | SSL 接続モード: `disable`、`require`、`verify-ca`、または `verify-full`（デフォルト: `disable`） |

3. **Test Connectivity** をクリックして接続を検証します。テストが成功したら、**OK** をクリックしてデータソースを保存します。

## 使用上の推奨事項 {#usage-recommendations}

- アプリケーションのワークロードと共有するのではなく、PostgreSQL 専用のアカウントを使用する
- `CDC Only` または `Snapshot + CDC` タスクを作成する予定がある場合は、そのアカウントにレプリケーション関連の権限があることを確認する
- 下流タスクを作成する前に、ネットワークアクセス、WAL 設定、および権限を確認する

## 次のステップ {#next-steps}

このデータソースを作成した後は、これを使用して [PostgreSQL Integration Task](/tidb-cloud-lake/guides/integrate-with-postgresql.md) を作成できます。