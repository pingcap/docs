---
title: ticloud serverless authorized-network create
summary: ticloud serverless authorized-network create` のリファレンス。
---

# ticloud サーバーレス 承認済みネットワークの作成 {#ticloud-serverless-authorized-network-create}

承認済みネットワークを作成します。

```shell
ticloud serverless authorized-network create [flags]
```

## 例 {#examples}

対話モードで承認済みネットワークを作成します。

```shell
ticloud serverless authorized-network create
```

非対話型モードで承認済みネットワークを作成します。

```shell
ticloud serverless authorized-network create -c <cluster-id> --display-name <display-name> --start-ip-address <start-ip-address> --end-ip-address <end-ip-address>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                    | 説明                            | 必須  | 注記                       |
| ---------------------- | ----------------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列   | クラスターの ID を指定します。             | はい  | 非対話型モードでのみ動作します。         |
| --display-name 文字列     | 承認されたネットワークの名前を指定します。         | はい  | 非対話型モードでのみ動作します。         |
| --start-ip-address 文字列 | 承認されたネットワークの開始 IP アドレスを指定します。 | はい  | 非対話型モードでのみ動作します。         |
| --end-ip-address 文字列   | 承認されたネットワークの終了 IP アドレスを指定します。 | はい  | 非対話型モードでのみ動作します。         |
| -h, --help             | このコマンドのヘルプ情報を表示します。           | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
