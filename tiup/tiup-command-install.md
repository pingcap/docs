---
title: tiup install
---

# tiup install {#tiup-install}

`tiup install`コマンドは、コンポーネントのインストールに使用されます。指定されたバージョンのコンポーネントパッケージをミラー リポジトリからダウンロードし、後で使用するためにローカルのTiUPデータ ディレクトリに解凍します。さらに、 TiUP がミラー リポジトリに存在しないコンポーネントを実行する必要がある場合、まずコンポーネントをダウンロードしてから、自動的に実行します。コンポーネントがリポジトリに存在しない場合、エラーが報告されます。

## 構文 {#syntax}

```shell
tiup install <component1>[:version] [component2...N] [flags]
```

`<component1>`と`<component2>`コンポーネント名を表し、 `[version]`オプションのバージョン番号を表します。 `version`が追加されていない場合、指定されたコンポーネントの最新の安定バージョンがインストールされます。 `[component2...N]` 、同時に複数のコンポーネントまたは同じコンポーネントの複数のバージョンを指定できることを意味します。

## オプション {#option}

なし

## 出力 {#output}

-   通常はコンポーネントのダウンロード情報を出力します。
-   コンポーネントが存在しない場合、 `The component "%s" not found`エラーが報告されます。
-   バージョンが存在しない場合、 `version %s not supported by component %s`エラーが報告されます。

[&lt;&lt; 前のページに戻る - TiUPリファレンス コマンド一覧](/tiup/tiup-reference.md#command-list)
