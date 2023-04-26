---
title: tiup mirror genkey
---

# tiup mirror genkey {#tiup-mirror-genkey}

TiUP [鏡](/tiup/tiup-mirror-reference.md)は、その定義によると、ユーザーの 3 つの役割があります。

-   ミラー管理者: `root.json` 、 `index.json` 、 `snapshot.json` 、および`timestamp.json`を変更する権限があります。
-   コンポーネントの所有者: 対応するコンポーネントを変更する権限があります。
-   通常のユーザー: コンポーネントをダウンロードして使用できます。

TiUP は、ファイルを変更するために対応する所有者/管理者の署名を必要とするため、所有者/管理者は自分の秘密鍵を持っている必要があります。コマンド`tiup mirror genkey`は、秘密鍵を生成するために使用されます。

> **警告：**
>
> 秘密鍵をインターネット経由で送信**しないでください**。

## 構文 {#syntax}

```shell
tiup mirror genkey [flags]
```

## オプション {#options}

### -n, --name {#n-name}

-   最終的に生成されるファイルの名前も決定するキーの名前を指定します。生成された秘密鍵ファイルのパスは`${TIUP_HOME}/keys/{name}.json`です。 `TIUP_HOME` TiUPのホーム ディレクトリを指し、デフォルトでは`$HOME/.tiup`です。 `name` `-n/--name`が指定する秘密鍵の名前を指します。
-   データ型: `STRING`
-   デフォルト: 「非公開」

### -p, --public {#p-public}

-   オプション`-n/--name`で指定された秘密鍵に対応する公開鍵を示します。
-   `-p/--public`を指定すると、 TiUP は新しい秘密鍵を作成しません。 `-n/--name`で指定した秘密鍵が存在しない場合、 TiUPはエラーを返します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を何も渡さないようにします。

### - 保存 {#save}

-   公開鍵の情報をカレントディレクトリにファイルとして保存します。ファイル名は`{hash-prefix}-public.json`です。 `hash-prefix`はキー ID の最初の 16 ビットです。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を何も渡さないようにします。

## 出力 {#outputs}

-   `-p/--public`が指定されていない場合:
    -   `-n/--name`で指定した秘密鍵が存在する場合: TiUP は`Key already exists, skipped`を出力します。
    -   `-n/--name`で指定した秘密鍵が存在しない場合: TiUP は`private key have been write to ${TIUP_HOME}/keys/{name}.json`を出力します。
-   `-p/--public`を指定した場合:
    -   `-n/--name`で指定した秘密鍵が存在しない場合: TiUP はエラー`Error: open ${TIUP_HOME}/keys/{name}.json: no such file or directory`を報告します。
    -   `-n/--name`で指定した秘密鍵が存在する場合： TiUPは対応する公開鍵の内容を出力します。

[&lt;&lt; 前のページに戻る - TiUP Mirror コマンド一覧](/tiup/tiup-command-mirror.md#command-list)
