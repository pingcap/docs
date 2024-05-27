---
title: ticloud import start mysql
summary: ticloud import start mysql のリファレンス。
---

# ticloud インポート開始 mysql {#ticloud-import-start-mysql}

MySQL 互換データベースから[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターにテーブルをインポートします。

```shell
ticloud import start mysql [flags]
```

> **注記：**
>
> -   このコマンドを実行する前に、まず MySQL コマンドライン ツールがインストールされていることを確認してください。詳細については、 [インストール](/tidb-cloud/get-started-with-cli.md#installation)参照してください。
> -   ターゲット データベースにターゲット テーブルが既に存在する場合、このコマンドをテーブル インポートに使用するには、ターゲット テーブル名がソース テーブル名と同じであることを確認して、コマンドに`skip-create-table`フラグを追加します。
> -   ターゲット データベースにターゲット テーブルが存在しない場合は、このコマンドを実行すると、ターゲット データベースにソース テーブルと同じ名前のテーブルが自動的に作成されます。

## 例 {#examples}

-   対話モードでインポート タスクを開始します。

    ```shell
    ticloud import start mysql
    ```

-   非対話型モードでインポート タスクを開始します (TiDB Serverless クラスターのデフォルト ユーザー`<username-prefix>.root`を使用)。

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password>
    ```

-   非対話型モードでインポート タスクを開始します (特定のユーザーを使用)。

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password> --target-user <target-user>
    ```

-   ターゲット データベースにターゲット テーブルが既に存在する場合は、ターゲット テーブルの作成をスキップするインポート タスクを開始します。

    ```shell
    ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password> --skip-create-table
    ```

> **注記：**
>
> MySQL 8.0 では、デフォルトの照合順序として`utf8mb4_0900_ai_ci`使用されますが、これは現在 TiDB ではサポートされていません。ソース テーブルで`utf8mb4_0900_ai_ci`照合順序が使用されている場合は、インポート前に、ソース テーブルの照合順序を[TiDBの照合順序をサポート](/character-set-and-collation.md#character-sets-and-collations-supported-by-tidb)に変更するか、TiDB でターゲット テーブルを手動で作成する必要があります。

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                   | 説明                                                       | 必須  | 注記                       |
| --------------------- | -------------------------------------------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列  | クラスター ID を指定します。                                         | はい  | 非対話型モードでのみ動作します。         |
| -h, --help            | このコマンドのヘルプ情報を表示します。                                      | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| -p, --プロジェクトID 文字列    | プロジェクト ID を指定します。                                        | はい  | 非対話型モードでのみ動作します。         |
| --テーブルの作成をスキップ        | ターゲット データベースにターゲット テーブルが既に存在する場合は、ターゲット テーブルの作成をスキップします。 | いいえ | 非対話型モードでのみ動作します。         |
| --source-database 文字列 | ソース MySQL データベースの名前。                                     | はい  | 非対話型モードでのみ動作します。         |
| --source-host 文字列     | ソース MySQL インスタンスのホスト。                                    | はい  | 非対話型モードでのみ動作します。         |
| --source-password 文字列 | ソース MySQL インスタンスのパスワード。                                  | はい  | 非対話型モードでのみ動作します。         |
| --source-port 整数      | ソース MySQL インスタンスのポート。                                    | はい  | 非対話型モードでのみ動作します。         |
| --ソーステーブル文字列          | ソース MySQL データベース内のソース テーブル名。                             | はい  | 非対話型モードでのみ動作します。         |
| --source-user 文字列     | ソース MySQL インスタンスにログインするユーザー。                             | はい  | 非対話型モードでのみ動作します。         |
| --ターゲットデータベース文字列      | TiDB Serverless クラスター内のターゲット データベース名。                    | はい  | 非対話型モードでのみ動作します。         |
| --target-password 文字列 | ターゲット TiDB Serverless クラスターのパスワード。                       | はい  | 非対話型モードでのみ動作します。         |
| --ターゲットユーザー文字列        | ターゲット TiDB Serverless クラスターにログインするユーザー。                  | いいえ | 非対話型モードでのみ動作します。         |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                           |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------------ |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                     |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
