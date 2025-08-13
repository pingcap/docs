---
title: Database Audit Logging for TiDB Cloud Starter and Essential
summary: TiDB TiDB CloudでTiDB Cloud Starter またはTiDB Cloud Essential クラスターを監査する方法について説明します。
---

# TiDB Cloud StarterおよびEssential向けデータベース監査ログ（ベータ版） {#database-audit-logging-beta-for-tidb-cloud-starter-and-essential}

TiDB Cloud Starter およびTiDB Cloud Essential は、ユーザー アクセスの詳細 (実行された SQL ステートメントなど) の履歴をログに記録するデータベース監査ログ機能を提供します。

> **注記：**
>
> 現在、データベース監査ログ機能はリクエストに応じてのみご利用いただけます。この機能をリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポートをリクエスト」**をクリックしてください。次に、 **「説明」**欄に「 TiDB Cloud Starter またはTiDB Cloud Essential データベース監査ログの申請」と入力し、 **「送信**」をクリックしてください。

組織のユーザー アクセス ポリシーやその他の情報セキュリティ対策の有効性を評価するには、データベース監査ログを定期的に分析することがセキュリティのベスト プラクティスです。

監査ログ機能はデフォルトで無効になっています。クラスターを監査するには、クラスターの監査ログを有効にする必要があります。

## 監査ログを有効にする {#enable-audit-logging}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターの監査ログを有効にするには、 [TiDB CloudCLI](/tidb-cloud/ticloud-auditlog-config.md)使用します。

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled
```

TiDB Cloud Starter またはTiDB Cloud Essential クラスターの監査ログを無効にするには、 [TiDB CloudCLI](/tidb-cloud/ticloud-auditlog-config.md)使用します。

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled=false
```

> **注記：**
>
> 監査ログを有効にするだけでは監査ログは生成されません。ログに記録するイベントを指定するには、フィルターを設定する必要があります。詳細については、 [監査ログフィルタルールを管理する](#manage-audit-logging-filter-rules)ご覧ください。

## 監査ログフィルタルールを管理する {#manage-audit-logging-filter-rules}

監査ログをフィルタリングするには、ログに記録するイベントを指定するためのフィルタルールを作成する必要があります。フィルタルールは[TiDB CloudCLI](/tidb-cloud/ticloud-auditlog-filter-create.md)使用して管理できます。

フィルター ルールには次のフィールドが含まれます。

-   `users` : 監査イベントをフィルタリングするユーザー名のリスト。ワイルドカード`%`使用すると、任意のユーザー名に一致します。
-   `filters` : フィルターオブジェクトのリスト。各フィルターオブジェクトには以下のフィールドが含まれます。

    -   `classes` : 監査イベントをフィルタリングするイベントクラスのリスト。例： `["QUERY", "EXECUTE"]` 。
    -   `tables` : テーブルフィルターのリスト。詳細については、[テーブルフィルター]を参照してください。
    -   `statusCodes` : 監査イベントをフィルター処理するためのステータス コードのリスト。2 `1`成功、 `0`失敗を意味します。

データベース監査ログのすべてのイベント クラスの概要は次のとおりです。

| イベントクラス  | 説明                                                          | 親クラス      |
| -------- | ----------------------------------------------------------- | --------- |
| 繋がり      | ハンドシェイク、接続、切断、接続のリセット、ユーザーの変更など、接続に関連するすべての操作を記録します。        | <li></li> |
| 接続する     | 接続時のハンドシェイクのすべての操作を記録する                                     | 繋がり       |
| 切断       | 切断のすべての操作を記録する                                              | 繋がり       |
| ユーザーの変更  | 変更するユーザーのすべての操作を記録する                                        | 繋がり       |
| クエリ      | データのクエリと変更に関するすべてのエラーを含む、SQL ステートメントのすべての操作を記録します。          | <li></li> |
| 取引       | `BEGIN`など、取引に関連する`COMMIT`の操作`ROLLBACK`記録する                  | クエリ       |
| 実行する     | `EXECUTE`ステートメントのすべての操作を記録する                                | クエリ       |
| クエリ_DML  | `INSERT` `REPLACE`含むDML `LOAD DATA`の`UPDATE`の操作`DELETE`記録する | クエリ       |
| 入れる      | `INSERT`ステートメントのすべての操作を記録する                                 | クエリ_DML   |
| 交換する     | `REPLACE`ステートメントのすべての操作を記録する                                | クエリ_DML   |
| アップデート   | `UPDATE`ステートメントのすべての操作を記録する                                 | クエリ_DML   |
| 消去       | `DELETE`ステートメントのすべての操作を記録する                                 | クエリ_DML   |
| データをロード  | `LOAD DATA`ステートメントのすべての操作を記録する                              | クエリ_DML   |
| 選択       | `SELECT`ステートメントのすべての操作を記録する                                 | クエリ       |
| クエリ_DDL  | DDL文のすべての操作を記録する                                            | クエリ       |
| 監査       | システム変数の設定やシステム関数の呼び出しなど、TiDB データベース監査の設定に関連するすべての操作を記録します。  | <li></li> |
| 監査機能呼び出し | TiDBデータベース監査に関連するシステム関数の呼び出し操作をすべて記録します。                    | 監査        |

### フィルタールールを作成する {#create-a-filter-rule}

すべての監査ログをキャプチャするフィルタ ルールを作成するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

すべての EXECUTE イベントをフィルタリングするフィルタ ルールを作成するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter create --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["EXECUTE"]]}'
```

### フィルタルールを更新する {#update-a-filter-rule}

フィルター ルールを無効にするには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --enabled=false
```

