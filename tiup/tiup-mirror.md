---
title: Create a Private Mirror
summary: Learn how to create a private mirror.
---

# プライベートミラーを作成する {#create-a-private-mirror}

プライベートクラウドを作成するときは、通常、TiUPの公式ミラーにアクセスできない分離されたネットワーク環境を使用する必要があります。したがって、主に`mirror`コマンドで実装されるプライベートミラーを作成できます。 `mirror`コマンドを使用してオフライン展開することもできます。プライベートミラーを使用すると、自分で作成してパッケージ化したコンポーネントを使用することもできます。

## TiUP <code>mirror</code>の概要 {#tiup-code-mirror-code-overview}

次のコマンドを実行して、 `mirror`コマンドのヘルプ情報を取得します。

{{< copyable "" >}}

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
      --skip-version-check   Skip the strict version check, by default a version must be a valid SemVer string

Use "tiup mirror [command] --help" for more information about a command.
```

## ミラーのクローンを作成する {#clone-a-mirror}

`tiup mirror clone`コマンドを実行して、ローカルミラーを構築できます。

{{< copyable "" >}}

```bash
tiup mirror clone <target-dir> [global-version] [flags]
```

-   `target-dir` ：クローンデータが保存されるディレクトリを指定するために使用されます。
-   `global-version` ：すべてのコンポーネントのグローバルバージョンをすばやく設定するために使用されます。

`tiup mirror clone`コマンドは、多くのオプションのフラグを提供します（将来さらに提供される可能性があります）。これらのフラグは、使用目的に応じて次のカテゴリに分類できます。

-   クローン作成時にバージョンと一致するようにプレフィックス一致を使用するかどうかを決定します

    `--prefix`フラグが指定されている場合、バージョン番号はクローンのプレフィックスと一致します。たとえば、「v5.0.0」として`--prefix`を指定すると、「v5.0.0-rc」と「v5.0.0」が一致します。

-   フルクローンを使用するかどうかを決定します

    `--full`フラグを指定すると、公式ミラーを完全に複製できます。

    > **ノート：**
    >
    > `--full`フラグ、およびコンポーネントバージョンが指定されていない場合、一部のメタ情報のみが複製され`global-version` 。

-   特定のプラットフォームからパッケージを複製するかどうかを決定します

    特定のプラットフォームのパッケージのみを複製する場合は、 `-os`と`-arch`を使用してプラットフォームを指定します。例えば：

    -   Linux用にクローンを作成するには、 `tiup mirror clone <target-dir> [global-version] --os=linux`コマンドを実行します。
    -   `tiup mirror clone <target-dir> [global-version] --arch=amd64`コマンドを実行して、amd64のクローンを作成します。
    -   `tiup mirror clone <target-dir> [global-version] --os=linux --arch=amd64`コマンドを実行して、linux/amd64のクローンを作成します。

-   パッケージの特定のバージョンを複製するかどうかを決定します

    コンポーネントの1つのバージョン（すべてのバージョンではない）のみを複製する場合は、 `--<component>=<version>`を使用してこのバージョンを指定します。例えば：

    -   `tiup mirror clone <target-dir> --tidb v6.1.0`コマンドを実行して、TiDBコンポーネントのv6.1.0バージョンのクローンを作成します。
    -   `tiup mirror clone <target-dir> --tidb v6.1.0 --tikv all`コマンドを実行して、TiDBコンポーネントのv6.1.0バージョンとTiKVコンポーネントのすべてのバージョンのクローンを作成します。
    -   `tiup mirror clone <target-dir> v6.1.0`コマンドを実行して、クラスタのすべてのコンポーネントのv6.1.0バージョンのクローンを作成します。

クローン作成後、署名キーが自動的に設定されます。

### プライベートリポジトリを管理する {#manage-the-private-repository}

SCP、NFSを介してファイルを共有するか、HTTPまたはHTTPSプロトコルを介してリポジトリを利用できるようにすることで、ホスト間で`tiup mirror clone`を使用して複製されたリポジトリを共有できます。 `tiup mirror set <location>`を使用して、リポジトリの場所を指定します。

```bash
tiup mirror set /shared_data/tiup
```

```bash
tiup mirror set https://tiup-mirror.example.com/
```

> **ノート：**
>
> `tiup mirror clone`を実行するマシンで`tiup mirror set...`を実行すると、次に`tiup mirror clone...`を実行するときに、マシンはリモートミラーではなくローカルミラーからクローンを作成します。したがって、プライベートミラーを更新する前に、 `tiup mirror set --reset`を実行してミラーをリセットする必要があります。

ミラーを使用する別の方法は、 `TIUP_MIRRORS`の環境変数を使用することです。プライベートリポジトリで`tiup list`を実行する例を次に示します。

```bash
export TIUP_MIRRORS=/shared_data/tiup
tiup list
```

`TIUP_MIRRORS`に設定すると、ミラー構成を永続的に変更できます（例： `tiup mirror set` ）。詳細については、 [tiup問題＃651](https://github.com/pingcap/tiup/issues/651)を参照してください。

### プライベートリポジトリを更新する {#update-the-private-repository}

同じ`target-dir`を使用して`tiup mirror clone`コマンドを再度実行すると、マシンは新しいマニフェストを作成し、使用可能なコンポーネントの最新バージョンをダウンロードします。

> **ノート：**
>
> マニフェストを再作成する前に、すべてのコンポーネントとバージョン（以前にダウンロードしたものを含む）が含まれていることを確認してください。

## カスタムリポジトリ {#custom-repository}

自分で作成したTiDB、TiKV、PDなどのTiDBコンポーネントを操作するカスタムリポジトリを作成できます。独自のtiupコンポーネントを作成することもできます。

独自のコンポーネントを作成するには、 `tiup package`コマンドを実行し、 [コンポーネントのパッケージ](https://github.com/pingcap/tiup/blob/master/doc/user/package.md)の指示に従って実行します。

### カスタムリポジトリを作成する {#create-a-custom-repository}

`/data/mirror`で空のリポジトリを作成するには：

```bash
tiup mirror init /data/mirror
```

リポジトリ作成の一環として、キーは`/data/mirror/keys`に書き込まれます。

`~/.tiup/keys/private.json`で新しい秘密鍵を作成するには：

```bash
tiup mirror genkey
```

`/data/mirror`の秘密鍵`~/.tiup/keys/private.json`の所有権を持つ`jdoe`を付与します。

```bash
tiup mirror set /data/mirror
tiup mirror grant jdoe
```

### カスタムコンポーネントを操作する {#work-with-custom-components}

1.  helloというカスタムコンポーネントを作成します。

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

2.  リポジトリと秘密鍵を作成し、リポジトリに所有権を付与します。

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

    ```
    The component `hello` version  is not installed; downloading from repository.
    Starting component `hello`: /home/dvaneeden/.tiup/components/hello/v0.0.1/hello
    hello
    ```

    `tiup mirror merge`を使用すると、カスタムコンポーネントを含むリポジトリを別のリポジトリにマージできます。これは、 `/data/my_custom_components`のすべてのコンポーネントが現在の`$USER`によって署名されていることを前提としています。

    ```bash
    $ tiup mirror set /data/my_mirror
    $ tiup mirror grant $USER
    $ tiup mirror merge /data/my_custom_components
    ```
