---
title: tiup mirror
---

# tiup mirror {#tiup-mirror}

TiUPでは[鏡](/tiup/tiup-mirror-reference.md)が重要な概念です。 TiUP は現在、次の 2 つの形式のミラーリングをサポートしています。

-   ローカル ミラー: TiUPクライアントとミラーは同じマシン上にあり、クライアントはファイル システムを通じてミラーにアクセスします。
-   リモート ミラー: TiUPクライアントとミラーは同じマシン上になく、クライアントはネットワーク経由でミラーにアクセスします。

`tiup mirror`コマンドはミラーの管理に使用され、ミラーの作成、コンポーネントの配布、キーの管理を行う方法を提供します。

## 構文 {#syntax}

```shell
tiup mirror <command> [flags]
```

`<command>`サブコマンドを表します。サポートされているサブコマンドの一覧は、以下の[コマンドリスト](#command-list)を参照してください。

## オプション {#option}

なし

## コマンド一覧 {#command-list}

-   [ゲンキー](/tiup/tiup-command-mirror-genkey.md) : 秘密鍵ファイルを生成します
-   [サイン](/tiup/tiup-command-mirror-sign.md) : 秘密鍵ファイルを使用して特定のファイルに署名します
-   [初期化](/tiup/tiup-command-mirror-init.md) : 空のミラーを開始します
-   [セット](/tiup/tiup-command-mirror-set.md) : カレントミラーを設定します
-   [付与](/tiup/tiup-command-mirror-grant.md) : 現在のミラーに新しいコンポーネント所有者を付与します。
-   [公開](/tiup/tiup-command-mirror-publish.md) : 新しいコンポーネントを現在のミラーに公開します
-   [修正する](/tiup/tiup-command-mirror-modify.md) : 現在のミラー内のコンポーネントの属性を変更します
-   [回転させる](/tiup/tiup-command-mirror-rotate.md) : 現在のミラー内のルート証明書を更新します
-   [クローン](/tiup/tiup-command-mirror-clone.md) : 既存のミラーから新しいミラーのクローンを作成します
-   [マージ](/tiup/tiup-command-mirror-merge.md) : ミラーを結合します

[&lt;&lt; 前のページに戻る - TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
