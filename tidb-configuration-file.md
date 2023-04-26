---
title: TiDB Configuration File
summary: Learn the TiDB configuration file options that are not involved in command line options.
---

<!-- markdownlint-disable MD001 -->

<!-- markdownlint-disable MD024 -->

# TiDBコンフィグレーションファイル {#tidb-configuration-file}

TiDB 構成ファイルは、コマンドライン パラメーターよりも多くのオプションをサポートしています。デフォルトの構成ファイル[`config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example)ダウンロードして、名前を`config.toml`に変更できます。このドキュメントでは、 [コマンド ライン オプション](/command-line-flags-for-tidb-configuration.md)に含まれないオプションのみを説明します。

### <code>split-table</code> {#code-split-table-code}

-   テーブルごとに個別のリージョンを作成するかどうかを決定します。
-   デフォルト値: `true`
-   多数のテーブル (たとえば、10 万を超えるテーブル) を作成する必要がある場合は、 `false`に設定することをお勧めします。

### <code>tidb-max-reuse-chunk</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-tidb-max-reuse-chunk-code-span-class-version-mark-new-in-v6-4-0-span}

-   チャンク割り当ての最大キャッシュ チャンク オブジェクトを制御します。この構成項目を大きすぎる値に設定すると、OOM のリスクが高まる可能性があります。
-   デフォルト値: `64`
-   最小値: `0`
-   最大値: `2147483647`

### <code>tidb-max-reuse-column</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-tidb-max-reuse-column-code-span-class-version-mark-new-in-v6-4-0-span}

-   チャンク割り当ての最大キャッシュ列オブジェクトを制御します。この構成項目を大きすぎる値に設定すると、OOM のリスクが高まる可能性があります。
-   デフォルト値: `256`
-   最小値: `0`
-   最大値: `2147483647`

### <code>token-limit</code> {#code-token-limit-code}

-   リクエストを同時に実行できるセッションの数。
-   タイプ: 整数
-   デフォルト値: `1000`
-   最小値: `1`
-   最大値 (64 ビット プラットフォーム): `18446744073709551615`
-   最大値 (32 ビット プラットフォーム): `4294967295`

### <code>temp-dir</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-temp-dir-code-span-class-version-mark-new-in-v6-3-0-span}

-   TiDB が一時データを格納するために使用するファイル システムの場所。機能が TiDB ノードのローカルstorageを必要とする場合、TiDB は対応する一時データをこの場所に保存します。
-   インデックスの作成時に[`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が有効になっている場合、新しく作成されたインデックスのためにバックフィルが必要なデータは、最初に TiDB ローカルの一時ディレクトリに保存され、次にバッチで TiKV にインポートされるため、インデックスの作成が高速化されます。
-   デフォルト値: `"/tmp/tidb"`

### <code>oom-use-tmp-storage</code> {#code-oom-use-tmp-storage-code}

> **警告：**
>
> v6.3.0 以降、この構成項目は廃止され、システム変数[`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom)に置き換えられました。 TiDB クラスターが v6.3.0 以降のバージョンにアップグレードされると、変数が`oom-use-tmp-storage`の値で自動的に初期化されます。その後、 `oom-use-tmp-storage`の値を変更しても有効**になりません**。

-   1 つの SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部の演算子の一時storageを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>tmp-storage-path</code> {#code-tmp-storage-path-code}

-   1 つの SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超える場合に、一部の演算子の一時storageパスを指定します。
-   デフォルト値: `<temporary directory of OS>/<OS user ID>_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage` 。 `MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=` `<host>:<port>/<statusHost>:<statusPort>`の`Base64`エンコード結果です。
-   この構成は、システム変数[`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom)が`ON`の場合にのみ有効です。

### <code>tmp-storage-quota</code> {#code-tmp-storage-quota-code}

-   `tmp-storage-path`のstorageのクォータを指定します。単位はバイトです。
-   単一の SQL ステートメントが一時ディスクを使用し、TiDBサーバーの一時ディスクの総量がこの構成値を超えた場合、現在の SQL 操作はキャンセルされ、 `Out of Global Storage Quota!`エラーが返されます。
-   この構成の値が`0`より小さい場合、上記のチェックと制限は適用されません。
-   デフォルト値: `-1`
-   `tmp-storage-path`の残りの使用可能なstorageが`tmp-storage-quota`で定義された値よりも少ない場合、TiDBサーバーは起動時にエラーを報告し、終了します。

### <code>lease</code> {#code-lease-code}

-   DDL リースのタイムアウト。
-   デフォルト値: `45s`
-   単位：秒

### <code>compatible-kill-query</code> {#code-compatible-kill-query-code}

-   `KILL`ステートメントを MySQL 互換に設定するかどうかを決定します。
-   デフォルト値: `false`
-   TiDB での`KILL xxx`の動作は、MySQL での動作とは異なります。 TiDB には`TIDB`キーワード、つまり`KILL TIDB xxx`必要です。 `compatible-kill-query`が`true`に設定されている場合、 `TIDB`キーワードは必要ありません。
-   ユーザーが<kbd>Ctrl</kbd> + <kbd>C</kbd>を押したときの MySQL コマンドライン クライアントのデフォルトの動作は、バックエンドへの新しい接続を作成し、その新しい接続で`KILL`ステートメントを実行するため、この区別は重要です。ロード バランサーまたはプロキシが元のセッションとは異なる TiDBサーバーインスタンスに新しい接続を送信した場合、間違ったセッションが終了し、クラスターを使用しているアプリケーションが中断される可能性があります。 `KILL`ステートメントで参照する接続が、 `KILL`ステートメントの送信先と同じサーバー上にあることが確実な場合にのみ、 `compatible-kill-query`有効にしてください。

### <code>check-mb4-value-in-utf8</code> {#code-check-mb4-value-in-utf8-code}

-   `utf8mb4`文字チェックを有効にするかどうかを決定します。この機能が有効な場合、文字セットが`utf8`で、 `mb4`文字が`utf8`に挿入されると、エラーが返されます。
-   デフォルト値: `false`
-   v6.1.0 以降、 `utf8mb4`文字チェックを有効にするかどうかは、TiDB 構成項目`instance.tidb_check_mb4_value_in_utf8`またはシステム変数`tidb_check_mb4_value_in_utf8`によって決定されます。 `check-mb4-value-in-utf8`引き続き有効です。ただし、 `check-mb4-value-in-utf8`と`instance.tidb_check_mb4_value_in_utf8`の両方が設定されている場合は、後者が有効になります。

### <code>treat-old-version-utf8-as-utf8mb4</code> {#code-treat-old-version-utf8-as-utf8mb4-code}

-   古いテーブルの`utf8`文字セットを`utf8mb4`として扱うかどうかを決定します。
-   デフォルト値: `true`

### <code>alter-primary-key</code> (非推奨) {#code-alter-primary-key-code-deprecated}

-   主キー制約を列に追加するか列から削除するかを決定します。
-   デフォルト値: `false`
-   このデフォルト設定では、主キー制約の追加または削除はサポートされていません。 `alter-primary-key` ～ `true`を設定すると、この機能を有効にできます。ただし、スイッチがオンになる前にテーブルがすでに存在し、その主キー列のデータ型が整数である場合、この構成項目を`true`に設定しても、列から主キーを削除することはできません。

> **ノート：**
>
> この構成項目は廃止され、現在は`@tidb_enable_clustered_index`の値が`INT_ONLY`の場合にのみ有効です。主キーを追加または削除する必要がある場合は、テーブルの作成時に代わりに`NONCLUSTERED`キーワードを使用してください。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。

### <code>server-version</code> {#code-server-version-code}

-   次の状況で、TiDB によって返されるバージョン文字列を変更します。
    -   内蔵`VERSION()`機能使用時。
    -   TiDB がクライアントへの最初の接続を確立し、サーバーのバージョン文字列を含む最初のハンドシェイク パケットを返すとき。詳細については、 [MySQL 初期ハンドシェイク パケット](https://dev.mysql.com/doc/internals/en/connection-phase-packets.html#packet-Protocol::Handshake)を参照してください。
-   デフォルト値: &quot;&quot;
-   デフォルトでは、TiDB バージョン文字列の形式は`5.7.${mysql_latest_minor_version}-TiDB-${tidb_version}`です。

### <code>repair-mode</code> {#code-repair-mode-code}

-   信頼できない修復モードを有効にするかどうかを決定します。 `repair-mode`が`true`に設定されている場合、 `repair-table-list`の不良テーブルはロードできません。
-   デフォルト値: `false`
-   `repair`構文はデフォルトではサポートされていません。これは、TiDB の開始時にすべてのテーブルがロードされることを意味します。

### <code>repair-table-list</code> {#code-repair-table-list-code}

-   `repair-table-list`は、 [`repair-mode`](#repair-mode) `true`に設定されている場合にのみ有効です。 `repair-table-list`は、インスタンスで修復する必要がある不良テーブルのリストです。リストの例: [&quot;db.table1&quot;,&quot;db.table2&quot;...].
-   デフォルト値: []
-   デフォルトでは、リストは空です。これは、修復が必要な不良テーブルがないことを意味します。

### <code>new_collations_enabled_on_first_bootstrap</code> {#code-new-collations-enabled-on-first-bootstrap-code}

-   新しい照合順序サポートを有効または無効にします。
-   デフォルト値: `true`
-   注: この構成は、最初に初期化された TiDB クラスターに対してのみ有効です。初期化後は、この構成項目を使用して新しい照合順序サポートを有効または無効にすることはできません。

### <code>max-server-connections</code> {#code-max-server-connections-code}

-   TiDB で許可される同時クライアント接続の最大数。リソースを制御するために使用されます。
-   デフォルト値: `0`
-   デフォルトでは、TiDB は同時クライアント接続数に制限を設定しません。この構成項目の値が`0`より大きく、実際のクライアント接続数がこの値に達すると、TiDBサーバーは新しいクライアント接続を拒否します。
-   v6.2.0 以降、TiDB 構成項目[`instance.max_connections`](/tidb-configuration-file.md#max_connections)またはシステム変数[`max_connections`](/system-variables.md#max_connections)を使用して、TiDB で許可される同時クライアント接続の最大数を設定します。 `max-server-connections`は引き続き有効です。ただし、 `max-server-connections`と`instance.max_connections`同時に設定した場合は、後者が有効になります。

### <code>max-index-length</code> {#code-max-index-length-code}

-   新しく作成されたインデックスの最大許容長を設定します。
-   デフォルト値: `3072`
-   単位：バイト
-   現在、有効な値の範囲は`[3072, 3072*4]`です。 MySQL と TiDB (バージョン &lt; v3.0.11) にはこの構成項目はありませんが、どちらも新しく作成されたインデックスの長さを制限しています。 MySQL でのこの制限は`3072`です。 TiDB (バージョン =&lt; 3.0.7) では、この制限は`3072*4`です。 TiDB (3.0.7 &lt; バージョン &lt; 3.0.11) では、この制限は`3072`です。この構成は、MySQL および以前のバージョンの TiDB との互換性を保つために追加されています。

### <code>table-column-count-limit</code> <span class="version-mark">v5.0 の新機能</span> {#code-table-column-count-limit-code-span-class-version-mark-new-in-v5-0-span}

-   1 つのテーブルの列数の制限を設定します。
-   デフォルト値: `1017`
-   現在、有効な値の範囲は`[1017, 4096]`です。

### <code>index-limit</code> <span class="version-mark">v5.0 の新機能</span> {#code-index-limit-code-span-class-version-mark-new-in-v5-0-span}

-   1 つのテーブル内のインデックス数の制限を設定します。
-   デフォルト値: `64`
-   現在、有効な値の範囲は`[64, 512]`です。

### <code>enable-telemetry</code> <span class="version-mark">v4.0.2 の新機能</span> {#code-enable-telemetry-code-span-class-version-mark-new-in-v4-0-2-span}

-   TiDB でのテレメトリ収集を有効または無効にします。
-   デフォルト値: v6.5.0 の場合は`true` 。 v6.5.1 以降の v6.5.x バージョンの場合は`false`
-   この構成が TiDB インスタンスで`true`に設定され、 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数が`ON`に設定されている場合、この TiDB インスタンスでのテレメトリ収集が有効になります。
-   この構成がすべての TiDB インスタンスで`false`に設定されている場合、TiDB でのテレメトリ収集は無効になり、 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数は有効になりません。詳細は[テレメトリー](/telemetry.md)を参照してください。

### <code>enable-tcp4-only</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-tcp4-only-code-span-class-version-mark-new-in-v5-0-span}

-   TCP4 のみでのリッスンを有効または無効にします。
-   デフォルト値: `false`
-   このオプションを有効にすると、「tcp4」プロトコルで[TCP ヘッダーからの実際のクライアント IP](https://github.com/alibaba/LVS/tree/master/kernel/net/toa)正しく解析できるため、TiDB を LVS で使用してロード バランシングを行う場合に便利です。

### <code>enable-enum-length-limit</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-enum-length-limit-code-span-class-version-mark-new-in-v5-0-span}

-   単一の`ENUM`要素と単一の`SET`要素の最大長を制限するかどうかを決定します。
-   デフォルト値: `true`
-   この構成値が`true`の場合、単一の`ENUM`要素と単一の`SET`要素の最大長は 255 文字で、これは[MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/string-type-syntax.html)と互換性があります。この構成値が`false`の場合、1 つの要素の長さに制限はなく、TiDB (v5.0 より前) と互換性があります。

### <code>graceful-wait-before-shutdown</code> <span class="version-mark">v5.0 の新機能</span> {#code-graceful-wait-before-shutdown-code-span-class-version-mark-new-in-v5-0-span}

-   サーバーをシャットダウンするときに TiDB が待機する秒数を指定します。これにより、クライアントは切断できるようになります。
-   デフォルト値: `0`
-   TiDB が (猶予期間で) シャットダウンを待機している場合、HTTP ステータスは失敗を示し、ロード バランサーがトラフィックを再ルーティングできるようにします。

### <code>enable-global-kill</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-enable-global-kill-code-span-class-version-mark-new-in-v6-1-0-span}

-   Global Kill (インスタンス間のクエリまたは接続の終了) 機能を有効にするかどうかを制御します。
-   デフォルト値: `true`
-   値が`true`の場合、 `KILL`と`KILL TIDB`ステートメントの両方がインスタンス間のクエリまたは接続を終了できるため、クエリまたは接続を誤って終了することを心配する必要はありません。クライアントを使用して任意の TiDB インスタンスに接続し、 `KILL`または`KILL TIDB`ステートメントを実行すると、ステートメントはターゲットの TiDB インスタンスに転送されます。クライアントと TiDB クラスターの間にプロキシがある場合、 `KILL`と`KILL TIDB`ステートメントも実行のためにターゲット TiDB インスタンスに転送されます。現在、 `enable-global-kill`が`true`の場合、MySQL コマンドライン<kbd>ctrl</kbd> + <kbd>c</kbd>を使用して TiDB でクエリまたは接続を終了することはサポートされていません。 `KILL`ステートメントの詳細については、 [殺す](/sql-statements/sql-statement-kill.md)参照してください。

### <code>initialize-sql-file</code> <span class="version-mark">v6.5.1 の新機能</span> {#code-initialize-sql-file-code-span-class-version-mark-new-in-v6-5-1-span}

-   TiDB クラスターの初回起動時に実行する SQL スクリプトを指定します。
-   デフォルト値: `""`
-   このスクリプト内のすべての SQL ステートメントは、権限チェックなしで最高の権限で実行されます。指定した SQL スクリプトの実行に失敗すると、TiDB クラスターが起動しない可能性があります。
-   この構成アイテムは、システム変数の値の変更、ユーザーの作成、権限などの操作を実行するために使用されます。

### <span class="version-mark">v5.0.0 の新</span><code>enable-forwarding</code> {#code-enable-forwarding-code-span-class-version-mark-new-in-v5-0-0-span}

-   ネットワーク分離の可能性がある場合に、TiDB の PD クライアントと TiKV クライアントがフォロワー経由でリーダーにリクエストを転送するかどうかを制御します。
-   デフォルト値: `false`
-   環境でネットワークが分離されている可能性がある場合、このパラメーターを有効にすると、サービスが利用できなくなる期間を短縮できます。
-   分離、ネットワークの中断、またはダウンタイムが発生したかどうかを正確に判断できない場合、このメカニズムを使用すると判断を誤るリスクがあり、可用性とパフォーマンスが低下します。ネットワーク障害が発生したことがない場合は、このパラメーターを有効にすることはお勧めしません。

### <code>enable-table-lock</code> <span class="version-mark">v4.0.0 の新機能</span> {#code-enable-table-lock-code-span-class-version-mark-new-in-v4-0-0-span}

> **警告：**
>
> テーブル ロックは実験的機能です。本番環境で使用することはお勧めしません。

-   テーブル ロック機能を有効にするかどうかを制御します。
-   デフォルト値: `false`
-   テーブル ロックは、複数のセッション間で同じテーブルへの同時アクセスを調整するために使用されます。現在、 `READ` 、 `WRITE` 、および`WRITE LOCAL`ロック タイプがサポートされています。構成項目が`false`に設定されている場合、 `LOCK TABLES`または`UNLOCK TABLES`ステートメントを実行しても効果がなく、「LOCK/UNLOCK TABLES is not supported」という警告が返されます。詳細については、 [`LOCK TABLES`と<code>UNLOCK TABLES</code>](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)参照してください。

### <code>labels</code> {#code-labels-code}

-   サーバーラベルを指定します。たとえば、 `{ zone = "us-west-1", dc = "dc1", rack = "rack1", host = "tidb1" }`です。
-   デフォルト値: `{}`

> **ノート：**
>
> -   TiDB では、 `zone`ラベルは、サーバーが配置されているゾーンを指定するために特別に使用されます。 `zone`が null 以外の値に設定されている場合、対応する値が[`txn-score`](/system-variables.md#txn_scope)や[`Follower read`](/follower-read.md)などの機能によって自動的に使用されます。
> -   `group`ラベルはTiDB Operatorで特別な用途があります。 [TiDB Operator](/tidb-operator-overview.md)使用してデプロイされたクラスターの場合、 `group`ラベルを手動で指定することは**お**勧めしません。

## ログ {#log}

ログに関するコンフィグレーション項目です。

### <code>level</code> {#code-level-code}

-   ログ出力レベルを指定します。
-   値のオプション: `debug` 、 `info` 、 `warn` 、 `error` 、および`fatal` 。
-   デフォルト値: `info`

### <code>format</code> {#code-format-code}

-   ログ出力形式を指定します。
-   値のオプション: `json`および`text` 。
-   デフォルト値: `text`

### <code>enable-timestamp</code> {#code-enable-timestamp-code}

-   ログでのタイムスタンプ出力を有効にするかどうかを決定します。
-   デフォルト値: `null`
-   値を`false`に設定すると、ログはタイムスタンプを出力しません。

> **ノート：**
>
> -   下位互換性を維持するために、最初の`disable-timestamp`構成アイテムは引き続き有効です。ただし、 `disable-timestamp`値が`enable-timestamp`の値と意味的に競合する場合 (たとえば、 `enable-timestamp`と`disable-timestamp`の両方が`true`に設定されている場合)、TiDB は`disable-timestamp`の値を無視します。
> -   現在、TiDB は`disable-timestamp`を使用してログにタイムスタンプを出力するかどうかを決定します。この場合、 `enable-timestamp`の値は`null`です。
> -   それ以降のバージョンでは、 `disable-timestamp`構成が削除されます。 `disable-timestamp`破棄して、意味的に理解しやすい`enable-timestamp`使用します。

### <code>enable-slow-log</code> {#code-enable-slow-log-code}

-   スロー クエリ ログを有効にするかどうかを決定します。
-   デフォルト値: `true`
-   スロー クエリ ログを有効にするには、 `enable-slow-log` ～ `true`を設定します。それ以外の場合は、 `false`に設定します。
-   v6.1.0 以降、スロー クエリ ログを有効にするかどうかは、TiDB 構成項目[`instance.tidb_enable_slow_log`](/tidb-configuration-file.md#tidb_enable_slow_log)またはシステム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)によって決定されます。 `enable-slow-log`は引き続き有効です。ただし、 `enable-slow-log`と`instance.tidb_enable_slow_log`同時に設定した場合は、後者が有効になります。

### <code>slow-query-file</code> {#code-slow-query-file-code}

-   スロー クエリ ログのファイル名。
-   デフォルト値: `tidb-slow.log`
-   TiDB v2.1.8ではスローログのフォーマットが更新されたため、スローログはスローログファイルに別途出力されます。 v2.1.8 より前のバージョンでは、この変数はデフォルトで &quot;&quot; に設定されています。
-   設定後、スロークエリのログは別途このファイルに出力されます。

### <code>slow-threshold</code> {#code-slow-threshold-code}

-   スローログの消費時間の閾値を出力します。
-   デフォルト値: `300`
-   単位: ミリ秒
-   クエリの値がデフォルト値より大きい場合、それはスロー クエリであり、スロー ログに出力されます。
-   v6.1.0以降、スローログの消費時間の閾値は、TiDBの設定項目[`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold)またはシステム変数[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)で指定されるようになりました。 `slow-threshold`は引き続き有効です。ただし、 `slow-threshold`と`instance.tidb_slow_log_threshold`同時に設定した場合は、後者が有効になります。

### <code>record-plan-in-slow-log</code> {#code-record-plan-in-slow-log-code}

-   実行計画をスロー ログに記録するかどうかを決定します。
-   デフォルト値: `1`
-   v6.1.0 以降、スローログに実行計画を記録するかどうかは、TiDB 構成項目[`instance.tidb_record_plan_in_slow_log`](/tidb-configuration-file.md#tidb_record_plan_in_slow_log)またはシステム変数[`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log)によって決定されます。 `record-plan-in-slow-log`は引き続き有効です。ただし、 `record-plan-in-slow-log`と`instance.tidb_record_plan_in_slow_log`同時に設定した場合は、後者が有効になります。

### <code>expensive-threshold</code> {#code-expensive-threshold-code}

-   `expensive`回の操作で行数の閾値を出力します。
-   デフォルト値: `10000`
-   クエリの行数（統計に基づく中間結果を含む）がこの値より大きい場合は、 `expensive`操作で`[EXPENSIVE_QUERY]`プレフィックスを付けてログを出力します。

## ログファイル {#log-file}

ログファイルに関するコンフィグレーション項目です。

#### <code>filename</code> {#code-filename-code}

-   一般ログ ファイルのファイル名。
-   デフォルト値: &quot;&quot;
-   設定すると、このファイルにログが出力されます。

#### <code>max-size</code> {#code-max-size-code}

-   ログ ファイルのサイズ制限。
-   デフォルト値: 300
-   単位：MB
-   最大値は 4096 です。

#### <code>max-days</code> {#code-max-days-code}

-   ログが保持される最大日数。
-   デフォルト値: `0`
-   ログはデフォルトで保持されます。値を設定すると、期限切れのログは`max-days`後にクリーンアップされます。

#### <code>max-backups</code> {#code-max-backups-code}

-   保持されるログの最大数。
-   デフォルト値: `0`
-   デフォルトでは、すべてのログ ファイルが保持されます。 `7`に設定すると、最大 7 つのログ ファイルが保持されます。

## Security {#security}

セキュリティに関するコンフィグレーション項目です。

### <code>enable-sem</code> {#code-enable-sem-code}

-   Security拡張モード (SEM) を有効にします。
-   デフォルト値: `false`
-   SEM のステータスは、システム変数[`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)から取得できます。

### <code>ssl-ca</code> {#code-ssl-ca-code}

-   PEM 形式の信頼できる CA 証明書のファイル パス。
-   デフォルト値: &quot;&quot;
-   このオプションと`--ssl-cert` 、 `--ssl-key`を同時に設定すると、TiDB は、クライアントが証明書を提示するときに、このオプションで指定された信頼できる CA のリストに基づいてクライアント証明書を認証します。認証に失敗すると、接続が終了します。
-   このオプションを設定してもクライアントが証明書を提示しない場合、クライアント証明書認証なしでセキュア接続が続行されます。

### <code>ssl-cert</code> {#code-ssl-cert-code}

-   PEM 形式の SSL 証明書のファイル パス。
-   デフォルト値: &quot;&quot;
-   このオプションと`--ssl-key`同時に設定すると、TiDB はクライアントが TLS を使用して TiDB に安全に接続することを許可します (強制はしません)。
-   指定された証明書または秘密鍵が無効な場合、TiDB は通常どおり起動しますが、安全な接続を受け取ることができません。

### <code>ssl-key</code> {#code-ssl-key-code}

-   PEM 形式の SSL 証明書キー、つまり`--ssl-cert`で指定された証明書の秘密キーのファイル パス。
-   デフォルト値: &quot;&quot;
-   現在、TiDB はパスワードで保護された秘密鍵のロードをサポートしていません。

### <code>cluster-ssl-ca</code> {#code-cluster-ssl-ca-code}

-   TiKV または PD を TLS で接続するために使用される CA ルート証明書。
-   デフォルト値: &quot;&quot;

### <code>cluster-ssl-cert</code> {#code-cluster-ssl-cert-code}

-   TiKV または PD を TLS で接続するために使用される SSL 証明書ファイルのパス。
-   デフォルト値: &quot;&quot;

### <code>cluster-ssl-key</code> {#code-cluster-ssl-key-code}

-   TiKV または PD を TLS で接続するために使用される SSL 秘密鍵ファイルのパス。
-   デフォルト値: &quot;&quot;

### <code>spilled-file-encryption-method</code> {#code-spilled-file-encryption-method-code}

-   こぼれたファイルをディスクに保存するために使用する暗号化方式を決定します。
-   デフォルト値: `"plaintext"` 、暗号化を無効にします。
-   オプションの値: `"plaintext"`および`"aes128-ctr"`

### <code>auto-tls</code> {#code-auto-tls-code}

-   起動時に TLS 証明書を自動的に生成するかどうかを決定します。
-   デフォルト値: `false`

### <code>tls-version</code> {#code-tls-version-code}

-   MySQL プロトコル接続の最小 TLS バージョンを設定します。
-   デフォルト値: &quot;&quot;。TLSv1.1 以上を許可します。
-   オプションの値: `"TLSv1.0"` 、 `"TLSv1.1"` 、 `"TLSv1.2"` 、および`"TLSv1.3"`

### <code>auth-token-jwks</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-auth-token-jwks-code-span-class-version-mark-new-in-v6-4-0-span}

> **警告：**
>
> `tidb_auth_token`認証方法は、 TiDB Cloudの内部操作のみに使用されます。この構成の値を変更し**ないでください**。

-   `tidb_auth_token`認証方法の JSON Web Key Sets (JWKS) のローカル ファイル パスを設定します。
-   デフォルト値: `""`

### <code>auth-token-refresh-interval</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-auth-token-refresh-interval-code-span-class-version-mark-new-in-v6-4-0-span}

> **警告：**
>
> `tidb_auth_token`認証方法は、 TiDB Cloudの内部操作のみに使用されます。この構成の値を変更し**ないでください**。

-   `tidb_auth_token`認証方式の JWKS 更新間隔を設定します。
-   デフォルト値: `1h`

### <span class="version-mark">v6.5.0 の新</span><code>disconnect-on-expired-password</code> {#code-disconnect-on-expired-password-code-span-class-version-mark-new-in-v6-5-0-span}

-   パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを決定します。
-   デフォルト値: `true`
-   オプションの値: `true` 、 `false`
-   `true`に設定すると、パスワードの有効期限が切れたときにクライアント接続が切断されます。 `false`に設定すると、クライアント接続は「サンドボックス モード」に制限され、ユーザーはパスワードのリセット操作のみを実行できます。

### <code>session-token-signing-cert</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-session-token-signing-cert-code-span-class-version-mark-new-in-v6-4-0-span}

> **警告：**
>
> このパラメーターによって制御される機能は開発中です。**デフォルト値を変更しないでください**。

-   デフォルト値: &quot;&quot;

### <code>session-token-signing-key</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-session-token-signing-key-code-span-class-version-mark-new-in-v6-4-0-span}

> **警告：**
>
> このパラメーターによって制御される機能は開発中です。**デフォルト値を変更しないでください**。

-   デフォルト値: &quot;&quot;

## パフォーマンス {#performance}

性能に関するコンフィグレーション項目です。

### <code>max-procs</code> {#code-max-procs-code}

-   TiDB が使用する CPU の数。
-   デフォルト値: `0`
-   デフォルトの`0`マシン上のすべての CPU を使用することを示します。 n に設定すると、TiDB は n 個の CPU を使用することもできます。

### <code>server-memory-quota</code> <span class="version-mark">v4.0.9 の新機能</span> {#code-server-memory-quota-code-span-class-version-mark-new-in-v4-0-9-span}

> **警告：**
>
> v6.5.0 以降、 `server-memory-quota`構成アイテムは廃止され、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)に置き換えられました。

-   tidb-server インスタンスのメモリ使用制限。
-   デフォルト値: `0` (バイト単位)。これは、メモリ制限がないことを意味します。

### <code>max-txn-ttl</code> {#code-max-txn-ttl-code}

-   1 つのトランザクションがロックを保持できる最長時間。この時間を超えると、トランザクションのロックが他のトランザクションによってクリアされ、このトランザクションを正常にコミットできなくなる可能性があります。
-   デフォルト値: `3600000`
-   単位：ミリ秒
-   この時間より長くロックを保持しているトランザクションは、コミットまたはロールバックすることしかできません。コミットが成功しない可能性があります。

### <code>stmt-count-limit</code> {#code-stmt-count-limit-code}

-   1 つの TiDB トランザクションで許可されるステートメントの最大数。
-   デフォルト値: `5000`
-   ステートメントの数が`stmt-count-limit`超えた後にトランザクションがロールバックまたはコミットされない場合、TiDB は`statement count 5001 exceeds the transaction limitation, autocommit = false`エラーを返します。この構成は、リトライ可能な楽観的トランザクションで**のみ**有効です。悲観的トランザクションを使用するか、トランザクションの再試行を無効にしている場合、トランザクション内のステートメントの数はこの構成によって制限されません。

### <code>txn-entry-size-limit</code> <span class="version-mark">v5.0 の新機能</span> {#code-txn-entry-size-limit-code-span-class-version-mark-new-in-v5-0-span}

-   TiDB の 1 行のデータのサイズ制限。
-   デフォルト値: `6291456` (バイト単位)
-   トランザクション内の単一のキー値レコードのサイズ制限。サイズ制限を超えると、TiDB は`entry too large`エラーを返します。この構成アイテムの最大値は`125829120` (120 MB) を超えません。
-   TiKV にも同様の制限があることに注意してください。 1 回の書き込みリクエストのデータ サイズが[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)を超える場合 (デフォルトでは 8 MB)、TiKV はこのリクエストの処理を拒否します。テーブルに大きなサイズの行がある場合、両方の構成を同時に変更する必要があります。
-   デフォルト値[`max_allowed_packet`](/system-variables.md#max_allowed_packet-new-in-v610) (MySQL プロトコルのパケットの最大サイズ) は 67108864 (64 MiB) です。行が`max_allowed_packet`より大きい場合、行は切り捨てられます。
-   デフォルト値[`txn-total-size-limit`](#txn-total-size-limit) (TiDB での単一トランザクションのサイズ制限) は 100 MiB です。 `txn-entry-size-limit`値を増やして 100 MiB を超える場合は、それに応じて`txn-total-size-limit`値を増やす必要があります。

### <code>txn-total-size-limit</code> {#code-txn-total-size-limit-code}

-   TiDB での単一トランザクションのサイズ制限。
-   デフォルト値: `104857600` (バイト単位)
-   1 回のトランザクションで、キー値レコードの合計サイズがこの値を超えることはできません。このパラメーターの最大値は`1099511627776` (1 TB) です。 binlogを使用してダウンストリーム コンシューマー Kafka ( `arbiter`クラスターなど) にサービスを提供している場合、このパラメーターの値は`1073741824` (1 GB) を超えてはならないことに注意してください。これは、Kafka が処理できる単一のメッセージ サイズの上限が 1 GB であるためです。それ以外の場合、この制限を超えるとエラーが返されます。
-   TiDB v6.5.0 以降のバージョンでは、この構成は推奨されなくなりました。トランザクションのメモリサイズはセッションのメモリ使用量に累積され、セッションメモリのしきい値を超えると[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)変数が有効になります。以前のバージョンとの互換性を保つために、以前のバージョンから TiDB v6.5.0 以降にアップグレードする場合、この構成は次のように機能します。
    -   この構成が設定されていないか、デフォルト値 ( `104857600` ) に設定されている場合、アップグレード後に、トランザクションのメモリサイズがセッションのメモリ使用量に累積され、変数`tidb_mem_quota_query`が有効になります。
    -   この構成がデフォルト ( `104857600` ) に設定されていない場合でも有効であり、単一のトランザクションのサイズを制御する動作は、アップグレードの前後で変更されません。これは、トランザクションのメモリサイズが`tidb_mem_quota_query`変数によって制御されないことを意味します。

### <code>tcp-keep-alive</code> {#code-tcp-keep-alive-code}

-   TCPレイヤーで`keepalive`を有効にするかどうかを決定します。
-   デフォルト値: `true`

### <code>tcp-no-delay</code> {#code-tcp-no-delay-code}

-   TCPレイヤーで TCP_NODELAY を有効にするかどうかを決定します。有効にすると、TiDB は TCP/IP プロトコルの Nagle アルゴリズムを無効にし、小さなデータ パケットの送信を許可してネットワークレイテンシーを短縮します。これは、データの転送量が少なく、遅延の影響を受けやすいアプリケーションに適しています。
-   デフォルト値: `true`

### <code>cross-join</code> {#code-cross-join-code}

-   デフォルト値: `true`
-   TiDB は、デフォルトで両側テーブルの条件 ( `WHERE`フィールド) なしで`JOIN`ステートメントの実行をサポートします。値を`false`に設定すると、そのような`JOIN`ステートメントが表示されたときにサーバーは実行を拒否します。

### <code>stats-lease</code> {#code-stats-lease-code}

-   統計の再ロード、表の行数の更新、自動分析の実行が必要かどうかの確認、フィードバックを使用した統計の更新、および列の統計のロードの時間間隔。
-   デフォルト値: `3s`
    -   `stats-lease`回の間隔で、TiDB は更新の統計をチェックし、更新が存在する場合はそれらをメモリに更新します。
    -   TiDB は`20 * stats-lease`回の間隔で、DML によって生成された行の総数と変更された行の数をシステム テーブルに更新します。
    -   `stats-lease`の間隔で、TiDB は自動的に分析する必要があるテーブルとインデックスをチェックします。
    -   `stats-lease`の間隔で、TiDB はメモリにロードする必要がある列統計をチェックします。
    -   `200 * stats-lease`の間隔で、TiDB はメモリにキャッシュされたフィードバックをシステム テーブルに書き込みます。
    -   `5 * stats-lease`の間隔で、TiDB はシステム テーブルのフィードバックを読み取り、メモリにキャッシュされた統計を更新します。
-   `stats-lease`を 0 に設定すると、TiDB は定期的にシステム テーブルのフィードバックを読み取り、メモリにキャッシュされた統計を 3 秒ごとに更新します。ただし、TiDB は次の統計関連のシステム テーブルを自動的に変更しなくなりました。
    -   `mysql.stats_meta` : TiDB は、トランザクションによって変更されたテーブル行の数を自動的に記録しなくなり、それをこのシステム テーブルに更新します。
    -   `mysql.stats_histograms` / `mysql.stats_buckets`および`mysql.stats_top_n` : TiDB は統計を自動的に分析し、プロアクティブに更新しなくなりました。
    -   `mysql.stats_feedback` : TiDB は、クエリされたデータによって返される統計の一部に従って、テーブルとインデックスの統計を更新しなくなります。

### <code>pseudo-estimate-ratio</code> {#code-pseudo-estimate-ratio-code}

-   テーブル内の (変更された行の数)/(行の総数) の比率。この値を超えると、システムは統計の有効期限が切れたと見なし、疑似統計が使用されます。
-   デフォルト値: `0.8`
-   最小値は`0`で、最大値は`1`です。

### <code>force-priority</code> {#code-force-priority-code}

-   すべてのステートメントの優先度を設定します。
-   デフォルト値: `NO_PRIORITY`
-   値のオプション: デフォルト値`NO_PRIORITY` 、ステートメントの優先度が強制的に変更されないことを意味します。その他のオプションは、昇順で`LOW_PRIORITY` 、 `DELAYED` 、および`HIGH_PRIORITY`です。
-   v6.1.0 以降、すべてのステートメントの優先順位は、TiDB 構成項目[`instance.tidb_force_priority`](/tidb-configuration-file.md#tidb_force_priority)またはシステム変数[`tidb_force_priority`](/system-variables.md#tidb_force_priority)によって決定されます。 `force-priority`は引き続き有効です。ただし、 `force-priority`と`instance.tidb_force_priority`同時に設定した場合は、後者が有効になります。

### <code>distinct-agg-push-down</code> {#code-distinct-agg-push-down-code}

-   オプティマイザが`Distinct` ( `select count(distinct a) from t`など) の集計関数をコプロセッサにプッシュ ダウンする操作を実行するかどうかを決定します。
-   デフォルト: `false`
-   この変数は、システム変数[`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)の初期値です。

### <code>enforce-mpp</code> {#code-enforce-mpp-code}

-   オプティマイザーのコスト見積もりを無視して、強制的に TiFlash の MPP モードをクエリ実行に使用するかどうかを決定します。
-   デフォルト値: `false`
-   この構成アイテムは、 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。たとえば、この構成項目が`true`に設定されている場合、デフォルト値の`tidb_enforce_mpp`は`ON`です。

### <code>enable-stats-cache-mem-quota</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-enable-stats-cache-mem-quota-code-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> この変数は実験的機能です。本番環境で使用することはお勧めしません。

-   統計キャッシュのメモリクォータを有効にするかどうかを制御します。
-   デフォルト値: `false`

### <code>stats-load-concurrency</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-stats-load-concurrency-code-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、統計の同期読み込みは実験的機能です。本番環境で使用することはお勧めしません。

-   TiDB 同期ロード統計機能が同時に処理できる列の最大数。
-   デフォルト値: `5`
-   現在、有効な値の範囲は`[1, 128]`です。

### <code>stats-load-queue-size</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-stats-load-queue-size-code-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、統計の同期読み込みは実験的機能です。本番環境で使用することはお勧めしません。

-   TiDB 同期読み込み統計機能がキャッシュできる列リクエストの最大数。
-   デフォルト値: `1000`
-   現在、有効な値の範囲は`[1, 100000]`です。

## オープントレース {#opentracing}

opentracing に関連するコンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   一部の TiDB コンポーネントの呼び出しオーバーヘッドを追跡するための opentracing を有効にします。 opentracing を有効にすると、パフォーマンスが低下することに注意してください。
-   デフォルト値: `false`

### <code>rpc-metrics</code> {#code-rpc-metrics-code}

-   RPC メトリックを有効にします。
-   デフォルト値: `false`

## opentracing.sampler {#opentracing-sampler}

opentracing.sampler に関するコンフィグレーション項目です。

### <code>type</code> {#code-type-code}

-   opentracing サンプラーのタイプを指定します。文字列値は大文字と小文字を区別しません。
-   デフォルト値: `"const"`
-   値のオプション: `"const"` 、 `"probabilistic"` 、 `"ratelimiting"` 、 `"remote"`

### <code>param</code> {#code-param-code}

-   opentracing サンプラーのパラメーター。
    -   `const`タイプの場合、値は`0`または`1`で、 `const`サンプラーを有効にするかどうかを示します。
    -   `probabilistic`タイプの場合、パラメーターはサンプリング確率を指定します。これは、 `0`から`1`までの浮動小数点数にすることができます。
    -   `ratelimiting`タイプの場合、パラメーターは 1 秒あたりにサンプリングされるスパンの数を指定します。
    -   `remote`タイプの場合、パラメーターはサンプリング確率を指定します。これは、 `0`から`1`までの浮動小数点数にすることができます。
-   デフォルト値: `1.0`

### <code>sampling-server-url</code> {#code-sampling-server-url-code}

-   jaeger-agent サンプリングサーバーの HTTP URL。
-   デフォルト値: `""`

### <code>max-operations</code> {#code-max-operations-code}

-   サンプラーがトレースできる操作の最大数。操作がトレースされない場合、デフォルトの確率的サンプラーが使用されます。
-   デフォルト値: `0`

### <code>sampling-refresh-interval</code> {#code-sampling-refresh-interval-code}

-   jaeger-agent サンプリング ポリシーをポーリングする頻度を制御します。
-   デフォルト値: `0`

## opentracing.reporter {#opentracing-reporter}

opentracing.reporter に関するコンフィグレーション項目です。

### <code>queue-size</code> {#code-queue-size-code}

-   レポーター レコードがメモリ内にまたがるキュー サイズ。
-   デフォルト値: `0`

### <code>buffer-flush-interval</code> {#code-buffer-flush-interval-code}

-   レポーターがメモリ内のスパンをstorageにフラッシュする間隔。
-   デフォルト値: `0`

### <code>log-spans</code> {#code-log-spans-code}

-   送信されたすべてのスパンのログを出力するかどうかを決定します。
-   デフォルト値: `false`

### <code>local-agent-host-port</code> {#code-local-agent-host-port-code}

-   レポーターがスパンを jaeger-agent に送信するアドレス。
-   デフォルト値: `""`

## tikv クライアント {#tikv-client}

### <code>grpc-connection-count</code> {#code-grpc-connection-count-code}

-   各 TiKV で確立される接続の最大数。
-   デフォルト値: `4`

### <code>grpc-keepalive-time</code> {#code-grpc-keepalive-time-code}

-   TiDB ノードと TiKV ノード間の RPC 接続の`keepalive`時間間隔。指定された時間間隔内にネットワーク パケットがない場合、gRPC クライアントは TiKV に対して`ping`コマンドを実行して、生きているかどうかを確認します。
-   デフォルト: `10`
-   単位：秒

### <code>grpc-keepalive-timeout</code> {#code-grpc-keepalive-timeout-code}

-   TiDB ノードと TiKV ノード間の RPC `keepalive`チェックのタイムアウト。
-   デフォルト値: `3`
-   単位：秒

### <code>grpc-compression-type</code> {#code-grpc-compression-type-code}

-   TiDB ノードと TiKV ノード間のデータ転送に使用される圧縮タイプを指定します。デフォルト値は`"none"`で、これは圧縮なしを意味します。 gzip 圧縮を有効にするには、この値を`"gzip"`に設定します。
-   デフォルト値: `"none"`
-   値のオプション: `"none"` 、 `"gzip"`

### <code>commit-timeout</code> {#code-commit-timeout-code}

-   トランザクションコミット実行時の最大タイムアウト。
-   デフォルト値: `41s`
-   この値をRaft選択タイムアウトの 2 倍より大きく設定する必要があります。

### <code>max-batch-size</code> {#code-max-batch-size-code}

-   バッチで送信される RPC パケットの最大数。値が`0`でない場合、 `BatchCommands` API を使用してリクエストが TiKV に送信され、同時実行性が高い場合は RPCレイテンシーを短縮できます。この値は変更しないことをお勧めします。
-   デフォルト値: `128`

### <code>max-batch-wait-time</code> {#code-max-batch-wait-time-code}

-   `max-batch-wait-time`がデータ パケットをバッチで大きなパケットにカプセル化し、TiKV ノードに送信するのを待ちます。 `tikv-client.max-batch-size`の値が`0`より大きい場合にのみ有効です。この値は変更しないことをお勧めします。
-   デフォルト値: `0`
-   単位：ナノ秒

### <code>batch-wait-size</code> {#code-batch-wait-size-code}

-   バッチで TiKV に送信されるパケットの最大数。この値は変更しないことをお勧めします。
-   デフォルト値: `8`
-   値が`0`の場合、この機能は無効になります。

### <code>overload-threshold</code> {#code-overload-threshold-code}

-   TiKV 負荷のしきい値。 TiKV 負荷がこのしきい値を超えると、TiKV の圧力を軽減するために、より多くの`batch`パケットが収集されます。 `tikv-client.max-batch-size`の値が`0`より大きい場合にのみ有効です。この値は変更しないことをお勧めします。
-   デフォルト値: `200`

## tikv-client.copr-cache <span class="version-mark">v4.0.0 の新機能</span> {#tikv-client-copr-cache-span-class-version-mark-new-in-v4-0-0-span}

このセクションでは、コプロセッサーキャッシュ機能に関連する設定項目を紹介します。

### <code>capacity-mb</code> {#code-capacity-mb-code}

-   キャッシュされたデータの合計サイズ。キャッシュ スペースがいっぱいになると、古いキャッシュ エントリが削除されます。値が`0.0`の場合、コプロセッサー・キャッシュ機能は無効になります。
-   デフォルト値: `1000.0`
-   単位：MB
-   タイプ: フロート

## txn ローカル ラッチ {#txn-local-latches}

トランザクション ラッチに関するコンフィグレーション。多くのローカル トランザクションの競合が発生する場合は、有効にすることをお勧めします。

### <code>enabled</code> {#code-enabled-code}

-   トランザクションのメモリロックを有効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>capacity</code> {#code-capacity-code}

-   ハッシュに対応するスロットの数。2 の指数倍数に自動的に調整されます。各スロットは 32 バイトのメモリを占有します。設定が小さすぎると、データの書き込みが比較的広い範囲をカバーするシナリオ (データのインポートなど) で、実行速度が遅くなり、パフォーマンスが低下する可能性があります。
-   デフォルト値: `2048000`

## binlog {#binlog}

TiDB Binlogに関連する構成。

### <code>enable</code> {#code-enable-code}

-   binlog を有効または無効にします。
-   デフォルト値: `false`

### <code>write-timeout</code> {#code-write-timeout-code}

-   binlogをPumpに書き込む際のタイムアウト。この値を変更することはお勧めしません。
-   デフォルト: `15s`
-   単位：秒

### <code>ignore-error</code> {#code-ignore-error-code}

-   binlog をPumpに書き込むプロセスで発生したエラーを無視するかどうかを決定します。この値を変更することはお勧めしません。
-   デフォルト値: `false`
-   値を`true`に設定してエラーが発生すると、TiDB はbinlog の書き込みを停止し、 `tidb_server_critical_error_total`監視項目のカウントに`1`を追加します。値が`false`に設定されている場合、 binlog の書き込みは失敗し、TiDB サービス全体が停止します。

### <code>binlog-socket</code> {#code-binlog-socket-code}

-   binlogのエクスポート先のネットワーク アドレス。
-   デフォルト値: &quot;&quot;

### <code>strategy</code> {#code-strategy-code}

-   binlogをエクスポートするときのPump選択の戦略。現在、 `hash`と`range`方法のみがサポートされています。
-   デフォルト値: `range`

## スターテス {#status}

TiDB サービスのステータスに関するコンフィグレーション。

### <code>report-status</code> {#code-report-status-code}

-   HTTP API サービスを有効または無効にします。
-   デフォルト値: `true`

### <code>record-db-qps</code> {#code-record-db-qps-code}

-   データベース関連の QPS メトリクスを Prometheus に送信するかどうかを決定します。
-   デフォルト値: `false`

## pessimistic-txn {#pessimistic-txn}

悲観的トランザクションの使用法については、 [TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)を参照してください。

### max-retry-count {#max-retry-count}

-   悲観的トランザクションでの各ステートメントの最大再試行回数。再試行回数がこの制限を超えると、エラーが発生します。
-   デフォルト値: `256`

### deadlock-history-capacity {#deadlock-history-capacity}

-   1 つの TiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)のテーブルに記録できるデッドロック イベントの最大数。このテーブルがいっぱいになり、追加のデッドロック イベントが発生した場合、テーブル内の最も古いレコードが削除され、最新のエラーに対応します。
-   デフォルト値: `10`
-   最小値: `0`
-   最大値: `10000`

### deadlock-history-collect-retryable {#deadlock-history-collect-retryable}

-   [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロック エラーの情報を収集するかどうかを制御します。再試行可能なデッドロック エラーの説明については、 [再試行可能なデッドロック エラー](/information-schema/information-schema-deadlocks.md#retryable-deadlock-errors)を参照してください。
-   デフォルト値: `false`

### pessimistic-auto-commit<span class="version-mark">v6.0.0 の新機能</span> {#pessimistic-auto-commit-span-class-version-mark-new-in-v6-0-0-span}

-   悲観的トランザクション モードがグローバルに有効になっている場合 ( `tidb_txn_mode='pessimistic'` )、自動コミット トランザクションが使用するトランザクション モードを決定します。デフォルトでは、悲観的トランザクション モードがグローバルに有効になっている場合でも、自動コミット トランザクションは引き続き楽観的トランザクション モードを使用します。 `pessimistic-auto-commit`を有効にした後 ( `true`に設定)、自動コミット トランザクションは悲観的モードも使用します。これは、他の明示的にコミットされた悲観的トランザクションと一致します。
-   競合のあるシナリオでは、この構成を有効にした後、TiDB は自動コミット トランザクションをグローバル ロックレイテンシー管理に含めます。
-   競合のないシナリオの場合、多くの自動コミット トランザクションがある場合 (具体的な数は実際のシナリオによって決定されます。たとえば、自動コミット トランザクションの数は、アプリケーションの総数の半分以上を占めます)。 1 つのトランザクションで大量のデータが処理されるため、この構成を有効にするとパフォーマンスが低下します。たとえば、auto-commit `INSERT INTO SELECT`ステートメントです。
-   デフォルト値: `false`

### constraint-check-in-place-pessimistic <span class="version-mark">v6.4.0 の新機能</span> {#constraint-check-in-place-pessimistic-span-class-version-mark-new-in-v6-4-0-span}

-   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)のデフォルト値を制御します。
-   デフォルト値: `true`

## 分離読み取り {#isolation-read}

読み取り分離に関連するコンフィグレーション項目。

### <code>engines</code> {#code-engines-code}

-   TiDB がデータの読み取りを許可するエンジンを制御します。
-   デフォルト値: [&quot;tikv&quot;, &quot;tiflash&quot;, &quot;tidb&quot;]。エンジンがオプティマイザによって自動的に選択されることを示します。
-   値のオプション: 「tikv」、「tiflash」、および「tidb」の任意の組み合わせ。たとえば、[&quot;tikv&quot;, &quot;tidb&quot;] または [&quot;tiflash&quot;, &quot;tidb&quot;]

## 実例 {#instance}

### <code>tidb_enable_collect_execution_info</code> {#code-tidb-enable-collect-execution-info-code}

-   この構成は、各オペレーターの実行情報をスロー クエリ ログに記録するかどうかを制御します。
-   デフォルト値: `true`
-   v6.1.0 より前では、この構成は`enable-collect-execution-info`で設定されています。

### <code>tidb_enable_slow_log</code> {#code-tidb-enable-slow-log-code}

-   この構成は、スロー ログ機能を有効にするかどうかを制御するために使用されます。
-   デフォルト値: `true`
-   値のオプション: `true`または`false`
-   v6.1.0 より前では、この構成は`enable-slow-log`で設定されます。

### <code>tidb_slow_log_threshold</code> {#code-tidb-slow-log-threshold-code}

-   この構成は、スローログの消費時間のしきい値を出力するために使用されます。クエリの消費時間がこの値よりも大きい場合、そのクエリはスロー ログと見なされ、そのログがスロー クエリ ログに出力されます。
-   デフォルト値: `300`
-   範囲: `[-1, 9223372036854775807]`
-   単位: ミリ秒
-   v6.1.0 より前では、この構成は`slow-threshold`で設定されます。

### <code>tidb_record_plan_in_slow_log</code> {#code-tidb-record-plan-in-slow-log-code}

-   この構成は、スロー ログにスロー クエリの実行プランを含めるかどうかを制御するために使用されます。
-   デフォルト値: `1`
-   値のオプション: `1` (有効、デフォルト) または`0` (無効)。
-   この構成の値は、システム変数[`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log)の値を初期化します
-   v6.1.0 より前では、この構成は`record-plan-in-slow-log`で設定されます。

### <code>tidb_force_priority</code> {#code-tidb-force-priority-code}

-   この構成は、TiDBサーバーで実行されるステートメントのデフォルトの優先順位を変更するために使用されます。
-   デフォルト値: `NO_PRIORITY`
-   デフォルト値`NO_PRIORITY`は、ステートメントの優先度が強制的に変更されないことを意味します。その他のオプションは、昇順で`LOW_PRIORITY` 、 `DELAYED` 、および`HIGH_PRIORITY`です。
-   v6.1.0 より前では、この構成は`force-priority`で設定されます。

### <code>max_connections</code> {#code-max-connections-code}

-   1 つの TiDB インスタンスに許可される接続の最大数。リソース制御に使用できます。
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   デフォルト値`0`は制限なしを意味します。この変数の値が`0`よりも大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新しい接続を拒否します。
-   この構成の値は、システム変数[`max_connections`](/system-variables.md#max_connections)の値を初期化します
-   v6.2.0 より前では、この構成は`max-server-connections`で設定されます。

### <code>tidb_enable_ddl</code> {#code-tidb-enable-ddl-code}

-   この構成は、対応する TiDB インスタンスが DDL 所有者になることができるかどうかを制御します。
-   デフォルト値: `true`
-   可能な値: `OFF` 、 `ON`
-   この構成の値は、システム変数[`tidb_enable_ddl`](/system-variables.md#tidb_enable_ddl)の値を初期化します
-   v6.3.0 より前では、この構成は`run-ddl`で設定されています。

## プロキシプロトコル {#proxy-protocol}

PROXY プロトコルに関するコンフィグレーション項目です。

### <code>networks</code> {#code-networks-code}

-   [プロキシ プロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を使用して TiDB に接続できるプロキシ サーバーの IP アドレスのリスト
-   デフォルト値: &quot;&quot;
-   一般に、リバース プロキシの背後にある TiDB にアクセスすると、TiDB はリバース プロキシサーバーの IP アドレスをクライアントの IP アドレスとして取得します。 PROXY プロトコルを有効にすることで、このプロトコルをサポートする HAProxy などのリバース プロキシは、実際のクライアント IP アドレスを TiDB に渡すことができます。
-   このパラメータを設定すると、TiDB は、設定された送信元 IP アドレスが PROXY プロトコルを使用して TiDB に接続できるようにします。 PROXY 以外のプロトコルが使用されている場合、この接続は拒否されます。このパラメーターを空のままにすると、PROXY プロトコルを使用して IP アドレスが TiDB に接続できなくなります。値は、IP アドレス (192.168.1.50) または CIDR (192.168.1.0/24) で、区切り記号として`,`を使用できます。 `*`任意の IP アドレスを意味します。

> **警告：**
>
> `*`を使用すると、任意の IP アドレスのクライアントがその IP アドレスを報告できるようになり、セキュリティ上のリスクが生じる可能性があるため、注意して使用してください。さらに、 `*`を使用すると、TiDB に直接接続する内部コンポーネント(TiDB ダッシュボードなど) が使用できなくなる可能性もあります。

## 実験的 {#experimental}

v3.1.0 で導入された`experimental`セクションでは、TiDB の実験的機能に関連する構成について説明します。

### <code>allow-expression-index</code> <span class="version-mark">v4.0.0 の新機能</span> {#code-allow-expression-index-code-span-class-version-mark-new-in-v4-0-0-span}

-   式インデックスを作成できるかどうかを制御します。 TiDB v5.2.0 以降、式の関数が安全な場合、この構成を有効にしなくても、この関数に基づいて式インデックスを直接作成できます。他の関数に基づいて式インデックスを作成する場合は、この構成を有効にできますが、正確性の問題が存在する可能性があります。 `tidb_allow_function_for_expression_index`変数を照会することで、式の作成に直接使用しても安全な関数を取得できます。
-   デフォルト値: `false`
