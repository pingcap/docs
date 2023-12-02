---
title: ticloud import start mysql
summary: The reference of `ticloud import start mysql`.
---

# ticloudインポート開始mysql {#ticloud-import-start-mysql}

MySQL 互換データベースから[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターにテーブルをインポートします。

```shell
ticloud import start mysql [flags]
```

> **注記：**
>
> -   このコマンドを実行する前に、まず MySQL コマンドライン ツールがインストールされていることを確認してください。詳細については、 [インストール](/tidb-cloud/get-started-with-cli.md#installation)を参照してください。
> -   ターゲット テーブルがターゲット データベースにすでに存在する場合、テーブルのインポートにこのコマンドを使用するには、ターゲット テーブル名がソース テーブル名と同じであることを確認し、コマンドに`skip-create-table`フラグを追加します。
> -   ターゲットテーブルがターゲットデータベースに存在しない場合、このコマンドを実行すると、ソーステーブルと同じ名前のテーブルがターゲットデータベースに自動的に作成されます。

## 例 {#examples}

-   対話モードでインポート タスクを開始します。

    ```shell
    ticloud import start mysql
    ```

-   非対話モードでインポート タスクを開始します (TiDB サーバーレス クラスターのデフォルト ユーザー`<username-prefix>.root`を使用)。

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password>
    ```

-   非対話モードでインポート タスクを開始します (特定のユーザーを使用)。

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password> --target-user <target-user>
    ```

-   ターゲット テーブルがターゲット データベースにすでに存在する場合、ターゲット テーブルの作成をスキップするインポート タスクを開始します。

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password> --skip-create-table
    ```

> **注記：**
>
> MySQL 8.0 はデフォルトの照合順序として`utf8mb4_0900_ai_ci`を使用しますが、これは現在 TiDB でサポートされていません。ソース テーブルで`utf8mb4_0900_ai_ci`照合順序が使用されている場合、インポート前にソース テーブルの照合順序を[TiDB の照合順序をサポート](/character-set-and-collation.md#character-sets-and-collations-supported-by-tidb)に変更するか、TiDB にターゲット テーブルを手動で作成する必要があります。

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                 | 説明                                                       | 必須  | 注記                       |
| ------------------- | -------------------------------------------------------- | --- | ------------------------ |
| -c、--cluster-id 文字列 | クラスターIDを指定します。                                           | はい  | 非対話モードでのみ動作します。          |
| -h, --help          | このコマンドのヘルプ情報を表示します。                                      | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| -p、--プロジェクトID文字列    | プロジェクトIDを指定します。                                          | はい  | 非対話モードでのみ動作します。          |
| --スキップ作成テーブル        | ターゲット テーブルがターゲット データベースにすでに存在する場合、ターゲット テーブルの作成をスキップします。 | いいえ | 非対話モードでのみ動作します。          |
| --ソースデータベース文字列      | ソース MySQL データベースの名前。                                     | はい  | 非対話モードでのみ動作します。          |
| --ソースホスト文字列         | ソース MySQL インスタンスのホスト。                                    | はい  | 非対話モードでのみ動作します。          |
| --source-パスワード文字列   | ソース MySQL インスタンスのパスワード。                                  | はい  | 非対話モードでのみ動作します。          |
| --source-port int   | ソース MySQL インスタンスのポート。                                    | はい  | 非対話モードでのみ動作します。          |
| --ソーステーブル文字列        | ソース MySQL データベース内のソース テーブル名。                             | はい  | 非対話モードでのみ動作します。          |
| --source-user 文字列   | ソース MySQL インスタンスにログインするユーザー。                             | はい  | 非対話モードでのみ動作します。          |
| --ターゲットデータベース文字列    | TiDB サーバーレス クラスター内のターゲット データベース名。                        | はい  | 非対話モードでのみ動作します。          |
| --ターゲットパスワード文字列     | ターゲット TiDB サーバーレス クラスターのパスワード。                           | はい  | 非対話モードでのみ動作します。          |
| --ターゲットユーザー文字列      | ターゲット TiDB サーバーレス クラスターにログインするユーザー。                      | いいえ | 非対話モードでのみ動作します。          |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                               | 必須  | 注記                                                                |
| -------------- | -------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                                   | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
