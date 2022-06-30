---
title: System Variables
summary: Use system variables to optimize performance or alter running behavior.
---

# システム変数 {#system-variables}

TiDBシステム変数は、設定が`SESSION`または`GLOBAL`スコープに適用されるという点でMySQLと同様に動作します。

-   `SESSION`スコープでの変更は、現在のセッションにのみ影響します。
-   `GLOBAL`スコープの変更はすぐに適用されます。この変数のスコープも`SESSION`の場合、すべてのセッション（セッションを含む）は引き続き現在のセッション値を使用します。
-   変更は[`SET`ステートメント](/sql-statements/sql-statement-set-variable.md)を使用して行われます：

```sql
# These two identical statements change a session variable
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# These two identical statements change a global variable
SET @@global.tidb_distsql_scan_concurrency = 10;
SET  GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **ノート：**
>
> いくつかの`GLOBAL`変数がTiDBクラスタに存続します。このドキュメントの一部の変数には`Persists to cluster`の設定があり、 `Yes`または`No`に構成できます。
>
> -   `Persists to cluster: Yes`に設定された変数の場合、グローバル変数が変更されると、システム変数キャッシュを更新するためにすべてのTiDBサーバーに通知が送信されます。 TiDBサーバーを追加するか、既存のTiDBサーバーを再起動すると、永続化された構成値が自動的に使用されます。
> -   設定が`Persists to cluster: No`の変数の場合、変更は接続しているローカルTiDBインスタンスにのみ適用されます。設定された値を保持するには、 `tidb.toml`の構成ファイルで変数を指定する必要があります。
>
> さらに、TiDBはいくつかのMySQL変数を読み取り可能で設定可能として提供します。これは、アプリケーションとコネクタの両方がMySQL変数を読み取ることが一般的であるため、互換性のために必要です。たとえば、JDBCコネクタは、動作に依存していなくても、クエリキャッシュ設定の読み取りと設定の両方を行います。

> **ノート：**
>
> 値を大きくしても、必ずしもパフォーマンスが向上するとは限りません。ほとんどの設定は各接続に適用されるため、ステートメントを実行している同時接続の数を考慮することも重要です。
>
> 安全な値を決定するときは、変数の単位を考慮してください。
>
> -   スレッドの場合、安全な値は通常、CPUコアの数までです。
> -   バイトの場合、安全な値は通常、システムメモリの量よりも少なくなります。
> -   時間については、単位が秒またはミリ秒である可能性があることに注意してください。
>
> 同じユニットを使用する変数は、同じリソースのセットをめぐって競合する可能性があります。

## 変数リファレンス {#variable-reference}

### allow_auto_random_explicit_insertv4.0.3<span class="version-mark">の新機能</span> {#allow-auto-random-explicit-insert-span-class-version-mark-new-in-v4-0-3-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   `INSERT`ステートメントで`AUTO_RANDOM`属性を持つ列の値を明示的に指定できるようにするかどうかを決定します。

### auto_increment_increment {#auto-increment-increment}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1`
-   範囲： `[1, 65535]`
-   列に割り当てられる`AUTO_INCREMENT`の値のステップサイズを制御します。多くの場合、 `auto_increment_offset`と組み合わせて使用されます。

### auto_increment_offset {#auto-increment-offset}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1`
-   範囲： `[1, 65535]`
-   列に割り当てられる`AUTO_INCREMENT`の値の初期オフセットを制御します。この設定は、多くの場合`auto_increment_increment`と組み合わせて使用されます。例えば：

```sql
mysql> CREATE TABLE t1 (a int not null primary key auto_increment);
Query OK, 0 rows affected (0.10 sec)

mysql> set auto_increment_offset=1;
Query OK, 0 rows affected (0.00 sec)

mysql> set auto_increment_increment=3;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (),(),(),();
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+
| a  |
+----+
|  1 |
|  4 |
|  7 |
| 10 |
+----+
4 rows in set (0.00 sec)
```

### 自動コミット {#autocommit}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   明示的なトランザクションでないときにステートメントを自動的にコミットするかどうかを制御します。詳細については、 [取引概要](/transaction-overview.md#autocommit)を参照してください。

### block_encryption_mode {#block-encryption-mode}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `aes-128-ecb`
-   `AES_ENCRYPT()`および`AES_DECRYPT()`関数の暗号化モードを定義します。

### character_set_client {#character-set-client}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `utf8mb4`
-   クライアントから送信されるデータの文字セット。 TiDBでの文字セットと照合の使用の詳細については、 [文字セットと照合](/character-set-and-collation.md)を参照してください。必要に応じて、 [`SET NAMES`](/sql-statements/sql-statement-set-names.md)を使用して文字セットを変更することをお勧めします。

### character_set_connection {#character-set-connection}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `utf8mb4`
-   指定された文字セットを持たない文字列リテラルの文字セット。

### character_set_database {#character-set-database}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `utf8mb4`
-   この変数は、使用中のデフォルトデータベースの文字セットを示します。**この変数を設定することはお勧めしません**。新しいデフォルトデータベースが選択されると、サーバーは変数値を変更します。

### character_set_results {#character-set-results}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `utf8mb4`
-   データがクライアントに送信されるときに使用される文字セット。

### character_set_server {#character-set-server}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `utf8mb4`
-   サーバーのデフォルトの文字セット。

### collation_connection {#collation-connection}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `utf8mb4_bin`
-   この変数は、指定された照合順序を持たない文字列リテラルの照合順序を示します。

### collation_database {#collation-database}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `utf8mb4_bin`
-   この変数は、使用中のデフォルトデータベースの照合順序を示します。**この変数を設定することはお勧めしません**。新しいデフォルトデータベースが選択されると、サーバーは変数値を変更します。

### collation_server {#collation-server}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `utf8mb4_bin`
-   サーバーのデフォルトの照合順序。

### cte_max_recursion_depth {#cte-max-recursion-depth}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1000`
-   範囲： `[0, 4294967295]`
-   共通テーブル式の最大再帰深度を制御します。

### datadir {#datadir}

-   スコープ：なし
-   デフォルト値：/ tmp / tidb
-   この変数は、データが保存される場所を示します。データがTiKVに保存されている場合、この場所はローカルパスにすることも、PDサーバーを指すこともできます。
-   `ip_address:port`の形式の値は、起動時にTiDBが接続するPDサーバーを示します。

### ddl_slow_threshold {#ddl-slow-threshold}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   デフォルト値： `300`
-   単位：ミリ秒
-   実行時間がしきい値を超えるDDL操作をログに記録します。

### default_authentication_plugin {#default-authentication-plugin}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `mysql_native_password`
-   可能な`caching_sha2_password` ： `mysql_native_password`
-   この変数は、サーバーとクライアントの接続が確立されているときにサーバーがアドバタイズする認証方法を設定します。この変数の可能な値は[認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status)に記載されています。
-   値のオプション： `mysql_native_password`および`caching_sha2_password` 。詳細については、 [認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status)を参照してください。

### default_week_format {#default-week-format}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 7]`
-   `WEEK()`関数で使用される週の形式を設定します。

### external_key_checks {#foreign-key-checks}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   互換性のために、TiDBは外部キーチェックを`OFF`として返します。

### group_concat_max_len {#group-concat-max-len}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1024`
-   範囲： `[4, 18446744073709551615]`
-   `GROUP_CONCAT()`関数のアイテムの最大バッファーサイズ。

### have_openssl {#have-openssl}

-   スコープ：なし
-   デフォルト値： `DISABLED`
-   MySQL互換性のための読み取り専用変数。サーバーでTLSが有効になっている場合、サーバーによって`YES`に設定されます。

### have_ssl {#have-ssl}

-   スコープ：なし
-   デフォルト値： `DISABLED`
-   MySQL互換性のための読み取り専用変数。サーバーでTLSが有効になっている場合、サーバーによって`YES`に設定されます。

### ホスト名 {#hostname}

