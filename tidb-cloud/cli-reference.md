---
title: TiDB Cloud CLI Reference
summary: Provides an overview of TiDB Cloud CLI.
---

# TiDB CloudCLI リファレンス {#tidb-cloud-cli-reference}

TiDB Cloud CLI はコマンド ライン インターフェイスであり、数行のコマンドで端末からTiDB Cloudを操作できます。 TiDB Cloud CLI では、 TiDB Cloudクラスターの管理、クラスターへのデータのインポート、およびその他の操作の実行を簡単に行うことができます。

## あなたが始める前に {#before-you-begin}

最初に[TiDB Cloud CLI 環境をセットアップする](/tidb-cloud/get-started-with-cli.md)を確認してください。 `ticloud` CLI をインストールしたら、それを使用して、コマンド ラインからTiDB Cloudクラスターを管理できます。

## 利用可能なコマンド {#commands-available}

次の表に、 TiDB Cloud CLI で使用できるコマンドを示します。

端末で`ticloud` CLI を使用するには、 `ticloud [command] [subcommand]`を実行します。 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview)使用している場合は、代わりに`tiup cloud [command] [subcommand]`を使用してください。

| 指図     | サブコマンド                          | 説明                                                                                                |
| ------ | ------------------------------- | ------------------------------------------------------------------------------------------------- |
| 集まる    | 作成、削除、記述、一覧表示、接続情報              | クラスターを管理する                                                                                        |
| 完了     | バッシュ、フィッシュ、パワーシェル、zsh           | 指定されたシェルの完了スクリプトを生成する                                                                             |
| 構成     | 作成、削除、記述、編集、リスト、設定、使用           | ユーザー プロファイルの構成                                                                                    |
| 接続     | <li></li>                       | TiDB クラスターに接続する                                                                                   |
| ヘルプ    | クラスター、完了、構成、ヘルプ、インポート、プロジェクト、更新 | コマンドのヘルプをビュー                                                                                      |
| 輸入     | キャンセル、説明、リスト、開始                 | [輸入](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)件のタスクを管理する |
| 計画     | リスト                             | プロジェクトの管理                                                                                         |
| アップデート | <li></li>                       | CLI を最新バージョンに更新する                                                                                 |

## コマンドモード {#command-modes}

TiDB Cloud CLI は、簡単に使用できるように、いくつかのコマンドに 2 つのモードを提供します。

-   インタラクティブモード

    フラグなしでコマンド ( `ticloud config create`など) を実行すると、CLI から入力を求めるプロンプトが表示されます。

-   非対話モード

    `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`など、コマンドの実行時に必要なすべての引数とフラグを指定する必要があります。

## ユーザープロフィール {#user-profile}

TiDB Cloud CLI の場合、ユーザー プロファイルは、プロファイル名、公開鍵、秘密鍵など、ユーザーに関連付けられたプロパティのコレクションです。 TiDB Cloud CLI を使用するには、最初にユーザー プロファイルを作成する必要があります。

### ユーザー プロファイルを作成する {#create-a-user-profile}

[`ticloud config create`](/tidb-cloud/ticloud-config-create.md)を使用して、ユーザー プロファイルを作成します。

### すべてのユーザー プロファイルを一覧表示する {#list-all-user-profiles}

すべてのユーザー プロファイルを一覧表示するには、 [`ticloud config list`](/tidb-cloud/ticloud-config-list.md)を使用します。

出力例は次のとおりです。

```
Profile Name
default (active)
dev
staging
```

この出力例では、ユーザー プロファイル`default`が現在アクティブです。

### ユーザー プロファイルの説明 {#describe-a-user-profile}

ユーザー プロファイルのプロパティを取得するには、 [`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md)を使用します。

出力例は次のとおりです。

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### ユーザー プロファイルでプロパティを設定する {#set-properties-in-a-user-profile}

ユーザー プロファイルのプロパティを設定するには、 [`ticloud config set`](/tidb-cloud/ticloud-config-set.md)を使用します。

### 別のユーザー プロファイルに切り替える {#switch-to-another-user-profile}

別のユーザー プロファイルに切り替えるには、 [`ticloud config use`](/tidb-cloud/ticloud-config-use.md)を使用します。

出力例は次のとおりです。

```
Current profile has been changed to default
```

### 設定ファイルを編集する {#edit-the-config-file}

[`ticloud config edit`](/tidb-cloud/ticloud-config-edit.md)を使用して、構成ファイルを編集用に開きます。

### ユーザー プロファイルを削除する {#delete-a-user-profile}

ユーザー プロファイルを削除するには、 [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md)を使用します。

## グローバル フラグ {#global-flags}

次の表に、 TiDB Cloud CLI のグローバル フラグを示します。

| 国旗              | 説明                                   | 必要  | ノート                                                             |
| --------------- | ------------------------------------ | --- | --------------------------------------------------------------- |
| --無色            | 出力の色を無効にします。                         | いいえ | 非対話モードでのみ機能します。インタラクティブ モードでは、一部の UI コンポーネントでは色を無効にできない場合があります。 |
| -P, --プロファイル文字列 | このコマンドで使用されるアクティブなユーザー プロファイルを指定します。 | いいえ | 非インタラクティブ モードとインタラクティブ モードの両方で動作します。                            |

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
