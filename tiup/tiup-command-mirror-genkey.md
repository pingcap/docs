---
title: tiup mirror genkey
summary: TiUP mirror genkey は、 TiUP用の秘密鍵を生成するためのコマンドです。鍵の名前を指定したり、対応する公開鍵を表示したりするオプションがあります。また、公開鍵の情報をファイルとして保存することもできます。秘密鍵をインターネット経由で送信しないよう注意してください。
---

# tiup mirror genkey {#tiup-mirror-genkey}

TiUP [鏡](/tiup/tiup-mirror-reference.md)定義によれば、ユーザーには 3 つの役割があります。

-   ミラー管理者: `root.json` 、 `index.json` 、 `snapshot.json` 、 `timestamp.json`を変更する権限があります。
-   コンポーネント所有者: 対応するコンポーネントを変更する権限を持ちます。
-   通常ユーザー: コンポーネントをダウンロードして使用できます。

TiUPファイルを変更するには対応する所有者/管理者の署名が必要となるため、所有者/管理者は独自の秘密鍵を保有している必要があります。コマンド`tiup mirror genkey`秘密鍵を生成するために使用されます。

> **警告：**
>
> 秘密鍵をインターネット経由で送信**しないでください**。

## 構文 {#syntax}

```shell
tiup mirror genkey [flags]
```

## オプション {#options}

### -n, --name {#n-name}

-   キーの名前を指定します。この名前は、最終的に生成されるファイルの名前も決定します。生成される秘密鍵ファイルのパスは`${TIUP_HOME}/keys/{name}.json`です。 `TIUP_HOME` TiUPのホームディレクトリ（デフォルトでは`$HOME/.tiup`を指します。 `name` `-n/--name`指定される秘密鍵の名前を指します。
-   データ型: `STRING`
-   デフォルト:「プライベート」

### -p, --public {#p-public}

-   オプション`-n/--name`で指定された秘密鍵に対応する公開鍵を表示します。
-   `-p/--public`指定された場合、 TiUP は新しい`-n/--name`鍵を作成しません。3 で指定された秘密鍵が存在しない場合、 TiUP はエラーを返します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないかのいずれかを選択します。

### - 保存 {#save}

-   公開鍵の情報を現在のディレクトリにファイルとして保存します。ファイル名は`{hash-prefix}-public.json`です。3 `hash-prefix`鍵IDの最初の16ビットです。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないかのいずれかを選択します。

## 出力 {#outputs}

-   `-p/--public`が指定されていない場合:
    -   `-n/--name`で指定された秘密鍵が存在する場合: TiUP は`Key already exists, skipped`出力します。
    -   `-n/--name`で指定された秘密鍵が存在しない場合: TiUP は`private key have been write to ${TIUP_HOME}/keys/{name}.json`出力します。
-   `-p/--public`指定した場合:
    -   `-n/--name`で指定された秘密鍵が存在しない場合: TiUP はエラー`Error: open ${TIUP_HOME}/keys/{name}.json: no such file or directory`報告します。
    -   `-n/--name`で指定された秘密鍵が存在する場合： TiUPは対応する公開鍵の内容を出力します。

[&lt;&lt; 前のページに戻る - TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
