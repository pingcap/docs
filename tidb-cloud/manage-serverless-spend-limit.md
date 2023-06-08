---
title: Manage Spend Limit for TiDB Serverless clusters
summary: Learn how to manage spend limit for your TiDB Serverless clusters.
---

# TiDB Serverless クラスタの支出制限を管理する {#manage-spend-limit-for-tidb-serverless-clusters}

> **ノート：**
>
> 使用制限は、TiDB Serverless クラスタにのみ適用されます。

支出制限とは、1 か月に特定のワークロードに費やすことができる最大金額を指します。これは、TiDB Serverless クラスタの予算を設定できるコスト管理メカニズムです。

TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB Serverless クラスタを作成できます。さらにTiDB Serverless クラスターを作成するには、クレジット カードを追加し、使用量の制限を設定する必要があります。ただし、さらに作成する前に以前のクラスターの一部を削除した場合でも、クレジット カードがなくても新しいクラスターを作成できます。

## 使用量割り当て {#usage-quota}

組織内の最初の 5 つの TiDB Serverless クラスタに対して、 TiDB Cloud は各クラスターに次のように無料の使用量クォータを提供します。

-   行storage: 5 GiB
-   [<a href="/tidb-cloud/tidb-cloud-glossary.md#request-unit">リクエストユニット (RU)</a>](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月あたり 5,000 万 RU

クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、新しい月の初めに使用量が[<a href="#update-spend-limit">割り当てを増やす</a>](#update-spend-limit)されるまでスロットルされます。たとえば、クラスターのstorageが 5 GiB を超えると、単一トランザクションの最大サイズ制限が 10 MiB から 1 MiB に減ります。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク下りなど) の RU 消費量、料金の詳細、および調整された情報の詳細については、 [<a href="https://www.pingcap.com/tidb-cloud-serverless-pricing-details">TiDB Serverlessの料金詳細</a>](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

追加のクォータを使用して TiDB Serverless クラスタを作成する場合は、クラスター作成ページで使用制限を編集できます。詳細については、 [<a href="/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster">TiDB クラスターを作成する</a>](/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster)を参照してください。

## 支出制限を更新する {#update-spend-limit}

既存の TiDB Serverless クラスタの場合、次のように使用制限を更新することで、使用量クォータを増やすことができます。

1.  TiDB Cloudコンソールで、左上隅にある ☰ ホバー メニューをクリックし、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、☰ ホバー メニューで別のプロジェクトに切り替えることができます。

2.  **「今月の使用量」**領域で、 **「使用量クォータをさらに取得する」**をクリックします。

3.  必要に応じて、毎月の支出制限を編集します。支払い方法を追加していない場合は、制限を編集した後にクレジット カードを追加する必要があります。

4.  **[支出制限を更新]**をクリックします。
