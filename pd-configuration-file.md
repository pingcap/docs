---
title: PD Configuration File
summary: Learn the PD configuration file.
---

# PDConfiguration / コンフィグレーションファイル {#pd-configuration-file}

<!-- markdownlint-disable MD001 -->

PD構成ファイルは、コマンドラインパラメーターよりも多くのオプションをサポートします。デフォルトの設定ファイル[ここ](https://github.com/pingcap/pd/blob/master/conf/config.toml)を見つけることができます。

このドキュメントでは、コマンドラインパラメータに含まれていないパラメータについてのみ説明します。コマンドラインパラメータについては[ここ](/command-line-flags-for-pd-configuration.md)を確認してください。

### <code>name</code> {#code-name-code}

-   PDノードの一意の名前
-   デフォルト値： `"pd"`
-   複数のPDノードを開始するには、ノードごとに一意の名前を使用します。

### <code>data-dir</code> {#code-data-dir-code}

-   PDがデータを保存するディレクトリ
-   デフォルト値： `default.${name}"`

### <code>client-urls</code> {#code-client-urls-code}

-   PDがリッスンするクライアントURLのリスト
-   デフォルト値： `"http://127.0.0.1:2379"`
-   クラスタを展開するときは、現在のホストのIPアドレスを`client-urls` （たとえば、 `"http://192.168.100.113:2379"` ）として指定する必要があります。クラスタがDockerで実行されている場合は、DockerのIPアドレスを`"http://0.0.0.0:2379"`として指定します。

### <code>advertise-client-urls</code> {#code-advertise-client-urls-code}

-   クライアントがPDにアクセスするためのアドバタイズURLのリスト
-   デフォルト値： `"${client-urls}"`
-   DockerまたはNATネットワーク環境などの一部の状況で、クライアントがPDによってリッスンされるデフォルトのクライアントURLを介してPDにアクセスできない場合は、アドバタイズするクライアントURLを手動で設定する必要があります。
-   たとえば、Dockerの内部IPアドレスは`172.17.0.1`ですが、ホストのIPアドレスは`192.168.100.113`で、ポートマッピングは`-p 2380:2380`に設定されています。この場合、 `advertise-client-urls`を設定でき`"http://192.168.100.113:2380"` 。クライアントは`"http://192.168.100.113:2380"`までこのサービスを見つけることができます。

### <code>peer-urls</code> {#code-peer-urls-code}

-   PDノードがリッスンするピアURLのリスト
-   デフォルト値： `"http://127.0.0.1:2380"`
-   クラスタを展開するときは、現在のホストのIPアドレスとして`peer-urls` （ `"http://192.168.100.113:2380"`など）を指定する必要があります。クラスタがDockerで実行されている場合は、DockerのIPアドレスを`"http://0.0.0.0:2380"`として指定します。

### <code>advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   PDノードにアクセスするための他のPDノード（ピア）のアドバタイズURLのリスト
-   デフォルト： `"${peer-urls}"`
-   DockerまたはNATネットワーク環境などの一部の状況で、他のノード（ピア）がこのPDノードによってリッスンされるデフォルトのピアURLを介してPDノードにアクセスできない場合は、アドバタイズするピアURLを手動で設定する必要があります。
-   たとえば、Dockerの内部IPアドレスは`172.17.0.1`ですが、ホストのIPアドレスは`192.168.100.113`で、ポートマッピングは`-p 2380:2380`に設定されています。この場合、 `advertise-peer-urls`を設定でき`"http://192.168.100.113:2380"` 。他のPDノードは`"http://192.168.100.113:2380"`を介してこのサービスを見つけることができます。

### <code>initial-cluster</code> {#code-initial-cluster-code}

-   ブートストラップの初期クラスタ構成
-   デフォルト値： `"{name}=http://{advertise-peer-url}"`
-   たとえば、 `name`が「pd」で`advertise-peer-urls`が`"http://192.168.100.113:2380"`の場合、 `initial-cluster`は`"pd=http://192.168.100.113:2380"`です。
-   3台のPDサーバーを起動する必要がある場合、 `initial-cluster`台は次のようになります。

    ```
    pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380
    ```

### <code>initial-cluster-state</code> {#code-initial-cluster-state-code}

-   クラスタの初期状態
-   デフォルト値： `"new"`

### <code>initial-cluster-token</code> {#code-initial-cluster-token-code}

-   ブートストラップフェーズ中にさまざまなクラスターを識別します
-   デフォルト値： `"pd-cluster"`
-   同じ構成のノードを持つ複数のクラスターが連続してデプロイされる場合は、異なるクラスタノードを分離するために異なるトークンを指定する必要があります。

### <code>lease</code> {#code-lease-code}

-   PDリーダーキーリースのタイムアウト。タイムアウト後、システムはリーダーを再選出します。
-   デフォルト値： `3`
-   単位：秒

### <code>quota-backend-bytes</code> {#code-quota-backend-bytes-code}

-   メタ情報データベースのストレージサイズ（デフォルトでは8GiB）
-   デフォルト値： `8589934592`

### <code>auto-compaction-mod</code> {#code-auto-compaction-mod-code}

-   メタ情報データベースの自動圧縮モード
-   使用可能なオプション： `periodic` （サイクル別）および`revision` （バージョン番号別）。
-   デフォルト値： `periodic`

### <code>auto-compaction-retention</code> {#code-auto-compaction-retention-code}

-   `auto-compaction-retention`が`periodic`の場合のメタ情報データベースの自動圧縮の時間間隔。圧縮モードが`revision`に設定されている場合、このパラメーターは自動圧縮のバージョン番号を示します。
-   デフォルト値：1時間

### <code>force-new-cluster</code> {#code-force-new-cluster-code}

-   PDを強制的に新しいクラスタとして開始し、 Raftメンバーの数を`1`に変更するかどうかを決定します
-   デフォルト値： `false`

## 安全 {#security}

セキュリティに関連するConfiguration / コンフィグレーション項目

### <code>cacert-path</code> {#code-cacert-path-code}

-   CAファイルのパス
-   デフォルト値： &quot;&quot;

### <code>cert-path</code> {#code-cert-path-code}

-   X509証明書を含むPrivacyEnhancedMail（PEM）ファイルのパス
-   デフォルト値： &quot;&quot;

### <code>key-path</code> {#code-key-path-code}

-   X509キーを含むPEMファイルのパス
-   デフォルト値： &quot;&quot;

### <code>redact-info-log</code><span class="version-mark">新機能</span> {#code-redact-info-log-code-span-class-version-mark-new-in-v5-0-span}

-   PDログでログ編集を有効にするかどうかを制御します
-   構成値を`true`に設定すると、PDログのユーザーデータが編集されます。
-   デフォルト値： `false`

## <code>log</code> {#code-log-code}

ログに関連するConfiguration / コンフィグレーション項目

### <code>level</code> {#code-level-code}

-   出力ログのレベルを指定します
-   `"error"` `"fatal"` `"warn"` `"debug"` `"info"`
-   デフォルト値： `"info"`

### <code>format</code> {#code-format-code}

-   ログ形式
-   オプション`"json"` ： `"text"`
-   デフォルト値： `"text"`

### <code>disable-timestamp</code> {#code-disable-timestamp-code}

-   ログに自動生成されたタイムスタンプを無効にするかどうか
-   デフォルト値： `false`

## <code>log.file</code> {#code-log-file-code}

ログファイルに関連するConfiguration / コンフィグレーション項目

### <code>max-size</code> {#code-max-size-code}

-   単一のログファイルの最大サイズ。この値を超えると、システムはログをいくつかのファイルに自動的に分割します。
-   デフォルト値： `300`
-   単位：MiB
-   最小値： `1`

### <code>max-days</code> {#code-max-days-code}

-   ログが保持される最大日数
-   デフォルト値： `0`

### <code>max-backups</code> {#code-max-backups-code}

-   保持するログファイルの最大数
-   デフォルト値： `0`

## <code>metric</code> {#code-metric-code}

モニタリングに関連するConfiguration / コンフィグレーション項目

### <code>interval</code> {#code-interval-code}

-   モニタリングメトリックデータがPrometheusにプッシュされる間隔
-   デフォルト値： `15s`

## <code>schedule</code> {#code-schedule-code}

スケジューリングに関連するConfiguration / コンフィグレーション項目

### <code>max-merge-region-size</code> {#code-max-merge-region-size-code}

-   `Region Merge`のサイズ制限を制御します。リージョンサイズが指定された値より大きい場合、PDはリージョンを隣接するリージョンとマージしません。
-   デフォルト値： `20`
-   単位：MiB

### <code>max-merge-region-keys</code> {#code-max-merge-region-keys-code}

-   `Region Merge`キーの上限を指定します。リージョンキーが指定された値より大きい場合、PDはリージョンを隣接するリージョンとマージしません。
-   デフォルト値： `200000`

### <code>patrol-region-interval</code> {#code-patrol-region-interval-code}

-   `replicaChecker`がリージョンのヘルス状態をチェックする実行頻度を制御します。この値が小さいほど、 `replicaChecker`回の実行が速くなります。通常、このパラメータを調整する必要はありません。
-   デフォルト値： `10ms`

### <code>split-merge-interval</code> {#code-split-merge-interval-code}

-   同じリージョンでの`split`回の操作と`merge`の操作の間の時間間隔を制御します。つまり、新しく分割されたリージョンはしばらくの間マージされません。
-   デフォルト値： `1h`

### <code>max-snapshot-count</code> {#code-max-snapshot-count-code}

-   1つのストアが同時に受信または送信するスナップショットの最大数を制御します。 PDスケジューラーは、通常のトラフィックに使用されるリソースがプリエンプションされるのを防ぐために、この構成に依存しています。
-   デフォルト値： `64`

### <code>max-pending-peer-count</code> {#code-max-pending-peer-count-code}

-   1つのストアで保留中のピアの最大数を制御します。 PDスケジューラーは、この構成に依存して、古いログを持つリージョンが一部のノードで生成されるのを防ぎます。
-   デフォルト値： `64`

### <code>max-store-down-time</code> {#code-max-store-down-time-code}

-   切断されたストアを回復できないとPDが判断するまでのダウンタイム。 PDは、指定された時間が経過してもストアからハートビートを受信できない場合、他のノードにレプリカを追加します。
-   デフォルト値： `30m`

### <code>leader-schedule-limit</code> {#code-leader-schedule-limit-code}

-   同時に実行されたリーダースケジューリングタスクの数
-   デフォルト値： `4`

### <code>region-schedule-limit</code> {#code-region-schedule-limit-code}

-   同時に実行されたリージョンスケジューリングタスクの数
-   デフォルト値： `2048`

### <code>hot-region-schedule-limit</code> {#code-hot-region-schedule-limit-code}

-   同時に実行されているホットリージョンスケジューリングタスクを制御します。これは、リージョンのスケジューリングとは無関係です。
-   デフォルト値： `4`

### <code>hot-region-cache-hits-threshold</code> {#code-hot-region-cache-hits-threshold-code}

-   ホットリージョンを識別するために必要な分数を設定するために使用されるしきい値。 PDは、リージョンがこの分数を超えてホットスポット状態になった後でのみ、ホットスポットスケジューリングに参加できます。
-   デフォルト値： `3`

### <code>replica-schedule-limit</code> {#code-replica-schedule-limit-code}

-   同時に実行されたレプリカスケジューリングタスクの数
-   デフォルト値： `64`

### <code>merge-schedule-limit</code> {#code-merge-schedule-limit-code}

-   同時に実行された`Region Merge`のスケジューリングタスクの数。 `Region Merge`を無効にするには、このパラメーターを`0`に設定します。
-   デフォルト値： `8`

### <code>high-space-ratio</code> {#code-high-space-ratio-code}

-   それを下回るとストアの容量が十分になるしきい値の比率。ストアのスペース占有率がこのしきい値よりも小さい場合、PDはスケジューリングを実行するときにストアの残りのスペースを無視し、主にリージョンサイズに基づいて負荷を分散します。この構成は、 `region-score-formula-version`が`v1`に設定されている場合にのみ有効になります。
-   デフォルト値： `0.7`
-   最小値： `0`より大きい
-   最大値： `1`未満

### <code>low-space-ratio</code> {#code-low-space-ratio-code}

-   それを超えると店舗の容量が不足するしきい値比率。ストアのスペース占有率がこのしきい値を超える場合、PDはデータをこのストアに移行することを可能な限り回避します。一方、PDは、対応するストアのディスク容量が不足しないように、主にストアの残りの容量に基づいてスケジューリングを実行します。
-   デフォルト値： `0.8`
-   最小値： `0`より大きい
-   最大値： `1`未満

### <code>tolerant-size-ratio</code> {#code-tolerant-size-ratio-code}

-   `balance`のバッファサイズを制御します
-   デフォルト値： `0` （バッファサイズを自動的に調整します）
-   最小値： `0`

### <code>enable-cross-table-merge</code> {#code-enable-cross-table-merge-code}

-   クロステーブルリージョンのマージを有効にするかどうかを決定します
-   デフォルト値： `true`

### <code>region-score-formula-version</code> <span class="version-mark">versionv5.0の新機能</span> {#code-region-score-formula-version-code-span-class-version-mark-new-in-v5-0-span}

-   地域スコア式のバージョンを制御します
-   デフォルト値： `v2`
-   オプションの値： `v1`および`v2` 。 v1と比較して、v2での変更はよりスムーズであり、スペースの再利用によって引き起こされるスケジューリングジッターが改善されています。

> **ノート：**
>
> クラスタをTiDB4.0バージョンから現在のバージョンにアップグレードした場合、アップグレードの前後で一貫したPDの動作を保証するために、新しい数式バージョンはデフォルトで自動的に無効になります。数式のバージョンを変更する場合は、手動で`pd-ctl`の設定を切り替える必要があります。詳しくは[PD Control](/pd-control.md#config-show--set-option-value--placement-rules)をご覧ください。

### <code>enable-joint-consensus</code><span class="version-mark">の新機能</span> {#code-enable-joint-consensus-code-span-class-version-mark-new-in-v5-0-span}

-   レプリカのスケジューリングにジョイントコンセンサスを使用するかどうかを制御します。この構成が無効になっている場合、PDは一度に1つのレプリカをスケジュールします。
-   デフォルト値： `true`

### <code>hot-regions-write-interval</code><span class="version-mark">の新機能</span> {#code-hot-regions-write-interval-code-span-class-version-mark-new-in-v5-4-0-span}

-   PDがホットリージョン情報を保存する時間間隔。
-   デフォルト値： `10m`

> **ノート：**
>
> ホットリージョンに関する情報は、3分ごとに更新されます。間隔が3分未満に設定されている場合、間隔中の更新は無意味になる可能性があります。

### <code>hot-regions-reserved-days</code> <span class="version-mark">daysv5.4.0の新機能</span> {#code-hot-regions-reserved-days-code-span-class-version-mark-new-in-v5-4-0-span}

-   ホットリージョン情報を保持する日数を指定します。
-   デフォルト値： `7`

## <code>replication</code> {#code-replication-code}

レプリカに関連するConfiguration / コンフィグレーション項目

### <code>max-replicas</code> {#code-max-replicas-code}

-   レプリカの数、つまり、リーダーとフォロワーの数の合計。デフォルト値`3`は、1人のリーダーと2人のフォロワーを意味します。この構成がオンラインで変更されると、PDは、レプリカの数がこの構成と一致するように、バックグラウンドでリージョンをスケジュールします。
-   デフォルト値： `3`

### <code>location-labels</code> {#code-location-labels-code}

-   TiKVクラスタのトポロジー情報
-   デフォルト値： `[]`
-   [クラスタートポロジ構成](/schedule-replicas-by-topology-labels.md)

### <code>isolation-level</code> {#code-isolation-level-code}

-   TiKVクラスタの最小トポロジー分離レベル
-   デフォルト値： `""`
-   [クラスタートポロジ構成](/schedule-replicas-by-topology-labels.md)

### <code>strictly-match-label</code> {#code-strictly-match-label-code}

-   TiKVラベルがPDの`location-labels`と一致するかどうかの厳密なチェックを有効にします。
-   デフォルト値： `false`

### <code>enable-placement-rules</code> {#code-enable-placement-rules-code}

-   `placement-rules`を有効にします。
-   デフォルト値： `false`
-   [配置ルール](/configure-placement-rules.md)を参照してください。
-   TiDB4.0の実験的機能。

### <code>flow-round-by-digit</code>ごとの<span class="version-mark">フローTiDB5.1の新機能</span> {#code-flow-round-by-digit-code-span-class-version-mark-new-in-tidb-5-1-span}

-   デフォルト値：3
-   PDはフロー番号の最下位桁を丸めます。これにより、リージョンフロー情報の変更によって引き起こされる統計の更新が削減されます。この構成項目は、リージョンフロー情報を丸める最下位桁数を指定するために使用されます。たとえば、デフォルト値は`3`であるため、フロー`100512`は`101000`に丸められます。この構成は`trace-region-flow`を置き換えます。

> **ノート：**
>
> クラスタをTiDB4.0バージョンから現在のバージョンにアップグレードした場合、アップグレード後の`flow-round-by-digit`の動作と、アップグレード前の`trace-region-flow`の動作はデフォルトで一貫しています。これは、アップグレード前に`trace-region-flow`の値がfalseの場合、アップグレード後の`flow-round-by-digit`の値は127であることを意味します。アップグレード前の`trace-region-flow`の値が`true`の場合、アップグレード後の`flow-round-by-digit`の値は`3`です。

## <code>label-property</code> {#code-label-property-code}

ラベルに関連するConfiguration / コンフィグレーション項目

### <code>key</code> {#code-key-code}

-   リーダーを拒否したストアのラベルキー
-   デフォルト値： `""`

### <code>value</code> {#code-value-code}

-   リーダーを拒否したストアのラベル値
-   デフォルト値： `""`

## <code>dashboard</code> {#code-dashboard-code}

[TiDBダッシュボード](/dashboard/dashboard-intro.md)内蔵PDに関連するConfiguration / コンフィグレーション項目。

### <code>tidb-cacert-path</code> {#code-tidb-cacert-path-code}

-   ルートCA証明書ファイルのパス。 TLSを使用してTiDBのSQLサービスに接続するときに、このパスを構成できます。
-   デフォルト値： `""`

### <code>tidb-cert-path</code> {#code-tidb-cert-path-code}

-   SSL証明書ファイルのパス。 TLSを使用してTiDBのSQLサービスに接続するときに、このパスを構成できます。
-   デフォルト値： `""`

### <code>tidb-key-path</code> {#code-tidb-key-path-code}

-   SSL秘密鍵ファイルのパス。 TLSを使用してTiDBのSQLサービスに接続するときに、このパスを構成できます。
-   デフォルト値： `""`

### <code>public-path-prefix</code> {#code-public-path-prefix-code}

-   TiDBダッシュボードがリバースプロキシの背後でアクセスされる場合、このアイテムはすべてのWebリソースのパブリックURLパスプレフィックスを設定します。
-   デフォルト値： `/dashboard`
-   リバースプロキシの背後ではなくTiDBダッシュボードにアクセスする場合は、この構成アイテムを変更し**ない**でください。そうしないと、アクセスの問題が発生する可能性があります。詳細については、 [リバースプロキシの背後でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。

### <code>enable-telemetry</code> {#code-enable-telemetry-code}

-   TiDBダッシュボードでテレメトリ収集機能を有効にするかどうかを決定します。
-   デフォルト値： `true`
-   詳細については、 [テレメトリー](/telemetry.md)を参照してください。

## <code>replication-mode</code> {#code-replication-mode-code}

すべてのリージョンのレプリケーションモードに関連するConfiguration / コンフィグレーションアイテム。詳細については、 [DR自動同期モードを有効にします](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)を参照してください。
