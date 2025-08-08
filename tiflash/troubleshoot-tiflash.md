---
title: Troubleshoot a TiFlash Cluster
summary: TiFlashクラスターのトラブルシューティングを行う際の一般的な操作を学習します。
---

# TiFlashクラスタのトラブルシューティング {#troubleshoot-a-tiflash-cluster}

このセクションでは、 TiFlashの使用時によく発生する問題、その原因、および解決策について説明します。

## TiFlashが起動に失敗する {#tiflash-fails-to-start}

TiFlash は様々な理由により正常に起動しない場合があります。以下の手順に従って、段階的に問題を解決してください。

1.  システムが CentOS 8 かどうかを確認します。

    CentOS 8にはデフォルトでシステムライブラリ`libnsl.so`含まれていないため、 TiFlashの起動に失敗する可能性があります。以下のコマンドで手動でインストールできます。

    ```shell
    dnf install libnsl
    ```

2.  システムの`ulimit`パラメータ設定を確認してください。

    ```shell
    ulimit -n 1000000
    ```

3.  PD Controlツールを使用して、ノード（同じIPとポート）上でオフライン化に失敗したTiFlashインスタンスがあるかどうかを確認し、インスタンスを強制的にオフライン化します。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

4.  CPU が SIMD 命令をサポートしているかどうかを確認します。

    バージョン6.3以降、Linux AMD64アーキテクチャでTiFlashを展開するには、AVX2命令セットをサポートするCPUが必要です。1 `grep avx2 /proc/cpuinfo`出力が生成されることを確認して検証してください。Linux ARM64アーキテクチャの場合、CPUはARMv8命令セットアーキテクチャをサポートしている必要があります。3 `grep 'crc32' /proc/cpuinfo | grep 'asimd'`出力が生成されることを確認して検証してください。

    仮想マシンにデプロイするときにこの問題が発生した場合は、VM の CPUアーキテクチャを Haswell に変更してから、 TiFlash を再デプロイしてみてください。

上記の方法で問題を解決できない場合は、PingCAP またはコミュニティからTiFlashログ ファイルと[サポートを受ける](/support.md)収集します。

## 一部のクエリでは<code>Region Unavailable</code>エラーが返されます。 {#some-queries-return-the-code-region-unavailable-code-error}

TiFlashのワークロードが大きすぎてTiFlashデータのレプリケーションが遅れる場合、一部のクエリでエラー`Region Unavailable`が返されることがあります。

この場合、ワークロードを[TiFlashノードの追加](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)ずつバランスさせることができます。

## データファイルの破損 {#data-file-corruption}

データ ファイルの破損を処理するには、次の手順に従います。

