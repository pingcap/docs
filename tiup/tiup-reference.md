---
title: TiUP Reference
summary: TiUP は、TiDB エコシステムのパッケージ マネージャーであり、TiDB、PD、TiKV などのコンポーネントを管理します。install、list、uninstall、update、status、clean、mirror、telemetry、completion、env、help などのコマンドをサポートします。また、クラスターと TiDB データ移行 (DM) クラスターも管理します。
---

# TiUPリファレンス {#tiup-reference}

TiUP は、 TiDB エコシステムのパッケージ マネージャーとして機能します。TiDB、PD、TiKV など、TiDB エコシステム内のコンポーネントを管理します。

## 構文 {#syntax}

```shell
tiup [flags] <command> [args...]        # Executes a command
# or
tiup [flags] <component> [args...]      # Runs a component
```

`--help`コマンドを使用すると、特定のコマンドの情報を取得できます。各コマンドの概要には、そのパラメータとその使用方法が表示されます。必須パラメータは山括弧で示され、オプション パラメータは角括弧で示されます。

`<command>`コマンド名を表します。サポートされているコマンドのリストについては、以下の[コマンドリスト](#command-list)参照してください。4 `<component>`コンポーネント名を表します。サポートされているコンポーネントのリストについては、以下の[コンポーネントリスト](#component-list)参照してください。

## オプション {#options}

### - バイナリ {#binary}

-   このオプションを有効にすると、指定されたバイナリ ファイルのパスが印刷されます。

    -   `tiup --binary <component>`実行すると、最新の安定版がインストールされた`<component>`コンポーネントのパスが出力されます。5 `<component>`インストールされていない場合は、エラーが返されます。
    -   `tiup --binary <component>:<version>`実行すると、インストールされた`<component>`コンポーネントの`<version>`のパスが出力されます。この`<version>`が出力されない場合は、エラーが返されます。

-   データ型: `BOOLEAN`

-   このオプションはデフォルトでは無効になっており、デフォルト値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにします。

> **注記：**
>
> このオプションは、 `tiup [flags] <component> [args...]`形式のコマンドでのみ使用できます。

### --binパス {#binpath}

> **注記：**
>
> このオプションは、 `tiup [flags] <component> [args...]`形式のコマンドでのみ使用できます。

-   実行するコンポーネントのパスを指定します。コンポーネントの実行時に、 TiUPミラー内のバイナリ ファイルを使用しない場合は、このオプションを追加して、カスタム パス内のバイナリ ファイルを使用するように指定できます。
-   データ型: `STRING`

### -T, --タグ {#t-tag}

-   開始するコンポーネントのタグを指定します。一部のコンポーネントは実行中にディスクstorageを使用する必要があり、 TiUP はこの実行用に一時storageディレクトリを割り当てます。TiUPで固定ディレクトリを割り当てる場合は、 `-T/--tag`使用してディレクトリ名を指定します。これにより、同じタグを使用して複数の実行で同じファイルのバッチを読み書きできます。
-   データ型: `STRING`

### -v, --バージョン {#v-version}

TiUPバージョンを印刷します。

### - ヘルプ {#help}

ヘルプ情報を出力します。

## コマンドリスト {#command-list}

TiUP には複数のコマンドがあり、これらのコマンドには複数のサブコマンドがあります。特定のコマンドとその詳細な説明については、以下のリストの対応するリンクをクリックしてください。

-   [インストール](/tiup/tiup-command-install.md) :コンポーネントをインストールします。
-   [リスト](/tiup/tiup-command-list.md) :コンポーネントリストを表示します。
-   [アンインストール](/tiup/tiup-command-uninstall.md) :コンポーネントをアンインストールします。
-   [アップデート](/tiup/tiup-command-update.md) : インストールされているコンポーネントを更新します。
-   [状態](/tiup/tiup-command-status.md) :コンポーネントの実行ステータスを表示します。
-   [クリーン](/tiup/tiup-command-clean.md) :コンポーネントのデータディレクトリをクリーンアップします。
-   [鏡](/tiup/tiup-command-mirror.md) : ミラーを管理します。
-   [テレメトリー](/tiup/tiup-command-telemetry.md) : テレメトリを有効または無効にします。
-   [完了](/tiup/tiup-command-completion.md) : TiUPコマンドを完了します。
-   [環境](/tiup/tiup-command-env.md) : TiUP関連の環境変数を表示します。
-   [ヘルプ](/tiup/tiup-command-help.md) : コマンドまたはコンポーネントのヘルプ情報を表示します。

## コンポーネントリスト {#component-list}

-   [クラスタ](/tiup/tiup-component-cluster.md) :本番環境で TiDB クラスターを管理します。
-   [dm](/tiup/tiup-component-dm.md) :本番環境で TiDB データ移行 (DM) クラスターを管理します。
