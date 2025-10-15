---
title: TiDB Cloud CLI Reference
summary: TiDB Cloud CLI の概要を説明します。
---

# TiDB Cloud CLI リファレンス (ベータ版) {#tidb-cloud-cli-reference-beta}

> **注記：**
>
> 現在、 TiDB Cloud CLI はベータ版であり、 TiDB Cloud Dedicated クラスターには適用されません。

TiDB Cloud CLIは、数行のコマンドでターミナルからTiDB Cloudを操作できるコマンドラインインターフェースです。TiDB TiDB Cloud CLIでは、 TiDB Cloudクラスターの管理、クラスターへのデータのインポート、その他の操作を簡単に実行できます。

## 始める前に {#before-you-begin}

最初に[TiDB Cloud CLI環境をセットアップする](/tidb-cloud/get-started-with-cli.md)必ず実行してください。3 CLI `ticloud`インストールしたら、それを使用してコマンドラインからTiDB Cloudクラスターを管理できます。

## 利用可能なコマンド {#commands-available}

次の表に、 TiDB Cloud CLI で使用できるコマンドを示します。

ターミナルで`ticloud` CLI を使用するには、 `ticloud [command] [subcommand]`実行してください。 [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview)使用している場合は、代わりに`tiup cloud [command] [subcommand]`実行してください。

| 指示            | サブコマンド                                           | 説明                                                                |
| ------------- | ------------------------------------------------ | ----------------------------------------------------------------- |
| 認証            | ログイン、ログアウト、whoami                                | ログインとログアウト                                                        |
| サーバーレス（別名: s） | 作成、削除、説明、一覧表示、更新、支出制限、リージョン、シェル                  | TiDB Cloud Starter またはTiDB Cloud Essential クラスターを管理する             |
| サーバーレスブランチ    | 作成、削除、説明、一覧表示、シェル                                | TiDB Cloud Starter またはTiDB Cloud Essential クラスターのブランチを管理する        |
| サーバーレスインポート   | キャンセル、説明、リスト、開始                                  | TiDB Cloud Starter またはTiDB Cloud Essential クラスターのインポート タスクを管理します  |
| サーバーレスエクスポート  | 作成、説明、リスト、キャンセル、ダウンロード                           | TiDB Cloud Starter またはTiDB Cloud Essential クラスターのエクスポート タスクを管理します |
| サーバーレスSQLユーザー | 作成、リスト、削除、更新                                     | TiDB Cloud Starter またはTiDB Cloud Essential クラスターの SQL ユーザーを管理します  |
| サーバーレス監査ログ    | config、describe、filter-rule（別名: filter）、download | TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータベース監査ログを管理します |
| 完了            | bash、fish、powershell、zsh                         | 指定されたシェルの補完スクリプトを生成する                                             |
| 設定            | 作成、削除、説明、編集、一覧表示、設定、使用                           | ユーザープロファイルを構成する                                                   |
| プロジェクト        | リスト                                              | プロジェクトの管理                                                         |
| アップグレード       | <li></li>                                        | CLIを最新バージョンに更新する                                                  |
| ヘルプ           | 認証、構成、サーバーレス、プロジェクト、アップグレード、ヘルプ、完了               | 任意のコマンドのヘルプをビュー                                                   |

## コマンドモード {#command-modes}

TiDB Cloud CLI では、簡単に使用できるように、一部のコマンドに 2 つのモードが用意されています。

-   インタラクティブモード

    フラグなしでコマンドを実行すると ( `ticloud config create`など)、CLI によって入力が求められます。

-   非対話モード

    コマンドを実行するときに必要なすべての引数とフラグ (例: `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>` ) を指定する必要があります。

## ユーザープロフィール {#user-profile}

TiDB Cloud CLI の場合、ユーザープロファイルとは、プロファイル名、公開鍵、秘密鍵、OAuth トークンなど、ユーザーに関連付けられたプロパティの集合です。TiDB TiDB Cloud CLI を使用するには、ユーザープロファイルが必要です。

### TiDB Cloud APIキーを使用してユーザープロファイルを作成する {#create-a-user-profile-with-tidb-cloud-api-key}

[`ticloud config create`](/tidb-cloud/ticloud-config-create.md)使用してユーザー プロファイルを作成します。

### OAuthトークンを使用してユーザープロファイルを作成する {#create-a-user-profile-with-oauth-token}

現在のプロファイルにOAuthトークンを割り当てるには、 [`ticloud auth login`](/tidb-cloud/ticloud-auth-login.md)使用します。プロファイルが存在しない場合は、 `default`名前のプロファイルが自動的に作成されます。

> **注記：**
>
> 上記の2つの方法では、 TiDB Cloud APIキーがOAuthトークンよりも優先されます。現在のプロファイルで両方が利用可能な場合は、APIキーが使用されます。

### すべてのユーザープロファイルを一覧表示する {#list-all-user-profiles}

すべてのユーザー プロファイルを一覧表示するには、 [`ticloud config list`](/tidb-cloud/ticloud-config-list.md)使用します。

出力例は次のとおりです。

    Profile Name
    default (active)
    dev
    staging

この出力例では、ユーザー プロファイル`default`現在アクティブです。

### ユーザープロフィールを説明する {#describe-a-user-profile}

ユーザー プロファイルのプロパティを取得するには、 [`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md)使用します。

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

別のユーザー プロファイルに切り替えるには、 [`ticloud config use`](/tidb-cloud/ticloud-config-use.md)使用します。

出力例は次のとおりです。

    Current profile has been changed to default

### 設定ファイルを編集する {#edit-the-config-file}

[`ticloud config edit`](/tidb-cloud/ticloud-config-edit.md)使用して構成ファイルを開き、編集します。

### ユーザープロファイルを削除する {#delete-a-user-profile}

ユーザープロファイルを削除するには[`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md)使用します。

## グローバルフラグ {#global-flags}

次の表は、TiDB Cloud CLI のグローバル フラグを示しています。

| フラグ               | 説明                                   | 必須  | 注記                                                      |
| ----------------- | ------------------------------------ | --- | ------------------------------------------------------- |
| --色なし             | 出力のカラーを無効にします。                       | いいえ | 非対話モードでのみ機能します。対話モードでは、一部のUIコンポーネントで色の無効化が機能しない場合があります。 |
| -P, --profile 文字列 | このコマンドで使用されるアクティブなユーザー プロファイルを指定します。 | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |
| -D, --debug       | デバッグモードを有効にする                        | いいえ | 非対話型モードと対話型モードの両方で動作します。                                |

## フィードバック {#feedback}

TiDB Cloud CLI についてご質問やご提案がございましたら、お気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)作成してください。また、皆様からの貢献も歓迎いたします。
