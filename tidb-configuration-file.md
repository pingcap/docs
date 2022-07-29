---
title: TiDB Configuration File
summary: Learn the TiDB configuration file options that are not involved in command line options.
---

<!-- markdownlint-disable MD001 -->

<!-- markdownlint-disable MD024 -->

# TiDBConfiguration / コンフィグレーションファイル {#tidb-configuration-file}

TiDB構成ファイルは、コマンドラインパラメーターよりも多くのオプションをサポートしています。デフォルトの構成ファイル[`config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example)をダウンロードして、名前を`config.toml`に変更できます。このドキュメントでは、 [コマンドラインオプション](/command-line-flags-for-tidb-configuration.md)に関係のないオプションについてのみ説明します。

### <code>split-table</code> {#code-split-table-code}

-   テーブルごとに個別のリージョンを作成するかどうかを決定します。
-   デフォルト値： `true`
-   多数のテーブル（たとえば、10万を超えるテーブル）を作成する必要がある場合は、 `false`に設定することをお勧めします。

### <code>token-limit</code> {#code-token-limit-code}

-   リクエストを同時に実行できるセッションの数。
-   タイプ：整数
-   デフォルト値： `1000`
-   最小値： `1`
-   最大値（64ビットプラットフォーム）： `18446744073709551615`
-   最大値（32ビットプラットフォーム）： `4294967295`

### <code>oom-use-tmp-storage</code> {#code-oom-use-tmp-storage-code}

-   単一のSQLステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えたときに、一部のオペレータの一時ストレージを有効にするかどうかを制御します。
-   デフォルト値： `true`

### <code>tmp-storage-path</code> {#code-tmp-storage-path-code}

-   単一のSQLステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリー割り当てを超えた場合に、一部のオペレーターの一時記憶域パスを指定します。
-   デフォルト値： `<temporary directory of OS>/<OS user ID>_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage` 。 `MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=`は`<host>:<port>/<statusHost>:<statusPort>`の`Base64`エンコード結果です。
-   この構成は、 `oom-use-tmp-storage`が`true`の場合にのみ有効になります。

### <code>tmp-storage-quota</code> {#code-tmp-storage-quota-code}

-   `tmp-storage-path`のストレージのクォータを指定します。単位はバイトです。
-   単一のSQLステートメントが一時ディスクを使用し、TiDBサーバーの一時ディスクの合計ボリュームがこの構成値を超えると、現在のSQL操作がキャンセルされ、 `Out of Global Storage Quota!`エラーが返されます。
-   この構成の値が`0`より小さい場合、上記のチェックと制限は適用されません。
-   デフォルト値： `-1`
-   `tmp-storage-path`の残りの使用可能なストレージが`tmp-storage-quota`で定義された値よりも小さい場合、TiDBサーバーは起動時にエラーを報告し、終了します。

### <code>lease</code> {#code-lease-code}

-   DDLリースのタイムアウト。
-   デフォルト値： `45s`
-   単位：秒

### <code>compatible-kill-query</code> {#code-compatible-kill-query-code}

-   `KILL`ステートメントをMySQL互換に設定するかどうかを決定します。
-   デフォルト値： `false`
-   TiDBでの`KILL xxx`の動作は、MySQLでの動作とは異なります。 TiDBには`TIDB`キーワード、つまり`KILL TIDB xxx`が必要です。 `compatible-kill-query`が`true`に設定されている場合、 `TIDB`キーワードは必要ありません。
-   ユーザーが<kbd>Ctrl</kbd> + <kbd>C</kbd>を押したときのMySQLコマンドラインクライアントのデフォルトの動作は、バックエンドへの新しい接続を作成し、その新しい接続で`KILL`ステートメントを実行することであるため、この区別は重要です。ロードバランサーまたはプロキシが新しい接続を元のセッションとは異なるTiDBサーバーインスタンスに送信した場合、間違ったセッションが終了し、クラスタを使用するアプリケーションが中断される可能性があります。 `KILL`ステートメントで参照している接続が、 `KILL`ステートメントの送信先と同じサーバー上にあることが確実な場合にのみ、 `compatible-kill-query`を有効にします。

### <code>check-mb4-value-in-utf8</code> {#code-check-mb4-value-in-utf8-code}

-   `utf8mb4`文字チェックを有効にするかどうかを決定します。この機能を有効にすると、文字セットが`utf8`で、 `mb4`文字が`utf8`に挿入されると、エラーが返されます。
-   デフォルト値： `false`

### <code>treat-old-version-utf8-as-utf8mb4</code> {#code-treat-old-version-utf8-as-utf8mb4-code}

-   古いテーブルの`utf8`文字セットを`utf8mb4`として扱うかどうかを決定します。
-   デフォルト値： `true`

### <code>alter-primary-key</code> （非推奨） {#code-alter-primary-key-code-deprecated}

-   主キー制約を列に追加するか、列から削除するかを決定します。
-   デフォルト値： `false`
-   このデフォルト設定では、主キー制約の追加または削除はサポートされていません。この機能を有効にするには、 `alter-primary-key`を`true`に設定します。ただし、スイッチがオンになる前にテーブルがすでに存在し、その主キー列のデータ型が整数である場合、この構成項目を`true`に設定しても、列から主キーを削除することはできません。

> **ノート：**
>
> この構成アイテムは非推奨になり、現在、値`@tidb_enable_clustered_index`が`INT_ONLY`の場合にのみ有効になります。主キーを追加または削除する必要がある場合は、テーブルを作成するときに代わりに`NONCLUSTERED`キーワードを使用してください。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化されたインデックス](/clustered-indexes.md)を参照してください。

### <code>server-version</code> {#code-server-version-code}

-   次の状況でTiDBによって返されるバージョン文字列を変更します。
    -   内蔵の`VERSION()`機能を使用する場合。
    -   TiDBがクライアントへの初期接続を確立し、サーバーのバージョン文字列を含む初期ハンドシェイクパケットを返す場合。詳細については、 [MySQL初期ハンドシェイクパケット](https://dev.mysql.com/doc/internals/en/connection-phase-packets.html#packet-Protocol::Handshake)を参照してください。
-   デフォルト値： &quot;&quot;
-   デフォルトでは、TiDBバージョン文字列の形式は`5.7.${mysql_latest_minor_version}-TiDB-${tidb_version}`です。

### <code>repair-mode</code> {#code-repair-mode-code}

-   信頼できない修復モードを有効にするかどうかを決定します。 `repair-mode`を`true`に設定すると、 `repair-table-list`の不良テーブルをロードできません。
-   デフォルト値： `false`
-   `repair`構文はデフォルトではサポートされていません。これは、TiDBの起動時にすべてのテーブルがロードされることを意味します。

### <code>repair-table-list</code> {#code-repair-table-list-code}

-   `repair-table-list`は、 [`repair-mode`](#repair-mode)が`true`に設定されている場合にのみ有効です。 `repair-table-list`は、インスタンスで修復する必要がある不良テーブルのリストです。リストの例は、[&quot;db.table1&quot;、&quot;db.table2&quot;...]です。
-   デフォルト値：[]
-   リストはデフォルトでは空です。これは、修復する必要のある不良テーブルがないことを意味します。

### <code>new_collations_enabled_on_first_bootstrap</code> {#code-new-collations-enabled-on-first-bootstrap-code}

-   新しい照合順序サポートを有効または無効にします。
-   デフォルト値： `true`
-   注：この構成は、最初に初期化されたTiDBクラスタに対してのみ有効です。初期化後、この構成アイテムを使用して、新しい照合順序サポートを有効または無効にすることはできません。 TiDBクラスタがv4.0以降にアップグレードされると、クラスタは以前に初期化されているため、この構成アイテムの`true`と`false`の両方の値が`false`と見なされます。

### <code>max-server-connections</code> {#code-max-server-connections-code}

-   TiDBで許可される同時クライアント接続の最大数。リソースを制御するために使用されます。
-   デフォルト値： `0`
-   デフォルトでは、TiDBは同時クライアント接続の数に制限を設定していません。この構成アイテムの値が`0`より大きく、実際のクライアント接続の数がこの値に達すると、TiDBサーバーは新しいクライアント接続を拒否します。

### <code>max-index-length</code> {#code-max-index-length-code}

-   新しく作成されたインデックスの最大許容長を設定します。
-   デフォルト値： `3072`
-   単位：バイト
-   現在、有効な値の範囲は`[3072, 3072*4]`です。 MySQLとTiDB（バージョン&lt;v3.0.11）にはこの構成アイテムはありませんが、どちらも新しく作成されたインデックスの長さを制限します。 MySQLのこの制限は`3072`です。 TiDB（バージョン= &lt;3.0.7）では、この制限は`3072*4`です。 TiDB（3.0.7 &lt;バージョン&lt;3.0.11）では、この制限は`3072`です。この構成は、MySQLおよび以前のバージョンのTiDBと互換性があるように追加されています。

### <code>table-column-count-limit</code> <span class="version-mark">limitv5.0の新機能</span> {#code-table-column-count-limit-code-span-class-version-mark-new-in-v5-0-span}

-   1つのテーブルの列数の制限を設定します。
-   デフォルト値： `1017`
-   現在、有効な値の範囲は`[1017, 4096]`です。

### <code>index-limit</code> <span class="version-mark">limitv5.0の新機能</span> {#code-index-limit-code-span-class-version-mark-new-in-v5-0-span}

-   1つのテーブル内のインデックス数の制限を設定します。
-   デフォルト値： `64`
-   現在、有効な値の範囲は`[64, 512]`です。

### <code>enable-telemetry</code> <span class="version-mark">telemetryv4.0.2の新機能</span> {#code-enable-telemetry-code-span-class-version-mark-new-in-v4-0-2-span}

-   TiDBのテレメトリコレクションを有効または無効にします。
-   デフォルト値： `true`
-   この構成がすべてのTiDBインスタンスで`false`に設定されている場合、TiDBのテレメトリ収集は無効になり、 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数は有効になりません。詳細については、 [テレメトリー](/telemetry.md)を参照してください。

### <code>enable-tcp4-only</code><span class="version-mark">新</span>機能 {#code-enable-tcp4-only-code-span-class-version-mark-new-in-v5-0-span}

-   TCP4でのみリスニングを有効または無効にします。
-   デフォルト値： `false`
-   このオプションを有効にすると、TiDBをLVSとともにロードバランシングに使用する場合に役立ちます。これは、 [TCPヘッダーからの実際のクライアントIP](https://github.com/alibaba/LVS/tree/master/kernel/net/toa)が「tcp4」プロトコルによって正しく解析されるためです。

### <code>enable-enum-length-limit</code> <span class="version-mark">limitv5.0の新機能</span> {#code-enable-enum-length-limit-code-span-class-version-mark-new-in-v5-0-span}

-   単一の`ENUM`要素と単一の`SET`要素の最大長を制限するかどうかを決定します。
-   デフォルト値： `true`
-   この構成値が`true`の場合、単一の`ENUM`要素と単一の`SET`要素の最大長は255文字であり、 [MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/string-type-syntax.html)と互換性があります。この構成値が`false`の場合、TiDB（v5.0より前）と互換性のある単一要素の長さに制限はありません。

### <code>graceful-wait-before-shutdown</code><span class="version-mark">の新</span>機能 {#code-graceful-wait-before-shutdown-code-span-class-version-mark-new-in-v5-0-span}

-   サーバーをシャットダウンするときにTiDBが待機する秒数を指定します。これにより、クライアントは切断できます。
-   デフォルト値： `0`
-   TiDBが（猶予期間内に）シャットダウンを待機している場合、HTTPステータスは失敗を示し、ロードバランサーがトラフィックを再ルーティングできるようにします。

### <code>enable-global-kill</code> <span class="version-mark">killv6.1.0の新機能</span> {#code-enable-global-kill-code-span-class-version-mark-new-in-v6-1-0-span}

-   グローバルキル（インスタンス間のクエリまたは接続の終了）機能を有効にするかどうかを制御します。
-   デフォルト値： `true`
-   値が`true`の場合、 `KILL`ステートメントと`KILL TIDB`ステートメントの両方でインスタンス間のクエリまたは接続を終了できるため、クエリまたは接続を誤って終了することを心配する必要はありません。クライアントを使用して任意のTiDBインスタンスに接続し、 `KILL`または`KILL TIDB`ステートメントを実行すると、ステートメントはターゲットTiDBインスタンスに転送されます。クライアントとTiDBクラスタの間にプロキシがある場合、 `KILL`ステートメントと`KILL TIDB`ステートメントも実行のためにターゲットTiDBインスタンスに転送されます。現在、 `enable-global-kill`が`true`の場合、MySQLコマンドライン<kbd>ctrl</kbd> + <kbd>c</kbd>を使用してTiDBでクエリまたは接続を終了することはサポートされていません。 `KILL`ステートメントの詳細については、 [殺す](/sql-statements/sql-statement-kill.md)を参照してください。

## ログ {#log}

ログに関連するConfiguration / コンフィグレーション項目。

### <code>level</code> {#code-level-code}

-   ログ出力レベルを指定します。
-   `info`のオプション`warn` `debug` 、 `fatal` `error`
-   デフォルト値： `info`

### <code>format</code> {#code-format-code}

-   ログの出力形式を指定します。
-   値のオプション： `json`および`text` 。
-   デフォルト値： `text`

### <code>enable-timestamp</code> {#code-enable-timestamp-code}

-   ログでタイムスタンプ出力を有効にするかどうかを決定します。
-   デフォルト値： `null`
-   値を`false`に設定すると、ログはタイムスタンプを出力しません。

> **ノート：**
>
> -   下位互換性を保つために、最初の`disable-timestamp`の構成項目は引き続き有効です。ただし、 `disable-timestamp`の値が`enable-timestamp`の値と意味的に競合する場合（たとえば、 `enable-timestamp`と`disable-timestamp`の両方が`true`に設定されている場合）、TiDBは`disable-timestamp`の値を無視します。
> -   現在、TiDBは`disable-timestamp`を使用して、タイムスタンプをログに出力するかどうかを決定します。この状況では、 `enable-timestamp`の値は`null`です。
> -   それ以降のバージョンでは、 `disable-timestamp`の構成が削除されます。 `disable-timestamp`を破棄し、意味的に理解しやすい`enable-timestamp`を使用します。

### <code>enable-slow-log</code> {#code-enable-slow-log-code}

-   遅いクエリログを有効にするかどうかを決定します。
-   デフォルト値： `true`
-   遅いクエリログを有効にするには、 `enable-slow-log`を`true`に設定します。それ以外の場合は、 `false`に設定します。

### <code>slow-query-file</code> {#code-slow-query-file-code}

-   遅いクエリログのファイル名。
-   デフォルト値： `tidb-slow.log`
-   低速ログの形式はTiDBv2.1.8で更新されているため、低速ログは個別に低速ログファイルに出力されます。 v2.1.8より前のバージョンでは、この変数はデフォルトで「」に設定されています。
-   設定後、低速クエリログがこのファイルに個別に出力されます。

### <code>slow-threshold</code> {#code-slow-threshold-code}

-   スローログに消費時間のしきい値を出力します。
-   デフォルト値： `300ms`
-   クエリの値がデフォルト値よりも大きい場合、それは低速クエリであり、低速ログに出力されます。

### <code>record-plan-in-slow-log</code> {#code-record-plan-in-slow-log-code}

-   実行プランを低速ログに記録するかどうかを決定します。
-   デフォルト値： `1`
-   `0`は無効にすることを意味し、 `1` （デフォルト）は有効にすることを意味します。このパラメーターの値は、 [`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log)システム変数の初期値です。

