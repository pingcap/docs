---
title: tiup dm deploy
---

# tiupdmデプロイ {#tiup-dm-deploy}

`tiup dm deploy`コマンドは、新しいクラスタをデプロイするために使用されます。

## 構文 {#syntax}

```shell
tiup dm deploy <cluster-name> <version> <topology.yaml> [flags]
```

-   `<cluster-name>` ：新しいクラスタの名前。既存のクラスタ名と同じにすることはできません。
-   `<version>` ：デプロイするDMクラスタのバージョン番号（ `v2.0.0`など）。
-   `<topology.yaml>` ：準備された[トポロジーファイル](/tiup/tiup-dm-topology-reference.md) 。

## オプション {#options}

### -u、-user {#u-user}

-   ターゲットマシンへの接続に使用されるユーザー名を指定します。このユーザーは、ターゲットマシンでシークレットフリーのsudoroot権限を持っている必要があります。
-   データ型： `STRING`
-   デフォルト：コマンドを実行する現在のユーザー。

### -i、-identity_file {#i-identity-file}

-   ターゲットマシンへの接続に使用されるキーファイルを指定します。
-   データ型： `STRING`
-   デフォルト： `~/.ssh/id_rsa`

### -p、-password {#p-password}

-   ターゲットマシンへの接続に使用するパスワードを指定します。このオプションと`-i/--identity_file`を同時に使用しないでください。
-   データ型： `BOOLEAN`
-   デフォルト：false

### -h, --help {#h-help}

-   ヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   デフォルト：false

## 出力 {#output}

展開ログ。

[&lt;&lt;前のページに戻るTiUP DMコマンドリスト](/tiup/tiup-component-dm.md#command-list)
