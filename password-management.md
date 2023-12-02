---
title: TiDB Password Management
summary: Learn the mechanism of user password management in TiDB.
---

# TiDB パスワード管理 {#tidb-password-management}

ユーザー パスワードのセキュリティを保護するために、TiDB は v6.5.0 以降、次のパスワード管理ポリシーをサポートします。

-   パスワードの複雑さのポリシー: 空のパスワードや弱いパスワードを防ぐために、ユーザーに強力なパスワードを設定するよう要求します。
-   パスワード有効期限ポリシー: ユーザーにパスワードを定期的に変更するよう要求します。
-   パスワード再利用ポリシー: ユーザーが古いパスワードを再利用できないようにします。
-   ログイン失敗の追跡と一時的なアカウント ロック ポリシー: 間違ったパスワードによって複数回ログインが失敗した後に、同じユーザーがログインを試みることを防ぐために、ユーザー アカウントを一時的にロックします。

## TiDB 認証資格情報storage {#tidb-authentication-credential-storage}

ユーザー ID の信頼性を確保するために、TiDB はユーザーが TiDBサーバーにログインするときにユーザーを認証するための資格情報としてパスワードを使用します。

このドキュメントで説明されている*パスワードは*、TiDB によって生成、保存、検証される内部認証情報を指します。 TiDB はユーザー パスワードを`mysql.user`システム テーブルに保存します。

次の認証プラグインは TiDB パスワード管理に関連しています。

-   `mysql_native_password`
-   `caching_sha2_password`
-   `tidb_sm3_password`