1.  対応するTiFlashノードを停止するには、 [TiFlashノードをダウンさせる](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。
2.  TiFlashノードの関連データを削除します。
3.  クラスター内のTiFlashノードを再デプロイします。

## TiFlashノードの削除は遅い {#removing-tiflash-nodes-is-slow}

この問題を解決するには、次の手順に従います。

1.  クラスターのスケールイン後に利用可能なTiFlashノードの数よりも多くのTiFlashレプリカがあるテーブルがあるかどうかを確認します。

    ```sql
    SELECT * FROM information_schema.tiflash_replica WHERE REPLICA_COUNT > 'tobe_left_nodes';
    ```

    `tobe_left_nodes`はスケールイン後のTiFlashノードの数です。

    クエリ結果が空でない場合は、対応するテーブルのTiFlashレプリカ数を変更する必要があります。スケールイン後にTiFlashレプリカ数がTiFlashノード数を超えると、PDは削除対象のTiFlashノードからリージョンピアを移動せず、これらのTiFlashノードの削除が失敗するためです。

2.  すべてのTiFlashノードをクラスターから削除する必要があるシナリオで、表`INFORMATION_SCHEMA.TIFLASH_REPLICA`にクラスター内にTiFlashレプリカが存在しないことが示されていても、 TiFlashノードの削除が依然として失敗する場合は、最近`DROP TABLE <db-name>.<table-name>`または`DROP DATABASE <db-name>`操作を実行したかどうかを確認します。

    TiFlashレプリカを持つテーブルまたはデータベースの場合、 `DROP TABLE <db-name>.<table-name>`または`DROP DATABASE <db-name>`実行した後、TiDBはPD内の対応するテーブルのTiFlashレプリケーションルールをすぐに削除しません。代わりに、対応するテーブルがガベージコレクション（GC）条件を満たすまで待機してから、これらのレプリケーションルールを削除します。GCが完了すると、対応するTiFlashノードを正常に削除できます。

    GC 条件が満たされる前にTiFlashのデータ複製ルールを手動で削除するには、次の操作を実行できます。

    > **注記：**
    >
    > テーブルのTiFlashレプリケーション ルールを手動で削除した後、このテーブルに対して`RECOVER TABLE` 、または`FLASHBACK DATABASE` `FLASHBACK TABLE`を実行すると、このテーブルのTiFlashレプリカは復元されません。

    1.  現在の PD インスタンス内のTiFlashに関連するすべてのデータ複製ルールをビュー。

        ```shell
        curl http://<pd_ip>:<pd_port>/pd/api/v1/config/rules/group/tiflash
        ```

            [
              {
                "group_id": "tiflash",
                "id": "table-45-r",
                "override": true,
                "start_key": "7480000000000000FF2D5F720000000000FA",
                "end_key": "7480000000000000FF2E00000000000000F8",
                "role": "learner",
                "count": 1,
                "label_constraints": [
                  {
                    "key": "engine",
                    "op": "in",
                    "values": [
                      "tiflash"
                    ]
                  }
                ]
              }
            ]

    2.  TiFlashに関連するすべてのデータ複製ルールを削除します。例えば、 `id`が`table-45-r`であるルールを例に挙げます。以下のコマンドで削除します。

        ```shell
        curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
        ```

## TiFlash分析は遅い {#tiflash-analysis-is-slow}

ステートメントにMPPモードでサポートされていない演算子または関数が含まれている場合、TiDBはMPPモードを選択しません。そのため、ステートメントの解析速度が低下します。この場合、 `EXPLAIN`ステートメントを実行して、MPPモードでサポートされていない演算子または関数の有無を確認できます。

```sql
create table t(a datetime);
alter table t set tiflash replica 1;
insert into t values('2022-01-13');
set @@session.tidb_enforce_mpp=1;
explain select count(*) from t where subtime(a, '12:00:00') > '2022-01-01' group by a;
show warnings;
```

この例では、警告メッセージは、TiDB 5.4 以前のバージョンでは`subtime`関数がサポートされていないため、TiDB が MPP モードを選択しないことを示しています。

    +---------+------+-----------------------------------------------------------------------------+
    | Level   | Code | Message                                                                     |
    +---------+------+-----------------------------------------------------------------------------+
    | Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
    +---------+------+-----------------------------------------------------------------------------+

## TiFlashレプリカは常に利用できません {#tiflash-replica-is-always-unavailable}

TiDB クラスターを展開した後、 TiFlashレプリカの作成が継続的に失敗するか、 TiFlashレプリカが最初は正常に作成されたものの、一定期間後にすべてまたは一部のテーブルの作成に失敗した場合は、次の操作を実行して問題をトラブルシューティングできます。

1.  PDの[配置ルール](/configure-placement-rules.md)機能が有効になっているかどうかを確認します。v5.0以降、この機能はデフォルトで有効になっています。

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    -   `true`が返された場合は、次のステップに進みます。
    -   `false`が返された場合は[配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)返して次のステップに進みます。

2.  **TiFlash -Summary** Grafana パネルの**UpTime**メトリックをチェックして、 TiFlashプロセスが正常に動作しているかどうかを確認します。

3.  TiFlashとPD間の接続が正常かどうかを確認します。

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} store
    ```

    TiFlashの`store.labels` `{"key": "engine", "value": "tiflash"}`ような情報が含まれています。この情報を確認することで、 TiFlashのインスタンスを確認できます。

4.  `default` ID を持つ配置ルールの`count`正しいかどうかを確認します。

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} config placement-rules show | grep -C 10 default
    ```

    -   値`count`がクラスター内の TiKV ノードの数以下の場合は、次の手順に進みます。

    -   `count`の値がクラスタ内の TiKV ノードの数より大きい場合（例えば、テストクラスタに TiKV ノードが 1 つしかなく、 `count`が`3`場合）、PD はTiFlashノードにリージョンピアを追加しません。この問題に対処するには、 `count`クラスタ内の TiKV ノードの数以下の整数に変更してください。

    > **注記：**
    >
    > デフォルト値は`count`で、 `3`です。本番環境では、通常、この値は TiKV ノードの数よりも小さくなります。テスト環境で、リージョンレプリカが 1 つだけで問題ない場合は、この値を`1`に設定できます。

    ```shell
        curl -X POST -d '{
            "group_id": "pd",
            "id": "default",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 3,
            "location_labels": [
            "host"
            ]
        }' <http://172.16.x.xxx:2379/pd/api/v1/config/rule>
    ```

