---
title: System Variables
summary: システム変数を使用して、パフォーマンスを最適化したり、実行動作を変更したりします。
---

# システム変数 {#system-variables}

TiDB システム変数は、設定が`SESSION`または`GLOBAL`スコープに適用されるという点で、MySQL と同様に動作します。

-   スコープ`SESSION`の変更は現在のセッションにのみ影響します。
-   スコープ`GLOBAL`の変更はすぐに適用されます。この変数もスコープ`SESSION`に設定されている場合、すべてのセッション (自分のセッションを含む) は引き続き現在のセッション値を使用します。
-   Changes are made using the [`SET`ステートメント](/sql-statements/sql-statement-set-variable.md):

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
> いくつかの`GLOBAL`変数は TiDB クラスターに保持されます。このドキュメントの一部の変数には`Persists to cluster`設定があり、これを`Yes`または`No`に設定できます。
>
> -   `Persists to cluster: Yes`に設定されている変数の場合、グローバル変数が変更されると、すべての TiDB サーバーにシステム変数キャッシュを更新する通知が送信されます。追加の TiDB サーバーを追加するか、既存の TiDB サーバーを再起動すると、永続化された構成値が自動的に使用されます。
> -   `Persists to cluster: No`に設定されている変数の場合、変更は接続しているローカル TiDB インスタンスにのみ適用されます。設定された値を保持するには、 `tidb.toml`構成ファイルで変数を指定する必要があります。
>
> さらに、TiDB はいくつかの MySQL 変数を読み取り可能かつ設定可能として提示します。これは互換性のために必要です。アプリケーションとコネクタの両方が MySQL 変数を読み取るのが一般的だからです。たとえば、JDBC コネクタは、動作に依存していないにもかかわらず、クエリ キャッシュ設定の読み取りと設定の両方を行います。

> **注記：**
>
> 値を大きくしても、必ずしもパフォーマンスが向上するわけではありません。ほとんどの設定は各接続に適用されるため、ステートメントを実行している同時接続の数を考慮することも重要です。
>
> 安全な値を決定するときは、変数の単位を考慮してください。
>
> -   スレッドの場合、安全な値は通常、CPU コアの数までになります。
> -   バイトの場合、安全な値は通常、システムメモリの量よりも小さくなります。
> -   時間については、単位が秒またはミリ秒になる可能性があることに注意してください。
>
> 同じ単位を使用する変数は、同じリソース セットを競合する可能性があります。

Starting from v7.4.0, you can temporarily modify the value of some `SESSION` variables during statement execution using [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value). After the statement is executed, the value of the system variable in the current session is automatically changed back to the original value. This hint can be used to modify some system variables related to the optimizer and executor. Variables in this document have a `Applies to hint SET_VAR` setting, which can be configured to `Yes` or `No`.

-   For variables with the `Applies to hint SET_VAR: Yes` setting, you can use the [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) hint to modify the value of the system variable in the current session during statement execution.
-   For variables with the `Applies to hint SET_VAR: No` setting, you cannot use the [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) hint to modify the value of the system variable in the current session during statement execution.

For more information about the `SET_VAR` hint, see [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value).

## 変数参照 {#variable-reference}

### allow_auto_random_explicit_insert <span class="version-mark">v4.0.3 の新機能</span> {#allow-auto-random-explicit-insert-span-class-version-mark-new-in-v4-0-3-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `INSERT`ステートメントで`AUTO_RANDOM`属性を持つ列の値を明示的に指定できるようにするかどうかを決定します。

### authentication_ldap_sasl_auth_method_name <span class="version-mark">v7.1.0 の新</span>機能 {#authentication-ldap-sasl-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `SCRAM-SHA-1`
-   可能な値: `SCRAM-SHA-1` 、 `SCRAM-SHA-256` 、および`GSSAPI` 。
-   LDAP SASL 認証の場合、この変数は認証方法名を指定します。

### authentication_ldap_sasl_bind_base_dn<span class="version-mark">バージョン7.1.0の新</span>機能 {#authentication-ldap-sasl-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は検索ツリー内の検索範囲を制限します。1 `AS ...`なしでユーザーが作成された場合、TiDB はユーザー名に従って LDAPサーバーで`dn`を自動的に検索します。

### authentication_ldap_sasl_bind_root_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。

### authentication_ldap_sasl_bind_root_pwd<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。

### authentication_ldap_sasl_ca_path <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は StartTLS 接続の証明機関ファイルの絶対パスを指定します。

### authentication_ldap_sasl_init_pool_size <span class="version-mark">v7.1.0 の新</span>機能 {#authentication-ldap-sasl-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーへの接続プール内の初期接続を指定します。

### authentication_ldap_sasl_max_pool_size <span class="version-mark">v7.1.0 の新</span>機能 {#authentication-ldap-sasl-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーへの接続プール内の最大接続数を指定します。

### authentication_ldap_sasl_server_host<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は LDAPサーバーのホスト名または IP アドレスを指定します。

### authentication_ldap_sasl_server_port<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### authentication_ldap_sasl_tls <span class="version-mark">v7.1.0 の新</span>機能 {#authentication-ldap-sasl-tls-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP SASL 認証の場合、この変数はプラグインによる LDAPサーバーへの接続が StartTLS で保護されるかどうかを制御します。

### authentication_ldap_simple_auth_method_name <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `SIMPLE`
-   可能な値: `SIMPLE` 。
-   LDAP シンプル認証の場合、この変数は認証方法名を指定します。サポートされる値は`SIMPLE`です。

### authentication_ldap_simple_bind_base_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP シンプル認証の場合、この変数は検索ツリー内の検索範囲を制限します。1 `AS ...`なしでユーザーが作成された場合、TiDB はユーザー名に従って LDAPサーバーで`dn`を自動的に検索します。

### authentication_ldap_simple_bind_root_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。

### authentication_ldap_simple_bind_root_pwd<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。

### authentication_ldap_simple_ca_path <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は StartTLS 接続の証明機関ファイルの絶対パスを指定します。

### authentication_ldap_simple_init_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーへの接続プール内の初期接続を指定します。

### authentication_ldap_simple_max_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP シンプル認証の場合、この変数は LDAPサーバーへの接続プール内の最大接続数を指定します。

### authentication_ldap_simple_server_host<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は LDAPサーバーのホスト名または IP アドレスを指定します。

### authentication_ldap_simple_server_port<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### authentication_ldap_simple_tls <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-tls-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP 簡易認証の場合、この変数はプラグインによる LDAPサーバーへの接続が StartTLS で保護されるかどうかを制御します。

### 自動増分 {#auto-increment-increment}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   Controls the step size of `AUTO_INCREMENT` values to be allocated to a column, and allocation rules for `AUTO_RANDOM` IDs. It is often used in combination with [`auto_increment_offset`](#auto_increment_offset).

