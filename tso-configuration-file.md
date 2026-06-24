---
title: TSO Configuration File
summary: TSO 構成ファイルには、ノード名、データ パス、ノード URL などの複数の構成項目が含まれています。
---

# TSOコンフィグレーションファイル {#tso-configuration-file}

<!-- markdownlint-disable MD001 -->

TSOノードは、PD用の`tso`マイクロサービスを提供するために使用されます。このドキュメントはPDマイクロサービスモードにのみ適用されます。

> **ヒント：**
>
> 構成項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>name</code> {#code-name-code}

-   TSOノードの名前
-   デフォルト値: `"TSO"`
-   複数の TSO ノードを起動するには、各ノードに一意の名前を使用します。

### <code>data-dir</code> {#code-data-dir-code}

-   TSOノードがデータを保存するディレクトリ
-   デフォルト値: `"default.${name}"`

### <code>listen-addr</code> {#code-listen-addr-code}

-   現在のTSOノードがリッスンするクライアントURL
-   デフォルト値: `"http://127.0.0.1:3379"`
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`listen-addr` （例： `"http://192.168.100.113:3379"` ）に指定する必要があります。ノードがDocker上で実行されている場合は、DockerのIPアドレスを`"http://0.0.0.0:3379"`に指定してください。

### <code>advertise-listen-addr</code> {#code-advertise-listen-addr-code}

-   クライアントがTSOノードにアクセスするためのURL
-   デフォルト値: `"${listen-addr}"`
-   Docker や NAT ネットワーク環境などの状況では、クライアントが TSO ノードによってリッスンされるデフォルトのクライアント URL を通じて TSO ノードにアクセスできない場合は、クライアント アクセスに手動で`advertise-listen-addr`設定する必要があります。
-   例えば、Dockerの内部IPアドレスは`172.17.0.1`ですが、ホストのIPアドレスは`192.168.100.113`で、ポートマッピングは`-p 3379:3379`に設定されています。この場合、 `advertise-listen-addr="http://192.168.100.113:3379"`設定できます。そうすることで、クライアントは`http://192.168.100.113:3379`を通じてこのサービスを見つけることができるようになります。

### <code>backend-endpoints</code> {#code-backend-endpoints-code}

-   現在の TSO ノードがリッスンしている他の TSO ノードのバックエンド エンドポイントのリスト
-   デフォルト値: `"http://127.0.0.1:2379"`

### <code>lease</code> {#code-lease-code}

-   TSOプライマリキーリースのタイムアウト。タイムアウト後、システムはプライマリを再選出します。
-   デフォルト値: `3`
-   単位: 秒

### <code>tso-update-physical-interval</code> {#code-tso-update-physical-interval-code}

-   TSO 物理時間が更新される間隔。
-   TSO物理時間のデフォルトの更新間隔（ `50ms` ）内で、TSOサーバーは最大262144個のTSOを提供します。より多くのTSOを取得するには、この設定項目の値を減らすことができます。最小値は`1ms`です。
-   この間隔を短くすると、TSOサーバーのCPU使用率が増加する可能性があります。テストによると、更新間隔が`50ms`の場合と比較して、間隔が`1ms`場合、TSOサーバーのCPU使用率は[CPU使用率](https://man7.org/linux/man-pages/man1/top.1.html)で約10%増加します。
-   デフォルト値: `50ms`
-   最小値: `1ms`

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

-   TSO ノード ログでログ編集を有効にするかどうかを制御します。
-   構成値を`true`に設定すると、TSO ノード ログでユーザー データが編集されます。
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
-   構成項目が設定されていないか、デフォルト値`0`に設定されている場合、TSO はログ ファイルをクリーンアップしません。
-   デフォルト値: `0`

### <code>max-backups</code> {#code-max-backups-code}

-   保持されるログ ファイルの最大数。
-   構成項目が設定されていないか、デフォルト値`0`に設定されている場合、TSO はすべてのログ ファイルを保持します。
-   デフォルト値: `0`

## メトリック {#metric}

監視に関連するコンフィグレーション項目

### <code>interval</code> {#code-interval-code}

-   監視メトリックデータがPrometheusにプッシュされる間隔
-   デフォルト値: `15s`
