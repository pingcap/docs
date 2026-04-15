---
title: Back Up and Restore TiDB Cloud Starter or Essential Data
summary: TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのバックアップと復元方法を学びましょう。
aliases: ['/ja/tidbcloud/restore-deleted-tidb-cluster']
---

# TiDB Cloud StarterまたはEssentialデータのバックアップと復元 {#back-up-and-restore-tidb-cloud-starter-or-essential-data}

このドキュメントでは、TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンス上のデータのバックアップと復元方法について説明します。

> **ヒント：**
>
> TiDB Cloud Dedicatedクラスター上のデータをバックアップおよび復元する方法については、 [TiDB Cloud Dedicatedデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)復元」を参照してください。

## バックアップページをビュー {#view-the-backup-page}

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックすると、その概要ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  左側のナビゲーションペインで、 **[データ]** &gt; **[バックアップ]**をクリックします。

## 自動バックアップ {#automatic-backups}

TiDB Cloudはデータを自動的にバックアップするため、災害発生時にバックアップスナップショットからデータを復元することで、データ損失を最小限に抑えることができます。

### バックアップ設定について学ぶ {#learn-about-the-backup-setting}

自動バックアップの設定は、 TiDB Cloud StarterインスタンスとTiDB Cloud Essentialインスタンスで異なり、以下の表に示されています。

| バックアップ設定   | TiDB Cloud Starter （無料） | TiDB Cloud Starter （利用限度額 &gt; 0） | TiDB Cloud Essential |
| ---------- | ----------------------- | --------------------------------- | -------------------- |
| バックアップサイクル | 毎日                      | 毎日                                | 毎日                   |
| バックアップ保持   | 1日                      | 最大30日間                            | 最大30日間               |
| バックアップ時間   | 固定時間                    | 設定可能                              | 設定可能                 |

-   **バックアップサイクル**とは、バックアップが実行される頻度のことです。

-   **バックアップ保持期間**とは、バックアップが保持される期間のことです。期限切れのバックアップは復元できません。

    -   無料のTiDB Cloud Starterインスタンスの場合、バックアップの保持期間は1日間です。
    -   TiDB Cloud Starter （利用限度額が0より大きい場合）またはTiDB Cloud Essentialインスタンスの場合、バックアップの保持期間を1日から30日の間の任意の値に設定できます。デフォルトの保持期間は14日です。

-   **バックアップ時刻**とは、バックアップのスケジュールが開始される時刻です。最終的なバックアップ時刻は、設定されたバックアップ時刻よりも遅れる場合があることにご注意ください。

    -   無料のTiDB Cloud Starterインスタンスの場合、バックアップ時間はランダムに固定された時間になります。
    -   TiDB Cloud Starter （利用限度額が0より大きい場合）またはTiDB Cloud Essentialインスタンスの場合、バックアップ間隔を30分ごとに設定できます。デフォルト値はランダムに固定された時間です。

### バックアップ設定を構成する {#configure-the-backup-setting}

TiDB Cloud Essentialインスタンスのバックアップ時間を設定するには、以下の手順を実行します。

1.  TiDB Cloud StarterまたはEssentialインスタンスの[**バックアップ**](#view-the-backup-page)ページに移動します。

2.  **「バックアップ設定」**をクリックしてください。すると**「バックアップ設定」**ウィンドウが開きます。ここで、必要に応じて自動バックアップの設定を構成できます。

3.  **「バックアップ時間」**で、毎日のバックアップの開始時間を設定します。

4.  **「確認」**をクリックしてください。

## 復元する {#restore}

TiDB Cloudは、偶発的なデータ損失や破損が発生した場合にデータを復旧するための復元機能を提供します。

### 復元モード {#restore-mode}

TiDB Cloudは、 TiDB Cloud StarterまたはEssentialインスタンスのスナップショット復元と特定時点への復元をサポートしています。

-   **スナップショット復元**：特定のバックアップスナップショットからTiDB Cloud StarterまたはEssentialインスタンスを復元します。

-   **ポイントインタイム復元（ベータ版）** ： TiDB Cloud Essentialインスタンスを特定の時点の状態に復元します。

    -   TiDB Cloud Starterインスタンス：サポートされていません。
    -   TiDB Cloud Essentialインスタンス：バックアップ保持期間内の任意の時点に復元できますが、 TiDB Cloud Essentialインスタンスの作成時刻より前、または現在時刻の1分前より後には復元できません。

### 目的地を復元する {#restore-destination}

TiDB Cloudは、新しいTiDB Cloud StarterまたはEssentialインスタンスへのデータ復元をサポートしています。

### 復元タイムアウト {#restore-timeout}

復元プロセスは通常数分以内に完了します。復元に3時間以上かかる場合は、自動的にキャンセルされ、新しいTiDB Cloud StarterまたはEssentialインスタンスは削除されますが、元のインスタンスは変更されません。

キャンセルされた復元後にデータが破損し、復旧できない場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

### 新しいTiDB Cloud StarterまたはEssentialインスタンスに復元します {#restore-to-a-new-instance} {#restore-to-a-new-instance}

> **注記：**
>
> 元のTiDB Cloud StarterまたはEssentialインスタンスのユーザー認証情報と権限は、新しいTiDB Cloud StarterまたはEssentialインスタンスには復元されません。

新しいTiDB Cloud StarterまたはEssentialインスタンスにデータを復元するには、以下の手順に従ってください。

1.  TiDB Cloud StarterまたはEssentialインスタンスの[**バックアップ**](#view-the-backup-page)ページに移動します。

2.  **「復元」**をクリックしてください。

3.  **復元モード**では、特定のバックアップから復元するか、任意の時点から復元するかを選択できます。

     <SimpleTab>
     <div label="Snapshot Restore">

    選択したバックアップスナップショットから復元するには、次の手順を実行します。

    1.  **「スナップショット復元」**をクリックします。
    2.  復元元のバックアップスナップショットを選択してください。

    </div>
     <div label="Point-in-Time Restore">

    TiDB Cloud Essentialインスタンスを特定の時点に復元するには、以下の手順を実行してください。

    1.  **「特定時点への復元」**をクリックします。
    2.  復元したい日時を選択してください。

    </div>
     </SimpleTab>

4.  新しいインスタンスの名前を入力してください。

5.  必要に応じて容量を更新してください。

    -   TiDB Cloud Starterインスタンスの場合、 [無料割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)よりも多くのリソースが必要な場合は、毎月の支出制限を設定してください。
    -   TiDB Cloud Essentialインスタンスの場合、最小RCUと最大RCUを設定し、必要に応じて詳細設定を構成してください。

6.  **「復元」**をクリックして復元プロセスを開始してください。

復元処理が開始されると、 TiDB Cloud StarterまたはEssentialインスタンスのステータスが**「復元中」**に変わります。復元が完了し、ステータスが**「利用可能」**に変わるまで、 TiDB Cloud StarterまたはEssentialインスタンスは利用できません。

## 制限事項 {#limitations}

-   TiFlashレプリカが有効になっている場合、データの再構築がTiFlash内で行われるため、復元後一定期間は利用できなくなります。
-   TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスでは、手動バックアップはサポートされていません。
-   TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスで、1 TiBを超えるデータが含まれている場合、デフォルトでは新しいインスタンスへの復元はサポートされません。より大規模なデータセットに関するサポートが必要な場合は[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。
