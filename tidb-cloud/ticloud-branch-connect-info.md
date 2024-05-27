---
title: ticloud branch connect-info
summary: ticloud branch connect-info のリファレンス。
---

# ticloud ブランチ接続情報 {#ticloud-branch-connect-info}

ブランチの接続文字列を取得します。

```shell
ticloud branch connect-info [flags]
```

## 例 {#examples}

対話モードでブランチの接続文字列を取得します。

```shell
ticloud branch connect-info
```

非対話モードでブランチの接続文字列を取得します。

```shell
ticloud branch connect-info --branch-id <branch-id> --cluster-id <cluster-id> --client <client-name> --operating-system <operating-system>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                  | 説明                                                                                                                                                                                                                                                                                                                                                                                                           | 必須  | 注記                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- | ------------------------ |
| -c, --cluster-id 文字列 | ブランチが作成されるクラスターのID                                                                                                                                                                                                                                                                                                                                                                                           | はい  | 非対話型モードでのみ動作します。         |
| -b, --branch-id 文字列  | ブランチのID                                                                                                                                                                                                                                                                                                                                                                                                      | はい  | 非対話型モードでのみ動作します。         |
| --クライアント文字列          | 接続に使用する目的のクライアント。サポートされているクライアントには、 `general` 、 `mysql_cli` 、 `mycli` 、 `libmysqlclient` 、 `python_mysqlclient` 、 `pymysql` 、 `mysql_connector_python` 、 `mysql_connector_java` 、 `go_mysql_driver` 、 `node_mysql2` 、 `ruby_mysql2` 、 `php_mysqli` 、 `rust_mysql` 、 `mybatis` 、 `hibernate` 、 `spring_boot` 、 `django_tidb` `gorm` `prisma` `sequelize_mysql2` `sqlalchemy_mysqlclient` `active_record`あります。 | はい  | 非対話型モードでのみ動作します。         |
| --オペレーティングシステム文字列    | オペレーティング システム名。サポートされているオペレーティング システムには、 `macOS` 、 `Windows` 、 `Ubuntu` 、 `CentOS` 、 `RedHat` 、 `Fedora` 、 `Debian` 、 `Arch` 、 `OpenSUSE` 、 `Alpine` 、 `Others`があります。                                                                                                                                                                                                                                        | はい  | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報                                                                                                                                                                                                                                                                                                                                                                                                 | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                           |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------------ |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                     |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
