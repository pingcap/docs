---
title: Connect via SQL Shell
summary: Learn how to connect to your TiDB cluster via SQL Shell.
---

# SQL シェル経由で接続 {#connect-via-sql-shell}

TiDB Cloud SQL Shell では、 TiDB SQL を試したり、TiDB と MySQL との互換性をすばやくテストしたり、データベース ユーザー権限を管理したりできます。

> **ノート：**
>
> SQL シェルを使用して[Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)に接続することはできません。 Serverless Tierクラスターに接続するには、 [Serverless Tierクラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md#serverless-tier)を参照してください。

SQL シェルを使用して TiDB クラスターに接続するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

2.  ターゲット クラスターの名前をクリックしてそのクラスターの概要ページに移動し、右上隅にある**[接続]**をクリックします。接続ダイアログが表示されます。

3.  ダイアログで**[Web SQL シェル]**タブを選択し、 <strong>[SQL シェルを開く]</strong>をクリックします。

4.  プロンプトが表示された**Enter password**行で、現在のクラスターの root パスワードを入力します。次に、アプリケーションが TiDB クラスターに接続されます。
