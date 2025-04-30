---
title: PD Configuration File
summary: PD 構成ファイルについて学習します。
---

# PDコンフィグレーションファイル {#pd-configuration-file}

<!-- markdownlint-disable MD001 -->

PD設定ファイルは、コマンドラインパラメータよりも多くのオプションをサポートしています。デフォルトの設定ファイルは[ここ](https://github.com/pingcap/pd/blob/release-8.1/conf/config.toml)あります。

このドキュメントでは、コマンドラインパラメータに含まれないパラメータについてのみ説明します。コマンドラインパラメータについては、 [ここ](/command-line-flags-for-pd-configuration.md)参照してください。

> **ヒント：**
>
> 構成項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>name</code> {#code-name-code}

-   PDノードの一意の名前
-   デフォルト値: `"pd"`
-   複数の PD ノードを開始するには、各ノードに一意の名前を使用します。

### <code>data-dir</code> {#code-data-dir-code}

-   PDがデータを保存するディレクトリ
-   デフォルト値: `default.${name}"`

### <code>client-urls</code> {#code-client-urls-code}

-   PDがリッスンするクライアントURLのリスト
-   デフォルト値: `"http://127.0.0.1:2379"`
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`client-urls` （例： `"http://192.168.100.113:2379"` ）に指定する必要があります。クラスターをDocker上で実行する場合は、DockerのIPアドレスを`"http://0.0.0.0:2379"`に指定してください。

### <code>advertise-client-urls</code> {#code-advertise-client-urls-code}

-   クライアントがPDにアクセスするためのアドバタイズURLのリスト
-   デフォルト値: `"${client-urls}"`
-   Docker または NAT ネットワーク環境などの状況では、クライアントが PD がリッスンするデフォルトのクライアント URL を通じて PD にアクセスできない場合は、アドバタイズ クライアント URL を手動で設定する必要があります。
-   例えば、Dockerの内部IPアドレスは`172.17.0.1` 、ホストのIPアドレスは`192.168.100.113` 、ポートマッピングは`-p 2380:2380`に設定されています。この場合、 `advertise-client-urls`を`"http://192.168.100.113:2380"`に設定できます。クライアントは`"http://192.168.100.113:2380"`を通じてこのサービスを見つけられます。

### <code>peer-urls</code> {#code-peer-urls-code}

-   PDノードがリッスンするピアURLのリスト
-   デフォルト値: `"http://127.0.0.1:2380"`
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`peer-urls` （例： `"http://192.168.100.113:2380"`に指定する必要があります。クラスターがDocker上で実行される場合は、DockerのIPアドレスを`"http://0.0.0.0:2380"`に指定してください。

### <code>advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   他のPDノード（ピア）がPDノードにアクセスするためのアドバタイズURLのリスト
-   デフォルト: `"${peer-urls}"`
-   Docker または NAT ネットワーク環境などの状況では、他のノード (ピア) がこの PD ノードによってリッスンされるデフォルトのピア URL を介して PD ノードにアクセスできない場合は、アドバタイズ ピア URL を手動で設定する必要があります。
-   例えば、Dockerの内部IPアドレスが`172.17.0.1`で、ホストのIPアドレスが`192.168.100.113` 、ポートマッピングが`-p 2380:2380`に設定されている場合、 `advertise-peer-urls`を`"http://192.168.100.113:2380"`に設定できます。他のPDノードは`"http://192.168.100.113:2380"`を介してこのサービスを検出できます。

### <code>initial-cluster</code> {#code-initial-cluster-code}

-   ブートストラップのための初期クラスタ構成
-   デフォルト値: `"{name}=http://{advertise-peer-url}"`
-   たとえば、 `name`が「pd」、 `advertise-peer-urls`が`"http://192.168.100.113:2380"`の場合、 `initial-cluster`は`"pd=http://192.168.100.113:2380"`なります。
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

-   PDLeaderキーリースのタイムアウト。タイムアウト後、システムはLeaderを再選出します。
-   デフォルト値: `3`
-   単位：秒

### <code>quota-backend-bytes</code> {#code-quota-backend-bytes-code}

-   メタ情報データベースのstorageサイズ（デフォルトでは8GiB）
-   デフォルト値: `8589934592`

### <code>auto-compaction-mod</code> {#code-auto-compaction-mod-code}

-   メタ情報データベースの自動圧縮モード
-   使用可能なオプション: `periodic` (サイクル別) および`revision` (バージョン番号別)。
-   デフォルト値: `periodic`

### <code>auto-compaction-retention</code> {#code-auto-compaction-retention-code}

-   `auto-compaction-retention`が`periodic`場合、メタ情報データベースの自動圧縮間隔。圧縮モードが`revision`に設定されている場合、このパラメータは自動圧縮のバージョン番号を示します。
-   デフォルト値: 1時間

### <code>force-new-cluster</code> {#code-force-new-cluster-code}

-   PDを強制的に新しいクラスタとして起動し、 Raftメンバーの数を`1`に変更するかどうかを決定します。
-   デフォルト値: `false`

### <code>tso-update-physical-interval</code> {#code-tso-update-physical-interval-code}

-   PD が TSO の物理時間を更新する間隔。
-   TSO物理時間のデフォルトの更新間隔では、PDは最大262144個のTSOを提供します。より多くのTSOを取得するには、この設定項目の値を減らしてください。最小値は`1ms`です。
-   この設定項目を減らすと、PDのCPU使用率が増加する可能性があります。テストによると、間隔が`50ms`の場合と比較して、間隔が`1ms`の場合、PDのCPU [CPU使用率](https://man7.org/linux/man-pages/man1/top.1.html)で約10%増加します。
-   デフォルト値: `50ms`
-   最小値: `1ms`

## pdサーバー {#pd-server}

pd-server関連のコンフィグレーション項目

### <code>server-memory-limit</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-server-memory-limit-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   PDインスタンスのメモリ制限比率。値`0`メモリ制限がないことを意味します。
-   デフォルト値: `0`
-   最小値: `0`
-   最大値: `0.99`

### <code>server-memory-limit-gc-trigger</code> <span class="version-mark">v6.6.0の新機能</span> {#code-server-memory-limit-gc-trigger-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   PDがGCをトリガーしようとする閾値比率。PDのメモリ使用量が`server-memory-limit` × `server-memory-limit-gc-trigger`の値に達すると、PDはGolang GCをトリガーします。1分間にトリガーされるGCは1回のみです。
-   デフォルト値: `0.7`
-   最小値: `0.5`
-   最大値: `0.99`

### <code>enable-gogc-tuner</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-enable-gogc-tuner-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   GOGC チューナーを有効にするかどうかを制御します。
-   デフォルト値: `false`

### <code>gc-tuner-threshold</code> <span class="version-mark">6.6.0の新機能</span> {#code-gc-tuner-threshold-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> この設定は実験的機能です。本番環境での使用は推奨されません。

-   GOGCチューナーのチューニングにおける最大メモリしきい値比。メモリがこのしきい値`server-memory-limit` × `gc-tuner-threshold` ）を超えると、GOGCチューナーは動作を停止します。
-   デフォルト値: `0.6`
-   最小値: `0`
-   最大値: `0.9`

### <code>flow-round-by-digit</code> <span class="version-mark">TiDB 5.1 の新機能</span> {#code-flow-round-by-digit-code-span-class-version-mark-new-in-tidb-5-1-span}

-   デフォルト値: 3
-   PDはフロー番号の最下位桁を丸めることで、リージョンフロー情報の変更に伴う統計情報の更新を削減します。この設定項目は、リージョンフロー情報の最小桁数を指定します。例えば、フロー`100512`デフォルト値が`3`であるため、 `101000`に丸められます。この設定により、 `trace-region-flow`置き換えられます。

> **注記：**
>
> クラスターをTiDB 4.0バージョンから現在のバージョンにアップグレードした場合、アップグレード後の`flow-round-by-digit`の動作とアップグレード前の`trace-region-flow`の動作はデフォルトで一致します。つまり、アップグレード前の`trace-region-flow`の値がfalseの場合、アップグレード後の`flow-round-by-digit`の値は127になります。アップグレード前の`trace-region-flow`の値が`true`の場合、アップグレード後の`flow-round-by-digit`の値は`3`なります。

### <code>min-resolved-ts-persistence-interval</code><span class="version-mark">バージョン6.0.0の新機能</span> {#code-min-resolved-ts-persistence-interval-code-span-class-version-mark-new-in-v6-0-0-span}

-   PDに最小解決タイムスタンプが保持される間隔を決定します。この値が`0`に設定されている場合、保持は無効になります。
-   デフォルト値: v6.3.0 より前のバージョンでは、デフォルト値は`"0s"`です。v6.3.0 以降では、デフォルト値は`"1s"` （最小の正の値）です。
-   最小値: `0`
-   単位：秒

> **注記：**
>
> v6.0.0～v6.2.0からアップグレードされたクラスターの場合、デフォルト値の`min-resolved-ts-persistence-interval`アップグレード後も変更されず、 `"0s"`ままとなります。この機能を有効にするには、この設定項目の値を手動で変更する必要があります。

## 安全 {#security}

セキュリティ関連のコンフィグレーション項目

### <code>cacert-path</code> {#code-cacert-path-code}

-   CAファイルのパス
-   デフォルト値: &quot;&quot;

### <code>cert-path</code> {#code-cert-path-code}

-   X509証明書を含むPrivacy Enhanced Mail（PEM）ファイルのパス
-   デフォルト値: &quot;&quot;

### <code>key-path</code> {#code-key-path-code}

-   X509キーを含むPEMファイルのパス
-   デフォルト値: &quot;&quot;

### <code>redact-info-log</code><span class="version-mark">バージョン5.0の新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v5-0-span}

-   PDログでログ編集を有効にするかどうかを制御します
-   構成値を`true`に設定すると、PD ログでユーザー データが編集されます。
-   デフォルト値: `false`

## <code>log</code> {#code-log-code}

ログ関連のコンフィグレーション項目

### <code>level</code> {#code-level-code}

-   出力ログのレベルを指定します
-   `"warn"` `"fatal"` `"error"` `"debug"` `"info"`
-   デフォルト値: `"info"`

### <code>format</code> {#code-format-code}

-   ログ形式
-   オプション`"json"` : `"text"`
-   デフォルト値: `"text"`

### <code>disable-timestamp</code> {#code-disable-timestamp-code}

-   ログ内の自動生成されたタイムスタンプを無効にするかどうか
-   デフォルト値: `false`

## <code>log.file</code> {#code-log-file-code}

ログファイルに関連するコンフィグレーション項目

### <code>max-size</code> {#code-max-size-code}

-   1つのログファイルの最大サイズ。この値を超えると、システムは自動的にログを複数のファイルに分割します。
-   デフォルト値: `300`
-   単位: MiB
-   最小値: `1`

### <code>max-days</code> {#code-max-days-code}

-   ログが保存される最大日数
-   構成項目が設定されていない場合、またはその値がデフォルト値 0 に設定されている場合、PD はログ ファイルを消去しません。
-   デフォルト値: `0`

### <code>max-backups</code> {#code-max-backups-code}

-   保存するログファイルの最大数
-   構成項目が設定されていない場合、またはその値がデフォルト値 0 に設定されている場合、PD はすべてのログ ファイルを保持します。
-   デフォルト値: `0`

## <code>metric</code> {#code-metric-code}

監視に関連するコンフィグレーション項目

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
> -   既存のクラスターの場合は、コマンドラインツール[PD Control](/pd-control.md)を使用して変更を加えてください。設定ファイル内の`schedule`に関連するPD設定項目を直接変更しても、既存のクラスターには反映されません。

### <code>max-merge-region-size</code> {#code-max-merge-region-size-code}

-   サイズ制限を`Region Merge`に制御します。リージョンサイズが指定された値より大きい場合、PD はリージョンを隣接する領域と結合しません。
-   デフォルト値: `20`
-   単位: MiB

### <code>max-merge-region-keys</code> {#code-max-merge-region-keys-code}

-   `Region Merge`キーの上限を指定します。リージョンキーが指定された値より大きい場合、PDはリージョンを隣接するリージョンと結合しません。
-   デフォルト値: `200000`

### <code>patrol-region-interval</code> {#code-patrol-region-interval-code}

-   `replicaChecker` リージョンのヘルス状態をチェックする実行頻度を制御します。この値が小さいほど、 `replicaChecker`実行速度が速くなります。通常、このパラメータを調整する必要はありません。
-   デフォルト値: `10ms`

### <code>split-merge-interval</code> {#code-split-merge-interval-code}

-   同じリージョンにおける`split`の操作と`merge`操作間の時間間隔を制御します。つまり、新しく分割されたリージョンはしばらくの間マージされません。
-   デフォルト値: `1h`

### <code>max-snapshot-count</code> {#code-max-snapshot-count-code}

-   1 つのストアが同時に受信または送信するスナップショットの最大数を制御します。PD スケジューラは、この構成に依存して、通常のトラフィックに使用されるリソースがプリエンプトされるのを防ぎます。
-   デフォルト値: `64`

### <code>max-pending-peer-count</code> {#code-max-pending-peer-count-code}

-   単一ストア内の保留中のピアの最大数を制御します。PD スケジューラはこの構成に依存して、一部のノードで古いログを持つリージョンが過剰に生成されるのを防ぎます。
-   デフォルト値: `64`

### <code>max-store-down-time</code> {#code-max-store-down-time-code}

-   PDが切断されたストアを復旧不可能と判断するまでのダウンタイム。指定された時間内にストアからのハートビートを受信できない場合、PDは他のノードにレプリカを追加します。
-   デフォルト値: `30m`

### <code>max-store-preparing-time</code><span class="version-mark">バージョン6.1.0の新機能</span> {#code-max-store-preparing-time-code-span-class-version-mark-new-in-v6-1-0-span}

-   ストアがオンラインになるまでの最大待機時間を制御します。ストアがオンライン段階にある間、PDはストアのオンライン進行状況を照会できます。指定された時間を超えると、PDはストアがオンラインになったとみなし、再度ストアのオンライン進行状況を照会できなくなります。ただし、これによってリージョンが新しいオンラインストアに移行できなくなるわけではありません。ほとんどの場合、このパラメータを調整する必要はありません。
-   デフォルト値: `48h`

### <code>leader-schedule-limit</code> {#code-leader-schedule-limit-code}

-   同時に実行されるLeaderスケジュールタスクの数
-   デフォルト値: `4`

### <code>region-schedule-limit</code> {#code-region-schedule-limit-code}

-   同時に実行されるリージョンスケジュールタスクの数
-   デフォルト値: `2048`

### <code>enable-diagnostic</code><span class="version-mark">バージョン6.3.0の新機能</span> {#code-enable-diagnostic-code-span-class-version-mark-new-in-v6-3-0-span}

-   診断機能を有効にするかどうかを制御します。有効にすると、PDは診断を支援するためにスケジューリング中の状態を記録します。有効にすると、スケジューリング速度に若干影響し、ストア数が多い場合にメモリ消費量が増加する可能性があります。
-   デフォルト値: バージョン7.1.0以降、デフォルト値は`false`から`true`に変更されます。クラスターをバージョン7.1.0より前のバージョンからバージョン7.1.0以降にアップグレードした場合、デフォルト値は変更されません。

### <code>hot-region-schedule-limit</code> {#code-hot-region-schedule-limit-code}

-   同時に実行されているホットなリージョンスケジューリングタスクを制御します。リージョンスケジューリングとは独立しています。
-   デフォルト値: `4`

### <code>hot-region-cache-hits-threshold</code> {#code-hot-region-cache-hits-threshold-code}

-   ホットリージョンを識別するために必要な分数を設定するために使用されるしきい値。PD は、リージョンがこの分数を超えてホットスポット状態になった後にのみ、ホットスポット スケジューリングに参加できます。
-   デフォルト値: `3`

### <code>replica-schedule-limit</code> {#code-replica-schedule-limit-code}

-   同時に実行されるレプリカスケジュールタスクの数
-   デフォルト値: `64`

### <code>merge-schedule-limit</code> {#code-merge-schedule-limit-code}

-   同時に実行される`Region Merge`スケジュールタスクの数`Region Merge`を無効にするには、このパラメータを`0`に設定します。
-   デフォルト値: `8`

### <code>high-space-ratio</code> {#code-high-space-ratio-code}

-   ストアの容量が十分であることを示す閾値比率。ストアのスペース占有率がこの閾値を下回る場合、PDはスケジューリング時にストアの残りのスペースを無視し、主にリージョンサイズに基づいて負荷分散を行います。この設定は、 `region-score-formula-version` `v1`に設定した場合のみ有効です。
-   デフォルト値: `0.7`
-   最小値: `0`より大きい
-   最大値: `1`未満

### <code>low-space-ratio</code> {#code-low-space-ratio-code}

-   ストアの容量が不足する閾値比率。ストアのスペース占有率がこの閾値を超えると、PDはこのストアへのデータ移行を可能な限り回避します。同時に、該当ストアのディスク容量が枯渇することを避けるため、PDは主にストアの残容量に基づいてスケジューリングを行います。
-   デフォルト値: `0.8`
-   最小値: `0`より大きい
-   最大値: `1`未満

### <code>tolerant-size-ratio</code> {#code-tolerant-size-ratio-code}

-   `balance`バッファサイズを制御します
-   デフォルト値: `0` (バッファサイズを自動調整)
-   最小値: `0`

### <code>enable-cross-table-merge</code> {#code-enable-cross-table-merge-code}

-   クロステーブル領域の結合を有効にするかどうかを決定します
-   デフォルト値: `true`

### <code>region-score-formula-version</code> <span class="version-mark">v5.0 の新機能</span> {#code-region-score-formula-version-code-span-class-version-mark-new-in-v5-0-span}

-   リージョンスコアの計算式のバージョンを制御します
-   デフォルト値: `v2`
-   オプション値: `v1`および`v2`と比較して、v2 の変更はよりスムーズになり、スペースの再利用によって発生するスケジュールのジッターが改善されています。

> **注記：**
>
> クラスターをTiDB 4.0バージョンから最新バージョンにアップグレードした場合、アップグレード前後のPD動作の一貫性を確保するため、新しいFormulaバージョンはデフォルトで自動的に無効化されます。Formulaバージョンを変更する場合は、 `pd-ctl`設定を手動で切り替える必要があります。詳細は[PD Control](/pd-control.md#config-show--set-option-value--placement-rules)を参照してください。

### <code>store-limit-version</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-store-limit-version-code-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> この設定項目を`"v2"`に設定するのは実験的機能です。本番環境での使用は推奨されません。

-   店舗制限の計算式のバージョンを制御します
-   デフォルト値: `v1`
-   値のオプション:
    -   `v1` : v1 モードでは、 `store limit`手動で変更して、単一の TiKV のスケジュール速度を制限できます。
    -   `v2` : (実験的機能) v2モードでは、PDがTiKVスナップショットの機能に基づいて動的に調整するため、 `store limit`値を手動で設定する必要はありません。詳細については、 [店舗制限の原則 v2](/configure-store-limit.md#principles-of-store-limit-v2)を参照してください。

### <code>enable-joint-consensus</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-joint-consensus-code-span-class-version-mark-new-in-v5-0-span}

-   レプリカのスケジュール設定にジョイントコンセンサスを使用するかどうかを制御します。この設定が無効になっている場合、PDは一度に1つのレプリカをスケジュールします。
-   デフォルト値: `true`

### <code>hot-regions-write-interval</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-hot-regions-write-interval-code-span-class-version-mark-new-in-v5-4-0-span}

-   PD がホットリージョン情報を保存する時間間隔。
-   デフォルト値: `10m`

> **注記：**
>
> ホットリージョンに関する情報は3分ごとに更新されます。更新間隔を3分未満に設定した場合、更新間隔中の更新は意味をなさない可能性があります。

### <code>hot-regions-reserved-days</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-hot-regions-reserved-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   ホットリージョン情報を保持する日数を指定します。
-   デフォルト値: `7`

## <code>replication</code> {#code-replication-code}

レプリカに関連するコンフィグレーション項目

### <code>max-replicas</code> {#code-max-replicas-code}

-   レプリカ数、つまりリーダーとフォロワーの数の合計です。デフォルト値の`3` 、リーダー1台とフォロワー2台を意味します。この設定が動的に変更された場合、PDはバックグラウンドでリージョンをスケジュールし、レプリカ数がこの設定と一致するようにします。
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

-   `placement-rules`有効にします。
-   デフォルト値: `true`
-   [配置ルール](/configure-placement-rules.md)参照。

## <code>label-property</code> （非推奨） {#code-label-property-code-deprecated}

`reject-leader`種類のみをサポートする、ラベルに関連するコンフィグレーション項目。

> **注記：**
>
> バージョン5.2以降、ラベル関連の設定項目は非推奨となりました。レプリカポリシーの設定には[配置ルール](/configure-placement-rules.md#scenario-2-place-five-replicas-in-three-data-centers-in-the-proportion-of-221-and-the-leader-should-not-be-in-the-third-data-center)使用することをお勧めします。

### <code>key</code> （非推奨） {#code-key-code-deprecated}

-   Leaderを拒否した店舗のラベルキー
-   デフォルト値: `""`

### <code>value</code> （非推奨） {#code-value-code-deprecated}

-   Leaderを拒否した店舗のラベル値
-   デフォルト値: `""`

## <code>dashboard</code> {#code-dashboard-code}

[TiDBダッシュボード](/dashboard/dashboard-intro.md)内蔵 PD に関するコンフィグレーション項目です。

### <code>disable-custom-prom-addr</code> {#code-disable-custom-prom-addr-code}

-   [TiDBダッシュボード](/dashboard/dashboard-intro.md)でカスタム Prometheus データ ソース アドレスの構成を無効にするかどうか。
-   デフォルト値: `false`
-   `true`に設定すると、TiDB ダッシュボードでカスタム Prometheus データ ソース アドレスを構成すると、TiDB ダッシュボードはエラーを報告します。

### <code>tidb-cacert-path</code> {#code-tidb-cacert-path-code}

-   ルートCA証明書ファイルのパス。TLSを使用してTiDBのSQLサービスに接続するときに、このパスを設定できます。
-   デフォルト値: `""`

### <code>tidb-cert-path</code> {#code-tidb-cert-path-code}

-   SSL証明書ファイルのパス。TLSを使用してTiDBのSQLサービスに接続するときに、このパスを設定できます。
-   デフォルト値: `""`

### <code>tidb-key-path</code> {#code-tidb-key-path-code}

-   SSL 秘密鍵ファイルのパス。TLS を使用して TiDB の SQL サービスに接続するときに、このパスを設定できます。
-   デフォルト値: `""`

### <code>public-path-prefix</code> {#code-public-path-prefix-code}

-   TiDB ダッシュボードがリバース プロキシの背後でアクセスされる場合、この項目はすべての Web リソースのパブリック URL パス プレフィックスを設定します。
-   デフォルト値: `/dashboard`
-   リバースプロキシを経由せずにTiDBダッシュボードにアクセスする場合は、この設定項目を変更し**ないで**ください。変更すると、アクセスの問題が発生する可能性があります。詳細は[リバースプロキシの背後でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)ご覧ください。

### <code>enable-telemetry</code> {#code-enable-telemetry-code}

> **警告：**
>
> v8.1.0以降、TiDBダッシュボードのテレメトリ機能は削除され、この設定項目は機能しなくなりました。これは以前のバージョンとの互換性のためだけに保持されています。

-   v8.1.0 より前では、この構成項目は TiDB ダッシュボードでテレメトリ収集を有効にするかどうかを制御します。
-   デフォルト値: `false`

## <code>replication-mode</code> {#code-replication-mode-code}

全リージョンのレプリケーションモードに関するコンフィグレーション項目です。詳細は[DR自動同期モードを有効にする](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)ご覧ください。

## コントローラ {#controller}

このセクションでは、 PD for [リソース管理](/tidb-resource-control.md)に組み込まれている構成項目について説明します。

### <code>degraded-mode-wait-duration</code> {#code-degraded-mode-wait-duration-code}

-   縮退モードをトリガーするまでの待機時間。縮退モードとは、ローカルトークンバケット（LTB）とグローバルトークンバケット（GTB）が失われた場合、LTBはデフォルトのリソースグループ構成にフォールバックし、GTB認証トークンがなくなることを意味します。これにより、ネットワークの分離や異常が発生した場合でも、サービスが影響を受けないことが保証されます。
-   デフォルト値: 0秒
-   デフォルトでは、劣化モードは無効になっています。

### <code>request-unit</code> {#code-request-unit-code}

[リクエストユニット（RU）](/tidb-resource-control.md#what-is-request-unit-ru)に関する設定項目は以下のとおりです。

#### <code>read-base-cost</code> {#code-read-base-cost-code}

-   読み取り要求からRUへの変換の基礎係数
-   デフォルト値: 0.125

#### <code>write-base-cost</code> {#code-write-base-cost-code}

-   書き込み要求からRUへの変換の基礎係数
-   デフォルト値: 1

#### <code>read-cost-per-byte</code> {#code-read-cost-per-byte-code}

-   読み取りフローからRUへの変換の基礎係数
-   デフォルト値: 1/(64 * 1024)
-   1 RU = 64 KiB の読み取りバイト

#### <code>write-cost-per-byte</code> {#code-write-cost-per-byte-code}

-   書き込みフローからRUへの変換の基礎係数
-   デフォルト値: 1/1024
-   1 RU = 1 KiB 書き込みバイト

#### <code>read-cpu-ms-cost</code> {#code-read-cpu-ms-cost-code}

-   CPUからRUへの変換の基礎係数
-   デフォルト値: 1/3
-   1 RU = 3ミリ秒のCPU時間
