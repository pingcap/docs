---
title: TiDB Configuration File
summary: コマンドライン オプションに関係しない TiDB 構成ファイル オプションについて学習します。
---

<!-- markdownlint-disable MD001 -->

<!-- markdownlint-disable MD024 -->

# TiDBコンフィグレーションファイル {#tidb-configuration-file}

TiDB 構成ファイルは、コマンドライン パラメータよりも多くのオプションをサポートしています。デフォルトの構成ファイル[`config.toml.example`](https://github.com/pingcap/tidb/blob/release-8.1/pkg/config/config.toml.example)をダウンロードして、名前を`config.toml`に変更することができます。このドキュメントでは、 [コマンドラインオプション](/command-line-flags-for-tidb-configuration.md)に関係のないオプションについてのみ説明します。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>split-table</code> {#code-split-table-code}

-   各テーブルに個別のリージョンを作成するかどうかを決定します。
-   デフォルト値: `true`
-   多数のテーブル (たとえば、10 万を超えるテーブル) を作成する必要がある場合は、 `false`に設定することをお勧めします。

### <code>tidb-max-reuse-chunk</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-tidb-max-reuse-chunk-code-span-class-version-mark-new-in-v6-4-0-span}

-   チャンク割り当ての最大キャッシュ チャンク オブジェクトを制御します。この構成項目を大きすぎる値に設定すると、OOM のリスクが増大する可能性があります。
-   デフォルト値: `64`
-   最小値: `0`
-   最大値: `2147483647`

### <code>tidb-max-reuse-column</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-tidb-max-reuse-column-code-span-class-version-mark-new-in-v6-4-0-span}

-   チャンク割り当ての最大キャッシュ列オブジェクトを制御します。この構成項目を大きすぎる値に設定すると、OOM のリスクが増大する可能性があります。
-   デフォルト値: `256`
-   最小値: `0`
-   最大値: `2147483647`

### <code>token-limit</code> {#code-token-limit-code}

-   リクエストを同時に実行できるセッションの数。
-   タイプ: 整数
-   デフォルト値: `1000`
-   最小値: `1`
-   最大値（64 ビット プラットフォーム）: `18446744073709551615`
-   最大値（32 ビット プラットフォーム）: `4294967295`

### <code>temp-dir</code> <span class="version-mark">v6.3.0 の新機能</span> {#code-temp-dir-code-span-class-version-mark-new-in-v6-3-0-span}

-   TiDB が一時データを保存するために使用するファイル システムの場所。機能で TiDB ノードにローカルstorageが必要な場合、TiDB は対応する一時データをこの場所に保存します。
-   インデックスを作成するときに、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)を有効にすると、新しく作成されたインデックスのバックフィルが必要なデータは、最初に TiDB のローカル一時ディレクトリに保存され、その後バッチで TiKV にインポートされるため、インデックスの作成が高速化されます。
-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)を使用してデータをインポートすると、ソートされたデータは最初に TiDB のローカル一時ディレクトリに保存され、その後バッチで TiKV にインポートされます。
-   デフォルト値: `"/tmp/tidb"`

> **注記：**
>
> ディレクトリが存在しない場合は、TiDB は起動時に自動的に作成します。ディレクトリの作成に失敗した場合、または TiDB にそのディレクトリに対する読み取りおよび書き込み権限がない場合は[`Fast Online DDL`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)予期しない問題が発生する可能性があります。

### <code>oom-use-tmp-storage</code> {#code-oom-use-tmp-storage-code}

> **警告：**
>
> v6.3.0 以降、この構成項目は非推奨となり、システム変数[`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom)に置き換えられました。TiDB クラスターを v6.3.0 以降のバージョンにアップグレードすると、変数は自動的に`oom-use-tmp-storage`の値で初期化されます。その後、 `oom-use-tmp-storage`の値を変更しても有効に**なりません**。

-   単一の SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部の演算子の一時storageを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>tmp-storage-path</code> {#code-tmp-storage-path-code}

-   単一の SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部の演算子の一時storageパスを指定します。
-   デフォルト値: `<temporary directory of OS>/<OS user ID>_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage` 。 `MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=`は`<host>:<port>/<statusHost>:<statusPort>`の`Base64`エンコード結果です。
-   この構成は、システム変数[`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom)が`ON`の場合にのみ有効になります。

### <code>tmp-storage-quota</code> {#code-tmp-storage-quota-code}

-   storageのクォータを`tmp-storage-path`で指定します。単位はバイトです。
-   単一の SQL ステートメントが一時ディスクを使用し、TiDBサーバーの一時ディスクの合計容量がこの設定値を超えると、現在の SQL 操作はキャンセルされ、エラー`Out of Global Storage Quota!`が返されます。
-   この設定の値が`0`未満の場合、上記のチェックと制限は適用されません。
-   デフォルト値: `-1`
-   `tmp-storage-path`の残りの使用可能なstorageが`tmp-storage-quota`で定義された値よりも少ない場合、 TiDBサーバーは起動時にエラーを報告し、終了します。

### <code>lease</code> {#code-lease-code}

-   DDL リースのタイムアウト。
-   デフォルト値: `45s`
-   単位: 秒

### <code>compatible-kill-query</code> {#code-compatible-kill-query-code}

