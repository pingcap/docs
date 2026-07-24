---
title: PD Configuration File
summary: PD 構成ファイルについて学習します。
---

# PDコンフィグレーションファイル {#pd-configuration-file}

<!-- markdownlint-disable MD001 -->

PD設定ファイルは、コマンドラインパラメータよりも多くのオプションをサポートしています。デフォルトの設定ファイルは[ここ](https://github.com/tikv/pd/blob/release-8.5/conf/config.toml)あります。

このドキュメントでは、コマンドラインパラメータに含まれないパラメータについてのみ説明します。コマンドラインパラメータについては、 [ここ](/command-line-flags-for-pd-configuration.md)参照してください。

> **Tip:**
>
> PD 初期化後に設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)と[PD Controlユーザー ガイド](/pd-control.md)を参照してください。

### `name` {#name}

-   PDノードの一意の名前
-   デフォルト値: `"pd"`
-   複数の PD ノードを開始するには、各ノードに一意の名前を使用します。

### `data-dir` {#data-dir}

-   PDがデータを保存するディレクトリ
-   デフォルト値: `default.${name}"`

### `client-urls` {#client-urls}

-   PDがリッスンするクライアントURLのリスト
-   デフォルト値: `"http://127.0.0.1:2379"`
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`client-urls` （例： `"http://192.168.100.113:2379"` ）に指定する必要があります。クラスターをDocker上で実行する場合は、DockerのIPアドレスを`"http://0.0.0.0:2379"`に指定してください。

### `advertise-client-urls` {#advertise-client-urls}

-   クライアントがPDにアクセスするためのアドバタイズURLのリスト
-   デフォルト値: `"${client-urls}"`
-   Docker または NAT ネットワーク環境などの状況では、クライアントが PD がリッスンするデフォルトのクライアント URL を通じて PD にアクセスできない場合は、アドバタイズ クライアント URL を手動で設定する必要があります。
-   例えば、Dockerの内部IPアドレスは`172.17.0.1` 、ホストのIPアドレスは`192.168.100.113` 、ポートマッピングは`-p 2380:2380`に設定されています。この場合、 `advertise-client-urls`を`"http://192.168.100.113:2380"`に設定できます。クライアントは`"http://192.168.100.113:2380"`を通じてこのサービスを見つけます。

### `peer-urls` {#peer-urls}

-   PDノードがリッスンするピアURLのリスト
-   デフォルト値: `"http://127.0.0.1:2380"`
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`peer-urls` （例： `"http://192.168.100.113:2380"` ）に指定する必要があります。クラスターがDocker上で実行される場合は、DockerのIPアドレスを`"http://0.0.0.0:2380"`に指定してください。

### `advertise-peer-urls` {#advertise-peer-urls}

-   他のPDノード（ピア）がPDノードにアクセスするためのアドバタイズURLのリスト
-   デフォルト: `"${peer-urls}"`
-   Docker または NAT ネットワーク環境などの状況では、他のノード (ピア) がこの PD ノードによってリッスンされるデフォルトのピア URL を介して PD ノードにアクセスできない場合は、アドバタイズ ピア URL を手動で設定する必要があります。
-   例えば、Dockerの内部IPアドレスが`172.17.0.1`で、ホストのIPアドレスが`192.168.100.113` 、ポートマッピングが`-p 2380:2380`に設定されている場合、 `advertise-peer-urls`を`"http://192.168.100.113:2380"`に設定できます。他のPDノードは`"http://192.168.100.113:2380"`を介してこのサービスを検出できます。

### `initial-cluster` {#initial-cluster}

-   ブートストラップのための初期クラスタ構成
-   デフォルト値: `"{name}=http://{advertise-peer-url}"`
-   たとえば、 `name`が「pd」、 `advertise-peer-urls`が`"http://192.168.100.113:2380"`の場合、 `initial-cluster`は`"pd=http://192.168.100.113:2380"`なります。
-   3 つの PD サーバーを起動する必要がある場合、 `initial-cluster`は次のようになります。

        pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380

