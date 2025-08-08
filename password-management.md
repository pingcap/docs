---
title: TiDB Password Management
summary: TiDB でのユーザー パスワード管理のメカニズムを学習します。
---

# TiDB パスワード管理 {#tidb-password-management}

ユーザー パスワードのセキュリティを保護するために、TiDB は v6.5.0 以降で次のパスワード管理ポリシーをサポートしています。

-   パスワードの複雑さのポリシー: 空のパスワードや弱いパスワードを防ぐために、ユーザーに強力なパスワードの設定を要求します。
-   パスワード有効期限ポリシー: ユーザーにパスワードを定期的に変更することを要求します。
-   パスワード再利用ポリシー: ユーザーが古いパスワードを再利用できないようにします。
-   ログイン失敗の追跡と一時的なアカウント ロック ポリシー: 間違ったパスワードによる複数回のログイン失敗後に同じユーザーがログインを試行するのを防ぐために、ユーザー アカウントを一時的にロックします。

## TiDB認証資格情報storage {#tidb-authentication-credential-storage}

ユーザー ID の信頼性を保証するために、TiDB は、ユーザーが TiDBサーバーにログインするときにパスワードを資格情報として使用してユーザーを認証します。

このドキュメントで説明されている*パスワードは*、TiDB によって生成、保存、検証される内部資格情報を指します。TiDB は、ユーザー パスワードを`mysql.user`システム テーブルに保存します。

次の認証プラグインは TiDB パスワード管理に関連しています。

-   `mysql_native_password`
-   `caching_sha2_password`
-   `tidb_sm3_password`

TiDB 認証プラグインの詳細については、 [認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status)参照してください。

## パスワードの複雑さのポリシー {#password-complexity-policy}

TiDBでは、パスワードの複雑さのチェックはデフォルトで無効になっています。パスワードの複雑さに関連するシステム変数を設定することで、パスワードの複雑さのチェックを有効にし、ユーザーのパスワードがパスワードの複雑さのポリシーに準拠していることを確認できます。

パスワードの複雑さのポリシーには次の機能があります。

