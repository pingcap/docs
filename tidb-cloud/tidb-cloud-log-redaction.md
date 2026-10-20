---
title: User-Controlled Log Redaction
summary: TiDB Cloudでユーザーが制御するログのマスキングを有効または無効にする方法を学び、実行ログ内の機密データの可視性を管理しましょう。
---

# ユーザーによるログの秘匿化 {#user-controlled-log-redaction}

ユーザー制御のログ秘匿化により、<CustomContent plan="dedicated">[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスター</CustomContent><CustomContent plan="premium,byoc">{{{ .premium }}} または {{{ .byoc }}} インスタンス</CustomContent>のログ内の機密データの可視性を管理できます。この秘匿化機能を切り替えることで、情報を保護し、運用上のニーズとセキュリティのバランスを取り、<CustomContent plan="dedicated">{{{ .dedicated }}} クラスター</CustomContent><CustomContent plan="premium,byoc">{{{ .premium }}} または {{{ .byoc }}} インスタンス</CustomContent>のログに表示される内容を制御できます。

ログのマスキングはデフォルトで有効になっており、実行ログや実行計画内の機密情報が隠蔽されます。<CustomContent plan="dedicated">{{{ .dedicated }}} クラスター</CustomContent><CustomContent plan="premium,byoc">{{{ .premium }}} または {{{ .byoc }}} インスタンス</CustomContent>のメンテナンスや SQL チューニングのために、より詳細なログ情報が必要な場合は、この機能をいつでも無効にできます。

> **Note:**
>
> ログの秘匿化機能は、TiDB Cloud Dedicated クラスター、{{{ .premium }}} インスタンス、および {{{ .byoc }}} インスタンスでサポートされています。

## 前提条件 {#prerequisites}

<CustomContent plan="dedicated">

- TiDB Cloudでは、組織の**Organization Owner**または**Project Owner**の役割を担っている必要があります。
- TiDB Cloud Dedicatedクラスターが`paused`状態にある場合、ログのマスキングを有効または無効にできません。

</CustomContent>

<CustomContent plan="premium,byoc">

- TiDB Cloudにおいて、組織の**Organization Owner**の役割を担っている必要があります。

</CustomContent>

## ログの秘匿化を無効にする {#disable-log-redaction}

> **Warning:**
>
> ログの秘匿化を無効にすると、機密情報が公開され、データ漏洩のリスクが高まる可能性があります。続行する前に、このリスクを理解し、認識していることを確認してください。診断またはメンテナンス作業が完了したら、できるだけ早く再度有効にしてください。

ログの秘匿化を無効にするには、次の手順を実行します。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。
2. [**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象の<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium,byoc">{{{ .premium }}} または {{{ .byoc }}} インスタンス</CustomContent>の名前をクリックして、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず対象の組織に切り替えてください。

3. 左側のナビゲーションペインで、**Settings** > **Security**をクリックします。
4. **Execution Log Redaction**セクションで、秘匿化機能がデフォルトで**Enabled**になっていることを確認できます。
5. **Disable**をクリックします。ログの秘匿化を無効にするリスクを説明する警告が表示されます。
6. 無効化を確認します。

ログの秘匿化を無効にした後は、次の点に注意してください。

* この変更は、新しいデータベース接続にのみ適用されます。
* 既存の接続には影響しません。変更を有効にするには、再接続する必要があります。
* 新しいセッションのログは秘匿化されなくなります。

## 更新されたログを確認してください {#check-the-updated-logs}

ログのマスキングが無効になった後に更新されたログを確認するには、次の手順を実行します。

1. クエリの実行速度が遅いことが原因で発生するパフォーマンスの問題をシミュレートします。たとえば、次の SQL文を実行します。

    ```sql
    SELECT *, SLEEP(2) FROM users WHERE email LIKE "%useremail%";
    ```

2. スロークエリログが更新されるまで数分お待ちください。

3. ログを確認して、機密データが秘匿化されていないことを確認してください。

## ログの秘匿化を有効にする {#enable-log-redaction}

データセキュリティを維持するため、診断またはメンテナンス作業が完了したら、次のように**ログの秘匿化を有効に**してください。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。
2. [**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象の<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium,byoc">{{{ .premium }}} または {{{ .byoc }}} インスタンス</CustomContent>の名前をクリックして、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず対象の組織に切り替えてください。

3. 左側のナビゲーションペインで、**Settings** > **Security**をクリックします。
4. **Execution Log Redaction**セクションで、秘匿化機能が**Disabled**になっていることを確認できます。
5. 有効にするには、**Enable**をクリックします。
6. 変更を新しいセッションに反映させるには、データベースに再接続します。
