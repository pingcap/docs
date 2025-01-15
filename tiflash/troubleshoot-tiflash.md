---
title: Troubleshoot a TiFlash Cluster
summary: TiFlashクラスターのトラブルシューティングを行う際の一般的な操作を学習します。
---

# TiFlashクラスタのトラブルシューティング {#troubleshoot-a-tiflash-cluster}

このセクションでは、 TiFlashの使用時によく発生する問題、その理由、および解決策について説明します。

## TiFlash が起動に失敗する {#tiflash-fails-to-start}

この問題はさまざまな理由で発生する可能性があります。以下の手順に従ってトラブルシューティングすることをお勧めします。

1.  システムが RedHat Enterprise Linux 8 であるかどうかを確認します。

    RedHat Enterprise Linux 8 には`libnsl.so`システム ライブラリがありません。次のコマンドを使用して手動でインストールできます。

    ```shell
    dnf install libnsl
    ```

2.  システムの`ulimit`のパラメータ設定を確認してください。

    ```shell
    ulimit -n 1000000
    ```

3.  PD Controlツールを使用して、ノード (同じ IP とポート) 上でオフラインに失敗したTiFlashインスタンスがあるかどうかを確認し、インスタンスを強制的にオフラインにします。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

上記の方法で問題を解決できない場合は、 TiFlashログ ファイルと PingCAP またはコミュニティからの[サポートを受ける](/support.md)保存します。

## TiFlashレプリカは常に利用できません {#tiflash-replica-is-always-unavailable}

これは、 TiFlash が構成エラーまたは環境の問題により異常な状態にあるためです。障害のあるコンポーネントを特定するには、次の手順を実行してください。

1.  PD が`Placement Rules`機能を有効にしているかどうかを確認します。

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    -   `true`が返された場合は、次の手順に進みます。
    -   `false`が返された場合は[配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)返して次のステップに進みます。

2.  TiFlash -Summary 監視パネルの`UpTime`を表示して、 TiFlashプロセスが正しく動作しているかどうかを確認します。

