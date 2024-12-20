---
title: tiup mirror genkey
summary: TiUP mirror genkey は、 TiUPの秘密鍵を生成するために使用されるコマンドです。キーの名前を指定したり、対応する公開鍵を表示したりするオプションがあります。このコマンドでは、公開鍵情報をファイルとして保存することもできます。秘密鍵をインターネット経由で送信しないことが重要です。
---

# tiup mirror genkey {#tiup-mirror-genkey}

TiUP [鏡](/tiup/tiup-mirror-reference.md)の定義によれば、ユーザーには 3 つの役割があります。

-   ミラー管理者: `root.json` 、 `index.json` 、 `snapshot.json` 、 `timestamp.json`を変更する権限を持ちます。
-   コンポーネント所有者: 対応するコンポーネントを変更する権限を持ちます。
-   通常ユーザー: コンポーネントをダウンロードして使用できます。

TiUPファイルを変更するには対応する所有者/管理者の署名が必要なので、所有者/管理者は独自の秘密鍵を持っている必要があります。コマンド`tiup mirror genkey`は秘密鍵を生成するために使用されます。

> **警告：**
>
> 秘密鍵をインターネット経由で送信**しないでください**。

## 構文 {#syntax}

```shell
tiup mirror genkey [flags]
```

## オプション {#options}

### -n, --名前 {#n-name}

-   キーの名前を指定します。これにより、最終的に生成されるファイルの名前も決まります。生成される秘密キー ファイルのパスは`${TIUP_HOME}/keys/{name}.json`です。 `TIUP_HOME` TiUPのホーム ディレクトリ (デフォルトでは`$HOME/.tiup`を参照します。 `name` `-n/--name`で指定される秘密キー名を参照します。
-   データ型: `STRING`
-   デフォルト: &quot;private&quot;

### -p, --パブリック {#p-public}

-   オプション`-n/--name`で指定された秘密鍵に対応する公開鍵を表示します。
-   `-p/--public`指定した場合、 TiUP は新しい秘密鍵を作成しません。3 `-n/--name`指定した秘密鍵が存在しない場合は、 TiUP はエラーを返します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

### - 保存 {#save}

-   公開鍵の情報を現在のディレクトリにファイルとして保存します。ファイル名は`{hash-prefix}-public.json`です。 `hash-prefix`キー ID の最初の 16 ビットです。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

## 出力 {#outputs}

-   `-p/--public`が指定されていない場合:
    -   `-n/--name`で指定された秘密鍵が存在する場合: TiUP は`Key already exists, skipped`出力します。
    -   `-n/--name`で指定された秘密鍵が存在しない場合: TiUP は`private key have been write to ${TIUP_HOME}/keys/{name}.json`出力します。
-   `-p/--public`が指定された場合:
    -   `-n/--name`で指定された秘密鍵が存在しない場合: TiUP はエラー`Error: open ${TIUP_HOME}/keys/{name}.json: no such file or directory`を報告します。
    -   `-n/--name`で指定した秘密鍵が存在する場合: TiUPは対応する公開鍵の内容を出力します。

[&lt;&lt; 前のページに戻る - TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
