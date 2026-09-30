---
title: Tiered Storage の制限事項
summary: TiDB Cloud Premium または BYOC における tiered storage の制限事項、スロットリング、互換性、およびクエリ性能の不確実性について説明します。
---

# Tiered Storage の制限事項

このドキュメントでは、Infrequent Access (IA) ストレージの現在の制限事項と運用上の影響について説明します。これには、機能上の制約、コールドリードのスロットリング、ツール互換性、およびクエリ性能の不確実性が含まれます。

> **Note:**
>
> tiered storage は {{{ .premium }}} および {{{ .byoc }}} 向けに **private preview** として提供されており、デフォルトでは無効です。利用するには、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) に連絡してインスタンスで有効化してもらう必要があります。このページで説明する動作は現在の preview 実装に基づいており、一般提供 (GA) 前に変更される可能性があります。

## 機能上の制限事項 {#feature-limitations}

| 制限事項 | 説明 |
|-|-|
| Hash / Key partitions | IA に設定できません |
| Index-independent setting | インデックスに対して個別に IA を設定することはできません |
| TTL auto-tiering | 業務フィールドに基づく自動的な cold/hot tiering はサポートされていません |
| Syntax conflict | `STORAGE_CLASS` と `ENGINE_ATTRIBUTE` は同時に指定できません |
| Partition selector mixing | `names_in` / `less_than` / `values_in` は同時に使用できません |
| TiFlash | IA には従わず、データは常にローカルに保持されます |
| Cache level scope | IA の cache level は、個別の論理インスタンスや特定のテーブルまたはパーティションではなく、基盤となる TiKV 物理クラスターのレベルで適用されます。同じ物理クラスターを共有するすべての論理インスタンスは、そのうちのいずれか 1 つで cache level を変更すると影響を受けます。論理インスタンスレベルでの制御は将来のリリースで予定されています |
| Cache level enablement | IA の cache level を変更するには、tiered storage の private preview 有効化に加えて別途 allowlist への登録が必要であり、デフォルトでは無効です。有効化するには [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) に連絡してください |
| Segment size adjustment | `kvengine.ia.segment-size` は {{{ .byoc }}} でのみ変更でき、TiKV ノードの rolling restart 後にのみ有効になります |
| Cache level provisioning | cache level の変更自体は hot update として反映されますが、基盤リソースは TiDB Cloud によって自動的にプロビジョニングされるため、反映までに時間がかかる場合があります |
| Transition progress visibility | `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` の行は、そのテーブルに対する `ALL` 権限を持っている場合にのみ表示されます。アクセスできないテーブルの行は、エラーを出さずにスキップされます |
| Transition progress freshness | 変換の進行状況は 10 秒ごとに収集されるため、`INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` の値はリアルタイムではありません |

## アクセススロットリングの制約 {#access-throttling-constraints}

共有物理クラスターではオブジェクトストレージの帯域幅に限りがあるため、IA コールドストレージへのアクセスは次の制限に従う必要があります。

| 制約の観点 | 制限 | 理由 |
|-|-|-|
| 単一 SQL のコールドリードスループット | ≤ 100 MiB/s | 1 つのクエリが過剰な帯域幅を消費するのを防ぐため |
| コールドリードの同時実行スループット合計 | ≤ 1 GiB/s (≤ 10 concurrent) | クラスター内の他のテナントを保護するため |
| TiKV 単一 miss の load サイズ | ≤ ~3 MiB (estimated) | 3 つの LSM レベルからのセグメント |

> **Note:**
>
> 単一の TiKV miss は、単一のクエリ miss を意味するわけではありません。たとえば、1 つのクエリが複数の TiKV miss（例: 1000）を伴う場合があります。5 台の TiKV ノードがそのクエリを処理する場合、各 TiKV は平均 200 miss を処理し、結果として 200 回のリモート cold data クエリが発生します。各 TiKV 内では並行して処理されるものの、200 miss の処理には非常に長い時間がかかるため、最終的なクエリレイテンシーが極めて高くなる可能性があります。

**業務で cold data への継続的かつ高負荷なアクセスがある場合、IA は推奨されません。テーブルを Standard storage に戻してください。** システムの安定性を確保するため、将来の技術リリースでは cold data アクセスに対するハードスロットリングが追加される予定です。現時点では、上記の制約を順守する必要があります。

単一 SQL による cold data アクセス量は、Cloud Console → Monitoring → Diagnosis → Slow Query → Coprocessor の `IA Remote Read Segment Size` パネルで監視できます。クラスター全体の IA キャッシュ動作を監視するには、[階層型ストレージの可観測性](/tidb-cloud/tiered-storage-observability.md) で説明されている **IA Cache Performance** パネルを使用してください。

## 周辺ツールへの影響 {#impact-on-peripheral-tools}

| ツール | 影響 | 互換性 |
|-|-|-|
| **TiCDC** | 論理データのセマンティクスは変わりません。init scan や古いデータの読み取りではレイテンシーが高くなる可能性があります。リージョン変更は通常どおり処理されます | Compatible |
| **BR backup & restore** | ストレージクラスのメタデータを保持します。restore 後も IA テーブルは IA のセマンティクスで引き続き load されます | Compatible |
| **IMPORT INTO** | インポートされたデータは flush/compaction を通じて IA に移行します。インポート後の大範囲検証では cold cache に遭遇する可能性があります | Compatible |
| **PITR** | ストレージクラスのメタデータを保持します。restore 後に schema manager が再同期されます | Compatible |

