---
title: ticloud cluster connect-info
summary: The reference of `ticloud cluster connect-info`.
---

# ticloud クラスター接続情報 {#ticloud-cluster-connect-info}

クラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info [flags]
```

## 例 {#examples}

対話モードでクラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info
```

非対話モードでクラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info --project-id <project-id> --cluster-id <cluster-id> --client <client-name> --operating-system <operating-system>
```

## フラグ {#flags}

非対話モードでは、必要なフラグを手動で入力する必要があります。対話モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                   | 説明                                                                                                                                                                                                                                                                                                                                                     | 必要  | ノート                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- | ------------------------------------ |
| -p, --project-id 文字列 | クラスターが作成されるプロジェクトの ID                                                                                                                                                                                                                                                                                                                                  | はい  | 非対話モードでのみ機能します。                      |
| -c, --cluster-id 文字列 | クラスターの ID                                                                                                                                                                                                                                                                                                                                              | はい  | 非対話モードでのみ機能します。                      |
| --クライアント文字列          | 接続に使用される目的のクライアント。 `mybatis` `hibernate` `ruby_mysql2` `php_mysqli` `rust_mysql` `prisma` `pymysql` `mysql_cli` `mysql_connector_python` `general` `gorm` `mysql_connector_java` `spring_boot` `libmysqlclient` `go_mysql_driver` `mycli` `python_mysqlclient` `node_mysql2` `sequelize_mysql2` `django_tidb` `sqlalchemy_mysqlclient` `active_record` | はい  | 非対話モードでのみ機能します。                      |
| --オペレーティング システム文字列   | オペレーティング システム名。サポートされているオペレーティング システムには、 `macOS` 、 `Windows` 、 `Ubuntu` 、 `CentOS` 、 `RedHat` 、 `Fedora` 、 `Debian` 、 `Arch` 、 `OpenSUSE` 、 `Alpine` 、および`Others`が含まれます。                                                                                                                                                                               | はい  | 非対話モードでのみ機能します。                      |
| -h, --help           | このコマンドのヘルプ情報                                                                                                                                                                                                                                                                                                                                           | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| 国旗              | 説明                                                                               | 必要  | ノート                                                             |
| --------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                                                                     | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