-   `KILL`ステートメントを MySQL 互換に設定するかどうかを決定します。
-   デフォルト値: `false`
-   `compatible-kill-query` [`enable-global-kill`](#enable-global-kill-new-in-v610)が`false`に設定されている場合にのみ有効になります。
-   [`enable-global-kill`](#enable-global-kill-new-in-v610)が`false`の場合、 `compatible-kill-query`クエリを強制終了するときに`TIDB`キーワードを追加する必要があるかどうかを制御します。
    -   `compatible-kill-query`が`false`の場合、TiDB の`KILL xxx`の動作は MySQL とは異なります。TiDB でクエリを強制終了するには、 `KILL TIDB xxx`のように`TIDB`キーワードを追加する必要があります。
    -   `compatible-kill-query`が`true`の場合、TiDB でクエリを強制終了するには、キーワード`TIDB`を追加する必要はありません。クライアントが常に同じ TiDB インスタンスに接続されることが確実でない限り、構成ファイルで`compatible-kill-query`を`true`に設定することは**強く推奨されません**。これは、デフォルトの MySQL クライアントで<kbd>Control</kbd> + <kbd>C</kbd>を押すと、 `KILL`が実行される新しい接続が開かれるためです。クライアントと TiDB クラスターの間にプロキシがある場合、新しい接続は別の TiDB インスタンスにルーティングされる可能性があり、誤って別のセッションが強制終了される可能性があります。
-   [`enable-global-kill`](#enable-global-kill-new-in-v610)が`true`の場合、 `KILL xxx`と`KILL TIDB xxx`同じ効果がありますが、クエリを強制終了するために<kbd>Control</kbd> + <kbd>C</kbd>を使用することはサポートされていません。
-   `KILL`ステートメントの詳細については、 [殺す [TIDB]](/sql-statements/sql-statement-kill.md)を参照してください。

### <code>check-mb4-value-in-utf8</code> {#code-check-mb4-value-in-utf8-code}

-   `utf8mb4`文字のチェックを有効にするかどうかを決定します。この機能を有効にすると、文字セットが`utf8`で、 `mb4`文字が`utf8`に挿入されると、エラーが返されます。
-   デフォルト値: `false`
-   v6.1.0 以降、 `utf8mb4`文字チェックを有効にするかどうかは、TiDB 構成項目`instance.tidb_check_mb4_value_in_utf8`またはシステム変数`tidb_check_mb4_value_in_utf8`によって決定されます。7 `check-mb4-value-in-utf8`引き続き有効です。ただし、 `check-mb4-value-in-utf8`と`instance.tidb_check_mb4_value_in_utf8`両方が設定されている場合は、後者が有効になります。

### <code>treat-old-version-utf8-as-utf8mb4</code> {#code-treat-old-version-utf8-as-utf8mb4-code}

-   古いテーブル内の`utf8`文字セットを`utf8mb4`として扱うかどうかを決定します。
-   デフォルト値: `true`

### <code>alter-primary-key</code> (非推奨) {#code-alter-primary-key-code-deprecated}

-   列に主キー制約を追加するか、列から主キー制約を削除するかを決定します。
-   デフォルト値: `false`
-   このデフォルト設定では、主キー制約の追加または削除はサポートされていません。 `alter-primary-key`を`true`に設定することで、この機能を有効にすることができます。ただし、スイッチをオンにする前にテーブルが既に存在し、その主キー列のデータ型が整数である場合、この構成項目を`true`に設定しても、列から主キーを削除することはできません。

> **注記：**
>
> この構成項目は非推奨になっており、現在は`@tidb_enable_clustered_index`の値が`INT_ONLY`の場合にのみ有効になります。主キーを追加または削除する必要がある場合は、テーブルの作成時に代わりに`NONCLUSTERED`キーワードを使用します。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。

### <code>server-version</code> {#code-server-version-code}

-   次の状況で TiDB によって返されるバージョン文字列を変更します。
    -   組み込み関数`VERSION()`を使用する場合。
    -   TiDB がクライアントとの初期接続を確立し、サーバーのバージョン文字列を含む初期ハンドシェイク パケットを返すとき。詳細については、 [MySQL 初期ハンドシェイク パケット](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_connection_phase.html#sect_protocol_connection_phase_initial_handshake)参照してください。
-   デフォルト値: &quot;&quot;
-   デフォルトでは、TiDB バージョン文字列の形式は`8.0.11-TiDB-${tidb_version}`です。

> **注記：**
>
> TiDB ノードは、現在の TiDB バージョンを確認するために値`server-version`を使用します。したがって、予期しない動作を回避するには、TiDB クラスターをアップグレードする前に、値`server-version`を空または現在の TiDB クラスターの実際のバージョンに設定する必要があります。

### <code>repair-mode</code> {#code-repair-mode-code}

-   信頼できない修復モードを有効にするかどうかを決定します。 `repair-mode` `true`に設定すると、 `repair-table-list`の不良テーブルをロードできません。
-   デフォルト値: `false`
-   `repair`構文はデフォルトではサポートされていません。つまり、TiDB の起動時にすべてのテーブルがロードされます。

### <code>repair-table-list</code> {#code-repair-table-list-code}

-   `repair-table-list` 、 [`repair-mode`](#repair-mode)が`true`に設定されている場合にのみ有効です。 `repair-table-list` 、インスタンスで修復する必要がある不良テーブルのリストです。 リストの例: [&quot;db.table1&quot;,&quot;db.table2&quot;...]。
-   デフォルト値: []
-   デフォルトではリストは空です。これは、修復する必要がある不良テーブルがないことを意味します。

### <code>new_collations_enabled_on_first_bootstrap</code> {#code-new-collations-enabled-on-first-bootstrap-code}

-   新しい照合順序のサポートを有効または無効にします。
-   デフォルト値: `true`
-   注意: この構成は、最初に初期化された TiDB クラスターに対してのみ有効です。初期化後は、この構成項目を使用して新しい照合順序のサポートを有効または無効にすることはできません。

### <code>max-server-connections</code> {#code-max-server-connections-code}

-   TiDB で許可される同時クライアント接続の最大数。リソースを制御するために使用されます。
-   デフォルト値: `0`
-   デフォルトでは、TiDB は同時クライアント接続の数に制限を設定しません。この構成項目の値が`0`より大きく、実際のクライアント接続の数がこの値に達すると、TiDBサーバーは新しいクライアント接続を拒否します。
-   v6.2.0 以降、TiDB 構成項目[`instance.max_connections`](/tidb-configuration-file.md#max_connections)またはシステム変数[`max_connections`](/system-variables.md#max_connections)を使用して、TiDB で許可される同時クライアント接続の最大数を設定します。5 `max-server-connections`引き続き有効です。ただし、 `max-server-connections`と`instance.max_connections`同時に設定されている場合、後者が有効になります。

### <code>max-index-length</code> {#code-max-index-length-code}

-   新しく作成されるインデックスの最大許容長を設定します。
-   デフォルト値: `3072`
-   単位: バイト
-   現在、有効な値の範囲は`[3072, 3072*4]`です。MySQL と TiDB (バージョン &lt; v3.0.11) にはこの設定項目はありませんが、どちらも新しく作成されるインデックスの長さを制限します。MySQL でのこの制限は`3072`です。TiDB (バージョン =&lt; 3.0.7) では、この制限は`3072*4`です。TiDB (3.0.7 &lt; バージョン &lt; 3.0.11) では、この制限は`3072`です。この設定は、MySQL および以前のバージョンの TiDB との互換性を確保するために追加されました。

### <code>table-column-count-limit</code> <span class="version-mark">v5.0 の新機能</span> {#code-table-column-count-limit-code-span-class-version-mark-new-in-v5-0-span}

-   単一のテーブル内の列数の制限を設定します。
-   デフォルト値: `1017`
-   現在、有効な値の範囲は`[1017, 4096]`です。

### <code>index-limit</code> <span class="version-mark">v5.0 の新</span>機能 {#code-index-limit-code-span-class-version-mark-new-in-v5-0-span}

-   単一テーブル内のインデックスの数の制限を設定します。
-   デフォルト値: `64`
-   現在、有効な値の範囲は`[64, 512]`です。

### <code>enable-telemetry</code> <span class="version-mark">v4.0.2 の新機能</span> {#code-enable-telemetry-code-span-class-version-mark-new-in-v4-0-2-span}

-   TiDB でのテレメトリ収集を有効または無効にします。
-   デフォルト値: `false`
-   TiDB インスタンスでこの構成を`true`に設定すると、この TiDB インスタンスでのテレメトリ収集が有効になり、 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数が有効になります。
-   すべての TiDB インスタンスでこの構成が`false`に設定されている場合、TiDB のテレメトリ収集は無効になり、 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数は有効になりません。詳細については、 [テレメトリー](/telemetry.md)参照してください。

### <code>deprecate-integer-display-length</code> {#code-deprecate-integer-display-length-code}

-   この構成項目が`true`に設定されている場合、整数型の表示幅は非推奨になります。
-   デフォルト値: `false`

### <code>enable-tcp4-only</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-tcp4-only-code-span-class-version-mark-new-in-v5-0-span}

-   TCP4 のみのリッスンを有効または無効にします。
-   デフォルト値: `false`
-   このオプションを有効にすると、 [TCP ヘッダーからの実際のクライアント IP](https://github.com/alibaba/LVS/tree/master/kernel/net/toa) 「tcp4」プロトコルによって正しく解析できるため、負荷分散のために TiDB が LVS と共に使用される場合に便利です。

### <code>enable-enum-length-limit</code> <span class="version-mark">v5.0 の新機能</span> {#code-enable-enum-length-limit-code-span-class-version-mark-new-in-v5-0-span}

-   単一の`ENUM`要素と単一の`SET`要素の最大長を制限するかどうかを決定します。
-   デフォルト値: `true`
-   この設定値が`true`の場合、単一の`ENUM`要素と単一の`SET`要素の最大長は 255 文字となり、 [MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/string-type-syntax.html)と互換性があります。この設定値が`false`の場合、単一の要素の長さに制限はなく、TiDB (v5.0 より前) と互換性があります。

### <code>graceful-wait-before-shutdown</code> <span class="version-mark">v5.0 の新機能</span> {#code-graceful-wait-before-shutdown-code-span-class-version-mark-new-in-v5-0-span}

-   サーバーをシャットダウンしてクライアントが切断できるようにする際に TiDB が待機する秒数を指定します。
-   デフォルト値: `0`
-   TiDB がシャットダウンを待機している場合 (猶予期間中)、HTTP ステータスは失敗を示し、ロード バランサーはトラフィックを再ルーティングできます。

> **注記：**
>
> TiDB がサーバーをシャットダウンするまでの待機時間は、次のパラメータによっても影響を受けます。
>
> -   SystemD を採用しているプラ​​ットフォームを使用する場合、デフォルトの停止タイムアウトは 90 秒です。より長いタイムアウトが必要な場合は、 [`TimeoutStopSec=`](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html#TimeoutStopSec=)設定できます。
>
> -   TiUP クラスタコンポーネントを使用する場合、 [`--wait-timeout`](/tiup/tiup-component-cluster.md#--wait-timeout) 120 秒です。
>
> -   Kubernetes を使用する場合、デフォルトは[`terminationGracePeriodSeconds`](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#lifecycle)で 30 秒です。

### <code>enable-global-kill</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-enable-global-kill-code-span-class-version-mark-new-in-v6-1-0-span}

-   グローバル キル (インスタンス間のクエリまたは接続の終了) 機能を有効にするかどうかを制御します。
-   デフォルト値: `true`
-   値が`true`の場合、 `KILL`と`KILL TIDB`両方のステートメントでインスタンス間のクエリまたは接続を終了できるため、クエリまたは接続が誤って終了することを心配する必要はありません。クライアントを使用して任意の TiDB インスタンスに接続し、 `KILL`または`KILL TIDB`ステートメントを実行すると、ステートメントはターゲット TiDB インスタンスに転送されます。クライアントと TiDB クラスターの間にプロキシがある場合は、 `KILL`と`KILL TIDB`ステートメントもターゲット TiDB インスタンスに転送されて実行されます。
-   v7.3.0 以降では、 `enable-global-kill`と[`enable-32bits-connection-id`](#enable-32bits-connection-id-new-in-v730)両方が`true`に設定されている場合、MySQL コマンドラインの<kbd>Control+C</kbd>を使用してクエリまたは接続を終了できます。詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)を参照してください。

### <code>enable-32bits-connection-id</code> <span class="version-mark">v7.3.0 の新機能</span> {#code-enable-32bits-connection-id-code-span-class-version-mark-new-in-v7-3-0-span}

-   32 ビット接続 ID 機能を有効にするかどうかを制御します。
-   デフォルト値: `true`
-   この設定項目と[`enable-global-kill`](#enable-global-kill-new-in-v610)両方を`true`に設定すると、TiDB は 32 ビットの接続 ID を生成します。これにより、MySQL コマンドラインの<kbd>Control+C</kbd>でクエリまたは接続を終了できるようになります。

> **警告：**
>
> クラスター内の TiDB インスタンスの数が 2048 を超えるか、単一の TiDB インスタンスの同時接続数が 1048576 を超えると、32 ビット接続 ID スペースが不足し、自動的に 64 ビット接続 ID にアップグレードされます。アップグレード プロセス中、既存のビジネス接続と確立された接続は影響を受けません。ただし、後続の新しい接続は、MySQL コマンドラインで<kbd>Control+C</kbd>を使用して終了することはできません。

### <code>initialize-sql-file</code> <span class="version-mark">v6.6.0の新機能</span> {#code-initialize-sql-file-code-span-class-version-mark-new-in-v6-6-0-span}

-   TiDB クラスターを初めて起動したときに実行される SQL スクリプトを指定します。
-   デフォルト値: `""`
-   このスクリプト内のすべての SQL ステートメントは、権限チェックなしで最高の権限で実行されます。指定された SQL スクリプトの実行に失敗した場合、TiDB クラスターの起動に失敗する可能性があります。
-   この構成項目は、システム変数の値の変更、ユーザーの作成、権限の付与などの操作を実行するために使用されます。

### <code>enable-forwarding</code> <span class="version-mark">v5.0.0 の新</span>機能 {#code-enable-forwarding-code-span-class-version-mark-new-in-v5-0-0-span}

-   ネットワークが分離される可能性がある場合に、TiDB 内の PD クライアントと TiKV クライアントがフォロワー経由でリーダーにリクエストを転送するかどうかを制御します。
-   デフォルト値: `false`
-   環境に分離されたネットワークがある場合、このパラメータを有効にすると、サービスが利用できない期間を短縮できます。
-   分離、ネットワーク中断、またはダウンタイムが発生したかどうかを正確に判断できない場合、このメカニズムを使用すると誤判断のリスクがあり、可用性とパフォーマンスが低下します。ネットワーク障害が発生したことがない場合は、このパラメータを有効にすることはお勧めしません。

### <code>enable-table-lock</code> <span class="version-mark">v4.0.0 の新機能</span> {#code-enable-table-lock-code-span-class-version-mark-new-in-v4-0-0-span}

> **警告：**
>
> テーブル ロックは実験的機能です。本番環境での使用はお勧めしません。

-   テーブル ロック機能を有効にするかどうかを制御します。
-   デフォルト値: `false`
-   テーブル ロックは、複数のセッション間で同じテーブルへの同時アクセスを調整するために使用されます。現在、 `READ` 、 `WRITE` 、および`WRITE LOCAL`ロック タイプがサポートされています。構成項目が`false`に設定されている場合、 `LOCK TABLES`または`UNLOCK TABLES`ステートメントを実行しても有効にならず、「LOCK/UNLOCK TABLES はサポートされていません」という警告が返されます。詳細については、 [`LOCK TABLES`と`UNLOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)を参照してください。

### <code>labels</code> {#code-labels-code}

-   サーバーラベルを指定します。たとえば、 `{ zone = "us-west-1", dc = "dc1", rack = "rack1", host = "tidb1" }` 。
-   デフォルト値: `{}`

> **注記：**
>
> -   TiDB では、 `zone`ラベルは、サーバーが配置されているゾーンを指定するために特別に使用されます。 `zone` null 以外の値に設定されている場合、対応する値は[`txn-score`](/system-variables.md#txn_scope)や[`Follower read`](/follower-read.md)などの機能によって自動的に使用されます。
> -   `group`ラベルはTiDB Operatorで特別な用途があります。 [TiDB Operator](/tidb-operator-overview.md)を使用してデプロイされたクラスターの場合、 `group`ラベルを手動で指定することはお勧めし**ません**。

## ログ {#log}

ログに関するコンフィグレーション項目。

### <code>level</code> {#code-level-code}

-   ログ出力レベルを指定します。
-   `warn` `info` `fatal` : `debug` `error`
-   デフォルト値: `info`

### <code>format</code> {#code-format-code}

-   ログ出力形式を指定します。
-   値のオプション: `json`と`text` 。
-   デフォルト値: `text`

### <code>enable-timestamp</code> {#code-enable-timestamp-code}

-   ログにタイムスタンプの出力を有効にするかどうかを決定します。
-   デフォルト値: `null`
-   値を`false`に設定すると、ログはタイムスタンプを出力しません。

> **注記：**
>
> -   下位互換性を保つために、初期の`disable-timestamp`構成項目は有効なままです。ただし、 `disable-timestamp`の値が`enable-timestamp`の値と意味的に競合する場合 (たとえば、 `enable-timestamp`と`disable-timestamp`の両方が`true`に設定されている場合)、TiDB は`disable-timestamp`の値を無視します。
> -   現在、TiDB は`disable-timestamp`使用して、ログにタイムスタンプを出力するかどうかを決定します。この状況では、 `enable-timestamp`の値は`null`です。
> -   以降のバージョンでは、 `disable-timestamp`構成は削除されます。3 `disable-timestamp`破棄し、意味的に理解しやすい`enable-timestamp`を使用します。

### <code>enable-slow-log</code> {#code-enable-slow-log-code}

-   スロークエリログを有効にするかどうかを決定します。
-   デフォルト値: `true`
-   スロークエリログを有効にするには、 `enable-slow-log`を`true`に設定します。それ以外の場合は、 `false`に設定します。
-   v6.1.0 以降、スロー クエリ ログを有効にするかどうかは、TiDB 構成項目[`instance.tidb_enable_slow_log`](/tidb-configuration-file.md#tidb_enable_slow_log)またはシステム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)によって決定されます。5 `enable-slow-log`引き続き有効です。ただし、 `enable-slow-log`と`instance.tidb_enable_slow_log`同時に設定されている場合、後者が有効になります。

### <code>slow-query-file</code> {#code-slow-query-file-code}

-   スロークエリログのファイル名。
-   デフォルト値: `tidb-slow.log`
-   TiDB v2.1.8 ではスロー ログの形式が更新されたため、スロー ログはスロー ログ ファイルに別途出力されます。v2.1.8 より前のバージョンでは、この変数はデフォルトで &quot;&quot; に設定されています。
-   設定後、スロークエリログがこのファイルに別途出力されます。

### <code>slow-threshold</code> {#code-slow-threshold-code}

-   消費時間のしきい値をスローログに出力します。
-   デフォルト値: `300`
-   単位: ミリ秒
-   クエリ内の値がデフォルト値より大きい場合、それは遅いクエリであり、スロー ログに出力されます。
-   v6.1.0 以降、スロー ログの消費時間のしきい値は、TiDB 構成項目[`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold)またはシステム変数[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)で指定されます。5 `slow-threshold`引き続き有効です。ただし、 `slow-threshold`と`instance.tidb_slow_log_threshold`同時に設定されている場合、後者が有効になります。

### <code>record-plan-in-slow-log</code> {#code-record-plan-in-slow-log-code}

-   実行プランをスロー ログに記録するかどうかを決定します。
-   デフォルト値: `1`
-   v6.1.0 以降、実行プランをスロー ログに記録するかどうかは、TiDB 構成項目[`instance.tidb_record_plan_in_slow_log`](/tidb-configuration-file.md#tidb_record_plan_in_slow_log)またはシステム変数[`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log)によって決定されます。5 `record-plan-in-slow-log`引き続き有効です。ただし、 `record-plan-in-slow-log`と`instance.tidb_record_plan_in_slow_log`同時に設定されている場合、後者が有効になります。

### <code>expensive-threshold</code> {#code-expensive-threshold-code}

> **警告：**
>
> v5.4.0 以降では、 `expensive-threshold`構成項目は非推奨となり、システム変数[`tidb_expensive_query_time_threshold`](/system-variables.md#tidb_expensive_query_time_threshold)に置き換えられました。

-   `expensive`操作の行数のしきい値を出力します。
-   デフォルト値: `10000`
-   クエリ行数（統計に基づく中間結果を含む）がこの値より大きい場合は、 `expensive`操作となり、 `[EXPENSIVE_QUERY]`プレフィックスが付いたログを出力します。

### <code>general-log-file</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-general-log-file-code-span-class-version-mark-new-in-v8-0-0-span}

-   [一般ログ](/system-variables.md#tidb_general_log)のファイル名。
-   デフォルト値: `""`
-   ファイル名を指定すると、一般ログは指定されたファイルに書き込まれます。値が空白の場合、一般ログは TiDB インスタンスのサーバーログに書き込まれます。サーバーログの名前は[`filename`](#filename)使用して指定できます。

### <code>timeout</code> <span class="version-mark">v7.1.0 の新</span>機能 {#code-timeout-code-span-class-version-mark-new-in-v7-1-0-span}

-   TiDB でのログ書き込み操作のタイムアウトを設定します。ディスク障害によりログの書き込みができない場合、この構成項目により、TiDB プロセスがハングするのではなくpanicになる可能性があります。
-   デフォルト値: `0` 、タイムアウトが設定されていないことを示します。
-   単位: 秒
-   一部のユーザー シナリオでは、TiDB ログがホットプラグ可能なディスクまたはネットワーク接続ディスクに保存され、永久に使用できなくなる場合があります。このような場合、TiDB はそのような障害から自動的に回復できず、ログ書き込み操作は永久にブロックされます。TiDB プロセスは実行されているように見えますが、要求に応答しません。この構成項目は、このような状況に対処するために設計されています。

## ログファイル {#log-file}

ログ ファイルに関連するコンフィグレーション項目。

#### <code>filename</code> {#code-filename-code}

-   一般ログファイルのファイル名。
-   デフォルト値: &quot;&quot;
-   設定するとこのファイルにログが出力されます。

#### <code>max-size</code> {#code-max-size-code}

-   ログ ファイルのサイズ制限。
-   デフォルト値: 300
-   単位: MB
-   最大値は4096です。

#### <code>max-days</code> {#code-max-days-code}

-   ログが保持される最大日数。
-   デフォルト値: `0`
-   デフォルトではログは保持されます。値を設定すると、期限切れのログは`max-days`後にクリーンアップされます。

#### <code>max-backups</code> {#code-max-backups-code}

-   保持されるログの最大数。
-   デフォルト値: `0`
-   デフォルトではすべてのログファイルが保持されます。 `7`に設定すると、最大 7 つのログファイルが保持されます。

#### <code>compression</code> <span class="version-mark">v8.0.0 の新</span>機能 {#code-compression-code-span-class-version-mark-new-in-v8-0-0-span}

-   ログの圧縮方法。
-   デフォルト値: `""`
-   値`"gzip"`オプション: `""`
-   デフォルト値は`""`で、圧縮なしを意味します。gzip 圧縮を有効にするには、この値を`"gzip"`に設定します。圧縮を有効にすると、 [`slow-query-file`](#slow-query-file)や[`general-log-file`](#general-log-file-new-in-v800)など、すべてのログ ファイルが影響を受けます。

## Security {#security}

セキュリティに関するコンフィグレーション項目。

### <code>enable-sem</code> {#code-enable-sem-code}

-   Security拡張モード (SEM) を有効にします。
-   デフォルト値: `false`
-   SEM のステータスはシステム変数[`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)を介して確認できます。

### <code>ssl-ca</code> {#code-ssl-ca-code}

-   PEM 形式の信頼できる CA 証明書のファイル パス。
-   デフォルト値: &quot;&quot;
-   このオプションと`--ssl-cert` 、 `--ssl-key`同時に設定すると、クライアントが証明書を提示したときに、TiDB はこのオプションで指定された信頼された CA のリストに基づいてクライアント証明書を認証します。認証が失敗すると、接続は終了します。
-   このオプションを設定してもクライアントが証明書を提示しない場合は、クライアント証明書の認証なしで安全な接続が継続されます。

### <code>ssl-cert</code> {#code-ssl-cert-code}

-   PEM 形式の SSL 証明書のファイル パス。
-   デフォルト値: &quot;&quot;
-   このオプションと`--ssl-key`同時に設定すると、TiDB はクライアントが TLS を使用して TiDB に安全に接続することを許可します (強制はしません)。
-   指定された証明書または秘密鍵が無効な場合、TiDB は通常どおり起動しますが、安全な接続を受信できません。

### <code>ssl-key</code> {#code-ssl-key-code}

-   PEM 形式の SSL 証明書キー、つまり`--ssl-cert`で指定された証明書の秘密キーのファイル パス。
-   デフォルト値: &quot;&quot;
-   現在、TiDB はパスワードで保護された秘密鍵の読み込みをサポートしていません。

### <code>cluster-ssl-ca</code> {#code-cluster-ssl-ca-code}

-   TLS を使用して TiKV または PD を接続するために使用される CA ルート証明書。
-   デフォルト値: &quot;&quot;

### <code>cluster-ssl-cert</code> {#code-cluster-ssl-cert-code}

-   TLS を使用して TiKV または PD を接続するために使用される SSL 証明書ファイルのパス。
-   デフォルト値: &quot;&quot;

### <code>cluster-ssl-key</code> {#code-cluster-ssl-key-code}

-   TLS を使用して TiKV または PD を接続するために使用される SSL 秘密キー ファイルのパス。
-   デフォルト値: &quot;&quot;

### <code>spilled-file-encryption-method</code> {#code-spilled-file-encryption-method-code}

-   流出したファイルをディスクに保存するために使用される暗号化方法を決定します。
-   デフォルト値: `"plaintext"` 、暗号化を無効にします。
-   オプション値: `"plaintext"`と`"aes128-ctr"`

### <code>auto-tls</code> {#code-auto-tls-code}

-   起動時に TLS 証明書を自動的に生成するかどうかを決定します。
-   デフォルト値: `false`

### <code>tls-version</code> {#code-tls-version-code}

> **警告：**
>
> `"TLSv1.0"`および`"TLSv1.1"`プロトコルは TiDB v7.6.0 では非推奨となり、v8.0.0 では削除されます。

-   MySQL プロトコル接続の最小 TLS バージョンを設定します。
-   デフォルト値: &quot;&quot;。TLSv1.2 以降のバージョンを許可します。TiDB v7.6.0 より前では、デフォルト値は TLSv1.1 以降のバージョンを許可します。
-   オプションの値: `"TLSv1.2"`と`"TLSv1.3"` v8.0.0 より前では、 `"TLSv1.0"`と`"TLSv1.1"`も許可されます。

### <code>auth-token-jwks</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-auth-token-jwks-code-span-class-version-mark-new-in-v6-4-0-span}

-   [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token)の認証方法の JSON Web Key Sets (JWKS) のローカル ファイル パスを設定します。
-   デフォルト値: `""`

### <code>auth-token-refresh-interval</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-auth-token-refresh-interval-code-span-class-version-mark-new-in-v6-4-0-span}

-   [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token)認証方法の JWKS 更新間隔を設定します。
-   デフォルト値: `1h`

### <code>disconnect-on-expired-password</code> <span class="version-mark">v6.5.0 の新機能</span> {#code-disconnect-on-expired-password-code-span-class-version-mark-new-in-v6-5-0-span}

-   パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを決定します。
-   デフォルト値: `true`
-   オプション値: `true` 、 `false`
-   `true`に設定すると、パスワードの有効期限が切れたときにクライアント接続が切断されます。 `false`に設定すると、クライアント接続は「サンドボックス モード」に制限され、ユーザーはパスワード リセット操作のみを実行できます。

### <code>session-token-signing-cert</code> <span class="version-mark">v6.4.0 の新</span>機能 {#code-session-token-signing-cert-code-span-class-version-mark-new-in-v6-4-0-span}

-   セッション移行のために[Tiプロキシ](/tiproxy/tiproxy-overview.md)で使用される証明書ファイル パス。
-   デフォルト値: &quot;&quot;
-   値が空の場合、TiProxy セッションの移行は失敗します。セッションの移行を有効にするには、すべての TiDB ノードでこれを同じ証明書とキーに設定する必要があります。つまり、すべての TiDB ノードに同じ証明書とキーを保存する必要があります。

### <code>session-token-signing-key</code> <span class="version-mark">v6.4.0 の新機能</span> {#code-session-token-signing-key-code-span-class-version-mark-new-in-v6-4-0-span}

-   セッション移行のために[Tiプロキシ](/tiproxy/tiproxy-overview.md)で使用されるキー ファイル パス。
-   デフォルト値: &quot;&quot;
-   [`session-token-signing-cert`](#session-token-signing-cert-new-in-v640)の説明を参照してください。

## パフォーマンス {#performance}

パフォーマンスに関連するコンフィグレーション項目。

### <code>max-procs</code> {#code-max-procs-code}

-   TiDB で使用される CPU の数。
-   デフォルト値: `0`
-   デフォルトの`0`マシン上のすべての CPU を使用することを示します。これを n に設定することもできます。その場合、TiDB は n 個の CPU を使用します。

### <code>server-memory-quota</code> <span class="version-mark">v4.0.9 の新機能</span> {#code-server-memory-quota-code-span-class-version-mark-new-in-v4-0-9-span}

> **警告：**
>
> v6.5.0 以降、 `server-memory-quota`構成項目は非推奨となり、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)に置き換えられました。

-   tidb-server インスタンスのメモリ使用量制限。
-   デフォルト値: `0` (バイト単位)。メモリ制限がないことを意味します。

### <code>max-txn-ttl</code> {#code-max-txn-ttl-code}

-   単一のトランザクションがロックを保持できる最長時間。この時間を超えると、トランザクションのロックが他のトランザクションによってクリアされ、このトランザクションを正常にコミットできなくなる可能性があります。
-   デフォルト値: `3600000`
-   単位: ミリ秒
-   この時間より長くロックを保持するトランザクションは、コミットまたはロールバックのみ可能です。コミットは成功しない可能性があります。
-   [`&quot;bulk&quot;` DMLモード](/system-variables.md#tidb_dml_type-new-in-v800)を使用して実行されるトランザクションの場合、最大 TTL はこの構成項目の制限を超えることができます。最大値は、この構成項目と 24 時間のうち大きい方の値になります。

### <code>stmt-count-limit</code> {#code-stmt-count-limit-code}

-   単一の TiDB トランザクションで許可されるステートメントの最大数。
-   デフォルト値: `5000`
-   ステートメントの数が`stmt-count-limit`超えた後もトランザクションがロールバックまたはコミットしない場合、TiDB は`statement count 5001 exceeds the transaction limitation, autocommit = false`エラーを返します。この構成は、再試行可能な楽観的トランザクションで**のみ**有効です。悲観的トランザクションを使用する場合、またはトランザクションの再試行を無効にした場合、トランザクション内のステートメントの数は、この構成によって制限されません。

### <code>txn-entry-size-limit</code> <span class="version-mark">v5.0 の新機能</span> {#code-txn-entry-size-limit-code-span-class-version-mark-new-in-v5-0-span}

-   TiDB 内のデータの 1 行あたりのサイズ制限。
-   デフォルト値: `6291456` (バイト単位)
-   トランザクション内の単一のキー値レコードのサイズ制限。サイズ制限を超えると、TiDB は`entry too large`エラーを返します。この構成項目の最大値は`125829120` (120 MB) を超えません。
-   v7.6.0 以降では、システム変数[`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)を使用して、この構成項目の値を動的に変更できます。
-   TiKV にも同様の制限があることに注意してください。単一の書き込み要求のデータ サイズが[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) (デフォルトでは 8 MB) を超えると、TiKV はこの要求の処理を拒否します。テーブルに大きなサイズの行がある場合は、両方の構成を同時に変更する必要があります。
-   デフォルト値[`max_allowed_packet`](/system-variables.md#max_allowed_packet-new-in-v610) (MySQL プロトコルのパケットの最大サイズ) は 67108864 (64 MiB) です。行が`max_allowed_packet`より大きい場合、行は切り捨てられます。
-   [`txn-total-size-limit`](#txn-total-size-limit) (TiDB の単一トランザクションのサイズ制限) のデフォルト値は 100 MiB です。3 `txn-entry-size-limit`値を 100 MiB 以上に増やす場合は、それに応じて`txn-total-size-limit`値を増やす必要があります。

### <code>txn-total-size-limit</code> {#code-txn-total-size-limit-code}

-   TiDB における単一トランザクションのサイズ制限。
-   デフォルト値: `104857600` (バイト単位)
-   1 回のトランザクションで、キー値レコードの合計サイズはこの値を超えることはできません。このパラメータの最大値は`1099511627776` (1 TB) です。下流のコンシューマー Kafka ( `arbiter`クラスターなど) にbinlogを使用した場合、このパラメータの値は`1073741824` (1 GB) 以下にする必要があります。これは、1 GB が Kafka が処理できる単一のメッセージ サイズの上限であるためです。それ以外の場合、この制限を超えるとエラーが返されます。
-   TiDB v6.5.0 以降のバージョンでは、この構成は推奨されなくなりました。トランザクションのメモリサイズはセッションのメモリ使用量に累積され、セッションメモリしきい値を超えると[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)変数が有効になります。以前のバージョンとの互換性を保つために、以前のバージョンから TiDB v6.5.0 以降にアップグレードする場合、この構成は次のように機能します。
    -   この設定が設定されていないか、デフォルト値 ( `104857600` ) に設定されている場合、アップグレード後にトランザクションのメモリサイズがセッションのメモリ使用量に蓄積され、 `tidb_mem_quota_query`変数が有効になります。
    -   この設定がデフォルト（ `104857600` ）になっていない場合でも、設定は有効であり、単一トランザクションのサイズを制御する動作はアップグレードの前後で変更されません。つまり、トランザクションのメモリサイズは`tidb_mem_quota_query`変数によって制御されません。

### <code>tcp-keep-alive</code> {#code-tcp-keep-alive-code}

-   TCPレイヤーで`keepalive`有効にするかどうかを決定します。
-   デフォルト値: `true`

### <code>tcp-no-delay</code> {#code-tcp-no-delay-code}

-   TCPレイヤーで TCP_NODELAY を有効にするかどうかを決定します。有効にすると、TiDB は TCP/IP プロトコルの Nagle アルゴリズムを無効にし、小さなデータ パケットを送信してネットワークレイテンシーを削減します。これは、データの転送量が少なく、遅延の影響を受けやすいアプリケーションに適しています。
-   デフォルト値: `true`

### <code>cross-join</code> {#code-cross-join-code}

-   デフォルト値: `true`
-   TiDB は、デフォルトで両側のテーブルの条件なしの`JOIN`ステートメント ( `WHERE`フィールド) の実行をサポートしています。値を`false`に設定すると、サーバーはそのような`JOIN`ステートメントが出現したときに実行を拒否します。

### <code>stats-lease</code> {#code-stats-lease-code}

-   統計の再読み込み、テーブル行数の更新、自動分析を実行する必要があるかどうかの確認、フィードバックを使用した統計の更新、列の統計の読み込みの時間間隔。
-   デフォルト値: `3s`
    -   TiDB は`stats-lease`間隔で統計情報をチェックし、更新が存在する場合はそれをメモリに更新します。
    -   TiDB は、 `20 * stats-lease`時間間隔で、DML によって生成された行の合計数と変更された行の数をシステム テーブルに更新します。
    -   TiDB は`stats-lease`間隔で、自動的に分析する必要があるテーブルとインデックスをチェックします。
    -   `stats-lease`間隔で、TiDB はメモリにロードする必要がある列統計をチェックします。
    -   `200 * stats-lease`間隔で、TiDB はメモリにキャッシュされたフィードバックをシステム テーブルに書き込みます。
    -   TiDB は`5 * stats-lease`間隔でシステム テーブル内のフィードバックを読み取り、メモリにキャッシュされた統計を更新します。
-   `stats-lease` 0 に設定すると、TiDB はシステム テーブル内のフィードバックを定期的に読み取り、メモリにキャッシュされた統計を 3 秒ごとに更新します。ただし、TiDB は次の統計関連のシステム テーブルを自動的に変更しなくなります。
    -   `mysql.stats_meta` : TiDB は、トランザクションによって変更されたテーブル行の数を自動的に記録しなくなり、このシステム テーブルに更新します。
    -   `mysql.stats_histograms` / `mysql.stats_buckets`および`mysql.stats_top_n` : TiDB は統計を自動的に分析し、積極的に更新しなくなりました。
    -   `mysql.stats_feedback` : TiDB は、クエリされたデータによって返される統計の一部に従って、テーブルとインデックスの統計を更新しなくなりました。

### <code>pseudo-estimate-ratio</code> {#code-pseudo-estimate-ratio-code}

-   テーブル内の (変更された行数)/(合計行数) の比率。この値を超えると、統計の有効期限が切れたとシステムが判断し、疑似統計が使用されます。
-   デフォルト値: `0.8`
-   最小値は`0` 、最大値は`1`です。

### <code>force-priority</code> {#code-force-priority-code}

-   すべてのステートメントの優先順位を設定します。
-   デフォルト値: `NO_PRIORITY`
-   値のオプション: デフォルト値`NO_PRIORITY` 、ステートメントの優先度が強制的に変更されないことを意味します。その他のオプションは、昇順で`LOW_PRIORITY` 、 `DELAYED` 、 `HIGH_PRIORITY`です。
-   v6.1.0 以降、すべてのステートメントの優先順位は、 TiDB 構成項目[`instance.tidb_force_priority`](/tidb-configuration-file.md#tidb_force_priority)またはシステム変数[`tidb_force_priority`](/system-variables.md#tidb_force_priority)によって決定されます。 `force-priority`引き続き有効です。 ただし、 `force-priority`と`instance.tidb_force_priority`同時に設定されている場合、後者が有効になります。

> **注記：**
>
> v6.6.0 以降、TiDB は[リソース管理](/tidb-resource-control.md)サポートします。この機能を使用すると、異なるリソース グループで異なる優先度の SQL ステートメントを実行できます。これらのリソース グループに適切なクォータと優先度を構成することで、異なる優先度の SQL ステートメントのスケジュール制御を向上させることができます。リソース制御を有効にすると、ステートメントの優先度は適用されなくなります。異なる SQL ステートメントのリソース使用を管理するには、 [リソース管理](/tidb-resource-control.md)使用することをお勧めします。

### <code>distinct-agg-push-down</code> {#code-distinct-agg-push-down-code}

-   オプティマイザが、集計関数を`Distinct` ( `select count(distinct a) from t`など) でコプロセッサにプッシュダウンする操作を実行するかどうかを決定します。
-   デフォルト: `false`
-   この変数はシステム変数[`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)の初期値です。

### <code>enforce-mpp</code> {#code-enforce-mpp-code}

-   オプティマイザのコスト見積もりを無視し、クエリ実行に TiFlash の MPP モードを強制的に使用するかどうかを決定します。
-   デフォルト値: `false`
-   この設定項目は、初期値[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)を制御します。たとえば、この設定項目が`true`に設定されている場合、デフォルト値`tidb_enforce_mpp`は`ON`になります。

### <code>enable-stats-cache-mem-quota</code> <span class="version-mark">v6.1.0 の新機能</span> {#code-enable-stats-cache-mem-quota-code-span-class-version-mark-new-in-v6-1-0-span}

-   統計キャッシュのメモリクォータを有効にするかどうかを制御します。
-   デフォルト値: `true`

### <code>stats-load-concurrency</code> <span class="version-mark">v5.4.0 の新</span>機能 {#code-stats-load-concurrency-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiDB 同期ロード統計機能が同時に処理できる列の最大数。
-   デフォルト値: `5`
-   現在、有効な値の範囲は`[1, 128]`です。

### <code>stats-load-queue-size</code> <span class="version-mark">v5.4.0 の新機能</span> {#code-stats-load-queue-size-code-span-class-version-mark-new-in-v5-4-0-span}

-   TiDB 同期ロード統計機能がキャッシュできる列要求の最大数。
-   デフォルト値: `1000`
-   現在、有効な値の範囲は`[1, 100000]`です。

### <code>concurrently-init-stats</code> <span class="version-mark">v8.1.0 および v7.5.2 の新</span>機能 {#code-concurrently-init-stats-code-span-class-version-mark-new-in-v8-1-0-and-v7-5-2-span}

-   TiDB の起動時に統計を同時に初期化するかどうかを制御します。
-   デフォルト値: `false`

### <code>lite-init-stats</code> <span class="version-mark">v7.1.0 の新</span>機能 {#code-lite-init-stats-code-span-class-version-mark-new-in-v7-1-0-span}

-   TiDB の起動時に軽量統計初期化を使用するかどうかを制御します。
-   デフォルト値: v7.2.0 より前のバージョンの場合は`false` 、v7.2.0 以降のバージョンの場合は`true` 。
-   `lite-init-stats`の値が`true`の場合、統計の初期化では、インデックスまたは列のヒストグラム、TopN、または Count-Min Sketch はメモリにロードされません。 `lite-init-stats`の値が`false`の場合、統計の初期化では、インデックスと主キーのヒストグラム、TopN、および Count-Min Sketch はメモリにロードされますが、主キー以外の列のヒストグラム、TopN、または Count-Min Sketch はメモリにロードされません。 オプティマイザーが特定のインデックスまたは列のヒストグラム、TopN、および Count-Min Sketch を必要とする場合、必要な統計は同期的または非同期的にメモリにロードされます ( [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)で制御)。
-   `lite-init-stats`から`true`に設定すると、統計の初期化が高速化され、不要な統計のロードが回避されるため、TiDB のメモリ使用量が削減されます。詳細については、 [負荷統計](/statistics.md#load-statistics)を参照してください。

### <code>force-init-stats</code> <span class="version-mark">v6.5.7 および v7.1.0 の新</span>機能 {#code-force-init-stats-code-span-class-version-mark-new-in-v6-5-7-and-v7-1-0-span}

-   TiDB の起動中にサービスを提供する前に、統計の初期化が完了するまで待機するかどうかを制御します。
-   デフォルト値: v7.2.0 より前のバージョンの場合は`false` 、v7.2.0 以降のバージョンの場合は`true` 。
-   `force-init-stats`の値が`true`の場合、TiDB は起動時にサービスを提供する前に、統計の初期化が完了するまで待機する必要があります。テーブルとパーティションの数が多く、 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)の値が`false`場合、 `force-init-stats`から`true`に設定すると、TiDB がサービスの提供を開始するまでの時間が長くなる可能性があることに注意してください。
-   `force-init-stats`の値が`false`の場合、統計の初期化が完了する前に TiDB はサービスを提供できますが、オプティマイザーは疑似統計を使用して決定を下すため、最適でない実行プランが生成される場合があります。

## オープントレーシング {#opentracing}

opentracing に関連するコンフィグレーション項目。

### <code>enable</code> {#code-enable-code}

-   一部の TiDB コンポーネントの呼び出しオーバーヘッドをトレースするために、OpenTracing を有効にします。OpenTracing を有効にすると、パフォーマンスが低下することに注意してください。
-   デフォルト値: `false`

### <code>rpc-metrics</code> {#code-rpc-metrics-code}

-   RPC メトリックを有効にします。
-   デフォルト値: `false`

## opentracing.サンプラー {#opentracing-sampler}

opentracing.sampler に関連するコンフィグレーション項目。

### <code>type</code> {#code-type-code}

-   OpenTracing サンプラーのタイプを指定します。文字列値は大文字と小文字を区別しません。
-   デフォルト値: `"const"`
-   `"remote"` `"probabilistic"` `"ratelimiting"` : `"const"`

### <code>param</code> {#code-param-code}

-   OpenTracing サンプラーのパラメータ。
    -   `const`タイプの場合、値は`0`または`1`になり、 `const`サンプラーを有効にするかどうかを示します。
    -   `probabilistic`タイプの場合、パラメータはサンプリング確率を指定します。これは`0`から`1`までの浮動小数点数値になります。
    -   `ratelimiting`タイプの場合、パラメータは 1 秒あたりにサンプリングされるスパンの数を指定します。
    -   `remote`タイプの場合、パラメータはサンプリング確率を指定します。これは`0`から`1`までの浮動小数点数値になります。
-   デフォルト値: `1.0`

### <code>sampling-server-url</code> {#code-sampling-server-url-code}

-   jaeger-agent サンプリングサーバーの HTTP URL。
-   デフォルト値: `""`

### <code>max-operations</code> {#code-max-operations-code}

-   サンプラーがトレースできる操作の最大数。操作がトレースされない場合、デフォルトの確率サンプラーが使用されます。
-   デフォルト値: `0`

### <code>sampling-refresh-interval</code> {#code-sampling-refresh-interval-code}

-   jaeger-agent サンプリング ポリシーのポーリング頻度を制御します。
-   デフォルト値: `0`

## オープントレーシングレポーター {#opentracing-reporter}

opentracing.reporter に関連するコンフィグレーション項目。

### <code>queue-size</code> {#code-queue-size-code}

-   レポーターがメモリ内のスパンを記録するキューのサイズ。
-   デフォルト値: `0`

### <code>buffer-flush-interval</code> {#code-buffer-flush-interval-code}

-   レポーターがメモリ内のスパンをstorageにフラッシュする間隔。
-   デフォルト値: `0`

### <code>log-spans</code> {#code-log-spans-code}

-   送信されたすべてのスパンのログを印刷するかどうかを決定します。
-   デフォルト値: `false`

### <code>local-agent-host-port</code> {#code-local-agent-host-port-code}

-   レポーターが jaeger エージェントにスパンを送信するアドレス。
-   デフォルト値: `""`

## tikv クライアント {#tikv-client}

### <code>grpc-connection-count</code> {#code-grpc-connection-count-code}

-   各 TiKV で確立される接続の最大数。
-   デフォルト値: `4`

### <code>grpc-keepalive-time</code> {#code-grpc-keepalive-time-code}

-   TiDB ノードと TiKV ノード間の RPC 接続の`keepalive`時間間隔。指定された時間間隔内にネットワーク パケットがない場合、gRPC クライアントは TiKV に対して`ping`コマンドを実行して、TiKV が稼働しているかどうかを確認します。
-   デフォルト: `10`
-   単位: 秒

### <code>grpc-keepalive-timeout</code> {#code-grpc-keepalive-timeout-code}

-   TiDB ノードと TiKV ノード間の RPC `keepalive`チェックのタイムアウト。
-   デフォルト値: `3`
-   単位: 秒

### <code>grpc-compression-type</code> {#code-grpc-compression-type-code}

-   TiDB ノードと TiKV ノード間のデータ転送に使用する圧縮タイプを指定します。デフォルト値は`"none"`で、圧縮なしを意味します。gzip 圧縮を有効にするには、この値を`"gzip"`に設定します。
-   デフォルト値: `"none"`
-   値`"gzip"`オプション: `"none"`

### <code>commit-timeout</code> {#code-commit-timeout-code}

-   トランザクションコミットを実行する際の最大タイムアウト。
-   デフォルト値: `41s`
-   この値は、 Raft選択タイムアウトの 2 倍より大きく設定する必要があります。

### <code>max-batch-size</code> {#code-max-batch-size-code}

-   バッチで送信される RPC パケットの最大数。値が`0`ない場合、 `BatchCommands` API を使用して TiKV にリクエストが送信され、同時実行性が高い場合に RPCレイテンシーが短縮される可能性があります。この値を変更しないことをお勧めします。
-   デフォルト値: `128`

### <code>max-batch-wait-time</code> {#code-max-batch-wait-time-code}

-   `max-batch-wait-time`を待機して、データ パケットをバッチで大きなパケットにカプセル化し、TiKV ノードに送信します。 `tikv-client.max-batch-size`の値が`0`より大きい場合にのみ有効です。この値を変更しないことをお勧めします。
-   デフォルト値: `0`
-   単位: ナノ秒

### <code>batch-wait-size</code> {#code-batch-wait-size-code}

-   バッチで TiKV に送信されるパケットの最大数。この値を変更しないことをお勧めします。
-   デフォルト値: `8`
-   値が`0`の場合、この機能は無効になります。

### <code>overload-threshold</code> {#code-overload-threshold-code}

-   TiKV 負荷のしきい値。TiKV 負荷がこのしきい値を超えると、TiKV の負荷を軽減するために`0`さらに`batch`パケットが収集されます。3 の値が`tikv-client.max-batch-size`より大きい場合にのみ有効です。この値を変更しないことをお勧めします。
-   デフォルト値: `200`

### <code>copr-req-timeout</code> <span class="version-mark">v7.5.0 の新</span>機能 {#code-copr-req-timeout-code-span-class-version-mark-new-in-v7-5-0-span}

> **警告：**
>
> この構成パラメータは将来のバージョンでは廃止される可能性があります。値を変更**しないでください**。

-   単一のコプロセッサー要求のタイムアウト。
-   デフォルト値: `60`
-   単位: 秒

### <code>enable-replica-selector-v2</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-enable-replica-selector-v2-code-span-class-version-mark-new-in-v8-0-0-span}

> **警告：**
>
> この構成パラメータは将来のバージョンでは廃止される可能性があります。値を変更**しないでください**。

-   RPC リクエストを TiKV に送信するときに、リージョンレプリカ セレクターの新しいバージョンを使用するかどうか。
-   デフォルト値: `true`

## tikv-client.copr-cache <span class="version-mark">v4.0.0 の新</span>機能 {#tikv-client-copr-cache-span-class-version-mark-new-in-v4-0-0-span}

このセクションでは、コプロセッサーキャッシュ機能に関連する構成項目について説明します。

### <code>capacity-mb</code> {#code-capacity-mb-code}

-   キャッシュされたデータの合計サイズ。キャッシュ スペースがいっぱいになると、古いキャッシュ エントリが削除されます。値が`0.0`の場合、コプロセッサーキャッシュ機能は無効になります。
-   デフォルト値: `1000.0`
-   単位: MB
-   タイプ: フロート

## txn ローカル ラッチ {#txn-local-latches}

トランザクション ラッチに関連するコンフィグレーション項目。これらの構成項目は将来廃止される可能性があります。使用することはお勧めしません。

### <code>enabled</code> {#code-enabled-code}

-   トランザクションのメモリロックを有効にするかどうかを決定します。
-   デフォルト値: `false`

### <code>capacity</code> {#code-capacity-code}

-   ハッシュに対応するスロットの数は、2 の指数倍数に自動的に調整されます。各スロットは 32 バイトのメモリを占有します。設定が小さすぎると、データの書き込みが比較的広い範囲をカバーするシナリオ (データのインポートなど) で実行速度が低下し、パフォーマンスが低下する可能性があります。
-   デフォルト値: `2048000`

## binlog {#binlog}

TiDB Binlogに関連する構成。

### <code>enable</code> {#code-enable-code}

-   binlog を有効または無効にします。
-   デフォルト値: `false`

### <code>write-timeout</code> {#code-write-timeout-code}

-   Pumpにbinlogを書き込むタイムアウト。この値を変更することはお勧めしません。
-   デフォルト: `15s`
-   単位: 秒

### <code>ignore-error</code> {#code-ignore-error-code}

-   binlogをPumpに書き込むプロセスで発生したエラーを無視するかどうかを決定します。この値を変更することはお勧めしません。
-   デフォルト値: `false`
-   値が`true`に設定され、エラーが発生すると、TiDB はbinlog の書き込みを停止し、監視項目`tidb_server_critical_error_total`のカウントに`1`を追加します。値が`false`に設定されている場合、 binlog の書き込みは失敗し、TiDB サービス全体が停止します。

### <code>binlog-socket</code> {#code-binlog-socket-code}

-   binlogがエクスポートされるネットワーク アドレス。
-   デフォルト値: &quot;&quot;

### <code>strategy</code> {#code-strategy-code}

-   binlogをエクスポートする際のPump選択の戦略。現在は、 `hash`と`range`方法のみがサポートされています。
-   デフォルト値: `range`

## 状態 {#status}

TiDB サービスのステータスに関連するコンフィグレーション。

### <code>report-status</code> {#code-report-status-code}

-   HTTP API サービスを有効または無効にします。
-   デフォルト値: `true`

### <code>record-db-qps</code> {#code-record-db-qps-code}

-   データベース関連の QPS メトリックを Prometheus に送信するかどうかを決定します。
-   デフォルト値: `false`

### <code>record-db-label</code> {#code-record-db-label-code}

-   データベース関連の QPS メトリックを Prometheus に送信するかどうかを決定します。
-   期間やステートメントなど、 `record-db-qps`より多くのメトリック タイプをサポートします。
-   デフォルト値: `false`

## pessimistic-txn {#pessimistic-txn}

悲観的トランザクションの使用については、 [TiDB 悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。

### max-retry-count {#max-retry-count}

-   悲観的トランザクションにおける各ステートメントの最大再試行回数。再試行回数がこの制限を超えると、エラーが発生します。
-   デフォルト値: `256`

### deadlock-history-capacity {#deadlock-history-capacity}

-   単一の TiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)のテーブルに記録できるデッドロック イベントの最大数。このテーブルがいっぱいのときに追加のデッドロック イベントが発生すると、テーブル内の最も古いレコードが削除され、最新のエラーのための場所が確保されます。
-   デフォルト値: `10`
-   最小値: `0`
-   最大値: `10000`

### deadlock-history-collect-retryable {#deadlock-history-collect-retryable}

-   [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロック エラーの情報を収集するかどうかを制御します。再試行可能なデッドロック エラーの説明については、 [再試行可能なデッドロック エラー](/information-schema/information-schema-deadlocks.md#retryable-deadlock-errors)を参照してください。
-   デフォルト値: `false`

### pessimistic-auto-commit<span class="version-mark">v6.0.0 の新</span>機能 {#pessimistic-auto-commit-span-class-version-mark-new-in-v6-0-0-span}

-   ペシ悲観的トランザクション モードがグローバルに有効になっている場合 ( `tidb_txn_mode='pessimistic'` ) に、自動コミット トランザクションが使用するトランザクション モードを決定します。デフォルトでは、悲観的トランザクション モードがグローバルに有効になっている場合でも、自動コミット トランザクションは楽観的トランザクション モードを使用します。 `pessimistic-auto-commit`を有効にすると ( `true`に設定)、自動コミット トランザクションも悲観的モードを使用します。これは、他の明示的にコミットされた悲観的トランザクションと一致します。
-   競合が発生するシナリオでは、この構成を有効にすると、TiDB は自動コミット トランザクションをグローバル ロック待機管理に組み込み、デッドロックを回避し、デッドロックの原因となる競合によって生じるレイテンシーの急増を軽減します。
-   競合のないシナリオでは、自動コミット トランザクションが多数あり (具体的な数は実際のシナリオによって決まります。たとえば、自動コミット トランザクションの数がアプリケーションの総数の半分以上を占める場合など)、単一のトランザクションで大量のデータを操作する場合は、この構成を有効にするとパフォーマンスが低下します。たとえば、auto-commit `INSERT INTO SELECT`ステートメントなどです。
-   セッション レベルのシステム変数[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800)が`"bulk"`に設定されている場合、セッションでのこの構成の効果は、 `false`に設定するのと同等になります。
-   デフォルト値: `false`

### constraint-check-in-place-pessimistic<span class="version-mark">v6.4.0 の新機能</span> {#constraint-check-in-place-pessimistic-span-class-version-mark-new-in-v6-4-0-span}

-   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)のデフォルト値を制御します。
-   デフォルト値: `true`

## 分離読み取り {#isolation-read}

読み取り分離に関連するコンフィグレーション項目。

### <code>engines</code> {#code-engines-code}

-   TiDB がどのエンジンからデータを読み取ることを許可するかを制御します。
-   デフォルト値: [&quot;tikv&quot;, &quot;tiflash&quot;, &quot;tidb&quot;]。エンジンがオプティマイザーによって自動的に選択されることを示します。
-   値のオプション: 「tikv」、「tiflash」、「tidb」の任意の組み合わせ。たとえば、[&quot;tikv&quot;, &quot;tidb&quot;] または [&quot;tiflash&quot;, &quot;tidb&quot;]

## 実例 {#instance}

### <code>tidb_enable_collect_execution_info</code> {#code-tidb-enable-collect-execution-info-code}

-   この構成は、スロークエリログに各演算子の実行情報を記録するかどうか、および[インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)を記録するかどうかを制御します。
-   デフォルト値: `true`
-   v6.1.0 より前では、この構成は`enable-collect-execution-info`で設定されます。

### <code>tidb_enable_slow_log</code> {#code-tidb-enable-slow-log-code}

-   この構成は、スロー ログ機能を有効にするかどうかを制御するために使用されます。
-   デフォルト値: `true`
-   値のオプション: `true`または`false`
-   v6.1.0 より前では、この構成は`enable-slow-log`で設定されます。

### <code>tidb_slow_log_threshold</code> {#code-tidb-slow-log-threshold-code}

-   この設定は、スロー ログに消費される時間のしきい値を出力するために使用されます。クエリの消費時間がこの値より大きい場合、このクエリはスロー ログとみなされ、そのログがスロー クエリ ログに出力されます。
-   デフォルト値: `300`
-   範囲: `[-1, 9223372036854775807]`
-   単位: ミリ秒
-   v6.1.0 より前では、この構成は`slow-threshold`で設定されます。

### <code>in-mem-slow-query-topn-num</code> <span class="version-mark">v7.3.0 の新機能</span> {#code-in-mem-slow-query-topn-num-code-span-class-version-mark-new-in-v7-3-0-span}

-   構成により、メモリにキャッシュされる最も遅いクエリの数を制御します。
-   デフォルト値: 30

### <code>in-mem-slow-query-recent-num</code> <span class="version-mark">v7.3.0 の新機能</span> {#code-in-mem-slow-query-recent-num-code-span-class-version-mark-new-in-v7-3-0-span}

-   この構成では、メモリにキャッシュされる最近使用された低速クエリの数を制御します。
-   デフォルト値: 500

### <code>tidb_expensive_query_time_threshold</code> {#code-tidb-expensive-query-time-threshold-code}

-   この構成は、コストの高いクエリ ログを出力するかどうかを決定するしきい値を設定するために使用されます。コストの高いクエリ ログと低速なクエリ ログの違いは次のとおりです。
    -   ステートメントの実行後にスロー ログが出力されます。
    -   コストのかかるクエリ ログには、実行時間がしきい値を超えている実行中のステートメントとその関連情報が出力されます。
-   デフォルト値: `60`
-   範囲: `[10, 2147483647]`
-   単位: 秒
-   v5.4.0 より前では、この構成は`expensive-threshold`で設定されます。

### <code>tidb_record_plan_in_slow_log</code> {#code-tidb-record-plan-in-slow-log-code}

-   この構成は、スロー ログにスロー クエリの実行プランを含めるかどうかを制御するために使用されます。
-   デフォルト値: `1`
-   値のオプション: `1` (有効、デフォルト) または`0` (無効)。
-   この設定の値はシステム変数[`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log)の値を初期化します
-   v6.1.0 より前では、この構成は`record-plan-in-slow-log`で設定されます。

### <code>tidb_force_priority</code> {#code-tidb-force-priority-code}

-   この構成は、TiDBサーバー上で実行されるステートメントのデフォルトの優先順位を変更するために使用されます。
-   デフォルト値: `NO_PRIORITY`
-   デフォルト値`NO_PRIORITY` 、ステートメントの優先度が強制的に変更されないことを意味します。その他のオプションは、昇順で`LOW_PRIORITY` 、 `DELAYED` 、 `HIGH_PRIORITY`です。
-   v6.1.0 より前では、この構成は`force-priority`で設定されます。

> **注記：**
>
> v6.6.0 以降、TiDB は[リソース管理](/tidb-resource-control.md)サポートします。この機能を使用すると、異なるリソース グループで異なる優先度の SQL ステートメントを実行できます。これらのリソース グループに適切なクォータと優先度を構成することで、異なる優先度の SQL ステートメントのスケジュール制御を向上させることができます。リソース制御を有効にすると、ステートメントの優先度は適用されなくなります。異なる SQL ステートメントのリソース使用を管理するには、 [リソース管理](/tidb-resource-control.md)使用することをお勧めします。

### <code>max_connections</code> {#code-max-connections-code}

-   単一の TiDB インスタンスに許可される最大接続数。リソース制御に使用できます。
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   デフォルト値`0`制限がないことを意味します。この変数の値が`0`より大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新しい接続を拒否します。
-   この設定の値はシステム変数[`max_connections`](/system-variables.md#max_connections)の値を初期化します
-   v6.2.0 より前では、この構成は`max-server-connections`で設定されます。

### <code>tidb_enable_ddl</code> {#code-tidb-enable-ddl-code}

-   この構成は、対応する TiDB インスタンスが DDL 所有者になれるかどうかを制御します。
-   デフォルト値: `true`
-   可能`ON`値: `OFF`
-   この設定の値はシステム変数[`tidb_enable_ddl`](/system-variables.md#tidb_enable_ddl-new-in-v630)の値を初期化します。
-   v6.3.0 より前では、この構成は`run-ddl`で設定されます。

### <code>tidb_stmt_summary_enable_persistent</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-tidb-stmt-summary-enable-persistent-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   ステートメント サマリーの永続性を有効にするかどうかを制御します。
-   デフォルト値: `false`
-   詳細については[永続ステートメントの概要](/statement-summary-tables.md#persist-statements-summary)参照してください。

### <code>tidb_stmt_summary_filename</code> <span class="version-mark">v6.6.0 の新</span>機能 {#code-tidb-stmt-summary-filename-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   ステートメント サマリーの永続性が有効になっている場合、この構成では永続データが書き込まれるファイルを指定します。
-   デフォルト値: `tidb-statements.log`

### <code>tidb_stmt_summary_file_max_days</code> <span class="version-mark">v6.6.0 の新</span>機能 {#code-tidb-stmt-summary-file-max-days-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   ステートメント サマリーの永続性が有効になっている場合、この構成では永続データ ファイルを保持する最大日数を指定します。
-   デフォルト値: `3`
-   単位: 日
-   データ保持要件とディスク領域の使用量に基づいて値を調整できます。

### <code>tidb_stmt_summary_file_max_size</code> <span class="version-mark">v6.6.0 の新</span>機能 {#code-tidb-stmt-summary-file-max-size-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   ステートメント サマリーの永続性が有効になっている場合、この構成は永続データ ファイルの最大サイズを指定します。
-   デフォルト値: `64`
-   単位: MiB
-   データ保持要件とディスク領域の使用量に基づいて値を調整できます。

### <code>tidb_stmt_summary_file_max_backups</code> <span class="version-mark">v6.6.0 の新機能</span> {#code-tidb-stmt-summary-file-max-backups-code-span-class-version-mark-new-in-v6-6-0-span}

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   ステートメント サマリーの永続化が有効になっている場合、この構成では永続化できるデータ ファイルの最大数を指定します。1 `0`ファイル数に制限がないことを意味します。
-   デフォルト値: `0`
-   データ保持要件とディスク領域の使用量に基づいて値を調整できます。

## プロキシプロトコル {#proxy-protocol}

PROXY プロトコルに関連するコンフィグレーション項目。

### <code>networks</code> {#code-networks-code}

-   [PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を使用してTiDBに接続できるプロキシサーバーのIPアドレスのリスト
-   デフォルト値: &quot;&quot;
-   通常、リバース プロキシの背後で TiDB にアクセスすると、TiDB はリバース プロキシサーバーの IP アドレスをクライアントの IP アドレスとして取得します。PROXY プロトコルを有効にすると、このプロトコルをサポートする HAProxy などのリバース プロキシは、実際のクライアント IP アドレスを TiDB に渡すことができます。
-   このパラメータを設定すると、TiDB は設定されたソース IP アドレスが PROXY プロトコルを使用して TiDB に接続できるようにします。PROXY 以外のプロトコルが使用されている場合、この接続は拒否されます。このパラメータを空のままにすると、どの IP アドレスも PROXY プロトコルを使用して TiDB に接続できません。値には、 `,`を区切り文字として IP アドレス (192.168.1.50) または CIDR (192.168.1.0/24) を指定できます。3 `*`任意の IP アドレスを意味します。

> **警告：**
>
> `*` 、任意の IP アドレスのクライアントがその IP アドレスを報告できるようにすることでセキュリティ リスクを招く可能性があるため、注意して使用してください。また、 `*`を使用すると、TiDB に直接接続する内部コンポーネント(TiDB ダッシュボードなど) が使用できなくなる可能性もあります。

### <code>fallbackable</code> <span class="version-mark">v6.5.1 の新</span>機能 {#code-fallbackable-code-span-class-version-mark-new-in-v6-5-1-span}

-   PROXY プロトコル フォールバック モードを有効にするかどうかを制御します。この構成項目が`true`に設定されている場合、TiDB は PROXY プロトコル仕様を使用せずに、または PROXY プロトコル ヘッダーを送信せずに、 `proxy-protocol.networks`に属するクライアントが TiDB に接続するのを受け入れることができます。デフォルトでは、TiDB は`proxy-protocol.networks`に属し、PROXY プロトコル ヘッダーを送信するクライアント接続のみを受け入れます。
-   デフォルト値: `false`

## 実験的 {#experimental}

v3.1.0 で導入されたセクション`experimental`では、TiDB の実験的機能に関連する構成について説明します。

### <code>allow-expression-index</code> <span class="version-mark">v4.0.0 の新</span>機能 {#code-allow-expression-index-code-span-class-version-mark-new-in-v4-0-0-span}

-   式インデックスを作成できるかどうかを制御します。TiDB v5.2.0 以降、式内の関数が安全な場合は、この構成を有効にしなくても、この関数に基づいて直接式インデックスを作成できます。他の関数に基づいて式インデックスを作成する場合は、この構成を有効`tidb_allow_function_for_expression_index`することができますが、正確性の問題が発生する可能性があります。1 変数をクエリすると、式の作成に直接使用しても安全な関数を取得できます。
-   デフォルト値: `false`
