---
title: (The same as L1 heading) Such as "Get Started with TiDB" in 59 characters or less. Include the keywords of this document. Test title here https://moz.com/learn/seo/title-tag
summary: このドキュメントを 115 ～ 145 文字で要約します。このドキュメントからユーザーが何を得ることができるかを伝える SEO に適した動詞で始めます。たとえば、「10 分で TiDB をすぐに使い始める方法を学ぶ」などです。導入段落で記事の意図を説明している場合は、長さを調整してここで使用できます。
---

# L1 見出し (メタデータのタイトルと同じ) {#l1-heading-the-same-as-title-in-the-metadata}

> このテンプレートについて:
>
> -   このドキュメントはタスクトピックのテンプレートで、ユーザーに特定のタスクを段階的に実行する方法を説明します。このテンプレートを直接コピーして使用し、不要な注釈を削除できます。このタイプのドキュメントの例: [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)
> -   新しいドキュメントの場合は、 `TOC.md`ファイル内の適切な場所へのリンクを追加してください (ユーザーが目次内でこのドキュメントを探す可能性が最も高い場所を考慮してください)。
> -   ドキュメント内の見出しはレベルをスキップできないため、レベル 5 の見出しの使用は避けてください。

**必須**最初の段落では、このドキュメントの内容を数文で要約します。

このドキュメントのタスクは次のように説明できます。

「このドキュメントでは、... (ツール) を使用して ... (タスク) を実行する方法について説明します。」

## L2 見出し (通常は「前提条件」または「環境の準備」) {#l2-heading-usually-prerequisites-or-prepare-the-environment}

ハードウェア、ネットワーク、ソフトウェアのバージョンなど、タスクの前提条件を紹介します。

## ステップ1.xxx {#step-1-xxx}

順序付きリスト（1、2、3、…）を使用して、ステップをより小さなサブステップに分割できます。

1.  xxx

    この手順を説明する場合は、 **4 スペース**インデントし、この段落の前に空白行を残します。

    **注釈**や**警告を**使用する必要がある場合は、次の形式で注釈を記述します。

    > **警告**
    >
    > 情報によって、システムの可用性、セキュリティ、データ損失などのリスクがユーザーにもたらされる可能性がある場合は、警告を使用します。たとえば、「現在の機能は実験的機能であり、本番環境での使用は推奨されません。」

    > **注記**
    >
    > 一般的なヒントや注意事項については、注記を使用します。たとえば、「履歴データを読み取る際、現在のテーブル構造が履歴データのテーブル構造と異なっていても、履歴データはその時点の履歴データのテーブル構造で返されます。」

    メモや警告がリスト内にネストされている場合は、4 つのスペースでインデントします。

    誤った表示を防ぐため、PingCAP Web サイトのすべてのインデントは 4 スペースにする必要があります。

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

    リスト内に別のリストをネストする場合は、順序付きリスト (1、2、3、…) または順序なしリスト (*/+/-) を使用し、4 つのスペースをインデントします。

    1.  サブステップ1
    2.  サブステップ2
    3.  サブステップ3

    または：

    -   一品
    -   別のアイテム
    -   もう1つ

4.  xxx

    手順に構成ファイルの更新が含まれる場合は、構成ファイルの詳細な場所（ノードとディレクトリなど）と構成ファイルの名前を示し、ユーザーが理解しやすいように構成ファイル内の主要なフィールドについて説明します。

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

このセクションでは、ユーザーが読みたいと思う可能性のある次のような関連ドキュメントを提供します。

-   TiFlash のバージョン、重要なログ、システム テーブルを表示するには、 [TiFlashクラスタを管理](/tiflash/maintain-tiflash.md)参照してください。
-   TiFlashノードを削除する必要がある場合は、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)参照してください。

次のような、ユーザーが興味を持ちそうなドキュメントを直接提供することもできます。

-   [HTAPを探索する](/explore-htap.md)
-   [TiFlashアーキテクチャ](/tiflash/tiflash-overview.md#architecture)
-   [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md)
