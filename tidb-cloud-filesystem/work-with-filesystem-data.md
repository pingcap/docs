---
title: TiDB Cloud Filesystem でファイルとディレクトリを操作する
summary: コンソールでファイルメタデータを表示し、TiDB Cloud CLI を使用してファイルのアップロード、ダウンロード、読み取り、整理、検索を行う方法を学びます。
aliases: ['/ja/ai/work-with-filesystem-data']
---

# TiDB Cloud Filesystem でファイルとディレクトリを操作する

TiDB Cloud Filesystem では、[TiDB Cloud コンソール](https://tidbcloud.com/) でファイルおよびディレクトリのメタデータを参照したり、TiDB Cloud CLI (`ti`) を使用して、ファイルシステムをマウントせずにファイルのアップロード、ダウンロード、読み取り、整理、検索を行ったりできます。すべてのコマンドとオプションについては、[`ti fs` リファレンス](/ai/ti/reference/ti-filesystem.md)を参照してください。

ファイルシステムをマシンに[マウントする](/tidb-cloud-filesystem/filesystem-mount.md)と、ローカルファイルシステムと同じようにファイルやディレクトリを操作できます。

## 前提条件 {#prerequisites}

以下の前提条件は CLI 操作に適用されます。TiDB Cloud コンソールでファイルメタデータを参照するだけでよい場合は、[ファイルを表示する](#view-files)を参照してください。

- [TiDB Cloud CLI をインストールする](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- [ファイルシステムを作成する](/tidb-cloud-filesystem/manage-filesystem-resources.md)か、既存のファイルシステムへのアクセス権を取得します。
- ファイルシステムを選択し、そのトークンを `ti` から利用できるようにします。利用可能なアクセス方法については、[既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md)を参照してください。

## ファイルを表示する {#view-files}

TiDB Cloud コンソールまたは TiDB Cloud CLI を使用して、ファイルやディレクトリを参照し、そのメタデータを表示できます。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で組織の [**File Systems**](https://tidbcloud.com/filesystems) ページに移動し、クラウドプロバイダーとリージョンを選択してから、対象のファイルシステム名をクリックします。
2. 左側のナビゲーションペインで **Files** をクリックします。このページには、ディレクトリとファイルが、そのタイプ、サイズ、更新時刻とともに一覧表示されます。
3. ディレクトリを展開して内容を参照したり、**Search** を使用して表示中のファイルツリーを絞り込んだり、ファイル名をクリックしてそのメタデータを表示したりできます。

コンソールにはファイルメタデータが表示されます。ファイル内容を読み取ったり、ファイルやディレクトリを変更したりするには、CLI コマンドを使用するか、[ファイルシステムをマウント](/tidb-cloud-filesystem/filesystem-mount.md)してください。

</div>

<div label="CLI" value="cli">

ディレクトリの内容を一覧表示します。

```shell
ti fs list-files --path /reports --output text
```

出力例:

```text
NAME       TYPE  SIZE  MTIME
archive    dir   0     0
report.md  file  23    0
```

ファイルまたはディレクトリのメタデータを確認します。

```shell
ti fs describe-file --path /reports/report.md
```

</div>

</SimpleTab>

## ファイルをアップロードおよびダウンロードする {#upload-and-download-files}

ローカルファイルをファイルシステムにアップロードします。

```shell
ti fs copy-file \
  --from-local ./report.md \
  --to-remote /reports/report.md
```

ファイルシステムからファイルをダウンロードします。

```shell
ti fs copy-file \
  --from-remote /reports/report.md \
  --to-local ./downloads/report.md \
  --create-parents
```

`copy-file` を使用すると、ファイルシステム内でファイルまたはディレクトリをコピーしたり、標準入力または標準出力を介してデータをストリーミングしたり、ファイルに追記したり、中断された転送を再開したりすることもできます。

ディレクトリを再帰的にコピーするには、`--recursive` を使用します。サポートされているすべてのコピー操作とオプションについては、[`copy-file` リファレンス](/ai/ti/reference/ti-fs-copy-file.md)を参照してください。

## ファイルを読み取る {#read-files}

ファイルの内容全体を読み取ります。

```shell
ti fs read-file --path /reports/report.md
```

このコマンドは、ファイル内容を JSON でラップせずに、標準出力へ直接書き出します。

ファイルの一部だけを読み取るには、`--offset` と `--length` を使用します。たとえば、次のコマンドは先頭の 1024 バイトを読み取ります。

```shell
ti fs read-file \
  --path /reports/report.md \
  --offset 0 \
  --length 1024
```

## ファイルとディレクトリを整理する {#organize-files-and-directories}

ディレクトリを作成します。

```shell
ti fs create-directory --path /reports/archive
```

ファイルを別のパスへ移動します。

```shell
ti fs move-file \
  --from-remote /draft.md \
  --to-remote /reports/final.md
```

ファイルまたはディレクトリを削除します。

```shell
ti fs delete-file --path /scratch --recursive
```

> **Warning:**
>
> `delete-file --recursive` は、指定したディレクトリとその内容を完全に削除します。削除する前にパスを確認してください。`--dry-run` を使用すると、データを削除せずにリクエストを検証できます。

POSIX スタイルのメタデータやリンクが必要なワークフローでは、[`chmod-file`](/ai/ti/reference/ti-fs-chmod-file.md)、[`create-symlink`](/ai/ti/reference/ti-fs-create-symlink.md)、[`create-hardlink`](/ai/ti/reference/ti-fs-create-hardlink.md)も使用できます。

## ファイルと内容を検索する {#search-files-and-content}

内容に基づいてファイルを検索するには、`search-file-content` を使用します。

```shell
ti fs search-file-content \
  --path /reports \
  --pattern "TODO"
```

`--pattern` は正規表現や glob ではなく、テキストクエリです。`--limit` を使用して、結果の最大件数を制御できます。

詳細については、[`search-file-content` リファレンス](/ai/ti/reference/ti-fs-search-file-content.md)を参照してください。

内容ではなくファイル自体について何らかの条件が分かっている場合は、`find-files` を使用します。ファイル名、タイプ、タグ、サイズ、更新時刻で絞り込めます。

たとえば、`stage=review` のタグが付いた Markdown ファイルを検索するには、次のようにします。

```shell
ti fs find-files \
  --path /reports \
  --file-name-pattern "*.md" \
  --tag stage=review
```

タグは、`copy-file --tag key=value` を使用してファイルをアップロードするときに設定します。同じパスに対して後からアップロード時に `--tag` を指定すると、以前のタグに追加されるのではなく、以前のタグが置き換えられます。

結果には一致したパスが一覧表示されます。空のテーブルは、コマンドが失敗したことではなく、一致するものがなかったことを意味します。

利用可能なすべてのフィルターについては、[`find-files` リファレンス](/ai/ti/reference/ti-fs-find-files.md)を参照してください。

## スクリプトでコマンド出力を使用する {#use-command-output-in-scripts}

コマンド出力を使用する前に、終了ステータスを確認してください。`read-file` と `copy-file --to-stdout` は、CLI メタデータではなくファイル内容をストリーミングします。これらの内容をキャプチャする場合は、stderr を分離してください。

`ti` v0.2.6 および v0.2.7 では、`create-directory` が `--output json` を指定していても、JSON の結果の前に `created ...` 行を出力することがあります。その出力は単一の JSON ドキュメントとしては解析できません。終了ステータスを確認したうえで、`describe-file` または `list-files` を使ってディレクトリを確認してください。スクリプトでその出力形式に依存する前に、インストール済みバージョンの出力形式を確認してください。

## 次のステップ {#what-s-next}

- [ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md): ローカルディレクトリと既存のローカルツールを通じてファイルシステムデータを操作します。
- [ファイルシステムのレイヤーとチェックポイントを管理する](/tidb-cloud-filesystem/manage-filesystem-layers.md): ベースファイルシステムに適用する前に、分離された変更を作成して確認します。
- [マシン間でファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md): 別のマシンまたは環境にファイルシステムへのアクセス権を付与します。
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md): 完全なコマンド構文とオプションを確認します。