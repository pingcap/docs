---
title: ticloud cluster create
summary: The reference of `ticloud cluster create`.
---

# ticloud クラスタの作成 {#ticloud-cluster-create}

クラスターを作成します。

```shell
ticloud cluster create [flags]
```

> **ノート：**
>
> 現在、上記のコマンドを使用して作成できるクラスターは[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)だけです。

## 例 {#examples}

インタラクティブ モードでクラスターを作成します。

```shell
ticloud cluster create
```

非インタラクティブ モードでクラスターを作成します。

```shell
ticloud cluster create --project-id <project-id> --cluster-name <cluster-name> --cloud-provider <cloud-provider> --region <region> --root-password <password> --cluster-type <cluster-type>
```

## フラグ {#flags}

非対話モードでは、必要なフラグを手動で入力する必要があります。対話モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                   | 説明                                      | 必要  | ノート                                 |
| -------------------- | --------------------------------------- | --- | ----------------------------------- |
| --クラウドプロバイダー文字列      | クラウド プロバイダー (現在、 `AWS`だけがサポートされています)    | はい  | 非対話モードでのみ機能します。                     |
| --cluster-name 文字列   | 作成するクラスターの名前                            | はい  | 非対話モードでのみ機能します。                     |
| --cluster-type 文字列   | クラスタの種類 (現在、 `SERVERLESS`だけがサポートされています) | はい  | 非対話モードでのみ機能します。                     |
| -h, --help           | このコマンドのヘルプ情報を取得する                       | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します |
| -p, --project-id 文字列 | クラスターが作成されるプロジェクトの ID                   | はい  | 非対話モードでのみ機能します。                     |
| -r, --地域文字列          | クラウド リージョン                              | はい  | 非対話モードでのみ機能します。                     |
| --root-パスワード文字列      | クラスタのルート パスワード                          | はい  | 非対話モードでのみ機能します。                     |

## 継承されたフラグ {#inherited-flags}

| 国旗              | 説明                                                                               | 必要  | ノート                                                             |
| --------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                                                                     | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
