---
title: tiup mirror
---

# tiup mirror {#tiup-mirror}

TiUPでは、 [鏡](/tiup/tiup-mirror-reference.md)は重要な概念です。 TiUPは現在、次の2つの形式のミラーリングをサポートしています。

-   ローカルミラー：TiUPクライアントとミラーは同じマシン上にあり、クライアントはファイルシステムを介してミラーにアクセスします。
-   リモートミラー：TiUPクライアントとミラーは同じマシン上になく、クライアントはネットワークを介してミラーにアクセスします。

`tiup mirror`コマンドは、ミラーを管理するために使用され、ミラーを作成し、コンポーネントを配布し、キーを管理する方法を提供します。

## 構文 {#syntax}

```shell
tiup mirror <command> [flags]
```

`<command>`はサブコマンドを表します。サポートされているサブコマンドのリストについては、以下の[コマンドリスト](#command-list)を参照してください。

## オプション {#option}

なし

## コマンドリスト {#command-list}

-   [ゲンキー](/tiup/tiup-command-mirror-genkey.md) ：秘密鍵ファイルを生成します
-   [サイン](/tiup/tiup-command-mirror-sign.md) ：秘密鍵ファイルを使用して特定のファイルに署名します
-   [初期化](/tiup/tiup-command-mirror-init.md) ：空のミラーを開始します
-   [設定](/tiup/tiup-command-mirror-set.md) ：現在のミラーを設定します
-   [許す](/tiup/tiup-command-mirror-grant.md) ：現在のミラーの新しいコンポーネント所有者を付与します
-   [公開](/tiup/tiup-command-mirror-publish.md) ：新しいコンポーネントを現在のミラーに公開します
-   [変更](/tiup/tiup-command-mirror-modify.md) ：現在のミラーのコンポーネントの属性を変更します
-   [回転する](/tiup/tiup-command-mirror-rotate.md) ：現在のミラーのルート証明書を更新します
-   [クローン](/tiup/tiup-command-mirror-clone.md) ：既存のミラーから新しいミラーを複製します
-   [マージ](/tiup/tiup-command-mirror-merge.md) ：ミラーをマージします

[&lt;&lt;前のページに戻る-TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
