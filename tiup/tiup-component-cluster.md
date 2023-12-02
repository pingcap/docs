---
title: TiUP Cluster
---

# TiUPクラスタ {#tiup-cluster}

TiUP クラスタ は、 Golangで書かれたTiUPのクラスター管理コンポーネントです。 TiUPクラスタコンポーネントを使用すると、展開、起動、シャットダウン、破棄、エラスティック スケーリング、TiDB クラスターのアップグレード、TiDB クラスター パラメーターの管理などの日常の操作とメンテナンスを実行できます。

## 構文 {#syntax}

```shell
tiup cluster [command] [flags]
```

`[command]`はコマンドの名前です。サポートされているコマンドについては、以下の[コマンドリスト](#command-list)を参照してください。

## オプション {#options}

### --ssh {#ssh}

-   コマンドを実行するためにリモート エンド (TiDB サービスがデプロイされているマシン) に接続する SSH クライアントを指定します。

-   データ型: `STRING`

-   サポートされている値:

    -   `builtin` : tiup-clusterに組み込まれている easyssh クライアントを SSH クライアントとして使用します。
    -   `system` : 現在のオペレーティング システムのデフォルトの SSH クライアントを使用します。
    -   `none` : SSH クライアントは使用されません。デプロイメントは現在のマシンのみに対して行われます。

-   コマンド内でこのオプションが指定されていない場合、デフォルト値として`builtin`が使用されます。

### --ssh-タイムアウト {#ssh-timeout}

-   SSH 接続のタイムアウトを秒単位で指定します。
-   データ型: `UINT`
-   このオプションがコマンドで指定されていない場合、デフォルトのタイムアウトは`5`秒です。

### --待機タイムアウト {#wait-timeout}

-   操作プロセスの各ステップの最大待機時間を秒単位で指定します。操作プロセスは、systemctl を指定してサービスを開始または停止したり、ポートがオンラインまたはオフラインになるのを待機したりするなど、多くのステップで構成されます。各ステップには数秒かかる場合があります。ステップの実行時間が指定されたタイムアウトを超えると、ステップはエラーで終了します。
-   データ型: `UINT`
-   コマンドでこのオプションを指定しない場合、各ステップの最大待ち時間は`120`秒です。

### -y、--はい {#y-yes}

-   すべての危険な操作の二次確認をスキップします。スクリプトを使用してTiUPを呼び出す場合を除き、このオプションの使用はお勧めできません。
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

### -v、--バージョン {#v-version}

-   TiUP クラスタの現在のバージョンを出力します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

### -h, --help {#h-help}

-   関連するコマンドのヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

## コマンド一覧 {#command-list}

-   [輸入](/tiup/tiup-component-cluster-import.md) : Ansible によってデプロイされたクラスターをインポートします
-   [テンプレート](/tiup/tiup-component-cluster-template.md) : トポロジテンプレートを出力します。
-   [チェック](/tiup/tiup-component-cluster-check.md) : デプロイメントの前後にクラスターをチェックします。
-   [展開する](/tiup/tiup-component-cluster-deploy.md) : 指定されたトポロジに基づいてクラスターをデプロイします
-   [リスト](/tiup/tiup-component-cluster-list.md) : デプロイされたクラスターのリストをクエリします。
-   [画面](/tiup/tiup-component-cluster-display.md) : 指定されたクラスターのステータスを表示します。
-   [始める](/tiup/tiup-component-cluster-start.md) : 指定されたクラスターを開始します
-   [停止](/tiup/tiup-component-cluster-stop.md) : 指定されたクラスターを停止します
-   [再起動](/tiup/tiup-component-cluster-restart.md) : 指定されたクラスターを再起動します
-   [スケールイン](/tiup/tiup-component-cluster-scale-in.md) : 指定されたクラスター内でスケーリングします
-   [規格外](/tiup/tiup-component-cluster-scale-out.md) : 指定されたクラスターをスケールアウトします。
-   [アップグレード](/tiup/tiup-component-cluster-upgrade.md) : 指定されたクラスターをアップグレードします
-   [プルーン](/tiup/tiup-component-cluster-prune.md) : 指定されたクラスターの廃棄状態のインスタンスをクリーンアップします。
-   [編集構成](/tiup/tiup-component-cluster-edit-config.md) : 指定されたクラスターの構成を変更します
-   [リロード](/tiup/tiup-component-cluster-reload.md) : 指定されたクラスターの構成を再ロードします
-   [パッチ](/tiup/tiup-component-cluster-patch.md) : デプロイされたクラスター内のサービスを置き換えます
-   [名前を変更する](/tiup/tiup-component-cluster-rename.md) : クラスターの名前を変更します
-   [クリーン](/tiup/tiup-component-cluster-clean.md) : 指定されたクラスターからデータを削除します
-   [破壊する](/tiup/tiup-component-cluster-destroy.md) : 指定されたクラスターを破棄します
-   [監査](/tiup/tiup-component-cluster-audit.md) : 指定されたクラスターの操作監査ログを照会します。
-   [リプレイ](/tiup/tiup-component-cluster-replay.md) : 指定されたコマンドを再試行します
-   [有効にする](/tiup/tiup-component-cluster-enable.md) : マシンの再起動後にクラスターサービスの自動有効化を有効にします。
-   [無効にする](/tiup/tiup-component-cluster-disable.md) : マシンの再起動後のクラスターサービスの自動有効化を無効にします。
-   [メタバックアップ](/tiup/tiup-component-cluster-meta-backup.md) : 指定されたクラスターの運用と保守に必要なTiUPメタ ファイルをバックアップします。
-   [メタ復元](/tiup/tiup-component-cluster-meta-restore.md) : 指定されたクラスターのTiUPメタ ファイルを復元します
-   [ヘルプ](/tiup/tiup-component-cluster-help.md) : ヘルプ情報を出力。

[&lt;&lt; 前のページに戻る - TiUPリファレンスコンポーネントリスト](/tiup/tiup-reference.md#component-list)
