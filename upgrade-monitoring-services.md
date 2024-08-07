---
title: Upgrade Cluster Monitoring Services
summary: TiDB クラスターの Prometheus、Grafana、および Alertmanager 監視サービスをアップグレードする方法を学びます。
---

# TiDBクラスタ監視サービスのアップグレード {#upgrade-tidb-cluster-monitoring-services}

TiDB クラスターをデプロイすると、 TiUP はクラスターの監視サービス (Prometheus、Grafana、Alertmanager など) を自動的にデプロイします。このクラスターをスケールアウトすると、 TiUP はスケーリング中に新しく追加されたノードの監視構成も自動的に追加します。TiUP によって自動的にデプロイされる監視サービスは、通常、これらのサードパーティ監視サービスの最新バージョンではありません。最新バージョンを使用するには、このドキュメントに従って監視サービスをアップグレードしてください。

クラスターを管理する際、 TiUP は独自の構成を使用して監視サービスの構成を上書きします。構成ファイルを置き換えて監視サービスを直接アップグレードすると、クラスターでの後続のTiUP操作`scale-out` `deploy` `reload` ) によってアップグレードが上書き`scale-in`れ、エラーが発生する可能性があります。Prometheus、Grafana、および Alertmanager をアップグレードするには、構成ファイルを直接置き換えるのではなく、このドキュメントの手順に従ってください。

> **注記：**
>
> -   監視サービスが[手動で展開](/deploy-monitoring-services.md)場合は、 TiUPを使用する代わりに、このドキュメントを参照せずに直接アップグレードできます。
> -   新しいバージョンの監視サービスとの TiDB の互換性はテストされていないため、アップグレード後に一部の機能が期待どおりに動作しない可能性があります。問題がある場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)作成してください。
> -   このドキュメントのアップグレード手順は、 TiUPバージョン 1.9.0 以降に適用されます。したがって、アップグレードする前にTiUP のバージョンを確認してください。
> -   TiUPを使用して TiDB クラスターをアップグレードすると、 TiUP は監視サービスをデフォルト バージョンに再デプロイします。TiDB のアップグレード後に、監視サービスのアップグレードを再度実行する必要があります。

## プロメテウスのアップグレード {#upgrade-prometheus}

