---
title: Scheduling Configuration File
summary: スケジューリング構成ファイルには、ノード名、データ パス、ノード URL などの複数の構成項目が含まれています。
---

# スケジュールコンフィグレーションファイル {#scheduling-configuration-file}

<!-- markdownlint-disable MD001 -->

スケジューリング ノードは、PD の`scheduling`マイクロサービスを提供するために使用されます。このドキュメントは、PD マイクロサービス モードでのみ適用されます。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>name</code> {#code-name-code}

-   スケジューリングノードの名前
-   デフォルト値: `"Scheduling"`
-   複数のスケジューリング ノードを開始するには、各ノードに一意の名前を使用します。

### <code>data-dir</code> {#code-data-dir-code}

-   スケジューリングノードがデータを保存するディレクトリ
-   デフォルト値: `"default.${name}"`

### <code>listen-addr</code> {#code-listen-addr-code}

-   現在のスケジューリングノードがリッスンするクライアント URL
-   デフォルト値: `"http://127.0.0.1:3379"`
-   クラスターをデプロイするときは、現在のホストの IP アドレスを`listen-addr` (たとえば`"http://192.168.100.113:3379"` ) として指定する必要があります。ノードが Docker 上で実行される場合は、Docker IP アドレスを`"http://0.0.0.0:3379"`として指定します。

### <code>advertise-listen-addr</code> {#code-advertise-listen-addr-code}

-   スケジュールノードにアクセスするためのクライアントのURL
-   デフォルト値: `"${listen-addr}"`
-   Docker や NAT ネットワーク環境などの状況では、クライアントがスケジューリング ノードによってリッスンされるデフォルトのクライアント URL を通じてスケジューリング ノードにアクセスできない場合は、クライアント アクセスに手動で`advertise-listen-addr`設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 3379:3379`に設定されています。この場合、 `advertise-listen-addr="http://192.168.100.113:2379"`設定できます。すると、クライアントは`http://192.168.100.113:2379`を通じてこのサービスを見つけることができます。

### <code>backend-endpoints</code> {#code-backend-endpoints-code}

-   現在のスケジューリングノードがリッスンする他のスケジューリングノードのバックエンドエンドポイントのリスト
-   デフォルト値: `"http://127.0.0.1:2379"`

### <code>lease</code> {#code-lease-code}

-   スケジュール プライマリ キー リースのタイムアウト。タイムアウト後、システムはプライマリを再選択します。
-   デフォルト値: `3`
-   単位: 秒

## 安全 {#security}

セキュリティに関するコンフィグレーション項目

### <code>cacert-path</code> {#code-cacert-path-code}

-   CAファイルのパス
-   デフォルト値: &quot;&quot;

### <code>cert-path</code> {#code-cert-path-code}

-   X.509証明書を含むPrivacy Enhanced Mail (PEM)ファイルのパス
-   デフォルト値: &quot;&quot;

### <code>key-path</code> {#code-key-path-code}

-   X.509キーを含むPEMファイルのパス
-   デフォルト値: &quot;&quot;

### <code>redact-info-log</code> {#code-redact-info-log-code}

-   スケジューリング ノード ログでログ編集を有効にするかどうかを制御します。
-   構成値を`true`に設定すると、スケジューリング ノード ログでユーザー データが編集されます。
-   デフォルト値: `false`

## ログ {#log}

ログに関連するコンフィグレーション項目。

### <code>level</code> {#code-level-code}

-   出力ログのレベルを指定します。
-   `"error"` `"fatal"` `"warn"` `"debug"` `"info"`
-   デフォルト値: `"info"`

### <code>format</code> {#code-format-code}

-   ログ形式
-   オプション値: `"text"` 、 `"json"`
-   デフォルト値: `"text"`

### <code>disable-timestamp</code> {#code-disable-timestamp-code}

-   ログ内の自動生成されたタイムスタンプを無効にするかどうかを制御します。
-   デフォルト値: `false`

## ログファイル {#log-file}

ログファイルに関するコンフィグレーション項目

### <code>max-size</code> {#code-max-size-code}

-   1 つのログ ファイルの最大サイズ。この値を超えると、システムは自動的にログを複数のファイルに分割します。
-   デフォルト値: `300`
-   単位: MiB
-   最小値: `1`

### <code>max-days</code> {#code-max-days-code}

-   ログが保持される最大日数。
-   構成項目が設定されていないか、デフォルト値`0`に設定されている場合、スケジュールではログ ファイルはクリーンアップされません。
-   デフォルト値: `0`

### <code>max-backups</code> {#code-max-backups-code}

-   保持されるログ ファイルの最大数。
-   構成項目が設定されていないか、デフォルト値`0`に設定されている場合、スケジュールはすべてのログ ファイルを保持します。
-   デフォルト値: `0`

## メトリック {#metric}

監視に関するコンフィグレーション項目

### <code>interval</code> {#code-interval-code}

-   監視メトリックデータがPrometheusにプッシュされる間隔
-   デフォルト値: `15s`