フィルター ルールを更新するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter update --cluster-id <cluster-id> --name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

更新時には、完全な`--rule`フィールドを渡す必要があることに注意してください。

### フィルタルールを削除する {#delete-a-filter-rule}

フィルター ルールを削除するには、次のコマンドを実行します。

```shell
ticloud serverless audit-log filter delete --cluster-id <cluster-id> --name <rule-name>
```

## 監査ログを構成する {#configure-audit-logging}

### データ編集 {#data-redaction}

TiDB Cloud StarterとTiDB Cloud Essentialは、監査ログ内の機密データをデフォルトで編集します。次のSQL文を例に挙げましょう。

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES (1, 'Alice', '123456');
```

以下のように編集されています。

```sql
INSERT INTO `test`.`users` (`id`, `name`, `password`) VALUES ( ... );
```

編集を無効にする場合は、 [TiDB CloudCLI](/tidb-cloud/ticloud-auditlog-config.md)使用します。

```shell
ticloud serverless audit-log config --cluster-id <cluster-id> --unredacted
```

### ログファイルのローテーション {#log-file-rotation}

TiDB Cloud Starter およびTiDB Cloud Essential は、次のいずれかの条件が満たされると、新しい監査ログ ファイルを生成します。

-   現在のログ ファイルのサイズは 100 MiB に達します。
-   前回のログ生成から1時間が経過しました。内部のスケジュール設定によっては、ログ生成が数分遅れる場合があります。

> **注記：**
>
> 現在、ログファイルのローテーション設定は変更できません。TiDB TiDB Cloud Starter およびTiDB Cloud Essential は、上記の条件に基づいて監査ログファイルを自動的にローテーションします。

## アクセス監査ログ {#access-audit-logging}

TiDB Cloud Starter およびTiDB Cloud Essential 監査ログは、 `YYYY-MM-DD-<index>.log`という名前の読み取り可能なテキスト ファイルとして保存されます。

現在、監査ログはTiDB Cloud内に365日間保存されます。この期間が経過すると、ログは自動的に削除されます。

> **注記：**
>
> 監査ログを外部storage(Amazon S3、Azure Blob Storage、Google Cloud Storage、Alibaba Cloud OSS など) に保存する必要がある場合は、 [TiDB Cloudサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

監査ログを表示およびダウンロードするには、 [TiDB CloudCLI](/tidb-cloud/ticloud-auditlog-download.md)使用します。

```shell
ticloud serverless audit-log download --cluster-id <cluster-id> --output-path <output-path> --start-date <start-date> --end-date <end-date>
```

-   `start-date` : ダウンロードする監査ログの開始日（ `YYYY-MM-DD`の形式、例`2025-01-01` ）。
-   `end-date` : ダウンロードする監査ログの終了日（ `YYYY-MM-DD`の形式、例`2025-01-01` ）。

> **注記：**
>
> TiDB Cloud StarterおよびTiDB Cloud Essentialは、監査ログの順序付けを保証しません`YYYY-MM-DD-<index>.log`という名前のログファイルには、以前の日付の監査ログが含まれている可能性があります。特定の日付（例えば2025年1月1日）のすべてのログを取得したい場合は、通常は`--start-date 2025-01-01`と`--end-date 2025-01-02`指定すれば問題ありません。ただし、極端な状況では、すべてのログファイルをダウンロードし、 `TIME`フィールドで順序付けする必要があるかもしれません。

## 監査ログフィールド {#audit-logging-fields}

監査ログ内の各データベース イベント レコードに対して、TiDB は次のフィールドを提供します。

### 一般情報 {#general-information}

すべてのクラスの監査ログには、次の情報が含まれます。

| 分野                           | 説明                                          |
| ---------------------------- | ------------------------------------------- |
| ID                           | 操作の監査記録を識別する一意の識別子                          |
| 時間                           | 監査記録のタイムスタンプ                                |
| イベント                         | 監査レコードのイベントクラス。複数のイベントタイプはカンマで区切られます（ `,` ） |
| ユーザー                         | 監査レコードのユーザー名                                |
| 役割                           | 操作時のユーザーの役割                                 |
| 接続ID                         | ユーザーの接続の識別子                                 |
| テーブル                         | この監査レコードに関連するアクセスされたテーブル                    |
| ステータスコード                     | 監査レコードのステータス コード。1 `1`成功、 `0`失敗を意味します。      |
| キースペース名                      | 監査レコードのキースペース名。                             |
| サーバーレステナントID                 | クラスターが属するサーバーレス テナントの ID。                   |
| サーバーレス_TSERVERLESS_プロジェクト_ID | クラスターが属するサーバーレス プロジェクトの ID。                 |
| サーバーレスクラスターID                | 監査レコードが属するサーバーレス クラスターの ID。                 |
| 理由                           | 監査レコードのエラーメッセージ。操作中にエラーが発生した場合にのみ記録されます。    |

### SQL文の情報 {#sql-statement-information}

イベント クラスが`QUERY`または`QUERY`のサブクラスの場合、監査ログには次の情報が含まれます。

| 分野        | 説明                                                                  |
| --------- | ------------------------------------------------------------------- |
| 現在のデータベース | 現在のデータベースの名前。                                                       |
| SQL_TEXT  | 実行された SQL 文。監査ログの編集が有効になっている場合は、編集された SQL 文が記録されます。                 |
| 実行パラメータ   | `EXECUTE`ステートメントのパラメータ。イベントクラスに`EXECUTE`含まれ、編集が無効になっている場合にのみ記録されます。 |
| 影響を受ける行   | SQL文の影響を受けた行数。イベントクラスに`QUERY_DML`含まれる場合にのみ記録されます。                   |

### 接続情報 {#connection-information}

イベント クラスが`CONNECTION`または`CONNECTION`のサブクラスの場合、監査ログには次の情報が含まれます。

| 分野        | 説明                                                   |
| --------- | ---------------------------------------------------- |
| 現在のデータベース | 現在のデータベースの名前。イベントクラスにDISCONNECTが含まれる場合、この情報は記録されません。 |
| 接続タイプ     | 接続の種類 (ソケット、UnixSocket、SSL/TLS など)。                  |
| PID       | 現在の接続のプロセス ID。                                       |
| サーバーバージョン | 接続されている TiDBサーバーの現在のバージョン。                           |
| SSL_バージョン | 現在使用されている SSL のバージョン。                                |
| ホストIP     | 接続されている TiDBサーバーの現在の IP アドレス。                        |
| ホストポート    | 接続されている TiDBサーバーの現在のポート。                             |
| クライアントIP  | クライアントの現在の IP アドレス。                                  |
| クライアントポート | クライアントの現在のポート。                                       |

### 監査操作情報 {#audit-operation-information}

イベント クラスが`AUDIT`または`AUDIT`のサブクラスの場合、監査ログには次の情報が含まれます。

| 分野        | 説明                           |
| --------- | ---------------------------- |
| 監査操作ターゲット | TiDB データベース監査に関連する設定のオブジェクト。 |
| 監査オプション引数 | TiDB データベース監査に関連する設定の引数。     |

## 監査ログの制限 {#audit-logging-limitations}

-   監査ログは現在、 TiDB Cloud CLI 経由でのみ利用可能です。
-   監査ログは現在、 TiDB Cloudにのみ保存できます。
-   TiDB Cloud StarterおよびTiDB Cloud Essentialでは、監査ログの順序は保証されません。そのため、最新のイベントを確認するには、すべてのログファイルを確認する必要がある場合があります。ログを時系列で並べ替えるには、監査ログの`TIME`フィールドを使用できます。
