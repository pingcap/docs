---
title: Encryption at Rest Using Customer-Managed Encryption Keys on Azure
summary: 顧客管理暗号化キー (CMEK) を使用して、Azure でホストされているTiDB Cloudクラスター内のデータを暗号化する方法について説明します。
---

# Azure での顧客管理の暗号化キーを使用した保存時の暗号化 {#encryption-at-rest-using-customer-managed-encryption-keys-on-azure}

顧客管理暗号鍵（CMEK）を使用すると、完全に管理可能な対称暗号鍵を利用して、 TiDB Cloud Dedicated クラスタ内の静的データを保護できます。この鍵はCMEK鍵と呼ばれます。

プロジェクトでCMEKを有効にすると、そのプロジェクト内で作成されるすべてのクラスタは、CMEK鍵を使用して静的データを暗号化します。さらに、これらのクラスタによって生成されるバックアップデータも同じ鍵を使用して暗号化されます。CMEKが有効になっていない場合、 TiDB Cloudはエスクロー鍵を使用して、クラスタ内のすべての保存データを暗号化します。

## 制限 {#restrictions}

-   現在、 TiDB Cloud はCMEK を提供するために AWS KMS と Azure Key Vault の使用のみをサポートしています。
-   CMEK を使用するには、プロジェクトの作成時に CMEK を有効にし、クラスタを作成する前に CMEK 関連の設定を完了する必要があります。既存のプロジェクトでは CMEK を有効にできません。
-   現在、CMEK 対応プロジェクトでは、AWS と Azure でホストされるクラスターを[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)つだけ作成できます。
-   現在、CMEK 対応プロジェクトでは、 [デュアルリージョンバックアップ](/tidb-cloud/backup-and-restore-concepts.md#dual-region-backup)サポートされていません。
-   現在、CMEK 対応プロジェクトでは、AWS と Azure で CMEK を有効化できます。クラウドプロバイダーごとに、リージョンごとに 1 つの固有の暗号化キーを設定できます。選択したクラウドプロバイダーの暗号化キーを設定したリージョンでのみ、クラスタを作成できます。

## CMEKを有効にする {#enable-cmek}

アカウントが所有する暗号化キーを使用してデータを暗号化する場合は、次の手順を実行します。

### ステップ 1. CMEK 対応プロジェクトを作成する {#step-1-create-a-cmek-enabled-project}

組織で`Organization Owner`ロールを担っている場合は、次の手順を実行して CMEK 対応プロジェクトを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用して対象の組織に切り替えます。
2.  左側のナビゲーション ペインで、 **[プロジェクト]**をクリックします。
3.  **「プロジェクト」**ページで、右上隅の**「新しいプロジェクトの作成」を**クリックします。
4.  プロジェクト名を入力してください。
5.  プロジェクトの CMEK 機能を有効にすることを選択します。
6.  **「確認」**をクリックしてプロジェクトの作成を完了します。

### ステップ2. プロジェクトのCMEK構成を完了する {#step-2-complete-the-cmek-configuration-of-the-project}

Azure Portal または Azure Resource Manager のいずれかでTiDB Cloudコンソールを使用して、プロジェクトの CMEK 構成を完了できます。

> **注記：**
>
> -   キーのポリシーが要件を満たしており、権限不足やアカウントの問題などのエラーがないことを確認してください。これらのエラーがあると、このキーを使用してクラスターが誤って作成される可能性があります。
> -   Azure マネージド ディスクのクロステナント カスタマー マネージド キー (CMK) 機能は現在プレビュー段階であり、一部の Azure リージョンでのみご利用いただけます。現在、サポート対象は可用性リージョンのみです。詳細については、 [テナント間の顧客管理キーを使用してマネージド ディスクを暗号化する](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-cross-tenant-customer-managed-keys?tabs=azure-portal#preview-regional-availability)ご覧ください。

<SimpleTab groupId="method">
<div label="Use Azure portal" value="console">

TiDB Cloudコンソールと Azure ポータルを使用して CMEK を構成するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[暗号化アクセス]**をクリックします。

3.  **[暗号化アクセス]**ページで、 **[暗号化キーの作成] を**クリックします。

4.  **[キー管理サービス**] で**[Azure Key Vault]**を選択し、暗号化キーが使用されるリージョンを選択します。

5.  TiDB が提供するエンタープライズ アプリケーションのサービス プリンシパルがテナント内にまだ存在しない場合は、作成してください。TiDB TiDB Cloudコンソールに**Microsoft Entra アプリケーション名**と**ID**が表示されます。これらは、このプロセスと以降の手順で必要になります。サービス プリンシパルを作成するには、 **「サービス プリンシパルの作成」**セクションから次のコマンドを実行します。

    ```shell
    az ad sp create --id {Microsoft_Entra_Application_ID}
    ```

    詳細については[Microsoft Entra ID のアプリケーションおよびサービス プリンシパル オブジェクト](https://learn.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)参照してください。

6.  AzureアカウントでKey Vaultを作成するか、既存のKey Vaultを選択します。以下の点を確認してください。

    -   **パージ保護**が有効になっています。
    -   **リージョンは**クラスターのリージョンと一致します。

7.  TiDB Cloudコンソールで、Key Vault 名とキー名を入力します。TiDB TiDB Cloud は、セキュリティ強化のため、キー名に一意のサフィックスを追加します。キー名全体をコピーし、Azure ポータルで暗号化キーを作成します。詳細については、 [暗号化キーを作成する](https://learn.microsoft.com/en-us/azure/key-vault/keys/quick-create-portal)参照してください。

8.  現在のユーザーに**Key Vault Crypto Officer**ロールを割り当てます。

    1.  [Azureポータル](https://portal.azure.com/)で、Key Vault に移動します。
    2.  **[アクセス制御 (IAM)]**をクリックし、 **[追加]** &gt; **[ロール割り当ての追加]**をクリックします。
    3.  **Key Vault Crypto Officer**ロールを検索して選択し、 **[次へ]**をクリックします。
    4.  [**メンバー]**タブで、 **[アクセスの割り当て先] を****[ユーザー、グループ、またはサービス プリンシパル]**に設定します。
    5.  **「+メンバーを選択」**をクリックし、現在のユーザーを検索してメンバーとして選択します。次に、 **「選択」**をクリックします。
    6.  設定を確認し、 **[確認 + 割り当て]**をクリックします。

9.  暗号化キー用の TiDB 提供エンタープライズ アプリケーションに**Key Vault Crypto Service 暗号化ユーザー**ロールを割り当てます。

    1.  Key Vault で、作成した暗号化キー オブジェクトに移動します。
    2.  **[追加]** &gt; **[ロールの割り当ての追加] を**クリックします。
    3.  **Key Vault Crypto Service 暗号化ユーザー**ロールを検索して選択し、 **[次へ]**をクリックします。
    4.  [**メンバー]**タブで、 **[アクセスの割り当て先] を****[ユーザー、グループ、またはサービス プリンシパル]**に設定します。
    5.  **「+ メンバーを選択」を**クリックし、TiDB が提供する**エンタープライズアプリケーション名**を入力して、メンバーとして選択します。次に、 **「選択」**をクリックします。
    6.  構成を確認し、 **「確認 + 割り当て」**をクリックします。

10. TiDB Cloudコンソールで、 **「暗号化キーのテストと作成」**をクリックして構成を検証し、暗号化キーを作成します。

</div>
<div label="Use Azure Resource Manager" value="arm">

TiDB Cloudコンソールと Azure Resource Manager を使用して CMEK を構成するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)では、左上隅のコンボ ボックスを使用して、対象のプロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[暗号化アクセス]**に移動します。

3.  **[暗号化アクセス]**ページで、 **[暗号化キーの作成] を**クリックします。

4.  **[キー管理サービス]**で**[Azure Key Vault]**を選択し、暗号化キーが使用可能なリージョンを指定します。

5.  TiDB が提供するエンタープライズ アプリケーションのサービス プリンシパルがテナント内にまだ存在しない場合は、作成してください。サービス プリンシパルを作成するには、 **「サービス プリンシパルの作成」**セクションから次のコマンドを実行します。

    ```shell
    az ad sp create --id {Microsoft_Entra_Application_ID}
    ```

    詳細については[Microsoft Entra ID のアプリケーションおよびサービス プリンシパル オブジェクト](https://learn.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)参照してください。

6.  Azureポータルで[Azure Resource Manager 用の TiDB カスタム デプロイメント テンプレート](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Ftcidm.blob.core.windows.net%2Fcmek%2Fazure_cmek_rmt.json%3Fsv%3D2015-04-05%26ss%3Db%26srt%3Dco%26sp%3Drl%26se%3D2029-03-01T00%3A00%3A01.0000000Z%26sig%3DIA02CymcFpYCwoTsqCSJVD%2F8Khh%2F0UAPrkKDeLMIIFc%3D)開きます。**サブスクリプション**と**リソースグループ**を選択し、 **「インスタンスの詳細」**セクションに次のように入力します。

    -   **リージョン**: Key Vault を作成する場所を選択します。これはクラスターのリージョンと一致する必要があります。
    -   **Key Vault 名**: Azure Key Vault の名前を入力します。
    -   **キー名**: Key Vaultに作成するキーの完全な名前を入力します。TiDB TiDB Cloudコンソールでキー名のプレフィックスを入力し、 **「コピー」**をクリックすると、キーの完全な名前が表示されます。
    -   **エンタープライズアプリのサービスプリンシパルID** : TiDBが提供するエンタープライズアプリケーションのサービスプリンシパルIDを入力します。**サービスプリンシパルID**を取得するには、次のコマンドを実行します（ `{microsoft_enterprise_app_id}`はTiDB Cloudコンソールに表示される実際のIDに置き換えてください）。

    ```shell
    az ad sp show --id {microsoft_enterprise_app_id} --query id -o tsv
    ```

</div>
</SimpleTab>

> **注記：**
>
> この機能は今後さらに強化される予定であり、今後の機能には追加の権限が必要になる可能性があります。そのため、このポリシー要件は変更される可能性があります。

### ステップ3. クラスターを作成する {#step-3-create-a-cluster}

[ステップ1](#step-1-create-a-cmek-enabled-project)で作成したプロジェクトの下に、Azure でホストされるTiDB Cloud Dedicated クラスターを作成します。詳細な手順については、 [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

クラウドプロバイダーとリージョンを選択すると、適切な暗号化キーが自動的に選択されます。プロバイダーとリージョンで利用可能な暗号化キーがない場合は、コンソールに暗号化キーの作成に役立つヒントが表示されます。

> **注記：**
>
> CMEK が有効になっている場合、 TiDB Cloud は、クラスター ノードで使用される Premium SSD v2 とクラスター バックアップ用のstorageBLOB の両方を CMEK で暗号化します。

## CMEKを回転させる {#rotate-cmek}

Azure Key Vaultで[暗号鍵の自動ローテーション](https://learn.microsoft.com/en-us/azure/key-vault/keys/how-to-configure-key-rotation)設定できます。このローテーションを有効にすると、 TiDB Cloudのプロジェクト設定で**暗号化アクセス**を更新する必要はありません。

## CMEK を無効にして再度有効にする {#disable-and-re-enable-cmek}

TiDB Cloud の CMEK へのアクセスを一時的に取り消す必要がある場合は、次の手順に従います。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクト内の対応するクラスターを一時停止します。
2.  Azure Key Vault コンソールで、暗号化キーを右クリックし、 **[無効]**を選択します。

> **注記：**
>
> Azure Key Vault で CMEK を無効にすると、実行中のクラスターは CMEK にアクセスできなくなるため、数分以内に使用できなくなります。

TiDB Cloud の CMEK へのアクセスを無効にした後、アクセスを復元する必要がある場合は、次の手順に従います。

1.  Azure Key Vault コンソールで、暗号化キーを選択し、 **[有効化]**をクリックします。
2.  TiDB Cloudコンソールで、プロジェクト内の対応するクラスターを復元します。
