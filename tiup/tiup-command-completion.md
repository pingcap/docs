---
title: tiup completion
---

# tiup完了 {#tiup-completion}

ユーザーコストを削減するために、TiUPは自動コマンドライン補完用の構成ファイルを生成する`tiup completion`のコマンドを提供します。現在、TiUPは`bash`および`zsh`のコマンドの完了をサポートしています。

`bash`のコマンドを完了する場合は、最初に`bash-completion`をインストールする必要があります。次の手順を参照してください。

-   macOSの場合：bashのバージョンが4.1より前の場合は、 `brew install bash-completion`を実行します。それ以外の場合は、 `brew install bash-completion@2`を実行します。
-   Linuxの場合：パッケージマネージャーを使用して`bash-completion`をインストールします。たとえば、 `yum install bash-completion`または`apt install bash-completion`を実行します。

## 構文 {#syntax}

```shell
tiup completion <shell>
```

`<shell>`は、使用するシェルのタイプを設定するために使用されます。現在、 `bash`と`zsh`がサポートされています。

## 使用法 {#usage}

### バッシュ {#bash}

`tiup completion bash`コマンドをファイルに書き込み、 `.bash_profile`でファイルを調達します。次の例を参照してください。

```shell
tiup completion bash > ~/.tiup.completion.bash

printf "
# tiup shell completion
source '$HOME/.tiup.completion.bash'
" >> $HOME/.bash_profile

source $HOME/.bash_profile
```

### zsh {#zsh}

```shell
tiup completion zsh > "${fpath[1]}/_tiup"
```

[&lt;&lt;前のページに戻る-TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
