---
title: ticloud serverless audit-log config
summary: ticloud serverless audit-log config` のリファレンス。
---

# ticloud サーバーレス監査ログ設定 {#ticloud-serverless-audit-log-config}

TiDB Cloud Serverless クラスターのデータベース監査ログを構成します。

```shell
ticloud serverless audit-log config [flags]
```

## 例 {#examples}

対話モードでデータベース監査ログを構成します。

```shell
ticloud serverless audit-log config
```

非対話型モードでデータベース監査ログを有効にします。

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled
```

非対話型モードでデータベース監査ログを無効にします。

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled=false
```

非対話型モードでデータベース監査ログを編集解除します。

```shell
ticloud serverless audit-log config -c <cluster-id> --unredacted
```

## 旗 {#flags}

非対話型モードでは、必要なフラグを手動で入力する必要があります。対話型モードでは、CLIプロンプトに従って入力するだけです。

| フラグ                  | 説明                      | 必須  | 注記                       |
| -------------------- | ----------------------- | --- | ------------------------ |
| -c, --cluster-id 文字列 | クラスターの ID。              | はい  | 非対話型モードでのみ動作します。         |
| --有効                 | データベース監査ログを有効または無効にします。 | いいえ | 非対話型モードでのみ動作します。         |
| --編集なし               | 監査ログのデータ編集を有効または無効にします。 | いいえ | 非対話型モードでのみ動作します。         |
| -h, --help           | このコマンドのヘルプ情報を表示します。     | いいえ | 非対話型モードと対話型モードの両方で動作します。 |

## 継承されたフラグ {#inherited-flags}

| フラグ               | 説明                                                                             | 必須  | 注記                                                      |
| ----------------- | ------------------------------------------------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                                                                 | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用するアクティブ[ユーザープロフィール](/tidb-cloud/cli-reference.md#user-profile)を指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグ モードを有効にします。                                                               | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