5.  TiFlashノードの残りのディスク容量の割合を確認します。

    TiFlashノードのディスク使用量が[`low-space-ratio`](/pd-configuration-file.md#low-space-ratio) （デフォルト： `0.8` ）を超えると、PDはディスク枯渇を防ぐため、そのノードへの新規データのスケジュールを停止します。すべてのTiFlashノードの空きディスク容量が不足している場合、PDはTiFlashへの新規リージョンピアのスケジュール設定ができないため、レプリカが利用できない状態（つまり、progress &lt; 1）になります。

    -   ディスク使用量が`low-space-ratio`以上になった場合、ディスク容量が不足していることを示します。この場合、以下のいずれかの対処を行ってください。

        -   値を`low-space-ratio`に変更すると、PD は新しいしきい値に達するまでTiFlashノードへの領域のスケジュールを再開できるようになります。

                tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} config set low-space-ratio 0.9

        -   新しいTiFlashノードをスケールアウトします。PD はTiFlashノード間でリージョンのバランスを自動的に取り、十分なディスク容量を持つTiFlashノードへのリージョンのスケジュールを再開します。

        -   TiFlashノードディスクから、ログファイルやディレクトリ`${data}/flash/`の`space_placeholder_file`ファイルなどの不要なファイルを削除します。必要に応じて、 `tiflash-learner.toml` ～ `0MB`の`storage.reserve-space`同時に設定し、 TiFlashサービスを一時的に再開します。

    ディスク使用量が`low-space-ratio`未満の場合は、ディスク容量が通常通り利用可能であることを示します。次の手順に進みます。

6.  `down peer`があるかどうかを確認します。

    ダウンしているピアが残っていると、レプリケーションが停止する可能性があります。以下のコマンドを実行して、 `down peer`残っているかどうかを確認してください。

    ```shell
    pd-ctl region check-down-peer
    ```

    ある場合は、次のコマンドを実行して削除します。

    ```shell
    pd-ctl operator add remove-peer <region-id> <tiflash-store-id>
    ```

