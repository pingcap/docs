---
title: PD Control User Guide
summary: PD Controlを使用して、クラスターの状態情報を取得し、クラスターを調整します。
---

# PD Controlユーザー ガイド {#pd-control-user-guide}

PD のコマンドラインツールであるPD Control は、クラスターの状態情報を取得し、クラスターをチューニングします。

## PD Controlをインストールする {#install-pd-control}

> **注記：**
>
> 使用する制御ツールのバージョンは、クラスターのバージョンと一致させることをお勧めします。

### TiUPコマンドを使用する {#use-tiup-command}

PD Controlを使用するには、 `tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> [-i]`コマンドを実行します。

### インストールパッケージをダウンロードする {#download-the-installation-package}

最新バージョンの`pd-ctl`入手するには、TiDBサーバーインストール パッケージをダウンロードします。3 `pd-ctl` `ctl-{version}-linux-{arch}.tar.gz`パッケージに含まれています。

| インストールパッケージ                                                                                | OS    | アーキテクチャ | SHA256チェックサム                                                                             |
| :----------------------------------------------------------------------------------------- | :---- | :------ | :--------------------------------------------------------------------------------------- |
| `https://download.pingcap.com/tidb-community-server-{version}-linux-amd64.tar.gz` (pd-ctl) | リナックス | amd64   | `https://download.pingcap.com/tidb-community-server-{version}-linux-amd64.tar.gz.sha256` |
| `https://download.pingcap.com/tidb-community-server-{version}-linux-arm64.tar.gz` (pd-ctl) | リナックス | アーム64   | `https://download.pingcap.com/tidb-community-server-{version}-linux-arm64.tar.gz.sha256` |

> **注記：**
>
> リンク内の`{version}` TiDBのバージョン番号を示します。例えば、 `amd64`アーキテクチャの`v8.5.4`のダウンロードリンクは`https://download.pingcap.com/tidb-community-server-v8.5.4-linux-amd64.tar.gz`です。

### ソースコードからコンパイルする {#compile-from-source-code}

