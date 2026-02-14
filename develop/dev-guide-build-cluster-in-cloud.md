---
title: Create a TiDB Cloud Starter Cluster
summary: TiDB Cloud Starter クラスターを作成し、それに接続する方法を学習します。
aliases: ['/ja/tidb/stable/dev-guide-build-cluster-in-cloud/','/ja/tidbcloud/dev-guide-build-cluster-in-cloud/']
---

<!-- markdownlint-disable MD029 -->

# TiDB Cloudスタータークラスタを作成する {#create-a-tidb-cloud-starter-cluster}

このドキュメントでは、TiDBを使い始めるための最も簡単な方法を解説します。1 [TiDB Cloud](https://www.pingcap.com/tidb-cloud)使用してTiDB Cloud Starterクラスターを作成し、接続し、サンプルアプリケーションを実行します。

ローカルマシンで TiDB を実行する必要がある場合は、 [ローカルで TiDB を起動する](/quick-start-with-tidb.md)参照してください。

## ステップ 1. TiDB Cloud Starter クラスターを作成する {#step-1-create-a-tidb-cloud-cluster} {#step-1-create-a-tidb-cloud-cluster}

1.  TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/free-trial)をクリックしてアカウントを登録してください。

2.  [ログイン](https://tidbcloud.com/) TiDB Cloudアカウントに追加します。

3.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、 **[クラスタの作成] を**クリックします。

4.  **「クラスタの作成」**ページでは、デフォルトで**「スターター」**が選択されています。必要に応じてデフォルトのクラスター名を更新し、クラスターを作成するリージョンを選択してください。

5.  **「作成」**をクリックして、 TiDB Cloud Starter クラスターを作成します。

    TiDB Cloudクラスターは約 30 秒で作成されます。

6.  TiDB Cloudクラスターが作成されたら、クラスター名をクリックしてクラスターの概要ページに移動し、右上隅の**「接続」**をクリックします。接続ダイアログボックスが表示されます。

7.  ダイアログで、希望する接続方法とオペレーティングシステムを選択して、対応する接続​​文字列を取得します。このドキュメントでは、MySQLクライアントを例として使用します。

8.  **「パスワードを生成」をクリックすると、ランダムなパスワード**が生成されます。生成されたパスワードは再度表示されないため、安全な場所に保管してください。ルートパスワードを設定しないと、クラスターに接続できません。

> **注記：**
>
> [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)クラスターの場合、クラスターに接続する際には、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix)参照してください。

## ステップ2. クラスターに接続する {#step-2-connect-to-a-cluster}

1.  MySQL クライアントがインストールされていない場合は、オペレーティング システムを選択し、以下の手順に従ってインストールしてください。

<SimpleTab>

<div label="macOS">

macOS の場合、 [Homebrew](https://brew.sh/index)インストールされていない場合はインストールし、次のコマンドを実行して MySQL クライアントをインストールします。

```shell
brew install mysql-client
```

出力は次のようになります。

    mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
    because it conflicts with mysql (which contains client libraries).

    If you need to have mysql-client first in your PATH, run:
      echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

    For compilers to find mysql-client you may need to set:
      export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
      export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"

MySQL クライアントを PATH に追加するには、上記の出力で次のコマンドを見つけて (出力がドキュメント内の上記の出力と一致しない場合は、代わりに出力内の対応するコマンドを使用してください)、実行します。

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

次に、 `source`コマンドでグローバル環境変数を宣言し、MySQL クライアントが正常にインストールされていることを確認します。

```shell
source ~/.zshrc
mysql --version
```

予想される出力の例:

    mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)

</div>

<div label="Linux">

Linux の場合、次の例では Ubuntu を取り上げます。

```shell
apt-get install mysql-client
```

次に、MySQL クライアントが正常にインストールされていることを確認します。

```shell
mysql --version
```

予想される出力の例:

    mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1

</div>

</SimpleTab>

2.  [ステップ1](#step-1-create-a-tidb-cloud-cluster)で取得した接続文字列を実行します。

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

> **注記：**
>
> -   TiDB Cloud Starter クラスターに接続する場合は、 [TLS接続を使用する](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)実行する必要があります。
> -   TiDB Cloud Starter クラスターへの接続時に問題が発生した場合は、詳細については[TiDB Cloudスターター クラスターへのセキュリティ接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)参照してください。

3.  パスワードを入力してサインインしてください。

## ステップ3. SQL文を実行する {#step-3-execute-a-sql-statement}

TiDB Cloudで最初の SQL ステートメントを実行してみましょう。

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

実際の出力が期待された出力と似ている場合は、おめでとうございます。TiDB TiDB Cloudで SQL ステートメントが正常に実行されました。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
