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
| **Available** | クラスターは正常で、利用可能です。                |
| **作成**   | クラスターを作成中です。作成中はクラスターにアクセスできません。 |
| **Importing**   | クラスターにデータをインポートしています。            |
| **維持する** | クラスターはメンテナンス中です。                 |
| **変更する** | クラスターが変更されています。                  |
| **Unavailable** | クラスターに障害が発生し、TiDB はそれを復旧できません。   |
| **Pausing** | クラスターを一時停止しています。                 |
| **一時停止** | クラスターは一時停止されています。                |
| **Resuming**   | クラスターは一時停止状態から再開されます。            |
| **Restoring**   | 現在、クラスターはバックアップから復元中です。          |

### TiDBノードの状態 {#tidb-node-status}

> **Note:**
>
> TiDBノードの状態は、 TiDB Cloud Dedicatedクラスタでのみ利用可能です。

`tidb`で始まるノード名はTiDBノードであり、 `tiproxy`で始まるノード名はTiProxyノードです。

| TiDBノードの状態 | 説明                 |
| :--------- | :----------------- |
| **Available**   | TiDBノードは正常で利用可能です。 |
| **作成**     | TiDBノードが作成されています。  |
| **Unavailable**   | TiDBノードが利用できません。   |
| **Deleting**    | TiDBノードが削除されています。  |

### TiKVノードの状態 {#tikv-node-status}

> **Note:**
>
> TiKVノードの状態は、 TiDB Cloud Dedicatedクラスタでのみ利用可能です。

| TiKVノードの状態 | 説明                 |
| :--------- | :----------------- |
| **Available**   | TiKVノードは正常で利用可能です。 |
| **作成**     | TiKVノードが作成されています。  |
| **Unavailable**   | TiKVノードは利用できません。   |
| **Deleting**    | TiKVノードが削除されます。    |

</CustomContent>

<CustomContent plan="starter,essential,premium">

## インスタンスの状態 {#instance-status}

[**My TiDB**](https://tidbcloud.com/tidbs)ページでは、 **Status**列に、実行中の各TiDB Cloudインスタンスの現在のステータスが表示されます。

| 状態        | 説明                                 |
| :-------- | :--------------------------------- |
| **Active** | インスタンスは正常に動作しており、利用可能です。           |
| **作成**    | インスタンスを作成中です。作成中はインスタンスにアクセスできません。 |
| **Importing**    | インスタンスにデータをインポートしています。             |
| **維持する**  | 現在、インスタンスはメンテナンス中です。               |
| **変更する**  | インスタンスが変更されています。                   |
| **Unavailable**  | インスタンスが失敗し、TiDB はそれを復旧できません。       |
| **Restoring**    | 現在、インスタンスはバックアップから復元中です。           |

</CustomContent>

## モニタリング指標 {#monitoring-metrics}

TiDB Cloudでは、次のページから、 <CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>クラスターの一般的に使用されるメトリクスを表示できます。

- **Overview**ページ
- **Metrics**ページ

### 概要ページ {#overview-page}

**Overview**ページには、TiDB Cloudリソースの一般的な指標が表示されます。

概要ページで指標を表示するには、以下の手順に従ってください。

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象リソースの名前をクリックすると、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. **Core Metrics**セクションを確認してください。

### 指標ページ {#metrics-page}

**Metrics**ページには、 TiDB Cloudリソースに関するすべてのメトリクスが表示されます。これらのメトリクスを確認することで、パフォーマンスの問題を容易に特定し、現在のデータベースデプロイが要件を満たしているかどうかを判断できます。

**Metrics**ページで指標を表示するには、以下の手順に従ってください。

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象リソースの名前をクリックすると、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. 左側のナビゲーションペインで、 **Monitoring** &gt; **Metrics**をクリックします。

詳細については、 [TiDB Cloud の組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)を参照してください。
