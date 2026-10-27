---
title: ファイルシステムをマウントする
summary: ファイルシステムをいつマウントするか、どのマウント方法を使用するか、ファイルシステムのマウントで利用できる機能と制限について説明します。
aliases: ['/ja/ai/mount-filesystem']
---

# ファイルシステムをマウントする

TiDB Cloud Filesystem では、エディタ、アプリケーション、エージェント、またはその他のツールでローカルファイルパスが必要な場合に、ファイルシステムをローカルディレクトリとしてマウントできます。マウントすると、これらのツールはローカルのファイル操作を使ってリモートファイルを読み書きできます。

CLI のみでアクセスする場合は、マウントせずに [`ti fs` コマンド](/tidb-cloud-filesystem/work-with-filesystem-data.md) を使用して、ファイルの読み取り、コピー、整理、検索を行ってください。

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能およびインターフェースは予告なく変更される場合があります。

## マウント方法を選択する {#choose-a-mount-method}

利用可能なマウント方法は、環境によって異なります。

| 環境 | マウント方法 | ガイド |
| --- | --- | --- |
| Linux | FUSE | [Linux でファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount-linux.md) |
| macOS | 一般的なファイルアクセスには WebDAV、または FUSE 固有の機能には macFUSE を使用した FUSE | [macOS でファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount-macos.md) |
| Linux 上の Docker | `/dev/fuse` へのアクセスと追加のコンテナ権限を備えた FUSE | [Docker でファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount-docker.md) |

Windows ではネイティブなファイルシステムマウントはサポートされていません。Windows では、代わりに `ti fs copy-file`、`ti fs read-file`、`ti fs list-files` などの直接コマンドを使用してください。

macOS では、一般的なファイルアクセスには WebDAV で十分であり、追加のマウントソフトウェアは不要です。レイヤーやチェックポイントのマウント、`--read-only` を使用したローカルの読み取り専用マウントの作成、`drain-file-system` の使用などの機能には FUSE が必要です。

## プロファイルを設定せずにトークンを使用する {#use-a-token-without-configuring-a-profile}

ファイルシステムトークンとリージョンがあれば、`ti` プロファイルを設定したり TiDB Cloud API キーを指定したりせずにファイルへアクセスできます。

```bash
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

その後、使用する環境向けのガイドに従ってください。トークンはファイルシステムを識別し、現在の環境で利用可能なパスと操作を制限します。トークンは秘密情報として扱ってください。

## 共通のマウント機能 {#common-mount-capabilities}

ファイルシステムのマウントでは、ローカルマウントを通じて公開される内容を変更するための複数のオプションがサポートされています。

### ファイルシステムの一部のみをマウントする {#mount-only-part-of-the-file-system}

デフォルトでは、マウントはファイルシステムのルート `/` を公開します。代わりに特定のリモートディレクトリを公開するには、`--remote-path` を使用します。これは、スコープ付きトークンが特定のパスへのアクセスのみを許可している場合にも便利です。

### 読み取り専用マウントを作成する {#create-a-read-only-mount}

FUSE マウント経由の書き込みを防ぐには、`--driver fuse --read-only` を使用します。WebDAV はこのオプションをサポートしていません。マウントと CLI コマンド全体で読み取り専用アクセスを強制するには、`read` と `list` 権限のみを持つスコープ付きトークンを使用してください。マウントオプションはトークンの権限を変更しません。

### レイヤーとチェックポイントをマウントする {#mount-layers-and-checkpoints}

レイヤーとチェックポイントには FUSE が必要です。チェックポイントのマウントは常に読み取り専用です。

レイヤーおよびチェックポイントのワークフローについては、[ファイルシステムのレイヤーとチェックポイントを管理する](/tidb-cloud-filesystem/manage-filesystem-layers.md) を参照してください。

## 使用前にマウントを検証する {#verify-a-mount-before-using-it}

マウントコマンドが成功したことやディレクトリ一覧が表示できることだけでは、ファイルの読み書きが正常に動作することは確認できません。`ti fs copy-file` でアップロードした既知の小さなファイルを読み取ってください。書き込み可能なマウントの場合は、新しいテストファイルを書き込み、それを閉じて、正常にアンマウントしてください。その後、`ti fs read-file` でそのファイルを読み取り、書き込みがサービスに到達したことを確認します。完全な例については、[Linux の検証手順](/tidb-cloud-filesystem/filesystem-mount-linux.md#mount-and-verify-the-file-system) または [macOS WebDAV の検証手順](/tidb-cloud-filesystem/filesystem-mount-macos.md#mount-with-webdav) に従ってください。

小さなファイルの確認が 30 秒経っても戻らない場合は、中断して [マウントは成功するがファイルアクセスがハングする](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs) に従ってください。検証が成功するまでは、そのマウント上でアプリケーションを起動しないでください。

## 安全に終了する {#finish-safely}

### 作業が終わったらアンマウントする {#unmount-when-you-are-finished}

アプリケーションがマウントされたディレクトリへ書き込むのを停止し、開いているファイルを閉じてから、プラットフォーム別ガイドに従って `ti fs unmount-file-system` を実行してください。通常の FUSE アンマウントでは、マウントを停止する前に保留中の書き込みがフラッシュされます。マシンまたはそのローカルキャッシュを削除する前に、必要なファイルを直接 CLI で読み取って確認してください。アンマウントするとローカルマウントは削除されますが、ファイルシステムやそのデータは削除されません。

### FUSE の書き込み動作 {#fuse-write-behavior}

FUSE マウントでは、サービスへ送信する前に書き込みがローカルでバッファされることがあります。通常のアンマウントにはドレインが含まれるため、事前に `drain-file-system` を実行する必要はありません。アンマウント後にマウントログで `force_quit` または保留中の書き込みが報告された場合は、[アンマウントは成功を返すがマウントプロセスが異常終了する](/tidb-cloud-filesystem/filesystem-troubleshooting.md#unmount-returns-success-but-the-mount-process-exits-abnormally) に従ってください。

`drain-file-system` は、マウントを維持したまま保留中の書き込みをファイルシステムに到達させる必要がある場合にのみ使用してください。たとえば、チェックポイントを作成する前や、更新済みファイルを別の環境で利用可能にする前などです。

WebDAV マウントは `drain-file-system` をサポートしていません。

> **Warning:**
>
> FUSE のドレインまたはアンマウントに失敗した場合は、エラーを解決し、必要なファイルがファイルシステムに到達したことを確認するまで、マウントとマシンを利用可能な状態に保ってください。一部の保留中の書き込みは、まだそのマシン上にしか存在していない可能性があります。

## 次のステップ {#what-s-next}

使用する環境向けのガイドを選択してください。

- [Linux でファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount-linux.md)
- [macOS でファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount-macos.md)
- [Docker でファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount-docker.md)

すべてのマウントオプションについては、[`mount-file-system` コマンドリファレンス](/ai/ti/reference/ti-fs-mount-file-system.md) を参照してください。