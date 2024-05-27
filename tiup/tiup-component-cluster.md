---
title: TiUP Cluster
summary: TiUP クラスタ は、 Golangで記述されたTiUPのクラスター管理コンポーネントです。デプロイ、起動、シャットダウン、破棄、エラスティック スケーリング、TiDB クラスターのアップグレード、TiDB クラスター パラメーターの管理など、日常的な操作とメンテナンスに使用されます。TiUP クラスタを使用するための構文は、「tiup cluster [コマンド] [フラグ]」です。サポートされているコマンドには、import、template、check、deploy、list、display、start、stop、restart、scale-in、scale-out、upgrade、prune、edit-config、reload、patch、rename、clean、destroy、audit、replay、enable、disable、meta backup、meta restore、help などがあります。
---

# TiUPクラスタ {#tiup-cluster}

TiUP クラスタ は、 Golangで記述されたTiUPのクラスター管理コンポーネントです。TiUP クラスタコンポーネントを使用すると、 TiUPクラスターのデプロイ、起動、シャットダウン、破棄、エラスティック スケーリング、アップグレード、TiDB クラスター パラメータの管理など、日常的な操作とメンテナンスを実行できます。

## 構文 {#syntax}

```shell
tiup cluster [command] [flags]
```

`[command]`はコマンド名です。サポートされているコマンドについては、以下の[コマンドリスト](#command-list)を参照してください。

## オプション {#options}

### --ssh {#ssh}

-   コマンド実行のためにリモート エンド (TiDB サービスがデプロイされているマシン) に接続する SSH クライアントを指定します。

-   データ型: `STRING`

-   サポートされる値:

    -   `builtin` : tiup-clusterに組み込まれている easyssh クライアントを SSH クライアントとして使用します。
    -   `system` : 現在のオペレーティング システムのデフォルトの SSH クライアントを使用します。
    -   `none` : SSH クライアントは使用されません。展開は現在のマシンのみに適用されます。

-   コマンドでこのオプションが指定されていない場合は、デフォルト値として`builtin`使用されます。

### --sshタイムアウト {#ssh-timeout}

-   SSH 接続のタイムアウトを秒単位で指定します。
-   データ型: `UINT`
-   このオプションがコマンドで指定されていない場合、デフォルトのタイムアウトは`5`秒です。

### --wait-timeout {#wait-timeout}

-   操作プロセスの各ステップの最大待機時間 (秒単位) を指定します。操作プロセスは、systemctl を指定してサービスを開始または停止したり、ポートがオンラインまたはオフラインになるまで待機したりするなど、多くのステップで構成されます。各ステップには数秒かかる場合があります。ステップの実行時間が指定されたタイムアウトを超えると、ステップはエラーで終了します。
-   データ型: `UINT`
-   コマンドでこのオプションが指定されていない場合、各ステップの最大待機時間は`120`秒になります。

### -y、--はい {#y-yes}

-   すべての危険な操作の二次確認をスキップします。スクリプトを使用してTiUPを呼び出す場合を除き、このオプションの使用はお勧めしません。
-   このオプションは、デフォルトで値`false`で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにする必要があります。

### -v, --バージョン {#v-version}

-   TiUP クラスタの現在のバージョンを出力します。
-   データ型: `BOOLEAN`
-   このオプションは、デフォルトで値`false`で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにする必要があります。

### -h, --help {#h-help}

-   関連するコマンドのヘルプ情報を出力します。
-   データ型: `BOOLEAN`
-   このオプションは、デフォルトで値`false`で無効になっています。このオプションを有効にするには、このオプションをコマンドに追加し、値`true`を渡すか、値を渡さないようにする必要があります。

## コマンドリスト {#command-list}

-   [輸入](/tiup/tiup-component-cluster-import.md) : Ansibleによってデプロイされたクラスターをインポートします
-   [テンプレート](/tiup/tiup-component-cluster-template.md) : トポロジテンプレートを出力する
-   [チェック](/tiup/tiup-component-cluster-check.md) : デプロイメントの前後にクラスターをチェックします
-   [展開する](/tiup/tiup-component-cluster-deploy.md) : 指定されたトポロジに基づいてクラスターを展開します
-   [リスト](/tiup/tiup-component-cluster-list.md) : デプロイされたクラスタのリストを照会する
-   [画面](/tiup/tiup-component-cluster-display.md) : 指定されたクラスターのステータスを表示します
-   [始める](/tiup/tiup-component-cluster-start.md) : 指定されたクラスターを起動します
-   [停止](/tiup/tiup-component-cluster-stop.md) : 指定されたクラスターを停止します
-   [再起動](/tiup/tiup-component-cluster-restart.md) : 指定されたクラスターを再起動します
-   [スケールイン](/tiup/tiup-component-cluster-scale-in.md) : 指定されたクラスター内でスケールする
-   [規格外](/tiup/tiup-component-cluster-scale-out.md) : 指定されたクラスターをスケールアウトする
-   [アップグレード](/tiup/tiup-component-cluster-upgrade.md) : 指定されたクラスターをアップグレードします
-   [プルーン](/tiup/tiup-component-cluster-prune.md) : 指定されたクラスターの Tombstone ステータスのインスタンスをクリーンアップします
-   [編集設定](/tiup/tiup-component-cluster-edit-config.md) : 指定されたクラスタの構成を変更します
-   [リロード](/tiup/tiup-component-cluster-reload.md) : 指定されたクラスタの構成を再読み込みします
-   [パッチ](/tiup/tiup-component-cluster-patch.md) : デプロイされたクラスター内のサービスを置き換えます
-   [名前を変更する](/tiup/tiup-component-cluster-rename.md) : クラスターの名前を変更する
-   [クリーン](/tiup/tiup-component-cluster-clean.md) : 指定されたクラスターからデータを削除します
-   [破壊する](/tiup/tiup-component-cluster-destroy.md) : 指定されたクラスターを破棄します
-   [監査](/tiup/tiup-component-cluster-audit.md) : 指定されたクラスタの操作監査ログを照会します
-   [リプレイ](/tiup/tiup-component-cluster-replay.md) : 指定されたコマンドを再試行します
-   [有効にする](/tiup/tiup-component-cluster-enable.md) : マシンの再起動後にクラスタ サービスの自動有効化を有効にする
-   [無効にする](/tiup/tiup-component-cluster-disable.md) : マシンの再起動後にクラスタ サービスの自動有効化を無効にします
-   [メタバックアップ](/tiup/tiup-component-cluster-meta-backup.md) : 指定されたクラスタの運用と保守に必要なTiUPメタファイルをバックアップします
-   [メタリストア](/tiup/tiup-component-cluster-meta-restore.md) : 指定されたクラスターのTiUPメタファイルを復元します
-   [ヘルプ](/tiup/tiup-component-cluster-help.md) : ヘルプ情報を出力

[&lt;&lt; 前のページに戻る - TiUP参照コンポーネントリスト](/tiup/tiup-reference.md#component-list)
