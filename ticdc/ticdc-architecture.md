---
title: TiCDC New Architecture
summary: TiCDCの新しいアーキテクチャの機能、アーキテクチャ設計、導入ガイド、および注意事項を紹介します。
---

# TiCDCの新アーキテクチャ {#ticdc-new-architecture}

[TiCDC v8.5.4-release.1](https://github.com/pingcap/ticdc/releases/tag/v8.5.4-release.1)以降、TiCDCは、リアルタイムデータレプリケーションのパフォーマンス、拡張性、安定性を向上させつつ、リソースコストを削減する新しいアーキテクチャを導入しました。

この新しいアーキテクチャは[従来のTiCDCアーキテクチャ](/ticdc/ticdc-classic-architecture.md)アーキテクチャの構成、使用法、API との互換性を維持しながら、TiCDC コア コンポーネントを再設計し、そのデータ処理ワークフローを最適化します。これには次のような利点があります。

-   **シングルノードのパフォーマンス向上**：シングルノードで最大50万個のテーブルを複製でき、テーブル数の多いシナリオではシングルノードで最大190 MiB/sの複製スループットを実現します。
-   **拡張性の向上**：クラスタレプリケーション機能はほぼ線形に拡張可能です。単一のクラスタは100ノード以上に拡張でき、10,000を超えるチェンジフィードをサポートし、単一のチェンジフィード内で数百万のテーブルをレプリケートできます。
-   **安定性の向上**：トラフィック量が多く、DDL操作が頻繁に発生し、クラスタのスケーリングイベントが発生するシナリオにおいて、変更フィードのレイテンシーが短縮され、パフォーマンスがより安定します。リソースの分離と優先度スケジューリングにより、複数の変更フィードタスク間の干渉が軽減されます。
-   **リソースコストの削減**：リソース利用率の向上と冗長性の削減により、一般的なシナリオではCPUとメモリのリソース使用量を最大50%削減できます。

## 建築設計 {#architectural-design}

![TiCDC New Architecture](/media/ticdc/ticdc-new-arch-1.png)

TiCDCの新しいアーキテクチャは、ログサービスとダウンストリームアダプタという2つの主要コンポーネントで構成されています。

-   ログサービス：コアデータサービスレイヤーとして、ログサービスはアップストリームのTiDBクラスタから行の変更やDDLイベントなどの情報を取得し、変更データをローカルディスクに一時的に保存します。また、ダウンストリームアダプタからのデータ要求にも応答し、DMLデータとDDLデータを定期的にマージおよびソートして、ソート済みのデータをダウンストリームアダプタに送信します。
-   ダウンストリームアダプタ：ダウンストリームデータレプリケーション適応レイヤーとして、ダウンストリームアダプタはユーザーが開始する変更フィード操作を処理します。関連するレプリケーションタスクをスケジュールおよび生成し、ログサービスからデータを取得し、取得したデータをダウンストリームシステムにレプリケートします。

TiCDCの新しいアーキテクチャは、アーキテクチャをステートフルコンポーネントとステートレスコンポーネントに分離することで、システムの拡張性、信頼性、柔軟性を大幅に向上させています。ステートフルコンポーネントであるログサービスは、データの取得、ソート、およびstorageに重点を置いています。これを変更フィード処理ロジックから分離することで、複数の変更フィード間でデータを共有できるようになり、リソース利用率を効果的に向上させ、システムオーバーヘッドを削減できます。ステートレスコンポーネントであるダウンストリームアダプタは、インスタンス間でレプリケーションタスクを迅速に移行できる軽量スケジューリングメカニズムを使用しています。ワークロードの変化に基づいてレプリケーションタスクの分割とマージを動的に調整できるため、さまざまなシナリオで低遅延のレプリケーションが保証されます。

## 古典的建築と新建築の比較 {#comparison-between-the-classic-and-new-architectures}

新しいアーキテクチャは、継続的なシステム拡張時に発生するパフォーマンスのボトルネック、安定性の不足、拡張性の制限といった一般的な問題に対処するように設計されています。[古典アーキテクチャ](/ticdc/ticdc-classic-architecture.md)と比較して、新しいアーキテクチャは以下の主要な側面で大幅な最適化を実現しています。

| 特徴                | TiCDCクラシックアーキテクチャ                                      | TiCDCの新アーキテクチャ                                                                                            |
| ----------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **処理ロジックドライバ**    | タイマー駆動                                                 | イベント駆動型                                                                                                   |
| **タスクのトリガーメカニズム** | タイマーでトリガーされるメインループは、50ミリ秒ごとにタスクをチェックしますが、処理性能は限られています。 | イベント駆動型で、DML変更、DDL変更、変更フィード操作などのイベントによってトリガーされます。キュー内のイベントは、固定の50ミリ秒間隔を待たずに可能な限り迅速に処理され、追加のレイテンシーが削減されます。 |
| **タスクスケジューリング方法** | 各変更フィードは、タスクをポーリングするメインループを実行します。                      | イベントはキューに入れられ、複数のスレッドによって並行して処理されます。                                                                      |
| **タスク処理効率**       | 各タスクは複数のサイクルを経るため、パフォーマンスのボトルネックが生じる。                  | イベントは固定間隔を待たずに即座に処理されるため、レイテンシーが軽減されます。                                                                   |
| **資源消費**          | 非アクティブなテーブルを頻繁にチェックすると、CPUリソースが無駄になる。                  | コンシューマスレッドはキューに入れられたイベントのみを処理し、非アクティブなタスクのチェックによるリソース消費を回避します。                                            |
| **複雑**            | O(n)であり、テーブル数が増えるにつれてパフォーマンスが低下する。                     | O(1)であり、テーブル数に影響されないため、効率が向上します。                                                                          |
| **CPU使用率**        | 各チェンジフィードは1つの論理CPUしか使用できません。                           | 各チェンジフィードは、マルチコアCPUの並列処理機能を最大限に活用できます。                                                                    |
| **拡張性**           | 拡張性が低い（CPU数に制限される）                                     | マルチスレッド処理とイベントキューによる高い拡張性                                                                                 |
| **変更フィード干渉**      | オーナーノードが変更フィード間の干渉を引き起こす可能性がある                         | イベント駆動モードは、変更フィード間の干渉を回避します。                                                                              |

![Comparison between the TiCDC classic and new architectures](/media/ticdc/ticdc-new-arch-2.png)

## クラシックな建築様式と新しい建築様式からお選びください。 {#choose-between-the-classic-and-new-architectures}

ワークロードが次のいずれかの条件を満たす場合は、パフォーマンスと安定性を向上させるために、[従来のTiCDCアーキテクチャ](/ticdc/ticdc-classic-architecture.md)から新しいアーキテクチャに切り替えることをお勧めします。

-   増分スキャンパフォーマンスのボトルネック: 増分スキャンタスクの完了に過度に時​​間がかかり、レプリケーションのレイテンシーが継続的に増加します。
-   超高トラフィックシナリオ：変更フィードの総トラフィックが700 MiB/秒を超える場合。
-   MySQL シンクで高スループット書き込みを行う単一テーブル: ターゲットテーブルには**、プライマリキーまたは NULL 以外の一意キーが 1 つだけ**あります。
-   大規模なテーブルレプリケーション：レプリケーション対象のテーブル数が10万を超える場合。
-   頻繁な DDL 操作によるレイテンシー: DDL ステートメントの頻繁な実行は、レプリケーションのレイテンシーを大幅に増加させます。

## 新機能 {#new-features}

新しいアーキテクチャでは、すべてのシンクに対して**テーブルレベルのタスク分割が**サポートされています。この機能は、changefeed 設定で`scheduler.enable-table-across-nodes = true`設定することで有効にできます。

この機能を有効にすると、TiCDC は、以下のいずれかの条件を満たすテーブルを自動的に分割し、複数のノードに分散させて並列レプリケーションを実行します。これにより、レプリケーションの効率とリソース利用率が向上します。

-   テーブルのリージョン数が設定されたしきい値を超えています（デフォルトでは`10000` 、 `scheduler.region-threshold`で調整可能）。
-   テーブルへの書き込みトラフィックが設定されたしきい値を超えています（デフォルトでは無効、 `scheduler.write-key-threshold`で設定可能）。

> **注記：**
>
> MySQLシンクの変更フィードの場合、テーブルレベルのタスク分割モードでのデータレプリケーションの正確性を確保するため、前述の条件のいずれかを満たし、**かつ主キーまたはNULL以外の一意キーが正確に1つ**だけ存在するテーブルのみがTiCDCによって分割および分散されます。

### テーブルレベルのタスク分割に関する推奨構成 {#recommended-configurations-for-table-level-task-splitting}

新しい TiCDCアーキテクチャに切り替えた後は、従来のアーキテクチャのテーブル分割設定を再利用しないでください。ほとんどの場合、新しいアーキテクチャのデフォルト設定を使用してください。レプリケーションのパフォーマンスにボトルネックが生じたり、スケジューリングの不均衡が発生したりする特別なシナリオでのみ、デフォルト値に基づいて段階的な調整を行ってください。

テーブル分割モードでは、以下の設定に注意してください。

-   [`scheduler.region-threshold`](/ticdc/ticdc-changefeed-config.md#region-threshold) : デフォルト値は`10000`です。テーブル内のリージョン数がこのしきい値を超えると、TiCDC はテーブルを分割します。リージョン数が比較的少ないが全体的な書き込みスループットが高いテーブルの場合は、この値を適切に減らすことができます。このパラメータは`scheduler.region-count-per-span`以上である必要があります。そうでない場合、タスクが繰り返し再スケジュールされ、レプリケーションのレイテンシーが増加する可能性があります。
-   [`scheduler.region-count-per-span`](/ticdc/ticdc-changefeed-config.md#region-count-per-span-new-in-v854) : デフォルト値は`100`です。変更フィードの初期化中に、TiCDC はこのパラメータに従って分割条件を満たすテーブルを分割します。分割後、各サブテーブルには最大で`region-count-per-span`個のリージョンが含まれます。
-   [`scheduler.write-key-threshold`](/ticdc/ticdc-changefeed-config.md#write-key-threshold) : デフォルト値は`0` (無効) です。テーブルのシンク書き込みスループットがこのしきい値を超えると、TiCDC はテーブル分割をトリガーします。ほとんどの場合、このパラメータは`0`に設定してください。

## 互換性 {#compatibility}

以下の特別な場合を除き、TiCDC の新しいアーキテクチャは従来のアーキテクチャと完全に互換性があります。

### DDL進捗状況追跡テーブル {#ddl-progress-tracking-table}

TiCDC の従来のアーキテクチャでは、DDL レプリケーション操作は厳密にシリアルであるため、レプリケーションの進行状況は変更フィードの`CheckpointTs`を使用してのみ追跡できます。しかし、新しいアーキテクチャでは、DDL レプリケーションの効率を向上させるために、可能な限り異なるテーブルの DDL 変更を並列でレプリケートします。ダウンストリームの MySQL 互換データベースで各テーブルの DDL レプリケーションの進行状況を正確に記録するために、TiCDC の新しいアーキテクチャでは、ダウンストリームデータベースに`tidb_cdc.ddl_ts_v1`という名前のテーブルを作成し、変更フィードの DDL レプリケーションの進行状況情報を格納します。

### DDLレプリケーション動作の変更 {#changes-in-ddl-replication-behavior}

-   従来のTiCDCアーキテクチャでは、テーブル名を入れ替えるDDL（例： `RENAME TABLE a TO c, b TO a, c TO b;` ）はサポートされていません。新しいアーキテクチャでは、このようなDDLがサポートされています。

-   新しいアーキテクチャは`RENAME` DDL のフィルタリング ルールを統一し、簡素化します。

    -   従来のアーキテクチャでは、フィルタリングロジックは以下のとおりです。

        -   単一テーブル名の変更：DDLステートメントは、古いテーブル名がフィルタルールに一致する場合にのみ複製されます。
        -   複数テーブルの名前変更：DDLステートメントは、古いテーブル名と新しいテーブル名の両方がフィルタルールに一致する場合にのみ複製されます。

    -   新しいアーキテクチャでは、単一テーブルと複数テーブルの両方の名前変更において、ステートメント内の古いテーブル名がフィルタルールに一致する限り、DDLステートメントが複製されます。

        次のフィルタルールを例にとってみましょう。

        ```toml
        [filter]
        rules = ['test.t*']
        ```

        -   従来のアーキテクチャでは、 `RENAME TABLE test.t1 TO ignore.t1`のような単一テーブルの名前変更の場合、古いテーブル名`test.t1`ルールに一致するため、複製されます。 `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`のような複数テーブルの名前変更の場合、新しいテーブル名`ignore.t1`がルールに一致しないため、複製されません。
        -   新しい TiCDCアーキテクチャでは、 `RENAME TABLE test.t1 TO ignore.t1`と`RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`の両方の古いテーブル名がルールに一致するため、両方の DDL ステートメントが複製されます。

## 制限事項 {#limitations}

新しいTiCDCアーキテクチャは、従来のアーキテクチャのすべての機能を統合しています。ただし、一部の機能はまだ十分にテストされていません。システムの安定性を確保するため、以下の機能はコア本番環境で使用することは推奨さ**れません**。

-   [シンクポイント](/ticdc/ticdc-upstream-downstream-check.md)
-   [リドゥログ](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)
-   [パルサーシンク](/ticdc/ticdc-sink-to-pulsar.md)
-   [収納シンク](/ticdc/ticdc-sink-to-cloud-storage.md)

さらに、新しいTiCDCアーキテクチャでは、ダウンストリームレプリケーションのために大規模なトランザクションを複数のバッチに分割する機能が現状ではサポートされていません。そのため、非常に大きなトランザクションを処理する際にメモリ不足（OOM）が発生するリスクが依然として存在します。新しいアーキテクチャを使用する前に、このリスクを適切に評価し、軽減策を講じてください。

## アップグレードガイド {#upgrade-guide}

新しいアーキテクチャのTiCDCは、TiDBクラスタのバージョン7.5.0以降にのみデプロイできます。デプロイ前に、TiDBクラスタがこの要件を満たしていることを確認してください。

TiUPまたはTiDB Operatorを使用して、新しいアーキテクチャにTiCDCノードをデプロイできます。

### 新しいアーキテクチャでTiCDCノードを備えた新しいTiDBクラスタをデプロイ {#deploy-a-new-tidb-cluster-with-ticdc-nodes-in-the-new-architecture}

<SimpleTab>
<div label="TiUP">

TiUPを使用して v8.5.4 以降の新しい TiDB クラスタをデプロイする場合、新しいアーキテクチャで TiCDC ノードも同時にデプロイできます。そのためには、 TiUP がTiDB クラスタの起動に使用する構成ファイルに TiCDC 関連のセクションを追加し、 `newarch: true`を設定するだけです。以下に例を示します。

```yaml
cdc_servers:
  - host: 10.0.1.20
    config:
      newarch: true
  - host: 10.0.1.21
    config:
      newarch: true
```

TiCDC デプロイメントの詳細については、 [TiUPを使用してTiCDCを含む新しいTiDBクラスタをデプロイ](/ticdc/deploy-ticdc.md#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup)参照してください。

</div>
<div label="TiDB Operator">

TiDB Operator を使用して v8.5.4 以降の新しい TiDB クラスタをデプロイする場合、新しいアーキテクチャで TiCDC ノードを同時にデプロイすることもできます。そのためには、クラスタ構成ファイルに TiCDC 関連のセクションを追加し、 `newarch = true`を設定するだけです。以下に例を示します。

```yaml
spec:
  ticdc:
    baseImage: pingcap/ticdc
    version: v8.5.4
    replicas: 3
    config:
      newarch = true
```

TiCDC 導入の詳細については、 [TiCDCの新規導入](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-ticdc/#fresh-ticdc-deployment)参照してください。

</div>
</SimpleTab>

### 既存のTiDBクラスタに新しいアーキテクチャでTiCDCノードをデプロイ {#deploy-ticdc-nodes-in-the-new-architecture-in-an-existing-tidb-cluster}

<SimpleTab>
<div label="TiUP">

TiUPを使用して新しいアーキテクチャにTiCDCノードをデプロイするには、以下の手順を実行してください。

1.  TiDB クラスターにまだ TiCDC ノードがない場合は、 [TiCDCクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster)を参照してクラスターに新しい TiCDC ノードを追加します。それ以外の場合は、この手順をスキップしてください。

2.  TiDBクラスタのバージョンがv8.5.4より前の場合は、新しいアーキテクチャのTiCDCバイナリパッケージを手動でダウンロードし、ダウンロードしたファイルをTiDBクラスタにパッチ適用する必要があります。それ以外の場合は、この手順をスキップしてください。

    ダウンロード リンクは次の形式に従います: `https://tiup-mirrors.pingcap.com/cdc-${version}-${os}-${arch}.tar.gz` 。ここで、 `${version}`は TiCDC バージョン (利用可能なバージョン[TiCDCが新アーキテクチャ向けにリリース](https://github.com/pingcap/ticdc/releases)方向へのリリースを参照)、 `${os}`はオペレーティング システムです。 `${arch}`は、コンポーネントが実行されるプラットフォーム ( `amd64`または`arm64` ) です。

    例えば、Linux (x86-64) 用の TiCDC v8.5.4-release.1 のバイナリパッケージをダウンロードするには、次のコマンドを実行します。

    ```shell
    wget https://tiup-mirrors.pingcap.com/cdc-v8.5.4-release.1-linux-amd64.tar.gz
    ```

3.  TiDB クラスターで実行中のチェンジフィードがある場合は、 [レプリケーションタスクを一時停止する](/ticdc/ticdc-manage-changefeed.md#pause-a-replication-task)を参照して、チェンジフィードのすべてのレプリケーションタスクを一時停止します。

    ```shell
    # The default server port of TiCDC is 8300.
    cdc cli changefeed pause --server=http://<ticdc-host>:8300 --changefeed-id <changefeed-name>
    ```

4.  [`tiup cluster patch`](/tiup/tiup-component-cluster-patch.md)コマンドを使用して、ダウンロードした TiCDC バイナリファイルを TiDB クラスタにパッチ適用します。

    ```shell
    tiup cluster patch <cluster-name> ./cdc-v8.5.4-release.1-linux-amd64.tar.gz -R cdc --overwrite
    ```

5.  新しいアーキテクチャを有効にするには、[`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用して TiCDC の設定を更新してください。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    ```yaml
    server_configs:
      cdc:
        newarch: true
    ```

6.  すべてのレプリケーション タスクを再開するには、 [レプリケーションタスクを再開する](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task)を参照してください。

    ```shell
    # The default server port of TiCDC is 8300.
    cdc cli changefeed resume --server=http://<ticdc-host>:8300 --changefeed-id <changefeed-name>
    ```

</div>
<div label="TiDB Operator">

TiDB Operatorを使用して既存のTiDBクラスタに新しいアーキテクチャでTiCDCノードをデプロイするには、次の手順を実行します。

-   TiDB クラスターに TiCDCコンポーネントが含まれていない場合は、 [既存のTiDBクラスタにTiCDCを追加する](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-ticdc/#add-ticdc-to-an-existing-tidb-cluster)を参照して、新しい TiCDC ノードを追加します。その際、クラスター構成ファイルで TiCDC イメージのバージョンを新しいアーキテクチャのバージョンとして指定します。利用可能なバージョンについては、 [TiCDCが新アーキテクチャ向けにリリース](https://github.com/pingcap/ticdc/releases)参照してください。

    例えば：

    ```yaml
    spec:
      ticdc:
        baseImage: pingcap/ticdc
        version: v8.5.4-release.1
        replicas: 3
        config:
          newarch = true
    ```

-   TiDBクラスタに既にTiCDCコンポーネントが含まれている場合は、以下の手順を実行してください。

    1.  TiDBクラスタで実行中のチェンジフィードがある場合は、チェンジフィードのすべてのレプリケーションタスクを一時停止してください。

        ```shell
        kubectl exec -it ${pod_name} -n ${namespace} -- sh
        ```

        ```shell
        # The default server port of TiCDC deployed via TiDB Operator is 8301.
        /cdc cli changefeed pause --server=http://127.0.0.1:8301 --changefeed-id <changefeed-name>
        ```

    2.  クラスタ構成ファイル内のTiCDCイメージバージョンを新しいアーキテクチャバージョンに更新してください。

        ```shell
        kubectl edit tc ${cluster_name} -n ${namespace}
        ```

        ```yaml
        spec:
          ticdc:
            baseImage: pingcap/ticdc
            version: v8.5.4-release.1
            replicas: 3
        ```

        ```shell
        kubectl apply -f ${cluster_name} -n ${namespace}
        ```

    3.  変更フィードのすべてのレプリケーションタスクを再開します。

        ```shell
        kubectl exec -it ${pod_name} -n ${namespace} -- sh
        ```

        ```shell
        # The default server port of TiCDC deployed via TiDB Operator is 8301.
        /cdc cli changefeed resume --server=http://127.0.0.1:8301 --changefeed-id <changefeed-name>
        ```

</div>
</SimpleTab>

## 新しいアーキテクチャを使用する {#use-the-new-architecture}

新しいアーキテクチャでTiCDCノードをデプロイした後も、従来のアーキテクチャと同じコマンドを引き続き使用できます。新しいコマンドを学習したり、従来のアーキテクチャで使用していたコマンドを変更したりする必要はありません。

例えば、新しいアーキテクチャで新しいTiCDCノードのレプリケーションタスクを作成するには、次のコマンドを実行します。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

特定のレプリケーションタスクの詳細を照会するには、次のコマンドを実行します。

```shell
cdc cli changefeed query -s --server=http://127.0.0.1:8300 --changefeed-id=simple-replication-task
```

コマンドの使用方法と詳細については、[変更フィードを管理する](/ticdc/ticdc-manage-changefeed.md)参照してください。

## 監視 {#monitoring}

新しいアーキテクチャにおける TiCDC の監視ダッシュボードは**、TiCDC-New-Arch**です。TiDB クラスタのバージョンが v8.5.4 以降の場合、この監視ダッシュボードはクラスタのデプロイまたはアップグレード時に Grafana に統合されるため、手動操作は不要です。クラスタのバージョンが v8.5.4 より前の場合は、監視を有効にするために[TiCDC監視メトリクスファイル](https://github.com/pingcap/ticdc/blob/master/metrics/grafana/ticdc_new_arch.json)を手動でインポートする必要があります。

インポート手順と各監視メトリクスの詳細な説明については、 [新アーキテクチャにおけるTiCDCのメトリクス](/ticdc/monitor-ticdc.md#metrics-for-ticdc-in-the-new-architecture)参照してください。
