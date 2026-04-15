---
title: TiDB Cloud CLI Reference
summary: TiDB Cloud CLIの概要を説明します。
---

# TiDB Cloud CLI リファレンス (ベータ版) {#tidb-cloud-cli-reference-beta}

> **注記：**
>
> 現在、 TiDB Cloud CLIはベータ版であり、 TiDB Cloud Dedicatedクラスタには適用できません。

TiDB Cloud CLIはコマンドラインインターフェースであり、ターミナルから数行のコマンドを入力するだけでTiDB Cloudを操作できます。TiDB TiDB Cloud CLIを使用すると、 TiDB Cloud StarterおよびEssentialインスタンスを簡単に管理したり、インスタンスにデータをインポートしたり、その他の操作を実行したりできます。

## 始める前に {#before-you-begin}

必ず最初に[TiDB Cloud CLI環境をセットアップする](/tidb-cloud/get-started-with-cli.md)。 `ticloud` CLI をインストールすると、それを使用してコマンド ラインからTiDB Cloud StarterインスタンスとEssentialインスタンスを管理できるようになります。

## 使用可能なコマンド {#commands-available}

以下の表は、TiDB Cloud CLIで使用できるコマンドの一覧です。

ターミナルで`ticloud` CLIを使用するには、 `ticloud [command] [subcommand]`を実行してください。TiUP [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview)使用している場合は、代わりに`tiup cloud [command] [subcommand]`を使用してください。

| 指示            | サブコマンド                             | 説明                                                               |
| ------------- | ---------------------------------- | ---------------------------------------------------------------- |
| 認証            | ログイン、ログアウト、whoami                  | ログインとログアウト                                                       |
| サーバーレス（別名：s）  | 作成、削除、説明、一覧表示、更新、支出制限、リージョン、シェル    | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを管理する             |
| サーバーレスブランチ    | 作成、削除、説明、一覧表示、シェル                  | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのブランチを管理します。      |
| サーバーレスインポート   | キャンセル、説明、リスト、開始                    | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのインポートタスクを管理します。  |
| サーバーレスエクスポート  | 作成、説明、一覧表示、キャンセル、ダウンロード            | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのエクスポートタスクを管理します。 |
| サーバーレスSQLユーザー | 作成、一覧表示、削除、更新                      | TiDB Cloud StarterまたはTiDB Cloud EssentialインスタンスのSQLユーザーを管理する     |
| サーバーレス監査ログ    | 設定、説明、フィルタルール（別名：フィルタ）、ダウンロード      | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのデータベース監査ログを管理する  |
| 完了            | bash、fish、powershell、zsh           | 指定されたシェル用の補完スクリプトを生成する                                           |
| 設定            | 作成、削除、説明、編集、一覧表示、設定、使用             | ユーザープロファイルの設定                                                    |
| プロジェクト        | リスト                                | プロジェクトを管理する                                                      |
| アップグレード       | -                                  | CLIを最新バージョンにアップデートしてください                                         |
| ヘルプ           | 認証、設定、サーバーレス、プロジェクト、アップグレード、ヘルプ、完了 | 任意のコマンドのヘルプをビュー                                                  |

## コマンドモード {#command-modes}

TiDB Cloud CLIは、一部のコマンドを簡単に使用できるよう、2つのモードを提供しています。

-   対話モード

    フラグなしでコマンドを実行することもできます（例： `ticloud config create` ）。その場合、CLIは入力を求めます。

-   非対話モード

    `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`のように、コマンドを実行する際に必要なすべての引数とフラグを指定する必要があります。

## ユーザープロフィール {#user-profile}

TiDB Cloud CLI では、ユーザープロファイルとは、プロファイル名、公開鍵、秘密鍵、OAuth トークンなど、ユーザーに関連付けられたプロパティの集合です。TiDB TiDB Cloud CLI を使用するには、ユーザープロファイルが必要です。

### TiDB Cloud APIキーを使用してユーザープロファイルを作成します。 {#create-a-user-profile-with-tidb-cloud-api-key}

[`ticloud config create`](/tidb-cloud/ticloud-config-create.md)を使用してユーザープロファイルを作成します。

### OAuthトークンを使用してユーザープロファイルを作成します。 {#create-a-user-profile-with-oauth-token}

[`ticloud auth login`](/tidb-cloud/ticloud-auth-login.md)使用して、現在のプロファイルに OAuth トークンを割り当てます。プロファイルが存在しない場合は、 `default`という名前のプロファイルが自動的に作成されます。

> **注記：**
>
> 上記2つの方法では、 TiDB Cloud APIキーがOAuthトークンよりも優先されます。現在のプロファイルに両方が存在する場合は、APIキーが使用されます。

### すべてのユーザープロファイルを一覧表示します {#list-all-user-profiles}

[`ticloud config list`](/tidb-cloud/ticloud-config-list.md)を使用して、すべてのユーザープロファイルを一覧表示します。

出力例は以下のとおりです。

    Profile Name
    default (active)
    dev
    staging

この出力例では、ユーザープロファイル`default`が現在アクティブです。

### ユーザープロファイルについて説明してください {#describe-a-user-profile}

[`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md)を使用して、ユーザープロファイルのプロパティを取得します。

出力例は以下のとおりです。

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### ユーザープロファイルでプロパティを設定する {#set-properties-in-a-user-profile}

[`ticloud config set`](/tidb-cloud/ticloud-config-set.md)使用して、ユーザープロファイルのプロパティを設定します。

### 別のユーザープロファイルに切り替える {#switch-to-another-user-profile}

[`ticloud config use`](/tidb-cloud/ticloud-config-use.md)使用して、別のユーザープロファイルに切り替えます。

出力例は以下のとおりです。

    Current profile has been changed to default

### 設定ファイルを編集する {#edit-the-config-file}

[`ticloud config edit`](/tidb-cloud/ticloud-config-edit.md)使用して、設定ファイルを開いて編集します。

### ユーザープロファイルを削除する {#delete-a-user-profile}

[`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md)を使用してユーザープロファイルを削除します。

## 世界の国旗 {#global-flags}

以下の表は、TiDB Cloud CLI のグローバルフラグの一覧です。

| フラグ                 | 説明                                  | 必須  | 注記                                                         |
| ------------------- | ----------------------------------- | --- | ---------------------------------------------------------- |
| --色なし               | 出力における色の使用を無効にします。                  | いいえ | 非対話モードでのみ動作します。対話モードでは、一部のUIコンポーネントで色の無効化が正しく機能しない場合があります。 |
| -P、--profile string | このコマンドで使用されるアクティブなユーザープロファイルを指定します。 | いいえ | 非対話モードと対話モードの両方で動作します。                                     |
| -D、--debug          | デバッグモードを有効にする                       | いいえ | 非対話モードと対話モードの両方で動作します。                                     |

## フィードバック {#feedback}

TiDB Cloud CLI に関してご質問やご提案がありましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)ご報告ください。また、皆様からの貢献も歓迎いたします。
