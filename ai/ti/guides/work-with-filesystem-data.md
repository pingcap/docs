---
title: TiDB Cloud Filesystem データを操作する
summary: CLI を使用して、TiDB Cloud Filesystem 内のファイルやディレクトリをコピー、読み取り、整理、検索、確認する方法を学びます。
---

# TiDB Cloud Filesystem データを操作する

TiDB Cloud CLI では、[`ti fs` コマンド](/ai/ti/reference/ti-filesystem.md)を使用して、ローカルストレージと TiDB Cloud Filesystem 間でデータを転送したり、リモート名前空間を管理したりできます。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- [Filesystem を作成する](/ai/ti/guides/manage-filesystem-resources.md)か、既存の Filesystem へのアクセス権を取得します。
- `--file-system-id` を渡す、`TI_FS_FILE_SYSTEM_ID` を設定する、または対象を識別する FS トークンを指定して、Filesystem を選択します。各操作に必要な権限を持つ FS トークンを指定してください。

## データをコピーする {#copy-data}

ローカルファイルをリモートパスにアップロードします。

```shell
ti fs copy-file --from-local ./report.md --to-remote /reports/report.md
```

[`copy-file`](/ai/ti/reference/ti-fs-copy-file.md) は、ダウンロード、ストリーミング、追記、再開、再帰コピーもサポートしています。

## データを読み取り確認する {#read-and-inspect-data}

ファイルまたはバイト範囲を標準出力に読み取ります。

```shell
ti fs read-file --path /reports/report.md --offset 0 --length 1024
```

ディレクトリを一覧表示し、1 つのパスを確認します。

```shell
ti fs list-files --path /reports --output text
ti fs describe-file --path /reports/report.md
```

## 名前空間を整理する {#organize-the-namespace}

対応するコマンドを使用して、ディレクトリを作成し、ファイルを移動し、データを削除します。

```shell
ti fs create-directory --path /reports/archive
ti fs move-file --from-remote /draft.md --to-remote /reports/final.md
ti fs delete-file --path /scratch --recursive
```

また、`chmod-file`、`create-symlink`、`create-hardlink` を使用して、POSIX スタイルのメタデータやリンクを管理することもできます。

> **Warning:**
>
> `delete-file --recursive` は、対象ディレクトリとその内容を完全に削除します。コマンドを実行する前に、リモートパスを確認してください。

## データを検索する {#search-for-data}

パス配下のファイル内容を検索します。

```shell
ti fs search-file-content --path /reports --pattern "TODO"
```

名前、タイプ、タグ、サイズ、またはタイムスタンプでパスを検索します。

```shell
ti fs find-files --path /reports --file-name-pattern "*.md" --tag stage=review
```

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem のレイヤーとチェックポイントを管理する](/ai/ti/guides/manage-filesystem-layers.md)
- [TiDB Cloud Filesystem をマウントする](/ai/ti/guides/mount-filesystem.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