上記のすべてのチェックに合格しても問題が解決しない場合は、 [データはTiFlashに複製されません](#data-is-not-replicated-to-tiflash)の手順に従って、どのコンポーネントまたはデータ レプリケーション プロセスで問題が発生しているかを特定します。

## データはTiFlashに複製されません {#data-is-not-replicated-to-tiflash}

TiFlashノードをデプロイし、 `ALTER TABLE ... SET TIFLASH REPLICA ...`実行してレプリケーションを開始したにもかかわらず、データが複製されません。この場合、次の手順を実行することで問題を特定し、対処できます。

1.  `ALTER TABLE ... SET TIFLASH REPLICA ...<num>`実行してレプリケーションが成功したかどうかを確認し、出力を確認します。

    -   クエリがブロックされている場合は、 `SELECT * FROM information_schema.tiflash_replica`ステートメントを実行して、 TiFlashレプリカが作成されたかどうかを確認します。
        -   [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)を通じて、DDL 文が期待どおりに実行されているかどうかを確認します。TiFlash レプリカ文のTiFlashをブロックする可能性のある他の DDL 文 ( `ADD INDEX`など) が実行中かどうかを確認します。
        -   実行中のTiFlashレプリカ ステートメントの変更をブロックする[`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md)を通じて、同じテーブルで DML ステートメントが実行されているかどうかを確認します。
    -   ブロッキングステートメントが完了するかキャンセルされるまで待ってから、 TiFlashレプリカの設定を再度試してください。問題が発生しない場合は、次の手順に進みます。

2.  TiFlashリージョンレプリケーションが正しく実行されているかどうかを確認します。

    [`information_schema.tiflash_replica`](/information-schema/information-schema-tiflash-replica.md)テーブルをクエリして、 TiFlashレプリカのレプリケーションの進行状況を示す`PROGRESS`フィールドが変化しているかどうかを確認します。または、 `tidb.log`ファイルでキーワード`Tiflash replica is not available`を検索して、関連ログと対応する`progress`値を確認します。

    -   レプリケーションの進行状況が変化する場合、 TiFlashレプリケーションは正常に機能しているものの、速度が遅くなっている可能性があります。最適化設定については、 [データの複製が遅い](#data-replication-is-slow)を参照してください。
    -   レプリケーションの進行状況に変化がない場合、 TiFlashレプリケーションは異常です。次の手順に進んでください。

3.  TiDB がテーブルの配置ルールを正常に作成したかどうかを確認します。

    TiDB DDL 所有者のログを検索し、TiDB が PD に配置ルールを追加するように通知したかどうかを確認します。

    -   パーティション化されていないテーブルの場合は、 `ConfigureTiFlashPDForTable`検索します。

    -   パーティション化されたテーブルの場合は、 `ConfigureTiFlashPDForPartitions`検索します。

    -   キーワードが見つかった場合は、次のステップに進みます。

    -   見つからない場合は、該当するコンポーネントのログを[サポートを受ける](/support.md)に収集します。

4.  PD がテーブルの配置ルールを設定しているかどうかを確認します。

    現在の PD 上のすべてのTiFlash配置ルールを表示するには、次のコマンドを実行します。

    ```shell
    curl http://<pd-ip>:<pd-port>/pd/api/v1/config/rules/group/tiflash
    ```

    -   ID形式が`table-<table_id>-r`ルールが存在する場合、PDは配置ルールを正常に設定しています。次の手順に進みます。
    -   そのようなルールが存在しない場合は、対応するコンポーネントのログを[サポートを受ける](/support.md)に収集します。

5.  PD が適切にスケジュールされているかどうかを確認します。

    `pd.log`ファイルで`table-<table_id>-r`というキーワードを検索し、 `add operator`ようなスケジューリングログを見つけてください。または、Grafana の PD ダッシュボードの**Operator/Schedule オペレータ作成で**`add-rule-peer`オペレータが存在するかどうかを確認してください。また、Grafana の PD ダッシュボードで**Scheduler/Patrol リージョン時間の**値を確認することもできます。Patrol **リージョン時間は、PD がすべてのリージョンをスキャンしてスケジューリング操作を生成するまでの所要時間です。値が大きいと、**スケジューリングに遅延が発生する可能性があります。

    -   `pd.log`キーワード`table-<table_id>-r`と`add operator`スケジュール ログが含まれている場合、または**Scheduler/Patrol リージョン時間**パネルの期間値が正常に表示される場合は、PD スケジュールが適切に機能していることを示します。
    -   `add-rule-peer`スケジュールログが見つからない場合、または**パトロールリージョンの時間**が30分を超える場合、PD はスケジュールを正しく実行していないか、スケジュールの実行に時間がかかっています。TiDB、PD、およびTiFlash のログファイルを[サポートを受ける](/support.md)に収集してください。

上記の方法で問題を解決できない場合は、TiDB、PD、およびTiFlashログ ファイルと[サポートを受ける](/support.md) PingCAP またはコミュニティから収集します。

## データの複製が遅い {#data-replication-is-slow}

原因はさまざまです。次の手順を実行することで問題を解決できます。

1.  レプリケーションを高速化するには、 [TiFlashレプリケーションの高速化](/tiflash/create-tiflash-replicas.md#speed-up-tiflash-replication)に従います。

2.  TiFlashの負荷を調整します。

    TiFlashへの負荷が高すぎると、レプリケーションが遅くなる場合があります。Grafanaの**TiFlash -Summary**パネルで、 TiFlashインジケーターの負荷を確認できます。

    -   `Applying snapshots Count` ： `TiFlash-summary` &gt; `raft` &gt; `Applying snapshots Count`
    -   `Snapshot Predecode Duration` ： `TiFlash-summary` &gt; `raft` &gt; `Snapshot Predecode Duration`
    -   `Snapshot Flush Duration` ： `TiFlash-summary` &gt; `raft` &gt; `Snapshot Flush Duration`
    -   `Write Stall Duration` ： `TiFlash-summary` &gt; `Storage Write Stall` &gt; `Write Stall Duration`
    -   `generate snapshot CPU` ： `TiFlash-Proxy-Details` &gt; `Thread CPU` &gt; `Region task worker pre-handle/generate snapshot CPU`

    サービスの優先順位に基づいて負荷を調整し、最適なパフォーマンスを実現します。
