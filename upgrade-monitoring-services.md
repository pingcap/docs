---
title: Upgrade Cluster Monitoring Services
summary: Learn how to upgrade the Prometheus, Grafana, and Alertmanager monitoring services for your TiDB cluster.
---

# TiDBクラスタ監視サービスのアップグレード {#upgrade-tidb-cluster-monitoring-services}

TiDB クラスターをデプロイする場合、 TiUP はクラスターの監視サービス (Prometheus、Grafana、Alertmanager など) を自動的にデプロイします。このクラスターをスケールアウトすると、 TiUP はスケーリング中に新しく追加されたノードの監視構成も自動的に追加します。 TiUPによって自動的に展開される監視サービスは、通常、これらのサードパーティ監視サービスの最新バージョンではありません。最新バージョンを使用するには、このドキュメントに従って監視サービスをアップグレードします。

クラスターを管理する場合、 TiUP は独自の構成を使用して監視サービスの構成をオーバーライドします。構成ファイルを置き換えることによってモニタリング サービスを直接アップグレードすると、クラスター上での後続のTiUP操作 ( `deploy` 、 `scale-out` 、 `scale-in` 、 `reload`など) によってアップグレードが上書きされ、エラーが発生する可能性があります。 Prometheus、Grafana、および Alertmanager をアップグレードするには、構成ファイルを直接置き換えるのではなく、このドキュメントの手順に従ってください。

> **注記：**
>
> -   TiUPを使用せずに監視サービスが[手動でデプロイされる](/deploy-monitoring-services.md)の場合は、このドキュメントを参照せずに直接アップグレードできます。
> -   TiDB と監視サービスの新しいバージョンとの互換性はテストされていないため、アップグレード後に一部の機能が期待どおりに動作しない可能性があります。問題がある場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を作成してください。
> -   このドキュメントのアップグレード手順は、 TiUPバージョン 1.9.0 以降に適用されます。したがって、アップグレードする前にTiUP のバージョンを確認してください。
> -   TiUPを使用して TiDB クラスターをアップグレードすると、 TiUP はモニタリング サービスをデフォルト バージョンに再デプロイします。 TiDB のアップグレード後に、モニタリング サービスのアップグレードをやり直す必要があります。

## プロメテウスをアップグレードする {#upgrade-prometheus}

