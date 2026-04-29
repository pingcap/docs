---
title: TiDB Cloud Billing
summary: TiDB Cloudの課金体系について学びましょう。
---

# TiDB Cloud課金 {#tidb-cloud-billing}

TiDB Cloudは、お客様が使用したリソースに応じて課金されます。

## 価格設定 {#pricing}

### TiDB Cloud Dedicatedの料金プラン {#pricing-for-tidb-cloud-dedicated}

[TiDB Cloud Dedicatedの料金詳細](https://www.pingcap.com/tidb-dedicated-pricing-details/)参照してください。

### TiDB Cloud Starterの料金プラン {#pricing-for-starter} {#pricing-for-starter}

[TiDB Cloud Starterの料金詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)参照してください。

### TiDB Cloud Essentialの価格設定 {#pricing-for-essential} {#pricing-for-essential}

TiDB Cloud Essentialでは、アプリケーションの実際の使用量で**はなく**、プロビジョニングされたリクエスト容量ユニット (RCU) の数に基づいて課金されます。TiDB [TiDB Cloud Essential の価格詳細](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)ご覧ください。

### TiDB Cloud Premium の価格設定 {#pricing-for-premium} {#pricing-for-premium}

TiDB Cloud Premium の場合、基礎となるバックエンド ノードやプロビジョニングされたディスク サイズではなく、実際の[要求容量単位（RCU）](/tidb-cloud/tidb-cloud-glossary.md#request-capacity-unit-rcu)消費量と実際に使用するstorageに基づいて請求されます。 [TiDB Cloud Premiumの料金詳細](https://www.pingcap.com/tidb-cloud-premium-pricing-details/)ご覧ください。

## 請求書 {#invoices}

組織内で`Organization Owner`または`Organization Billing Manager`の役割を担っている場合は、 TiDB Cloudの請求書情報を管理できます。それ以外の場合は、このセクションをスキップしてください。

支払い方法を設定した後、コストが割り当て (デフォルトでは 500 ドル) に達すると、 TiDB Cloud は請求書を生成します。割り当てを引き上げたい場合、または月に 1 回の請求書を受け取りたい場合は、[営業担当者にお問い合わせください](https://www.pingcap.com/contact-us/)。

<CustomContent language="en,zh">

> **注記：**
>
> [AWS Marketplace](https://aws.amazon.com/marketplace) 、 [Azure Marketplace](https://azuremarketplace.microsoft.com/) 、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 、または[アリババクラウドマーケットプレイス](https://marketplace.alibabacloud.com/)Cloud Marketplace を通じてTiDB Cloudにサインアップした場合、AWS アカウント、Azure アカウント、Google Cloud アカウント、または Alibaba Cloud アカウントを通じて直接支払うことはできますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

</CustomContent>

<CustomContent language="ja">

> **注記：**
>
> [AWS Marketplace](https://aws.amazon.com/marketplace) 、 [Azure Marketplace](https://azuremarketplace.microsoft.com/) 、または[Google Cloud Marketplace](https://console.cloud.google.com/marketplace)経由でTiDB Cloudにサインアップした場合、AWSアカウント、Azureアカウント、またはGoogle Cloudアカウントを通じて直接支払いを行うことができますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

</CustomContent>

お客様が弊社の営業担当に連絡して月次請求書の発行を依頼すると、 TiDB Cloudは毎月初めに前月分の請求書を自動的に作成します。

請求金額には、TiDBリソースの使用消費量、割引、バックアップstorage費用、サポートサービス費用、クレジット消費量、および組織内のデータ送信費用が含まれます。

毎月の請求書ごとに：

-   TiDB Cloudは毎月9日に請求書をお送りします。1日から9日までは前月の料金明細は表示できませんが、請求コンソールから当月のリソース使用状況を確認できます。
-   請求書の支払い方法は、原則としてクレジットカードによる引き落としとなります。他の支払い方法をご希望の場合は、チケットリクエストを送信してお知らせください。
-   今月と前月の料金の概要と詳細をご覧いただけます。

> **注記：**
>
> 請求金額の引き落としはすべて、第三者プラットフォームであるStripeを通じて行われます。

請求書の一覧を表示するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。

2.  左側のナビゲーションペインで、 **「請求」**をクリックします。

3.  **請求**ページで、「**請求書」**タブをクリックします。

## 請求明細 {#billing-details}

組織内で`Organization Owner`または`Organization Billing Manager`の役割を担っている場合は、 TiDB Cloudの請求詳細を表示およびエクスポートできます。それ以外の場合は、このセクションをスキップしてください。

支払い方法を設定すると、 TiDB Cloudは過去の月の請求書と請求明細を生成し、毎月初めに当月の請求明細を生成します。請求明細には、組織のTiDBリソース使用量、割引、バックアップstorage費用、データ転送費用、サポートサービス費用、クレジット消費量、プロジェクト分割情報などが含まれます。

> **注記：**
>
> 遅延その他の理由により、当月の請求明細は参考情報であり、正確性を保証するものではありません。TiDB TiDB Cloudは過去の請求書の正確性を保証するため、原価計算やその他のニーズに対応できます。

請求明細を確認するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。

2.  左側のナビゲーションペインで、 **「請求」**をクリックします。

**請求**ページでは、デフォルトで「**請求書」**タブが表示されます。

「**請求書」**タブには、プロジェクト別およびインスタンス別の請求概要と、サービス別の請求概要が表示されます。また、使用状況の詳細を確認したり、データをCSV形式でダウンロードしたりすることもできます。

> **注記：**
>
> 精度の違いにより、月々の請求書の合計金額は日々の使用明細の金額と異なる場合があります。
>
> -   月額請求額の合計は、小数点以下第2位で四捨五入されます。
> -   日ごとの利用明細に記載されている合計金額は、小数点以下第6位まで正確です。

## コストエクスプローラー {#cost-explorer}

組織内で`Organization Owner`または`Organization Billing Manager`の役割を担っている場合は、 TiDB Cloudの使用コストを表示および分析できます。それ以外の場合は、このセクションをスキップしてください。

組織のコストレポートを分析およびカスタマイズするには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
2.  左側のナビゲーションペインで、 **「請求」**をクリックします。
3.  **請求**ページで、 **「コストエクスプローラー」**タブをクリックします。
4.  **コストエクスプローラー**タブで、右上隅の**フィルター**セクションを展開してレポートをカスタマイズします。期間を設定したり、グループ化オプション（サービス、プロジェクト、クラスター、地域、製品タイプ、料金タイプなど）を選択したり、特定のサービス、プロジェクト、クラスター、または地域を選択してフィルターを適用したりできます。コストエクスプローラーには、次の情報が表示されます。

    -   **コストグラフ**：選択した期間におけるコストの推移を視覚化します。**月次**、**日次**、**合計の各**表示を切り替えることができます。
    -   **コスト内訳**：選択したグループ分けオプションに基づいて、コストの詳細な内訳を表示します。さらに分析したい場合は、データをCSV形式でダウンロードできます。

## 請求プロファイル {#billing-profile}

有料会員は請求プロファイルを作成できます。このプロファイルの情報は、税金の計算に使用されます。

組織の請求プロファイルを表示または更新するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
2.  左側のナビゲーションペインで、 **「請求」**をクリックします。
3.  **請求**ページで、 **「請求プロファイル」**タブをクリックします。

請求プロファイルには4つの項目があります。

### 会社名（任意） {#company-name-optional}

この項目を指定すると、請求書には組織名の代わりにこの名前が表示されます。

### 請求用メールアドレス（任意） {#billing-email-optional}

この項目を指定すると、請求書やその他の請求関連の通知がこのメールアドレスに送信されます。

### 主要事業所住所 {#primary-business-address}

これは、 TiDB Cloudサービスを購入する企業の住所です。適用される税金の計算に使用されます。

### 事業税番号（任意） {#business-tax-id-optional}

貴社がVAT/GSTに登録されている場合は、有効なVAT/GST IDを入力してください。この情報をご提供いただくことで、該当する場合、VAT/GSTの課税が免除されます。これは、VAT/GST登録により特定の税金免除または還付が認められる地域で事業を営む企業にとって重要です。

## クレジット {#credits}

TiDB Cloudは、概念実証（PoC）ユーザー向けに一定数のクレジットを提供しています。1クレジットは1米ドルに相当します。クレジットは有効期限が切れる前に、TiDBの利用料金の支払いに使用できます。

> **ヒント：**
>
> PoC を申請するには、 [TiDB Cloudを使用して概念実証（PoC）を実施する](/tidb-cloud/tidb-cloud-poc.md)参照してください。

クレジットに関する詳細情報は、「**クレジット」**タブで確認できます。そこには、合計クレジット数、利用可能なクレジット数、現在の使用状況、およびステータスが含まれます。

信用情報を確認するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
2.  左側のナビゲーションペインで、 **「請求」**をクリックします。
3.  **請求**ページで、 **「クレジット」**タブをクリックします。

> **注記：**
>
> -   お支払い方法を設定すると、リソース使用料はまず未使用のクレジットから差し引かれ、次に設定したお支払い方法から差し引かれます。
> -   クレジットはサポートプランの料金の支払いには使用できません。

> **警告：**
>
> PoCプロセス中：
>
> -   お支払い方法を追加する前にすべてのクレジットが期限切れになった場合、新しいTiDB Cloud Dedicatedクラスターを作成することはできません。3 日後には、既存のすべてのTiDB Cloud Dedicatedクラスターがリサイクルされます。7 日後には、すべてのバックアップがリサイクルされます。処理を再開するには、お支払い方法を追加してください。
> -   支払い方法を追加した後にすべてのクレジットが期限切れになった場合でも、PoCプロセスは続行され、手数料は支払い方法から差し引かれます。

## 割引 {#discounts}

組織内で`Organization Owner`または`Organization Billing Manager`の役割を担っている場合は、 **[割引]**タブでTiDB Cloudの割引情報を確認できます。それ以外の場合は、このセクションをスキップしてください。

割引情報には、お客様が受けたすべての割引、そのステータス、割引率、割引の開始日と終了日が含まれます。

割引情報を確認するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
2.  左側のナビゲーションペインで、 **「請求」**をクリックします。
3.  **請求**ページで、 **「割引」**タブをクリックします。

## 支払方法 {#payment-method}

組織内で`Organization Owner`または`Organization Billing Manager`の役割を担っている場合は、 TiDB Cloudの支払い情報を管理できます。それ以外の場合は、このセクションをスキップしてください。

<CustomContent language="en,zh">

> **注記：**
>
> [AWS Marketplace](https://aws.amazon.com/marketplace) 、 [Azure Marketplace](https://azuremarketplace.microsoft.com/) 、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 、または[アリババクラウドマーケットプレイス](https://marketplace.alibabacloud.com/)Cloud Marketplace を通じてTiDB Cloudにサインアップした場合、AWS アカウント、Azure アカウント、Google Cloud アカウント、または Alibaba Cloud アカウントを通じて直接支払うことはできますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

</CustomContent>

<CustomContent language="ja">

> **注記：**
>
> [AWS Marketplace](https://aws.amazon.com/marketplace) 、 [Azure Marketplace](https://azuremarketplace.microsoft.com/) 、または[Google Cloud Marketplace](https://console.cloud.google.com/marketplace)経由でTiDB Cloudにサインアップした場合、AWSアカウント、Azureアカウント、またはGoogle Cloudアカウントを通じて直接支払いを行うことができますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

</CustomContent>

料金は、ご利用のリソースに応じて、登録済みのクレジットカードから引き落とされます。有効なクレジットカードを追加するには、以下のいずれかの方法をご利用ください。

-   TiDB Cloud Dedicatedクラスターを作成する場合：

    1.  **リソース作成**ページで、 **「クレジットカードを追加」**をクリックします。
    2.  **「カードを追加」**ダイアログで、カード情報と請求先住所を入力してください。
    3.  **「カードを保存」**をクリックしてください。

-   請求コンソールではいつでも：

    1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
    2.  左側のナビゲーションペインで、 **「請求」**をクリックします。
    3.  **請求**ページで、 **「支払い方法」**タブをクリックし、 **「新しいカードを追加」**をクリックします。
    4.  クレジットカード情報とクレジットカードの住所を入力し、 **「カードを保存」**をクリックしてください。

        主要事業所住所を指定しない場合 税金計算には、クレジットカードの住所が主要事業所住所として使用されます。主要事業所住所は[**請求プロファイル**](#billing-profile)**請求プロファイル**でいつでも更新できます。

> **注記：**
>
> クレジットカードの機密データのセキュリティを確保するため、 TiDB Cloudは顧客のクレジットカード情報を一切保存せず、サードパーティの決済プラットフォームであるStripeに保存します。すべての請求処理はStripeを通じて行われます。

複数のクレジットカードを登録し、請求コンソールの支払い方法でそのうちの1枚をデフォルトのクレジットカードとして設定できます。設定後、以降の請求は自動的にデフォルトのクレジットカードから引き落とされます。

デフォルトのクレジットカードを設定するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
2.  左側のナビゲーションペインで、 **「請求」**をクリックします。
3.  **請求**ページで、 **「支払い方法」**タブをクリックします。
4.  クレジットカード一覧からクレジットカードを選択し、デフォルトのクレジットカードとして設定するかどうかを尋ねられたら**「はい」**をクリックしてください。

## 契約 {#contract}

組織内で`Organization Owner`または`Organization Billing Manager`の役割を担っている場合は、 TiDB CloudコンソールでカスタマイズされたTiDB Cloudサブスクリプションを管理して、コンプライアンス要件を満たすことができます。それ以外の場合は、このセクションをスキップしてください。

弊社営業担当者と契約内容について合意し、オンラインで契約内容を確認して承認するためのメールを受け取った場合は、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
2.  左側のナビゲーションペインで、 **「請求」**をクリックします。
3.  **請求**ページで、 **「契約」**タブをクリックします。
4.  「**契約」**タブで、確認したい契約を見つけ、その契約の行にある**「…」**をクリックします。

契約について詳しく知りたい場合は、[営業担当者にお問い合わせください](https://www.pingcap.com/contact-us/)。

## クラウドプロバイダーマーケットプレイスからの請求 {#billing-from-cloud-provider-marketplace}

<CustomContent language="en,zh">

組織内で`Organization Owner`または`Organization Billing Manager`の役割を担っている場合は、 TiDB Cloudアカウントをクラウド プロバイダー (AWS、Azure、Google Cloud、または Alibaba Cloud) の請求アカウントにリンクできます。それ以外の場合は、このセクションをスキップしてください。

</CustomContent>

<CustomContent language="ja">

組織内で`Organization Owner`または`Organization Billing Manager`の役割を担っている場合は、 TiDB Cloudアカウントをクラウド プロバイダー (AWS、Azure、または Google Cloud) の請求アカウントにリンクできます。それ以外の場合は、このセクションをスキップしてください。

</CustomContent>

TiDB Cloudを初めてご利用になる方で、 TiDB Cloudアカウントをお持ちでない場合は、ご利用のクラウドプロバイダーのマーケットプレイスからTiDB Cloudアカウントに登録し、クラウドプロバイダーの請求アカウントを通じて利用料金をお支払いいただけます。

<CustomContent language="en,zh">

-   [AWS Marketplace](https://aws.amazon.com/marketplace)からサインアップするには、 [AWS Marketplace](https://aws.amazon.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   [Azure Marketplace](https://azuremarketplace.microsoft.com)からサインアップするには、 [Azure Marketplace](https://azuremarketplace.microsoft.com)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)からサインアップするには、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   [アリババクラウドマーケットプレイス](https://marketplace.alibabacloud.com/)[アリババクラウドマーケットプレイス](https://marketplace.alibabacloud.com/)`TiDB Cloud`を検索し、 TiDB Cloudにサブスクライブし、画面上の指示に従ってTiDB Cloudアカウントを設定します。

既にTiDB Cloudアカウントをお持ちで、AWS、Azure、Google Cloud、またはAlibaba Cloudの請求アカウントを通じて利用料金を支払いたい場合は、 TiDB CloudアカウントをAWS、Azure、Google Cloud、またはAlibaba Cloudの請求アカウントにリンクできます。

</CustomContent>

<CustomContent language="ja">

-   [AWS Marketplace](https://aws.amazon.com/marketplace)からサインアップするには、 [AWS Marketplace](https://aws.amazon.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   [Azure Marketplace](https://azuremarketplace.microsoft.com)からサインアップするには、 [Azure Marketplace](https://azuremarketplace.microsoft.com)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)からサインアップするには、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。

既にTiDB Cloudアカウントをお持ちで、AWS、Azure、またはGoogle Cloudの請求アカウントを通じて利用料金を支払いたい場合は、 TiDB CloudアカウントをAWS、Azure、またはGoogle Cloudの請求アカウントにリンクできます。

</CustomContent>

<SimpleTab>
<div label="AWS Marketplace">

TiDB CloudアカウントをAWSの請求アカウントにリンクするには、以下の手順に従ってください。

1.  [AWS Marketplaceページ](https://aws.amazon.com/marketplace)を開き、 `TiDB Cloud`を検索して、検索結果から**TiDB Cloud**を選択します。TiDB TiDB Cloud の製品ページが表示されます。

2.  TiDB Cloud製品ページで、 **「購読を続ける」を**クリックします。注文ページが表示されます。

3.  注文ページで**「購読」**をクリックし、次に**「アカウントの設定」を**クリックしてください。TiDB TiDB Cloudのサインアップページに移動します。

4.  サインアップページの上部にある通知を確認し、 **「サインイン」**をクリックしてください。

5.  TiDB Cloudアカウントでサインインしてください。AWS**請求アカウントへのリンクページ**が表示されます。

6.  **「AWS請求アカウントへのリンク」**ページで、対象の組織を選択し、 **「リンク」**をクリックしてAWS請求アカウントにリンクします。

    > **注記：**
    >
    > 組織が既にTiDB Cloudで支払い方法を登録している場合、その組織の既存の支払い方法は、新たに追加されたAWS請求アカウントに置き換えられます。

</div>

<div label="Azure Marketplace">

TiDB CloudアカウントをAzureの請求アカウントにリンクするには、以下の手順に従ってください。

1.  [Azure Marketplace ページ](https://azuremarketplace.microsoft.com)を開き、 `TiDB Cloud`を検索して、検索結果から**TiDB Cloud on Azure (プレビュー)**を選択します。TiDB TiDB Cloud の製品ページが表示されます。

2.  TiDB Cloud製品ページで、 **「今すぐ入手」**をクリックし、利用規約に同意してから、 **「続行」**をクリックして注文ページに進んでください。

    > **注記：**
    >
    > Microsoft アカウントに国と地域の情報を追加していない場合は、 **[続行]**をクリックする前にその情報を入力する必要があります。

3.  注文ページで**「購読」**をクリックし、 **「基本情報」**タブで必要な情報を入力してから、 **「確認＋購読」**をクリックします。内容に問題がなければ**「購読」**をクリックし、購読が完了するまで数秒お待ちください。

4.  購読手続きが完了したら、 **「アカウント設定」**をクリックしてください。TiDB TiDB Cloudのサインアップページに移動します。

5.  サインアップページの上部にある通知を確認し、 **「サインイン」**をクリックしてください。

6.  TiDB Cloudアカウントでサインインしてください。Azure**請求アカウントへのリンクページ**が表示されます。

7.  **「Azure 請求アカウントへのリンク」**ページで、対象の組織を選択し、 **「リンク」**をクリックして AWS 請求アカウントにリンクします。

    > **注記：**
    >
    > 組織が既にTiDB Cloudで支払い方法を登録している場合、その組織の既存の支払い方法は、新たに追加されたAzure請求アカウントに置き換えられます。

</div>

<div label="Google Cloud Marketplace">

TiDB CloudアカウントをGoogle Cloudの請求アカウントにリンクするには、以下の手順に従ってください。

1.  [Google Cloud Marketplace のページ](https://console.cloud.google.com/marketplace)を開きます`TiDB Cloud`を検索し、検索結果から**TiDB Cloud**を選択します。TiDB TiDB Cloudの製品ページが表示されます。

2.  TiDB Cloud製品ページで、 **「購読」**をクリックします。購読ページが表示されます。

3.  購読ページで**「購読」**をクリックし、次に**「製品ページへ移動」**をクリックします。TiDB TiDB Cloudのサインアップページに移動します。

4.  サインアップページの上部にある通知を確認し、 **「サインイン」**をクリックしてください。

5.  TiDB Cloudアカウントでサインインしてください。Google Cloudの請求アカウントにリンクするためのページが表示されます。

6.  ページ上で対象の組織を選択し、 **「リンク」**をクリックしてGoogle Cloudの請求アカウントにリンクします。

    > **注記：**
    >
    > 組織が既にTiDB Cloudで支払い方法を登録している場合、その組織の既存の支払い方法は、新たに追加されたGoogle Cloudの請求アカウントに置き換えられます。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud Marketplace">

TiDB CloudアカウントをAlibaba Cloudの請求アカウントにリンクするには、以下の手順に従ってください。

1.  [アリババクラウドマーケットプレイスページ](https://marketplace.alibabacloud.com/)ページを開き、 `TiDB Cloud`を検索し、検索結果から**TiDB Cloud**を選択します。 TiDB Cloudの製品ページが表示されます。

2.  TiDB Cloud製品ページで**「今すぐ有効化」**をクリックし、画面の指示に従って従量課金モードを確認し、有効化アプリケーションを表示します。

3.  購読ページで、 TiDB Cloudの購読情報を探し、 **「自動ログイン」**をクリックしてください。TiDB TiDB Cloudのサインアップページに移動します。

4.  サインアップページの上部にある通知を確認し、 **「サインイン」**をクリックしてください。

5.  TiDB Cloudアカウントでサインインしてください。Alibaba Cloudの請求アカウントにリンクするためのページが表示されます。

6.  ページ上で対象の組織を選択し、 **「リンク」**をクリックしてAlibaba Cloudの請求アカウントにリンクしてください。

    > **注記：**
    >
    > 組織が既にTiDB Cloudで支払い方法を登録している場合、その組織の既存の支払い方法は、新たに追加されたAlibaba Cloudの請求アカウントに置き換えられます。

</div>
</CustomContent>
</SimpleTab>
