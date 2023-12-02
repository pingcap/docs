---
title: Create a Private Mirror
summary: Learn how to create a private mirror.
---

# プライベートミラーを作成する {#create-a-private-mirror}

プライベート クラウドを作成する場合、通常は、 TiUPの公式ミラーにアクセスできない、隔離されたネットワーク環境を使用する必要があります。したがって、プライベート ミラーを作成できます。これは主に`mirror`コマンドによって実装されます。オフライン展開には`mirror`コマンドを使用することもできます。プライベート ミラーを使用すると、自分で構築およびパッケージ化したコンポーネントを使用することもできます。

## TiUP <code>mirror</code>概要 {#tiup-code-mirror-code-overview}

次のコマンドを実行して、 `mirror`コマンドのヘルプ情報を取得します。

```bash
tiup mirror --help
```

```bash
The `mirror` command is used to manage a component repository for TiUP, you can use
it to create a private repository, or to add new component to an existing repository.
The repository can be used either online or offline.
It also provides some useful utilities to help manage keys, users, and versions
of components or the repository itself.

Usage:
  tiup mirror <command> [flags]

Available Commands:
  init        Initialize an empty repository
  sign        Add signatures to a manifest file
  genkey      Generate a new key pair
  clone       Clone a local mirror from a remote mirror and download all selected components
  merge       Merge two or more offline mirrors
  publish     Publish a component
  show        Show the mirror address
  set         Set mirror address
  modify      Modify published component
  renew       Renew the manifest of a published component.
  grant       grant a new owner
  rotate      Rotate root.json

Global Flags:
      --help                 Help for this command

Use "tiup mirror [command] --help" for more information about a command.
```

## ミラーのクローンを作成する {#clone-a-mirror}

`tiup mirror clone`コマンドを実行してローカル ミラーを構築できます。

```bash
tiup mirror clone <target-dir> [global-version] [flags]
```

-   `target-dir` : クローンデータが保存されるディレクトリを指定するために使用されます。
-   `global-version` : すべてのコンポーネントのグローバル バージョンを迅速に設定するために使用されます。

`tiup mirror clone`コマンドは、多くのオプションのフラグを提供します (将来的にはさらに多くのフラグが提供される可能性があります)。これらのフラグは、使用目的に応じて次のカテゴリに分類できます。

-   クローン作成時にバージョンを一致させるためにプレフィックス マッチングを使用するかどうかを決定します。

    `--prefix`フラグが指定されている場合、バージョン番号はクローンのプレフィックスによって照合されます。たとえば、「v5.0.0」として`--prefix`指定すると、「v5.0.0-rc」と「v5.0.0」が一致します。

-   完全なクローンを使用するかどうかを決定します

    `--full`フラグを指定すると、公式ミラーを完全に複製できます。

    > **注記：**
    >
    > `--full` 、 `global-version`フラグ、およびコンポーネントのバージョンが指定されていない場合は、一部のメタ情報のみが複製されます。

-   特定のプラットフォームからパッケージを複製するかどうかを決定します

    特定のプラットフォームに対してのみパッケージのクローンを作成する場合は、 `-os`と`-arch`を使用してプラットフォームを指定します。例えば：

    -   `tiup mirror clone <target-dir> [global-version] --os=linux`コマンドを実行して、Linux のクローンを作成します。
    -   `tiup mirror clone <target-dir> [global-version] --arch=amd64`コマンドを実行して amd64 のクローンを作成します。
    -   `tiup mirror clone <target-dir> [global-version] --os=linux --arch=amd64`コマンドを実行して、linux/amd64 のクローンを作成します。

-   パッケージの特定のバージョンのクローンを作成するかどうかを決定します

    コンポーネントの 1 つのバージョン (すべてのバージョンではない) のみを複製する場合は、 `--<component>=<version>`を使用してこのバージョンを指定します。例えば：

    -   `tiup mirror clone <target-dir> --tidb v7.5.0`コマンドを実行して、TiDBコンポーネントの v7.5.0 バージョンのクローンを作成します。
    -   `tiup mirror clone <target-dir> --tidb v7.5.0 --tikv all`コマンドを実行して、v7.5.0 バージョンの TiDBコンポーネントとすべてのバージョンの TiKVコンポーネントのクローンを作成します。
    -   `tiup mirror clone <target-dir> v7.5.0`コマンドを実行して、クラスター内のすべてのコンポーネントの v7.5.0 バージョンのクローンを作成します。

