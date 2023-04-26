---
title: tiup mirror rotate
---

# tiup mirror rotate {#tiup-mirror-rotate}

`root.json`はTiUPミラーの重要なファイルです。システム全体に必要な公開鍵を格納し、 TiUPの信頼チェーンの基礎となります。主に次の部分で構成されています。

-   ミラー管理者の署名。オフィシャルミラーには5名のサイン入り。初期化されたミラーには、デフォルトで 3 つの署名があります。
-   次のファイルの検証に使用される公開鍵:
    -   root.json
    -   index.json
    -   スナップショット.json
    -   タイムスタンプ.json
-   `root.json`の有効期限。公式ミラーの場合、有効期限は`root.json`の作成日から 1 年後です。

TiUPミラーの詳細な説明については、 [TiUPミラー リファレンス](/tiup/tiup-mirror-reference.md)を参照してください。

次の場合は、 `root.json`を更新する必要があります。

-   ミラーのキーを交換します。
-   証明書ファイルの有効期限を更新します。

`root.json`の内容が更新された後、すべての管理者がファイルに再署名する必要があります。そうでない場合、クライアントはファイルを拒否します。更新プロセスは次のとおりです。

1.  ユーザー (クライアント) は`root.json`の内容を更新します。
2.  すべての管理者が新しい`root.json`ファイルに署名します。
3.  tiup-server は`snapshot.json`を更新して、新しい`root.json`ファイルのバージョンを記録します。
4.  tiup-server は新しい`snapshot.json`ファイルに署名します。
5.  tiup-server は`timestamp.json`を更新して、新しい`snapshot.json`ファイルのハッシュ値を記録します。
6.  tiup-server は新しい`timestamp.json`ファイルに署名します。

TiUP はコマンド`tiup mirror rotate`を使用して、上記のプロセスを自動化します。

> **ノート：**
>
> -   v1.5.0 より前のTiUPバージョンでは、このコマンドを実行しても正しい新しい`root.json`ファイルが返されません。 [#983](https://github.com/pingcap/tiup/issues/983)を参照してください。
> -   このコマンドを使用する前に、すべてのTiUPクライアントが v1.5.0 以降のバージョンにアップグレードされていることを確認してください。

## 構文 {#syntax}

```shell
tiup mirror rotate [flags]
```

このコマンドを実行した後、 TiUP は、ユーザーがファイルの内容を目的の値に変更するためのエディターを起動します ( `expires`フィールドの値を後の日付に変更するなど)。次に、 TiUP は`version`フィールドを`N`から`N+1`に変更し、ファイルを保存します。ファイルが保存されると、 TiUP は一時的な HTTPサーバーを起動し、すべてのミラー管理者がファイルに署名するのを待ちます。

ミラー管理者がファイルに署名する方法については、 [`sign`コマンド](/tiup/tiup-command-mirror-sign.md)を参照してください。

## オプション {#options}

### --addr {#addr}

-   一時サーバーのリッスン アドレスを指定します。他のミラー管理者が[`sign`コマンド](/tiup/tiup-command-mirror-sign.md)を使用してファイルに署名できるように、アドレスにアクセスできることを確認する必要があります。
-   データ型: `STRING`
-   このオプションがコマンドで指定されていない場合、 TiUP はデフォルトで`0.0.0.0:8080`をリッスンします。

## 出力 {#outputs}

各ミラー管理者の現在の署名ステータス。

[&lt;&lt; 前のページに戻る - TiUP Mirror コマンド一覧](/tiup/tiup-command-mirror.md#command-list)
