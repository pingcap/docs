---
title: PD Control User Guide
summary: Use PD Control to obtain the state information of a cluster and tune a cluster.
---

# PD Controlユーザー ガイド {#pd-control-user-guide}

PD Control は、PD のコマンド ライン ツールとして、クラスターの状態情報を取得し、クラスターをチューニングします。

## PD Controlをインストールする {#install-pd-control}

> **ノート：**
>
> 使用するコントロール ツールのバージョンは、クラスターのバージョンと一致していることが推奨されます。

### TiUPコマンドを使用する {#use-tiup-command}

PD Controlを使用するには、 `tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> [-i]`コマンドを実行します。

### TiDB インストール パッケージのダウンロード {#download-tidb-installation-package}

`pd-ctl`の最新バージョンをダウンロードする場合は、TiDB パッケージに`pd-ctl`含まれているため、TiDB パッケージを直接ダウンロードします。

| パッケージのダウンロード リンク                                                          | OS    | アーキテクチャ | SHA256 チェックサム                                                    |
| :------------------------------------------------------------------------ | :---- | :------ | :--------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (pd-ctl) | Linux | amd64   | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |

> **ノート：**
>
> `{version}` TiDB のバージョン番号を示します。たとえば、 `{version}`が`v5.4.3`の場合、パッケージのダウンロード リンクは`https://download.pingcap.org/tidb-v5.4.3-linux-amd64.tar.gz`です。

### ソースコードからコンパイル {#compile-from-source-code}