クローン作成後、署名キーが自動的に設定されます。

### プライベートリポジトリを管理する {#manage-the-private-repository}

`tiup mirror clone`を使用して複製されたリポジトリは、SCP、NFS 経由でファイルを共有するか、HTTP または HTTPS プロトコル経由でリポジトリを利用できるようにすることで、ホスト間で共有できます。リポジトリの場所を指定するには、 `tiup mirror set <location>`使用します。

```bash
tiup mirror set /shared_data/tiup
```

```bash
tiup mirror set https://tiup-mirror.example.com/
```

> **注記：**
>
> `tiup mirror clone`実行しているマシンで`tiup mirror set...`を実行すると、次回`tiup mirror clone...`を実行するときに、マシンはリモート ミラーではなくローカル ミラーからクローンを作成します。したがって、プライベート ミラーを更新する前に、 `tiup mirror set --reset`を実行してミラーをリセットする必要があります。

ミラーを使用する別の方法は、 `TIUP_MIRRORS`環境変数を使用することです。以下はプライベート リポジトリで`tiup list`を実行する例です。

```bash
export TIUP_MIRRORS=/shared_data/tiup
tiup list
```

`TIUP_MIRRORS`設定では、ミラー構成を永続的に変更できます (例: `tiup mirror set` 。詳細は[ティアップ号 #651](https://github.com/pingcap/tiup/issues/651)を参照してください。

### プライベートリポジトリを更新する {#update-the-private-repository}

同じ`target-dir`を指定して`tiup mirror clone`コマンドを再度実行すると、マシンは新しいマニフェストを作成し、利用可能なコンポーネントの最新バージョンをダウンロードします。

> **注記：**
>
> マニフェストを再作成する前に、すべてのコンポーネントとバージョン (以前にダウンロードした以前のものを含む) が含まれていることを確認してください。

## カスタムリポジトリ {#custom-repository}

カスタム リポジトリを作成して、自分で構築した TiDB、TiKV、PD などの TiDB コンポーネントを操作できます。独自の tiup コンポーネントを作成することもできます。

独自のコンポーネントを作成するには、 `tiup package`コマンドを実行し、 [コンポーネントの梱包](https://github.com/pingcap/tiup/blob/master/doc/user/package.md)の指示に従って実行します。

### カスタムリポジトリを作成する {#create-a-custom-repository}

`/data/mirror`で空のリポジトリを作成するには:

```bash
tiup mirror init /data/mirror
```

リポジトリの作成の一環として、キーは`/data/mirror/keys`に書き込まれます。

`~/.tiup/keys/private.json`で新しい秘密キーを作成するには:

```bash
tiup mirror genkey
```

秘密鍵`~/.tiup/keys/private.json`持つ`jdoe`に`/data/mirror`の所有権を付与します。

```bash
tiup mirror set /data/mirror
tiup mirror grant jdoe
```

### カスタムコンポーネントの操作 {#work-with-custom-components}

1.  hello という名前のカスタムコンポーネントを作成します。

    ```bash
    $ cat > hello.c << END
    > #include <stdio.h>
    int main() {
      printf("hello\n");
      return (0);
    }
    END
    $ gcc hello.c -o hello
    $ tiup package hello --entry hello --name hello --release v0.0.1
    ```

    `package/hello-v0.0.1-linux-amd64.tar.gz`が作成されます。

2.  リポジトリと秘密キーを作成し、リポジトリに所有権を付与します。

    ```bash
    $ tiup mirror init /tmp/m
    $ tiup mirror genkey
    $ tiup mirror set /tmp/m
    $ tiup mirror grant $USER
    ```

    ```bash
    tiup mirror publish hello v0.0.1 package/hello-v0.0.1-linux-amd64.tar.gz hello
    ```

3.  コンポーネントを実行します。まだインストールされていない場合は、最初にダウンロードされます。

    ```bash
    $ tiup hello
    ```

        The component `hello` version  is not installed; downloading from repository.
        Starting component `hello`: /home/dvaneeden/.tiup/components/hello/v0.0.1/hello
        hello

    `tiup mirror merge`を使用すると、カスタム コンポーネントを含むリポジトリを別のリポジトリにマージできます。これは、 `/data/my_custom_components`のすべてのコンポーネントが現在の`$USER`によって署名されていることを前提としています。

    ```bash
    $ tiup mirror set /data/my_mirror
    $ tiup mirror grant $USER
    $ tiup mirror merge /data/my_custom_components
    ```
