---
title: PD Control User Guide
summary: Use PD Control to obtain the state information of a cluster and tune a cluster.
---

# PD制御ユーザーガイド {#pd-control-user-guide}

PDのコマンドラインツールとして、PD Controlはクラスターの状態情報を取得し、クラスタを調整しクラスタ。

## PD制御をインストールします {#install-pd-control}

> **ノート：**
>
> 使用するコントロールツールのバージョンは、クラスタのバージョンと一致していることをお勧めします。

### TiUPコマンドを使用する {#use-tiup-command}

PD制御を使用するには、 `tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> [-i]`コマンドを実行します。

### インストールパッケージをダウンロードする {#download-the-installation-package}

PD制御インストールパッケージ（ `pd-ctl` ）は、TiDBツールキットに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロードする](/download-ecosystem-tools.md)を参照してください。

### ソースコードからコンパイルする {#compile-from-source-code}

1.  [行け](https://golang.org/) Goモジュールが使用されているため、バージョン1.13以降。
2.  [PDプロジェクト](https://github.com/pingcap/pd)のルートディレクトリで、 `make`または`make pd-ctl`コマンドを使用して`bin/pd-ctl`をコンパイルおよび生成します。

## 使用法 {#usage}

シングルコマンドモード：

```bash
tiup ctl pd store -u http://127.0.0.1:2379
```

インタラクティブモード：

```bash
tiup ctl pd -i -u http://127.0.0.1:2379
```

環境変数を使用する：

```bash
export PD_ADDR=http://127.0.0.1:2379
tiup ctl pd
```

TLSを使用して暗号化します。

```bash
tiup ctl pd -u https://127.0.0.1:2379 --cacert="path/to/ca" --cert="path/to/cert" --key="path/to/key"
```

## コマンドラインフラグ {#command-line-flags}

### <code>--cacert</code> {#code-cacert-code}

-   信頼できるCAの証明書ファイルへのパスをPEM形式で指定します
-   デフォルト： &quot;&quot;

### <code>--cert</code> {#code-cert-code}

-   SSLの証明書へのパスをPEM形式で指定します
-   デフォルト： &quot;&quot;

### <code>--detach</code> / <code>-d</code> {#code-detach-code-code-d-code}

-   シングルコマンドラインモードを使用します（readlineに入らない）
-   デフォルト：true

### -- <code>--help</code> / <code>-h</code> {#code-help-code-code-h-code}

-   ヘルプ情報を出力します
-   デフォルト：false

### -- <code>--interact</code> / <code>-i</code> {#code-interact-code-code-i-code}

-   インタラクティブモードを使用します（readlineに入る）
-   デフォルト：false

### <code>--key</code> {#code-key-code}

-   SSLの証明書キーファイルへのパスをPEM形式で指定します。これは、 `--cert`で指定された証明書の秘密キーです。
-   デフォルト： &quot;&quot;

### <code>--pd</code> / <code>-u</code> {#code-pd-code-code-u-code}

-   PDアドレスを指定します
-   デフォルトアドレス： `http://127.0.0.1:2379`
-   環境変数： `PD_ADDR`

### -- <code>--version</code> / <code>-V</code> {#code-version-code-code-v-code}

-   バージョン情報を出力して終了します
-   デフォルト：false

## 指示 {#command}

### <code>cluster</code> {#code-cluster-code}

このコマンドを使用して、クラスタの基本情報を表示します。

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

-   `max-snapshot-count`は、単一のストアが同時に受信または送信するスナップショットの最大数を制御します。スケジューラーは、通常のアプリケーションリソースを使用しないように、この構成によって制限されます。レプリカの追加やバランシングの速度を向上させる必要がある場合は、この値を増やしてください。

    ```bash
    config set max-snapshot-count 64  // Set the maximum number of snapshots to 64
    ```

-   `max-pending-peer-count`は、単一ストア内の保留中のピアの最大数を制御します。一部のノードで最新のログがない状態で多数のリージョンが生成されないように、スケジューラーはこの構成によって制限されます。レプリカの追加やバランシングの速度を向上させる必要がある場合は、この値を増やしてください。 0に設定すると、制限がないことを示します。

    ```bash
    config set max-pending-peer-count 64  // Set the maximum number of pending peers to 64
    ```

-   `max-merge-region-size`は、リージョンマージのサイズの上限を制御します（単位はMです）。 `regionSize`が指定された値を超えると、PDはそれを隣接するリージョンとマージしません。 0に設定すると、リージョンマージが無効になります。

    ```bash
    config set max-merge-region-size 16 // Set the upper limit on the size of Region Merge to 16M
    ```

-   `max-merge-region-keys`は、リージョンマージのキーカウントの上限を制御します。 `regionKeyCount`が指定された値を超えると、PDはそれを隣接するリージョンとマージしません。

    ```bash
    config set max-merge-region-keys 50000 // Set the the upper limit on keyCount to 50000
    ```

-   `split-merge-interval`は、同じリージョンでの`split`つの操作と`merge`の操作の間の間隔を制御します。これは、新しく分割されたリージョンが一定期間内にマージされないことを意味します。

    ```bash
    config set split-merge-interval 24h  // Set the interval between `split` and `merge` to one day
    ```

-   `enable-one-way-merge`は、PDがリージョンを次のリージョンとマージすることのみを許可するかどうかを制御します。 `false`に設定すると、PDにより、リージョンを隣接する2つのリージョンとマージできます。

    ```bash
    config set enable-one-way-merge true  // Enables one-way merging.
    ```

-   `enable-cross-table-merge`は、クロステーブルリージョンのマージを有効にするために使用されます。 `false`に設定すると、PDは異なるテーブルのリージョンをマージしません。このオプションは、キータイプが「テーブル」の場合にのみ機能します。

    ```bash
    config set enable-cross-table-merge true  // Enable cross table merge.
    ```

-   `key-type`は、クラスタに使用されるキーエンコードタイプを指定します。サポートされているオプションは[&quot;table&quot;、 &quot;raw&quot;、 &quot;txn&quot;]で、デフォルト値は&quot;table&quot;です。

    -   クラスタにTiDBインスタンスが存在しない場合、 `key-type`は「raw」または「txn」になり、PDは、 `enable-cross-table-merge`の設定に関係なく、テーブル間でリージョンをマージできます。
    -   クラスタにTiDBインスタンスが存在する場合、 `key-type`は「テーブル」である必要があります。 PDがテーブル間でリージョンをマージできるかどうかは`enable-cross-table-merge`によって決定されます。 `key-type`が「生」の場合、配置ルールは機能しません。

    ```bash
    config set key-type raw  // Enable cross table merge.
    ```

-   `region-score-formula-version`は、リージョンスコア式のバージョンを制御します。値のオプションは`v1`と`v2`です。式のバージョン2は、TiKVノードをオンラインまたはオフラインにするなど、一部のシナリオで冗長バランス領域スケジューリングを削減するのに役立ちます。

    {{< copyable "" >}}

    ```bash
    config set region-score-formula-version v2
    ```

-   `patrol-region-interval`は、 `replicaChecker`がリージョンのヘルスステータスをチェックする実行頻度を制御します。間隔が短いほど、実行頻度が高くなります。通常、調整する必要はありません。

    ```bash
    config set patrol-region-interval 10ms // Set the execution frequency of replicaChecker to 10ms
    ```

-   `max-store-down-time`は、PDが切断されたストアを超えた場合に復元できないと判断する時間を制御します。 PDが指定された期間内にストアからハートビートを受信しない場合、PDは他のノードにレプリカを追加します。

    ```bash
    config set max-store-down-time 30m  // Set the time within which PD receives no heartbeats and after which PD starts to add replicas to 30 minutes
    ```

-   `max-store-preparing-time`は、ストアがオンラインになるまでの最大待機時間を制御します。ストアのオンライン段階で、PDはストアのオンライン進行状況を照会できます。指定された時間を超えると、PDはストアがオンラインであると見なし、ストアのオンライン進行状況を再度照会することはできません。ただし、これはリージョンが新しいオンラインストアに移行することを妨げるものではありません。ほとんどのシナリオでは、このパラメーターを調整する必要はありません。

    次のコマンドは、ストアがオンラインになるまでの最大待機時間を4時間に指定します。

    {{< copyable "" >}}

    ```bash
    config set max-store-preparing-time 4h
    ```

-   `leader-schedule-limit`は、リーダーを同時にスケジュールするタスクの数を制御します。この値は、リーダーのバランスの速度に影響します。値が大きいほど速度が速くなり、値を0に設定するとスケジューリングが終了します。通常、リーダースケジューリングの負荷は小さく、必要な値を増やすことができます。

    ```bash
    config set leader-schedule-limit 4         // 4 tasks of leader scheduling at the same time at most
    ```

-   `region-schedule-limit`は、同時にリージョンをスケジュールするタスクの数を制御します。この値は、作成されるリージョンバランス演算子が多すぎるのを防ぎます。デフォルト値は`2048`で、これはすべてのサイズのクラスターに十分です。値を`0`に設定すると、スケジューリングが終了します。通常、リージョンのスケジューリング速度は`store-limit`に制限されていますが、何をしているのかを正確に理解していない限り、この値をカスタマイズしないことをお勧めします。

    ```bash
    config set region-schedule-limit 2         // 2 tasks of Region scheduling at the same time at most
    ```

-   `replica-schedule-limit`は、レプリカを同時にスケジュールするタスクの数を制御します。この値は、ノードがダウンまたは削除されたときのスケジューリング速度に影響します。値が大きいほど速度が速くなり、値を0に設定するとスケジューリングが終了します。通常、レプリカスケジューリングには大きな負荷がかかるため、あまり大きな値を設定しないでください。この構成項目は通常、デフォルト値のままであることに注意してください。値を変更する場合は、いくつかの値を試して、実際の状況に応じてどれが最適に機能するかを確認する必要があります。

    ```bash
    config set replica-schedule-limit 4        // 4 tasks of replica scheduling at the same time at most
    ```

-   `merge-schedule-limit`は、リージョンマージスケジューリングタスクの数を制御します。値を0に設定すると、リージョンマージが閉じます。通常、マージスケジューリングには大きな負荷がかかるため、あまり大きな値を設定しないでください。この構成項目は通常、デフォルト値のままであることに注意してください。値を変更する場合は、いくつかの値を試して、実際の状況に応じてどれが最適に機能するかを確認する必要があります。

    ```bash
    config set merge-schedule-limit 16       // 16 tasks of Merge scheduling at the same time at most
    ```

-   `hot-region-schedule-limit`は、同時に実行されているホットリージョンスケジューリングタスクを制御します。その値を`0`に設定すると、スケジューリングが無効になります。大きすぎる値を設定することはお勧めしません。そうしないと、システムパフォーマンスに影響を与える可能性があります。この構成項目は通常、デフォルト値のままであることに注意してください。値を変更する場合は、いくつかの値を試して、実際の状況に応じてどれが最適に機能するかを確認する必要があります。

    ```bash
    config set hot-region-schedule-limit 4       // 4 tasks of hot Region scheduling at the same time at most
    ```

-   `hot-region-cache-hits-threshold`は、ホットリージョンを識別するために必要な分数を設定するために使用されます。 PDは、リージョンがこの分数を超えてホットスポット状態になった後でのみ、ホットスポットスケジューリングに参加できます。

-   `tolerant-size-ratio`は、バランスバッファ領域のサイズを制御します。 2つのストアのリーダーまたはリージョン間のスコアの差がリージョンサイズの指定された倍数よりも小さい場合、PDによってバランスが取れていると見なされます。

    ```bash
    config set tolerant-size-ratio 20        // Set the size of the buffer area to about 20 times of the average Region Size
    ```

-   `low-space-ratio`は、不十分な保管スペースと見なされるしきい値を制御します。ノードが占めるスペースの比率が指定された値を超えると、PDはデータを対応するノードにできるだけ移行しないようにします。同時に、PDは主に残りのスペースをスケジュールして、対応するノードのディスクスペースを使い果たしないようにします。

    ```bash
    config set low-space-ratio 0.9              // Set the threshold value of insufficient space to 0.9
    ```

-   `high-space-ratio`は、十分な保管スペースと見なされるしきい値を制御します。この構成は、 `region-score-formula-version`が`v1`に設定されている場合にのみ有効になります。ノードが占めるスペースの比率が指定された値よりも小さい場合、PDは残りのスペースを無視し、主に実際のデータボリュームをスケジュールします。

    ```bash
    config set high-space-ratio 0.5             // Set the threshold value of sufficient space to 0.5
    ```

-   `cluster-version`はクラスタのバージョンであり、一部の機能を有効または無効にし、互換性の問題に対処するために使用されます。デフォルトでは、これはクラスタで通常実行されているすべてのTiKVノードの最小バージョンです。以前のバージョンにロールバックする必要がある場合にのみ、手動で設定できます。

    ```bash
    config set cluster-version 1.0.8              // Set the version of the cluster to 1.0.8
    ```

-   `replication-mode`は、デュアルデータセンターシナリオのリージョンのレプリケーションモードを制御します。詳細については、 [DR自動同期モードを有効にします](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)を参照してください。

-   `leader-schedule-policy`は、リーダーのスケジューリング戦略を選択するために使用されます。 `size`または`count`に従ってリーダーをスケジュールできます。

-   `scheduler-max-waiting-operator`は、各スケジューラーで待機しているオペレーターの数を制御するために使用されます。

-   `enable-remove-down-replica`は、DownReplicaを自動的に削除する機能を有効にするために使用されます。 `false`に設定すると、PDはダウンタイムレプリカを自動的にクリーンアップしません。

-   `enable-replace-offline-replica`は、OfflineReplicaの移行機能を有効にするために使用されます。 `false`に設定すると、PDはオフラインレプリカを移行しません。

-   `enable-make-up-replica`は、レプリカを作成する機能を有効にするために使用されます。 `false`に設定すると、PDは十分なレプリカがないリージョンのレプリカを追加しません。

-   `enable-remove-extra-replica`は、余分なレプリカを削除する機能を有効にするために使用されます。 `false`に設定すると、PDは冗長レプリカを持つリージョンの余分なレプリカを削除しません。

-   `enable-location-replacement`は、分離レベルチェックを有効にするために使用されます。 `false`に設定すると、PDはスケジューリングによってリージョンレプリカの分離レベルを上げません。

-   `enable-debug-metrics`は、デバッグ用のメトリックを有効にするために使用されます。 `true`に設定すると、PDは`balance-tolerant-size`などのいくつかのメトリックを有効にします。

-   `enable-placement-rules`は、配置ルールを有効にするために使用されます。これは、v5.0以降のバージョンではデフォルトで有効になっています。

-   `store-limit-mode`は、ストア速度を制限するモードを制御するために使用されます。オプションのモードは`auto`と`manual`です。 `auto`モードでは、店舗は負荷に応じて自動的にバランスが取られます（実験的）。

-   PDはフロー番号の最下位桁を丸めます。これにより、リージョンフロー情報の変更によって引き起こされる統計の更新が削減されます。この構成項目は、リージョンフロー情報を丸める最下位桁数を指定するために使用されます。たとえば、デフォルト値は`3`であるため、フロー`100512`は`101000`に丸められます。この構成は`trace-region-flow`を置き換えます。

-   たとえば、値を`flow-round-by-digit`から`4`に設定します。

    {{< copyable "" >}}

    ```bash
    config set flow-round-by-digit 4
    ```

#### <code>config placement-rules [disable | enable | load | save | show | rule-group]</code> {#code-config-placement-rules-disable-enable-load-save-show-rule-group-code}

`config placement-rules [disable | enable | load | save | show | rule-group]`の使用法については、 [配置ルールを構成する](/configure-placement-rules.md#configure-rules)を参照してください。

### <code>health</code> {#code-health-code}

このコマンドを使用して、クラスタのヘルス情報を表示します。

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

このコマンドを使用して、クラスタのホットスポット情報を表示します。

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

このコマンドを使用して、クラスタのラベル情報を表示します。

使用法：

```bash
>> label                                // Display all labels
>> label store zone cn                  // Display all stores including the "zone":"cn" label
```

### <code>member [delete | leader_priority | leader [show | resign | transfer &#x3C;member_name>]]</code> {#code-member-delete-leader-priority-leader-show-resign-transfer-x3c-member-name-code}

このコマンドを使用して、PDメンバーを表示したり、指定したメンバーを削除したり、リーダーの優先順位を設定したりします。

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

リージョンの分割は、可能な限り中央に近い位置から開始されます。この位置は、「スキャン」と「近似」の2つの戦略を使用して見つけることができます。違いは、前者はリージョンをスキャンして中央のキーを決定し、後者はSSTファイルに記録されている統計をチェックしておおよその位置を取得することです。一般に、前者の方が正確ですが、後者の方がI / Oの消費量が少なく、より速く完了することができます。

### <code>ping</code> {#code-ping-code}

このコマンドを使用して、 `ping`のPDにかかる時間を表示します。

使用法：

```bash
>> ping
time: 43.12698ms
```

### <code>region &#x3C;region_id> [--jq="&#x3C;query string>"]</code> {#code-region-x3c-region-id-jq-x3c-query-string-code}

このコマンドを使用して、リージョン情報を表示します。 jq形式の出力については、 [jq-formatted-json-output-usage](#jq-formatted-json-output-usage)を参照してください。

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

このコマンドを使用して、特定のキーが存在するリージョンを照会します。これは、raw、encoding、およびhex形式をサポートします。また、キーがエンコード形式の場合は、キーを一重引用符で囲む必要があります。

16進形式の使用法（デフォルト）：

```bash
>> region key 7480000000000000FF1300000000000000F8
{
  "region": {
    "id": 2,
    ......
  }
}
```

生のフォーマットの使用法：

```bash
>> region key --format=raw abc
{
  "region": {
    "id": 2,
    ......
  }
}
```

エンコーディング形式の使用法：

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

このコマンドを使用して、特定のリージョンの隣接するリージョンを確認します。

使用法：

```bash
>> region sibling 2
{
  "count": 2,
  "regions": [......],
}
```

### <code>region keys [--format=raw|encode|hex] &#x3C;start_key> &#x3C;end_key> &#x3C;limit></code> {#code-region-keys-format-raw-encode-hex-x3c-start-key-x3c-end-key-x3c-limit-code}

このコマンドを使用して、指定された範囲`[startkey, endkey)`のすべてのリージョンを照会します。 `endKey`秒のない範囲がサポートされています。

`limit`パラメーターは、キーの数を制限します。デフォルト値の`limit`は`16`で、値`-1`は無制限のキーを意味します。

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

このコマンドを使用して、読み取りフローが上位のリージョンを一覧表示します。制限のデフォルト値は16です。

使用法：

```bash
>> region topread
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topwrite [limit]</code> {#code-region-topwrite-limit-code}

このコマンドを使用して、書き込みフローが上位のリージョンを一覧表示します。制限のデフォルト値は16です。

使用法：

```bash
>> region topwrite
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topconfver [limit]</code> {#code-region-topconfver-limit-code}

このコマンドを使用して、上位confバージョンのリージョンを一覧表示します。制限のデフォルト値は16です。

使用法：

```bash
>> region topconfver
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topversion [limit]</code> {#code-region-topversion-limit-code}

このコマンドを使用して、最上位バージョンのリージョンを一覧表示します。制限のデフォルト値は16です。

使用法：

```bash
>> region topversion
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topsize [limit]</code> {#code-region-topsize-limit-code}

このコマンドを使用して、最上位のおおよそのサイズのリージョンを一覧表示します。制限のデフォルト値は16です。

使用法：

```bash
>> region topsize
{
  "count": 16,
  "regions": [......],
}

```

### <code>region check [miss-peer | extra-peer | down-peer | pending-peer | offline-peer | empty-region | hist-size | hist-keys]</code> {#code-region-check-miss-peer-extra-peer-down-peer-pending-peer-offline-peer-empty-region-hist-size-hist-keys-code}

このコマンドを使用して、異常な状態のリージョンを確認します。

さまざまなタイプの説明：

-   ミスピア：十分なレプリカがない地域
-   エクストラピア：追加のレプリカがある地域
-   ダウンピア：一部のレプリカがダウンしているリージョン
-   保留中のピア：一部のレプリカが保留中のリージョン

使用法：

```bash
>> region check miss-peer
{
  "count": 2,
  "regions": [......],
}
```

### <code>scheduler [show | add | remove | pause | resume | config]</code> {#code-scheduler-show-add-remove-pause-resume-config-code}

このコマンドを使用して、スケジューリングポリシーを表示および制御します。

使用法：

```bash
>> scheduler show                                 // Display all created schedulers
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

### <code>scheduler config balance-leader-scheduler</code> {#code-scheduler-config-balance-leader-scheduler-code}

このコマンドを使用して、 `balance-leader-scheduler`のポリシーを表示および制御します。

TiDB v6.0.0以降、PDは、バランスリーダーがタスクを処理する速度を制御するために`balance-leader-scheduler`に`Batch`パラメーターを導入しています。このパラメーターを使用するには、pd-ctlを使用して`balance-leader batch`の構成項目を変更できます。

v6.0.0より前では、PDにはこの構成項目がありません。これは`balance-leader batch=1`を意味します。 v6.0.0以降のバージョンでは、デフォルト値の`balance-leader batch`は`4`です。この構成項目を`4`より大きい値に設定するには、同時に[`scheduler-max-waiting-operator`](#config-show--set-option-value--placement-rules) （デフォルト値は`5` ）に大きい値を設定する必要があります。両方の構成アイテムを変更した後にのみ、期待される加速効果を得ることができます。

```bash
scheduler config balance-leader-scheduler set batch 3 // Set the size of the operator that the balance-leader scheduler can execute in a batch to 3
```

#### <code>scheduler config balance-hot-region-scheduler</code> {#code-scheduler-config-balance-hot-region-scheduler-code}

このコマンドを使用して、 `balance-hot-region-scheduler`のポリシーを表示および制御します。

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

-   `min-hot-byte-rate`は、カウントされる最小のバイト数を意味し、通常は100です。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-byte-rate 100
    ```

-   `min-hot-key-rate`は、カウントされるキーの最小数を意味し、通常は10です。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-key-rate 10
    ```

-   `min-hot-query-rate`は、カウントされるクエリの最小数を意味し、通常は10です。

    ```bash
    scheduler config balance-hot-region-scheduler set min-hot-query-rate 10
    ```

-   `max-zombie-rounds`は、オペレーターが保留中の影響と見なすことができるハートビートの最大数を意味します。これをより大きな値に設定すると、保留中の影響に含まれる演算子が増える可能性があります。通常、その値を調整する必要はありません。保留中の影響とは、スケジューリング中に生成されるが、それでも影響を与えるオペレーターの影響を指します。

    ```bash
    scheduler config balance-hot-region-scheduler set max-zombie-rounds 3
    ```

-   `max-peer-number`は、解決するピアの最大数を意味します。これにより、スケジューラーが遅くなりすぎるのを防ぎます。

    ```bash
    scheduler config balance-hot-region-scheduler set max-peer-number 1000
    ```

-   `byte-rate-rank-step-ratio` 、および`key-rate-rank-step-ratio`は`query-rate-rank-step-ratio` 、バイト、キー、クエリ、およびカウントのステップランクを意味し`count-rank-step-ratio` 。ランクステップ比は、ランクが計算されるときのステップを決定します。 `great-dec-ratio`と`minor-dec-ratio`は、 `dec`ランクを決定するために使用されます。通常、これらのアイテムを変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set byte-rate-rank-step-ratio 0.05
    ```

-   `src-tolerance-ratio`と`dst-tolerance-ratio`は、期待スケジューラの構成項目です。 `tolerance-ratio`が小さいほど、スケジューリングが容易になります。冗長なスケジューリングが発生した場合は、この値を適切に増やすことができます。

    ```bash
    scheduler config balance-hot-region-scheduler set src-tolerance-ratio 1.1
    ```

-   `read-priorities` 、および`write-leader-priorities`は、スケジューラがホットリージョンスケジューリングで優先するディメンションを制御し`write-peer-priorities` 。構成には2つの次元がサポートされています。

    -   `read-priorities`および`write-leader-priorities`は、読み取りおよび書き込みリーダータイプのホットリージョンをスケジュールするためにスケジューラーが優先するディメンションを制御します。寸法オプションは`query` 、および`byte` `key` 。

    -   `write-peer-priorities`は、書き込みピアタイプのホットリージョンをスケジュールするためにスケジューラが優先するディメンションを制御します。寸法オプションは`byte`と`key`です。

    > **ノート：**
    >
    > クラスタコンポーネントがv5.2より前の場合、 `query`次元の構成は有効になりません。一部のコンポーネントがv5.2以降にアップグレードされた場合でも、デフォルトでは`byte`次元と`key`次元がホットリージョンスケジューリングの優先順位を持ちます。クラスタのすべてのコンポーネントがv5.2以降にアップグレードされた後も、互換性のためにそのような構成が有効になります。 `pd-ctl`コマンドを使用して、リアルタイム構成を表示できます。通常、これらの構成を変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set read-priorities query,byte
    ```

-   `strict-picking-store`は、ホットリージョンスケジューリングの検索スペースを制御します。通常は有効になっています。有効にすると、ホットリージョンスケジューリングにより、構成された2つのディメンションでホットスポットのバランスが確保されます。無効にすると、ホットリージョンスケジューリングでは、最優先のディメンションのバランスのみが保証され、他のディメンションのバランスが低下する可能性があります。通常、この構成を変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set strict-picking-store true
    ```

-   `enable-for-tiflash`は、ホットリージョンスケジューリングをTiFlashインスタンスに対して有効にするかどうかを制御します。通常は有効になっています。無効にすると、TiFlashインスタンス間のホットリージョンスケジューリングは実行されません。

    ```bash
    scheduler config balance-hot-region-scheduler set enable-for-tiflash true
    ```

### <code>store [delete | cancel-delete | label | weight | remove-tombstone | limit ] &#x3C;store_id> [--jq="&#x3C;query string>"]</code> {#code-store-delete-cancel-delete-label-weight-remove-tombstone-limit-x3c-store-id-jq-x3c-query-string-code}

このコマンドを使用して、ストア情報を表示するか、指定したストアを削除します。 jq形式の出力については、 [jq-formatted-json-output-usage](#jq-formatted-json-output-usage)を参照してください。

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
>> store cancel-delete 1               // Cancel the delete operation previously performed on the store with the id of 1 which is in the offline state. After the cancellation, the store will enter the up state. Note that this command cannot make the tombstone store back to the up state. If the PD leader has been switched during the offline process, you need to manually modify the store limit.
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
> -   `store limit`コマンドの元の`region-add`および`region-remove`パラメーターは廃止され、 `add-peer`および`remove-peer`に置き換えられました。
> -   `pd-ctl`を使用して、TiKVストアのステータス（アップ、切断、オフライン、ダウン、またはトゥームストーン）を確認できます。各ステータスの関係については、 [TiKVストアの各ステータス間の関係](/tidb-scheduling.md#information-collection)を参照してください。

### <code>log [fatal | error | warn | info | debug]</code> {#code-log-fatal-error-warn-info-debug-code}

このコマンドを使用して、PDリーダーのログレベルを設定します。

使用法：

```bash
log warn
```

### <code>tso</code> {#code-tso-code}

このコマンドを使用して、TSOの物理的および論理的な時間を解析します。

使用法：

```bash
>> tso 395181938313123110        // Parse TSO
system:  2017-10-09 05:50:59 +0800 CST
logic:  120102
```

### <code>unsafe remove-failed-stores [store-ids | show]</code> {#code-unsafe-remove-failed-stores-store-ids-show-code}

> **警告：**
>
> -   この機能は不可逆リカバリであるため、TiKVは、この機能の使用後にデータの整合性とデータインデックスの整合性を保証できません。
> -   TiDBチームのサポートを受けて、機能関連の操作を実行することをお勧めします。誤操作が発生した場合、クラスタの復旧が困難になる場合があります。

このコマンドを使用して、永続的に損傷したレプリカが原因でデータが使用できなくなった場合に、損失の多いリカバリ操作を実行します。次の例を参照してください。詳細は[オンラインの安全でない回復](/online-unsafe-recovery.md)に記載されています

Online Unsafe Recoveryを実行して、恒久的に損傷したストアを削除します。

```bash
unsafe remove-failed-stores 101,102,103
```

```bash
Success!
```

オンラインの安全でないリカバリの現在または過去の状態を表示します。

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

## Jq形式のJSON出力の使用法 {#jq-formatted-json-output-usage}

### <code>store</code>の出力を簡素化する {#simplify-the-output-of-code-store-code}

```bash
>> store --jq=".stores[].store | { id, address, state_name}"
{"id":1,"address":"127.0.0.1:20161","state_name":"Up"}
{"id":30,"address":"127.0.0.1:20162","state_name":"Up"}
...
```

### ノードの残りのスペースを照会します {#query-the-remaining-space-of-the-node}

```bash
>> store --jq=".stores[] | {id: .store.id, available: .status.available}"
{"id":1,"available":"10 GiB"}
{"id":30,"available":"10 GiB"}
...
```

### ステータスが<code>Up</code>ではないすべてのノードをクエリします {#query-all-nodes-whose-status-is-not-code-up-code}

{{< copyable "" >}}

```bash
store --jq='.stores[].store | select(.state_name!="Up") | { id, address, state_name}'
```

```
{"id":1,"address":"127.0.0.1:20161""state_name":"Offline"}
{"id":5,"address":"127.0.0.1:20162""state_name":"Offline"}
...
```

### すべてのTiFlashノードをクエリします {#query-all-tiflash-nodes}

{{< copyable "" >}}

```bash
store --jq='.stores[].store | select(.labels | length>0 and contains([{"key":"engine","value":"tiflash"}])) | { id, address, state_name}'
```

```
{"id":1,"address":"127.0.0.1:20161""state_name":"Up"}
{"id":5,"address":"127.0.0.1:20162""state_name":"Up"}
...
```

### リージョンレプリカの配布ステータスを照会します {#query-the-distribution-status-of-the-region-replicas}

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id]}"
{"id":2,"peer_stores":[1,30,31]}
{"id":4,"peer_stores":[1,31,34]}
...
```

### レプリカの数に応じてリージョンをフィルタリングする {#filter-regions-according-to-the-number-of-replicas}

たとえば、レプリカの数が3ではないすべてのリージョンを除外するには。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length != 3)}"
{"id":12,"peer_stores":[30,32]}
{"id":2,"peer_stores":[1,30,31,32]}
```

### レプリカのストアIDに従ってリージョンをフィルタリングします {#filter-regions-according-to-the-store-id-of-replicas}

たとえば、store30にレプリカがあるすべてのリージョンを除外するには、次のようにします。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==30))}"
{"id":6,"peer_stores":[1,30,31]}
{"id":22,"peer_stores":[1,30,32]}
...
```

同様に、store30またはstore31にレプリカがあるすべてのリージョンを見つけることもできます。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(any(.==(30,31)))}"
{"id":16,"peer_stores":[1,30,34]}
{"id":28,"peer_stores":[1,30,32]}
{"id":12,"peer_stores":[30,32]}
...
```

### データを復元するときに関連するリージョンを探す {#look-for-relevant-regions-when-restoring-data}

たとえば、[store1、store30、store31]がダウンタイムで利用できない場合、ダウンレプリカが通常のレプリカよりも多いすべてのリージョンを見つけることができます。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length as $total | map(if .==(1,30,31) then . else empty end) | length>=$total-length) }"
{"id":2,"peer_stores":[1,30,31,32]}
{"id":12,"peer_stores":[30,32]}
{"id":14,"peer_stores":[1,30,32]}
...
```

または、[store1、store30、store31]の開始に失敗した場合、store1でデータを手動で安全に削除できるリージョンを見つけることができます。このようにして、store1にレプリカがあり、他のDownPeerがないすべてのリージョンを除外できます。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length>1 and any(.==1) and all(.!=(30,31)))}"
{"id":24,"peer_stores":[1,32,33]}
```

[store30、store31]がダウンしているときに、 `remove-peer`の演算子を作成することで安全に処理できるすべてのリージョン、つまり、唯一のDownPeerを持つリージョンを見つけます。

```bash
>> region --jq=".regions[] | {id: .id, remove_peer: [.peers[].store_id] | select(length>1) | map(if .==(30,31) then . else empty end) | select(length==1)}"
{"id":12,"remove_peer":[30]}
{"id":4,"remove_peer":[31]}
{"id":22,"remove_peer":[30]}
...
```
