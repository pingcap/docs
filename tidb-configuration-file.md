---
title: TiDB Configuration File
summary: コマンドラインオプションに関係しない、TiDB設定ファイルオプションについて学びましょう。
---

<!-- markdownlint-disable MD001 -->

<!-- markdownlint-disable MD024 -->

# TiDBコンフィグレーションファイル {#tidb-configuration-file}

TiDB 構成ファイルは、コマンドライン パラメーターよりも多くのオプションをサポートしています。デフォルトの構成ファイル[`config.toml.example`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/config/config.toml.example)をダウンロードし、その名前を`config.toml`に変更できます。本書では[コマンドラインオプション](/command-line-flags-for-tidb-configuration.md)に関係のないオプションのみを説明します。

> **Tip:**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### `split-table` {#split-table}

-   各テーブルごとに個別のリージョンを作成するかどうかを決定します。
-   デフォルト値: `true`
-   多数のテーブル（例えば、10万個以上のテーブル）を作成する必要がある場合は`false`に設定することをお勧めします。

### `tidb-max-reuse-chunk` <span class="version-mark">v6.4.0の新機能</span> {#tidb-max-reuse-chunk-new-in-v640}

-   チャンク割り当てにおけるキャッシュ可能なチャンクオブジェクトの最大数を制御します。この設定項目に大きすぎる値を設定すると、メモリ不足（OOM）のリスクが高まる可能性があります。
-   デフォルト値: `64`
-   最小値: `0`
-   最大値: `2147483647`

### `tidb-max-reuse-column` <span class="version-mark">v6.4.0で追加</span> {#tidb-max-reuse-column-new-in-v640}

-   チャンク割り当てにおけるキャッシュ可能な列オブジェクトの最大数を制御します。この設定項目に大きすぎる値を設定すると、メモリ不足（OOM）のリスクが高まる可能性があります。
-   デフォルト値: `256`
-   最小値: `0`
-   最大値: `2147483647`

### `token-limit` {#token-limit}

-   同時にリクエストを実行できるセッションの数。
-   型: Integer
-   デフォルト値: `1000`
-   最小値: `1`
-   最大値: `1048576`

### `temp-dir` <span class="version-mark">v6.3.0 で追加されました。</span> {#temp-dir-new-in-v630}

-   TiDBが一時データを保存するために使用されるファイルシステム上の場所。機能がTiDBノード内でローカルストレージを必要とする場合、TiDBはこの場所に対応する一時データを保存します。
-   インデックスを作成する際に、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)有効になっている場合、新しく作成されたインデックスのバックフィルが必要なデータは、まず TiDB のローカル一時ディレクトリに保存され、その後バッチ処理で TiKV にインポートされるため、インデックス作成が高速化されます。
-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)使用してデータをインポートする場合、ソートされたデータはまず TiDB のローカル一時ディレクトリに保存され、その後バッチ処理で TiKV にインポートされます。
-   デフォルト値: `"/tmp/tidb"`

> **Note:**
>
> ディレクトリが存在しない場合、TiDB は起動時に自動的に作成します。ディレクトリの作成に失敗した場合、または TiDB にそのディレクトリへの読み取り/書き込み権限がない場合、 [`Fast Online DDL`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)予期しない問題が発生する可能性があります。

### `oom-use-tmp-storage` {#oom-use-tmp-storage}

> **Warning:**
>
> バージョン 6.3.0 以降、この設定項目は非推奨となり、システム変数[`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom)に置き換えられました。TiDB クラスタをバージョン 6.3.0 以降にアップグレードすると、この変数は`oom-use-tmp-storage`の値で自動的に初期化されます。その後、 `oom-use-tmp-storage`の値を変更しても効果は**ありません**。

-   単一の SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部のオペレーターに対して一時ストレージを有効にするかどうかを制御します。
-   デフォルト値: `true`

### `tmp-storage-path` {#tmp-storage-path}

-   単一の SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部のオペレーターの一時的なストレージパスを指定します。
-   デフォルト値: `<temporary directory of OS>/<OS user ID>_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage` 。 `MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=`は`Base64`の`<host>:<port>/<statusHost>:<statusPort>`エンコード結果です。
-   この設定は、システム変数[`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom)が`ON`の場合にのみ有効になります。

### `tmp-storage-quota` {#tmp-storage-quota}

-   `tmp-storage-path`のストレージのクォータを指定します。単位はバイトです。
-   単一の SQL ステートメントが一時ディスクを使用し、TiDBサーバーの一時ディスクの合計ボリュームがこの構成値を超えると、現在の SQL 操作はキャンセルされ、 `Out of Global Storage Quota!`エラーが返されます。
-   この設定の値が`0`より小さい場合、上記のチェックと制限は適用されません。
-   デフォルト値: `-1`
-   `tmp-storage-path`の残りの使用可能なストレージが`tmp-storage-quota`で定義された値よりも少ない場合、TiDBサーバーは起動時にエラーを報告して終了します。

### `lease` {#lease}

-   DDLリース契約のタイムアウト。
-   デフォルト値: `45s`
-   単位：秒

### `compatible-kill-query` {#compatible-kill-query}

