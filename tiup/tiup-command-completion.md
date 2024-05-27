---
title: tiup completion
summary: TiUP は、`bash` および `zsh` コマンドをサポートする、自動コマンドライン補完用の設定ファイルを生成するtiup completionコマンドを提供します。`bash` コマンドを補完するには、`bash-completion` をインストールし、`tiup completion <shell>` 構文を使用してシェル タイプを設定します。`bash` の場合は、コマンドをファイルに記述し、`.bash_profile` でソース化します。`zsh` の場合は、`tiup completion zsh` コマンドを使用します。
---

# tiup completion {#tiup-completion}

ユーザーのコスト削減のため、 TiUP は自動コマンドライン補完用の構成ファイルを生成する`tiup completion`コマンドを提供します。現在、 TiUP は`bash`と`zsh`コマンドの補完をサポートしています。

`bash`コマンドを完了するには、まず`bash-completion`をインストールする必要があります。次の手順を参照してください。

-   macOS の場合: bash バージョンが 4.1 より前の場合は`brew install bash-completion`実行し、それ以外の場合は`brew install bash-completion@2`実行します。
-   Linux の場合: パッケージ マネージャーを使用して`bash-completion`インストールします。たとえば、 `yum install bash-completion`または`apt install bash-completion`を実行します。

## 構文 {#syntax}

```shell
tiup completion <shell>
```

`<shell>`は、使用するシェルの種類を設定するために使用されます。現在、 `bash`と`zsh`がサポートされています。

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

### 翻訳 {#zsh}

```shell
tiup completion zsh > "${fpath[1]}/_tiup"
```

[&lt;&lt; 前のページに戻る - TiUPリファレンスコマンドリスト](/tiup/tiup-reference.md#command-list)
