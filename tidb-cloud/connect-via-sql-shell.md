---
title: Connect via SQL Shell
summary: Learn how to connect to your TiDB cluster via SQL Shell.
---

# SQL シェル経由で接続する {#connect-via-sql-shell}

TiDB Cloud SQL Shell では、 TiDB SQL を試し、TiDB と MySQL の互換性をすばやくテストし、データベース ユーザー権限を管理できます。

> **ノート：**
>
> SQL Shell を使用して[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverlessクラスタ</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)に接続することはできません。 TiDB Serverless クラスタに接続するには、 [<a href="/tidb-cloud/connect-to-tidb-cluster.md#tidb-serverless">TiDB Serverlessクラスタに接続する</a>](/tidb-cloud/connect-to-tidb-cluster.md#tidb-serverless)を参照してください。

SQL シェルを使用して TiDB クラスターに接続するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)にログインし、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅にある ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

2.  ターゲット クラスターの名前をクリックしてクラスターの概要ページに移動し、右上隅の**[接続]**をクリックします。接続ダイアログが表示されます。

3.  ダイアログで、 **「Web SQL Shell」**タブを選択し、 **「Open SQL Shell」**をクリックします。

4.  プロンプトが表示される**「パスワードの入力**」行に、現在のクラスターの root パスワードを入力します。これで、アプリケーションが TiDB クラスターに接続されます。