### `initial-cluster-state` {#initial-cluster-state}

-   クラスターの初期状態
-   デフォルト値: `"new"`

### `initial-cluster-token` {#initial-cluster-token}

-   ブートストラップフェーズ中に異なるクラスターを識別する
-   デフォルト値: `"pd-cluster"`
-   同じ構成のノードを持つ複数のクラスターが連続してデプロイされる場合、異なるクラスター ノードを分離するために異なるトークンを指定する必要があります。

### `lease` {#lease}

-   PDリーダーキーリースのタイムアウト。タイムアウト後、システムはリーダーを再選出します。
-   デフォルト値: v8.5.2 以降では、デフォルト値は`5`です。v8.5.2 より前では、デフォルト値は`3`です。
-   単位: 秒

### `quota-backend-bytes` {#quota-backend-bytes}

-   メタ情報データベースのストレージサイズはデフォルトで8GiBです
-   デフォルト値: `8589934592`

### `auto-compaction-mod` {#auto-compaction-mod}

-   メタ情報データベースの自動圧縮モード
-   使用可能なオプション: `periodic` (サイクル別) および`revision` (バージョン番号別)。
-   デフォルト値: `periodic`

### `auto-compaction-retention` {#auto-compaction-retention}

-   `auto-compaction-retention`が`periodic`の場合、メタ情報データベースの自動圧縮の間隔。圧縮モードが`revision`に設定されている場合、このパラメータは自動圧縮のバージョン番号を示します。
-   デフォルト値: 1時間

### `tick-interval` {#tick-interval}

-   etcdの設定項目`heartbeat-interval`に相当します。異なるPDノードに埋め込まれたetcdインスタンス間のRaftハートビート間隔を制御します。値を小さくすると障害検出が高速化されますが、ネットワーク負荷が増加します。
-   デフォルト値: `500ms`

### `election-interval` {#election-interval}