### 自動増分オフセット {#auto-increment-offset}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   Controls the initial offset of `AUTO_INCREMENT` values to be allocated to a column, and allocation rules for `AUTO_RANDOM` IDs. This setting is often used in combination with [`auto_increment_increment`](#auto_increment_increment). For example:

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
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   Controls whether statements should automatically commit when not in an explicit transaction. See [トランザクションの概要](/transaction-overview.md#autocommit) for more information.

### ブロック暗号化モード {#block-encryption-mode}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `aes-128-ecb`
-   `aes-256-cbc` `aes-256-ecb` `aes-192-cbc` `aes-128-cbc` `aes-128-ecb` `aes-192-ecb` `aes-128-ofb` `aes-192-ofb` `aes-256-ofb` `aes-128-cfb` `aes-192-cfb` `aes-256-cfb`
-   この変数は、組み込み関数[`AES_ENCRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_encrypt)および[`AES_DECRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_decrypt)の暗号化モードを設定します。

### 文字セットクライアント {#character-set-client}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `utf8mb4`
-   クライアントから送信されるデータの文字セット。TiDB での文字セットと照合順序の使用の詳細については、 [文字セットと照合順序](/character-set-and-collation.md)参照してください。必要に応じて[`SET NAMES`](/sql-statements/sql-statement-set-names.md)使用して文字セットを変更することをお勧めします。

### 文字セット接続 {#character-set-connection}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `utf8mb4`
-   指定された文字セットを持たない文字列リテラルの文字セット。

### 文字セットデータベース {#character-set-database}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `utf8mb4`
-   この変数は、使用中のデフォルト データベースの文字セットを示します。**この変数を設定することは推奨されません**。新しいデフォルト データベースが選択されると、サーバーは変数値を変更します。

### 文字セットの結果 {#character-set-results}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `utf8mb4`
-   データがクライアントに送信されるときに使用される文字セット。

### 文字セットサーバー {#character-set-server}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `utf8mb4`
-   サーバーのデフォルトの文字セット。

### 照合接続 {#collation-connection}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `utf8mb4_bin`
-   この変数は、現在の接続で使用されている照合順序を示します。これは、MySQL 変数`collation_connection`と一致します。

### 照合データベース {#collation-database}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `utf8mb4_bin`
-   この変数は、使用中のデータベースの照合順序の照合順序を示します。**この変数を設定することは推奨されません**。新しいデータベースが選択されると、TiDB はこの変数値を変更します。

### 照合サーバー {#collation-server}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `utf8mb4_bin`
-   データベースの作成時に使用されるデフォルトの照合照合順序。

### cte_max_recursion_depth {#cte-max-recursion-depth}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[0, 4294967295]`
-   共通テーブル式の最大再帰深度を制御します。

### データディレクトリ {#datadir}

> **注記：**
>
> This variable is not supported on [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

<CustomContent platform="tidb">

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値:コンポーネントと展開方法によって異なります。
    -   `/tmp/tidb`: when you set `"unistore"` for [`--store`](/command-line-flags-for-tidb-configuration.md#--store) or if you don't set `--store`.
    -   `${pd-ip}:${pd-port}` : Kubernetes デプロイメント用のTiUPおよびTiDB Operatorのデフォルトのstorageエンジンである TiKV を使用する場合。
-   この変数は、データが保存される場所を示します。この場所は、ローカル パス`/tmp/tidb`にすることも、データが TiKV に保存されている場合は PDサーバーを指すこともできます`${pd-ip}:${pd-port}`という形式の値は、起動時に TiDB が接続する PDサーバーを示します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値:コンポーネントと展開方法によって異なります。
    -   `/tmp/tidb`: when you set `"unistore"` for [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store) or if you don't set `--store`.
    -   `${pd-ip}:${pd-port}` : Kubernetes デプロイメント用のTiUPおよびTiDB Operatorのデフォルトのstorageエンジンである TiKV を使用する場合。
-   この変数は、データが保存される場所を示します。この場所は、ローカル パス`/tmp/tidb`にすることも、データが TiKV に保存されている場合は PDサーバーを指すこともできます`${pd-ip}:${pd-port}`という形式の値は、起動時に TiDB が接続する PDサーバーを示します。

</CustomContent>

### ddl_slow_threshold {#ddl-slow-threshold}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   実行時間がしきい値を超える DDL 操作をログに記録します。

### デフォルト認証プラグイン {#default-authentication-plugin}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `mysql_native_password`
-   可能な`caching_sha2_password` : `mysql_native_password` `authentication_ldap_simple` `tidb_sm3_password` `tidb_auth_token` `authentication_ldap_sasl`
-   この変数は、サーバーとクライアントの接続が確立されるときにサーバーが通知する認証方法を設定します。
-   To authenticate using the `tidb_sm3_password` method, you can connect to TiDB using [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3).

<CustomContent platform="tidb">

For more possible values of this variable, see [認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status).

</CustomContent>

### default_collation_for_utf8mb4 <span class="version-mark">v7.4.0 の新機能</span> {#default-collation-for-utf8mb4-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: グローバル | セッション
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   デフォルト値: `utf8mb4_bin`
-   `utf8mb4_0900_ai_ci` `utf8mb4_general_ci`オプション: `utf8mb4_bin`
-   This variable is used to set the default [照合順序](/character-set-and-collation.md) for the `utf8mb4` character set. It affects the behavior of the following statements:
    -   [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)と[`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)ステートメントに表示されるデフォルトの照合照合順序。
    -   [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)および[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)ステートメントに、照合順序を指定せずにテーブルまたは列に対して`CHARACTER SET utf8mb4`句が含まれている場合、この変数で指定された照合順序順序が使用されます。これは、 `CHARACTER SET`句が使用されていない場合の動作には影響しません。
    -   [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)と[`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)ステートメントに照合順序を指定せずに`CHARACTER SET utf8mb4`の句が含まれている場合、この変数で指定された照合順序が使用されます。これは、 `CHARACTER SET`番目の句が使用されていない場合の動作には影響しません。
    -   `COLLATE`句が使用されていない場合、 `_utf8mb4'string'`形式のすべてのリテラル文字列はこの変数で指定された照合順序を使用します。

### default_password_lifetime <span class="version-mark">v6.5.0 の新機能</span> {#default-password-lifetime-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 65535]`
-   自動パスワード有効期限のグローバル ポリシーを設定します。デフォルト値`0`は、パスワードが期限切れにならないことを示します。このシステム変数が正の整数`N`に設定されている場合、パスワードの有効期間は`N`日間であり、 `N`日以内にパスワードを変更する必要があります。

### デフォルトの週の形式 {#default-week-format}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 7]`
-   `WEEK()`関数で使用される週の形式を設定します。

### disconnect_on_expired_password <span class="version-mark">v6.5.0 の新機能</span> {#disconnect-on-expired-password-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は読み取り専用です。パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを示します。変数が`ON`に設定されている場合、パスワードの有効期限が切れるとクライアント接続が切断されます。変数が`OFF`に設定されている場合、クライアント接続は「サンドボックス モード」に制限され、ユーザーはパスワード リセット操作のみを実行できます。

<CustomContent platform="tidb">

-   If you need to change the behavior of the client connection for the expired password, modify the [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) configuration item in the configuration file.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   If you need to change the default behavior of the client connection for the expired password, contact [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md).

</CustomContent>

### div_precision_increment <span class="version-mark">v8.0.0 の新機能</span> {#div-precision-increment-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[0, 30]`
-   この変数は、 `/`演算子を使用して実行された除算演算の結果のスケールを増やす桁数を指定します。この変数は MySQL と同じです。

### エラー数 {#error-count}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   メッセージを生成した最後のステートメントから発生したエラーの数を示す読み取り専用変数。

### 外部キーチェック {#foreign-key-checks}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: v6.6.0 より前では、デフォルト値は`OFF`です。v6.6.0 以降では、デフォルト値は`ON`です。
-   この変数は、外部キー制約チェックを有効にするかどうかを制御します。

### グループ連結最大長 {#group-concat-max-len}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[4, 18446744073709551615]`
-   `GROUP_CONCAT()`関数内の項目の最大バッファ サイズ。

### オープンSSL {#have-openssl}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQL 互換性のための読み取り専用変数。サーバーで TLS が有効になっている場合は、サーバーによって`YES`に設定されます。

### SSLがある {#have-ssl}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQL 互換性のための読み取り専用変数。サーバーで TLS が有効になっている場合は、サーバーによって`YES`に設定されます。

### ホスト名 {#hostname}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: (システムホスト名)
-   読み取り専用変数としての TiDBサーバーのホスト名。

### アイデンティティ<span class="version-mark">v5.3.0 の新機能</span> {#identity-span-class-version-mark-new-in-v5-3-0-span}

This variable is an alias for [`last_insert_id`](#last_insert_id).

### 初期化接続 {#init-connect}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   `init_connect`機能により、TiDBサーバーに初めて接続するときに SQL ステートメントが自動的に実行されます。 `CONNECTION_ADMIN`または`SUPER`権限がある場合、この`init_connect`ステートメントは実行されません。 `init_connect`ステートメントでエラーが発生した場合、ユーザー接続は終了します。

### innodb_lock_wait_timeout {#innodb-lock-wait-timeout}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `50`
-   範囲: `[1, 3600]`
-   単位: 秒
-   悲観的トランザクションのロック待機タイムアウト (デフォルト)。

### インタラクティブタイムアウト {#interactive-timeout}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[1, 31536000]`
-   単位: 秒
-   This variable represents the idle timeout of the interactive user session. Interactive user session refers to the session established by calling [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API using the `CLIENT_INTERACTIVE` option (for example, MySQL Shell and MySQL Client). This variable is fully compatible with MySQL.

### 最後の挿入ID {#last-insert-id}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、挿入ステートメントによって生成された最後の`AUTO_INCREMENT`または`AUTO_RANDOM`値を返します。
-   `last_insert_id`の値は、関数`LAST_INSERT_ID()`によって返される値と同じです。

### last_plan_from_binding <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-binding-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable is used to show whether the execution plan used in the previous statement was influenced by a [プランバインディング](/sql-plan-management.md)

### last_plan_from_cache <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-cache-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、前の`execute`ステートメントで使用された実行プランがプラン キャッシュから直接取得されたかどうかを示すために使用されます。

### last_sql_use_alloc <span class="version-mark">v6.4.0 の新機能</span> {#last-sql-use-alloc-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `OFF`
-   この変数は読み取り専用です。前のステートメントがキャッシュされたチャンク オブジェクト (チャンク割り当て) を使用するかどうかを示すために使用されます。

### ライセンス {#license}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `Apache License 2.0`
-   この変数は、TiDBサーバーインストールのライセンスを示します。

### max_allowed_packet <span class="version-mark">v6.1.0 の新機能</span> {#max-allowed-packet-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `67108864`
-   範囲: `[1024, 1073741824]`
-   値は 1024 の整数倍である必要があります。値が 1024 で割り切れない場合は警告が表示され、値は切り捨てられます。たとえば、値が 1025 に設定されている場合、TiDB の実際の値は 1024 です。
-   1 回のパケット送信でサーバーとクライアントが許可する最大パケット サイズ。
-   `SESSION`スコープでは、この変数は読み取り専用です。
-   この変数は MySQL と互換性があります。

### password_history <span class="version-mark">v6.5.0 の新機能</span> {#password-history-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、パスワード変更回数に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、パスワード変更回数に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数が正の整数`N`に設定されている場合、最後の`N`パスワードの再利用は許可されません。

### mpp_exchange_compression_mode <span class="version-mark">v6.6.0 の新機能</span> {#mpp-exchange-compression-mode-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   デフォルト値: `UNSPECIFIED`
-   `HIGH_COMPRESSION` `FAST` `UNSPECIFIED` : `NONE`
-   この変数は、MPP Exchange オペレータのデータ圧縮モードを指定するために使用されます。この変数は、TiDB がバージョン番号`1`の MPP 実行プランを選択した場合に有効になります。変数値の意味は次のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。TiDB は圧縮モードを自動的に選択します。現在、TiDB は`FAST`モードを自動的に選択します。
    -   `NONE` : データ圧縮は使用されません。
    -   `FAST` : 高速モード。全体的なパフォーマンスは良好で、圧縮率は`HIGH_COMPRESSION`未満です。
    -   `HIGH_COMPRESSION` : 高圧縮比モード。

### mpp_version <span class="version-mark">v6.6.0 の新機能</span> {#mpp-version-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   デフォルト値: `UNSPECIFIED`
-   `1` `0` `2` : `UNSPECIFIED`
-   この変数は、MPP 実行プランの異なるバージョンを指定するために使用されます。バージョンを指定すると、TiDB は指定されたバージョンの MPP 実行プランを選択します。変数値の意味は次のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。TiDB は最新バージョン`2`自動的に選択します。
    -   `0` : すべての TiDB クラスター バージョンと互換性があります。このモードでは、MPP バージョンが`0`より大きい機能は有効になりません。
    -   `1`: new in v6.6.0, used to enable data exchange with compression on TiFlash. For details, see [MPPバージョンと交換データ圧縮](/explain-mpp.md#mpp-version-and-exchange-data-compression).
    -   `2` : v7.3.0 の新機能。MPP タスクがTiFlashでエラーに遭遇したときに、より正確なエラー メッセージを提供するために使用されます。

### password_reuse_interval <span class="version-mark">v6.5.0 の新機能</span> {#password-reuse-interval-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、経過時間に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0`は、経過時間に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数が正の整数`N`に設定されている場合、過去`N`日間に使用されたパスワードの再利用は許可されません。

### 最大接続数 {#max-connections}

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   単一の TiDB インスタンスに許可される同時接続の最大数。この変数はリソース制御に使用できます。
-   デフォルト値`0`制限がないことを意味します。この変数の値が`0`より大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新しい接続を拒否します。

### 最大実行時間 {#max-execution-time}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   ステートメントの最大実行時間。デフォルト値は無制限 (ゼロ) です。

> **注記：**
>
> v6.4.0 より前では、 `max_execution_time`システム変数はすべてのタイプのステートメントに適用されます。v6.4.0 以降では、この変数は読み取り専用ステートメントの最大実行時間のみを制御します。タイムアウト値の精度はおよそ 100 ミリ秒です。つまり、指定したとおりに正確なミリ秒数でステートメントが終了しない可能性があります。

<CustomContent platform="tidb">

ヒント[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)を持つ SQL 文の場合、この文の最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、説明されているように、SQL バインディングで使用することもできます[in the SQL FAQ](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

ヒント[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)を持つ SQL 文の場合、この文の最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、説明されているように、SQL バインディングで使用することもできます[in the SQL FAQ](https://docs.pingcap.com/tidb/stable/sql-faq) 。

</CustomContent>

### 最大準備済みステートメント数 {#max-prepared-stmt-count}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 1048576]`
-   Specifies the maximum number of [`PREPARE`](/sql-statements/sql-statement-prepare.md) statements in the current TiDB instance.
-   値`-1`は、現在の TiDB インスタンス内のステートメントの最大数`PREPARE`に制限がないことを意味します。
-   変数を上限`1048576`超える値に設定した場合、代わりに`1048576`使用されます。

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

### pd_enable_follower_handle_region <span class="version-mark">v7.6.0 の新機能</span> {#pd-enable-follower-handle-region-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、アクティブ PDFollower機能を有効にするかどうかを制御します (現在はリージョン情報の要求にのみ適用されます)。値が`OFF`の場合、TiDB は PD リーダーからのみリージョン情報を取得します。値が`ON`の場合、TiDB はリージョン情報の要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を処理できるため、PD リーダーの CPU 負荷が軽減されます。
-   アクティブ PDFollowerを有効にするシナリオ:
    -   多数のリージョンを持つクラスターでは、ハートビートの処理とタスクのスケジュール設定によるオーバーヘッドの増加により、PD リーダーの CPU 負荷が高くなります。
    -   多数の TiDB インスタンスを含む TiDB クラスターでは、リージョン情報に対する要求の同時性が高いため、PD リーダーの CPU 負荷が高くなります。

### プラグインディレクトリ {#plugin-dir}

> **注記：**
>
> This variable is not supported on [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   コマンドラインフラグで指定されたプラグインをロードするディレクトリを示します。

### プラグインロード {#plugin-load}

> **注記：**
>
> This variable is not supported on [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   TiDB の起動時にロードするプラグインを示します。これらのプラグインは、コマンドライン フラグで指定され、カンマで区切られます。

### ポート {#port}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 65535]`
-   MySQL プロトコルを話すときに`tidb-server`がリッスンしているポート。

### ランドシード1 {#rand-seed1}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL 関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作は MySQL と互換性があります。

### ランドシード2 {#rand-seed2}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL 関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作は MySQL と互換性があります。

### require_secure_transport <span class="version-mark">v6.1.0 の新機能</span> {#require-secure-transport-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> Currently, this variable is not supported on [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated). DO **NOT** enable this variable for TiDB Cloud Dedicated clusters. Otherwise, you might get SQL client connection failures. This restriction is a temporary control measure and will be resolved in a future release.

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: TiDBセルフ`ON`の場合は`OFF` [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)場合は[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)

<CustomContent platform="tidb">

-   This variable ensures that all connections to TiDB are either on a local socket, or using TLS. See [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md) for additional details.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB へのすべての接続がローカル ソケット上にあるか、TLS を使用していることを保証します。

</CustomContent>

-   この変数を`ON`に設定すると、TLS が有効になっているセッションから TiDB に接続する必要があります。これにより、TLS が正しく構成されていない場合にロックアウト シナリオが発生するのを防ぐことができます。
-   この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。
-   v6.5.6、v7.1.2、v7.5.1、v8.0.0 以降では、Security強化モード (SEM) が有効になっている場合、ユーザーの接続に関する潜在的な問題を回避するために、この変数を`ON`に設定することは禁止されています。

### skip_name_resolve <span class="version-mark">v5.2.0 の新機能</span> {#skip-name-resolve-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `tidb-server`インスタンスが接続ハンドシェイクの一部としてホスト名を解決するかどうかを制御します。
-   DNS が信頼できない場合は、このオプションを有効にしてネットワーク パフォーマンスを向上させることができます。

> **注記：**
>
> `skip_name_resolve=ON`の場合、ID にホスト名を持つユーザーはサーバーにログインできなくなります。例:
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> この例では、 `apphost` IPアドレスまたはワイルドカード（ `%` ）に置き換えることをお勧めします。

### ソケット {#socket}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   MySQL プロトコルを話すときに`tidb-server`がリッスンしているローカル UNIX ソケット ファイル。

### SQLモード {#sql-mode}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   デフォルト値: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
-   This variable controls a number of MySQL compatibility behaviors. See [SQL モード](/sql-mode.md) for more information.

### sql_require_primary_key <span class="version-mark">v6.3.0 の新機能</span> {#sql-require-primary-key-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、テーブルに主キーが必要であるという要件を強制するかどうかを制御します。この変数を有効にすると、主キーのないテーブルを作成または変更しようとするとエラーが発生します。
-   This feature is based on the similarly named [`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key) in MySQL 8.0.
-   TiCDC を使用する場合は、この変数を有効にすることを強くお勧めします。これは、MySQL シンクへの変更をレプリケートするには、テーブルに主キーが必要であるためです。

<CustomContent platform="tidb">

-   If you enable this variable and are using TiDB Data Migration (DM) to migrate data, it is recommended that you add `sql_require_ primary_key` to the `session` part in the [DM タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) and set it to `OFF`. Otherwise, it will cause DM to fail to create tasks.

</CustomContent>

### sql_select_limit <span class="version-mark">v4.0.2 の新機能</span> {#sql-select-limit-span-class-version-mark-new-in-v4-0-2-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `18446744073709551615`
-   範囲: `[0, 18446744073709551615]`
-   単位: 行
-   `SELECT`ステートメントによって返される行の最大数。

### ssl_ca {#ssl-ca}

<CustomContent platform="tidb">

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   The location of the certificate authority file (if there is one). The value of this variable is defined by the TiDB configuration item [`ssl-ca`](/tidb-configuration-file.md#ssl-ca).

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   The location of the certificate authority file (if there is one). The value of this variable is defined by the TiDB configuration item [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca).

</CustomContent>

### SSL証明書 {#ssl-cert}

<CustomContent platform="tidb">

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   The location of the certificate file (if there is a file) that is used for SSL/TLS connections. The value of this variable is defined by the TiDB configuration item [`ssl-cert`](/tidb-configuration-file.md#ssl-cert).

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   The location of the certificate file (if there is a file) that is used for SSL/TLS connections. The value of this variable is defined by the TiDB configuration item [`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert).

</CustomContent>

### SSLキー {#ssl-key}

<CustomContent platform="tidb">

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   The location of the private key file (if there is one) that is used for SSL/TLS connections. The value of this variable is defined by TiDB configuration item [`ssl-key`](/tidb-configuration-file.md#ssl-cert).

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   The location of the private key file (if there is one) that is used for SSL/TLS connections. The value of this variable is defined by TiDB configuration item [`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key).

</CustomContent>

### システムタイムゾーン {#system-time-zone}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: (システム依存)
-   This variable shows the system time zone from when TiDB was first bootstrapped. See also [`time_zone`](#time_zone).

### tidb_adaptive_closest_read_threshold <span class="version-mark">v6.3.0 の新機能</span> {#tidb-adaptive-closest-read-threshold-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `4096`
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   This variable is used to control the threshold at which the TiDB server prefers to send read requests to a replica in the same availability zone as the TiDB server when [`tidb_replica_read`](#tidb_replica_read-new-in-v40) is set to `closest-adaptive`. If the estimated result is higher than or equal to this threshold, TiDB prefers to send read requests to a replica in the same availability zone. Otherwise, TiDB sends read requests to the leader replica.

### tidb_allow_tiflash_cop <span class="version-mark">v7.3.0 の新機能</span> {#tidb-allow-tiflash-cop-span-class-version-mark-new-in-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   TiDB が計算タスクをTiFlashにプッシュダウンする場合、選択できる方法 (またはプロトコル) は、Cop、BatchCop、および MPP の 3 つです。Cop や BatchCop と比較すると、MPP プロトコルはより成熟しており、タスクとリソースの管理がより優れています。したがって、MPP プロトコルを使用することをお勧めします。
    -   `0`または`OFF` : オプティマイザーはTiFlash MPP プロトコルを使用してのみプランを生成します。
    -   `1`または`ON` : オプティマイザーは、コスト見積もりに基づいて実行プランを生成するために Cop、BatchCop、または MPP プロトコルを使用するかどうかを決定します。

### tidb_allow_batch_cop <span class="version-mark">v4.0 の新機能</span> {#tidb-allow-batch-cop-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   この変数は、TiDB がコプロセッサ要求をTiFlashに送信する方法を制御するために使用されます。次の値があります。

    -   `0` : リクエストをバッチで送信しない
    -   `1` :集計と参加のリクエストはバッチで送信されます
    -   `2` : すべてのコプロセッサ要求はバッチで送信されます

### tidb_allow_fallback_to_tikv<span class="version-mark">バージョン5.0の新機能</span> {#tidb-allow-fallback-to-tikv-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   デフォルト値: &quot;&quot;
-   この変数は、TiKV にフォールバックする可能性のあるstorageエンジンのリストを指定するために使用されます。リスト内の指定されたstorageエンジンの障害により SQL ステートメントの実行が失敗した場合、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。この変数は、&quot;&quot; または &quot;tiflash&quot; に設定できます。この変数が &quot;tiflash&quot; に設定されている場合、 TiFlash がタイムアウト エラー (エラー コード: ErrTiFlashServerTimeout) を返すと、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。

### tidb_allow_function_for_expression_index <span class="version-mark">v5.2.0 の新機能</span> {#tidb-allow-function-for-expression-index-span-class-version-mark-new-in-v5-2-0-span}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash`
-   This read-only variable is used to show the functions that are allowed to be used for creating [表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index).

### tidb_allow_mpp <span class="version-mark">v5.0 の新機能</span> {#tidb-allow-mpp-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `ON`
-   クエリを実行するためにTiFlashの MPP モードを使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0` or `OFF`, which means that the MPP mode will not be used. For v7.3.0 or a later version, if you set the value of this variable to `0` or `OFF`, you also need to enable the [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730) variable. Otherwise, queries might return errors.
    -   `1`または`ON` 。これは、オプティマイザがコスト推定に基づいて MPP モードを使用するかどうかを決定することを意味します (デフォルト)。

MPP is a distributed computing framework provided by the TiFlash engine, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. For details about the selection of the MPP mode, refer to [MPPモードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode).

### tidb_allow_remove_auto_inc <span class="version-mark">v2.1.18 および v3.0.4 の新機能</span> {#tidb-allow-remove-auto-inc-span-class-version-mark-new-in-v2-1-18-and-v3-0-4-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`ステートメントを実行して列の`AUTO_INCREMENT`のプロパティを削除できるかどうかを設定するために使用されます。デフォルトでは許可されていません。

### tidb_analyze_column_options <span class="version-mark">v8.3.0 の新機能</span> {#tidb-analyze-column-options-span-class-version-mark-new-in-v8-3-0-span}

> **注記：**
>
> -   This variable only works when [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510) is set to `2`.
> -   TiDB クラスターを v8.3.0 より前のバージョンから v8.3.0 以降にアップグレードする場合、元の動作を維持するために、この変数はデフォルトで`ALL`に設定されます。
> -   v8.3.0 以降では、新しくデプロイされた TiDB クラスターの場合、この変数はデフォルトで`PREDICATE`に設定されます。

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `PREDICATE`
-   `PREDICATE`のオプション: `ALL`
-   This variable controls the behavior of the `ANALYZE TABLE` statement. Setting it to `PREDICATE` means only collecting statistics for [述語列](/statistics.md#collect-statistics-on-some-columns); setting it to `ALL` means collecting statistics for all columns. In scenarios where OLAP queries are used, it is recommended to set it to `ALL`, otherwise collecting statistics can result in a significant drop in query performance.

### tidb_analyze_distsql_scan_concurrency <span class="version-mark">v7.6.0 の新機能</span> {#tidb-analyze-distsql-scan-concurrency-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[0, 4294967295]` 。v8.2.0 より前のバージョンでは、最小値は`1`です。 `0`に設定すると、クラスターのサイズに基づいて同時実行性が適応的に調整されます。
-   この変数は、 `ANALYZE`操作を実行するときに`scan`操作の同時実行性を設定するために使用されます。

### tidb_analyze_partition_concurrency {#tidb-analyze-partition-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `2` 。v7.4.0 以前のバージョンではデフォルト値は`1`です。
-   範囲: `[1, 128]` 。v8.4.0 より前では、値の範囲は`[1, 18446744073709551615]`です。
-   この変数は、TiDB がパーティションテーブルを分析するときに、収集された統計情報を書き込む同時実行性を指​​定します。

### tidb_analyze_version <span class="version-mark">v5.1.0 の新機能</span> {#tidb-analyze-version-span-class-version-mark-new-in-v5-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   TiDB が統計を収集する方法を制御します。
    -   TiDB Self-Managed の場合、この変数のデフォルト値は、v5.3.0 以降で`1`から`2`に変更されます。
    -   TiDB Cloudの場合、この変数のデフォルト値は、v6.5.0 以降で`1`から`2`に変更されます。
    -   クラスターが以前のバージョンからアップグレードされた場合、アップグレード後もデフォルト値`tidb_analyze_version`は変更されません。
-   For detailed introduction about this variable, see [統計入門](/statistics.md).

### tidb_analyze_skip_column_types <span class="version-mark">v7.2.0 の新機能</span> {#tidb-analyze-skip-column-types-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: 「json、blob、mediumblob、longblob、mediumtext、longtext」。 v8.2.0 より前のデフォルト値は「json,blob,mediumblob,longblob」です。
-   可能な値: &quot;json、blob、mediumblob、longblob、text、mediumtext、longtext&quot;
-   この変数は、統計を収集する`ANALYZE`コマンドを実行するときに、統計収集でスキップされる列のタイプを制御します。この変数は`tidb_analyze_version = 2`にのみ適用されます。 `ANALYZE TABLE t COLUMNS c1, ... , cn`使用して列を指定しても、そのタイプが`tidb_analyze_skip_column_types`の場合、指定された列の統計は収集されません。

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

### tidb_auto_analyze_concurrency <span class="version-mark">v8.4.0 の新機能</span> {#tidb-auto-analyze-concurrency-span-class-version-mark-new-in-v8-4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 2147483647]`
-   この変数は、単一の自動統計収集タスク内の同時実行性を設定するために使用されます。v8.4.0 より前では、この同時実行性は`1`に固定されています。統計収集タスクを高速化するには、クラスターの使用可能なリソースに基づいてこの同時実行性を増やすことができます。

### tidb_auto_analyze_終了時間 {#tidb-auto-analyze-end-time}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、UTC 時間で午前 1 時から午前 3 時までの間のみ自動統計更新を許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`設定します。

### tidb_auto_analyze_partition_batch_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-auto-analyze-partition-batch-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `128` 。v7.6.0 より前では、デフォルト値は`1`です。
-   範囲: `[1, 1024]`
-   This variable specifies the number of partitions that TiDB [自動的に分析する](/statistics.md#automatic-update) when analyzing a partitioned table (which means automatically collecting statistics on a partitioned table).
-   この変数の値がパーティション数より小さい場合、TiDB はパーティションテーブルのすべてのパーティションを複数のバッチで自動的に分析します。この変数の値がパーティション数以上の場合、TiDB はパーティションテーブルのすべてのパーティションを同時に分析します。
-   パーティションテーブルのパーティション数がこの変数値よりもはるかに多く、自動分析に時間がかかる場合は、この変数の値を増やして時間の消費を減らすことができます。

### tidb_auto_analyze_ratio {#tidb-auto-analyze-ratio}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: フロート
-   デフォルト値: `0.5`
-   範囲: `(0, 1]` 。v8.0.0 以前のバージョンの範囲は`[0, 18446744073709551615]`です。
-   This variable is used to set the threshold when TiDB automatically executes [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) in a background thread to update table statistics. For example, a value of 0.5 means that auto-analyze is triggered when greater than 50% of the rows in a table have been modified. Auto-analyze can be restricted to only execute during certain hours of the day by specifying `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`.

> **注記：**
>
> この機能を使用するには、システム変数`tidb_enable_auto_analyze` `ON`に設定する必要があります。

### tidb_auto_analyze_start_time {#tidb-auto-analyze-start-time}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、UTC 時間で午前 1 時から午前 3 時までの間のみ自動統計更新を許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`設定します。

### tidb_auto_build_stats_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-auto-build-stats-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、統計の自動更新を実行する同時実行性を設定するために使用されます。

### tidb_backoff_lock_fast {#tidb-backoff-lock-fast}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 2147483647]`
-   この変数は、読み取り要求がロックに遭遇する`backoff`回を設定するために使用されます。

### tidb_backoff_weight {#tidb-backoff-weight}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB `backoff`の最大時間、つまり、内部ネットワークまたはその他のコンポーネント(TiKV、PD) の障害が発生したときに再試行要求を送信するための最大再試行時間の重みを増やすために使用されます。この変数は最大再試行時間を調整するために使用でき、最小値は 1 です。

    たとえば、TiDB が PD から TSO を取得する場合の基本タイムアウトは 15 秒です。1 `tidb_backoff_weight = 2`場合、TSO を取得する場合の最大タイムアウトは、*基本時間 * 2 = 30 秒*です。

    ネットワーク環境が悪い場合、この変数の値を適切に増やすことで、タイムアウトによってアプリケーション側へのエラー報告を効果的に軽減できます。アプリケーション側でエラー情報をより早く受け取りたい場合は、この変数の値を最小にしてください。

### tidb_バッチコミット {#tidb-batch-commit}

> **警告：**
>
> この変数を有効にすることはお勧めし**ません**。

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチコミット機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、いくつかのステートメントをグループ化してトランザクションを複数のトランザクションに分割し、非アトミックにコミットする可能性がありますが、これは推奨されません。

### tidb_batch_delete {#tidb-batch-delete}

> **警告：**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [非トランザクションDML](/non-transactional-dml.md).

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨の batch-dml 機能の一部である batch-delete 機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `DELETE`ステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`も有効にして、 `tidb_dml_batch_size`に正の値を設定する必要がありますが、これは推奨されません。

### tidb_batch_insert {#tidb-batch-insert}

> **警告：**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [非トランザクションDML](/non-transactional-dml.md).

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨の batch-dml 機能の一部である batch-insert 機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `INSERT`ステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`も有効にして、 `tidb_dml_batch_size`に正の値を設定する必要がありますが、これは推奨されません。

### tidb_batch_pending_tiflash_count <span class="version-mark">v6.0 の新機能</span> {#tidb-batch-pending-tiflash-count-span-class-version-mark-new-in-v6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 4294967295]`
-   `ALTER DATABASE SET TIFLASH REPLICA`使用してTiFlashレプリカを追加するときに許可される使用不可テーブルの最大数を指定します。使用不可テーブルの数がこの制限を超えると、操作が停止するか、残りのテーブルに対するTiFlashレプリカの設定が非常に遅くなります。

### tidb_broadcast_join_threshold_count <span class="version-mark">v5.0 の新機能</span> {#tidb-broadcast-join-threshold-count-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `10240`
-   範囲: `[0, 9223372036854775807]`
-   単位: 行
-   結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを見積もることができません。この場合、サイズは結果セットの行数によって決まります。サブクエリの推定行数がこの変数の値より少ない場合、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   This variable will not take effect after [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) is enabled.

### tidb_broadcast_join_threshold_size <span class="version-mark">v5.0 の新機能</span> {#tidb-broadcast-join-threshold-size-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `104857600` (100 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   テーブル サイズが変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   This variable will not take effect after [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) is enabled.

### tidb_build_stats_concurrency {#tidb-build-stats-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `2` 。v7.4.0 以前のバージョンではデフォルト値は`4`です。
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `ANALYZE`ステートメントを実行する同時実行性を設定するために使用されます。
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_build_sampling_stats_concurrency <span class="version-mark">v7.5.0 の新機能</span> {#tidb-build-sampling-stats-concurrency-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   単位: スレッド
-   デフォルト値: `2`
-   範囲: `[1, 256]`
-   この変数は、 `ANALYZE`プロセスでのサンプリング同時実行性を設定するために使用されます。
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_capture_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-capture-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable is used to control whether to enable the [ベースラインキャプチャ](/sql-plan-management.md#baseline-capturing) feature. This feature depends on the statement summary, so you need to enable the statement summary before you use baseline capturing.
-   この機能を有効にすると、ステートメント サマリー内の履歴 SQL ステートメントが定期的に走査され、少なくとも 2 回出現する SQL ステートメントに対してバインディングが自動的に作成されます。

### tidb_cdc_write_source <span class="version-mark">v6.5.0 の新機能</span> {#tidb-cdc-write-source-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   スコープ: セッション
-   クラスターに存続: いいえ
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数が 0 以外の値に設定されている場合、このセッションで書き込まれたデータは TiCDC によって書き込まれたものと見なされます。この変数は TiCDC によってのみ変更できます。いかなる場合でも、この変数を手動で変更しないでください。

### tidb_check_mb4_value_in_utf8 {#tidb-check-mb4-value-in-utf8}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable is used to enforce that the `utf8` character set only stores values from the [基本多言語面 (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane). To store characters outside the BMP, it is recommended to use the `utf8mb4` character set.
-   You might need to disable this option when upgrading your cluster from an earlier version of TiDB where the `utf8` checking was more relaxed. For details, see [アップグレード後のよくある質問](https://docs.pingcap.com/tidb/stable/upgrade-faq).

### tidb_チェックサム_テーブル_同時実行性 {#tidb-checksum-table-concurrency}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   This variable is used to set the scan index concurrency of executing the [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) statement.
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_committer_concurrency <span class="version-mark">v6.1.0 の新機能</span> {#tidb-committer-concurrency-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `128`
-   範囲: `[1, 10000]`
-   単一トランザクションのコミット フェーズでコミットの実行に関連する要求の goroutine の数。
-   コミットするトランザクションが大きすぎる場合、トランザクションがコミットされるときのフロー制御キューの待機時間が長すぎる可能性があります。このような状況では、構成値を増やすことでコミットを高速化できます。
-   この設定は以前は`tidb.toml`オプション ( `performance.committer-concurrency` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_config {#tidb-config}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   この変数は読み取り専用です。現在の TiDBサーバーの構成情報を取得するために使用されます。

### tidb_constraint_check_in_place {#tidb-constraint-check-in-place}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable only applies to optimistic transactions. For pessimistic transactions, use [`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-new-in-v630) instead.
-   When this variable is set to `OFF`, checking for duplicate values in unique indexes is deferred until the transaction commits. This helps improve performance but might be an unexpected behavior for some applications. See [制約](/constraints.md#optimistic-transactions) for details.

    -   `tidb_constraint_check_in_place` ～ `OFF`に設定し、楽観的トランザクションを使用する場合:

        ```sql
        tidb> create table t (i int key);
        tidb> insert into t values (1);
        tidb> begin optimistic;
        tidb> insert into t values (1);
        Query OK, 1 row affected
        tidb> commit; -- Check only when a transaction is committed.
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    -   `tidb_constraint_check_in_place` ～ `ON`に設定し、楽観的トランザクションを使用する場合:

        ```sql
        tidb> set @@tidb_constraint_check_in_place=ON;
        tidb> begin optimistic;
        tidb> insert into t values (1);
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_constraint_check_in_place_pessimistic <span class="version-mark">v6.3.0 の新機能</span> {#tidb-constraint-check-in-place-pessimistic-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: デフォルトでは、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)構成項目は`true`なので、この変数のデフォルト値は`ON`です。 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) `false`に設定されている場合、この変数のデフォルト値は`OFF`です。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`

</CustomContent>

-   This variable only applies to pessimistic transactions. For optimistic transactions, use [`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place) instead.
-   When this variable is set to `OFF`, TiDB defers the unique constraint check of a unique index (to the next time when executing a statement that requires a lock to the index or to the time when committing the transaction). This helps improve performance but might be an unexpected behavior for some applications. See [制約](/constraints.md#pessimistic-transactions) for details.
-   この変数を無効にすると、悲観的トランザクションで TiDB が`LazyUniquenessCheckFailure`エラーを返す可能性があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。
-   When this variable is disabled, you cannot use [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md) in pessimistic transactions.
-   この変数が無効になっている場合、悲観的トランザクションをコミットすると`Write conflict`または`Duplicate entry`エラーが返される可能性があります。このようなエラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    -   `tidb_constraint_check_in_place_pessimistic` ～ `OFF`に設定し、悲観的トランザクションを使用する場合:

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

    -   `tidb_constraint_check_in_place_pessimistic` ～ `ON`に設定し、悲観的トランザクションを使用する場合:

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

            ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'

### tidb_cost_model_version <span class="version-mark">v6.2.0 の新機能</span> {#tidb-cost-model-version-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> -   TiDB v6.5.0 以降、新しく作成されたクラスターはデフォルトでコスト モデル バージョン 2 を使用します。TiDB バージョンを v6.5.0 より前から v6.5.0 以降にアップグレードした場合、値`tidb_cost_model_version`は変更されません。
> -   コスト モデルのバージョンを切り替えると、クエリ プランが変更される可能性があります。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `2`
-   値のオプション:
    -   `1` : TiDB v6.4.0 以前のバージョンでデフォルトで使用されるコスト モデル バージョン 1 を有効にします。
    -   `2`: enables the [コストモデル バージョン 2](/cost-model.md#cost-model-version-2), which is generally available in TiDB v6.5.0 and is more accurate than the version 1 in internal tests.
-   The version of cost model affects the plan decision of optimizer. For more details, see [コストモデル](/cost-model.md).

### tidb_current_ts {#tidb-current-ts}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は読み取り専用です。現在のトランザクションのタイムスタンプを取得するために使用されます。

### tidb_ddl_disk_quota <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-disk-quota-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `107374182400` (100 GiB)
-   範囲: `[107374182400, 1125899906842624]` ([100 GiB、1 PiB])
-   単位: バイト
-   This variable only takes effect when [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630) is enabled. It sets the usage limit of local storage during backfilling when creating an index.

### tidb_ddl_enable_fast_reorg <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-enable-fast-reorg-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> -   If you are using a [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) cluster, to improve the speed for index creation using this variable, make sure that your TiDB cluster is hosted on AWS and your TiDB node size is at least 8 vCPU.
> -   For [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters, this variable is read-only.

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックス作成のバックフィルの速度を向上させるために、 `ADD INDEX`と`CREATE INDEX`のアクセラレーションを有効にするかどうかを制御します。この変数値を`ON`に設定すると、大量のデータを含むテーブルでのインデックス作成のパフォーマンスが向上します。
-   v7.1.0 以降、インデックス アクセラレーション操作はチェックポイントをサポートします。障害により TiDB 所有者ノードが再起動または変更された場合でも、TiDB は定期的に自動的に更新されるチェックポイントから進行状況を回復できます。
-   To verify whether a completed `ADD INDEX` operation is accelerated, you can execute the [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs) statement to see whether `ingest` is displayed in the `JOB_TYPE` column.

<CustomContent platform="tidb">

> **注記：**
>
> -   Index acceleration requires a [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) that is writable and has enough free space. If the `temp-dir` is unusable, TiDB falls back to non-accelerated index building. It is recommended to put the `temp-dir` on a SSD disk.
>
> -   Before you upgrade TiDB to v6.5.0 or later, it is recommended that you check whether the [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) path of TiDB is correctly mounted to an SSD disk. Make sure that the operating system user that runs TiDB has the read and write permissions for this directory. Otherwise, The DDL operations might experience unpredictable issues. This path is a TiDB configuration item, which takes effect after TiDB is restarted. Therefore, setting this configuration item before upgrading can avoid another restart.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> Currently, this feature is not fully compatible with [1 つの`ALTER TABLE`ステートメントで複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md). When adding a unique index with the index acceleration, you need to avoid altering other columns or indexes in the same statement.

</CustomContent>

### tidb_enable_dist_task <span class="version-mark">v7.1.0 の新機能</span> {#tidb-enable-dist-task-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `ON`
-   This variable is used to control whether to enable the [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md). After the framework is enabled, the DXF tasks such as DDL and import will be distributedly executed and completed by multiple TiDB nodes in the cluster.
-   Starting from TiDB v7.1.0, the DXF supports distributedly executing the [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) statement for partitioned tables.
-   Starting from TiDB v7.2.0, the DXF supports distributedly executing the [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) statement for import jobs.
-   TiDB v8.1.0 以降では、この変数はデフォルトで有効になっています。DXF が有効になっているクラスターを v8.1.0 以降にアップグレードする場合は、アップグレード前に DXF を無効にします ( `tidb_enable_dist_task`を`OFF`に設定)。これにより、アップグレード中に`ADD INDEX`操作が発生してデータ インデックスの不整合が発生するのを回避できます。アップグレード後に、DXF を手動で有効にすることができます。
-   この変数は`tidb_ddl_distribute_reorg`から名前が変更されました。

### tidb_cloud_storage_uri <span class="version-mark">v7.4.0 の新機能</span> {#tidb-cloud-storage-uri-span-class-version-mark-new-in-v7-4-0-span}

> **注記：**
>
> 現在、 [グローバルソート](/tidb-global-sort.md)プロセスは TiDB ノードのコンピューティング リソースとメモリリソースを大量に消費しています。ユーザー ビジネス アプリケーションの実行中にオンラインでインデックスを追加するなどのシナリオでは、クラスターに新しい TiDB ノードを追加し、これらのノードの[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)変数を構成し、これらのノードに接続してタスクを作成することをお勧めします。このようにして、分散フレームワークはこれらのノードにタスクをスケジュールし、ワークロードを他の TiDB ノードから分離して、 `ADD INDEX`や`IMPORT INTO`などのバックエンド タスクの実行がユーザー ビジネス アプリケーションに与える影響を軽減します。

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `""`
-   この変数は、Amazon S3 クラウドstorageURI を指定して[グローバルソート](/tidb-global-sort.md)有効にするために使用されます。 [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md)を有効にした後、URI を構成し、storageにアクセスするために必要な権限を持つ適切なクラウドstorageパスを指すようにすることで、グローバル ソート機能を使用できます。詳細については、 [Amazon S3 URI 形式](/external-storage-uri.md#amazon-s3-uri-format)参照してください。
-   次のステートメントでは、グローバル ソート機能を使用できます。
    -   The [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) statement.
    -   The [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) statement for import jobs.

### tidb_ddl_エラーカウント制限 {#tidb-ddl-error-count-limit}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `512`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、DDL 操作が失敗した場合の再試行回数を設定するために使用されます。再試行回数がパラメータ値を超えると、間違った DDL 操作はキャンセルされます。

### tidb_ddl_flashback_concurrency <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-flashback-concurrency-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `64`
-   範囲: `[1, 256]`
-   This variable controls the concurrency of [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md).

### tidb_ddl_reorg_バッチサイズ {#tidb-ddl-reorg-batch-size}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `256`
-   範囲: `[32, 10240]`
-   単位: 行
-   この変数は、DDL 操作のフェーズ`re-organize`でバッチ サイズを設定するために使用されます。たとえば、TiDB が`ADD INDEX`操作を実行する場合、インデックス データは`tidb_ddl_reorg_worker_cnt` (数) の同時ワーカーによってバックフィルされる必要があります。各ワーカーは、インデックス データをバッチでバックフィルします。
    -   `tidb_ddl_enable_fast_reorg` `OFF`に設定すると、 `ADD INDEX`トランザクションとして実行されます。 `ADD INDEX`実行中に対象列に`UPDATE`や`REPLACE`などの更新操作が多数ある場合、バッチ サイズが大きいほどトランザクション競合の可能性が高くなります。 この場合、バッチ サイズを小さい値に設定することをお勧めします。 最小値は 32 です。
    -   If the transaction conflict does not exist, or if `tidb_ddl_enable_fast_reorg` is set to `ON`, you can set the batch size to a large value. This makes data backfilling faster but also increases the write pressure on TiKV. For a proper batch size, you also need to refer to the value of `tidb_ddl_reorg_worker_cnt`. See [オンライン ワークロードと`ADD INDEX`操作のインタラクション テスト](https://docs.pingcap.com/tidb/dev/online-workloads-and-add-index-operations) for reference.
    -   v8.3.0 以降、このパラメータは SESSION レベルでサポートされます。GLOBAL レベルでパラメータを変更しても、現在実行中の DDL ステートメントには影響しません。新しいセッションで送信された DDL にのみ適用されます。

### tidb_ddl_reorg_priority {#tidb-ddl-reorg-priority}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `PRIORITY_LOW`
-   `PRIORITY_HIGH` `PRIORITY_NORMAL`オプション: `PRIORITY_LOW`
-   この変数は、第`re-organize`フェーズで第`ADD INDEX`操作を実行する優先度を設定するために使用されます。
-   この変数の値は`PRIORITY_LOW` 、 `PRIORITY_NORMAL`または`PRIORITY_HIGH`に設定できます。

### tidb_ddl_reorg_max_write_speed <span class="version-mark">v8.5.0 の新機能</span> {#tidb-ddl-reorg-max-write-speed-span-class-version-mark-new-in-v8-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 1125899906842624]` (設定できる最大値は 1 PiB)
-   This variable limits the write bandwidth for each TiKV node and only takes effect when index creation acceleration is enabled (controlled by the [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630) variable). When the data size in your cluster is quite large (such as billions of rows), limiting the write bandwidth for index creation can effectively reduce the impact on application workloads.
-   デフォルト値`0`書き込み帯域幅の制限がないことを意味します。デフォルトの単位はバイト/秒です。 `'1GiB'`や`'256MiB'`などの形式で値を設定することもできます。

### tidb_ddl_reorg_worker_cnt {#tidb-ddl-reorg-worker-cnt}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、第`re-organize`フェーズでの DDL 操作の同時実行性を設定するために使用されます。
-   v8.3.0 以降、このパラメータは SESSION レベルでサポートされます。GLOBAL レベルでパラメータを変更しても、現在実行中の DDL ステートメントには影響しません。新しいセッションで送信された DDL にのみ適用されます。

### <code>tidb_enable_fast_create_table</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-tidb-enable-fast-create-table-code-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON` 。v8.5.0 より前では、デフォルト値は`OFF`です。
-   This variable is used to control whether to enable [TiDB 高速テーブル作成](/accelerated-table-creation.md).
-   Starting from v8.0.0, TiDB supports accelerating table creation by the [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) statement using `tidb_enable_fast_create_table`.
-   This variable is renamed from the variable [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760) that is introduced in v7.6.0. Starting from v8.0.0, `tidb_ddl_version` no longer takes effect.
-   TiDB v8.5.0 以降では、新しく作成されたクラスターに対して高速テーブル作成機能がデフォルトで有効になっており、 `tidb_enable_fast_create_table`が`ON`に設定されています。v8.4.0 以前のバージョンからアップグレードされたクラスターの場合、デフォルト値の`tidb_enable_fast_create_table`は変更されません。

### tidb_default_string_match_selectivity <span class="version-mark">v6.2.0 の新機能</span> {#tidb-default-string-match-selectivity-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: フロート
-   デフォルト値: `0.8`
-   範囲: `[0, 1]`
-   この変数は、行数を推定するときに、フィルター条件で`like` 、 `rlike` 、および`regexp`関数の関数の選択性を設定するために使用されます。この変数は、これらの関数の推定を支援するために TopN を有効にするかどうかも制御します。
-   TiDB は、統計を使用してフィルター条件の`like`推定しようとします。ただし、 `like`複雑な文字列に一致する場合、または`rlike`または`regexp`使用する場合、TiDB は統計を十分に使用できないことが多く、代わりにデフォルト値の`0.8`選択率として設定され、不正確な推定が発生します。
-   この変数は、前述の動作を変更するために使用されます。変数が`0`以外の値に設定されている場合、選択率は`0.8`ではなく指定された変数値になります。
-   If the variable is set to `0`, TiDB tries to evaluate using TopN in statistics to improve the accuracy and consider the NULL number in statistics when estimating the preceding three functions. The prerequisite is that statistics are collected when [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510) is set to `2`. Such evaluation might slightly affect the performance.
-   変数が`0.8`以外の値に設定されている場合、TiDB はそれに応じて`not like` 、 `not rlike` 、および`not regexp`の推定値を調整します。

### tidb_disable_txn_auto_retry {#tidb-disable-txn-auto-retry}

> **警告：**
>
> Starting from v8.0.0, this variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. As an alternative, when encountering optimistic transaction conflicts, you can capture the error and retry transactions in your application, or use the [悲観的なトランザクションモード](/pessimistic-transaction.md) instead.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、明示的な楽観的トランザクションの自動再試行を無効にするかどうかを設定するために使用されます。デフォルト値`ON`は、トランザクションが TiDB で自動的に再試行されず、 `COMMIT`ステートメントがアプリケーションレイヤーで処理する必要があるエラーを返す可能性があることを意味します。

    値を`OFF`に設定すると、TiDB は自動的にトランザクションを再試行し、 `COMMIT`ステートメントからのエラーが少なくなります。この変更を行うときは、更新が失われる可能性があるため注意してください。

    この変数は、TiDB で自動的にコミットされた暗黙的なトランザクションや内部的に実行されたトランザクションには影響しません。これらのトランザクションの最大再試行回数は、値`tidb_retry_limit`によって決まります。

    For more details, see [再試行の制限](/optimistic-transaction.md#limits-of-retry).

    <CustomContent platform="tidb">

    This variable only applies to optimistic transactions, not to pessimistic transactions. The number of retries for pessimistic transactions is controlled by [`max_retry_count`](/tidb-configuration-file.md#max-retry-count).

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は 256 です。

    </CustomContent>

### tidb_distsql_scan_concurrency {#tidb-distsql-scan-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `15`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `scan`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。
-   OLAP シナリオの場合、最大値はすべての TiKV ノードの CPU コアの数を超えてはなりません。
-   テーブルに多数のパーティションがある場合は、変数値を適切に減らして（スキャンするデータのサイズとスキャンの頻度によって決定）、TiKV がメモリ不足 (OOM) になるのを防ぐことができます。
-   `LIMIT`句のみを含む単純なクエリの場合、 `LIMIT`値が 100000 未満であれば、TiKV にプッシュダウンされたスキャン操作では、この変数の値が`1`として扱われ、実行効率が向上します。
-   `SELECT MAX/MIN(col) FROM ...`クエリの場合、 `col`列に`MAX(col)`または`MIN(col)`関数で必要な順序と同じ順序でソートされたインデックスがある場合、TiDB はクエリを`SELECT col FROM ... LIMIT 1`に書き換えて処理し、この変数の値も`1`として処理されます。たとえば、 `SELECT MIN(col) FROM ...`の場合、 `col`列に昇順のインデックスがある場合、TiDB はクエリを`SELECT col FROM ... LIMIT 1`に書き換えてインデックスの最初の行を直接読み取ることで、 `MIN(col)`値をすばやく取得できます。
-   For queries on the [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) table, this variable controls the concurrency for parsing the slow log file.

### tidb_dml_バッチサイズ {#tidb-dml-batch-size}

> **警告：**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [非トランザクションDML](/non-transactional-dml.md).

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: 行
-   この値が`0`より大きい場合、TiDB は`INSERT`などのステートメントを小さなトランザクションにバッチコミットします。これによりメモリ使用量が削減され、一括変更によって`txn-total-size-limit`に達しないようにすることができます。
-   ACID準拠を実現するのは値`0`のみです。これを他の値に設定すると、TiDB の原子性と分離性の保証が破られます。
-   この変数を機能させるには、 `tidb_enable_batch_dml` 、 `tidb_batch_insert`および`tidb_batch_delete`の少なくとも 1 つも有効にする必要があります。

> **注記：**
>
> Starting from v7.0.0, `tidb_dml_batch_size` no longer takes effect on the [`LOAD DATA`ステートメント](/sql-statements/sql-statement-load-data.md).

### tidb_dml_type <span class="version-mark">v8.0.0 の新機能</span> {#tidb-dml-type-span-class-version-mark-new-in-v8-0-0-span}

> **警告：**
>
> The bulk DML execution mode (`tidb_dml_type = "bulk"`) is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues). In the current version, when TiDB performs large transactions using the bulk DML mode, it might affect the memory usage and execution efficiency of TiCDC, TiFlash, and the resolved-ts module of TiKV, and might cause OOM issues. Additionally, BR might be blocked and fail to process when encountering locks. Therefore, it is not recommended to use this mode when these components or features are enabled.

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 文字列
-   デフォルト値: `"standard"`
-   `"bulk"`のオプション: `"standard"`
-   この変数は、DML ステートメントの実行モードを制御します。
    -   `"standard"`標準の DML 実行モードを示します。このモードでは、TiDB トランザクションはコミットされる前にメモリにキャッシュされます。このモードは、競合が発生する可能性のある同時実行性の高いトランザクション シナリオに適しており、デフォルトで推奨される実行モードです。
    -   `"bulk"`バルク DML 実行モードを示します。これは、大量のデータが書き込まれ、TiDB で過剰なメモリ使用が発生するシナリオに適しています。
        -   TiDB トランザクションの実行中、データは TiDBメモリに完全にキャッシュされるのではなく、メモリ使用量を削減し、書き込み負荷を軽減するために TiKV に継続的に書き込まれます。
        -   `"bulk"`モードの影響を受けるのは、 `INSERT` 、 `UPDATE` 、 `REPLACE` 、および`DELETE`ステートメントのみです。 `"bulk"`モードではパイプライン実行が行われるため、更新によって競合が発生した場合、 `INSERT IGNORE ... ON DUPLICATE UPDATE ...`を使用すると`Duplicate entry`エラーが発生する可能性があります。 一方、 `"standard"`モードでは、 `IGNORE`キーワードが設定されているため、このエラーは無視され、ユーザーに返されません。
        -   `"bulk"`モードは、大量の**データが競合なく書き込まれる**シナリオにのみ適しています。書き込み間の競合により大規模なトランザクションが失敗し、ロールバックされる可能性があるため、このモードは書き込みの競合の処理には効率的ではありません。
        -   `"bulk"` mode only takes effect on statements with auto-commit enabled, and requires the [`pessimistic-auto-commit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#pessimistic-auto-commit-new-in-v600) configuration item to be set to `false`.
        -   When using the `"bulk"` mode to execute statements, ensure that the [メタデータロック](/metadata-lock.md) remains enabled during the execution process.
        -   `"bulk"`モードは[一時テーブル](/temporary-tables.md)および[cached tables](/cached-tables.md)では使用できません。
        -   `"bulk"`モードは、外部キー制約チェックが有効になっている場合（ `foreign_key_checks = ON` ）、外部キーを含むテーブルや外部キーによって参照されるテーブルでは使用できません。
        -   In situations that the environment does not support or is incompatible with the `"bulk"` mode, TiDB falls back to the `"standard"` mode and returns a warning message. To verify if the `"bulk"` mode is used, you can check the `pipelined` field using [`tidb_last_txn_info`](#tidb_last_txn_info-new-in-v409). A `true` value indicates that the `"bulk"` mode is used.
        -   `"bulk"`モードで大規模なトランザクションを実行すると、トランザクションの継続時間が長くなる可能性があります。このモードのトランザクションの場合、トランザクション ロックの最大 TTL は[`max-txn-ttl`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#max-txn-ttl) ～ 24 時間のうち大きい方の値になります。また、トランザクションの実行時間が[`tidb_gc_max_wait_time`](#tidb_gc_max_wait_time-new-in-v610)で設定された値を超えると、GC によってトランザクションのロールバックが強制され、失敗する可能性があります。
        -   When TiDB executes transactions in the `"bulk"` mode, transaction size is not limited by the TiDB configuration item [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit).
        -   このモードは、パイプライン DML 機能によって実装されます。詳細な設計と GitHub の問題については、 [パイプライン化された DML](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2024-01-09-pipelined-DML.md)と[#50215](https://github.com/pingcap/tidb/issues/50215)参照してください。

### tidb_enable_1pc<span class="version-mark">バージョン5.0の新機能</span> {#tidb-enable-1pc-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、1 つのリージョンにのみ影響するトランザクションに対して 1 フェーズ コミット機能を有効にするかどうかを指定するために使用されます。よく使用される 2 フェーズ コミットと比較して、1 フェーズ コミットはトランザクション コミットのレイテンシーを大幅に削減し、スループットを向上させることができます。

> **注記：**
>
> -   デフォルト値`ON`は新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   このパラメータを有効にすると、1 フェーズ コミットがトランザクション コミットのオプション モードになるだけです。実際、トランザクション コミットの最も適切なモードは TiDB によって決定されます。

### tidb_enable_analyze_snapshot <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-analyze-snapshot-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `ANALYZE`実行するときに履歴データを読み取るか、最新のデータを読み取るかを制御します。この変数が`ON`に設定されている場合、 `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ります。この変数が`OFF`に設定されている場合、 `ANALYZE`最新のデータを読み取ります。
-   v5.2 より前は、 `ANALYZE`最新のデータを読み取ります。v5.2 から v6.1 までは、 `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ります。

> **警告：**
>
> `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取る場合、履歴データがガベージコレクションされるため、 `AUTO ANALYZE`の長い期間によって`GC life time is shorter than transaction duration`エラーが発生する可能性があります。

### tidb_enable_async_commit <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-async-commit-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、2 フェーズ トランザクション コミットの 2 番目のフェーズをバックグラウンドで非同期に実行するために、非同期コミット機能を有効にするかどうかを制御します。この機能を有効にすると、トランザクション コミットのレイテンシーを短縮できます。

> **注記：**
>
> -   デフォルト値`ON`は新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   このパラメータを有効にすると、非同期コミットがトランザクション コミットのオプション モードになるだけです。実際、トランザクション コミットの最も適切なモードは TiDB によって決定されます。

### tidb_enable_auto_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-auto-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB がバックグラウンド操作としてテーブル統計を自動的に更新するかどうかを決定します。
-   この設定は以前は`tidb.toml`オプション ( `performance.run-auto-analyze` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_enable_auto_analyze_priority_queue <span class="version-mark">v8.0.0 の新機能</span> {#tidb-enable-auto-analyze-priority-queue-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、優先キューを有効にして、統計を自動的に収集するタスクをスケジュールするかどうかを制御するために使用されます。この変数を有効にすると、TiDB は、新しく作成されたインデックスやパーティションが変更されたパーティション テーブルなど、収集する価値の高いテーブルの統計の収集を優先します。さらに、TiDB はヘルス スコアが低いテーブルを優先し、キューの先頭に配置します。

### tidb_enable_auto_increment_in_generated {#tidb-enable-auto-increment-in-generated}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、生成された列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定するために使用されます。

### tidb_enable_batch_dml {#tidb-enable-batch-dml}

> **警告：**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [非トランザクションDML](/non-transactional-dml.md).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨の batch-dml 機能を有効にするかどうかを制御します。この機能を有効にすると、特定のステートメントが複数のトランザクションに分割される可能性があります。これは非アトミックであり、注意して使用する必要があります。batch-dml を使用する場合は、操作対象のデータに対して同時操作がないことを確認する必要があります。この機能を動作させるには、 `tidb_batch_dml_size`に正の値を指定し、 `tidb_batch_insert`と`tidb_batch_delete`の少なくとも 1 つを有効にする必要があります。

### tidb_enable_cascades_planner {#tidb-enable-cascades-planner}

> **警告：**
>
> 現在、カスケード プランナーは実験的機能です。本番環境での使用はお勧めしません。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、カスケード プランナーを有効にするかどうかを制御するために使用されます。

### tidb_enable_check_constraint <span class="version-mark">v7.2.0 の新</span>機能 {#tidb-enable-check-constraint-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable is used to control whether to enable the [`CHECK`制約](/constraints.md#check) feature.

### tidb_enable_chunk_rpc <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-chunk-rpc-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサーで`Chunk`データ エンコーディング形式を有効にするかどうかを制御するために使用されます。

### tidb_enable_clustered_index <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-clustered-index-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `ON`
-   可能な`INT_ONLY` `ON` `OFF`
-   This variable is used to control whether to create the primary key as a [クラスター化インデックス](/clustered-indexes.md) by default. "By default" here means that the statement does not explicitly specify the keyword `CLUSTERED`/`NONCLUSTERED`. Supported values are `OFF`, `ON`, and `INT_ONLY`:
    -   `OFF` 、主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
    -   `ON` 、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
    -   `INT_ONLY`動作が構成項目`alter-primary-key`によって制御されることを示します。 `alter-primary-key` `true`に設定すると、すべての主キーはデフォルトで非クラスター化インデックスとして作成されます。 `false`に設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

### tidb_enable_ddl <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-ddl-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON`
-   この変数は、対応する TiDB インスタンスが DDL 所有者になれるかどうかを制御します。現在の TiDB クラスターに TiDB インスタンスが 1 つしかない場合は、それが DDL 所有者になることを防ぐことはできません。つまり、この変数を`OFF`に設定することはできません。

### tidb_enable_collect_execution_info {#tidb-enable-collect-execution-info}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable controls whether to record the execution information of each operator in the slow query log and whether to record the [インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md).

### tidb_enable_column_tracking <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-column-tracking-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> Starting from v8.3.0, this variable is deprecated. TiDB tracks predicate columns by default. For more information, see [`tidb_analyze_column_options`](#tidb_analyze_column_options-new-in-v830).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable controls whether to enable TiDB to collect `PREDICATE COLUMNS`. After enabling the collection, if you disable it, the information of previously collected `PREDICATE COLUMNS` is cleared. For details, see [いくつかの列の統計を収集する](/statistics.md#collect-statistics-on-some-columns).

### tidb_enable_enhanced_security {#tidb-enable-enhanced-security}

-   範囲: なし
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: `OFF`
-   この変数は、接続している TiDBサーバーでSecurity拡張モード (SEM) が有効になっているかどうかを示します。値を変更するには、TiDBサーバー構成ファイルの値`enable-sem`を変更し、TiDBサーバーを再起動する必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`
-   この変数は読み取り専用です。TiDB TiDB Cloudの場合、Security拡張モード (SEM) はデフォルトで有効になっています。

</CustomContent>

-   SEM is inspired by the design of systems such as [セキュリティ強化Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux). It reduces the abilities of users with the MySQL `SUPER` privilege and instead requires `RESTRICTED` fine-grained privileges to be granted as a replacement. These fine-grained privileges include:
    -   `RESTRICTED_TABLES_ADMIN` : `mysql`スキーマのシステム テーブルにデータを書き込み、 `information_schema`テーブルの機密列を表示する機能。
    -   `RESTRICTED_STATUS_ADMIN` : コマンド`SHOW STATUS`内の機密変数を確認する機能。
    -   `RESTRICTED_VARIABLES_ADMIN` : `SHOW [GLOBAL] VARIABLES`および`SET`の機密変数を表示および設定する機能。
    -   `RESTRICTED_USER_ADMIN` : 他のユーザーがユーザー アカウントを変更したり削除したりすることを防ぐ機能。

### tidb_enable_exchange_partition {#tidb-enable-exchange-partition}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable controls whether to enable the [`exchange partitions with tables`](/partitioned-table.md#partition-management) feature. The default value is `ON`, that is, `exchange partitions with tables` is enabled by default.
-   この変数は v6.3.0 以降では非推奨です。その値はデフォルト値`ON`に固定されます。つまり、デフォルトでは`exchange partitions with tables`が有効になります。

### tidb_enable_extended_stats {#tidb-enable-extended-stats}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable indicates whether TiDB can collect the extended statistic to guide the optimizer. See [拡張統計入門](/extended-statistics.md) for more information.

### tidb_enable_external_ts_read <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-external-ts-read-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   If this variable is set to `ON`, TiDB reads data with the timestamp specified by [`tidb_external_ts`](#tidb_external_ts-new-in-v640).

### tidb_external_ts <span class="version-mark">v6.4.0 の新機能</span> {#tidb-external-ts-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   If [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-new-in-v640) is set to `ON`, TiDB reads data with the timestamp specified by this variable.

### tidb_enable_fast_analyze {#tidb-enable-fast-analyze}

> **警告：**
>
> v7.5.0 以降では、この変数は非推奨です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計`Fast Analyze`機能を有効にするかどうかを設定するために使用されます。
-   統計`Fast Analyze`機能を有効にすると、TiDB は統計として約 10,000 行のデータをランダムにサンプリングします。データが不均等に分散されていたり、データ サイズが小さい場合、統計の精度は低くなります。これにより、間違ったインデックスを選択するなど、最適でない実行プランが発生する可能性があります。通常の`Analyze`ステートメントの実行時間が許容できる場合は、 `Fast Analyze`機能を無効にすることをお勧めします。

### tidb_enable_fast_table_check <span class="version-mark">v7.2.0 の新機能</span> {#tidb-enable-fast-table-check-span-class-version-mark-new-in-v7-2-0-span}

> **注記：**
>
> This variable does not work for [多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes) and prefix indexes.

-   範囲: セッション | グローバル
-   クラスターに永続化: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、チェックサムベースのアプローチを使用してテーブル内のデータとインデックスの整合性を迅速にチェックするかどうかを制御するために使用されます。デフォルト値`ON`は、この機能がデフォルトで有効になっていることを意味します。
-   When this variable is enabled, TiDB can execute the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement in a faster way.

### tidb_enable_foreign_key <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-foreign-key-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: v6.6.0 より前では、デフォルト値は`OFF`です。v6.6.0 以降では、デフォルト値は`ON`です。
-   この変数は、 `FOREIGN KEY`機能を有効にするかどうかを制御します。

### tidb_enable_gc_aware_memory_track {#tidb-enable-gc-aware-memory-track}

> **警告：**
>
> この変数は、TiDB のデバッグ用の内部変数です。将来のリリースで削除される可能性があります。この変数を設定し**ないでください**。

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、GC 対応メモリトラックを有効にするかどうかを制御します。

### tidb_enable_global_index <span class="version-mark">v7.6.0 の新機能</span> {#tidb-enable-global-index-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable controls whether to support creating [グローバルインデックス](/partitioned-table.md#global-indexes) for partitioned tables. When this variable is enabled, TiDB allows you to create unique indexes that **do not include all the columns used in the partition expressions** by specifying `GLOBAL` in the index definition.
-   This variable is deprecated since v8.4.0. Its value will be fixed to the default value `ON`, that is, [グローバルインデックス](/partitioned-table.md#global-indexes) is enabled by default.

### tidb_enable_lazy_cursor_fetch <span class="version-mark">v8.3.0 の新機能</span> {#tidb-enable-lazy-cursor-fetch-span-class-version-mark-new-in-v8-3-0-span}

> **警告：**
>
> The feature controlled by this variable is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

<CustomContent platform="tidb">

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   可能な値: `OFF` 、 `ON`
-   This variable controls the behavior of the [カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result) feature.
    -   カーソルフェッチが有効で、この変数が`OFF`に設定されている場合、TiDB はステートメント実行の開始時にすべてのデータを読み取り、そのデータを TiDB のメモリに格納し、後続のクライアント読み取り用にクライアントが指定した`FetchSize`に基づいてクライアントに返します。結果セットが大きすぎる場合、TiDB は結果を一時的にハードディスクに書き込むことがあります。
    -   カーソル フェッチが有効で、この変数が`ON`に設定されている場合、TiDB はすべてのデータを一度に TiDB ノードに読み込まず、クライアントがデータを取得するたびに TiDB ノードにデータを増分的に読み込みます。
-   この変数によって制御される機能には、次の制限があります。
    -   明示的なトランザクション内のステートメントはサポートされません。
    -   `TableReader` `IndexReader`演算子のみ`IndexLookUp`含む実行プランのみがサポートさ`Projection` `Selection` 。
    -   Lazy Cursor Fetch を使用するステートメントの場合、実行情報は[声明の概要](/statement-summary-tables.md)と[slow query log](/identify-slow-queries.md)に表示されません。
-   サポートされていないシナリオでは、この変数を`OFF`に設定した場合と同じ動作になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   可能な値: `OFF` 、 `ON`
-   This variable controls the behavior of the [カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result) feature.
    -   カーソルフェッチが有効で、この変数が`OFF`に設定されている場合、TiDB はステートメント実行の開始時にすべてのデータを読み取り、そのデータを TiDB のメモリに格納し、後続のクライアント読み取り用にクライアントが指定した`FetchSize`に基づいてクライアントに返します。結果セットが大きすぎる場合、TiDB は結果を一時的にハードディスクに書き込むことがあります。
    -   カーソル フェッチが有効で、この変数が`ON`に設定されている場合、TiDB はすべてのデータを一度に TiDB ノードに読み込まず、クライアントがデータを取得するたびに TiDB ノードにデータを増分的に読み込みます。
-   この変数によって制御される機能には、次の制限があります。
    -   明示的なトランザクション内のステートメントはサポートされません。
    -   `TableReader` `IndexReader`演算子のみ`IndexLookUp`含む実行プランのみがサポートさ`Projection` `Selection` 。
    -   Lazy Cursor Fetch を使用するステートメントの場合、実行情報は[声明の概要](/statement-summary-tables.md)と[slow query log](https://docs.pingcap.com/tidb/stable/identify-slow-queries)に表示されません。
-   サポートされていないシナリオでは、この変数を`OFF`に設定した場合と同じ動作になります。

</CustomContent>

### tidb_enable_non_prepared_plan_cache {#tidb-enable-non-prepared-plan-cache}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable controls whether to enable the [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md) feature.
-   この機能を有効にすると、追加のメモリと CPU オーバーヘッドが発生する可能性があり、すべての状況に適しているとは限りません。実際のシナリオに応じて、この機能を有効にするかどうかを判断してください。

### tidb_enable_non_prepared_plan_cache_for_dml <span class="version-mark">v7.1.0 の新機能</span> {#tidb-enable-non-prepared-plan-cache-for-dml-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> The non-prepared execution plan cache for DML statements is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF` 。
-   This variable controls whether to enable the [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md) feature for DML statements.

### tidb_enable_gogc_tuner <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-gogc-tuner-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、GOGC チューナーを有効にするかどうかを制御します。

### 履歴統計を有効にする {#tidb-enable-historical-stats}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF` 。v8.2.0 より前では、デフォルト値は`ON`です。
-   この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`で、履歴統計はデフォルトで無効になっていることを意味します。

### tidb_enable_historical_stats_for_capture {#tidb-enable-historical-stats-for-capture}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CAPTURE`でキャプチャされた情報にデフォルトで履歴統計が含まれるかどうかを制御します。デフォルト値`OFF` 、履歴統計がデフォルトで含まれないことを意味します。

### tidb_enable_index_merge <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-index-merge-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> -   TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードすると、実行プランの変更によるパフォーマンスの低下を防ぐため、この変数はデフォルトで無効になります。
>
> -   TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードした後も、この変数はアップグレード前の設定のままになります。
>
> -   v5.4.0 以降、新しくデプロイされた TiDB クラスターでは、この変数はデフォルトで有効になっています。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックス マージ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_index_merge_join {#tidb-enable-index-merge-join}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `IndexMergeJoin`演算子を有効にするかどうかを指定します。
-   この変数は TiDB の内部操作にのみ使用されます。調整することは**お勧めしません**。調整すると、データの正確性が影響を受ける可能性があります。

### tidb_enable_legacy_instance_scope <span class="version-mark">v6.0.0 の新機能</span> {#tidb-enable-legacy-instance-scope-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `SET SESSION`および`SET GLOBAL`構文を使用して`INSTANCE`スコープの変数を設定することを許可します。
-   このオプションは、TiDB の以前のバージョンとの互換性を保つためにデフォルトで有効になっています。

### tidb_enable_list_partition <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-list-partition-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `LIST (COLUMNS) TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。
-   This variable is deprecated since v8.4.0. Its value will be fixed to the default value `ON`, that is, [List パーティショニング](/partitioned-table.md#list-partitioning) is enabled by default.

### tidb_enable_local_txn {#tidb-enable-local-txn}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は未リリースの機能に使用されます。**変数値を変更しないでください**。

### tidb_enable_metadata_lock <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-metadata-lock-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable is used to set whether to enable the [メタデータロック](/metadata-lock.md) feature. Note that when setting this variable, you need to make sure that there are no running DDL statements in the cluster. Otherwise, the data might be incorrect or inconsistent.

### tidb_enable_mutation_checker <span class="version-mark">v6.0.0 の新機能</span> {#tidb-enable-mutation-checker-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable is used to control whether to enable TiDB mutation checker, which is a tool used to check consistency between data and indexes during the execution of DML statements. If the checker returns an error for a statement, TiDB rolls back the execution of the statement. Enabling this variable causes a slight increase in CPU usage. For more information, see [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md).
-   v6.0.0 以降のバージョンの新しいクラスターの場合、デフォルト値は`ON`です。v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_enable_new_cost_interface <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-new-cost-interface-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB v6.2.0 は、以前のコスト モデルの実装をリファクタリングします。この変数は、リファクタリングされたコスト モデルの実装を有効にするかどうかを制御します。
-   リファクタリングされたコスト モデルでは以前と同じコスト式が使用され、プランの決定は変更されないため、この変数はデフォルトで有効になっています。
-   クラスターが v6.1 から v6.2 にアップグレードされた場合、この変数は`OFF`のままなので、手動で有効にすることをお勧めします。クラスターが v6.1 より前のバージョンからアップグレードされた場合、この変数はデフォルトで`ON`に設定されます。

### tidb_enable_new_only_full_group_by_check <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-new-only-full-group-by-check-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable controls the behavior when TiDB performs the `ONLY_FULL_GROUP_BY` check. For detailed information about `ONLY_FULL_GROUP_BY`, see the [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by). In v6.1.0, TiDB handles this check more strictly and correctly.
-   バージョンのアップグレードによって発生する可能性のある互換性の問題を回避するために、この変数のデフォルト値は v6.1.0 では`OFF`になっています。

### tidb_enable_noop_functions <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-noop-functions-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   可能な`WARN` `ON` `OFF`
-   デフォルトでは、まだ実装されていない機能の構文を使用しようとすると、TiDB はエラーを返します。変数値が`ON`に設定されている場合、TiDB はそのような使用できない機能のケースを黙って無視します。これは、SQL コードを変更できない場合に役立ちます。
-   `noop`関数を有効にすると、次の動作が制御されます。
    -   `LOCK IN SHARE MODE`構文
    -   `SQL_CALC_FOUND_ROWS`構文
    -   `START TRANSACTION READ ONLY`と`SET TRANSACTION READ ONLY`構文
    -   `tx_read_only` `transaction_read_only` `sql_auto_is_null` `offline_mode` `super_read_only` `read_only`
    -   `GROUP BY <expr> ASC|DESC`構文

> **警告：**
>
> 安全であると考えられるのは、デフォルト値の`OFF`のみです`tidb_enable_noop_functions=1`に設定すると、TiDB がエラーを出さずに特定の構文を無視することを許可するため、アプリケーションで予期しない動作が発生する可能性があります。たとえば、構文`START TRANSACTION READ ONLY`は許可されますが、トランザクションは読み取り/書き込みモードのままになります。

### tidb_enable_noop_variables <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-noop-variables-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `ON`
-   変数値を`OFF`に設定すると、TiDB は次のように動作します。
    -   `SET`使用して`noop`変数を設定すると、TiDB は`"setting *variable_name* has no effect in TiDB"`警告を返します。
    -   `SHOW [SESSION | GLOBAL] VARIABLES`の結果には`noop`変数は含まれません。
    -   `SELECT`使用して`noop`変数を読み取ると、TiDB は`"variable *variable_name* has no effect in TiDB"`警告を返します。
-   TiDB インスタンスが`noop`変数を設定して読み取ったかどうかを確認するには、 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;`ステートメントを使用できます。

### tidb_enable_null_aware_anti_join <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-null-aware-anti-join-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   デフォルト値: v7.0.0 より前では、デフォルト値は`OFF`です。v7.0.0 以降では、デフォルト値は`ON`です。
-   タイプ: ブール値
-   この変数は、特殊なセット演算子`NOT IN`と`!= ALL`によって導かれるサブクエリによって ANTI JOIN が生成される場合に、TiDB が Null Aware Hash Join を適用するかどうかを制御します。
-   以前のバージョンから v7.0.0 以降のクラスターにアップグレードすると、この機能は自動的に有効になり、この変数は`ON`に設定されます。

### tidb_enable_outer_join_reorder <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-outer-join-reorder-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `ON`
-   Since v6.1.0, the [結合したテーブルの再配置](/join-reorder.md) algorithm of TiDB supports Outer Join. This variable controls whether TiDB enables the Join Reorder's support for Outer Join.
-   クラスターが以前のバージョンの TiDB からアップグレードされる場合は、次の点に注意してください。

    -   アップグレード前の TiDB バージョンが v6.1.0 より前の場合、アップグレード後のこの変数のデフォルト値は`ON`なります。
    -   アップグレード前の TiDB バージョンが v6.1.0 以降の場合、アップグレード後の変数のデフォルト値はアップグレード前の値に従います。

### <code>tidb_enable_inl_join_inner_multi_pattern</code> <span class="version-mark">v7.0.0 の新機能</span> {#code-tidb-enable-inl-join-inner-multi-pattern-code-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `ON` 。v8.3.0 以前のバージョンではデフォルト値は`OFF`です。
-   この変数は、内部テーブルに`Selection` 、 `Aggregation` 、または`Projection`の演算子がある場合に、インデックス結合がサポートされるかどうかを制御します。デフォルト値`OFF` 、このシナリオではインデックス結合がサポートされないことを意味します。
-   TiDB クラスターを v7.0.0 より前のバージョンから v8.4.0 以降にアップグレードする場合、この変数はデフォルトで`OFF`に設定され、このシナリオではインデックス結合がサポートされていないことを示します。

### tidb_enable_instance_plan_cache <span class="version-mark">v8.4.0 の新機能</span> {#tidb-enable-instance-plan-cache-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> Currently, Instance Plan Cache is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、インスタンス プラン キャッシュ機能を有効にするかどうかを制御します。この機能はインスタンス レベルの実行プラン キャッシュを実装します。これにより、同じ TiDB インスタンス内のすべてのセッションが実行プラン キャッシュを共有できるようになり、メモリ使用率が向上します。インスタンス プラン キャッシュを有効にする前に、セッション レベル[準備された実行計画キャッシュ](/sql-prepared-plan-cache.md)と[Non-prepared execution plan cache](/sql-non-prepared-plan-cache.md)無効にすることをお勧めします。

### tidb_enable_ordered_result_mode {#tidb-enable-ordered-result-mode}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   最終出力結果を自動的にソートするかどうかを指定します。
-   たとえば、この変数を有効にすると、TiDB は`SELECT a, MAX(b) FROM t GROUP BY a` `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`として処理します。

### tidb_enable_paging <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-paging-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサ要求を送信するためにページング方式を使用するかどうかを制御します。TiDB バージョン [v5.4.0、v6.2.0) の場合、この変数は`IndexLookup`演算子にのみ有効です。v6.2.0 以降の場合、この変数はグローバルに適用されます。v6.4.0 以降、この変数のデフォルト値は`OFF`から`ON`に変更されます。
-   ユーザーシナリオ:

    -   すべての OLTP シナリオでは、ページング方式を使用することをお勧めします。
    -   For read queries that use `IndexLookup` and `Limit` and that `Limit` cannot be pushed down to `IndexScan`, there might be high latency for the read queries and high usage for TiKV `Unified read pool CPU`. In such cases, because the `Limit` operator only requires a small set of data, if you set [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540) to `ON`, TiDB processes less data, which reduces query latency and resource consumption.
    -   In scenarios such as data export using [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) and full table scan, enabling paging can effectively reduce the memory consumption of TiDB processes.

> **注記：**
>
> TiFlashの代わりに TiKV がstorageエンジンとして使用される OLAP シナリオでは、ページングを有効にすると、場合によってはパフォーマンスが低下する可能性があります。低下が発生した場合は、この変数を使用してページングを無効にするか、 [`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-new-in-v620)および[`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-new-in-v630)変数を使用してページング サイズの行の範囲を調整することを検討してください。

### tidb_enable_parallel_apply <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-parallel-apply-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `Apply`演算子の同時実行を有効にするかどうかを制御します。同時実行の数は`tidb_executor_concurrency`変数によって制御されます。5 `Apply`は相関サブクエリを処理し、デフォルトでは同時実行がないため、実行速度は遅くなります。この変数値を`1`に設定すると、同時実行が増加し、実行速度が向上します。現在、 `Apply`の同時実行はデフォルトで無効になっています。

### tidb_enable_parallel_hashagg_spill <span class="version-mark">v8.0.0 の新機能</span> {#tidb-enable-parallel-hashagg-spill-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB が並列 HashAgg アルゴリズムのディスク スピルをサポートするかどうかを制御します。 `ON`の場合、HashAgg 演算子は、並列条件下でのメモリ使用量に基づいてデータ スピルを自動的にトリガーできるため、パフォーマンスとデータ スループットのバランスが取れます。 この変数を`OFF`に設定することはお勧めしません。 v8.2.0 以降では、これを`OFF`に設定するとエラーが報告されます。 この変数は、将来のリリースでは非推奨になります。

### tidb_enable_pipelined_window_function パイプラインウィンドウ関数を有効にする {#tidb-enable-pipelined-window-function}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable specifies whether to use the pipeline execution algorithm for [ウィンドウ関数](/functions-and-operators/window-functions.md).

### tidb_enable_plan_cache_for_param_limit <span class="version-mark">v6.6.0 の新機能</span> {#tidb-enable-plan-cache-for-param-limit-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 プリペアドプランキャッシュ が、変数を`LIMIT`パラメータ ( `LIMIT ?` ) として持つ実行プランをキャッシュするかどうかを制御します。デフォルト値は`ON`で、 プリペアドプランキャッシュ がそのような実行プランのキャッシュをサポートすることを意味します。Prepared プリペアドプランキャッシュ は、 10000 を超える変数を持つ実行プランのキャッシュをサポートしないことに注意してください。

### tidb_enable_plan_cache_for_subquery <span class="version-mark">v7.0.0 の新機能</span> {#tidb-enable-plan-cache-for-subquery-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュがサブクエリを含むクエリをキャッシュするかどうかを制御します。

### tidb_enable_plan_replayer_capture {#tidb-enable-plan-replayer-capture}

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CAPTURE`機能を有効にするかどうかを制御します。デフォルト値`OFF` 、 `PLAN REPLAYER CAPTURE`機能を無効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable controls whether to enable the [`PLAN REPLAYER CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans). The default value `ON` means to enable the `PLAN REPLAYER CAPTURE` feature.

</CustomContent>

### tidb_enable_plan_replayer_continuous_capture <span class="version-mark">v7.0.0 の新機能</span> {#tidb-enable-plan-replayer-continuous-capture-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CONTINUOUS CAPTURE`機能を有効にするかどうかを制御します。デフォルト値`OFF` 、機能を無効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable controls whether to enable the [`PLAN REPLAYER CONTINUOUS CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-continuous-capture). The default value `OFF` means to disable the feature.

</CustomContent>

### tidb_enable_prepared_plan_cache <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-prepared-plan-cache-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `ON`
-   Determines whether to enable [プリペアドプランキャッシュ](/sql-prepared-plan-cache.md). When it is enabled, the execution plans of `Prepare` and `Execute` are cached so that the subsequent executions skip optimizing the execution plans, which brings performance improvement.
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-prepared-plan-cache-memory-monitor-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `ON`
-   This variable controls whether to count the memory consumed by the execution plans cached in the Prepared Plan Cache. For details, see [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache).

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">v5.3.0 の新機能</span> {#tidb-enable-pseudo-for-outdated-stats-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計が古くなった場合にテーブルの統計を使用する際のオプティマイザの動作を制御します。

<CustomContent platform="tidb">

-   The optimizer determines whether the statistics of a table is outdated in this way: since the last time `ANALYZE` is executed on a table to get the statistics, if 80% of the table rows are modified (the modified row count divided by the total row count), the optimizer determines that the statistics of this table is outdated. You can change this ratio using the [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) configuration.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   オプティマイザは、次のようにしてテーブルの統計が古くなっているかどうかを判断します。統計を取得するためにテーブルで最後に`ANALYZE`実行されて以降、テーブル行の 80% が変更されている場合 (変更された行数を合計行数で割った値)、オプティマイザはこのテーブルの統計が古くなっていると判断します。

</CustomContent>

-   デフォルトでは (変数値`OFF` )、テーブルの統計が古くなった場合、オプティマイザは引き続きテーブルの統計を使用します。変数値を`ON`に設定すると、オプティマイザは、合計行数を除いてテーブルの統計が信頼できないと判断します。次に、オプティマイザは疑似統計を使用します。
-   テーブル上のデータが頻繁に変更され、そのテーブルに対して`ANALYZE`時間内に実行されない場合、実行プランを安定させるために、変数値を`OFF`に設定することをお勧めします。

### tidb_enable_rate_limit_action {#tidb-enable-rate-limit-action}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、データを読み取る演算子の動的メモリ制御機能を有効にするかどうかを制御します。デフォルトでは、この演算子は、データを読み取るために許可される最大スレッド数[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)を有効にします。単一の SQL ステートメントのメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超えると、データを読み取る演算子は 1 つのスレッドを停止します。

<CustomContent platform="tidb">

-   データを読み取る演算子に残っているスレッドが 1 つだけであり、単一の SQL ステートメントのメモリ使用量が継続的に[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超える場合、この SQL ステートメントは[spilling data to disk](/system-variables.md#tidb_enable_tmp_storage_on_oom)などの他のメモリ制御動作をトリガーします。
-   この変数は、SQL ステートメントがデータを読み取るだけの場合に、メモリ使用量を効果的に制御します。コンピューティング操作 (結合操作や集計操作など) が必要な場合は、メモリ使用量が`tidb_mem_quota_query`によって制御されない可能性があり、OOM のリスクが高まります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   When the operator that reads data has only one thread left and the memory usage of a single SQL statement continues to exceed [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), this SQL statement triggers other memory control behaviors, such as spilling data to disk.

</CustomContent>

### tidb_enable_resource_control <span class="version-mark">v6.6.0 の新機能</span> {#tidb-enable-resource-control-span-class-version-mark-new-in-v6-6-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `ON`
-   タイプ: ブール値
-   This variable is a switch for [リソース制御機能](/tidb-resource-control.md). When this variable is set to `ON`, the TiDB cluster can isolate application resources based on resource groups.

### tidb_enable_reuse_chunk <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-reuse-chunk-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `ON`
-   `ON`のオプション: `OFF`
-   この変数は、TiDB がチャンク オブジェクト キャッシュを有効にするかどうかを制御します。値が`ON`の場合、TiDB はキャッシュされたチャンク オブジェクトを優先的に使用し、要求されたオブジェクトがキャッシュにない場合にのみシステムから要求します。値が`OFF`場合、TiDB はシステムからチャンク オブジェクトを直接要求します。

### tidb_enable_shared_lock_promotion <span class="version-mark">v8.3.0 の新機能</span> {#tidb-enable-shared-lock-promotion-span-class-version-mark-new-in-v8-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、共有ロックを排他ロックにアップグレードする機能を有効にするかどうかを制御します。TiDB はデフォルトで`SELECT LOCK IN SHARE MODE`サポートしていません。変数値が`ON`の場合、TiDB は`SELECT LOCK IN SHARE MODE`ステートメントを`SELECT FOR UPDATE`にアップグレードし、悲観的ロックを追加しようとします。この変数のデフォルト値は`OFF`で、共有ロックを排他ロックにアップグレードする機能が無効であることを意味します。
-   Enabling this variable takes effect on the `SELECT LOCK IN SHARE MODE` statement, regardless of whether [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) is enabled or not.

### 遅いログを有効にする {#tidb-enable-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_tmp_storage_on_oom {#tidb-enable-tmp-storage-on-oom}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `ON`
-   `ON`のオプション: `OFF`
-   Controls whether to enable the temporary storage for some operators when a single SQL statement exceeds the memory quota specified by the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query).
-   v6.3.0 より前では、TiDB 構成項目`oom-use-tmp-storage`を使用してこの機能を有効または無効にできます。クラスターを v6.3.0 以降のバージョンにアップグレードすると、TiDB クラスターはこの変数を`oom-use-tmp-storage`の値を使用して自動的に初期化します。その後、値`oom-use-tmp-storage`を変更しても有効になり**ません**。

### tidb_enable_stats_owner <span class="version-mark">v8.4.0 の新機能</span> {#tidb-enable-stats-owner-span-class-version-mark-new-in-v8-4-0-span}

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON`
-   This variable controls whether the corresponding TiDB instance can run [自動統計更新](/statistics.md#automatic-update) tasks. If there is only one TiDB instance in the current TiDB cluster, you cannot disable automatic statistics update on this instance, which means you cannot set this variable to `OFF`.

### tidb_enable_stmt_summary <span class="version-mark">v3.0.4 の新機能</span> {#tidb-enable-stmt-summary-span-class-version-mark-new-in-v3-0-4-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ステートメント サマリー機能を有効にするかどうかを制御するために使用されます。有効にすると、時間消費などの SQL 実行情報が`information_schema.STATEMENTS_SUMMARY`システム テーブルに記録され、SQL パフォーマンスの問題を特定してトラブルシューティングできるようになります。

### tidb_enable_strict_double_type_check <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-strict-double-type-check-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、タイプ`DOUBLE`の無効な定義でテーブルを作成できるかどうかを制御するために使用されます。この設定は、タイプの検証がそれほど厳格ではなかった以前のバージョンの TiDB からのアップグレード パスを提供することを目的としています。
-   デフォルト値`ON`は MySQL と互換性があります。

たとえば、浮動小数点型の精度は保証されていないため、型`DOUBLE(10)`は無効とみなされます。 `tidb_enable_strict_double_type_check` `OFF`に変更すると、次のテーブルが作成されます。

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
> MySQL では`FLOAT`の型の精度が許可されているため、この設定は型`DOUBLE`にのみ適用されます。この動作は MySQL 8.0.17 以降では非推奨であり、 `FLOAT`または`DOUBLE`型の精度を指定することは推奨されません。

### tidb_enable_table_partition {#tidb-enable-table-partition}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `ON`
-   This variable is deprecated since v8.4.0. Its value will be fixed to the default value `ON`, that is, [テーブルパーティション](/partitioned-table.md) is enabled by default.

### tidb_enable_telemetry <span class="version-mark">v4.0.2 で新規、v8.1.0 で非推奨</span> {#tidb-enable-telemetry-span-class-version-mark-new-in-v4-0-2-and-deprecated-in-v8-1-0-span}

> **警告：**
>
> v8.1.0 以降では、TiDB のテレメトリ機能が削除され、この変数は機能しなくなりました。これは、以前のバージョンとの互換性のためだけに保持されています。

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   v8.1.0 より前では、この変数は TiDB でテレメトリ収集を有効にするかどうかを制御します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-tiflash-read-for-write-stmt-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `INSERT` 、 `DELETE` 、および`UPDATE`を含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできるかどうかを制御します。例:

    -   `SELECT` queries in `INSERT INTO SELECT` statements (typical usage scenario: [TiFlashクエリ結果の具体化](/tiflash/tiflash-results-materialization.md))
    -   `UPDATE`文と`DELETE`文の`WHERE`条件フィルタリング
-   v7.1.0 以降、この変数は非推奨です。 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)場合、オプティマイザーは、 [SQL mode](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定します。TiDB では、現在のセッションの[SQL モード](/sql-mode.md)が厳密でない場合にのみ、 `INSERT` 、 `DELETE` 、および`UPDATE` ( `INSERT INTO SELECT`など) を含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできることに注意してください。つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`と`STRICT_ALL_TABLES`含まれません。

### tidb_enable_top_sql <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-top-sql-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   This variable is used to control whether to enable the [Top SQL](/dashboard/top-sql.md) feature.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable is used to control whether to enable the [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) feature.

</CustomContent>

### tidb_enable_tso_follower_proxy <span class="version-mark">v5.3.0 の新機能</span> {#tidb-enable-tso-follower-proxy-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TSOFollowerプロキシ機能を有効にするかどうかを制御します。値が`OFF`の場合、TiDB は PD リーダーからのみ TSO を取得します。値が`ON`の場合、TiDB は TSO の要求をすべての PD サーバーに均等に分散し、PD フォロワーも TSO 要求を処理できるため、PD リーダーの CPU 負荷が軽減されます。
-   TSOFollowerプロキシを有効にするシナリオ:
    -   TSO 要求の負荷が高いため、PD リーダーの CPU がボトルネックになり、TSO RPC 要求のレイテンシーが高くなります。
    -   The TiDB cluster has many TiDB instances, and increasing the value of [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530) cannot alleviate the high latency issue of TSO RPC requests.

> **注記：**
>
> -   PD リーダーの CPU 使用率のボトルネック以外の理由 (ネットワークの問題など) で TSO RPCレイテンシーが増加するとします。この場合、TSOFollowerプロキシを有効にすると、TiDB での実行レイテンシーが増加し、クラスターの QPS パフォーマンスに影響する可能性があります。
> -   この機能は[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)と互換性がありません。この機能を有効にすると、 [`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)機能しません。

### tidb_enable_unsafe_substitute <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-unsafe-substitute-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable controls whether to replace expressions with generated columns in an unsafe way. The default value is `OFF`, which means that unsafe replacement is disabled by default. For more details, see [生成された列](/generated-columns.md).

### tidb_enable_vectorized_expression <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-vectorized-expression-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ベクトル化された実行を有効にするかどうかを制御するために使用されます。

### tidb_enable_window_function {#tidb-enable-window-function}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   This variable is used to control whether to enable the support for [ウィンドウ関数](/functions-and-operators/window-functions.md). Note that window functions might use reserved keywords. This might cause SQL statements that can be executed normally to fail to be parsed after TiDB is upgraded. In this case, you can set `tidb_enable_window_function` to `OFF`.

### <code>tidb_enable_row_level_checksum</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-enable-row-level-checksum-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   This variable is used to control whether to enable the [単一行データの TiCDC データ整合性検証](/ticdc/ticdc-integrity-check.md) feature.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable is used to control whether to enable the [単一行データの TiCDC データ整合性検証](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check) feature.

</CustomContent>

-   You can use the [`TIDB_ROW_CHECKSUM()`](/functions-and-operators/tidb-functions.md#tidb_row_checksum) function to get the checksum value of a row.

### tidb_enforce_mpp <span class="version-mark">v5.1 の新機能</span> {#tidb-enforce-mpp-span-class-version-mark-new-in-v5-1-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   To change this default value, modify the [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) configuration value.

</CustomContent>

-   オプティマイザのコスト見積もりを無視し、クエリ実行に TiFlash の MPP モードを強制的に使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF` 。MPP モードが強制的に使用されないことを意味します (デフォルト)。
    -   `1`または`ON`場合、コスト推定は無視され、MPP モードが強制的に使用されます。この設定は`tidb_allow_mpp=true`場合にのみ有効になることに注意してください。

MPP is a distributed computing framework provided by the TiFlash engine, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. For details about the selection of the MPP mode, refer to [MPPモードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode).

### tidb_evolve_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable is used to control whether to enable the baseline evolution feature. For detailed introduction or usage , see [ベースライン進化](/sql-plan-management.md#baseline-evolution).
-   ベースラインの進化がクラスターに与える影響を軽減するには、次の構成を使用します。
    -   各実行プランの最大実行時間を制限するには`tidb_evolve_plan_task_max_time`設定します。デフォルト値は 600 秒です。
    -   時間ウィンドウを制限するには、 `tidb_evolve_plan_task_start_time`と`tidb_evolve_plan_task_end_time`設定します。デフォルト値はそれぞれ`00:00 +0000`と`23:59 +0000`です。

### tidb_evolve_plan_task_end_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-end-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、1 日のベースライン進化の終了時刻を設定するために使用されます。

### tidb_evolve_plan_task_max_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-max-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `600`
-   範囲: `[-1, 9223372036854775807]`
-   単位: 秒
-   この変数は、ベースライン進化機能の各実行プランの最大実行時間を制限するために使用されます。

### tidb_evolve_plan_task_start_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-start-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、1 日のベースライン進化の開始時刻を設定するために使用されます。

### tidb_executor_concurrency <span class="version-mark">v5.0 の新機能</span> {#tidb-executor-concurrency-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `5`
-   範囲: `[1, 256]`
-   単位: スレッド

この変数は、次の SQL 演算子の同時実行性を (1 つの値に) 設定するために使用されます。

-   `index lookup`
-   `index lookup join`
-   `hash join`
-   `hash aggregation` (第`partial`フェーズと`final`フェーズ)
-   `window`
-   `projection`
-   `sort`

`tidb_executor_concurrency`管理を容易にするために、次の既存のシステム変数が全体的に組み込まれています。

-   `tidb_index_lookup_concurrency`
-   `tidb_index_lookup_join_concurrency`
-   `tidb_hash_join_concurrency`
-   `tidb_hashagg_partial_concurrency`
-   `tidb_hashagg_final_concurrency`
-   `tidb_projection_concurrency`
-   `tidb_window_concurrency`

v5.0 以降では、上記のシステム変数を個別に変更することができます (非推奨の警告が返されます)。変更は対応する単一の演算子にのみ影響します。その後、 `tidb_executor_concurrency`使用して演算子の同時実行性を変更した場合、個別に変更された演算子は影響を受けません。 `tidb_executor_concurrency`使用してすべての演算子の同時実行性を変更する場合は、上記のすべての変数の値を`-1`に設定できます。

以前のバージョンから v5.0 にアップグレードされたシステムの場合、上記の変数の値を変更していない場合 (つまり、 `tidb_hash_join_concurrency`値が`5`で、残りの値が`4`場合)、これらの変数によって以前に管理されていた演算子の同時実行性は、自動的に`tidb_executor_concurrency`によって管理されます。これらの変数のいずれかを変更した場合、対応する演算子の同時実行性は、変更された変数によって引き続き制御されます。

### tidb_expensive_query_time_threshold {#tidb-expensive-query-time-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 2147483647]`
-   単位: 秒
-   この変数は、コストの高いクエリ ログを出力するかどうかを決定するしきい値を設定するために使用されます。コストの高いクエリ ログと低速なクエリ ログの違いは次のとおりです。
    -   ステートメントの実行後にスロー ログが出力されます。
    -   コストのかかるクエリ ログには、実行時間がしきい値を超えている実行中のステートメントとその関連情報が出力されます。

### tidb_expensive_txn_time_threshold <span class="version-mark">v7.2.0 の新機能</span> {#tidb-expensive-txn-time-threshold-span-class-version-mark-new-in-v7-2-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `600`
-   範囲: `[60, 2147483647]`
-   単位: 秒
-   この変数は、高価なトランザクションをログに記録するためのしきい値を制御します。デフォルトでは 600 秒です。トランザクションの期間がしきい値を超え、トランザクションがコミットもロールバックもされない場合、そのトランザクションは高価なトランザクションとみなされ、ログに記録されます。

### tidb_force_priority {#tidb-force-priority}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `NO_PRIORITY`
-   可能`LOW_PRIORITY` `DELAYED` `HIGH_PRIORITY` `NO_PRIORITY`
-   この変数は、TiDBサーバーで実行されるステートメントのデフォルトの優先度を変更するために使用されます。使用例としては、OLAP クエリを実行している特定のユーザーが、OLTP クエリを実行しているユーザーよりも低い優先度を受け取るようにすることが挙げられます。
-   デフォルト値`NO_PRIORITY` 、ステートメントの優先順位が強制的に変更されないことを意味します。

> **注記：**
>
> v6.6.0 以降、TiDB は[リソース管理](/tidb-resource-control.md)サポートします。この機能を使用すると、異なるリソース グループで異なる優先度の SQL ステートメントを実行できます。これらのリソース グループに適切なクォータと優先度を構成することで、異なる優先度の SQL ステートメントのスケジュール制御を向上させることができます。リソース制御を有効にすると、ステートメントの優先度は適用されなくなります。異なる SQL ステートメントのリソース使用を管理するには、 [Resource Control](/tidb-resource-control.md)使用することをお勧めします。

### tidb_gc_concurrency <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-concurrency-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `-1`または`[1, 256]`
-   単位: スレッド
-   この変数は、 [Garbage Collection (GC)](/garbage-collection-overview.md)プロセスの[ロックを解決する](/garbage-collection-overview.md#resolve-locks)番目のステップでの同時スレッドの数を制御します。
-   Starting from v8.3.0, this variable also controls the number of concurrent threads during the [範囲を削除](/garbage-collection-overview.md#delete-ranges) step of the GC process.
-   デフォルトでは、この変数は`-1`に設定されており、TiDB はワークロードに基づいて適切なスレッド数を自動的に決定します。
-   この変数が`[1, 256]`の範囲の数値に設定されている場合:
    -   ロックの解決では、この変数に設定された値がスレッド数として直接使用されます。
    -   削除範囲では、この変数に設定された値の 4 分の 1 がスレッド数として使用されます。

### tidb_gc_enable <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-enable-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiKV のガベージコレクションを有効にします。ガベージコレクションを無効にすると、古いバージョンの行が削除されなくなるため、システムのパフォーマンスが低下します。

### tidb_gc_life_time <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-life-time-span-class-version-mark-new-in-v5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: TiDBセルフマネージドの場合は`[10m0s, 8760h0m0s]` [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) `[10m0s, 168h0m0s]`は[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   各 GC でデータが保持される時間制限 (Go Duration 形式)。GC が発生すると、現在の時刻からこの値を引いた値が安全ポイントになります。

> **注記：**
>
> -   頻繁に更新されるシナリオでは、 `tidb_gc_life_time`に大きな値 (日数または月数) を指定すると、次のような潜在的な問題が発生する可能性があります。
>     -   より大きなstorageの使用
>     -   大量の履歴データは、特に`select count(*) from t`のような範囲クエリの場合、ある程度パフォーマンスに影響を与える可能性があります。
> -   `tidb_gc_life_time`より長く実行されているトランザクションがある場合、GC 中、このトランザクションが実行を継続できるように`start_ts`以降のデータが保持されます。たとえば、 `tidb_gc_life_time` 10 分に設定されている場合、実行中のすべてのトランザクションのうち、最も早く開始されたトランザクションが 15 分間実行されているため、GC は最近の 15 分間のデータを保持します。

### tidb_gc_max_wait_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-gc-max-wait-time-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `86400`
-   範囲: `[600, 31536000]`
-   単位: 秒
-   この変数は、アクティブなトランザクションが GC セーフ ポイントをブロックする最大時間を設定するために使用されます。GC の各時間中、セーフ ポイントはデフォルトで進行中のトランザクションの開始時間を超えません。アクティブなトランザクションの実行時間がこの変数値を超えない場合、実行時間がこの値を超えるまで GC セーフ ポイントはブロックされます。

### tidb_gc_run_interval <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-run-interval-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   GC間隔をGo Durationの形式で指定します。たとえば、 `"1h30m"`などです`"15m"`

### tidb_gc_scan_lock_mode <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-scan-lock-mode-span-class-version-mark-new-in-v5-0-span}

> **警告：**
>
> 現在、Green GC は実験的機能です。本番環境での使用はお勧めしません。

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `LEGACY`
-   可能な値: `PHYSICAL` 、 `LEGACY`
    -   `LEGACY` : 古いスキャン方法を使用します。つまり、Green GC を無効にします。
    -   `PHYSICAL` : 物理スキャン方式を使用します。つまり、Green GC を有効にします。

<CustomContent platform="tidb">

-   This variable specifies the way of scanning locks in the Resolve Locks step of GC. When the variable value is set to `LEGACY`, TiDB scans locks by Regions. When the value `PHYSICAL` is used, it enables each TiKV node to bypass the Raft layer and directly scan data, which can effectively mitigate the impact of GC wakening up all Regions when the [休止状態リージョン](/tikv-configuration-file.md#hibernate-regions) feature is enabled, thus improving the execution speed in the Resolve Locks step.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、GC のロック解決ステップでロックをスキャンする方法を指定します。変数値が`LEGACY`に設定されている場合、TiDB は領域ごとにロックをスキャンします。値`PHYSICAL`を使用すると、各 TiKV ノードがRaftレイヤーをバイパスしてデータを直接スキャンできるようになり、GC がすべての領域を起動する影響を効果的に軽減できるため、ロック解決ステップでの実行速度が向上します。

</CustomContent>

### tidb_general_log {#tidb-general-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb-cloud">

-   この変数は、すべての SQL ステートメントをログに記録するかどうかを設定するために使用されます。この機能はデフォルトでは無効になっています。問題を特定するときにすべての SQL ステートメントをトレースする必要がある場合は、この機能を有効にします。

</CustomContent>

<CustomContent platform="tidb">

-   This variable is used to set whether to record all SQL statements in the [ログ](/tidb-configuration-file.md#logfile). This feature is disabled by default. If maintenance personnel needs to trace all SQL statements when locating issues, they can enable this feature.

-   To see all records of this feature in the log, you need to set the TiDB configuration item [`log.level`](/tidb-configuration-file.md#level) to `"info"` or `"debug"` and then query the `"GENERAL_LOG"` string. The following information is recorded:
    -   `conn` : 現在のセッションの ID。
    -   `user` : 現在のセッションユーザー。
    -   `schemaVersion` : 現在のスキーマ バージョン。
    -   `txnStartTS` : 現在のトランザクションが開始されるタイムスタンプ。
    -   `forUpdateTS`: In the pessimistic transactional mode, `forUpdateTS` is the current timestamp of the SQL statement. When a write conflict occurs in the pessimistic transaction, TiDB retries the SQL statement currently being executed and updates this timestamp. You can configure the number of retries via [`max-retry-count`](/tidb-configuration-file.md#max-retry-count). In the optimistic transactional model, `forUpdateTS` is equivalent to `txnStartTS`.
    -   `isReadConsistency` : 現在のトランザクション分離レベルが Read Committed (RC) であるかどうかを示します。
    -   `current_db` : 現在のデータベースの名前。
    -   `txn_mode` : トランザクション モード。値のオプションは`OPTIMISTIC`と`PESSIMISTIC`です。
    -   `sql` : 現在のクエリに対応する SQL ステートメント。

</CustomContent>

### tidb_非準備プランのキャッシュサイズ {#tidb-non-prepared-plan-cache-size}

> **警告：**
>
> Starting from v7.1.0, this variable is deprecated. Instead, use [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710) for setting.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   This variable controls the maximum number of execution plans that can be cached by [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md).

### tidb_pre_split_regions <span class="version-mark">v8.4.0 の新機能</span> {#tidb-pre-split-regions-span-class-version-mark-new-in-v8-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数は、新しく作成されたテーブルの行分割シャードのデフォルト数を設定するために使用されます。この変数がゼロ以外の値に設定されている場合、TiDB は、 `CREATE TABLE`のステートメントを実行するときに`PRE_SPLIT_REGIONS` (たとえば、 `NONCLUSTERED`テーブル) の使用を許可するテーブルにこの属性を自動的に適用します。詳細については、 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)参照してください。この変数は通常、 [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-new-in-v840)と組み合わせて使用され、新しいテーブルをシャードし、新しいテーブルのリージョンを事前に分割します。

### tidb_generate_binary_plan <span class="version-mark">v6.2.0 の新機能</span> {#tidb-generate-binary-plan-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログとステートメントの概要にバイナリ エンコードされた実行プランを生成するかどうかを制御します。
-   この変数を`ON`に設定すると、TiDB ダッシュボードで視覚的な実行プランを表示できます。TiDB ダッシュボードでは、この変数を有効にした後に生成された実行プランのみが視覚的に表示されることに注意してください。
-   You can execute the [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan) statement to parse the specific plan from a binary plan.

### tidb_gogc_tuner_max_value <span class="version-mark">v7.5.0 の新機能</span> {#tidb-gogc-tuner-max-value-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `500`
-   範囲: `[10, 2147483647]`
-   この変数は、GOGC チューナーが調整できる GOGC の最大値を制御するために使用されます。

### tidb_gogc_tuner_min_value <span class="version-mark">v7.5.0 の新機能</span> {#tidb-gogc-tuner-min-value-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[10, 2147483647]`
-   この変数は、GOGC チューナーが調整できる GOGC の最小値を制御するために使用されます。

### tidb_gogc_tuner_threshold <span class="version-mark">v6.4.0 の新機能</span> {#tidb-gogc-tuner-threshold-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `0.6`
-   範囲: `[0, 0.9)`
-   この変数は、GOGC をチューニングするための最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC Tuner は動作を停止します。

### tidb_guarantee_linearizability <span class="version-mark">v5.0 の新機能</span> {#tidb-guarantee-linearizability-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、非同期コミットのコミット TS の計算方法を制御します。デフォルト (値`ON` ) では、2 フェーズ コミットは PDサーバーから新しい TS を要求し、その TS を使用して最終コミット TS を計算します。この状況では、すべての同時トランザクションの線形化可能性が保証されます。
-   If you set this variable to `OFF`, the process of fetching TS from the PD server is skipped, with the cost that only causal consistency is guaranteed but not linearizability. For more details, see the blog post [非同期コミット、TiDB 5.0 のトランザクションコミットのアクセラレータ](https://www.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/).
-   因果一貫性のみが必要なシナリオでは、この変数を`OFF`に設定してパフォーマンスを向上させることができます。

### tidb_hash_exchange_with_new_collation {#tidb-hash-exchange-with-new-collation}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、新しい照合順序が有効になっているクラスターで MPP ハッシュ パーティション交換演算子が生成されるかどうかを制御します。1 `true`演算子を生成することを意味し、 `false`演算子を生成しないことを意味します。
-   この変数は TiDB の内部操作に使用されます。この変数を設定することは**お勧めしません**。

### tidb_hash_join_concurrency {#tidb-hash-join-concurrency}

> **警告：**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `hash join`アルゴリズムの同時実行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hash_join_version <span class="version-mark">v8.4.0 の新機能</span> {#tidb-hash-join-version-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> The feature controlled by this variable is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 列挙
-   デフォルト値: `legacy`
-   可能な値: `legacy` 、 `optimized`
-   この変数は、TiDB がハッシュ結合の最適化バージョンを使用するかどうかを制御するために使用されます。デフォルトの値は`legacy`で、最適化バージョンが使用されないことを意味します`optimized`に設定すると、TiDB はパフォーマンスを向上させるために、最適化バージョンを使用してハッシュ結合を実行します。

> **注記：**
>
> 現在、最適化されたハッシュ結合は内部結合と外部結合のみをサポートしているため、他の結合については、 `tidb_hash_join_version`が`optimized`に設定されている場合でも、TiDB は従来のハッシュ結合を使用します。

### tidb_hashagg_final_concurrency {#tidb-hashagg-final-concurrency}

> **警告：**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、第`final`フェーズで同時実行`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメータが異なっている場合、 `HashAgg`同時に実行され、それぞれ`partial`フェーズと`final`フェーズの 2 つのフェーズで実行されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hashagg_部分的同時実行性 {#tidb-hashagg-partial-concurrency}

> **警告：**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、第`partial`フェーズで同時実行`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメータが異なっている場合、 `HashAgg`同時に実行され、それぞれ`partial`フェーズと`final`フェーズの 2 つのフェーズで実行されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_historical_stats_duration <span class="version-mark">v6.6.0 の新機能</span> {#tidb-historical-stats-duration-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 期間
-   デフォルト値: `168h` 、7日間を意味します
-   この変数は、履歴統計がstorageに保持される期間を制御します。

### tidb_idle_transaction_timeout <span class="version-mark">v7.6.0 の新機能</span> {#tidb-idle-transaction-timeout-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 31536000]`
-   単位: 秒
-   この変数は、ユーザー セッション内のトランザクションのアイドル タイムアウトを制御します。ユーザー セッションがトランザクション状態にあり、この変数の値を超える期間アイドル状態のままになると、TiDB はセッションを終了します。アイドル状態のユーザー セッションとは、アクティブなリクエストがなく、セッションが新しいリクエストを待機していることを意味します。
-   デフォルト値`0`は無制限を意味します。

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">v6.0.0 の新機能</span> {#tidb-ignore-prepared-cache-close-stmt-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、プリペアドステートメントキャッシュを閉じるコマンドを無視するかどうかを設定するために使用されます。
-   この変数を`ON`に設定すると、バイナリプロトコルの`COM_STMT_CLOSE`コマンドとテキストプロトコルの[`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md)ステートメントは無視されます。詳細については、 [Ignore the `COM_STMT_CLOSE` command and the `DEALLOCATE PREPARE` statement](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)参照してください。

### tidb_index_join_batch_size {#tidb-index-join-batch-size}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `25000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup join`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_index_join_double_read_penalty_cost_rate <span class="version-mark">v6.6.0 の新機能</span> {#tidb-index-join-double-read-penalty-cost-rate-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、インデックス結合の選択にペナルティ コストを適用するかどうかを決定し、これにより、オプティマイザがインデックス結合を選択する可能性が低くなり、ハッシュ結合や tiflash 結合などの代替結合方法を選択する可能性が高くなります。
-   インデックス結合を選択すると、多くのテーブル検索要求がトリガーされ、リソースが過剰に消費されます。この変数を使用すると、オプティマイザーがインデックス結合を選択する可能性を減らすことができます。
-   This variable takes effect only when the [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620) variable is set to `2`.

### tidb_index_lookup_concurrency {#tidb-index-lookup-concurrency}

> **警告：**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_join_concurrency {#tidb-index-lookup-join-concurrency}

> **警告：**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup join`アルゴリズムの同時実行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_merge_intersection_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-index-merge-intersection-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   この変数は、インデックス マージが実行する交差操作の最大同時実行性を設定します。これは、TiDB が動的プルーニング モードでパーティション テーブルにアクセスする場合にのみ有効です。実際の同時実行性は、 `tidb_index_merge_intersection_concurrency`とパーティションテーブルのパーティション数のうち小さい方の値になります。
-   デフォルト値`-1` 、値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_size {#tidb-index-lookup-size}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `20000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_index_serial_scan_concurrency {#tidb-index-serial-scan-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `serial scan`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_init_チャンクサイズ {#tidb-init-chunk-size}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `32`
-   範囲: `[1, 32]`
-   単位: 行
-   この変数は、実行プロセス中に初期チャンクの行数を設定するために使用されます。チャンクの行数は、単一のクエリに必要なメモリ量に直接影響します。クエリ内のすべての列の合計幅とチャンクの行数を考慮すると、単一のチャンクに必要なメモリを大まかに見積もることができます。これをエグゼキュータの同時実行性と組み合わせると、単一のクエリに必要な合計メモリを大まかに見積もることができます。単一のチャンクの合計メモリは16 MiB を超えないようにすることをお勧めします。

### tidb_instance_plan_cache_reserved_percentage <span class="version-mark">v8.4.0 の新機能</span> {#tidb-instance-plan-cache-reserved-percentage-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> Currently, Instance Plan Cache is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: フロート
-   デフォルト値: `0.1`
-   範囲: `[0, 1]`
-   この変数は、メモリの削除後に[インスタンスプランキャッシュ](#tidb_enable_instance_plan_cache-new-in-v840)に予約されるアイドルメモリの割合を制御します。インスタンス プラン キャッシュによって使用されるメモリが[`tidb_instance_plan_cache_max_size`](#tidb_instance_plan_cache_max_size-new-in-v840)で設定された制限に達すると、TiDB は、アイドルメモリの割合が[`tidb_instance_plan_cache_reserved_percentage`](#tidb_instance_plan_cache_reserved_percentage-new-in-v840)で設定された値を超えるまで、Least Recently Used (LRU) アルゴリズムを使用してメモリから実行プランの削除を開始します。

### tidb_instance_plan_cache_max_size <span class="version-mark">v8.4.0 の新機能</span> {#tidb-instance-plan-cache-max-size-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> Currently, Instance Plan Cache is an experimental feature. is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `125829120` (120 MiB)
-   単位: バイト
-   This variable sets the maximum memory usage for [インスタンスプランキャッシュ](#tidb_enable_instance_plan_cache-new-in-v840).

### tidb_isolation_read_engines <span class="version-mark">v4.0 の新機能</span> {#tidb-isolation-read-engines-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   デフォルト値: `tikv,tiflash,tidb`
-   この変数は、TiDB がデータを読み取るときに使用できるstorageエンジン リストを設定するために使用されます。

### tidb_last_ddl_info <span class="version-mark">v6.0.0 の新機能</span> {#tidb-last-ddl-info-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   タイプ: 文字列
-   これは読み取り専用変数です。現在のセッション内の最後の DDL 操作の情報を取得するために TiDB で内部的に使用されます。
    -   &quot;query&quot;: 最後の DDL クエリ文字列。
    -   &quot;seq_num&quot;: 各 DDL 操作のシーケンス番号。DDL 操作の順序を識別するために使用されます。

### tidb_last_query_info <span class="version-mark">v4.0.14 の新機能</span> {#tidb-last-query-info-span-class-version-mark-new-in-v4-0-14-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: &quot;&quot;
-   これは読み取り専用変数です。これは、最後の DML ステートメントのトランザクション情報を照会するために TiDB で内部的に使用されます。情報には次のものが含まれます。
    -   `txn_scope` : トランザクションのスコープ`global`または`local`になります。
    -   `start_ts` : トランザクションの開始タイムスタンプ。
    -   `for_update_ts` : 前回実行された DML ステートメントの`for_update_ts`これは、テストに使用される TiDB の内部用語です。通常、この情報は無視できます。
    -   `error` : エラー メッセージ (ある場合)。
    -   `ru_consumption`: Consumed [ロシア](/tidb-resource-control.md#what-is-request-unit-ru) for executing the statement.

### tidb_last_txn_info <span class="version-mark">v4.0.9 の新機能</span> {#tidb-last-txn-info-span-class-version-mark-new-in-v4-0-9-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   この変数は、現在のセッション内の最後のトランザクション情報を取得するために使用されます。これは読み取り専用変数です。トランザクション情報には次のものが含まれます。
    -   トランザクションの範囲。
    -   TS の開始とコミット。
    -   トランザクション コミット モード。2 フェーズ、1 フェーズ、または非同期コミットのいずれかになります。
    -   非同期コミットまたは 1 フェーズ コミットから 2 フェーズ コミットへのトランザクション フォールバックの情報。
    -   エラーが発生しました。

### tidb_last_plan_replayer_token <span class="version-mark">v6.3.0 の新機能</span> {#tidb-last-plan-replayer-token-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 文字列
-   この変数は読み取り専用であり、現在のセッションの最後の`PLAN REPLAYER DUMP`の実行の結果を取得するために使用されます。

### tidb_load_based_replica_read_threshold <span class="version-mark">v7.0.0 の新機能</span> {#tidb-load-based-replica-read-threshold-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   タイプ: 文字列
-   This variable is used to set the threshold for triggering load-based replica read. When the estimated queue time of the leader node exceeds the threshold, TiDB prioritizes reading data from the follower node. The format is a time duration, such as `"100ms"` or `"1s"`. For more details, see [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots).

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   タイプ: 文字列
-   This variable is used to set the threshold for triggering load-based replica read. When the estimated queue time of the leader node exceeds the threshold, TiDB prioritizes reading data from the follower node. The format is a time duration, such as `"100ms"` or `"1s"`. For more details, see [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#scatter-read-hotspots).

</CustomContent>

### <code>tidb_load_binding_timeout</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-tidb-load-binding-timeout-code-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `200`
-   範囲: `(0, 2147483647]`
-   単位: ミリ秒
-   この変数は、バインディングの読み込みのタイムアウトを制御するために使用されます。バインディングの読み込みの実行時間がこの値を超えると、読み込みは停止します。

### <code>tidb_lock_unchanged_keys</code> <span class="version-mark">v7.1.1 および v7.3.0 の新機能</span> {#code-tidb-lock-unchanged-keys-code-span-class-version-mark-new-in-v7-1-1-and-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、次のシナリオで特定のキーをロックするかどうかを制御するために使用されます。値が`ON`に設定されている場合、これらのキーはロックされます。値が`OFF`に設定されている場合、これらのキーはロックされません。
    -   Duplicate keys in `INSERT IGNORE` and `REPLACE` statements. Before v6.1.6, these keys were not locked. This issue has been fixed in [＃42121](https://github.com/pingcap/tidb/issues/42121).
    -   Unique keys in `UPDATE` statements when the values of the keys are not changed. Before v6.5.2, these keys were not locked. This issue has been fixed in [＃36438](https://github.com/pingcap/tidb/issues/36438).
-   トランザクションの一貫性と合理性を維持するために、この値を変更することは推奨されません。TiDB をアップグレードすると、これら 2 つの修正により重大なパフォーマンスの問題が発生し、ロックなしの動作が許容できる場合 (前述の問題を参照)、この変数を`OFF`に設定できます。

### tidb_log_file_max_days <span class="version-mark">v5.3.0 の新機能</span> {#tidb-log-file-max-days-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`

<CustomContent platform="tidb">

-   This variable is used to set the maximum days that the log is retained on the current TiDB instance. Its value defaults to the value of the [`max-days`](/tidb-configuration-file.md#max-days) configuration in the configuration file. Changing the variable value only affects the current TiDB instance. After TiDB is restarted, the variable value is reset and the configuration value is not affected.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、現在の TiDB インスタンスにログが保持される最大日数を設定するために使用されます。

</CustomContent>

### 低解像度tso {#tidb-low-resolution-tso}

-   範囲: セッション | グローバル
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   This variable is used to set whether to enable the low-precision TSO feature. After this feature is enabled, TiDB uses the cached timestamp to read data. The cached timestamp is updated every 2 seconds by default. Starting from v8.0.0, you can configure the update interval by [`tidb_low_resolution_tso_update_interval`](#tidb_low_resolution_tso_update_interval-new-in-v800).
-   主な適用可能なシナリオは、古いデータの読み取りが許容される場合に、小さな読み取り専用トランザクションの TSO 取得のオーバーヘッドを削減することです。
-   v8.3.0 以降、この変数は GLOBAL スコープをサポートします。

### <code>tidb_low_resolution_tso_update_interval</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-tidb-low-resolution-tso-update-interval-code-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `2000`
-   範囲: `[10, 60000]`
-   単位: ミリ秒
-   この変数は、低精度 TSO 機能で使用されるキャッシュされたタイムスタンプの更新間隔をミリ秒単位で設定するために使用されます。
-   This variable is only available when [`tidb_low_resolution_tso`](#tidb_low_resolution_tso) is enabled.

### tidb_max_auto_analyze_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-auto-analyze-time-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `43200`
-   範囲: `[0, 2147483647]`
-   単位: 秒
-   この変数は、自動`ANALYZE`タスクの最大実行時間を指定するために使用されます。自動`ANALYZE`タスクの実行時間が指定された時間を超えると、タスクは終了します。この変数の値が`0`の場合、自動`ANALYZE`タスクの最大実行時間に制限はありません。

### tidb_max_bytes_before_tiflash_external_group_by <span class="version-mark">v7.0.0 の新機能</span> {#tidb-max-bytes-before-tiflash-external-group-by-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   This variable is used to specify the maximum memory usage of the Hash Aggregation operator with `GROUP BY` in TiFlash, in bytes. When the memory usage exceeds the specified value, TiFlash triggers the Hash Aggregation operator to spill to disk. When the value of this variable is `-1`, TiDB does not pass this variable to TiFlash. Only when the value of this variable is greater than or equal to `0`, TiDB passes this variable to TiFlash. When the value of this variable is `0`, it means that the memory usage is unlimited, that is, TiFlash Hash Aggregation operator will not trigger spilling. For details, see [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md).

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、通常、集計は複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の集計演算子の最大メモリ使用量を制御します。
> -   When this variable is set to `-1`, TiFlash determines the maximum memory usage of the aggregation operator based on the value of its own configuration item [`max_bytes_before_external_group_by`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、通常、集計は複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の集計演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目`max_bytes_before_external_group_by`の値に基づいて集計演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_join <span class="version-mark">v7.0.0 の新機能</span> {#tidb-max-bytes-before-tiflash-external-join-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   This variable is used to specify the maximum memory usage of the Hash Join operator with `JOIN` in TiFlash, in bytes. When the memory usage exceeds the specified value, TiFlash triggers the Hash Join operator to spill to disk. When the value of this variable is `-1`, TiDB does not pass this variable to TiFlash. Only when the value of this variable is greater than or equal to `0`, TiDB passes this variable to TiFlash. When the value of this variable is `0`, it means that the memory usage is unlimited, that is, TiFlash Hash Join operator will not trigger spilling. For details, see [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md).

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、結合は通常、複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の結合演算子の最大メモリ使用量を制御します。
> -   When this variable is set to `-1`, TiFlash determines the maximum memory usage of the join operator based on the value of its own configuration item [`max_bytes_before_external_join`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、結合は通常、複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の結合演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目`max_bytes_before_external_join`の値に基づいて結合演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_sort <span class="version-mark">v7.0.0 の新機能</span> {#tidb-max-bytes-before-tiflash-external-sort-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   This variable is used to specify the maximum memory usage of the TopN and Sort operators in TiFlash, in bytes. When the memory usage exceeds the specified value, TiFlash triggers the TopN and Sort operators to spill to disk. When the value of this variable is `-1`, TiDB does not pass this variable to TiFlash. Only when the value of this variable is greater than or equal to `0`, TiDB passes this variable to TiFlash. When the value of this variable is `0`, it means that the memory usage is unlimited, that is, TiFlash TopN and Sort operators will not trigger spilling. For details, see [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md).

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、TopN と Sort は通常、複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の TopN および Sort 演算子の最大メモリ使用量を制御します。
> -   When this variable is set to `-1`, TiFlash determines the maximum memory usage of the TopN and Sort operators based on the value of its own configuration item [`max_bytes_before_external_sort`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、TopN と Sort は通常、複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の TopN および Sort 演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目`max_bytes_before_external_sort`の値に基づいて、TopN 演算子と Sort 演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_chunk_size {#tidb-max-chunk-size}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[32, 2147483647]`
-   単位: 行
-   This variable is used to set the maximum number of rows in a chunk during the execution process. Setting to too large of a value may cause cache locality issues. The recommended value for this variable is no larger than 65536. The number of rows for a chunk directly affects the amount of memory required for a single query. You can roughly estimate the memory needed for a single chunk by considering the total width of all columns in the query and the number of rows for the chunk. Combining this with the concurrency of the executor, you can make a rough estimation of the total memory required for a single query. It is recommended that the total memory for a single chunk does not exceed 16 MiB. When the query involves a large amount of data and a single chunk is insufficient to handle all the data, TiDB processes it multiple times, doubling the chunk size with each processing iteration, starting from [`tidb_init_chunk_size`](#tidb_init_chunk_size) until the chunk size reaches the value of `tidb_max_chunk_size`.

### tidb_max_delta_schema_count <span class="version-mark">v2.1.18 および v3.0.5 の新機能</span> {#tidb-max-delta-schema-count-span-class-version-mark-new-in-v2-1-18-and-v3-0-5-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[100, 16384]`
-   この変数は、キャッシュできるスキーマ バージョン (対応するバージョン用に変更されたテーブル ID) の最大数を設定するために使用されます。値の範囲は 100 ～ 16384 です。

### tidb_max_paging_size <span class="version-mark">v6.3.0 の新機能</span> {#tidb-max-paging-size-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `50000`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサ ページング要求プロセス中の最大行数を設定するために使用されます。この変数を小さすぎる値に設定すると、TiDB と TiKV 間の RPC カウントが増加し、大きすぎる値に設定すると、データのロードや完全なテーブル スキャンなどの場合にメモリ使用量が過剰になります。この変数のデフォルト値では、OLAP シナリオよりも OLTP シナリオでパフォーマンスが向上します。アプリケーションがstorageエンジンとして TiKV のみを使用する場合は、OLAP ワークロード クエリを実行するときにこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

### tidb_max_tiflash_threads <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-tiflash-threads-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、 TiFlash がリクエストを実行するための最大同時実行数を設定するために使用されます。デフォルト値は`-1`で、このシステム変数が無効であり、最大同時実行数はTiFlash構成`profiles.default.max_threads`の設定に依存することを示します。値が`0`の場合、最大スレッド数はTiFlashによって自動的に設定されます。

### tidb_mem_oom_action <span class="version-mark">v6.1.0 の新機能</span> {#tidb-mem-oom-action-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `CANCEL`
-   可能な値: `CANCEL` 、 `LOG`

<CustomContent platform="tidb">

-   Specifies what operation TiDB performs when a single SQL statement exceeds the memory quota specified by `tidb_mem_quota_query` and cannot be spilled over to disk. See [TiDB メモリ制御](/configure-memory-usage.md) for details.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   Specifies what operation TiDB performs when a single SQL statement exceeds the memory quota specified by [`tidb_mem_quota_query`](#tidb_mem_quota_query) and cannot be spilled over to disk.

</CustomContent>

-   デフォルト値は`CANCEL`ですが、TiDB v4.0.2 以前のバージョンではデフォルト値は`LOG`です。
-   この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_mem_quota_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-mem-quota-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト
-   This variable controls the maximum memory usage of TiDB updating statistics. Such a memory usage occurs when you manually execute [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) and when TiDB automatically analyzes tasks in the background. When the total memory usage exceeds this threshold, user-executed `ANALYZE` will exit, and an error message is reported that reminds you to try a lower sampling rate or retry later. If the automatic task in the TiDB background exits because the memory threshold is exceeded, and the sampling rate used is higher than the default value, TiDB will retry the update using the default sampling rate. When this variable value is negative or zero, TiDB does not limit the memory usage of both the manual and automatic update tasks.

> **注記：**
>
> `auto_analyze` 、TiDB 起動構成ファイルで`run-auto-analyze`が有効になっている場合にのみ、TiDB クラスターでトリガーされます。

### tidb_mem_quota_apply_cache <span class="version-mark">v5.0 の新機能</span> {#tidb-mem-quota-apply-cache-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `33554432` (32 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、 `Apply`演算子のローカル キャッシュのメモリ使用量しきい値を設定するために使用されます。
-   `Apply`演算子のローカル キャッシュは、 `Apply`演算子の計算を高速化するために使用されます。変数を`0`に設定すると、 `Apply`キャッシュ機能を無効にすることができます。

### tidb_mem_quota_binding_cache <span class="version-mark">v6.0.0 の新機能</span> {#tidb-mem-quota-binding-cache-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[0, 2147483647]`
-   単位: バイト
-   この変数は、バインディングのキャッシュに使用されるメモリのしきい値を設定するために使用されます。
-   システムが過剰なバインディングを作成またはキャプチャし、メモリ領域が過剰に使用されると、TiDB はログに警告を返します。この場合、キャッシュは利用可能なすべてのバインディングを保持できないか、どのバインディングを保存するかを決定することができません。このため、一部のクエリではバインディングが失われる可能性があります。この問題に対処するには、この変数の値を増やすことができます。これにより、バインディングのキャッシュに使用されるメモリが増加します。このパラメータを変更した後、 `admin reload bindings`実行してバインディングを再ロードし、変更を検証する必要があります。

### tidb_mem_quota_query {#tidb-mem-quota-query}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `1073741824` (1 GiB)
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト

<CustomContent platform="tidb">

-   TiDB v6.1.0 より前のバージョンでは、これはセッション スコープ変数であり、初期値として`tidb.toml`から`mem-quota-query`の値を使用します。v6.1.0 以降では、 `tidb_mem_quota_query` `SESSION | GLOBAL`スコープ変数です。
-   For versions earlier than TiDB v6.5.0, this variable is used to set the threshold value of memory quota for **a query**. If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation defined by [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610).
-   TiDB v6.5.0 以降のバージョンでは、この変数は**セッション**のメモリクォータのしきい値を設定するために使用されます。実行中のセッションのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。TiDB v6.5.0 以降では、セッションのメモリ使用量には、セッション内のトランザクションによって消費されるメモリが含まれることに注意してください。TiDB v6.5.0 以降のバージョンでのトランザクションメモリ使用量の制御動作については、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)参照してください。
-   変数値を`0`または`-1`に設定すると、メモリしきい値は正の無限大になります。 128 より小さい値を設定すると、値はデフォルトで`128`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB v6.1.0 より前のバージョンでは、これはセッション スコープ変数です。v6.1.0 以降では、 `tidb_mem_quota_query` `SESSION | GLOBAL`スコープ変数です。
-   For versions earlier than TiDB v6.5.0, this variable is used to set the threshold value of memory quota for **a query**. If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation defined by [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610).
-   For TiDB v6.5.0 and later versions, this variable is used to set the threshold value of memory quota for **a session**. If the memory quota of a session during execution exceeds the threshold value, TiDB performs the operation defined by [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610). Note that starting from TiDB v6.5.0, the memory usage of a session contains the memory consumed by the transactions in the session.
-   変数値を`0`または`-1`に設定すると、メモリしきい値は正の無限大になります。 128 より小さい値を設定すると、値はデフォルトで`128`になります。

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio {#tidb-memory-debug-mode-alarm-ratio}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: フロート
-   デフォルト値: `0`
-   この変数は、TiDBメモリデバッグ モードで許可されるメモリ統計エラー値を表します。
-   この変数は TiDB の内部テストに使用されます。この変数を設定することは**お勧めしません**。

### tidb_memory_debug_mode_min_heap_inuse {#tidb-memory-debug-mode-min-heap-inuse}

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `0`
-   この変数は TiDB の内部テストに使用されます。この変数を設定することは**推奨されません**。この変数を有効にすると、TiDB のパフォーマンスに影響します。
-   このパラメータを設定すると、TiDB はメモリデバッグ モードに入り、メモリ追跡の精度を分析します。TiDB は、後続の SQL ステートメントの実行中に頻繁に GC をトリガーし、実際のメモリ使用量とメモリ統計を比較します。現在のメモリ使用量が`tidb_memory_debug_mode_min_heap_inuse`より大きく、メモリ統計エラーが`tidb_memory_debug_mode_alarm_ratio`を超える場合、TiDB は関連するメモリ情報をログとファイルに出力します。

### tidb_メモリ使用量アラーム比率 {#tidb-memory-usage-alarm-ratio}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0.0, 1.0]`

<CustomContent platform="tidb">

-   This variable sets the memory usage ratio that triggers the tidb-server memory alarm. By default, TiDB prints an alarm log when TiDB memory usage exceeds 70% of its total memory and any of the [警報条件](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage) is met.
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能は無効になります。
-   この変数が`0`より大きく`1`より小さい値に設定されている場合、メモリしきい値アラーム機能が有効になっていることを意味します。

    -   If the value of the system variable [`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640) is `0`, the memory alarm threshold is `tidb_memory-usage-alarm-ratio * system memory size`.
    -   システム変数`tidb_server_memory_limit`の値が 0 より大きい値に設定されている場合、メモリアラームしきい値は`tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable sets the memory usage ratio that triggers the [tidb-serverメモリアラーム](https://docs.pingcap.com/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage).
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能は無効になります。
-   この変数が`0`より大きく`1`より小さい値に設定されている場合、メモリしきい値アラーム機能が有効になっていることを意味します。

</CustomContent>

### tidb_memory_usage_alarm_keep_record_num <span class="version-mark">v6.4.0 の新機能</span> {#tidb-memory-usage-alarm-keep-record-num-span-class-version-mark-new-in-v6-4-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `5`
-   範囲: `[1, 10000]`
-   tidb-server のメモリ使用量がメモリアラームしきい値を超えてアラームをトリガーすると、TiDB はデフォルトで最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この変数を使用してこの数を調整できます。

### tidb_merge_join_concurrency {#tidb-merge-join-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   範囲: `[1, 256]`
-   デフォルト値: `1`
-   この変数は、クエリが実行されるときに`MergeJoin`演算子の同時実行性を設定します。
-   この変数を設定することは**推奨されません**。この変数の値を変更すると、データの正確性に問題が発生する可能性があります。

### tidb_merge_partition_stats_concurrency {#tidb-merge-partition-stats-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   デフォルト値: `1`
-   この変数は、TiDB がパーティションテーブルを分析するときに、パーティションテーブルの統計をマージする同時実行性を指​​定します。

### tidb_enable_async_merge_global_stats <span class="version-mark">v7.5.0 の新機能</span> {#tidb-enable-async-merge-global-stats-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `ON` 。TiDB を v7.5.0 より前のバージョンから v7.5.0 以降のバージョンにアップグレードする場合、デフォルト値は`OFF`なります。
-   この変数は、OOM の問題を回避するために TiDB がグローバル統計を非同期的にマージするために使用されます。

### tidb_metric_query_range_duration <span class="version-mark">v4.0 の新機能</span> {#tidb-metric-query-range-duration-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位: 秒
-   この変数は、クエリ`METRICS_SCHEMA`時に生成される Prometheus ステートメントの範囲期間を設定するために使用されます。

### tidb_metric_query_step <span class="version-mark">v4.0 の新機能</span> {#tidb-metric-query-step-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位: 秒
-   この変数は、クエリ`METRICS_SCHEMA`時に生成される Prometheus ステートメントのステップを設定するために使用されます。

### tidb_min_paging_size <span class="version-mark">v6.2.0 の新機能</span> {#tidb-min-paging-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `128`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサ ページング要求プロセス中の最小行数を設定するために使用されます。この変数を小さすぎる値に設定すると、TiDB と TiKV 間の RPC 要求数が増加し、大きすぎる値に設定すると、IndexLookup と Limit を使用してクエリを実行するときにパフォーマンスが低下する可能性があります。この変数のデフォルト値では、OLAP シナリオよりも OLTP シナリオでパフォーマンスが向上します。アプリケーションがstorageエンジンとして TiKV のみを使用する場合は、OLAP ワークロード クエリを実行するときにこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

![Paging size impact on TPCH](/media/paging-size-impact-on-tpch.png)

この図に示すように、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)有効になっている場合、 `tidb_min_paging_size`と[`tidb_max_paging_size`](#tidb_max_paging_size-new-in-v630)の設定によって TPCH のパフォーマンスが影響を受けます。縦軸は実行時間で、小さいほど優れています。

### tidb_mpp_store_fail_ttl {#tidb-mpp-store-fail-ttl}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 期間
-   デフォルト値: `60s`
-   新しく起動したTiFlashノードはサービスを提供しません。クエリが失敗しないように、TiDB は tidb-server がクエリを送信することを新しく起動したTiFlashノードに制限します。この変数は、新しく起動したTiFlashノードにリクエストが送信されない時間範囲を示します。

### tidb_multi_statement_mode <span class="version-mark">v4.0.11 の新機能</span> {#tidb-multi-statement-mode-span-class-version-mark-new-in-v4-0-11-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   可能な`WARN` `ON` `OFF`
-   この変数は、 `COM_QUERY`呼び出しで複数のクエリを実行できるかどうかを制御します。
-   SQL インジェクション攻撃の影響を軽減するために、TiDB ではデフォルトで`COM_QUERY`呼び出しで複数のクエリが実行されないようにするようになりました。この変数は、以前のバージョンの TiDB からのアップグレード パスの一部として使用することを目的としています。次の動作が適用されます。

| クライアント設定        | `tidb_multi_statement_mode`値 | 複数のステートメントが許可されますか? |
| --------------- | ---------------------------- | ------------------- |
| 複数のステートメント = ON | オフ                           | はい                  |
| 複数のステートメント = ON | の上                           | はい                  |
| 複数のステートメント = ON | 警告                           | はい                  |
| 複数のステートメント = オフ | オフ                           | いいえ                 |
| 複数のステートメント = オフ | の上                           | はい                  |
| 複数のステートメント = オフ | 警告                           | はい（+警告が返されました）      |

> **注記：**
>
> 安全だと考えられるのは、デフォルト値の`OFF`だけです。アプリケーションが TiDB の以前のバージョン用に特別に設計されている場合は、設定`tidb_multi_statement_mode=ON`必要になることがあります。アプリケーションで複数のステートメントのサポートが必要な場合は、 `tidb_multi_statement_mode`オプションではなく、クライアント ライブラリによって提供される設定を使用することをお勧めします。例:
>
> -   [go-sql-ドライバー](https://github.com/go-sql-driver/mysql#multistatements) (`multiStatements`)
> -   [コネクタ/J](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) (`allowMultiQueries`)
> -   PHP [mysqli](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) (`mysqli_multi_query`)

### tidb_nontransactional_ignore_error <span class="version-mark">v6.1.0 の新機能</span> {#tidb-nontransactional-ignore-error-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非トランザクション DML ステートメントでエラーが発生した場合に、すぐにエラーを返すかどうかを指定します。
-   値を`OFF`に設定すると、非トランザクション DML ステートメントは最初のエラーで直ちに停止し、エラーを返します。後続のバッチはすべてキャンセルされます。
-   値を`ON`に設定した場合、バッチでエラーが発生すると、すべてのバッチが実行されるまで後続のバッチが引き続き実行されます。実行プロセス中に発生したすべてのエラーは、結果にまとめて返されます。

### tidb_opt_agg_push_down {#tidb-opt-agg-push-down}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが集計関数を Join、Projection、および UnionAll の前の位置にプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリで集計操作が遅い場合は、変数値を ON に設定できます。

### tidb_opt_ブロードキャスト_カルテシアン_結合 {#tidb-opt-broadcast-cartesian-join}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   ブロードキャスト カテシアン結合を許可するかどうかを示します。
-   `0` means that the Broadcast Cartesian Join is not allowed. `1` means that it is allowed based on [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50). `2` means that it is always allowed even if the table size exceeds the threshold.
-   この変数は TiDB で内部的に使用されるため、その値を変更することは推奨され**ません**。

### tidb_opt_concurrency_factor {#tidb-opt-concurrency-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   Indicates the CPU cost of starting a Golang goroutine in TiDB. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_copcpu_factor {#tidb-opt-copcpu-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   Indicates the CPU cost for TiKV Coprocessor to process one row. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_相関係数 {#tidb-opt-correlation-exp-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Integer
-   Default value: `1`
-   Range: `[0, 2147483647]`
-   When the method that estimates the number of rows based on column order correlation is not available, the heuristic estimation method is used. This variable is used to control the behavior of the heuristic method.
    -   When the value is 0, the heuristic method is not used.
    -   When the value is greater than 0:
        -   A larger value indicates that an index scan will probably be used in the heuristic method.
        -   A smaller value indicates that a table scan will probably be used in the heuristic method.

### tidb_opt_correlation_threshold {#tidb-opt-correlation-threshold}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Default value: `0.9`
-   Range: `[0, 1]`
-   This variable is used to set the threshold value that determines whether to enable estimating the row count by using column order correlation. If the order correlation between the current column and the `handle` column exceeds the threshold value, this method is enabled.

### tidb_opt_cpu_factor {#tidb-opt-cpu-factor}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Range: `[0, 2147483647]`
-   Default value: `3.0`
-   Indicates the CPU cost for TiDB to process one row. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### <code>tidb_opt_derive_topn</code> <span class="version-mark">New in v7.0.0</span> {#code-tidb-opt-derive-topn-code-span-class-version-mark-new-in-v7-0-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   Controls whether to enable the optimization rule of [ウィンドウ関数から TopN または Limit を導出する](/derive-topn-from-window.md).

### tidb_opt_desc_factor {#tidb-opt-desc-factor}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Range: `[0, 18446744073709551615]`
-   Default value: `3.0`
-   Indicates the cost for TiKV to scan one row from the disk in descending order. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_disk_factor {#tidb-opt-disk-factor}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Range: `[0, 18446744073709551615]`
-   Default value: `1.5`
-   Indicates the I/O cost for TiDB to read or write one byte of data from or to the temporary disk. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_distinct_agg_push_down {#tidb-opt-distinct-agg-push-down}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function with `distinct` (such as `select count(distinct a) from t`) to Coprocessor.
-   When the aggregate function with the `distinct` operation is slow in the query, you can set the variable value to `1`.

In the following example, before `tidb_opt_distinct_agg_push_down` is enabled, TiDB needs to read all data from TiKV and execute `distinct` on the TiDB side. After `tidb_opt_distinct_agg_push_down` is enabled, `distinct a` is pushed down to Coprocessor, and a `group by` column `test.t.a` is added to `HashAgg_5`.

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

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `ON`
-   This variable is used to control whether the optimizer estimates the number of rows based on column order correlation

### tidb_opt_enable_hash_join <span class="version-mark">New in v6.5.6, v7.1.2, and v7.4.0</span> {#tidb-opt-enable-hash-join-span-class-version-mark-new-in-v6-5-6-v7-1-2-and-v7-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable is used to control whether the optimizer selects hash joins for tables. The value is `ON` by default. If it is set to `OFF`, the optimizer avoids selecting hash joins when generating execution plans, unless no other join algorithm is available.
-   If both the system variable `tidb_opt_enable_hash_join` and the `HASH_JOIN` hint are configured, the `HASH_JOIN` hint takes precedence. Even if `tidb_opt_enable_hash_join` is set to `OFF`, when you specify a `HASH_JOIN` hint in a query, the TiDB optimizer still enforces a hash join plan.

### tidb_opt_enable_non_eval_scalar_subquery <span class="version-mark">New in v7.3.0</span> {#tidb-opt-enable-non-eval-scalar-subquery-span-class-version-mark-new-in-v7-3-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to control whether the `EXPLAIN` statement disables the execution of constant subqueries that can be expanded at the optimization stage. When this variable is set to `OFF`, the `EXPLAIN` statement expands the subquery in advance at the optimization stage. When this variable is set to `ON`, the `EXPLAIN` statement does not expand the subquery at the optimization stage. For more information, see [サブクエリの拡張を無効にする](/explain-walkthrough.md#disable-the-early-execution-of-subqueries).

### tidb_opt_enable_late_materialization <span class="version-mark">New in v7.0.0</span> {#tidb-opt-enable-late-materialization-span-class-version-mark-new-in-v7-0-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `ON`
-   この変数は、 [TiFlash の遅い実体化](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御するために使用されます。TiFlashの遅延マテリアライゼーションは[fast scan mode](/tiflash/use-fastscan.md)では有効にならないことに注意してください。
-   When this variable is set to `OFF` to disable the TiFlash late materialization feature, to process a `SELECT` statement with filter conditions (`WHERE` clause), TiFlash scans all the data of the required columns before filtering. When this variable is set to `ON` to enable the TiFlash late materialization feature, TiFlash can first scan the column data related to the filter conditions that are pushed down to the TableScan operator, filter the rows that meet the conditions, and then scan the data of other columns of these rows for further calculations, thereby reducing IO scans and computations of data processing.

### tidb_opt_enable_mpp_shared_cte_execution <span class="version-mark">New in v7.2.0</span> {#tidb-opt-enable-mpp-shared-cte-execution-span-class-version-mark-new-in-v7-2-0-span}

> **Warning:**
>
> The feature controlled by this variable is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   This variable controls whether the non-recursive [共通テーブル式 (CTE)](/sql-statements/sql-statement-with.md) can be executed on TiFlash MPP. By default, when this variable is disabled, CTE is executed on TiDB, which has a large performance gap compared with enabling this feature.

### tidb_opt_enable_fuzzy_binding <span class="version-mark">New in v7.6.0</span> {#tidb-opt-enable-fuzzy-binding-span-class-version-mark-new-in-v7-6-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   This variable controls whether to enable the [データベース間のバインディング](/sql-plan-management.md#cross-database-binding) feature.

### tidb_opt_fix_control <span class="version-mark">New in v6.5.3 and v7.1.0</span> {#tidb-opt-fix-control-span-class-version-mark-new-in-v6-5-3-and-v7-1-0-span}

<CustomContent platform="tidb">

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: String
-   Default value: `""`
-   This variable is used to control some internal behaviors of the optimizer.
-   The optimizer's behavior might vary depending on user scenarios or SQL statements. This variable provides a more fine-grained control over the optimizer and helps to prevent performance regression after upgrading caused by behavior changes in the optimizer.
-   For a more detailed introduction, see [オプティマイザー修正コントロール](/optimizer-fix-controls.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: String
-   Default value: `""`
-   This variable is used to control some internal behaviors of the optimizer.
-   The optimizer's behavior might vary depending on user scenarios or SQL statements. This variable provides a more fine-grained control over the optimizer and helps to prevent performance regression after upgrading caused by behavior changes in the optimizer.
-   For a more detailed introduction, see [オプティマイザー修正コントロール](https://docs.pingcap.com/tidb/v7.2/optimizer-fix-controls).

</CustomContent>

### tidb_opt_force_inline_cte <span class="version-mark">New in v6.3.0</span> {#tidb-opt-force-inline-cte-span-class-version-mark-new-in-v6-3-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to control whether common table expressions (CTEs) in the entire session are inlined or not. The default value is `OFF`, which means that inlining CTE is not enforced by default. However, you can still inline CTE by specifying the `MERGE()` hint. If the variable is set to `ON`, all CTEs (except recursive CTE) in this session are forced to be inlined.

### tidb_opt_advanced_join_hint <span class="version-mark">New in v7.0.0</span> {#tidb-opt-advanced-join-hint-span-class-version-mark-new-in-v7-0-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `ON`
-   この変数は、 [`HASH_JOIN()`ヒント](/optimizer-hints.md#hash_joint1_name--tl_name-)や[`MERGE_JOIN()` hint](/optimizer-hints.md#merge_joint1_name--tl_name-)などの結合方法ヒントが、 [`LEADING()`ヒント](/optimizer-hints.md#leadingt1_name--tl_name-)の使用を含む結合したテーブルの再配置の最適化プロセスに影響を与えるかどうかを制御するために使用されます。デフォルト値は`ON`で、影響を与えないことを意味します。 `OFF`に設定すると、結合方法ヒントと`LEADING()`ヒントの両方が同時に使用されるシナリオで競合が発生する可能性があります。

> **Note:**
>
> The behavior of versions earlier than v7.0.0 is consistent with that of setting this variable to `OFF`. To ensure forward compatibility, when you upgrade from an earlier version to a v7.0.0 or later cluster, this variable is set to `OFF`. To obtain more flexible hint behavior, it is strongly recommended to switch this variable to `ON` under the condition that there is no performance regression.

### tidb_opt_insubq_to_join_and_agg {#tidb-opt-insubq-to-join-and-agg}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `ON`
-   This variable is used to set whether to enable the optimization rule that converts a subquery to join and aggregation.
-   For example, after you enable this optimization rule, the subquery is converted as follows:

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    The subquery is converted to join as follows:

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    If `t1` is limited to be `unique` and `not null` in the `aa` column. You can use the following statement, without aggregation.

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold {#tidb-opt-join-reorder-threshold}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Integer
-   Default value: `0`
-   Range: `[0, 2147483647]`
-   This variable is used to control the selection of the TiDB Join Reorder algorithm. When the number of nodes participating in Join Reorder is greater than this threshold, TiDB selects the greedy algorithm, and when it is less than this threshold, TiDB selects the dynamic programming algorithm.
-   Currently, for OLTP queries, it is recommended to keep the default value. For OLAP queries, it is recommended to set the variable value to 10~15 to get better connection orders in OLAP scenarios.

### tidb_opt_limit_push_down_threshold {#tidb-opt-limit-push-down-threshold}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Integer
-   Default value: `100`
-   Range: `[0, 2147483647]`
-   This variable is used to set the threshold that determines whether to push the Limit or TopN operator down to TiKV.
-   If the value of the Limit or TopN operator is smaller than or equal to this threshold, these operators are forcibly pushed down to TiKV. This variable resolves the issue that the Limit or TopN operator cannot be pushed down to TiKV partly due to wrong estimation.

### tidb_opt_memory_factor {#tidb-opt-memory-factor}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Range: `[0, 2147483647]`
-   Default value: `0.001`
-   Indicates the memory cost for TiDB to store one row. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">New in v5.1.0</span> {#tidb-opt-mpp-outer-join-fixed-build-side-span-class-version-mark-new-in-v5-1-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   When the variable value is `ON`, the left join operator always uses inner table as the build side and the right join operator always uses outer table as the build side. If you set the value to `OFF`, the outer join operator can use either side of the tables as the build side.

### tidb_opt_network_factor {#tidb-opt-network-factor}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Range: `[0, 2147483647]`
-   Default value: `1.0`
-   Indicates the net cost of transferring 1 byte of data through the network. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_objective <span class="version-mark">New in v7.4.0</span> {#tidb-opt-objective-span-class-version-mark-new-in-v7-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Enumeration
-   Default value: `moderate`
-   Possible values: `moderate`, `determinate`
-   This variable controls the objective of the optimizer. `moderate` maintains the default behavior in versions prior to TiDB v7.4.0, where the optimizer tries to use more information to generate better execution plans. `determinate` mode tends to be more conservative and makes the execution plan more stable.
-   The real-time statistics are the total number of rows and the number of modified rows that are automatically updated based on DML statements. When this variable is set to `moderate` (default), TiDB generates the execution plan based on real-time statistics. When this variable is set to `determinate`, TiDB does not use real-time statistics for generating the execution plan, which will make execution plans more stable.
-   For long-term stable OLTP workload, or if the user is affirmative on the existing execution plans, it is recommended to use the `determinate` mode to reduce the possibility of unexpected execution plan changes. Additionally, you can use the [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) to prevent the statistics from being modified and further stabilize the execution plan.

### tidb_opt_ordering_index_selectivity_ratio <span class="version-mark">New in v8.0.0</span> {#tidb-opt-ordering-index-selectivity-ratio-span-class-version-mark-new-in-v8-0-0-span}

-   Scope: SESSION | GLOBAL

-   Persists to cluster: Yes

-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes

-   Type: Float

-   Default value: `-1`

-   Range: `[-1, 1]`

-   This variable controls the estimated number of rows for an index that matches the SQL statement `ORDER BY` when there are `ORDER BY` and `LIMIT` clauses in a SQL statement, but does not cover some filter conditions.

-   This addresses the same query patterns as the system variable [tidb_opt_ordering_index_selectivity_threshold](#tidb_opt_ordering_index_selectivity_threshold-new-in-v700).

-   It differs in implementation by applying a ratio or percentage of the possible range that the qualified rows will be found.

-   A value of `-1` (default) or less than `0` disables this ratio. Any value between `0` and `1` applies a ratio of 0% to 100% (for example, `0.5` corresponds to `50%`).

-   In the following examples, the table `t` has a total of 1,000,000 rows. The same query is used, but different values for `tidb_opt_ordering_index_selectivity_ratio` are used. The query in the example contains a `WHERE` clause predicate that qualifies a small percentage of rows (9,000 out of 1,000,000). There is an index that supports the `ORDER BY a` (index `ia`), but the filter on `b` is not included in this index. Depending on the actual data distribution, the rows matching the `WHERE` clause and `LIMIT 1` might be found as the first row accessed when scanning the non-filtering index, or at worst, after nearly all the rows have been processed.

-   Each example uses an index hint to demonstrate the impact on estRows. The final plan selection depends on the availability and cost of other plans.

-   The first example uses the default value `-1`, which uses the existing estimation formula. By default, a small percentage of rows are scanned for estimation before the qualified rows are found.

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

-   The second example uses `0`, which assumes that 0% of rows will be scanned before the qualified rows are found.

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

-   The third example uses `0.1`, which assumes that 10% of rows will be scanned before the qualified rows are found. This condition is highly selective, with only 1% of rows meeting the condition. Therefore, in the worst-case scenario, it might be necessary to scan 99% of rows before finding the 1% that qualify. 10% of that 99% is approximately 9.9%, which is reflected in the estRows.

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

-   The fourth example uses `1.0`, which assumes that 100% of rows will be scanned before the qualified rows are found.

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

-   The fifth example also uses `1.0`, but adds a predicate on `a`, limiting the scan range in the worst-case scenario. This is because `WHERE a <= 9000` matches the index, with approximately 9,000 rows would qualify. Given that the filter predicate on `b` is not in the index, all the approximately 9,000 rows are considered to be scanned before finding a row that matches `b <= 9000`.

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

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">New in v7.0.0</span> {#tidb-opt-ordering-index-selectivity-threshold-span-class-version-mark-new-in-v7-0-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Default value: `0`
-   Range: `[0, 1]`
-   This variable is used to control how the optimizer selects an index when there are `ORDER BY` and `LIMIT` clauses with filter conditions in a SQL statement.
-   For such queries, the optimizer considers selecting the corresponding index to satisfy the `ORDER BY` and `LIMIT` clauses (even if this index does not satisfy any filter conditions). However, due to the complexity of data distribution, the optimizer might select a suboptimal index in this scenario.
-   This variable represents a threshold. When an index exists that can satisfy filtering conditions and its selectivity estimate is lower than this threshold, the optimizer will avoid selecting an index used to satisfy `ORDER BY` and `LIMIT`. Instead, it prioritizes an index that satisfies the filtering conditions.
-   For example, when the variable is set to `0`, the optimizer maintains its default behavior; when it is set to `1`, the optimizer always prioritizes selecting indexes that satisfy the filter conditions and avoids selecting indexes that satisfy both `ORDER BY` and `LIMIT` clauses.
-   In the following example, table `t` has a total of 1,000,000 rows. When using an index on column `b`, its estimated row count is approximately 8,748, so its selectivity estimate value is about 0.0087. By default, the optimizer selects an index on column `a`. However, after setting this variable to 0.01, since the selectivity of an index on column `b` (0.0087) is less than 0.01, the optimizer selects an index on column `b`.

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

### tidb_opt_prefer_range_scan <span class="version-mark">New in v5.0</span> {#tidb-opt-prefer-range-scan-span-class-version-mark-new-in-v5-0-span}

> **Note:**
>
> Starting from v8.4.0, the default value of this variable is changed from `OFF` to `ON`.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `ON`
-   When the value of this variable is `ON`, the optimizer prefers range scans over full table scans for tables without statistics (pseudo statistics) or empty tables (zero statistics).
-   In the following example, before you enable `tidb_opt_prefer_range_scan`, the TiDB optimizer performs a full table scan. After you enable `tidb_opt_prefer_range_scan`, the optimizer selects an index range scan.

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

### tidb_opt_prefix_index_single_scan <span class="version-mark">New in v6.4.0</span> {#tidb-opt-prefix-index-single-scan-span-class-version-mark-new-in-v6-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Default value: `ON`
-   This variable controls whether the TiDB optimizer pushes down some filter conditions to the prefix index to avoid unnecessary table lookup and to improve query performance.
-   When this variable value is set to `ON`, some filter conditions are pushed down to the prefix index. Suppose that the `col` column is the index prefix column in a table. The `col is null` or `col is not null` condition in the query is handled as a filter condition on the index instead of a filter condition for the table lookup, so that unnecessary table lookup is avoided.

<details><summary><code>tidb_opt_prefix_index_single_scan</code>の使用例</summary>

Create a table with a prefix index:

```sql
CREATE TABLE t (a INT, b VARCHAR(10), c INT, INDEX idx_a_b(a, b(5)));
```

Disable `tidb_opt_prefix_index_single_scan`:

```sql
SET tidb_opt_prefix_index_single_scan = 'OFF';
```

For the following query, the execution plan uses the prefix index `idx_a_b` but requires a table lookup (the `IndexLookUp` operator appears).

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

Enable `tidb_opt_prefix_index_single_scan`:

```sql
SET tidb_opt_prefix_index_single_scan = 'ON';
```

After enabling this variable, for the following query, the execution plan uses the prefix index `idx_a_b` but does not require a table lookup.

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

### tidb_opt_projection_push_down <span class="version-mark">New in v6.1.0</span> {#tidb-opt-projection-push-down-span-class-version-mark-new-in-v6-1-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `ON`. Before v8.3.0, the default value is `OFF`.
-   Specifies whether to allow the optimizer to push the `Projection` operator down to the TiKV coprocessor. When enabled, the optimizer might push the following three types of `Projection` operators down to TiKV:
    -   演算子の最上位の式はすべて[JSONクエリ関数](/functions-and-operators/json-functions/json-functions-search.md)または[JSON value attribute functions](/functions-and-operators/json-functions/json-functions-return.md)です。例: `SELECT JSON_EXTRACT(data, '$.name') FROM users;` 。
    -   The top-level expressions of the operator include a mix of JSON query functions or JSON value attribute functions, and direct column reads. For example: `SELECT JSON_DEPTH(data), name FROM users;`.
    -   The top-level expressions of the operator are all direct column reads, and the number of output columns is less than the number of input columns. For example: `SELECT name FROM users;`.
-   The final decision to push down a `Projection` operator also depends on the optimizer's comprehensive evaluation of query cost.
-   For TiDB clusters that are upgraded from a version earlier than v8.3.0 to v8.3.0 or later, the default value of this variable is `OFF`.

### tidb_opt_range_max_size <span class="version-mark">New in v6.4.0</span> {#tidb-opt-range-max-size-span-class-version-mark-new-in-v6-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Default value: `67108864` (64 MiB)
-   Scope: `[0, 9223372036854775807]`
-   Unit: Bytes
-   This variable is used to set the upper limit of memory usage for the optimizer to build scan ranges. When the variable value is `0`, there is no memory limit for building scan ranges. If building exact scan ranges consumes memory that exceeds the limit, the optimizer uses more relaxed scan ranges (such as `[[NULL,+inf]]`). If the execution plan does not use exact scan ranges, you can increase the value of this variable to let the optimizer build exact scan ranges.

The usage example of this variable is as follows:

<details><summary><code>tidb_opt_range_max_size</code>使用例</summary>

View the default value of this variable. From the result, you can see that the optimizer uses up to 64 MiB of memory to build scan ranges.

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

In the 64 MiB memory upper limit, the optimizer builds the following exact scan ranges `[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`, as shown in the following execution plan result.

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

Now set the upper limit of memory usage for the optimizer to build scan ranges to 1500 bytes.

```sql
SET @@tidb_opt_range_max_size = 1500;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

In the 1500-byte memory limit, the optimizer builds more relaxed scan ranges `[10,10], [20,20], [30,30]`, and uses a warning to inform the user that the memory usage required to build exact scan ranges exceeds the limit of `tidb_opt_range_max_size`.

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

Then set the upper limit of memory usage to 100 bytes:

```sql
set @@tidb_opt_range_max_size = 100;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

In the 100-byte memory limit, the optimizer chooses `IndexFullScan`, and uses a warning to inform the user that the memory required to build exact scan ranges exceeds the limit of `tidb_opt_range_max_size`.

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

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Range: `[0, 2147483647]`
-   Default value: `1.5`
-   Indicates the cost for TiKV to scan one row of data from the disk in ascending order. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_seek_factor {#tidb-opt-seek-factor}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Range: `[0, 2147483647]`
-   Default value: `20`
-   Indicates the start-up cost for TiDB to request data from TiKV. This variable is internally used in the [コストモデル](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_skew_distinct_agg <span class="version-mark">New in v6.2.0</span> {#tidb-opt-skew-distinct-agg-span-class-version-mark-new-in-v6-2-0-span}

> **Note:**
>
> The query performance optimization by enabling this variable is effective **only for TiFlash**.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   This variable sets whether the optimizer rewrites the aggregate functions with `DISTINCT` to the two-level aggregate functions, such as rewriting `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b` to `SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`. When the aggregation column has serious skew and the `DISTINCT` column has many different values, this rewriting can avoid the data skew in the query execution and improve the query performance.

### tidb_opt_three_stage_distinct_agg <span class="version-mark">New in v6.3.0</span> {#tidb-opt-three-stage-distinct-agg-span-class-version-mark-new-in-v6-3-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `ON`
-   This variable specifies whether to rewrite a `COUNT(DISTINCT)` aggregation into a three-stage aggregation in MPP mode.
-   This variable currently applies to an aggregation that only contains one `COUNT(DISTINCT)`.

### tidb_opt_tiflash_concurrency_factor {#tidb-opt-tiflash-concurrency-factor}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: YES
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Float
-   Range: `[0, 2147483647]`
-   Default value: `24.0`
-   Indicates the concurrency number of TiFlash computation. This variable is internally used in the Cost Model, and it is NOT recommended to modify its value.

### tidb_opt_use_invisible_indexes <span class="version-mark">New in v8.0.0</span> {#tidb-opt-use-invisible-indexes-span-class-version-mark-new-in-v8-0-0-span}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   This variable controls whether the optimizer can select [非表示のインデックス](/sql-statements/sql-statement-create-index.md#invisible-index) for query optimization in the current session. Invisible indexes are maintained by DML statements, but will not be used by the query optimizer. This is useful in scenarios where you want to double-check before removing an index permanently. When the variable is set to `ON`, the optimizer can select invisible indexes for query optimization in the session.

### tidb_opt_write_row_id {#tidb-opt-write-row-id}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to control whether to allow `INSERT`, `REPLACE`, and `UPDATE` statements to operate on the `_tidb_rowid` column. This variable can be used only when you import data using TiDB tools.

### tidb_optimizer_selectivity_level {#tidb-optimizer-selectivity-level}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Integer
-   Default value: `0`
-   Range: `[0, 2147483647]`
-   This variable controls the iteration of the optimizer's estimation logic. After changing the value of this variable, the estimation logic of the optimizer will change greatly. Currently, `0` is the only valid value. It is not recommended to set it to other values.

### tidb_partition_prune_mode <span class="version-mark">New in v5.1</span> {#tidb-partition-prune-mode-span-class-version-mark-new-in-v5-1-span}

> **Warning:**
>
> Starting from v8.5.0, setting this variable to `static` or `static-only` returns a warning. This variable will be deprecated in a future release.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Enumeration
-   Default value: `dynamic`
-   Possible values: `static`, `dynamic`, `static-only`, `dynamic-only`
-   パーティション化されたテーブルに`dynamic`と`static`モードのどちらを使用するかを指定します。動的パーティションは、完全なテーブル レベルの統計、またはグローバル統計が収集された後にのみ有効になることに注意してください。グローバル統計の収集が完了する前に`dynamic`プルーニング モードを有効にすると、グローバル統計が完全に収集されるまで TiDB は`static`モードのままになります。グローバル統計の詳細については、 [動的プルーニングモードでパーティションテーブルの統計を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。動的プルーニング モードの詳細については、 [Dynamic Pruning Mode for Partitioned Tables](/partitioned-table.md#dynamic-pruning-mode)参照してください。

### tidb_persist_analyze_options <span class="version-mark">New in v5.4.0</span> {#tidb-persist-analyze-options-span-class-version-mark-new-in-v5-4-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable controls whether to enable the [構成の永続性を分析する](/statistics.md#persist-analyze-configurations) feature.

### tidb_pessimistic_txn_fair_locking <span class="version-mark">New in v7.0.0</span> {#tidb-pessimistic-txn-fair-locking-span-class-version-mark-new-in-v7-0-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   Determines whether to use enhanced pessimistic locking wake-up model for pessimistic transactions. This model strictly controls the wake-up order of pessimistic transactions in the pessimistic locking single-point conflict scenarios to avoid unnecessary wake-ups. It greatly reduces the uncertainty brought by the randomness of the existing wake-up mechanism. If you encounter frequent single-point pessimistic locking conflicts in your business scenario (such as frequent updates to the same row of data), and thus cause frequent statement retries, high tail latency, or even occasional `pessimistic lock retry limit reached` errors, you can try to enable this variable to solve the problem.
-   This variable is disabled by default for TiDB clusters that are upgraded from versions earlier than v7.0.0 to v7.0.0 or later versions.

> **Note:**
>
> -   Depending on the specific business scenario, enabling this option might cause a certain degree of throughput reduction (average latency increase) for transactions with frequent lock conflicts.
> -   This option only takes effect on statements that need to lock a single key. If a statement needs to lock multiple rows at the same time, this option will not take effect on such statements.
> -   This feature is introduced in v6.6.0 by the [`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660) variable, which is disabled by default.

### tidb_placement_mode <span class="version-mark">New in v6.0.0</span> {#tidb-placement-mode-span-class-version-mark-new-in-v6-0-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Enumeration
-   Default value: `STRICT`
-   Possible values: `STRICT`, `IGNORE`
-   This variable controls whether DDL statements ignore the [SQLで指定された配置ルール](/placement-rules-in-sql.md). When the variable value is `IGNORE`, all placement rule options are ignored.
-   It is intended to be used by logical dump/restore tools to ensure that tables can always be created even if invalid placement rules are assigned. This is similar to how mysqldump writes `SET FOREIGN_KEY_CHECKS=0;` to the start of every dump file.

### <code>tidb_plan_cache_invalidation_on_fresh_stats</code> <span class="version-mark">New in v7.1.0</span> {#code-tidb-plan-cache-invalidation-on-fresh-stats-code-span-class-version-mark-new-in-v7-1-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable controls whether to invalidate the plan cache automatically when statistics on related tables are updated.
-   After enabling this variable, plan cache can make use of statistics more sufficiently to generate execution plans. For example:
    -   If execution plans are generated before statistics are available, plan cache re-generates execution plans once the statistics are available.
    -   If the data distribution of a table changes, causing the previously optimal execution plan to become non-optimal, plan cache re-generates execution plans after the statistics are re-collected.
-   This variable is disabled by default for TiDB clusters that are upgraded from a version earlier than v7.1.0 to v7.1.0 or later.

### <code>tidb_plan_cache_max_plan_size</code> <span class="version-mark">New in v7.1.0</span> {#code-tidb-plan-cache-max-plan-size-code-span-class-version-mark-new-in-v7-1-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Default value: `2097152` (which is 2 MiB)
-   Range: `[0, 9223372036854775807]`, in bytes. The memory format with the units "KiB|MiB|GiB|TiB" is also supported. `0` means no limit.
-   この変数は、準備済みプラン キャッシュまたは準備されていないプラン キャッシュにキャッシュできるプランの最大サイズを制御します。プランのサイズがこの値を超えると、プランはキャッシュされません。詳細については、 [準備されたプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)および[Non-prepared plan cache](/sql-plan-management.md#usage)参照してください。

### tidb_pprof_sql_cpu <span class="version-mark">New in v4.0</span> {#tidb-pprof-sql-cpu-span-class-version-mark-new-in-v4-0-span}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: GLOBAL
-   Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `0`
-   Range: `[0, 1]`
-   This variable is used to control whether to mark the corresponding SQL statement in the profile output to identify and troubleshoot performance issues.

### tidb_prefer_broadcast_join_by_exchange_data_size <span class="version-mark">New in v7.1.0</span> {#tidb-prefer-broadcast-join-by-exchange-data-size-span-class-version-mark-new-in-v7-1-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Default value: `OFF`
-   This variable controls whether to use the algorithm with the minimum overhead of network transmission when TiDB selects the [MPPハッシュ結合アルゴリズム](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode). If this variable is enabled, TiDB estimates the size of the data to be exchanged in the network using `Broadcast Hash Join` and `Shuffled Hash Join` respectively, and then chooses the one with the smaller size.
-   この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)有効になりません。

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">New in v6.1.0</span> {#tidb-prepared-plan-cache-memory-guard-ratio-span-class-version-mark-new-in-v6-1-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Float
-   Default value: `0.1`
-   Range: `[0, 1]`
-   The threshold at which the prepared plan cache triggers a memory protection mechanism. For details, see [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md).
-   This setting was previously a `tidb.toml` option (`prepared-plan-cache.memory-guard-ratio`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_prepared_plan_cache_size <span class="version-mark">New in v6.1.0</span> {#tidb-prepared-plan-cache-size-span-class-version-mark-new-in-v6-1-0-span}

> **Warning:**
>
> Starting from v7.1.0, this variable is deprecated. Instead, use [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710) for setting.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `100`
-   Range: `[1, 100000]`
-   The maximum number of plans that can be cached in a session. For details, see [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md).
-   This setting was previously a `tidb.toml` option (`prepared-plan-cache.capacity`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_projection_concurrency {#tidb-projection-concurrency}

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `-1`
-   Range: `[-1, 256]`
-   Unit: Threads
-   This variable is used to set the concurrency of the `Projection` operator.
-   A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_query_log_max_len {#tidb-query-log-max-len}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `4096` (4 KiB)
-   Range: `[0, 1073741824]`
-   Unit: Bytes
-   The maximum length of the SQL statement output. When the output length of a statement is larger than the `tidb_query_log_max_len` value, the statement is truncated to output.
-   This setting was previously also available as a `tidb.toml` option (`log.query-log-max-len`), but is only a system variable starting from TiDB v6.1.0.

### tidb_rc_read_check_ts <span class="version-mark">New in v6.0.0</span> {#tidb-rc-read-check-ts-span-class-version-mark-new-in-v6-0-0-span}

> **Warning:**
>
> -   This feature is incompatible with [`replica-read`](#tidb_replica_read-new-in-v40). Do not enable `tidb_rc_read_check_ts` and `replica-read` at the same time.
> -   If your client uses a cursor, it is not recommended to enable `tidb_rc_read_check_ts` in case that the previous batch of returned data has already been used by the client and the statement eventually fails.
> -   Starting from v7.0.0, this variable is no longer valid for the cursor fetch read mode that uses the prepared statement protocol.

-   Scope: GLOBAL
-   Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to optimize the timestamp acquisition, which is suitable for scenarios with read-committed isolation level where read-write conflicts are rare. Enabling this variable can avoid the latency and cost of getting the global timestamp, and can optimize the transaction-level read latency.
-   If read-write conflicts are severe, enabling this feature will increase the cost and latency of getting the global timestamp, and might cause performance regression. For details, see [コミット読み取り分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level).

### tidb_rc_write_check_ts <span class="version-mark">New in v6.3.0</span> {#tidb-rc-write-check-ts-span-class-version-mark-new-in-v6-3-0-span}

> **Warning:**
>
> This feature is currently incompatible with [`replica-read`](#tidb_replica_read-new-in-v40). After this variable is enabled, all requests sent by the client cannot use `replica-read`. Therefore, do not enable `tidb_rc_write_check_ts` and `replica-read` at the same time.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to optimize the acquisition of timestamps and is suitable for scenarios with few point-write conflicts in `READ-COMMITTED` isolation level of pessimistic transactions. Enabling this variable can avoid the latency and overhead brought by obtaining the global timestamps during the execution of point-write statements. Currently, this variable is applicable to three types of point-write statements: `UPDATE`, `DELETE`, and `SELECT ...... FOR UPDATE`. A point-write statement refers to a write statement that uses the primary key or unique key as a filter condition and the final execution operator contains `POINT-GET`.
-   If the point-write conflicts are severe, enabling this variable will increase extra overhead and latency, resulting in performance regression. For details, see [コミット読み取り分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level).

### tidb_read_consistency <span class="version-mark">New in v5.4.0</span> {#tidb-read-consistency-span-class-version-mark-new-in-v5-4-0-span}

-   Scope: SESSION
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用: はい ( [non-transactional DML statements](/non-transactional-dml.md)が存在する場合、ヒントを使用してこの変数の値を変更しても有効にならない可能性があることに注意してください。)
-   Type: String
-   Default value: `strict`
-   This variable is used to control the read consistency for an auto-commit read statement.
-   If the variable value is set to `weak`, the locks encountered by the read statement are skipped directly and the read execution might be faster, which is the weak consistency read mode. However, the transaction semantics (such as atomicity) and distributed consistency (such as linearizability) are not guaranteed.
-   For user scenarios where the auto-commit read needs to return fast and weak consistency read results are acceptable, you can use the weak consistency read mode.

### tidb_read_staleness <span class="version-mark">New in v5.4.0</span> {#tidb-read-staleness-span-class-version-mark-new-in-v5-4-0-span}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `0`
-   Range: `[-2147483648, 0]`
-   This variable is used to set the time range of historical data that TiDB can read in the current session. After setting the value, TiDB selects a timestamp as new as possible from the range allowed by this variable, and all subsequent read operations are performed against this timestamp. For example, if the value of this variable is set to `-5`, on the condition that TiKV has the corresponding historical version's data, TiDB selects a timestamp as new as possible within a 5-second time range.

### tidb_record_plan_in_slow_log {#tidb-record-plan-in-slow-log}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: GLOBAL
-   Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable is used to control whether to include the execution plan of slow queries in the slow log.

### tidb_redact_log {#tidb-redact-log}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Enumeration
-   Default value: `OFF`
-   Possible values: `OFF`, `ON`, `MARKER`
-   This variable controls whether to hide the user information in the SQL statement being recorded into the TiDB log and slow log.
-   The default value is `OFF`, which means that the user information is not processed in any way.
-   When you set the variable to `ON`, the user information is hidden. For example, if the executed SQL statement is `INSERT INTO t VALUES (1,2)`, the statement is recorded as `INSERT INTO t VALUES (?,?)` in the log.
-   When you set the variable to `MARKER`, the user information is wrapped in `‹ ›`. For example, if the executed SQL statement is `INSERT INTO t VALUES (1,2)`, the statement is recorded as `INSERT INTO t VALUES (‹1›,‹2›)` in the log. If user data contains `‹` or `›`, `‹` is escaped as `‹‹`, and `›` is escaped as `››`. Based on the marked logs, you can decide whether to desensitize the marked information when the logs are displayed.

### tidb_regard_null_as_point <span class="version-mark">New in v5.4.0</span> {#tidb-regard-null-as-point-span-class-version-mark-new-in-v5-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable controls whether the optimizer can use a query condition including null equivalence as a prefix condition for index access.
-   This variable is enabled by default. When it is enabled, the optimizer can reduce the volume of index data to be accessed, which accelerates query execution. For example, if a query involves multiple-column indexes `index(a, b)` and the query condition contains `a<=>null and b=1`, the optimizer can use both `a<=>null` and `b=1` in the query condition for index access. If the variable is disabled, because `a<=>null and b=1` includes the null equivalence condition, the optimizer does not use `b=1` for index access.

### tidb_remove_orderby_in_subquery <span class="version-mark">New in v6.1.0</span> {#tidb-remove-orderby-in-subquery-span-class-version-mark-new-in-v6-1-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: Before v7.2.0, the default value is `OFF`. Starting from v7.2.0, the default value is `ON`.
-   Specifies whether to remove `ORDER BY` clause in a subquery.
-   In the ISO/IEC SQL standard, `ORDER BY` is mainly used to sort the results of top-level queries. For subqueries, the standard does not require that the results be sorted by `ORDER BY`.
-   To sort subquery results, you can usually handle it in the outer query, such as using the window function or using `ORDER BY` again in the outer query. Doing so ensures the order of the final result set.

### tidb_replica_read <span class="version-mark">New in v4.0</span> {#tidb-replica-read-span-class-version-mark-new-in-v4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Enumeration
-   Default value: `leader`
-   Possible values: `leader`, `follower`, `leader-and-follower`, `prefer-leader`, `closest-replicas`, `closest-adaptive`, and `learner`. The `learner` value is introduced in v6.6.0.
-   This variable is used to control where TiDB reads data.
-   For more details about usage and implementation, see [Followerが読んだ](/follower-read.md).

### tidb_restricted_read_only <span class="version-mark">New in v5.2.0</span> {#tidb-restricted-read-only-span-class-version-mark-new-in-v5-2-0-span}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   `tidb_restricted_read_only`と[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)同様に動作します。ほとんどの場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを使用する必要があります。
-   Users with the `SUPER` or `SYSTEM_VARIABLES_ADMIN` privilege can modify this variable. However, if the [Security強化モード](#tidb_enable_enhanced_security) is enabled, the additional `RESTRICTED_VARIABLES_ADMIN` privilege is required to read or modify this variable.
-   `tidb_restricted_read_only` affects [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) in the following cases:
    -   Setting `tidb_restricted_read_only` to `ON` will update [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) to `ON`.
    -   Setting `tidb_restricted_read_only` to `OFF` leaves [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) unchanged.
    -   If `tidb_restricted_read_only` is `ON`, [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) cannot be set to `OFF`.
-   TiDB の DBaaS プロバイダーの場合、TiDB クラスターが別のデータベースのダウンストリーム データベースである場合、TiDB クラスターを読み取り専用にするには、 [Security強化モード](#tidb_enable_enhanced_security)有効にした`tidb_restricted_read_only`使用する必要があります。これにより、顧客が[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)使用してクラスターを書き込み可能にすることができなくなります。これを実現するには、 [Security強化モード](#tidb_enable_enhanced_security)有効にし、 `SYSTEM_VARIABLES_ADMIN`および`RESTRICTED_VARIABLES_ADMIN`権限を持つ管理者ユーザーを使用して`tidb_restricted_read_only`制御し、データベース ユーザーが`SUPER`権限を持つルート ユーザーを使用して[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを制御できるようにする必要があります。
-   This variable controls the read-only status of the entire cluster. When the variable is `ON`, all TiDB servers in the entire cluster are in the read-only mode. In this case, TiDB only executes the statements that do not modify data, such as `SELECT`, `USE`, and `SHOW`. For other statements such as `INSERT` and `UPDATE`, TiDB rejects executing those statements in the read-only mode.
-   Enabling the read-only mode using this variable only ensures that the entire cluster finally enters the read-only status. If you have changed the value of this variable in a TiDB cluster but the change has not yet propagated to other TiDB servers, the un-updated TiDB servers are still **not** in the read-only mode.
-   TiDB checks the read-only flag before SQL statements are executed. Since v6.2.0, the flag is also checked before SQL statements are committed. This helps prevent the case where long-running [自動コミット](/transaction-overview.md#autocommit) statements might modify data after the server has been placed in read-only mode.
-   When this variable is enabled, TiDB handles the uncommitted transactions in the following ways:
    -   For uncommitted read-only transactions, you can commit the transactions normally.
    -   For uncommitted transactions that are not read-only, SQL statements that perform write operations in these transactions are rejected.
    -   For uncommitted read-only transactions with modified data, the commit of these transactions is rejected.
-   After the read-only mode is enabled, all users (including the users with the `SUPER` privilege) cannot execute the SQL statements that might write data unless the user is explicitly granted the `RESTRICTED_REPLICA_WRITER_ADMIN` privilege.

### tidb_request_source_type <span class="version-mark">New in v7.4.0</span> {#tidb-request-source-type-span-class-version-mark-new-in-v7-4-0-span}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: String
-   Default value: `""`
-   Possible values: `"ddl"`, `"stats"`, `"br"`, `"lightning"`, `"background"`
-   This variable is used to explicitly specify the task type for the current session, which is identified and controlled by [リソース管理](/tidb-resource-control.md). For example: `SET @@tidb_request_source_type = "background"`.

### tidb_resource_control_strict_mode <span class="version-mark">New in v8.2.0</span> {#tidb-resource-control-strict-mode-span-class-version-mark-new-in-v8-2-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   この変数は、権限制御が[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)ステートメントと[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザヒントに適用されるかどうかを制御します。このシステム変数が`ON`に設定されている場合、これら 2 つの方法で現在のセッションまたは現在のステートメントのバインドされたリソースグループを変更するには、 `SUPER` 、 `RESOURCE_GROUP_ADMIN` 、または`RESOURCE_GROUP_USER`の権限が必要です。 `OFF`に設定されている場合、これらの権限はいずれも必要なく、動作はこの変数のない以前の TiDB バージョンと同じです。
-   When you upgrade your TiDB cluster from an earlier version to v8.2.0 or later, the default value of this variable is set to `OFF`, which means this feature is disabled by default.

### tidb_retry_limit {#tidb-retry-limit}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `10`
-   Range: `[-1, 9223372036854775807]`
-   This variable is used to set the maximum number of the retries for optimistic transactions. When a transaction encounters retryable errors (such as transaction conflicts, very slow transaction commit, or table schema changes), this transaction is re-executed according to this variable. Note that setting `tidb_retry_limit` to `0` disables the automatic retry. This variable only applies to optimistic transactions, not to pessimistic transactions.

### tidb_row_format_version {#tidb-row-format-version}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `2`
-   Range: `[1, 2]`
-   Controls the format version of the newly saved data in the table. In TiDB v4.0, the [新しいstorage行形式](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2018-07-19-row-format.md) version `2` is used by default to save new data.
-   If you upgrade from a TiDB version earlier than v4.0.0 to v4.0.0 or later versions, the format version is not changed, and TiDB continues to use the old format of version `1` to write data to the table, which means that **only newly created clusters use the new data format by default**.
-   Note that modifying this variable does not affect the old data that has been saved, but applies the corresponding version format only to the newly written data after modifying this variable.

### tidb_runtime_filter_mode <span class="version-mark">New in v7.2.0</span> {#tidb-runtime-filter-mode-span-class-version-mark-new-in-v7-2-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Enumeration
-   Default value: `OFF`
-   Possible values: `OFF`, `LOCAL`
-   Controls the mode of Runtime Filter, that is, the relationship between the **Filter Sender operator** and **Filter Receiver operator**. There are two modes: `OFF` and `LOCAL`. `OFF` means disabling Runtime Filter. `LOCAL` means enabling Runtime Filter in the local mode. For more information, see [ランタイムフィルターモード](/runtime-filter.md#runtime-filter-mode).

### tidb_runtime_filter_type <span class="version-mark">New in v7.2.0</span> {#tidb-runtime-filter-type-span-class-version-mark-new-in-v7-2-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Enumeration
-   Default value: `IN`
-   Possible values: `IN`
-   Controls the type of predicate used by the generated Filter operator. Currently, only one type is supported: `IN`. For more information, see [ランタイムフィルタータイプ](/runtime-filter.md#runtime-filter-type).

### tidb_scatter_region {#tidb-scatter-region}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Enumeration
-   Default value: `""`
-   Possible values: `""`, `table`, `global`
-   If the `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` parameters are set during table creation, then the system automatically splits the table into a specified number of Regions upon successful creation. This variable controls the scattering strategy for these split Regions. TiDB processes the Regions based on the selected scattering strategy. It is important to note that because the table creation operation waits for the scattering process to complete before returning a success status, enabling this variable might significantly increase the execution time of the `CREATE TABLE` statement. Compared to the scenario where this variable is disabled, the execution time could be several times longer. Descriptions of possible values are as follows:
    -   `""`: the default value, indicating that the Regions of the table are not scattered after table creation.
    -   `table`: indicates that if you set the `PRE_SPLIT_REGIONS` or `SHARD_ROW_ID_BITS` attribute when you create a table, in the scenario of pre-splitting multiple Regions, the Regions of these tables are scattered according to the granularity of the tables. However, if you do not set the preceding attribute when you create a table, in the scenario of creating a large number of tables rapidly, it will cause the Regions of these tables to be concentrated on a few TiKV nodes, resulting in an uneven distribution of Regions.
    -   `global`: indicates that TiDB scatters the Regions of newly created tables according to the data distribution of the entire cluster. Especially when creating a large number of tables rapidly, using the `global` option helps prevent Regions from becoming overly concentrated on a few TiKV nodes, ensuring a more balanced distribution of Regions across the cluster.

### tidb_schema_cache_size <span class="version-mark">New in v8.0.0</span> {#tidb-schema-cache-size-span-class-version-mark-new-in-v8-0-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `536870912` (512 MiB)
-   Range: `0` or `[67108864, 9223372036854775807]`
-   Before TiDB v8.4.0, the default value of this variable is `0`.
-   Starting from TiDB v8.4.0, the default value is `536870912`. When you upgrade from an earlier version to v8.4.0 or later, the old value set in the earlier version is used.
-   This variable controls the size of the schema cache in TiDB. The unit is byte. Setting this variable to `0` means the cache limit feature is disabled. To enable this feature, you need to set a value within the range `[67108864, 9223372036854775807]`. TiDB will use this value as the maximum available memory limit and apply the Least Recently Used (LRU) algorithm to cache the required tables, effectively reducing the memory used by schema information.

### tidb_schema_version_cache_limit <span class="version-mark">New in v7.4.0</span> {#tidb-schema-version-cache-limit-span-class-version-mark-new-in-v7-4-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `16`
-   Range: `[2, 255]`
-   This variable limits how many historical schema versions can be cached in a TiDB instance. The default value is `16`, which means that TiDB caches 16 historical schema versions by default.
-   Generally, you do not need to modify this variable. When the [ステイル読み取り](/stale-read.md) feature is used and DDL operations are executed very frequently, it will cause the schema version to change very frequently. Consequently, when Stale Read tries to obtain schema information from a snapshot, it might take a lot of time to rebuild the information due to schema cache misses. In this case, you can increase the value of `tidb_schema_version_cache_limit` (for example, `32`) to avoid the problem of schema cache misses.
-   Modifying this variable causes the memory usage of TiDB to increase slightly. Monitor the memory usage of TiDB to avoid OOM problems.

### tidb_server_memory_limit <span class="version-mark">New in v6.4.0</span> {#tidb-server-memory-limit-span-class-version-mark-new-in-v6-4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `80%`
-   Range:
    -   You can set the value in the percentage format, which means the percentage of the memory usage relative to the total memory. The value range is `[1%, 99%]`.
    -   You can also set the value in memory size. The value range is `0` and `[536870912, 9223372036854775807]` in bytes. The memory format with the units "KiB|MiB|GiB|TiB" is supported. `0` means no memory limit.
    -   If this variable is set to a memory size that is less than 512 MiB but not `0`, TiDB uses 512 MiB as the actual size.
-   This variable specifies the memory limit for a TiDB instance. When the memory usage of TiDB reaches the limit, TiDB cancels the currently running SQL statement with the highest memory usage. After the SQL statement is successfully canceled, TiDB tries to call Golang GC to immediately reclaim memory to relieve memory stress as soon as possible.
-   Only the SQL statements with more memory usage than the [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640) limit are selected as the SQL statements to be canceled first.
-   Currently, TiDB cancels only one SQL statement at a time. After TiDB completely cancels a SQL statement and recovers resources, if the memory usage is still greater than the limit set by this variable, TiDB starts the next cancel operation.

### tidb_server_memory_limit_gc_trigger <span class="version-mark">New in v6.4.0</span> {#tidb-server-memory-limit-gc-trigger-span-class-version-mark-new-in-v6-4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `70%`
-   Range: `[50%, 99%]`
-   The threshold at which TiDB tries to trigger GC. When the memory usage of TiDB reaches the value of `tidb_server_memory_limit` * the value of `tidb_server_memory_limit_gc_trigger`, TiDB will actively trigger a Golang GC operation. Only one GC operation will be triggered in one minute.

### tidb_server_memory_limit_sess_min_size <span class="version-mark">New in v6.4.0</span> {#tidb-server-memory-limit-sess-min-size-span-class-version-mark-new-in-v6-4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `134217728` (which is 128 MiB)
-   Range: `[128, 9223372036854775807]`, in bytes. The memory format with the units "KiB|MiB|GiB|TiB" is also supported.
-   After you enable the memory limit, TiDB will terminate the SQL statement with the highest memory usage on the current instance. This variable specifies the minimum memory usage of the SQL statement to be terminated. If the memory usage of a TiDB instance that exceeds the limit is caused by too many sessions with low memory usage, you can properly lower the value of this variable to allow more sessions to be canceled.

### tidb_service_scope <span class="version-mark">New in v7.4.0</span> {#tidb-service-scope-span-class-version-mark-new-in-v7-4-0-span}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: GLOBAL
-   Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: String
-   Default value: ""
-   Optional value: a string with a length of up to 64 characters. Valid characters include digits `0-9`, letters `a-zA-Z`, underscores `_`, and hyphens `-`.
-   この変数はインスタンス レベルのシステム変数です。これを使用して、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)の下にある各 TiDB ノードのサービス スコープを制御できます。DXF は、この変数の値に基づいて、分散タスクを実行するようにスケジュールできる TiDB ノードを決定します。具体的なルールについては、 [Task scheduling](/tidb-distributed-execution-framework.md#task-scheduling)参照してください。

### tidb_session_alias <span class="version-mark">New in v7.4.0</span> {#tidb-session-alias-span-class-version-mark-new-in-v7-4-0-span}

-   Scope: SESSION
-   Persists to cluster: No
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Default value: ""
-   You can use this variable to customize the value of the `session_alias` column in the logs related to the current session, which helps identify the session in troubleshooting. This setting affects the logs of multiple nodes involved in the statement execution (including TiKV). The maximum length of this variable is limited to 64 characters, and any characters exceeding the length will be truncated automatically. Spaces at the end of the value will also be removed automatically.

### tidb_session_plan_cache_size <span class="version-mark">New in v7.1.0</span> {#tidb-session-plan-cache-size-span-class-version-mark-new-in-v7-1-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `100`
-   Range: `[1, 100000]`
-   この変数は、キャッシュできるプランの最大数を制御します。1 と[準備されたプランキャッシュ](/sql-prepared-plan-cache.md) [non-prepared plan cache](/sql-non-prepared-plan-cache.md)同じキャッシュを共有します。
-   When you upgrade from an earlier version to a v7.1.0 or later version, this variable remains the same value as [`tidb_prepared_plan_cache_size`](#tidb_prepared_plan_cache_size-new-in-v610)

### tidb_shard_allocate_step <span class="version-mark">New in v5.0</span> {#tidb-shard-allocate-step-span-class-version-mark-new-in-v5-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `9223372036854775807`
-   Range: `[1, 9223372036854775807]`
-   この変数は、 [`AUTO_RANDOM`](/auto-random.md)または[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)属性に割り当てられる連続 ID の最大数を制御します。通常、1 つのトランザクションでは、 `AUTO_RANDOM` ID または`SHARD_ROW_ID_BITS`の注釈付き行 ID が増分され、連続します。この変数を使用すると、大規模なトランザクション シナリオでのホットスポットの問題を解決できます。

### tidb_shard_row_id_bits <span class="version-mark">New in v8.4.0</span> {#tidb-shard-row-id-bits-span-class-version-mark-new-in-v8-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `0`
-   Range: `[0, 15]`
-   This variable is used to set the default number of row ID shards for newly created tables. When this variable is set to a non-zero value, TiDB will automatically apply this attribute to tables that allow the use of `SHARD_ROW_ID_BITS` (for example, `NONCLUSTERED` tables) when executing `CREATE TABLE` statements. For more information, see [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md).

### tidb_simplified_metrics {#tidb-simplified-metrics}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   When this variable is enabled, TiDB does not collect or record the metrics that are not used in the Grafana panels.

### tidb_skip_ascii_check <span class="version-mark">New in v5.0</span> {#tidb-skip-ascii-check-span-class-version-mark-new-in-v5-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to set whether to skip ASCII validation.
-   Validating ASCII characters affects the performance. When you are sure that the input characters are valid ASCII characters, you can set the variable value to `ON`.

### tidb_skip_isolation_level_check {#tidb-skip-isolation-level-check}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   After this switch is enabled, if an isolation level unsupported by TiDB is assigned to `tx_isolation`, no error is reported. This helps improve compatibility with applications that set (but do not depend on) a different isolation level.

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_missing_partition_stats <span class="version-mark">New in v7.3.0</span> {#tidb-skip-missing-partition-stats-span-class-version-mark-new-in-v7-3-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   When accessing a partitioned table in [動的剪定モード](/partitioned-table.md#dynamic-pruning-mode), TiDB aggregates the statistics of each partition to generate global statistics. This variable controls the generation of global statistics when partition statistics are missing.

    -   If this variable is `ON`, TiDB skips missing partition statistics when generating global statistics so the generation of global statistics is not affected.
    -   If this variable is `OFF`, TiDB stops generating global statistics when it detects any missing partition statistics.

### tidb_skip_utf8_check {#tidb-skip-utf8-check}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to set whether to skip UTF-8 validation.
-   Validating UTF-8 characters affects the performance. When you are sure that the input characters are valid UTF-8 characters, you can set the variable value to `ON`.

> **Note:**
>
> If the character check is skipped, TiDB might fail to detect illegal UTF-8 characters written by the application, cause decoding errors when `ANALYZE` is executed, and introduce other unknown encoding issues. If your application cannot guarantee the validity of the written string, it is not recommended to skip the character check.

### tidb_slow_log_threshold {#tidb-slow-log-threshold}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: GLOBAL
-   Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `300`
-   Range: `[-1, 9223372036854775807]`
-   Unit: Milliseconds
-   This variable outputs the threshold value of the time consumed by the slow log, and is set to 300 milliseconds by default. When the time consumed by a query is larger than this value, this query is considered as a slow query and its log is output to the slow query log. Note that when the output level of [`log.level`](https://docs.pingcap.com/tidb/dev/tidb-configuration-file#level) is `"debug"`, all queries are recorded in the slow query log, regardless of the setting of this variable.

### tidb_slow_query_file {#tidb-slow-query-file}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: ""
-   When `INFORMATION_SCHEMA.SLOW_QUERY` is queried, only the slow query log name set by `slow-query-file` in the configuration file is parsed. The default slow query log name is "tidb-slow.log". To parse other logs, set the `tidb_slow_query_file` session variable to a specific file path, and then query `INFORMATION_SCHEMA.SLOW_QUERY` to parse the slow query log based on the set file path.

<CustomContent platform="tidb">

For details, see [遅いクエリを特定する](/identify-slow-queries.md).

</CustomContent>

### tidb_snapshot {#tidb-snapshot}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: ""
-   This variable is used to set the time point at which the data is read by the session. For example, when you set the variable to "2017-11-11 20:20:20" or a TSO number like "400036290571534337", the current session reads the data of this moment.

### tidb_source_id <span class="version-mark">New in v6.5.0</span> {#tidb-source-id-span-class-version-mark-new-in-v6-5-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `1`
-   Range: `[1, 15]`

<CustomContent platform="tidb">

-   This variable is used to configure the different cluster IDs in a [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md) cluster.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable is used to configure the different cluster IDs in a [双方向レプリケーション](https://docs.pingcap.com/tidb/stable/ticdc-bidirectional-replication) cluster.

</CustomContent>

### tidb_stats_cache_mem_quota <span class="version-mark">New in v6.1.0</span> {#tidb-stats-cache-mem-quota-span-class-version-mark-new-in-v6-1-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Unit: Byte
-   Default value: `0`, which means that the memory quota is automatically set to half of the total memory size of the TiDB instance.
-   Range: `[0, 1099511627776]`
-   This variable sets the memory quota for the TiDB statistics cache.

### tidb_stats_load_pseudo_timeout <span class="version-mark">New in v5.4.0</span> {#tidb-stats-load-pseudo-timeout-span-class-version-mark-new-in-v5-4-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable controls how TiDB behaves when the waiting time of SQL optimization reaches the timeout to synchronously load complete column statistics. The default value `ON` means that the SQL optimization gets back to using pseudo statistics after the timeout. If this variable to `OFF`, SQL execution fails after the timeout.

### tidb_stats_load_sync_wait <span class="version-mark">New in v5.4.0</span> {#tidb-stats-load-sync-wait-span-class-version-mark-new-in-v5-4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Integer
-   Default value: `100`
-   Range: `[0, 2147483647]`
-   Unit: Milliseconds
-   This variable controls whether to enable the synchronously loading statistics feature. The value `0` means that the feature is disabled. To enable the feature, you can set this variable to a timeout (in milliseconds) that SQL optimization can wait for at most to synchronously load complete column statistics. For details, see [負荷統計](/statistics.md#load-statistics).

### tidb_stmt_summary_enable_persistent <span class="version-mark">New in v6.6.0</span> {#tidb-stmt-summary-enable-persistent-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   Scope: GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   This variable is read-only. It controls whether to enable [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary).

<CustomContent platform="tidb">

-   The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660).

</CustomContent>

### tidb_stmt_summary_filename <span class="version-mark">New in v6.6.0</span> {#tidb-stmt-summary-filename-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   Scope: GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: String
-   Default value: `"tidb-statements.log"`
-   This variable is read-only. It specifies the file to which persistent data is written when [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary) is enabled.

<CustomContent platform="tidb">

-   The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660).

</CustomContent>

### tidb_stmt_summary_file_max_backups <span class="version-mark">New in v6.6.0</span> {#tidb-stmt-summary-file-max-backups-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   Scope: GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `0`
-   This variable is read-only. It specifies the maximum number of data files that can be persisted when [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary) is enabled.

<CustomContent platform="tidb">

-   The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660).

</CustomContent>

### tidb_stmt_summary_file_max_days <span class="version-mark">New in v6.6.0</span> {#tidb-stmt-summary-file-max-days-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   Scope: GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `3`
-   Unit: day
-   This variable is read-only. It specifies the maximum number of days to keep persistent data files when [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary) is enabled.

<CustomContent platform="tidb">

-   The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660).

</CustomContent>

### tidb_stmt_summary_file_max_size <span class="version-mark">New in v6.6.0</span> {#tidb-stmt-summary-file-max-size-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [問題](https://github.com/pingcap/tidb/issues) on GitHub.

-   Scope: GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `64`
-   Unit: MiB
-   This variable is read-only. It specifies the maximum size of a persistent data file when [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary) is enabled.

<CustomContent platform="tidb">

-   The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660).

</CustomContent>

### tidb_stmt_summary_history_size <span class="version-mark">New in v4.0</span> {#tidb-stmt-summary-history-size-span-class-version-mark-new-in-v4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `24`
-   Range: `[0, 255]`
-   This variable is used to set the history capacity of [ステートメント要約表](/statement-summary-tables.md).

### tidb_stmt_summary_internal_query <span class="version-mark">New in v4.0</span> {#tidb-stmt-summary-internal-query-span-class-version-mark-new-in-v4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to control whether to include the SQL information of TiDB in [ステートメント要約表](/statement-summary-tables.md).

### tidb_stmt_summary_max_sql_length <span class="version-mark">New in v4.0</span> {#tidb-stmt-summary-max-sql-length-span-class-version-mark-new-in-v4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `4096`
-   Range: `[0, 2147483647]`
-   Unit: Bytes

<CustomContent platform="tidb">

-   この変数は、 [ステートメント要約表](/statement-summary-tables.md)と[TiDB Dashboard](/dashboard/dashboard-intro.md)の SQL 文字列の長さを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable is used to control the length of the SQL string in [ステートメント要約表](/statement-summary-tables.md).

</CustomContent>

### tidb_stmt_summary_max_stmt_count <span class="version-mark">New in v4.0</span> {#tidb-stmt-summary-max-stmt-count-span-class-version-mark-new-in-v4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `3000`
-   Range: `[1, 32767]`
-   This variable is used to set the maximum number of statements that [ステートメント要約表](/statement-summary-tables.md) store in memory.

### tidb_stmt_summary_refresh_interval <span class="version-mark">New in v4.0</span> {#tidb-stmt-summary-refresh-interval-span-class-version-mark-new-in-v4-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `1800`
-   Range: `[1, 2147483647]`
-   Unit: Seconds
-   This variable is used to set the refresh time of [ステートメント要約表](/statement-summary-tables.md).

### tidb_store_batch_size {#tidb-store-batch-size}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Integer
-   Default value: `4`
-   Range: `[0, 25000]`
-   This variable is used to control the batch size of the Coprocessor Tasks of the `IndexLookUp` operator. `0` means to disable batch. When the number of tasks is relatively large and slow queries occur, you can increase this variable to optimize the query.

### tidb_store_limit <span class="version-mark">New in v3.0.4 and v4.0</span> {#tidb-store-limit-span-class-version-mark-new-in-v3-0-4-and-v4-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `0`
-   Range: `[0, 9223372036854775807]`
-   This variable is used to limit the maximum number of requests TiDB can send to TiKV at the same time. 0 means no limit.

### tidb_streamagg_concurrency {#tidb-streamagg-concurrency}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `1`
-   This variable sets the concurrency of the `StreamAgg` operator when queries are executed.
-   It is **NOT recommended** to set this variable. Modifying the variable value might cause data correctness issues.

### tidb_super_read_only <span class="version-mark">New in v5.3.1</span> {#tidb-super-read-only-span-class-version-mark-new-in-v5-3-1-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   `tidb_super_read_only` aims to be implemented as a replacement of the MySQL variable `super_read_only`. However, because TiDB is a distributed database, `tidb_super_read_only` does not make the database read-only immediately after execution, but eventually.
-   Users with the `SUPER` or `SYSTEM_VARIABLES_ADMIN` privilege can modify this variable.
-   This variable controls the read-only status of the entire cluster. When the variable is `ON`, all TiDB servers in the entire cluster are in the read-only mode. In this case, TiDB only executes the statements that do not modify data, such as `SELECT`, `USE`, and `SHOW`. For other statements such as `INSERT` and `UPDATE`, TiDB rejects executing those statements in the read-only mode.
-   Enabling the read-only mode using this variable only ensures that the entire cluster finally enters the read-only status. If you have changed the value of this variable in a TiDB cluster but the change has not yet propagated to other TiDB servers, the un-updated TiDB servers are still **not** in the read-only mode.
-   TiDB checks the read-only flag before SQL statements are executed. Since v6.2.0, the flag is also checked before SQL statements are committed. This helps prevent the case where long-running [自動コミット](/transaction-overview.md#autocommit) statements might modify data after the server has been placed in read-only mode.
-   When this variable is enabled, TiDB handles the uncommitted transactions in the following ways:
    -   For uncommitted read-only transactions, you can commit the transactions normally.
    -   For uncommitted transactions that are not read-only, SQL statements that perform write operations in these transactions are rejected.
    -   For uncommitted read-only transactions with modified data, the commit of these transactions is rejected.
-   After the read-only mode is enabled, all users (including the users with the `SUPER` privilege) cannot execute the SQL statements that might write data unless the user is explicitly granted the `RESTRICTED_REPLICA_WRITER_ADMIN` privilege.
-   [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)システム変数が`ON`に設定されている場合、 `tidb_super_read_only` [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の影響を受ける場合があります。詳細な影響については、 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の説明を参照してください。

### tidb_sysdate_is_now <span class="version-mark">New in v6.0.0</span> {#tidb-sysdate-is-now-span-class-version-mark-new-in-v6-0-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `OFF`
-   This variable is used to control whether the `SYSDATE` function can be replaced by the `NOW` function. This configuration item has the same effect as the MySQL option [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now).

### tidb_sysproc_scan_concurrency <span class="version-mark">New in v6.5.0</span> {#tidb-sysproc-scan-concurrency-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `1`
-   Range: `[0, 4294967295]`. The maximum value for v7.5.0 and earlier versions is `256`. Before v8.2.0, the minimum value is `1`. When you set it to `0`, it adaptively adjusts the concurrency based on the cluster size.
-   This variable is used to set the concurrency of scan operations performed when TiDB executes internal SQL statements (such as an automatic update of statistics).

### tidb_table_cache_lease <span class="version-mark">New in v6.0.0</span> {#tidb-table-cache-lease-span-class-version-mark-new-in-v6-0-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `3`
-   Range: `[1, 10]`
-   Unit: Seconds
-   This variable is used to control the lease time of [キャッシュされたテーブル](/cached-tables.md) with a default value of `3`. The value of this variable affects the modification to cached tables. After a modification is made to cached tables, the longest waiting time might be `tidb_table_cache_lease` seconds. If the table is read-only or can accept a high write latency, you can increase the value of this variable to increase the valid time for caching tables and to reduce the frequency of lease renewal.

### tidb_tmp_table_max_size <span class="version-mark">New in v5.3.0</span> {#tidb-tmp-table-max-size-span-class-version-mark-new-in-v5-3-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `67108864`
-   Range: `[1048576, 137438953472]`
-   Unit: Bytes
-   This variable is used to set the maximum size of a single [一時テーブル](/temporary-tables.md). Any temporary table with a size larger than this variable value causes error.

### tidb_top_sql_max_meta_count <span class="version-mark">New in v6.0.0</span> {#tidb-top-sql-max-meta-count-span-class-version-mark-new-in-v6-0-0-span}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `5000`
-   Range: `[1, 10000]`

<CustomContent platform="tidb">

-   This variable is used to control the maximum number of SQL statement types collected by [Top SQL](/dashboard/top-sql.md) per minute.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable is used to control the maximum number of SQL statement types collected by [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) per minute.

</CustomContent>

### tidb_top_sql_max_time_series_count <span class="version-mark">New in v6.0.0</span> {#tidb-top-sql-max-time-series-count-span-class-version-mark-new-in-v6-0-0-span}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

> **Note:**
>
> Currently, the Top SQL page in TiDB Dashboard only displays the top 5 types of SQL queries that contribute the most to the load, which is irrelevant with the configuration of `tidb_top_sql_max_time_series_count`.

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `100`
-   Range: `[1, 5000]`

<CustomContent platform="tidb">

-   This variable is used to control how many SQL statements that contribute the most to the load (that is, top N) can be recorded by [Top SQL](/dashboard/top-sql.md) per minute.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable is used to control how many SQL statements that contribute the most to the load (that is, top N) can be recorded by [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) per minute.

</CustomContent>

### tidb_track_aggregate_memory_usage {#tidb-track-aggregate-memory-usage}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable controls whether TiDB tracks the memory usage of aggregate functions.

> **Warning:**
>
> If you disable this variable, TiDB might not accurately track the memory usage and cannot control the memory usage of the corresponding SQL statements.

### tidb_tso_client_batch_max_wait_time <span class="version-mark">New in v5.3.0</span> {#tidb-tso-client-batch-max-wait-time-span-class-version-mark-new-in-v5-3-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Float
-   Default value: `0`
-   Range: `[0, 10]`
-   Unit: Milliseconds
-   This variable is used to set the maximum waiting time for a batch operation when TiDB requests TSO from PD. The default value is `0`, which means no extra waiting time.
-   When obtaining TSO requests from PD each time, PD Client, used by TiDB, collects as many TSO requests received at the same time as possible. Then, PD Client merges the collected requests in batch into one RPC request and sends the request to PD. This helps reduce the pressure on PD.
-   After setting this variable to a value greater than `0`, TiDB waits for the maximum duration of this value before the end of each batch merge. This is to collect more TSO requests and improve the effect of batch operations.
-   Scenarios for increasing the value of this variable:
    -   Due to the high pressure of TSO requests, the CPU of the PD leader reaches a bottleneck, which causes high latency of TSO RPC requests.
    -   There are not many TiDB instances in the cluster, but every TiDB instance is in high concurrency.
-   It is recommended to set this variable to a value as small as possible.

> **Note:**
>
> -   Suppose that the TSO RPC latency increases for reasons other than a CPU usage bottleneck of the PD leader (such as network issues). In this case, increasing the value of `tidb_tso_client_batch_max_wait_time` might increase the execution latency in TiDB and affect the QPS performance of the cluster.
> -   この機能は[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)と互換性がありません。この変数がゼロ以外の値に設定されている場合、 [`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)有効になりません。

### tidb_tso_client_rpc_mode <span class="version-mark">New in v8.4.0</span> {#tidb-tso-client-rpc-mode-span-class-version-mark-new-in-v8-4-0-span}

-   Scope: GLOBAL

-   Persists to cluster: Yes

-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No

-   Type: Enumeration

-   Default value: `DEFAULT`

-   Value options: `DEFAULT`, `PARALLEL`, `PARALLEL-FAST`

-   This variable switches the mode in which TiDB sends TSO RPC requests to PD. The mode determines whether TSO RPC requests are processed in parallel and affects the time spent on batch-waiting for each TS retrieval operation, thereby helping reduce the wait time for retrieving TS during query execution in certain scenarios.

    -   `DEFAULT`: TiDB collects TS retrieval operations over a specific period into a single TSO RPC request and sends it to PD to get timestamps in a batch. Therefore, the duration of each TS retrieval operation consists of the time spent waiting to be batched and the time spent performing the RPC. In `DEFAULT` mode, different TSO RPC requests are processed serially, and the average duration of each TS retrieval operation is about 1.5 times the actual time cost of a TSO RPC request.
    -   `PARALLEL`: In this mode, TiDB attempts to reduce the duration for collecting each batch to half of that in `DEFAULT` mode and tries to maintain two concurrent TSO RPC requests. In this way, the average duration of each TS retrieval operation can theoretically be reduced to about 1.25 times the TSO RPC duration, which is about 83% of the time cost in `DEFAULT` mode. However, the effect of batching will be reduced, and the number of TSO RPC requests will increase to roughly double that in `DEFAULT` mode.
    -   `PARALLEL-FAST`: Similar to `PARALLEL` mode, in this mode, TiDB attempts to reduce the duration for collecting each batch to a quarter of that in `DEFAULT` mode and tries to maintain four concurrent TSO RPC requests. In this way, the average duration of each TS retrieval operation can theoretically be reduced to about 1.125 times the TSO RPC duration, which is about 75% of the time cost in `DEFAULT` mode. However, the effect of batching will be further reduced, and the number of TSO RPC requests will increase to roughly four times that in `DEFAULT` mode.

-   When the following conditions are met, you can consider switching this variable to `PARALLEL` or `PARALLEL-FAST` for potential performance improvements:

    -   TSO waiting time constitutes a significant portion of the total execution time of SQL queries.
    -   The TSO allocation in PD has not reached its bottleneck.
    -   PD and TiDB nodes have sufficient CPU resources.
    -   The network latency between TiDB and PD is significantly higher than the time PD takes to allocate TSO (that is, network latency accounts for the majority of TSO RPC duration).
        -   To get the duration of TSO RPC requests, check the **PD TSO RPC Duration** panel in the PD Client section of the Grafana TiDB dashboard.
        -   To get the duration of PD TSO allocation, check the **PD server TSO handle duration** panel in the TiDB section of the Grafana PD dashboard.
    -   The additional network traffic resulting from more TSO RPC requests between TiDB and PD (twice for `PARALLEL` or four times for `PARALLEL-FAST`) is acceptable.

> **Note:**
>
> -   `PARALLEL`および`PARALLEL-FAST`モードは、 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)および[`tidb_enable_tso_follower_proxy`](#tidb_enable_tso_follower_proxy-new-in-v530)と互換性がありません。 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)がゼロ以外の値に設定されている場合、または[`tidb_enable_tso_follower_proxy`](#tidb_enable_tso_follower_proxy-new-in-v530)が有効になっている場合、 `tidb_tso_client_rpc_mode`の構成は有効にならず、 TiDB は常に`DEFAULT`モードで動作します。
> -   `PARALLEL` and `PARALLEL-FAST` modes are designed to reduce the average time for retrieving TS in TiDB. In situations with significant latency fluctuations, such as long-tail latency or latency spikes, these two modes might not provide any remarkable performance improvements.

### tidb_ttl_delete_rate_limit <span class="version-mark">New in v6.5.0</span> {#tidb-ttl-delete-rate-limit-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `0`
-   Range: `[0, 9223372036854775807]`
-   This variable is used to limit the rate of `DELETE` statements in TTL jobs on each TiDB node. The value represents the maximum number of `DELETE` statements allowed per second in a single node in a TTL job. When this variable is set to `0`, no limit is applied. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_ttl_delete_batch_size <span class="version-mark">New in v6.5.0</span> {#tidb-ttl-delete-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `100`
-   Range: `[1, 10240]`
-   This variable is used to set the maximum number of rows that can be deleted in a single `DELETE` transaction in a TTL job. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_ttl_delete_worker_count <span class="version-mark">New in v6.5.0</span> {#tidb-ttl-delete-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `4`
-   Range: `[1, 256]`
-   This variable is used to set the maximum concurrency of TTL jobs on each TiDB node. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_ttl_job_enable <span class="version-mark">New in v6.5.0</span> {#tidb-ttl-job-enable-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `ON`
-   Type: Boolean
-   This variable is used to control whether TTL jobs are enabled. If it is set to `OFF`, all tables with TTL attributes automatically stop cleaning up expired data. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_ttl_scan_batch_size <span class="version-mark">New in v6.5.0</span> {#tidb-ttl-scan-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `500`
-   Range: `[1, 10240]`
-   This variable is used to set the `LIMIT` value of each `SELECT` statement used to scan expired data in a TTL job. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_ttl_scan_worker_count <span class="version-mark">New in v6.5.0</span> {#tidb-ttl-scan-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `4`
-   Range: `[1, 256]`
-   This variable is used to set the maximum concurrency of TTL scan jobs on each TiDB node. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_ttl_job_schedule_window_start_time <span class="version-mark">New in v6.5.0</span> {#tidb-ttl-job-schedule-window-start-time-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Time
-   Persists to cluster: Yes
-   Default value: `00:00 +0000`
-   This variable is used to control the start time of the scheduling window of TTL jobs in the background. When you modify the value of this variable, be cautious that a small window might cause the cleanup of expired data to fail. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_ttl_job_schedule_window_end_time <span class="version-mark">New in v6.5.0</span> {#tidb-ttl-job-schedule-window-end-time-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Time
-   Persists to cluster: Yes
-   Default value: `23:59 +0000`
-   This variable is used to control the end time of the scheduling window of TTL jobs in the background. When you modify the value of this variable, be cautious that a small window might cause the cleanup of expired data to fail. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_ttl_running_tasks <span class="version-mark">New in v7.0.0</span> {#tidb-ttl-running-tasks-span-class-version-mark-new-in-v7-0-0-span}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `-1`
-   Range: `-1` and `[1, 256]`
-   Specifies the maximum number of running TTL tasks in the entire cluster. `-1` means the number of TTL tasks is equivalent to the number of TiKV nodes. For more information, refer to [生きる時間](/time-to-live.md).

### tidb_txn_assertion_level <span class="version-mark">New in v6.0.0</span> {#tidb-txn-assertion-level-span-class-version-mark-new-in-v6-0-0-span}

-   Scope: SESSION | GLOBAL

-   Persists to cluster: Yes

-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No

-   Type: Enumeration

-   Default value: `FAST`

-   Possible values: `OFF`, `FAST`, `STRICT`

-   This variable is used to control the assertion level. Assertion is a consistency check between data and indexes, which checks whether a key being written exists in the transaction commit process. For more information, see [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md).

    -   `OFF`: Disable this check.
    -   `FAST`: Enable most of the check items, with almost no impact on performance.
    -   `STRICT`: Enable all check items, with a minor impact on pessimistic transaction performance when the system workload is high.

-   For new clusters of v6.0.0 or later versions, the default value is `FAST`. For existing clusters that upgrade from versions earlier than v6.0.0, the default value is `OFF`.

### tidb_txn_commit_batch_size <span class="version-mark">New in v6.2.0</span> {#tidb-txn-commit-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `16384`
-   Range: `[1, 1073741824]`
-   Unit: Bytes

<CustomContent platform="tidb">

-   This variable is used to control the batch size of transaction commit requests that TiDB sends to TiKV. If most of the transactions in the application workload have a large number of write operations, adjusting this variable to a larger value can improve the performance of batch processing. However, if this variable is set to too large a value and exceeds the limit of TiKV's [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size), the commits might fail.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable is used to control the batch size of transaction commit requests that TiDB sends to TiKV. If most of the transactions in the application workload have a large number of write operations, adjusting this variable to a larger value can improve the performance of batch processing. However, if this variable is set to too large a value and exceeds the limit of TiKV's maximum size of a single log (which is 8 MiB by default), the commits might fail.

</CustomContent>

### tidb_txn_entry_size_limit <span class="version-mark">New in v7.6.0</span> {#tidb-txn-entry-size-limit-span-class-version-mark-new-in-v7-6-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `0`
-   Range: `[0, 125829120]`
-   Unit: Bytes

<CustomContent platform="tidb">

-   This variable is used to dynamically modify the TiDB configuration item [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500). It limits the size of a single row of data in TiDB, which is equivalent to the configuration item. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, `txn-entry-size-limit` is also set to the same value.

</CustomContent>

<CustomContent platform="tidb-cloud">

-   This variable is used to dynamically modify the TiDB configuration item [`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500). It limits the size of a single row of data in TiDB, which is equivalent to the configuration item. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, `txn-entry-size-limit` is also set to the same value.

</CustomContent>

> **Note:**
>
> Modifying this variable with the SESSION scope only affects the current user session, not the internal TiDB session. This might lead to transaction failure if the entry size of an internal TiDB transaction exceeds the limit of the configuration item. Therefore, to dynamically increase the limit, it is recommended that you modify the variable with the GLOBAL scope.

### tidb_txn_mode {#tidb-txn-mode}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Enumeration
-   Default value: `pessimistic`
-   Possible values: `pessimistic`, `optimistic`
-   This variable is used to set the transaction mode. TiDB 3.0 supports the pessimistic transactions. Since TiDB 3.0.8, the [悲観的トランザクションモード](/pessimistic-transaction.md) is enabled by default.
-   If you upgrade TiDB from v3.0.7 or earlier versions to v3.0.8 or later versions, the default transaction mode does not change. **Only the newly created clusters use the pessimistic transaction mode by default**.
-   If this variable is set to "optimistic" or "", TiDB uses the [楽観的トランザクションモード](/optimistic-transaction.md).

### tidb_use_plan_baselines <span class="version-mark">New in v4.0</span> {#tidb-use-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable is used to control whether to enable the execution plan binding feature. It is enabled by default, and can be disabled by assigning the `OFF` value. For the use of the execution plan binding, see [実行プランのバインディング](/sql-plan-management.md#create-a-binding).

### tidb_wait_split_region_finish {#tidb-wait-split-region-finish}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   It usually takes a long time to scatter Regions, which is determined by PD scheduling and TiKV loads. This variable is used to set whether to return the result to the client after all Regions are scattered completely when the `SPLIT REGION` statement is being executed:
    -   `ON` requires that the `SPLIT REGIONS` statement waits until all Regions are scattered.
    -   `OFF` permits the `SPLIT REGIONS` statement to return before finishing scattering all Regions.
-   Note that when scattering Regions, the write and read performances for the Region that is being scattered might be affected. In batch-write or data importing scenarios, it is recommended to import data after Regions scattering is finished.

### tidb_wait_split_region_timeout {#tidb-wait-split-region-timeout}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `300`
-   Range: `[1, 2147483647]`
-   Unit: Seconds
-   This variable is used to set the timeout for executing the `SPLIT REGION` statement. If a statement is not executed completely within the specified time value, a timeout error is returned.

### tidb_window_concurrency <span class="version-mark">New in v4.0</span> {#tidb-window-concurrency-span-class-version-mark-new-in-v4-0-span}

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `-1`
-   Range: `[1, 256]`
-   Unit: Threads
-   This variable is used to set the concurrency degree of the window operator.
-   A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tiflash_fastscan <span class="version-mark">New in v6.3.0</span> {#tiflash-fastscan-span-class-version-mark-new-in-v6-3-0-span}

-   Scope: SESSION | GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Default value: `OFF`
-   Type: Boolean
-   If [高速スキャン](/tiflash/use-fastscan.md) is enabled (set to `ON`), TiFlash provides more efficient query performance, but does not guarantee the accuracy of the query results or data consistency.

### tiflash_fine_grained_shuffle_batch_size <span class="version-mark">New in v6.2.0</span> {#tiflash-fine-grained-shuffle-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   Scope: SESSION | GLOBAL
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Default value: `8192`
-   Range: `[1, 18446744073709551615]`
-   When Fine Grained Shuffle is enabled, the window function pushed down to TiFlash can be executed in parallel. This variable controls the batch size of the data sent by the sender.
-   Impact on performance: set a reasonable size according to your business requirements. Improper setting affects the performance. If the value is set too small, for example `1`, it causes one network transfer per Block. If the value is set too large, for example, the total number of rows of the table, it causes the receiving end to spend most of the time waiting for data, and the piplelined computation cannot work. To set a proper value, you can observe the distribution of the number of rows received by the TiFlash receiver. If most threads receive only a few rows, for example a few hundred, you can increase this value to reduce the network overhead.

### tiflash_fine_grained_shuffle_stream_count <span class="version-mark">New in v6.2.0</span> {#tiflash-fine-grained-shuffle-stream-count-span-class-version-mark-new-in-v6-2-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Integer
-   Default value: `0`
-   Range: `[-1, 1024]`
-   When the window function is pushed down to TiFlash for execution, you can use this variable to control the concurrency level of the window function execution. The possible values are as follows:

    -   -1: the Fine Grained Shuffle feature is disabled. The window function pushed down to TiFlash is executed in a single thread.
    -   0: 細粒度シャッフル機能が有効です。 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)有効な値 (0 より大きい値) に設定されている場合、 `tiflash_fine_grained_shuffle_stream_count` [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)の値に設定されます。 それ以外の場合は、 TiFlashコンピューティング ノードの CPU リソースに基づいて自動的に推定されます。 TiFlashのウィンドウ関数の実際の同時実行レベルは、 min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノード上の物理スレッドの数) です。
    -   Integer greater than 0: the Fine Grained Shuffle feature is enabled. The window function pushed down to TiFlash is executed in multiple threads. The concurrency level is: min(`tiflash_fine_grained_shuffle_stream_count`, the number of physical threads on TiFlash nodes).
-   Theoretically, the performance of the window function increases linearly with this value. However, if the value exceeds the actual number of physical threads, it instead leads to performance degradation.

### tiflash_mem_quota_query_per_node <span class="version-mark">New in v7.4.0</span> {#tiflash-mem-quota-query-per-node-span-class-version-mark-new-in-v7-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `0`
-   Range: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashノードでのクエリの最大メモリ使用量を制限します。クエリのメモリ使用量がこの制限を超えると、 TiFlash はエラーを返し、クエリを終了します。この変数を`-1`または`0`に設定すると、制限なしになります。この変数が`0`より大きい値に設定され、 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)有効な値に設定されている場合、 TiFlash は[query-level spilling](/tiflash/tiflash-spill-disk.md#query-level-spilling)有効にします。

### tiflash_query_spill_ratio <span class="version-mark">New in v7.4.0</span> {#tiflash-query-spill-ratio-span-class-version-mark-new-in-v7-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Float
-   Default value: `0.7`
-   Range: `[0, 0.85]`
-   この変数は、 TiFlash [クエリレベルのスピル](/tiflash/tiflash-spill-disk.md#query-level-spilling)のしきい値を制御します`0`自動クエリ レベルのスピルを無効にすることを意味します。この変数が`0`より大きく、クエリのメモリ使用量が[`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) * `tiflash_query_spill_ratio`を超えると、 TiFlash はクエリ レベルのスピルをトリガーし、必要に応じてクエリでサポートされている演算子のデータをスピルします。

> **Note:**
>
> -   この変数は、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)が`0`より大きい場合にのみ有効になります。つまり、 [tiflash_mem_quota_query_per_node](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)が`0`または`-1`場合、 `tiflash_query_spill_ratio`が`0`より大きい場合でも、クエリ レベルのスピルは有効になりません。
> -   TiFlashクエリ レベルのスピルが有効になっている場合、個々のTiFlash演算子のスピルしきい値は自動的に無効になります。つまり、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)と`tiflash_query_spill_ratio`両方が 0 より大きい場合、 [tidb_max_bytes_before_tiflash_external_sort](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700) 、 [tidb_max_bytes_before_tiflash_external_group_by](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) 、および[tidb_max_bytes_before_tiflash_external_join](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)の 3 つの変数は自動的に無効になり、これを`0`に設定するのと同じです。

### tiflash_replica_read <span class="version-mark">New in v7.3.0</span> {#tiflash-replica-read-span-class-version-mark-new-in-v7-3-0-span}

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Enumeration
-   Default value: `all_replicas`
-   Value options: `all_replicas`, `closest_adaptive`, or `closest_replicas`
-   This variable is used to set the strategy for selecting TiFlash replicas when a query requires the TiFlash engine.
    -   `all_replicas` means using all available TiFlash replicas for analytical computing.
    -   `closest_adaptive` means preferring to use TiFlash replicas in the same zone as the TiDB node initiating the query. If replicas in this zone do not contain all the required data, the query will involve TiFlash replicas from other zones along with their corresponding TiFlash nodes.
    -   `closest_replicas` means using only TiFlash replicas in the same zone as the TiDB node initiating the query. If replicas in this zone do not contain all the required data, the query will return an error.

<CustomContent platform="tidb">

> **Note:**
>
> -   If TiDB nodes do not have [ゾーン属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb) configured and `tiflash_replica_read` is not set to `all_replicas`, TiFlash ignores the replica selection strategy. Instead, it uses all TiFlash replicas for queries and returns the `The variable tiflash_replica_read is ignored.` warning.
> -   If TiFlash nodes do not have [ゾーン属性](/schedule-replicas-by-topology-labels.md#configure-labels-for-tikv-and-tiflash) configured, they are treated as nodes not belonging to any zone.

</CustomContent>

### tiflash_hashagg_preaggregation_mode <span class="version-mark">New in v8.3.0</span> {#tiflash-hashagg-preaggregation-mode-span-class-version-mark-new-in-v8-3-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
-   Type: Enumeration
-   Default value: `force_preagg`
-   Value options: `force_preagg`, `force_streaming`, `auto`
-   This variable controls the pre-aggregation strategy used during the first stage of two-stage or three-stage HashAgg operations pushed down to TiFlash:
    -   `force_preagg`: TiFlash forces pre-aggregation during the first stage of HashAgg. This behavior is consistent with the behavior before v8.3.0.
    -   `force_streaming`: TiFlash directly sends data to the next stage of HashAgg without pre-aggregation.
    -   `auto`: TiFlash automatically chooses whether to perform pre-aggregation based on the current workload's aggregation degree.

### tikv_client_read_timeout <span class="version-mark">New in v7.4.0</span> {#tikv-client-read-timeout-span-class-version-mark-new-in-v7-4-0-span}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `0`
-   Range: `[0, 2147483647]`
-   Unit: Millisecond
-   You can use `tikv_client_read_timeout` to set the timeout for TiDB to send a TiKV RPC read request in a query. When a TiDB cluster is in an environment with unstable network or serious TiKV I/O latency jitter, and your application is sensitive to the latency of the SQL queries, you can set `tikv_client_read_timeout` to reduce the timeout of the TiKV RPC read requests. In this case, when a TiKV node has I/O latency jitter, TiDB can time out quickly and re-send the RPC request to the TiKV node where the next TiKV Region Peer is located. If the requests of all TiKV Region Peers time out, TiDB will retry with the default timeout (usually 40 seconds).
-   You can also use the optimizer hint `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */` in a query to set the timeout for TiDB to send a TiKV RPC read request. If both the optimizer hint and this system variable are set, the optimizer hint takes higher priority.
-   The default value `0` indicates that the default timeout (usually 40 seconds) is used.

> **Note:**
>
> -   Normally, a regular query takes a few milliseconds, but occasionally when a TiKV node is in unstable network or gets I/O jitter, the query can take more than 1 second or even 10 seconds. In this case, you can set the TiKV RPC read request timeout to 100 milliseconds for a specific query by using the optimizer hint `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=100) */`. In this way, even if the response of a TiKV node is slow, TiDB can quickly time out and then re-send the RPC request to the TiKV node where the next TiKV Region Peer is located. Because the probability of two TiKV nodes getting I/O jitter simultaneously is low, the query can be completed usually within a few milliseconds to 110 milliseconds.
> -   Do not set too small values (for example, 1 millisecond) for `tikv_client_read_timeout`. Otherwise, the requests might time out easily when the workload of a TiDB cluster is high, and subsequent retries will further increase the load on the TiDB cluster.
> -   If you need to set different timeout values for different types of queries, it is recommended to use optimizer hints.

### time_zone {#time-zone}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `SYSTEM`
-   This variable returns the current time zone. Values can be specified as either an offset such as '-8:00' or a named zone 'America/Los_Angeles'.
-   The value `SYSTEM` means that the time zone should be the same as the system host, which is available via the [`system_time_zone`](#system_time_zone) variable.

### timestamp {#timestamp}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Float
-   Default value: `0`
-   Range: `[0, 2147483647]`
-   A non-empty value of this variable indicates the UNIX epoch that is used as the timestamp for `CURRENT_TIMESTAMP()`, `NOW()`, and other functions. This variable might be used in data restore or replication.

### transaction_isolation {#transaction-isolation}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Enumeration
-   Default value: `REPEATABLE-READ`
-   Possible values: `READ-UNCOMMITTED`, `READ-COMMITTED`, `REPEATABLE-READ`, `SERIALIZABLE`
-   This variable sets the transaction isolation. TiDB advertises `REPEATABLE-READ` for compatibility with MySQL, but the actual isolation level is Snapshot Isolation. See [トランザクション分離レベル](/transaction-isolation-levels.md) for further details.

### tx_isolation {#tx-isolation}

This variable is an alias for `transaction_isolation`.

### tx_isolation_one_shot {#tx-isolation-one-shot}

> **Note:**
>
> This variable is internally used in TiDB. You are not expected to use it.

Internally, the TiDB parser transforms the `SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]` statements to `SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`.

### tx_read_ts {#tx-read-ts}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: ""
-   In the Stale Read scenarios, this session variable is used to help record the Stable Read timestamp value.
-   This variable is used for the internal operation of TiDB. It is **NOT recommended** to set this variable.

### txn_scope {#txn-scope}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `global`
-   Value options: `global` and `local`
-   This variable is used to set whether the current session transaction is a global transaction or a local transaction.
-   This variable is used for the internal operation of TiDB. It is **NOT recommended** to set this variable.

### validate_password.check_user_name <span class="version-mark">New in v6.5.0</span> {#validate-password-check-user-name-span-class-version-mark-new-in-v6-5-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `ON`
-   Type: Boolean
-   This variable is a check item in the password complexity check. It checks whether the password matches the username. This variable takes effect only when [`validate_password.enable`](#validate_passwordenable-new-in-v650) is enabled.
-   When this variable is effective and set to `ON`, if you set a password, TiDB compares the password with the username (excluding the hostname). If the password matches the username, the password is rejected.
-   This variable is independent of [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) and not affected by the password complexity check level.

### validate_password.dictionary <span class="version-mark">New in v6.5.0</span> {#validate-password-dictionary-span-class-version-mark-new-in-v6-5-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `""`
-   Type: String
-   この変数は、パスワードの複雑さのチェックにおけるチェック項目です。パスワードが辞書と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) `2` (STRONG) に設定されている場合にのみ有効になります。
-   This variable is a string not longer than 1024 characters. It contains a list of words that cannot exist in the password. Each word is separated by semicolon (`;`).
-   This variable is set to an empty string by default, which means no dictionary check is performed. To perform the dictionary check, you need to include the words to be matched in the string. If this variable is configured, when you set a password, TiDB compares each substring (length in 4 to 100 characters) of the password with the words in the dictionary. If any substring of the password matches a word in the dictionary, the password is rejected. The comparison is case-insensitive.

### validate_password.enable <span class="version-mark">New in v6.5.0</span> {#validate-password-enable-span-class-version-mark-new-in-v6-5-0-span}

> **Note:**
>
> This variable is always enabled for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `OFF`
-   Type: Boolean
-   This variable controls whether to perform password complexity check. If this variable is set to `ON`, TiDB performs the password complexity check when you set a password.

### validate_password.length <span class="version-mark">New in v6.5.0</span> {#validate-password-length-span-class-version-mark-new-in-v6-5-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `8`
-   範囲: TiDBセルフマネージドの場合は`[0, 2147483647]` [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) `[8, 2147483647]`は[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   This variable is a check item in the password complexity check. It checks whether the password length is sufficient. By default, the minimum password length is `8`. This variable takes effect only when [`validate_password.enable`](#validate_passwordenable-new-in-v650) is enabled.
-   The value of this variable must not be smaller than the expression: `validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`.
-   If you change the value of `validate_password.number_count`, `validate_password.special_char_count`, or `validate_password.mixed_case_count` such that the expression value is larger than `validate_password.length`, the value of `validate_password.length` is automatically changed to match the expression value.

### validate_password.mixed_case_count <span class="version-mark">New in v6.5.0</span> {#validate-password-mixed-case-count-span-class-version-mark-new-in-v6-5-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `1`
-   範囲: TiDBセルフマネージドの場合は`[0, 2147483647]` [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) `[1, 2147483647]`は[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   この変数は、パスワードの複雑さチェックにおけるチェック項目です。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) `1` (MEDIUM) 以上に設定されている場合にのみ有効になります。
-   Neither the number of uppercase letters nor the number of lowercase letters in the password can be fewer than the value of `validate_password.mixed_case_count`. For example, when the variable is set to `1`, the password must contain at least one uppercase letter and one lowercase letter.

### validate_password.number_count <span class="version-mark">New in v6.5.0</span> {#validate-password-number-count-span-class-version-mark-new-in-v6-5-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `1`
-   範囲: TiDBセルフマネージドの場合は`[0, 2147483647]` [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) `[1, 2147483647]`は[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   この変数は、パスワードの複雑さのチェックにおけるチェック項目です。パスワードに十分な数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) `1` (MEDIUM) 以上に設定されている場合にのみ有効になります。

### validate_password.policy <span class="version-mark">New in v6.5.0</span> {#validate-password-policy-span-class-version-mark-new-in-v6-5-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Enumeration
-   Default value: `1`
-   値`2`オプション: TiDB Self-Managed [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) `1`は`0` `1` [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)は`2`
-   This variable controls the policy for the password complexity check. This variable takes effect only when [`validate_password.enable`](#password_reuse_interval-new-in-v650) is enabled. The value of this variable determines whether other `validate-password` variables take effect in the password complexity check, except for `validate_password.check_user_name`.
-   This value of this variable can be `0`, `1`, or `2` (corresponds to LOW, MEDIUM, or STRONG). Different policy levels have different checks:
    -   0 or LOW: password length.
    -   1 or MEDIUM: password length, uppercase and lowercase letters, numbers, and special characters.
    -   2 or STRONG: password length, uppercase and lowercase letters, numbers, special characters, and dictionary match.

### validate_password.special_char_count <span class="version-mark">New in v6.5.0</span> {#validate-password-special-char-count-span-class-version-mark-new-in-v6-5-0-span}

-   Scope: GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `1`
-   範囲: TiDBセルフマネージドの場合は`[0, 2147483647]` [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) `[1, 2147483647]`は[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   この変数は、パスワードの複雑さのチェックにおけるチェック項目です。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効になります。

### version {#version}

-   Scope: NONE
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `8.0.11-TiDB-`(tidb version)
-   This variable returns the MySQL version, followed by the TiDB version. For example '8.0.11-TiDB-v8.5.0'.

### version_comment {#version-comment}

-   Scope: NONE
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: (string)
-   This variable returns additional details about the TiDB version. For example, 'TiDB Server (Apache License 2.0) Community Edition, MySQL 8.0 compatible'.

### version_compile_machine {#version-compile-machine}

-   Scope: NONE
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: (string)
-   This variable returns the name of the CPU architecture on which TiDB is running.

### version_compile_os {#version-compile-os}

-   Scope: NONE
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: (string)
-   This variable returns the name of the OS on which TiDB is running.

### wait_timeout {#wait-timeout}

> **Note:**
>
> This variable is read-only for [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless).

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Integer
-   Default value: `28800`
-   Range: `[0, 31536000]`
-   Unit: Seconds
-   This variable controls the idle timeout of user sessions. A zero-value means unlimited.

### warning_count {#warning-count}

-   Scope: SESSION
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Default value: `0`
-   This read-only variable indicates the number of warnings that occurred in the statement that was previously executed.

### windowing_use_high_precision {#windowing-use-high-precision}

-   Scope: SESSION | GLOBAL
-   Persists to cluster: Yes
-   Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
-   Type: Boolean
-   Default value: `ON`
-   This variable controls whether to use the high precision mode when computing the [ウィンドウ関数](/functions-and-operators/window-functions.md).
