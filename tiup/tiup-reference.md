---
title: TiUP Reference
---

# TiUPリファレンス {#tiup-reference}

TiUP は、 TiDB エコシステムのパッケージ マネージャーとして機能します。 TiDB、PD、TiKV などの TiDB エコシステムのコンポーネントを管理します。

## 構文 {#syntax}

```shell
tiup [flags] <command> [args...]        # Executes a command
# or
tiup [flags] <component> [args...]      # Runs a component
```

`--help`コマンドを使用して、特定のコマンドの情報を取得できます。各コマンドの概要には、そのパラメーターとその使用法が表示されます。必須パラメーターは山括弧で示され、オプションのパラメーターは角括弧で示されます。

`<command>`コマンド名を表します。サポートされているコマンドのリストについては、以下の[コマンド一覧](#command-list)を参照してください。 `<component>`コンポーネント名を表します。サポートされているコンポーネントのリストについては、以下の[コンポーネントリスト](#component-list)を参照してください。

## オプション {#options}

### - バイナリ {#binary}

-   このオプションを有効にすると、指定したバイナリ ファイル パスが出力されます。

    -   `tiup --binary <component>`を実行すると、インストールされた最新の安定した`<component>`コンポーネントのパスが表示されます。 `<component>`がインストールされていない場合は、エラーが返されます。
    -   `tiup --binary <component>:<version>`を実行すると、インストールされた`<component>`コンポーネントの`<version>`パスが表示されます。この`<version>`が出力されない場合、エラーが返されます。

-   データ型: `BOOLEAN`

-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を何も渡さないようにします。

> **ノート：**
>
> このオプションは、 `tiup [flags] <component> [args...]`形式のコマンドでのみ使用できます。

### --binpath {#binpath}

> **ノート：**
>
> このオプションは、 `tiup [flags] <component> [args...]`形式のコマンドでのみ使用できます。

-   実行するコンポーネントのパスを指定します。コンポーネント実行時にTiUPミラーのバイナリファイルを使用したくない場合、このオプションを追加することでカスタムパスのバイナリファイルを使用するように指定できます。
-   データ型: `STRING`

### -T, --タグ {#t-tag}

-   開始するコンポーネントのタグを指定します。一部のコンポーネントは実行中にディスクstorageを使用する必要があり、 TiUP はこの実行のために一時的なstorageディレクトリを割り当てます。 TiUPに固定ディレクトリを割り当てる場合は、 `-T/--tag`を使用してディレクトリの名前を指定できます。これにより、同じファイルのバッチを同じタグで複数の実行で読み書きできるようになります。
-   データ型: `STRING`

### -v, --version {#v-version}

TiUP のバージョンを出力します。

### - ヘルプ {#help}

ヘルプ情報を出力します。

## コマンド一覧 {#command-list}

TiUPには複数のコマンドがあり、これらのコマンドには複数のサブコマンドがあります。特定のコマンドとその詳細な説明については、以下のリストの対応するリンクをクリックしてください。

-   [インストール](/tiup/tiup-command-install.md) :コンポーネントをインストールします。
-   [リスト](/tiup/tiup-command-list.md) :コンポーネントリストを表示します。
-   [アンインストール](/tiup/tiup-command-uninstall.md) :コンポーネントをアンインストールします。
-   [アップデート](/tiup/tiup-command-update.md) : インストールされたコンポーネントを更新します。
-   [スターテス](/tiup/tiup-command-status.md) :コンポーネントの実行ステータスを示します。
-   [綺麗](/tiup/tiup-command-clean.md) :コンポーネントのデータ ディレクトリを消去します。
-   [鏡](/tiup/tiup-command-mirror.md) : ミラーを管理します。
-   [テレメトリー](/tiup/tiup-command-telemetry.md) : テレメトリを有効または無効にします。
-   [完了](/tiup/tiup-command-completion.md) : TiUPコマンドを完了します。
-   [環境](/tiup/tiup-command-env.md) : TiUP関連の環境変数を表示します。
-   [ヘルプ](/tiup/tiup-command-help.md) : コマンドまたはコンポーネントのヘルプ情報を表示します。

## コンポーネントリスト {#component-list}

-   [集まる](/tiup/tiup-component-cluster.md) :本番環境で TiDB クラスターを管理します。
-   [dm](/tiup/tiup-component-dm.md) :本番環境で TiDB データ移行 (DM) クラスターを管理します。
