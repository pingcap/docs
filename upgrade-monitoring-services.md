---
title: Upgrade Cluster Monitoring Services
summary: TiDB クラスターの Prometheus、Grafana、および Alertmanager 監視サービスをアップグレードする方法を学習します。
---

# TiDBクラスタ監視サービスのアップグレード {#upgrade-tidb-cluster-monitoring-services}

TiDB クラスターをデプロイすると、 TiUP はクラスターの監視サービス（Prometheus、Grafana、Alertmanager など）を自動的にデプロイします。このクラスターをスケールアウトすると、 TiUP はスケーリング中に新しく追加されたノードの監視設定も自動的に追加します。TiUP によって自動的にデプロイされる監視サービスは、通常、これらのサードパーティ製監視サービスの最新バージョンではありません。最新バージョンを使用するには、こちらのドキュメントに従って監視サービスをアップグレードしてください。

クラスターを管理する際、 TiUP は独自の設定を使用して監視サービスの設定を上書きします。監視サービスの設定ファイルを置き換えて直接アップグレードすると、クラスター上で`deploy` 、 `scale-out` 、 `scale-in` 、 `reload`などの後続のTiUP操作によってアップグレードが上書きされ、エラーが発生する可能性があります。Prometheus、Grafana、および Alertmanager をアップグレードするには、設定ファイルを直接置き換えるのではなく、このドキュメントの手順に従ってください。

> **注記：**
>
> -   監視サービスが[手動で展開](/deploy-monitoring-services.md)場合、 TiUPを使用する代わりに、このドキュメントを参照せずに直接アップグレードできます。
> -   TiDBと新しいバージョンの監視サービスとの互換性はテストされていないため、アップグレード後、一部の機能が期待どおりに動作しない可能性があります。問題が発生した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)作成してください。
> -   このドキュメントのアップグレード手順は、 TiUPバージョン 1.9.0 以降に適用されます。そのため、アップグレード前にTiUP のバージョンをご確認ください。
> -   TiUPを使用して TiDB クラスターをアップグレードすると、 TiUP は監視サービスをデフォルトバージョンに再デプロイします。TiDB のアップグレード後、監視サービスのアップグレードを再度実行する必要があります。

## プロメテウスのアップグレード {#upgrade-prometheus}

