---
title: TiDB Cloud Filesystem FAQ
summary: TiDB Cloud Filesystem の使用方法、共有書き込み、リージョン、マウント、SDK、検索、チェックポイント、プレビュー期間中のポリシー、料金に関する回答を確認できます。
---

# TiDB Cloud Filesystem FAQ

TiDB Cloud Filesystem は現在パブリックプレビュー中です。機能およびインターフェースは予告なく変更される場合があります。

## TiDB Cloud Filesystem とは何ですか？ {#what-is-tidb-cloud-filesystem}

TiDB Cloud Filesystem は、アプリケーション、自動化、AI エージェント向けに永続的で共有可能なファイルストレージを提供します。ファイルは、それを作成したマシンやプロセスとは独立して利用可能な状態が維持されるため、別のセッション、サンドボックス、エージェント、またはレビュアーが同じワークスペースを継続して利用できます。

ファイルには、TiDB Cloud CLI（`ti`）コマンドを使用してアクセスすることも、ファイルシステムをローカルディレクトリとしてマウントしてアクセスすることもできます。TiDB データベースをプロビジョニングしたり管理したりする必要はありません。詳細は、[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) を参照してください。

## サンドボックスですでに永続化が提供されている場合でも、TiDB Cloud Filesystem は必要ですか？ {#do-i-need-tidb-cloud-filesystem-if-my-sandbox-already-provides-persistence}

ワークフローが 1 つのサンドボックスプラットフォーム内で完結する場合は、そのプラットフォームのスナップショット、一時停止と再開機能、または永続ボリュームで十分なことがあります。同じ作業ディレクトリに別のプラットフォーム、マシン、エージェント、レビュアー、または CI ジョブからアクセスする必要がある場合は、TiDB Cloud Filesystem を検討してください。

例については、[自動化と AI エージェントのワークフロー](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md) を参照してください。

## ファイルの変更は他の環境ですぐに利用可能になりますか？ {#are-file-changes-immediately-available-to-other-environments}

必ずしもそうではありません。マウントは、変更をリモートファイルシステムにアップロードする前にローカルでバッファリングすることがあります。FUSE マウントはデフォルトでこの動作を行うため、ローカルで書き込みが完了していても、別の環境ですでに更新済みファイルを読み取れるとは限りません。

FUSE マウントの場合は、アプリケーションによる書き込みを停止し、開いているファイルを閉じてから、[`ti fs drain-file-system --mount-path <local-mount-path>`](/ai/ti/reference/ti-fs-drain-file-system.md) を使用して、マウントを維持したまま保留中の書き込みをアップロードします。通常の FUSE アンマウントでも保留中の書き込みはアップロードされます。WebDAV はこのコマンドをサポートしていないため、アプリケーションによる書き込みを停止し、開いているファイルを閉じてからアンマウントしてください。

マシンまたはそのローカルキャッシュを削除する前に、`ti fs read-file` を使用して、必要な変更がリモートファイルシステムに到達していることを確認してください。drain またはアンマウントに失敗した場合は、リカバリのためにマシンとそのローカルデータを利用可能な状態で保持してください。詳細は、[安全に終了する](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) を参照してください。

## どのリージョンが TiDB Cloud Filesystem をサポートしていますか？ {#which-regions-support-tidb-cloud-filesystem}

現在の一覧については、[サポートされるリージョン](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions) を参照してください。ファイルシステムの提供状況は、TiDB Cloud Starter の提供状況とは異なります。

CLI を使用してファイルシステムを作成する場合は、`ti configure` でサポートされているリージョンを選択するか、コマンドに対して `--region` を使用して設定済みのデフォルトを上書きします。作成手順については、[TiDB Cloud Filesystem を使い始める](/tidb-cloud-filesystem/filesystem-quick-start.md) を参照してください。

## ノートパソコンでファイルシステムをマウントできますか？ {#can-i-mount-a-file-system-on-my-laptop}

はい、macOS または Linux で可能です。評価目的では、ファイルシステムと同じリージョンにあるクラウド仮想マシン（VM）を使用することを推奨します。リモートファイルを読み取るだけでよい場合は、マウントせずに `ti fs read-file` を使用してください。

Windows ではネイティブマウントはサポートされていません。プラットフォーム要件と代替手段については、[ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) を参照してください。

## TiDB Cloud Filesystem は POSIX をサポートしていますか？ {#does-tidb-cloud-filesystem-support-posix}

はい。マウント時、TiDB Cloud Filesystem は POSIX 互換のアクセスを提供します。アプリケーションやエージェントは、通常のローカルパス、シェルコマンド、ファイルシステム API を通じてファイルの読み書きができます。

