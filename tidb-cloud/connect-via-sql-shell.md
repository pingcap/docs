---
title: Connect via SQL Shell
summary: Learn how to connect to your TiDB cluster via SQL Shell.
---

# SQL シェル経由で接続する {#connect-via-sql-shell}

TiDB Cloud SQL Shell では、 TiDB SQL を試し、TiDB と MySQL の互換性をすばやくテストし、データベース ユーザー権限を管理できます。

> **注記：**
>
> SQL Shell を使用して[TiDB サーバーレスクラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)に接続することはできません。 TiDB サーバーレス クラスターに接続するには、 [TiDB サーバーレスクラスターに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)を参照してください。

SQL シェルを使用して TiDB クラスターに接続するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅の をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  ターゲット クラスターの名前をクリックしてクラスターの概要ページに移動し、右上隅の**[接続]**をクリックします。接続ダイアログが表示されます。

3.  ダイアログで、 **「Web SQL Shell」**タブを選択し、 **「Open SQL Shell」**をクリックします。

4.  プロンプトが表示される**「パスワードの入力**」行に、現在のクラスターの root パスワードを入力します。これで、アプリケーションが TiDB クラスターに接続されます。
