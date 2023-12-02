---
title: Configuration Options
summary: Learn the configuration options in TiDB.
---

# コンフィグレーションオプション {#configuration-options}

TiDB クラスターを開始するときは、コマンドライン オプションまたは環境変数を使用して構成できます。このドキュメントでは、TiDB のコマンド オプションを紹介します。デフォルトの TiDB ポートは、クライアント要求用に`4000` 、ステータス レポート用に`10080`です。

## <code>--advertise-address</code> {#code-advertise-address-code}

-   TiDBサーバーへのログインに使用する IP アドレス
-   デフォルト: `""`
-   このアドレスには、TiDB クラスターの残りの部分とユーザーがアクセスできる必要があります。

## <code>--config</code> {#code-config-code}

-   設定ファイル
-   デフォルト: `""`
-   構成ファイルを指定した場合、TiDB は構成ファイルを読み取ります。対応する設定がコマンド ライン オプションにも存在する場合、TiDB はコマンド ライン オプションの設定を使用して、設定ファイル内の設定を上書きします。詳しい構成情報については、 [TiDBコンフィグレーションファイルの説明](/tidb-configuration-file.md)を参照してください。

## <code>--config-check</code> {#code-config-check-code}

-   設定ファイルの有効性を確認して終了します
-   デフォルト: `false`

## <code>--config-strict</code> {#code-config-strict-code}

-   構成ファイルの有効性を強制します
-   デフォルト: `false`

## <code>--cors</code> {#code-cors-code}

-   TiDB HTTP ステータス サービスの Cross-Origin Request Sharing (CORS) リクエストに`Access-Control-Allow-Origin`値を指定します。
-   デフォルト: `""`

## <code>--enable-binlog</code> {#code-enable-binlog-code}

-   TiDBbinlogの生成を有効または無効にします。
-   デフォルト: `false`

## <code>--host</code> {#code-host-code}

-   TiDBサーバーが監視するホスト アドレス
-   デフォルト: `"0.0.0.0"`
-   TiDBサーバーはこのアドレスを監視します。
-   `"0.0.0.0"`アドレスはデフォルトですべてのネットワーク カードを監視します。複数のネットワーク カードがある場合は、サービスを提供するネットワーク カードを指定します ( `192.168.100.113`など)。

## <code>--initialize-insecure</code> {#code-initialize-insecure-code}

-   tidb-server を安全でないモードでブートストラップする
-   デフォルト: `true`

## <code>--initialize-secure</code> {#code-initialize-secure-code}

-   tidb-server をセキュアモードでブートストラップする
-   デフォルト: `false`

## <code>--initialize-sql-file</code> {#code-initialize-sql-file-code}

