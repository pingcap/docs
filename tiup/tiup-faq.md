---
title: TiUP FAQ
summary: Provide answers to common questions asked by TiUP users.
---

# TiUP FAQ {#tiup-faq}

## TiUPは公式のミラーソースを使用できませんか？ {#can-tiup-not-use-the-official-mirror-source}

TiUPは、 `TIUP_MIRRORS`の環境変数を介したミラーソースの指定をサポートしています。ミラーソースのアドレスは、ローカルディレクトリまたはHTTPサーバーアドレスにすることができます。ご使用の環境がネットワークにアクセスできない場合は、TiUPを使用するための独自のオフラインミラーソースを作成できます。

非公式ミラーを使用した後、公式ミラーを元に戻して使用する場合は、次のいずれかの方法を実行してください。

-   `TIUP_MIRRORS`変数を公式ミラーアドレスに設定します： `https://tiup-mirrors.pingcap.com` 。
-   `TIUP_MIRRORS`変数が設定されていないことを確認してから、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行してください。

## 自分のコンポーネントをTiUPミラーに入れるにはどうすればよいですか？ {#how-do-i-put-my-own-component-into-the-tiup-mirrors}

TiUPは当面サードパーティのコンポーネントをサポートしていませんが、TiUPチームはTiUPコンポーネント開発仕様を開発し、tiup-publishコンポーネントを開発しています。すべての準備が整ったら、寄稿者は`tiup publish <comp> <version>`コマンドを使用して、独自のコンポーネントをTiUPの公式ミラーに公開できます。

## TiUPプレイグラウンドとTiUPクラスタコンポーネントの違いは何ですか？ {#what-is-the-difference-between-the-tiup-playground-and-tiup-cluster-components}

TiUPプレイグラウンドコンポーネントは、主にLinuxまたはmacOSオペレーティングシステムでスタンドアロンの開発環境を構築するために使用されます。すばやく開始し、指定したバージョンのTiUPクラスタを簡単に実行するのに役立ちます。 TiUPクラスタコンポーネントは、主に本番環境クラスタ（通常は大規模クラスタ）の展開と保守に使用されます。

## TiUPクラスタコンポーネントのトポロジファイルを作成するにはどうすればよいですか？ {#how-do-i-write-the-topology-file-for-the-tiup-cluster-component}

トポロジファイルを書き込むには、 [これらのテンプレート](https://github.com/pingcap/tiup/tree/master/examples)を参照してください。テンプレートには次のものが含まれます。

-   マルチDC展開トポロジ
-   最小限の展開トポロジ
-   完全なトポロジーファイル

テンプレートとニーズに基づいてトポロジファイルを編集できます。

## 同じホストに複数のインスタンスをデプロイできますか？ {#can-multiple-instances-be-deployed-on-the-same-host}

TiUPクラスタコンポーネントを使用して、同じホストに複数のインスタンスをデプロイできますが、異なるポートとディレクトリが構成されています。そうしないと、ディレクトリとポートの競合が発生する可能性があります。

## 同じクラスタ内でポートとディレクトリの競合が検出されていますか？ {#are-port-and-directory-conflicts-detected-within-the-same-cluster}

同じクラスタのポートとディレクトリの競合は、展開およびスケーリング中に検出されます。ディレクトリまたはポートの競合がある場合、展開またはスケーリングプロセスが中断されます。

## 異なるクラスター間でポートとディレクトリの競合が検出されていますか？ {#are-port-and-directory-conflicts-detected-among-different-clusters}

複数の異なるクラスターが同じTiUP制御マシンによって展開されている場合、これらのクラスター間のポートとディレクトリの競合は、展開およびスケーリング中に検出されます。クラスターが異なるTiUP制御マシンによってデプロイされている場合、競合検出は現在サポートされていません。

## クラスタの展開中に、TiUPは<code>ssh: handshake failed: read tcp 10.10.10.34:38980 -&gt; 10.10.10.34:3600: read: connection reset by peer</code>ました {#during-cluster-deployment-tiup-received-an-code-ssh-handshake-failed-read-tcp-10-10-10-34-38980-10-10-10-34-3600-read-connection-reset-by-peer-code-error}

TiUPのデフォルトの同時スレッド数がSSH接続のデフォルトの最大数を超えているため、エラーが発生する可能性があります。この問題を解決するには、SSH接続のデフォルト数を増やしてから、sshdサービスを再起動します。

{{< copyable "" >}}

```shell
vi /etc/ssh/sshd_config
```

```bash
MaxSessions 1000
MaxStartups 1000
```
