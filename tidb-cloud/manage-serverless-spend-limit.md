---
title: Manage Spend Limit for Serverless Tier clusters
summary: Learn how to manage spend limit for your Serverless Tier clusters.
---

# Serverless Tierクラスターの使用制限を管理する {#manage-spend-limit-for-serverless-tier-clusters}

> **ノート：**
>
> 使用制限は、Serverless Tierクラスターにのみ適用されます。

使用制限とは、1 か月に特定のワークロードに使用できる最大金額を指します。これは、Serverless Tierクラスターの予算を設定できるコスト管理メカニズムです。

TiDB Cloudの組織ごとに、デフォルトで最大 5 つのServerless Tierクラスターを作成できます。 Serverless Tierクラスターをさらに作成するには、クレジット カードを追加し、使用量の上限を設定する必要があります。ただし、新しいクラスターを作成する前に以前のクラスターの一部を削除した場合でも、クレジット カードがなくても新しいクラスターを作成できます。

## 利用枠 {#usage-quota}

組織内の最初の 5 つのServerless Tierクラスターについて、 TiDB Cloud は、次のようにそれぞれに無料の使用量割り当てを提供します。

-   行storage: 5 GiB
-   [リクエスト ユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 1 か月あたり 5,000 万 RU

クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、 [クォータを増やす](#update-spend-limit)または新しい月の開始時に使用量がリセットされるまで調整されます。たとえば、クラスターのstorageが 5 GiB を超えると、1 つのトランザクションの最大サイズ制限が 10 MiB から 1 MiB に減少します。

さまざまなリソース (読み取り、書き込み、SQL CPU、およびネットワーク エグレスを含む) の RU 消費、料金の詳細、調整された情報について詳しくは、 [TiDB CloudServerless Tierの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

追加のクォータを使用してServerless Tierクラスターを作成する場合は、クラスター作成ページで使用制限を編集できます。詳細については、 [TiDB クラスターを作成する](/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster)を参照してください。

## 費用の上限を更新する {#update-spend-limit}

既存のServerless Tierクラスターの場合、次のように使用制限を更新することで、使用クォータを増やすことができます。

1.  TiDB Cloudコンソールで、左上隅にある ☰ ホバー メニューをクリックし、ターゲット クラスターの名前をクリックして概要ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、☰ ホバー メニューで別のプロジェクトに切り替えることができます。

2.  **[今月の使用量]**領域で、 <strong>[使用量クォータをさらに取得]</strong>をクリックします。

3.  必要に応じて、毎月の使用制限を編集します。支払い方法を追加していない場合は、制限を編集した後にクレジット カードを追加する必要があります。

4.  **[ 使用制限の更新 ]**をクリックします。
