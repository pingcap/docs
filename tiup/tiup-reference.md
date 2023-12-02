---
title: TiUP Reference
---

# TiUPリファレンス {#tiup-reference}

TiUP は、 TiDB エコシステムのパッケージ マネージャーとして機能します。 TiDB、PD、TiKV などの TiDB エコシステム内のコンポーネントを管理します。

## 構文 {#syntax}

```shell
tiup [flags] <command> [args...]        # Executes a command
# or
tiup [flags] <component> [args...]      # Runs a component
```

`--help`コマンドを使用すると、特定のコマンドの情報を取得できます。各コマンドの概要には、そのパラメーターとその使用法が示されています。必須パラメータは山括弧内に示され、オプションのパラメータは角括弧内に示されます。

`<command>`コマンド名を表します。サポートされているコマンドのリストについては、以下の[コマンド一覧](#command-list)を参照してください。 `<component>`コンポーネント名を表します。サポートされているコンポーネントのリストについては、以下の[コンポーネントリスト](#component-list)を参照してください。

## オプション {#options}

### - バイナリ {#binary}

-   このオプションを有効にすると、指定されたバイナリ ファイルのパスが出力されます。

    -   `tiup --binary <component>`を実行すると、最新の安定してインストールされた`<component>`コンポーネントのパスが出力されます。 `<component>`がインストールされていない場合は、エラーが返されます。
    -   `tiup --binary <component>:<version>`を実行すると、インストールされている`<component>`コンポーネントの`<version>`パスが出力されます。この`<version>`が出力されない場合は、エラーが返されます。

-   データ型: `BOOLEAN`

-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加して、値`true`渡すか、値を渡さないことができます。

> **注記：**
>
> このオプションは`tiup [flags] <component> [args...]`形式のコマンドでのみ使用できます。

### --binpath {#binpath}

> **注記：**
>
> このオプションは`tiup [flags] <component> [args...]`形式のコマンドでのみ使用できます。

-   実行するコンポーネントのパスを指定します。コンポーネントの実行時に、 TiUPミラー内のバイナリ ファイルを使用したくない場合は、このオプションを追加して、カスタム パス内のバイナリ ファイルの使用を指定できます。
-   データ型: `STRING`

### -T、--タグ {#t-tag}

-   起動するコンポーネントのタグを指定します。一部のコンポーネントは実行中にディスクstorageを使用する必要があり、 TiUP はこの実行用に一時storageディレクトリを割り当てます。 TiUPに固定のディレクトリを割り当てたい場合は、 `-T/--tag`を使用してディレクトリの名前を指定すると、同じタグを使用して複数の実行で同じファイルのバッチを読み書きできるようになります。
-   データ型: `STRING`

### -v、--バージョン {#v-version}

TiUP のバージョンを出力します。

### - ヘルプ {#help}

ヘルプ情報を印刷します。

## コマンド一覧 {#command-list}

TiUPには複数のコマンドがあり、これらのコマンドには複数のサブコマンドがあります。特定のコマンドとその詳細な説明については、以下のリスト内の対応するリンクをクリックしてください。

-   [インストール](/tiup/tiup-command-install.md) :コンポーネントをインストールします。
-   [リスト](/tiup/tiup-command-list.md) :コンポーネントリストを表示します。
-   [アンインストール](/tiup/tiup-command-uninstall.md) :コンポーネントをアンインストールします。
-   [アップデート](/tiup/tiup-command-update.md) : インストールされているコンポーネントを更新します。
-   [状態](/tiup/tiup-command-status.md) :コンポーネントの実行ステータスを示します。
-   [クリーン](/tiup/tiup-command-clean.md) :コンポーネントのデータ ディレクトリをクリーンアップします。
-   [鏡](/tiup/tiup-command-mirror.md) : ミラーを管理します。
-   [テレメトリー](/tiup/tiup-command-telemetry.md) : テレメトリを有効または無効にします。
-   [完了](/tiup/tiup-command-completion.md) : TiUPコマンドを完了します。
-   [環境](/tiup/tiup-command-env.md) : TiUP関連の環境変数を表示します。
-   [ヘルプ](/tiup/tiup-command-help.md) : コマンドまたはコンポーネントのヘルプ情報を表示します。

## コンポーネントリスト {#component-list}

-   [集まる](/tiup/tiup-component-cluster.md) :本番環境で TiDB クラスターを管理します。
-   [DMで](/tiup/tiup-component-dm.md) :本番環境で TiDB Data Migration (DM) クラスターを管理します。
