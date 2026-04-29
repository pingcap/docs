---
title: Manage TiDB Cloud Resources and Projects
summary: TiDB Cloudのリソースとプロジェクトの管理方法については、「マイTiDB」ページをご覧ください。
---

# TiDB Cloudのリソースとプロジェクトを管理する {#manage-tidb-cloud-resources-and-projects}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、[**私のTiDB**](https://tidbcloud.com/tidbs)ページで組織内のすべてのTiDB Cloudリソースとプロジェクトを検出、アクセス、管理できます。

## TiDB Cloudのリソースとプロジェクトとは何ですか？ {#what-are-tidb-cloud-resources-and-projects}

### TiDB Cloudのリソース {#tidb-cloud-resources}

TiDB Cloudのリソースは、管理可能なデプロイ可能な単位です。以下のいずれかになります。

-   TiDB Xインスタンスは、 [TiDB Xアーキテクチャ](/tidb-cloud/tidb-x-architecture.md)上に構築されたサービス指向のTiDB Cloud製品です。TiDB TiDB Cloud Starter、 Essential、またはPremiumインスタンスなど。
-   TiDB Cloud Dedicatedクラスター

### TiDB Cloudプロジェクト {#tidb-cloud-projects}

TiDB Cloudでは、 [プロジェクト](/tidb-cloud/tidb-cloud-glossary.md#project)を使用してTiDB Cloudリソースを整理および管理できます。

-   TiDB Xインスタンスの場合、プロジェクトはオプションです。つまり、これらのインスタンスをプロジェクトにグループ化することも、組織レベルで管理することもできます。
-   TiDB Cloud Dedicatedクラスターの場合、プロジェクトが必要です。

## TiDB Cloudのリソースを管理する {#manage-tidb-cloud-resources}

このセクションでは[**私のTiDB**](https://tidbcloud.com/tidbs)ページを使用してTiDB Cloudのリソースを表示、作成、管理する方法について説明します。

### TiDB Cloudのリソースをビュー {#view-tidb-cloud-resources}

デフォルトでは、[**私のTiDB**](https://tidbcloud.com/tidbs)ページにはリソースビューが表示され、現在の組織内でアクセス権限を持つすべてのリソースが表示されます。

組織内に多数のインスタンスやクラスターがある場合は、ページ上部のフィルターを使用して必要なものをすばやく見つけることができます。

TiDB Cloudリソースの詳細情報を表示するには、対象のリソース名をクリックして概要ページに移動してください。

### TiDB Cloudリソースを作成する {#create-tidb-cloud-resources}

TiDB Cloudリソースを作成するには、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[リソースの作成] を**クリックします。

詳細については、以下の資料を参照してください。

-   [TiDB Cloud StarterまたはEssentialインスタンスを作成します。](/tidb-cloud/create-tidb-cluster-serverless.md)

-   [TiDB Cloud Premiumインスタンスを作成する](/tidb-cloud/premium/create-tidb-instance-premium.md)

-   [TiDB Cloud Dedicatedクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)

### TiDB Cloudのリソースを管理する {#manage-tidb-cloud-resources}

**「マイ TiDB」**ページでは、対象リソースの行にある**「...」**をクリックすることで、 TiDB Cloudリソースに対して、データの削除、名前変更、インポートなどのクイックアクションを実行できます。

特定のTiDB Cloudリソースに対してより多くの操作を実行したり、設定を管理したりするには、対象のリソース名をクリックして概要ページに移動してください。

## TiDB Cloudプロジェクトを管理する {#manage-tidb-cloud-projects}

このセクションでは[**私のTiDB**](https://tidbcloud.com/tidbs)ページを使用してTiDB Cloudプロジェクトを表示、作成、管理する方法について説明します。

### プロジェクトをビュー {#view-projects}

TiDB Cloudのリソースをプロジェクトごとにグループ化して表示するには、[**私のTiDB**](https://tidbcloud.com/tidbs)ページの**「プロジェクトビュー」**タブをクリックします。

> **ヒント：**
>
> 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

プロジェクトビューでは、組織内で自分が所属しているプロジェクトを確認できます。

-   どのプロジェクトにも属さない TiDB X インスタンスは`Out of project`という名前のテーブルに表示されます。
-   特定のプロジェクトに属するTiDB Xインスタンスは、対応するTiDB Xプロジェクトテーブルに表示されます。
-   TiDB Cloud Dedicatedクラスターは、対応するDedicatedプロジェクトテーブルに表示されます。これらのテーブルのフォルダーアイコンには、**Dedicated**プロジェクトの種類を示す**「D」**の文字が付いています。

### プロジェクトを作成する {#create-a-project}

> **注記：**
>
> -   無料トライアルユーザーは新規プロジェクトを作成できません。
> -   TiDB Xインスタンスの場合、プロジェクトの作成は任意です。TiDB TiDB Cloud Dedicatedクラスタの場合は、デフォルトのプロジェクトを使用するか、新しいプロジェクトを作成して管理する必要があります。

`Organization Owner`の役割をお持ちの場合は、組織内でプロジェクトを作成できます。

新しいプロジェクトを作成するには、以下の手順に従ってください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **「プロジェクトの作成」を**クリックします。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  表示されたダイアログにプロジェクト名を入力してください。

3.  プロジェクトを作成する対象となるTiDB Cloudリソースの種類に応じて、次のいずれかの操作を行います。

    -   プロジェクトが TiDB X インスタンス用に作成されている場合は、 **[確認]**をクリックします。

        > **注記：**
        >
        > TiDB Cloud Premium インスタンスの場合、暗号化はプロジェクトごとではなくインスタンスごとに構成されます。インスタンスを作成した後、 [二重層データ暗号化](/tidb-cloud/premium/dual-layer-data-encryption-premium.md)有効にして、デフォルトのストレージ層の暗号化に加えてデータベース層の暗号化を追加できます。

    -   プロジェクトがTiDB Cloud Dedicatedクラスター用に作成されている場合は、 **「Dedicatedクラスタ用に作成」**オプションを選択し、プロジェクトの [顧客管理型暗号化キー（CMEK）](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)と[メンテナンスウィンドウ](/tidb-cloud/configure-maintenance-window.md)を構成して、 **「確認」**をクリックします。

### プロジェクトを管理する {#manage-a-project}

`Organization Owner`または`Project Owner`の役割を担っている場合は、プロジェクトを管理できます。

プロジェクトを管理するには、以下の手順に従ってください。

1.  TiDB Cloudコンソールで、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  プロジェクトビューで、対象のプロジェクトを見つけて、次のように管理します。

    -   TiDB X プロジェクトとTiDB Dedicatedプロジェクトの両方で、ターゲット プロジェクトの行にある**[...]**をクリックして、プロジェクトの名前変更やプロジェクトへのメンバーの招待など、プロジェクトに対してクイック アクションを実行できます。詳細については、[プロジェクトへのアクセスを管理する](/tidb-cloud/manage-user-access.md)参照してください。
    -   TiDB Dedicatedプロジェクトの場合、対象プロジェクトの行にある<MDSvgIcon name="icon-project-settings" />アイコンをクリックすると、プロジェクトごとにTiDB Cloud Dedicatedクラスターのネットワーク、メンテナンス、アラートの購読、暗号化アクセスなどの設定を管理できます。

### TiDB Xインスタンスをプロジェクト間で移動する {#move-a-tidb-x-instance-between-projects}

`Organization Owner`または`Project Owner`の役割を担っている場合、TiDB X インスタンスをプロジェクトに移動したり、任意のプロジェクトから移動したりできます。

> **注記：**
>
> TiDB Xインスタンスのみが、TiDB Xプロジェクト間の移動およびTiDB Xプロジェクトからの離脱をサポートしています。TiDB TiDB Cloud Dedicatedクラスタは、プロジェクト間の移動をサポートしていません。

TiDB Xインスタンスを移動するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

2.  プロジェクトビューで、移動する TiDB X インスタンスを含むプロジェクトフォルダーを展開し、対象の TiDB X インスタンスの**...**をクリックしてから、 **[移動]**をクリックします。

    > **ヒント：**
    >
    > TiDB Xインスタンスがどのプロジェクトにも含まれていない場合、それは**「プロジェクト外」**フォルダに表示されます。

3.  表示されたダイアログで、次のいずれかの操作を行います。

    -   TiDB Xインスタンスをプロジェクトに移動するには、 **「プロジェクトへ」**を選択し、ドロップダウンリストから対象のプロジェクトを選択します。
    -   TiDB X インスタンスをどのプロジェクトからも移動するには、 **[どのプロジェクトからも移動]**を選択します。

4.  **「移動」**をクリックします。