-   `KILL`ステートメントを MySQL 互換に設定するかどうかを決定します。
-   デフォルト値: `false`
-   `compatible-kill-query` 、 [`enable-global-kill`](#enable-global-kill-new-in-v610) `false`に設定されている場合にのみ有効になります。
-   [`enable-global-kill`](#enable-global-kill-new-in-v610)が`false`の場合、 `compatible-kill-query`クエリを強制終了する際に`TIDB`キーワードを追加する必要があるかどうかを制御します。
    -   `compatible-kill-query`が`false`の場合、TiDB での`KILL xxx`の動作は MySQL とは異なります。TiDB でクエリを強制終了するには、 `TIDB`のように`KILL TIDB xxx`キーワードを追加する必要があります。
    -   `compatible-kill-query`が`true`の場合、TiDB でクエリを強制終了するには、 `TIDB`キーワードを追加する必要はありません。クライアントが**常に同じ TiDB インスタンスに接続されることが確実でない限り**、構成ファイルで`compatible-kill-query`を`true`に設定することは強くお勧めしません。これは、デフォルトの MySQL クライアントで<kbd>Control</kbd> + <kbd>C</kbd>を押すと`KILL`が実行される新しい接続が開かれるためです。クライアントと TiDB クラスタの間にプロキシがある場合、新しい接続は別の TiDB インスタンスにルーティングされる可能性があり、誤って別のセッションが強制終了される可能性があります。
-   [`enable-global-kill`](#enable-global-kill-new-in-v610)が`true`の場合、 `KILL xxx`と`KILL TIDB xxx`は同じ効果を持ちます。
-   `KILL`ステートメントの詳細については、[キル [TIDB]](/sql-statements/sql-statement-kill.md)参照してください。

### `check-mb4-value-in-utf8` {#check-mb4-value-in-utf8}

-   `utf8mb4`文字チェックを有効にするかどうかを決定します。この機能が有効になっている場合、文字セットが`utf8`で、 `mb4`に`utf8`文字が挿入されると、エラーが返されます。
-   デフォルト値: `false`
-   バージョン6.1.0以降、 `utf8mb4`文字チェックを有効にするかどうかは、TiDB構成項目`instance.tidb_check_mb4_value_in_utf8`またはシステム変数`tidb_check_mb4_value_in_utf8`によって決定されます。 `check-mb4-value-in-utf8`引き続き有効です。ただし、 `check-mb4-value-in-utf8`と`instance.tidb_check_mb4_value_in_utf8`の両方が設定されている場合は、後者が有効になります。

### `treat-old-version-utf8-as-utf8mb4` {#treat-old-version-utf8-as-utf8mb4}

-   古いテーブルの`utf8`文字セットを`utf8mb4`として扱うかどうかを決定します。
-   デフォルト値: `true`

### `alter-primary-key`(非推奨) {#alter-primary-key-deprecated}

-   列に主キー制約を追加するか削除するかを決定します。
-   デフォルト値: `false`
-   このデフォルト設定では、主キー制約の追加または削除はサポートされていません。 `alter-primary-key`を`true`に設定することで、この機能を有効にできます。ただし、スイッチをオンにする前にテーブルが既に存在し、その主キー列のデータ型が整数である場合、この構成項目を`true`に設定しても、列から主キーを削除することはできません。

> **Note:**
>
> この設定項目は非推奨となり、現在では`@tidb_enable_clustered_index`の値が`INT_ONLY`の場合にのみ有効になります。主キーを追加または削除する必要がある場合は、テーブル作成時に代わりに`NONCLUSTERED`キーワードを使用してください。 `CLUSTERED`型の主キーの詳細については、[クラスター化インデックス](/clustered-indexes.md)参照してください。

### `server-version` {#server-version}

-   以下の状況において、TiDBが返すバージョン文字列を変更します。
    -   組み込み関数`VERSION()`を使用する場合。
    -   TiDB がクライアントへの最初の接続を確立し、サーバーのバージョン文字列を含む最初のハンドシェイク パケットを返すとき。詳細については、 [MySQL 初期ハンドシェイクパケット](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_connection_phase.html#sect_protocol_connection_phase_initial_handshake)を参照してください。
-   デフォルト値: &quot;&quot;
-   デフォルトでは、TiDB バージョン文字列の形式は`8.0.11-TiDB-${tidb_version}`です。

> **Note:**
>
> TiDBノードは`server-version`の値を使用して現在のTiDBバージョンを確認します。そのため、予期しない動作を避けるため、TiDBクラスタをアップグレードする前に、 `server-version`の値を空にするか、現在のTiDBクラスタの実際のバージョンに設定する必要があります。

### `repair-mode` {#repair-mode}

-   信頼できない修復モードを有効にするかどうかを決定します。 `repair-mode`が`true`に設定されている場合、 `repair-table-list`内の不良テーブルはロードできません。
-   デフォルト値: `false`
-   `repair`構文はデフォルトではサポートされていません。つまり、TiDB起動時にすべてのテーブルがロードされます。

### `repair-table-list` {#repair-table-list}

-   `repair-table-list` 、 [`repair-mode`](#repair-mode) `true`に設定されている場合にのみ有効です。 `repair-table-list`は、インスタンス内で修復が必要な不良テーブルのリストです。リストの例は次のとおりです: [&quot;db.table1&quot;,&quot;db.table2&quot;...]。
-   デフォルト値: []
-   リストはデフォルトでは空です。これは、修復が必要な不良テーブルが存在しないことを意味します。

### `new_collations_enabled_on_first_bootstrap` {#new_collations_enabled_on_first_bootstrap}

-   新しい照合順序のサポートを有効または無効にします。
-   デフォルト値: `true`
-   注：この設定は、最初に初期化された TiDB クラスタにのみ有効です。初期化後は、この設定項目を使用して新しい照合順序のサポートを有効または無効にすることはできません。

### `max-server-connections` {#max-server-connections}

-   TiDBで許可される同時クライアント接続の最大数。リソース制御に使用されます。
-   デフォルト値: `0`
-   デフォルトでは、TiDB は同時クライアント接続数の制限を設定しません。この設定項目の値が`0`より大きく、実際のクライアント接続数がこの値に達すると、TiDBサーバーは新しいクライアント接続を拒否します。
-   バージョン 6.2.0 以降、TiDB で許可される同時クライアント接続の最大数を設定するには、TiDB 構成項目[`instance.max_connections`](/tidb-configuration-file.md#max_connections)またはシステム変数[`max_connections`](/system-variables.md#max_connections)が使用されます。 `max-server-connections`引き続き有効です。ただし、 `max-server-connections`と`instance.max_connections`が同時に設定されている場合、後者が有効になります。

### `max-index-length` {#max-index-length}

-   新しく作成されるインデックスの最大許容長を設定します。
-   デフォルト値: `3072`
-   単位：バイト
-   範囲: `[3072, 3072*4]`
-   互換性：
    -   MySQL: インデックスの最大長は3072バイトに固定されています。
    -   TiDBの以前のバージョン：
        -   バージョン3.0.7以前：インデックスの最大長は3072×4バイトに固定されています。
        -   v3.0.8 ～ v3.0.10: インデックスの最大長は3072バイトに固定されています。
    -   v3.0.11以降のバージョンでは、TiDBはさまざまなTiDBバージョンおよびMySQLとの互換性を確保するために、 `max-index-length`構成項目を導入しました。

### `table-column-count-limit` <span class="version-mark">v5.0の新機能</span> {#table-column-count-limit-new-in-v50}

-   単一テーブル内の列数の上限を設定します。
-   デフォルト値: `1017`
-   現在、有効な値の範囲は`[1017, 4096]`です。

### `index-limit` <span class="version-mark">v5.0で追加</span> {#index-limit-new-in-v50}

-   単一テーブル内のインデックス数の上限を設定します。
-   デフォルト値: `64`
-   現在、有効な値の範囲は`[64, 512]`です。

### `enable-telemetry` <span class="version-mark">v4.0.2の新機能</span> {#enable-telemetry-new-in-v402}

> **Warning:**
>
> -   バージョン8.1.0から8.5.2までは、TiDBはテレメトリ機能を削除しており、この設定項目は無効になります。以前のバージョンとの互換性のためにのみ残されています。
> -   バージョン8.5.3から8.5.6までは、TiDBはテレメトリ機能を復活させました。ただし、テレメトリ関連の情報はローカルにのみ記録され、ネットワーク経由でPingCAPにデータは送信されなくなりました。
> -   v8.5.7以降、TiDBはこの設定項目とテレメトリ機能を非推奨にしました。

-   TiDBインスタンスでテレメトリ収集を有効にするかどうかを制御します。
-   デフォルト値: `false`

### `deprecate-integer-display-length` {#deprecate-integer-display-length}

-   この構成項目が`true`に設定されている場合、整数型の表示幅は非推奨になります。
-   デフォルト値: `true` 。v8.5.0 より前のバージョンでは、デフォルト値は`false`です。

### `enable-tcp4-only` <span class="version-mark">v5.0の新機能</span> {#enable-tcp4-only-new-in-v50}

-   TCP4のみでのリスニングを有効または無効にします。
-   デフォルト値: `false`
-   [TCPヘッダーからの実際のクライアントIP](https://github.com/alibaba/LVS/tree/master/kernel/net/toa) 「tcp4」プロトコルで正しく解析できるため、ロード バランシングのために TiDB を LVS とともに使用する場合、このオプションを有効にすると便利です。

### `enable-enum-length-limit` <span class="version-mark">v5.0で追加</span> {#enable-enum-length-limit-new-in-v50}

-   単一の`ENUM`要素と単一の`SET`要素の最大長を制限するかどうかを決定します。
-   デフォルト値: `true`
-   この構成値が`true`の場合、単一の`ENUM`要素と単一の`SET`要素の最大長は 255 文字で、 [MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/string-type-syntax.html)と互換性があります。この構成値が`false`の場合、単一要素の長さに制限はなく、TiDB (v5.0 より前) と互換性があります。

### `graceful-wait-before-shutdown` <span class="version-mark">（v5.0の新機能）</span> {#graceful-wait-before-shutdown-new-in-v50}

-   TiDBがサーバーをシャットダウンした際に待機する秒数を指定します。この待機時間により、クライアントは切断することができます。
-   デフォルト値: `0`
-   TiDBがシャットダウンを待機しているとき（猶予期間中）、HTTPステータスは失敗を示し、ロードバランサーがトラフィックを再ルーティングできるようになります。TiDBは`COM_PING`コマンドに対してもエラーを返します。

> **Note:**
>
> TiDBがサーバーをシャットダウンするまでの待機時間は、以下のパラメータによっても影響を受けます。
>
> -   SystemD を使用するプラットフォームの場合、デフォルトの停止タイムアウトは 90 秒です。より長いタイムアウトが必要な場合は、 [`TimeoutStopSec=`](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html#TimeoutStopSec=)を設定できます。
>
> -   TiUP クラスタコンポーネントを使用する場合、デフォルトの[`--wait-timeout`](/tiup/tiup-component-cluster.md#--wait-timeout)は120秒です。
>
> -   Kubernetesを使用する場合、デフォルトの[`terminationGracePeriodSeconds`](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#lifecycle)は30秒です。

### `enable-global-kill` <span class="version-mark">v6.1.0 で追加されました。</span> {#enable-global-kill-new-in-v610}

-   グローバルキル（インスタンスをまたいでクエリや接続を終了する）機能を有効にするかどうかを制御します。
-   デフォルト値: `true`
-   値が`true`の場合、 `KILL`および`KILL TIDB`ステートメントはインスタンス間でクエリまたは接続を終了できるため、クエリまたは接続が誤って終了することを心配する必要はありません。クライアントを使用して任意の TiDB インスタンスに接続し、 `KILL`または`KILL TIDB`ステートメントを実行すると、ステートメントは対象の TiDB インスタンスに転送されます。クライアントと TiDB クラスタの間にプロキシがある場合、 `KILL`および`KILL TIDB`ステートメントも実行のために対象の TiDB インスタンスに転送されます。
-   バージョン7.3.0以降では、 `enable-global-kill`<kbd>に</kbd>`true`されている場合、MySQLコマンドラインのControl+Cを使用して[`enable-32bits-connection-id`](#enable-32bits-connection-id-new-in-v730)できます。詳細については、[`KILL`](/sql-statements/sql-statement-kill.md)参照してください。

### `enable-32bits-connection-id` <span class="version-mark">v7.3.0で追加</span> {#enable-32bits-connection-id-new-in-v730}

-   32ビット接続ID機能を有効にするかどうかを制御します。
-   デフォルト値: `true`
-   この設定項目と[`enable-global-kill`](#enable-global-kill-new-in-v610)両方が`true`に設定されている場合、TiDBは32ビットの接続IDを生成します。これにより、MySQLコマンドラインの<kbd>Control+C</kbd>を使用してクエリまたは接続を終了できます。

> **Warning:**
>
> クラスタ内の TiDB インスタンス数が 2048 を超えるか、単一の TiDB インスタンスの同時接続数が 1048576 を超えると、32 ビットの接続 ID 空間が不足し、自動的に 64 ビットの接続 ID にアップグレードされます。アップグレード処理中は、既存のビジネス接続および確立済みの接続には影響はありません。ただし、その後に開始される新しい接続は、MySQL コマンドラインで<kbd>Control+C</kbd>を使用して終了することはできません。

### `initialize-sql-file` <span class="version-mark">v6.6.0で追加</span> {#initialize-sql-file-new-in-v660}

-   TiDBクラスタが初めて起動されたときに実行されるSQLスクリプトを指定します。
-   デフォルト値: `""`
-   このスクリプト内のすべてのSQL文は、権限チェックなしで最高権限で実行されます。指定されたSQLスクリプトの実行に失敗すると、TiDBクラスタの起動に失敗する可能性があります。
-   この構成項目は、システム変数の値の変更、ユーザーの作成、権限の付与などの操作を実行するために使用されます。

### `enable-forwarding` <span class="version-mark">v5.0.0の新機能</span> {#enable-forwarding-new-in-v500}

-   TiDB内のPDクライアントとTiKVクライアントが、ネットワークが隔離された場合に、フォロワーを介してリーダーにリクエストを転送するかどうかを制御します。
-   デフォルト値: `false`
-   環境が孤立したネットワークである可能性がある場合、このパラメータを有効にすることで、サービスが利用できなくなる時間を短縮できます。
-   隔離、ネットワーク障害、またはダウンタイムが発生したかどうかを正確に判断できない場合、このメカニズムを使用すると誤判断のリスクがあり、可用性とパフォーマンスが低下します。ネットワーク障害が一度も発生したことがない場合は、このパラメータを有効にすることは推奨されません。

### `enable-table-lock` <span class="version-mark">v4.0.0で追加</span> {#enable-table-lock-new-in-v400}

> **Warning:**
>
> テーブルロック機能は実験的機能です。本番環境での使用は推奨されません。

-   テーブルロック機能を有効にするかどうかを制御します。
-   デフォルト値: `false`
-   テーブルロックは、複数のセッション間で同じテーブルへの同時アクセスを調整するために使用されます。現在、 `READ` 、 `WRITE` 、および`WRITE LOCAL`ロックタイプがサポートされています。構成項目が`false`に設定されている場合、 `LOCK TABLES`または`UNLOCK TABLES`ステートメントを実行しても効果がなく、「LOCK/UNLOCK TABLES はサポートされていません」という警告が表示されます。詳細については、「 [`LOCK TABLES`と`UNLOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)を参照してください。

### `labels` {#labels}

-   サーバーラベルを指定します。例: `{ zone = "us-west-1", dc = "dc1", rack = "rack1", host = "tidb1" }` 。
-   デフォルト値: `{}`

> **Note:**
>
> -   TiDBでは、 `zone`ラベルは、サーバーが配置されているゾーンを指定するために特別に使用されます。 `zone`がnull以外の値に設定されている場合、対応する値は[`txn-score`](/system-variables.md#txn_scope)や[`Follower read`](/follower-read.md)などの機能によって自動的に使用されます。
> -   `group`ラベルは、TiDB Operatorにおいて特別な用途があります。TiDB [TiDB Operator](/tidb-operator-overview.md)を使用してデプロイされたクラスタでは、 `group`ラベルを手動で指定することは推奨さ**れません**。

## log {#log}

ログに関連するコンフィグレーション項目。

### `level` {#level}

-   ログ出力レベルを指定します。
-   値のオプション: `debug` 、 `info` 、 `warn` 、 `error` 、および`fatal` 。
-   デフォルト値: `info`

### `format` {#format}

-   ログ出力形式を指定します。
-   値のオプション: `json`および`text` 。
-   デフォルト値: `text`

### `enable-timestamp` {#enable-timestamp}

-   ログにタイムスタンプを出力するかどうかを決定します。
-   デフォルト値: `null`
-   値を`false`に設定すると、ログにタイムスタンプが出力されません。

> **Note:**
>
> -   下位互換性を維持するため、初期設定項目`disable-timestamp`は有効なままです。ただし、 `disable-timestamp`の値が`enable-timestamp`の値と意味的に競合する場合 (たとえば、 `enable-timestamp`と`disable-timestamp`両方が`true`に設定されている場合)、TiDB は`disable-timestamp`の値を無視します。
> -   現在、TiDB は`disable-timestamp`を使用して、ログにタイムスタンプを出力するかどうかを判断します。この場合、 `enable-timestamp`の値は`null`になります。
> -   後のバージョンでは、 `disable-timestamp`の設定は削除されます。 `disable-timestamp`は破棄し、意味的に理解しやすい`enable-timestamp`を使用してください。

### `enable-slow-log` {#enable-slow-log}

-   スロークエリログを有効にするかどうかを決定します。
-   デフォルト値: `true`
-   スロークエリログを有効にするには、 `enable-slow-log`を`true`に設定してください。それ以外の場合は、 `false`に設定してください。
-   バージョン6.1.0以降、スロークエリログを有効にするかどうかは、TiDB構成アイテム[`instance.tidb_enable_slow_log`](/tidb-configuration-file.md#tidb_enable_slow_log)またはシステム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)によって決定されます。 `enable-slow-log`は引き続き有効です。ただし、 `enable-slow-log`と`instance.tidb_enable_slow_log`が同時に設定されている場合、後者が有効になります。

### `slow-query-file` {#slow-query-file}

-   スロークエリログのファイル名。
-   デフォルト値: `tidb-slow.log`
-   TiDB v2.1.8ではスローログのフォーマットが更新され、スローログはスローログファイルに個別に出力されるようになりました。v2.1.8より前のバージョンでは、この変数はデフォルトで「」に設定されています。
-   設定後、スロークエリのログはこのファイルに別途出力されます。

### `slow-threshold` {#slow-threshold}

-   スローログに記録された、消費時間のしきい値を出力します。
-   デフォルト値: `300`
-   単位：ミリ秒
-   クエリの実行時間がこの値よりも長い場合、そのクエリはスロークエリとみなされ、そのログがスロークエリログに出力されます。なお、 [`log.level`](#level)の出力レベルが`"debug"`の場合、このパラメータの設定に関わらず、すべてのクエリがスロークエリログに記録されます。
-   バージョン 6.1.0 以降、スロー ログの消費時間のしきい値は、TiDB 設定項目の[`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold)またはシステム変数[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)で指定されます。 `slow-threshold`引き続き有効です。ただし、 `slow-threshold`と`instance.tidb_slow_log_threshold`が同時に設定されている場合、後者が有効になります。

### `record-plan-in-slow-log` {#record-plan-in-slow-log}

-   実行計画をスローログに記録するかどうかを決定します。
-   デフォルト値: `1`
-   バージョン 6.1.0 以降、実行プランをスロー ログに記録するかどうかは、TiDB 設定項目の[`instance.tidb_record_plan_in_slow_log`](/tidb-configuration-file.md#tidb_record_plan_in_slow_log)またはシステム変数[`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log)によって決定されます。 `record-plan-in-slow-log`引き続き有効です。ただし、 `record-plan-in-slow-log`と`instance.tidb_record_plan_in_slow_log`が同時に設定されている場合は、後者が有効になります。

### `expensive-threshold` {#expensive-threshold}

> **Warning:**
>
> バージョン5.4.0以降、 `expensive-threshold`構成項目は非推奨となり、システム変数[`tidb_expensive_query_time_threshold`](/system-variables.md#tidb_expensive_query_time_threshold)に置き換えられました。

-   `expensive`操作の行数のしきい値を出力します。
-   デフォルト値: `10000`
-   クエリ行数（統計に基づく中間結果を含む）がこの値より大きい場合、 `expensive`操作となり、 `[EXPENSIVE_QUERY]`接頭辞が付いたログが出力されます。

### `general-log-file` <span class="version-mark">v8.0.0で追加</span> {#general-log-file-new-in-v800}

-   [一般ログ](/system-variables.md#tidb_general_log)のファイル名。
-   デフォルト値: `""`
-   ファイル名を指定すると、一般ログはこの指定されたファイルに書き込まれます。値が空白の場合は、一般ログは TiDB インスタンスのサーバーログに書き込まれます。サーバーログの名前は[`filename`](#filename)を使用して指定できます。

### `timeout` <span class="version-mark">v7.1.0の新機能</span> {#timeout-new-in-v710}

-   TiDBにおけるログ書き込み操作のタイムアウトを設定します。ディスク障害によりログの書き込みができない場合、この設定項目によってTiDBプロセスがハングアップするのではなく、panicになることがあります。
-   デフォルト値： `0` 。これはタイムアウトが設定されていないことを示します。
-   単位：秒
-   一部のユーザーシナリオでは、TiDBログがホットプラグ対応ディスクまたはネットワーク接続ディスクに保存されることがありますが、これらのディスクが永久的に使用不能になる可能性があります。このような場合、TiDBは自動的に復旧できず、ログ書き込み操作は永久的にブロックされます。TiDBプロセスは実行されているように見えても、実際にはどの要求にも応答しません。この設定項目は、このような状況に対処するために設計されています。

### log.file {#logfile}

ログファイルに関連するコンフィグレーション項目。

#### `filename` {#filename}

-   一般ログファイルのファイル名。
-   デフォルト値: &quot;&quot;
-   設定すると、ログはこのファイルに出力されます。

#### `max-size` {#max-size}

-   ログファイルのサイズ制限。
-   デフォルト値: 300
-   単位: MB
-   最大値は4096です。

#### `max-days` {#max-days}

-   ログが保持される最大日数。
-   デフォルト値: `0`
-   デフォルトではログは保持されます。値を設定すると、期限切れのログは`max-days`の後にクリーンアップされます。

#### `max-backups` {#max-backups}

-   保持するログの最大数。
-   デフォルト値: `0`
-   デフォルトでは、すべてのログファイルが保持されます。 `7`に設定すると、最大で 7 つのログファイルが保持されます。

#### `compression` <span class="version-mark">（v8.0.0の新機能）</span> {#compression-new-in-v800}

-   ログの圧縮方法。
-   デフォルト値: `""`
-   値のオプション: `""` 、 `"gzip"`
-   デフォルト値は`""`で、これは圧縮なしを意味します。gzip 圧縮を有効にするには、この値を`"gzip"`に設定してください。圧縮を有効にすると、 [`slow-query-file`](#slow-query-file)や[`general-log-file`](#general-log-file-new-in-v800)など、すべてのログファイルが影響を受けます。

## security {#security}

セキュリティに関連するコンフィグレーション項目。

### `enable-sem` {#enable-sem}

-   セキュリティ強化モード（SEM）を有効にします。
-   デフォルト値: `false`
-   SEM の状態は、システム変数[`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)を通じて確認できます。

### `ssl-ca` {#ssl-ca}

-   信頼済みCA証明書（PEM形式）のファイルパス。
-   デフォルト値: &quot;&quot;
-   このオプションと`--ssl-cert` 、 `--ssl-key`を同時に設定した場合、クライアントが証明書を提示すると、TiDB はこのオプションで指定された信頼済み CA のリストに基づいてクライアント証明書を認証します。認証に失敗した場合、接続は切断されます。
-   このオプションを設定した場合でも、クライアントが証明書を提示しない場合は、クライアント証明書の認証なしでセキュアな接続が継続されます。

### `ssl-cert` {#ssl-cert}

-   PEM形式のSSL証明書のファイルパス。
-   デフォルト値: &quot;&quot;
-   このオプションと`--ssl-key`を同時に設定すると、TiDB はクライアントが TLS を使用して TiDB に安全に接続することを許可します (ただし、強制はしません)。
-   指定された証明書または秘密鍵が無効な場合、TiDBは通常どおり起動しますが、安全な接続を受信できません。

### `ssl-key` {#ssl-key}

-   PEM形式のSSL証明書キーのファイルパス、つまり`--ssl-cert`で指定された証明書の秘密鍵。
-   デフォルト値: &quot;&quot;
-   現在、TiDBはパスワードで保護された秘密鍵の読み込みをサポートしていません。

### `cluster-ssl-ca` {#cluster-ssl-ca}

-   TiKVまたはPDをTLSで接続するために使用されるCAルート証明書。
-   デフォルト値: &quot;&quot;

### `cluster-ssl-cert` {#cluster-ssl-cert}

-   TiKVまたはPDをTLSで接続するために使用されるSSL証明書ファイルのパス。
-   デフォルト値: &quot;&quot;

### `cluster-ssl-key` {#cluster-ssl-key}

-   TiKVまたはPDをTLSに接続するために使用されるSSL秘密鍵ファイルのパス。
-   デフォルト値: &quot;&quot;

### `cluster-verify-cn` {#cluster-verify-cn}

-   クライアントから提示される証明書において許容されるX.509共通名のリスト。提示された共通名がリスト内のいずれかのエントリと完全に一致する場合にのみ、リクエストが許可されます。
-   デフォルト値: []。これは、クライアント証明書のCNチェックが無効になっていることを意味します。

### `spilled-file-encryption-method` {#spilled-file-encryption-method}

-   漏洩したファイルをディスクに保存する際に使用する暗号化方式を決定します。
-   デフォルト値： `"plaintext"` 。これは暗号化を無効にします。
-   オプション値： `"plaintext"`および`"aes128-ctr"`

### `auto-tls` {#auto-tls}

-   起動時にTLS証明書を自動的に生成するかどうかを決定します。
-   デフォルト値: `false`

### `tls-version` {#tls-version}

> **Warning:**
>
> `"TLSv1.0"`および`"TLSv1.1"`プロトコルは TiDB v7.6.0 で非推奨となり、v8.0.0 で削除されます。

-   MySQLプロトコル接続に使用するTLSの最小バージョンを設定します。
-   デフォルト値は「」で、TLSv1.2以降のバージョンを許可します。TiDB v7.6.0より前のバージョンでは、デフォルト値はTLSv1.1以降のバージョンを許可します。
-   オプション値: `"TLSv1.2"`および`"TLSv1.3"` 。TiDB v8.0.0 より前のバージョンでは、 `"TLSv1.0"`および`"TLSv1.1"`も使用可能です。

### `auth-token-jwks` <span class="version-mark">v6.4.0の新機能</span> {#auth-token-jwks-new-in-v640}

-   [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token)認証方式で使用するJSON Web Key Sets（JWKS）のローカルファイルパスを設定します。
-   デフォルト値: `""`

### `auth-token-refresh-interval` <span class="version-mark">v6.4.0 で追加されました。</span> {#auth-token-refresh-interval-new-in-v640}

-   [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token)認証方式のJWKS更新間隔を設定します。
-   デフォルト値: `1h`

### `disconnect-on-expired-password` <span class="version-mark">（v6.5.0の新機能）</span> {#disconnect-on-expired-password-new-in-v650}

-   パスワードの有効期限が切れたときに、TiDBがクライアント接続を切断するかどうかを決定します。
-   デフォルト値: `true`
-   オプション値: `true` 、 `false`
-   `true`に設定すると、パスワードの有効期限が切れたときにクライアント接続が切断されます。 `false`に設定すると、クライアント接続は「サンドボックスモード」に制限され、ユーザーはパスワードリセット操作のみを実行できます。

### `session-token-signing-cert` <span class="version-mark">v6.4.0 の新機能</span> {#session-token-signing-cert-new-in-v640}

-   [TiProxy](/tiproxy/tiproxy-overview.md)がセッション移行に使用する証明書ファイルのパス。
-   デフォルト値: &quot;&quot;
-   値が空の場合、TiProxy のセッション移行は失敗します。セッション移行を有効にするには、すべての TiDB ノードで同じ証明書とキーを設定する必要があります。つまり、すべての TiDB ノードに同じ証明書とキーを保存する必要があります。

### `session-token-signing-key` <span class="version-mark">v6.4.0 の新機能</span> {#session-token-signing-key-new-in-v640}

-   [TiProxy](/tiproxy/tiproxy-overview.md)がセッション移行に使用するキーファイルのパス。
-   デフォルト値: &quot;&quot;
-   [`session-token-signing-cert`](#session-token-signing-cert-new-in-v640)の説明を参照してください。

## performance {#performance}

パフォーマンスに関連するコンフィグレーション項目。

### `max-procs` {#max-procs}

-   TiDBが使用するCPUの数。
-   デフォルト値: `0`
-   デフォルト値の`0`は、マシン上のすべてのCPUを使用することを示します。nに設定すると、TiDBはn個のCPUを使用します。

### `server-memory-quota` <span class="version-mark">v4.0.9の新機能</span> {#server-memory-quota-new-in-v409}

> **Warning:**
>
> バージョン6.5.0以降、 `server-memory-quota`構成項目は非推奨となり、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)に置き換えられました。

-   tidb-serverインスタンスのメモリ使用量制限。
-   デフォルト値: `0` (バイト単位)。これはメモリ制限がないことを意味します。

### `max-txn-ttl` {#max-txn-ttl}

-   単一のトランザクションがロックを保持できる最長時間。この時間を超えると、他のトランザクションによってトランザクションのロックが解除され、そのトランザクションを正常にコミットできなくなる可能性があります。
-   デフォルト値: `3600000`
-   単位：ミリ秒
-   この時間よりも長くロックを保持しているトランザクションは、コミットまたはロールバックのいずれかしか実行できません。コミットが成功しない場合もあります。
-   [`&quot;bulk&quot;` DMLモード](/system-variables.md#tidb_dml_type-new-in-v800)を使用して実行されるトランザクションの場合、最大TTLはこの設定項目の制限を超えることができます。最大値は、この設定項目と24時間のうち大きい方の値となります。

### `stmt-count-limit` {#stmt-count-limit}

-   TiDBトランザクション1回で許可されるステートメントの最大数。
-   デフォルト値: `5000`
-   ステートメント数が`stmt-count-limit`を超えた後にトランザクションがロールバックまたはコミットされない場合、TiDB は`statement count 5001 exceeds the transaction limitation, autocommit = false`エラーを返します。この設定は、再試行可能な楽観的トランザクションで**のみ**有効です。悲観的トランザクションを使用している場合、またはトランザクションの再試行を無効にしている場合は、トランザクション内のステートメント数はこの設定によって制限されません。

### `txn-entry-size-limit`<span class="version-mark">は v4.0.10 および v5.0.0 で追加されました。</span> {#txn-entry-size-limit-new-in-v4010-and-v500}

-   TiDBにおける単一行データのサイズ制限。
-   デフォルト値: `6291456` (バイト単位)
-   トランザクション内の単一のキー値レコードのサイズ制限。サイズ制限を超えると、TiDB は`entry too large`エラーを返します。この構成項目の最大値は`125829120` (120 MB) を超えません。
-   バージョン7.6.0以降では、システム変数[`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)を使用して、この設定項目の値を動的に変更できます。
-   TiKVにも同様の制限があることに注意してください。単一の書き込みリクエストのデータサイズが、デフォルトで8MBに設定されている[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)超えると、TiKVはこのリクエストの処理を拒否します。テーブルに大きな行がある場合は、両方の設定を同時に変更する必要があります。
-   [`max_allowed_packet`](/system-variables.md#max_allowed_packet-new-in-v610) （MySQLプロトコルのパケットの最大サイズ）のデフォルト値は67108864（64 MiB）です。行が`max_allowed_packet`より大きい場合、行は切り捨てられます。
-   [`txn-total-size-limit`](#txn-total-size-limit) （TiDBにおける単一トランザクションのサイズ制限）のデフォルト値は100 MiBです。 `txn-entry-size-limit`の値を100 MiB以上に増やす場合は、 `txn-total-size-limit`の値もそれに合わせて増やす必要があります。

### `txn-total-size-limit` {#txn-total-size-limit}

-   TiDBにおける単一トランザクションのサイズ制限。
-   デフォルト値: `104857600` (バイト単位)
-   単一のトランザクションにおいて、キーと値のレコードの合計サイズはこの値を超えることはできません。このパラメータの最大値は`1099511627776` (1 TB) です。
-   TiDB v6.5.0 以降のバージョンでは、この設定は推奨されなくなりました。トランザクションのメモリサイズはセッションのメモリ使用量に累積され、セッションのメモリしきい値を超えると[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)変数が有効になります。以前のバージョンとの互換性を保つため、以前のバージョンから TiDB v6.5.0 以降にアップグレードする場合、この設定は次のように動作します。
    -   この設定が設定されていないか、デフォルト値 ( `104857600` ) に設定されている場合、アップグレード後にトランザクションのメモリサイズがセッションのメモリ使用量に累積され、 `tidb_mem_quota_query`変数が有効になります。
    -   この設定がデフォルト設定（ `104857600` ）になっていない場合でも、設定は有効であり、単一トランザクションのサイズを制御する動作はアップグレード前後で変わりません。つまり、トランザクションのメモリサイズは`tidb_mem_quota_query`変数によって制御されません。
-   TiDB が[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) `"bulk"`モードでトランザクションを実行する場合、トランザクションのサイズは TiDB 構成項目[`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)によって制限されません。

### `tcp-keep-alive` {#tcp-keep-alive}

-   TCPレイヤーで`keepalive`を有効にするかどうかを決定します。
-   デフォルト値: `true`

### `tcp-no-delay` {#tcp-no-delay}

-   TCPレイヤーでTCP_NODELAYを有効にするかどうかを決定します。有効にすると、TiDBはTCP/IPプロトコルのNagleアルゴリズムを無効にし、小さなデータパケットを送信してネットワークレイテンシーを低減します。これは、送信データ量が少なく、遅延に敏感なアプリケーションに適しています。
-   デフォルト値: `true`

### `cross-join` {#cross-join}

-   デフォルト値: `true`
-   TiDB は、デフォルトでは、両方のテーブルの条件 ( `WHERE`フィールド) なしで`JOIN`ステートメントを実行することをサポートしています。値を`false`に設定すると、そのような`JOIN`ステートメントが現れたときにサーバーは実行を拒否します。

> **Note:**
>
> クラスターを作成する際は、 `cross-join`を false に設定**しないでください**。設定してしまうと、クラスターの起動に失敗します。

### `stats-lease` {#stats-lease}

-   統計情報の再読み込み、テーブル行数の更新、自動分析の実行が必要かどうかの確認、フィードバックを使用した統計情報の更新、および列の統計情報の読み込みを行う時間間隔。
-   デフォルト値: `3s`
    -   `stats-lease`間隔で、TiDB は統計情報の更新をチェックし、更新が存在する場合はそれをメモリに更新します。
    -   `20 * stats-lease`間隔で、TiDB は DML によって生成された行の総数と変更された行の数をシステム テーブルに更新します。
    -   `stats-lease`の間隔で、TiDB は自動分析が必要なテーブルとインデックスをチェックします。
    -   `stats-lease`の間隔で、TiDB はメモリにロードする必要のある列統計をチェックします。
    -   `200 * stats-lease`の間隔で、TiDB はメモリにキャッシュされたフィードバックをシステム テーブルに書き込みます。
    -   `5 * stats-lease`の間隔で、TiDB はシステム テーブル内のフィードバックを読み取り、メモリにキャッシュされた統計情報を更新します。
-   `stats-lease`を 0s に設定すると、TiDB はシステム テーブル内のフィードバックを定期的に読み取り、メモリにキャッシュされた統計情報を 3 秒ごとに更新します。ただし、TiDB は、以下の統計情報関連のシステム テーブルを自動的に変更しなくなります。
    -   `mysql.stats_meta` : TiDB は、トランザクションによって変更されたテーブル行の数を自動的に記録し、このシステム テーブルに更新しなくなりました。
    -   `mysql.stats_histograms` / `mysql.stats_buckets`および`mysql.stats_top_n` : TiDB は統計情報を自動的に分析して積極的に更新しなくなりました。
    -   `mysql.stats_feedback` : TiDB は、クエリされたデータによって返される統計情報の一部に基づいて、テーブルとインデックスの統計情報を更新しなくなりました。

### `pseudo-estimate-ratio` {#pseudo-estimate-ratio}

-   テーブル内の（変更された行数）／（総行数）の比率。この値を超えると、システムは統計情報が期限切れになったと判断し、擬似統計情報を使用します。
-   デフォルト値: `0.8`
-   最小値は`0`で、最大値は`1`です。

### `force-priority` {#force-priority}

-   すべてのステートメントの優先順位を設定します。
-   デフォルト値: `NO_PRIORITY`
-   値のオプション: デフォルト値`NO_PRIORITY` 、ステートメントの優先順位が強制的に変更されないことを意味します。その他のオプションは、昇順で`LOW_PRIORITY` 、 `DELAYED` 、 `HIGH_PRIORITY` 。
-   バージョン6.1.0以降、すべてのステートメントの優先順位は、TiDB構成アイテム[`instance.tidb_force_priority`](/tidb-configuration-file.md#tidb_force_priority)またはシステム変数[`tidb_force_priority`](/system-variables.md#tidb_force_priority)によって決定されます。 `force-priority`引き続き有効です。ただし、 `force-priority`と`instance.tidb_force_priority`が同時に設定されている場合、後者が有効になります。

> **Note:**
>
> バージョン6.6.0以降、TiDBは[リソース制御](/tidb-resource-control-ru-groups.md)サポートしています。この機能を使用すると、異なるリソースグループで異なる優先度のSQLステートメントを実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、異なる優先度のSQLステートメントのスケジューリングをより適切に制御できます。リソース制御が有効になっている場合、ステートメントの優先度は適用されなくなります。 を使用して[リソース制御](/tidb-resource-control-ru-groups.md)異なるSQLステートメントのリソース使用量を管理することをお勧めします。

### `distinct-agg-push-down` {#distinct-agg-push-down}

-   オプティマイザが`Distinct` (例えば`select count(distinct a) from t` ) を使用して集約関数をコプロセッサにプッシュダウンする操作を実行するかどうかを決定します。
-   デフォルト: `false`
-   この変数は、システム変数[`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)の初期値です。

### `enforce-mpp` {#enforce-mpp}

-   オプティマイザのコスト見積もりを無視し、クエリ実行にTiFlashのMPPモードを強制的に使用するかどうかを決定します。
-   デフォルト値: `false`
-   この設定項目は、 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の初期値を制御します。たとえば、この設定項目が`true`に設定されている場合、 `tidb_enforce_mpp`のデフォルト値は`ON`になります。

### `enable-stats-cache-mem-quota` <span class="version-mark">v6.1.0で追加</span> {#enable-stats-cache-mem-quota-new-in-v610}

-   統計キャッシュのメモリ割り当てを有効にするかどうかを制御します。
-   デフォルト値: `true`

### `stats-load-concurrency` <span class="version-mark">v5.4.0の新機能</span> {#stats-load-concurrency-new-in-v540}

-   TiDBの同期統計情報読み込み機能が同時に処理できる列の最大数。
-   デフォルト値: `0` 。v8.2.0 より前のバージョンでは、デフォルト値は`5`です。
-   現在、有効な値の範囲は`[0, 128]`です。値`0`は自動モードを意味し、サーバーの設定に基づいて同時実行数を自動的に調整します。v8.2.0 より前のバージョンでは、最小値は`1`でした。

### `stats-load-queue-size` <span class="version-mark">v5.4.0で追加</span> {#stats-load-queue-size-new-in-v540}

-   TiDBの同期統計情報読み込み機能がキャッシュできる列リクエストの最大数。
-   デフォルト値: `1000`
-   現在、有効な値の範囲は`[1, 100000]`です。

### `concurrently-init-stats` <span class="version-mark">v8.1.0 および v7.5.2 で追加されました。</span> {#concurrently-init-stats-new-in-v810-and-v752}

-   TiDB の起動時に統計情報を同時に初期化するかどうかを制御します。この設定項目は、 [`lite-init-stats`](#lite-init-stats-new-in-v710) `false`に設定されている場合にのみ有効になります。
-   デフォルト値: v8.2.0 より前のバージョンでは`false` 、v8.2.0 以降のバージョンでは`true` 。

### `lite-init-stats` <span class="version-mark">v7.1.0の新機能</span> {#lite-init-stats-new-in-v710}

-   TiDBの起動時に軽量統計初期化を使用するかどうかを制御します。
-   デフォルト値: v7.2.0 より前のバージョンでは`false` 、v7.2.0 以降のバージョンでは`true` 。
-   `lite-init-stats`の値が`true`の場合、統計情報の初期化では、インデックスと列のヒストグラム、TopN、または Count-Min Sketch はメモリにロードされません。 `lite-init-stats`の値が`false`の場合、統計情報の初期化では、インデックスのヒストグラム、TopN、および Count-Min Sketch はメモリにロードされますが、主キーと列のヒストグラム、TopN、または Count-Min Sketch はメモリにロードされません。オプティマイザが特定の主キーまたは列のヒストグラム、TopN、および Count-Min Sketch を必要とする場合、必要な統計情報は同期または非同期でメモリにロードされます ( [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)で制御)。
-   `lite-init-stats`を`true`に設定すると、統計情報の初期化が高速化され、不要な統計情報の読み込みを回避することで TiDB のメモリ使用量が削減されます。詳細については、[負荷統計](/statistics.md#load-statistics)参照してください。

### `force-init-stats` <span class="version-mark">v6.5.7 および v7.1.0 で追加されました。</span> {#force-init-stats-new-in-v657-and-v710}

-   TiDBの起動時に、サービスを提供する前に統計情報の初期化が完了するまで待機するかどうかを制御します。
-   デフォルト値: v7.2.0 より前のバージョンでは`false` 、v7.2.0 以降のバージョンでは`true` 。
-   `force-init-stats`の値が`true`の場合、TiDB は起動時にサービスを提供する前に、統計情報の初期化が完了するまで待機する必要があります。テーブルとパーティションの数が多く、lite-init-stats の値が`false`の場合、 `force-init-stats` `true`に設定すると、 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)がサービスの提供を開始するまでの時間が長くなる可能性があることに注意してください。
-   `force-init-stats`の値が`false`の場合、統計情報の初期化が完了する前に TiDB はサービスを提供できますが、オプティマイザは擬似統計情報を使用して決定を行うため、最適ではない実行プランになる可能性があります。

### `enable-async-batch-get` <span class="version-mark">v8.5.5で追加</span> {#enable-async-batch-get-new-in-v855}

-   TiDBがバッチ取得演算子を実行する際に非同期モードを使用するかどうかを制御します。非同期モードを使用すると、ゴルーチンのオーバーヘッドを削減し、パフォーマンスを向上させることができます。通常、この設定項目を変更する必要はありません。
-   デフォルト値: `false`

## opentracing {#opentracing}

OpenTracingに関連するコンフィグレーション項目。

### `enable` {#enable}

-   一部のTiDBコンポーネントの呼び出しオーバーヘッドをトレースするために、opentracingを有効にします。opentracingを有効にすると、パフォーマンスが低下することに注意してください。
-   デフォルト値: `false`

### `rpc-metrics` {#rpc-metrics}

-   RPCメトリクスを有効にします。
-   デフォルト値: `false`

### opentracing.sampler {#opentracingsampler}

opentracing.sampler に関連するコンフィグレーション項目。

#### `type` {#type}

-   OpenTracingサンプラーのタイプを指定します。文字列値は大文字と小文字を区別しません。
-   デフォルト値: `"const"`
-   値のオプション: `"const"` 、 `"probabilistic"` 、 `"ratelimiting"` 、 `"remote"`

#### `param` {#param}

-   OpenTracingサンプラーのパラメータ。
    -   `const`タイプの場合、値は`0`または`1`となり、これは`const`サンプラーを有効にするかどうかを示します。
    -   `probabilistic`タイプの場合、パラメータはサンプリング確率を指定します。サンプリング確率は、 `0`から`1`までの浮動小数点数になります。
    -   `ratelimiting`タイプの場合、パラメータは 1 秒あたりにサンプリングされるスパンの数を指定します。
    -   `remote`タイプの場合、パラメータはサンプリング確率を指定します。サンプリング確率は、 `0`から`1`までの浮動小数点数になります。
-   デフォルト値: `1.0`

#### `sampling-server-url` {#sampling-server-url}

-   jaeger-agent サンプリングサーバーの HTTP URL。
-   デフォルト値: `""`

#### `max-operations` {#max-operations}

-   サンプラーがトレースできる操作の最大数。操作がトレースされない場合は、デフォルトの確率的サンプラーが使用されます。
-   デフォルト値: `0`

#### `sampling-refresh-interval` {#sampling-refresh-interval}

-   jaeger-agentのサンプリングポリシーをポーリングする頻度を制御します。
-   デフォルト値: `0`

### opentracing.reporter {#opentracingreporter}

opentracing.reporter に関連するコンフィグレーション項目。

#### `queue-size` {#queue-size}

-   レポーターがメモリ内に記録するキューのサイズ。
-   デフォルト値: `0`

#### `buffer-flush-interval` {#buffer-flush-interval}

-   レポーターがメモリ内のスパンをストレージにフラッシュする間隔。
-   デフォルト値: `0`

#### `log-spans` {#log-spans}

-   送信されたすべてのスパンのログを出力するかどうかを決定します。
-   デフォルト値: `false`

#### `local-agent-host-port` {#local-agent-host-port}

-   記者がメールを送る宛先は、イェーガーエージェントに繋がっている。
-   デフォルト値: `""`

## pd-client {#pd-client}

### `pd-server-timeout` {#pd-server-timeout}

-   TiDBがPDクライアントを介してPDノードにリクエストを送信する際のタイムアウト時間。
-   デフォルト値: 3
-   単位：秒

## tikv-client {#tikv-client}

### `grpc-connection-count` {#grpc-connection-count}

-   各TiKVとの間で確立できる最大接続数。
-   デフォルト値: `4`

### `grpc-keepalive-time` {#grpc-keepalive-time}

-   TiDBノードとTiKVノード間のRPC接続の`keepalive`時間間隔。指定された時間間隔内にネットワークパケットがない場合、gRPCクライアントは`ping`コマンドをTiKVに実行して、TiKVがアクティブかどうかを確認します。
-   デフォルト: `10`
-   最小値: `1`
-   単位：秒

### `grpc-keepalive-timeout` {#grpc-keepalive-timeout}

-   TiDBノードとTiKVノード間のRPC `keepalive`チェックのタイムアウト。
-   デフォルト値: `3`
-   最小値: `0.05`
-   単位：秒

### `grpc-compression-type` {#grpc-compression-type}

-   TiDBノードからTiKVノードへのデータ転送に使用される圧縮タイプを指定します。デフォルト値は`"none"`で、これは圧縮なしを意味します。gzip圧縮を有効にするには、この値を`"gzip"`に設定します。
-   デフォルト値: `"none"`
-   値のオプション: `"none"` 、 `"gzip"`

> **Note:**
>
> TiKVノードからTiDBノードに返される応答メッセージの圧縮アルゴリズムは、TiKV構成項目[`grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)によって制御されます。

### `commit-timeout` {#commit-timeout}

-   トランザクションコミット実行時の最大タイムアウト時間。
-   デフォルト値: `41s`
-   この値は、 Raft選挙のタイムアウト時間の2倍よりも大きく設定する必要があります。

### `batch-policy` <span class="version-mark">v8.3.0の新機能</span> {#batch-policy-new-in-v830}

-   TiDB から TiKV へのリクエストのバッチ処理戦略を制御します。TiDB は、TiKV にリクエストを送信する際、常に現在の待機キュー内のリクエストを`BatchCommandsRequest`にカプセル化し、パケットとして TiKV に送信します。これが基本的なバッチ処理戦略です。TiKV の負荷スループットが高い場合、TiDB は`batch-policy`の値に基づいて、基本的なバッチ処理の後にさらに待機するかどうかを決定します。この追加のバッチ処理により、より多くのリクエストを単一の`BatchCommandsRequest`にカプセル化されたできます。
-   デフォルト値: `"standard"`
-   お得なオプション：
    -   `"basic"` : この動作は、v8.3.0 より前のバージョンと一致しており、TiDB は[`tikv-client.max-batch-wait-time`](#max-batch-wait-time)が 0 より大きく、TiKV の負荷が[`tikv-client.overload-threshold`](#overload-threshold)の値を超えた場合にのみ追加のバッチ処理を実行します。
    -   `"standard"` : TiDB は、最近のリクエストの到着時間間隔に基づいてリクエストを動的にバッチ処理します。これは、高スループットのシナリオに適しています。
    -   `"positive"` : TiDB は常に追加のバッチ処理を実行します。これは、最適なパフォーマンスを実現するために、高スループットのテストシナリオに適しています。ただし、低負荷のシナリオでは、この戦略により不要なバッチ処理の待機時間が発生し、パフォーマンスが低下する可能性があります。
    -   `"custom{...}"` : バッチ処理戦略のパラメータをカスタマイズできます。このオプションは TiDB の内部テスト用であり、一般的な使用には**推奨されません**。

### `max-batch-size` {#max-batch-size}

-   バッチで送信されるRPCパケットの最大数。値が`0`でない場合、 `BatchCommands` APIを使用してTiKVにリクエストが送信され、同時実行数が多い場合にRPCのレイテンシーが軽減される可能性があります。この値は変更しないことをお勧めします。
-   デフォルト値: `128`

### `max-batch-wait-time` {#max-batch-wait-time}

-   `max-batch-wait-time`がデータパケットをまとめて大きなパケットにカプセル化し、TiKVノードに送信するまで待機します。これは、 `tikv-client.max-batch-size`の値が`0`より大きい場合にのみ有効です。この値を変更しないことを推奨します。
-   デフォルト値: `0`
-   単位：ナノ秒

### `batch-wait-size` {#batch-wait-size}

-   TiKVに一括送信されるパケットの最大数。この値は変更しないことを推奨します。
-   デフォルト値: `8`
-   値が`0`の場合、この機能は無効になります。

### `overload-threshold` {#overload-threshold}

-   TiKV負荷のしきい値。TiKV負荷がこのしきい値を超えると、TiKVの負荷を軽減するために`batch`パケットがさらに収集されます。この設定項目は、 [`tikv-client.max-batch-size`](#max-batch-size)と[`tikv-client.max-batch-wait-time`](#max-batch-wait-time)の両方が`0`より大きい値に設定されている場合にのみ有効になります。この値を変更しないことをお勧めします。
-   デフォルト値: `200`

### `copr-req-timeout` <span class="version-mark">v7.5.0で追加</span> {#copr-req-timeout-new-in-v750}

> **Warning:**
>
> この設定パラメータは将来のバージョンで非推奨になる可能性があります。値を変更**しないでください**。

-   単一のコプロセッサー要求のタイムアウト時間。
-   デフォルト値: `60`
-   単位：秒

### `enable-replica-selector-v2` <span class="version-mark">v8.0.0の新機能</span> {#enable-replica-selector-v2-new-in-v800}

> **Warning:**
>
> バージョン8.2.0以降、この設定項目は非推奨となりました。TiKVへのRPCリクエスト送信時には、デフォルトで新しいバージョンのリージョンレプリカセレクタが使用されます。

-   TiKVにRPCリクエストを送信する際に、リージョンレプリカセレクターの新しいバージョンを使用するかどうか。
-   デフォルト値: `true`

### tikv-client.copr-cache <span class="version-mark">v4.0.0 の新機能</span> {#tikv-clientcopr-cache-new-in-v400}

[コプロセッサーキャッシュ](/coprocessor-cache.md)キャッシュ機能に関する設定項目を紹介します。

#### `capacity-mb` {#capacity-mb}

-   キャッシュされたデータの合計サイズ。キャッシュ領域がいっぱいになると、古いキャッシュエントリが削除されます。値が`0.0`の場合、コプロセッサーキャッシュ機能は無効になります。
-   デフォルト値: `1000.0`
-   単位: MB
-   型: Float

## txn-local-latches {#txn-local-latches}

トランザクションラッチに関連するコンフィグレーション項目。これらの設定項目は将来的に非推奨となる可能性があります。使用は推奨されません。

### `enabled` {#enabled}

-   トランザクションのメモリロックを有効にするかどうかを決定します。
-   デフォルト値: `false`

### `capacity` {#capacity}

-   ハッシュに対応するスロット数。この値は自動的に2の倍数に調整されます。各スロットは32バイトのメモリを占有します。値が小さすぎると、データ書き込み範囲が比較的広い場合（データのインポートなど）に、実行速度が低下したり、パフォーマンスが低下したりする可能性があります。
-   デフォルト値: `2048000`

## status {#status}

TiDBサービスの状態に関するコンフィグレーション。

### `report-status` {#report-status}

-   HTTP APIサービスを有効または無効にします。
-   デフォルト値: `true`

### `record-db-qps` {#record-db-qps}

-   データベース関連のQPSメトリクスをPrometheusに送信するかどうかを決定します。
-   デフォルト値: `false`

### `record-db-label` {#record-db-label}

-   データベース関連のQPSメトリクスをPrometheusに送信するかどうかを決定します。
-   `record-db-qps`よりも多くのメトリックタイプをサポートしています。たとえば、期間やステートメントなどです。
-   デフォルト値: `false`

## pessimistic-txn {#pessimistic-txn}

悲観的トランザクションの使用法については、 [TiDB悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。

### max-retry-count {#max-retry-count}

-   悲観的トランザクションにおける各ステートメントの最大再試行回数。再試行回数がこの制限を超えると、エラーが発生します。
-   デフォルト値: `256`

### deadlock-history-capacity {#deadlock-history-capacity}

-   単一の TiDBサーバーの[`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルに記録できるデッドロック イベントの最大数。このテーブルが満杯の状態でさらにデッドロック イベントが発生した場合、最新のエラーを記録するために、テーブル内の最も古いレコードが削除されます。
-   デフォルト値: `10`
-   最小値: `0`
-   最大値: `10000`

### deadlock-history-collect-retryable {#deadlock-history-collect-retryable}

-   [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md)テーブルが再試行可能なデッドロック エラーの情報を収集するかどうかを制御します。再試行可能なデッドロック エラーの説明については、 [再試行可能なデッドロックエラー](/information-schema/information-schema-deadlocks.md#retryable-deadlock-errors)を参照してください。
-   デフォルト値: `false`

### pessimistic-auto-commit は<span class="version-mark">v6.0.0 で追加されました。</span> {#pessimistic-auto-commit-new-in-v600}

-   悲観的トランザクション モードがグローバルに有効になっている場合 ( `tidb_txn_mode='pessimistic'` ) に、自動コミット トランザクションが使用するトランザクション モードを決定します。デフォルトでは、悲観的トランザクション モードがグローバルに有効になっていても、自動コミット トランザクションは楽観的トランザクション モードを使用します。 `pessimistic-auto-commit`を有効にすると ( `true` } に設定)、自動コミット トランザクションも悲観的モードを使用するようになり、明示的にコミットされた他の悲観的トランザクションと一貫性が保たれます。
-   競合が発生するシナリオでは、この設定を有効にすると、TiDB は自動コミットトランザクションをグローバルロック待機管理に組み込み、デッドロックを回避し、デッドロックを引き起こす競合によって発生するレイテンシーの急増を軽減します。
-   競合のないシナリオで、自動コミット トランザクションが多数ある場合 (具体的な数は実際のシナリオによって決まります。たとえば、自動コミット トランザクションの数がアプリケーションの総数の半分以上を占める場合)、単一のトランザクションが大量のデータを操作すると、この構成を有効にするとパフォーマンスが低下します。たとえば、自動コミット`INSERT INTO SELECT`ステートメントです。
-   セッションレベルのシステム変数[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) `"bulk"`に設定されている場合、セッションにおけるこの設定の効果は、それを`false`に設定することと同じです。
-   デフォルト値: `false`

### constraint-check-in-place-pessimistic） <span class="version-mark">v6.4.0の新機能</span> {#constraint-check-in-place-pessimistic-new-in-v640}

-   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)のデフォルト値を制御します。
-   デフォルト値: `true`

## isolation-read {#isolation-read}

読み取り分離に関連するコンフィグレーション項目。

### `engines` {#engines}

-   TiDBがデータを読み取ることを許可するエンジンを制御する。
-   デフォルト値: [&quot;tikv&quot;, &quot;tiflash&quot;, &quot;tidb&quot;]。これは、エンジンがオプティマイザによって自動的に選択されることを示します。
-   値のオプション: 「tikv」、「tiflash」、「tidb」の任意の組み合わせ。例: [&quot;tikv&quot;, &quot;tidb&quot;] または [&quot;tiflash&quot;, &quot;tidb&quot;]

## instance {#instance}

### `tidb_enable_collect_execution_info` {#tidb_enable_collect_execution_info}

-   この設定では、各オペレーターの実行情報をスロークエリログに記録するかどうか、および[インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)を記録するかどうかを制御します。
-   デフォルト値: `true`
-   v6.1.0より前は、この設定は`enable-collect-execution-info`によって設定されます。

### `tidb_enable_slow_log` {#tidb_enable_slow_log}

-   この設定は、スローログ機能を有効にするかどうかを制御するために使用されます。
-   デフォルト値: `true`
-   値のオプション: `true`または`false`
-   v6.1.0より前は、この設定は`enable-slow-log`によって設定されます。

### `tidb_slow_log_threshold` {#tidb_slow_log_threshold}

-   スローログが消費する時間のしきい値を出力します。
-   デフォルト値: `300`
-   範囲: `[-1, 9223372036854775807]`
-   単位：ミリ秒
-   クエリの実行時間がこの値よりも長い場合、そのクエリはスロークエリとみなされ、そのログがスロークエリログに出力されます。なお、 [`log.level`](#level)の出力レベルが`"debug"`の場合、このパラメータの設定に関わらず、すべてのクエリがスロークエリログに記録されます。
-   v6.1.0より前は、この設定は`slow-threshold`によって設定されます。

### `in-mem-slow-query-topn-num` <span class="version-mark">v7.3.0の新機能</span> {#in-mem-slow-query-topn-num-new-in-v730}

-   この設定は、メモリにキャッシュされるスロークエリの上位件数を制御します。
-   デフォルト値: 30

### `in-mem-slow-query-recent-num` <span class="version-mark">（v7.3.0で追加）</span> {#in-mem-slow-query-recent-num-new-in-v730}

-   この設定は、最近使用されたスロークエリのうち、メモリにキャッシュされるクエリの数を制御します。
-   デフォルト値: 500

### `tidb_expensive_query_time_threshold` {#tidb_expensive_query_time_threshold}

-   この設定は、高負荷なクエリログを出力するかどうかを決定するしきい値を設定するために使用されます。高負荷なクエリログと低負荷なクエリログの違いは次のとおりです。
    -   スローログは、ステートメントの実行後に出力されます。
    -   コストの高いクエリログには、実行時間がしきい値を超えた実行中のステートメントと、それに関連する情報が出力されます。
-   デフォルト値: `60`
-   範囲: `[10, 2147483647]`
-   単位：秒
-   v5.4.0より前は、この設定は`expensive-threshold`によって設定されます。

### `tidb_record_plan_in_slow_log` {#tidb_record_plan_in_slow_log}

-   この設定は、スロークエリの実行プランをスローログに含めるかどうかを制御するために使用されます。
-   デフォルト値: `1`
-   値のオプション: `1` (有効、デフォルト) または`0` (無効)。
-   この設定値は、システム変数[`tidb_record_plan_in_slow_log`](/system-variables.md#tidb_record_plan_in_slow_log)の値を初期化します。
-   v6.1.0より前は、この設定は`record-plan-in-slow-log`によって設定されます。

### `tidb_force_priority` {#tidb_force_priority}

-   この設定は、TiDBサーバー上で実行されるステートメントのデフォルトの優先度を変更するために使用されます。
-   デフォルト値: `NO_PRIORITY`
-   デフォルト値`NO_PRIORITY`は、ステートメントの優先順位が強制的に変更されないことを意味します。その他のオプションは、昇順で`LOW_PRIORITY` 、 `DELAYED` 、 `HIGH_PRIORITY` 。
-   v6.1.0より前は、この設定は`force-priority`によって設定されます。

> **Note:**
>
> バージョン6.6.0以降、TiDBは[リソース制御](/tidb-resource-control-ru-groups.md)サポートしています。この機能を使用すると、異なるリソースグループで異なる優先度のSQLステートメントを実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、異なる優先度のSQLステートメントのスケジューリングをより適切に制御できます。リソース制御が有効になっている場合、ステートメントの優先度は適用されなくなります。 を使用して[リソース制御](/tidb-resource-control-ru-groups.md)異なるSQLステートメントのリソース使用量を管理することをお勧めします。

### `max_connections` {#max_connections}

-   単一のTiDBインスタンスで許可される最大接続数。リソース制御に使用できます。
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   デフォルト値`0`は制限なしを意味します。この変数の値が`0`より大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新規接続を拒否します。
-   この設定値は、システム変数[`max_connections`](/system-variables.md#max_connections)の値を初期化します。
-   v6.2.0より前は、この設定は`max-server-connections`によって設定されます。

### `tidb_enable_ddl` {#tidb_enable_ddl}

-   この設定により、対応するTiDBインスタンスがDDLの所有者になれるかどうかを制御します。
-   デフォルト値: `true`
-   指定可能な値: `OFF` 、 `ON`
-   この設定値は、システム変数[`tidb_enable_ddl`](/system-variables.md#tidb_enable_ddl-new-in-v630)の値を初期化します。
-   v6.3.0より前は、この設定は`run-ddl`によって設定されます。

### `tidb_enable_stats_owner` <span class="version-mark">v8.4.0 で追加されました。</span> {#tidb_enable_stats_owner-new-in-v840}

-   この構成は、対応する TiDB インスタンスが[統計情報の自動更新](/statistics.md#automatic-update)タスクを実行できるかどうかを制御します。
-   デフォルト値: `true`
-   指定可能な値: `true` 、 `false`
-   この設定値は、システム変数[`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-new-in-v840)の値を初期化します。

### `tidb_stmt_summary_enable_persistent` <span class="version-mark">v6.6.0で追加</span> {#tidb_stmt_summary_enable_persistent-new-in-v660}

> **Warning:**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   明細書の要約を永続化するかどうかを制御します。
-   デフォルト値: `false`
-   詳細については、 [持続ステートメントの概要](/statement-summary-tables.md#persist-statements-summary)ご覧ください。

### `tidb_stmt_summary_filename` <span class="version-mark">v6.6.0で追加</span> {#tidb_stmt_summary_filename-new-in-v660}

> **Warning:**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   明細書の要約データの永続化が有効になっている場合、この設定では永続データが書き込まれるファイルを指定します。
-   デフォルト値: `tidb-statements.log`

### `tidb_stmt_summary_file_max_days` <span class="version-mark">v6.6.0 で追加されました。</span> {#tidb_stmt_summary_file_max_days-new-in-v660}

> **Warning:**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   明細書の要約データの永続化が有効になっている場合、この設定では永続データファイルを保持する最大日数を指定します。
-   デフォルト値: `3`
-   単位：日
-   データ保持要件とディスク容量の使用状況に基づいて値を調整できます。

### `tidb_stmt_summary_file_max_size` <span class="version-mark">v6.6.0 で追加されました。</span> {#tidb_stmt_summary_file_max_size-new-in-v660}

> **Warning:**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   明細書の要約の永続化が有効になっている場合、この設定では永続データファイルの最大サイズを指定します。
-   デフォルト値: `64`
-   単位: MiB
-   データ保持要件とディスク容量の使用状況に基づいて値を調整できます。

### `tidb_stmt_summary_file_max_backups` <span class="version-mark">v6.6.0で追加</span> {#tidb_stmt_summary_file_max_backups-new-in-v660}

> **Warning:**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   ステートメントサマリーの永続化が有効になっている場合、この設定では永続化できるデータファイルの最大数を指定します。 `0`ファイル数に制限がないことを意味します。
-   デフォルト値: `0`
-   データ保持要件とディスク容量の使用状況に基づいて値を調整できます。

## proxy-protocol {#proxy-protocol}

PROXYプロトコルに関連するコンフィグレーション項目。

### `networks` {#networks}

-   [プロキシプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)プロトコルを使用して TiDB に接続できるプロキシ サーバーの IP アドレスのリスト
-   デフォルト値: &quot;&quot;
-   一般的に、リバースプロキシ経由でTiDBにアクセスする場合、TiDBはリバースプロキシサーバーのIPアドレスをクライアントのIPアドレスとして認識します。HAProxyなど、PROXYプロトコルをサポートするリバースプロキシは、PROXYプロトコルを有効にすることで、実際のクライアントIPアドレスをTiDBに渡すことができます。
-   このパラメータを設定すると、TiDB は設定された送信元 IP アドレスが PROXY プロトコルを使用して TiDB に接続することを許可します。PROXY 以外のプロトコルが使用されると、この接続は拒否されます。このパラメータを空のままにすると、どの IP アドレスも PROXY プロトコルを使用して TiDB に接続できません。値は`,`を区切り文字とする IP アドレス (192.168.1.50) または CIDR (192.168.1.0/24) です。 `*`任意の IP アドレスを意味します。

> **Warning:**
>
> `*`は、任意の IP アドレスのクライアントが自身の IP アドレスを報告できるようになるため、セキュリティ上のリスクが生じる可能性があるため、慎重に使用してください。また、 `*`を使用すると、TiDB に直接接続する内部コンポーネント(TiDB Dashboardなど) が利用できなくなる可能性もあります。

### `fallbackable` <span class="version-mark">（v6.5.1の新機能）</span> {#fallbackable-new-in-v651}

-   PROXYプロトコルのフォールバックモードを有効にするかどうかを制御します。この設定項目が`true`に設定されている場合、TiDBは`proxy-protocol.networks`に属するクライアントがPROXYプロトコル仕様を使用せずに、またはPROXYプロトコルヘッダーを送信せずにTiDBに接続することを受け入れられます。デフォルトでは、TiDBは`proxy-protocol.networks`に属し、PROXYプロトコルヘッダーを送信するクライアント接続のみを受け入れます。
-   デフォルト値: `false`

## experimental {#experimental}

バージョン3.1.0で導入された`experimental`セクションでは、TiDBの実験的機能に関連する設定について説明します。

### `allow-expression-index` <span class="version-mark">v4.0.0の新機能</span> {#allow-expression-index-new-in-v400}

-   式インデックスを作成できるかどうかを制御します。TiDB v5.2.0 以降では、式内の関数が安全であれば、この設定を有効にしなくても、その関数に基づいて式インデックスを直接作成できます。他の関数に基づいて式インデックスを作成する場合は、この設定を有効にできますが、正確性の問題が発生する可能性があります。 `tidb_allow_function_for_expression_index`変数を照会することで、式の作成に直接使用しても安全な関数を取得できます。
-   デフォルト値: `false`
