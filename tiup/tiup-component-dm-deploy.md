---
title: tiup dm deploy
summary: tiup dm deploy` コマンドは、新しいクラスターをデプロイするために使用されます。クラスター名、バージョン、および準備されたトポロジ ファイルが必要です。オプションのフラグには、ユーザー、ID ファイル、パスワード、およびヘルプが含まれます。出力はデプロイメント ログです。
---

# tiup dm デプロイ {#tiup-dm-deploy}

`tiup dm deploy`コマンドは、新しいクラスターをデプロイするために使用されます。

## 構文 {#syntax}

```shell
tiup dm deploy <cluster-name> <version> <topology.yaml> [flags]
```

-   `<cluster-name>` : 新しいクラスターの名前。既存のクラスター名と同じにすることはできません。
-   `<version>` : デプロイする DM クラスターのバージョン番号 (例: `v2.0.0` 。
-   `<topology.yaml>` : 準備された[トポロジファイル](/tiup/tiup-dm-topology-reference.md) 。

## オプション {#options}

### -u、--ユーザー {#u-user}

-   ターゲット マシンへの接続に使用するユーザー名を指定します。このユーザーには、ターゲット マシンに対するシークレットフリーの sudo ルート権限が必要です。
-   データ型: `STRING`
-   デフォルト: コマンドを実行する現在のユーザー。

### -i, --identity_file {#i-identity-file}

-   ターゲット マシンに接続するために使用されるキー ファイルを指定します。
-   データ型: `STRING`
-   デフォルト: `~/.ssh/id_rsa`

### -p, --パスワード {#p-password}

-   ターゲット マシンに接続するために使用するパスワードを指定します。このオプションと`-i/--identity_file`同時に使用しないでください。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

デプロイメント ログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
