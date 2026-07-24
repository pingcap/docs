---
title: Configuration Options
summary: TiDB の構成オプションについて学習します。
---

# コンフィグレーションオプション {#configuration-options}

TiDBクラスタを起動する際には、コマンドラインオプションまたは環境変数を使用して設定できます。このドキュメントでは、TiDBのコマンドオプションについて説明します。デフォルトのTiDBポートは、クライアントリクエスト用に`4000` 、ステータスレポート用に`10080`です。

## `--advertise-address` {#--advertise-address}

-   TiDBサーバーにログインするためのIPアドレス
-   デフォルト: `""`
-   このアドレスは、TiDB クラスターの残りの部分とユーザーがアクセスできる必要があります。

## `--config` {#--config}

-   設定ファイル
-   デフォルト: `""`
-   設定ファイルが指定されている場合、TiDB は設定ファイルを読み取ります。対応する設定がコマンドラインオプションにも存在する場合、TiDB はコマンドラインオプションの設定を使用して設定ファイルの設定を上書きします。詳細な設定情報については、 [TiDBコンフィグレーションファイルの説明](/tidb-configuration-file.md)参照してください。

## `--config-check` {#--config-check}

-   設定ファイルの有効性をチェックして終了します
-   デフォルト: `false`

## `--config-strict` {#--config-strict}

-   設定ファイルの有効性を強制する
-   デフォルト: `false`

## `--cors` {#--cors}

-   TiDB HTTPステータスサービスのクロスオリジンリクエスト共有（CORS）リクエストの値`Access-Control-Allow-Origin`指定します。
-   デフォルト: `""`

## `--host` {#--host}

-   TiDBサーバーが監視するホストアドレス
-   デフォルト: `"0.0.0.0"`
-   TiDBサーバーはこのアドレスを監視します。
-   `"0.0.0.0"`アドレスはデフォルトですべてのネットワークカードを監視します。複数のネットワークカードがある場合は、サービスを提供するネットワークカード（例： `192.168.100.113` ）を指定してください。

## `--initialize-insecure` {#--initialize-insecure}

-   tidb-server を非セキュアモードでブートストラップする
-   デフォルト: `true`

## `--initialize-secure` {#--initialize-secure}

-   tidb-server の初期化時に、認証方式`auth_socket`使用してアカウント`root`を作成するかどうかを制御します。 `true`に設定した場合、TiDB への初回ログインにはソケット接続を使用する必要があります。これにより、セキュリティが強化されます。
-   デフォルト: `false`

## `--initialize-sql-file` {#--initialize-sql-file}