### <code>expensive-threshold</code> {#code-expensive-threshold-code}

-   `expensive`の操作の行数のしきい値を出力します。
-   デフォルト値： `10000`
-   クエリ行の数（統計に基づく中間結果を含む）がこの値よりも大きい場合、それは`expensive`操作であり、接頭辞`[EXPENSIVE_QUERY]`が付いたログを出力します。

## log.file {#log-file}

ログファイルに関連するConfiguration / コンフィグレーション項目。

#### <code>filename</code> {#code-filename-code}

-   一般ログファイルのファイル名。
-   デフォルト値： &quot;&quot;
-   設定すると、このファイルにログが出力されます。

#### <code>max-size</code> {#code-max-size-code}

-   ログファイルのサイズ制限。
-   デフォルト値：300
-   単位：MB
-   最大値は4096です。

#### <code>max-days</code> {#code-max-days-code}

-   ログが保持される最大日数。
-   デフォルト値： `0`
-   ログはデフォルトで保持されます。値を設定すると、期限切れのログは`max-days`後にクリーンアップされます。

#### <code>max-backups</code> {#code-max-backups-code}

-   保持されるログの最大数。
-   デフォルト値： `0`
-   デフォルトでは、すべてのログファイルが保持されます。 `7`に設定すると、最大7つのログファイルが保持されます。

