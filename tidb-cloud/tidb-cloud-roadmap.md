---
title: TiDB Cloud Roadmap
summary: Learn about TiDB Cloud's roadmap for the next few months. See the new features or improvements in advance, follow the progress, learn about the key milestones on the way.
---

# TiDB Cloudロードマップ {#tidb-cloud-roadmap}

TiDB Cloudロードマップには、近い将来に何が提供されるかが示されているため、新機能や改善点を事前に確認し、進捗状況を追跡し、途中の主要なマイルストーンについて学ぶことができます。開発の過程で、このロードマップはユーザーのニーズ、フィードバック、および当社の評価に基づいて変更される可能性があります。

✅: この機能または改善は、すでにTiDB Cloudで利用可能です。

> **セーフハーバーに関する声明:**
>
> 当社のドキュメント、ロードマップ、ブログ、Web サイト、プレスリリース、または現在利用できない公式声明で議論または参照されている未リリースの機能 (「未リリースの機能」) は、当社の裁量により変更される可能性があり、計画どおりに提供されない、またはまったく提供されない場合があります。 。お客様は、特に明記されていない限り、購入の決定は現在利用可能な関数にのみ基づいて行われること、および PingCAP が契約合意の一部として前述の未リリースの機能を提供する義務がないことを承認するものとします。

## 開発者のエクスペリエンスとエンタープライズグレードの機能 {#developer-experience-and-enterprise-grade-features}

<table>
  <thead>
    <tr>
      ドメイン</th><th>特徴</th><th>説明
    </tr>
  </thead>

  <tbody>
    <tr>
      開発者の経験</td><td>✅ サンプル データセットを手動で読み込みます。</td><td>サンプル データセットのクラスターへのロードをサポートします。このデータを使用して、 TiDB Cloudの機能のテストをすぐに開始できます。
    </tr>

    <tr>
      ✅ Chat2Query (AI を活用した SQL エディター) を追加します。</td><td> Chat2Query では、AI に SQL クエリを自動的に生成させることも、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することもできます。
    </tr>

    <tr>
      ✅ データサービスをサポートします。</td><td> Data Service (ベータ) を使用すると、カスタム API エンドポイントを使用した HTTPS リクエスト経由でTiDB Cloudデータの読み取りまたは書き込みができます。
    </tr>

    <tr>
      クラウドプロバイダーマーケットプレイス</td><td>✅ AWS Marketplace と Google Cloud Marketplace のユーザー エクスペリエンスを向上させます。</td><td> AWS Marketplace および Google Cloud Marketplace からサインアップするユーザーのユーザー ジャーニーとエクスペリエンスを向上させます。
    </tr>

    <tr>
      エンタープライズグレードの機能</td><td>✅ 複数の組織のユーザーを管理します。</td><td>招待を受け入れることで、ユーザーが複数の組織に参加できるようにします。
    </tr>

    <tr>
      ✅ 階層的なユーザーの役割と権限をサポートします。</td><td> TiDB Cloudコンソールのロールベースのアクセス制御 (RBAC) をサポートします。ユーザー権限は、クラスター、請求、メンバーごとなど、きめ細かい方法で管理できます。
    </tr>

    <tr>
      UI エクスペリエンス</td><td>✅ より便利なフィードバックチャネルを提供します。</td><td>ユーザーは製品に関するサポートをすぐに受けたり、製品に関するフィードバックを提供したりできます。
    </tr>

    <tr>
      ✅ 左側のナビゲーションを追加します。</td><td> TiDB Cloudコンソールを組織、プロジェクト、ユーザーの構造に表示して、レイアウト ロジックを簡素化し、ユーザー エクスペリエンスを向上させます。
    </tr>

    <tr>
      プレイグラウンドを最適化します。</td><td>ユーザーが TiDB とTiDB Cloudをより深く理解できるよう、コンテキスト主導のチュートリアルを提供します。
    </tr>
  </tbody>
</table>

## TiDB カーネル {#tidb-kernel}

