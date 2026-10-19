---
title: PostgreSQL互換 TiDB Cloud Starter を使い始める
summary: PostgreSQL互換の TiDB Cloud Starter インスタンスを作成して接続する方法を学びます。
category: quick start
---

# PostgreSQL互換 TiDB Cloud Starter を使い始める

このチュートリアルでは、PostgreSQL互換の TiDB Cloud Starter インスタンスを作成し、接続する手順を説明します。

> **Note:**
>
> PostgreSQL互換 TiDB Cloud Starter は現在パブリックプレビューで提供されています。

また、[TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start) で TiDB の機能を試すこともできます。

## ステップ 1. {{{ .starter }}} インスタンスを作成する {#step-1-create-a-starter-instance}

{{{ .starter }}} インスタンスを作成するには、次の手順を実行します。

1. TiDB Cloud アカウントをお持ちでない場合は、[こちら](https://tidbcloud.com/free-trial) をクリックしてサインアップします。

    メールアドレスとパスワードでサインアップして TiDB Cloud でパスワードを管理することも、Google、GitHub、または Microsoft アカウントでサインインして TiDB Cloud にシングルサインオン（SSO）することもできます。

2. [ログイン](https://tidbcloud.com/) して TiDB Cloud アカウントにアクセスします。

    デフォルトでは、[**My TiDB**](https://tidbcloud.com/tidbs) ページが表示されます。

3. 新しい PostgreSQL互換 {{{ .starter }}} インスタンスを作成するには、次の手順を実行します。

    1. **Create Resource** をクリックします。
    2. **Create Resource** ページで、**Starter** を選択します。
    3. **Compatibility Mode** セクションで、**PostgreSQL Compatible** を選択します。
    4. {{{ .starter }}} インスタンスの名前を入力し、クラウドプロバイダーと対象のリージョンを選択してから、**Create** をクリックします。

    > **Note:**
    >
    > PostgreSQL互換 {{{ .starter }}} インスタンスは、現在パブリックプレビュー期間中は無料で利用できます。
    >
    > 組織内の最初の 10 個の PostgreSQL互換 {{{ .starter }}} インスタンスが無料枠の対象です。対象となる各インスタンスには、毎月次の無料枠が含まれます。
    >
    > + 50 GiB の行ベースストレージ
    > + 5 億 Request Units (RUs)
    >
    > PostgreSQL互換 {{{ .starter }}} インスタンスが無料枠に達すると、超過したリソース消費に対して使用制限またはサービス停止が適用される場合があります。これらの上限を超える見込みがある場合は、要件について相談するために <a href="mailto:support@pingcap.com">support@pingcap.com</a> までご連絡ください。

## ステップ 2. {{{ .starter }}} インスタンスに接続する {#step-2-connect-to-your-starter-instance}

PostgreSQL互換 {{{ .starter }}} インスタンスは PostgreSQL wire protocol をサポートしているため、ほとんどの PostgreSQL ツール、ドライバー、ORM を使用して接続できます。以下の手順では、例として PostgreSQL CLI クライアント `psql` を使用します。

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .starter }}} インスタンス名をクリックして概要ページを開きます。
2. 右上の **Connect** をクリックします。接続パラメータを含む接続ダイアログが表示されます。
3. 接続ダイアログ内の設定が、ご利用の実行環境と一致していることを確認します。
4. **Generate Password** をクリックしてランダムなパスワードを作成します。
5. **Connect With** ドロップダウンリストで、**PostgreSQL CLI** を選択します。
6. 接続コマンドをコピーしてターミナルに貼り付け、**Enter** を押して実行します。

PostgreSQL CLI クライアント `psql` が起動し、{{{ .starter }}} インスタンスに接続されます。

## 次のステップ {#what-s-next}

- PostgreSQL 互換性については、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。
- TiDB Cloud が現在サポートしている PostgreSQL 拡張機能については、[PostgreSQL 拡張機能](/tidb-cloud/starter/pg-extensions-overview.md) を参照してください。