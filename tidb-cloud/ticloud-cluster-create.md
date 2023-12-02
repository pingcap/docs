---
title: ticloud cluster create
summary: The reference of `ticloud cluster create`.
---

# ticloud クラスターの作成 {#ticloud-cluster-create}

クラスターを作成します。

```shell
ticloud cluster create [flags]
```

> **注記：**
>
> 現在、前述のコマンドを使用して作成できるクラスターは[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)だけです。

## 例 {#examples}

対話モードでクラスターを作成します。

```shell
ticloud cluster create
```

非対話モードでクラスターを作成します。

```shell
ticloud cluster create --project-id <project-id> --cluster-name <cluster-name> --cloud-provider <cloud-provider> --region <region> --root-password <password> --cluster-type <cluster-type>
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ              | 説明                                     | 必須  | 注記                      |
| ---------------- | -------------------------------------- | --- | ----------------------- |
| --クラウドプロバイダー文字列  | クラウドプロバイダー (現在サポートされているのは`AWS`だけです)    | はい  | 非対話モードでのみ動作します。         |
| --クラスタ名文字列       | 作成するクラスターの名前                           | はい  | 非対話モードでのみ動作します。         |
| --クラスタタイプ文字列     | クラスタの種類 (現在は`SERVERLESS`のみがサポートされています) | はい  | 非対話モードでのみ動作します。         |
| -h, --help       | このコマンドのヘルプ情報を取得する                      | いいえ | 非対話型モードと対話型モードの両方で動作します |
| -p、--プロジェクトID文字列 | クラスターが作成されるプロジェクトの ID                  | はい  | 非対話モードでのみ動作します。         |
| -r、--地域文字列       | クラウド領域                                 | はい  | 非対話モードでのみ動作します。         |
| --root パスワード文字列  | クラスターの root パスワード                      | はい  | 非対話モードでのみ動作します。         |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                               | 必須  | 注記                                                                |
| -------------- | -------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                                   | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
