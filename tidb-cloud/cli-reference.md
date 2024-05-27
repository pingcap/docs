---
title: TiDB Cloud CLI Reference
summary: TiDB Cloud CLI の概要を説明します。
---

# TiDB CloudCLI リファレンス {#tidb-cloud-cli-reference}

TiDB Cloud CLI は、数行のコマンドでターミナルからTiDB Cloudを操作できるコマンドライン インターフェイスです。TiDB TiDB Cloud CLI では、 TiDB Cloudクラスターを簡単に管理したり、クラスターにデータをインポートしたり、その他の操作を実行したりできます。

## あなたが始める前に {#before-you-begin}

最初に[TiDB Cloud CLI環境を設定する](/tidb-cloud/get-started-with-cli.md)実行してください。3 CLI `ticloud`インストールしたら、それを使用してコマンド ラインからTiDB Cloudクラスターを管理できます。

## 利用可能なコマンド {#commands-available}

次の表に、TiDB Cloud CLI で使用できるコマンドを示します。

ターミナルで`ticloud` CLI を使用するには、 `ticloud [command] [subcommand]`実行します。 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview)使用している場合は、代わりに`tiup cloud [command] [subcommand]`使用します。

| 指示     | サブコマンド                          | 説明                                                                                              |
| ------ | ------------------------------- | ----------------------------------------------------------------------------------------------- |
| 集まる    | 作成、削除、説明、一覧表示、接続情報              | クラスターを管理する                                                                                      |
| 支店     | 作成、削除、説明、一覧表示、接続情報              | ブランチの管理                                                                                         |
| 完了     | bash、フィッシュ、パワーシェル、zsh           | 指定されたシェルの完了スクリプトを生成する                                                                           |
| 設定     | 作成、削除、説明、編集、リスト、設定、使用           | ユーザープロファイルを構成する                                                                                 |
| 接続する   | <li></li>                       | TiDBクラスターに接続する                                                                                  |
| ヘルプ    | クラスター、完了、構成、ヘルプ、インポート、プロジェクト、更新 | 任意のコマンドのヘルプをビュー                                                                                 |
| 輸入     | キャンセル、説明、リスト、開始                 | [輸入](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)タスクを管理する |
| プロジェクト | リスト                             | プロジェクトの管理                                                                                       |
| アップデート | <li></li>                       | CLIを最新バージョンに更新する                                                                                |

## コマンドモード {#command-modes}

TiDB Cloud CLI では、簡単に使用できるように、一部のコマンドに 2 つのモードが用意されています。

-   インタラクティブモード

    フラグなしでコマンドを実行すると ( `ticloud config create`など)、CLI によって入力が求められます。

-   非対話モード

    コマンドを実行するときに必要なすべての引数とフラグ (例: `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`を指定する必要があります。

## ユーザープロフィール {#user-profile}

TiDB Cloud CLI の場合、ユーザー プロファイルは、プロファイル名、公開キー、秘密キーなど、ユーザーに関連付けられたプロパティのコレクションです。TiDB TiDB Cloud CLI を使用するには、まずユーザー プロファイルを作成する必要があります。

### ユーザープロフィールを作成する {#create-a-user-profile}

[`ticloud config create`](/tidb-cloud/ticloud-config-create.md)使用してユーザー プロファイルを作成します。

### すべてのユーザープロファイルを一覧表示する {#list-all-user-profiles}

すべてのユーザー プロファイルを一覧表示するには[`ticloud config list`](/tidb-cloud/ticloud-config-list.md)使用します。

出力例は次のとおりです。

    Profile Name
    default (active)
    dev
    staging

この出力例では、ユーザー プロファイル`default`が現在アクティブです。

### ユーザープロフィールを説明する {#describe-a-user-profile}

ユーザー プロファイルのプロパティを取得するには[`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md)使用します。

出力例は次のとおりです。

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### ユーザープロファイルのプロパティを設定する {#set-properties-in-a-user-profile}

ユーザー プロファイルのプロパティを設定するには[`ticloud config set`](/tidb-cloud/ticloud-config-set.md)使用します。

### 別のユーザープロファイルに切り替える {#switch-to-another-user-profile}

別のユーザー プロファイルに切り替えるには[`ticloud config use`](/tidb-cloud/ticloud-config-use.md)使用します。

出力例は次のとおりです。

    Current profile has been changed to default

### 設定ファイルを編集する {#edit-the-config-file}

[`ticloud config edit`](/tidb-cloud/ticloud-config-edit.md)使用して設定ファイルを編集用に開きます。

### ユーザープロファイルを削除する {#delete-a-user-profile}

ユーザー プロファイルを削除するには[`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md)使用します。

## グローバルフラグ {#global-flags}

次の表は、 TiDB Cloud CLI のグローバル フラグを示しています。

| フラグ               | 説明                                   | 必須  | 注記                                                             |
| ----------------- | ------------------------------------ | --- | -------------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                       | いいえ | 非対話型モードでのみ機能します。対話型モードでは、一部の UI コンポーネントで色を無効にしても機能しない可能性があります。 |
| -P, --profile 文字列 | このコマンドで使用されるアクティブなユーザー プロファイルを指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                       |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、あらゆる貢献を歓迎します。
