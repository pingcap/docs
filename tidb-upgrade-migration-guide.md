---
title: Migrate and Upgrade a TiDB Cluster
summary: 完全バックアップと復元にBRを使用し、増分データ レプリケーションに TiCDC を使用して、TiDB クラスターを移行およびアップグレードする方法を学習します。
---

# TiDBクラスタの移行とアップグレード {#migrate-and-upgrade-a-tidb-cluster}

このドキュメントでは、 [BR](/br/backup-and-restore-overview.md)で完全バックアップと復元を行い、 [ティCDC](/ticdc/ticdc-overview.md)で増分データ レプリケーションを行って、TiDB クラスターを移行およびアップグレードする方法について説明します (ブルーグリーン アップグレードとも呼ばれます)。このソリューションでは、デュアル クラスターの冗長性と増分レプリケーションを使用して、スムーズなトラフィック切り替えと高速ロールバックを実現し、重要なシステムに信頼性が高くリスクの少ないアップグレード パスを提供します。パフォーマンスの向上と新機能のメリットを継続的に享受し、安全で効率的なデータベース システムを維持するために、データベース バージョンを定期的にアップグレードすることをお勧めします。このソリューションの主な利点は次のとおりです。

-   **制御可能なリスク**: 数分以内に元のクラスターへのロールバックをサポートし、ビジネスの継続性を確保します。
-   **データの整合性**: データの損失を防ぐために、多段階の検証メカニズムを使用します。
-   **ビジネスへの影響は最小限**: 最終的な切り替えには短いメンテナンス期間のみが必要です。

移行とアップグレードのコアワークフローは次のとおりです。

1.  **リスクの事前チェック**: クラスターの状態とソリューションの実現可能性を確認します。
2.  **新しいクラスターを準備します**。古いクラスターの完全バックアップから新しいクラスターを作成し、それをターゲット バージョンにアップグレードします。
3.  **増分データを複製する**: TiCDC を使用してフォワード データ レプリケーション チャネルを確立します。
4.  **切り替えと検証**: 多次元検証を実行し、ビジネス トラフィックを新しいクラスターに切り替え、TiCDC リバース レプリケーション チャネルを設定します。
5.  **ステータスを観察**: リバース レプリケーション チャネルを維持します。観察期間後、環境をクリーンアップします。

**ロールバック プラン**: 移行およびアップグレード プロセス中に新しいクラスターで問題が発生した場合、いつでもビジネス トラフィックを元のクラスターに戻すことができます。

次のセクションでは、TiDB クラスターの移行とアップグレードの標準化されたプロセスと一般的な手順について説明します。サンプル コマンドは、TiDB セルフマネージド環境に基づいています。

## ステップ1: ソリューションの実現可能性を評価する {#step-1-evaluate-solution-feasibility}

移行およびアップグレードを行う前に、関連するコンポーネントの互換性を評価し、クラスターの健全性ステータスを確認してください。

-   TiDB クラスターのバージョンを確認します。このソリューションは、TiDB v6.5.0 以降のバージョンに適用されます。

