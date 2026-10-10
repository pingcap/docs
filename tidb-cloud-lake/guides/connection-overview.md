---
title: TiDB Cloud Lake への接続
summary: TiDB Cloud Lake は、さまざまなユースケースに対応するために複数の接続方法をサポートしています。以下のすべてのオプションは、**TiDB Cloud Lake** と **self-hosted {{{ .lake }}}** の両方で利用できます。
---

# TiDB Cloud Lake への接続

{{{ .lake }}} は、さまざまなユースケースに対応するために複数の接続方法をサポートしています。

## クイック選択 {#quick-selection}

| したいこと | 推奨 |
|-------------|-------------|
| 対話的に SQL クエリを実行する | **LakeSQL** (CLI) |
| アプリケーションを構築する | 言語別の **Driver** |
| ダッシュボードやレポートを作成する | **BI/可視化ツール** |

## 接続文字列 {#connection-strings}

| デプロイメント | 形式 |
|------------|--------|
| **{{{ .lake }}}** | `lake://<user>:<pass>@<tenant>.gw.<region>.default.tidbcloud.com:443/<db>?warehouse=<name>` |

> **Tip:**
>
> **{{{ .lake }}}**: ログイン → **Connect** をクリック → 生成された DSN をコピー

## SQL クライアント {#sql-clients}

| ツール | 種類 | 最適な用途 |
|------|------|----------|
| [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) | CLI | 開発者、スクリプト、自動化 |

## ドライバー {#drivers}

| 言語 | ガイド | ユースケース |
|----------|-------|----------|
| Go | [Golang Driver](/tidb-cloud-lake/guides/connect-using-golang.md) | バックエンドサービス、マイクロサービス |
| Python | [Python Connector](/tidb-cloud-lake/guides/connect-using-python.md) | データサイエンス、分析、ML |
| Node.js | [Node.js Driver](/tidb-cloud-lake/guides/connect-using-node-js.md) | Web アプリケーション |
| Java | [JDBC Driver](/tidb-cloud-lake/guides/connect-using-java.md) | エンタープライズアプリケーション |
| Rust | [Rust Driver](/tidb-cloud-lake/guides/connect-using-rust.md) | システムプログラミング |

## 可視化ツール {#visualization-tools}

| ツール | 種類 |
|------|------|
| [Tableau](/tidb-cloud-lake/guides/tableau.md) | ビジネスインテリジェンス |
| [Deepnote](/tidb-cloud-lake/guides/deepnote.md) | コラボレーションノートブック |