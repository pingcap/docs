---
title: TiUP FAQs
summary: Provide answers to common questions asked by TiUP users.
---

# TiUPよくある質問 {#tiup-faqs}

このドキュメントには、 TiUPに関するよくある質問 (FAQ) がまとめられています。

## TiUP は公式ミラーソースを使用できないのでしょうか? {#can-tiup-not-use-the-official-mirror-source}

TiUP は、 `TIUP_MIRRORS`環境変数を使用したミラー ソースの指定をサポートしています。ミラー ソースのアドレスは、ローカル ディレクトリまたは HTTPサーバーアドレスです。環境がネットワークにアクセスできない場合は、 TiUPを使用する独自のオフライン ミラー ソースを作成できます。

非公式ミラーを使用した後、公式ミラーに戻して使用したい場合は、次のいずれかの措置を行ってください。

-   変数`TIUP_MIRRORS`を公式のミラー アドレスに設定します: `https://tiup-mirrors.pingcap.com` 。
-   `TIUP_MIRRORS`変数が設定されていないことを確認してから、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## 独自のコンポーネントをTiUPミラーに配置するにはどうすればよいですか? {#how-do-i-put-my-own-component-into-the-tiup-mirrors}

TiUP は当面、サードパーティ コンポーネントをサポートしませんが、 TiUPチームはTiUPコンポーネント開発仕様を開発し、 tiup-publishコンポーネントを開発しています。すべての準備が完了したら、寄稿者は`tiup publish <comp> <version>`コマンドを使用して、独自のコンポーネントを TiUP の公式ミラーに公開できます。

## TiUPプレイグラウンドとTiUPクラスター コンポーネントの違いは何ですか? {#what-is-the-difference-between-the-tiup-playground-and-tiup-cluster-components}

TiUPプレイグラウンドコンポーネントは主に、Linux または macOS オペレーティング システム上にスタンドアロン開発環境を構築するために使用されます。これにより、迅速に開始し、指定したバージョンのTiUPクラスターを簡単に実行できます。 TiUPクラスターコンポーネントは、主に実本番環境クラスター (通常は大規模クラスター) の展開と維持に使用されます。

## TiUPクラスターコンポーネントのトポロジ ファイルを作成するにはどうすればよいですか? {#how-do-i-write-the-topology-file-for-the-tiup-cluster-component}

トポロジファイルの作成は[これらのテンプレート](https://github.com/pingcap/tiup/tree/master/embed/examples/cluster)を参照してください。テンプレートには次のものが含まれます。

-   マルチ DC 導入トポロジ
-   最小限の導入トポロジ
-   完全なトポロジ ファイル

テンプレートとニーズに基づいてトポロジ ファイルを編集できます。

## 複数のインスタンスを同じホストにデプロイできますか? {#can-multiple-instances-be-deployed-on-the-same-host}

TiUPクラスターコンポーネントを使用すると、同じホスト上に複数のインスタンスをデプロイできますが、異なるポートとディレクトリが構成されています。そうしないと、ディレクトリとポートの競合が発生する可能性があります。

## 同じクラスター内でポートとディレクトリの競合が検出されますか? {#are-port-and-directory-conflicts-detected-within-the-same-cluster}

同じクラスター内のポートとディレクトリの競合は、デプロイメントおよびスケーリング中に検出されます。ディレクトリまたはポートの競合がある場合、デプロイメントまたはスケーリングのプロセスは中断されます。

## 異なるクラスター間でポートとディレクトリの競合が検出されますか? {#are-port-and-directory-conflicts-detected-among-different-clusters}

複数の異なるクラスターが同じTiUP制御マシンによってデプロイされている場合、デプロイメントおよびスケーリング中にこれらのクラスター間のポートとディレクトリの競合が検出されます。クラスターが異なるTiUP制御マシンによってデプロイされている場合、競合検出は現在サポートされていません。

## クラスターの展開中に、 TiUP が<code>ssh: handshake failed: read tcp 10.10.10.34:38980 -&gt; 10.10.10.34:3600: read: connection reset by peer</code> {#during-cluster-deployment-tiup-received-an-code-ssh-handshake-failed-read-tcp-10-10-10-34-38980-10-10-10-34-3600-read-connection-reset-by-peer-code-error}

TiUPのデフォルトの同時スレッド数がデフォルトの SSH 接続の最大数を超えているために、エラーが発生する可能性があります。この問題を解決するには、デフォルトの SSH 接続数を増やしてから、sshd サービスを再起動します。

```shell
vi /etc/ssh/sshd_config
```

```bash
MaxSessions 1000
MaxStartups 1000
```
