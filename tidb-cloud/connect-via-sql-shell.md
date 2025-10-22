---
title: Connect via SQL Shell
summary: SQL Shell 経由で TiDB クラスターに接続する方法を学習します。
---

# SQL シェル経由で接続する {#connect-via-sql-shell}

TiDB Cloud SQL Shell では、 TiDB SQLを試したり、TiDB と MySQL の互換性をすぐにテストしたり、データベース ユーザー権限を管理したりできます。

> **注記：**
>
> SQL Shellを使用して[TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)または[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)に接続することはできません。TiDB TiDB Cloud StarterまたはTiDB Cloud Essentialクラスターに接続するには、 [TiDB Cloud StarterまたはEssential クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。

SQL シェルを使用して TiDB クラスターに接続するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックしてクラスターの概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **[ネットワーク]**ページで、右上隅の**[Web SQL Shell]**をクリックします。

4.  プロンプトが表示されたら、 **「パスワードを入力**」行に現在のクラスタのルートパスワードを入力します。これで、アプリケーションがTiDBクラスタに接続されます。