-   TiCDC の互換性を確認します。

    -   **テーブル スキーマの要件**: 複製するテーブルに有効なインデックスが含まれていることを確認します。詳細については、 [TiCDC 有効インデックス](/ticdc/ticdc-overview.md#best-practices)参照してください。
    -   **機能制限**: TiCDC はシーケンスまたはTiFlash DDL レプリケーションをサポートしていません。詳細については、 [TiCDC がサポートしていないシナリオ](/ticdc/ticdc-overview.md#unsupported-scenarios)参照してください。
    -   **ベスト プラクティス**: スイッチオーバー中に TiCDC のアップストリーム クラスターで DDL 操作を実行しないでください。

-   BR互換性を確認します。

    -   BRフルバックアップの互換性マトリックスを確認してください。詳細については、 [BRバージョン互換性マトリックス](/br/backup-and-restore-overview.md#version-compatibility)参照してください。
    -   BRバックアップと復元の既知の制限事項を確認してください。詳細については、 [BRの使用制限](/br/backup-and-restore-overview.md#restrictions)参照してください。

-   [リージョン](/glossary.md#regionpeerraft-group)健全性やノードのリソース使用率など、クラスターの健全性ステータスを確認します。

## ステップ2: 新しいクラスターを準備する {#step-2-prepare-the-new-cluster}

### 1. 古いクラスタのGC有効期間を調整する {#1-adjust-the-gc-lifetime-of-the-old-cluster}

データ レプリケーションの安定性を確保するには、システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) 、 BRバックアップ、 BR復元、クラスター アップグレード、およびTiCDC Changefeedレプリケーション セットアップの操作と間隔の合計期間をカバーする値に調整します。そうしないと、レプリケーション タスクが回復不能な`failed`状態になり、新しい完全バックアップから移行およびアップグレード プロセス全体を再起動する必要が生じる可能性があります。

次の例では、 `tidb_gc_life_time`を`60h`に設定します。

```sql
-- Check the current GC lifetime setting.
SHOW VARIABLES LIKE '%tidb_gc_life_time%';
-- Set GC lifetime.
SET GLOBAL tidb_gc_life_time=60h;
```

> **注記：**
>
> `tidb_gc_life_time`増やすと、 [MVCC](/glossary.md#multi-version-concurrency-control-mvcc)データのstorage使用量が増加し、クエリのパフォーマンスに影響する可能性があります。詳細については、 [GC の概要](/garbage-collection-overview.md)参照してください。storageとパフォーマンスへの影響を考慮しながら、推定操作時間に基づいて GC 期間を調整します。

### 2. 新しいクラスターに全データを移行する {#2-migrate-full-data-to-the-new-cluster}

完全なデータを新しいクラスターに移行するときは、次の点に注意してください。

-   **バージョンの互換性**: バックアップと復元に使用されるBRバージョンは、古いクラスターのメジャー バージョンと一致する必要があります。

-   **パフォーマンスへの影響**: BRバックアップはシステム リソースを消費します。ビジネスへの影響を最小限に抑えるには、オフピーク時にバックアップを実行します。

-   **時間の見積もり**: 最適なハードウェア条件 (ディスク I/O またはネットワーク帯域幅のボトルネックなし) では、推定時間は次のとおりです。

    -   バックアップ速度: 8 つのスレッドで TiKV ノードごとに 1 TiB のデータのバックアップに約 1 時間かかります。
    -   復元速度: TiKV ノードごとに 1 TiB のデータの復元には約 20 分かかります。

-   **コンフィグレーションの一貫性**: 古いクラスターと新しいクラスター間で[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)構成が同一であることを確認します。そうでない場合、 BR の復元は失敗します。

-   **システム テーブルの復元**: BR復元中に`--with-sys-table`オプションを使用して、システム テーブル データを復元します。

完全なデータを新しいクラスターに移行するには、次の手順を実行します。

1.  古いクラスターで完全バックアップを実行します。

    ```shell
    tiup br:${cluster_version} backup full --pd ${pd_host}:${pd_port} -s ${backup_location}
    ```

2.  後でTiCDC Changefeed を作成するために、古いクラスターの TSO を記録します。

    ```shell
    tiup br:${cluster_version} validate decode --field="end-version" \
    --storage "s3://xxx?access-key=${access-key}&secret-access-key=${secret-access-key}" | tail -n1
    ```

3.  新しいクラスターをデプロイ。

    ```shell
    tiup cluster deploy ${new_cluster_name} ${cluster_version} tidb-cluster.yaml
    ```

4.  完全バックアップを新しいクラスターに復元します。

    ```shell
    tiup br:${cluster_version} restore full --pd ${pd_host}:${pd_port} -s ${backup_location} --with-sys-table
    ```

### 3. 新しいクラスターをターゲットバージョンにアップグレードする {#3-upgrade-the-new-cluster-to-the-target-version}

時間を節約するために、次のコマンドを使用してオフライン アップグレードを実行できます。その他のアップグレード方法については、 [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)参照してください。

```shell
tiup cluster stop <new_cluster_name>      # Stop the cluster
tiup cluster upgrade <new_cluster_name> <v_target_version> --offline  # Perform offline upgrade
tiup cluster start <new_cluster_name>     # Start the cluster
```

ビジネスの継続性を維持するには、構成項目やシステム変数などの重要な構成を古いクラスターから新しいクラスターに複製する必要があります。

## ステップ3: 増分データを複製する {#step-3-replicate-incremental-data}

### 1. フォワードデータレプリケーションチャネルを確立する {#1-establish-a-forward-data-replication-channel}

この段階では、古いクラスターは元のバージョンのままですが、新しいクラスターはターゲット バージョンにアップグレードされています。この手順では、古いクラスターから新しいクラスターへの転送データ レプリケーション チャネルを確立する必要があります。

> **注記：**
>
> TiCDCコンポーネントのバージョンは、古いクラスターのメジャー バージョンと一致する必要があります。

-   Changefeedタスクを作成し、データ損失を防ぐために、増分レプリケーションの開始点（ `${tso}` ）を[ステップ2](#step-2-prepare-the-new-cluster)で記録したバックアップTSOとまったく同じに設定します。

    ```shell
    tiup ctl:${cluster_version} cdc changefeed create --server http://${cdc_host}:${cdc_port} --sink-uri="mysql://${username}:${password}@${tidb_endpoint}:${port}" --config config.toml --start-ts ${tso}
    ```

-   レプリケーション タスクのステータスを確認し、 `tso`または`checkpoint`継続的に進んでいることを確認します。

    ```shell
    tiup ctl:${cluster_version} cdc changefeed list --server http://${cdc_host}:${cdc_port}
    ```

    出力は次のようになります。

    ```shell
    [{
        "id": "cdcdb-cdc-task-standby",
        "summary": {
          "state": "normal",
          "tso": 417886179132964865,
          "checkpoint": "202x-xx-xx xx:xx:xx.xxx",
          "error": null
        }
    }]
    ```

増分データ レプリケーション中は、レプリケーション チャネルの状態を継続的に監視し、必要に応じて設定を調整します。

-   レイテンシ メトリック: `Changefeed checkpoint lag` 5 分以内などの許容範囲内に留まることを確認します。
-   スループットの健全性: `Sink flush rows/s`一貫してビジネス書き込みレートを超えていることを確認します。
-   エラーとアラート: TiCDC ログとアラート情報を定期的に確認してください。
-   (オプション) テスト データ レプリケーション: テスト データを更新し、Changefeed がそれを新しいクラスターに正しく複製することを確認します。
-   (オプション) TiCDC 構成項目[`gc-ttl`](/ticdc/ticdc-server-config.md)調整します (デフォルトは 24 時間)。

    レプリケーション タスクが利用できないか中断され、時間内に解決できない場合、 `gc-ttl` 、TiCDC に必要なデータがガベージコレクション(GC) によって消去されることなく TiKV に保持されることを保証します。この期間を超えると、レプリケーション タスクは`failed`状態になり、回復できなくなります。この場合、PD の GC セーフ ポイントは進み続けるため、プロセスを再開するには新しいバックアップが必要になります。

    `gc-ttl`の値を増やすと、 `tidb_gc_life_time`増やすのと同様に、より多くの MVCC データが蓄積されます。適度に長くて適切な値に設定することをお勧めします。

### 2. データの一貫性を確認する {#2-verify-data-consistency}

データのレプリケーションが完了したら、次の方法を使用して、古いクラスターと新しいクラスター間のデータの整合性を確認します。

-   [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)ツールを使用します。

    ```shell
    ./sync_diff_inspector --config=./config.toml
    ```

-   [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)のスナップショット構成を TiCDC の[同期ポイント](/ticdc/ticdc-upstream-downstream-check.md)機能と組み合わせて使用し、Changefeed レプリケーションを停止せずにデータの整合性を検証します。詳細については、 [上流および下流のクラスタデータ検証とスナップショット読み取り](/ticdc/ticdc-upstream-downstream-check.md)参照してください。

-   テーブルの行数の比較など、ビジネス データの手動検証を実行します。

### 3. 環境設定を完了する {#3-finalize-the-environment-setup}

この移行手順では、 BR `--with-sys-table`オプションを使用して一部のシステム テーブル データを復元します。範囲に含まれていないテーブルについては、手動で復元する必要があります。確認および補足する一般的な項目は次のとおりです。

-   ユーザー権限: `mysql.user`テーブルを比較します。
-   コンフィグレーション設定: 構成項目とシステム変数が一貫していることを確認します。
-   自動インクリメント列: 新しいクラスター内の自動インクリメント ID キャッシュをクリアします。
-   統計: 統計を手動で収集するか、新しいクラスターで自動収集を有効にします。

さらに、新しいクラスターをスケールアウトして、予想されるワークロードを処理し、アラート サブスクリプション、スケジュールされた統計収集スクリプト、データ バックアップ スクリプトなどの運用タスクを移行することもできます。

## ステップ4: ビジネストラフィックの切り替えとロールバック {#step-4-switch-business-traffic-and-rollback}

### 1. 切り替えの準備 {#1-prepare-for-the-switchover}

-   レプリケーションステータスを確認します。

    -   TiCDC Changefeedレプリケーションのレイテンシーを監視します。
    -   増分レプリケーションのスループットがピーク時のビジネス書き込み速度以上であることを確認します。

-   次のような多次元検証を実行します。

    -   すべてのデータ検証手順が完了していることを確認し、必要な追加チェックを実行します。
    -   新しいクラスター内のアプリケーションに対して健全性テストまたは統合テストを実行します。

### 2. 切り替えを実行する {#2-execute-the-switchover}

1.  古いクラスターがビジネス トラフィックを処理できないように、アプリケーション サービスを停止します。アクセスをさらに制限するには、次のいずれかの方法を使用できます。

    -   古いクラスター内のユーザー アカウントをロックします。

        ```sql
        ALTER USER ACCOUNT LOCK;
        ```

    -   古いクラスターを読み取り専用モードに設定します。アクティブなビジネス セッションをクリアし、読み取り専用モードに入っていない接続を防止するために、古いクラスター内の TiDB ノードを再起動することをお勧めします。

        ```sql
        SET GLOBAL tidb_super_read_only=ON;
        ```

2.  TiCDC が追いつくようにします:

    -   古いクラスターを読み取り専用モードに設定した後、現在の`up-tso`取得します。

        ```sql
        SELECT tidb_current_ts();
        ```

    -   Changefeed `checkpointTs`監視して、それが`up-tso`超えていることを確認します。これは、TiCDC がデータ複製を完了したことを示します。

3.  新しいクラスターと古いクラスター間のデータの一貫性を確認します。

    -   TiCDC が追いついたら、新しいクラスターから`down-tso`取得します。
    -   [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)ツールを使用して、 `up-tso`と`down-tso`の新しいクラスターと古いクラスター間のデータの一貫性を比較します。

4.  フォワード Changefeed レプリケーション タスクを一時停止します。

    ```shell
    tiup ctl:${cluster_version} cdc changefeed pause --server http://${cdc_host}:${cdc_port} -c <changefeedid>
    ```

5.  新しいクラスター内の TiDB ノードを再起動して、自動増分 ID キャッシュをクリアします。

6.  次の方法を使用して、新しいクラスターの動作ステータスを確認します。

    -   TiDB のバージョンがターゲット バージョンと一致していることを確認します。

        ```shell
        tiup cluster display <cluster-name>
        ```

    -   データベースにログインし、コンポーネントのバージョンを確認します。

        ```sql
        SELECT * FROM INFORMATION_SCHEMA.CLUSTER_INFO;
        ```

    -   Grafana を使用してサービス ステータスを監視します[**概要 &gt; サービス ポート ステータス**](/grafana-overview-dashboard.md)に移動し、すべてのサービスが**Up**状態であることを確認します。

7.  新しいクラスターから古いクラスターへのリバースレプリケーションを設定します。

    1.  古いクラスターのユーザー アカウントのロックを解除し、読み取り/書き込みモードを復元します。

        ```sql
        ALTER USER ACCOUNT UNLOCK;
        SET GLOBAL tidb_super_read_only=OFF;
        ```

    2.  新しいクラスターの現在の TSO を記録します。

        ```sql
        SELECT tidb_current_ts();
        ```

    3.  リバース レプリケーション リンクを構成し、Changefeed タスクが適切に実行されていることを確認します。

        -   この段階では業務が停止しているため、現在の TSO を使用することができます。
        -   ループバック書き込みのリスクを回避するために、古いクラスターのアドレスに`sink-uri`が設定されていることを確認します。

        ```shell
        tiup ctl:${cluster_version} cdc changefeed create --server http://${cdc_host}:${cdc_port} --sink-uri="mysql://${username}:${password}@${tidb_endpoint}:${port}" --config config.toml --start-ts ${tso}

        tiup ctl:${cluster_version} cdc changefeed list --server http://${cdc_host}:${cdc_port}
        ```

8.  ビジネス トラフィックを新しいクラスターにリダイレクトします。

9.  次の Grafana パネルを使用して、新しいクラスターの負荷と動作ステータスを監視します。

    -   [**TiDBダッシュボード &gt; クエリサマリー**](/grafana-tidb-dashboard.md#query-summary) : 期間、QPS、失敗したクエリ OPM メトリックを確認します。
    -   [**TiDBダッシュボード &gt; サーバー**](/grafana-tidb-dashboard.md#server) :**接続数**メトリックを監視して、ノード間で接続が均等に分散されるようにします。

この時点で、ビジネス トラフィックは新しいクラスターに正常に切り替えられ、TiCDC リバース レプリケーション チャネルが確立されます。

### 3. 緊急ロールバックを実行する {#3-execute-emergency-rollback}

ロールバック計画は次のとおりです。

-   新しいクラスターと古いクラスター間のデータの一貫性を定期的にチェックし、リバース レプリケーション リンクが適切に動作していることを確認します。
-   1 週間など、指定された期間にわたってシステムを監視します。問題が発生した場合は、古いクラスターに戻します。
-   観察期間が終了したら、リバース レプリケーション リンクを削除し、古いクラスターを削除します。

以下では、トラフィックを古いクラスターに戻す緊急ロールバックの使用シナリオと手順について説明します。

-   使用シナリオ: 重大な問題を解決できない場合は、ロールバック プランを実行します。
-   手順:

    1.  新しいクラスターへのビジネス アクセスを停止します。
    2.  ビジネス アカウントを再認証し、古いクラスターへの読み取り/書き込みアクセスを復元します。
    3.  リバース レプリケーション リンクをチェックし、TiCDC が追いついていることを確認し、新しいクラスターと古いクラスター間のデータの一貫性を検証します。
    4.  ビジネス トラフィックを古いクラスターにリダイレクトします。

## ステップ5: クリーンアップ {#step-5-clean-up}

新しいクラスターを一定期間監視し、安定した業務運用を確認した後、TiCDC リバース レプリケーションを削除し、古いクラスターを削除できます。

-   TiCDC リバースレプリケーションを削除します。

    ```shell
    tiup ctl:${cluster_version} cdc changefeed remove --server http://${cdc_host}:${cdc_port} -c <changefeedid>
    ```

-   古いクラスターを削除します。保持する場合は、 `tidb_gc_life_time`元の値に戻します。

    ```sql
    -- Restore to the original value before modification.
    SET GLOBAL tidb_gc_life_time=10m;
    ```
