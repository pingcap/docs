---
title: Troubleshoot a TiFlash Cluster
summary: Learn common operations when you troubleshoot a TiFlash cluster.
---

# TiFlashクラスタのトラブルシューティング {#troubleshoot-a-tiflash-cluster}

このセクションでは、 TiFlash の使用時によく発生する問題、その理由、および解決策について説明します。

## TiFlash が起動できない {#tiflash-fails-to-start}

この問題はさまざまな理由で発生する可能性があります。以下の手順に従ってトラブルシューティングを行うことをお勧めします。

1.  システムが RedHat Enterprise Linux 8 であるかどうかを確認します。

    RedHat Enterprise Linux 8 には`libnsl.so`システム ライブラリがありません。次のコマンドを使用して手動でインストールできます。

    ```shell
    dnf install libnsl
    ```

2.  システムの`ulimit`パラメータ設定を確認してください。

    ```shell
    ulimit -n 1000000
    ```

3.  PD Controlツールを使用して、ノード (同じ IP およびポート) 上でオフラインにできなかったTiFlashインスタンスがあるかどうかを確認し、インスタンスを強制的にオフラインにします。詳細な手順については、 [TiFlashクラスターでのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

上記の方法で問題を解決できない場合は、PingCAP またはコミュニティからTiFlashログ ファイルと[支持を得ます](/support.md)を保存してください。

## TiFlashレプリカは常に利用できない {#tiflash-replica-is-always-unavailable}

これは、設定エラーや環境の問題によりTiFlashが異常な状態にあるためです。障害のあるコンポーネントを特定するには、次の手順を実行します。

1.  PD が`Placement Rules`機能を有効にしているかどうかを確認します。

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    -   `true`が返された場合は、次のステップに進みます。
    -   `false`が返された場合は[配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)返し、次のステップに進みます。

2.  TiFlash - Summary モニタリング パネルの`UpTime`を表示して、 TiFlashプロセスが正しく動作しているかどうかを確認します。

3.  TiFlashプロキシのステータスが正常であるかどうかを`pd-ctl`まで確認します。

    ```shell
    echo "store" | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    TiFlashプロキシの`store.labels` `{"key": "engine", "value": "tiflash"}`などの情報が含まれます。この情報をチェックして、 TiFlashプロキシを確認できます。

4.  `pd buddy`がログを正しく出力できるかどうかを確認します (ログ パスは、[flash.flash_cluster] 構成項目の値`log`です。デフォルトのログ パスは、 TiFlash構成ファイルで構成されている`tmp`ディレクトリの下にあります)。

5.  構成されたレプリカの数がクラスター内の TiKV ノードの数以下であるかどうかを確認します。そうでない場合、PD はデータをTiFlashに複製できません。

    ```shell
    echo 'config placement-rules show' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    `default: count`の値を再確認します。

    > **注記：**
    >
    > [配置ルール](/configure-placement-rules.md)機能を有効にすると、以前に設定した`max-replicas`と`location-labels`は無効になります。レプリカ ポリシーを調整するには、配置ルールに関連するインターフェイスを使用します。

6.  マシン ( TiFlashノードの`store`存在する) の残りのディスク容量が十分であるかどうかを確認します。デフォルトでは、残りのディスク容量が`store`容量 ( `low-space-ratio`パラメータで制御される) の 20% 未満の場合、PD はこのTiFlashノードにデータをスケジュールできません。

## 一部のクエリは<code>Region Unavailable</code>エラーを返します {#some-queries-return-the-code-region-unavailable-code-error}

TiFlashの負荷が重すぎて、 TiFlashデータ レプリケーションが遅れる場合、一部のクエリで`Region Unavailable`エラーが返されることがあります。

この場合、 TiFlashノードをさらに追加することで負荷圧力のバランスをとることができます。

## データファイルの破損 {#data-file-corruption}

データ ファイルの破損に対処するには、次の手順を実行します。

1.  対応するTiFlashノードを停止するには、 [TiFlashノードを停止します](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。
2.  TiFlashノードの関連データを削除します。
3.  クラスターにTiFlashノードを再デプロイします。

## TiFlash解析が遅い {#tiflash-analysis-is-slow}

MPP モードでサポートされていない演算子または関数がステートメントに含まれている場合、TiDB は MPP モードを選択しません。したがって、声明の分析は遅くなります。この場合、 `EXPLAIN`ステートメントを実行して、MPP モードでサポートされていない演算子または関数を確認できます。

```sql
create table t(a datetime);
alter table t set tiflash replica 1;
insert into t values('2022-01-13');
set @@session.tidb_enforce_mpp=1;
explain select count(*) from t where subtime(a, '12:00:00') > '2022-01-01' group by a;
show warnings;
```

この例では、TiDB 5.4 以前のバージョンでは`subtime`機能がサポートされていないため、TiDB が MPP モードを選択しないことを警告メッセージが示しています。

    +---------+------+-----------------------------------------------------------------------------+
    > | Level   | Code | Message                                                                     |
    +---------+------+-----------------------------------------------------------------------------+
    | Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
    +---------+------+-----------------------------------------------------------------------------+

## データはTiFlashにレプリケートされません {#data-is-not-replicated-to-tiflash}

TiFlashノードをデプロイし、(ALTER 操作を実行して) レプリケーションを開始した後、データはそこにレプリケートされません。この場合、次の手順に従って問題を特定して対処できます。

1.  `ALTER table <tbl_name> set tiflash replica <num>`コマンドを実行してレプリケーションが成功したかどうかを確認し、出力を確認します。

    -   出力がある場合は、次のステップに進みます。
    -   出力がない場合は、 `SELECT * FROM information_schema.tiflash_replica`コマンドを実行して、 TiFlashレプリカが作成されたかどうかを確認します。そうでない場合は、 `ALTER table ${tbl_name} set tiflash replica ${num}`コマンドを再度実行し、他のステートメント ( `add index`など) が実行されたかどうかを確認するか、DDL の実行が成功したかどうかを確認します。

2.  TiFlashリージョンのレプリケーションが正しく実行されているかどうかを確認します。

    `progress`に変更があるかどうかを確認します。

    -   「はい」の場合、 TiFlashレプリケーションは正しく実行されます。
    -   「いいえ」の場合、 TiFlashレプリケーションは異常です。 `tidb.log`で、 `Tiflash replica is not available`というログを検索します。該当テーブルの`progress`更新されているか確認してください。そうでない場合は、 `tiflash log`で詳細を確認してください。たとえば、 `tiflash log`のうち`lag_region_info`検索して、どのリージョンが遅れているかを確認します。

3.  pd-ctlを使用して[配置ルール](/configure-placement-rules.md)機能が有効になっているかどうかを確認します。

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    -   `true`が返された場合は、次のステップに進みます。
    -   `false`が返された場合は[配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)返し、次のステップに進みます。

4.  `max-replicas`構成が正しいかどうかを確認します。

    -   値`max-replicas`がクラスター内の TiKV ノードの数を超えない場合は、次のステップに進みます。

    -   値`max-replicas`がクラスター内の TiKV ノードの数より大きい場合、PD はデータをTiFlashノードに複製しません。この問題に対処するには、 `max-replicas`クラスター内の TiKV ノードの数以下の整数に変更します。

    > **注記：**
    >
    > `max-replicas`のデフォルトは 3 です。本番環境では、この値は通常、TiKV ノードの数よりも少なくなります。テスト環境では、値を 1 にすることができます。

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

    TiDB DDL Owner のログを検索し、TiDB が PD に配置ルールを追加するように通知したかどうかを確認します。パーティション化されていないテーブルの場合は、 `ConfigureTiFlashPDForTable`を検索します。パーティション化されたテーブルの場合は、 `ConfigureTiFlashPDForPartitions`検索します。

    -   キーワードが見つかった場合は、次のステップに進みます。
    -   そうでない場合は、トラブルシューティングのために対応するコンポーネントのログを収集します。

6.  PD がテーブルの配置ルールを設定しているかどうかを確認します。

    `curl http://<pd-ip>:<pd-port>/pd/api/v1/config/rules/group/tiflash`コマンドを実行して、現在の PD 上のすべてのTiFlash配置ルールを表示します。 ID が`table-<table_id>-r`ルールが見つかった場合、PD は配置ルールを正常に構成しました。

7.  PD が適切にスケジュールを設定しているかどうかを確認します。

    `pd.log`ファイルで`table-<table_id>-r`キーワードを検索し、 `add operator`のような動作をスケジュールします。

    -   キーワードが見つかった場合、PD は適切にスケジュールを設定します。
    -   そうでない場合、PD は適切にスケジュールを設定しません。

## データレプリケーションが停止する {#data-replication-gets-stuck}

TiFlashでのデータ レプリケーションが正常に開始された後、一定期間経過してもすべてまたは一部のデータのレプリケーションが失敗する場合は、次の手順を実行して問題を確認または解決できます。

1.  ディスク容量を確認してください。

    ディスク容量比率が`low-space-ratio`の値より大きいかどうかを確認します (デフォルトは 0.8。ノードの容量使用率が 80% を超えると、ディスク容量の枯渇を避けるために、PD はこのノードへのデータの移行を停止します)。

    -   ディスク使用率が値`low-space-ratio`以上の場合、ディスク容量が不足しています。ディスク容量を確保するには、 `${data}/flash/`フォルダ配下の不要なファイル`space_placeholder_file`などを削除します (必要に応じて、ファイルを削除した後、 `reserve-space`を 0MB に設定します)。
    -   ディスク使用率が値`low-space-ratio`未満の場合、ディスク容量は十分です。次のステップに進みます。

2.  `down peer`があるかどうかを確認します ( `down peer`あるとレプリケーションが停止する可能性があります)。

    `pd-ctl region check-down-peer`コマンドを実行して、 `down peer`があるかどうかを確認します。存在する場合は、 `pd-ctl operator add remove-peer <region-id> <tiflash-store-id>`コマンドを実行して削除します。

## データのレプリケーションが遅い {#data-replication-is-slow}

原因はさまざまです。次の手順を実行することで問題に対処できます。

1.  レプリケーションを高速化するには、 [`store limit`](/configure-store-limit.md#usage)を増やします。

2.  TiFlashの負荷を調整します。

    TiFlashの負荷が高すぎると、レプリケーションが遅くなる可能性があります。 TiFlashインジケーターの負荷は、Grafana の**TiFlash- Summary**パネルで確認できます。

    -   `Applying snapshots Count` ： `TiFlash-summary` ＞ `raft` ＞ `Applying snapshots Count`
    -   `Snapshot Predecode Duration` ： `TiFlash-summary` ＞ `raft` ＞ `Snapshot Predecode Duration`
    -   `Snapshot Flush Duration` ： `TiFlash-summary` ＞ `raft` ＞ `Snapshot Flush Duration`
    -   `Write Stall Duration` ： `TiFlash-summary` ＞ `Storage Write Stall` ＞ `Write Stall Duration`
    -   `generate snapshot CPU` ： `TiFlash-Proxy-Details` ＞ `Thread CPU` ＞ `Region task worker pre-handle/generate snapshot CPU`

    サービスの優先順位に基づいて負荷を調整し、最適なパフォーマンスを実現します。
