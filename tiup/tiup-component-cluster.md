---
title: TiUP Cluster
summary: TiUP クラスタは、 Golangで記述されたTiUPのクラスタ管理コンポーネントです。TiDBクラスタのデプロイ、起動、シャットダウン、破棄、エラスティックスケーリング、アップグレード、 TiUPクラスタパラメータの管理など、日常的な運用とメンテナンスに使用されます。TiUP クラスタを使用するための構文は「tiup cluster [コマンド] [フラグ]」です。サポートされているコマンドには、import、template、check、deploy、list、display、start、stop、restart、scale-in、scale-out、upgrade、prune、edit-config、reload、patch、rename、clean、destroy、audit、replay、enable、disable、meta backup、meta restore、helpなどがあります。
---

# TiUPクラスタ {#tiup-cluster}

TiUP クラスタは、 Golangで記述されたTiUPのクラスタ管理コンポーネントです。TiUP クラスタコンポーネントを使用すると、 TiUPクラスタのデプロイ、起動、シャットダウン、破棄、エラスティックスケーリング、アップグレード、TiDBクラスタパラメータの管理など、日常的な運用とメンテナンスを実行できます。

## 構文 {#syntax}

```shell
tiup cluster [command] [flags]
```

`[command]`はコマンド名です。サポートされているコマンドについては、以下の[コマンドリスト](#command-list)を参照してください。

## オプション {#options}

### --ssh {#--ssh}

- コマンド実行のためにリモート エンド (TiDB サービスがデプロイされているマシン) に接続する SSH クライアントを指定します。

- データ型: `STRING`

- サポートされる値:

    - `builtin` : tiup-clusterに組み込まれている easyssh クライアントを SSH クライアントとして使用します。
    - `system` : 現在のオペレーティングシステムのデフォルトの SSH クライアントを使用します。
    - `none` : SSHクライアントは使用されません。デプロイメントは現在のマシンのみに適用されます。

- コマンドでこのオプションを指定しない場合は、デフォルト値として`builtin`が使用されます。

### --sshタイムアウト {#--ssh-timeout}

- SSH 接続のタイムアウトを秒単位で指定します。
- データ型: `UINT`
- コマンドでこのオプションを指定しない場合、デフォルトのタイムアウトは`5`秒になります。

### --wait-timeout {#--wait-timeout}

- 操作プロセスの各ステップの最大待機時間（秒単位）を指定します。操作プロセスは、systemctl によるサービスの開始または停止の指定、ポートのオンラインまたはオフラインの待機など、多くのステップで構成されます。各ステップは数秒かかる場合があります。ステップの実行時間が指定されたタイムアウトを超えた場合、そのステップはエラーで終了します。
- データ型: `UINT`
- コマンドでこのオプションを指定しない場合、各ステップの最大待機時間は`120`秒になります。

### -y, --yes {#-y---yes}

- すべてのリスクのある操作の2次確認をスキップします。スクリプトを使用してTiUPを呼び出す場合を除き、このオプションの使用は推奨されません。
- このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### -v, --version {#-v---version}

- TiUP クラスタの現在のバージョンを出力します。
- データ型: `BOOLEAN`
- このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

### -h, --help {#-h---help}

- 関連するコマンドのヘルプ情報を出力します。
- データ型: `BOOLEAN`
- このオプションはデフォルトで値`false`で無効になっています。このオプションを有効にするには、コマンドにこのオプションを追加し、値`true`を渡すか、値を渡さないでください。

## コマンドリスト {#command-list}

- [import](/tiup/tiup-component-cluster-import.md) : Ansibleによってデプロイされたクラスターをインポートします
- [template](/tiup/tiup-component-cluster-template.md) : トポロジテンプレートを出力する
- [check](/tiup/tiup-component-cluster-check.md) : デプロイメントの前後にクラスターをチェックします
- [deploy](/tiup/tiup-component-cluster-deploy.md) : 指定されたトポロジに基づいてクラスターを展開します
- [list](/tiup/tiup-component-cluster-list.md) : デプロイされたクラスタのリストを照会する
- [display](/tiup/tiup-component-cluster-display.md) : 指定されたクラスターのステータスを表示します
- [start](/tiup/tiup-component-cluster-start.md) : 指定されたクラスターを起動します
- [stop](/tiup/tiup-component-cluster-stop.md) : 指定されたクラスターを停止します
- [restart](/tiup/tiup-component-cluster-restart.md) : 指定されたクラスターを再起動します
- [scale-in](/tiup/tiup-component-cluster-scale-in.md) : 指定されたクラスター内でスケールする
- [scale-out](/tiup/tiup-component-cluster-scale-out.md) : 指定されたクラスターをスケールアウトする
- [upgrade](/tiup/tiup-component-cluster-upgrade.md) : 指定されたクラスターをアップグレードします
- [prune](/tiup/tiup-component-cluster-prune.md) : 指定されたクラスターの Tombstone ステータスのインスタンスをクリーンアップします
- [edit-config](/tiup/tiup-component-cluster-edit-config.md) : 指定されたクラスターの構成を変更します
- [reload](/tiup/tiup-component-cluster-reload.md) : 指定されたクラスタの構成を再読み込みします
- [patch](/tiup/tiup-component-cluster-patch.md) : デプロイされたクラスター内のサービスを置き換えます
- [rename](/tiup/tiup-component-cluster-rename.md) : クラスターの名前を変更する
- [clean](/tiup/tiup-component-cluster-clean.md) : 指定されたクラスターからデータを削除します
- [destroy](/tiup/tiup-component-cluster-destroy.md) : 指定されたクラスターを破棄する
- [audit](/tiup/tiup-component-cluster-audit.md) : 指定されたクラスタの操作監査ログを照会します
- [replay](/tiup/tiup-component-cluster-replay.md) : 指定されたコマンドを再試行します
- [enable](/tiup/tiup-component-cluster-enable.md) : マシンの再起動後にクラスタ サービスの自動有効化を有効にします
- [disable](/tiup/tiup-component-cluster-disable.md) : マシンの再起動後にクラスタ サービスの自動有効化を無効にします
- [meta backup](/tiup/tiup-component-cluster-meta-backup.md) : 指定されたクラスタの運用と保守に必要なTiUPメタファイルをバックアップします
- [meta restore](/tiup/tiup-component-cluster-meta-restore.md) : 指定されたクラスターのTiUPメタファイルを復元します
- [help](/tiup/tiup-component-cluster-help.md) : ヘルプ情報を出力

[&lt;&lt; 前のページに戻る - TiUP参照コンポーネントリスト](/tiup/tiup-reference.md#component-list)
