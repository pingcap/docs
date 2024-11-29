---
title: tiup mirror
summary: TiUPミラーは、ローカルおよびリモートのミラーリングをサポートする、 TiUPの重要な概念です。「tiup mirror」コマンドは、ミラーの管理、コンポーネントの作成と配布、およびキーの管理を行います。構文は「tiup mirror <command> [flags]」です。サポートされているサブコマンドには、genkey、sign、init、set、grant、publish、modify、rotate、clone、merge などがあります。
---

# tiup mirror {#tiup-mirror}

TiUPでは、 [鏡](/tiup/tiup-mirror-reference.md)重要な概念です。TiUPは現在、2 つの形式のミラーリングをサポートしています。

-   ローカル ミラー: TiUPクライアントとミラーは同じマシン上にあり、クライアントはファイル システムを介してミラーにアクセスします。
-   リモート ミラー: TiUPクライアントとミラーは同じマシン上に存在せず、クライアントはネットワーク経由でミラーにアクセスします。

`tiup mirror`コマンドはミラーの管理に使用され、ミラーの作成、コンポーネントの配布、キーの管理を行う方法を提供します。

## 構文 {#syntax}

```shell
tiup mirror <command> [flags]
```

`<command>`サブコマンドを表します。サポートされているサブコマンドのリストについては、以下の[コマンドリスト](#command-list)を参照してください。

## オプション {#option}

なし

## コマンドリスト {#command-list}

-   [ゲンキー](/tiup/tiup-command-mirror-genkey.md) : 秘密鍵ファイルを生成する
-   [サイン](/tiup/tiup-command-mirror-sign.md) : 秘密鍵ファイルを使用して特定のファイルに署名する
-   [初期化](/tiup/tiup-command-mirror-init.md) : 空のミラーを開始します
-   [セット](/tiup/tiup-command-mirror-set.md) : 現在のミラーを設定します
-   [付与](/tiup/tiup-command-mirror-grant.md) : 現在のミラーに新しいコンポーネント所有者を付与します
-   [公開](/tiup/tiup-command-mirror-publish.md) : 新しいコンポーネントを現在のミラーに公開します
-   [修正する](/tiup/tiup-command-mirror-modify.md) : 現在のミラー内のコンポーネントの属性を変更します
-   [回転する](/tiup/tiup-command-mirror-rotate.md) : 現在のミラーのルート証明書を更新します
-   [クローン](/tiup/tiup-command-mirror-clone.md) : 既存のミラーから新しいミラーを複製します
-   [マージ](/tiup/tiup-command-mirror-merge.md) : ミラーをマージする

[&lt;&lt; 前のページに戻る - TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
