---
title: Create a TiDB Cloud Starter or Essential Instance
summary: TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの作成方法を学びましょう。
---

# TiDB Cloud StarterまたはEssentialインスタンスを作成します。 {#create-a-tidb-cloud-starter-or-essential-instance}

このドキュメントでは、[TiDB Cloudコンソール](https://tidbcloud.com/)でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを作成する方法について説明します。

> **Tip:**
>
> TiDB Cloud Dedicatedクラスターを作成する方法については、 [TiDB Cloud Dedicatedクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

## 始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、[ここ](https://tidbcloud.com/signup)をクリックしてアカウントを作成してください。

<CustomContent language="en,zh">

- TiDB Cloudを使用してパスワードを管理できるように、メールアドレスとパスワードで登録するか、Google、GitHub、またはMicrosoftアカウントで登録することができます。
- AWS Marketplace をご利用の方は、AWS Marketplace からサインアップすることもできます。サインアップするには、 [AWS Marketplace](https://aws.amazon.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
- Azure Marketplace をご利用の方は、Azure Marketplace からサインアップすることもできます。サインアップするには、 [Azure Marketplace](https://azuremarketplace.microsoft.com)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
- Google Cloud Marketplace をご利用の方は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
- Alibaba Cloud Marketplace ユーザーの場合は、Alibaba Cloud Marketplace を通じてサインアップすることもできます。これを行うには、[Alibaba Cloud Marketplace](https://marketplace.alibabacloud.com/)で`TiDB Cloud`を検索し、 TiDB Cloudにサブスクライブし、画面上の指示に従ってTiDB Cloudアカウントを設定します。

</CustomContent>

<CustomContent language="ja">

- TiDB Cloudを使用してパスワードを管理できるように、メールアドレスとパスワードで登録するか、Google、GitHub、またはMicrosoftアカウントで登録することができます。
- AWS Marketplace をご利用の方は、AWS Marketplace からサインアップすることもできます。サインアップするには、 [AWS Marketplace](https://aws.amazon.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
- Azure Marketplace をご利用の方は、Azure Marketplace からサインアップすることもできます。サインアップするには、 [Azure Marketplace](https://azuremarketplace.microsoft.com)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
- Google Cloud Marketplace をご利用の方は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。

</CustomContent>

> **Note:**
>
> PostgreSQL互換のTiDB Cloud Starterは現在パブリックプレビューで利用できます。Starterインスタンスの作成時にPostgreSQL互換モードを選択できます。

## 手順 {#steps}

`Organization Owner`または`Project Owner`ロールを持っている場合は、次のようにしてTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを作成できます。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

2. **Create Resource**をクリックします。

3. プランを選択してください。

    **Starter**または**Essential**を選択できます。

    MySQL互換ワークロードの場合は、Starterインスタンスから開始し、後でニーズの増大に応じてEssentialインスタンスにアップグレードできます。詳細については、[プランを選択する](/tidb-cloud/select-cluster-tier.md)をご覧ください。

4. **Starter**を選択した場合は、**Compatibility Mode**セクションで次のいずれかのオプションを選択します。

    - **MySQL Compatible**: TiDB Cloud Starterのデフォルトの互換モードです。
    - **PostgreSQL Compatible**: PostgreSQL互換性を提供し、現在パブリックプレビュー中です。この互換モードはTiDB Cloud Starterでのみ利用できます。

5. インスタンスの名前を入力し、次にインスタンスをホストするクラウドプロバイダーとリージョンを選択してください。

6. （オプション）このインスタンスを管理対象プロジェクトにグループ化するには、 **Group Your Instance in a Project**をクリックし、インスタンスのターゲットプロジェクトを選択します。組織内にプロジェクトがない場合は、 **Create a Project**をクリックして作成できます。

7. 選択したプランと互換モードに基づいて、容量と使用量クォータを設定または確認します。各Starter互換モードの無料使用量クォータについては、[プランを選択する](/tidb-cloud/select-cluster-tier.md#starter)をご覧ください。

    - **MySQL 互換 Starter**:

        - TiDB Cloud Starterインスタンスの利用限度額を更新できます。利用限度額を0に設定すると、インスタンスは無料のままです。利用限度額を0より大きい値に設定する場合は、インスタンスを作成する前にクレジットカードを追加する必要があります。
        - デフォルトでは、各組織は最大5つの無料のMySQL互換Starterインスタンスを作成できます。追加のインスタンスを作成するには、クレジットカードを追加し、利用限度額を指定する必要があります。

    - **PostgreSQL 互換 Starter**:

        パブリックプレビュー期間中、各組織は最大10個の無料のPostgreSQL互換Starterインスタンスを作成できます。

        インスタンスが無料クォータに達すると、過剰なリソース消費に対して使用制限またはサービス停止が適用される場合があります。無料使用量クォータを超えることが予想される場合は、要件について相談するために<a href="mailto:support@pingcap.com">support@pingcap.com</a>までお問い合わせください。

    - **Essential**:

        - CLOUD.202603.x以降で実行されるTiDB Cloud Essentialインスタンスでは、デフォルトで**Elastic Mode**が選択されています。Elastic Modeでは、RCUの最大数を設定しません。代わりに、インスタンスは固定の**Baseline RCU**である2,000 RCUを使用します。これは、課金対象となる最小のリクエストキャパシティユニット（RCU）数であり、自動スケーリングの初期容量でもあります。

        - 容量を制限するには、**Limited Mode**を選択してから、インスタンスがスケールアップできるRCUの最大数を指定します。以前のバージョンのTiDB Cloud EssentialインスタンスはElastic Modeをサポートしていません。これらのインスタンスでは、RCUの最小数と最大数の両方を指定します。

        - RCUは、ワークロード用にプロビジョニングされたコンピューティングリソースを表します。TiDB Cloudは、需要に基づいてTiDB Cloud Essentialインスタンスを自動的にスケーリングします。ワークロードで一貫して100,000 RCUを超える必要がある場合は、潜在的なボトルネックを回避するために{{{ .premium }}}へのアップグレードを検討してください。

8. **Create**をクリックします。

インスタンス作成プロセスが開始され、約30秒でインスタンスが作成されます。

## 次は？ {#what-s-next}

- TiDB Cloud StarterまたはEssentialインスタンスが作成されたら、 [パブリックエンドポイント経由でTiDB Cloudに接続します](/tidb-cloud/connect-via-standard-connection-serverless.md)の手順に従って、インスタンスのパスワードを作成します。

    > **Note:**
    >
    > パスワードを設定しないと、 TiDB Cloud StarterまたはEssentialインスタンスに接続できません。

- TiDB Cloud CLI を使用してインスタンスを管理するには、[TiDB Cloud CLI Reference (PREVIEW)](/tidb-cloud/cli-reference.md) を参照してください。
