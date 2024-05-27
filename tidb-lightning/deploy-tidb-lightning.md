---
title: Deploy TiDB Lightning
summary: TiDB Lightningをデプロイ、大量の新しいデータを迅速にインポートします。
---

# TiDB Lightning をデプロイ {#deploy-tidb-lightning}

このドキュメントでは、TiDB Lightningを使用してデータをインポートするためのハードウェア要件と、手動でデプロイする方法について説明します。ハードウェア リソースの要件は、インポート モードによって異なります。詳細については、次のドキュメントを参照してください。

-   [物理インポート モードの要件と制限](/tidb-lightning/tidb-lightning-physical-import-mode.md#requirements-and-restrictions)
-   [論理インポート モードの要件と制限](/tidb-lightning/tidb-lightning-logical-import-mode.md)

## TiUPを使用したオンライン展開 (推奨) {#online-deployment-using-tiup-recommended}

1.  次のコマンドを使用してTiUP をインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    このコマンドは、 TiUP を`PATH`環境変数に自動的に追加します。 TiUP を使用するには、新しいターミナルセッションを開始するか、 `source ~/.bashrc`を実行する必要があります。 (環境によっては、 `source ~/.profile`実行する必要がある場合があります。特定のコマンドについては、 TiUPの出力を確認してください。)

2.  TiUPを使用してTiDB Lightningをインストールします。

    ```shell
    tiup install tidb-lightning
    ```

## 手動展開 {#manual-deployment}

### TiDB Lightningバイナリをダウンロード {#download-tidb-lightning-binaries}

[TiDBツールをダウンロード](/download-ecosystem-tools.md)を参照して、 TiDB Lightningバイナリをダウンロードしてください。TiDB TiDB Lightning は、TiDB の初期バージョンと完全に互換性があります。最新バージョンのTiDB Lightningを使用することをお勧めします。

TiDB Lightningバイナリ パッケージを解凍して、 `tidb-lightning`実行可能ファイルを取得します。

```bash
tar -zxvf tidb-lightning-${version}-linux-amd64.tar.gz
chmod +x tidb-lightning
```

### TiDB Lightning のアップグレード {#upgrade-tidb-lightning}

TiDB Lightning は、追加の設定をせずにバイナリのみを置き換えることでアップグレードできます。アップグレード後は、 TiDB Lightningを再起動する必要があります。詳細については、 [TiDB Lightningを適切に再起動する方法](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning)参照してください。

インポート タスクが実行中の場合は、タスクが完了するまで待ってからTiDB Lightning をアップグレードすることをお勧めします。そうしないと、チェックポイントがバージョン間で機能するという保証がないため、最初から再インポートする必要がある可能性があります。
