---
title: TiUP DM
summary: TiUP DMは、DMクラスタの管理（デプロイ、起動、停止、破棄、スケーリング、アップグレード、構成パラメータの管理など）に使用されます。SSH、タイムアウト、確認のスキップ、バージョン情報の表示、ヘルプ情報などのオプションをサポートしています。サポートされるコマンドは、import、template、deploy、list、display、start、stop、restart、scale-in、scale-out、upgrade、prune、edit-config、reload、patch、destroy、audit、replay、enable、disable、helpです。
---

# TiUP DM {#tiup-dm}

TiDBクラスタの管理に使用される[TiUPクラスタ](/tiup/tiup-component-cluster.md)と同様に、 TiUP DMはDMクラスタの管理に使用されます。TiUP TiUP DMコンポーネントを使用すると、DMクラスタのデプロイ、起動、停止、破棄、エラスティックスケーリング、DMクラスタのアップグレード、DMクラスタの構成パラメータの管理など、DMクラスタの日常的な運用および保守タスクを実行できます。

## 構文 {#syntax}

```shell
tiup dm [command] [flags]
```

`[command]`コマンド名を渡すために使用されます。サポートされているコマンドについては[コマンドリスト](#command-list)参照してください。

## オプション {#options}

### --ssh {#ssh}

-   コマンド実行のためにリモート エンド (TiDB サービスがデプロイされているマシン) に接続する SSH クライアントを指定します。

-   データ型: `STRING`

-   サポート値:

    -   `builtin` : tiup-clusterの組み込み easyssh クライアントを SSH クライアントとして使用します。
    -   `system` : 現在のオペレーティング システムのデフォルトの SSH クライアントを使用します。
    -   `none` : SSHクライアントは使用されません。デプロイメントは現在のマシンのみに適用されます。

-   コマンドでこのオプションを指定しない場合は、デフォルト値として`builtin`使用されます。

### --sshタイムアウト {#ssh-timeout}

-   SSH 接続のタイムアウトを秒単位で指定します。
-   データ型: `UINT`
-   コマンドでこのオプションを指定しない場合、デフォルトのタイムアウトは`5`秒になります。

### --wait-timeout {#wait-timeout}

-   操作プロセスの各ステップの最大待機時間（秒単位）を指定します。操作プロセスは、systemctl によるサービスの開始または停止の指定、ポートのオンラインまたはオフラインの待機など、多くのステップで構成されます。各ステップは数秒かかる場合があります。ステップの実行時間が指定されたタイムアウトを超えた場合、そのステップはエラーで終了します。
-   データ型: `UINT`
-   コマンドでこのオプションを指定しない場合、各ステップの最大待機時間は`120`秒になります。

### -y, --はい {#y-yes}

-   すべてのリスクのある操作の2次確認をスキップします。スクリプトを使用してTiUPを呼び出す場合を除き、このオプションの使用は推奨されません。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### -v, --バージョン {#v-version}

-   TiUP DMの現在のバージョンを印刷します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### -h, --help {#h-help}

-   指定されたコマンドに関するヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

## コマンドリスト {#command-list}

-   [輸入](/tiup/tiup-component-dm-import.md) : DM-Ansible によってデプロイされた DM v1.0 クラスターをインポートします。
-   [テンプレート](/tiup/tiup-component-dm-template.md) : トポロジ テンプレートを出力します。
-   [展開する](/tiup/tiup-component-dm-deploy.md) : 指定されたトポロジに基づいてクラスターをデプロイします。
-   [リスト](/tiup/tiup-component-dm-list.md) : デプロイされたクラスターのリストを照会します。
-   [画面](/tiup/tiup-component-dm-display.md) : 指定されたクラスターのステータスを表示します。
-   [始める](/tiup/tiup-component-dm-start.md) : 指定されたクラスターを起動します。
-   [停止](/tiup/tiup-component-dm-stop.md) : 指定されたクラスターを停止します。
-   [再起動](/tiup/tiup-component-dm-restart.md) : 指定されたクラスターを再起動します。
-   [スケールイン](/tiup/tiup-component-dm-scale-in.md) : 指定されたクラスター内でスケールします。
-   [スケールアウト](/tiup/tiup-component-dm-scale-out.md) : 指定されたクラスターをスケールアウトします。
-   [アップグレード](/tiup/tiup-component-dm-upgrade.md) : 指定されたクラスターをアップグレードします。
-   [プルーン](/tiup/tiup-component-dm-prune.md) : 指定されたクラスターの Tombstone ステータスのインスタンスをクリーンアップします。
-   [編集設定](/tiup/tiup-component-dm-edit-config.md) : 指定されたクラスターの構成を変更します。
-   [リロード](/tiup/tiup-component-dm-reload.md) : 指定されたクラスターの構成を再読み込みします。
-   [パッチ](/tiup/tiup-component-dm-patch.md) : デプロイされたクラスター内の指定されたサービスを置き換えます。
-   [破壊する](/tiup/tiup-component-dm-destroy.md) : 指定されたクラスターを破棄します。
-   [監査](/tiup/tiup-component-dm-audit.md) : 指定されたクラスターの操作監査ログを照会します。
-   [リプレイ](/tiup/tiup-component-dm-replay.md) : 指定されたコマンドを再生する
-   [有効にする](/tiup/tiup-component-dm-enable.md) : マシンの再起動後にクラスター サービスを自動的に有効化します。
-   [無効にする](/tiup/tiup-component-dm-disable.md) : マシンの再起動後にクラスター サービスの自動有効化を無効にします。
-   [ヘルプ](/tiup/tiup-component-dm-help.md) : ヘルプ情報を出力します。

[&lt;&lt; 前のページに戻る - TiUP参照コンポーネントリスト](/tiup/tiup-reference.md#component-list)