## 安全 {#security}

セキュリティに関連するConfiguration / コンフィグレーション項目。

### <code>enable-sem</code> {#code-enable-sem-code}

-   セキュリティ拡張モード（SEM）を有効にします。
-   デフォルト値： `false`
-   SEMのステータスは、システム変数[`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)を介して取得できます。

### <code>ssl-ca</code> {#code-ssl-ca-code}

-   PEM形式の信頼できるCA証明書のファイルパス。
-   デフォルト値： &quot;&quot;
-   このオプションと`--ssl-cert`を同時に設定すると、 `--ssl-key`は、クライアントが証明書を提示するときに、このオプションで指定された信頼できるCAのリストに基づいてクライアント証明書を認証します。認証が失敗した場合、接続は終了します。
-   このオプションを設定したが、クライアントが証明書を提示しない場合、クライアント証明書認証なしで安全な接続が続行されます。

### <code>ssl-cert</code> {#code-ssl-cert-code}

-   PEM形式のSSL証明書のファイルパス。
-   デフォルト値： &quot;&quot;
-   このオプションと`--ssl-key`を同時に設定すると、TiDBは、クライアントがTLSを使用してTiDBに安全に接続することを許可します（強制はしません）。
-   指定された証明書または秘密鍵が無効な場合、TiDBは通常どおり起動しますが、安全な接続を受信できません。

### <code>ssl-key</code> {#code-ssl-key-code}

-   PEM形式のSSL証明書キーのファイルパス、つまり`--ssl-cert`で指定された証明書の秘密キー。
-   デフォルト値： &quot;&quot;
-   現在、TiDBはパスワードで保護された秘密鍵のロードをサポートしていません。

### <code>cluster-ssl-ca</code> {#code-cluster-ssl-ca-code}

-   TiKVまたはPDをTLSに接続するために使用されるCAルート証明書。
-   デフォルト値： &quot;&quot;

### <code>cluster-ssl-cert</code> {#code-cluster-ssl-cert-code}

-   TiKVまたはPDをTLSに接続するために使用されるSSL証明書ファイルのパス。
-   デフォルト値： &quot;&quot;

### <code>cluster-ssl-key</code> {#code-cluster-ssl-key-code}

-   TiKVまたはPDをTLSに接続するために使用されるSSL秘密鍵ファイルのパス。
-   デフォルト値： &quot;&quot;

### <code>spilled-file-encryption-method</code> {#code-spilled-file-encryption-method-code}

-   こぼれたファイルをディスクに保存するために使用される暗号化方法を決定します。
-   デフォルト値： `"plaintext"` 、これは暗号化を無効にします。
-   オプション値： `"plaintext"`および`"aes128-ctr"`

### <code>auto-tls</code> {#code-auto-tls-code}

-   起動時にTLS証明書を自動的に生成するかどうかを決定します。
-   デフォルト値： `false`

### <code>tls-version</code> {#code-tls-version-code}

-   MySQLプロトコル接続の最小TLSバージョンを設定します。
-   デフォルト値： &quot;&quot;、TLSv1.1以降を許可します。
-   オプション`"TLSv1.1"` ： `"TLSv1.0"` 、 `"TLSv1.3"` `"TLSv1.2"`

## パフォーマンス {#performance}

パフォーマンスに関連するConfiguration / コンフィグレーション項目。

### <code>max-procs</code> {#code-max-procs-code}

-   TiDBが使用するCPUの数。
-   デフォルト値： `0`
-   デフォルトの`0`は、マシン上のすべてのCPUを使用することを示します。 nに設定することもでき、TiDBはn個のCPUを使用します。

### <code>server-memory-quota</code> <span class="version-mark">quotav4.0.9の新機能</span> {#code-server-memory-quota-code-span-class-version-mark-new-in-v4-0-9-span}

> **警告：**
>
> `server-memory-quota`はまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

-   tidb-serverインスタンスのメモリ使用制限。
-   デフォルト値： `0` （バイト単位）。これは、メモリ制限がないことを意味します。

### <code>memory-usage-alarm-ratio</code> <span class="version-mark">ratiov4.0.9の新機能</span> {#code-memory-usage-alarm-ratio-code-span-class-version-mark-new-in-v4-0-9-span}

-   TiDBは、tidb-serverインスタンスのメモリ使用量が特定のしきい値を超えるとアラームをトリガーします。この構成アイテムの有効な値の範囲は`0` `1` 。 `0`または`1`として設定されている場合、このアラーム機能は無効になります。
-   デフォルト値： `0.8`
-   メモリ使用量アラームが有効になっているときに[`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)が設定されていない場合、メモリ使用量のしきい値は``the `memory-usage-alarm-ratio` value * the system memory size``です。 `server-memory-quota`が0より大きい値に設定されている場合、メモリ使用量のしきい値は``the `memory-usage-alarm-ratio` value * the `server-memory-quota` value``です。
-   TiDBは、tidb-serverインスタンスのメモリ使用量がしきい値を超えていることを検出すると、OOMのリスクがある可能性があると見なします。したがって、メモリ使用量が最も多い10個のSQLステートメント、実行時間が最も長い10個のSQLステートメント、および現在実行中のすべてのSQLステートメントのヒーププロファイルをディレクトリ[`tmp-storage-path/record`](/tidb-configuration-file.md#tmp-storage-path)に記録し、キーワード`tidb-server has the risk of OOM`を含むログを出力します。
-   この構成項目の値は、システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)の初期値です。

