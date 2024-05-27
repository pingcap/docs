---
title: Configuration Options
summary: TiDB の構成オプションについて学習します。
---

# コンフィグレーションオプション {#configuration-options}

TiDB クラスターを起動するときに、コマンドライン オプションまたは環境変数を使用して構成できます。このドキュメントでは、TiDB のコマンド オプションについて説明します。デフォルトの TiDB ポートは、クライアント要求の場合は`4000` 、ステータス レポートの場合は`10080`です。

## <code>--advertise-address</code> {#code-advertise-address-code}

-   TiDBサーバーにログインするためのIPアドレス
-   デフォルト: `""`
-   このアドレスは、TiDB クラスターの残りの部分とユーザーからアクセスできる必要があります。

## <code>--config</code> {#code-config-code}

-   設定ファイル
-   デフォルト: `""`
-   設定ファイルを指定している場合、TiDB は設定ファイルを読み取ります。コマンドライン オプションにも対応する設定が存在する場合、TiDB はコマンドライン オプションの設定を使用して設定ファイルの設定を上書きします。詳細な設定情報については、 [TiDBコンフィグレーションファイルの説明](/tidb-configuration-file.md)参照してください。

## <code>--config-check</code> {#code-config-check-code}

-   設定ファイルの有効性をチェックして終了します
-   デフォルト: `false`

## <code>--config-strict</code> {#code-config-strict-code}

-   設定ファイルの有効性を強制する
-   デフォルト: `false`

## <code>--cors</code> {#code-cors-code}

-   TiDB HTTPステータスサービスのクロスオリジンリクエスト共有（CORS）リクエストの値`Access-Control-Allow-Origin`を指定します。
-   デフォルト: `""`

## <code>--enable-binlog</code> {#code-enable-binlog-code}

-   TiDBbinlog生成を有効または無効にする
-   デフォルト: `false`

## <code>--host</code> {#code-host-code}

-   TiDBサーバーが監視するホストアドレス
-   デフォルト: `"0.0.0.0"`
-   TiDBサーバーはこのアドレスを監視します。
-   `"0.0.0.0"`アドレスは、デフォルトですべてのネットワーク カードを監視します。複数のネットワーク カードがある場合は、 `192.168.100.113`のように、サービスを提供するネットワーク カードを指定します。

## <code>--initialize-insecure</code> {#code-initialize-insecure-code}

-   tidb-server を非セキュアモードでブートストラップする
-   デフォルト: `true`

## <code>--initialize-secure</code> {#code-initialize-secure-code}

-   tidb-server をセキュアモードでブートストラップする
-   デフォルト: `false`

## <code>--initialize-sql-file</code> {#code-initialize-sql-file-code}

