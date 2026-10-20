---
title: ファイルシステムでジャーナルを使用する
summary: ファイルシステムジャーナルの作成、ワークフローイベントの記録、読み取り結果と検索結果のページネーション、記録された履歴の検証方法を学びます。
aliases: ['/ja/ai/use-filesystem-journals']
---

# ファイルシステムでジャーナルを使用する

TiDB Cloud Filesystem では、ファイルシステムジャーナルを使用して、タスクの開始、完了、引き継ぎなどのエージェントおよび自動化イベントを、順序付きかつ永続的な記録として保持できます。エントリを読み取ったり検索したりすることで、何が起きたのか、どのエージェントが各アクションを実行したのかを追跡できます。

エントリは追記専用です。イベントを追加することはできますが、既存のエントリを変更することはできません。エントリはハッシュチェーンで連結されているため、整合性と順序を検証できます。

成果物や作業ファイルは、ファイルシステム内の通常のファイルとして保存してください。ジャーナルはイベントを記録するものであり、アクションを再実行したり、ワークフローの出力を置き換えたりするものではありません。

> **Note:**
>
> 現在の `ti` CLI には、個々のジャーナルを削除するコマンドはありません。後で削除する必要が生じる可能性のあるシークレットやその他のデータは記録しないでください。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- [TiDB Cloud CLI をインストールする](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- TiDB Cloud Filesystem 内の既存のファイルシステムにアクセスできること。
- ファイルシステムとそのトークンを `ti` から利用できるようにすること。詳細は [既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) を参照してください。

## ジャーナルを作成する {#create-a-journal}

記録したいワークフロー用のジャーナルを作成します。

```shell
ti fs-journal create-journal \
  --journal-kind agent \
  --title "review task" \
  --actor agent:reviewer
```

ジャーナル ID を省略すると、サービスによってジャーナル ID が生成されます。返された ID は、エントリの追記、読み取り、検証に使用するため保存しておいてください。

ジャーナルの種類、タイトル、actor はコンテキスト情報として機能し、後で関連するワークフロー記録を見つける際にも役立ちます。

## エントリを追記する {#append-entries}

ジャーナルにイベントを追記します。

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --idempotency-key review-started \
  --entry-json '{"type":"review_started"}'
```

各エントリには `type` が必要です。ただし、`--entry-type` で指定する場合は不要です。`summary`、`actor`、`occurred_at` などのフィールドを含めることもできます。

このイベントを再試行する場合は、重複エントリを避けるために同じ `--idempotency-key` を再利用してください。別のイベントには新しいキーを使用してください。

サポートされるすべてのフィールドと入力形式については、[`append-journal-entries` リファレンス](/ai/ti/reference/ti-fs-journal-append-journal-entries.md) を参照してください。

## エントリを読み取って検索する {#read-and-search-entries}

### 1 つのジャーナルを読み取る {#read-one-journal}

1 つのジャーナルの履歴を確認するには、そのエントリを読み取ります。

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>"
```

エントリはシーケンス順で返され、デフォルトでは 1 回の呼び出しにつき最大 100 件まで取得されます。次のページを取得するには、`<last-seq>` を最後に返されたエントリの `seq` に置き換えます。

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>" \
  --after-seq "<last-seq>" \
  --limit 100
```

成功したレスポンスで `entries` 配列が空になるまで、各ページの最後のシーケンスから継続してください。リクエストが失敗した場合は、同じシーケンスから再試行してください。読み取り中でもアクティブなジャーナルには新しいエントリが追加される可能性があり、ページネーションによってスナップショットは作成されません。

### ジャーナルをまたいで検索する {#search-across-journals}

選択したファイルシステム内のジャーナル全体から `review_started` イベントを検索します。

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --limit 100
```

検索では、デフォルトで 1 回の呼び出しにつき最大 100 件まで一致結果が返されます。同じフィルターを維持したまま、最後の一致結果の `cursor` を次のリクエストに渡します。

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --limit 100 \
  --cursor "<last-match-cursor>"
```

成功したレスポンスで `matches` 配列が空になるまで続けてください。リクエストが失敗した場合は、同じ cursor で再試行してください。検索を固定の時間範囲に制限するには、RFC3339 形式の `--since` と `--until` の値を指定し、ページをまたいでも変更しないでください。

完全なエントリ内容を 1 ページ分取得するには、`--include-entries` を追加します。ページネーション時はこれを省略してください。この出力では一致結果の cursor が保持されません。

一致したエントリを個別に取得するには、その `journal_id` を使って `read-journal-entries` を実行し、`--after-seq` を対象エントリの `seq` より 1 小さい値に設定し、`--limit 1` を指定します。たとえば、シーケンス `42` のエントリを読み取るには、`--after-seq 41 --limit 1` を使用します。

## ジャーナルを検証する {#verify-a-journal}

保存されたジャーナル履歴の内部整合性を確認するには、そのハッシュチェーンを検証します。

```shell
ti fs-journal verify-journal \
  --journal-id "<journal-id>"
```

検証が成功すると、保存されているシーケンスとハッシュチェーンに整合性があることが確認されます。ただし、エージェントやアプリケーションによって報告されたイベント自体の正確性を保証するものではありません。

## 次のステップ {#what-s-next}

- エンドツーエンドのエージェントワークフロー例については、[ファイルシステムジャーナルにエージェントワークフローを記録する](/ai/ti/guides/ti-journal-agent-workflow-example.md) を参照してください。
- すべてのジャーナルコマンドとオプションについては、[TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md) を参照してください。