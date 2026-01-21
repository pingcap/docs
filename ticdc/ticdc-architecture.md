---
title: TiCDC New Architecture
summary: TiCDC の新しいアーキテクチャの機能、アーキテクチャ設計、展開ガイド、および注意事項を紹介します。
---

# TiCDC の新しいアーキテクチャ {#ticdc-new-architecture}

[TiCDC v8.5.4-リリース.1](https://github.com/pingcap/ticdc/releases/tag/v8.5.4-release.1)から、TiCDC は、リソース コストを削減しながら、リアルタイム データ レプリケーションのパフォーマンス、スケーラビリティ、および安定性を向上させる新しいアーキテクチャを導入します。

この新しいアーキテクチャは、TiCDCのコアコンポーネントを再設計し、データ処理ワークフローを最適化しながら、 [古典的なTiCDCアーキテクチャ](/ticdc/ticdc-classic-architecture.md)の構成、使用方法、APIとの互換性を維持しています。これにより、以下の利点が得られます。

-   **単一ノードのパフォーマンスの向上**: 単一ノードで最大 500,000 個のテーブルを複製でき、ワイド テーブル シナリオでは単一ノードで最大 190 MiB/秒のレプリケーション スループットを実現します。
-   **拡張性の向上**：クラスタレプリケーション機能はほぼ直線的に拡張可能です。単一のクラスタで100ノード以上に拡張でき、10,000以上の変更フィードをサポートし、単一の変更フィード内で数百万のテーブルをレプリケートできます。
-   **安定性の向上**：高トラフィック、頻繁なDDL操作、クラスターのスケーリングイベントが発生するシナリオにおいて、チェンジフィードのレイテンシーが短縮され、パフォーマンスがより安定します。リソースの分離と優先スケジューリングにより、複数のチェンジフィードタスク間の干渉が軽減されます。
-   **リソース コストの削減**: リソース使用率の向上と冗長性の削減により、一般的なシナリオでは CPU とメモリのリソース使用量を最大 50% 削減できます。

## 建築設計 {#architectural-design}

![TiCDC New Architecture](/media/ticdc/ticdc-new-arch-1.png)

TiCDC の新しいアーキテクチャは、ログ サービスとダウンストリーム アダプターの 2 つのコア コンポーネントで構成されます。

-   ログサービス：コアデータサービスレイヤーとして、ログサービスは上流TiDBクラスタから行変更やDDLイベントなどの情報を取得し、変更データをローカルディスクに一時的に保存します。また、下流アダプタからのデータ要求に応答し、DMLデータとDDLデータを定期的にマージおよびソートし、ソート済みのデータを下流アダプタにプッシュします。
-   ダウンストリームアダプタ：ダウンストリームデータレプリケーション適応レイヤーとして、ダウンストリームアダプタはユーザーが開始した変更フィード操作を処理します。関連するレプリケーションタスクをスケジュールおよび生成し、ログサービスからデータを取得し、取得したデータをダウンストリームシステムに複製します。

TiCDCの新しいアーキテクチャは、アーキテクチャをステートフルコンポーネントとステートレスコンポーネントに分離することで、システムのスケーラビリティ、信頼性、柔軟性を大幅に向上させます。ステートフルコンポーネントであるログサービスは、データの取得、ソート、storageに重点を置いています。ログサービスをチェンジフィード処理ロジックから分離することで、複数のチェンジフィード間でのデータ共有が可能になり、リソース使用率を効果的に向上させ、システムオーバーヘッドを削減します。ステートレスコンポーネントであるダウンストリームアダプタは、軽量なスケジューリングメカニズムを使用して、インスタンス間でのレプリケーションタスクの迅速な移行を可能にします。ワークロードの変化に基づいてレプリケーションタスクの分割とマージを動的に調整できるため、さまざまなシナリオで低レイテンシのレプリケーションを実現します。

## 古典的なアーキテクチャと新しいアーキテクチャの比較 {#comparison-between-the-classic-and-new-architectures}

新しいアーキテクチャは、パフォーマンスのボトルネック、不十分な安定性、スケーラビリティの限界など、システムの継続的なスケーリング時に[古典アーキテクチャ](/ticdc/ticdc-classic-architecture.md)する一般的な問題に対処するように設計されています。1と比較して、新しいアーキテクチャは以下の主要な側面において大幅な最適化を実現しています。

| 特徴                | TiCDC クラシックアーキテクチャ                                    | TiCDCの新しいアーキテクチャ                                                                                                |
| ----------------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **処理ロジックドライバー**   | タイマー駆動                                                | イベント駆動型                                                                                                         |
| **タスクトリガーメカニズム**  | 50 ミリ秒ごとにタスクをチェックするタイマートリガーのメインループ。処理パフォーマンスは限られています。 | イベントドリブン型。DML変更、DDL変更、チェンジフィード操作などのイベントによってトリガーされます。キュー内のイベントは、固定の50ミリ秒間隔を待たずに可能な限り迅速に処理されるため、追加のレイテンシーが削減されます。 |
| **タスクスケジューリング方法** | 各チェンジフィードはタスクをポーリングするメインループを実行します                     | イベントはキューに入れられ、複数のスレッドによって同時に処理されます                                                                              |
| **タスク処理効率**       | 各タスクは複数のサイクルを経るため、パフォーマンスのボトルネックが発生します。               | イベントは一定間隔を待たずに即座に処理され、レイテンシーが短縮されます。                                                                            |
| **資源消費**          | 非アクティブなテーブルを頻繁にチェックするとCPUリソースが浪費される                   | 消費者スレッドはキューに入れられたイベントのみを処理し、非アクティブなタスクのチェックの消費を回避します。                                                           |
| **複雑**            | O(n)、テーブル数が増えるとパフォーマンスは低下する                           | O(1)、テーブル数の影響を受けず、効率が向上                                                                                         |
| **CPU使用率**        | 各変更フィードは1つの論理CPUのみを使用できます                             | 各チェンジフィードは、マルチコアCPUの並列処理能力を最大限に活用できます。                                                                          |
| **スケーラビリティ**      | スケーラビリティが低い（CPUの数によって制限される）                           | マルチスレッド処理とイベントキューによる強力なスケーラビリティ                                                                                 |
| **チェンジフィード干渉**    | オーナーノードはチェンジフィード間の干渉を引き起こす可能性がある                      | イベント駆動モードはチェンジフィード間の干渉を回避します                                                                                    |

![Comparison between the TiCDC classic and new architectures](/media/ticdc/ticdc-new-arch-2.png)

## クラシックアーキテクチャと新しいアーキテクチャから選択 {#choose-between-the-classic-and-new-architectures}

ワークロードが次のいずれかの条件を満たす場合は、パフォーマンスと安定性を向上させるために、アーキテクチャ[古典的なTiCDCアーキテクチャ](/ticdc/ticdc-classic-architecture.md)から新しいアーキテクチャに切り替えることをお勧めします。

-   増分スキャン パフォーマンスのボトルネック: 増分スキャン タスクの完了に非常に長い時間がかかり、レプリケーションのレイテンシーが継続的に増加します。
-   超高トラフィック シナリオ: 合計変更フィード トラフィックが 700 MiB/s を超えます。
-   MySQL シンクでの高スループット書き込みを備えた単一テーブル: ターゲット テーブルには**主キーまたは null 以外の一意のキーが 1 つだけ**あります。
-   大規模なテーブルレプリケーション: 複製するテーブルの数が 100,000 を超えます。
-   頻繁な DDL 操作によるレイテンシーの発生: DDL ステートメントを頻繁に実行すると、レプリケーションのレイテンシーが大幅に増加します。

## 新機能 {#new-features}

新しいアーキテクチャは、 MySQLシンクの**テーブルレベルのタスク分割を**サポートします。この機能を有効にするには、changefeed設定で`scheduler.enable-table-across-nodes = true`設定します。

この機能を有効にすると、TiCDCは、以下のいずれかの条件を満たすテーブルを**、主キーが1つだけ、またはNULL以外の一意キーを**持つテーブルに自動的に分割し、複数のノードに分散して並列レプリケーションを実行します。これにより、レプリケーションの効率とリソース利用率が向上します。

-   テーブルのリージョン数が設定されたしきい値 (デフォルトでは`100000`ですが、 `scheduler.region-threshold`で調整可能) を超えています。
-   テーブル書き込みトラフィックが設定されたしきい値を超えています (デフォルトでは無効、 `scheduler.write-key-threshold`で設定可能)。

## 互換性 {#compatibility}

### DDL 進捗追跡テーブル {#ddl-progress-tracking-table}

TiCDCの従来のアーキテクチャでは、DDLレプリケーション操作は厳密にシリアル化されているため、レプリケーションの進行状況は変更フィードの`CheckpointTs`を使用してのみ追跡できます。しかし、新しいアーキテクチャでは、TiCDCは可能な限り異なるテーブルのDDL変更を並列にレプリケートすることで、DDLレプリケーションの効率を向上させます。下流のMySQL互換データベースの各テーブルのDDLレプリケーションの進行状況を正確に記録するために、TiCDCの新しいアーキテクチャは下流データベースに`tidb_cdc.ddl_ts_v1`という名前のテーブルを作成し、変更フィードのDDLレプリケーションの進行状況情報を具体的に保存します。

### DDLレプリケーション動作の変更 {#changes-in-ddl-replication-behavior}

-   従来のTiCDCアーキテクチャでは、テーブル名を入れ替えるDDL（例： `RENAME TABLE a TO c, b TO a, c TO b;` ）はサポートされていません。新しいアーキテクチャでは、このようなDDLがサポートされています。

-   新しいアーキテクチャでは、 `RENAME` DDL のフィルタリング ルールが統合され、簡素化されます。

    -   クラシックアーキテクチャでは、フィルタリング ロジックは次のようになります。

        -   単一テーブルの名前変更: 古いテーブル名がフィルター ルールと一致する場合にのみ、DDL ステートメントが複製されます。
        -   複数テーブルの名前変更: 古いテーブル名と新しいテーブル名の両方がフィルター ルールに一致する場合にのみ、DDL ステートメントが複製されます。

    -   新しいアーキテクチャでは、単一テーブルと複数テーブルの両方の名前変更において、ステートメント内の古いテーブル名がフィルター ルールと一致する限り、DDL ステートメントが複製されます。

        次のフィルタ ルールを例に挙げます。

        ```toml
        [filter]
        rules = ['test.t*']
        ```

        -   クラシックアーキテクチャの場合： `RENAME TABLE test.t1 TO ignore.t1`のような単一テーブルの名前変更では、古いテーブル名`test.t1`ルールに一致するため、レプリケートされます。5 `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`ような複数テーブルの名前変更では、新しいテーブル名`ignore.t1`ルールに一致しないため、レプリケートされません。
        -   新しい TiCDCアーキテクチャでは、 `RENAME TABLE test.t1 TO ignore.t1`と`RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`の両方の古いテーブル名がルールに一致するため、両方の DDL ステートメントが複製されます。

## 制限事項 {#limitations}

新しいTiCDCアーキテクチャには、従来のアーキテクチャのすべての機能が組み込まれています。ただし、一部の機能はまだ完全にテストされていません。システムの安定性を確保するため、以下の機能は本番本番環境での使用は推奨さ**れません**。

-   [同期ポイント](/ticdc/ticdc-upstream-downstream-check.md)
-   [再実行ログ](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)
-   [パルサーシンク](/ticdc/ticdc-sink-to-pulsar.md)
-   [収納シンク](/ticdc/ticdc-sink-to-cloud-storage.md)

さらに、新しいTiCDCアーキテクチャは現在、ダウンストリームレプリケーションのために大規模なトランザクションを複数のバッチに分割することをサポートしていません。そのため、非常に大規模なトランザクションを処理する際には、依然としてOOMのリスクが存在します。新しいアーキテクチャを使用する前に、このリスクを適切に評価し、軽減するようにしてください。

## アップグレードガイド {#upgrade-guide}

新しいアーキテクチャの TiCDC は、TiDB クラスター v7.5.0 以降にのみ導入できます。導入前に、TiDB クラスターがこの要件を満たしていることを確認してください。

TiUPまたはTiDB Operator を使用して、新しいアーキテクチャに TiCDC ノードをデプロイできます。

### 新しいアーキテクチャで TiCDC ノードを使用して新しい TiDB クラスターをデプロイ {#deploy-a-new-tidb-cluster-with-ticdc-nodes-in-the-new-architecture}

<SimpleTab>
<div label="TiUP">

TiUPを使用して v8.5.4 以降の新しい TiDB クラスターをデプロイする際に、同時に新しいアーキテクチャの TiCDC ノードもデプロイできます。これを行うには、 TiUP がTiDB クラスターの起動に使用する設定ファイルに TiCDC 関連のセクションを追加し、 `newarch: true`設定するだけです。以下は例です。

```yaml
cdc_servers:
  - host: 10.0.1.20
    config:
      newarch: true
  - host: 10.0.1.21
    config:
      newarch: true
```

TiCDC の展開の詳細については、 [TiUPを使用して TiCDC を含む新しい TiDB クラスターをデプロイ。](/ticdc/deploy-ticdc.md#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup)参照してください。

</div>
<div label="TiDB Operator">

TiDB Operator を使用して v8.5.4 以降の新しい TiDB クラスターをデプロイする際に、同時に新しいアーキテクチャの TiCDC ノードもデプロイできます。そのためには、クラスター設定ファイルに TiCDC 関連のセクションを追加し、 `newarch = true`設定するだけです。以下は例です。

```yaml
spec:
  ticdc:
    baseImage: pingcap/ticdc
    version: v8.5.4
    replicas: 3
    config:
      newarch = true
```

TiCDC の展開の詳細については、 [新しい TiCDC の展開](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-ticdc/#fresh-ticdc-deployment)参照してください。

</div>
</SimpleTab>

### 既存の TiDB クラスタに新しいアーキテクチャの TiCDC ノードをデプロイ {#deploy-ticdc-nodes-in-the-new-architecture-in-an-existing-tidb-cluster}

<SimpleTab>
<div label="TiUP">

TiUPを使用して新しいアーキテクチャに TiCDC ノードを展開するには、次の手順を実行します。

1.  TiDBクラスターにまだTiCDCノードが存在しない場合は、 [TiCDC クラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster)を参照してクラスターに新しいTiCDCノードを追加してください。そうでない場合は、この手順をスキップしてください。

2.  TiDBクラスタのバージョンがv8.5.4より前の場合は、新しいアーキテクチャのTiCDCバイナリパッケージを手動でダウンロードし、ダウンロードしたファイルをTiDBクラスタにパッチ適用する必要があります。それ以外の場合は、この手順をスキップしてください。

    ダウンロード リンクの形式は`https://tiup-mirrors.pingcap.com/cdc-${version}-${os}-${arch}.tar.gz`です`${version}`は TiCDC のバージョン (使用可能なバージョンについては[新しいアーキテクチャ向けのTiCDCリリース](https://github.com/pingcap/ticdc/releases)参照)、 `${os}`はオペレーティング システム、 `${arch}`はコンポーネントが実行されるプラットフォーム ( `amd64`または`arm64` ) です。

    たとえば、Linux (x86-64) 用の TiCDC v8.5.4-release.1 のバイナリ パッケージをダウンロードするには、次のコマンドを実行します。

    ```shell
    wget https://tiup-mirrors.pingcap.com/cdc-v8.5.4-release.1-linux-amd64.tar.gz
    ```

3.  TiDB クラスターで変更フィードが実行中の場合は、 [レプリケーションタスクを一時停止する](/ticdc/ticdc-manage-changefeed.md#pause-a-replication-task)を参照して、変更フィードのすべてのレプリケーション タスクを一時停止します。

    ```shell
    # The default server port of TiCDC is 8300.
    cdc cli changefeed pause --server=http://<ticdc-host>:8300 --changefeed-id <changefeed-name>
    ```

4.  [`tiup cluster patch`](/tiup/tiup-component-cluster-patch.md)コマンドを使用して、ダウンロードした TiCDC バイナリ ファイルを TiDB クラスターにパッチ適用します。

    ```shell
    tiup cluster patch <cluster-name> ./cdc-v8.5.4-release.1-linux-amd64.tar.gz -R cdc --overwrite
    ```

5.  新しいアーキテクチャを有効にするには、 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用して TiCDC 構成を更新します。

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

TiDB Operatorを使用して既存の TiDB クラスターに新しいアーキテクチャの TiCDC ノードをデプロイするには、次の手順を実行します。

-   TiDBクラスタにTiCDCコンポーネントが含まれていない場合は、 [既存の TiDB クラスターに TiCDC を追加する](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-ticdc/#add-ticdc-to-an-existing-tidb-cluster)参照して新しいTiCDCノードを追加してください。その際、クラスタ構成ファイルで新しいアーキテクチャバージョンとしてTiCDCイメージバージョンを指定してください。使用可能なバージョンについては、 [新しいアーキテクチャ向けのTiCDCリリース](https://github.com/pingcap/ticdc/releases)参照してください。

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

-   TiDB クラスターにすでに TiCDCコンポーネントが含まれている場合は、次の手順を実行します。

    1.  TiDB クラスターで変更フィードが実行されている場合は、変更フィードのすべてのレプリケーション タスクを一時停止します。

        ```shell
        kubectl exec -it ${pod_name} -n ${namespace} -- sh
        ```

        ```shell
        # The default server port of TiCDC deployed via TiDB Operator is 8301.
        /cdc cli changefeed pause --server=http://127.0.0.1:8301 --changefeed-id <changefeed-name>
        ```

    2.  クラスター構成ファイル内の TiCDC イメージ バージョンを新しいアーキテクチャバージョンに更新します。

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

    3.  変更フィードのすべてのレプリケーション タスクを再開します。

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

新しいアーキテクチャでTiCDCノードをデプロイした後も、クラシックアーキテクチャと同じコマンドを引き続き使用できます。新しいコマンドを学習したり、クラシックアーキテクチャで使用されていたコマンドを変更したりする必要はありません。

たとえば、新しいアーキテクチャで新しい TiCDC ノードのレプリケーション タスクを作成するには、次のコマンドを実行します。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

特定のレプリケーション タスクの詳細を照会するには、次のコマンドを実行します。

```shell
cdc cli changefeed query -s --server=http://127.0.0.1:8300 --changefeed-id=simple-replication-task
```

コマンドの使用方法や詳細については、 [チェンジフィードを管理する](/ticdc/ticdc-manage-changefeed.md)参照してください。

## 監視 {#monitoring}

新しいアーキテクチャにおけるTiCDCの監視ダッシュボードは**TiCDC-New-Arch**です。v8.5.4以降のバージョンのTiDBクラスターでは、この監視ダッシュボードはクラスターのデプロイまたはアップグレード時にGrafanaに統合されるため、手動操作は不要です。v8.5.4より前のバージョンのクラスターをご利用の場合は、監視を有効にするために[TiCDC 監視メトリックファイル](https://github.com/pingcap/ticdc/blob/master/metrics/grafana/ticdc_new_arch.json)手動でインポートする必要があります。

インポート手順と各監視メトリックの詳細な説明については、 [新しいアーキテクチャにおける TiCDC のメトリクス](/ticdc/monitor-ticdc.md#metrics-for-ticdc-in-the-new-architecture)参照してください。
