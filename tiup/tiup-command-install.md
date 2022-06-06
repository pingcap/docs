---
title: tiup install
---

# tiupインストール {#tiup-install}

`tiup install`コマンドは、コンポーネントのインストールに使用されます。指定されたバージョンのコンポーネントパッケージをミラーリポジトリからダウンロードし、後で使用できるようにローカルTiUPデータディレクトリに解凍します。さらに、TiUPがミラーリポジトリに存在しないコンポーネントを実行する必要がある場合、TiUPは最初にコンポーネントをダウンロードしてから、自動的に実行しようとします。コンポーネントがリポジトリに存在しない場合、エラーが報告されます。

## 構文 {#syntax}

```shell
tiup install <component1>[:version] [component2...N] [flags]
```

`<component1>`と`<component2>`はコンポーネント名を表し、 `[version]`はオプションのバージョン番号を表します。 `version`が追加されていない場合は、指定されたコンポーネントの最新の安定バージョンがインストールされます。 `[component2...N]`は、複数のコンポーネントまたは同じコンポーネントの複数のバージョンを同時に指定できることを意味します。

## オプション {#option}

なし

## 出力 {#output}

-   通常、コンポーネントのダウンロード情報を出力します。
-   コンポーネントが存在しない場合は、 `The component "%s" not found`エラーが報告されます。
-   バージョンが存在しない場合は、 `version %s not supported by component %s`エラーが報告されます。

[&lt;&lt;前のページに戻る-TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
