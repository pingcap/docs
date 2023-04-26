---
title: System Variables
summary: Use system variables to optimize performance or alter running behavior.
---

# システム変数 {#system-variables}

TiDB システム変数は、設定が`SESSION`または`GLOBAL`スコープに適用されるという点で、MySQL と同様に動作します。

-   `SESSION`スコープの変更は、現在のセッションにのみ影響します。
-   `GLOBAL`スコープの変更はすぐに適用されます。この変数のスコープも`SESSION`場合、すべてのセッション (自分のセッションを含む) は引き続き現在のセッション値を使用します。
-   変更は[`SET`ステートメント](/sql-statements/sql-statement-set-variable.md)を使用して行われます。

```sql
# These two identical statements change a session variable
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# These two identical statements change a global variable
SET @@global.tidb_distsql_scan_concurrency = 10;
SET GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **ノート：**
>
> いくつかの`GLOBAL`変数が TiDB クラスターに保持されます。このドキュメントの一部の変数には`Persists to cluster`設定があり、これは`Yes`または`No`に構成できます。
>
> -   設定が`Persists to cluster: Yes`変数の場合、グローバル変数が変更されると、すべての TiDB サーバーに通知が送信され、システム変数キャッシュが更新されます。 TiDB サーバーを追加するか、既存の TiDB サーバーを再起動すると、永続化された構成値が自動的に使用されます。
> -   `Persists to cluster: No`設定の変数の場合、変更は接続先のローカル TiDB インスタンスにのみ適用されます。値セットを保持するには、 `tidb.toml`構成ファイルで変数を指定する必要があります。
>
> さらに、TiDB はいくつかの MySQL 変数を読み取り可能かつ設定可能として提供します。これは、アプリケーションとコネクタの両方が MySQL 変数を読み取るのが一般的であるため、互換性のために必要です。たとえば、JDBC コネクタは、動作に依存していないにもかかわらず、クエリ キャッシュ設定の読み取りと設定の両方を行います。

> **ノート：**
>
> 値が大きいほど、常にパフォーマンスが向上するとは限りません。ほとんどの設定は各接続に適用されるため、ステートメントを実行している同時接続の数を考慮することも重要です。
>
> 安全な値を決定するときは、変数の単位を考慮してください。
>
> -   スレッドの場合、安全な値は通常、CPU コアの数までです。
> -   バイトの場合、安全な値は通常、システムメモリの量よりも小さくなります。
> -   時間については、単位が秒またはミリ秒である可能性があることに注意してください。
>
> 同じユニットを使用する変数は、同じリソースのセットを求めて競合する可能性があります。

## 変数参照 {#variable-reference}

### allow_auto_random_explicit_insert <span class="version-mark">v4.0.3 の新機能</span> {#allow-auto-random-explicit-insert-span-class-version-mark-new-in-v4-0-3-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `INSERT`ステートメントで`AUTO_RANDOM`属性を持つ列の値を明示的に指定できるようにするかどうかを決定します。

### auto_increment_increment {#auto-increment-increment}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てられる`AUTO_INCREMENT`値のステップ サイズを制御します。 `auto_increment_offset`と組み合わせて使用することが多い。

### auto_increment_offset {#auto-increment-offset}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てられる`AUTO_INCREMENT`値の初期オフセットを制御します。この設定は`auto_increment_increment`と組み合わせて使用されることがよくあります。例えば：

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

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   明示的なトランザクションでない場合にステートメントを自動的にコミットするかどうかを制御します。詳細については[トランザクション概要](/transaction-overview.md#autocommit)参照してください。

### block_encryption_mode {#block-encryption-mode}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `aes-128-ecb`
-   値のオプション: `aes-128-ecb` 、 `aes-192-ecb` 、 `aes-256-ecb` 、 `aes-128-cbc` 、 `aes-192-cbc` 、 `aes-256-cbc` 、 `aes-128-ofb` 、 `aes-192-ofb` 、 `aes-256-ofb` 、 `aes-128-cfb` 、 `aes-192-cfb` 、 `aes-256-cfb`
-   この変数は、組み込み関数`AES_ENCRYPT()`および`AES_DECRYPT()`の暗号化モードを設定します。

### character_set_client {#character-set-client}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `utf8mb4`
-   クライアントから送信されたデータの文字セット。 TiDB での文字セットと照合順序の使用の詳細については、 [文字セットと照合順序](/character-set-and-collation.md)を参照してください。必要に応じて[`SET NAMES`](/sql-statements/sql-statement-set-names.md)を使用して文字セットを変更することをお勧めします。

### character_set_connection {#character-set-connection}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `utf8mb4`
-   指定された文字セットを持たない文字列リテラルの文字セット。

### character_set_database {#character-set-database}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `utf8mb4`
-   この変数は、使用中のデフォルト データベースの文字セットを示します。**この変数を設定することはお勧めしません**。新しいデフォルト データベースが選択されると、サーバーは変数値を変更します。

### character_set_results {#character-set-results}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `utf8mb4`
-   データがクライアントに送信されるときに使用される文字セット。

### character_set_server {#character-set-server}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `utf8mb4`
-   サーバーのデフォルトの文字セット。

### collation_connection {#collation-connection}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `utf8mb4_bin`
-   この変数は、現在の接続で使用される照合順序を示します。これは、MySQL 変数`collation_connection`と一致しています。

### collation_database {#collation-database}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `utf8mb4_bin`
-   この変数は、使用中のデータベースのデフォルトの照合順序を示します。**この変数を設定することはお勧めしません**。新しいデータベースが選択されると、TiDB はこの変数の値を変更します。

### collation_server {#collation-server}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `utf8mb4_bin`
-   データベースの作成時に使用されるデフォルトの照合順序。

### cte_max_recursion_depth {#cte-max-recursion-depth}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[0, 4294967295]`
-   共通テーブル式の最大再帰深度を制御します。

### データディレクトリ {#datadir}

<CustomContent platform="tidb">

-   スコープ: なし
-   デフォルト値:コンポーネントとデプロイ方法によって異なります。
    -   `/tmp/tidb` : [`--store`](/command-line-flags-for-tidb-configuration.md#--store)に対して`"unistore"`設定した場合、または`--store`を設定しなかった場合。
    -   `${pd-ip}:${pd-port}` : TiUPおよびTiDB Operator for Kubernetes デプロイメントのデフォルトのstorageエンジンである TiKV を使用する場合。
-   この変数は、データが格納されている場所を示します。この場所は、ローカル パス`/tmp/tidb`にすることも、データが TiKV に保存されている場合は PDサーバーを指すこともできます。 `${pd-ip}:${pd-port}`の形式の値は、起動時に TiDB が接続する PDサーバーを示します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   スコープ: なし
-   デフォルト値:コンポーネントとデプロイ方法によって異なります。
    -   `/tmp/tidb` : [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store)に対して`"unistore"`設定した場合、または`--store`を設定しなかった場合。
    -   `${pd-ip}:${pd-port}` : TiUPおよびTiDB Operator for Kubernetes デプロイメントのデフォルトのstorageエンジンである TiKV を使用する場合。
-   この変数は、データが格納されている場所を示します。この場所は、ローカル パス`/tmp/tidb`にすることも、データが TiKV に保存されている場合は PDサーバーを指すこともできます。 `${pd-ip}:${pd-port}`の形式の値は、起動時に TiDB が接続する PDサーバーを示します。

</CustomContent>

### ddl_slow_threshold {#ddl-slow-threshold}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   実行時間がしきい値を超える DDL 操作をログに記録します。

### default_authentication_plugin {#default-authentication-plugin}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `mysql_native_password`
-   可能な値: `mysql_native_password` 、 `caching_sha2_password` 、 `tidb_sm3_password` 、および`tidb_auth_token`
-   `tidb_auth_token`認証方法は、 TiDB Cloudの内部操作のみに使用されます。変数をこの値に設定し**ないでください**。
-   この変数は、サーバーとクライアントの接続が確立されているときにサーバーが通知する認証方法を設定します。
-   `tidb_sm3_password`メソッドを使用して認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)を使用して TiDB に接続できます。

<CustomContent platform="tidb">

この変数のその他の可能な値については、 [認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status)を参照してください。

</CustomContent>

### default_password_lifetime <span class="version-mark">v6.5.0 の新機能</span> {#default-password-lifetime-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 65535]`
-   パスワードの自動有効期限切れのグローバル ポリシーを設定します。デフォルト値`0`は、パスワードが無期限であることを示します。このシステム変数が正の整数`N`に設定されている場合、パスワードの有効期間は`N`日間であり、 `N`日以内にパスワードを変更する必要があることを意味します。

### default_week_format {#default-week-format}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 7]`
-   `WEEK()`関数で使用される週の形式を設定します。

### disconnect_on_expired_password <span class="version-mark">v6.5.0 の新機能</span> {#disconnect-on-expired-password-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は読み取り専用です。パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを示します。変数が`ON`に設定されている場合、パスワードの有効期限が切れるとクライアント接続が切断されます。変数が`OFF`に設定されている場合、クライアント接続は「サンドボックス モード」に制限され、ユーザーはパスワードのリセット操作のみを実行できます。

<CustomContent platform="tidb">