TiDB カーネルのロードマップについては、 [TiDB ロードマップ](https://docs.pingcap.com/tidb/dev/tidb-roadmap)を参照してください。

## 診断とメンテナンス {#diagnosis-and-maintenance}

<table>
  <thead>
    <tr>
      ドメイン</th><th>特徴</th><th>説明
    </tr>
  </thead>

  <tbody>
    <tr>
      レポートを使用したセルフサービスのクラスター分析と診断</td><td>✅クラスタの健全性レポート。</td><td>いくつかの異なる使用シナリオに対する診断および分析レポートを提供します。
    </tr>

    <tr>
      ✅クラスタのステータス比較レポート。</td><td>いくつかのシナリオでクラスターの障害を特定し、推奨される解決策を提供します。
    </tr>

    <tr>
      ✅クラスタシステムのチェックレポート。</td><td>いくつかのシナリオについて、クラスター キーのステータスの概要を提供します。
    </tr>

    <tr>
      HTAP ワークロードの SQL チューニング</td><td>HTAP ワークロードにおけるTiFlashおよび TiKV の SQL の最適化に関する提案を提供します。</td><td> HTAP ワークロードのアプリケーションの観点から SQL 実行の概要を表示するダッシュボードを提供します。
    </tr>

    <tr>
      アプリケーションの観点から SQL 実行情報を提供します。</td><td> 1 つまたは複数の HTAP シナリオについて、SQL の最適化に関する提案を提供します。
    </tr>

    <tr>
      クラスタ診断データへのアクセス可能性</td><td>✅ 診断データにオンラインでリアルタイムにアクセスします。</td><td>さまざまな監視および診断システムと統合して、リアルタイム データ アクセス機能を向上させます。
    </tr>

    <tr>
      ✅ 診断データにオフラインでアクセスします。</td><td>大規模な診断、分析、チューニングのためのオフライン データ アクセスを提供します。
    </tr>

    <tr>
      データ再構築のためのロジックを構築します。</td><td>データの安定性を向上させ、データ再構築のためのロジックを構築します。
    </tr>

    <tr>
      TiDB Cloudサービスのトレース</td><td>TiDB Cloudサービスの各コンポーネントのモニタリング リンクを構築します。

      <td>
        <li>ユーザー シナリオでTiDB Cloudサービスの各コンポーネントのトレース リンクを構築します。</li><li>ユーザーの観点からサービスの可用性を評価します。</li>
      </td>
    </tr>
  </tbody>
</table>

## データのバックアップと移行 {#data-backup-and-migration}

<table>
  <thead>
    <tr>
      ドメイン</th><th>特徴</th><th>説明
    </tr>
  </thead>

  <tbody>
    <tr>
      Kafka/MySQL へのデータ レプリケーション</td><td>✅ TiDB Cloudは、 Kafka/MySQL へのデータのレプリケーションをサポートします。</td><td> TiDB Cloud は、 Kafka および MySQL 互換データベースへの TiCDC ベースのデータ レプリケーションをサポートしています。
    </tr>

    <tr>
      バックアップと復元</td><td>✅ EBS スナップショットベースのバックアップと復元をサポートします。</td><td> TiDB Cloud上のBRサービスは、EBS スナップショットベースのバックアップと復元を使用します。
    </tr>

    <tr>
      バックアップと復元</td><td>AWS EBS または Google Cloud 永続ディスクのスナップショットに基づくバックアップおよび復元サービス。</td><td> AWS EBS または Google Cloud 永続ディスクのスナップショットに基づいて、クラウド上でバックアップおよび復元サービスを提供します。
    </tr>

    <tr>
      オンラインでのデータ移行</td><td>✅ Amazon Relational Database Service (RDS) からの完全なデータ移行をサポートします。</td><td> RDS からTiDB Cloudへの完全なデータ移行。
    </tr>

    <tr>
      RDS からの増分データ移行をサポートします。</td><td> Amazon RDS やAuroraなどの MySQL サービスからTiDB Cloudへの完全および増分データ移行。
    </tr>
  </tbody>
</table>

## Security {#security}

<table>
  <thead>
    <tr>
      ドメイン</th><th>特徴</th><th>説明
    </tr>
  </thead>

  <tbody>
    <tr>
      TLS ローテーション</td><td>TiDB クラスターの TLS ローテーションをサポートします。</td><td> TiDB クラスターでの内部 TLS ローテーション設定と自動更新をサポートします。
    </tr>

    <tr>
      データ暗号化</td><td>顧客管理の暗号化キーの有効化。</td><td>顧客がTiDB Cloud上で独自の KMS 暗号化キーを使用できるようにします。
    </tr>

    <tr>
      データベース監査ログ</td><td>✅ データベース監査ログを強化します。</td><td>データベース監査ログの機能を強化します。
    </tr>

    <tr>
      コンソール監査ログ</td><td>✅ TiDB Cloudコンソール操作の監査をサポートします。</td><td> TiDB Cloudコンソールでのさまざまな操作に対する信頼性の高い監査機能をサポートします。
    </tr>
  </tbody>
</table>
