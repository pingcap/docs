---
title: TiDB Cloud Lake クイックスタート
summary: 3 つのステップで TiDB Cloud Lake を使い始めましょう。サインアップし、Lake を初期化し、Lake ワークスペースを確認します。
---

# TiDB Cloud Lake クイックスタート

このチュートリアルでは、TiDB Cloud Lake を簡単に使い始める方法を案内します。

## ステップ 1. TiDB Cloud にサインアップする {#step-1-sign-up-for-tidb-cloud}

1. <https://tidbcloud.com> にアクセスします。

2. TiDB Cloud アカウントにサインアップするか、既存のアカウントでログインします。

## ステップ 2. TiDB Cloud Lake を初期化する {#step-2-initialize-tidb-cloud-lake}

1. 左側のナビゲーションバーで **My Lake** をクリックします。

2. 右上隅で **Try TiDB Cloud Lake** をクリックします。新しいタブが開きます。

3. 画面の指示に従って TiDB Cloud Lake を初期化します。

    - **Name**: Lake の名前を入力します。
    - **Plan**: ユースケースに合ったプランを選択します。
    - **Cloud Provider and Region**: デプロイ先のリージョンを選択します。

4. **Create** をクリックし、初期化が完了するまで待ちます。

## ステップ 3. Lake ワークスペースを確認する {#step-3-explore-your-lake-workspace}

1. 初期化が完了したら、ホームページで Lake 名、プラン、クラウドプロバイダー、リージョンなどの Lake 情報を確認します。
2. ホームページの各エントリポイントを使って次に進みます。

    - **Connect**: 接続情報を取得します。
    - **Load Data** または **Load from Cloud Storage**: データのロード (load) を開始します。
    - **Query Data**: SQL Worksheet を作成します。

## 次のステップ {#what-s-next}

- [**TiDB Cloud Lake への接続**](/tidb-cloud-lake/guides/connection-overview.md): ワークフローに適したクライアントまたはドライバーを選択します。
- [**アーキテクチャを学ぶ**](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md): メタデータ、コンピュート、ストレージの各レイヤーを理解します。
- [**製品機能を確認する**](/tidb-cloud-lake/guides/vector-search-guide.md): 分析、ベクトル、検索、geo 機能から始めましょう。