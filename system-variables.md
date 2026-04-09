---
title: System Variables
summary: システム変数を使用して、パフォーマンスを最適化したり、実行時の動作を変更したりできます。
---

# システム変数 {#system-variables}

TiDBのシステム変数はMySQLと同様に、設定が`SESSION`または`GLOBAL`スコープで適用されるという点で類似した動作をします。

-   スコープ`SESSION`に対する変更は、現在のセッションのみに影響します。
-   スコープが`GLOBAL`の場合、変更は即座に反映されます。この変数がスコープ`SESSION`にも設定されている場合は、すべてのセッション（あなたのセッションを含む）で現在のセッション値が引き続き使用されます。
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
> いくつかの`GLOBAL`変数は TiDB クラスタに保持されます。このドキュメントにあるいくつかの変数には`Persists to cluster`設定があり、 `Yes`または`No`に設定できます。
>
> -   設定が`Persists to cluster: Yes`の変数については、グローバル変数が変更されると、すべてのTiDBサーバーに通知が送信され、システム変数キャッシュが更新されます。TiDBサーバーを追加したり、既存のTiDBサーバーを再起動したりすると、保存された設定値が自動的に使用されます。
> -   設定が`Persists to cluster: No`変数については、変更は接続先のローカルTiDBインスタンスにのみ適用されます。設定した値を保持するには、設定ファイル`tidb.toml`で変数を指定する必要があります。
>
> さらに、TiDBはいくつかのMySQL変数を読み取りと設定の両方が可能な変数として提供します。これは、アプリケーションとコネクタの両方がMySQL変数を読み取ることが一般的であるため、互換性のために必要です。たとえば、JDBCコネクタは、その動作に依存していないにもかかわらず、クエリキャッシュ設定の読み取りと設定の両方を行います。

> **注記：**
>
> 値が大きいほど必ずしもパフォーマンスが向上するとは限りません。また、ほとんどの設定は接続ごとに適用されるため、ステートメントを実行している同時接続数を考慮することも重要です。
>
> 安全な値を決定する際には、変数の単位を考慮してください。
>
> -   スレッドの場合、安全な値は通常、CPUコアの数までです。
> -   バイト単位の場合、安全な値は通常、システムメモリの量よりも小さくなります。
> -   時間を表す単位は秒またはミリ秒の場合があることに注意してください。
>
> 同じ単位を使用する変数は、同じリソースを巡って競合する可能性がある。

バージョン7.4.0以降では、 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)を使用してステートメントの実行中に`SESSION`変数の値を一時的に変更できます。ステートメントの実行後、現在のセッションのシステム変数の値は自動的に元の値に戻ります。このヒントは、オプティマイザとエグゼキュータに関連する一部のシステム変数を変更するために使用できます。このドキュメントの変数には`Applies to hint SET_VAR`設定があり、 `Yes`または`No`に設定できます。

-   設定が`Applies to hint SET_VAR: Yes`の変数については、 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)ヒントを使用して、ステートメントの実行中に現在のセッション内のシステム変数の値を変更できます。
-   設定が`Applies to hint SET_VAR: No`変数については、ステートメントの実行中に、 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)ヒントを使用して現在のセッションのシステム変数の値を変更することはできません。

ヒント`SET_VAR`詳細については、 [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)参照してください。

## 変数参照 {#variable-reference}

### allow_auto_random_explicit_insert <span class="version-mark">v4.0.3で追加</span> {#allow-auto-random-explicit-insert-span-class-version-mark-new-in-v4-0-3-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `INSERT`ステートメントで、 `AUTO_RANDOM`属性を持つ列の値を明示的に指定することを許可するかどうかを決定します。

### authentication_ldap_sasl_auth_method_name <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-sasl-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `SCRAM-SHA-1`
-   可能`GSSAPI`値： `SCRAM-SHA-1` `SCRAM-SHA-256`
-   LDAP SASL認証の場合、この変数は認証方法名を指定します。

### authentication_ldap_sasl_bind_base_dn は<span class="version-mark">v7.1.0 で追加されました。</span> {#authentication-ldap-sasl-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL認証の場合、この変数は検索ツリー内の検索範囲を制限します。1 `AS ...`を指定せずにユーザーを作成した場合、TiDBはユーザー名に基づいてLDAPサーバー内で`dn`を自動的に検索します。

### authentication_ldap_sasl_bind_root_dn は<span class="version-mark">v7.1.0 で追加されました。</span> {#authentication-ldap-sasl-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL認証の場合、この変数はLDAPサーバーにログインしてユーザーを検索するために使用される`dn`指定します。

### authentication_ldap_sasl_bind_root_pwd は<span class="version-mark">v7.1.0 で追加されました。</span> {#authentication-ldap-sasl-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL認証の場合、この変数はLDAPサーバーにログインしてユーザーを検索する際に使用するパスワードを指定します。

### authentication_ldap_sasl_ca_path <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-sasl-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL認証の場合、この変数はStartTLS接続用の認証局ファイルの絶対パスを指定します。

### authentication_ldap_sasl_init_pool_size <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-sasl-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP SASL認証の場合、この変数はLDAPサーバーへの接続プール内の初期接続を指定します。

### authentication_ldap_sasl_max_pool_size <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-sasl-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP SASL認証の場合、この変数はLDAPサーバーへの接続プール内の最大接続数を指定します。

### authentication_ldap_sasl_server_host <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-sasl-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL認証の場合、この変数はLDAPサーバーのホスト名またはIPアドレスを指定します。

### authentication_ldap_sasl_server_port <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-sasl-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP SASL認証の場合、この変数はLDAPサーバーのTCP/IPポート番号を指定します。

### authentication_ldap_sasl_tls <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-sasl-tls-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP SASL認証の場合、この変数は、プラグインによるLDAPサーバーへの接続がStartTLSで保護されるかどうかを制御します。

### authentication_ldap_simple_auth_method_name <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-simple-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `SIMPLE`
-   可能な値: `SIMPLE` 。
-   LDAP簡易認証の場合、この変数は認証方法名を指定します。サポートされている値は`SIMPLE`です。

### authentication_ldap_simple_bind_base_dn は<span class="version-mark">v7.1.0 で追加されました。</span> {#authentication-ldap-simple-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP シンプル認証の場合、この変数は検索ツリー内の検索範囲を制限します。1 `AS ...`を指定せずにユーザーを作成した場合、TiDB はユーザー名に基づいて LDAPサーバー内で`dn`を自動的に検索します。

### authentication_ldap_simple_bind_root_dn は<span class="version-mark">v7.1.0 で追加されました。</span> {#authentication-ldap-simple-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP簡易認証の場合、この変数はLDAPサーバーにログインしてユーザーを検索するために使用される`dn`指定します。

### authentication_ldap_simple_bind_root_pwd <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-simple-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP簡易認証の場合、この変数はLDAPサーバーにログインしてユーザーを検索する際に使用するパスワードを指定します。

### authentication_ldap_simple_ca_path <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-simple-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP簡易認証の場合、この変数はStartTLS接続用の認証局ファイルの絶対パスを指定します。

### authentication_ldap_simple_init_pool_size <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-simple-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP シンプル認証の場合、この変数は、LDAPサーバーへの接続プール内の初期接続を指定します。

### authentication_ldap_simple_max_pool_size <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-simple-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP シンプル認証の場合、この変数は、LDAPサーバーへの接続プール内の最大接続数を指定します。

### authentication_ldap_simple_server_host <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-simple-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP簡易認証の場合、この変数はLDAPサーバーのホスト名またはIPアドレスを指定します。

### authentication_ldap_simple_server_port <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-simple-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP シンプル認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### authentication_ldap_simple_tls <span class="version-mark">v7.1.0で追加</span> {#authentication-ldap-simple-tls-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP簡易認証の場合、この変数はプラグインによるLDAPサーバーへの接続をStartTLSで保護するかどうかを制御します。

### 自動インクリメントインクリメント {#auto-increment-increment}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てる値のステップサイズ（ `AUTO_INCREMENT`と、 `AUTO_RANDOM` IDの割り当てルールを制御します。auto_increment_offsetと[`auto_increment_offset`](#auto_increment_offset)て使用​​されることがよくあります。

