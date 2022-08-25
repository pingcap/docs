---
title: TiUP DM
---

# TiUP DM {#tiup-dm}

TiDB クラスターの管理に使用される[TiUPクラスター](/tiup/tiup-component-cluster.md)と同様に、 TiUP DMは DM クラスターの管理に使用されます。 TiUP DMコンポーネントを使用して、DM クラスターの日常の運用および保守タスクを実行できます。これには、デプロイ、開始、停止、破棄、エラスティック スケーリング、DM クラスターのアップグレード、DM クラスターの構成パラメーターの管理が含まれます。

## 構文 {#syntax}

```shell
tiup dm [command] [flags]
```

`[command]`は、コマンドの名前を渡すために使用されます。サポートされているコマンドについては、 [コマンド一覧](#command-list)を参照してください。

## オプション {#options}

### --ssh {#ssh}

-   コマンド実行のためにリモート エンド (TiDB サービスがデプロイされているマシン) に接続する SSH クライアントを指定します。

-   データ型: `STRING`

-   サポート値:

    -   `builtin` : tiup-cluster の組み込みの easyssh クライアントを SSH クライアントとして使用します。
    -   `system` : 現在のオペレーティング システムの既定の SSH クライアントを使用します。
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

-   すべての危険な操作の二次確認をスキップします。スクリプトを使用して TiUP を呼び出す場合を除き、このオプションを使用することはお勧めしません。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を何も渡さないでください。

### -v, --version {#v-version}

-   TiUP DMの現在のバージョンを出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を何も渡さないでください。

### -h, --help {#h-help}

-   指定されたコマンドに関するヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションはデフォルトで無効になっており、値は`false`です。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を何も渡さないでください。

## コマンド一覧 {#command-list}

-   [輸入](/tiup/tiup-component-dm-import.md) : DM-Ansible によってデプロイされた DM v1.0クラスタをインポートします。
-   [テンプレート](/tiup/tiup-component-dm-template.md) : トポロジ テンプレートを出力します。
-   [配備](/tiup/tiup-component-dm-deploy.md) : 指定されたトポロジに基づいてクラスタをデプロイします。
-   [リスト](/tiup/tiup-component-dm-list.md) : デプロイされたクラスターのリストを照会します。
-   [画面](/tiup/tiup-component-dm-display.md) : 指定したクラスタのステータスを表示します。
-   [始める](/tiup/tiup-component-dm-start.md) : 指定されたクラスタを開始します。
-   [止まる](/tiup/tiup-component-dm-stop.md) : 指定したクラスタを停止します。
-   [再起動](/tiup/tiup-component-dm-restart.md) : 指定したクラスタを再起動します。
-   [スケールイン](/tiup/tiup-component-dm-scale-in.md) : 指定されたクラスタでスケーリングします。
-   [規格外](/tiup/tiup-component-dm-scale-out.md) : 指定されたクラスタをスケールアウトします。
-   [アップグレード](/tiup/tiup-component-dm-upgrade.md) : 指定したクラスタをアップグレードします。
-   [プルーン](/tiup/tiup-component-dm-prune.md) : 指定されたクラスタのトゥームストーン ステータスのインスタンスをクリーンアップします。
-   [編集構成](/tiup/tiup-component-dm-edit-config.md) : 指定されたクラスタの構成を変更します。
-   [リロード](/tiup/tiup-component-dm-reload.md) : 指定されたクラスタの構成を再ロードします。
-   [パッチ](/tiup/tiup-component-dm-patch.md) : デプロイされたクラスタの指定されたサービスを置き換えます。
-   [破壊する](/tiup/tiup-component-dm-destroy.md) : 指定されたクラスタを破棄します。
-   [監査](/tiup/tiup-component-dm-audit.md) : 指定したクラスタの操作監査ログを問い合わせます。
-   [リプレイ](/tiup/tiup-component-dm-replay.md) : 指定したコマンドを再生します
-   [有効](/tiup/tiup-component-dm-enable.md) : マシンの再起動後にクラスタサービスの自動有効化を有効にします。
-   [無効にする](/tiup/tiup-component-dm-disable.md) : マシンの再起動後のクラスタサービスの自動有効化を無効にします。
-   [ヘルプ](/tiup/tiup-component-dm-help.md) : ヘルプ情報を出力します。

[&lt;&lt; 前のページに戻る - TiUP 参考成分一覧](/tiup/tiup-reference.md#component-list)
