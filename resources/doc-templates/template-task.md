---
title: (The same as L1 heading) Such as "Get Started with TiDB" in 59 characters or less. Include the keywords of this document. Test title here https://moz.com/learn/seo/title-tag
summary: Summarize this doc in 115 to 145 characters. Start with an SEO-friendly verb that tells the users what they can get from this doc. For example, "Learn how to quickly get started with TiDB in 10 minutes". If your intro paragraph describes your article's intent, you can use it here, edited for length.
---

# L1 見出し (メタデータのタイトルと同じ) {#l1-heading-the-same-as-title-in-the-metadata}

> このテンプレートについて:
>
> -   このドキュメントはタスク トピックのテンプレートであり、特定のタスクを段階的に実行する方法をユーザーに説明します。このテンプレートを直接コピーして使用したり、不要な注釈を削除したりできます。このタイプの文書の例: [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)
> -   新しいドキュメントの場合は、 `TOC.md`ファイル内の適切な場所へのリンクを追加してください (ユーザーが目次のどこでこのドキュメントを探す可能性が最も高いかを考慮してください)。
> -   文書内の見出しはレベルをスキップできないため、レベル 5 の見出しの使用は避けるようにしてください。

**必須**最初の段落では、この文書の内容を数文で要約してください。

このドキュメントのタスクは次のように説明できます。

「このドキュメントでは、... (ツール) を使用して ... (タスク) を行う方法について説明します。」

## L2 見出し (通常は「前提条件」または「環境の準備」) {#l2-heading-usually-prerequisites-or-prepare-the-environment}

ハードウェア、ネットワーク、ソフトウェアのバージョンなど、タスクの前提条件を紹介します。

## ステップ1.xxx {#step-1-xxx}

順序付きリスト (1、2、3、…) を使用して、ステップを小さなサブステップに分割できます。

1.  xxx

    この手順を説明する場合は、この段落の前に**4 つのスペース**をインデントし、空白行を残してください。

    **注記**や**警告**を使用する必要がある場合は、次の形式で注記を記述します。

    > **警告**
    >
    > 情報がシステムの可用性、セキュリティ、データ損失などのリスクをユーザーにもたらす可能性がある場合は、警告を使用します。たとえば、「現在の機能は実験的機能であり、本番環境には推奨されません。」

    > **注記**
    >
    > 一般的なヒントとメモについては、メモを使用してください。たとえば、「履歴データを読み込む場合、現在のテーブル構造と履歴データのテーブル構造が異なっていても、履歴データはその時点の履歴データのテーブル構造で返されます。」

    注または警告がリスト内でネストされている場合は、4 つのスペースでインデントします。

    誤った表示を防ぐため、PingCAP Web サイトのインデントはすべてスペース 4 文字にする必要があります。

2.  xxx

    コード ブロックを使用する場合は、4 つのスペースをインデントし、ブロックの前に空白行を残します。

    ```bash
    # command
    ```

    各ステップの後に、ユーザーが操作が成功したかどうかを確認できるように、予想される結果を提供することをお勧めします。

    ```bash
    # expected output
    ```

    エラーが発生した場合の対処方法をユーザーに伝えます。

3.  xxx

    リスト内に別のリストをネストする場合は、順序付きリスト (1、2、3、…) または順序なしリスト (*/+/-) を使用し、同様に 4 つのスペースをインデントします。

    1.  サブステップ 1
    2.  サブステップ 2
    3.  サブステップ 3

    または：

    -   一品
    -   別のアイテム
    -   もう一品

4.  xxx

    ステップに構成ファイルの更新が含まれる場合は、構成ファイルの詳細な場所 (どのノードとどのディレクトリーかなど)、構成ファイルの名前を示し、ユーザーが理解しやすいように構成ファイル内の主要なフィールドについて説明します。

    ```toml
    ### tidb-lightning global configuration

    [lightning]
    # The HTTP port used to pull the web interface and Prometheus metrics. Set to 0 to disable the port.
    status-addr = ':8289'

    # Switch to server mode and use the web interface
    # For details, see the "TiDB Lightning Web UI" document.
    server-mode = false

    # log
    level = "info"
    file = "tidb-lightning.log"
    max-size = 128 # MB
    max-days = 28
    max-backups = 14
    ```

5.  xxx

    各ステップの後に、ユーザーが操作が成功したかどうかを確認できるように、予想される結果を提供することをお勧めします。

## ステップ2.xxx {#step-2-xxx}

1.  xxx

    1.  xxx
    2.  xxx

2.  xxx

3.  xxx

## ステップ3.xxx {#step-3-xxx}

## 次は何ですか {#what-s-next}

このセクションでは、ユーザーが読みたいと思われる次のような関連ドキュメントをさらに提供します。

-   TiFlashのバージョン、重要なログ、およびシステム テーブルを表示するには、 [TiFlashクラスタの管理](/tiflash/maintain-tiflash.md)を参照してください。
-   TiFlashノードを削除する必要がある場合は、 [TiFlashクラスターでのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

ユーザーが興味を持つ可能性のある次のようなドキュメントを直接提供することもできます。

-   [HTAP を探索する](/explore-htap.md)
-   [TiFlashアーキテクチャ](/tiflash/tiflash-overview.md#architecture)
-   [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md)
