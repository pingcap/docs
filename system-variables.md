---
title: System Variables
summary: Use system variables to optimize performance or alter running behavior.
---

# システム変数 {#system-variables}

TiDB システム変数は、設定が`SESSION`または`GLOBAL`スコープに適用されるという点で、MySQL と同様に動作します。

-   `SESSION`スコープでの変更は、現在のセッションにのみ影響します。
-   `GLOBAL`スコープの変更はすぐに適用されます。この変数も`SESSION`スコープの場合、すべてのセッション (セッションを含む) は現在のセッション値を引き続き使用します。
-   変更は[`SET`ステートメント](/sql-statements/sql-statement-set-variable.md)を使用して行われます。

```sql
# These two identical statements change a session variable
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# These two identical statements change a global variable
SET @@global.tidb_distsql_scan_concurrency = 10;
SET GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **注記：**
>
> いくつかの`GLOBAL`変数が TiDB クラスターに永続化されます。このドキュメントの一部の変数には`Persists to cluster`設定があり、 `Yes`または`No`に構成できます。
>
> -   `Persists to cluster: Yes`設定の変数の場合、グローバル変数が変更されると、システム変数キャッシュを更新するためにすべての TiDB サーバーに通知が送信されます。 TiDB サーバーを追加するか、既存の TiDB サーバーを再起動すると、永続化された構成値が自動的に使用されます。
> -   `Persists to cluster: No`設定の変数の場合、変更は接続しているローカル TiDB インスタンスにのみ適用されます。設定された値を保持するには、 `tidb.toml`ファイルで変数を指定する必要があります。
>
> さらに、TiDB は、読み取り可能および設定可能としていくつかの MySQL 変数を提供します。アプリケーションとコネクタの両方が MySQL 変数を読み取るのが一般的であるため、これは互換性のために必要です。たとえば、JDBC コネクタは、動作に依存していないにもかかわらず、クエリ キャッシュ設定の読み取りと設定の両方を行います。

> **注記：**
>
> 値を大きくすると、必ずしもパフォーマンスが向上するとは限りません。ほとんどの設定は各接続に適用されるため、ステートメントを実行する同時接続の数を考慮することも重要です。
>
> 安全な値を決定するときは、変数の単位を考慮してください。
>
> -   スレッドの場合、安全な値は通常、CPU コアの数までです。
> -   バイトの場合、安全な値は通常、システムメモリの量より小さくなります。
> -   時間については、単位が秒またはミリ秒であることに注意してください。
>
> 同じユニットを使用する変数は、同じリソースのセットをめぐって競合する可能性があります。

## 変数参照 {#variable-reference}

### allow_auto_random_explicit_insert <span class="version-mark">v4.0.3 の新機能</span> {#allow-auto-random-explicit-insert-span-class-version-mark-new-in-v4-0-3-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `INSERT`ステートメントで`AUTO_RANDOM`属性を持つ列の値を明示的に指定できるかどうかを決定します。

### 認証_ldap_sasl_auth_method_name <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `SCRAM-SHA-1`
-   可能な値: `SCRAM-SHA-1` 、 `SCRAM-SHA-256` 、および`GSSAPI` 。
-   LDAP SASL 認証の場合、この変数は認証方法名を指定します。

### Authentication_ldap_sasl_bind_base_dn <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は検索ツリー内の検索範囲を制限します。ユーザーが`AS ...`句なしで作成された場合、TiDB はユーザー名に従って LDAPサーバー内の`dn`自動的に検索します。

### Authentication_ldap_sasl_bind_root_dn <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は LDAPサーバーにログインしてユーザーを検索するために使用される`dn`を指定します。

### Authentication_ldap_sasl_bind_root_pwd <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用するパスワードを指定します。

### 認証_ldap_sasl_ca_path <span class="version-mark">v7.1.0の新機能</span> {#authentication-ldap-sasl-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は StartTLS 接続の認証局ファイルの絶対パスを指定します。

### Authentication_ldap_sasl_init_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP SASL 認証の場合、この変数は、接続プール内の LDAPサーバーへの最初の接続を指定します。

### Authentication_ldap_sasl_max_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP SASL 認証の場合、この変数は、LDAPサーバーへの接続プール内の最大接続数を指定します。

### 認証_ldap_sasl_server_host <span class="version-mark">v7.1.0の新機能</span> {#authentication-ldap-sasl-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は LDAPサーバーのホスト名または IP アドレスを指定します。

### 認証_ldap_sasl_server_port <span class="version-mark">v7.1.0の新機能</span> {#authentication-ldap-sasl-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### 認証_ldap_sasl_tls <span class="version-mark">v7.1.0の新機能</span> {#authentication-ldap-sasl-tls-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP SASL 認証の場合、この変数は、プラグインによる LDAPサーバーへの接続が StartTLS で保護されるかどうかを制御します。

### 認証_ldap_simple_auth_method_name <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `SIMPLE`
-   可能な値: `SIMPLE` 。
-   LDAP 簡易認証の場合、この変数は認証方法名を指定します。サポートされている値は`SIMPLE`のみです。

### Authentication_ldap_simple_bind_base_dn <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は検索ツリー内の検索範囲を制限します。ユーザーが`AS ...`句なしで作成された場合、TiDB はユーザー名に従って LDAPサーバー内の`dn`自動的に検索します。

### Authentication_ldap_simple_bind_root_dn <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は LDAPサーバーにログインしてユーザーを検索するために使用される`dn`を指定します。

### Authentication_ldap_simple_bind_root_pwd <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用するパスワードを指定します。

### 認証_ldap_simple_ca_path <span class="version-mark">v7.1.0の新機能</span> {#authentication-ldap-simple-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は StartTLS 接続の認証局ファイルの絶対パスを指定します。

### Authentication_ldap_simple_init_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP 簡易認証の場合、この変数は、接続プール内の LDAPサーバーへの最初の接続を指定します。

### Authentication_ldap_simple_max_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP 簡易認証の場合、この変数は、LDAPサーバーへの接続プール内の最大接続数を指定します。

### 認証_ldap_simple_server_host <span class="version-mark">v7.1.0の新機能</span> {#authentication-ldap-simple-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は LDAPサーバーのホスト名または IP アドレスを指定します。

### 認証_ldap_simple_server_port <span class="version-mark">v7.1.0の新機能</span> {#authentication-ldap-simple-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### 認証_ldap_simple_tls <span class="version-mark">v7.1.0の新機能</span> {#authentication-ldap-simple-tls-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP 簡易認証の場合、この変数は、プラグインによる LDAPサーバーへの接続を StartTLS で保護するかどうかを制御します。

### auto_increment_increment {#auto-increment-increment}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てられる`AUTO_INCREMENT`値のステップ サイズを制御します。 `auto_increment_offset`と組み合わせて使用​​されることが多いです。

### auto_increment_offset {#auto-increment-offset}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てられる`AUTO_INCREMENT`値の初期オフセットを制御します。この設定は、多くの場合、 `auto_increment_increment`と組み合わせて使用​​されます。例えば：

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

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   明示的なトランザクションにないときにステートメントを自動的にコミットするかどうかを制御します。詳細については[トランザクション概要](/transaction-overview.md#autocommit)参照してください。

### block_encryption_mode {#block-encryption-mode}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `aes-128-ecb`
-   値のオプション: `aes-128-ecb` 、 `aes-192-ecb` 、 `aes-256-ecb` 、 `aes-128-cbc` 、 `aes-192-cbc` 、 `aes-256-cbc` 、 `aes-128-ofb` 、 `aes-192-ofb` 、 `aes-256-ofb` 、 `aes-128-cfb` 、 `aes-192-cfb` 、 `aes-256-cfb`
-   この変数は、組み込み関数`AES_ENCRYPT()`および`AES_DECRYPT()`の暗号化モードを設定します。

### キャラクターセットクライアント {#character-set-client}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `utf8mb4`
-   クライアントから送信されるデータの文字セット。 TiDB での文字セットと照合順序の使用の詳細については、 [文字セットと照合順序](/character-set-and-collation.md)を参照してください。必要に応じて文字セットを変更するには[`SET NAMES`](/sql-statements/sql-statement-set-names.md)を使用することをお勧めします。

### 文字セット接続 {#character-set-connection}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `utf8mb4`
-   指定された文字セットを持たない文字列リテラルの文字セット。

### キャラクターセットデータベース {#character-set-database}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `utf8mb4`
-   この変数は、使用されているデフォルトのデータベースの文字セットを示します。**この変数を設定することはお勧めできません**。新しいデフォルト データベースが選択されると、サーバーは変数値を変更します。

### 文字セットの結果 {#character-set-results}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `utf8mb4`
-   データがクライアントに送信されるときに使用される文字セット。

### キャラクターセットサーバー {#character-set-server}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `utf8mb4`
-   サーバーのデフォルトの文字セット。

### 照合接続 {#collation-connection}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `utf8mb4_bin`
-   この変数は、現在の接続で使用される照合順序を示します。これは MySQL 変数`collation_connection`と一致します。

### 照合データベース {#collation-database}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `utf8mb4_bin`
-   この変数は、使用中のデータベースのデフォルトの照合順序を示します。**この変数を設定することはお勧めできません**。新しいデータベースが選択されると、TiDB はこの変数値を変更します。

### 照合サーバー {#collation-server}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `utf8mb4_bin`
-   データベースの作成時に使用されるデフォルトの照合順序。

### cte_max_recursion_ Depth {#cte-max-recursion-depth}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[0, 4294967295]`
-   共通テーブル式の最大再帰の深さを制御します。

### データディレクトリ {#datadir}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)ではサポートされていません。

<CustomContent platform="tidb">

-   範囲: なし
-   デフォルト値:コンポーネントとデプロイメント方法によって異なります。
    -   `/tmp/tidb` : [`--store`](/command-line-flags-for-tidb-configuration.md#--store)に`"unistore"`設定した場合、または`--store`を設定しなかった場合。
    -   `${pd-ip}:${pd-port}` : TiKV を使用する場合。これは、 TiUPおよびTiDB Operator for Kubernetes デプロイメントのデフォルトのstorageエンジンです。
-   この変数は、データが保存される場所を示します。この場所はローカル パス`/tmp/tidb`にすることも、データが TiKV に保存されている場合は PDサーバーを指すこともできます。 `${pd-ip}:${pd-port}`の形式の値は、起動時に TiDB が接続する PDサーバーを示します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   デフォルト値:コンポーネントとデプロイメント方法によって異なります。
    -   `/tmp/tidb` : [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store)に`"unistore"`設定した場合、または`--store`を設定しなかった場合。
    -   `${pd-ip}:${pd-port}` : TiKV を使用する場合。これは、 TiUPおよびTiDB Operator for Kubernetes デプロイメントのデフォルトのstorageエンジンです。
-   この変数は、データが保存される場所を示します。この場所はローカル パス`/tmp/tidb`にすることも、データが TiKV に保存されている場合は PDサーバーを指すこともできます。 `${pd-ip}:${pd-port}`の形式の値は、起動時に TiDB が接続する PDサーバーを示します。

</CustomContent>

### ddl_slow_threshold {#ddl-slow-threshold}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   実行時間がしきい値を超えた DDL 操作をログに記録します。

### デフォルト認証プラグイン {#default-authentication-plugin}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `mysql_native_password`
-   可能な値: `mysql_native_password` 、 `caching_sha2_password` 、 `tidb_sm3_password` 、 `tidb_auth_token` 、 `authentication_ldap_sasl` 、および`authentication_ldap_simple` 。
-   `tidb_auth_token`認証方法は、 TiDB Cloudの内部操作にのみ使用されます。変数をこの値に設定し**ないでください**。
-   この変数は、サーバーとクライアントの接続が確立されているときにサーバーが通知する認証方法を設定します。
-   `tidb_sm3_password`方法を使用して認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)を使用して TiDB に接続できます。

<CustomContent platform="tidb">

この変数のその他の可能な値については、 [認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status)を参照してください。

</CustomContent>

### default_password_lifetime <span class="version-mark">v6.5.0 の新機能</span> {#default-password-lifetime-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 65535]`
-   パスワードの自動有効期限のグローバル ポリシーを設定します。デフォルト値`0`は、パスワードの有効期限が切れないことを示します。このシステム変数が正の整数`N`に設定されている場合、パスワードの有効期間は`N`日であり、 `N`日以内にパスワードを変更する必要があることを意味します。

### デフォルト_週_形式 {#default-week-format}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 7]`
-   `WEEK()`関数で使用される週の形式を設定します。

### connect_on_expired_pa​​ssword <span class="version-mark">v6.5.0 の新機能</span> {#disconnect-on-expired-password-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は読み取り専用です。パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを示します。この変数が`ON`に設定されている場合、パスワードの有効期限が切れるとクライアント接続は切断されます。変数が`OFF`に設定されている場合、クライアント接続は「サンドボックス モード」に制限され、ユーザーはパスワード リセット操作のみを実行できます。

<CustomContent platform="tidb">

