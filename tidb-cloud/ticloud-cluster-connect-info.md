---
title: ticloud cluster connect-info
summary: ticloud cluster connect-info のリファレンス。
---

# ticloud クラスター接続情報 {#ticloud-cluster-connect-info}

クラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info [flags]
```

> **注記：**
>
> 現在、このコマンドは[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの接続文字列の取得のみをサポートしています。

## 例 {#examples}

対話モードでクラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info
```

非対話型モードでクラスターの接続文字列を取得します。

```shell
ticloud cluster connect-info --project-id <project-id> --cluster-id <cluster-id> --client <client-name> --operating-system <operating-system>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従ってフラグを入力するだけです。

| フラグ                  | 説明                                                                                                                                                                                                                                                                                                                                                                                                           | 必須  | 注記                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- | ------------------------ |
| -p, --プロジェクトID 文字列   | クラスターが作成されるプロジェクトのID                                                                                                                                                                                                                                                                                                                                                                                         | はい  | 非対話型モードでのみ動作します。         |
| -c, --cluster-id 文字列 | クラスターのID                                                                                                                                                                                                                                                                                                                                                                                                     | はい  | 非対話型モードでのみ動作します。         |
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
