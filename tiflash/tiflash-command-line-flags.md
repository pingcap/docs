---
title: TiFlash Command-line Flags
summary: TiFlashのコマンドライン起動フラグについて学習します。
---

# TiFlashコマンドラインフラグ {#tiflash-command-line-flags}

このドキュメントでは、 TiFlash を起動するときに使用できるコマンドライン フラグについて説明します。

## <code>server --config-file</code> {#code-server-config-file-code}

-   TiFlash構成ファイルのパスを指定します
-   デフォルト： &quot;&quot;
-   設定ファイルを指定する必要があります。詳細な設定項目については[TiFlash構成パラメータ](/tiflash/tiflash-configuration.md)を参照してください。

## <code>dttool migrate</code> {#code-dttool-migrate-code}

-   DTFile のファイル形式を移行します (テストまたはダウングレード用)。データは 1 つの DTFile 単位で移行されます。テーブル全体を移行する場合は、 `<data dir>/t_<table id>/stable/dmf_<file id>`に類似したすべてのパスを見つけて、1 つずつ移行する必要があります。スクリプトを使用して移行を自動化できます。

-   ユーザーシナリオ:

    -   データ検証が有効になっているバージョン &gt;= v5.4.0 からバージョン &lt; v5.4.0 にTiFlash をダウングレードする必要がある場合は、このツールを使用して DTFile のデータ形式をダウングレードできます。
    -   TiFlash をバージョン &gt;= v5.4.0 にアップグレードし、既存のデータのデータ検証を有効にする場合は、このツールを使用して DTFile のデータ形式をアップグレードできます。
    -   さまざまな構成で DTFile のスペース使用量と読み取り速度をテストします。
    -   小さなファイルのマージが有効になっているバージョン &gt;= v7.3.0 (つまり、 `storage.format_version` &gt;= 5) からバージョン &lt; v7.3.0 にTiFlash をダウングレードする必要がある場合は、このツールを使用して DTFile のデータ形式をダウングレードできます。

-   パラメータ:
    -   `--imitative` : DTFile の暗号化機能を使用しない場合は、このフラグを使用して構成ファイルの使用と PD への接続を回避できます。
    -   `--version` : DTFile のターゲット バージョン。値のオプションは`1` 、 `2` (既定値)、 `3`です。 `1`は古いバージョン、 `2`新しいチェックサムに対応するバージョン、 `3`小さなファイルのマージをサポートするバージョンです。
    -   `--algorithm` : データ検証に使用されるハッシュ アルゴリズム。値のオプションは`xxh3` (デフォルト)、 `city128` 、 `crc32` 、 `crc64` 、および`none`です。このパラメーターは`version`が`2`の場合にのみ有効です。
    -   `--frame` : 検証フレームのサイズ。デフォルト値は`1048576`です。このパラメータは`version`が`2`場合にのみ有効です。
    -   `--compression` : ターゲット圧縮アルゴリズム。値のオプションは`LZ4` (デフォルト)、 `LZ4HC` 、 `zstd` 、および`none`です。
    -   `--level` : ターゲットの圧縮レベル。指定しない場合は、圧縮アルゴリズムに応じて、推奨される圧縮レベルがデフォルトで使用されます。2 `compression` `LZ4`または`zstd`に設定されている場合、デフォルトのレベルは 1 です`compression`が`LZ4HC`に設定されている場合、デフォルトのレベルは 9 です。
    -   `--config-file` : `dttool migrate`の設定ファイルは[`server`の設定ファイル](/tiflash/tiflash-command-line-flags.md#server---config-file)と同じです。詳細については`--imitative`参照してください。
    -   `--file-id` : DTFile の ID。たとえば、DTFile `dmf_123`の ID は`123`です。
    -   `--workdir` : `dmf_xxx`の親ディレクトリ。
    -   `--dry` : ドライランモード。移行プロセスのみが出力されます。
    -   `--nokeep` : 元のデータを保持しません。このオプションが有効になっていない場合、 `dmf_xxx.old`ファイルが作成されます。

> **警告：**
>
> TiFlash は、カスタム圧縮アルゴリズムと圧縮レベルを使用する DTFile を読み取ることができます。ただし、デフォルトの圧縮レベルを持つ`lz4`アルゴリズムのみが正式にサポートされています。カスタム圧縮パラメータは十分にテストされておらず、実験的ものにすぎません。

> **注記：**
>
> セキュリティ上の理由から、DTTool は移行モードで作業ディレクトリにロックを追加しようとします。そのため、同じディレクトリでは、同時に 1 つの DTTool のみが移行タスクを実行できます。ロックが解除されていない状態で DTTool を強制的に停止すると、後で DTTool を再実行しようとしたときに、移行タスクの実行が拒否される可能性があります。
>
> このような状況が発生した場合、LOCK ファイルを削除してもデータが破損しないことがわかっている場合は、作業ディレクトリ内の LOCK ファイルを手動で削除してロックを解除できます。

## <code>dttool bench</code> {#code-dttool-bench-code}

-   DTFile の基本的な I/O 速度テストを提供します。
-   パラメータ:

    -   `--version` : DTFileのバージョン。2 [`dttool migrate`の`--version`](#dttool-migrate)参照してください。
    -   `--algorithm` : データ検証に使用されるハッシュアルゴリズム。2 [`dttool migrate`の`--algorithm`](#dttool-migrate)参照してください。
    -   `--frame` : 検証フレームのサイズ。2 [`--frame` `dttool migrate`で使用](#dttool-migrate)参照してください。
    -   `--column` : テストするテーブルの列。デフォルト値は`100`です。
    -   `--size` : テストするテーブルの行。デフォルト値は`1000`です。
    -   `--field` : テストするテーブルのフィールド長の制限。デフォルト値は`1024`です。
    -   `--random` : ランダム シード。このパラメータを指定しない場合、ランダム シードはシステム エントロピー プールから取得されます。
    -   `--encryption` : 暗号化機能を有効にします。
    -   `--repeat` : テストを繰り返す回数。デフォルト値は`5`です。
    -   `--workdir` : テスト対象のファイル システム内のパスを指す一時データ ディレクトリ。デフォルト値は`/tmp/test`です。

## <code>dttool inspect</code> {#code-dttool-inspect-code}

-   DTFile の整合性をチェックします。データ検証は、単一の DTFile 単位で実行されます。テーブル全体を検証する場合は、 `<data dir>/t_<table id>/stable/dmf_<file id>`に類似するすべてのパスを見つけて、1 つずつ検証する必要があります。スクリプトを使用して検証を自動化できます。

-   ユーザーシナリオ:

    -   形式のアップグレードまたはダウングレードを実行した後、DTFile のデータ整合性を検証できます。
    -   DTFile を新しい環境に移行した後、DTFile のデータ整合性を検証できます。

-   パラメータ:

    -   `--config-file` : `dttool bench`の設定ファイル[`dttool migrate`の`--config-file`](#dttool-migrate)を参照してください。
    -   `--check` : ハッシュ検証を実行します。
    -   `--file-id` : DTFileのID。2 [`dttool migrate`の`--file-id`](#dttool-migrate)参照してください。
    -   `--imitative` : データベースのコンテキストを模倣します。 [`dttool migrate`の`--imitative`](#dttool-migrate)を参照してください。
    -   `--workdir` : データディレクトリ。2 [`dttool migrate`の`--workdir`](#dttool-migrate)参照してください。
