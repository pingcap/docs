---
title: ticloud cluster delete
summary: ticloud クラスターを削除する方法について説明します。対話モードでは、"ticloud cluster delete" コマンドを使用し、非対話モードでは、"ticloud cluster delete --project-id <project-id> --cluster-id <cluster-id>" コマンドを使用します。削除するクラスターのIDとプロジェクトIDが必要です。確認なしでクラスターを削除するには、"--force" フラグを使用します。質問や提案がある場合は、TiDB Cloud CLI の問題を作成してください。
---

# ticloud クラスターの削除 {#ticloud-cluster-delete}

プロジェクトからクラスターを削除します。

```shell
ticloud cluster delete [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud cluster rm [flags]
```

## 例 {#examples}

対話モードでクラスターを削除します。

```shell
ticloud cluster delete
```

非対話モードでクラスターを削除します。

```shell
ticloud cluster delete --project-id <project-id> --cluster-id <cluster-id>
```

## フラグ {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                 | 説明                 | 必須  | 注記                       |
| ------------------- | ------------------ | --- | ------------------------ |
| -c、--cluster-id 文字列 | 削除するクラスターのID       | はい  | 非対話モードでのみ動作します。          |
|  --force            | 確認なしでクラスターを削除します   | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| -h, --help          | このコマンドのヘルプ情報       | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| -p、--プロジェクトID文字列    | 削除するクラスターのプロジェクトID | はい  | 非対話モードでのみ動作します。          |

## 継承されたフラグ {#inherited-flags}

| フラグ            | 説明                                                                          | 必須  | 注記                                                                |
| -------------- | --------------------------------------------------------------------------- | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                                                              | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブな[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile) 。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
