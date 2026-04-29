---
title: User-Controlled Log Redaction
summary: TiDB Cloudでユーザーが制御するログのマスキングを有効または無効にする方法を学び、実行ログ内の機密データの可視性を管理しましょう。
---

# ユーザーによるログの編集 {#user-controlled-log-redaction}

ユーザー制御のログ秘匿化により<CustomContent plan="dedicated">[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>ログ内の機密データの可視性を管理できます。この編集機能を切り替えることで、情報を保護し、運用上のニーズとセキュリティのバランスをとり、 <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>ログに表示される内容を制御できます。

ログのマスキングはデフォルトで有効になっており、実行ログや実行プラン内の機密情報が隠蔽されます。TiDB <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>メンテナンスやSQLチューニングのために、より詳細なログ情報が必要な場合は、この機能をいつでも無効にできます。

> **注記：**
>
> ログ編集機能は、 TiDB Cloud DedicatedクラスターおよびTiDB Cloud Premium インスタンスでサポートされています。

## 前提条件 {#prerequisites}

<CustomContent plan="dedicated">

-   TiDB Cloudでは、組織の**組織オーナー**または**プロジェクトオーナー**の役割を担っている必要があります。
-   TiDB Cloud Dedicatedクラスターが`paused`状態にある場合、ログのマスキングを有効または無効にすることはできません。

</CustomContent>

<CustomContent plan="premium">

-   TiDB Cloudにおいて、組織の**組織オーナー**の役割を担っている必要があります。

</CustomContent>

## ログの編集を無効にする {#disable-log-redaction}

> **警告：**
>
> ログのマスキングを無効にすると、機密情報が公開され、データ漏洩のリスクが高まる可能性があります。続行する前に、このリスクを理解し、認識していることを確認してください。診断またはメンテナンス作業が完了したら、すぐにログのマスキングを再度有効にすることを忘れないでください。

ログのマスキングを無効にするには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。

2.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>の名前をクリックして、その概要ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

3.  左側のナビゲーションペインで、 **[設定]** &gt; **[Security]**をクリックします。

4.  **実行ログの編集**セクションでは、編集機能がデフォルトで**有効になっている**ことがわかります。

5.  **「無効にする」**をクリックします。ログのマスキングを無効にすることのリスクを説明する警告が表示されます。

6.  無効化を確認してください。

ログのマスキングを無効にした後、以下の点に注意してください。

-   この変更は、新規のデータベース接続にのみ適用されます。
-   既存の接続には影響はありません。変更を有効にするには、既存の接続を再接続する必要があります。
-   新規セッションのログは今後編集されなくなります。

## 更新されたログを確認してください {#check-the-updated-logs}

ログのマスキングが無効になった後に更新されたログを確認するには、次の手順を実行します。

1.  クエリの実行速度が遅いことが原因で発生するパフォーマンスの問題をシミュレートします。たとえば、次の SQL ステートメントを実行します。

    ```sql
    SELECT *, SLEEP(2) FROM users WHERE email LIKE "%useremail%";
    ```

2.  スロークエリログが更新されるまで数分お待ちください。

3.  ログを確認して、機密データが削除されていないことを確認してください。

## ログの編集を有効にする {#enable-log-redaction}

データセキュリティを維持するため、診断またはメンテナンス作業が完了したらすぐに、以下の手順で**ログのマスキングを有効にしてください**。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。

2.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>の名前をクリックして、その概要ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

3.  左側のナビゲーションペインで、 **[設定]** &gt; **[Security]**をクリックします。

4.  **実行ログの編集**セクションでは、編集機能が**無効になって**いることがわかります。

5.  有効にするには、 **「有効にする**」をクリックしてください。

6.  変更内容を新しいセッションに反映させるには、データベースに再接続してください。
