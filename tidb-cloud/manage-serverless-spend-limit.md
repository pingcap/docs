---
title: Manage Spending Limit for TiDB Cloud Starter Instances
summary: TiDB Cloud Starterインスタンスの利用限度額を管理する方法を学びましょう。
---

# TiDB Cloud Starterインスタンスの利用限度額を管理する {#manage-spending-limit-for-tidb-cloud-starter-instances}

> **注記：**
>
> 支出制限は、 TiDB Cloud Starterインスタンスにのみ適用されます。

支出制限とは、特定のワークロードに対して1か月間に支出できる最大金額のことです。これは、TiDB Cloud Starterインスタンスの予算を設定できるコスト管理メカニズムです。

TiDB Cloudの各組織につき、最大 5 つの [無料のTiDB Cloud Starterインスタンス](/tidb-cloud/select-cluster-tier.md#starter)デフォルトで作成できます。TiDB Cloud Starterインスタンスをさらに作成するには、クレジットカードを追加し、月間利用限度額を設定する必要があります。ただし、新しいインスタンスを作成する前に以前のTiDB Cloud Starterインスタンスを削除した場合、新しいTiDB Cloud Starterインスタンスはクレジットカードなしで作成できます。

## 使用クォータ {#usage-quota}

組織内の最初の 5 つのTiDB Cloud Starterインスタンス（無料版かスケーラブル版かを問わず）については、 TiDB Cloud はそれぞれに以下の無料使用クォ​​ータを提供します。

-   行ベースstorage：5 GiB
-   カラム型storage：5 GiB
-   [要求単位（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) : 5,000万RU/月

TiDB Cloud Starterインスタンスが使用クォータに達すると、ユーザーが または新しい月の開始時に使用がリセットさ[割り当てを増やす](#update-spending-limit)まで、新しい接続試行は即座に拒否されます。クォータに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。たとえば、無料のTiDB Cloud StarterTiDB Cloud Starterの行ベースのstorageが5 GiB を超えると、 TiDB Cloud Starterインスタンスは自動的に新しい接続試行を制限します。

さまざまなリソース（読み取り、書き込み、SQL CPU、ネットワーク出力など）のRU消費量、価格の詳細、およびスロットリング情報の詳細については、 [TiDB Cloud Starterの料金詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)参照してください。

追加のクォータを使用してTiDB Cloud Starterインスタンスを作成する場合は、 TiDB Cloud Starterインスタンスの作成ページで支出制限を編集できます。詳細については、 [TiDB Cloud Starterインスタンスを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)参照してください。

## 支出限度額を更新する {#update-spending-limit}

無料のTiDB Cloud Starterインスタンスの場合、インスタンス作成時に月間利用制限を設定することで、利用クォータを増やすことができます。既存のTiDB Cloud Starter TiDB Cloud Starterインスタンスの場合は、月間利用制限を直接調整できます。

TiDB Cloud Starterインスタンスの支出制限を更新するには、以下の手順を実行してください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Starterインスタンスの名前をクリックすると、その概要ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  **「今月使用した容量」**の欄で、 **「支出制限を設定」を**クリックします。

    以前に支出限度額を設定していて、それを更新したい場合は、クリックしてください。 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>**編集**。

3.  必要に応じて月間支出限度額を編集してください。支払い方法を登録していない場合は、限度額を編集した後にクレジットカードを追加する必要があります。

4.  **「支出限度額の更新」**をクリックしてください。
