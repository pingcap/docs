---
title: ticloud serverless create
summary: "`ticloud serverless create` のリファレンス。"
---

# ticloud serverless create {#ticloud-serverless-create}

TiDB Cloud Starter またはEssential インスタンスを作成します。

```shell
ticloud serverless create [flags]
```

## 例 {#examples}

対話モードでTiDB Cloud Starter またはEssential インスタンスを作成します。

```shell
ticloud serverless create
```

非対話型モードでTiDB Cloud Starter またはEssential インスタンスを作成します。

```shell
ticloud serverless create --display-name <display-name> --region <region>
```

非対話型モードで支出限度額付きのTiDB Cloud Starter インスタンスを作成します。

```shell
ticloud serverless create --display-name <display-name> --region <region> --spending-limit-monthly <spending-limit-monthly>
```

非対話型モードでTiDB Cloud Essential インスタンスを作成します。

```shell
ticloud serverless create --display-name <display-name> --region <region> --max-rcu <maximum-rcu> --min-rcu <minimum-rcu>
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                                                                                                   | 必須  | 注記                      |
| -------------------- | ---------------------------------------------------------------------------------------------------- | --- | ----------------------- |
| -n, --display-name string  | 作成するTiDB Cloud Starter またはEssential インスタンスの名前を指定します。                                                                                  | はい  | 非対話型モードでのみ動作します。        |
| --spending-limit-monthly int       | 月間最大支出限度額を USD セント単位で指定します。                                                                          | いいえ | 非対話型モードでのみ動作します。        |
| -p, --project-id string | TiDB Cloud Starter またはEssential インスタンスが作成されるプロジェクトのIDを指定します。デフォルト値は`default project`です。                                               | いいえ | 非対話型モードでのみ動作します。        |
| -r, --region string     | クラウドリージョンの名前を指定します。 `ticloud serverless region`コマンドを使用すると、利用可能なすべてのリージョンを表示できます。                     | はい  | 非対話型モードでのみ動作します。        |
| --disable-public-endpoint | パブリックエンドポイントを無効にします。TiDB Cloud Starter またはEssential インスタンスへのパブリックアクセスを禁止する場合は、このオプションを使用します。                                          | いいえ | 非対話型モードでのみ動作します。        |
| --encryption                | 二重層データ暗号化を有効にします。TiDB Cloud Essential インスタンスではデフォルトで有効、 TiDB Cloud Starter インスタンスではデフォルトで無効になっています。 | いいえ | 非対話型モードでのみ動作します。        |
| --max-rcu int32      | TiDB Cloud Essential インスタンスの最大リクエストキャパシティユニット (RCU) を 100000 まで設定します。                                       | いいえ | 非対話型モードでのみ動作します。        |
| --min-rcu int32      | TiDB Cloud Essential インスタンスの最小リクエストキャパシティユニット (RCU) を少なくとも 2000 に設定します。                                     | いいえ | 非対話型モードでのみ動作します。        |
| -h, --help           | このコマンドのヘルプ情報を表示します。                                                                                  | いいえ | 非対話型モードと対話型モードの両方で動作します |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --no-color             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile string | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグモードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[Issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、皆様からの貢献も歓迎いたします。
