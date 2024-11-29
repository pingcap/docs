---
title: PD Configuration File
summary: PD 構成ファイルについて学習します。
---

# PDコンフィグレーションファイル {#pd-configuration-file}

<!-- markdownlint-disable MD001 -->

PD 構成ファイルは、コマンドライン パラメータよりも多くのオプションをサポートしています。デフォルトの構成ファイルは[ここ](https://github.com/pingcap/pd/blob/release-8.1/conf/config.toml)あります。

このドキュメントでは、コマンドライン パラメータに含まれないパラメータについてのみ説明します。コマンドライン パラメータについては[ここ](/command-line-flags-for-pd-configuration.md)確認してください。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>name</code> {#code-name-code}

-   PDノードの一意の名前
-   デフォルト値: `"pd"`
-   複数の PD ノードを起動するには、各ノードに一意の名前を使用します。

### <code>data-dir</code> {#code-data-dir-code}

-   PDがデータを保存するディレクトリ
-   デフォルト値: `default.${name}"`

### <code>client-urls</code> {#code-client-urls-code}

-   PDがリッスンするクライアントURLのリスト
-   デフォルト値: `"http://127.0.0.1:2379"`
-   クラスターをデプロイするときは、現在のホストの IP アドレスを`client-urls` (たとえば`"http://192.168.100.113:2379"` ) として指定する必要があります。クラスターが Docker 上で実行される場合は、Docker の IP アドレスを`"http://0.0.0.0:2379"`として指定します。

### <code>advertise-client-urls</code> {#code-advertise-client-urls-code}

-   クライアントがPDにアクセスするためのアドバタイズURLのリスト
-   デフォルト値: `"${client-urls}"`
-   Docker や NAT ネットワーク環境などの状況では、クライアントが PD がリッスンするデフォルトのクライアント URL を通じて PD にアクセスできない場合は、アドバタイズ クライアント URL を手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 2380:2380`に設定されています。この場合、 `advertise-client-urls` `"http://192.168.100.113:2380"`に設定できます。クライアントは`"http://192.168.100.113:2380"`を通じてこのサービスを見つけることができます。

### <code>peer-urls</code> {#code-peer-urls-code}

-   PDノードがリッスンするピアURLのリスト
-   デフォルト値: `"http://127.0.0.1:2380"`
-   クラスターをデプロイするときは、現在のホストの IP アドレスとして`peer-urls`指定する必要があります (例: `"http://192.168.100.113:2380"` 。クラスターが Docker 上で実行される場合は、Docker の IP アドレスを`"http://0.0.0.0:2380"`として指定します。

### <code>advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   他のPDノード（ピア）がPDノードにアクセスするためのアドバタイズURLのリスト
-   デフォルト: `"${peer-urls}"`
-   Docker または NAT ネットワーク環境などの状況では、他のノード (ピア) がこの PD ノードによってリッスンされるデフォルトのピア URL を介して PD ノードにアクセスできない場合は、アドバタイズ ピア URL を手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 2380:2380`に設定されています。この場合、 `advertise-peer-urls` `"http://192.168.100.113:2380"`に設定できます。他の PD ノードは`"http://192.168.100.113:2380"`を通じてこのサービスを見つけることができます。

### <code>initial-cluster</code> {#code-initial-cluster-code}

-   ブートストラップのための初期クラスタ構成
-   デフォルト値: `"{name}=http://{advertise-peer-url}"`
-   たとえば、 `name` 「pd」で、 `advertise-peer-urls`が`"http://192.168.100.113:2380"`の場合、 `initial-cluster` `"pd=http://192.168.100.113:2380"`なります。
-   3 つの PD サーバーを起動する必要がある場合、 `initial-cluster`は次のようになります。

        pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380

### <code>initial-cluster-state</code> {#code-initial-cluster-state-code}

-   クラスターの初期状態
-   デフォルト値: `"new"`

### <code>initial-cluster-token</code> {#code-initial-cluster-token-code}

-   ブートストラップフェーズ中に異なるクラスターを識別する
-   デフォルト値: `"pd-cluster"`
-   同じ構成のノードを持つ複数のクラスターが連続してデプロイされる場合は、異なるクラスター ノードを分離するために異なるトークンを指定する必要があります。

### <code>lease</code> {#code-lease-code}

-   PDLeaderキー リースのタイムアウト。タイムアウト後、システムはLeaderを再選出します。
-   デフォルト値: `3`
-   単位: 秒

### <code>quota-backend-bytes</code> {#code-quota-backend-bytes-code}

-   メタ情報データベースのstorageサイズはデフォルトで8GiBです
-   デフォルト値: `8589934592`

### <code>auto-compaction-mod</code> {#code-auto-compaction-mod-code}

-   メタ情報データベースの自動圧縮モード
-   使用可能なオプション: `periodic` (サイクル別) および`revision` (バージョン番号別)。
-   デフォルト値: `periodic`

### <code>auto-compaction-retention</code> {#code-auto-compaction-retention-code}

-   `auto-compaction-retention`の場合のメタ情報データベースの自動圧縮の時間間隔は`periodic`です。圧縮モードが`revision`に設定されている場合、このパラメータは自動圧縮のバージョン番号を示します。
-   デフォルト値: 1h

### <code>force-new-cluster</code> {#code-force-new-cluster-code}

-   PDを強制的に新しいクラスターとして起動し、 Raftメンバーの数を`1`に変更するかどうかを決定します。
-   デフォルト値: `false`

### <code>tso-update-physical-interval</code> {#code-tso-update-physical-interval-code}

-   PD が TSO の物理時間を更新する間隔。
-   TSO 物理時間のデフォルトの更新間隔では、PD は最大 262144 個の TSO を提供します。より多くの TSO を取得するには、この構成項目の値を減らすことができます。最小値は`1ms`です。
-   この設定項目を減らすと、PD の CPU 使用率が増加する可能性があります。テストによると、間隔が`50ms`の場合と比較して、間隔が`1ms`場合、PD の[CPU使用率](https://man7.org/linux/man-pages/man1/top.1.html)約 10% 増加します。
-   デフォルト値: `50ms`
-   最小値: `1ms`

## pdサーバー {#pd-server}

pd-serverに関連するコンフィグレーション項目

### <code>server-memory-limit</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-server-memory-limit-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用はお勧めしません。

-   PD インスタンスのメモリ制限比率。値`0`はメモリ制限がないことを意味します。
-   デフォルト値: `0`
-   最小値: `0`
-   最大値: `0.99`

### <code>server-memory-limit-gc-trigger</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-server-memory-limit-gc-trigger-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用はお勧めしません。

-   PD が GC をトリガーしようとするしきい値比率。PD のメモリ使用量が`server-memory-limit` * `server-memory-limit-gc-trigger`の値に達すると、PD はGolang GC をトリガーします。1 分間にトリガーされる GC は 1 つだけです。
-   デフォルト値: `0.7`
-   最小値: `0.5`
-   最大値: `0.99`

### <code>enable-gogc-tuner</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-enable-gogc-tuner-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用はお勧めしません。

-   GOGC チューナーを有効にするかどうかを制御します。
-   デフォルト値: `false`

### <code>gc-tuner-threshold</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-gc-tuner-threshold-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用はお勧めしません。

-   GOGC をチューニングするための最大メモリしきい値比。メモリがこのしきい値、つまり`server-memory-limit`の値 * `gc-tuner-threshold`の値を超えると、GOGC チューナーは動作を停止します。
-   デフォルト値: `0.6`
-   最小値: `0`
-   最大値: `0.9`

### <code>flow-round-by-digit</code> <span class="version-mark">TiDB 5.1 の新</span>機能 {#code-flow-round-by-digit-code-span-class-version-mark-new-in-tidb-5-1-span}

-   デフォルト値: 3
-   PD はフロー番号の最下位桁を丸め、リージョンフロー情報の変更によって発生する統計の更新を減らします。この設定項目は、リージョンフロー情報の丸める最下位桁の数を指定するために使用されます。たとえば、フロー`100512`デフォルト値が`3`であるため`101000`に丸められます。この設定は`trace-region-flow`置き​​換えます。

> **注記：**
>
> クラスターを TiDB 4.0 バージョンから現在のバージョンにアップグレードした場合、アップグレード後の`flow-round-by-digit`の動作とアップグレード前の`trace-region-flow`の動作はデフォルトで一貫しています。つまり、アップグレード前の`trace-region-flow`の値が false の場合、アップグレード後の`flow-round-by-digit`の値は 127 になります。アップグレード前の`trace-region-flow`の値が`true`の場合、アップグレード後の`flow-round-by-digit`の値は`3`なります。

### <code>min-resolved-ts-persistence-interval</code> <span class="version-mark">v6.0.0 の新機能</span> {#code-min-resolved-ts-persistence-interval-code-span-class-version-mark-new-in-v6-0-0-span}

-   最小の解決済みタイムスタンプが PD に永続化される間隔を決定します。この値が`0`に設定されている場合、永続化は無効であることを意味します。
-   デフォルト値: v6.3.0 より前では、デフォルト値は`"0s"`です。v6.3.0 以降では、デフォルト値は`"1s"`で、これは最小の正の値です。
-   最小値: `0`
-   単位: 秒

> **注記：**
>
> v6.0.0～v6.2.0 からアップグレードされたクラスターの場合、デフォルト値`min-resolved-ts-persistence-interval`はアップグレード後も変更されず、 `"0s"`ままになります。この機能を有効にするには、この構成項目の値を手動で変更する必要があります。

## 安全 {#security}

セキュリティに関するコンフィグレーション項目

### <code>cacert-path</code> {#code-cacert-path-code}

-   CAファイルのパス
-   デフォルト値: &quot;&quot;

### <code>cert-path</code> {#code-cert-path-code}

-   X509証明書を含むPrivacy Enhanced Mail (PEM)ファイルのパス
-   デフォルト値: &quot;&quot;

### <code>key-path</code> {#code-key-path-code}

-   X509キーを含むPEMファイルのパス
-   デフォルト値: &quot;&quot;

### <code>redact-info-log</code> <span class="version-mark">v5.0 の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v5-0-span}

-   PDログでログ編集を有効にするかどうかを制御します
-   構成値を`true`に設定すると、PD ログでユーザー データが編集されます。
-   デフォルト値: `false`

## <code>log</code> {#code-log-code}

ログに関するコンフィグレーション項目

### <code>level</code> {#code-level-code}

-   出力ログのレベルを指定します
-   `"error"` `"fatal"` `"warn"` `"debug"` `"info"`
-   デフォルト値: `"info"`

### <code>format</code> {#code-format-code}

-   ログ形式
-   オプション値: `"text"` 、 `"json"`
-   デフォルト値: `"text"`

### <code>disable-timestamp</code> {#code-disable-timestamp-code}

-   ログ内の自動生成されたタイムスタンプを無効にするかどうか
-   デフォルト値: `false`

## <code>log.file</code> {#code-log-file-code}

ログファイルに関するコンフィグレーション項目

### <code>max-size</code> {#code-max-size-code}

-   1 つのログ ファイルの最大サイズ。この値を超えると、システムは自動的にログを複数のファイルに分割します。
-   デフォルト値: `300`
-   単位: MiB
-   最小値: `1`

### <code>max-days</code> {#code-max-days-code}

-   ログが保存される最大日数
-   構成項目が設定されていない場合、またはその値がデフォルト値 0 に設定されている場合、PD はログ ファイルをクリーンアップしません。
-   デフォルト値: `0`

### <code>max-backups</code> {#code-max-backups-code}

-   保存するログファイルの最大数
-   構成項目が設定されていない場合、またはその値がデフォルト値 0 に設定されている場合、PD はすべてのログ ファイルを保持します。
-   デフォルト値: `0`

## <code>metric</code> {#code-metric-code}

監視に関するコンフィグレーション項目

### <code>interval</code> {#code-interval-code}

-   監視メトリックデータがPrometheusにプッシュされる間隔
-   デフォルト値: `15s`

## <code>schedule</code> {#code-schedule-code}

スケジュールに関連するコンフィグレーション項目

> **注記：**
>
> `schedule`に関連するこれらの PD 構成項目を変更するには、クラスターのステータスに基づいて次のいずれかの方法を選択します。
>
> -   新しくデプロイするクラスターの場合は、PD 構成ファイルを直接変更できます。
> -   既存のクラスターの場合は、代わりにコマンドライン ツール[PD Control](/pd-control.md)を使用して変更を加えます。構成ファイル内の`schedule`に関連するこれらの PD 構成項目を直接変更しても、既存のクラスターには反映されません。

### <code>max-merge-region-size</code> {#code-max-merge-region-size-code}

-   `Region Merge`のサイズ制限を制御します。リージョンのサイズが指定された値より大きい場合、PD はリージョンを隣接する領域と結合しません。
-   デフォルト値: `20`
-   単位: MiB

### <code>max-merge-region-keys</code> {#code-max-merge-region-keys-code}

-   `Region Merge`キーの上限を指定します。リージョンキーが指定された値より大きい場合、PD はリージョンを隣接するリージョンと結合しません。
-   デフォルト値: `200000`

### <code>patrol-region-interval</code> {#code-patrol-region-interval-code}

-   `replicaChecker`リージョンのヘルス状態をチェックする実行頻度を制御します。この値が小さいほど、 `replicaChecker`実行が速くなります。通常、このパラメータを調整する必要はありません。
-   デフォルト値: `10ms`

### <code>split-merge-interval</code> {#code-split-merge-interval-code}

-   同じリージョンでの`split`の操作と`merge`操作の間の時間間隔を制御します。つまり、新しく分割されたリージョンはしばらくは結合されません。
-   デフォルト値: `1h`

### <code>max-snapshot-count</code> {#code-max-snapshot-count-code}

-   1 つのストアが同時に受信または送信するスナップショットの最大数を制御します。PD スケジューラは、通常のトラフィックに使用されるリソースがプリエンプトされるのを防ぐためにこの構成に依存します。
-   デフォルト値: `64`

### <code>max-pending-peer-count</code> {#code-max-pending-peer-count-code}

-   単一ストア内の保留中のピアの最大数を制御します。PD スケジューラは、一部のノードで古いログを持つリージョンが大量に生成されるのを防ぐために、この構成に依存しています。
-   デフォルト値: `64`

### <code>max-store-down-time</code> {#code-max-store-down-time-code}

-   切断されたストアを回復できないと PD が判断するまでのダウンタイム。指定された期間内にストアからのハートビートを受信できない場合、PD は他のノードにレプリカを追加します。
-   デフォルト値: `30m`

### <code>max-store-preparing-time</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-max-store-preparing-time-code-span-class-version-mark-new-in-v6-1-0-span}

-   ストアがオンラインになるまでの最大待機時間を制御します。ストアのオンライン段階では、PD はストアのオンライン進行状況を照会できます。指定された時間を超えると、PD はストアがオンラインになったと想定し、ストアのオンライン進行状況を再度照会できなくなります。ただし、これによってリージョンが新しいオンライン ストアに転送されることが防止されるわけではありません。ほとんどのシナリオでは、このパラメータを調整する必要はありません。
-   デフォルト値: `48h`

### <code>leader-schedule-limit</code> {#code-leader-schedule-limit-code}

-   同時に実行されるLeaderスケジュールタスクの数
-   デフォルト値: `4`

### <code>region-schedule-limit</code> {#code-region-schedule-limit-code}

-   同時に実行されるリージョンスケジュールタスクの数
-   デフォルト値: `2048`

### <code>enable-diagnostic</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-enable-diagnostic-code-span-class-version-mark-new-in-v6-3-0-span}

-   診断機能を有効にするかどうかを制御します。有効にすると、PD は診断に役立つようにスケジュール中の状態を記録します。有効にすると、スケジュール速度に若干影響し、ストアの数が多い場合にメモリ消費量が増える可能性があります。
-   デフォルト値: v7.1.0 以降では、デフォルト値が`false`から`true`に変更されます。クラスターが v7.1.0 より前のバージョンから v7.1.0 以降にアップグレードされた場合、デフォルト値は変更されません。

### <code>hot-region-schedule-limit</code> {#code-hot-region-schedule-limit-code}

-   同時に実行されているホットなリージョンスケジューリング タスクを制御します。これはリージョンスケジューリングとは独立しています。
-   デフォルト値: `4`

### <code>hot-region-cache-hits-threshold</code> {#code-hot-region-cache-hits-threshold-code}

-   ホットリージョンを識別するために必要な分数を設定するために使用されるしきい値。PD は、リージョンがこの分数を超えてホット スポット状態になった後にのみ、ホット スポット スケジューリングに参加できます。
-   デフォルト値: `3`

### <code>replica-schedule-limit</code> {#code-replica-schedule-limit-code}

-   同時に実行されるレプリカ スケジューリング タスクの数
-   デフォルト値: `64`

### <code>merge-schedule-limit</code> {#code-merge-schedule-limit-code}

-   同時に実行される`Region Merge`スケジュール タスクの数`Region Merge`無効にするには、このパラメーターを`0`に設定します。
-   デフォルト値: `8`

### <code>high-space-ratio</code> {#code-high-space-ratio-code}

-   ストアの容量が十分であるしきい値比率。ストアのスペース占有率がこのしきい値より小さい場合、PD はスケジュールを実行するときにストアの残りのスペースを無視し、主にリージョンサイズに基づいて負荷を分散します。この構成は、 `region-score-formula-version` `v1`に設定されている場合にのみ有効になります。
-   デフォルト値: `0.7`
-   最小値: `0`より大きい
-   最大値: `1`未満

### <code>low-space-ratio</code> {#code-low-space-ratio-code}

-   ストアの容量が不足するしきい値比率。ストアのスペース占有率がこのしきい値を超えると、PD はこのストアへのデータの移行を可能な限り回避します。一方、PD は、対応するストアのディスク容量が枯渇することを回避するために、主にストアの残り容量に基づいてスケジュールを実行します。
-   デフォルト値: `0.8`
-   最小値: `0`より大きい
-   最大値: `1`未満

### <code>tolerant-size-ratio</code> {#code-tolerant-size-ratio-code}

-   `balance`バッファサイズを制御します
-   デフォルト値: `0` (バッファサイズを自動的に調整します)
-   最小値: `0`

### <code>enable-cross-table-merge</code> {#code-enable-cross-table-merge-code}

-   クロステーブル領域の結合を有効にするかどうかを決定します
-   デフォルト値: `true`

### <code>region-score-formula-version</code> <span class="version-mark">v5.0 の新機能</span> {#code-region-score-formula-version-code-span-class-version-mark-new-in-v5-0-span}

-   リージョンスコアの計算式のバージョンを制御します
-   デフォルト値: `v2`
-   オプションの値: `v1`と`v2`と比較すると、v2 の変更はよりスムーズになり、スペースの再利用によって発生するスケジュールのジッターが改善されます。

> **注記：**
>
> クラスターを TiDB 4.0 バージョンから現在のバージョンにアップグレードした場合、アップグレード前後の PD 動作の一貫性を確保するために、新しい数式バージョンはデフォルトで自動的に無効になります。数式バージョンを変更する場合は、 `pd-ctl`設定を手動で切り替える必要があります。詳細については、 [PD Control](/pd-control.md#config-show--set-option-value--placement-rules)を参照してください。

### <code>store-limit-version</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-store-limit-version-code-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> この構成項目を`"v2"`に設定するのは実験的機能です。本番環境での使用はお勧めしません。

-   店舗制限の計算式のバージョンを制御します
-   デフォルト値: `v1`
-   値のオプション:
    -   `v1` : v1 モードでは、 `store limit`を手動で変更して、単一の TiKV のスケジュール速度を制限できます。
    -   `v2` : (実験的機能 ) v2 モードでは、PD が TiKV スナップショットの機能に基づいて動的に調整するため、 `store limit`値を手動で設定する必要はありません。詳細については、 [ストア制限の原則 v2](/configure-store-limit.md#principles-of-store-limit-v2)を参照してください。

### <code>enable-joint-consensus</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-joint-consensus-code-span-class-version-mark-new-in-v5-0-span}

-   レプリカのスケジュールに Joint Consensus を使用するかどうかを制御します。この構成が無効になっている場合、PD は一度に 1 つのレプリカをスケジュールします。
-   デフォルト値: `true`

### <code>hot-regions-write-interval</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-hot-regions-write-interval-code-span-class-version-mark-new-in-v5-4-0-span}

-   PD がホットリージョン情報を保存する時間間隔。
-   デフォルト値: `10m`

> **注記：**
>
> ホット リージョンに関する情報は 3 分ごとに更新されます。間隔を 3 分未満に設定すると、間隔中の更新は意味をなさない可能性があります。

### <code>hot-regions-reserved-days</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-hot-regions-reserved-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   ホットリージョン情報を保持する日数を指定します。
-   デフォルト値: `7`

## <code>replication</code> {#code-replication-code}

レプリカに関連するコンフィグレーション項目

### <code>max-replicas</code> {#code-max-replicas-code}

-   レプリカの数、つまりリーダーとフォロワーの数の合計。デフォルト値`3`は、リーダー 1 台とフォロワー 2 台を意味します。この構成が動的に変更されると、PD は、レプリカの数がこの構成と一致するようにバックグラウンドでリージョンをスケジュールします。
-   デフォルト値: `3`

### <code>location-labels</code> {#code-location-labels-code}

-   TiKVクラスタのトポロジ情報
-   デフォルト値: `[]`
-   [クラスタトポロジ構成](/schedule-replicas-by-topology-labels.md)

### <code>isolation-level</code> {#code-isolation-level-code}

-   TiKVクラスタの最小トポロジカル分離レベル
-   デフォルト値: `""`
-   [クラスタトポロジ構成](/schedule-replicas-by-topology-labels.md)

### <code>strictly-match-label</code> {#code-strictly-match-label-code}

-   TiKV ラベルが PD `location-labels`と一致するかどうかを厳密にチェックできるようにします。
-   デフォルト値: `false`

### <code>enable-placement-rules</code> {#code-enable-placement-rules-code}

-   `placement-rules`を有効にします。
-   デフォルト値: `true`
-   [配置ルール](/configure-placement-rules.md)参照。

## <code>label-property</code> (非推奨) {#code-label-property-code-deprecated}

ラベルに関連するコンフィグレーション項目`reject-leader`種類のみをサポートします。

> **注記：**
>
> v5.2 以降では、ラベルに関連する設定項目は非推奨になりました。レプリカ ポリシーを設定するには、 [配置ルール](/configure-placement-rules.md#scenario-2-place-five-replicas-in-three-data-centers-in-the-proportion-of-221-and-the-leader-should-not-be-in-the-third-data-center)使用することをお勧めします。

### <code>key</code> （非推奨） {#code-key-code-deprecated}

-   Leaderを拒否したストアのラベルキー
-   デフォルト値: `""`

### <code>value</code> (非推奨) {#code-value-code-deprecated}

-   Leaderを拒否した店舗のラベル値
-   デフォルト値: `""`

## <code>dashboard</code> {#code-dashboard-code}

[TiDBダッシュボード](/dashboard/dashboard-intro.md)内蔵 PD に関するコンフィグレーション項目です。

### <code>tidb-cacert-path</code> {#code-tidb-cacert-path-code}

-   ルート CA 証明書ファイルのパス。TLS を使用して TiDB の SQL サービスに接続するときに、このパスを構成できます。
-   デフォルト値: `""`

### <code>tidb-cert-path</code> {#code-tidb-cert-path-code}

-   SSL 証明書ファイルのパス。TLS を使用して TiDB の SQL サービスに接続するときに、このパスを構成できます。
-   デフォルト値: `""`

### <code>tidb-key-path</code> {#code-tidb-key-path-code}

-   SSL 秘密キー ファイルのパス。TLS を使用して TiDB の SQL サービスに接続するときに、このパスを構成できます。
-   デフォルト値: `""`

### <code>public-path-prefix</code> {#code-public-path-prefix-code}

-   TiDB ダッシュボードがリバース プロキシの背後でアクセスされる場合、この項目はすべての Web リソースのパブリック URL パス プレフィックスを設定します。
-   デフォルト値: `/dashboard`
-   TiDB ダッシュボードがリバース プロキシを経由せずにアクセスされる場合は、この構成項目を変更し**ないで**ください。変更すると、アクセスの問題が発生する可能性があります。詳細については[リバースプロキシの背後でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照してください。

### <code>enable-telemetry</code> {#code-enable-telemetry-code}

> **警告：**
>
> v8.1.0 以降では、TiDB ダッシュボードのテレメトリ機能が削除され、この構成項目は機能しなくなりました。これは、以前のバージョンとの互換性のためだけに保持されています。

-   v8.1.0 より前では、この構成項目は TiDB ダッシュボードでテレメトリ収集を有効にするかどうかを制御します。
-   デフォルト値: `false`

## <code>replication-mode</code> {#code-replication-mode-code}

全リージョンのレプリケーションモードに関するコンフィグレーション項目です。詳細は[DR自動同期モードを有効にする](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)参照してください。

## コントローラ {#controller}

このセクションでは、 PD for [リソース管理](/tidb-resource-control.md)に組み込まれている構成項目について説明します。

### <code>degraded-mode-wait-duration</code> {#code-degraded-mode-wait-duration-code}

-   劣化モードをトリガーするまでの待機時間。劣化モードとは、ローカル トークン バケット (LTB) とグローバル トークン バケット (GTB) が失われた場合に、LTB がデフォルトのリソース グループ構成にフォールバックし、GTB 認証トークンがなくなるため、ネットワークの分離や異常が発生した場合でもサービスが影響を受けないことが保証されることを意味します。
-   デフォルト値: 0秒
-   デフォルトでは、劣化モードは無効になっています。

### <code>request-unit</code> {#code-request-unit-code}

[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru)に関する設定項目は以下のとおりです。

#### <code>read-base-cost</code> {#code-read-base-cost-code}

-   読み取り要求から RU への変換の基礎係数
-   デフォルト値: 0.25

#### <code>write-base-cost</code> {#code-write-base-cost-code}

-   書き込み要求からRUへの変換の基礎係数
-   デフォルト値: 1

#### <code>read-cost-per-byte</code> {#code-read-cost-per-byte-code}

-   読み取りフローからRUへの変換の基礎係数
-   デフォルト値: 1/(64 * 1024)
-   1 RU = 64 KiB 読み取りバイト

#### <code>write-cost-per-byte</code> {#code-write-cost-per-byte-code}

-   書き込みフローからRUへの変換の基礎係数
-   デフォルト値: 1/1024
-   1 RU = 1 KiB 書き込みバイト

#### <code>read-cpu-ms-cost</code> {#code-read-cpu-ms-cost-code}

-   CPUからRUへの変換の基礎係数
-   デフォルト値: 1/3
-   1 RU = 3 ミリ秒の CPU 時間