## リスク分離メカニズム {#risk-isolation-mechanisms}

テーブルに IA を設定した後、システムは IA テーブルと非 IA テーブルを分離するために次の対策を使用します。

**リージョンレベル**:

- IA テーブル/パーティションは専用のリージョンを占有し、必要に応じて split が発生します
- ストレージクラスが異なる隣接リージョンは merge が制限され、hot/cold data の混在を防ぎます
- 1 つのリージョンは完全に IA であるか、完全に非 IA であるかのいずれかです

**コンピュートレイヤー**:

- Standard テーブルと IA テーブルはコンピュートレイヤーでは分離されません。TiDB にはこの 2 種類のテーブルに対する個別の分離戦略はありません

**ストレージレイヤー**:

- コールドリードのレート制限

> **Note:**
>
> 共有リソース（CPU、ネットワーク、ローカルディスク、オブジェクトストレージ帯域幅）は完全には分離できません。極端な場合、大規模な IA scan が他のテナントに影響する可能性があります。これがアクセススロットリングの制約が存在する根本的な理由です。

## 緊急リカバリ方法 {#emergency-recovery-methods}

IA テーブルで問題が発生した場合、ユーザーと TiDB Cloud チームは次の方法を使用できます。

| 方法 | シナリオ | 優先度 | 説明 |
|-|-|-|-|
| IA → Standard switch-back | 性能が許容できないと判断した場合 | **Your primary choice** | システムがデータをローカルに再ロードし、リモートパスをバイパスします |
| **Flow Control (already available)** | IA テーブルとオブジェクトストレージ間のトラフィックを制御する | TiDB Cloud チームの選択肢 | レート制限によってクラスターの安定性を保護します。TiDB Cloud チームが管理します |
| Contact TiDB Cloud Support | ストレージクラス変換が停止している場合: `DURATION` が増え続ける一方で `COMPLETED_REPLICAS` が増加しない、または `NULL` のままである | Required | 停止した変換はユーザー自身では解決できません。検出方法については、[階層型ストレージの可観測性](/tidb-cloud/tiered-storage-observability.md) を参照してください |

## IA ローカルキャッシュとクエリ性能の不確実性 {#ia-local-cache-and-query-performance-uncertainty}

tiered storage は、最近アクセスされた cold data への繰り返しアクセスを高速化するために、ローカル IA データキャッシュ（IaManager により管理）を維持します。ただし、次の重要な点を理解しておく必要があります。

- **キャッシュ容量は調整可能ですが、キャッシュ動作は引き続きシステム管理です**: Cloud Console で IA cache level を選択し、ローカルディスク上にキャッシュする IA データ量を制御できます。ただし、eviction policy は引き続きシステムによって管理されます。どのデータをキャッシュに残すかを指定することはできず、cache level は個別の論理インスタンス、テーブル、またはパーティションではなく、基盤となる TiKV 物理クラスターに適用されます。キャッシュヒット率は実際のアクセスパターンに依存します。アクセスが集中していれば 95% を超えることがありますが、アクセスが分散している場合は 95% を下回ることがあります。
- **IA クエリの応答時間は決定的ではありません**: クエリがローカルキャッシュにヒットした場合、性能は Standard テーブルに近くなります。しかし、データをリモートオブジェクトストレージからロードする必要がある場合（cache miss）、各リモートリクエストで約 500ms~2s のレイテンシーが追加されます。1 回の SQL 実行で複数回のリモートロードが発生することがあり、その結果レイテンシーが累積します。そのため、IA テーブルのクエリ応答時間は Standard テーブルほど予測可能ではありません。業務側ではこの点を考慮して計画する必要があります。
- **推奨: パーティションテーブルを使用して cold data の範囲を正確に制御する**: パーティションテーブルを使用し、低頻度アクセスであることが確認された履歴パーティションのみを IA に設定し、アクティブなパーティションは Standard のままにしてください。これにより、キャッシュの不確実性を明確に定義されたデータ範囲に限定でき、テーブル全体のクエリ性能を cache miss リスクにさらさずに済みます。
- **キャッシュ領域を増やすことはコスト増加を意味します**: より高い cache level では、より多くの IA データがローカルディスクに保持されるため、より多くのローカルディスクおよび TiKV リソースを消費します。{{{ .premium }}} では、より高い cache level により課金対象の IA ストレージ量が増加します。{{{ .byoc }}} では、追加リソースはお客様自身のクラウドアカウント内にプロビジョニングされ、クラウドプロバイダーから課金され、プロビジョニング完了までに時間がかかります。業務要件に応じて、cold-read 性能とコストのバランスを取ってください。

**要するに:** IA ストレージは、ストレージコストを削減する代わりに、クエリ性能の予測可能性を低下させます。これは設計上避けられないトレードオフです。どのデータを cold data とするかを正確に定義し、その影響をそのデータに限定するために、パーティションテーブルを使用してください。業務で予測可能なクエリ応答時間が必要な場合は、レイテンシーに敏感なデータを Standard storage に保持してください。