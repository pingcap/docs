---
title: PD Configuration File
summary: Learn the PD configuration file.
---

# PDコンフィグレーションファイル {#pd-configuration-file}

<!-- markdownlint-disable MD001 -->

PD 構成ファイルは、コマンドライン パラメーターよりも多くのオプションをサポートしています。デフォルトの構成ファイル[ここ](https://github.com/pingcap/pd/blob/release-7.5/conf/config.toml)が見つかります。

このドキュメントでは、コマンドライン パラメーターに含まれないパラメーターのみについて説明します。コマンドラインパラメータの場合は[ここ](/command-line-flags-for-pd-configuration.md)確認してください。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>name</code> {#code-name-code}

-   PD ノードの一意の名前
-   デフォルト値: `"pd"`
-   複数の PD ノードを開始するには、各ノードに一意の名前を使用します。

### <code>data-dir</code> {#code-data-dir-code}

-   PDがデータを保存するディレクトリ
-   デフォルト値: `default.${name}"`

### <code>client-urls</code> {#code-client-urls-code}

-   PD がリッスンするクライアント URL のリスト
-   デフォルト値: `"http://127.0.0.1:2379"`
-   クラスターをデプロイするときは、現在のホストの IP アドレスを`client-urls` (たとえば、 `"http://192.168.100.113:2379"` ) として指定する必要があります。クラスターが Docker 上で実行されている場合は、Docker の IP アドレスを`"http://0.0.0.0:2379"`として指定します。

### <code>advertise-client-urls</code> {#code-advertise-client-urls-code}

-   クライアントが PD にアクセスするためのアドバタイズ URL のリスト
-   デフォルト値: `"${client-urls}"`
-   Docker や NAT ネットワーク環境などの状況によっては、PD がリッスンするデフォルトのクライアント URL を介してクライアントが PD にアクセスできない場合は、アドバタイズ クライアント URL を手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 2380:2380`に設定されています。この場合、 `advertise-client-urls` ～ `"http://192.168.100.113:2380"`を設定できます。クライアントは`"http://192.168.100.113:2380"`を通じてこのサービスを見つけることができます。

### <code>peer-urls</code> {#code-peer-urls-code}

-   PD ノードがリッスンするピア URL のリスト
-   デフォルト値: `"http://127.0.0.1:2380"`
-   クラスターをデプロイするときは、現在のホストの IP アドレスとして`peer-urls` ( `"http://192.168.100.113:2380"`など) を指定する必要があります。クラスターが Docker 上で実行されている場合は、Docker の IP アドレスを`"http://0.0.0.0:2380"`として指定します。

### <code>advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   他の PD ノード (ピア) が PD ノードにアクセスするためのアドバタイズ URL のリスト
-   デフォルト: `"${peer-urls}"`
-   Docker または NAT ネットワーク環境などの状況によっては、他のノード (ピア) が、この PD ノードがリッスンするデフォルトのピア URL を介して PD ノードにアクセスできない場合は、アドバタイズピア URL を手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 2380:2380`に設定されています。この場合、 `advertise-peer-urls` ～ `"http://192.168.100.113:2380"`を設定できます。他の PD ノードは`"http://192.168.100.113:2380"`を通じてこのサービスを見つけることができます。

### <code>initial-cluster</code> {#code-initial-cluster-code}

-   ブートストラップ用の初期クラスター構成
-   デフォルト値: `"{name}=http://{advertise-peer-url}"`
-   たとえば、 `name`が &quot;pd&quot; で、 `advertise-peer-urls`が`"http://192.168.100.113:2380"`の場合、 `initial-cluster`は`"pd=http://192.168.100.113:2380"`になります。
-   3 つの PD サーバーを起動する必要がある場合、 `initial-cluster`は次のようになります。

        pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380

### <code>initial-cluster-state</code> {#code-initial-cluster-state-code}

-   クラスターの初期状態
-   デフォルト値: `"new"`

### <code>initial-cluster-token</code> {#code-initial-cluster-token-code}

-   ブートストラップフェーズ中にさまざまなクラスターを識別します
-   デフォルト値: `"pd-cluster"`
-   同じ構成のノードを持つ複数のクラスターが連続してデプロイされる場合は、異なるクラスター ノードを分離するために異なるトークンを指定する必要があります。

### <code>lease</code> {#code-lease-code}

-   PDLeaderキーのリースのタイムアウト。タイムアウト後、システムはLeaderを再選出します。
-   デフォルト値: `3`
-   単位：秒

### <code>quota-backend-bytes</code> {#code-quota-backend-bytes-code}

-   メタ情報データベースのstorageサイズ (デフォルトでは 8GiB)
-   デフォルト値: `8589934592`

### <code>auto-compaction-mod</code> {#code-auto-compaction-mod-code}

-   メタ情報データベースの自動圧縮モード
-   利用可能なオプション: `periodic` (サイクル別) および`revision` (バージョン番号別)。
-   デフォルト値: `periodic`

### <code>auto-compaction-retention</code> {#code-auto-compaction-retention-code}

-   `auto-compaction-retention`が`periodic`の場合のメタ情報データベースの自動圧縮の時間間隔。圧縮モードが`revision`に設定されている場合、このパラメータは自動圧縮のバージョン番号を示します。
-   デフォルト値: 1h

### <code>force-new-cluster</code> {#code-force-new-cluster-code}

-   PD を強制的に新しいクラスターとして起動し、 Raftメンバーの数を`1`に変更するかどうかを決定します。
-   デフォルト値: `false`

### <code>tso-update-physical-interval</code> {#code-tso-update-physical-interval-code}

-   PD が TSO の物理時間を更新する間隔。
-   TSO 物理時間のデフォルトの更新間隔では、PD は最大 262144 個の TSO を提供します。より多くの TSO を取得するには、この構成項目の値を減らすことができます。最小値は`1ms`です。
-   この設定項目を減らすと、PD の CPU 使用率が増加する可能性があります。実験によると、間隔が`50ms`場合に比べ、間隔が`1ms`の場合は PD の[CPU使用率](https://man7.org/linux/man-pages/man1/top.1.html)約 10% 増加します。
-   デフォルト値: `50ms`
-   最小値: `1ms`

## PDサーバー {#pd-server}

pd-serverに関するコンフィグレーション項目

### <code>server-memory-limit</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-server-memory-limit-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この構成は実験的機能です。本番環境での使用はお勧めできません。

-   PD インスタンスのメモリ制限率。値`0`はメモリ制限がないことを意味します。
-   デフォルト値: `0`
-   最小値: `0`
-   最大値： `0.99`

### <code>server-memory-limit-gc-trigger</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-server-memory-limit-gc-trigger-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この構成は実験的機能です。本番環境での使用はお勧めできません。

-   PD が GC をトリガーしようとするしきい値比率。 PD のメモリ使用量が`server-memory-limit` * `server-memory-limit-gc-trigger`の値に達すると、PD はGolang GC をトリガーします。 1 分間にトリガーされる GC は 1 つだけです。
-   デフォルト値: `0.7`
-   最小値: `0.5`
-   最大値： `0.99`

### <code>enable-gogc-tuner</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-enable-gogc-tuner-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この構成は実験的機能です。本番環境での使用はお勧めできません。

-   GOGC チューナーを有効にするかどうかを制御します。
-   デフォルト値: `false`

### <code>gc-tuner-threshold</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-gc-tuner-threshold-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この構成は実験的機能です。本番環境での使用はお勧めできません。

-   GOGC を調整するための最大メモリしきい値比率。メモリがこのしきい値、つまり`server-memory-limit`の値 * `gc-tuner-threshold`の値を超えると、GOGC チューナーは動作を停止します。
-   デフォルト値: `0.6`
-   最小値: `0`
-   最大値： `0.9`

### <code>flow-round-by-digit</code> <span class="version-mark">TiDB 5.1 の新機能</span> {#code-flow-round-by-digit-code-span-class-version-mark-new-in-tidb-5-1-span}

-   デフォルト値: 3
-   PD はフロー番号の最下位の桁を丸めます。これにより、リージョンフロー情報の変更によって引き起こされる統計の更新が削減されます。この設定項目は、リージョンフロー情報の四捨五入の最下位桁数を指定するために使用されます。たとえば、デフォルト値が`3`であるため、フロー`100512` `101000`に丸められます。この構成は`trace-region-flow`を置き​​換えます。

> **注記：**
>
> クラスターを TiDB 4.0 バージョンから現在のバージョンにアップグレードした場合、アップグレード後の`flow-round-by-digit`の動作とアップグレード前の`trace-region-flow`の動作はデフォルトで一貫しています。これは、アップグレード前の値`trace-region-flow`が false の場合、アップグレード後の値`flow-round-by-digit`は 127 であることを意味します。アップグレード前の値`trace-region-flow`が`true`の場合、アップグレード後の値`flow-round-by-digit`は`3`になります。

### <code>min-resolved-ts-persistence-interval</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-min-resolved-ts-persistence-interval-code-span-class-version-mark-new-in-v6-0-0-span}

-   最小の解決されたタイムスタンプが PD に対して永続化される間隔を決定します。この値が`0`に設定されている場合は、永続性が無効になっていることを意味します。
-   デフォルト値: v6.3.0 より前のデフォルト値は`"0s"`です。 v6.3.0 以降、デフォルト値は`"1s"`で、これは正の最小値です。
-   最小値: `0`
-   単位：秒

> **注記：**
>
> v6.0.0 ～ v6.2.0 からアップグレードされたクラスターの場合、デフォルト値`min-resolved-ts-persistence-interval`はアップグレード後も変更されず、 `"0s"`のままになります。この機能を有効にするには、この構成項目の値を手動で変更する必要があります。

## 安全 {#security}

セキュリティに関するコンフィグレーション項目

### <code>cacert-path</code> {#code-cacert-path-code}

-   CA ファイルのパス
-   デフォルト値: &quot;&quot;

### <code>cert-path</code> {#code-cert-path-code}

-   X509 証明書を含むプライバシー強化メール (PEM) ファイルのパス
-   デフォルト値: &quot;&quot;

### <code>key-path</code> {#code-key-path-code}

-   X509 キーを含む PEM ファイルのパス
-   デフォルト値: &quot;&quot;

### <code>redact-info-log</code> <span class="version-mark">v5.0 の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v5-0-span}

-   PD ログでログ編集を有効にするかどうかを制御します
-   構成値を`true`に設定すると、PD ログ内のユーザー データが編集されます。
-   デフォルト値: `false`

## <code>log</code> {#code-log-code}

ログに関するコンフィグレーション項目

### <code>level</code> {#code-level-code}

-   出力ログのレベルを指定します
-   オプションの値: `"debug"` 、 `"info"` 、 `"warn"` 、 `"error"` 、 `"fatal"`
-   デフォルト値: `"info"`

### <code>format</code> {#code-format-code}

-   ログ形式
-   オプション`"json"`値: `"text"`
-   デフォルト値: `"text"`

### <code>disable-timestamp</code> {#code-disable-timestamp-code}

-   ログ内で自動的に生成されたタイムスタンプを無効にするかどうか
-   デフォルト値: `false`

## <code>log.file</code> {#code-log-file-code}

ログファイルに関するコンフィグレーション項目

### <code>max-size</code> {#code-max-size-code}

-   単一のログ ファイルの最大サイズ。この値を超えると、システムはログを自動的に複数のファイルに分割します。
-   デフォルト値: `300`
-   単位: MiB
-   最小値: `1`

### <code>max-days</code> {#code-max-days-code}

-   ログが保存される最大日数
-   構成項目が設定されていない場合、またはその値がデフォルト値 0 に設定されている場合、PD はログ ファイルを消去しません。
-   デフォルト値: `0`

### <code>max-backups</code> {#code-max-backups-code}

-   保存するログ ファイルの最大数
-   構成項目が設定されていない場合、またはその値がデフォルト値 0 に設定されている場合、PD はすべてのログ ファイルを保持します。
-   デフォルト値: `0`

## <code>metric</code> {#code-metric-code}

監視に関するコンフィグレーション項目

### <code>interval</code> {#code-interval-code}

-   監視メトリクス データが Prometheus にプッシュされる間隔
-   デフォルト値: `15s`

## <code>schedule</code> {#code-schedule-code}

スケジュールに関するコンフィグレーション項目

### <code>max-merge-region-size</code> {#code-max-merge-region-size-code}

-   サイズ制限`Region Merge`を制御します。リージョンサイズが指定された値より大きい場合、PD はリージョンを隣接するリージョンとマージしません。
-   デフォルト値: `20`
-   単位: MiB

### <code>max-merge-region-keys</code> {#code-max-merge-region-keys-code}

-   `Region Merge`キーの上限を指定します。リージョンキーが指定された値より大きい場合、PD はリージョンを隣接するリージョンとマージしません。
-   デフォルト値: `200000`

### <code>patrol-region-interval</code> {#code-patrol-region-interval-code}

-   `replicaChecker`がリージョンの健全性状態をチェックする実行頻度を制御します。この値が小さいほど、 `replicaChecker`回の実行が速くなります。通常、このパラメータを調整する必要はありません。
-   デフォルト値: `10ms`

### <code>split-merge-interval</code> {#code-split-merge-interval-code}

-   同じリージョンに対する`split`と`merge`操作間の時間間隔を制御します。つまり、新しく分割されたリージョンはしばらくマージされません。
-   デフォルト値: `1h`

### <code>max-snapshot-count</code> {#code-max-snapshot-count-code}

-   単一ストアが同時に受信または送信するスナップショットの最大数を制御します。 PD スケジューラは、この設定に依存して、通常のトラフィックに使用されるリソースがプリエンプトされるのを防ぎます。
-   デフォルト値の値: `64`

### <code>max-pending-peer-count</code> {#code-max-pending-peer-count-code}

-   単一ストア内の保留中のピアの最大数を制御します。 PD スケジューラーはこの構成に依存して、一部のノードで古いログを持つリージョンが多数生成されるのを防ぎます。
-   デフォルト値: `64`

### <code>max-store-down-time</code> {#code-max-store-down-time-code}

-   PD が切断されたストアを回復できないと判断するまでのダウンタイム。 PD は、指定された時間が経過してもストアからハートビートを受信できない場合、他のノードにレプリカを追加します。
-   デフォルト値: `30m`

### <code>max-store-preparing-time</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-max-store-preparing-time-code-span-class-version-mark-new-in-v6-1-0-span}

-   ストアがオンラインになるまでの最大待ち時間を制御します。ストアのオンライン段階で、PD はストアのオンライン進行状況をクエリできます。指定された時間を超えると、PD はストアがオンラインになったとみなし、ストアのオンラインの進行状況を再度照会できなくなります。ただし、これはリージョンが新しいオンライン ストアに移行することを妨げるものではありません。ほとんどのシナリオでは、このパラメーターを調整する必要はありません。
-   デフォルト値: `48h`

### <code>leader-schedule-limit</code> {#code-leader-schedule-limit-code}

-   同時に実行されるLeaderのスケジュール設定タスクの数
-   デフォルト値: `4`

### <code>region-schedule-limit</code> {#code-region-schedule-limit-code}

-   同時に実行されるリージョンスケジュール タスクの数
-   デフォルト値: `2048`

### <code>enable-diagnostic</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-enable-diagnostic-code-span-class-version-mark-new-in-v6-3-0-span}

-   診断機能を有効にするかどうかを制御します。有効にすると、PD はスケジューリング中に状態を記録し、診断に役立てます。有効にすると、ストアの数が多い場合、スケジューリング速度にわずかに影響し、より多くのメモリを消費する可能性があります。
-   デフォルト値: v7.1.0 以降、デフォルト値は`false`から`true`に変更されます。クラスターが v7.1.0 より前のバージョンから v7.1.0 以降にアップグレードされた場合、デフォルト値は変更されません。

### <code>hot-region-schedule-limit</code> {#code-hot-region-schedule-limit-code}

-   同時に実行されているホットリージョンのスケジュール タスクを制御します。これは、リージョンのスケジュールとは独立しています。
-   デフォルト値: `4`

### <code>hot-region-cache-hits-threshold</code> {#code-hot-region-cache-hits-threshold-code}

-   ホットリージョンを識別するために必要な分数を設定するために使用されるしきい値。 PD は、リージョンがこの分数を超えてホットスポット状態になった後にのみホットスポット スケジューリングに参加できます。
-   デフォルト値: `3`

### <code>replica-schedule-limit</code> {#code-replica-schedule-limit-code}

-   同時に実行されるレプリカのスケジューリング タスクの数
-   デフォルト値: `64`

### <code>merge-schedule-limit</code> {#code-merge-schedule-limit-code}

-   同時に実行される`Region Merge`スケジューリング タスクの数。 `Region Merge`を無効にするには、このパラメータを`0`に設定します。
-   デフォルト値: `8`

### <code>high-space-ratio</code> {#code-high-space-ratio-code}

-   ストアの容量がそれ以下であれば十分であるというしきい値比率。ストアのスペース占有率がこのしきい値より小さい場合、PD はスケジューリングを実行する際にストアの残りスペースを無視し、主にリージョンサイズに基づいて負荷分散を行います。この設定は、 `region-score-formula-version`が`v1`に設定されている場合にのみ有効になります。
-   デフォルト値: `0.7`
-   最小値: `0`より大きい
-   最大値： `1`未満

### <code>low-space-ratio</code> {#code-low-space-ratio-code}

-   ストアの容量が不足するしきい値比率。ストアのスペース占有率がこのしきい値を超える場合、PD はそのストアへのデータの移行を可能な限り回避します。一方、対応するストアのディスク容量が枯渇するのを避けるために、PD は主にストアの残り容量に基づいてスケジューリングを実行します。
-   デフォルト値: `0.8`
-   最小値: `0`より大きい
-   最大値： `1`未満

### <code>tolerant-size-ratio</code> {#code-tolerant-size-ratio-code}

-   `balance`バッファ サイズを制御します
-   デフォルト値: `0` (バッファサイズを自動的に調整します)
-   最小値: `0`

### <code>enable-cross-table-merge</code> {#code-enable-cross-table-merge-code}

-   テーブル間のリージョンの結合を有効にするかどうかを決定します。
-   デフォルト値: `true`

### <code>region-score-formula-version</code> <span class="version-mark">v5.0 の新機能</span> {#code-region-score-formula-version-code-span-class-version-mark-new-in-v5-0-span}

-   リージョンスコア式のバージョンを制御します
-   デフォルト値: `v2`
-   オプションの値: `v1`および`v2` 。 v1 と比較して、v2 の変更はよりスムーズであり、スペースの再利用によって引き起こされるスケジューリングのジッターは改善されています。

> **注記：**
>
> クラスターを TiDB 4.0 バージョンから現在のバージョンにアップグレードした場合、アップグレードの前後で一貫した PD 動作を確保するために、新しいフォーミュラ バージョンはデフォルトで自動的に無効になります。式のバージョンを変更したい場合は、 `pd-ctl`設定を手動で切り替える必要があります。詳細は[PD Control](/pd-control.md#config-show--set-option-value--placement-rules)を参照してください。

### <code>store-limit-version</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-store-limit-version-code-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> この構成項目を`"v2"`に設定するのは実験的機能です。本番環境での使用はお勧めできません。

-   ストア制限式のバージョンを制御します
-   デフォルト値: `v1`
-   値のオプション:
    -   `v1` : v1 モードでは、 `store limit`手動で変更して、単一の TiKV のスケジュール速度を制限できます。
    -   `v2` : (実験的機能) v2 モードでは、PD が TiKV スナップショットの機能に基づいて`store limit`値を動的に調整するため、手動で 2 の値を設定する必要はありません。詳細については[ストア制限 v2 の原則](/configure-store-limit.md#principles-of-store-limit-v2)を参照してください。

### <code>enable-joint-consensus</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-joint-consensus-code-span-class-version-mark-new-in-v5-0-span}

-   レプリカのスケジュールに共同コンセンサスを使用するかどうかを制御します。この構成が無効になっている場合、PD は一度に 1 つのレプリカをスケジュールします。
-   デフォルト値: `true`

### <code>hot-regions-write-interval</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-hot-regions-write-interval-code-span-class-version-mark-new-in-v5-4-0-span}

-   PD がホットリージョン情報を保存する時間間隔。
-   デフォルト値: `10m`

> **注記：**
>
> ホット リージョンに関する情報は 3 分ごとに更新されます。間隔が 3 分未満に設定されている場合、間隔中の更新は無意味になる可能性があります。

### <code>hot-regions-reserved-days</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-hot-regions-reserved-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   ホットリージョン情報を保持する日数を指定します。
-   デフォルト値: `7`

## <code>replication</code> {#code-replication-code}

レプリカに関するコンフィグレーション項目

### <code>max-replicas</code> {#code-max-replicas-code}

-   レプリカの数、つまりリーダーとフォロワーの数の合計。デフォルト値`3` 1 人のリーダーと 2 人のフォロワーを意味します。この構成が動的に変更されると、PD はレプリカの数がこの構成と一致するようにバックグラウンドでリージョンをスケジュールします。
-   デフォルト値: `3`

### <code>location-labels</code> {#code-location-labels-code}

-   TiKVクラスターのトポロジー情報
-   デフォルト値: `[]`
-   [クラスタトポロジ構成](/schedule-replicas-by-topology-labels.md)

### <code>isolation-level</code> {#code-isolation-level-code}

-   TiKV クラスターの最小トポロジ分離レベル
-   デフォルト値: `""`
-   [クラスタトポロジ構成](/schedule-replicas-by-topology-labels.md)

### <code>strictly-match-label</code> {#code-strictly-match-label-code}

-   TiKV ラベルが PD と一致するかどうかの厳密なチェックを有効にします`location-labels` 。
-   デフォルト値: `false`

### <code>enable-placement-rules</code> {#code-enable-placement-rules-code}

-   `placement-rules`を有効にします。
-   デフォルト値: `true`
-   [配置ルール](/configure-placement-rules.md)を参照してください。

## <code>label-property</code> {#code-label-property-code}

ラベルに関するコンフィグレーション項目

### <code>key</code> {#code-key-code}

-   Leaderを拒否したストアのラベル キー
-   デフォルト値: `""`

### <code>value</code> {#code-value-code}

-   Leaderを拒否したストアのラベル値
-   デフォルト値: `""`

## <code>dashboard</code> {#code-dashboard-code}

[TiDB ダッシュボード](/dashboard/dashboard-intro.md)内蔵 PD に関するコンフィグレーション項目。

### <code>tidb-cacert-path</code> {#code-tidb-cacert-path-code}

-   ルート CA 証明書ファイルのパス。 TLS を使用して TiDB の SQL サービスに接続するときに、このパスを構成できます。
-   デフォルト値: `""`

### <code>tidb-cert-path</code> {#code-tidb-cert-path-code}

-   SSL証明書ファイルのパス。 TLS を使用して TiDB の SQL サービスに接続するときに、このパスを構成できます。
-   デフォルト値: `""`

### <code>tidb-key-path</code> {#code-tidb-key-path-code}

-   SSL秘密キーファイルのパス。 TLS を使用して TiDB の SQL サービスに接続するときに、このパスを構成できます。
-   デフォルト値: `""`

### <code>public-path-prefix</code> {#code-public-path-prefix-code}

-   TiDB ダッシュボードがリバース プロキシの背後でアクセスされる場合、この項目はすべての Web リソースのパブリック URL パス プレフィックスを設定します。
-   デフォルト値: `/dashboard`
-   リバース プロキシの背後以外で TiDB ダッシュボードにアクセスする場合は、この構成項目を変更し**ないで**ください。そうしないと、アクセスの問題が発生する可能性があります。詳細は[リバース プロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照してください。

### <code>enable-telemetry</code> {#code-enable-telemetry-code}

-   TiDB ダッシュボードでテレメトリ収集機能を有効にするかどうかを決定します。
-   デフォルト値: `false`
-   詳細については[テレメトリー](/telemetry.md)を参照してください。

## <code>replication-mode</code> {#code-replication-mode-code}

すべてのリージョンのレプリケーション モードに関連するコンフィグレーション項目。詳細については[DR 自動同期モードを有効にする](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)を参照してください。

## コントローラー {#controllor}

このセクションでは、PD for [リソース制御](/tidb-resource-control.md)に組み込まれる設定項目について説明します。

### <code>degraded-mode-wait-duration</code> {#code-degraded-mode-wait-duration-code}

-   劣化モードをトリガーするまでの待機時間。劣化モードとは、ローカル トークン バケット (LTB) とグローバル トークン バケット (GTB) が失われると、LTB がデフォルトのリソース グループ構成にフォールバックし、GTB 認証トークンがなくなることを意味します。これにより、サービスが影響を受けないようになります。ネットワークの分離または異常のイベント。
-   デフォルト値: 0
-   劣化モードはデフォルトでは無効になっています。

### <code>request-unit</code> {#code-request-unit-code}

[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru)に関する設定項目は以下のとおりです。

#### <code>read-base-cost</code> {#code-read-base-cost-code}

-   読み取りリクエストからRUへの変換の基本係数
-   デフォルト値: 0.25

#### <code>write-base-cost</code> {#code-write-base-cost-code}

-   書き込みリクエストからRUへの変換の基本要素
-   デフォルト値: 1

#### <code>read-cost-per-byte</code> {#code-read-cost-per-byte-code}

-   読み取りフローから RU への変換の基本係数
-   デフォルト値: 1/(64 * 1024)
-   1 RU = 64 KiB 読み取りバイト

#### <code>write-cost-per-byte</code> {#code-write-cost-per-byte-code}

-   書き込みフローから RU への変換の基本係数
-   デフォルト値: 1/1024
-   1 RU = 1 KiB 書き込みバイト

#### <code>read-cpu-ms-cost</code> {#code-read-cpu-ms-cost-code}

-   CPU から RU への変換の基本係数
-   デフォルト値: 1/3
-   1 RU = 3 ミリ秒の CPU 時間
