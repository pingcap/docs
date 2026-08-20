---
title: ticloud serverless audit-log filter-rule create
summary: ticloud serverless audit-log filter-rule create` のリファレンス。
---

# ticloud serverless audit-log filter-rule create {#ticloud-serverless-audit-log-filter-rule-create}

TiDB Cloud Essential クラスターの監査ログフィルタールールを作成します。

```shell
ticloud serverless audit-log filter-rule create [flags]
```

## 例 {#examples}

対話モードでフィルタルールを作成します。

```shell
ticloud serverless audit-log filter-rule create
```

非対話型モードですべての監査ログをキャプチャするためのフィルタールールを作成します。

```shell
ticloud serverless audit-log filter-rule create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

非対話型モードで、テーブル`test.t` `QUERY`および`EXECUTE`イベントと、すべてのテーブルの`QUERY`イベントをキャプチャするフィルタールールを作成します。

```shell
ticloud serverless audit-log filter-rule create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY","EXECUTE"],"tables":["test.t"]},{"classes":["QUERY"]}]}'
```

## フラグ {#flags}

| フラグ                  | 説明                                                                                    | 必須  | 注記                                   |
| -------------------- | ------------------------------------------------------------------------------------- | --- | ------------------------------------ |
| -c, --cluster-id string | クラスターの ID。                                                                            | はい  | 非対話型モードでのみ動作します。                     |
| --display-name string   | フィルタールールの表示名。                                                                        | はい  | 非対話型モードでのみ動作します。                     |
| --rule string             | フィルタールール式。フィルターテンプレートを表示するには`ticloud serverless audit-log filter-rule template`を使用します。 | はい  | 非対話型モードでのみ動作します。                     |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                                   | いいえ | インタラクティブモードと非インタラクティブモードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                        | 必須  | 注記                                   |
| ----------------- | ------------------------- | --- | ------------------------------------ |
| -D, --debug       | デバッグ モードを有効にします。          | いいえ | インタラクティブモードと非インタラクティブモードの両方で動作します。 |
| --no-color             | カラー出力を無効にします。             | いいえ | 非対話型モードでのみ動作します。                     |
| -P, --profile string | 構成ファイルから使用するプロファイルを指定します。 | いいえ | インタラクティブモードと非インタラクティブモードの両方で動作します。 |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、皆様からの貢献も歓迎いたします。
