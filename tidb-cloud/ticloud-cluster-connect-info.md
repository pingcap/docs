---
title: ticloud cluster connect-info
summary: The reference of `ticloud cluster connect-info`.
---

# ticloud クラスターの接続情報 {#ticloud-cluster-connect-info}

クラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info [flags]
```

> **注記：**
>
> 現在、このコマンドは[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの接続文字列の取得のみをサポートしています。

## 例 {#examples}

対話型モードでクラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info
```

非対話モードでクラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info --project-id <project-id> --cluster-id <cluster-id> --client <client-name> --operating-system <operating-system>
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                 | 説明                                                                                                                                                                                                                                                                                                                                                     | 必須  | 注記                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- | ------------------------ |
| -p、--プロジェクトID文字列    | クラスターが作成されるプロジェクトの ID                                                                                                                                                                                                                                                                                                                                  | はい  | 非対話モードでのみ動作します。          |
| -c、--cluster-id 文字列 | クラスターのID                                                                                                                                                                                                                                                                                                                                               | はい  | 非対話モードでのみ動作します。          |
| --クライアント文字列         | 接続に使用される目的のクライアント。 `go_mysql_driver` `php_mysqli` `rust_mysql` `spring_boot` `mysql_cli` `pymysql` `mysql_connector_python` `general` `hibernate` `mybatis` `ruby_mysql2` `mycli` `mysql_connector_java` `libmysqlclient` `python_mysqlclient` `node_mysql2` `gorm` `prisma` `sequelize_mysql2` `django_tidb` `sqlalchemy_mysqlclient` `active_record` | はい  | 非対話モードでのみ動作します。          |
| --オペレーティング システム文字列  | オペレーティング システム名。サポートされているオペレーティング システムには、 `macOS` 、 `Windows` 、 `Ubuntu` 、 `CentOS` 、 `RedHat` 、 `Fedora` 、 `Debian` 、 `Arch` 、 `OpenSUSE` 、 `Alpine` 、および`Others`が含まれます。                                                                                                                                                                               | はい  | 非対話モードでのみ動作します。          |
| -h, --help          | このコマンドのヘルプ情報                                                                                                                                                                                                                                                                                                                                           | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                               | 必須  | 注記                                                                 |
| -------------- | -------------------------------------------------------------------------------- | --- | ------------------------------------------------------------------ |
| --色なし          | 出力のカラーを無効にします。                                                                   | いいえ | 非対話型モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                           |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
