---
title: tiup install
---

# tiup install {#tiup-install}

`tiup install`コマンドはコンポーネントのインストールに使用されます。指定されたバージョンのコンポーネントパッケージをミラー リポジトリからダウンロードし、後で使用できるようにローカルのTiUPデータ ディレクトリに解凍します。さらに、 TiUP がミラー リポジトリに存在しないコンポーネントを実行する必要がある場合、最初にコンポーネントのダウンロードを試行し、その後自動的に実行します。コンポーネントがリポジトリに存在しない場合は、エラーが報告されます。

## 構文 {#syntax}

```shell
tiup install <component1>[:version] [component2...N] [flags]
```

`<component1>`と`<component2>`コンポーネント名を表し、 `[version]`オプションのバージョン番号を表します。 `version`が追加されていない場合は、指定されたコンポーネントの最新の安定したバージョンがインストールされます。 `[component2...N]`複数のコンポーネント、または同じコンポーネントの複数のバージョンを同時に指定できることを意味します。

## オプション {#option}

なし

## 出力 {#output}

-   通常はコンポーネントのダウンロード情報を出力します。
-   コンポーネントが存在しない場合は、エラー`The component "%s" not found`が報告されます。
-   バージョンが存在しない場合は、 `version %s not supported by component %s`エラーが報告されます。

[&lt;&lt; 前のページに戻る - TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
