---
title: TiDB Dashboard Cluster Information Page
summary: View the running status of TiDB, TiKV, PD, TiFlash components in the entire cluster and the running status of the host on which these components are located.
---

# TiDB ダッシュボードクラスタ情報ページ {#tidb-dashboard-cluster-information-page}

クラスター情報ページでは、クラスター全体の TiDB、TiKV、PD、 TiFlashコンポーネントの実行ステータスと、これらのコンポーネントが配置されているホストの実行ステータスを表示できます。

## ページにアクセスする {#access-the-page}

次の 2 つの方法のいずれかを使用して、クラスター情報ページにアクセスできます。

-   TiDB ダッシュボードにログインした後、左側のナビゲーション メニューで [**クラスタ情報**] をクリックします。

    ![Access cluster information page](/media/dashboard/dashboard-cluster-info-access.png)

-   ブラウザで[http://127.0.0.1:2379/dashboard/#/cluster_info/instance](http://127.0.0.1:2379/dashboard/#/cluster_info/instance)にアクセスします。 `127.0.0.1:2379`を実際の PD インスタンスのアドレスとポートに置き換えます。

## インスタンス一覧 {#instance-list}

**インスタンス**をクリックして、インスタンスのリストを表示します。

![Instance list](/media/dashboard/dashboard-cluster-info-instances.png)

このインスタンス リストには、クラスター内の TiDB、TiKV、PD、およびTiFlashコンポーネントのすべてのインスタンスの概要情報が表示されます。

リストには次の情報が含まれます。

-   アドレス: インスタンスのアドレス。
-   ステータス: インスタンスの実行ステータス。
-   稼働時間: インスタンスの開始時間。
-   バージョン: インスタンスのバージョン番号。
-   デプロイ ディレクトリ: インスタンス バイナリ ファイルが配置されているディレクトリ。
-   Git ハッシュ: インスタンスのバイナリ ファイルに対応する Git ハッシュ値。

### インスタンスのステータス {#instance-status}

インスタンスは、次のいずれかのステータスで実行できます。

-   Up: インスタンスは正常に動作しています。
-   ダウンまたは到達不能: インスタンスが実行されていないか、対応するホストにネットワークの問題が存在します。
-   Tombstone: インスタンスのデータは完全に移行され、スケールインが完了しました。このステータスは、TiKV またはTiFlashインスタンスにのみ存在します。
-   退出中: インスタンスのデータが移行されており、スケールインが進行中です。このステータスは、TiKV またはTiFlashインスタンスにのみ存在します。
-   不明: インスタンスの実行状態は不明です。

> **ノート：**
>
> -   TiDB ダッシュボードでは`Leaving` 、PD API によって返される`Offline` 、 TiUPでは`Pending Offline`は同じステータスを示します。
> -   テーブルの一部の列は、インスタンスが起動している場合にのみ表示できます。

インスタンスのステータスは、PD スケジューリング情報から取得されます。詳細については、 [情報収集](/tidb-scheduling.md#information-collection)を参照してください。

## ホスト一覧 {#host-list}

[**ホスト**] をクリックして、ホストのリストを表示します。

![Host list](/media/dashboard/dashboard-cluster-info-hosts.png)

このホスト リストには、クラスター内の TiDB、TiKV、PD、およびTiFlashコンポーネントのすべてのインスタンスに対応するホストの実行ステータスが表示されます。

リストには次の情報が含まれます。

-   アドレス: ホスト IP アドレス。
-   CPU: ホスト CPU の論理コア数。
-   CPU 使用率: 現在の 1 秒間のユーザー モードおよびカーネル モードの CPU 使用率。
-   メモリ: ホストの合計物理メモリ サイズ。
-   メモリ使用量: ホストの現在のメモリ使用量。
-   ディスク: インスタンスが実行されているホスト上のディスクのファイル システムと、このディスクのマウント パス。
-   ディスク使用量: インスタンスが実行されているホスト上のディスクのスペース使用量。

> **ノート：**
>
> ホスト一覧情報はインスタンスプロセスごとに提供されるため、ホスト上のすべてのインスタンスがダウンしている場合、ホスト情報は表示されません。
