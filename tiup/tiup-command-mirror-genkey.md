---
title: tiup mirror genkey
---

# tiupミラーゲンキー {#tiup-mirror-genkey}

TiUP [鏡](/tiup/tiup-mirror-reference.md)は、その定義によれば、ユーザーの3つの役割があります。

-   ミラー管理者`snapshot.json` `root.json` 、および`index.json`を変更する権限があり`timestamp.json` 。
-   コンポーネントの所有者：対応するコンポーネントを変更する権限があります。
-   通常のユーザー：コンポーネントをダウンロードして使用できます。

TiUPはファイルを変更するために対応する所有者/管理者の署名を必要とするため、所有者/管理者は自分の秘密鍵を持っている必要があります。コマンド`tiup mirror genkey`は、秘密鍵を生成するために使用されます。

> **警告：**
>
> インターネット経由で秘密鍵を送信し**ない**でください。

## 構文 {#syntax}

```shell
tiup mirror genkey [flags]
```

## オプション {#options}

### -n、-name {#n-name}

-   キーの名前を指定します。これにより、最終的に生成されるファイルの名前も決まります。生成された秘密鍵ファイルのパスは`${TIUP_HOME}/keys/{name}.json`です。 `TIUP_HOME`は、TiUPのホームディレクトリを指します。デフォルトでは`$HOME/.tiup`です。 `name`は、 `-n/--name`が指定する秘密鍵名を指します。
-   データ型： `STRING`
-   デフォルト：「プライベート」

### -p、-public {#p-public}

-   オプション`-n/--name`で指定された秘密鍵の対応する公開鍵を表示します。
-   `-p/--public`が指定されている場合、TiUPは新しい秘密鍵を作成しません。 `-n/--name`で指定された秘密鍵が存在しない場合、TiUPはエラーを返します。
-   データ型： `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、 `true`の値を渡すか、値を渡さないようにします。

### - 保存 {#save}

-   公開鍵の情報をファイルとして現在のディレクトリに保存します。ファイル名は`{hash-prefix}-public.json`です。 `hash-prefix`はキーIDの最初の16ビットです。
-   データ型： `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、 `true`の値を渡すか、値を渡さないようにします。

## 出力 {#outputs}

-   `-p/--public`が指定されていない場合：
    -   `-n/--name`で指定された秘密鍵が存在する場合：TiUPは`Key already exists, skipped`を出力します。
    -   `-n/--name`で指定された秘密鍵が存在しない場合：TiUPは`private key have been write to ${TIUP_HOME}/keys/{name}.json`を出力します。
-   `-p/--public`を指定した場合：
    -   `-n/--name`で指定された秘密鍵が存在しない場合：TiUPはエラー`Error: open ${TIUP_HOME}/keys/{name}.json: no such file or directory`を報告します。
    -   `-n/--name`で指定された秘密鍵が存在する場合：TiUPは、対応する公開鍵の内容を出力します。

[&lt;&lt;前のページに戻る-TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
