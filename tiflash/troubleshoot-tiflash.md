---
title: Troubleshoot a TiFlash Cluster
summary: Learn common operations when you troubleshoot a TiFlash cluster.
---

# TiFlashクラスターのトラブルシューティング {#troubleshoot-a-tiflash-cluster}

このセクションでは、TiFlashを使用するときによく発生する問題、その理由、および解決策について説明します。

## TiFlashの起動に失敗する {#tiflash-fails-to-start}

この問題は、さまざまな理由で発生する可能性があります。以下の手順に従ってトラブルシューティングを行うことをお勧めします。

1.  システムがCentOS8であるかどうかを確認してください。

    CentOS8には`libnsl.so`のシステムライブラリがありません。次のコマンドを使用して手動でインストールできます。

    {{< copyable "" >}}

    ```shell
    dnf install libnsl
    ```

2.  システムの`ulimit`パラメータ設定を確認してください。

    {{< copyable "" >}}

    ```shell
    ulimit -n 1000000
    ```

3.  PD制御ツールを使用して、ノード（同じIPとポート）でオフラインにできなかったTiFlashインスタンスがあるかどうかを確認し、インスタンスを強制的にオフラインにします。詳細な手順については、 [TiFlashクラスタでのスケーリング](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

上記の方法で問題を解決できない場合は、TiFlashログファイルと電子メールを[info@pingcap.com](mailto:info@pingcap.com)に保存して詳細を確認してください。

## TiFlashレプリカは常に利用できません {#tiflash-replica-is-always-unavailable}

これは、TiFlashが構成エラーまたは環境問題によって異常な状態にあるためです。障害のあるコンポーネントを特定するには、次の手順を実行します。

1.  PDが`Placement Rules`つの機能を有効にしているかどうかを確認します。

    {{< copyable "" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    -   `true`が返された場合は、次の手順に進みます。
    -   `false`が返された場合は、 [配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)を実行して、次の手順に進みます。

2.  TiFlash-Summaryモニタリングパネルで`UpTime`を表示して、TiFlashプロセスが正しく機能しているかどうかを確認します。

3.  TiFlashプロキシのステータスが`pd-ctl`まで正常かどうかを確認します。

    {{< copyable "" >}}

    ```shell
    echo "store" | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    TiFlashプロキシの`store.labels`には、 `{"key": "engine", "value": "tiflash"}`などの情報が含まれています。この情報を確認して、TiFlashプロキシを確認できます。

4.  `pd buddy`がログを正しく印刷できるかどうかを確認します（ログパスは[flash.flash_cluster]構成項目の値`log`です。デフォルトのログパスは、TiFlash構成ファイルで構成された`tmp`ディレクトリの下にあります）。

5.  構成されたレプリカの数がクラスタのTiKVノードの数以下であるかどうかを確認します。そうでない場合、PDはデータをTiFlashに複製できません。

    {{< copyable "" >}}

    ```shell
    echo 'config placement-rules show' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    `default: count`の値を再確認します。

    > **ノート：**
    >
    > [配置ルール](/configure-placement-rules.md)機能を有効にすると、以前に構成した`max-replicas`と`location-labels`は無効になります。レプリカポリシーを調整するには、配置ルールに関連するインターフェイスを使用します。

6.  マシンの残りのディスク容量（TiFlashノードの`store` ）が十分かどうかを確認します。デフォルトでは、残りのディスク容量が`store`の容量（ `low-space-ratio`のパラメーターによって制御される）の20％未満の場合、PDはこのTiFlashノードにデータをスケジュールできません。

## TiFlashのクエリ時間は不安定であり、エラーログには多くの<code>Lock Exception</code>メッセージが出力されます {#tiflash-query-time-is-unstable-and-the-error-log-prints-many-code-lock-exception-code-messages}

これは、大量のデータがクラスタに書き込まれるため、TiFlashクエリでロックが発生し、クエリの再試行が必要になるためです。

TiDBでは、クエリのタイムスタンプを1秒前に設定できます。たとえば、現在の時刻が「2020-04-08 20:15:01」の場合、クエリを実行する前に`set @@tidb_snapshot='2020-04-08 20:15:00';`を実行できます。これにより、TiFlashクエリでロックが発生することが少なくなり、クエリ時間が不安定になるリスクが軽減されます。

## 一部のクエリは、 <code>Region Unavailable</code>エラーを返します {#some-queries-return-the-code-region-unavailable-code-error}

TiFlashの負荷圧力が大きすぎて、TiFlashデータレプリケーションが遅れる場合、一部のクエリは`Region Unavailable`エラーを返す可能性があります。

この場合、TiFlashノードを追加することで負荷圧力のバランスをとることができます。

## データファイルの破損 {#data-file-corruption}

データファイルの破損を処理するには、次の手順を実行します。

1.  対応するTiFlashノードを停止するには、 [TiFlashノードを停止します](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。
2.  TiFlashノードの関連データを削除します。
3.  クラスタにTiFlashノードを再デプロイします。

## TiFlash分析は遅い {#tiflash-analysis-is-slow}

ステートメントにMPPモードでサポートされていない演算子または関数が含まれている場合、TiDBはMPPモードを選択しません。したがって、ステートメントの分析は遅くなります。この場合、 `EXPLAIN`ステートメントを実行して、MPPモードでサポートされていない演算子または関数をチェックできます。

{{< copyable "" >}}

```sql
create table t(a datetime);
alter table t set tiflash replica 1;
insert into t values('2022-01-13');
set @@session.tidb_enforce_mpp=1;
explain select count(*) from t where subtime(a, '12:00:00') > '2022-01-01' group by a;
show warnings;
```

この例では、警告メッセージは、TiDB 5.4以前のバージョンが`subtime`機能をサポートしていないため、TiDBがMPPモードを選択しないことを示しています。

```
+---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
+---------+------+-----------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
+---------+------+-----------------------------------------------------------------------------+
```

## データはTiFlashに複製されません {#data-is-not-replicated-to-tiflash}

TiFlashノードをデプロイしてレプリケーションを開始した後（ALTER操作を実行することにより）、データはそのノードにレプリケートされません。この場合、以下の手順に従って問題を特定して対処できます。

1.  `ALTER table <tbl_name> set tiflash replica <num>`コマンドを実行してレプリケーションが成功したかどうかを確認し、出力を確認します。

    -   出力がある場合は、次の手順に進みます。
    -   出力がない場合は、 `SELECT * FROM information_schema.tiflash_replica`コマンドを実行して、TiFlashレプリカが作成されているかどうかを確認します。そうでない場合は、 `ALTER table ${tbl_name} set tiflash replica ${num}`コマンドを再度実行するか、他のステートメント（たとえば、 `add index` ）が実行されたかどうかを確認するか、DDLの実行が成功したかどうかを確認します。

2.  TiFlashプロセスが正しく実行されているかどうかを確認します。

    `progress`ファイルの`flash_region_count`パラメータ、および`tiflash_cluster_manager.log`監視項目`Uptime`に変更があるかどうかを確認します。

    -   はいの場合、TiFlashプロセスは正しく実行されます。
    -   いいえの場合、TiFlashプロセスは異常です。詳細については、 `tiflash`ログを確認してください。

3.  pd-ctlを使用して、 [配置ルール](/configure-placement-rules.md)の機能が有効になっているかどうかを確認します。

    {{< copyable "" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    -   `true`が返された場合は、次の手順に進みます。
    -   `false`が返された場合は、 [配置ルール機能を有効にする](/configure-placement-rules.md#enable-placement-rules)を実行して、次の手順に進みます。

4.  `max-replicas`の構成が正しいかどうかを確認します。

    -   `max-replicas`の値がクラスタのTiKVノードの数を超えない場合は、次の手順に進みます。

    -   `max-replicas`の値がクラスタのTiKVノードの数よりも大きい場合、PDはデータをTiFlashノードに複製しません。この問題に対処するには、 `max-replicas`をクラスタのTiKVノードの数以下の整数に変更します。

    > **ノート：**
    >
    > `max-replicas`はデフォルトで3に設定されます。実稼働環境では、値は通常、TiKVノードの数よりも少なくなります。テスト環境では、値は1にすることができます。

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

5.  TiDBまたはPDとTiFlash間の接続が正常かどうかを確認します。

    `flash_cluster_manager.log`ファイルで`ERROR`キーワードを検索します。

    -   `ERROR`が見つからない場合、接続は正常です。次のステップに進みます。
    -   `ERROR`が見つかった場合、接続は異常です。以下の確認を行ってください。

        -   ログにPDキーワードが記録されているかどうかを確認します。

            PDキーワードが見つかった場合は、TiFlash構成ファイルの`raft.pd_addr`が有効かどうかを確認してください。具体的には、 `curl '{pd-addr}/pd/api/v1/config/rules'`コマンドを実行し、5秒以内に出力があるかどうかを確認します。

        -   ログにTiDB関連のキーワードが記録されているかどうかを確認します。

            TiDBキーワードが見つかった場合は、TiFlash構成ファイルの`flash.tidb_status_addr`が有効かどうかを確認してください。具体的には、 `curl '{tidb-status-addr}/tiflash/replica'`コマンドを実行し、5秒以内に出力があるかどうかを確認します。

        -   ノードが相互にpingできるかどうかを確認します。

    > **ノート：**
    >
    > 問題が解決しない場合は、トラブルシューティングのために対応するコンポーネントのログを収集します。

6.  テーブルに`placement-rule`が作成されているかどうかを確認します。

    `flash_cluster_manager.log`ファイルで`Set placement rule … table-<table_id>-r`キーワードを検索します。

    -   キーワードが見つかった場合は、次の手順に進みます。
    -   そうでない場合は、トラブルシューティングのために対応するコンポーネントのログを収集します。

7.  PDが適切にスケジュールされているかどうかを確認します。

    `pd.log`のファイルで`table-<table_id>-r`のキーワードと`add operator`のようなスケジューリング動作を検索します。

    -   キーワードが見つかった場合、PDは適切にスケジュールします。
    -   そうでない場合、PDは適切にスケジュールされません。ヘルプが必要な場合は、PingCAPテクニカルサポートにお問い合わせください。

> **ノート：**
>
> 複製するテーブルに多数の小さなリージョンがあり、 `region merge`パラメーターが有効になっているか、大きな値に設定されている場合、複製の進行状況は変わらないか、一定期間減少する可能性があります。

## データレプリケーションがスタックする {#data-replication-gets-stuck}

TiFlashでのデータ複製は正常に開始されますが、一定期間後にすべてまたは一部のデータが複製されない場合は、次の手順を実行して問題を確認または解決できます。

1.  ディスク容量を確認してください。

    ディスクスペース率が値`low-space-ratio` （デフォルトは0.8）より大きいかどうかを確認します。ノードのスペース使用量が80％を超えると、PDはディスクスペースの枯渇を防ぐためにこのノードへのデータの移行を停止します。

    -   ディスク使用率が`low-space-ratio`以上の場合、ディスク容量が不足しています。ディスク容量を減らすには、 `${data}/flash/`フォルダの下にある`space_placeholder_file`などの不要なファイルを削除します（必要に応じて、ファイルを削除した後、 `reserve-space`を0MBに設定します）。
    -   ディスク使用率が`low-space-ratio`未満の場合は、ディスク容量で十分です。次のステップに進みます。

2.  TiKV、TiFlash、PD間のネットワーク接続を確認してください。

    `flash_cluster_manager.log`で、スタックしたテーブルに対応する`flash_region_count`への新しい更新があるかどうかを確認します。

    -   いいえの場合は、次の手順に進みます。
    -   はいの場合、 `down peer`を検索します（ダウンしているピアがある場合、レプリケーションがスタックします）。

        -   `pd-ctl region check-down-peer`を実行して`down peer`を検索します。
        -   `down peer`が見つかった場合は、 `pd-ctl operator add remove-peer\<region-id> \<tiflash-store-id>`を実行して削除します。

3.  CPU使用率を確認してください。

    Grafanaで、 **TiFlash-Proxy-Details** &gt; <strong>Thread CPU</strong> &gt; Regiontaskworkerの<strong>事前処理/スナップショットCPUの生成を</strong>選択します。 `<instance-ip>:<instance-port>-region-worker`のCPU使用率を確認します。

    曲線が直線の場合、TiFlashノードはスタックしています。 TiFlashプロセスを終了して再起動するか、PingCAPテクニカルサポートに問い合わせてください。

## データ複製が遅い {#data-replication-is-slow}

原因はさまざまです。次の手順を実行することで、問題に対処できます。

1.  スケジューリングパラメータの値を調整します。

    -   [`store limit`](/configure-store-limit.md#usage)を増やすと、複製が高速化されます。
    -   [`config set patrol-region-interval 10ms`](/pd-control.md#command)を減らすと、TiKVでリージョンのチェッカースキャンがより頻繁になります。
    -   [`region merge`](/pd-control.md#command)を増やすと、リージョンの数が減ります。つまり、スキャンが少なくなり、チェック頻度が高くなります。

2.  TiFlshの負荷を調整します。

    TiFlashの負荷が高すぎると、レプリケーションが遅くなる可能性もあります。 TiFlashインジケーターの負荷は、Grafanaの**TiFlash-Summary**パネルで確認できます。

    -   `Applying snapshots Count` ： `TiFlash-summary` &gt; `raft` &gt; `Applying snapshots Count`
    -   `Snapshot Predecode Duration` ： `TiFlash-summary` &gt; `raft` &gt; `Snapshot Predecode Duration`
    -   `Snapshot Flush Duration` ： `TiFlash-summary` &gt; `raft` &gt; `Snapshot Flush Duration`
    -   `Write Stall Duration` ： `TiFlash-summary` &gt; `Storage Write Stall` &gt; `Write Stall Duration`
    -   `generate snapshot CPU` ： `TiFlash-Proxy-Details` &gt; `Thread CPU` &gt; `Region task worker pre-handle/generate snapshot CPU`

    サービスの優先順位に基づいて、それに応じて負荷を調整し、最適なパフォーマンスを実現します。
