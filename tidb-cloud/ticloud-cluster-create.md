---
title: ticloud cluster create
summary: ticloud cluster create のリファレンス。
---

# ticloud クラスター作成 {#ticloud-cluster-create}

クラスターを作成します。

```shell
ticloud cluster create [flags]
```

> **注記：**
>
> 現在、上記のコマンドを使用して作成できるクラスターは[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)だけです。

## 例 {#examples}

対話モードでクラスターを作成します。

```shell
ticloud cluster create
```

非対話型モードでクラスターを作成します。

```shell
ticloud cluster create --project-id <project-id> --cluster-name <cluster-name> --cloud-provider <cloud-provider> --region <region> --root-password <password> --cluster-type <cluster-type>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                | 説明                                     | 必須  | 注記                                |
| ------------------ | -------------------------------------- | --- | --------------------------------- |
| --クラウドプロバイダー文字列    | クラウド プロバイダー (現在サポートされているのは`AWS`だけです)   | はい  | 非対話型モードでのみ動作します。                  |
| --cluster-name 文字列 | 作成するクラスターの名前                           | はい  | 非対話型モードでのみ動作します。                  |
| --cluster-type 文字列 | クラスタタイプ（現在、 `SERVERLESS`のみがサポートされています） | はい  | 非対話型モードでのみ動作します。                  |
| -h, --help         | このコマンドのヘルプ情報を取得する                      | いいえ | 非インタラクティブモードとインタラクティブモードの両方で動作します |
| -p, --プロジェクトID 文字列 | クラスターが作成されるプロジェクトのID                   | はい  | 非対話型モードでのみ動作します。                  |
| -r, --region 文字列   | クラウド領域                                 | はい  | 非対話型モードでのみ動作します。                  |
| --root-パスワード文字列    | クラスターのルートパスワード                         | はい  | 非対話型モードでのみ動作します。                  |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
