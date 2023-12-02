---
title: TiDB Cloud CLI Reference
summary: Provides an overview of TiDB Cloud CLI.
---

# TiDB CloudCLI リファレンス {#tidb-cloud-cli-reference}

TiDB Cloud CLI はコマンド ライン インターフェイスであり、数行のコマンドで端末からTiDB Cloudを操作できるようになります。 TiDB Cloud CLI では、 TiDB Cloudクラスターの管理、クラスターへのデータのインポート、その他の操作の実行が簡単に行えます。

## あなたが始める前に {#before-you-begin}

必ず最初に[TiDB Cloud CLI 環境をセットアップする](/tidb-cloud/get-started-with-cli.md)を行ってください。 `ticloud` CLI をインストールすると、それを使用してコマンド ラインからTiDB Cloudクラスターを管理できるようになります。

## 利用可能なコマンド {#commands-available}

次の表に、 TiDB Cloud CLI で使用できるコマンドを示します。

ターミナルで`ticloud` CLI を使用するには、 `ticloud [command] [subcommand]`を実行します。 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview)使用している場合は、代わりに`tiup cloud [command] [subcommand]`を使用してください。

| 指示     | サブコマンド                          | 説明                                                                                              |
| ------ | ------------------------------- | ----------------------------------------------------------------------------------------------- |
| 集まる    | 作成、削除、説明、リスト、接続情報               | クラスターの管理                                                                                        |
| 支店     | 作成、削除、説明、リスト、接続情報               | ブランチの管理                                                                                         |
| 完了     | バッシュ、フィッシュ、パワーシェル、zsh           | 指定されたシェルの完了スクリプトを生成します                                                                          |
| 構成     | 作成、削除、説明、編集、リスト、設定、使用           | ユーザープロファイルを構成する                                                                                 |
| 接続する   | <li></li>                       | TiDB クラスターに接続する                                                                                 |
| ヘルプ    | クラスター、完了、構成、ヘルプ、インポート、プロジェクト、更新 | 任意のコマンドのヘルプをビュー                                                                                 |
| 輸入     | キャンセル、説明、リスト、開始                 | [輸入](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)タスクを管理する |
| プロジェクト | リスト                             | プロジェクトを管理する                                                                                     |
| アップデート | <li></li>                       | CLIを最新バージョンに更新します                                                                               |

## コマンドモード {#command-modes}

TiDB Cloud CLI は、簡単に使用できるようにいくつかのコマンドに対して 2 つのモードを提供します。

-   インタラクティブモード

    フラグ ( `ticloud config create`など) を指定せずにコマンドを実行すると、CLI によって入力を求めるプロンプトが表示されます。

-   非対話型モード

    コマンドの実行時に必要なすべての引数とフラグ`ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`など) を指定する必要があります。

## ユーザープロフィール {#user-profile}

TiDB Cloud CLI の場合、ユーザー プロファイルは、プロファイル名、公開キー、秘密キーなど、ユーザーに関連付けられたプロパティのコレクションです。 TiDB Cloud CLI を使用するには、最初にユーザー プロファイルを作成する必要があります。

### ユーザープロファイルを作成する {#create-a-user-profile}

ユーザー プロファイルを作成するには[`ticloud config create`](/tidb-cloud/ticloud-config-create.md)を使用します。

### すべてのユーザープロファイルをリストする {#list-all-user-profiles}

すべてのユーザー プロファイルをリストするには[`ticloud config list`](/tidb-cloud/ticloud-config-list.md)を使用します。

出力例は次のとおりです。

    Profile Name
    default (active)
    dev
    staging

この出力例では、ユーザー プロファイル`default`が現在アクティブです。

### ユーザープロフィールを説明する {#describe-a-user-profile}

ユーザー プロファイルのプロパティを取得するには、 [`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md)を使用します。

出力例は次のとおりです。

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### ユーザープロファイルでプロパティを設定する {#set-properties-in-a-user-profile}

ユーザー プロファイルのプロパティを設定するには[`ticloud config set`](/tidb-cloud/ticloud-config-set.md)を使用します。

### 別のユーザー プロファイルに切り替える {#switch-to-another-user-profile}

別のユーザー プロファイルに切り替えるには[`ticloud config use`](/tidb-cloud/ticloud-config-use.md)を使用します。

出力例は次のとおりです。

    Current profile has been changed to default

### 設定ファイルを編集する {#edit-the-config-file}

編集のために構成ファイルを開くには、 [`ticloud config edit`](/tidb-cloud/ticloud-config-edit.md)を使用します。

### ユーザープロファイルを削除する {#delete-a-user-profile}

ユーザー プロファイルを削除するには[`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md)を使用します。

## グローバルフラグ {#global-flags}

次の表に、 TiDB Cloud CLI のグローバル フラグを示します。

| フラグ            | 説明                                   | 必須  | 注記                                                                |
| -------------- | ------------------------------------ | --- | ----------------------------------------------------------------- |
| --色なし          | 出力のカラーを無効にします。                       | いいえ | 非対話モードでのみ動作します。インタラクティブ モードでは、一部の UI コンポーネントで色の無効化が機能しない可能性があります。 |
| -P、--プロファイル文字列 | このコマンドで使用されるアクティブなユーザー プロファイルを指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                          |

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
