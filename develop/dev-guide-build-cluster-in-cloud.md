---
title: Build a TiDB Serverless Cluster
summary: Learn how to build a TiDB Serverless cluster in TiDB Cloud and connect to it.
---

<!-- markdownlint-disable MD029 -->

# TiDB サーバーレスクラスタを構築する {#build-a-tidb-serverless-cluster}

<CustomContent platform="tidb">

このドキュメントでは、TiDB を始める最も簡単な方法を説明します。 [TiDB Cloud](https://en.pingcap.com/tidb-cloud)を使用して TiDB サーバーレス クラスターを作成し、それに接続し、サンプル アプリケーションを実行します。

ローカル マシンで TiDB を実行する必要がある場合は、 [TiDB をローカルで開始する](/quick-start-with-tidb.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

このドキュメントでは、 TiDB Cloudを開始するための最も簡単な方法を説明します。 TiDB クラスターを作成し、それに接続し、その上でサンプル アプリケーションを実行します。

</CustomContent>

## ステップ 1. TiDB サーバーレスクラスターを作成する {#step-1-create-a-tidb-serverless-cluster}

1.  TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/free-trial)をクリックしてアカウントにサインアップしてください。

2.  TiDB Cloudアカウントに[ログイン](https://tidbcloud.com/) 。

3.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、 **「クラスタの作成」**をクリックします。

4.  **「クラスタの作成」**ページでは、デフォルトで**サーバーレス**が選択されています。必要に応じてデフォルトのクラスター名を更新し、クラスターを作成するリージョンを選択します。

5.  **「作成」を**クリックして、TiDB サーバーレスクラスターを作成します。

    TiDB Cloudクラスターは約 30 秒で作成されます。

6.  TiDB Cloudクラスターが作成されたら、クラスター名をクリックしてクラスターの概要ページに移動し、右上隅の**[接続]**をクリックします。接続ダイアログボックスが表示されます。

7.  ダイアログで、希望の接続方法とオペレーティング システムを選択して、対応する接続​​文字列を取得します。このドキュメントでは、例として MySQL クライアントを使用します。

8.  **「パスワードの作成」**をクリックして、ランダムなパスワードを生成します。生成されたパスワードは再度表示されないため、パスワードを安全な場所に保存してください。 root パスワードを設定しないと、クラスターに接続できません。

<CustomContent platform="tidb">

> **注記：**
>
> [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターの場合、クラスターに接続するときに、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターの場合、クラスターに接続するときに、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

</CustomContent>

## ステップ 2. クラスターに接続する {#step-2-connect-to-a-cluster}

1.  MySQL クライアントがインストールされていない場合は、オペレーティング システムを選択し、以下の手順に従ってインストールします。

<SimpleTab>

<div label="macOS">

macOS の場合、 [Homebrew](https://brew.sh/index)がない場合はインストールし、次のコマンドを実行して MySQL クライアントをインストールします。

```shell
brew install mysql-client
```

出力は次のとおりです。

    mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
    because it conflicts with mysql (which contains client libraries).

    If you need to have mysql-client first in your PATH, run:
      echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

    For compilers to find mysql-client you may need to set:
      export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
      export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"

MySQL クライアントを PATH に追加するには、上記の出力内で次のコマンドを見つけて実行します (出力がドキュメント内の上記の出力と一致しない場合は、代わりに出力内の対応するコマンドを使用してください)。

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

Linux の場合、次の例では CentOS 7 を使用します。

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

2.  [ステップ1](#step-1-create-a-tidb-serverless-cluster)で取得した接続文字列を実行します。

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB サーバーレス クラスターに接続する場合は、 [TLS接続を使用する](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)を行う必要があります。
> -   TiDB サーバーレス クラスターに接続するときに問題が発生した場合は、 [TiDB サーバーレスクラスターへのセキュリティ接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)を読んで詳細を確認してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB サーバーレス クラスターに接続する場合は、 [TLS接続を使用する](/tidb-cloud/secure-connections-to-serverless-clusters.md)を行う必要があります。
> -   TiDB サーバーレス クラスターに接続するときに問題が発生した場合は、 [TiDB サーバーレスクラスターへのセキュリティ接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を読んで詳細を確認してください。

</CustomContent>

3.  パスワードを入力してサインインします。

## ステップ 3. SQL ステートメントを実行する {#step-3-execute-a-sql-statement}

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

実際の出力が予想される出力と類似している場合、おめでとうございます。TiDB TiDB Cloudで SQL ステートメントが正常に実行されました。
