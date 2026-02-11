---
title: System Variables
summary: システム変数を使用して、パフォーマンスを最適化したり、実行動作を変更したりします。
---

# システム変数 {#system-variables}

TiDB システム変数は、設定が`SESSION`または`GLOBAL`スコープに適用されるという点で、MySQL と同様に動作します。

-   スコープ`SESSION`の変更は現在のセッションにのみ影響します。
-   スコープ`GLOBAL`での変更は即時に適用されます。この変数のスコープが`SESSION`に設定されている場合、すべてのセッション（あなたのセッションを含む）は現在のセッション値を引き続き使用します。
-   変更は[`SET`ステートメント](/sql-statements/sql-statement-set-variable.md)を使用して行われます:

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
> いくつかの`GLOBAL`変数はTiDBクラスタに保持されます。このドキュメントの一部の変数には`Persists to cluster`設定されていますが、これは`Yes`または`No`に設定できます。
>
> -   `Persists to cluster: Yes`に設定されている変数の場合、グローバル変数が変更されると、すべての TiDB サーバーに通知が送信され、システム変数キャッシュが更新されます。TiDB サーバーを追加したり、既存の TiDB サーバーを再起動したりすると、保存された設定値が自動的に使用されます。
> -   `Persists to cluster: No`に設定されている変数の場合、変更は接続しているローカル TiDB インスタンスにのみ適用されます。設定された値を保持するには、 `tidb.toml`設定ファイルで変数を指定する必要があります。
>
> さらに、TiDBはいくつかのMySQL変数を読み取りと設定の両方が可能としています。これは互換性を保つために必要です。なぜなら、アプリケーションとコネクタの両方がMySQL変数を読み取ることは一般的だからです。例えば、JDBCコネクタは、その動作に依存していないにもかかわらず、クエリキャッシュ設定の読み取りと設定の両方を行います。

> **注記：**
>
> 値を大きくしても必ずしもパフォーマンスが向上するわけではありません。ほとんどの設定は各接続に適用されるため、ステートメントを実行している同時接続の数を考慮することも重要です。
>
> 安全な値を決定するときは、変数の単位を考慮してください。
>
> -   スレッドの場合、安全な値は通常、CPU コアの数までになります。
> -   バイトの場合、安全な値は通常、システムメモリの量よりも小さくなります。
> -   時間の場合、単位が秒またはミリ秒になる可能性があることに注意してください。
>
> 同じ単位を使用する変数は、同じリソース セットを競合する可能性があります。

バージョン7.4.0以降では、 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)を使用して、ステートメント実行中に一部の`SESSION`変数の値を一時的に変更できます。ステートメント実行後、現在のセッションのシステム変数の値は自動的に元の値に戻ります。このヒントは、オプティマイザーとエグゼキューターに関連する一部のシステム変数を変更するために使用できます。このドキュメントの変数には`Applies to hint SET_VAR`設定されており、 `Yes`または`No`に設定できます。

