---
title: ticloud serverless audit-log filter-rule create
summary: ticloud serverless audit-log filter-rule create` のリファレンス。
---

# ticloud サーバーレス監査ログフィルタールールの作成 {#ticloud-serverless-audit-log-filter-rule-create}

TiDB Cloud Essential クラスターの監査ログ フィルター ルールを作成します。

```shell
ticloud serverless audit-log filter-rule create [flags]
```

## 例 {#examples}

対話モードでフィルタ ルールを作成します。

```shell
ticloud serverless audit-log filter-rule create
```

非対話型モードですべての監査ログをキャプチャするためのフィルター ルールを作成します。

```shell
ticloud serverless audit-log filter-rule create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

非対話型モードで、テーブル`test.t` `QUERY`および`EXECUTE`イベントと、すべてのテーブルの`QUERY`イベントをキャプチャするフィルター ルールを作成します。

```shell
ticloud serverless audit-log filter-rule create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY","EXECUTE"],"tables":["test.t"]},{"classes":["QUERY"]}]}'
```

## 旗 {#flags}

| フラグ                  | 説明                                                                                    | 必須  | 注記                                   |
| -------------------- | ------------------------------------------------------------------------------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID。                                                                            | はい  | 非対話型モードでのみ動作します。                     |
| --display-name 文字列   | フィルター ルールの表示名。                                                                        | はい  | 非対話型モードでのみ動作します。                     |
| --ルール文字列             | フィルタールール式。フィルターテンプレートを表示するには`ticloud serverless audit-log filter-rule template`使用します。 | はい  | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                                   | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug       | デバッグ モードを有効にします。          | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |
| --色なし             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile 文字列 | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブ モードと非インタラクティブ モードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
