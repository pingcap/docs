---
title: TiUP Troubleshooting Guide
summary: TiUPの使用中に問題が発生した場合のトラブルシューティング方法と解決策を紹介します。
---

# TiUPトラブルシューティングガイド {#tiup-troubleshooting-guide}

このドキュメントでは、 TiUPの使用時によくある問題とそのトラブルシューティング方法について解説します。このドキュメントに記載されていない問題が発生した場合、Github TiUPリポジトリの[新しい問題を提出する](https://github.com/pingcap/tiup/issues)参照してください。

## TiUPコマンドのトラブルシューティング {#troubleshoot-tiup-commands}

### <code>tiup list</code>を使用して最新のコンポーネントリストを表示できません {#can-t-see-the-latest-component-list-using-code-tiup-list-code}

TiUPはミラーサーバーから最新のコンポーネントリストを毎回更新するわけではありません。1 `tiup list`実行することで、コンポーネントリストを強制的に更新できます。

### <code>tiup list &lt;component&gt;</code>を使用してコンポーネントの最新バージョン情報を表示できません {#can-t-see-the-latest-version-information-of-a-component-using-code-tiup-list-x3c-component-code}

前回の問題と同様に、コンポーネントのバージョン情報は、ローカルキャッシュが存在しない場合にのみミラーサーバーから取得されます。1 `tiup list <component>`実行することでコンポーネントリストを更新できます。

### コンポーネントのダウンロードプロセスが中断されました {#component-downloading-process-is-interrupted}

ネットワークが不安定な場合、コンポーネントのダウンロードプロセスが中断される可能性があります。コンポーネントのダウンロードを再度お試しください。複数回試してもダウンロードできない場合は、CDNサーバーに問題がある可能性がありますので、問題を報告してください[ここ](https://github.com/pingcap/tiup/issues) 。

### コンポーネントのダウンロードプロセス中にチェックサムエラーが発生しました {#a-checksum-error-occurs-during-component-downloading-process}

CDNサーバーのキャッシュ時間が短いため、新しいチェックサムファイルがコンポーネントパッケージと一致しない可能性があります。5分後に再度ダウンロードをお試しください。それでも新しいチェックサムファイルがコンポーネントパッケージと一致しない場合は、問題[ここ](https://github.com/pingcap/tiup/issues)報告してください。

## TiUPクラスタコンポーネントのトラブルシューティング {#troubleshoot-tiup-cluster-component}

### <code>unable to authenticate, attempted methods [none publickey]</code>プロンプト表示されます。 {#code-unable-to-authenticate-attempted-methods-none-publickey-code-is-prompted-during-deployment}

デプロイメント中に、コンポーネントパッケージがリモートホストにアップロードされ、初期化が実行されます。このプロセスではリモートホストへの接続が必要です。このエラーは、リモートホストに接続するためのSSH秘密鍵が見つからないために発生します。

この問題を解決するには、 `tiup cluster deploy -i identity_file`実行して秘密鍵を指定したかどうかを確認します。

-   `-i`フラグが指定されていない場合、 TiUP は秘密鍵のパスを自動的に検出しない可能性があります。3 `-i`使用して秘密鍵のパスを明示的に指定することをお勧めします。
-   フラグ`-i`が指定されている場合、 TiUPは指定された秘密鍵を使用してリモートホストにログインできない可能性があります。3コマンド`ssh -i identity_file user@remote`手動で実行することで確認できます。
-   リモート ホストへのログインにパスワードを使用する場合は、フラグ`-p`を指定して正しいログイン パスワードを入力したことを確認してください。

### TiUPクラスタコンポーネントを使用したクラスタのアップグレード プロセスが中断されます {#the-process-of-upgrading-the-cluster-using-the-tiup-cluster-component-is-interrupted}

誤用を避けるため、 TiUPクラスターコンポーネントは指定されたノードのアップグレードをサポートしていません。そのため、アップグレードが失敗した後は、アップグレード プロセス中のべき等操作を含むアップグレード操作を再度実行する必要があります。

アップグレード プロセスは次の手順に分けられます。

1.  すべてのノード上のコンポーネントの古いバージョンをバックアップします
2.  新しいコンポーネントをリモートに配布
3.  すべてのコンポーネントのローリング再起動を実行します

ローリング再起動中にアップグレードが中断された場合は、操作`tiup cluster upgrade`を繰り返す代わりに、操作`tiup cluster restart -N <node1> -N <node2>`使用して、再起動が完了していないノードを再起動できます。

同じコンポーネントの再起動されていないノードの数が比較的多い場合は、 `tiup cluster restart -R <component>`実行して特定のタイプのコンポーネントを再起動することもできます。

### アップグレード中に、 <code>node_exporter-9100.service/blackbox_exporter-9115.service</code>が存在しないことがわかります。 {#during-the-upgrade-you-find-that-code-node-exporter-9100-service-blackbox-exporter-9115-service-code-does-not-exist}

以前にTiDB Ansibleからクラスタを移行し、エクスポーターがTiDB Ansibleにデプロイされていない場合、この状況が発生する可能性があります。この問題を解決するには、当面の間、他のノードから新しいノードに不足しているファイルを手動でコピーしてください。TiUPチームは、移行プロセス中に不足しているコンポーネントを補完します。
