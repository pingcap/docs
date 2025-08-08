---
title: TiUP FAQs
summary: TiUPユーザーからよく寄せられる質問に対する回答を提供します。
---

# TiUPに関するよくある質問 {#tiup-faqs}

このドキュメントでは、 TiUPに関するよくある質問 (FAQ) をまとめています。

## TiUP は公式ミラーソースを使用できないのでしょうか? {#can-tiup-not-use-the-official-mirror-source}

TiUPは、環境変数`TIUP_MIRRORS`を介してミラーソースを指定することをサポートしています。ミラーソースのアドレスは、ローカルディレクトリまたはHTTPサーバーのアドレスにすることができます。ネットワークにアクセスできない場合は、 TiUPを使用するために独自のオフラインミラーソースを作成することができます。

非公式ミラーを使用した後、公式ミラーに戻して使用する場合は、以下のいずれかの措置を講じてください。

-   `TIUP_MIRRORS`変数を公式ミラー アドレス`https://tiup-mirrors.pingcap.com`に設定します。
-   `TIUP_MIRRORS`変数が設定されていないことを確認してから、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## 独自のコンポーネントをTiUPミラーに組み込むにはどうすればよいでしょうか? {#how-do-i-put-my-own-component-into-the-tiup-mirrors}

TiUPは現時点ではサードパーティ製コンポーネントをサポートしていませんが、 TiUPチームはTiUPコンポーネント開発仕様を策定し、tiup-publishコンポーネントを開発中です。準備が整ったら、貢献者は`tiup publish <comp> <version>`コマンドを使用して、独自のコンポーネントをTiUPの公式ミラーに公開できます。

## TiUPプレイグラウンドとTiUPクラスター コンポーネントの違いは何ですか? {#what-is-the-difference-between-the-tiup-playground-and-tiup-cluster-components}

TiUPプレイグラウンド・コンポーネントは、主にLinuxまたはmacOSオペレーティングシステム上でスタンドアロン開発環境を構築するために使用されます。これにより、 TiUPクラスタの特定のバージョンを迅速に開始し、簡単に実行できます。TiUPクラスタ・コンポーネントは、主に本番環境クラスタ（通常は大規模クラスタ）のデプロイと保守に使用されます。TiUPTiUPグラウンドでデプロイされたTiDBクラスタには、一部の機能と運用能力が不足している可能性があるため、完全な機能テストや安定性テストには推奨されません。

## TiUPクラスターコンポーネントのトポロジ ファイルを作成するにはどうすればよいでしょうか? {#how-do-i-write-the-topology-file-for-the-tiup-cluster-component}

トポロジファイルの作成方法については、 [これらのテンプレート](https://github.com/pingcap/tiup/tree/master/embed/examples/cluster)を参照してください。テンプレートには以下が含まれます。

-   マルチDC展開トポロジ
-   最小限の展開トポロジ
-   完全なトポロジファイル

テンプレートとニーズに基づいてトポロジ ファイルを編集できます。

## 同じホストに複数のインスタンスを展開できますか? {#can-multiple-instances-be-deployed-on-the-same-host}

TiUPクラスターコンポーネントを使用すると、同じホストに複数のインスタンスをデプロイできますが、異なるポートとディレクトリを構成しないと、ディレクトリとポートの競合が発生する可能性があります。

## 同じクラスター内でポートとディレクトリの競合が検出されますか? {#are-port-and-directory-conflicts-detected-within-the-same-cluster}

デプロイメントおよびスケーリング中に、同一クラスター内でのポートおよびディレクトリの競合が検出されます。ディレクトリまたはポートの競合が発生した場合、デプロイメントまたはスケーリングのプロセスは中断されます。

## 異なるクラスター間でポートとディレクトリの競合が検出されますか? {#are-port-and-directory-conflicts-detected-among-different-clusters}

複数の異なるクラスタが同じTiUP制御マシンにデプロイされている場合、デプロイおよびスケーリング中にこれらのクラスタ間のポートおよびディレクトリの競合が検出されます。クラスタが異なるTiUP制御マシンにデプロイされている場合、現在、競合検出はサポートされていません。

## クラスタの展開中に、 TiUPは<code>ssh: handshake failed: read tcp 10.10.10.34:38980 -&gt; 10.10.10.34:3600: read: connection reset by peer</code>エラーを受信しました {#during-cluster-deployment-tiup-received-an-code-ssh-handshake-failed-read-tcp-10-10-10-34-38980-10-10-10-34-3600-read-connection-reset-by-peer-code-error}

このエラーは、 TiUPのデフォルトの同時スレッド数が SSH 接続の最大数を超えているために発生する可能性があります。この問題を解決するには、デフォルトの SSH 接続数を増やしてから、sshd サービスを再起動してください。

```shell
vi /etc/ssh/sshd_config
```

```bash
MaxSessions 1000
MaxStartups 1000
```
