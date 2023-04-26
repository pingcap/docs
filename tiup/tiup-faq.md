---
title: TiUP FAQs
summary: Provide answers to common questions asked by TiUP users.
---

# TiUPよくある質問 {#tiup-faqs}

このドキュメントは、 TiUPに関するよくある質問 (FAQ) をまとめたものです。

## TiUP は公式のミラーソースを使用できませんか? {#can-tiup-not-use-the-official-mirror-source}

TiUP は、 `TIUP_MIRRORS`環境変数によるミラー ソースの指定をサポートしています。ミラー ソースのアドレスは、ローカル ディレクトリまたは HTTPサーバーアドレスにすることができます。環境がネットワークにアクセスできない場合は、独自のオフライン ミラー ソースを作成してTiUPを使用できます。

非公式ミラーを使用した後、公式ミラーに戻して使用したい場合は、次のいずれかの方法を実行してください。

-   `TIUP_MIRRORS`変数を公式のミラーアドレス: `https://tiup-mirrors.pingcap.com`に設定します。
-   `TIUP_MIRRORS`変数が設定されていないことを確認してから、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## 独自のコンポーネントをTiUPミラーに配置するにはどうすればよいですか? {#how-do-i-put-my-own-component-into-the-tiup-mirrors}

TiUPは当分の間、サードパーティのコンポーネントをサポートしていませんが、 TiUPチームはTiUPコンポーネント開発仕様を開発し、tiup-publishコンポーネントを開発しています。すべての準備が整ったら、貢献者は`tiup publish <comp> <version>`コマンドを使用して、独自のコンポーネントを TiUP の公式ミラーに公開できます。

## TiUPプレイグラウンドとTiUPクラスター コンポーネントの違いは何ですか? {#what-is-the-difference-between-the-tiup-playground-and-tiup-cluster-components}

TiUPプレイグラウンドコンポーネントは、主に Linux または macOS オペレーティング システム上でスタンドアロンの開発環境を構築するために使用されます。これにより、 TiUPクラスターの指定されたバージョンを簡単に開始して実行することができます。 TiUPクラスターコンポーネントは、主に本番環境クラスター (通常は大規模クラスター) の展開と保守に使用されます。

## TiUPクラスタコンポーネントのトポロジ ファイルを作成するにはどうすればよいですか? {#how-do-i-write-the-topology-file-for-the-tiup-cluster-component}

[これらのテンプレート](https://github.com/pingcap/tiup/tree/master/embed/examples/cluster)を参照して、トポロジ ファイルを記述します。テンプレートには次のものがあります。

-   マルチ DC 展開トポロジ
-   最小限の展開トポロジ
-   完全なトポロジ ファイル

テンプレートとニーズに基づいて、トポロジ ファイルを編集できます。

## 複数のインスタンスを同じホストにデプロイできますか? {#can-multiple-instances-be-deployed-on-the-same-host}

TiUPクラスターコンポーネントを使用して、同じホスト上に複数のインスタンスを展開できますが、異なるポートとディレクトリが構成されています。そうしないと、ディレクトリとポートの競合が発生する可能性があります。

## 同じクラスタ内でポートとディレクトリの競合が検出されていますか? {#are-port-and-directory-conflicts-detected-within-the-same-cluster}

同じクラスター内のポートとディレクトリの競合は、デプロイとスケーリング中に検出されます。ディレクトリまたはポートの競合がある場合、デプロイまたはスケーリング プロセスは中断されます。

## 異なるクラスタ間でポートとディレクトリの競合が検出されていますか? {#are-port-and-directory-conflicts-detected-among-different-clusters}

複数の異なるクラスターが同じTiUPコントロール マシンによって展開されている場合、これらのクラスター間のポートとディレクトリの競合は、展開とスケーリング中に検出されます。クラスターが異なるTiUP制御マシンによって展開されている場合、競合検出は現在サポートされていません。

## クラスターの展開中に、 TiUP <code>ssh: handshake failed: read tcp 10.10.10.34:38980 -&gt; 10.10.10.34:3600: read: connection reset by peer</code>エラーを受け取りました {#during-cluster-deployment-tiup-received-an-code-ssh-handshake-failed-read-tcp-10-10-10-34-38980-10-10-10-34-3600-read-connection-reset-by-peer-code-error}

TiUPのデフォルトの同時スレッド数が SSH 接続のデフォルトの最大数を超えているために、エラーが発生する可能性があります。この問題を解決するには、SSH 接続のデフォルト数を増やしてから、sshd サービスを再起動します。

{{< copyable "" >}}

```shell
vi /etc/ssh/sshd_config
```

```bash
MaxSessions 1000
MaxStartups 1000
```
