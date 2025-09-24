---
title: Configuration Options
summary: TiDB の構成オプションについて学習します。
---

# コンフィグレーションオプション {#configuration-options}

TiDBクラスタを起動する際には、コマンドラインオプションまたは環境変数を使用して設定できます。このドキュメントでは、TiDBのコマンドオプションについて説明します。デフォルトのTiDBポートは、クライアントリクエスト用に`4000` 、ステータスレポート用に`10080`です。

## <code>--advertise-address</code> {#code-advertise-address-code}

-   TiDBサーバーにログインするためのIPアドレス
-   デフォルト: `""`
-   このアドレスは、TiDB クラスターの残りの部分とユーザーがアクセスできる必要があります。

## <code>--config</code> {#code-config-code}

-   設定ファイル
-   デフォルト: `""`
-   設定ファイルが指定されている場合、TiDB は設定ファイルを読み取ります。対応する設定がコマンドラインオプションにも存在する場合、TiDB はコマンドラインオプションの設定を使用して設定ファイルの設定を上書きします。詳細な設定情報については、 [TiDBコンフィグレーションファイルの説明](/tidb-configuration-file.md)参照してください。

## <code>--config-check</code> {#code-config-check-code}

-   設定ファイルの有効性をチェックして終了します
-   デフォルト: `false`

## <code>--config-strict</code> {#code-config-strict-code}

-   設定ファイルの有効性を強制する
-   デフォルト: `false`

## <code>--cors</code> {#code-cors-code}

-   TiDB HTTPステータスサービスのクロスオリジンリクエスト共有（CORS）リクエストの値`Access-Control-Allow-Origin`指定します。
-   デフォルト: `""`

## <code>--host</code> {#code-host-code}

-   TiDBサーバーが監視するホストアドレス
-   デフォルト: `"0.0.0.0"`
-   TiDBサーバーはこのアドレスを監視します。
-   `"0.0.0.0"`アドレスはデフォルトですべてのネットワークカードを監視します。複数のネットワークカードがある場合は、サービスを提供するネットワークカード（例： `192.168.100.113` ）を指定してください。

## <code>--initialize-insecure</code> {#code-initialize-insecure-code}

-   tidb-server を非セキュアモードでブートストラップする
-   デフォルト: `true`

## <code>--initialize-secure</code> {#code-initialize-secure-code}

-   tidb-server の初期化時に、認証方式`auth_socket`使用してアカウント`root`を作成するかどうかを制御します。 `true`に設定した場合、TiDB への初回ログインにはソケット接続を使用する必要があります。これにより、セキュリティが強化されます。
-   デフォルト: `false`

## <code>--initialize-sql-file</code> {#code-initialize-sql-file-code}

