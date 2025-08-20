---
title: Create a Private Mirror
summary: プライベートミラーを作成する方法を学びます。
---

# プライベートミラーを作成する {#create-a-private-mirror}

プライベートクラウドを構築する場合、通常、 TiUPの公式ミラーにアクセスできない隔離されたネットワーク環境を使用する必要があります。そのため、プライベートミラーを作成することができます。プライベートミラーは主に`mirror`コマンドで実装されます。オフラインデプロイメントには`mirror`コマンドも使用できます。プライベートミラーでは、独自に構築およびパッケージ化したコンポーネントも使用できます。

## TiUP <code>mirror</code>概要 {#tiup-code-mirror-code-overview}

`mirror`コマンドのヘルプ情報を取得するには、次のコマンドを実行します。

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

`tiup mirror clone`コマンドを実行してローカルミラーを構築できます。

```bash
tiup mirror clone <target-dir> [global-version] [flags]
```

-   `target-dir` : クローンデータが保存されるディレクトリを指定するために使用されます。
-   `global-version` : すべてのコンポーネントのグローバル バージョンをすばやく設定するために使用されます。

`tiup mirror clone`コマンドは多くのオプションフラグを提供します（将来的にはさらに追加される可能性があります）。これらのフラグは、その用途に応じて以下のカテゴリに分類できます。

-   クローン作成時にバージョンを一致させるためにプレフィックスマッチングを使用するかどうかを決定します

    フラグ`--prefix`が指定された場合、クローンのバージョン番号はプレフィックスによって照合されます。例えば、 `--prefix` 「v5.0.0」と指定した場合、「v5.0.0-rc」と「v5.0.0」が一致します。

-   完全なクローンを使用するかどうかを決定します

    `--full`フラグを指定すると、公式ミラーを完全にクローンできます。

    > **注記：**
    >
    > フラグ`--full` 、およびコンポーネントバージョン`global-version`指定されていない場合は、一部のメタ情報のみが複製されます。

-   特定のプラットフォームからパッケージをクローンするかどうかを決定します

    特定のプラットフォーム用のパッケージのみをクローンしたい場合は、 `-os`と`-arch`使ってプラットフォームを指定します。例：

    -   Linux のクローンを作成するには、 `tiup mirror clone <target-dir> [global-version] --os=linux`コマンドを実行します。
    -   amd64 のクローンを作成するには、 `tiup mirror clone <target-dir> [global-version] --arch=amd64`コマンドを実行します。
    -   linux/amd64 のクローンを作成するには、 `tiup mirror clone <target-dir> [global-version] --os=linux --arch=amd64`コマンドを実行します。

-   パッケージの特定のバージョンをクローンするかどうかを決定します

    コンポーネントの1つのバージョンのみ（すべてのバージョンではなく）を複製したい場合は、 `--<component>=<version>`使用してそのバージョンを指定します。例：

    -   `tiup mirror clone <target-dir> --tidb v8.5.3`コマンドを実行して、TiDBコンポーネントの v8.5.3 バージョンのクローンを作成します。
    -   `tiup mirror clone <target-dir> --tidb v8.5.3 --tikv all`コマンドを実行して、TiDBコンポーネントの v8.5.3 バージョンと TiKVコンポーネントのすべてのバージョンのクローンを作成します。
    -   `tiup mirror clone <target-dir> v8.5.3`コマンドを実行して、クラスター内のすべてのコンポーネントの v8.5.3 バージョンを複製します。

クローン作成後、署名キーが自動的に設定されます。

### プライベートリポジトリを管理する {#manage-the-private-repository}

1でクローンしたリポジトリは、SCP、NFS経由でファイルを共有するか、HTTPまたはHTTPSプロトコル経由でリポジトリを公開することで、 `tiup mirror clone`のホスト間で共有できます`tiup mirror set <location>`でリポジトリの場所を指定します。

```bash
tiup mirror set /shared_data/tiup
```

```bash
tiup mirror set https://tiup-mirror.example.com/
```

> **注記：**
>
> `tiup mirror clone`実行したマシンで`tiup mirror set...`実行した場合、次に`tiup mirror clone...`実行したときに、マシンはリモートミラーではなくローカルミラーからクローンを作成します。そのため、プライベートミラーを更新する前に`tiup mirror set --reset`実行してミラーをリセットする必要があります。

ミラーを使用する別の方法は、環境変数`TIUP_MIRRORS`使用することです。以下は、プライベートリポジトリで`tiup list`実行する例です。

```bash
export TIUP_MIRRORS=/shared_data/tiup
tiup list
```

`TIUP_MIRRORS`設定ではミラー構成を永続的に変更できます（例： `tiup mirror set` ）。詳細については[ティアップ号 #651](https://github.com/pingcap/tiup/issues/651)参照してください。

### プライベートリポジトリを更新する {#update-the-private-repository}

同じ`target-dir`で`tiup mirror clone`コマンドを再度実行すると、マシンは新しいマニフェストを作成し、利用可能なコンポーネントの最新バージョンをダウンロードします。

> **注記：**
>
> マニフェストを再作成する前に、すべてのコンポーネントとバージョン (以前にダウンロードしたものも含む) が含まれていることを確認してください。

## カスタムリポジトリ {#custom-repository}

独自に構築したTiDB、TiKV、PDなどのTiDBコンポーネントを扱うためのカスタムリポジトリを作成できます。また、独自のtiupコンポーネントを作成することも可能です。

独自のコンポーネントを作成するには、 `tiup package`コマンドを実行し、 [コンポーネントのパッケージング](https://github.com/pingcap/tiup/blob/master/doc/user/package.md)指示に従って実行します。

### カスタムリポジトリを作成する {#create-a-custom-repository}

`/data/mirror`で空のリポジトリを作成するには:

```bash
tiup mirror init /data/mirror
```

リポジトリ作成の一環として、キーが`/data/mirror/keys`に書き込まれます。

`~/.tiup/keys/private.json`で新しい秘密鍵を作成するには:

```bash
tiup mirror genkey
```

秘密鍵`jdoe`に`~/.tiup/keys/private.json` `/data/mirror`所有権を付与する:

```bash
tiup mirror set /data/mirror
tiup mirror grant jdoe
```

### カスタムコンポーネントの操作 {#work-with-custom-components}

1.  hello というカスタムコンポーネントを作成します。

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

        The component `hello` version  is not installed; downloading from repository.
        Starting component `hello`: /home/dvaneeden/.tiup/components/hello/v0.0.1/hello
        hello

    `tiup mirror merge`使用すると、カスタムコンポーネントを含むリポジトリを別のリポジトリにマージできます。これは、 `/data/my_custom_components`内のすべてのコンポーネントが現在の`$USER`によって署名されていることを前提としています。

    ```bash
    $ tiup mirror set /data/my_mirror
    $ tiup mirror grant $USER
    $ tiup mirror merge /data/my_custom_components
    ```
