---
title: Troubleshoot a TiFlash Cluster
summary: Learn common operations when you troubleshoot a TiFlash cluster.
---

# TiFlashクラスタのトラブルシューティング {#troubleshoot-a-tiflash-cluster}

このセクションでは、 TiFlash の使用時によく発生する問題、その理由、および解決策について説明します。

## TiFlashが起動しない {#tiflash-fails-to-start}

この問題は、さまざまな理由で発生する可能性があります。以下の手順に従ってトラブルシューティングを行うことをお勧めします。

1.  システムが RedHat Enterprise Linux 8 であるかどうかを確認します。

    RedHat Enterprise Linux 8 には`libnsl.so`システム ライブラリがありません。次のコマンドを使用して手動でインストールできます。

    {{< copyable "" >}}

    ```shell
    dnf install libnsl
    ```

2.  システムの`ulimit`パラメータ設定を確認してください。

    {{< copyable "" >}}

    ```shell
    ulimit -n 1000000
    ```

3.  PD Controlツールを使用して、ノード (同じ IP とポート) でオフラインにできなかったTiFlashインスタンスがあるかどうかを確認し、インスタンスを強制的にオフラインにします。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

上記の方法で問題を解決できない場合は、 TiFlashログ ファイルと[支持を得ます](/support.md) PingCAP またはコミュニティから保存してください。

## TiFlashレプリカは常に利用できません {#tiflash-replica-is-always-unavailable}

これは、設定エラーまたは環境の問題によって、 TiFlashが異常な状態にあるためです。次の手順を実行して、障害のあるコンポーネントを特定します。

