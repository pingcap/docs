---
title: Build a TiDB Cloud Serverless Cluster
summary: TiDB CloudでTiDB Cloud Serverless クラスターを構築し、それに接続する方法を学習します。
---

<!-- markdownlint-disable MD029 -->

# TiDB Cloudサーバーレスクラスタを構築する {#build-a-tidb-cloud-serverless-cluster}

<CustomContent platform="tidb">

このドキュメントでは、TiDB を使い始めるための最も簡単な方法を説明します。1 [TiDB Cloud](https://www.pingcap.com/tidb-cloud)使用してTiDB Cloud Serverless クラスターを作成し、それに接続し、その上でサンプル アプリケーションを実行します。

ローカルマシンで TiDB を実行する必要がある場合は、 [ローカルで TiDB を起動する](/quick-start-with-tidb.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

このドキュメントでは、 TiDB Cloudを使い始めるための最も簡単な方法を説明します。TiDB クラスターを作成し、それに接続し、その上でサンプル アプリケーションを実行します。

</CustomContent>

## ステップ1. TiDB Cloud Serverlessクラスターを作成する {#step-1-create-a-tidb-cloud-serverless-cluster}

1.  TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/free-trial)クリックしてアカウントを登録してください。

2.  [ログイン](https://tidbcloud.com/) TiDB Cloudアカウントに追加します。

3.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、 **[クラスタの作成]**をクリックします。

4.  **[クラスタの作成]**ページでは、デフォルトで**Serverless**が選択されています。必要に応じてデフォルトのクラスター名を更新し、クラスターを作成するリージョンを選択します。

5.  **「作成」**をクリックして、 TiDB Cloud Serverless クラスターを作成します。

    TiDB Cloudクラスターは約 30 秒で作成されます。

6.  TiDB Cloudクラスターが作成されたら、クラスター名をクリックしてクラスターの概要ページに移動し、右上隅の**[接続]**をクリックします。接続ダイアログ ボックスが表示されます。

7.  ダイアログで、希望する接続方法とオペレーティング システムを選択して、対応する接続文字列を取得します。このドキュメントでは、例として MySQL クライアントを使用します。

8.  「**パスワードの生成」**をクリックすると、ランダムなパスワードが生成されます。生成されたパスワードは再度表示されないため、パスワードは安全な場所に保存してください。ルート パスワードを設定しないと、クラスターに接続できません。

<CustomContent platform="tidb">

> **注記：**
>
> [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターの場合、クラスターに接続するときは、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名プレフィックス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターの場合、クラスターに接続するときは、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名プレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。

</CustomContent>

## ステップ2. クラスターに接続する {#step-2-connect-to-a-cluster}

1.  MySQL クライアントがインストールされていない場合は、オペレーティング システムを選択し、以下の手順に従ってインストールしてください。

<SimpleTab>

<div label="macOS">

macOS の場合、まだインストールしていない場合は[Homebrew](https://brew.sh/index)インストールし、次のコマンドを実行して MySQL クライアントをインストールします。

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

Linux の場合、以下は CentOS 7 を例にしています。

```shell
yum install mysql
```

次に、MySQL クライアントが正常にインストールされていることを確認します。

```shell
mysql --version
```

予想される出力の例:

    mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1

</div>

</SimpleTab>

2.  [ステップ1](#step-1-create-a-tidb-cloud-serverless-cluster)で取得した接続文字列を実行します。

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB Cloud Serverless クラスターに接続する場合は、 [TLS接続を使用する](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)実行する必要があります。
> -   TiDB Cloud Serverless クラスターへの接続時に問題が発生した場合は、詳細については[TiDB Cloudサーバーレス クラスターへのセキュリティ接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB Cloud Serverless クラスターに接続する場合は、 [TLS接続を使用する](/tidb-cloud/secure-connections-to-serverless-clusters.md)実行する必要があります。
> -   TiDB Cloud Serverless クラスターへの接続時に問題が発生した場合は、詳細については[TiDB Cloudサーバーレス クラスターへのセキュリティ接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)参照してください。

</CustomContent>

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

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