-   プレーンテキストでユーザーパスワードを設定するSQL文（ `CREATE USER` `SET PASSWORD`含む）の場合、TiDBはパスワード複雑性ポリシーに照らしてパスワードをチェックします。パスワードが要件`ALTER USER`満たしていない場合、そのパスワードは拒否されます。
-   パスワードの強度を検証するには、SQL 関数[`VALIDATE_PASSWORD_STRENGTH()`](/functions-and-operators/encryption-and-compression-functions.md#validate_password_strength)使用できます。

> **注記：**
>
> -   `CREATE USER`ステートメントについてですが、アカウント作成時にロックできる場合でも、適切なパスワードを設定する必要があります。そうしないと、アカウントのロックが解除された際に、このアカウントはパスワード複雑性ポリシーに準拠していないパスワードを使用して TiDB にログインできてしまいます。
> -   パスワードの複雑さのポリシーを変更しても、既存のパスワードには影響せず、新しく設定されたパスワードにのみ影響します。

次の SQL ステートメントを実行すると、パスワードの複雑さのポリシーに関連するすべてのシステム変数を表示できます。

```sql
mysql> SHOW VARIABLES LIKE 'validate_password.%';

+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password.check_user_name    | ON     |
| validate_password.dictionary         |        |
| validate_password.enable             | OFF    |
| validate_password.length             | 8      |
| validate_password.mixed_case_count   | 1      |
| validate_password.number_count       | 1      |
| validate_password.policy             | MEDIUM |
| validate_password.special_char_count | 1      |
+--------------------------------------+--------+
8 rows in set (0.00 sec)
```

各システム変数の詳細な説明については、 [システム変数](/system-variables.md#validate_passwordcheck_user_name-new-in-v650)参照してください。

### パスワードの複雑さのポリシーを構成する {#configure-password-complexity-policy}

このセクションでは、パスワードの複雑さのポリシーに関連するシステム変数を構成する例を示します。

パスワードの複雑さのチェックを有効にします。

```sql
SET GLOBAL validate_password.enable = ON;
```

ユーザー名と同じパスワードの使用をユーザーに許可しません。

```sql
SET GLOBAL validate_password.check_user_name = ON;
```

パスワードの複雑さのレベルを`LOW`に設定します。

```sql
SET GLOBAL validate_password.policy = LOW;
```

パスワードの最小長を`10`に設定します。

```sql
SET GLOBAL validate_password.length = 10;
```

パスワードには少なくとも 2 つの数字、1 つの大文字、1 つの小文字、および 1 つの特殊文字を含める必要があります。

```sql
SET GLOBAL validate_password.number_count = 2;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.special_char_count = 1;
```

パスワードに`mysql`や`abcd`などの単語が含まれないようにする辞書チェックを有効にします。

```sql
SET GLOBAL validate_password.dictionary = 'mysql;abcd';
```

> **注記：**
>
> -   値`validate_password.dictionary`は1024文字以下の文字列です。パスワードに存在してはならない単語のリストが含まれます。各単語はセミコロン ( `;` ) で区切られます。
> -   辞書チェックでは大文字と小文字は区別されません。

### パスワードの複雑さのチェック例 {#password-complexity-check-examples}

システム変数`validate_password.enable` `ON`に設定すると、TiDB はパスワードの複雑さのチェックを有効にします。チェック結果の例を以下に示します。

TiDBは、ユーザーのプレーンテキストパスワードをデフォルトのパスワード複雑性ポリシーと照合します。設定されたパスワードがポリシーを満たしていない場合、そのパスワードは拒否されます。

```sql
mysql> ALTER USER 'test'@'localhost' IDENTIFIED BY 'abc';
ERROR 1819 (HY000): Require Password Length: 8
```

TiDB は、ハッシュされたパスワードをパスワード複雑さポリシーと照合しません。

```sql
mysql> ALTER USER 'test'@'localhost' IDENTIFIED WITH mysql_native_password AS '*0D3CED9BEC10A777AEC23CCC353A8C08A633045E';
Query OK, 0 rows affected (0.01 sec)
```

最初にロックされたアカウントを作成するときは、パスワードの複雑さのポリシーに一致するパスワードも設定する必要があります。そうしないと、作成は失敗します。

```sql
mysql> CREATE USER 'user02'@'localhost' ACCOUNT LOCK;
ERROR 1819 (HY000): Require Password Length: 8
```

### パスワード強度検証機能 {#password-strength-validation-function}

パスワードの強度を確認するには、 [`VALIDATE_PASSWORD_STRENGTH()`](/functions-and-operators/encryption-and-compression-functions.md#validate_password_strength)関数を使用します。この関数はパスワード引数を受け取り、0（弱い）から100（強い）までの整数を返します。

> **注記：**
>
> この関数は、現在のパスワード複雑性ポリシーに基づいてパスワードの強度を評価します。パスワード複雑性ポリシーが変更された場合、同じパスワードでも評価結果が異なる場合があります。

次の例は、 [`VALIDATE_PASSWORD_STRENGTH()`](/functions-and-operators/encryption-and-compression-functions.md#validate_password_strength)関数の使用方法を示しています。

```sql
mysql> SELECT VALIDATE_PASSWORD_STRENGTH('weak');
+------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('weak') |
+------------------------------------+
|                                 25 |
+------------------------------------+
1 row in set (0.01 sec)

mysql> SELECT VALIDATE_PASSWORD_STRENGTH('lessweak$_@123');
+----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('lessweak$_@123') |
+----------------------------------------------+
|                                           50 |
+----------------------------------------------+
1 row in set (0.01 sec)

mysql> SELECT VALIDATE_PASSWORD_STRENGTH('N0Tweak$_@123!');
+----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('N0Tweak$_@123!') |
+----------------------------------------------+
|                                          100 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

## パスワード有効期限ポリシー {#password-expiration-policy}

TiDBは、パスワードのセキュリティ強化のため、ユーザーが定期的にパスワードを変更することを義務付けるパスワード有効期限ポリシーの設定をサポートしています。アカウントのパスワードを手動で有効期限切れにすることも、自動的にパスワードを有効期限切れにするポリシーを設定することもできます。

自動パスワード有効期限ポリシーは、グローバルレベルとアカウントレベルで設定できます。データベース管理者は、グローバルレベルで自動パスワード有効期限ポリシーを設定できるほか、アカウントレベルのポリシーを使用してグローバルポリシーをオーバーライドすることもできます。

パスワード有効期限ポリシーを設定するための権限は次のとおりです。

-   `SUPER`または`CREATE USER`権限を持つデータベース管理者は、手動でパスワードの有効期限を設定できます。
-   `SUPER`または`CREATE USER`権限を持つデータベース管理者は、アカウント レベルのパスワード有効期限ポリシーを設定できます。
-   `SUPER`または`SYSTEM_VARIABLES_ADMINR`権限を持つデータベース管理者は、グローバル レベルのパスワード有効期限ポリシーを設定できます。

### 手動での有効期限 {#manual-expiration}

アカウント パスワードを手動で期限切れにするには、 `CREATE USER`または`ALTER USER`ステートメントを使用します。

```sql
ALTER USER 'test'@'localhost' PASSWORD EXPIRE;
```

データベース管理者によってアカウントのパスワードの有効期限が設定されている場合、TiDBにログインする前にパスワードを変更する必要があります。手動で設定した有効期限は取り消すことはできません。

`CREATE ROLE`文で作成されたロールはパスワードを必要としないため、パスワードフィールドは空になります。このような場合、TiDB は`password_expired`属性を`'Y'`に設定します。これは、ロールのパスワードが手動で期限切れになっていることを意味します。この設計の目的は、ロールのロックが解除され、空のパスワードで TiDB にログインすることを防ぐことです。7 文でロールのロックが解除されると、パスワードが空であってもこのアカウントでログインできます。そのため、TiDB は`ALTER USER ... ACCOUNT UNLOCK`属性`password_expired`使用してパスワードを手動で期限切れにし、ユーザーがアカウントに有効なパスワードを設定するようにしています。

```sql
mysql> CREATE ROLE testrole;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT user,password_expired,Account_locked FROM mysql.user WHERE user = 'testrole';
+----------+------------------+----------------+
| user     | password_expired | Account_locked |
+----------+------------------+----------------+
| testrole | Y                | Y              |
+----------+------------------+----------------+
1 row in set (0.02 sec)
```

### 自動有効期限 {#automatic-expiration}

自動パスワード有効期限は、**パスワードの有効期間**と**パスワードの有効期間**に基づいて設定されます。

-   パスワードの有効期間：前回のパスワード変更日から現在までの期間。前回のパスワード変更時刻は、システムテーブル`mysql.user`に記録されます。
-   パスワードの有効期間: TiDB へのログインにパスワードを使用できる日数。

パスワードの有効期間よりも長い期間使用された場合、サーバーは自動的にそのパスワードを期限切れとして扱います。

TiDB は、グローバル レベルとアカウント レベルでの自動パスワード有効期限をサポートします。

-   世界レベル

    システム変数[`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650)を設定することで、パスワードの有効期間を制御できます。デフォルト値`0` 、パスワードが無期限であることを示します。このシステム変数を正の整数`N`に設定すると、パスワードの有効期間は`N`日間となり、 `N`日ごとにパスワードを変更する必要があります。

    グローバル自動パスワード有効期限ポリシーは、アカウント レベルのオーバーライドを持たないすべてのアカウントに適用されます。

    次の例では、パスワードの有効期間が 180 日間のグローバル自動パスワード有効期限ポリシーを確立します。

    ```sql
    SET GLOBAL default_password_lifetime = 180;
    ```

-   アカウントレベル

    個々のアカウントに対して自動パスワード有効期限ポリシーを確立するには、 `CREATE USER`または`ALTER USER`ステートメントの`PASSWORD EXPIRE`オプションを使用します。

    次の例では、ユーザー パスワードを 90 日ごとに変更する必要があります。

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;
    ```

    次の例では、個々のアカウントの自動パスワード有効期限ポリシーを無効にします。

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE NEVER;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE NEVER;
    ```

    指定されたアカウントのアカウント レベルの自動パスワード有効期限ポリシーを削除して、グローバル自動パスワード有効期限ポリシーに従うようにします。

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE DEFAULT;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE DEFAULT;
    ```

### パスワード有効期限チェックメカニズム {#password-expiration-check-mechanism}

クライアントが TiDBサーバーに接続すると、サーバーは次の順序でパスワードの有効期限が切れていないかどうかを確認します。

1.  サーバーは、パスワードが手動で期限切れに設定されているかどうかを確認します。
2.  パスワードが手動で期限切れに設定されていない場合、サーバーはパスワードの有効期間が設定された有効期限よりも長いかどうかを確認します。有効期間が長い場合、サーバーはパスワードを期限切れとして扱います。

### 期限切れのパスワードの処理 {#handle-an-expired-password}

パスワードの有効期限切れに関するTiDBサーバーの動作を制御できます。パスワードの有効期限が切れると、サーバーはクライアントを切断するか、クライアントを「サンドボックスモード」に制限します。「サンドボックスモード」では、TiDBサーバーは期限切れのアカウントからの接続を許可します。ただし、この接続では、ユーザーはパスワードのリセットのみを実行できます。

TiDBサーバーは、「サンドボックスモード」において、パスワードの有効期限が切れたユーザーを制限するかどうかを制御できます。パスワードの有効期限が切れた場合のTiDBサーバーの動作を制御するには、TiDB設定ファイルの[`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)のパラメータを設定します。

```toml
[security]
disconnect-on-expired-password = true
```

-   `disconnect-on-expired-password` `true` (デフォルト) に設定すると、パスワードの有効期限が切れるとサーバーはクライアントとの接続を切断します。
-   `disconnect-on-expired-password` `false`に設定すると、サーバーは「サンドボックスモード」を有効にし、ユーザーがサーバーに接続できるようにします。ただし、ユーザーはパスワードのリセットのみ可能です。パスワードをリセットすると、ユーザーはSQL文を通常どおり実行できるようになります。

`disconnect-on-expired-password`有効になっている場合、アカウントのパスワードが期限切れになると、TiDB はそのアカウントからの接続を拒否します。このような場合、以下の方法でパスワードを変更できます。

-   通常のアカウントのパスワードの有効期限が切れた場合、管理者は SQL ステートメントを使用してアカウントのパスワードを変更できます。
-   管理者アカウントのパスワードの有効期限が切れた場合、別の管理者が SQL ステートメントを使用してアカウントのパスワードを変更できます。
-   管理者アカウントのパスワードが期限切れで、パスワードの変更を手伝ってくれる他の管理者がいない場合は、 `skip-grant-table`メカニズムを使用してアカウントのパスワードを変更できます。詳細については、 [パスワードを忘れた場合の手続き](/user-account-management.md#forget-the-root-password)参照してください。

## パスワード再利用ポリシー {#password-reuse-policy}

TiDBは、以前のパスワードの再利用を制限できます。パスワード再利用ポリシーは、パスワードの変更回数、経過時間、またはその両方に基づいて設定できます。

パスワード再利用ポリシーは、グローバルレベルとアカウントレベルで設定できます。グローバルレベルでパスワード再利用ポリシーを設定することも、アカウントレベルのポリシーでグローバルポリシーをオーバーライドすることもできます。

TiDB はアカウントのパスワード履歴を記録し、履歴からの新しいパスワードの選択を制限します。

-   パスワード再利用ポリシーがパスワード変更回数に基づいている場合、新しいパスワードは指定された回数の最新のパスワードのいずれとも重複してはなりません。例えば、パスワード変更の最小回数が`3`に設定されている場合、新しいパスワードは過去3回のパスワードのいずれとも重複してはなりません。
-   パスワード再利用ポリシーが経過時間に基づいている場合、新しいパスワードは指定された日数内に使用されたパスワードと同じであってはなりません。例えば、パスワード再利用間隔が`60`に設定されている場合、新しいパスワードは過去60日間に使用されたパスワードと同じであってはなりません。

> **注記：**
>
> 空のパスワードはパスワード履歴に記録されず、いつでも再利用できます。

### グローバルレベルのパスワード再利用ポリシー {#global-level-password-reuse-policy}

グローバル パスワード再利用ポリシーを確立するには、システム変数[`password_history`](/system-variables.md#password_history-new-in-v650)と[`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650)使用します。

たとえば、過去 6 個のパスワードと過去 365 日以内に使用されたパスワードの再利用を禁止するグローバル パスワード再利用ポリシーを確立するには、次のようにします。

```sql
SET GLOBAL password_history = 6;
SET GLOBAL password_reuse_interval = 365;
```

グローバル パスワード再利用ポリシーは、アカウント レベルのオーバーライドを持たないすべてのアカウントに適用されます。

### アカウントレベルのパスワード再利用ポリシー {#account-level-password-reuse-policy}

アカウント レベルのパスワード再利用ポリシーを確立するには、 `CREATE USER`または`ALTER USER`ステートメントの`PASSWORD HISTORY`および`PASSWORD REUSE INTERVAL`オプションを使用します。

例えば：

過去 5 つのパスワードの再利用を禁止するには:

```sql
CREATE USER 'test'@'localhost' PASSWORD HISTORY 5;
ALTER USER 'test'@'localhost' PASSWORD HISTORY 5;
```

過去 365 日以内に使用したパスワードの再利用を禁止するには:

```sql
CREATE USER 'test'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'test'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
```

2 種類の再利用ポリシーを組み合わせるには、 `PASSWORD HISTORY`と`PASSWORD REUSE INTERVAL`両方を使用します。

```sql
CREATE USER 'test'@'localhost'
  PASSWORD HISTORY 5
  PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'test'@'localhost'
  PASSWORD HISTORY 5
  PASSWORD REUSE INTERVAL 365 DAY;
```

指定されたアカウントのアカウント レベルのパスワード再利用ポリシーを削除して、グローバル パスワード再利用ポリシーに従うようにするには、次の手順を実行します。

```sql
CREATE USER 'test'@'localhost'
  PASSWORD HISTORY DEFAULT
  PASSWORD REUSE INTERVAL DEFAULT;
ALTER USER 'test'@'localhost'
  PASSWORD HISTORY DEFAULT
  PASSWORD REUSE INTERVAL DEFAULT;
```

> **注記：**
>
> -   パスワード再利用ポリシーを複数回設定した場合、最後に設定した値が有効になります。
> -   オプション`PASSWORD HISTORY`および`PASSWORD REUSE INTERVAL`のデフォルト値は 0 で、再利用ポリシーが無効であることを意味します。
> -   ユーザー名を変更すると、TiDB は`mysql.password_history`システム テーブル内の対応するパスワード履歴を元のユーザー名から新しいユーザー名に移行します。

## ログイン失敗の追跡と一時的なアカウントロックポリシー {#failed-login-tracking-and-temporary-account-locking-policy}

TiDBは、アカウントのログイン失敗回数を追跡できます。ブルートフォース攻撃によるパスワード解読を防ぐため、TiDBは指定回数のログイン失敗後にアカウントをロックすることができます。

> **注記：**
>
> -   TiDB は、失敗したログインの追跡と一時的なアカウントのロックをアカウント レベルでのみサポートしており、グローバル レベルではサポートしていません。
> -   ログイン失敗とは、クライアントが接続試行中に正しいパスワードを入力できなかったことを意味し、不明なユーザーまたはネットワークの問題による接続失敗は含まれません。
> -   アカウントに対して失敗したログインの追跡と一時的なアカウントのロックを有効にすると、アカウントがログインを試行するときに追加のチェックが実行されます。これは、特に同時ログインが多いシナリオでは、ログイン操作のパフォーマンスに影響します。

### ログイン失敗追跡ポリシーを構成する {#configure-the-login-failure-tracking-policy}

`CREATE USER`または`ALTER USER`ステートメントの`FAILED_LOGIN_ATTEMPTS`および`PASSWORD_LOCK_TIME`オプションを使用して、各アカウントのログイン失敗回数とロック時間を設定できます。使用可能な値オプションは次のとおりです。

-   `FAILED_LOGIN_ATTEMPTS` : N。2 `N`連続してログインに失敗すると、アカウントは一時的にロックされます。Nの値の範囲は0～32767です。
-   `PASSWORD_LOCK_TIME` : N | 無制限。
    -   Nは、連続してログインに失敗すると、アカウントが`N`日間一時的にロックされることを意味します。Nの値の範囲は0～32767です。
    -   `UNBOUNDED`ロック時間が無制限であり、アカウントを手動でロック解除する必要があることを意味します。Nの値の範囲は0から32767です。

> **注記：**
>
> -   1つのSQL文で設定できるのは`FAILED_LOGIN_ATTEMPTS`または`PASSWORD_LOCK_TIME`だけです。この場合、アカウントロックは有効になりません。
> -   アカウントのロックは、 `FAILED_LOGIN_ATTEMPTS`と`PASSWORD_LOCK_TIME`両方が 0 でない場合にのみ有効になります。

アカウント ロック ポリシーは次のように構成できます。

ユーザーを作成し、アカウントロックポリシーを設定します。パスワードを3回連続して間違えると、アカウントは3日間一時的にロックされます。

```sql
CREATE USER 'test1'@'localhost' IDENTIFIED BY 'password' FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 3;
```

既存ユーザーのアカウントロックポリシーを変更します。パスワードを4回連続して間違えると、手動でロック解除するまでアカウントは無期限にロックされます。

```sql
ALTER USER 'test2'@'localhost' FAILED_LOGIN_ATTEMPTS 4 PASSWORD_LOCK_TIME UNBOUNDED;
```

既存のユーザーのアカウント ロック ポリシーを無効にします。

```sql
ALTER USER 'test3'@'localhost' FAILED_LOGIN_ATTEMPTS 0 PASSWORD_LOCK_TIME 0;
```

### ロックされたアカウントのロックを解除する {#unlock-the-locked-account}

次のシナリオでは、連続したパスワードエラーの回数をリセットできます。

-   `ALTER USER ... ACCOUNT UNLOCK`ステートメントを実行するとき。
-   ログインに成功したとき。

次のシナリオでは、ロックされたアカウントのロックを解除できます。

-   ロック時間が終了すると、次回のログイン試行時にアカウントの自動ロックフラグがリセットされます。
-   `ALTER USER ... ACCOUNT UNLOCK`ステートメントを実行するとき。

> **注記：**
>
> 連続してログインに失敗したためにアカウントがロックされた場合、アカウント ロック ポリシーを変更すると、次の影響があります。
>
> -   `FAILED_LOGIN_ATTEMPTS`変更しても、アカウントのロック状態は変わりません。3 `FAILED_LOGIN_ATTEMPTS`変更は、アカウントのロックが解除され、再度ログインを試みた後に有効になります。
> -   `PASSWORD_LOCK_TIME`変更しても、アカウントのロック状態は変わりません。3 `PASSWORD_LOCK_TIME`変更は、アカウントが再度ログインしようとした際に有効になります。その際、TiDB は新しいロック時間が経過したかどうかを確認します。経過した場合、TiDB はユーザーのロックを解除します。