### <code>max-txn-ttl</code> {#code-max-txn-ttl-code}

-   1つのトランザクションがロックを保持できる最長時間。この時間を超えると、トランザクションのロックが他のトランザクションによってクリアされ、このトランザクションを正常にコミットできなくなる可能性があります。
-   デフォルト値： `3600000`
-   単位：ミリ秒
-   この時間より長くロックを保持するトランザクションは、コミットまたはロールバックすることしかできません。コミットが成功しない可能性があります。

### <code>stmt-count-limit</code> {#code-stmt-count-limit-code}

-   1回のTiDBトランザクションで許可されるステートメントの最大数。
-   デフォルト値： `5000`
-   ステートメントの数が`stmt-count-limit`を超えた後、トランザクションがロールバックまたはコミットされない場合、TiDBは`statement count 5001 exceeds the transaction limitation, autocommit = false`エラーを返します。この構成は、再試行可能なオプティミスティックトランザクションで**のみ**有効になります。ペシミスティックトランザクションを使用する場合、またはトランザクションの再試行を無効にした場合、トランザクション内のステートメントの数はこの構成によって制限されません。

### <code>txn-entry-size-limit</code><span class="version-mark">新機能</span> {#code-txn-entry-size-limit-code-span-class-version-mark-new-in-v5-0-span}