マウント機能はプラットフォームとドライバーによって異なります。たとえば、レイヤーおよびチェックポイントのマウントには FUSE が必要です。[マウントプラットフォームのサポート](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#mount-platform-support) を参照してください。

## TiDB Cloud Filesystem で利用可能な SDK はありますか？ {#are-sdks-available-for-tidb-cloud-filesystem}

はい。TypeScript、Go、Python、Rust、Kotlin、Swift 向けの Drive9 クライアント SDK を使用できます。Drive9 は、TiDB Cloud Filesystem で使用されているワークスペースエンジンです。

SDK の API キーとしてファイルシステムトークンを使用し、サーバー URL にはファイルシステムのリージョンに対応する TiDB Cloud Filesystem エンドポイントを設定してください。デフォルトの `https://api.drive9.ai` エンドポイントは TiDB Cloud Filesystem トークンを受け付けません。SDK のリリースには、ホスト型サービスではまだサポートされていない操作が含まれる場合があるため、使用前に SDK ドキュメントを確認してください。

エンドポイントの対応表と統合ガイドについては、[TiDB Cloud Filesystem SDKs](/tidb-cloud-filesystem/filesystem-sdks.md) を参照してください。

## ファイルに対してセマンティック検索やベクトル検索を使用できますか？ {#can-i-use-semantic-or-vector-search-over-my-files}

はい。セマンティック検索は、テキストを数値ベクトルとして表現する埋め込みを使用して、意味に基づいてコンテンツを見つけます。画像、音声、動画を検索するには、検索可能なテキストまたは説明を生成するようにメディア抽出を設定してください。

セマンティック検索には埋め込みが必要です。プロバイダーを設定する前に、ファイルシステムの埋め込み設定を確認してください。一部のファイルシステムではサービス管理の埋め込みを使用しており、カスタムプロバイダーを許可していません。メディア抽出とカスタム埋め込みプロバイダーは任意であり、それぞれ個別に設定できます。

`ti fs search-file-content` コマンドは、全文検索用のテキストクエリを受け付け、埋め込みが利用可能な場合はセマンティック検索も行えます。その `--pattern` の値は、正規表現でも glob でもありません。名前、タイプ、タグ、サイズ、更新時刻でパスを検索するには、`ti fs find-files` を使用してください。

設定については、[ファイルシステムの AI プロバイダーを設定する](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md) を参照してください。検索例については、[ファイルとディレクトリを操作する](/tidb-cloud-filesystem/work-with-filesystem-data.md) を参照してください。

## パブリックプレビューではチェックポイントとロールバックをサポートしていますか？ {#does-the-public-preview-support-checkpoints-and-rollback}

はい。レイヤーを使用すると、レイヤーをコミットするまで共有ベースファイルシステムを変更せずにファイルを変更できます。`ti fs create-layer-checkpoint` を使用して、レイヤー履歴内の時点を保存します。`ti fs rollback-layer` を使用して、未コミットの変更を破棄します。

ロールバックでは、以前のチェックポイントは復元されません。チェックポイントから作業を続けるには、それを新しい書き込み可能なレイヤーにフォークしてください。チェックポイントはレイヤー履歴を保持しますが、ベースファイルシステム全体を固定するものではなく、バックアップの代わりにもなりません。複雑なレイヤー履歴には、パブリックプレビュー中に追加の制限があります。詳細は、[境界と制限事項](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md#boundaries-and-limitations) を参照してください。

概念と制限事項については、[レイヤーとチェックポイント](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) を参照してください。コマンドについては、[ファイルシステムのレイヤーとチェックポイントを管理する](/tidb-cloud-filesystem/manage-filesystem-layers.md) を参照してください。

## パブリックプレビュー期間中にサービスレベル契約（SLA）は利用できますか？ {#is-a-service-level-agreement-sla-available-during-public-preview}

いいえ。評価データのバックアップを TiDB Cloud Filesystem の外部に保持し、予期しない動作があれば報告してください。

## パブリックプレビュー終了後、ワークスペースはどうなりますか？ {#what-happens-to-my-workspace-after-public-preview-ends}

パブリックプレビュー終了後にワークスペースを保持するか削除するかのポリシーは、まだ確定していません。重要なデータのバックアップを TiDB Cloud Filesystem の外部に保持してください。

## TiDB Cloud Filesystem の料金はいくらですか？ {#how-much-does-tidb-cloud-filesystem-cost}

TiDB Cloud Filesystem では、読み取り、書き込み、ストレージ、インターネット送信量に対して従量課金制が適用されます。各組織には、すべてのファイルシステム、課金項目、リージョンで共有される月額 $5.00 の無料枠が提供されます。この無料枠は使用料金を減額するものであり、月額請求の上限ではありません。

パブリックプレビュー期間中の価格は、一般提供時に変更される可能性があります。現在のリージョン別料金、無料枠の詳細、クレジットカードなしでの利用制限については、[TiDB Cloud Filesystem Pricing Details](https://www.pingcap.com/tidb-cloud-filesystem-pricing-details/) を参照してください。