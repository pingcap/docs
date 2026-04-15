---
title: Monitor TiDB
summary: TiDB Cloudリソースの監視方法を学びましょう。
---

# TiDBを監視する {#monitor-tidb}

このドキュメントでは<CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>クラスターを監視する方法について説明します。

<CustomContent plan="dedicated">

## クラスタの状態とノードの状態 {#cluster-status-and-node-status}

各実行中のクラスターの現在のステータスは、クラスターページで確認できます。

### クラスタの状態 {#cluster-status}

| クラスタの状態  | 説明                               |
| :------- | :------------------------------- |
| **利用可能** | クラスターは正常で、利用可能です。                |
| **作成**   | クラスターを作成中です。作成中はクラスターにアクセスできません。 |
| **輸入**   | クラスターにデータをインポートしています。            |
| **維持する** | クラスターはメンテナンス中です。                 |
| **変更する** | クラスターが変更されています。                  |
| **利用不可** | クラスターに障害が発生し、TiDB はそれを復旧できません。   |
| **一時停止** | クラスターを一時停止しています。                 |
| **一時停止** | クラスターは一時停止されています。                |
| **再開**   | クラスターは一時停止状態から再開されます。            |
| **復元**   | 現在、クラスターはバックアップから復元中です。          |

### TiDBノードの状態 {#tidb-node-status}

> **注記：**
>
> TiDBノードの状態は、 TiDB Cloud Dedicatedクラスタでのみ利用可能です。

`tidb`で始まるノード名はTiDBノードであり、 `tiproxy`で始まるノード名はTiProxyノードです。

| TiDBノードの状態 | 説明                 |
| :--------- | :----------------- |
| **利用可能**   | TiDBノードは正常で利用可能です。 |
| **作成**     | TiDBノードが作成されています。  |
| **利用不可**   | TiDBノードが利用できません。   |
| **削除中**    | TiDBノードが削除されています。  |

### TiKVノードの状態 {#tikv-node-status}

> **注記：**
>
> TiKVノードの状態は、 TiDB Cloud Dedicatedクラスタでのみ利用可能です。

| TiKVノードの状態 | 説明                 |
| :--------- | :----------------- |
| **利用可能**   | TiKVノードは正常で利用可能です。 |
| **作成**     | TiKVノードが作成されています。  |
| **利用不可**   | TiKVノードは利用できません。   |
| **削除中**    | TiKVノードが削除されます。    |

</CustomContent>

<CustomContent plan="starter,essential,premium">

## インスタンスの状態 {#instance-status}

[**私のTiDB**](https://tidbcloud.com/tidbs)ページでは、 **「ステータス」**列に、実行中の各TiDB Cloudインスタンスの現在のステータスが表示されます。

| 状態        | 説明                                 |
| :-------- | :--------------------------------- |
| **アクティブ** | インスタンスは正常に動作しており、利用可能です。           |
| **作成**    | インスタンスを作成中です。作成中はインスタンスにアクセスできません。 |
| **輸入**    | インスタンスにデータをインポートしています。             |
| **維持する**  | 現在、インスタンスはメンテナンス中です。               |
| **変更する**  | インスタンスが変更されています。                   |
| **利用不可**  | インスタンスが失敗し、TiDB はそれを復旧できません。       |
| **復元**    | 現在、インスタンスはバックアップから復元中です。           |

</CustomContent>

## モニタリング指標 {#monitoring-metrics}

TiDB Cloudでは、次のページから、 <CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>クラスターの一般的に使用されるメトリクスを表示できます。

-   **概要**ページ
-   **指標**ページ

### 概要ページ {#overview-page}

**概要**ページには、TiDB Cloudリソースの一般的な指標が表示されます。

概要ページで指標を表示するには、以下の手順に従ってください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象リソースの名前をクリックすると、その概要ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  **「コアメトリクス」**セクションを確認してください。

### 指標ページ {#metrics-page}

**メトリクス**ページには、 TiDB Cloudリソースに関するすべてのメトリクスが表示されます。これらのメトリクスを確認することで、パフォーマンスの問題を容易に特定し、現在のデータベース展開が要件を満たしているかどうかを判断できます。

**メトリクス**ページで指標を表示するには、以下の手順に従ってください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象リソースの名前をクリックすると、その概要ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  左側のナビゲーションペインで、 **[監視]** &gt; **[メトリクス]**をクリックします。

詳細については、 [TiDB Cloud の組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)を参照してください。