-   TiDBクラスタの初回起動時に実行されるSQLスクリプト。詳細は[構成項目`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)参照。
-   デフォルト: `""`

## `-L` {#-l}

-   ログレベル
-   デフォルト: `"info"`
-   `"warn"` `"fatal"` `"error"` `"debug"` `"info"`

## `--lease` {#--lease}

-   スキーマリースの期間。何をするかを十分に理解していない場合は、値を変更するのは**危険**です。
-   デフォルト: `45s`

## `--log-file` {#--log-file}

-   ログファイル
-   デフォルト: `""`
-   このオプションが設定されていない場合、ログは「stderr」に出力されます。このオプションが設定されている場合、ログは対応するファイルに出力されます。

## `--log-general` {#--log-general}

-   [一般ログ](/system-variables.md#tidb_general_log)のファイル名
-   デフォルト: `""`
-   このオプションが設定されていない場合、一般ログはデフォルトで[`--log-file`](#--log-file)で指定されたファイルに書き込まれます。

## `--log-slow-query` {#--log-slow-query}

-   スロークエリログのディレクトリ
-   デフォルト: `""`
-   このオプションが設定されていない場合、ログはデフォルトで`--log-file`で指定されたファイルに出力されます。

## `--metrics-addr` {#--metrics-addr}

-   Prometheus Pushgatewayアドレス
-   デフォルト: `""`
-   空のままにすると、Prometheus クライアントのプッシュが停止します。
-   形式は`--metrics-addr=192.168.100.115:9091`です。

## `--metrics-interval` {#--metrics-interval}

-   Prometheusクライアントのプッシュ間隔（秒）
-   デフォルト: `15s`
-   値を 0 に設定すると、Prometheus クライアントのプッシュが停止します。

## `-P` {#-p}

-   TiDBサービスの監視ポート
-   デフォルト: `"4000"`
-   TiDBサーバーはこのポートからの MySQL クライアント要求を受け入れます。

## `--path` {#--path}

-   「unistore」のようなローカルストレージエンジンのデータディレクトリへのパス
-   `--store = tikv`場合、パスを指定する必要があります。 `--store = unistore`場合、パスを指定しないとデフォルト値が使用されます。
-   TiKVのような分散ストレージエンジンの場合、 `--path`実際のPDアドレスを指定します。PDサーバーを192.168.100.113:2379、192.168.100.114:2379、192.168.100.115:2379にデプロイすると仮定すると、 `--path`値は「192.168.100.113:2379、192.168.100.114:2379、192.168.100.115:2379」となります。
-   デフォルト: `"/tmp/tidb"`
-   純粋なインメモリ TiDB を有効にするには、 `tidb-server --store=unistore --path=""`使用します。

## `--proxy-protocol-fallbackable` {#--proxy-protocol-fallbackable}

-   PROXYプロトコルフォールバックモードを有効にするかどうかを制御します。このパラメータを`true`に設定すると、TiDBはPROXYプロトコル仕様を使用せず、PROXYプロトコルヘッダーを送信せずに、 `--proxy-protocol-networks`に属するクライアント接続を受け入れます。デフォルトでは、TiDBは`--proxy-protocol-networks`に属し、PROXYプロトコルヘッダーを送信するクライアント接続のみを受け入れます。
-   デフォルト値: `false`

## `--proxy-protocol-networks` {#--proxy-protocol-networks}

-   [PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)使用して TiDB に接続できるプロキシ サーバーの IP アドレスのリスト。
-   デフォルト: `""`
-   通常、リバースプロキシを経由してTiDBにアクセスする場合、TiDBはリバースプロキシサーバーのIPアドレスをクライアントのIPアドレスとして取得します。PROXYプロトコルを有効にすると、HAProxyなどのこのプロトコルをサポートするリバースプロキシは、実際のクライアントIPアドレスをTiDBに渡すことができます。
-   このフラグを設定すると、TiDBは設定された送信元IPアドレスがPROXYプロトコルを使用してTiDBに接続することを許可します。PROXY以外のプロトコルが使用されている場合、この接続は拒否されます。その他のアドレスはPROXYプロトコルを使用せずにTiDBに接続できます。このフラグを空のままにすると、どのIPアドレスもPROXYプロトコルを使用してTiDBに接続できなくなります。値は、IPアドレス（192.168.1.50）またはCIDR（192.168.1.0/24）で、区切り文字として`,`使用します。3 `*`任意のIPアドレスを意味します。

> **Warning:**
>
> `*` 、任意の IP アドレスのクライアントが自身の IP アドレスを報告できるようになるため、セキュリティリスクが生じる可能性があるため、注意して使用してください。また、 `*`使用すると、 `--proxy-protocol-fallbackable` `true`に設定しないと、TiDB に直接接続する内部コンポーネント（TiDB Dashboardなど）が利用できなくなる可能性があります。

> **Note:**
>
> PROXYプロトコルを有効にしたAWS Network Load Balancer（NLB）を使用するには、NLBの`target group`プロパティを設定する必要があります。具体的には、 `proxy_protocol_v2.client_to_server.header_place`を`on_first_ack`に設定します。同時に、AWSサポートにチケットを送信する必要があります。PROXYプロトコルを有効にすると、クライアントはサーバーからのハンドシェイクパケットの取得に失敗し、クライアントがタイムアウトするまでパケットがブロックされることに注意してください。これは、NLBがクライアントがデータを送信した後にのみプロキシパケットを送信するためです。ただし、クライアントがデータパケットを送信する前に、サーバーから送信されたデータパケットは内部ネットワークでドロップされます。

## `--proxy-protocol-header-timeout` {#--proxy-protocol-header-timeout}

-   PROXYプロトコルヘッダー読み取りのタイムアウト
-   デフォルト: `5` (秒)

> **Warning:**
>
> バージョン6.3.0以降、このパラメータは非推奨となりました。ネットワークデータの初回読み取り時にPROXYプロトコルヘッダーが読み込まれるため、このパラメータは使用されなくなりました。このパラメータを非推奨にすることで、ネットワークデータの初回読み取り時に設定されるタイムアウトに影響を与えなくなります。

> **Note:**
>
> 値を`0`に設定しないでください。特別な状況を除き、デフォルト値を使用してください。

## `--report-status` {#--report-status}

-   ステータスレポートとpprofツールを有効（ `true` ）または無効（ `false` ）にする
-   デフォルト: `true`
-   このパラメータを`true`に設定すると、メトリクスとpprofが有効になります。 `false`に設定すると、メトリクスとpprofが無効になります。

## `--run-ddl` {#--run-ddl}

-   `tidb-server` DDL文を実行するかどうかを確認し、クラスタ内の`tidb-server`の数が2を超える場合に設定する
-   デフォルト: `true`
-   値は (true) または (false) になります。 (true) は、 `tidb-server` DDL 自体を実行することを示します。 (false) は、 `tidb-server` DDL 自体を実行しないことを示します。

## `--socket string` {#--socket-string}

-   TiDB サービスは、外部接続に Unix ソケット ファイルを使用します。
-   デフォルト: `""`
-   `/tmp/tidb.sock`使用して Unix ソケット ファイルを開きます。

## `--status` {#--status}

-   TiDBサーバーのステータスレポートポート
-   デフォルト: `"10080"`
-   このポートはサーバー内部データを取得するために使用されます。データには[Prometheusメトリクス](https://prometheus.io/)と[専門家](https://golang.org/pkg/net/http/pprof/)含まれます。
-   Prometheus メトリックには`"http://host:status_port/metrics"`でアクセスできます。
-   pprof データには`"http://host:status_port/debug/pprof"`でアクセスできます。

## `--status-host` {#--status-host}

-   TiDBサービスのステータスを監視するために使用される`HOST`
-   デフォルト: `0.0.0.0`

## `--store` {#--store}

-   最下層で TiDB が使用するストレージエンジンを指定します
-   デフォルト: `"unistore"`
-   「unistore」または「tikv」を選択できます。（「unistore」はローカルストレージエンジン、「tikv」は分散ストレージエンジンです）

## `--temp-dir` {#--temp-dir}

-   TiDBの一時ディレクトリ
-   デフォルト: `"/tmp/tidb"`

## `--tidb-service-scope` {#--tidb-service-scope}

-   現在の TiDB インスタンスの初期値として[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)指定します。
-   デフォルト: `""`

## `--token-limit` {#--token-limit}

-   TiDBで同時に実行できるセッション数。トラフィック制御に使用されます。
-   デフォルト: `1000`
-   同時セッション数が`token-limit`より大きい場合、リクエストはブロックされ、トークンを解放する操作が終了するまで待機します。

## `-V` {#-v}

-   TiDBのバージョンを出力します
-   デフォルト: `""`

## `--plugin-dir` {#--plugin-dir}

-   プラグインのストレージディレクトリ。
-   デフォルト: `"/data/deploy/plugin"`

## `--plugin-load` {#--plugin-load}

-   ロードするプラグインの名前。それぞれはコンマで区切られます。
-   デフォルト: `""`

## `--affinity-cpus` {#--affinity-cpus}

-   TiDBサーバーのCPUアフィニティをカンマ区切りで設定します。例：&quot;1,2,3&quot;。
-   デフォルト: `""`

## `--redact` {#--redact}

-   サブコマンド`collect-log`使用するときに、 TiDBサーバーがログ ファイルを非感度化するかどうかを決定します。
-   デフォルト: false
-   値が`true`の場合、マスキング操作となり、 `‹ ›`マーク記号で囲まれたすべてのフィールドが`?`に置き換えられます。値が`false`の場合、リストア操作となり、すべてのマーク記号が削除されます。この機能を使用するには、 `./tidb-server --redact=xxx collect-log <input> <output>`実行して、 `<input>`で指定された TiDBサーバーログファイルを非感応化またはリストアし、 `<output>`に出力します。詳細については、システム変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log)参照してください。

## `--repair-mode` {#--repair-mode}

-   データ修復シナリオでのみ使用される修復モードを有効にするかどうかを決定します。
-   デフォルト: `false`

## `--repair-list` {#--repair-list}

-   修復モードで修復されるテーブルの名前。
-   デフォルト: `""`
