---
title: tiup mirror rotate
---

# tiupミラーが回転します {#tiup-mirror-rotate}

`root.json`はTiUPミラーの重要なファイルです。システム全体に必要な公開鍵を保存し、TiUPの信頼の鎖の基礎となります。主に次の部分が含まれています。

-   ミラー管理者の署名。公式ミラーには、5つの署名があります。初期化されたミラーの場合、デフォルトで3つのシグニチャがあります。
-   次のファイルの検証に使用される公開キー：
    -   root.json
    -   index.json
    -   snapshot.json
    -   timestamp.json
-   有効期限は`root.json`です。オフィシャルミラーの場合、有効期限は作成日`root.json`より1年遅れています。

TiUPミラーの詳細については、 [TiUPミラーリファレンス](/tiup/tiup-mirror-reference.md)を参照してください。

次の場合は`root.json`を更新する必要があります。

-   ミラーのキーを交換してください。
-   証明書ファイルの有効期限を更新します。

`root.json`の内容が更新された後、ファイルはすべての管理者によって再署名される必要があります。それ以外の場合、クライアントはファイルを拒否します。更新プロセスは次のとおりです。

1.  ユーザー（クライアント）は`root.json`の内容を更新します。
2.  すべての管理者が新しい`root.json`のファイルに署名します。
3.  tiup-serverは`snapshot.json`を更新して、新しい`root.json`ファイルのバージョンを記録します。
4.  tiup-serverは新しい`snapshot.json`ファイルに署名します。
5.  tiup-serverは`timestamp.json`を更新して、新しい`snapshot.json`ファイルのハッシュ値を記録します。
6.  tiup-serverは新しい`timestamp.json`ファイルに署名します。

TiUPは、コマンド`tiup mirror rotate`を使用して上記のプロセスを自動化します。

> **ノート：**
>
> -   v1.5.0より前のバージョンのTiUPの場合、このコマンドを実行しても正しい新しい`root.json`ファイルは返されません。 [＃983](https://github.com/pingcap/tiup/issues/983)を参照してください。
> -   このコマンドを使用する前に、すべてのTiUPクライアントがv1.5.0以降のバージョンにアップグレードされていることを確認してください。

## 構文 {#syntax}

```shell
tiup mirror rotate [flags]
```

このコマンドを実行した後、TiUPは、 `expires`フィールドの値を後日変更するなど、ユーザーがファイルの内容をターゲット値に変更するためのエディターを起動します。次に、TiUPは`version`フィールドを`N`から`N+1`に変更し、ファイルを保存します。ファイルが保存された後、TiUPは一時的なHTTPサーバーを起動し、すべてのミラー管理者がファイルに署名するのを待ちます。

ミラー管理者がファイルに署名する方法については、 [`sign`コマンド](/tiup/tiup-command-mirror-sign.md)を参照してください。

## オプション {#options}

### --addr {#addr}

-   一時サーバーのリスニングアドレスを指定します。他のミラー管理者が[`sign`コマンド](/tiup/tiup-command-mirror-sign.md)を使用してファイルに署名できるように、アドレスにアクセスできることを確認する必要があります。
-   データ型： `STRING`
-   このオプションがコマンドで指定されていない場合、TiUPはデフォルトで`0.0.0.0:8080`をリッスンします。

## 出力 {#outputs}

各ミラー管理者の現在の署名状況。

[&lt;&lt;前のページに戻る-TiUPミラーコマンドリスト](/tiup/tiup-command-mirror.md#command-list)
