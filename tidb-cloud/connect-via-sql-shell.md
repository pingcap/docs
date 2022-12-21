---
title: Connect via SQL Shell
summary: Learn how to connect to your TiDB cluster via SQL Shell.
---

# SQL シェル経由で接続 {#connect-via-sql-shell}

TiDB Cloud SQL Shell では、 TiDB SQLを試したり、TiDB と MySQL との互換性をすばやくテストしたり、データベース ユーザー権限を管理したりできます。

> **ノート：**
>
> SQL シェルを使用して[サーバーレス階層クラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)に接続することはできません。 Serverless Tier クラスターに接続するには、 [サーバーレス層クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md#serverless-tier)を参照してください。

SQL シェルを使用して TiDB クラスターに接続するには、次の手順を実行します。

1.  [**クラスタ**](https://tidbcloud.com/console/clusters)ページに移動し、左側のナビゲーション バーの上部でターゲット プロジェクトを選択します。

2.  クラスターを見つけて、クラスター領域の右上隅にある [**接続**] をクリックし、接続ダイアログで [ <strong>Web SQL シェル</strong>] タブを選択します。

3.  [ **SQL シェルを開く]**をクリックします。

4.  プロンプトが表示された**TiDB パスワード**行で、現在のクラスターのルート パスワードを入力します。次に、アプリケーションが TiDB クラスターに接続されます。
