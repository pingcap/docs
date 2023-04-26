---
title: TiDB Cloud Roadmap
summary: Learn about TiDB Cloud's roadmap for the next few months. See the new features or improvements in advance, follow the progress, learn about the key milestones on the way.
---

# TiDB Cloudロードマップ {#tidb-cloud-roadmap}

TiDB Cloudのロードマップは、近い将来に何が起こるかを示しているため、新機能や改善点を事前に確認し、進行状況を追跡し、途中で重要なマイルストーンについて知ることができます。開発の過程で、このロードマップは、ユーザーのニーズ、フィードバック、および評価に基づいて変更される可能性があります。

✅: 機能または改善はTiDB Cloudで既に利用可能です。

> **セーフ ハーバー ステートメント:**
>
> ドキュメント、ロードマップ、ブログ、ウェブサイト、プレス リリース、または公式声明で説明または参照されている、現在利用できない未リリースの機能 (「未リリースの機能」) は、当社の裁量で変更される可能性があり、計画どおりに提供されないか、まったく提供されない可能性があります。 .お客様は、購入の決定は現在利用可能な関数のみに基づいていること、および PingCAP は、別段の記載がない限り、契約上の合意の一部として前述の未リリースの機能を提供する義務を負わないことを認めます。

## 開発者の経験とエンタープライズ グレードの機能 {#developer-experience-and-enterprise-grade-features}

<table><thead><tr><th>ドメイン</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">開発者の経験</td><td>✅ サンプル データセットを手動でロードします。</td><td>サンプル データセットのクラスターへの読み込みをサポートします。このデータを使用して、 TiDB Cloudの機能のテストをすぐに開始できます。</td></tr><tr><td> ✅ Chat2Query (AI 搭載の SQL エディター) を追加します。</td><td> Chat2Query では、AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で記述して、端末なしでデータベースに対して SQL クエリを実行することができます。</td></tr><tr><td> ✅ サポート データ サービス。</td><td> Data Service (ベータ版) を使用すると、カスタム API エンドポイントを使用して HTTPS 要求を介してTiDB Cloudデータを読み書きできます。</td></tr><tr><td>クラウド プロバイダー マーケットプレイス</td><td>✅ AWS Marketplace と GCP Marketplace からのユーザー エクスペリエンスを向上させます。</td><td> AWS Marketplace と GCP Marketplace からサインアップするユーザーのユーザー ジャーニーとエクスペリエンスを向上させます。</td></tr><tr><td rowspan="2">エンタープライズ グレードの機能</td><td>✅ 複数の組織でユーザーを管理します。</td><td>招待を受け入れることで、ユーザーが複数の組織に参加できるようにします。</td></tr><tr><td>階層的なユーザーの役割と権限をサポートします。</td><td> TiDB Cloudコンソールの役割ベースのアクセス制御 (RBAC) をサポートします。クラスター、課金、メンバーなど、きめ細かい方法でユーザーのアクセス許可を管理できます。</td></tr><tr><td rowspan="3"> UI エクスペリエンス</td><td>✅ より便利なフィードバック チャネルを提供します。</td><td>ユーザーは、製品に関するヘルプやフィードバックをすぐに得ることができます。</td></tr><tr><td> ✅ 左ナビゲーションを追加します。</td><td>組織、プロジェクト、およびユーザーの構造でTiDB Cloudコンソールを表示して、レイアウト ロジックを簡素化し、ユーザー エクスペリエンスを向上させます。</td></tr><tr><td>プレイグラウンドを最適化します。</td><td> Chat2Query と組み合わせて対話性を向上させ、ユーザーがチュートリアルを完了するようにガイドします。</td></tr></tbody></table>

## TiDB カーネル {#tidb-kernel}

