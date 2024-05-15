---
title: System Variables
summary: Use system variables to optimize performance or alter running behavior.
---

# システム変数 {#system-variables}

TiDB システム変数は、設定が`SESSION`または`GLOBAL`スコープに適用されるという点で、MySQL と同様に動作します。

-   スコープ`SESSION`の変更は現在のセッションにのみ影響します。
-   スコープ`GLOBAL`の変更はすぐに適用されます。この変数もスコープ`SESSION`に設定されている場合、すべてのセッション (自分のセッションを含む) は引き続き現在のセッション値を使用します。
-   変更は[`SET`ステートメント](/sql-statements/sql-statement-set-variable.md)使用して行われます:

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

v7.4.0 以降では、 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)を使用して、ステートメントの実行中に一部の`SESSION`変数の値を一時的に変更できます。ステートメントの実行後、現在のセッションのシステム変数の値は自動的に元の値に戻ります。このヒントを使用して、オプティマイザーとエグゼキューターに関連する一部のシステム変数を変更できます。このドキュメントの変数には`Applies to hint SET_VAR`設定があり、 `Yes`または`No`に構成できます。

-   `Applies to hint SET_VAR: Yes`に設定されている変数の場合、 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)ヒントを使用して、ステートメントの実行中に現在のセッションのシステム変数の値を変更できます。
-   `Applies to hint SET_VAR: No`に設定された変数の場合、ステートメントの実行中に[`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)ヒントを使用して現在のセッションのシステム変数の値を変更することはできません。

`SET_VAR`ヒントの詳細については、 [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)を参照してください。

## 変数参照 {#variable-reference}

### allow_auto_random_explicit_insert <span class="version-mark">v4.0.3 の新機能</span> {#allow-auto-random-explicit-insert-span-class-version-mark-new-in-v4-0-3-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `INSERT`ステートメントで`AUTO_RANDOM`属性を持つ列の値を明示的に指定できるようにするかどうかを決定します。

### authentication_ldap_sasl_auth_method_name <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `SCRAM-SHA-1`
-   可能な値: `SCRAM-SHA-1` 、 `SCRAM-SHA-256` 、および`GSSAPI` 。
-   LDAP SASL 認証の場合、この変数は認証方法名を指定します。

### authentication_ldap_sasl_bind_base_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は検索ツリー内の検索範囲を制限します。1 節`AS ...`でユーザーが作成された場合、TiDB はユーザー名に従って LDAPサーバーで`dn`自動的に検索します。

### authentication_ldap_sasl_bind_root_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。

### authentication_ldap_sasl_bind_root_pwd<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。

### authentication_ldap_sasl_ca_path <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は StartTLS 接続の証明機関ファイルの絶対パスを指定します。

### authentication_ldap_sasl_init_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーへの接続プール内の初期接続を指定します。

### authentication_ldap_sasl_max_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-sasl-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーへの接続プール内の最大接続数を指定します。

### authentication_ldap_sasl_server_host<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は LDAPサーバーのホスト名または IP アドレスを指定します。

### authentication_ldap_sasl_server_port<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### authentication_ldap_sasl_tls <span class="version-mark">v7.1.0 の新</span>機能 {#authentication-ldap-sasl-tls-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP SASL 認証の場合、この変数はプラグインによる LDAPサーバーへの接続が StartTLS で保護されるかどうかを制御します。

### authentication_ldap_simple_auth_method_name <span class="version-mark">v7.1.0 の新</span>機能 {#authentication-ldap-simple-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `SIMPLE`
-   可能な値: `SIMPLE` 。
-   LDAP シンプル認証の場合、この変数は認証方法名を指定します。サポートされる値は`SIMPLE`のみです。

### authentication_ldap_simple_bind_base_dn バージョン<span class="version-mark">7.1.0の新機能</span> {#authentication-ldap-simple-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP シンプル認証の場合、この変数は検索ツリー内の検索範囲を制限します。1 節`AS ...`でユーザーが作成された場合、TiDB はユーザー名に従って LDAPサーバーで`dn`自動的に検索します。

### authentication_ldap_simple_bind_root_dn バージョン<span class="version-mark">7.1.0の新機能</span> {#authentication-ldap-simple-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。

### authentication_ldap_simple_bind_root_pwd バージョン<span class="version-mark">7.1.0の新機能</span> {#authentication-ldap-simple-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。

### authentication_ldap_simple_ca_path <span class="version-mark">v7.1.0 の新</span>機能 {#authentication-ldap-simple-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は StartTLS 接続の証明機関ファイルの絶対パスを指定します。

### authentication_ldap_simple_init_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーへの接続プール内の初期接続を指定します。

### authentication_ldap_simple_max_pool_size <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーへの接続プール内の最大接続数を指定します。

### authentication_ldap_simple_server_host <span class="version-mark">v7.1.0 の新</span>機能 {#authentication-ldap-simple-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は LDAPサーバーのホスト名または IP アドレスを指定します。

### authentication_ldap_simple_server_port<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### authentication_ldap_simple_tls <span class="version-mark">v7.1.0 の新機能</span> {#authentication-ldap-simple-tls-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP 簡易認証の場合、この変数はプラグインによる LDAPサーバーへの接続が StartTLS で保護されるかどうかを制御します。

### 自動増分 {#auto-increment-increment}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てる`AUTO_INCREMENT`値のステップ サイズと`AUTO_RANDOM` ID の割り当てルールを制御します。 [`auto_increment_offset`](#auto_increment_offset)と組み合わせて使用​​されることが多いです。

### 自動増分オフセット {#auto-increment-offset}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てられる`AUTO_INCREMENT`値の初期オフセットと、 `AUTO_RANDOM` ID の割り当てルールを制御します。この設定は、多くの場合、 [`auto_increment_increment`](#auto_increment_increment)と組み合わせて使用​​されます。例:

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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   明示的なトランザクションでない場合にステートメントを自動的にコミットするかどうかを制御します。詳細については[トランザクションの概要](/transaction-overview.md#autocommit)を参照してください。

### ブロック暗号化モード {#block-encryption-mode}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `aes-128-ecb`
-   `aes-256-cbc` `aes-128-cbc` `aes-192-cbc` `aes-256-ecb` `aes-128-ecb` `aes-192-ecb` `aes-128-ofb` `aes-192-ofb` `aes-256-ofb` `aes-128-cfb` `aes-192-cfb` `aes-256-cfb`
-   この変数は、組み込み関数`AES_ENCRYPT()`および`AES_DECRYPT()`暗号化モードを設定します。

### 文字セットクライアント {#character-set-client}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   クライアントから送信されるデータの文字セット。TiDB での文字セットと照合順序の使用の詳細については、 [文字セットと照合順序](/character-set-and-collation.md)参照してください。必要に応じて[`SET NAMES`](/sql-statements/sql-statement-set-names.md)を使用して文字セットを変更することをお勧めします。

### 文字セット接続 {#character-set-connection}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   指定された文字セットを持たない文字列リテラルの文字セット。

### 文字セットデータベース {#character-set-database}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   この変数は、使用中のデフォルト データベースの文字セットを示します。**この変数を設定することはお勧めしません**。新しいデフォルト データベースが選択されると、サーバーは変数値を変更します。

### 文字セットの結果 {#character-set-results}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   データがクライアントに送信されるときに使用される文字セット。

### 文字セットサーバー {#character-set-server}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   サーバーのデフォルトの文字セット。

### 照合接続 {#collation-connection}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4_bin`
-   この変数は、現在の接続で使用されている照合順序を示します。これは、MySQL 変数`collation_connection`と一致します。

### 照合データベース {#collation-database}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4_bin`
-   この変数は、使用中のデータベースのデフォルトの照合順序を示します。**この変数を設定することは推奨されません**。新しいデータベースが選択されると、TiDB はこの変数値を変更します。

### 照合サーバー {#collation-server}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4_bin`
-   データベースの作成時に使用されるデフォルトの照合順序。

### cte_max_recursion_depth {#cte-max-recursion-depth}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[0, 4294967295]`
-   共通テーブル式の最大再帰深度を制御します。

### データディレクトリ {#datadir}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)ではサポートされていません。

<CustomContent platform="tidb">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値:コンポーネントと展開方法によって異なります。
    -   `/tmp/tidb` : [`--store`](/command-line-flags-for-tidb-configuration.md#--store)に`"unistore"`設定した場合、または`--store`設定しない場合。
    -   `${pd-ip}:${pd-port}` : Kubernetes デプロイメント用のTiUPおよびTiDB Operatorのデフォルトのstorageエンジンである TiKV を使用する場合。
-   この変数は、データが保存される場所を示します。この場所は、ローカル パス`/tmp/tidb`にすることも、データが TiKV に保存されている場合は PDサーバーを指すこともできます。3 という形式の値`${pd-ip}:${pd-port}` 、起動時に TiDB が接続する PDサーバーを示します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値:コンポーネントと展開方法によって異なります。
    -   `/tmp/tidb` : [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store)に`"unistore"`設定した場合、または`--store`設定しない場合。
    -   `${pd-ip}:${pd-port}` : Kubernetes デプロイメント用のTiUPおよびTiDB Operatorのデフォルトのstorageエンジンである TiKV を使用する場合。
-   この変数は、データが保存される場所を示します。この場所は、ローカル パス`/tmp/tidb`にすることも、データが TiKV に保存されている場合は PDサーバーを指すこともできます。3 という形式の値`${pd-ip}:${pd-port}` 、起動時に TiDB が接続する PDサーバーを示します。

</CustomContent>

### ddl_slow_threshold {#ddl-slow-threshold}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   実行時間がしきい値を超える DDL 操作をログに記録します。

### デフォルト認証プラグイン {#default-authentication-plugin}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `mysql_native_password`
-   可能`authentication_ldap_simple`値: `mysql_native_password` `tidb_sm3_password` `tidb_auth_token` `authentication_ldap_sasl` `caching_sha2_password`
-   この変数は、サーバーとクライアントの接続が確立されるときにサーバーが通知する認証方法を設定します。
-   `tidb_sm3_password`方法で認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)使用して TiDB に接続できます。

<CustomContent platform="tidb">

この変数の可能な値の詳細については、 [認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status)参照してください。

</CustomContent>

### default_collat​​ion_for_utf8mb4 <span class="version-mark">v7.4.0 の新</span>機能 {#default-collation-for-utf8mb4-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: グローバル | セッション
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: `utf8mb4_bin`
-   値`utf8mb4_general_ci` `utf8mb4_0900_ai_ci` : `utf8mb4_bin`
-   この変数は、 `utf8mb4`文字セットのデフォルト[照合順序](/character-set-and-collation.md)を設定するために使用されます。これは、次のステートメントの動作に影響します。
    -   [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)と[`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)のステートメントに表示されるデフォルトの照合順序。
    -   [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)および[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)ステートメントに、照合順序を指定せずにテーブルまたは列に対して`CHARACTER SET utf8mb4`節が含まれている場合、この変数で指定された照合順序が使用されます。これは、 `CHARACTER SET`節が使用されていない場合の動作には影響しません。
    -   [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)と[`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)ステートメントに照合順序を指定せずに`CHARACTER SET utf8mb4`句が含まれている場合、この変数で指定された照合順序が使用されます。これは、 `CHARACTER SET`番目の句が使用されていない場合の動作には影響しません。
    -   `COLLATE`句が使用されていない場合、 `_utf8mb4'string'`形式のすべてのリテラル文字列はこの変数で指定された照合順序を使用します。

### default_password_lifetime <span class="version-mark">v6.5.0 の新機能</span> {#default-password-lifetime-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 65535]`
-   自動パスワード有効期限のグローバル ポリシーを設定します。デフォルト値`0` 、パスワードが期限切れにならないことを示します。このシステム変数が正の整数`N`に設定されている場合、パスワードの有効期間は`N`日間であり、 `N`日以内にパスワードを変更する必要があります。

### デフォルトの週の形式 {#default-week-format}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 7]`
-   `WEEK()`関数で使用される週の形式を設定します。

### disconnect_on_expired_pa​​ssword <span class="version-mark">v6.5.0 の新</span>機能 {#disconnect-on-expired-password-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は読み取り専用です。パスワードの有効期限が切れたときに TiDB がクライアント接続を切断するかどうかを示します。変数が`ON`に設定されている場合、パスワードの有効期限が切れるとクライアント接続が切断されます。変数が`OFF`に設定されている場合、クライアント接続は「サンドボックス モード」に制限され、ユーザーはパスワード リセット操作のみを実行できます。

<CustomContent platform="tidb">

-   期限切れのパスワードに対するクライアント接続の動作を変更する必要がある場合は、構成ファイル内の[`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)構成項目を変更します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   期限切れのパスワードに対するクライアント接続のデフォルトの動作を変更する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

</CustomContent>

### エラー数 {#error-count}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   メッセージを生成した最後のステートメントから発生したエラーの数を示す読み取り専用変数。

### 外部キーチェック {#foreign-key-checks}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: v6.6.0 より前では、デフォルト値は`OFF`です。v6.6.0 以降では、デフォルト値は`ON`です。
-   この変数は、外部キー制約チェックを有効にするかどうかを制御します。

### グループ連結最大長 {#group-concat-max-len}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[4, 18446744073709551615]`
-   `GROUP_CONCAT()`関数内の項目の最大バッファ サイズ。

### オープンSSLを持つ {#have-openssl}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQL 互換性のための読み取り専用変数。サーバーで TLS が有効になっている場合は、サーバーによって`YES`に設定されます。

### SSLがある {#have-ssl}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQL 互換性のための読み取り専用変数。サーバーで TLS が有効になっている場合は、サーバーによって`YES`に設定されます。

### ホスト名 {#hostname}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: (システムホスト名)
-   読み取り専用変数としての TiDBサーバーのホスト名。

### アイデンティティ<span class="version-mark">v5.3.0 の新</span>機能 {#identity-span-class-version-mark-new-in-v5-3-0-span}

この変数は[`last_insert_id`](#last_insert_id)の別名です。

### 初期化接続 {#init-connect}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   `init_connect`機能により、TiDBサーバーに初めて接続するときに SQL ステートメントが自動的に実行されます。 `CONNECTION_ADMIN`または`SUPER`権限がある場合、この`init_connect`ステートメントは実行されません。 `init_connect`ステートメントでエラーが発生した場合、ユーザー接続は終了します。

### innodb_lock_wait_timeout {#innodb-lock-wait-timeout}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `50`
-   範囲: `[1, 3600]`
-   単位: 秒
-   悲観的トランザクションのロック待機タイムアウト (デフォルト)。

### インタラクティブタイムアウト {#interactive-timeout}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[1, 31536000]`
-   単位: 秒
-   この変数は、対話型ユーザー セッションのアイドル タイムアウトを表します。対話型ユーザー セッションとは、 `CLIENT_INTERACTIVE`オプション (MySQL Shell や MySQL Client など) を使用して[`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API を呼び出すことによって確立されたセッションを指します。この変数は MySQL と完全に互換性があります。

### 最後の挿入ID {#last-insert-id}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、挿入ステートメントによって生成された最後`AUTO_INCREMENT`または`AUTO_RANDOM`値を返します。
-   `last_insert_id`の値は、関数`LAST_INSERT_ID()`によって返される値と同じです。

### last_plan_from_binding <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-binding-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、前のステートメントで使用された実行計画が[プランバインディング](/sql-plan-management.md)の影響を受けたかどうかを示すために使用されます。

### last_plan_from_cache <span class="version-mark">v4.0 の新</span>機能 {#last-plan-from-cache-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、前の`execute`ステートメントで使用された実行プランがプラン キャッシュから直接取得されたかどうかを示すために使用されます。

### last_sql_use_alloc <span class="version-mark">v6.4.0 の新機能</span> {#last-sql-use-alloc-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `OFF`
-   この変数は読み取り専用です。前のステートメントがキャッシュされたチャンク オブジェクト (チャンク割り当て) を使用するかどうかを示すために使用されます。

### ライセンス {#license}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `Apache License 2.0`
-   この変数は、TiDBサーバーインストールのライセンスを示します。

### ログビン {#log-bin}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は[TiDBBinlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview)が使用されているかどうかを示します。

### max_allowed_pa​​cket <span class="version-mark">v6.1.0 の新</span>機能 {#max-allowed-packet-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `67108864`
-   範囲: `[1024, 1073741824]`
-   値は 1024 の整数倍である必要があります。値が 1024 で割り切れない場合は警告が表示され、値は切り捨てられます。たとえば、値が 1025 に設定されている場合、TiDB の実際の値は 1024 です。
-   1 回のパケット送信でサーバーとクライアントが許可する最大パケット サイズ。
-   `SESSION`スコープでは、この変数は読み取り専用です。
-   この変数は MySQL と互換性があります。

### password_history <span class="version-mark">v6.5.0 の新機能</span> {#password-history-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、パスワード変更回数に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0` 、パスワード変更回数に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数が正の整数`N`に設定されている場合、最後の`N`のパスワードの再利用は許可されません。

### mpp_exchange_compression_mode <span class="version-mark">v6.6.0 の新</span>機能 {#mpp-exchange-compression-mode-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `UNSPECIFIED`
-   `UNSPECIFIED` `FAST` `HIGH_COMPRESSION` : `NONE`
-   この変数は、MPP Exchange オペレータのデータ圧縮モードを指定するために使用されます。この変数は、TiDB がバージョン番号`1`の MPP 実行プランを選択した場合に有効になります。変数値の意味は次のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。TiDB は圧縮モードを自動的に選択します。現在、TiDB は`FAST`モードを自動的に選択します。
    -   `NONE` : データ圧縮は使用されません。
    -   `FAST` : 高速モード。全体的なパフォーマンスは良好で、圧縮率は`HIGH_COMPRESSION`未満です。
    -   `HIGH_COMPRESSION` : 高圧縮比モード。

### mpp_version <span class="version-mark">v6.6.0 の新</span>機能 {#mpp-version-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `UNSPECIFIED`
-   値`0` `1` : `UNSPECIFIED`
-   この変数は、MPP 実行プランの異なるバージョンを指定するために使用されます。バージョンを指定すると、TiDB は指定されたバージョンの MPP 実行プランを選択します。変数値の意味は次のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。TiDB は最新バージョン`1`を自動的に選択します。
    -   `0` : すべての TiDB クラスター バージョンと互換性があります。このモードでは、MPP バージョンが`0`より大きい機能は有効になりません。
    -   `1` : v6.6.0 の新機能。TiFlashで圧縮によるデータ交換を有効にするために使用されます。詳細については、 [MPPバージョンと交換データ圧縮](/explain-mpp.md#mpp-version-and-exchange-data-compression)を参照してください。

### password_reuse_interval <span class="version-mark">v6.5.0 の新機能</span> {#password-reuse-interval-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、経過時間に基づいて TiDB がパスワードの再利用を制限できるようにするパスワード再利用ポリシーを確立するために使用されます。デフォルト値`0` 、経過時間に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数が正の整数`N`に設定されている場合、過去`N`日間に使用されたパスワードの再利用は許可されません。

### 最大接続数 {#max-connections}

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   単一の TiDB インスタンスに許可される同時接続の最大数。この変数はリソース制御に使用できます。
-   デフォルト値`0`制限がないことを意味します。この変数の値が`0`より大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新しい接続を拒否します。

### 最大実行時間 {#max-execution-time}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   ステートメントの最大実行時間。デフォルト値は無制限 (ゼロ) です。

> **注記：**
>
> `max_execution_time`システム変数は現在、読み取り専用 SQL ステートメントの最大実行時間のみを制御します。タイムアウト値の精度はおよそ 100 ミリ秒です。つまり、指定した正確なミリ秒数でステートメントが終了しない可能性があります。

<CustomContent platform="tidb">

ヒント[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)を持つ SQL 文の場合、この文の最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、説明されているように、SQL バインディングで使用することもできます[SQL FAQで](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

ヒント[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)を持つ SQL 文の場合、この文の最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、説明されているように、SQL バインディングで使用することもできます[SQL FAQで](https://docs.pingcap.com/tidb/stable/sql-faq) 。

</CustomContent>

### 最大準備済みステートメント数 {#max-prepared-stmt-count}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 1048576]`
-   現在の TiDB インスタンス内の[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントの最大数を指定します。
-   値`-1`は、現在の TiDB インスタンス内のステートメントの最大数`PREPARE`に制限がないことを意味します。
-   変数を上限`1048576`を超える値に設定した場合、代わりに`1048576`が使用されます。

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

### プラグインディレクトリ {#plugin-dir}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)ではサポートされていません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   コマンドラインフラグで指定されたプラグインをロードするディレクトリを示します。

### プラグインロード {#plugin-load}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)ではサポートされていません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   TiDB の起動時にロードするプラグインを示します。これらのプラグインは、コマンドライン フラグで指定され、カンマで区切られます。

### ポート {#port}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 65535]`
-   MySQL プロトコルを話すときに`tidb-server`リッスンしているポート。

### ランドシード1 {#rand-seed1}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL 関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作は MySQL と互換性があります。

### ランドシード2 {#rand-seed2}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、 `RAND()` SQL 関数で使用されるランダム値ジェネレーターをシードするために使用されます。
-   この変数の動作は MySQL と互換性があります。

### require_secure_transport <span class="version-mark">v6.1.0 の新</span>機能 {#require-secure-transport-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> 現在、この変数は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated)ではサポートされていません。TiDB 専用クラスターではこの変数を有効にし**ないで**ください。有効にしないと、SQL クライアント接続エラーが発生する可能性があります。この制限は一時的な制御手段であり、将来のリリースで解決される予定です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: TiDBセルフホストの場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) `ON`は`OFF`

<CustomContent platform="tidb">

-   この変数は、TiDB へのすべての接続がローカル ソケット上にあるか、TLS を使用していることを保証します。詳細については[TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB へのすべての接続がローカル ソケット上にあるか、TLS を使用していることを保証します。

</CustomContent>

-   この変数を`ON`に設定すると、TLS が有効になっているセッションから TiDB に接続する必要があります。これにより、TLS が正しく構成されていない場合にロックアウト シナリオが発生するのを防ぐことができます。
-   この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。
-   v7.5.1 以降の v7.5 パッチ バージョンでは、Security拡張モード (SEM) が有効になっている場合、ユーザーの接続に関する潜在的な問題を回避するために、この変数を`ON`に設定することは禁止されています。

### skip_name_resolve <span class="version-mark">v5.2.0 の新機能</span> {#skip-name-resolve-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `tidb-server`インスタンスが接続ハンドシェイクの一部としてホスト名を解決するかどうかを制御します。
-   DNS が信頼できない場合は、このオプションを有効にしてネットワーク パフォーマンスを向上させることができます。

> **注記：**
>
> `skip_name_resolve=ON`場合、ID にホスト名を持つユーザーはサーバーにログインできなくなります。例:
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> この例では、 `apphost` IPアドレスまたはワイルドカード（ `%` ）に置き換えることをお勧めします。

### ソケット {#socket}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   MySQL プロトコルを話すときに`tidb-server`リッスンしているローカル UNIX ソケット ファイル。

### sql_log_bin {#sql-log-bin}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   変更を[TiDBBinlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview)に書き込むかどうかを示します。

> **注記：**
>
> TiDB の将来のバージョンでは、これをセッション変数としてのみ設定できるようになる可能性があるため、 `sql_log_bin`グローバル変数として設定することはお勧めしません。

### SQLモード {#sql-mode}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
-   この変数は、いくつかの MySQL 互換性動作を制御します。詳細については、 [SQL モード](/sql-mode.md)参照してください。

### sql_require_primary_key <span class="version-mark">v6.3.0 の新</span>機能 {#sql-require-primary-key-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、テーブルに主キーが必要であるという要件を強制するかどうかを制御します。この変数を有効にすると、主キーのないテーブルを作成または変更しようとするとエラーが発生します。
-   この機能は、MySQL 8.0 の同様の名前の[`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key)に基づいています。
-   TiCDC を使用する場合は、この変数を有効にすることを強くお勧めします。これは、MySQL シンクへの変更をレプリケートするには、テーブルに主キーが必要であるためです。

<CustomContent platform="tidb">

-   この変数を有効にし、TiDB データ移行 (DM) を使用してデータを移行する場合は、 [DM タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)の`session`の部分に`sql_require_ primary_key`を追加して`OFF`に設定することをお勧めします。そうしないと、DM がタスクを作成できなくなります。

</CustomContent>

### sql_select_limit <span class="version-mark">v4.0.2 の新機能</span> {#sql-select-limit-span-class-version-mark-new-in-v4-0-2-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `18446744073709551615`
-   範囲: `[0, 18446744073709551615]`
-   単位: 行
-   `SELECT`ステートメントによって返される行の最大数。

### ssl_ca {#ssl-ca}

<CustomContent platform="tidb">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   証明機関ファイルの場所（存在する場合）。この変数の値は、TiDB 構成項目[`ssl-ca`](/tidb-configuration-file.md#ssl-ca)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   証明機関ファイルの場所（存在する場合）。この変数の値は、TiDB 構成項目[`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca)によって定義されます。

</CustomContent>

### SSL証明書 {#ssl-cert}

<CustomContent platform="tidb">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される証明書ファイル (ファイルがある場合) の場所。この変数の値は、TiDB 構成項目[`ssl-cert`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される証明書ファイル (ファイルがある場合) の場所。この変数の値は、TiDB 構成項目[`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert)によって定義されます。

</CustomContent>

### SSLキー {#ssl-key}

<CustomContent platform="tidb">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される秘密鍵ファイル (存在する場合) の場所。この変数の値は、TiDB 構成項目[`ssl-key`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS 接続に使用される秘密鍵ファイル (存在する場合) の場所。この変数の値は、TiDB 構成項目[`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key)によって定義されます。

</CustomContent>

### システムタイムゾーン {#system-time-zone}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: (システム依存)
-   この変数は、TiDB が最初にブートストラップされたときのシステム タイム ゾーンを示します。1 [`time_zone`](#time_zone)参照してください。

### tidb_adaptive_closest_read_threshold <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-adaptive-closest-read-threshold-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `4096`
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、 [`tidb_replica_read`](#tidb_replica_read-new-in-v40) `closest-adaptive`に設定されている場合に、TiDBサーバーが読み取り要求を TiDBサーバーと同じアベイラビリティ ゾーン内のレプリカに送信することを優先するしきい値を制御するために使用されます。推定結果がこのしきい値以上の場合、TiDB は同じアベイラビリティ ゾーン内のレプリカに読み取り要求を送信することを優先します。それ以外の場合、TiDB はリーダー レプリカに読み取り要求を送信します。

### tidb_allow_tiflash_cop <span class="version-mark">v7.3.0 の新</span>機能 {#tidb-allow-tiflash-cop-span-class-version-mark-new-in-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   TiDB が計算タスクをTiFlashにプッシュダウンする場合、選択できる方法 (またはプロトコル) は、Cop、BatchCop、および MPP の 3 つです。Cop や BatchCop と比較すると、MPP プロトコルはより成熟しており、タスクとリソースの管理がより優れています。したがって、MPP プロトコルを使用することをお勧めします。
    -   `0`または`OFF` : オプティマイザーはTiFlash MPP プロトコルを使用してのみプランを生成します。
    -   `1`または`ON` : オプティマイザーは、コスト見積もりに基づいて実行プランを生成するために Cop、BatchCop、または MPP プロトコルを使用するかどうかを決定します。

### tidb_allow_batch_cop <span class="version-mark">v4.0 の新</span>機能 {#tidb-allow-batch-cop-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   この変数は、TiDB がコプロセッサ要求をTiFlashに送信する方法を制御するために使用されます。次の値があります。

    -   `0` : リクエストをバッチで送信しない
    -   `1` :集計および参加リクエストはバッチで送信されます
    -   `2` : すべてのコプロセッサ要求はバッチで送信されます

### tidb_allow_fallback_to_tikv<span class="version-mark">バージョン5.0の新機能</span> {#tidb-allow-fallback-to-tikv-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: &quot;&quot;
-   この変数は、TiKV にフォールバックする可能性のあるstorageエンジンのリストを指定するために使用されます。リスト内の指定されたstorageエンジンの障害により SQL ステートメントの実行が失敗した場合、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。この変数は、&quot;&quot; または &quot;tiflash&quot; に設定できます。この変数が &quot;tiflash&quot; に設定されている場合、 TiFlash がタイムアウト エラー (エラー コード: ErrTiFlashServerTimeout) を返すと、TiDB は TiKV を使用してこの SQL ステートメントの実行を再試行します。

### tidb_allow_function_for_expression_index <span class="version-mark">v5.2.0 の新</span>機能 {#tidb-allow-function-for-expression-index-span-class-version-mark-new-in-v5-2-0-span}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   `json_array_append` `json_contains` `json_array_insert` `json_array` `json_contains_path` `json_depth` `json_extract` `json_insert` `json_keys` `json_length` `json_merge_patch` `json_merge_preserve` `json_object` `json_pretty` `json_quote` `json_remove` `json_replace` `json_search` `json_set` `json_storage_size` `json_type` `json_unquote` `json_valid` `lower` `md5` `reverse` `tidb_shard` `upper` `vitess_hash`
-   この変数は、式インデックスの作成に使用できる関数を表示するために使用されます。

### tidb_allow_mpp <span class="version-mark">v5.0 の新</span>機能 {#tidb-allow-mpp-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   クエリを実行するためにTiFlashの MPP モードを使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF` 。これは MPP モードが使用されないことを意味します。v7.3.0 以降のバージョンでは、この変数の値を`0`または`OFF`に設定する場合は、 [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)変数も有効にする必要があります。そうしないと、クエリでエラーが返される可能性があります。
    -   `1`または`ON` 。これは、オプティマイザがコスト推定に基づいて MPP モードを使用するかどうかを決定することを意味します (デフォルト)。

MPP はTiFlashエンジンが提供する分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能で高スループットの SQL アルゴリズムを提供します。MPP モードの選択の詳細については、 [MPPモードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_allow_remove_auto_inc <span class="version-mark">v2.1.18 および v3.0.4 の新機能</span> {#tidb-allow-remove-auto-inc-span-class-version-mark-new-in-v2-1-18-and-v3-0-4-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`ステートメントを実行して列の`AUTO_INCREMENT`プロパティを削除できるかどうかを設定するために使用されます。デフォルトでは許可されていません。

### tidb_analyze_partition_concurrency {#tidb-analyze-partition-concurrency}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `2` 。v7.4.0 以前のバージョンではデフォルト値は`1`です。
-   この変数は、TiDB がパーティションテーブルを分析するときに、パーティションテーブルの統計の読み取りと書き込みの同時実行を指定します。

### tidb_analyze_version <span class="version-mark">v5.1.0 の新</span>機能 {#tidb-analyze-version-span-class-version-mark-new-in-v5-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   TiDB が統計を収集する方法を制御します。
    -   TiDB Self-Hosted の場合、この変数のデフォルト値は、v5.3.0 以降で`1`から`2`に変更されます。
    -   TiDB Cloudの場合、この変数のデフォルト値は、v6.5.0 以降で`1`から`2`に変更されます。
    -   クラスターが以前のバージョンからアップグレードされた場合、アップグレード後もデフォルト値`tidb_analyze_version`は変更されません。
-   この変数の詳細な説明については[統計入門](/statistics.md)参照してください。

### tidb_analyze_skip_column_types <span class="version-mark">v7.2.0 の新機能</span> {#tidb-analyze-skip-column-types-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;json,blob,mediumblob,longblob&quot;
-   可能な値: &quot;json、blob、mediumblob、longblob、text、mediumtext、longtext&quot;
-   この変数は、統計を収集する`ANALYZE`コマンドを実行するときに、統計収集でスキップされる列のタイプを制御します。この変数は`tidb_analyze_version = 2`にのみ適用されます。 `ANALYZE TABLE t COLUMNS c1, ... , cn`を使用して列を指定しても、そのタイプが`tidb_analyze_skip_column_types`の場合、指定された列の統計は収集されません。

<!---->

    mysql> SHOW CREATE TABLE t;
    +-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Table | Create Table                                                                                                                                                                                                             |
    +-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | t     | CREATE TABLE `t` (
      `a` int(11) DEFAULT NULL,
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

### tidb_auto_analyze_終了時間 {#tidb-auto-analyze-end-time}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、UTC 時間で午前 1 時から午前 3 時までの間のみ自動統計更新を許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`設定します。

### tidb_auto_analyze_partition_batch_size <span class="version-mark">v6.4.0 の新</span>機能 {#tidb-auto-analyze-partition-batch-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `1`
-   範囲: `[1, 1024]`
-   この変数は、パーティションテーブルを分析するときに TiDB [自動的に分析する](/statistics.md#automatic-update)が実行するパーティションの数を指定します (つまり、パーティションテーブルの統計情報を自動的に収集します)。
-   この変数の値がパーティション数より小さい場合、TiDB はパーティションテーブルのすべてのパーティションを複数のバッチで自動的に分析します。この変数の値がパーティション数以上の場合、TiDB はパーティションテーブルのすべてのパーティションを同時に分析します。
-   パーティションテーブルのパーティション数がこの変数値よりもはるかに多く、自動分析に時間がかかる場合は、この変数の値を増やして時間の消費を減らすことができます。

### tidb_自動分析比率 {#tidb-auto-analyze-ratio}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.5`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、TiDB がバックグラウンド スレッドで[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)自動的に実行してテーブル統計を更新するときのしきい値を設定するために使用されます。たとえば、値が 0.5 の場合、テーブル内の行の 50% 以上が変更されたときに自動分析がトリガーされます。 `tidb_auto_analyze_start_time`と`tidb_auto_analyze_end_time`を指定すると、自動分析が特定の時間帯にのみ実行されるように制限できます。

> **注記：**
>
> この機能を使用するには、システム変数`tidb_enable_auto_analyze` `ON`に設定する必要があります。

### tidb_auto_analyze_start_time {#tidb-auto-analyze-start-time}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、統計の自動更新が許可される時間枠を制限するために使用されます。たとえば、UTC 時間で午前 1 時から午前 3 時までの間のみ自動統計更新を許可するには、 `tidb_auto_analyze_start_time='01:00 +0000'`と`tidb_auto_analyze_end_time='03:00 +0000'`設定します。

### tidb_auto_build_stats_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-auto-build-stats-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、統計の自動更新を実行する同時実行性を設定するために使用されます。

### tidb_backoff_lock_fast {#tidb-backoff-lock-fast}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 2147483647]`
-   この変数は、読み取り要求がロックに遭遇する`backoff`回を設定するために使用されます。

### tidb_backoff_weight {#tidb-backoff-weight}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB `backoff`の最大時間、つまり、内部ネットワークまたはその他のコンポーネント(TiKV、PD) の障害が発生したときに再試行要求を送信するための最大再試行時間の重みを増やすために使用されます。この変数は最大再試行時間を調整するために使用でき、最小値は 1 です。

    たとえば、TiDB が PD から TSO を取得するための基本タイムアウトは 15 秒です。 `tidb_backoff_weight = 2`場合、TSO を取得するための最大タイムアウトは、*基本時間 * 2 = 30 秒*です。

    ネットワーク環境が悪い場合、この変数の値を適切に増やすことで、タイムアウトによってアプリケーション側へのエラー報告を効果的に軽減できます。アプリケーション側でエラー情報をより早く受け取りたい場合は、この変数の値を最小にしてください。

### tidb_バッチコミット {#tidb-batch-commit}

> **警告：**
>
> この変数を有効にすることはお勧め**しません**。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチコミット機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、いくつかのステートメントをグループ化してトランザクションを複数のトランザクションに分割し、非アトミックにコミットする可能性がありますが、これは推奨されません。

### tidb_batch_delete {#tidb-batch-delete}

> **警告：**
>
> この変数は、非推奨の batch-dml 機能に関連付けられており、データの破損を引き起こす可能性があります。したがって、batch-dml に対してこの変数を有効にすることはお勧めしません。代わりに[非トランザクションDML](/non-transactional-dml.md)を使用してください。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨の batch-dml 機能の一部である batch-delete 機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `DELETE`ステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`有効にして、 `tidb_dml_batch_size`に正の値を設定する必要がありますが、これは推奨されません。

### tidb_batch_insert {#tidb-batch-insert}

> **警告：**
>
> この変数は、非推奨の batch-dml 機能に関連付けられており、データの破損を引き起こす可能性があります。したがって、batch-dml に対してこの変数を有効にすることはお勧めしません。代わりに[非トランザクションDML](/non-transactional-dml.md)を使用してください。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨の batch-dml 機能の一部である batch-insert 機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、 `INSERT`ステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを機能させるには、 `tidb_enable_batch_dml`有効にして、 `tidb_dml_batch_size`に正の値を設定する必要がありますが、これは推奨されません。

### tidb_batch_pending_tiflash_count <span class="version-mark">v6.0 の新</span>機能 {#tidb-batch-pending-tiflash-count-span-class-version-mark-new-in-v6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 4294967295]`
-   `ALTER DATABASE SET TIFLASH REPLICA`使用してTiFlashレプリカを追加するときに許可される使用不可テーブルの最大数を指定します。使用不可テーブルの数がこの制限を超えると、操作が停止するか、残りのテーブルに対するTiFlashレプリカの設定が非常に遅くなります。

### tidb_broadcast_join_threshold_count <span class="version-mark">v5.0 の新機能</span> {#tidb-broadcast-join-threshold-count-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `10240`
-   範囲: `[0, 9223372036854775807]`
-   単位: 行
-   結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを見積もることができません。この場合、サイズは結果セットの行数によって決まります。サブクエリの推定行数がこの変数の値より少ない場合、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   この変数は、 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)有効になると有効になりません。

### tidb_broadcast_join_threshold_size <span class="version-mark">v5.0 の新</span>機能 {#tidb-broadcast-join-threshold-size-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `104857600` (100 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   テーブル サイズが変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   この変数は、 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)有効になると有効になりません。

### tidb_build_stats_concurrency {#tidb-build-stats-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2` 。v7.4.0 以前のバージョンではデフォルト値は`4`です。
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `ANALYZE`ステートメントを実行する同時実行性を設定するために使用されます。
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_build_sampling_stats_concurrency <span class="version-mark">v7.5.0 の新機能</span> {#tidb-build-sampling-stats-concurrency-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   単位: スレッド
-   デフォルト値： `2`
-   範囲: `[1, 256]`
-   この変数は、 `ANALYZE`プロセスでのサンプリング同時実行性を設定するために使用されます。
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_capture_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-capture-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [ベースラインキャプチャ](/sql-plan-management.md#baseline-capturing)機能を有効にするかどうかを制御するために使用されます。この機能はステートメント サマリーに依存するため、ベースライン キャプチャを使用する前にステートメント サマリーを有効にする必要があります。
-   この機能を有効にすると、ステートメント サマリー内の履歴 SQL ステートメントが定期的に走査され、少なくとも 2 回出現する SQL ステートメントに対してバインディングが自動的に作成されます。

### tidb_cdc_write_source <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-cdc-write-source-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   スコープ: セッション
-   クラスターに存続: いいえ
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `utf8`文字セットに[基本多言語面 (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane)の値のみを格納するように強制するために使用されます。BMP 外の文字を格納するには、 `utf8mb4`文字セットを使用することをお勧めします。
-   `utf8`チェックが緩やかだった以前のバージョンの TiDB からクラスターをアップグレードする場合は、このオプションを無効にする必要がある場合があります。詳細については、 [アップグレード後のよくある質問](https://docs.pingcap.com/tidb/stable/upgrade-faq)を参照してください。

### tidb_チェックサム_テーブル_同時実行性 {#tidb-checksum-table-concurrency}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)ステートメントを実行するスキャン インデックスの同時実行性を設定するために使用されます。
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_committer_concurrency <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-committer-concurrency-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   この変数は読み取り専用です。現在の TiDBサーバーの構成情報を取得するために使用されます。

### tidb_constraint_check_in_place {#tidb-constraint-check-in-place}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は楽観的トランザクションにのみ適用されます。悲観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-new-in-v630)使用します。
-   この変数を`OFF`に設定すると、一意のインデックス内の重複値のチェックは、トランザクションがコミットされるまで延期されます。これによりパフォーマンスが向上しますが、一部のアプリケーションでは予期しない動作になる可能性があります。詳細については[制約](/constraints.md#optimistic-transactions)を参照してください。

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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: デフォルトでは、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)構成項目は`true`なので、この変数のデフォルト値は`ON`です。 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)が`false`に設定されている場合、この変数のデフォルト値は`OFF`です。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`

</CustomContent>

-   この変数は悲観的トランザクションにのみ適用されます。楽観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place)使用します。
-   この変数を`OFF`に設定すると、TiDB は一意のインデックスの一意制約チェックを延期します (インデックスへのロックを必要とするステートメントを次回実行するとき、またはトランザクションをコミットするときまで)。これによりパフォーマンスが向上しますが、一部のアプリケーションでは予期しない動作になる可能性があります。詳細については[制約](/constraints.md#pessimistic-transactions)を参照してください。
-   この変数を無効にすると、悲観的トランザクションで TiDB が`LazyUniquenessCheckFailure`エラーを返す可能性があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。
-   この変数が無効になっている場合、悲観的トランザクションで[`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)使用できません。
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

### tidb_cost_model_version <span class="version-mark">v6.2.0 の新</span>機能 {#tidb-cost-model-version-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> -   TiDB v6.5.0 以降、新しく作成されたクラスターはデフォルトでコスト モデル バージョン 2 を使用します。TiDB バージョンを v6.5.0 より前から v6.5.0 以降にアップグレードした場合、 `tidb_cost_model_version`値は変更されません。
> -   コスト モデルのバージョンを切り替えると、クエリ プランが変更される可能性があります。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   値のオプション:
    -   `1` : TiDB v6.4.0 以前のバージョンでデフォルトで使用されるコスト モデル バージョン 1 を有効にします。
    -   `2` : [コストモデル バージョン 2](/cost-model.md#cost-model-version-2)を有効にします。これは TiDB v6.5.0 で一般に利用可能であり、内部テストではバージョン 1 よりも正確です。
-   コストモデルのバージョンはオプティマイザの計画決定に影響します。詳細については[コストモデル](/cost-model.md)を参照してください。

### tidb_current_ts {#tidb-current-ts}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は読み取り専用です。現在のトランザクションのタイムスタンプを取得するために使用されます。

### tidb_ddl_disk_quota <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-ddl-disk-quota-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `107374182400` (100 GiB)
-   範囲: `[107374182400, 1125899906842624]` ([100 GiB、1 PiB])
-   単位: バイト
-   この変数は[`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630)が有効になっている場合にのみ有効になります。インデックス作成時のバックフィル中のローカルstorageの使用制限を設定します。

### tidb_ddl_enable_fast_reorg <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-enable-fast-reorg-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> -   [TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated)クラスターを使用している場合、この変数を使用してインデックス作成の速度を向上させるには、TiDB クラスターが AWS でホストされ、TiDB ノードのサイズが少なくとも 8 vCPU であることを確認してください。
> -   [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターの場合、この変数は読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックス作成のバックフィルの速度を向上させるために、 `ADD INDEX`と`CREATE INDEX`のアクセラレーションを有効にするかどうかを制御します。この変数値を`ON`に設定すると、大量のデータを含むテーブルでのインデックス作成のパフォーマンスが向上します。
-   v7.1.0 以降、インデックス アクセラレーション操作はチェックポイントをサポートします。障害により TiDB 所有者ノードが再起動または変更された場合でも、TiDB は定期的に自動的に更新されるチェックポイントから進行状況を回復できます。
-   完了した`ADD INDEX`操作が高速化されているかどうかを確認するには、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)ステートメントを実行して、 `JOB_TYPE`列に`ingest`が表示されるかどうかを確認します。

<CustomContent platform="tidb">

> **注記：**
>
> -   インデックスの高速化には、書き込み可能で十分な空き領域がある[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)必要です。3 `temp-dir`使用できない場合、TiDB は高速化されていないインデックス構築にフォールバックします。5 `temp-dir` SSD ディスクに配置することをお勧めします。
>
> -   TiDB を v6.5.0 以降にアップグレードする前に、TiDB の[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)パスが SSD ディスクに正しくマウントされているかどうかを確認することをお勧めします。TiDB を実行するオペレーティング システム ユーザーに、このディレクトリの読み取りおよび書き込み権限があることを確認してください。権限がない場合、DDL 操作で予期しない問題が発生する可能性があります。このパスは TiDB 構成項目であり、TiDB の再起動後に有効になります。したがって、アップグレード前にこの構成項目を設定すると、再度の再起動を回避できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> 現在、この機能は[1 つの`ALTER TABLE`ステートメントで複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md)と完全に互換性がありません。インデックス アクセラレーションを使用して一意のインデックスを追加する場合は、同じステートメントで他の列またはインデックスを変更しないようにする必要があります。

</CustomContent>

### tidb_enable_dist_task <span class="version-mark">v7.1.0 の新</span>機能 {#tidb-enable-dist-task-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `OFF`
-   この変数は、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)を有効にするかどうかを制御するために使用されます。フレームワークを有効にすると、DDL やインポートなどの DXF タスクは、クラスター内の複数の TiDB ノードによって分散実行され、完了します。
-   TiDB v7.1.0 以降、DXF はパーティション化されたテーブルに対して[`ADD INDEX`](/sql-statements/sql-statement-add-index.md)ステートメントを分散して実行することをサポートします。
-   TiDB v7.2.0 以降、DXF はインポート ジョブの[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)ステートメントの分散実行をサポートします。
-   この変数は`tidb_ddl_distribute_reorg`から名前が変更されました。

### tidb_cloud_storage_uri <span class="version-mark">v7.4.0 の新</span>機能 {#tidb-cloud-storage-uri-span-class-version-mark-new-in-v7-4-0-span}

> **警告：**
>
> この機能は実験的ものです。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `""`
-   この変数は、Amazon S3 クラウドstorageURI を指定して[グローバルソート](/tidb-global-sort.md)有効にするために使用されます。 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)を有効にした後、URI を構成し、storageにアクセスするために必要な権限を持つ適切なクラウドstorageパスを指すようにすることで、グローバル ソート機能を使用できます。詳細については、 [Amazon S3 URI 形式](/external-storage-uri.md#amazon-s3-uri-format)を参照してください。
-   次のステートメントでは、グローバル ソート機能を使用できます。
    -   [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)番目のステートメント。
    -   インポート ジョブの[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)のステートメント。

### tidb_ddl_エラーカウント制限 {#tidb-ddl-error-count-limit}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `512`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、DDL 操作が失敗した場合の再試行回数を設定するために使用されます。再試行回数がパラメータ値を超えると、間違った DDL 操作はキャンセルされます。

### tidb_ddl_flashback_concurrency <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-flashback-concurrency-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `64`
-   範囲: `[1, 256]`
-   この変数は[`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)の同時実行性を制御します。

### tidb_ddl_reorg_バッチサイズ {#tidb-ddl-reorg-batch-size}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `256`
-   範囲: `[32, 10240]`
-   単位: 行
-   この変数は、DDL 操作のフェーズ`re-organize`中にバッチ サイズを設定するために使用されます。たとえば、TiDB が`ADD INDEX`操作を実行する場合、インデックス データは`tidb_ddl_reorg_worker_cnt` (数) の同時ワーカーによってバックフィルされる必要があります。各ワーカーは、インデックス データをバッチでバックフィルします。
    -   `ADD INDEX`操作中に`UPDATE`や`REPLACE`などの更新操作が多数存在する場合、バッチ サイズが大きいほどトランザクション競合の可能性が高くなります。この場合、バッチ サイズを小さい値に調整する必要があります。最小値は 32 です。
    -   トランザクションの競合が存在しない場合は、バッチ サイズを大きな値に設定できます (ワーカー数を考慮してください。参考として[オンライン ワークロードと`ADD INDEX`操作のインタラクション テスト](https://docs.pingcap.com/tidb/stable/online-workloads-and-add-index-operations)を参照してください)。これにより、データのバックフィルの速度が向上しますが、TiKV への書き込み圧力も高くなります。

### tidb_ddl_reorg_priority {#tidb-ddl-reorg-priority}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `PRIORITY_LOW`
-   値`PRIORITY_NORMAL` `PRIORITY_HIGH` : `PRIORITY_LOW`
-   この変数は、 `re-organize`フェーズで第`ADD INDEX`操作を実行する優先度を設定するために使用されます。
-   この変数の値は`PRIORITY_LOW` 、 `PRIORITY_NORMAL` 、または`PRIORITY_HIGH`に設定できます。

### tidb_ddl_reorg_worker_cnt {#tidb-ddl-reorg-worker-cnt}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `re-organize`フェーズでの DDL 操作の同時実行性を設定するために使用されます。

### tidb_default_string_match_selectivity <span class="version-mark">v6.2.0 の新</span>機能 {#tidb-default-string-match-selectivity-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   デフォルト値: `0.8`
-   範囲: `[0, 1]`
-   この変数は、行数を推定するときに、フィルター条件で`like` 、 `rlike` 、および`regexp`関数のデフォルトの選択性を設定するために使用されます。この変数は、これらの関数の推定を支援するために TopN を有効にするかどうかも制御します。
-   TiDB は、統計を使用してフィルター条件の`like`を推定しようとします。ただし、 `like`複雑な文字列に一致する場合、または`rlike`または`regexp`を使用する場合、TiDB は統計を十分に使用できないことが多く、代わりにデフォルト値の`0.8`が選択率として設定され、不正確な推定が発生します。
-   この変数は、前述の動作を変更するために使用されます。変数が`0`以外の値に設定されている場合、選択率は`0.8`ではなく指定された変数値になります。
-   変数が`0`に設定されている場合、TiDB は統計で TopN を使用して評価して精度を向上させ、前述の 3 つの関数を推定するときに統計で NULL 番号を考慮します。前提条件は、 [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510)が`2`に設定されているときに統計が収集されることです。このような評価は、パフォーマンスにわずかに影響を及ぼす可能性があります。
-   変数が`0.8`以外の値に設定されている場合、TiDB はそれに応じて`not like` 、 `not rlike` 、および`not regexp`の推定値を調整します。

### tidb_disable_txn_auto_retry {#tidb-disable-txn-auto-retry}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、明示的な楽観的トランザクションの自動再試行を無効にするかどうかを設定するために使用されます。デフォルト値`ON`は、トランザクションが TiDB で自動的に再試行されず、 `COMMIT`ステートメントがアプリケーションレイヤーで処理する必要があるエラーを返す可能性があることを意味します。

    値を`OFF`に設定すると、TiDB は自動的にトランザクションを再試行し、 `COMMIT`ステートメントからのエラーが少なくなります。この変更を行うときは、更新が失われる可能性があるため注意してください。

    この変数は、TiDB で自動的にコミットされた暗黙的なトランザクションや内部的に実行されたトランザクションには影響しません。これらのトランザクションの最大再試行回数は、値`tidb_retry_limit`によって決まります。

    詳細については[再試行の制限](/optimistic-transaction.md#limits-of-retry)参照してください。

    <CustomContent platform="tidb">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は[`max_retry_count`](/tidb-configuration-file.md#max-retry-count)で制御されます。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は 256 です。

    </CustomContent>

### tidb_distsql_scan_concurrency {#tidb-distsql-scan-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `15`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `scan`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。
-   OLAP シナリオの場合、最大値はすべての TiKV ノードの CPU コアの数を超えてはなりません。
-   テーブルに多数のパーティションがある場合は、変数値を適切に減らして（スキャンするデータのサイズとスキャンの頻度によって決定）、TiKV がメモリ(OOM) になるのを防ぐことができます。

### tidb_dml_バッチサイズ {#tidb-dml-batch-size}

> **警告：**
>
> この変数は、非推奨の batch-dml 機能に関連付けられており、データの破損を引き起こす可能性があります。したがって、batch-dml に対してこの変数を有効にすることはお勧めしません。代わりに[非トランザクションDML](/non-transactional-dml.md)を使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: 行
-   この値が`0`より大きい場合、TiDB は`INSERT`などのステートメントを小さなトランザクションにバッチコミットします。これによりメモリ使用量が削減され、一括変更によって`txn-total-size-limit`に達しないようにすることができます。
-   ACID準拠を実現するのは値`0`のみです。これを他の値に設定すると、TiDB の原子性と分離性の保証が破られます。
-   この変数を機能させるには、 `tidb_enable_batch_dml`と、 `tidb_batch_insert`および`tidb_batch_delete`の少なくとも 1 つを有効にする必要があります。

> **注記：**
>
> v7.0.0 以降、 `tidb_dml_batch_size` [`LOAD DATA`ステートメント](/sql-statements/sql-statement-load-data.md)には適用されなくなりました。

### tidb_enable_1pc<span class="version-mark">バージョン5.0の新機能</span> {#tidb-enable-1pc-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、1 つのリージョンにのみ影響するトランザクションに対して 1 フェーズ コミット機能を有効にするかどうかを指定するために使用されます。よく使用される 2 フェーズ コミットと比較して、1 フェーズ コミットはトランザクション コミットのレイテンシーを大幅に削減し、スループットを向上させることができます。

> **注記：**
>
> -   デフォルト値`ON`は新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   TiDB Binlogを有効にしている場合、この変数を有効にしてもパフォーマンスは向上しません。パフォーマンスを向上させるには、代わりに[ティCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)使用することをお勧めします。
> -   このパラメータを有効にすると、1 フェーズ コミットがトランザクション コミットのオプション モードになるだけです。実際、トランザクション コミットの最適なモードは TiDB によって決定されます。

### tidb_enable_analyze_snapshot <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-analyze-snapshot-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `ANALYZE`実行するときに履歴データを読み取るか、最新のデータを読み取るかを制御します。この変数が`ON`に設定されている場合、 `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ります。この変数が`OFF`に設定されている場合、 `ANALYZE`最新のデータを読み取ります。
-   v5.2 より前は、 `ANALYZE`最新のデータを読み取ります。v5.2 から v6.1 までは、 `ANALYZE`で`ANALYZE`の時点で利用可能な履歴データを読み取ります。

> **警告：**
>
> `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取る場合、履歴データがガベージコレクションされるため、 `AUTO ANALYZE`の長い期間によって`GC life time is shorter than transaction duration`エラーが発生する可能性があります。

### tidb_enable_async_commit <span class="version-mark">v5.0 の新</span>機能 {#tidb-enable-async-commit-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、2 フェーズ トランザクション コミットの 2 番目のフェーズをバックグラウンドで非同期に実行するために、非同期コミット機能を有効にするかどうかを制御します。この機能を有効にすると、トランザクション コミットのレイテンシーを短縮できます。

> **注記：**
>
> -   デフォルト値`ON`は新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   TiDB Binlogを有効にしている場合、この変数を有効にしてもパフォーマンスは向上しません。パフォーマンスを向上させるには、代わりに[ティCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)使用することをお勧めします。
> -   このパラメータを有効にすると、非同期コミットがトランザクション コミットのオプション モードになるだけです。実際、トランザクション コミットの最も適切なモードは TiDB によって決定されます。

### tidb_enable_auto_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-auto-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB がバックグラウンド操作としてテーブル統計を自動的に更新するかどうかを決定します。
-   この設定は以前は`tidb.toml`オプション ( `performance.run-auto-analyze` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_enable_auto_increment_in_generated {#tidb-enable-auto-increment-in-generated}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、生成された列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定するために使用されます。

### tidb_enable_batch_dml {#tidb-enable-batch-dml}

> **警告：**
>
> この変数は、非推奨の batch-dml 機能に関連付けられており、データの破損を引き起こす可能性があります。したがって、batch-dml に対してこの変数を有効にすることはお勧めしません。代わりに[非トランザクションDML](/non-transactional-dml.md)を使用してください。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨の batch-dml 機能を有効にするかどうかを制御します。この機能を有効にすると、特定のステートメントが複数のトランザクションに分割される可能性があります。これは非アトミックであり、注意して使用する必要があります。batch-dml を使用する場合は、操作対象のデータに対して同時操作が行われていないことを確認する必要があります。この機能を動作させるには、 `tidb_batch_dml_size`に正の値を指定し、 `tidb_batch_insert`と`tidb_batch_delete`の少なくとも 1 つを有効にする必要があります。

### tidb_enable_cascades_planner {#tidb-enable-cascades-planner}

> **警告：**
>
> 現在、カスケード プランナーは実験的機能です。本番環境での使用はお勧めしません。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、カスケード プランナーを有効にするかどうかを制御するために使用されます。

### tidb_enable_check_constraint <span class="version-mark">v7.2.0 の新</span>機能 {#tidb-enable-check-constraint-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [`CHECK`制約](/constraints.md#check)機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_chunk_rpc <span class="version-mark">v4.0 の新</span>機能 {#tidb-enable-chunk-rpc-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサーで`Chunk`データ エンコーディング形式を有効にするかどうかを制御するために使用されます。

### tidb_enable_clustered_index <span class="version-mark">v5.0 の新</span>機能 {#tidb-enable-clustered-index-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `ON`
-   可能`ON` `INT_ONLY` : `OFF`
-   この変数は、デフォルトで主キーを[クラスター化インデックス](/clustered-indexes.md)として作成するかどうかを制御するために使用されます。ここでの「デフォルト」とは、ステートメントでキーワード`CLUSTERED` / `NONCLUSTERED`が明示的に指定されていないことを意味します。サポートされている値は`OFF` 、 `ON` 、および`INT_ONLY`です。
    -   `OFF` 、主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
    -   `ON` 、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
    -   `INT_ONLY` 、動作が構成項目`alter-primary-key`によって制御されることを示します。 `alter-primary-key`を`true`に設定すると、すべての主キーはデフォルトで非クラスター化インデックスとして作成されます。 `false`に設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

### tidb_enable_ddl <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-enable-ddl-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   可能な値: `OFF` 、 `ON`
-   この変数は、対応する TiDB インスタンスが DDL 所有者になれるかどうかを制御します。現在の TiDB クラスターに TiDB インスタンスが 1 つしかない場合は、それが DDL 所有者になることを防ぐことはできません。つまり、これを`OFF`に設定することはできません。

### tidb_enable_collect_execution_info {#tidb-enable-collect-execution-info}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、各演算子の実行情報をスロー クエリ ログに記録するかどうかを制御します。

### tidb_enable_column_tracking <span class="version-mark">v5.4.0 の新</span>機能 {#tidb-enable-column-tracking-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> 現在、 `PREDICATE COLUMNS`の統計収集は実験的機能です。本番環境での使用はお勧めしません。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB が`PREDICATE COLUMNS`収集できるようにするかどうかを制御します。収集を有効にした後で無効にすると、以前に収集された`PREDICATE COLUMNS`の情報がクリアされます。詳細については、 [いくつかの列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)を参照してください。

### tidb_enable_enhanced_security {#tidb-enable-enhanced-security}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: `OFF`
-   この変数は、接続している TiDBサーバーでSecurity拡張モード (SEM) が有効になっているかどうかを示します。値を変更するには、TiDBサーバー構成ファイルの値`enable-sem`を変更し、TiDBサーバーを再起動する必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`
-   この変数は読み取り専用です。TiDB TiDB Cloudの場合、Security拡張モード (SEM) はデフォルトで有効になっています。

</CustomContent>

-   SEM は、 [セキュリティ強化Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux)などのシステムの設計にヒントを得ています。SEM では、MySQL `SUPER`権限を持つユーザーの権限が制限され、代わりに`RESTRICTED`権限を付与する必要があります。これらのきめ細かい権限には、次のものが含まれます。
    -   `RESTRICTED_TABLES_ADMIN` : `mysql`のスキーマのシステム テーブルにデータを書き込み、 `information_schema`テーブルの機密列を表示する機能。
    -   `RESTRICTED_STATUS_ADMIN` : コマンド`SHOW STATUS`内の機密変数を確認する機能。
    -   `RESTRICTED_VARIABLES_ADMIN` : `SHOW [GLOBAL] VARIABLES`および`SET`の機密変数を表示および設定する機能。
    -   `RESTRICTED_USER_ADMIN` : 他のユーザーがユーザー アカウントを変更したり削除したりすることを防ぐ機能。

### tidb_enable_exchange_partition {#tidb-enable-exchange-partition}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、デフォルトでは`exchange partitions with tables`が有効になっています。
-   この変数は v6.3.0 以降では非推奨です。その値はデフォルト値`ON`に固定されます。つまり、デフォルトでは`exchange partitions with tables`が有効になります。

### tidb_enable_extended_stats {#tidb-enable-extended-stats}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB がオプティマイザーをガイドするための拡張統計を収集できるかどうかを示します。詳細については、 [拡張統計入門](/extended-statistics.md)参照してください。

### tidb_enable_external_ts_read <span class="version-mark">v6.4.0 の新</span>機能 {#tidb-enable-external-ts-read-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数が`ON`に設定されている場合、TiDB は[`tidb_external_ts`](#tidb_external_ts-new-in-v640)で指定されたタイムスタンプを持つデータを読み取ります。

### tidb_external_ts <span class="version-mark">v6.4.0 の新機能</span> {#tidb-external-ts-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-new-in-v640) `ON`に設定すると、TiDB はこの変数で指定されたタイムスタンプを持つデータを読み取ります。

### tidb_enable_fast_analyze {#tidb-enable-fast-analyze}

> **警告：**
>
> v7.5.0 以降では、この変数は非推奨です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計`Fast Analyze`機能を有効にするかどうかを設定するために使用されます。
-   統計`Fast Analyze`機能を有効にすると、TiDB は統計として約 10,000 行のデータをランダムにサンプリングします。データが不均等に分散されていたり、データ サイズが小さい場合、統計の精度は低くなります。これにより、間違ったインデックスを選択するなど、最適でない実行プランが発生する可能性があります。通常の`Analyze`ステートメントの実行時間が許容できる場合は、 `Fast Analyze`機能を無効にすることをお勧めします。

### tidb_enable_fast_table_check <span class="version-mark">v7.2.0 の新</span>機能 {#tidb-enable-fast-table-check-span-class-version-mark-new-in-v7-2-0-span}

> **注記：**
>
> この変数は[多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)およびプレフィックス インデックスでは機能しません。

-   範囲: セッション | グローバル
-   クラスターに永続化: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、チェックサムベースのアプローチを使用してテーブル内のデータとインデックスの整合性を迅速にチェックするかどうかを制御するために使用されます。デフォルト値`ON` 、この機能がデフォルトで有効になっていることを意味します。
-   この変数を有効にすると、TiDB は[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントをより高速に実行できます。

### tidb_enable_foreign_key <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-enable-foreign-key-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: v6.6.0 より前では、デフォルト値は`OFF`です。v6.6.0 以降では、デフォルト値は`ON`です。
-   この変数は、 `FOREIGN KEY`機能を有効にするかどうかを制御します。

### tidb_enable_gc_aware_memory_track {#tidb-enable-gc-aware-memory-track}

> **警告：**
>
> この変数は、TiDB のデバッグ用の内部変数です。将来のリリースで削除される可能性があります。この変数を設定**しないでください**。

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、GC 対応メモリトラックを有効にするかどうかを制御します。

### tidb_enable_non_prepared_plan_cache {#tidb-enable-non-prepared-plan-cache}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。
-   この機能を有効にすると、追加のメモリと CPU オーバーヘッドが発生する可能性があり、すべての状況に適しているとは限りません。実際のシナリオに応じて、この機能を有効にするかどうかを判断してください。

### tidb_enable_non_prepared_plan_cache_for_dml <span class="version-mark">v7.1.0 の新機能</span> {#tidb-enable-non-prepared-plan-cache-for-dml-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> DML ステートメントの準備されていない実行プラン キャッシュは実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF` 。
-   この変数は、DML ステートメントに対して[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。

### tidb_enable_gogc_tuner <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-gogc-tuner-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、GOGC チューナーを有効にするかどうかを制御します。

### 履歴統計を有効にする {#tidb-enable-historical-stats}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`から`ON`に変更され、履歴統計がデフォルトで有効になっていることを意味します。

### tidb_enable_historical_stats_for_capture {#tidb-enable-historical-stats-for-capture}

> **警告：**
>
> この変数によって制御される機能は、現在の TiDB バージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CAPTURE`で取得された情報にデフォルトで履歴統計が含まれるかどうかを制御します。デフォルト値`OFF` 、履歴統計がデフォルトで含まれないことを意味します。

### tidb_enable_index_merge <span class="version-mark">v4.0 の新</span>機能 {#tidb-enable-index-merge-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> -   TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードすると、実行プランの変更によるパフォーマンスの低下を防ぐため、この変数はデフォルトで無効になります。
>
> -   TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードした後も、この変数はアップグレード前の設定のままになります。
>
> -   v5.4.0 以降、新しくデプロイされた TiDB クラスターでは、この変数はデフォルトで有効になっています。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックス マージ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_index_merge_join {#tidb-enable-index-merge-join}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `IndexMergeJoin`演算子を有効にするかどうかを指定します。
-   この変数は TiDB の内部操作にのみ使用されます。調整することは**お勧めしません**。調整すると、データの正確性が影響を受ける可能性があります。

### tidb_enable_legacy_instance_scope <span class="version-mark">v6.0.0 の新機能</span> {#tidb-enable-legacy-instance-scope-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `SET SESSION`および`SET GLOBAL`構文を使用して`INSTANCE`スコープの変数を設定することを許可します。
-   このオプションは、TiDB の以前のバージョンとの互換性を保つためにデフォルトで有効になっています。

### tidb_enable_list_partition <span class="version-mark">v5.0 の新</span>機能 {#tidb-enable-list-partition-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `LIST (COLUMNS) TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。

### tidb_enable_local_txn {#tidb-enable-local-txn}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は未リリースの機能に使用されます。**変数値を変更しないでください**。

### tidb_enable_metadata_lock <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-metadata-lock-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [メタデータロック](/metadata-lock.md)機能を有効にするかどうかを設定するために使用されます。この変数を設定するときは、クラスター内で実行中の DDL ステートメントがないことを確認する必要があります。そうでない場合、データが不正確または不整合になる可能性があります。

### tidb_enable_mutation_checker <span class="version-mark">v6.0.0 の新</span>機能 {#tidb-enable-mutation-checker-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB ミューテーション チェッカーを有効にするかどうかを制御するために使用します。これは、DML ステートメントの実行中にデータとインデックス間の一貫性をチェックするために使用されるツールです。チェッカーがステートメントに対してエラーを返すと、TiDB はステートメントの実行をロールバックします。この変数を有効にすると、CPU 使用率がわずかに増加します。詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。
-   v6.0.0 以降のバージョンの新しいクラスターの場合、デフォルト値は`ON`です。v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_enable_new_cost_interface <span class="version-mark">v6.2.0 の新</span>機能 {#tidb-enable-new-cost-interface-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB v6.2.0 は、以前のコスト モデルの実装をリファクタリングします。この変数は、リファクタリングされたコスト モデルの実装を有効にするかどうかを制御します。
-   リファクタリングされたコスト モデルでは以前と同じコスト式が使用され、プランの決定は変更されないため、この変数はデフォルトで有効になっています。
-   クラスターが v6.1 から v6.2 にアップグレードされた場合、この変数は`OFF`ままなので、手動で有効にすることをお勧めします。クラスターが v6.1 より前のバージョンからアップグレードされた場合、この変数はデフォルトで`ON`に設定されます。

### tidb_enable_new_only_full_group_by_check <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-enable-new-only-full-group-by-check-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB が`ONLY_FULL_GROUP_BY`チェックを実行するときの動作を制御します。 `ONLY_FULL_GROUP_BY`の詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)を参照してください。 v6.1.0 では、TiDB はこのチェックをより厳格かつ正確に処理します。
-   バージョンのアップグレードによって発生する可能性のある互換性の問題を回避するために、この変数のデフォルト値は v6.1.0 では`OFF`なっています。

### tidb_enable_noop_functions <span class="version-mark">v4.0 の新</span>機能 {#tidb-enable-noop-functions-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   可能`ON` `WARN` : `OFF`
-   デフォルトでは、まだ実装されていない機能の構文を使用しようとすると、TiDB はエラーを返します。変数値が`ON`に設定されている場合、TiDB はそのような利用できない機能のケースを黙って無視します。これは、SQL コードを変更できない場合に役立ちます。
-   `noop`関数を有効にすると、次の動作が制御されます。
    -   `LOCK IN SHARE MODE`構文
    -   `SQL_CALC_FOUND_ROWS`構文
    -   `START TRANSACTION READ ONLY`と`SET TRANSACTION READ ONLY`構文
    -   `tx_read_only` `super_read_only` `read_only` `sql_auto_is_null` `transaction_read_only` `offline_mode`
    -   `GROUP BY <expr> ASC|DESC`構文

> **警告：**
>
> 安全であると考えられるのは、デフォルト値の`OFF`のみです。3 に設定する`tidb_enable_noop_functions=1` 、TiDB がエラーを出さずに特定の構文を無視することを許可するため、アプリケーションで予期しない動作が発生する可能性があります。たとえば、構文`START TRANSACTION READ ONLY`は許可されますが、トランザクションは読み取り/書き込みモードのままになります。

### tidb_enable_noop_variables <span class="version-mark">v6.2.0 の新</span>機能 {#tidb-enable-noop-variables-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   変数値を`OFF`に設定すると、TiDB は次のように動作します。
    -   `SET`使用して`noop`変数を設定すると、TiDB は`"setting *variable_name* has no effect in TiDB"`警告を返します。
    -   `SHOW [SESSION | GLOBAL] VARIABLES`の結果には`noop`変数は含まれません。
    -   `SELECT`使用して`noop`変数を読み取ると、TiDB は`"variable *variable_name* has no effect in TiDB"`警告を返します。
-   TiDB インスタンスが`noop`変数を設定して読み取ったかどうかを確認するには、 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;`ステートメントを使用できます。

### tidb_enable_null_aware_anti_join <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-enable-null-aware-anti-join-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: v7.0.0 より前では、デフォルト値は`OFF`です。v7.0.0 以降では、デフォルト値は`ON`です。
-   タイプ: ブール値
-   この変数は、特殊なセット演算子`NOT IN`と`!= ALL`によって導かれるサブクエリによって ANTI JOIN が生成される場合に、TiDB が Null Aware Hash Join を適用するかどうかを制御します。
-   以前のバージョンから v7.0.0 以降のクラスターにアップグレードすると、この機能は自動的に有効になり、この変数は`ON`に設定されます。

### tidb_enable_outer_join_reorder <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-enable-outer-join-reorder-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   v6.1.0 以降、TiDB の[結合したテーブルの再配置](/join-reorder.md)アルゴリズムは Outer Join をサポートしています。この変数は、TiDB が Join Reorder の Outer Join のサポートを有効にするかどうかを制御します。
-   クラスターが以前のバージョンの TiDB からアップグレードされる場合は、次の点に注意してください。

    -   アップグレード前の TiDB バージョンが v6.1.0 より前の場合、アップグレード後のこの変数のデフォルト値は`ON`なります。
    -   アップグレード前の TiDB バージョンが v6.1.0 以降の場合、アップグレード後の変数のデフォルト値はアップグレード前の値に従います。

### <code>tidb_enable_inl_join_inner_multi_pattern</code> <span class="version-mark">v7.0.0 の新</span>機能 {#code-tidb-enable-inl-join-inner-multi-pattern-code-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、内部テーブルに`Selection`または`Projection`演算子がある場合に、インデックス結合がサポートされるかどうかを制御します。デフォルト値`OFF` 、このシナリオではインデックス結合がサポートされないことを意味します。

### tidb_enable_ordered_result_mode {#tidb-enable-ordered-result-mode}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   最終出力結果を自動的にソートするかどうかを指定します。
-   たとえば、この変数を有効にすると、TiDB は`SELECT a, MAX(b) FROM t GROUP BY a` `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`として処理します。

### tidb_enable_paging <span class="version-mark">v5.4.0 の新</span>機能 {#tidb-enable-paging-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサ要求を送信するためにページング方式を使用するかどうかを制御します。TiDB バージョン [v5.4.0、v6.2.0) の場合、この変数は`IndexLookup`演算子にのみ有効です。v6.2.0 以降の場合、この変数はグローバルに適用されます。v6.4.0 以降、この変数のデフォルト値は`OFF`から`ON`に変更されます。
-   ユーザーシナリオ:

    -   すべての OLTP シナリオでは、ページング方式を使用することをお勧めします。
    -   `IndexLookup`と`Limit`を使用し、 `Limit`を`IndexScan`にプッシュダウンできない読み取りクエリの場合、読み取りクエリのレイテンシーが高くなり、 TiKV `Unified read pool CPU`の使用率が高くなる可能性があります。このような場合、 `Limit`演算子は少量のデータ セットのみを必要とするため、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)を`ON`に設定すると、 TiDB が処理するデータが少なくなり、クエリのレイテンシーとリソース消費が削減されます。
    -   [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用したデータのエクスポートや完全なテーブル スキャンなどのシナリオでは、ページングを有効にすると、TiDB プロセスのメモリ消費を効果的に削減できます。

> **注記：**
>
> TiFlashの代わりに TiKV がstorageエンジンとして使用される OLAP シナリオでは、ページングを有効にすると、場合によってはパフォーマンスが低下する可能性があります。低下が発生した場合は、この変数を使用してページングを無効にするか、 [`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-new-in-v620)および[`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-new-in-v630)変数を使用してページング サイズの行の範囲を調整することを検討してください。

### tidb_enable_parallel_apply <span class="version-mark">v5.0 の新</span>機能 {#tidb-enable-parallel-apply-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `Apply`演算子の`Apply`実行を有効にするかどうかを制御します。同時実行の数は`tidb_executor_concurrency`変数によって制御されます。5 演算子は相関サブクエリを処理し、デフォルトでは同時実行がないため、実行速度は遅くなります。この変数値を`1`に設定すると、同時実行が増加し、実行速度が向上します。現在、 `Apply`の同時実行はデフォルトで無効になっています。

### tidb_enable_pipelined_window_function パイプラインウィンドウ関数を有効にする {#tidb-enable-pipelined-window-function}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数にパイプライン実行アルゴリズムを使用するかどうかを指定します。

### tidb_enable_plan_cache_for_param_limit <span class="version-mark">v6.6.0 の新</span>機能 {#tidb-enable-plan-cache-for-param-limit-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュ が、変数を`LIMIT`パラメータ ( `LIMIT ?` ) として持つ実行プランをキャッシュするかどうかを制御します。デフォルト値は`ON`で、 プリペアドプランキャッシュ がそのような実行プランのキャッシュをサポートすることを意味します。Prepared プリペアドプランキャッシュ は、 10000 を超える変数を持つ実行プランのキャッシュをサポートしないことに注意してください。

### tidb_enable_plan_cache_for_subquery <span class="version-mark">v7.0.0 の新</span>機能 {#tidb-enable-plan-cache-for-subquery-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュキャッシュがサブクエリを含むクエリをキャッシュするかどうかを制御します。

### tidb_enable_plan_replayer_capture {#tidb-enable-plan-replayer-capture}

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CAPTURE`機能を有効にするかどうかを制御します。デフォルト値`OFF` 、 `PLAN REPLAYER CAPTURE`機能を無効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`PLAN REPLAYER CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)を有効にするかどうかを制御します。デフォルト値`ON` `PLAN REPLAYER CAPTURE`機能を有効にすることを意味します。

</CustomContent>

### tidb_enable_plan_replayer_continuous_capture <span class="version-mark">v7.0.0 の新</span>機能 {#tidb-enable-plan-replayer-continuous-capture-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CONTINUOUS CAPTURE`機能を有効にするかどうかを制御します。デフォルト値`OFF` 、機能を無効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [`PLAN REPLAYER CONTINUOUS CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)を有効にするかどうかを制御します。デフォルト値`OFF` 、機能が無効であることを意味します。

</CustomContent>

### tidb_enable_prepared_plan_cache <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-enable-prepared-plan-cache-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   [プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)有効にするかどうかを決定します。有効にすると、 `Prepare`と`Execute`の実行プランがキャッシュされ、以降の実行では実行プランの最適化がスキップされ、パフォーマンスが向上します。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">v6.4.0 の新</span>機能 {#tidb-enable-prepared-plan-cache-memory-monitor-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュにキャッシュされた実行プランによって消費されるメモリをカウントするかどうかを制御します。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)参照してください。

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">v5.3.0 の新機能</span> {#tidb-enable-pseudo-for-outdated-stats-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計が古くなった場合にテーブルの統計を使用する際のオプティマイザの動作を制御します。

<CustomContent platform="tidb">

-   オプティマイザは、次のようにしてテーブルの統計が古くなっているかどうかを判断します。統計を取得するためにテーブルで最後に`ANALYZE`実行されて以降、テーブル行の 80% が変更された場合 (変更された行数を合計行数で割った値)、オプティマイザはこのテーブルの統計が古くなっていると判断します。この比率は、 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)構成を使用して変更できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   オプティマイザは、次のようにしてテーブルの統計が古くなっているかどうかを判断します。統計を取得するためにテーブルで最後に`ANALYZE`実行されて以降、テーブル行の 80% が変更されている場合 (変更された行数を合計行数で割った値)、オプティマイザはこのテーブルの統計が古くなっていると判断します。

</CustomContent>

-   デフォルトでは (変数値`OFF` )、テーブルの統計が古くなった場合でも、オプティマイザはテーブルの統計を使用し続けます。変数値を`ON`に設定すると、オプティマイザは、合計行数を除いてテーブルの統計が信頼できないと判断します。次に、オプティマイザは疑似統計を使用します。
-   テーブル上のデータが頻繁に変更され、そのテーブルに対して`ANALYZE`時間内に実行されない場合、実行プランを安定させるために、変数値を`OFF`に設定することをお勧めします。

### tidb_enable_rate_limit_action {#tidb-enable-rate-limit-action}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、データを読み取る演算子の動的メモリ制御機能を有効にするかどうかを制御します。デフォルトでは、この演算子は、データを読み取るために許可される最大数のスレッドを有効にします。単一の SQL ステートメントのメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超えると、データを読み取る演算子は[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)つのスレッドを停止します。

<CustomContent platform="tidb">

-   データを読み取る演算子に残っているスレッドが 1 つだけであり、単一の SQL ステートメントのメモリ使用量が継続的に[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超える場合、この SQL ステートメントは[ディスクへのデータの流出](/system-variables.md#tidb_enable_tmp_storage_on_oom)などの他のメモリ制御動作をトリガーします。
-   この変数は、SQL ステートメントがデータを読み取るだけの場合に、メモリ使用量を効果的に制御します。コンピューティング操作 (結合操作や集計操作など) が必要な場合は、メモリ使用量が`tidb_mem_quota_query`によって制御されない可能性があり、OOM のリスクが高まります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   データを読み取る演算子に残っているスレッドが 1 つだけであり、単一の SQL ステートメントのメモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超え続ける場合、この SQL ステートメントは、データをディスクに書き出すなどの他のメモリ制御動作をトリガーします。

</CustomContent>

### tidb_enable_resource_control <span class="version-mark">v6.6.0 の新</span>機能 {#tidb-enable-resource-control-span-class-version-mark-new-in-v6-6-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は[リソース制御機能](/tidb-resource-control.md)のスイッチです。この変数を`ON`に設定すると、TiDB クラスターはリソース グループに基づいてアプリケーション リソースを分離できます。

### tidb_enable_reuse_chunk <span class="version-mark">v6.4.0 の新</span>機能 {#tidb-enable-reuse-chunk-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   値`ON`オプション: `OFF`
-   この変数は、TiDB がチャンク オブジェクト キャッシュを有効にするかどうかを制御します。値が`ON`の場合、TiDB はキャッシュされたチャンク オブジェクトを優先的に使用し、要求されたオブジェクトがキャッシュにない場合にのみシステムから要求します。値が`OFF`の場合、TiDB はシステムからチャンク オブジェクトを直接要求します。

### 遅いログを有効にする {#tidb-enable-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_tmp_storage_on_oom {#tidb-enable-tmp-storage-on-oom}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   値`ON`オプション: `OFF`
-   単一の SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部の演算子の一時storageを有効にするかどうかを制御します。
-   v6.3.0 より前では、TiDB 構成項目`oom-use-tmp-storage`を使用してこの機能を有効または無効にできます。クラスターを v6.3.0 以降のバージョンにアップグレードすると、TiDB クラスターは自動的に値`oom-use-tmp-storage`を使用してこの変数を初期化します。その後、値`oom-use-tmp-storage`を変更しても有効になり**ません**。

### tidb_enable_stmt_summary <span class="version-mark">v3.0.4 の新</span>機能 {#tidb-enable-stmt-summary-span-class-version-mark-new-in-v3-0-4-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ステートメント サマリー機能を有効にするかどうかを制御するために使用されます。有効にすると、時間消費などの SQL 実行情報が`information_schema.STATEMENTS_SUMMARY`システム テーブルに記録され、SQL パフォーマンスの問題を特定してトラブルシューティングできるようになります。

### tidb_enable_strict_double_type_check <span class="version-mark">v5.0 の新機能</span> {#tidb-enable-strict-double-type-check-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、タイプ`DOUBLE`の無効な定義でテーブルを作成できるかどうかを制御するために使用されます。この設定は、タイプの検証がそれほど厳格ではなかった以前のバージョンの TiDB からのアップグレード パスを提供することを目的としています。
-   デフォルト値`ON`は MySQL と互換性があります。

たとえば、浮動小数点型の精度は保証されていないため、型`DOUBLE(10)`は無効とみなされます。 `tidb_enable_strict_double_type_check`を`OFF`に変更すると、次のテーブルが作成されます。

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
> MySQL では`FLOAT`型の精度が許可されているため、この設定は型`DOUBLE`にのみ適用されます。この動作は MySQL 8.0.17 以降では非推奨であり、 `FLOAT`または`DOUBLE`型の精度を指定することは推奨されません。

### tidb_enable_table_partition {#tidb-enable-table-partition}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `ON`
-   可能`ON` `AUTO` : `OFF`
-   この変数は、 `TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。
    -   `ON` 、範囲パーティション分割、ハッシュ パーティション分割、および 1 つの列による範囲列パーティション分割を有効にすることを示します。
    -   `AUTO` `ON`と同じように関数。
    -   `OFF` `TABLE PARTITION`機能を無効にすることを示します。この場合、パーティション テーブルを作成する構文は実行できますが、作成されるテーブルはパーティション化されたテーブルではありません。

### tidb_enable_telemetry <span class="version-mark">v4.0.2 の新</span>機能 {#tidb-enable-telemetry-span-class-version-mark-new-in-v4-0-2-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、TiDB でのテレメトリ収集を有効にするかどうかを動的に制御するために使用されます。現在のバージョンでは、テレメトリはデフォルトで無効になっています。すべての TiDB インスタンスで[`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) TiDB 構成項目が`false`に設定されている場合、テレメトリ収集は常に無効になり、このシステム変数は有効になりません。詳細については、 [テレメトリー](/telemetry.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB でのテレメトリ収集を有効にするかどうかを動的に制御するために使用されます。

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-enable-tiflash-read-for-write-stmt-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `INSERT` 、 `DELETE` 、および`UPDATE`を含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできるかどうかを制御します。例:

    -   `INSERT INTO SELECT`ステートメントに`SELECT`クエリ (一般的な使用シナリオ: [TiFlashクエリ結果の実現](/tiflash/tiflash-results-materialization.md) )
    -   `UPDATE`文と`DELETE`文の`WHERE`条件フィルタリング
-   v7.1.0 以降、この変数は非推奨です。 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)場合、オプティマイザーは、 [SQL モード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定します。TiDB では、現在のセッションの[SQL モード](/sql-mode.md)が厳密でない場合にのみ、 `INSERT` 、 `DELETE` 、および`UPDATE` ( `INSERT INTO SELECT`など) を含む SQL ステートメントの読み取り操作をTiFlashにプッシュダウンできることに注意してください。つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`と`STRICT_ALL_TABLES`含まれません。

### tidb_enable_top_sql <span class="version-mark">v5.4.0 の新</span>機能 {#tidb-enable-top-sql-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、 [Top SQL](/dashboard/top-sql.md)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

### tidb_enable_tso_follower_proxy <span class="version-mark">v5.3.0 の新</span>機能 {#tidb-enable-tso-follower-proxy-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TSOFollowerプロキシ機能を有効にするために使用されます。値が`OFF`の場合、TiDB は PD リーダーからのみ TSO を取得します。この機能を有効にすると、TiDB はすべての PD ノードに要求を均等に送信し、TSO 要求を PD フォロワー経由で転送することで TSO を取得します。これにより、PD リーダーの CPU 負荷が軽減されます。
-   TSOFollowerプロキシを有効にするシナリオ:
    -   TSO 要求の負荷が高いため、PD リーダーの CPU がボトルネックになり、TSO RPC 要求のレイテンシーが高くなります。
    -   TiDB クラスターには多数の TiDB インスタンスがあり、値を[`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)に増やしても、TSO RPC 要求の高レイテンシーの問題を軽減することはできません。

> **注記：**
>
> PD リーダーの CPU 使用率のボトルネック以外の理由 (ネットワークの問題など) で TSO RPCレイテンシーが増加するとします。この場合、TSOFollowerプロキシを有効にすると、TiDB での実行レイテンシーが増加し、クラスターの QPS パフォーマンスに影響する可能性があります。

### tidb_enable_unsafe_substitute <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-enable-unsafe-substitute-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、式を生成された列に安全でない方法で置き換えるかどうかを制御します。デフォルト値は`OFF`で、安全でない置換はデフォルトで無効になっていることを意味します。詳細については、 [生成された列](/generated-columns.md)を参照してください。

### tidb_enable_vectorized_expression <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-vectorized-expression-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ベクトル化された実行を有効にするかどうかを制御するために使用されます。

### tidb_enable_window_function {#tidb-enable-window-function}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数のサポートを有効にするかどうかを制御するために使用されます。ウィンドウ関数では予約キーワードが使用される場合があることに注意してください。これにより、正常に実行できる SQL ステートメントが TiDB のアップグレード後に解析できなくなる可能性があります。この場合、 `tidb_enable_window_function`を`OFF`に設定できます。

### <code>tidb_enable_row_level_checksum</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-enable-row-level-checksum-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、 [単一行データの TiCDC データ整合性検証](/ticdc/ticdc-integrity-check.md)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [単一行データの TiCDC データ整合性検証](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

### tidb_enforce_mpp <span class="version-mark">v5.1 の新機能</span> {#tidb-enforce-mpp-span-class-version-mark-new-in-v5-1-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   このデフォルト値を変更するには、 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値を変更します。

</CustomContent>

-   オプティマイザのコスト見積もりを無視し、クエリ実行に TiFlash の MPP モードを強制的に使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF` 。MPP モードが強制的に使用されないことを意味します (デフォルト)。
    -   `1`または`ON`場合、コスト推定は無視され、MPP モードが強制的に使用されます。この設定は`tidb_allow_mpp=true`場合にのみ有効になることに注意してください。

MPP はTiFlashエンジンが提供する分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能で高スループットの SQL アルゴリズムを提供します。MPP モードの選択の詳細については、 [MPPモードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_evolve_plan_baselines <span class="version-mark">v4.0 の新</span>機能 {#tidb-evolve-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ベースライン進化機能を有効にするかどうかを制御するために使用されます。詳細な紹介や使用方法については、 [ベースライン進化](/sql-plan-management.md#baseline-evolution)参照してください。
-   ベースラインの進化がクラスターに与える影響を軽減するには、次の構成を使用します。
    -   各実行プランの最大実行時間を制限するには`tidb_evolve_plan_task_max_time`設定します。デフォルト値は 600 秒です。
    -   時間ウィンドウを制限するには、 `tidb_evolve_plan_task_start_time`と`tidb_evolve_plan_task_end_time`設定します。デフォルト値はそれぞれ`00:00 +0000`と`23:59 +0000`です。

### tidb_evolve_plan_task_end_time <span class="version-mark">v4.0 の新</span>機能 {#tidb-evolve-plan-task-end-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、1 日のベースライン進化の終了時刻を設定するために使用されます。

### tidb_evolve_plan_task_max_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-max-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `600`
-   範囲: `[-1, 9223372036854775807]`
-   単位: 秒
-   この変数は、ベースライン進化機能の各実行プランの最大実行時間を制限するために使用されます。

### tidb_evolve_plan_task_start_time <span class="version-mark">v4.0 の新</span>機能 {#tidb-evolve-plan-task-start-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、1 日のベースライン進化の開始時刻を設定するために使用されます。

### tidb_executor_concurrency <span class="version-mark">v5.0 の新</span>機能 {#tidb-executor-concurrency-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
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

`tidb_executor_concurrency` 、管理を容易にするために、次の既存のシステム変数が全体的に組み込まれています。

-   `tidb_index_lookup_concurrency`
-   `tidb_index_lookup_join_concurrency`
-   `tidb_hash_join_concurrency`
-   `tidb_hashagg_partial_concurrency`
-   `tidb_hashagg_final_concurrency`
-   `tidb_projection_concurrency`
-   `tidb_window_concurrency`

v5.0 以降では、上記のシステム変数を個別に変更することができます (非推奨の警告が返されます)。変更は対応する単一の演算子にのみ影響します。その後、 `tidb_executor_concurrency`使用して演算子の同時実行性を変更した場合、個別に変更された演算子は影響を受けません。 `tidb_executor_concurrency`を使用してすべての演算子の同時実行性を変更する場合は、上記のすべての変数の値を`-1`に設定できます。

以前のバージョンから v5.0 にアップグレードされたシステムの場合、上記の変数の値を変更していない場合 (つまり、 `tidb_hash_join_concurrency`値が`5`で、残りの値が`4`場合)、これらの変数によって以前に管理されていた演算子の同時実行性は、自動的に`tidb_executor_concurrency`によって管理されます。これらの変数のいずれかを変更した場合、対応する演算子の同時実行性は、変更された変数によって引き続き制御されます。

### tidb_expensive_query_time_threshold {#tidb-expensive-query-time-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `NO_PRIORITY`
-   `HIGH_PRIORITY` `LOW_PRIORITY` `DELAYED` : `NO_PRIORITY`
-   この変数は、TiDBサーバーで実行されるステートメントのデフォルトの優先度を変更するために使用されます。使用例としては、OLAP クエリを実行している特定のユーザーが、OLTP クエリを実行しているユーザーよりも低い優先度を受け取るようにすることが挙げられます。
-   デフォルト値`NO_PRIORITY` 、ステートメントの優先順位が強制的に変更されないことを意味します。

> **注記：**
>
> v6.6.0 以降、TiDB は[リソース管理](/tidb-resource-control.md)サポートします。この機能を使用すると、異なるリソース グループで異なる優先度の SQL ステートメントを実行できます。これらのリソース グループに適切なクォータと優先度を構成することで、異なる優先度の SQL ステートメントのスケジュール制御を向上させることができます。リソース制御を有効にすると、ステートメントの優先度は無効になります。異なる SQL ステートメントのリソース使用を管理するには、 [リソース管理](/tidb-resource-control.md)使用することをお勧めします。

### tidb_gc_concurrency <span class="version-mark">v5.0 の新</span>機能 {#tidb-gc-concurrency-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   GC の[ロックを解決する](/garbage-collection-overview.md#resolve-locks)ステップ目のスレッド数を指定します。値が`-1`の場合、TiDB は使用するガベージコレクションスレッドの数を自動的に決定します。

### tidb_gc_enable <span class="version-mark">v5.0 の新</span>機能 {#tidb-gc-enable-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiKV のガベージコレクションを有効にします。ガベージコレクションを無効にすると、古いバージョンの行が削除されなくなるため、システムのパフォーマンスが低下します。

### tidb_gc_life_time <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-life-time-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   各 GC でデータが保持される時間制限 (Go Duration 形式)。GC が発生すると、現在の時刻からこの値を引いた値が安全ポイントになります。

> **注記：**
>
> -   頻繁に更新されるシナリオでは、 `tidb_gc_life_time`に大きな値 (日数または月数) を指定すると、次のような潜在的な問題が発生する可能性があります。
>     -   より大きなstorageの使用
>     -   大量の履歴データは、特に`select count(*) from t`ような範囲クエリの場合、ある程度パフォーマンスに影響を与える可能性があります。
> -   `tidb_gc_life_time`より長く実行されているトランザクションがある場合、GC 中、このトランザクションが実行を継続できるように`start_ts`以降のデータが保持されます。たとえば、 `tidb_gc_life_time`が 10 分に設定されている場合、実行中のすべてのトランザクションのうち、最も早く開始されたトランザクションが 15 分間実行されているため、GC は最近の 15 分間のデータを保持します。

### tidb_gc_max_wait_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-gc-max-wait-time-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `86400`
-   範囲: `[600, 31536000]`
-   単位: 秒
-   この変数は、アクティブなトランザクションが GC セーフ ポイントをブロックする最大時間を設定するために使用されます。GC の各時間中、セーフ ポイントはデフォルトで進行中のトランザクションの開始時間を超えません。アクティブなトランザクションの実行時間がこの変数値を超えない場合、実行時間がこの値を超えるまで GC セーフ ポイントはブロックされます。

### tidb_gc_run_interval <span class="version-mark">v5.0 の新</span>機能 {#tidb-gc-run-interval-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   GC間隔をGo Durationの形式で指定します。たとえば、 `"1h30m"`などです`"15m"`

### tidb_gc_scan_lock_mode <span class="version-mark">v5.0 の新</span>機能 {#tidb-gc-scan-lock-mode-span-class-version-mark-new-in-v5-0-span}

> **警告：**
>
> 現在、Green GC は実験的機能です。本番環境での使用はお勧めしません。

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `LEGACY`
-   可能な値: `PHYSICAL` 、 `LEGACY`
    -   `LEGACY` : 古いスキャン方法を使用します。つまり、Green GC を無効にします。
    -   `PHYSICAL` : 物理スキャン方式を使用します。つまり、Green GC を有効にします。

<CustomContent platform="tidb">

-   この変数は、GC のロック解決ステップでロックをスキャンする方法を指定します。変数値が`LEGACY`に設定されている場合、TiDB は領域ごとにロックをスキャンします。値`PHYSICAL`を使用すると、各 TiKV ノードがRaftレイヤーをバイパスしてデータを直接スキャンできるようになり、 [休止状態リージョン](/tikv-configuration-file.md#hibernate-regions)機能が有効な場合に GC がすべての領域を起動する影響を効果的に軽減できるため、ロック解決ステップでの実行速度が向上します。

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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb-cloud">

-   この変数は、すべての SQL ステートメントをログに記録するかどうかを設定するために使用されます。この機能はデフォルトでは無効になっています。問題を特定するときにすべての SQL ステートメントをトレースする必要がある場合は、この機能を有効にします。

</CustomContent>

<CustomContent platform="tidb">

-   この変数は、 [ログ](/tidb-configuration-file.md#logfile)内のすべての SQL 文を記録するかどうかを設定するために使用されます。この機能はデフォルトでは無効になっています。保守担当者が問題を見つけるときにすべての SQL 文をトレースする必要がある場合は、この機能を有効にすることができます。

-   ログ内のこの機能のすべてのレコードを表示するには、TiDB 構成項目[`log.level`](/tidb-configuration-file.md#level)を`"info"`または`"debug"`に設定し、文字列`"GENERAL_LOG"`をクエリする必要があります。次の情報が記録されます。
    -   `conn` : 現在のセッションの ID。
    -   `user` : 現在のセッションユーザー。
    -   `schemaVersion` : 現在のスキーマ バージョン。
    -   `txnStartTS` : 現在のトランザクションが開始されるタイムスタンプ。
    -   `forUpdateTS` :悲観的トランザクション モードでは、 `forUpdateTS` SQL 文の現在のタイムスタンプです。悲観的トランザクションで書き込み競合が発生すると、TiDB は現在実行中の SQL 文を再試行し、このタイムスタンプを更新します。再試行回数は[`max-retry-count`](/tidb-configuration-file.md#max-retry-count)で設定できます。楽観的トランザクション モデルでは、 `forUpdateTS` `txnStartTS`に相当します。
    -   `isReadConsistency` : 現在のトランザクション分離レベルが Read Committed (RC) であるかどうかを示します。
    -   `current_db` : 現在のデータベースの名前。
    -   `txn_mode` : トランザクション モード。値のオプションは`OPTIMISTIC`と`PESSIMISTIC`です。
    -   `sql` : 現在のクエリに対応する SQL ステートメント。

</CustomContent>

### tidb_非準備プランのキャッシュサイズ {#tidb-non-prepared-plan-cache-size}

> **警告：**
>
> v7.1.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は、 [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)でキャッシュできる実行プランの最大数を制御します。

### tidb_generate_binary_plan <span class="version-mark">v6.2.0 の新</span>機能 {#tidb-generate-binary-plan-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログとステートメントの概要にバイナリ エンコードされた実行プランを生成するかどうかを制御します。
-   この変数を`ON`に設定すると、TiDB ダッシュボードで視覚的な実行プランを表示できます。TiDB ダッシュボードでは、この変数を有効にした後に生成された実行プランのみが視覚的に表示されることに注意してください。
-   `SELECT tidb_decode_binary_plan('xxx...')`ステートメントを実行して、バイナリ プランから特定のプランを解析できます。

### tidb_gogc_tuner_max_value <span class="version-mark">v7.5.0 の新</span>機能 {#tidb-gogc-tuner-max-value-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `500`
-   範囲: `[10, 2147483647]`
-   この変数は、GOGC チューナーが調整できる GOGC の最大値を制御するために使用されます。

### tidb_gogc_tuner_min_value <span class="version-mark">v7.5.0 の新</span>機能 {#tidb-gogc-tuner-min-value-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[10, 2147483647]`
-   この変数は、GOGC チューナーが調整できる GOGC の最小値を制御するために使用されます。

### tidb_gogc_tuner_threshold <span class="version-mark">v6.4.0 の新機能</span> {#tidb-gogc-tuner-threshold-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `0.6`
-   範囲: `[0, 0.9)`
-   この変数は、GOGC をチューニングするための最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC Tuner は動作を停止します。

### tidb_guarantee_linearizability <span class="version-mark">v5.0 の新</span>機能 {#tidb-guarantee-linearizability-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、非同期コミットのコミット TS の計算方法を制御します。デフォルト (値`ON` ) では、2 フェーズ コミットは PDサーバーから新しい TS を要求し、その TS を使用して最終コミット TS を計算します。この状況では、すべての同時トランザクションの線形化可能性が保証されます。
-   この変数を`OFF`に設定すると、PDサーバーから TS を取得するプロセスがスキップされますが、因果一貫性のみが保証され、線形化可能性は保証されません。詳細については、ブログ投稿[非同期コミット、TiDB 5.0 のトランザクションコミットのアクセラレータ](https://en.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/)を参照してください。
-   因果一貫性のみが必要なシナリオでは、この変数を`OFF`に設定してパフォーマンスを向上させることができます。

### 新しい照合順序による tidb_hash_exchange {#tidb-hash-exchange-with-new-collation}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、新しい照合順序が有効になっているクラスターで MPP ハッシュ パーティション交換演算子が生成されるかどうかを制御します。1 `true`演算子を生成することを意味し、 `false`演算子を生成しないことを意味します。
-   この変数は TiDB の内部操作に使用されます。この変数を設定することは**お勧めしません**。

### tidb_hash_join_concurrency {#tidb-hash-join-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `hash join`アルゴリズムの同時実行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hashagg_final_concurrency {#tidb-hashagg-final-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `final`フェーズで同時実行`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメータが一意でない場合、 `HashAgg`同時に実行され、それぞれ`partial`フェーズと`final`フェーズの 2 つのフェーズで実行されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hashagg_部分的同時実行性 {#tidb-hashagg-partial-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `partial`フェーズで同時実行`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメータが一意でない場合、 `HashAgg`同時に実行され、それぞれ`partial`フェーズと`final`フェーズの 2 つのフェーズで実行されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_historical_stats_duration <span class="version-mark">v6.6.0 の新</span>機能 {#tidb-historical-stats-duration-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   スタイル: 期間
-   デフォルト値: `168h` 、7日間を意味します
-   この変数は、履歴統計がstorageに保持される期間を制御します。

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">v6.0.0 の新</span>機能 {#tidb-ignore-prepared-cache-close-stmt-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、プリペアドステートメントキャッシュを閉じるコマンドを無視するかどうかを設定するために使用されます。
-   この変数を`ON`に設定すると、バイナリプロトコルの`COM_STMT_CLOSE`コマンドとテキストプロトコルの[`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md)ステートメントは無視されます。詳細については、 [`COM_STMT_CLOSE`コマンドと`DEALLOCATE PREPARE`ステートメントを無視します。](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)を参照してください。

### tidb_index_join_batch_size {#tidb-index-join-batch-size}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `25000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup join`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_index_join_double_read_penalty_cost_rate <span class="version-mark">v6.6.0 の新</span>機能 {#tidb-index-join-double-read-penalty-cost-rate-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、インデックス結合の選択にペナルティ コストを適用するかどうかを決定し、これにより、オプティマイザがインデックス結合を選択する可能性が低くなり、ハッシュ結合や tiflash 結合などの代替結合方法を選択する可能性が高くなります。
-   インデックス結合を選択すると、多くのテーブル検索要求がトリガーされ、リソースが過剰に消費されます。この変数を使用すると、オプティマイザーがインデックス結合を選択する可能性を減らすことができます。
-   この変数は、 [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620)変数が`2`に設定されている場合にのみ有効になります。

### tidb_index_lookup_concurrency {#tidb-index-lookup-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
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
> v5.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup join`アルゴリズムの同時実行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_merge_intersection_concurrency <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-index-merge-intersection-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   この変数は、インデックス マージが実行する交差操作の最大同時実行性を設定します。これは、TiDB が動的プルーニング モードでパーティション テーブルにアクセスする場合にのみ有効です。実際の同時実行性は、 `tidb_index_merge_intersection_concurrency`とパーティションテーブルのパーティション数のうち小さい方の値になります。
-   デフォルト値`-1` 、値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_size {#tidb-index-lookup-size}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `20000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_index_serial_scan_concurrency {#tidb-index-serial-scan-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `serial scan`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_init_チャンクサイズ {#tidb-init-chunk-size}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `32`
-   範囲: `[1, 32]`
-   単位: 行
-   この変数は、実行プロセス中に最初のチャンクの行数を設定するために使用されます。チャンクの行数は、単一のクエリに必要なメモリ量に直接影響します。クエリ内のすべての列の合計幅とチャンクの行数を考慮すると、単一のチャンクに必要なメモリを大まかに見積もることができます。これをエグゼキュータの同時実行性と組み合わせると、単一のクエリに必要な合計メモリを大まかに見積もることができます。単一のチャンクの合計メモリは16 MiB を超えないようにすることをお勧めします。

### tidb_isolation_read_engines <span class="version-mark">v4.0 の新</span>機能 {#tidb-isolation-read-engines-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `tikv,tiflash,tidb`
-   この変数は、TiDB がデータを読み取るときに使用できるstorageエンジン リストを設定するために使用されます。

### tidb_last_ddl_info <span class="version-mark">v6.0.0 の新</span>機能 {#tidb-last-ddl-info-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   タイプ: 文字列
-   これは読み取り専用変数です。現在のセッション内の最後の DDL 操作の情報を取得するために TiDB で内部的に使用されます。
    -   &quot;query&quot;: 最後の DDL クエリ文字列。
    -   &quot;seq_num&quot;: 各 DDL 操作のシーケンス番号。DDL 操作の順序を識別するために使用されます。

### tidb_last_query_info <span class="version-mark">v4.0.14 の新</span>機能 {#tidb-last-query-info-span-class-version-mark-new-in-v4-0-14-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   これは読み取り専用変数です。これは、最後の DML ステートメントのトランザクション情報を照会するために TiDB で内部的に使用されます。情報には次のものが含まれます。
    -   `txn_scope` : トランザクションのスコープ。2 または`global` `local`なります。
    -   `start_ts` : トランザクションの開始タイムスタンプ。
    -   `for_update_ts` : 前回実行された DML ステートメントの`for_update_ts`これは、テストに使用される TiDB の内部用語です。通常、この情報は無視できます。
    -   `error` : エラー メッセージ (ある場合)。
    -   `ru_consumption` : ステートメントの実行に[ロシア](/tidb-resource-control.md#what-is-request-unit-ru)消費されました。

### tidb_last_txn_info <span class="version-mark">v4.0.9 の新機能</span> {#tidb-last-txn-info-span-class-version-mark-new-in-v4-0-9-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   この変数は、現在のセッション内の最後のトランザクション情報を取得するために使用されます。これは読み取り専用変数です。トランザクション情報には次のものが含まれます。
    -   トランザクションの範囲。
    -   TS の開始とコミット。
    -   トランザクション コミット モード。2 フェーズ、1 フェーズ、または非同期コミットのいずれかになります。
    -   非同期コミットまたは 1 フェーズ コミットから 2 フェーズ コミットへのトランザクション フォールバックの情報。
    -   エラーが発生しました。

### tidb_last_plan_replayer_token <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-last-plan-replayer-token-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   この変数は読み取り専用であり、現在のセッションの最後の`PLAN REPLAYER DUMP`の実行の結果を取得するために使用されます。

### tidb_load_based_replica_read_threshold <span class="version-mark">v7.0.0 の新機能</span> {#tidb-load-based-replica-read-threshold-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   タイプ: 文字列
-   この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定するために使用されます。リーダー ノードの推定キュー時間がしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。形式は、 `"100ms"`や`"1s"`などの時間間隔です。詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   タイプ: 文字列
-   この変数は、負荷ベースのレプリカ読み取りをトリガーするためのしきい値を設定するために使用されます。リーダー ノードの推定キュー時間がしきい値を超えると、TiDB はフォロワー ノードからのデータの読み取りを優先します。形式は、 `"100ms"`や`"1s"`などの時間間隔です。詳細については、 [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#scatter-read-hotspots)を参照してください。

</CustomContent>

### <code>tidb_lock_unchanged_keys</code> <span class="version-mark">v7.1.1 および v7.3.0 の新機能</span> {#code-tidb-lock-unchanged-keys-code-span-class-version-mark-new-in-v7-1-1-and-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、次のシナリオで特定のキーをロックするかどうかを制御するために使用されます。値が`ON`に設定されている場合、これらのキーはロックされます。値が`OFF`に設定されている場合、これらのキーはロックされません。
    -   `INSERT IGNORE`および`REPLACE`ステートメントに重複キーがあります。v6.1.6 より前では、これらのキーはロックされていませんでした。この問題は[＃42121](https://github.com/pingcap/tidb/issues/42121)で修正されました。
    -   キーの値が変更されていない場合の`UPDATE`ステートメント内の一意のキー。v6.5.2 より前では、これらのキーはロックされていませんでした。この問題は[＃36438](https://github.com/pingcap/tidb/issues/36438)で修正されました。
-   トランザクションの一貫性と合理性を維持するために、この値を変更することは推奨されません。TiDB のアップグレードにより、これら 2 つの修正により重大なパフォーマンスの問題が発生し、ロックなしの動作が許容できる場合 (前述の問題を参照)、この変数を`OFF`に設定できます。

### tidb_log_file_max_days <span class="version-mark">v5.3.0 の新</span>機能 {#tidb-log-file-max-days-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`

<CustomContent platform="tidb">

-   この変数は、現在の TiDB インスタンスでログが保持される最大日数を設定するために使用されます。この値は、構成ファイル内の[`max-days`](/tidb-configuration-file.md#max-days)構成の値にデフォルト設定されます。変数値の変更は、現在の TiDB インスタンスにのみ影響します。TiDB を再起動すると、変数値はリセットされ、構成値は影響を受けません。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、現在の TiDB インスタンスにログが保持される最大日数を設定するために使用されます。

</CustomContent>

### 低解像度tso {#tidb-low-resolution-tso}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、低精度 TSO 機能を有効にするかどうかを設定するために使用されます。この機能を有効にすると、新しいトランザクションは 2 秒ごとに更新されるタイムスタンプを使用してデータを読み取ります。
-   主な適用可能なシナリオは、古いデータの読み取りが許容される場合に、小さな読み取り専用トランザクションの TSO 取得のオーバーヘッドを削減することです。

### tidb_max_auto_analyze_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-auto-analyze-time-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `43200`
-   範囲: `[0, 2147483647]`
-   単位: 秒
-   この変数は、自動`ANALYZE`タスクの最大実行時間を指定するために使用されます。自動`ANALYZE`タスクの実行時間が指定された時間を超えると、タスクは終了します。この変数の値が`0`の場合、自動`ANALYZE`タスクの最大実行時間に制限はありません。

### tidb_max_bytes_before_tiflash_external_group_by <span class="version-mark">v7.0.0 の新機能</span> {#tidb-max-bytes-before-tiflash-external-group-by-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashのハッシュ集計演算子の最大メモリ使用量をバイト`GROUP BY`で指定するために使用されます。メモリ使用量が指定された値を超えると、 TiFlash はハッシュ集計演算子をトリガーしてディスクに書き出します。この変数の値が`-1`の場合、 TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、 TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量が無制限であることを意味します。つまり、 TiFlashハッシュ集計演算子は書き出しをトリガーしません。詳細については、 [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md)を参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、通常、集計は複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の集計演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目[`max_bytes_before_external_group_by`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて集計演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、通常、集計は複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の集計演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目`max_bytes_before_external_group_by`の値に基づいて集計演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_join <span class="version-mark">v7.0.0 の新</span>機能 {#tidb-max-bytes-before-tiflash-external-join-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashのハッシュ結合演算子の最大メモリ使用量をバイト`JOIN`で指定するために使用されます。メモリ使用量が指定された値を超えると、 TiFlash はハッシュ結合演算子をトリガーしてディスクにスピルします。この変数の値が`-1`の場合、 TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、 TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量が無制限であることを意味します。つまり、 TiFlashハッシュ結合演算子はスピルをトリガーしません。詳細については、 [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md)を参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、結合は通常、複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノードでの結合演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目[`max_bytes_before_external_join`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて結合演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、結合は通常、複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノードでの結合演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目`max_bytes_before_external_join`の値に基づいて結合演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_sort <span class="version-mark">v7.0.0 の新</span>機能 {#tidb-max-bytes-before-tiflash-external-sort-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashの TopN および Sort 演算子の最大メモリ使用量をバイト単位で指定するために使用されます。メモリ使用量が指定値を超えると、 TiFlash はTopN および Sort 演算子をトリガーしてディスクに書き出します。この変数の値が`-1`の場合、 TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、 TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量が無制限であることを意味します。つまり、 TiFlash TopN および Sort 演算子は書き出しをトリガーしません。詳細については、 [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md)を参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB クラスターに複数のTiFlashノードがある場合、TopN と Sort は通常、複数のTiFlashノードで分散して実行されます。この変数は、単一のTiFlashノード上の TopN および Sort 演算子の最大メモリ使用量を制御します。
> -   この変数が`-1`に設定されている場合、 TiFlash は独自の構成項目[`max_bytes_before_external_sort`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて、TopN 演算子と Sort 演算子の最大メモリ使用量を決定します。

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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[32, 2147483647]`
-   単位: 行
-   この変数は、実行プロセス中にチャンク内の最大行数を設定するために使用されます。設定値が大きすぎると、キャッシュの局所性の問題が発生する可能性があります。この変数の推奨値は 65536 以下です。チャンクの行数は、単一のクエリに必要なメモリ量に直接影響します。クエリ内のすべての列の合計幅とチャンクの行数を考慮することで、単一のチャンクに必要なメモリを大まかに見積もることができます。これをエグゼキュータの同時実行性と組み合わせることで、単一のクエリに必要な合計メモリを大まかに見積もることができます。単一のチャンクの合計メモリは16 MiB を超えないようにすることをお勧めします。クエリに大量のデータが含まれ、単一のチャンクではすべてのデータを処理できない場合、TiDB はそれを複数回処理し、チャンク サイズが[`tidb_init_chunk_size`](#tidb_init_chunk_size)から始まり、チャンク サイズが`tidb_max_chunk_size`に達するまで、処理の反復ごとにチャンク サイズを 2 倍にします。

### tidb_max_delta_schema_count <span class="version-mark">v2.1.18 および v3.0.5 の新機能</span> {#tidb-max-delta-schema-count-span-class-version-mark-new-in-v2-1-18-and-v3-0-5-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[100, 16384]`
-   この変数は、キャッシュできるスキーマ バージョン (対応するバージョン用に変更されたテーブル ID) の最大数を設定するために使用されます。値の範囲は 100 ～ 16384 です。

### tidb_max_paging_size <span class="version-mark">v6.3.0 の新</span>機能 {#tidb-max-paging-size-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `50000`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサ ページング要求プロセス中の最大行数を設定するために使用されます。この変数を小さすぎる値に設定すると、TiDB と TiKV 間の RPC カウントが増加し、大きすぎる値に設定すると、データのロードや完全なテーブル スキャンなどの場合にメモリ使用量が過剰になります。この変数のデフォルト値では、OLAP シナリオよりも OLTP シナリオでパフォーマンスが向上します。アプリケーションがstorageエンジンとして TiKV のみを使用する場合は、OLAP ワークロード クエリを実行するときにこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

### tidb_max_tiflash_threads <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-max-tiflash-threads-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、 TiFlash がリクエストを実行するための最大同時実行数を設定するために使用されます。デフォルト値は`-1`で、このシステム変数が無効であり、最大同時実行数はTiFlash構成`profiles.default.max_threads`の設定に依存することを示します。値が`0`の場合、最大スレッド数はTiFlashによって自動的に設定されます。

### tidb_mem_oom_action <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-mem-oom-action-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `CANCEL`
-   可能な値: `CANCEL` 、 `LOG`

<CustomContent platform="tidb">

-   単一の SQL ステートメントが`tidb_mem_quota_query`で指定されたメモリクォータを超え、ディスクに書き込むことができない場合に TiDB が実行する操作を指定します。詳細については[TiDB メモリ制御](/configure-memory-usage.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   単一の SQL ステートメントが[`tidb_mem_quota_query`](#tidb_mem_quota_query)で指定されたメモリクォータを超え、ディスクに書き込むことができない場合に TiDB が実行する操作を指定します。

</CustomContent>

-   デフォルト値は`CANCEL`ですが、TiDB v4.0.2 以前のバージョンではデフォルト値は`LOG`です。
-   この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_mem_quota_analyze <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-mem-quota-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト
-   この変数は、TiDB 統計更新の最大メモリ使用量を制御します。このようなメモリ使用量は、手動で[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行した場合と、TiDB がバックグラウンドでタスクを自動的に分析した場合に発生します。合計メモリ使用量がこのしきい値を超えると、ユーザーが実行した`ANALYZE`が終了し、より低いサンプリング レートを試すか、後で再試行するように通知するエラー メッセージが報告されます。メモリしきい値を超えたために TiDB バックグラウンドの自動タスクが終了し、使用されているサンプリング レートが既定値よりも高い場合、TiDB は既定のサンプリング レートを使用して更新を再試行します。この変数値が負またはゼロの場合、TiDB は手動更新タスクと自動更新タスクの両方のメモリ使用量を制限しません。

> **注記：**
>
> `auto_analyze` 、TiDB 起動構成ファイルで`run-auto-analyze`が有効になっている場合にのみ、TiDB クラスターでトリガーされます。

### tidb_mem_quota_apply_cache <span class="version-mark">v5.0 の新</span>機能 {#tidb-mem-quota-apply-cache-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `33554432` (32 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、 `Apply`演算子のローカル キャッシュのメモリ使用量しきい値を設定するために使用されます。
-   `Apply`演算子のローカル キャッシュは、 `Apply`演算子の計算を高速化するために使用されます。変数を`0`に設定すると、 `Apply`キャッシュ機能を無効にすることができます。

### tidb_mem_quota_binding_cache <span class="version-mark">v6.0.0 の新</span>機能 {#tidb-mem-quota-binding-cache-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[0, 2147483647]`
-   単位: バイト
-   この変数は、バインディングのキャッシュに使用されるメモリのしきい値を設定するために使用されます。
-   システムが過剰なバインディングを作成またはキャプチャし、メモリ領域が過剰に使用されると、TiDB はログに警告を返します。この場合、キャッシュは利用可能なすべてのバインディングを保持できないか、どのバインディングを保存するかを決定することができません。このため、一部のクエリではバインディングが失われる可能性があります。この問題に対処するには、この変数の値を増やして、バインディングのキャッシュに使用されるメモリを増やすことができます。このパラメータを変更した後、 `admin reload bindings`実行してバインディングを再読み込みし、変更を検証する必要があります。

### tidb_mem_quota_query {#tidb-mem-quota-query}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1073741824` (1 GiB)
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト

<CustomContent platform="tidb">

-   TiDB v6.1.0 より前のバージョンでは、これはセッション スコープ変数であり、初期値として`tidb.toml`から`mem-quota-query`の値を使用します。v6.1.0 以降では、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0 より前のバージョンでは、この変数は**クエリ**のメモリクォータのしきい値を設定するために使用されます。実行中のクエリのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0 以降のバージョンでは、この変数は**セッション**のメモリクォータのしきい値を設定するために使用されます。実行中のセッションのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。TiDB v6.5.0 以降では、セッションのメモリ使用量には、セッション内のトランザクションによって消費されるメモリが含まれることに注意してください。TiDB v6.5.0 以降のバージョンでのトランザクションメモリ使用量の制御動作については、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)を参照してください。
-   変数値を`0`または`-1`に設定すると、メモリしきい値は正の無限大になります。 128 より小さい値を設定すると、値はデフォルトで`128`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB v6.1.0 より前のバージョンでは、これはセッション スコープ変数です。v6.1.0 以降では、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0 より前のバージョンでは、この変数は**クエリ**のメモリクォータのしきい値を設定するために使用されます。実行中のクエリのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0 以降のバージョンでは、この変数は**セッション**のメモリクォータのしきい値を設定するために使用されます。実行中のセッションのメモリクォータがしきい値を超えると、TiDB は[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。TiDB v6.5.0 以降では、セッションのメモリ使用量には、セッション内のトランザクションによって消費されるメモリが含まれることに注意してください。
-   変数値を`0`または`-1`に設定すると、メモリしきい値は正の無限大になります。 128 より小さい値を設定すると、値はデフォルトで`128`になります。

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio {#tidb-memory-debug-mode-alarm-ratio}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   この変数は、TiDBメモリデバッグ モードで許可されるメモリ統計エラー値を表します。
-   この変数は TiDB の内部テストに使用されます。この変数を設定することは**お勧めしません**。

### tidb_memory_debug_mode_min_heap_inuse {#tidb-memory-debug-mode-min-heap-inuse}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0.0, 1.0]`

<CustomContent platform="tidb">

-   この変数は、tidb-serverメモリアラームをトリガーするメモリ使用率を設定します。デフォルトでは、TiDB のメモリ使用量が合計メモリの 70% を超え、 [警報条件](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage)のいずれかが満たされると、TiDB はアラーム ログを出力。
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能は無効になります。
-   この変数が`0`より大きく`1`より小さい値に設定されている場合、メモリしきい値アラーム機能が有効になっていることを意味します。

    -   システム変数[`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640)の値が`0`の場合、メモリアラームしきい値は`tidb_memory-usage-alarm-ratio * system memory size`なります。
    -   システム変数`tidb_server_memory_limit`の値が 0 より大きい値に設定されている場合、メモリアラームしきい値は`tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [tidb-serverメモリアラーム](https://docs.pingcap.com/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage)トリガーするメモリ使用率を設定します。
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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `5`
-   範囲: `[1, 10000]`
-   tidb-server のメモリ使用量がメモリアラームしきい値を超えてアラームをトリガーすると、TiDB はデフォルトで最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この変数を使用してこの数を調整できます。

### tidb_merge_join_concurrency {#tidb-merge-join-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   範囲: `[1, 256]`
-   デフォルト値: `1`
-   この変数は、クエリが実行されるときに`MergeJoin`演算子の同時実行性を設定します。
-   この変数を設定することは**推奨されません**。この変数の値を変更すると、データの正確性に問題が発生する可能性があります。

### tidb_merge_partition_stats_concurrency {#tidb-merge-partition-stats-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `1`
-   この変数は、TiDB がパーティションテーブルを分析するときに、パーティションテーブルの統計をマージする同時実行性を指​​定します。

### tidb_enable_async_merge_global_stats <span class="version-mark">v7.5.0 の新</span>機能 {#tidb-enable-async-merge-global-stats-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON` 。TiDB を v7.5.0 より前のバージョンから v7.5.0 以降のバージョンにアップグレードする場合、デフォルト値は`OFF`になります。
-   この変数は、OOM の問題を回避するために TiDB がグローバル統計を非同期的にマージするために使用されます。

### tidb_metric_query_range_duration <span class="version-mark">v4.0 の新</span>機能 {#tidb-metric-query-range-duration-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位: 秒
-   この変数は、クエリ`METRICS_SCHEMA`時に生成される Prometheus ステートメントの範囲期間を設定するために使用されます。

### tidb_metric_query_step <span class="version-mark">v4.0 の新</span>機能 {#tidb-metric-query-step-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 216000]`
-   単位: 秒
-   この変数は、クエリ`METRICS_SCHEMA`時に生成される Prometheus ステートメントのステップを設定するために使用されます。

### tidb_min_paging_size <span class="version-mark">v6.2.0 の新</span>機能 {#tidb-min-paging-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 期間
-   デフォルト値: `60s`
-   新しく起動したTiFlashノードはサービスを提供しません。クエリが失敗しないように、TiDB は tidb-server がクエリを送信することを新しく起動したTiFlashノードに制限します。この変数は、新しく起動したTiFlashノードにリクエストが送信されない時間範囲を示します。

### tidb_multi_statement_mode <span class="version-mark">v4.0.11 の新</span>機能 {#tidb-multi-statement-mode-span-class-version-mark-new-in-v4-0-11-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   可能`ON` `WARN` : `OFF`
-   この変数は、 `COM_QUERY`の呼び出しで複数のクエリを実行できるかどうかを制御します。
-   SQL インジェクション攻撃の影響を軽減するために、TiDB ではデフォルトで`COM_QUERY`回の呼び出しで複数のクエリが実行されないようにするようになりました。この変数は、以前のバージョンの TiDB からのアップグレード パスの一部として使用することを目的としています。次の動作が適用されます。

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
> -   [go-sql-ドライバー](https://github.com/go-sql-driver/mysql#multistatements) ( `multiStatements` )
> -   [コネクタ/J](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) ( `allowMultiQueries` )
> -   PHP [mysqli](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) ( `mysqli_multi_query` )

### tidb_nontransactional_ignore_error <span class="version-mark">v6.1.0 の新機能</span> {#tidb-nontransactional-ignore-error-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非トランザクション DML ステートメントでエラーが発生した場合に、すぐにエラーを返すかどうかを指定します。
-   値を`OFF`に設定すると、非トランザクション DML ステートメントは最初のエラーで直ちに停止し、エラーを返します。後続のバッチはすべてキャンセルされます。
-   値を`ON`に設定した場合、バッチでエラーが発生すると、すべてのバッチが実行されるまで後続のバッチが引き続き実行されます。実行プロセス中に発生したすべてのエラーは、結果にまとめて返されます。

### tidb_opt_agg_push_down {#tidb-opt-agg-push-down}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが集計関数を Join、Projection、および UnionAll の前の位置にプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリで集計操作が遅い場合は、変数値を ON に設定できます。

### tidb_opt_ブロードキャスト_カルテシアン_結合 {#tidb-opt-broadcast-cartesian-join}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   ブロードキャスト カテシアン結合を許可するかどうかを示します。
-   `0`ブロードキャスト カテシアン結合が許可されないことを意味します。 `1` [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50)に基づいて許可されることを意味します。 `2`テーブル サイズがしきい値を超えても常に許可されることを意味します。
-   この変数は TiDB で内部的に使用されるため、その値を変更することはお勧めし**ません**。

### tidb_opt_concurrency_factor {#tidb-opt-concurrency-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiDB でGolang goroutine を開始する際の CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_copcpu_factor {#tidb-opt-copcpu-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKVコプロセッサーが 1 行を処理するための CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_相関係数 {#tidb-opt-correlation-exp-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2147483647]`
-   列順序の相関に基づいて行数を推定する方法が利用できない場合は、ヒューリスティック推定方法が使用されます。この変数は、ヒューリスティック方法の動作を制御するために使用されます。
    -   値が 0 の場合、ヒューリスティック手法は使用されません。
    -   値が0より大きい場合:
        -   値が大きいほど、ヒューリスティックな方法でインデックス スキャンが使用される可能性が高くなります。
        -   値が小さいほど、ヒューリスティックな方法でテーブルスキャンが使用される可能性が高くなります。

### tidb_opt_相関しきい値 {#tidb-opt-correlation-threshold}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   デフォルト値: `0.9`
-   範囲: `[0, 1]`
-   この変数は、列順序の相関関係を使用して行数を推定することを有効にするかどうかを決定するしきい値を設定するために使用されます。現在の列と`handle`列目の順序の相関関係がしきい値を超えると、この方法が有効になります。

### tidb_opt_cpu_factor {#tidb-opt-cpu-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `3.0`
-   TiDB が 1 行を処理するための CPU コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨され**ません**。

### <code>tidb_opt_derive_topn</code> <span class="version-mark">v7.0.0 の新</span>機能 {#code-tidb-opt-derive-topn-code-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   [ウィンドウ関数から TopN または Limit を導出する](/derive-topn-from-window.md)の最適化ルールを有効にするかどうかを制御します。

### tidb_opt_desc_factor {#tidb-opt-desc-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKV がディスクから 1 行を降順でスキャンするのにかかるコストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_ディスク係数 {#tidb-opt-disk-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `1.5`
-   TiDB が一時ディスクから 1 バイトのデータを読み書きするための I/O コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_distinct_agg_push_down {#tidb-opt-distinct-agg-push-down}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが集計関数を`distinct` ( `select count(distinct a) from t`など) でコプロセッサーにプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリ内で`distinct`演算を含む集計関数が遅い場合は、変数値を`1`に設定できます。

次の例では、 `tidb_opt_distinct_agg_push_down`有効になる前に、 TiDB は TiKV からすべてのデータを読み取り、 TiDB 側で`distinct`を実行する必要があります。 `tidb_opt_distinct_agg_push_down`が有効になると、 `distinct a`がコプロセッサーにプッシュダウンされ、 `group by`列`test.t.a`が`HashAgg_5`に追加されます。

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
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザが列順序の相関に基づいて行数を推定するかどうかを制御するために使用されます。

### tidb_opt_enable_hash_join <span class="version-mark">v6.5.6、v7.1.2、v7.4.0 の新機能</span> {#tidb-opt-enable-hash-join-span-class-version-mark-new-in-v6-5-6-v7-1-2-and-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザがテーブルに対してハッシュ結合を選択するかどうかを制御するために使用されます。デフォルトの値は`ON`です。 `OFF`に設定すると、他の結合アルゴリズムが利用できない場合を除き、オプティマイザは実行プランを生成するときにハッシュ結合を選択しません。
-   システム変数`tidb_opt_enable_hash_join`と`HASH_JOIN`ヒントの両方が設定されている場合は、 `HASH_JOIN`ヒントが優先されます。 `tidb_opt_enable_hash_join`が`OFF`に設定されている場合でも、クエリで`HASH_JOIN`ヒントを指定すると、TiDB オプティマイザーはハッシュ結合プランを適用します。

### tidb_opt_enable_non_eval_scalar_subquery <span class="version-mark">v7.3.0 の新</span>機能 {#tidb-opt-enable-non-eval-scalar-subquery-span-class-version-mark-new-in-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `EXPLAIN`文が最適化段階で展開できる定数サブクエリの実行を無効にするかどうかを制御するために使用されます。この変数が`OFF`に設定されている場合、 `EXPLAIN`文は最適化段階でサブクエリを事前に展開します。この変数が`ON`に設定されている場合、 `EXPLAIN`文は最適化段階でサブクエリを展開しません。詳細については、 [サブクエリの拡張を無効にする](/explain-walkthrough.md#disable-the-early-execution-of-subqueries)を参照してください。

### tidb_opt_enable_late_materialization <span class="version-mark">v7.0.0 の新</span>機能 {#tidb-opt-enable-late-materialization-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [TiFlash の遅い実体化](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御するために使用されます。TiFlashの遅延マテリアライゼーションは[高速スキャンモード](/tiflash/use-fastscan.md)では有効にならないことに注意してください。
-   この変数を`OFF`に設定してTiFlash の遅延マテリアライゼーション機能を無効にした場合、フィルター条件 ( `WHERE`句) を含む`SELECT`ステートメントを処理するために、 TiFlash はフィルター処理の前に必要な列のすべてのデータをスキャンします。この変数を`ON`に設定してTiFlash の遅延マテリアライゼーション機能を有効にすると、 TiFlash は最初に TableScan 演算子にプッシュダウンされたフィルター条件に関連する列データをスキャンし、条件を満たす行をフィルター処理してから、これらの行の他の列のデータをスキャンしてさらに計算できるため、データ処理の IO スキャンと計算が削減されます。

### tidb_opt_enable_mpp_shared_cte_execution <span class="version-mark">v7.2.0 の新</span>機能 {#tidb-opt-enable-mpp-shared-cte-execution-span-class-version-mark-new-in-v7-2-0-span}

> **警告：**
>
> この変数によって制御される機能は実験的ものです。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非再帰[共通テーブル式 (CTE)](/sql-statements/sql-statement-with.md) TiFlash MPP で実行できるかどうかを制御します。デフォルトでは、この変数が無効になっている場合、CTE は TiDB で実行されますが、この機能を有効にした場合と比較してパフォーマンスの差が大きくなります。

### tidb_opt_fix_control <span class="version-mark">v6.5.3 および v7.1.0 の新機能</span> {#tidb-opt-fix-control-span-class-version-mark-new-in-v6-5-3-and-v7-1-0-span}

<CustomContent platform="tidb">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 文字列
-   デフォルト値: `""`
-   この変数は、オプティマイザの内部動作を制御するために使用されます。
-   オプティマイザーの動作は、ユーザー シナリオまたは SQL ステートメントによって異なる場合があります。この変数により、オプティマイザーをより細かく制御できるようになり、アップグレード後にオプティマイザーの動作変更によって発生するパフォーマンスの低下を防ぐことができます。
-   より詳しい紹介については[オプティマイザー修正コントロール](/optimizer-fix-controls.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 文字列
-   デフォルト値: `""`
-   この変数は、オプティマイザの内部動作を制御するために使用されます。
-   オプティマイザーの動作は、ユーザー シナリオまたは SQL ステートメントによって異なる場合があります。この変数により、オプティマイザーをより細かく制御できるようになり、アップグレード後にオプティマイザーの動作変更によって発生するパフォーマンスの低下を防ぐことができます。
-   より詳しい紹介については[オプティマイザー修正コントロール](https://docs.pingcap.com/tidb/v7.2/optimizer-fix-controls)参照してください。

</CustomContent>

### tidb_opt_force_inline_cte <span class="version-mark">v6.3.0 の新機能</span> {#tidb-opt-force-inline-cte-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、セッション全体の共通テーブル式 (CTE) がインライン化されるかどうかを制御するために使用されます。デフォルト値は`OFF`で、これは CTE のインライン化がデフォルトでは強制されないことを意味します。ただし、 `MERGE()`ヒントを指定することにより、CTE をインライン化することはできます。変数が`ON`に設定されている場合、このセッション内のすべての CTE (再帰 CTE を除く) は強制的にインライン化されます。

### tidb_opt_advanced_join_hint <span class="version-mark">v7.0.0 の新</span>機能 {#tidb-opt-advanced-join-hint-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`HASH_JOIN()`ヒント](/optimizer-hints.md#hash_joint1_name--tl_name-)や[`MERGE_JOIN()`ヒント](/optimizer-hints.md#merge_joint1_name--tl_name-)などの結合方法ヒントが、 [`LEADING()`ヒント](/optimizer-hints.md#leadingt1_name--tl_name-)の使用を含む結合したテーブルの再配置の最適化プロセスに影響を与えるかどうかを制御するために使用されます。デフォルト値は`ON`で、影響がないことを意味します。 `OFF`に設定すると、結合方法ヒントと`LEADING()`ヒントの両方が同時に使用されるシナリオで競合が発生する可能性があります。

> **注記：**
>
> v7.0.0 より前のバージョンの動作は、この変数を`OFF`に設定した場合の動作と一致します。以前のバージョンから v7.0.0 以降のクラスターにアップグレードする場合、前方互換性を確保するために、この変数は`OFF`に設定されます。より柔軟なヒント動作を得るには、パフォーマンスの低下がないという条件で、この変数を`ON`に切り替えることを強くお勧めします。

### tidb_opt_insubq_to_join_and_agg {#tidb-opt-insubq-to-join-and-agg}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、サブクエリを結合と集計に変換する最適化ルールを有効にするかどうかを設定するために使用されます。
-   たとえば、この最適化ルールを有効にすると、サブクエリは次のように変換されます。

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    サブクエリは次のように結合に変換されます。

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    `t1` `aa`列目の`unique`と`not null`に制限されている場合、集計なしで次のステートメントを使用できます。

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold {#tidb-opt-join-reorder-threshold}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB 結合したテーブルの再配置アルゴリズムの選択を制御するために使用されます。Join 結合したテーブルの再配置に参加するノードの数がこのしきい値より大きい場合、TiDB は貪欲アルゴリズムを選択し、このしきい値より小さい場合、TiDB は動的プログラミング アルゴリズムを選択します。
-   現在、OLTP クエリの場合、デフォルト値を維持することをお勧めします。OLAP クエリの場合、OLAP シナリオでより適切な接続順序を得るために、変数値を 10 ～ 15 に設定することをお勧めします。

### tidb_opt_limit_push_down_threshold {#tidb-opt-limit-push-down-threshold}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   この変数は、Limit または TopN 演算子を TiKV まで押し下げるかどうかを決定するしきい値を設定するために使用されます。
-   Limit または TopN 演算子の値がこのしきい値以下の場合、これらの演算子は強制的に TiKV にプッシュダウンされます。この変数は、誤った推定により Limit または TopN 演算子を TiKV にプッシュダウンできない問題を解決します。

### tidb_opt_メモリ係数 {#tidb-opt-memory-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `0.001`
-   TiDB が 1 行を格納するためのメモリコストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">v5.1.0 の新</span>機能 {#tidb-opt-mpp-outer-join-fixed-build-side-span-class-version-mark-new-in-v5-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   変数値が`ON`の場合、左結合演算子は常に内部テーブルを構築側として使用し、右結合演算子は常に外部テーブルを構築側として使用します。値を`OFF`に設定すると、外部結合演算子はどちらの側のテーブルも構築側として使用できます。

### tidb_opt_ネットワーク係数 {#tidb-opt-network-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.0`
-   ネットワークを介して 1 バイトのデータを転送する際の純コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_objective <span class="version-mark">v7.4.0 の新</span>機能 {#tidb-opt-objective-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `moderate`
-   可能な値: `moderate` 、 `determinate`
-   この変数は、オプティマイザの目的を制御します。1 `moderate` 、TiDB v7.4.0 より前のバージョンのデフォルトの動作を維持し、オプティマイザはより多くの情報を使用して、より優れた実行プランを生成しようとします`determinate`モードはより保守的になり、実行プランがより安定する傾向があります。
-   リアルタイム統計は、DML ステートメントに基づいて自動的に更新される行の合計数と変更された行の数です。この変数が`moderate` (デフォルト) に設定されている場合、TiDB はリアルタイム統計に基づいて実行プランを生成します。この変数が`determinate`に設定されている場合、TiDB は実行プランの生成にリアルタイム統計を使用しません。これにより、実行プランがより安定します。
-   長期にわたって安定した OLTP ワークロードの場合、またはユーザーが既存の実行プランに満足している場合は、予期しない実行プランの変更の可能性を減らすために`determinate`モードを使用することをお勧めします。また、統計が変更されないようにし、実行プランをさらに安定させるために[`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)を使用することもできます。

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">v7.0.0 の新機能</span> {#tidb-opt-ordering-index-selectivity-threshold-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、SQL ステートメントにフィルター条件を持つ句が`ORDER BY`または`LIMIT`ある場合に、オプティマイザーがインデックスを選択する方法を制御するために使用されます。
-   このようなクエリの場合、オプティマイザーは、 `ORDER BY`と`LIMIT`の句を満たす対応するインデックスを選択することを検討します (このインデックスがフィルター条件を満たしていない場合でも)。ただし、データ分散の複雑さにより、このシナリオではオプティマイザーが最適でないインデックスを選択する可能性があります。
-   この変数はしきい値を表します。フィルタリング条件を満たすインデックスが存在し、その選択性推定値がこのしきい値より低い場合、オプティマイザは`ORDER BY`と`LIMIT`を満たすために使用されるインデックスを選択しません。代わりに、フィルタリング条件を満たすインデックスを優先します。
-   たとえば、変数が`0`に設定されている場合、オプティマイザはデフォルトの動作を維持します。 `1`に設定されている場合、オプティマイザは常にフィルタ条件を満たすインデックスの選択を優先し、 `ORDER BY`と`LIMIT`句の両方を満たすインデックスの選択を回避します。
-   次の例では、テーブル`t`には合計 1,000,000 行があります。列`b`のインデックスを使用する場合、推定行数は約 8,748 なので、選択性推定値は約 0.0087 になります。デフォルトでは、オプティマイザは列`a`のインデックスを選択します。ただし、この変数を 0.01 に設定すると、列`b`のインデックスの選択性 (0.0087) は 0.01 未満になるため、オプティマイザは列`b`のインデックスを選択します。

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

### tidb_opt_prefer_range_scan <span class="version-mark">v5.0 の新</span>機能 {#tidb-opt-prefer-range-scan-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数の値を`ON`に設定すると、オプティマイザは常にフル テーブル スキャンよりも範囲スキャンを優先します。
-   次の例では、 `tidb_opt_prefer_range_scan`有効にする前に、TiDB オプティマイザは完全なテーブル スキャンを実行します。 `tidb_opt_prefer_range_scan`を有効にすると、オプティマイザはインデックス範囲スキャンを選択します。

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

### tidb_opt_prefix_index_single_scan <span class="version-mark">v6.4.0 の新</span>機能 {#tidb-opt-prefix-index-single-scan-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `ON`
-   この変数は、不要なテーブル検索を回避し、クエリのパフォーマンスを向上させるために、TiDB オプティマイザーが一部のフィルター条件をプレフィックス インデックスにプッシュダウンするかどうかを制御します。
-   この変数値が`ON`に設定されている場合、一部のフィルター条件がプレフィックス インデックスにプッシュダウンされます。 `col`列目がテーブル内のインデックス プレフィックス列であるとします。クエリ内の`col is null`または`col is not null`条件は、テーブル検索のフィルター条件ではなく、インデックスのフィルター条件として処理されるため、不要なテーブル検索が回避されます。

<details><summary><code>tidb_opt_prefix_index_single_scan</code>の使用例</summary>

プレフィックス インデックスを持つテーブルを作成します。

```sql
CREATE TABLE t (a INT, b VARCHAR(10), c INT, INDEX idx_a_b(a, b(5)));
```

無効化`tidb_opt_prefix_index_single_scan` :

```sql
SET tidb_opt_prefix_index_single_scan = 'OFF';
```

次のクエリでは、実行プランはプレフィックス インデックス`idx_a_b`を使用しますが、テーブル検索が必要です ( `IndexLookUp`演算子が表示されます)。

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

この変数を有効にすると、次のクエリでは実行プランでプレフィックス インデックス`idx_a_b`が使用されますが、テーブル検索は必要ありません。

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
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   オプティマイザが TiKV またはTiFlashコプロセッサに`Projection`プッシュダウンできるようにするかどうかを指定します。

### tidb_opt_range_max_size <span class="version-mark">v6.4.0 の新</span>機能 {#tidb-opt-range-max-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `67108864` (64 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、スキャン範囲を構築するためにオプティマイザが使用するメモリの上限を設定するために使用されます。変数値が`0`の場合、スキャン範囲を構築するためのメモリ制限はありません。正確なスキャン範囲を構築することで制限を超えるメモリが消費される場合、オプティマイザはより緩やかなスキャン範囲 ( `[[NULL,+inf]]`など) を使用します。実行プランで正確なスキャン範囲を使用しない場合は、この変数の値を増やして、オプティマイザが正確なスキャン範囲を構築できるようにすることができます。

この変数の使用例は次のとおりです。

<details><summary><code>tidb_opt_range_max_size</code>使用例</summary>

この変数のデフォルト値をビュー。結果から、オプティマイザーがスキャン範囲を構築するために最大 64 MiB のメモリを使用していることがわかります。

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

64 MiB のメモリ上限では、次の実行プランの結果に示すように、オプティマイザは次の正確なスキャン範囲`[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`を構築します。

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

ここで、スキャン範囲を構築するためのオプティマイザーのメモリ使用量の上限を 1500 バイトに設定します。

```sql
SET @@tidb_opt_range_max_size = 1500;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

1500 バイトのメモリ制限では、オプティマイザはより緩やかなスキャン範囲`[10,10], [20,20], [30,30]`を構築し、正確なスキャン範囲を構築するために必要なメモリ使用量が`tidb_opt_range_max_size`の制限を超えたことを警告を使用してユーザーに通知します。

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

100 バイトのメモリ制限では、オプティマイザは`IndexFullScan`選択し、正確なスキャン範囲を構築するために必要なメモリが`tidb_opt_range_max_size`の制限を超えていることを警告を使用してユーザーに通知します。

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

### tidb_opt_スキャン係数 {#tidb-opt-scan-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.5`
-   TiKV がディスクから 1 行のデータを昇順でスキャンするのにかかるコストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_seek_factor {#tidb-opt-seek-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `20`
-   TiDB が TiKV からデータを要求するための起動コストを示します。この変数は[コストモデル](/cost-model.md)で内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_skew_distinct_agg <span class="version-mark">v6.2.0 の新機能</span> {#tidb-opt-skew-distinct-agg-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この変数を有効にしてクエリ パフォーマンスを最適化すると、 **TiFlashに対してのみ**効果があります。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが`DISTINCT`を含む集計関数を 2 レベルの集計関数に書き換えるかどうか (たとえば、 `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換える) を設定します。集計列に重大な偏りがあり、 `DISTINCT`列に多くの異なる値がある場合、この書き換えによってクエリ実行時のデータ偏りを回避し、クエリのパフォーマンスを向上させることができます。

### tidb_opt_three_stage_distinct_agg <span class="version-mark">v6.3.0 の新機能</span> {#tidb-opt-three-stage-distinct-agg-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、MPP モードで`COUNT(DISTINCT)`段階の集約を 3 段階の集約に書き換えるかどうかを指定します。
-   この変数は現在、 `COUNT(DISTINCT)` 1 つだけ含む集計に適用されます。

### tidb_opt_tiflash_同時実行係数 {#tidb-opt-tiflash-concurrency-factor}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `24.0`
-   TiFlash計算の同時実行数を示します。この変数はコスト モデルで内部的に使用されるため、値を変更することは推奨されません。

### tidb_opt_write_row_id {#tidb-opt-write-row-id}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `INSERT` 、 `REPLACE` 、および`UPDATE`ステートメントが`_tidb_rowid`列で動作できるようにするかどうかを制御するために使用されます。この変数は、TiDB ツールを使用してデータをインポートする場合にのみ使用できます。

### tidb_optimizer_selectivity_level {#tidb-optimizer-selectivity-level}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、オプティマイザの推定ロジックの反復を制御します。この変数の値を変更すると、オプティマイザの推定ロジックが大きく変わります。現在、有効な値は`0`のみです。他の値に設定することはお勧めしません。

### tidb_partition_prune_mode <span class="version-mark">v5.1 の新</span>機能 {#tidb-partition-prune-mode-span-class-version-mark-new-in-v5-1-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `dynamic`
-   `static-only` `dynamic` `dynamic-only` : `static`
-   パーティション化されたテーブルに`dynamic`モードと`static`モードのどちらを使用するかを指定します。動的パーティション分割は、完全なテーブル レベルの統計、つまり GlobalStats が収集された後にのみ有効になることに注意してください。GlobalStats が収集される前は、TiDB は代わりに`static`モードを使用します。GlobalStats の詳細については、 [動的プルーニングモードでパーティションテーブルの統計を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)を参照してください。動的プルーニング モードの詳細については、 [パーティションテーブルの動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)を参照してください。

### tidb_persist_analyze_options <span class="version-mark">v5.4.0 の新</span>機能 {#tidb-persist-analyze-options-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [構成の永続性を分析する](/statistics.md#persist-analyze-configurations)機能を有効にするかどうかを制御します。

### tidb_pessimistic_txn_fair_locking <span class="version-mark">v7.0.0 の新機能</span> {#tidb-pessimistic-txn-fair-locking-span-class-version-mark-new-in-v7-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   悲観的トランザクションに拡張悲観的ロック ウェイクアップ モデルを使用するかどうかを決定します。このモデルは、悲観的ロックの単一ポイント競合シナリオで悲観的トランザクションのウェイクアップ順序を厳密に制御し、不要なウェイクアップを回避します。これにより、既存のウェイクアップ メカニズムのランダム性によってもたらされる不確実性が大幅に軽減されます。ビジネス シナリオで単一ポイントの悲観的ロック競合が頻繁に発生し (同じデータ行が頻繁に更新されるなど)、ステートメントの再試行が頻繁に発生したり、テールレイテンシーが長くなったり、 `pessimistic lock retry limit reached`エラーが時々発生したりする場合は、この変数を有効にして問題を解決してみてください。
-   この変数は、v7.0.0 より前のバージョンから v7.0.0 以降のバージョンにアップグレードされた TiDB クラスターではデフォルトで無効になっています。

> **注記：**
>
> -   特定のビジネス シナリオによっては、このオプションを有効にすると、ロックの競合が頻繁に発生するトランザクションで、ある程度のスループットの低下 (平均レイテンシーの増加) が発生する可能性があります。
> -   このオプションは、単一のキーをロックする必要があるステートメントにのみ有効です。ステートメントが複数の行を同時にロックする必要がある場合、このオプションはそのようなステートメントには有効ではありません。
> -   この機能は、デフォルトでは無効になっている[`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)変数によって v6.6.0 で導入されました。

### tidb_placement_mode <span class="version-mark">v6.0.0 の新</span>機能 {#tidb-placement-mode-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `STRICT`
-   可能`IGNORE`値: `STRICT`
-   この変数は、DDL ステートメントが[SQLで指定された配置ルール](/placement-rules-in-sql.md)無視するかどうかを制御します。変数値が`IGNORE`の場合、すべての配置ルール オプションは無視されます。
-   これは、無効な配置ルールが割り当てられている場合でもテーブルが常に作成できることを保証するために、論理ダンプ/リストア ツールによって使用されることを目的としています。これは、mysqldump がすべてのダンプ ファイルの先頭に`SET FOREIGN_KEY_CHECKS=0;`書き込む方法に似ています。

### <code>tidb_plan_cache_invalidation_on_fresh_stats</code> <span class="version-mark">v7.1.0 の新</span>機能 {#code-tidb-plan-cache-invalidation-on-fresh-stats-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、関連するテーブルの統計が更新されたときにプラン キャッシュを自動的に無効にするかどうかを制御します。
-   この変数を有効にすると、プラン キャッシュは統計をより十分に活用して実行プランを生成できるようになります。例:
    -   統計が利用可能になる前に実行プランが生成された場合、統計が利用可能になるとプラン キャッシュは実行プランを再生成します。
    -   テーブルのデータ分布が変更され、以前は最適だった実行プランが最適でなくなった場合、プラン キャッシュは統計が再収集された後に実行プランを再生成します。
-   この変数は、v7.1.0 より前のバージョンから v7.1.0 以降にアップグレードされた TiDB クラスターではデフォルトで無効になっています。

### <code>tidb_plan_cache_max_plan_size</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-plan-cache-max-plan-size-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `2097152` (2 MiB)
-   範囲: `[0, 9223372036854775807]` (バイト単位)。単位「KiB|MiB|GiB|TiB」のメモリ形式もサポートされています。3 `0`制限がないことを意味します。
-   この変数は、準備済みプラン キャッシュまたは準備されていないプラン キャッシュにキャッシュできるプランの最大サイズを制御します。プランのサイズがこの値を超えると、プランはキャッシュされません。詳細については、 [準備されたプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)および[準備されていないプラン キャッシュ](/sql-plan-management.md#usage)を参照してください。

### tidb_pprof_sql_cpu <span class="version-mark">v4.0 の新機能</span> {#tidb-pprof-sql-cpu-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、パフォーマンスの問題を識別してトラブルシューティングするために、プロファイル出力内の対応する SQL ステートメントをマークするかどうかを制御するために使用されます。

### tidb_prefer_broadcast_join_by_exchange_data_size <span class="version-mark">v7.1.0 の新機能</span> {#tidb-prefer-broadcast-join-by-exchange-data-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `OFF`
-   この変数は、TiDB が[MPPハッシュ結合アルゴリズム](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode)を選択するときに、ネットワーク転送のオーバーヘッドが最小のアルゴリズムを使用するかどうかを制御します。この変数を有効にすると、TiDB はそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`を使用してネットワークで交換されるデータのサイズを推定し、サイズの小さい方を選択します。
-   この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)有効になりません。

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">v6.1.0 の新機能</span> {#tidb-prepared-plan-cache-memory-guard-ratio-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.1`
-   範囲: `[0, 1]`
-   準備されたプラン キャッシュがメモリ保護メカニズムをトリガーするしきい値。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)を参照してください。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.memory-guard-ratio` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_prepared_plan_cache_size <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-prepared-plan-cache-size-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> v7.1.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   セッションでキャッシュできるプランの最大数。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)を参照してください。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.capacity` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_projection_concurrency {#tidb-projection-concurrency}

> **警告：**
>
> v5.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、 `Projection`演算子の同時実行性を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_query_log_max_len {#tidb-query-log-max-len}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4096` (4 KiB)
-   範囲: `[0, 1073741824]`
-   単位: バイト
-   SQL ステートメント出力の最大長。ステートメントの出力長が`tidb_query_log_max_len`値より大きい場合、ステートメントは切り捨てられて出力されます。
-   この設定は以前は`tidb.toml`オプション ( `log.query-log-max-len` ) としても使用可能でしたが、TiDB v6.1.0 以降ではシステム変数としてのみ使用可能になりました。

### tidb_rc_read_check_ts <span class="version-mark">v6.0.0 の新</span>機能 {#tidb-rc-read-check-ts-span-class-version-mark-new-in-v6-0-0-span}

> **警告：**
>
> -   この機能は[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。 `tidb_rc_read_check_ts`と`replica-read`同時に有効にしないでください。
> -   クライアントがカーソルを使用する場合、返されたデータの前のバッチがすでにクライアントによって使用されていて、ステートメントが最終的に失敗する可能性があるため、 `tidb_rc_read_check_ts`有効にすることはお勧めしません。
> -   v7.0.0 以降、この変数は、プリペアドステートメントプロトコルを使用するカーソル フェッチ読み取りモードでは有効ではなくなりました。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、タイムスタンプの取得を最適化するために使用されます。これは、読み取り/書き込みの競合がほとんど発生しない、読み取りコミット分離レベルのシナリオに適しています。この変数を有効にすると、グローバル タイムスタンプの取得にかかるレイテンシーとコストを回避でき、トランザクション レベルの読み取りレイテンシーを最適化できます。
-   読み取り/書き込みの競合が深刻な場合、この機能を有効にすると、グローバル タイムスタンプの取得にかかるコストとレイテンシーが増加し、パフォーマンスが低下する可能性があります。詳細については、 [コミット読み取り分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level)参照してください。

### tidb_rc_write_check_ts <span class="version-mark">v6.3.0 の新機能</span> {#tidb-rc-write-check-ts-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この機能は現在[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。この変数を有効にすると、クライアントから送信されるすべてのリクエストで`replica-read`を使用できなくなります。したがって、 `tidb_rc_write_check_ts`と`replica-read`同時に有効にしないでください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、タイムスタンプの取得を最適化するために使用され、悲観的トランザクションの分離レベル`READ-COMMITTED`でポイント書き込みの競合が少ないシナリオに適しています。この変数を有効にすると、ポイント書き込みステートメントの実行中にグローバル タイムスタンプを取得することによるレイテンシーとオーバーヘッドを回避できます。現在、この変数は`UPDATE` 、 `DELETE` 、および`SELECT ...... FOR UPDATE` 3 種類のポイント書き込みステートメントに適用できます。ポイント書き込みステートメントとは、主キーまたは一意キーをフィルター条件として使用し、最終実行演算子に`POINT-GET`含まれる書き込みステートメントを指します。
-   ポイント書き込みの競合が深刻な場合、この変数を有効にすると余分なオーバーヘッドとレイテンシーが増加し、パフォーマンスが低下します。詳細については、 [コミット読み取り分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level)参照してください。

### tidb_read_consistency <span class="version-mark">v5.4.0 の新</span>機能 {#tidb-read-consistency-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 文字列
-   デフォルト値: `strict`
-   この変数は、自動コミット読み取りステートメントの読み取り一貫性を制御するために使用されます。
-   変数値が`weak`に設定されている場合、読み取りステートメントによって検出されたロックは直接スキップされ、読み取り実行が高速化される可能性があります。これは、弱い一貫性の読み取りモードです。ただし、トランザクション セマンティクス (アトミック性など) と分散一貫性 (線形化可能性など) は保証されません。
-   自動コミット読み取りが高速に返す必要があり、弱い一貫性の読み取り結果が許容されるユーザー シナリオでは、弱い一貫性の読み取りモードを使用できます。

### tidb_read_staleness <span class="version-mark">v5.4.0 の新</span>機能 {#tidb-read-staleness-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-2147483648, 0]`
-   この変数は、TiDB が現在のセッションで読み取ることができる履歴データの時間範囲を設定するために使用されます。値を設定すると、TiDB はこの変数で許可された範囲からできるだけ新しいタイムスタンプを選択し、その後のすべての読み取り操作はこのタイムスタンプに対して実行されます。たとえば、この変数の値が`-5`に設定されている場合、TiKV に対応する履歴バージョンのデータがあるという条件で、TiDB は 5 秒の時間範囲内でできるだけ新しいタイムスタンプを選択します。

### tidb_record_plan_in_slow_log {#tidb-record-plan-in-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログにスロー クエリの実行プランを含めるかどうかを制御するために使用されます。

### tidb_redact_log {#tidb-redact-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB ログとスロー ログに記録される SQL ステートメント内のユーザー情報を非表示にするかどうかを制御します。
-   変数を`1`に設定すると、ユーザー情報は非表示になります。たとえば、実行された SQL 文が`insert into t values (1,2)`の場合、ログには`insert into t values (?,?)`として記録されます。

### tidb_regard_null_as_point <span class="version-mark">v5.4.0 の新</span>機能 {#tidb-regard-null-as-point-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザがインデックス アクセスのプレフィックス条件として NULL 等価性を含むクエリ条件を使用できるかどうかを制御します。
-   この変数はデフォルトで有効になっています。有効にすると、オプティマイザはアクセスするインデックス データのボリュームを削減できるため、クエリの実行が高速化されます。たとえば、クエリに複数列のインデックス`index(a, b)`が含まれ、クエリ条件に`a<=>null and b=1`含まれている場合、オプティマイザはインデックス アクセスのクエリ条件で`a<=>null`と`b=1`両方を使用できます。変数が無効になっている場合、 `a<=>null and b=1` null 等価条件が含まれているため、オプティマイザはインデックス アクセスに`b=1`使用しません。

### tidb_remove_orderby_in_subquery <span class="version-mark">v6.1.0 の新機能</span> {#tidb-remove-orderby-in-subquery-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: v7.2.0 より前では、デフォルト値は`OFF`です。v7.2.0 以降では、デフォルト値は`ON`です。
-   サブクエリ内の`ORDER BY`句を削除するかどうかを指定します。

### tidb_replica_read <span class="version-mark">v4.0 の新</span>機能 {#tidb-replica-read-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `leader`
-   可能な値: `leader` 、 `follower` 、 `leader-and-follower` 、 `prefer-leader` 、 `closest-replicas` 、 `closest-adaptive` 、および`learner` 。 値`learner` 、v6.6.0 で導入されました。
-   この変数は、TiDB がデータを読み取る場所を制御するために使用されます。
-   使用方法と実装の詳細については、 [Followerが読んだ](/follower-read.md)参照してください。

### tidb_restricted_read_only <span class="version-mark">v5.2.0 の新機能</span> {#tidb-restricted-read-only-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_restricted_read_only`と[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)同様に動作します。ほとんどの場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを使用する必要があります。
-   `SUPER`または`SYSTEM_VARIABLES_ADMIN`権限を持つユーザーはこの変数を変更できます。ただし、 [Security強化モード](#tidb_enable_enhanced_security)が有効になっている場合は、この変数の読み取りまたは変更には追加の`RESTRICTED_VARIABLES_ADMIN`権限が必要です。
-   次の場合には`tidb_restricted_read_only` [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)影響します。
    -   `tidb_restricted_read_only` `ON`に設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)を`ON`に更新されます。
    -   `tidb_restricted_read_only` `OFF`に設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)変更されません。
    -   `tidb_restricted_read_only`が`ON`の場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) `OFF`に設定することはできません。
-   TiDB の DBaaS プロバイダーの場合、TiDB クラスターが別のデータベースのダウンストリーム データベースである場合、TiDB クラスターを読み取り専用にするには、 [Security強化モード](#tidb_enable_enhanced_security)有効にした`tidb_restricted_read_only`を使用する必要があります。これにより、顧客が[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)を使用してクラスターを書き込み可能にすることができなくなります。これを実現するには、 [Security強化モード](#tidb_enable_enhanced_security)有効にし、 `SYSTEM_VARIABLES_ADMIN`および`RESTRICTED_VARIABLES_ADMIN`権限を持つ管理者ユーザーを使用して`tidb_restricted_read_only`を制御し、データベース ユーザーが`SUPER`権限を持つルート ユーザーを使用して[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを制御できるようにする必要があります。
-   この変数は、クラスター全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスター全体のすべての TiDB サーバーは読み取り専用モードになります。この場合、 TiDB は`SELECT` 、 `USE` 、 `SHOW`などのデータを変更しないステートメントのみを実行します。 `INSERT`や`UPDATE`などの他のステートメントについては、 TiDB は読み取り専用モードでのそれらのステートメントの実行を拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスター全体が最終的に読み取り専用ステータスになることが保証されます。TiDB クラスターでこの変数の値を変更したが、その変更がまだ他の TiDB サーバーに伝播していない場合、更新されていない TiDB サーバーはまだ読み取り専用モードではあり**ません**。
-   TiDB は、SQL ステートメントが実行される前に読み取り専用フラグをチェックします。v6.2.0 以降では、SQL ステートメントがコミットされる前にもフラグがチェックされます。これにより、サーバーが読み取り専用モードになった後に、長時間実行される[自動コミット](/transaction-overview.md#autocommit)ステートメントによってデータが変更される可能性を防ぐことができます。
-   この変数を有効にすると、TiDB はコミットされていないトランザクションを次の方法で処理します。
    -   コミットされていない読み取り専用トランザクションの場合は、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行する SQL ステートメントは拒否されます。
    -   変更されたデータを含むコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードを有効にすると、ユーザーに`RESTRICTED_REPLICA_WRITER_ADMIN`権限が明示的に付与されていない限り、すべてのユーザー ( `SUPER`権限を持つユーザーを含む) は、データを書き込む可能性のある SQL ステートメントを実行できなくなります。

### tidb_request_source_type <span class="version-mark">v7.4.0 の新</span>機能 {#tidb-request-source-type-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: `""`
-   `"br"` `"stats"` `"background"` `"lightning"` `"ddl"`
-   この変数は、 [リソース管理](/tidb-resource-control.md)によって識別および制御される現在のセッションのタスク タイプを明示的に指定するために使用されます。例: `SET @@tidb_request_source_type = "background"` 。

### tidb_再試行制限 {#tidb-retry-limit}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、楽観的トランザクションの最大再試行回数を設定するために使用されます。トランザクションで再試行可能なエラー (トランザクションの競合、非常に遅いトランザクションのコミット、テーブル スキーマの変更など) が発生すると、このトランザクションはこの変数に従って再実行されます。1 から`tidb_retry_limit`に設定すると、自動再試行が無効になることに注意してください。この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用され`0`ん。

### tidb_row_format_version {#tidb-row-format-version}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   テーブルに新しく保存されるデータの形式バージョンを制御します。TiDB v4.0 では、新しいデータを保存するにはデフォルトでバージョン[新しいstorage行形式](https://github.com/pingcap/tidb/blob/release-7.5/docs/design/2018-07-19-row-format.md) `2`が使用されます。
-   TiDB バージョン v4.0.0 より前のバージョンから v4.0.0 以降のバージョンにアップグレードする場合、フォーマット バージョンは変更されず、TiDB は引き続きバージョン`1`の古いフォーマットを使用してテーブルにデータを書き込みます。つまり、**新しく作成されたクラスターのみがデフォルトで新しいデータ フォーマットを使用する**ことになります。
-   この変数を変更しても、保存されている古いデータには影響しませんが、この変数を変更した後に新しく書き込まれたデータにのみ、対応するバージョン形式が適用されることに注意してください。

### tidb_runtime_filter_mode <span class="version-mark">v7.2.0 の新</span>機能 {#tidb-runtime-filter-mode-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   可能`LOCAL`値: `OFF`
-   ランタイム フィルターのモード、つまり**フィルター送信側演算子**と**フィルター受信側演算子**の関係を制御します。モードは`OFF`と`LOCAL` 2 つがあります。9 `OFF`ランタイム フィルターを無効にすることを意味します。11 `LOCAL`ローカル モードでランタイム フィルターを有効にすることを意味します。詳細については、 [ランタイムフィルターモード](/runtime-filter.md#runtime-filter-mode)を参照してください。

### tidb_runtime_filter_type <span class="version-mark">v7.2.0 の新</span>機能 {#tidb-runtime-filter-type-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `IN`
-   可能な値: `IN`
-   生成されたフィルター演算子によって使用される述語のタイプを制御します。現在サポートされているタイプは`IN`のみです。詳細については、 [ランタイムフィルタータイプ](/runtime-filter.md#runtime-filter-type)を参照してください。

### tidb_scatter_region {#tidb-scatter-region}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   デフォルトでは、TiDB で新しいテーブルが作成されるときに、そのテーブルの領域が分割されます。この変数を有効にすると、 `CREATE TABLE`のステートメントの実行中に、新しく分割された領域がすぐに分散されます。これは、テーブルがバッチで作成された直後にデータをバッチで書き込む必要があるシナリオに適用されます。これは、新しく分割された領域を事前に TiKV に分散できるため、PD によってスケジュールされるのを待つ必要がないためです。バッチでのデータ書き込みの継続的な安定性を確保するために、 `CREATE TABLE`のステートメントは、領域が正常に分散された後にのみ成功を返します。これにより、この変数を無効にした場合よりも、ステートメントの実行時間が何倍も長くなります。
-   テーブルの作成時に`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`設定されている場合、テーブルの作成後に指定された数のリージョンが均等に分割されることに注意してください。

### tidb_schema_version_cache_limit <span class="version-mark">v7.4.0 の新</span>機能 {#tidb-schema-version-cache-limit-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `16`
-   範囲: `[2, 255]`
-   この変数は、TiDB インスタンスにキャッシュできる履歴スキーマ バージョンの数を制限します。デフォルト値は`16`で、これは、TiDB がデフォルトで 16 個の履歴スキーマ バージョンをキャッシュすることを意味します。
-   通常、この変数を変更する必要はありません。 [ステイル読み取り](/stale-read.md)機能を使用し、DDL 操作が頻繁に実行されると、スキーマ バージョンが頻繁に変更されます。その結果、 ステイル読み取り がスナップショットからスキーマ情報を取得しようとすると、スキーマ キャッシュ ミスのために情報の再構築に時間がかかる場合があります。この場合、 `tidb_schema_version_cache_limit`の値を増やす (たとえば、 `32` ) ことで、スキーマ キャッシュ ミスの問題を回避できます。
-   この変数を変更すると、TiDB のメモリ使用量がわずかに増加します。OOM の問題を回避するには、TiDB のメモリ使用量を監視してください。

### tidb_server_memory_limit <span class="version-mark">v6.4.0 の新</span>機能 {#tidb-server-memory-limit-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `80%`
-   範囲：
    -   値はパーセンテージ形式で設定できます。これは、メモリ使用量を総メモリに対してパーセンテージで表したものです。値の範囲は`[1%, 99%]`です。
    -   メモリサイズの値も設定できます。値の範囲はバイト単位で`0` ～ `[536870912, 9223372036854775807]`です。単位が「KiB|MiB|GiB|TiB」のメモリ形式がサポートされています。5 `0`メモリ制限がないことを意味します。
    -   この変数が 512 MiB 未満で`0`以外のメモリサイズに設定されている場合、TiDB は実際のサイズとして 512 MiB を使用します。
-   この変数は、TiDB インスタンスのメモリ制限を指定します。TiDB のメモリ使用量が制限に達すると、TiDB はメモリ使用量が最も高い現在実行中の SQL ステートメントをキャンセルします。SQL ステートメントが正常にキャンセルされると、TiDB はGolang GC を呼び出してメモリをすぐに再利用し、できるだけ早くメモリのストレスを軽減しようとします。
-   メモリ使用量が[`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)制限を超える SQL ステートメントのみが、最初にキャンセルされる SQL ステートメントとして選択されます。
-   現在、TiDB は一度に 1 つの SQL ステートメントのみをキャンセルします。TiDB が SQL ステートメントを完全にキャンセルしてリソースを回復した後、メモリ使用量がこの変数で設定された制限よりもまだ大きい場合、TiDB は次のキャンセル操作を開始します。

### tidb_server_memory_limit_gc_trigger <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-gc-trigger-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `70%`
-   範囲: `[50%, 99%]`
-   TiDB が GC をトリガーしようとするしきい値。TiDB のメモリ使用量が`tidb_server_memory_limit` * `tidb_server_memory_limit_gc_trigger`の値に達すると、TiDB はGolang GC 操作をアクティブにトリガーします。1 分間にトリガーされる GC 操作は 1 つだけです。

### tidb_server_memory_limit_sess_min_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-sess-min-size-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `134217728` (128 MiB)
-   範囲: `[128, 9223372036854775807]` (バイト単位)。単位「KiB|MiB|GiB|TiB」のメモリ形式もサポートされています。
-   メモリ制限を有効にすると、TiDB は現在のインスタンスでメモリ使用量が最も高い SQL ステートメントを終了します。この変数は、終了する SQL ステートメントの最小メモリ使用量を指定します。メモリメモリメモリが制限を超えている場合は、この変数の値を適切に下げて、より多くのセッションをキャンセルできるようにすることができます。

### tidb_service_scope <span class="version-mark">v7.4.0 の新</span>機能 {#tidb-service-scope-span-class-version-mark-new-in-v7-4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに存続: いいえ
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   オプション値: &quot;&quot;, `background`
-   この変数はインスタンス レベルのシステム変数です。これを使用して、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)の下にある TiDB ノードのサービス スコープを制御できます。TiDB ノードの`tidb_service_scope` `background`に設定すると、DXF はその TiDB ノードが[`ADD INDEX`](/sql-statements/sql-statement-add-index.md)や[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)などのバックグラウンド タスクを実行するようにスケジュールします。

> **注記：**
>
> -   クラスター内のどの TiDB ノードにも`tidb_service_scope`設定されていない場合、DXF はすべての TiDB ノードがバックグラウンド タスクを実行するようにスケジュールします。現在のビジネスに対するパフォーマンスの影響が懸念される場合は、いくつかの TiDB ノードに`tidb_service_scope` ～ `background`を設定できます。これらのノードのみがバックグラウンド タスクを実行します。
> -   複数の TiDB ノードがあるクラスターでは、2 つ以上の TiDB ノードでこのシステム変数を`background`に設定することを強くお勧めします。1 つの TiDB ノードのみに`tidb_service_scope`が設定されている場合、ノードが再起動されるか障害が発生すると、タスクは`background`が設定されていない他の TiDB ノードに再スケジュールされ、これらの TiDB ノードに影響を及ぼします。
> -   新しくスケールされたノードの場合、スケールされたノードのリソースの消費を避けるため、DXF タスクはデフォルトでは実行されません。このスケールされたノードでバックグラウンド タスクを実行する場合は、このノードの`tidb_service_scop` `background`に手動で設定する必要があります。

### tidb_session_alias <span class="version-mark">v7.4.0 の新機能</span> {#tidb-session-alias-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: セッション
-   クラスターに存続: いいえ
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: &quot;&quot;
-   この変数を使用すると、現在のセッションに関連するログの`session_alias`列目の値をカスタマイズできます。これは、トラブルシューティングでセッションを識別するのに役立ちます。この設定は、ステートメントの実行に関係する複数のノード (TiKV を含む) のログに影響します。この変数の最大長は 64 文字に制限されており、長さを超える文字は自動的に切り捨てられます。値の末尾のスペースも自動的に削除されます。

### tidb_session_plan_cache_size <span class="version-mark">v7.1.0 の新</span>機能 {#tidb-session-plan-cache-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は[準備されたプランキャッシュ](/sql-prepared-plan-cache.md)キャッシュできるプランの最大数を制御します。1 と[準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)同じキャッシュを共有します。
-   以前のバージョンからv7.1.0以降のバージョンにアップグレードすると、この変数は[`tidb_prepared_plan_cache_size`](#tidb_prepared_plan_cache_size-new-in-v610)と同じ値のままになります。

### tidb_shard_allocate_step <span class="version-mark">v5.0 の新</span>機能 {#tidb-shard-allocate-step-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `9223372036854775807`
-   範囲: `[1, 9223372036854775807]`
-   この変数は、 [`AUTO_RANDOM`](/auto-random.md)または[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)属性に割り当てられる連続 ID の最大数を制御します。通常、1 つのトランザクションでは、 `AUTO_RANDOM` ID または`SHARD_ROW_ID_BITS`注釈付き行 ID が増分され、連続します。この変数を使用すると、大規模なトランザクション シナリオでのホットスポットの問題を解決できます。

### tidb_簡易メトリクス {#tidb-simplified-metrics}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数を有効にすると、TiDB は Grafana パネルで使用されていないメトリックを収集または記録しません。

### tidb_skip_ascii_check <span class="version-mark">v5.0 の新</span>機能 {#tidb-skip-ascii-check-span-class-version-mark-new-in-v5-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ASCII 検証をスキップするかどうかを設定するために使用されます。
-   ASCII 文字の検証はパフォーマンスに影響します。入力文字が有効な ASCII 文字であることが確実な場合は、変数値を`ON`に設定できます。

### tidb_skip_isolation_level_check {#tidb-skip-isolation-level-check}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   このスイッチを有効にすると、TiDB でサポートされていない分離レベルが`tx_isolation`に割り当てられても、エラーは報告されません。これにより、異なる分離レベルを設定する (ただし、それに依存しない) アプリケーションとの互換性が向上します。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_missing_partition_stats <span class="version-mark">v7.3.0 の新機能</span> {#tidb-skip-missing-partition-stats-span-class-version-mark-new-in-v7-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   [動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)でパーティションテーブルにアクセスすると、TiDB は各パーティションの統計を集計して GlobalStats を生成します。この変数は、パーティション統計が欠落している場合の GlobalStats の生成を制御します。

    -   この変数が`ON`の場合、TiDB は GlobalStats を生成するときに欠落しているパーティション統計をスキップするため、GlobalStats の生成には影響しません。
    -   この変数が`OFF`の場合、TiDB はパーティション統計の欠落を検出すると GlobalStats の生成を停止します。

### tidb_skip_utf8_check {#tidb-skip-utf8-check}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、UTF-8 検証をスキップするかどうかを設定するために使用されます。
-   UTF-8 文字の検証はパフォーマンスに影響します。入力文字が有効な UTF-8 文字であることが確実な場合は、変数値を`ON`に設定できます。

> **注記：**
>
> 文字チェックをスキップすると、TiDB はアプリケーションによって書き込まれた不正な UTF-8 文字を検出できず、 `ANALYZE`実行時にデコード エラーが発生し、その他の未知のエンコードの問題が発生する可能性があります。アプリケーションが書き込まれた文字列の有効性を保証できない場合は、文字チェックをスキップすることはお勧めしません。

### tidb_slow_log_threshold {#tidb-slow-log-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持: いいえ。接続している現在の TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[-1, 9223372036854775807]`
-   単位: ミリ秒
-   この変数は、スロー ログで消費される時間のしきい値を出力するために使用されます。クエリで消費される時間がこの値より大きい場合、このクエリはスロー ログとみなされ、そのログはスロー クエリ ログに出力されます。

### tidb_slow_query_file {#tidb-slow-query-file}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   `INFORMATION_SCHEMA.SLOW_QUERY`をクエリすると、構成ファイルで`slow-query-file`で設定されたスロー クエリ ログ名のみが解析されます。デフォルトのスロー クエリ ログ名は「tidb-slow.log」です。他のログを解析するには、 `tidb_slow_query_file`セッション変数を特定のファイル パスに設定し、 `INFORMATION_SCHEMA.SLOW_QUERY`をクエリして、設定されたファイル パスに基づいてスロー クエリ ログを解析します。

<CustomContent platform="tidb">

詳細は[遅いクエリを特定する](/identify-slow-queries.md)参照。

</CustomContent>

### スナップショット {#tidb-snapshot}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   この変数は、セッションによってデータが読み取られる時点を設定するために使用されます。たとえば、変数を「2017-11-11 20:20:20」または「400036290571534337」のような TSO 番号に設定すると、現在のセッションはその瞬間のデータを読み取ります。

### tidb_source_id <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-source-id-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 15]`

<CustomContent platform="tidb">

-   この変数は、 [双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)クラスター内の異なるクラスター ID を構成するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [双方向レプリケーション](https://docs.pingcap.com/tidb/stable/ticdc-bidirectional-replication)クラスター内の異なるクラスター ID を構成するために使用されます。

</CustomContent>

### tidb_stats_cache_mem_quota <span class="version-mark">v6.1.0 の新</span>機能 {#tidb-stats-cache-mem-quota-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   単位: バイト
-   デフォルト値: `0` 。これは、メモリクォータが TiDB インスタンスの合計メモリサイズの半分に自動的に設定されることを意味します。
-   範囲: `[0, 1099511627776]`
-   この変数は、TiDB 統計キャッシュのメモリクォータを設定します。

### tidb_stats_load_pseudo_timeout <span class="version-mark">v5.4.0 の新機能</span> {#tidb-stats-load-pseudo-timeout-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、SQL 最適化の待機時間がタイムアウトに達し、完全な列統計を同期的にロードするときに TiDB がどのように動作するかを制御します。デフォルト値`ON` 、タイムアウト後に SQL 最適化が疑似統計の使用に戻ることを意味します。この変数を`OFF`に設定すると、タイムアウト後に SQL 実行が失敗します。

### tidb_stats_load_sync_wait <span class="version-mark">v5.4.0 の新機能</span> {#tidb-stats-load-sync-wait-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   この変数は、統計の同期ロード機能を有効にするかどうかを制御します。値`0` 、機能が無効であることを意味します。この機能を有効にするには、この変数を、完全な列統計を同期ロードするために SQL 最適化が最大で待機できるタイムアウト (ミリ秒単位) に設定できます。詳細については、 [負荷統計](/statistics.md#load-statistics)を参照してください。

### tidb_stmt_summary_enable_persistent <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-enable-persistent-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効にするかどうかを制御します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_filename <span class="version-mark">v6.6.0 の新</span>機能 {#tidb-stmt-summary-filename-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: `"tidb-statements.log"`
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合に永続データが書き込まれるファイルを指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_backups <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-file-max-backups-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合に保持できるデータ ファイルの最大数を指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_days <span class="version-mark">v6.6.0 の新</span>機能 {#tidb-stmt-summary-file-max-days-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `3`
-   単位: 日
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合に永続データ ファイルを保持する最大日数を指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_size <span class="version-mark">v6.6.0 の新</span>機能 {#tidb-stmt-summary-file-max-size-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `64`
-   単位: MiB
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合、永続データ ファイルの最大サイズを指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_history_size <span class="version-mark">v4.0 の新</span>機能 {#tidb-stmt-summary-history-size-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `24`
-   範囲: `[0, 255]`
-   この変数は、履歴容量を[ステートメント要約表](/statement-summary-tables.md)に設定するために使用されます。

### tidb_stmt_summary_internal_query <span class="version-mark">v4.0 の新</span>機能 {#tidb-stmt-summary-internal-query-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB の SQL 情報を[ステートメント要約表](/statement-summary-tables.md)に含めるかどうかを制御するために使用されます。

### tidb_stmt_summary_max_sql_length <span class="version-mark">v4.0 の新</span>機能 {#tidb-stmt-summary-max-sql-length-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4096`
-   範囲: `[0, 2147483647]`
-   単位: バイト

<CustomContent platform="tidb">

-   この変数は、 [ステートメント要約表](/statement-summary-tables.md)と[TiDBダッシュボード](/dashboard/dashboard-intro.md)の SQL 文字列の長さを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [ステートメント要約表](/statement-summary-tables.md)の SQL 文字列の長さを制御するために使用されます。

</CustomContent>

### tidb_stmt_summary_max_stmt_count <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-max-stmt-count-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `3000`
-   範囲: `[1, 32767]`
-   この変数は、メモリ[ステートメント要約表](/statement-summary-tables.md)保存するステートメントの最大数を設定するために使用されます。

### tidb_stmt_summary_refresh_interval <span class="version-mark">v4.0 の新</span>機能 {#tidb-stmt-summary-refresh-interval-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1800`
-   範囲: `[1, 2147483647]`
-   単位: 秒
-   この変数は、 [ステートメント要約表](/statement-summary-tables.md)の更新時間を設定するために使用されます。

### tidb_store_batch_size {#tidb-store-batch-size}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[0, 25000]`
-   この変数は、 `IndexLookUp`オペレータのコプロセッサータスクのバッチ サイズを制御するために使用されます。3 `0`バッチを無効にすることを意味します。タスクの数が比較的多く、遅いクエリが発生する場合は、この変数を増やしてクエリを最適化できます。

### tidb_store_limit <span class="version-mark">v3.0.4 および v4.0 の新</span>機能 {#tidb-store-limit-span-class-version-mark-new-in-v3-0-4-and-v4-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、TiDB が TiKV に同時に送信できるリクエストの最大数を制限するために使用されます。0 は制限なしを意味します。

### tidb_streamagg_同時実行性 {#tidb-streamagg-concurrency}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   この変数は、クエリが実行されるときに`StreamAgg`演算子の同時実行性を設定します。
-   この変数を設定することは**推奨されません**。変数値を変更すると、データの正確性に問題が発生する可能性があります。

### tidb_super_read_only <span class="version-mark">v5.3.1 の新機能</span> {#tidb-super-read-only-span-class-version-mark-new-in-v5-3-1-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_super_read_only` MySQL 変数`super_read_only`の置き換えとして実装することを目指しています。ただし、TiDB は分散データベースであるため、 `tidb_super_read_only`実行後すぐにデータベースを読み取り専用にするのではなく、最終的には読み取り専用にします。
-   権限`SUPER`または`SYSTEM_VARIABLES_ADMIN`を持つユーザーはこの変数を変更できます。
-   この変数は、クラスター全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスター全体のすべての TiDB サーバーは読み取り専用モードになります。この場合、 TiDB は`SELECT` 、 `USE` 、 `SHOW`などのデータを変更しないステートメントのみを実行します。 `INSERT`や`UPDATE`などの他のステートメントについては、 TiDB は読み取り専用モードでのそれらのステートメントの実行を拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスター全体が最終的に読み取り専用ステータスになることが保証されます。TiDB クラスターでこの変数の値を変更したが、その変更がまだ他の TiDB サーバーに伝播していない場合、更新されていない TiDB サーバーはまだ読み取り専用モードではあり**ません**。
-   TiDB は、SQL ステートメントが実行される前に読み取り専用フラグをチェックします。v6.2.0 以降では、SQL ステートメントがコミットされる前にもフラグがチェックされます。これにより、サーバーが読み取り専用モードになった後に、長時間実行される[自動コミット](/transaction-overview.md#autocommit)ステートメントによってデータが変更される可能性を防ぐことができます。
-   この変数を有効にすると、TiDB はコミットされていないトランザクションを次の方法で処理します。
    -   コミットされていない読み取り専用トランザクションの場合は、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行する SQL ステートメントは拒否されます。
    -   変更されたデータを含むコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードを有効にすると、ユーザーに`RESTRICTED_REPLICA_WRITER_ADMIN`権限が明示的に付与されていない限り、すべてのユーザー ( `SUPER`権限を持つユーザーを含む) は、データを書き込む可能性のある SQL ステートメントを実行できなくなります。
-   [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)システム変数が`ON`に設定されている場合、 `tidb_super_read_only` [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の影響を受ける場合があります。詳細な影響については、 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の説明を参照してください。

### tidb_sysdate_is_now <span class="version-mark">v6.0.0 の新機能</span> {#tidb-sysdate-is-now-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、関数`SYSDATE`関数`NOW`に置き換えることができるかどうかを制御するために使用されます。この構成項目は、MySQL オプション[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。

### tidb_sysproc_scan_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-sysproc-scan-concurrency-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、TiDB が内部 SQL ステートメント (統計の自動更新など) を実行するときに実行されるスキャン操作の同時実行性を設定するために使用されます。

### tidb_table_cache_lease <span class="version-mark">v6.0.0 の新</span>機能 {#tidb-table-cache-lease-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `3`
-   範囲: `[1, 10]`
-   単位: 秒
-   この変数は、リース時間[キャッシュされたテーブル](/cached-tables.md)を制御するために使用されます。デフォルト値は`3`です。この変数の値は、キャッシュされたテーブルの変更に影響します。キャッシュされたテーブルに変更を加えた後、最長の待機時間は`tidb_table_cache_lease`秒になる可能性があります。テーブルが読み取り専用であるか、書き込みレイテンシーが長い場合は、この変数の値を増やして、キャッシュ テーブルの有効時間を増やし、リース更新の頻度を減らすことができます。

### tidb_tmp_table_max_size <span class="version-mark">v5.3.0 の新</span>機能 {#tidb-tmp-table-max-size-span-class-version-mark-new-in-v5-3-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[1048576, 137438953472]`
-   単位: バイト
-   この変数は、単一の[一時テーブル](/temporary-tables.md)の最大サイズを設定するために使用されます。この変数値より大きいサイズの一時テーブルではエラーが発生します。

### tidb_top_sql_max_meta_count <span class="version-mark">v6.0.0 の新機能</span> {#tidb-top-sql-max-meta-count-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `5000`
-   範囲: `[1, 10000]`

<CustomContent platform="tidb">

-   この変数は、1 分あたり[Top SQL](/dashboard/top-sql.md)ずつ収集される SQL ステートメント タイプの最大数を制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、1 分あたり[Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)ずつ収集される SQL ステートメント タイプの最大数を制御するために使用されます。

</CustomContent>

### tidb_top_sql_max_time_series_count <span class="version-mark">v6.0.0 の新機能</span> {#tidb-top-sql-max-time-series-count-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

> **注記：**
>
> 現在、TiDB ダッシュボードの「Top SQL」ページには、負荷に最も寄与している上位 5 種類の SQL クエリのみが表示されます。これは、 `tidb_top_sql_max_time_series_count`の構成とは無関係です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
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

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB が集計関数のメモリ使用量を追跡するかどうかを制御します。

> **警告：**
>
> この変数を無効にすると、TiDB はメモリ使用量を正確に追跡できず、対応する SQL ステートメントのメモリ使用量を制御できなくなる可能性があります。

### tidb_tso_client_batch_max_wait_time <span class="version-mark">v5.3.0 の新</span>機能 {#tidb-tso-client-batch-max-wait-time-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 10]`
-   単位: ミリ秒
-   この変数は、TiDB が PD から TSO を要求するときのバッチ操作の最大待機時間を設定するために使用されます。デフォルト値は`0`で、追加の待機時間がないことを意味します。
-   TiDB が使用する PD クライアントは、PD から TSO 要求を毎回取得する際に、同時に受信した TSO 要求を可能な限り収集します。その後、PD クライアントは収集した要求をバッチで 1 つの RPC 要求にマージして PD に送信します。これにより、PD の負荷を軽減できます。
-   この変数を`0`より大きい値に設定すると、TiDB は各バッチ マージの終了前にこの値の最大期間待機します。これは、より多くの TSO 要求を収集し、バッチ操作の効果を向上させるためです。
-   この変数の値を増やすシナリオ:
    -   TSO 要求の負荷が高いため、PD リーダーの CPU がボトルネックになり、TSO RPC 要求のレイテンシーが高くなります。
    -   クラスター内の TiDB インスタンスは多くありませんが、すべての TiDB インスタンスは高い同時実行性を備えています。
-   この変数はできるだけ小さい値に設定することをお勧めします。

> **注記：**
>
> PD リーダーの CPU 使用率のボトルネック以外の理由 (ネットワークの問題など) で TSO RPCレイテンシーが増加するとします。この場合、値を`tidb_tso_client_batch_max_wait_time`に増やすと、TiDB での実行レイテンシーが増加し、クラスターの QPS パフォーマンスに影響する可能性があります。

### tidb_ttl_delete_rate_limit <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-rate-limit-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、各 TiDB ノードの TTL ジョブにおける`DELETE`ステートメントのレート制限に使用されます。この値は、TTL ジョブの単一ノードで 1 秒あたりに許可される`DELETE`ステートメントの最大数を表します。この変数を`0`に設定すると、制限は適用されません。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_delete_batch_size <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-ttl-delete-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `100`
-   範囲: `[1, 10240]`
-   この変数は、TTL ジョブ内の単一`DELETE`トランザクションで削除できる行の最大数を設定するために使用されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_delete_worker_count <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-ttl-delete-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各 TiDB ノード上の TTL ジョブの最大同時実行数を設定するために使用されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_job_enable <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-ttl-job-enable-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、TTL ジョブを有効にするかどうかを制御するために使用されます。 `OFF`に設定すると、TTL 属性を持つすべてのテーブルで期限切れのデータのクリーンアップが自動的に停止されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_scan_batch_size <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-ttl-scan-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `500`
-   範囲: `[1, 10240]`
-   この変数は、TTL ジョブで期限切れのデータをスキャンするために使用される各`SELECT`ステートメントの`LIMIT`値を設定するために使用されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_scan_worker_count <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-ttl-scan-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各 TiDB ノード上の TTL スキャン ジョブの最大同時実行数を設定するために使用されます。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_job_schedule_window_start_time <span class="version-mark">v6.5.0 の新</span>機能 {#tidb-ttl-job-schedule-window-start-time-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   クラスターに存続: はい
-   デフォルト値: `00:00 +0000`
-   この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの開始時間を制御するために使用されます。この変数の値を変更する場合、ウィンドウが小さいと期限切れのデータのクリーンアップが失敗する可能性があるので注意してください。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_job_schedule_window_end_time <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-schedule-window-end-time-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   クラスターに存続: はい
-   デフォルト値: `23:59 +0000`
-   この変数は、バックグラウンドでの TTL ジョブのスケジュール ウィンドウの終了時間を制御するために使用されます。この変数の値を変更する場合、ウィンドウが小さいと期限切れのデータのクリーンアップが失敗する可能性があるので注意してください。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_ttl_running_tasks <span class="version-mark">v7.0.0 の新</span>機能 {#tidb-ttl-running-tasks-span-class-version-mark-new-in-v7-0-0-span}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `-1` ～ `[1, 256]`
-   クラスター全体で実行中の TTL タスクの最大数を指定します。1 `-1` 、TTL タスクの数が TiKV ノードの数と等しいことを意味します。詳細については、 [有効期間](/time-to-live.md)を参照してください。

### tidb_txn_assertion_level <span class="version-mark">v6.0.0 の新</span>機能 {#tidb-txn-assertion-level-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: セッション | グローバル

-   クラスターに存続: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ

-   タイプ: 列挙

-   デフォルト値: `FAST`

-   可能`FAST` `STRICT` : `OFF`

-   この変数はアサーション レベルを制御するために使用されます。アサーションは、データとインデックス間の一貫性チェックであり、書き込まれるキーがトランザクション コミット プロセスに存在するかどうかをチェックします。詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。

    -   `OFF` : このチェックを無効にします。
    -   `FAST` : ほとんどのチェック項目を有効にしますが、パフォーマンスにはほとんど影響しません。
    -   `STRICT` : すべてのチェック項目を有効にします。システムのワークロードが高い場合、悲観的トランザクションのパフォーマンスにわずかな影響があります。

-   v6.0.0 以降のバージョンの新しいクラスターの場合、デフォルト値は`FAST`です。v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_txn_commit_batch_size <span class="version-mark">v6.2.0 の新</span>機能 {#tidb-txn-commit-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `16384`
-   範囲: `[1, 1073741824]`
-   単位: バイト

<CustomContent platform="tidb">

-   この変数は、TiDB が TiKV に送信するトランザクション コミット要求のバッチ サイズを制御するために使用されます。アプリケーション ワークロードのほとんどのトランザクションに大量の書き込み操作がある場合は、この変数をより大きな値に調整すると、バッチ処理のパフォーマンスが向上します。ただし、この変数が大きすぎる値に設定され、TiKV の[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)の制限を超えると、コミットが失敗する可能性があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB が TiKV に送信するトランザクション コミット要求のバッチ サイズを制御するために使用されます。アプリケーション ワークロードのほとんどのトランザクションに大量の書き込み操作がある場合は、この変数をより大きな値に調整すると、バッチ処理のパフォーマンスが向上します。ただし、この変数が大きすぎる値に設定され、TiKV の単一ログの最大サイズ (デフォルトでは 8 MiB) の制限を超えると、コミットが失敗する可能性があります。

</CustomContent>

### tidb_txn_モード {#tidb-txn-mode}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `pessimistic`
-   可能`optimistic`値: `pessimistic`
-   この変数はトランザクション モードを設定するために使用されます。TiDB 3.0 は悲観的トランザクションをサポートしています。TiDB 3.0.8 以降では、 [悲観的トランザクションモード](/pessimistic-transaction.md)がデフォルトで有効になっています。
-   TiDB を v3.0.7 以前のバージョンから v3.0.8 以降のバージョンにアップグレードした場合、デフォルトのトランザクション モードは変更されません。**新しく作成されたクラスターのみが、デフォルトで悲観的トランザクション モードを使用します**。
-   この変数が「楽観的」または「」に設定されている場合、 TiDB は[楽観的トランザクションモード](/optimistic-transaction.md)使用します。

### tidb_use_plan_baselines <span class="version-mark">v4.0 の新</span>機能 {#tidb-use-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、実行プラン バインディング機能を有効にするかどうかを制御するために使用されます。デフォルトでは有効になっていますが、値`OFF`を割り当てることで無効にすることができます。実行プラン バインディングの使用については、 [実行プランのバインディング](/sql-plan-management.md#create-a-binding)を参照してください。

### tidb_wait_split_region_finish {#tidb-wait-split-region-finish}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   通常、リージョンの分散には長い時間がかかります。これは、PD スケジューリングと TiKV ロードによって決まります。この変数は、 `SPLIT REGION`ステートメントの実行時にすべてのリージョンが完全に分散された後に結果をクライアントに返すかどうかを設定するために使用されます。
    -   `ON`では、すべての領域が分散されるまで`SPLIT REGIONS`ステートメントが待機する必要があります。
    -   `OFF` 、すべての領域の分散が完了する前に`SPLIT REGIONS`ステートメントが戻ることを許可します。
-   リージョンを分散させると、分散されているリージョンの書き込みおよび読み取りパフォーマンスが影響を受ける可能性があることに注意してください。バッチ書き込みまたはデータ インポートのシナリオでは、リージョンの分散が完了した後にデータをインポートすることをお勧めします。

### tidb_wait_split_region_timeout {#tidb-wait-split-region-timeout}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[1, 2147483647]`
-   単位: 秒
-   この変数は、 `SPLIT REGION`ステートメントを実行するためのタイムアウトを設定するために使用されます。指定された時間値内にステートメントが完全に実行されない場合は、タイムアウト エラーが返されます。

### tidb_window_concurrency <span class="version-mark">v4.0 の新</span>機能 {#tidb-window-concurrency-span-class-version-mark-new-in-v4-0-span}

> **警告：**
>
> v5.0 以降、この変数は非推奨です。代わりに、設定には[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)使用してください。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、ウィンドウ演算子の同時実行度を設定するために使用されます。
-   値`-1`は、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tiflash_fastscan <span class="version-mark">v6.3.0 の新</span>機能 {#tiflash-fastscan-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   [高速スキャン](/tiflash/use-fastscan.md)が有効になっている場合（ `ON`に設定）、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の正確性やデータの一貫性は保証されません。

### tiflash_fine_grained_shuffle_batch_size <span class="version-mark">v6.2.0 の新</span>機能 {#tiflash-fine-grained-shuffle-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `8192`
-   範囲: `[1, 18446744073709551615]`
-   Fine Grained Shuffle を有効にすると、 TiFlashにプッシュダウンされたウィンドウ関数を並列に実行できます。この変数は、送信者が送信するデータのバッチ サイズを制御します。
-   パフォーマンスへの影響: ビジネス要件に応じて適切なサイズを設定します。不適切な設定はパフォーマンスに影響します。値が小さすぎる場合 (たとえば`1` )、ブロックごとに 1 つのネットワーク転送が発生します。値が大きすぎる場合 (たとえば、テーブルの合計行数)、受信側はデータの待機にほとんどの時間を費やし、パイプライン計算が機能しなくなります。適切な値を設定するには、 TiFlashレシーバーが受信した行数の分布を観察できます。ほとんどのスレッドが数行 (たとえば数百行) のみを受信する場合は、この値を増やしてネットワーク オーバーヘッドを削減できます。

### tiflash_fine_grained_shuffle_stream_count <span class="version-mark">v6.2.0 の新機能</span> {#tiflash-fine-grained-shuffle-stream-count-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-1, 1024]`
-   ウィンドウ関数が実行のためにTiFlashにプッシュダウンされる場合、この変数を使用してウィンドウ関数実行の同時実行レベルを制御できます。可能な値は次のとおりです。

    -   -1: Fine Grained Shuffle 機能は無効ですTiFlashにプッシュダウンされたウィンドウ関数は、単一のスレッドで実行されます。
    -   0: 細粒度シャッフル機能が有効です。 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)が有効な値 (0 より大きい値) に設定されている場合、 `tiflash_fine_grained_shuffle_stream_count` [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)の値に設定されます。 それ以外の場合は、 TiFlashコンピューティング ノードの CPU リソースに基づいて自動的に推定されます。 TiFlashのウィンドウ関数の実際の同時実行レベルは、 min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノード上の物理スレッドの数) です。
    -   0 より大きい整数: 細粒度シャッフル機能が有効になりますTiFlashにプッシュダウンされたウィンドウ関数は、複数のスレッドで実行されます。同時実行レベルは、min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノード上の物理スレッドの数) です。
-   理論的には、ウィンドウ関数のパフォーマンスはこの値に比例して増加します。ただし、値が実際の物理スレッド数を超えると、パフォーマンスの低下につながります。

### tiflash_mem_quota_query_per_node <span class="version-mark">v7.4.0 の新</span>機能 {#tiflash-mem-quota-query-per-node-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashノードでのクエリの最大メモリ使用量を制限します。クエリのメモリ使用量がこの制限を超えると、 TiFlash はエラーを返し、クエリを終了します。この変数を`-1`または`0`に設定すると、制限なしになります。この変数を`0`より大きい値に設定し、 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)を有効な値に設定すると、 TiFlash は[クエリレベルのスピル](/tiflash/tiflash-spill-disk.md#query-level-spilling)有効にします。

### tiflash_query_spill_ratio <span class="version-mark">v7.4.0 の新</span>機能 {#tiflash-query-spill-ratio-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0, 0.85]`
-   この変数は、 TiFlash [クエリレベルのスピル](/tiflash/tiflash-spill-disk.md#query-level-spilling)のしきい値を制御します。3 `0` 、自動クエリ レベルのスピルを無効にすることを意味します。この変数が`0`より大きく、クエリのメモリ使用量が[`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) * `tiflash_query_spill_ratio`を超えると、 TiFlash はクエリ レベルのスピルをトリガーし、必要に応じてクエリでサポートされている演算子のデータをスピルします。

> **注記：**
>
> -   この変数は、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)が`0`より大きい場合にのみ有効になります。つまり、 [tiflash_mem_quota_query_per_node](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)が`0`または`-1`の場合、 `tiflash_query_spill_ratio`が`0`より大きい場合でも、クエリ レベルのスピルは有効になりません。
> -   TiFlashクエリ レベルのスピルが有効になっている場合、個々のTiFlash演算子のスピルしきい値は自動的に無効になります。つまり、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)と`tiflash_query_spill_ratio`両方が 0 より大きい場合、 [tidb_max_bytes_before_tiflash_external_sort](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700) 、 [tidb_max_bytes_before_tiflash_external_group_by](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) 、および[tidb_max_bytes_before_tiflash_external_join](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700) 3 つの変数は自動的に無効になり、これを`0`に設定するのと同じです。

### tiflash_replica_read <span class="version-mark">v7.3.0 の新</span>機能 {#tiflash-replica-read-span-class-version-mark-new-in-v7-3-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `all_replicas`
-   値のオプション: `all_replicas` `closest_adaptive`または`closest_replicas`
-   この変数は、クエリにTiFlashエンジンが必要な場合にTiFlashレプリカを選択するための戦略を設定するために使用されます。
    -   `all_replicas` 、分析コンピューティングに利用可能なすべてのTiFlashレプリカを使用することを意味します。
    -   `closest_adaptive`は、クエリを開始する TiDB ノードと同じゾーンのTiFlashレプリカを優先的に使用することを意味します。このゾーンのレプリカに必要なデータがすべて含まれていない場合、クエリには他のゾーンのTiFlashレプリカと、それに対応するTiFlashノードが含まれます。
    -   `closest_replicas` 、クエリを開始する TiDB ノードと同じゾーン内のTiFlashレプリカのみを使用することを意味します。このゾーン内のレプリカに必要なデータがすべて含まれていない場合、クエリはエラーを返します。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB ノードに[ゾーン属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)設定されておらず、 `tiflash_replica_read`が`all_replicas`に設定されていない場合、 TiFlashはレプリカ選択戦略を無視します。代わりに、クエリにすべてのTiFlashレプリカを使用し、 `The variable tiflash_replica_read is ignored.`警告を返します。
> -   TiFlashノードに[ゾーン属性](/schedule-replicas-by-topology-labels.md#configure-labels-for-tikv-and-tiflash)設定されていない場合、そのノードはどのゾーンにも属さないノードとして扱われます。

</CustomContent>

### tikv_client_read_timeout <span class="version-mark">v7.4.0 の新</span>機能 {#tikv-client-read-timeout-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   `tikv_client_read_timeout`使用すると、クエリで TiKV RPC 読み取り要求を送信する TiDB のタイムアウトを設定できます。TiDB クラスターが不安定なネットワークまたは深刻な TiKV I/Oレイテンシージッターのある環境にあり、アプリケーションが SQL クエリのレイテンシーに敏感な場合は、 `tikv_client_read_timeout`設定して TiKV RPC 読み取り要求のタイムアウトを短縮できます。この場合、TiKV ノードに I/Oレイテンシージッターがあると、TiDB はすぐにタイムアウトし、次の TiKVリージョンピアが配置されている TiKV ノードに RPC 要求を再送信できます。すべての TiKVリージョンピアの要求がタイムアウトすると、TiDB はデフォルトのタイムアウト (通常は 40 秒) で再試行します。
-   クエリでオプティマイザ ヒント`/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */`を使用して、TiDB が TiKV RPC 読み取り要求を送信するタイムアウトを設定することもできます。オプティマイザ ヒントとこのシステム変数の両方が設定されている場合、オプティマイザ ヒントが優先されます。
-   デフォルト値`0` 、デフォルトのタイムアウト (通常は 40 秒) が使用されることを示します。

> **注記：**
>
> -   通常、通常のクエリには数ミリ秒かかりますが、TiKV ノードが不安定なネットワークにある場合や I/O ジッターが発生する場合、クエリに 1 秒以上、場合によっては 10 秒以上かかることがあります。この場合、オプティマイザ ヒント`/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=100) */`を使用して、特定のクエリの TiKV RPC 読み取り要求タイムアウトを 100 ミリ秒に設定できます。このようにすると、TiKV ノードの応答が遅い場合でも、TiDB はすぐにタイムアウトし、次の TiKVリージョンピアが配置されている TiKV ノードに RPC 要求を再送信できます。2 つの TiKV ノードが同時に I/O ジッターが発生する可能性は低いため、クエリは通常、数ミリ秒から 110 ミリ秒以内に完了します。
> -   `tikv_client_read_timeout`にあまり小さい値（たとえば、1 ミリ秒）を設定しないでください。そうしないと、TiDB クラスターのワークロードが高いときに要求が簡単にタイムアウトし、その後の再試行によって TiDB クラスターの負荷がさらに増加する可能性があります。
> -   異なるタイプのクエリに異なるタイムアウト値を設定する必要がある場合は、オプティマイザーヒントを使用することをお勧めします。

### タイムゾーン {#time-zone}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `SYSTEM`
-   この変数は現在のタイムゾーンを返します。値は、「-8:00」などのオフセット、または「America/Los_Angeles」などの名前付きゾーンとして指定できます。
-   値`SYSTEM` 、タイム ゾーンがシステム ホストと同じである必要があることを意味します。これは、変数[`system_time_zone`](#system_time_zone)を介して利用できます。

### タイムスタンプ {#timestamp}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数の空でない値は、 `CURRENT_TIMESTAMP()` 、 `NOW()` 、およびその他の関数のタイムスタンプとして使用される UNIX エポックを示します。この変数は、データの復元またはレプリケーションに使用される場合があります。

### トランザクション分離 {#transaction-isolation}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `REPEATABLE-READ`
-   `REPEATABLE-READ` `READ-COMMITTED` `SERIALIZABLE` : `READ-UNCOMMITTED`
-   この変数はトランザクション分離を設定します。TiDB は MySQL との互換性のために`REPEATABLE-READ`宣言していますが、実際の分離レベルはスナップショット分離です。詳細については[トランザクション分離レベル](/transaction-isolation-levels.md)を参照してください。

### 送信分離 {#tx-isolation}

この変数は`transaction_isolation`の別名です。

### 送信分離ワンショット {#tx-isolation-one-shot}

> **注記：**
>
> この変数は TiDB で内部的に使用されます。ユーザーが使用することは想定されていません。

内部的には、TiDB パーサーは`SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]`ステートメントを`SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`に変換します。

### tx_read_ts {#tx-read-ts}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   ステイル読み取りシナリオでは、このセッション変数は、安定した読み取りタイムスタンプ値を記録するために使用されます。
-   この変数は TiDB の内部操作に使用されます。この変数を設定することは**お勧めしません**。

### トランザクションスコープ {#txn-scope}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `global`
-   値のオプション: `global`と`local`
-   この変数は、現在のセッション トランザクションがグローバル トランザクションであるかローカル トランザクションであるかを設定するために使用されます。
-   この変数は TiDB の内部操作に使用されます。この変数を設定することは**お勧めしません**。

### validate_password.check_user_name <span class="version-mark">v6.5.0 の新</span>機能 {#validate-password-check-user-name-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、パスワードの複雑さのチェックにおけるチェック項目です。パスワードがユーザー名と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効になります。
-   この変数が有効で`ON`に設定されている場合、パスワードを設定すると、TiDB はパスワードとユーザー名 (ホスト名を除く) を比較します。パスワードがユーザー名と一致する場合、パスワードは拒否されます。
-   この変数は[`validate_password.policy`](#validate_passwordpolicy-new-in-v650)とは独立しており、パスワードの複雑さのチェック レベルの影響を受けません。

### validate_password.dictionary <span class="version-mark">v6.5.0 の新</span>機能 {#validate-password-dictionary-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `""`
-   タイプ: 文字列
-   この変数は、パスワードの複雑さのチェックにおけるチェック項目です。パスワードが辞書と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`2` (STRONG) に設定されている場合にのみ有効になります。
-   この変数は 1024 文字以下の文字列です。パスワードに存在できない単語のリストが含まれます。各単語はセミコロン ( `;` ) で区切られます。
-   この変数はデフォルトで空の文字列に設定されており、辞書チェックは実行されません。辞書チェックを実行するには、文字列に一致させる単語を含める必要があります。この変数が設定されている場合、パスワードを設定すると、TiDB はパスワードの各サブ文字列 (長さ 4 ～ 100 文字) を辞書内の単語と比較します。パスワードのいずれかのサブ文字列が辞書内の単語と一致すると、パスワードは拒否されます。比較では大文字と小文字は区別されません。

### validate_password.enable <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-enable-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は常に[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)に対して有効です。

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数を`ON`に設定すると、パスワードを設定するときに TiDB はパスワードの複雑さのチェックを実行します。

### validate_password.length <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-length-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `8`
-   範囲: TiDBセルフホストの場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)場合`[8, 2147483647]` `[0, 2147483647]`
-   この変数は、パスワードの複雑さのチェックにおけるチェック項目です。パスワードの長さが十分かどうかをチェックします。デフォルトでは、パスワードの最小長は`8`です。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効になっている場合にのみ有効になります。
-   この変数の値は、式`validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`より小さくてはなりません。
-   式の値が`validate_password.length`より大きくなるように`validate_password.number_count` 、 `validate_password.special_char_count` 、または`validate_password.mixed_case_count`値を変更すると、 `validate_password.length`の値は式の値に合わせて自動的に変更されます。

### validate_password.mixed_case_count <span class="version-mark">v6.5.0 の新</span>機能 {#validate-password-mixed-case-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: TiDBセルフホストの場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)場合`[1, 2147483647]` `[0, 2147483647]`
-   この変数は、パスワードの複雑さチェックにおけるチェック項目です。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) `1` (MEDIUM) 以上に設定されている場合にのみ有効になります。
-   パスワード内の大文字の数も小文字の数も`validate_password.mixed_case_count`より少なくすることはできません。たとえば、変数が`1`に設定されている場合、パスワードには少なくとも 1 つの大文字と 1 つの小文字が含まれている必要があります。

### validate_password.number_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-number-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: TiDBセルフホストの場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)場合`[1, 2147483647]` `[0, 2147483647]`
-   この変数は、パスワードの複雑さのチェックにおけるチェック項目です。パスワードに十分な数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効になります。

### validate_password.policy <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-policy-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `1`
-   値のオプション: TiDBセルフホストの場合は`0` 、 `1` 、 `2` 、 [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) 、 `1` 、 `2`
-   この変数は、パスワードの複雑さのチェックのポリシーを制御します。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)有効になっている場合にのみ有効になります。この変数の値によって、 `validate_password.check_user_name`を除く他の`validate-password`つの変数がパスワードの複雑さのチェックで有効になるかどうかが決まります。
-   この変数の値は`0` 、 `1` 、または`2` (LOW、MEDIUM、STRONG に対応) になります。ポリシー レベルによってチェック内容が異なります。
    -   0 または LOW: パスワードの長さ。
    -   1 または MEDIUM: パスワードの長さ、大文字と小文字、数字、特殊文字。
    -   2 または強力: パスワードの長さ、大文字と小文字、数字、特殊文字、辞書の一致。

### validate_password.special_char_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-special-char-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: TiDBセルフホストの場合は[TiDB専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)場合`[1, 2147483647]` `[0, 2147483647]`
-   この変数は、パスワードの複雑さのチェックにおけるチェック項目です。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)が`1` (MEDIUM) 以上に設定されている場合にのみ有効になります。

### バージョン {#version}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `8.0.11-TiDB-` (tidb バージョン)
-   この変数は、MySQL のバージョンに続いて TiDB のバージョンを返します。たとえば、「8.0.11-TiDB-v7.5.1」などです。

### バージョンコメント {#version-comment}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: (文字列)
-   この変数は、TiDB バージョンに関する追加の詳細を返します。たとえば、「TiDB Server (Apache License 2.0) Community Edition、MySQL 8.0 互換」などです。

### バージョン_コンパイル_マシン {#version-compile-machine}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: (文字列)
-   この変数は、TiDB が実行されている CPUアーキテクチャの名前を返します。

### バージョン_コンパイル_os {#version-compile-os}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: (文字列)
-   この変数は、TiDB が実行されている OS の名前を返します。

### 待機タイムアウト {#wait-timeout}

> **注記：**
>
> この変数は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)の場合読み取り専用です。

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[0, 31536000]`
-   単位: 秒
-   この変数は、ユーザー セッションのアイドル タイムアウトを制御します。値が 0 の場合、無制限を意味します。

### 警告回数 {#warning-count}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `0`
-   この読み取り専用変数は、以前実行されたステートメントで発生した警告の数を示します。

### ウィンドウ使用高精度 {#windowing-use-high-precision}

-   範囲: セッション | グローバル
-   クラスターに存続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ウィンドウ関数を計算するときに高精度モードを使用するかどうかを制御します。