-   etcdの`election-timeout`の設定項目に相当します。PDノードに組み込まれたetcdインスタンスの選出タイムアウトを制御します。etcdインスタンスがこの期間内に他のetcdインスタンスから有効なハートビートを受信しない場合、 Raft選出を開始します。
-   デフォルト値: `3000ms`
-   この値は[`tick-interval`](#tick-interval)の5倍以上でなければなりません。例えば、 `tick-interval`が`500ms`の場合、 `election-interval`は`2500ms`以上でなければなりません。

### `enable-prevote` {#enable-prevote}

-   etcdの`pre-vote`の設定項目に相当します。PDノードに組み込まれたetcdがRaft事前投票を有効にするかどうかを制御します。有効にすると、etcdは追加の選挙フェーズを実行し、選挙に勝つのに十分な票数を得られるかどうかを確認します。これにより、サービスの中断を最小限に抑えることができます。
-   デフォルト値: `true`

### `force-new-cluster` {#force-new-cluster}

-   PDを強制的に新しいクラスターとして起動し、 Raftメンバーの数を`1`に変更するかどうかを決定します。
-   デフォルト値: `false`

### `tso-update-physical-interval` {#tso-update-physical-interval}

-   PD が TSO の物理時間を更新する間隔。
-   TSO物理時間のデフォルトの更新間隔では、PDは最大262144個のTSOを提供します。より多くのTSOを取得するには、この設定項目の値を減らしてください。最小値は`1ms`です。
-   この設定項目を減らすと、PDのCPU使用率が増加する可能性があります。テストによると、間隔が`50ms`の場合と比較して、間隔が`1ms`の場合、PDの[CPU使用率](https://man7.org/linux/man-pages/man1/top.1.html)が約10%増加します。
-   デフォルト値: `50ms`
-   最小値: `1ms`

## pd-server {#pd-server}

pd-server関連のコンフィグレーション項目

### `server-memory-limit` <span class="version-mark">v6.6.0 の新機能</span> {#server-memory-limit-new-in-v660}

> **Warning:**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   PDインスタンスのメモリ制限比率。値`0`はメモリ制限がないことを意味します。
-   デフォルト値: `0`
-   最小値: `0`
-   最大値: `0.99`

### `server-memory-limit-gc-trigger` <span class="version-mark">v6.6.0の新機能</span> {#server-memory-limit-gc-trigger-new-in-v660}

> **Warning:**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   PDがGCをトリガーしようとする閾値比率。PDのメモリ使用量が`server-memory-limit` × `server-memory-limit-gc-trigger`の値に達すると、PDはGolang GCをトリガーします。1分間にGCがトリガーされるのは1回のみです。
-   デフォルト値: `0.7`
-   最小値: `0.5`
-   最大値: `0.99`

### `enable-gogc-tuner` <span class="version-mark">v6.6.0 の新機能</span> {#enable-gogc-tuner-new-in-v660}

> **Warning:**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   GOGC チューナーを有効にするかどうかを制御します。
-   デフォルト値: `false`

### `gc-tuner-threshold` <span class="version-mark">6.6.0の新機能</span> {#gc-tuner-threshold-new-in-v660}

> **Warning:**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   GOGCチューナーのチューニングにおける最大メモリしきい値比。メモリがこのしきい値`server-memory-limit` × `gc-tuner-threshold` ）を超えると、GOGCチューナーは動作を停止します。
-   デフォルト値: `0.6`
-   最小値: `0`
-   最大値: `0.9`

### `flow-round-by-digit` <span class="version-mark">TiDB 5.1 の新機能</span> {#flow-round-by-digit-new-in-tidb-51}

-   デフォルト値: 3
-   PDはフロー番号の最下位桁を丸めることで、リージョンフロー情報の変更に伴う統計情報の更新を削減します。この設定項目は、リージョンフロー情報の最小桁数を指定します。例えば、フロー`100512`はデフォルト値が`3`であるため、 `101000`に丸められます。この設定は`trace-region-flow`置き換えます。

> **Note:**
>
> クラスターをTiDB 4.0バージョンから現在のバージョンにアップグレードした場合、アップグレード後の`flow-round-by-digit`の動作とアップグレード前の`trace-region-flow`の動作はデフォルトで一致します。つまり、アップグレード前の値`trace-region-flow`がfalseの場合、アップグレード後の値`flow-round-by-digit`は127になります。また、アップグレード前の値`trace-region-flow`が`true`の場合、アップグレード後の値`flow-round-by-digit`は`3`になります。

### `min-resolved-ts-persistence-interval` <span class="version-mark">6.0.0の新機能</span> {#min-resolved-ts-persistence-interval-new-in-v600}

-   PDに最小解決タイムスタンプが保持される間隔を決定します。この値が`0`に設定されている場合、保持は無効です。
-   デフォルト値: v6.3.0 より前のバージョンでは、デフォルト値は`"0s"`です。v6.3.0 以降では、デフォルト値は`"1s"` （最小の正の値）です。
-   最小値: `0`
-   単位: 秒

> **Note:**
>
> v6.0.0～v6.2.0からアップグレードされたクラスターの場合、デフォルト値の`min-resolved-ts-persistence-interval`はアップグレード後も変更されず、 `"0s"`ままとなります。この機能を有効にするには、この設定項目の値を手動で変更する必要があります。

## security {#security}

セキュリティ関連のコンフィグレーション項目

### `cacert-path` {#cacert-path}

-   CAファイルのパス
-   デフォルト値: &quot;&quot;

### `cert-path` {#cert-path}

-   X509証明書を含むPrivacy Enhanced Mail（PEM）ファイルのパス
-   デフォルト値: &quot;&quot;

### `key-path` {#key-path}

-   X509キーを含むPEMファイルのパス
-   デフォルト値: &quot;&quot;

### `redact-info-log`<span class="version-mark">バージョン5.0の新機能</span> {#redact-info-log-new-in-v50}

-   PDログでログ編集を有効にするかどうかを制御します
-   オプション`true` `"marker"` `false`
-   デフォルト値: `false`
-   使用方法の詳細については、 [PD側でのログ編集](/log-redaction.md#log-redaction-in-pd-side)参照してください。

## `log` {#log}

ログ関連のコンフィグレーション項目

### `level` {#level}

-   出力ログのレベルを指定します
-   `"fatal"` `"error"` `"warn"` `"debug"` `"info"`
-   デフォルト値: `"info"`

### `format` {#format}

-   ログ形式
-   オプション`"json"` : `"text"`
-   デフォルト値: `"text"`

### `disable-timestamp` {#disable-timestamp}

-   ログ内の自動生成されたタイムスタンプを無効にするかどうか
-   デフォルト値: `false`

## `log.file` {#log-file}

ログファイルに関連するコンフィグレーション項目

### `max-size` {#max-size}

-   1つのログファイルの最大サイズ。この値を超えると、システムは自動的にログを複数のファイルに分割します。
-   デフォルト値: `300`
-   単位: MiB
-   最小値: `1`

### `max-days` {#max-days}

-   ログが保存される最大日数
-   構成項目が設定されていない場合、またはその値がデフォルト値 0 に設定されている場合、PD はログ ファイルを消去しません。
-   デフォルト値: `0`

### `max-backups` {#max-backups}

-   保存するログファイルの最大数
-   構成項目が設定されていない場合、またはその値がデフォルト値 0 に設定されている場合、PD はすべてのログ ファイルを保持します。
-   デフォルト値: `0`

## `metric` {#metric}

監視に関連するコンフィグレーション項目

### `interval` {#interval}

-   監視メトリックデータがPrometheusにプッシュされる間隔
-   デフォルト値: `15s`

## `schedule` {#schedule}

スケジュールに関連するコンフィグレーション項目

> **Note:**
>
> `schedule`に関連するこれらの PD 構成項目を変更するには、クラスターのステータスに基づいて次のいずれかの方法を選択します。
>
> -   新しくデプロイするクラスターの場合は、PD 構成ファイルを直接変更できます。
> -   既存のクラスターの場合は、コマンドラインツール[PD Control](/pd-control.md)を使用して変更を加えてください。設定ファイル内の`schedule`に関連するPD設定項目を直接変更しても、既存のクラスターには反映されません。

### `max-merge-region-size` {#max-merge-region-size}

-   `Region Merge`のサイズ制限を制御します。リージョンのサイズが指定された値より大きい場合、PD はリージョンを隣接するリージョンと結合しません。
-   デフォルト値: `54` 。v8.4.0より前のバージョンでは、デフォルト値は`20`です。v8.4.0以降では、デフォルト値は`54`です。
-   単位: MiB

### `max-merge-region-keys` {#max-merge-region-keys}

-   `Region Merge`キーの上限を指定します。リージョンキーが指定された値より大きい場合、PDはリージョンを隣接するリージョンと結合しません。
-   デフォルト値: `540000` 。v8.4.0より前のバージョンでは、デフォルト値は`200000`です。v8.4.0以降では、デフォルト値は`540000`です。

### `max-affinity-merge-region-size` <span class="version-mark">v8.5.5 の新機能</span> {#max-affinity-merge-region-size-new-in-v855}

-   [親和性](/table-affinity.md)グループに属する隣接する小さなリージョンを自動的にマージするためのしきい値を制御します。リージョンがアフィニティグループに属し、そのサイズがこのしきい値より小さい場合、PD はこのリージョンを同じアフィニティグループ内の他の隣接する小さなリージョンとマージして、リージョン数を減らし、アフィニティ効果を維持しようとします。
-   これを`0`に設定すると、アフィニティ グループ内の隣接する小さいリージョンの自動マージが無効になります。
-   デフォルト値: `256`
-   単位: MiB

### `patrol-region-interval` {#patrol-region-interval}

-   チェッカーがリージョンのヘルス状態を検査する実行頻度を制御します。この値が小さいほど、チェッカーの実行速度は速くなります。通常、この設定を変更する必要はありません。
-   デフォルト値: `10ms`

### `patrol-region-worker-count`<span class="version-mark">バージョン8.5.0の新機能</span> {#patrol-region-worker-count-new-in-v850}

> **Warning:**
>
> この設定項目を1より大きい値に設定すると、同時チェックが有効になります。これは実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/tikv/pd/issues)報告してください。

-   リージョンのヘルス状態を検査する際にチェッカーによって作成される同時実行数[オペレーター](/glossary.md#operator)を制御します。通常、この設定を調整する必要はありません。
-   デフォルト値: `1`

### `split-merge-interval` {#split-merge-interval}

-   同じリージョンにおける`split`の操作と`merge`操作間の時間間隔を制御します。つまり、新しく分割されたリージョンはしばらくの間マージされません。
-   デフォルト値: `1h`

### `max-movable-hot-peer-size` <span class="version-mark">v6.1.0 の新機能</span> {#max-movable-hot-peer-size-new-in-v610}

-   ホットリージョンスケジュールにスケジュールできる最大リージョンサイズを制御します。
-   デフォルト値: `512`
-   単位: MiB

### `max-snapshot-count` {#max-snapshot-count}

-   1 つのストアが同時に受信または送信するスナップショットの最大数を制御します。PD スケジューラは、この構成に依存して、通常のトラフィックに使用されるリソースがプリエンプトされるのを防ぎます。
-   デフォルト値: `64`

### `max-pending-peer-count` {#max-pending-peer-count}

-   単一ストア内の保留中のピアの最大数を制御します。PD スケジューラはこの構成に依存して、一部のノードで古いログを持つリージョンが過剰に生成されるのを防ぎます。
-   デフォルト値: `64`

### `max-store-down-time` {#max-store-down-time}

-   PDが切断されたストアを復旧不可能と判断するまでのダウンタイム。指定された時間内にストアからのハートビートを受信できない場合、PDは他のノードにレプリカを追加します。
-   デフォルト値: `30m`

### `max-store-preparing-time` <span class="version-mark">v6.1.0 の新機能</span> {#max-store-preparing-time-new-in-v610}

-   ストアがオンラインになるまでの最大待機時間を制御します。ストアがオンライン段階にある間、PDはストアのオンライン進行状況を照会できます。指定された時間を超えると、PDはストアがオンラインになったとみなし、再度ストアのオンライン進行状況を照会できなくなります。ただし、これによってリージョンが新しいオンラインストアに移行するのが妨げられることはありません。ほとんどの場合、このパラメータを調整する必要はありません。
-   デフォルト値: `48h`

### `leader-schedule-limit` {#leader-schedule-limit}

-   同時に実行されるリーダースケジュールタスクの数
-   デフォルト値: `4`

### `region-schedule-limit` {#region-schedule-limit}

-   同時に実行されるリージョンスケジュールタスクの数
-   デフォルト値: `2048`

### `enable-diagnostic` <span class="version-mark">6.3.0の新機能</span> {#enable-diagnostic-new-in-v630}

-   診断機能を有効にするかどうかを制御します。有効にすると、PDは診断を支援するためにスケジューリング中の状態を記録します。有効にすると、スケジューリング速度に若干影響し、ストア数が多い場合にメモリ消費量が増える可能性があります。
-   デフォルト値: バージョン7.1.0以降、デフォルト値は`false`から`true`に変更されます。クラスターをバージョン7.1.0より前のバージョンからバージョン7.1.0以降にアップグレードした場合、デフォルト値は変更されません。

### `hot-region-schedule-limit` {#hot-region-schedule-limit}

-   同時に実行されているホットなリージョンスケジューリングタスクを制御します。これはリージョンスケジューリングとは独立しています。
-   デフォルト値: `4`

### `hot-region-cache-hits-threshold` {#hot-region-cache-hits-threshold}

-   ホットリージョンを識別するために必要な分数を設定するために使用されるしきい値。PD は、リージョンがこの分数を超えてホットスポット状態になった場合にのみ、ホットスポット スケジューリングに参加できます。
-   デフォルト値: `3`

### `replica-schedule-limit` {#replica-schedule-limit}

-   同時に実行されるレプリカスケジュールタスクの数
-   デフォルト値: `64`

### `merge-schedule-limit` {#merge-schedule-limit}

-   同時に実行される`Region Merge`スケジュールタスクの数`Region Merge`を無効にするには、このパラメータを`0`に設定します。
-   デフォルト値: `8`

### `affinity-schedule-limit` <span class="version-mark">v8.5.5 の新機能</span> {#affinity-schedule-limit-new-in-v855}

-   同時に実行できる[親和性](/table-affinity.md)スケジュールタスクの数を制御します。3に設定すると`0`アフィニティスケジュールが無効になります。
-   デフォルト値: `0`

### `high-space-ratio` {#high-space-ratio}

-   ストアの容量が十分であることを示す閾値比率。ストアのスペース占有率がこの閾値を下回る場合、PDはスケジューリング時にストアの残りのスペースを無視し、主にリージョンサイズに基づいて負荷分散を行います。この設定は、 `region-score-formula-version` `v1`に設定した場合のみ有効です。
-   デフォルト値: `0.7`
-   最小値: `0`より大きい
-   最大値: `1`未満

### `low-space-ratio` {#low-space-ratio}

-   ストアの容量が不足する閾値比率。ストアのスペース占有率がこの閾値を超えると、PDはこのストアへのデータ移行を可能な限り回避します。同時に、該当ストアのディスク容量が枯渇することを避けるため、PDは主にストアの残容量に基づいてスケジューリングを行います。
-   デフォルト値: `0.8`
-   最小値: `0`より大きい
-   最大値: `1`未満

### `tolerant-size-ratio` {#tolerant-size-ratio}

-   `balance`バッファサイズを制御します
-   デフォルト値: `0` (バッファサイズを自動調整)
-   最小値: `0`

### `enable-cross-table-merge` {#enable-cross-table-merge}

-   クロステーブルリージョンの結合を有効にするかどうかを決定します
-   デフォルト値: `true`

### `region-score-formula-version` <span class="version-mark">v5.0 の新機能</span> {#region-score-formula-version-new-in-v50}

-   リージョンスコア計算式のバージョンを制御します
-   デフォルト値: `v2`
-   オプション値: `v1`および`v2`と比較して、v2 の変更はよりスムーズになり、スペースの再利用によって発生するスケジュールのジッターが改善されています。

> **Note:**
>
> クラスターをTiDB 4.0バージョンから最新バージョンにアップグレードした場合、アップグレード前後のPD動作の一貫性を確保するため、新しいFormulaバージョンはデフォルトで自動的に無効化されます。Formulaバージョンを変更する場合は、 `pd-ctl`設定を手動で切り替える必要があります。詳細は[PD Control](/pd-control.md#config-show--set-option-value--placement-rules)を参照してください。

### `store-limit-version` <span class="version-mark">v7.1.0 の新機能</span> {#store-limit-version-new-in-v710}

-   ストア制限の計算式のバージョンを制御します
-   デフォルト値: `v1`
-   値のオプション:
    -   `v1` : v1 モードでは、 `store limit`を手動で変更して、単一の TiKV のスケジュール速度を制限できます。
    -   `v2` : v2モードでは、PDがTiKVスナップショットの機能に基づいて動的に調整するため、 `store limit`値を手動で設定する必要はありません。詳細については、 [ストア制限の原則 v2](/configure-store-limit.md#principles-of-store-limit-v2)を参照してください。

### `enable-joint-consensus` <span class="version-mark">5.0の新機能</span> {#enable-joint-consensus-new-in-v50}

-   レプリカのスケジュール設定にジョイントコンセンサスを使用するかどうかを制御します。この設定が無効になっている場合、PDは一度に1つのレプリカをスケジュールします。
-   デフォルト値: `true`

### `hot-regions-write-interval` <span class="version-mark">v5.4.0 の新機能</span> {#hot-regions-write-interval-new-in-v540}

-   PD がホットリージョン情報を保存する時間間隔。
-   デフォルト値: `10m`

> **Note:**
>
> ホットリージョンに関する情報は3分ごとに更新されます。更新間隔を3分未満に設定した場合、更新間隔中の更新は意味をなさない可能性があります。

### `hot-regions-reserved-days` <span class="version-mark">v5.4.0 の新機能</span> {#hot-regions-reserved-days-new-in-v540}

-   ホットリージョン情報を保持する日数を指定します。
-   デフォルト値: `7`

### `enable-heartbeat-breakdown-metrics` <span class="version-mark">v8.0.0 の新機能</span> {#enable-heartbeat-breakdown-metrics-new-in-v800}

-   リージョンハートビートの内訳メトリクスを有効にするかどうかを制御します。これらのメトリクスは、リージョンハートビート処理の各段階で消費された時間を測定し、監視による分析を容易にします。
-   デフォルト値: `true`

### `enable-heartbeat-concurrent-runner`<span class="version-mark">バージョン 8.0.0 の新機能</span> {#enable-heartbeat-concurrent-runner-new-in-v800}

-   リージョンハートビートの非同期同時処理を有効にするかどうかを制御します。有効にすると、独立したエグゼキューターがリージョンハートビートリクエストを非同期かつ同時に処理するため、ハートビート処理のスループットが向上し、レイテンシーが短縮されます。
-   デフォルト値: `true`

## `replication` {#replication}

レプリカに関連するコンフィグレーション項目

### `max-replicas` {#max-replicas}

-   レプリカの数、つまりリーダーとフォロワーの数の合計です。デフォルト値の`3` 、リーダーが1つ、フォロワーが2つであることを意味します。この設定が動的に変更されると、PDはバックグラウンドでリージョンをスケジュールし、レプリカの数がこの設定と一致するようにします。
-   デフォルト値: `3`

### `location-labels` {#location-labels}

-   TiKVクラスタのトポロジ情報
-   デフォルト値: `[]`
-   [クラスタトポロジ構成](/schedule-replicas-by-topology-labels.md)

### `isolation-level` {#isolation-level}

-   TiKVクラスタの最小トポロジカル分離レベル
-   デフォルト値: `""`
-   [クラスタトポロジ構成](/schedule-replicas-by-topology-labels.md)

### `strictly-match-label` {#strictly-match-label}

-   TiKV ラベルが PD `location-labels`と一致するかどうかを厳密にチェックできるようにします。
-   デフォルト値: `false`

### `enable-placement-rules` {#enable-placement-rules}

-   `placement-rules`を有効にします。
-   デフォルト値: `true`
-   [配置ルール](/configure-placement-rules.md)参照。

## <code>label-property</code> （非推奨） {#code-label-property-code-deprecated}

ラベルに関連するコンフィグレーション項目`reject-leader`型のみをサポートします。

> **Note:**
>
> バージョン5.2以降、ラベル関連の設定項目は非推奨となりました。レプリカポリシーの設定には[配置ルール](/configure-placement-rules.md#scenario-2-place-five-replicas-in-three-data-centers-in-the-proportion-of-221-and-the-leader-should-not-be-in-the-third-data-center)使用することをお勧めします。

### <code>key</code> （非推奨） {#code-key-code-deprecated}

-   リーダーを拒否したストアのラベルキー
-   デフォルト値: `""`

### <code>value</code> （非推奨） {#code-value-code-deprecated}

-   リーダーを拒否したストアのラベル値
-   デフォルト値: `""`

## `dashboard` {#dashboard}

[TiDB Dashboard](/dashboard/dashboard-intro.md)内蔵 PD に関するコンフィグレーション項目です。

### `disable-custom-prom-addr` {#disable-custom-prom-addr}

-   [TiDB Dashboard](/dashboard/dashboard-intro.md)でカスタム Prometheus データ ソース アドレスの構成を無効にするかどうか。
-   デフォルト値: `false`
-   `true`に設定すると、TiDB Dashboardでカスタム Prometheus データ ソース アドレスを構成すると、TiDB Dashboardはエラーを報告します。

### `tidb-cacert-path` {#tidb-cacert-path}

-   ルートCA証明書ファイルのパス。TLSを使用してTiDBのSQLサービスに接続するときに、このパスを設定できます。
-   デフォルト値: `""`

### `tidb-cert-path` {#tidb-cert-path}

-   SSL証明書ファイルのパス。TLSを使用してTiDBのSQLサービスに接続するときに、このパスを設定できます。
-   デフォルト値: `""`

### `tidb-key-path` {#tidb-key-path}

-   SSL秘密鍵ファイルのパス。TLSを使用してTiDBのSQLサービスに接続するときに、このパスを設定できます。
-   デフォルト値: `""`

### `public-path-prefix` {#public-path-prefix}

-   TiDB Dashboardがリバース プロキシの背後でアクセスされる場合、この項目はすべての Web リソースのパブリック URL パス プレフィックスを設定します。
-   デフォルト値: `/dashboard`
-   リバースプロキシを経由せずにTiDB Dashboardにアクセスする場合は、この設定項目を変更**しないで**ください。変更すると、アクセスの問題が発生する可能性があります。詳細は[リバースプロキシの背後で TiDB Dashboardを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照してください。

### `enable-telemetry` {#enable-telemetry}

> **Warning:**
>
> v8.1.0以降、TiDB Dashboardのテレメトリ機能は削除され、この設定項目は機能しなくなりました。これは以前のバージョンとの互換性のためだけに残されています。

-   v8.1.0 より前では、この構成項目は、TiDB Dashboardでテレメトリ収集を有効にするかどうかを制御します。
-   デフォルト値: `false`

## `replication-mode` {#replication-mode}

全リージョンのレプリケーションモードに関するコンフィグレーション項目です。詳細は[DR自動同期モードを有効にする](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)ご覧ください。

## controller {#controller}

このセクションでは、 PD for [リソース管理](/tidb-resource-control-ru-groups.md)に組み込まれている構成項目について説明します。

### `degraded-mode-wait-duration` {#degraded-mode-wait-duration}

-   縮退モードをトリガーするまでの待機時間。縮退モードとは、ローカルトークンバケット（LTB）とグローバルトークンバケット（GTB）が失われた場合、LTBがデフォルトのリソースグループ構成にフォールバックし、GTB認証トークンがなくなることを意味します。これにより、ネットワークの分離や異常が発生した場合でも、サービスが影響を受けないことが保証されます。
-   デフォルト値: 0秒
-   デフォルトでは、劣化モードは無効になっています。

### `request-unit` {#request-unit}

[リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)に関する設定項目は以下のとおりです。

#### `read-base-cost` {#read-base-cost}

-   読み取り要求からRUへの変換の基礎係数
-   デフォルト値: 0.125

#### `write-base-cost` {#write-base-cost}

-   書き込み要求からRUへの変換の基礎係数
-   デフォルト値: 1

#### `read-cost-per-byte` {#read-cost-per-byte}

-   読み取りフローからRUへの変換の基礎係数
-   デフォルト値: 1/(64 * 1024)
-   1 RU = 64 KiB の読み取りバイト

#### `write-cost-per-byte` {#write-cost-per-byte}

-   書き込みフローからRUへの変換の基礎係数
-   デフォルト値: 1/1024
-   1 RU = 1 KiB 書き込みバイト

#### `read-cpu-ms-cost` {#read-cpu-ms-cost}

-   CPUからRUへの変換の基礎係数
-   デフォルト値: 1/3
-   1 RU = 3ミリ秒のCPU時間
