---
title: TiUP Troubleshooting Guide
summary: Introduce the troubleshooting methods and solutions if you encounter issues when using TiUP.
---

# TiUPトラブルシューティング ガイド {#tiup-troubleshooting-guide}

このドキュメントでは、 TiUP を使用する際の一般的な問題とトラブルシューティング方法を紹介します。このドキュメントに遭遇した問題が含まれていない場合は、Github TiUPリポジトリで[新しい問題を提出する](https://github.com/pingcap/tiup/issues) .

## TiUPコマンドのトラブルシューティング {#troubleshoot-tiup-commands}

### <code>tiup list</code>を使用して最新のコンポーネントリストを表示できない {#can-t-see-the-latest-component-list-using-code-tiup-list-code}

TiUP は、ミラーサーバーから最新のコンポーネントリストを毎回更新するわけではありません。 `tiup list`を実行すると、コンポーネントリストを強制的に更新できます。

### <code>tiup list &lt;component&gt;</code>を使用してコンポーネントの最新バージョン情報を表示できない {#can-t-see-the-latest-version-information-of-a-component-using-code-tiup-list-x3c-component-code}

前回同様、コンポーネントのバージョン情報はローカルキャッシュがない場合のみミラーサーバーから取得します。 `tiup list <component>`を実行すると、コンポーネントリストを更新できます。

### コンポーネントのダウンロード プロセスが中断されました {#component-downloading-process-is-interrupted}

ネットワークが不安定な場合、コンポーネントのダウンロード プロセスが中断される可能性があります。コンポーネントのダウンロードを再試行できます。何度か試してもダウンロードできない場合は、CDNサーバーが原因である可能性があり、問題を報告することができます[ここ](https://github.com/pingcap/tiup/issues) 。

### コンポーネントのダウンロード プロセス中にチェックサム エラーが発生する {#a-checksum-error-occurs-during-component-downloading-process}

CDNサーバーのキャッシュ時間が短いため、新しいチェックサム ファイルがコンポーネントパッケージと一致しない場合があります。 5 分後にもう一度ダウンロードしてみてください。新しいチェックサム ファイルが依然としてコンポーネントパッケージと一致しない場合は、問題を報告してください[ここ](https://github.com/pingcap/tiup/issues) 。

## TiUPクラスタコンポーネントのトラブルシューティング {#troubleshoot-tiup-cluster-component}

### <code>unable to authenticate, attempted methods [none publickey]</code>展開中にプロンプトが表示されます {#code-unable-to-authenticate-attempted-methods-none-publickey-code-is-prompted-during-deployment}

展開中に、コンポーネントパッケージがリモート ホストにアップロードされ、初期化が実行されます。このプロセスでは、リモート ホストに接続する必要があります。このエラーは、リモート ホストに接続するための SSH 秘密鍵が見つからないために発生します。

この問題を解決するには、 `tiup cluster deploy -i identity_file`を実行して秘密鍵を指定したかどうかを確認します。

-   `-i`フラグが指定されていない場合、 TiUP が秘密鍵のパスを自動的に見つけられない可能性があります。 `-i`を使用して秘密鍵のパスを明示的に指定することをお勧めします。
-   `-i`フラグが指定されている場合、指定された秘密鍵を使用してTiUP がリモート ホストにログインできない可能性があります。 `ssh -i identity_file user@remote`コマンドを手動で実行することで確認できます。
-   パスワードを使用してリモート ホストにログインする場合は、 `-p`フラグを指定し、正しいログイン パスワードを入力したことを確認してください。

### TiUPクラスターコンポーネントを使用したクラスターのアップグレード プロセスが中断されました。 {#the-process-of-upgrading-the-cluster-using-the-tiup-cluster-component-is-interrupted}

誤用を避けるために、 TiUPクラスターコンポーネントは指定されたノードのアップグレードをサポートしていないため、アップグレードが失敗した後は、アップグレード プロセス中のべき等操作を含むアップグレード操作を再度実行する必要があります。

アップグレード プロセスは、次の手順に分けることができます。

1.  すべてのノードで古いバージョンのコンポーネントをバックアップします
2.  新しいコンポーネントをリモートに配布する
3.  すべてのコンポーネントに対してローリング再起動を実行します

ローリング再起動中にアップグレードが中断された場合、 `tiup cluster upgrade`操作を繰り返す代わりに、 `tiup cluster restart -N <node1> -N <node2>`使用して、再起動が完了していないノードを再起動できます。

同じコンポーネントの再起動されていないノードの数が比較的多い場合は、 `tiup cluster restart -R <component>`を実行して特定のタイプのコンポーネントを再起動することもできます。

### アップグレード中に、 <code>node_exporter-9100.service/blackbox_exporter-9115.service</code>存在しないことがわかります {#during-the-upgrade-you-find-that-code-node-exporter-9100-service-blackbox-exporter-9115-service-code-does-not-exist}

以前に TiDB Ansible からクラスターを移行し、エクスポーターが TiDB Ansible にデプロイされていない場合、この状況が発生する可能性があります。それを解決するために、当面の間、不足しているファイルを他のノードから新しいノードに手動でコピーできます。 TiUPチームは、移行プロセス中に不足しているコンポーネントを完成させます。
