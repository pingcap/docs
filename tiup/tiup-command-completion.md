---
title: tiup completion
summary: TiUPは、 tiup completionコマンドを使用して、bash`および`zsh`コマンドに対応したコマンドライン自動補完用の設定ファイルを生成します。`bash`コマンドを補完するには、`bash-completion`をインストールし、`tiup completion <shell>`構文を使用してシェルの種類を設定します。`bash`の場合は、コマンドをファイルに記述し、`.bash_profile`でsourceコマンドとして読み込みます。`zsh`の場合は、`tiup completion zsh`コマンドを使用します。
---

# tiup completion {#tiup-completion}

ユーザーの負担を軽減するため、 TiUP はコマンドラインの自動補完用の設定ファイルを生成するコマンド`tiup completion`を提供しています。現在、 TiUP はコマンド`bash`と`zsh`補完をサポートしています。

`bash`コマンドを実行するには、まず`bash-completion`をインストールする必要があります。以下の手順をご覧ください。

-   macOS の場合: bash バージョンが 4.1 より前の場合は`brew install bash-completion`実行し、それ以外の場合は`brew install bash-completion@2`実行します。
-   Linuxの場合：パッケージマネージャーを使用して`bash-completion`インストールします。たとえば、 `yum install bash-completion`または`apt install bash-completion`実行します。

## 構文 {#syntax}

```shell
tiup completion <shell>
```

`<shell>`は使用するシェルの種類を設定するために使用されます。現在、 `bash`と`zsh`サポートされています。

## 使用法 {#usage}

### バッシュ {#bash}

`tiup completion bash`コマンドをファイルに書き込み、 `.bash_profile`でそのファイルをソースコードとして読み込みます。次の例をご覧ください。

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
