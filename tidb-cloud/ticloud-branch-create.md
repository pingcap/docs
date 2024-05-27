---
title: ticloud branch create
summary: ticloud branch create のリファレンス。
---

# ticloud ブランチ作成 {#ticloud-branch-create}

クラスターのブランチを作成します。

```shell
ticloud branch create [flags]
```

> **注記：**
>
> 現在、 [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターに対してのみブランチを作成できます。

## 例 {#examples}

対話モードでブランチを作成します。

```shell
ticloud branch create
```

非対話モードでブランチを作成します。

```shell
ticloud branch create --cluster-id <cluster-id> --branch-name <branch-name>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                  | 説明                 | 必須  | 注記                                |
| -------------------- | ------------------ | --- | --------------------------------- |
| -c, --cluster-id 文字列 | ブランチが作成されるクラスターのID | はい  | 非対話型モードでのみ動作します。                  |
| --ブランチ名文字列           | 作成するブランチの名前        | はい  | 非対話型モードでのみ動作します。                  |
| -h, --help           | このコマンドのヘルプ情報を取得する  | いいえ | 非インタラクティブモードとインタラクティブモードの両方で動作します |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
