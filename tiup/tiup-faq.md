---
title: TiUP FAQs
summary: TiUPユーザーからよく寄せられる質問に対する回答を提供します。
---

# TiUPに関するよくある質問 {#tiup-faqs}

このドキュメントには、 TiUPに関するよくある質問 (FAQ) がまとめられています。

## TiUP は公式ミラーソースを使用できないのでしょうか? {#can-tiup-not-use-the-official-mirror-source}

TiUP は、 `TIUP_MIRRORS`環境変数を通じてミラー ソースを指定することをサポートしています。ミラー ソースのアドレスは、ローカル ディレクトリまたは HTTPサーバーアドレスにすることができます。環境がネットワークにアクセスできない場合は、独自のオフライン ミラー ソースを作成してTiUPを使用することができます。

非公式ミラーを使用した後、公式ミラーに戻して使用する場合は、次のいずれかの対策を講じてください。

-   `TIUP_MIRRORS`変数を公式ミラー アドレス`https://tiup-mirrors.pingcap.com`に設定します。
-   `TIUP_MIRRORS`変数が設定されていないことを確認してから、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## 独自のコンポーネントをTiUPミラーに組み込むにはどうすればよいでしょうか? {#how-do-i-put-my-own-component-into-the-tiup-mirrors}

TiUP は今のところサードパーティのコンポーネントをサポートしていませんが、 TiUPチームはTiUPコンポーネント開発仕様を策定し、 tiup-publishコンポーネントを開発しています。準備が整ったら、貢献者は`tiup publish <comp> <version>`コマンドを使用して、独自のコンポーネントを TiUP の公式ミラーに公開できます。

## TiUPプレイグラウンドとTiUPクラスター コンポーネントの違いは何ですか? {#what-is-the-difference-between-the-tiup-playground-and-tiup-cluster-components}

TiUPプレイグラウンドコンポーネントは、主に Linux または macOS オペレーティング システム上にスタンドアロン開発環境を構築するために使用されます。これにより、すぐに開始して、指定されたバージョンのTiUPクラスターを簡単に実行できます。TiUP クラスターコンポーネントは、主に本番環境クラスター (通常は大規模クラスター) の展開と保守に使用されます。TiUP プレイグラウンドによって展開された TiDB クラスターには、一部の機能と運用能力が不足している可能性があるTiUP、完全な機能テストと安定性テストには推奨されません。

## TiUPクラスターコンポーネントのトポロジ ファイルを作成するにはどうすればよいでしょうか? {#how-do-i-write-the-topology-file-for-the-tiup-cluster-component}

トポロジーファイルを書き込むには、 [これらのテンプレート](https://github.com/pingcap/tiup/tree/master/embed/examples/cluster)を参照してください。テンプレートには次のものが含まれます。

-   マルチDC展開トポロジ
-   最小限の展開トポロジ
-   完全なトポロジファイル

テンプレートとニーズに基づいてトポロジ ファイルを編集できます。

## 同じホストに複数のインスタンスを展開できますか? {#can-multiple-instances-be-deployed-on-the-same-host}

TiUPクラスターコンポーネントを使用すると、同じホストに複数のインスタンスをデプロイできますが、異なるポートとディレクトリを構成する必要があります。そうしないと、ディレクトリとポートの競合が発生する可能性があります。

## 同じクラスター内でポートとディレクトリの競合が検出されますか? {#are-port-and-directory-conflicts-detected-within-the-same-cluster}

デプロイメントおよびスケーリング中に、同じクラスター内のポートとディレクトリの競合が検出されます。ディレクトリまたはポートの競合がある場合、デプロイメントまたはスケーリング プロセスは中断されます。

## 異なるクラスター間でポートとディレクトリの競合が検出されますか? {#are-port-and-directory-conflicts-detected-among-different-clusters}

複数の異なるクラスターが同じTiUP制御マシンによってデプロイされている場合、デプロイおよびスケーリング中にこれらのクラスター間のポートとディレクトリの競合が検出されます。クラスターが異なるTiUP制御マシンによってデプロイされている場合、競合の検出は現在サポートされていません。

## クラスタの展開中に、 TiUP は<code>ssh: handshake failed: read tcp 10.10.10.34:38980 -&gt; 10.10.10.34:3600: read: connection reset by peer</code> {#during-cluster-deployment-tiup-received-an-code-ssh-handshake-failed-read-tcp-10-10-10-34-38980-10-10-10-34-3600-read-connection-reset-by-peer-code-error}

このエラーは、 TiUPの同時スレッドのデフォルト数が SSH 接続のデフォルトの最大数を超えているために発生する可能性があります。この問題を解決するには、SSH 接続のデフォルト数を増やしてから、sshd サービスを再起動します。

```shell
vi /etc/ssh/sshd_config
```

```bash
MaxSessions 1000
MaxStartups 1000
```
