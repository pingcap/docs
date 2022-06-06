---
title: TiUP Reference
---

# TiUPリファレンス {#tiup-reference}

TiUPは、TiDBエコシステムのパッケージマネージャーとして機能します。 TiDB、PD、TiKVなどのTiDBエコシステムのコンポーネントを管理します。

## 構文 {#syntax}

```shell
tiup [flags] <command> [args...]        # Executes a command
# or
tiup [flags] <component> [args...]      # Runs a component
```

`--help`コマンドを使用して、特定のコマンドの情報を取得できます。各コマンドの要約には、そのパラメーターとその使用法が示されています。必須パラメーターは山括弧で示され、オプションパラメーターは角括弧で示されます。

`<command>`はコマンド名を表します。サポートされているコマンドのリストについては、以下の[コマンドリスト](#command-list)を参照してください。 `<component>`はコンポーネント名を表します。サポートされているコンポーネントのリストについては、以下の[コンポーネントリスト](#component-list)を参照してください。

## オプション {#options}

### -B、-binary {#b-binary}

-   このオプションを有効にすると、指定したバイナリファイルパスが出力されます。

    -   `tiup -B/--binary <component>`を実行すると、最新の安定してインストールされた`<component>`コンポーネントのパスが印刷されます。 `<component>`がインストールされていない場合、エラーが返されます。
    -   `tiup -B/--binary <component>:<version>`を実行すると、インストールされている`<component>`のコンポーネントの`<version>`のパスが出力されます。この`<version>`が印刷されない場合、エラーが返されます。

-   データ型： `BOOLEAN`

-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、 `true`の値を渡すか、値を渡さないようにします。

> **ノート：**
>
> このオプションは、 `tiup [flags] <component> [args...]`形式のコマンドでのみ使用できます。

### --binpath {#binpath}

> **ノート：**
>
> このオプションは、 `tiup [flags] <component> [args...]`形式のコマンドでのみ使用できます。

-   実行するコンポーネントのパスを指定します。コンポーネントの実行時に、TiUPミラーでバイナリファイルを使用したくない場合は、このオプションを追加して、カスタムパスでバイナリファイルを使用するように指定できます。
-   データ型： `STRING`

### --skip-version-check {#skip-version-check}

> **ノート：**
>
> このオプションは、v1.3.0以降廃止されました。

-   バージョン番号の有効性チェックをスキップします。デフォルトでは、指定されたバージョン番号はセマンティックバージョンのみになります。
-   データ型： `BOOLEAN`
-   このオプションはデフォルトで無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、 `true`の値を渡すか、値を渡さないようにします。

### -T、-tag {#t-tag}

-   開始するコンポーネントのタグを指定します。一部のコンポーネントは実行中にディスクストレージを使用する必要があり、TiUPはこの実行のために一時ストレージディレクトリを割り当てます。 TiUPに固定ディレクトリを割り当てたい場合は、 `-T/--tag`を使用してディレクトリの名前を指定し、同じタグを使用して同じバッチのファイルを複数回実行して読み書きできるようにすることができます。
-   データ型： `STRING`

### -v、-version {#v-version}

TiUPバージョンを印刷します。

### - ヘルプ {#help}

ヘルプ情報を出力します。

## コマンドリスト {#command-list}

TiUPには複数のコマンドがあり、これらのコマンドには複数のサブコマンドがあります。特定のコマンドとその詳細な説明については、以下のリストにある対応するリンクをクリックしてください。

-   [インストール](/tiup/tiup-command-install.md) ：コンポーネントをインストールします。
-   [リスト](/tiup/tiup-command-list.md) ：コンポーネントリストを表示します。
-   [アンインストール](/tiup/tiup-command-uninstall.md) ：コンポーネントをアンインストールします。
-   [アップデート](/tiup/tiup-command-update.md) ：インストールされているコンポーネントを更新します。
-   [状態](/tiup/tiup-command-status.md) ：コンポーネントの実行ステータスを示します。
-   [掃除](/tiup/tiup-command-clean.md) ：コンポーネントのデータディレクトリをクリーンアップします。
-   [鏡](/tiup/tiup-command-mirror.md) ：ミラーを管理します。
-   [テレメトリー](/tiup/tiup-command-telemetry.md) ：テレメトリを有効または無効にします。
-   [完了](/tiup/tiup-command-completion.md) ：TiUPコマンドを完了します。
-   [環境](/tiup/tiup-command-env.md) ：TiUP関連の環境変数を表示します。
-   [ヘルプ](/tiup/tiup-command-help.md) ：コマンドまたはコンポーネントのヘルプ情報を表示します。

## コンポーネントリスト {#component-list}

-   [クラスタ](/tiup/tiup-component-cluster.md) ：実稼働環境でTiDBクラスタを管理します。
-   [dm](/tiup/tiup-component-dm.md) ：実稼働環境でTiDBデータ移行（DM）クラスタを管理します。