TiDB 認証プラグインの詳細については、 [認証プラグインのステータス](/security-compatibility-with-mysql.md#authentication-plugin-status)を参照してください。

## パスワードの複雑さのポリシー {#password-complexity-policy}

TiDB では、パスワードの複雑さのチェックはデフォルトで無効になっています。パスワードの複雑さに関連するシステム変数を構成することで、パスワードの複雑さのチェックを有効にし、ユーザーのパスワードがパスワードの複雑さのポリシーに準拠していることを確認できます。

パスワードの複雑さのポリシーには次の機能があります。

-   ユーザー パスワードをプレーンテキスト ( `CREATE USER` 、 `ALTER USER` 、および`SET PASSWORD`を含む) で設定する SQL ステートメントの場合、TiDB はパスワードの複雑さのポリシーに照らしてパスワードをチェックします。パスワードが要件を満たしていない場合、パスワードは拒否されます。
-   SQL 関数[`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_validate-password-strength)を使用して、パスワードの強度を検証できます。

> **注記：**
>
> -   `CREATE USER`ステートメントの場合、作成時にアカウントをロックできる場合でも、許容可能なパスワードを設定する必要があります。それ以外の場合、アカウントのロックが解除されると、このアカウントはパスワードの複雑さのポリシーに準拠していないパスワードを使用して TiDB にログインできます。
> -   パスワードの複雑さのポリシーの変更は、既存のパスワードには影響せず、新しく設定されたパスワードにのみ影響します。

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

各システム変数の詳細については、 [システム変数](/system-variables.md#validate_passwordcheck_user_name-new-in-v650)を参照してください。

### パスワードの複雑さのポリシーを構成する {#configure-password-complexity-policy}

このセクションでは、パスワードの複雑さのポリシーに関連するシステム変数の構成例を示します。

パスワードの複雑さのチェックを有効にします。

```sql
SET GLOBAL validate_password.enable = ON;
```

ユーザー名と同じパスワードの使用をユーザーに許可しないでください。

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

パスワードに`mysql`や`abcd`の単語が含まれないようにする辞書チェックを有効にします。

```sql
SET GLOBAL validate_password.dictionary = 'mysql;abcd';
```

> **注記：**
>
> -   値`validate_password.dictionary`は 1024 文字以内の文字列です。これには、パスワードに存在してはいけない単語のリストが含まれています。各単語はセミコロン ( `;` ) で区切られます。
> -   辞書チェックでは大文字と小文字が区別されません。

### パスワードの複雑さチェックの例 {#password-complexity-check-examples}

システム変数`validate_password.enable`が`ON`に設定されている場合、TiDB はパスワードの複雑さのチェックを有効にします。チェック結果の例は次のとおりです。

TiDB は、ユーザーの平文パスワードをデフォルトのパスワード複雑さポリシーと照合してチェックします。設定されたパスワードがポリシーを満たさない場合、パスワードは拒否されます。

```sql
mysql> ALTER USER 'test'@'localhost' IDENTIFIED BY 'abc';
ERROR 1819 (HY000): Require Password Length: 8
```

TiDB は、ハッシュされたパスワードをパスワードの複雑さのポリシーに照らしてチェックしません。

```sql
mysql> ALTER USER 'test'@'localhost' IDENTIFIED WITH mysql_native_password AS '*0D3CED9BEC10A777AEC23CCC353A8C08A633045E';
Query OK, 0 rows affected (0.01 sec)
```

最初にロックされたアカウントを作成する場合は、パスワードの複雑さのポリシーに一致するパスワードも設定する必要があります。そうしないと、作成は失敗します。

```sql
mysql> CREATE USER 'user02'@'localhost' ACCOUNT LOCK;
ERROR 1819 (HY000): Require Password Length: 8
```

### パスワード強度検証機能 {#password-strength-validation-function}

パスワードの強度を確認するには、 `VALIDATE_PASSWORD_STRENGTH()`機能を使用できます。この関数はパスワード引数を受け取り、0 (弱い) ～ 100 (強い) の整数を返します。

> **注記：**
>
> この関数は、現在のパスワードの複雑さのポリシーに基づいてパスワードの強度を評価します。パスワードの複雑さのポリシーが変更されると、同じパスワードでも異なる評価結果が得られる可能性があります。

次の例は、 `VALIDATE_PASSWORD_STRENGTH()`関数の使用方法を示しています。

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

## パスワードの有効期限ポリシー {#password-expiration-policy}

TiDB は、パスワードのセキュリティを向上させるためにユーザーが定期的にパスワードを変更する必要があるように、パスワード有効期限ポリシーの構成をサポートしています。アカウントのパスワードの有効期限を手動で設定したり、パスワードの自動有効期限のポリシーを確立したりできます。

自動パスワード有効期限ポリシーは、グローバル レベルおよびアカウント レベルで設定できます。データベース管理者は、グローバル レベルで自動パスワード有効期限ポリシーを確立したり、アカウント レベルのポリシーを使用してグローバル ポリシーをオーバーライドしたりできます。

パスワード有効期限ポリシーを設定する権限は次のとおりです。

-   `SUPER`または`CREATE USER`権限を持つデータベース管理者は、パスワードの有効期限を手動で設定できます。
-   `SUPER`または`CREATE USER`権限を持つデータベース管理者は、アカウント レベルのパスワード有効期限ポリシーを設定できます。
-   `SUPER`または`SYSTEM_VARIABLES_ADMINR`権限を持つデータベース管理者は、グローバル レベルのパスワード有効期限ポリシーを設定できます。

### 手動有効期限切れ {#manual-expiration}

アカウントのパスワードを手動で期限切れにするには、 `CREATE USER`または`ALTER USER`ステートメントを使用します。

```sql
ALTER USER 'test'@'localhost' PASSWORD EXPIRE;
```

データベース管理者によってアカウントのパスワードの有効期限が設定されている場合、TiDB にログインする前にパスワードを変更する必要があります。手動有効期限は取り消すことができません。

`CREATE ROLE`ステートメントを使用して作成されたロールの場合、ロールにはパスワードが必要ないため、ロールのパスワード フィールドは空です。このような場合、TiDB は`password_expired`属性を`'Y'`に設定します。これは、ロールのパスワードが手動で期限切れになることを意味します。この設計の目的は、ロールのロックが解除され、空のパスワードで TiDB にログインすることを防ぐことです。 `ALTER USER ... ACCOUNT UNLOCK`ステートメントによってロールのロックが解除されると、パスワードが空であっても、このアカウントを使用してログインできます。したがって、TiDB は`password_expired`属性を使用してパスワードを手動で期限切れにし、ユーザーがアカウントに有効なパスワードを設定する必要があるようにします。

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

### 自動有効期限切れ {#automatic-expiration}

パスワードの自動有効期限は、**パスワードの有効期間**と**パスワードの有効期間**に基づいて設定されます。

-   パスワードの有効期間: 最後にパスワードを変更した日から現在の日付までの時間間隔。最後にパスワードを変更した時刻は、システム テーブル`mysql.user`に記録されます。
-   パスワードの有効期間: TiDB へのログインにパスワードを使用できる日数。

パスワードが有効期間を超えて使用された場合、サーバーは自動的にパスワードを期限切れとして扱います。

TiDB は、グローバル レベルおよびアカウント レベルでの自動パスワード有効期限をサポートしています。

-   世界レベル

    システム変数[`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650)を設定して、パスワードの有効期間を制御できます。デフォルト値`0`は、パスワードの有効期限が切れないことを示します。このシステム変数が正の整数`N`に設定されている場合、パスワードの有効期間は`N`日であり、 `N`日ごとにパスワードを変更する必要があることを意味します。

    グローバル自動パスワード有効期限ポリシーは、アカウント レベルの上書きがないすべてのアカウントに適用されます。

    次の例では、パスワードの有効期間が 180 日であるグローバル自動パスワード有効期限ポリシーを確立します。

    ```sql
    SET GLOBAL default_password_lifetime = 180;
    ```

-   アカウントレベル

    個々のアカウントの自動パスワード有効期限ポリシーを確立するには、 `CREATE USER`または`ALTER USER`ステートメントで`PASSWORD EXPIRE`オプションを使用します。

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

    指定したアカウントのアカウント レベルの自動パスワード有効期限ポリシーを削除して、グローバルな自動パスワード有効期限ポリシーに従うようにします。

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE DEFAULT;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE DEFAULT;
    ```

### パスワードの有効期限チェックの仕組み {#password-expiration-check-mechanism}

クライアントが TiDBサーバーに接続すると、サーバーは次の順序でパスワードの有効期限が切れているかどうかを確認します。

1.  サーバーは、パスワードが手動で期限切れとして設定されているかどうかを確認します。
2.  パスワードが手動で期限切れになっていない場合、サーバーはパスワードの有効期間が設定された有効期間より長いかどうかを確認します。有効な場合、サーバーはパスワードを期限切れとして扱います。

### 期限切れのパスワードを処理する {#handle-an-expired-password}

パスワードの有効期限に関する TiDBサーバーの動作を制御できます。パスワードの有効期限が切れると、サーバーはクライアントを切断するか、クライアントを「サンドボックス モード」に制限します。 「サンドボックス モード」では、TiDBサーバーは期限切れのアカウントからの接続を許可します。ただし、そのような接続では、ユーザーはパスワードのリセットのみを許可されます。

TiDBサーバーは、 「サンドボックス モード」でパスワードが期限切れになったユーザーを制限するかどうかを制御できます。パスワードの有効期限が切れたときの TiDBサーバーの動作を制御するには、TiDB 構成ファイルで[`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650)パラメーターを構成します。

