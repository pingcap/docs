---
title: TiUP Troubleshooting Guide
summary: Introduce the troubleshooting methods and solutions if you encounter issues when using TiUP.
---

# TiUPトラブルシューティングガイド {#tiup-troubleshooting-guide}

このドキュメントでは、TiUPを使用する際の一般的な問題とトラブルシューティング方法を紹介します。このドキュメントに遭遇した問題が含まれていない場合は、GithubTiUPリポジトリに[新しい問題を提出する](https://github.com/pingcap/tiup/issues)つ。

## TiUPコマンドのトラブルシューティング {#troubleshoot-tiup-commands}

### <code>tiup list</code>を使用して最新のコンポーネントリストを表示できません {#can-t-see-the-latest-component-list-using-code-tiup-list-code}

TiUPは、ミラーサーバーからの最新のコンポーネントリストを毎回更新するわけではありません。 `tiup list`を実行すると、コンポーネントリストを強制的に更新できます。

### <code>tiup list &lt;component&gt;</code>を使用してコンポーネントの最新バージョン情報を表示できません {#can-t-see-the-latest-version-information-of-a-component-using-code-tiup-list-x3c-component-code}

前号と同様に、コンポーネントのバージョン情報は、ローカルキャッシュがない場合にのみミラーサーバーから取得されます。 `tiup list <component>`を実行すると、コンポーネントリストを更新できます。

### コンポーネントのダウンロードプロセスが中断されました {#component-downloading-process-is-interrupted}

ネットワークが不安定な場合、コンポーネントのダウンロードプロセスが中断される可能性があります。コンポーネントのダウンロードを再試行できます。複数回試してもダウンロードできない場合は、CDNサーバーが原因である可能性があり、問題[ここ](https://github.com/pingcap/tiup/issues)を報告できます。

### コンポーネントのダウンロードプロセス中にチェックサムエラーが発生する {#a-checksum-error-occurs-during-component-downloading-process}

CDNサーバーのキャッシュ時間は短いため、新しいチェックサムファイルがコンポーネントパッケージと一致しない可能性があります。 5分後にもう一度ダウンロードしてみてください。それでも新しいチェックサムファイルがコンポーネントパッケージと一致しない場合は、問題[ここ](https://github.com/pingcap/tiup/issues)を報告してください。

## TiUPクラスタコンポーネントのトラブルシューティング {#troubleshoot-tiup-cluster-component}

### <code>unable to authenticate, attempted methods [none publickey]</code>がプロンプトされます {#code-unable-to-authenticate-attempted-methods-none-publickey-code-is-prompted-during-deployment}

展開中に、コンポーネントパッケージがリモートホストにアップロードされ、初期化が実行されます。このプロセスでは、リモートホストに接続する必要があります。このエラーは、リモートホストに接続するためのSSH秘密鍵が見つからなかったことが原因で発生します。

この問題を解決するには、 `tiup cluster deploy -i identity_file`を実行して秘密鍵を指定したかどうかを確認します。

-   `-i`フラグが指定されていない場合、TiUPが秘密鍵パスを自動的に検出しない可能性があります。 `-i`を使用して秘密鍵パスを明示的に指定することをお勧めします。
-   `-i`フラグが指定されている場合、TiUPは指定された秘密鍵を使用してリモートホストにログインできない可能性があります。 `ssh -i identity_file user@remote`コマンドを手動で実行することで確認できます。
-   リモートホストへのログインにパスワードを使用する場合は、 `-p`フラグを指定し、正しいログインパスワードを入力したことを確認してください。

### TiUPクラスタコンポーネントを使用してクラスタをアップグレードするプロセスが中断されます {#the-process-of-upgrading-the-cluster-using-the-tiup-cluster-component-is-interrupted}

誤用を避けるために、TiUPクラスタコンポーネントは指定されたノードのアップグレードをサポートしていません。そのため、アップグレードが失敗した後、アップグレードプロセス中のべき等操作を含むアップグレード操作を再度実行する必要があります。

アップグレードプロセスは、次の手順に分けることができます。

1.  すべてのノードで古いバージョンのコンポーネントをバックアップします
2.  新しいコンポーネントをリモートに配布する
3.  すべてのコンポーネントに対してローリングリスタートを実行します

ローリングリスタート中にアップグレードが中断された場合は、 `tiup cluster upgrade`の操作を繰り返す代わりに、 `tiup cluster restart -N <node1> -N <node2>`を使用してリスタートを完了していないノードをリスタートできます。

同じコンポーネントの再起動されていないノードの数が比較的多い場合は、 `tiup cluster restart -R <component>`を実行して特定のタイプのコンポーネントを再起動することもできます。

### アップグレード中に、 <code>node_exporter-9100.service/blackbox_exporter-9115.service</code>が存在しないことがわかりました {#during-the-upgrade-you-find-that-code-node-exporter-9100-service-blackbox-exporter-9115-service-code-does-not-exist}

以前にクラスタをTiDBAnsibleから移行し、エクスポーターがTiDB Ansibleにデプロイされていなかった場合、この状況が発生する可能性があります。これを解決するには、当面の間、不足しているファイルを他のノードから新しいノードに手動でコピーします。 TiUPチームは、移行プロセス中に不足しているコンポーネントを完了します。