TiDB との互換性を高めるために、TiDB インストール パッケージで提供される Prometheus インストール パッケージを使用することをお勧めします。TiDB インストール パッケージ内の Prometheus のバージョンは固定されています。新しいバージョンの Prometheus を使用する場合は、各バージョンの新機能については[プロメテウス リリースノート](https://github.com/prometheus/prometheus/releases)を参照し、本番環境に適したバージョンを選択してください。推奨バージョンについては、PingCAP の技術スタッフに問い合わせることもできます。

次のアップグレード手順では、Prometheus Web サイトから必要なバージョンの Prometheus インストール パッケージをダウンロードし、それを使用してTiUPが使用できる Prometheus パッケージを作成する必要があります。

### ステップ1. PrometheusのWebサイトから新しいPrometheusインストールパッケージをダウンロードします。 {#step-1-download-a-new-prometheus-installation-package-from-the-prometheus-website}

[Prometheus ダウンロードページ](https://prometheus.io/download/)から新しいインストール パッケージをダウンロードして解凍します。

### ステップ2. TiDBが提供するPrometheusインストールパッケージをダウンロードする {#step-2-download-the-prometheus-installation-package-provided-by-tidb}

1.  TiDBサーバーパッケージをダウンロードして解凍します。ダウンロードすると、 [プライバシーポリシー](https://www.pingcap.com/privacy-policy/)に同意したことになります。

        https://download.pingcap.org/tidb-community-server-{version}-linux-{arch}.tar.gz

    > **ヒント：**
    >
    > リンク内の`{version}` TiDB のバージョン番号を示し、 `{arch}`システムのアーキテクチャ( `amd64`または`arm64`を示します。たとえば、 `amd64`アーキテクチャの`v7.5.3`のダウンロード リンクは`https://download.pingcap.org/tidb-community-toolkit-v7.5.3-linux-amd64.tar.gz`です。

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

## Grafana のアップグレード {#upgrade-grafana}

TiDB との互換性を高めるために、TiDB インストール パッケージで提供される Grafana インストール パッケージを使用することをお勧めします。TiDB インストール パッケージ内の Grafana のバージョンは固定されています。より新しいバージョンの Grafana を使用する場合は、各バージョンの新機能については[Grafana リリースノート](https://grafana.com/docs/grafana/latest/whatsnew/)を参照し、本番環境に適したバージョンを選択してください。推奨バージョンについては、PingCAP の技術スタッフに問い合わせることもできます。

次のアップグレード手順では、Grafana Web サイトから必要なバージョンの Grafana インストール パッケージをダウンロードし、それを使用してTiUPが使用できる Grafana パッケージを作成する必要があります。

### ステップ1. GrafanaのWebサイトから新しいGrafanaインストールパッケージをダウンロードします。 {#step-1-download-a-new-grafana-installation-package-from-the-grafana-website}

1.  [Grafana ダウンロードページ](https://grafana.com/grafana/download?pg=get&#x26;plcmt=selfmanaged-box1-cta1)から新しいインストール パッケージをダウンロードします。 必要に応じて、 `OSS`または`Enterprise`エディションを選択できます。
2.  ダウンロードしたパッケージを解凍します。

### ステップ2. TiDBが提供するGrafanaインストールパッケージをダウンロードする {#step-2-download-the-grafana-installation-package-provided-by-tidb}

1.  TiDBサーバーパッケージをダウンロードして解凍します。ダウンロードすると、 [プライバシーポリシー](https://www.pingcap.com/privacy-policy/)に同意したことになります。

        https://download.pingcap.org/tidb-community-server-{version}-linux-{arch}.tar.gz

    > **ヒント：**
    >
    > リンク内の`{version}` TiDB のバージョン番号を示し、 `{arch}`システムのアーキテクチャ( `amd64`または`arm64`を示します。たとえば、 `amd64`アーキテクチャの`v7.5.3`のダウンロード リンクは`https://download.pingcap.org/tidb-community-toolkit-v7.5.3-linux-amd64.tar.gz`です。

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

アップグレード後、Grafanaサーバーのホームページ (通常は`http://<Grafana-server-host-name>:3000` ) に移動し、ページで Grafana のバージョンを確認して、アップグレードが成功したかどうかを確認できます。

## Alertmanager のアップグレード {#upgrade-alertmanager}

TiDB インストール パッケージ内の Alertmanager パッケージは、Prometheus Web サイトから直接提供されます。したがって、Alertmanager をアップグレードする場合は、Prometheus Web サイトから新しいバージョンの Alertmanager をダウンロードしてインストールするだけで済みます。

### ステップ1. PrometheusのWebサイトから新しいAlertmanagerインストールパッケージをダウンロードします。 {#step-1-download-a-new-alertmanager-installation-package-from-the-prometheus-website}

[Prometheus ダウンロードページ](https://prometheus.io/download/#alertmanager)から`alertmanager`インストール パッケージをダウンロードします。

### ステップ2. ダウンロードしたインストールパッケージを使用してAlertmanagerをアップグレードする {#step-2-upgrade-alertmanager-using-the-downloaded-installation-package}

Alertmanager をアップグレードするには、次のコマンドを実行します。

```bash
tiup cluster patch <cluster-name> alertmanager-v{new-version}-linux-amd64.tar.gz -R alertmanager --overwrite
```

アップグレード後、Alertmanagerサーバーのホームページ (通常は`http://<Alertmanager-server-host-name>:9093` ) に移動し、上部のナビゲーション メニューで**[ステータス]**をクリックして、Alertmanager のバージョンを確認し、アップグレードが成功したかどうかを確認できます。
