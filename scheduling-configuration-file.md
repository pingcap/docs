---
title: Scheduling Configuration File
summary: スケジューリング構成ファイルには、ノード名、データ パス、ノード URL などの複数の構成項目が含まれています。
---

# スケジュールコンフィグレーションファイル {#scheduling-configuration-file}

<!-- markdownlint-disable MD001 -->

スケジューリングノードは、PD用の`scheduling`サービスを提供するために使用されます。このドキュメントはPDマイクロサービスモードにのみ適用されます。

> **ヒント：**
>
> 構成項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

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
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`listen-addr` （例： `"http://192.168.100.113:3379"` ）に指定する必要があります。ノードがDocker上で実行されている場合は、DockerのIPアドレスを`"http://0.0.0.0:3379"`に指定してください。

### <code>advertise-listen-addr</code> {#code-advertise-listen-addr-code}

-   クライアントがスケジューリングノードにアクセスするためのURL
-   デフォルト値: `"${listen-addr}"`
-   Docker や NAT ネットワーク環境などの状況では、クライアントがスケジューリング ノードによってリッスンされるデフォルトのクライアント URL を通じてスケジューリング ノードにアクセスできない場合は、クライアント アクセスに手動で`advertise-listen-addr`設定する必要があります。
-   例えば、Dockerの内部IPアドレスは`172.17.0.1`ですが、ホストのIPアドレスは`192.168.100.113`で、ポートマッピングは`-p 3379:3379`に設定されています。この場合、 `advertise-listen-addr="http://192.168.100.113:2379"`設定できます。そうすることで、クライアントは`http://192.168.100.113:2379`を通じてこのサービスを見つけることができるようになります。

### <code>backend-endpoints</code> {#code-backend-endpoints-code}

-   現在のスケジューリングノードがリッスンする他のスケジューリングノードのバックエンドエンドポイントのリスト
-   デフォルト値: `"http://127.0.0.1:2379"`

### <code>lease</code> {#code-lease-code}

-   スケジュールプライマリキーリースのタイムアウト。タイムアウト後、システムはプライマリを再選出します。
-   デフォルト値: `3`
-   単位: 秒

## 安全 {#security}

セキュリティ関連のコンフィグレーション項目

### <code>cacert-path</code> {#code-cacert-path-code}

-   CAファイルのパス
-   デフォルト値: &quot;&quot;

### <code>cert-path</code> {#code-cert-path-code}

-   X.509証明書を含むPrivacy Enhanced Mail（PEM）ファイルのパス
-   デフォルト値: &quot;&quot;

### <code>key-path</code> {#code-key-path-code}

-   X.509キーを含むPEMファイルのパス
-   デフォルト値: &quot;&quot;

### <code>redact-info-log</code> {#code-redact-info-log-code}

-   スケジュール ノード ログでログ編集を有効にするかどうかを制御します。
-   構成値を`true`に設定すると、スケジュール ノード ログでユーザー データが編集されます。
-   デフォルト値: `false`

## ログ {#log}

ログに関するコンフィグレーション項目。

### <code>level</code> {#code-level-code}

-   出力ログのレベルを指定します。
-   `"warn"` `"fatal"` `"error"` `"debug"` `"info"`
-   デフォルト値: `"info"`

### <code>format</code> {#code-format-code}

-   ログ形式
-   オプション`"json"` : `"text"`
-   デフォルト値: `"text"`

### <code>disable-timestamp</code> {#code-disable-timestamp-code}

-   ログ内の自動生成されたタイムスタンプを無効にするかどうかを制御します。
-   デフォルト値: `false`

## ログファイル {#log-file}

ログファイルに関連するコンフィグレーション項目

### <code>max-size</code> {#code-max-size-code}

-   1つのログファイルの最大サイズ。この値を超えると、システムは自動的にログを複数のファイルに分割します。
-   デフォルト値: `300`
-   単位: MiB
-   最小値: `1`

### <code>max-days</code> {#code-max-days-code}

-   ログが保持される最大日数。
-   構成項目が設定されていないか、デフォルト値`0`に設定されている場合、スケジュールではログ ファイルがクリーンアップされません。
-   デフォルト値: `0`

### <code>max-backups</code> {#code-max-backups-code}

-   保持されるログ ファイルの最大数。
-   構成項目が設定されていないか、デフォルト値`0`に設定されている場合、スケジュールはすべてのログ ファイルを保持します。
-   デフォルト値: `0`

## メトリック {#metric}

監視に関連するコンフィグレーション項目

### <code>interval</code> {#code-interval-code}

-   監視メトリックデータがPrometheusにプッシュされる間隔
-   デフォルト値: `15s`