TiDB カーネルのロードマップについては、 [TiDB ロードマップ](https://github.com/pingcap/tidb/blob/master/roadmap.md#tidb-kernel)を参照してください。

## 診断とメンテナンス {#diagnosis-and-maintenance}

<table><thead><tr><th>ドメイン</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td rowspan="3">レポートを使用したセルフサービスのクラスター分析と診断</td><td>✅クラスタのヘルス レポート。</td><td>いくつかの異なる使用シナリオの診断および分析レポートを提供します。</td></tr><tr><td> ✅クラスタ状況比較レポート。</td><td>一部のシナリオでクラスターの障害を特定し、推奨される解決策を提供します。</td></tr><tr><td> ✅クラスタシステムチェックレポート。</td><td>一部のシナリオでは、クラスター キーのステータスの概要を提供します。</td></tr><tr><td rowspan="2"> HTAP ワークロードの SQL チューニング</td><td>HTAP ワークロードでのTiFlashおよび TiKV の SQL の最適化に関する提案を提供します。</td><td> HTAP ワークロードのアプリケーションの観点から SQL 実行の概要を表示するダッシュボードを提供します。</td></tr><tr><td>アプリケーションの観点から SQL 実行情報を提供します。</td><td> 1 つまたは複数の HTAP シナリオについて、SQL の最適化に関する提案を提供してください。</td></tr><tr><td rowspan="3">クラスタ診断データのアクセシビリティ</td><td>✅ オンラインで診断データにリアルタイムでアクセスします。</td><td>さまざまな監視および診断システムと統合して、リアルタイムのデータ アクセス機能を向上させます。</td></tr><tr><td> ✅ 診断データにオフラインでアクセスします。</td><td>大規模な診断、分析、およびチューニングのためのオフライン データ アクセスを提供します。</td></tr><tr><td>データ再構築のロジックを構築します。</td><td>データの安定性を向上させ、データ再構築のためのロジックを構築します。</td></tr><tr><td> TiDB Cloudサービスのトレース</td><td>TiDB Cloudサービスの各コンポーネントの監視リンクを構築します。</td><td><ul><li>ユーザー シナリオでTiDB Cloudサービスの各コンポーネントのトレース リンクを構築します。</li><li>ユーザーの視点からサービスの可用性を評価します。</li></ul></td></tr></tbody></table>

## データのバックアップと移行 {#data-backup-and-migration}

<table><thead><tr><th>ドメイン</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>Kafka/MySQL へのデータ複製</td><td>✅ TiDB Cloud はKafka/MySQL へのデータの複製をサポートしています。</td><td> TiDB Cloud は、 Kafka および MySQL 互換データベースへの TiCDC ベースのデータ複製をサポートしています。</td></tr><tr><td>バックアップと復元</td><td>✅ EBS スナップショット ベースのバックアップと復元をサポートします。</td><td> TiDB CloudのBRサービスは、EBS スナップショット ベースのバックアップと復元を使用します。</td></tr><tr><td>バックアップと復元</td><td>AWS EBS または GCP 永続ディスクのスナップショットに基づくバックアップおよび復元サービス。</td><td> AWS EBS または GCP 永続ディスク スナップショットに基づいて、クラウド上でバックアップおよび復元サービスを提供します。</td></tr><tr><td rowspan="2">オンライン データ移行</td><td>✅ Amazon Relational Database Service (RDS) からの完全なデータ移行をサポートします。</td><td> RDS からTiDB Cloudへの完全なデータ移行。</td></tr><tr><td> RDS からの増分データ移行をサポートします。</td><td> Amazon RDS やAuroraなどの MySQL サービスからTiDB Cloudへの完全および増分データ移行。</td></tr></tbody></table>

## Security {#security}

<table><thead><tr><th>ドメイン</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>TLS ローテーション</td><td>TiDB クラスターの TLS ローテーションをサポートします。</td><td> TiDB クラスターでの内部 TLS ローテーション設定と自動更新をサポートします。</td></tr><tr><td>データ暗号化</td><td>顧客管理の暗号化キーの有効化。</td><td>顧客がTiDB Cloudで独自の KMS 暗号化キーを使用できるようにします。</td></tr><tr><td>データベース監査ログ</td><td>✅ データベースの監査ログを強化します。</td><td>データベース監査ロギングの機能を強化します。</td></tr><tr><td>コンソール監査ログ</td><td>✅ TiDB Cloudコンソール操作の監査をサポートします。</td><td> TiDB Cloudコンソールでのさまざまな操作に対する信頼性の高い監査機能をサポートします。</td></tr></tbody></table>
