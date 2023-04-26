---
title: tiup dm deploy
---

# tiup dm デプロイ {#tiup-dm-deploy}

`tiup dm deploy`コマンドは、新しいクラスターをデプロイするために使用されます。

## 構文 {#syntax}

```shell
tiup dm deploy <cluster-name> <version> <topology.yaml> [flags]
```

-   `<cluster-name>` : 新しいクラスターの名前。既存のクラスター名と同じにすることはできません。
-   `<version>` : デプロイする DM クラスターのバージョン番号`v2.0.0`など)。
-   `<topology.yaml>` : 準備された[トポロジ ファイル](/tiup/tiup-dm-topology-reference.md) 。

## オプション {#options}

### -u, --user {#u-user}

-   ターゲット マシンへの接続に使用するユーザー名を指定します。このユーザーには、ターゲット マシンでシークレットのない sudo root 権限が必要です。
-   データ型: `STRING`
-   デフォルト: コマンドを実行する現在のユーザー。

### -i, --identity_file {#i-identity-file}

-   ターゲット マシンへの接続に使用するキー ファイルを指定します。
-   データ型: `STRING`
-   デフォルト: `~/.ssh/id_rsa`

### -p, --password {#p-password}

-   ターゲット マシンへの接続に使用するパスワードを指定します。このオプションと`-i/--identity_file`を同時に使用しないでください。
-   データ型: `BOOLEAN`
-   デフォルト: false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   デフォルト: false

## 出力 {#output}

展開ログ。

[&lt;&lt; 前のページに戻る - TiUP DMコマンド一覧](/tiup/tiup-component-dm.md#command-list)