```toml
[security]
disconnect-on-expired-password = true
```

-   `disconnect-on-expired-password`が`true` (デフォルト) に設定されている場合、パスワードの有効期限が切れると、サーバーはクライアントを切断します。
-   `disconnect-on-expired-password`を`false`に設定すると、サーバーは「サンドボックス モード」を有効にし、ユーザーがサーバーに接続できるようにします。ただし、ユーザーができるのはパスワードのリセットのみです。パスワードがリセットされると、ユーザーは通常どおり SQL ステートメントを実行できるようになります。

`disconnect-on-expired-password`が有効な場合、アカウントのパスワードの有効期限が切れている場合、TiDB はアカウントからの接続を拒否します。このような場合は、次の方法でパスワードを変更できます。

-   通常のアカウントのパスワードの有効期限が切れた場合、管理者は SQL ステートメントを使用してアカウントのパスワードを変更できます。
-   管理者アカウントのパスワードの有効期限が切れた場合、別の管理者は SQL ステートメントを使用してアカウントのパスワードを変更できます。
-   管理者アカウントのパスワードの有効期限が切れており、パスワードの変更を手伝ってくれる他の管理者がいない場合は、 `skip-grant-table`メカニズムを使用してアカウントのパスワードを変更できます。詳細は[パスワードを忘れた場合の手続き](/user-account-management.md#forget-the-root-password)を参照してください。

## パスワード再利用ポリシー {#password-reuse-policy}

TiDB は、以前のパスワードの再利用を制限できます。パスワード再利用ポリシーは、パスワード変更の回数または経過時間、あるいはその両方に基づくことができます。

パスワード再利用ポリシーは、グローバル レベルおよびアカウント レベルで設定できます。パスワード再利用ポリシーをグローバル レベルで確立したり、アカウント レベルのポリシーを使用してグローバル ポリシーをオーバーライドしたりすることもできます。

TiDB はアカウントのパスワード履歴を記録し、履歴からの新しいパスワードの選択を制限します。

-   パスワード再利用ポリシーがパスワードの変更回数に基づいている場合、新しいパスワードは、指定された数の最新のパスワードと同じであってはなりません。たとえば、パスワード変更の最小回数が`3`に設定されている場合、新しいパスワードは以前の 3 つのパスワードのいずれかと同じにすることはできません。
-   パスワード再利用ポリシーが経過時間に基づいている場合、新しいパスワードは、指定された日数内に使用されたパスワードと同じであってはなりません。たとえば、パスワードの再利用間隔が`60`に設定されている場合、新しいパスワードは、過去 60 日以内に使用されたパスワードと同じにすることはできません。

> **注記：**
>
> 空のパスワードはパスワード履歴に記録されず、いつでも再利用できます。

### グローバルレベルのパスワード再利用ポリシー {#global-level-password-reuse-policy}

グローバルなパスワード再利用ポリシーを確立するには、 [`password_history`](/system-variables.md#password_history-new-in-v650)および[`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650)システム変数を使用します。

たとえば、過去 6 個のパスワードと過去 365 日以内に使用されたパスワードの再利用を禁止するグローバル パスワード再利用ポリシーを確立するには、次のようにします。

```sql
SET GLOBAL password_history = 6;
SET GLOBAL password_reuse_interval = 365;
```

グローバル パスワード再利用ポリシーは、アカウント レベルの上書きがないすべてのアカウントに適用されます。

### アカウントレベルのパスワード再利用ポリシー {#account-level-password-reuse-policy}

アカウントレベルのパスワード再利用ポリシーを確立するには、 `CREATE USER`または`ALTER USER`ステートメントで`PASSWORD HISTORY`および`PASSWORD REUSE INTERVAL`オプションを使用します。

例えば：

最新の 5 つのパスワードの再利用を禁止するには:

```sql
CREATE USER 'test'@'localhost' PASSWORD HISTORY 5;
ALTER USER 'test'@'localhost' PASSWORD HISTORY 5;
```

過去 365 日以内に使用したパスワードの再利用を禁止するには:

```sql
CREATE USER 'test'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'test'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
```

2 種類の再利用ポリシーを組み合わせるには、 `PASSWORD HISTORY`と`PASSWORD REUSE INTERVAL`の両方を使用します。

```sql
CREATE USER 'test'@'localhost'
  PASSWORD HISTORY 5
  PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'test'@'localhost'
  PASSWORD HISTORY 5
  PASSWORD REUSE INTERVAL 365 DAY;
```

指定したアカウントのアカウント レベルのパスワード再利用ポリシーを削除して、グローバル パスワード再利用ポリシーに従うようにするには、次の手順を実行します。

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
> -   パスワード再利用ポリシーを複数回設定すると、最後に設定した値が有効になります。
> -   `PASSWORD HISTORY`および`PASSWORD REUSE INTERVAL`オプションのデフォルト値は 0 で、これは再利用ポリシーが無効であることを意味します。
> -   ユーザー名を変更すると、TiDB は`mysql.password_history`システム テーブル内の対応するパスワード履歴を元のユーザー名から新しいユーザー名に移行します。

## ログイン失敗の追跡と一時的なアカウント ロック ポリシー {#failed-login-tracking-and-temporary-account-locking-policy}

TiDB は、アカウントのログイン試行の失敗回数を追跡できます。パスワードがブルート フォースによって解読されるのを防ぐために、TiDB はログイン試行が指定回数失敗した後にアカウントをロックできます。

> **注記：**
>
> -   TiDB は、失敗したログインの追跡とアカウント レベルでの一時的なアカウント ロックのみをサポートしており、グローバル レベルではサポートしていません。
> -   ログイン失敗とは、クライアントが接続試行中に正しいパスワードの入力に失敗したことを意味し、不明なユーザーやネットワークの問題による接続失敗は含まれません。
> -   アカウントの失敗したログインの追跡と一時的なアカウント ロックを有効にすると、アカウントがログインを試行するときに、そのアカウントは追加のチェックの対象になります。これは、特に同時実行性の高いログイン シナリオで、ログイン操作のパフォーマンスに影響します。

### ログイン失敗追跡ポリシーを構成する {#configure-the-login-failure-tracking-policy}

`CREATE USER`または`ALTER USER`ステートメントの`FAILED_LOGIN_ATTEMPTS`および`PASSWORD_LOCK_TIME`オプションを使用して、ログイン試行の失敗回数と各アカウントのロック時間を構成できます。使用可能な値のオプションは次のとおりです。

-   `FAILED_LOGIN_ATTEMPTS` : N。2 `N`連続してログインに失敗すると、アカウントは一時的にロックされます。 N の値の範囲は 0 ～ 32767 です。
-   `PASSWORD_LOCK_TIME` : N |無制限。
    -   N は、ログイン試行が連続して失敗した後、アカウントが`N`日間一時的にロックされることを意味します。 N の値の範囲は 0 ～ 32767 です。
    -   `UNBOUNDED` 、ロック時間が無制限で、アカウントのロックを手動で解除する必要があることを意味します。 N の値の範囲は 0 ～ 32767 です。

> **注記：**
>
> -   1 つの SQL ステートメントで設定できるのは`FAILED_LOGIN_ATTEMPTS`または`PASSWORD_LOCK_TIME`だけです。この場合、アカウントのロックは有効になりません。
> -   アカウントのロックは、 `FAILED_LOGIN_ATTEMPTS`と`PASSWORD_LOCK_TIME`が両方とも 0 でない場合にのみ有効になります。

アカウント ロック ポリシーは次のように構成できます。

ユーザーを作成し、アカウント ロック ポリシーを構成します。パスワードを 3 回連続で間違えると、アカウントは 3 日間一時的にロックされます。

```sql
CREATE USER 'test1'@'localhost' IDENTIFIED BY 'password' FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 3;
```

既存のユーザーのアカウント ロック ポリシーを変更します。パスワードを 4 回連続して間違って入力すると、アカウントは手動でロックを解除するまで無期限にロックされます。

```sql
ALTER USER 'test2'@'localhost' FAILED_LOGIN_ATTEMPTS 4 PASSWORD_LOCK_TIME UNBOUNDED;
```

既存のユーザーのアカウント ロック ポリシーを無効にします。

```sql
ALTER USER 'test3'@'localhost' FAILED_LOGIN_ATTEMPTS 0 PASSWORD_LOCK_TIME 0;
```

### ロックされたアカウントのロックを解除する {#unlock-the-locked-account}

次のシナリオでは、連続したパスワード エラーの数をリセットできます。

-   `ALTER USER ... ACCOUNT UNLOCK`ステートメントを実行するとき。
-   ログインに成功したとき。

次のシナリオでは、ロックされたアカウントのロックを解除できます。

-   ロック時間が終了すると、次回ログイン時にアカウントの自動ロックフラグがリセットされます。
-   `ALTER USER ... ACCOUNT UNLOCK`ステートメントを実行するとき。

> **注記：**
>
> 連続したログイン失敗によりアカウントがロックされた場合、アカウント ロック ポリシーを変更すると次のような影響があります。
>
> -   `FAILED_LOGIN_ATTEMPTS`を変更しても、アカウントのロック状態は変わりません。変更された`FAILED_LOGIN_ATTEMPTS`アカウントのロックが解除され、再度ログインを試行した後に有効になります。
> -   `PASSWORD_LOCK_TIME`を変更しても、アカウントのロック状態は変わりません。変更された`PASSWORD_LOCK_TIME`アカウントが再度ログインしようとしたときに有効になります。このとき、TiDB は新しいロック時間に達したかどうかを確認します。 「はい」の場合、TiDB はユーザーのロックを解除します。