-   スコープ：なし
-   デフォルト値:(システムホスト名）
-   読み取り専用変数としてのTiDBサーバーのホスト名。

### 身元 {#identity}

この変数は`last_insert_id`のエイリアスです。

### init_connect {#init-connect}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   デフォルト値： &quot;&quot;
-   `init_connect`機能を使用すると、TiDBサーバーに最初に接続したときにSQLステートメントを自動的に実行できます。 `CONNECTION_ADMIN`つまたは`SUPER`の特権がある場合、この`init_connect`のステートメントは実行されません。 `init_connect`ステートメントでエラーが発生した場合、ユーザー接続は終了します。

### innodb_lock_wait_timeout {#innodb-lock-wait-timeout}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `50`
-   範囲： `[1, 3600]`
-   単位：秒
-   悲観的トランザクションのロック待機タイムアウト（デフォルト）。

### Interactive_timeout {#interactive-timeout}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `28800`
-   範囲： `[1, 31536000]`
-   単位：秒
-   この変数は、対話型ユーザーセッションのアイドルタイムアウトを表します。インタラクティブユーザーセッションとは、 `CLIENT_INTERACTIVE`のオプション（MySQLシェルやMySQLクライアントなど）を使用して[`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html)のAPIを呼び出すことによって確立されるセッションを指します。この変数はMySQLと完全に互換性があります。

### last_insert_id {#last-insert-id}

-   スコープ：セッション
-   デフォルト値： `0`
-   この変数は、挿入ステートメントによって生成された最後の`AUTO_INCREMENT`または`AUTO_RANDOM`の値を返します。
-   `last_insert_id`の値は、関数`LAST_INSERT_ID()`によって返される値と同じです。

### last_plan_from_bindingv4.0<span class="version-mark">の新</span>機能 {#last-plan-from-binding-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、前のステートメントで使用された実行プランが[プランバインディング](/sql-plan-management.md)の影響を受けたかどうかを示すために使用されます。

### last_plan_from_cachev4.0<span class="version-mark">の新</span>機能 {#last-plan-from-cache-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、前の`execute`ステートメントで使用された実行プランがプランキャッシュから直接取得されたかどうかを示すために使用されます。

### ライセンス {#license}

-   スコープ：なし
-   デフォルト値： `Apache License 2.0`
-   この変数は、TiDBサーバーインストールのライセンスを示します。

### log_bin {#log-bin}

-   スコープ：なし
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)が使用されているかどうかを示します。

### max_allowed_packet {#max-allowed-packet}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `67108864`
-   範囲： `[1024, 1073741824]`
-   単位：バイト
-   MySQLプロトコルのパケットの最大サイズ。

### max_execution_time {#max-execution-time}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 2147483647]`
-   単位：ミリ秒
-   ステートメントの最大実行時間。デフォルト値は無制限（ゼロ）です。

> **ノート：**
>
> MySQLとは異なり、 `max_execution_time`システム変数は現在、 `SELECT`ステートメントに限定されるだけでなく、TiDBのすべての種類のステートメントで機能します。タイムアウト値の精度は約100msです。これは、指定したとおりにステートメントが正確なミリ秒で終了しない可能性があることを意味します。

### plugin_dir {#plugin-dir}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   デフォルト値： &quot;&quot;
-   コマンドラインフラグで指定されたプラグインをロードするディレクトリを示します。

### plugin_load {#plugin-load}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   デフォルト値： &quot;&quot;
-   TiDBの起動時にロードするプラグインを示します。これらのプラグインは、コマンドラインフラグで指定され、コンマで区切られます。

### ポート {#port}

-   スコープ：なし
-   タイプ：整数
-   デフォルト値： `4000`
-   範囲： `[0, 65535]`
-   MySQLプロトコルを話すときに`tidb-server`がリッスンしているポート。

### rand_seed1 {#rand-seed1}

-   スコープ：セッション
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 2147483647]`
-   この変数は、 `RAND()`関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作はMySQLと互換性があります。

### rand_seed2 {#rand-seed2}

-   スコープ：セッション
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 2147483647]`
-   この変数は、 `RAND()`関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作はMySQLと互換性があります。

### require_secure_transportv6.1.0<span class="version-mark">の新機能</span> {#require-secure-transport-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、TiDBへのすべての接続がローカルソケット上にあるか、TLSを使用していることを保証します。詳細については、 [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)を参照してください。
-   この変数を`ON`に設定するには、TLSが有効になっているセッションからTiDBに接続する必要があります。これは、TLSが正しく構成されていない場合のロックアウトシナリオを防ぐのに役立ちます。
-   この設定は、以前は`tidb.toml`オプション（ `security.require-secure-transport` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。

### skip_name_resolvev5.2.0<span class="version-mark">の新機能</span> {#skip-name-resolve-span-class-version-mark-new-in-v5-2-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 `tidb-server`つのインスタンスが接続ハンドシェイクの一部としてホスト名を解決するかどうかを制御します。
-   DNSの信頼性が低い場合は、このオプションを有効にしてネットワークパフォーマンスを向上させることができます。

> **ノート：**
>
> `skip_name_resolve=ON`の場合、IDにホスト名が含まれるユーザーはサーバーにログインできなくなります。例えば：
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> この例では、 `apphost`をIPアドレスまたはワイルドカード（ `%` ）に置き換えることをお勧めします。

### ソケット {#socket}

-   スコープ：なし
-   デフォルト値： &quot;&quot;
-   MySQLプロトコルを話すときに`tidb-server`がリッスンしているローカルUNIXソケットファイル。

### sql_log_bin {#sql-log-bin}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   変更を[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)に書き込むかどうかを示します。

> **ノート：**
>
> `sql_log_bin`をグローバル変数として設定することはお勧めしません。これは、TiDBの将来のバージョンでは、これをセッション変数としてのみ設定できる可能性があるためです。

### sql_mode {#sql-mode}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
-   この変数は、MySQLの互換性動作の数を制御します。詳細については、 [SQLモード](/sql-mode.md)を参照してください。

### sql_select_limitv4.0.2<span class="version-mark">の新機能</span> {#sql-select-limit-span-class-version-mark-new-in-v4-0-2-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `18446744073709551615`
-   範囲： `[0, 18446744073709551615]`
-   単位：行
-   `SELECT`ステートメントによって返される行の最大数。

### ssl_ca {#ssl-ca}

-   スコープ：なし
-   デフォルト値： &quot;&quot;
-   認証局ファイルの場所（存在する場合）。

### ssl_cert {#ssl-cert}

-   スコープ：なし
-   デフォルト値： &quot;&quot;
-   SSL / TLS接続に使用される証明書ファイル（ファイルがある場合）の場所。

### ssl_key {#ssl-key}

-   スコープ：なし
-   デフォルト値： &quot;&quot;
-   SSL / TLS接続に使用される秘密鍵ファイル（存在する場合）の場所。

### system_time_zone {#system-time-zone}

-   スコープ：なし
-   デフォルト値:(システムに依存）
-   この変数は、TiDBが最初にブートストラップされたときからのシステムタイムゾーンを示します。 [`time_zone`](#time_zone)も参照してください。

### tidb_allow_batch_copv4.0<span class="version-mark">の新</span>機能 {#tidb-allow-batch-cop-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1`
-   範囲： `[0, 2]`
-   この変数は、TiDBがコプロセッサー要求をTiFlashに送信する方法を制御するために使用されます。次の値があります。

    -   `0` ：リクエストをバッチで送信しない
    -   `1` ：集計および結合要求はバッチで送信されます
    -   `2` ：すべてのコプロセッサー要求はバッチで送信されます

### tidb_allow_fallback_to_tikvv5.0<span class="version-mark">の新</span>機能 {#tidb-allow-fallback-to-tikv-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： &quot;&quot;
-   この変数は、TiKVにフォールバックする可能性のあるストレージエンジンのリストを指定するために使用されます。リスト内の指定されたストレージエンジンの障害が原因でSQLステートメントの実行が失敗した場合、TiDBはTiKVを使用してこのSQLステートメントの実行を再試行します。この変数は、「」または「tiflash」に設定できます。この変数が「tiflash」に設定されている場合、TiFlashがタイムアウトエラー（エラーコード：ErrTiFlashServerTimeout）を返すと、TiDBはTiKVを使用してこのSQLステートメントの実行を再試行します。

### tidb_allow_function_for_expression_indexv5.2.0<span class="version-mark">の新機能</span> {#tidb-allow-function-for-expression-index-span-class-version-mark-new-in-v5-2-0-span}

-   スコープ：なし
-   デフォルト値： `lower, md5, reverse, tidb_shard, upper, vitess_hash`
-   この変数は、式インデックスの作成に使用できる関数を示すために使用されます。

### tidb_allow_mppv5.0<span class="version-mark">の新</span>機能 {#tidb-allow-mpp-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   TiFlashのMPPモードを使用してクエリを実行するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF`これは、MPPモードが使用されないことを意味します。
    -   `1`または`ON`これは、オプティマイザがコスト見積もりに基づいてMPPモードを使用するかどうかを決定することを意味します（デフォルト）。

MPPは、TiFlashエンジンによって提供される分散コンピューティングフレームワークであり、ノード間のデータ交換を可能にし、高性能、高スループットのSQLアルゴリズムを提供します。 MPPモードの選択の詳細については、 [MPPモードを選択するかどうかを制御します](/tiflash/use-tiflash.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_allow_remove_auto_incv2.1.18<span class="version-mark">およびv3.0.4の新機能</span> {#tidb-allow-remove-auto-inc-span-class-version-mark-new-in-v2-1-18-and-v3-0-4-span}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 `ALTER TABLE MODIFY`つまたは`ALTER TABLE CHANGE`のステートメントを実行して列の`AUTO_INCREMENT`のプロパティを削除できるかどうかを設定するために使用されます。デフォルトでは許可されていません。

### tidb_analyze_versionv5.1.0<span class="version-mark">の新機能</span> {#tidb-analyze-version-span-class-version-mark-new-in-v5-1-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `2`
-   範囲： `[1, 2]`
-   TiDBが統計を収集する方法を制御します。
-   v5.3.0以降のバージョンでは、この変数のデフォルト値は`2`であり、これは実験的機能として機能します。クラスタがv5.3.0より前のバージョンからv5.3.0以降にアップグレードされた場合、デフォルト値の`tidb_analyze_version`は変更されません。詳細な紹介については、 [統計入門](/statistics.md)を参照してください。

### tidb_auto_analyze_end_time {#tidb-auto-analyze-end-time}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：時間
-   デフォルト値： `23:59 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、午前1時から午前3時までの統計の自動更新のみを許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`を設定します。

### tidb_auto_analyze_ratio {#tidb-auto-analyze-ratio}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：フロート
-   デフォルト値： `0.5`
-   範囲： `[0, 18446744073709551615]`
-   この変数は、TiDBがバックグラウンドスレッドで[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)を自動的に実行してテーブル統計を更新するときのしきい値を設定するために使用されます。たとえば、値0.5は、テーブルの行の50％以上が変更されたときに自動分析がトリガーされることを意味します。自動分析は、 `tidb_auto_analyze_start_time`と`tidb_auto_analyze_end_time`を指定することにより、1日の特定の時間帯にのみ実行するように制限できます。

> **ノート：**
>
> この機能では、システム変数`tidb_enable_auto_analyze`を`ON`に設定する必要があります。

### tidb_auto_analyze_start_time {#tidb-auto-analyze-start-time}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：時間
-   デフォルト値： `00:00 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、午前1時から午前3時までの統計の自動更新のみを許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`を設定します。

### <code>tidb_max_auto_analyze_time</code><span class="version-mark">の新機能</span> {#code-tidb-max-auto-analyze-time-code-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   デフォルト値： `43200`
-   範囲： `[0, 2147483647]`
-   単位：秒
-   この変数は、自動`ANALYZE`タスクの最大実行時間を指定するために使用されます。自動`ANALYZE`タスクの実行時間が指定時間を超えると、タスクは終了します。この変数の値が`0`の場合、自動`ANALYZE`タスクの最大実行時間に制限はありません。

### tidb_backoff_lock_fast {#tidb-backoff-lock-fast}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `10`
-   範囲： `[1, 2147483647]`
-   この変数は、読み取り要求がロックに遭遇したときの`backoff`回を設定するために使用されます。

### tidb_backoff_weight {#tidb-backoff-weight}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `2`
-   範囲： `[0, 2147483647]`
-   この変数は、TiDB `backoff`の最大時間、つまり、内部ネットワークまたは他のコンポーネント（TiKV、PD）の障害が発生したときに再試行要求を送信するための最大再試行時間の重みを増やすために使用されます。この変数は、最大再試行時間を調整するために使用でき、最小値は1です。

    たとえば、TiDBがPDからTSOを取得するための基本タイムアウトは15秒です。 `tidb_backoff_weight = 2`の場合、TSOを取得するための最大タイムアウトは次のとおりです。*基本時間* 2=30秒*。

    ネットワーク環境が悪い場合、この変数の値を適切に増やすと、タイムアウトによって引き起こされるアプリケーション側へのエラー報告を効果的に軽減できます。アプリケーション側がエラー情報をより迅速に受信したい場合は、この変数の値を最小化します。

### tidb_broadcast_join_threshold_countv5.0<span class="version-mark">の新</span>機能 {#tidb-broadcast-join-threshold-count-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `10240`
-   範囲： `[0, 9223372036854775807]`
-   単位：行
-   結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリ結果セットのサイズを見積もることができません。この状況では、サイズは結果セットの行数によって決まります。サブクエリの推定行数がこの変数の値よりも少ない場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。

### tidb_broadcast_join_threshold_sizev5.0<span class="version-mark">の新</span>機能 {#tidb-broadcast-join-threshold-size-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `104857600` （100 MiB）
-   範囲： `[0, 9223372036854775807]`
-   単位：バイト
-   テーブルサイズが変数の値よりも小さい場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。

### tidb_build_stats_concurrency {#tidb-build-stats-concurrency}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `4`
-   単位：スレッド
-   この変数は、 `ANALYZE`ステートメントの実行の同時実行性を設定するために使用されます。
-   変数をより大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_capture_plan_baselinesv4.0<span class="version-mark">の新</span>機能 {#tidb-capture-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 [ベースラインキャプチャ](/sql-plan-management.md#baseline-capturing)機能を有効にするかどうかを制御するために使用されます。この機能はステートメントの要約に依存するため、ベースラインキャプチャを使用する前に、ステートメントの要約を有効にする必要があります。
-   この機能を有効にすると、ステートメントの要約内の履歴SQLステートメントが定期的にトラバースされ、少なくとも2回出現するSQLステートメントのバインディングが自動的に作成されます。

### tidb_check_mb4_value_in_utf8 {#tidb-check-mb4-value-in-utf8}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、 `utf8`文字セットが[基本的な多言語平面（BMP）](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane)からの値のみを格納するように強制するために使用されます。 BMPの外部に文字を格納するには、 `utf8mb4`文字セットを使用することをお勧めします。
-   `utf8`のチェックがより緩和された以前のバージョンのTiDBからクラスタをアップグレードする場合は、このオプションを無効にする必要がある場合があります。詳細については、 [アップグレード後のよくある質問](/faq/upgrade-faq.md)を参照してください。

### tidb_checksum_table_concurrency {#tidb-checksum-table-concurrency}

-   スコープ：セッション
-   デフォルト値： `4`
-   単位：スレッド
-   この変数は、 `ADMIN CHECKSUM TABLE`ステートメントを実行するスキャンインデックスの同時実行性を設定するために使用されます。
-   変数をより大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_committer_concurrencyv6.1.0<span class="version-mark">の新機能</span> {#tidb-committer-concurrency-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `128`
-   範囲： `[1, 10000]`
-   単一トランザクションのコミットフェーズでのコミットの実行に関連するリクエストのゴルーチンの数。
-   コミットするトランザクションが大きすぎる場合、トランザクションがコミットされるときのフロー制御キューの待機時間が長すぎる可能性があります。この状況では、構成値を増やしてコミットを高速化できます。
-   この設定は、以前は`tidb.toml`オプション（ `performance.committer-concurrency` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。

### tidb_config {#tidb-config}

-   スコープ：セッション
-   デフォルト値： &quot;&quot;
-   この変数は読み取り専用です。現在のTiDBサーバーの構成情報を取得するために使用されます。

### tidb_constraint_check_in_place {#tidb-constraint-check-in-place}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この設定は、楽観的なトランザクションにのみ適用されます。この変数が`OFF`に設定されている場合、UNIQUEインデックスの重複値のチェックは、トランザクションがコミットされるまで延期されます。これはパフォーマンスの向上に役立ちますが、一部のアプリケーションでは予期しない動作になる可能性があります。詳細については、 [制約](/constraints.md)を参照してください。

    -   ゼロに設定され、楽観的なトランザクションを使用する場合：

        ```sql
        tidb> create table t (i int key);
        tidb> insert into t values (1);
        tidb> begin optimistic;
        tidb> insert into t values (1);
        Query OK, 1 row affected
        tidb> commit; -- Check only when a transaction is committed.
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

    -   1に設定し、楽観的なトランザクションを使用する場合：

        ```sql
        tidb> set @@tidb_constraint_check_in_place=1;
        tidb> begin optimistic;
        tidb> insert into t values (1);
        ERROR 1062 : Duplicate entry '1' for key 'PRIMARY'
        ```

制約チェックは、悲観的なトランザクションに対して常に実行されます（デフォルト）。

### tidb_current_ts {#tidb-current-ts}

-   スコープ：セッション
-   デフォルト値： `0`
-   この変数は読み取り専用です。現在のトランザクションのタイムスタンプを取得するために使用されます。

### tidb_ddl_error_count_limit {#tidb-ddl-error-count-limit}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `512`
-   範囲： `[0, 9223372036854775807]`
-   この変数は、DDL操作が失敗したときの再試行回数を設定するために使用されます。再試行回数がパラメータ値を超えると、誤ったDDL操作がキャンセルされます。

### tidb_ddl_reorg_batch_size {#tidb-ddl-reorg-batch-size}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `256`
-   範囲： `[32, 10240]`
-   単位：行
-   この変数は、DDL操作の`re-organize`フェーズでバッチサイズを設定するために使用されます。たとえば、TiDBが`ADD INDEX`の操作を実行する場合、インデックスデータは`tidb_ddl_reorg_worker_cnt` （数）の同時ワーカーによって埋め戻される必要があります。各ワーカーは、インデックスデータをバッチで埋め戻します。
    -   `ADD INDEX`操作中に`UPDATE`や`REPLACE`などの更新操作が多数存在する場合、バッチサイズが大きいほど、トランザクションが競合する可能性が高くなります。この場合、バッチサイズを小さい値に調整する必要があります。最小値は32です。
    -   トランザクションの競合が存在しない場合は、バッチサイズを大きな値に設定できます（ワーカー数を考慮してください。参照については[オンラインワークロードと`ADD INDEX`操作の相互作用テスト](/benchmark/online-workloads-and-add-index-operations.md)を参照してください）。これにより、データの埋め戻し速度を上げることができますが、TiKVへの書き込み圧力も高くなります。

### tidb_ddl_reorg_priority {#tidb-ddl-reorg-priority}

-   スコープ：セッション
-   デフォルト値： `PRIORITY_LOW`
-   この変数は、 `re-organize`フェーズで`ADD INDEX`操作を実行する優先順位を設定するために使用されます。
-   この変数の値は、 `PRIORITY_LOW` 、または`PRIORITY_NORMAL`に設定でき`PRIORITY_HIGH` 。

### tidb_ddl_reorg_worker_cnt {#tidb-ddl-reorg-worker-cnt}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `4`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、 `re-organize`フェーズでのDDL操作の同時実行性を設定するために使用されます。

### tidb_disable_txn_auto_retry {#tidb-disable-txn-auto-retry}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、明示的なオプティミスティックトランザクションの自動再試行を無効にするかどうかを設定するために使用されます。デフォルト値の`ON`は、トランザクションがTiDBで自動的に再試行せず、 `COMMIT`のステートメントがアプリケーション層で処理する必要のあるエラーを返す可能性があることを意味します。

    値を`OFF`に設定すると、TiDBが自動的にトランザクションを再試行し、 `COMMIT`のステートメントからのエラーが少なくなります。この変更を行うときは、更新が失われる可能性があるので注意してください。

    この変数は、TiDBで自動的にコミットされた暗黙のトランザクションおよび内部で実行されたトランザクションには影響しません。これらのトランザクションの最大再試行回数は、値`tidb_retry_limit`によって決まります。

    詳細については、 [再試行の制限](/optimistic-transaction.md#limits-of-retry)を参照してください。

    この変数は楽観的なトランザクションにのみ適用され、悲観的なトランザクションには適用されません。悲観的トランザクションの再試行回数は[`max_retry_count`](/tidb-configuration-file.md#max-retry-count)で制御されます。

### tidb_distsql_scan_concurrency {#tidb-distsql-scan-concurrency}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `15`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、 `scan`操作の同時実行性を設定するために使用されます。
-   OLAPシナリオでは大きな値を使用し、OLTPシナリオでは小さな値を使用します。
-   OLAPシナリオの場合、最大値はすべてのTiKVノードのCPUコアの数を超えてはなりません。
-   テーブルに多数のパーティションがある場合は、変数値を適切に減らして（スキャンするデータのサイズとスキャンの頻度によって決定される）、TiKVがメモリ不足（OOM）になるのを防ぐことができます。

### tidb_dml_batch_size {#tidb-dml-batch-size}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 2147483647]`
-   単位：行
-   この値が`0`より大きい場合、TiDBは`INSERT`や`LOAD DATA`などのステートメントをより小さなトランザクションにバッチコミットします。これにより、メモリ使用量が削減され、一括変更によって`txn-total-size-limit`に到達しないようにすることができます。
-   値`0`のみがACID準拠を提供します。これを他の値に設定すると、TiDBの原子性と分離の保証が破られます。

### tidb_enable_1pcv5.0<span class="version-mark">の新</span>機能 {#tidb-enable-1pc-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、1つのリージョンにのみ影響するトランザクションに対して1フェーズコミット機能を有効にするかどうかを指定するために使用されます。頻繁に使用される2フェーズコミットと比較して、1フェーズコミットはトランザクションコミットのレイテンシーを大幅に削減し、スループットを向上させることができます。

> **ノート：**
>
> -   デフォルト値の`ON`は、新しいクラスターにのみ適用されます。クラスタが以前のバージョンのTiDBからアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   TiDB Binlogを有効にしている場合、この変数を有効にしてもパフォーマンスは向上しません。パフォーマンスを向上させるために、代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用することをお勧めします。
> -   このパラメーターを有効にすると、1フェーズコミットがトランザクションコミットのオプションモードになるだけです。実際、トランザクションコミットの最適なモードはTiDBによって決定されます。

### tidb_enable_amend_pessimistic_txnv4.0.7<span class="version-mark">の新機能</span> {#tidb-enable-amend-pessimistic-txn-span-class-version-mark-new-in-v4-0-7-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 `AMEND TRANSACTION`機能を有効にするかどうかを制御するために使用されます。悲観的トランザクションで`AMEND TRANSACTION`の機能を有効にすると、このトランザクションに関連付けられたテーブルにDDL操作とスキーマバージョンの変更が同時に存在する場合、TiDBはトランザクションを修正しようとします。 TiDBは、トランザクションのコミットを修正して、コミットを最新の有効なスキーマバージョンと一致させ、 `Information schema is changed`エラーが発生することなくトランザクションを正常にコミットできるようにします。この機能は、次の同時DDL操作で有効です。

    -   `ADD COLUMN`または`DROP COLUMN`の操作。
    -   フィールドの長さを増やす`MODIFY COLUMN`または`CHANGE COLUMN`の操作。
    -   トランザクションが開かれる前にインデックス列が作成される`ADD INDEX`または`DROP INDEX`の操作。

> **ノート：**
>
> 現在、この機能は一部のシナリオではTiDB Binlogと互換性がなく、トランザクションでセマンティック変更を引き起こす可能性があります。この機能のその他の使用上の注意については、 [トランザクションセマンティックに関する非互換性の問題](https://github.com/pingcap/tidb/issues/21069)および[TiDBBinlogに関する非互換性の問題](https://github.com/pingcap/tidb/issues/20996)を参照してください。

### tidb_enable_async_commitv5.0<span class="version-mark">の新</span>機能 {#tidb-enable-async-commit-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、2フェーズトランザクションコミットの第2フェーズで非同期コミット機能を有効にしてバックグラウンドで非同期に実行するかどうかを制御します。この機能を有効にすると、トランザクションコミットの待ち時間を短縮できます。

> **ノート：**
>
> -   デフォルト値の`ON`は、新しいクラスターにのみ適用されます。クラスタが以前のバージョンのTiDBからアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   TiDB Binlogを有効にしている場合、この変数を有効にしてもパフォーマンスは向上しません。パフォーマンスを向上させるために、代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用することをお勧めします。
> -   このパラメーターを有効にすることは、非同期コミットがトランザクションコミットのオプションモードになることを意味するだけです。実際、トランザクションコミットの最適なモードはTiDBによって決定されます。

### tidb_enable_auto_analyzev6.1.0<span class="version-mark">の新機能</span> {#tidb-enable-auto-analyze-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   TiDBがバックグラウンド操作としてテーブル統計を自動的に更新するかどうかを決定します。
-   この設定は、以前は`tidb.toml`オプション（ `performance.run-auto-analyze` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。

### tidb_enable_auto_increment_in_generated {#tidb-enable-auto-increment-in-generated}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、生成された列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定するために使用されます。

### tidb_enable_change_multi_schema {#tidb-enable-change-multi-schema}

> **警告：**
>
> TiDBは、将来、より多くの種類のマルチスキーマ変更をサポートする予定です。このシステム変数は、TiDBの将来のリリースで削除される予定です。

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 `ALTER TABLE`つのステートメントで複数の列またはインデックスを変更できるかどうかを制御するために使用されます。この変数の値が`ON`の場合、次のマルチスキーマ変更のみがサポートされます。
    -   複数の列を追加します。たとえば、 `ATLER TABLE t ADD COLUMN c1 INT, ADD COLUMN c2 INT;` 。
    -   複数の列を削除します。たとえば、 `ATLER TABLE t DROP COLUMN c1, DROP COLUMN c2;` 。
    -   複数のインデックスを削除します。たとえば、 `ATLER TABLE t DROP INDEX i1, DROP INDEX i2;` 。
    -   単一列のインデックスでカバーされている列を削除します。たとえば、スキーマに`INDEX idx(c1)`が含まれている`ALTER TABLE t DROP COLUMN c1` 。

### tidb_enable_cascades_planner {#tidb-enable-cascades-planner}

> **警告：**
>
> 現在、カスケードプランナーは実験的機能です。実稼働環境で使用することはお勧めしません。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、カスケードプランナーを有効にするかどうかを制御するために使用されます。

### tidb_enable_chunk_rpcv4.0<span class="version-mark">の新</span>機能 {#tidb-enable-chunk-rpc-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、コプロセッサーで`Chunk`データエンコード形式を有効にするかどうかを制御するために使用されます。

### tidb_enable_clustered_indexv5.0<span class="version-mark">の新</span>機能 {#tidb-enable-clustered-index-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `INT_ONLY`
-   可能な`ON` `INT_ONLY` `OFF`
-   この変数は、デフォルトで主キーを[クラスター化されたインデックス](/clustered-indexes.md)として作成するかどうかを制御するために使用されます。ここでの「デフォルト」とは、ステートメントがキーワード`CLUSTERED`を明示的に指定していないことを意味し`NONCLUSTERED` 。サポートされている値は`OFF` 、および`ON` `INT_ONLY` 。
    -   `OFF`は、主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
    -   `ON`は、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
    -   `INT_ONLY`は、動作が構成項目`alter-primary-key`によって制御されていることを示します。 `alter-primary-key`が`true`に設定されている場合、すべての主キーはデフォルトで非クラスター化インデックスとして作成されます。 `false`に設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

### tidb_enable_collect_execution_info {#tidb-enable-collect-execution-info}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、各オペレーターの実行情報を低速クエリログに記録するかどうかを制御します。

### tidb_enable_column_trackingv5.4.0<span class="version-mark">の新機能</span> {#tidb-enable-column-tracking-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、 `PREDICATE COLUMNS`に関する統計の収集は実験的機能です。実稼働環境で使用することはお勧めしません。

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、TiDBが`PREDICATE COLUMNS`を収集できるようにするかどうかを制御します。収集を有効にした後、無効にすると、以前に収集した`PREDICATE COLUMNS`の情報が消去されます。詳細については、 [一部の列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)を参照してください。

### tidb_enable_enhanced_security {#tidb-enable-enhanced-security}

-   スコープ：なし
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、接続しているTiDBサーバーでセキュリティ拡張モード（SEM）が有効になっているかどうかを示します。その値を変更するには、TiDBサーバー構成ファイルの値`enable-sem`を変更し、TiDBサーバーを再起動する必要があります。
-   SEMは、 [セキュリティが強化されたLinux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux)などのシステムの設計に触発されています。これにより、MySQL `SUPER`特権を持つユーザーの能力が低下し、代わりに`RESTRICTED`つのきめ細かい特権を付与する必要があります。これらのきめ細かい特権には、次のものが含まれます。
    -   `RESTRICTED_TABLES_ADMIN` ： `mysql`のスキーマのシステムテーブルにデータを書き込み、 `information_schema`のテーブルの機密列を表示する機能。
    -   `RESTRICTED_STATUS_ADMIN` ：コマンド`SHOW STATUS`で機密変数を表示する機能。
    -   `RESTRICTED_VARIABLES_ADMIN` ： `SHOW [GLOBAL] VARIABLES`と`SET`の機密変数を表示および設定する機能。
    -   `RESTRICTED_USER_ADMIN` ：他のユーザーがユーザーアカウントを変更または削除できないようにする機能。

### tidb_enable_fast_analyze {#tidb-enable-fast-analyze}

> **警告：**
>
> 現在、 `Fast Analyze`は実験的機能です。実稼働環境で使用することはお勧めしません。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、統計`Fast Analyze`機能を有効にするかどうかを設定するために使用されます。
-   統計`Fast Analyze`機能が有効になっている場合、TiDBは約10,000行のデータを統計としてランダムにサンプリングします。データが不均一に分布している場合やデータサイズが小さい場合、統計の精度は低くなります。これにより、たとえば、間違ったインデックスを選択するなど、最適でない実行プランが発生する可能性があります。通常の`Analyze`ステートメントの実行時間が許容できる場合は、 `Fast Analyze`機能を無効にすることをお勧めします。

### tidb_enable_index_mergev4.0<span class="version-mark">の新</span>機能 {#tidb-enable-index-merge-span-class-version-mark-new-in-v4-0-span}

> **ノート：**
>
> -   TiDBクラスタをv4.0.0より前のバージョンからv5.4.0以降にアップグレードした後、実行プランの変更によるパフォーマンスの低下を防ぐために、この変数はデフォルトで無効になっています。
>
> -   TiDBクラスタをv4.0.0以降からv5.4.0以降にアップグレードした後、この変数はアップグレード前の設定のままです。
>
> -   v5.4.0以降、新しくデプロイされたTiDBクラスタの場合、この変数はデフォルトで有効になっています。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、インデックスマージ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_legacy_instance_scopev6.0.0<span class="version-mark">の新機能</span> {#tidb-enable-legacy-instance-scope-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数を使用すると、 `SET SESSION`構文と`SET GLOBAL`構文を使用して`INSTANCE`のスコープ変数を設定できます。
-   このオプションは、以前のバージョンのTiDBとの互換性のためにデフォルトで有効になっています。

### tidb_enable_list_partitionv5.0<span class="version-mark">の新</span>機能 {#tidb-enable-list-partition-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、 `LIST (COLUMNS) TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。

### tidb_enable_mutation_checkerv6.0.0<span class="version-mark">の新機能</span> {#tidb-enable-mutation-checker-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、DMLステートメントの実行中にデータとインデックス間の整合性をチェックするために使用されるツールであるTiDBミューテーションチェッカーを有効にするかどうかを制御するために使用されます。チェッカーがステートメントに対してエラーを返した場合、TiDBはステートメントの実行をロールバックします。この変数を有効にすると、CPU使用率がわずかに増加します。詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)を参照してください。
-   v6.0.0以降のバージョンの新しいクラスターの場合、デフォルト値は`ON`です。 v6.0.0より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_enable_new_only_full_group_by_checkv6.1.0<span class="version-mark">の新機能</span> {#tidb-enable-new-only-full-group-by-check-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `OFF`
-   値のオプション： `OFF`および`ON`
-   この変数は、TiDBが`ONLY_FULL_GOUP_BY`チェックを実行するときの動作を制御します。 `ONLY_FULL_GROUP_BY`の詳細については、 [MySQLドキュメント](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)を参照してください。 v6.1.0では、TiDBはこのチェックをより厳密かつ正確に処理します。
-   バージョンのアップグレードによって引き起こされる潜在的な互換性の問題を回避するために、この変数のデフォルト値はv6.1.0では`OFF`です。

### tidb_enable_noop_functionsv4.0<span class="version-mark">の新</span>機能 {#tidb-enable-noop-functions-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `OFF`
-   可能な`ON` `WARN` `OFF`
-   デフォルトでは、まだ実装されていない機能の構文を使用しようとすると、TiDBはエラーを返します。変数値が`ON`に設定されている場合、TiDBはこのような機能が利用できない場合を黙って無視します。これは、SQLコードに変更を加えることができない場合に役立ちます。
-   `noop`の機能を有効にすると、次の動作が制御されます。
    -   `LOCK IN SHARE MODE`構文
    -   `SQL_CALC_FOUND_ROWS`構文
    -   `START TRANSACTION READ ONLY`および`SET TRANSACTION READ ONLY`構文
    -   `tx_read_only` `read_only` `offline_mode` `transaction_read_only` `sql_auto_is_null`システム`super_read_only`
    -   `GROUP BY <expr> ASC|DESC`構文

> **警告：**
>
> 安全と見なすことができるのは、デフォルト値の`OFF`のみです。 `tidb_enable_noop_functions=1`を設定すると、TiDBがエラーを提供せずに特定の構文を無視できるため、アプリケーションで予期しない動作が発生する可能性があります。たとえば、構文`START TRANSACTION READ ONLY`は許可されていますが、トランザクションは読み取り/書き込みモードのままです。

### tidb_enable_outer_join_reorderv6.1.0<span class="version-mark">の新機能</span> {#tidb-enable-outer-join-reorder-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `ON`
-   v6.1.0以降、TiDBの[結合したテーブルの再配置](/join-reorder.md)アルゴリズムは外部結合をサポートしています。この変数はサポート動作を制御し、デフォルト値は`ON`です。
-   v6.1.0より前のバージョンからアップグレードされたクラスタの場合、デフォルト値は`TRUE`のままです。

### tidb_enable_pagingv5.4.0<span class="version-mark">の新機能</span> {#tidb-enable-paging-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、ページングの方法を使用して`IndexLookUp`のオペレーターでコプロセッサー要求を送信するかどうかを制御します。
-   ユーザーシナリオ： `IndexLookup`と`Limit`を使用し、 `Limit`を`IndexScan`にプッシュダウンできない読み取りクエリの場合、読み取りクエリの待機時間が長くなり、TiKVの`unified read pool`のCPU使用率が高くなる可能性があります。このような場合、 `Limit`演算子は少数のデータセットしか必要としないため、 `tidb_enable_paging`を`ON`に設定すると、TiDBが処理するデータが少なくなり、クエリの待機時間とリソース消費が削減されます。
-   `tidb_enable_paging`が有効になっている場合、プッシュダウンできず`960`未満の`Limit`の`IndexLookUp`の要求に対して、TiDBはページングの方法を使用してコプロセッサー要求を送信します。 `Limit`が少ないほど、最適化はより明白になります。

### tidb_enable_parallel_applyv5.0<span class="version-mark">の新</span>機能 {#tidb-enable-parallel-apply-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 `Apply`演算子の同時実行を有効にするかどうかを制御します。同時実行の数は、 `tidb_executor_concurrency`の変数によって制御されます。 `Apply`オペレーターは相関サブクエリを処理し、デフォルトでは同時実行性がないため、実行速度が遅くなります。この変数値を`1`に設定すると、同時実行性が向上し、実行が高速化されます。現在、 `Apply`の同時実行はデフォルトで無効になっています。

### tidb_enable_prepared_plan_cachev6.1.0<span class="version-mark">の新機能</span> {#tidb-enable-prepared-plan-cache-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   [準備された計画キャッシュ](/sql-prepared-plan-cache.md)を有効にするかどうかを決定します。有効にすると、 `Prepare`と`Execute`の実行プランがキャッシュされるため、後続の実行では実行プランの最適化がスキップされ、パフォーマンスが向上します。
-   この設定は、以前は`tidb.toml`オプション（ `prepared-plan-cache.enabled` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。

### tidb_enable_pseudo_for_outdated_statsv5.3.0<span class="version-mark">の新機能</span> {#tidb-enable-pseudo-for-outdated-stats-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、統計が古くなったときにテーブルの統計を使用する際のオプティマイザーの動作を制御します。
-   オプティマイザは、この方法でテーブルの統計が古くなっているかどうかを判断します。統計を取得するためにテーブルで最後に`ANALYZE`が実行されてから、テーブルの行の80％が変更された場合（変更された行数を合計行数で割ったもの） ）、オプティマイザは、このテーブルの統計が古くなっていると判断します。この比率は、 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)の構成を使用して変更できます。
-   デフォルト（変数値`ON` ）では、テーブルの統計が古くなっている場合、オプティマイザーは、合計行数を除いて、テーブルの統計が信頼できなくなったと判断します。次に、オプティマイザは疑似統計を使用します。変数値を`OFF`に設定すると、テーブルの統計が古くなっていても、オプティマイザーは統計を使用し続けます。
-   テーブルのデータが、このテーブルで`ANALYZE`を実行せずに頻繁に変更される場合は、実行プランを安定させるために、変数値を`OFF`に設定できます。

### tidb_enable_rate_limit_action {#tidb-enable-rate-limit-action}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、データを読み取るオペレーターの動的メモリー制御機能を有効にするかどうかを制御します。デフォルトでは、この演算子は、 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)がデータの読み取りを許可するスレッドの最大数を有効にします。 1つのSQLステートメントのメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超えると、データを読み取るオペレーターが1つのスレッドを停止します。
-   データを読み取る演算子に残っているスレッドが1つだけで、単一のSQLステートメントのメモリ使用量が引き続き[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超える場合、このSQLステートメントは[データをディスクにこぼす](/tidb-configuration-file.md#oom-use-tmp-storage)などの他のメモリ制御動作をトリガーします。

### tidb_enable_slow_log {#tidb-enable-slow-log}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、スローログ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_stmt_summaryv3.0.4<span class="version-mark">の新機能</span> {#tidb-enable-stmt-summary-span-class-version-mark-new-in-v3-0-4-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、ステートメント要約機能を有効にするかどうかを制御するために使用されます。有効にすると、消費時間などのSQL実行情報が`information_schema.STATEMENTS_SUMMARY`システムテーブルに記録され、SQLパフォーマンスの問題を特定してトラブルシューティングします。

### tidb_enable_strict_double_type_checkv5.0<span class="version-mark">の新</span>機能 {#tidb-enable-strict-double-type-check-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、タイプ`DOUBLE`の無効な定義を使用してテーブルを作成できるかどうかを制御するために使用されます。この設定は、タイプの検証がそれほど厳密ではなかった以前のバージョンのTiDBからのアップグレードパスを提供することを目的としています。
-   デフォルト値の`ON`はMySQLと互換性があります。

たとえば、浮動小数点型の精度が保証されていないため、型`DOUBLE(10)`は無効と見なされるようになりました。 `tidb_enable_strict_double_type_check`を`OFF`に変更すると、テーブルが作成されます。

```sql
mysql> CREATE TABLE t1 (id int, c double(10));
ERROR 1149 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use

mysql> SET tidb_enable_strict_double_type_check = 'OFF';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE t1 (id int, c double(10));
Query OK, 0 rows affected (0.09 sec)
```

> **ノート：**
>
> MySQLでは`FLOAT`のタイプの精度が許可されているため、この設定はタイプ`DOUBLE`にのみ適用されます。この動作はMySQL8.0.17以降で非推奨になり、 `FLOAT`または`DOUBLE`タイプの精度を指定することはお勧めしません。

### tidb_enable_table_partition {#tidb-enable-table-partition}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `ON`
-   可能な`ON` `AUTO` `OFF`
-   この変数は、 `TABLE PARTITION`つの機能を有効にするかどうかを設定するために使用されます。
    -   `ON`は、1つの単一列で範囲分割、ハッシュ分割、および範囲列分割を有効にすることを示します。
    -   `AUTO`は`ON`と同じように機能します。
    -   `OFF`は、 `TABLE PARTITION`の機能を無効にすることを示します。この場合、パーティションテーブルを作成する構文を実行できますが、作成されるテーブルはパーティションテーブルではありません。

### tidb_enable_telemetryv4.0.2<span class="version-mark">の新機能</span> {#tidb-enable-telemetry-span-class-version-mark-new-in-v4-0-2-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、TiDBのテレメトリコレクションを有効にするかどうかを動的に制御するために使用されます。値を`OFF`に設定すると、テレメトリ収集が無効になります。すべての[`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)インスタンスで3TiDB構成項目が`false`に設定されている場合、テレメトリ収集は常に無効になり、このシステム変数は有効になりません。詳細については、 [テレメトリー](/telemetry.md)を参照してください。

### tidb_enable_top_sqlv5.4.0<span class="version-mark">の新機能</span> {#tidb-enable-top-sql-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、 Top SQLは実験的機能です。実稼働環境での使用はお勧めしません。

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 [Top SQL](/dashboard/top-sql.md)機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_tso_follower_proxyv5.3.0<span class="version-mark">の新機能</span> {#tidb-enable-tso-follower-proxy-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、TSOフォロワープロキシ機能を有効にするために使用されます。値が`OFF`の場合、TiDBはPDリーダーからのみTSOを取得します。この機能を有効にすると、TiDBはすべてのPDノードにリクエストを均等に送信し、PDフォロワーを介してTSOリクエストを転送することでTSOを取得します。これは、PDリーダーのCPUプレッシャーを軽減するのに役立ちます。
-   TSOフォロワープロキシを有効にするためのシナリオ：
    -   TSO要求のプレッシャーが高いため、PDリーダーのCPUがボトルネックに達し、TSORPC要求の待ち時間が長くなります。
    -   TiDBクラスタには多くのTiDBインスタンスがあり、値を[`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)に増やしても、TSORPC要求の高遅延の問題を軽減することはできません。

> **ノート：**
>
> PDリーダーのCPU使用率のボトルネック以外の理由（ネットワークの問題など）でTSORPC遅延が増加するとします。この場合、TSOフォロワープロキシを有効にすると、TiDBの実行遅延が増加し、クラスタのQPSパフォーマンスに影響を与える可能性があります。

### tidb_enable_vectorized_expressionv4.0<span class="version-mark">の新</span>機能 {#tidb-enable-vectorized-expression-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、ベクトル化された実行を有効にするかどうかを制御するために使用されます。

### tidb_enable_window_function {#tidb-enable-window-function}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、ウィンドウ関数のサポートを有効にするかどうかを制御するために使用されます。ウィンドウ関数は予約済みのキーワードを使用する場合があることに注意してください。これにより、通常実行できるSQLステートメントがTiDBのアップグレード後に解析できなくなる可能性があります。この場合、 `tidb_enable_window_function`を設定でき`OFF` 。

### tidb_enforce_mppv5.1<span class="version-mark">の新</span>機能 {#tidb-enforce-mpp-span-class-version-mark-new-in-v5-1-span}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `OFF`
-   このデフォルト値を変更するには、 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値を変更します。
-   オプティマイザのコスト見積もりを無視するかどうか、およびクエリ実行にTiFlashのMPPモードを強制的に使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF`これは、MPPモードが強制的に使用されないことを意味します（デフォルト）。
    -   `1`または`ON`は、コスト見積もりが無視され、MPPモードが強制的に使用されることを意味します。この設定は、 `tidb_allow_mpp=true`の場合にのみ有効になることに注意してください。

MPPは、TiFlashエンジンによって提供される分散コンピューティングフレームワークであり、ノード間のデータ交換を可能にし、高性能、高スループットのSQLアルゴリズムを提供します。 MPPモードの選択の詳細については、 [MPPモードを選択するかどうかを制御します](/tiflash/use-tiflash.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_evolve_plan_baselinesv4.0<span class="version-mark">の新</span>機能 {#tidb-evolve-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、ベースライン進化機能を有効にするかどうかを制御するために使用されます。詳細な紹介または使用法については、 [ベースラインの進化](/sql-plan-management.md#baseline-evolution)を参照してください。
-   クラスタに対するベースラインの進化の影響を減らすには、次の構成を使用します。
    -   各実行プランの最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`を設定します。デフォルト値は600秒です。
    -   時間枠を制限するには、 `tidb_evolve_plan_task_start_time`と`tidb_evolve_plan_task_end_time`を設定します。デフォルト値はそれぞれ`00:00 +0000`と`23:59 +0000`です。

### tidb_evolve_plan_task_end_timev4.0<span class="version-mark">の新</span>機能 {#tidb-evolve-plan-task-end-time-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：時間
-   デフォルト値： `23:59 +0000`
-   この変数は、1日のベースライン進化の終了時間を設定するために使用されます。

### tidb_evolve_plan_task_max_timev4.0<span class="version-mark">の新</span>機能 {#tidb-evolve-plan-task-max-time-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `600`
-   範囲： `[-1, 9223372036854775807]`
-   単位：秒
-   この変数は、ベースライン進化機能の各実行プランの最大実行時間を制限するために使用されます。

### tidb_evolve_plan_task_start_timev4.0<span class="version-mark">の新</span>機能 {#tidb-evolve-plan-task-start-time-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：時間
-   デフォルト値： `00:00 +0000`
-   この変数は、1日のベースライン進化の開始時間を設定するために使用されます。

### tidb_executor_concurrencyv5.0<span class="version-mark">の新</span>機能 {#tidb-executor-concurrency-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `5`
-   範囲： `[1, 256]`
-   単位：スレッド

この変数は、次のSQL演算子の同時実行性を（1つの値に）設定するために使用されます。

-   `index lookup`
-   `index lookup join`
-   `hash join`
-   `hash aggregation` （ `partial`フェーズと`final`フェーズ）
-   `window`
-   `projection`

`tidb_executor_concurrency`には、管理を容易にするために、全体として次の既存のシステム変数が組み込まれています。

-   `tidb_index_lookup_concurrency`
-   `tidb_index_lookup_join_concurrency`
-   `tidb_hash_join_concurrency`
-   `tidb_hashagg_partial_concurrency`
-   `tidb_hashagg_final_concurrency`
-   `tidb_projection_concurrency`
-   `tidb_window_concurrency`

v5.0以降でも、上記のシステム変数を個別に変更でき（非推奨の警告が返されます）、変更は対応する単一の演算子にのみ影響します。その後、 `tidb_executor_concurrency`を使用して演算子の同時実行性を変更しても、個別に変更された演算子は影響を受けません。 `tidb_executor_concurrency`を使用してすべての演算子の同時実行性を変更する場合は、上記のすべての変数の値を`-1`に設定できます。

以前のバージョンからv5.0にアップグレードされたシステムの場合、上記の変数の値を変更していない場合（つまり、 `tidb_hash_join_concurrency`の値が`5`で、残りの値が`4` ）、オペレーターの同時実行性は以前にこれらの変数は自動的に`tidb_executor_concurrency`によって管理されます。これらの変数のいずれかを変更した場合でも、対応する演算子の並行性は変更された変数によって制御されます。

### tidb_expensive_query_time_threshold {#tidb-expensive-query-time-threshold}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：整数
-   デフォルト値： `60`
-   範囲： `[10, 2147483647]`
-   単位：秒
-   この変数は、高価なクエリログを印刷するかどうかを決定するしきい値を設定するために使用されます。高価なクエリログと遅いクエリログの違いは次のとおりです。
    -   ステートメントの実行後、遅いログが出力されます。
    -   高価なクエリログは、実行時間がしきい値を超えた状態で実行されているステートメントとその関連情報を出力します。

### tidb_force_priority {#tidb-force-priority}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   デフォルト値： `NO_PRIORITY`
-   この変数は、TiDBサーバーで実行されるステートメントのデフォルトの優先度を変更するために使用されます。ユースケースは、OLAPクエリを実行している特定のユーザーがOLTPクエリを実行しているユーザーよりも低い優先度を確実に受け取るようにすることです。
-   この変数の`LOW_PRIORITY`は、 `NO_PRIORITY` 、または`HIGH_PRIORITY`に設定でき`DELAYED` 。

### tidb_gc_concurrencyv5.0<span class="version-mark">の新</span>機能 {#tidb-gc-concurrency-span-class-version-mark-new-in-v5-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `-1`
-   範囲： `[1, 256]`
-   単位：スレッド
-   GCの[ロックを解決する](/garbage-collection-overview.md#resolve-locks)ステップのスレッド数を指定します。値`-1`は、TiDBが使用するガベージコレクションスレッドの数を自動的に決定することを意味します。

### tidb_gc_enablev5.0<span class="version-mark">の新</span>機能 {#tidb-gc-enable-span-class-version-mark-new-in-v5-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   TiKVのガベージコレクションを有効にします。ガベージコレクションを無効にすると、古いバージョンの行が削除されなくなるため、システムパフォーマンスが低下します。

### tidb_gc_life_timev5.0<span class="version-mark">の新</span>機能 {#tidb-gc-life-time-span-class-version-mark-new-in-v5-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：期間
-   デフォルト値： `10m0s`
-   範囲： `[10m0s, 8760h0m0s]`
-   GoDurationの形式で各GCのデータが保持される時間制限。 GCが発生した場合、現在の時刻からこの値を引いた値が安全なポイントです。

> **ノート：**
>
> -   頻繁に更新されるシナリオでは、 `tidb_gc_life_time`の値が大きい（数日または数か月）と、次のような潜在的な問題が発生する可能性があります。
>     -   より大きなストレージの使用
>     -   大量の履歴データは、特に`select count(*) from t`などの範囲クエリの場合、パフォーマンスにある程度影響を与える可能性があります。
> -   `tidb_gc_life_time`より長く実行されているトランザクションがある場合、GC中に、このトランザクションが実行を継続するために`start_ts`以降のデータが保持されます。たとえば、 `tidb_gc_life_time`が10分に設定されている場合、実行されているすべてのトランザクションの中で、最も早く開始されたトランザクションが15分間実行され、GCは最近の15分のデータを保持します。

### tidb_gc_max_wait_timev6.1.0<span class="version-mark">の新機能</span> {#tidb-gc-max-wait-time-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   デフォルト値： `86400`
-   範囲： `[600, 31536000]`
-   単位：秒
-   この変数は、アクティブなトランザクションがGCセーフポイントをブロックする最大時間を設定するために使用されます。 GCの各時間中、セーフポイントはデフォルトで進行中のトランザクションの開始時間を超えません。アクティブなトランザクションの実行時間がこの変数値を超えない場合、実行時間がこの値を超えるまで、GCセーフポイントはブロックされます。この変数値は整数型です。

### tidb_gc_run_intervalv5.0<span class="version-mark">の新</span>機能 {#tidb-gc-run-interval-span-class-version-mark-new-in-v5-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：期間
-   デフォルト値： `10m0s`
-   範囲： `[10m0s, 8760h0m0s]`
-   GC間隔をGoDurationの形式で指定し`"15m"` `"1h30m"` 。

### tidb_gc_scan_lock_modev5.0<span class="version-mark">の新</span>機能 {#tidb-gc-scan-lock-mode-span-class-version-mark-new-in-v5-0-span}

> **警告：**
>
> 現在、GreenGCは実験的機能です。実稼働環境で使用することはお勧めしません。

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `LEGACY`
-   可能な`LEGACY` ： `PHYSICAL`
    -   `LEGACY` ：古いスキャン方法を使用します。つまり、GreenGCを無効にします。
    -   `PHYSICAL` ：物理スキャン方式を使用します。つまり、GreenGCを有効にします。
-   この変数は、GCの[ロックの解決]ステップでロックをスキャンする方法を指定します。変数値が`LEGACY`に設定されている場合、TiDBはリージョンごとにロックをスキャンします。値`PHYSICAL`を使用すると、各TiKVノードがRaftレイヤーをバイパスし、データを直接スキャンできるようになります。これにより、 [Hibernateリージョン](/tikv-configuration-file.md#hibernate-regions)の機能が有効になっている場合に、GCがすべてのリージョンをウェイクアップする影響を効果的に軽減できるため、ロックの解決での実行速度が向上します。ステップ。

### tidb_general_log {#tidb-general-log}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、すべてのSQLステートメントを[ログ](/tidb-configuration-file.md#logfile)に記録するかどうかを設定するために使用されます。この機能はデフォルトで無効になっています。保守担当者が問題を特定するときにすべてのSQLステートメントをトレースする必要がある場合は、この機能を有効にすることができます。
-   この機能のすべてのレコードをログに表示するには、 `"GENERAL_LOG"`の文字列をクエリします。次の情報が記録されます。
    -   `conn` ：現在のセッションのID。
    -   `user` ：現在のセッションユーザー。
    -   `schemaVersion` ：現在のスキーマバージョン。
    -   `txnStartTS` ：現在のトランザクションが開始するタイムスタンプ。
    -   `forUpdateTS` ：悲観的トランザクションモードでは、 `forUpdateTS`はSQLステートメントの現在のタイムスタンプです。ペシミスティックトランザクションで書き込みの競合が発生すると、TiDBは現在実行されているSQLステートメントを再試行し、このタイムスタンプを更新します。再試行回数は[`max-retry-count`](/tidb-configuration-file.md#max-retry-count)で設定できます。楽観的なトランザクションモデルでは、 `forUpdateTS`は`txnStartTS`に相当します。
    -   `isReadConsistency` ：現在のトランザクション分離レベルが読み取りコミット（RC）であるかどうかを示します。
    -   `current_db` ：現在のデータベースの名前。
    -   `txn_mode` ：トランザクションモード。値のオプションは`OPTIMISTIC`と`PESSIMISTIC`です。
    -   `sql` ：現在のクエリに対応するSQLステートメント。

### tidb_hash_join_concurrency {#tidb-hash-join-concurrency}

> **警告：**
>
> v5.0以降、この変数は非推奨になりました。代わりに、 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定します。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `-1`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、 `hash join`アルゴリズムの同時実行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hashagg_final_concurrency {#tidb-hashagg-final-concurrency}

> **警告：**
>
> v5.0以降、この変数は非推奨になりました。代わりに、 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定します。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `-1`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、 `final`フェーズで同時`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメーターが明確でない場合、 `HashAgg`は同時に実行され、それぞれ2つのフェーズ（ `partial`フェーズと`final`フェーズ）で実行されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hashagg_partial_concurrency {#tidb-hashagg-partial-concurrency}

> **警告：**
>
> v5.0以降、この変数は非推奨になりました。代わりに、 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定します。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `-1`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、 `partial`フェーズで同時`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメーターが明確でない場合、 `HashAgg`は同時に実行され、それぞれ2つのフェーズ（ `partial`フェーズと`final`フェーズ）で実行されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_ignore_prepared_cache_close_stmtv6.0.0<span class="version-mark">の新機能</span> {#tidb-ignore-prepared-cache-close-stmt-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、プリペアドステートメントキャッシュを閉じるためのコマンドを無視するかどうかを設定するために使用されます。
-   この変数が`ON`に設定されている場合、バイナリプロトコルの`COM_STMT_CLOSE`コマンドとテキストプロトコルの[`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md)ステートメントは無視されます。詳細については、 [`COM_STMT_CLOSE`コマンドとDEALLOCATEPREPAREステートメントを無視し<code>DEALLOCATE PREPARE</code>](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)を参照してください。

### tidb_index_join_batch_size {#tidb-index-join-batch-size}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `25000`
-   範囲： `[1, 2147483647]`
-   単位：行
-   この変数は、 `index lookup join`の操作のバッチサイズを設定するために使用されます。
-   OLAPシナリオでは大きな値を使用し、OLTPシナリオでは小さな値を使用します。

### tidb_index_lookup_concurrency {#tidb-index-lookup-concurrency}

> **警告：**
>
> v5.0以降、この変数は非推奨になりました。代わりに、 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定します。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `-1`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、 `index lookup`操作の同時実行性を設定するために使用されます。
-   OLAPシナリオでは大きな値を使用し、OLTPシナリオでは小さな値を使用します。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_join_concurrency {#tidb-index-lookup-join-concurrency}

> **警告：**
>
> v5.0以降、この変数は非推奨になりました。代わりに、 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定します。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `-1`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、 `index lookup join`アルゴリズムの同時実行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_size {#tidb-index-lookup-size}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `20000`
-   範囲： `[1, 2147483647]`
-   単位：行
-   この変数は、 `index lookup`の操作のバッチサイズを設定するために使用されます。
-   OLAPシナリオでは大きな値を使用し、OLTPシナリオでは小さな値を使用します。

### tidb_index_serial_scan_concurrency {#tidb-index-serial-scan-concurrency}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、 `serial scan`操作の同時実行性を設定するために使用されます。
-   OLAPシナリオでは大きな値を使用し、OLTPシナリオでは小さな値を使用します。

### tidb_init_chunk_size {#tidb-init-chunk-size}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `32`
-   範囲： `[1, 32]`
-   単位：行
-   この変数は、実行プロセス中の初期チャンクの行数を設定するために使用されます。

### tidb_isolation_read_enginesv4.0<span class="version-mark">の新</span>機能 {#tidb-isolation-read-engines-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション
-   デフォルト値： `tikv,tiflash,tidb`
-   この変数は、TiDBがデータを読み取るときに使用できるストレージエンジンリストを設定するために使用されます。

### tidb_log_file_max_daysv5.3.0<span class="version-mark">の新機能</span> {#tidb-log-file-max-days-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ：セッション
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 2147483647]`
-   この変数は、現在のTiDBインスタンスのロガーの最大日数を調整するために使用されます。その値は、デフォルトで構成ファイルの[`max-days`](/tidb-configuration-file.md#max-days)構成の値になります。変数値の変更は、現在のTiDBインスタンスにのみ影響します。 TiDBが再起動された後、変数値はリセットされ、構成値は影響を受けません。

### tidb_low_resolution_tso {#tidb-low-resolution-tso}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、低精度TSO機能を有効にするかどうかを設定するために使用されます。この機能を有効にすると、新しいトランザクションは2秒ごとに更新されるタイムスタンプを使用してデータを読み取ります。
-   適用可能な主なシナリオは、古いデータの読み取りが許容される場合に、小さな読み取り専用トランザクションのTSOを取得するオーバーヘッドを削減することです。

### tidb_max_chunk_size {#tidb-max-chunk-size}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1024`
-   範囲： `[32, 2147483647]`
-   単位：行
-   この変数は、実行プロセス中にチャンク内の最大行数を設定するために使用されます。値を大きくしすぎると、キャッシュの局所性の問題が発生する可能性があります。

### tidb_max_delta_schema_countv2.1.18<span class="version-mark">およびv3.0.5の新機能</span> {#tidb-max-delta-schema-count-span-class-version-mark-new-in-v2-1-18-and-v3-0-5-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1024`
-   範囲： `[100, 16384]`
-   この変数は、キャッシュできるスキーマバージョン（対応するバージョン用に変更されたテーブルID）の最大数を設定するために使用されます。値の範囲は100〜16384です。

### tidb_mem_oom_actionv6.1.0<span class="version-mark">の新機能</span> {#tidb-mem-oom-action-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `CANCEL`
-   可能な`LOG` ： `CANCEL`
-   1つのSQLステートメントが`tidb_mem_quota_query`で指定されたメモリクォータを超え、ディスクにスピルオーバーできない場合にTiDBが実行する操作を指定します。詳細については、 [TiDBメモリ制御](/configure-memory-usage.md)を参照してください。
-   デフォルト値は`CANCEL`ですが、TiDB v4.0.2以前のバージョンでは、デフォルト値は`LOG`です。
-   この設定は、以前は`tidb.toml`オプション（ `oom-action` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。

### tidb_mem_quota_analyzev6.1.0<span class="version-mark">の新機能</span> {#tidb-mem-quota-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

-   スコープ：グローバル
-   クラスタに永続化：はい
-   デフォルト値： `0`
-   単位：バイト
-   この変数は、TiDB更新統計の最大メモリ使用量を制御します。このようなメモリ使用量は、手動で[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)を実行した場合、およびTiDBがバックグラウンドでタスクを自動的に分析した場合に発生します。合計メモリ使用量がこのしきい値を超えると、ユーザーが実行した`ANALYZE`が終了し、より低いサンプリングレートを試すか、後で再試行するように通知するエラーメッセージが報告されます。メモリしきい値を超えたためにTiDBバックグラウンドの自動タスクが終了し、使用されたサンプリングレートがデフォルト値よりも高い場合、TiDBはデフォルトのサンプリングレートを使用して更新を再試行します。この変数値が負またはゼロの場合、TiDBは手動更新タスクと自動更新タスクの両方のメモリ使用量を制限しません。

> **ノート：**
>
> `auto_analyze`は、TiDBスタートアップコンフィギュレーションファイルで`run-auto-analyze`が有効になっている場合にのみ、TiDBクラスタでトリガーされます。

### tidb_mem_quota_apply_cachev5.0<span class="version-mark">の新</span>機能 {#tidb-mem-quota-apply-cache-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `33554432` （32 MiB）
-   範囲： `[0, 9223372036854775807]`
-   単位：バイト
-   この変数は、 `Apply`演算子でローカルキャッシュのメモリ使用量のしきい値を設定するために使用されます。
-   `Apply`演算子のローカルキャッシュは、 `Apply`演算子の計算を高速化するために使用されます。変数を`0`に設定して、 `Apply`キャッシュ機能を無効にすることができます。

### tidb_mem_quota_binding_cachev6.0.0<span class="version-mark">の新機能</span> {#tidb-mem-quota-binding-cache-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `67108864`
-   範囲： `[0, 2147483647]`
-   単位：バイト
-   この変数は、バインディングのキャッシュに使用されるメモリのしきい値を設定するために使用されます。
-   システムが過剰なバインディングを作成またはキャプチャして、メモリスペースが過剰に使用された場合、TiDBはログに警告を返します。この場合、キャッシュは使用可能なすべてのバインディングを保持したり、保存するバインディングを決定したりすることはできません。このため、一部のクエリはバインディングを見逃す可能性があります。この問題に対処するには、この変数の値を増やすことができます。これにより、バインディングのキャッシュに使用されるメモリが増えます。このパラメーターを変更した後、 `admin reload bindings`を実行してバインディングを再ロードし、変更を検証する必要があります。

### tidb_mem_quota_query {#tidb-mem-quota-query}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1073741824` （1 GiB）
-   範囲： `[-1, 9223372036854775807]`
-   単位：バイト
-   この変数は、クエリのメモリクォータのしきい値を設定するために使用されます。
-   実行中のクエリのメモリクォータがしきい値を超えると、TiDBは`tidb_mem_oom_action`で指定された操作を実行します。
-   この設定は、以前はセッションスコープであり、初期値として`tidb.toml`から`mem-quota-query`の値を使用していました。 v6.1.0以降、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープの変数になりました。

### tidb_memory_usage_alarm_ratio {#tidb-memory-usage-alarm-ratio}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：フロート
-   デフォルト値： `0.8`
-   範囲： `[0, 1]`
-   TiDBは、必要なメモリの割合が特定のしきい値を超えると、アラームをトリガーします。この機能の詳細な使用法の説明については、 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409)を参照してください。
-   [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409)を設定することにより、この変数の初期値を設定できます。

### tidb_metric_query_range_durationv4.0<span class="version-mark">の新</span>機能 {#tidb-metric-query-range-duration-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション
-   タイプ：整数
-   デフォルト値： `60`
-   範囲： `[10, 216000]`
-   単位：秒
-   この変数は、 `METRICS_SCHEMA`を照会するときに生成されるPrometheusステートメントの範囲期間を設定するために使用されます。

### tidb_metric_query_stepv4.0<span class="version-mark">の新</span>機能 {#tidb-metric-query-step-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション
-   タイプ：整数
-   デフォルト値： `60`
-   範囲： `[10, 216000]`
-   単位：秒
-   この変数は、 `METRICS_SCHEMA`を照会するときに生成されるPrometheusステートメントのステップを設定するために使用されます。

### tidb_multi_statement_modev4.0.11<span class="version-mark">の新機能</span> {#tidb-multi-statement-mode-span-class-version-mark-new-in-v4-0-11-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `OFF`
-   可能な`ON` `WARN` `OFF`
-   この変数は、同じ`COM_QUERY`の呼び出しで複数のクエリを実行できるようにするかどうかを制御します。
-   SQLインジェクション攻撃の影響を減らすために、TiDBは、デフォルトで同じ`COM_QUERY`の呼び出しで複数のクエリが実行されるのを防ぐようになりました。この変数は、以前のバージョンのTiDBからのアップグレードパスの一部として使用することを目的としています。次の動作が適用されます。

| クライアント設定      | `tidb_multi_statement_mode`値 | 複数のステートメントが許可されていますか？ |
| ------------- | ---------------------------- | --------------------- |
| 複数のステートメント=オン | オフ                           | はい                    |
| 複数のステートメント=オン | オン                           | はい                    |
| 複数のステートメント=オン | 暖かい                          | はい                    |
| 複数のステートメント=オフ | オフ                           | いいえ                   |
| 複数のステートメント=オフ | オン                           | はい                    |
| 複数のステートメント=オフ | 暖かい                          | はい（+警告が返されました）        |

> **ノート：**
>
> 安全と見なすことができるのは、デフォルト値の`OFF`のみです。アプリケーションが以前のバージョンのTiDB用に特別に設計されている場合は、設定`tidb_multi_statement_mode=ON`が必要になることがあります。アプリケーションで複数のステートメントのサポートが必要な場合は、 `tidb_multi_statement_mode`オプションではなく、クライアントライブラリによって提供される設定を使用することをお勧めします。例えば：
>
> -   [go-sql-driver](https://github.com/go-sql-driver/mysql#multistatements) （ `multiStatements` ）
> -   [コネクタ/J](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-configuration-properties.html) （ `allowMultiQueries` ）
> -   PHP [mysqli](https://dev.mysql.com/doc/apis-php/en/apis-php-mysqli.quickstart.multiple-statement.html) （ `mysqli_multi_query` ）

### tidb_nontransactional_ignore_errorv6.1.0<span class="version-mark">の新機能</span> {#tidb-nontransactional-ignore-error-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `OFF`
-   この変数は、非トランザクションDMLステートメントでエラーが発生したときにエラーをすぐに返すかどうかを指定します。
-   値が`OFF`に設定されている場合、非トランザクションDMLステートメントは最初のエラーですぐに停止し、エラーを返します。以下のバッチはすべてキャンセルされます。
-   値が`ON`に設定されていて、バッチでエラーが発生した場合、次のバッチはすべてのバッチが実行されるまで実行され続けます。実行プロセス中に発生したすべてのエラーは、結果にまとめて返されます。

### tidb_opt_agg_push_down {#tidb-opt-agg-push-down}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、オプティマイザーが、Join、Projection、UnionAllの前の位置に集計関数をプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリで集計操作が遅い場合は、変数値をONに設定できます。

### tidb_opt_correlation_exp_factor {#tidb-opt-correlation-exp-factor}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1`
-   範囲： `[0, 2147483647]`
-   列の順序の相関に基づいて行数を推定する方法が利用できない場合は、ヒューリスティックな推定方法が使用されます。この変数は、ヒューリスティックメソッドの動作を制御するために使用されます。
    -   値が0の場合、ヒューリスティックな方法は使用されません。
    -   値が0より大きい場合：
        -   値が大きいほど、ヒューリスティック手法でインデックススキャンが使用される可能性があることを示します。
        -   値が小さいほど、ヒューリスティック手法でテーブルスキャンが使用される可能性があります。

### tidb_opt_correlation_threshold {#tidb-opt-correlation-threshold}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：フロート
-   デフォルト値： `0.9`
-   範囲： `[0, 1]`
-   この変数は、列順序相関を使用して行数の推定を有効にするかどうかを決定するしきい値を設定するために使用されます。現在の列と`handle`列の間の次数相関がしきい値を超えると、このメソッドが有効になります。

### tidb_opt_distinct_agg_push_down {#tidb-opt-distinct-agg-push-down}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、オプティマイザーが`distinct` （ `select count(distinct a) from t`など）の集計関数をコプロセッサーにプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   `distinct`操作の集計関数がクエリで遅い場合は、変数値を`1`に設定できます。

次の例では、 `tidb_opt_distinct_agg_push_down`を有効にする前に、TiDBはTiKVからすべてのデータを読み取り、TiDB側で`distinct`を実行する必要があります。 `tidb_opt_distinct_agg_push_down`を有効にすると、 `distinct a`がコプロセッサーにプッシュダウンされ、 `group by`列`test.t.a`が`HashAgg_5`に追加されます。

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```

### tidb_opt_enable_correlation_adjustment {#tidb-opt-enable-correlation-adjustment}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、オプティマイザーが列の順序の相関に基づいて行数を推定するかどうかを制御するために使用されます

### tidb_opt_insubq_to_join_and_agg {#tidb-opt-insubq-to-join-and-agg}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、サブクエリを結合および集約に変換する最適化ルールを有効にするかどうかを設定するために使用されます。
-   たとえば、この最適化ルールを有効にすると、サブクエリは次のように変換されます。

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    サブクエリは、次のように結合に変換されます。

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    `aa`列で`t1`が`unique`と`not null`に制限されている場合。集計せずに、次のステートメントを使用できます。

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_limit_push_down_threshold {#tidb-opt-limit-push-down-threshold}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `100`
-   範囲： `[0, 2147483647]`
-   この変数は、LimitまたはTopN演算子をTiKVにプッシュするかどうかを決定するしきい値を設定するために使用されます。
-   LimitまたはTopN演算子の値がこのしきい値以下の場合、これらの演算子は強制的にTiKVにプッシュダウンされます。この変数は、推定が間違っていることもあり、LimitまたはTopN演算子をTiKVにプッシュダウンできないという問題を解決します。

### tidb_opt_prefer_range_scanv5.0<span class="version-mark">の新</span>機能 {#tidb-opt-prefer-range-scan-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数の値を`ON`に設定すると、オプティマイザーは常に全表スキャンよりも範囲スキャンを優先します。
-   次の例では、 `tidb_opt_prefer_range_scan`を有効にする前に、TiDBオプティマイザが全表スキャンを実行します。 `tidb_opt_prefer_range_scan`を有効にすると、オプティマイザはインデックス範囲スキャンを選択します。

```sql
explain select * from t where age=5;
+-------------------------+------------+-----------+---------------+-------------------+
| id                      | estRows    | task      | access object | operator info     |
+-------------------------+------------+-----------+---------------+-------------------+
| TableReader_7           | 1048576.00 | root      |               | data:Selection_6  |
| └─Selection_6           | 1048576.00 | cop[tikv] |               | eq(test.t.age, 5) |
|   └─TableFullScan_5     | 1048576.00 | cop[tikv] | table:t       | keep order:false  |
+-------------------------+------------+-----------+---------------+-------------------+
3 rows in set (0.00 sec)

set session tidb_opt_prefer_range_scan = 1;

explain select * from t where age=5;
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| id                            | estRows    | task      | access object               | operator info                 |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| IndexLookUp_7                 | 1048576.00 | root      |                             |                               |
| ├─IndexRangeScan_5(Build)     | 1048576.00 | cop[tikv] | table:t, index:idx_age(age) | range:[5,5], keep order:false |
| └─TableRowIDScan_6(Probe)     | 1048576.00 | cop[tikv] | table:t                     | keep order:false              |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
3 rows in set (0.00 sec)
```

### tidb_opt_write_row_id {#tidb-opt-write-row-id}

-   スコープ：セッション
-   デフォルト値： `OFF`
-   この変数は、 `INSERT` 、および`REPLACE`ステートメントが`UPDATE`列で動作できるようにするかどうかを制御するために使用され`_tidb_rowid` 。この変数は、TiDBツールを使用してデータをインポートする場合にのみ使用できます。

### tidb_partition_prune_modev5.1<span class="version-mark">の新</span>機能 {#tidb-partition-prune-mode-span-class-version-mark-new-in-v5-1-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `static`
-   パーティション表に対して`dynamic`モードを有効にするかどうかを指定します。動的プルーニングモードの詳細については、 [パーティションテーブルの動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)を参照してください。

### tidb_persist_analyze_optionsv5.4.0<span class="version-mark">の新機能</span> {#tidb-persist-analyze-options-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、 [ANALYZE構成の永続性](/statistics.md#persist-analyze-configurations)つの機能を有効にするかどうかを制御します。

### tidb_placement_modev6.0.0<span class="version-mark">の新機能</span> {#tidb-placement-mode-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `STRICT`
-   可能な`IGNORE` ： `STRICT`
-   この変数は、DDLステートメントが[SQLで指定された配置ルール](/placement-rules-in-sql.md)を無視するかどうかを制御します。変数値が`IGNORE`の場合、すべての配置ルールオプションは無視されます。
-   無効な配置ルールが割り当てられている場合でも、テーブルを常に作成できるようにするために、論理ダンプ/復元ツールで使用することを目的としています。これは、mysqldumpがすべてのダンプファイルの先頭に`SET FOREIGN_KEY_CHECKS=0;`を書き込む方法と似ています。

### tidb_pprof_sql_cpuv4.0<span class="version-mark">の新</span>機能 {#tidb-pprof-sql-cpu-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 1]`
-   この変数は、パフォーマンスの問題を特定してトラブルシューティングするために、プロファイル出力で対応するSQLステートメントをマークするかどうかを制御するために使用されます。

### tidb_prepared_plan_cache_memory_guard_ratiov6.1.0<span class="version-mark">の新機能</span> {#tidb-prepared-plan-cache-memory-guard-ratio-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：フロート
-   デフォルト値： `0.1`
-   範囲： `[0, 1]`
-   準備されたプランキャッシュがメモリ保護メカニズムをトリガーするしきい値。詳細については、 [準備された計画キャッシュのメモリ管理](/sql-prepared-plan-cache.md)を参照してください。
-   この設定は、以前は`tidb.toml`オプション（ `prepared-plan-cache.memory-guard-ratio` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。

### tidb_prepared_plan_cache_sizev6.1.0<span class="version-mark">の新機能</span> {#tidb-prepared-plan-cache-size-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `100`
-   範囲： `[1, 100000]`
-   セッションでキャッシュできるプランの最大数。詳細については、 [準備された計画キャッシュのメモリ管理](/sql-prepared-plan-cache.md)を参照してください。
-   この設定は、以前は`tidb.toml`オプション（ `prepared-plan-cache.capacity` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。

### tidb_projection_concurrency {#tidb-projection-concurrency}

> **警告：**
>
> v5.0以降、この変数は非推奨になりました。代わりに、 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定します。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `-1`
-   範囲： `[-1, 256]`
-   単位：スレッド
-   この変数は、 `Projection`演算子の同時実行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_query_log_max_len {#tidb-query-log-max-len}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `4096` （4 KiB）
-   範囲： `[0, 1073741824]`
-   単位：バイト
-   SQLステートメント出力の最大長。ステートメントの出力長が`tidb_query_log_max_len`の値より大きい場合、ステートメントは切り捨てられて出力されます。
-   この設定は、以前は`tidb.toml`オプション（ `log.query-log-max-len` ）としても使用可能でしたが、TiDBv6.1.0以降のシステム変数にすぎません。

### tidb_rc_read_check_tsv6.0.0<span class="version-mark">の新機能</span> {#tidb-rc-read-check-ts-span-class-version-mark-new-in-v6-0-0-span}

> **警告：**
>
> -   この機能は[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。 `tidb_rc_read_check_ts`と`replica-read`を同時に有効にしないでください。
> -   クライアントがカーソルを使用している場合、返されたデータの前のバッチがクライアントによってすでに使用されていて、ステートメントが最終的に失敗する場合に備えて、 `tidb_rc_read_check_ts`を有効にすることはお勧めしません。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、タイムスタンプの取得を最適化するために使用されます。これは、読み取りと書き込みの競合がまれである読み取りコミット分離レベルのシナリオに適しています。この変数を有効にすると、グローバルタイムスタンプを取得するためのレイテンシとコストを回避でき、トランザクションレベルの読み取りレイテンシを最適化できます。
-   読み取りと書き込みの競合が深刻な場合、この機能を有効にすると、グローバルタイムスタンプを取得するためのコストと遅延が増加し、パフォーマンスが低下する可能性があります。詳細については、 [コミットされた分離レベルを読み取る](/transaction-isolation-levels.md#read-committed-isolation-level)を参照してください。

### tidb_read_stalenessv5.4.0<span class="version-mark">の新機能</span> {#tidb-read-staleness-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ：セッション
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[-2147483648, 0]`
-   この変数は、TiDBが現在のセッションで読み取ることができる履歴データの時間範囲を設定するために使用されます。値を設定した後、TiDBはこの変数で許可されている範囲から可能な限り新しいタイムスタンプを選択し、以降のすべての読み取り操作はこのタイムスタンプに対して実行されます。たとえば、この変数の値が`-5`に設定されている場合、TiKVに対応する履歴バージョンのデータがあるという条件で、TiDBは5秒の時間範囲内で可能な限り新しいタイムスタンプを選択します。

### tidb_record_plan_in_slow_log {#tidb-record-plan-in-slow-log}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、低速クエリの実行プランを低速ログに含めるかどうかを制御するために使用されます。

### tidb_redact_log {#tidb-redact-log}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、TiDBログと低速ログに記録されているSQLステートメントのユーザー情報を非表示にするかどうかを制御します。
-   変数を`1`に設定すると、ユーザー情報は非表示になります。たとえば、実行されたSQLステートメントが`insert into t values (1,2)`の場合、ステートメントはログに`insert into t values (?,?)`として記録されます。

### tidb_regard_null_as_pointv5.4.0<span class="version-mark">の新機能</span> {#tidb-regard-null-as-point-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、オプティマイザがインデックスアクセスのプレフィックス条件としてnull等価を含むクエリ条件を使用できるかどうかを制御します。
-   この変数はデフォルトで有効になっています。有効にすると、オプティマイザはアクセスされるインデックスデータの量を減らすことができ、クエリの実行を高速化します。たとえば、クエリに複数列のインデックス`index(a, b)`が含まれ、クエリ条件に`a<=>null and b=1`が含まれている場合、オプティマイザはインデックスアクセスのクエリ条件で`a<=>null`と`b=1`の両方を使用できます。変数が無効になっている場合、 `a<=>null and b=1`にはヌル等価条件が含まれているため、オプティマイザーは`b=1`をインデックスアクセスに使用しません。

### tidb_replica_readv4.0<span class="version-mark">の新</span>機能 {#tidb-replica-read-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `leader`
-   `closest-replicas`な`follower` `leader-and-follower` `leader`
-   この変数は、TiDBがデータを読み取る場所を制御するために使用されます。 3つのオプションがあります。
    -   リーダー：リーダーノードからのみ読み取り
    -   フォロワー：フォロワーノードからの読み取り専用
    -   リーダーとフォロワー：リーダーまたはフォロワーノードから読み取ります
-   詳細については、 [フォロワーは読む](/follower-read.md)を参照してください。

### tidb_restricted_read_onlyv5.2.0<span class="version-mark">の新機能</span> {#tidb-restricted-read-only-span-class-version-mark-new-in-v5-2-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、クラスタ全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスタ全体のすべてのTiDBサーバーは読み取り専用モードになります。この場合、 `USE`は、 `SELECT`などのデータを変更しないステートメントのみを実行し`SHOW` 。 `INSERT`や`UPDATE`などの他のステートメントの場合、TiDBはこれらのステートメントを読み取り専用モードで実行することを拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスタ全体が最終的に読み取り専用ステータスになります。 TiDBクラスタでこの変数の値を変更したが、その変更が他のTiDBサーバーにまだ伝播されていない場合、更新されてい**ない**TiDBサーバーはまだ読み取り専用モードではありません。
-   この変数を有効にすると、実行中のSQLステートメントは影響を受けません。 TiDBは、実行さ**れる**SQLステートメントの読み取り専用チェックのみを実行します。
-   この変数を有効にすると、TiDBはコミットされていないトランザクションを次の方法で処理します。
    -   コミットされていない読み取り専用トランザクションの場合、トランザクションを通常どおりコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行するSQLステートメントは拒否されます。
    -   データが変更されたコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードを有効にすると、すべてのユーザー（ `SUPER`特権を持つユーザーを含む）は、ユーザーに`RESTRICTED_REPLICA_WRITER_ADMIN`特権が明示的に付与されていない限り、データを書き込む可能性のあるSQLステートメントを実行できなくなります。
-   `RESTRICTED_VARIABLES_ADMIN`つまたは`SUPER`の特権を持つユーザーは、この変数を変更できます。ただし、 [セキュリティ強化モード](#tidb_enable_enhanced_security)が有効になっている場合、この変数を変更できるのは`RESTRICTED_VARIABLES_ADMIN`特権を持つユーザーのみです。

### tidb_retry_limit {#tidb-retry-limit}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `10`
-   範囲： `[-1, 9223372036854775807]`
-   この変数は、楽観的なトランザクションの再試行の最大数を設定するために使用されます。トランザクションで再試行可能なエラー（トランザクションの競合、非常に遅いトランザクションコミット、テーブルスキーマの変更など）が発生すると、この変数に従ってこのトランザクションが再実行されます。 `tidb_retry_limit`から`0`に設定すると、自動再試行が無効になることに注意してください。この変数は楽観的なトランザクションにのみ適用され、悲観的なトランザクションには適用されません。

### tidb_row_format_version {#tidb-row-format-version}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `2`
-   範囲： `[1, 2]`
-   テーブルに新しく保存されたデータのフォーマットバージョンを制御します。 TiDB v4.0では、新しいデータを保存するためにデフォルトで[新しいストレージ行フォーマット](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md)バージョン`2`が使用されます。
-   4.0.0より前のバージョンのTiDBから4.0.0にアップグレードする場合、フォーマットバージョンは変更されず、TiDBは引き続きバージョン`1`の古いフォーマットを使用してデータをテーブルに書き込みます。つまり、**新しく作成されたクラスターのみが使用します**。<strong>デフォルトでは、新しいデータ形式</strong>。
-   この変数を変更しても、保存されている古いデータには影響しませんが、この変数を変更した後、新しく書き込まれたデータにのみ対応するバージョン形式が適用されることに注意してください。

### tidb_scatter_region {#tidb-scatter-region}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   デフォルトでは、TiDBで作成されるときに、リージョンは新しいテーブル用に分割されます。この変数を有効にすると、 `CREATE TABLE`ステートメントの実行中に、新しく分割されたリージョンがすぐに分散されます。これは、テーブルがバッチで作成された直後にデータをバッチで書き込む必要があるシナリオに当てはまります。これは、新しく分割されたリージョンを事前にTiKVに分散させることができ、PDによるスケジュールを待つ必要がないためです。バッチでのデータ書き込みの継続的な安定性を確保するために、 `CREATE TABLE`ステートメントは、リージョンが正常に分散された後にのみ成功を返します。これにより、この変数を無効にした場合よりも、ステートメントの実行時間が数倍長くなります。
-   テーブルの作成時に`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`が設定されている場合、テーブルの作成後に指定された数のリージョンが均等に分割されることに注意してください。

### tidb_skip_ascii_checkv5.0<span class="version-mark">の新</span>機能 {#tidb-skip-ascii-check-span-class-version-mark-new-in-v5-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、ASCII検証をスキップするかどうかを設定するために使用されます。
-   ASCII文字の検証はパフォーマンスに影響します。入力文字が有効なASCII文字であることが確実な場合は、変数値を`ON`に設定できます。

### tidb_skip_isolation_level_check {#tidb-skip-isolation-level-check}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   このスイッチを有効にした後、TiDBでサポートされていない分離レベルが`tx_isolation`に割り当てられている場合、エラーは報告されません。これにより、異なる分離レベルを設定する（ただし、依存しない）アプリケーションとの互換性を向上させることができます。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_utf8_check {#tidb-skip-utf8-check}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、UTF-8検証をスキップするかどうかを設定するために使用されます。
-   UTF-8文字を検証すると、パフォーマンスに影響します。入力文字が有効なUTF-8文字であることが確実な場合は、変数値を`ON`に設定できます。

> **ノート：**
>
> 文字チェックをスキップすると、TiDBはアプリケーションによって書き込まれた不正なUTF-8文字の検出に失敗し、 `ANALYZE`の実行時にデコードエラーを引き起こし、その他の不明なエンコードの問題を引き起こす可能性があります。アプリケーションが書き込まれた文字列の有効性を保証できない場合は、文字チェックをスキップすることはお勧めしません。

### tidb_slow_log_threshold {#tidb-slow-log-threshold}

-   スコープ：グローバル
-   クラスタに永続化：いいえ
-   タイプ：整数
-   デフォルト値： `300`
-   範囲： `[-1, 9223372036854775807]`
-   単位：ミリ秒
-   この変数は、低速ログによって消費された時間のしきい値を出力するために使用されます。クエリに費やされた時間がこの値よりも大きい場合、このクエリは低速ログと見なされ、そのログは低速クエリログに出力されます。

使用例：

```sql
SET tidb_slow_log_threshold = 200;
```

### tidb_max_tiflash_threadsv6.1.0<span class="version-mark">の新機能</span> {#tidb-max-tiflash-threads-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `-1`
-   範囲： `[-1, 256]`
-   この変数は、TiFlashがリクエストを実行するための最大同時実行性を設定するために使用されます。デフォルト値は`-1`で、このシステム変数が無効であることを示します。値が`0`の場合、スレッドの最大数はTiFlashによって自動的に構成されます。

### tidb_slow_query_file {#tidb-slow-query-file}

-   スコープ：セッション
-   デフォルト値： &quot;&quot;
-   `INFORMATION_SCHEMA.SLOW_QUERY`が照会されると、構成ファイルで`slow-query-file`によって設定された低速照会ログ名のみが解析されます。デフォルトの低速クエリログ名は「tidb-slow.log」です。他のログを解析するには、 `tidb_slow_query_file`セッション変数を特定のファイルパスに設定してから、クエリ`INFORMATION_SCHEMA.SLOW_QUERY`を実行して、設定されたファイルパスに基づいて低速クエリログを解析します。詳細については、 [遅いクエリを特定する](/identify-slow-queries.md)を参照してください。

### tidb_snapshot {#tidb-snapshot}

-   スコープ：セッション
-   デフォルト値： &quot;&quot;
-   この変数は、セッションによってデータが読み取られる時点を設定するために使用されます。たとえば、変数を「2017-11-11 20:20:20」または「400036290571534337」のようなTSO番号に設定すると、現在のセッションはこの瞬間のデータを読み取ります。

### tidb_stats_cache_mem_quotav6.1.0<span class="version-mark">の新機能</span> {#tidb-stats-cache-mem-quota-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> この変数は実験的機能です。実稼働環境での使用はお勧めしません。

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 1099511627776]`
-   この変数は、TiDB統計キャッシュのメモリクォータを設定します。

### tidb_stats_load_pseudo_timeoutv5.4.0<span class="version-mark">の新機能</span> {#tidb-stats-load-pseudo-timeout-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、統計を同期的にロードすることは実験的機能です。実稼働環境で使用することはお勧めしません。

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、SQL最適化の待機時間がタイムアウトに達したときのTiDBの動作を制御して、完全な列統計を同期的にロードします。デフォルト値`OFF`は、タイムアウト後にSQLの実行が失敗することを意味します。この変数を`ON`に設定すると、SQL最適化は、タイムアウト後に疑似統計の使用に戻ります。

### tidb_stats_load_sync_waitv5.4.0<span class="version-mark">の新機能</span> {#tidb-stats-load-sync-wait-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、統計を同期的にロードすることは実験的機能です。実稼働環境で使用することはお勧めしません。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 2147483647]`
-   単位：ミリ秒
-   この変数は、統計の同期ロード機能を有効にするかどうかを制御します。デフォルト値`0`は、機能が無効になっていることを意味します。この機能を有効にするには、この変数をタイムアウト（ミリ秒単位）に設定して、SQL最適化が最大で完全な列統計を同期的にロードするのを待つことができます。詳細については、 [負荷統計](/statistics.md#load-statistics)を参照してください。

### tidb_stmt_summary_history_sizev4.0<span class="version-mark">の新</span>機能 {#tidb-stmt-summary-history-size-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `24`
-   範囲： `[0, 255]`
-   この変数は、履歴容量を[ステートメント要約表](/statement-summary-tables.md)に設定するために使用されます。

### tidb_stmt_summary_internal_queryv4.0<span class="version-mark">の新</span>機能 {#tidb-stmt-summary-internal-query-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、TiDBのSQL情報を[ステートメント要約表](/statement-summary-tables.md)に含めるかどうかを制御するために使用されます。

### tidb_stmt_summary_max_sql_lengthv4.0<span class="version-mark">の新</span>機能 {#tidb-stmt-summary-max-sql-length-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `4096`
-   範囲： `[0, 2147483647]`
-   この変数は、 [ステートメント要約表](/statement-summary-tables.md)のSQL文字列の長さを制御するために使用されます。

### tidb_stmt_summary_max_stmt_countv4.0<span class="version-mark">の新</span>機能 {#tidb-stmt-summary-max-stmt-count-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `3000`
-   範囲： `[1, 32767]`
-   この変数は、 [ステートメント要約表](/statement-summary-tables.md)がメモリに格納するステートメントの最大数を設定するために使用されます。

### tidb_stmt_summary_refresh_intervalv4.0<span class="version-mark">の新</span>機能 {#tidb-stmt-summary-refresh-interval-span-class-version-mark-new-in-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `1800`
-   範囲： `[1, 2147483647]`
-   単位：秒
-   この変数は、リフレッシュ時間を[ステートメント要約表](/statement-summary-tables.md)に設定するために使用されます。

### tidb_store_limitv3.0.4<span class="version-mark">およびv4.0の新機能</span> {#tidb-store-limit-span-class-version-mark-new-in-v3-0-4-and-v4-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `0`
-   範囲： `[0, 9223372036854775807]`
-   この変数は、TiDBが同時にTiKVに送信できるリクエストの最大数を制限するために使用されます。 0は制限がないことを意味します。

### tidb_sysdate_is_nowv6.0.0<span class="version-mark">の新機能</span> {#tidb-sysdate-is-now-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `OFF`
-   この変数は、 `SYSDATE`つの関数を`NOW`の関数に置き換えることができるかどうかを制御するために使用されます。この構成アイテムは、MySQLオプション[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。

### tidb_table_cache_leasev6.0.0<span class="version-mark">の新機能</span> {#tidb-table-cache-lease-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `3`
-   範囲： `[1, 10]`
-   単位：秒
-   この変数は、デフォルト値`3`でリース時間を[キャッシュされたテーブル](/cached-tables.md)に制御するために使用されます。この変数の値は、キャッシュされたテーブルへの変更に影響します。キャッシュされたテーブルに変更が加えられた後、最長の待機時間は`tidb_table_cache_lease`秒になる可能性があります。テーブルが読み取り専用であるか、高い書き込みレイテンシーを受け入れることができる場合は、この変数の値を増やして、テーブルをキャッシュするための有効時間を増やし、リース更新の頻度を減らすことができます。

### tidb_tmp_table_max_sizev5.3.0<span class="version-mark">の新機能</span> {#tidb-tmp-table-max-size-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `67108864`
-   範囲： `[1048576, 137438953472]`
-   単位：バイト
-   この変数は、単一の[一時テーブル](/temporary-tables.md)の最大サイズを設定するために使用されます。この変数値よりも大きいサイズの一時テーブルがあると、エラーが発生します。

### tidb_top_sql_max_meta_countv6.0.0<span class="version-mark">の新機能</span> {#tidb-top-sql-max-meta-count-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `5000`
-   範囲： `[1, 10000]`
-   この変数は、1分あたり[Top SQL](/dashboard/top-sql.md)つ収集されるSQLステートメントタイプの最大数を制御するために使用されます。

### tidb_top_sql_max_time_series_countv6.0.0<span class="version-mark">の新機能</span> {#tidb-top-sql-max-time-series-count-span-class-version-mark-new-in-v6-0-0-span}

> **ノート：**
>
> 現在、TiDBダッシュボードの[Top SQL ]ページには、負荷に最も寄与する上位5種類のSQLクエリのみが表示されます。これは、 `tidb_top_sql_max_time_series_count`の構成とは関係ありません。

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `100`
-   範囲： `[1, 5000]`
-   この変数は、負荷に最も寄与するSQLステートメント（つまり、上位N）を[Top SQL](/dashboard/top-sql.md)分あたり1回記録できるSQLステートメントの数を制御するために使用されます。

### tidb_tso_client_batch_max_wait_timev5.3.0<span class="version-mark">の新機能</span> {#tidb-tso-client-batch-max-wait-time-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ：グローバル
-   クラスタに永続化：はい
-   タイプ：フロート
-   デフォルト値： `0`
-   範囲： `[0, 10]`
-   範囲： `[0, 10]`
-   単位：ミリ秒
-   この変数は、TiDBがPDからTSOを要求するときのバッチ操作の最大待機時間を設定するために使用されます。デフォルト値は`0`です。これは、余分な待機時間がないことを意味します。
-   毎回PDからTSO要求を取得する場合、TiDBが使用するPDクライアントは、同時に受信したTSO要求をできるだけ多く収集します。次に、PDクライアントは収集された要求をバッチで1つのRPC要求にマージし、要求をPDに送信します。これは、PDへの圧力を軽減するのに役立ちます。
-   この変数を`0`より大きい値に設定した後、TiDBは、各バッチマージが終了する前に、この値の最大期間を待機します。これは、より多くのTSO要求を収集し、バッチ操作の効果を向上させるためです。
-   この変数の値を増やすためのシナリオ：
    -   TSO要求のプレッシャーが高いため、PDリーダーのCPUがボトルネックに達し、TSORPC要求の待ち時間が長くなります。
    -   クラスタに多くのTiDBインスタンスはありませんが、すべてのTiDBインスタンスは高い同時実行性にあります。
-   この変数をできるだけ小さい値に設定することをお勧めします。

> **ノート：**
>
> PDリーダーのCPU使用率のボトルネック以外の理由（ネットワークの問題など）でTSORPC遅延が増加するとします。この場合、値を`tidb_tso_client_batch_max_wait_time`に増やすと、TiDBの実行待ち時間が長くなり、クラスタのQPSパフォーマンスに影響を与える可能性があります。

### tidb_txn_assertion_levelv6.0.0<span class="version-mark">の新機能</span> {#tidb-txn-assertion-level-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ：セッション|グローバル

-   クラスタに永続化：はい

-   タイプ：列挙

-   デフォルト値： `FAST`

-   可能な`FAST` `STRICT` `OFF`

-   この変数は、アサーションレベルを制御するために使用されます。アサーションは、データとインデックス間の整合性チェックであり、書き込まれているキーがトランザクションコミットプロセスに存在するかどうかをチェックします。詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)を参照してください。

    -   `OFF` ：このチェックを無効にします。
    -   `FAST` ：パフォーマンスにほとんど影響を与えずに、ほとんどのチェック項目を有効にします。
    -   `STRICT` ：すべてのチェック項目を有効にしますが、システムのワークロードが高い場合の悲観的なトランザクションパフォーマンスへの影響はわずかです。

-   v6.0.0以降のバージョンの新しいクラスターの場合、デフォルト値は`FAST`です。 v6.0.0より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_txn_mode {#tidb-txn-mode}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `pessimistic`
-   可能な`optimistic` ： `pessimistic`
-   この変数は、トランザクションモードを設定するために使用されます。 TiDB 3.0は、悲観的なトランザクションをサポートします。 TiDB 3.0.8以降、 [悲観的なトランザクションモード](/pessimistic-transaction.md)はデフォルトで有効になっています。
-   TiDBをv3.0.7以前のバージョンからv3.0.8以降のバージョンにアップグレードしても、デフォルトのトランザクションモードは変更されません。**デフォルトでは、新しく作成されたクラスターのみが悲観的トランザクションモードを使用します**。
-   この変数が「optimistic」または「」に設定されている場合、TiDBは[楽観的なトランザクションモード](/optimistic-transaction.md)を使用します。

### tidb_use_plan_baselinesv4.0<span class="version-mark">の新</span>機能 {#tidb-use-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、実行プランのバインド機能を有効にするかどうかを制御するために使用されます。デフォルトで有効になっていますが、 `OFF`の値を割り当てることで無効にできます。実行プランバインディングの使用については、 [実行プランのバインド](/sql-plan-management.md#create-a-binding)を参照してください。

### tidb_wait_split_region_finish {#tidb-wait-split-region-finish}

-   スコープ：セッション
-   タイプ：ブール
-   デフォルト値： `ON`
-   通常、リージョンの分散には長い時間がかかります。これは、PDスケジューリングとTiKV負荷によって決定されます。この変数は、 `SPLIT REGION`のステートメントが実行されているときに、すべてのリージョンが完全に分散された後に結果をクライアントに返すかどうかを設定するために使用されます。
    -   `ON`では、 `SPLIT REGIONS`ステートメントがすべてのリージョンが分散するまで待機する必要があります。
    -   `OFF`は、すべてのリージョンの分散を終了する前に`SPLIT REGIONS`ステートメントが戻ることを許可します。
-   リージョンをスキャッターする場合、スキャッターされているリージョンの書き込みと読み取りのパフォーマンスが影響を受ける可能性があることに注意してください。バッチ書き込みまたはデータインポートのシナリオでは、リージョンの分散が終了した後にデータをインポートすることをお勧めします。

### tidb_wait_split_region_timeout {#tidb-wait-split-region-timeout}

-   スコープ：セッション
-   タイプ：整数
-   デフォルト値： `300`
-   範囲： `[1, 2147483647]`
-   単位：秒
-   この変数は、 `SPLIT REGION`ステートメントを実行するためのタイムアウトを設定するために使用されます。指定された時間値内にステートメントが完全に実行されない場合、タイムアウトエラーが返されます。

### tidb_window_concurrencyv4.0<span class="version-mark">の新</span>機能 {#tidb-window-concurrency-span-class-version-mark-new-in-v4-0-span}

> **警告：**
>
> v5.0以降、この変数は非推奨になりました。代わりに、 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定します。

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `-1`
-   範囲： `[1, 256]`
-   単位：スレッド
-   この変数は、ウィンドウ演算子の同時実行度を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### time_zone {#time-zone}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   デフォルト値： `SYSTEM`
-   この変数は、現在のタイムゾーンを返します。値は、「-8：00」などのオフセットまたは名前付きゾーン「America/Los_Angeles」のいずれかとして指定できます。
-   値`SYSTEM`は、タイムゾーンがシステムホストと同じである必要があることを意味します。システムホストは、 [`system_time_zone`](#system_time_zone)変数を介して利用できます。

### タイムスタンプ {#timestamp}

-   スコープ：セッション
-   タイプ：フロート
-   デフォルト値： `0`
-   範囲： `[0, 2147483647]`
-   この変数の空でない`NOW()` `CURRENT_TIMESTAMP()`およびその他の関数のタイムスタンプとして使用されるUNIXエポックを示します。この変数は、データの復元またはレプリケーションで使用される場合があります。

### transaction_isolation {#transaction-isolation}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：列挙
-   デフォルト値： `REPEATABLE-READ`
-   `SERIALIZABLE`な`READ-COMMITTED` `REPEATABLE-READ` `READ-UNCOMMITTED`
-   この変数は、トランザクション分離を設定します。 TiDBはMySQLとの互換性のために`REPEATABLE-READ`をアドバタイズしますが、実際の分離レベルはスナップショット分離です。詳細については、 [トランザクション分離レベル](/transaction-isolation-levels.md)を参照してください。

### tx_isolation {#tx-isolation}

この変数は`transaction_isolation`のエイリアスです。

### バージョン {#version}

-   スコープ：なし
-   デフォルト値： `5.7.25-TiDB-` （tidbバージョン）
-   この変数は、MySQLバージョンを返し、その後にTiDBバージョンが続きます。たとえば、「5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253」。

### version_comment {#version-comment}

-   スコープ：なし
-   デフォルト値:(文字列）
-   この変数は、TiDBバージョンに関する追加の詳細を返します。たとえば、「TiDBサーバー（Apache License 2.0）Community Edition、MySQL5.7互換」。

### version_compile_machine {#version-compile-machine}

-   スコープ：なし
-   デフォルト値:(文字列）
-   この変数は、TiDBが実行されているCPUアーキテクチャの名前を返します。

### version_compile_os {#version-compile-os}

-   スコープ：なし
-   デフォルト値:(文字列）
-   この変数は、TiDBが実行されているOSの名前を返します。

### wait_timeout {#wait-timeout}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：整数
-   デフォルト値： `28800`
-   範囲： `[0, 31536000]`
-   単位：秒
-   この変数は、ユーザーセッションのアイドルタイムアウトを制御します。ゼロ値は無制限を意味します。

### warning_count {#warning-count}

-   スコープ：セッション
-   デフォルト値： `0`
-   この読み取り専用変数は、以前に実行されたステートメントで発生した警告の数を示します。

### windowing_use_high_precision {#windowing-use-high-precision}

-   スコープ：セッション|グローバル
-   クラスタに永続化：はい
-   タイプ：ブール
-   デフォルト値： `ON`
-   この変数は、ウィンドウ関数を計算するときに高精度モードを使用するかどうかを制御します。
