---
title: ticloud cluster describe
summary: The reference of `ticloud cluster describe`.
---

# ticloud クラスタの説明 {#ticloud-cluster-describe}

クラスターに関する情報 (クラウド プロバイダー、クラスターの種類、クラスター構成、クラスターの状態など) を取得します。

```shell
ticloud cluster describe [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud cluster get [flags]
```

## 例 {#examples}

対話モードでクラスター情報を取得します。

```shell
ticloud cluster describe
```

非対話モードでクラスター情報を取得します。

```shell
ticloud cluster describe --project-id <project-id> --cluster-id <cluster-id>
```

## フラグ {#flags}

非対話モードでは、必要なフラグを手動で入力する必要があります。対話モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                   | 説明              | 必要  | ノート                                  |
| -------------------- | --------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID       | はい  | 非対話モードでのみ機能します。                      |
| -h, --help           | このコマンドのヘルプ情報    | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。 |
| -p, --project-id 文字列 | クラスターのプロジェクト ID | はい  | 非対話モードでのみ機能します。                      |

## 継承されたフラグ {#inherited-flags}

| 国旗              | 説明                                                                               | 必要  | ノート                                                             |
| --------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                                                                     | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