-   TiDBの1行のデータのサイズ制限。
-   デフォルト値： `6291456` （バイト単位）
-   トランザクション内の単一のKey-Valueレコードのサイズ制限。サイズ制限を超えると、TiDBは`entry too large`エラーを返します。この構成アイテムの最大値は`125829120` （120 MB）を超えません。
-   TiKVにも同様の制限があることに注意してください。 1回の書き込み要求のデータサイズが[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) （デフォルトでは8 MB）を超えると、TiKVはこの要求の処理を拒否します。テーブルに大きなサイズの行がある場合は、両方の構成を同時に変更する必要があります。

### <code>txn-total-size-limit</code> {#code-txn-total-size-limit-code}

-   TiDBでの単一トランザクションのサイズ制限。
-   デフォルト値： `104857600` （バイト単位）
-   1つのトランザクションで、Key-Valueレコードの合計サイズがこの値を超えることはできません。このパラメーターの最大値は`1099511627776` （1 TB）です。 binlogを使用してダウンストリームコンシューマーKafka（ `arbiter`クラスタなど）にサービスを提供した場合、このパラメーターの値は`1073741824` （1 GB）以下でなければならないことに注意してください。これは、Kafkaが処理できる単一のメッセージサイズの上限が1GBであるためです。それ以外の場合、この制限を超えるとエラーが返されます。

### <code>tcp-keep-alive</code> {#code-tcp-keep-alive-code}

-   TCP層で`keepalive`を有効にするかどうかを決定します。
-   デフォルト値： `true`

### <code>tcp-no-delay</code> {#code-tcp-no-delay-code}

-   TCP層でTCP_NODELAYを有効にするかどうかを決定します。有効にした後、TiDBはTCP / IPプロトコルのNagleアルゴリズムを無効にし、小さなデータパケットを送信してネットワーク遅延を削減できるようにします。これは、データの送信量が少ない、遅延の影響を受けやすいアプリケーションに適しています。
-   デフォルト値： `true`

### <code>cross-join</code> {#code-cross-join-code}

-   デフォルト値： `true`
-   TiDBは、デフォルトで両側テーブルの条件なしで`JOIN`ステートメント（ `WHERE`フィールド）の実行をサポートします。値を`false`に設定すると、そのような`JOIN`ステートメントが表示されたときにサーバーは実行を拒否します。

### <code>stats-lease</code> {#code-stats-lease-code}

-   統計の再読み込み、テーブルの行数の更新、自動分析の実行が必要かどうかの確認、フィードバックを使用した統計の更新、および列の統計の読み込みの時間間隔。
-   デフォルト値： `3s`
    -   `stats-lease`回の間隔で、TiDBは更新の統計をチェックし、更新が存在する場合はそれらをメモリに更新します。
    -   TiDBは、 `20 * stats-lease`回の間隔で、DMLによって生成された行の総数と変更された行の数をシステムテーブルに更新します。
    -   TiDBは、 `stats-lease`の間隔で、自動的に分析する必要のあるテーブルとインデックスをチェックします。
    -   TiDBは、 `stats-lease`の間隔で、メモリにロードする必要のある列統計をチェックします。
    -   TiDBは、 `200 * stats-lease`の間隔で、メモリにキャッシュされたフィードバックをシステムテーブルに書き込みます。
    -   `5 * stats-lease`の間隔で、TiDBはシステムテーブルのフィードバックを読み取り、メモリにキャッシュされている統計を更新します。