TiDBとの互換性を高めるため、TiDBインストールパッケージに含まれるPrometheusインストールパッケージの使用をお勧めします。TiDBインストールパッケージに含まれるPrometheusのバージョンは固定です。より新しいバージョンのPrometheusをご利用になる場合は、各バージョンの新機能については[プロメテウス リリースノート](https://github.com/prometheus/prometheus/releases)を参照し、本番環境に適したバージョンをお選びください。推奨バージョンについては、PingCAPの技術スタッフにご相談ください。

次のアップグレード手順では、Prometheus Web サイトから必要なバージョンの Prometheus インストール パッケージをダウンロードし、それを使用してTiUPが使用できる Prometheus パッケージを作成する必要があります。

### ステップ1. Prometheusのウェブサイトから新しいPrometheusインストールパッケージをダウンロードする {#step-1-download-a-new-prometheus-installation-package-from-the-prometheus-website}

[Prometheusのダウンロードページ](https://prometheus.io/download/)から新しいインストール パッケージをダウンロードして解凍します。

### ステップ2. TiDBが提供するPrometheusインストールパッケージをダウンロードする {#step-2-download-the-prometheus-installation-package-provided-by-tidb}

1.  TiDBサーバーパッケージをダウンロードし、解凍してください。ダウンロードすることにより、 [プライバシーポリシー](https://www.pingcap.com/privacy-policy/)に同意したことになります。

        https://download.pingcap.com/tidb-community-server-{version}-linux-{arch}.tar.gz

    > **ヒント：**
    >
    > リンク内の`{version}` TiDBのバージョン番号を示し、 `{arch}`システムのアーキテクチャ（ `amd64`または`arm64`を示します。例えば、 `amd64`アーキテクチャの`v8.5.4`のダウンロードリンクは`https://download.pingcap.com/tidb-community-toolkit-v8.5.4-linux-amd64.tar.gz`です。

2.  抽出したファイルで、 `prometheus-v{version}-linux-amd64.tar.gz`見つけて抽出します。

    ```bash
    tar -xzf prometheus-v{version}-linux-amd64.tar.gz
    ```

### ステップ3. TiUPが使用できる新しいPrometheusパッケージを作成する {#step-3-create-a-new-prometheus-package-that-tiup-can-use}

1.  [ステップ1](#step-1-download-a-new-prometheus-installation-package-from-the-prometheus-website)で抽出したファイルをコピーし、コピーしたファイルを使用して[ステップ2](#step-2-download-the-prometheus-installation-package-provided-by-tidb)で抽出した`./prometheus-v{version}-linux-amd64/prometheus`ディレクトリ内のファイルを置き換えます。
2.  `./prometheus-v{version}-linux-amd64`ディレクトリを再圧縮し、新しい圧縮パッケージに`prometheus-v{new-version}.tar.gz`という名前を付けます。5 `{new-version}`必要に応じて指定できます。

    ```bash
    cd prometheus-v{version}-linux-amd64
    tar -zcvf ../prometheus-v{new-version}.tar.gz ./
    ```

### ステップ4. 新しく作成したPrometheusパッケージを使用してPrometheusをアップグレードする {#step-4-upgrade-prometheus-using-the-newly-created-prometheus-package}

Prometheus をアップグレードするには、次のコマンドを実行します。

```bash
tiup cluster patch <cluster-name> prometheus-v{new-version}.tar.gz -R prometheus --overwrite
```

アップグレード後、Prometheusサーバーのホームページ (通常は`http://<Prometheus-server-host-name>:9090` ) に移動し、上部のナビゲーション メニューで**[ステータス]**をクリックして、 **[ランタイムとビルド情報]**ページを開き、Prometheus のバージョンを確認し、アップグレードが成功したかどうかを確認できます。

## Grafanaのアップグレード {#upgrade-grafana}

TiDBとの互換性を高めるため、TiDBインストールパッケージに同梱されているGrafanaインストールパッケージのご利用をお勧めします。TiDBインストールパッケージに含まれるGrafanaのバージョンは固定です。より新しいGrafanaバージョンをご利用になる場合は、各バージョンの新機能については[Grafana リリースノート](https://grafana.com/docs/grafana/latest/whatsnew/)を参照し、本番環境に適したバージョンをお選びください。推奨バージョンについては、PingCAPの技術スタッフまでお問い合わせください。

次のアップグレード手順では、Grafana Web サイトから必要なバージョンの Grafana インストール パッケージをダウンロードし、それを使用してTiUPが使用できる Grafana パッケージを作成する必要があります。

### ステップ1. Grafanaのウェブサイトから新しいGrafanaインストールパッケージをダウンロードします。 {#step-1-download-a-new-grafana-installation-package-from-the-grafana-website}

1.  [Grafanaのダウンロードページ](https://grafana.com/grafana/download?pg=get&#x26;plcmt=selfmanaged-box1-cta1)から新しいインストールパッケージをダウンロードしてください。ニーズに応じて、 `OSS`または`Enterprise`エディションのいずれかを選択できます。
2.  ダウンロードしたパッケージを解凍します。

### ステップ2. TiDBが提供するGrafanaインストールパッケージをダウンロードする {#step-2-download-the-grafana-installation-package-provided-by-tidb}

1.  TiDBサーバーパッケージをダウンロードし、解凍してください。ダウンロードすることにより、 [プライバシーポリシー](https://www.pingcap.com/privacy-policy/)に同意したことになります。

        https://download.pingcap.com/tidb-community-server-{version}-linux-{arch}.tar.gz

    > **ヒント：**
    >
    > リンク内の`{version}` TiDBのバージョン番号を示し、 `{arch}`システムのアーキテクチャ（ `amd64`または`arm64`を示します。例えば、 `amd64`アーキテクチャの`v8.5.4`のダウンロードリンクは`https://download.pingcap.com/tidb-community-toolkit-v8.5.4-linux-amd64.tar.gz`です。

2.  抽出したファイルで、 `grafana-v{version}-linux-amd64.tar.gz`見つけて抽出します。

    ```bash
    tar -xzf grafana-v{version}-linux-amd64.tar.gz
    ```

### ステップ3. TiUPが使用できる新しいGrafanaパッケージを作成する {#step-3-create-a-new-grafana-package-that-tiup-can-use}

1.  [ステップ1](#step-1-download-a-new-grafana-installation-package-from-the-grafana-website)で抽出したファイルをコピーし、コピーしたファイルを使用して[ステップ2](#step-2-download-the-grafana-installation-package-provided-by-tidb)で抽出した`./grafana-v{version}-linux-amd64/`ディレクトリ内のファイルを置き換えます。
2.  `./grafana-v{version}-linux-amd64`ディレクトリを再圧縮し、新しい圧縮パッケージに`grafana-v{new-version}.tar.gz`という名前を付けます。5 `{new-version}`必要に応じて指定できます。

    ```bash
    cd grafana-v{version}-linux-amd64
    tar -zcvf ../grafana-v{new-version}.tar.gz ./
    ```

### ステップ4. 新しく作成したGrafanaパッケージを使用してGrafanaをアップグレードする {#step-4-upgrade-grafana-using-the-newly-created-grafana-package}

Grafana をアップグレードするには、次のコマンドを実行します。

```bash
tiup cluster patch <cluster-name> grafana-v{new-version}.tar.gz -R grafana --overwrite

```

アップグレード後、Grafanaサーバーのホームページ (通常は`http://<Grafana-server-host-name>:3000` ) に移動し、ページで Grafana のバージョンをチェックして、アップグレードが成功したかどうかを確認できます。

## Alertmanager のアップグレード {#upgrade-alertmanager}

TiDBインストールパッケージに含まれるAlertmanagerパッケージは、Prometheusウェブサイトから直接入手できます。そのため、Alertmanagerをアップグレードする場合は、Prometheusウェブサイトから新しいバージョンのAlertmanagerをダウンロードしてインストールするだけで済みます。

### ステップ1. PrometheusのWebサイトから新しいAlertmanagerインストールパッケージをダウンロードします。 {#step-1-download-a-new-alertmanager-installation-package-from-the-prometheus-website}

[Prometheusのダウンロードページ](https://prometheus.io/download/#alertmanager)から`alertmanager`インストール パッケージをダウンロードします。

### ステップ2. ダウンロードしたインストールパッケージを使用してAlertmanagerをアップグレードする {#step-2-upgrade-alertmanager-using-the-downloaded-installation-package}

Alertmanager をアップグレードするには、次のコマンドを実行します。

```bash
tiup cluster patch <cluster-name> alertmanager-v{new-version}-linux-amd64.tar.gz -R alertmanager --overwrite
```

アップグレード後、Alertmanagerサーバーのホームページ (通常は`http://<Alertmanager-server-host-name>:9093` ) に移動し、上部のナビゲーション メニューで**[ステータス]**をクリックして、Alertmanager のバージョンを確認し、アップグレードが成功したかどうかを確認できます。