-   期限切れのパスワードに対するクライアント接続の動作を変更する必要がある場合は、構成ファイル内の[`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)構成項目を変更します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   期限切れのパスワードに対するクライアント接続のデフォルトの動作を変更する必要がある場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

### エラー数 {#error-count}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   メッセージを生成した最後のステートメントの結果発生したエラーの数を示す読み取り専用変数。

### 外部キーチェック {#foreign-key-checks}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: v6.6.0 より前のデフォルト値は`OFF`です。 v6.6.0 以降、デフォルト値は`ON`です。
-   この変数は、外部キー制約チェックを有効にするかどうかを制御します。

### group_concat_max_len {#group-concat-max-len}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[4, 18446744073709551615]`
-   `GROUP_CONCAT()`関数内の項目の最大バッファ サイズ。

### have_openssl {#have-openssl}

-   範囲: なし
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQL 互換性のための読み取り専用変数。サーバーで TLS が有効になっている場合、サーバーによって`YES`に設定されます。

### have_ssl {#have-ssl}

-   範囲: なし
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQL 互換性のための読み取り専用変数。サーバーで TLS が有効になっている場合、サーバーによって`YES`に設定されます。

### ホスト名 {#hostname}

-   範囲: なし
-   デフォルト値: (システムのホスト名)
-   読み取り専用変数としての TiDBサーバーのホスト名。

### ID <span class="version-mark">v5.3.0 の新機能</span> {#identity-span-class-version-mark-new-in-v5-3-0-span}

この変数は[`last_insert_id`](#last_insert_id)のエイリアスです。

### init_connect {#init-connect}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: &quot;&quot;
-   `init_connect`機能により、TiDBサーバーに初めて接続したときに SQL ステートメントを自動的に実行できます。 `CONNECTION_ADMIN`または`SUPER`権限を持っている場合、この`init_connect`ステートメントは実行されません。 `init_connect`ステートメントの結果がエラーになると、ユーザー接続は終了します。

### innodb_lock_wait_timeout {#innodb-lock-wait-timeout}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `50`
-   範囲: `[1, 3600]`
-   単位: 秒
-   悲観的トランザクションのロック待機タイムアウト (デフォルト)。

### インタラクティブタイムアウト {#interactive-timeout}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[1, 31536000]`
-   単位: 秒
-   この変数は、対話型ユーザー セッションのアイドル タイムアウトを表します。インタラクティブ ユーザー セッションとは、 `CLIENT_INTERACTIVE`オプションを使用して[`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API を呼び出すことによって確立されるセッション (たとえば、MySQL Shell と MySQL Client) を指します。この変数は MySQL と完全な互換性があります。

### last_insert_id {#last-insert-id}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、挿入ステートメントによって生成された最後の`AUTO_INCREMENT`または`AUTO_RANDOM`値を返します。
-   値`last_insert_id`は、関数`LAST_INSERT_ID()`によって返される値と同じです。

### last_plan_from_binding <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-binding-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、前のステートメントで使用された実行計画が[計画バインディング](/sql-plan-management.md)影響を受けたかどうかを示すために使用されます。

### last_plan_from_cache <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-cache-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、前の`execute`ステートメントで使用された実行プランがプラン キャッシュから直接取得されたかどうかを示すために使用されます。

### last_sql_use_alloc <span class="version-mark">v6.4.0 の新機能</span> {#last-sql-use-alloc-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション
-   デフォルト値: `OFF`
-   この変数は読み取り専用です。これは、前のステートメントがキャッシュされたチャンク オブジェクトを使用しているかどうか (チャンク割り当て) を示すために使用されます。

### ライセンス {#license}

-   範囲: なし
-   デフォルト値: `Apache License 2.0`
-   この変数は、TiDBサーバーインストールのライセンスを示します。

### ログビン {#log-bin}

-   範囲: なし
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [TiDBBinlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview)が使用されるかどうかを示します。

### max_allowed_pa​​cket <span class="version-mark">v6.1.0 の新機能</span> {#max-allowed-packet-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `67108864`
-   範囲: `[1024, 1073741824]`
-   値は 1024 の整数倍である必要があります。値が 1024 で割り切れない場合は、警告が表示され、値は切り捨てられます。たとえば、値が 1025 に設定されている場合、TiDB の実際の値は 1024 になります。
-   サーバーとクライアントが 1 回のパケット送信で許可する最大パケット サイズ。
-   この変数は MySQL と互換性があります。

### パスワード_履歴<span class="version-mark">v6.5.0 の新機能</span> {#password-history-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、パスワードの変更回数に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、パスワード変更の回数に基づいてパスワード再利用ポリシーを無効にすることを意味します。この変数が正の整数`N`に設定されている場合、最後の`N`パスワードの再利用は許可されません。

### mpp_exchange_compression_mode <span class="version-mark">v6.6.0 の新機能</span> {#mpp-exchange-compression-mode-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `UNSPECIFIED`
-   値のオプション: `NONE` 、 `FAST` 、 `HIGH_COMPRESSION` 、 `UNSPECIFIED`
-   この変数は、MPP Exchange オペレーターのデータ圧縮モードを指定するために使用されます。この変数は、TiDB がバージョン番号`1`の MPP 実行プランを選択したときに有効になります。変数値の意味は次のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。 TiDB は圧縮モードを自動的に選択します。現在、TiDB は自動的に`FAST`モードを選択します。
    -   `NONE` : データ圧縮は使用されません。
    -   `FAST` : 高速モード。全体的なパフォーマンスは良好で、圧縮率は`HIGH_COMPRESSION`未満です。
    -   `HIGH_COMPRESSION` : 高圧縮率モード。

### mpp_version <span class="version-mark">v6.6.0 の新機能</span> {#mpp-version-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `UNSPECIFIED`
-   値のオプション: `UNSPECIFIED` 、 `0` 、 `1`
-   この変数は、MPP 実行プランのさまざまなバージョンを指定するために使用されます。バージョンが指定されると、TiDB は MPP 実行プランの指定されたバージョンを選択します。変数値の意味は次のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。 TiDB は最新バージョン`1`を自動的に選択します。
    -   `0` : すべての TiDB クラスター バージョンと互換性があります。 MPP バージョンが`0`より大きい機能は、このモードでは有効になりません。
    -   `1` : v6.6.0 の新機能。 TiFlashでの圧縮によるデータ交換を有効にするために使用されます。詳細は[MPP バージョンと交換データ圧縮](/explain-mpp.md#mpp-version-and-exchange-data-compression)を参照してください。

### パスワード_再使用_間隔<span class="version-mark">v6.5.0 の新機能</span> {#password-reuse-interval-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、TiDB が経過時間に基づいてパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、経過時間に基づいてパスワード再利用ポリシーを無効にすることを意味します。この変数が正の整数`N`に設定されている場合、過去`N`日間に使用されたパスワードの再利用は許可されません。

### 最大接続数 {#max-connections}

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   単一の TiDB インスタンスに許可される同時接続の最大数。この変数はリソース制御に使用できます。
-   デフォルト値`0`は制限がないことを意味します。この変数の値が`0`より大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新しい接続を拒否します。

### 最大実行時間 {#max-execution-time}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   ステートメントの最大実行時間。デフォルト値は無制限 (ゼロ) です。

> **注記：**
>
> 現在、 `max_execution_time`システム変数は読み取り専用 SQL ステートメントの最大実行時間を制御するだけです。タイムアウト値の精度は約 100 ミリ秒です。これは、ステートメントが指定どおりに正確なミリ秒で終了しない可能性があることを意味します。

<CustomContent platform="tidb">

[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)ヒントを含む SQL ステートメントの場合、このステートメントの最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、説明したように SQL バインディングでも使用できます[SQL FAQ内](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)ヒントを含む SQL ステートメントの場合、このステートメントの最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、説明したように SQL バインディングでも使用できます[SQL FAQ内](https://docs.pingcap.com/tidb/stable/sql-faq) 。

</CustomContent>

### max_prepared_stmt_count {#max-prepared-stmt-count}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 1048576]`
-   現在の TiDB インスタンス内の[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントの最大数を指定します。
-   値`-1`は、現在の TiDB インスタンス内の`PREPARE`のステートメントの最大数に制限がないことを意味します。
-   変数に上限`1048576`を超える値を設定すると、代わりに`1048576`が使用されます。

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

### プラグイン_ディレクトリ {#plugin-dir}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)ではサポートされていません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: &quot;&quot;
-   コマンドライン フラグで指定されたプラグインをロードするディレクトリを示します。

### プラグイン_ロード {#plugin-load}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)ではサポートされていません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: &quot;&quot;
-   TiDB の起動時にロードするプラグインを示します。これらのプラグインは、コマンドライン フラグで指定し、カンマで区切ります。

### ポート {#port}

-   範囲: なし
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 65535]`
-   `tidb-server`が MySQL プロトコルを話すときにリッスンするポート。

### ランドシード1 {#rand-seed1}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL 関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作は MySQL と互換性があります。

### ランドシード2 {#rand-seed2}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL 関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作は MySQL と互換性があります。

### require_secure_transport <span class="version-mark">v6.1.0 の新機能</span> {#require-secure-transport-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> 現在、この変数は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated)ではサポートされていません。 TiDB 専用クラスターではこの変数を有効にし**ない**でください。そうしないと、SQL クライアント接続エラーが発生する可能性があります。この制限は一時的な制御手段であり、将来のリリースで解決される予定です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) : TiDB セルフホストの場合は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合は`OFF` 、 `ON`

<CustomContent platform="tidb">

-   この変数により、TiDB へのすべての接続がローカル ソケット上か TLS を使用するようになります。詳細については[TiDB クライアントとサーバーの間で TLS を有効にする](/enable-tls-between-clients-and-servers.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数により、TiDB へのすべての接続がローカル ソケット上か TLS を使用するようになります。

</CustomContent>

-   この変数を`ON`に設定するには、TLS が有効になっているセッションから TiDB に接続する必要があります。これは、TLS が正しく構成されていない場合のロックアウト シナリオを防ぐのに役立ちます。
-   この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。

### Skip_name_resolve <span class="version-mark">v5.2.0 の新機能</span> {#skip-name-resolve-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `tidb-server`インスタンスが接続ハンドシェイクの一部としてホスト名を解決するかどうかを制御します。
-   DNS が信頼できない場合は、このオプションを有効にしてネットワーク パフォーマンスを向上させることができます。

> **注記：**
>
> `skip_name_resolve=ON`の場合、アイデンティティにホスト名を持つユーザーはサーバーにログインできなくなります。例えば：
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> この例では、 `apphost` IP アドレスまたはワイルドカード ( `%` ) に置き換えることをお勧めします。

### ソケット {#socket}

-   範囲: なし
-   デフォルト値: &quot;&quot;
-   `tidb-server`が MySQL プロトコルを話すときにリッスンしているローカルの UNIX ソケット ファイル。

### sql_log_bin {#sql-log-bin}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   変更を[TiDBBinlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview)に書き込むかどうかを示します。

> **注記：**
>
> TiDB の将来のバージョンでは、これをセッション変数としてのみ設定できる可能性があるため、グローバル変数として`sql_log_bin`を設定することはお勧めできません。

### SQLモード {#sql-mode}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
-   この変数は、多くの MySQL 互換性動作を制御します。詳細については[SQLモード](/sql-mode.md)参照してください。

### sql_require_primary_key <span class="version-mark">v6.3.0 の新機能</span> {#sql-require-primary-key-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、テーブルに主キーがあるという要件を強制するかどうかを制御します。この変数を有効にした後、主キーなしでテーブルを作成または変更しようとすると、エラーが発生します。
-   この機能は、MySQL 8.0 の同様の名前の[`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key)に基づいています。
-   TiCDC を使用する場合は、この変数を有効にすることを強くお勧めします。これは、変更を MySQL シンクにレプリケートするには、テーブルに主キーが必要であるためです。

### sql_select_limit <span class="version-mark">v4.0.2 の新機能</span> {#sql-select-limit-span-class-version-mark-new-in-v4-0-2-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `18446744073709551615`
-   範囲: `[0, 18446744073709551615]`
-   単位: 行
-   `SELECT`ステートメントによって返される行の最大数。

### ssl_ca {#ssl-ca}

<CustomContent platform="tidb">

-   範囲: なし
-   デフォルト値: &quot;&quot;
-   認証局ファイルの場所 (存在する場合)。この変数の値は、TiDB 構成項目[`ssl-ca`](/tidb-configuration-file.md#ssl-ca)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   デフォルト値: &quot;&quot;
-   認証局ファイルの場所 (存在する場合)。この変数の値は、TiDB 構成項目[`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca)によって定義されます。

</CustomContent>

### ssl_cert {#ssl-cert}

<CustomContent platform="tidb">

-   範囲: なし
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される証明書ファイル (ファイルがある場合) の場所。この変数の値は、TiDB 構成項目[`ssl-cert`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される証明書ファイル (ファイルがある場合) の場所。この変数の値は、TiDB 構成項目[`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert)によって定義されます。

</CustomContent>

### ssl_key {#ssl-key}

<CustomContent platform="tidb">

-   範囲: なし
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される秘密キー ファイル (存在する場合) の場所。この変数の値は、TiDB 構成項目[`ssl-key`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される秘密キー ファイル (存在する場合) の場所。この変数の値は、TiDB 構成項目[`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key)によって定義されます。

</CustomContent>

### システムタイムゾーン {#system-time-zone}

-   範囲: なし
-   デフォルト値：（システムに依存）
-   この変数は、TiDB が最初にブートストラップされたときのシステム タイム ゾーンを示します。 [`time_zone`](#time_zone)も参照してください。

### tidb_adaptive_closest_read_threshold <span class="version-mark">v6.3.0 の新機能</span> {#tidb-adaptive-closest-read-threshold-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `4096`
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、 [`tidb_replica_read`](#tidb_replica_read-new-in-v40)が`closest-adaptive`に設定されている場合に、TiDBサーバーがTiDBサーバーと同じアベイラビリティーゾーン内のレプリカに読み取りリクエストを送信することを優先するしきい値を制御するために使用されます。推定結果がこのしきい値以上の場合、TiDB は同じアベイラビリティーゾーン内のレプリカに読み取りリクエストを送信することを優先します。それ以外の場合、TiDB は読み取りリクエストをリーダー レプリカに送信します。

### tidb_allow_batch_cop <span class="version-mark">v4.0 の新機能</span> {#tidb-allow-batch-cop-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   この変数は、TiDB がコプロセッサ リクエストをTiFlashに送信する方法を制御するために使用されます。次の値があります。

    -   `0` : リクエストをバッチで送信しない
    -   `1` :集計および結合リクエストはバッチで送信されます
    -   `2` : すべてのコプロセッサ要求はバッチで送信されます

### tidb_allow_fallback_to_tikv <span class="version-mark">v5.0 の新機能</span> {#tidb-allow-fallback-to-tikv-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: &quot;&quot;
-   この変数は、TiKV にフォールバックする可能性のあるstorageエンジンのリストを指定するために使用されます。リスト内の指定されたstorageエンジンの障害により SQL ステートメントの実行が失敗した場合、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。この変数は「」または「tflash」に設定できます。この変数が「tiflash」に設定されている場合、 TiFlash がタイムアウト エラー (エラー コード: ErrTiFlashServerTimeout) を返した場合、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。

### tidb_allow_function_for_expression_index <span class="version-mark">v5.2.0 の新機能</span> {#tidb-allow-function-for-expression-index-span-class-version-mark-new-in-v5-2-0-span}

-   範囲: なし
-   `json_contains` `json_array_insert` `json_array_append` `json_array` `json_contains_path` `json_depth` `json_extract` `json_insert` `json_keys` `json_length` `json_merge_patch` `json_merge_preserve` `json_object` `json_pretty` `json_quote` `json_remove` `json_replace` `json_search` `json_set` `json_storage_size` `json_type` `json_unquote` `json_valid` `lower` `tidb_shard` `md5` `reverse` `upper` `vitess_hash`
-   この変数は、式インデックスの作成に使用できる関数を示すために使用されます。

### tidb_allow_mpp <span class="version-mark">v5.0 の新機能</span> {#tidb-allow-mpp-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   クエリを実行するためにTiFlashの MPP モードを使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF` 、MPP モードが使用されないことを意味します。
    -   `1`または`ON` 。オプティマイザがコスト推定に基づいて MPP モードを使用するかどうかを決定することを意味します (デフォルト)。

MPP は、 TiFlashエンジンによって提供される分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能、高スループットの SQL アルゴリズムを提供します。 MPP モードの選択については、 [MPP モードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_allow_remove_auto_inc <span class="version-mark">v2.1.18 および v3.0.4 の新機能</span> {#tidb-allow-remove-auto-inc-span-class-version-mark-new-in-v2-1-18-and-v3-0-4-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、列の`AUTO_INCREMENT`のプロパティを`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`ステートメントの実行によって削除できるかどうかを設定するために使用されます。デフォルトでは許可されていません。

### tidb_analyze_partition_concurrency {#tidb-analyze-partition-concurrency}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `1`
-   この変数は、TiDB がパーティションテーブルを分析するときのパーティションテーブルの統計の読み取りおよび書き込みの同時実行性を指​​定します。

### tidb_analyze_version <span class="version-mark">v5.1.0 の新機能</span> {#tidb-analyze-version-span-class-version-mark-new-in-v5-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   TiDB が統計を収集する方法を制御します。
    -   TiDB セルフホストの場合、v5.3.0 以降、この変数のデフォルト値は`1`から`2`に変更されます。
    -   TiDB Cloudの場合、v6.5.0 以降、この変数のデフォルト値は`1`から`2`に変更されます。
    -   クラスターが以前のバージョンからアップグレードされた場合、デフォルト値の`tidb_analyze_version`はアップグレード後も変更されません。
-   この変数の詳細については、 [統計入門](/statistics.md)を参照してください。

### tidb_auto_analyze_end_time {#tidb-auto-analyze-end-time}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、自動統計更新を UTC 時間の午前 1 時から午前 3 時の間のみ許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`を設定します。

### tidb_auto_analyze_partition_batch_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-auto-analyze-partition-batch-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `1`
-   範囲: `[1, 1024]`
-   この変数は、パーティションテーブルを分析するときに TiDB [自動的に分析します](/statistics.md#automatic-update)が実行するパーティションの数を指定します (つまり、パーティションテーブルに関する統計を自動的に収集します)。
-   この変数の値がパーティションの数より小さい場合、TiDB はパーティションテーブルのすべてのパーティションを複数のバッチで自動的に分析します。この変数の値がパーティション数以上の場合、TiDB はパーティションテーブルのすべてのパーティションを同時に分析します。
-   パーティションテーブルのパーティション数がこの変数値よりもはるかに大きく、自動分析に時間がかかる場合は、この変数の値を増やすことで時間の消費を減らすことができます。

### tidb_auto_analyze_ratio {#tidb-auto-analyze-ratio}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.5`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、TiDB がバックグラウンド スレッドで自動的に[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行してテーブル統計を更新するときのしきい値を設定するために使用されます。たとえば、値 0.5 は、テーブル内の行の 50% 以上が変更されたときに自動分析がトリガーされることを意味します。 `tidb_auto_analyze_start_time`と`tidb_auto_analyze_end_time`を指定すると、自動分析を 1 日の特定の時間帯にのみ実行するように制限できます。

> **注記：**
>
> この機能を使用するには、システム変数`tidb_enable_auto_analyze` `ON`に設定する必要があります。

### tidb_auto_analyze_start_time {#tidb-auto-analyze-start-time}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、自動統計更新を UTC 時間の午前 1 時から午前 3 時の間のみ許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`を設定します。

### tidb_auto_build_stats_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-auto-build-stats-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、統計の自動更新を実行する同時実行数を設定するために使用されます。

### tidb_backoff_lock_fast {#tidb-backoff-lock-fast}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 2147483647]`
-   この変数は、読み取りリクエストがロックに遭遇する`backoff`を設定するために使用されます。

### tidb_backoff_weight {#tidb-backoff-weight}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB `backoff`の最大時間、つまり内部ネットワークまたは他のコンポーネント(TiKV、PD) の障害が発生したときにリトライ要求を送信するための最大リトライ時間の重みを増やすために使用されます。この変数は最大再試行時間を調整するために使用でき、最小値は 1 です。

    たとえば、TiDB が PD から TSO を取得するための基本タイムアウトは 15 秒です。 `tidb_backoff_weight = 2`の場合、TSO 取得の最大タイムアウトは、*基本時間 * 2 = 30 秒*です。

    ネットワーク環境が劣悪な場合、この変数の値を適切に増やすと、タイムアウトによって引き起こされるアプリケーション側へのエラー報告を効果的に軽減できます。アプリケーション側でエラー情報をより迅速に受信したい場合は、この変数の値を最小限に抑えます。

### tidb_batch_commit {#tidb-batch-commit}

> **警告：**
>
> この変数を有効にすることはお勧めできませ**ん**。

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチコミット機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、トランザクションがいくつかのステートメントをグループ化することによって複数のトランザクションに分割され、非アトミックにコミットされる可能性がありますが、これはお勧めできません。

### tidb_batch_delete {#tidb-batch-delete}

> **警告：**
>
> この変数は非推奨のバッチ dml 機能に関連付けられており、データ破損を引き起こす可能性があります。したがって、batch-dml に対してこの変数を有効にすることはお勧めできません。代わりに[非トランザクション DML](/non-transactional-dml.md)を使用してください。

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチ dml 機能の一部であるバッチ削除機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `DELETE`のステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`有効にして`tidb_dml_batch_size`に正の値を設定する必要もありますが、これはお勧めできません。

### tidb_batch_insert {#tidb-batch-insert}

> **警告：**
>
> この変数は非推奨のバッチ dml 機能に関連付けられており、データ破損を引き起こす可能性があります。したがって、batch-dml に対してこの変数を有効にすることはお勧めできません。代わりに[非トランザクション DML](/non-transactional-dml.md)を使用してください。

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチ dml 機能の一部であるバッチ挿入機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `INSERT`のステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`有効にして`tidb_dml_batch_size`に正の値を設定する必要もありますが、これはお勧めできません。

### tidb_batch_pending_tiflash_count <span class="version-mark">v6.0 の新機能</span> {#tidb-batch-pending-tiflash-count-span-class-version-mark-new-in-v6-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 4294967295]`
-   TiFlashレプリカを追加するために`ALTER DATABASE SET TIFLASH REPLICA`を使用する場合に、許可される使用不可テーブルの最大数を指定します。使用できないテーブルの数がこの制限を超えると、操作が停止されるか、残りのテーブルに対するTiFlashレプリカの設定が非常に遅くなります。

### tidb_broadcast_join_threshold_count <span class="version-mark">v5.0 の新機能</span> {#tidb-broadcast-join-threshold-count-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `10240`
-   範囲: `[0, 9223372036854775807]`
-   単位: 行
-   結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを推定できません。この状況では、サイズは結果セット内の行数によって決まります。サブクエリ内の推定行数がこの変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   この変数は、 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)を有効にすると有効になりません。

### tidb_broadcast_join_threshold_size <span class="version-mark">v5.0 の新機能</span> {#tidb-broadcast-join-threshold-size-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `104857600` (100 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   テーブル サイズが変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   この変数は、 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)を有効にすると有効になりません。

### tidb_build_stats_concurrency {#tidb-build-stats-concurrency}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `ANALYZE`ステートメント実行の同時実行性を設定するために使用されます。
-   変数をより大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_capture_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-capture-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [ベースラインのキャプチャ](/sql-plan-management.md#baseline-capturing)機能を有効にするかどうかを制御するために使用されます。この機能はステートメントの概要に依存するため、ベースライン キャプチャを使用する前にステートメントの概要を有効にする必要があります。
-   この機能を有効にすると、ステートメントの概要内の履歴 SQL ステートメントが定期的に調べられ、少なくとも 2 回出現する SQL ステートメントに対してバインディングが自動的に作成されます。

### tidb_cdc_write_source <span class="version-mark">v6.5.0 の新機能</span> {#tidb-cdc-write-source-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション
-   クラスターを維持する: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数が 0 以外の値に設定されている場合、このセッションで書き込まれたデータは TiCDC によって書き込まれたものとみなされます。この変数は TiCDC によってのみ変更できます。いかなる場合でも、この変数を手動で変更しないでください。

### tidb_check_mb4_value_in_utf8 {#tidb-check-mb4-value-in-utf8}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `utf8`文字セットが[基本多言語面 (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane)の値のみを格納するように強制するために使用されます。 BMP の外に文字を保存するには、 `utf8mb4`文字セットを使用することをお勧めします。
-   `utf8`チェックがより緩和されていた以前のバージョンの TiDB からクラスターをアップグレードする場合は、このオプションを無効にする必要がある場合があります。詳細は[アップグレード後のよくある質問](https://docs.pingcap.com/tidb/stable/upgrade-faq)を参照してください。

### tidb_checksum_table_concurrency {#tidb-checksum-table-concurrency}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)ステートメントを実行する際のスキャン インデックスの同時実行性を設定するために使用されます。
-   変数をより大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_committer_concurrency <span class="version-mark">v6.1.0 の新機能</span> {#tidb-committer-concurrency-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `128`
-   範囲: `[1, 10000]`
-   単一トランザクションのコミットフェーズでのコミットの実行に関連するリクエストのゴルーチンの数。
-   コミットするトランザクションが大きすぎる場合、トランザクションをコミットするときのフロー制御キューの待ち時間が長すぎる可能性があります。この状況では、構成値を増やしてコミットを高速化できます。
-   この設定は以前は`tidb.toml`オプション ( `performance.committer-concurrency` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。

### tidb_config {#tidb-config}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: &quot;&quot;
-   この変数は読み取り専用です。現在の TiDBサーバーの構成情報を取得するために使用されます。

### tidb_constraint_check_in_place {#tidb-constraint-check-in-place}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は楽観的トランザクションにのみ適用されます。悲観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-new-in-v630)を使用します。
-   この変数が`OFF`に設定されている場合、一意のインデックス内の重複値のチェックは、トランザクションがコミットされるまで延期されます。これはパフォーマンスの向上に役立ちますが、一部のアプリケーションでは予期しない動作になる可能性があります。詳細は[制約](/constraints.md#optimistic-transactions)参照してください。

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

-   範囲: セッション
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: デフォルトでは、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)構成項目は`true`であるため、この変数のデフォルト値は`ON`です。 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)が`false`に設定されている場合、この変数のデフォルト値は`OFF`です。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`

</CustomContent>

-   この変数は、悲観的トランザクションにのみ適用されます。楽観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place)を使用します。
-   この変数が`OFF`に設定されている場合、TiDB は一意のインデックスの一意制約チェックを (インデックスへのロックを必要とするステートメントを次回実行するとき、またはトランザクションをコミットするときまで) 延期します。これはパフォーマンスの向上に役立ちますが、一部のアプリケーションでは予期しない動作になる可能性があります。詳細は[制約](/constraints.md#pessimistic-transactions)参照してください。
-   この変数を無効にすると、悲観的トランザクションで TiDB が`LazyUniquenessCheckFailure`エラーを返す可能性があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。
-   この変数が無効になっている場合、悲観的トランザクションで[`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)を使用することはできません。
-   この変数が無効になっている場合、悲観的トランザクションをコミットすると、 `Write conflict`または`Duplicate entry`エラーが返される可能性があります。このようなエラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    -   `tidb_constraint_check_in_place_pessimistic` ～ `OFF`を設定し、悲観的トランザクションを使用する場合:

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=OFF;
        create table t (i int key);
        insert into t values (1);
        begin pessimistic;
        insert into t values (1);
        ```

            Query OK, 1 row affected

        ```sql
        tidb> commit; -- Check only when a transaction is committed.
        ```

            ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'

    -   `tidb_constraint_check_in_place_pessimistic` ～ `ON`を設定し、悲観的トランザクションを使用する場合:

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

            ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'

### tidb_cost_model_version <span class="version-mark">v6.2.0 の新機能</span> {#tidb-cost-model-version-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> -   TiDB v6.5.0 以降、新しく作成されたクラスターはデフォルトでコスト モデル バージョン 2 を使用します。 TiDB バージョン v6.5.0 より前のバージョンから v6.5.0 以降にアップグレードしても、値`tidb_cost_model_version`は変わりません。
> -   コスト モデルのバージョンを切り替えると、クエリ プランが変更される可能性があります。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   値のオプション:
    -   `1` : TiDB v6.4.0 以前のバージョンでデフォルトで使用されるコスト モデル バージョン 1 を有効にします。
    -   `2` : [コストモデルバージョン2](/cost-model.md#cost-model-version-2)有効にします。これは TiDB v6.5.0 で一般提供されており、内部テストではバージョン 1 よりも正確です。
-   コスト モデルのバージョンは、オプティマイザーの計画決定に影響します。詳細については、 [コストモデル](/cost-model.md)を参照してください。

### tidb_current_ts {#tidb-current-ts}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は読み取り専用です。現在のトランザクションのタイムスタンプを取得するために使用されます。

### tidb_ddl_disk_quota <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-disk-quota-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `107374182400` (100 GiB)
-   範囲: `[107374182400, 1125899906842624]` ([100 GiB、1 PiB])
-   単位: バイト
-   この変数は、 [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630)が有効な場合にのみ有効になります。インデックス作成時のバックフィル中のローカルstorageの使用制限を設定します。

### tidb_ddl_enable_fast_reorg <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-enable-fast-reorg-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> -   [TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated)クラスターを使用している場合、この変数を使用してインデックス作成の速度を向上させるには、TiDB クラスターが AWS でホストされており、TiDB ノードのサイズが少なくとも 8 vCPU であることを確認してください。
> -   [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターの場合、この変数は読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックス作成のバックフィル速度を向上させるために`ADD INDEX`と`CREATE INDEX`の高速化を有効にするかどうかを制御します。この変数値を`ON`に設定すると、大量のデータを含むテーブルでのインデックス作成のパフォーマンスが向上します。
-   v7.1.0 以降、インデックス アクセラレーション操作はチェックポイントをサポートします。障害により TiDB 所有者ノードが再起動または変更された場合でも、TiDB は定期的に自動的に更新されるチェックポイントから進行状況を回復できます。
-   完了した`ADD INDEX`操作が高速化されているかどうかを確認するには、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)ステートメントを実行して`JOB_TYPE`列に`ingest`が表示されるかどうかを確認します。

<CustomContent platform="tidb">

> **警告：**
>
> 現在、PITR リカバリは、互換性を実現するために、ログ バックアップ中にインデックス アクセラレーションによって作成されたインデックスを追加の処理で処理します。詳細は[インデックス追加の高速化機能が PITR と互換性がないのはなぜですか?](/faq/backup-and-restore-faq.md#why-is-the-acceleration-of-adding-indexes-feature-incompatible-with-pitr)を参照してください。

> **注記：**
>
> -   インデックスの高速化には、書き込み可能で十分な空き領域がある[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)必要です。 `temp-dir`が使用できない場合、TiDB は非高速インデックス構築に戻ります。 `temp-dir` SSD ディスクに配置することをお勧めします。
>
> -   TiDB を v6.5.0 以降にアップグレードする前に、TiDB の[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)パスが SSD ディスクに正しくマウントされているかどうかを確認することをお勧めします。 TiDB を実行するオペレーティング システム ユーザーが、このディレクトリに対する読み取りおよび書き込み権限を持っていることを確認してください。そうしないと、DDL 操作で予期しない問題が発生する可能性があります。このパスは TiDB 構成アイテムであり、TiDB の再起動後に有効になります。したがって、アップグレード前にこの構成項目を設定すると、再度の再起動を回避できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> 現在、この機能は[単一の`ALTER TABLE`ステートメントで複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md)と完全には互換性がありません。インデックス アクセラレーションを使用して一意のインデックスを追加する場合は、同じステートメント内の他の列やインデックスを変更しないようにする必要があります。
>
> 現在、PITR リカバリは、互換性を実現するために、ログ バックアップ中にインデックス アクセラレーションによって作成されたインデックスを追加の処理で処理します。詳細は[インデックス追加の高速化機能が PITR と互換性がないのはなぜですか?](https://docs.pingcap.com/tidb/v7.0/backup-and-restore-faq#why-is-the-acceleration-of-adding-indexes-feature-incompatible-with-pitr)を参照してください。

</CustomContent>

### tidb_enable_dist_task <span class="version-mark">v7.1.0 の新機能</span> {#tidb-enable-dist-task-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> この機能はまだ実験的段階にあります。本番環境でこの機能を有効にすることはお勧めできません。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `OFF`
-   この変数は、 [TiDB バックエンド タスク分散実行フレームワーク](/tidb-distributed-execution-framework.md)を有効にするかどうかを制御するために使用されます。フレームワークが有効になると、DDL やインポートなどのバックエンド タスクがクラスター内の複数の TiDB ノードによって分散実行され、完了します。
-   TiDB v7.1.0 では、フレームワークはパーティション化されたテーブルの`ADD INDEX`ステートメントのみの分散実行をサポートします。
-   この変数の名前は`tidb_ddl_distribute_reorg`から変更されます。

### tidb_ddl_error_count_limit {#tidb-ddl-error-count-limit}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `512`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、DDL 操作が失敗した場合の再試行回数を設定するために使用されます。再試行回数がパラメータ値を超えると、間違った DDL 操作がキャンセルされます。

### tidb_ddl_flashback_concurrency <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-flashback-concurrency-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `64`
-   範囲: `[1, 256]`
-   この変数は[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)の同時実行性を制御します。

### tidb_ddl_reorg_batch_size {#tidb-ddl-reorg-batch-size}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `256`
-   範囲: `[32, 10240]`
-   単位: 行
-   この変数は、DDL 操作の`re-organize`フェーズ中にバッチ サイズを設定するために使用されます。たとえば、TiDB が`ADD INDEX`オペレーションを実行する場合、インデックス データは`tidb_ddl_reorg_worker_cnt` (数値) の同時ワーカーによってバックフィルされる必要があります。各ワーカーはインデックス データをバッチでバックフィルします。
    -   `ADD INDEX`操作中に`UPDATE`や`REPLACE`などの多くの更新操作が存在する場合、バッチ サイズが大きいほど、トランザクション競合が発生する可能性が高くなります。この場合、バッチ サイズをより小さい値に調整する必要があります。最小値は 32 です。
    -   トランザクションの競合が存在しない場合は、バッチ サイズを大きな値に設定できます (ワーカー数を考慮してください。参照については[オンライン ワークロードと`ADD INDEX`操作の対話テスト](https://docs.pingcap.com/tidb/stable/online-workloads-and-add-index-operations)を参照してください)。これにより、データのバックフィルの速度が向上しますが、TiKV への書き込み圧力も高くなります。

### tidb_ddl_reorg_priority {#tidb-ddl-reorg-priority}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション
-   タイプ: 列挙型
-   デフォルト値: `PRIORITY_LOW`
-   値のオプション: `PRIORITY_LOW` 、 `PRIORITY_NORMAL` 、 `PRIORITY_HIGH`
-   この変数は、 `re-organize`フェーズの`ADD INDEX`オペレーションを実行する優先順位を設定するために使用されます。
-   この変数の値は`PRIORITY_LOW` 、 `PRIORITY_NORMAL` 、または`PRIORITY_HIGH`に設定できます。

### tidb_ddl_reorg_worker_cnt {#tidb-ddl-reorg-worker-cnt}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `re-organize`フェーズでの DDL 操作の同時実行性を設定するために使用されます。

### tidb_default_string_match_selectivity <span class="version-mark">v6.2.0 の新機能</span> {#tidb-default-string-match-selectivity-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.8`
-   範囲: `[0, 1]`
-   この変数は、行数を見積もる際のフィルター条件における`like` 、 `rlike` 、および`regexp`関数のデフォルトの選択性を設定するために使用されます。この変数は、TopN がこれらの関数の推定に役立つようにするかどうかも制御します。
-   TiDB は統計を使用してフィルター条件の`like`を推定しようとします。ただし、 `like`複雑な文字列に一致する場合、または`rlike`または`regexp`を使用する場合、TiDB は統計を完全に活用できないことが多く、代わりにデフォルト値`0.8`選択率として設定されるため、推定が不正確になります。
-   この変数は、前述の動作を変更するために使用されます。変数が`0`以外の値に設定されている場合、選択率は`0.8`ではなく、指定された変数値になります。
-   変数が`0`に設定されている場合、TiDB は精度を向上させるために統計に TopN を使用して評価を試行し、前述の 3 つの関数を推定するときに統計の NULL 数を考慮します。前提条件は、 [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510)が`2`に設定されている場合に統計が収集されることです。このような評価は、パフォーマンスにわずかに影響を与える可能性があります。
-   変数が`0.8`以外の値に設定されている場合、TiDB はそれに応じて`not like` 、 `not rlike` 、および`not regexp`の推定を調整します。

### tidb_disable_txn_auto_retry {#tidb-disable-txn-auto-retry}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、明示的な楽観的トランザクションの自動再試行を無効にするかどうかを設定するために使用されます。デフォルト値の`ON` 、TiDB でトランザクションが自動的に再試行されず、 `COMMIT`ステートメントがアプリケーションレイヤーで処理する必要があるエラーを返す可能性があることを意味します。

    値を`OFF`に設定すると、TiDB がトランザクションを自動的に再試行し、 `COMMIT`ステートメントによるエラーが少なくなります。更新が失われる可能性があるため、この変更を行う場合は注意してください。

    この変数は、自動的にコミットされた暗黙的なトランザクションおよび TiDB で内部的に実行されたトランザクションには影響しません。これらのトランザクションの最大再試行回数は、値`tidb_retry_limit`によって決まります。

    詳細については、 [再試行の制限](/optimistic-transaction.md#limits-of-retry)を参照してください。

    <CustomContent platform="tidb">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は[`max_retry_count`](/tidb-configuration-file.md#max-retry-count)によって制御されます。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は 256 回です。

    </CustomContent>

### tidb_distsql_scan_concurrency {#tidb-distsql-scan-concurrency}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `15`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `scan`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオではより大きな値を使用し、OLTP シナリオではより小さな値を使用します。
-   OLAP シナリオの場合、最大値はすべての TiKV ノードの CPU コア数を超えてはなりません。
-   テーブルに多数のパーティションがある場合は、TiKV のメモリ不足 (OOM) を回避するために、変数値を適切に (スキャンするデータのサイズとスキャンの頻度によって決まります) 減らすことができます。

### tidb_dml_batch_size {#tidb-dml-batch-size}

> **警告：**
>
> この変数は非推奨のバッチ dml 機能に関連付けられており、データ破損を引き起こす可能性があります。したがって、batch-dml に対してこの変数を有効にすることはお勧めできません。代わりに[非トランザクション DML](/non-transactional-dml.md)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: 行
-   この値が`0`より大きい場合、TiDB は`INSERT`などのコミット ステートメントを小さなトランザクションにバッチ処理します。これによりメモリ使用量が削減され、一括変更によって`txn-total-size-limit`に到達することがなくなります。
-   値`0`のみがACID準拠を提供します。これを他の値に設定すると、TiDB のアトミック性と分離性の保証が失われます。
-   この変数を機能させるには、 `tidb_enable_batch_dml`と`tidb_batch_insert`と`tidb_batch_delete`の少なくとも 1 つを有効にする必要もあります。

> **注記：**
>
> v7.0.0 以降、 `tidb_dml_batch_size` [`LOAD DATA`ステートメント](/sql-statements/sql-statement-load-data.md)に対して有効になりません。

### tidb_enable_1pc <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-1pc-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、1 つのリージョンにのみ影響するトランザクションに対して 1 フェーズ コミット機能を有効にするかどうかを指定するために使用されます。よく使用される 2 フェーズ コミットと比較して、1 フェーズ コミットはトランザクション コミットのレイテンシーを大幅に短縮し、スループットを向上させることができます。

> **注記：**
>
> -   デフォルト値の`ON`新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   TiDB Binlogを有効にしている場合、この変数を有効にしてもパフォーマンスは向上しません。パフォーマンスを向上させるには、代わりに[TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)を使用することをお勧めします。
> -   このパラメータを有効にすることは、1 フェーズ コミットがトランザクション コミットのオプション モードになることを意味するだけです。実際、トランザクション コミットの最適なモードは TiDB によって決定されます。

### tidb_enable_analyze_snapshot <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-analyze-snapshot-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `ANALYZE`を実行するときに履歴データを読み取るか最新のデータを読み取るかを制御します。この変数が`ON`に設定されている場合、 `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ります。この変数が`OFF`に設定されている場合、 `ANALYZE`最新のデータを読み取ります。
-   v5.2 より前では、 `ANALYZE`最新のデータを読み取ります。 v5.2 から v6.1 では、 `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ります。

> **警告：**
>
> `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取る場合、履歴データがガベージ コレクションされるため、 `AUTO ANALYZE`の継続時間が長いと`GC life time is shorter than transaction duration`エラーが発生する可能性があります。

### tidb_enable_async_commit <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-async-commit-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、2 フェーズ トランザクション コミットの第 2 フェーズの非同期コミット機能を有効にしてバックグラウンドで非同期に実行するかどうかを制御します。この機能を有効にすると、トランザクションのコミットのレイテンシーを短縮できます。

> **注記：**
>
> -   デフォルト値の`ON`新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   TiDB Binlogを有効にしている場合、この変数を有効にしてもパフォーマンスは向上しません。パフォーマンスを向上させるには、代わりに[TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)を使用することをお勧めします。
> -   このパラメータを有効にすることは、非同期コミットがトランザクション コミットのオプション モードになることを意味するだけです。実際、トランザクション コミットの最適なモードは TiDB によって決定されます。

### tidb_enable_auto_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-auto-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB がバックグラウンド操作としてテーブル統計を自動的に更新するかどうかを決定します。
-   この設定は以前は`tidb.toml`オプション ( `performance.run-auto-analyze` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。

### tidb_enable_auto_increment_in_generated {#tidb-enable-auto-increment-in-generated}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、生成列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定するために使用されます。

### tidb_enable_batch_dml {#tidb-enable-batch-dml}

> **警告：**
>
> この変数は非推奨のバッチ dml 機能に関連付けられており、データ破損を引き起こす可能性があります。したがって、batch-dml に対してこの変数を有効にすることはお勧めできません。代わりに[非トランザクション DML](/non-transactional-dml.md)を使用してください。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチ dml 機能を有効にするかどうかを制御します。これを有効にすると、特定のステートメントが複数のトランザクションに分割される可能性がありますが、これは非アトミックであるため、注意して使用する必要があります。 Batch-DML を使用する場合は、操作しているデータに対して同時操作が行われていないことを確認する必要があります。これを機能させるには、 `tidb_batch_dml_size`に正の値を指定し、 `tidb_batch_insert`と`tidb_batch_delete`の少なくとも 1 つを有効にする必要もあります。

### tidb_enable_cascades_planner {#tidb-enable-cascades-planner}

> **警告：**
>
> 現在、カスケード プランナーは実験的機能です。本番環境で使用することはお勧めできません。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、カスケード プランナーを有効にするかどうかを制御するために使用されます。

### tidb_enable_chunk_rpc <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-chunk-rpc-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサーで`Chunk`データ エンコード形式を有効にするかどうかを制御するために使用されます。

### tidb_enable_clustered_index <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-clustered-index-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON` 、 `INT_ONLY`
-   この変数は、主キーをデフォルトで[クラスター化インデックス](/clustered-indexes.md)として作成するかどうかを制御するために使用されます。ここでの「デフォルト」とは、ステートメントでキーワード`CLUSTERED` / `NONCLUSTERED`が明示的に指定されていないことを意味します。サポートされている値は`OFF` 、 `ON` 、および`INT_ONLY`です。
    -   `OFF` 、主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
    -   `ON` 、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
    -   `INT_ONLY` 、動作が構成項目`alter-primary-key`によって制御されることを示します。 `alter-primary-key`を`true`に設定すると、デフォルトですべての主キーが非クラスター化インデックスとして作成されます。 `false`に設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

### tidb_enable_ddl <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-ddl-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON`
-   この変数は、対応する TiDB インスタンスが DDL 所有者になれるかどうかを制御します。現在の TiDB クラスターに TiDB インスタンスが 1 つしかない場合、そのインスタンスが DDL 所有者になるのを防ぐことはできません。つまり、それを`OFF`に設定することはできません。

### tidb_enable_collect_execution_info {#tidb-enable-collect-execution-info}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、各オペレータの実行情報をスロー クエリ ログに記録するかどうかを制御します。

### tidb_enable_column_tracking <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-column-tracking-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、 `PREDICATE COLUMNS`に関する統計の収集は実験的機能です。本番環境で使用することはお勧めできません。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB が`PREDICATE COLUMNS`を収集できるようにするかどうかを制御します。収集を有効にした後、無効にすると、以前に収集した`PREDICATE COLUMNS`の情報がクリアされます。詳細は[いくつかの列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)を参照してください。

### tidb_enable_enhanced_security {#tidb-enable-enhanced-security}

-   範囲: なし
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: `OFF`
-   この変数は、接続している TiDBサーバーでSecurity強化モード (SEM) が有効になっているかどうかを示します。その値を変更するには、TiDBサーバー構成ファイル内の値`enable-sem`を変更し、TiDBサーバーを再起動する必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`
-   この変数は読み取り専用です。 TiDB Cloudの場合、Security強化モード (SEM) がデフォルトで有効になっています。

</CustomContent>

-   SEM は、 [セキュリティ強化された Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux)のようなシステムの設計からインスピレーションを得ています。これにより、MySQL `SUPER`権限を持つユーザーの能力が低下し、代わりに`RESTRICTED`権限を付与する必要があります。これらのきめ細かい権限には次のものが含まれます。
    -   `RESTRICTED_TABLES_ADMIN` : `mysql`スキーマのシステム テーブルにデータを書き込み、 `information_schema`のテーブルの機密列を表示する機能。
    -   `RESTRICTED_STATUS_ADMIN` : コマンド内の機密変数を表示する機能`SHOW STATUS` 。
    -   `RESTRICTED_VARIABLES_ADMIN` : `SHOW [GLOBAL] VARIABLES`と`SET`の機密変数を表示および設定する機能。
    -   `RESTRICTED_USER_ADMIN` : 他のユーザーがユーザー アカウントを変更したり削除したりできないようにする機能。

### tidb_enable_exchange_partition {#tidb-enable-exchange-partition}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、デフォルトで`exchange partitions with tables`が有効になります。
-   この変数は v6.3.0 以降非推奨になりました。その値はデフォルト値`ON`に固定されます。つまり、デフォルトでは`exchange partitions with tables`が有効になります。

### tidb_enable_extended_stats {#tidb-enable-extended-stats}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB がオプティマイザーをガイドする拡張統計を収集できるかどうかを示します。詳細については[拡張統計の概要](/extended-statistics.md)参照してください。

### tidb_enable_external_ts_read <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-external-ts-read-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数が`ON`に設定されている場合、TiDB は[`tidb_external_ts`](#tidb_external_ts-new-in-v640)で指定されたタイムスタンプを持つデータを読み取ります。

### tidb_external_ts <span class="version-mark">v6.4.0 の新機能</span> {#tidb-external-ts-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-new-in-v640)を`ON`に設定すると、TiDB はこの変数で指定されたタイムスタンプを持つデータを読み取ります。

### tidb_enable_fast_analyze {#tidb-enable-fast-analyze}

> **警告：**
>
> 現在、 `Fast Analyze`は実験的機能です。本番環境で使用することはお勧めできません。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計`Fast Analyze`機能を有効にするかどうかを設定するために使用されます。
-   統計`Fast Analyze`機能が有効になっている場合、TiDB は統計として約 10,000 行のデータをランダムにサンプリングします。データが偏っていたり、データサイズが小さかったりすると、統計精度が低くなります。これにより、たとえば間違ったインデックスが選択されるなど、最適ではない実行計画が生じる可能性があります。通常の`Analyze`ステートメントの実行時間が許容できる場合は、 `Fast Analyze`機能を無効にすることをお勧めします。

### tidb_enable_foreign_key <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-foreign-key-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: v6.6.0 より前のデフォルト値は`OFF`です。 v6.6.0 以降、デフォルト値は`ON`です。
-   この変数は、 `FOREIGN KEY`機能を有効にするかどうかを制御します。

### tidb_enable_gc_aware_memory_track {#tidb-enable-gc-aware-memory-track}

> **警告：**
>
> この変数は、TiDB でデバッグするための内部変数です。将来のリリースでは削除される可能性があります。この変数は設定し**ないでください**。

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、GC 対応メモリトラックを有効にするかどうかを制御します。

### tidb_enable_non_prepared_plan_cache {#tidb-enable-non-prepared-plan-cache}

> **警告：**
>
> 準備されていない実行プラン キャッシュは実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。

### tidb_enable_non_prepared_plan_cache_for_dml <span class="version-mark">v7.1.0 の新機能</span> {#tidb-enable-non-prepared-plan-cache-for-dml-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> 準備されていない実行プラン キャッシュは実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF` 。
-   この変数は、DML ステートメントの[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。

### tidb_enable_gogc_tuner <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-gogc-tuner-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、GOGC チューナーを有効にするかどうかを制御します。

### tidb_enable_historyal_stats {#tidb-enable-historical-stats}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更されます。これは、履歴統計がデフォルトで有効になることを意味します。

### tidb_enable_historyal_stats_for_capture {#tidb-enable-historical-stats-for-capture}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CAPTURE`によって取得される情報にデフォルトで履歴統計が含まれるかどうかを制御します。デフォルト値`OFF` 、履歴統計がデフォルトで含まれないことを意味します。

### tidb_enable_index_merge <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-index-merge-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> -   TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードした後、実行計画の変更によるパフォーマンスの低下を防ぐために、この変数はデフォルトで無効になります。
>
> -   TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードした後、この変数はアップグレード前の設定のままになります。
>
> -   v5.4.0 以降、新しくデプロイされた TiDB クラスターでは、この変数はデフォルトで有効になっています。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックスのマージ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_index_merge_join {#tidb-enable-index-merge-join}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `IndexMergeJoin`演算子を有効にするかどうかを指定します。
-   この変数は、TiDB の内部操作にのみ使用されます。調整することは**お勧めしません**。そうしないと、データの正確性に影響が出る可能性があります。

### tidb_enable_legacy_instance_scope <span class="version-mark">v6.0.0 の新機能</span> {#tidb-enable-legacy-instance-scope-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数では、 `INSTANCE`スコープ付き変数を`SET SESSION`および`SET GLOBAL`構文を使用して設定できます。
-   このオプションは、TiDB の以前のバージョンとの互換性のためにデフォルトで有効になっています。

### tidb_enable_list_partition <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-list-partition-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `LIST (COLUMNS) TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。

### tidb_enable_local_txn {#tidb-enable-local-txn}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は未リリースの機能に使用されます。**変数の値は変更しないでください**。

### tidb_enable_metadata_lock <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-metadata-lock-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [メタデータロック](/metadata-lock.md)機能を有効にするかどうかを設定するために使用されます。この変数を設定するときは、クラスター内で実行中の DDL ステートメントがないことを確認する必要があることに注意してください。そうしないと、データが正しくないか、一貫性がなくなる可能性があります。

### tidb_enable_mutation_checker <span class="version-mark">v6.0.0 の新機能</span> {#tidb-enable-mutation-checker-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、DML ステートメントの実行中にデータとインデックス間の一貫性をチェックするために使用されるツールである TiDB ミューテーション チェッカーを有効にするかどうかを制御するために使用されます。チェッカーがステートメントに対してエラーを返した場合、TiDB はステートメントの実行をロールバックします。この変数を有効にすると、CPU 使用率がわずかに増加します。詳細については、 [データとインデックス間の不一致のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)を参照してください。
-   v6.0.0 以降のバージョンの新しいクラスターの場合、デフォルト値は`ON`です。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_enable_new_cost_interface <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-new-cost-interface-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB v6.2.0 では、以前のコスト モデルの実装がリファクタリングされています。この変数は、リファクタリングされたコスト モデルの実装を有効にするかどうかを制御します。
-   リファクタリングされたコスト モデルでは以前と同じコスト式が使用され、計画の決定は変更されないため、この変数はデフォルトで有効になっています。
-   クラスターが v6.1 から v6.2 にアップグレードされた場合、この変数は`OFF`のままになるため、手動で有効にすることをお勧めします。クラスターが v6.1 より前のバージョンからアップグレードされた場合、この変数はデフォルトで`ON`に設定されます。

### tidb_enable_new_only_full_group_by_check <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-new-only-full-group-by-check-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB が`ONLY_FULL_GROUP_BY`チェックを実行するときの動作を制御します。 `ONLY_FULL_GROUP_BY`の詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)を参照してください。 v6.1.0 では、TiDB はこのチェックをより厳密かつ正確に処理します。
-   バージョンのアップグレードによって生じる潜在的な互換性の問題を回避するために、v6.1.0 ではこの変数のデフォルト値は`OFF`です。

### tidb_enable_noop_functions <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-noop-functions-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `OFF`
-   可能な値: `OFF` 、 `ON` 、 `WARN`
-   デフォルトでは、まだ実装されていない機能の構文を使用しようとすると、TiDB はエラーを返します。変数値が`ON`に設定されている場合、TiDB はそのような使用できない機能のケースを黙って無視します。これは、SQL コードを変更できない場合に役立ちます。
-   `noop`関数を有効にすると、次の動作が制御されます。
    -   `LOCK IN SHARE MODE`の構文
    -   `SQL_CALC_FOUND_ROWS`の構文
    -   `START TRANSACTION READ ONLY`と`SET TRANSACTION READ ONLY`の構文
    -   `tx_read_only` 、 `transaction_read_only` 、 `offline_mode` 、 `super_read_only` 、 `read_only` 、および`sql_auto_is_null`システム変数
    -   `GROUP BY <expr> ASC|DESC`の構文

> **警告：**
>
> デフォルト値の`OFF`のみが安全であると考えられます。 `tidb_enable_noop_functions=1`を設定すると、TiDB がエラーを表示せずに特定の構文を無視できるようになるため、アプリケーションで予期しない動作が発生する可能性があります。たとえば、構文`START TRANSACTION READ ONLY`は許可されますが、トランザクションは読み取り/書き込みモードのままになります。

### tidb_enable_noop_variables <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-noop-variables-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ON`
-   変数値を`OFF`に設定すると、TiDB は次のように動作します。
    -   `SET`を使用して`noop`変数を設定すると、TiDB は`"setting *variable_name* has no effect in TiDB"`警告を返します。
    -   `SHOW [SESSION | GLOBAL] VARIABLES`の結果には`noop`変数は含まれません。
    -   `SELECT`を使用して`noop`変数を読み取ると、TiDB は`"variable *variable_name* has no effect in TiDB"`警告を返します。
-   TiDB インスタンスが`noop`変数を設定および読み取りしたかどうかを確認するには、 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;`ステートメントを使用できます。

### tidb_enable_null_aware_anti_join <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-null-aware-anti-join-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: v7.0.0 より前のデフォルト値は`OFF`です。 v7.0.0 以降、デフォルト値は`ON`です。
-   タイプ: ブール値
-   この変数は、特別な集合演算子`NOT IN`および`!= ALL`によって導かれるサブクエリによって ANTI JOIN が生成されるときに、TiDB が Null Aware Hash Join を適用するかどうかを制御します。
-   以前のバージョンから v7.0.0 以降のクラスターにアップグレードすると、この機能は自動的に有効になります。つまり、この変数は`ON`に設定されます。

### tidb_enable_outer_join_reorder <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-outer-join-reorder-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   v6.1.0 以降、TiDB の[結合したテーブルの再配置](/join-reorder.md)アルゴリズムは、Outer Join をサポートします。この変数は、TiDB が Outer Join に対する Join Reorder のサポートを有効にするかどうかを制御します。
-   クラスターが TiDB の以前のバージョンからアップグレードされている場合は、次の点に注意してください。

    -   アップグレード前の TiDB バージョンが v6.1.0 より前の場合、アップグレード後のこの変数のデフォルト値は`ON`です。
    -   アップグレード前の TiDB バージョンが v6.1.0 以降の場合、アップグレード後の変数のデフォルト値はアップグレード前の値に従います。

### <code>tidb_enable_inl_join_inner_multi_pattern</code> <span class="version-mark">v7.0.0 の新機能</span> {#code-tidb-enable-inl-join-inner-multi-pattern-code-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、内部テーブルに`Selection`または`Projection`の演算子がある場合にインデックス結合をサポートするかどうかを制御します。デフォルト値`OFF` 、このシナリオではインデックス結合がサポートされていないことを意味します。

### tidb_enable_ordered_result_mode {#tidb-enable-ordered-result-mode}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   最終出力結果を自動的にソートするかどうかを指定します。
-   たとえば、この変数を有効にすると、TiDB は`SELECT a, MAX(b) FROM t GROUP BY a`を`SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`として処理します。

### tidb_enable_paging <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-paging-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサ要求の送信にページング方式を使用するかどうかを制御します。 TiDB バージョン [v5.4.0、v6.2.0) の場合、この変数は`IndexLookup`演算子にのみ有効です。 v6.2.0 以降では、この変数はグローバルに有効になります。 v6.4.0 以降、この変数のデフォルト値は`OFF`から`ON`に変更されます。
-   ユーザーシナリオ:

    -   すべての OLTP シナリオで、ページング方式を使用することをお勧めします。
    -   `IndexLookup`と`Limit`使用し、 `Limit` `IndexScan`にプッシュダウンできない読み取りクエリの場合、読み取りクエリのレイテンシーが長くなり、TiKV `Unified read pool CPU`の使用率が高くなる可能性があります。このような場合、 `Limit`演算子は少量のデータ セットのみを必要とするため、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)を`ON`に設定すると、TiDB が処理するデータが減り、クエリのレイテンシーとリソースの消費が削減されます。
    -   [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)やフル テーブル スキャンを使用したデータ エクスポートなどのシナリオでは、ページングを有効にすることで TiDB プロセスのメモリ消費を効果的に削減できます。

> **注記：**
>
> TiFlashの代わりに TiKV がstorageエンジンとして使用される OLAP シナリオでは、ページングを有効にすると、場合によってはパフォーマンスの低下が発生する可能性があります。回帰が発生した場合は、この変数を使用してページングを無効にするか、 [`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-new-in-v620)および[`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-new-in-v630)変数を使用してページング サイズの行範囲を調整することを検討してください。

### tidb_enable_Parallel_apply <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-parallel-apply-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `Apply`オペレーターの同時実行を有効にするかどうかを制御します。同時実行の数は`tidb_executor_concurrency`変数によって制御されます。 `Apply`オペレーターは相関サブクエリを処理し、デフォルトでは同時実行性がないため、実行速度が遅くなります。この変数値を`1`に設定すると、同時実行性が向上し、実行速度が向上します。現在、 `Apply`の同時実行性はデフォルトで無効になっています。

### tidb_enable_pipelined_window_function {#tidb-enable-pipelined-window-function}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数にパイプライン実行アルゴリズムを使用するかどうかを指定します。

### tidb_enable_plan_cache_for_param_limit <span class="version-mark">v6.6.0 の新機能</span> {#tidb-enable-plan-cache-for-param-limit-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 プリペアドプランキャッシュ が`LIMIT`パラメータ ( `LIMIT ?` ) として変数を使用して実行プランをキャッシュするかどうかを制御します。デフォルト値は`ON`です。これは、 プリペアドプランキャッシュ がそのような実行計画のキャッシュをサポートすることを意味します。 プリペアドプランキャッシュ は、10000 を超える変数を含む実行プランのキャッシュをサポートしていないことに注意してください。

### tidb_enable_plan_cache_for_subquery <span class="version-mark">v7.0.0 の新機能</span> {#tidb-enable-plan-cache-for-subquery-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 プリペアドプランキャッシュ がサブクエリを含むクエリをキャッシュするかどうかを制御します。

### tidb_enable_plan_replayer_capture {#tidb-enable-plan-replayer-capture}

<CustomContent platform="tidb-cloud">

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CAPTURE`機能を有効にするかどうかを制御します。デフォルト値`OFF` `PLAN REPLAYER CAPTURE`機能を無効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`PLAN REPLAYER CAPTURE`機能を計画する](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)を有効にするかどうかを制御します。デフォルト値`ON` `PLAN REPLAYER CAPTURE`機能を有効にすることを意味します。

</CustomContent>

### tidb_enable_plan_replayer_continuous_capture <span class="version-mark">v7.0.0 の新機能</span> {#tidb-enable-plan-replayer-continuous-capture-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb-cloud">

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CONTINUOUS CAPTURE`機能を有効にするかどうかを制御します。デフォルト値`OFF` 、この機能を無効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [`PLAN REPLAYER CONTINUOUS CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)を有効にするかどうかを制御します。デフォルト値`OFF` 、この機能を無効にすることを意味します。

</CustomContent>

### tidb_enable_prepared_plan_cache <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-prepared-plan-cache-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   [プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)を有効にするかどうかを決定します。有効にすると、 `Prepare`と`Execute`の実行計画がキャッシュされるため、後続の実行では実行計画の最適化がスキップされ、パフォーマンスが向上します。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-prepared-plan-cache-memory-monitor-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュにキャッシュされた実行プランによって消費されるメモリをカウントするかどうかを制御します。詳細は[プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)を参照してください。

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">v5.3.0 の新機能</span> {#tidb-enable-pseudo-for-outdated-stats-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計が古い場合にテーブルの統計を使用する際のオプティマイザーの動作を制御します。

<CustomContent platform="tidb">

-   オプティマイザは、統計を取得するためにテーブルで最後に`ANALYZE`が実行されてから、テーブルの行の 80% が変更されているかどうか (変更された行数を合計行数で割った値) という方法で、テーブルの統計が古いかどうかを判断します。 )、オプティマイザは、このテーブルの統計が古いと判断します。 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)構成を使用してこの比率を変更できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   オプティマイザは、テーブルの統計が古いかどうかを次の方法で判断します。統計を取得するためにテーブルで最後に`ANALYZE`が実行されてから、テーブルの行の 80% が変更されているかどうか (変更された行数を合計行数で割ったもの) )、オプティマイザは、このテーブルの統計が古いと判断します。

</CustomContent>

-   デフォルト (変数値`OFF`の場合) では、テーブルの統計が古くなった場合でも、オプティマイザーはテーブルの統計を引き続き使用します。変数値を`ON`に設定すると、オプティマイザは、合計行数を除いてテーブルの統計が信頼できなくなったと判断します。次に、オプティマイザは擬似統計を使用します。
-   このテーブルで`ANALYZE`時間内に実行せずにテーブルのデータが頻繁に変更される場合は、実行計画を安定させるために、変数値を`OFF`に設定することをお勧めします。

### tidb_enable_rate_limit_action {#tidb-enable-rate-limit-action}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、データを読み取るオペレーターの動的メモリ制御機能を有効にするかどうかを制御します。デフォルトでは、この演算子は、データの読み取りを許可するスレッドの最大数を[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)で有効にします。 1 つの SQL ステートメントのメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超えると、データを読み取るオペレーターは 1 つのスレッドを停止します。

<CustomContent platform="tidb">

-   データを読み取るオペレーターにスレッドが 1 つだけ残っており、単一の SQL ステートメントのメモリ使用量が常に[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超える場合、この SQL ステートメントは他のメモリ制御動作 ( [データをディスクに書き出す](/system-variables.md#tidb_enable_tmp_storage_on_oom)など) をトリガーします。
-   この変数は、SQL ステートメントがデータを読み取るだけの場合に、メモリ使用量を効果的に制御します。コンピューティング操作 (結合操作や集計操作など) が必要な場合、メモリ使用量が`tidb_mem_quota_query`の制御下にない可能性があり、OOM のリスクが増加します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   データを読み取るオペレーターに残っているスレッドが 1 つだけで、単一の SQL ステートメントのメモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超え続ける場合、この SQL ステートメントは、データをディスクにスピルするなど、他のメモリ制御動作をトリガーします。

</CustomContent>

### tidb_enable_resource_control <span class="version-mark">v6.6.0 の新機能</span> {#tidb-enable-resource-control-span-class-version-mark-new-in-v6-6-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は[リソース制御機能](/tidb-resource-control.md)のスイッチです。この変数が`ON`に設定されている場合、TiDB クラスターはリソース グループに基づいてアプリケーション リソースを分離できます。

### tidb_enable_reuse_chunk <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-reuse-chunk-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ON`
-   値`ON`オプション: `OFF`
-   この変数は、TiDB がチャンク オブジェクト キャッシュを有効にするかどうかを制御します。値が`ON`の場合、TiDB はキャッシュされたチャンク オブジェクトの使用を優先し、要求されたオブジェクトがキャッシュにない場合にのみシステムから要求します。値が`OFF`場合、TiDB はシステムからチャンク オブジェクトを直接要求します。

### tidb_enable_slow_log {#tidb-enable-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_tmp_storage_on_oom {#tidb-enable-tmp-storage-on-oom}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ON`
-   値`ON`オプション: `OFF`
-   単一の SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部の演算子の一時storageを有効にするかどうかを制御します。
-   v6.3.0 より前では、TiDB 構成項目`oom-use-tmp-storage`を使用してこの機能を有効または無効にすることができます。クラスターを v6.3.0 以降のバージョンにアップグレードすると、TiDB クラスターは値`oom-use-tmp-storage`を使用してこの変数を自動的に初期化します。その後、 `oom-use-tmp-storage`の値を変更しても**無効になります**。

### tidb_enable_stmt_summary <span class="version-mark">v3.0.4 の新機能</span> {#tidb-enable-stmt-summary-span-class-version-mark-new-in-v3-0-4-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ステートメントの要約機能を有効にするかどうかを制御するために使用されます。有効にすると、時間消費などの SQL 実行情報が`information_schema.STATEMENTS_SUMMARY`システム テーブルに記録され、SQL パフォーマンスの問題を特定してトラブルシューティングします。

### tidb_enable_strict_double_type_check <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-strict-double-type-check-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、タイプ`DOUBLE`の無効な定義を使用してテーブルを作成できるかどうかを制御するために使用されます。この設定は、型の検証がそれほど厳密ではなかった TiDB の以前のバージョンからのアップグレード パスを提供することを目的としています。
-   デフォルト値の`ON` MySQL と互換性があります。

たとえば、浮動小数点型の精度が保証されていないため、型`DOUBLE(10)`は無効とみなされます。 `tidb_enable_strict_double_type_check`を`OFF`に変更すると、テーブルが作成されます。

```sql
mysql> CREATE TABLE t1 (id int, c double(10));
ERROR 1149 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use

mysql> SET tidb_enable_strict_double_type_check = 'OFF';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE t1 (id int, c double(10));
Query OK, 0 rows affected (0.09 sec)
```

> **注記：**
>
> MySQL では`FLOAT`タイプの精度が許可されているため、この設定はタイプ`DOUBLE`にのみ適用されます。この動作は MySQL 8.0.17 以降では非推奨となり、 `FLOAT`または`DOUBLE`型の精度を指定することは推奨されません。

### tidb_enable_table_partition {#tidb-enable-table-partition}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON` 、 `AUTO`
-   この変数は、 `TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。
    -   `ON` 、範囲パーティショニング、ハッシュ パーティショニング、および 1 つの列での範囲列パーティショニングを有効にすることを示します。
    -   `AUTO` `ON`と同じように関数。
    -   `OFF` `TABLE PARTITION`機能を無効にすることを示します。この場合、パーティション テーブルを作成する構文は実行できますが、作成されるテーブルはパーティション化されたテーブルではありません。

### tidb_enable_telemetry <span class="version-mark">v4.0.2 の新機能</span> {#tidb-enable-telemetry-span-class-version-mark-new-in-v4-0-2-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、TiDB でのテレメトリ収集が有効かどうかを動的に制御するために使用されます。現在のバージョンでは、テレメトリはデフォルトで無効になっています。すべての TiDB インスタンスで[`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) TiDB 構成項目が`false`に設定されている場合、テレメトリ収集は常に無効になり、このシステム変数は有効になりません。詳細は[テレメトリー](/telemetry.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB でのテレメトリ収集が有効かどうかを動的に制御するために使用されます。

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-tiflash-read-for-write-stmt-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `INSERT` 、 `DELETE` 、および`UPDATE`を含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできるかどうかを制御します。例えば：

    -   `INSERT INTO SELECT`ステートメントにクエリが`SELECT` (一般的な使用シナリオ: [TiFlashクエリ結果の具体化](/tiflash/tiflash-results-materialization.md) )
    -   `UPDATE`および`DELETE`ステートメントでの`WHERE`条件フィルタリング
-   v7.1.0 以降、この変数は非推奨になりました。 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)の場合、オプティマイザは[SQLモード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュするかどうかをインテリジェントに決定します。 TiDB では、現在のセッションの[SQLモード](/sql-mode.md)厳密ではない場合、つまり`sql_mode`値に`STRICT_TRANS_TABLES`含まれていない場合に限り、 `INSERT` 、 `DELETE` 、および`UPDATE` ( `INSERT INTO SELECT`など) を含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできることに注意してください。 `STRICT_ALL_TABLES` ．

### tidb_enable_top_sql <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-top-sql-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、 [Top SQL](/dashboard/top-sql.md)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

### tidb_enable_tso_follower_proxy <span class="version-mark">v5.3.0 の新機能</span> {#tidb-enable-tso-follower-proxy-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TSOFollowerプロキシ機能を有効にするために使用されます。値が`OFF`の場合、TiDB は PD リーダーからのみ TSO を取得します。この機能を有効にすると、TiDB はすべての PD ノードにリクエストを均等に送信し、PD フォロワーを通じて TSO リクエストを転送することによって TSO を取得します。これは、PD リーダーの CPU 負荷を軽減するのに役立ちます。
-   TSOFollowerプロキシを有効にするシナリオ:
    -   TSO 要求の負荷が高いため、PD リーダーの CPU がボトルネックに達し、TSO RPC 要求のレイテンシーが長くなります。
    -   TiDB クラスターには多数の TiDB インスタンスがあり、値[`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)を増やしても、TSO RPC リクエストのレイテンシーが長い問題は軽減できません。

> **注記：**
>
> PD リーダーの CPU 使用率のボトルネック以外の理由 (ネットワークの問題など) で TSO RPCレイテンシーが増加すると仮定します。この場合、TSO Follower Proxy を有効にすると、TiDB での実行レイテンシーが増加し、クラスターの QPS パフォーマンスに影響を与える可能性があります。

### tidb_enable_unsafe_substitute <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-unsafe-substitute-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、式を安全でない方法で生成された列に置き換えるかどうかを制御します。デフォルト値は`OFF`です。これは、安全でない置換がデフォルトで無効になっていることを意味します。詳細については、 [生成された列](/generated-columns.md)を参照してください。

### tidb_enable_vectorized_expression <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-vectorized-expression-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ベクトル化された実行を有効にするかどうかを制御するために使用されます。

### tidb_enable_window_function {#tidb-enable-window-function}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数のサポートを有効にするかどうかを制御するために使用されます。ウィンドウ関数は予約されたキーワードを使用する場合があることに注意してください。これにより、TiDB のアップグレード後に、通常は実行できた SQL ステートメントが解析できなくなる可能性があります。この場合、 `tidb_enable_window_function` ～ `OFF`を設定できます。

### <code>tidb_enable_row_level_checksum</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-enable-row-level-checksum-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、 [単一行データの TiCDC データ整合性検証](/ticdc/ticdc-integrity-check.md)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [単一行データの TiCDC データ整合性検証](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

### tidb_enforce_mpp <span class="version-mark">v5.1 の新機能</span> {#tidb-enforce-mpp-span-class-version-mark-new-in-v5-1-span}

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   このデフォルト値を変更するには、 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値を変更します。

</CustomContent>

-   オプティマイザのコスト推定を無視し、クエリ実行に TiFlash の MPP モードを強制的に使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF` 。MPP モードが強制的に使用されないことを意味します (デフォルト)。
    -   `1`または`ON` 。コスト推定が無視され、MPP モードが強制的に使用されることを意味します。この設定は`tidb_allow_mpp=true`の場合にのみ有効であることに注意してください。

MPP は、 TiFlashエンジンによって提供される分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能、高スループットの SQL アルゴリズムを提供します。 MPP モードの選択については、 [MPP モードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_evolve_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ベースライン進化機能を有効にするかどうかを制御するために使用されます。詳しい導入や使用方法については、 [ベースラインの進化](/sql-plan-management.md#baseline-evolution)を参照してください。
-   クラスターに対するベースラインの進化の影響を軽減するには、次の構成を使用します。
    -   各実行プランの最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`を設定します。デフォルト値は 600 秒です。
    -   時間枠を制限するには、 `tidb_evolve_plan_task_start_time`と`tidb_evolve_plan_task_end_time`を設定します。デフォルト値はそれぞれ`00:00 +0000`と`23:59 +0000`です。

### tidb_evolve_plan_task_end_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-end-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、1 日のベースライン展開の終了時間を設定するために使用されます。

### tidb_evolve_plan_task_max_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-max-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `600`
-   範囲: `[-1, 9223372036854775807]`
-   単位: 秒
-   この変数は、ベースライン展開機能の各実行プランの最大実行時間を制限するために使用されます。

### tidb_evolve_plan_task_start_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-start-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、1 日のベースライン展開の開始時刻を設定するために使用されます。

### tidb_executor_concurrency <span class="version-mark">v5.0 の新機能</span> {#tidb-executor-concurrency-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `5`
-   範囲: `[1, 256]`
-   単位: スレッド

この変数は、次の SQL 演算子の同時実行性を (1 つの値に) 設定するために使用されます。

-   `index lookup`
-   `index lookup join`
-   `hash join`
-   `hash aggregation` （ `partial`相と`final`相）
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

v5.0 以降、上記のシステム変数を個別に変更することができ (非推奨の警告が返されます)、変更は対応する単一の演算子にのみ影響します。その後、 `tidb_executor_concurrency`を使用して演算子の同時実行性を変更しても、個別に変更された演算子は影響を受けません。 `tidb_executor_concurrency`を使用してすべての演算子の同時実行性を変更する場合は、上記のすべての変数の値を`-1`に設定できます。

以前のバージョンから v5.0 にアップグレードされたシステムの場合、上記の変数の値を何も変更していない場合 (つまり、 `tidb_hash_join_concurrency`値は`5`で、残りの値は`4`です)、オペレータの同時実行性は以前はこれらの変数は`tidb_executor_concurrency`によって自動的に管理されます。これらの変数のいずれかを変更した場合でも、対応する演算子の同時実行性は変更された変数によって制御されます。

### tidb_expensive_query_time_threshold {#tidb-expensive-query-time-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 2147483647]`
-   単位: 秒
-   この変数は、高価なクエリ ログを印刷するかどうかを決定するしきい値を設定するために使用されます。高価なクエリ ログと低速なクエリ ログの違いは次のとおりです。
    -   スローログはステートメントの実行後に出力されます。
    -   負荷の高いクエリ ログには、実行時間がしきい値を超えて実行されているステートメントとその関連情報が出力されます。

### tidb_force_priority {#tidb-force-priority}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 列挙型
-   デフォルト値: `NO_PRIORITY`
-   可能な値: `NO_PRIORITY` 、 `LOW_PRIORITY` 、 `HIGH_PRIORITY` 、 `DELAYED`
-   この変数は、TiDBサーバー上で実行されるステートメントのデフォルトの優先順位を変更するために使用されます。使用例は、OLAP クエリを実行している特定のユーザーが OLTP クエリを実行しているユーザーよりも低い優先順位を確実に受け取るようにすることです。
-   デフォルト値`NO_PRIORITY`は、ステートメントの優先順位が強制的に変更されないことを意味します。

### tidb_gc_concurrency <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-concurrency-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   GCの[ロックの解決](/garbage-collection-overview.md#resolve-locks)ステップのスレッド数を指定します。値`-1`は、TiDB が使用するガベージコレクションスレッドの数を自動的に決定することを意味します。

### tidb_gc_enable <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-enable-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiKV のガベージコレクションを有効にします。ガベージコレクションを無効にすると、古いバージョンの行がパージされなくなるため、システムのパフォーマンスが低下します。

### tidb_gc_life_time <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-life-time-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   各 GC のデータが保持される時間制限 (Go 継続時間の形式)。 GC が発生した場合、現在時刻からこの値を引いた時間が安全点となります。

> **注記：**
>
> -   頻繁に更新が行われるシナリオでは、 `tidb_gc_life_time`値が大きい (日または月単位) と、次のような潜在的な問題が発生する可能性があります。
>     -   より大規模なstorageの使用
>     -   大量の履歴データは、特に`select count(*) from t`のような範囲クエリの場合、パフォーマンスにある程度影響を与える可能性があります。
> -   `tidb_gc_life_time`より長く実行されているトランザクションがある場合、GC 中に、このトランザクションが実行を継続するために`start_ts`以降のデータが保持されます。たとえば、 `tidb_gc_life_time`が 10 分に設定されている場合、実行中のすべてのトランザクションのうち、最も早く開始されたトランザクションが 15 分間実行されており、GC は最近 15 分間のデータを保持します。

### tidb_gc_max_wait_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-gc-max-wait-time-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `86400`
-   範囲: `[600, 31536000]`
-   単位: 秒
-   この変数は、アクティブなトランザクションが GC セーフ ポイントをブロックする最大時間を設定するために使用されます。デフォルトでは、GC の各時間中、安全ポイントは進行中のトランザクションの開始時刻を超えません。アクティブなトランザクションの実行時間がこの変数値を超えない場合、実行時間がこの値を超えるまで GC セーフ ポイントはブロックされます。

### tidb_gc_run_interval <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-run-interval-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   GC 間隔を Go 期間の形式で指定します (例: `"1h30m"` 、 `"15m"`

### tidb_gc_scan_lock_mode <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-scan-lock-mode-span-class-version-mark-new-in-v5-0-span}

> **警告：**
>
> 現在、Green GC は実験的機能です。本番環境で使用することはお勧めできません。

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `LEGACY`
-   可能な値: `PHYSICAL` 、 `LEGACY`
    -   `LEGACY` : 古いスキャン方法を使用します。つまり、Green GC を無効にします。
    -   `PHYSICAL` : 物理スキャン方式を使用します。つまり、Green GC を有効にします。

<CustomContent platform="tidb">

-   この変数は、GC のロックの解決ステップでロックをスキャンする方法を指定します。変数値が`LEGACY`に設定されている場合、TiDB はリージョンごとにロックをスキャンします。値`PHYSICAL`を使用すると、各 TiKV ノードがRaftレイヤーをバイパスしてデータを直接スキャンできるようになり、機能[ハイバネートリージョン](/tikv-configuration-file.md#hibernate-regions)有効になっているときにすべてのリージョンをウェイクアップする GC の影響を効果的に軽減できるため、ロック解決の実行速度が向上します。ステップ。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、GC のロックの解決ステップでロックをスキャンする方法を指定します。変数値が`LEGACY`に設定されている場合、TiDB はリージョンごとにロックをスキャンします。値`PHYSICAL`を使用すると、各 TiKV ノードがRaftレイヤーをバイパスしてデータを直接スキャンできるようになり、すべてのリージョンをウェイクアップする GC の影響を効果的に軽減できるため、ロックの解決ステップの実行速度が向上します。

</CustomContent>

### tidb_general_log {#tidb-general-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb-cloud">

-   この変数は、すべての SQL ステートメントをログに記録するかどうかを設定するために使用されます。この機能はデフォルトでは無効になっています。問題を特定するときにすべての SQL ステートメントをトレースする必要がある場合は、この機能を有効にします。

</CustomContent>

<CustomContent platform="tidb">

-   この変数は、すべての SQL ステートメントを[ログ](/tidb-configuration-file.md#logfile)に記録するかどうかを設定するために使用されます。この機能はデフォルトでは無効になっています。保守担当者が問題を特定するときにすべての SQL ステートメントをトレースする必要がある場合は、この機能を有効にすることができます。

-   ログ内のこの機能のすべてのレコードを確認するには、TiDB 構成項目を[`log.level`](/tidb-configuration-file.md#level)から`"info"`または`"debug"`に設定し、文字列`"GENERAL_LOG"`をクエリする必要があります。次の情報が記録されます。
    -   `conn` : 現在のセッションの ID。
    -   `user` : 現在のセッション ユーザー。
    -   `schemaVersion` : 現在のスキーマのバージョン。
    -   `txnStartTS` : 現在のトランザクションが開始されるタイムスタンプ。
    -   `forUpdateTS` :悲観的トランザクション モードでは、 `forUpdateTS`は SQL ステートメントの現在のタイムスタンプです。悲観的トランザクションで書き込み競合が発生すると、TiDB は現在実行中の SQL ステートメントを再試行し、このタイムスタンプを更新します。再試行回数は[`max-retry-count`](/tidb-configuration-file.md#max-retry-count)で設定できます。楽観的トランザクション モデルでは、 `forUpdateTS`は`txnStartTS`に相当します。
    -   `isReadConsistency` : 現在のトランザクション分離レベルが Read Committed (RC) であるかどうかを示します。
    -   `current_db` : 現在のデータベースの名前。
    -   `txn_mode` : トランザクションモード。値のオプションは`OPTIMISTIC`および`PESSIMISTIC`です。
    -   `sql` : 現在のクエリに対応する SQL ステートメント。

</CustomContent>

### tidb_non_prepared_plan_cache_size {#tidb-non-prepared-plan-cache-size}

> **警告：**
>
> v7.1.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は、キャッシュできる実行プランの最大数を[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)単位で制御します。

### tidb_generate_binary_plan <span class="version-mark">v6.2.0 の新機能</span> {#tidb-generate-binary-plan-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログおよびステートメント サマリーにバイナリ エンコードされた実行プランを生成するかどうかを制御します。
-   この変数を`ON`に設定すると、TiDB ダッシュボードで視覚的な実行プランを表示できます。 TiDB ダッシュボードは、この変数が有効になった後に生成された実行プランの視覚的な表示のみを提供することに注意してください。
-   `SELECT tidb_decode_binary_plan('xxx...')`ステートメントを実行して、バイナリ プランから特定のプランを解析できます。

### tidb_gogc_tuner_threshold <span class="version-mark">v6.4.0 の新機能</span> {#tidb-gogc-tuner-threshold-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `0.6`
-   範囲: `[0, 0.9)`
-   この変数は、GOGC を調整するための最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC チューナーは動作を停止します。

### tidb_guarantee_linearizability <span class="version-mark">v5.0 の新機能</span> {#tidb-guarantee-linearizability-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、非同期コミットのコミット TS の計算方法を制御します。デフォルト (値`ON` ) では、2 フェーズ コミットは PDサーバーから新しい TS を要求し、その TS を使用して最終コミット TS を計算します。この状況では、すべての同時トランザクションに対して線形化可能性が保証されます。
-   この変数を`OFF`に設定すると、PDサーバーから TS を取得するプロセスがスキップされますが、その代償として、因果関係の一貫性のみが保証されますが、線形化可能性は保証されません。詳細については、ブログ投稿[非同期コミット、TiDB 5.0 のトランザクションコミットのアクセラレータ](https://en.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/)参照してください。
-   因果関係の一貫性のみが必要なシナリオの場合、この変数を`OFF`に設定すると、パフォーマンスが向上します。

### tidb_hash_exchange_with_new_collat​​ion {#tidb-hash-exchange-with-new-collation}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、新しい照合順序が有効になっているクラスターで MPP ハッシュ パーティション交換演算子を生成するかどうかを制御します。 `true`演算子を生成することを意味し、 `false`演算子を生成しないことを意味します。
-   この変数は TiDB の内部操作に使用されます。この変数を設定すること**はお勧めできません**。

### tidb_hash_join_concurrency {#tidb-hash-join-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `hash join`アルゴリズムの同時実行性を設定するために使用されます。
-   値`-1`は、値`tidb_executor_concurrency`が代わりに使用されることを意味します。

### tidb_hashagg_final_concurrency {#tidb-hashagg-final-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `final`フェーズで同時実行`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメーターが明確でない場合、 `HashAgg`は`partial`フェーズと`final`フェーズの 2 つのフェーズで同時に実行されます。
-   値`-1`は、値`tidb_executor_concurrency`が代わりに使用されることを意味します。

### tidb_hashagg_partial_concurrency {#tidb-hashagg-partial-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `partial`フェーズで同時実行`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメーターが明確でない場合、 `HashAgg`は`partial`フェーズと`final`フェーズの 2 つのフェーズで同時に実行されます。
-   値`-1`は、値`tidb_executor_concurrency`が代わりに使用されることを意味します。

### tidb_historyal_stats_duration <span class="version-mark">v6.6.0 の新機能</span> {#tidb-historical-stats-duration-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   スタイル: 期間
-   デフォルト値: `168h` (7 日を意味します)
-   この変数は、履歴統計がstorageに保持される期間を制御します。

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">v6.0.0 の新機能</span> {#tidb-ignore-prepared-cache-close-stmt-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、プリペアドステートメントキャッシュを閉じるためのコマンドを無視するかどうかを設定するために使用されます。
-   この変数が`ON`に設定されている場合、バイナリ プロトコルの`COM_STMT_CLOSE`コマンドとテキスト プロトコルの[`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md)ステートメントは無視されます。詳細は[`COM_STMT_CLOSE`コマンドと`DEALLOCATE PREPARE`ステートメントを無視します。](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)を参照してください。

### tidb_index_join_batch_size {#tidb-index-join-batch-size}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `25000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup join`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオではより大きな値を使用し、OLTP シナリオではより小さな値を使用します。

### tidb_index_join_double_read_penalty_cost_rate <span class="version-mark">v6.6.0 の新機能</span> {#tidb-index-join-double-read-penalty-cost-rate-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、インデックス結合の選択にペナルティ コストを適用するかどうかを決定します。これにより、オプティマイザがインデックス結合を選択する可能性が減り、ハッシュ結合や tflash 結合などの代替結合方法が選択される可能性が高くなります。
-   インデックス結合が選択されている場合、多くのテーブル検索リクエストがトリガーされ、大量のリソースが消費されます。この変数を使用すると、オプティマイザがインデックス結合を選択する可能性を減らすことができます。
-   この変数は、 [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620)変数が`2`に設定されている場合にのみ有効になります。

### tidb_index_lookup_concurrency {#tidb-index-lookup-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオではより大きな値を使用し、OLTP シナリオではより小さな値を使用します。
-   値`-1`は、値`tidb_executor_concurrency`が代わりに使用されることを意味します。

### tidb_index_lookup_join_concurrency {#tidb-index-lookup-join-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup join`アルゴリズムの同時実行性を設定するために使用されます。
-   値`-1`は、値`tidb_executor_concurrency`が代わりに使用されることを意味します。

### tidb_index_merge_intersection_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-index-merge-intersection-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   この変数は、インデックス マージが実行する交差操作の最大同時実行数を設定します。これは、TiDB が動的プルーニング モードでパーティション化されたテーブルにアクセスする場合にのみ有効です。実際の同時実行数は、 `tidb_index_merge_intersection_concurrency`とパーティションテーブルのパーティション数の小さい方の値です。
-   デフォルト値`-1`値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_size {#tidb-index-lookup-size}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `20000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオではより大きな値を使用し、OLTP シナリオではより小さな値を使用します。

### tidb_index_serial_scan_concurrency {#tidb-index-serial-scan-concurrency}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `serial scan`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオではより大きな値を使用し、OLTP シナリオではより小さな値を使用します。

### tidb_init_chunk_size {#tidb-init-chunk-size}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `32`
-   範囲: `[1, 32]`
-   単位: 行
-   この変数は、実行プロセス中に最初のチャンクの行数を設定するために使用されます。

### tidb_isolation_read_engines <span class="version-mark">v4.0 の新機能</span> {#tidb-isolation-read-engines-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション
-   デフォルト値: `tikv,tiflash,tidb`
-   この変数は、TiDB がデータを読み取るときに使用できるstorageエンジン リストを設定するために使用されます。

### tidb_last_ddl_info <span class="version-mark">v6.0.0 の新機能</span> {#tidb-last-ddl-info-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション
-   デフォルト値: &quot;&quot;
-   タイプ: 文字列
-   これは読み取り専用の変数です。これは、現在のセッション内の最後の DDL 操作の情報を取得するために TiDB で内部的に使用されます。
    -   &quot;query&quot;: 最後の DDL クエリ文字列。
    -   &quot;seq_num&quot;: 各 DDL 操作のシーケンス番号。これは、DDL 操作の順序を識別するために使用されます。

### tidb_last_query_info <span class="version-mark">v4.0.14 の新機能</span> {#tidb-last-query-info-span-class-version-mark-new-in-v4-0-14-span}

-   範囲: セッション
-   デフォルト値: &quot;&quot;
-   これは読み取り専用の変数です。これは、最後の DML ステートメントのトランザクション情報をクエリするために TiDB で内部的に使用されます。情報には次のものが含まれます。
    -   `txn_scope` : トランザクションのスコープ。 `global`または`local`です。
    -   `start_ts` : トランザクションの開始タイムスタンプ。
    -   `for_update_ts` : 以前に実行された DML ステートメントの`for_update_ts` 。これは、テストに使用される TiDB の内部用語です。通常、この情報は無視してかまいません。
    -   `error` : エラー メッセージ (存在する場合)。

### tidb_last_txn_info <span class="version-mark">v4.0.9 の新機能</span> {#tidb-last-txn-info-span-class-version-mark-new-in-v4-0-9-span}

-   範囲: セッション
-   タイプ: 文字列
-   この変数は、現在のセッション内の最後のトランザクション情報を取得するために使用されます。読み取り専用の変数です。取引情報には次のものが含まれます。
    -   トランザクションのスコープ。
    -   TS の開始とコミット。
    -   トランザクション コミット モード。2 フェーズ、1 フェーズ、または非同期コミットの場合があります。
    -   非同期コミットまたは1フェーズコミットから2フェーズコミットへのトランザクションフォールバックの情報。
    -   エラーが発生しました。

### tidb_last_plan_replayer_token <span class="version-mark">v6.3.0 の新機能</span> {#tidb-last-plan-replayer-token-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション
-   タイプ: 文字列
-   この変数は読み取り専用で、現在のセッションの最後の`PLAN REPLAYER DUMP`の実行結果を取得するために使用されます。

### tidb_load_based_replica_read_threshold <span class="version-mark">v7.0.0 の新機能</span> {#tidb-load-based-replica-read-threshold-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb">

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   タイプ: 文字列
-   この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定するために使用されます。リーダー ノードの推定キュー時間がしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。形式は、 `"100ms"`や`"1s"`などの期間です。詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   タイプ: 文字列
-   この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定するために使用されます。リーダー ノードの推定キュー時間がしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。形式は、 `"100ms"`や`"1s"`などの期間です。詳細については、 [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#scatter-read-hotspots)を参照してください。

</CustomContent>

### <code>tidb_lock_unchanged_keys</code> <span class="version-mark">v7.1.1 の新機能</span> {#code-tidb-lock-unchanged-keys-code-span-class-version-mark-new-in-v7-1-1-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、次のシナリオで特定のキーをロックするかどうかを制御するために使用されます。値を`ON`に設定すると、これらのキーはロックされます。値が`OFF`に設定されている場合、これらのキーはロックされません。
    -   `INSERT IGNORE`と`REPLACE`ステートメントでキーが重複しています。 v6.1.6 より前では、これらのキーはロックされていませんでした。この問題は[#42121](https://github.com/pingcap/tidb/issues/42121)で修正されました。
    -   キーの値が変更されていない場合の`UPDATE`ステートメント内の一意のキー。 v6.5.2 より前では、これらのキーはロックされていませんでした。この問題は[#36438](https://github.com/pingcap/tidb/issues/36438)で修正されました。
-   トランザクションの一貫性と合理性を維持するために、この値を変更することはお勧めできません。 TiDB をアップグレードすると、これら 2 つの修正が原因で深刻なパフォーマンスの問題が発生し、ロックなしの動作が許容される場合 (前述の問題を参照)、この変数を`OFF`に設定できます。

### tidb_log_file_max_days <span class="version-mark">v5.3.0 の新機能</span> {#tidb-log-file-max-days-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`

<CustomContent platform="tidb">

-   この変数は、現在の TiDB インスタンスでログが保持される最大日数を設定するために使用されます。その値のデフォルトは、構成ファイル内の[`max-days`](/tidb-configuration-file.md#max-days)構成の値です。変数値の変更は、現在の TiDB インスタンスにのみ影響します。 TiDB が再起動されると、変数値はリセットされ、構成値は影響を受けません。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、現在の TiDB インスタンスでログが保持される最大日数を設定するために使用されます。

</CustomContent>

### tidb_low_resolution_tso {#tidb-low-resolution-tso}

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、低精度 TSO 機能を有効にするかどうかを設定するために使用されます。この機能を有効にすると、新しいトランザクションは 2 秒ごとに更新されるタイムスタンプを使用してデータを読み取ります。
-   適用可能な主なシナリオは、古いデータの読み取りが許容される場合に、小規模な読み取り専用トランザクションの TSO 取得のオーバーヘッドを削減することです。

### tidb_max_auto_analyze_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-auto-analyze-time-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `43200`
-   範囲: `[0, 2147483647]`
-   単位: 秒
-   この変数は、自動`ANALYZE`タスクの最大実行時間を指定するために使用されます。自動`ANALYZE`タスクの実行時間が指定時間を超えると、タスクは終了します。この変数の値が`0`の場合、 `ANALYZE`の自動タスクの最大実行時間に制限はありません。

### tidb_max_bytes_before_tiflash_external_group_by <span class="version-mark">v7.0.0 の新機能</span> {#tidb-max-bytes-before-tiflash-external-group-by-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashの`GROUP BY`でハッシュ集計演算子の最大メモリ使用量をバイト単位で指定するために使用されます。メモリ使用量が指定された値を超えると、 TiFlash はハッシュ集計オペレータをトリガーしてディスクに書き込みます。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量が無制限であること、つまり、 TiFlash Hash 集計オペレータがスピルをトリガーしないことを意味します。詳細は[TiFlash のディスクへの流出](/tiflash/tiflash-spill-disk.md)を参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、通常、集約は複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の集約オペレーターの最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目[`max_bytes_before_external_group_by`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて集計演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、通常、集約は複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の集約オペレーターの最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目`max_bytes_before_external_group_by`の値に基づいて集計演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_join <span class="version-mark">v7.0.0 の新機能</span> {#tidb-max-bytes-before-tiflash-external-join-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashで`JOIN`使用してハッシュ結合演算子の最大メモリ使用量をバイト単位で指定するために使用されます。メモリ使用量が指定された値を超えると、 TiFlash はハッシュ結合演算子をトリガーしてディスクに書き込みます。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量が無制限であること、つまり、 TiFlash Hash Join 演算子がスピルをトリガーしないことを意味します。詳細は[TiFlash のディスクへの流出](/tiflash/tiflash-spill-disk.md)を参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、結合は通常、複数のTiFlashノードで分散的に実行されます。この変数は、単一のTiFlashノード上の結合演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は自身の構成項目[`max_bytes_before_external_join`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて結合演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、結合は通常、複数のTiFlashノードで分散的に実行されます。この変数は、単一のTiFlashノード上の結合演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は自身の構成項目`max_bytes_before_external_join`の値に基づいて結合演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_sort <span class="version-mark">v7.0.0 の新機能</span> {#tidb-max-bytes-before-tiflash-external-sort-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashの TopN および Sort オペレーターの最大メモリ使用量をバイト単位で指定するために使用されます。メモリ使用量が指定された値を超えると、 TiFlash はTopN および Sort オペレータをトリガーしてディスクに書き込みます。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量が無制限であることを意味します。つまり、 TiFlash TopN および Sort オペレータがスピルをトリガーしないことを意味します。詳細は[TiFlash のディスクへの流出](/tiflash/tiflash-spill-disk.md)を参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、通常、TopN と Sort は複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の TopN および Sort オペレーターの最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は、独自の構成項目[`max_bytes_before_external_sort`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて、TopN および Sort オペレーターの最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、通常、TopN と Sort は複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の TopN および Sort オペレーターの最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は、独自の構成項目`max_bytes_before_external_sort`の値に基づいて、TopN および Sort オペレーターの最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_chunk_size {#tidb-max-chunk-size}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[32, 2147483647]`
-   単位: 行
-   この変数は、実行プロセス中にチャンク内の最大行数を設定するために使用されます。値を大きすぎる値に設定すると、キャッシュの局所性の問題が発生する可能性があります。

### tidb_max_delta_schema_count <span class="version-mark">v2.1.18 および v3.0.5 の新機能</span> {#tidb-max-delta-schema-count-span-class-version-mark-new-in-v2-1-18-and-v3-0-5-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[100, 16384]`
-   この変数は、キャッシュできるスキーマ バージョン (対応するバージョンに変更されたテーブル ID) の最大数を設定するために使用されます。値の範囲は 100 ～ 16384 です。

### tidb_max_paging_size <span class="version-mark">v6.3.0 の新機能</span> {#tidb-max-paging-size-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `50000`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサーのページング要求プロセス中に最大行数を設定するために使用されます。この値を小さすぎる値に設定すると、TiDB と TiKV の間の RPC カウントが増加します。一方、値を大きすぎる値に設定すると、データのロードやテーブル全体のスキャンなど、場合によっては過剰なメモリ使用量が発生します。この変数のデフォルト値により、OLAP シナリオよりも OLTP シナリオの方がパフォーマンスが向上します。アプリケーションがstorageエンジンとして TiKV のみを使用している場合は、OLAP ワークロード クエリを実行するときにこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

### tidb_max_tiflash_threads <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-tiflash-threads-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、リクエストを実行するためのTiFlash の最大同時実行数を設定するために使用されます。デフォルト値は`-1`で、このシステム変数が無効であることを示します。値が`0`の場合、スレッドの最大数はTiFlashによって自動的に設定されます。

### tidb_mem_oom_action <span class="version-mark">v6.1.0 の新機能</span> {#tidb-mem-oom-action-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `CANCEL`
-   可能な値: `CANCEL` 、 `LOG`

<CustomContent platform="tidb">

-   単一の SQL ステートメントが`tidb_mem_quota_query`で指定されたメモリクォータを超え、ディスクにスピルオーバーできない場合に TiDB が実行する操作を指定します。詳細は[TiDB メモリ制御](/configure-memory-usage.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   単一の SQL ステートメントが[`tidb_mem_quota_query`](#tidb_mem_quota_query)で指定されたメモリクォータを超え、ディスクにスピルオーバーできない場合に TiDB が実行する操作を指定します。

</CustomContent>

-   デフォルト値は`CANCEL`ですが、TiDB v4.0.2 以前のバージョンでは、デフォルト値は`LOG`です。
-   この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。

### tidb_mem_quota_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-mem-quota-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト
-   この変数は、TiDB 更新統計の最大メモリ使用量を制御します。このようなメモリ使用量は、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)手動で実行する場合と、TiDB がバックグラウンドでタスクを自動的に分析する場合に発生します。合計メモリ使用量がこのしきい値を超えると、ユーザーが実行した`ANALYZE`終了し、サンプリング レートを低くするか、後で再試行することを促すエラー メッセージが報告されます。メモリしきい値を超え、使用されているサンプリング レートがデフォルト値より高いために TiDB バックグラウンドの自動タスクが終了した場合、TiDB はデフォルトのサンプリング レートを使用して更新を再試行します。この変数値が負またはゼロの場合、TiDB は手動更新タスクと自動更新タスクの両方のメモリ使用量を制限しません。

> **注記：**
>
> `auto_analyze` TiDB 起動構成ファイルで`run-auto-analyze`が有効になっている場合にのみ、TiDB クラスターでトリガーされます。

### tidb_mem_quota_apply_cache <span class="version-mark">v5.0 の新機能</span> {#tidb-mem-quota-apply-cache-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `33554432` (32 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、 `Apply`オペレーターのローカル キャッシュのメモリ使用量のしきい値を設定するために使用されます。
-   `Apply`演算子のローカル キャッシュは、 `Apply`演算子の計算を高速化するために使用されます。変数を`0`に設定すると、 `Apply`キャッシュ機能を無効にすることができます。

### tidb_mem_quota_binding_cache <span class="version-mark">v6.0.0 の新機能</span> {#tidb-mem-quota-binding-cache-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[0, 2147483647]`
-   単位: バイト
-   この変数は、バインディングのキャッシュに使用されるメモリのしきい値を設定するために使用されます。
-   システムが過剰なバインディングを作成またはキャプチャし、その結果メモリ領域が過剰に使用される場合、TiDB はログに警告を返します。この場合、キャッシュは使用可能なすべてのバインディングを保持することも、どのバインディングを保存するかを決定することもできません。このため、一部のクエリではバインディングが失われる可能性があります。この問題に対処するには、この変数の値を増やすと、バインドのキャッシュに使用されるメモリが増加します。このパラメータを変更した後、 `admin reload bindings`実行してバインディングをリロードし、変更を検証する必要があります。

### tidb_mem_quota_query {#tidb-mem-quota-query}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1073741824` (1 GiB)
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト

<CustomContent platform="tidb">

-   TiDB v6.1.0 より前のバージョンの場合、これはセッション スコープ変数であり、 `tidb.toml`から`mem-quota-query`の値を初期値として使用します。 v6.1.0 以降、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0 より前のバージョンでは、この変数は**クエリの**メモリクォータのしきい値を設定するために使用されます。実行中のクエリのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0 以降のバージョンでは、この変数は**セッション**のメモリクォータのしきい値を設定するために使用されます。実行中のセッションのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。 TiDB v6.5.0 以降、セッションのメモリ使用量には、セッション内のトランザクションによって消費されるメモリが含まれることに注意してください。 TiDB v6.5.0 以降のバージョンでのトランザクションメモリ使用量の制御動作については、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)を参照してください。
-   変数値を`0`または`-1`に設定すると、メモリしきい値は正の無限大になります。 128 より小さい値を設定すると、値はデフォルトの`128`に設定されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB v6.1.0 より前のバージョンの場合、これはセッション スコープ変数です。 v6.1.0 以降、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0 より前のバージョンでは、この変数は**クエリの**メモリクォータのしきい値を設定するために使用されます。実行中のクエリのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0 以降のバージョンでは、この変数は**セッション**のメモリクォータのしきい値を設定するために使用されます。実行中のセッションのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。 TiDB v6.5.0 以降、セッションのメモリ使用量には、セッション内のトランザクションによって消費されるメモリが含まれることに注意してください。
-   変数値を`0`または`-1`に設定すると、メモリしきい値は正の無限大になります。 128 より小さい値を設定すると、値はデフォルトの`128`に設定されます。

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio {#tidb-memory-debug-mode-alarm-ratio}

-   範囲: セッション
-   タイプ: フロート
-   デフォルト値: `0`
-   この変数は、TiDBメモリデバッグ モードで許可されるメモリ統計エラー値を表します。
-   この変数は、TiDB の内部テストに使用されます。この変数を設定すること**はお勧めできません**。

### tidb_memory_debug_mode_min_heap_inuse {#tidb-memory-debug-mode-min-heap-inuse}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   この変数は、TiDB の内部テストに使用されます。この変数を設定すること**はお勧めできません**。この変数を有効にすると、TiDB のパフォーマンスに影響します。
-   このパラメータを設定した後、TiDB はメモリデバッグ モードに入り、メモリトラッキングの精度を分析します。 TiDB は、後続の SQL ステートメントの実行中に頻繁に GC をトリガーし、実際のメモリ使用量とメモリ統計を比較します。現在のメモリ使用量が`tidb_memory_debug_mode_min_heap_inuse`を超え、メモリ統計エラーが`tidb_memory_debug_mode_alarm_ratio`超える場合、TiDB は関連するメモリ情報をログとファイルに出力します。

### tidb_memory_usage_alarm_ratio {#tidb-memory-usage-alarm-ratio}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0.0, 1.0]`

<CustomContent platform="tidb">

-   この変数は、tidb-serverメモリアラームをトリガーするメモリ使用率を設定します。デフォルトでは、TiDB のメモリ使用量が総メモリの 70% を超え、 [アラーム条件](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage)のいずれかが満たされた場合、TiDB はアラーム ログを出力。
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能が無効になっていることを意味します。
-   この変数が`0`より大きく`1`未満の値に構成されている場合、メモリしきい値アラーム機能が有効であることを意味します。

    -   システム変数[`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640)の値が`0`の場合、メモリアラームしきい値は`tidb_memory-usage-alarm-ratio * system memory size`です。
    -   システム変数`tidb_server_memory_limit`の値が 0 より大きい値に設定されている場合、メモリアラームしきい値は`tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [tidb サーバーのメモリアラーム](https://docs.pingcap.com/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage)をトリガーするメモリ使用率を設定します。
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能が無効になっていることを意味します。
-   この変数が`0`より大きく`1`未満の値に構成されている場合、メモリしきい値アラーム機能が有効であることを意味します。

</CustomContent>

### tidb_memory_usage_alarm_keep_record_num <span class="version-mark">v6.4.0 の新機能</span> {#tidb-memory-usage-alarm-keep-record-num-span-class-version-mark-new-in-v6-4-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `5`
-   範囲: `[1, 10000]`
-   tidb サーバーのメモリ使用量がメモリアラームしきい値を超えてアラームがトリガーされると、TiDB はデフォルトで最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この変数を使用してこの数値を調整できます。

### tidb_merge_join_concurrency {#tidb-merge-join-concurrency}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   範囲: `[1, 256]`
-   デフォルト値: `1`
-   この変数は、クエリ実行時の`MergeJoin`演算子の同時実行性を設定します。
-   この変数を設定すること**はお勧めできません**。この変数の値を変更すると、データの正確性の問題が発生する可能性があります。

### tidb_merge_partition_stats_concurrency {#tidb-merge-partition-stats-concurrency}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `1`
-   この変数は、TiDB がパーティションテーブルパーティションテーブルを分析するときに、パーティション テーブルの統計をマージする同時実行性を指​​定します。

### tidb_metric_query_range_duration <span class="version-mark">v4.0 の新機能</span> {#tidb-metric-query-range-duration-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位: 秒
-   この変数は、 `METRICS_SCHEMA`をクエリするときに生成される Prometheus ステートメントの範囲期間を設定するために使用されます。

### tidb_metric_query_step <span class="version-mark">v4.0 の新機能</span> {#tidb-metric-query-step-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位: 秒
-   この変数は、 `METRICS_SCHEMA`をクエリするときに生成される Prometheus ステートメントのステップを設定するために使用されます。

### tidb_min_paging_size <span class="version-mark">v6.2.0 の新機能</span> {#tidb-min-paging-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `128`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサーのページング要求プロセス中に最小行数を設定するために使用されます。小さすぎる値に設定すると、TiDB と TiKV の間の RPC リクエスト数が増加します。一方、大きすぎる値に設定すると、制限付きの IndexLookup を使用してクエリを実行するときにパフォーマンスが低下する可能性があります。この変数のデフォルト値により、OLAP シナリオよりも OLTP シナリオの方がパフォーマンスが向上します。アプリケーションがstorageエンジンとして TiKV のみを使用している場合は、OLAP ワークロード クエリを実行するときにこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

![Paging size impact on TPCH](/media/paging-size-impact-on-tpch.png)

この図に示すように、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)が有効な場合、TPCH のパフォーマンスは`tidb_min_paging_size`と[`tidb_max_paging_size`](#tidb_max_paging_size-new-in-v630)の設定によって影響を受けます。縦軸は実行時間であり、小さいほど良い。

### tidb_mpp_store_fail_ttl {#tidb-mpp-store-fail-ttl}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 期間
-   デフォルト値: `60s`
-   新しく開始されたTiFlashノードはサービスを提供しません。クエリの失敗を防ぐために、TiDB は、クエリを送信する tidb サーバーを新しく開始されたTiFlashノードに制限します。この変数は、新しく開始されたTiFlashノードがリクエストを送信しない時間範囲を示します。

### tidb_multi_statement_mode <span class="version-mark">v4.0.11 の新機能</span> {#tidb-multi-statement-mode-span-class-version-mark-new-in-v4-0-11-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `OFF`
-   可能な値: `OFF` 、 `ON` 、 `WARN`
-   この変数は、同じ`COM_QUERY`呼び出しで複数のクエリの実行を許可するかどうかを制御します。
-   SQL インジェクション攻撃の影響を軽減するために、TiDB では、デフォルトで複数のクエリが同じ`COM_QUERY`の呼び出しで実行されないようになっています。この変数は、TiDB の以前のバージョンからのアップグレード パスの一部として使用することを目的としています。次の動作が適用されます。

| クライアント設定        | `tidb_multi_statement_mode`値 | 複数のステートメントは許可されますか? |
| --------------- | ---------------------------- | ------------------- |
| 複数のステートメント = ON | オフ                           | はい                  |
| 複数のステートメント = ON | の上                           | はい                  |
| 複数のステートメント = ON | 警告                           | はい                  |
| 複数のステートメント = オフ | オフ                           | いいえ                 |
| 複数のステートメント = オフ | の上                           | はい                  |
| 複数のステートメント = オフ | 警告                           | はい (+ 警告が返されました)    |

> **注記：**
>
> デフォルト値の`OFF`のみが安全であると考えられます。アプリケーションが TiDB の以前のバージョン用に特別に設計されている場合は、設定`tidb_multi_statement_mode=ON`必要になる場合があります。アプリケーションで複数のステートメントのサポートが必要な場合は、 `tidb_multi_statement_mode`オプションの代わりにクライアント ライブラリによって提供される設定を使用することをお勧めします。例えば：
>
> -   [go-sql-ドライバー](https://github.com/go-sql-driver/mysql#multistatements) ( `multiStatements` )
> -   [コネクタ/J](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-configuration-properties.html) ( `allowMultiQueries` )
> -   PHP [ミスクリ](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) ( `mysqli_multi_query` )

### tidb_nontransactional_ignore_error <span class="version-mark">v6.1.0 の新機能</span> {#tidb-nontransactional-ignore-error-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非トランザクション DML ステートメントでエラーが発生した場合に、ただちにエラーを返すかどうかを指定します。
-   値が`OFF`に設定されている場合、非トランザクション DML ステートメントは最初のエラーですぐに停止し、エラーを返します。以下のバッチはすべてキャンセルされます。
-   値が`ON`に設定され、バッチでエラーが発生した場合、すべてのバッチが実行されるまで次のバッチが実行され続けます。実行プロセス中に発生したすべてのエラーが結果としてまとめて返されます。

### tidb_opt_agg_push_down {#tidb-opt-agg-push-down}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが集計関数を Join、Projection、UnionAll の前の位置にプッシュ ダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリでの集計操作が遅い場合は、変数値を ON に設定できます。

### tidb_opt_broadcast_cartesian_join {#tidb-opt-broadcast-cartesian-join}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   ブロードキャスト デカルト結合を許可するかどうかを示します。
-   `0` 、ブロードキャスト デカルト結合が許可されていないことを意味します。 `1` [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50)に基づいて許可されることを意味します。 `2`テーブル サイズがしきい値を超えた場合でも常に許可されることを意味します。
-   この変数は TiDB で内部的に使用されるため、その値を変更することは**お**勧めできません。

### tidb_opt_concurrency_factor {#tidb-opt-concurrency-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiDB でGolangゴルーチンを開始する際の CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### tidb_opt_copcpu_factor {#tidb-opt-copcpu-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKVコプロセッサーが1 行を処理するための CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### tidb_opt_correlation_exp_factor {#tidb-opt-correlation-exp-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2147483647]`
-   列の順序の相関に基づいて行数を見積もる方法が利用できない場合は、ヒューリスティックな見積方法が使用されます。この変数は、ヒューリスティック手法の動作を制御するために使用されます。
    -   値が 0 の場合、ヒューリスティック手法は使用されません。
    -   値が 0 より大きい場合:
        -   値が大きいほど、インデックス スキャンがヒューリスティック手法で使用される可能性が高いことを示します。
        -   値が小さいほど、テーブル スキャンがヒューリスティック手法で使用される可能性が高いことを示します。

### tidb_opt_correlation_threshold {#tidb-opt-correlation-threshold}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.9`
-   範囲: `[0, 1]`
-   この変数は、列順序相関を使用した行数の推定を有効にするかどうかを決定するしきい値を設定するために使用されます。現在の列と`handle`列目の順序相関がしきい値を超えている場合、このメソッドが有効になります。

### tidb_opt_cpu_factor {#tidb-opt-cpu-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `3.0`
-   TiDB が 1 行を処理するための CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### <code>tidb_opt_derive_topn</code> <span class="version-mark">v7.0.0 の新機能</span> {#code-tidb-opt-derive-topn-code-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   最適化ルール[ウィンドウ関数からの TopN または Limit の導出](/derive-topn-from-window.md)を有効にするかどうかを制御します。

### tidb_opt_desc_factor {#tidb-opt-desc-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKV がディスクから 1 行をスキャンするためのコストを降順で示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### tidb_opt_disk_factor {#tidb-opt-disk-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `1.5`
-   TiDB が一時ディスクとの間で 1 バイトのデータを読み書きするための I/O コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### tidb_opt_distinct_agg_push_down {#tidb-opt-distinct-agg-push-down}

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが`distinct`集合関数 ( `select count(distinct a) from t`など) をコプロセッサーにプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリ内で`distinct`操作を行う集計関数が遅い場合は、変数値を`1`に設定できます。

次の例では、 `tidb_opt_distinct_agg_push_down`を有効にする前に、TiDB は TiKV からすべてのデータを読み取り、TiDB 側で`distinct`を実行する必要があります。 `tidb_opt_distinct_agg_push_down`が有効になった後、 `distinct a`がコプロセッサーにプッシュダウンされ、 `group by`列`test.t.a`が`HashAgg_5`に追加されます。

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

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザが列順序の相関に基づいて行数を推定するかどうかを制御するために使用されます。

### tidb_opt_enable_hash_join <span class="version-mark">v7.1.2 の新機能</span> {#tidb-opt-enable-hash-join-span-class-version-mark-new-in-v7-1-2-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザがテーブルのハッシュ結合を選択するかどうかを制御するために使用されます。デフォルトの値は`ON`です。 `OFF`に設定すると、他の結合アルゴリズムが使用できない場合を除き、オプティマイザーは実行プランの生成時にハッシュ結合の選択を回避します。
-   システム変数`tidb_opt_enable_hash_join`と`HASH_JOIN`ヒントの両方が設定されている場合は、 `HASH_JOIN`ヒントが優先されます。 `tidb_opt_enable_hash_join`が`OFF`に設定されている場合でも、クエリで`HASH_JOIN`ヒントを指定すると、TiDB オプティマイザーはハッシュ結合プランを強制します。

### tidb_opt_enable_late_materialization <span class="version-mark">v7.0.0 の新機能</span> {#tidb-opt-enable-late-materialization-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [TiFlash後期実体化](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御するために使用されます。 TiFlash遅延実体化は[高速スキャンモード](/tiflash/use-fastscan.md)では有効にならないことに注意してください。
-   この変数を`OFF`に設定してTiFlash遅延実体化機能を無効にし、フィルター条件 ( `WHERE`句) を含む`SELECT`ステートメントを処理すると、 TiFlash はフィルター処理の前に必要な列のすべてのデータをスキャンします。この変数を`ON`に設定してTiFlash遅延実体化機能を有効にすると、 TiFlash はまず、TableScan オペレーターにプッシュダウンされたフィルター条件に関連する列データをスキャンし、条件を満たす行をフィルターしてから、次のデータをスキャンできます。これらの行の他の列はさらなる計算のために使用されるため、IO スキャンとデータ処理の計算が削減されます。

### tidb_opt_fix_control <span class="version-mark">v7.1.0 の新機能</span> {#tidb-opt-fix-control-span-class-version-mark-new-in-v7-1-0-span}

<CustomContent platform="tidb">

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: `""`
-   この変数は、オプティマイザーの一部の内部動作を制御するために使用されます。
-   オプティマイザーの動作は、ユーザー シナリオまたは SQL ステートメントによって異なる場合があります。この変数は、オプティマイザーに対するよりきめ細かい制御を提供し、オプティマイザーの動作変更によって引き起こされるアップグレード後のパフォーマンスの低下を防ぐのに役立ちます。
-   より詳細な紹介については、 [オプティマイザー修正コントロール](/optimizer-fix-controls.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 文字列
-   デフォルト値: `""`
-   この変数は、オプティマイザーの一部の内部動作を制御するために使用されます。
-   オプティマイザーの動作は、ユーザー シナリオまたは SQL ステートメントによって異なる場合があります。この変数は、オプティマイザーに対するよりきめ細かい制御を提供し、オプティマイザーの動作変更によって引き起こされるアップグレード後のパフォーマンスの低下を防ぐのに役立ちます。
-   より詳細な紹介については、 [オプティマイザー修正コントロール](https://docs.pingcap.com/tidb/v7.1/optimizer-fix-controls)を参照してください。

</CustomContent>

### tidb_opt_force_inline_cte <span class="version-mark">v6.3.0 の新機能</span> {#tidb-opt-force-inline-cte-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、セッション全体の共通テーブル式 (CTE) をインライン化するかどうかを制御するために使用されます。デフォルト値は`OFF`です。これは、CTE のインライン化がデフォルトでは強制されないことを意味します。ただし、 `MERGE()`ヒントを指定することで CTE をインライン化できます。変数が`ON`に設定されている場合、このセッション内のすべての CTE (再帰 CTE を除く) が強制的にインライン化されます。

### tidb_opt_advanced_join_hint <span class="version-mark">v7.0.0 の新機能</span> {#tidb-opt-advanced-join-hint-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`HASH_JOIN()`ヒント](/optimizer-hints.md#hash_joint1_name--tl_name-)や[`MERGE_JOIN()`ヒント](/optimizer-hints.md#merge_joint1_name--tl_name-)などの結合方法ヒントが、 [`LEADING()`ヒント](/optimizer-hints.md#leadingt1_name--tl_name-)の使用を含む結合したテーブルの再配置最適化プロセスに影響を与えるかどうかを制御するために使用されます。デフォルト値は`ON`で、影響しないことを意味します。 `OFF`に設定すると、結合メソッド ヒントと`LEADING()`ヒントの両方が同時に使用される一部のシナリオで競合が発生する可能性があります。

> **注記：**
>
> v7.0.0 より前のバージョンの動作は、この変数を`OFF`に設定した場合の動作と一致しています。上位互換性を確保するために、以前のバージョンから v7.0.0 以降のクラスターにアップグレードする場合、この変数は`OFF`に設定されます。より柔軟なヒント動作を得るには、パフォーマンスの低下がないという条件でこの変数を`ON`に切り替えることを強くお勧めします。

### tidb_opt_insubq_to_join_and_agg {#tidb-opt-insubq-to-join-and-agg}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、サブクエリを結合および集計に変換する最適化ルールを有効にするかどうかを設定するために使用されます。
-   たとえば、この最適化ルールを有効にすると、サブクエリは次のように変換されます。

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    サブクエリは次のように結合に変換されます。

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    `t1`が`aa`列の`unique`と`not null`に制限される場合。集計を行わずに次のステートメントを使用できます。

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold {#tidb-opt-join-reorder-threshold}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB 結合したテーブルの再配置アルゴリズムの選択を制御するために使用されます。 結合したテーブルの再配置に参加するノードの数がこのしきい値より大きい場合、TiDB は貪欲アルゴリズムを選択し、このしきい値より小さい場合、TiDB は動的プログラミング アルゴリズムを選択します。
-   現在、OLTP クエリについては、デフォルト値を保持することをお勧めします。 OLAP クエリの場合、OLAP シナリオでの接続順序を向上させるために、変数値を 10 ～ 15 に設定することをお勧めします。

### tidb_opt_limit_push_down_threshold {#tidb-opt-limit-push-down-threshold}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   この変数は、Limit 演算子または TopN 演算子を TiKV にプッシュダウンするかどうかを決定するしきい値を設定するために使用されます。
-   Limit または TopN 演算子の値がこのしきい値以下の場合、これらの演算子は強制的に TiKV にプッシュダウンされます。この変数は、誤った推定が部分的に原因で、Limit または TopN オペレーターを TiKV にプッシュダウンできない問題を解決します。

### tidb_opt_memory_factor {#tidb-opt-memory-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `0.001`
-   TiDB が 1 行を保存するためのメモリコストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">v5.1.0 の新機能</span> {#tidb-opt-mpp-outer-join-fixed-build-side-span-class-version-mark-new-in-v5-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   変数値が`ON`の場合、左結合演算子は常に内部テーブルをビルド側として使用し、右結合演算子は常に外部テーブルをビルド側として使用します。値を`OFF`に設定すると、外部結合演算子はテーブルのどちらかの側を構築側として使用できます。

### tidb_opt_network_factor {#tidb-opt-network-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.0`
-   ネットワーク経由で 1 バイトのデータを転送するための正味コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">v7.0.0 の新機能</span> {#tidb-opt-ordering-index-selectivity-threshold-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、SQL ステートメントにフィルター条件を含む句が`ORDER BY`つと`LIMIT`ある場合に、オプティマイザーがインデックスを選択する方法を制御するために使用されます。
-   このようなクエリの場合、オプティマイザは、(このインデックスがどのフィルター条件も満たさない場合でも) `ORDER BY`節と`LIMIT`節を満たすための対応するインデックスの選択を検討します。ただし、データ分散の複雑さのため、このシナリオではオプティマイザが次善のインデックスを選択する可能性があります。
-   この変数はしきい値を表します。フィルター条件を満たすインデックスが存在し、その選択性推定値がこのしきい値よりも低い場合、オプティマイザーは`ORDER BY`と`LIMIT`を満たすために使用されるインデックスの選択を回避します。代わりに、フィルタリング条件を満たすインデックスが優先されます。
-   たとえば、変数が`0`に設定されている場合、オプティマイザはデフォルトの動作を維持します。 `1`に設定すると、オプティマイザーは常にフィルター条件を満たすインデックスの選択を優先し、 `ORDER BY`節と`LIMIT`節の両方を満たすインデックスの選択を回避します。
-   次の例では、テーブル`t`には合計 1,000,000 行があります。列`b`でインデックスを使用する場合、その推定行数は約 8,748 であるため、その選択性推定値は約 0.0087 になります。デフォルトでは、オプティマイザは列`a`のインデックスを選択します。ただし、この変数を 0.01 に設定すると、列`b`のインデックスの選択性 (0.0087) が 0.01 未満になるため、オプティマイザは列`b`のインデックスを選択します。

```sql
> EXPLAIN SELECT * FROM t WHERE b <= 9000 ORDER BY a LIMIT 1;
+-----------------------------------+---------+-----------+----------------------+--------------------+
| id                                | estRows | task      | access object        | operator info      |
+-----------------------------------+---------+-----------+----------------------+--------------------+
| Limit_12                          | 1.00    | root      |                      | offset:0, count:1  |
| └─Projection_25                   | 1.00    | root      |                      | test.t.a, test.t.b |
|   └─IndexLookUp_24                | 1.00    | root      |                      |                    |
|     ├─IndexFullScan_21(Build)     | 114.30  | cop[tikv] | table:t, index:ia(a) | keep order:true    |
|     └─Selection_23(Probe)         | 1.00    | cop[tikv] |                      | le(test.t.b, 9000) |
|       └─TableRowIDScan_22         | 114.30  | cop[tikv] | table:t              | keep order:false   |
+-----------------------------------+---------+-----------+----------------------+--------------------+

> SET SESSION tidb_opt_ordering_index_selectivity_threshold = 0.01;

> EXPLAIN SELECT * FROM t WHERE b <= 9000 ORDER BY a LIMIT 1;
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
| id                               | estRows | task      | access object        | operator info                       |
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
| TopN_9                           | 1.00    | root      |                      | test.t.a, offset:0, count:1         |
| └─IndexLookUp_20                 | 1.00    | root      |                      |                                     |
|   ├─IndexRangeScan_17(Build)     | 8748.62 | cop[tikv] | table:t, index:ib(b) | range:[-inf,9000], keep order:false |
|   └─TopN_19(Probe)               | 1.00    | cop[tikv] |                      | test.t.a, offset:0, count:1         |
|     └─TableRowIDScan_18          | 8748.62 | cop[tikv] | table:t              | keep order:false                    |
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
```

### tidb_opt_prefer_range_scan <span class="version-mark">v5.0 の新機能</span> {#tidb-opt-prefer-range-scan-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数の値を`ON`に設定すると、オプティマイザは常にテーブル全体のスキャンよりも範囲スキャンを優先します。
-   次の例では、 `tidb_opt_prefer_range_scan`有効にする前に、TiDB オプティマイザーはテーブル全体のスキャンを実行します。 `tidb_opt_prefer_range_scan`を有効にすると、オプティマイザはインデックス範囲スキャンを選択します。

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

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ON`
-   この変数は、不要なテーブル ルックアップを回避し、クエリのパフォーマンスを向上させるために、TiDB オプティマイザーが一部のフィルター条件をプレフィックス インデックスにプッシュ ダウンするかどうかを制御します。
-   この変数値が`ON`に設定されると、一部のフィルター条件がプレフィックス インデックスにプッシュダウンされます。 `col`列がテーブルのインデックス接頭辞列であると仮定します。クエリ内の`col is null`または`col is not null`条件は、テーブル検索のフィルター条件ではなく、インデックスのフィルター条件として処理されるため、不要なテーブル検索が回避されます。

<details><summary><code>tidb_opt_prefix_index_single_scan</code>の使用例</summary>

接頭辞インデックスを使用してテーブルを作成します。

```sql
CREATE TABLE t (a INT, b VARCHAR(10), c INT, INDEX idx_a_b(a, b(5)));
```

無効化`tidb_opt_prefix_index_single_scan` :

```sql
SET tidb_opt_prefix_index_single_scan = 'OFF';
```

次のクエリの場合、実行プランはプレフィックス インデックス`idx_a_b`を使用しますが、テーブル検索が必要です ( `IndexLookUp`演算子が表示されます)。

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

この変数を有効にすると、次のクエリの実行プランではプレフィックス インデックス`idx_a_b`が使用されますが、テーブル ルックアップは必要ありません。

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

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   オプティマイザーが TiKV またはTiFlashコプロセッサーに`Projection`をプッシュダウンできるようにするかどうかを指定します。

### tidb_opt_range_max_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-opt-range-max-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `67108864` (64 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を設定するために使用されます。変数値が`0`の場合、スキャン範囲を構築するためのメモリ制限はありません。正確なスキャン範囲を構築すると制限を超えるメモリが消費される場合、オプティマイザはより緩和されたスキャン範囲 ( `[[NULL,+inf]]`など) を使用します。実行計画で正確なスキャン範囲が使用されていない場合は、この変数の値を増やして、オプティマイザーが正確なスキャン範囲を構築できるようにすることができます。

この変数の使用例は次のとおりです。

<details><summary><code>tidb_opt_range_max_size</code>の使用例</summary>

この変数のデフォルト値をビュー。結果から、オプティマイザはスキャン範囲を構築するために最大 64 MiB のメモリを使用していることがわかります。

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

次の実行計画の結果に示すように、64 MiB のメモリ上限では、オプティマイザは次の正確なスキャン範囲`[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`を構築します。

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

次に、オプティマイザのメモリ使用量の上限を設定して、スキャン範囲を 1500 バイトに構築します。

```sql
SET @@tidb_opt_range_max_size = 1500;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

1500 バイトのメモリ制限では、オプティマイザはより緩和されたスキャン範囲`[10,10], [20,20], [30,30]`を構築し、正確なスキャン範囲を構築するために必要なメモリ使用量が制限`tidb_opt_range_max_size`を超えていることをユーザーに通知する警告を使用します。

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

100 バイトのメモリ制限では、オプティマイザは`IndexFullScan`を選択し、警告を使用して、正確なスキャン範囲を構築するために必要なメモリが制限の`tidb_opt_range_max_size`を超えていることをユーザーに通知します。

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

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.5`
-   TiKV がディスクから 1 行のデータを昇順でスキャンするためのコストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### tidb_opt_seek_factor {#tidb-opt-seek-factor}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `20`
-   TiDB が TiKV からデータをリクエストするための初期コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用され、その値を変更することは**お**勧めできません。

### tidb_opt_skew_distinct_agg <span class="version-mark">v6.2.0 の新機能</span> {#tidb-opt-skew-distinct-agg-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この変数を有効にすることによるクエリ パフォーマンスの最適化は**、 TiFlashに対してのみ**有効です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが`DISTINCT`集合関数を2 レベルの集合関数に書き換えるかどうか ( `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換えるなど) を設定します。集計列に深刻なスキューがあり、 `DISTINCT`番目の列に多くの異なる値がある場合、この書き換えによりクエリ実行時のデータ スキューを回避し、クエリのパフォーマンスを向上させることができます。

### tidb_opt_three_stage_distinct_agg <span class="version-mark">v6.3.0 の新機能</span> {#tidb-opt-three-stage-distinct-agg-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、MPP モードで`COUNT(DISTINCT)`集計を 3 段階の集計に書き換えるかどうかを指定します。
-   この変数は現在、 `COUNT(DISTINCT)`を 1 つだけ含む集計に適用されます。

### tidb_opt_tiflash_concurrency_factor {#tidb-opt-tiflash-concurrency-factor}

-   範囲: セッション |グローバル
-   クラスターに永続化: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `24.0`
-   TiFlash計算の同時実行数を示します。この変数はコスト モデルで内部的に使用されるため、その値を変更することはお勧めできません。

### tidb_opt_write_row_id {#tidb-opt-write-row-id}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `INSERT` 、 `REPLACE` 、および`UPDATE`ステートメントが`_tidb_rowid`列で動作することを許可するかどうかを制御するために使用されます。この変数は、TiDB ツールを使用してデータをインポートする場合にのみ使用できます。

### tidb_optimizer_selectivity_level {#tidb-optimizer-selectivity-level}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、オプティマイザーの推定ロジックの反復を制御します。この変数の値を変更すると、オプティマイザの推定ロジックが大きく変わります。現在、有効な値は`0`のみです。他の値に設定することはお勧めできません。

### tidb_partition_prune_mode <span class="version-mark">v5.1 の新機能</span> {#tidb-partition-prune-mode-span-class-version-mark-new-in-v5-1-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `dynamic`
-   可能な値: `static` 、 `dynamic` 、 `static-only` 、 `dynamic-only`
-   パーティションテーブルに`dynamic`を使用するか`static`モードを使用するかを指定します。動的パーティショニングは、完全なテーブルレベルの統計 (GlobalStats) が収集された後にのみ有効であることに注意してください。 GlobalStats が収集される前に、TiDB は代わりに`static`モードを使用します。 GlobalStats の詳細については、 [動的プルーニング モードでパーティション テーブルの統計を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。動的プルーニング モードの詳細については、 [パーティションテーブルの動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)を参照してください。

### tidb_persist_analyze_options <span class="version-mark">v5.4.0 の新機能</span> {#tidb-persist-analyze-options-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [構成の永続性を分析する](/statistics.md#persist-analyze-configurations)機能を有効にするかどうかを制御します。

### tidb_pessimistic_txn_fair_locking <span class="version-mark">v7.0.0 の新機能</span> {#tidb-pessimistic-txn-fair-locking-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   悲観的トランザクションに対して拡張された悲観的ロック ウェイクアップ モデルを使用するかどうかを決定します。このモデルは、不必要なウェイクアップを回避するために、悲観的ロックの単一点競合シナリオにおける悲観的トランザクションのウェイクアップ順序を厳密に制御します。これにより、既存のウェイクアップ メカニズムのランダム性によってもたらされる不確実性が大幅に軽減されます。ビジネス シナリオで単一ポイントの悲観的ロックの競合 (同じデータ行への頻繁な更新など) が頻繁に発生し、ステートメントの頻繁な再試行、高いテールレイテンシー、または場合によっては`pessimistic lock retry limit reached`エラーが発生する場合は、これを有効にしてみてください。問題を解決するための変数。
-   この変数は、v7.0.0 より前のバージョンから v7.0.0 以降のバージョンにアップグレードされた TiDB クラスターではデフォルトで無効になっています。

> **注記：**
>
> -   特定のビジネス シナリオによっては、このオプションを有効にすると、ロックの競合が頻繁に発生するトランザクションのスループットがある程度低下する (平均レイテンシーの増加) 可能性があります。
> -   このオプションは、単一のキーをロックする必要があるステートメントにのみ有効です。ステートメントで複数の行を同時にロックする必要がある場合、このオプションはそのようなステートメントに対しては効果がありません。
> -   この機能は、v6.6.0 で[`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)変数によって導入され、デフォルトでは無効になっています。

### tidb_placement_mode <span class="version-mark">v6.0.0 の新機能</span> {#tidb-placement-mode-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `STRICT`
-   可能な値: `STRICT` 、 `IGNORE`
-   この変数は、DDL ステートメントが[SQLで指定された配置ルール](/placement-rules-in-sql.md)無視するかどうかを制御します。変数値が`IGNORE`場合、すべての配置ルール オプションは無視されます。
-   これは、無効な配置ルールが割り当てられている場合でもテーブルを常に作成できるようにするために、論理ダンプ/復元ツールで使用することを目的としています。これは、mysqldump がすべてのダンプ ファイルの先頭に`SET FOREIGN_KEY_CHECKS=0;`を書き込む方法と似ています。

### <code>tidb_plan_cache_invalidation_on_fresh_stats</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-plan-cache-invalidation-on-fresh-stats-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、関連テーブルの統計が更新されたときにプラン キャッシュを自動的に無効にするかどうかを制御します。
-   この変数を有効にすると、プラン キャッシュは統計をより十分に利用して実行プランを生成できるようになります。例えば：
    -   統計が利用可能になる前に実行プランが生成された場合、統計が利用可能になるとプラン キャッシュによって実行プランが再生成されます。
    -   テーブルのデータ分散が変化し、以前は最適であった実行プランが最適でなくなる場合、統計が再収集された後、プラン キャッシュによって実行プランが再生成されます。
-   この変数は、v7.1.0 より前のバージョンから v7.1.0 以降にアップグレードされた TiDB クラスターではデフォルトで無効になっています。

### <code>tidb_plan_cache_max_plan_size</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-plan-cache-max-plan-size-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `2097152` (2 MB)
-   範囲: `[0, 9223372036854775807]` (バイト単位)。 「KB|MB|GB|TB」単位のメモリ形式もサポートされています。 `0`制限なしを意味します。
-   この変数は、準備済みプラン キャッシュまたは準備されていないプラン キャッシュにキャッシュできるプランの最大サイズを制御します。プランのサイズがこの値を超える場合、プランはキャッシュされません。詳細については、 [準備されたプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)および[準備されていないプラン キャッシュ](/sql-plan-management.md#usage)を参照してください。

### tidb_pprof_sql_cpu <span class="version-mark">v4.0 の新機能</span> {#tidb-pprof-sql-cpu-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、パフォーマンスの問題を特定してトラブルシューティングするために、プロファイル出力内の対応する SQL ステートメントをマークするかどうかを制御するために使用されます。

### tidb_prefer_broadcast_join_by_exchange_data_size <span class="version-mark">v7.1.0 の新機能</span> {#tidb-prefer-broadcast-join-by-exchange-data-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `OFF`
-   この変数は、TiDB が[MPP ハッシュ結合アルゴリズム](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode)を選択するときに、ネットワーク送信のオーバーヘッドを最小限に抑えたアルゴリズムを使用するかどうかを制御します。この変数が有効な場合、TiDB はネットワーク内で交換されるデータのサイズをそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`を使用して推定し、サイズの小さい方を選択します。
-   この変数を有効にした後は、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)は無効になります。

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">v6.1.0 の新機能</span> {#tidb-prepared-plan-cache-memory-guard-ratio-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   デフォルト値: `0.1`
-   範囲: `[0, 1]`
-   準備されたプラン キャッシュがメモリ保護メカニズムをトリガーするしきい値。詳細は[プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)を参照してください。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.memory-guard-ratio` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。

### tidb_prepared_plan_cache_size <span class="version-mark">v6.1.0 の新機能</span> {#tidb-prepared-plan-cache-size-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> v7.1.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   セッション内にキャッシュできるプランの最大数。詳細は[プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)を参照してください。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.capacity` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。

### tidb_projection_concurrency {#tidb-projection-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、 `Projection`オペレーターの同時実行性を設定するために使用されます。
-   値`-1`は、値`tidb_executor_concurrency`が代わりに使用されることを意味します。

### tidb_query_log_max_len {#tidb-query-log-max-len}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `4096` (4 KiB)
-   範囲: `[0, 1073741824]`
-   単位: バイト
-   SQL ステートメント出力の最大長。ステートメントの出力長が値`tidb_query_log_max_len`より大きい場合、ステートメントは切り詰められて出力されます。
-   この設定は以前は`tidb.toml`オプション ( `log.query-log-max-len` ) としても使用できましたが、TiDB v6.1.0 以降はシステム変数のみです。

### tidb_rc_read_check_ts <span class="version-mark">v6.0.0 の新機能</span> {#tidb-rc-read-check-ts-span-class-version-mark-new-in-v6-0-0-span}

> **警告：**
>
> -   この機能は[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。 `tidb_rc_read_check_ts`と`replica-read`同時に有効にしないでください。
> -   クライアントがカーソルを使用する場合、返されたデータの以前のバッチがクライアントによってすでに使用されており、ステートメントが最終的に失敗する可能性があるため、 `tidb_rc_read_check_ts`有効にすることはお勧めできません。
> -   v7.0.0 以降、この変数はプリペアドステートメントプロトコルを使用するカーソル フェッチ読み取りモードでは無効になりました。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、タイムスタンプの取得を最適化するために使用されます。これは、読み取りと書き込みの競合がまれな読み取りコミット分離レベルのシナリオに適しています。この変数を有効にすると、グローバル タイムスタンプの取得にかかるレイテンシーとコストを回避し、トランザクション レベルの読み取りレイテンシーを最適化できます。
-   読み取り/書き込み競合が深刻な場合、この機能を有効にすると、グローバル タイムスタンプを取得するコストとレイテンシーが増加し、パフォーマンスの低下を引き起こす可能性があります。詳細は[コミットされた分離レベルの読み取り](/transaction-isolation-levels.md#read-committed-isolation-level)を参照してください。

### tidb_rc_write_check_ts <span class="version-mark">v6.3.0 の新機能</span> {#tidb-rc-write-check-ts-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この機能は現在[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。この変数を有効にすると、クライアントから送信されるすべてのリクエストは`replica-read`を使用できなくなります。したがって、 `tidb_rc_write_check_ts`と`replica-read`同時に有効にしないでください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数はタイムスタンプの取得を最適化するために使用され、悲観的トランザクションの`READ-COMMITTED`分離レベルでポイント書き込み競合がほとんどないシナリオに適しています。この変数を有効にすると、point-write ステートメントの実行中にグローバル タイムスタンプを取得することによってもたらされるレイテンシーとオーバーヘッドを回避できます。現在、この変数は`UPDATE` 、 `DELETE` 、 `SELECT ...... FOR UPDATE`の 3 種類の point-write ステートメントに適用できます。 point-write ステートメントは、主キーまたは一意キーをフィルター条件として使用し、最終的な実行演算子に`POINT-GET`が含まれる write ステートメントを指します。
-   ポイントと書き込みの競合が深刻な場合、この変数を有効にすると、余分なオーバーヘッドとレイテンシーが増加し、パフォーマンスが低下します。詳細は[コミットされた分離レベルの読み取り](/transaction-isolation-levels.md#read-committed-isolation-level)を参照してください。

### tidb_read_consistency <span class="version-mark">v5.4.0 の新機能</span> {#tidb-read-consistency-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション
-   タイプ: 文字列
-   デフォルト値: `strict`
-   この変数は、自動コミット読み取りステートメントの読み取り一貫性を制御するために使用されます。
-   変数値が`weak`に設定されている場合、読み取りステートメントで発生したロックは直接スキップされ、読み取りの実行が高速になる可能性があります。これは、弱い整合性読み取りモードです。ただし、トランザクション セマンティクス (原子性など) および分散一貫性 (線形化可能性など) は保証されません。
-   自動コミット読み取りが高速に返す必要があり、弱い整合性の読み取り結果が許容されるユーザー シナリオの場合は、弱い整合性の読み取りモードを使用できます。

### tidb_read_staleness <span class="version-mark">v5.4.0 の新機能</span> {#tidb-read-staleness-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-2147483648, 0]`
-   この変数は、TiDB が現在のセッションで読み取ることができる履歴データの時間範囲を設定するために使用されます。値を設定した後、TiDB はこの変数で許可される範囲からできるだけ新しいタイムスタンプを選択し、後続のすべての読み取り操作はこのタイムスタンプに対して実行されます。たとえば、この変数の値が`-5`に設定されている場合、TiKV に対応する履歴バージョンのデータがあるという条件で、TiDB は 5 秒の時間範囲内でできるだけ新しいタイムスタンプを選択します。

### tidb_record_plan_in_slow_log {#tidb-record-plan-in-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、低速クエリの実行計画を低速ログに含めるかどうかを制御するために使用されます。

### tidb_redact_log {#tidb-redact-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB ログおよびスロー ログに記録される SQL ステートメント内のユーザー情報を非表示にするかどうかを制御します。
-   変数を`1`に設定すると、ユーザー情報は非表示になります。たとえば、実行された SQL ステートメントが`insert into t values (1,2)`の場合、そのステートメントはログに`insert into t values (?,?)`として記録されます。

### tidb_regard_null_as_point <span class="version-mark">v5.4.0 の新機能</span> {#tidb-regard-null-as-point-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザがインデックス アクセスの接頭辞条件として NULL 等価性を含むクエリ条件を使用できるかどうかを制御します。
-   この変数はデフォルトで有効になっています。これを有効にすると、オプティマイザーはアクセスするインデックス データの量を削減できるため、クエリの実行が高速化されます。たとえば、クエリに複数列インデックス`index(a, b)`が含まれ、クエリ条件に`a<=>null and b=1`含まれる場合、オプティマイザはインデックス アクセスのクエリ条件で`a<=>null`と`b=1`の両方を使用できます。変数が無効になっている場合、 `a<=>null and b=1`は NULL 等価条件が含まれているため、オプティマイザはインデックス アクセスに`b=1`を使用しません。

### tidb_remove_orderby_in_subquery <span class="version-mark">v6.1.0 の新機能</span> {#tidb-remove-orderby-in-subquery-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   サブクエリ内の`ORDER BY`句を削除するかどうかを指定します。

### tidb_replica_read <span class="version-mark">v4.0 の新機能</span> {#tidb-replica-read-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `leader`
-   可能な値: `leader` 、 `follower` 、 `leader-and-follower` 、 `prefer-leader` 、 `closest-replicas` 、 `closest-adaptive` 、および`learner` 。値`learner`は v6.6.0 で導入されました。
-   この変数は、TiDB がデータを読み取る場所を制御するために使用されます。
-   使用法と実装の詳細については、 [Followerが読んだ](/follower-read.md)を参照してください。

### tidb_restricted_read_only <span class="version-mark">v5.2.0 の新機能</span> {#tidb-restricted-read-only-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_restricted_read_only`と[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)同様に動作します。ほとんどの場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを使用する必要があります。
-   `SUPER`または`SYSTEM_VARIABLES_ADMIN`権限を持つユーザーは、この変数を変更できます。ただし、 [Security強化モード](#tidb_enable_enhanced_security)が有効な場合、この変数の読み取りまたは変更には追加の`RESTRICTED_VARIABLES_ADMIN`権限が必要です。
-   次の場合、 `tidb_restricted_read_only` [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)に影響します。
    -   `tidb_restricted_read_only` ～ `ON`設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) ～ `ON`が更新されます。
    -   `tidb_restricted_read_only` ～ `OFF`設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)変更されません。
    -   `tidb_restricted_read_only`が`ON`場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) `OFF`に設定することはできません。
-   TiDB の DBaaS プロバイダーの場合、TiDB クラスターが別のデータベースのダウンストリーム データベースである場合、TiDB クラスターを読み取り専用にするには、 `tidb_restricted_read_only`を使用して[Security強化モード](#tidb_enable_enhanced_security)有効にする必要がある場合があります。これにより、顧客は[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)を使用してクラスターを書き込み可能にすることができなくなります。これを実現するには、 [Security強化モード](#tidb_enable_enhanced_security)有効にし、 `SYSTEM_VARIABLES_ADMIN`および`RESTRICTED_VARIABLES_ADMIN`権限を持つ管理者ユーザーを使用して`tidb_restricted_read_only`制御し、データベース ユーザーが`SUPER`権限を持つ root ユーザーを使用して[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)を制御できるようにする必要があります。
-   この変数は、クラスター全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスター全体のすべての TiDB サーバーは読み取り専用モードになります。この場合、TiDB は、 `SELECT` 、 `USE` 、 `SHOW`など、データを変更しないステートメントのみを実行します。 `INSERT`や`UPDATE`などの他のステートメントの場合、TiDB は読み取り専用モードでのそれらのステートメントの実行を拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスター全体が最終的に読み取り専用ステータスになることだけが保証されます。 TiDB クラスターでこの変数の値を変更したが、その変更がまだ他の TiDB サーバーに反映されていない場合、更新されていない TiDB サーバーは**依然として**読み取り専用モードになっていません。
-   この変数を有効にすると、実行中の SQL ステートメントは影響を受けません。 TiDB は、**実行**される SQL ステートメントの読み取り専用チェックのみを実行します。
-   この変数が有効な場合、TiDB はコミットされていないトランザクションを次の方法で処理します。
    -   コミットされていない読み取り専用トランザクションの場合は、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行する SQL ステートメントは拒否されます。
    -   データが変更されたコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードが有効になると、ユーザーに明示的に`RESTRICTED_REPLICA_WRITER_ADMIN`権限が付与されない限り、すべてのユーザー ( `SUPER`権限を持つユーザーを含む) はデータを書き込む可能性のある SQL ステートメントを実行できなくなります。

### tidb_retry_limit {#tidb-retry-limit}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、楽観的トランザクションの最大再試行数を設定するために使用されます。トランザクションで再試行可能なエラー (トランザクションの競合、トランザクションのコミットが非常に遅い、テーブル スキーマの変更など) が発生すると、このトランザクションはこの変数に従って再実行されます。 `tidb_retry_limit` ～ `0`を設定すると、自動リトライが無効になることに注意してください。この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。

### tidb_row_format_version {#tidb-row-format-version}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   テーブルに新しく保存されたデータの形式バージョンを制御します。 TiDB v4.0 では、新しいデータを保存するためにデフォルトで[新しいstorage行フォーマット](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md)バージョン`2`が使用されます。
-   v4.0.0 より前の TiDB バージョンから v4.0.0 以降のバージョンにアップグレードする場合、形式のバージョンは変更されず、TiDB は引き続きバージョン`1`の古い形式を使用して**テーブル**にデータを書き込みます。**作成されたクラスターは、デフォルトで新しいデータ形式を使用します**。
-   この変数を変更しても、保存されている古いデータには影響しませんが、対応するバージョン形式は、この変数を変更した後に新しく書き込まれたデータにのみ適用されることに注意してください。

### tidb_scatter_region {#tidb-scatter-region}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   デフォルトでは、TiDB での新しいテーブルの作成時にリージョンが分割されます。この変数を有効にすると、新しく分割されたリージョンは`CREATE TABLE`ステートメントの実行中にすぐに分散されます。これは、テーブルがバッチで作成された直後にデータをバッチで書き込む必要があるシナリオに当てはまります。これは、新しく分割されたリージョンを事前に TiKV に分散させることができ、PD によるスケジュールを待つ必要がないためです。バッチでのデータ書き込みの継続的な安定性を確保するために、 `CREATE TABLE`ステートメントはリージョンが正常に分散された後にのみ成功を返します。これにより、ステートメントの実行時間は、この変数を無効にした場合よりも数倍長くなります。
-   テーブルの作成時に`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`を設定した場合、テーブル作成後に指定された数のリージョンが均等に分割されることに注意してください。

### tidb_server_memory_limit <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `80%`
-   範囲：
    -   値はパーセント形式で設定できます。これは、合計メモリに対するメモリ使用量のパーセントを意味します。値の範囲は`[1%, 99%]`です。
    -   メモリサイズに値を設定することもできます。値の範囲はバイト単位で`0`から`[536870912, 9223372036854775807]`です。 「KB|MB|GB|TB」単位のメモリ形式がサポートされています。 `0`メモリ制限がないことを意味します。
    -   この変数が`0`ではなく 512 MB 未満のメモリサイズに設定されている場合、TiDB は実際のサイズとして 512 MB を使用します。
-   この変数は、TiDB インスタンスのメモリ制限を指定します。 TiDB のメモリ使用量が制限に達すると、TiDB は現在実行中のメモリ使用量が最も高い SQL ステートメントをキャンセルします。 SQL ステートメントが正常にキャンセルされると、TiDB はGolang GC を呼び出して直ちにメモリを再利用し、できるだけ早くメモリのストレスを軽減しようとします。
-   メモリ使用量が制限[`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)を超えている SQL ステートメントのみが、最初にキャンセルされる SQL ステートメントとして選択されます。
-   現在、TiDB は一度に 1 つの SQL ステートメントのみをキャンセルします。 TiDB が SQL ステートメントを完全にキャンセルしてリソースを回復した後、メモリ使用量がまだこの変数で設定された制限を超えている場合、TiDB は次のキャンセル操作を開始します。

### tidb_server_memory_limit_gc_trigger <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-gc-trigger-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `70%`
-   範囲: `[50%, 99%]`
-   TiDB が GC をトリガーしようとするしきい値。 TiDB のメモリ使用量が`tidb_server_memory_limit` * `tidb_server_memory_limit_gc_trigger`の値に達すると、TiDB はGolang GC 操作をアクティブにトリガーします。 1 分間にトリガーされる GC 操作は 1 つだけです。

### tidb_server_memory_limit_sess_min_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-sess-min-size-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `134217728` (128 MB)
-   範囲: `[128, 9223372036854775807]` (バイト単位)。 「KB|MB|GB|TB」単位のメモリ形式もサポートされています。
-   メモリ制限を有効にすると、TiDB は現在のインスタンスでメモリ使用量が最も多い SQL ステートメントを終了します。この変数は、終了する SQL ステートメントの最小メモリ使用量を指定します。メモリ使用量が少ないセッションが多すぎることが原因で TiDB インスタンスのメモリ使用量が制限を超えている場合は、この変数の値を適切に下げて、より多くのセッションをキャンセルできるようにすることができます。

### <code>tidb_session_plan_cache_size</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-session-plan-cache-size-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は、キャッシュできるプランの最大数を制御します。 [準備されたプランのキャッシュ](/sql-prepared-plan-cache.md)と[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)同じキャッシュを共有します。
-   以前のバージョンから v7.1.0 以降のバージョンにアップグレードすると、この変数は[`tidb_prepared_plan_cache_size`](#tidb_prepared_plan_cache_size-new-in-v610)と同じ値のままになります。

### tidb_shard_allocate_step <span class="version-mark">v5.0 の新機能</span> {#tidb-shard-allocate-step-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `9223372036854775807`
-   範囲: `[1, 9223372036854775807]`
-   この変数は、 [`AUTO_RANDOM`](/auto-random.md)または[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)属性に割り当てられる連続 ID の最大数を制御します。通常、 `AUTO_RANDOM` ID または注釈付きの`SHARD_ROW_ID_BITS`の行 ID は、1 つのトランザクション内で増分され、連続します。この変数を使用すると、大規模なトランザクション シナリオにおけるホットスポットの問題を解決できます。

### tidb_simplified_metrics {#tidb-simplified-metrics}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数が有効な場合、TiDB は Grafana パネルで使用されないメトリクスを収集または記録しません。

### tidb_skip_ascii_check <span class="version-mark">v5.0 の新機能</span> {#tidb-skip-ascii-check-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ASCII 検証をスキップするかどうかを設定するために使用されます。
-   ASCII 文字の検証はパフォーマンスに影響します。入力文字が有効な ASCII 文字であることが確実な場合は、変数値を`ON`に設定できます。

### tidb_skip_isolation_level_check {#tidb-skip-isolation-level-check}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   このスイッチを有効にした後、TiDB でサポートされていない分離レベルが`tx_isolation`に割り当てられた場合、エラーは報告されません。これは、異なる分離レベルを設定する (ただし依存しない) アプリケーションとの互換性を向上させるのに役立ちます。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_utf8_check {#tidb-skip-utf8-check}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、UTF-8 検証をスキップするかどうかを設定するために使用されます。
-   UTF-8 文字の検証はパフォーマンスに影響します。入力文字が有効な UTF-8 文字であることが確実な場合は、変数値を`ON`に設定できます。

> **注記：**
>
> 文字チェックがスキップされると、TiDB はアプリケーションによって書き込まれた不正な UTF-8 文字の検出に失敗し、 `ANALYZE`の実行時にデコード エラーが発生し、その他の不明なエンコードの問題が発生する可能性があります。アプリケーションが書き込まれた文字列の正当性を保証できない場合は、文字チェックをスキップすることはお勧めできません。

### tidb_slow_log_threshold {#tidb-slow-log-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに永続化: いいえ、接続している現在の TiDB インスタンスにのみ適用されます。
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[-1, 9223372036854775807]`
-   単位: ミリ秒
-   この変数は、スローログの消費時間の閾値を出力するために使用されます。クエリの所要時間がこの値よりも長い場合、そのクエリはスローログとみなされ、スロークエリログにログが出力されます。

### tidb_slow_query_file {#tidb-slow-query-file}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション
-   デフォルト値: &quot;&quot;
-   `INFORMATION_SCHEMA.SLOW_QUERY`がクエリされると、構成ファイルの`slow-query-file`で設定されたスロー クエリ ログ名のみが解析されます。デフォルトのスロークエリログ名は「tidb-slow.log」です。他のログを解析するには、セッション変数`tidb_slow_query_file`を特定のファイル パスに設定し、クエリ`INFORMATION_SCHEMA.SLOW_QUERY`を実行して、設定されたファイル パスに基づいてスロー クエリ ログを解析します。

<CustomContent platform="tidb">

詳細は[遅いクエリを特定する](/identify-slow-queries.md)を参照してください。

</CustomContent>

### tidb_スナップショット {#tidb-snapshot}

-   範囲: セッション
-   デフォルト値: &quot;&quot;
-   この変数は、セッションによってデータが読み取られる時点を設定するために使用されます。たとえば、変数を「2017-11-11 20:20:20」または「400036290571534337」のような TSO 番号に設定すると、現在のセッションはこの時点のデータを読み取ります。

### tidb_source_id <span class="version-mark">v6.5.0 の新機能</span> {#tidb-source-id-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 15]`

<CustomContent platform="tidb">

-   この変数は、 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)クラスター内でさまざまなクラスター ID を構成するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [双方向レプリケーション](https://docs.pingcap.com/tidb/stable/ticdc-bidirectional-replication)クラスター内でさまざまなクラスター ID を構成するために使用されます。

</CustomContent>

### tidb_stats_cache_mem_quota <span class="version-mark">v6.1.0 の新機能</span> {#tidb-stats-cache-mem-quota-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> この変数は実験的機能です。本番環境での使用はお勧めできません。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 1099511627776]`
-   この変数は、TiDB 統計キャッシュのメモリ割り当てを設定します。

### tidb_stats_load_pseudo_timeout <span class="version-mark">v5.4.0 の新機能</span> {#tidb-stats-load-pseudo-timeout-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、SQL 最適化の待機時間がタイムアウトに達し、完全な列統計を同期的にロードするときに TiDB がどのように動作するかを制御します。デフォルト値`ON`は、タイムアウト後に SQL 最適化が擬似統計の使用に戻ることを意味します。この変数を`OFF`に設定すると、タイムアウト後に SQL の実行が失敗します。

### tidb_stats_load_sync_wait <span class="version-mark">v5.4.0 の新機能</span> {#tidb-stats-load-sync-wait-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   この変数は、統計の同期読み込み機能を有効にするかどうかを制御します。値`0` 、機能が無効であることを意味します。この機能を有効にするには、この変数を、SQL 最適化が完全な列統計を同期的にロードするまで待機できるタイムアウト (ミリ秒単位) に設定できます。詳細は[負荷統計](/statistics.md#load-statistics)を参照してください。

### tidb_stmt_summary_enable_persistent <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-enable-persistent-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントの概要の永続化は実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   範囲: グローバル
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)を有効にするかどうかを制御します。

<CustomContent platform="tidb">

-   この変数の値は、設定項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_filename <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-filename-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントの概要の永続化は実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   範囲: グローバル
-   タイプ: 文字列
-   デフォルト値: `"tidb-statements.log"`
-   この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に永続データが書き込まれるファイルを指定します。

<CustomContent platform="tidb">

-   この変数の値は、設定項目[`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_backups <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-file-max-backups-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントの概要の永続化は実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   範囲: グローバル
-   タイプ: 整数
-   デフォルト値: `0`
-   この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に保持できるデータ ファイルの最大数を指定します。

<CustomContent platform="tidb">

-   この変数の値は、設定項目[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_days <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-file-max-days-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントの概要の永続化は実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   範囲: グローバル
-   タイプ: 整数
-   デフォルト値: `3`
-   単位：日
-   この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合、永続データ ファイルを保持する最大日数を指定します。

<CustomContent platform="tidb">

-   この変数の値は、設定項目[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_size <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-file-max-size-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントの概要の永続化は実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

-   範囲: グローバル
-   タイプ: 整数
-   デフォルト値: `64`
-   単位: MiB
-   この変数は読み取り専用です。 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合、永続データ ファイルの最大サイズを指定します。

<CustomContent platform="tidb">

-   この変数の値は、設定項目[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_history_size <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-history-size-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `24`
-   範囲: `[0, 255]`
-   この変数は、履歴容量を[ステートメント概要テーブル](/statement-summary-tables.md)に設定するために使用されます。

### tidb_stmt_summary_internal_query <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-internal-query-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB の SQL 情報を[ステートメント概要テーブル](/statement-summary-tables.md)に含めるかどうかを制御するために使用されます。

### tidb_stmt_summary_max_sql_length <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-max-sql-length-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `4096`
-   範囲: `[0, 2147483647]`
-   この変数は、 [ステートメント概要テーブル](/statement-summary-tables.md)の SQL 文字列の長さを制御するために使用されます。

### tidb_stmt_summary_max_stmt_count <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-max-stmt-count-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `3000`
-   範囲: `[1, 32767]`
-   この変数は、メモリに保存[ステートメント概要テーブル](/statement-summary-tables.md)ステートメントの最大数を設定するために使用されます。

### tidb_stmt_summary_refresh_interval <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-refresh-interval-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1800`
-   範囲: `[1, 2147483647]`
-   単位: 秒
-   この変数は、リフレッシュ時間を[ステートメント概要テーブル](/statement-summary-tables.md)に設定するために使用されます。

### tidb_store_batch_size {#tidb-store-batch-size}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[0, 25000]`
-   この変数は、 `IndexLookUp`オペレーターのコプロセッサータスクのバッチ サイズを制御するために使用されます。 `0`バッチを無効にすることを意味します。タスクの数が比較的多く、クエリが遅い場合は、この変数を増やしてクエリを最適化できます。

### tidb_store_limit <span class="version-mark">v3.0.4 および v4.0 の新機能</span> {#tidb-store-limit-span-class-version-mark-new-in-v3-0-4-and-v4-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、TiDB が TiKV に同時に送信できるリクエストの最大数を制限するために使用されます。 0 は制限がないことを意味します。

### tidb_streamagg_concurrency {#tidb-streamagg-concurrency}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   この変数は、クエリ実行時の`StreamAgg`演算子の同時実行性を設定します。
-   この変数を設定すること**はお勧めできません**。変数値を変更すると、データの正確性の問題が発生する可能性があります。

### tidb_super_read_only <span class="version-mark">v5.3.1 の新機能</span> {#tidb-super-read-only-span-class-version-mark-new-in-v5-3-1-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_super_read_only` MySQL 変数`super_read_only`の置き換えとして実装されることを目的としています。ただし、TiDB は分散データベースであるため、 `tidb_super_read_only`実行直後にデータベースを読み取り専用にするのではなく、最終的には読み取り専用になります。
-   `SUPER`または`SYSTEM_VARIABLES_ADMIN`権限を持つユーザーは、この変数を変更できます。
-   この変数は、クラスター全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスター全体のすべての TiDB サーバーは読み取り専用モードになります。この場合、TiDB は、 `SELECT` 、 `USE` 、 `SHOW`など、データを変更しないステートメントのみを実行します。 `INSERT`や`UPDATE`などの他のステートメントの場合、TiDB は読み取り専用モードでのそれらのステートメントの実行を拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスター全体が最終的に読み取り専用ステータスになることだけが保証されます。 TiDB クラスターでこの変数の値を変更したが、その変更がまだ他の TiDB サーバーに反映されていない場合、更新されていない TiDB サーバーは**依然として**読み取り専用モードになっていません。
-   TiDB は、SQL ステートメントが実行される前に読み取り専用フラグをチェックします。 v6.2.0 以降、SQL ステートメントがコミットされる前にフラグもチェックされます。これは、サーバーが読み取り専用モードになった後に、長時間実行される[自動コミット](/transaction-overview.md#autocommit)ステートメントによってデータが変更される可能性がある場合を防ぐのに役立ちます。
-   この変数が有効な場合、TiDB はコミットされていないトランザクションを次の方法で処理します。
    -   コミットされていない読み取り専用トランザクションの場合は、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行する SQL ステートメントは拒否されます。
    -   データが変更されたコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードが有効になると、ユーザーに明示的に`RESTRICTED_REPLICA_WRITER_ADMIN`権限が付与されない限り、すべてのユーザー ( `SUPER`権限を持つユーザーを含む) はデータを書き込む可能性のある SQL ステートメントを実行できなくなります。
-   システム変数[`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520) `ON`に設定されている場合、場合によっては`tidb_super_read_only` [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の影響を受けることがあります。詳細な影響については、 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の説明を参照してください。

### tidb_sysdate_is_now <span class="version-mark">v6.0.0 の新機能</span> {#tidb-sysdate-is-now-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `SYSDATE`機能を`NOW`機能で置き換えることができるかどうかを制御するために使用されます。この設定項目は、MySQL オプション[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。

### tidb_sysproc_scan_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-sysproc-scan-concurrency-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、TiDB が内部 SQL ステートメント (統計の自動更新など) を実行するときに実行されるスキャン操作の同時実行性を設定するために使用されます。

### tidb_table_cache_lease <span class="version-mark">v6.0.0 の新機能</span> {#tidb-table-cache-lease-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `3`
-   範囲: `[1, 10]`
-   単位: 秒
-   この変数は、リース時間を[キャッシュされたテーブル](/cached-tables.md)に制御するために使用され、デフォルト値は`3`です。この変数の値は、キャッシュされたテーブルの変更に影響します。キャッシュされたテーブルに変更が加えられた後、最長の待機時間が`tidb_table_cache_lease`秒になる場合があります。テーブルが読み取り専用である場合、または高い書き込みレイテンシーを許容できる場合は、この変数の値を増やしてテーブルをキャッシュする有効時間を増やし、リース更新の頻度を減らすことができます。

### tidb_tmp_table_max_size <span class="version-mark">v5.3.0 の新機能</span> {#tidb-tmp-table-max-size-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[1048576, 137438953472]`
-   単位: バイト
-   この変数は、単一の[一時テーブル](/temporary-tables.md)の最大サイズを設定するために使用されます。この変数値よりも大きいサイズの一時テーブルではエラーが発生します。

### tidb_top_sql_max_meta_count <span class="version-mark">v6.0.0 の新機能</span> {#tidb-top-sql-max-meta-count-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `5000`
-   範囲: `[1, 10000]`

<CustomContent platform="tidb">

-   この変数は、収集される SQL ステートメント タイプの最大数を[Top SQL](/dashboard/top-sql.md)分あたり 1 つずつ制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、収集される SQL ステートメント タイプの最大数を[Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)分あたり 1 つずつ制御するために使用されます。

</CustomContent>

### tidb_top_sql_max_time_series_count <span class="version-mark">v6.0.0 の新機能</span> {#tidb-top-sql-max-time-series-count-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

> **注記：**
>
> 現在、TiDB ダッシュボードの[Top SQL]ページには、負荷に最も寄与する上位 5 種類の SQL クエリのみが表示されますが、これは`tidb_top_sql_max_time_series_count`の構成とは無関係です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 5000]`

<CustomContent platform="tidb">

-   この変数は、負荷に最も寄与する SQL ステートメント (つまり、上位 N) を 1 分あたり[Top SQL](/dashboard/top-sql.md)ずつ記録できる数を制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、負荷に最も寄与する SQL ステートメント (つまり、上位 N) を 1 分あたり[Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)ずつ記録できる数を制御するために使用されます。

</CustomContent>

### tidb_track_aggregate_memory_usage {#tidb-track-aggregate-memory-usage}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB が集計関数のメモリ使用量を追跡するかどうかを制御します。

> **警告：**
>
> この変数を無効にすると、TiDB はメモリ使用量を正確に追跡できなくなり、対応する SQL ステートメントのメモリ使用量を制御できなくなる可能性があります。

### tidb_tso_client_batch_max_wait_time <span class="version-mark">v5.3.0 の新機能</span> {#tidb-tso-client-batch-max-wait-time-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 10]`
-   単位: ミリ秒
-   この変数は、TiDB が PD から TSO を要求するときのバッチ操作の最大待ち時間を設定するために使用されます。デフォルト値は`0`で、追加の待ち時間がないことを意味します。
-   TiDB が使用する PD Client は、毎回 PD から TSO リクエストを取得する際に、同時に受信した TSO リクエストをできるだけ多く収集します。次に、PD Client は、収集したリクエストを 1 つの RPC リクエストにまとめて PD に送信します。これは PD へのプレッシャーを軽減するのに役立ちます。
-   この変数を`0`より大きい値に設定すると、TiDB は各バッチ マージの終了前にこの値の最大期間待機します。これは、より多くの TSO 要求を収集し、バッチ操作の効果を向上させるためです。
-   この変数の値を増やすシナリオ:
    -   TSO 要求の負荷が高いため、PD リーダーの CPU がボトルネックに達し、TSO RPC 要求のレイテンシーが長くなります。
    -   クラスター内の TiDB インスタンスはそれほど多くありませんが、すべての TiDB インスタンスは高い同時実行性を持っています。
-   この変数をできるだけ小さい値に設定することをお勧めします。

> **注記：**
>
> PD リーダーの CPU 使用率のボトルネック以外の理由 (ネットワークの問題など) で TSO RPCレイテンシーが増加すると仮定します。この場合、値`tidb_tso_client_batch_max_wait_time`を増やすと、TiDB での実行レイテンシーが増加し、クラスターの QPS パフォーマンスに影響を与える可能性があります。

### tidb_ttl_delete_rate_limit <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-rate-limit-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、各 TiDB ノード上の TTL ジョブの`DELETE`ステートメントのレートを制限するために使用されます。この値は、TTL ジョブの単一ノードで 1 秒あたりに許可される`DELETE`のステートメントの最大数を表します。この変数が`0`に設定されている場合、制限は適用されません。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_delete_batch_size <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `100`
-   範囲: `[1, 10240]`
-   この変数は、TTL ジョブの`DELETE`つのトランザクションで削除できる最大行数を設定するために使用されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_delete_worker_count <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各 TiDB ノードでの TTL ジョブの最大同時実行数を設定するために使用されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_job_enable <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-enable-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、TTL ジョブを有効にするかどうかを制御するために使用されます。これを`OFF`に設定すると、TTL 属性を持つすべてのテーブルが期限切れデータのクリーンアップを自動的に停止します。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_scan_batch_size <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-scan-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `500`
-   範囲: `[1, 10240]`
-   この変数は、TTL ジョブの期限切れデータのスキャンに使用される各`SELECT`ステートメントの`LIMIT`値を設定するために使用されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_scan_worker_count <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-scan-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各 TiDB ノードでの TTL スキャン ジョブの最大同時実行数を設定するために使用されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_job_schedule_window_start_time <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-schedule-window-start-time-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   タイプ: 時間
-   クラスターへの永続化: はい
-   デフォルト値: `00:00 +0000`
-   この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの開始時間を制御するために使用されます。この変数の値を変更する場合は、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_job_schedule_window_end_time <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-schedule-window-end-time-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   タイプ: 時間
-   クラスターへの永続化: はい
-   デフォルト値: `23:59 +0000`
-   この変数は、バックグラウンドで TTL ジョブのスケジュール ウィンドウの終了時間を制御するために使用されます。この変数の値を変更する場合は、ウィンドウが小さいと期限切れデータのクリーンアップが失敗する可能性があることに注意してください。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_running_tasks <span class="version-mark">v7.0.0 の新機能</span> {#tidb-ttl-running-tasks-span-class-version-mark-new-in-v7-0-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `-1`と`[1, 256]`
-   クラスター全体で実行中の TTL タスクの最大数を指定します。 `-1` TTL タスクの数が TiKV ノードの数と等しいことを意味します。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_txn_assertion_level <span class="version-mark">v6.0.0 の新機能</span> {#tidb-txn-assertion-level-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション |グローバル

-   クラスターへの永続化: はい

-   タイプ: 列挙型

-   デフォルト値: `FAST`

-   可能な値: `OFF` 、 `FAST` 、 `STRICT`

-   この変数はアサーション レベルを制御するために使用されます。アサーションは、データとインデックス間の整合性チェックであり、書き込まれるキーがトランザクションのコミット プロセスに存在するかどうかをチェックします。詳細については、 [データとインデックス間の不一致のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)を参照してください。

    -   `OFF` : このチェックを無効にします。
    -   `FAST` : ほとんどのチェック項目を有効にし、パフォーマンスにほとんど影響を与えません。
    -   `STRICT` : すべてのチェック項目を有効にします。システムのワークロードが高い場合、悲観的トランザクションのパフォーマンスにわずかな影響を与えます。

-   v6.0.0 以降のバージョンの新しいクラスターの場合、デフォルト値は`FAST`です。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_txn_commit_batch_size <span class="version-mark">v6.2.0 の新機能</span> {#tidb-txn-commit-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `16384`
-   範囲: `[1, 1073741824]`
-   単位: バイト

<CustomContent platform="tidb">

-   この変数は、TiDB が TiKV に送信するトランザクション コミット リクエストのバッチ サイズを制御するために使用されます。アプリケーション ワークロード内のほとんどのトランザクションで多数の書き込み操作が行われる場合、この変数をより大きな値に調整すると、バッチ処理のパフォーマンスが向上する可能性があります。ただし、この変数の設定値が大きすぎて TiKV の[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)の制限を超えると、コミットが失敗する可能性があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB が TiKV に送信するトランザクション コミット リクエストのバッチ サイズを制御するために使用されます。アプリケーション ワークロード内のほとんどのトランザクションで多数の書き込み操作が行われる場合、この変数をより大きな値に調整すると、バッチ処理のパフォーマンスが向上する可能性があります。ただし、この変数の設定値が大きすぎて、TiKV の単一ログの最大サイズの制限 (デフォルトでは 8 MB) を超える場合、コミットが失敗する可能性があります。

</CustomContent>

### tidb_txn_mode {#tidb-txn-mode}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `pessimistic`
-   可能な値: `pessimistic` 、 `optimistic`
-   この変数はトランザクション モードを設定するために使用されます。 TiDB 3.0 は悲観的トランザクションをサポートします。 TiDB 3.0.8 以降、 [悲観的トランザクションモード](/pessimistic-transaction.md)デフォルトで有効になっています。
-   TiDB を v3.0.7 以前のバージョンから v3.0.8 以降のバージョンにアップグレードしても、デフォルトのトランザクション モードは変更されません。**新しく作成されたクラスタのみが、デフォルトで悲観的トランザクション モードを使用します**。
-   この変数が「楽観的」または「」に設定されている場合、TiDB は[楽観的トランザクションモード](/optimistic-transaction.md)を使用します。

### tidb_use_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-use-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、実行プラン バインディング機能を有効にするかどうかを制御するために使用されます。これはデフォルトで有効になっていますが、値`OFF`を割り当てることで無効にできます。実行計画バインディングの使用方法については、 [実行計画のバインド](/sql-plan-management.md#create-a-binding)を参照してください。

### tidb_wait_split_region_finish {#tidb-wait-split-region-finish}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション
-   タイプ: ブール値
-   デフォルト値: `ON`
-   通常、リージョンを分散するには長い時間がかかりますが、これは PD スケジューリングと TiKV 負荷によって決まります。この変数は、 `SPLIT REGION`ステートメントの実行時にすべてのリージョンが完全に分散された後に結果をクライアントに返すかどうかを設定するために使用されます。
    -   `ON`では、すべてのリージョンが分散されるまで`SPLIT REGIONS`ステートメントが待機する必要があります。
    -   `OFF`指定すると、すべてのリージョンの分散が完了する前に`SPLIT REGIONS`ステートメントが戻ることが許可されます。
-   リージョンを分散すると、分散されているリージョンの書き込みおよび読み取りのパフォーマンスが影響を受ける可能性があることに注意してください。バッチ書き込みまたはデータのインポートのシナリオでは、リージョンの分散が終了した後にデータをインポートすることをお勧めします。

### tidb_wait_split_region_timeout {#tidb-wait-split-region-timeout}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[1, 2147483647]`
-   単位: 秒
-   この変数は、 `SPLIT REGION`ステートメントの実行のタイムアウトを設定するために使用されます。指定された時間値内にステートメントが完全に実行されない場合は、タイムアウト エラーが返されます。

### tidb_window_concurrency <span class="version-mark">v4.0 の新機能</span> {#tidb-window-concurrency-span-class-version-mark-new-in-v4-0-span}

> **警告：**
>
> v5.0 以降、この変数は非推奨になりました。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用してください。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、ウィンドウ オペレーターの同時実行度を設定するために使用されます。
-   値`-1`は、値`tidb_executor_concurrency`が代わりに使用されることを意味します。

### tiflash_fastscan <span class="version-mark">v6.3.0 の新機能</span> {#tiflash-fastscan-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション |グローバル
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   [ファストスキャン](/tiflash/use-fastscan.md)が有効になっている ( `ON`に設定されている) 場合、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度やデータの一貫性は保証されません。

### tiflash_fine_graned_shuffle_batch_size <span class="version-mark">v6.2.0 の新機能</span> {#tiflash-fine-grained-shuffle-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション |グローバル
-   デフォルト値: `8192`
-   範囲: `[1, 18446744073709551615]`
-   Fine Grained Shuffle を有効にすると、 TiFlashにプッシュダウンされたウィンドウ関数を並列実行できます。この変数は、送信者によって送信されるデータのバッチ サイズを制御します。
-   パフォーマンスへの影響: ビジネス要件に応じて適切なサイズを設定します。設定を誤るとパフォーマンスに影響を与えます。値の設定が小さすぎる場合 (たとえば`1` )、ブロックごとに 1 回のネットワーク転送が発生します。テーブルの合計行数など、値が大きすぎると、受信側でデータの待機にほとんどの時間が費やされ、パイプライン計算が機能しなくなります。適切な値を設定するには、 TiFlashレシーバーが受信した行数の分布を観察します。ほとんどのスレッドが数行 (たとえば数百行) しか受信しない場合は、この値を増やすことでネットワークのオーバーヘッドを減らすことができます。

### tiflash_fine_graned_shuffle_stream_count <span class="version-mark">v6.2.0 の新機能</span> {#tiflash-fine-grained-shuffle-stream-count-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-1, 1024]`
-   ウィンドウ関数がTiFlashにプッシュダウンされて実行される場合、この変数を使用してウィンドウ関数実行の同時実行レベルを制御できます。可能な値は次のとおりです。

    -   -1: ファイン グレイン シャッフル機能は無効になります。 TiFlashにプッシュダウンされたウィンドウ関数はシングルスレッドで実行されます。
    -   0: ファイン グレイン シャッフル機能が有効になります。 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)が有効な値 (0 より大きい) に設定されている場合、 `tiflash_fine_grained_shuffle_stream_count`は[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)の値に設定されます。それ以外の場合は、8 に設定されますTiFlash上のウィンドウ関数の実際の同時実行レベルは、min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノード上の物理スレッドの数) です。
    -   0 より大きい整数: ファイン グレイン シャッフル機能が有効になります。 TiFlashにプッシュダウンされたウィンドウ関数はマルチスレッドで実行されます。同時実行レベルは次のとおりです: min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノード上の物理スレッドの数)。
-   理論的には、ウィンドウ関数のパフォーマンスはこの値に比例して増加します。ただし、この値が実際の物理スレッド数を超えると、かえってパフォーマンスの低下につながります。

### タイムゾーン {#time-zone}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `SYSTEM`
-   この変数は現在のタイムゾーンを返します。値は、「-8:00」などのオフセット、または名前付きゾーン「America/Los_Angeles」のいずれかとして指定できます。
-   値`SYSTEM` 、タイム ゾーンがシステム ホストと同じである必要があることを意味します。これは、変数[`system_time_zone`](#system_time_zone)で取得できます。

### タイムスタンプ {#timestamp}

-   範囲: セッション
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数の空でない値は、 `CURRENT_TIMESTAMP()` 、およびその他の関数のタイムスタンプとして使用`NOW()`れる UNIX エポックを示します。この変数は、データの復元またはレプリケーションで使用される可能性があります。

### トランザクション分離 {#transaction-isolation}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `REPEATABLE-READ`
-   可能な値: `READ-UNCOMMITTED` 、 `READ-COMMITTED` 、 `REPEATABLE-READ` 、 `SERIALIZABLE`
-   この変数はトランザクションの分離を設定します。 TiDB は MySQL との互換性のために`REPEATABLE-READ`を宣伝しますが、実際の分離レベルはスナップショット分離です。詳細については[トランザクション分離レベル](/transaction-isolation-levels.md)参照してください。

### tx_isolation {#tx-isolation}

この変数は`transaction_isolation`のエイリアスです。

### tx_isolation_one_shot {#tx-isolation-one-shot}

> **注記：**
>
> この変数は TiDB で内部的に使用されます。使用することは期待されていません。

内部的には、TiDB パーサーは`SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]`ステートメントを`SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`に変換します。

### tx_read_ts {#tx-read-ts}

-   範囲: セッション
-   デフォルト値: &quot;&quot;
-   ステイル読み取りシナリオでは、このセッション変数は、安定した読み取りのタイムスタンプ値を記録するために使用されます。
-   この変数は TiDB の内部操作に使用されます。この変数を設定すること**はお勧めできません**。

### txn_scope {#txn-scope}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション
-   デフォルト値: `global`
-   値のオプション: `global`および`local`
-   この変数は、現在のセッションのトランザクションがグローバル トランザクションであるかローカル トランザクションであるかを設定するために使用されます。
-   この変数は TiDB の内部操作に使用されます。この変数を設定すること**はお勧めできません**。

### validate_password.check_user_name <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-check-user-name-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、パスワード複雑さチェックのチェック項目です。パスワードがユーザー名と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効な場合にのみ有効になります。
-   この変数が有効で`ON`に設定されている場合、パスワードを設定すると、TiDB はパスワードとユーザー名 (ホスト名を除く) を比較します。パスワードがユーザー名と一致する場合、パスワードは拒否されます。
-   この変数は[`validate_password.policy`](#validate_passwordpolicy-new-in-v650)とは独立しており、パスワードの複雑さのチェック レベルの影響を受けません。

### validate_password.dictionary <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-dictionary-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `""`
-   タイプ: 文字列
-   この変数は、パスワード複雑さチェックのチェック項目です。パスワードが辞書と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`2` (STRONG) に設定されている場合にのみ有効です。
-   この変数は 1024 文字以内の文字列です。これには、パスワードに存在できない単語のリストが含まれています。各単語はセミコロン ( `;` ) で区切られます。
-   この変数はデフォルトで空の文字列に設定されます。これは、辞書チェックが実行されないことを意味します。辞書チェックを実行するには、一致する単語を文字列に含める必要があります。この変数が設定されている場合、パスワードを設定すると、TiDB はパスワードの各部分文字列 (4 ～ 100 文字の長さ) を辞書内の単語と比較します。パスワードの一部の文字列が辞書内の単語と一致する場合、パスワードは拒否されます。比較では大文字と小文字は区別されません。

### validate_password.enable <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-enable-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は常に[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)で有効になります。

-   範囲: グローバル
-   クラスターへの永続化: はい
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数が`ON`に設定されている場合、TiDB はパスワードの設定時にパスワードの複雑さのチェックを実行します。

### validate_password.length <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-length-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `8`
-   `[0, 2147483647]` : TiDB セルフホスト型の場合は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) 、 `[8, 2147483647]`
-   この変数は、パスワード複雑さチェックのチェック項目です。パスワードの長さが十分であるかどうかをチェックします。デフォルトでは、パスワードの最小長は`8`です。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効な場合にのみ有効になります。
-   この変数の値は、式`validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`より小さくてはなりません。
-   式の値が`validate_password.length`より大きくなるように`validate_password.number_count` 、 `validate_password.special_char_count` 、または`validate_password.mixed_case_count`の値を変更すると、式の値と一致するように`validate_password.length`の値が自動的に変更されます。

### validate_password.mixed_case_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-mixed-case-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   `[0, 2147483647]` : TiDB セルフホスト型の場合は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) 、 `[1, 2147483647]`
-   この変数は、パスワード複雑さチェックのチェック項目です。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。
-   パスワードの大文字の数も小文字の数も、値`validate_password.mixed_case_count`より少なくすることはできません。たとえば、変数が`1`に設定されている場合、パスワードには少なくとも 1 つの大文字と 1 つの小文字が含まれている必要があります。

### validate_password.number_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-number-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   `[0, 2147483647]` : TiDB セルフホスト型の場合は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) 、 `[1, 2147483647]`
-   この変数は、パスワード複雑さチェックのチェック項目です。パスワードに十分な数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。

### validate_password.policy <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-policy-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 列挙型
-   デフォルト値: `1`
-   値のオプション: TiDB セルフホストの場合は`0` 、 `1` 、および`2`および[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) 。 `1`と`2` [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合
-   この変数は、パスワードの複雑さチェックのポリシーを制御します。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効な場合にのみ有効になります。この変数の値によって`validate_password.check_user_name`を除く他の`validate-password`変数がパスワードの複雑さのチェックで有効になるかどうかが決まります。
-   この変数の値は`0` 、 `1` 、または`2` (LOW、MEDIUM、または STRONG に対応) です。ポリシー レベルが異なると、チェックも異なります。
    -   0 または LOW: パスワードの長さ。
    -   1 または MEDIUM: パスワードの長さ、大文字と小文字、数字、特殊文字。
    -   2 または STRONG: パスワードの長さ、大文字と小文字、数字、特殊文字、および辞書の一致。

### validate_password.special_char_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-special-char-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   `[0, 2147483647]` : TiDB セルフホスト型の場合は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) 、 `[1, 2147483647]`
-   この変数は、パスワード複雑さチェックのチェック項目です。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効です。

### バージョン {#version}

-   範囲: なし
-   デフォルト値: `5.7.25-TiDB-` (tidb バージョン)
-   この変数は MySQL バージョンを返し、その後に TiDB バージョンを返します。たとえば、「5.7.25-TiDB-v7.1.0」です。

### バージョン_コメント {#version-comment}

-   範囲: なし
-   デフォルト値: (文字列)
-   この変数は、TiDB バージョンに関する追加の詳細を返します。たとえば、「TiDB サーバー (Apache License 2.0) Community Edition、 MySQL 5.7互換」などです。

### version_compile_machine {#version-compile-machine}

-   範囲: なし
-   デフォルト値: (文字列)
-   この変数は、TiDB が実行されている CPUアーキテクチャの名前を返します。

### version_compile_os {#version-compile-os}

-   範囲: なし
-   デフォルト値: (文字列)
-   この変数は、TiDB が実行されている OS の名前を返します。

### wait_timeout {#wait-timeout}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して読み取り専用です。

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[0, 31536000]`
-   単位: 秒
-   この変数は、ユーザー セッションのアイドル タイムアウトを制御します。ゼロ値は無制限を意味します。

### warning_count {#warning-count}

-   範囲: セッション
-   デフォルト値: `0`
-   この読み取り専用変数は、以前に実行されたステートメントで発生した警告の数を示します。

### windowing_use_high_precision {#windowing-use-high-precision}

-   範囲: セッション |グローバル
-   クラスターへの永続化: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数を計算するときに高精度モードを使用するかどうかを制御します。
