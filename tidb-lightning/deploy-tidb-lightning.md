---
title: Deploy TiDB Lightning
summary: TiDB Lightningをデプロイ、大量の新しいデータを迅速にインポートします。
---

# TiDB Lightningをデプロイ {#deploy-tidb-lightning}

このドキュメントでは、TiDB Lightningを使用してデータをインポートするためのハードウェア要件と、手動でのデプロイ方法について説明します。ハードウェアリソースの要件は、インポートモードによって異なります。詳細については、以下のドキュメントを参照してください。

-   [物理インポートモードの要件と制限](/tidb-lightning/tidb-lightning-physical-import-mode.md#requirements-and-restrictions)
-   [論理インポートモードの要件と制限](/tidb-lightning/tidb-lightning-logical-import-mode.md)

## TiUPを使用したオンライン展開 (推奨) {#online-deployment-using-tiup-recommended}

1.  次のコマンドを使用してTiUPをインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    このコマンドは、 TiUP を環境変数`PATH`に自動的に追加します。 TiUP を使用するには、新しいターミナルセッションを開始するか、 `source ~/.bashrc`実行する必要があります。（環境によっては`source ~/.profile`実行する必要がある場合があります。具体的なコマンドについては、 TiUPの出力を確認してください。）

2.  TiUPを使用してTiDB Lightningをインストールします。

    ```shell
    tiup install tidb-lightning
    ```

## 手動展開 {#manual-deployment}

### TiDB Lightningバイナリをダウンロード {#download-tidb-lightning-binaries}

[TiDBツールをダウンロード](/download-ecosystem-tools.md)を参照してTiDB Lightning のバイナリをダウンロードしてください。TiDB TiDB Lightning はTiDB の以前のバージョンと完全に互換性があります。最新バージョンのTiDB Lightning を使用することをお勧めします。

TiDB Lightningバイナリ パッケージを解凍して、 `tidb-lightning`実行可能ファイルを取得します。

```bash
tar -zxvf tidb-lightning-${version}-linux-amd64.tar.gz
chmod +x tidb-lightning
```

### TiDB Lightning のアップグレード {#upgrade-tidb-lightning}

TiDB Lightning は、追加の設定を必要とせず、バイナリのみを置き換えるだけでアップグレードできます。アップグレード後は、 TiDB Lightningを再起動する必要があります。詳細は[TiDB Lightningを適切に再起動する方法](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning)参照してください。

インポートタスクが実行中の場合は、 TiDB Lightningをアップグレードする前に、タスクが完了するまで待つことをお勧めします。そうしないと、チェックポイントがバージョン間で機能する保証がないため、最初から再インポートが必要になる可能性があります。
