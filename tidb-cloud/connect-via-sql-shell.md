---
title: Connect via SQL Shell
summary: SQLシェルを使用してTiDBクラスタに接続する方法を学びましょう。
---

# SQL Shell経由で接続する {#connect-via-sql-shell}

TiDB Cloud SQL Shell では、 TiDB SQL を試用したり、TiDB と MySQL の互換性を迅速にテストしたり、データベースのユーザー権限を管理したりできます。

> **注記：**
>
> SQL Shell を使用して[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)または[TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)に接続することはできません。 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続するには、 [TiDB Cloud StarterまたはEssentialインスタンスに接続します。](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。

SQLシェルを使用してTiDBに接続するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「設定」** &gt; **「ネットワーク」**をクリックします。

3.  **ネットワーク**ページで、右上隅にある**「Web SQL Shell」**をクリックします。

4.  **「パスワードを入力してください**」というプロンプトが表示されたら、現在のクラスタのrootパスワードを入力してください。これで、アプリケーションがTiDBクラスタに接続されます。
