---
title: User-Controlled Log Redaction
summary: 実行ログ内の機密データの可視性を管理するために、 TiDB Cloudでユーザー制御のログ編集を有効または無効にする方法を学習します。
---

# ユーザー制御のログ編集 {#user-controlled-log-redaction}

ユーザー制御のログ編集により、機密データの可視性を管理できます。<customcontent plan="dedicated"> [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスター</customcontent><customcontent plan="premium">TiDB Cloud Premiumインスタンス</customcontent>ログ。この編集機能を切り替えることで、情報を保護し、運用上のニーズとセキュリティのバランスを取り、ログに表示される内容を制御できます。<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>ログ。

ログ編集はデフォルトで有効になっており、実行ログや実行計画内の機密情報が隠蔽されます。より詳細なログ情報が必要な場合は、<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>メンテナンスや SQL チューニングのため、この機能はいつでも無効にできます。

<CustomContent plan="dedicated">

> **注記：**
>
> ログ編集機能は、 TiDB Cloud Dedicated クラスターでのみサポートされます。

</CustomContent>

<CustomContent plan="premium">

> **注記：**
>
> ログ編集機能は、 TiDB Cloud Dedicated クラスターとTiDB Cloud Premium インスタンスでサポートされています。

</CustomContent>

## 前提条件 {#prerequisites}

<CustomContent plan="dedicated">

-   TiDB Cloudで組織の**組織所有者**または**プロジェクト所有者**の役割を持っている必要があります。
-   クラスターが`paused`状態にある場合、ログ編集を有効または無効にすることはできません。

</CustomContent>

<CustomContent plan="premium">

-   TiDB Cloudで組織の**組織所有者**の役割を持っている必要があります。

</CustomContent>

## ログ編集を無効にする {#disable-log-redaction}

> **警告：**
>
> ログ編集を無効にすると、機密情報が漏洩し、データ漏洩のリスクが高まる可能性があります。続行する前に、このリスクを十分に理解し、認識していることを確認してください。診断またはメンテナンスタスクを完了したら、すぐにログ編集を再度有効にしてください。

ログ編集を無効にするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。

2.  に移動<customcontent plan="dedicated">[**クラスター**](https://tidbcloud.com/project/clusters)</customcontent><customcontent plan="premium"> [**TiDBインスタンス**](https://tidbcloud.com/tidbs)</customcontent>ページに移動し、ターゲットの名前をクリックします<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>概要ページに移動します。

    <CustomContent plan="dedicated">

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    </CustomContent>

    <CustomContent plan="premium">

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織とインスタンスを切り替えることができます。

    </CustomContent>

3.  左側のナビゲーション ペインで、 **[設定]** &gt; **[Security]**をクリックします。

4.  **実行ログの編集**セクションでは、編集機能がデフォルトで**有効になっている**ことがわかります。

5.  **「無効にする」**をクリックします。ログ編集を無効にすることのリスクを説明する警告が表示されます。

6.  無効化を確認します。

ログ編集を無効にした後、次の点に注意してください。

-   変更は新しいデータベース接続にのみ適用されます。
-   既存の接続は影響を受けません。変更を有効にするには、再接続する必要があります。
-   新しいセッションのログは編集されなくなります。

## 更新されたログを確認する {#check-the-updated-logs}

ログ編集を無効にした後で更新されたログを確認するには、次の手順を実行します。

1.  遅いクエリによって発生するパフォーマンスの問題をシミュレートします。例えば、次のSQL文を実行します。

    ```sql
    SELECT *, SLEEP(2) FROM users WHERE email LIKE "%useremail%";
    ```

2.  スロークエリログが更新されるまで数分間お待ちください。

3.  ログを確認して、機密データが編集されていないことを確認します。

## ログ編集を有効にする {#enable-log-redaction}

データのセキュリティを維持するために、次のように診断またはメンテナンス タスクを完了したらすぐに**ログ編集を有効にします**。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。

2.  に移動<customcontent plan="dedicated">[**クラスター**](https://tidbcloud.com/project/clusters)</customcontent><customcontent plan="premium"> [**TiDBインスタンス**](https://tidbcloud.com/tidbs)</customcontent>ページに移動し、ターゲットの名前をクリックします<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>概要ページに移動します。

    <CustomContent plan="dedicated">

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

    </CustomContent>

    <CustomContent plan="premium">

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織とインスタンスを切り替えることができます。

    </CustomContent>

3.  左側のナビゲーション ペインで、 **[設定]** &gt; **[Security]**をクリックします。

4.  **実行ログの編集**セクションでは、編集機能が**無効になって**いることがわかります。

5.  有効にするには、 **[有効]**をクリックします。

6.  新しいセッションで変更を有効にするには、データベースに再接続します。
