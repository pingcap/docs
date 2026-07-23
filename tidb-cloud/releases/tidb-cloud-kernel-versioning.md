---
title: TiDB Cloud Premium のカーネルバージョニング
summary: TiDB Cloud Premium のカーネルのバージョニング規則と形式について説明します。
---

# TiDB Cloud Premium のカーネルバージョニング

このドキュメントでは、TiDB Cloud Premium で使用される基盤データベースカーネルのバージョニング規則について説明します。

> **Note:**
>
> このドキュメントで説明するカーネルバージョニング規則は、TiDB Cloud Premium にのみ適用されます。その他の TiDB Cloud プランでは、異なるカーネルバージョニングモデルが使用されます。
>
> - TiDB Cloud Starter インスタンスは、従来の TiDB v8.5.3 カーネルをベースにしたカスタマイズ済みの TiDB X エンジン上で動作します。このカーネルは、TiDB Cloud Premium のカーネルとは若干異なります。
> - TiDB Cloud Essential インスタンスは、デフォルトで従来の TiDB v8.5.3 カーネルをベースにしたカスタマイズ済みの TiDB X エンジン上で動作します。TiDB Cloud Essential インスタンスを TiDB Cloud Premium と同じカーネルで動作させたい場合は、[TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) にお問い合わせください。
> - TiDB Cloud Dedicated クラスターは、従来の TiDB カーネル上で動作し、そのカーネルバージョンは TiDB Self-Managed のバージョンに直接対応します。

## カーネルバージョニング {#kernel-versioning}

TiDB Cloud Premium のカーネルバージョンは、次の日付ベースの形式を使用します。

```text
TiDB-X-CLOUD.YYYYMM.x
```

例:

```text
TiDB-X-CLOUD.202510.1
```

各要素の意味は次のとおりです。

- `YYYYMM` は、カーネルの開発に使用されたベースラインコードブランチを示します。たとえば、`202510` はベースラインブランチが 2025 年 10 月に作成されたことを意味します。これは、カーネルバージョンのリリース時期を示すものではありません。
- `x` は、そのベースラインブランチに対するパッチリリース番号を示します。

たとえば、`TiDB-X-CLOUD.202510.1` は、そのカーネルが 2025 年 10 月に作成されたブランチに基づいており、そのブランチからビルドされた最初のパッチリリースであることを示します。

カーネルの開発スケジュールとリリーススケジュールは独立しているため、カーネルバージョンはベースラインブランチの作成から数か月後にリリースされる場合があります。

TiDB Cloud Premium は独自のカーネルリリースサイクルに従うため、[TiDB Cloud Premium release notes](/tidb-cloud/releases/tidb-x-cloud.202510.1.md) は [TiDB Self-Managed release notes](https://docs.pingcap.com/releases/tidb-self-managed/) とは別に公開されます。

## FAQ {#faq}

### TiDB Cloud Premium インスタンスのカーネルバージョンを選択できますか？ {#can-i-choose-the-kernel-version-for-my-tidb-cloud-premium-instance}

いいえ。TiDB Cloud は、TiDB Cloud Premium のカーネルライフサイクル全体を管理します。

TiDB Cloud は、新しいデプロイに対して検証済みのカーネルバージョンを自動的に提供し、必要に応じて管理されたアップグレードを実行します。これにより、手動メンテナンスを行うことなく、セキュリティ、安定性、互換性を確保しつつ、最新の機能や改善点を利用できます。