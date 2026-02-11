---
title: Connect to TiDB with MySQL Tools
summary: MySQL ツールを使用して TiDB に接続する方法を学習します。
---

# MySQLツールでTiDBに接続する {#connect-to-tidb-with-mysql-tools}

TiDBはMySQLプロトコルと高い互換性があります。クライアントリンクパラメータの完全なリストについては、 [MySQLクライアントオプション](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html)参照してください。

TiDB は[MySQL クライアント/サーバー プロトコル](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)をサポートしており、これにより、ほとんどのクライアント ドライバーと ORM フレームワークは、MySQL に接続するのと同じように TiDB に接続できます。

個人の好みに応じて、MySQL クライアントまたは MySQL シェルの使用を選択できます。

<SimpleTab>

<div label="MySQL Client">

TiDB には、MySQL クライアントを使用して接続できます。MySQL クライアントは、TiDB のコマンドラインツールとして使用できます。MySQL クライアントをインストールするには、YUM ベースの Linux ディストリビューションの以下の手順に従ってください。

```shell
sudo yum install mysql
```

インストール後、次のコマンドを使用して TiDB に接続できます。

```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

macOS上のMySQL v9.0クライアントはプラグイン`mysql_native_password`を正しくロードできないため、TiDBへの接続時にエラー`ERROR 2059 (HY000): Authentication plugin 'mysql_native_password' cannot be loaded`が発生します。この問題を解決するには、MySQL v8.0クライアントをインストールしてTiDBに接続することをお勧めします。インストールするには、以下のコマンドを実行してください。

```shell
brew install mysql-client@8.0
brew unlink mysql
brew link mysql-client@8.0
```

それでもエラーが発生する場合は、MySQL v8.0クライアントのインストールパスを指定してTiDBに接続してください。以下のコマンドを実行してください。

```shell
/opt/homebrew/opt/mysql-client@8.0/bin/mysql --comments --host ${YOUR_IP_ADDRESS} --port ${YOUR_PORT_NUMBER} -u ${your_user_name} -p
```

上記のコマンドの`/opt/homebrew/opt/mysql-client@8.0/bin/mysql` 、実際の環境の MySQL v8.0 クライアントのインストール パスに置き換えます。

</div>

<div label="MySQL Shell">

TiDBへの接続には、MySQL Shellを使用します。MySQL Shellは、TiDBのコマンドラインツールとして使用できます。MySQL Shellをインストールするには、 [MySQL Shell ドキュメント](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html)手順に従ってください。インストール後、以下のコマンドでTiDBに接続できます。

```shell
mysqlsh --sql mysql://root@<tidb_server_host>:4000
```

</div>

</SimpleTab>

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
