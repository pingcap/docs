---
title: ticloud import describe
summary: The reference of `ticloud import describe`.
---

# ticloud インポートの説明 {#ticloud-import-describe}

データ インポート タスクのインポートの詳細を取得します。

```shell
ticloud import describe [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud import get [flags]
```

## 例 {#examples}

インタラクティブ モードでインポート タスクを記述します。

```shell
ticloud import describe
```

非対話モードでのインポート タスクを説明します。

```shell
ticloud import describe --project-id <project-id> --cluster-id <cluster-id> --import-id <import-id>
```

## フラグ {#flags}

非対話モードでは、必要なフラグを手動で入力する必要があります。対話モードでは、CLI プロンプトに従って入力するだけです。

| 国旗                   | 説明            | 必要  | ノート                                  |
| -------------------- | ------------- | --- | ------------------------------------ |
| -c, --cluster-id 文字列 | クラスタID        | はい  | 非対話モードでのみ機能します。                      |
| -h, --help           | このコマンドのヘルプ情報  | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。 |
| --インポート ID 文字列       | インポート タスクの ID | はい  | 非対話モードでのみ機能します。                      |
| -p, --project-id 文字列 | プロジェクト ID     | はい  | 非対話モードでのみ機能します。                      |

## 継承されたフラグ {#inherited-flags}

| 国旗              | 説明                                                                               | 必要  | ノート                                                             |
| --------------- | -------------------------------------------------------------------------------- | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                                                                     | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブ[ユーザー プロファイル](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