-   TiDBクラスタの初回起動時に実行されるSQLスクリプト。詳細は[構成項目`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)参照。
-   デフォルト: `""`

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト: `"info"`
-   `"warn"` `"fatal"` `"error"` `"debug"` `"info"`

## <code>--lease</code> {#code-lease-code}

-   スキーマリースの期間。何をするかを十分に理解していない場合は、値を変更するのは**危険**です。
-   デフォルト: `45s`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト: `""`
-   このオプションが設定されていない場合、ログは「stderr」に出力されます。このオプションが設定されている場合、ログは対応するファイルに出力されます。

## <code>--log-general</code> {#code-log-general-code}

-   [一般ログ](/system-variables.md#tidb_general_log)のファイル名
-   デフォルト: `""`
-   このオプションが設定されていない場合、一般ログはデフォルトで[`--log-file`](#--log-file)で指定されたファイルに書き込まれます。

## <code>--log-slow-query</code> {#code-log-slow-query-code}

-   スロークエリログのディレクトリ
-   デフォルト: `""`
-   このオプションが設定されていない場合、ログはデフォルトで`--log-file`で指定されたファイルに出力されます。

## <code>--metrics-addr</code> {#code-metrics-addr-code}

-   Prometheus Pushgatewayアドレス
-   デフォルト: `""`
-   空のままにすると、Prometheus クライアントのプッシュが停止します。
-   形式は`--metrics-addr=192.168.100.115:9091`です。

## <code>--metrics-interval</code> {#code-metrics-interval-code}

-   Prometheusクライアントのプッシュ間隔（秒）
-   デフォルト: `15s`
-   値を 0 に設定すると、Prometheus クライアントのプッシュが停止します。

## <code>-P</code> {#code-p-code}

-   TiDBサービスの監視ポート
-   デフォルト: `"4000"`
-   TiDBサーバーはこのポートからの MySQL クライアント要求を受け入れます。

## <code>--path</code> {#code-path-code}

-   「unistore」のようなローカルstorageエンジンのデータディレクトリへのパス
-   `--store = tikv`場合、パスを指定する必要があります。 `--store = unistore`場合、パスを指定しないとデフォルト値が使用されます。
-   TiKVのような分散storageエンジンの場合、 `--path`実際のPDアドレスを指定します。PDサーバーを192.168.100.113:2379、192.168.100.114:2379、192.168.100.115:2379にデプロイすると仮定すると、 `--path`値は「192.168.100.113:2379、192.168.100.114:2379、192.168.100.115:2379」となります。
-   デフォルト: `"/tmp/tidb"`
-   純粋なインメモリ TiDB を有効にするには、 `tidb-server --store=unistore --path=""`使用します。

## <code>--proxy-protocol-fallbackable</code> {#code-proxy-protocol-fallbackable-code}

-   PROXYプロトコルフォールバックモードを有効にするかどうかを制御します。このパラメータを`true`に設定すると、TiDBはPROXYプロトコル仕様を使用せず、PROXYプロトコルヘッダーを送信せずに、 `--proxy-protocol-networks`に属するクライアント接続を受け入れます。デフォルトでは、TiDBは`--proxy-protocol-networks`に属し、PROXYプロトコルヘッダーを送信するクライアント接続のみを受け入れます。
-   デフォルト値: `false`

## <code>--proxy-protocol-networks</code> {#code-proxy-protocol-networks-code}

-   [PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)使用して TiDB に接続できるプロキシ サーバーの IP アドレスのリスト。
-   デフォルト: `""`
-   通常、リバースプロキシを経由してTiDBにアクセスする場合、TiDBはリバースプロキシサーバーのIPアドレスをクライアントのIPアドレスとして取得します。PROXYプロトコルを有効にすると、HAProxyなどのこのプロトコルをサポートするリバースプロキシは、実際のクライアントIPアドレスをTiDBに渡すことができます。
-   このフラグを設定すると、TiDBは設定された送信元IPアドレスがPROXYプロトコルを使用してTiDBに接続することを許可します。PROXY以外のプロトコルが使用されている場合、この接続は拒否されます。その他のアドレスはPROXYプロトコルを使用せずにTiDBに接続できます。このフラグを空のままにすると、どのIPアドレスもPROXYプロトコルを使用してTiDBに接続できなくなります。値は、IPアドレス（192.168.1.50）またはCIDR（192.168.1.0/24）で、区切り文字として`,`使用します。3 `*`任意のIPアドレスを意味します。

> **警告：**
>
> `*` 、任意の IP アドレスのクライアントが自身の IP アドレスを報告できるようになるため、セキュリティリスクが生じる可能性があるため、注意して使用してください。また、 `*`使用すると、 `--proxy-protocol-fallbackable` `true`に設定しないと、TiDB に直接接続する内部コンポーネント（TiDB ダッシュボードなど）が利用できなくなる可能性があります。

> **注記：**
>
> PROXYプロトコルを有効にしたAWS Network Load Balancer（NLB）を使用するには、NLBの`target group`プロパティを設定する必要があります。具体的には、 `proxy_protocol_v2.client_to_server.header_place`を`on_first_ack`に設定します。同時に、AWSサポートにチケットを送信する必要があります。PROXYプロトコルを有効にすると、クライアントはサーバーからのハンドシェイクパケットの取得に失敗し、クライアントがタイムアウトするまでパケットがブロックされることに注意してください。これは、NLBがクライアントがデータを送信した後にのみプロキシパケットを送信するためです。ただし、クライアントがデータパケットを送信する前に、サーバーから送信されたデータパケットは内部ネットワークでドロップされます。

## <code>--proxy-protocol-header-timeout</code> {#code-proxy-protocol-header-timeout-code}

-   PROXYプロトコルヘッダー読み取りのタイムアウト
-   デフォルト: `5` (秒)

> **警告：**
>
> バージョン6.3.0以降、このパラメータは非推奨となりました。ネットワークデータの初回読み取り時にPROXYプロトコルヘッダーが読み込まれるため、このパラメータは使用されなくなりました。このパラメータを非推奨にすることで、ネットワークデータの初回読み取り時に設定されるタイムアウトに影響を与えなくなります。

> **注記：**
>
> 値を`0`に設定しないでください。特別な状況を除き、デフォルト値を使用してください。

## <code>--report-status</code> {#code-report-status-code}

-   ステータスレポートとpprofツールを有効（ `true` ）または無効（ `false` ）にする
-   デフォルト: `true`
-   このパラメータを`true`に設定すると、メトリクスとpprofが有効になります。 `false`に設定すると、メトリクスとpprofが無効になります。

## <code>--run-ddl</code> {#code-run-ddl-code}

-   `tidb-server` DDL文を実行するかどうかを確認し、クラスタ内の`tidb-server`の数が2を超える場合に設定する
-   デフォルト: `true`
-   値は (true) または (false) になります。 (true) は、 `tidb-server` DDL 自体を実行することを示します。 (false) は、 `tidb-server` DDL 自体を実行しないことを示します。

## <code>--socket string</code> {#code-socket-string-code}

-   TiDB サービスは、外部接続に Unix ソケット ファイルを使用します。
-   デフォルト: `""`
-   `/tmp/tidb.sock`使用して Unix ソケット ファイルを開きます。

## <code>--status</code> {#code-status-code}

-   TiDBサーバーのステータスレポートポート
-   デフォルト: `"10080"`
-   このポートはサーバー内部データを取得するために使用されます。データには[プロメテウスメトリクス](https://prometheus.io/)と[専門家](https://golang.org/pkg/net/http/pprof/)含まれます。
-   Prometheus メトリックには`"http://host:status_port/metrics"`でアクセスできます。
-   pprof データには`"http://host:status_port/debug/pprof"`でアクセスできます。

## <code>--status-host</code> {#code-status-host-code}

-   TiDBサービスのステータスを監視するために使用される`HOST`
-   デフォルト: `0.0.0.0`

## <code>--store</code> {#code-store-code}

-   最レイヤーで TiDB が使用するstorageエンジンを指定します
-   デフォルト: `"unistore"`
-   「unistore」または「tikv」を選択できます。（「unistore」はローカルstorageエンジン、「tikv」は分散storageエンジンです）

## <code>--temp-dir</code> {#code-temp-dir-code}

-   TiDBの一時ディレクトリ
-   デフォルト: `"/tmp/tidb"`

## <code>--tidb-service-scope</code> {#code-tidb-service-scope-code}

-   現在の TiDB インスタンスの初期値として[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)指定します。
-   デフォルト: `""`

## <code>--token-limit</code> {#code-token-limit-code}

-   TiDBで同時に実行できるセッション数。トラフィック制御に使用されます。
-   デフォルト: `1000`
-   同時セッション数が`token-limit`より大きい場合、リクエストはブロックされ、トークンを解放する操作が終了するまで待機します。

## <code>-V</code> {#code-v-code}

-   TiDBのバージョンを出力します
-   デフォルト: `""`

## <code>--plugin-dir</code> {#code-plugin-dir-code}

-   プラグインのstorageディレクトリ。
-   デフォルト: `"/data/deploy/plugin"`

## <code>--plugin-load</code> {#code-plugin-load-code}

-   ロードするプラグインの名前。それぞれはコンマで区切られます。
-   デフォルト: `""`

## <code>--affinity-cpus</code> {#code-affinity-cpus-code}

-   TiDBサーバーのCPUアフィニティをカンマ区切りで設定します。例：&quot;1,2,3&quot;。
-   デフォルト: `""`

## <code>--redact</code> {#code-redact-code}

-   サブコマンド`collect-log`使用するときに、 TiDBサーバーがログ ファイルを非感度化するかどうかを決定します。
-   デフォルト: false
-   値が`true`の場合、マスキング操作となり、 `‹ ›`マーク記号で囲まれたすべてのフィールドが`?`に置き換えられます。値が`false`の場合、リストア操作となり、すべてのマーク記号が削除されます。この機能を使用するには、 `./tidb-server --redact=xxx collect-log <input> <output>`実行して、 `<input>`で指定された TiDBサーバーログファイルを非感応化またはリストアし、 `<output>`に出力します。詳細については、システム変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log)参照してください。

## <code>--repair-mode</code> {#code-repair-mode-code}

-   データ修復シナリオでのみ使用される修復モードを有効にするかどうかを決定します。
-   デフォルト: `false`

## <code>--repair-list</code> {#code-repair-list-code}

-   修復モードで修復されるテーブルの名前。
-   デフォルト: `""`
