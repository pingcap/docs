---
title: tiup completion
summary: TiUPは、ユーザーのコストを削減するために、コマンドラインを自動補完する構成ファイルを生成するコマンドを提供しています。現在、TiUPはbashとzshコマンドの完了をサポートしており、使用するシェルのタイプを設定するためにtiup completion <shell>コマンドを使用します。具体的な使用法として、bashの場合はtiup completion bashコマンドをファイルに書き込み、.bash_profileでそのファイルをソースします。zshの場合はtiup completion zshコマンドを使用します。
---

# tiup completion {#tiup-completion}

ユーザーのコストを削減するために、 TiUP、コマンド ラインを自動補完するための構成ファイルを生成するコマンドが`tiup completion`提供されています。現在、 TiUP は`bash`と`zsh`コマンドの完了をサポートしています。

`bash`コマンドを完了したい場合は、最初に`bash-completion`をインストールする必要があります。次の手順を参照してください。

-   macOS の場合: bash バージョンが 4.1 より前の場合は、 `brew install bash-completion`を実行します。それ以外の場合は、 `brew install bash-completion@2`を実行します。
-   Linux の場合: パッケージ マネージャーを使用して`bash-completion`をインストールします。たとえば、 `yum install bash-completion`または`apt install bash-completion`を実行します。

## 構文 {#syntax}

```shell
tiup completion <shell>
```

`<shell>`は、使用するシェルのタイプを設定するために使用されます。現在、 `bash`と`zsh`がサポートされています。

## 使用法 {#usage}

### バッシュ {#bash}

`tiup completion bash`コマンドをファイルに書き込み、 `.bash_profile`でそのファイルをソースします。次の例を参照してください。

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

[&lt;&lt; 前のページに戻る - TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