3.  `pd-ctl`を通じてTiFlashプロキシの状態が正常かどうかを確認します。

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} store
    ```

    TiFlashプロキシの`store.labels`は`{"key": "engine", "value": "tiflash"}`などの情報が含まれています。この情報を確認することで、 TiFlashプロキシを確認できます。

4.  構成されたレプリカの数が、クラスター内の TiKV ノードの数以下であるかどうかを確認します。そうでない場合、PD はデータをTiFlashに複製できません。

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} config placement-rules show | grep -C 10 default
    ```

    `default: count`の値を再確認します。

    > **注記：**
    >
    > -   [配置ルール](/configure-placement-rules.md)が有効になっていて、複数のルールが存在する場合、以前に構成された[`max-replicas`](/pd-configuration-file.md#max-replicas) 、 [`location-labels`](/pd-configuration-file.md#location-labels) 、および[`isolation-level`](/pd-configuration-file.md#isolation-level)有効になりません。レプリカ ポリシーを調整するには、配置ルールに関連するインターフェイスを使用します。
    > -   [配置ルール](/configure-placement-rules.md)が有効になっていて、デフォルト ルールが 1 つだけ存在する場合、 `max-replicas` 、または`isolation-level` `location-labels`が変更されると、TiDB はこのデフォルト ルールを自動的に更新します。

5.  マシン ( TiFlashノードの`store`があるマシン) の残りのディスク容量が十分かどうかを確認します。デフォルトでは、残りのディスク容量が`store`容量 ( [`low-space-ratio`](/pd-configuration-file.md#low-space-ratio)パラメータによって制御されます) の 20% 未満の場合、PD はこのTiFlashノードにデータをスケジュールできません。

## 一部のクエリでは、 <code>Region Unavailable</code>エラーが返されます。 {#some-queries-return-the-code-region-unavailable-code-error}

TiFlashへの負荷が大きすぎてTiFlashデータのレプリケーションが遅れる場合、一部のクエリで`Region Unavailable`エラーが返されることがあります。

この場合、 TiFlashノードを追加することで負荷圧力をバランスさせることができます。

## データファイルの破損 {#data-file-corruption}

データ ファイルの破損を処理するには、次の手順を実行します。

1.  対応するTiFlashノードを停止するには、 [TiFlashノードをダウンさせる](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。
2.  TiFlashノードの関連データを削除します。
3.  クラスター内のTiFlashノードを再デプロイします。

## TiFlashノードの削除は遅い {#removing-tiflash-nodes-is-slow}

この問題に対処するには、次の手順を実行します。

1.  クラスターのスケールイン後に使用可能なTiFlashノードの数よりも多くのTiFlashレプリカがテーブルに存在するかどうかを確認します。

    ```sql
    SELECT * FROM information_schema.tiflash_replica WHERE REPLICA_COUNT > 'tobe_left_nodes';
    ```

    `tobe_left_nodes`スケールイン後のTiFlashノードの数です。

    クエリ結果が空でない場合は、対応するテーブルのTiFlashレプリカの数を変更する必要があります。これは、スケールイン後にTiFlashレプリカの数がTiFlashノードの数を超えると、PD が削除するTiFlashノードからリージョンピアを移動しないため、これらのTiFlashノードの削除が失敗するためです。

2.  すべてのTiFlashノードをクラスターから削除する必要があるシナリオで、 `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルにクラスター内にTiFlashレプリカが存在しないことが示されていても、 TiFlashノードの削除が依然として失敗する場合は、最近`DROP TABLE <db-name>.<table-name>`または`DROP DATABASE <db-name>`操作を実行したかどうかを確認します。

    TiFlashレプリカを持つテーブルまたはデータベースの場合、 `DROP TABLE <db-name>.<table-name>`または`DROP DATABASE <db-name>`実行した後、TiDB は PD 内の対応するテーブルのTiFlashレプリケーション ルールをすぐに削除しません。代わりに、対応するテーブルがガベージコレクション(GC) 条件を満たすまで待機してから、これらのレプリケーション ルールを削除します。GC が完了すると、対応するTiFlashノードを正常に削除できます。

    GC 条件が満たされる前にTiFlashのデータ複製ルールを手動で削除するには、次の操作を実行します。

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

    2.  TiFlashに関連するすべてのデータ複製ルールを削除します。1 が`id` `table-45-r`あるルールを例にとります。次のコマンドで削除します。

        ```shell
        curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
        ```

## TiFlash分析は遅い {#tiflash-analysis-is-slow}

ステートメントに MPP モードでサポートされていない演算子または関数が含まれている場合、TiDB は MPP モードを選択しません。そのため、ステートメントの分析は遅くなります。この場合、 `EXPLAIN`ステートメントを実行して、MPP モードでサポートされていない演算子または関数をチェックできます。

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
    > | Level   | Code | Message                                                                     |
    +---------+------+-----------------------------------------------------------------------------+
    | Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
    +---------+------+-----------------------------------------------------------------------------+

## データはTiFlashに複製されません {#data-is-not-replicated-to-tiflash}

TiFlashノードをデプロイし、レプリケーションを開始した後 (ALTER 操作を実行して)、そのノードにデータがレプリケートされません。この場合、次の手順に従って問題を特定し、対処できます。

1.  `ALTER table <tbl_name> set tiflash replica <num>`コマンドを実行して出力を確認し、レプリケーションが成功したかどうかを確認します。

    -   出力がある場合は、次の手順に進みます。
    -   出力がない場合は、 `SELECT * FROM information_schema.tiflash_replica`コマンドを実行して、 TiFlashレプリカが作成されたかどうかを確認します。作成されていない場合は、 `ALTER table ${tbl_name} set tiflash replica ${num}`コマンドを再度実行し、他のステートメント (たとえば、 `add index` ) が実行されたかどうか、または DDL 実行が成功したかどうかを確認します。

2.  TiFlashリージョンのレプリケーションが正しく実行されているかどうかを確認します。

    `progress`に変化があるかどうかを確認します。

    -   はいの場合、 TiFlashレプリケーションは正常に実行されます。
    -   いいえの場合、 TiFlashレプリケーションは異常です。 `tidb.log`で、 `Tiflash replica is not available`のログを検索します。対応するテーブルの`progress`が更新されているかどうかを確認します。更新されていない場合は、 `tiflash log`で詳細情報を確認します。たとえば、 `tiflash log`の`lag_region_info`検索して、どのリージョンが遅れているかを確認します。

3.  pd-ctl を使用して、 [配置ルール](/configure-placement-rules.md)機能が有効になっているかどうかを確認します。

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    -   `true`が返された場合は、次の手順に進みます。
    -   `false`が返された場合は[配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)返して次のステップに進みます。

4.  `max-replicas`構成が正しいかどうかを確認します。

    -   値`max-replicas`がクラスター内の TiKV ノードの数を超えない場合は、次の手順に進みます。

    -   `max-replicas`の値がクラスター内の TiKV ノードの数より大きい場合、PD はTiFlashノードにデータを複製しません。この問題を解決するには、 `max-replicas`クラスター内の TiKV ノードの数以下の整数に変更します。

    > **注記：**
    >
    > `max-replicas`はデフォルトで 3 に設定されます。本番環境では、この値は通常 TiKV ノードの数よりも少なくなります。テスト環境では、この値は 1 になる場合があります。

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

5.  TiDB がテーブルの配置ルールを作成したかどうかを確認します。

    TiDB DDL 所有者のログを検索し、TiDB が PD に配置ルールを追加するように通知したかどうかを確認します。パーティション化されていないテーブルの場合は`ConfigureTiFlashPDForTable`検索します。パーティション化されたテーブルの場合は`ConfigureTiFlashPDForPartitions`検索します。

    -   キーワードが見つかった場合は、次の手順に進みます。
    -   そうでない場合は、トラブルシューティングのために、対応するコンポーネントのログを収集します。

6.  PD がテーブルの配置ルールを設定しているかどうかを確認します。

    現在の PD 上のすべてのTiFlash配置ルールを表示するには、 `curl http://<pd-ip>:<pd-port>/pd/api/v1/config/rules/group/tiflash`コマンドを実行します。ID が`table-<table_id>-r`ルールが見つかった場合、PD は配置ルールを正常に構成しています。

7.  PD のスケジュールが適切に設定されているかどうかを確認します。

    `pd.log`ファイルで`table-<table_id>-r`キーワードと`add operator`のようなスケジュール動作を検索します。

    -   キーワードが見つかった場合、PD は適切にスケジュールします。
    -   そうでない場合、PD は適切にスケジュールされません。

## データの複製が停止する {#data-replication-gets-stuck}

TiFlash上のデータ複製が正常に開始されたが、一定期間後にすべてまたは一部のデータの複製に失敗した場合は、次の手順を実行して問題を確認または解決できます。

1.  ディスク容量を確認してください。

    ディスク スペース比率が`low-space-ratio`の値より大きいかどうかを確認します (デフォルトは 0.8 です。ノードのスペース使用率が 80% を超えると、PD はディスク スペースの枯渇を回避するためにこのノードへのデータの移行を停止します)。

    -   ディスク使用率が`low-space-ratio`以上の場合には、ディスク容量が不足しています。ディスク容量を解放するには、 `${data}/flash/`フォルダ以下の`space_placeholder_file`などの不要なファイルを削除してください（必要な場合は、ファイルを削除した後、 `reserve-space` 0MB に設定してください）。
    -   ディスク使用率が`low-space-ratio`未満の場合は、ディスク容量は十分です。次の手順に進みます。

2.  `down peer`があるかどうかを確認します ( `down peer`があるとレプリケーションが停止する可能性があります)。

    `pd-ctl region check-down-peer`コマンドを実行して、 `down peer`があるかどうかを確認します。 3 がある場合は、 `pd-ctl operator add remove-peer <region-id> <tiflash-store-id>`コマンドを実行して削除します。

## データの複製が遅い {#data-replication-is-slow}

原因はさまざまです。次の手順を実行することで問題を解決できます。

1.  レプリケーションを高速化するには[`store limit`](/configure-store-limit.md#usage)増やします。

2.  TiFlashの負荷を調整します。

    TiFlashの負荷が高すぎると、レプリケーションが遅くなることもあります。Grafana の**TiFlash -Summary**パネルでTiFlashインジケーターの負荷を確認できます。

    -   `Applying snapshots Count` : `TiFlash-summary` &gt; `raft` &gt; `Applying snapshots Count`
    -   `Snapshot Predecode Duration` : `TiFlash-summary` &gt; `raft` &gt; `Snapshot Predecode Duration`
    -   `Snapshot Flush Duration` : `TiFlash-summary` &gt; `raft` &gt; `Snapshot Flush Duration`
    -   `Write Stall Duration` : `TiFlash-summary` &gt; `Storage Write Stall` &gt; `Write Stall Duration`
    -   `generate snapshot CPU` : `TiFlash-Proxy-Details` &gt; `Thread CPU` &gt; `Region task worker pre-handle/generate snapshot CPU`

    サービスの優先順位に基づいて負荷を調整し、最適なパフォーマンスを実現します。