1.  PD が`Placement Rules`機能を有効にするかどうかを確認します。

    {{< copyable "" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    -   `true`が返された場合は、次のステップに進みます。
    -   `false`が返された場合は、 [配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)返し、次のステップに進みます。

2.  TiFlash -Summary モニタリング パネルで`UpTime`を表示して、 TiFlashプロセスが正しく機能しているかどうかを確認します。

3.  `pd-ctl`でTiFlashプロキシの状態が正常かどうかを確認します。

    {{< copyable "" >}}

    ```shell
    echo "store" | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    TiFlashプロキシの`store.labels` `{"key": "engine", "value": "tiflash"}`などの情報が含まれます。この情報を確認して、 TiFlashプロキシを確認できます。

4.  `pd buddy`がログを正しく出力できるかどうかを確認します (ログ パスは、[flash.flash_cluster] 構成アイテムの`log`の値です。デフォルトのログ パスは、 TiFlash構成ファイルで構成された`tmp`ディレクトリの下にあります)。

5.  構成されたレプリカの数が、クラスター内の TiKV ノードの数以下であるかどうかを確認します。そうでない場合、PD はデータをTiFlashに複製できません。

    {{< copyable "" >}}

    ```shell
    echo 'config placement-rules show' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    `default: count`の値を再確認します。

    > **ノート：**
    >
    > [配置ルール](/configure-placement-rules.md)機能が有効になると、以前に構成された`max-replicas`と`location-labels`無効になります。レプリカ ポリシーを調整するには、配置ルールに関連するインターフェイスを使用します。

6.  マシンの残りのディスク容量 ( TiFlashノードの`store`ある場所) が十分かどうかを確認します。デフォルトでは、残りのディスク容量が`store`容量の 20% 未満の場合 (これは`low-space-ratio`パラメーターによって制御されます)、PD はこのTiFlashノードにデータをスケジュールできません。

## 一部のクエリが<code>Region Unavailable</code>エラーを返す {#some-queries-return-the-code-region-unavailable-code-error}

TiFlashの負荷が重すぎて、 TiFlashデータのレプリケーションが遅れる原因となる場合、一部のクエリで`Region Unavailable`エラーが返されることがあります。

この場合、 TiFlashノードを追加することで負荷のバランスを取ることができます。

## データファイルの破損 {#data-file-corruption}

データ ファイルの破損を処理するには、次の手順を実行します。

1.  対応するTiFlashノードを停止するには、 [TiFlashノードをダウンさせる](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。
2.  TiFlashノードの関連データを削除します。
3.  クラスターにTiFlashノードを再デプロイします。

## TiFlash解析が遅い {#tiflash-analysis-is-slow}

MPP モードでサポートされていない演算子または関数がステートメントに含まれている場合、TiDB は MPP モードを選択しません。したがって、ステートメントの分析は遅くなります。この場合、 `EXPLAIN`ステートメントを実行して、MPP モードでサポートされていない演算子または関数をチェックできます。

{{< copyable "" >}}

```sql
create table t(a datetime);
alter table t set tiflash replica 1;
insert into t values('2022-01-13');
set @@session.tidb_enforce_mpp=1;
explain select count(*) from t where subtime(a, '12:00:00') > '2022-01-01' group by a;
show warnings;
```

この例では、警告メッセージは、TiDB 5.4 以前のバージョンが`subtime`関数をサポートしていないため、TiDB が MPP モードを選択しないことを示しています。

```
+---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
+---------+------+-----------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
+---------+------+-----------------------------------------------------------------------------+
```

## データはTiFlashに複製されません {#data-is-not-replicated-to-tiflash}

TiFlashノードをデプロイし、(ALTER 操作を実行して) レプリケーションを開始した後、それにデータがレプリケートされません。この場合、次の手順に従って問題を特定し、対処できます。

1.  `ALTER table <tbl_name> set tiflash replica <num>`コマンドを実行してレプリケーションが成功したかどうかを確認し、出力を確認します。

    -   出力がある場合は、次のステップに進みます。
    -   出力がない場合は、 `SELECT * FROM information_schema.tiflash_replica`コマンドを実行して、 TiFlashレプリカが作成されているかどうかを確認します。そうでない場合は、 `ALTER table ${tbl_name} set tiflash replica ${num}`コマンドを再度実行し、他のステートメント ( `add index`など) が実行されたかどうかを確認するか、DDL の実行が成功したかどうかを確認します。

2.  TiFlashリージョンのレプリケーションが正しく実行されるかどうかを確認します。

    `progress`に変更があるかどうかを確認します。

    -   はいの場合、 TiFlashレプリケーションは正しく実行されます。
    -   いいえの場合、 TiFlashレプリケーションは異常です。 `tidb.log`で、 `Tiflash replica is not available`言ってログを検索します。該当テーブルの`progress`更新されているか確認します。そうでない場合は、詳細について`tiflash log`確認してください。たとえば、 `tiflash log`中`lag_region_info`検索して、どのリージョンが遅れているかを調べます。

3.  pd-ctl を使用して、 [配置ルール](/configure-placement-rules.md)機能が有効になっているかどうかを確認します。

    {{< copyable "" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    -   `true`が返された場合は、次のステップに進みます。
    -   `false`が返された場合は、 [配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)返し、次のステップに進みます。

4.  `max-replicas`の構成が正しいかどうかを確認します。

    -   `max-replicas`の値がクラスター内の TiKV ノードの数を超えていない場合は、次の手順に進みます。

    -   値`max-replicas`がクラスター内の TiKV ノードの数より大きい場合、PD はデータをTiFlashノードに複製しません。この問題に対処するには、 `max-replicas`クラスター内の TiKV ノードの数以下の整数に変更します。

    > **ノート：**
    >
    > `max-replicas`はデフォルトで 3 に設定されています。本番環境では、この値は通常、TiKV ノードの数よりも少なくなります。テスト環境では、値は 1 です。

    {{< copyable "" >}}

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

    TiDB DDL Owner のログを検索し、TiDB が配置ルールを追加するように PD に通知したかどうかを確認します。分割されていないテーブルの場合は、 `ConfigureTiFlashPDForTable`を検索します。分割されたテーブルの場合は、 `ConfigureTiFlashPDForPartitions`を検索します。

    -   キーワードが見つかった場合は、次の手順に進みます。
    -   そうでない場合は、トラブルシューティングのために、対応するコンポーネントのログを収集します。

6.  PD がテーブルの配置ルールを構成しているかどうかを確認します。

    `curl http://<pd-ip>:<pd-port>/pd/api/v1/config/rules/group/tiflash`コマンドを実行して、現在の PD のすべてのTiFlash配置ルールを表示します。 ID が`table-<table_id>-r`ルールが見つかった場合、PD は配置ルールを正常に構成しています。

7.  PD が正しくスケジュールされているかどうかを確認します。

    `pd.log`ファイルで`table-<table_id>-r`キーワードとスケジューリング動作 ( `add operator`など) を検索します。

    -   キーワードが見つかった場合、PD は適切にスケジュールします。
    -   そうでない場合、PD は適切にスケジュールされません。

## データの複製が停止する {#data-replication-gets-stuck}

TiFlashでのデータ複製が正常に開始された後、一定時間経過してもすべてまたは一部のデータの複製に失敗する場合は、次の手順を実行して問題を確認または解決できます。

1.  ディスク容量を確認してください。

    ディスク容量の比率が値`low-space-ratio`よりも高いかどうかを確認します (デフォルトは 0.8 です。ノードの容量使用率が 80% を超えると、PD はこのノードへのデータの移行を停止して、ディスク容量の枯渇を回避します)。

    -   ディスク使用率が`low-space-ratio`以上の場合、ディスク容量が不足しています。ディスク容量を解放するには、 `${data}/flash/`フォルダーの下にある`space_placeholder_file` (必要に応じて、ファイルを削除した後に`reserve-space`を 0MB に設定) などの不要なファイルを削除します。
    -   ディスク使用率が値`low-space-ratio`未満の場合、ディスク容量は十分です。次のステップに進みます。

2.  `down peer`があるかどうかを確認します ( `down peer`場合、レプリケーションが停止する可能性があります)。

    `pd-ctl region check-down-peer`コマンドを実行して、 `down peer`があるかどうかを確認します。存在する場合は、 `pd-ctl operator add remove-peer <region-id> <tiflash-store-id>`コマンドを実行して削除します。

## データ複製が遅い {#data-replication-is-slow}

原因はさまざまです。次の手順を実行することで、この問題に対処できます。

1.  レプリケーションを高速化するには、 [`store limit`](/configure-store-limit.md#usage)を増やします。

2.  TiFlashの負荷を調整します。

    TiFlashの負荷が高すぎると、レプリケーションが遅くなる可能性もあります。 Grafana の**TiFlash -Summary**パネルでTiFlashインジケータの負荷を確認できます。

    -   `Applying snapshots Count` : `TiFlash-summary` &gt; `raft` &gt; `Applying snapshots Count`
    -   `Snapshot Predecode Duration` : `TiFlash-summary` &gt; `raft` &gt; `Snapshot Predecode Duration`
    -   `Snapshot Flush Duration` : `TiFlash-summary` &gt; `raft` &gt; `Snapshot Flush Duration`
    -   `Write Stall Duration` : `TiFlash-summary` &gt; `Storage Write Stall` &gt; `Write Stall Duration`
    -   `generate snapshot CPU` : `TiFlash-Proxy-Details` &gt; `Thread CPU` &gt; `Region task worker pre-handle/generate snapshot CPU`

    サービスの優先順位に基づいて、それに応じて負荷を調整し、最適なパフォーマンスを実現します。
