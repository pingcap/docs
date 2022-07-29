---
title: TiUP DM
---

# TiUP DM {#tiup-dm}

TiDBクラスターの管理に使用される[TiUPクラスター](/tiup/tiup-component-cluster.md)と同様に、 TiUP DMはDMクラスターの管理に使用されます。 TiUP DMコンポーネントを使用して、DMクラスターの展開、開始、停止、破棄、エラスティックスケーリング、DMクラスターのアップグレード、DMクラスターの構成パラメーターの管理など、DMクラスターの日常の操作および保守タスクを実行できます。

## 構文 {#syntax}

```shell
tiup dm [command] [flags]
```

`[command]`は、コマンドの名前を渡すために使用されます。サポートされているコマンドについては、 [コマンドリスト](#command-list)を参照してください。

## オプション {#options}

### --ssh {#ssh}

-   コマンド実行のためにリモートエンド（TiDBサービスが展開されているマシン）に接続するSSHクライアントを指定します。

-   データ型： `STRING`

-   サポート値：

    -   `builtin` ：SSHクライアントとしてtiup-clusterの組み込みeasysshクライアントを使用します。
    -   `system` ：現在のオペレーティングシステムのデフォルトのSSHクライアントを使用します。
    -   `none` ：SSHクライアントは使用されません。展開は、現在のマシンのみを対象としています。

-   このオプションがコマンドで指定されていない場合、デフォルト値として`builtin`が使用されます。

### --ssh-timeout {#ssh-timeout}

-   SSH接続タイムアウトを秒単位で指定します。
-   データ型： `UINT`
-   このオプションがコマンドで指定されていない場合、デフォルトのタイムアウトは`5`秒です。

### --wait-timeout {#wait-timeout}

-   操作プロセスの各ステップの最大待機時間（秒単位）を指定します。操作プロセスは、サービスを開始または停止するようにsystemctlを指定する、ポートがオンラインまたはオフラインになるのを待つなど、多くのステップで構成されます。各ステップには数秒かかる場合があります。ステップの実行時間が指定されたタイムアウトを超えると、ステップはエラーで終了します。
-   データ型： `UINT`
-   このオプションがコマンドで指定されていない場合、各ステップの最大待機時間は`120`秒です。

### -y、-yes {#y-yes}

-   すべての危険な操作の二次確認をスキップします。スクリプトを使用してTiUPを呼び出す場合を除いて、このオプションを使用することはお勧めしません。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

### -v、-version {#v-version}

-   TiUP DMの現在のバージョンを出力します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

### -h, --help {#h-help}

-   指定されたコマンドに関するヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

## コマンドリスト {#command-list}

-   [輸入](/tiup/tiup-component-dm-import.md) ：DM-AnsibleによってデプロイされたDMv1.0クラスタをインポートします。
-   [テンプレート](/tiup/tiup-component-dm-template.md) ：トポロジーテンプレートを出力します。
-   [配備](/tiup/tiup-component-dm-deploy.md) ：指定されたトポロジに基づいてクラスタをデプロイします。
-   [リスト](/tiup/tiup-component-dm-list.md) ：デプロイされたクラスターのリストを照会します。
-   [画面](/tiup/tiup-component-dm-display.md) ：指定したクラスタの状態を表示します。
-   [始める](/tiup/tiup-component-dm-start.md) ：指定されたクラスタを開始します。
-   [止まる](/tiup/tiup-component-dm-stop.md) ：指定したクラスタを停止します。
-   [再起動](/tiup/tiup-component-dm-restart.md) ：指定したクラスタを再起動します。
-   [スケールイン](/tiup/tiup-component-dm-scale-in.md) ：指定されたクラスタでスケーリングします。
-   [規格外](/tiup/tiup-component-dm-scale-out.md) ：指定されたクラスタをスケールアウトします。
-   [アップグレード](/tiup/tiup-component-dm-upgrade.md) ：指定されたクラスタをアップグレードします。
-   [プルーン](/tiup/tiup-component-dm-prune.md) ：指定されたクラスタのトゥームストーンステータスのインスタンスをクリーンアップします。
-   [edit-config](/tiup/tiup-component-dm-edit-config.md) ：指定したクラスタの構成を変更します。
-   [リロード](/tiup/tiup-component-dm-reload.md) ：指定されたクラスタの構成を再ロードします。
-   [パッチ](/tiup/tiup-component-dm-patch.md) ：デプロイされたクラスタの指定されたサービスを置き換えます。
-   [破壊する](/tiup/tiup-component-dm-destroy.md) ：指定されたクラスタを破棄します。
-   [監査](/tiup/tiup-component-dm-audit.md) ：指定されたクラスタの操作監査ログを照会します。
-   [リプレイ](/tiup/tiup-component-dm-replay.md) ：指定したコマンドを再生します
-   [有効](/tiup/tiup-component-dm-enable.md) ：マシンの再起動後にクラスタサービスの自動有効化を有効にします。
-   [無効にする](/tiup/tiup-component-dm-disable.md) ：マシンの再起動後、クラスタサービスの自動有効化を無効にします。
-   [ヘルプ](/tiup/tiup-component-dm-help.md) ：ヘルプ情報を出力します。

[&lt;&lt;前のページに戻る-TiUPリファレンスコンポーネントリスト](/tiup/tiup-reference.md#component-list)