1.  [行く](https://golang.org/) Go モジュールが使用されるため、1.23 以降が必要です。
2.  [PDプロジェクト](https://github.com/pingcap/pd)のルート ディレクトリで、 `make`または`make pd-ctl`コマンドを使用して`bin/pd-ctl`コンパイルして生成します。

## 使用法 {#usage}

シングルコマンドモード:

```bash
tiup ctl:v<CLUSTER_VERSION> pd store -u http://127.0.0.1:2379
```

インタラクティブモード:

```bash
tiup ctl:v<CLUSTER_VERSION> pd -i -u http://127.0.0.1:2379
```

環境変数を使用します:

```bash
export PD_ADDR=http://127.0.0.1:2379
tiup ctl:v<CLUSTER_VERSION> pd
```

TLS を使用して暗号化します:

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u https://127.0.0.1:2379 --cacert="path/to/ca" --cert="path/to/cert" --key="path/to/key"
```

## コマンドラインフラグ {#command-line-flags}

### <code>--cacert</code> {#code-cacert-code}

-   信頼されたCAの証明書ファイルへのパスをPEM形式で指定します。
-   デフォルト： &quot;&quot;

### <code>--cert</code> {#code-cert-code}

-   PEM形式のSSL証明書へのパスを指定します
-   デフォルト： &quot;&quot;

### <code>--detach</code> / <code>-d</code> {#code-detach-code-code-d-code}

-   単一のコマンドラインモードを使用します（readline には入りません）
-   デフォルト: true

### <code>--help</code> / <code>-h</code> {#code-help-code-code-h-code}

-   ヘルプ情報を出力します
-   デフォルト: false

### <code>--interact</code> / <code>-i</code> {#code-interact-code-code-i-code}

-   対話モードを使用する（readlineに入る）
-   デフォルト: false

### <code>--key</code> {#code-key-code}

-   PEM形式のSSL証明書キーファイルへのパスを指定します。これは`--cert`で指定された証明書の秘密鍵です。
-   デフォルト： &quot;&quot;

### <code>--pd</code> / <code>-u</code> {#code-pd-code-code-u-code}

-   PDアドレスを指定します
-   デフォルトアドレス: `http://127.0.0.1:2379`
-   環境変数: `PD_ADDR`

### <code>--version</code> / <code>-V</code> {#code-version-code-code-v-code}

-   バージョン情報を出力して終了します
-   デフォルト: false

## 指示 {#command}

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
    "max-merge-region-keys": 540000,
    "max-merge-region-size": 54,
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
"8.5.4"
```

-   `max-snapshot-count`単一のストアが同時に受信または送信するスナップショットの最大数を制御します。スケジューラは、通常のアプリケーションリソースの消費を回避するために、この設定によって制限されます。レプリカの追加やバランシングの速度を向上させる必要がある場合は、この値を大きくしてください。

    ```bash
    config set max-snapshot-count 64  // Set the maximum number of snapshots to 64
    ```

-   `max-pending-peer-count`単一ストア内の保留中のピアの最大数を制御します。この設定により、一部のノードで最新のログがないリージョンが多数生成されるのを防ぐため、スケジューラは制限されます。レプリカの追加やバランシングの速度を向上させる必要がある場合は、この値を増やしてください。0 に設定すると、制限はありません。

    ```bash
    config set max-pending-peer-count 64  // Set the maximum number of pending peers to 64
    ```

-   `max-merge-region-size`リージョンマージのサイズ上限を制御します（単位は MiB）。2 `regionSize`指定値を超える場合、PD は隣接するリージョンとマージしません。0 に設定すると、リージョンマージが無効になります。

    ```bash
    config set max-merge-region-size 16 // Set the upper limit on the size of Region Merge to 16 MiB
    ```

-   `max-merge-region-keys`リージョンマージのキー数の上限を制御します。2 `regionKeyCount`指定された値を超える場合、PD は隣接するリージョンとマージしません。

    ```bash
    config set max-merge-region-keys 50000 // Set the upper limit on keyCount to 50000
    ```

-   `split-merge-interval`同じリージョンにおける`split`の操作と`merge`操作の間隔を制御します。つまり、新しく分割されたリージョンは一定期間内に統合されません。

    ```bash
    config set split-merge-interval 24h  // Set the interval between `split` and `merge` to one day
    ```

-   `enable-one-way-merge` 、PD がリージョン を次のリージョンとの結合のみを許可するかどうかを制御します。2 `false`設定すると、PD はリージョン を隣接する 2 つの Region との結合を許可します。

    ```bash
    config set enable-one-way-merge true  // Enables one-way merging.
    ```

-   `enable-cross-table-merge` 、テーブル間のリージョンのマージを有効にするために使用されます。2 `false`設定すると、PD は異なるテーブルのリージョンをマージしません。このオプションは、キータイプが「テーブル」の場合にのみ機能します。

    ```bash
    config set enable-cross-table-merge true  // Enable cross table merge.
    ```

-   `key-type` 、クラスターで使用されるキーエンコーディングの種類を指定します。サポートされているオプションは [&quot;table&quot;, &quot;raw&quot;, &quot;txn&quot;] で、デフォルト値は &quot;table&quot; です。

    -   クラスター内に TiDB インスタンスが存在しない場合は、 `key-type` 「raw」または「txn」になり、PD は`enable-cross-table-merge`設定に関係なくテーブル間でリージョンをマージできます。
    -   クラスター内にTiDBインスタンスが存在する場合、 `key-type` 「table」である必要があります。PDがテーブル間でリージョンをマージできるかどうかは、 `enable-cross-table-merge`によって決まります。5 `key-type` 「raw」の場合、配置ルールは機能しません。

    ```bash
    config set key-type raw  // Enable cross table merge.
    ```

-   `region-score-formula-version`リージョン計算式のバージョンを制御します。値の選択肢は`v1`と`v2`です。計算式のバージョン 2 は、TiKV ノードをオンラインまたはオフラインにするなど、一部のシナリオにおいて、リージョンの冗長なリージョンスケジューリングを削減するのに役立ちます。

    ```bash
    config set region-score-formula-version v2
    ```

-   `patrol-region-interval` 、チェッカーがリージョンのヘルスステータスを検査する実行頻度を制御します。間隔が短いほど、実行頻度が高くなります。通常、調整する必要はありません。

    ```bash
    config set patrol-region-interval 10ms // Set the execution frequency of the checker to 10ms
    ```

-   `patrol-region-worker-count` 、リージョンのヘルス状態を検査する際にチェッカーによって作成される同時実行数[オペレーター](/glossary.md#operator)を制御します。通常、この設定を調整する必要はありません。この設定項目を 1 より大きい値に設定すると、同時実行チェックが有効になります。現在、この機能は実験的であり、本番環境での使用は推奨されません。

    ```bash
    config set patrol-region-worker-count 2 // Set the checker concurrency to 2
    ```

-   `max-store-down-time` 、PD が切断されたストアを復元できないと判断するまでの時間を制御します。指定された時間内に PD がストアからハートビートを受信しない場合、PD は他のノードにレプリカを追加します。

    ```bash
    config set max-store-down-time 30m  // Set the time within which PD receives no heartbeats and after which PD starts to add replicas to 30 minutes
    ```

-   `max-store-preparing-time`ストアがオンラインになるまでの最大待機時間を制御します。ストアがオンライン状態の間、PD はストアのオンライン進行状況を照会できます。指定された時間を超えると、PD はストアがオンライン状態になったとみなし、再度ストアのオンライン進行状況を照会できなくなります。ただし、これによってリージョンが新しいオンラインストアに移行するのが妨げられることはありません。ほとんどのシナリオでは、このパラメータを調整する必要はありません。

    次のコマンドは、ストアがオンラインになるまでの最大待機時間が 4 時間であることを指定します。

    ```bash
    config set max-store-preparing-time 4h
    ```

-   `leader-schedule-limit`リーダータスクを同時にスケジュールするタスクの数を制御します。この値はリーダータスクのバランス調整の速度に影響します。値が大きいほど速度が速くなり、値を0に設定するとスケジューリングが閉じられます。通常、リーダータスクのスケジューリングの負荷は小さいため、必要に応じて値を増やすことができます。

    ```bash
    config set leader-schedule-limit 4         // 4 tasks of leader scheduling at the same time at most
    ```

-   `region-schedule-limit` 、同時にリージョンをスケジュールするタスクの数を制御します。この値を設定すると、リージョンバランスオペレータが過剰に作成されるのを回避できます。デフォルト値は`2048`で、あらゆるサイズのクラスターに十分な値です。値を`0`に設定すると、スケジューリングが制限されます。通常、リージョンのスケジューリング速度は`store-limit`に制限されますが、何をしようとしているのかを正確に理解していない限り、この値をカスタマイズしないことをお勧めします。

    ```bash
    config set region-schedule-limit 2         // 2 tasks of Region scheduling at the same time at most
    ```

-   `replica-schedule-limit` 、レプリカを同時にスケジュールするタスクの数を制御します。この値は、ノードがダウンまたは削除された場合のスケジュール速度に影響します。値が大きいほど速度が速くなり、値を 0 に設定するとスケジュールが停止します。通常、レプリカのスケジュールは大きな負荷がかかるため、あまり大きな値を設定しないでください。この設定項目は通常、デフォルト値のままです。値を変更する場合は、実際の状況に応じて最適な値を見つけるために、いくつかの値を試す必要があります。

    ```bash
    config set replica-schedule-limit 4        // 4 tasks of replica scheduling at the same time at most
    ```

-   `merge-schedule-limit`リージョンマージのスケジュールタスクの数を制御します。値を 0 に設定すると、リージョンマージは終了します。通常、マージスケジュールは負荷が大きいため、あまり大きな値を設定しないでください。この設定項目は通常、デフォルト値のままです。値を変更する場合は、いくつかの値を試してみて、実際の状況に最適な値を見つける必要があります。

    ```bash
    config set merge-schedule-limit 16       // 16 tasks of Merge scheduling at the same time at most
    ```

-   `hot-region-schedule-limit` 、同時に実行されているホットなリージョンスケジューリングタスクを制御します。値を`0`に設定すると、スケジューリングが無効になります。あまり大きな値を設定することはお勧めしません。システムパフォーマンスに影響を与える可能性があります。この設定項目は通常、デフォルト値のままです。値を変更する場合は、実際の状況に応じて最適な値を見つけるために、いくつかの値を試す必要があります。

    ```bash
    config set hot-region-schedule-limit 4       // 4 tasks of hot Region scheduling at the same time at most
    ```

-   `hot-region-cache-hits-threshold` 、ホットリージョンを識別するために必要な分数を設定するために使用されます。PD は、リージョンがこの分数を超えてホットスポット状態になった後にのみ、ホットスポット スケジューリングに参加できます。

-   `tolerant-size-ratio`バランスバッファ領域のサイズを制御します。2つの店舗のリーダーまたはリージョン間のスコア差が、指定されたリージョンサイズの倍数未満の場合、PDはバランスが取れているとみなします。

    ```bash
    config set tolerant-size-ratio 20        // Set the size of the buffer area to about 20 times of the average Region Size
    ```

-   `low-space-ratio` 、ストアスペース不足とみなされるしきい値を制御します。ノードが占有するスペースの割合が指定値を超えると、PDは対応するノードへのデータの移行を可能な限り回避しようとします。同時に、PDは対応するノードのディスクスペースを使い果たさないように、残りのスペースを主にスケジュールします。

    ```bash
    config set low-space-ratio 0.9              // Set the threshold value of insufficient space to 0.9
    ```

-   `high-space-ratio`十分なストアスペースとみなされるしきい値を制御します。この設定は、 `region-score-formula-version` `v1`に設定した場合にのみ有効になります。ノードが占有するスペースの割合が指定値を下回る場合、PDは残りのスペースを無視し、主に実際のデータ量に基づいてスケジュールします。

    ```bash
    config set high-space-ratio 0.5             // Set the threshold value of sufficient space to 0.5
    ```

-   `cluster-version`はクラスターのバージョンで、一部の機能を有効化または無効化したり、互換性の問題に対処したりするために使用されます。デフォルトでは、クラスター内で正常に動作しているすべての TiKV ノードの最小バージョンです。以前のバージョンにロールバックする必要がある場合にのみ、手動で設定できます。

    ```bash
    config set cluster-version 8.5.4             // Set the version of the cluster to 8.5.4
    ```

-   `replication-mode`デュアルデータセンターシナリオにおけるリージョンのレプリケーションモードを制御します。詳細は[DR自動同期モードを有効にする](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)参照してください。

-   `leader-schedule-policy`はリーダーのスケジューリング戦略を選択するために使用されます。2 または`size`に従ってリーダー`count`スケジュールできます。

-   `scheduler-max-waiting-operator`は、各スケジューラ内の待機オペレータの数を制御するために使用されます。

-   `enable-remove-down-replica`は`false`ダウンタイムレプリカの自動削除機能を有効にするために使用されます。2 に設定すると、PDはダウンタイムレプリカを自動的にクリーンアップしません。

-   `enable-replace-offline-replica`は、OfflineReplica の移行機能を有効にするために使用されます。2 `false`設定すると、PD はオフラインレプリカを移行しません。

-   `enable-make-up-replica`はレプリカ作成機能を有効にするために使用されます。 `false`に設定すると、PDはレプリカが不足しているリージョンに対してレプリカを追加しません。

-   `enable-remove-extra-replica` 、余分なレプリカを削除する機能を有効にするために使用されます。2 `false`設定すると、PDは冗長レプリカを持つリージョンの余分なレプリカを削除しません。

-   `enable-location-replacement`は分離レベルチェックを有効にするために使用されます。 `false`に設定すると、PDはスケジュール設定によってリージョンレプリカの分離レベルを上げません。

-   `enable-debug-metrics`はデバッグ用のメトリクスを有効にするために使用されます。 `true`に設定すると、PDは`balance-tolerant-size`などの一部のメトリクスを有効にします。

-   `enable-placement-rules`は配置ルールを有効にするために使用され、v5.0 以降のバージョンではデフォルトで有効になっています。

-   `store-limit-mode`はストア速度を制限するモードを制御するために使用されます。オプションのモードは`auto`と`manual`です。6 `auto`では、ストアは負荷に応じて自動的にバランス調整されます（非推奨）。

-   `store-limit-version`ストア制限の計算式のバージョンを制御します。v1 モードでは、 `store limit`を手動で変更することで、単一の TiKV のスケジュール速度を制限できます。v2 モードでは、PD が TiKV スナップショットの機能に基づいて 4 の値を動的に調整するため、 `store limit`値を手動で設定する必要はありません。詳細については、 [店舗制限の原則 v2](/configure-store-limit.md#principles-of-store-limit-v2)を参照してください。

    ```bash
    config set store-limit-version v2       // using store limit v2
    ```

-   PDはフロー番号の最下位桁を丸めることで、リージョンフロー情報の変更に伴う統計情報の更新を削減します。この設定項目は、リージョンフロー情報の最小桁数を指定します。例えば、フロー`100512`はデフォルト値が`3`であるため、 `101000`に丸められます。この設定は`trace-region-flow`置き換えます。

-   たとえば、 `flow-round-by-digit`の値を`4`に設定します。

    ```bash
    config set flow-round-by-digit 4
    ```

### <code>config [show | set service-middleware &#x3C;option> [&#x3C;key> &#x3C;value> | &#x3C;label> &#x3C;qps|concurrency> &#x3C;value>]]</code> {#code-config-show-set-service-middleware-x3c-option-x3c-key-x3c-value-x3c-label-x3c-qps-concurrency-x3c-value-code}

`service-middleware`はPDの設定モジュールであり、主にPDサービスのミドルウェア関数（監査ログ、リクエストレート制限、同時実行制限など）の管理と制御に使用されます。v8.5.0以降では、 `pd-ctl`を使用して`service-middleware`の以下の設定を変更できます。

-   `audit` : PD によって処理される HTTP リクエストの監査ログを有効にするかどうかを制御します（デフォルトで有効）。有効にすると、 `service-middleware` HTTP リクエストに関する情報を PD ログに記録します。
-   `rate-limit` : PD によって処理される HTTP API リクエストの最大レートと同時実行性を制限します。
-   `grpc-rate-limit` : PD によって処理される gRPC API リクエストの最大レートと同時実行性を制限します。

> **注記：**
>
> リクエスト レート制限と同時実行制限が PD パフォーマンスに与える影響を回避するために、 `service-middleware`の設定を変更することはお勧めしません。

`service-middleware`の構成情報を表示します:

```bash
config show service-middleware
```

```bash
{
  "audit": {
    "enable-audit": "true"
  },
  "rate-limit": {
    "enable-rate-limit": "true",
    "limiter-config": {}
  },
  "grpc-rate-limit": {
    "enable-grpc-rate-limit": "true",
    "grpc-limiter-config": {}
  }
}
```

`service-middleware audit` 、HTTP リクエストの監査ログ機能を有効または無効にします。例えば、この機能を無効にするには、次のコマンドを実行します。

```bash
config set service-middleware audit enable-audit false
```

`service-middleware grpc-rate-limit`次の gRPC API リクエストの最大レートと同時実行性を制御します。

-   `GetRegion` : 指定されたリージョンに関する情報を取得する
-   `GetStore` : 指定された店舗の情報を取得する
-   `GetMembers` : PDクラスタメンバーに関する情報を取得する

gRPC API リクエストの最大レート（ `GetRegion` API リクエストなど）を制御するには、次のコマンドを実行します。

```bash
config set service-middleware grpc-rate-limit GetRegion qps 100
```

gRPC API リクエストの最大同時実行数（ `GetRegion` API リクエストなど）を制御するには、次のコマンドを実行します。

```bash
config set service-middleware grpc-rate-limit GetRegion concurrency 10
```

変更された構成をビュー。

```bash
config show service-middleware
```

```bash
{
  "audit": {
    "enable-audit": "true"
  },
  "rate-limit": {
    "enable-rate-limit": "true",
    "limiter-config": {}
  },
  "grpc-rate-limit": {
    "enable-grpc-rate-limit": "true",
    "grpc-limiter-config": {
      "GetRegion": {
        "QPS": 100,
        "QPSBurst": 100, // Automatically adjusted based on QPS, for display only
        "ConcurrencyLimit": 10
      }
    }
  }
}
```

上記の設定をリセットします。

```bash
config set service-middleware grpc-rate-limit GetRegion qps 0
config set service-middleware grpc-rate-limit GetRegion concurrency 0
```

`service-middleware rate-limit` 、次の HTTP API 要求の最大レートと同時実行性を制御します。

-   `GetRegion` : 指定されたリージョンに関する情報を取得する
-   `GetStore` : 指定された店舗の情報を取得する

`GetRegion` API リクエストなどの HTTP API リクエストの最大レートを制御するには、次のコマンドを実行します。

```bash
config set service-middleware rate-limit GetRegion qps 100
```

`GetRegion` API リクエストなど、HTTP API リクエストの最大同時実行数を制御するには、次のコマンドを実行します。

```bash
config set service-middleware rate-limit GetRegion concurrency 10
```

上記の設定をリセットします。

```bash
config set service-middleware rate-limit GetRegion qps 0
config set service-middleware rate-limit GetRegion concurrency 0
```

### <code>config placement-rules [disable | enable | load | save | show | rule-group]</code> {#code-config-placement-rules-disable-enable-load-save-show-rule-group-code}

`config placement-rules [disable | enable | load | save | show | rule-group]`の使い方については[配置ルールを構成する](/configure-placement-rules.md#configure-rules)参照してください。

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

> **注記：**
>
> 本番環境では、 `member delete`コマンドを使用して PD ノードを削除**しないでください**。PD ノードを削除するには、 [TiDB/PD/TiKV クラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tidbpdtikv-cluster)と[Kubernetes 上で TiDB を手動でスケールする](https://docs.pingcap.com/tidb-in-kubernetes/stable/scale-a-tidb-cluster/)参照してください。

このコマンドを使用して、PD メンバーを表示したり、指定されたメンバーを削除したり、リーダーの優先度を設定したりします。

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
>> member delete id 1319539429105371180 // Delete a node using ID
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

PDリーダーの優先度を指定します:

```bash
member leader_priority  pd-1 4
member leader_priority  pd-2 3
member leader_priority  pd-3 2
member leader_priority  pd-4 1
member leader_priority  pd-5 0
```

> **注記：**
>
> 利用可能なすべての PD ノードの中で、優先順位番号が最も高いノードがリーダーになります。

### <code>operator [check | show | add | remove]</code> {#code-operator-check-show-add-remove-code}

このコマンドを使用して、スケジュール操作を表示および制御します。

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

リージョンの分割は、可能な限り中央に近い位置から開始されます。この位置を特定するには、「スキャン」と「近似」という2つの戦略があります。これらの違いは、前者はリージョンをスキャンして中央のキーを決定するのに対し、後者はSSTファイルに記録された統計情報をチェックすることでおおよその位置を取得することです。一般的に、前者の方が精度が高く、後者はI/Oの消費量が少なく、処理が高速です。

### <code>ping</code> {#code-ping-code}

このコマンドを使用して、 `ping` PD にかかる時間を表示します。

使用法：

```bash
>> ping
time: 43.12698ms
```

### <code>region &#x3C;region_id> [--jq="&#x3C;query string>"]</code> {#code-region-x3c-region-id-jq-x3c-query-string-code}

このコマンドを使用してリージョン情報を表示します。jq形式の出力については、 [jq形式のjson出力の使用法](#jq-formatted-json-output-usage)参照してください。

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

このコマンドを使用して、特定のキーが存在するリージョンを照会します。raw形式、エンコード形式、および16進形式をサポートしています。エンコード形式の場合は、キーを一重引用符で囲む必要があります。

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

生の形式の使用法:

```bash
>> region key --format=raw abc
{
  "region": {
    "id": 2,
    ......
  }
}
```

エンコード形式の使用:

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

すべてのリージョンを取得するには、このコマンドを使用します。

使用法：

```bash
>> region scan
{
  "count": 20,
  "regions": [......],
}
```

### <code>region sibling &#x3C;region_id></code> {#code-region-sibling-x3c-region-id-code}

このコマンドを使用して、特定のリージョンに隣接するリージョンを確認します。

使用法：

```bash
>> region sibling 2
{
  "count": 2,
  "regions": [......],
}
```

### <code>region keys [--format=raw|encode|hex] &#x3C;start_key> &#x3C;end_key> &#x3C;limit></code> {#code-region-keys-format-raw-encode-hex-x3c-start-key-x3c-end-key-x3c-limit-code}

このコマンドを使用して、指定された範囲`[startkey, endkey)`内のすべてのリージョンを照会します。 `endKey`のない範囲もサポートされています。

パラメータ`limit`はキーの数を制限します。デフォルト値は`limit`で`16` 、値`-1`はキーの数を無制限にすることを意味します。

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

このコマンドを使用して、読み取りフローが最も大きいリージョンを一覧表示します。制限のデフォルト値は`16`です。

使用法：

```bash
>> region topread
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topwrite [limit]</code> {#code-region-topwrite-limit-code}

このコマンドを使用して、書き込みフローが最も大きいリージョンを一覧表示します。制限のデフォルト値は`16`です。

使用法：

```bash
>> region topwrite
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topconfver [limit]</code> {#code-region-topconfver-limit-code}

このコマンドを使用して、最も高い conf バージョンを持つリージョンを一覧表示します。制限のデフォルト値は`16`です。

使用法：

```bash
>> region topconfver
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topversion [limit]</code> {#code-region-topversion-limit-code}

このコマンドを使用して、最上位バージョンのリージョンを一覧表示します。制限のデフォルト値は`16`です。

使用法：

```bash
>> region topversion
{
  "count": 16,
  "regions": [......],
}
```

### <code>region topsize [limit]</code> {#code-region-topsize-limit-code}

このコマンドを使用して、おおよそのサイズを持つリージョンを一覧表示します。制限のデフォルト値は`16`です。

使用法：

```bash
>> region topsize
{
  "count": 16,
  "regions": [......],
}

```

### <code>region check [miss-peer | extra-peer | down-peer | pending-peer | offline-peer | empty-region | hist-size | hist-keys] [--jq="&#x3C;query string>"]</code> {#code-region-check-miss-peer-extra-peer-down-peer-pending-peer-offline-peer-empty-region-hist-size-hist-keys-jq-x3c-query-string-code}

このコマンドを使用して、異常状態にある領域を確認します。jq形式の出力については、 [jq形式のJSON出力の使用法](#jq-formatted-json-output-usage)参照してください。

各種タイプの説明:

-   ミスピア: 十分なレプリカがないリージョン
-   extra-peer: 追加のレプリカを持つリージョン
-   ダウンピア: 一部のレプリカがダウンしているリージョン
-   pending-peer: レプリカが保留中のリージョン

使用法：

```bash
>> region check miss-peer
{
  "count": 2,
  "regions": [......],
}
```

### <code>resource-manager [command]</code> {#code-resource-manager-command-code}

#### リソース制御のコントローラ構成をビュー {#view-the-controller-configuration-of-resource-control}

```bash
resource-manager config controller show
```

```bash
{
    "degraded-mode-wait-duration": "0s",
    "ltb-max-wait-duration": "30s",
    "request-unit": {                    # Configurations of RU. Do not modify.
        "read-base-cost": 0.125,
        "read-per-batch-base-cost": 0.5,
        "read-cost-per-byte": 0.0000152587890625,
        "write-base-cost": 1,
        "write-per-batch-base-cost": 1,
        "write-cost-per-byte": 0.0009765625,
        "read-cpu-ms-cost": 0.3333333333333333
    },
    "enable-controller-trace-log": "false"
}
```

-   `ltb-max-wait-duration` : ローカルトークンバケット (LTB) の最大待機時間。デフォルト値は`30s`で、値の範囲は`[0, 24h]`です。SQL リクエストの推定消費量[リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) LTB の現在の累積 RU を超える場合、リクエストは一定時間待機する必要があります。推定待機時間がこの最大値を超えると、事前にアプリケーションにエラーメッセージ[`ERROR 8252 (HY000) : Exceeded resource group quota limitation`](/error-codes.md)が返されます。この値を増やすと、同時実行数の急増、大規模なトランザクション、大規模なクエリが発生した場合に`ERROR 8252`発生する可能性が低くなります。
-   `enable-controller-trace-log` : コントローラー診断ログを有効にするかどうかを制御します。

#### リソース制御のコントローラー構成を変更する {#modify-the-controller-configuration-of-resource-control}

`ltb-max-wait-duration`設定を変更するには、次のコマンドを使用します。

```bash
pd-ctl resource-manager config controller set ltb-max-wait-duration 30m
```

### <code>scheduler [show | add | remove | pause | resume | config | describe]</code> {#code-scheduler-show-add-remove-pause-resume-config-describe-code}

このコマンドを使用して、スケジュール ポリシーを表示および制御します。

使用法：

```bash
>> scheduler show                                          // Display all created schedulers
>> scheduler add grant-leader-scheduler 1                  // Schedule all the leaders of the Regions on store 1 to store 1
>> scheduler add evict-leader-scheduler 1                  // Move all the Region leaders on store 1 out
>> scheduler config evict-leader-scheduler                 // Display the stores in which the scheduler is located since v4.0.0
>> scheduler config evict-leader-scheduler add-store 2     // Add leader eviction scheduling for store 2
>> scheduler config evict-leader-scheduler delete-store 2  // Remove leader eviction scheduling for store 2
>> scheduler add evict-slow-store-scheduler                // When there is one and only one slow store, evict all Region leaders of that store
>> scheduler remove grant-leader-scheduler-1               // Remove the corresponding scheduler, and `-1` corresponds to the store ID
>> scheduler pause balance-region-scheduler 10             // Pause the balance-region scheduler for 10 seconds
>> scheduler pause all 10                                  // Pause all schedulers for 10 seconds
>> scheduler resume balance-region-scheduler               // Continue to run the balance-region scheduler
>> scheduler resume all                                    // Continue to run all schedulers
>> scheduler config balance-hot-region-scheduler           // Display the configuration of the balance-hot-region scheduler
>> scheduler describe balance-region-scheduler             // Display the running state and related diagnostic information of the balance-region scheduler
```

### <code>scheduler describe balance-region-scheduler</code> {#code-scheduler-describe-balance-region-scheduler-code}

このコマンドを使用して、 `balance-region-scheduler`の実行状態と関連する診断情報を表示します。

TiDB v6.3.0以降、PDは`balance-region-scheduler`と`balance-leader-scheduler`の実行状態と簡単な診断情報を提供します。他のスケジューラとチェッカーはまだサポートされていません。この機能を有効にするには、 `pd-ctl`を使用して[`enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-new-in-v630)設定項目を変更します。

スケジューラの状態は次のいずれかになります。

-   `disabled` : スケジューラは使用できないか削除されています。
-   `paused` : スケジューラは一時停止されています。
-   `scheduling` : スケジューラはスケジューリング演算子を生成しています。
-   `pending` : スケジューラはスケジューリング演算子を生成できません。状態`pending`のスケジューラには、簡単な診断情報が返されます。この簡単な情報は、ストアの状態と、これらのストアをスケジューリング対象として選択できない理由を説明します。
-   `normal` : スケジューリング演算子を生成する必要はありません。

### <code>scheduler config balance-leader-scheduler</code> {#code-scheduler-config-balance-leader-scheduler-code}

このコマンドを使用して、 `balance-leader-scheduler`ポリシーを表示および制御します。

TiDB v6.0.0以降、PDはバランスリーダーがタスクを処理する速度を制御するためのパラメータ`Batch` （ `balance-leader-scheduler`を導入しました。このパラメータを使用するには、pd-ctlを使用して設定項目`balance-leader batch`を変更します。

v6.0.0より前のPDにはこの設定項目がないため、 `balance-leader batch=1`なります。v6.0.0以降のバージョンでは、 `balance-leader batch`のデフォルト値は`4`です。この設定項目を`4`より大きい値に設定するには、同時に[`scheduler-max-waiting-operator`](#config-show--set-option-value--placement-rules) （デフォルト値は`5` ）にもより大きな値を設定する必要があります。両方の設定項目を変更することで、期待される高速化効果が得られます。

```bash
scheduler config balance-leader-scheduler set batch 3 // Set the size of the operator that the balance-leader scheduler can execute in a batch to 3
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
  "enable-for-tiflash": "true",
  "rank-formula-version": "v2"
}
```

-   `min-hot-byte-rate`カウントされる最小バイト数を意味し、通常は 100 です。

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

-   `max-zombie-rounds`オペレータが保留中の影響力を持つと見なされるハートビートの最大数を意味します。より大きな値に設定すると、より多くのオペレータが保留中の影響力に含まれる可能性があります。通常、この値を調整する必要はありません。保留中の影響力とは、スケジューリング中に生成されるものの、依然として効果を持つオペレータの影響力を指します。

    ```bash
    scheduler config balance-hot-region-scheduler set max-zombie-rounds 3
    ```

-   `max-peer-number`は解決するピアの最大数を意味し、これによりスケジューラが遅くなりすぎるのを防ぎます。

    ```bash
    scheduler config balance-hot-region-scheduler set max-peer-number 1000
    ```

-   `byte-rate-rank-step-ratio` 、 `key-rate-rank-step-ratio` 、 `query-rate-rank-step-ratio` 、 `count-rank-step-ratio`はそれぞれ、バイト、キー、クエリ、カウントのステップランクを表します。rank-step-ratio は、ランクを計算する際のステップを決定します。8 と`minor-dec-ratio` `great-dec-ratio` `dec`ランクを決定するために使用されます。通常、これらの項目を変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set byte-rate-rank-step-ratio 0.05
    ```

-   `src-tolerance-ratio`と`dst-tolerance-ratio`期待値スケジューラの設定項目です。4 `tolerance-ratio`小さいほど、スケジューリングが容易になります。冗長なスケジューリングが発生する場合は、この値を適切に増やしてください。

    ```bash
    scheduler config balance-hot-region-scheduler set src-tolerance-ratio 1.1
    ```

-   `read-priorities` 、 `write-leader-priorities` 、 `write-peer-priorities` 、ホットリージョンスケジューリングにおいてスケジューラがどのディメンションを優先するかを制御します。設定では2つのディメンションがサポートされています。

    -   `read-priorities`と`write-leader-priorities` 、読み取りリーダー型および書き込みリーダー型のホット領域をスケジューリングする際に、スケジューラがどの次元を優先するかを制御します。次元のオプションは`query` 、 `byte` 、 `key`です。

    -   `write-peer-priorities` 、書き込みピアタイプのホットリージョンのスケジュールにおいて、スケジューラがどのディメンションを優先するかを制御します。ディメンションのオプションは`byte`と`key`です。

    > **注記：**
    >
    > クラスタコンポーネントがv5.2より前のバージョンの場合、 `query`次元の設定は有効になりません。一部のコンポーネントをv5.2以降にアップグレードした場合でも、 `byte`と`key`次元はデフォルトでホットリージョンスケジューリングの優先権を持ちます。クラスタのすべてのコンポーネントをv5.2以降にアップグレードした後も、互換性のためにこれらの設定は有効になります。7 `pd-ctl`を使用してリアルタイム設定を表示できます。通常、これらの設定を変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set read-priorities query,byte
    ```

-   `strict-picking-store`ホットリージョンスケジューリングの検索空間を制御します。通常は有効になっています。この設定項目は、 `rank-formula-version`が`v1`場合のみ動作に影響します。有効にすると、ホットリージョンスケジューリングは設定された2つのディメンションのホットリージョンバランスを確保します。無効にすると、ホットリージョンスケジューリングは優先度が最も高いディメンションのバランスのみを確保するため、他のディメンションのバランスが低下する可能性があります。通常、この設定を変更する必要はありません。

    ```bash
    scheduler config balance-hot-region-scheduler set strict-picking-store true
    ```

-   `rank-formula-version`ホットリージョンスケジューリングで使用するスケジューラアルゴリズムのバージョンを制御します。値の選択肢は`v1`と`v2`です。デフォルト値は`v2`です。

    -   `v1`アルゴリズムは、TiDB v6.3.0以前のバージョンで使用されていたスケジューラ戦略です。このアルゴリズムは、主にストア間の負荷差を軽減することに重点を置いており、他のディメンションへの副作用の発生を回避します。
    -   `v2`アルゴリズムは、TiDB v6.3.0 で導入された実験的スケジューラ戦略であり、TiDB v6.4.0 で一般提供（GA）されました。このアルゴリズムは、副作用を少なくしながら、ストアとファクタ間の公平性を向上させることに主眼を置いています。5 が`strict-picking-store` `true`ある`v1`アルゴリズムと比較すると、 `v2`アルゴリズムは第 1 次元の優先度均等化により重点を置いています。13 が`strict-picking-store` `false`ある`v1`アルゴリズムと比較すると、 `v2`アルゴリズムは第 2 次元のバランスを考慮しています。
    -   `strict-picking-store`を`true`とする`v1`アルゴリズムは保守的であり、両次元に高負荷のストアがある場合にのみスケジューリングが生成されます。特定のシナリオでは、次元の競合によりバランス調整を継続できなくなる可能性があります。第 1 次元でより適切なバランス調整を実現するには、 `strict-picking-store`を`false`に設定する必要があります。11 アルゴリズムは`v2`両次元でより適切なバランス調整を実現し、無効なスケジューリングを削減します。

    ```bash
    scheduler config balance-hot-region-scheduler set rank-formula-version v2
    ```

-   `enable-for-tiflash` 、 TiFlashインスタンス間のホットリージョンスケジューリングを有効にするかどうかを制御します。通常は有効です。無効にすると、 TiFlashインスタンス間のホットリージョンスケジューリングは実行されません。

    ```bash
    scheduler config balance-hot-region-scheduler set enable-for-tiflash true
    ```

### <code>scheduler config evict-leader-scheduler</code> {#code-scheduler-config-evict-leader-scheduler-code}

このコマンドを使用して、 `evict-leader-scheduler`の構成を表示および管理します。

-   `evict-leader-scheduler`がすでに存在する場合は、 `add-store`サブコマンドを使用して、指定されたストアのリーダー削除スケジュールを追加します。

    ```bash
    scheduler config evict-leader-scheduler add-store 2       // Add leader eviction scheduling for store 2
    ```

-   `evict-leader-scheduler`がすでに存在する場合は、 `delete-store`サブコマンドを使用して、指定されたストアのリーダー削除スケジュールを削除します。

    ```bash
    scheduler config evict-leader-scheduler delete-store 2    // Remove leader eviction scheduling for store 2
    ```

    `evict-leader-scheduler`のすべてのストア構成が削除されると、スケジューラ自体も自動的に削除されます。

-   `evict-leader-scheduler`が既に存在する場合は、 `set batch`サブコマンドを使用して`batch`値を変更します。 `batch`単一のスケジューリングプロセスで生成されるオペレータの数を制御します。デフォルト値は`3`で、範囲は`[1, 10]`です。 `batch`値が大きいほど、スケジューリング速度が速くなります。

    ```bash
    scheduler config evict-leader-scheduler set batch 10 // Set the batch value to 10
    ```

### <code>service-gc-safepoint</code> {#code-service-gc-safepoint-code}

このコマンドを使用して、現在のGCセーフポイントとサービスGCセーフポイントを照会します。出力は次のとおりです。

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

### <code>store [delete | cancel-delete | label | weight | remove-tombstone | limit ] &#x3C;store_id> [--jq="&#x3C;query string>"]</code> {#code-store-delete-cancel-delete-label-weight-remove-tombstone-limit-x3c-store-id-jq-x3c-query-string-code}

jq 形式の出力については、 [jq形式のjson出力の使用法](#jq-formatted-json-output-usage)参照してください。

#### ストアを取得する {#get-a-store}

すべてのストアの情報を表示するには、次のコマンドを実行します。

```bash
store
```

    {
      "count": 3,
      "stores": [...]
    }

ID が 1 のストアを取得するには、次のコマンドを実行します。

```bash
store 1
```

    ......

#### ストアを削除する {#delete-a-store}

ID が 1 のストアを削除するには、次のコマンドを実行します。

```bash
store delete 1
```

`store delete`で削除された`Offline`状態のストアの削除をキャンセルするには、 `store cancel-delete`コマンドを実行します。キャンセル後、ストアは`Offline`から`Up`に変わります。 `store cancel-delete`コマンドでは`Tombstone`状態のストアを`Up`状態に変更できないことに注意してください。

ID が 1 のストアの削除をキャンセルするには、次のコマンドを実行します。

```bash
store cancel-delete 1
```

`Tombstone`状態にあるすべてのストアを削除するには、次のコマンドを実行します。

```bash
store remove-tombstone
```

> **注記：**
>
> ストアの削除中に PD リーダーが変更された場合は、 [`store limit`](#configure-store-scheduling-speed)コマンドを使用してストア制限を手動で変更する必要があります。

#### ストアラベルを管理する {#manage-store-labels}

ストアのラベルを管理するには、 `store label`コマンドを実行します。

-   ID が 1 のストアにキーが`"zone"` 、値が`"cn"`ラベルを設定するには、次のコマンドを実行します。

    ```bash
    store label 1 zone=cn
    ```

-   ストアのラベルを更新するには、たとえば、ID が 1 のストアのキー`"zone"`の値を`"cn"`から`"us"`に変更するには、次のコマンドを実行します。

    ```bash
    store label 1 zone=us
    ```

-   ID が 1 のストアのすべてのラベルを書き換えるには、 `--rewrite`オプションを使用します。このオプションは既存のラベルをすべて上書きすることに注意してください。

    ```bash
    store label 1 region=us-est-1 disk=ssd --rewrite
    ```

-   ID 1 のストアのラベル`"disk"`を削除するには、オプション`--delete`を使用します。

    ```bash
    store label 1 disk --delete
    ```

> **注記：**
>
> -   ストアのラベルはマージ戦略によって更新されます。TiKVプロセスが再起動されると、その設定ファイル内のストアラベルはPDに保存されているストアラベルとマージされ、マージされた結果が保持されます。マージプロセス中に、PD側とTiKV設定ファイルの間で重複するストアラベルが存在する場合、TiKVストアラベル設定によってPDラベルが上書きされます。例えば、ストア1のストアラベルが`"zone=cn"` ～ `store label 1 zone=cn`に設定されているのに、TiKV設定ファイルに`zone = "us"`設定されている場合、TiKVの再起動後に`"zone"`が`"us"`に更新されます。
> -   TiUPを使用してストアのラベルを管理するには、クラスターを再起動する前に、 `store label <id> --force`コマンドを実行して PD に保存されているラベルを空にします。

#### 店舗の重量を設定する {#configure-store-weight}

ID が 1 のストアのリーダー ウェイトを`5`に、リージョンウェイトを`10`に設定するには、次のコマンドを実行します。

```bash
store weight 1 5 10
```

#### 店舗スケジュールの速度を設定する {#configure-store-scheduling-speed}

`store limit`使って店舗のスケジュール速度を設定できます。 `store limit`の原理と使用方法の詳細については、 [`store limit`](/configure-store-limit.md)参照してください。

```bash
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

> **注記：**
>
> `pd-ctl`使用すると、TiKVストアの状態（ `Up` 、 `Disconnect` 、 `Offline` 、 `Down` 、または`Tombstone` ）を確認できます。各状態の関係については、 [TiKVストアの各状態間の関係](/tidb-scheduling.md#information-collection)参照してください。

### <code>log [fatal | error | warn | info | debug]</code> {#code-log-fatal-error-warn-info-debug-code}

このコマンドを使用して、PD リーダーのログ レベルを設定します。

使用法：

```bash
log warn
```

### <code>tso</code> {#code-tso-code}

このコマンドを使用して、TSO の物理時間と論理時間を解析します。

使用法：

```bash
>> tso 395181938313123110        // Parse TSO
system:  2017-10-09 05:50:59 +0800 CST
logic:  120102
```

### <code>unsafe remove-failed-stores [store-ids | show]</code> {#code-unsafe-remove-failed-stores-store-ids-show-code}

> **警告：**
>
> -   この機能は非可逆回復であるため、TiKV はこの機能を使用した後のデータの整合性とデータ インデックスの整合性を保証できません。
> -   機能関連の操作は、TiDB チームのサポートを受けながら実行することをお勧めします。誤った操作を行うと、クラスターの復旧が困難になる可能性があります。

このコマンドは、レプリカが永久的に破損し、データが利用できなくなった場合に、損失を伴うリカバリ操作を実行するために使用します。次の例を参照してください。詳細は[オンラインの安全でない回復](/online-unsafe-recovery.md)に記載されています。

永久的に損傷したストアを削除するには、オンラインの安全でないリカバリを実行します。

```bash
unsafe remove-failed-stores 101,102,103
```

```bash
Success!
```

オンライン安全でない回復の現在の状態または履歴状態を表示します。

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

## Jq形式のJSON出力の使用 {#jq-formatted-json-output-usage}

### <code>store</code>の出力を簡素化 {#simplify-the-output-of-code-store-code}

```bash
>> store --jq=".stores[].store | {id, address, state_name}"
{"id":1,"address":"127.0.0.1:20161","state_name":"Up"}
{"id":30,"address":"127.0.0.1:20162","state_name":"Up"}
...
```

### ノードの残り容量を照会する {#query-the-remaining-space-of-the-node}

```bash
>> store --jq=".stores[] | {id: .store.id, available: .status.available}"
{"id":1,"available":"10 GiB"}
{"id":30,"available":"10 GiB"}
...
```

### ステータスが<code>Up</code>ではないすべてのノードを照会する {#query-all-nodes-whose-status-is-not-code-up-code}

```bash
store --jq='.stores[].store | select(.state_name!="Up") | {id, address, state_name}'
```

    {"id":1,"address":"127.0.0.1:20161""state_name":"Offline"}
    {"id":5,"address":"127.0.0.1:20162""state_name":"Offline"}
    ...

### すべてのTiFlashノードをクエリする {#query-all-tiflash-nodes}

```bash
store --jq='.stores[].store | select(.labels | length>0 and contains([{"key":"engine","value":"tiflash"}])) | {id, address, state_name}'
```

    {"id":1,"address":"127.0.0.1:20161""state_name":"Up"}
    {"id":5,"address":"127.0.0.1:20162""state_name":"Up"}
    ...

### リージョンレプリカの配布ステータスを照会する {#query-the-distribution-status-of-the-region-replicas}

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id]}"
{"id":2,"peer_stores":[1,30,31]}
{"id":4,"peer_stores":[1,31,34]}
...
```

### レプリカの数に応じて領域をフィルタリングする {#filter-regions-according-to-the-number-of-replicas}

たとえば、レプリカ数が 3 ではないすべてのリージョンをフィルターするには、次のようにします。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length != 3)}"
{"id":12,"peer_stores":[30,32]}
{"id":2,"peer_stores":[1,30,31,32]}
```

### レプリカのストアIDに応じてリージョンをフィルタリングする {#filter-regions-according-to-the-store-id-of-replicas}

たとえば、store30 にレプリカがあるすべてのリージョンをフィルタリングするには、次のようにします。

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

### データを復元するときに関連する地域を探す {#look-for-relevant-regions-when-restoring-data}

たとえば、ダウンタイム時に`[store1, store30, store31]`利用できない場合、ダウンしているレプリカが通常のレプリカよりも多いすべてのリージョンを見つけることができます。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length as $total | map(if .==(1,30,31) then . else empty end) | length>=$total-length) }"
{"id":2,"peer_stores":[1,30,31,32]}
{"id":12,"peer_stores":[30,32]}
{"id":14,"peer_stores":[1,30,32]}
...
```

あるいは、 `[store1, store30, store31]`起動に失敗した場合、store1上でデータを安全に手動で削除できるリージョンを見つけることができます。この方法では、store1にレプリカがあり、他のDownPeerを持たないすべてのリージョンをフィルタリングできます。

```bash
>> region --jq=".regions[] | {id: .id, peer_stores: [.peers[].store_id] | select(length>1 and any(.==1) and all(.!=(30,31)))}"
{"id":24,"peer_stores":[1,32,33]}
```

`[store30, store31]`ダウンしている場合は、 `remove-peer`オペレータを作成して安全に処理できるすべてのリージョン、つまり DownPeer が 1 つだけあるリージョンを見つけます。

```bash
>> region --jq=".regions[] | {id: .id, remove_peer: [.peers[].store_id] | select(length>1) | map(if .==(30,31) then . else empty end) | select(length==1)}"
{"id":12,"remove_peer":[30]}
{"id":4,"remove_peer":[31]}
{"id":22,"remove_peer":[30]}
...
```