1.  [行く](https://golang.org/) Go モジュールを使用するため、バージョン 1.13 以降。
2.  [PDプロジェクト](https://github.com/pingcap/pd)のルート ディレクトリで、 `make`または`make pd-ctl`コマンドを使用して`bin/pd-ctl`をコンパイルおよび生成します。

## 使用法 {#usage}

シングルコマンドモード:

```bash
tiup ctl:<cluster-version> pd store -u http://127.0.0.1:2379
```

対話モード:

```bash
tiup ctl:<cluster-version> pd -i -u http://127.0.0.1:2379
```

環境変数を使用します。

```bash
export PD_ADDR=http://127.0.0.1:2379
tiup ctl:<cluster-version> pd
```

TLS を使用して暗号化します。

```bash
tiup ctl:<cluster-version> pd -u https://127.0.0.1:2379 --cacert="path/to/ca" --cert="path/to/cert" --key="path/to/key"
```

## コマンド ライン フラグ {#command-line-flags}

### <code>--cacert</code> {#code-cacert-code}

-   信頼できる CA の証明書ファイルへのパスを PEM 形式で指定します
-   デフォルト： &quot;&quot;

### <code>--cert</code> {#code-cert-code}

-   SSLの証明書へのパスをPEM形式で指定します
-   デフォルト： &quot;&quot;

### <code>--detach</code> / <code>-d</code> {#code-detach-code-code-d-code}

-   単一コマンド ライン モードを使用する (readline に入らない)
-   デフォルト: 真

### <code>--help</code> / <code>-h</code> {#code-help-code-code-h-code}

-   ヘルプ情報を出力します
-   デフォルト: false

### <code>--interact</code> / <code>-i</code> {#code-interact-code-code-i-code}

-   対話モードを使用します (readline に入ります)
-   デフォルト: false

### <code>--key</code> {#code-key-code}

-   `--cert`で指定した証明書の秘密鍵であるSSLの証明書鍵ファイルへのパスをPEM形式で指定する
-   デフォルト： &quot;&quot;

### <code>--pd</code> / <code>-u</code> {#code-pd-code-code-u-code}

-   PDアドレスを指定
-   デフォルトのアドレス: `http://127.0.0.1:2379`
-   環境変数: `PD_ADDR`

### <code>--version</code> / <code>-V</code> {#code-version-code-code-v-code}

-   バージョン情報を出力して終了します
-   デフォルト: false

## 指図 {#command}

### <code>cluster</code> {#code-cluster-code}

このコマンドを使用して、クラスターの基本情報を表示します。

使用法：

```bash
>> cluster                                     // To show the cluster information
{
  "id": 6493707687106161130,
  "max_peer_count": 3
}
```

### <code>config [show | set &#x3C;option> &#x3C;value> | placement-rules]</code> {#code-config-show-set-x3c-option-x3c-value-placement-rules-code}

このコマンドを使用して、構成情報を表示または変更します。

使用法：

```bash
>> config show                                // Display the config information of the scheduling
{
  "replication": {
    "enable-placement-rules": "true",
    "isolation-level": "",
    "location-labels": "",
    "max-replicas": 3,
    "strictly-match-label": "false"
  },
  "schedule": {
    "enable-cross-table-merge": "true",
    "high-space-ratio": 0.7,
    "hot-region-cache-hits-threshold": 3,
    "hot-region-schedule-limit": 4,
    "leader-schedule-limit": 4,
    "leader-schedule-policy": "count",
    "low-space-ratio": 0.8,
    "max-merge-region-keys": 200000,
    "max-merge-region-size": 20,
    "max-pending-peer-count": 64,
    "max-snapshot-count": 64,
    "max-store-down-time": "30m0s",
    "merge-schedule-limit": 8,
    "patrol-region-interval": "10ms",
    "region-schedule-limit": 2048,
    "region-score-formula-version": "v2",
    "replica-schedule-limit": 64,
    "scheduler-max-waiting-operator": 5,
    "split-merge-interval": "1h0m0s",
    "tolerant-size-ratio": 0
  }
}
>> config show all                            // Display all config information
>> config show replication                    // Display the config information of replication
{
  "max-replicas": 3,
  "location-labels": "",
  "isolation-level": "",
  "strictly-match-label": "false",
  "enable-placement-rules": "true"
}

>> config show cluster-version                // Display the current version of the cluster, which is the current minimum version of TiKV nodes in the cluster and does not correspond to the binary version.
"5.2.2"
```

-   `max-snapshot-count` 、1 つのストアが同時に受信または送信するスナップショットの最大数を制御します。スケジューラは、通常のアプリケーション リソースを占有しないように、この構成によって制限されます。レプリカの追加またはバランシングの速度を向上させる必要がある場合は、この値を増やしてください。

    ```bash
    config set max-snapshot-count 64  // Set the maximum number of snapshots to 64
    ```

-   `max-pending-peer-count` 1 つのストア内の保留中のピアの最大数を制御します。スケジューラーは、一部のノードで最新のログなしで多数のリージョンが生成されるのを避けるために、この構成によって制限されます。レプリカの追加またはバランシングの速度を向上させる必要がある場合は、この値を増やしてください。 0 に設定すると、制限がないことを示します。

    ```bash
    config set max-pending-peer-count 64  // Set the maximum number of pending peers to 64
    ```

-   `max-merge-region-size`リージョンマージのサイズの上限を制御します (単位は MiB)。 `regionSize`が指定値を超えると、PD は隣接するリージョンとマージしません。 0 に設定すると、リージョンマージが無効になります。

    ```bash
    config set max-merge-region-size 16 // Set the upper limit on the size of Region Merge to 16 MiB
    ```

-   `max-merge-region-keys`リージョンマージのキー カウントの上限を制御します。 `regionKeyCount`が指定値を超えると、PD は隣接するリージョンとマージしません。

    ```bash
    config set max-merge-region-keys 50000 // Set the the upper limit on keyCount to 50000
    ```

-   `split-merge-interval`同じリージョンでの`split`と`merge`の操作の間隔を制御します。これは、新しく分割されたリージョンが一定期間内にマージされないことを意味します。

    ```bash
    config set split-merge-interval 24h  // Set the interval between `split` and `merge` to one day
    ```

-   `enable-one-way-merge`は、PD がリージョン を次のリージョンとマージすることのみを許可するかどうかを制御します。 `false`に設定すると、PD はリージョンが隣接する 2 つのリージョンとマージできるようにします。

    ```bash
    config set enable-one-way-merge true  // Enables one-way merging.
    ```

-   `enable-cross-table-merge`はクロステーブルのリージョンのマージを有効にするために使用されます。 `false`に設定すると、PD は異なるテーブルのリージョンをマージしません。このオプションは、キー タイプが「テーブル」の場合にのみ機能します。

    ```bash
    config set enable-cross-table-merge true  // Enable cross table merge.
    ```

-   `key-type`クラスターに使用されるキーのエンコード タイプを指定します。サポートされているオプションは [&quot;table&quot;, &quot;raw&quot;, &quot;txn&quot;] で、デフォルト値は &quot;table&quot; です。

    -   クラスターに TiDB インスタンスが存在しない場合、 `key-type` 「raw」または「txn」になり、PD は`enable-cross-table-merge`設定に関係なく、テーブル全体でリージョンをマージできます。
    -   クラスターに TiDB インスタンスが存在する場合、 `key-type` 「テーブル」である必要があります。 PD がテーブル間でリージョンをマージできるかどうかは、 `enable-cross-table-merge`によって決定されます。 `key-type`が「raw」の場合、配置ルールは機能しません。

    ```bash
    config set key-type raw  // Enable cross table merge.
    ```

-   `region-score-formula-version`リージョンスコア式のバージョンを制御します。値のオプションは`v1`と`v2`です。式のバージョン 2 は、TiKV ノードをオンラインまたはオフラインにするなど、一部のシナリオで冗長なバランスリージョンスケジューリングを減らすのに役立ちます。

    {{< copyable "" >}}

    ```bash
    config set region-score-formula-version v2
    ```

-   `patrol-region-interval` `replicaChecker`リージョンのヘルス ステータスをチェックする実行頻度を制御します。間隔が短いほど、実行頻度が高くなります。通常、調整する必要はありません。

    ```bash
    config set patrol-region-interval 10ms // Set the execution frequency of replicaChecker to 10ms
    ```

-   `max-store-down-time`超えると、PD が切断されたストアを復元できないと判断する時間を制御します。 PD が指定された期間内にストアからハートビートを受信しない場合、PD は他のノードにレプリカを追加します。

    ```bash
    config set max-store-down-time 30m  // Set the time within which PD receives no heartbeats and after which PD starts to add replicas to 30 minutes
    ```

-   `leader-schedule-limit`リーダーを同時にスケジュールするタスクの数を制御します。この値は、リーダー バランスの速度に影響します。値が大きいほど高速であることを意味し、値を 0 に設定するとスケジューリングが終了します。通常、リーダー スケジューリングの負荷は小さいため、必要に応じて値を増やすことができます。

    ```bash
    config set leader-schedule-limit 4         // 4 tasks of leader scheduling at the same time at most
    ```

-   `region-schedule-limit`リージョンを同時にスケジューリングするタスクの数を制御します。この値により、作成されるリージョンバランス オペレータが多すぎるのを回避できます。デフォルト値は`2048`で、すべてのサイズのクラスターで十分です。値を`0`に設定すると、スケジューリングが終了します。通常、リージョンのスケジューリング速度は`store-limit`に制限されていますが、何を行っているかを正確に把握していない限り、この値をカスタマイズしないことをお勧めします。

    ```bash
    config set region-schedule-limit 2         // 2 tasks of Region scheduling at the same time at most
    ```

-   `replica-schedule-limit`レプリカを同時にスケジュールするタスクの数を制御します。この値は、ノードがダウンまたは削除されたときのスケジューリング速度に影響します。値が大きいほど高速であることを意味し、値を 0 に設定するとスケジューリングが終了します。通常、レプリカのスケジューリングは負荷が大きいため、あまり大きな値を設定しないでください。通常、この構成項目はデフォルト値のままであることに注意してください。値を変更する場合は、いくつかの値を試して、実際の状況に応じてどれが最適かを確認する必要があります。

    ```bash
    config set replica-schedule-limit 4        // 4 tasks of replica scheduling at the same time at most
    ```

-   `merge-schedule-limit` リージョン Merge スケジューリング タスクの数を制御します。値を 0 に設定すると、リージョンマージが閉じます。通常、Merge スケジューリングは負荷が大きいため、あまり大きな値を設定しないでください。通常、この構成項目はデフォルト値のままであることに注意してください。値を変更する場合は、いくつかの値を試して、実際の状況に応じてどれが最適かを確認する必要があります。

    ```bash
    config set merge-schedule-limit 16       // 16 tasks of Merge scheduling at the same time at most
    ```

-   `hot-region-schedule-limit`同時に実行されているホットリージョンスケジューリング タスクを制御します。値を`0`に設定すると、スケジューリングが無効になります。大きすぎる値を設定することはお勧めしません。そうしないと、システムのパフォーマンスに影響を与える可能性があります。通常、この構成項目はデフォルト値のままであることに注意してください。値を変更する場合は、いくつかの値を試して、実際の状況に応じてどれが最適かを確認する必要があります。

    ```bash
    config set hot-region-schedule-limit 4       // 4 tasks of hot Region scheduling at the same time at most
    ```

-   `hot-region-cache-hits-threshold`は、ホットリージョンを識別するのに必要な分数を設定するために使用されます。 PD は、リージョンがこの分数を超えてホットスポット状態になった後にのみ、ホットスポット スケジューリングに参加できます。

-   `tolerant-size-ratio`バランス バッファ領域のサイズを制御します。 2 店舗のリーダーまたはリージョンのスコア差が、指定されたリージョンサイズの倍数未満の場合、PD によってバランスが取れていると見なされます。

    ```bash
    config set tolerant-size-ratio 20        // Set the size of the buffer area to about 20 times of the average Region Size
    ```

-   `low-space-ratio`ストア スペースが不十分であると見なされるしきい値を制御します。ノードが占有するスペースの割合が指定された値を超えると、PD は該当するノードへのデータの移行を可能な限り回避しようとします。同時に、PD は主に残りの領域をスケジュールして、対応するノードのディスク領域を使い果たすことを回避します。

    ```bash
    config set low-space-ratio 0.9              // Set the threshold value of insufficient space to 0.9
    ```

-   `high-space-ratio`十分なストア スペースと見なされるしきい値を制御します。この構成は、 `region-score-formula-version`が`v1`に設定されている場合にのみ有効です。ノードが占有する容量の比率が指定された値よりも小さい場合、PD は残りの容量を無視し、主に実際のデータ ボリュームをスケジュールします。

    ```bash
    config set high-space-ratio 0.5             // Set the threshold value of sufficient space to 0.5
    ```

-   `cluster-version`はクラスターのバージョンで、一部の機能を有効または無効にしたり、互換性の問題に対処したりするために使用されます。デフォルトでは、これはクラスター内で正常に実行されているすべての TiKV ノードの最小バージョンです。以前のバージョンにロールバックする必要がある場合にのみ、手動で設定できます。

    ```bash
    config set cluster-version 1.0.8              // Set the version of the cluster to 1.0.8
    ```

-   `replication-mode`デュアル データ センター シナリオでのリージョンのレプリケーション モードを制御します。詳細は[DR 自動同期モードを有効にする](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)を参照してください。

-   `leader-schedule-policy`は、リーダーのスケジューリング戦略を選択するために使用されます。 `size`または`count`に従ってリーダーをスケジュールできます。

-   `scheduler-max-waiting-operator`は、各スケジューラーで待機中のオペレーターの数を制御するために使用されます。

-   `enable-remove-down-replica`は、DownReplica を自動的に削除する機能を有効にするために使用されます。 `false`に設定すると、PD はダウンタイム レプリカを自動的にクリーンアップしません。

-   `enable-replace-offline-replica`は、OfflineReplica の移行機能を有効にするために使用されます。 `false`に設定すると、PD はオフライン レプリカを移行しません。

-   `enable-make-up-replica`は、レプリカを作成する機能を有効にするために使用されます。 `false`に設定すると、PD は十分なレプリカがないリージョンのレプリカを追加しません。

-   `enable-remove-extra-replica`は、余分なレプリカを削除する機能を有効にするために使用されます。 `false`に設定すると、PD は冗長レプリカを持つリージョンの余分なレプリカを削除しません。

-   分離レベルのチェックを有効にするには、 `enable-location-replacement`を使用します。 `false`に設定すると、PD はスケジューリングによってリージョンレプリカの分離レベルを上げません。

-   `enable-debug-metrics`は、デバッグ用のメトリックを有効にするために使用されます。 `true`に設定すると、PD は`balance-tolerant-size`などのいくつかのメトリックを有効にします。

-   `enable-placement-rules` 、v5.0 以降のバージョンでデフォルトで有効になっている配置ルールを有効にするために使用されます。

-   `store-limit-mode`は、ストア速度を制限するモードを制御するために使用されます。オプションのモードは`auto`と`manual`です。 `auto`モードでは、負荷に応じてストアが自動的にバランス調整されます (実験的)。

-   PD は、フロー番号の最下位桁を四捨五入します。これにより、リージョンフロー情報の変更によって引き起こされる統計の更新が減少します。この構成項目は、リージョンフロー情報を丸める最小桁数を指定するために使用されます。たとえば、デフォルト値が`3`であるため、フロー`100512` `101000`に丸められます。この構成は`trace-region-flow`を置き換えます。

-   たとえば、 `flow-round-by-digit`の値を`4`に設定します。

    {{< copyable "" >}}

    ```bash
    config set flow-round-by-digit 4
    ```

#### <code>config placement-rules [disable | enable | load | save | show | rule-group]</code> {#code-config-placement-rules-disable-enable-load-save-show-rule-group-code}

`config placement-rules [disable | enable | load | save | show | rule-group]`の使い方は[配置ルールを構成する](/configure-placement-rules.md#configure-rules)を参照。

### <code>health</code> {#code-health-code}

このコマンドを使用して、クラスターのヘルス情報を表示します。

使用法：

```bash
>> health                                // Display the health information
[
  {
    "name": "pd",
    "member_id": 13195394291058371180,
    "client_urls": [
      "http://127.0.0.1:2379"
      ......
    ],
    "health": true
  }
  ......
]
```

### <code>hot [read | write | store|  history &#x3C;start_time> &#x3C;end_time> [&#x3C;key> &#x3C;value>]]</code> {#code-hot-read-write-store-history-x3c-start-time-x3c-end-time-x3c-key-x3c-value-code}

このコマンドを使用して、クラスターのホット スポット情報を表示します。

使用法：

```bash
>> hot read                                // Display hot spot for the read operation
>> hot write                               // Display hot spot for the write operation
>> hot store                               // Display hot spot for all the read and write operations
>> hot history 1629294000000 1631980800000 // Display history hot spot for the specified period (milliseconds). 1629294000000 is the start time and 1631980800000 is the end time.
{
  "history_hot_region": [
    {
      "update_time": 1630864801948,
      "region_id": 103,
      "peer_id": 1369002,
      "store_id": 3,
      "is_leader": true,
      "is_learner": false,
      "hot_region_type": "read",
      "hot_degree": 152,
      "flow_bytes": 0,
      "key_rate": 0,
      "query_rate": 305,
      "start_key": "7480000000000000FF5300000000000000F8",
      "end_key": "7480000000000000FF5600000000000000F8"
    },
    ...
  ]
}
>> hot history 1629294000000 1631980800000 hot_region_type read region_id 1,2,3 store_id 1,2,3 peer_id 1,2,3 is_leader true is_learner true // Display history hotspot for the specified period with more conditions
{
  "history_hot_region": [
    {
      "update_time": 1630864801948,
      "region_id": 103,
      "peer_id": 1369002,
      "store_id": 3,
      "is_leader": true,
      "is_learner": false,
      "hot_region_type": "read",
      "hot_degree": 152,
      "flow_bytes": 0,
      "key_rate": 0,
      "query_rate": 305,
      "start_key": "7480000000000000FF5300000000000000F8",
      "end_key": "7480000000000000FF5600000000000000F8"
    },
    ...
  ]
}
```

### <code>label [store &#x3C;name> &#x3C;value>]</code> {#code-label-store-x3c-name-x3c-value-code}

このコマンドを使用して、クラスターのラベル情報を表示します。

使用法：

```bash
>> label                                // Display all labels
>> label store zone cn                  // Display all stores including the "zone":"cn" label
```

### <code>member [delete | leader_priority | leader [show | resign | transfer &#x3C;member_name>]]</code> {#code-member-delete-leader-priority-leader-show-resign-transfer-x3c-member-name-code}

このコマンドを使用して、PD メンバーを表示したり、指定したメンバーを削除したり、リーダーの優先順位を構成したりします。

使用法：

```bash
>> member                               // Display the information of all members
{
  "header": {......},
  "members": [......],
  "leader": {......},
  "etcd_leader": {......},
}
>> member delete name pd2               // Delete "pd2"
Success!
>> member delete id 1319539429105371180 // Delete a node using id
Success!
>> member leader show                   // Display the leader information
{
  "name": "pd",
  "member_id": 13155432540099656863,
  "peer_urls": [......],
  "client_urls": [......]
}
>> member leader resign // Move leader away from the current member
......
>> member leader transfer pd3 // Migrate leader to a specified member
......
```

### <code>operator [check | show | add | remove]</code> {#code-operator-check-show-add-remove-code}

このコマンドを使用して、スケジューリング操作を表示および制御します。

使用法：

```bash
>> operator show                                        // Display all operators
>> operator show admin                                  // Display all admin operators
>> operator show leader                                 // Display all leader operators
>> operator show region                                 // Display all Region operators
>> operator add add-peer 1 2                            // Add a replica of Region 1 on store 2
>> operator add add-learner 1 2                         // Add a learner replica of Region 1 on store 2
>> operator add remove-peer 1 2                         // Remove a replica of Region 1 on store 2
>> operator add transfer-leader 1 2                     // Schedule the leader of Region 1 to store 2
>> operator add transfer-region 1 2 3 4                 // Schedule Region 1 to stores 2,3,4
>> operator add transfer-peer 1 2 3                     // Schedule the replica of Region 1 on store 2 to store 3
>> operator add merge-region 1 2                        // Merge Region 1 with Region 2
>> operator add split-region 1 --policy=approximate     // Split Region 1 into two Regions in halves, based on approximately estimated value
>> operator add split-region 1 --policy=scan            // Split Region 1 into two Regions in halves, based on accurate scan value
>> operator remove 1                                    // Remove the scheduling operation of Region 1
>> operator check 1                                     // Check the status of the operators related to Region 1
```

リージョンの分割は、できるだけ中央に近い位置から開始します。この位置は、「スキャン」と「概算」という 2 つの戦略を使用して見つけることができます。それらの違いは、前者はリージョン をスキャンして中間キーを決定し、後者は SST ファイルに記録された統計をチェックしておおよその位置を取得することです。一般に、前者はより正確ですが、後者はより少ない I/O を消費し、より速く完了することができます。

### <code>ping</code> {#code-ping-code}

このコマンドを使用して、 `ping` PD にかかる時間を表示します。

使用法：

```bash
>> ping
time: 43.12698ms
```

### <code>region &#x3C;region_id> [--jq="&#x3C;query string>"]</code> {#code-region-x3c-region-id-jq-x3c-query-string-code}

このコマンドを使用して、リージョン情報を表示します。 jq 形式の出力については、 [jq-formatted-json-output-usage](#jq-formatted-json-output-usage)を参照してください。

使用法：

```bash
>> region                               //　Display the information of all Regions
{
  "count": 1,
  "regions": [......]
}

>> region 2                             // Display the information of the Region with the ID of 2
{
  "id": 2,
  "start_key": "7480000000000000FF1D00000000000000F8",
  "end_key": "7480000000000000FF1F00000000000000F8",
  "epoch": {
    "conf_ver": 1,
    "version": 15
  },
  "peers": [
    {
      "id": 40,
      "store_id": 3
    }
  ],
  "leader": {
    "id": 40,
    "store_id": 3
  },
  "written_bytes": 0,
  "read_bytes": 0,
  "written_keys": 0,
  "read_keys": 0,
  "approximate_size": 1,
  "approximate_keys": 0
}
```

### <code>region key [--format=raw|encode|hex] &#x3C;key></code> {#code-region-key-format-raw-encode-hex-x3c-key-code}

このコマンドを使用して、特定のキーが存在するリージョンを照会します。未加工、エンコード、および 16 進形式をサポートしています。また、キーがエンコーディング形式の場合は、キーを一重引用符で囲む必要があります。

16 進形式の使用法 (デフォルト):

```bash
>> region key 7480000000000000FF1300000000000000F8
{
  "region": {
    "id": 2,
    ......
  }
}
```

Raw フォーマットの使用法:

```bash
>> region key --format=raw abc
{
  "region": {
    "id": 2,
    ......
  }
}
```

エンコード形式の使用法:

```bash
>> region key --format=encode 't\200\000\000\000\000\000\000\377\035_r\200\000\000\000\000\377\017U\320\000\000\000\000\000\372'
{
  "region": {
    "id": 2,
    ......
  }
}
```

### <code>region scan</code> {#code-region-scan-code}

このコマンドを使用して、すべてのリージョンを取得します。

使用法：

```bash
>> region scan
{
  "count": 20,
  "regions": [......],
}
```

### <code>region sibling &#x3C;region_id></code> {#code-region-sibling-x3c-region-id-code}

このコマンドを使用して、特定のリージョンの隣接する Region を確認します。

使用法：

```bash
>> region sibling 2
{
  "count": 2,
  "regions": [......],
}
```

### <code>region keys [--format=raw|encode|hex] &#x3C;start_key> &#x3C;end_key> &#x3C;limit></code> {#code-region-keys-format-raw-encode-hex-x3c-start-key-x3c-end-key-x3c-limit-code}

このコマンドを使用して、特定の範囲`[startkey, endkey)`内のすべてのリージョンを照会します。 `endKey`秒のない範囲がサポートされています。

`limit`パラメータは、キーの数を制限します。デフォルト値`limit` `16`で、値`-1`は無制限のキーを意味します。

使用法：

```bash
>> region keys --format=raw a         // Display all Regions that start from the key a with a default limit count of 16
{
  "count": 16,
  "regions": [......],
}

>> region keys --format=raw a z      // Display all Regions in the range [a, z) with a default limit count of 16
{
  "count": 16,
  "regions": [......],
}

>> region keys --format=raw a z -1   // Display all Regions in the range [a, z) without a limit count
{
  "count": ...,
  "regions": [......],
}

>> region keys --format=raw a "" 20   // Display all Regions that start from the key a with a limit count of 20
{
  "count": 20,
  "regions": [......],
}
```

### <code>region store &#x3C;store_id></code> {#code-region-store-x3c-store-id-code}

このコマンドを使用して、特定のストアのすべてのリージョンを一覧表示します。

使用法：

```bash
>> region store 2
{
  "count": 10,
  "regions": [......],
}
```

### <code>region topread [limit]</code> {#code-region-topread-limit-code}

このコマンドを使用して、読み取りフローが上位のリージョンを一覧表示します。制限のデフォルト値は 16 です。

使用法：

```bash
>> region topread
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topwrite [limit]</code> {#code-region-topwrite-limit-code}

このコマンドを使用して、書き込みフローが上位のリージョンを一覧表示します。制限のデフォルト値は 16 です。

使用法：

```bash
>> region topwrite
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topconfver [limit]</code> {#code-region-topconfver-limit-code}

このコマンドを使用して、最上位の conf バージョンでリージョンを一覧表示します。制限のデフォルト値は 16 です。

使用法：

```bash
>> region topconfver
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topversion [limit]</code> {#code-region-topversion-limit-code}

このコマンドを使用して、トップ バージョンのリージョンを一覧表示します。制限のデフォルト値は 16 です。

使用法：

```bash
>> region topversion
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topsize [limit]</code> {#code-region-topsize-limit-code}

このコマンドを使用して、上部のおおよそのサイズでリージョンを一覧表示します。制限のデフォルト値は 16 です。

使用法：

```bash
>> region topsize
{
  "count": 16,
  "regions": [......],
}

```

### <code>region check [miss-peer | extra-peer | down-peer | pending-peer | offline-peer | empty-region | hist-size | hist-keys]</code> {#code-region-check-miss-peer-extra-peer-down-peer-pending-peer-offline-peer-empty-region-hist-size-hist-keys-code}

このコマンドを使用して、異常な状態のリージョンをチェックします。

さまざまなタイプの説明:

-   miss-peer: 十分なレプリカがないリージョン
-   extra-peer: 追加のレプリカを持つリージョン
-   down-peer: 一部のレプリカがダウンしているリージョン
-   pending-peer：一部のレプリカが保留中のリージョン

使用法：

```bash
>> region check miss-peer
{
  "count": 2,
  "regions": [......],
}
```

### <code>scheduler [show | add | remove | pause | resume | config]</code> {#code-scheduler-show-add-remove-pause-resume-config-code}

このコマンドを使用して、スケジューリング ポリシーを表示および制御します。

使用法：

```bash
>> scheduler show                                 // Display all schedulers
>> scheduler add grant-leader-scheduler 1         // Schedule all the leaders of the Regions on store 1 to store 1
>> scheduler add evict-leader-scheduler 1         // Move all the Region leaders on store 1 out
>> scheduler config evict-leader-scheduler        // Display the stores in which the scheduler is located since v4.0.0
>> scheduler add shuffle-leader-scheduler         // Randomly exchange the leader on different stores
>> scheduler add shuffle-region-scheduler         // Randomly scheduling the Regions on different stores
>> scheduler add evict-slow-store-scheduler       // When there is one and only one slow store, evict all Region leaders of that store
>> scheduler remove grant-leader-scheduler-1      // Remove the corresponding scheduler, and `-1` corresponds to the store ID
>> scheduler pause balance-region-scheduler 10    // Pause the balance-region scheduler for 10 seconds
>> scheduler pause all 10                         // Pause all schedulers for 10 seconds
>> scheduler resume balance-region-scheduler      // Continue to run the balance-region scheduler
>> scheduler resume all                           // Continue to run all schedulers
>> scheduler config balance-hot-region-scheduler  // Display the configuration of the balance-hot-region scheduler
```

#### <code>scheduler config balance-hot-region-scheduler</code> {#code-scheduler-config-balance-hot-region-scheduler-code}

このコマンドを使用して、 `balance-hot-region-scheduler`ポリシーを表示および制御します。

使用法：

```bash
>> scheduler config balance-hot-region-scheduler  // Display all configuration of the balance-hot-region scheduler
{
  "min-hot-byte-rate": 100,
  "min-hot-key-rate": 10,
  "min-hot-query-rate": 10,
  "max-zombie-rounds": 3,
  "max-peer-number": 1000,
  "byte-rate-rank-step-ratio": 0.05,
  "key-rate-rank-step-ratio": 0.05,
  "query-rate-rank-step-ratio": 0.05,
  "count-rank-step-ratio": 0.01,
  "great-dec-ratio": 0.95,
  "minor-dec-ratio": 0.99,
  "src-tolerance-ratio": 1.05,
  "dst-tolerance-ratio": 1.05,
  "read-priorities": [
    "query",
    "byte"
  ],
  "write-leader-priorities": [
    "key",
    "byte"
  ],
  "write-peer-priorities": [
    "byte",
    "key"
  ],
  "strict-picking-store": "true",
  "enable-for-tiflash": "true"
}
```

-   `min-hot-byte-rate`カウントされる最小のバイト数を意味し、通常は 100 です。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-byte-rate 100
    ```

-   `min-hot-key-rate`カウントされるキーの最小数を意味し、通常は 10 です。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-key-rate 10
    ```

-   `min-hot-query-rate`カウントされるクエリの最小数を意味し、通常は 10 です。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-query-rate 10
    ```

-   `max-zombie-rounds`オペレーターが保留中の影響と見なすことができるハートビートの最大数を意味します。より大きな値に設定すると、保留中の影響に含まれるオペレーターが増える可能性があります。通常、その値を調整する必要はありません。保留中の影響とは、スケジューリング中に生成されるが、まだ効果があるオペレーターの影響を指します。

    ```bash
    scheduler config balance-hot-region-scheduler set max-zombie-rounds 3
    ```

-   `max-peer-number`解決されるピアの最大数を意味し、スケジューラが遅すぎるのを防ぎます。

    ```bash
    scheduler config balance-hot-region-scheduler set max-peer-number 1000
    ```

-   `byte-rate-rank-step-ratio` 、 `key-rate-rank-step-ratio` 、 `query-rate-rank-step-ratio` 、および`count-rank-step-ratio` 、それぞれバイト、キー、クエリ、およびカウントのステップ ランクを意味します。ランクステップ比は、ランクを計算する際のステップを決定します。 `great-dec-ratio`と`minor-dec-ratio` `dec`ランクを決定するために使用されます。通常、これらの項目を変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set byte-rate-rank-step-ratio 0.05
    ```

-   `src-tolerance-ratio`と`dst-tolerance-ratio`は、期待スケジューラの設定項目です。 `tolerance-ratio`が小さいほど、スケジューリングが容易になります。冗長なスケジューリングが発生した場合は、この値を適切に増やすことができます。

    ```bash
    scheduler config balance-hot-region-scheduler set src-tolerance-ratio 1.1
    ```

-   `read-priorities` 、 `write-leader-priorities` 、および`write-peer-priorities` 、スケジューラーがホットリージョンスケジューリングで優先するディメンションを制御します。構成では 2 つのディメンションがサポートされています。

    -   `read-priorities`と`write-leader-priorities` 、読み取りおよび書き込みリーダー タイプのホット リージョンをスケジュールするためにスケジューラが優先するディメンションを制御します。次元オプションは`query` 、 `byte` 、および`key`です。

    -   `write-peer-priorities`書き込みピア タイプのホット リージョンをスケジュールするために、スケジューラがどのディメンションを優先するかを制御します。次元オプションは`byte`と`key`です。

    > **ノート：**
    >
    > クラスタコンポーネントがv5.2 より前の場合、 `query`ディメンションの構成は有効になりません。一部のコンポーネントが v5.2 以降にアップグレードされた場合でも、デフォルトでは`byte`と`key`が引き続きホットリージョンスケジューリングの優先順位を持ちます。クラスターのすべてのコンポーネントが v5.2 以降にアップグレードされた後も、そのような構成は互換性のために有効になります。 `pd-ctl`コマンドを使用して、リアルタイムの構成を表示できます。通常、これらの構成を変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set read-priorities query,byte
    ```

-   `strict-picking-store`ホットリージョンスケジューリングの検索スペースを制御します。通常は有効になっています。有効にすると、ホットリージョンスケジューリングにより、構成された 2 つのディメンションでホットスポットのバランスが確保されます。無効にすると、ホットリージョンスケジューリングは優先度が最も高いディメンションのバランスのみを確保するため、他のディメンションのバランスが低下する可能性があります。通常、この構成を変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set strict-picking-store true
    ```

-   `enable-for-tiflash`ホットリージョンスケジューリングがTiFlashインスタンスに対して有効かどうかを制御します。通常は有効になっています。無効にすると、 TiFlashインスタンス間のホットリージョンスケジューリングは実行されません。

    ```bash
    scheduler config balance-hot-region-scheduler set enable-for-tiflash true
    ```

### <code>service-gc-safepoint</code> {#code-service-gc-safepoint-code}

このコマンドを使用して、現在の GC セーフポイントとサービス GC セーフポイントを照会します。出力は次のとおりです。

```bash
{
  "service_gc_safe_points": [
    {
      "service_id": "gc_worker",
      "expired_at": 9223372036854775807,
      "safe_point": 439923410637160448
    }
  ],
  "gc_safe_point": 0
}
```

### <code>store [delete | label | weight | remove-tombstone | limit ] &#x3C;store_id>  [--jq="&#x3C;query string>"]</code> {#code-store-delete-label-weight-remove-tombstone-limit-x3c-store-id-jq-x3c-query-string-code}

このコマンドを使用して、ストア情報を表示したり、指定したストアを削除したりします。 jq 形式の出力については、 [jq-formatted-json-output-usage](#jq-formatted-json-output-usage)を参照してください。

使用法：

```bash
>> store                               // Display information of all stores
{
  "count": 3,
  "stores": [...]
}
>> store 1                             // Get the store with the store id of 1
......
>> store delete 1                      // Delete the store with the store id of 1
......
>> store label 1 zone cn               // Set the value of the label with the "zone" key to "cn" for the store with the store id of 1
>> store weight 1 5 10                 // Set the leader weight to 5 and Region weight to 10 for the store with the store id of 1
>> store remove-tombstone              // Remove stores that are in tombstone state
>> store limit                         // Show the speed limit of adding-peer operations and the limit of removing-peer operations per minute in all stores
>> store limit add-peer                // Show the speed limit of adding-peer operations per minute in all stores
>> store limit remove-peer             // Show the limit of removing-peer operations per minute in all stores
>> store limit all 5                   // Set the limit of adding-peer operations to 5 and the limit of removing-peer operations to 5 per minute for all stores
>> store limit 1 5                     // Set the limit of adding-peer operations to 5 and the limit of removing-peer operations to 5 per minute for store 1
>> store limit all 5 add-peer          // Set the limit of adding-peer operations to 5 per minute for all stores
>> store limit 1 5 add-peer            // Set the limit of adding-peer operations to 5 per minute for store 1
>> store limit 1 5 remove-peer         // Set the limit of removing-peer operations to 5 per minute for store 1
>> store limit all 5 remove-peer       // Set the limit of removing-peer operations to 5 per minute for all stores
```

> **ノート：**
>
> `pd-ctl`を使用して、TiKV ストアのステータス (アップ、切断、オフライン、ダウン、または廃棄) を確認できます。各ステータスの関係は[TiKV店舗の各ステータスの関係](/tidb-scheduling.md#information-collection)を参照してください。

### <code>log [fatal | error | warn | info | debug]</code> {#code-log-fatal-error-warn-info-debug-code}

このコマンドを使用して、PD リーダーのログ レベルを設定します。

使用法：

```bash
log warn
```

### <code>tso</code> {#code-tso-code}

このコマンドを使用して、TSO の物理時刻と論理時刻を解析します。

使用法：

```bash
>> tso 395181938313123110        // Parse TSO
system:  2017-10-09 05:50:59 +0800 CST
logic:  120102
```

### <code>unsafe remove-failed-stores [store-ids | show | history]</code> {#code-unsafe-remove-failed-stores-store-ids-show-history-code}

> **警告：**
>
> -   この機能は非可逆リカバリであるため、TiKV は機能の使用後にデータの整合性とデータ インデックスの整合性を保証できません。
> -   Online Unsafe Recovery は実験的機能であり、本番環境で使用することは**お**勧めしません。この機能のインターフェイス、戦略、および内部実装は、一般提供 (GA) になったときに変更される可能性があります。この機能はいくつかのシナリオでテストされていますが、完全に検証されておらず、システムが使用できなくなる可能性があります。
> -   TiDB チームのサポートを受けて機能関連の操作を実行することをお勧めします。操作を誤ると、クラスタの復旧が困難になる場合があります。

このコマンドを使用して、永続的に損傷したレプリカによってデータが使用できなくなった場合に、損失のある回復操作を実行します。例えば：

Online Unsafe Recovery を実行して、完全に破損したストアを削除します。

```bash
unsafe remove-failed-stores 101,102,103
```

```bash
Success!
```

Online Unsafe Recovery の現在または過去の状態を表示します。

```bash
unsafe remove-failed-stores show
```

```bash
[
  "Collecting cluster info from all alive stores, 10/12.",
  "Stores that have reports to PD: 1, 2, 3, ...",
  "Stores that have not reported to PD: 11, 12",
]
```

```bash
>> unsafe remove-failed-stores history
```

```bash
[
  "Store reports collection:",
  "Store 7: region 3 [start_key, end_key), {peer1, peer2, peer3} region 4 ...",
  "Store 8: region ...",
  "...",
  "Recovery Plan:",
  "Store 7, creates: region 11, region 12, ...; updates: region 21, region 22, ... deletes: ... ",
  "Store 8, ..."
  "...",
  "Execution Progress:",
  "Store 10 finished,",
  "Store 7 not yet finished",
  "...",
]
```

## Jq 形式の JSON 出力の使用法 {#jq-formatted-json-output-usage}

### <code>store</code>の出力を簡素化する {#simplify-the-output-of-code-store-code}

```bash
>> store --jq=".stores[].store | { id, address, state_name}"
{"id":1,"address":"127.0.0.1:20161","state_name":"Up"}
{"id":30,"address":"127.0.0.1:20162","state_name":"Up"}
...
```

### ノードの残りのスペースを照会する {#query-the-remaining-space-of-the-node}

```bash
>> store --jq=".stores[] | {id: .store.id, available: .status.available}"
{"id":1,"available":"10 GiB"}
{"id":30,"available":"10 GiB"}
...
```

### ステータスが<code>Up</code>でないすべてのノードを照会する {#query-all-nodes-whose-status-is-not-code-up-code}

{{< copyable "" >}}

```bash
store --jq='.stores[].store | select(.state_name!="Up") | { id, address, state_name}'
```

```
{"id":1,"address":"127.0.0.1:20161""state_name":"Offline"}
{"id":5,"address":"127.0.0.1:20162""state_name":"Offline"}
...
```

### すべてのTiFlashノードを照会する {#query-all-tiflash-nodes}

{{< copyable "" >}}

```bash
store --jq='.stores[].store | select(.labels | length>0 and contains([{"key":"engine","value":"tiflash"}])) | { id, address, state_name}'
```

```
{"id":1,"address":"127.0.0.1:20161""state_name":"Up"}
{"id":5,"address":"127.0.0.1:20162""state_name":"Up"}
...
```

### リージョンレプリカの配布ステータスを照会する {#query-the-distribution-status-of-the-region-replicas}

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id]}"
{"id":2,"peer_stores":[1,30,31]}
{"id":4,"peer_stores":[1,31,34]}
...
```

### レプリカの数に応じてリージョンをフィルタリングする {#filter-regions-according-to-the-number-of-replicas}

たとえば、レプリカの数が 3 ではないすべてのリージョンを除外するには、次のようにします。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length != 3)}"
{"id":12,"peer_stores":[30,32]}
{"id":2,"peer_stores":[1,30,31,32]}
```

### レプリカのストア ID に従ってリージョンをフィルター処理する {#filter-regions-according-to-the-store-id-of-replicas}

たとえば、store30 にレプリカがあるすべてのリージョンを除外するには、次のようにします。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==30))}"
{"id":6,"peer_stores":[1,30,31]}
{"id":22,"peer_stores":[1,30,32]}
...
```

同じ方法で、store30 または store31 にレプリカがあるすべてのリージョンを見つけることもできます。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==(30,31)))}"
{"id":16,"peer_stores":[1,30,34]}
{"id":28,"peer_stores":[1,30,32]}
{"id":12,"peer_stores":[30,32]}
...
```

### データの復元時に関連するリージョンを探す {#look-for-relevant-regions-when-restoring-data}

たとえば、[store1, store30, store31] がダウンタイムに利用できない場合、ダウン レプリカが通常のレプリカより多いすべてのリージョンを見つけることができます。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length as $total | map(if .==(1,30,31) then . else empty end) | length>=$total-length) }"
{"id":2,"peer_stores":[1,30,31,32]}
{"id":12,"peer_stores":[30,32]}
{"id":14,"peer_stores":[1,30,32]}
...
```

または、[store1, store30, store31] が起動に失敗した場合、store1 でデータを手動で安全に削除できるリージョンを見つけることができます。このようにして、store1 にレプリカがあるが他の DownPeer を持たないすべてのリージョンを除外できます。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length>1 and any(.==1) and all(.!=(30,31)))}"
{"id":24,"peer_stores":[1,32,33]}
```

[store30, store31] がダウンしている場合、 `remove-peer` Operator を作成することで安全に処理できるすべてのリージョン、つまり DownPeer が 1 つだけのリージョンを見つけます。

```bash
>> region --jq=".regions[] | {id: .id, remove_peer: [.peers[].store_id] | select(length>1) | map(if .==(30,31) then . else empty end) | select(length==1)}"
{"id":12,"remove_peer":[30]}
{"id":4,"remove_peer":[31]}
{"id":22,"remove_peer":[30]}
...
```
