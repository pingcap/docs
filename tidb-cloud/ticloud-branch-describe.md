---
title: ticloud branch describe
summary: ticloud branch describe のリファレンス。
---

# ticloudブランチの説明 {#ticloud-branch-describe}

ブランチに関する情報 (エンドポイント、 [ユーザー名プレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix) 、使用状況など) を取得します。

```shell
ticloud branch describe [flags]
```

または、次のエイリアス コマンドを使用します。

```shell
ticloud branch get [flags]
```

## 例 {#examples}

対話モードでブランチ情報を取得します。

```shell
ticloud branch describe
```

非対話モードでブランチ情報を取得します。

```shell
ticloud branch describe --branch-id <branch-id> --cluster-id <cluster-id>
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLI プロンプトに従って入力するだけです。

| フラグ                  | 説明           | 必須  | 注記                       |
| -------------------- | ------------ | --- | ------------------------ |
| -b, --branch-id 文字列  | ブランチのID      | はい  | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報 | いいえ | 非対話型モードと対話型モードの両方で動作します。 |
| -c, --cluster-id 文字列 | ブランチのクラスタID  | はい  | 非対話型モードでのみ動作します。         |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                             |
| ----------------- | ------------------------------------------------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
