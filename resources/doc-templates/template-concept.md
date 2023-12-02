---
title: (The same as L1 heading) Concept such as "Garbage Collection Overview" in 59 characters or less. Include the keywords of this document. Test title here https://moz.com/learn/seo/title-tag
summary: Summarize this doc in 115 to 145 characters. Start with an SEO-friendly verb that tells users what they can get from this doc. For example, "Learn how to quickly get started with the TiDB database". If your intro paragraph describes your article's intent, you can use it here, edited for length.
---

# L1 見出し (メタデータのタイトルと同じ) {#l1-heading-the-same-as-title-in-the-metadata}

> このテンプレートについて:
>
> -   このドキュメントは、コンセプトと説明情報の紹介に重点を置いたコンセプト トピックのテンプレートです。このテンプレートを直接コピーして使用したり、不要な注釈を削除したりできます。このタイプの文書の例: [TiCDC の概要](/ticdc/ticdc-overview.md) .
> -   新しいドキュメントの場合は、 `TOC.md`ファイル内の適切な場所へのリンクを追加してください (ユーザーが目次のどこでこのドキュメントを探す可能性が最も高いかを考慮してください)。
> -   文書内の見出しはレベルをスキップできないため、レベル 5 の見出しの使用は避けるようにしてください。

**必須**最初の段落では、この文書の内容を数文で要約してください。

この段落の 1 ～ 3 文で重要な用語と定義を明確にすることができます。

## L2 見出し (例: アーキテクチャ) {#l2-heading-e-g-architecture}

アーキテクチャ全体を例に挙げると、まずコア コンポーネントを 1 ～ 2 文で紹介し、次に対応するアーキテクチャ図を提供します。

<!--  ![Architecture](/path/to/image)  -->

画像サイズは 300 KB 以下にしてください。 `.png`または`.jpg`を使用します。 `.gif`または`.svg`使用しないでください。

画像の下にさらに詳しい説明を書きます。各コンポーネントを導入するには、順序なしリスト ( `*` ) `+` `-`します。

-   コンポーネント 1:xxx
-   コンポーネント 2: xxx

ここで基本的な動作原理を説明したり、その原理を上記のコンポーネントの紹介に組み込んだりすることもできます。

### L3 見出し (オプション、例: 「xxxコンポーネント」) {#l3-heading-optional-e-g-xxx-component}

コンポーネントが複雑な場合は、このセクションのように別のセクションで詳細を説明できます。

### L3 見出し {#l3-heading}

xxx

## L2 見出し (オプション、例: 「主な機能/制限事項」) {#l2-heading-optional-e-g-key-features-limitations}

2 番目の L2 見出しでは、主な機能、使用シナリオ、制限事項など、ユーザーが事前に知っておく必要がある基本情報を紹介します。

この情報を提供する必要がない場合は、このセクションを省略できます。

注記や警告を追加する必要がある場合は、次の形式に厳密に従ってください。

> **警告**
>
> 情報がシステムの可用性、セキュリティ、データ損失などのリスクをユーザーにもたらす可能性がある場合は、警告を使用します。たとえば、現在の機能は実験的機能であり、本番環境には推奨されません。

> **注記**
>
> 一般的なヒントとメモについては、メモを使用してください。たとえば、履歴データを読み込む場合、現在のテーブル構造が履歴データのテーブル構造と異なっていても、履歴データはその時点の履歴データのテーブル構造で返されます。

注または警告がリスト内でネストされている場合は、4 つのスペースでインデントします。

誤った表示を防ぐため、PingCAP Web サイトのインデントはすべてスペース 4 文字にする必要があります。

## 次は何ですか {#what-s-next}

このセクションでは、ユーザーが読みたいと思われる次のような関連ドキュメントをさらに提供します。

-   TiCDC を展開および保守する方法については、 [TiCDC のデプロイと管理](/ticdc/deploy-ticdc.md)を参照してください。
-   チェンジフィードについて学習するには、 [チェンジフィードの概要](/ticdc/ticdc-changefeed-overview.md)を参照してください。

ユーザーが興味を持つ可能性のある次のようなドキュメントを直接提供することもできます。

-   [HTAP を探索する](/explore-htap.md)
-   [TiCDC よくある質問](/ticdc/ticdc-faq.md)
-   [TiCDC 用語集](/ticdc/ticdc-glossary.md)