### 自動インクリメントオフセット {#auto-increment-offset}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てる`AUTO_INCREMENT`値の初期オフセットと、 `AUTO_RANDOM` IDの割り当てルールを制御します。この設定は、 [`auto_increment_increment`](#auto_increment_increment)と組み合わせて使用​​されることがよくあります。例：

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

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   明示的なトランザクションにないときにステートメントを自動的にコミットするかどうかを制御します。詳細については、[トランザクション概要](/transaction-overview.md#autocommit)参照してください。

### ブロック暗号化モード {#block-encryption-mode}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `aes-128-ecb`
-   `aes-256-ecb` `aes-192-cbc` `aes-128-cbc` `aes-128-ecb` `aes-192-ecb` `aes-256-cbc` `aes-128-ofb` `aes-192-ofb` `aes-256-ofb` `aes-128-cfb` `aes-192-cfb` `aes-256-cfb`
-   この変数は、組み込み関数[`AES_ENCRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_encrypt)および[`AES_DECRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_decrypt)の暗号化モードを設定します。

### 文字セットクライアント {#character-set-client}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `utf8mb4`
-   クライアントから送信されるデータの文字セット。 TiDB での文字セットと照合順序の使用の詳細については、[文字セットと照合](/character-set-and-collation.md)を参照してください。必要に応じて、 [`SET NAMES`](/sql-statements/sql-statement-set-names.md)を使用して文字セットを変更することをお勧めします。

### 文字セット接続 {#character-set-connection}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `utf8mb4`
-   文字セットが指定されていない文字列リテラルに使用される文字セット。

### 文字セットデータベース {#character-set-database}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `utf8mb4`
-   この変数は、現在使用されているデフォルトデータベースの文字セットを示します。**この変数を設定することは推奨されません**。新しいデフォルトデータベースが選択されると、サーバーはこの変数の値を変更します。

### 文字セット結果 {#character-set-results}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `utf8mb4`
-   クライアントにデータを送信する際に使用される文字セット。

### 文字セットサーバー {#character-set-server}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `utf8mb4`
-   サーバーのデフォルトの文字セット。

### 照合接続 {#collation-connection}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `utf8mb4_bin`
-   この変数は、現在の接続で使用されている照合順序を示します。これは、MySQL 変数`collation_connection`と一致します。

### 照合データベース {#collation-database}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `utf8mb4_bin`
-   この変数は、使用中のデータベースのデフォルトの照合照合順序を示します。**この変数を設定することは推奨されません**。新しいデータベースが選択されると、TiDBはこの変数の値を変更します。

### 照合サーバー {#collation-server}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `utf8mb4_bin`
-   データベース作成時にデフォルトで使用される照合照合順序。

### cte_max_recursion_depth {#cte-max-recursion-depth}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `1000`
-   範囲: `[0, 4294967295]`
-   共通テーブル式における最大再帰深度を制御します。

### データディレクトリ {#datadir}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)ではサポートされていません。

<CustomContent platform="tidb">

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値：コンポーネントとデプロイ方法によって異なります。
    -   `/tmp/tidb` : [`--store`](/command-line-flags-for-tidb-configuration.md#--store)に`"unistore"`設定した場合、または`--store`設定しなかった場合。
    -   `${pd-ip}:${pd-port}` : TiKV を使用する場合。TiKV は、Kubernetes デプロイメント用のTiUPおよびTiDB Operator のデフォルトのstorageエンジンです。
-   この変数は、データが保存されている場所を示します。この場所は、ローカルパス`/tmp/tidb`を指定することも、データがTiKVに保存されている場合はPDサーバーを指すこともできます。3の形式の値は`${pd-ip}:${pd-port}` TiDBが起動時に接続するPDサーバーを示します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値：コンポーネントとデプロイ方法によって異なります。
    -   `/tmp/tidb` : [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store)に`"unistore"`設定した場合、または`--store`設定しなかった場合。
    -   `${pd-ip}:${pd-port}` : TiKV を使用する場合。TiKV は、Kubernetes デプロイメント用のTiUPおよびTiDB Operator のデフォルトのstorageエンジンです。
-   この変数は、データが保存されている場所を示します。この場所は、ローカルパス`/tmp/tidb`を指定することも、データがTiKVに保存されている場合はPDサーバーを指すこともできます。3の形式の値は`${pd-ip}:${pd-port}` TiDBが起動時に接続するPDサーバーを示します。

</CustomContent>

### ddl_slow_threshold {#ddl-slow-threshold}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `300`
-   範囲: `[0, 2147483647]`
-   単位：ミリ秒
-   実行時間がしきい値を超えたDDL操作をログに記録する。

### デフォルト認証プラグイン {#default-authentication-plugin}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `mysql_native_password`
-   `authentication_ldap_simple` `tidb_auth_token` `caching_sha2_password` `tidb_sm3_password` `mysql_native_password` `authentication_ldap_sasl`
-   この変数は、サーバーとクライアント間の接続が確立される際にサーバーが通知する認証方法を設定します。
-   `tidb_sm3_password`方法で認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)を使用してTiDBに接続できます。

<CustomContent platform="tidb">

この変数の可能な値の詳細については、 [認証プラグインの状態](/security-compatibility-with-mysql.md#authentication-plugin-status)を参照してください。

</CustomContent>

### default_collat​​ion_for_utf8mb4 <span class="version-mark">v7.4.0で追加</span> {#default-collation-for-utf8mb4-span-class-version-mark-new-in-v7-4-0-span}

-   範囲：グローバル | セッション
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: `utf8mb4_bin`
-   `utf8mb4_0900_ai_ci` `utf8mb4_general_ci` ： `utf8mb4_bin`
-   この変数は、 `utf8mb4`文字セットのデフォルト[照合順序](/character-set-and-collation.md)を設定するために使用されます。これは、以下のステートメントの動作に影響します。
    -   [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)および[`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)ステートメントに表示されるデフォルトの照合順序。
    -   [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)および[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)ステートメントで、テーブルまたは列に対して`CHARACTER SET utf8mb4`句が指定されているにもかかわらず照合順序が指定されていない場合、この変数で指定された照合順序が使用されます。これは、 `CHARACTER SET`句が使用されていない場合の動作には影響しません。
    -   [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)および[`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)ステートメントに、照合順序を指定しない`CHARACTER SET utf8mb4`句が含まれている場合、この変数で指定された照合順序が使用されます。これは、 `CHARACTER SET`句を使用しない場合の動作には影響しません。
    -   `COLLATE`句が使用されない場合、 `_utf8mb4'string'`の形式のリテラル文字列はすべて、この変数で指定された照合順序を使用します。

### default_password_lifetime <span class="version-mark">v6.5.0で追加</span> {#default-password-lifetime-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 65535]`
-   パスワードの自動有効期限に関するグローバルポリシーを設定します。デフォルト値の`0`パスワードの有効期限がないことを示します。このシステム変数を正の整数`N`に設定すると、パスワードの有効期間は`N`日間となり、 `N`日以内にパスワードを変更する必要があります。

### デフォルトの週フォーマット {#default-week-format}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 7]`
-   `WEEK()`関数で使用される週の形式を設定します。

### パスワード期限切れ時の切断機能<span class="version-mark">(v6.5.0 で追加)</span> {#disconnect-on-expired-password-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は読み取り専用です。パスワードの有効期限が切れたときに、TiDBがクライアント接続を切断するかどうかを示します。変数が`ON`に設定されている場合、パスワードの有効期限が切れるとクライアント接続が切断されます。変数が`OFF`に設定されている場合、クライアント接続は「サンドボックスモード」に制限され、ユーザーはパスワードリセット操作のみを実行できます。

<CustomContent platform="tidb">

-   パスワードの有効期限切れ時のクライアント接続の動作を変更する必要がある場合は、設定ファイル内の[`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)設定項目を変更してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   有効期限切れのパスワードに対するクライアント接続のデフォルト動作を変更する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

### div_precision_increment <span class="version-mark">v8.0.0で追加</span> {#div-precision-increment-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `4`
-   範囲: `[0, 30]`
-   この変数は、演算子`/`を使用して実行される除算演算の結果の桁数を増やすための桁数を指定します。この変数はMySQLと同じです。

### エラー数 {#error-count}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   メッセージを生成した最後のステートメントによって発生したエラーの数を示す読み取り専用変数。

### 外部キーチェック {#foreign-key-checks}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値：v6.6.0より前のバージョンではデフォルト値は`OFF`です。v6.6.0以降ではデフォルト値は`ON`です。
-   この変数は、外部キー制約チェックを有効にするかどうかを制御します。

### グループ連結最大長さ {#group-concat-max-len}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1024`
-   範囲: `[4, 18446744073709551615]`
-   `GROUP_CONCAT()`関数内の項目の最大バッファサイズ。

### have_openssl {#have-openssl}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQLとの互換性を確保するための読み取り専用変数。サーバーがTLSを有効にしている場合、サーバーによって`YES`に設定されます。

### have_sl {#have-ssl}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQLとの互換性を確保するための読み取り専用変数。サーバーがTLSを有効にしている場合、サーバーによって`YES`に設定されます。

### ホスト名 {#hostname}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: (システムホスト名)
-   TiDBサーバーのホスト名を読み取り専用変数として指定します。

### アイデンティティ<span class="version-mark">v5.3.0の新機能</span> {#identity-span-class-version-mark-new-in-v5-3-0-span}

この変数は[`last_insert_id`](#last_insert_id)の別名です。

### init_connect {#init-connect}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   `init_connect`機能を使用すると、TiDBサーバーに初めて接続したときにSQLステートメントが自動的に実行されます。3 `CONNECTION_ADMIN`または`SUPER`権限を持っている場合、この`init_connect`ステートメントは実行されません。9 `init_connect`のステートメントでエラーが発生した場合、ユーザー接続は終了します。

### innodb_lock_wait_timeout {#innodb-lock-wait-timeout}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `50`
-   範囲: `[1, 3600]`
-   単位：秒
-   悲観的トランザクションのロック待機タイムアウト（デフォルト）。

### インタラクティブタイムアウト {#interactive-timeout}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `28800`
-   範囲: `[1, 31536000]`
-   単位：秒
-   この変数は、対話型ユーザーセッションのアイドルタイムアウトを表します。対話型ユーザーセッションとは[`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API をオプション`CLIENT_INTERACTIVE`を使用して呼び出すことで確立されるセッション（例えば、MySQL Shell や MySQL Client）を指します。この変数は MySQL と完全に互換性があります。

### 最後の挿入ID {#last-insert-id}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、INSERT文によって生成された最後の`AUTO_INCREMENT`または`AUTO_RANDOM`値を返します。
-   `last_insert_id`の値は、関数`LAST_INSERT_ID()`によって返される値と同じです。

### last_plan_from_binding <span class="version-mark">v4.0の新機能</span> {#last-plan-from-binding-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   この変数は、前のステートメントで使用された実行計画が[計画の製図](/sql-plan-management.md)の影響を受けたかどうかを示すために使用されます。

### last_plan_from_cache <span class="version-mark">v4.0で追加</span> {#last-plan-from-cache-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   この変数は、前のステートメント`execute`で使用された実行プランがプランキャッシュから直接取得されたものかどうかを示すために使用されます。

### last_sql_use_alloc <span class="version-mark">v6.4.0で追加</span> {#last-sql-use-alloc-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   この変数は読み取り専用です。前のステートメントがキャッシュされたチャンクオブジェクト（チャンク割り当て）を使用しているかどうかを示すために使用されます。

### ライセンス {#license}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `Apache License 2.0`
-   この変数は、TiDBサーバーのインストールにおけるライセンスを示します。

### max_allowed_pa <span class="version-mark">​​cket v6.1.0で追加</span> {#max-allowed-packet-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `67108864`
-   範囲: `[1024, 1073741824]`
-   値は1024の整数倍である必要があります。値が1024で割り切れない場合は、警告が表示され、値は切り捨てられます。たとえば、値を1025に設定した場合、TiDBでの実際の値は1024になります。
-   サーバーとクライアントが1回のパケット送信で許容する最大パケットサイズ。
-   スコープ`SESSION`では、この変数は読み取り専用です。
-   この変数はMySQLと互換性があります。

### password_history <span class="version-mark">v6.5.0で追加</span> {#password-history-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、パスワード変更回数に基づいてパスワードの再利用を制限するTiDBのパスワード再利用ポリシーを設定するために使用されます。デフォルト値の`0` 、パスワード変更回数に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数を正の整数`N`に設定すると、過去`N`パスワードの再利用は許可されません。

### mpp_exchange_compression_mode <span class="version-mark">v6.6.0で追加</span> {#mpp-exchange-compression-mode-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `UNSPECIFIED`
-   `UNSPECIFIED` `FAST` `HIGH_COMPRESSION` `NONE`
-   この変数は、MPP Exchange オペレータのデータ圧縮モードを指定するために使用されます。この変数は、TiDB がバージョン番号`1`の MPP 実行プランを選択した場合に有効になります。変数の値の意味は次のとおりです。
    -   `UNSPECIFIED` ：未指定を意味します。TiDBは圧縮モードを自動的に選択します。現在、TiDBは自動的にモード`FAST`を選択します。
    -   `NONE` ：データ圧縮は使用されません。
    -   `FAST` ：高速モード。全体的なパフォーマンスは良好で、圧縮率は`HIGH_COMPRESSION`未満です。
    -   `HIGH_COMPRESSION` ：高圧縮比モード。

### mpp_version <span class="version-mark">v6.6.0で追加</span> {#mpp-version-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `UNSPECIFIED`
-   `2` `0` `1` `UNSPECIFIED`
-   この変数は、MPP実行プランの異なるバージョンを指定するために使用されます。バージョンが指定されると、TiDBは指定されたバージョンのMPP実行プランを選択します。変数の値の意味は次のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。TiDB は自動的に最新バージョン`2`を選択します。
    -   `0` ：すべてのTiDBクラスタバージョンと互換性があります。MPPバージョンが`0`より大きい機能は、このモードでは有効になりません。
    -   `1` : v6.6.0 の新機能。 TiFlashでの圧縮によるデータ交換を有効にするために使用されます。詳細については、 [MPPバージョンとデータ圧縮の交換](/explain-mpp.md#mpp-version-and-exchange-data-compression)を参照してください。
    -   `2` : v7.3.0 で新しく追加され、 TiFlash上で MPP タスクがエラーに遭遇したときに、より正確なエラー メッセージを提供するために使用されます。

### password_reuse_interval は<span class="version-mark">v6.5.0 で追加されました。</span> {#password-reuse-interval-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、TiDBが経過時間に基づいてパスワードの再利用を制限できるようにするパスワード再利用ポリシーを設定するために使用されます。デフォルト値の`0`経過時間に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数を正の整数`N`に設定すると、過去`N`日間に使用されたパスワードの再利用は許可されません。

### 最大接続数 {#max-connections}

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   単一のTiDBインスタンスで許可される同時接続の最大数。この変数はリソース制御に使用できます。
-   デフォルト値の`0`は制限なしを意味します。この変数の値が`0`より大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新規接続を拒否します。

### 最大実行時間 {#max-execution-time}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位：ミリ秒
-   ステートメントの最大実行時間。デフォルト値は無制限（ゼロ）です。

> **注記：**
>
> バージョン6.4.0より前は、システム変数`max_execution_time`すべての種類のステートメントに適用されていました。バージョン6.4.0以降では、この変数は`SELECT`ステートメントの最大実行時間のみを制御します。タイムアウト値の精度は約100ミリ秒です。つまり、指定したミリ秒数でステートメントが正確に終了しない可能性があります。

<CustomContent platform="tidb">

[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)ヒントを指定したSQL文の場合、この文の最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは[SQL FAQにて](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement)記載されているように、SQLバインディングでも使用できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)ヒントを指定したSQL文の場合、この文の最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは[SQL FAQにて](https://docs.pingcap.com/tidb/stable/sql-faq)記載されているように、SQLバインディングでも使用できます。

</CustomContent>

### max_prepared_stmt_count {#max-prepared-stmt-count}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 1048576]`
-   現在のTiDBインスタンスにおける[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントの最大数を指定します。
-   値が`-1`の場合、現在のTiDBインスタンスにおける最大`PREPARE`のステートメント数に制限はありません。
-   変数に上限値`1048576`を超える値を設定すると、代わりに`1048576`使用されます。

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

### pd_enable_follower_handle_region <span class="version-mark">v7.6.0で追加</span> {#pd-enable-follower-handle-region-span-class-version-mark-new-in-v7-6-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、アクティブPDFollower機能を有効にするかどうかを制御します（現在はリージョン情報の要求にのみ適用されます）。値が`OFF`の場合、TiDBはPDリーダーからのみリージョン情報を取得します。値が`ON`の場合、TiDBはリージョン情報の要求をすべてのPDサーバーに均等に分散し、PDフォロワーもリージョン要求を処理できるため、PDリーダーのCPU負荷が軽減されます。
-   アクティブPDFollowerを有効にするシナリオ：
    -   リージョン数が多いクラスタでは、ハートビートの処理やタスクのスケジューリングに伴うオーバーヘッドが増加するため、PDリーダーのCPU負荷が高くなります。
    -   TiDBインスタンスが多数存在するTiDBクラスタでは、リージョン情報に対する要求の同時発生率が高いため、PDリーダーに高いCPU負荷がかかります。

### プラグインディレクトリ {#plugin-dir}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)ではサポートされていません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   コマンドラインフラグで指定されたプラグインをロードするディレクトリを示します。

### プラグインロード {#plugin-load}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)ではサポートされていません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   TiDB起動時にロードするプラグインを指定します。これらのプラグインはコマンドラインフラグで指定し、カンマで区切ります。

### ポート {#port}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 65535]`
-   `tidb-server` MySQL プロトコルで通信する際にリッスンしているポート。

### rand_seed1 {#rand-seed1}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL関数で使用される乱数生成器のシード値として使用されます。
-   この変数の動作はMySQLと互換性があります。

### rand_seed2 {#rand-seed2}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL関数で使用される乱数生成器のシード値として使用されます。
-   この変数の動作はMySQLと互換性があります。

### require_secure_transport <span class="version-mark">v6.1.0で追加</span> {#require-secure-transport-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> 現在、この変数は[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)ではサポートされていません。TiDB TiDB Cloud Dedicatedクラスターでは、この変数を有効にし**ないで**ください。有効にすると、SQL クライアントの接続エラーが発生する可能性があります。この制限は一時的な対策であり、今後のリリースで解消される予定です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値：TiDB Self-Managedおよび[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合は`OFF` 、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は`ON`

<CustomContent platform="tidb">

-   この変数により、TiDB へのすべての接続がローカル ソケット上か TLS を使用するようになります。詳細については、 [TiDBクライアントとサーバー間でTLSを有効にする](/enable-tls-between-clients-and-servers.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数により、TiDBへのすべての接続はローカルソケットを使用するか、TLSを使用することが保証されます。

</CustomContent>

-   この変数を`ON`に設定するには、TLSが有効になっているセッションからTiDBに接続する必要があります。これにより、TLSが正しく設定されていない場合に発生するロックアウトを防ぐことができます。
-   この設定は以前はオプション`tidb.toml` （ `security.require-secure-transport` ）でしたが、TiDB v6.1.0以降はシステム変数に変更されました。
-   バージョン6.5.6、7.1.2、7.5.1、および8.0.0以降では、Security強化モード（SEM）が有効になっている場合、ユーザーの接続に関する潜在的な問題を回避するため、この変数を`ON`に設定することは禁止されています。

### skip_name_resolve <span class="version-mark">v5.2.0で追加</span> {#skip-name-resolve-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、インスタンス`tidb-server`が接続ハンドシェイクの一部としてホスト名を解決するかどうかを制御します。
-   DNSが不安定な場合、このオプションを有効にすることでネットワークパフォーマンスを向上させることができます。

> **注記：**
>
> `skip_name_resolve=ON`の場合、ホスト名を ID に含むユーザーはサーバーにログインできなくなります。例:
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> この例では、 `apphost` IP アドレスまたはワイルドカード ( `%` ) に置き換えることをお勧めします。

### ソケット {#socket}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   `tidb-server` MySQLプロトコルで通信する際にリッスンしているローカルUnixソケットファイル。

### sql_mode {#sql-mode}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
-   この変数は、MySQLとの互換性に関する様々な動作を制御します。詳細については、 [SQLモード](/sql-mode.md)を参照してください。

### sql_require_primary_key<span class="version-mark">は v6.3.0 で追加されました。</span> {#sql-require-primary-key-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、テーブルに主キーが必要であるという要件を強制するかどうかを制御します。この変数を有効にすると、主キーのないテーブルを作成または変更しようとするとエラーが発生します。
-   この機能は、MySQL 8.0 の同名の[`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key)に基づいています。
-   TiCDCを使用する際は、この変数を有効にすることを強くお勧めします。これは、MySQLシンクへの変更のレプリケートには、テーブルに主キーが必要となるためです。

<CustomContent platform="tidb">

-   この変数を有効にし、TiDB Data Migration (DM) を使用してデータを移行している場合は、 [DMタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)の`session`部分に`sql_require_ primary_key`追加して`OFF`に設定することをお勧めします。そうしないと、DM がタスクを作成できなくなります。

</CustomContent>

### sql_select_limit は<span class="version-mark">v4.0.2 で追加されました</span> {#sql-select-limit-span-class-version-mark-new-in-v4-0-2-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `18446744073709551615`
-   範囲: `[0, 18446744073709551615]`
-   単位：行
-   `SELECT`ステートメントによって返される行の最大数。

### ssl_ca {#ssl-ca}

<CustomContent platform="tidb">

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   認証局ファイルの場所（存在する場合）。この変数の値は、TiDB 構成項目[`ssl-ca`](/tidb-configuration-file.md#ssl-ca)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   認証局ファイルの場所（存在する場合）。この変数の値は、TiDB 構成項目[`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca)によって定義されます。

</CustomContent>

### SSL証明書 {#ssl-cert}

<CustomContent platform="tidb">

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS接続に使用される証明書ファイルの場所（ファイルが存在する場合）。この変数の値は、TiDB構成項目[`ssl-cert`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS接続に使用される証明書ファイルの場所（ファイルが存在する場合）。この変数の値は、TiDB構成項目[`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert)によって定義されます。

</CustomContent>

### SSLキー {#ssl-key}

<CustomContent platform="tidb">

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS接続に使用される秘密鍵ファイル（存在する場合）の場所。この変数の値は、TiDB構成項目[`ssl-key`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS接続に使用される秘密鍵ファイル（存在する場合）の場所。この変数の値は、TiDB構成項目[`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key)によって定義されます。

</CustomContent>

### システムタイムゾーン {#system-time-zone}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値：（システム依存）
-   この変数は、TiDBが最初にブートストラップされた時点のシステムタイムゾーンを示します[`time_zone`](#time_zone)も参照してください。

### tidb_adaptive_closest_read_threshold は<span class="version-mark">v6.3.0 で追加されました。</span> {#tidb-adaptive-closest-read-threshold-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `4096`
-   範囲: `[0, 9223372036854775807]`
-   単位：バイト
-   この変数は、 [`tidb_replica_read`](#tidb_replica_read-new-in-v40)が`closest-adaptive`に設定されている場合に、TiDBサーバーが読み取りリクエストを TiDBサーバーと同じ可用性ゾーンにあるレプリカに送信することを優先するしきい値を制御するために使用されます。推定結果がこのしきい値以上の場合、TiDB は同じ可用性ゾーンにあるレプリカに読み取りリクエストを送信することを優先します。それ以外の場合は、TiDB はリーダーレプリカに読み取りリクエストを送信します。

### tidb_advancer_check_point_lag_limit は<span class="version-mark">v8.5.5 で追加されました。</span> {#tidb-advancer-check-point-lag-limit-span-class-version-mark-new-in-v8-5-5-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ：期間
-   デフォルト値: `48h0m0s`
-   範囲: `[1s, 8760h0m0s]`
-   この変数は、ログバックアップタスクで許容される最大チェックポイント遅延を制御します。タスクのチェックポイント遅延がこの制限を超えると、TiDB Advancer はタスクを一時停止します。

### tidb_allow_tiflash_cop <span class="version-mark">v7.3.0で追加</span> {#tidb-allow-tiflash-cop-span-class-version-mark-new-in-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   TiDBが計算タスクをTiFlashにプッシュダウンする場合、Cop、BatchCop、MPPの3つの方法（プロトコル）から選択できます。CopおよびBatchCopと比較して、MPPプロトコルはより成熟しており、タスクおよびリソース管理において優れています。そのため、MPPプロトコルの使用をお勧めします。
    -   `0`または`OFF` ：オプティマイザはTiFlash MPPプロトコルを使用したプランのみを生成します。
    -   `1`または`ON` ：オプティマイザは、コスト見積もりに基づいて実行プランを生成するために、Cop、BatchCop、またはMPPプロトコルを使用するかどうかを決定します。

### tidb_allow_batch_cop <span class="version-mark">v4.0で追加</span> {#tidb-allow-batch-cop-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   この変数は、TiDBがTiFlashにコプロセッサ要求を送信する方法を制御するために使用されます。この変数には以下の値があります。

    -   `0` ：リクエストをバッチで送信しないでください
    -   `1` ：集計および結合リクエストはバッチで送信されます
    -   `2` ：すべてのコプロセッサ要求はバッチで送信されます

### tidb_allow_fallback_to_tikv <span class="version-mark">v5.0で追加</span> {#tidb-allow-fallback-to-tikv-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: &quot;&quot;
-   この変数は、TiKV にフォールバックする可能性のあるstorageエンジンのリストを指定するために使用されます。リストで指定されたstorageエンジンの障害により SQL ステートメントの実行が失敗した場合、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。この変数は &quot;&quot; または &quot;tiflash&quot; に設定できます。この変数が &quot;tiflash&quot; に設定されている場合、 TiFlash がタイムアウト エラー (エラー コード: ErrTiFlashServerTimeout) を返すと、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。

### tidb_allow_function_for_expression_index <span class="version-mark">v5.2.0で追加</span> {#tidb-allow-function-for-expression-index-span-class-version-mark-new-in-v5-2-0-span}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_schema_valid, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash`
-   この読み取り専用変数は、 [発現指数](/sql-statements/sql-statement-create-index.md#expression-index)を作成するために使用できる関数を表示するために使用されます。

### tidb_allow_mpp <span class="version-mark">v5.0で追加</span> {#tidb-allow-mpp-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiFlashのMPPモードを使用してクエリを実行するかどうかを制御します。値のオプションは以下のとおりです。
    -   `0`または`OFF`指定すると、MPPモードは使用されません。v7.3.0以降のバージョンでは、この変数の値を`0`または`OFF`に設定する場合は、 [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)変数も有効にする必要があります。そうしないと、クエリでエラーが発生する可能性があります。
    -   `1`または`ON`場合、オプティマイザはコスト見積もりに基づいてMPPモードを使用するかどうかを決定します（デフォルト）。

MPP は、 TiFlashエンジンによって提供される分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能、高スループットの SQL アルゴリズムを提供します。 MPPモードの選択の詳細については、 [MPPモードを選択するかどうかを制御する](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)。

### tidb_allow_remove_auto_inc は<span class="version-mark">v2.1.18 および v3.0.4 で追加されました。</span> {#tidb-allow-remove-auto-inc-span-class-version-mark-new-in-v2-1-18-and-v3-0-4-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、列の`AUTO_INCREMENT`のプロパティを`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`ステートメントを実行することで削除できるかどうかを設定するために使用されます。デフォルトでは許可されていません。

### tidb_analyze_column_options は<span class="version-mark">v8.3.0 で追加されました。</span> {#tidb-analyze-column-options-span-class-version-mark-new-in-v8-3-0-span}

> **注記：**
>
> -   この変数は、 [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510)が`2`に設定されている場合にのみ機能します。
> -   TiDBクラスタをv8.3.0より前のバージョンからv8.3.0以降にアップグレードする場合、元の動作を維持するために、この変数はデフォルトで`ALL`に設定されます。
> -   バージョン8.3.0から8.5.4までの新規デプロイされたTiDBクラスタの場合、この変数はデフォルトで`PREDICATE`に設定されます。
> -   バージョン8.5.5以降に新規にデプロイされたTiDBクラスタの場合、この変数はデフォルトで`ALL`に設定されます。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `ALL`
-   `PREDICATE`オプション： `ALL`
-   この変数は、 `ANALYZE TABLE`ステートメントの動作を制御します`PREDICATE`に設定すると、 [述語列](/statistics.md#collect-statistics-on-some-columns)の統計情報のみが収集されます`ALL`に設定すると、すべての列の統計情報が収集されます。OLAP クエリを使用するシナリオでは、 `ALL`に設定することをお勧めします。そうしないと、統計情報の収集によってクエリのパフォーマンスが著しく低下する可能性があります。

### tidb_analyze_distsql_scan_concurrency <span class="version-mark">v7.6.0で追加</span> {#tidb-analyze-distsql-scan-concurrency-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `4`
-   範囲: `[0, 4294967295]`より前のバージョンでは、最小値は`1`です`0`に設定すると、クラスタサイズに基づいて同時実行数が適応的に調整されます。
-   この変数は、操作`ANALYZE`を実行する際に、操作`scan`の同時実行数を設定するために使用されます。

### tidb_analyze_partition_concurrency {#tidb-analyze-partition-concurrency}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値： `2`以前のバージョンではデフォルト値は`1`です。
-   範囲: `[1, 128]`より前は、値の範囲は`[1, 18446744073709551615]`です。
-   この変数は、TiDB がパーティションテーブルを分析する際に、収集された統計情報を書き込む際の同時実行数を指定します。

### tidb_analyze_version <span class="version-mark">v5.1.0で追加</span> {#tidb-analyze-version-span-class-version-mark-new-in-v5-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   TiDBが統計情報を収集する方法を制御します。
    -   TiDB Self-Managedの場合、この変数のデフォルト値はv5.3.0以降、 `1`から`2`に変更されます。
    -   TiDB Cloudの場合、この変数のデフォルト値はv6.5.0以降、 `1`から`2`に変更されます。
    -   クラスターを以前のバージョンからアップグレードした場合、デフォルト値の`tidb_analyze_version`はアップグレード後も変更されません。
-   この変数の詳細については、[統計入門](/statistics.md)参照してください。

### tidb_analyze_skip_column_types は<span class="version-mark">v7.2.0 で追加されました。</span> {#tidb-analyze-skip-column-types-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: 「json、blob、mediumblob、longblob、mediumtext、longtext」。 v8.2.0 より前のデフォルト値は「json,blob,mediumblob,longblob」です。
-   指定可能な値: &quot;json,blob,mediumblob,longblob,text,mediumtext,longtext&quot;
-   この変数は、統計情報を収集するコマンド`ANALYZE`を実行する際に、統計情報の収集対象から除外する列の種類を制御します。この変数は`tidb_analyze_version = 2`にのみ適用されます。5 `ANALYZE TABLE t COLUMNS c1, ... , cn`使用して列を指定した場合でも、その列の型が`tidb_analyze_skip_column_types`に含まれる場合は、指定された列の統計情報は収集されません。

<!---->

    mysql> SHOW CREATE TABLE t;
    +-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Table | Create Table                                                                                                                                                                                                             |
    +-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | t     | CREATE TABLE `t` (
      `a` int DEFAULT NULL,
      `b` varchar(10) DEFAULT NULL,
      `c` json DEFAULT NULL,
      `d` blob DEFAULT NULL,
      `e` longblob DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
    +-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

    mysql> SELECT @@tidb_analyze_skip_column_types;
    +----------------------------------+
    | @@tidb_analyze_skip_column_types |
    +----------------------------------+
    | json,blob,mediumblob,longblob    |
    +----------------------------------+
    1 row in set (0.00 sec)

    mysql> ANALYZE TABLE t;
    Query OK, 0 rows affected, 1 warning (0.05 sec)

    mysql> SELECT job_info FROM mysql.analyze_jobs ORDER BY end_time DESC LIMIT 1;
    +---------------------------------------------------------------------+
    | job_info                                                            |
    +---------------------------------------------------------------------+
    | analyze table columns a, b with 256 buckets, 500 topn, 1 samplerate |
    +---------------------------------------------------------------------+
    1 row in set (0.00 sec)

    mysql> ANALYZE TABLE t COLUMNS a, c;
    Query OK, 0 rows affected, 1 warning (0.04 sec)

    mysql> SELECT job_info FROM mysql.analyze_jobs ORDER BY end_time DESC LIMIT 1;
    +------------------------------------------------------------------+
    | job_info                                                         |
    +------------------------------------------------------------------+
    | analyze table columns a with 256 buckets, 500 topn, 1 samplerate |
    +------------------------------------------------------------------+
    1 row in set (0.00 sec)

### tidb_auto_analyze_concurrency <span class="version-mark">v8.4.0で追加</span> {#tidb-auto-analyze-concurrency-span-class-version-mark-new-in-v8-4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[1, 2147483647]`
-   この変数は、TiDBクラスタで同時に実行できる自動分析操作の数を制御します。v8.4.0より前のバージョンでは、この同時実行数は1に固定されていました。統計情報の収集タスクを高速化するには、クラスタで使用可能なリソースに基づいてこの同時実行数を増やすことができます。

### tidb_auto_analyze_end_time {#tidb-auto-analyze-end-time}

-   対象範囲：グローバル

-   クラスターに保持される: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ

-   タイプ: 時間

-   デフォルト値: `23:59 +0000`

-   この変数は、統計情報の自動更新が許可される時間帯を制限するために使用されます。たとえば、UTC時間で午前1時から午前3時の間のみ統計情報の自動更新を許可するには、次のように時間を設定します。

    -   `tidb_auto_analyze_start_time='01:00 +0000'`
    -   `tidb_auto_analyze_end_time='03:00 +0000'`

-   パラメータ内の時刻にタイムゾーン情報が含まれている場合、そのタイムゾーンが解析に使用されます。含まれていない場合は、現在のセッションで「 `time_zone`によって指定されたタイムゾーンが使用されます。例えば、 `01:00 +0000`はUTCの午前1時を表します。

### tidb_auto_analyze_partition_batch_size は<span class="version-mark">v6.4.0 で追加されました。</span> {#tidb-auto-analyze-partition-batch-size-span-class-version-mark-new-in-v6-4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `8192`より前のバージョンでは、デフォルト値は`1`です。v7.6.0 から v8.1.x までのバージョンでは、デフォルト値は`128`です。v8.2.0 以降では、デフォルト値は`8192`に変更されます。
-   範囲: `[1, 8192]`より前は、値の範囲は`[1, 1024]`です。
-   この変数は、パーティションテーブルを分析するときに TiDB が[自動的に分析します](/statistics.md#automatic-update)パーティションの数を指定します (つまり、パーティションテーブルに関する統計を自動的に収集します)。
-   この変数の値がパーティション数より小さい場合、TiDB はパーティションテーブルのすべてのパーティションを複数回に分けて自動的に分析します。この変数の値がパーティション数以上の場合、TiDB はパーティションテーブルのすべてのパーティションを同時に分析します。
-   パーティションテーブルのパーティション数がこの変数の値よりもはるかに多く、自動分析に時間がかかる場合は、この変数の値を増やすことで処理時間を短縮できます。

### tidb_auto_analyze_ratio {#tidb-auto-analyze-ratio}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: フロート
-   デフォルト値: `0.5`
-   範囲: `(0, 1]`以前のバージョンの範囲は`[0, 18446744073709551615]`です。
-   この変数は、TiDB がバックグラウンド スレッドで[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)自動的に実行してテーブル統計を更新する際のしきい値を設定するために使用されます。たとえば、値が 0.5 の場合、テーブル内の行の 50% 以上が変更されたときに自動分析がトリガーされます。自動分析は、 `tidb_auto_analyze_start_time`と`tidb_auto_analyze_end_time`指定することで、特定の時間帯のみ実行するように制限できます。

> **注記：**
>
> この機能を使用するには、システム変数`tidb_enable_auto_analyze` `ON`に設定する必要があります。

### tidb_auto_analyze_start_time {#tidb-auto-analyze-start-time}

-   対象範囲：グローバル

-   クラスターに保持される: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ

-   タイプ: 時間

-   デフォルト値: `00:00 +0000`

-   この変数は、統計情報の自動更新が許可される時間帯を制限するために使用されます。たとえば、UTC時間で午前1時から午前3時の間のみ統計情報の自動更新を許可するには、次のように時間を設定します。

    -   `tidb_auto_analyze_start_time='01:00 +0000'`
    -   `tidb_auto_analyze_end_time='03:00 +0000'`

-   パラメータ内の時刻にタイムゾーン情報が含まれている場合、そのタイムゾーンが解析に使用されます。含まれていない場合は、現在のセッションで「 `time_zone`によって指定されたタイムゾーンが使用されます。例えば、 `01:00 +0000`はUTCの午前1時を表します。

### tidb_auto_build_stats_concurrency <span class="version-mark">v6.5.0で追加</span> {#tidb-auto-build-stats-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、統計情報の自動更新を実行する際の同時実行数を設定するために使用されます。

### tidb_backoff_lock_fast {#tidb-backoff-lock-fast}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `10`
-   範囲: `[1, 2147483647]`
-   この変数は、読み取り要求がロックに遭遇する`backoff`タイミングを設定するために使用されます。

### tidb_backoff_weight {#tidb-backoff-weight}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `2`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB `backoff`の最大再試行待機時間の重みを増やすために使用されます。つまり、内部ネットワークまたはその他のコンポーネント(TiKV、PD) の障害が発生した場合に再試行要求を送信する際の最大再試行待機時間です。この変数を使用して最大再試行待機時間を調整でき、最小値は`1`です。

    例えば、TiDB が TiKV から KV を取得する際の基本再試行待機時間は 15 秒です。 が`tidb_backoff_weight = 2`場合、KV を取得する際の最大再試行待機時間は、*基本時間 * 2 = 30 秒*となります。

    ネットワーク環境が悪い場合、この変数の値を適切に増やすことで、タイムアウトによってアプリケーション側に発生するエラー報告を効果的に軽減できます。アプリケーション側でエラー情報をより迅速に受信したい場合は、この変数の値を最小化してください。

<CustomContent platform="tidb">

> **注記：**
>
> このシステム変数は、TSOリクエストを非同期で取得する場合に**適用されません**。TSO取得のタイムアウトを調整するには、 [`pd-server-timeout`](/tidb-configuration-file.md#pd-server-timeout)設定項目を設定してください。

</CustomContent>

### tidb_batch_commit {#tidb-batch-commit}

> **警告：**
>
> この変数を有効にすることは推奨**されません**。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチコミット機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、トランザクションが複数のトランザクションに分割され、いくつかのステートメントがグループ化されて非アトミックにコミットされる可能性がありますが、これは推奨されません。

### tidb_batch_delete {#tidb-batch-delete}

> **警告：**
>
> この変数は、非推奨のバッチ DML 機能に関連付けられており、データ破損を引き起こす可能性があります。そのため、バッチ DML でこの変数を有効にすることは推奨されません。代わりに、[非トランザクションDML](/non-transactional-dml.md)を使用してください。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチ DML 機能の一部であるバッチ削除機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `DELETE`ステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`有効にし、 `tidb_dml_batch_size`に正の値を設定する必要がありますが、これは推奨されません。

### tidb_batch_insert {#tidb-batch-insert}

> **警告：**
>
> この変数は、非推奨のバッチ DML 機能に関連付けられており、データ破損を引き起こす可能性があります。そのため、バッチ DML でこの変数を有効にすることは推奨されません。代わりに、[非トランザクションDML](/non-transactional-dml.md)を使用してください。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチ DML 機能の一部であるバッチ挿入機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `INSERT`ステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`有効にし、 `tidb_dml_batch_size`に正の値を設定する必要がありますが、これは推奨されません。

### tidb_batch_pending_tiflash_count <span class="version-mark">v6.0で追加</span> {#tidb-batch-pending-tiflash-count-span-class-version-mark-new-in-v6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 4294967295]`
-   TiFlashレプリカを追加する際に`ALTER DATABASE SET TIFLASH REPLICA`を指定する場合、許可される使用不可テーブルの最大数を指定します。使用不可テーブルの数がこの制限を超えると、操作が停止するか、残りのテーブルのTiFlashレプリカの設定が非常に遅くなります。

### tidb_broadcast_join_threshold_count <span class="version-mark">v5.0で追加</span> {#tidb-broadcast-join-threshold-count-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `10240`
-   範囲: `[0, 9223372036854775807]`
-   単位：行
-   結合操作の対象がサブクエリに属する​​場合、オプティマイザはサブクエリの結果セットのサイズを推定できません。この場合、サイズは結果セットの行数によって決定されます。サブクエリの推定行数がこの変数の値より少ない場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。そうでない場合は、シャッフルハッシュ結合アルゴリズムが使用されます。
-   この変数は、 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)が有効になった後は効果を発揮しません。

### tidb_broadcast_join_threshold_size <span class="version-mark">v5.0で追加</span> {#tidb-broadcast-join-threshold-size-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値： `104857600` （100 MiB）
-   範囲: `[0, 9223372036854775807]`
-   単位：バイト
-   テーブルサイズが変数の値より小さい場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。
-   この変数は、 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)が有効になった後は効果を発揮しません。

### tidb_build_stats_concurrency {#tidb-build-stats-concurrency}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値： `2`以前のバージョンではデフォルト値は`4`です。
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、 `ANALYZE`ステートメントの実行の同時実行数を設定するために使用されます。
-   変数をより大きな値に設定すると、他のクエリの実行パフォーマンスに影響が出ます。

### tidb_build_sampling_stats_concurrency は<span class="version-mark">v7.5.0 で追加されました。</span> {#tidb-build-sampling-stats-concurrency-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   単位：糸
-   デフォルト値: `2`
-   範囲: `[1, 256]`
-   この変数は、 `ANALYZE`プロセスにおけるサンプリングの同時実行数を設定するために使用されます。
-   変数をより大きな値に設定すると、他のクエリの実行パフォーマンスに影響が出ます。

### tidb_capture_plan_baselines <span class="version-mark">v4.0で追加</span> {#tidb-capture-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [ベースラインの取得](/sql-plan-management.md#baseline-capturing)機能を有効にするかどうかを制御するために使用されます。この機能はステートメントサマリーに依存するため、ベースラインキャプチャを使用する前にステートメントサマリーを有効にする必要があります。
-   この機能を有効にすると、ステートメントサマリー内の過去のSQLステートメントが定期的に走査され、少なくとも2回出現するSQLステートメントに対してバインディングが自動的に作成されます。

### tidb_cdc_write_source <span class="version-mark">v6.5.0で追加</span> {#tidb-cdc-write-source-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   範囲: セッション
-   クラスターに保持される: いいえ
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数に0以外の値が設定されている場合、このセッションで書き込まれたデータはTiCDCによって書き込まれたものとみなされます。この変数はTiCDCのみが変更できます。いかなる場合でも、この変数を手動で変更しないでください。

### tidb_check_mb4_value_in_utf8 {#tidb-check-mb4-value-in-utf8}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `utf8`文字セットが[基本多言語平面（BMP）](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane)の値のみを格納するように強制するために使用されます。BMP以外の文字を格納するには、 `utf8mb4`文字セットを使用することをお勧めします。
-   `utf8`チェックがより緩和されていた以前のバージョンの TiDB からクラスターをアップグレードする場合は、このオプションを無効にする必要がある場合があります。詳細については、 [アップグレード後のよくある質問](https://docs.pingcap.com/tidb/stable/upgrade-faq)を参照してください。

### tidb_checksum_table_concurrency {#tidb-checksum-table-concurrency}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、 [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)ステートメントを実行する際のスキャン インデックスの同時実行数を設定するために使用されます。
-   変数をより大きな値に設定すると、他のクエリの実行パフォーマンスに影響が出ます。

### tidb_committer_concurrency <span class="version-mark">v6.1.0で追加</span> {#tidb-committer-concurrency-span-class-version-mark-new-in-v6-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `128`
-   範囲: `[1, 10000]`
-   単一トランザクションのコミットフェーズにおけるコミット実行に関連するリクエストのためのゴルーチンの数。
-   コミットするトランザクションが大きすぎる場合、トランザクションがコミットされる際のフロー制御キューの待機時間が長くなる可能性があります。このような場合は、設定値を増やすことでコミットを高速化できます。
-   この設定は以前はオプション`tidb.toml` （ `performance.committer-concurrency` ）でしたが、TiDB v6.1.0以降はシステム変数に変更されました。

### tidb_config {#tidb-config}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   この変数は読み取り専用です。現在のTiDBサーバーの構成情報を取得するために使用されます。

### tidb_constraint_check_in_place {#tidb-constraint-check-in-place}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は楽観的トランザクションにのみ適用されます。悲観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-new-in-v630)を使用してください。
-   この変数を`OFF`に設定すると、一意インデックス内の重複値のチェックはトランザクションがコミットされるまで延期されます。これによりパフォーマンスが向上しますが、一部のアプリケーションでは予期しない動作となる可能性があります。詳細については、[制約](/constraints.md#optimistic-transactions)参照してください。

    -   `tidb_constraint_check_in_place` ～ `OFF`に設定し、楽観的トランザクションを使用する場合：

        ```sql
        tidb> create table t (i int key);
        tidb> insert into t values (1);
        tidb> begin optimistic;
        tidb> insert into t values (1);
        Query OK, 1 row affected
        tidb> commit; -- Check only when a transaction is committed.
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    -   `tidb_constraint_check_in_place` ～ `ON`に設定し、楽観的トランザクションを使用する場合：

        ```sql
        tidb> set @@tidb_constraint_check_in_place=ON;
        tidb> begin optimistic;
        tidb> insert into t values (1);
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_constraint_check_in_place_pessimistic <span class="version-mark">v6.3.0 で追加</span> {#tidb-constraint-check-in-place-pessimistic-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: デフォルトでは、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)設定項目は`true`なので、この変数のデフォルト値は`ON`です。pessimistic [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)が`false`に設定されている場合、この変数のデフォルト値は`OFF`です。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`

</CustomContent>

-   この変数は悲観的トランザクションにのみ適用されます。楽観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place)を使用してください。
-   この変数を`OFF`に設定すると、TiDB は一意インデックスの一意制約チェックを延期します (インデックスへのロックを必要とするステートメントを実行する次回のタイミング、またはトランザクションをコミットするタイミングまで)。これによりパフォーマンスが向上しますが、一部のアプリケーションでは予期しない動作となる可能性があります。 詳細は[制約](/constraints.md#pessimistic-transactions)を参照してください。
-   この変数を無効にすると、TiDB が悲観的トランザクションでエラー`LazyUniquenessCheckFailure`を返す可能性があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。
-   この変数が無効になっている場合、悲観的トランザクションで[`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)使用することはできません。
-   この変数が無効になっている場合、悲観的トランザクションをコミットすると、 `Write conflict`または`Duplicate entry`エラーが返される可能性があります。このようなエラーが発生した場合、TiDBは現在のトランザクションをロールバックします。

    -   `tidb_constraint_check_in_place_pessimistic` ～ `OFF`に設定し、悲観的取引を使用する場合：

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

    -   `tidb_constraint_check_in_place_pessimistic` ～ `ON`に設定し、悲観的取引を使用する場合：

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

            ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'

### tidb_cost_model_version <span class="version-mark">v6.2.0で追加</span> {#tidb-cost-model-version-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> -   TiDB v6.5.0以降では、新しく作成されたクラスタはデフォルトでコストモデルバージョン2を使用します。TiDBバージョンをv6.5.0より前のバージョンからv6.5.0以降にアップグレードした場合、 `tidb_cost_model_version`値は変更されません。
> -   コストモデルのバージョンを変更すると、クエリプランに変更が生じる可能性があります。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `2`
-   お得なオプション：
    -   `1` ：コストモデルバージョン1を有効にします。これはTiDB v6.4.0以前のバージョンでデフォルトで使用されます。
    -   `2` :[コストモデル バージョン2](/cost-model.md#cost-model-version-2)を有効にします。これは TiDB v6.5.0 で一般提供されており、内部テストではバージョン 1 よりも正確です。
-   コスト モデルのバージョンは、オプティマイザーの計画決定に影響します。詳細については、[コストモデル](/cost-model.md)を参照してください。

### tidb_current_ts {#tidb-current-ts}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は読み取り専用です。現在のトランザクションのタイムスタンプを取得するために使用されます。

### tidb_ddl_disk_quota <span class="version-mark">v6.3.0で追加</span> {#tidb-ddl-disk-quota-span-class-version-mark-new-in-v6-3-0-span}

<CustomContent platform="tidb-cloud" plan="starter,essential">

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> この変数は、 [TiDB Cloudプレミアム](https://docs-preview.pingcap.com/tidbcloud/tidb-cloud-intro/#deployment-options)では読み取り専用です。

</CustomContent>

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値： `107374182400` （100 GiB）
-   範囲: `[107374182400, 1125899906842624]` ([100 GiB、1 PiB])
-   単位：バイト
-   この変数は、 [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630)が有効になっている場合にのみ有効になります。インデックス作成時のバックフィル処理におけるローカルstorageの使用制限を設定します。

### tidb_ddl_enable_fast_reorg は<span class="version-mark">v6.3.0 で追加されました。</span> {#tidb-ddl-enable-fast-reorg-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> -   [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)クラスターを使用している場合、この変数を使用してインデックス作成の速度を向上させるには、TiDB クラスターが AWS 上でホストされていること、および TiDB ノードのサイズが少なくとも 8 vCPU であることを確認してください。
> -   4 vCPUを搭載した[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)クラスタの場合、インデックス作成中にリソース制限がクラスタの安定性に影響を与えないように、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)手動で無効にすることをお勧めします。この設定を無効にすることで、トランザクションを使用してインデックスを作成できるようになり、クラスタ全体への影響を軽減できます。
> -   [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスタの場合、この変数は読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックス作成時のバックフィル処理速度を向上させるために、 `ADD INDEX`と`CREATE INDEX`の高速化を有効にするかどうかを制御します。この変数の値を`ON`に設定すると、大量のデータを含むテーブルのインデックス作成のパフォーマンスが向上します。
-   バージョン7.1.0以降、インデックス高速化処理はチェックポイントをサポートしています。障害によりTiDBオーナーノードが再起動または変更された場合でも、TiDBは定期的に自動更新されるチェックポイントから処理の進行状況を回復できます。
-   完了した操作`ADD INDEX`が高速化されたかどうかを確認するには、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)ステートメントを実行して、 `JOB_TYPE`列目に`ingest`表示されているかどうかを確認します。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、この変数は読み取り専用です。変更する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

<CustomContent platform="tidb">

> **注記：**
>
> -   インデックスの高速化には、書き込み可能で十分な空き容量のある[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)が必要です。一時ディレクトリ`temp-dir`が使用できない場合、TiDBは高速化されていないインデックス構築にフォールバックします。一時ディレクトリ`temp-dir`はSSDディスクに配置することをお勧めします。
>
> -   TiDBをv6.5.0以降にアップグレードする前に、TiDBの[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)パスがSSDディスクに正しくマウントされているかどうかを確認することをお勧めします。TiDBを実行するオペレーティングシステムのユーザーが、このディレクトリへの読み取りおよび書き込み権限を持っていることを確認してください。そうでない場合、DDL操作で予期しない問題が発生する可能性があります。このパスはTiDBの設定項目であり、TiDBの再起動後に有効になります。したがって、アップグレード前にこの設定項目を設定しておくことで、再度再起動する必要がなくなります。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> 現在、この機能は[単一の`ALTER TABLE`ステートメントで複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md)完全には互換性がありません。インデックス アクセラレーションを使用して一意のインデックスを追加する場合は、同じステートメント内の他の列やインデックスを変更しないようにする必要があります。

</CustomContent>

### tidb_stats_update_during_ddl は<span class="version-mark">v8.5.4 で追加されました。</span> {#tidb-stats-update-during-ddl-span-class-version-mark-new-in-v8-5-4-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `OFF`
-   この変数は、DDL 埋め込み`ANALYZE`を有効にするかどうかを制御します。有効にすると、新しいインデックスの作成 ( [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) ) または既存のインデックスの再編成 ( [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)および[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) ) を行う DDL ステートメントは、インデックスが表示される前に統計を自動的に収集します。詳細については、 [DDLステートメントに埋め込まれた`ANALYZE`](/ddl_embedded_analyze.md)参照してください。

### tidb_enable_dist_task <span class="version-mark">v7.1.0で追加</span> {#tidb-enable-dist-task-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   この変数は[TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)有効にするかどうかを制御するために使用されます。フレームワークが有効になると、DDLやインポートなどのDXFタスクは、クラスタ内の複数のTiDBノードによって分散的に実行および完了されます。
-   TiDB v7.1.0以降、DXFはパーティションテーブルに対する[`ADD INDEX`](/sql-statements/sql-statement-add-index.md)ステートメントの分散実行をサポートしています。
-   TiDB v7.2.0以降、DXFはインポートジョブにおける[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)ステートメントの分散実行をサポートしています。
-   TiDB v8.1.0以降では、この変数はデフォルトで有効になっています。DXFが有効になっているクラスタをv8.1.0以降にアップグレードする場合は、アップグレード前にDXFを無効（ `tidb_enable_dist_task` ～ `OFF`に設定）にしてください。これにより、アップグレード中に発生する`ADD INDEX`操作によるデータインデックスの不整合を回避できます。アップグレード後、DXFを手動で有効にすることができます。
-   この変数は`tidb_ddl_distribute_reorg`から名前が変更されました。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、この変数は読み取り専用です。変更する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

### tidb_cloud_storage_uri <span class="version-mark">v7.4.0で追加</span> {#tidb-cloud-storage-uri-span-class-version-mark-new-in-v7-4-0-span}

> **注記：**
>
> 現在、[グローバルソート](/tidb-global-sort.md)プロセスは、TiDBノードのコンピューティングリソースとメモリリソースを大量に消費します。ユーザー業務アプリケーションの実行中にオンラインでインデックスを追加するなどのシナリオでは、クラスタに新しいTiDBノードを追加し、これらのノードに対して[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)変数を設定し、これらのノードに接続してタスクを作成することをお勧めします。このようにして、分散フレームワークはタスクをこれらのノードにスケジュールし、ワークロードを他のTiDBノードから分離することで、 `ADD INDEX`や`IMPORT INTO`などのバックエンドタスクの実行がユーザー業務アプリケーションに与える影響を軽減します。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `""`
-   この変数は、[グローバルソート](/tidb-global-sort.md)を有効にするための Amazon S3 クラウドstorageURI を指定するために使用されます。 [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)を有効にすると、URI を構成し、storageへのアクセスに必要な権限を持つ適切なクラウドstorageパスを指すようにすることで、グローバル ソート機能を使用できるようになります。詳細については、 [Amazon S3 URI形式](/external-storage-uri.md#amazon-s3-uri-format)を参照してください。
-   以下のステートメントでは、グローバルソート機能を使用できます。
    -   [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)文。
    -   インポートジョブ用の[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)ステートメント。

### tidb_ddl_error_count_limit {#tidb-ddl-error-count-limit}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `512`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、DDL操作が失敗した場合の再試行回数を設定するために使用されます。再試行回数がパラメータ値を超えると、誤ったDDL操作はキャンセルされます。

### tidb_ddl_flashback_concurrency <span class="version-mark">v6.3.0で追加</span> {#tidb-ddl-flashback-concurrency-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `64`
-   範囲: `[1, 256]`
-   この変数は[`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)の同時実行を制御します。

### tidb_ddl_reorg_batch_size {#tidb-ddl-reorg-batch-size}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `256`
-   範囲: `[32, 10240]`
-   単位：行
-   この変数は、DDL操作の第`re-organize`フェーズにおけるバッチサイズを設定するために使用されます。例えば、TiDBが第`ADD INDEX`フェーズを実行する際、インデックスデータは`tidb_ddl_reorg_worker_cnt` （数値）の同時実行ワーカーによってバックフィルされる必要があります。各ワーカーは、インデックスデータをバッチ単位でバックフィルします。
    -   `tidb_ddl_enable_fast_reorg` `OFF`に設定されている場合、 `ADD INDEX`トランザクションとして実行されます。11 `ADD INDEX`実行中に、対象列で`UPDATE`や`REPLACE`などの更新操作が多数発生する場合、バッチサイズが大きいほどトランザクション競合が発生する可能性が高くなります。この場合、バッチサイズを小さい値に設定することをお勧めします。最小値は32です。
    -   トランザクションの競合が存在しない場合、または`tidb_ddl_enable_fast_reorg` `ON`に設定されている場合は、バッチ サイズを大きな値に設定できます。これにより、データのバックフィルが高速になりますが、TiKV への書き込み圧力も増加します。適切なバッチ サイズについては、 `tidb_ddl_reorg_worker_cnt`の値も参照する必要があります。参考として[オンラインワークロードと`ADD INDEX`操作に関する相互作用テスト](https://docs.pingcap.com/tidb/dev/online-workloads-and-add-index-operations)参照してください。
    -   バージョン8.3.0以降、このパラメータはセッションレベルでサポートされています。グローバルレベルでパラメータを変更しても、現在実行中のDDLステートメントには影響しません。変更は、新規セッションで送信されるDDLにのみ適用されます。
    -   バージョン 8.5.0 以降では、 `ADMIN ALTER DDL JOBS <job_id> BATCH_SIZE = <new_batch_size>;`実行することで、実行中の DDL ジョブのこのパラメータを変更できます。TiDB バージョン 8.5.5 より前のバージョンでは、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)が有効になっている場合、 `ADD INDEX` DDL に対してこの操作はサポートされていないことに注意してください。詳細については、 [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)を参照してください。

### tidb_ddl_reorg_priority {#tidb-ddl-reorg-priority}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `PRIORITY_LOW`
-   `PRIORITY_HIGH` `PRIORITY_NORMAL` ： `PRIORITY_LOW`
-   この変数は、第`re-organize`フェーズで第`ADD INDEX`操作を実行する際の優先順位を設定するために使用されます。
-   この変数の値は、 `PRIORITY_LOW` `PRIORITY_NORMAL`または`PRIORITY_HIGH`に設定できます。

### tidb_ddl_reorg_max_write_speed は<span class="version-mark">、v6.5.12、v7.5.5、v8.5.0 で新たに追加されました。</span> {#tidb-ddl-reorg-max-write-speed-span-class-version-mark-new-in-v6-5-12-v7-5-5-and-v8-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: `0`
-   範囲: `[0, 1PiB]`
-   この変数は、インデックスのバックフィル中に、**単一の TiDB ノードから単一の TiKV ノードへの**書き込み帯域幅を制限します。これは、インデックス作成の高速化が有効になっている場合 ( [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630)変数で制御) にのみ有効になります。[グローバルソート](/tidb-global-sort.md)が有効になっている場合、複数の TiDB ノードが TiKV に同時に書き込むことができます。クラスタ内のデータサイズが非常に大きい場合 (数十億行など)、インデックス作成の書き込み帯域幅を制限することで、アプリケーションのワークロードへの影響を効果的に軽減できます。
-   デフォルト値の`0` 、書き込み帯域幅制限がないことを意味します。
-   この変数の値は、単位を指定しても指定しなくても構いません。
    -   単位を指定せずに値を指定した場合、デフォルトの単位はバイト/秒となります。例えば、 `67108864` 1秒あたり`64MiB`を表します。
    -   値を単位付きで指定する場合、サポートされている単位は KiB、MiB、GiB、TiB です。たとえば、 `'1GiB` 」は 1 GiB/秒を表し、 `'256MiB'`は 256 MiB/秒を表します。

例：

4つのTiDBノードと複数のTiKVノードを持つクラスタがあると仮定します。このクラスタでは、各TiDBノードがインデックスのバックフィルを実行でき、リージョンはすべてのTiKVノードに均等に分散されています。1から`tidb_ddl_reorg_max_write_speed` `100MiB`設定すると、次のようになります。

-   グローバルソートが無効になっている場合、一度に TiDB ノードが TiKV に書き込むのは 1 つだけです。この場合、TiKV ノードあたりの最大書き込み帯域幅は`100MiB`です。
-   グローバルソートが有効になっている場合、4 つの TiDB ノードすべてが同時に TiKV に書き込むことができます。この場合、TiKV ノードあたりの最大書き込み帯域幅は`4 * 100MiB = 400MiB`です。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、この変数は適切な値に自動的に調整されるため、ユーザーが変更することはできません。設定を調整する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

### tidb_ddl_reorg_worker_cnt {#tidb-ddl-reorg-worker-cnt}

<CustomContent platform="tidb-cloud">

<CustomContent plan="starter,essential">

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

</CustomContent>

<CustomContent plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、このTiDB変数を変更しても、 `MODIFY COLUMN` DDLジョブにのみ影響し、 `ADD INDEX` DDLジョブには影響しません。

</CustomContent>

</CustomContent>

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、第`re-organize`フェーズにおけるDDL操作の並行性を設定するために使用されます。
-   バージョン8.3.0以降、このパラメータはセッションレベルでサポートされています。グローバルレベルでパラメータを変更しても、現在実行中のDDLステートメントには影響しません。変更は、新規セッションで送信されるDDLにのみ適用されます。
-   バージョン 8.5.0 以降では、 `ADMIN ALTER DDL JOBS <job_id> THREAD = <new_thread_count>;`実行することで、実行中の DDL ジョブのこのパラメータを変更できます。TiDB バージョン 8.5.5 より前のバージョンでは、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)が有効になっている場合、 `ADD INDEX` DDL に対してこの操作はサポートされていないことに注意してください。詳細については、 [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)を参照してください。

### <code>tidb_enable_fast_create_table</code> <span class="version-mark">v8.0.0 で追加されました。</span> {#code-tidb-enable-fast-create-table-code-span-class-version-mark-new-in-v8-0-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`より前のバージョンでは、デフォルト値は`OFF`でした。
-   この変数は[TiDB高速テーブル作成](/accelerated-table-creation.md)を有効にするかどうかを制御するために使用されます。
-   `tidb_enable_fast_create_table` 8.0.0以降、TiDBは[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)ステートメントを使用してテーブル作成を高速化することをサポートしています。
-   この変数は、v7.6.0で導入された変数[`tidb_ddl_version`](https://docs-archive.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)から名前が変更されました。v8.0.0以降、 `tidb_ddl_version`無効になります。
-   TiDB v8.5.0以降、新しく作成されるクラスタでは、高速テーブル作成機能がデフォルトで有効になり、 `tidb_enable_fast_create_table`から`ON`に設定されます。v8.4.0以前のバージョンからアップグレードされたクラスタの場合、デフォルト値の`tidb_enable_fast_create_table`は変更されません。

### tidb_default_string_match_selectivity <span class="version-mark">v6.2.0で追加</span> {#tidb-default-string-match-selectivity-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   デフォルト値: `0.8`
-   範囲: `[0, 1]`
-   この変数は、行数を推定する際のフィルタ条件における`like` `regexp`のデフォルトの選択性を設定するために使用されます。また、この変数は`rlike`これらの関数の推定を支援するためにTopNを有効にするかどうかも制御します。
-   TiDBは統計情報を使用してフィルタ条件の`like`推定しようとします。しかし、 `like`複雑な文字列に一致する場合、または`rlike`や`regexp`使用する場合、TiDBは統計情報を十分に活用できず、代わりにデフォルト値の`0.8`が選択率として設定され、結果として不正確な推定結果となることがあります。
-   この変数は、前述の動作を変更するために使用されます。この変数が`0`以外の値に設定されている場合、選択率は`0.8`ではなく、指定された変数の値になります。
-   変数が`0`に設定されている場合、TiDB は統計情報で TopN を使用して評価を行い、精度を向上させ、前述の 3 つの関数を推定する際に統計情報で NULL 値を考慮します。前提条件として、 [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510)が`2`に設定されているときに統計情報が収集されている必要があります。このような評価は、パフォーマンスに若干影響を与える可能性があります。
-   変数が`0.8`以外の値に設定されている場合、TiDBは`not like` `not rlike`推定値`not regexp`それに応じて調整します。

### tidb_disable_txn_auto_retry {#tidb-disable-txn-auto-retry}

> **警告：**
>
> バージョン8.0.0以降、この変数は非推奨となり、TiDBは楽観的トランザクションの自動再試行をサポートしなくなりました。代替策として、楽観的トランザクションの競合が発生した場合は、エラーを捕捉してアプリケーションでトランザクションを再試行するか、[悲観的な取引モード](/pessimistic-transaction.md)を使用してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、明示的な楽観的トランザクションの自動再試行を無効にするかどうかを設定するために使用されます。デフォルト値の`ON`は、TiDB でトランザクションが自動的に再試行されないことを意味し、 `COMMIT`ステートメントはアプリケーションレイヤーで処理する必要のあるエラーを返す可能性があります。

    値を`OFF`に設定すると、TiDBはトランザクションを自動的に再試行し、 `COMMIT`ステートメントからのエラーが減少します。この変更を行う際は、更新が失われる可能性があるため注意してください。

    この変数は、TiDB で自動的にコミットされる暗黙的トランザクションおよび内部的に実行されるトランザクションには影響しません。これらのトランザクションの最大再試行回数は、値`tidb_retry_limit`によって決定されます。

    詳細については、 [再試行の制限](/optimistic-transaction.md#limits-of-retry)を参照してください。

    <CustomContent platform="tidb">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は、[`max_retry_count`](/tidb-configuration-file.md#max-retry-count)によって制御されます。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は256回です。

    </CustomContent>

### tidb_distsql_scan_concurrency {#tidb-distsql-scan-concurrency}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `15`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、 `scan`操作の同時実行数を設定するために使用されます。
-   OLAPシナリオではより大きな値を使用し、OLTPシナリオではより小さな値を使用してください。
-   OLAPシナリオの場合、最大値はすべてのTiKVノードのCPUコア数を超えてはなりません。
-   テーブルにパーティションが多数ある場合、変数値を適切に減らすことで（スキャンするデータのサイズとスキャンの頻度によって決まります）、TiKVがメモリ不足（OOM）になるのを防ぐことができます。
-   `LIMIT`句のみを含む単純なクエリの場合、 `LIMIT`値が 100000 未満であれば、TiKV にプッシュダウンされるスキャン操作では、実行効率を高めるためにこの変数の値を`1`として扱います。
-   `SELECT MAX/MIN(col) FROM ...`クエリの場合、 `col`列に`MAX(col)`または`MIN(col)`関数で要求されるのと同じ順序でソートされたインデックスがある場合、TiDB はクエリを`SELECT col FROM ... LIMIT 1`に書き換えて処理し、この変数の値も`1`として処理されます。たとえば、 `SELECT MIN(col) FROM ...`の場合、 `col`列に昇順のインデックスがある場合、TiDB はクエリを`SELECT col FROM ... LIMIT 1`に書き換えてインデックスの最初の行を直接読み取ることで、 `MIN(col)`値をすばやく取得できます。
-   [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)テーブルに対するクエリの場合、この変数はスローログファイルの解析における同時実行数を制御します。

### tidb_dml_batch_size {#tidb-dml-batch-size}

> **警告：**
>
> この変数は、非推奨のバッチ DML 機能に関連付けられており、データ破損を引き起こす可能性があります。そのため、バッチ DML でこの変数を有効にすることは推奨されません。代わりに、[非トランザクションDML](/non-transactional-dml.md)を使用してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位：行
-   この値が`0`より大きい場合、TiDB は`INSERT`ようなコミット ステートメントをより小さなトランザクションにまとめて実行します。これによりメモリ使用量が削減され、一括変更によってメモリ使用量が`txn-total-size-limit`に達するのを防ぐことができます。
-   値`0`のみがACID準拠を保証します。この値を他の値に設定すると、TiDBのアトミック性と分離性の保証が損なわれます。
-   この変数を機能させるには、1 と`tidb_batch_insert`および`tidb_batch_delete`の少なくとも`tidb_enable_batch_dml`つを有効にする必要があります。

> **注記：**
>
> v7.0.0 以降、 `tidb_dml_batch_size` [`LOAD DATA`ステートメント](/sql-statements/sql-statement-load-data.md)に影響しなくなりました。

### tidb_dml_type <span class="version-mark">v8.0.0で追加</span> {#tidb-dml-type-span-class-version-mark-new-in-v8-0-0-span}

> **警告：**
>
> 一括DML実行モード（ `tidb_dml_type = "bulk"` ）は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、[問題](https://github.com/pingcap/tidb/issues)を報告してください。現在のバージョンでは、TiDBが一括DMLモードを使用して大規模なトランザクションを実行すると、TiCDC、 TiFlash、およびTiKVのresolved-tsモジュールのメモリ使用量と実行効率に影響を与え、OOM問題を引き起こす可能性があります。さらに、ロックに遭遇するとBRがブロックされ、処理に失敗する可能性があります。したがって、これらのコンポーネントまたは機能が有効になっている場合は、このモードの使用は推奨されません。

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 文字列
-   デフォルト値: `"standard"`
-   `"bulk"`オプション： `"standard"`
-   この変数は、DMLステートメントの実行モードを制御します。
    -   `"standard"`標準のDML実行モードを示し、TiDBトランザクションはコミットされる前にメモリにキャッシュされます。このモードは、競合が発生する可能性のある高並行トランザクションシナリオに適しており、推奨されるデフォルトの実行モードです。
    -   `"bulk"`パイプライン DML 実行モードを示し、大量のデータが書き込まれ、TiDB で過剰なメモリ使用量が発生するシナリオに適しています。詳細については、[パイプラインDML](/pipelined-dml.md)参照してください。

### tidb_enable_1pc <span class="version-mark">v5.0の新機能</span> {#tidb-enable-1pc-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、1つのリージョンのみに影響を与えるトランザクションに対して、1フェーズコミット機能を有効にするかどうかを指定するために使用されます。よく使用される2フェーズコミットと比較して、1フェーズコミットはトランザクションコミットのレイテンシーを大幅に削減し、スループットを向上させることができます。

> **注記：**
>
> -   デフォルト値の`ON`は、新規クラスターにのみ適用されます。クラスターが以前のバージョンのTiDBからアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   このパラメータを有効にしても、ワンフェーズコミットがトランザクションコミットのオプションモードになるだけです。実際には、最適なトランザクションコミットモードはTiDBによって決定されます。

### tidb_enable_analyze_snapshot <span class="version-mark">v6.2.0で追加</span> {#tidb-enable-analyze-snapshot-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `ANALYZE`実行する際に履歴データを読み取るか最新データを読み取るかを制御します。この変数が`ON`に設定されている場合、 `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ります。この変数が`OFF`に設定されている場合、 `ANALYZE`最新データを読み取ります。
-   v5.2より前は、 `ANALYZE`最新のデータを読み取ります。v5.2からv6.1までは、 `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ります。

> **警告：**
>
> `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ると、履歴データがガベージコレクションされるため、 `AUTO ANALYZE`の長い期間が`GC life time is shorter than transaction duration`エラーを引き起こす可能性があります。

### tidb_enable_async_commit <span class="version-mark">v5.0で追加</span> {#tidb-enable-async-commit-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、2段階トランザクションコミットの第2フェーズで非同期コミット機能を有効にして、バックグラウンドで非同期に実行するかどうかを制御します。この機能を有効にすると、トランザクションコミットのレイテンシーを短縮できます。

> **注記：**
>
> -   デフォルト値の`ON`は、新規クラスターにのみ適用されます。クラスターが以前のバージョンのTiDBからアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   このパラメータを有効にしても、非同期コミットがトランザクションコミットのオプションモードになるだけです。実際には、最適なトランザクションコミットモードはTiDBによって決定されます。

### tidb_enable_auto_analyze <span class="version-mark">v6.1.0で追加</span> {#tidb-enable-auto-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDBがテーブル統計情報をバックグラウンド操作として自動的に更新するかどうかを決定します。
-   この設定は以前はオプション`tidb.toml` （ `performance.run-auto-analyze` ）でしたが、TiDB v6.1.0以降はシステム変数に変更されました。

### tidb_enable_auto_analyze_priority_queue <span class="version-mark">v8.0.0で追加</span> {#tidb-enable-auto-analyze-priority-queue-span-class-version-mark-new-in-v8-0-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、統計情報の自動収集タスクをスケジュールするための優先度キューを有効にするかどうかを制御するために使用されます。この変数を有効にすると、TiDB は、新しく作成されたインデックスやパーティションが変更されたパーティションテーブルなど、収集する価値の高いテーブルの統計情報の収集を優先します。さらに、TiDB は健全性スコアの低いテーブルを優先し、キューの先頭に配置します。

### tidb_enable_auto_increment_in_generated {#tidb-enable-auto-increment-in-generated}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、生成列または式インデックスを作成する際に、 `AUTO_INCREMENT`列を含めるかどうかを決定するために使用されます。

### tidb_enable_batch_dml {#tidb-enable-batch-dml}

> **警告：**
>
> この変数は、非推奨のバッチ DML 機能に関連付けられており、データ破損を引き起こす可能性があります。そのため、バッチ DML でこの変数を有効にすることは推奨されません。代わりに、[非トランザクションDML](/non-transactional-dml.md)を使用してください。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨の batch-dml 機能を有効にするかどうかを制御します。有効にすると、特定のステートメントが複数のトランザクションに分割される可能性があり、これは非アトミックであるため、慎重に使用する必要があります。batch-dml を使用する場合は、操作対象のデータに対して同時実行操作がないことを確認する必要があります。この機能を動作させるには、 `tidb_batch_dml_size`に正の値を指定し、 `tidb_batch_insert`と`tidb_batch_delete`の少なくとも 1 つを有効にする必要があります。

### tidb_enable_cascades_planner {#tidb-enable-cascades-planner}

> **警告：**
>
> 現在、カスケードプランナーは実験的機能です。本番環境での使用は推奨されません。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、カスケードプランナーを有効にするかどうかを制御するために使用されます。

### tidb_enable_check_constraint <span class="version-mark">v7.2.0で追加</span> {#tidb-enable-check-constraint-span-class-version-mark-new-in-v7-2-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [`CHECK`制約](/constraints.md#check)機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_chunk_rpc <span class="version-mark">v4.0で追加</span> {#tidb-enable-chunk-rpc-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサーで`Chunk`データエンコード形式を有効にするかどうかを制御するために使用されます。

### tidb_enable_clustered_index <span class="version-mark">v5.0で追加</span> {#tidb-enable-clustered-index-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `ON`
-   `ON` `INT_ONLY`値： `OFF`
-   この変数は、デフォルトで主キーを[クラスター化インデックス](/clustered-indexes.md)として作成するかどうかを制御するために使用されます。ここでの「デフォルト」とは、ステートメントでキーワード`CLUSTERED` / `NONCLUSTERED`が明示的に指定されていないことを意味します。サポートされている値は`OFF` 、 `ON` 、および`INT_ONLY`です。
    -   `OFF` 、プライマリキーがデフォルトで非クラスター化インデックスとして作成されることを示します。
    -   `ON` 、プライマリキーがデフォルトでクラスタ化インデックスとして作成されることを示します。
    -   `INT_ONLY` 、動作が構成項目`alter-primary-key`によって制御されることを示します。4 `alter-primary-key` `true`に設定されている場合、すべての主キーはデフォルトで非クラスタ化インデックスとして作成されます。8 `false`設定されている場合、整数列で構成される主キーのみがクラスタ化インデックスとして作成されます。

### tidb_enable_ddl は<span class="version-mark">v6.3.0 で追加されました。</span> {#tidb-enable-ddl-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   可能な`ON` : `OFF`
-   この変数は、対応する TiDB インスタンスが DDL の所有者になれるかどうかを制御します。現在の TiDB クラスタに TiDB インスタンスが 1 つしかない場合、そのインスタンスが DDL の所有者になることを防ぐことはできません。つまり、この変数を`OFF`に設定することはできません。

### tidb_enable_collect_execution_info {#tidb-enable-collect-execution-info}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー クエリ ログに各オペレーターの実行情報を記録するかどうか、および[インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)を記録するかどうかを制御します。

### tidb_enable_column_tracking <span class="version-mark">v5.4.0で追加</span> {#tidb-enable-column-tracking-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> バージョン8.3.0以降、この変数は非推奨となりました。TiDBはデフォルトで述語列を追跡します。詳細については、 [`tidb_analyze_column_options`](#tidb_analyze_column_options-new-in-v830)参照してください。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`より前のバージョンでは、デフォルト値は`OFF`でした。
-   この変数は、TiDB が`PREDICATE COLUMNS`を収集できるようにするかどうかを制御します。収集を有効にした後、無効にすると、以前に収集した`PREDICATE COLUMNS`の情報はクリアされます。詳細は[いくつかの列の統計情報を収集する](/statistics.md#collect-statistics-on-some-columns)ご覧ください。

### tidb_enable_enhanced_security {#tidb-enable-enhanced-security}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: `OFF`
-   この変数は、接続先のTiDBサーバーでSecurity拡張モード（SEM）が有効になっているかどうかを示します。値を変更するには、TiDBサーバーの設定ファイルで値「 `enable-sem`を変更し、TiDBサーバーを再起動する必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`
-   この変数は読み取り専用です。TiDB TiDB Cloudでは、Security強化モード（SEM）がデフォルトで有効になっています。

</CustomContent>

-   SEMは、 [セキュリティ強化Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux)などのシステムの設計に触発されています。MySQL `SUPER`権限を持つユーザーの能力を制限し、代わりに`RESTRICTED`権限を付与する必要があります。これらのきめ細かい権限には以下が含まれます。
    -   `RESTRICTED_TABLES_ADMIN` : `mysql`スキーマのシステム テーブルにデータを書き込む機能と、 `information_schema`テーブルの機密列を表示する機能。
    -   `RESTRICTED_STATUS_ADMIN` : コマンド`SHOW STATUS`内の機密変数を表示する機能。
    -   `RESTRICTED_VARIABLES_ADMIN` : `SHOW [GLOBAL] VARIABLES`と`SET`の機密変数を表示および設定する機能。
    -   `RESTRICTED_USER_ADMIN` ：他のユーザーが変更を加えたり、ユーザーアカウントを削除したりすることを阻止する機能。

### tidb_enable_exchange_partition {#tidb-enable-exchange-partition}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は[`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、デフォルトでは`exchange partitions with tables`有効になっています。
-   この変数はバージョン6.3.0以降非推奨となりました。値はデフォルト値の`ON`に固定され、つまり`exchange partitions with tables`デフォルトで有効になります。

### tidb_enable_extended_stats {#tidb-enable-extended-stats}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB がオプティマイザーをガイドする拡張統計を収集できるかどうかを示します。詳細については、[拡張統計入門](/extended-statistics.md)参照してください。

### tidb_enable_external_ts_read は<span class="version-mark">v6.4.0 で追加されました。</span> {#tidb-enable-external-ts-read-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数が`ON`に設定されている場合、TiDB は[`tidb_external_ts`](#tidb_external_ts-new-in-v640)で指定されたタイムスタンプを持つデータを読み取ります。

### tidb_external_ts <span class="version-mark">v6.4.0で追加</span> {#tidb-external-ts-span-class-version-mark-new-in-v6-4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-new-in-v640)が`ON`に設定されている場合、TiDB はこの変数で指定されたタイムスタンプを持つデータを読み取ります。

### tidb_enable_fast_analyze {#tidb-enable-fast-analyze}

> **警告：**
>
> バージョン7.5.0以降、この変数は非推奨となりました。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計情報`Fast Analyze`機能を有効にするかどうかを設定するために使用されます。
-   統計情報`Fast Analyze`機能が有効になっている場合、TiDBは約10,000行のデータをランダムにサンプリングして統計情報とします。データの分布が不均一であったり、データサイズが小さい場合、統計情報の精度は低くなります。そのため、例えば誤ったインデックスを選択するなど、最適な実行プランが立てられない可能性があります。通常の`Analyze`ステートメントの実行時間が許容範囲内であれば、 `Fast Analyze`機能を無効にすることをお勧めします。

### tidb_enable_fast_table_check は<span class="version-mark">v7.2.0 で追加されました。</span> {#tidb-enable-fast-table-check-span-class-version-mark-new-in-v7-2-0-span}

> **注記：**
>
> この変数は[多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)およびプレフィックス インデックスに対しては機能しません。

-   範囲: セッション | グローバル
-   クラスターに永続化：はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、テーブル内のデータとインデックスの整合性を迅速にチェックするために、チェックサムベースの手法を使用するかどうかを制御するために使用されます。デフォルト値の`ON`は、この機能がデフォルトで有効になっていることを意味します。
-   この変数が有効になっている場合、TiDB は[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントをより高速に実行できます。

### tidb_enable_foreign_key は<span class="version-mark">v6.3.0 で追加されました。</span> {#tidb-enable-foreign-key-span-class-version-mark-new-in-v6-3-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値：v6.6.0より前のバージョンではデフォルト値は`OFF`です。v6.6.0以降ではデフォルト値は`ON`です。
-   この変数は、 `FOREIGN KEY`機能を有効にするかどうかを制御します。

### tidb_enable_gc_aware_memory_track {#tidb-enable-gc-aware-memory-track}

> **警告：**
>
> この変数はTiDBのデバッグ用内部変数です。将来のリリースで削除される可能性があります。この変数を設定**しないでください**。

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、GC対応メモリトラックを有効にするかどうかを制御します。

### tidb_enable_global_index <span class="version-mark">v7.6.0で追加</span> {#tidb-enable-global-index-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、パーティション化されたテーブルに対して[グローバルインデックス](/global-indexes.md)なインデックスの作成をサポートするかどうかを制御します。この変数を有効にすると、TiDB は、インデックス定義で`GLOBAL`指定することで**、パーティション式で使用されているすべての列を含まない**一意のインデックスを作成できるようになります。
-   この変数は v8.4.0 以降非推奨になりました。その値はデフォルト値`ON`に固定されています。つまり、[グローバルインデックス](/global-indexes.md)がデフォルトで有効になります。

### tidb_enable_lazy_cursor_fetch <span class="version-mark">v8.3.0で追加</span> {#tidb-enable-lazy-cursor-fetch-span-class-version-mark-new-in-v8-3-0-span}

> **警告：**
>
> この変数で制御される機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

<CustomContent platform="tidb">

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   可能な`ON` : `OFF`
-   この変数は[カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)機能の動作を制御します。
    -   カーソルフェッチが有効で、この変数が`OFF`に設定されている場合、TiDB はステートメント実行の開始時にすべてのデータを読み込み、そのデータを TiDB のメモリに格納し、クライアントが指定した`FetchSize`に基づいて、後続のクライアント読み取りのためにクライアントに返します。結果セットが大きすぎる場合、TiDB は一時的に結果をハードディスクに書き込むことがあります。
    -   カーソルフェッチが有効で、この変数が`ON`に設定されている場合、TiDB はすべてのデータを一度に TiDB ノードに読み込むのではなく、クライアントがフェッチするにつれてデータを TiDB ノードに段階的に読み込みます。
-   この変数によって制御される機能には、以下の制限があります。
    -   明示的なトランザクション内のステートメントはサポートしていません。
    -   `TableReader` `IndexLookUp` `IndexReader` `Projection`のみ`Selection`含む実行プランのみをサポートします。
    -   Lazy Cursor Fetch を使用するステートメントの場合、実行情報は[声明の概要](/statement-summary-tables.md)と[スロークエリログ](/identify-slow-queries.md)ログに表示されません。
-   サポートされていないシナリオでは、この変数を`OFF`に設定した場合と同じ動作になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   可能な`ON` : `OFF`
-   この変数は[カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)機能の動作を制御します。
    -   カーソルフェッチが有効で、この変数が`OFF`に設定されている場合、TiDB はステートメント実行の開始時にすべてのデータを読み込み、そのデータを TiDB のメモリに格納し、クライアントが指定した`FetchSize`に基づいて、後続のクライアント読み取りのためにクライアントに返します。結果セットが大きすぎる場合、TiDB は一時的に結果をハードディスクに書き込むことがあります。
    -   カーソルフェッチが有効で、この変数が`ON`に設定されている場合、TiDB はすべてのデータを一度に TiDB ノードに読み込むのではなく、クライアントがフェッチするにつれてデータを TiDB ノードに段階的に読み込みます。
-   この変数によって制御される機能には、以下の制限があります。
    -   明示的なトランザクション内のステートメントはサポートしていません。
    -   `TableReader` `IndexLookUp` `IndexReader` `Projection`のみ`Selection`含む実行プランのみをサポートします。
    -   Lazy Cursor Fetch を使用するステートメントの場合、実行情報は[声明の概要](/statement-summary-tables.md)と[スロークエリログ](https://docs.pingcap.com/tidb/stable/identify-slow-queries)ログに表示されません。
-   サポートされていないシナリオでは、この変数を`OFF`に設定した場合と同じ動作になります。

</CustomContent>

### tidb_enable_non_prepared_plan_cache {#tidb-enable-non-prepared-plan-cache}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は[準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。
-   この機能を有効にすると、メモリとCPUのオーバーヘッドが増加する可能性があり、すべての状況に適しているとは限りません。実際の使用状況に応じて、この機能を有効にするかどうかを判断してください。

### tidb_enable_non_prepared_plan_cache_for_dml <span class="version-mark">v7.1.0 で追加</span> {#tidb-enable-non-prepared-plan-cache-for-dml-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> DML ステートメント用の未準備実行プラン キャッシュは実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF` 。
-   この変数は、DML ステートメントの[準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)キャッシュ機能を有効にするかどうかを制御します。

### tidb_enable_gogc_tuner <span class="version-mark">v6.4.0で追加</span> {#tidb-enable-gogc-tuner-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、GOGC Tunerを有効にするかどうかを制御します。

### tidb_enable_historical_stats {#tidb-enable-historical-stats}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`より前のバージョンでは、デフォルト値は`ON`でした。
-   この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`で、これは履歴統計がデフォルトで無効になっていることを意味します。

### tidb_enable_historical_stats_for_capture {#tidb-enable-historical-stats-for-capture}

> **警告：**
>
> この変数で制御される機能は、現在のTiDBバージョンでは完全には動作しません。デフォルト値を変更しないでください。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CAPTURE`で取得される情報にデフォルトで過去の統計情報が含まれるかどうかを制御します。デフォルト値の`OFF` 、デフォルトでは過去の統計情報が含まれないことを意味します。

### tidb_enable_index_merge <span class="version-mark">v4.0で追加</span> {#tidb-enable-index-merge-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> -   TiDBクラスタをv4.0.0より前のバージョンからv5.4.0以降にアップグレードした後、実行プランの変更によるパフォーマンス低下を防ぐため、この変数はデフォルトで無効になります。
>
> -   TiDBクラスタをv4.0.0以降からv5.4.0以降にアップグレードした後も、この変数はアップグレード前の設定のままです。
>
> -   バージョン5.4.0以降、新規にデプロイされたTiDBクラスタでは、この変数はデフォルトで有効になっています。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックスのマージ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_index_merge_join {#tidb-enable-index-merge-join}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `IndexMergeJoin`演算子を有効にするかどうかを指定します。
-   この変数はTiDBの内部動作のみに使用されます。変更することは**推奨されません**。変更すると、データの正確性に影響が出る可能性があります。

### tidb_enable_legacy_instance_scope <span class="version-mark">v6.0.0で追加</span> {#tidb-enable-legacy-instance-scope-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数を使用すると、スコープが`INSTANCE`変数を、 `SET SESSION`および`SET GLOBAL`構文を使用して設定できます。
-   このオプションは、以前のバージョンのTiDBとの互換性を保つため、デフォルトで有効になっています。

### tidb_enable_list_partition <span class="version-mark">v5.0で追加</span> {#tidb-enable-list-partition-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `LIST (COLUMNS) TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。
-   この変数はv8.4.0以降非推奨です。その値はデフォルト値`ON`に固定されます。つまり、 [List パーティショニング](/partitioned-table.md#list-partitioning)はデフォルトで有効になります。

### tidb_enable_local_txn {#tidb-enable-local-txn}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は未公開機能に使用されます。**変数の値を変更しないでください**。

### tidb_enable_metadata_lock は<span class="version-mark">v6.3.0 で追加されました。</span> {#tidb-enable-metadata-lock-span-class-version-mark-new-in-v6-3-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、[メタデータロック](/metadata-lock.md)機能を有効にするかどうかを設定するために使用されます。この変数を設定する際は、クラスター内で実行中の DDL ステートメントがないことを確認してください。そうでない場合、データが正しくない、または矛盾が生じる可能性があります。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、この変数は読み取り専用です。変更する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

### tidb_enable_mutation_checker <span class="version-mark">v6.0.0で追加</span> {#tidb-enable-mutation-checker-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、DML ステートメントの実行中にデータとインデックス間の一貫性をチェックするために使用されるツールである TiDB ミューテーション チェッカーを有効にするかどうかを制御するために使用されます。チェッカーがステートメントに対してエラーを返した場合、TiDB はステートメントの実行をロールバックします。この変数を有効にすると、CPU 使用率がわずかに増加します。詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。
-   v6.0.0以降のバージョンの新規クラスターの場合、デフォルト値は`ON`です。v6.0.0より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_enable_new_cost_interface <span class="version-mark">v6.2.0で追加</span> {#tidb-enable-new-cost-interface-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB v6.2.0では、以前のコストモデルの実装がリファクタリングされています。この変数は、リファクタリングされたコストモデルの実装を有効にするかどうかを制御します。
-   この変数はデフォルトで有効になっています。なぜなら、リファクタリングされたコストモデルは以前と同じコスト計算式を使用しており、計画決定に影響を与えないからです。
-   クラスターがv6.1からv6.2にアップグレードされた場合、この変数は`OFF`ままとなり、手動で有効にすることをお勧めします。クラスターがv6.1より前のバージョンからアップグレードされた場合、この変数はデフォルトで`ON`に設定されます。

### tidb_enable_new_only_full_group_by_check <span class="version-mark">v6.1.0の新機能</span> {#tidb-enable-new-only-full-group-by-check-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB が`ONLY_FULL_GROUP_BY`チェックを実行する際の動作を制御します。3 `ONLY_FULL_GROUP_BY`詳細については、 [MySQLドキュメント](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)を参照してください。v6.1.0 では、TiDB はこのチェックをより厳密かつ正確に処理します。
-   バージョンアップグレードによって発生する可能性のある互換性の問題を回避するため、v6.1.0 ではこの変数のデフォルト値は`OFF`に設定されています。

### tidb_enable_noop_functions <span class="version-mark">v4.0で追加</span> {#tidb-enable-noop-functions-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `OFF`
-   `ON` `WARN`値： `OFF`
-   TiDBはデフォルトでは、まだ実装されていない機能の構文を使用しようとするとエラーを返します。変数の値を`ON`に設定すると、TiDBは利用できない機能のケースを黙って無視します。これは、SQLコードを変更できない場合に役立ちます。
-   `noop`関数を有効にすると、以下の動作が制御されます。
    -   `LOCK IN SHARE MODE`構文
    -   `SQL_CALC_FOUND_ROWS`構文
    -   `START TRANSACTION READ ONLY`と`SET TRANSACTION READ ONLY`構文
    -   `tx_read_only` `super_read_only` `sql_auto_is_null` `read_only` `transaction_read_only` `offline_mode`
    -   `GROUP BY <expr> ASC|DESC`構文

> **警告：**
>
> デフォルト値の`OFF`のみが安全と言えます。3 `tidb_enable_noop_functions=1`設定すると、TiDBが特定の構文をエラーなしで無視することを許可するため、アプリケーションで予期しない動作が発生する可能性があります。たとえば、構文`START TRANSACTION READ ONLY`は許可されますが、トランザクションは読み書きモードのままになります。

### tidb_enable_noop_variables は<span class="version-mark">v6.2.0 で追加されました。</span> {#tidb-enable-noop-variables-span-class-version-mark-new-in-v6-2-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   変数の値を`OFF`に設定すると、TiDBは次のように動作します。
    -   `SET`使用して`noop`変数を設定すると、TiDB は`"setting *variable_name* has no effect in TiDB"`警告を返します。
    -   結果`SHOW [SESSION | GLOBAL] VARIABLES`には`noop`変数は含まれていません。
    -   `SELECT`使用して`noop`変数を読み取ると、TiDB は`"variable *variable_name* has no effect in TiDB"`警告を返します。
-   TiDBインスタンスが変数`noop`を設定および読み取ったかどうかを確認するには、 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;`ステートメントを使用できます。

### tidb_enable_null_aware_anti_join <span class="version-mark">v6.3.0で追加</span> {#tidb-enable-null-aware-anti-join-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値：v7.0.0より前のバージョンではデフォルト値は`OFF`です。v7.0.0以降ではデフォルト値は`ON`です。
-   タイプ: ブール値
-   この変数は、特別な集合演算子`NOT IN`および`!= ALL`によって開始されるサブクエリによって ANTI JOIN が生成された場合に TiDB が Null Aware Hash Join を適用するかどうかを制御します。
-   以前のバージョンからv7.0.0以降のクラスターにアップグレードすると、この機能は自動的に有効になり、この変数は`ON`に設定されます。

### tidb_enable_outer_join_reorder <span class="version-mark">v6.1.0で追加</span> {#tidb-enable-outer-join-reorder-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   v6.1.0 以降、TiDB の[結合したテーブルの再配置](/join-reorder.md)アルゴリズムは、Outer Join をサポートしています。この変数は、TiDB が Outer Join に対する Join Reorder のサポートを有効にするかどうかを制御します。
-   TiDBの以前のバージョンからクラスターをアップグレードする場合は、以下の点に注意してください。

    -   アップグレード前の TiDB バージョンが v6.1.0 より前の場合、アップグレード後のこの変数のデフォルト値は`ON`なります。
    -   アップグレード前のTiDBのバージョンがv6.1.0以降の場合、アップグレード後の変数のデフォルト値はアップグレード前の値に従います。

### <code>tidb_enable_inl_join_inner_multi_pattern</code> <span class="version-mark">v7.0.0で追加</span> {#code-tidb-enable-inl-join-inner-multi-pattern-code-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値： `ON`以前のバージョンではデフォルト値は`OFF`です。
-   この変数は、内部テーブルに演算子が`Selection` 、 `Aggregation` 、または`Projection`ある場合に、インデックス結合がサポートされるかどうかを制御します。デフォルト値の`OFF`このシナリオではインデックス結合がサポートされないことを意味します。
-   TiDBクラスタをv7.0.0より前のバージョンからv8.4.0以降にアップグレードすると、この変数はデフォルトで`OFF`に設定され、このシナリオではインデックス結合がサポートされていないことを示します。

### tidb_enable_instance_plan_cache <span class="version-mark">v8.4.0で追加</span> {#tidb-enable-instance-plan-cache-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> 現在、インスタンスプランキャッシュは実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、インスタンス プラン キャッシュ機能を有効にするかどうかを制御します。この機能はインスタンス レベルの実行プラン キャッシュを実装しており、同じ TiDB インスタンス内のすべてのセッションが実行プラン キャッシュを共有できるため、メモリ使用率が向上します。インスタンス プラン キャッシュを有効にする前に、セッション レベル[準備された実行プランキャッシュ](/sql-prepared-plan-cache.md)キャッシュ[準備されていない実行プランのキャッシュ](/sql-non-prepared-plan-cache.md)を無効にすることをお勧めします。

### tidb_enable_ordered_result_mode {#tidb-enable-ordered-result-mode}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   最終出力結果を自動的にソートするかどうかを指定します。
-   例えば、この変数を有効にすると、TiDB は`SELECT a, MAX(b) FROM t GROUP BY a` `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`として処理します。

### tidb_enable_paging は<span class="version-mark">v5.4.0 で追加されました。</span> {#tidb-enable-paging-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ページング方式を使用してコプロセッサ要求を送信するかどうかを制御します。TiDB バージョン (v5.4.0、v6.2.0) では、この変数は`IndexLookup`演算子にのみ有効です。v6.2.0 以降では、この変数はグローバルに有効です。v6.4.0 以降、この変数のデフォルト値は`OFF`から`ON`に変更されました。
-   ユーザーシナリオ：

    -   すべてのOLTPシナリオにおいて、ページング方式を使用することが推奨されます。
    -   `IndexLookup`と`Limit`使用する読み取りクエリで、 `Limit` `IndexScan`にプッシュダウンできない場合、読み取りクエリのレイテンシーが高くなり、TiKV `Unified read pool CPU`の使用率が高くなる可能性があります。このような場合、 `Limit`演算子は少量のデータしか必要としないため、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540) `ON`に設定すると、TiDBが処理するデータ量が少なくなり、クエリのレイテンシーとリソース消費が削減されます。
    -   [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用したデータエクスポートやフルテーブルスキャンなどのシナリオでは、ページングを有効にすることで、TiDBプロセスのメモリ消費量を効果的に削減できます。

> **注記：**
>
> TiFlashの代わりにTiKVをstorageエンジンとして使用するOLAPシナリオでは、ページングを有効にすると、場合によってはパフォーマンスが低下する可能性があります。パフォーマンスが低下した場合は、この変数を使用してページングを無効にするか、 [`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-new-in-v620)および[`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-new-in-v630)変数を使用してページングサイズの行範囲を調整することを検討してください。

### tidb_enable_parallel_apply <span class="version-mark">v5.0で追加</span> {#tidb-enable-parallel-apply-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、演算子`Apply`同時実行を有効にするかどうかを制御します。同時実行の数は、変数`tidb_executor_concurrency`で制御されます。演算子`Apply`は相関サブクエリを処理し、デフォルトでは同時実行が有効になっていないため、実行速度が遅くなります。この変数の値を`1`に設定すると、同時実行数を増やして実行速度を向上させることができます。現在、演算子`Apply`の同時実行はデフォルトで無効になっています。

### tidb_enable_parallel_hashagg_spill <span class="version-mark">v8.0.0で追加</span> {#tidb-enable-parallel-hashagg-spill-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB が並列 HashAgg アルゴリズムでディスク スピルをサポートするかどうかを制御します。この変数が`ON`場合、HashAgg オペレータは、あらゆる並列条件下でメモリ使用量に基づいてデータ スピルを自動的にトリガーし、パフォーマンスとデータ スループットのバランスを取ることができます。この変数を`OFF`に設定することは推奨されません。v8.2.0 以降では、 `OFF`に設定するとエラーが報告されます。この変数は将来のリリースで非推奨になります。

### tidb_enable_pipelined_window_function {#tidb-enable-pipelined-window-function}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は[ウィンドウ関数](/functions-and-operators/window-functions.md)のパイプライン実行アルゴリズムを使用するかどうかを指定します。

### tidb_enable_plan_cache_for_param_limit <span class="version-mark">v6.6.0で追加</span> {#tidb-enable-plan-cache-for-param-limit-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュ が`LIMIT`パラメータとして変数 ( `LIMIT ?` ) を持つ実行プランをキャッシュするかどうかを制御します。デフォルト値は`ON`で、これはプリペアドプランキャッシュ がそのような実行プランのキャッシュをサポートすることを意味します。Prepared プリペアドプランキャッシュ は、 10000 を超える変数を持つ実行プランのキャッシュをサポートしないことに注意してください。

### tidb_enable_plan_cache_for_subquery <span class="version-mark">v7.0.0で追加</span> {#tidb-enable-plan-cache-for-subquery-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュがサブクエリを含むクエリをキャッシュするかどうかを制御します。

### tidb_enable_plan_replayer_capture {#tidb-enable-plan-replayer-capture}

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、機能`PLAN REPLAYER CAPTURE`を有効にするかどうかを制御します。デフォルト値の`ON` 、機能`PLAN REPLAYER CAPTURE`を有効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は[`PLAN REPLAYER CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)を有効にするかどうかを制御します。デフォルト値の`ON` `PLAN REPLAYER CAPTURE`機能を有効にすることを意味します。

</CustomContent>

### tidb_enable_plan_replayer_continuous_capture <span class="version-mark">v7.0.0で追加</span> {#tidb-enable-plan-replayer-continuous-capture-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CONTINUOUS CAPTURE`機能を有効にするかどうかを制御します。デフォルト値の`OFF` 、その機能を無効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は[`PLAN REPLAYER CONTINUOUS CAPTURE`機能）](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)を有効にするかどうかを制御します。デフォルト値の`OFF`は、この機能を無効にすることを意味します。

</CustomContent>

### tidb_enable_point_get_cache {#tidb-enable-point-get-cache}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   テーブルロックタイプを[`LOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)で`READ`に設定した場合、この変数を`ON`に設定すると、ポイントクエリ結果のキャッシュが有効になり、繰り返しクエリのオーバーヘッドが削減され、ポイントクエリのパフォーマンスが向上します。

### tidb_enable_prepared_plan_cache <span class="version-mark">v6.1.0で追加</span> {#tidb-enable-prepared-plan-cache-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   [プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)を有効にするかどうかを決定します。有効にすると、 `Prepare`と`Execute`の実行計画がキャッシュされるため、後続の実行では実行計画の最適化がスキップされ、パフォーマンスが向上します。
-   この設定は以前はオプション`tidb.toml` （ `prepared-plan-cache.enabled` ）でしたが、TiDB v6.1.0以降はシステム変数に変更されました。

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">v6.4.0で追加</span> {#tidb-enable-prepared-plan-cache-memory-monitor-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュにキャッシュされた実行プランによって消費されるメモリをカウントするかどうかを制御します。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)ご覧ください。

### tidb_enable_pseudo_for_outdated_stats は<span class="version-mark">v5.3.0 で追加されました。</span> {#tidb-enable-pseudo-for-outdated-stats-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計情報が古い場合に、オプティマイザがテーブルの統計情報を使用するかどうかの動作を制御します。

<CustomContent platform="tidb">

-   オプティマイザは、テーブルの統計情報が古いかどうかを次のように判断します。テーブルに対して最後に統計情報を取得する処理`ANALYZE`が実行されてから、テーブルの行の80%が変更された場合（変更された行数を総行数で割った値）、オプティマイザはこのテーブルの統計情報が古いと判断します。この比率は[`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)設定を使用して変更できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   オプティマイザは、テーブルの統計情報が古くなっているかどうかを次のように判断します。テーブルに対して最後に統計情報を取得するために`ANALYZE`実行されてから、テーブルの行の80%が変更された場合（変更された行数を総行数で割った値）、オプティマイザはこのテーブルの統計情報が古くなっていると判断します。

</CustomContent>

-   デフォルトでは（変数の値が`OFF`場合）、テーブルの統計情報が古くなっている場合でも、オプティマイザは引き続きテーブルの統計情報を使用します。変数の値を`ON`に設定すると、オプティマイザは、行の総数を除いてテーブルの統計情報が信頼できないと判断します。そして、オプティマイザは擬似統計情報を使用します。
-   テーブル上のデータが頻繁に変更されるにもかかわらず、そのテーブルに対してタイムリーに`ANALYZE`実行されない場合、実行プランを安定させるために、変数の値を`OFF`に設定することをお勧めします。

### tidb_enable_rate_limit_action {#tidb-enable-rate-limit-action}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、データを読み取るオペレータに対して動的メモリ制御機能を有効にするかどうかを制御します。デフォルトでは、このオペレータは、 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)データ読み取りに許可する最大スレッド数を有効にします。単一の SQL ステートメントのメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超えると、データを読み取るオペレータは 1 つのスレッドを停止します。

<CustomContent platform="tidb">

-   データを読み取るオペレーターにスレッドが 1 つだけ残っており、単一の SQL ステートメントのメモリ使用量が常に[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超える場合、この SQL ステートメントは[データをディスクに書き出す](/system-variables.md#tidb_enable_tmp_storage_on_oom)などの他のメモリ制御動作をトリガーします。
-   この変数は、SQL文がデータの読み取りのみを行う場合にメモリ使用量を効果的に制御します。結合や集計などの計算操作が必要な場合、メモリ使用量は`tidb_mem_quota_query`の制御下にない可能性があり、メモリ不足（OOM）のリスクが高まります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   データを読み取るオペレータに残っているスレッドが1つしかなく、単一のSQLステートメントのメモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超え続ける場合、このSQLステートメントは、データをディスクに書き出すなどの他のメモリ制御動作をトリガーします。

</CustomContent>

### tidb_enable_resource_control <span class="version-mark">v6.6.0で追加</span> {#tidb-enable-resource-control-span-class-version-mark-new-in-v6-6-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は[リソース制御機能](/tidb-resource-control-ru-groups.md)のスイッチです。この変数が`ON`に設定されている場合、TiDB クラスターはリソース グループに基づいてアプリケーション リソースを分離できます。

### tidb_enable_reuse_chunk <span class="version-mark">v6.4.0で追加</span> {#tidb-enable-reuse-chunk-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   `ON`オプション： `OFF`
-   この変数は、TiDBがチャンクオブジェクトのキャッシュを有効にするかどうかを制御します。値が`ON`の場合、TiDBはキャッシュされたチャンクオブジェクトの使用を優先し、要求されたオブジェクトがキャッシュに存在しない場合にのみシステムに要求します。値が`OFF`場合、TiDBはシステムから直接チャンクオブジェクトを要求します。

### tidb_enable_shared_lock_promotion <span class="version-mark">v8.3.0で追加</span> {#tidb-enable-shared-lock-promotion-span-class-version-mark-new-in-v8-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、共有ロックを排他ロックにアップグレードする機能を有効にするかどうかを制御します。TiDB はデフォルトでは`SELECT LOCK IN SHARE MODE`サポートしていません。変数の値が`ON`の場合、TiDB は`SELECT LOCK IN SHARE MODE`ステートメントを`SELECT FOR UPDATE`にアップグレードし、悲観的ロックを追加しようとします。この変数のデフォルト値は`OFF`であり、これは共有ロックを排他ロックにアップグレードする機能が無効になっていることを意味します。
-   この変数を有効にすると、 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)が有効になっているかどうかに関わらず、 `SELECT LOCK IN SHARE MODE`ステートメントに効果が適用されます。

### tidb_enable_slow_log {#tidb-enable-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スローログ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_tmp_storage_on_oom {#tidb-enable-tmp-storage-on-oom}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   `ON`オプション： `OFF`
-   単一の SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部のオペレーターに対して一時storageを有効にするかどうかを制御します。
-   バージョン6.3.0より前のバージョンでは、TiDB構成項目`oom-use-tmp-storage`を使用してこの機能を有効または無効にできます。クラスターをバージョン6.3.0以降にアップグレードすると、TiDBクラスターはこの変数を自動的に値`oom-use-tmp-storage`で初期化します。その後、値`oom-use-tmp-storage`を変更しても効果は**ありません**。

### tidb_enable_stats_owner は<span class="version-mark">v8.4.0 で追加されました。</span> {#tidb-enable-stats-owner-span-class-version-mark-new-in-v8-4-0-span}

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   可能な`ON` : `OFF`
-   この変数は、対応する TiDB インスタンスが[統計情報の自動更新](/statistics.md#automatic-update)タスクを実行できるかどうかを制御します。現在の TiDB クラスタに TiDB インスタンスが 1 つしかない場合、このインスタンスで統計の自動更新を無効にすることはできません。つまり、この変数を`OFF`に設定することはできません。

### tidb_enable_stmt_summary <span class="version-mark">v3.0.4で追加</span> {#tidb-enable-stmt-summary-span-class-version-mark-new-in-v3-0-4-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ステートメントサマリー機能を有効にするかどうかを制御するために使用されます。有効にすると、SQL実行時間などのSQL実行情報がシステムテーブル`information_schema.STATEMENTS_SUMMARY`に記録され、SQLパフォーマンスの問題を特定してトラブルシューティングするために役立ちます。

### tidb_enable_strict_double_type_check <span class="version-mark">v5.0で追加</span> {#tidb-enable-strict-double-type-check-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、タイプ`DOUBLE`の無効な定義を持つテーブルを作成できるかどうかを制御するために使用されます。この設定は、タイプの検証がそれほど厳格ではなかった以前のバージョンのTiDBからのアップグレードパスを提供することを目的としています。
-   デフォルト値の`ON`はMySQLと互換性があります。

例えば、浮動小数点型の精度は保証されないため、型`DOUBLE(10)`は無効とみなされます。3 `tidb_enable_strict_double_type_check` `OFF`に変更すると、次の表が作成されます。

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
> この設定はタイプ`DOUBLE`にのみ適用されます。MySQLでは`FLOAT`タイプに対して精度指定が可能なためです。この動作はMySQL 8.0.17以降非推奨となり、 `FLOAT`または`DOUBLE`のタイプに対して精度を指定することは推奨されません。

### tidb_enable_table_partition {#tidb-enable-table-partition}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `ON`
-   この変数は v8.4.0 以降非推奨になりました。その値はデフォルト値`ON`に固定されます。つまり、[テーブルパーティショニング](/partitioned-table.md)はデフォルトで有効になります。

### tidb_enable_telemetry <span class="version-mark">v4.0.2で追加</span> {#tidb-enable-telemetry-span-class-version-mark-new-in-v4-0-2-span}

> **警告：**
>
> -   バージョン8.1.0より前のバージョンでは、TiDBは定期的にテレメトリデータをPingCAPに報告します。
> -   バージョン8.1.0から8.5.1までは、TiDBはテレメトリ機能を削除しており、変数`tidb_enable_telemetry`もはや有効ではありません。この変数は、以前のバージョンとの互換性のためにのみ保持されています。
> -   バージョン8.5.3以降、TiDBはテレメトリ機能を復活させました。ただし、テレメトリ関連の情報はローカルにのみ記録され、ネットワーク経由でPingCAPにデータは送信されなくなりました。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`以降、デフォルト値は`OFF`から`ON`に変更されました。

<CustomContent platform="tidb">

-   この変数は、TiDB でテレメトリ機能を有効にするかどうかを制御します。v8.5.3 以降、この変数は TiDB インスタンスの[`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)設定項目が`true`に設定されている場合にのみ有効になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">v6.3.0で追加</span> {#tidb-enable-tiflash-read-for-write-stmt-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は`UPDATE` `INSERT` `DELETE`含むSQL文の読み取り操作をTiFlashにプッシュダウンできるかどうかを制御します。例：

    -   `INSERT INTO SELECT`ステートメントでクエリが`SELECT` (典型的な使用シナリオ:[TiFlashクエリ結果の具体化](/tiflash/tiflash-results-materialization.md))
    -   `UPDATE`と`DELETE`ステートメントで条件フィルタリングを`WHERE`
-   バージョン 7.1.0 以降、この変数は非推奨です。tidb_allow_mpp [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)の場合、オプティマイザは、 [SQLモード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定します。TiDB では、現在のセッションの SQL [SQLモード](/sql-mode.md)が厳密でない場合（つまり、 `INSERT INTO SELECT` `sql_mode` `DELETE` `STRICT_TRANS_TABLES` `INSERT` `STRICT_ALL_TABLES` `UPDATE` TiFlashにプッシュダウンできることに注意してください。

### tidb_enable_top_sql <span class="version-mark">v5.4.0で追加</span> {#tidb-enable-top-sql-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、 [Top SQL](/dashboard/top-sql.md)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

### tidb_enable_tso_follower_proxy <span class="version-mark">v5.3.0で追加</span> {#tidb-enable-tso-follower-proxy-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TSOFollowerプロキシ機能を有効にするかどうかを制御します。値が`OFF`の場合、TiDBはPDリーダーからのみTSOを取得します。値が`ON`の場合、TiDBはTSO要求をすべてのPDサーバーに均等に分散し、PDフォロワーもTSO要求を処理できるため、PDリーダーのCPU負荷が軽減されます。
-   TSOFollowerプロキシを有効にするシナリオ：
    -   TSOリクエストの負荷が高いため、PDリーダーのCPUがボトルネックとなり、TSO RPCリクエストのレイテンシーが増大する。
    -   TiDBクラスタには多数のTiDBインスタンスが存在するため、 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)の値を増やしても、TSO RPCリクエストの高レイテンシーの問題は解消されません。

> **注記：**
>
> -   PDリーダーのCPU使用率のボトルネック以外の理由（ネットワークの問題など）でTSO RPCのレイテンシーが増加したとします。この場合、TSOFollowerプロキシを有効にすると、TiDBの実行レイテンシーが増加し、クラスタのQPSパフォーマンスに影響を与える可能性があります。
> -   この機能は[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)と互換性がありません。この機能を有効にすると、[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)は有効になりません。

### tidb_enable_unsafe_substitute <span class="version-mark">v6.3.0で追加</span> {#tidb-enable-unsafe-substitute-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、式を生成された列に安全でない方法で置き換えるかどうかを制御します。デフォルト値は`OFF`で、これはデフォルトで安全でない置換が無効になっていることを意味します。詳細については、[生成された列](/generated-columns.md)参照してください。

### tidb_enable_vectorized_expression <span class="version-mark">v4.0で追加</span> {#tidb-enable-vectorized-expression-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ベクトル化実行を有効にするかどうかを制御するために使用されます。

### tidb_enable_window_function {#tidb-enable-window-function}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [ウィンドウ関数](/functions-and-operators/window-functions.md)のサポートを有効にするかどうかを制御するために使用されます。 ウィンドウ関数は予約語を使用する可能性があることに注意してください。これにより、TiDB のアップグレード後に、通常実行できる SQL ステートメントが解析に失敗する可能性があります。この場合、 `tidb_enable_window_function` ～ `OFF`に設定できます。

### <code>tidb_enable_row_level_checksum</code> <span class="version-mark">v7.1.0で追加</span> {#code-tidb-enable-row-level-checksum-code-span-class-version-mark-new-in-v7-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は[TiCDCによる単一行データのデータ整合性検証](/ticdc/ticdc-integrity-check.md)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は[TiCDCによる単一行データのデータ整合性検証](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

-   [`TIDB_ROW_CHECKSUM()`](/functions-and-operators/tidb-functions.md#tidb_row_checksum)関数を使用すると、行のチェックサム値を取得できます。

### tidb_enforce_mpp <span class="version-mark">v5.1の新機能</span> {#tidb-enforce-mpp-span-class-version-mark-new-in-v5-1-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   このデフォルト値を変更するには、 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)設定値を変更してください。

</CustomContent>

-   オプティマイザのコスト見積もりを無視し、クエリ実行にTiFlashのMPPモードを強制的に使用するかどうかを制御します。値オプションは以下のとおりです。
    -   `0`または`OFF`場合、MPPモードは強制的に使用されません（デフォルトでは）。
    -   `1`または`ON`場合、コスト見積もりは無視され、MPP モードが強制的に使用されます。この設定は`tidb_allow_mpp=true`場合にのみ有効になることに注意してください。

MPP は、 TiFlashエンジンによって提供される分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能、高スループットの SQL アルゴリズムを提供します。 MPPモードの選択の詳細については、 [MPPモードを選択するかどうかを制御する](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)。

### tidb_evolve_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-baselines-span-class-version-mark-new-in-v4-0-span}

> **警告：**
>
> この変数で制御される機能は実験的機能です。本番環境での使用は推奨されません。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ベースライン進化機能を有効にするかどうかを制御するために使用されます。詳しい導入方法や使い方については、 [ベースライン進化](/sql-plan-management.md#baseline-evolution)ご覧ください。
-   ベースラインの進化がクラスターに与える影響を軽減するには、以下の設定を使用してください。
    -   各実行プランの最大実行時間を制限するには、値を`tidb_evolve_plan_task_max_time`設定します。デフォルト値は600秒です。
    -   時間範囲を制限するには、 `tidb_evolve_plan_task_start_time`と`tidb_evolve_plan_task_end_time`を設定してください。デフォルト値はそれぞれ`00:00 +0000`と`23:59 +0000`です。

### tidb_evolve_plan_task_end_time <span class="version-mark">v4.0で追加</span> {#tidb-evolve-plan-task-end-time-span-class-version-mark-new-in-v4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、1日におけるベースライン進化の終了時刻を設定するために使用されます。

### tidb_evolve_plan_task_max_time <span class="version-mark">v4.0で追加</span> {#tidb-evolve-plan-task-max-time-span-class-version-mark-new-in-v4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `600`
-   範囲: `[-1, 9223372036854775807]`
-   単位：秒
-   この変数は、ベースライン進化機能における各実行プランの最大実行時間を制限するために使用されます。

### tidb_evolve_plan_task_start_time <span class="version-mark">v4.0で追加</span> {#tidb-evolve-plan-task-start-time-span-class-version-mark-new-in-v4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、1日におけるベースライン変化の開始時刻を設定するために使用されます。

### tidb_executor_concurrency <span class="version-mark">v5.0で追加</span> {#tidb-executor-concurrency-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `5`
-   範囲: `[1, 256]`
-   単位：糸

この変数は、以下のSQL演算子の同時実行数を（単一の値に）設定するために使用されます。

-   `index lookup`
-   `index lookup join`
-   `hash join`
-   `hash aggregation` （ `partial`相と`final`相）
-   `window`
-   `projection`
-   `sort`

`tidb_executor_concurrency`管理を容易にするために、以下の既存のシステム変数を全体として統合します。

-   `tidb_index_lookup_concurrency`
-   `tidb_index_lookup_join_concurrency`
-   `tidb_hash_join_concurrency`
-   `tidb_hashagg_partial_concurrency`
-   `tidb_hashagg_final_concurrency`
-   `tidb_projection_concurrency`
-   `tidb_window_concurrency`

バージョン5.0以降では、上記にリストされているシステム変数を個別に変更することも可能です（ただし、非推奨の警告が表示されます）。変更は対応する単一の演算子にのみ影響します。その後、 `tidb_executor_concurrency`使用して演算子の同時実行数を変更した場合、個別に変更された演算子には影響しません。3 `tidb_executor_concurrency`使用してすべての演算子の同時実行数を変更する場合は、上記にリストされているすべての変数の値を`-1`に設定してください。

以前のバージョンからv5.0にアップグレードしたシステムの場合、上記の変数の値を変更していない場合（つまり、 `tidb_hash_join_concurrency`値が`5`で、残りの値が`4`の場合）、これらの変数によって以前管理されていた演算子の同時実行性は、自動的に`tidb_executor_concurrency`によって管理されます。これらの変数のいずれかを変更した場合は、対応する演算子の同時実行性は、変更後の変数によって引き続き制御されます。

### tidb_expensive_query_time_threshold {#tidb-expensive-query-time-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `60`
-   範囲: `[10, 2147483647]`
-   単位：秒
-   この変数は、高負荷なクエリログを出力するかどうかを決定するしきい値を設定するために使用されます。高負荷なクエリログと低負荷なクエリログの違いは次のとおりです。
    -   スローログは、ステートメントの実行後に出力されます。
    -   コストの高いクエリログには、実行時間がしきい値を超えた実行中のステートメントと、それに関連する情報が出力されます。

### tidb_expensive_txn_time_threshold <span class="version-mark">v7.2.0で追加</span> {#tidb-expensive-txn-time-threshold-span-class-version-mark-new-in-v7-2-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `600`
-   範囲: `[60, 2147483647]`
-   単位：秒
-   この変数は、高負荷トランザクションをログに記録するしきい値を制御します。デフォルト値は600秒です。トランザクションの所要時間がこのしきい値を超え、かつトランザクションがコミットもロールバックもされない場合、そのトランザクションは高負荷トランザクションとみなされ、ログに記録されます。

### tidb_force_priority {#tidb-force-priority}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `NO_PRIORITY`
-   `LOW_PRIORITY` `DELAYED`値`HIGH_PRIORITY` `NO_PRIORITY`
-   この変数は、TiDBサーバー上で実行されるステートメントのデフォルトの優先度を変更するために使用されます。使用例としては、OLAPクエリを実行する特定のユーザーが、OLTPクエリを実行するユーザーよりも低い優先度を受け取るようにすることが挙げられます。
-   デフォルト値の`NO_PRIORITY` 、ステートメントの優先順位が強制的に変更されないことを意味します。

> **注記：**
>
> バージョン6.6.0以降、TiDBは[リソース制御](/tidb-resource-control-ru-groups.md)サポートしています。この機能を使用すると、異なるリソースグループで異なる優先度のSQLステートメントを実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、異なる優先度のSQLステートメントのスケジューリングをより適切に制御できます。リソース制御が有効になっている場合、ステートメントの優先度は適用されなくなります。 を使用して[リソース制御](/tidb-resource-control-ru-groups.md)異なるSQLステートメントのリソース使用量を管理することをお勧めします。

### tidb_gc_concurrency <span class="version-mark">v5.0で追加</span> {#tidb-gc-concurrency-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲： `-1`または`[1, 256]`
-   単位：糸
-   この変数は[ごみ収集（GC）](/garbage-collection-overview.md)プロセスの[ロックを解除する](/garbage-collection-overview.md#resolve-locks)ステップ中の同時スレッドの数を制御します。
-   v8.3.0 以降、この変数は、GC プロセスの[範囲の削除](/garbage-collection-overview.md#delete-ranges)ステップ中の同時スレッドの数も制御します。
-   デフォルトでは、この変数は`-1`設定されており、TiDB がワークロードに基づいて適切なスレッド数を自動的に決定できるようになっています。
-   この変数が`[1, 256]`から始まる数値に設定されている場合：
    -   ロック解決機能は、この変数に設定された値をスレッド数として直接使用します。
    -   Delete Rangeは、この変数に設定された値の4分の1をスレッド数として使用します。

### tidb_gc_enable <span class="version-mark">v5.0で追加</span> {#tidb-gc-enable-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiKVのガベージコレクションを有効にします。ガベージコレクションを無効にすると、行の古いバージョンが削除されなくなるため、システムパフォーマンスが低下します。

### tidb_gc_life_time <span class="version-mark">v5.0で追加</span> {#tidb-gc-life-time-span-class-version-mark-new-in-v5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ：期間
-   デフォルト値: `10m0s`
-   範囲：TiDB Self-Managedおよび[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合は`[10m0s, 8760h0m0s]` 、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は`[10m0s, 168h0m0s]`
-   各GCにおいてデータが保持される時間制限（Go Duration形式）。GCが発生すると、現在の時刻からこの値を引いた時点が安全ポイントとなります。

> **注記：**
>
> -   頻繁に更新が行われるシナリオでは、 `tidb_gc_life_time`値が大きい場合 (日数または月数)、次のような潜在的な問題が発生する可能性があります。
>     -   storage使用量の増加
>     -   大量の履歴データは、特に範囲クエリ（例： `select count(*) from t`の場合、パフォーマンスに一定の影響を与える可能性があります。
> -   GC の実行中に、実行時間が`tidb_gc_life_time`超えるトランザクションがある場合、そのトランザクションの実行を継続するために、 `start_ts`以降のデータが保持されます。たとえば、 `tidb_gc_life_time` 10 分に設定されている場合、実行中のすべてのトランザクションの中で、最も早く開始されたトランザクションが 15 分間実行されている場合、GC は直近 15 分間のデータを保持します。

### tidb_gc_max_wait_time は<span class="version-mark">v6.1.0 で追加されました。</span> {#tidb-gc-max-wait-time-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `86400`
-   範囲: `[600, 31536000]`
-   単位：秒
-   この変数は、アクティブなトランザクションがGCセーフポイントをブロックする最大時間を設定するために使用されます。デフォルトでは、GCの各実行時間において、セーフポイントは進行中のトランザクションの開始時間を超えません。アクティブなトランザクションの実行時間がこの変数の値を超えない場合、実行時間がこの値を超えるまでGCセーフポイントはブロックされます。

### tidb_gc_run_interval <span class="version-mark">v5.0で追加</span> {#tidb-gc-run-interval-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ：期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   GC間隔をGo Durationの形式で指定します。例えば、 `"1h30m"`などです`"15m"`

### tidb_gc_scan_lock_mode <span class="version-mark">v5.0で追加</span> {#tidb-gc-scan-lock-mode-span-class-version-mark-new-in-v5-0-span}

> **警告：**
>
> 現在、Green GCは実験的機能です。本番環境での使用は推奨されません。

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `LEGACY`
-   可能な`LEGACY` : `PHYSICAL`
    -   `LEGACY` ：従来のスキャン方法を使用します。つまり、Green GCを無効にします。
    -   `PHYSICAL` ：物理スキャン方式を使用する、つまりグリーンGCを有効にする。

<CustomContent platform="tidb">

-   この変数は、GC のロック解決ステップにおけるロックのスキャン方法を指定します。変数の値が`LEGACY`に設定されている場合、TiDB はリージョンごとにロックをスキャンします。値`PHYSICAL`を使用すると、各 TiKV ノードがRaftレイヤーをバイパスしてデータを直接スキャンできるようになり、 [冬眠リージョン](/tikv-configuration-file.md#hibernate-regions)領域機能が有効になっている場合に GC がすべてのリージョンを起動することによる影響を効果的に軽減できるため、ロック解決ステップの実行速度が向上します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、GCの「ロックの解決」ステップにおけるロックのスキャン方法を指定します。変数の値が`LEGACY`に設定されている場合、TiDBはリージョンごとにロックをスキャンします。値`PHYSICAL`を使用すると、各TiKVノードがRaftレイヤーをバイパスしてデータを直接スキャンできるようになり、GCがすべてのリージョンを起動する影響を効果的に軽減できるため、「ロックの解決」ステップの実行速度が向上します。

</CustomContent>

### tidb_general_log {#tidb-general-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb-cloud">

-   この変数は、すべてのSQLステートメントをログに記録するかどうかを設定するために使用されます。この機能はデフォルトでは無効になっています。問題箇所を特定する際にすべてのSQLステートメントをトレースする必要がある場合は、この機能を有効にしてください。

</CustomContent>

<CustomContent platform="tidb">

-   この変数は、すべてのSQLステートメントを[ログ](/tidb-configuration-file.md#logfile)に記録するかどうかを設定するために使用されます。この機能はデフォルトでは無効になっています。保守担当者が問題箇所を特定する際にすべてのSQLステートメントを追跡する必要がある場合は、この機能を有効にできます。

-   [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800)設定項目が指定されている場合、一般ログは指定されたファイルに個別に書き込まれます。

-   [`log.format`](/tidb-configuration-file.md#format)設定項目を使用すると、ログメッセージのフォーマット、一般的なログを別のファイルに保存するか、他のログと結合するかを設定できます。

-   [`tidb_redact_log`](#tidb_redact_log)変数を使用すると、一般ログに記録されたSQLステートメントを編集できます。

-   一般ログには、正常に実行されたステートメントのみが記録されます。失敗したステートメントは一般ログには記録されず、代わりにTiDBログに`command dispatched failed`というメッセージとともに記録されます。

-   この機能に関するすべての記録をログで確認するには、TiDB構成項目の[`log.level`](/tidb-configuration-file.md#level) `"info"`または`"debug"`に設定し、 `"GENERAL_LOG"`番目の文字列をクエリする必要があります。以下の情報が記録されます。
    -   `time` ：イベント発生時刻。
    -   `conn` ：現在のセッションのID。
    -   `user` ：現在のセッションユーザー。
    -   `schemaVersion` ：現在のスキーマバージョン。
    -   `txnStartTS` ：現在のトランザクションが開始されたタイムスタンプ。
    -   `forUpdateTS` :悲観的トランザクションモードでは、 `forUpdateTS` SQL ステートメントの現在のタイムスタンプです。悲観的トランザクションで書き込み競合が発生すると、TiDB は現在実行中の SQL ステートメントを再試行し、このタイムスタンプを更新します。再試行回数は[`max-retry-count`](/tidb-configuration-file.md#max-retry-count)で設定できます。楽観的トランザクションモデルでは、 `forUpdateTS` `txnStartTS`と同等です。
    -   `isReadConsistency` ：現在のトランザクション分離レベルが読み取りコミット（RC）であるかどうかを示します。
    -   `current_db` ：現在のデータベースの名前。
    -   `txn_mode` ：トランザクションモード。値の選択肢は`OPTIMISTIC`と`PESSIMISTIC`です。
    -   `sql` ：現在のクエリに対応するSQLステートメント。

</CustomContent>

### tidb_non_prepared_plan_cache_size {#tidb-non-prepared-plan-cache-size}

> **警告：**
>
> バージョン7.1.0以降、この変数は非推奨となりました。代わりに、 [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は[準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)によってキャッシュできる実行プランの最大数を制御します。

### tidb_pre_split_regions <span class="version-mark">v8.4.0で追加</span> {#tidb-pre-split-regions-span-class-version-mark-new-in-v8-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数は、新しく作成されたテーブルのデフォルトの行分割シャード数を設定するために使用されます。この変数にゼロ以外の値を設定すると、TiDB は`CREATE TABLE`ステートメントを実行する際に`PRE_SPLIT_REGIONS`の使用を許可するテーブル (たとえば、 `NONCLUSTERED`テーブル) にこの属性を自動的に適用します。詳細については、 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)を参照してください。この変数は通常、 [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-new-in-v840)と組み合わせて、新しいテーブルのシャーディングと新しいテーブルのリージョンの事前分割に使用されます。

### tidb_generate_binary_plan <span class="version-mark">v6.2.0で追加</span> {#tidb-generate-binary-plan-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スローログとステートメントサマリーにバイナリエンコードされた実行プランを生成するかどうかを制御します。
-   この変数を`ON`に設定すると、TiDBダッシュボードで実行プランを視覚的に表示できます。ただし、TiDBダッシュボードでは、この変数が有効になった後に生成された実行プランのみを視覚的に表示できることに注意してください。
-   [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan)ステートメントを実行すると、バイナリ プランから特定のプランを解析できます。

### tidb_gogc_tuner_max_value <span class="version-mark">v7.5.0で追加</span> {#tidb-gogc-tuner-max-value-span-class-version-mark-new-in-v7-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `500`
-   範囲: `[10, 2147483647]`
-   この変数は、GOGCチューナーが調整できるGOGCの最大値を制御するために使用されます。

### tidb_gogc_tuner_min_value <span class="version-mark">v7.5.0で追加</span> {#tidb-gogc-tuner-min-value-span-class-version-mark-new-in-v7-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `100`
-   範囲: `[10, 2147483647]`
-   この変数は、GOGCチューナーが調整できるGOGCの最小値を制御するために使用されます。

### tidb_gogc_tuner_threshold <span class="version-mark">v6.4.0で追加</span> {#tidb-gogc-tuner-threshold-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `0.6`
-   範囲: `[0, 0.9)`
-   この変数は、GOGC のチューニングにおける最大メモリ使用量を指定します。メモリがこのしきい値を超えると、GOGC Tuner は動作を停止します。

### tidb_guarantee_linearizability <span class="version-mark">v5.0で追加</span> {#tidb-guarantee-linearizability-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、非同期コミットにおけるコミットTSの計算方法を制御します。デフォルト（値`ON` ）では、2フェーズコミットはPDサーバーから新しいTSを要求し、そのTSを使用して最終的なコミットTSを計算します。この場合、すべての同時実行トランザクションに対して線形化可能性が保証されます。
-   この変数を`OFF`に設定すると、PDサーバーから TS を取得するプロセスがスキップされますが、その代償として、因果関係の一貫性のみが保証されますが、線形化可能性は保証されません。詳細については、ブログ投稿[TiDB 5.0 のトランザクションコミットを加速する非同期コミット](https://www.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/)を参照してください。
-   因果関係の一貫性のみを必要とするシナリオでは、この変数を`OFF`に設定することでパフォーマンスを向上させることができます。

### tidb_hash_exchange_with_new_collat​​ion {#tidb-hash-exchange-with-new-collation}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、新しい照合順序が有効になっているクラスタで MPP ハッシュパーティション交換演算子を生成するかどうかを制御します。1 `true`演算子を生成することを意味し、 `false`生成しないことを意味します。
-   この変数はTiDBの内部動作に使用されます。この変数を設定することは**推奨されません**。

### tidb_hash_join_concurrency {#tidb-hash-join-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨となりました。代わりに、[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、 `hash join`アルゴリズムの並行性を設定するために使用されます。
-   値が`-1`の場合は、代わりに値`tidb_executor_concurrency`が使用されます。

### tidb_hash_join_version <span class="version-mark">v8.4.0で追加</span> {#tidb-hash-join-version-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> この変数で制御される機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: 列挙型
-   デフォルト値: `legacy`
-   可能な`optimized` : `legacy`
-   この変数は、TiDBがハッシュ結合の最適化バージョンを使用するかどうかを制御するために使用されます。デフォルト値は`legacy`で、これは最適化バージョンが使用されないことを意味します。3 `optimized`設定すると、TiDBはパフォーマンス向上のために最適化バージョンを使用してハッシュ結合を実行します。

> **注記：**
>
> 現在、最適化されたハッシュ結合は内部結合と外部結合のみをサポートしているため、他の結合については、 `tidb_hash_join_version` `optimized`に設定しても、TiDB は従来のハッシュ結合を使用します。

### tidb_hashagg_final_concurrency {#tidb-hashagg-final-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨となりました。代わりに、[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、第`final`フェーズで並行アルゴリズム`hash aggregation`を実行する際の並行度を設定するために使用されます。
-   集計関数のパラメータが区別できない場合、 `HashAgg`並行して実行され、それぞれ2つのフェーズ（フェーズ`partial`とフェーズ`final` ）で実行されます。
-   値が`-1`の場合は、代わりに値`tidb_executor_concurrency`が使用されます。

### tidb_hashagg_partial_concurrency {#tidb-hashagg-partial-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨となりました。代わりに、[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、第`partial`フェーズで並行アルゴリズム`hash aggregation`を実行する際の並行度を設定するために使用されます。
-   集計関数のパラメータが区別できない場合、 `HashAgg`並行して実行され、それぞれ2つのフェーズ（フェーズ`partial`とフェーズ`final` ）で実行されます。
-   値が`-1`の場合は、代わりに値`tidb_executor_concurrency`が使用されます。

### tidb_historical_stats_duration <span class="version-mark">v6.6.0で追加</span> {#tidb-historical-stats-duration-span-class-version-mark-new-in-v6-6-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ：期間
-   デフォルト値： `168h` （7日間）
-   この変数は、履歴統計がstorageに保持される期間を制御します。

### tidb_idle_transaction_timeout は<span class="version-mark">v7.6.0 で追加されました。</span> {#tidb-idle-transaction-timeout-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 31536000]`
-   単位：秒
-   この変数は、ユーザーセッションにおけるトランザクションのアイドルタイムアウトを制御します。ユーザーセッションがトランザクション状態にあり、この変数の値を超える時間アイドル状態が続くと、TiDB はセッションを終了します。アイドル状態のユーザーセッションとは、アクティブなリクエストがなく、新しいリクエストを待機している状態を指します。
-   デフォルト値の`0`は無制限を意味します。

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">v6.0.0で追加</span> {#tidb-ignore-prepared-cache-close-stmt-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、プリペアドステートメントキャッシュを閉じるコマンドを無視するかどうかを設定するために使用されます。
-   この変数が`ON`に設定されている場合、バイナリ プロトコルの`COM_STMT_CLOSE`コマンドとテキスト プロトコルの[`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md)ステートメントは無視されます。詳細については、 [`COM_STMT_CLOSE`コマンドと`DEALLOCATE PREPARE`ステートメントは無視してください。](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)参照してください。

### tidb_ignore_inlist_plan_digest <span class="version-mark">v7.6.0 の新機能</span> {#tidb-ignore-inlist-plan-digest-span-class-version-mark-new-in-v7-6-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB がプランダイジェストを生成する際に、異なるクエリ間で`IN`リスト内の要素の差異を無視するかどうかを制御します。

    -   デフォルト値が`OFF`場合、TiDBはプランダイジェストを生成する際に、 `IN`番目のリスト内の要素の差異（要素数の違いを含む）を無視しません。5 `IN`のリスト内の要素の差異により、異なるプランダイジェストが生成されます。
    -   この値を`ON`に設定すると、TiDB は`IN`リスト内の要素の差異 (要素数の違いを含む) を無視し、 `...`を使用して`IN`リスト内の要素を Plan Digests 内で置き換えます。この場合、TiDB は同じタイプの`IN`のクエリに対して同じ Plan Digests を生成します。

### tidb_index_join_batch_size {#tidb-index-join-batch-size}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `25000`
-   範囲: `[1, 2147483647]`
-   単位：行
-   この変数は、 `index lookup join`操作のバッチサイズを設定するために使用されます。
-   OLAPシナリオではより大きな値を使用し、OLTPシナリオではより小さな値を使用してください。

### tidb_index_join_double_read_penalty_cost_rate<span class="version-mark">は v6.6.0 で追加されました。</span> {#tidb-index-join-double-read-penalty-cost-rate-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、インデックス結合の選択にペナルティコストを適用するかどうかを決定します。ペナルティコストを適用することで、オプティマイザがインデックス結合を選択する可能性が低くなり、ハッシュ結合やTIFlash結合などの代替結合方法を選択する可能性が高くなります。
-   インデックス結合を選択すると、多数のテーブル検索要求が発生し、リソースを過剰に消費します。この変数を使用することで、オプティマイザがインデックス結合を選択する可能性を低減できます。
-   この変数は、 [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620)変数が`2`に設定されている場合にのみ有効になります。

### tidb_index_lookup_concurrency {#tidb-index-lookup-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨となりました。代わりに、[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、 `index lookup`操作の同時実行数を設定するために使用されます。
-   OLAPシナリオではより大きな値を使用し、OLTPシナリオではより小さな値を使用してください。
-   値が`-1`の場合は、代わりに値`tidb_executor_concurrency`が使用されます。

### tidb_index_lookup_join_concurrency {#tidb-index-lookup-join-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨となりました。代わりに、[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、 `index lookup join`アルゴリズムの並行性を設定するために使用されます。
-   値が`-1`の場合は、代わりに値`tidb_executor_concurrency`が使用されます。

### tidb_index_lookup_pushdown_policy <span class="version-mark">v8.5.5で追加</span> {#tidb-index-lookup-pushdown-policy-span-class-version-mark-new-in-v8-5-5-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: 列挙型
-   デフォルト値: `hint-only`
-   `force` `affinity-force` ： `hint-only`
-   この変数は、TiDBが`IndexLookUp`演算子をTiKVにプッシュダウンするかどうか、またプッシュダウンするタイミングを制御します。値のオプションは以下のとおりです。
    -   `hint-only` (デフォルト): TiDB は、SQL ステートメントで[`INDEX_LOOKUP_PUSHDOWN`](/optimizer-hints.md#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)ヒントが明示的に指定されている場合にのみ、 `IndexLookUp`演算子を TiKV にプッシュダウンします。
    -   `affinity-force` : TiDB は、 `AFFINITY`オプションで構成されたテーブルに対してのみプッシュダウンを自動的に有効にします。
    -   `force` : TiDB はすべてのテーブルに対して`IndexLookUp`プッシュダウンを有効にします。

### tidb_index_merge_intersection_concurrency <span class="version-mark">v6.5.0で追加</span> {#tidb-index-merge-intersection-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   この変数は、インデックスマージが実行する交差操作の最大同時実行数を設定します。これは、TiDB が動的プルーニングモードでパーティションテーブルにアクセスする場合にのみ有効です。実際の同時実行数は、 `tidb_index_merge_intersection_concurrency`とパーティションテーブルのパーティション数のうち小さい方の値になります。
-   デフォルト値`-1` 、値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_size {#tidb-index-lookup-size}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `20000`
-   範囲: `[1, 2147483647]`
-   単位：行
-   この変数は、 `index lookup`操作のバッチサイズを設定するために使用されます。
-   OLAPシナリオではより大きな値を使用し、OLTPシナリオではより小さな値を使用してください。

### tidb_index_serial_scan_concurrency {#tidb-index-serial-scan-concurrency}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、 `serial scan`操作の同時実行数を設定するために使用されます。
-   OLAPシナリオではより大きな値を使用し、OLTPシナリオではより小さな値を使用してください。

### tidb_init_chunk_size {#tidb-init-chunk-size}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `32`
-   範囲: `[1, 32]`
-   単位：行
-   この変数は、実行プロセス中に最初のチャンクの行数を設定するために使用されます。チャンクの行数は、単一のクエリに必要なメモリ量に直接影響します。クエリ内のすべての列の合計幅とチャンクの行数を考慮することで、単一のチャンクに必要なメモリを概算できます。これにエグゼキュータの同時実行性を組み合わせることで、単一のクエリに必要な合計メモリを概算できます。単一のチャンクの合計メモリは16 MiBを超えないことを推奨します。

### tidb_instance_plan_cache_reserved_percentage <span class="version-mark">v8.4.0で追加</span> {#tidb-instance-plan-cache-reserved-percentage-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> 現在、インスタンスプランキャッシュは実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: フロート
-   デフォルト値: `0.1`
-   範囲: `[0, 1]`
-   この変数は、メモリ削除後に[インスタンスプランキャッシュ](#tidb_enable_instance_plan_cache-new-in-v840)プラン キャッシュ用に予約されるアイドルメモリの割合を制御します。インスタンス プラン キャッシュで使用されるメモリが[`tidb_instance_plan_cache_max_size`](#tidb_instance_plan_cache_max_size-new-in-v840)で設定された制限に達すると、TiDB はアイドル メモリの割合が[`tidb_instance_plan_cache_reserved_percentage`](#tidb_instance_plan_cache_reserved_percentage-new-in-v840)で設定された値を超えるまで、Least Recently Used (LRU) アルゴリズムを使用してメモリからメモリプランを削除し始めます。

### tidb_instance_plan_cache_max_size は<span class="version-mark">v8.4.0 で追加されました。</span> {#tidb-instance-plan-cache-max-size-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> 現在、インスタンスプランキャッシュは実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値： `125829120` （120MiB）
-   単位：バイト
-   この変数は[インスタンスプランキャッシュ](#tidb_enable_instance_plan_cache-new-in-v840)の最大メモリ使用量を設定します。

### tidb_isolation_read_engines <span class="version-mark">v4.0の新機能</span> {#tidb-isolation-read-engines-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `tikv,tiflash,tidb`
-   この変数は、TiDBがデータを読み取る際に使用できるstorageエンジンのリストを設定するために使用されます。

### tidb_last_ddl_info <span class="version-mark">v6.0.0で追加</span> {#tidb-last-ddl-info-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   型: 文字列
-   これは読み取り専用変数です。TiDB内部で、現在のセッションにおける最後のDDL操作の情報を取得するために使用されます。
    -   「query」：最後のDDLクエリ文字列。
    -   「seq_num」：各DDL操作のシーケンス番号。DDL操作の順序を識別するために使用されます。

### tidb_last_query_info <span class="version-mark">v4.0.14で追加</span> {#tidb-last-query-info-span-class-version-mark-new-in-v4-0-14-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   これは読み取り専用変数です。TiDB内部で、最後のDMLステートメントのトランザクション情報を照会するために使用されます。情報には以下が含まれます。
    -   `txn_scope` : トランザクションの範囲。2 または`global` `local`なります。
    -   `start_ts` ：トランザクションの開始タイムスタンプ。
    -   `for_update_ts` ：直前に実行されたDMLステートメントの`for_update_ts`の値。これはTiDBの内部用語で、テストに使用されます。通常、この情報は無視して構いません。
    -   `error` ：エラーメッセージ（存在する場合）。
    -   `ru_consumption` ：ステートメントの実行に消費された[RU](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) 。

### tidb_last_txn_info <span class="version-mark">v4.0.9で追加</span> {#tidb-last-txn-info-span-class-version-mark-new-in-v4-0-9-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   この変数は、現在のセッション内の最後のトランザクション情報を取得するために使用されます。これは読み取り専用変数です。トランザクション情報には以下が含まれます。
    -   トランザクションの範囲。
    -   開始およびコミットTS。
    -   トランザクションのコミットモードは、2フェーズコミット、1フェーズコミット、または非同期コミットのいずれかになります。
    -   非同期コミットまたは1フェーズコミットから2フェーズコミットへのトランザクションフォールバックに関する情報。
    -   発生したエラー。

### tidb_last_plan_replayer_token <span class="version-mark">v6.3.0で追加</span> {#tidb-last-plan-replayer-token-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   この変数は読み取り専用であり、現在のセッションにおける最後の`PLAN REPLAYER DUMP`の実行結果を取得するために使用されます。

### tidb_load_based_replica_read_threshold <span class="version-mark">v7.0.0 で追加</span> {#tidb-load-based-replica-read-threshold-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   型: 文字列
-   この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定するために使用されます。リーダー ノードの推定キュー時間がしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。形式は、 `"100ms"`や`"1s"`などの期間です。詳細については、 [ホットスポットの問題をトラブルシューティングする](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   型: 文字列
-   この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定するために使用されます。リーダー ノードの推定キュー時間がしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。形式は、 `"100ms"`や`"1s"`などの期間です。詳細については、 [ホットスポットの問題をトラブルシューティングする](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#scatter-read-hotspots)参照してください。

</CustomContent>

### <code>tidb_load_binding_timeout</code> <span class="version-mark">v8.0.0で追加</span> {#code-tidb-load-binding-timeout-code-span-class-version-mark-new-in-v8-0-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `200`
-   範囲: `(0, 2147483647]`
-   単位：ミリ秒
-   この変数は、バインディングの読み込みタイムアウトを制御するために使用されます。バインディングの読み込み実行時間がこの値を超えると、読み込みが停止します。

### <code>tidb_lock_unchanged_keys</code> <span class="version-mark">v7.1.1 および v7.3.0 で追加されました。</span> {#code-tidb-lock-unchanged-keys-code-span-class-version-mark-new-in-v7-1-1-and-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、以下のシナリオで特定のキーをロックするかどうかを制御するために使用されます。値が`ON`に設定されている場合、これらのキーはロックされます。値が`OFF`に設定されている場合、これらのキーはロックされません。
    -   `INSERT IGNORE`と`REPLACE`ステートメントに重複するキーがあります。v6.1.6 より前のバージョンでは、これらのキーはロックされていませんでした。この問題は[#42121](https://github.com/pingcap/tidb/issues/42121)で修正されました。
    -   キーの値が変更されない場合、 `UPDATE`ステートメントで一意のキーが保持されます。v6.5.2 より前は、これらのキーはロックされていませんでした。この問題は[#36438](https://github.com/pingcap/tidb/issues/36438)で修正されました。
-   トランザクションの一貫性と合理性を維持するため、この値を変更することは推奨されません。TiDB のアップグレードによって、これら 2 つの修正が原因で深刻なパフォーマンスの問題が発生する場合、かつロックなしの動作が許容範囲内である場合 (前述の問題を参照)、この変数を`OFF`に設定できます。

### tidb_log_file_max_days は<span class="version-mark">v5.3.0 で追加されました。</span> {#tidb-log-file-max-days-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`

<CustomContent platform="tidb">

-   この変数は、現在の TiDB インスタンスでログを保持する最大日数を設定するために使用されます。デフォルト値は、設定ファイル内の[`max-days`](/tidb-configuration-file.md#max-days)設定の値です。変数の値を変更しても、現在の TiDB インスタンスにのみ影響します。TiDB を再起動すると、変数の値はリセットされ、設定値には影響しません。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、現在のTiDBインスタンス上でログを保持する最大日数を設定するために使用されます。

</CustomContent>

### tidb_low_resolution_tso {#tidb-low-resolution-tso}

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、低精度TSO機能を有効にするかどうかを設定するために使用されます。この機能が有効になると、TiDBはキャッシュされたタイムスタンプを使用してデータを読み取ります。キャッシュされたタイムスタンプは、デフォルトでは2秒ごとに更新されます。v8.0.0以降では、 [`tidb_low_resolution_tso_update_interval`](#tidb_low_resolution_tso_update_interval-new-in-v800)を使用して更新間隔を設定できます。
-   主な適用シナリオは、古いデータの読み取りが許容される場合に、小規模な読み取り専用トランザクションのTSO取得にかかるオーバーヘッドを削減することです。
-   バージョン8.3.0以降、この変数はグローバルスコープをサポートします。

### <code>tidb_low_resolution_tso_update_interval</code> <span class="version-mark">v8.0.0で追加</span> {#code-tidb-low-resolution-tso-update-interval-code-span-class-version-mark-new-in-v8-0-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `2000`
-   範囲: `[10, 60000]`
-   単位：ミリ秒
-   この変数は、低精度TSO機能で使用されるキャッシュされたタイムスタンプの更新間隔をミリ秒単位で設定するために使用されます。
-   この変数は、 [`tidb_low_resolution_tso`](#tidb_low_resolution_tso)が有効になっている場合にのみ利用可能です。

### tidb_max_auto_analyze_time は<span class="version-mark">v6.1.0 で追加されました。</span> {#tidb-max-auto-analyze-time-span-class-version-mark-new-in-v6-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値： `43200` （12時間）
-   範囲: `[0, 2147483647]`
-   単位：秒
-   この変数は、自動タスク`ANALYZE`の最大実行時間を指定するために使用されます。自動タスク`ANALYZE`の実行時間が指定された時間を超えると、タスクは終了します。この変数の値が`0`の場合、自動タスク`ANALYZE`の最大実行時間に制限はありません。

### tidb_max_bytes_before_tiflash_external_group_by <span class="version-mark">v7.0.0で追加</span> {#tidb-max-bytes-before-tiflash-external-group-by-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashのハッシュ集計演算子の最大メモリ使用量をバイト`GROUP BY`で指定するために使用します。メモリ使用量が指定された値を超えると、 TiFlash はハッシュ集計演算子をトリガーしてディスクに書き出します。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合のみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量は無制限、つまりTiFlashハッシュ集計演算子は書き出しをトリガーしません。詳細は、 [TiFlashディスクへのスピル](/tiflash/tiflash-spill-disk.md)参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、集計処理は通常、複数のTiFlashノードに分散して実行されます。この変数は、単一のTiFlashノードにおける集計演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は、自身の構成項目[`max_bytes_before_external_group_by`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて、集約演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、集計処理は通常、複数のTiFlashノードに分散して実行されます。この変数は、単一のTiFlashノードにおける集計演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は自身の構成項目`max_bytes_before_external_group_by`値に基づいて集約演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_join <span class="version-mark">v7.0.0で追加</span> {#tidb-max-bytes-before-tiflash-external-join-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashのハッシュ結合演算子の最大メモリ使用量を`JOIN`単位で指定するために使用されます。メモリ使用量が指定された値を超えると、 TiFlash はハッシュ結合演算子をトリガーしてディスクに書き出します。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合のみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量は無制限、つまりTiFlashハッシュ結合演算子は書き出しをトリガーしません。詳細は、 [TiFlashディスクへのスピル](/tiflash/tiflash-spill-disk.md)を参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、結合処理は通常、複数のTiFlashノード上で分散して実行されます。この変数は、単一のTiFlashノード上での結合演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は、自身の構成項目[`max_bytes_before_external_join`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて、結合演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、結合処理は通常、複数のTiFlashノード上で分散して実行されます。この変数は、単一のTiFlashノード上での結合演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は自身の構成項目`max_bytes_before_external_join`値に基づいて結合演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_sort <span class="version-mark">v7.0.0で追加</span> {#tidb-max-bytes-before-tiflash-external-sort-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashの TopN および Sort 演算子の最大メモリ使用量をバイト単位で指定するために使用されます。メモリ使用量が指定された値を超えると、 TiFlash はTopN および Sort 演算子をトリガーしてディスクに書き出します。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合のみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量は無制限、つまりTiFlash のTopN および Sort 演算子は書き出しをトリガーしません。詳細については、 [TiFlashディスクへのスピル](/tiflash/tiflash-spill-disk.md)参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、TopNとSortは通常、複数のTiFlashノードで分散実行されます。この変数は、単一のTiFlashノードにおけるTopNおよびSort演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は、独自の構成項目[`max_bytes_before_external_sort`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて、TopN および Sort オペレーターの最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、TopNとSortは通常、複数のTiFlashノードで分散実行されます。この変数は、単一のTiFlashノードにおけるTopNおよびSort演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は、自身の構成項目`max_bytes_before_external_sort`の値に基づいて TopN および Sort 演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_chunk_size {#tidb-max-chunk-size}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1024`
-   範囲: `[32, 2147483647]`
-   単位：行
-   この変数は、実行プロセス中にチャンク内の最大行数を設定するために使用されます。大きすぎる値を設定すると、キャッシュの局所性の問題が発生する可能性があります。この変数の推奨値は 65536 以下です。チャンクの行数は、単一のクエリに必要なメモリ量に直接影響します。クエリ内のすべての列の合計幅とチャンクの行数を考慮することで、単一のチャンクに必要なメモリを概算できます。これをエグゼキュータの同時実行性と組み合わせることで、単一のクエリに必要な合計メモリを概算できます。単一のチャンクの合計メモリは16 MiB を超えないことを推奨します。クエリに大量のデータが含まれており、単一のチャンクではすべてのデータを処理するのに不十分な場合、TiDB はそれを複数回処理し、チャンクサイズが`tidb_max_chunk_size`に達するまで、各処理反復でチャンクサイズを 2 [`tidb_init_chunk_size`](#tidb_init_chunk_size)にします。

### tidb_max_delta_schema_count は<span class="version-mark">v2.1.18 および v3.0.5 で追加されました。</span> {#tidb-max-delta-schema-count-span-class-version-mark-new-in-v2-1-18-and-v3-0-5-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1024`
-   範囲: `[100, 16384]`
-   この変数は、キャッシュ可能なスキーマバージョンの最大数（対応するバージョンに合わせて変更されたテーブルID）を設定するために使用されます。値の範囲は100～16384です。

### tidb_max_paging_size <span class="version-mark">v6.3.0で追加</span> {#tidb-max-paging-size-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `50000`
-   範囲: `[1, 9223372036854775807]`
-   単位：行
-   この変数は、コプロセッサのページング要求処理中に処理する最大行数を設定するために使用されます。値を小さく設定しすぎると、TiDBとTiKV間のRPC回数が増加します。一方、値を大きく設定しすぎると、データのロードやフルテーブルスキャンなど、場合によってはメモリ使用量が過剰になります。この変数のデフォルト値は、OLAPシナリオよりもOLTPシナリオで優れたパフォーマンスを発揮します。アプリケーションがstorageエンジンとしてTiKVのみを使用している場合は、OLAPワークロードクエリを実行する際にこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

### tidb_max_tiflash_threads は<span class="version-mark">v6.1.0 で追加されました。</span> {#tidb-max-tiflash-threads-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位：糸
-   この変数は、 TiFlashがリクエストを実行する際の最大同時実行数を設定するために使用されます。デフォルト値は`-1`で、このシステム変数が無効であり、最大同時実行数はTiFlash構成`profiles.default.max_threads`の設定に依存することを示しています。値が`0`の場合、最大スレッド数はTiFlashによって自動的に構成されます。

### tidb_mem_oom_action <span class="version-mark">v6.1.0で追加</span> {#tidb-mem-oom-action-span-class-version-mark-new-in-v6-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `CANCEL`
-   可能な`LOG` : `CANCEL`

<CustomContent platform="tidb">

-   単一の SQL ステートメントが`tidb_mem_quota_query`で指定されたメモリクォータを超え、ディスクに書き出すことができない場合に TiDB が実行する操作を指定します。詳細は[TiDBメモリ制御](/configure-memory-usage.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   単一の SQL ステートメントが[`tidb_mem_quota_query`](#tidb_mem_quota_query)で指定されたメモリクォータを超え、ディスクに書き出すことができない場合に、TiDB が実行する操作を指定します。

</CustomContent>

-   デフォルト値は`CANCEL`ですが、TiDB v4.0.2 以前のバージョンではデフォルト値は`LOG`です。
-   この設定は以前はオプション`tidb.toml` （ `oom-action` ）でしたが、TiDB v6.1.0以降はシステム変数に変更されました。

### tidb_mem_quota_analyze <span class="version-mark">v6.1.0で追加</span> {#tidb-mem-quota-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> 現在、メモリ割り当て`ANALYZE`実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   単位：バイト
-   この変数は、TiDB の統計情報更新における最大メモリ使用量を制御します。このようなメモリ使用量は、手動で[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行した場合と、TiDB がバックグラウンドでタスクを自動的に分析した場合に発生します。合計メモリ使用量がこのしきい値を超えると、ユーザーが実行した`ANALYZE`終了し、より低いサンプリング レートを試すか、後で再試行するように促すエラー メッセージが表示されます。TiDB のバックグラウンドで自動タスクがメモリしきい値を超えたために終了し、使用されているサンプリング レートがデフォルト値よりも高い場合、TiDB はデフォルトのサンプリング レートを使用して更新を再試行します。この変数の値が負またはゼロの場合、TiDB は手動および自動更新タスクの両方のメモリ使用量を制限しません。

> **注記：**
>
> TiDBクラスタでは、TiDB起動設定ファイルで`run-auto-analyze`有効になっている場合にのみ、 `auto_analyze`トリガーされます。

### tidb_mem_quota_apply_cache <span class="version-mark">v5.0で追加</span> {#tidb-mem-quota-apply-cache-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値： `33554432` （32 MiB）
-   範囲: `[0, 9223372036854775807]`
-   単位：バイト
-   この変数は、 `Apply`演算子内のローカルキャッシュのメモリ使用量しきい値を設定するために使用されます。
-   `Apply`演算子内のローカルキャッシュは、 `Apply`演算子の計算を高速化するために使用されます。変数を`0`に設定すると、 `Apply`キャッシュ機能を無効にできます。

### tidb_mem_quota_binding_cache <span class="version-mark">v6.0.0で追加</span> {#tidb-mem-quota-binding-cache-span-class-version-mark-new-in-v6-0-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `67108864`
-   範囲: `[0, 2147483647]`
-   単位：バイト
-   この変数は、バインディングのキャッシュに使用されるメモリのしきい値を設定するために使用されます。
-   システムが過剰なバインディングを作成またはキャプチャし、メモリ領域を過剰に使用すると、TiDB はログに警告を返します。この場合、キャッシュは利用可能なすべてのバインディングを保持できず、どのバインディングを保存するかを判断できません。そのため、一部のクエリでバインディングが見つからない場合があります。この問題を解決するには、この変数の値を増やして、バインディングのキャッシュに使用されるメモリを増やします。このパラメータを変更した後は、コマンド`admin reload bindings`を実行してバインディングを再読み込みし、変更を検証する必要があります。

### tidb_mem_quota_query {#tidb-mem-quota-query}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値： `1073741824` （1 GiB）
-   範囲: `[-1, 9223372036854775807]`
-   単位：バイト

<CustomContent platform="tidb">

-   TiDB v6.1.0より前のバージョンでは、これはセッションスコープ変数であり、初期値として`tidb.toml`から`mem-quota-query`の値を使用します。v6.1.0以降では、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0 より前のバージョンでは、この変数は**クエリ**のメモリ割り当てのしきい値を設定するために使用されます。実行中にクエリのメモリ割り当てがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0 以降のバージョンでは、この変数は**セッション**のメモリクォータのしきい値を設定するために使用されます。実行中にセッションのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。TiDB v6.5.0 以降では、セッションのメモリ使用量には、セッション内のトランザクションによって消費されたメモリが含まれることに注意してください。TiDB v6.5.0 以降のバージョンにおけるトランザクションのメモリ使用量の制御動作については、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)参照してください。
-   変数の値を`0`または`-1`に設定すると、メモリのしきい値は正の無限大になります。128より小さい値を設定すると、デフォルト値として`128`が使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB v6.1.0より前のバージョンでは、これはセッションスコープ変数です。v6.1.0以降では、 `tidb_mem_quota_query` `SESSION | GLOBAL`スコープ変数になります。
-   TiDB v6.5.0 より前のバージョンでは、この変数は**クエリ**のメモリ割り当てのしきい値を設定するために使用されます。実行中にクエリのメモリ割り当てがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0 以降のバージョンでは、この変数は**セッション**のメモリ割り当てのしきい値を設定するために使用されます。実行中にセッションのメモリ割り当てがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。TiDB v6.5.0 以降では、セッションのメモリ使用量には、セッション内のトランザクションによって消費されたメモリが含まれることに注意してください。
-   変数の値を`0`または`-1`に設定すると、メモリのしきい値は正の無限大になります。128より小さい値を設定すると、デフォルト値として`128`が使用されます。

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio {#tidb-memory-debug-mode-alarm-ratio}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   この変数は、TiDBのメモリデバッグモードで許容されるメモリ統計エラー値を表します。
-   この変数はTiDBの内部テストに使用されます。この変数を設定することは**推奨されません**。

### tidb_memory_debug_mode_min_heap_inuse {#tidb-memory-debug-mode-min-heap-inuse}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   この変数はTiDBの内部テストに使用されます。この変数を設定することは**推奨されません**。この変数を有効にすると、TiDBのパフォーマンスに影響が出ます。
-   このパラメータを設定すると、TiDB はメモリデバッグモードに入り、メモリ追跡の精度を分析します。TiDB は、後続の SQL ステートメントの実行中に頻繁に GC をトリガーし、実際のメモリ使用量とメモリ統計を比較します。現在のメモリ使用量が`tidb_memory_debug_mode_min_heap_inuse`より大きく、メモリ統計の誤差が`tidb_memory_debug_mode_alarm_ratio`超える場合、TiDB は関連するメモリ情報をログとファイルに出力します。

### tidb_memory_usage_alarm_ratio {#tidb-memory-usage-alarm-ratio}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0.0, 1.0]`

<CustomContent platform="tidb">

-   この変数は、tidb-server のメモリアラームをトリガーするメモリ使用率を設定します。デフォルトでは、TiDB のメモリ使用率が総メモリの 70% を超え、かついずれかの[警報状態](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage)が満たされた場合、TiDB はアラームログを出力。
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能が無効になります。
-   この変数が`0`より大きく`1`より小さい値に設定されている場合、メモリしきい値アラーム機能が有効になっていることを意味します。

    -   システム変数[`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640)の値が`0`の場合、メモリアラームのしきい値は`tidb_memory-usage-alarm-ratio * system memory size`になります。
    -   システム変数`tidb_server_memory_limit`の値が0より大きい値に設定されている場合、メモリアラームのしきい値は`tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は[tidb-serverメモリアラーム](https://docs.pingcap.com/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage)をトリガーするメモリ使用率を設定します。
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能が無効になります。
-   この変数が`0`より大きく`1`より小さい値に設定されている場合、メモリしきい値アラーム機能が有効になっていることを意味します。

</CustomContent>

### tidb_memory_usage_alarm_keep_record_num <span class="version-mark">v6.4.0で追加</span> {#tidb-memory-usage-alarm-keep-record-num-span-class-version-mark-new-in-v6-4-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `5`
-   範囲: `[1, 10000]`
-   tidb-serverのメモリ使用量がメモリアラームのしきい値を超えてアラームが発生した場合、TiDBはデフォルトでは直近5件のアラーム発生時に生成されたステータスファイルのみを保持します。この件数は、この変数で調整できます。

### tidb_merge_join_concurrency {#tidb-merge-join-concurrency}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   範囲: `[1, 256]`
-   デフォルト値: `1`
-   この変数は、クエリ実行時の`MergeJoin`演算子の同時実行数を設定します。
-   この変数を設定することは**推奨されません**。この変数の値を変更すると、データの正確性に問題が生じる可能性があります。

### tidb_merge_partition_stats_concurrency {#tidb-merge-partition-stats-concurrency}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `1`
-   この変数は、TiDB がパーティション テーブルを分析する際に、パーティションテーブルパーティションテーブルに対する統計情報をマージする同時実行回数を指定します。

### tidb_enable_async_merge_global_stats は<span class="version-mark">v7.5.0 で追加されました。</span> {#tidb-enable-async-merge-global-stats-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`を v7.5.0 より前のバージョンから v7.5.0 以降のバージョンにアップグレードする場合、デフォルト値は`OFF`になります。
-   この変数は、TiDBがグローバル統計情報を非同期的にマージしてメモリ不足の問題を回避するために使用されます。

### tidb_metric_query_range_duration <span class="version-mark">v4.0で追加</span> {#tidb-metric-query-range-duration-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位：秒
-   この変数は、 `METRICS_SCHEMA`をクエリしたときに生成される Prometheus ステートメントの範囲期間を設定するために使用されます。

### tidb_metric_query_step <span class="version-mark">v4.0で追加</span> {#tidb-metric-query-step-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位：秒
-   この変数は、クエリ`METRICS_SCHEMA`を実行する際に生成されるPrometheusステートメントのステップを設定するために使用されます。

### tidb_min_paging_size <span class="version-mark">v6.2.0で追加</span> {#tidb-min-paging-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `128`
-   範囲: `[1, 9223372036854775807]`
-   単位：行
-   この変数は、コプロセッサのページング要求処理中に最小行数を設定するために使用されます。値を小さく設定しすぎると、TiDBとTiKV間のRPC要求数が増加します。一方、値を大きく設定しすぎると、Limitを使用したIndexLookupクエリの実行時にパフォーマンスが低下する可能性があります。この変数のデフォルト値は、OLAPシナリオよりもOLTPシナリオで優れたパフォーマンスを発揮します。アプリケーションがstorageエンジンとしてTiKVのみを使用している場合は、OLAPワークロードクエリを実行する際にこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

![Paging size impact on TPCH](/media/paging-size-impact-on-tpch.png)

この図に示すように、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)有効になっている場合、TPCH のパフォーマンスは`tidb_min_paging_size`と[`tidb_max_paging_size`](#tidb_max_paging_size-new-in-v630)の設定によって影響を受けます。縦軸は実行時間で、値が小さいほど良いことを示します。

### tidb_mpp_store_fail_ttl {#tidb-mpp-store-fail-ttl}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ：期間
-   デフォルト値: `0s`以前のバージョンでは、デフォルト値は`60s`です。
-   新しく起動したTiFlashノードはサービスを提供しません。クエリの失敗を防ぐため、TiDBはtidb-serverが新しく起動したTiFlashノードにクエリを送信することを制限します。この変数は、新しく起動したTiFlashノードにリクエストが送信されない時間範囲を示します。

### tidb_multi_statement_mode <span class="version-mark">v4.0.11で追加</span> {#tidb-multi-statement-mode-span-class-version-mark-new-in-v4-0-11-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `OFF`
-   `ON` `WARN`値： `OFF`
-   この変数は、同じ`COM_QUERY`呼び出しで複数のクエリを実行することを許可するかどうかを制御します。
-   SQLインジェクション攻撃の影響を軽減するため、TiDBはデフォルトで、同じ`COM_QUERY`の呼び出しで複数のクエリが実行されないようにするようになりました。この変数は、以前のバージョンのTiDBからのアップグレードパスの一部として使用されることを想定しています。以下の動作が適用されます。

| クライアント設定        | `tidb_multi_statement_mode`値 | 複数の発言は許可されていますか？ |
| --------------- | ---------------------------- | ---------------- |
| 複数のステートメント = ON | オフ                           | はい               |
| 複数のステートメント = ON | の上                           | はい               |
| 複数のステートメント = ON | 警告                           | はい               |
| 複数のステートメント = オフ | オフ                           | いいえ              |
| 複数のステートメント = オフ | の上                           | はい               |
| 複数のステートメント = オフ | 警告                           | はい（+警告が返されました）   |

> **注記：**
>
> デフォルト値の`OFF`のみが安全とみなされます。アプリケーションがTiDBの以前のバージョン向けに設計されている場合は、設定`tidb_multi_statement_mode=ON`必要になる場合があります。アプリケーションで複数のステートメントのサポートが必要な場合は、オプション`tidb_multi_statement_mode`ではなく、クライアントライブラリが提供する設定を使用することをお勧めします。例：
>
> -   [go-sql-driver](https://github.com/go-sql-driver/mysql#multistatements) ( `multiStatements` )
> -   [コネクタ/J](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) ( `allowMultiQueries` )
> -   PHP [mysqli](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) ( `mysqli_multi_query` )

### tidb_nontransactional_ignore_error <span class="version-mark">v6.1.0で追加</span> {#tidb-nontransactional-ignore-error-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非トランザクションDMLステートメントでエラーが発生した場合に、直ちにエラーを返すかどうかを指定します。
-   値が`OFF`に設定されている場合、非トランザクション DML ステートメントは最初のエラーが発生した時点で直ちに停止し、エラーを返します。以降のすべてのバッチはキャンセルされます。
-   値が`ON`に設定されている場合、バッチ処理中にエラーが発生すると、すべてのバッチが実行されるまで、後続のバッチ処理が継続して実行されます。実行プロセス中に発生したすべてのエラーは、結果としてまとめて返されます。

### tidb_opt_agg_push_down {#tidb-opt-agg-push-down}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが集計関数をJoin、Projection、およびUnionAllの前の位置にプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリにおける集計処理が遅い場合は、変数の値をONに設定できます。

### tidb_opt_broadcast_cartesian_join {#tidb-opt-broadcast-cartesian-join}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   ブロードキャストによる直交座標結合を許可するかどうかを示します。
-   `0` 、ブロードキャスト カルテシアン結合が許可されていないことを意味します。2 `1` 、 [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50)に基づいて許可されることを意味します。6 `2` 、テーブル サイズがしきい値を超えても常に許可されることを意味します。
-   この変数はTiDB内部で使用されているため、その値を変更することは推奨さ**れません**。

### tidb_opt_concurrency_factor {#tidb-opt-concurrency-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiDBでGolangゴルーチンを起動する際のCPUコストを示します。この変数は内部的に[コストモデル](/cost-model.md)で使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_copcpu_factor {#tidb-opt-copcpu-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKVコプロセッサーが1行を処理する際のCPUコストを示します。この変数は[コストモデル](/cost-model.md)内部で使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_correlation_exp_factor {#tidb-opt-correlation-exp-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2147483647]`
-   列順序の相関に基づいて行数を推定する方法が利用できない場合、ヒューリスティック推定法が使用されます。この変数は、ヒューリスティック推定法の動作を制御するために使用されます。
    -   値が0の場合、ヒューリスティック法は使用されません。
    -   値が0より大きい場合：
        -   値が大きいほど、ヒューリスティック手法においてインデックススキャンが使用される可能性が高いことを示します。
        -   値が小さいほど、ヒューリスティック手法ではテーブルスキャンが使用される可能性が高いことを示します。

### tidb_opt_correlation_threshold {#tidb-opt-correlation-threshold}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   デフォルト値: `0.9`
-   範囲: `[0, 1]`
-   この変数は、列順序相関を使用して行数を推定するかどうかを決定するしきい値を設定するために使用されます。現在の列と`handle`番目の列の順序相関がしきい値を超えると、この方法が有効になります。

### tidb_opt_cpu_factor {#tidb-opt-cpu-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `3.0`
-   TiDBが1行を処理する際のCPUコストを示します。この変数は内部的に[コストモデル](/cost-model.md)で使用されるため、値を変更することは推奨さ**れません**。

### <code>tidb_opt_derive_topn</code> <span class="version-mark">v7.0.0で追加</span> {#code-tidb-opt-derive-topn-code-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   [ウィンドウ関数からTopNまたはLimitを導出する](/derive-topn-from-window.md)最適化ルールを有効にするかどうかを制御します。

### tidb_opt_desc_factor {#tidb-opt-desc-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKVがディスクから1行を降順でスキャンする際のコストを示します。この変数は[コストモデル](/cost-model.md)の内部で使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_disk_factor {#tidb-opt-disk-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `1.5`
-   TiDBが一時ディスクから1バイトのデータを読み書きする際のI/Oコストを示します。この変数は内部的に[コストモデル](/cost-model.md)で使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_distinct_agg_push_down {#tidb-opt-distinct-agg-push-down}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが集約関数を`distinct` ( `select count(distinct a) from t`など) でコプロセッサーにプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリで`distinct`操作を含む集計関数が遅い場合は、変数の値を`1`に設定できます。

次の例では、 `tidb_opt_distinct_agg_push_down`有効になる前に、TiDB は TiKV からすべてのデータを読み込み、TiDB 側で`distinct`実行する必要があります。5 `tidb_opt_distinct_agg_push_down`有効になった後、 `distinct a`コプロセッサーにプッシュダウンされ、 `group by`番目の列`test.t.a`が`HashAgg_5`に追加されます。

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

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザが列順序の相関に基づいて行数を推定するかどうかを制御するために使用されます。

### tidb_opt_enable_hash_join は<span class="version-mark">、v6.5.6、v7.1.2、v7.4.0 で新しく追加されました。</span> {#tidb-opt-enable-hash-join-span-class-version-mark-new-in-v6-5-6-v7-1-2-and-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザがテーブルのハッシュ結合を選択するかどうかを制御するために使用されます。デフォルト値は`ON`です`OFF`に設定すると、他の結合アルゴリズムが利用できない場合を除き、オプティマイザは実行プラン生成時にハッシュ結合を選択しません。
-   システム変数`tidb_opt_enable_hash_join`とヒント`HASH_JOIN`両方が設定されている場合、ヒント`HASH_JOIN`が優先されます。7 `tidb_opt_enable_hash_join` `OFF`設定されている場合でも、クエリでヒント`HASH_JOIN`を指定すると、TiDBオプティマイザはハッシュ結合プランを適用します。

### tidb_opt_enable_non_eval_scalar_subquery <span class="version-mark">v7.3.0で追加</span> {#tidb-opt-enable-non-eval-scalar-subquery-span-class-version-mark-new-in-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、最適化段階で展開可能な定数サブクエリの実行を`EXPLAIN`ステートメントで無効にするかどうかを制御するために使用されます。この変数が`OFF`に設定されている場合、 `EXPLAIN`ステートメントは最適化段階でサブクエリを事前に展開します。この変数が`ON`に設定されている場合、 `EXPLAIN`ステートメントは最適化段階でサブクエリを展開しません。詳細については、以下を参照してください。 [サブクエリ展開を無効にする](/explain-walkthrough.md#disable-the-early-execution-of-subqueries)サブクエリ

### tidb_opt_enable_late_materialization <span class="version-mark">v7.0.0で追加</span> {#tidb-opt-enable-late-materialization-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [TiFlashの遅延実現](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御するために使用されます。 TiFlash の遅延実体化は[高速スキャンモード](/tiflash/use-fastscan.md)では有効にならないことに注意してください。
-   この変数を`OFF`に設定してTiFlash の遅延マテリアライゼーション機能を無効にした場合、フィルタ条件 ( `WHERE`句) を含む`SELECT`ステートメントを処理するために、 TiFlash はフィルタリング前に必要な列のすべてのデータをスキャンします。この変数を`ON`に設定してTiFlash の遅延マテリアライゼーション機能を有効にすると、 TiFlash は、TableScan オペレータにプッシュダウンされたフィルタ条件に関連する列データを最初にスキャンし、条件を満たす行をフィルタリングしてから、これらの行の他の列のデータをスキャンしてさらに計算を行うことができ、データ処理の IO スキャンと計算を削減できます。

### tidb_opt_enable_mpp_shared_cte_execution <span class="version-mark">v7.2.0で追加</span> {#tidb-opt-enable-mpp-shared-cte-execution-span-class-version-mark-new-in-v7-2-0-span}

> **警告：**
>
> この変数で制御される機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非再帰的な[共通テーブル式（CTE）](/sql-statements/sql-statement-with.md) TiFlash MPP上で実行できるかどうかを制御します。デフォルトでは、この変数が無効になっている場合、CTEはTiDB上で実行されますが、この機能を有効にした場合と比較してパフォーマンスに大きな差が生じます。

### tidb_opt_enable_fuzzy_binding <span class="version-mark">v7.6.0で追加</span> {#tidb-opt-enable-fuzzy-binding-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は[クロスデータベースバインディング](/sql-plan-management.md#cross-database-binding)機能を有効にするかどうかを制御します。

### tidb_opt_enable_no_decorrelate_in_select <span class="version-mark">v8.5.4で追加</span> {#tidb-opt-enable-no-decorrelate-in-select-span-class-version-mark-new-in-v8-5-4-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `SELECT`リスト内のサブクエリを含むすべてのクエリに対してオプティマイザが[`NO_DECORRELATE()`](/optimizer-hints.md#no_decorrelate)ヒントを適用するかどうかを制御します。

### tidb_opt_enable_semi_join_rewrite は<span class="version-mark">v8.5.4 で追加されました。</span> {#tidb-opt-enable-semi-join-rewrite-span-class-version-mark-new-in-v8-5-4-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、サブクエリを含むすべてのクエリに対してオプティマイザが[`SEMI_JOIN_REWRITE()`](/optimizer-hints.md#semi_join_rewrite)ヒントを適用するかどうかを制御します。

### tidb_opt_fix_control は<span class="version-mark">v6.5.3 および v7.1.0 で追加されました。</span> {#tidb-opt-fix-control-span-class-version-mark-new-in-v6-5-3-and-v7-1-0-span}

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 文字列
-   デフォルト値: `""`
-   この変数は、オプティマイザの内部動作の一部を制御するために使用されます。
-   オプティマイザの動作は、ユーザーシナリオやSQLステートメントによって異なる場合があります。この変数を使用することで、オプティマイザをより細かく制御でき、オプティマイザの動作変更によってアップグレード後に発生するパフォーマンス低下を防ぐことができます。
-   より詳細な概要については、[オプティマイザー修正コントロール](/optimizer-fix-controls.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 文字列
-   デフォルト値: `""`
-   この変数は、オプティマイザの内部動作の一部を制御するために使用されます。
-   オプティマイザの動作は、ユーザーシナリオやSQLステートメントによって異なる場合があります。この変数を使用することで、オプティマイザをより細かく制御でき、オプティマイザの動作変更によってアップグレード後に発生するパフォーマンス低下を防ぐことができます。
-   より詳細な概要については、[オプティマイザー修正コントロール](/optimizer-fix-controls.md)参照してください。

</CustomContent>

### tidb_opt_force_inline_cte <span class="version-mark">v6.3.0で追加</span> {#tidb-opt-force-inline-cte-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、セッション全体の共通テーブル式（CTE）をインライン化するかどうかを制御するために使用されます。デフォルト値は`OFF`で、デフォルトでは CTE のインライン化は強制されません。ただし、ヒント`MERGE()`を指定することで CTE をインライン化できます。この変数を`ON`に設定すると、このセッション内のすべての CTE（再帰 CTE を除く）が強制的にインライン化されます。

### tidb_opt_advanced_join_hint <span class="version-mark">v7.0.0 の新機能</span> {#tidb-opt-advanced-join-hint-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`HASH_JOIN()`ヒント](/optimizer-hints.md#hash_joint1_name--tl_name-)や[`MERGE_JOIN()`ヒント](/optimizer-hints.md#merge_joint1_name--tl_name-)などの結合方法ヒントが、 [`LEADING()`ヒント](/optimizer-hints.md#leadingt1_name--tl_name-)の使用を含む結合したテーブルの再配置最適化プロセスに影響を与えるかどうかを制御するために使用されます。デフォルト値は`ON`で、これは影響を与えないことを意味します。9に設定すると、結合方法ヒントと`LEADING()`ヒント`OFF`同時に使用されるシナリオで競合が発生する可能性があります。

> **注記：**
>
> v7.0.0より前のバージョンでは、この変数を`OFF`に設定した場合と同様の動作となります。前方互換性を確保するため、以前のバージョンからv7.0.0以降のクラスタにアップグレードする場合、この変数は`OFF`に設定されます。より柔軟なヒント動作を実現するには、パフォーマンスの低下がないことを条件に、この変数を`ON`に切り替えることを強くお勧めします。

### tidb_opt_insubq_to_join_and_agg {#tidb-opt-insubq-to-join-and-agg}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、サブクエリを結合と集計に変換する最適化ルールを有効にするかどうかを設定するために使用されます。
-   例えば、この最適化ルールを有効にすると、サブクエリは次のように変換されます。

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    サブクエリは次のように結合に変換されます。

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    `aa`列目の`t1` `unique`と`not null`に制限されている場合、集計なしで以下のステートメントを使用できます。

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold {#tidb-opt-join-reorder-threshold}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDBの結合したテーブルの再配置アルゴリズムの選択を制御するために使用されます。Join 結合したテーブルの再配置に参加するノード数がこのしきい値を超えると、TiDBは貪欲アルゴリズムを選択し、このしきい値を下回ると、TiDBは動的計画法アルゴリズムを選択します。
-   現在、OLTPクエリの場合はデフォルト値を維持することを推奨します。OLAPクエリの場合は、OLAPシナリオでの接続順序を改善するために、変数の値を10～15に設定することをお勧めします。

### tidb_opt_limit_push_down_threshold {#tidb-opt-limit-push-down-threshold}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   この変数は、Limit または TopN 演算子を TiKV まで下げるかどうかを決定するしきい値を設定するために使用されます。
-   Limit演算子またはTopN演算子の値がこのしきい値以下の場合、これらの演算子は強制的にTiKVにプッシュダウンされます。この変数により、推定値の誤りなどが原因でLimit演算子またはTopN演算子をTiKVにプッシュダウンできないという問題が解決されます。

### tidb_opt_memory_factor {#tidb-opt-memory-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `0.001`
-   TiDBが1行を保存するために必要メモリ量を示します。この変数は内部的に[コストモデル](/cost-model.md)で使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">v5.1.0で追加</span> {#tidb-opt-mpp-outer-join-fixed-build-side-span-class-version-mark-new-in-v5-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   変数の値が`ON`場合、左結合演算子は常に内部テーブルを構築側として使用し、右結合演算子は常に外部テーブルを構築側として使用します。値を`OFF`に設定すると、外部結合演算子はテーブルのどちら側でも構築側として使用できます。

### tidb_opt_network_factor {#tidb-opt-network-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.0`
-   ネットワーク経由で1バイトのデータを転送する際の正味コストを示します。この変数は[コストモデル](/cost-model.md)の内部で使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_objective <span class="version-mark">v7.4.0で追加</span> {#tidb-opt-objective-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: 列挙型
-   デフォルト値: `moderate`
-   可能な`determinate` : `moderate`
-   この変数はオプティマイザの目的を制御します。1 `moderate` TiDB v7.4.0 より前のバージョンにおけるデフォルトの動作を維持し、オプティマイザはより多くの情報を使用してより良い実行プランを生成しようとします。3 `determinate`はより保守的になり、実行プランをより安定させます。
-   リアルタイム統計とは、DMLステートメントに基づいて自動的に更新される行の総数と変更された行の数です。この変数が`moderate` （デフォルト）に設定されている場合、TiDBはリアルタイム統計に基づいて実行プランを生成します。この変数が`determinate`に設定されている場合、TiDBは実行プランの生成にリアルタイム統計を使用しないため、実行プランがより安定します。
-   長期的に安定したOLTPワークロードを維持する場合、またはユーザーが既存の実行プランに満足している場合は、予期せぬ実行プランの変更の可能性を減らすために、モード`determinate`を使用することをお勧めします。さらに、[`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)を使用することで、統計情報の変更を防ぎ、実行プランをより安定させることができます。

### tidb_opt_ordering_index_selectivity_ratio <span class="version-mark">v8.0.0で追加</span> {#tidb-opt-ordering-index-selectivity-ratio-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: セッション | グローバル

-   クラスターに保持される: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい

-   タイプ: フロート

-   デフォルト値: `-1`

-   範囲: `[-1, 1]`

-   この変数は、SQL文に`ORDER BY`または`LIMIT`の句がある場合に、SQL文`ORDER BY`に一致するインデックスの推定行数を制御しますが、一部のフィルタ条件はカバーしません。

-   これは、システム変数[tidb_opt_ordering_index_selectivity_threshold](#tidb_opt_ordering_index_selectivity_threshold-new-in-v700)と同じクエリパターンに対応します。

-   実装方法が異なるのは、条件を満たす行が見つかる可能性のある範囲の比率またはパーセンテージを適用する点です。

-   値が`-1` （デフォルト値）または`0`未満の場合、この比率は無効になります。5から`1`の間`0`値を指定すると、0%から100%までの比率が適用されます（例えば、 `0.5` `50%`に相当します）。

-   以下の例では、テーブル`t`は合計 1,000,000 行があります。同じクエリが使用されますが、 `tidb_opt_ordering_index_selectivity_ratio`の値は異なります。例のクエリには、行のごく一部 (1,000,000 行のうち 9,000 行) を条件とする`WHERE`句述語が含まれています。7 `ORDER BY a`サポートするインデックス (インデックス`ia` ) はありますが、 `b`のフィルタはこのインデックスには含まれていません。実際のデータ分布によっては、 `WHERE`句と`LIMIT 1`に一致する行は、フィルタなしインデックスをスキャンしたときに最初にアクセスされる行として見つかる場合もあれば、最悪の場合、ほぼすべての行が処理された後に見つかる場合もあります。

-   各例では、インデックスヒントを使用してestRowsへの影響を示しています。最終的なプランの選択は、他のプランの利用可能性とコストによって決まります。

-   最初の例では、デフォルト値の`-1`を使用しています。これは、既存の推定式を使用するものです。デフォルトでは、対象となる行が見つかる前に、推定のために少数の行がスキャンされます。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = -1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | id                                | estRows | task      | access object         | operator info                   |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00    | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00    | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 109.20  | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 109.20  | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    ```

-   2番目の例では`0`使用していますが、これは条件を満たす行が見つかるまでにスキャンされる行の割合が0%であることを前提としています。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 0;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | id                                | estRows | task      | access object         | operator info                   |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00    | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00    | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 1.00    | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 1.00    | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    ```

-   3番目の例では、条件を満たす行が見つかるまでに行の10%がスキャンされると想定した`0.1`使用しています。この条件は非常に選択的で、条件を満たす行はわずか1%です。したがって、最悪の場合、条件を満たす1%の行を見つけるまでに、行の99%をスキャンする必要があるかもしれません。その99%の10%は約9.9%であり、これはestRowsに反映されます。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 0.1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    | id                                | estRows  | task      | access object         | operator info                   |
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00     | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00     | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00     | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 99085.21 | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00     | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 99085.21 | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    ```

-   4番目の例では`1.0`使用していますが、これは条件を満たす行が見つかる前にすべての行がスキャンされることを前提としています。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    | id                                | estRows   | task      | access object         | operator info                   |
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00      | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00      | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00      | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 990843.14 | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00      | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 990843.14 | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    ```

-   5番目の例も`1.0`使用していますが、 `a`に述語を追加することで、最悪の場合のスキャン範囲を制限しています。これは、 `WHERE a <= 9000`インデックスに一致し、約9,000行が該当するためです。7 `b`フィルタ述語はインデックスに含まれていないため、 `b <= 9000`に一致する行が見つかる前に、約9,000行すべてがスキャンされたとみなされます。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE a <= 9000 AND b <= 9000 ORDER BY a LIMIT 1;
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    | id                                 | estRows | task      | access object         | operator info                      |
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    | Limit_12                           | 1.00    | root      |                       | offset:0, count:1                  |
    | └─Projection_22                    | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c       |
    |   └─IndexLookUp_21                 | 1.00    | root      |                       |                                    |
    |     ├─IndexRangeScan_18(Build)     | 9074.99 | cop[tikv] | table:t, index:ia(a)  | range:[-inf,9000], keep order:true |
    |     └─Selection_20(Probe)          | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)                 |
    |       └─TableRowIDScan_19          | 9074.99 | cop[tikv] | table:t               | keep order:false                   |
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    ```

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">v7.0.0で追加</span> {#tidb-opt-ordering-index-selectivity-threshold-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、SQL文にフィルタ条件を含む句が`ORDER BY`または`LIMIT`ある場合に、オプティマイザがインデックスを選択する方法を制御するために使用されます。
-   このようなクエリの場合、オプティマイザは、対応するインデックスを選択して、 `ORDER BY`と`LIMIT`項を満たすことを検討します（たとえそのインデックスがフィルタ条件を満たしていなくても）。ただし、データ分布の複雑さから、このシナリオではオプティマイザが最適ではないインデックスを選択する可能性があります。
-   この変数はしきい値を表します。フィルタリング条件を満たすインデックスが存在し、その選択性推定値がこのしきい値よりも低い場合、オプティマイザは`ORDER BY`と`LIMIT`を満たすために使用されるインデックスの選択を避けます。代わりに、フィルタリング条件を満たすインデックスを優先します。
-   例えば、変数が`0`に設定されている場合、オプティマイザはデフォルトの動作を維持します。変数が`1`に設定されている場合、オプティマイザは常にフィルタ条件を満たすインデックスの選択を優先し、 `ORDER BY`と`LIMIT`項の両方を満たすインデックスの選択を回避します。
-   次の例では、テーブル`t`には合計 1,000,000 行があります。列`b`にインデックスを使用すると、推定行数は約 8,748 なので、選択性の推定値は約 0.0087 になります。デフォルトでは、オプティマイザは列`a`にインデックスを選択します。しかし、この変数を 0.01 に設定すると、列`b`のインデックスの選択性 (0.0087) が 0.01 未満になるため、オプティマイザは列`b`にインデックスを選択します。

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

### tidb_opt_prefer_range_scan <span class="version-mark">v5.0で追加</span> {#tidb-opt-prefer-range-scan-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> バージョン8.4.0以降、この変数のデフォルト値は`OFF`から`ON`に変更されました。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数の値が`ON`場合、オプティマイザは、統計情報のないテーブル (擬似統計情報) または空のテーブル (統計情報がゼロ) に対して、フルテーブルスキャンよりも範囲スキャンを優先します。
-   次の例では、 `tidb_opt_prefer_range_scan`有効にする前は、TiDB オプティマイザはフルテーブルスキャンを実行します。3 `tidb_opt_prefer_range_scan`有効にすると、オプティマイザはインデックス範囲スキャンを選択します。

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

### tidb_opt_prefix_index_single_scan <span class="version-mark">v6.4.0で追加</span> {#tidb-opt-prefix-index-single-scan-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `ON`
-   この変数は、TiDBオプティマイザが不要なテーブル検索を回避し、クエリパフォーマンスを向上させるために、一部のフィルタ条件をプレフィックスインデックスにプッシュダウンするかどうかを制御します。
-   この変数の値が`ON`に設定されている場合、一部のフィルタ条件がプレフィックス インデックスにプッシュダウンされます。たとえば、テーブルの`col`列がインデックスのプレフィックス 列であるとします。クエリ内の`col is null`または`col is not null`条件は、テーブル検索のフィルタ条件ではなく、インデックスのフィルタ条件として処理されるため、不要なテーブル検索が回避されます。

<details><summary><code>tidb_opt_prefix_index_single_scan</code>の使用例</summary>

プレフィックスインデックス付きのテーブルを作成します。

```sql
CREATE TABLE t (a INT, b VARCHAR(10), c INT, INDEX idx_a_b(a, b(5)));
```

無効化`tidb_opt_prefix_index_single_scan` :

```sql
SET tidb_opt_prefix_index_single_scan = 'OFF';
```

次のクエリの場合、実行プランではプレフィックスインデックス`idx_a_b`を使用しますが、テーブルルックアップが必要です（ `IndexLookUp`演算子が表示されます）。

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

この変数を有効にすると、次のクエリの実行プランではプレフィックスインデックス`idx_a_b`が使用されますが、テーブルルックアップは不要になります。

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

### tidb_opt_projection_push_down <span class="version-mark">v6.1.0で追加</span> {#tidb-opt-projection-push-down-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`より前のバージョンでは、デフォルト値は`OFF`でした。
-   オプティマイザが`Projection`演算子を TiKV コプロセッサにプッシュダウンすることを許可するかどうかを指定します。有効にすると、オプティマイザは次の 3 種類の`Projection`演算子を TiKV にプッシュダウンする可能性があります。
    -   演算子のトップレベル式はすべて[JSONクエリ関数](/functions-and-operators/json-functions/json-functions-search.md)または[JSON値属性関数](/functions-and-operators/json-functions/json-functions-return.md)です。例: `SELECT JSON_EXTRACT(data, '$.name') FROM users;` 。
    -   演算子の最上位式には、JSON クエリ関数または JSON 値属性関数と直接列読み取りの組み合わせが含まれます。例: `SELECT JSON_DEPTH(data), name FROM users;` 。
    -   演算子の最上位式はすべて直接列読み取りであり、出力列の数は入力列の数より少ない。例: `SELECT name FROM users;` 。
-   `Projection`演算子を押し下げる最終決定は、オプティマイザによるクエリコストの総合的な評価にも依存します。
-   TiDB クラスターが v8.3.0 より前のバージョンから v8.3.0 以降にアップグレードされた場合、この変数のデフォルト値は`OFF`です。

### tidb_opt_range_max_size <span class="version-mark">v6.4.0で追加</span> {#tidb-opt-range-max-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値： `67108864` （64 MiB）
-   範囲: `[0, 9223372036854775807]`
-   単位：バイト
-   この変数は、オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を設定するために使用されます。変数の値が`0`の場合、スキャン範囲の構築にメモリ制限はありません。正確なスキャン範囲の構築によって消費されるメモリが制限を超える場合、オプティマイザはより緩やかなスキャン範囲 (例えば`[[NULL,+inf]]` ) を使用します。実行プランで正確なスキャン範囲を使用しない場合は、この変数の値を増やすことで、オプティマイザが正確なスキャン範囲を構築できるようになります。

この変数の使用例は以下のとおりです。

<details><summary><code>tidb_opt_range_max_size</code>使用例</summary>

この変数のデフォルト値をビュー。結果から、オプティマイザがスキャン範囲の構築に最大64MiBのメモリを使用していることがわかります。

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

64 MiB のメモリ上限では、オプティマイザは次の実行プランの結果に示すように、次の正確なスキャン範囲`[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`構築します。

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

次に、オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を1500バイトに設定します。

```sql
SET @@tidb_opt_range_max_size = 1500;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

1500バイトのメモリ制限では、オプティマイザはより緩やかなスキャン範囲`[10,10], [20,20], [30,30]`構築し、正確なスキャン範囲を構築するために必要なメモリ使用量が制限`tidb_opt_range_max_size`を超えていることをユーザーに警告します。

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

次に、メモリ使用量の上限を100バイトに設定します。

```sql
set @@tidb_opt_range_max_size = 100;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

100バイトのメモリ制限では、オプティマイザは`IndexFullScan`選択し、正確なスキャン範囲を構築するために必要なメモリが`tidb_opt_range_max_size`の制限を超えていることをユーザーに警告します。

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

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.5`
-   TiKVがディスクから1行のデータを昇順でスキャンする際のコストを示します。この変数は[コストモデル](/cost-model.md)内部で使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_seek_factor {#tidb-opt-seek-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `20`
-   TiDBがTiKVからデータを要求する際の起動コストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_skew_distinct_agg <span class="version-mark">v6.2.0で追加</span> {#tidb-opt-skew-distinct-agg-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この変数を有効にすることでクエリのパフォーマンスを最適化する効果は**、 TiFlashに対してのみ**有効です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが`DISTINCT`集計関数を2段階の集計関数に書き換えるかどうかを設定します（例えば、 `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換えるなど）。集計列に深刻な偏りがあり、 `DISTINCT`列目に多くの異なる値がある場合、この書き換えによってクエリ実行時のデータ偏りを回避し、クエリのパフォーマンスを向上させることができます。

### tidb_opt_three_stage_distinct_agg <span class="version-mark">v6.3.0で追加</span> {#tidb-opt-three-stage-distinct-agg-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、MPPモードで`COUNT(DISTINCT)`集計を3段階集計に書き換えるかどうかを指定します。
-   この変数は現在、 `COUNT(DISTINCT)`のみを含む集計に適用されます。

### tidb_opt_tiflash_concurrency_factor {#tidb-opt-tiflash-concurrency-factor}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `24.0`
-   TiFlash計算の同時実行数を示します。この変数はコストモデル内部で使用されるため、値を変更することは推奨されません。

### tidb_opt_use_invisible_indexes <span class="version-mark">v8.0.0で追加</span> {#tidb-opt-use-invisible-indexes-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが現在のセッションでクエリ最適化のために[目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)を選択できるかどうかを制御します。非表示のインデックスは DML ステートメントによって維持されますが、クエリ最適化では使用されません。これは、インデックスを完全に削除する前に二重チェックしたい場合に役立ちます。この変数が`ON`に設定されている場合、オプティマイザはセッションでクエリ最適化のために非表示のインデックスを選択できます。

### tidb_opt_write_row_id {#tidb-opt-write-row-id}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `INSERT` `UPDATE`ステートメントが`_tidb_rowid`番目の列に対して操作を実行することを許可するかどうかを制御するために使用されます。この変数は`REPLACE` TiDBツールを使用してデータをインポートする場合にのみ使用できます。

### tidb_opt_hash_agg_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-hash-agg-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_hash_join_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-hash-join-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_join_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-index-join-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_lookup_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-index-lookup-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_merge_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-index-merge-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_reader_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-index-reader-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_scan_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-index-scan-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_limit_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-limit-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_merge_join_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-merge-join-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_sort_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-sort-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_stream_agg_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-stream-agg-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_full_scan_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-table-full-scan-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_range_scan_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-table-range-scan-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_reader_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-table-reader-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_rowid_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-table-rowid-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_tiflash_scan_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-table-tiflash-scan-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_topn_cost_factor <span class="version-mark">v8.5.3で追加</span> {#tidb-opt-topn-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用され、その値を変更することはお勧め**できません**。

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_optimizer_selectivity_level {#tidb-optimizer-selectivity-level}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、最適化アルゴリズムの推定ロジックの反復回数を制御します。この変数の値を変更すると、最適化アルゴリズムの推定ロジックが大きく変化します。現在、有効な値は`0`のみです。他の値を設定することは推奨されません。

### tidb_partition_prune_mode <span class="version-mark">v5.1で追加</span> {#tidb-partition-prune-mode-span-class-version-mark-new-in-v5-1-span}

> **警告：**
>
> バージョン8.5.0以降、この変数を`static`または`static-only`に設定すると警告が表示されます。この変数は今後のリリースで非推奨となります。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: 列挙型
-   デフォルト値: `dynamic`
-   `dynamic` `dynamic-only`値`static-only` `static`
-   パーティションテーブルに`dynamic`モードを使用するか`static`モードを使用するかを指定します。動的パーティショニングは、完全なテーブルレベル統計、またはグローバル統計が収集された後にのみ有効であることに注意してください。グローバル統計収集が完了する前に`dynamic`プルーニング モードを有効にした場合、TiDB はグローバル統計が完全に収集されるまで`static`モードのままになります。グローバル統計の詳細については、 [動的プルーニングモードでパーティションテーブルの統計情報を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)。動的プルーニング モードの詳細については、[パーティションテーブルの動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)参照してください。

### tidb_persist_analyze_options は<span class="version-mark">v5.4.0 で追加されました。</span> {#tidb-persist-analyze-options-span-class-version-mark-new-in-v5-4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は[構成の永続性を分析する](/statistics.md#persist-analyze-configurations)機能を有効にするかどうかを制御します。

### tidb_pessimistic_txn_fair_locking <span class="version-mark">v7.0.0で追加</span> {#tidb-pessimistic-txn-fair-locking-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   悲観的トランザクションに対して拡張悲観的ロックウェイクアップモデルを使用するかどうかを決定します。このモデルは、悲観的ロックの単一点競合シナリオにおける悲観的トランザクションのウェイクアップ順序を厳密に制御し、不要なウェイクアップを回避します。既存のウェイクアップメカニズムのランダム性によって生じる不確実性を大幅に低減します。ビジネスシナリオで頻繁に単一点悲観的ロックの競合が発生し（同じデータ行への頻繁な更新など）、その結果、ステートメントの再試行が頻繁に発生したり、テールレイテンシーが高くなったり、場合によってはエラー`pessimistic lock retry limit reached`が発生する場合は、この変数を有効にして問題を解決してみてください。
-   この変数は、TiDBクラスタをv7.0.0より前のバージョンからv7.0.0以降のバージョンにアップグレードする場合、デフォルトで無効になっています。

> **注記：**
>
> -   具体的なビジネスシナリオによっては、このオプションを有効にすると、ロックの競合が頻繁に発生するトランザクションにおいて、スループットが一定程度低下する（平均レイテンシーが増加する）可能性があります。
> -   このオプションは、単一のキーをロックする必要があるステートメントにのみ有効です。ステートメントが複数の行を同時にロックする必要がある場合、このオプションは有効になりません。
> -   この機能は、デフォルトでは無効になっている[`tidb_pessimistic_txn_aggressive_locking`](https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)変数によってv6.6.0で導入されました。

### tidb_placement_mode <span class="version-mark">v6.0.0で追加</span> {#tidb-placement-mode-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `STRICT`
-   可能な`IGNORE` : `STRICT`
-   この変数は、DDL ステートメントが[SQLで指定された配置ルール](/placement-rules-in-sql.md)を無視するかどうかを制御します。変数値が`IGNORE`の場合、すべての配置ルール オプションは無視されます。
-   これは、論理ダンプ/リストアツールが、無効な配置ルールが割り当てられた場合でもテーブルが必ず作成されるようにするために使用されます。これは、mysqldumpがすべてのダンプファイルの先頭に`SET FOREIGN_KEY_CHECKS=0;`書き込むのと同様の仕組みです。

### <code>tidb_plan_cache_invalidation_on_fresh_stats</code> <span class="version-mark">v7.1.0 で追加されました。</span> {#code-tidb-plan-cache-invalidation-on-fresh-stats-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、関連テーブルの統計情報が更新されたときに、プランキャッシュを自動的に無効化するかどうかを制御します。
-   この変数を有効にすると、プランキャッシュは統計情報をより効果的に活用して実行プランを生成できるようになります。例えば、次のようになります。
    -   統計情報が利用可能になる前に実行計画が生成された場合、統計情報が利用可能になった時点で、計画キャッシュは実行計画を再生成します。
    -   テーブルのデータ分布が変化し、以前は最適だった実行プランが最適ではなくなった場合、プランキャッシュは統計情報を再収集した後、実行プランを再生成します。
-   この変数は、TiDBクラスタをv7.1.0より前のバージョンからv7.1.0以降にアップグレードする場合、デフォルトで無効になります。

### <code>tidb_plan_cache_max_plan_size</code> <span class="version-mark">v7.1.0 で追加されました。</span> {#code-tidb-plan-cache-max-plan-size-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値： `2097152` （2MiBに相当）
-   範囲： `[0, 9223372036854775807]` （バイト単位）。「KiB|MiB|GiB|TiB」単位のメモリ形式もサポートされています。3 `0`制限なしを意味します。
-   この変数は、準備済みプラン キャッシュまたは準備されていないプラン キャッシュにキャッシュできるプランの最大サイズを制御します。プランのサイズがこの値を超える場合、プランはキャッシュされません。詳細については、 [準備済みプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)[準備されていないプランキャッシュ](/sql-plan-management.md#usage)を参照してください。

### tidb_pprof_sql_cpu <span class="version-mark">v4.0で追加</span> {#tidb-pprof-sql-cpu-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、プロファイル出力において対応するSQL文をマークして、パフォーマンスの問題を特定およびトラブルシューティングするかどうかを制御するために使用されます。

### tidb_prefer_broadcast_join_by_exchange_data_size<span class="version-mark">は v7.1.0 で追加されました。</span> {#tidb-prefer-broadcast-join-by-exchange-data-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `OFF`
-   この変数は、TiDBが[MPPハッシュ結合アルゴリズム](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode)この変数が有効になっている場合、TiDBはネットワークで交換されるデータのサイズをそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`を使用して推定し、より小さいサイズを選択します。
-   この変数が有効になった後は、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)有効になりません。

### tidb_prepared_plan_cache_memory_guard_ratio は<span class="version-mark">v6.1.0 で追加されました。</span> {#tidb-prepared-plan-cache-memory-guard-ratio-span-class-version-mark-new-in-v6-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: フロート
-   デフォルト値: `0.1`
-   範囲: `[0, 1]`
-   準備されたプラン キャッシュがメモリ保護メカニズムをトリガーするしきい値。詳細については、[プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)ご覧ください。
-   この設定は以前はオプション`tidb.toml` （ `prepared-plan-cache.memory-guard-ratio` ）でしたが、TiDB v6.1.0以降はシステム変数に変更されました。

### tidb_prepared_plan_cache_size <span class="version-mark">v6.1.0で追加</span> {#tidb-prepared-plan-cache-size-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> バージョン7.1.0以降、この変数は非推奨となりました。代わりに、 [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   セッション内にキャッシュできるプランの最大数。詳細については、[プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)ご覧ください。
-   この設定は以前はオプション`tidb.toml` （ `prepared-plan-cache.capacity` ）でしたが、TiDB v6.1.0以降はシステム変数に変更されました。

### tidb_projection_concurrency {#tidb-projection-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨となりました。代わりに、[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位：糸
-   この変数は、 `Projection`演算子の同時実行数を設定するために使用されます。
-   値が`-1`の場合は、代わりに値`tidb_executor_concurrency`が使用されます。

### tidb_query_log_max_len {#tidb-query-log-max-len}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値： `4096` （4 KiB）
-   範囲: `[0, 1073741824]`
-   単位：バイト
-   SQL ステートメントの出力の最大長。ステートメントの出力長が`tidb_query_log_max_len`値より大きい場合、ステートメントは切り詰められて出力されます。
-   この設定は以前はオプション`tidb.toml` （ `log.query-log-max-len` ）としても利用可能でしたが、TiDB v6.1.0以降はシステム変数としてのみ利用可能です。

### tidb_rc_read_check_ts は<span class="version-mark">v6.0.0 で追加されました。</span> {#tidb-rc-read-check-ts-span-class-version-mark-new-in-v6-0-0-span}

> **警告：**
>
> -   この機能は[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。3と`tidb_rc_read_check_ts` `replica-read`同時に有効にしないでください。
> -   クライアントがカーソルを使用している場合、返されたデータの前のバッチが既にクライアントによって使用されており、最終的にステートメントが失敗する可能性があるため、 `tidb_rc_read_check_ts`有効にすることは推奨されません。
> -   バージョン7.0.0以降、この変数は、プリペアドステートメントプロトコルを使用するカーソルフェッチ読み取りモードでは無効になります。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数はタイムスタンプの取得を最適化するために使用され、読み取りコミット分離レベルが採用され、読み書きの競合がまれなシナリオに適しています。この変数を有効にすることで、グローバルタイムスタンプの取得に伴うレイテンシーとコストを回避し、トランザクションレベルの読み取りレイテンシーを最適化できます。
-   読み取り/書き込み競合が深刻な場合、この機能を有効にすると、グローバル タイムスタンプを取得するコストとレイテンシーが増加し、パフォーマンスの低下を引き起こす可能性があります。詳細については、 [隔離レベルを遵守する](/transaction-isolation-levels.md#read-committed-isolation-level)ご覧ください。

### tidb_rc_write_check_ts は<span class="version-mark">v6.3.0 で追加されました。</span> {#tidb-rc-write-check-ts-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この機能は現在、 [`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。この変数を有効にすると、クライアントから送信されるすべてのリクエストで`replica-read`使用できなくなります。したがって、 `tidb_rc_write_check_ts`と`replica-read`同時に有効にしないでください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数はタイムスタンプの取得を最適化するために使用され、悲観的トランザクションの分離レベル`READ-COMMITTED`でポイント書き込み競合が少ないシナリオに適しています。この変数を有効にすると、ポイント書き込みステートメントの実行中にグローバルタイムスタンプを取得することによって発生するレイテンシーとオーバーヘッドを回避できます。現在、この変数は`UPDATE` 、 `DELETE` 、および`SELECT ...... FOR UPDATE`の 3 種類のポイント書き込みステートメントに適用できます。ポイント書き込みステートメントとは、フィルタ条件として主キーまたは一意キーを使用し、最終実行演算子に`POINT-GET`含まれる書き込みステートメントを指します。
-   ポイントと書き込みの競合が深刻な場合、この変数を有効にすると、余分なオーバーヘッドとレイテンシーが増加し、パフォーマンスの低下につながります。詳細については、 [隔離レベルを遵守する](/transaction-isolation-levels.md#read-committed-isolation-level)ご覧ください。

### tidb_read_consistency <span class="version-mark">v5.4.0で追加</span> {#tidb-read-consistency-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用: はい ([非トランザクションDMLステートメント](/non-transactional-dml.md)が存在する場合、ヒントを使用してこの変数の値を変更しても有効にならない可能性があることに注意してください。)
-   型: 文字列
-   デフォルト値: `strict`
-   この変数は、自動コミット読み取りステートメントの読み取り一貫性を制御するために使用されます。
-   変数の値が`weak`に設定されている場合、read ステートメントで発生するロックは直接スキップされ、read の実行が高速化される可能性があります。これは弱一貫性読み取りモードです。ただし、トランザクションのセマンティクス（原子性など）や分散一貫性（線形化可能性など）は保証されません。
-   自動コミット読み取りが高速で、かつ弱い整合性の読み取り結果でも許容されるユーザーシナリオでは、弱い整合性の読み取りモードを使用できます。

### tidb_read_staleness <span class="version-mark">v5.4.0で追加</span> {#tidb-read-staleness-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[-2147483648, 0]`
-   この変数は、TiDBが現在のセッションで読み取ることができる履歴データの時間範囲を設定するために使用されます。値を設定すると、TiDBはこの変数で許可された範囲から可能な限り新しいタイムスタンプを選択し、以降のすべての読み取り操作はこのタイムスタンプに対して実行されます。たとえば、この変数の値が`-5`に設定されている場合、TiKVが対応する履歴バージョンのデータを持っているという条件の下で、TiDBは5秒以内の時間範囲内で可能な限り新しいタイムスタンプを選択します。

### tidb_record_plan_in_slow_log {#tidb-record-plan-in-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、遅いクエリの実行プランをスローログに含めるかどうかを制御するために使用されます。

### tidb_redact_log {#tidb-redact-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `OFF`
-   `ON` `MARKER`値： `OFF`
-   この変数は、TiDBログおよびスローログに記録されるSQLステートメント内のユーザー情報を非表示にするかどうかを制御します。
-   デフォルト値は`OFF`で、これはユーザー情報が一切処理されないことを意味します。
-   変数を`ON`に設定すると、ユーザー情報は非表示になります。例えば、実行されたSQL文が`INSERT INTO t VALUES (1,2)`の場合、ログには`INSERT INTO t VALUES (?,?)`として記録されます。
-   変数を`MARKER`に設定すると、ユーザー情報は`‹ ›`で囲まれます。たとえば、実行された SQL ステートメントが`INSERT INTO t VALUES (1,2)`の場合、ログには`INSERT INTO t VALUES (‹1›,‹2›)`として記録されます。ユーザーデータに`‹`または`›`含まれている場合、 `‹`は`‹‹`に、 `›`は`››`にエスケープされます。マークされたログに基づいて、ログを表示する際にマークされた情報を非機密化するかどうかを決定できます。

### tidb_regard_null_as_point <span class="version-mark">v5.4.0で追加</span> {#tidb-regard-null-as-point-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザがNULL等価性を含むクエリ条件をインデックスアクセスのプレフィックス条件として使用できるかどうかを制御します。
-   この変数はデフォルトで有効になっています。有効になっている場合、オプティマイザはアクセスするインデックスデータの量を削減できるため、クエリの実行が高速化されます。たとえば、クエリに複数列インデックス`index(a, b)`が含まれ、クエリ条件に`a<=>null and b=1`含まれている場合、オプティマイザはクエリ条件内の`a<=>null`と`b=1`両方を使用してインデックスにアクセスします。変数が無効になっている場合、 `a<=>null and b=1`は null 等価条件が含まれているため、オプティマイザはインデックスアクセスに`b=1`使用しません。

### tidb_remove_orderby_in_subquery <span class="version-mark">v6.1.0で追加</span> {#tidb-remove-orderby-in-subquery-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値：v7.2.0より前のバージョンではデフォルト値は`OFF`です。v7.2.0以降ではデフォルト値は`ON`です。
-   サブクエリ内の`ORDER BY`句を削除するかどうかを指定します。
-   ISO/IEC SQL 規格では、 `ORDER BY`主にトップレベルクエリの結果をソートするために使用されます。サブクエリの場合、規格では結果を`ORDER BY`でソートすることを要求していません。
-   サブクエリの結果をソートするには、通常、外側のクエリで処理できます。例えば、ウィンドウ関数を使用したり、外側のクエリで再度`ORDER BY`指定したりする方法があります。こうすることで、最終的な結果セットの順序が保証されます。

### tidb_replica_read <span class="version-mark">v4.0で追加</span> {#tidb-replica-read-span-class-version-mark-new-in-v4-0-span}

<CustomContent platform="tidb-cloud" plan="starter,essential">

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では読み取り専用です。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> この変数は、 [TiDB Cloudプレミアム](https://docs-preview.pingcap.com/tidbcloud/tidb-cloud-intro/#deployment-options)では読み取り専用です。

</CustomContent>

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: 列挙型
-   デフォルト値: `leader`
-   指定可能な値`prefer-leader` 、 `leader` `follower` `learner` `leader-and-follower`値`closest-replicas` `closest-adaptive` 6.6.0で追加`learner`れました。
-   この変数は、TiDBがデータを読み込む場所を制御するために使用されます。バージョン8.5.4以降、この変数は読み取り専用のSQL文にのみ有効です。
-   使用方法と実装の詳細については、 [Follower Read](/follower-read.md)参照してください。

### tidb_restricted_read_only <span class="version-mark">v5.2.0で追加</span> {#tidb-restricted-read-only-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_restricted_read_only`と[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)同様の動作をします。ほとんどの場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを使用してください。
-   権限レベル`SUPER`または`SYSTEM_VARIABLES_ADMIN`ユーザーは、この変数を変更できます。ただし、 [Security強化モード](#tidb_enable_enhanced_security)有効になっている場合は、この変数を読み取りまたは変更するために、追加の権限レベル`RESTRICTED_VARIABLES_ADMIN`が必要になります。
-   `tidb_restricted_read_only` 、以下のケースで[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)影響を与えます。
    -   `tidb_restricted_read_only`から`ON`に設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) `ON`に更新されます。
    -   設定を`tidb_restricted_read_only`から`OFF`にしても、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)変更されません。
    -   `tidb_restricted_read_only`が`ON`の場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) `OFF`に設定することはできません。
-   TiDB の DBaaS プロバイダーの場合、TiDB クラスタが別のデータベースのダウンストリーム データベースである場合、TiDB クラスタを読み取り専用にするには、 [Security強化モード](#tidb_enable_enhanced_security)を有効にした状態で`tidb_restricted_read_only`使用する必要がある場合があります。これにより、顧客が[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)使用してクラスタを書き込み可能にすることができなくなります。これを実現するには、 [Security強化モード](#tidb_enable_enhanced_security)を有効にし、 `SYSTEM_VARIABLES_ADMIN`および`RESTRICTED_VARIABLES_ADMIN`権限を持つ管理者ユーザーを使用して`tidb_restricted_read_only`制御し、データベース ユーザーが`SUPER`権限を持つルート ユーザーを使用して[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを制御できるようにする必要があります。
-   この変数は、クラスタ全体の読み取り専用状態を制御します。変数が`ON`の場合、クラスタ内のすべての TiDB サーバーが読み取り専用モードになります。この場合、TiDB は`SHOW` `SELECT`のようにデータを変更しないステートメントのみを実行します。9 や`USE` `INSERT`の他のステートメントについては、TiDB は読み取り専用モードで`UPDATE`実行を拒否します。
-   この変数を使用して読み取り専用モードを有効にしても、最終的にクラスタ全体が読み取り専用状態になることが保証されるだけです。TiDBクラスタでこの変数の値を変更しても、その変更が他のTiDBサーバーにまだ反映されていない場合、更新されていないTiDBサーバーは読み取り専用モードになり**ません**。
-   TiDB は、SQL ステートメントの実行前に読み取り専用フラグを確認します。v6.2.0 以降では、SQL ステートメントのコミット前にもフラグがチェックされます。これにより、サーバーが読み取り専用モードになった後に、長時間実行される[自動コミット](/transaction-overview.md#autocommit)ステートメントがデータを変更するケースを防ぐことができます。
-   この変数が有効になっている場合、TiDB はコミットされていないトランザクションを次のように処理します。
    -   コミットされていない読み取り専用トランザクションについては、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではない未コミットのトランザクションの場合、これらのトランザクション内で書き込み操作を実行するSQL文は拒否されます。
    -   データが変更された未コミットの読み取り専用トランザクションについては、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードが有効になると、明示的に権限`RESTRICTED_REPLICA_WRITER_ADMIN`が付与されない限り、すべてのユーザー（権限`SUPER`を持つユーザーを含む）はデータを書き込む可能性のあるSQLステートメントを実行できなくなります。

### tidb_request_source_type <span class="version-mark">v7.4.0で追加</span> {#tidb-request-source-type-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: `""`
-   `"stats"` `"lightning"` `"background"` `"br"` `"ddl"`
-   この変数は[リソース制御](/tidb-resource-control-ru-groups.md)現在のセッションのタスクタイプを明示的に指定するために使用され、それは によって識別および制御されます。例: `SET @@tidb_request_source_type = "background"` 。

### tidb_resource_control_strict_mode は<span class="version-mark">v8.2.0 で追加されました。</span> {#tidb-resource-control-strict-mode-span-class-version-mark-new-in-v8-2-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)ステートメントおよび[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザヒントに権限制御を適用するかどうかを制御します。このシステム変数が`ON`に設定されている場合、現在のセッションまたは現在のステートメントのバインドされたリソース グループをこれらの 2 つの方法で変更するには、権限`SUPER` 、または`RESOURCE_GROUP_ADMIN` `RESOURCE_GROUP_USER`必要です`OFF`に設定されている場合、これらの権限は不要となり、この変数がない以前の TiDB バージョンと同じ動作になります。
-   TiDBクラスタを以前のバージョンからv8.2.0以降にアップグレードすると、この変数のデフォルト値は`OFF`に設定され、この機能はデフォルトで無効になります。

### tidb_retry_limit {#tidb-retry-limit}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `10`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、楽観的トランザクションの再試行回数の最大値を設定するために使用されます。トランザクションが再試行可能なエラー（トランザクションの競合、トランザクションのコミットが非常に遅い、テーブルスキーマの変更など）に遭遇した場合、この変数に基づいてトランザクションが再実行されます。1～ `0` `tidb_retry_limit`設定すると、自動再試行が無効になることに注意してください。この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。

### tidb_row_format_version {#tidb-row-format-version}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   テーブルに新しく保存されたデータの形式バージョンを制御します。 TiDB v4.0 では、新しいデータの保存にデフォルトで[新しいstorage行フォーマット](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2018-07-19-row-format.md)バージョン`2`が使用されます。
-   TiDB のバージョンが v4.0.0 より前のバージョンから v4.0.0 以降のバージョンにアップグレードした場合、フォーマット バージョンは変更されず、TiDB は引き続きバージョン`1`の古いフォーマットを使用してテーブルにデータを書き込みます。つまり**、新しく作成されたクラスタのみがデフォルトで新しいデータ フォーマットを使用します**。
-   この変数を変更しても、既に保存されている古いデータには影響しませんが、この変数を変更した後に新たに書き込まれるデータにのみ、対応するバージョン形式が適用されます。

### tidb_runtime_filter_mode <span class="version-mark">v7.2.0で追加</span> {#tidb-runtime-filter-mode-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: 列挙型
-   デフォルト値: `OFF`
-   可能な`LOCAL` : `OFF`
-   ランタイム フィルターのモード、つまり**フィルター送信者オペレーター**と**フィルター受信者オペレーター**間の関係を制御します。 `OFF`と`LOCAL` 2 つのモードがあります。 `OFF` 、ランタイム フィルターを無効にすることを意味します。 `LOCAL` 、ローカル モードでランタイム フィルターを有効にすることを意味します。詳細については、[ランタイムフィルタモード](/runtime-filter.md#runtime-filter-mode)を参照してください。

### tidb_runtime_filter_type <span class="version-mark">v7.2.0で追加</span> {#tidb-runtime-filter-type-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: 列挙型
-   デフォルト値: `IN`
-   可能な値: `IN`
-   生成されたフィルター演算子によって使用される述語のタイプを制御します。現在、1 つのタイプのみがサポートされています: `IN` 。詳細については、[ランタイムフィルタタイプ](/runtime-filter.md#runtime-filter-type)を参照してください。

### tidb_scatter_region {#tidb-scatter-region}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `""`
-   `table` `global`値： `""`
-   テーブル作成時にパラメータ`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`設定されている場合、システムはテーブルの作成が成功すると、自動的に指定された数のリージョンに分割します。この変数は、分割されたリージョンの分散戦略を制御します。TiDB は、選択された分散戦略に基づいてリージョンを処理します。テーブル作成操作は、成功ステータスを返す前に分散処理が完了するまで待機するため、この変数を有効にすると、ステートメント`CREATE TABLE`の実行時間が大幅に増加する可能性があることに注意してください。この変数が無効になっている場合と比較すると、実行時間は数倍長くなる可能性があります。可能な値の説明は次のとおりです。
    -   `""` ：デフォルト値。テーブル作成後、テーブルの領域が分散されないことを示します。
    -   `table` ：テーブル作成時に属性`PRE_SPLIT_REGIONS`または`SHARD_ROW_ID_BITS`を設定した場合、複数のリージョンを事前に分割するシナリオでは、これらのテーブルのリージョンはテーブルの粒度に応じて分散されます。ただし、テーブル作成時に上記の属性を設定しない場合、多数のテーブルを迅速に作成するシナリオでは、これらのテーブルのリージョンが少数のTiKVノードに集中し、リージョンの分布が不均一になります。
    -   `global` ：TiDBは、新しく作成されたテーブルのリージョンをクラスタ全体のデータ分布に従って分散します。特に、多数のテーブルを迅速に作成する場合、 `global`オプションを使用すると、リージョンが少数のTiKVノードに過度に集中するのを防ぎ、クラスタ全体にリージョンがよりバランスよく分散されるようにすることができます。

### tidb_schema_cache_size <span class="version-mark">v8.0.0で追加</span> {#tidb-schema-cache-size-span-class-version-mark-new-in-v8-0-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値： `536870912` （512 MiB）
-   範囲： `0`または`[67108864, 9223372036854775807]`
-   TiDB v8.4.0 より前のバージョンでは、この変数のデフォルト値は`0`です。
-   TiDB v8.4.0以降では、デフォルト値は`536870912`です。以前のバージョンからv8.4.0以降にアップグレードする場合、以前のバージョンで設定されていた値が使用されます。
-   この変数は、TiDB のスキーマ キャッシュのサイズを制御します。単位はバイトです。この変数を`0`に設定すると、キャッシュ制限機能が無効になります。この機能を有効にするには、 `[67108864, 9223372036854775807]`範囲内の値を設定する必要があります。TiDB はこの値を最大使用可能メモリ制限として使用し、LRU (Least Recently Used、最近使用頻度の低いもの）アルゴリズムを適用して必要なテーブルをキャッシュすることで、スキーマ情報によって使用されるメモリを効果的に削減します。
-   クラスターに多数のパーティションテーブルが含まれている場合、またはパーティションテーブルに対して DDL 操作を頻繁に実行する場合 ( `TRUNCATE`や`DROP PARTITION`など)、この変数を`0`に設定することをお勧めします。

### tidb_schema_version_cache_limit <span class="version-mark">v7.4.0で追加</span> {#tidb-schema-version-cache-limit-span-class-version-mark-new-in-v7-4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `16`
-   範囲: `[2, 255]`
-   この変数は、TiDBインスタンスにキャッシュできる履歴スキーマバージョンの数を制限します。デフォルト値は`16`で、これはTiDBがデフォルトで16個の履歴スキーマバージョンをキャッシュすることを意味します。
-   通常、この変数を変更する必要はありません。[ステイル読み取り](/stale-read.md)機能を使用し、DDL操作が非常に頻繁に実行されると、スキーマバージョンが頻繁に変更されます。その結果、ステイル読み取りがスナップショットからスキーマ情報を取得しようとすると、スキーマキャッシュミスにより情報の再構築に時間がかかる場合があります。この場合、スキーマキャッシュミスの問題を回避するために、 `tidb_schema_version_cache_limit`の値を増やす（例えば`32`する）ことができます。
-   この変数を変更すると、TiDBのメモリ使用量がわずかに増加します。メモリ不足の問題を回避するため、TiDBのメモリ使用量を監視してください。

### tidb_server_memory_limit <span class="version-mark">v6.4.0で追加</span> {#tidb-server-memory-limit-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `80%`
-   範囲：
    -   値をパーセンテージ形式で設定できます。これは、メモリ使用量が総メモリに対して占める割合を意味します。値の範囲は`[1%, 99%]`です。
    -   メモリサイズの値も設定できます。値の範囲は`0` ～ `[536870912, 9223372036854775807]`バイトです。「KiB|MiB|GiB|TiB」単位のメモリ形式がサポートされています。5 `0`メモリ制限なしを意味します。
    -   この変数に512 MiB未満で`0`以外のメモリサイズが設定されている場合、TiDBは実際のサイズとして512 MiBを使用します。
-   この変数は、TiDBインスタンスのメモリ制限を指定します。TiDBのメモリ使用量がこの制限に達すると、TiDBは現在実行中のSQL文のうち、最もメモリ使用量の多い文をキャンセルします。SQL文が正常にキャンセルされた後、TiDBはGolangのガベージコレクション（GC）を呼び出してメモリを解放し、メモリ負荷をできるだけ早く軽減しようとします。
-   [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)の制限を超えるメモリ使用量を持つ SQL ステートメントのみが、最初にキャンセルされる SQL ステートメントとして選択されます。
-   現在、TiDBは一度に1つのSQL文のみをキャンセルします。TiDBがSQL文を完全にキャンセルしてリソースを解放した後も、メモリ使用量がこの変数で設定された制限を超えている場合、TiDBは次のキャンセル操作を開始します。

### tidb_server_memory_limit_gc_trigger は<span class="version-mark">v6.4.0 で追加されました。</span> {#tidb-server-memory-limit-gc-trigger-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `70%`
-   範囲: `[50%, 99%]`
-   TiDBがGCをトリガーしようとするしきい値。TiDBのメモリ使用量が`tidb_server_memory_limit` × `tidb_server_memory_limit_gc_trigger`の値に達すると、TiDBはGolangのGC操作を積極的にトリガーします。1分間にトリガーされるGC操作は1回のみです。

### tidb_server_memory_limit_sess_min_size<span class="version-mark">は v6.4.0 で追加されました。</span> {#tidb-server-memory-limit-sess-min-size-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値： `134217728` （128MiB）
-   範囲： `[128, 9223372036854775807]` （バイト単位）。「KiB|MiB|GiB|TiB」単位のメモリフォーマットもサポートされています。
-   メモリ制限を有効にすると、TiDB は現在のインスタンス上でメモリ使用量が最も高い SQL ステートメントを終了します。この変数は、終了する SQL ステートメントの最小メモリ使用量を指定します。メモリ使用量が低いセッションが多すぎるために TiDB インスタンスのメモリ使用量が制限を超えている場合は、この変数の値を適切に下げることで、より多くのセッションをキャンセルできるようになります。

### tidb_service_scope <span class="version-mark">v7.4.0で追加</span> {#tidb-service-scope-span-class-version-mark-new-in-v7-4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: &quot;&quot;
-   オプションの値: 最大 64 文字の文字列。有効な文字は、数字`0-9` 、文字`a-zA-Z` 、アンダースコア`_` 、ハイフン`-`です。
-   この変数はインスタンスレベルのシステム変数です。これを使用して[TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)の下で各 TiDB ノードのサービス スコープを制御できます。 DXF は、この変数の値に基づいて、どの TiDB ノードが分散タスクを実行するようにスケジュールできるかを決定します。特定のルールについては、 [タスクスケジューリング](/tidb-distributed-execution-framework.md#task-scheduling)を参照してください。

### tidb_session_alias <span class="version-mark">v7.4.0で追加</span> {#tidb-session-alias-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション
-   クラスターに保持される: いいえ
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: &quot;&quot;
-   この変数を使用すると、現在のセッションに関連するログの`session_alias`列の値をカスタマイズできます。これにより、トラブルシューティング時にセッションを特定しやすくなります。この設定は、ステートメントの実行に関与する複数のノード (TiKV を含む) のログに影響します。この変数の最大長は 64 文字に制限されており、それを超える文字は自動的に切り捨てられます。値の末尾のスペースも自動的に削除されます。

### tidb_session_plan_cache_size <span class="version-mark">v7.1.0で追加</span> {#tidb-session-plan-cache-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は、キャッシュできるプランの最大数を制御します。[準備済みプランキャッシュ](/sql-prepared-plan-cache.md)[準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)は同じキャッシュを共有します。
-   以前のバージョンからv7.1.0以降のバージョンにアップグレードした場合、この変数は[`tidb_prepared_plan_cache_size`](#tidb_prepared_plan_cache_size-new-in-v610)と同じ値のままです。

### tidb_shard_allocate_step <span class="version-mark">v5.0で追加</span> {#tidb-shard-allocate-step-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `9223372036854775807`
-   範囲: `[1, 9223372036854775807]`
-   この変数は、 [`AUTO_RANDOM`](/auto-random.md)または[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)属性に割り当てられる連続IDの最大数を制御します。通常、1つのトランザクション内では、 `AUTO_RANDOM` IDまたは`SHARD_ROW_ID_BITS`注釈付き行IDが連続して増分されます。この変数を使用すると、大規模なトランザクションシナリオにおけるホットスポットの問題を解決できます。

### tidb_shard_row_id_bits <span class="version-mark">v8.4.0で追加</span> {#tidb-shard-row-id-bits-span-class-version-mark-new-in-v8-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数は、新しく作成されるテーブルのデフォルトの行 ID シャード数を設定するために使用されます。この変数にゼロ以外の値を設定すると、TiDB は`CREATE TABLE`ステートメントを実行する際に`SHARD_ROW_ID_BITS`の使用を許可するテーブル (たとえば、 `NONCLUSTERED`テーブル) にこの属性を自動的に適用します。詳細については、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)参照してください。

### tidb_simplified_metrics {#tidb-simplified-metrics}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数が有効になっている場合、TiDB は Grafana パネルで使用されていないメトリックを収集または記録しません。

### tidb_skip_ascii_check <span class="version-mark">v5.0で追加</span> {#tidb-skip-ascii-check-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ASCII検証をスキップするかどうかを設定するために使用されます。
-   ASCII文字の検証はパフォーマンスに影響します。入力文字が有効なASCII文字であることが確実な場合は、変数の値を`ON`に設定できます。

### tidb_skip_isolation_level_check {#tidb-skip-isolation-level-check}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   このスイッチを有効にした後、TiDBでサポートされていない分離レベルが`tx_isolation`に割り当てられた場合でも、エラーは報告されません。これにより、異なる分離レベルを設定する（ただし、それに依存しない）アプリケーションとの互換性が向上します。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_missing_partition_stats は<span class="version-mark">v7.3.0 で追加されました。</span> {#tidb-skip-missing-partition-stats-span-class-version-mark-new-in-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   パーティション [動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)でパーティションテーブルにアクセスする場合、TiDB は各パーティションの統計情報を集約してグローバル統計情報を生成します。この変数は、パーティション統計情報が欠落している場合にグローバル統計情報を生成するかどうかを制御します。

    -   この変数が`ON`場合、TiDB はグローバル統計を生成する際に不足しているパーティション統計をスキップするため、グローバル統計の生成には影響しません。
    -   この変数が`OFF`場合、TiDB は欠落しているパーティション統計を検出すると、グローバル統計の生成を停止します。

### tidb_skip_utf8_check {#tidb-skip-utf8-check}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、UTF-8検証をスキップするかどうかを設定するために使用されます。
-   UTF-8文字の検証はパフォーマンスに影響します。入力文字が有効なUTF-8文字であることが確実な場合は、変数の値を`ON`に設定してください。

> **注記：**
>
> 文字チェックをスキップすると、TiDB はアプリケーションによって書き込まれた無効な UTF-8 文字を検出できず、 `ANALYZE`実行時にデコードエラーが発生したり、その他の未知のエンコードの問題を引き起こしたりする可能性があります。アプリケーションが書き込まれた文字列の有効性を保証できない場合は、文字チェックをスキップすることはお勧めしません。

### tidb_slow_log_threshold {#tidb-slow-log-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスタに永続化しますか？：いいえ、現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `300`
-   範囲: `[-1, 9223372036854775807]`
-   単位：ミリ秒
-   この変数は、スローログの処理時間のしきい値を出力します。デフォルト値は300ミリ秒です。クエリの処理時間がこの値を超えると、そのクエリはスロークエリとみなされ、そのログがスロークエリログに出力されます。なお、 [`log.level`](https://docs.pingcap.com/tidb/dev/tidb-configuration-file#level)の出力レベルが`"debug"`場合、この変数の設定に関わらず、すべてのクエリがスロークエリログに記録されます。

### tidb_slow_query_file {#tidb-slow-query-file}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   `INFORMATION_SCHEMA.SLOW_QUERY`が照会された場合、設定ファイルで`slow-query-file`によって設定されたスロークエリログ名のみが解析されます。デフォルトのスロークエリログ名は「tidb-slow.log」です。他のログを解析するには、 `tidb_slow_query_file`セッション変数に特定のファイルパスを設定し、 `INFORMATION_SCHEMA.SLOW_QUERY`照会して、設定したファイルパスに基づいてスロークエリログを解析します。

<CustomContent platform="tidb">

詳細については、[遅いクエリを特定する](/identify-slow-queries.md)参照してください。

</CustomContent>

### tidb_slow_txn_log_threshold は<span class="version-mark">v7.0.0 で追加されました。</span> {#tidb-slow-txn-log-threshold-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 符号なし整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   単位：ミリ秒
-   この変数は、低速トランザクションのログ記録のしきい値を設定します。トランザクションの実行時間がこのしきい値を超えると、TiDB はトランザクションに関する詳細情報をログに記録します。値が`0`に設定されている場合、この機能は無効になります。

### tidb_snapshot {#tidb-snapshot}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   この変数は、セッションがデータを読み取る時点を設定するために使用されます。たとえば、変数を「2017-11-11 20:20:20」または「400036290571534337」のようなTSO番号に設定すると、現在のセッションはこの時点のデータを読み取ります。

### tidb_source_id <span class="version-mark">v6.5.0で追加</span> {#tidb-source-id-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲: `[1, 15]`

<CustomContent platform="tidb">

-   この変数は、 [双方向複製](/ticdc/ticdc-bidirectional-replication.md)クラスター内のさまざまなクラスター ID を構成するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [双方向複製](https://docs.pingcap.com/tidb/stable/ticdc-bidirectional-replication)クラスター内のさまざまなクラスター ID を構成するために使用されます。

</CustomContent>

### tidb_stats_cache_mem_quota <span class="version-mark">（v6.1.0で追加）</span> {#tidb-stats-cache-mem-quota-span-class-version-mark-new-in-v6-1-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   単位：バイト
-   デフォルト値は`0` 、これは TiDB 統計キャッシュのメモリ割り当てが TiDB インスタンスの総メモリの 20% であることを意味します。v8.5.1 より前のバージョンでは、 `0`メモリ割り当てが TiDB インスタンスの総メモリの 50% であることを意味します。
-   範囲: `[0, 1099511627776]`
-   この変数は、TiDB統計キャッシュのメモリ割り当て量を設定します。

### tidb_stats_load_pseudo_timeout <span class="version-mark">v5.4.0で追加</span> {#tidb-stats-load-pseudo-timeout-span-class-version-mark-new-in-v5-4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、SQL最適化の待機時間がタイムアウトに達し、完全な列統計情報を同期的にロードする際のTiDBの動作を制御します。デフォルト値の`ON`は、タイムアウト後にSQL最適化が擬似統計情報を使用する状態に戻ることを意味します。この変数を`OFF`に設定すると、タイムアウト後にSQL実行が失敗します。

### tidb_stats_load_sync_wait <span class="version-mark">v5.4.0で追加</span> {#tidb-stats-load-sync-wait-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   単位：ミリ秒
-   この変数は、同期的に統計情報を読み込む機能を有効にするかどうかを制御します。値`0`は、この機能が無効であることを意味します。この機能を有効にするには、この変数に、SQL 最適化が列統計情報を完全に同期的に読み込むために待機できる最大時間 (ミリ秒単位) を設定します。詳細については、[負荷統計](/statistics.md#load-statistics)参照してください。

### tidb_stmt_summary_enable_persistent <span class="version-mark">v6.6.0で追加</span> {#tidb-stmt-summary-enable-persistent-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   対象範囲：グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)を有効にするかどうかを制御します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_filename <span class="version-mark">v6.6.0で追加</span> {#tidb-stmt-summary-filename-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   対象範囲：グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 文字列
-   デフォルト値: `"tidb-statements.log"`
-   この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に永続データが書き込まれるファイルを指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_backups <span class="version-mark">v6.6.0で追加</span> {#tidb-stmt-summary-file-max-backups-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   対象範囲：グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に保存できるデータ ファイルの最大数を指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_days<span class="version-mark">は v6.6.0 で追加されました。</span> {#tidb-stmt-summary-file-max-days-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントのサマリー永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   対象範囲：グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `3`
-   単位：日
-   この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合に、永続的なデータ ファイルを保持する最大日数を指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_size は<span class="version-mark">v6.6.0 で追加されました。</span> {#tidb-stmt-summary-file-max-size-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントのサマリー永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

-   対象範囲：グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `64`
-   単位: MiB
-   この変数は読み取り専用です。 [ステートメントの要約持続性](/statement-summary-tables.md#persist-statements-summary)が有効な場合の永続データ ファイルの最大サイズを指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_history_size <span class="version-mark">v4.0で追加</span> {#tidb-stmt-summary-history-size-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `24`
-   範囲: `[0, 255]`
-   この変数は[明細書概要表](/statement-summary-tables.md)の履歴容量を設定するために使用されます。

### tidb_stmt_summary_internal_query <span class="version-mark">v4.0で追加</span> {#tidb-stmt-summary-internal-query-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、[明細書概要表](/statement-summary-tables.md)にTiDBのSQL情報を含めるかどうかを制御するために使用されます。

### tidb_stmt_summary_max_sql_length <span class="version-mark">v4.0で追加</span> {#tidb-stmt-summary-max-sql-length-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `4096`
-   範囲: `[0, 2147483647]`
-   単位：バイト

<CustomContent platform="tidb">

-   この変数は、[明細書概要表](/statement-summary-tables.md)および[TiDBダッシュボード](/dashboard/dashboard-intro.md)の SQL 文字列の長さを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は[明細書概要表](/statement-summary-tables.md)の SQL 文字列の長さを制御するために使用されます。

</CustomContent>

### tidb_stmt_summary_max_stmt_count <span class="version-mark">v4.0で追加</span> {#tidb-stmt-summary-max-stmt-count-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `3000`
-   範囲: `[1, 32767]`
-   この変数は、 [`statements_summary`](/statement-summary-tables.md#statements_summary)と[`statements_summary_history`](/statement-summary-tables.md#statements_summary_history)テーブルがメモリに格納できる SQL ダイジェストの総数を制限するために使用されます。

<CustomContent platform="tidb">

> **注記：**
>
> [`tidb_stmt_summary_enable_persistent`](/statement-summary-tables.md#persist-statements-summary)が有効になっている場合、 `tidb_stmt_summary_max_stmt_count` [`statements_summary`](/statement-summary-tables.md#statements_summary)テーブルがメモリに格納できる SQL ダイジェストの数を制限するだけです。

</CustomContent>

### tidb_stmt_summary_refresh_interval <span class="version-mark">v4.0で追加</span> {#tidb-stmt-summary-refresh-interval-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1800`
-   範囲: `[1, 2147483647]`
-   単位：秒
-   この変数は[明細書概要表](/statement-summary-tables.md)の更新時間を設定するために使用されます。

### tidb_store_batch_size {#tidb-store-batch-size}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `4`
-   範囲: `[0, 25000]`
-   この変数は、 `IndexLookUp`オペレータのコプロセッサータスクのバッチ サイズを制御するために使用されます。3 `0`バッチを無効にすることを意味します。タスク数が比較的多く、クエリの処理が遅い場合は、この変数を増やすことでクエリを最適化できます。

### tidb_store_limit は<span class="version-mark">v3.0.4 および v4.0 で追加されました。</span> {#tidb-store-limit-span-class-version-mark-new-in-v3-0-4-and-v4-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、TiDBが同時にTiKVに送信できるリクエストの最大数を制限するために使用されます。0は制限なしを意味します。

### tidb_streamagg_concurrency {#tidb-streamagg-concurrency}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   この変数は、クエリ実行時の`StreamAgg`演算子の同時実行数を設定します。
-   この変数を設定することは**推奨されません**。変数の値を変更すると、データの正確性に問題が生じる可能性があります。

### tidb_super_read_only <span class="version-mark">v5.3.1で追加</span> {#tidb-super-read-only-span-class-version-mark-new-in-v5-3-1-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_super_read_only` MySQL 変数`super_read_only`の代替として実装されることを目指しています。ただし、TiDB は分散データベースであるため、 `tidb_super_read_only`実行直後にデータベースを読み取り専用にするのではなく、最終的には読み取り専用にします。
-   権限レベル`SUPER`または`SYSTEM_VARIABLES_ADMIN`のユーザーは、この変数を変更できます。
-   この変数は、クラスタ全体の読み取り専用状態を制御します。変数が`ON`の場合、クラスタ内のすべての TiDB サーバーが読み取り専用モードになります。この場合、TiDB は`SHOW` `SELECT`のようにデータを変更しないステートメントのみを実行します。9 や`USE` `INSERT`の他のステートメントについては、TiDB は読み取り専用モードでの実行`UPDATE`拒否します。
-   この変数を使用して読み取り専用モードを有効にしても、最終的にクラスタ全体が読み取り専用状態になることが保証されるだけです。TiDBクラスタでこの変数の値を変更しても、その変更が他のTiDBサーバーにまだ反映されていない場合、更新されていないTiDBサーバーは読み取り専用モードになり**ません**。
-   TiDB は、SQL ステートメントの実行前に読み取り専用フラグを確認します。v6.2.0 以降では、SQL ステートメントのコミット前にもフラグがチェックされます。これにより、サーバーが読み取り専用モードになった後に、長時間実行される[自動コミット](/transaction-overview.md#autocommit)ステートメントがデータを変更するケースを防ぐことができます。
-   この変数が有効になっている場合、TiDB はコミットされていないトランザクションを次のように処理します。
    -   コミットされていない読み取り専用トランザクションについては、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではない未コミットのトランザクションの場合、これらのトランザクション内で書き込み操作を実行するSQL文は拒否されます。
    -   データが変更された未コミットの読み取り専用トランザクションについては、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードが有効になると、明示的に権限`RESTRICTED_REPLICA_WRITER_ADMIN`が付与されない限り、すべてのユーザー（権限`SUPER`を持つユーザーを含む）はデータを書き込む可能性のあるSQLステートメントを実行できなくなります。
-   [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)システム変数が`ON`に設定されている場合、場合によっては`tidb_super_read_only` [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の影響を受けます。詳細な影響については、 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の説明を参照してください。

### tidb_sysdate_is_now は<span class="version-mark">v6.0.0 で追加されました。</span> {#tidb-sysdate-is-now-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、関数`SYSDATE`関数`NOW`に置き換えることができるかどうかを制御するために使用されます。この設定項目は、MySQLオプションの[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果を持ちます。

### tidb_sysproc_scan_concurrency <span class="version-mark">v6.5.0で追加</span> {#tidb-sysproc-scan-concurrency-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲： `[0, 4294967295]`以前のバージョンの最大値は`256`です。v8.2.0より前のバージョンでは、最小値は`1`です`0`に設定すると、クラスタサイズに基づいて同時実行数が適応的に調整されます。
-   この変数は、TiDBが内部SQLステートメント（統計情報の自動更新など）を実行する際に実行されるスキャン操作の同時実行数を設定するために使用されます。

### tidb_table_cache_lease <span class="version-mark">v6.0.0で追加</span> {#tidb-table-cache-lease-span-class-version-mark-new-in-v6-0-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `3`
-   範囲: `[1, 10]`
-   単位：秒
-   この変数は、キャッシュ[キャッシュされたテーブル](/cached-tables.md)テーブルのリース時間を制御するために使用され、デフォルト値は`3`です。この変数の値は、キャッシュされたテーブルの変更に影響します。キャッシュされたテーブルが変更された後、最長の待機時間は`tidb_table_cache_lease`秒になる場合があります。テーブルが読み取り専用であるか、高い書き込みレイテンシーを許容できる場合は、この変数の値を増やすことで、キャッシュされたテーブルの有効時間を長くし、リース更新の頻度を減らすことができます。

### tidb_tmp_table_max_size は<span class="version-mark">v5.3.0 で追加されました。</span> {#tidb-tmp-table-max-size-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `67108864`
-   範囲: `[1048576, 137438953472]`
-   単位：バイト
-   この変数は、単一[一時テーブル](/temporary-tables.md)の最大サイズを設定するために使用されます。この変数の値よりも大きいサイズの一時テーブルはエラーになります。

### tidb_top_sql_max_meta_count は<span class="version-mark">v6.0.0 で追加されました。</span> {#tidb-top-sql-max-meta-count-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `5000`
-   範囲: `[1, 10000]`

<CustomContent platform="tidb">

-   この変数は、 [Top SQL](/dashboard/top-sql.md)が1分あたりに収集するSQLステートメントタイプの最大数を制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)が1分あたりに収集するSQLステートメントタイプの最大数を制御するために使用されます。

</CustomContent>

### tidb_top_sql_max_time_series_count は<span class="version-mark">v6.0.0 で追加されました。</span> {#tidb-top-sql-max-time-series-count-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

> **注記：**
>
> 現在、TiDBダッシュボードのTop SQLページには、負荷に最も寄与する上位5種類のSQLクエリのみが表示されますが、これは`tidb_top_sql_max_time_series_count`の設定とは無関係です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `100`
-   範囲: `[1, 5000]`

<CustomContent platform="tidb">

-   この変数は、負荷に最も大きく寄与するSQLステートメント（つまり、上位N個）を、1分あたり[Top SQL](/dashboard/top-sql.md)で記録する数を制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、負荷に最も大きく寄与するSQLステートメント（つまり、上位N個）を、1分あたり[Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)で記録する数を制御するために使用されます。

</CustomContent>

### tidb_track_aggregate_memory_usage {#tidb-track-aggregate-memory-usage}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB が集計関数のメモリ使用量を追跡するかどうかを制御します。

> **警告：**
>
> この変数を無効にすると、TiDB はメモリ使用量を正確に追跡できず、対応する SQL ステートメントのメモリ使用量を制御できなくなる可能性があります。

### tidb_tso_client_batch_max_wait_time は<span class="version-mark">v5.3.0 で追加されました。</span> {#tidb-tso-client-batch-max-wait-time-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 10]`
-   単位：ミリ秒
-   この変数は、TiDBがPDからTSOを要求する際のバッチ操作の最大待機時間を設定するために使用されます。デフォルト値は`0`で、これは追加の待機時間がないことを意味します。
-   TiDBで使用されるPDクライアントは、PDからTSOリクエストを取得する際、同時に受信したTSOリクエストを可能な限り多く収集します。そして、収集したリクエストをバッチ処理で1つのRPCリクエストに統合し、PDに送信します。これにより、PDへの負荷を軽減できます。
-   この変数を`0`より大きい値に設定すると、TiDBは各バッチマージの終了前に、この値の最大期間待機します。これは、より多くのTSOリクエストを収集し、バッチ処理の効果を向上させるためです。
-   この変数の値を増加させるシナリオ：
    -   TSOリクエストの負荷が高いため、PDリーダーのCPUがボトルネックとなり、TSO RPCリクエストのレイテンシーが増大する。
    -   クラスター内にはTiDBインスタンスは多くありませんが、すべてのTiDBインスタンスが高い同時実行性で動作しています。
-   この変数はできるだけ小さい値に設定することをお勧めします。

> **注記：**
>
> -   TSO RPCのレイテンシーが、PDリーダーのCPU使用率のボトルネック以外の理由（ネットワークの問題など）で増加するとします。この場合、 `tidb_tso_client_batch_max_wait_time`の値を増やすと、TiDBの実行レイテンシーが増加し、クラスタのQPSパフォーマンスに影響を与える可能性があります。
> -   この機能は[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)と互換性がありません。この変数にゼロ以外の値を設定すると、[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)有効になりません。

### tidb_tso_client_rpc_mode <span class="version-mark">v8.4.0で追加</span> {#tidb-tso-client-rpc-mode-span-class-version-mark-new-in-v8-4-0-span}

-   対象範囲：グローバル

-   クラスターに保持される: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ

-   タイプ: 列挙型

-   デフォルト値: `DEFAULT`

-   `PARALLEL-FAST` `PARALLEL` ： `DEFAULT`

-   この変数は、TiDB が TSO RPC リクエストを PD に送信するモードを切り替えます。このモードによって、TSO RPC リクエストが並列処理されるかどうかが決まり、各 TS 取得操作のバッチ待機時間に影響します。これにより、特定のシナリオにおいて、クエリ実行中の TS 取得の待機時間を短縮できます。

    -   `DEFAULT` : TiDBは、特定の期間にわたるTS取得操作を単一のTSO RPCリクエストに集約し、バッチ処理でPDに送信してタイムスタンプを取得します。そのため、各TS取得操作の所要時間は、バッチ処理待ち時間とRPC実行時間で構成されます。2 `DEFAULT`では、異なるTSO RPCリクエストが直列に処理され、各TS取得操作の平均所要時間は、TSO RPCリクエストの実際の処理時間の約1.5倍になります。
    -   `PARALLEL` ：このモードでは、TiDBは各バッチの収集時間を`DEFAULT`モードの半分に短縮し、同時に2つのTSO RPCリクエストを維持しようとします。このようにして、各TS取得操作の平均時間は理論的にはTSO RPC時間の約1.25倍に短縮でき、これは`DEFAULT`モードの時間コストの約83%に相当します。ただし、バッチ処理の効果は低下し、TSO RPCリクエストの数は`DEFAULT`モードの約2倍に増加します。
    -   `PARALLEL-FAST` ： `PARALLEL`モードと同様に、このモードでは、TiDBは各バッチの収集時間を`DEFAULT`モードの4分の1に短縮し、同時に4つのTSO RPCリクエストを維持しようとします。このようにして、各TS取得操作の平均時間は理論的にはTSO RPC時間の約1.125倍に短縮でき、これは`DEFAULT`モードの時間コストの約75%に相当します。ただし、バッチ処理の効果はさらに低下し、TSO RPCリクエストの数は`DEFAULT`モードの約4倍に増加します。

-   以下の条件を満たす場合、パフォーマンス向上の可能性を考慮して、この変数を`PARALLEL`または`PARALLEL-FAST`に切り替えることを検討してください。

    -   TSOの待機時間は、SQLクエリの総実行時間の大部分を占める。
    -   PDにおけるTSOの割り当ては、まだボトルネックに達していません。
    -   PDノードとTiDBノードは十分なCPUリソースを備えている。
    -   TiDBとPD間のネットワークレイテンシーは、PDがTSOを割り当てるのにかかる時間よりもかなり長い（つまり、TSO RPCの実行時間の大部分はネットワークレイテンシーによるものである）。
        -   TSO RPCリクエストの所要時間を取得するには、Grafana TiDBダッシュボードのPDクライアントセクションにある**PD TSO RPC所要時間**パネルを確認してください。
        -   PD TSO割り当ての期間を確認するには、Grafana PDダッシュボードのTiDBセクションにある**PDサーバーTSOハンドル期間**パネルを確認してください。
    -   TiDBとPD間のTSO RPCリクエストの増加（ `PARALLEL`の場合は2倍、 `PARALLEL-FAST`の場合は4倍）によって生じる追加のネットワークトラフィックは許容範囲内です。

> **注記：**
>
> -   モード`PARALLEL`とモード`PARALLEL-FAST`は、 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)および[`tidb_enable_tso_follower_proxy`](#tidb_enable_tso_follower_proxy-new-in-v530)と互換性がありません。tidb_tso_client_batch_max_wait_time [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)ゼロ以外の値に設定されている場合、または[`tidb_enable_tso_follower_proxy`](#tidb_enable_tso_follower_proxy-new-in-v530)が有効になっている場合、モード`tidb_tso_client_rpc_mode`の設定は有効にならず、TiDBは常にモード`DEFAULT`で動作します。
> -   `PARALLEL`と`PARALLEL-FAST`モードは、TiDBにおけるTSの取得にかかる平均時間を短縮するように設計されています。ただし、レイテンシーの変動が大きい場合（例えば、テールレイテンシーが長い場合やレイテンシーに上昇する場合など）は、これらの2つのモードでは顕著なパフォーマンス向上は得られない可能性があります。

### tidb_cb_pd_metadata_error_rate_threshold_ratio<span class="version-mark">は v8.5.5 で追加されました。</span> {#tidb-cb-pd-metadata-error-rate-threshold-ratio-span-class-version-mark-new-in-v8-5-5-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、TiDBがサーキットブレーカーをトリガーするタイミングを制御します。値を`0` （デフォルト）に設定すると、サーキットブレーカーは無効になります。3～ `0.01` `1`値を設定すると有効になり、PDに送信される特定のリクエストのエラー率がしきい値に達するか超えた場合にサーキットブレーカーがトリガーされます。

### tidb_ttl_delete_rate_limit は<span class="version-mark">v6.5.0 で追加されました。</span> {#tidb-ttl-delete-rate-limit-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、各 TiDB ノード上の TTL ジョブにおける`DELETE`ステートメントの実行速度を制限するために使用されます。この値は、TTL ジョブ内の単一ノードで 1 秒あたりに許可される最大`DELETE`ステートメント数を表します。この変数を`0`に設定すると、制限は適用されません。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_ttl_delete_batch_size は<span class="version-mark">v6.5.0 で追加されました。</span> {#tidb-ttl-delete-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `100`
-   範囲: `[1, 10240]`
-   この変数は、TTL ジョブの`DELETE`つのトランザクションで削除できる最大行数を設定するために使用されます。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_ttl_delete_worker_count は<span class="version-mark">v6.5.0 で追加されました。</span> {#tidb-ttl-delete-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各 TiDB ノードでの TTL ジョブの最大同時実行数を設定するために使用されます。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_ttl_job_enable <span class="version-mark">v6.5.0で追加</span> {#tidb-ttl-job-enable-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、TTL ジョブを有効にするかどうかを制御するために使用されます。これを`OFF`に設定すると、TTL 属性を持つすべてのテーブルが期限切れデータのクリーンアップを自動的に停止します。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_ttl_scan_batch_size は<span class="version-mark">v6.5.0 で追加されました。</span> {#tidb-ttl-scan-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `500`
-   範囲: `[1, 10240]`
-   この変数は、TTL ジョブで期限切れデータをスキャンするために使用される各`SELECT`ステートメントの`LIMIT`値を設定するために使用されます。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_ttl_scan_worker_count は<span class="version-mark">v6.5.0 で追加されました。</span> {#tidb-ttl-scan-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各 TiDB ノードでの TTL スキャン ジョブの最大同時実行数を設定するために使用されます。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_ttl_job_schedule_window_start_time は<span class="version-mark">v6.5.0 で追加されました。</span> {#tidb-ttl-job-schedule-window-start-time-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 時間
-   クラスターに保持される: はい
-   デフォルト値: `00:00 +0000`
-   この変数は、バックグラウンドで実行されるTTLジョブのスケジューリングウィンドウの開始時刻を制御するために使用されます。この変数の値を変更する際は、ウィンドウが小さすぎると期限切れデータのクリーンアップが失敗する可能性があるため注意してください。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_ttl_job_schedule_window_end_time は<span class="version-mark">v6.5.0 で追加されました。</span> {#tidb-ttl-job-schedule-window-end-time-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 時間
-   クラスターに保持される: はい
-   デフォルト値: `23:59 +0000`
-   この変数は、バックグラウンドで実行されるTTLジョブのスケジューリングウィンドウの終了時刻を制御するために使用されます。この変数の値を変更する際は、ウィンドウが小さすぎると期限切れデータのクリーンアップが失敗する可能性があるため注意してください。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_ttl_running_tasks は<span class="version-mark">v7.0.0 で追加されました。</span> {#tidb-ttl-running-tasks-span-class-version-mark-new-in-v7-0-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲： `-1` ～ `[1, 256]`
-   クラスター全体で実行中の TTL タスクの最大数を指定します。 `-1` 、TTL タスクの数が TiKV ノードの数と等しいことを意味します。詳細については、[生きる時が来た](/time-to-live.md)を参照してください。

### tidb_txn_assertion_level <span class="version-mark">v6.0.0で追加</span> {#tidb-txn-assertion-level-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル

-   クラスターに保持される: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ

-   タイプ: 列挙型

-   デフォルト値: `FAST`

-   `FAST` `STRICT`値： `OFF`

-   この変数はアサーション レベルを制御するために使用されます。アサーションは、データとインデックス間の整合性チェックであり、書き込まれるキーがトランザクションのコミット プロセスに存在するかどうかをチェックします。詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。

    -   `OFF` ：このチェックを無効にする。
    -   `FAST` ：ほとんどのチェック項目を有効にしますが、パフォーマンスへの影響はほとんどありません。
    -   `STRICT` ：すべてのチェック項目を有効にします。システム負荷が高い場合、悲観的トランザクションのパフォーマンスにわずかな影響があります。

-   v6.0.0以降のバージョンの新規クラスターの場合、デフォルト値は`FAST`です。v6.0.0より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_txn_commit_batch_size は<span class="version-mark">v6.2.0 で追加されました。</span> {#tidb-txn-commit-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `16384`
-   範囲: `[1, 1073741824]`
-   単位：バイト

<CustomContent platform="tidb">

-   この変数は、TiDB が TiKV に送信するトランザクションコミット要求のバッチサイズを制御するために使用されます。アプリケーションワークロード内のトランザクションの大部分に多数の書き込み操作が含まれている場合、この変数の値を大きくすることでバッチ処理のパフォーマンスを向上させることができます。ただし、この変数を大きすぎる値に設定して TiKV の[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)の制限を超えると、コミットが失敗する可能性があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB が TiKV に送信するトランザクション コミット リクエストのバッチ サイズを制御するために使用されます。アプリケーション ワークロード内のトランザクションの大部分で書き込み操作が多数発生する場合、この変数の値を大きくすることでバッチ処理のパフォーマンスを向上させることができます。ただし、この変数を大きすぎる値に設定して TiKV の単一ログの最大サイズ (デフォルトでは 8 MiB) の制限を超えると、コミットが失敗する可能性があります。

</CustomContent>

### tidb_txn_entry_size_limit は<span class="version-mark">v7.6.0 で追加されました。</span> {#tidb-txn-entry-size-limit-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 125829120]`
-   単位：バイト

<CustomContent platform="tidb">

-   この変数は、TiDB 構成項目[`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)動的に変更するために使用されます。これは、TiDB 内の単一行のデータのサイズを制限し、構成項目 7 と同等です。この変数のデフォルト値は`0`であり、これは TiDB がデフォルトで構成項目`txn-entry-size-limit`の値を使用することを意味します。この変数がゼロ以外の値に設定されている場合、 `txn-entry-size-limit`も同じ値に設定されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB 構成項目[`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)動的に変更するために使用されます。これは、TiDB 内の単一行のデータのサイズを制限し、構成項目 7 と同等です。この変数のデフォルト値は`0`であり、これは TiDB がデフォルトで構成項目`txn-entry-size-limit`の値を使用することを意味します。この変数がゼロ以外の値に設定されている場合、 `txn-entry-size-limit`も同じ値に設定されます。

</CustomContent>

> **注記：**
>
> この変数をSESSIONスコープで変更すると、現在のユーザーセッションのみに影響し、内部TiDBセッションには影響しません。内部TiDBトランザクションのエントリサイズが構成項目の制限を超えると、トランザクションが失敗する可能性があります。したがって、制限を動的に増やすには、変数をGLOBALスコープで変更することをお勧めします。

### tidb_txn_mode {#tidb-txn-mode}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `pessimistic`
-   可能な`optimistic` : `pessimistic`
-   この変数はトランザクション モードを設定するために使用されます。 TiDB 3.0 は悲観的トランザクションをサポートします。 TiDB 3.0.8 以降、[悲観的取引モード](/pessimistic-transaction.md)はデフォルトで有効になっています。
-   TiDBをv3.0.7以前のバージョンからv3.0.8以降のバージョンにアップグレードしても、デフォルトのトランザクションモードは変更されません。**新しく作成されたクラスタのみが、デフォルトで悲観的トランザクションモードを使用します**。
-   この変数が「楽観的」または「」に設定されている場合、TiDB は[楽観的取引モード](/optimistic-transaction.md)を使用します。

### tidb_use_plan_baselines <span class="version-mark">v4.0で追加</span> {#tidb-use-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、実行プランのバインディング機能を有効にするかどうかを制御するために使用されます。デフォルトでは有効になっており、値`OFF`を割り当てることで無効にできます。実行プランのバインディングの使用方法については、[実行計画の拘束](/sql-plan-management.md#create-a-binding)拘束」を参照してください。

### tidb_wait_split_region_finish {#tidb-wait-split-region-finish}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   リージョンの分散には通常長い時間がかかりますが、これはPDスケジューリングとTiKVの負荷によって決まります。この変数は、 `SPLIT REGION`ステートメントの実行時にすべてのリージョンの分散が完了した後に結果をクライアントに返すかどうかを設定するために使用されます。
    -   `ON` 、 `SPLIT REGIONS`ステートメントがすべてのリージョンが分散されるまで待機することを要求します。
    -   `OFF`を指定すると、 `SPLIT REGIONS`ステートメントはすべての領域の散布が完了する前に戻ることができます。
-   リージョンを分散させる場合、分散対象のリージョンの書き込みおよび読み取りパフォーマンスに影響が出る可能性があることに注意してください。バッチ書き込みやデータインポートのシナリオでは、リージョンの分散処理が完了してからデータをインポートすることをお勧めします。

### tidb_wait_split_region_timeout {#tidb-wait-split-region-timeout}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `300`
-   範囲: `[1, 2147483647]`
-   単位：秒
-   この変数は、 `SPLIT REGION`ステートメントの実行タイムアウトを設定するために使用されます。ステートメントが指定された時間内に完全に実行されない場合、タイムアウトエラーが返されます。

### tidb_window_concurrency <span class="version-mark">v4.0で追加</span> {#tidb-window-concurrency-span-class-version-mark-new-in-v4-0-span}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨となりました。代わりに、[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)を使用して設定してください。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位：糸
-   この変数は、ウィンドウ演算子の並行度を設定するために使用されます。
-   値が`-1`の場合は、代わりに値`tidb_executor_concurrency`が使用されます。

### tiflash_fastscan <span class="version-mark">v6.3.0の新機能</span> {#tiflash-fastscan-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   [ファストスキャン](/tiflash/use-fastscan.md)が有効になっている場合 ( `ON`に設定されている場合)、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度やデータの一貫性は保証されません。

### tiflash_fine_grained_shuffle_batch_size <span class="version-mark">v6.2.0で追加</span> {#tiflash-fine-grained-shuffle-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   デフォルト値: `8192`
-   範囲: `[1, 18446744073709551615]`
-   細粒度シャッフルが有効になっている場合、 TiFlashにプッシュダウンされるウィンドウ関数を並列実行できます。この変数は、送信側から送信されるデータのバッチサイズを制御します。
-   パフォーマンスへの影響：ビジネス要件に応じて適切なサイズを設定してください。不適切な設定はパフォーマンスに影響します。値が小さすぎる場合（例えば`1` 、ブロックごとに 1 つのネットワーク転送が発生します。値が大きすぎる場合（例えばテーブルの総行数）、受信側がデータの待機にほとんどの時間を費やすため、パイプライン処理が機能しなくなります。適切な値を設定するには、 TiFlashレシーバーが受信する行数の分布を確認してください。ほとんどのスレッドが数行（例えば数百行）しか受信しない場合は、この値を増やしてネットワークのオーバーヘッドを削減できます。

### tiflash_fine_grained_shuffle_stream_count <span class="version-mark">v6.2.0で追加</span> {#tiflash-fine-grained-shuffle-stream-count-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[-1, 1024]`
-   ウィンドウ関数が実行のためにTiFlashにプッシュダウンされる際、この変数を使用してウィンドウ関数の実行の並行レベルを制御できます。指定可能な値は以下のとおりです。

    -   -1: 細粒度シャッフル機能が無効になります。TiFlashにプッシュダウンされたウィンドウ関数は、シングルスレッドで実行されます。
    -   0: 細粒度シャッフル機能が有効になります。tidb_max_tiflash_threads [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)有効な値 (0 より大きい値) に設定されている場合、 `tiflash_fine_grained_shuffle_stream_count` [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)の値に設定されます。それ以外の場合は、 TiFlash計算ノードの CPU リソースに基づいて自動的に推定されます。TiFlash 上のウィンドウ関数の実際の並行レベルは、min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashTiFlash上の物理スレッド数) です。
    -   0より大きい整数: 細粒度シャッフル機能が有効になります。TiFlashにプッシュダウンされたウィンドウ関数は、複数のスレッドで実行されます。並行処理レベルは、min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノード上の物理スレッド数)です。
-   理論的には、ウィンドウ関数のパフォーマンスはこの値に比例して向上します。しかし、この値が実際の物理スレッド数を超えると、逆にパフォーマンスが低下します。

### tiflash_mem_quota_query_per_node <span class="version-mark">v7.4.0で追加</span> {#tiflash-mem-quota-query-per-node-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashノード上のクエリの最大メモリ使用量を制限します。クエリのメモリ使用量がこの制限を超えると、 TiFlashはエラーを返してクエリを終了します。この変数を`-1`または`0`に設定すると、制限なしとなります。この変数が`0`より大きい値に設定され、 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)有効な値に設定されている場合、 TiFlashは[クエリレベルのスピル](/tiflash/tiflash-spill-disk.md#query-level-spilling)有効にします。

### tiflash_query_spill_ratio <span class="version-mark">v7.4.0で追加</span> {#tiflash-query-spill-ratio-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0, 0.85]`
-   この変数はTiFlashのしきい値を制御します。 [クエリレベルのスピル](/tiflash/tiflash-spill-disk.md#query-level-spilling)`0`は自動クエリ レベル スピルを無効にすることを意味します。この変数が`0`より大きく、クエリのメモリ使用量が[`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) * `tiflash_query_spill_ratio`を超えると、 TiFlash はクエリ レベル スピルをトリガーし、必要に応じてクエリ内のサポートされている演算子のデータをスピルします。

> **注記：**
>
> -   この変数は、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)が`0`より大きい場合にのみ有効になります。つまり、 [tiflash_mem_quota_query_per_node](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)が`0`または`-1`の場合、 `tiflash_query_spill_ratio`が`0`より大きい場合でも、クエリレベルのスピルは有効になりません。
> -   TiFlashクエリレベルのスピリングが有効になっている場合、個々のTiFlashオペレータのスピリングしきい値は自動的に無効になります。つまり、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)と`tiflash_query_spill_ratio`両方が0より大きい場合、 [tidb_max_bytes_before_tiflash_external_sort](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700) 、 [tidb_max_bytes_before_tiflash_external_group_by](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) 、 [tidb_max_bytes_before_tiflash_external_join](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)の3つの変数は自動的に無効になり、これらを`0`に設定するのと同等になります。

### tiflash_replica_read <span class="version-mark">v7.3.0の新機能</span> {#tiflash-replica-read-span-class-version-mark-new-in-v7-3-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `all_replicas`
-   金額オプション： `all_replicas` `closest_adaptive`または`closest_replicas`
-   この変数は、クエリがTiFlashエンジンを必要とする場合に、 TiFlashレプリカを選択するための戦略を設定するために使用されます。
    -   `all_replicas` 、分析計算に利用可能なすべてのTiFlashレプリカを使用することを意味します。
    -   `closest_adaptive` 、クエリを開始するTiDBノードと同じゾーンにあるTiFlashレプリカを優先的に使用することを意味します。このゾーンのレプリカに必要なデータがすべて含まれていない場合、クエリは他のゾーンのTiFlashレプリカと、それに対応するTiFlashノードを巻き込みます。
    -   `closest_replicas`を指定すると、クエリを開始するTiDBノードと同じゾーンにあるTiFlashレプリカのみを使用します。このゾーンのレプリカに必要なデータがすべて含まれていない場合、クエリはエラーを返します。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDBノードに[ゾーン属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)設定されておらず、 `tiflash_replica_read` `all_replicas`に設定されていない場合、 TiFlashはレプリカ選択戦略を無視します。代わりに、すべてのTiFlashレプリカを使用してクエリを実行し、警告`The variable tiflash_replica_read is ignored.`返します。
> -   TiFlashノードに[ゾーン属性](/schedule-replicas-by-topology-labels.md#configure-labels-for-tikv-and-tiflash)設定されていない場合、それらのノードはどのゾーンにも属さないノードとして扱われます。

</CustomContent>

### tiflash_hashagg_preaggregation_mode <span class="version-mark">v8.3.0で追加</span> {#tiflash-hashagg-preaggregation-mode-span-class-version-mark-new-in-v8-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：はい
-   タイプ: 列挙型
-   デフォルト値: `force_preagg`
-   `auto` `force_streaming` ： `force_preagg`
-   この変数は、 TiFlashにプッシュダウンされる2段階または3段階のHashAgg操作の最初の段階で使用される事前集計戦略を制御します。
    -   `force_preagg` ： TiFlashはHashAggの最初の段階で事前集計を強制します。この動作はv8.3.0以前の動作と一致しています。
    -   `force_streaming` : TiFlash は、事前集計を行わずにデータを HashAgg の次のステージに直接送信します。
    -   `auto` ： TiFlashは、現在のワークロードの集約度に基づいて、事前集約を実行するかどうかを自動的に選択します。

### tikv_client_read_timeout は<span class="version-mark">v7.4.0 で追加されました。</span> {#tikv-client-read-timeout-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位：ミリ秒
-   `tikv_client_read_timeout`使用すると、クエリで TiDB が TiKV RPC 読み取りリクエストを送信するタイムアウトを設定できます。TiDB クラスタが不安定なネットワーク環境または深刻な TiKV I/Oレイテンシーのジッターがある環境にあり、アプリケーションが SQL クエリのレイテンシーに敏感な場合は、 `tikv_client_read_timeout`設定して TiKV RPC 読み取りリクエストのタイムアウトを短縮できます。この場合、TiKV ノードで I/Oレイテンシーのジッターが発生すると、TiDB はすぐにタイムアウトして、次の TiKVリージョンピアがある TiKV ノードに RPC リクエストを再送信できます。すべての TiKVリージョンピアのリクエストがタイムアウトした場合、TiDB はデフォルトのタイムアウト (通常 40 秒) で再試行します。
-   クエリ内でオプティマイザヒント`/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */`使用すると、TiDBがTiKV RPC読み取りリクエストを送信するタイムアウトを設定できます。オプティマイザヒントとこのシステム変数の両方が設定されている場合は、オプティマイザヒントが優先されます。
-   デフォルト値の`0` 、デフォルトのタイムアウト（通常は40秒）が使用されることを示します。

> **注記：**
>
> -   通常、通常のクエリは数ミリ秒で完了しますが、TiKVノードのネットワークが不安定な場合やI/Oジッターが発生すると、クエリに1秒以上、場合によっては10秒以上かかることがあります。このような場合、オプティマイザヒント`/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=100) */`を使用して、特定のクエリのTiKV RPC読み取りリクエストのタイムアウトを100ミリ秒に設定できます。こうすることで、TiKVノードの応答が遅い場合でも、TiDBはすぐにタイムアウトして、次のTiKVリージョンピアが存在するTiKVノードにRPCリクエストを再送信できます。2つのTiKVノードが同時にI/Oジッターが発生する確率は低いため、クエリは通常、数ミリ秒から110ミリ秒以内に完了します。
> -   `tikv_client_read_timeout`に小さすぎる値（例えば 1 ミリ秒）を設定しないでください。そうしないと、TiDB クラスタのワークロードが高い場合にリクエストがタイムアウトしやすくなり、その後の再試行によって TiDB クラスタへの負荷がさらに増加し​​ます。
> -   クエリの種類ごとに異なるタイムアウト値を設定する必要がある場合は、オプティマイザヒントを使用することをお勧めします。

### タイムゾーン {#time-zone}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `SYSTEM`
-   この変数は現在のタイムゾーンを返します。値は、「-8:00」のようなオフセット、または「America/Los_Angeles」のような名前付きゾーンのいずれかで指定できます。
-   値`SYSTEM`は、タイムゾーンがシステムホストと同じであるべきであることを意味し、これは[`system_time_zone`](#system_time_zone)変数で取得できます。

### タイムスタンプ {#timestamp}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数の値が空でない場合、それは関数`CURRENT_TIMESTAMP()` `NOW()`およびその他の関数のタイムスタンプとして使用されるUNIXエポックを示します。この変数は、データ復元またはレプリケーションで使用される可能性があります。

### トランザクション分離 {#transaction-isolation}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `REPEATABLE-READ`
-   `READ-COMMITTED` `SERIALIZABLE`値`REPEATABLE-READ` `READ-UNCOMMITTED`
-   この変数はトランザクションの分離を設定します。 TiDB は MySQL との互換性のために`REPEATABLE-READ`宣伝しますが、実際の分離レベルはスナップショット分離です。詳細については、[トランザクション分離レベル](/transaction-isolation-levels.md)参照してください。

### tx_isolation {#tx-isolation}

この変数は`transaction_isolation`の別名です。

### tx_isolation_one_shot {#tx-isolation-one-shot}

> **注記：**
>
> この変数はTiDB内部で使用されます。ユーザー側で使用する必要はありません。

内部的には、TiDBパーサーは`SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]`ステートメントを`SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`に変換します。

### tx_read_ts {#tx-read-ts}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: &quot;&quot;
-   ステイル読み取りシナリオでは、このセッション変数を使用して、Stable Read のタイムスタンプ値を記録します。
-   この変数はTiDBの内部動作に使用されます。この変数を設定することは**推奨されません**。

### トランザクションスコープ {#txn-scope}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `global`
-   値オプション： `global`と`local`
-   この変数は、現在のセッショントランザクションがグローバルトランザクションかローカルトランザクションかを設定するために使用されます。
-   この変数はTiDBの内部動作に使用されます。この変数を設定することは**推奨されません**。

### validate_password.check_user_name<span class="version-mark">は v6.5.0 で追加されました。</span> {#validate-password-check-user-name-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、パスワードの複雑性チェックにおけるチェック項目です。パスワードがユーザー名と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効になります。
-   この変数が有効で`ON`に設定されている場合、パスワードを設定すると、TiDBはパスワードをユーザー名（ホスト名を除く）と比較します。パスワードがユーザー名と一致する場合、パスワードは拒否されます。
-   この変数は[`validate_password.policy`](#validate_passwordpolicy-new-in-v650)とは独立しており、パスワードの複雑性チェックレベルの影響を受けません。

### validate_password.dictionary <span class="version-mark">v6.5.0で追加</span> {#validate-password-dictionary-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `""`
-   型: 文字列
-   この変数は、パスワードの複雑性チェックにおけるチェック項目です。パスワードが辞書と一致するかどうかを確認します。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`2` (STRONG) に設定されている場合にのみ有効になります。
-   この変数は、1024文字以下の文字列です。パスワードに使用できない単語のリストが含まれています。各単語はセミコロン（ `;` ）で区切られています。
-   この変数はデフォルトでは空の文字列に設定されており、辞書チェックは実行されません。辞書チェックを実行するには、照合する単語を文字列に含める必要があります。この変数が設定されている場合、パスワードを設定すると、TiDB はパスワードの各部分文字列 (長さは 4 ～ 100 文字) を辞書内の単語と比較します。パスワードのいずれかの部分文字列が辞書内の単語と一致する場合、パスワードは拒否されます。比較では大文字と小文字は区別されません。

### validate_password.enable は<span class="version-mark">v6.5.0 で追加されました。</span> {#validate-password-enable-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では常に有効になっています。

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   この変数は、パスワードの複雑性チェックを実行するかどうかを制御します。この変数を`ON`に設定すると、パスワードを設定する際にTiDBがパスワードの複雑性チェックを実行します。

### validate_password.length <span class="version-mark">v6.5.0で追加</span> {#validate-password-length-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `8`
-   範囲：TiDB Self-Managedおよび[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合は`[0, 2147483647]` 、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は`[8, 2147483647]`
-   この変数は、パスワードの複雑性チェックにおけるチェック項目です。パスワードの長さが十分かどうかをチェックします。デフォルトでは、パスワードの最小長さは`8`です。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効になります。
-   この変数の値は、式`validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`より小さくてはなりません。
-   `validate_password.number_count` `validate_password.special_char_count`または`validate_password.mixed_case_count`の値を変更して式の値が`validate_password.length`より大きくなると、 `validate_password.length`の値は自動的に式の値に合わせて変更されます。

### validate_password.mixed_case_count <span class="version-mark">v6.5.0で追加</span> {#validate-password-mixed-case-count-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲：TiDB Self-Managedおよび[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合は`[0, 2147483647]` 、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は`[1, 2147483647]`
-   この変数は、パスワードの複雑性チェックにおけるチェック項目です。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合のみ有効になります。
-   パスワードに含まれる大文字の数と小文字の数は、いずれも`validate_password.mixed_case_count`未満であってはなりません。例えば、変数が`1`に設定されている場合、パスワードには少なくとも1つの大文字と1つの小文字が含まれている必要があります。

### validate_password.number_count<span class="version-mark">は v6.5.0 で追加されました。</span> {#validate-password-number-count-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲：TiDB Self-Managedおよび[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合は`[0, 2147483647]` 、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は`[1, 2147483647]`
-   この変数は、パスワードの複雑性チェックにおけるチェック項目です。パスワードに十分な数の数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` （MEDIUM）以上に設定されている場合にのみ有効になります。

### validate_password.policy <span class="version-mark">v6.5.0で追加</span> {#validate-password-policy-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: 列挙型
-   デフォルト値: `1`
-   値オプション：TiDB Self- `2`および[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合は`0` `1` [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) `1`場合は`2`
-   この変数は、パスワードの複雑性チェックのポリシーを制御します。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効になっている場合にのみ有効になります。この変数の値によって、 `validate_password.check_user_name`を除く他の`validate-password`変数がパスワードの複雑性チェックで有効になるかどうかが決まります。
-   この変数の値は`0` `1`または`2` （それぞれLOW、MEDIUM、STRONGに対応）になります。ポリシーレベルによってチェック項目が異なります。
    -   0またはLOW：パスワードの長さ。
    -   1 または MEDIUM: パスワードの長さ、大文字と小文字、数字、および特殊文字。
    -   2 または強力: パスワードの長さ、大文字と小文字、数字、特殊文字、および辞書との一致。

### validate_password.special_char_count<span class="version-mark">は v6.5.0 で追加されました。</span> {#validate-password-special-char-count-span-class-version-mark-new-in-v6-5-0-span}

-   対象範囲：グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `1`
-   範囲：TiDB Self-Managedおよび[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合は`[0, 2147483647]` 、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は`[1, 2147483647]`
-   この変数は、パスワードの複雑性チェックにおけるチェック項目です。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合のみ有効になります。

### バージョン {#version}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値： `8.0.11-TiDB-` （tidbバージョン）
-   この変数は、MySQLのバージョンに続いてTiDBのバージョンを返します。例えば、「8.0.11-TiDB-v8.5.4」のようになります。

### バージョンコメント {#version-comment}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: (文字列)
-   この変数は、TiDBのバージョンに関する詳細情報を返します。例えば、「TiDB Server (Apache License 2.0) Community Edition、MySQL 8.0互換」などです。

### バージョンコンパイルマシン {#version-compile-machine}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: (文字列)
-   この変数は、TiDBが実行されているCPUアーキテクチャの名前を返します。

### バージョンコンパイルOS {#version-compile-os}

-   適用範囲：なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: (文字列)
-   この変数は、TiDBが実行されているOSの名前を返します。

### 待機タイムアウト {#wait-timeout}

> **注記：**
>
> この変数は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   型: 整数
-   デフォルト値: `28800`
-   範囲: `[0, 31536000]`
-   単位：秒
-   この変数は、ユーザーセッションのアイドルタイムアウトを制御します。値がゼロの場合は無制限です。

### 警告回数 {#warning-count}

-   範囲: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   デフォルト値: `0`
-   この読み取り専用変数は、前回実行されたステートメントで発生した警告の数を示します。

### ウィンドウ処理で高精度を使用 {#windowing-use-high-precision}

-   範囲: セッション | グローバル
-   クラスターに保持される: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用：いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は[ウィンドウ関数](/functions-and-operators/window-functions.md)を計算するときに高精度モードを使用するかどうかを制御します。
