---
title: Build a TiDB Cluster in TiDB Cloud (Serverless Tier)
summary: Learn how to build a TiDB cluster in TiDB Cloud (Serverless Tier) and connect to a TiDB Cloud cluster.
---

<!-- markdownlint-disable MD029 -->

# TiDB Cloud(Serverless Tier) で TiDBクラスタを構築する {#build-a-tidb-cluster-in-tidb-cloud-serverless-tier}

<CustomContent platform="tidb">

このドキュメントでは、TiDB を使い始める最も簡単な方法について説明します。 [TiDB Cloud](https://en.pingcap.com/tidb-cloud)を使用してServerless Tierクラスターを作成し、それに接続して、サンプル アプリケーションを実行します。

ローカル マシンで TiDB を実行する必要がある場合は、 [TiDB をローカルで起動する](/quick-start-with-tidb.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

このドキュメントでは、 TiDB Cloudを開始するための最も簡単な方法について説明します。 TiDB クラスターを作成して接続し、サンプル アプリケーションを実行します。

</CustomContent>

## ステップ 1.Serverless Tierクラスターを作成する {#step-1-create-a-serverless-tier-cluster}

1.  TiDB Cloudアカウントを持っていない場合は、 [ここ](https://tidbcloud.com/free-trial)クリックしてアカウントにサインアップします。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントに追加します。

    デフォルトでは[**クラスター**](https://tidbcloud.com/console/clusters)リスト ページが表示されます。

3.  新しいサインアップ ユーザーの場合、 TiDB Cloud はデフォルトのServerless Tierクラスター`Cluster0`を自動的に作成します。以降の手順でこのデフォルト クラスタを使用するか、独自に新しいServerless Tierクラスタを作成することができます。

    自分で新しいServerless Tierクラスターを作成するには、次の操作を行います。

    1.  **[クラスタの作成]**をクリックします。
    2.  **[クラスタの作成]**ページでは、<strong>サーバーレスが</strong>デフォルトで選択されています。クラスターのターゲット リージョンを選択し、必要に応じて既定のクラスター名を更新して、 <strong>[作成]</strong>をクリックします。 Serverless Tierクラスタは約 30 秒で作成されます。

4.  クラスターの概要ページで、右上隅にある**[接続]**をクリックします。接続ダイアログボックスが表示されます。

5.  ダイアログで、希望する接続方法とオペレーティング システムを選択して、対応する接続文字列を取得します。このドキュメントでは、MySQL クライアントを例として使用します。

6.  **[パスワードの作成]**をクリックして、ランダムなパスワードを生成します。生成されたパスワードは二度と表示されないため、パスワードを安全な場所に保存してください。 root パスワードを設定しないと、クラスターに接続できません。

<CustomContent platform="tidb">

> **ノート：**
>
> [Serverless Tierクラスター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier)の場合、クラスターに接続するときに、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#user-name-prefix)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)の場合、クラスターに接続するときに、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

</CustomContent>

## ステップ 2. クラスターに接続する {#step-2-connect-to-a-cluster}

1.  MySQL クライアントがインストールされていない場合は、オペレーティング システムを選択し、以下の手順に従ってインストールします。

<SimpleTab>

<div label="macOS">

macOS の場合、 [Homebrew](https://brew.sh/index)がない場合はインストールしてから、次のコマンドを実行して MySQL クライアントをインストールします。

```shell
brew install mysql-client
```

出力は次のとおりです。

```
mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with mysql (which contains client libraries).

If you need to have mysql-client first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql-client you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
```

MySQL クライアントを PATH に追加するには、上記の出力で次のコマンドを見つけて (出力がドキュメントの上記の出力と一致しない場合は、代わりに出力で対応するコマンドを使用してください)、それを実行します。

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

次に、 `source`コマンドでグローバル環境変数を宣言し、MySQL クライアントが正常にインストールされていることを確認します。

```shell
source ~/.zshrc
mysql --version
```

予想される出力の例:

```
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

Linux の場合、次の例では CentOS 7 を使用しています。

```shell
yum install mysql
```

次に、MySQL クライアントが正常にインストールされたことを確認します。

```shell
mysql --version
```

予想される出力の例:

```
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```

</div>

</SimpleTab>

2.  [ステップ1](#step-1-create-a-serverless-tier-cluster)で取得した接続文字列を実行します。

    {{< copyable "" >}}

    ```shell
    mysql --connect-timeout 15 -u '<prefix>.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p
    ```

<CustomContent platform="tidb">

> **ノート：**
>
> -   Serverless Tierクラスターに接続する場合は、 [TLS 接続を使用する](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters) .
> -   Serverless Tierクラスターへの接続時に問題が発生した場合は、詳細について[Serverless Tierクラスターへのセキュリティ接続](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> -   Serverless Tierクラスターに接続する場合は、 [TLS 接続を使用する](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md) .
> -   Serverless Tierクラスターへの接続時に問題が発生した場合は、詳細について[Serverless Tierクラスターへのセキュリティ接続](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)を参照してください。

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

実際の出力が予想される出力と似ている場合は、おめでとう、 TiDB Cloudで SQL ステートメントを正常に実行したことになります。
