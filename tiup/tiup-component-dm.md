---
title: TiUP DM
---

# TiUP DM {#tiup-dm}

TiDB クラスターの管理に使用される[TiUPクラスタ](/tiup/tiup-component-cluster.md)と同様に、 TiUP DM はDM クラスターの管理に使用されます。 TiUP DMコンポーネントを使用すると、DM クラスターの展開、開始、停止、破棄、エラスティック スケーリング、DM クラスターのアップグレード、DM クラスターの構成パラメーターの管理など、DM クラスターの日常的な運用およびメンテナンス タスクを実行できます。

## 構文 {#syntax}

```shell
tiup dm [command] [flags]
```

`[command]`はコマンドの名前を渡すために使用されます。サポートされているコマンドについては、 [コマンド一覧](#command-list)を参照してください。

## オプション {#options}

### --ssh {#ssh}

-   コマンドを実行するためにリモート エンド (TiDB サービスがデプロイされているマシン) に接続する SSH クライアントを指定します。

-   データ型: `STRING`

-   サポート値:

    -   `builtin` : tiup-clusterの組み込み easyssh クライアントを SSH クライアントとして使用します。
    -   `system` : 現在のオペレーティング システムのデフォルトの SSH クライアントを使用します。
    -   `none` : SSH クライアントは使用されません。デプロイメントは現在のマシンのみに対して行われます。

-   コマンド内でこのオプションが指定されていない場合は、デフォルト値として`builtin`が使用されます。

### --ssh-タイムアウト {#ssh-timeout}

-   SSH 接続のタイムアウトを秒単位で指定します。
-   データ型: `UINT`
-   このオプションがコマンドで指定されていない場合、デフォルトのタイムアウトは`5`秒です。

### --待機タイムアウト {#wait-timeout}

-   操作プロセスの各ステップの最大待機時間を秒単位で指定します。操作プロセスは、systemctl を指定してサービスを開始または停止したり、ポートがオンラインまたはオフラインになるのを待機したりするなど、多くのステップで構成されます。各ステップには数秒かかる場合があります。ステップの実行時間が指定されたタイムアウトを超えると、ステップはエラーで終了します。
-   データ型: `UINT`
-   コマンドでこのオプションを指定しない場合、各ステップの最大待ち時間は`120`秒です。

### -y、--はい {#y-yes}

-   すべての危険な操作の二次確認をスキップします。スクリプトを使用してTiUP を呼び出す場合を除き、このオプションを使用することはお勧めできません。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

### -v、--バージョン {#v-version}

-   TiUP DMの現在のバージョンを出力します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

### -h, --help {#h-help}

-   指定されたコマンドに関するヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、値`false`を指定するとデフォルトで無効になります。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を渡しません。

## コマンド一覧 {#command-list}

-   [輸入](/tiup/tiup-component-dm-import.md) : DM-Ansible によってデプロイされた DM v1.0 クラスターをインポートします。
-   [テンプレート](/tiup/tiup-component-dm-template.md) : トポロジテンプレートを出力します。
-   [展開する](/tiup/tiup-component-dm-deploy.md) : 指定されたトポロジに基づいてクラスターをデプロイします。
-   [リスト](/tiup/tiup-component-dm-list.md) : デプロイされたクラスターのリストを照会します。
-   [画面](/tiup/tiup-component-dm-display.md) : 指定したクラスターの状態を表示します。
-   [始める](/tiup/tiup-component-dm-start.md) : 指定されたクラスターを開始します。
-   [停止](/tiup/tiup-component-dm-stop.md) : 指定されたクラスターを停止します。
-   [再起動](/tiup/tiup-component-dm-restart.md) : 指定されたクラスターを再起動します。
-   [スケールイン](/tiup/tiup-component-dm-scale-in.md) : 指定されたクラスター内でスケールします。
-   [規格外](/tiup/tiup-component-dm-scale-out.md) : 指定されたクラスターをスケールアウトします。
-   [アップグレード](/tiup/tiup-component-dm-upgrade.md) : 指定されたクラスターをアップグレードします。
-   [プルーン](/tiup/tiup-component-dm-prune.md) : 指定されたクラスターの廃棄状態のインスタンスをクリーンアップします。
-   [編集構成](/tiup/tiup-component-dm-edit-config.md) : 指定されたクラスターの構成を変更します。
-   [リロード](/tiup/tiup-component-dm-reload.md) : 指定されたクラスターの構成を再ロードします。
-   [パッチ](/tiup/tiup-component-dm-patch.md) : デプロイされたクラスター内の指定されたサービスを置き換えます。
-   [破壊する](/tiup/tiup-component-dm-destroy.md) : 指定されたクラスターを破棄します。
-   [監査](/tiup/tiup-component-dm-audit.md) : 指定したクラスターの操作監査ログを照会します。
-   [リプレイ](/tiup/tiup-component-dm-replay.md) : 指定されたコマンドを再生します
-   [有効にする](/tiup/tiup-component-dm-enable.md) : マシンの再起動後のクラスター サービスの自動有効化を有効にします。
-   [無効にする](/tiup/tiup-component-dm-disable.md) : マシンの再起動後のクラスター サービスの自動有効化を無効にします。
-   [ヘルプ](/tiup/tiup-component-dm-help.md) : ヘルプ情報を出力します。

[&lt;&lt; 前のページに戻る - TiUPリファレンスコンポーネントリスト](/tiup/tiup-reference.md#component-list)