-   `stats-lease`を0に設定すると、TiDBはシステムテーブルのフィードバックを定期的に読み取り、メモリにキャッシュされている統計を3秒ごとに更新します。ただし、TiDBは、次の統計関連のシステムテーブルを自動的に変更しなくなりました。
    -   `mysql.stats_meta` ：TiDBは、トランザクションによって変更されたテーブル行の数を自動的に記録し、それをこのシステムテーブルに更新しなくなりました。
    -   `mysql.stats_top_n` `mysql.stats_buckets` `mysql.stats_histograms`は、統計を自動的に分析してプロアクティブに更新しなくなりました。
    -   `mysql.stats_feedback` ：TiDBは、クエリされたデータによって返された統計の一部に従って、テーブルとインデックスの統計を更新しなくなりました。

### <code>feedback-probability</code> {#code-feedback-probability-code}

-   TiDBが各クエリのフィードバック統計を収集する確率。
-   デフォルト値： `0`
-   この機能はデフォルトで無効になっているため、この機能を有効にすることはお勧めしません。有効になっている場合、TiDBは統計を更新するために`feedback-probability`の確率で各クエリのフィードバックを収集します。

### <code>query-feedback-limit</code> {#code-query-feedback-limit-code}

-   メモリにキャッシュできるクエリフィードバックの最大数。この制限を超える余分なフィードバックは破棄されます。
-   デフォルト値： `1024`

### <code>pseudo-estimate-ratio</code> {#code-pseudo-estimate-ratio-code}

-   テーブル内の（変更された行の数）/（行の総数）の比率。値を超えると、システムは統計の有効期限が切れていると見なし、疑似統計が使用されます。
-   デフォルト値： `0.8`
-   最小値は`0` 、最大値は`1`です。

### <code>force-priority</code> {#code-force-priority-code}

-   すべてのステートメントの優先度を設定します。
-   デフォルト値： `NO_PRIORITY`
-   オプションの`LOW_PRIORITY` ： `NO_PRIORITY` 、 `DELAYED` `HIGH_PRIORITY`

### <code>distinct-agg-push-down</code> {#code-distinct-agg-push-down-code}

