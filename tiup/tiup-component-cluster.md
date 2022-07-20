---
title: TiUP Cluster
---

# TiUPクラスター {#tiup-cluster}

TiUP Clusterは、Golangで記述されたTiUPのクラスタ管理コンポーネントです。 TiUPクラスターコンポーネントを使用して、展開、開始、シャットダウン、破棄、エラスティックスケーリング、TiDBクラスターのアップグレード、TiDBクラスタパラメーターの管理など、日常の操作とメンテナンスを実行できます。

## 構文 {#syntax}

```shell
tiup cluster [command] [flags]
```

`[command]`はコマンドの名前です。サポートされているコマンドについては、以下の[コマンドリスト](#command-list)を参照してください。

## オプション {#options}

### --ssh {#ssh}

-   コマンド実行のためにリモートエンド（TiDBサービスが展開されているマシン）に接続するSSHクライアントを指定します。

-   データ型： `STRING`

-   サポートされている値：

    -   `builtin` ：SSHクライアントとしてtiup-clusterに組み込まれているeasysshクライアントを使用します。
    -   `system` ：現在のオペレーティングシステムのデフォルトのSSHクライアントを使用します。
    -   `none` ：SSHクライアントは使用されません。展開は、現在のマシンのみを対象としています。

-   コマンドでこのオプションが指定されていない場合、デフォルト値として`builtin`が使用されます。

### --ssh-timeout {#ssh-timeout}

-   SSH接続タイムアウトを秒単位で指定します。
-   データ型： `UINT`
-   このオプションがコマンドで指定されていない場合、デフォルトのタイムアウトは`5`秒です。

### --wait-timeout {#wait-timeout}

-   操作プロセスの各ステップの最大待機時間（秒単位）を指定します。操作プロセスは、サービスを開始または停止するsystemctlの指定や、ポートがオンラインまたはオフラインになるのを待つなど、多くのステップで構成されます。各ステップには数秒かかる場合があります。ステップの実行時間が指定されたタイムアウトを超えると、ステップはエラーで終了します。
-   データ型： `UINT`
-   コマンドでこのオプションが指定されていない場合、各ステップの最大待機時間は`120`秒です。

### -y、-yes {#y-yes}

-   すべての危険な操作の二次確認をスキップします。スクリプトを使用してTiUPを呼び出す場合を除いて、このオプションの使用はお勧めしません。
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

### -v、-version {#v-version}

-   TiUPクラスターの現在のバージョンを印刷します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

### -h、-help {#h-help}

-   関連するコマンドのヘルプ情報を出力します。
-   データ型： `BOOLEAN`
-   このオプションは、デフォルトで`false`の値で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、 `true`の値を渡すか、値を渡さないようにします。

## コマンドリスト {#command-list}

-   [輸入](/tiup/tiup-component-cluster-import.md) ：Ansibleによってデプロイされたクラスタをインポートします
-   [テンプレート](/tiup/tiup-component-cluster-template.md) ：トポロジーテンプレートを出力します
-   [小切手](/tiup/tiup-component-cluster-check.md) ：デプロイの前後にクラスタをチェックします
-   [配備](/tiup/tiup-component-cluster-deploy.md) ：指定されたトポロジに基づいてクラスタをデプロイします
-   [リスト](/tiup/tiup-component-cluster-list.md) ：デプロイされたクラスターのリストを照会します
-   [画面](/tiup/tiup-component-cluster-display.md) ：指定したクラスタの状態を表示します
-   [始める](/tiup/tiup-component-cluster-start.md) ：指定されたクラスタを開始します
-   [止まる](/tiup/tiup-component-cluster-stop.md) ：指定されたクラスタを停止します
-   [再起動](/tiup/tiup-component-cluster-restart.md) ：指定したクラスタを再起動します
-   [スケールイン](/tiup/tiup-component-cluster-scale-in.md) ：指定されたクラスタのスケール
-   [規格外](/tiup/tiup-component-cluster-scale-out.md) ：指定されたクラスタをスケールアウトします
-   [アップグレード](/tiup/tiup-component-cluster-upgrade.md) ：指定されたクラスタをアップグレードします
-   [プルーン](/tiup/tiup-component-cluster-prune.md) ：指定されたクラスタのトゥームストーンステータスのインスタンスをクリーンアップします
-   [edit-config](/tiup/tiup-component-cluster-edit-config.md) ：指定したクラスタの構成を変更します
-   [リロード](/tiup/tiup-component-cluster-reload.md) ：指定されたクラスタの構成を再ロードします
-   [パッチ](/tiup/tiup-component-cluster-patch.md) ：デプロイされたクラスタのサービスを置き換えます
-   [名前を変更](/tiup/tiup-component-cluster-rename.md) ：クラスタの名前を変更します
-   [掃除](/tiup/tiup-component-cluster-clean.md) ：指定したクラスタからデータを削除します
-   [破壊する](/tiup/tiup-component-cluster-destroy.md) ：指定されたクラスタを破棄します
-   [監査](/tiup/tiup-component-cluster-audit.md) ：指定されたクラスタの操作監査ログを照会します
-   [リプレイ](/tiup/tiup-component-cluster-replay.md) ：指定したコマンドを再試行します
-   [有効](/tiup/tiup-component-cluster-enable.md) ：マシンの再起動後にクラスタサービスの自動有効化を有効にします。
-   [無効にする](/tiup/tiup-component-cluster-disable.md) ：マシンの再起動後にクラスタサービスの自動有効化を無効にします。
-   [ヘルプ](/tiup/tiup-component-cluster-help.md) ：ヘルプ情報を出力します

[&lt;&lt;前のページに戻る-TiUPリファレンスコンポーネントリスト](/tiup/tiup-reference.md#component-list)