-   期限切れのパスワードに対するクライアント接続の動作を変更する必要がある場合は、構成ファイルの[`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)構成項目を変更します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   期限切れのパスワードに対するクライアント接続のデフォルトの動作を変更する必要がある場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

### error_count {#error-count}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   メッセージを生成した最後のステートメントから発生したエラーの数を示す読み取り専用変数。

### Foreign_key_checks {#foreign-key-checks}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   互換性のために、TiDB は外部キー チェックを`OFF`として返します。

### group_concat_max_len {#group-concat-max-len}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[4, 18446744073709551615]`
-   `GROUP_CONCAT()`関数内の項目の最大バッファー サイズ。

### have_openssl {#have-openssl}

-   スコープ: なし
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQL との互換性のための読み取り専用変数。サーバーで TLS が有効になっている場合、サーバーによって`YES`に設定されます。

### have_ssl {#have-ssl}

-   スコープ: なし
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQL との互換性のための読み取り専用変数。サーバーで TLS が有効になっている場合、サーバーによって`YES`に設定されます。

### ホスト名 {#hostname}

-   スコープ: なし
-   デフォルト値: (システムのホスト名)
-   読み取り専用変数としての TiDBサーバーのホスト名。

### ID <span class="version-mark">v5.3.0 の新機能</span> {#identity-span-class-version-mark-new-in-v5-3-0-span}

この変数は[`last_insert_id`](#last_insert_id)のエイリアスです。

### init_connect {#init-connect}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: &quot;&quot;
-   `init_connect`機能により、最初に TiDBサーバーに接続したときに SQL ステートメントを自動的に実行できます。 `CONNECTION_ADMIN`または`SUPER`権限を持っている場合、この`init_connect`ステートメントは実行されません。 `init_connect`ステートメントでエラーが発生した場合、ユーザー接続は終了します。

### innodb_lock_wait_timeout {#innodb-lock-wait-timeout}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `50`
-   範囲: `[1, 3600]`
-   単位: 秒
-   悲観的トランザクションのロック待機タイムアウト (デフォルト)。

### interactive_timeout {#interactive-timeout}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[1, 31536000]`
-   単位: 秒
-   この変数は、対話型ユーザー セッションのアイドル タイムアウトを表します。対話型ユーザー セッションとは、 `CLIENT_INTERACTIVE`オプションを使用して[`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API を呼び出すことによって確立されたセッションを指します (たとえば、MySQL シェルと MySQL クライアント)。この変数は MySQL と完全に互換性があります。

### last_insert_id {#last-insert-id}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、insert ステートメントによって生成された最後の`AUTO_INCREMENT`または`AUTO_RANDOM`値を返します。
-   `last_insert_id`の値は、関数`LAST_INSERT_ID()`によって返される値と同じです。

### last_plan_from_binding <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-binding-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、前のステートメントで使用された実行計画が[製本](/sql-plan-management.md)影響を受けたかどうかを示すために使用されます。

### last_plan_from_cache <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-cache-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、前の`execute`ステートメントで使用された実行プランがプラン キャッシュから直接取得されたかどうかを示すために使用されます。

### last_sql_use_alloc <span class="version-mark">v6.4.0 の新機能</span> {#last-sql-use-alloc-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション
-   デフォルト値: `OFF`
-   この変数は読み取り専用です。前のステートメントがキャッシュされたチャンク オブジェクト (チャンク割り当て) を使用するかどうかを示すために使用されます。

### ライセンス {#license}

-   スコープ: なし
-   デフォルト値: `Apache License 2.0`
-   この変数は、TiDBサーバーのインストールのライセンスを示します。

### log_bin {#log-bin}

-   スコープ: なし
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [TiDBBinlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview)が使用されているかどうかを示します。

### max_allowed_packet <span class="version-mark">v6.1.0 の新機能</span> {#max-allowed-packet-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `67108864`
-   範囲: `[1024, 1073741824]`
-   値は 1024 の整数倍である必要があります。値が 1024 で割り切れない場合は、警告が表示され、値は切り捨てられます。たとえば、値が 1025 に設定されている場合、TiDB の実際の値は 1024 です。
-   サーバーとクライアントが 1 回のパケット送信で許可する最大パケット サイズ。
-   この変数は MySQL と互換性があります。

### password_history <span class="version-mark">v6.5.0 の新機能</span> {#password-history-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、TiDB がパスワードの変更回数に基づいてパスワードの再利用を制限できるパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、パスワードの変更回数に基づいてパスワード再利用ポリシーを無効にすることを意味します。この変数が正の整数`N`に設定されている場合、最後の`N`のパスワードの再使用は許可されません。

### password_reuse_interval <span class="version-mark">v6.5.0 の新機能</span> {#password-reuse-interval-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、経過時間に基づいて TiDB がパスワードの再利用を制限できるパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、経過時間に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数が正の整数`N`に設定されている場合、過去`N`日間に使用されたパスワードの再利用は許可されません。

### 最大接続数 {#max-connections}

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   1 つの TiDB インスタンスに許可される同時接続の最大数。この変数はリソース制御に使用できます。
-   デフォルト値`0`は制限なしを意味します。この変数の値が`0`よりも大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新しい接続を拒否します。

### max_execution_time {#max-execution-time}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   ステートメントの最大実行時間。デフォルト値は無制限 (ゼロ) です。

> **ノート：**
>
> MySQL とは異なり、システム変数`max_execution_time`は現在、TiDB のすべての種類のステートメントで機能し、 `SELECT`ステートメントに限定されません。タイムアウト値の精度は約 100ms です。これは、指定した正確なミリ秒でステートメントが終了しない可能性があることを意味します。

<CustomContent platform="tidb">

ヒントが[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) SQL ステートメントの場合、このステートメントの最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、説明されているように SQL バインディングでも使用できます[SQL FAQで](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

ヒントが[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) SQL ステートメントの場合、このステートメントの最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、説明されているように SQL バインディングでも使用できます[SQL FAQで](https://docs.pingcap.com/tidb/stable/sql-faq) 。

</CustomContent>

### max_prepared_stmt_count {#max-prepared-stmt-count}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 1048576]`
-   現在の TiDB インスタンス内の[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントの最大数を指定します。
-   値`-1`は、現在の TiDB インスタンスのステートメントの最大数`PREPARE`に制限がないことを意味します。
-   変数を上限`1048576`を超える値に設定すると、代わりに`1048576`が使用されます。

```sql
mysql> SET GLOBAL max_prepared_stmt_count = 1048577;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------------+
| Level   | Code | Message                                                      |
+---------+------+--------------------------------------------------------------+
| Warning | 1292 | Truncated incorrect max_prepared_stmt_count value: '1048577' |
+---------+------+--------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'max_prepared_stmt_count';
+-------------------------+---------+
| Variable_name           | Value   |
+-------------------------+---------+
| max_prepared_stmt_count | 1048576 |
+-------------------------+---------+
1 row in set (0.00 sec)
```

### plugin_dir {#plugin-dir}

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: &quot;&quot;
-   コマンドライン フラグで指定されたプラグインをロードするディレクトリを示します。

### plugin_load {#plugin-load}

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: &quot;&quot;
-   TiDB の起動時にロードするプラグインを示します。これらのプラグインは、コマンドライン フラグによって指定され、カンマで区切られます。

### ポート {#port}

-   スコープ: なし
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 65535]`
-   MySQL プロトコルを話すときに`tidb-server`がリッスンしているポート。

### rand_seed1 {#rand-seed1}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL 関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作は MySQL と互換性があります。

### rand_seed2 {#rand-seed2}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL 関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作は MySQL と互換性があります。

### require_secure_transport <span class="version-mark">v6.1.0 の新機能</span> {#require-secure-transport-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、TiDB へのすべての接続がローカル ソケット上にあるか、TLS を使用していることを保証します。詳細については[TiDB クライアントとサーバー間の TLS を有効にする](/enable-tls-between-clients-and-servers.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB へのすべての接続がローカル ソケット上にあるか、TLS を使用していることを保証します。

</CustomContent>

-   この変数を`ON`に設定するには、TLS が有効になっているセッションから TiDB に接続する必要があります。これにより、TLS が正しく構成されていない場合のロックアウト シナリオを防ぐことができます。
-   この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。

### skip_name_resolve <span class="version-mark">v5.2.0 の新機能</span> {#skip-name-resolve-span-class-version-mark-new-in-v5-2-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `tidb-server`インスタンスが接続ハンドシェイクの一部としてホスト名を解決するかどうかを制御します。
-   DNS が信頼できない場合、このオプションを有効にしてネットワーク パフォーマンスを向上させることができます。

> **ノート：**
>
> `skip_name_resolve=ON`の場合、ID にホスト名を持つユーザーはサーバーにログインできなくなります。例えば：
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> この例では、 `apphost` IP アドレスまたはワイルドカード ( `%` ) に置き換えることをお勧めします。

### ソケット {#socket}

-   スコープ: なし
-   デフォルト値: &quot;&quot;
-   MySQL プロトコルを話すときに`tidb-server`がリッスンしているローカル UNIX ソケット ファイル。

### sql_log_bin {#sql-log-bin}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   変更を[TiDBBinlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview)に書き込むかどうかを示します。

> **ノート：**
>
> TiDB の将来のバージョンでは、これをセッション変数としてのみ設定できるようになる可能性があるため、 `sql_log_bin`グローバル変数として設定することはお勧めしません。

### sql_mode {#sql-mode}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
-   この変数は、多数の MySQL 互換性動作を制御します。詳細については[SQL モード](/sql-mode.md)参照してください。

### sql_require_primary_key <span class="version-mark">v6.3.0 の新機能</span> {#sql-require-primary-key-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、テーブルに主キーがあるという要件を適用するかどうかを制御します。この変数を有効にした後、主キーなしでテーブルを作成または変更しようとすると、エラーが発生します。
-   この機能は、MySQL 8.0 の同様の名前の[`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key)に基づいています。
-   TiCDC を使用する場合は、この変数を有効にすることを強くお勧めします。これは、変更を MySQL シンクにレプリケートするには、テーブルにプライマリ キーが必要なためです。

### sql_select_limit <span class="version-mark">v4.0.2 の新機能</span> {#sql-select-limit-span-class-version-mark-new-in-v4-0-2-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `18446744073709551615`
-   範囲: `[0, 18446744073709551615]`
-   単位: 行
-   `SELECT`ステートメントによって返される行の最大数。

### ssl_ca {#ssl-ca}

<CustomContent platform="tidb">

-   スコープ: なし
-   デフォルト値: &quot;&quot;
-   認証局ファイルの場所 (存在する場合)。この変数の値は、TiDB 構成項目[`ssl-ca`](/tidb-configuration-file.md#ssl-ca)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   スコープ: なし
-   デフォルト値: &quot;&quot;
-   認証局ファイルの場所 (存在する場合)。この変数の値は、TiDB 構成項目[`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca)によって定義されます。

</CustomContent>

### ssl_cert {#ssl-cert}

<CustomContent platform="tidb">

-   スコープ: なし
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される証明書ファイルの場所 (ファイルがある場合)。この変数の値は、TiDB 構成項目[`ssl-cert`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   スコープ: なし
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される証明書ファイルの場所 (ファイルがある場合)。この変数の値は、TiDB 構成項目[`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert)によって定義されます。

</CustomContent>

### ssl_key {#ssl-key}

<CustomContent platform="tidb">

-   スコープ: なし
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される秘密鍵ファイル (存在する場合) の場所。この変数の値は、TiDB 構成項目[`ssl-key`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   スコープ: なし
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される秘密鍵ファイル (存在する場合) の場所。この変数の値は、TiDB 構成項目[`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key)によって定義されます。

</CustomContent>

### system_time_zone {#system-time-zone}

-   スコープ: なし
-   デフォルト値: (システムに依存)
-   この変数は、TiDB が最初にブートストラップされたときのシステム タイム ゾーンを示します。 [`time_zone`](#time_zone)も参照してください。

### tidb_adaptive_closest_read_threshold <span class="version-mark">v6.3.0 の新機能</span> {#tidb-adaptive-closest-read-threshold-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `4096`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、 [`tidb_replica_read`](#tidb_replica_read-new-in-v40)が`closest-adaptive`に設定されている場合に、TiDBサーバーがTiDBサーバーと同じ可用性ゾーン内のレプリカに読み取り要求を送信することを好むしきい値を制御するために使用されます。推定結果がこのしきい値以上の場合、TiDB は同じ可用性ゾーン内のレプリカに読み取り要求を送信することを優先します。それ以外の場合、TiDB は読み取り要求をリーダー レプリカに送信します。

### tidb_allow_batch_cop <span class="version-mark">v4.0 の新機能</span> {#tidb-allow-batch-cop-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   この変数は、TiDB がコプロセッサー要求をTiFlashに送信する方法を制御するために使用されます。次の値があります。

    -   `0` : リクエストをバッチで送信しない
    -   `1` :集計および結合要求はバッチで送信されます
    -   `2` : すべてのコプロセッサー要求がバッチで送信されます

### tidb_allow_fallback_to_tikv <span class="version-mark">v5.0 の新機能</span> {#tidb-allow-fallback-to-tikv-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: &quot;&quot;
-   この変数は、TiKV にフォールバックするstorageエンジンのリストを指定するために使用されます。リスト内の指定されたstorageエンジンの障害が原因で SQL ステートメントの実行が失敗した場合、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。この変数は、&quot;&quot; または &quot;tiflash&quot; に設定できます。この変数が「tiflash」に設定されている場合、 TiFlash がタイムアウト エラー (エラー コード: ErrTiFlashServerTimeout) を返した場合、TiDB は TiKV でこの SQL ステートメントの実行をリトライします。

### tidb_allow_function_for_expression_index <span class="version-mark">v5.2.0 の新機能</span> {#tidb-allow-function-for-expression-index-span-class-version-mark-new-in-v5-2-0-span}

-   スコープ: なし
-   `json_contains` `json_array_insert` `json_array_append` `json_array` `json_contains_path` `json_depth` `json_extract` `json_insert` `json_keys` `json_length` `json_merge_patch` `json_merge_preserve` `json_object` `json_pretty` `json_quote` `json_remove` `json_replace` `json_search` `json_set` `json_storage_size` `json_type` `json_unquote` `json_valid` `lower` , `md5` , `reverse` , `tidb_shard` , `upper` , `vitess_hash`
-   この変数は、式インデックスの作成に使用できる関数を示すために使用されます。

### tidb_allow_mpp <span class="version-mark">v5.0 の新機能</span> {#tidb-allow-mpp-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiFlashの MPP モードを使用してクエリを実行するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF` 。これは、MPP モードが使用されないことを意味します。
    -   `1`または`ON` 。これは、オプティマイザーが (デフォルトで) コストの見積もりに基づいて MPP モードを使用するかどうかを決定することを意味します。

MPP は、 TiFlashエンジンによって提供される分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能で高スループットの SQL アルゴリズムを提供します。 MPP モードの選択については、 [MPP モードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_allow_remove_auto_inc <span class="version-mark">v2.1.18 および v3.0.4 の新機能</span> {#tidb-allow-remove-auto-inc-span-class-version-mark-new-in-v2-1-18-and-v3-0-4-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`ステートメントを実行して列の`AUTO_INCREMENT`のプロパティを削除できるかどうかを設定するために使用されます。デフォルトでは許可されていません。

### tidb_analyze_partition_concurrency {#tidb-analyze-partition-concurrency}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `1`
-   この変数は、TiDB がパーティションテーブルを分析するときに、パーティションテーブルの統計の読み取りと書き込みの同時実行性を指定します。

### tidb_analyze_version <span class="version-mark">v5.1.0 の新機能</span> {#tidb-analyze-version-span-class-version-mark-new-in-v5-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: オンプレミス TiDB の場合は`2` 、 TiDB Cloudの場合は`1`
-   範囲: `[1, 2]`
-   TiDB が統計を収集する方法を制御します。

<CustomContent platform="tidb">

-   v5.3.0 以降のバージョンでは、この変数のデフォルト値は`2`です。クラスターが v5.3.0 より前のバージョンから v5.3.0 以降にアップグレードされた場合、デフォルト値の`tidb_analyze_version`は変更されません。詳細な紹介については、 [統計入門](/statistics.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数の詳細については、 [統計入門](/statistics.md)を参照してください。

</CustomContent>

### tidb_auto_analyze_end_time {#tidb-auto-analyze-end-time}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、午前 1 時から午前 3 時までの自動統計更新のみを許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`を設定します。

### tidb_auto_analyze_partition_batch_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-auto-analyze-partition-batch-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `1`
-   範囲: `[1, 1024]`
-   この変数は、パーティションテーブルを分析するときに TiDB [自動分析](/statistics.md#automatic-update)が使用するパーティションの数を指定します (つまり、パーティションテーブルの統計を自動的に収集することを意味します)。
-   この変数の値がパーティションの数よりも小さい場合、TiDB はパーティションテーブルのすべてのパーティションを複数のバッチで自動的に分析します。この変数の値がパーティションの数以上の場合、TiDB はパーティションテーブルのすべてのパーティションを同時に分析します。
-   パーティションテーブルのパーティション数がこの変数の値よりもはるかに多く、自動分析に時間がかかる場合は、この変数の値を増やして時間の消費を減らすことができます。

### tidb_auto_analyze_ratio {#tidb-auto-analyze-ratio}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.5`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、TiDB がテーブル統計を更新するためにバックグラウンド スレッドで[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)自動的に実行するときのしきい値を設定するために使用されます。たとえば、値 0.5 は、テーブル内の行の 50% 以上が変更されたときに自動分析がトリガーされることを意味します。自動分析は、 `tidb_auto_analyze_start_time`および`tidb_auto_analyze_end_time`を指定することにより、1 日の特定の時間帯のみに実行するように制限できます。

> **ノート：**
>
> この機能には、システム変数`tidb_enable_auto_analyze`を`ON`に設定する必要があります。

### tidb_auto_analyze_start_time {#tidb-auto-analyze-start-time}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、午前 1 時から午前 3 時までの自動統計更新のみを許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`を設定します。

### tidb_auto_build_stats_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-auto-build-stats-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、統計の自動更新の同時実行を設定するために使用されます。

### tidb_backoff_lock_fast {#tidb-backoff-lock-fast}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 2147483647]`
-   この変数は、読み取り要求がロックに一致する`backoff`回を設定するために使用されます。

### tidb_backoff_weight {#tidb-backoff-weight}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB `backoff`の最大時間、つまり、内部ネットワークまたは他のコンポーネント(TiKV、PD) の障害が発生したときにリトライ要求を送信するための最大リトライ時間の重みを増やすために使用されます。この変数は、最大再試行時間を調整するために使用でき、最小値は 1 です。

    たとえば、TiDB が PD から TSO を取得するための基本タイムアウトは 15 秒です。 `tidb_backoff_weight = 2`の場合、TSO 取得の最大タイムアウトは、*基本時間 * 2 = 30 秒*です。

    ネットワーク環境が劣悪な場合、この変数の値を適切に増やすと、タイムアウトによってアプリケーション側に報告されるエラーを効果的に軽減できます。アプリケーション側でエラー情報をより迅速に受け取りたい場合は、この変数の値を最小限に抑えてください。

### tidb_batch_commit {#tidb-batch-commit}

> **警告：**
>
> この変数を有効にすることはお勧めしませ**ん**。

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチコミット機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、いくつかのステートメントをグループ化することでトランザクションが複数のトランザクションに分割され、非アトミックにコミットされる可能性がありますが、これはお勧めできません。

### tidb_batch_delete {#tidb-batch-delete}

> **警告：**
>
> この変数は非推奨の batch-dml 機能に関連付けられており、データが破損する可能性があります。したがって、batch-dml でこの変数を有効にすることはお勧めしません。代わりに、 [非トランザクション DML](/non-transactional-dml.md)を使用してください。

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチ dml 機能の一部であるバッチ削除機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `DELETE`のステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`有効にして`tidb_dml_batch_size`に正の値を設定する必要もありますが、これはお勧めできません。

### tidb_batch_insert {#tidb-batch-insert}

> **警告：**
>
> この変数は非推奨の batch-dml 機能に関連付けられており、データが破損する可能性があります。したがって、batch-dml でこの変数を有効にすることはお勧めしません。代わりに、 [非トランザクション DML](/non-transactional-dml.md)を使用してください。

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチ dml 機能の一部であるバッチ挿入機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `INSERT`のステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`有効にして`tidb_dml_batch_size`に正の値を設定する必要もありますが、これはお勧めできません。

### tidb_batch_pending_tiflash_count <span class="version-mark">v6.0 の新機能</span> {#tidb-batch-pending-tiflash-count-span-class-version-mark-new-in-v6-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 4294967295]`
-   `ALTER DATABASE SET TIFLASH REPLICA`を使用してTiFlashレプリカを追加する場合に、許容される使用不可テーブルの最大数を指定します。使用できないテーブルの数がこの制限を超えると、操作が停止するか、残りのテーブルのTiFlashレプリカの設定が非常に遅くなります。

### tidb_broadcast_join_threshold_count <span class="version-mark">v5.0 の新機能</span> {#tidb-broadcast-join-threshold-count-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `10240`
-   範囲: `[0, 9223372036854775807]`
-   単位: 行
-   結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを見積もることができません。この場合、サイズは結果セットの行数によって決まります。サブクエリの推定行数がこの変数の値より少ない場合、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、Shuffled Hash Join アルゴリズムが使用されます。

### tidb_broadcast_join_threshold_size <span class="version-mark">v5.0 の新機能</span> {#tidb-broadcast-join-threshold-size-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `104857600` (100 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   テーブル サイズが変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、Shuffled Hash Join アルゴリズムが使用されます。

### tidb_build_stats_concurrency {#tidb-build-stats-concurrency}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `ANALYZE`ステートメントの同時実行を設定するために使用されます。
-   変数に大きな値を設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_capture_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-capture-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [ベースラインのキャプチャ](/sql-plan-management.md#baseline-capturing)機能を有効にするかどうかを制御するために使用されます。この機能はステートメント サマリーに依存するため、ベースライン キャプチャを使用する前にステートメント サマリーを有効にする必要があります。
-   この機能を有効にすると、ステートメント サマリーの履歴 SQL ステートメントが定期的に走査され、少なくとも 2 回出現する SQL ステートメントのバインドが自動的に作成されます。

### tidb_cdc_write_source <span class="version-mark">v6.5.0 の新機能</span> {#tidb-cdc-write-source-span-class-version-mark-new-in-v6-5-0-span}

-   スコープ: セッション
-   クラスターに永続化: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数が 0 以外の値に設定されている場合、このセッションで書き込まれたデータは TiCDC によって書き込まれたと見なされます。この変数は、TiCDC によってのみ変更できます。どのような場合でも、この変数を手動で変更しないでください。

### tidb_check_mb4_value_in_utf8 {#tidb-check-mb4-value-in-utf8}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `utf8`文字セットが[基本多言語面 (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane)からの値のみを格納することを強制するために使用されます。 BMP の外に文字を格納するには、 `utf8mb4`文字セットを使用することをお勧めします。
-   `utf8`のチェックがより緩和された以前のバージョンの TiDB からクラスターをアップグレードする場合は、このオプションを無効にする必要がある場合があります。詳細については、 [アップグレード後の FAQ](https://docs.pingcap.com/tidb/stable/upgrade-faq)を参照してください。

### tidb_checksum_table_concurrency {#tidb-checksum-table-concurrency}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)ステートメントを実行するスキャン インデックスの同時実行数を設定するために使用されます。
-   変数に大きな値を設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_committer_concurrency <span class="version-mark">v6.1.0 の新機能</span> {#tidb-committer-concurrency-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `128`
-   範囲: `[1, 10000]`
-   単一トランザクションのコミット フェーズでのコミットの実行に関連する要求のゴルーチンの数。
-   コミットするトランザクションが大きすぎる場合、トランザクションがコミットされるときのフロー制御キューの待機時間が長すぎる可能性があります。この状況では、構成値を増やしてコミットを高速化できます。
-   この設定は以前は`tidb.toml`オプション ( `performance.committer-concurrency` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。

### tidb_config {#tidb-config}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: &quot;&quot;
-   この変数は読み取り専用です。現在の TiDBサーバーの構成情報を取得するために使用されます。

### tidb_constraint_check_in_place {#tidb-constraint-check-in-place}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は楽観的トランザクションにのみ適用されます。悲観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-new-in-v630)を使用してください。
-   この変数が`OFF`に設定されている場合、一意のインデックス内の重複値のチェックは、トランザクションがコミットされるまで延期されます。これはパフォーマンスの向上に役立ちますが、一部のアプリケーションでは予期しない動作になる場合があります。詳細は[制約](/constraints.md#optimistic-transactions)参照してください。

    -   `tidb_constraint_check_in_place` ～ `OFF`を設定し、楽観的トランザクションを使用する場合:

        ```sql
        tidb> create table t (i int key);
        tidb> insert into t values (1);
        tidb> begin optimistic;
        tidb> insert into t values (1);
        Query OK, 1 row affected
        tidb> commit; -- Check only when a transaction is committed.
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    -   `tidb_constraint_check_in_place` ～ `ON`を設定し、楽観的トランザクションを使用する場合:

        ```sql
        tidb> set @@tidb_constraint_check_in_place=ON;
        tidb> begin optimistic;
        tidb> insert into t values (1);
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_constraint_check_in_place_pessimistic <span class="version-mark">v6.3.0 の新機能</span> {#tidb-constraint-check-in-place-pessimistic-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: デフォルトでは、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)構成アイテムは`true`であるため、この変数のデフォルト値は`ON`です。 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)が`false`に設定されている場合、この変数のデフォルト値は`OFF`です。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`

</CustomContent>

-   この変数は悲観的トランザクションにのみ適用されます。楽観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place)を使用してください。
-   この変数が`OFF`に設定されている場合、TiDB は一意のインデックスの一意の制約チェックを延期します (インデックスへのロックを必要とするステートメントを次に実行するとき、またはトランザクションをコミットするときまで)。これはパフォーマンスの向上に役立ちますが、一部のアプリケーションでは予期しない動作になる場合があります。詳細は[制約](/constraints.md#pessimistic-transactions)参照してください。
-   この変数を無効にすると、悲観的トランザクションで TiDB が`LazyUniquenessCheckFailure`エラーを返す可能性があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。
-   この変数が無効になっている場合、悲観的トランザクションでは[`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)を使用できません。
-   この変数が無効になっている場合、悲観的トランザクションをコミットすると、 `Write conflict`または`Duplicate entry`エラーが返される場合があります。このようなエラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    -   `tidb_constraint_check_in_place_pessimistic` ～ `OFF`を設定し、悲観的トランザクションを使用する場合:

        {{< copyable "" >}}

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=OFF;
        create table t (i int key);
        insert into t values (1);
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        Query OK, 1 row affected
        ```

        ```sql
        tidb> commit; -- Check only when a transaction is committed.
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    -   `tidb_constraint_check_in_place_pessimistic` ～ `ON`を設定し、悲観的トランザクションを使用する場合:

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_cost_model_version <span class="version-mark">v6.2.0 の新機能</span> {#tidb-cost-model-version-span-class-version-mark-new-in-v6-2-0-span}

> **ノート：**
>
> -   TiDB v6.5.0 以降、新しく作成されたクラスターはデフォルトでコスト モデル バージョン 2 を使用します。 v6.5.0 より前の TiDB バージョンから v6.5.0 以降にアップグレードする場合、 `tidb_cost_model_version`値は変更されません。
> -   コスト モデルのバージョンを切り替えると、クエリ プランが変更される場合があります。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   値のオプション:
    -   `1` : TiDB v6.4.0 以前のバージョンでデフォルトで使用されるコスト モデル バージョン 1 を有効にします。
    -   `2` : [コスト モデル バージョン 2](/cost-model.md#cost-model-version-2)有効にします。これは TiDB v6.5.0 で一般的に利用可能であり、内部テストでバージョン 1 よりも正確です。
-   コスト モデルのバージョンは、オプティマイザの計画決定に影響します。詳細については、 [コストモデル](/cost-model.md)を参照してください。

### tidb_current_ts {#tidb-current-ts}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は読み取り専用です。現在のトランザクションのタイムスタンプを取得するために使用されます。

### tidb_ddl_disk_quota <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-disk-quota-span-class-version-mark-new-in-v6-3-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。 TiDB Cloudのこの変数のデフォルト値を変更しないでください。

</CustomContent>

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `107374182400` (100 GiB)
-   範囲: `[107374182400, 1125899906842624]` ([100 GiB、1 PiB])
-   単位: バイト
-   この変数は、 [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630)が有効になっている場合にのみ有効です。インデックス作成時のバックフィル時のローカルstorageの使用制限を設定します。

### tidb_ddl_enable_fast_reorg <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-enable-fast-reorg-span-class-version-mark-new-in-v6-3-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この変数を使用してインデックス作成の速度を向上させるには、TiDB クラスターが AWS でホストされ、TiDB ノードのサイズが少なくとも 8 vCPU であることを確認してください。 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターの場合、この機能は使用できません。

</CustomContent>

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `ADD INDEX`と`CREATE INDEX`のアクセラレーションを有効にして、インデックス作成のバックフィルの速度を向上させるかどうかを制御します。この変数の値を`ON`に設定すると、大量のデータを含むテーブルでのインデックス作成のパフォーマンスが向上する可能性があります。
-   完了した`ADD INDEX`操作が高速化されるかどうかを確認するには、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)ステートメントを実行して、 `JOB_TYPE`列に`ingest`が表示されるかどうかを確認します。

<CustomContent platform="tidb">

> **警告：**
>
> 現在、この機能は一意のインデックスの追加と完全には互換性がありません。ユニーク インデックスを追加する場合は、インデックス アクセラレーション機能を無効にすることをお勧めします ( `tidb_ddl_enable_fast_reorg` ～ `OFF`を設定)。
>
> [PITR (ポイントインタイム リカバリ)](/br/backup-and-restore-overview.md)を無効にすると、v6.1.0 の約 10 倍のインデックス追加速度が期待できます。ただし、PITR とインデックス アクセラレーションの両方が有効になっている場合、パフォーマンスは向上しません。パフォーマンスを最適化するには、PITR を無効にし、すばやくインデックスを追加してから、PITR を有効にしてフル バックアップを実行することをお勧めします。そうしないと、次の動作が発生する可能性があります。
>
> -   PITR が最初に動作を開始すると、構成が`ON`に設定されていても、インデックス追加ジョブは既定で自動的にレガシー モードに戻ります。インデックスはゆっくりと追加されます。
> -   インデックス追加ジョブが最初に開始されると、エラーをスローして PITR のログ バックアップ ジョブが開始されないようにします。これは、進行中のインデックス追加ジョブには影響しません。インデックス追加ジョブが完了したら、ログ バックアップ ジョブを再開し、完全バックアップを手動で実行する必要があります。
> -   PITR のログバックアップジョブとインデックス追加ジョブが同時に開始された場合、2 つのジョブがお互いを検出できないため、エラーは発生しません。 PITR は、新しく追加されたインデックスをバックアップしません。インデックス追加ジョブが完了したら、ログ バックアップ ジョブを再開し、手動でフル バックアップを実行する必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> 現在、この機能は[単一の`ALTER TABLE`ステートメントで複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md)と完全には互換性がありません。インデックス アクセラレーションを使用して一意のインデックスを追加する場合は、同じステートメントで他の列またはインデックスを変更しないようにする必要があります。
>
> [PITR (ポイントインタイム リカバリ)](/tidb-cloud/backup-and-restore.md)を無効にすると、v6.1.0 の約 10 倍のインデックス追加速度が期待できます。ただし、PITR とインデックス アクセラレーションの両方が有効になっている場合、パフォーマンスは向上しません。パフォーマンスを最適化するには、PITR を無効にし、すばやくインデックスを追加してから、PITR を有効にしてフル バックアップを実行することをお勧めします。そうしないと、次の予期される動作が発生する可能性があります。
>
> -   PITR が最初に動作を開始すると、構成が`ON`に設定されていても、インデックス追加ジョブは既定で自動的にレガシー モードに戻ります。インデックスはゆっくりと追加されます。
> -   インデックス追加ジョブが最初に開始されると、エラーをスローして PITR のログ バックアップ ジョブが開始されないようにします。これは、進行中のインデックス追加ジョブには影響しません。インデックス追加ジョブが完了したら、ログ バックアップ ジョブを再開し、完全バックアップを手動で実行する必要があります。
> -   PITR のログバックアップジョブとインデックス追加ジョブが同時に開始された場合、2 つのジョブがお互いを検出できないため、エラーは発生しません。 PITR は、新しく追加されたインデックスをバックアップしません。インデックス追加ジョブが完了したら、ログ バックアップ ジョブを再開し、手動でフル バックアップを実行する必要があります。

</CustomContent>

### tidb_ddl_error_count_limit {#tidb-ddl-error-count-limit}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `512`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、DDL 操作が失敗した場合の再試行回数を設定するために使用されます。再試行回数がパラメーター値を超えると、間違った DDL 操作が取り消されます。

### tidb_ddl_flashback_concurrency <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-flashback-concurrency-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `64`
-   範囲: `[1, 256]`
-   この変数は[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)の並行性を制御します。

### tidb_ddl_reorg_batch_size {#tidb-ddl-reorg-batch-size}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `256`
-   範囲: `[32, 10240]`
-   単位: 行
-   この変数は、DDL 操作の`re-organize`フェーズでバッチ サイズを設定するために使用されます。たとえば、TiDB が`ADD INDEX`操作を実行する場合、インデックス データは`tidb_ddl_reorg_worker_cnt` (数) の同時ワーカーによってバックフィルされる必要があります。各ワーカーは、バッチでインデックス データをバックフィルします。
    -   `ADD INDEX`操作中に`UPDATE`や`REPLACE`などの多くの更新操作が存在する場合、バッチ サイズが大きいほど、トランザクションの競合が発生する可能性が高くなります。この場合、バッチ サイズをより小さい値に調整する必要があります。最小値は 32 です。
    -   トランザクションの競合が存在しない場合は、バッチ サイズを大きな値に設定できます (ワーカー数を考慮してください。参考として[オンライン ワークロードと`ADD INDEX`操作の相互作用テスト](https://docs.pingcap.com/tidb/stable/online-workloads-and-add-index-operations)を参照してください)。これにより、データのバックフィルの速度を上げることができますが、TiKV への書き込み圧力も高くなります。

### tidb_ddl_reorg_priority {#tidb-ddl-reorg-priority}

-   スコープ: セッション
-   タイプ: 列挙
-   デフォルト値: `PRIORITY_LOW`
-   値のオプション: `PRIORITY_LOW` 、 `PRIORITY_NORMAL` 、 `PRIORITY_HIGH`
-   この変数は、 `re-organize`フェーズで`ADD INDEX`操作を実行する優先順位を設定するために使用されます。
-   この変数の値は`PRIORITY_LOW` 、 `PRIORITY_NORMAL`または`PRIORITY_HIGH`に設定できます。

### tidb_ddl_reorg_worker_cnt {#tidb-ddl-reorg-worker-cnt}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `re-organize`フェーズでの DDL 操作の並行性を設定するために使用されます。

### tidb_default_string_match_selectivity <span class="version-mark">v6.2.0 の新機能</span> {#tidb-default-string-match-selectivity-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.8`
-   範囲: `[0, 1]`
-   この変数は、行数を見積もるときのフィルタ条件で`like` 、 `rlike` 、および`regexp`関数のデフォルトの選択性を設定するために使用されます。この変数は、TopN を有効にしてこれらの関数を推定するかどうかも制御します。
-   TiDB は、統計を使用してフィルター条件で`like`を推定しようとします。しかし、 `like`複雑な文字列に一致する場合、または`rlike`または`regexp`を使用する場合、TiDB はしばしば統計を十分に活用できず、代わりにデフォルト値`0.8`選択率として設定され、結果として不正確な推定が行われます。
-   この変数は、前述の動作を変更するために使用されます。変数が`0`以外の値に設定されている場合、選択率は`0.8`ではなく、指定された変数値になります。
-   変数が`0`に設定されている場合、TiDB は統計で TopN を使用して評価を試み、精度を向上させ、前の 3 つの関数を推定するときに統計で NULL 数を考慮します。前提条件は、 [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510) `2`に設定されたときに統計が収集されることです。そのような評価は、パフォーマンスにわずかに影響を与える可能性があります。
-   変数が`0.8`以外の値に設定されている場合、TiDB はそれに応じて`not like` 、 `not rlike` 、および`not regexp`の推定値を調整します。

### tidb_disable_txn_auto_retry {#tidb-disable-txn-auto-retry}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、明示的楽観的トランザクションの自動再試行を無効にするかどうかを設定するために使用されます。デフォルト値`ON` 、トランザクションが TiDB で自動的に再試行されず、 `COMMIT`のステートメントがアプリケーションレイヤーで処理する必要があるエラーを返す可能性があることを意味します。

    値を`OFF`に設定すると、TiDB が自動的にトランザクションを再試行し、 `COMMIT`ステートメントからのエラーが少なくなります。更新が失われる可能性があるため、この変更を行うときは注意してください。

    この変数は、自動的にコミットされた暗黙のトランザクションと、TiDB で内部的に実行されるトランザクションには影響しません。これらのトランザクションの最大再試行回数は、 `tidb_retry_limit`の値によって決まります。

    詳細については、 [再試行の制限](/optimistic-transaction.md#limits-of-retry)を参照してください。

    <CustomContent platform="tidb">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は[`max_retry_count`](/tidb-configuration-file.md#max-retry-count)で制御されます。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションのリトライ回数は 256 回です。

    </CustomContent>

### tidb_distsql_scan_concurrency {#tidb-distsql-scan-concurrency}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `15`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `scan`操作の並行性を設定するために使用されます。
-   OLAP シナリオでは大きな値を使用し、OLTP シナリオでは小さな値を使用します。
-   OLAP シナリオの場合、最大値はすべての TiKV ノードの CPU コア数を超えてはなりません。
-   テーブルに多数のパーティションがある場合は、TiKV がメモリ不足 (OOM) にならないように、(スキャンするデータのサイズとスキャンの頻度によって決定される) 変数値を適切に減らすことができます。

### tidb_dml_batch_size {#tidb-dml-batch-size}

> **警告：**
>
> この変数は非推奨の batch-dml 機能に関連付けられており、データが破損する可能性があります。したがって、batch-dml でこの変数を有効にすることはお勧めしません。代わりに、 [非トランザクション DML](/non-transactional-dml.md)を使用してください。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: 行
-   この値が`0`より大きい場合、TiDB は`INSERT`や`LOAD DATA`などの commit ステートメントを小さなトランザクションにバッチ処理します。これにより、メモリ使用量が削減され、一括変更によって`txn-total-size-limit`に到達しないことが保証されます。
-   値`0`のみがACID準拠を提供します。これを他の値に設定すると、TiDB の原子性と分離の保証が壊れます。
-   この変数を機能させるには、 `tidb_enable_batch_dml`と、少なくとも`tidb_batch_insert`と`tidb_batch_delete`の 1 つを有効にする必要もあります。

### tidb_enable_1pc <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-1pc-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、1 つのリージョンのみに影響するトランザクションに対して 1 フェーズ コミット機能を有効にするかどうかを指定するために使用されます。よく使用される 2 フェーズ コミットと比較して、1 フェーズ コミットはトランザクション コミットのレイテンシーを大幅に短縮し、スループットを向上させることができます。

> **ノート：**
>
> -   デフォルト値の`ON`新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   TiDB Binlogを有効にしている場合、この変数を有効にしてもパフォーマンスは向上しません。パフォーマンスを向上させるには、代わりに[TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)を使用することをお勧めします。
> -   このパラメーターを有効にすることは、1 フェーズ コミットがトランザクション コミットのオプション モードになることを意味するだけです。実際、トランザクション コミットの最適なモードは TiDB によって決定されます。

### tidb_enable_amend_pessimistic_txn <span class="version-mark">v4.0.7 の新機能</span> {#tidb-enable-amend-pessimistic-txn-span-class-version-mark-new-in-v4-0-7-span}

> **警告：**
>
> v6.5.0 以降、この変数は廃止され、TiDB はデフォルトで[メタデータ ロック](/metadata-lock.md)機能を使用して`Information schema is changed`エラーを回避します。この変数は v6.6.0 で削除される予定であることに注意してください。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `AMEND TRANSACTION`機能を有効にするかどうかを制御するために使用されます。悲観的トランザクションで`AMEND TRANSACTION`機能を有効にした場合、同時 DDL 操作と SCHEMA VERSION 変更がこのトランザクションに関連付けられたテーブルに存在する場合、TiDB はトランザクションの修正を試みます。 TiDB は、トランザクション コミットを修正して、コミットが最新の有効な SCHEMA VERSION と一致するようにし、トランザクションが`Information schema is changed`エラーを取得することなく正常にコミットできるようにします。この機能は、次の同時 DDL 操作で有効です。

    -   `ADD COLUMN`または`DROP COLUMN`の操作。
    -   フィールドの長さを増やす`MODIFY COLUMN`または`CHANGE COLUMN`の操作。
    -   トランザクションが開かれる前にインデックス列が作成される`ADD INDEX`または`DROP INDEX`の操作。

> **ノート：**
>
> 現在、この機能は一部のシナリオで TiDB Binlogと互換性がなく、トランザクションでセマンティックの変更を引き起こす可能性があります。この機能の使用上の注意事項については、 [トランザクション セマンティックに関する非互換性の問題](https://github.com/pingcap/tidb/issues/21069)および[TiDB Binlogに関する非互換性の問題](https://github.com/pingcap/tidb/issues/20996)を参照してください。

### tidb_enable_analyze_snapshot <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-analyze-snapshot-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、実行時に過去のデータを読み取るか最新のデータを読み取るかを制御します`ANALYZE` 。この変数が`ON`に設定されている場合、 `ANALYZE` `ANALYZE`の時点で使用可能な履歴データを読み取ります。この変数が`OFF`に設定されている場合、 `ANALYZE`最新のデータを読み取ります。
-   v5.2 より前では、 `ANALYZE`最新のデータが読み取られます。 v5.2 から v6.1 まで、 `ANALYZE` `ANALYZE`の時点で使用可能な履歴データを読み取ります。

> **警告：**
>
> `ANALYZE` `ANALYZE`の時点で使用可能な履歴データを読み取る場合、履歴データはガベージ コレクションされるため、 `AUTO ANALYZE`の長い期間によって`GC life time is shorter than transaction duration`エラーが発生する可能性があります。

### tidb_enable_async_commit <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-async-commit-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、2 フェーズ トランザクション コミットの第 2 フェーズの非同期コミット機能を有効にして、バックグラウンドで非同期に実行するかどうかを制御します。この機能を有効にすると、トランザクション コミットのレイテンシーを短縮できます。

> **ノート：**
>
> -   デフォルト値の`ON`新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   TiDB Binlogを有効にしている場合、この変数を有効にしてもパフォーマンスは向上しません。パフォーマンスを向上させるには、代わりに[TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)を使用することをお勧めします。
> -   このパラメーターを有効にすることは、Async Commit がトランザクション コミットのオプション モードになることを意味するだけです。実際、トランザクション コミットの最適なモードは TiDB によって決定されます。

### tidb_enable_auto_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-auto-analyze-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB がテーブル統計をバックグラウンド操作として自動的に更新するかどうかを決定します。
-   この設定は以前は`tidb.toml`オプション ( `performance.run-auto-analyze` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。

### tidb_enable_auto_increment_in_generated {#tidb-enable-auto-increment-in-generated}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、生成された列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定するために使用されます。

### tidb_enable_batch_dml {#tidb-enable-batch-dml}

> **警告：**
>
> この変数は非推奨の batch-dml 機能に関連付けられており、データが破損する可能性があります。したがって、batch-dml でこの変数を有効にすることはお勧めしません。代わりに、 [非トランザクション DML](/non-transactional-dml.md)を使用してください。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチ dml 機能を有効にするかどうかを制御します。有効にすると、特定のステートメントが複数のトランザクションに分割される可能性がありますが、これはアトミックではないため、注意して使用する必要があります。 batch-dml を使用する場合は、操作対象のデータに対して同時操作がないことを確認する必要があります。これを機能させるには、 `tidb_batch_dml_size`に正の値を指定し、少なくとも`tidb_batch_insert`と`tidb_batch_delete`のいずれかを有効にする必要があります。

### tidb_enable_cascades_planner {#tidb-enable-cascades-planner}

> **警告：**
>
> 現在、カスケード プランナーは実験的機能です。本番環境で使用することはお勧めしません。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、カスケード プランナーを有効にするかどうかを制御するために使用されます。

### tidb_enable_chunk_rpc <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-chunk-rpc-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサーで`Chunk`データ エンコーディング フォーマットを有効にするかどうかを制御するために使用されます。

### tidb_enable_clustered_index <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-clustered-index-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON` 、 `INT_ONLY`
-   この変数は、デフォルトで主キーを[クラスター化インデックス](/clustered-indexes.md)として作成するかどうかを制御するために使用されます。ここでの「デフォルト」とは、ステートメントがキーワード`CLUSTERED` / `NONCLUSTERED`を明示的に指定していないことを意味します。サポートされている値は`OFF` 、 `ON` 、および`INT_ONLY`です。
    -   `OFF` 、主キーが既定で非クラスター化インデックスとして作成されることを示します。
    -   `ON` 、主キーが既定でクラスター化インデックスとして作成されることを示します。
    -   `INT_ONLY` 、動作が構成アイテム`alter-primary-key`によって制御されることを示します。 `alter-primary-key`が`true`に設定されている場合、すべての主キーはデフォルトで非クラスター化インデックスとして作成されます。 `false`に設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

### tidb_enable_ddl {#tidb-enable-ddl}

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON`
-   この変数は、対応する TiDB インスタンスが DDL 所有者になることができるかどうかを制御します。現在の TiDB クラスターに TiDB インスタンスが 1 つしかない場合、それが DDL 所有者になるのを防ぐことはできません。つまり、それを`OFF`に設定することはできません。

### tidb_enable_collect_execution_info {#tidb-enable-collect-execution-info}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、各オペレーターの実行情報をスロー クエリ ログに記録するかどうかを制御します。

### tidb_enable_column_tracking <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-column-tracking-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、 `PREDICATE COLUMNS`に関する統計の収集は実験的機能です。本番環境で使用することはお勧めしません。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB が`PREDICATE COLUMNS`を収集できるようにするかどうかを制御します。収集を有効にした後、無効にすると、以前に収集された`PREDICATE COLUMNS`の情報はクリアされます。詳細については、 [一部の列で統計を収集する](/statistics.md#collect-statistics-on-some-columns)を参照してください。

### tidb_enable_concurrent_ddl <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-concurrent-ddl-span-class-version-mark-new-in-v6-2-0-span}

> **警告：**
>
> **この変数を変更しないでください**。この変数を無効にするリスクは不明であり、クラスターのメタデータが破損する可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB が同時 DDL ステートメントを使用できるようにするかどうかを制御します。並行 DDL ステートメントを使用すると、DDL 実行フローが変更され、DDL ステートメントが他の DDL ステートメントによって簡単にブロックされなくなります。また、複数のインデックスを同時に追加することもできます。

### tidb_enable_enhanced_security {#tidb-enable-enhanced-security}

-   スコープ: なし
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: `OFF`
-   この変数は、接続している TiDBサーバーでSecurity Enhanced Mode (SEM) が有効になっているかどうかを示します。この値を変更するには、TiDBサーバー構成ファイルで値`enable-sem`を変更し、TiDBサーバーを再起動する必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`
-   この変数は読み取り専用です。 TiDB Cloudでは、 Security Enhanced Mode (SEM) がデフォルトで有効になっています。

</CustomContent>

-   SEM は、次のようなシステムの設計に触発されています[セキュリティが強化された Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) 。これにより、MySQL `SUPER`権限を持つユーザーの能力が低下し、代わりに`RESTRICTED`権限を付与する必要があります。これらのきめの細かい権限には次のものがあります。
    -   `RESTRICTED_TABLES_ADMIN` : `mysql`スキーマのシステム テーブルにデータを書き込み、 `information_schema`のテーブルの機密列を表示する機能。
    -   `RESTRICTED_STATUS_ADMIN` : コマンド`SHOW STATUS`で機密変数を表示する機能。
    -   `RESTRICTED_VARIABLES_ADMIN` : `SHOW [GLOBAL] VARIABLES`および`SET`で機密変数を表示および設定する機能。
    -   `RESTRICTED_USER_ADMIN` : 他のユーザーがユーザー アカウントを変更したり削除したりできないようにする機能。

### tidb_enable_exchange_partition {#tidb-enable-exchange-partition}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、デフォルトで`exchange partitions with tables`が有効になっています。
-   この変数は、v6.3.0 以降では非推奨です。その値はデフォルト値`ON`に固定されます。つまり、デフォルトで`exchange partitions with tables`が有効になっています。

### tidb_enable_extended_stats {#tidb-enable-extended-stats}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザをガイドするために TiDB が拡張統計を収集できるかどうかを示します。詳細については[拡張統計の概要](/extended-statistics.md)参照してください。

### tidb_enable_external_ts_read <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-external-ts-read-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数が`ON`に設定されている場合、TiDB は[`tidb_external_ts`](#tidb_external_ts-new-in-v640)で指定されたタイムスタンプを持つデータを読み取ります。

### tidb_external_ts <span class="version-mark">v6.4.0 の新機能</span> {#tidb-external-ts-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-new-in-v640)が`ON`に設定されている場合、TiDB はこの変数で指定されたタイムスタンプでデータを読み取ります。

### tidb_enable_fast_analyze {#tidb-enable-fast-analyze}

> **警告：**
>
> 現在、 `Fast Analyze`は実験的機能です。本番環境で使用することはお勧めしません。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計`Fast Analyze`機能を有効にするかどうかを設定するために使用されます。
-   統計`Fast Analyze`機能が有効になっている場合、TiDB は統計として約 10,000 行のデータをランダムにサンプリングします。データが偏在している場合やデータサイズが小さい場合、統計精度は低くなります。これにより、不適切なインデックスを選択するなど、最適でない実行計画が発生する可能性があります。通常の`Analyze`ステートメントの実行時間が許容できる場合は、 `Fast Analyze`機能を無効にすることをお勧めします。

### tidb_enable_foreign_key <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-foreign-key-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `FOREIGN KEY`機能を有効にするかどうかを制御します。

### tidb_enable_gc_aware_memory_track {#tidb-enable-gc-aware-memory-track}

> **警告：**
>
> この変数は、TiDB でのデバッグ用の内部変数です。将来のリリースで削除される可能性があります。この変数を設定し**ないでください**。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、GC-Awareメモリトラックを有効にするかどうかを制御します。

### tidb_enable_general_plan_cache <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-general-plan-cache-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、General Plan Cache 機能を有効にするかどうかを制御します。

### tidb_enable_gogc_tuner <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-gogc-tuner-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、GOGC チューナーを有効にするかどうかを制御します。

### tidb_enable_historical_stats {#tidb-enable-historical-stats}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、未リリースの機能に使用されます。**変数値を変更しないでください**。

### tidb_enable_index_merge <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-index-merge-span-class-version-mark-new-in-v4-0-span}

> **ノート：**
>
> -   TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードすると、実行計画の変更によるパフォーマンスの低下を防ぐために、この変数はデフォルトで無効になります。
>
> -   TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードした後、この変数はアップグレード前の設定のままです。
>
> -   v5.4.0 以降、新しくデプロイされた TiDB クラスターの場合、この変数はデフォルトで有効になっています。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックス マージ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_index_merge_join {#tidb-enable-index-merge-join}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `IndexMergeJoin`演算子を有効にするかどうかを指定します。
-   この変数は、TiDB の内部操作にのみ使用されます。調整することは**お勧めしません**。そうしないと、データの正確性が影響を受ける可能性があります。

### tidb_enable_legacy_instance_scope <span class="version-mark">v6.0.0 の新機能</span> {#tidb-enable-legacy-instance-scope-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数では、 `SET SESSION`および`SET GLOBAL`構文を使用して`INSTANCE`スコープ変数を設定できます。
-   このオプションは、以前のバージョンの TiDB との互換性のためにデフォルトで有効になっています。

### tidb_enable_list_partition <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-list-partition-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `LIST (COLUMNS) TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。

### tidb_enable_local_txn {#tidb-enable-local-txn}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、未リリースの機能に使用されます。**変数値を変更しないでください**。

### tidb_enable_metadata_lock <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-metadata-lock-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [メタデータ ロック](/metadata-lock.md)機能を有効にするかどうかを設定するために使用されます。この変数を設定するときは、クラスター内で実行中の DDL ステートメントがないことを確認する必要があることに注意してください。そうしないと、データが正しくないか、矛盾している可能性があります。

### tidb_enable_mutation_checker <span class="version-mark">v6.0.0 の新機能</span> {#tidb-enable-mutation-checker-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、DML ステートメントの実行中にデータとインデックス間の整合性をチェックするために使用されるツールである TiDB ミューテーション チェッカーを有効にするかどうかを制御するために使用されます。チェッカーがステートメントのエラーを返した場合、TiDB はステートメントの実行をロールバックします。この変数を有効にすると、CPU 使用率がわずかに増加します。詳細については、 [データとインデックス間の不一致のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)を参照してください。
-   v6.0.0 以降のバージョンの新しいクラスターの場合、デフォルト値は`ON`です。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_enable_new_cost_interface <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-new-cost-interface-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB v6.2.0 は、以前のコスト モデルの実装をリファクタリングします。この変数は、リファクタリングされたコスト モデルの実装を有効にするかどうかを制御します。
-   この変数はデフォルトで有効になっています。これは、リファクタリングされたコスト モデルが以前と同じコスト式を使用し、計画の決定が変更されないためです。
-   クラスターが v6.1 から v6.2 にアップグレードされた場合、この変数は`OFF`のままであり、手動で有効にすることをお勧めします。クラスターが v6.1 より前のバージョンからアップグレードされた場合、この変数はデフォルトで`ON`に設定されます。

### tidb_enable_new_only_full_group_by_check <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-new-only-full-group-by-check-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB が`ONLY_FULL_GOUP_BY`チェックを実行するときの動作を制御します。 `ONLY_FULL_GROUP_BY`の詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)を参照してください。 v6.1.0 では、TiDB はこのチェックをより厳密かつ正確に処理します。
-   バージョンのアップグレードに起因する潜在的な互換性の問題を回避するために、この変数のデフォルト値は v6.1.0 では`OFF`です。

### tidb_enable_noop_functions <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-noop-functions-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   可能な値: `OFF` 、 `ON` 、 `WARN`
-   デフォルトでは、まだ実装されていない機能の構文を使用しようとすると、TiDB はエラーを返します。変数値が`ON`に設定されている場合、TiDB はそのような利用できない機能のケースを黙って無視します。これは、SQL コードを変更できない場合に役立ちます。
-   `noop`関数を有効にすると、次の動作が制御されます。
    -   `LOCK IN SHARE MODE`構文
    -   `SQL_CALC_FOUND_ROWS`構文
    -   `START TRANSACTION READ ONLY`と`SET TRANSACTION READ ONLY`の構文
    -   `tx_read_only` 、 `transaction_read_only` 、 `offline_mode` 、 `super_read_only` 、 `read_only` 、および`sql_auto_is_null`システム変数
    -   `GROUP BY <expr> ASC|DESC`構文

> **警告：**
>
> デフォルト値の`OFF`だけが安全であると見なすことができます。設定`tidb_enable_noop_functions=1` 、TiDB がエラーを提供せずに特定の構文を無視することを許可するため、アプリケーションで予期しない動作につながる可能性があります。たとえば、構文`START TRANSACTION READ ONLY`は許可されますが、トランザクションは読み書きモードのままです。

### tidb_enable_noop_variables <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-noop-variables-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `ON`
-   変数の値を`OFF`に設定すると、TiDB は次のように動作します。
    -   `SET`を使用して`noop`変数を設定すると、TiDB は`"setting *variable_name* has no effect in TiDB"`警告を返します。
    -   `SHOW [SESSION | GLOBAL] VARIABLES`の結果には`noop`変数は含まれません。
    -   `SELECT`を使用して`noop`変数を読み取ると、TiDB は`"variable *variable_name* has no effect in TiDB"`警告を返します。
-   TiDB インスタンスが`noop`変数を設定して読み取ったかどうかを確認するには、 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;`ステートメントを使用できます。

### tidb_enable_null_aware_anti_join <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-null-aware-anti-join-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   この変数は、ANTI JOIN が特別なセット演算子`NOT IN`および`!= ALL`によって導かれるサブクエリによって生成されるときに、TiDB が Null Aware Hash Join を適用するかどうかを制御します。

### tidb_enable_outer_join_reorder <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-outer-join-reorder-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   v6.1.0 以降、TiDB の[結合したテーブルの再配置](/join-reorder.md)アルゴリズムは Outer Join をサポートしています。この変数は、TiDB が Join Reorder の Outer Join のサポートを有効にするかどうかを制御します。
-   クラスターが以前のバージョンの TiDB からアップグレードされている場合は、次の点に注意してください。

    -   アップグレード前の TiDB のバージョンが v6.1.0 より前の場合、アップグレード後のこの変数のデフォルト値は`ON`です。
    -   アップグレード前のTiDBのバージョンがv6.1.0以降の場合、アップグレード後の変数のデフォルト値はアップグレード前の値に従います。

### <code>tidb_enable_inl_join_inner_multi_pattern</code> <span class="version-mark">v6.5.2 の新機能</span> {#code-tidb-enable-inl-join-inner-multi-pattern-code-span-class-version-mark-new-in-v6-5-2-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、内部テーブルに`Selection`または`Projection`の演算子がある場合に Index Join がサポートされるかどうかを制御します。デフォルト値`OFF` 、このシナリオではインデックス結合がサポートされていないことを意味します。

### tidb_enable_ordered_result_mode {#tidb-enable-ordered-result-mode}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   最終出力結果を自動的にソートするかどうかを指定します。
-   たとえば、この変数を有効にすると、TiDB は`SELECT a, MAX(b) FROM t GROUP BY a`を`SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`として処理します。

### tidb_enable_paging <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-paging-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ページングの方法を使用してコプロセッサー要求を送信するかどうかを制御します。 [v5.4.0、v6.2.0) の TiDB バージョンでは、この変数は`IndexLookup`演算子でのみ有効です。 v6.2.0 以降では、この変数はグローバルに有効になります。 v6.4.0 以降、この変数のデフォルト値は`OFF`から`ON`に変更されました。
-   ユーザー シナリオ:

    -   すべての OLTP シナリオで、ページングの方法を使用することをお勧めします。
    -   `IndexLookup`と`Limit`使用し、 `Limit` `IndexScan`にプッシュできない読み取りクエリの場合、読み取りクエリのレイテンシーが高くなり、TiKV `Unified read pool CPU`の使用率が高くなる可能性があります。このような場合、 `Limit`演算子は小さなデータセットしか必要としないため、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)から`ON`を設定すると、TiDB が処理するデータが少なくなり、クエリのレイテンシーとリソース消費が削減されます。
    -   [Dumpling](/dumpling-overview.md)およびフル テーブル スキャンを使用したデータ エクスポートなどのシナリオでは、ページングを有効にすると、TiDB プロセスのメモリ消費を効果的に削減できます。

> **ノート：**
>
> TiFlashの代わりに TiKV がstorageエンジンとして使用される OLAP シナリオでは、ページングを有効にすると、場合によってはパフォーマンスが低下する可能性があります。回帰が発生した場合は、この変数を使用してページングを無効にするか、 [`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-new-in-v620)および[`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-new-in-v630)変数を使用してページング サイズの行の範囲を調整することを検討してください。

### tidb_enable_parallel_apply <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-parallel-apply-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `Apply`オペレーターの並行性を有効にするかどうかを制御します。同時実行数は`tidb_executor_concurrency`変数によって制御されます。 `Apply`オペレーターは相関サブクエリを処理し、デフォルトでは同時実行性がないため、実行速度が遅くなります。この変数の値を`1`に設定すると、同時実行性が向上し、実行速度が向上します。現在、 `Apply`の同時実行はデフォルトで無効になっています。

### tidb_enable_pipelined_window_function {#tidb-enable-pipelined-window-function}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数にパイプライン実行アルゴリズムを使用するかどうかを指定します。

### tidb_enable_plan_replayer_capture {#tidb-enable-plan-replayer-capture}

> 警告：
>
> この変数は、現在の TiDB バージョンでは完全には機能しない機能を制御します。デフォルト値を変更しないでください。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

### tidb_enable_prepared_plan_cache <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-prepared-plan-cache-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   [プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)を有効にするかどうかを決定します。有効にすると、 `Prepare`と`Execute`の実行プランがキャッシュされるため、以降の実行では実行プランの最適化がスキップされ、パフォーマンスが向上します。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-prepared-plan-cache-memory-monitor-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `ON`
-   この変数は、 プリペアドプランキャッシュにキャッシュされた実行プランによって消費されるメモリをカウントするかどうかを制御します。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)を参照してください。

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">v5.3.0 の新機能</span> {#tidb-enable-pseudo-for-outdated-stats-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計が古い場合にテーブルの統計を使用する際のオプティマイザの動作を制御します。

<CustomContent platform="tidb">

-   オプティマイザは、テーブルの統計が古いかどうかを次のように判断します。統計を取得するために最後にテーブルで`ANALYZE`が実行されてから、テーブル行の 80% が変更された場合 (変更された行数を合計行数で割った値) )、オプティマイザは、このテーブルの統計が古いと判断します。この比率は、 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)構成を使用して変更できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   オプティマイザは、テーブルの統計が古いかどうかを次のように判断します。統計を取得するために最後にテーブルで`ANALYZE`が実行されてから、テーブル行の 80% が変更された場合 (変更された行数を合計行数で割った値) )、オプティマイザは、このテーブルの統計が古いと判断します。

</CustomContent>

-   デフォルトでは (変数値`OFF`を使用)、表の統計が古くなっても、オプティマイザーは引き続き表の統計を使用します。変数の値を`ON`に設定すると、オプティマイザは、合計行数を除いてテーブルの統計が信頼できなくなったと判断します。次に、オプティマイザは疑似統計を使用します。
-   テーブルのデータが頻繁に変更され、このテーブルで`ANALYZE`適時に実行しない場合は、実行計画を安定させるために、変数値を`OFF`に設定することをお勧めします。

### tidb_enable_rate_limit_action {#tidb-enable-rate-limit-action}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、データを読み取るオペレーターの動的メモリ制御機能を有効にするかどうかを制御します。デフォルトでは、この演算子は、データの読み取りを許可する[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)の最大数を有効にします。 1 つの SQL ステートメントのメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超えると、データを読み取るオペレーターは 1 つのスレッドを停止します。

<CustomContent platform="tidb">

-   データを読み取るオペレーターに残っているスレッドが 1 つだけで、単一の SQL ステートメントのメモリ使用量が常に[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超える場合、この SQL ステートメントは[スピル, データをディスクに](/system-variables.md#tidb_enable_tmp_storage_on_oom)などの他のメモリ制御動作をトリガーします。
-   この変数は、SQL ステートメントがデータの読み取りのみを行う場合に、メモリの使用を効果的に制御します。計算操作 (結合操作や集計操作など) が必要な場合、メモリ使用量が`tidb_mem_quota_query`の制御下にない可能性があり、OOM のリスクが高まります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   データを読み取るオペレーターのスレッドが 1 つしか残っておらず、単一の SQL ステートメントのメモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超え続けている場合、この SQL ステートメントは、データをディスクにスピルするなど、他のメモリ制御動作をトリガーします。

</CustomContent>

### tidb_enable_reuse_chunk <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-reuse-chunk-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `ON`
-   値のオプション: `OFF` 、 `ON`
-   この変数は、TiDB がチャンク オブジェクト キャッシュを有効にするかどうかを制御します。値が`ON`の場合、TiDB はキャッシュされたチャンク オブジェクトを優先して使用し、要求されたオブジェクトがキャッシュにない場合はシステムからの要求のみを使用します。値が`OFF`場合、TiDB はシステムからチャンク オブジェクトを直接要求します。

### tidb_enable_slow_log {#tidb-enable-slow-log}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_tmp_storage_on_oom {#tidb-enable-tmp-storage-on-oom}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `ON`
-   値のオプション: `OFF` 、 `ON`
-   1 つの SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部の演算子の一時storageを有効にするかどうかを制御します。
-   v6.3.0 より前では、TiDB 構成項目`oom-use-tmp-storage`を使用して、この機能を有効または無効にすることができます。クラスターを v6.3.0 以降のバージョンにアップグレードした後、TiDB クラスターは値`oom-use-tmp-storage`を使用してこの変数を自動的に初期化します。その後、 `oom-use-tmp-storage`の値を変更しても有効**になりません**。

### tidb_enable_stmt_summary <span class="version-mark">v3.0.4 の新機能</span> {#tidb-enable-stmt-summary-span-class-version-mark-new-in-v3-0-4-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ステートメント要約機能を有効にするかどうかを制御するために使用されます。有効にすると、時間消費などの SQL 実行情報が`information_schema.STATEMENTS_SUMMARY`システム テーブルに記録され、SQL パフォーマンスの問題を特定してトラブルシューティングします。

### tidb_enable_strict_double_type_check <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-strict-double-type-check-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、タイプ`DOUBLE`の無効な定義でテーブルを作成できるかどうかを制御するために使用されます。この設定は、タイプの検証がそれほど厳密ではない以前のバージョンの TiDB からのアップグレード パスを提供することを目的としています。
-   デフォルト値の`ON` MySQL と互換性があります。

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
> MySQL では`FLOAT`型の精度が許可されているため、この設定は型`DOUBLE`にのみ適用されます。この動作は MySQL 8.0.17 以降では推奨されておらず、 `FLOAT`または`DOUBLE`型の精度を指定することはお勧めしません。

### tidb_enable_table_partition {#tidb-enable-table-partition}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON` 、 `AUTO`
-   この変数は、 `TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。
    -   `ON` 1 つの列でレンジ パーティション分割、ハッシュ パーティション分割、およびレンジ列パーティション分割を有効にすることを示します。
    -   `AUTO` `ON`と同じように関数。
    -   `OFF` `TABLE PARTITION`機能を無効にすることを示します。この場合、パーティション テーブルを作成する構文は実行できますが、作成されるテーブルはパーティション化されたものではありません。

### tidb_enable_telemetry <span class="version-mark">v4.0.2 の新機能</span> {#tidb-enable-telemetry-span-class-version-mark-new-in-v4-0-2-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: v6.5.0 の場合は`ON` 。 v6.5.1 以降の v6.5.x バージョンの場合は`OFF`

<CustomContent platform="tidb">

-   この変数は、TiDB の[テレメトリ コレクション](/telemetry.md)を有効にするかどうかを動的に制御するために使用されます。すべての TiDB インスタンスで TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目が`false`に設定されている場合、テレメトリ収集は常に無効になり、このシステム変数は有効になりません。詳細は[テレメトリー](/telemetry.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB でのテレメトリ コレクションを有効にするかどうかを動的に制御するために使用されます。

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-tiflash-read-for-write-stmt-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは実験的ものです。本番環境で使用することはお勧めしません。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `INSERT` 、および`UPDATE`を含む SQL ステートメントの読み取り操作をTiFlashにプッシュできるかどうかを制御`DELETE`ます。例えば：

    -   `INSERT INTO SELECT`ステートメントで`SELECT`クエリ (一般的な使用シナリオ: [TiFlashクエリ結果の実体化](/tiflash/tiflash-results-materialization.md) )
    -   `UPDATE`と`DELETE`ステートメントで`WHERE`条件フィルタリング

### tidb_enable_top_sql <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-top-sql-span-class-version-mark-new-in-v5-4-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> 現在、 Top SQL は実験的機能です。本番環境で使用することはお勧めしません。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、 [Top SQL](/dashboard/top-sql.md)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

### tidb_enable_tso_follower_proxy <span class="version-mark">v5.3.0 の新機能</span> {#tidb-enable-tso-follower-proxy-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TSOFollowerプロキシ機能を有効にするために使用されます。値が`OFF`の場合、TiDB は PD リーダーから TSO のみを取得します。この機能を有効にすると、TiDB はすべての PD ノードにリクエストを均等に送信し、PD フォロワーを介して TSO リクエストを転送することで TSO を取得します。これにより、PD リーダーの CPU 負荷が軽減されます。
-   TSOFollowerプロキシを有効にするシナリオ:
    -   TSO 要求の負荷が高いため、PD リーダーの CPU がボトルネックに達し、TSO RPC 要求のレイテンシーが長くなります。
    -   TiDB クラスターには多くの TiDB インスタンスがあり、値を[`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)に増やしても、TSO RPC 要求の高レイテンシーの問題を軽減することはできません。

> **ノート：**
>
> PD リーダーの CPU 使用率のボトルネック以外の理由 (ネットワークの問題など) で、TSO RPCレイテンシーが増加したとします。この場合、TSOFollowerプロキシを有効にすると、TiDB での実行レイテンシーが増加し、クラスターの QPS パフォーマンスに影響を与える可能性があります。

### tidb_enable_unsafe_substitute <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-unsafe-substitute-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、式を安全でない方法で生成された列に置き換えるかどうかを制御します。デフォルト値は`OFF`です。これは、安全でない置換がデフォルトで無効になっていることを意味します。詳細については、 [生成された列](/generated-columns.md)を参照してください。

### tidb_enable_vectorized_expression <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-vectorized-expression-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ベクトル化された実行を有効にするかどうかを制御するために使用されます。

### tidb_enable_window_function {#tidb-enable-window-function}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数のサポートを有効にするかどうかを制御するために使用されます。ウィンドウ関数は予約済みのキーワードを使用する場合があることに注意してください。これにより、通常は実行できた SQL ステートメントが、TiDB のアップグレード後に解析できなくなる可能性があります。この場合、 `tidb_enable_window_function` ～ `OFF`を設定できます。

### tidb_enforce_mpp <span class="version-mark">v5.1 の新機能</span> {#tidb-enforce-mpp-span-class-version-mark-new-in-v5-1-span}

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   このデフォルト値を変更するには、 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値を変更します。

</CustomContent>

-   オプティマイザーのコスト見積もりを無視し、TiFlash の MPP モードをクエリ実行に強制的に使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF` 。これは、MPP モードが強制的に使用されないことを意味します (デフォルト)。
    -   `1`または`ON` 。これは、コスト見積もりが無視され、MPP モードが強制的に使用されることを意味します。この設定は`tidb_allow_mpp=true`の場合にのみ有効であることに注意してください。

MPP は、 TiFlashエンジンによって提供される分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能で高スループットの SQL アルゴリズムを提供します。 MPP モードの選択については、 [MPP モードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_evolve_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ベースライン進化機能を有効にするかどうかを制御するために使用されます。詳細な導入または使用方法については、 [ベースライン進化](/sql-plan-management.md#baseline-evolution)を参照してください。
-   クラスターに対するベースラインの進化の影響を軽減するには、次の構成を使用します。
    -   各実行計画の最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`を設定します。デフォルト値は 600 秒です。
    -   時間枠を制限するには、 `tidb_evolve_plan_task_start_time`と`tidb_evolve_plan_task_end_time`を設定します。デフォルト値はそれぞれ`00:00 +0000`と`23:59 +0000`です。

### tidb_evolve_plan_task_end_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-end-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、1 日のベースライン進化の終了時間を設定するために使用されます。

### tidb_evolve_plan_task_max_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-max-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `600`
-   範囲: `[-1, 9223372036854775807]`
-   単位: 秒
-   この変数は、ベースライン進化機能の各実行プランの最大実行時間を制限するために使用されます。

### tidb_evolve_plan_task_start_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-start-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、1 日のベースライン進化の開始時刻を設定するために使用されます。

### tidb_executor_concurrency <span class="version-mark">v5.0 の新機能</span> {#tidb-executor-concurrency-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `5`
-   範囲: `[1, 256]`
-   単位: スレッド

この変数は、次の SQL 演算子の同時実行を (1 つの値に) 設定するために使用されます。

-   `index lookup`
-   `index lookup join`
-   `hash join`
-   `hash aggregation` ( `partial`および`final`フェーズ)
-   `window`
-   `projection`

`tidb_executor_concurrency`は、管理を容易にするために、次の既存のシステム変数が全体として組み込まれています。

-   `tidb_index_lookup_concurrency`
-   `tidb_index_lookup_join_concurrency`
-   `tidb_hash_join_concurrency`
-   `tidb_hashagg_partial_concurrency`
-   `tidb_hashagg_final_concurrency`
-   `tidb_projection_concurrency`
-   `tidb_window_concurrency`

v5.0 以降、上記のシステム変数を個別に変更することができ (非推奨の警告が返されます)、変更は対応する単一の演算子にのみ影響します。その後、 `tidb_executor_concurrency`を使用してオペレーターの同時実行数を変更しても、個別に変更されたオペレーターは影響を受けません。 `tidb_executor_concurrency`を使用してすべてのオペレーターの同時実行数を変更する場合は、上記のすべての変数の値を`-1`に設定できます。

以前のバージョンから v5.0 にアップグレードされたシステムの場合、上記の変数の値を変更していない場合 (つまり、 `tidb_hash_join_concurrency`値が`5`で、残りの値が`4`であることを意味します)、以前に管理されていたオペレーターの同時実行は、これらの変数は`tidb_executor_concurrency`によって自動的に管理されます。これらの変数のいずれかを変更した場合、対応する演算子の同時実行性は、変更された変数によって引き続き制御されます。

### tidb_expensive_query_time_threshold {#tidb-expensive-query-time-threshold}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 2147483647]`
-   単位: 秒
-   この変数は、負荷の高いクエリ ログを出力するかどうかを決定するしきい値を設定するために使用されます。高価なクエリ ログと遅いクエリ ログの違いは次のとおりです。
    -   ステートメントの実行後にスローログが出力されます。
    -   高価なクエリ ログには、実行時間がしきい値を超えて実行されているステートメントと、その関連情報が出力されます。

### tidb_force_priority {#tidb-force-priority}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 列挙
-   デフォルト値: `NO_PRIORITY`
-   可能な値: `NO_PRIORITY` 、 `LOW_PRIORITY` 、 `HIGH_PRIORITY` 、 `DELAYED`
-   この変数は、TiDBサーバーで実行されるステートメントのデフォルトの優先度を変更するために使用されます。使用例は、OLAP クエリを実行している特定のユーザーが OLTP クエリを実行しているユーザーよりも低い優先度を受け取るようにすることです。
-   デフォルト値`NO_PRIORITY`は、ステートメントの優先度が強制的に変更されないことを意味します。

### tidb_gc_concurrency <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-concurrency-span-class-version-mark-new-in-v5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   GC の[ロックを解決する](/garbage-collection-overview.md#resolve-locks)ステップのスレッド数を指定します。値`-1`は、TiDB が使用するガベージコレクションスレッドの数を自動的に決定することを意味します。

### tidb_gc_enable <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-enable-span-class-version-mark-new-in-v5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiKV のガベージコレクションを有効にします。ガベージコレクションを無効にすると、古いバージョンの行が削除されなくなるため、システム パフォーマンスが低下します。

### tidb_gc_life_time <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-life-time-span-class-version-mark-new-in-v5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   Go Duration の形式で、GC ごとにデータが保持される制限時間。 GC が発生すると、現在の時刻からこの値を差し引いた値が安全なポイントになります。

> **ノート：**
>
> -   更新が頻繁に行われるシナリオでは、 `tidb_gc_life_time`の値が大きい (数日または数か月) と、次のような潜在的な問題が発生する可能性があります。
>     -   より大きなstorageの使用
>     -   大量の履歴データは、特に`select count(*) from t`などの範囲クエリの場合、パフォーマンスにある程度影響を与える可能性があります。
> -   `tidb_gc_life_time`よりも長く実行されているトランザクションがある場合、GC 中に、このトランザクションが実行を継続するために`start_ts`以降のデータが保持されます。たとえば、 `tidb_gc_life_time`が 10 分に設定されている場合、実行中のすべてのトランザクションの中で、最も早く開始されたトランザクションが 15 分間実行されており、GC は最近の 15 分間のデータを保持します。

### tidb_gc_max_wait_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-gc-max-wait-time-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `86400`
-   範囲: `[600, 31536000]`
-   単位: 秒
-   この変数は、アクティブなトランザクションが GC セーフ ポイントをブロックする最大時間を設定するために使用されます。デフォルトでは、GC の各時間中、セーフ ポイントは進行中のトランザクションの開始時間を超えません。アクティブなトランザクションの実行時間がこの変数値を超えない場合、実行時間がこの値を超えるまで GC セーフ ポイントはブロックされます。

### tidb_gc_run_interval <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-run-interval-span-class-version-mark-new-in-v5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   Go Duration の形式で GC 間隔を指定します (例: `"1h30m"`および`"15m"` 。

### tidb_gc_scan_lock_mode <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-scan-lock-mode-span-class-version-mark-new-in-v5-0-span}

> **警告：**
>
> 現在、Green GC は実験的機能です。本番環境で使用することはお勧めしません。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `LEGACY`
-   可能な値: `PHYSICAL` 、 `LEGACY`
    -   `LEGACY` : 従来のスキャン方法を使用します。つまり、Green GC を無効にします。
    -   `PHYSICAL` : 物理スキャン方式を使用します。つまり、Green GC を有効にします。

<CustomContent platform="tidb">

-   この変数は、GC のロックの解決ステップでロックをスキャンする方法を指定します。変数値が`LEGACY`に設定されている場合、TiDB はリージョンごとにロックをスキャンします。値`PHYSICAL`を使用すると、各 TiKV ノードがRaftレイヤーをバイパスし、データを直接スキャンできるようになります。これにより、 [休止リージョン](/tikv-configuration-file.md#hibernate-regions)機能が有効な場合にすべてのリージョンをウェイクアップする GC の影響を効果的に軽減できるため、Resolve Locks の実行速度が向上します。ステップ。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、GC のロックの解決ステップでロックをスキャンする方法を指定します。変数値が`LEGACY`に設定されている場合、TiDB はリージョンごとにロックをスキャンします。値`PHYSICAL`を使用すると、各 TiKV ノードがRaftレイヤーをバイパスし、データを直接スキャンできるようになります。これにより、すべてのリージョンをウェイクアップする GC の影響を効果的に軽減できるため、Resolve Locks ステップでの実行速度が向上します。

</CustomContent>

### tidb_general_log {#tidb-general-log}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb-cloud">

-   この変数は、すべての SQL ステートメントをログに記録するかどうかを設定するために使用されます。この機能はデフォルトで無効になっています。問題を特定するときにすべての SQL ステートメントをトレースする必要がある場合は、この機能を有効にします。

</CustomContent>

<CustomContent platform="tidb">

-   この変数は、すべての SQL ステートメントを[ログ](/tidb-configuration-file.md#logfile)に記録するかどうかを設定するために使用されます。この機能はデフォルトで無効になっています。メンテナンス担当者が問題を特定するときにすべての SQL ステートメントをトレースする必要がある場合、この機能を有効にすることができます。

-   ログ内のこの機能のすべてのレコードを表示するには、TiDB 構成項目[`log.level`](/tidb-configuration-file.md#level)を`"info"`または`"debug"`に設定してから、 `"GENERAL_LOG"`文字列を照会する必要があります。次の情報が記録されます。
    -   `conn` : 現在のセッションの ID。
    -   `user` : 現在のセッション ユーザー。
    -   `schemaVersion` : 現在のスキーマ バージョン。
    -   `txnStartTS` : 現在のトランザクションが開始されるタイムスタンプ。
    -   `forUpdateTS` :悲観的トランザクション モードでは、 `forUpdateTS`は SQL ステートメントの現在のタイムスタンプです。悲観的トランザクションで書き込み競合が発生すると、TiDB は現在実行中の SQL ステートメントを再試行し、このタイムスタンプを更新します。 [`max-retry-count`](/tidb-configuration-file.md#max-retry-count)で再試行回数を設定できます。楽観的トランザクション モデルでは、 `forUpdateTS`は`txnStartTS`に相当します。
    -   `isReadConsistency` : 現在のトランザクション分離レベルが Read Committed (RC) かどうかを示します。
    -   `current_db` : 現在のデータベースの名前。
    -   `txn_mode` : トランザクション モード。値のオプションは`OPTIMISTIC`と`PESSIMISTIC`です。
    -   `sql` : 現在のクエリに対応する SQL ステートメント。

</CustomContent>

### tidb_general_plan_cache_size <span class="version-mark">v6.3.0 の新機能</span> {#tidb-general-plan-cache-size-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は、General Plan Cache によってキャッシュできる実行プランの最大数を制御します。

### tidb_generate_binary_plan <span class="version-mark">v6.2.0 の新機能</span> {#tidb-generate-binary-plan-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログとステートメント サマリーでバイナリ エンコードされた実行プランを生成するかどうかを制御します。
-   この変数が`ON`に設定されている場合、TiDB ダッシュボードで視覚的な実行計画を表示できます。 TiDB ダッシュボードは、この変数が有効になった後に生成された実行計画の視覚的な表示のみを提供することに注意してください。
-   `SELECT tidb_decode_binary_plan('xxx...')`ステートメントを実行して、バイナリ プランから特定のプランを解析できます。

### tidb_gogc_tuner_threshold <span class="version-mark">v6.4.0 の新機能</span> {#tidb-gogc-tuner-threshold-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: `0.6`
-   範囲: `[0, 0.9)`
-   この変数は、GOGC を調整するための最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC チューナーは動作を停止します。

### tidb_guarantee_linearizability <span class="version-mark">v5.0 の新機能</span> {#tidb-guarantee-linearizability-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、非同期コミットのコミット TS の計算方法を制御します。デフォルト (値`ON` ) では、2 フェーズ コミットは PDサーバーから新しい TS を要求し、TS を使用して最終的なコミット TS を計算します。この状況では、すべての同時トランザクションに対して線形化可能性が保証されます。
-   この変数を`OFF`に設定すると、PDサーバーから TS をフェッチするプロセスがスキップされます。その代償として、因果的一貫性のみが保証されますが、線形化可能性は保証されません。詳細については、ブログ投稿[Async Commit、TiDB 5.0 のトランザクションコミットのアクセラレータ](https://en.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/)参照してください。
-   因果関係のみが必要なシナリオでは、この変数を`OFF`に設定してパフォーマンスを向上させることができます。

### tidb_hash_exchange_with_new_collation {#tidb-hash-exchange-with-new-collation}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、MPP ハッシュ パーティション交換演算子が、新しい照合順序が有効になっているクラスターで生成されるかどうかを制御します。 `true`演算子を生成することを意味し、 `false`生成しないことを意味します。
-   この変数は、TiDB の内部操作に使用されます。この変数を設定すること**はお勧めし**ません。

### tidb_hash_join_concurrency {#tidb-hash-join-concurrency}

> **警告：**
>
> v5.0 以降、この変数は廃止されました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用します。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `hash join`アルゴリズムの並行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hashagg_final_concurrency {#tidb-hashagg-final-concurrency}

> **警告：**
>
> v5.0 以降、この変数は廃止されました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用します。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、第`final`フェーズで並行`hash aggregation`アルゴリズムを実行する並行性を設定するために使用されます。
-   集約関数のパラメーターが明確でない場合、 `HashAgg`同時に実行され、それぞれ 2 つのフェーズ ( `partial`フェーズと`final`フェーズ) で実行されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hashagg_partial_concurrency {#tidb-hashagg-partial-concurrency}

> **警告：**
>
> v5.0 以降、この変数は廃止されました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用します。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、第`partial`フェーズで並行`hash aggregation`アルゴリズムを実行する並行性を設定するために使用されます。
-   集約関数のパラメーターが明確でない場合、 `HashAgg`同時に実行され、それぞれ 2 つのフェーズ ( `partial`フェーズと`final`フェーズ) で実行されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">v6.0.0 の新機能</span> {#tidb-ignore-prepared-cache-close-stmt-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、プリペアドステートメントキャッシュを閉じるためのコマンドを無視するかどうかを設定するために使用されます。
-   この変数が`ON`に設定されている場合、バイナリ プロトコルの`COM_STMT_CLOSE`コマンドとテキスト プロトコルの[`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md)ステートメントは無視されます。詳細については、 [`COM_STMT_CLOSE`コマンドと<code>DEALLOCATE PREPARE</code>ステートメントを無視する](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)を参照してください。

### tidb_index_join_batch_size {#tidb-index-join-batch-size}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `25000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup join`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオでは大きな値を使用し、OLTP シナリオでは小さな値を使用します。

### tidb_index_lookup_concurrency {#tidb-index-lookup-concurrency}

> **警告：**
>
> v5.0 以降、この変数は廃止されました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用します。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup`操作の並行性を設定するために使用されます。
-   OLAP シナリオでは大きな値を使用し、OLTP シナリオでは小さな値を使用します。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_join_concurrency {#tidb-index-lookup-join-concurrency}

> **警告：**
>
> v5.0 以降、この変数は廃止されました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用します。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup join`アルゴリズムの並行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_merge_intersection_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-index-merge-intersection-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   この変数は、インデックス マージが実行する交差操作の最大同時実行数を設定します。これは、TiDB が動的プルーニング モードで分割されたテーブルにアクセスする場合にのみ有効です。実際の同時実行数は、 `tidb_index_merge_intersection_concurrency`とパーティションテーブルの分割数の小さい方の値です。
-   デフォルト値`-1`値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_size {#tidb-index-lookup-size}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `20000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオでは大きな値を使用し、OLTP シナリオでは小さな値を使用します。

### tidb_index_serial_scan_concurrency {#tidb-index-serial-scan-concurrency}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `serial scan`操作の並行性を設定するために使用されます。
-   OLAP シナリオでは大きな値を使用し、OLTP シナリオでは小さな値を使用します。

### tidb_init_chunk_size {#tidb-init-chunk-size}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `32`
-   範囲: `[1, 32]`
-   単位: 行
-   この変数は、実行プロセス中に初期チャンクの行数を設定するために使用されます。

### tidb_isolation_read_engines <span class="version-mark">v4.0 の新機能</span> {#tidb-isolation-read-engines-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   デフォルト値: `tikv,tiflash,tidb`
-   この変数は、データの読み取り時に TiDB が使用できるstorageエンジン リストを設定するために使用されます。

### tidb_last_ddl_info <span class="version-mark">v6.0.0 の新機能</span> {#tidb-last-ddl-info-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション
-   デフォルト値: &quot;&quot;
-   タイプ: 文字列
-   これは読み取り専用の変数です。現在のセッション内の最後の DDL 操作の情報を取得するために、TiDB で内部的に使用されます。
    -   &quot;query&quot;: 最後の DDL クエリ文字列。
    -   &quot;seq_num&quot;: 各 DDL 操作のシーケンス番号。 DDL操作の順序を識別するために使用されます。

### tidb_last_query_info <span class="version-mark">v4.0.14 の新機能</span> {#tidb-last-query-info-span-class-version-mark-new-in-v4-0-14-span}

-   スコープ: セッション
-   デフォルト値: &quot;&quot;
-   これは読み取り専用の変数です。最後の DML ステートメントのトランザクション情報を照会するために、TiDB で内部的に使用されます。情報には次が含まれます。
    -   `txn_scope` : `global`または`local`のトランザクションのスコープ。
    -   `start_ts` : トランザクションの開始タイムスタンプ。
    -   `for_update_ts` : 以前に実行された DML ステートメントの`for_update_ts` 。これは、テスト用に使用される TiDB の内部用語です。通常、この情報は無視できます。
    -   `error` : エラー メッセージ (存在する場合)。

### tidb_last_txn_info <span class="version-mark">v4.0.9 の新機能</span> {#tidb-last-txn-info-span-class-version-mark-new-in-v4-0-9-span}

-   スコープ: セッション
-   タイプ: 文字列
-   この変数は、現在のセッション内の最後のトランザクション情報を取得するために使用されます。これは読み取り専用の変数です。取引情報には以下が含まれます。
    -   トランザクション スコープ。
    -   TS の開始とコミット。
    -   トランザクション コミット モード。2 フェーズ、1 フェーズ、または非同期コミットの可能性があります。
    -   非同期コミットまたは 1 フェーズ コミットから 2 フェーズ コミットへのトランザクション フォールバックの情報。
    -   発生したエラー。

### tidb_last_plan_replayer_token <span class="version-mark">v6.3.0 の新機能</span> {#tidb-last-plan-replayer-token-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション
-   タイプ: 文字列
-   この変数は読み取り専用で、現在のセッションの最後の`PLAN REPLAYER DUMP`の実行の結果を取得するために使用されます。

### tidb_log_file_max_days <span class="version-mark">v5.3.0 の新機能</span> {#tidb-log-file-max-days-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`

<CustomContent platform="tidb">

-   この変数は、ログが現在の TiDB インスタンスに保持される最大日数を設定するために使用されます。その値のデフォルトは、構成ファイルの[`max-days`](/tidb-configuration-file.md#max-days)構成の値です。変数値の変更は、現在の TiDB インスタンスにのみ影響します。 TiDB の再始動後、変数値はリセットされ、構成値は影響を受けません。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、ログが現在の TiDB インスタンスに保持される最大日数を設定するために使用されます。

</CustomContent>

### tidb_low_resolution_tso {#tidb-low-resolution-tso}

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、低精度 TSO 機能を有効にするかどうかを設定するために使用されます。この機能を有効にすると、新しいトランザクションは 2 秒ごとに更新されるタイムスタンプを使用してデータを読み取ります。
-   適用可能な主なシナリオは、古いデータの読み取りが許容される場合に、小さな読み取り専用トランザクションの TSO を取得するオーバーヘッドを削減することです。

### tidb_max_auto_analyze_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-auto-analyze-time-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `43200`
-   範囲: `[0, 2147483647]`
-   単位: 秒
-   この変数は、自動`ANALYZE`タスクの最大実行時間を指定するために使用されます。自動`ANALYZE`タスクの実行時間が指定時間を超えると、タスクは終了します。この変数の値が`0`の場合、自動`ANALYZE`タスクの最大実行時間に制限はありません。

### tidb_max_chunk_size {#tidb-max-chunk-size}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[32, 2147483647]`
-   単位: 行
-   この変数は、実行プロセス中にチャンク内の最大行数を設定するために使用されます。大きすぎる値を設定すると、キャッシュの局所性の問題が発生する可能性があります。

### tidb_max_delta_schema_count <span class="version-mark">v2.1.18 および v3.0.5 の新機能</span> {#tidb-max-delta-schema-count-span-class-version-mark-new-in-v2-1-18-and-v3-0-5-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[100, 16384]`
-   この変数は、キャッシュできるスキーマ バージョン (対応するバージョン用に変更されたテーブル ID) の最大数を設定するために使用されます。値の範囲は 100 ～ 16384 です。

### tidb_max_paging_size <span class="version-mark">v6.3.0 の新機能</span> {#tidb-max-paging-size-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `50000`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサーのページング要求プロセス中に行の最大数を設定するために使用されます。設定値が小さすぎると、TiDB と TiKV 間の RPC カウントが増加しますが、設定値が大きすぎると、データのロードやテーブル全体のスキャンなど、場合によってはメモリの使用量が過剰になります。この変数のデフォルト値は、OLAP シナリオよりも OLTP シナリオで優れたパフォーマンスをもたらします。アプリケーションがstorageエンジンとして TiKV のみを使用する場合は、OLAP ワークロード クエリを実行するときにこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

### tidb_max_tiflash_threads <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-tiflash-threads-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、 TiFlash がリクエストを実行する最大同時実行数を設定するために使用されます。デフォルト値は`-1`で、このシステム変数が無効であることを示します。値が`0`場合、スレッドの最大数はTiFlashによって自動的に構成されます。

### tidb_mem_oom_action <span class="version-mark">v6.1.0 の新機能</span> {#tidb-mem-oom-action-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `CANCEL`
-   可能な値: `CANCEL` 、 `LOG`

<CustomContent platform="tidb">

-   単一の SQL ステートメントが`tidb_mem_quota_query`で指定されたメモリクォータを超え、ディスクにスピルオーバーできない場合に、TiDB が実行する操作を指定します。詳細は[TiDB メモリ制御](/configure-memory-usage.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   単一の SQL ステートメントが[`tidb_mem_quota_query`](#tidb_mem_quota_query)で指定されたメモリクォータを超え、ディスクにスピルオーバーできない場合に、TiDB が実行する操作を指定します。

</CustomContent>

-   デフォルト値は`CANCEL`ですが、TiDB v4.0.2 以前のバージョンでは、デフォルト値は`LOG`です。
-   この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。

### tidb_mem_quota_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-mem-quota-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト
-   この変数は、TiDB 更新統計の最大メモリ使用量を制御します。このようなメモリ使用量は、手動で[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行するときと、TiDB がバックグラウンドでタスクを自動的に分析するときに発生します。合計メモリ使用量がこのしきい値を超えると、ユーザーが実行した`ANALYZE`が終了し、サンプリング レートを下げるか後で再試行するように促すエラー メッセージが報告されます。メモリのしきい値を超えたために TiDB バックグラウンドの自動タスクが終了し、使用されているサンプリング レートがデフォルト値よりも高い場合、TiDB はデフォルトのサンプリング レートを使用して更新を再試行します。この変数の値が負またはゼロの場合、TiDB は手動更新タスクと自動更新タスクの両方のメモリ使用量を制限しません。

> **ノート：**
>
> `auto_analyze` TiDB スタートアップ構成ファイルで`run-auto-analyze`有効になっている場合にのみ、TiDB クラスターでトリガーされます。

### tidb_mem_quota_apply_cache <span class="version-mark">v5.0 の新機能</span> {#tidb-mem-quota-apply-cache-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `33554432` (32 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、 `Apply`演算子でローカル キャッシュのメモリ使用量のしきい値を設定するために使用されます。
-   `Apply`演算子のローカル キャッシュは、 `Apply`演算子の計算を高速化するために使用されます。変数を`0`に設定して、 `Apply`キャッシュ機能を無効にすることができます。

### tidb_mem_quota_binding_cache <span class="version-mark">v6.0.0 の新機能</span> {#tidb-mem-quota-binding-cache-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[0, 2147483647]`
-   単位: バイト
-   この変数は、バインディングのキャッシュに使用されるメモリのしきい値を設定するために使用されます。
-   システムが過剰なバインドを作成またはキャプチャして、メモリ領域が過剰に使用された場合、TiDB はログに警告を返します。この場合、キャッシュは使用可能なすべてのバインディングを保持したり、保存するバインディングを決定したりできません。このため、クエリによってはバインディングが失われる場合があります。この問題に対処するには、この変数の値を大きくします。これにより、バインディングのキャッシュに使用されるメモリが増加します。このパラメーターを変更した後、 `admin reload bindings`実行してバインディングをリロードし、変更を検証する必要があります。

### tidb_mem_quota_query {#tidb-mem-quota-query}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1073741824` (1 GiB)
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト

<CustomContent platform="tidb">

-   TiDB v6.1.0 より前のバージョンでは、これはセッション スコープ変数であり、初期値として`tidb.toml`から`mem-quota-query`の値を使用します。 v6.1.0 から、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0 より前のバージョンでは、この変数を使用して、**クエリ**のメモリクォータのしきい値を設定します。実行中のクエリのメモリクォータがしきい値を超えた場合、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0 以降のバージョンでは、この変数を使用して、**セッション**のメモリクォータのしきい値を設定します。実行中のセッションのメモリクォータがしきい値を超えた場合、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。 TiDB v6.5.0 以降、セッションのメモリ使用量には、セッション内のトランザクションによって消費されるメモリが含まれることに注意してください。 TiDB v6.5.0 以降のバージョンでのトランザクションメモリ使用量の制御動作については、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)を参照してください。
-   変数の値を`0`または`-1`に設定すると、メモリのしきい値は正の無限大になります。 128 より小さい値を設定すると、値はデフォルトで`128`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB v6.1.0 より前のバージョンでは、これはセッション スコープ変数です。 v6.1.0 から、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0 より前のバージョンでは、この変数を使用して、**クエリ**のメモリクォータのしきい値を設定します。実行中のクエリのメモリクォータがしきい値を超えた場合、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0 以降のバージョンでは、この変数を使用して、**セッション**のメモリクォータのしきい値を設定します。実行中のセッションのメモリクォータがしきい値を超えた場合、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。 TiDB v6.5.0 以降、セッションのメモリ使用量には、セッション内のトランザクションによって消費されるメモリが含まれることに注意してください。
-   変数の値を`0`または`-1`に設定すると、メモリのしきい値は正の無限大になります。 128 より小さい値を設定すると、値はデフォルトで`128`になります。

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio {#tidb-memory-debug-mode-alarm-ratio}

-   スコープ: セッション
-   タイプ: フロート
-   デフォルト値: `0`
-   この変数は、TiDBメモリデバッグ モードで許容されるメモリ統計エラー値を表します。
-   この変数は、TiDB の内部テストに使用されます。この変数を設定すること**はお勧めし**ません。

### tidb_memory_debug_mode_min_heap_inuse {#tidb-memory-debug-mode-min-heap-inuse}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   この変数は、TiDB の内部テストに使用されます。この変数を設定すること**はお勧めし**ません。この変数を有効にすると、TiDB のパフォーマンスに影響します。
-   このパラメータを設定した後、TiDB はメモリデバッグ モードに入り、メモリトラッキングの精度を分析します。 TiDB は、後続の SQL ステートメントの実行中に頻繁に GC をトリガーし、実際のメモリ使用量とメモリ統計を比較します。現在のメモリ使用量が`tidb_memory_debug_mode_min_heap_inuse`より大きく、メモリ統計エラーが`tidb_memory_debug_mode_alarm_ratio`超える場合、TiDB は関連するメモリ情報をログとファイルに出力します。

### tidb_memory_usage_alarm_ratio {#tidb-memory-usage-alarm-ratio}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0.0, 1.0]`

<CustomContent platform="tidb">

-   この変数は、tidb-serverメモリアラームをトリガーするメモリ使用率を設定します。デフォルトでは、TiDB のメモリ使用量がその総メモリの 70% を超え、 [アラーム条件](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage)つのいずれかが満たされると、TiDB はアラーム ログを出力。
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能が無効になっていることを意味します。
-   この変数が`0`より大きく`1`より小さい値に設定されている場合、メモリしきい値アラーム機能が有効になっていることを意味します。

    -   システム変数[`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640)の値が`0`の場合、メモリアラームのしきい値は`tidb_memory-usage-alarm-ratio * system memory size`です。
    -   システム変数`tidb_server_memory_limit`の値が 0 より大きい値に設定されている場合、メモリアラームのしきい値は`tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`です。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [tidb-serverメモリアラーム](https://docs.pingcap.com/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage)をトリガーするメモリ使用率を設定します。
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能が無効になっていることを意味します。
-   この変数が`0`より大きく`1`より小さい値に設定されている場合、メモリしきい値アラーム機能が有効になっていることを意味します。

</CustomContent>

### tidb_memory_usage_alarm_keep_record_num <span class="version-mark">v6.4.0 の新機能</span> {#tidb-memory-usage-alarm-keep-record-num-span-class-version-mark-new-in-v6-4-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `5`
-   範囲: `[1, 10000]`
-   tidb サーバーのメモリ使用量がメモリアラームのしきい値を超えてアラームがトリガーされると、TiDB はデフォルトで最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この数値は、この変数で調整できます。

### tidb_merge_join_concurrency {#tidb-merge-join-concurrency}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   範囲: `[1, 256]`
-   デフォルト値: `1`
-   この変数は、クエリが実行されるときの`MergeJoin`演算子の同時実行数を設定します。
-   この変数を設定すること**はお勧めし**ません。この変数の値を変更すると、データの正確性の問題が発生する可能性があります。

### tidb_merge_partition_stats_concurrency {#tidb-merge-partition-stats-concurrency}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `1`
-   この変数は、TiDB がパーティションテーブルを分析するときに、パーティションテーブルの統計をマージする同時実行性を指定します。

### tidb_metric_query_range_duration <span class="version-mark">v4.0 の新機能</span> {#tidb-metric-query-range-duration-span-class-version-mark-new-in-v4-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位: 秒
-   この変数は、照会時に生成される Prometheus ステートメントの範囲期間を設定するために使用されます`METRICS_SCHEMA` 。

### tidb_metric_query_step <span class="version-mark">v4.0 の新機能</span> {#tidb-metric-query-step-span-class-version-mark-new-in-v4-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位: 秒
-   この変数は、クエリ時に生成される Prometheus ステートメントのステップを設定するために使用されます`METRICS_SCHEMA` 。

### tidb_min_paging_size <span class="version-mark">v6.2.0 の新機能</span> {#tidb-min-paging-size-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `128`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサーのページング要求プロセス中に行の最小数を設定するために使用されます。設定値が小さすぎると、TiDB と TiKV 間の RPC リクエスト数が増加します。設定値が大きすぎると、IndexLookup を制限付きで使用してクエリを実行するときに、パフォーマンスが低下する可能性があります。この変数のデフォルト値は、OLAP シナリオよりも OLTP シナリオで優れたパフォーマンスをもたらします。アプリケーションがstorageエンジンとして TiKV のみを使用する場合は、OLAP ワークロード クエリを実行するときにこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

![Paging size impact on TPCH](/media/paging-size-impact-on-tpch.png)

この図に示すように、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)が有効な場合、TPCH のパフォーマンスは`tidb_min_paging_size`と[`tidb_max_paging_size`](#tidb_max_paging_size-new-in-v630)の設定の影響を受けます。縦軸は実行時間で、小さいほど良い。

### tidb_mpp_store_fail_ttl {#tidb-mpp-store-fail-ttl}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 期間
-   デフォルト値: `60s`
-   新しく開始されたTiFlashノードはサービスを提供しません。クエリが失敗しないようにするために、TiDB はクエリを送信する tidb-server を新しく開始されたTiFlashノードに制限します。この変数は、新しく開始されたTiFlashノードにリクエストが送信されない時間範囲を示します。

### tidb_multi_statement_mode <span class="version-mark">v4.0.11 の新機能</span> {#tidb-multi-statement-mode-span-class-version-mark-new-in-v4-0-11-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   可能な値: `OFF` 、 `ON` 、 `WARN`
-   この変数は、同じ`COM_QUERY`呼び出しで複数のクエリを実行できるようにするかどうかを制御します。
-   SQL インジェクション攻撃の影響を軽減するために、TiDB はデフォルトで複数のクエリが同じ`COM_QUERY`の呼び出しで実行されるのを防ぐようになりました。この変数は、以前のバージョンの TiDB からのアップグレード パスの一部として使用することを目的としています。次の動作が適用されます。

| クライアント設定        | `tidb_multi_statement_mode`値 | 複数のステートメントは許可されますか? |
| --------------- | ---------------------------- | ------------------- |
| 複数のステートメント = オン | オフ                           | はい                  |
| 複数のステートメント = オン | の上                           | はい                  |
| 複数のステートメント = オン | 警告する                         | はい                  |
| 複数のステートメント = オフ | オフ                           | いいえ                 |
| 複数のステートメント = オフ | の上                           | はい                  |
| 複数のステートメント = オフ | 警告する                         | はい (+警告が返されます)      |

> **ノート：**
>
> デフォルト値の`OFF`だけが安全であると見なすことができます。アプリケーションが以前のバージョンの TiDB 用に特別に設計されている場合は、設定`tidb_multi_statement_mode=ON`必要になることがあります。アプリケーションで複数ステートメントのサポートが必要な場合は、 `tidb_multi_statement_mode`オプションではなく、クライアント ライブラリによって提供される設定を使用することをお勧めします。例えば：
>
> -   [go-sql-ドライバー](https://github.com/go-sql-driver/mysql#multistatements) ( `multiStatements` )
> -   [コネクタ/J](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-configuration-properties.html) ( `allowMultiQueries` )
> -   PHP [みずい](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) ( `mysqli_multi_query` )

### tidb_nontransactional_ignore_error <span class="version-mark">v6.1.0 の新機能</span> {#tidb-nontransactional-ignore-error-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非トランザクション DML ステートメントでエラーが発生したときに、すぐにエラーを返すかどうかを指定します。
-   値が`OFF`に設定されている場合、非トランザクション DML ステートメントは最初のエラーですぐに停止し、エラーを返します。以下のバッチはすべてキャンセルされます。
-   値が`ON`に設定されている場合、バッチでエラーが発生すると、すべてのバッチが実行されるまで、次のバッチが実行され続けます。実行プロセス中に発生したすべてのエラーは、結果に一緒に返されます。

### tidb_opt_agg_push_down {#tidb-opt-agg-push-down}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザーが集約関数を Join、Projection、および UnionAll の前の位置に押し下げる最適化操作を実行するかどうかを設定するために使用されます。
-   クエリで集計操作が遅い場合は、変数の値を ON に設定できます。

### tidb_opt_broadcast_cartesian_join {#tidb-opt-broadcast-cartesian-join}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   ブロードキャストデカルト結合を許可するかどうかを示します。
-   `0` 、ブロードキャストデカルト結合が許可されていないことを意味します。 `1` [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50)に基づいて許可されることを意味します。 `2`テーブル サイズがしきい値を超えても常に許可されることを意味します。
-   この変数は TiDB で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_concurrency_factor {#tidb-opt-concurrency-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiDB でGolangゴルーチンを開始するための CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_copcpu_factor {#tidb-opt-copcpu-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKVコプロセッサーが1 行を処理するための CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_correlation_exp_factor {#tidb-opt-correlation-exp-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2147483647]`
-   列の順序相関に基づいて行数を見積もる方法がない場合は、ヒューリスティックな見積もり方法が使用されます。この変数は、ヒューリスティック メソッドの動作を制御するために使用されます。
    -   値が 0 の場合、ヒューリスティック手法は使用されません。
    -   値が 0 より大きい場合:
        -   値が大きいほど、ヒューリスティックな方法でインデックス スキャンが使用される可能性が高いことを示します。
        -   値が小さいほど、ヒューリスティックな方法でテーブル スキャンが使用される可能性が高いことを示します。

### tidb_opt_correlation_threshold {#tidb-opt-correlation-threshold}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.9`
-   範囲: `[0, 1]`
-   この変数は、列順序相関を使用した行数の見積もりを有効にするかどうかを決定するしきい値を設定するために使用されます。現在の列と`handle`列の順序相関がしきい値を超える場合、このメソッドが有効になります。

### tidb_opt_cpu_factor {#tidb-opt-cpu-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `3.0`
-   TiDB が 1 行を処理するための CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_desc_factor {#tidb-opt-desc-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKV がディスクから 1 行を降順でスキャンするためのコストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_disk_factor {#tidb-opt-disk-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `1.5`
-   TiDB が一時ディスクとの間で 1 バイトのデータを読み書きするための I/O コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_distinct_agg_push_down {#tidb-opt-distinct-agg-push-down}

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが集約関数を`distinct` ( `select count(distinct a) from t`など) でコプロセッサーにプッシュ ダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリで`distinct`操作の集計関数が遅い場合は、変数値を`1`に設定できます。

次の例では、 `tidb_opt_distinct_agg_push_down`を有効にする前に、TiDB は TiKV からすべてのデータを読み取り、TiDB 側で`distinct`を実行する必要があります。 `tidb_opt_distinct_agg_push_down`が有効になった後、 `distinct a`がコプロセッサーにプッシュされ、 `group by`列の`test.t.a` `HashAgg_5`に追加されます。

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

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザーが列の順序の相関に基づいて行数を見積もるかどうかを制御するために使用されます

### tidb_opt_force_inline_cte <span class="version-mark">v6.3.0 の新機能</span> {#tidb-opt-force-inline-cte-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、セッション全体の共通テーブル式 (CTE) をインライン化するかどうかを制御するために使用されます。デフォルト値は`OFF`です。これは、インライン CTE がデフォルトで強制されないことを意味します。ただし、 `MERGE()`ヒントを指定して CTE をインライン化することはできます。変数が`ON`に設定されている場合、このセッションのすべての CTE (再帰 CTE を除く) は強制的にインライン化されます。

### tidb_opt_insubq_to_join_and_agg {#tidb-opt-insubq-to-join-and-agg}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、サブクエリを結合および集計に変換する最適化ルールを有効にするかどうかを設定するために使用されます。
-   たとえば、この最適化ルールを有効にすると、サブクエリは次のように変換されます。

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    サブクエリは、次のように結合に変換されます。

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    `t1`が`aa`列の`unique`と`not null`に制限されている場合。次のステートメントは、集計なしで使用できます。

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold {#tidb-opt-join-reorder-threshold}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB 結合したテーブルの再配置アルゴリズムの選択を制御するために使用されます。 結合したテーブルの再配置に参加しているノードの数がこのしきい値より多い場合、TiDB は欲張りアルゴリズムを選択し、このしきい値より少ない場合、TiDB は動的計画法アルゴリズムを選択します。
-   現在、OLTP クエリの場合、デフォルト値を維持することをお勧めします。 OLAP クエリの場合、変数値を 10 ～ 15 に設定して、OLAP シナリオでより適切な接続順序を取得することをお勧めします。

### tidb_opt_limit_push_down_threshold {#tidb-opt-limit-push-down-threshold}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   この変数は、Limit または TopN オペレーターを TiKV にプッシュするかどうかを決定するしきい値を設定するために使用されます。
-   Limit または TopN オペレーターの値がこのしきい値以下の場合、これらのオペレーターは TiKV に強制的にプッシュ ダウンされます。この変数は、部分的に誤った推定が原因で、Limit または TopN オペレーターを TiKV にプッシュダウンできないという問題を解決します。

### tidb_opt_memory_factor {#tidb-opt-memory-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `0.001`
-   TiDB が 1 行を格納するためのメモリコストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">v5.1.0 の新機能</span> {#tidb-opt-mpp-outer-join-fixed-build-side-span-class-version-mark-new-in-v5-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   変数値が`ON`の場合、左側の結合演算子は常にビルド側として内部テーブルを使用し、右側の結合演算子は常にビルド側として外部テーブルを使用します。値を`OFF`に設定すると、外部結合演算子はテーブルのいずれかの側を構築側として使用できます。

### tidb_opt_network_factor {#tidb-opt-network-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.0`
-   ネットワークを介して 1 バイトのデータを転送するための正味コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_prefer_range_scan <span class="version-mark">v5.0 の新機能</span> {#tidb-opt-prefer-range-scan-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数の値を`ON`に設定すると、オプティマイザは常に全表スキャンよりも範囲スキャンを優先します。
-   次の例では、 `tidb_opt_prefer_range_scan`有効にする前に、TiDB オプティマイザーがテーブル全体のスキャンを実行します。 `tidb_opt_prefer_range_scan`を有効にすると、オプティマイザーはインデックス レンジ スキャンを選択します。

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

### tidb_opt_prefix_index_single_scan <span class="version-mark">v6.4.0 の新機能</span> {#tidb-opt-prefix-index-single-scan-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `ON`
-   この変数は、不要なテーブル ルックアップを回避し、クエリ パフォーマンスを向上させるために、TiDB オプティマイザーが一部のフィルター条件をプレフィックス インデックスにプッシュ ダウンするかどうかを制御します。
-   この変数の値を`ON`に設定すると、一部のフィルタ条件がプレフィックス インデックスにプッシュ ダウンされます。 `col`列がテーブルのインデックス プレフィックス列であるとします。クエリの`col is null`または`col is not null`条件は、テーブル ルックアップのフィルター条件ではなく、インデックスのフィルター条件として処理されるため、不要なテーブル ルックアップが回避されます。

<details><summary><code>tidb_opt_prefix_index_single_scan</code>の使用例</summary>

プレフィックス インデックスを使用してテーブルを作成します。

```sql
CREATE TABLE t (a INT, b VARCHAR(10), c INT, INDEX idx_a_b(a, b(5)));
```

無効にする`tidb_opt_prefix_index_single_scan` :

```sql
SET tidb_opt_prefix_index_single_scan = 'OFF';
```

次のクエリでは、実行プランはプレフィックス インデックス`idx_a_b`を使用しますが、テーブル ルックアップが必要です ( `IndexLookUp`演算子が表示されます)。

```sql
EXPLAIN FORMAT='brief' SELECT COUNT(1) FROM t WHERE a = 1 AND b IS NOT NULL;
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| id                            | estRows | task      | access object                | operator info                                         |
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| HashAgg                       | 1.00    | root      |                              | funcs:count(Column#8)->Column#5                       |
| └─IndexLookUp                 | 1.00    | root      |                              |                                                       |
|   ├─IndexRangeScan(Build)     | 99.90   | cop[tikv] | table:t, index:idx_a_b(a, b) | range:[1 -inf,1 +inf], keep order:false, stats:pseudo |
|   └─HashAgg(Probe)            | 1.00    | cop[tikv] |                              | funcs:count(1)->Column#8                              |
|     └─Selection               | 99.90   | cop[tikv] |                              | not(isnull(test.t.b))                                 |
|       └─TableRowIDScan        | 99.90   | cop[tikv] | table:t                      | keep order:false, stats:pseudo                        |
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
6 rows in set (0.00 sec)
```

有効化`tidb_opt_prefix_index_single_scan` :

```sql
SET tidb_opt_prefix_index_single_scan = 'ON';
```

この変数を有効にした後、次のクエリでは、実行プランはプレフィックス インデックス`idx_a_b`を使用しますが、テーブル ルックアップは必要ありません。

```sql
EXPLAIN FORMAT='brief' SELECT COUNT(1) FROM t WHERE a = 1 AND b IS NOT NULL;
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| id                       | estRows | task      | access object                | operator info                                         |
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| StreamAgg                | 1.00    | root      |                              | funcs:count(Column#7)->Column#5                       |
| └─IndexReader            | 1.00    | root      |                              | index:StreamAgg                                       |
|   └─StreamAgg            | 1.00    | cop[tikv] |                              | funcs:count(1)->Column#7                              |
|     └─IndexRangeScan     | 99.90   | cop[tikv] | table:t, index:idx_a_b(a, b) | range:[1 -inf,1 +inf], keep order:false, stats:pseudo |
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
4 rows in set (0.00 sec)
```

</details>

### tidb_opt_projection_push_down <span class="version-mark">v6.1.0 の新機能</span> {#tidb-opt-projection-push-down-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   オプティマイザが TiKV またはTiFlashコプロセッサに`Projection`をプッシュできるようにするかどうかを指定します。

### tidb_opt_range_max_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-opt-range-max-size-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `67108864` (64 MiB)
-   スコープ: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を設定するために使用されます。変数値が`0`の場合、スキャン範囲を構築するためのメモリ制限はありません。正確なスキャン範囲を構築すると制限を超えるメモリが消費される場合、オプティマイザはより緩和されたスキャン範囲 ( `[[NULL,+inf]]`など) を使用します。実行計画で正確なスキャン範囲が使用されていない場合は、この変数の値を増やして、オプティマイザーが正確なスキャン範囲を構築できるようにすることができます。

この変数の使用例は次のとおりです。

<details><summary><code>tidb_opt_range_max_size</code>使用例</summary>

この変数のデフォルト値をビュー。この結果から、オプティマイザが最大 64 MiB のメモリを使用してスキャン範囲を構築していることがわかります。

```sql
SELECT @@tidb_opt_range_max_size;
```

```sql
+----------------------------+
| @@tidb_opt_range_max_size |
+----------------------------+
| 67108864                   |
+----------------------------+
1 row in set (0.01 sec)
```

```sql
EXPLAIN SELECT * FROM t use index (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

次の実行計画の結果に示すように、64 MiB のメモリ上限で、オプティマイザは次の正確なスキャン範囲`[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`を構築します。

```sql
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object            | operator info                                                                                                                                                               |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexLookUp_7                 | 0.90    | root      |                          |                                                                                                                                                                             |
| ├─IndexRangeScan_5(Build)     | 0.90    | cop[tikv] | table:t, index:idx(a, b) | range:[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 0.90    | cop[tikv] | table:t                  | keep order:false, stats:pseudo                                                                                                                                              |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

ここで、オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を 1500 バイトに設定します。

```sql
SET @@tidb_opt_range_max_size = 1500;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

1500 バイトのメモリ制限では、オプティマイザーはより緩和されたスキャン範囲`[10,10], [20,20], [30,30]`を構築し、警告を使用して、正確なスキャン範囲を構築するために必要なメモリ使用量が制限`tidb_opt_range_max_size`を超えていることをユーザーに通知します。

```sql
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
| id                            | estRows | task      | access object            | operator info                                                   |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
| IndexLookUp_8                 | 0.09    | root      |                          |                                                                 |
| ├─Selection_7(Build)          | 0.09    | cop[tikv] |                          | in(test.t.b, 40, 50, 60)                                        |
| │ └─IndexRangeScan_5          | 30.00   | cop[tikv] | table:t, index:idx(a, b) | range:[10,10], [20,20], [30,30], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 0.09    | cop[tikv] | table:t                  | keep order:false, stats:pseudo                                  |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)
```

```sql
SHOW WARNINGS;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                     |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Memory capacity of 1500 bytes for 'tidb_opt_range_max_size' exceeded when building ranges. Less accurate ranges such as full range are chosen |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

次に、メモリ使用量の上限を 100 バイトに設定します。

```sql
set @@tidb_opt_range_max_size = 100;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

100 バイトのメモリ制限では、オプティマイザは`IndexFullScan`を選択し、警告を使用して、正確なスキャン範囲を構築するために必要なメモリが`tidb_opt_range_max_size`の制限を超えていることをユーザーに通知します。

```sql
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
| id                            | estRows  | task      | access object            | operator info                                      |
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
| IndexLookUp_8                 | 8000.00  | root      |                          |                                                    |
| ├─Selection_7(Build)          | 8000.00  | cop[tikv] |                          | in(test.t.a, 10, 20, 30), in(test.t.b, 40, 50, 60) |
| │ └─IndexFullScan_5           | 10000.00 | cop[tikv] | table:t, index:idx(a, b) | keep order:false, stats:pseudo                     |
| └─TableRowIDScan_6(Probe)     | 8000.00  | cop[tikv] | table:t                  | keep order:false, stats:pseudo                     |
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)
```

```sql
SHOW WARNINGS;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                     |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Memory capacity of 100 bytes for 'tidb_opt_range_max_size' exceeded when building ranges. Less accurate ranges such as full range are chosen |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

</details>

### tidb_opt_scan_factor {#tidb-opt-scan-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.5`
-   TiKV がディスクから 1 行のデータを昇順にスキャンするためのコストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_seek_factor {#tidb-opt-seek-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `20`
-   TiDB が TiKV からデータを要求するための起動コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めしません。

### tidb_opt_skew_distinct_agg <span class="version-mark">v6.2.0 の新機能</span> {#tidb-opt-skew-distinct-agg-span-class-version-mark-new-in-v6-2-0-span}

> **ノート：**
>
> この変数を有効にすることによるクエリ パフォーマンスの最適化は**、 TiFlashに対してのみ**有効です。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが`DISTINCT`集約関数を2 レベルの集約関数に書き換えるかどうか ( `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換えるなど) を設定します。集計列に重大なスキューがあり、 `DISTINCT`列に多くの異なる値がある場合、この書き換えにより、クエリ実行でのデータ スキューを回避し、クエリのパフォーマンスを向上させることができます。

### tidb_opt_three_stage_distinct_agg <span class="version-mark">v6.3.0 の新機能</span> {#tidb-opt-three-stage-distinct-agg-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、MPP モードで`COUNT(DISTINCT)`集約を 3 段階集約に書き換えるかどうかを指定します。
-   現在、この変数は`COUNT(DISTINCT)`のみを含む集計に適用されます。

### tidb_opt_tiflash_concurrency_factor {#tidb-opt-tiflash-concurrency-factor}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `24.0`
-   TiFlash演算の同時実行数を示します。この変数はコスト モデルで内部的に使用されるため、値を変更することはお勧めしません。

### tidb_opt_write_row_id {#tidb-opt-write-row-id}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `INSERT` 、 `REPLACE` 、および`UPDATE`ステートメントが`_tidb_rowid`列で操作できるようにするかどうかを制御するために使用されます。この変数は、TiDB ツールを使用してデータをインポートする場合にのみ使用できます。

### tidb_optimizer_selectivity_level {#tidb-optimizer-selectivity-level}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、オプティマイザの推定ロジックの反復を制御します。この変数の値を変更すると、オプティマイザーの見積もりロジックが大幅に変更されます。現在、有効な値は`0`だけです。他の値に設定することはお勧めしません。

### tidb_partition_prune_mode <span class="version-mark">v5.1 の新機能</span> {#tidb-partition-prune-mode-span-class-version-mark-new-in-v5-1-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `dynamic`
-   可能な値: `static` 、 `dynamic` 、 `static-only` 、 `dynamic-only`
-   分割テーブルに`dynamic`または`static`モードのどちらを使用するかを指定します。動的パーティショニングは、完全なテーブル レベルの統計 (GlobalStats) が収集された後にのみ有効になることに注意してください。 GlobalStats が収集される前に、TiDB は代わりに`static`モードを使用します。 GlobalStats の詳細については、 [動的プルーニング モードで分割されたテーブルの統計を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。動的プルーニング モードの詳細については、 [分割されたテーブルの動的プルーニング モード](/partitioned-table.md#dynamic-pruning-mode)を参照してください。

### tidb_persist_analyze_options <span class="version-mark">v5.4.0 の新機能</span> {#tidb-persist-analyze-options-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [ANALYZE 構成の永続性](/statistics.md#persist-analyze-configurations)機能を有効にするかどうかを制御します。

### tidb_placement_mode <span class="version-mark">v6.0.0 の新機能</span> {#tidb-placement-mode-span-class-version-mark-new-in-v6-0-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `STRICT`
-   可能な値: `STRICT` 、 `IGNORE`

<CustomContent platform="tidb">

-   この変数は、DDL ステートメントが[SQL で指定された配置規則](/placement-rules-in-sql.md)無視するかどうかを制御します。変数値が`IGNORE`場合、すべての配置ルール オプションが無視されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、DDL ステートメントが[SQL で指定された配置規則](https://docs.pingcap.com/tidb/stable/placement-rules-in-sql)無視するかどうかを制御します。変数値が`IGNORE`場合、すべての配置ルール オプションが無視されます。

</CustomContent>

-   これは、無効な配置規則が割り当てられている場合でもテーブルを常に作成できるようにするために、論理ダンプ/復元ツールで使用することを目的としています。これは、mysqldump がすべてのダンプ ファイルの先頭に`SET FOREIGN_KEY_CHECKS=0;`を書き込む方法に似ています。

### tidb_pprof_sql_cpu <span class="version-mark">v4.0 の新機能</span> {#tidb-pprof-sql-cpu-span-class-version-mark-new-in-v4-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、パフォーマンスの問題を特定してトラブルシューティングするために、プロファイル出力内の対応する SQL ステートメントをマークするかどうかを制御するために使用されます。

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">v6.1.0 の新機能</span> {#tidb-prepared-plan-cache-memory-guard-ratio-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.1`
-   範囲: `[0, 1]`
-   準備されたプラン キャッシュがメモリ保護メカニズムをトリガーするしきい値。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)を参照してください。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.memory-guard-ratio` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。

### tidb_prepared_plan_cache_size <span class="version-mark">v6.1.0 の新機能</span> {#tidb-prepared-plan-cache-size-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   セッションでキャッシュできるプランの最大数。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)を参照してください。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.capacity` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。

### tidb_projection_concurrency {#tidb-projection-concurrency}

> **警告：**
>
> v5.0 以降、この変数は廃止されました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用します。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、 `Projection`オペレーターの並行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_query_log_max_len {#tidb-query-log-max-len}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `4096` (4 KiB)
-   範囲: `[0, 1073741824]`
-   単位: バイト
-   SQL ステートメント出力の最大長。ステートメントの出力長が`tidb_query_log_max_len`値より大きい場合、ステートメントは切り捨てられて出力されます。
-   この設定は、以前は`tidb.toml`オプション ( `log.query-log-max-len` ) としても使用できましたが、TiDB v6.1.0 以降ではシステム変数のみです。

### tidb_rc_read_check_ts <span class="version-mark">v6.0.0 の新機能</span> {#tidb-rc-read-check-ts-span-class-version-mark-new-in-v6-0-0-span}

> **警告：**
>
> -   この機能は[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。 `tidb_rc_read_check_ts`と`replica-read`同時に有効にしないでください。
> -   クライアントがカーソルを使用する場合、返されたデータの前のバッチがクライアントによって既に使用されており、ステートメントが最終的に失敗する場合に備えて、 `tidb_rc_read_check_ts`有効にすることはお勧めしません。

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、タイムスタンプの取得を最適化するために使用されます。これは、読み取りと書き込みの競合がまれな読み取りコミット分離レベルのシナリオに適しています。この変数を有効にすると、グローバル タイムスタンプを取得する際のレイテンシーとコストを回避でき、トランザクション レベルの読み取りレイテンシーを最適化できます。
-   読み取りと書き込みの競合が深刻な場合、この機能を有効にすると、グローバル タイムスタンプを取得するコストとレイテンシーが増加し、パフォーマンスが低下する可能性があります。詳細については、 [読み取りコミット分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level)を参照してください。

### tidb_rc_write_check_ts <span class="version-mark">v6.3.0 の新機能</span> {#tidb-rc-write-check-ts-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この機能は現在[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。この変数を有効にすると、クライアントから送信されるすべてのリクエストで`replica-read`を使用できなくなります。したがって、 `tidb_rc_write_check_ts`と`replica-read`同時に有効にしないでください。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、タイムスタンプの取得を最適化するために使用され、悲観的トランザクションの`READ-COMMITTED`分離レベルでポイント書き込み競合がほとんどないシナリオに適しています。この変数を有効にすると、ポイント書き込みステートメントの実行中にグローバル タイムスタンプを取得することによって生じるレイテンシーとオーバーヘッドを回避できます。現在、この変数は`UPDATE` 、 `DELETE` 、および`SELECT ...... FOR UPDATE`の 3 種類のポイント書き込みステートメントに適用できます。ポイント書き込みステートメントとは、主キーまたは一意キーをフィルター条件として使用し、最終実行演算子に`POINT-GET`を含む書き込みステートメントを指します。
-   ポイント書き込みの競合が深刻な場合、この変数を有効にすると、余分なオーバーヘッドとレイテンシーが増加し、パフォーマンスが低下します。詳細については、 [読み取りコミット分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level)を参照してください。

### tidb_read_consistency <span class="version-mark">v5.4.0 の新機能</span> {#tidb-read-consistency-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション
-   タイプ: 文字列
-   デフォルト値: `strict`
-   この変数は、自動コミット読み取りステートメントの読み取り一貫性を制御するために使用されます。
-   変数値が`weak`に設定されている場合、read ステートメントで検出されたロックは直接スキップされ、読み取り実行が高速になる可能性があります。これは、弱い一貫性の読み取りモードです。ただし、トランザクションのセマンティクス (原子性など) と分散一貫性 (線形化可能性など) は保証されません。
-   自動コミット読み取りが高速で弱い一貫性の読み取り結果を返す必要があるユーザー シナリオでは、弱い一貫性の読み取りモードを使用できます。

### tidb_read_staleness <span class="version-mark">v5.4.0 の新機能</span> {#tidb-read-staleness-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-2147483648, 0]`
-   この変数は、TiDB が現在のセッションで読み取ることができる履歴データの時間範囲を設定するために使用されます。値を設定した後、TiDB はこの変数によって許可された範囲からできるだけ新しいタイムスタンプを選択し、その後のすべての読み取り操作はこのタイムスタンプに対して実行されます。たとえば、この変数の値が`-5`に設定されている場合、TiKV に対応する履歴バージョンのデータがあるという条件で、TiDB は 5 秒の時間範囲内でできるだけ新しいタイムスタンプを選択します。

### tidb_record_plan_in_slow_log {#tidb-record-plan-in-slow-log}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログにスロー クエリの実行プランを含めるかどうかを制御するために使用されます。

### tidb_redact_log {#tidb-redact-log}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB ログとスローログに記録される SQL ステートメントでユーザー情報を非表示にするかどうかを制御します。
-   変数を`1`に設定すると、ユーザー情報は非表示になります。たとえば、実行された SQL ステートメントが`insert into t values (1,2)`の場合、そのステートメントはログに`insert into t values (?,?)`として記録されます。

### tidb_regard_null_as_point <span class="version-mark">v5.4.0 の新機能</span> {#tidb-regard-null-as-point-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザが null 等価を含むクエリ条件をインデックス アクセスのプレフィックス条件として使用できるかどうかを制御します。
-   この変数はデフォルトで有効になっています。有効にすると、オプティマイザーはアクセスするインデックス データの量を減らすことができるため、クエリの実行が高速化されます。たとえば、クエリに複数列インデックス`index(a, b)`が含まれ、クエリ条件に`a<=>null and b=1`含まれている場合、オプティマイザはインデックス アクセスのクエリ条件で`a<=>null`と`b=1`の両方を使用できます。変数が無効になっている場合、 `a<=>null and b=1`は NULL 等価条件が含まれているため、オプティマイザーはインデックス アクセスに`b=1`を使用しません。

### tidb_remove_orderby_in_subquery <span class="version-mark">v6.1.0 の新機能</span> {#tidb-remove-orderby-in-subquery-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   サブクエリで`ORDER BY`句を削除するかどうかを指定します。

### tidb_replica_read <span class="version-mark">v4.0 の新機能</span> {#tidb-replica-read-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `leader`
-   可能な値: `leader` 、 `follower` 、 `leader-and-follower` 、 `closest-replicas` 、 `closest-adaptive`
-   この変数は、TiDB がデータを読み取る場所を制御するために使用されます。
-   使用法と実装の詳細については、 [Followerの読み取り](/follower-read.md)を参照してください。

### tidb_restricted_read_only <span class="version-mark">v5.2.0 の新機能</span> {#tidb-restricted-read-only-span-class-version-mark-new-in-v5-2-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_restricted_read_only`と[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)同じように動作します。ほとんどの場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを使用する必要があります。
-   `SUPER`または`SYSTEM_VARIABLES_ADMIN`権限を持つユーザーは、この変数を変更できます。ただし、 [Security強化モード](#tidb_enable_enhanced_security)有効になっている場合、この変数の読み取りまたは変更には追加の`RESTRICTED_VARIABLES_ADMIN`権限が必要です。
-   次の場合、 `tidb_restricted_read_only` [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)に影響します。
    -   `tidb_restricted_read_only` ～ `ON`設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) ～ `ON`が更新されます。
    -   `tidb_restricted_read_only` ～ `OFF`に設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)変更されません。
    -   `tidb_restricted_read_only`が`ON`場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) `OFF`に設定することはできません。
-   TiDB の DBaaS プロバイダーの場合、TiDB クラスターが別のデータベースのダウンストリーム データベースである場合、TiDB クラスターを読み取り専用にするには、 [Security強化モード](#tidb_enable_enhanced_security)有効にして`tidb_restricted_read_only`を使用する必要がある場合があります。これにより、顧客は[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)を使用してクラスターを書き込み可能にすることができなくなります。これを実現するには、 [Security強化モード](#tidb_enable_enhanced_security)を有効にし、 `SYSTEM_VARIABLES_ADMIN`および`RESTRICTED_VARIABLES_ADMIN`権限を持つ管理者ユーザーを使用して`tidb_restricted_read_only`制御し、データベース ユーザーが`SUPER`権限を持つ root ユーザーを使用して[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)を制御できるようにする必要があります。
-   この変数は、クラスター全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスター全体のすべての TiDB サーバーが読み取り専用モードになります。この場合、TiDB は`SELECT` 、 `USE` 、および`SHOW`などのデータを変更しないステートメントのみを実行します。 `INSERT`や`UPDATE`などの他のステートメントの場合、TiDB はこれらのステートメントを読み取り専用モードで実行することを拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスター全体が最終的に読み取り専用状態になります。 TiDB クラスターでこの変数の値を変更したが、変更が他の TiDB サーバーにまだ反映されていない場合、更新されていない TiDB サーバーはまだ読み取り専用モードで**はあり**ません。
-   この変数が有効な場合、実行中の SQL ステートメントは影響を受けません。 TiDB は、**実行**される SQL ステートメントの読み取り専用チェックのみを実行します。
-   この変数を有効にすると、TiDB はコミットされていないトランザクションを次の方法で処理します。
    -   コミットされていない読み取り専用トランザクションの場合、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行する SQL ステートメントは拒否されます。
    -   データが変更されたコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードを有効にすると、すべてのユーザー ( `SUPER`特権を持つユーザーを含む) は、明示的に`RESTRICTED_REPLICA_WRITER_ADMIN`特権を付与されない限り、データを書き込む可能性のある SQL ステートメントを実行できません。

### tidb_retry_limit {#tidb-retry-limit}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、楽観的トランザクションの再試行の最大回数を設定するために使用されます。トランザクションで再試行可能なエラー (トランザクションの競合、非常に遅いトランザクション コミット、テーブル スキーマの変更など) が発生すると、このトランザクションはこの変数に従って再実行されます。 `tidb_retry_limit` ～ `0`を設定すると、自動リトライが無効になることに注意してください。この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。

### tidb_row_format_version {#tidb-row-format-version}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   テーブルに新しく保存されたデータの形式バージョンを制御します。 TiDB v4.0 では、新しいデータを保存するためにデフォルトで[新しいstorage行フォーマット](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md)バージョン`2`が使用されます。
-   v4.0.0 より前の TiDB バージョンから v4.0.0 以降のバージョンにアップグレードした場合、フォーマット バージョンは変更されず、TiDB は引き続きバージョン`1`の古いフォーマットを使用して**テーブル**にデータを書き込みます。<strong>作成されたクラスターは、デフォルトで新しいデータ形式を使用します</strong>。
-   この変数を変更しても、保存された古いデータには影響しませんが、この変数を変更した後に新しく書き込まれたデータにのみ、対応するバージョン形式が適用されることに注意してください。

### tidb_scatter_region {#tidb-scatter-region}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   デフォルトでは、TiDB で作成された新しいテーブルのリージョンは分割されます。この変数を有効にすると、新しく分割されたリージョンは`CREATE TABLE`ステートメントの実行中にすぐに分散されます。これは、テーブルがバッチで作成された直後にデータをバッチで書き込む必要があるシナリオに適用されます。これは、新しく分割されたリージョンを事前に TiKV に分散させることができ、PD によってスケジュールされるのを待つ必要がないためです。バッチでのデータ書き込みの継続的な安定性を確保するために、 `CREATE TABLE`ステートメントは、リージョンが正常に分散された後にのみ成功を返します。これにより、ステートメントの実行時間が、この変数を無効にした場合よりも数倍長くなります。
-   テーブルの作成時に`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`が設定されている場合、テーブルの作成後に指定された数のリージョンが均等に分割されます。

### tidb_server_memory_limit <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `80%`
-   範囲：
    -   パーセンテージ形式で値を設定できます。これは、合計メモリに対するメモリ使用量のパーセンテージを意味します。値の範囲は`[1%, 99%]`です。
    -   メモリサイズで値を設定することもできます。値の範囲は`0` ～ `[536870912, 9223372036854775807]`バイトです。 「KB|MB|GB|TB」単位のメモリフォーマットに対応しています。 `0`メモリ制限なしを意味します。
    -   この変数が`0`ではなく 512 MB 未満のメモリサイズに設定されている場合、TiDB は実際のサイズとして 512 MB を使用します。
-   この変数は、TiDB インスタンスのメモリ制限を指定します。 TiDB のメモリ使用量が上限に達すると、TiDB は現在実行中のメモリ使用量が最も多い SQL ステートメントをキャンセルします。 SQL ステートメントが正常にキャンセルされた後、TiDB はGolang GC を呼び出して、すぐにメモリを再利用し、できるだけ早くメモリストレスを軽減しようとします。
-   最初に取り消される SQL ステートメントとして、 [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)制限より多くのメモリ使用量を持つ SQL ステートメントのみが選択されます。
-   現在、TiDB は一度に 1 つの SQL ステートメントのみをキャンセルします。 TiDB が SQL ステートメントを完全にキャンセルしてリソースを回復した後、メモリ使用量がまだこの変数で設定された制限を超えている場合、TiDB は次のキャンセル操作を開始します。

### tidb_server_memory_limit_gc_trigger <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-gc-trigger-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `70%`
-   範囲: `[50%, 99%]`
-   TiDB が GC をトリガーしようとするしきい値。 TiDB のメモリ使用量が`tidb_server_memory_limit` * `tidb_server_memory_limit_gc_trigger`の値に達すると、TiDB はGolang GC 操作をアクティブにトリガーします。 1 分間にトリガーされる GC 操作は 1 つだけです。

### tidb_server_memory_limit_sess_min_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-sess-min-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `134217728` (128 MB)
-   範囲: `[128, 9223372036854775807]` 、バイト単位。単位が「KB|MB|GB|TB」のメモリフォーマットにも対応しています。
-   メモリ制限を有効にすると、TiDB は現在のインスタンスでメモリ使用量が最も多い SQL ステートメントを終了します。この変数は、終了する SQL ステートメントの最小メモリ使用量を指定します。制限を超える TiDB インスタンスのメモリ使用量が、メモリ使用量の少ないセッションが多すぎることが原因である場合は、この変数の値を適切に下げて、より多くのセッションをキャンセルできるようにすることができます。

### tidb_shard_allocate_step <span class="version-mark">v5.0 の新機能</span> {#tidb-shard-allocate-step-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `9223372036854775807`
-   範囲: `[1, 9223372036854775807]`
-   この変数は、 [`AUTO_RANDOM`](/auto-random.md)または[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)属性に割り当てられる連続 ID の最大数を制御します。通常、 `AUTO_RANDOM` ID または`SHARD_ROW_ID_BITS`の注釈付き行 ID は、1 つのトランザクションで増分的かつ連続的です。この変数を使用して、大規模なトランザクション シナリオでホットスポットの問題を解決できます。

### tidb_simplified_metrics {#tidb-simplified-metrics}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数が有効になっている場合、TiDB は Grafana パネルで使用されていないメトリックを収集または記録しません。

### tidb_skip_ascii_check <span class="version-mark">v5.0 の新機能</span> {#tidb-skip-ascii-check-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ASCII 検証をスキップするかどうかを設定するために使用されます。
-   ASCII 文字の検証はパフォーマンスに影響します。入力文字が有効な ASCII 文字であることを確認したら、変数値を`ON`に設定できます。

### tidb_skip_isolation_level_check {#tidb-skip-isolation-level-check}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   このスイッチを有効にした後、TiDB でサポートされていない分離レベルが`tx_isolation`に割り当てられた場合、エラーは報告されません。これにより、異なる分離レベルを設定する (ただし依存しない) アプリケーションとの互換性が向上します。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_utf8_check {#tidb-skip-utf8-check}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、UTF-8 検証をスキップするかどうかを設定するために使用されます。
-   UTF-8 文字の検証はパフォーマンスに影響します。入力文字が有効な UTF-8 文字であることを確認したら、変数値を`ON`に設定できます。

> **ノート：**
>
> 文字チェックがスキップされると、TiDB はアプリケーションによって書き込まれた不正な UTF-8 文字の検出に失敗し、 `ANALYZE`の実行時にデコード エラーが発生し、その他の未知のエンコーディングの問題が発生する可能性があります。アプリケーションが書き込まれた文字列の有効性を保証できない場合、文字チェックをスキップすることはお勧めしません。

### tidb_slow_log_threshold {#tidb-slow-log-threshold}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   Persists to cluster: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[-1, 9223372036854775807]`
-   単位: ミリ秒
-   この変数は、スローログの消費時間のしきい値を出力するために使用されます。クエリの消費時間がこの値よりも大きい場合、そのクエリはスロー ログと見なされ、そのログがスロー クエリ ログに出力されます。

### tidb_slow_query_file {#tidb-slow-query-file}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション
-   デフォルト値: &quot;&quot;
-   `INFORMATION_SCHEMA.SLOW_QUERY`がクエリされると、構成ファイルで`slow-query-file`によって設定されたスロー クエリ ログ名のみが解析されます。デフォルトのスロー クエリ ログ名は「tidb-slow.log」です。他のログを解析するには、 `tidb_slow_query_file`セッション変数を特定のファイル パスに設定し、 `INFORMATION_SCHEMA.SLOW_QUERY`をクエリして、設定されたファイル パスに基づいてスロー クエリ ログを解析します。

<CustomContent platform="tidb">

詳細については、 [遅いクエリを特定する](/identify-slow-queries.md)を参照してください。

</CustomContent>

### tidb_snapshot {#tidb-snapshot}

-   スコープ: セッション
-   デフォルト値: &quot;&quot;
-   この変数は、セッションによってデータが読み取られる時点を設定するために使用されます。たとえば、変数を「2017-11-11 20:20:20」または「400036290571534337」のような TSO 番号に設定すると、現在のセッションはこの時点のデータを読み取ります。

### tidb_source_id <span class="version-mark">v6.5.0 の新機能</span> {#tidb-source-id-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 15]`

<CustomContent platform="tidb">

-   この変数は、 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)クラスターで異なるクラスター ID を構成するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [双方向レプリケーション](https://docs.pingcap.com/tidb/stable/ticdc-bidirectional-replication)クラスターで異なるクラスター ID を構成するために使用されます。

</CustomContent>

### tidb_stats_cache_mem_quota <span class="version-mark">v6.1.0 の新機能</span> {#tidb-stats-cache-mem-quota-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> この変数は実験的機能です。本番環境で使用することはお勧めしません。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 1099511627776]`
-   この変数は、TiDB 統計キャッシュのメモリクォータを設定します。

### tidb_stats_load_pseudo_timeout <span class="version-mark">v5.4.0 の新機能</span> {#tidb-stats-load-pseudo-timeout-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、SQL 最適化の待機時間がタイムアウトに達したときの TiDB の動作を制御して、完全な列統計を同期的にロードします。デフォルト値`ON`は、SQL 最適化がタイムアウト後に疑似統計の使用に戻ることを意味します。この変数が`OFF`場合、SQL の実行はタイムアウト後に失敗します。

### tidb_stats_load_sync_wait <span class="version-mark">v5.4.0 の新機能</span> {#tidb-stats-load-sync-wait-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   この変数は、同期ロード統計機能を有効にするかどうかを制御します。値`0` 、機能が無効であることを意味します。この機能を有効にするには、この変数をタイムアウト (ミリ秒単位) に設定します。これは、SQL 最適化が完全な列統計を同期的にロードするまで最大で待機できる時間です。詳細については、 [負荷統計](/statistics.md#load-statistics)を参照してください。

### tidb_stmt_summary_history_size <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-history-size-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `24`
-   範囲: `[0, 255]`
-   この変数は、履歴容量[ステートメント要約表](/statement-summary-tables.md)を設定するために使用されます。

### tidb_stmt_summary_internal_query <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-internal-query-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB の SQL 情報を[ステートメント要約表](/statement-summary-tables.md)に含めるかどうかを制御するために使用されます。

### tidb_stmt_summary_max_sql_length <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-max-sql-length-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `4096`
-   範囲: `[0, 2147483647]`
-   この変数は、 [ステートメント要約表](/statement-summary-tables.md)の SQL 文字列の長さを制御するために使用されます。

### tidb_stmt_summary_max_stmt_count <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-max-stmt-count-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `3000`
-   範囲: `[1, 32767]`
-   この変数は、メモリに格納[ステートメント要約表](/statement-summary-tables.md)ステートメントの最大数を設定するために使用されます。

### tidb_stmt_summary_refresh_interval <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-refresh-interval-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1800`
-   範囲: `[1, 2147483647]`
-   単位: 秒
-   この変数は、リフレッシュ時間を[ステートメント要約表](/statement-summary-tables.md)に設定するために使用されます。

### tidb_store_batch_size {#tidb-store-batch-size}

> **警告：**
>
> 現在、 `tidb_store_batch_size`はまだ安定していません。この変数は、将来のリリースで削除される可能性があります。本番環境で使用することはお勧めしません。デフォルト値を変更することはお勧めしません。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 25000]`
-   この変数は、 `IndexLookUp`オペレーターのコプロセッサー・タスクのバッチ・サイズを制御するために使用されます。 `0`バッチを無効にすることを意味します。タスクの数が比較的多く、低速のクエリが発生する場合は、この変数を増やしてクエリを最適化できます。

### tidb_store_limit <span class="version-mark">v3.0.4 および v4.0 の新機能</span> {#tidb-store-limit-span-class-version-mark-new-in-v3-0-4-and-v4-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、TiDB が同時に TiKV に送信できるリクエストの最大数を制限するために使用されます。 0 は無制限を意味します。

### tidb_streamagg_concurrency {#tidb-streamagg-concurrency}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   この変数は、クエリが実行されるときの`StreamAgg`演算子の同時実行を設定します。
-   この変数を設定すること**はお勧めし**ません。変数値を変更すると、データの正確性の問題が発生する可能性があります。

### tidb_super_read_only <span class="version-mark">v5.3.1 の新機能</span> {#tidb-super-read-only-span-class-version-mark-new-in-v5-3-1-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_super_read_only` MySQL 変数`super_read_only`の代わりとして実装されることを目的としています。ただし、TiDB は分散データベースであるため、 `tidb_super_read_only`実行直後にデータベースを読み取り専用にするのではなく、最終的にデータベースを読み取り専用にします。
-   `SUPER`または`SYSTEM_VARIABLES_ADMIN`権限を持つユーザーは、この変数を変更できます。
-   この変数は、クラスター全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスター全体のすべての TiDB サーバーが読み取り専用モードになります。この場合、TiDB は`SELECT` 、 `USE` 、および`SHOW`などのデータを変更しないステートメントのみを実行します。 `INSERT`や`UPDATE`などの他のステートメントの場合、TiDB はこれらのステートメントを読み取り専用モードで実行することを拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスター全体が最終的に読み取り専用状態になります。 TiDB クラスターでこの変数の値を変更したが、変更が他の TiDB サーバーにまだ反映されていない場合、更新されていない TiDB サーバーはまだ読み取り専用モードで**はあり**ません。
-   TiDB は、SQL ステートメントが実行される前に読み取り専用フラグをチェックします。 v6.2.0 以降、フラグは SQL ステートメントがコミットされる前にもチェックされます。これにより、サーバーが読み取り専用モードになった後に、長時間実行される[自動コミット](/transaction-overview.md#autocommit)ステートメントによってデータが変更される可能性を防ぐことができます。
-   この変数を有効にすると、TiDB はコミットされていないトランザクションを次の方法で処理します。
    -   コミットされていない読み取り専用トランザクションの場合、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行する SQL ステートメントは拒否されます。
    -   データが変更されたコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードを有効にすると、すべてのユーザー ( `SUPER`特権を持つユーザーを含む) は、明示的に`RESTRICTED_REPLICA_WRITER_ADMIN`特権を付与されない限り、データを書き込む可能性のある SQL ステートメントを実行できません。
-   システム変数[`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520) `ON`に設定されている場合、 `tidb_super_read_only` [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の影響を受ける場合があります。詳細な影響については、 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の説明を参照してください。

### tidb_sysdate_is_now <span class="version-mark">v6.0.0 の新機能</span> {#tidb-sysdate-is-now-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `SYSDATE`機能を`NOW`機能に置き換えることができるかどうかを制御するために使用されます。この構成項目は、MySQL オプション[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。

### tidb_sysproc_scan_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-sysproc-scan-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、TiDB が内部 SQL ステートメント (統計の自動更新など) を実行するときに実行されるスキャン操作の並行性を設定するために使用されます。

### tidb_table_cache_lease <span class="version-mark">v6.0.0 の新機能</span> {#tidb-table-cache-lease-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `3`
-   範囲: `[1, 10]`
-   単位: 秒
-   この変数は、デフォルト値`3`でリース時間を[キャッシュされたテーブル](/cached-tables.md)に制御するために使用されます。この変数の値は、キャッシュされたテーブルの変更に影響します。キャッシュされたテーブルに変更が加えられた後、最長の待機時間は`tidb_table_cache_lease`秒になる場合があります。テーブルが読み取り専用であるか、高い書き込みレイテンシーを許容できる場合は、この変数の値を増やして、テーブルをキャッシュする有効時間を増やし、リース更新の頻度を減らすことができます。

### tidb_tmp_table_max_size <span class="version-mark">v5.3.0 の新機能</span> {#tidb-tmp-table-max-size-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[1048576, 137438953472]`
-   単位: バイト
-   この変数は、単一の[一時テーブル](/temporary-tables.md)の最大サイズを設定するために使用されます。この変数の値より大きいサイズの一時テーブルは、エラーの原因になります。

### tidb_top_sql_max_meta_count <span class="version-mark">v6.0.0 の新機能</span> {#tidb-top-sql-max-meta-count-span-class-version-mark-new-in-v6-0-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `5000`
-   範囲: `[1, 10000]`

<CustomContent platform="tidb">

-   この変数は、 [Top SQL](/dashboard/top-sql.md)分間に 1 つずつ収集される SQL ステートメント タイプの最大数を制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)分間に 1 つずつ収集される SQL ステートメント タイプの最大数を制御するために使用されます。

</CustomContent>

### tidb_top_sql_max_time_series_count <span class="version-mark">v6.0.0 の新機能</span> {#tidb-top-sql-max-time-series-count-span-class-version-mark-new-in-v6-0-0-span}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **ノート：**
>
> 現在、TiDB ダッシュボードのTop SQLページには、負荷に最も貢献している上位 5 種類の SQL クエリのみが表示されますが、これは`tidb_top_sql_max_time_series_count`の構成とは無関係です。

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 5000]`

<CustomContent platform="tidb">

-   この変数は、負荷に最も寄与する SQL ステートメント (つまり、上位 N 個) を[Top SQL](/dashboard/top-sql.md)ずつ記録できる数を制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、負荷に最も寄与する SQL ステートメント (つまり、上位 N 個) を 1 分あたり[Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)ずつ記録できる数を制御するために使用されます。

</CustomContent>

### tidb_track_aggregate_memory_usage {#tidb-track-aggregate-memory-usage}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB が集計関数のメモリ使用量を追跡するかどうかを制御します。

> **警告：**
>
> この変数を無効にすると、TiDB はメモリ使用量を正確に追跡できず、対応する SQL ステートメントのメモリ使用量を制御できなくなります。

### tidb_tso_client_batch_max_wait_time <span class="version-mark">v5.3.0 の新機能</span> {#tidb-tso-client-batch-max-wait-time-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 10]`
-   範囲: `[0, 10]`
-   単位: ミリ秒
-   この変数は、TiDB が PD から TSO を要求するときのバッチ操作の最大待機時間を設定するために使用されます。デフォルト値は`0`で、余分な待ち時間がないことを意味します。
-   PD から TSO リクエストを毎回取得する際、TiDB が使用する PD Client は、同時に受信した TSO リクエストをできるだけ多く収集します。次に、PD クライアントは、収集されたリクエストをバッチで 1 つの RPC リクエストにマージし、リクエストを PD に送信します。これにより、PD への負担が軽減されます。
-   この変数を`0`より大きい値に設定した後、TiDB は、各バッチ マージが終了する前に、この値の最大期間待機します。これは、より多くの TSO 要求を収集し、バッチ操作の効果を向上させるためです。
-   この変数の値を増やすシナリオ:
    -   TSO 要求の負荷が高いため、PD リーダーの CPU がボトルネックに達し、TSO RPC 要求のレイテンシーが長くなります。
    -   クラスター内の TiDB インスタンスの数は多くありませんが、すべての TiDB インスタンスは高い同時実行性を維持しています。
-   この変数はできるだけ小さい値に設定することをお勧めします。

> **ノート：**
>
> PD リーダーの CPU 使用率のボトルネック以外の理由 (ネットワークの問題など) で、TSO RPCレイテンシーが増加したとします。この場合、値`tidb_tso_client_batch_max_wait_time`を増やすと、TiDB での実行レイテンシーが増加し、クラスターの QPS パフォーマンスに影響を与える可能性があります。

### tidb_ttl_delete_rate_limit <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-rate-limit-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、各 TiDB ノードの TTL ジョブで`DELETE`ステートメントのレートを制限するために使用されます。この値は、TTL ジョブの単一ノードで 1 秒間に許可される`DELETE`のステートメントの最大数を表します。この変数が`0`に設定されている場合、制限は適用されません。

### tidb_ttl_delete_batch_size <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `100`
-   範囲: `[1, 10240]`
-   この変数は、TTL ジョブの`DELETE`つのトランザクションで削除できる行の最大数を設定するために使用されます。

### tidb_ttl_delete_worker_count <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各 TiDB ノードでの TTL ジョブの最大同時実行数を設定するために使用されます。

### tidb_ttl_job_enable <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-enable-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、TTL ジョブを有効にするかどうかを制御するために使用されます。 `OFF`に設定されている場合、TTL 属性を持つすべてのテーブルは、期限切れデータのクリーンアップを自動的に停止します。

### tidb_ttl_scan_batch_size <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-scan-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `500`
-   範囲: `[1, 10240]`
-   この変数は、TTL ジョブで期限切れデータをスキャンするために使用される各`SELECT`ステートメントの`LIMIT`値を設定するために使用されます。

### tidb_ttl_scan_worker_count <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-scan-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各 TiDB ノードでの TTL スキャン ジョブの最大同時実行数を設定するために使用されます。

### tidb_ttl_job_run_interval <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-run-interval-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `1h0m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   この変数は、バックグラウンドでの TTL ジョブのスケジューリング間隔を制御するために使用されます。たとえば、現在の値が`1h0m0s`に設定されている場合、TTL 属性を持つ各テーブルは、1 時間ごとに期限切れのデータをクリーンアップします。

### tidb_ttl_job_schedule_window_start_time <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-schedule-window-start-time-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   タイプ: 時間
-   クラスターに永続化: はい
-   デフォルト値: `00:00 +0000`
-   この変数は、バックグラウンドでの TTL ジョブのスケジューリング ウィンドウの開始時刻を制御するために使用されます。この変数の値を変更するときは、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。

### tidb_ttl_job_schedule_window_end_time <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-schedule-window-end-time-span-class-version-mark-new-in-v6-5-0-span}

> **警告：**
>
> [TTL](/time-to-live.md)は実験的機能です。このシステム変数は、将来のリリースで変更または削除される可能性があります。

-   範囲: グローバル
-   タイプ: 時間
-   クラスターに永続化: はい
-   デフォルト値: `23:59 +0000`
-   この変数は、バックグラウンドでの TTL ジョブのスケジューリング ウィンドウの終了時間を制御するために使用されます。この変数の値を変更するときは、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。

### tidb_txn_assertion_level <span class="version-mark">v6.0.0 の新機能</span> {#tidb-txn-assertion-level-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション |グローバル

-   クラスターに永続化: はい

-   タイプ: 列挙

-   デフォルト値: `FAST`

-   可能な値: `OFF` 、 `FAST` 、 `STRICT`

-   この変数は、アサーション レベルを制御するために使用されます。アサーションは、データとインデックス間の整合性チェックであり、トランザクションのコミット プロセスで、書き込まれているキーが存在するかどうかをチェックします。詳細については、 [データとインデックス間の不一致のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)を参照してください。

    -   `OFF` : このチェックを無効にします。
    -   `FAST` : ほとんどのチェック項目を有効にしますが、パフォーマンスにはほとんど影響しません。
    -   `STRICT` : すべてのチェック項目を有効にします。システムのワークロードが高い場合、悲観的トランザクション パフォーマンスにわずかな影響があります。

-   v6.0.0 以降のバージョンの新しいクラスターの場合、デフォルト値は`FAST`です。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_txn_commit_batch_size <span class="version-mark">v6.2.0 の新機能</span> {#tidb-txn-commit-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `16384`
-   範囲: `[1, 1073741824]`
-   単位: バイト

<CustomContent platform="tidb">

-   この変数は、TiDB が TiKV に送信するトランザクション コミット リクエストのバッチ サイズを制御するために使用されます。アプリケーション ワークロード内のほとんどのトランザクションに多数の書き込み操作がある場合、この変数をより大きな値に調整すると、バッチ処理のパフォーマンスを向上させることができます。ただし、この変数が大きすぎる値に設定され、TiKV の[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)の制限を超えると、コミットが失敗する可能性があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB が TiKV に送信するトランザクション コミット リクエストのバッチ サイズを制御するために使用されます。アプリケーション ワークロード内のほとんどのトランザクションに多数の書き込み操作がある場合、この変数をより大きな値に調整すると、バッチ処理のパフォーマンスを向上させることができます。ただし、この変数が大きすぎる値に設定され、TiKV の単一ログの最大サイズ (デフォルトでは 8 MB) の制限を超えると、コミットが失敗する可能性があります。

</CustomContent>

### tidb_txn_mode {#tidb-txn-mode}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `pessimistic`
-   可能な値: `pessimistic` 、 `optimistic`
-   この変数は、トランザクション モードを設定するために使用されます。 TiDB 3.0 は悲観的トランザクションをサポートしています。 TiDB 3.0.8 以降、デフォルトで[悲観的トランザクション モード](/pessimistic-transaction.md)が有効になっています。
-   TiDB を v3.0.7 以前のバージョンから v3.0.8 以降のバージョンにアップグレードしても、デフォルトのトランザクション モードは変更されません。**新しく作成されたクラスタだけがデフォルトで悲観的トランザクション モードを使用します**。
-   この変数が「楽観的」または「」に設定されている場合、TiDB は[楽観的トランザクション モード](/optimistic-transaction.md)を使用します。

### tidb_use_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-use-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、実行計画バインディング機能を有効にするかどうかを制御するために使用されます。これはデフォルトで有効になっており、値`OFF`を割り当てることで無効にすることができます。実行計画バインディングの使用については、 [実行計画バインディング](/sql-plan-management.md#create-a-binding)を参照してください。

### tidb_wait_split_region_finish {#tidb-wait-split-region-finish}

-   スコープ: セッション
-   タイプ: ブール値
-   デフォルト値: `ON`
-   通常、PD のスケジューリングと TiKV の負荷によって決定されるリージョンの分散には長い時間がかかります。この変数は、 `SPLIT REGION`ステートメントが実行されているときに、すべてのリージョンが完全に分散された後に結果をクライアントに返すかどうかを設定するために使用されます。
    -   `ON`指定すると、すべてのリージョンが分散されるまで`SPLIT REGIONS`ステートメントが待機する必要があります。
    -   `OFF`すべての領域の分散を終了する前に`SPLIT REGIONS`ステートメントを返すことを許可します。
-   リージョンを分散すると、分散されているリージョンの書き込みおよび読み取りパフォーマンスが影響を受ける可能性があることに注意してください。バッチ書き込みまたはデータ インポートのシナリオでは、リージョンの分散が完了した後にデータをインポートすることをお勧めします。

### tidb_wait_split_region_timeout {#tidb-wait-split-region-timeout}

-   スコープ: セッション
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[1, 2147483647]`
-   単位: 秒
-   この変数は、 `SPLIT REGION`ステートメントを実行するためのタイムアウトを設定するために使用されます。指定された時間値内にステートメントが完全に実行されない場合、タイムアウト エラーが返されます。

### tidb_window_concurrency <span class="version-mark">v4.0 の新機能</span> {#tidb-window-concurrency-span-class-version-mark-new-in-v4-0-span}

> **警告：**
>
> v5.0 以降、この変数は廃止されました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用します。

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、ウィンドウ オペレーターの同時実行度を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tiflash_fastscan <span class="version-mark">v6.3.0 の新機能</span> {#tiflash-fastscan-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション |グローバル
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   [ファストスキャン](/develop/dev-guide-use-fastscan.md)が有効になっている ( `ON`に設定されている) 場合、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度やデータの一貫性は保証されません。

### tiflash_fine_grained_shuffle_batch_size <span class="version-mark">v6.2.0 の新機能</span> {#tiflash-fine-grained-shuffle-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション |グローバル
-   デフォルト値: `8192`
-   範囲: `[1, 18446744073709551615]`
-   Fine Grained Shuffle が有効な場合、 TiFlashにプッシュ ダウンされたウィンドウ関数を並行して実行できます。この変数は、送信者によって送信されるデータのバッチ サイズを制御します。
-   パフォーマンスへの影響: ビジネス要件に従って適切なサイズを設定します。不適切な設定はパフォーマンスに影響します。たとえば`1`ように値が小さすぎると、ブロックごとに 1 つのネットワーク転送が発生します。テーブルの総行数など、値が大きすぎると、受信側でデータの待機にほとんどの時間が費やされ、パイプライン化された計算が機能しなくなります。適切な値を設定するために、 TiFlashレシーバーが受信した行数の分布を観察できます。ほとんどのスレッドが数行 (数百行など) しか受信しない場合は、この値を増やしてネットワーク オーバーヘッドを減らすことができます。

### tiflash_fine_grained_shuffle_stream_count <span class="version-mark">v6.2.0 の新機能</span> {#tiflash-fine-grained-shuffle-stream-count-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-1, 1024]`
-   ウィンドウ関数が実行のためにTiFlashにプッシュされると、この変数を使用してウィンドウ関数実行の同時実行レベルを制御できます。可能な値は次のとおりです。

    -   -1: ファイン グレイン シャッフル機能が無効になります。 TiFlashにプッシュされたウィンドウ関数は、シングル スレッドで実行されます。
    -   0: ファイン グレイン シャッフル機能が有効になります。 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)が有効な値 (0 より大きい) に設定されている場合、 `tiflash_fine_grained_shuffle_stream_count`は値[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)に設定されます。それ以外の場合は、8 に設定されますTiFlashでのウィンドウ関数の実際の同時実行レベルは、min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノードの物理スレッドの数) です。
    -   0 より大きい整数: ファイングレイン シャッフル機能が有効になっています。 TiFlashにプッシュされたウィンドウ関数は、複数のスレッドで実行されます。同時実行レベルは次のとおりです。min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノード上の物理スレッドの数)。
-   理論的には、ウィンドウ関数のパフォーマンスはこの値に比例して向上します。ただし、値が実際の物理スレッド数を超えると、代わりにパフォーマンスが低下します。

### タイムゾーン {#time-zone}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   デフォルト値: `SYSTEM`
-   この変数は、現在のタイム ゾーンを返します。値は、「-8:00」などのオフセットまたは名前付きゾーン「America/Los_Angeles」として指定できます。
-   値`SYSTEM` 、タイム ゾーンがシステム ホストと同じであることを意味します。これは、変数[`system_time_zone`](#system_time_zone)を介して利用できます。

### タイムスタンプ {#timestamp}

-   スコープ: セッション
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数の空でない値は`NOW()` `CURRENT_TIMESTAMP()`およびその他の関数のタイムスタンプとして使用される UNIX エポックを示します。この変数は、データの復元または複製で使用される場合があります。

### トランザクション分離 {#transaction-isolation}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `REPEATABLE-READ`
-   可能な値: `READ-UNCOMMITTED` 、 `READ-COMMITTED` 、 `REPEATABLE-READ` 、 `SERIALIZABLE`
-   この変数は、トランザクションの分離を設定します。 TiDB は MySQL との互換性のために`REPEATABLE-READ`アドバタイズしますが、実際の分離レベルはスナップショット分離です。詳細については、 [トランザクション分離レベル](/transaction-isolation-levels.md)参照してください。

### tx_isolation {#tx-isolation}

この変数は`transaction_isolation`のエイリアスです。

### tx_isolation_one_shot {#tx-isolation-one-shot}

> **ノート：**
>
> この変数は、TiDB で内部的に使用されます。使用することは想定されていません。

内部的に、TiDB パーサーは`SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]`ステートメントを`SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`に変換します。

### tx_read_ts {#tx-read-ts}

-   スコープ: セッション
-   デフォルト値: &quot;&quot;
-   ステイル読み取りのシナリオでは、このセッション変数を使用して、安定した読み取りのタイムスタンプ値を記録します。
-   この変数は、TiDB の内部操作に使用されます。この変数を設定すること**はお勧めし**ません。

### txn_scope {#txn-scope}

-   スコープ: セッション
-   デフォルト値: `global`
-   値のオプション: `global`および`local`
-   この変数は、現在のセッション トランザクションがグローバル トランザクションかローカル トランザクションかを設定するために使用されます。
-   この変数は、TiDB の内部操作に使用されます。この変数を設定すること**はお勧めし**ません。

### validate_password.check_user_name <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-check-user-name-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、パスワード複雑度チェックのチェック項目です。パスワードがユーザー名と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効です。
-   この変数が有効で`ON`に設定されている場合、パスワードを設定すると、TiDB はパスワードをユーザー名 (ホスト名を除く) と比較します。パスワードがユーザー名と一致する場合、パスワードは拒否されます。
-   この変数は[`validate_password.policy`](#validate_passwordpolicy-new-in-v650)とは無関係であり、パスワードの複雑さチェック レベルの影響を受けません。

### validate_password.dictionary <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-dictionary-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `""`
-   タイプ: 文字列
-   この変数は、パスワード複雑度チェックのチェック項目です。パスワードが辞書と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`2` (STRONG) に設定されている場合にのみ有効です。
-   この変数は、1024 文字以内の文字列です。パスワードに存在できない単語のリストが含まれています。各単語はセミコロン ( `;` ) で区切られます。
-   この変数は、デフォルトで空の文字列に設定されています。これは、辞書チェックが実行されないことを意味します。辞書チェックを実行するには、一致させる単語を文字列に含める必要があります。この変数が構成されている場合、パスワードを設定すると、TiDB はパスワードの各部分文字列 (4 ～ 100 文字の長さ) を辞書内の単語と比較します。パスワードの部分文字列が辞書内の単語と一致する場合、パスワードは拒否されます。比較では大文字と小文字が区別されません。

### validate_password.enable <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-enable-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数が`ON`に設定されている場合、TiDB はパスワードの設定時にパスワードの複雑さのチェックを実行します。

### validate_password.length <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-length-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `8`
-   範囲: `[0, 2147483647]`
-   この変数は、パスワード複雑度チェックのチェック項目です。パスワードの長さが十分かどうかをチェックします。デフォルトでは、最小パスワード長は`8`です。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効です。
-   この変数の値は、式`validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`よりも小さくすることはできません。
-   式の値が`validate_password.length`より大きくなるように`validate_password.number_count` 、 `validate_password.special_char_count` 、または`validate_password.mixed_case_count`の値を変更すると、式の値と一致するように`validate_password.length`の値が自動的に変更されます。

### validate_password.mixed_case_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-mixed-case-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2147483647]`
-   この変数は、パスワード複雑度チェックのチェック項目です。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。
-   パスワードの大文字の数も小文字の数も、値`validate_password.mixed_case_count`より少なくすることはできません。たとえば、変数が`1`に設定されている場合、パスワードには少なくとも 1 つの大文字と 1 つの小文字が含まれている必要があります。

### validate_password.number_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-number-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2147483647]`
-   この変数は、パスワード複雑度チェックのチェック項目です。パスワードに十分な数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。

### validate_password.policy <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-policy-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 列挙
-   デフォルト値: `1`
-   値のオプション: `0` 、 `1` 、 `2`
-   この変数は、パスワードの複雑さチェックのポリシーを制御します。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効になっている場合にのみ有効です。この変数の値は、 `validate_password.check_user_name`を除く他の`validate-password`変数がパスワードの複雑さのチェックで有効になるかどうかを決定します。
-   この変数の値は`0` 、 `1` 、または`2`です (LOW、MEDIUM、または STRONG に対応)。ポリシー レベルごとに異なるチェックがあります。
    -   0 または LOW: パスワードの長さ。
    -   1 または MEDIUM: パスワードの長さ、大文字と小文字、数字、および特殊文字。
    -   2 または STRONG: パスワードの長さ、大文字と小文字、数字、特殊文字、および辞書の一致。

### validate_password.special_char_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-special-char-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2147483647]`
-   この変数は、パスワード複雑度チェックのチェック項目です。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。

### バージョン {#version}

-   スコープ: なし
-   デフォルト値: `5.7.25-TiDB-` (tidb バージョン)
-   この変数は、MySQL のバージョンに続いて TiDB のバージョンを返します。たとえば、「5.7.25-TiDB-v4.0.0-beta.2-716-g25e003253」です。

### version_comment {#version-comment}

-   スコープ: なし
-   デフォルト値: (文字列)
-   この変数は、TiDB のバージョンに関する追加の詳細を返します。たとえば、「TiDB Server (Apache License 2.0) Community Edition、 MySQL 5.7互換」などです。

### version_compile_machine {#version-compile-machine}

-   スコープ: なし
-   デフォルト値: (文字列)
-   この変数は、TiDB が実行されている CPUアーキテクチャの名前を返します。

### version_compile_os {#version-compile-os}

-   スコープ: なし
-   デフォルト値: (文字列)
-   この変数は、TiDB が実行されている OS の名前を返します。

### wait_timeout {#wait-timeout}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[0, 31536000]`
-   単位: 秒
-   この変数は、ユーザー セッションのアイドル タイムアウトを制御します。ゼロ値は無制限を意味します。

### warning_count {#warning-count}

-   スコープ: セッション
-   デフォルト値: `0`
-   この読み取り専用変数は、以前に実行されたステートメントで発生した警告の数を示します。

### windowing_use_high_precision {#windowing-use-high-precision}

-   スコープ: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数を計算するときに高精度モードを使用するかどうかを制御します。