-   TiDBクラスタを初めて起動したときに実行されるSQLスクリプト。詳細については[構成項目`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)参照してください。
-   デフォルト: `""`

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト: `"info"`
-   `"warn"` `"fatal"` `"error"` `"debug"` `"info"`

## <code>--lease</code> {#code-lease-code}

-   スキーマ リースの期間。何をするのか理解していない場合は、値を変更するのは**危険**です。
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

-   Prometheusクライアントのプッシュ間隔（秒単位）
-   デフォルト: `15s`
-   値を 0 に設定すると、Prometheus クライアントのプッシュが停止します。

## <code>-P</code> {#code-p-code}

-   TiDBサービスの監視ポート
-   デフォルト: `"4000"`
-   TiDBサーバーはこのポートからの MySQL クライアント要求を受け入れます。

## <code>--path</code> {#code-path-code}

-   「unistore」のようなローカルstorageエンジンのデータディレクトリへのパス
-   `--store = tikv`の場合、パスを指定する必要があります。 `--store = unistore`の場合、パスを指定しないとデフォルト値が使用されます。
-   TiKV のような分散storageエンジンの場合、 `--path`実際の PD アドレスを指定します。PDサーバーを 192.168.100.113:2379、192.168.100.114:2379、および 192.168.100.115:2379 にデプロイすると仮定すると、値`--path`は「192.168.100.113:2379、192.168.100.114:2379、192.168.100.115:2379」になります。
-   デフォルト: `"/tmp/tidb"`
-   `tidb-server --store=unistore --path=""`使用すると、純粋なインメモリ TiDB を有効にすることができます。

## <code>--proxy-protocol-fallbackable</code> {#code-proxy-protocol-fallbackable-code}

-   PROXY プロトコル フォールバック モードを有効にするかどうかを制御します。このパラメータを`true`に設定すると、TiDB は PROXY プロトコル仕様を使用せずに、または PROXY プロトコル ヘッダーを送信せずに、 `--proxy-protocol-networks`に属するクライアント接続を受け入れます。デフォルトでは、TiDB は`--proxy-protocol-networks`に属し、PROXY プロトコル ヘッダーを送信するクライアント接続のみを受け入れます。
-   デフォルト値: `false`

## <code>--proxy-protocol-networks</code> {#code-proxy-protocol-networks-code}

-   [PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を使用して TiDB に接続できるプロキシ サーバーの IP アドレスのリスト。
-   デフォルト: `""`
-   通常、リバース プロキシの背後で TiDB にアクセスすると、TiDB はリバース プロキシサーバーの IP アドレスをクライアントの IP アドレスとして取得します。PROXY プロトコルを有効にすると、HAProxy などのこのプロトコルをサポートするリバース プロキシは、実際のクライアント IP アドレスを TiDB に渡すことができます。
-   このフラグを設定すると、TiDB は設定されたソース IP アドレスが PROXY プロトコルを使用して TiDB に接続できるようにします。PROXY 以外のプロトコルが使用されている場合、この接続は拒否されます。その他のアドレスは PROXY プロトコルを使用せずに TiDB に接続できます。このフラグが空のままの場合、どの IP アドレスも PROXY プロトコルを使用して TiDB に接続できません。値には、 `,`を区切り文字として IP アドレス (192.168.1.50) または CIDR (192.168.1.0/24) を指定できます。3 `*`任意の IP アドレスを意味します。

> **警告：**
>
> `*` 、任意の IP アドレスのクライアントがその IP アドレスを報告できるようにすることでセキュリティ リスクを招く可能性があるため、注意して使用してください。また、 `*`を使用すると、 `--proxy-protocol-fallbackable` `true`に設定しない限り、TiDB に直接接続する内部コンポーネント(TiDB ダッシュボードなど) が使用できなくなる可能性があります。

> **注記：**
>
> PROXY プロトコルを有効にした AWS Network Load Balancer (NLB) を使用するには、NLB の`target group`プロパティを設定する必要があります。具体的には、 `proxy_protocol_v2.client_to_server.header_place`を`on_first_ack`に設定します。同時に、AWS サポートにチケットを送信する必要があります。PROXY プロトコルを有効にすると、クライアントはサーバーからハンドシェイク パケットを取得できなくなり、クライアントがタイムアウトするまでパケットがブロックされることに注意してください。これは、NLB がクライアントがデータを送信した後にのみプロキシ パケットを送信するためです。ただし、クライアントがデータ パケットを送信する前に、サーバーから送信されたデータ パケットは内部ネットワークでドロップされます。

## <code>--proxy-protocol-header-timeout</code> {#code-proxy-protocol-header-timeout-code}

-   PROXYプロトコルヘッダー読み取りのタイムアウト
-   デフォルト: `5` (秒)

> **警告：**
>
> v6.3.0 以降、このパラメータは非推奨です。ネットワーク データが初めて読み取られるときに PROXY プロトコル ヘッダーが読み取られるため、このパラメータは使用されなくなりました。このパラメータを非推奨にすると、ネットワーク データが初めて読み取られるときに設定されるタイムアウトに影響が及ばなくなります。

> **注記：**
>
> 値を`0`に設定しないでください。特別な状況を除いて、デフォルト値を使用してください。

## <code>--report-status</code> {#code-report-status-code}

-   ステータスレポートとpprofツールを有効（ `true` ）または無効（ `false` ）にする
-   デフォルト: `true`
-   `true`に設定すると、このパラメータはメトリックと pprof を有効にします。 `false`に設定すると、このパラメータはメトリックと pprof を無効にします。

## <code>--run-ddl</code> {#code-run-ddl-code}

-   `tidb-server` DDL文を実行するかどうかを確認し、クラスタ内の`tidb-server`の数が2を超える場合に設定する
-   デフォルト: `true`
-   値は (true) または (false) になります。 (true) は、 `tidb-server` DDL 自体を実行することを示します。 (false) は、 `tidb-server`が DDL 自体を実行しないことを示します。

## <code>--socket string</code> {#code-socket-string-code}

-   TiDB サービスは、外部接続に Unix ソケット ファイルを使用します。
-   デフォルト: `""`
-   `/tmp/tidb.sock`使用して Unix ソケット ファイルを開きます。

## <code>--status</code> {#code-status-code}

-   TiDBサーバーのステータスレポートポート
-   デフォルト: `"10080"`
-   このポートはサーバーの内部データを取得するために使用されます。データには[プロメテウスメトリクス](https://prometheus.io/)と[専門家](https://golang.org/pkg/net/http/pprof/)が含まれます。
-   Prometheus メトリックには`"http://host:status_port/metrics"`でアクセスできます。
-   pprof データには`"http://host:status_port/debug/pprof"`でアクセスできます。

## <code>--status-host</code> {#code-status-host-code}

-   TiDBサービスのステータスを監視するために使用される`HOST`
-   デフォルト: `0.0.0.0`

## <code>--store</code> {#code-store-code}

-   最レイヤーでTiDBが使用するstorageエンジンを指定します
-   デフォルト: `"unistore"`
-   「unistore」または「tikv」を選択できます。(「unistore」はローカルstorageエンジン、「tikv」は分散storageエンジンです)

## <code>--temp-dir</code> {#code-temp-dir-code}

-   TiDBの一時ディレクトリ
-   デフォルト: `"/tmp/tidb"`

## <code>--tidb-service-scope</code> {#code-tidb-service-scope-code}

-   現在の TiDB インスタンスの初期値[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)を指定します。
-   デフォルト: `""`

## <code>--token-limit</code> {#code-token-limit-code}

-   TiDB で同時に実行できるセッションの数。トラフィック制御に使用されます。
-   デフォルト: `1000`
-   同時セッション数が`token-limit`より大きい場合、リクエストはブロックされ、トークンを解放する操作が終了するまで待機します。

## <code>-V</code> {#code-v-code}

-   TiDBのバージョンを出力します
-   デフォルト: `""`

## <code>--plugin-dir</code> {#code-plugin-dir-code}

-   プラグインのstorageディレクトリ。
-   デフォルト: `"/data/deploy/plugin"`

## <code>--plugin-load</code> {#code-plugin-load-code}

-   ロードするプラグインの名前。それぞれカンマで区切られます。
-   デフォルト: `""`

## <code>--affinity-cpus</code> {#code-affinity-cpus-code}

-   TiDB サーバーの CPU アフィニティをコンマで区切って設定します。たとえば、「1,2,3」などです。
-   デフォルト: `""`

## <code>--redact</code> {#code-redact-code}

-   サブコマンド`collect-log`を使用するときに、 TiDBサーバーがログ ファイルを非感度化するかどうかを決定します。
-   デフォルト: false
-   値が`true`の場合はマスキング操作となり、 `‹ ›`マーク記号で囲まれたすべてのフィールドが`?`に置き換えられます。値が`false`の場合は復元操作となり、すべてのマーク記号が削除されます。この機能を使用するには、 `./tidb-server --redact=xxx collect-log <input> <output>`実行して、 `<input>`で指定した TiDBサーバーログ ファイルを非感応化または復元し、 `<output>`に出力します。詳細については、システム変数[`tidb_redact_log`](/system-variables.md#tidb_redact_log)を参照してください。

## <code>--repair-mode</code> {#code-repair-mode-code}

-   データ修復シナリオでのみ使用される修復モードを有効にするかどうかを決定します。
-   デフォルト: `false`

## <code>--repair-list</code> {#code-repair-list-code}

-   修復モードで修復するテーブルの名前。
-   デフォルト: `""`
