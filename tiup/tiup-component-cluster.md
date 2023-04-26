---
title: TiUP Cluster
---

# TiUPクラスタ {#tiup-cluster}

TiUP クラスタ は、 Golangで書かれたTiUPのクラスター管理コンポーネントです。 TiUPクラスタコンポーネントを使用して、展開、開始、シャットダウン、破棄、エラスティック スケーリング、TiDB クラスターのアップグレード、TiDB クラスター パラメーターの管理など、日常の操作とメンテナンスを実行できます。

## 構文 {#syntax}

```shell
tiup cluster [command] [flags]
```

`[command]`はコマンドの名前です。対応コマンドについては、下記[コマンド一覧](#command-list)を参照してください。

## オプション {#options}

### --ssh {#ssh}

-   コマンド実行のためにリモート エンド (TiDB サービスがデプロイされているマシン) に接続する SSH クライアントを指定します。

-   データ型: `STRING`

-   サポートされている値:

    -   `builtin` : tiup-clusterに組み込まれている easyssh クライアントを SSH クライアントとして使用します。
    -   `system` : 現在のオペレーティング システムのデフォルトの SSH クライアントを使用します。
    -   `none` : SSH クライアントは使用されません。展開は現在のマシンのみを対象としています。

-   コマンドでこのオプションを指定しない場合、デフォルト値として`builtin`が使用されます。

### --ssh-タイムアウト {#ssh-timeout}

-   SSH 接続のタイムアウトを秒単位で指定します。
-   データ型: `UINT`
-   このオプションがコマンドで指定されていない場合、デフォルトのタイムアウトは`5`秒です。

### --待機タイムアウト {#wait-timeout}

-   操作プロセスの各ステップの最大待機時間 (秒単位) を指定します。操作プロセスは、systemctl を指定してサービスを開始または停止したり、ポートがオンラインまたはオフラインになるのを待ったりするなど、多くの手順で構成されます。各ステップには数秒かかる場合があります。ステップの実行時間が指定されたタイムアウトを超えると、ステップはエラーで終了します。
-   データ型: `UINT`
-   コマンドでこのオプションを指定しない場合、各ステップの最大待機時間は`120`秒です。

### -y, --はい {#y-yes}

-   すべての危険な操作の二次確認をスキップします。スクリプトを使用してTiUPを呼び出す場合を除き、このオプションの使用はお勧めしません。
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

### -v, --version {#v-version}

-   TiUP クラスタの現在のバージョンを出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

### -h, --help {#h-help}

-   関連コマンドのヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`渡すか、値を何も渡さないでください。

## コマンド一覧 {#command-list}

-   [輸入](/tiup/tiup-component-cluster-import.md) : Ansible によってデプロイされたクラスターをインポートします
-   [レンプレート](/tiup/tiup-component-cluster-template.md) : トポロジ テンプレートを出力します。
-   [チェック](/tiup/tiup-component-cluster-check.md) : デプロイの前後にクラスターをチェックします
-   [配備](/tiup/tiup-component-cluster-deploy.md) : 指定されたトポロジーに基づいてクラスターをデプロイします
-   [リスト](/tiup/tiup-component-cluster-list.md) : デプロイされたクラスターのリストを照会します
-   [画面](/tiup/tiup-component-cluster-display.md) : 指定したクラスターのステータスを表示します
-   [始める](/tiup/tiup-component-cluster-start.md) : 指定されたクラスターを開始します
-   [ストップ](/tiup/tiup-component-cluster-stop.md) : 指定したクラスターを停止します
-   [再起動](/tiup/tiup-component-cluster-restart.md) : 指定したクラスターを再起動します
-   [スケールイン](/tiup/tiup-component-cluster-scale-in.md) : 指定されたクラスターでスケーリングします
-   [規格外](/tiup/tiup-component-cluster-scale-out.md) : 指定されたクラスターをスケールアウトします
-   [アップグレード](/tiup/tiup-component-cluster-upgrade.md) : 指定されたクラスターをアップグレードします
-   [プルーン](/tiup/tiup-component-cluster-prune.md) : 指定されたクラスターのトゥームストーン ステータスのインスタンスをクリーンアップします。
-   [編集構成](/tiup/tiup-component-cluster-edit-config.md) : 指定されたクラスターの構成を変更します
-   [リロード](/tiup/tiup-component-cluster-reload.md) : 指定されたクラスターの構成を再ロードします。
-   [パッチ](/tiup/tiup-component-cluster-patch.md) : デプロイされたクラスター内のサービスを置き換えます
-   [名前を変更](/tiup/tiup-component-cluster-rename.md) : クラスターの名前を変更します
-   [綺麗](/tiup/tiup-component-cluster-clean.md) : 指定されたクラスターからデータを削除します
-   [破壊](/tiup/tiup-component-cluster-destroy.md) : 指定されたクラスターを破棄します
-   [監査](/tiup/tiup-component-cluster-audit.md) : 指定したクラスタの動作監査ログを問い合わせる
-   [リプレイ](/tiup/tiup-component-cluster-replay.md) : 指定されたコマンドを再試行します
-   [有効](/tiup/tiup-component-cluster-enable.md) : マシンの再起動後にクラスター サービスの自動有効化を有効にします。
-   [無効にする](/tiup/tiup-component-cluster-disable.md) : マシンの再起動後のクラスター サービスの自動有効化を無効にします。
-   [メタ バックアップ](/tiup/tiup-component-cluster-meta-backup.md) : 指定したクラスターの運用と保守に必要なTiUPメタ ファイルをバックアップします。
-   [メタ リストア](/tiup/tiup-component-cluster-meta-restore.md) : 指定したクラスターのTiUPメタ ファイルを復元します。
-   [ヘルプ](/tiup/tiup-component-cluster-help.md) : ヘルプ情報を出力

[&lt;&lt; 前のページに戻る - TiUP参考コンポーネント一覧](/tiup/tiup-reference.md#component-list)