-   TiDB クラスターが初めて起動されるときに実行される SQL スクリプト。詳細は[構成項目`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660)を参照
-   デフォルト: `""`

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト: `"info"`
-   オプションの値: `"debug"` 、 `"info"` 、 `"warn"` 、 `"error"` 、 `"fatal"`

## <code>--lease</code> {#code-lease-code}

-   スキーマのリース期間。何をするのか理解していない場合に値を変更するのは**危険**です。
-   デフォルト: `45s`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト: `""`
-   このオプションが設定されていない場合、ログは「stderr」に出力されます。このオプションを設定すると、対応するファイルにログが出力されます。

## <code>--log-slow-query</code> {#code-log-slow-query-code}

-   スロークエリログのディレクトリ
-   デフォルト: `""`
-   このオプションが設定されていない場合、デフォルトでログは`--log-file`で指定されたファイルに出力されます。

## <code>--metrics-addr</code> {#code-metrics-addr-code}

-   Prometheus プッシュゲートウェイのアドレス
-   デフォルト: `""`
-   空のままにすると、Prometheus クライアントのプッシュが停止されます。
-   形式は`--metrics-addr=192.168.100.115:9091`です。

## <code>--metrics-interval</code> {#code-metrics-interval-code}

-   Prometheus クライアントのプッシュ間隔 (秒)
-   デフォルト: `15s`
-   値を 0 に設定すると、Prometheus クライアントのプッシュが停止されます。

## <code>-P</code> {#code-p-code}

-   TiDB サービスのモニタリング ポート
-   デフォルト: `"4000"`
-   TiDBサーバーは、このポートから MySQL クライアント リクエストを受け入れます。

## <code>--path</code> {#code-path-code}

-   「unistore」などのローカルstorageエンジンのデータ ディレクトリへのパス
-   `--store = tikv`の場合は、パスを指定する必要があります。 `--store = unistore`の場合、パスを指定しない場合はデフォルト値が使用されます。
-   TiKV のような分散storageエンジンの場合、 `--path`実際の PD アドレスを指定します。 PDサーバーを 192.168.100.113:2379、192.168.100.114:2379、および 192.168.100.115:2379 に展開すると仮定すると、 `--path`の値は「192.168.100.113:2379、192.168.100.114: 2379、192.168.100.115:2379&quot; 。
-   デフォルト: `"/tmp/tidb"`
-   `tidb-server --store=unistore --path=""`使用すると、純粋なインメモリ TiDB を有効にできます。

## <code>--proxy-protocol-fallbackable</code> {#code-proxy-protocol-fallbackable-code}

-   PROXY プロトコル フォールバック モードを有効にするかどうかを制御します。このパラメーターが`true`に設定されている場合、TiDB は、PROXY プロトコル仕様を使用せず、または PROXY プロトコル ヘッダーを送信せずに、 `--proxy-protocol-networks`に属するクライアント接続を受け入れます。デフォルトでは、TiDB は`--proxy-protocol-networks`に属し、PROXY プロトコル ヘッダーを送信するクライアント接続のみを受け入れます。
-   デフォルト値: `false`

## <code>--proxy-protocol-networks</code> {#code-proxy-protocol-networks-code}

-   [プロキシプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を使用して TiDB に接続できるプロキシ サーバーの IP アドレスのリスト。
-   デフォルト: `""`
-   一般に、リバース プロキシの背後で TiDB にアクセスすると、TiDB はリバース プロキシサーバーの IP アドレスをクライアントの IP アドレスとして取得します。 PROXY プロトコルを有効にすることにより、このプロトコルをサポートする HAProxy などのリバース プロキシは、実際のクライアント IP アドレスを TiDB に渡すことができます。
-   このフラグを設定すると、TiDB は、設定されたソース IP アドレスが PROXY プロトコルを使用して TiDB に接続できるようにします。 PROXY 以外のプロトコルが使用されている場合、この接続は拒否されます。他のアドレスは、PROXY プロトコルを使用せずに TiDB に接続できます。このフラグを空のままにすると、どの IP アドレスも PROXY プロトコルを使用して TiDB に接続できなくなります。値には、区切り文字として`,`を使用した IP アドレス (192.168.1.50) または CIDR (192.168.1.0/24) を指定できます。 `*`任意の IP アドレスを意味します。

> **警告：**
>
> `*`を使用すると、任意の IP アドレスのクライアントがその IP アドレスを報告できるようになるため、セキュリティ リスクが生じる可能性があるため、注意して使用してください。さらに、 `*`を使用すると、 `--proxy-protocol-fallbackable` `true`に設定されていない限り、TiDB に直接接続する内部コンポーネント(TiDB ダッシュボードなど) が使用できなくなる可能性があります。

> **注記：**
>
> PROXY プロトコルを有効にして AWS Network Load Balancer (NLB) を使用するには、NLB の`target group`プロパティを設定する必要があります。具体的には`proxy_protocol_v2.client_to_server.header_place` ～ `on_first_ack`を設定します。同時に、AWS サポートにチケットを送信する必要があります。 PROXY プロトコルを有効にすると、クライアントはサーバーからのハンドシェイク パケットの取得に失敗し、クライアントがタイムアウトになるまでパケットはブロックされることに注意してください。これは、NLB がクライアントがデータを送信した後にのみプロキシ パケットを送信するためです。ただし、クライアントがデータ パケットを送信する前に、サーバーから送信されたデータ パケットは内部ネットワークでドロップされます。

## <code>--proxy-protocol-header-timeout</code> {#code-proxy-protocol-header-timeout-code}

-   PROXY プロトコル ヘッダー読み取りのタイムアウト
-   デフォルト: `5` (秒)

> **警告：**
>
> v6.3.0 以降、このパラメータは非推奨になりました。初めてネットワーク データが読み取られるときに PROXY プロトコル ヘッダーが読み取られるため、これは使用されなくなりました。このパラメータを非推奨にすることで、ネットワーク データが初めて読み取られるときに設定されるタイムアウトに影響を与えることがなくなります。

> **注記：**
>
> 値を`0`に設定しないでください。特別な状況を除いてデフォルト値を使用してください。

## <code>--report-status</code> {#code-report-status-code}

-   ステータス レポートと pprof ツールを有効 ( `true` ) または無効 ( `false` ) にします。
-   デフォルト: `true`
-   このパラメーターを`true`に設定すると、メトリックと pprof が有効になります。このパラメータを`false`に設定すると、メトリクスと pprof が無効になります。

## <code>--run-ddl</code> {#code-run-ddl-code}

-   `tidb-server`が DDL ステートメントを実行するかどうかを確認し、クラスター内で`tidb-server`の数が 2 を超えたときに設定します。
-   デフォルト: `true`
-   値は (true) または (false) です。 (true) は、 `tidb-server` DDL 自体を実行することを示します。 (false) は、 `tidb-server` DDL 自体を実行しないことを示します。

## <code>--socket string</code> {#code-socket-string-code}

-   TiDB サービスは、外部接続に unix ソケット ファイルを使用します。
-   デフォルト: `""`
-   UNIX ソケット ファイルを開くには`/tmp/tidb.sock`を使用します。

## <code>--status</code> {#code-status-code}

-   TiDBサーバーのステータス レポート ポート
-   デフォルト: `"10080"`
-   このポートはサーバーの内部データを取得するために使用されます。データには[プロメテウスのメトリクス](https://prometheus.io/)と[プロフ](https://golang.org/pkg/net/http/pprof/)が含まれます。
-   Prometheus メトリクスには`"http://host:status_port/metrics"`でアクセスできます。
-   pprof データには`"http://host:status_port/debug/pprof"`によってアクセスできます。

## <code>--status-host</code> {#code-status-host-code}

-   `HOST` TiDB サービスのステータスを監視するために使用されます
-   デフォルト: `0.0.0.0`

## <code>--store</code> {#code-store-code}

-   最レイヤーの TiDB によって使用されるstorageエンジンを指定します
-   デフォルト: `"unistore"`
-   「unistore」または「tikv」を選択できます。 (「unistore」はローカルstorageエンジン、「tikv」は分散storageエンジンです)

## <code>--temp-dir</code> {#code-temp-dir-code}

-   TiDB の一時ディレクトリ
-   デフォルト: `"/tmp/tidb"`

## <code>--token-limit</code> {#code-token-limit-code}

-   TiDB で同時に実行できるセッションの数。交通規制に使われています。
-   デフォルト: `1000`
-   同時セッションの数が`token-limit`より大きい場合、リクエストはブロックされ、完了した操作がトークンを解放するのを待ちます。

## <code>-V</code> {#code-v-code}

-   TiDBのバージョンを出力します
-   デフォルト: `""`

## <code>--plugin-dir</code> {#code-plugin-dir-code}

-   プラグインのstorageディレクトリ。
-   デフォルト: `"/data/deploy/plugin"`

## <code>--plugin-load</code> {#code-plugin-load-code}

-   ロードするプラグインの名前。それぞれをカンマで区切ります。
-   デフォルト: `""`

## <code>--affinity-cpus</code> {#code-affinity-cpus-code}

-   TiDB サーバーの CPU アフィニティをカンマで区切って設定します。たとえば、「1、2、3」です。
-   デフォルト: `""`

## <code>--repair-mode</code> {#code-repair-mode-code}

-   データ修復シナリオでのみ使用される修復モードを有効にするかどうかを決定します。
-   デフォルト: `false`

## <code>--repair-list</code> {#code-repair-list-code}

-   修復モードで修復するテーブルの名前。
-   デフォルト: `""`
