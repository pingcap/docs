---
title: ticloud import describe
summary: ticloud import describe のリファレンス。
---

# ticloud インポート 説明 {#ticloud-import-describe}

データ インポート タスクのインポート詳細を取得します。

```shell
ticloud import describe [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud import get [flags]
```

## 例 {#examples}

インタラクティブ モードでインポート タスクを説明します。

```shell
ticloud import describe
```

非対話型モードでのインポート タスクについて説明します。

```shell
ticloud import describe --project-id <project-id> --cluster-id <cluster-id> --import-id <import-id>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                  | 説明           | 必須  | 注記                       |
| -------------------- | ------------ | --- | ------------------------ |
| -c, --cluster-id 文字列 | クラスタID       | はい  | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報 | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| --import-id 文字列      | インポートタスクのID  | はい  | 非対話型モードでのみ動作します。         |
| -p, --プロジェクトID 文字列   | プロジェクトID     | はい  | 非対話型モードでのみ動作します。         |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                           |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------------ |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                     |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
