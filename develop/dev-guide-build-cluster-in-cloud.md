---
title: Create a TiDB Cloud Starter Instance
summary: TiDB Cloud Starterインスタンスの作成方法と接続方法を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-build-cluster-in-cloud/','/ja/tidb/dev/dev-guide-build-cluster-in-cloud/','/ja/tidbcloud/dev-guide-build-cluster-in-cloud/']
---

<!-- markdownlint-disable MD029 -->

# TiDB Cloud Starterインスタンスを作成する {#create-a-tidb-cloud-starter-instance}

このドキュメントでは、TiDB を使い始めるための最も簡単な方法を説明します。TiDB [TiDB Cloud](https://www.pingcap.com/tidb-cloud)使用してTiDB Cloud Starterインスタンスを作成し、それに接続して、サンプル アプリケーションを実行します。

ローカル マシンで TiDB を実行する必要がある場合は、 [TiDBをローカルで起動する](/quick-start-with-tidb.md)を参照してください。

## ステップ1. TiDB Cloud Starterインスタンスを作成します {#step-1-create-a-starter-instance} {#step-1-create-a-starter-instance}

1.  TiDB Cloudアカウントをお持ちでない場合は、[ここ](https://tidbcloud.com/free-trial)をクリックしてアカウントを作成してください。

2.  TiDB Cloudアカウントに[ログイン](https://tidbcloud.com/)。

3.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、 **「リソースの作成」**をクリックします。

4.  **「リソースの作成」**ページでは、デフォルトで**「Starter」**が選択されています。TiDB TiDB Cloud Starterインスタンスの名前を入力し、作成先のクラウドプロバイダーとリージョンを選択してください。

5.  **「作成」**をクリックして、 TiDB Cloud Starterインスタンスを作成します。

    TiDB Cloud Starterインスタンスは、約30秒で作成されます。

6.  TiDB Cloud Starterインスタンスが作成されたら、インスタンス名をクリックして概要ページに移動し、右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

7.  ダイアログで、希望する接続方法とオペレーティングシステムを選択すると、対応する接続​​文字列が表示されます。このドキュメントでは、例としてMySQLクライアントを使用します。

8.  **「パスワードを生成」をクリックすると、ランダムなパスワード**が生成されます。生成されたパスワードは二度と表示されないため、安全な場所に保存してください。ルートパスワードを設定しないと、 TiDB Cloud Starterインスタンスに接続できません。

> **注記：**
>
> TiDB Cloud Starterインスタンスに接続するときは、ユーザー名にインスタンスのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名の接頭辞](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix)参照してください。

## ステップ2. TiDB Cloud Starterインスタンスに接続します {#step-2-connect-to-a-starter-instance} {#step-2-connect-to-a-starter-instance}

1.  MySQLクライアントがインストールされていない場合は、お使いのオペレーティングシステムを選択し、以下の手順に従ってインストールしてください。

<SimpleTab>

<div label="macOS">

macOSの場合、 [Homebrew](https://brew.sh/index)がインストールされていない場合はインストールし、以下のコマンドを実行してMySQLクライアントをインストールしてください。

```shell
brew install mysql-client
```

出力は以下のとおりです。

    mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
    because it conflicts with mysql (which contains client libraries).

    If you need to have mysql-client first in your PATH, run:
      echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

    For compilers to find mysql-client you may need to set:
      export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
      export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"

MySQLクライアントをPATHに追加するには、上記の出力から次のコマンドを探し（出力がドキュメントの上記の出力と一致しない場合は、代わりに出力にある対応するコマンドを使用してください）、実行します。

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

次に、 `source`コマンドを使用してグローバル環境変数を宣言し、MySQL クライアントが正常にインストールされていることを確認します。

```shell
source ~/.zshrc
mysql --version
```

期待される出力例：

    mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)

</div>

<div label="Linux">

Linuxの場合、以下ではUbuntuを例として挙げます。

```shell
apt-get install mysql-client
```

次に、MySQLクライアントが正常にインストールされていることを確認します。

```shell
mysql --version
```

期待される出力例：

    mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1

</div>

</SimpleTab>

2.  [ステップ1](#step-1-create-a-starter-instance)で取得した接続文字列を実行します。

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

> **注記：**
>
> -   TiDB Cloud Starterインスタンスに接続するときは、 [TLS接続を使用する](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)必要があります。
> -   TiDB Cloud Starterインスタンスへの接続時に問題が発生した場合は、 [TiDB Cloud Starterインスタンスへのセキュリティ接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)で詳細を確認してください。

3.  ログインするにはパスワードを入力してください。

## ステップ3．SQLステートメントを実行する {#step-3-execute-a-sql-statement}

TiDB Cloudで最初のSQL文を実行してみましょう。

```sql
SELECT 'Hello TiDB Cloud!';
```

期待される出力:

```sql
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
| Hello TiDB Cloud! |
+-------------------+
```

実際の出力が期待される出力と類似していれば、おめでとうございます。TiDB TiDB Cloud上で SQL ステートメントを正常に実行できました。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