-   `Applies to hint SET_VAR: Yes`に設定された変数の場合、 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)ヒントを使用して、ステートメントの実行中に現在のセッションのシステム変数の値を変更できます。
-   `Applies to hint SET_VAR: No`に設定された変数の場合、ステートメントの実行中に[`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value)ヒントを使用して現在のセッションのシステム変数の値を変更することはできません。

`SET_VAR`ヒントの詳細については、 [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)参照してください。

## 変数参照 {#variable-reference}

### allow_auto_random_explicit_insert <span class="version-mark">v4.0.3 の新機能</span> {#allow-auto-random-explicit-insert-span-class-version-mark-new-in-v4-0-3-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `INSERT`ステートメントで`AUTO_RANDOM`属性を持つ列の値を明示的に指定できるようにするかどうかを決定します。

### authentication_ldap_sasl_auth_method_name<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `SCRAM-SHA-1`
-   可能な値: `SCRAM-SHA-1` 、 `SCRAM-SHA-256` 、および`GSSAPI` 。
-   LDAP SASL 認証の場合、この変数は認証方法の名前を指定します。

### authentication_ldap_sasl_bind_base_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL認証の場合、この変数は検索ツリー内の検索範囲を制限します。1節`AS ...`指定せずにユーザーが作成された場合、TiDBはユーザー名に基づいてLDAPサーバー内の`dn`を自動的に検索します。

### authentication_ldap_sasl_bind_root_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。

### authentication_ldap_sasl_bind_root_pwd<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。

### authentication_ldap_sasl_ca_path<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は StartTLS 接続の証明機関ファイルの絶対パスを指定します。

### authentication_ldap_sasl_init_pool_size<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーへの接続プール内の初期接続を指定します。

### authentication_ldap_sasl_max_pool_size<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーへの接続プールの最大接続数を指定します。

### authentication_ldap_sasl_server_host<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP SASL 認証の場合、この変数は LDAPサーバーのホスト名または IP アドレスを指定します。

### authentication_ldap_sasl_server_port<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP SASL 認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### authentication_ldap_sasl_tls<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-sasl-tls-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP SASL 認証の場合、この変数はプラグインによる LDAPサーバーへの接続が StartTLS で保護されるかどうかを制御します。

### authentication_ldap_simple_auth_method_name<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-auth-method-name-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `SIMPLE`
-   可能な値: `SIMPLE` 。
-   LDAP簡易認証の場合、この変数は認証方式名を指定します。サポートされる値は`SIMPLE`です。

### authentication_ldap_simple_bind_base_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-bind-base-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP簡易認証の場合、この変数は検索ツリー内の検索範囲を制限します。1節`AS ...`指定せずにユーザーが作成された場合、TiDBはユーザー名に基づいてLDAPサーバー内の`dn`を自動的に検索します。

### authentication_ldap_simple_bind_root_dn<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-bind-root-dn-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は、ユーザーを検索するために LDAPサーバーにログインするために使用される`dn`指定します。

### authentication_ldap_simple_bind_root_pwd<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-bind-root-pwd-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数はユーザーを検索するために LDAPサーバーにログインするために使用されるパスワードを指定します。

### authentication_ldap_simple_ca_path<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-ca-path-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は StartTLS 接続の証明機関ファイルの絶対パスを指定します。

### authentication_ldap_simple_init_pool_size<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-init-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 32767]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーへの接続プール内の初期接続を指定します。

### authentication_ldap_simple_max_pool_size<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-max-pool-size-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[1, 32767]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーへの接続プールの最大接続数を指定します。

### authentication_ldap_simple_server_host<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-server-host-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   LDAP 簡易認証の場合、この変数は LDAPサーバーのホスト名または IP アドレスを指定します。

### authentication_ldap_simple_server_port<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-server-port-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `389`
-   範囲: `[1, 65535]`
-   LDAP 簡易認証の場合、この変数は LDAPサーバーの TCP/IP ポート番号を指定します。

### authentication_ldap_simple_tls<span class="version-mark">バージョン7.1.0の新機能</span> {#authentication-ldap-simple-tls-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   LDAP 簡易認証の場合、この変数は、プラグインによる LDAPサーバーへの接続が StartTLS で保護されるかどうかを制御します。

### 自動インクリメント {#auto-increment-increment}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てる`AUTO_INCREMENT`値のステップサイズと、 `AUTO_RANDOM` IDの割り当てルールを制御します。多くの場合、 [`auto_increment_offset`](#auto_increment_offset)と組み合わせて使用​​されます。

### 自動インクリメントオフセット {#auto-increment-offset}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 65535]`
-   列に割り当てる`AUTO_INCREMENT`値の初期オフセットと、 `AUTO_RANDOM` IDの割り当てルールを制御します。この設定は、多くの場合、 [`auto_increment_increment`](#auto_increment_increment)と組み合わせて使用​​されます。例：

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

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   明示的なトランザクションに含まれていない場合に、ステートメントを自動的にコミットするかどうかを制御します。詳細については[トランザクションの概要](/transaction-overview.md#autocommit)参照してください。

### ブロック暗号化モード {#block-encryption-mode}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `aes-128-ecb`
-   `aes-256-cbc` `aes-128-cbc` `aes-256-ecb` `aes-192-cbc` `aes-128-ecb` `aes-192-ecb` `aes-128-ofb` `aes-192-ofb` `aes-256-ofb` `aes-128-cfb` `aes-192-cfb` `aes-256-cfb`
-   この変数は、組み込み関数[`AES_ENCRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_encrypt)および[`AES_DECRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_decrypt)の暗号化モードを設定します。

### 文字セットクライアント {#character-set-client}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   クライアントから送信されるデータの文字セット。TiDBにおける文字セットと照合順序の使用に関する詳細は[文字セットと照合順序](/character-set-and-collation.md)参照してください。必要に応じて文字セットを変更するには、 [`SET NAMES`](/sql-statements/sql-statement-set-names.md)使用することをお勧めします。

### 文字セット接続 {#character-set-connection}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   指定された文字セットを持たない文字列リテラルの文字セット。

### 文字セットデータベース {#character-set-database}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   この変数は、使用中のデフォルトデータベースの文字セットを示します。**この変数を設定することは推奨されません**。新しいデフォルトデータベースが選択されると、サーバーはこの変数の値を変更します。

### 文字セット結果 {#character-set-results}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   データがクライアントに送信されるときに使用される文字セット。

### 文字セットサーバー {#character-set-server}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4`
-   サーバーのデフォルトの文字セット。

### 照合接続 {#collation-connection}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4_bin`
-   この変数は、現在の接続で使用されている照合順序を示します。これはMySQL変数`collation_connection`と一致します。

### 照合データベース {#collation-database}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4_bin`
-   この変数は、使用中のデータベースのデフォルトの照合照合順序を示します。**この変数を設定することは推奨されません**。新しいデータベースが選択されると、TiDBはこの変数の値を変更します。

### 照合サーバー {#collation-server}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `utf8mb4_bin`
-   データベースの作成時に使用されるデフォルトの照合照合順序。

### cte_max_recursion_depth {#cte-max-recursion-depth}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1000`
-   範囲: `[0, 4294967295]`
-   共通テーブル式の最大再帰深度を制御します。

### データディレクトリ {#datadir}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)ではサポートされていません。

<CustomContent platform="tidb">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値:コンポーネントと展開方法によって異なります。
    -   `/tmp/tidb` : [`--store`](/command-line-flags-for-tidb-configuration.md#--store)に`"unistore"`設定した場合、または`--store`設定しない場合。
    -   `${pd-ip}:${pd-port}` : Kubernetes デプロイメントのTiUPおよびTiDB Operator のデフォルトのstorageエンジンである TiKV を使用する場合。
-   この変数は、データが保存されている場所を示します。この場所はローカルパス`/tmp/tidb` 、またはデータがTiKVに保存されている場合はPDサーバーを指すことができます。値が`${pd-ip}:${pd-port}`の場合は、TiDBが起動時に接続するPDサーバーを示します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値:コンポーネントと展開方法によって異なります。
    -   `/tmp/tidb` : [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store)に`"unistore"`設定した場合、または`--store`設定しない場合。
    -   `${pd-ip}:${pd-port}` : Kubernetes デプロイメントのTiUPおよびTiDB Operator のデフォルトのstorageエンジンである TiKV を使用する場合。
-   この変数は、データが保存されている場所を示します。この場所はローカルパス`/tmp/tidb` 、またはデータがTiKVに保存されている場合はPDサーバーを指すことができます。値が`${pd-ip}:${pd-port}`の場合は、TiDBが起動時に接続するPDサーバーを示します。

</CustomContent>

### ddl_slow_threshold {#ddl-slow-threshold}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   実行時間がしきい値を超える DDL 操作をログに記録します。

### デフォルト認証プラグイン {#default-authentication-plugin}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `mysql_native_password`
-   可能な値`tidb_auth_token` `mysql_native_password` `tidb_sm3_password` `caching_sha2_password` `authentication_ldap_sasl` `authentication_ldap_simple`
-   この変数は、サーバーとクライアント間の接続が確立されるときにサーバーが通知する認証方法を設定します。
-   `tidb_sm3_password`方式を使用して認証するには、 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3)を使用して TiDB に接続できます。

<CustomContent platform="tidb">

この変数の可能な値の詳細については、 [認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status)参照してください。

</CustomContent>

### default_collat​​ion_for_utf8mb4<span class="version-mark">バージョン7.4.0の新機能</span> {#default-collation-for-utf8mb4-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: グローバル | セッション
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: `utf8mb4_bin`
-   `utf8mb4_0900_ai_ci` `utf8mb4_general_ci`オプション: `utf8mb4_bin`
-   この変数は、 `utf8mb4`文字セットのデフォルトである[照合順序](/character-set-and-collation.md)を設定するために使用されます。これは、以下のステートメントの動作に影響します。
    -   ステートメント[`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)および[`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)に表示されるデフォルトの照合順序。
    -   [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)および[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)ステートメントに、照合順序を指定せずにテーブルまたは列に対して`CHARACTER SET utf8mb4`節が含まれている場合、この変数で指定された照合順序が使用されます。これは、 `CHARACTER SET`節が使用されていない場合の動作には影響しません。
    -   [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)と[`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)ステートメントに照合順序を指定せずに`CHARACTER SET utf8mb4`句が含まれている場合、この変数で指定された照合順序が使用されます。これは、 `CHARACTER SET`番目の句が使用されていない場合の動作には影響しません。
    -   `COLLATE`句が使用されていない場合、 `_utf8mb4'string'`形式のすべてのリテラル文字列では、この変数によって指定された照合順序が使用されます。

### default_password_lifetime <span class="version-mark">v6.5.0 の新機能</span> {#default-password-lifetime-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 65535]`
-   パスワードの自動有効期限に関するグローバルポリシーを設定します。デフォルト値`0` 、パスワードの有効期限がないことを示します。このシステム変数を正の整数`N`に設定すると、パスワードの有効期間は`N`日間となり、 `N`日以内にパスワードを変更する必要があります。

### デフォルトの週の形式 {#default-week-format}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 7]`
-   `WEEK()`関数で使用される週の形式を設定します。

### パスワードの有効期限が切れた場合の切断<span class="version-mark">v6.5.0 の新機能</span> {#disconnect-on-expired-password-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は読み取り専用です。パスワードの有効期限が切れたときにTiDBがクライアント接続を切断するかどうかを示します。変数が`ON`に設定されている場合、パスワードの有効期限が切れるとクライアント接続は切断されます。変数が`OFF`に設定されている場合、クライアント接続は「サンドボックスモード」に制限され、ユーザーはパスワードリセット操作のみを実行できます。

<CustomContent platform="tidb">

-   期限切れのパスワードに対するクライアント接続の動作を変更する必要がある場合は、構成ファイル内の[`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)構成項目を変更します。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   期限切れのパスワードに対するクライアント接続のデフォルトの動作を変更する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してください。

</CustomContent>

### div_precision_increment<span class="version-mark">バージョン8.0.0の新機能</span> {#div-precision-increment-span-class-version-mark-new-in-v8-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[0, 30]`
-   この変数は、 `/`演算子を用いた除算の結果のスケールを何桁増やすかを指定します。この変数はMySQLと同じです。

### エラー数 {#error-count}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   メッセージを生成した最後のステートメントから発生したエラーの数を示す読み取り専用変数。

### 外部キーチェック {#foreign-key-checks}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: v6.6.0 より前のバージョンのデフォルト値は`OFF`です。v6.6.0 以降のバージョンのデフォルト値は`ON`です。
-   この変数は、外部キー制約チェックを有効にするかどうかを制御します。

### グループ連結最大長 {#group-concat-max-len}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[4, 18446744073709551615]`
-   `GROUP_CONCAT()`関数内の項目の最大バッファ サイズ。

### openssl がある {#have-openssl}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQLとの互換性のための読み取り専用変数。サーバーでTLSが有効になっている場合、サーバーによって`YES`に設定されます。

### SSLがある {#have-ssl}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `DISABLED`
-   MySQLとの互換性のための読み取り専用変数。サーバーでTLSが有効になっている場合、サーバーによって`YES`に設定されます。

### ホスト名 {#hostname}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: (システムホスト名)
-   読み取り専用変数としての TiDBサーバーのホスト名。

### アイデンティティ<span class="version-mark">v5.3.0 の新機能</span> {#identity-span-class-version-mark-new-in-v5-3-0-span}

この変数は[`last_insert_id`](#last_insert_id)の別名です。

### 初期化接続 {#init-connect}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   `init_connect`機能は、TiDBサーバーへの初回接続時に SQL 文を自動的に実行することを許可します。3 または`CONNECTION_ADMIN` `SUPER`権限がある場合、この`init_connect`文は実行されません。9 `init_connect`文でエラーが発生した場合、ユーザー接続は終了します。

### innodb_lock_wait_timeout {#innodb-lock-wait-timeout}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `50`
-   範囲: `[1, 3600]`
-   単位: 秒
-   悲観的トランザクションのロック待機タイムアウト (デフォルト)。

### インタラクティブタイムアウト {#interactive-timeout}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[1, 31536000]`
-   単位: 秒
-   この変数は、対話型ユーザーセッションのアイドルタイムアウトを表します。対話型ユーザーセッションとは、 `CLIENT_INTERACTIVE`オプション（例えば、MySQL ShellとMySQL Client）を使用して[`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) APIを呼び出すことによって確立されたセッションを指します。この変数はMySQLと完全に互換性があります。

### 最後の挿入ID {#last-insert-id}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、挿入ステートメントによって生成された最後の`AUTO_INCREMENT`または`AUTO_RANDOM`値を返します。
-   `last_insert_id`の値は、関数`LAST_INSERT_ID()`によって返される値と同じです。

### last_plan_from_binding <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-binding-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   この変数は、前の文で使用された実行計画が[計画の拘束](/sql-plan-management.md)影響を受けたかどうかを示すために使用されます。

### last_plan_from_cache <span class="version-mark">v4.0 の新機能</span> {#last-plan-from-cache-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   この変数は、前の`execute`ステートメントで使用された実行プランがプラン キャッシュから直接取得されたかどうかを示すために使用されます。

### last_sql_use_alloc <span class="version-mark">v6.4.0 の新機能</span> {#last-sql-use-alloc-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   この変数は読み取り専用です。前の文がキャッシュされたチャンクオブジェクト（チャンク割り当て）を使用したかどうかを示すために使用されます。

### ライセンス {#license}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `Apache License 2.0`
-   この変数は、TiDBサーバーインストールのライセンスを示します。

### max_allowed_pa​​cket <span class="version-mark">v6.1.0 の新機能</span> {#max-allowed-packet-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `67108864`
-   範囲: `[1024, 1073741824]`
-   値は1024の倍数である必要があります。値が1024で割り切れない場合は警告が表示され、値は切り捨てられます。例えば、値が1025に設定されている場合、TiDB内の実際の値は1024です。
-   1 回のパケット送信でサーバーとクライアントが許可する最大パケット サイズ。
-   `SESSION`スコープでは、この変数は読み取り専用です。
-   この変数は MySQL と互換性があります。

### password_history<span class="version-mark">バージョン6.5.0の新機能</span> {#password-history-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、パスワード再利用ポリシーを設定するために使用されます。このポリシーにより、TiDBはパスワード変更回数に基づいてパスワードの再利用を制限できます。デフォルト値`0`パスワード変更回数に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数を正の整数`N`に設定すると、過去`N`のパスワードの再利用は許可されません。

### mpp_exchange_compression_mode <span class="version-mark">v6.6.0 の新機能</span> {#mpp-exchange-compression-mode-span-class-version-mark-new-in-v6-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `UNSPECIFIED`
-   `UNSPECIFIED` `FAST` `HIGH_COMPRESSION` : `NONE`
-   この変数は、MPP Exchange演算子のデータ圧縮モードを指定するために使用されます。この変数は、TiDBがバージョン番号`1`のMPP実行プランを選択した場合に有効になります。変数値の意味は以下のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。TiDBは圧縮モードを自動的に選択します。現在、TiDBは`FAST`モードを自動的に選択します。
    -   `NONE` : データ圧縮は使用されません。
    -   `FAST` : 高速モード。全体的なパフォーマンスは良好で、圧縮率は`HIGH_COMPRESSION`未満です。
    -   `HIGH_COMPRESSION` : 高圧縮比モード。

### mpp_version <span class="version-mark">v6.6.0 の新機能</span> {#mpp-version-span-class-version-mark-new-in-v6-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `UNSPECIFIED`
-   `2` `0` `1` : `UNSPECIFIED`
-   この変数は、MPP実行プランの異なるバージョンを指定するために使用されます。バージョンが指定されると、TiDBは指定されたバージョンのMPP実行プランを選択します。変数値の意味は以下のとおりです。
    -   `UNSPECIFIED` : 未指定を意味します。TiDB は自動的に最新バージョン`2`を選択します。
    -   `0` : すべての TiDB クラスタバージョンと互換性があります。MPP バージョンが`0`より大きい機能は、このモードでは機能しません。
    -   `1` : v6.6.0 の新機能TiFlash上で圧縮されたデータ交換を可能にするために使用されます。詳細は[MPPバージョンと交換データ圧縮](/explain-mpp.md#mpp-version-and-exchange-data-compression)参照してください。
    -   `2` : v7.3.0 の新機能。MPP タスクがTiFlashでエラーに遭遇したときに、より正確なエラー メッセージを提供するために使用されます。

### password_reuse_interval <span class="version-mark">v6.5.0 の新機能</span> {#password-reuse-interval-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 4294967295]`
-   この変数は、TiDBが経過時間に基づいてパスワードの再利用を制限するためのパスワード再利用ポリシーを設定するために使用されます。デフォルト値`0` 、経過時間に基づくパスワード再利用ポリシーを無効にすることを意味します。この変数を正の整数`N`に設定すると、過去`N`日間に使用されたパスワードの再利用は許可されません。

### 最大接続数 {#max-connections}

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 100000]`
-   単一のTiDBインスタンスに許可される同時接続の最大数。この変数はリソース制御に使用できます。
-   デフォルト値`0`は無制限を意味します。この変数の値が`0`より大きく、接続数がその値に達すると、TiDBサーバーはクライアントからの新規接続を拒否します。

### 最大実行時間 {#max-execution-time}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   ステートメントの最大実行時間。デフォルト値は無制限（ゼロ）です。

> **注記：**
>
> v6.4.0より前では、システム変数`max_execution_time`はすべての種類のステートメントに適用されます。v6.4.0以降では、この変数は`SELECT`ステートメントの最大実行時間のみを制御します。タイムアウト値の精度は約100ミリ秒です。つまり、ステートメントは指定したミリ秒数で正確に終了しない可能性があります。

<CustomContent platform="tidb">

ヒント[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)が指定されたSQL文の場合、その文の最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、 [SQL FAQで](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement)で説明したSQLバインディングでも使用できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

ヒント[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)が指定されたSQL文の場合、その文の最大実行時間は、この変数ではなくヒントによって制限されます。ヒントは、 [SQL FAQで](https://docs.pingcap.com/tidb/stable/sql-faq)で説明したSQLバインディングでも使用できます。

</CustomContent>

### 最大準備済みステートメント数 {#max-prepared-stmt-count}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 1048576]`
-   現在の TiDB インスタンス内の[`PREPARE`](/sql-statements/sql-statement-prepare.md)ステートメントの最大数を指定します。
-   値`-1`は、現在の TiDB インスタンス内のステートメントの最大数`PREPARE`に制限がないことを意味します。
-   変数を上限`1048576`超える値に設定すると、代わりに`1048576`使用されます。

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
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、アクティブPDFollower機能（現在はリージョン情報のリクエストにのみ適用されます）を有効にするかどうかを制御します。値が`OFF`の場合、TiDBはPDリーダーからのみリージョン情報を取得します。値が`ON`の場合、TiDBはリージョン情報のリクエストをすべてのPDサーバーに均等に分散し、PDフォロワーもリージョンリクエストを処理できるため、PDリーダーのCPU負荷が軽減されます。
-   アクティブ PDFollowerを有効にするシナリオ:
    -   多数のリージョンを持つクラスターでは、ハートビートの処理とタスクのスケジュール設定によるオーバーヘッドの増加により、PD リーダーの CPU 負荷が高くなります。
    -   多数の TiDB インスタンスを含む TiDB クラスターでは、リージョン情報に対する要求の同時性が高いため、PD リーダーの CPU 負荷が高くなります。

### プラグインディレクトリ {#plugin-dir}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)ではサポートされていません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   コマンドラインフラグで指定されたプラグインをロードするディレクトリを示します。

### プラグインロード {#plugin-load}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)ではサポートされていません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   TiDB の起動時にロードするプラグインを指定します。これらのプラグインはコマンドラインフラグで指定し、カンマで区切ります。

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

### require_secure_transport <span class="version-mark">v6.1.0 の新機能</span> {#require-secure-transport-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> 現在、この変数は[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)ではサポートされていません。TiDB TiDB Cloud Dedicated クラスタではこの変数を有効にし**ないで**ください。有効にしないと、SQL クライアント接続エラーが発生する可能性があります。この制限は一時的な制御手段であり、将来のリリースで解決される予定です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: TiDB Self-Managed の場合は`OFF`および[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) [TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 、 `ON`

<CustomContent platform="tidb">

-   この変数は、TiDBへのすべての接続がローカルソケットまたはTLSを使用することを保証します。詳細については[TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB へのすべての接続がローカル ソケット上にあるか、TLS を使用していることを保証します。

</CustomContent>

-   この変数を`ON`に設定すると、TLSが有効になっているセッションからTiDBに接続する必要があります。これにより、TLSが正しく設定されていない場合に発生するロックアウトシナリオを回避できます。
-   この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。
-   v6.5.6、v7.1.2、v7.5.1、v8.0.0 以降では、Security拡張モード (SEM) が有効になっている場合、ユーザーの接続の問題が発生する可能性を回避するために、この変数を`ON`に設定することは禁止されています。

### skip_name_resolve <span class="version-mark">v5.2.0 の新機能</span> {#skip-name-resolve-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `tidb-server`インスタンスが接続ハンドシェイクの一部としてホスト名を解決するかどうかを制御します。
-   DNS が信頼できない場合は、このオプションを有効にしてネットワーク パフォーマンスを向上させることができます。

> **注記：**
>
> `skip_name_resolve=ON`の場合、アイデンティティにホスト名を持つユーザーはサーバーにログインできなくなります。例:
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

### sql_mode {#sql-mode}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
-   この変数は、MySQLの互換性に関するいくつかの動作を制御します。詳細については[SQLモード](/sql-mode.md)参照してください。

### sql_require_primary_key<span class="version-mark">バージョン6.3.0の新機能</span> {#sql-require-primary-key-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、テーブルに主キーが必要であるという要件を強制するかどうかを制御します。この変数を有効にすると、主キーのないテーブルを作成または変更しようとするとエラーが発生します。
-   この機能は、MySQL 8.0 の同様の名前の[`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key)に基づいています。
-   TiCDCを使用する場合は、この変数を有効にすることを強くお勧めします。これは、MySQLシンクへの変更をレプリケーションするには、テーブルに主キーが必要であるためです。

<CustomContent platform="tidb">

-   この変数を有効にし、TiDBデータ移行（DM）を使用してデータを移行する場合は、 [DM タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)の`session`部分に`sql_require_ primary_key`加算して`OFF`に設定することをお勧めします。そうしないと、DMはタスクの作成に失敗します。

</CustomContent>

### sql_select_limit <span class="version-mark">v4.0.2 の新機能</span> {#sql-select-limit-span-class-version-mark-new-in-v4-0-2-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
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
-   証明機関ファイルの場所（存在する場合）。この変数の値は、TiDB構成項目[`ssl-ca`](/tidb-configuration-file.md#ssl-ca)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   証明機関ファイルの場所（存在する場合）。この変数の値は、TiDB構成項目[`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca)によって定義されます。

</CustomContent>

### ssl_cert {#ssl-cert}

<CustomContent platform="tidb">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS接続に使用される証明書ファイル（存在する場合）の場所。この変数の値は、TiDB構成項目[`ssl-cert`](/tidb-configuration-file.md#ssl-cert)によって定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS接続に使用される証明書ファイル（存在する場合）の場所。この変数の値は、TiDB構成項目[`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert)によって定義されます。

</CustomContent>

### SSLキー {#ssl-key}

<CustomContent platform="tidb">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS接続に使用される秘密鍵ファイル（存在する場合）の場所。この変数の値は、TiDB構成項目[`ssl-key`](/tidb-configuration-file.md#ssl-cert)で定義されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   SSL/TLS接続に使用される秘密鍵ファイル（存在する場合）の場所。この変数の値は、TiDB構成項目[`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key)で定義されます。

</CustomContent>

### システムタイムゾーン {#system-time-zone}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: (システム依存)
-   この変数は、TiDBが最初にブートストラップされた時点のシステムタイムゾーンを示します。1 [`time_zone`](#time_zone)参照してください。

### tidb_adaptive_closest_read_threshold <span class="version-mark">v6.3.0 の新機能</span> {#tidb-adaptive-closest-read-threshold-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4096`
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、 [`tidb_replica_read`](#tidb_replica_read-new-in-v40) `closest-adaptive`に設定した場合に、TiDBサーバーが同じアベイラビリティゾーンにあるレプリカに読み取りリクエストを送信する際のしきい値を制御するために使用されます。推定結果がこのしきい値以上の場合、TiDB は同じアベイラビリティゾーンにあるレプリカに読み取りリクエストを送信することを優先します。それ以外の場合、TiDB はリーダーレプリカに読み取りリクエストを送信します。

### tidb_advancer_check_point_lag_limit <span class="version-mark">v8.5.5 の新機能</span> {#tidb-advancer-check-point-lag-limit-span-class-version-mark-new-in-v8-5-5-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 期間
-   デフォルト値: `48h0m0s`
-   範囲: `[1s, 8760h0m0s]`
-   この変数は、ログバックアップタスクの最大許容チェックポイントラグを制御します。タスクのチェックポイントラグがこの制限を超えると、TiDB Advancer はタスクを一時停止します。

### tidb_allow_tiflash_cop<span class="version-mark">バージョン7.3.0の新機能</span> {#tidb-allow-tiflash-cop-span-class-version-mark-new-in-v7-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   TiDBが計算タスクをTiFlashにプッシュダウンする場合、Cop、BatchCop、MPPの3つの方法（プロトコル）から選択できます。CopやBatchCopと比較して、MPPプロトコルはより成熟しており、タスクとリソースの管理が優れています。したがって、MPPプロトコルの使用が推奨されます。
    -   `0`または`OFF` : オプティマイザーはTiFlash MPP プロトコルを使用してのみプランを生成します。
    -   `1`または`ON` : オプティマイザーは、コスト見積もりに基づいて実行プランを生成するために Cop、BatchCop、または MPP プロトコルを使用するかどうかを決定します。

### tidb_allow_batch_cop <span class="version-mark">v4.0 の新機能</span> {#tidb-allow-batch-cop-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   この変数は、TiDBがTiFlashにコプロセッサ要求を送信する方法を制御するために使用されます。以下の値を持ちます。

    -   `0` : リクエストをバッチで送信しない
    -   `1` :集計と参加のリクエストはバッチで送信されます
    -   `2` : すべてのコプロセッサ要求はバッチで送信されます

### tidb_allow_fallback_to_tikv<span class="version-mark">バージョン5.0の新機能</span> {#tidb-allow-fallback-to-tikv-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: &quot;&quot;
-   この変数は、TiKVにフォールバックする可能性のあるstorageエンジンのリストを指定するために使用されます。リスト内の指定されたstorageエンジンの障害によりSQL文の実行が失敗した場合、TiDBはTiKVを使用してこのSQL文の実行を再試行します。この変数は &quot;&quot; または &quot;tiflash&quot; に設定できます。この変数が &quot;tiflash&quot; に設定されている場合、 TiFlashがタイムアウトエラー（エラーコード：ErrTiFlashServerTimeout）を返すと、TiDBはTiKVを使用してこのSQL文の実行を再試行します。

### tidb_allow_function_for_expression_index<span class="version-mark">バージョン5.2.0の新機能</span> {#tidb-allow-function-for-expression-index-span-class-version-mark-new-in-v5-2-0-span}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_schema_valid, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash`
-   この読み取り専用変数は、 [表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index)作成に使用できる関数を表示するために使用されます。

### tidb_allow_mpp<span class="version-mark">バージョン5.0の新機能</span> {#tidb-allow-mpp-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   クエリ実行時にTiFlashのMPPモードを使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF`場合、MPPモードは使用されません。v7.3.0以降のバージョンでは、この変数の値を`0`または`OFF`に設定する場合は、変数[`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730)も有効にする必要があります。有効にしないと、クエリでエラーが返される可能性があります。
    -   `1`または`ON` 。これは、オプティマイザーがコスト推定に基づいて MPP モードを使用するかどうかを決定することを意味します (デフォルト)。

MPPは、 TiFlashエンジンが提供する分散コンピューティングフレームワークであり、ノード間のデータ交換を可能にし、高性能かつ高スループットのSQLアルゴリズムを提供します。MPPモードの選択の詳細については、 [MPPモードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)を参照してください。

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
-   この変数は、列の`AUTO_INCREMENT`のプロパティを`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`ステートメントの実行で削除することを許可するかどうかを設定するために使用されます。デフォルトでは許可されていません。

### tidb_analyze_column_options <span class="version-mark">v8.3.0 の新機能</span> {#tidb-analyze-column-options-span-class-version-mark-new-in-v8-3-0-span}

> **注記：**
>
> -   この変数は[`tidb_analyze_version`](#tidb_analyze_version-new-in-v510) `2`に設定されている場合にのみ機能します。
> -   TiDB クラスターを v8.3.0 より前のバージョンから v8.3.0 以降にアップグレードする場合、元の動作を維持するために、この変数はデフォルトで`ALL`に設定されます。
> -   v8.3.0 から v8.5.4 に新しくデプロイされた TiDB クラスターの場合、この変数はデフォルトで`PREDICATE`に設定されます。
> -   v8.5.5 以降に新しくデプロイされた TiDB クラスターの場合、この変数はデフォルトで`ALL`に設定されます。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `ALL`
-   値`PREDICATE`オプション: `ALL`
-   この変数は、 `ANALYZE TABLE`ステートメントの動作を制御します。 `PREDICATE`に設定すると、 [述語列](/statistics.md#collect-statistics-on-some-columns)の統計のみが収集されます。 `ALL`に設定すると、すべての列の統計が収集されます。OLAPクエリを使用するシナリオでは、 `ALL`に設定することをお勧めします。そうしないと、統計の収集によってクエリのパフォーマンスが大幅に低下する可能性があります。

### tidb_analyze_distsql_scan_concurrency <span class="version-mark">v7.6.0 の新機能</span> {#tidb-analyze-distsql-scan-concurrency-span-class-version-mark-new-in-v7-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[0, 4294967295]` 。v8.2.0より前のバージョンでは、最小値は`1`です。5 `0`設定すると、クラスターのサイズに基づいて同時実行性が適応的に調整されます。
-   この変数は、 `ANALYZE`操作を実行するときに`scan`操作の同時実行性を設定するために使用されます。

### tidb_analyze_partition_concurrency {#tidb-analyze-partition-concurrency}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `2` 。v7.4.0 以前のバージョンではデフォルト値は`1`です。
-   範囲: `[1, 128]` 。v8.4.0 より前では、値の範囲は`[1, 18446744073709551615]`です。
-   この変数は、TiDB がパーティションテーブルを分析するときに、収集された統計を書き込む同時実行性を指​​定します。

### tidb_analyze_version <span class="version-mark">v5.1.0 の新機能</span> {#tidb-analyze-version-span-class-version-mark-new-in-v5-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   TiDB が統計を収集する方法を制御します。
    -   TiDB Self-Managed の場合、この変数のデフォルト値は、v5.3.0 以降、 `1`から`2`に変更されます。
    -   TiDB Cloudの場合、この変数のデフォルト値は、v6.5.0 以降、 `1`から`2`に変更されます。
    -   クラスターが以前のバージョンからアップグレードされた場合、アップグレード後もデフォルト値`tidb_analyze_version`は変更されません。
-   この変数の詳細な説明については[統計入門](/statistics.md)参照してください。

### tidb_analyze_skip_column_types <span class="version-mark">v7.2.0 の新機能</span> {#tidb-analyze-skip-column-types-span-class-version-mark-new-in-v7-2-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: 「json、blob、mediumblob、longblob、mediumtext、longtext」。 v8.2.0 より前のデフォルト値は「json,blob,mediumblob,longblob」です。
-   可能な値: &quot;json、blob、mediumblob、longblob、text、mediumtext、longtext&quot;
-   この変数は、統計情報を収集するコマンド`ANALYZE`を実行する際に、統計収集からどのタイプの列をスキップするかを制御します。この変数は`tidb_analyze_version = 2`にのみ適用されます。 `ANALYZE TABLE t COLUMNS c1, ... , cn`を使用して列を指定しても、その列の型が`tidb_analyze_skip_column_types`に該当する場合、その列の統計は収集されません。

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
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 2147483647]`
-   この変数は、TiDB クラスター内で同時に実行できる自動分析操作の数を制御します。v8.4.0 より前のバージョンでは、この同時実行数は 1 に固定されています。統計収集タスクを高速化するには、クラスター内の利用可能なリソースに応じてこの同時実行数を増やすことができます。

### tidb_auto_analyze_end_time {#tidb-auto-analyze-end-time}

-   範囲: グローバル

-   クラスターに持続: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ

-   タイプ: 時間

-   デフォルト値: `23:59 +0000`

-   この変数は、統計情報の自動更新を許可する時間帯を制限するために使用されます。例えば、UTC時間で午前1時から午前3時までの間のみ統計情報の自動更新を許可するには、次のように設定します。

    -   `tidb_auto_analyze_start_time='01:00 +0000'`
    -   `tidb_auto_analyze_end_time='03:00 +0000'`

-   パラメータの時刻にタイムゾーン情報が含まれている場合、そのタイムゾーンが解析に使用されます。含まれていない場合は、現在のセッションで`time_zone`に指定されたタイムゾーンが使用されます。例えば、 `01:00 +0000` UTCの午前1時を表します。

### tidb_auto_analyze_partition_batch_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-auto-analyze-partition-batch-size-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値： `8192` 。v7.6.0より前のバージョンでは、デフォルト値は`1`です。v7.6.0からv8.1.xのバージョンでは、デフォルト値は`128`です。v8.2.0以降では、デフォルト値は`8192`に変更されます。
-   範囲: `[1, 8192]` 。v8.2.0 より前では、値の範囲は`[1, 1024]`です。
-   この変数は、パーティションテーブルを分析するときに TiDB [自動的に分析する](/statistics.md#automatic-update)が実行するパーティションの数を指定します (つまり、パーティションテーブルで統計情報を自動的に収集します)。
-   この変数の値がパーティション数より小さい場合、TiDBはパーティションテーブルのすべてのパーティションを複数のバッチで自動的に分析します。この変数の値がパーティション数以上の場合、TiDBはパーティションテーブルのすべてのパーティションを同時に分析します。
-   パーティションテーブルのパーティション数がこの変数値よりもはるかに多く、自動分析に時間がかかる場合は、この変数の値を増やして時間の消費を減らすことができます。

### tidb_auto_analyze_ratio {#tidb-auto-analyze-ratio}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.5`
-   範囲: `(0, 1]` 。v8.0.0 以前のバージョンの範囲は`[0, 18446744073709551615]`です。
-   この変数は、TiDBがバックグラウンド[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)でテーブル統計情報を更新するために自動分析を実行する際のしきい値を設定するために使用されます。例えば、値が0.5の場合、テーブル内の行の50%以上が変更された時点で自動分析がトリガーされます。自動分析の実行を特定の時間帯のみに制限するには、 `tidb_auto_analyze_start_time`と`tidb_auto_analyze_end_time`指定します。

> **注記：**
>
> この機能を使用するには、システム変数`tidb_enable_auto_analyze` `ON`に設定する必要があります。

### tidb_auto_analyze_start_time {#tidb-auto-analyze-start-time}

-   範囲: グローバル

-   クラスターに持続: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ

-   タイプ: 時間

-   デフォルト値: `00:00 +0000`

-   この変数は、統計情報の自動更新を許可する時間帯を制限するために使用されます。例えば、UTC時間で午前1時から午前3時までの間のみ統計情報の自動更新を許可するには、次のように設定します。

    -   `tidb_auto_analyze_start_time='01:00 +0000'`
    -   `tidb_auto_analyze_end_time='03:00 +0000'`

-   パラメータの時刻にタイムゾーン情報が含まれている場合、そのタイムゾーンが解析に使用されます。含まれていない場合は、現在のセッションで`time_zone`に指定されたタイムゾーンが使用されます。例えば、 `01:00 +0000` UTCの午前1時を表します。

### tidb_auto_build_stats_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-auto-build-stats-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   この変数は、統計の自動更新の実行の同時性を設定するために使用されます。

### tidb_backoff_lock_fast {#tidb-backoff-lock-fast}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[1, 2147483647]`
-   この変数は、読み取り要求がロックに遭遇する`backoff`回目を設定するために使用されます。

### tidb_backoff_weight {#tidb-backoff-weight}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB `backoff`の最大再試行待機時間、つまり内部ネットワークまたはその他のコンポーネント（TiKV、PD）の障害発生時に再試行要求を送信する際の最大再試行待機時間の重み付けを増加させるために使用されます。この変数は最大再試行待機時間を調整するために使用でき、最小値は`1`です。

    例えば、TiDBがTiKVからKVを取得する際の基本再試行待機時間は15秒です。1 `tidb_backoff_weight = 2`場合、KV取得の最大再試行待機時間は、*基本時間×2＝30秒*となります。

    ネットワーク環境が悪い場合、この変数の値を適切に増やすことで、タイムアウトによるアプリケーション側へのエラー報告を効果的に軽減できます。アプリケーション側でエラー情報をより早く受け取りたい場合は、この変数の値を最小にしてください。

<CustomContent platform="tidb">

> **注記：**
>
> このシステム変数は、TSOリクエストの非同期取得には**適用されません**。TSO取得のタイムアウトを調整するには、設定項目[`pd-server-timeout`](/tidb-configuration-file.md#pd-server-timeout)を設定してください。

</CustomContent>

### tidb_batch_commit {#tidb-batch-commit}

> **警告：**
>
> この変数を有効にすることはお勧めし**ません**。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のバッチコミット機能を有効にするかどうかを制御するために使用されます。この変数を有効にすると、いくつかのステートメントをグループ化することでトランザクションが複数のトランザクションに分割され、非アトミックにコミットされる可能性がありますが、これは推奨されません。

### tidb_batch_delete {#tidb-batch-delete}

> **警告：**
>
> この変数は非推奨のbatch-dml機能に関連付けられており、データ破損を引き起こす可能性があります。そのため、batch-dmlでこの変数を有効にすることは推奨されません。代わりに[非トランザクションDML](/non-transactional-dml.md)使用してください。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のbatch-dml機能の一部であるbatch-delete機能を有効にするかどうかを制御します。この変数を有効にすると、 `DELETE`ステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを動作させるには、 `tidb_enable_batch_dml`有効にし、 `tidb_dml_batch_size`に正の値を設定する必要がありますが、これは推奨されません。

### tidb_batch_insert {#tidb-batch-insert}

> **警告：**
>
> この変数は非推奨のbatch-dml機能に関連付けられており、データ破損を引き起こす可能性があります。そのため、batch-dmlでこの変数を有効にすることは推奨されません。代わりに[非トランザクションDML](/non-transactional-dml.md)使用してください。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のbatch-dml機能の一部であるbatch-insert機能を有効にするかどうかを制御するために使用します。この変数を有効にすると、 `INSERT`ステートメントが複数のトランザクションに分割され、非アトミックにコミットされる可能性があります。これを動作させるには、 `tidb_enable_batch_dml`有効にし、 `tidb_dml_batch_size`に正の値を設定する必要がありますが、これは推奨されません。

### tidb_batch_pending_tiflash_count<span class="version-mark">バージョン6.0の新機能</span> {#tidb-batch-pending-tiflash-count-span-class-version-mark-new-in-v6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4000`
-   範囲: `[0, 4294967295]`
-   `ALTER DATABASE SET TIFLASH REPLICA`使用してTiFlashレプリカを追加する場合、許可される使用不可テーブルの最大数を指定します。使用不可テーブルの数がこの制限を超えると、操作が停止するか、残りのテーブルに対するTiFlashレプリカの設定に非常に時間がかかります。

### tidb_broadcast_join_threshold_count<span class="version-mark">バージョン5.0の新機能</span> {#tidb-broadcast-join-threshold-count-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `10240`
-   範囲: `[0, 9223372036854775807]`
-   単位: 行
-   結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを推定できません。この場合、サイズは結果セットの行数によって決定されます。サブクエリの推定行数がこの変数の値より少ない場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。
-   この変数は、 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)有効になった後は有効になりません。

### tidb_broadcast_join_threshold_size<span class="version-mark">バージョン5.0の新機能</span> {#tidb-broadcast-join-threshold-size-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `104857600` (100 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   テーブルサイズが変数の値より小さい場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。
-   この変数は、 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)有効になった後は有効になりません。

### tidb_build_stats_concurrency {#tidb-build-stats-concurrency}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2` 。v7.4.0 以前のバージョンではデフォルト値は`4`です。
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `ANALYZE`ステートメントを実行する同時実行性を設定するために使用されます。
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_build_sampling_stats_concurrency <span class="version-mark">v7.5.0 の新機能</span> {#tidb-build-sampling-stats-concurrency-span-class-version-mark-new-in-v7-5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   単位: スレッド
-   デフォルト値: `2`
-   範囲: `[1, 256]`
-   この変数は、 `ANALYZE`プロセスでのサンプリングの同時実行性を設定するために使用されます。
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_capture_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-capture-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [ベースラインキャプチャ](/sql-plan-management.md#baseline-capturing)機能を有効にするかどうかを制御するために使用します。この機能はステートメントサマリーに依存するため、ベースラインキャプチャを使用する前にステートメントサマリーを有効にする必要があります。
-   この機能を有効にすると、ステートメント サマリー内の履歴 SQL ステートメントが定期的に走査され、少なくとも 2 回出現する SQL ステートメントに対してバインディングが自動的に作成されます。

### tidb_cdc_write_source <span class="version-mark">v6.5.0 の新機能</span> {#tidb-cdc-write-source-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   スコープ: セッション
-   クラスターに持続: いいえ
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数が0以外の値に設定されている場合、このセッションで書き込まれたデータはTiCDCによって書き込まれたものとみなされます。この変数はTiCDCによってのみ変更できます。いかなる場合でも、この変数を手動で変更しないでください。

### tidb_check_mb4_value_in_utf8 {#tidb-check-mb4-value-in-utf8}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `utf8`文字セットに[基本多言語面（BMP）](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane)セットの値のみを格納するように強制するために使用されます。BMP以外の文字を格納するには、 `utf8mb4`文字セットを使用することをお勧めします。
-   `utf8`チェックが緩やかだった以前のバージョンのTiDBからクラスターをアップグレードする場合は、このオプションを無効にする必要がある場合があります。詳細については、 [アップグレード後のよくある質問](https://docs.pingcap.com/tidb/stable/upgrade-faq)参照してください。

### tidb_checksum_table_concurrency {#tidb-checksum-table-concurrency}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)ステートメントを実行するスキャン インデックスの同時実行性を設定するために使用されます。
-   変数を大きな値に設定すると、他のクエリの実行パフォーマンスに影響します。

### tidb_committer_concurrency <span class="version-mark">v6.1.0 の新機能</span> {#tidb-committer-concurrency-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `128`
-   範囲: `[1, 10000]`
-   単一トランザクションのコミット フェーズでコミットの実行に関連する要求の goroutine の数。
-   コミットするトランザクションが大きすぎる場合、トランザクションのコミット時にフロー制御キューの待機時間が長くなりすぎる可能性があります。このような場合は、設定値を増やすことでコミットを高速化できます。
-   この設定は以前は`tidb.toml`オプション ( `performance.committer-concurrency` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_config {#tidb-config}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   この変数は読み取り専用です。現在のTiDBサーバーの設定情報を取得するために使用されます。

### tidb_constraint_check_in_place {#tidb-constraint-check-in-place}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は楽観的トランザクションにのみ適用されます。悲観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-new-in-v630)使用してください。
-   この変数を`OFF`に設定すると、一意のインデックスにおける重複値のチェックはトランザクションがコミットされるまで延期されます。これはパフォーマンスの向上に役立ちますが、一部のアプリケーションでは予期しない動作となる可能性があります。詳細は[制約](/constraints.md#optimistic-transactions)参照してください。

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

-   デフォルト値: デフォルトでは、設定項目[`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)は`true`ているため、この変数のデフォルト値は`ON`です。7 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) `false`に設定されている場合、この変数のデフォルト値は`OFF`です。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`

</CustomContent>

-   この変数は悲観的トランザクションにのみ適用されます。楽観的トランザクションの場合は、代わりに[`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place)使用してください。
-   この変数を`OFF`に設定すると、TiDB はユニークインデックスのユニーク制約チェックを延期します（インデックスへのロックを必要とするステートメントを次回実行するとき、またはトランザクションをコミットするときまで）。これはパフォーマンスの向上に役立ちますが、一部のアプリケーションでは予期しない動作になる可能性があります。詳細は[制約](/constraints.md#pessimistic-transactions)参照してください。
-   この変数を無効にすると、TiDBは悲観的トランザクションでエラー`LazyUniquenessCheckFailure`を返す可能性があります。このエラーが発生した場合、TiDBは現在のトランザクションをロールバックします。
-   この変数が無効になっている場合、悲観的トランザクションで[`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)使用できません。
-   この変数が無効になっている場合、悲観的トランザクションをコミットするとエラー`Write conflict`または`Duplicate entry`が返される可能性があります。このようなエラーが発生した場合、TiDBは現在のトランザクションをロールバックします。

    -   `tidb_constraint_check_in_place_pessimistic` 〜 `OFF`に設定し、悲観的トランザクションを使用する場合:

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

    -   `tidb_constraint_check_in_place_pessimistic` 〜 `ON`に設定し、悲観的トランザクションを使用する場合:

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

            ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'

### tidb_cost_model_version <span class="version-mark">v6.2.0 の新機能</span> {#tidb-cost-model-version-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> -   TiDB v6.5.0以降、新規作成されたクラスターはデフォルトでコストモデルバージョン2を使用します。v6.5.0より前のTiDBバージョンからv6.5.0以降にアップグレードした場合、 `tidb_cost_model_version`値は変更されません。
> -   コスト モデルのバージョンを切り替えると、クエリ プランが変更される可能性があります。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `2`
-   値のオプション:
    -   `1` : TiDB v6.4.0 以前のバージョンでデフォルトで使用されるコスト モデル バージョン 1 を有効にします。
    -   `2` : [コストモデル バージョン 2](/cost-model.md#cost-model-version-2)を有効にします。これは TiDB v6.5.0 で一般に利用可能であり、内部テストではバージョン 1 よりも正確です。
-   コストモデルのバージョンはオプティマイザの計画決定に影響します。詳細については[コストモデル](/cost-model.md)参照してください。

### tidb_current_ts {#tidb-current-ts}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は読み取り専用です。現在のトランザクションのタイムスタンプを取得するために使用されます。

### tidb_ddl_disk_quota <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-disk-quota-span-class-version-mark-new-in-v6-3-0-span}

<CustomContent platform="tidb-cloud" plan="starter,essential">

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> この変数は[TiDB Cloudプレミアム](https://docs-preview.pingcap.com/tidbcloud/tidb-cloud-intro/#deployment-options)の場合読み取り専用です。

</CustomContent>

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `107374182400` (100 GiB)
-   範囲: `[107374182400, 1125899906842624]` ([100 GiB、1 PiB])
-   単位: バイト
-   この変数は[`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630)有効な場合にのみ有効になります。インデックス作成時のバックフィルにおけるローカルstorageの使用制限を設定します。

### tidb_ddl_enable_fast_reorg<span class="version-mark">バージョン6.3.0の新機能</span> {#tidb-ddl-enable-fast-reorg-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> -   [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)クラスターを使用している場合、この変数を使用してインデックス作成の速度を向上させるには、TiDB クラスターが AWS でホストされており、TiDB ノードのサイズが少なくとも 8 vCPU であることを確認してください。
> -   4つのvCPUを搭載したクラスタ[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合、インデックス作成時にリソース制限がクラスタの安定性に影響を与えないように、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)手動で無効にすることをお勧めします。この設定を無効にすると、トランザクションを使用してインデックスを作成できるようになり、クラスタ全体への影響が軽減されます。
> -   クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合、この変数は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックス作成時のバックフィル速度を向上させるために、 `ADD INDEX`と`CREATE INDEX`のアクセラレーションを有効にするかどうかを制御します。この変数値を`ON`に設定すると、大量のデータを持つテーブルでのインデックス作成のパフォーマンスが向上します。
-   バージョン7.1.0以降、インデックス高速化操作はチェックポイントをサポートします。TiDBオーナーノードが再起動されたり、障害により変更されたりした場合でも、TiDBは定期的に自動更新されるチェックポイントから進捗状況を回復できます。
-   完了した`ADD INDEX`操作が高速化されているかどうかを確認するには、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)ステートメントを実行して、 `JOB_TYPE`列に`ingest`が表示されるかどうかを確認します。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、この変数は読み取り専用です。変更が必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)ご連絡ください。

</CustomContent>

<CustomContent platform="tidb">

> **注記：**
>
> -   インデックス高速化には、書き込み可能で十分な空き容量のある[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)が必要です。3 `temp-dir`使用できない場合、TiDBは高速化されていないインデックス構築にフォールバックします。5 `temp-dir` SSDディスクに配置することをお勧めします。
>
> -   TiDBをv6.5.0以降にアップグレードする前に、TiDBの[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)のパスがSSDディスクに正しくマウントされているかどうかを確認することをお勧めします。TiDBを実行するオペレーティングシステムユーザーに、このディレクトリへの読み取りおよび書き込み権限があることを確認してください。権限がない場合、DDL操作で予期しない問題が発生する可能性があります。このパスはTiDBの設定項目であり、TiDBの再起動後に有効になります。そのため、アップグレード前にこの設定項目を設定しておくことで、再度の再起動を回避できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> 現在、この機能は[1つの`ALTER TABLE`文で複数の列またはインデックスを変更する](/sql-statements/sql-statement-alter-table.md)と完全に互換性がありません。インデックスアクセラレーションを使用して一意のインデックスを追加する場合、同じステートメント内で他の列やインデックスを変更しないようにする必要があります。

</CustomContent>

### tidb_stats_update_during_ddl <span class="version-mark">v8.5.4 の新機能</span> {#tidb-stats-update-during-ddl-span-class-version-mark-new-in-v8-5-4-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `OFF`
-   この変数は、DDL埋め込み`ANALYZE`有効にするかどうかを制御します。有効にすると、新しいインデックスを作成するDDL文（ [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) ）または既存のインデックスを再編成するDDL文（ [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)および[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) ）は、インデックスが可視になる前に自動的に統計情報を収集します。詳細については、 [DDL文に埋め込まれた`ANALYZE`](/ddl_embedded_analyze.md)参照してください。

### tidb_enable_dist_task <span class="version-mark">v7.1.0 の新機能</span> {#tidb-enable-dist-task-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   この変数は、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)を有効にするかどうかを制御するために使用されます。フレームワークを有効にすると、DDLやインポートなどのDXFタスクは、クラスター内の複数のTiDBノードによって分散実行され、完了します。
-   TiDB v7.1.0 以降、DXF はパーティション化されたテーブルに対して[`ADD INDEX`](/sql-statements/sql-statement-add-index.md)ステートメントを分散して実行することをサポートします。
-   TiDB v7.2.0 以降、DXF はインポート ジョブの[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)ステートメントの分散実行をサポートします。
-   TiDB v8.1.0以降では、この変数はデフォルトで有効になっています。DXFが有効になっているクラスターをv8.1.0以降にアップグレードする場合は、アップグレード前にDXFを無効（ `tidb_enable_dist_task`を`OFF`に設定）にしてください。これにより、アップグレード中に`ADD INDEX`操作が発生し、データインデックスの不整合が発生するのを回避できます。アップグレード後に、DXFを手動で有効にすることができます。
-   この変数は`tidb_ddl_distribute_reorg`から名前が変更されました。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、この変数は読み取り専用です。変更が必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)ご連絡ください。

</CustomContent>

### tidb_cloud_storage_uri <span class="version-mark">v7.4.0 の新機能</span> {#tidb-cloud-storage-uri-span-class-version-mark-new-in-v7-4-0-span}

> **注記：**
>
> 現在、 [グローバルソート](/tidb-global-sort.md)プロセスはTiDBノードの計算リソースとメモリリソースを大量に消費しています。ユーザーの業務アプリケーションの実行中にオンラインでインデックスを追加するなどのシナリオでは、クラスターに新しいTiDBノードを追加し、これらのノードに[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)変数を設定し、これらのノードに接続してタスクを作成することをお勧めします。これにより、分散フレームワークはこれらのノードにタスクをスケジュールし、他のTiDBノードからのワークロードを分離することで、 `ADD INDEX`や`IMPORT INTO`などのバックエンドタスクの実行がユーザーの業務アプリケーションに与える影響を軽減します。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `""`
-   この変数は、Amazon S3クラウドstorageのURIを指定して[グローバルソート](/tidb-global-sort.md)有効にするために使用されます。3 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)有効にすると、URIを設定し、storageへのアクセスに必要な権限を持つ適切なクラウドstorageパスを指定することで、グローバルソート機能を使用できるようになります。詳細については、 [Amazon S3 URI 形式](/external-storage-uri.md#amazon-s3-uri-format)参照してください。
-   次のステートメントでは、グローバル ソート機能を使用できます。
    -   [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)のステートメント。
    -   インポート ジョブの[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)のステートメント。

### tidb_ddl_error_count_limit {#tidb-ddl-error-count-limit}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `512`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、DDL操作が失敗した場合の再試行回数を設定するために使用されます。再試行回数がパラメータ値を超えると、誤ったDDL操作はキャンセルされます。

### tidb_ddl_flashback_concurrency <span class="version-mark">v6.3.0 の新機能</span> {#tidb-ddl-flashback-concurrency-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `64`
-   範囲: `[1, 256]`
-   この変数は[`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)の同時実行性を制御します。

### tidb_ddl_reorg_batch_size {#tidb-ddl-reorg-batch-size}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `256`
-   範囲: `[32, 10240]`
-   単位: 行
-   この変数は、DDL操作のフェーズ`re-organize`におけるバッチサイズを設定するために使用されます。例えば、TiDBがフェーズ`ADD INDEX`を実行する場合、インデックスデータは`tidb_ddl_reorg_worker_cnt` （number）の同時ワーカーによってバックフィルされる必要があります。各ワーカーは、インデックスデータをバッチでバックフィルします。
    -   `tidb_ddl_enable_fast_reorg` `OFF`に設定した場合、 `ADD INDEX`トランザクションとして実行されます。11 `ADD INDEX`実行中に、対象列に`UPDATE`や`REPLACE`などの更新操作が多数発生する場合、バッチサイズが大きいほどトランザクションの競合が発生する可能性が高くなります。このような場合は、バッチサイズを小さく設定することをお勧めします。最小値は 32 です。
    -   トランザクションの競合がない場合、または`tidb_ddl_enable_fast_reorg` `ON`に設定されている場合は、バッチサイズを大きく設定できます。これによりデータのバックフィルは高速化されますが、TiKVへの書き込み負荷も増加します。適切なバッチサイズについては、 `tidb_ddl_reorg_worker_cnt`の値も参照する必要があります。参考として[オンラインワークロードと`ADD INDEX`操作のインタラクションテスト](https://docs.pingcap.com/tidb/dev/online-workloads-and-add-index-operations)参照してください。
    -   バージョン8.3.0以降、このパラメータはSESSIONレベルでサポートされます。GLOBALレベルでパラメータを変更しても、現在実行中のDDL文には影響しません。新しいセッションで送信されるDDLにのみ適用されます。
    -   v8.5.0以降では、 `ADMIN ALTER DDL JOBS <job_id> BATCH_SIZE = <new_batch_size>;`実行することで実行中のDDLジョブに対してこのパラメータを変更できます。v8.5.5より前のTiDBバージョンでは、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)有効になっている場合、 `ADD INDEX` DDLではこの操作はサポートされませんのでご注意ください。詳細については、 [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)参照してください。

### tidb_ddl_reorg_priority {#tidb-ddl-reorg-priority}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `PRIORITY_LOW`
-   `PRIORITY_HIGH` `PRIORITY_NORMAL`オプション: `PRIORITY_LOW`
-   この変数は、第`re-organize`フェーズで第`ADD INDEX`操作を実行する優先度を設定するために使用されます。
-   この変数の値は`PRIORITY_LOW` 、 `PRIORITY_NORMAL`または`PRIORITY_HIGH`に設定できます。

### tidb_ddl_reorg_max_write_speed <span class="version-mark">v6.5.12、v7.5.5、v8.5.0 の新機能</span> {#tidb-ddl-reorg-max-write-speed-span-class-version-mark-new-in-v6-5-12-v7-5-5-and-v8-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: `0`
-   範囲: `[0, 1PiB]`
-   この変数は、インデックスのバックフィル中に、**単一のTiDBノードから単一のTiKVノードへの**書き込み帯域幅を制限します。これは、インデックス作成アクセラレーションが有効になっている場合（変数[`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630)で制御）にのみ有効になります。5 [グローバルソート](/tidb-global-sort.md)有効になっている場合、複数のTiDBノードがTiKVに同時に書き込みを行う可能性があることに注意してください。クラスター内のデータサイズが非常に大きい場合（数十億行など）、インデックス作成時の書き込み帯域幅を制限することで、アプリケーションのワークロードへの影響を効果的に軽減できます。
-   デフォルト値`0`は書き込み帯域幅の制限がないことを意味します。
-   この変数の値は、単位付きでも単位なしでも指定できます。
    -   単位なしで値を指定した場合、デフォルトの単位は1秒あたりのバイト数です。たとえば、 `67108864` 1秒あたり`64MiB`を表します。
    -   単位付きで値を指定する場合、サポートされる単位はKiB、MiB、GiB、TiBです。例えば、 `'1GiB` 」は1秒あたり1GiB、 `'256MiB'` 256MiB/秒を表します。

例：

4つのTiDBノードと複数のTiKVノードを持つクラスターがあると仮定します。このクラスターでは、各TiDBノードがインデックスのバックフィルを実行でき、リージョンはすべてのTiKVノードに均等に分散されます`tidb_ddl_reorg_max_write_speed`を`100MiB`に設定すると、次のようになります。

-   グローバルソートが無効になっている場合、TiKVへの書き込みは一度に1つのTiDBノードのみから行われます。この場合、TiKVノードあたりの最大書き込み帯域幅は`100MiB`です。
-   グローバルソートを有効にすると、4つのTiDBノードすべてが同時にTiKVに書き込むことができます。この場合、TiKVノードあたりの最大書き込み帯域幅は`4 * 100MiB = 400MiB`です。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、この変数は適切な値に自動的に調整され、ユーザーが変更することはできません。設定を調整する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

</CustomContent>

### tidb_ddl_reorg_worker_cnt {#tidb-ddl-reorg-worker-cnt}

<CustomContent platform="tidb-cloud">

<CustomContent plan="starter,essential">

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

</CustomContent>

<CustomContent plan="premium">

> **注記：**
>
> TiDB Cloud Premium の場合、この TiDB 変数を変更すると、 `MODIFY COLUMN` DDL ジョブにのみ反映され、 `ADD INDEX` DDL ジョブには影響しません。

</CustomContent>

</CustomContent>

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、第`re-organize`フェーズでの DDL 操作の同時実行性を設定するために使用されます。
-   バージョン8.3.0以降、このパラメータはSESSIONレベルでサポートされます。GLOBALレベルでパラメータを変更しても、現在実行中のDDL文には影響しません。新しいセッションで送信されるDDLにのみ適用されます。
-   v8.5.0以降では、 `ADMIN ALTER DDL JOBS <job_id> THREAD = <new_thread_count>;`実行することで実行中のDDLジョブに対してこのパラメータを変更できます。v8.5.5より前のTiDBバージョンでは、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)有効になっている場合、 `ADD INDEX` DDLではこの操作はサポートされませんのでご注意ください。詳細については、 [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)参照してください。

### <code>tidb_enable_fast_create_table</code><span class="version-mark">バージョン8.0.0の新機能</span> {#code-tidb-enable-fast-create-table-code-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON` 。v8.5.0 より前では、デフォルト値は`OFF`です。
-   この変数は[TiDB 高速テーブル作成](/accelerated-table-creation.md)有効にするかどうかを制御するために使用されます。
-   v8.0.0 以降、TiDB は`tidb_enable_fast_create_table`を使用した[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)ステートメントによるテーブル作成の高速化をサポートしています。
-   この変数は、v7.6.0で導入された変数[`tidb_ddl_version`](https://docs-archive.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760)から名前が変更されました。v8.0.0以降では、 `tidb_ddl_version`無効になります。
-   TiDB v8.5.0以降、新規作成されたクラスターでは高速テーブル作成機能がデフォルトで有効になり、 `tidb_enable_fast_create_table`が`ON`に設定されます。v8.4.0以前のバージョンからアップグレードされたクラスターでは、デフォルト値の`tidb_enable_fast_create_table`は変更されません。

### tidb_default_string_match_selectivity <span class="version-mark">v6.2.0 の新機能</span> {#tidb-default-string-match-selectivity-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   デフォルト値: `0.8`
-   範囲: `[0, 1]`
-   この変数は、行数を推定する際に、フィルター条件における`like` 、 `rlike` 、 `regexp`関数のデフォルトの選択度を設定するために使用されます。また、これらの関数の推定を支援するためにTopNを有効にするかどうかも制御します。
-   TiDBは、フィルタ条件の`like`統計情報を用いて推定しようとします。しかし、 `like`複雑な文字列に一致する場合や、 `rlike`や`regexp`を使用する場合、TiDBは統計情報を十分に活用できないことが多く、代わりにデフォルト値の`0.8`が選択率として設定され、結果として不正確な推定値となります。
-   この変数は、前述の動作を変更するために使用されます。この変数が`0`以外の値に設定されている場合、選択率は`0.8`ではなく、指定された変数値になります。
-   変数を`0`に設定すると、TiDB は統計において TopN を使用して評価することで精度を向上させ、前述の 3 つの関数を評価する際に統計における NULL 値を考慮します。前提条件として、 [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510) `2`に設定して統計情報を収集する必要があります。このような評価はパフォーマンスに若干の影響を与える可能性があります。
-   変数が`0.8`以外の値に設定されている場合、TiDB はそれに応じて`not like` 、 `not rlike` 、 `not regexp`の推定値を調整します。

### tidb_disable_txn_auto_retry {#tidb-disable-txn-auto-retry}

> **警告：**
>
> バージョン8.0.0以降、この変数は非推奨となり、TiDBは楽観的トランザクションの自動再試行をサポートしなくなりました。代替策として、楽観的的トランザクションの競合が発生した場合は、エラーをキャプチャしてアプリケーション内でトランザクションを再試行するか、代わりに[悲観的なトランザクションモード](/pessimistic-transaction.md)使用してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、明示的な楽観的トランザクションの自動再試行を無効にするかどうかを設定するために使用されます。デフォルト値の`ON`は、TiDBでトランザクションが自動的に再試行されないことを意味します。3 `COMMIT`場合、ステートメントはアプリケーションレイヤーで処理する必要があるエラーを返す可能性があります。

    値を`OFF`に設定すると、TiDBはトランザクションを自動的に再試行し、 `COMMIT`ステートメントからのエラーが少なくなります。この変更を行う際は、更新内容が失われる可能性があるため、ご注意ください。

    この変数は、TiDB内で自動的にコミットされる暗黙的なトランザクションと内部的に実行されるトランザクションには影響しません。これらのトランザクションの最大再試行回数は、値`tidb_retry_limit`によって決定されます。

    詳細については[再試行の限界](/optimistic-transaction.md#limits-of-retry)参照してください。

    <CustomContent platform="tidb">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は[`max_retry_count`](/tidb-configuration-file.md#max-retry-count)で制御されます。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。悲観的トランザクションの再試行回数は256回です。

    </CustomContent>

### tidb_distsql_scan_concurrency {#tidb-distsql-scan-concurrency}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `15`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `scan`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。
-   OLAP シナリオの場合、最大値はすべての TiKV ノードの CPU コアの数を超えてはなりません。
-   テーブルに多数のパーティションがある場合は、TiKV がメモリ不足 (OOM) になるのを避けるために、変数値を適切に減らすことができます (スキャンするデータのサイズとスキャンの頻度によって決まります)。
-   `LIMIT`句のみを含む単純なクエリの場合、 `LIMIT`値が 100000 未満であれば、TiKV にプッシュダウンされたスキャン操作では、この変数の値が`1`として扱われ、実行効率が向上します。
-   `SELECT MAX/MIN(col) FROM ...`クエリの場合、 `col`列のインデックスが`MAX(col)`または`MIN(col)`関数で必要な順序と同じ順序でソートされている場合、TiDB はクエリを`SELECT col FROM ... LIMIT 1`に書き換えて処理し、この変数の値も`1`として処理されます。例えば`SELECT MIN(col) FROM ...`の場合、 `col`列に昇順のインデックスがある場合、TiDB はクエリを`SELECT col FROM ... LIMIT 1`に書き換えてインデックスの最初の行を直接読み取ることで、 `MIN(col)`値を素早く取得できます。
-   [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)テーブルに対するクエリの場合、この変数はスロー ログ ファイルの解析の同時実行性を制御します。

### tidb_dml_batch_size {#tidb-dml-batch-size}

> **警告：**
>
> この変数は非推奨のbatch-dml機能に関連付けられており、データ破損を引き起こす可能性があります。そのため、batch-dmlでこの変数を有効にすることは推奨されません。代わりに[非トランザクションDML](/non-transactional-dml.md)使用してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: 行
-   この値が`0`より大きい場合、TiDB は`INSERT`ようなステートメントをより小さなトランザクションにまとめてコミットします。これによりメモリ使用量が削減され、一括変更によって`txn-total-size-limit`に達するのを防ぐことができます。
-   ACID準拠を実現するのは値`0`のみです。他の値に設定すると、TiDBの原子性と独立性の保証が損なわれます。
-   この変数を機能させるには、 1 と、 `tidb_batch_insert`と`tidb_batch_delete`の少なくとも`tidb_enable_batch_dml`つを有効にする必要があります。

> **注記：**
>
> v7.0.0 以降、 `tidb_dml_batch_size` [`LOAD DATA`ステートメント](/sql-statements/sql-statement-load-data.md)には適用されなくなりました。

### tidb_dml_type<span class="version-mark">バージョン8.0.0の新機能</span> {#tidb-dml-type-span-class-version-mark-new-in-v8-0-0-span}

> **警告：**
>
> バルクDML実行モード（ `tidb_dml_type = "bulk"` ）は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、 [問題](https://github.com/pingcap/tidb/issues)を報告してください。現在のバージョンでは、TiDBがバルクDMLモードを使用して大規模なトランザクションを実行すると、TiCDC、 TiFlash、およびTiKVのresolved-tsモジュールのメモリ使用量と実行効率に影響を与え、OOM問題が発生する可能性があります。また、ロックに遭遇するとBRがブロックされ、処理に失敗する可能性があります。したがって、これらのコンポーネントまたは機能が有効になっている場合は、このモードを使用することは推奨されません。

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 文字列
-   デフォルト値: `"standard"`
-   値`"bulk"`オプション: `"standard"`
-   この変数は、DML ステートメントの実行モードを制御します。
    -   `"standard"`標準の DML 実行モードを示します。このモードでは、TiDB トランザクションはコミット前にメモリにキャッシュされます。このモードは、競合が発生する可能性のある高同時実行トランザクションのシナリオに適しており、デフォルトの推奨実行モードです。
    -   `"bulk"`パイプラインDML実行モードを示します。これは、大量のデータが書き込まれ、TiDBで過剰なメモリ使用量が発生するシナリオに適しています。詳細については、 [パイプラインDML](/pipelined-dml.md)参照してください。

### tidb_enable_1pc<span class="version-mark">バージョン5.0の新機能</span> {#tidb-enable-1pc-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、1つのリージョンのみに影響するトランザクションに対して、1フェーズコミット機能を有効にするかどうかを指定するために使用されます。よく使用される2フェーズコミットと比較して、1フェーズコミットはトランザクションコミットのレイテンシーを大幅に短縮し、スループットを向上させることができます。

> **注記：**
>
> -   デフォルト値`ON`は新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   このパラメータを有効にすると、1フェーズコミットがトランザクションコミットのオプションモードになるというだけです。実際には、最適なトランザクションコミットモードはTiDBによって決定されます。

### tidb_enable_analyze_snapshot <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-analyze-snapshot-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `ANALYZE`実行する際に履歴データを読み取るか最新データを読み取るかを制御します。この変数が`ON`に設定されている場合、 `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取ります。この変数が`OFF`に設定されている場合、 `ANALYZE`最新データを読み取ります。
-   v5.2より前は、 `ANALYZE`最新データを読み取ります。v5.2からv6.1までは、 `ANALYZE` `ANALYZE`時点で利用可能な履歴データを読み取ります。

> **警告：**
>
> `ANALYZE` `ANALYZE`の時点で利用可能な履歴データを読み取る場合、履歴データがガベージコレクションされるため、 `AUTO ANALYZE`の長い期間によって`GC life time is shorter than transaction duration`エラーが発生する可能性があります。

### tidb_enable_async_commit<span class="version-mark">バージョン5.0の新機能</span> {#tidb-enable-async-commit-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、2フェーズトランザクションコミットの第2フェーズをバックグラウンドで非同期的に実行する非同期コミット機能を有効にするかどうかを制御します。この機能を有効にすると、トランザクションコミットのレイテンシーを短縮できます。

> **注記：**
>
> -   デフォルト値`ON`は新しいクラスターにのみ適用されます。クラスターが以前のバージョンの TiDB からアップグレードされた場合は、代わりに値`OFF`が使用されます。
> -   このパラメータを有効にすると、非同期コミットがトランザクションコミットのオプションモードになるというだけです。実際には、最適なトランザクションコミットモードはTiDBによって決定されます。

### tidb_enable_auto_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-auto-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB がバックグラウンド操作としてテーブル統計を自動的に更新するかどうかを決定します。
-   この設定は以前は`tidb.toml`オプション ( `performance.run-auto-analyze` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_enable_auto_analyze_priority_queue<span class="version-mark">バージョン8.0.0の新機能</span> {#tidb-enable-auto-analyze-priority-queue-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、優先キューを有効にして統計情報の自動収集タスクをスケジュールするかどうかを制御するために使用されます。この変数を有効にすると、TiDBは、新しく作成されたインデックスやパーティションが変更されたパーティションテーブルなど、収集する価値の高いテーブルの統計情報を優先的に収集します。さらに、TiDBはヘルススコアが低いテーブルを優先し、キューの先頭に配置します。

### tidb_enable_auto_increment_in_generated {#tidb-enable-auto-increment-in-generated}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、生成された列または式インデックスを作成するときに`AUTO_INCREMENT`列を含めるかどうかを決定するために使用されます。

### tidb_enable_batch_dml {#tidb-enable-batch-dml}

> **警告：**
>
> この変数は非推奨のbatch-dml機能に関連付けられており、データ破損を引き起こす可能性があります。そのため、batch-dmlでこの変数を有効にすることは推奨されません。代わりに[非トランザクションDML](/non-transactional-dml.md)使用してください。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非推奨のbatch-dml機能を有効にするかどうかを制御します。この機能を有効にすると、特定のステートメントが複数のトランザクションに分割される可能性があります。これはアトミックではないため、注意して使用する必要があります。batch-dmlを使用する場合は、操作対象のデータに対して同時操作が行われていないことを確認する必要があります。この機能を動作させるには、 `tidb_batch_dml_size`に正の値を指定し、 `tidb_batch_insert`と`tidb_batch_delete`の少なくとも1つを有効にする必要があります。

### tidb_enable_cascades_planner {#tidb-enable-cascades-planner}

> **警告：**
>
> 現在、カスケードプランナーは実験的機能です。本番環境でのご利用は推奨されません。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、カスケード プランナーを有効にするかどうかを制御するために使用されます。

### tidb_enable_check_constraint<span class="version-mark">バージョン7.2.0の新機能</span> {#tidb-enable-check-constraint-span-class-version-mark-new-in-v7-2-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [`CHECK`制約](/constraints.md#check)機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_chunk_rpc<span class="version-mark">バージョン4.0の新機能</span> {#tidb-enable-chunk-rpc-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサーで`Chunk`データ エンコーディング形式を有効にするかどうかを制御するために使用されます。

### tidb_enable_clustered_index<span class="version-mark">バージョン5.0の新機能</span> {#tidb-enable-clustered-index-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `ON`
-   `ON` `INT_ONLY`値: `OFF`
-   この変数は、主キーをデフォルトで[クラスター化インデックス](/clustered-indexes.md)として作成するかどうかを制御するために使用されます。ここでの「デフォルト」とは、ステートメントでキーワード`CLUSTERED` / `NONCLUSTERED`が明示的に指定されていないことを意味します。サポートされる値は`OFF` 、 `ON` 、 `INT_ONLY`です。
    -   `OFF` 、主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
    -   `ON` 、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
    -   `INT_ONLY` 、動作が設定項目`alter-primary-key`によって制御されることを示します。4 `alter-primary-key` `true`に設定すると、すべての主キーはデフォルトで非クラスター化インデックスとして作成されます。8 `false`設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

### tidb_enable_ddl <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-ddl-span-class-version-mark-new-in-v6-3-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   可能な`ON` : `OFF`
-   この変数は、対応するTiDBインスタンスがDDLオーナーになれるかどうかを制御します。現在のTiDBクラスタにTiDBインスタンスが1つしかない場合、そのインスタンスがDDLオーナーになることを阻止することはできません。つまり、この変数を`OFF`に設定することはできません。

### tidb_enable_collect_execution_info {#tidb-enable-collect-execution-info}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロークエリログに各演算子の実行情報を記録するかどうか、および[インデックスの使用統計](/information-schema/information-schema-tidb-index-usage.md)を記録するかどうかを制御します。

### tidb_enable_column_tracking <span class="version-mark">v5.4.0 の新機能</span> {#tidb-enable-column-tracking-span-class-version-mark-new-in-v5-4-0-span}

> **警告：**
>
> バージョン8.3.0以降、この変数は非推奨です。TiDBはデフォルトで述語列を追跡します。詳細については、 [`tidb_analyze_column_options`](#tidb_analyze_column_options-new-in-v830)参照してください。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON` 。v8.3.0 より前では、デフォルト値は`OFF`です。
-   この変数は、TiDBによる`PREDICATE COLUMNS`収集を有効にするかどうかを制御します。収集を有効にした後に無効にすると、以前に収集された`PREDICATE COLUMNS`の情報がクリアされます。詳細は[いくつかの列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)参照してください。

### tidb_enable_enhanced_security {#tidb-enable-enhanced-security}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値

<CustomContent platform="tidb">

-   デフォルト値: `OFF`
-   この変数は、接続先のTiDBサーバーでSecurity拡張モード（SEM）が有効になっているかどうかを示します。この値を変更するには、TiDBサーバー設定ファイルの値`enable-sem`を変更し、TiDBサーバーを再起動する必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   デフォルト値: `ON`
-   この変数は読み取り専用です。TiDB TiDB Cloudでは、Security拡張モード (SEM) がデフォルトで有効になっています。

</CustomContent>

-   SEMは、 [セキュリティ強化Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux)のようなシステムの設計に着想を得ています。MySQL `SUPER`権限を持つユーザーの権限を制限し、代わりに`RESTRICTED`な権限を付与する必要があります。これらのきめ細かな権限には、以下のものが含まれます。
    -   `RESTRICTED_TABLES_ADMIN` : `mysql`スキーマ内のシステム テーブルにデータを書き込み、 `information_schema`テーブルの機密列を表示する機能。
    -   `RESTRICTED_STATUS_ADMIN` : コマンド`SHOW STATUS`内の機密変数を確認する機能。
    -   `RESTRICTED_VARIABLES_ADMIN` : `SHOW [GLOBAL] VARIABLES`および`SET`の機密変数を表示および設定する機能。
    -   `RESTRICTED_USER_ADMIN` : 他のユーザーがユーザー アカウントを変更したり削除したりすることを防ぐ機能。

### tidb_enable_exchange_partition {#tidb-enable-exchange-partition}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`で、つまり`exchange partitions with tables`デフォルトで有効になります。
-   この変数はバージョン6.3.0以降非推奨です。値はデフォルト値の`ON`に固定されます。つまり、デフォルトでは`exchange partitions with tables`有効になります。

### tidb_enable_extended_stats {#tidb-enable-extended-stats}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDBがオプティマイザをガイドするための拡張統計を収集できるかどうかを示します。詳細については[拡張統計入門](/extended-statistics.md)参照してください。

### tidb_enable_external_ts_read <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-external-ts-read-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数を`ON`に設定すると、TiDB は[`tidb_external_ts`](#tidb_external_ts-new-in-v640)で指定されたタイムスタンプでデータを読み取ります。

### tidb_external_ts <span class="version-mark">v6.4.0 の新機能</span> {#tidb-external-ts-span-class-version-mark-new-in-v6-4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-new-in-v640) `ON`に設定すると、TiDB はこの変数で指定されたタイムスタンプでデータを読み取ります。

### tidb_enable_fast_analyze {#tidb-enable-fast-analyze}

> **警告：**
>
> v7.5.0 以降では、この変数は非推奨です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計`Fast Analyze`機能を有効にするかどうかを設定するために使用されます。
-   統計`Fast Analyze`機能を有効にすると、TiDBは約10,000行のデータをランダムにサンプリングして統計情報を取得します。データが不均一に分散している場合やデータサイズが小さい場合、統計の精度は低くなります。その結果、誤ったインデックスを選択するなど、最適な実行プランが得られない可能性があります。通常の`Analyze`文の実行時間が許容範囲内であれば、 `Fast Analyze`機能を無効にすることをお勧めします。

### tidb_enable_fast_table_check <span class="version-mark">v7.2.0 の新機能</span> {#tidb-enable-fast-table-check-span-class-version-mark-new-in-v7-2-0-span}

> **注記：**
>
> この変数は[多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)およびプレフィックス インデックスでは機能しません。

-   スコープ: セッション | グローバル
-   クラスターに永続化: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、テーブル内のデータとインデックスの整合性を迅速にチェックするために、チェックサムベースのアプローチを使用するかどうかを制御します。デフォルト値`ON`は、この機能がデフォルトで有効であることを意味します。
-   この変数を有効にすると、TiDB は[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントをより高速に実行できます。

### tidb_enable_foreign_key<span class="version-mark">バージョン6.3.0の新機能</span> {#tidb-enable-foreign-key-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: v6.6.0 より前のバージョンのデフォルト値は`OFF`です。v6.6.0 以降のバージョンのデフォルト値は`ON`です。
-   この変数は、 `FOREIGN KEY`機能を有効にするかどうかを制御します。

### tidb_enable_gc_aware_memory_track {#tidb-enable-gc-aware-memory-track}

> **警告：**
>
> この変数はTiDBのデバッグ用の内部変数です。将来のリリースで削除される可能性があります。この変数を設定**しないでください**。

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、GC 対応メモリトラックを有効にするかどうかを制御します。

### tidb_enable_global_index <span class="version-mark">v7.6.0 の新機能</span> {#tidb-enable-global-index-span-class-version-mark-new-in-v7-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、パーティションテーブルに対して[グローバルインデックス](/global-indexes.md)作成をサポートするかどうかを制御します。この変数を有効にすると、TiDBではインデックス定義で`GLOBAL`指定することで、**パーティション式で使用されるすべての列を含まない**一意のインデックスを作成できます。
-   この変数はバージョン8.4.0以降非推奨です。値はデフォルト値の`ON`に固定されており、デフォルトでは[グローバルインデックス](/global-indexes.md)有効になっています。

### tidb_enable_lazy_cursor_fetch <span class="version-mark">v8.3.0 の新機能</span> {#tidb-enable-lazy-cursor-fetch-span-class-version-mark-new-in-v8-3-0-span}

> **警告：**
>
> この変数で制御される機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

<CustomContent platform="tidb">

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   可能な`ON` : `OFF`
-   この変数は、 [カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)機能の動作を制御します。
    -   カーソルフェッチが有効で、この変数が`OFF`に設定されている場合、TiDB はステートメント実行開始時にすべてのデータを読み取り、TiDB のメモリに保存し、クライアントが指定した`FetchSize`に基づいて、後続のクライアント読み取りのためにクライアントにデータを返します。結果セットが大きすぎる場合、TiDB は結果を一時的にハードディスクに書き込むことがあります。
    -   カーソル フェッチが有効で、この変数が`ON`に設定されている場合、TiDB はすべてのデータを一度に TiDB ノードに読み取らず、クライアントがデータを取得するたびに TiDB ノードに増分的にデータを読み込みます。
-   この変数によって制御される機能には、次の制限があります。
    -   明示的なトランザクション内のステートメントはサポートされません。
    -   `TableReader` `IndexReader` `Projection`のみ`IndexLookUp`含む実行プランのみ`Selection`サポートされます。
    -   Lazy Cursor Fetch を使用するステートメントの場合、 [声明の要約](/statement-summary-tables.md)と[スロークエリログ](/identify-slow-queries.md)には実行情報が表示されません。
-   サポートされていないシナリオでは、この変数を`OFF`に設定した場合と同じ動作になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   可能な`ON` : `OFF`
-   この変数は、 [カーソルフェッチ](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result)機能の動作を制御します。
    -   カーソルフェッチが有効で、この変数が`OFF`に設定されている場合、TiDB はステートメント実行開始時にすべてのデータを読み取り、TiDB のメモリに保存し、クライアントが指定した`FetchSize`に基づいて、後続のクライアント読み取りのためにクライアントにデータを返します。結果セットが大きすぎる場合、TiDB は結果を一時的にハードディスクに書き込むことがあります。
    -   カーソル フェッチが有効で、この変数が`ON`に設定されている場合、TiDB はすべてのデータを一度に TiDB ノードに読み取るのではなく、クライアントがデータを取得するときに増分的に TiDB ノードにデータを読み込みます。
-   この変数によって制御される機能には、次の制限があります。
    -   明示的なトランザクション内のステートメントはサポートされません。
    -   `TableReader` `IndexReader` `Projection`のみ`IndexLookUp`含む実行プランのみ`Selection`サポートされます。
    -   Lazy Cursor Fetch を使用するステートメントの場合、 [声明の要約](/statement-summary-tables.md)と[スロークエリログ](https://docs.pingcap.com/tidb/stable/identify-slow-queries)には実行情報が表示されません。
-   サポートされていないシナリオでは、この変数を`OFF`に設定した場合と同じ動作になります。

</CustomContent>

### tidb_enable_non_prepared_plan_cache {#tidb-enable-non-prepared-plan-cache}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。
-   この機能を有効にすると、メモリとCPUのオーバーヘッドが増加する可能性があり、すべての状況に適しているとは限りません。実際のシナリオに応じて、この機能を有効にするかどうかを判断してください。

### tidb_enable_non_prepared_plan_cache_for_dml<span class="version-mark">バージョン7.1.0の新機能</span> {#tidb-enable-non-prepared-plan-cache-for-dml-span-class-version-mark-new-in-v7-1-0-span}

> **警告：**
>
> DML文の非準備実行プランキャッシュは実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF` 。
-   この変数は、DML ステートメントに対して[準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)機能を有効にするかどうかを制御します。

### tidb_enable_gogc_tuner <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-gogc-tuner-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、GOGC チューナーを有効にするかどうかを制御します。

### tidb_enable_historical_stats {#tidb-enable-historical-stats}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF` 。v8.2.0 より前では、デフォルト値は`ON`です。
-   この変数は、履歴統計を有効にするかどうかを制御します。デフォルト値は`OFF`で、履歴統計はデフォルトで無効になっています。

### tidb_enable_historical_stats_for_capture {#tidb-enable-historical-stats-for-capture}

> **警告：**
>
> この変数で制御される機能は、現在のTiDBバージョンでは完全には機能しません。デフォルト値を変更しないでください。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CAPTURE`で取得される情報にデフォルトで履歴統計情報が含まれるかどうかを制御します。デフォルト値`OFF`は、履歴統計情報がデフォルトで含まれないことを意味します。

### tidb_enable_index_merge<span class="version-mark">バージョン4.0の新機能</span> {#tidb-enable-index-merge-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> -   TiDB クラスターを v4.0.0 より前のバージョンから v5.4.0 以降にアップグレードすると、実行プランの変更によるパフォーマンスの低下を防ぐため、この変数はデフォルトで無効になります。
>
> -   TiDB クラスターを v4.0.0 以降から v5.4.0 以降にアップグレードした後も、この変数はアップグレード前の設定のままになります。
>
> -   v5.4.0 以降、新しくデプロイされた TiDB クラスターでは、この変数はデフォルトで有効になっています。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、インデックスマージ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_index_merge_join {#tidb-enable-index-merge-join}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `IndexMergeJoin`演算子を有効にするかどうかを指定します。
-   この変数はTiDBの内部処理にのみ使用されます。調整することは**推奨されません**。調整すると、データの正確性に影響する可能性があります。

### tidb_enable_legacy_instance_scope<span class="version-mark">バージョン6.0.0の新機能</span> {#tidb-enable-legacy-instance-scope-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `SET SESSION`および`SET GLOBAL`構文を使用して`INSTANCE`スコープの変数を設定することを許可します。
-   このオプションは、以前のバージョンの TiDB との互換性を保つためにデフォルトで有効になっています。

### tidb_enable_list_partition<span class="version-mark">バージョン5.0の新機能</span> {#tidb-enable-list-partition-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `LIST (COLUMNS) TABLE PARTITION`機能を有効にするかどうかを設定するために使用されます。
-   この変数はバージョン8.4.0以降非推奨です。値はデフォルト値の`ON`に固定されます。つまり、デフォルトでは[List パーティショニング](/partitioned-table.md#list-partitioning)有効になります。

### tidb_enable_local_txn {#tidb-enable-local-txn}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は未リリースの機能に使用されます。**変数値を変更しないでください**。

### tidb_enable_metadata_lock <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-metadata-lock-span-class-version-mark-new-in-v6-3-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [メタデータロック](/metadata-lock.md)機能を有効にするかどうかを設定するために使用されます。この変数を設定する際は、クラスター内で実行中の DDL ステートメントがないことを確認してください。そうでない場合、データが不正確になったり、不整合が生じたりする可能性があります。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumの場合、この変数は読み取り専用です。変更が必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)ご連絡ください。

</CustomContent>

### tidb_enable_mutation_checker <span class="version-mark">v6.0.0 の新機能</span> {#tidb-enable-mutation-checker-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDBミューテーションチェッカーを有効にするかどうかを制御します。これは、DML文の実行中にデータとインデックス間の整合性をチェックするツールです。チェッカーが文に対してエラーを返した場合、TiDBはその文の実行をロールバックします。この変数を有効にすると、CPU使用率がわずかに増加します。詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。
-   バージョン6.0.0以降の新しいクラスターの場合、デフォルト値は`ON`です。バージョン6.0.0より前のバージョンからアップグレードした既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_enable_new_cost_interface <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-new-cost-interface-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiDB v6.2.0 では、以前のコストモデルの実装がリファクタリングされています。この変数は、リファクタリングされたコストモデルの実装を有効にするかどうかを制御します。
-   リファクタリングされたコスト モデルでは以前と同じコスト式が使用され、プランの決定は変更されないため、この変数はデフォルトで有効になっています。
-   クラスターをv6.1からv6.2にアップグレードした場合、この変数は`OFF`ままです。手動で有効化することをお勧めします。クラスターをv6.1より前のバージョンからアップグレードした場合、この変数はデフォルトで`ON`に設定されます。

### tidb_enable_new_only_full_group_by_check <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-new-only-full-group-by-check-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDBが`ONLY_FULL_GROUP_BY`チェックを実行する際の動作を制御します。3 `ONLY_FULL_GROUP_BY`詳細については、 [MySQLドキュメント](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)を参照してください。v6.1.0では、TiDBはこのチェックをより厳格かつ正確に処理します。
-   バージョンアップグレードによって発生する可能性のある互換性の問題を回避するために、この変数のデフォルト値は v6.1.0 では`OFF`になっています。

### tidb_enable_noop_functions<span class="version-mark">バージョン4.0の新機能</span> {#tidb-enable-noop-functions-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   `ON` `WARN`値: `OFF`
-   デフォルトでは、TiDBは、まだ実装されていない機能の構文を使用しようとするとエラーを返します。変数値が`ON`に設定されている場合、TiDBはそのような利用できない機能を無視します。これは、SQLコードを変更できない場合に役立ちます。
-   `noop`関数を有効にすると、次の動作が制御されます。
    -   `LOCK IN SHARE MODE`構文
    -   `SQL_CALC_FOUND_ROWS`構文
    -   `START TRANSACTION READ ONLY`と`SET TRANSACTION READ ONLY`構文
    -   `tx_read_only` `super_read_only` `sql_auto_is_null` `read_only` `transaction_read_only` `offline_mode`
    -   `GROUP BY <expr> ASC|DESC`構文

> **警告：**
>
> 安全と考えられるのはデフォルト値の`OFF`のみです。3 `tidb_enable_noop_functions=1`設定すると、TiDBが特定の構文をエラーなしで無視することを許可するため、アプリケーションで予期しない動作が発生する可能性があります。例えば、構文`START TRANSACTION READ ONLY`は許可されますが、トランザクションは読み取り/書き込みモードのままになります。

### tidb_enable_noop_variables <span class="version-mark">v6.2.0 の新機能</span> {#tidb-enable-noop-variables-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   変数値を`OFF`に設定すると、TiDB は次のように動作します。
    -   `SET`使用して`noop`変数を設定すると、TiDB は`"setting *variable_name* has no effect in TiDB"`警告を返します。
    -   `SHOW [SESSION | GLOBAL] VARIABLES`の結果には`noop`変数は含まれません。
    -   `SELECT`使用して`noop`変数を読み取ると、TiDB は`"variable *variable_name* has no effect in TiDB"`警告を返します。
-   TiDB インスタンスが`noop`変数を設定して読み取ったかどうかを確認するには、 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;`ステートメントを使用できます。

### tidb_enable_null_aware_anti_join <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-null-aware-anti-join-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: v7.0.0 より前のバージョンでは、デフォルト値は`OFF`です。v7.0.0 以降では、デフォルト値は`ON`です。
-   タイプ: ブール値
-   この変数は、特殊なセット演算子`NOT IN`と`!= ALL`で始まるサブクエリによって ANTI JOIN が生成される場合に、TiDB が Null Aware Hash Join を適用するかどうかを制御します。
-   以前のバージョンから v7.0.0 以降のクラスターにアップグレードすると、この機能は自動的に有効になり、この変数は`ON`に設定されます。

### tidb_enable_outer_join_reorder <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-outer-join-reorder-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   v6.1.0以降、TiDBの[結合したテーブルの再配置](/join-reorder.md)アルゴリズムはOuter Joinをサポートしています。この変数は、TiDBがJoin ReorderのOuter Joinサポートを有効にするかどうかを制御します。
-   クラスターを以前のバージョンの TiDB からアップグレードする場合は、次の点に注意してください。

    -   アップグレード前の TiDB バージョンが v6.1.0 より前の場合、アップグレード後のこの変数のデフォルト値は`ON`なります。
    -   アップグレード前の TiDB バージョンが v6.1.0 以降の場合、アップグレード後の変数のデフォルト値はアップグレード前の値に従います。

### <code>tidb_enable_inl_join_inner_multi_pattern</code> <span class="version-mark">v7.0.0 の新機能</span> {#code-tidb-enable-inl-join-inner-multi-pattern-code-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON` 。v8.3.0 以前のバージョンではデフォルト値は`OFF`です。
-   この変数は、内部テーブルに`Selection` 、または`Projection`演算子がある場合にインデックス結合をサポートするかどうかを制御します。デフォルト値の`OFF` `Aggregation`このシナリオではインデックス結合がサポートされないことを意味します。
-   TiDB クラスターを v7.0.0 より前のバージョンから v8.4.0 以降にアップグレードする場合、この変数はデフォルトで`OFF`に設定され、このシナリオではインデックス結合がサポートされないことを示します。

### tidb_enable_instance_plan_cache <span class="version-mark">v8.4.0 の新機能</span> {#tidb-enable-instance-plan-cache-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> 現在、インスタンスプランキャッシュは実験的機能です。本番環境でのご利用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、インスタンスプランキャッシュ機能を有効にするかどうかを制御します。この機能はインスタンスレベルの実行プランキャッシュを実装し、同じTiDBインスタンス内のすべてのセッションで実行プランキャッシュを共有することで、メモリ使用率を向上させます。インスタンスプランキャッシュを有効にする前に、セッションレベル[準備された実行プランのキャッシュ](/sql-prepared-plan-cache.md)と[準備されていない実行プランのキャッシュ](/sql-non-prepared-plan-cache.md)を無効にすることをお勧めします。

### tidb_enable_ordered_result_mode {#tidb-enable-ordered-result-mode}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   最終出力結果を自動的にソートするかどうかを指定します。
-   たとえば、この変数を有効にすると、TiDB は`SELECT a, MAX(b) FROM t GROUP BY a` `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`として処理します。

### tidb_enable_paging<span class="version-mark">バージョン5.4.0の新機能</span> {#tidb-enable-paging-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、コプロセッサリクエストの送信にページング方式を使用するかどうかを制御します。TiDBバージョン[v5.4.0、v6.2.0)では、この変数は`IndexLookup`演算子にのみ適用されます。v6.2.0以降では、この変数はグローバルに適用されます。v6.4.0以降、この変数のデフォルト値は`OFF`から`ON`に変更されます。
-   ユーザーシナリオ:

    -   すべての OLTP シナリオでは、ページング方式を使用することをお勧めします。
    -   `IndexLookup`と`Limit`使用し、 `Limit`を`IndexScan`にプッシュダウンできない読み取りクエリの場合、読み取りクエリのレイテンシーが高くなり、TiKV `Unified read pool CPU`の使用率が高くなる可能性があります。このような場合、 `Limit`演算子は少量のデータしか必要としないため、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)を`ON`に設定すると、TiDB が処理するデータ量が少なくなり、クエリのレイテンシーとリソース消費が削減されます。
    -   [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用したデータのエクスポートや完全なテーブルスキャンなどのシナリオでは、ページングを有効にすると、TiDB プロセスのメモリ消費を効果的に削減できます。

> **注記：**
>
> TiFlashではなく TiKV をstorageエンジンとして使用する OLAP シナリオでは、ページングを有効にするとパフォーマンスが低下する場合があります。パフォーマンス低下が発生した場合は、この変数を使用してページングを無効にするか、変数[`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-new-in-v620)と[`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-new-in-v630)を使用してページングサイズの行範囲を調整することを検討してください。

### tidb_enable_parallel_apply<span class="version-mark">バージョン5.0の新機能</span> {#tidb-enable-parallel-apply-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、演算子`Apply`同時実行を有効にするかどうかを制御します。同時実行の数は、変数`tidb_executor_concurrency`によって制御されます。演算子`Apply`は相関サブクエリを処理し、デフォルトでは同時実行がないため、実行速度が遅くなります。この変数の値を`1`に設定すると、同時実行数が増加し、実行速度が向上します。現在、演算子`Apply`の同時実行はデフォルトで無効になっています。

### tidb_enable_parallel_hashagg_spill <span class="version-mark">v8.0.0 の新機能</span> {#tidb-enable-parallel-hashagg-spill-span-class-version-mark-new-in-v8-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDBが並列HashAggアルゴリズムのディスクスピルをサポートするかどうかを制御します。1 の場合`ON` HashAgg演算子は並列処理の条件を問わず、メモリ使用量に基づいて自動的にデータスピルをトリガーし、パフォーマンスとデータスループットのバランスを保ちます。この変数を`OFF`に設定することは推奨されません。v8.2.0以降、この変数を`OFF`に設定するとエラーが報告されます。この変数は将来のリリースで非推奨となる予定です。

### tidb_enable_pipelined_window_function {#tidb-enable-pipelined-window-function}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [ウィンドウ関数](/functions-and-operators/window-functions.md)にパイプライン実行アルゴリズムを使用するかどうかを指定します。

### tidb_enable_plan_cache_for_param_limit <span class="version-mark">v6.6.0 の新機能</span> {#tidb-enable-plan-cache-for-param-limit-span-class-version-mark-new-in-v6-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュ が、 `LIMIT`パラメータとして変数 ( `LIMIT ?` ) を持つ実行プランをキャッシュするかどうかを制御します。デフォルト値は`ON`で、 プリペアドプランキャッシュ がそのような実行プランのキャッシュをサポートすることを意味します。Prepared プリペアドプランキャッシュ は、 10000 を超える変数を持つ実行プランのキャッシュをサポートしないことに注意してください。

### tidb_enable_plan_cache_for_subquery<span class="version-mark">バージョン7.0.0の新機能</span> {#tidb-enable-plan-cache-for-subquery-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュがサブクエリを含むクエリをキャッシュするかどうかを制御します。

### tidb_enable_plan_replayer_capture {#tidb-enable-plan-replayer-capture}

<CustomContent platform="tidb-cloud">

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `PLAN REPLAYER CAPTURE`機能を有効にするかどうかを制御します。デフォルト値`ON` 、 `PLAN REPLAYER CAPTURE`機能を有効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`PLAN REPLAYER CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)を有効にするかどうかを制御します。デフォルト値`ON` `PLAN REPLAYER CAPTURE`機能を有効にすることを意味します。

</CustomContent>

### tidb_enable_plan_replayer_continuous_capture <span class="version-mark">v7.0.0 の新機能</span> {#tidb-enable-plan-replayer-continuous-capture-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb-cloud">

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `PLAN REPLAYER CONTINUOUS CAPTURE`機能を有効にするかどうかを制御します。デフォルト値`OFF` 、この機能を無効にすることを意味します。

</CustomContent>

<CustomContent platform="tidb">

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は[`PLAN REPLAYER CONTINUOUS CAPTURE`機能](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)を有効にするかどうかを制御します。デフォルト値`OFF` 、この機能を無効にすることを意味します。

</CustomContent>

### tidb_enable_point_get_cache {#tidb-enable-point-get-cache}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当：はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   テーブル ロック タイプを[`LOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) ～ `READ`に設定した場合、この変数を`ON`に設定すると、ポイント クエリの結果のキャッシュが有効になり、繰り返しクエリのオーバーヘッドが削減され、ポイント クエリのパフォーマンスが向上します。

### tidb_enable_prepared_plan_cache <span class="version-mark">v6.1.0 の新機能</span> {#tidb-enable-prepared-plan-cache-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   [プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)有効にするかどうかを決定します。有効にすると、 `Prepare`と`Execute`の実行プランがキャッシュされ、以降の実行では実行プランの最適化がスキップされるため、パフォーマンスが向上します。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-prepared-plan-cache-memory-monitor-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   この変数は、プリペアドプランキャッシュにキャッシュされた実行プランによって消費されたメモリをカウントするかどうかを制御します。詳細については[プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)参照してください。

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">v5.3.0 の新機能</span> {#tidb-enable-pseudo-for-outdated-stats-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、統計が古くなった場合にテーブルの統計を使用する際のオプティマイザの動作を制御します。

<CustomContent platform="tidb">

-   オプティマイザは、テーブルの統計情報が古くなっているかどうかを次のように判断します。統計情報を取得するためにテーブルに対して最後に`ANALYZE`を実行してから、テーブル行の 80% が変更された場合（変更された行数を合計行数で割った値）、オプティマイザはこのテーブルの統計情報が古くなっていると判断します。この比率は[`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)設定を使用して変更できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   オプティマイザは、次のようにしてテーブルの統計が古くなっているかどうかを判断します。統計を取得するためにテーブルで最後に`ANALYZE`実行されて以降、テーブル行の 80% が変更されている場合 (変更された行数を合計行数で割った値)、オプティマイザはこのテーブルの統計が古くなっていると判断します。

</CustomContent>

-   デフォルト（変数値`OFF` ）では、テーブルの統計情報が古くても、オプティマイザは引き続きそのテーブルの統計情報を使用します。変数値を`ON`に設定すると、オプティマイザは合計行数を除いてテーブルの統計情報が信頼できないと判断し、疑似統計情報を使用します。
-   テーブル上のデータが頻繁に変更され、そのテーブルに対して`ANALYZE`適時に実行できない場合は、実行プランを安定させるために、変数値を`OFF`に設定することをお勧めします。

### tidb_enable_rate_limit_action {#tidb-enable-rate-limit-action}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、データ読み取り演算子の動的メモリ制御機能を有効にするかどうかを制御します。デフォルトでは、この演算子はデータ読み取りに許可される最大スレッド数（ [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)を有効にします。単一のSQL文のメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超えると、データ読み取り演算子は1つのスレッドを停止します。

<CustomContent platform="tidb">

-   データを読み取る演算子に残っているスレッドが 1 つだけであり、単一の SQL ステートメントのメモリ使用量が継続的に[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超える場合、この SQL ステートメントは[ディスクへのデータの流出](/system-variables.md#tidb_enable_tmp_storage_on_oom)などの他のメモリ制御動作をトリガーします。
-   この変数は、SQL文がデータの読み取りのみを行う場合に、メモリ使用量を効果的に制御します。結合や集計などの計算処理が必要な場合は、メモリ使用量が`tidb_mem_quota_query`で制御できない可能性があり、OOM（オーバーヘッドメモリ）のリスクが高まります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   データを読み取る演算子に残っているスレッドが 1 つだけであり、単一の SQL ステートメントのメモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超え続ける場合、この SQL ステートメントは、データをディスクに書き出すなどの他のメモリ制御動作をトリガーします。

</CustomContent>

### tidb_enable_resource_control<span class="version-mark">バージョン6.6.0の新機能</span> {#tidb-enable-resource-control-span-class-version-mark-new-in-v6-6-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は[リソース制御機能](/tidb-resource-control-ru-groups.md)スイッチです。この変数を`ON`に設定すると、TiDB クラスターはリソースグループに基づいてアプリケーションリソースを分離できます。

### tidb_enable_reuse_chunk <span class="version-mark">v6.4.0 の新機能</span> {#tidb-enable-reuse-chunk-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   値`ON`オプション: `OFF`
-   この変数は、TiDBがチャンクオブジェクトのキャッシュを有効にするかどうかを制御します。値が`ON`の場合、TiDBはキャッシュされたチャンクオブジェクトを優先的に使用し、要求されたオブジェクトがキャッシュに存在しない場合にのみシステムから要求します。値が`OFF`の場合、TiDBはシステムから直接チャンクオブジェクトを要求します。

### tidb_enable_shared_lock_promotion <span class="version-mark">v8.3.0 の新機能</span> {#tidb-enable-shared-lock-promotion-span-class-version-mark-new-in-v8-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、共有ロックを排他ロックにアップグレードする機能を有効にするかどうかを制御します。TiDBはデフォルトで`SELECT LOCK IN SHARE MODE`サポートしていません。変数値が`ON`の場合、TiDBは`SELECT LOCK IN SHARE MODE`ステートメントを`SELECT FOR UPDATE`にアップグレードし、悲観的ロックを追加しようとします。この変数のデフォルト値は`OFF`で、共有ロックを排他ロックにアップグレードする機能は無効です。
-   この変数を有効にすると、 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)が有効かどうかに関係なく、 `SELECT LOCK IN SHARE MODE`ステートメントに影響します。

### tidb_enable_slow_log {#tidb-enable-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログ機能を有効にするかどうかを制御するために使用されます。

### tidb_enable_tmp_storage_on_oom {#tidb-enable-tmp-storage-on-oom}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   値`ON`オプション: `OFF`
-   単一の SQL ステートメントがシステム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)で指定されたメモリクォータを超えた場合に、一部の演算子の一時storageを有効にするかどうかを制御します。
-   v6.3.0より前のバージョンでは、TiDB設定項目`oom-use-tmp-storage`を使用してこの機能を有効化または無効化できます。クラスターをv6.3.0以降にアップグレードすると、TiDBクラスターはこの変数を自動的に値`oom-use-tmp-storage`で初期化します。その後、値`oom-use-tmp-storage`を変更しても効果は**ありません**。

### tidb_enable_stats_owner <span class="version-mark">v8.4.0 の新機能</span> {#tidb-enable-stats-owner-span-class-version-mark-new-in-v8-4-0-span}

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   可能な`ON` : `OFF`
-   この変数は、対応するTiDBインスタンスが[自動統計更新](/statistics.md#automatic-update)タスクを実行できるかどうかを制御します。現在のTiDBクラスタにTiDBインスタンスが1つしかない場合、このインスタンスの自動統計更新を無効にすることはできません。つまり、この変数を`OFF`に設定することはできません。

### tidb_enable_stmt_summary <span class="version-mark">v3.0.4 の新機能</span> {#tidb-enable-stmt-summary-span-class-version-mark-new-in-v3-0-4-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ステートメントサマリー機能を有効にするかどうかを制御するために使用されます。有効にすると、SQL実行情報（消費時間など）が`information_schema.STATEMENTS_SUMMARY`システムテーブルに記録され、SQLパフォーマンスの問題を特定してトラブルシューティングできるようになります。

### tidb_enable_strict_double_type_check<span class="version-mark">バージョン5.0の新機能</span> {#tidb-enable-strict-double-type-check-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、型`DOUBLE`の無効な定義を持つテーブルの作成を許可するかどうかを制御します。この設定は、型の検証がそれほど厳格ではなかった以前のバージョンの TiDB からのアップグレードパスを提供することを目的としています。
-   デフォルト値`ON`は MySQL と互換性があります。

例えば、浮動小数点型の精度は保証されていないため、型`DOUBLE(10)`は無効とみなされます。3 `tidb_enable_strict_double_type_check` `OFF`に変更すると、次のテーブルが作成されます。

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
> MySQLでは`FLOAT`型に対して精度を指定できるため、この設定は型`DOUBLE`にのみ適用されます。この動作はMySQL 8.0.17以降では非推奨となり、 `FLOAT`または`DOUBLE`型に対して精度を指定することは推奨されません。

### tidb_enable_table_partition {#tidb-enable-table-partition}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `ON`
-   この変数はバージョン8.4.0以降非推奨です。値はデフォルト値の`ON`に固定されます。つまり、デフォルトでは[テーブルパーティション](/partitioned-table.md)有効になります。

### tidb_enable_telemetry <span class="version-mark">v4.0.2 の新機能</span> {#tidb-enable-telemetry-span-class-version-mark-new-in-v4-0-2-span}

> **警告：**
>
> -   v8.1.0 より前のバージョンでは、TiDB は定期的にテレメトリ データを PingCAP に報告します。
> -   v8.1.0からv8.5.1のバージョンでは、TiDBはテレメトリ機能を削除し、変数`tidb_enable_telemetry`は無効になります。これは、以前のバージョンとの互換性のためだけに保持されています。
> -   v8.5.3以降、TiDBはテレメトリ機能を再度導入しました。ただし、テレメトリ関連の情報はローカルにのみ記録され、ネットワーク経由でPingCAPにデータが送信されなくなりました。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON` 。v8.5.3 以降では、デフォルト値が`OFF`から`ON`に変更されます。

<CustomContent platform="tidb">

-   この変数は、TiDBでテレメトリ機能を有効にするかどうかを制御します。v8.5.3以降、この変数はTiDBインスタンスの[`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)の設定項目が`true`に設定されている場合にのみ有効になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">v6.3.0 の新機能</span> {#tidb-enable-tiflash-read-for-write-stmt-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 `INSERT` 、 `DELETE` 、 `UPDATE`を含むSQL文の読み取り操作をTiFlashにプッシュダウンできるかどうかを制御します。例:

    -   `INSERT INTO SELECT`ステートメントに`SELECT`クエリ (一般的な使用シナリオ: [TiFlashクエリ結果の具体化](/tiflash/tiflash-results-materialization.md) )
    -   `UPDATE`と`DELETE`文の条件フィルタリング`WHERE`
-   バージョン7.1.0以降、この変数は非推奨です。1 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)場合、オプティマイザーは[SQLモード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定します。TiDBでは、 `INSERT` 、 `DELETE` 、 `UPDATE` （ `INSERT INTO SELECT`など）を含むSQL文の読み取り操作をTiFlashにプッシュダウンできるのは、現在のセッションの[SQLモード](/sql-mode.md)厳密ではない場合のみです。つまり、 `sql_mode`値には`STRICT_TRANS_TABLES`と`STRICT_ALL_TABLES`含まれません。

### tidb_enable_top_sql<span class="version-mark">バージョン5.4.0の新機能</span> {#tidb-enable-top-sql-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
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
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TSOFollowerプロキシ機能を有効にするかどうかを制御します。値が`OFF`の場合、TiDBはPDリーダーからのみTSOを取得します。値が`ON`の場合、TiDBはTSOリクエストをすべてのPDサーバーに均等に分散し、PDフォロワーもTSOリクエストを処理できるため、PDリーダーのCPU負荷が軽減されます。
-   TSOFollowerプロキシを有効にするシナリオ:
    -   TSO 要求の圧力が高いため、PD リーダーの CPU がボトルネックになり、TSO RPC 要求のレイテンシーが長くなります。
    -   TiDB クラスターには多数の TiDB インスタンスがあり、値を[`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)に増やしても、TSO RPC 要求の高レイテンシーの問題を軽減することはできません。

> **注記：**
>
> -   PDリーダーのCPU使用率のボトルネック以外の理由（ネットワークの問題など）でTSO RPCのレイテンシーが増加したとします。この場合、TSOFollowerプロキシを有効にすると、TiDBでの実行レイテンシーが増加し、クラスターのQPSパフォーマンスに影響を与える可能性があります。
> -   この機能は[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)と互換性がありません。この機能を有効にすると、 [`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)機能しません。

### tidb_enable_unsafe_substitute<span class="version-mark">バージョン6.3.0の新機能</span> {#tidb-enable-unsafe-substitute-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、式を生成列に安全でない方法で置換するかどうかを制御します。デフォルト値は`OFF`で、安全でない置換はデフォルトで無効になっています。詳細については[生成された列](/generated-columns.md)参照してください。

### tidb_enable_vectorized_expression <span class="version-mark">v4.0 の新機能</span> {#tidb-enable-vectorized-expression-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、ベクトル化された実行を有効にするかどうかを制御するために使用されます。

### tidb_enable_window_function {#tidb-enable-window-function}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [ウィンドウ関数](/functions-and-operators/window-functions.md)のサポートを有効にするかどうかを制御します。ウィンドウ関数は予約語を使用する場合があることに注意してください。そのため、TiDBのアップグレード後、正常に実行できるSQL文が解析に失敗する可能性があります。このような場合は、 `tidb_enable_window_function`を`OFF`に設定できます。

### <code>tidb_enable_row_level_checksum</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-enable-row-level-checksum-code-span-class-version-mark-new-in-v7-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   この変数は、 [単一行データの TiCDC データ整合性検証](/ticdc/ticdc-integrity-check.md)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [単一行データの TiCDC データ整合性検証](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)機能を有効にするかどうかを制御するために使用されます。

</CustomContent>

-   [`TIDB_ROW_CHECKSUM()`](/functions-and-operators/tidb-functions.md#tidb_row_checksum)関数を使用して、行のチェックサム値を取得できます。

### tidb_enforce_mpp<span class="version-mark">バージョン5.1の新機能</span> {#tidb-enforce-mpp-span-class-version-mark-new-in-v5-1-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb">

-   このデフォルト値を変更するには、 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値を変更します。

</CustomContent>

-   オプティマイザのコスト見積もりを無視し、クエリ実行時にTiFlashのMPPモードを強制的に使用するかどうかを制御します。値のオプションは次のとおりです。
    -   `0`または`OFF` 。MPP モードが強制的に使用されないことを意味します (デフォルト)。
    -   `1`または`ON`場合、コスト推定は無視され、MPPモードが強制的に使用されます。この設定は`tidb_allow_mpp=true`場合にのみ有効になることに注意してください。

MPPは、 TiFlashエンジンが提供する分散コンピューティングフレームワークであり、ノード間のデータ交換を可能にし、高性能かつ高スループットのSQLアルゴリズムを提供します。MPPモードの選択の詳細については、 [MPPモードを選択するかどうかを制御します](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)を参照してください。

### tidb_evolve_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-baselines-span-class-version-mark-new-in-v4-0-span}

> **警告：**
>
> この変数で制御される機能は実験的機能です。本番環境での使用は推奨されません。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ベースライン進化機能を有効にするかどうかを制御するために使用されます。詳細な説明と使用方法については、 [ベースライン進化](/sql-plan-management.md#baseline-evolution)参照してください。
-   ベースラインの進化がクラスターに与える影響を軽減するには、次の構成を使用します。
    -   各実行プランの最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`設定します。デフォルト値は 600 秒です。
    -   時間枠を制限するには、 `tidb_evolve_plan_task_start_time`と`tidb_evolve_plan_task_end_time`を設定します。デフォルト値はそれぞれ`00:00 +0000`と`23:59 +0000`です。

### tidb_evolve_plan_task_end_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-end-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   デフォルト値: `23:59 +0000`
-   この変数は、1 日のベースライン進化の終了時刻を設定するために使用されます。

### tidb_evolve_plan_task_max_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-max-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `600`
-   範囲: `[-1, 9223372036854775807]`
-   単位: 秒
-   この変数は、ベースライン進化機能の各実行プランの最大実行時間を制限するために使用されます。

### tidb_evolve_plan_task_start_time <span class="version-mark">v4.0 の新機能</span> {#tidb-evolve-plan-task-start-time-span-class-version-mark-new-in-v4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   デフォルト値: `00:00 +0000`
-   この変数は、1 日のベースライン進化の開始時刻を設定するために使用されます。

### tidb_executor_concurrency<span class="version-mark">バージョン5.0の新機能</span> {#tidb-executor-concurrency-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `5`
-   範囲: `[1, 256]`
-   単位: スレッド

この変数は、次の SQL 演算子の同時実行性を (1 つの値に) 設定するために使用されます。

-   `index lookup`
-   `index lookup join`
-   `hash join`
-   `hash aggregation` （第`partial`フェーズと`final`フェーズ）
-   `window`
-   `projection`
-   `sort`

`tidb_executor_concurrency` 、管理を容易にするために、次の既存のシステム変数が全体的に組み込まれています。

-   `tidb_index_lookup_concurrency`
-   `tidb_index_lookup_join_concurrency`
-   `tidb_hash_join_concurrency`
-   `tidb_hashagg_partial_concurrency`
-   `tidb_hashagg_final_concurrency`
-   `tidb_projection_concurrency`
-   `tidb_window_concurrency`

バージョン5.0以降でも、上記のシステム変数を個別に変更することは可能です（ただし、非推奨の警告が返されます）。変更は対応する個々の演算子にのみ影響します。その後、 `tidb_executor_concurrency`使用して演算子の同時実行性を変更しても、個別に変更された演算子には影響しません。 `tidb_executor_concurrency`使用してすべての演算子の同時実行性を変更する場合は、上記のすべての変数の値を`-1`に設定してください。

以前のバージョンからv5.0にアップグレードしたシステムにおいて、上記の変数の値を変更していない場合（つまり、 `tidb_hash_join_concurrency`値が`5`で、残りの値が`4`の場合）、これらの変数によって以前管理されていた演算子の同時実行性は、自動的に`tidb_executor_concurrency`によって管理されます。これらの変数のいずれかを変更した場合、対応する演算子の同時実行性は、変更された変数によって引き続き制御されます。

### tidb_expensive_query_time_threshold {#tidb-expensive-query-time-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `60`
-   範囲: `[10, 2147483647]`
-   単位: 秒
-   この変数は、高負荷クエリログを出力するかどうかを決定するしきい値を設定するために使用されます。高負荷クエリログと低負荷クエリログの違いは次のとおりです。
    -   ステートメントの実行後にスロー ログが出力されます。
    -   コストのかかるクエリ ログには、実行時間がしきい値を超えている実行中のステートメントとその関連情報が出力されます。

### tidb_expensive_txn_time_threshold <span class="version-mark">v7.2.0 の新機能</span> {#tidb-expensive-txn-time-threshold-span-class-version-mark-new-in-v7-2-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `600`
-   範囲: `[60, 2147483647]`
-   単位: 秒
-   この変数は、高負荷トランザクションのログ記録のしきい値を制御します。デフォルトでは600秒です。トランザクションの実行時間がしきい値を超え、コミットもロールバックも行われない場合、高負荷トランザクションとみなされ、ログに記録されます。

### tidb_force_priority {#tidb-force-priority}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `NO_PRIORITY`
-   `LOW_PRIORITY` `DELAYED`値`HIGH_PRIORITY` `NO_PRIORITY`
-   この変数は、TiDBサーバー上で実行されるステートメントのデフォルトの優先度を変更するために使用されます。例えば、OLAPクエリを実行している特定のユーザーに、OLTPクエリを実行しているユーザーよりも低い優先度を与えるようにすることができます。
-   デフォルト値`NO_PRIORITY`は、ステートメントの優先順位が強制的に変更されないことを意味します。

> **注記：**
>
> TiDB v6.6.0以降、 [リソース管理](/tidb-resource-control-ru-groups.md)サポートします。この機能を使用すると、異なるリソースグループで異なる優先度のSQL文を実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、優先度の異なるSQL文のスケジュールをより適切に制御できます。リソース制御を有効にすると、文の優先度は適用されなくなります。異なるSQL文のリソース使用量を管理するには、 [リソース管理](/tidb-resource-control-ru-groups.md)使用することをお勧めします。

### tidb_gc_concurrency<span class="version-mark">バージョン5.0の新機能</span> {#tidb-gc-concurrency-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `-1`または`[1, 256]`
-   単位: スレッド
-   この変数は、 [ガベージコレクション（GC）](/garbage-collection-overview.md)プロセスの[ロックを解決する](/garbage-collection-overview.md#resolve-locks)番目のステップでの同時スレッドの数を制御します。
-   v8.3.0 以降では、この変数は GC プロセスの[範囲を削除](/garbage-collection-overview.md#delete-ranges)ステップ中の同時スレッドの数も制御します。
-   デフォルトではこの変数は`-1`設定されており、TiDB はワークロードに基づいて適切なスレッド数を自動的に決定できます。
-   この変数が`[1, 256]`の範囲の数値に設定されている場合:
    -   ロックの解決では、この変数に設定された値がスレッド数として直接使用されます。
    -   削除範囲では、この変数に設定された値の 4 分の 1 がスレッド数として使用されます。

### tidb_gc_enable<span class="version-mark">バージョン5.0の新機能</span> {#tidb-gc-enable-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   TiKVのガベージコレクションを有効にします。ガベージコレクションを無効にすると、古いバージョンの行が削除されなくなるため、システムパフォーマンスが低下します。

### tidb_gc_life_time<span class="version-mark">バージョン5.0の新機能</span> {#tidb-gc-life-time-span-class-version-mark-new-in-v5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: TiDBセルフマネージドの場合は`[10m0s, 8760h0m0s]`と[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) `[10m0s, 168h0m0s]`場合[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   各GCでデータが保持される時間制限（Go Durationの形式）。GC発生時、現在の時刻からこの値を引いた時点が安全点となります。

> **注記：**
>
> -   頻繁に更新されるシナリオでは、 `tidb_gc_life_time`に大きな値 (日数または月数) を指定すると、次のような潜在的な問題が発生する可能性があります。
>     -   より大きなstorageの使用
>     -   大量の履歴データは、特に`select count(*) from t`ような範囲クエリの場合、ある程度パフォーマンスに影響を与える可能性があります。
> -   `tidb_gc_life_time`より長く実行されているトランザクションがある場合、GC実行中は、このトランザクションが実行を継続できるように`start_ts`以降のデータが保持されます。例えば、 `tidb_gc_life_time` 10 分に設定されている場合、実行中のすべてのトランザクションのうち、最も早く開始されたトランザクションが 15 分間実行されていると、GCは直近 15 分間のデータを保持します。

### tidb_gc_max_wait_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-gc-max-wait-time-span-class-version-mark-new-in-v6-1-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `86400`
-   範囲: `[600, 31536000]`
-   単位: 秒
-   この変数は、アクティブなトランザクションがGCセーフポイントをブロックする最大時間を設定するために使用されます。GCの実行中、セーフポイントはデフォルトで進行中のトランザクションの開始時刻を超えることはありません。アクティブなトランザクションの実行時間がこの変数値を超えない場合、実行時間がこの値を超えるまでGCセーフポイントはブロックされます。

### tidb_gc_run_interval <span class="version-mark">v5.0 の新機能</span> {#tidb-gc-run-interval-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 期間
-   デフォルト値: `10m0s`
-   範囲: `[10m0s, 8760h0m0s]`
-   GC間隔をGo Durationの形式で指定します（例： `"1h30m"` `"15m"`

### tidb_gc_scan_lock_mode<span class="version-mark">バージョン5.0の新機能</span> {#tidb-gc-scan-lock-mode-span-class-version-mark-new-in-v5-0-span}

> **警告：**
>
> 現在、Green GCは実験的機能です。本番環境での使用は推奨されません。

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `LEGACY`
-   可能な`LEGACY` : `PHYSICAL`
    -   `LEGACY` : 古いスキャン方法を使用します。つまり、Green GC を無効にします。
    -   `PHYSICAL` : 物理スキャン方式を使用します。つまり、Green GC を有効にします。

<CustomContent platform="tidb">

-   この変数は、GCのロック解決ステップにおけるロックのスキャン方法を指定します。変数値が`LEGACY`に設定されている場合、TiDBはリージョンごとにロックをスキャンします。値が`PHYSICAL`の場合、各TiKVノードはRaftレイヤーをバイパスしてデータを直接スキャンできるようになります。これにより、 [休止状態リージョン](/tikv-configuration-file.md#hibernate-regions)機能が有効な場合にGCがすべてのリージョンを起動する影響を効果的に軽減し、ロック解決ステップの実行速度を向上させます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、GCのロック解決ステップにおけるロックのスキャン方法を指定します。変数値が`LEGACY`に設定されている場合、TiDBはリージョンごとにロックをスキャンします。値が`PHYSICAL`の場合、各TiKVノードはRaftレイヤーをバイパスしてデータを直接スキャンできるため、GCがすべてのリージョンを起動する影響を効果的に軽減し、ロック解決ステップの実行速度を向上させます。

</CustomContent>

### tidb_general_log {#tidb-general-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`

<CustomContent platform="tidb-cloud">

-   この変数は、すべてのSQL文をログに記録するかどうかを設定するために使用されます。この機能はデフォルトで無効になっています。問題箇所を特定する際にすべてのSQL文をトレースする必要がある場合は、この機能を有効にしてください。

</CustomContent>

<CustomContent platform="tidb">

-   この変数は、 [ログ](/tidb-configuration-file.md#logfile)内のすべてのSQL文を記録するかどうかを設定するために使用されます。この機能はデフォルトで無効になっています。保守担当者が問題箇所を特定する際にすべてのSQL文をトレースする必要がある場合は、この機能を有効にできます。

-   設定項目を[`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800)指定した場合、一般ログは指定したファイルに別途書き込まれます。

-   [`log.format`](/tidb-configuration-file.md#format)構成項目を使用すると、一般ログを別のファイルに保存するか、他のログと結合するかなど、ログ メッセージの形式を構成できます。

-   [`tidb_redact_log`](#tidb_redact_log)変数を使用すると、一般ログに記録された SQL ステートメントを編集できます。

-   正常に実行されたステートメントのみが一般ログに記録されます。失敗したステートメントは一般ログには記録されず、代わりにTiDBログに`command dispatched failed`メッセージとともに記録されます。

-   この機能のすべての記録をログで確認するには、TiDB構成項目[`log.level`](/tidb-configuration-file.md#level)を`"info"`または`"debug"`に設定し、文字列`"GENERAL_LOG"`をクエリする必要があります。以下の情報が記録されます。
    -   `time` : イベントの時刻。
    -   `conn` : 現在のセッションの ID。
    -   `user` : 現在のセッション ユーザー。
    -   `schemaVersion` : 現在のスキーマ バージョン。
    -   `txnStartTS` : 現在のトランザクションが開始されるタイムスタンプ。
    -   `forUpdateTS` :悲観的トランザクションモードでは、 `forUpdateTS` SQL文の現在のタイムスタンプです。悲観的トランザクションで書き込み競合が発生した場合、TiDBは現在実行中のSQL文を再試行し、このタイムスタンプを更新します。再試行回数は[`max-retry-count`](/tidb-configuration-file.md#max-retry-count)で設定できます。楽観的トランザクションモデルでは、 `forUpdateTS`は`txnStartTS`に相当します。
    -   `isReadConsistency` : 現在のトランザクション分離レベルが Read Committed (RC) であるかどうかを示します。
    -   `current_db` : 現在のデータベースの名前。
    -   `txn_mode` : トランザクションモード。値のオプションは`OPTIMISTIC`と`PESSIMISTIC`です。
    -   `sql` : 現在のクエリに対応する SQL ステートメント。

</CustomContent>

### tidb_non_prepared_plan_cache_size {#tidb-non-prepared-plan-cache-size}

> **警告：**
>
> バージョン7.1.0以降、この変数は非推奨となりました。代わりに[`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は、 [準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)でキャッシュできる実行プランの最大数を制御します。

### tidb_pre_split_regions <span class="version-mark">v8.4.0 の新機能</span> {#tidb-pre-split-regions-span-class-version-mark-new-in-v8-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数は、新規作成テーブルの行分割シャード数のデフォルトを設定するために使用されます。この変数が0以外の値に設定されている場合、TiDBは、 `CREATE TABLE`ステートメントを実行する際に`PRE_SPLIT_REGIONS`シャードの使用を許可するテーブル（例えば、 `NONCLUSTERED`テーブル）にこの属性を自動的に適用します。詳細については、 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)を参照してください。この変数は通常、 [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-new-in-v840)と組み合わせて使用​​され、新しいテーブルをシャード化し、新しいテーブルのリージョンを事前に分割します。

### tidb_generate_binary_plan <span class="version-mark">v6.2.0 の新機能</span> {#tidb-generate-binary-plan-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログとステートメント サマリーにバイナリ エンコードされた実行プランを生成するかどうかを制御します。
-   この変数を`ON`に設定すると、TiDBダッシュボードでビジュアル実行プランを表示できます。ただし、TiDBダッシュボードでは、この変数を有効にした後に生成された実行プランのみがビジュアル表示されます。
-   [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan)ステートメントを実行して、バイナリ プランから特定のプランを解析できます。

### tidb_gogc_tuner_max_value <span class="version-mark">v7.5.0 の新機能</span> {#tidb-gogc-tuner-max-value-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `500`
-   範囲: `[10, 2147483647]`
-   この変数は、GOGC チューナーが調整できる GOGC の最大値を制御するために使用されます。

### tidb_gogc_tuner_min_value <span class="version-mark">v7.5.0 の新機能</span> {#tidb-gogc-tuner-min-value-span-class-version-mark-new-in-v7-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[10, 2147483647]`
-   この変数は、GOGC チューナーが調整できる GOGC の最小値を制御するために使用されます。

### tidb_gogc_tuner_threshold <span class="version-mark">v6.4.0 の新機能</span> {#tidb-gogc-tuner-threshold-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `0.6`
-   範囲: `[0, 0.9)`
-   この変数は、GOGCをチューニングするための最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC Tunerは動作を停止します。

### tidb_guarantee_linearizability<span class="version-mark">バージョン5.0の新機能</span> {#tidb-guarantee-linearizability-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、非同期コミットにおけるコミットTSの計算方法を制御します。デフォルト（値が`ON` ）では、2フェーズコミットはPDサーバーに新しいTSを要求し、そのTSを使用して最終的なコミットTSを計算します。この場合、すべての同時トランザクションの線形化可能性が保証されます。
-   この変数を`OFF`に設定すると、PDサーバーからTSを取得するプロセスがスキップされます。ただし、因果一貫性は保証されますが、線形化可能性は保証されません。詳細については、ブログ投稿[非同期コミット、TiDB 5.0 のトランザクションコミットのアクセラレータ](https://www.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/)をご覧ください。
-   因果一貫性のみが必要なシナリオでは、この変数を`OFF`に設定するとパフォーマンスが向上します。

### tidb_hash_exchange_with_new_collat​​ion {#tidb-hash-exchange-with-new-collation}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、新しい照合順序が有効になっているクラスターで MPP ハッシュ パーティション交換演算子が生成されるかどうかを制御します。1 `true`演算子を生成することを意味し、 `false`演算子を生成しないことを意味します。
-   この変数はTiDBの内部処理に使用されます。この変数を設定することは**推奨されません**。

### tidb_hash_join_concurrency {#tidb-hash-join-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨です。代わりに[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `hash join`アルゴリズムの同時実行性を設定するために使用されます。
-   値が`-1`の場合、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hash_join_version <span class="version-mark">v8.4.0 の新機能</span> {#tidb-hash-join-version-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> この変数で制御される機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `legacy`
-   可能な`optimized` : `legacy`
-   この変数は、TiDBがハッシュ結合の最適化バージョンを使用するかどうかを制御します。デフォルトの値は`legacy`で、最適化バージョンは使用されません。3 に設定すると、TiDBはパフォーマンス向上のため`optimized`ハッシュ結合の実行に最適化バージョンを使用します。

> **注記：**
>
> 現在、最適化されたハッシュ結合は内部結合と外部結合のみをサポートしているため、他の結合については、 `tidb_hash_join_version` `optimized`に設定しても、TiDB は従来のハッシュ結合を使用します。

### tidb_hashagg_final_concurrency {#tidb-hashagg-final-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨です。代わりに[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、第`final`フェーズで並行`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメータが異なっている場合、 `HashAgg`同時に実行され、それぞれ`partial`フェーズと`final`フェーズの 2 つのフェーズで実行されます。
-   値が`-1`の場合、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_hashagg_部分同時実行性 {#tidb-hashagg-partial-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨です。代わりに[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、第`partial`フェーズで並行`hash aggregation`アルゴリズムを実行する同時実行性を設定するために使用されます。
-   集計関数のパラメータが異なっている場合、 `HashAgg`同時に実行され、それぞれ`partial`フェーズと`final`フェーズの 2 つのフェーズで実行されます。
-   値が`-1`の場合、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_historical_stats_duration <span class="version-mark">v6.6.0 の新機能</span> {#tidb-historical-stats-duration-span-class-version-mark-new-in-v6-6-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 期間
-   デフォルト値: `168h` （7日間）
-   この変数は、履歴統計がstorageに保持される期間を制御します。

### tidb_idle_transaction_timeout <span class="version-mark">v7.6.0 の新機能</span> {#tidb-idle-transaction-timeout-span-class-version-mark-new-in-v7-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 31536000]`
-   単位: 秒
-   この変数は、ユーザーセッションにおけるトランザクションのアイドルタイムアウトを制御します。ユーザーセッションがトランザクション状態にあり、この変数の値を超える期間アイドル状態が続くと、TiDB はセッションを終了します。アイドル状態のユーザーセッションとは、アクティブなリクエストがなく、セッションが新しいリクエストを待機している状態を意味します。
-   デフォルト値`0`は無制限を意味します。

### tidb_ignore_prepared_cache_close_stmt<span class="version-mark">バージョン6.0.0の新機能</span> {#tidb-ignore-prepared-cache-close-stmt-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、プリペアドステートメントキャッシュを閉じるコマンドを無視するかどうかを設定するために使用されます。
-   この変数が`ON`に設定されている場合、バイナリプロトコルの`COM_STMT_CLOSE`コマンドとテキストプロトコルの[`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md)ステートメントは無視されます。詳細については[`COM_STMT_CLOSE`コマンドと`DEALLOCATE PREPARE`ステートメントを無視します。](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)参照してください。

### tidb_ignore_inlist_plan_digest <span class="version-mark">v7.6.0 の新機能</span> {#tidb-ignore-inlist-plan-digest-span-class-version-mark-new-in-v7-6-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、プラン ダイジェストを生成するときに、TiDB が異なるクエリ間の`IN`リスト内の要素の違いを無視するかどうかを制御します。

    -   デフォルト値`OFF`の場合、TiDB はプランダイジェストを生成する際に、リスト`IN`の要素の差異（要素数の差異を含む）を無視しません。リスト`IN`の要素の差異は、異なるプランダイジェストを生成します。
    -   `ON`に設定すると、TiDBは`IN`番目のリスト内の要素の差異（要素数の差異を含む）を無視し、 `...`のリスト内の要素をプランダイジェストの`IN`番目のリストに置き換えます。この場合、TiDBは同じタイプの`IN`のクエリに対して同じプランダイジェストを生成します。

### tidb_index_join_batch_size {#tidb-index-join-batch-size}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `25000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup join`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_index_join_double_read_penalty_cost_rate <span class="version-mark">v6.6.0 の新機能</span> {#tidb-index-join-double-read-penalty-cost-rate-span-class-version-mark-new-in-v6-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 18446744073709551615]`
-   この変数は、インデックス結合の選択にペナルティ コストを適用するかどうかを決定し、これにより、オプティマイザがインデックス結合を選択する可能性が低くなり、ハッシュ結合や tiflash 結合などの代替結合方法を選択する可能性が高くなります。
-   インデックス結合を選択すると、多くのテーブル検索リクエストがトリガーされ、リソースを過剰に消費します。この変数を使用すると、オプティマイザがインデックス結合を選択する可能性を低減できます。
-   この変数は、 [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620)変数が`2`に設定されている場合にのみ有効になります。

### tidb_index_lookup_concurrency {#tidb-index-lookup-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨です。代わりに[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。
-   値が`-1`の場合、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_join_concurrency {#tidb-index-lookup-join-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨です。代わりに[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `index lookup join`アルゴリズムの同時実行性を設定するために使用されます。
-   値が`-1`の場合、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_pushdown_policy <span class="version-mark">v8.5.5 の新機能</span> {#tidb-index-lookup-pushdown-policy-span-class-version-mark-new-in-v8-5-5-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `hint-only`
-   `force` `affinity-force`オプション: `hint-only`
-   この変数は、TiDBが`IndexLookUp`演算子をTiKVにプッシュダウンするかどうか、またプッシュダウンするタイミングを制御します。値のオプションは以下のとおりです。
    -   `hint-only` (デフォルト): TiDB は、SQL ステートメントで[`INDEX_LOOKUP_PUSHDOWN`](/optimizer-hints.md#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855)ヒントが明示的に指定されている場合にのみ、 `IndexLookUp`演算子を TiKV にプッシュダウンします。
    -   `affinity-force` : TiDB は、 `AFFINITY`オプションで設定されたテーブルに対してのみプッシュダウンを自動的に有効にします。
    -   `force` : TiDB はすべてのテーブルに対して`IndexLookUp`プッシュダウンを有効にします。

### tidb_index_merge_intersection_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-index-merge-intersection-concurrency-span-class-version-mark-new-in-v6-5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   この変数は、インデックスマージが実行する交差操作の最大同時実行数を設定します。これは、TiDBが動的プルーニングモードでパーティションテーブルにアクセスする場合にのみ有効です。実際の同時実行数は、 `tidb_index_merge_intersection_concurrency`とパーティションテーブルのパーティション数のいずれか小さい方の値になります。
-   デフォルト値`-1` 、値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_index_lookup_size {#tidb-index-lookup-size}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `20000`
-   範囲: `[1, 2147483647]`
-   単位: 行
-   この変数は、 `index lookup`操作のバッチ サイズを設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_index_serial_scan_concurrency {#tidb-index-serial-scan-concurrency}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、 `serial scan`操作の同時実行性を設定するために使用されます。
-   OLAP シナリオでは大きい値を使用し、OLTP シナリオでは小さい値を使用します。

### tidb_init_chunk_size {#tidb-init-chunk-size}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `32`
-   範囲: `[1, 32]`
-   単位: 行
-   この変数は、実行プロセス中の初期チャンクの行数を設定するために使用されます。チャンクの行数は、単一のクエリに必要なメモリ量に直接影響します。クエリ内のすべての列の合計幅とチャンクの行数を考慮することで、単一のチャンクに必要なメモリを大まかに見積もることができます。これをエグゼキューターの同時実行性と組み合わせることで、単一のクエリに必要な合計メモリを概算できます。単一のチャンクの合計メモリは16MiBを超えないようにすることをお勧めします。

### tidb_instance_plan_cache_reserved_percentage <span class="version-mark">v8.4.0 の新機能</span> {#tidb-instance-plan-cache-reserved-percentage-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> 現在、インスタンスプランキャッシュは実験的機能です。本番環境でのご利用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.1`
-   範囲: `[0, 1]`
-   この変数は、メモリのエビクション後に[インスタンスプランキャッシュ](#tidb_enable_instance_plan_cache-new-in-v840)に予約されるアイドルメモリの割合を制御します。インスタンスプランキャッシュによって使用されるメモリが[`tidb_instance_plan_cache_max_size`](#tidb_instance_plan_cache_max_size-new-in-v840)で設定された上限に達すると、TiDBはLRU（Least Recently Used）アルゴリズムを使用して、アイドルメモリの割合が[`tidb_instance_plan_cache_reserved_percentage`](#tidb_instance_plan_cache_reserved_percentage-new-in-v840)で設定された値を超えるまで、メモリから実行プランのエビクションを開始します。

### tidb_instance_plan_cache_max_size <span class="version-mark">v8.4.0 の新機能</span> {#tidb-instance-plan-cache-max-size-span-class-version-mark-new-in-v8-4-0-span}

> **警告：**
>
> 現在、インスタンスプランキャッシュは実験的機能です。本番環境でのご利用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `125829120` (120 MiB)
-   単位: バイト
-   この変数は、 [インスタンスプランキャッシュ](#tidb_enable_instance_plan_cache-new-in-v840)の最大メモリ使用量を設定します。

### tidb_isolation_read_engines <span class="version-mark">v4.0 の新機能</span> {#tidb-isolation-read-engines-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `tikv,tiflash,tidb`
-   この変数は、TiDB がデータを読み取るときに使用できるstorageエンジン リストを設定するために使用されます。

### tidb_last_ddl_info<span class="version-mark">バージョン6.0.0の新機能</span> {#tidb-last-ddl-info-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   タイプ: 文字列
-   これは読み取り専用変数です。TiDB内部で使用され、現在のセッション内で最後に実行されたDDL操作の情報を取得します。
    -   &quot;query&quot;: 最後の DDL クエリ文字列。
    -   &quot;seq_num&quot;: 各DDL操作のシーケンス番号。DDL操作の順序を識別するために使用されます。

### tidb_last_query_info <span class="version-mark">v4.0.14 の新機能</span> {#tidb-last-query-info-span-class-version-mark-new-in-v4-0-14-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   これは読み取り専用変数です。TiDB内部で、最後のDML文のトランザクション情報を照会するために使用されます。取得される情報は以下のとおりです。
    -   `txn_scope` : トランザクションのスコープ。2 または`global` `local`なります。
    -   `start_ts` : トランザクションの開始タイムスタンプ。
    -   `for_update_ts` : 前回実行されたDML文の`for_update_ts`番目。これはTiDBがテストに使用する内部用語です。通常、この情報は無視して構いません。
    -   `error` : エラー メッセージ (ある場合)。
    -   `ru_consumption` : ステートメントの実行に[ロシア](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)消費されました。

### tidb_last_txn_info <span class="version-mark">v4.0.9 の新機能</span> {#tidb-last-txn-info-span-class-version-mark-new-in-v4-0-9-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   この変数は、現在のセッションにおける最後のトランザクション情報を取得するために使用されます。これは読み取り専用変数です。トランザクション情報には以下が含まれます。
    -   トランザクションのスコープ。
    -   TS の開始とコミット。
    -   トランザクションのコミット モード。2 フェーズ、1 フェーズ、または非同期コミットになります。
    -   非同期コミットまたは 1 フェーズ コミットから 2 フェーズ コミットへのトランザクション フォールバックの情報。
    -   エラーが発生しました。

### tidb_last_plan_replayer_token <span class="version-mark">v6.3.0 の新機能</span> {#tidb-last-plan-replayer-token-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   この変数は読み取り専用で、現在のセッションの最後の`PLAN REPLAYER DUMP`の実行の結果を取得するために使用されます。

### tidb_load_based_replica_read_threshold <span class="version-mark">v7.0.0 の新機能</span> {#tidb-load-based-replica-read-threshold-span-class-version-mark-new-in-v7-0-0-span}

<CustomContent platform="tidb">

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   タイプ: 文字列
-   この変数は、負荷ベースのレプリカ読み取りをトリガーするための閾値を設定するために使用されます。リーダーノードの推定キュー時間が閾値を超えると、TiDBはフォロワーノードからのデータの読み取りを優先します。形式は`"100ms"`や`"1s"`などの時間間隔です。詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `"1s"`
-   範囲: `[0s, 1h]`
-   タイプ: 文字列
-   この変数は、負荷ベースのレプリカ読み取りをトリガーするための閾値を設定するために使用されます。リーダーノードの推定キュー時間が閾値を超えると、TiDBはフォロワーノードからのデータの読み取りを優先します。形式は`"100ms"`や`"1s"`などの時間間隔です。詳細については、 [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#scatter-read-hotspots)参照してください。

</CustomContent>

### <code>tidb_load_binding_timeout</code> <span class="version-mark">8.0.0の新機能</span> {#code-tidb-load-binding-timeout-code-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `200`
-   範囲: `(0, 2147483647]`
-   単位: ミリ秒
-   この変数は、バインディングの読み込みのタイムアウトを制御するために使用されます。バインディングの読み込みの実行時間がこの値を超えると、読み込みは停止します。

### <code>tidb_lock_unchanged_keys</code> <span class="version-mark">v7.1.1 および v7.3.0 の新機能</span> {#code-tidb-lock-unchanged-keys-code-span-class-version-mark-new-in-v7-1-1-and-v7-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、以下のシナリオにおいて特定のキーをロックするかどうかを制御するために使用されます。値が`ON`に設定されている場合、これらのキーはロックされます。値が`OFF`に設定されている場合、これらのキーはロックされません。
    -   `INSERT IGNORE`と`REPLACE`ステートメントに重複キーがあります。v6.1.6より前では、これらのキーはロックされていませんでした。この問題は[＃42121](https://github.com/pingcap/tidb/issues/42121)で修正されました。
    -   `UPDATE`ステートメント内のキーの値が変更されていない場合、キーは一意です。v6.5.2 より前では、これらのキーはロックされていませんでした。この問題は[＃36438](https://github.com/pingcap/tidb/issues/36438)で修正されました。
-   トランザクションの一貫性と合理性を維持するため、この値を変更することは推奨されません。TiDBのアップグレードにより、これら2つの修正により深刻なパフォーマンス問題が発生し、ロックなしの動作が許容できる場合（前述の問題を参照）、この変数を`OFF`に設定できます。

### tidb_log_file_max_days <span class="version-mark">v5.3.0 の新機能</span> {#tidb-log-file-max-days-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`

<CustomContent platform="tidb">

-   この変数は、現在のTiDBインスタンスでログを保持する最大日数を設定するために使用されます。この変数の値は、設定ファイル内の[`max-days`](/tidb-configuration-file.md#max-days)設定値にデフォルト設定されます。この変数値の変更は、現在のTiDBインスタンスにのみ影響します。TiDBを再起動すると、変数値はリセットされ、設定値は影響を受けません。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、現在の TiDB インスタンスにログが保持される最大日数を設定するために使用されます。

</CustomContent>

### tidb_low_resolution_tso {#tidb-low-resolution-tso}

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、低精度TSO機能を有効にするかどうかを設定するために使用されます。この機能を有効にすると、TiDBはキャッシュされたタイムスタンプを使用してデータを読み取ります。キャッシュされたタイムスタンプは、デフォルトでは2秒ごとに更新されます。v8.0.0以降では、更新間隔を[`tidb_low_resolution_tso_update_interval`](#tidb_low_resolution_tso_update_interval-new-in-v800)単位で設定できます。
-   主な適用可能なシナリオは、古いデータの読み取りが許容される場合に、小さな読み取り専用トランザクションの TSO 取得のオーバーヘッドを削減することです。
-   v8.3.0 以降、この変数は GLOBAL スコープをサポートします。

### <code>tidb_low_resolution_tso_update_interval</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-tidb-low-resolution-tso-update-interval-code-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2000`
-   範囲: `[10, 60000]`
-   単位: ミリ秒
-   この変数は、低精度 TSO 機能で使用されるキャッシュされたタイムスタンプの更新間隔をミリ秒単位で設定するために使用されます。
-   この変数は[`tidb_low_resolution_tso`](#tidb_low_resolution_tso)が有効な場合にのみ使用できます。

### tidb_max_auto_analyze_time <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-auto-analyze-time-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `43200` (12 時間)
-   範囲: `[0, 2147483647]`
-   単位: 秒
-   この変数は、自動タスク`ANALYZE`の最大実行時間を指定するために使用されます。自動タスク`ANALYZE`の実行時間が指定時間を超えると、タスクは終了します。この変数の値が`0`の場合、自動タスク`ANALYZE`の最大実行時間に制限はありません。

### tidb_max_bytes_before_tiflash_external_group_by<span class="version-mark">バージョン7.0.0の新機能</span> {#tidb-max-bytes-before-tiflash-external-group-by-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashにおけるハッシュ集計演算子の最大メモリ使用量をバイト単位で指定します`GROUP BY`に設定）。メモリ使用量が指定値を超えると、 TiFlash はハッシュ集計演算子によるディスクへの書き込みをトリガーします。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量は無制限、つまりTiFlashハッシュ集計演算子による書き込みはトリガーされません。詳細については、 [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md)参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、通常、集計は複数のTiFlashノードに分散して実行されます。この変数は、単一のTiFlashノードにおける集計演算子の最大メモリ使用量を制御します。
> -   この変数を`-1`に設定すると、 TiFlash は独自の構成項目[`max_bytes_before_external_group_by`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて集計演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、通常、集計は複数のTiFlashノードに分散して実行されます。この変数は、単一のTiFlashノードにおける集計演算子の最大メモリ使用量を制御します。
> -   この変数を`-1`に設定すると、 TiFlash は独自の構成項目`max_bytes_before_external_group_by`の値に基づいて集計演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_join<span class="version-mark">バージョン7.0.0の新機能</span> {#tidb-max-bytes-before-tiflash-external-join-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashにおけるハッシュ結合演算子の最大メモリ使用量を`JOIN`単位で指定します。メモリ使用量が指定値を超えると、 TiFlash はハッシュ結合演算子をトリガーしてディスクに書き出します。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量は無制限、つまりTiFlashハッシュ結合演算子は書き出しをトリガーしません。詳細については、 [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md)参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、結合は通常、複数のTiFlashノードに分散して実行されます。この変数は、単一のTiFlashノードにおける結合演算子の最大メモリ使用量を制御します。
> -   この変数を`-1`に設定すると、 TiFlash は独自の構成項目[`max_bytes_before_external_join`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて結合演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、結合は通常、複数のTiFlashノードに分散して実行されます。この変数は、単一のTiFlashノードにおける結合演算子の最大メモリ使用量を制御します。
> -   この変数を`-1`に設定すると、 TiFlash は独自の構成項目`max_bytes_before_external_join`の値に基づいて結合演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_sort <span class="version-mark">v7.0.0 の新機能</span> {#tidb-max-bytes-before-tiflash-external-sort-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlash内の TopN および Sort 演算子の最大メモリ使用量をバイト単位で指定するために使用されます。メモリ使用量が指定値を超えると、 TiFlash はTopN および Sort 演算子をトリガーしてディスクに書き出します。この変数の値が`-1`の場合、TiDB はこの変数をTiFlashに渡しません。この変数の値が`0`以上の場合にのみ、TiDB はこの変数をTiFlashに渡します。この変数の値が`0`の場合、メモリ使用量は無制限であり、 TiFlash のTopN および Sort 演算子は書き出しをトリガーしません。詳細については、 [TiFlashディスクへの書き込み](/tiflash/tiflash-spill-disk.md)参照してください。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、TopNおよびSortは通常、複数のTiFlashノードで分散実行されます。この変数は、単一のTiFlashノードにおけるTopNおよびSort演算子の最大メモリ使用量を制御します。
> -   この変数を`-1`に設定すると、 TiFlash は独自の構成項目[`max_bytes_before_external_sort`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)の値に基づいて、TopN 演算子と Sort 演算子の最大メモリ使用量を決定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDBクラスタに複数のTiFlashノードがある場合、TopNおよびSortは通常、複数のTiFlashノードで分散実行されます。この変数は、単一のTiFlashノードにおけるTopNおよびSort演算子の最大メモリ使用量を制御します。
> -   この変数を`-1`に設定すると、 TiFlash は独自の構成項目`max_bytes_before_external_sort`の値に基づいて、TopN 演算子と Sort 演算子の最大メモリ使用量を決定します。

</CustomContent>

### tidb_max_chunk_size {#tidb-max-chunk-size}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[32, 2147483647]`
-   単位: 行
-   この変数は、実行プロセス中にチャンク内の最大行数を設定するために使用されます。設定値が大きすぎると、キャッシュの局所性の問題が発生する可能性があります。この変数の推奨値は 65536 以下です。チャンクの行数は、単一のクエリに必要なメモリ量に直接影響します。クエリ内のすべての列の合計幅とチャンクの行数を考慮すると、1 つのチャンクに必要なメモリを大まかに見積もることができます。これをエグゼキュータの同時実行性と組み合わせると、1 つのクエリに必要な合計メモリを大まかに見積もることができます。1 つのチャンクの合計メモリは 16 MiB を超えないようにすることをお勧めします。クエリに大量のデータが含まれ、1 つのチャンクですべてのデータを処理できない場合、TiDB はそれを複数回処理し、チャンク サイズが[`tidb_init_chunk_size`](#tidb_init_chunk_size)から始まり、チャンク サイズが`tidb_max_chunk_size`の値に達するまで、処理の反復ごとにチャンク サイズを 2 倍にします。

### tidb_max_delta_schema_count <span class="version-mark">v2.1.18 および v3.0.5 の新機能</span> {#tidb-max-delta-schema-count-span-class-version-mark-new-in-v2-1-18-and-v3-0-5-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1024`
-   範囲: `[100, 16384]`
-   この変数は、キャッシュ可能なスキーマバージョン（対応するバージョンに変更されたテーブルID）の最大数を設定するために使用されます。値の範囲は100～16384です。

### tidb_max_paging_size <span class="version-mark">v6.3.0 の新機能</span> {#tidb-max-paging-size-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `50000`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサのページング要求処理中の最大行数を設定するために使用されます。値が小さすぎるとTiDBとTiKV間のRPC回数が増加し、値が大きすぎるとデータのロードやフルテーブルスキャンなど、場合によってはメモリ使用量が過剰になります。この変数のデフォルト値は、OLAPシナリオよりもOLTPシナリオで優れたパフォーマンスをもたらします。アプリケーションがstorageエンジンとしてTiKVのみを使用している場合は、OLAPワークロードクエリを実行する際にこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

### tidb_max_tiflash_threads <span class="version-mark">v6.1.0 の新機能</span> {#tidb-max-tiflash-threads-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、 TiFlashがリクエストを実行する際の最大同時実行数を設定するために使用されます。デフォルト値は`-1`で、このシステム変数は無効であり、最大同時実行数はTiFlash構成`profiles.default.max_threads`の設定に依存することを示します。値が`0`の場合、最大スレッド数はTiFlashによって自動的に設定されます。

### tidb_mem_oom_action <span class="version-mark">v6.1.0 の新機能</span> {#tidb-mem-oom-action-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `CANCEL`
-   可能な`LOG` : `CANCEL`

<CustomContent platform="tidb">

-   単一のSQL文が`tidb_mem_quota_query`で指定されたメモリクォータを超え、ディスクに書き込めない場合にTiDBが実行する操作を指定します。詳細は[TiDB メモリ制御](/configure-memory-usage.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   単一の SQL ステートメントが[`tidb_mem_quota_query`](#tidb_mem_quota_query)で指定されたメモリクォータを超え、ディスクに書き込むことができない場合に TiDB が実行する操作を指定します。

</CustomContent>

-   デフォルト値は`CANCEL`ですが、TiDB v4.0.2 以前のバージョンではデフォルト値は`LOG`です。
-   この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_mem_quota_analyze <span class="version-mark">v6.1.0 の新機能</span> {#tidb-mem-quota-analyze-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト
-   この変数は、TiDB 統計更新の最大メモリ使用量を制御します。このようなメモリ使用量は、手動で[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行した場合と、TiDB がバックグラウンドでタスクを自動分析した場合に発生します。メモリ使用量の合計がこのしきい値を超えると、ユーザーが実行した`ANALYZE`終了し、より低いサンプリングレートを試すか、後で再試行するように促すエラーメッセージが報告されます。メモリしきい値を超えたために TiDB バックグラウンドでの自動タスクが終了した場合、使用されているサンプリングレートがデフォルト値よりも高い場合、TiDB はデフォルトのサンプリングレートを使用して更新を再試行します。この変数値が負またはゼロの場合、TiDB は手動更新タスクと自動更新タスクの両方のメモリ使用量を制限しません。

> **注記：**
>
> `auto_analyze` 、TiDB スタートアップ構成ファイルで`run-auto-analyze`有効になっている場合にのみ、TiDB クラスターでトリガーされます。

### tidb_mem_quota_apply_cache<span class="version-mark">バージョン5.0の新機能</span> {#tidb-mem-quota-apply-cache-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `33554432` (32 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、 `Apply`オペレータ内のローカル キャッシュのメモリ使用量しきい値を設定するために使用されます。
-   `Apply`の演算子のローカルキャッシュは、 `Apply`番目の演算子の計算を高速化するために使用されます。変数を`0`に設定すると、 `Apply`キャッシュ機能を無効にすることができます。

### tidb_mem_quota_binding_cache<span class="version-mark">バージョン6.0.0の新機能</span> {#tidb-mem-quota-binding-cache-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[0, 2147483647]`
-   単位: バイト
-   この変数は、バインディングのキャッシュに使用されるメモリのしきい値を設定するために使用されます。
-   システムが過剰なバインディングを作成またはキャプチャし、メモリ空間の過剰使用につながる場合、TiDBはログに警告を返します。この場合、キャッシュは利用可能なすべてのバインディングを保持できないか、どのバインディングを保存するかを決定することができません。そのため、一部のクエリではバインディングが失われる可能性があります。この問題に対処するには、この変数の値を増やすことができます。これにより、バインディングのキャッシュに使用されるメモリが増加します。このパラメータを変更した後、 `admin reload bindings`実行してバインディングを再読み込みし、変更を検証する必要があります。

### tidb_mem_quota_query {#tidb-mem-quota-query}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1073741824` (1 GiB)
-   範囲: `[-1, 9223372036854775807]`
-   単位: バイト

<CustomContent platform="tidb">

-   TiDB v6.1.0より前のバージョンでは、これはセッションスコープ変数であり、 `tidb.toml`の`mem-quota-query`の値が初期値として使用されます。v6.1.0以降では、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0より前のバージョンでは、この変数は**クエリ**のメモリクォータのしきい値を設定するために使用されます。実行中のクエリのメモリクォータがこのしきい値を超えた場合、TiDBは[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0以降のバージョンでは、この変数は**セッション**のメモリクォータのしきい値を設定するために使用されます。実行中のセッションのメモリクォータがしきい値を超えた場合、TiDBは[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。TiDB v6.5.0以降では、セッションのメモリ使用量には、セッション内のトランザクションによって消費されたメモリが含まれることに注意してください。TiDB v6.5.0以降のバージョンにおけるトランザクションのメモリ使用量の制御動作については、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)参照してください。
-   変数値を`0`または`-1`に設定すると、メモリのしきい値は正の無限大になります。128 より小さい値を設定すると、デフォルトで`128`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB v6.1.0より前のバージョンでは、これはセッションスコープ変数です。v6.1.0以降では、 `tidb_mem_quota_query`は`SESSION | GLOBAL`スコープ変数です。
-   TiDB v6.5.0より前のバージョンでは、この変数は**クエリ**のメモリクォータのしきい値を設定するために使用されます。実行中のクエリのメモリクォータがこのしきい値を超えた場合、TiDBは[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。
-   TiDB v6.5.0以降では、この変数は**セッション**のメモリクォータのしきい値を設定するために使用されます。実行中のセッションのメモリクォータがしきい値を超えた場合、TiDBは[`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610)で定義された操作を実行します。TiDB v6.5.0以降では、セッションのメモリ使用量には、セッション内のトランザクションによって消費されたメモリが含まれることに注意してください。
-   変数値を`0`または`-1`に設定すると、メモリのしきい値は正の無限大になります。128 より小さい値を設定すると、デフォルトで`128`になります。

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio {#tidb-memory-debug-mode-alarm-ratio}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   この変数は、TiDBメモリデバッグ モードで許可されるメモリ統計エラー値を表します。
-   この変数はTiDBの内部テストに使用されます。この変数を設定することは**推奨されません**。

### tidb_memory_debug_mode_min_heap_inuse {#tidb-memory-debug-mode-min-heap-inuse}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   この変数はTiDBの内部テストに使用されます。この変数を設定することは**推奨されません**。この変数を有効にすると、TiDBのパフォーマンスに影響します。
-   このパラメータを設定すると、TiDBはメモリデバッグモードに入り、メモリトラッキングの精度を分析します。TiDBは後続のSQL文の実行中に頻繁にGCをトリガーし、実際のメモリ使用量とメモリ統計を比較します。現在のメモリ使用量が`tidb_memory_debug_mode_min_heap_inuse`を超え、メモリ統計エラーが`tidb_memory_debug_mode_alarm_ratio`超える場合、TiDBは関連するメモリ情報をログとファイルに出力します。

### tidb_memory_usage_alarm_ratio {#tidb-memory-usage-alarm-ratio}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0.0, 1.0]`

<CustomContent platform="tidb">

-   この変数は、tidb-server のメモリアラームをトリガーするメモリ使用率を設定します。デフォルトでは、TiDB のメモリ使用量が総メモリの 70% を超え、かつ[警報条件](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage)のいずれかの条件に該当する場合、TiDB はアラームログを出力。
-   この変数が`0`または`1`に設定されている場合、メモリしきい値アラーム機能は無効になります。
-   この変数が`0`より大きく`1`より小さい値に設定されている場合、メモリしきい値アラーム機能が有効になっていることを意味します。

    -   システム変数[`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640)の値が`0`の場合、メモリアラームしきい値は`tidb_memory-usage-alarm-ratio * system memory size`になります。
    -   システム変数`tidb_server_memory_limit`の値が 0 より大きく設定されている場合、メモリアラームしきい値は`tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [tidb-serverメモリアラーム](https://docs.pingcap.com/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage)をトリガーするメモリ使用率を設定します。
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
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `5`
-   範囲: `[1, 10000]`
-   tidb-server のメモリ使用量がメモリアラームしきい値を超えてアラームがトリガーされると、TiDB はデフォルトで直近 5 件のアラーム中に生成されたステータスファイルのみを保持します。この変数でこの数を調整できます。

### tidb_merge_join_concurrency {#tidb-merge-join-concurrency}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   範囲: `[1, 256]`
-   デフォルト値: `1`
-   この変数は、クエリが実行されるときに`MergeJoin`演算子の同時実行性を設定します。
-   この変数を設定することは**推奨されません**。この変数の値を変更すると、データの正確性に問題が生じる可能性があります。

### tidb_merge_partition_stats_concurrency {#tidb-merge-partition-stats-concurrency}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `1`
-   この変数は、TiDB がパーティションテーブルを分析するときに、パーティションテーブルの統計をマージする同時実行性を指​​定します。

### tidb_enable_async_merge_global_stats <span class="version-mark">v7.5.0 の新機能</span> {#tidb-enable-async-merge-global-stats-span-class-version-mark-new-in-v7-5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON` 。TiDB を v7.5.0 より前のバージョンから v7.5.0 以降のバージョンにアップグレードする場合、デフォルト値は`OFF`になります。
-   この変数は、OOM の問題を回避するために TiDB がグローバル統計を非同期的にマージするために使用されます。

### tidb_metric_query_range_duration <span class="version-mark">v4.0 の新機能</span> {#tidb-metric-query-range-duration-span-class-version-mark-new-in-v4-0-span}

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

### tidb_metric_query_step <span class="version-mark">v4.0 の新機能</span> {#tidb-metric-query-step-span-class-version-mark-new-in-v4-0-span}

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

### tidb_min_paging_size <span class="version-mark">v6.2.0 の新機能</span> {#tidb-min-paging-size-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `128`
-   範囲: `[1, 9223372036854775807]`
-   単位: 行
-   この変数は、コプロセッサのページング要求処理中の最小行数を設定するために使用されます。この変数を小さく設定しすぎると、TiDBとTiKV間のRPC要求数が増加し、大きく設定しすぎると、IndexLookup with Limitを使用したクエリ実行時にパフォーマンスが低下する可能性があります。この変数のデフォルト値は、OLAPシナリオよりもOLTPシナリオで優れたパフォーマンスをもたらします。アプリケーションがstorageエンジンとしてTiKVのみを使用している場合は、OLAPワークロードクエリを実行する際にこの変数の値を増やすことを検討してください。これにより、パフォーマンスが向上する可能性があります。

![Paging size impact on TPCH](/media/paging-size-impact-on-tpch.png)

この図に示すように、 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540)有効になっている場合、TPCH のパフォーマンスは`tidb_min_paging_size`と[`tidb_max_paging_size`](#tidb_max_paging_size-new-in-v630)の設定によって影響を受けます。縦軸は実行時間で、値が小さいほど優れています。

### tidb_mpp_store_fail_ttl {#tidb-mpp-store-fail-ttl}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 期間
-   デフォルト値: `0s` 。v8.5.3 以前のバージョンでは、デフォルト値は`60s`です。
-   新しく起動したTiFlashノードはサービスを提供していません。クエリの失敗を防ぐため、TiDBはtidbサーバーから新しく起動したTiFlashノードへのクエリ送信を制限します。この変数は、新しく起動したTiFlashノードにリクエストが送信されない時間範囲を示します。

### tidb_multi_statement_mode <span class="version-mark">v4.0.11 の新機能</span> {#tidb-multi-statement-mode-span-class-version-mark-new-in-v4-0-11-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   `ON` `WARN`値: `OFF`
-   この変数は、同じ`COM_QUERY`呼び出しで複数のクエリを実行できるようにするかどうかを制御します。
-   SQLインジェクション攻撃の影響を軽減するため、TiDBはデフォルトで、 `COM_QUERY`呼び出しで複数のクエリが実行されないようにするようになりました。この変数は、以前のバージョンのTiDBからのアップグレードパスの一部として使用することを目的としています。以下の動作が適用されます。

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
> 安全と考えられるのはデフォルト値の`OFF`のみです。アプリケーションが以前のバージョンのTiDB向けに設計されている場合は、設定値`tidb_multi_statement_mode=ON`必要になる場合があります。アプリケーションで複数ステートメントのサポートが必要な場合は、 `tidb_multi_statement_mode`ではなく、クライアントライブラリが提供する設定値を使用することをお勧めします。例：
>
> -   [go-sql-ドライバー](https://github.com/go-sql-driver/mysql#multistatements) ( `multiStatements` )
> -   [コネクタ/J](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) ( `allowMultiQueries` )
> -   PHP [MySQL](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) ( `mysqli_multi_query` )

### tidb_nontransactional_ignore_error <span class="version-mark">v6.1.0 の新機能</span> {#tidb-nontransactional-ignore-error-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、非トランザクション DML ステートメントでエラーが発生した場合に、すぐにエラーを返すかどうかを指定します。
-   値が`OFF`に設定されている場合、非トランザクションDML文は最初のエラーで直ちに停止し、エラーを返します。後続のバッチはすべてキャンセルされます。
-   値が`ON`に設定されている場合、バッチでエラーが発生すると、すべてのバッチが実行されるまで後続のバッチが継続して実行されます。実行プロセス中に発生したすべてのエラーは、結果にまとめて返されます。

### tidb_opt_agg_push_down {#tidb-opt-agg-push-down}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが Join、Projection、および UnionAll の前の位置に集計関数をプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリで集計操作が遅い場合は、変数値を ON に設定できます。

### tidb_opt_broadcast_cartesian_join {#tidb-opt-broadcast-cartesian-join}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2]`
-   ブロードキャスト カテシアン結合を許可するかどうかを示します。
-   `0`ブロードキャスト カテシアン結合が許可されないことを意味します。 `1` [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50)に基づいて許可されることを意味します。 `2`テーブル サイズがしきい値を超えても常に許可されることを意味します。
-   この変数は TiDB 内で内部的に使用されるため、その値を変更することはお勧めし**ません**。

### tidb_opt_concurrency_factor {#tidb-opt-concurrency-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiDBでGolangのgoroutineを起動する際のCPUコストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_copcpu_factor {#tidb-opt-copcpu-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKVコプロセッサーが1行を処理するのに必要なCPUコストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_相関係数 {#tidb-opt-correlation-exp-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 2147483647]`
-   列順序の相関に基づいて行数を推定する方法が利用できない場合、ヒューリスティック推定法が使用されます。この変数は、ヒューリスティック推定法の動作を制御するために使用されます。
    -   値が 0 の場合、ヒューリスティック手法は使用されません。
    -   値が0より大きい場合:
        -   値が大きいほど、ヒューリスティックな方法でインデックス スキャンが使用される可能性が高くなります。
        -   値が小さいほど、ヒューリスティックな方法でテーブルスキャンが使用される可能性が高くなります。

### tidb_opt_相関しきい値 {#tidb-opt-correlation-threshold}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   デフォルト値: `0.9`
-   範囲: `[0, 1]`
-   この変数は、列順序の相関を用いた行数の推定を有効にするかどうかを決定する閾値を設定するために使用されます。現在の列と`handle`番目の列の順序の相関がこの閾値を超える場合、この手法が有効になります。

### tidb_opt_cpu_factor {#tidb-opt-cpu-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `3.0`
-   TiDBが1行を処理するのに必要なCPUコストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨され**ません**。

### <code>tidb_opt_derive_topn</code><span class="version-mark">バージョン7.0.0の新機能</span> {#code-tidb-opt-derive-topn-code-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   [ウィンドウ関数からTopNまたはLimitを導出する](/derive-topn-from-window.md)の最適化ルールを有効にするかどうかを制御します。

### tidb_opt_desc_factor {#tidb-opt-desc-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `3.0`
-   TiKVがディスクから1行を降順でスキャンするのにかかるコストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_disk_factor {#tidb-opt-disk-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 18446744073709551615]`
-   デフォルト値: `1.5`
-   TiDBが一時ディスクから1バイトのデータを読み書きする際のI/Oコストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨され**ません**。

### tidb_opt_distinct_agg_push_down {#tidb-opt-distinct-agg-push-down}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが、集計関数を`distinct` ( `select count(distinct a) from t`など) でコプロセッサーにプッシュダウンする最適化操作を実行するかどうかを設定するために使用されます。
-   クエリ内で`distinct`演算を含む集計関数が遅い場合は、変数値を`1`に設定できます。

以下の例では、 `tidb_opt_distinct_agg_push_down`有効になる前に、TiDB は TiKV からすべてのデータを読み取り、TiDB 側で`distinct`実行する必要があります。5 `tidb_opt_distinct_agg_push_down`有効になった後、 `distinct a` コプロセッサーにプッシュダウンされ、 `group by`列目の`test.t.a` `HashAgg_5`に追加されます。

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

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザが列順序の相関に基づいて行数を推定するかどうかを制御するために使用されます。

### tidb_opt_enable_hash_join <span class="version-mark">v6.5.6、v7.1.2、v7.4.0 の新機能</span> {#tidb-opt-enable-hash-join-span-class-version-mark-new-in-v6-5-6-v7-1-2-and-v7-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザがテーブルに対してハッシュ結合を選択するかどうかを制御するために使用されます。デフォルトの値は`ON`です`OFF`に設定すると、他の結合アルゴリズムが利用できない場合を除き、オプティマイザは実行プランを生成する際にハッシュ結合を選択しません。
-   システム変数`tidb_opt_enable_hash_join`と`HASH_JOIN`ヒントの両方が設定されている場合、 `HASH_JOIN`ヒントが優先されます。 `tidb_opt_enable_hash_join` `OFF`に設定されている場合でも、クエリで`HASH_JOIN`ヒントを指定すると、TiDB オプティマイザーはハッシュ結合プランを適用します。

### tidb_opt_enable_non_eval_scalar_subquery <span class="version-mark">v7.3.0 の新機能</span> {#tidb-opt-enable-non-eval-scalar-subquery-span-class-version-mark-new-in-v7-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `EXPLAIN`文が最適化段階で展開可能な定数サブクエリの実行を無効にするかどうかを制御するために使用します。この変数が`OFF`に設定されている場合、 `EXPLAIN`文は最適化段階でサブクエリを事前に展開します。この変数が`ON`に設定されている場合、 `EXPLAIN`文は最適化段階でサブクエリを展開しません。詳細については、 [サブクエリの展開を無効にする](/explain-walkthrough.md#disable-the-early-execution-of-subqueries)参照してください。

### tidb_opt_enable_late_materialization <span class="version-mark">v7.0.0 の新機能</span> {#tidb-opt-enable-late-materialization-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [TiFlashの遅い実体化](/tiflash/tiflash-late-materialization.md)機能を有効にするかどうかを制御するために使用します。TiFlashの遅延マテリアライゼーションは[高速スキャンモード](/tiflash/use-fastscan.md)では有効にならないことに注意してください。
-   この変数を`OFF`に設定してTiFlashの遅延マテリアライゼーション機能を無効にした場合、フィルタ条件（ `WHERE`句）を含む`SELECT`文を処理するために、 TiFlashはフィルタリング前に必要な列のすべてのデータをスキャンします。この変数を`ON`に設定してTiFlashの遅延マテリアライゼーション機能を有効にすると、 TiFlashはまずTableScan演算子にプッシュダウンされたフィルタ条件に関連する列データをスキャンし、条件を満たす行をフィルタリングした後、これらの行の他の列のデータをスキャンしてさらなる計算を行うため、IOスキャンとデータ処理の計算を削減できます。

### tidb_opt_enable_mpp_shared_cte_execution <span class="version-mark">v7.2.0 の新機能</span> {#tidb-opt-enable-mpp-shared-cte-execution-span-class-version-mark-new-in-v7-2-0-span}

> **警告：**
>
> この変数で制御される機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 TiFlash MPPで非再帰的な[共通テーブル式（CTE）](/sql-statements/sql-statement-with.md)実行するかどうかを制御します。デフォルトでは、この変数が無効になっている場合、CTEはTiDBで実行されますが、この機能を有効にした場合と比較してパフォーマンスに大きな差が生じます。

### tidb_opt_enable_fuzzy_binding <span class="version-mark">v7.6.0 の新機能</span> {#tidb-opt-enable-fuzzy-binding-span-class-version-mark-new-in-v7-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 [データベース間のバインディング](/sql-plan-management.md#cross-database-binding)機能を有効にするかどうかを制御します。

### tidb_opt_enable_no_decorrelate_in_select <span class="version-mark">v8.5.4 の新機能</span> {#tidb-opt-enable-no-decorrelate-in-select-span-class-version-mark-new-in-v8-5-4-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが`SELECT`リスト内のサブクエリを含むすべてのクエリに[`NO_DECORRELATE()`](/optimizer-hints.md#no_decorrelate)ヒントを適用するかどうかを制御します。

### tidb_opt_enable_semi_join_rewrite <span class="version-mark">v8.5.4 の新機能</span> {#tidb-opt-enable-semi-join-rewrite-span-class-version-mark-new-in-v8-5-4-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザがサブクエリを含むすべてのクエリに[`SEMI_JOIN_REWRITE()`](/optimizer-hints.md#semi_join_rewrite)ヒントを適用するかどうかを制御します。

### tidb_opt_fix_control <span class="version-mark">v6.5.3 および v7.1.0 の新機能</span> {#tidb-opt-fix-control-span-class-version-mark-new-in-v6-5-3-and-v7-1-0-span}

<CustomContent platform="tidb">

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 文字列
-   デフォルト値: `""`
-   この変数は、オプティマイザの一部の内部動作を制御するために使用されます。
-   オプティマイザの動作は、ユーザーシナリオやSQL文によって異なる場合があります。この変数は、オプティマイザをよりきめ細かく制御し、アップグレード後にオプティマイザの動作変更によって発生するパフォーマンスの低下を防ぐのに役立ちます。
-   より詳しい紹介については[オプティマイザー修正コントロール](/optimizer-fix-controls.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 文字列
-   デフォルト値: `""`
-   この変数は、オプティマイザの一部の内部動作を制御するために使用されます。
-   オプティマイザの動作は、ユーザーシナリオやSQL文によって異なる場合があります。この変数は、オプティマイザをよりきめ細かく制御し、アップグレード後にオプティマイザの動作変更によって発生するパフォーマンスの低下を防ぐのに役立ちます。
-   より詳しい紹介については[オプティマイザー修正コントロール](/optimizer-fix-controls.md)参照してください。

</CustomContent>

### tidb_opt_force_inline_cte<span class="version-mark">バージョン6.3.0の新機能</span> {#tidb-opt-force-inline-cte-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、セッション全体の共通テーブル式（CTE）をインライン化するかどうかを制御するために使用されます。デフォルト値は`OFF`で、これはCTEのインライン化がデフォルトで強制されないことを意味します。ただし、 `MERGE()`ヒントを指定することで、CTEをインライン化することは可能です。この変数を`ON`に設定すると、このセッション内のすべてのCTE（再帰CTEを除く）が強制的にインライン化されます。

### tidb_opt_advanced_join_hint<span class="version-mark">バージョン7.0.0の新機能</span> {#tidb-opt-advanced-join-hint-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`HASH_JOIN()`ヒント](/optimizer-hints.md#hash_joint1_name--tl_name-)や[`MERGE_JOIN()`ヒント](/optimizer-hints.md#merge_joint1_name--tl_name-)などの結合方法ヒントが、 [`LEADING()`ヒント](/optimizer-hints.md#leadingt1_name--tl_name-)の使用を含む結合したテーブルの再配置最適化プロセスに影響を与えるかどうかを制御するために使用します。デフォルト値は`ON`で、影響を与えないことを意味します。 `OFF`に設定すると、結合方法ヒントと`LEADING()`ヒントが同時に使用されるシナリオで競合が発生する可能性があります。

> **注記：**
>
> v7.0.0より前のバージョンの動作は、この変数を`OFF`に設定した場合の動作と一致しています。以前のバージョンからv7.0.0以降のクラスターにアップグレードする場合、前方互換性を確保するため、この変数は`OFF`に設定されます。より柔軟なヒント動作を得るには、パフォーマンスの低下がないことを条件に、この変数を`ON`に切り替えることを強くお勧めします。

### tidb_opt_insubq_to_join_and_agg {#tidb-opt-insubq-to-join-and-agg}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
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

    `aa`列目の`t1` `unique`と`not null`に制限されている場合、集計なしで次のステートメントを使用できます。

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold {#tidb-opt-join-reorder-threshold}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、TiDB 結合したテーブルの再配置アルゴリズムの選択を制御するために使用されます。Join 結合したテーブルの再配置に参加するノードの数がこのしきい値より大きい場合、TiDBは貪欲アルゴリズムを選択し、このしきい値より小さい場合、TiDBは動的計画法アルゴリズムを選択します。
-   現在、OLTPクエリの場合はデフォルト値を維持することをお勧めします。OLAPクエリの場合は、OLAPシナリオでの接続順序を改善するために、変数値を10～15に設定することをお勧めします。

### tidb_opt_limit_push_down_threshold {#tidb-opt-limit-push-down-threshold}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   この変数は、Limit または TopN 演算子を TiKV まで押し下げるかどうかを決定するしきい値を設定するために使用されます。
-   Limit演算子またはTopN演算子の値がこのしきい値以下の場合、これらの演算子は強制的にTiKVにプッシュダウンされます。この変数は、Limit演算子またはTopN演算子がTiKVにプッシュダウンされないという、誤った推定値による問題を解決します。

### tidb_opt_メモリ係数 {#tidb-opt-memory-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `0.001`
-   TiDBが1行を格納するために必要なメモリコストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">v5.1.0 の新機能</span> {#tidb-opt-mpp-outer-join-fixed-build-side-span-class-version-mark-new-in-v5-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   変数値が`ON`場合、左結合演算子は常に内部テーブルをビルド側として使用し、右結合演算子は常に外部テーブルをビルド側として使用します。値を`OFF`に設定すると、外部結合演算子はどちらの側のテーブルもビルド側として使用できます。

### tidb_opt_network_factor {#tidb-opt-network-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.0`
-   ネットワークを介して1バイトのデータを転送する際の正味コストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_objective<span class="version-mark">バージョン7.4.0の新機能</span> {#tidb-opt-objective-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `moderate`
-   可能な`determinate` : `moderate`
-   この変数はオプティマイザの目的を制御します。1 `moderate` TiDB v7.4.0 より前のバージョンのデフォルトの動作を維持し、オプティマイザはより多くの情報を使用してより優れた実行プランを生成しようとします。3 `determinate`はより保守的になる傾向があり、実行プランをより安定させます。
-   リアルタイム統計とは、DML文に基づいて自動的に更新された行の総数と変更された行の数です。この変数を`moderate` （デフォルト）に設定すると、TiDBはリアルタイム統計に基づいて実行計画を生成します。この変数を`determinate`に設定すると、TiDBは実行計画の生成にリアルタイム統計を使用しなくなり、実行計画の安定性が向上します。
-   長期にわたって安定したOLTPワークロードの場合、またはユーザーが既存の実行プランに満足している場合は、予期せぬ実行プランの変更の可能性を低減するために、モード`determinate`使用をお勧めします。さらに、統計情報の変更を防ぎ、実行プランをさらに安定させるために、モード[`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)使用することもできます。

### tidb_opt_ordering_index_selectivity_ratio<span class="version-mark">バージョン8.0.0の新機能</span> {#tidb-opt-ordering-index-selectivity-ratio-span-class-version-mark-new-in-v8-0-0-span}

-   スコープ: セッション | グローバル

-   クラスターに持続: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい

-   タイプ: フロート

-   デフォルト値: `-1`

-   範囲: `[-1, 1]`

-   この変数は、SQL ステートメントに`ORDER BY`と`LIMIT`個の句があるが、一部のフィルター条件をカバーしていない場合に、SQL ステートメント`ORDER BY`に一致するインデックスの推定行数を制御します。

-   これは、システム変数[tidb_opt_ordering_index_selectivity_threshold](#tidb_opt_ordering_index_selectivity_threshold-new-in-v700)と同じクエリ パターンに対応します。

-   適格な行が見つかる可能性のある範囲の比率またはパーセンテージを適用することによって実装が異なります。

-   `-1` （デフォルト）または`0`未満の値を指定すると、この比率は無効になります。5から`0`まで`1`値は、0%から100%の比率を適用します（たとえば、 `0.5` `50%`に相当します）。

-   以下の例では、テーブル`t`は合計 1,000,000 行が含まれています。クエリは同じですが、 `tidb_opt_ordering_index_selectivity_ratio`の値は異なります。この例のクエリには、行のごく一部（1,000,000 行中 9,000 行）を修飾する`WHERE`節の述語が含まれています。7 `ORDER BY a`をサポートするインデックス（インデックス`ia` ）はありますが、 `b`のフィルターはこのインデックスには含まれていません。実際のデータ分布によっては、 `WHERE`節と`LIMIT 1`に一致する行は、非フィルタリングインデックスのスキャン時に最初にアクセスされる行として見つかる場合もあれば、最悪の場合、ほぼすべての行が処理された後に見つかる場合もあります。

-   各例では、インデックスヒントを使用してestRowsへの影響を示します。最終的なプランの選択は、他のプランの可用性とコストによって異なります。

-   最初の例では、既存の推定式を使用するデフォルト値`-1`を使用しています。デフォルトでは、条件に該当する行が見つかる前に、推定のためにごく一部の行がスキャンされます。

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

-   2 番目の例では`0`使用されており、これは、条件に該当する行が見つかる前に 0% の行がスキャンされることを想定しています。

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

-   3番目の例では`0.1`使用しています。これは、条件を満たす行が見つかるまでに行の10%がスキャンされると想定しています。この条件は非常に選択的であり、条件を満たす行は全体の1%のみです。したがって、最悪のシナリオでは、条件を満たす1%を見つけるまでに行の99%をスキャンする必要がある可能性があります。この99%の10%は約9.9%であり、estRowsに反映されています。

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

-   4 番目の例では`1.0`使用されており、これは、条件に該当する行が見つかる前に 100% の行がスキャンされることを想定しています。

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

-   5番目の例も`1.0`使用していますが、 `a`に述語を追加することで、最悪のシナリオにおけるスキャン範囲を制限しています。これは、 `WHERE a <= 9000`インデックスに一致し、約9,000行が条件を満たすためです。 `b`のフィルタ述語がインデックスに存在しないため、 `b <= 9000`一致する行を見つける前に、約9,000行すべてがスキャンされると考えられます。

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

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">v7.0.0 の新機能</span> {#tidb-opt-ordering-index-selectivity-threshold-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、SQL ステートメントにフィルタ条件を持つ句が`ORDER BY`または`LIMIT`ある場合に、オプティマイザがインデックスを選択する方法を制御するために使用されます。
-   このようなクエリの場合、オプティマイザは、 `ORDER BY`と`LIMIT`番目の句を満たす対応するインデックスを選択することを検討します（このインデックスがどのフィルタ条件も満たさない場合でも）。ただし、データ分布の複雑さにより、このシナリオではオプティマイザが最適ではないインデックスを選択する可能性があります。
-   この変数は閾値を表します。フィルタリング条件を満たすインデックスが存在し、その選択度の推定値がこの閾値よりも低い場合、オプティマイザは`ORDER BY`と`LIMIT`を満たすために使用されるインデックスの選択を避けます。代わりに、フィルタリング条件を満たすインデックスを優先します。
-   たとえば、変数が`0`に設定されている場合、オプティマイザはデフォルトの動作を維持します。 `1`に設定されている場合、オプティマイザは常にフィルタ条件を満たすインデックスの選択を優先し、 `ORDER BY`と`LIMIT`両方の句を満たすインデックスの選択を回避します。
-   次の例では、テーブル`t`には合計 1,000,000 行があります。列`b`のインデックスを使用する場合、推定行数は約 8,748 行なので、選択度の推定値は約 0.0087 になります。デフォルトでは、オプティマイザは列`a`のインデックスを選択します。しかし、この変数を 0.01 に設定すると、列`b`のインデックスの選択度 (0.0087) が 0.01 未満になるため、オプティマイザは列`b`のインデックスを選択します。

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

### tidb_opt_prefer_range_scan<span class="version-mark">バージョン5.0の新機能</span> {#tidb-opt-prefer-range-scan-span-class-version-mark-new-in-v5-0-span}

> **注記：**
>
> v8.4.0 以降、この変数のデフォルト値は`OFF`から`ON`に変更されます。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数の値が`ON`場合、オプティマイザは、統計のないテーブル (疑似統計) または空のテーブル (ゼロ統計) に対して、完全なテーブルスキャンよりも範囲スキャンを優先します。
-   次の例では、 `tidb_opt_prefer_range_scan`有効にする前は、TiDBオプティマイザはフルテーブルスキャンを実行します。3 `tidb_opt_prefer_range_scan`有効にすると、オプティマイザはインデックス範囲スキャンを選択します。

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

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `ON`
-   この変数は、不要なテーブル検索を回避し、クエリのパフォーマンスを向上させるために、TiDB オプティマイザーが一部のフィルター条件をプレフィックス インデックスにプッシュダウンするかどうかを制御します。
-   この変数値が`ON`に設定されると、一部のフィルタ条件がプレフィックスインデックスにプッシュダウンされます。例えば、テーブルの`col`番目の列がインデックスプレフィックス列であるとします。クエリ内の`col is null`または`col is not null`条件は、テーブル検索のフィルタ条件ではなく、インデックスのフィルタ条件として処理されるため、不要なテーブル検索が回避されます。

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

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON` 。v8.3.0 より前では、デフォルト値は`OFF`です。
-   オプティマイザが`Projection`の演算子をTiKVコプロセッサにプッシュダウンすることを許可するかどうかを指定します。有効にすると、オプティマイザは以下の3種類の`Projection`番目の演算子をTiKVにプッシュダウンする可能性があります。
    -   演算子の最上位の式はすべて[JSONクエリ関数](/functions-and-operators/json-functions/json-functions-search.md)または[JSON値属性関数](/functions-and-operators/json-functions/json-functions-return.md)です。例: `SELECT JSON_EXTRACT(data, '$.name') FROM users;` 。
    -   演算子の最上位レベルの式には、JSONクエリ関数またはJSON値属性関数と、直接列読み取りが混在しています。例: `SELECT JSON_DEPTH(data), name FROM users;` 。
    -   演算子の最上位の式はすべて直接列読み取りであり、出力列の数は入力列の数よりも少なくなります。例: `SELECT name FROM users;` 。
-   `Projection`演算子をプッシュダウンする最終決定は、オプティマイザーによるクエリ コストの総合的な評価によっても決まります。
-   v8.3.0 より前のバージョンから v8.3.0 以降にアップグレードされた TiDB クラスターの場合、この変数のデフォルト値は`OFF`です。

### tidb_opt_range_max_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-opt-range-max-size-span-class-version-mark-new-in-v6-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `67108864` (64 MiB)
-   範囲: `[0, 9223372036854775807]`
-   単位: バイト
-   この変数は、オプティマイザがスキャン範囲を構築する際に使用するメモリの上限を設定するために使用されます。変数値が`0`の場合、スキャン範囲の構築にメモリ制限はありません。正確なスキャン範囲の構築によってメモリ消費量が制限を超える場合、オプティマイザはより緩やかなスキャン範囲（例： `[[NULL,+inf]]` ）を使用します。実行プランで正確なスキャン範囲が使用されない場合は、この変数の値を増やすことで、オプティマイザが正確なスキャン範囲を構築できるようにすることができます。

この変数の使用例は次のとおりです。

<details><summary><code>tidb_opt_range_max_size</code>使用例</summary>

この変数のデフォルト値をビュー。結果から、オプティマイザーがスキャン範囲を構築するために最大64MiBのメモリを使用していることがわかります。

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

64 MiB のメモリ上限では、次の実行プランの結果に示すように、オプティマイザは次の正確なスキャン範囲`[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`構築します。

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

1500 バイトのメモリ制限では、オプティマイザはより緩やかなスキャン範囲`[10,10], [20,20], [30,30]`構築し、正確なスキャン範囲を構築するために必要なメモリ使用量が`tidb_opt_range_max_size`の制限を超えたことを警告を使用してユーザーに通知します。

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

100 バイトのメモリ制限では、オプティマイザは`IndexFullScan`選択し、正確なスキャン範囲を構築するために必要なメモリが`tidb_opt_range_max_size`の制限を超えていることをユーザーに通知する警告を使用します。

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

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1.5`
-   TiKVがディスクから1行のデータを昇順でスキャンするのにかかるコストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_seek_factor {#tidb-opt-seek-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `20`
-   TiDBがTiKVにデータを要求するための初期コストを示します。この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、値を変更することは推奨さ**れません**。

### tidb_opt_skew_distinct_agg <span class="version-mark">v6.2.0 の新機能</span> {#tidb-opt-skew-distinct-agg-span-class-version-mark-new-in-v6-2-0-span}

> **注記：**
>
> この変数を有効にしてクエリ パフォーマンスを最適化することは**、 TiFlashに対してのみ**有効です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、オプティマイザが`DISTINCT`集計関数を2段階の集計関数に書き換えるかどうかを設定します。例えば、 `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b`を`SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`に書き換えます。集計列に深刻な偏りがあり、 `DISTINCT`列に多くの異なる値がある場合、この書き換えによりクエリ実行時のデータ偏りを回避し、クエリパフォーマンスを向上させることができます。

### tidb_opt_three_stage_distinct_agg <span class="version-mark">v6.3.0 の新機能</span> {#tidb-opt-three-stage-distinct-agg-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、MPP モードで`COUNT(DISTINCT)`段階の集約を 3 段階の集約に書き換えるかどうかを指定します。
-   この変数は現在、 1 を`COUNT(DISTINCT)`つだけ含む集計に適用されます。

### tidb_opt_tiflash_concurrency_factor {#tidb-opt-tiflash-concurrency-factor}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `24.0`
-   TiFlash計算の同時実行数を示します。この変数はコストモデル内部で使用されるため、値を変更することは推奨されません。

### tidb_opt_use_invisible_indexes <span class="version-mark">v8.0.0 の新機能</span> {#tidb-opt-use-invisible-indexes-span-class-version-mark-new-in-v8-0-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、現在のセッションにおいて、オプティマイザがクエリの最適化に[目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)選択できるかどうかを制御します。非表示のインデックスはDML文によって維持されますが、クエリオプティマイザでは使用されません。これは、インデックスを永続的に削除する前に二重チェックを行いたい場合などに便利です。この変数を`ON`に設定すると、オプティマイザはセッションにおいてクエリの最適化に非表示のインデックスを選択できます。

### tidb_opt_write_row_id {#tidb-opt-write-row-id}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、 `_tidb_rowid`列目に対して`INSERT` `REPLACE`ステートメントを実行するかどうかを制御するために使用されます。この変数は`UPDATE` TiDBツールを使用してデータをインポートする場合にのみ使用できます。

### tidb_opt_hash_agg_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-hash-agg-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_hash_join_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-hash-join-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_join_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-index-join-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_lookup_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-index-lookup-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_merge_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-index-merge-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_reader_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-index-reader-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_index_scan_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-index-scan-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_limit_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-limit-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_merge_join_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-merge-join-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_sort_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-sort-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_stream_agg_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-stream-agg-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_full_scan_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-table-full-scan-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_range_scan_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-table-range-scan-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_reader_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-table-reader-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_rowid_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-table-rowid-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_table_tiflash_scan_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-table-tiflash-scan-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_opt_topn_cost_factor <span class="version-mark">v8.5.3 の新機能</span> {#tidb-opt-topn-cost-factor-span-class-version-mark-new-in-v8-5-3-span}

> **警告：**
>
> この変数は[コストモデル](/cost-model.md)によって内部的に使用されるため、その値を変更することは推奨さ**れません**。

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: フロート
-   範囲: `[0, 2147483647]`
-   デフォルト値: `1`

### tidb_optimizer_selectivity_level {#tidb-optimizer-selectivity-level}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数は、オプティマイザの推定ロジックの反復回数を制御します。この変数の値を変更すると、オプティマイザの推定ロジックが大きく変化します。現在、有効な値は`0`のみです。他の値に設定することは推奨されません。

### tidb_partition_prune_mode<span class="version-mark">バージョン5.1の新機能</span> {#tidb-partition-prune-mode-span-class-version-mark-new-in-v5-1-span}

> **警告：**
>
> バージョン8.5.0以降、この変数を`static`または`static-only`に設定すると警告が返されます。この変数は将来のリリースで廃止される予定です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `dynamic`
-   `dynamic` `dynamic-only`値`static-only` `static`
-   パーティション化されたテーブルにモード`dynamic`とモード`static`どちらを使用するかを指定します。動的パーティション分割は、テーブルレベルの統計情報、つまりグローバル統計情報が完全に収集された後にのみ有効になることに注意してください。グローバル統計情報の収集が完了する前にプルーニングモード`dynamic`を有効にした場合、TiDBはグローバル統計情報が完全に収集されるまでモード`static`ままになります。グローバル統計情報の詳細については、 [動的プルーニングモードでパーティションテーブルの統計を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。動的プルーニングモードの詳細については、 [パーティションテーブルの動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)参照してください。

### tidb_persist_analyze_options <span class="version-mark">v5.4.0 の新機能</span> {#tidb-persist-analyze-options-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [構成の永続性を分析する](/statistics.md#persist-analyze-configurations)機能を有効にするかどうかを制御します。

### tidb_pessimistic_txn_fair_locking<span class="version-mark">バージョン7.0.0の新機能</span> {#tidb-pessimistic-txn-fair-locking-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   悲観的・トランザクションに拡張悲観的・ロック・ウェイクアップ・モデルを使用するかどうかを決定します。このモデルは、悲観的・ロックのシングルポイント競合シナリオにおいて、悲観的・トランザクションのウェイクアップ順序を厳密に制御し、不要なウェイクアップを回避します。これにより、既存のウェイクアップ・メカニズムのランダム性によってもたらされる不確実性が大幅に軽減されます。ビジネス・シナリオにおいて、シングルポイント・悲観的・ロックの競合が頻繁に発生し（同じデータ行の頻繁な更新など）、ステートメントの再試行が頻繁に発生したり、テール・レイテンシーが長くなったり、場合によっては`pessimistic lock retry limit reached`エラーが発生したりする場合は、この変数を有効にすることで問題を解決できます。
-   この変数は、v7.0.0 より前のバージョンから v7.0.0 以降のバージョンにアップグレードされた TiDB クラスターではデフォルトで無効になっています。

> **注記：**
>
> -   特定のビジネス シナリオによっては、このオプションを有効にすると、ロックの競合が頻繁に発生するトランザクションで、ある程度のスループットの低下 (平均レイテンシーの増加) が発生する可能性があります。
> -   このオプションは、単一のキーをロックする必要があるステートメントにのみ適用されます。複数の行を同時にロックする必要があるステートメントには、このオプションは適用されません。
> -   この機能は、デフォルトでは無効になっている[`tidb_pessimistic_txn_aggressive_locking`](https://docs-archive.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660)変数によって v6.6.0 で導入されました。

### tidb_placement_mode<span class="version-mark">バージョン6.0.0の新機能</span> {#tidb-placement-mode-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `STRICT`
-   可能な`IGNORE` : `STRICT`
-   この変数は、DDL文が[SQLで指定された配置ルール](/placement-rules-in-sql.md)を無視するかどうかを制御します。変数値が`IGNORE`の場合、すべての配置ルールオプションは無視されます。
-   これは、論理ダンプ/リストアツールで、無効な配置ルールが割り当てられた場合でもテーブルが確実に作成できるようにするために使用することを目的としています。これは、mysqldumpがすべてのダンプファイルの先頭に`SET FOREIGN_KEY_CHECKS=0;`書き込む方法に似ています。

### <code>tidb_plan_cache_invalidation_on_fresh_stats</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-plan-cache-invalidation-on-fresh-stats-code-span-class-version-mark-new-in-v7-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、関連するテーブルの統計が更新されたときにプラン キャッシュを自動的に無効にするかどうかを制御します。
-   この変数を有効にすると、プランキャッシュは統計情報をより有効に活用して実行プランを生成できるようになります。例えば、次のようになります。
    -   統計が利用可能になる前に実行プランが生成された場合、統計が利用可能になるとプラン キャッシュは実行プランを再生成します。
    -   テーブルのデータ分布が変更され、以前は最適だった実行プランが最適ではなくなった場合、プラン キャッシュは統計が再収集された後に実行プランを再生成します。
-   この変数は、v7.1.0 より前のバージョンから v7.1.0 以降にアップグレードされた TiDB クラスターではデフォルトで無効になっています。

### <code>tidb_plan_cache_max_plan_size</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-tidb-plan-cache-max-plan-size-code-span-class-version-mark-new-in-v7-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `2097152` (2 MiB)
-   範囲: `[0, 9223372036854775807]` （バイト単位）。「KiB|MiB|GiB|TiB」単位のメモリ形式もサポートされています。3 `0`無制限を意味します。
-   この変数は、準備済みプランキャッシュまたは未準備プランキャッシュにキャッシュできるプランの最大サイズを制御します。プランのサイズがこの値を超える場合、プランはキャッシュされません。詳細については、 [準備されたプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)と[準備されていないプランキャッシュ](/sql-plan-management.md#usage)参照してください。

### tidb_pprof_sql_cpu<span class="version-mark">バージョン4.0の新機能</span> {#tidb-pprof-sql-cpu-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、パフォーマンスの問題を識別してトラブルシューティングするために、プロファイル出力内の対応する SQL ステートメントをマークするかどうかを制御するために使用されます。

### tidb_prefer_broadcast_join_by_exchange_data_size <span class="version-mark">v7.1.0 の新機能</span> {#tidb-prefer-broadcast-join-by-exchange-data-size-span-class-version-mark-new-in-v7-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `OFF`
-   この変数は、TiDBが[MPPハッシュ結合アルゴリズム](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode)を選択した場合に、ネットワーク転送のオーバーヘッドが最小となるアルゴリズムを使用するかどうかを制御します。この変数が有効になっている場合、TiDBはネットワークで交換されるデータのサイズをそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`を使用して推定し、サイズが小さい方を選択します。
-   この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)有効になりません。

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">v6.1.0 の新機能</span> {#tidb-prepared-plan-cache-memory-guard-ratio-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.1`
-   範囲: `[0, 1]`
-   準備されたプランキャッシュがメモリ保護メカニズムをトリガーするしきい値。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)参照してください。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.memory-guard-ratio` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_prepared_plan_cache_size <span class="version-mark">v6.1.0 の新機能</span> {#tidb-prepared-plan-cache-size-span-class-version-mark-new-in-v6-1-0-span}

> **警告：**
>
> バージョン7.1.0以降、この変数は非推奨となりました。代わりに[`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   セッション中にキャッシュできるプランの最大数。詳細については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md)参照してください。
-   この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.capacity` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。

### tidb_projection_concurrency {#tidb-projection-concurrency}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨です。代わりに[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[-1, 256]`
-   単位: スレッド
-   この変数は、 `Projection`演算子の同時実行性を設定するために使用されます。
-   値が`-1`の場合、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tidb_query_log_max_len {#tidb-query-log-max-len}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4096` (4 KiB)
-   範囲: `[0, 1073741824]`
-   単位: バイト
-   SQL文の出力の最大長。文の出力長が`tidb_query_log_max_len`値より大きい場合、文は切り捨てられて出力されます。
-   この設定は以前は`tidb.toml`オプション ( `log.query-log-max-len` ) としても使用可能でしたが、TiDB v6.1.0 以降ではシステム変数としてのみ使用可能になりました。

### tidb_rc_read_check_ts<span class="version-mark">バージョン6.0.0の新機能</span> {#tidb-rc-read-check-ts-span-class-version-mark-new-in-v6-0-0-span}

> **警告：**
>
> -   この機能は[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。 `tidb_rc_read_check_ts`と`replica-read`同時に有効にしないでください。
> -   クライアントがカーソルを使用する場合、返されたデータの前のバッチがすでにクライアントによって使用されていて、ステートメントが最終的に失敗する可能性があるので、 `tidb_rc_read_check_ts`有効にすることはお勧めしません。
> -   バージョン 7.0.0 以降、この変数は、プリペアドステートメントプロトコルを使用するカーソル フェッチ読み取りモードでは有効ではなくなりました。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数はタイムスタンプの取得を最適化するために使用されます。これは、読み取り/書き込み競合がまれな、読み取りコミット分離レベルのシナリオに適しています。この変数を有効にすると、グローバルタイムスタンプの取得にかかるレイテンシーとコストを回避し、トランザクションレベルの読み取りレイテンシーを最適化できます。
-   読み書き競合が深刻な場合、この機能を有効にするとグローバルタイムスタンプの取得コストとレイテンシーが増加し、パフォーマンスが低下する可能性があります。詳細については[コミット読み取り分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level)参照してください。

### tidb_rc_write_check_ts<span class="version-mark">バージョン6.3.0の新機能</span> {#tidb-rc-write-check-ts-span-class-version-mark-new-in-v6-3-0-span}

> **警告：**
>
> この機能は現在[`replica-read`](#tidb_replica_read-new-in-v40)と互換性がありません。この変数を有効にすると、クライアントから送信されるすべてのリクエストで`replica-read`使用できなくなります。したがって、 `tidb_rc_write_check_ts`と`replica-read`同時に有効にしないでください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数はタイムスタンプの取得を最適化するために使用され、分離レベル`READ-COMMITTED`の悲観的トランザクションにおいてポイント書き込みの競合が少ないシナリオに適しています。この変数を有効にすると、ポイント書き込みステートメントの実行中にグローバルタイムスタンプを取得することによるレイテンシーとオーバーヘッドを回避できます。現在、この変数は`UPDATE`の3種類のポイント書き込みステートメントに適用可能です。ポイント書き込みステートメントとは、主キーまたは一意キーをフィルター条件として使用し、最終実行演算子`DELETE` `SELECT ...... FOR UPDATE` `POINT-GET`含まれる書き込みステートメントを指します。
-   ポイント書き込みの競合が深刻な場合、この変数を有効にすると余分なオーバーヘッドとレイテンシーが増加し、パフォーマンスの低下につながります。詳細については[コミット読み取り分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level)参照してください。

### tidb_read_consistency <span class="version-mark">v5.4.0 の新機能</span> {#tidb-read-consistency-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に適用: はい ( [非トランザクションDMLステートメント](/non-transactional-dml.md)存在する場合、ヒントを使用してこの変数の値を変更しても有効にならない可能性があることに注意してください。)
-   タイプ: 文字列
-   デフォルト値: `strict`
-   この変数は、自動コミット読み取りステートメントの読み取り一貫性を制御するために使用されます。
-   変数値が`weak`に設定されている場合、読み取りステートメントで発生したロックは直接スキップされ、読み取り実行が高速化される可能性があります。これは、弱い一貫性読み取りモードです。ただし、トランザクションセマンティクス（アトミック性など）と分散一貫性（線形化可能性など）は保証されません。
-   自動コミット読み取りが高速に返す必要があり、弱い一貫性の読み取り結果が許容されるユーザー シナリオでは、弱い一貫性の読み取りモードを使用できます。

### tidb_read_staleness <span class="version-mark">v5.4.0 の新機能</span> {#tidb-read-staleness-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-2147483648, 0]`
-   この変数は、TiDBが現在のセッションで読み取ることができる履歴データの時間範囲を設定するために使用されます。値を設定すると、TiDBはこの変数で許可された範囲から可能な限り新しいタイムスタンプを選択し、それ以降のすべての読み取り操作はこのタイムスタンプに対して実行されます。例えば、この変数の値が`-5`に設定されている場合、TiKVに対応する履歴バージョンのデータが存在するという条件で、TiDBは5秒間の範囲で可能な限り新しいタイムスタンプを選択します。

### tidb_record_plan_in_slow_log {#tidb-record-plan-in-slow-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、スロー ログにスロー クエリの実行プランを含めるかどうかを制御するために使用されます。

### tidb_redact_log {#tidb-redact-log}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   `ON` `MARKER`値: `OFF`
-   この変数は、TiDB ログとスロー ログに記録される SQL ステートメント内のユーザー情報を非表示にするかどうかを制御します。
-   デフォルト値は`OFF`です。これは、ユーザー情報は一切処理されないことを意味します。
-   変数を`ON`に設定すると、ユーザー情報は非表示になります。例えば、実行されたSQL文が`INSERT INTO t VALUES (1,2)`の場合、ログには`INSERT INTO t VALUES (?,?)`として記録されます。
-   変数を`MARKER`に設定すると、ユーザー情報は`‹ ›`で囲まれます。例えば、実行されたSQL文が`INSERT INTO t VALUES (1,2)`の場合、ログには`INSERT INTO t VALUES (‹1›,‹2›)`として記録されます。ユーザーデータに`‹`または`›`含まれている場合、 `‹`は`‹‹`に、 `›`は`››`にエスケープされます。マークされたログに基づいて、ログを表示する際にマークされた情報を非感応化するかどうかを決定できます。

### tidb_regard_null_as_point <span class="version-mark">v5.4.0 の新機能</span> {#tidb-regard-null-as-point-span-class-version-mark-new-in-v5-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、オプティマイザがインデックス アクセスのプレフィックス条件として NULL 等価性を含むクエリ条件を使用できるかどうかを制御します。
-   この変数はデフォルトで有効になっています。有効にすると、オプティマイザはアクセスするインデックスデータの量を削減できるため、クエリの実行速度が向上します。例えば、クエリに複数列のインデックス`index(a, b)`が含まれており、クエリ条件に`a<=>null and b=1`含まれている場合、オプティマイザはインデックスアクセスにクエリ条件の`a<=>null`と`b=1`両方を使用できます。この変数が無効になっている場合、 `a<=>null and b=1`はヌル同値条件が含まれているため、オプティマイザはインデックスアクセスに`b=1`使用しません。

### tidb_remove_orderby_in_subquery <span class="version-mark">v6.1.0 の新機能</span> {#tidb-remove-orderby-in-subquery-span-class-version-mark-new-in-v6-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: v7.2.0 より前のバージョンでは、デフォルト値は`OFF`です。v7.2.0 以降では、デフォルト値は`ON`です。
-   サブクエリ内の`ORDER BY`句を削除するかどうかを指定します。
-   ISO/IEC SQL規格では、 `ORDER BY`主にトップレベルクエリの結果をソートするために使用されます。サブクエリの場合、規格では結果を`ORDER BY`でソートする必要はありません。
-   サブクエリの結果をソートするには、通常、ウィンドウ関数を使用するか、外側のクエリで再び`ORDER BY`使用するなど、外側のクエリで処理できます。これにより、最終的な結果セットの順序が保証されます。

### tidb_replica_read <span class="version-mark">v4.0 の新機能</span> {#tidb-replica-read-span-class-version-mark-new-in-v4-0-span}

<CustomContent platform="tidb-cloud" plan="starter,essential">

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は読み取り専用です。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> この変数は[TiDB Cloudプレミアム](https://docs-preview.pingcap.com/tidbcloud/tidb-cloud-intro/#deployment-options)の場合読み取り専用です。

</CustomContent>

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `leader`
-   可能な値: `leader` 、 `follower` 、 `leader-and-follower` 、 `prefer-leader` 、 `closest-replicas` 、 `closest-adaptive` 、 `learner` 。 `learner`はバージョン6.6.0で導入されました。
-   この変数は、TiDBがデータを読み取る場所を制御するために使用されます。v8.5.4以降、この変数は読み取り専用SQL文にのみ適用されます。
-   使用方法と実装の詳細については、 [Follower Read](/follower-read.md)参照してください。

### tidb_restricted_read_only <span class="version-mark">v5.2.0 の新機能</span> {#tidb-restricted-read-only-span-class-version-mark-new-in-v5-2-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_restricted_read_only`と[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)同じように動作します。ほとんどの場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを使用してください。
-   権限`SUPER`または`SYSTEM_VARIABLES_ADMIN`を持つユーザーはこの変数を変更できます。ただし、権限[Security強化モード](#tidb_enable_enhanced_security)が有効になっている場合は、この変数の読み取りまたは変更には追加の権限`RESTRICTED_VARIABLES_ADMIN`が必要です。
-   次の場合には`tidb_restricted_read_only` [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)影響します。
    -   `tidb_restricted_read_only`を`ON`に設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)を`ON`に更新されます。
    -   `tidb_restricted_read_only`を`OFF`に設定すると、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)変更されません。
    -   `tidb_restricted_read_only`が`ON`の場合、 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) `OFF`に設定することはできません。
-   TiDBのDBaaSプロバイダーの場合、TiDBクラスタが別のデータベースのダウンストリームデータベースである場合、TiDBクラスタを読み取り専用にするには、 [Security強化モード](#tidb_enable_enhanced_security)を有効にした`tidb_restricted_read_only`使用する必要があります。これにより、顧客が[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)使用してクラスタを書き込み可能にすることができなくなります。これを実現するには、 [Security強化モード](#tidb_enable_enhanced_security)を有効にし、 `SYSTEM_VARIABLES_ADMIN`と`RESTRICTED_VARIABLES_ADMIN`権限を持つ管理者ユーザーを使用して`tidb_restricted_read_only`制御し、データベースユーザーが`SUPER`権限を持つルートユーザーを使用して[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)のみを制御できるようにする必要があります。
-   この変数は、クラスタ全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスタ全体のすべてのTiDBサーバーは読み取り専用モードになります。この場合、TiDBは`SELECT` 、 `USE` 、 `SHOW`など、データを変更しないステートメントのみを実行します。 `INSERT`や`UPDATE`などの他のステートメントについては、TiDBは読み取り専用モードでの実行を拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスタ全体が最終的に読み取り専用状態になることが保証されます。TiDBクラスタでこの変数の値を変更したが、その変更が他のTiDBサーバーにまだ反映されていない場合、更新されていないTiDBサーバーは読み取り専用モードになり**ません**。
-   TiDBはSQL文を実行する前に読み取り専用フラグをチェックします。v6.2.0以降では、SQL文がコミットされる前にもこのフラグがチェックされます。これにより、サーバーが読み取り専用モードになった後に、長時間実行される[自動コミット](/transaction-overview.md#autocommit)文によってデータが変更される場合を防ぐことができます。
-   この変数を有効にすると、TiDB はコミットされていないトランザクションを次のように処理します。
    -   コミットされていない読み取り専用トランザクションの場合は、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行する SQL ステートメントは拒否されます。
    -   変更されたデータを含むコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードを有効にすると、ユーザーに`RESTRICTED_REPLICA_WRITER_ADMIN`権限が明示的に付与されない限り、すべてのユーザー ( `SUPER`権限を持つユーザーを含む) は、データを書き込む可能性のある SQL ステートメントを実行できなくなります。

### tidb_request_source_type <span class="version-mark">v7.4.0 の新機能</span> {#tidb-request-source-type-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: `""`
-   `"stats"` `"lightning"` `"background"` `"br"` `"ddl"`
-   この変数は、現在のセッションのタスクタイプを明示的に指定するために使用されます。タスクタイプは[リソース管理](/tidb-resource-control-ru-groups.md)によって識別および制御されます。例: `SET @@tidb_request_source_type = "background"` 。

### tidb_resource_control_strict_mode<span class="version-mark">バージョン8.2.0の新機能</span> {#tidb-resource-control-strict-mode-span-class-version-mark-new-in-v8-2-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)番目のステートメントと[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザヒントに権限制御を適用するかどうかを制御します。このシステム変数が`ON`に設定されている場合、現在のセッションまたは現在のステートメントにバインドされているリソースグループをこれらの 2 つの方法で変更するには、 `SUPER` 、 `RESOURCE_GROUP_ADMIN` 、または`RESOURCE_GROUP_USER` `OFF`が必要です。13 に設定されている場合、これらの権限はいずれも必要なく、この変数のない以前の TiDB バージョンと同じ動作になります。
-   TiDB クラスターを以前のバージョンから v8.2.0 以降にアップグレードすると、この変数のデフォルト値は`OFF`に設定され、この機能はデフォルトで無効になります。

### tidb_retry_limit {#tidb-retry-limit}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `10`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、楽観的トランザクションの最大再試行回数を設定するために使用されます。トランザクションで再試行可能なエラー（トランザクションの競合、非常に遅いトランザクションのコミット、テーブルスキーマの変更など）が発生した場合、この変数の値に従ってトランザクションが再実行されます。1～ `0` `tidb_retry_limit`設定すると自動再試行が無効になることに注意してください。この変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。

### tidb_row_format_version {#tidb-row-format-version}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `2`
-   範囲: `[1, 2]`
-   テーブルに新しく保存されるデータのフォーマットバージョンを制御します。TiDB v4.0では、新しいデータの保存にはデフォルトでバージョン[新しいstorage行形式](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2018-07-19-row-format.md)バージョン`2`が使用されます。
-   TiDB バージョン v4.0.0 より前のバージョンから v4.0.0 以降のバージョンにアップグレードする場合、フォーマット バージョンは変更されず、TiDB は引き続きバージョン`1`の古いフォーマットを使用してテーブルにデータを書き込みます。つまり、**新しく作成されたクラスターのみがデフォルトで新しいデータ フォーマットを使用する**ことになります。
-   この変数を変更しても、保存されている古いデータには影響しませんが、対応するバージョン形式は、この変数を変更した後に新しく書き込まれたデータにのみ適用されることに注意してください。

### tidb_runtime_filter_mode <span class="version-mark">v7.2.0 の新機能</span> {#tidb-runtime-filter-mode-span-class-version-mark-new-in-v7-2-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `OFF`
-   可能な`LOCAL` : `OFF`
-   ランタイムフィルタのモード、つまり**フィルタ送信オペレータ**と**フィルタ受信オペレータ**の関係を制御します。モードは`OFF`と`LOCAL` 2つあります。9 `OFF`ランタイムフィルタを無効にすることを意味します。11 `LOCAL`ローカルモードでランタイムフィルタを有効にすることを意味します。詳細については、 [ランタイムフィルターモード](/runtime-filter.md#runtime-filter-mode)参照してください。

### tidb_runtime_filter_type <span class="version-mark">v7.2.0 の新機能</span> {#tidb-runtime-filter-type-span-class-version-mark-new-in-v7-2-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `IN`
-   可能な値: `IN`
-   生成されたフィルター演算子で使用される述語のタイプを制御します。現在サポートされているのは`IN`のみです。詳細については[ランタイムフィルタータイプ](/runtime-filter.md#runtime-filter-type)参照してください。

### tidb_scatter_region {#tidb-scatter-region}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `""`
-   `table` `global`値: `""`
-   テーブル作成時にパラメータ`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`設定されている場合、テーブルが正常に作成された後、システムはテーブルを指定された数の領域に自動的に分割します。この変数は、分割された領域の分散戦略を制御します。TiDB は、選択された分散戦略に基づいて領域を処理します。テーブル作成操作は、分散プロセスの完了を待ってから成功ステータスを返すため、この変数を有効にすると、ステートメント`CREATE TABLE`の実行時間が大幅に長くなる可能性があることに注意してください。この変数が無効な場合と比較して、実行時間は数倍長くなる可能性があります。可能な値の説明は次のとおりです。
    -   `""` : デフォルト値。テーブルの作成後にテーブルの領域が分散されないことを示します。
    -   `table` : テーブル作成時に`PRE_SPLIT_REGIONS`または`SHARD_ROW_ID_BITS`属性を設定すると、複数のリージョンを事前分割するシナリオにおいて、これらのテーブルのリージョンはテーブルの粒度に応じて分散されます。ただし、テーブル作成時に上記の属性を設定しないと、大量のテーブルを急速に作成するシナリオにおいて、これらのテーブルのリージョンが少数の TiKV ノードに集中し、リージョンの分散が不均一になります。
    -   `global` : TiDB は、クラスター全体のデータ分布に応じて、新規作成されたテーブルのリージョンを分散させます。特に多数のテーブルを急速に作成する場合、 `global`オプションを使用すると、リージョンが少数の TiKV ノードに過度に集中するのを防ぎ、クラスター全体にわたってリージョンをよりバランスよく分散させることができます。

### tidb_schema_cache_size <span class="version-mark">v8.0.0 の新機能</span> {#tidb-schema-cache-size-span-class-version-mark-new-in-v8-0-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `536870912` (512 MiB)
-   範囲: `0`または`[67108864, 9223372036854775807]`
-   TiDB v8.4.0 より前では、この変数のデフォルト値は`0`です。
-   TiDB v8.4.0 以降では、デフォルト値は`536870912`です。以前のバージョンから v8.4.0 以降にアップグレードすると、以前のバージョンで設定された古い値が使用されます。
-   この変数は、TiDBのスキーマキャッシュのサイズを制御します。単位はバイトです。この変数を`0`に設定すると、キャッシュ制限機能が無効になります。この機能を有効にするには、 `[67108864, 9223372036854775807]`範囲内の値を設定する必要があります。TiDBはこの値を利用可能な最大メモリ制限として使用し、Least Recently Used (LRU)アルゴリズムを適用して必要なテーブルをキャッシュすることで、スキーマ情報によって使用されるメモリを効果的に削減します。

### tidb_schema_version_cache_limit <span class="version-mark">v7.4.0 の新機能</span> {#tidb-schema-version-cache-limit-span-class-version-mark-new-in-v7-4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `16`
-   範囲: `[2, 255]`
-   この変数は、TiDBインスタンスにキャッシュできる履歴スキーマバージョンの数を制限します。デフォルト値は`16`で、TiDBはデフォルトで16個の履歴スキーマバージョンをキャッシュします。
-   通常、この変数を変更する必要はありません。1 [ステイル読み取り](/stale-read.md)機能を使用し、DDL 操作が頻繁に実行される場合、スキーマバージョンが頻繁に変更されます。その結果、 ステイル読み取りがスナップショットからスキーマ情報を取得しようとすると、スキーマキャッシュミスのために情報の再構築に長い時間がかかる可能性があります。このような場合は、 `tidb_schema_version_cache_limit`の値を大きくして（たとえば`32` ）、スキーマキャッシュミスの問題を回避できます。
-   この変数を変更すると、TiDBのメモリ使用量がわずかに増加します。OOM問題を回避するために、TiDBのメモリ使用量を監視してください。

### tidb_server_memory_limit <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `80%`
-   範囲：
    -   値はパーセンテージ形式で設定できます。これは、メモリ使用量を総メモリの割合で表します。値の範囲は`[1%, 99%]`です。
    -   メモリサイズの値も設定できます。値の範囲は`0` ～ `[536870912, 9223372036854775807]` （バイト単位）です。「KiB|MiB|GiB|TiB」単位のメモリフォーマットがサポートされています。5 `0`メモリ制限なしを意味します。
    -   この変数が 512 MiB 未満かつ`0`以外のメモリサイズに設定されている場合、TiDB は実際のサイズとして 512 MiB を使用します。
-   この変数は、TiDBインスタンスのメモリ制限を指定します。TiDBのメモリ使用量が制限に達すると、TiDBは現在実行中のSQL文のうち、メモリ使用量が最も高いSQL文をキャンセルします。SQL文のキャンセルに成功すると、TiDBはGolang GCを呼び出してメモリを即時に解放し、メモリ負荷を可能な限り軽減しようとします。
-   最初にキャンセルする SQL 文として、メモリ使用量が[`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)制限を超える SQL 文のみが選択されます。
-   現在、TiDB は一度に 1 つの SQL 文のみをキャンセルします。TiDB が SQL 文を完全にキャンセルしてリソースを回復した後でも、メモリ使用量がこの変数で設定された制限を超えている場合、TiDB は次のキャンセル操作を開始します。

### tidb_server_memory_limit_gc_trigger <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-gc-trigger-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `70%`
-   範囲: `[50%, 99%]`
-   TiDBがGCをトリガーしようとするしきい値。TiDBのメモリ使用量が`tidb_server_memory_limit` × `tidb_server_memory_limit_gc_trigger`に達すると、TiDBはGolangのGC操作をアクティブにトリガーします。1分間に1回のみGC操作がトリガーされます。

### tidb_server_memory_limit_sess_min_size <span class="version-mark">v6.4.0 の新機能</span> {#tidb-server-memory-limit-sess-min-size-span-class-version-mark-new-in-v6-4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `134217728` (128 MiB)
-   範囲: `[128, 9223372036854775807]` （バイト単位）。「KiB|MiB|GiB|TiB」単位のメモリ形式もサポートされています。
-   メモリ制限を有効にすると、TiDBは現在のインスタンスで最もメモリ使用量が多いSQL文を終了します。この変数は、終了するSQL文の最小メモリ使用量を指定します。メモリ使用量の少ないセッションが多すぎるためにTiDBインスタンスのメモリ使用量が制限を超えている場合は、この変数の値を適切に下げることで、より多くのセッションをキャンセルできるようになります。

### tidb_service_scope<span class="version-mark">バージョン7.4.0の新機能</span> {#tidb-service-scope-span-class-version-mark-new-in-v7-4-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: &quot;&quot;
-   オプション値：最大64文字の文字列。有効な文字は、数字`0-9` 、文字`a-zA-Z` 、アンダースコア`_` 、ハイフン`-`です。
-   この変数はインスタンスレベルのシステム変数です。これを使用して、 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)配下の各 TiDB ノードのサービススコープを制御できます。DXF は、この変数の値に基づいて、どの TiDB ノードに分散タスクの実行をスケジュールするかを決定します。具体的なルールについては、 [タスクのスケジュール](/tidb-distributed-execution-framework.md#task-scheduling)参照してください。

### tidb_session_alias <span class="version-mark">v7.4.0 の新機能</span> {#tidb-session-alias-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: セッション
-   クラスターに持続: いいえ
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: &quot;&quot;
-   この変数を使用すると、現在のセッションに関連するログの`session_alias`列目の値をカスタマイズできます。この値は、トラブルシューティング時にセッションを識別するのに役立ちます。この設定は、ステートメント実行に関係する複数のノード（TiKVを含む）のログに影響します。この変数の最大長は64文字に制限されており、それを超える文字は自動的に切り捨てられます。値の末尾のスペースも自動的に削除されます。

### tidb_session_plan_cache_size <span class="version-mark">v7.1.0 の新機能</span> {#tidb-session-plan-cache-size-span-class-version-mark-new-in-v7-1-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[1, 100000]`
-   この変数は、キャッシュできるプランの最大数を制御します。1 [準備されたプランキャッシュ](/sql-prepared-plan-cache.md) [準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)同じキャッシュを共有します。
-   以前のバージョンからv7.1.0以降のバージョンにアップグレードすると、この変数は[`tidb_prepared_plan_cache_size`](#tidb_prepared_plan_cache_size-new-in-v610)と同じ値のままになります。

### tidb_shard_allocate_step<span class="version-mark">バージョン5.0の新機能</span> {#tidb-shard-allocate-step-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `9223372036854775807`
-   範囲: `[1, 9223372036854775807]`
-   この変数は、 [`AUTO_RANDOM`](/auto-random.md)または[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)番目の属性に割り当てる連続IDの最大数を制御します。通常、1つのトランザクションでは、 `AUTO_RANDOM` IDまたは`SHARD_ROW_ID_BITS`注釈付き行IDが増分かつ連続して割り当てられます。この変数を使用することで、大規模トランザクションのシナリオにおけるホットスポットの問題を解決できます。

### tidb_shard_row_id_bits <span class="version-mark">v8.4.0 の新機能</span> {#tidb-shard-row-id-bits-span-class-version-mark-new-in-v8-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 15]`
-   この変数は、新規に作成されるテーブルの行IDシャードのデフォルト数を設定するために使用されます。この変数が0以外の値に設定されている場合、TiDBは、 `CREATE TABLE`ステートメントを実行する際に`SHARD_ROW_ID_BITS` IDシャード（例えば`NONCLUSTERED`テーブル）の使用を許可するテーブルにこの属性を自動的に適用します。詳細については、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)参照してください。

### tidb_simplified_metrics {#tidb-simplified-metrics}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数を有効にすると、TiDB は Grafana パネルで使用されないメトリックを収集または記録しません。

### tidb_skip_ascii_check<span class="version-mark">バージョン5.0の新機能</span> {#tidb-skip-ascii-check-span-class-version-mark-new-in-v5-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、ASCII 検証をスキップするかどうかを設定するために使用されます。
-   ASCII文字の検証はパフォーマンスに影響します。入力文字が有効なASCII文字であることが確実な場合は、変数値を`ON`に設定できます。

### tidb_skip_isolation_level_check {#tidb-skip-isolation-level-check}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   このスイッチを有効にすると、TiDBでサポートされていない分離レベルが`tx_isolation`に割り当てられた場合でも、エラーは報告されません。これにより、異なる分離レベルを設定する（ただし、その分離レベルに依存しない）アプリケーションとの互換性が向上します。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_missing_partition_stats <span class="version-mark">v7.3.0 の新機能</span> {#tidb-skip-missing-partition-stats-span-class-version-mark-new-in-v7-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)のパーティションテーブルにアクセスすると、TiDBは各パーティションの統計情報を集約してグローバル統計情報を生成します。この変数は、パーティション統計情報が欠落している場合にグローバル統計情報を生成するかどうかを制御します。

    -   この変数が`ON`場合、TiDB はグローバル統計を生成するときに欠落しているパーティション統計をスキップするため、グローバル統計の生成には影響しません。
    -   この変数が`OFF`場合、TiDB はパーティション統計の欠落を検出するとグローバル統計の生成を停止します。

### tidb_skip_utf8_check {#tidb-skip-utf8-check}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、UTF-8 検証をスキップするかどうかを設定するために使用されます。
-   UTF-8文字の検証はパフォーマンスに影響します。入力文字が有効なUTF-8文字であることが確実な場合は、変数値を`ON`に設定できます。

> **注記：**
>
> 文字チェックを省略すると、TiDBはアプリケーションによって書き込まれた無効なUTF-8文字を検出できず、 `ANALYZE`実行時にデコードエラーが発生し、その他の未知のエンコード問題が発生する可能性があります。アプリケーションが書き込まれた文字列の有効性を保証できない場合は、文字チェックを省略することは推奨されません。

### tidb_slow_log_threshold {#tidb-slow-log-threshold}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに保持されます: いいえ。現在接続している TiDB インスタンスにのみ適用されます。
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[-1, 9223372036854775807]`
-   単位: ミリ秒
-   この変数は、スローログに記録される時間の閾値を出力します。デフォルトでは300ミリ秒に設定されています。クエリの消費時間がこの値を超えると、そのクエリはスロークエリとみなされ、スロークエリログにログが出力されます。なお、出力レベル[`log.level`](https://docs.pingcap.com/tidb/dev/tidb-configuration-file#level)が`"debug"`の場合、この変数の設定に関わらず、すべてのクエリがスロークエリログに記録されます。

### tidb_slow_query_file {#tidb-slow-query-file}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   `INFORMATION_SCHEMA.SLOW_QUERY`クエリすると、設定ファイル内の`slow-query-file`で設定されたスロークエリログ名のみが解析されます。デフォルトのスロークエリログ名は「tidb-slow.log」です。他のログを解析するには、セッション変数`tidb_slow_query_file`に特定のファイルパスを設定し、クエリ`INFORMATION_SCHEMA.SLOW_QUERY`を実行して、設定されたファイルパスに基づいてスロークエリログを解析します。

<CustomContent platform="tidb">

詳細は[遅いクエリを特定する](/identify-slow-queries.md)参照。

</CustomContent>

### tidb_slow_txn_log_threshold<span class="version-mark">バージョン7.0.0の新機能</span> {#tidb-slow-txn-log-threshold-span-class-version-mark-new-in-v7-0-0-span}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   型: 符号なし整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   単位: ミリ秒
-   この変数は、低速トランザクションログのしきい値を設定します。トランザクションの実行時間がこのしきい値を超えると、TiDBはトランザクションに関する詳細情報をログに記録します。値が`0`に設定されている場合、この機能は無効になります。

### tidb_スナップショット {#tidb-snapshot}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   この変数は、セッションでデータを読み取る時点を設定するために使用されます。例えば、変数を「2017-11-11 20:20:20」または「400036290571534337」のようなTSO番号に設定すると、現在のセッションはその時点のデータを読み取ります。

### tidb_source_id <span class="version-mark">v6.5.0 の新機能</span> {#tidb-source-id-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
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

### tidb_stats_cache_mem_quota <span class="version-mark">v6.1.0 の新機能</span> {#tidb-stats-cache-mem-quota-span-class-version-mark-new-in-v6-1-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   単位: バイト
-   デフォルト値： `0` 。これは、TiDB統計キャッシュのメモリクォータがTiDBインスタンスの総メモリの20%であることを意味します。v8.5.1より前では、 `0`メモリクォータがTiDBインスタンスの総メモリの50%であることを意味します。
-   範囲: `[0, 1099511627776]`
-   この変数は、TiDB 統計キャッシュのメモリクォータを設定します。

### tidb_stats_load_pseudo_timeout <span class="version-mark">v5.4.0 の新機能</span> {#tidb-stats-load-pseudo-timeout-span-class-version-mark-new-in-v5-4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、SQL最適化の待機時間がタイムアウトに達した際に、完全な列統計情報を同期的にロードするためのTiDBの動作を制御します。デフォルト値`ON`タイムアウト後にSQL最適化が疑似統計情報を使用する状態に戻ることを意味します。この変数を`OFF`に設定すると、タイムアウト後にSQL実行が失敗します。

### tidb_stats_load_sync_wait <span class="version-mark">v5.4.0 の新機能</span> {#tidb-stats-load-sync-wait-span-class-version-mark-new-in-v5-4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `100`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   この変数は、統計情報の同期ロード機能を有効にするかどうかを制御します。値`0`は機能が無効であることを意味します。この機能を有効にするには、SQL最適化が完全な列統計情報を同期ロードするまでの最大待機時間（ミリ秒単位）をこの変数に設定できます。詳細については、 [負荷統計](/statistics.md#load-statistics)参照してください。

### tidb_stmt_summary_enable_persistent <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-enable-persistent-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントサマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効にするかどうかを制御します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_filename <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-filename-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントサマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 文字列
-   デフォルト値: `"tidb-statements.log"`
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合、永続データが書き込まれるファイルを指定します。

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
> ステートメントサマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合、保存できるデータファイルの最大数を指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_days <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-file-max-days-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントサマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `3`
-   単位: 日
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合、永続データファイルを保持する最大日数を指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_file_max_size <span class="version-mark">v6.6.0 の新機能</span> {#tidb-stmt-summary-file-max-size-span-class-version-mark-new-in-v6-6-0-span}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

</CustomContent>

> **警告：**
>
> ステートメントサマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `64`
-   単位: MiB
-   この変数は読み取り専用です。1 [ステートメントの概要の永続性](/statement-summary-tables.md#persist-statements-summary)有効な場合、永続データファイルの最大サイズを指定します。

<CustomContent platform="tidb">

-   この変数の値は、構成項目[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)の値と同じです。

</CustomContent>

### tidb_stmt_summary_history_size <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-history-size-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `24`
-   範囲: `[0, 255]`
-   この変数は、履歴容量を[明細書要約表](/statement-summary-tables.md)に設定するために使用されます。

### tidb_stmt_summary_internal_query <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-internal-query-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、TiDB の SQL 情報を[明細書要約表](/statement-summary-tables.md)に含めるかどうかを制御するために使用されます。

### tidb_stmt_summary_max_sql_length <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-max-sql-length-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `4096`
-   範囲: `[0, 2147483647]`
-   単位: バイト

<CustomContent platform="tidb">

-   この変数は、 [明細書要約表](/statement-summary-tables.md)および[TiDBダッシュボード](/dashboard/dashboard-intro.md)の SQL 文字列の長さを制御するために使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、 [明細書要約表](/statement-summary-tables.md)の SQL 文字列の長さを制御するために使用されます。

</CustomContent>

### tidb_stmt_summary_max_stmt_count <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-max-stmt-count-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `3000`
-   範囲: `[1, 32767]`
-   この変数は、テーブル[`statements_summary`](/statement-summary-tables.md#statements_summary)と[`statements_summary_history`](/statement-summary-tables.md#statements_summary_history)がメモリ内に合計で保存できる SQL ダイジェストの数を制限するために使用されます。

<CustomContent platform="tidb">

> **注記：**
>
> [`tidb_stmt_summary_enable_persistent`](/statement-summary-tables.md#persist-statements-summary)有効になっている場合、 `tidb_stmt_summary_max_stmt_count` [`statements_summary`](/statement-summary-tables.md#statements_summary)テーブルがメモリに格納できる SQL ダイジェストの数のみを制限します。

</CustomContent>

### tidb_stmt_summary_refresh_interval <span class="version-mark">v4.0 の新機能</span> {#tidb-stmt-summary-refresh-interval-span-class-version-mark-new-in-v4-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1800`
-   範囲: `[1, 2147483647]`
-   単位: 秒
-   この変数は[明細書要約表](/statement-summary-tables.md)の更新時間を設定するために使用されます。

### tidb_store_batch_size {#tidb-store-batch-size}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `4`
-   範囲: `[0, 25000]`
-   この変数は、 `IndexLookUp`オペレータのコプロセッサータスクのバッチサイズを制御するために使用されます。3 `0`バッチを無効にすることを意味します。タスク数が比較的多く、低速なクエリが発生する場合は、この変数の値を大きくすることでクエリを最適化できます。

### tidb_store_limit <span class="version-mark">v3.0.4 および v4.0 の新機能</span> {#tidb-store-limit-span-class-version-mark-new-in-v3-0-4-and-v4-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、TiDB が TiKV に同時に送信できるリクエストの最大数を制限するために使用されます。0 は制限がないことを意味します。

### tidb_streamagg_concurrency {#tidb-streamagg-concurrency}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   この変数は、クエリが実行される際の`StreamAgg`演算子の同時実行性を設定します。
-   この変数を設定することは**推奨されません**。変数値を変更すると、データの正確性に問題が生じる可能性があります。

### tidb_super_read_only <span class="version-mark">v5.3.1 の新機能</span> {#tidb-super-read-only-span-class-version-mark-new-in-v5-3-1-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   `tidb_super_read_only` MySQL 変数`super_read_only`の置き換えとして実装することを目的としています。ただし、TiDB は分散データベースであるため、 `tidb_super_read_only`実行直後にデータベースを読み取り専用にするのではなく、最終的には読み取り専用にします。
-   権限`SUPER`または`SYSTEM_VARIABLES_ADMIN`を持つユーザーはこの変数を変更できます。
-   この変数は、クラスタ全体の読み取り専用ステータスを制御します。変数が`ON`の場合、クラスタ全体のすべてのTiDBサーバーは読み取り専用モードになります。この場合、TiDBは`SELECT` 、 `USE` 、 `SHOW`など、データを変更しないステートメントのみを実行します。 `INSERT`や`UPDATE`などの他のステートメントについては、TiDBは読み取り専用モードでの実行を拒否します。
-   この変数を使用して読み取り専用モードを有効にすると、クラスタ全体が最終的に読み取り専用状態になることが保証されます。TiDBクラスタでこの変数の値を変更したが、その変更が他のTiDBサーバーにまだ反映されていない場合、更新されていないTiDBサーバーは読み取り専用モードになり**ません**。
-   TiDBはSQL文を実行する前に読み取り専用フラグをチェックします。v6.2.0以降では、SQL文がコミットされる前にもこのフラグがチェックされます。これにより、サーバーが読み取り専用モードになった後に、長時間実行される[自動コミット](/transaction-overview.md#autocommit)文によってデータが変更される場合を防ぐことができます。
-   この変数を有効にすると、TiDB はコミットされていないトランザクションを次のように処理します。
    -   コミットされていない読み取り専用トランザクションの場合は、通常どおりトランザクションをコミットできます。
    -   読み取り専用ではないコミットされていないトランザクションの場合、これらのトランザクションで書き込み操作を実行する SQL ステートメントは拒否されます。
    -   変更されたデータを含むコミットされていない読み取り専用トランザクションの場合、これらのトランザクションのコミットは拒否されます。
-   読み取り専用モードを有効にすると、ユーザーに`RESTRICTED_REPLICA_WRITER_ADMIN`権限が明示的に付与されない限り、すべてのユーザー ( `SUPER`権限を持つユーザーを含む) は、データを書き込む可能性のある SQL ステートメントを実行できなくなります。
-   システム変数[`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520) `ON`に設定されている場合、 `tidb_super_read_only` [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の影響を受ける場合があります。詳細な影響については、 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520)の説明を参照してください。

### tidb_sysdate_is_now <span class="version-mark">v6.0.0 の新機能</span> {#tidb-sysdate-is-now-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `OFF`
-   この変数は、関数`SYSDATE`を関数`NOW`に置き換えるかどうかを制御するために使用します。この設定項目は、MySQL オプション[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。

### tidb_sysproc_scan_concurrency <span class="version-mark">v6.5.0 の新機能</span> {#tidb-sysproc-scan-concurrency-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: `[0, 4294967295]` 。v7.5.0以前のバージョンでは最大値は`256` 。v8.2.0より前のバージョンでは、最小値は`1` `0`に設定すると、クラスターのサイズに基づいて同時実行性が適応的に調整されます。
-   この変数は、TiDB が内部 SQL ステートメント (統計の自動更新など) を実行するときに実行されるスキャン操作の同時実行性を設定するために使用されます。

### tidb_table_cache_lease <span class="version-mark">v6.0.0 の新機能</span> {#tidb-table-cache-lease-span-class-version-mark-new-in-v6-0-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `3`
-   範囲: `[1, 10]`
-   単位: 秒
-   この変数は、リース期間（ [キャッシュされたテーブル](/cached-tables.md) 、デフォルト値は`3`を制御するために使用されます。この変数の値は、キャッシュされたテーブルの変更に影響します。キャッシュされたテーブルに変更を加えた後、最長の待機時間は`tidb_table_cache_lease`秒になる可能性があります。テーブルが読み取り専用の場合、または書き込みレイテンシーが長い場合は、この変数の値を増やすことで、キャッシュテーブルの有効期間を延長し、リース更新の頻度を減らすことができます。

### tidb_tmp_table_max_size <span class="version-mark">v5.3.0 の新機能</span> {#tidb-tmp-table-max-size-span-class-version-mark-new-in-v5-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `67108864`
-   範囲: `[1048576, 137438953472]`
-   単位: バイト
-   この変数は、単一の[一時テーブル](/temporary-tables.md)の最大サイズを設定するために使用されます。この変数値よりも大きいサイズの一時テーブルはエラーを引き起こします。

### tidb_top_sql_max_meta_count <span class="version-mark">v6.0.0 の新機能</span> {#tidb-top-sql-max-meta-count-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   範囲: グローバル
-   クラスターに持続: はい
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

### tidb_top_sql_max_time_series_count<span class="version-mark">バージョン6.0.0の新機能</span> {#tidb-top-sql-max-time-series-count-span-class-version-mark-new-in-v6-0-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

> **注記：**
>
> 現在、TiDB ダッシュボードの[Top SQL]ページには、負荷に最も寄与している上位 5 種類の SQL クエリのみが表示されます。これは、 `tidb_top_sql_max_time_series_count`の構成とは無関係です。

-   範囲: グローバル
-   クラスターに持続: はい
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

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、TiDB が集計関数のメモリ使用量を追跡するかどうかを制御します。

> **警告：**
>
> この変数を無効にすると、TiDB はメモリ使用量を正確に追跡できず、対応する SQL ステートメントのメモリ使用量を制御できなくなる可能性があります。

### tidb_tso_client_batch_max_wait_time <span class="version-mark">v5.3.0 の新機能</span> {#tidb-tso-client-batch-max-wait-time-span-class-version-mark-new-in-v5-3-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 10]`
-   単位: ミリ秒
-   この変数は、TiDBがPDにTSOを要求する際のバッチ操作の最大待機時間を設定するために使用されます。デフォルト値は`0`で、追加の待機時間が発生しないことを意味します。
-   TiDBが利用するPDクライアントは、PDからTSOリクエストを毎回取得する際に、同時に受信したTSOリクエストを可能な限り多く収集します。そして、PDクライアントは収集したリクエストを一括して1つのRPCリクエストにマージし、PDに送信します。これにより、PDの負荷を軽減できます。
-   この変数を`0`より大きい値に設定すると、TiDBは各バッチマージの終了前に、この値の最大時間だけ待機します。これは、より多くのTSOリクエストを収集し、バッチ操作の効果を向上させるためです。
-   この変数の値を増やすシナリオ:
    -   TSO 要求の圧力が高いため、PD リーダーの CPU がボトルネックになり、TSO RPC 要求のレイテンシーが長くなります。
    -   クラスター内の TiDB インスタンスはそれほど多くありませんが、すべての TiDB インスタンスは高い同時実行性を持っています。
-   この変数はできるだけ小さい値に設定することをお勧めします。

> **注記：**
>
> -   PDリーダーのCPU使用率のボトルネック以外の理由（ネットワークの問題など）でTSO RPCのレイテンシーが増加したとします。この場合、値を`tidb_tso_client_batch_max_wait_time`に増やすとTiDBでの実行レイテンシーが増加し、クラスターのQPSパフォーマンスに影響を与える可能性があります。
> -   この機能は[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)と互換性がありません。この変数がゼロ以外の値に設定されている場合、 [`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-new-in-v840)機能しません。

### tidb_tso_client_rpc_mode<span class="version-mark">バージョン8.4.0の新機能</span> {#tidb-tso-client-rpc-mode-span-class-version-mark-new-in-v8-4-0-span}

-   範囲: グローバル

-   クラスターに持続: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ

-   タイプ: 列挙

-   デフォルト値: `DEFAULT`

-   `PARALLEL-FAST` `PARALLEL`オプション: `DEFAULT`

-   この変数は、TiDBがPDにTSO RPCリクエストを送信するモードを切り替えます。このモードは、TSO RPCリクエストを並列処理するかどうかを決定し、各TS取得操作のバッチ待機時間に影響を与えます。これにより、特定のシナリオにおいて、クエリ実行中のTS取得の待機時間を短縮できます。

    -   `DEFAULT` ：TiDBは、特定の期間にわたるTS取得操作を単一のTSO RPCリクエストにまとめ、PDに送信してタイムスタンプを一括取得します。したがって、各TS取得操作の所要時間は、バッチ処理の待機時間とRPC実行時間で構成されます。2 `DEFAULT`では、異なるTSO RPCリクエストがシリアルに処理され、各TS取得操作の平均所要時間は、TSO RPCリクエストの実際の時間コストの約1.5倍になります。
    -   `PARALLEL` : このモードでは、TiDB は各バッチの収集にかかる時間を`DEFAULT`モードの半分に短縮し、2 つの TSO RPC 要求を同時に維持しようとします。これにより、各 TS 取得操作の平均時間は理論上、TSO RPC 時間の約 1.25 倍に短縮されます。これは`DEFAULT`モードの時間コストの約 83% に相当します。ただし、バッチ処理の効果は減少し、TSO RPC 要求の数は`DEFAULT`モードの約 2 倍に増加します。
    -   `PARALLEL-FAST` : `PARALLEL`モードと同様に、このモードでは TiDB は各バッチの収集時間を`DEFAULT`モードの 4 分の 1 に短縮し、同時に 4 つの TSO RPC 要求を維持しようとします。これにより、各 TS 取得操作の平均時間は理論上、TSO RPC 時間の約 1.125 倍に短縮され、これは`DEFAULT`モードの時間コストの約 75% に相当します。ただし、バッチ処理の効果はさらに低下し、TSO RPC 要求の数は`DEFAULT`モードの約 4 倍に増加します。

-   次の条件が満たされる場合は、パフォーマンスの向上を図るためにこの変数を`PARALLEL`または`PARALLEL-FAST`に切り替えることを検討できます。

    -   TSO 待機時間は、SQL クエリの合計実行時間の大部分を占めます。
    -   PD における TSO 割り当てはボトルネックに達していません。
    -   PD ノードと TiDB ノードには十分な CPU リソースがあります。
    -   TiDB と PD 間のネットワークレイテンシーは、PD が TSO を割り当てるのにかかる時間よりも大幅に長くなります (つまり、ネットワークレイテンシーが TSO RPC 期間の大部分を占めます)。
        -   TSO RPC 要求の期間を取得するには、Grafana TiDB ダッシュボードの PD クライアント セクションにある**PD TSO RPC 期間**パネルを確認します。
        -   PD TSO 割り当ての期間を取得するには、Grafana PD ダッシュボードの TiDB セクションにある**PDサーバーTSO ハンドル期間**パネルを確認します。
    -   TiDB と PD 間の TSO RPC 要求の増加 ( `PARALLEL`の場合は 2 回、 `PARALLEL-FAST`の場合は 4 回) によって発生する追加のネットワーク トラフィックは許容されます。

> **注記：**
>
> -   `PARALLEL`および`PARALLEL-FAST`モードは[`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)および[`tidb_enable_tso_follower_proxy`](#tidb_enable_tso_follower_proxy-new-in-v530)と互換性がありません。8 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530)ゼロ以外の値に設定されている場合、または[`tidb_enable_tso_follower_proxy`](#tidb_enable_tso_follower_proxy-new-in-v530)有効になっている場合、 `tidb_tso_client_rpc_mode`設定は有効にならず、TiDB は常に`DEFAULT`モードで動作します。
> -   `PARALLEL`および`PARALLEL-FAST`モードは、TiDB における TS 取得の平均時間を短縮するように設計されています。ロングテールレイテンシーやレイテンシースパイクなど、レイテンシーが大きく変動する状況では、これらの 2 つのモードでは目立ったパフォーマンス向上が得られない可能性があります。

### tidb_cb_pd_metadata_error_rate_threshold_ratio <span class="version-mark">v8.5.5 の新機能</span> {#tidb-cb-pd-metadata-error-rate-threshold-ratio-span-class-version-mark-new-in-v8-5-5-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `0`
-   範囲: `[0, 1]`
-   この変数は、TiDBがサーキットブレーカーをトリガーするタイミングを制御します。値を`0` （デフォルト）に設定すると、サーキットブレーカーは無効になります。3から`0.01` `1`値に設定すると有効になり、PDに送信された特定のリクエストのエラー率がしきい値に達するか超過すると、サーキットブレーカーがトリガーされます。

### tidb_ttl_delete_rate_limit <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-rate-limit-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `0`
-   範囲: `[0, 9223372036854775807]`
-   この変数は、各TiDBノードのTTLジョブにおける`DELETE`文のレートを制限するために使用されます。この値は、TTLジョブにおいて単一ノードで1秒あたりに許可される`DELETE`文の最大数を表します。この変数を`0`に設定すると、制限は適用されません。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_ttl_delete_batch_size <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `100`
-   範囲: `[1, 10240]`
-   この変数は、TTLジョブの`DELETE`トランザクションで削除できる行の最大数を設定するために使用されます。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_ttl_delete_worker_count <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-delete-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各TiDBノードにおけるTTLジョブの最大同時実行数を設定するために使用されます。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_ttl_job_enable <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-enable-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数は、TTLジョブの有効化を制御するために使用されます。1 `OFF`設定すると、TTL属性を持つすべてのテーブルで期限切れデータのクリーンアップが自動的に停止されます。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_ttl_scan_batch_size <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-scan-batch-size-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `500`
-   範囲: `[1, 10240]`
-   この変数は、TTLジョブで期限切れデータをスキャンするために使用される各`SELECT`のステートメントの`LIMIT`の値を設定するために使用されます。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_ttl_scan_worker_count <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-scan-worker-count-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `4`
-   範囲: `[1, 256]`
-   この変数は、各TiDBノードにおけるTTLスキャンジョブの最大同時実行数を設定するために使用されます。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_ttl_job_schedule_window_start_time <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-schedule-window-start-time-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   クラスターに持続: はい
-   デフォルト値: `00:00 +0000`
-   この変数は、バックグラウンドで実行されるTTLジョブのスケジュールウィンドウの開始時刻を制御するために使用されます。この変数の値を変更する際は、ウィンドウが小さいと期限切れデータのクリーンアップに失敗する可能性があるので注意してください。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_ttl_job_schedule_window_end_time <span class="version-mark">v6.5.0 の新機能</span> {#tidb-ttl-job-schedule-window-end-time-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 時間
-   クラスターに持続: はい
-   デフォルト値: `23:59 +0000`
-   この変数は、バックグラウンドで実行されるTTLジョブのスケジュールウィンドウの終了時刻を制御するために使用されます。この変数の値を変更する際は、ウィンドウが小さいと期限切れデータのクリーンアップに失敗する可能性があるので注意してください。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_ttl_running_tasks<span class="version-mark">バージョン7.0.0の新機能</span> {#tidb-ttl-running-tasks-span-class-version-mark-new-in-v7-0-0-span}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `-1` ～ `[1, 256]`
-   クラスタ全体で実行中のTTLタスクの最大数を指定します。1 `-1` 、TTLタスクの数がTiKVノードの数と等しいことを意味します。詳細については、 [生きる時間](/time-to-live.md)を参照してください。

### tidb_txn_assertion_level<span class="version-mark">バージョン6.0.0の新機能</span> {#tidb-txn-assertion-level-span-class-version-mark-new-in-v6-0-0-span}

-   スコープ: セッション | グローバル

-   クラスターに持続: はい

-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ

-   タイプ: 列挙

-   デフォルト値: `FAST`

-   `FAST` `STRICT`値: `OFF`

-   この変数はアサーションレベルを制御するために使用されます。アサーションとは、データとインデックス間の整合性チェックであり、トランザクションのコミットプロセスにおいて、書き込まれるキーが存在するかどうかを確認します。詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。

    -   `OFF` : このチェックを無効にします。
    -   `FAST` : ほとんどのチェック項目を有効にしますが、パフォーマンスにはほとんど影響しません。
    -   `STRICT` : すべてのチェック項目を有効にします。システムのワークロードが高い場合、悲観的トランザクションのパフォーマンスにわずかな影響があります。

-   バージョン6.0.0以降の新しいクラスターの場合、デフォルト値は`FAST`です。バージョン6.0.0より前のバージョンからアップグレードした既存のクラスターの場合、デフォルト値は`OFF`です。

### tidb_txn_commit_batch_size <span class="version-mark">v6.2.0 の新機能</span> {#tidb-txn-commit-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `16384`
-   範囲: `[1, 1073741824]`
-   単位: バイト

<CustomContent platform="tidb">

-   この変数は、TiDBがTiKVに送信するトランザクションコミット要求のバッチサイズを制御するために使用されます。アプリケーションワークロード内のトランザクションの大部分に大量の書き込み操作が含まれる場合、この変数の値を大きくすることでバッチ処理のパフォーマンスを向上させることができます。ただし、この変数の値が大きすぎてTiKVの制限値[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)を超えると、コミットが失敗する可能性があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDBがTiKVに送信するトランザクションコミット要求のバッチサイズを制御するために使用されます。アプリケーションワークロード内のトランザクションの大部分に大量の書き込み操作が含まれる場合、この変数の値を大きくすることでバッチ処理のパフォーマンスを向上させることができます。ただし、この変数の値が大きすぎて、TiKVの単一ログの最大サイズ（デフォルトでは8MiB）を超えると、コミットが失敗する可能性があります。

</CustomContent>

### tidb_txn_entry_size_limit <span class="version-mark">v7.6.0 の新機能</span> {#tidb-txn-entry-size-limit-span-class-version-mark-new-in-v7-6-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 125829120]`
-   単位: バイト

<CustomContent platform="tidb">

-   この変数は、TiDB設定項目[`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)を動的に変更するために使用されます。この変数は、TiDB内の1行のデータサイズ（設定項目 1 に相当）を制限します。この変数のデフォルト値は`0`で、TiDBはデフォルトで設定項目`txn-entry-size-limit`の値を使用します。この変数が0以外の値に設定された場合、 `txn-entry-size-limit`も同じ値に設定されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   この変数は、TiDB設定項目[`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)を動的に変更するために使用されます。この変数は、TiDB内の1行のデータサイズ（設定項目 1 に相当）を制限します。この変数のデフォルト値は`0`で、TiDBはデフォルトで設定項目`txn-entry-size-limit`の値を使用します。この変数が0以外の値に設定された場合、 `txn-entry-size-limit`も同じ値に設定されます。

</CustomContent>

> **注記：**
>
> この変数をSESSIONスコープで変更すると、現在のユーザーセッションにのみ影響し、内部TiDBセッションには影響しません。内部TiDBトランザクションのエントリサイズが設定項目の制限を超えた場合、トランザクションが失敗する可能性があります。したがって、制限を動的に増やすには、GLOBALスコープで変数を変更することをお勧めします。

### tidb_txn_mode {#tidb-txn-mode}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `pessimistic`
-   可能な`optimistic` : `pessimistic`
-   この変数はトランザクションモードを設定するために使用されます。TiDB 3.0は悲観的トランザクションをサポートしています。TiDB 3.0.8以降では、 [悲観的トランザクションモード](/pessimistic-transaction.md)がデフォルトで有効になっています。
-   TiDBをv3.0.7以前のバージョンからv3.0.8以降のバージョンにアップグレードした場合、デフォルトのトランザクションモードは変更されません。**新しく作成されたクラスターのみが、デフォルトで悲観的トランザクションモードを使用します**。
-   この変数が「楽観的」または「」に設定されている場合、 TiDB は[楽観的トランザクションモード](/optimistic-transaction.md)を使用します。

### tidb_use_plan_baselines <span class="version-mark">v4.0 の新機能</span> {#tidb-use-plan-baselines-span-class-version-mark-new-in-v4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、実行プランバインディング機能を有効にするかどうかを制御するために使用されます。デフォルトでは有効になっていますが、値`OFF`を割り当てることで無効にすることができます。実行プランバインディングの使用方法については、 [実行プランのバインディング](/sql-plan-management.md#create-a-binding)参照してください。

### tidb_wait_split_region_finish {#tidb-wait-split-region-finish}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   リージョンの分散には通常長い時間がかかります。これはPDスケジューリングとTiKVロードによって決まります。この変数は、 `SPLIT REGION`ステートメントの実行時に、すべてのリージョンが完全に分散された後に結果をクライアントに返すかどうかを設定するために使用されます。
    -   `ON`では、すべての領域が分散されるまで`SPLIT REGIONS`ステートメントが待機する必要があります。
    -   `OFF`すべての領域の分散が完了する前に`SPLIT REGIONS`ステートメントが戻ることを許可します。
-   リージョンを分散させると、分散対象のリージョンの書き込みおよび読み取りパフォーマンスに影響が出る可能性があることに注意してください。バッチ書き込みやデータのインポートを行う場合は、リージョンの分散が完了した後にデータをインポートすることをお勧めします。

### tidb_wait_split_region_timeout {#tidb-wait-split-region-timeout}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `300`
-   範囲: `[1, 2147483647]`
-   単位: 秒
-   この変数は、 `SPLIT REGION`ステートメントの実行に対するタイムアウトを設定するために使用されます。指定された時間内にステートメントが完全に実行されない場合は、タイムアウトエラーが返されます。

### tidb_window_concurrency <span class="version-mark">v4.0 の新機能</span> {#tidb-window-concurrency-span-class-version-mark-new-in-v4-0-span}

> **警告：**
>
> バージョン5.0以降、この変数は非推奨です。代わりに[`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50)設定してください。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `-1`
-   範囲: `[1, 256]`
-   単位: スレッド
-   この変数は、ウィンドウ オペレータの同時実行度を設定するために使用されます。
-   値が`-1`の場合、代わりに値`tidb_executor_concurrency`が使用されることを意味します。

### tiflash_fastscan <span class="version-mark">v6.3.0 の新機能</span> {#tiflash-fastscan-span-class-version-mark-new-in-v6-3-0-span}

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   [ファストスキャン](/tiflash/use-fastscan.md)が有効（ `ON`に設定）の場合、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の正確性やデータの一貫性は保証されません。

### tiflash_fine_grained_shuffle_batch_size <span class="version-mark">v6.2.0 の新機能</span> {#tiflash-fine-grained-shuffle-batch-size-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション | グローバル
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   デフォルト値: `8192`
-   範囲: `[1, 18446744073709551615]`
-   Fine Grained Shuffle を有効にすると、 TiFlashにプッシュダウンされたウィンドウ関数を並列実行できます。この変数は、送信側が送信するデータのバッチサイズを制御します。
-   パフォーマンスへの影響：ビジネス要件に応じて適切なサイズを設定してください。不適切な設定はパフォーマンスに影響します。値が小さすぎる場合（例えば`1` 、ブロックごとに1回のネットワーク転送が発生します。値が大きすぎる場合（例えばテーブルの行数の合計）、受信側はデータの待機にほとんどの時間を費やし、パイプライン計算が機能しなくなります。適切な値を設定するには、 TiFlashレシーバーが受信する行数の分布を観察することができます。ほとんどのスレッドが数行（例えば数百行）しか受信しない場合は、この値を増やすことでネットワークオーバーヘッドを削減できます。

### tiflash_fine_grained_shuffle_stream_count <span class="version-mark">v6.2.0 の新機能</span> {#tiflash-fine-grained-shuffle-stream-count-span-class-version-mark-new-in-v6-2-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-1, 1024]`
-   ウィンドウ関数がTiFlashにプッシュダウンされて実行される際、この変数を使用してウィンドウ関数実行の同時実行レベルを制御できます。指定可能な値は次のとおりです。

    -   -1: Fine Grained Shuffle機能は無効です。TiFlashにプッシュダウンされたウィンドウ関数は単一スレッドで実行されます。
    -   0: 細粒度シャッフル機能が有効です。1 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)有効な値（0より大きい値）に設定されている場合、 `tiflash_fine_grained_shuffle_stream_count` [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)に設定されます。それ以外の場合は、 TiFlashコンピューティングノードの CPU リソースに基づいて自動的に推定されます。TiFlash におけるウィンドウ関数の実際の同時実行レベルは、min( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashTiFlash上の物理スレッド数) です。
    -   0より大きい整数：Fine Grained Shuffle機能が有効です。TiFlashにプッシュダウンされたウィンドウ関数は複数のスレッドで実行されます。同時実行レベルはmin( `tiflash_fine_grained_shuffle_stream_count` 、 TiFlashノード上の物理スレッド数)です。
-   理論上、ウィンドウ関数のパフォーマンスはこの値に比例して向上します。ただし、この値が実際の物理スレッド数を超えると、パフォーマンスの低下につながります。

### tiflash_mem_quota_query_per_node <span class="version-mark">v7.4.0 の新機能</span> {#tiflash-mem-quota-query-per-node-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[-1, 9223372036854775807]`
-   この変数は、 TiFlashノードにおけるクエリの最大メモリ使用量を制限します。クエリのメモリ使用量がこの制限を超えると、 TiFlashはエラーを返し、クエリを終了します。この変数を`-1`または`0`に設定すると、制限なしとなります。この変数を`0`より大きい値に設定し、 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)有効な値に設定すると、 TiFlashは[クエリレベルのスピル](/tiflash/tiflash-spill-disk.md#query-level-spilling)有効にします。

### tiflash_query_spill_ratio <span class="version-mark">v7.4.0 の新機能</span> {#tiflash-query-spill-ratio-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0.7`
-   範囲: `[0, 0.85]`
-   この変数はTiFlash [クエリレベルのスピル](/tiflash/tiflash-spill-disk.md#query-level-spilling)のしきい値を制御します。3 `0` 、クエリレベルの自動スピルを無効にすることを意味します。この変数が`0`より大きく、クエリのメモリ使用量が[`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) * `tiflash_query_spill_ratio`を超えると、 TiFlash はクエリレベルのスピルをトリガーし、必要に応じてクエリ内のサポートされている演算子のデータをスピルします。

> **注記：**
>
> -   この変数は、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) `0`より大きい場合にのみ有効になります。つまり、 [tiflash_mem_quota_query_per_node](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)が`0`または`-1`場合、 `tiflash_query_spill_ratio`が`0`より大きい場合でも、クエリレベルのスピルは有効になりません。
> -   TiFlashクエリレベルのスピルが有効化されると、個々のTiFlash演算子のスピルしきい値は自動的に無効化されます。つまり、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)と`tiflash_query_spill_ratio`両方が 0 より大きい場合、3つの変数[tidb_max_bytes_before_tiflash_external_sort](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700) 、 [tidb_max_bytes_before_tiflash_external_group_by](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) 、 [tidb_max_bytes_before_tiflash_external_join](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)は自動的に無効化され、これは`0`に設定されたのと同じになります。

### tiflash_replica_read <span class="version-mark">v7.3.0 の新機能</span> {#tiflash-replica-read-span-class-version-mark-new-in-v7-3-0-span}

> **注記：**
>
> この TiDB 変数はTiDB Cloudには適用されません。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `all_replicas`
-   値のオプション: `all_replicas` `closest_adaptive`または`closest_replicas`
-   この変数は、クエリにTiFlashエンジンが必要な場合にTiFlashレプリカを選択するための戦略を設定するために使用されます。
    -   `all_replicas` 、分析コンピューティングに利用可能なすべてのTiFlashレプリカを使用することを意味します。
    -   `closest_adaptive` 、クエリを開始する TiDB ノードと同じゾーンにあるTiFlashレプリカを優先的に使用することを意味します。このゾーンのレプリカに必要なデータがすべて含まれていない場合、クエリには他のゾーンのTiFlashレプリカと、それに対応するTiFlashノードが利用されます。
    -   `closest_replicas` 、クエリを開始する TiDB ノードと同じゾーン内のTiFlashレプリカのみを使用することを意味します。このゾーン内のレプリカに必要なデータがすべて含まれていない場合、クエリはエラーを返します。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDBノードに[ゾーン属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)設定されておらず、 `tiflash_replica_read` `all_replicas`に設定されていない場合、 TiFlashはレプリカ選択戦略を無視します。代わりに、クエリにはすべてのTiFlashレプリカを使用し、 `The variable tiflash_replica_read is ignored.`警告を返します。
> -   TiFlashノードに[ゾーン属性](/schedule-replicas-by-topology-labels.md#configure-labels-for-tikv-and-tiflash)設定されていない場合、そのノードはどのゾーンにも属さないノードとして扱われます。

</CustomContent>

### tiflash_hashagg_preaggregation_mode <span class="version-mark">v8.3.0 の新機能</span> {#tiflash-hashagg-preaggregation-mode-span-class-version-mark-new-in-v8-3-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: はい
-   タイプ: 列挙
-   デフォルト値: `force_preagg`
-   `auto` `force_streaming`オプション: `force_preagg`
-   この変数は、 TiFlashにプッシュダウンされる 2 段階または 3 段階の HashAgg 操作の最初の段階で使用される事前集計戦略を制御します。
    -   `force_preagg` : TiFlashはHashAggの最初の段階で事前集計を強制します。この動作はv8.3.0より前の動作と一致しています。
    -   `force_streaming` : TiFlash は事前集計なしでデータを HashAgg の次のステージに直接送信します。
    -   `auto` : TiFlash は、現在のワークロードの集約度に基づいて、事前集約を実行するかどうかを自動的に選択します。

### tikv_client_read_timeout <span class="version-mark">v7.4.0 の新機能</span> {#tikv-client-read-timeout-span-class-version-mark-new-in-v7-4-0-span}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   単位: ミリ秒
-   `tikv_client_read_timeout`指定すると、TiDB がクエリ内で TiKV RPC 読み取り要求を送信する際のタイムアウトを設定できます。TiDB クラスターが不安定なネットワーク環境や TiKV I/Oレイテンシーのジッタが深刻な環境にあり、アプリケーションが SQL クエリのレイテンシーに敏感な場合は、 `tikv_client_read_timeout`設定することで TiKV RPC 読み取り要求のタイムアウトを短縮できます。この場合、TiKV ノードに I/Oレイテンシーのジッタが発生しても、TiDB はすぐにタイムアウトし、次の TiKVリージョンピアが配置されている TiKV ノードに RPC 要求を再送信できます。すべての TiKVリージョンピアの要求がタイムアウトした場合、TiDB はデフォルトのタイムアウト（通常 40 秒）で再試行します。
-   クエリでオプティマイザヒント`/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */`使用して、TiDBがTiKV RPC読み取りリクエストを送信する際のタイムアウトを設定することもできます。オプティマイザヒントとこのシステム変数の両方が設定されている場合、オプティマイザヒントが優先されます。
-   デフォルト値`0`は、デフォルトのタイムアウト (通常は 40 秒) が使用されることを示します。

> **注記：**
>
> -   通常、通常のクエリは数ミリ秒かかりますが、TiKVノードが不安定なネットワークにある場合やI/Oジッターが発生する場合、クエリに1秒以上、場合によっては10秒以上かかることがあります。このような場合、オプティマイザヒント`/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=100) */`を使用して、特定のクエリのTiKV RPC読み取り要求タイムアウトを100ミリ秒に設定できます。このようにして、TiKVノードの応答が遅い場合でも、TiDBはすぐにタイムアウトし、次のTiKVリージョンピアが配置されているTiKVノードにRPC要求を再送信できます。2つのTiKVノードが同時にI/Oジッターが発生する確率は低いため、クエリは通常、数ミリ秒から110ミリ秒以内に完了します。
> -   `tikv_client_read_timeout`にあまり小さい値（例えば1ミリ秒）を設定しないでください。小さすぎると、TiDBクラスタのワークロードが高いときにリクエストが簡単にタイムアウトし、その後の再試行によってTiDBクラスタの負荷がさらに増加する可能性があります。
> -   異なるタイプのクエリに異なるタイムアウト値を設定する必要がある場合は、オプティマイザーヒントを使用することをお勧めします。

### タイムゾーン {#time-zone}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `SYSTEM`
-   この変数は現在のタイムゾーンを返します。値は「-8:00」のようなオフセット、または「America/Los_Angeles」のような名前付きゾーンで指定できます。
-   値`SYSTEM`は、タイム ゾーンがシステム ホストと同じである必要があることを意味します。これは、変数[`system_time_zone`](#system_time_zone)を介して利用できます。

### タイムスタンプ {#timestamp}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: フロート
-   デフォルト値: `0`
-   範囲: `[0, 2147483647]`
-   この変数の値が空でない場合、 `CURRENT_TIMESTAMP()` `NOW()`およびその他の関数のタイムスタンプとして使用されるUNIXエポックを示します。この変数は、データの復元やレプリケーションに使用される可能性があります。

### トランザクション分離 {#transaction-isolation}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `REPEATABLE-READ`
-   `READ-COMMITTED` `SERIALIZABLE`値`REPEATABLE-READ` `READ-UNCOMMITTED`
-   この変数はトランザクション分離レベルを設定します。TiDBはMySQLとの互換性のために`REPEATABLE-READ`宣言していますが、実際の分離レベルはスナップショット分離レベルです。詳細は[トランザクション分離レベル](/transaction-isolation-levels.md)参照してください。

### トランザクション分離 {#tx-isolation}

この変数は`transaction_isolation`の別名です。

### tx_isolation_one_shot {#tx-isolation-one-shot}

> **注記：**
>
> この変数はTiDB内部で使用されます。ユーザーが使用することは想定されていません。

内部的には、TiDB パーサーは`SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]`ステートメントを`SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`に変換します。

### tx_read_ts {#tx-read-ts}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: &quot;&quot;
-   ステイル読み取りシナリオでは、このセッション変数は安定した読み取りタイムスタンプ値を記録するために使用されます。
-   この変数はTiDBの内部処理に使用されます。この変数を設定することは**推奨されません**。

### トランザクションスコープ {#txn-scope}

> **注記：**
>
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `global`
-   値のオプション: `global`と`local`
-   この変数は、現在のセッション トランザクションがグローバル トランザクションであるかローカル トランザクションであるかを設定するために使用されます。
-   この変数はTiDBの内部処理に使用されます。この変数を設定することは**推奨されません**。

### validate_password.check_user_name <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-check-user-name-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `ON`
-   タイプ: ブール値
-   この変数はパスワード複雑度チェックにおけるチェック項目です。パスワードがユーザー名と一致するかどうかをチェックします。この変数は[`validate_password.enable`](#validate_passwordenable-new-in-v650)有効な場合にのみ有効になります。
-   この変数が有効で`ON`に設定されている場合、パスワードを設定すると、TiDB はパスワードとユーザー名（ホスト名を除く）を比較します。パスワードがユーザー名と一致する場合、そのパスワードは拒否されます。
-   この変数は[`validate_password.policy`](#validate_passwordpolicy-new-in-v650)とは独立しており、パスワードの複雑さのチェック レベルの影響を受けません。

### validate_password.dictionary <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-dictionary-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `""`
-   タイプ: 文字列
-   この変数は、パスワードの複雑性チェックにおけるチェック項目です。パスワードが辞書と一致するかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) `2` （STRONG）に設定されている場合にのみ有効になります。
-   この変数は1024文字以下の文字列です。パスワードに使用できない単語のリストが含まれます。各単語はセミコロン（ `;` ）で区切られます。
-   この変数はデフォルトで空の文字列に設定されており、辞書チェックは実行されません。辞書チェックを実行するには、照合する単語を文字列に含める必要があります。この変数が設定されている場合、パスワードを設定すると、TiDBはパスワードの各部分文字列（4～100文字）を辞書内の単語と比較します。パスワードのいずれかの部分文字列が辞書内の単語と一致する場合、そのパスワードは拒否されます。比較は大文字と小文字を区別しません。

### validate_password.enable <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-enable-span-class-version-mark-new-in-v6-5-0-span}

> **注記：**
>
> この変数は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)と[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では常に有効になります。

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `OFF`
-   タイプ: ブール値
-   この変数は、パスワードの複雑さのチェックを実行するかどうかを制御します。この変数を`ON`に設定すると、TiDBはパスワード設定時にパスワードの複雑さのチェックを実行します。

### validate_password.length <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-length-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `8`
-   範囲: TiDBセルフマネージドの場合は`[0, 2147483647]`と[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) `[8, 2147483647]`場合[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   この変数は、パスワードの複雑さチェックにおけるチェック項目です。パスワードの長さが十分かどうかをチェックします。デフォルトでは、パスワードの最小長は`8`です。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)有効になっている場合にのみ有効になります。
-   この変数の値は、式`validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`より小さくてはなりません。
-   式の値が`validate_password.length`より大きくなるように`validate_password.number_count` 、 `validate_password.special_char_count` 、または`validate_password.mixed_case_count`の値を変更すると、式の値に合わせて`validate_password.length`の値が自動的に変更されます。

### validate_password.mixed_case_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-mixed-case-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: TiDBセルフマネージドの場合は`[0, 2147483647]`と[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) `[1, 2147483647]`場合[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   この変数は、パスワードの複雑さチェックにおけるチェック項目です。パスワードに十分な大文字と小文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#validate_passwordenable-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) `1` （中）以上に設定されている場合にのみ有効になります。
-   パスワード内の大文字と小文字の数は、どちらも`validate_password.mixed_case_count`未満にすることはできません。例えば、変数が`1`に設定されている場合、パスワードには少なくとも1つの大文字と1つの小文字が含まれている必要があります。

### validate_password.number_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-number-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: TiDBセルフマネージドの場合は`[0, 2147483647]`と[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) `[1, 2147483647]`場合[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   この変数は、パスワードの複雑さチェックにおけるチェック項目です。パスワードに十分な数字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) `1` （MEDIUM）以上に設定されている場合にのみ有効になります。

### validate_password.policy <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-policy-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 列挙
-   デフォルト値: `1`
-   値のオプション: TiDB Self-Managed の場合は`0` 、 3 、 `1` 、 `2`および[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) [TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)場合は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 、 `1`および`2`
-   この変数は、パスワードの複雑さのチェックに関するポリシーを制御します。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)有効になっている場合にのみ有効になります。この変数の値によって、パスワードの複雑さのチェックにおいて、 `validate_password.check_user_name`を除く他の`validate-password`変数が有効になるかどうかが決まります。
-   この変数の値は`0` 、 `1` 、または`2` （それぞれLOW、MEDIUM、STRONGに相当）です。ポリシーレベルによってチェック内容が異なります。
    -   0 または LOW: パスワードの長さ。
    -   1 または MEDIUM: パスワードの長さ、大文字と小文字、数字、特殊文字。
    -   2 または強力: パスワードの長さ、大文字と小文字、数字、特殊文字、辞書の一致。

### validate_password.special_char_count <span class="version-mark">v6.5.0 の新機能</span> {#validate-password-special-char-count-span-class-version-mark-new-in-v6-5-0-span}

-   範囲: グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `1`
-   範囲: TiDBセルフマネージドの場合は`[0, 2147483647]`と[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) `[1, 2147483647]`場合[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)
-   この変数は、パスワードの複雑さチェックにおけるチェック項目です。パスワードに十分な特殊文字が含まれているかどうかをチェックします。この変数は、 [`validate_password.enable`](#password_reuse_interval-new-in-v650)が有効で、 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) `1` （中）以上に設定されている場合にのみ有効になります。

### バージョン {#version}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `8.0.11-TiDB-` (tidb バージョン)
-   この変数はMySQLのバージョンとTiDBのバージョンを返します。例：&#39;8.0.11-TiDB-v8.5.4&#39;。

### バージョンコメント {#version-comment}

-   範囲: なし
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: (文字列)
-   この変数は、TiDBのバージョンに関する追加情報を返します。例えば、「TiDB Server (Apache License 2.0) Community Edition、MySQL 8.0互換」などです。

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
> この変数は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合は読み取り専用です。

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: 整数
-   デフォルト値: `28800`
-   範囲: `[0, 31536000]`
-   単位: 秒
-   この変数は、ユーザーセッションのアイドルタイムアウトを制御します。値が0の場合、タイムアウトは無制限となります。

### 警告数 {#warning-count}

-   スコープ: セッション
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   デフォルト値: `0`
-   この読み取り専用変数は、以前実行されたステートメントで発生した警告の数を示します。

### ウィンドウイング_使用_高精度 {#windowing-use-high-precision}

-   スコープ: セッション | グローバル
-   クラスターに持続: はい
-   ヒント[SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)に該当: いいえ
-   タイプ: ブール値
-   デフォルト値: `ON`
-   この変数は、 [ウィンドウ関数](/functions-and-operators/window-functions.md)を計算するときに高精度モードを使用するかどうかを制御します。
