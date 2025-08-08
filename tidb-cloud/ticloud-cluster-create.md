---
title: ticloud serverless create
summary: ticloud serverless create` のリファレンス。
---

# ticloud サーバーレス作成 {#ticloud-serverless-create}

TiDB Cloud Serverless クラスターを作成します。

```shell
ticloud serverless create [flags]
```

## 例 {#examples}

インタラクティブ モードでTiDB Cloud Serverless クラスターを作成します。

```shell
ticloud serverless create
```

非対話型モードでTiDB Cloud Serverless クラスターを作成します。

```shell
ticloud serverless create --display-name <display-name> --region <region>
```

非対話型モードで支出制限付きのTiDB Cloud Serverless クラスターを作成します。

```shell
ticloud serverless create --display-name <display-name> --region <region> --spending-limit-monthly <spending-limit-monthly>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                                                                  | 必須  | 注記                      |
| -------------------- | ------------------------------------------------------------------- | --- | ----------------------- |
| -n --表示名文字列          | 作成するクラスターの名前を指定します。                                                 | はい  | 非対話型モードでのみ動作します。        |
| --支出限度額-月間 int       | 月間最大支出限度額を USD セント単位で指定します。                                         | いいえ | 非対話型モードでのみ動作します。        |
| -p, --project-id 文字列 | クラスターが作成されるプロジェクトのIDを指定します。デフォルト値は`default project`です。              | いいえ | 非対話型モードでのみ動作します。        |
| -r, --region 文字列     | クラウドリージョン名を指定します。「ticloud serverlessregion」と入力すると、すべてのリージョンが表示されます。 | はい  | 非対話型モードでのみ動作します。        |
| --パブリックエンドポイントを無効にする | パブリックエンドポイントを無効にします。                                                | いいえ | 非対話型モードでのみ動作します。        |
| --暗号化                | 保存時の強化された暗号化を有効にします。                                                | いいえ | 非対話型モードでのみ動作します。        |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                 | いいえ | 非対話型モードと対話型モードの両方で動作します |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