TiDB との互換性を高めるために、TiDB インストール パッケージで提供される Prometheus インストール パッケージを使用することをお勧めします。 TiDB インストール パッケージ内の Prometheus のバージョンは修正されました。新しい Prometheus バージョンを使用する場合は、各バージョンの新機能について[プロメテウス リリースノート](https://github.com/prometheus/prometheus/releases)を参照し、本番環境に適したバージョンを選択してください。推奨バージョンについては、PingCAP 技術スタッフに問い合わせることもできます。

次のアップグレード手順では、Prometheus Web サイトから目的のバージョンの Prometheus インストール パッケージをダウンロードし、それを使用してTiUPが使用できる Prometheus パッケージを作成する必要があります。

### ステップ 1. Prometheus Web サイトから新しい Prometheus インストール パッケージをダウンロードします。 {#step-1-download-a-new-prometheus-installation-package-from-the-prometheus-website}

[プロメテウスのダウンロードページ](https://prometheus.io/download/)から新しいインストールパッケージをダウンロードして解凍します。

### ステップ 2. TiDB が提供する Prometheus インストール パッケージをダウンロードする {#step-2-download-the-prometheus-installation-package-provided-by-tidb}

1.  [TiDBダウンロードページ](https://www.pingcap.com/download/)から TiDB**サーバー パッケージ**をダウンロードして解凍します。
2.  抽出されたファイルで`prometheus-v{version}-linux-amd64.tar.gz`見つけて抽出します。

    ```bash
    tar -xzf prometheus-v{version}-linux-amd64.tar.gz
    ```

### ステップ 3. TiUPが使用できる新しい Prometheus パッケージを作成する {#step-3-create-a-new-prometheus-package-that-tiup-can-use}

1.  [ステップ1](#step-1-download-a-new-prometheus-installation-package-from-the-prometheus-website)で解凍したファイルをコピーし、 [ステップ2](#step-2-download-the-prometheus-installation-package-provided-by-tidb)で解凍した`./prometheus-v{version}-linux-amd64/prometheus`ディレクトリ内のファイルをコピーしたファイルで置き換えます。
2.  `./prometheus-v{version}-linux-amd64`ディレクトリを再圧縮し、新しい圧縮パッケージに`prometheus-v{new-version}.tar.gz`という名前を付けます。必要に応じて`{new-version}`を指定できます。

    ```bash
    cd prometheus-v{version}-linux-amd64.tar.gz
    tar -zcvf ../prometheus-v{new-version}.tar.gz ./
    ```

### ステップ 4. 新しく作成した Prometheus パッケージを使用して Prometheus をアップグレードする {#step-4-upgrade-prometheus-using-the-newly-created-prometheus-package}

次のコマンドを実行して Prometheus をアップグレードします。

```bash
tiup cluster patch <cluster-name> prometheus-v{new-version}.tar.gz -R prometheus
```

アップグレード後、Prometheusサーバーのホームページ (通常は`http://<Prometheus-server-host-name>:9090` ) に移動し、上部のナビゲーション メニューで**[ステータス]**をクリックし、[**ランタイムとビルド情報]**ページを開いて Prometheus のバージョンを確認し、アップグレードが成功したかどうかを確認できます。 。

## グラファナをアップグレードする {#upgrade-grafana}

TiDB との互換性を高めるために、TiDB インストール パッケージで提供される Grafana インストール パッケージを使用することをお勧めします。 TiDB インストール パッケージ内の Grafana のバージョンは修正されました。新しい Grafana バージョンを使用する場合は、各バージョンの新機能について[Grafana リリースノート](https://grafana.com/docs/grafana/latest/whatsnew/)を参照し、本番環境に適したバージョンを選択してください。推奨バージョンについては、PingCAP 技術スタッフに問い合わせることもできます。

次のアップグレード手順では、目的のバージョンの Grafana インストール パッケージを Grafana Web サイトからダウンロードし、それを使用してTiUPが使用できる Grafana パッケージを作成する必要があります。

### ステップ 1. Grafana Web サイトから新しい Grafana インストール パッケージをダウンロードします。 {#step-1-download-a-new-grafana-installation-package-from-the-grafana-website}

1.  [グラファナのダウンロードページ](https://grafana.com/grafana/download?pg=get&#x26;plcmt=selfmanaged-box1-cta1)から新しいインストール パッケージをダウンロードします。ニーズに応じて`OSS`または`Enterprise`エディションのいずれかを選択できます。
2.  ダウンロードしたパッケージを解凍します。

### ステップ 2. TiDB が提供する Grafana インストール パッケージをダウンロードする {#step-2-download-the-grafana-installation-package-provided-by-tidb}

1.  [TiDBダウンロードページ](https://www.pingcap.com/download)から TiDB **Server Package**パッケージをダウンロードして解凍します。
2.  抽出されたファイルで`grafana-v{version}-linux-amd64.tar.gz`見つけて抽出します。

    ```bash
    tar -xzf grafana-v{version}-linux-amd64.tar.gz
    ```

### ステップ 3. TiUPが使用できる新しい Grafana パッケージを作成する {#step-3-create-a-new-grafana-package-that-tiup-can-use}

1.  [ステップ1](#step-1-download-a-new-grafana-installation-package-from-the-grafana-website)で解凍したファイルをコピーし、 [ステップ2](#step-2-download-the-grafana-installation-package-provided-by-tidb)で解凍した`./grafana-v{version}-linux-amd64/`ディレクトリ内のファイルをコピーしたファイルで置き換えます。
2.  `./grafana-v{version}-linux-amd64`ディレクトリを再圧縮し、新しい圧縮パッケージに`grafana-v{new-version}.tar.gz`という名前を付けます。必要に応じて`{new-version}`を指定できます。

    ```bash
    cd grafana-v{version}-linux-amd64.tar.gz
    tar -zcvf ../grafana-v{new-version}.tar.gz ./
    ```

### ステップ 4. 新しく作成した Grafana パッケージを使用して Grafana をアップグレードする {#step-4-upgrade-grafana-using-the-newly-created-grafana-package}

次のコマンドを実行して Grafana をアップグレードします。

```bash
tiup cluster patch <cluster-name> grafana-v{new-version}.tar.gz -R grafana

```

アップグレード後、Grafanaサーバーのホームページ (通常は`http://<Grafana-server-host-name>:3000` ) に移動し、ページ上の Grafana バージョンをチェックしてアップグレードが成功したかどうかを確認できます。

## アラートマネージャーのアップグレード {#upgrade-alertmanager}

TiDB インストール パッケージ内の Alertmanager パッケージは、Prometheus Web サイトから直接取得されます。したがって、Alertmanager をアップグレードする場合は、Prometheus Web サイトから新しいバージョンの Alertmanager をダウンロードしてインストールするだけで済みます。

### ステップ 1. Prometheus Web サイトから新しい Alertmanager インストール パッケージをダウンロードします。 {#step-1-download-a-new-alertmanager-installation-package-from-the-prometheus-website}

[プロメテウスのダウンロードページ](https://prometheus.io/download/#alertmanager)から`alertmanager`インストール パッケージをダウンロードします。

### ステップ 2. ダウンロードしたインストール パッケージを使用して Alertmanager をアップグレードする {#step-2-upgrade-alertmanager-using-the-downloaded-installation-package}

次のコマンドを実行して、Alertmanager をアップグレードします。

```bash
tiup cluster patch <cluster-name> alertmanager-v{new-version}-linux-amd64.tar.gz -R alertmanager
```

アップグレード後、Alertmanagerサーバーのホームページ (通常は`http://<Alertmanager-server-host-name>:9093` ) に移動し、上部のナビゲーション メニューで**[ステータス]**をクリックし、Alertmanager のバージョンをチェックしてアップグレードが成功したかどうかを確認できます。