-   オプティマイザーが、 `Distinct` （ `select count(distinct a) from t`など）の集計関数をコプロセッサーにプッシュダウンする操作を実行するかどうかを決定します。
-   デフォルト： `false`
-   この変数は、システム変数[`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)の初期値です。

### <code>enforce-mpp</code> {#code-enforce-mpp-code}

-   オプティマイザのコスト見積もりを無視し、クエリの実行にTiFlashのMPPモードを強制的に使用するかどうかを決定します。
-   デフォルト値： `false`
-   この構成アイテムは、 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。たとえば、この構成アイテムが`true`に設定されている場合、デフォルト値の`tidb_enforce_mpp`は`ON`です。

### <code>enable-stats-cache-mem-quota</code> <span class="version-mark">quotav6.1.0の新機能</span> {#code-enable-stats-cache-mem-quota-code-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> この変数は実験的機能です。実稼働環境での使用はお勧めしません。

-   統計キャッシュのメモリクォータを有効にするかどうかを制御します。
-   デフォルト値： `false`

### <code>stats-load-concurrency</code><span class="version-mark">の新機能</span> {#code-stats-load-concurrency-code-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、統計を同期的にロードすることは実験的機能です。実稼働環境で使用することはお勧めしません。

-   TiDB同期ロード統計機能が同時に処理できる列の最大数。
-   デフォルト値： `5`
-   現在、有効な値の範囲は`[1, 128]`です。

### <code>stats-load-queue-size</code> <span class="version-mark">sizev5.4.0の新機能</span> {#code-stats-load-queue-size-code-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、統計を同期的にロードすることは実験的機能です。実稼働環境で使用することはお勧めしません。

-   TiDBが統計を同期的にロードする機能がキャッシュできる列要求の最大数。
-   デフォルト値： `1000`
-   現在、有効な値の範囲は`[1, 100000]`です。

## オープントレース {#opentracing}

オープントレースに関連するConfiguration / コンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   opentracingを有効にして、一部のTiDBコンポーネントの呼び出しオーバーヘッドをトレースします。オープントレースを有効にすると、パフォーマンスが低下することに注意してください。
-   デフォルト値： `false`

### <code>rpc-metrics</code> {#code-rpc-metrics-code}

-   RPCメトリックを有効にします。
-   デフォルト値： `false`

## opentracing.sampler {#opentracing-sampler}

opentracing.samplerに関連するConfiguration / コンフィグレーション項目。

### <code>type</code> {#code-type-code}

-   オープントレースサンプラーのタイプを指定します。
-   デフォルト値： `"const"`
-   `"probabilistic"`の`"remote"` `"rateLimiting"` `"const"`

### <code>param</code> {#code-param-code}

-   オープントレースサンプラーのパラメーター。
    -   `const`タイプの場合、値は`0`または`1`になり、 `const`サンプラーを有効にするかどうかを示します。
    -   `probabilistic`タイプの場合、パラメーターはサンプリング確率を指定します。これは、 `0`から`1`までの浮動小数点数にすることができます。
    -   `rateLimiting`タイプの場合、パラメーターは1秒あたりにサンプリングされるスパンの数を指定します。
    -   `remote`タイプの場合、パラメーターはサンプリング確率を指定します。これは、 `0`から`1`までの浮動小数点数にすることができます。
-   デフォルト値： `1.0`

### <code>sampling-server-url</code> {#code-sampling-server-url-code}

-   jaeger-agentサンプリングサーバーのHTTPURL。
-   デフォルト値： `""`

### <code>max-operations</code> {#code-max-operations-code}

-   サンプラーがトレースできる操作の最大数。操作がトレースされない場合は、デフォルトの確率的サンプラーが使用されます。
-   デフォルト値： `0`

### <code>sampling-refresh-interval</code> {#code-sampling-refresh-interval-code}

-   イェーガーエージェントのサンプリングポリシーをポーリングする頻度を制御します。
-   デフォルト値： `0`

## opentracing.reporter {#opentracing-reporter}

opentracing.reporterに関連するConfiguration / コンフィグレーションアイテム。

### <code>queue-size</code> {#code-queue-size-code}

-   レポーターが記録するキューサイズは、メモリにまたがっています。
-   デフォルト値： `0`

### <code>buffer-flush-interval</code> {#code-buffer-flush-interval-code}

-   レポーターがメモリ内のスパンをストレージにフラッシュする間隔。
-   デフォルト値： `0`

### <code>log-spans</code> {#code-log-spans-code}

-   送信されたすべてのスパンのログを印刷するかどうかを決定します。
-   デフォルト値： `false`

### <code>local-agent-host-port</code> {#code-local-agent-host-port-code}

-   レポーターが送信するアドレスは、jaeger-agentにまたがっています。
-   デフォルト値： `""`

## tikv-クライアント {#tikv-client}

### <code>grpc-connection-count</code> {#code-grpc-connection-count-code}

-   各TiKVで確立された接続の最大数。
-   デフォルト値： `4`

### <code>grpc-keepalive-time</code> {#code-grpc-keepalive-time-code}

-   TiDBノードとTiKVノード間のRPC接続の`keepalive`時間間隔。指定された時間間隔内にネットワークパケットがない場合、gRPCクライアントはTiKVに対して`ping`コマンドを実行して、それが生きているかどうかを確認します。
-   デフォルト： `10`
-   単位：秒

### <code>grpc-keepalive-timeout</code> {#code-grpc-keepalive-timeout-code}

-   TiDBノードと`keepalive`ノード間のRPC1チェックのタイムアウト。
-   デフォルト値： `3`
-   単位：秒

### <code>grpc-compression-type</code> {#code-grpc-compression-type-code}

-   TiDBノードとTiKVノード間のデータ転送に使用される圧縮タイプを指定します。デフォルト値は`"none"`で、これは圧縮がないことを意味します。 gzip圧縮を有効にするには、この値を`"gzip"`に設定します。
-   デフォルト値： `"none"`
-   `"gzip"`のオプション： `"none"`

### <code>commit-timeout</code> {#code-commit-timeout-code}

-   トランザクションコミットを実行するときの最大タイムアウト。
-   デフォルト値： `41s`
-   この値は、Raft選挙タイムアウトの2倍より大きく設定する必要があります。

### <code>max-batch-size</code> {#code-max-batch-size-code}

-   バッチで送信されるRPCパケットの最大数。値が`0`でない場合、 `BatchCommands` APIを使用してTiKVにリクエストを送信し、同時実行性が高い場合にRPCレイテンシを短縮できます。この値は変更しないことをお勧めします。
-   デフォルト値： `128`

### <code>max-batch-wait-time</code> {#code-max-batch-wait-time-code}

-   `max-batch-wait-time`がデータパケットをバッチで大きなパケットにカプセル化し、TiKVノードに送信するのを待ちます。 `tikv-client.max-batch-size`の値が`0`より大きい場合にのみ有効です。この値は変更しないことをお勧めします。
-   デフォルト値： `0`
-   単位：ナノ秒

### <code>batch-wait-size</code> {#code-batch-wait-size-code}

-   バッチでTiKVに送信されるパケットの最大数。この値は変更しないことをお勧めします。
-   デフォルト値： `8`
-   値が`0`の場合、この機能は無効になります。

### <code>overload-threshold</code> {#code-overload-threshold-code}

-   TiKV負荷のしきい値。 TiKVの負荷がこのしきい値を超えると、TiKVの圧力を軽減するために、さらに`batch`のパケットが収集されます。 `tikv-client.max-batch-size`の値が`0`より大きい場合にのみ有効です。この値は変更しないことをお勧めします。
-   デフォルト値： `200`

## tikv-client.copr-cachev4.0.0の<span class="version-mark">新機能</span> {#tikv-client-copr-cache-span-class-version-mark-new-in-v4-0-0-span}

このセクションでは、コプロセッサー・キャッシュ機能に関連する構成項目を紹介します。

### <code>capacity-mb</code> {#code-capacity-mb-code}

-   キャッシュされたデータの合計サイズ。キャッシュスペースがいっぱいになると、古いキャッシュエントリが削除されます。値が`0.0`の場合、コプロセッサーキャッシュ機能は無効になります。
-   デフォルト値： `1000.0`
-   単位：MB
-   タイプ：フロート

## txn-local-latches {#txn-local-latches}

トランザクションラッチに関連するConfiguration / コンフィグレーション。多くのローカルトランザクションの競合が発生した場合は、これを有効にすることをお勧めします。

### <code>enabled</code> {#code-enabled-code}

-   トランザクションのメモリロックを有効にするかどうかを決定します。
-   デフォルト値： `false`

### <code>capacity</code> {#code-capacity-code}

-   ハッシュに対応するスロットの数。2の指数倍数に自動的に上方に調整されます。各スロットは32バイトのメモリを占有します。設定が小さすぎると、データの書き込みが比較的広い範囲（データのインポートなど）をカバーするシナリオで、実行速度が遅くなり、パフォーマンスが低下する可能性があります。
-   デフォルト値： `2048000`

## binlog {#binlog}

Binlogに関連する構成。

### <code>enable</code> {#code-enable-code}

-   binlogを有効または無効にします。
-   デフォルト値： `false`

### <code>write-timeout</code> {#code-write-timeout-code}

-   binlogをPumpに書き込むタイムアウト。この値を変更することはお勧めしません。
-   デフォルト： `15s`
-   単位：秒

### <code>ignore-error</code> {#code-ignore-error-code}

-   binlogをPumpに書き込むプロセスで発生したエラーを無視するかどうかを決定します。この値を変更することはお勧めしません。
-   デフォルト値： `false`
-   値が`true`に設定されていてエラーが発生すると、TiDBはbinlogの書き込みを停止し、 `tidb_server_critical_error_total`の監視項目のカウントに`1`を追加します。値を`false`に設定すると、binlogの書き込みが失敗し、TiDBサービス全体が停止します。

### <code>binlog-socket</code> {#code-binlog-socket-code}

-   binlogのエクスポート先のネットワークアドレス。
-   デフォルト値： &quot;&quot;

### <code>strategy</code> {#code-strategy-code}

-   binlogがエクスポートされるときのPump選択の戦略。現在、 `hash`つと`range`の方法のみがサポートされています。
-   デフォルト値： `range`

## 状態 {#status}

TiDBサービスのステータスに関連するConfiguration / コンフィグレーション。

### <code>report-status</code> {#code-report-status-code}

-   HTTPAPIサービスを有効または無効にします。
-   デフォルト値： `true`

### <code>record-db-qps</code> {#code-record-db-qps-code}

-   データベース関連のQPSメトリックをPrometheusに送信するかどうかを決定します。
-   デフォルト値： `false`

## 悲観的-txn {#pessimistic-txn}

悲観的なトランザクションの使用法については、 [TiDBペシミスティックトランザクションモード](/pessimistic-transaction.md)を参照してください。

### max-retry-count {#max-retry-count}

-   悲観的トランザクションにおける各ステートメントの最大再試行回数。再試行回数がこの制限を超えると、エラーが発生します。
-   デフォルト値： `256`

### デッドロック-履歴-容量 {#deadlock-history-capacity}

-   単一のTiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)つのテーブルに記録できるデッドロックイベントの最大数。このテーブルがフルボリュームであり、追加のデッドロックイベントが発生した場合、テーブル内の最も古いレコードが削除され、最新のエラーが発生します。
-   デフォルト値： `10`
-   最小値： `0`
-   最大値： `10000`

### デッドロック-履歴-収集-再試行可能 {#deadlock-history-collect-retryable}

-   [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロックエラーの情報を収集するかどうかを制御します。再試行可能なデッドロックエラーの説明については、 [再試行可能なデッドロックエラー](/information-schema/information-schema-deadlocks.md#retryable-deadlock-errors)を参照してください。
-   デフォルト値： `false`

### pessimistic-auto-commit（v6.0.0の新機能） {#pessimistic-auto-commit-new-in-v6-0-0}

-   ペシミスティックトランザクションモードがグローバルに有効になっている場合に、自動コミットトランザクションが使用するトランザクションモードを決定します（ `tidb_txn_mode='pessimistic'` ）。デフォルトでは、ペシミスティックトランザクションモードがグローバルに有効になっている場合でも、自動コミットトランザクションはオプティミスティックトランザクションモードを使用します。 `pessimistic-auto-commit`を有効にした後（ `true`に設定）、自動コミットトランザクションもペシミスティックモードを使用します。これは、他の明示的にコミットされたペシミスティックトランザクションと一致します。
-   競合のあるシナリオの場合、この構成を有効にした後、TiDBはトランザクションをグローバルロック待機管理に組み込みます。これにより、デッドロックが回避され、デッドロックの原因となる競合によって引き起こされる遅延の急増が軽減されます。
-   競合のないシナリオで、自動コミットトランザクションが多数ある場合（特定の数は実際のシナリオによって決定されます。たとえば、自動コミットトランザクションの数は、アプリケーションの総数の半分以上を占めます）、および単一のトランザクションが大量のデータを操作するため、この構成を有効にするとパフォーマンスが低下します。たとえば、auto- `INSERT INTO SELECT`ステートメント。
-   デフォルト値： `false`

## 実験的 {#experimental}

v3.1.0で導入された`experimental`のセクションでは、TiDBの実験的機能に関連する構成について説明します。

### <code>allow-expression-index</code> <span class="version-mark">indexv4.0.0の新機能</span> {#code-allow-expression-index-code-span-class-version-mark-new-in-v4-0-0-span}

-   式インデックスを作成できるかどうかを制御します。 TiDB v5.2.0以降、式の関数が安全であれば、この構成を有効にしなくても、この関数に基づいて式インデックスを直接作成できます。他の関数に基づいて式インデックスを作成する場合は、この構成を有効にできますが、正確性の問題が存在する可能性があります。 `tidb_allow_function_for_expression_index`変数をクエリすることにより、式の作成に直接使用しても安全な関数を取得できます。
-   デフォルト値： `false`
